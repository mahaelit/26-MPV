#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
link_incollection_to_parent.py - Verknuepft incollection-BibKeys mit ihrem
Sammelband-Volltext, falls der Sammelband als PDF vorliegt.

Viele @incollection-Eintraege in Quellen.bib sind Kapitel aus einem Sammelband
(z.B. Handbuch Begabung 2021, Reintjes 2019). Wenn wir den Sammelband als PDF
haben, liegen die Kapitel implizit darin -- muessen nur verknuepft werden.

Vorgehen:
 1. Parse Quellen.bib: alle @incollection mit booktitle + pages
 2. Matche booktitle gegen bekannte Parent-BibKeys (kuratierte Tabelle)
 3. Wenn Parent-BibKey PDF hat: finde den Kapitel-Split, der den Seitenbereich
    des Kapitels enthaelt, und kopiere ihn als Literatur/<child>/source.pdf
 4. Erzeuge/aktualisiere Literatur/<child>/verified_quotes.md mit Hinweis

Idempotent: Schon existierende source.pdf werden nicht ueberschrieben, ausser
--force. Beleg-Notiz wird in .from_parent.txt dokumentiert.
"""
from __future__ import annotations
import argparse
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Optional

HERE = Path(__file__).resolve().parent
LIT = HERE / "Literatur"
BIB = HERE / "Quellen.bib"

# Kuratiertes Parent-Mapping: normierter booktitle-Substring -> parent_bibkey
PARENT_MAPPING: dict[str, str] = {
    "begabungsfoerderung und professionalisierung": "reintjes2019begabungsfoerderung",
    "inklusive bildung im schulischen mehrebenensystem": "preuss2018inklusive",
    "grundwissen hochbegabung in der schule": "behrensen2016grundwissen",
    "jenseits der norm": "brackmann2013jenseits",
    "handbuch begabung": "muelleroppliger2021handbuch",
}


def norm_umlaut(s: str) -> str:
    return (s.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
             .replace("Ä", "ae").replace("Ö", "oe").replace("Ü", "ue")
             .replace("ß", "ss").replace("{", "").replace("}", "").lower())


def parse_incollection_entries() -> list[dict[str, Any]]:
    """Parst alle @incollection-Eintraege aus Quellen.bib."""
    text = BIB.read_text(encoding="utf-8")
    entries = re.findall(r"@incollection\{([^,]+),(.+?)(?=\n@|\Z)", text, re.DOTALL)
    out: list[dict[str, Any]] = []
    for key, body in entries:
        key = key.strip()

        def f(name: str) -> str:
            m = re.search(name + r"\s*=\s*\{((?:[^{}]|\{[^{}]*\})+)\}", body, re.IGNORECASE)
            return m.group(1).strip() if m else ""

        booktitle = f("booktitle")
        pages = f("pages")
        author = f("author") or f("editor")
        title = f("title")
        year = f("year")
        out.append({
            "key": key,
            "author": author,
            "title": title,
            "year": year,
            "booktitle": booktitle,
            "pages": pages,
        })
    return out


def find_parent(booktitle: str) -> Optional[str]:
    bn = norm_umlaut(booktitle)
    for trigger, parent in PARENT_MAPPING.items():
        if trigger in bn:
            return parent
    return None


_OUTLINE_ROW_RE = re.compile(
    r"^\|\s*\d+\s*\|\s*S\.\s*(\d+)[\s\u2013-]+(\d+)\s*\(\d+\)\s*\|\s*\[`([^`]+)`\]\([^)]+\)\s*\|\s*(.+?)\s*\|",
    re.MULTILINE,
)


def load_parent_outline(parent_key: str) -> list[dict[str, Any]]:
    """Liest _outline.md des Sammelbands und liefert Liste (page_start, page_end, filename, title)."""
    outline = LIT / parent_key / "excerpts" / "_outline.md"
    if not outline.exists():
        return []
    txt = outline.read_text(encoding="utf-8")
    out = []
    for m in _OUTLINE_ROW_RE.finditer(txt):
        out.append({
            "page_start": int(m.group(1)),
            "page_end": int(m.group(2)),
            "file": m.group(3),
            "title": m.group(4).strip(),
        })
    return out


def parse_pages_range(pages: str) -> Optional[tuple[int, int]]:
    """Parst Seitenangaben wie '35--57', '160-172', '35-57'."""
    if not pages:
        return None
    m = re.search(r"(\d+)[\s\u2013\-]+(\d+)", pages)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def find_best_split(parent_outline: list[dict[str, Any]], page_start: int, page_end: int) -> Optional[dict[str, Any]]:
    """Findet den Split, der den angegebenen Seitenbereich am besten abdeckt.

    Strategie: Split mit hoechster Ueberlappung zu [page_start, page_end].
    Bevorzugt: Split, der in der Ueberschrift-Hierarchie oberflaechlich ist
    (also z.B. "4 Begabung..." vor "4.1 Teil A...").
    """
    best: tuple[float, Optional[dict[str, Any]]] = (0.0, None)
    target_len = page_end - page_start + 1
    for sp in parent_outline:
        overlap_start = max(sp["page_start"], page_start)
        overlap_end = min(sp["page_end"], page_end)
        if overlap_end < overlap_start:
            continue
        overlap = overlap_end - overlap_start + 1
        sp_len = sp["page_end"] - sp["page_start"] + 1
        # Score: Wie viel % der Kapitel-Seiten deckt der Split? +
        #        Wie viel % des Splits ist im Kapitel?
        coverage_target = overlap / target_len
        coverage_split = overlap / sp_len
        score = coverage_target * 0.7 + coverage_split * 0.3
        # Bonus fuer passgenauen Start
        if sp["page_start"] == page_start:
            score += 0.3
        # Bonus: bevorzugt gross (ganzes Kapitel) vor klein (nur Unterabschnitt)
        if sp_len >= target_len * 0.8:
            score += 0.1
        if score > best[0]:
            best = (score, sp)
    return best[1]


VQ_HINT_TEMPLATE = """# Verifizierte Zitate – {key}

**Quelle:** {author} ({year}). {title}. In: {booktitle}.
**Sammelband-BibKey:** `{parent_key}` (liegt als PDF vor)
**Seitenbereich im Sammelband:** S. {pages}
**Lokaler Pfad:** `source.pdf` (Auszug aus `../{parent_key}/excerpts/{split_file}`)

> **Hinweis:** Diese Quelle ist ein Kapitel im oben genannten Sammelband. Der Kapitel-Split unter `source.pdf` wurde automatisch durch `link_incollection_to_parent.py` aus dem Sammelband extrahiert.
> Fuer die Verifikation gilt der Kapitel-Split als identisch mit der Originalquelle.

---

## Zitate (gegen die Quelle gegengeprueft)

### Zitat 1 (S. XX)

> „Wortgetreues Zitat hier einfuegen."

**Kontext / Paraphrase:**
<eigene Zusammenfassung in 1-2 Saetzen>

**Verwendet in:**
- Lerndokument: §<Abschnitt>
- Abgabedokument: §<Abschnitt>

---

**Status:** 0 (ungeprueft, aber Volltext vorhanden via Sammelband)
**Verifiziert am:** <YYYY-MM-DD>
**Bearbeitet durch:** Inti Merolli
"""


def ensure_vq_file(child_dir: Path, key: str, entry: dict[str, Any], parent_key: str, split_file: str, force: bool) -> bool:
    """Schreibt verified_quotes.md falls nicht vorhanden (oder force)."""
    vq = child_dir / "verified_quotes.md"
    if vq.exists() and not force:
        return False
    vq.write_text(
        VQ_HINT_TEMPLATE.format(
            key=key,
            author=entry["author"] or "–",
            year=entry["year"] or "–",
            title=entry["title"] or "–",
            booktitle=entry["booktitle"] or "–",
            parent_key=parent_key,
            pages=entry["pages"] or "–",
            split_file=split_file,
        ),
        encoding="utf-8",
    )
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="Ueberschreibt existierende source.pdf und verified_quotes.md")
    ap.add_argument("--apply", action="store_true", help="Fuehrt Verknuepfung wirklich aus. Ohne: Dry-Run")
    args = ap.parse_args()

    entries = parse_incollection_entries()
    print(f"incollection-Eintraege: {len(entries)}")

    # Gruppiere nach parent
    by_parent: dict[str, list[dict[str, Any]]] = {}
    for e in entries:
        parent = find_parent(e["booktitle"])
        if parent:
            by_parent.setdefault(parent, []).append(e)

    stats = {"linked": 0, "skipped_parent_missing": 0, "skipped_exists": 0,
             "skipped_no_split": 0, "skipped_no_pages": 0}

    for parent_key, children in sorted(by_parent.items()):
        parent_pdf = LIT / parent_key / "source.pdf"
        parent_has_pdf = parent_pdf.exists() or (LIT / parent_key / "source.epub").exists()
        print(f"\n=== Parent: {parent_key} ({'OK' if parent_has_pdf else 'FEHLT'}) — {len(children)} Kapitel ===")
        if not parent_has_pdf:
            for c in children:
                stats["skipped_parent_missing"] += 1
                print(f"  [SKIP] {c['key']}: Parent-PDF fehlt")
            continue
        parent_outline = load_parent_outline(parent_key)
        if not parent_outline:
            print(f"  WARN: Keine _outline.md in {parent_key}")
            continue

        for c in children:
            pr = parse_pages_range(c["pages"])
            if not pr:
                stats["skipped_no_pages"] += 1
                print(f"  [SKIP] {c['key']}: Keine Seitenangabe ({c['pages']!r})")
                continue
            ps, pe = pr
            best = find_best_split(parent_outline, ps, pe)
            if not best:
                stats["skipped_no_split"] += 1
                print(f"  [SKIP] {c['key']}: Kein passender Split in [{ps}-{pe}]")
                continue
            # Kopieren
            child_dir = LIT / c["key"]
            child_dir.mkdir(parents=True, exist_ok=True)
            target = child_dir / "source.pdf"
            src_split = LIT / parent_key / "excerpts" / best["file"]
            status_marker = ""
            if target.exists() and not args.force:
                stats["skipped_exists"] += 1
                status_marker = "existiert bereits"
            else:
                if args.apply:
                    if target.exists() and args.force:
                        backup = target.with_suffix(".pdf.bak")
                        target.replace(backup)
                        status_marker = f"BACKUP -> {backup.name}; "
                    shutil.copy2(src_split, target)
                    stats["linked"] += 1
                    status_marker += f"LINKED ({target.stat().st_size // 1024} KB)"
                    # Marker-Datei
                    (child_dir / ".from_parent.txt").write_text(
                        f"parent_key: {parent_key}\n"
                        f"split_file: {best['file']}\n"
                        f"split_pages: {best['page_start']}-{best['page_end']}\n"
                        f"chapter_pages: {ps}-{pe}\n"
                        f"chapter_title: {c['title']}\n",
                        encoding="utf-8",
                    )
                    # verified_quotes.md
                    vq_new = ensure_vq_file(child_dir, c["key"], c, parent_key, best["file"], args.force)
                    if vq_new:
                        status_marker += " + vq-Stub"
                else:
                    status_marker = f"WOULD LINK from {best['file']}"
            print(f"  [{c['key']}] S.{ps}-{pe} -> {best['file']} (Split S.{best['page_start']}-{best['page_end']}): {status_marker}")

    print()
    print("Zusammenfassung:")
    for k, v in stats.items():
        print(f"  {k:30s} {v}")
    if not args.apply:
        print("\n(Dry-Run - keine Aenderungen. Mit --apply wirklich verknuepfen.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
