#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
match_external_pdfs.py - Abgleich externer Literatur-Ordner <-> 26-MPV/Literatur.

Scannt `MPV/Literatur/` (Parent-Verzeichnis) und versucht jede PDF einem
BibKey in `Quellen.bib` zuzuordnen (Autor + Jahr + Titel-Keywords).
Ergebnis:
 - ``EXTERN_ABGLEICH.md`` mit Status pro externer Datei:
   * already-in-26mpv: PDF existiert bereits, identisch gross
   * upgrade-candidate: PDF existiert bereits, aber extern ist groesser/neuer
   * new-for-bibkey: BibKey in bib, aber Volltext fehlt -> kopieren
   * no-bibkey: Kein passender BibKey -> Pascal entscheidet

Kein Kopieren ohne Bestaetigung (Dry-Run Default). Mit ``--apply`` wird kopiert.
"""
from __future__ import annotations
import argparse
import hashlib
import re
import shutil
import sys
import unicodedata
from pathlib import Path
from typing import Any, Optional

HERE = Path(__file__).resolve().parent
LIT_26MPV = HERE / "Literatur"
LIT_EXTERN = HERE.parent / "Literatur"  # C:\...\MPV\Literatur
BIB = HERE / "Quellen.bib"

UMLAUT_MAP = str.maketrans({
    "ä": "ae", "Ä": "ae", "ö": "oe", "Ö": "oe", "ü": "ue", "Ü": "ue",
    "ß": "ss", "é": "e", "è": "e", "ê": "e", "à": "a", "â": "a",
})


def _norm(s: str) -> str:
    return s.translate(UMLAUT_MAP).lower()


def parse_bib() -> dict[str, dict[str, str]]:
    """Liefert {bibkey: {author, year, title}}."""
    if not BIB.exists():
        return {}
    text = BIB.read_text(encoding="utf-8")
    entries = re.findall(r"@\w+\{([^,]+),\s*(.+?)(?=\n@|\Z)", text, re.DOTALL)
    out = {}
    for key, body in entries:
        key = key.strip()

        def f(name: str) -> str:
            m = re.search(name + r"\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}", body, re.IGNORECASE)
            return re.sub(r"[{}]", "", m.group(1)).strip() if m else ""

        out[key] = {
            "author": f("author") or f("editor"),
            "year": f("year"),
            "title": f("title"),
        }
    return out


def _author_surnames(author: str) -> list[str]:
    """Extrahiert Nachnamen aus einem BibTeX-Autorenfeld (A, V and B, V)."""
    if not author:
        return []
    parts = [p.strip() for p in author.split(" and ")]
    out = []
    for p in parts:
        if "," in p:
            out.append(_norm(p.split(",", 1)[0]).strip())
        else:
            toks = p.split()
            if toks:
                out.append(_norm(toks[-1]))
    return [s for s in out if s and len(s) > 2]


def _title_keywords(title: str, n: int = 5) -> list[str]:
    toks = re.findall(r"[a-zA-Z\u00c0-\u024f]{5,30}", _norm(title))
    stop = {"eine", "einer", "eines", "seine", "dass", "dies", "diese", "dieser",
            "unter", "deren", "which", "their", "seine", "einfuehrung"}
    return [t for t in toks if t not in stop][:n]


def _file_hash(p: Path, chunksize: int = 65536) -> str:
    h = hashlib.md5()
    with p.open("rb") as f:
        while chunk := f.read(chunksize):
            h.update(chunk)
    return h.hexdigest()[:16]


# Kuratiertes Mapping: externer Dateiname -> bibkey (oder None, wenn nicht in bib)
# Basiert auf manueller Sichtung. Fuer alle 26 Dateien im externen Ordner.
CURATED_MAPPING: dict[str, Optional[str]] = {
    "Begabte_Migration_Infoblatt_I_Keller_110621.pdf": "kellerkoller2011erkennen",
    "Begabung _ Eine Einführung -- Gabriele Weigand; Victor Müller-Oppliger; Timo Hoyer -- Bookwire GmbH, Darmstadt, 2013 -- WBG Academic --.pdf": "hoyer2013begabung",
    "Begabung_ Eine Einführung (Erziehungswissenschaft kompakt) -- Timo Hoyer, Gabriele Weigand, Victor Müller-Oppliger, -- Erziehungswissenschaft kompakt.pdf": "hoyer2013begabung",
    "Begabungsförderung und Migrationshintergrund_Dissertation Ulrike Leikhof_Online.pdf": "leikhof2021jugendliche",
    "Diagnostik bei Migrantinnen und Migranten _ ein Handbuch  1_ Auflage 2018, Göttingen, 2018 -- Hogrefe Verlag GmbH & Co.pdf": "maehler2018diagnostik",
    "Equitable Identification Practices for.pdf": "alodat2025equitable",
    "Fischer_et_al_2020_Begabungsfoerderung_II.pdf": "fischer2020begabungsfoerderung",
    "Grundwissen Hochbegabung in der Schule -- Behrensen, Solzbacher -- 2016.pdf": None,  # Behrensen/Solzbacher 2016 – NICHT in bib
    "HOCHBEGABUNG UND MIGRATIONSHINTERGRUND.pdf": "reutlinger2015hochbegabung",
    "Hochbegabung _ Erkennen, Verstehen, Fördern -- Preckel, Franzis; Baudson, Tanja Gabriele -- Verlag C_H_ Beck, München, 2013 -- Verlag C_H_.epub": "preckel2013hochbegabung",
    "Hochbegabung_k_ein_Problem.pdf": "brunner2021hochbegabung",
    "Identifying and Serving English Learners in Gifted Education Looking Back and Moving Forward.pdf": "mun2020identifying",
    "Inhaltsverzeichnis Alle gleich alle unterschiedlich Zum Umgang mit Heterogenität in Schule und Unterricht.pdf": "buholzer2010allegleich",
    "Inhaltsverzeichnis Motivation trifft Begabung Begabte Kinder und Jugendliche verstehen und gezielt fördern.pdf": "lehwald2017motivation",
    "Inklusive Bildung im schulischen Mehrebenensystem_ -- Bianca Preuß (auth_) -- 1_ Auflage 2018, Wiesbaden, 2018 -- VS Verlag für Sozialwisse.pdf": None,  # Preuss 2018 – NICHT in bib
    "Jenseits der Norm - hochbegabt und hoch sensibel_ (Leben -- Andrea Brackmann.pdf": None,  # Brackmann – NICHT in bib
    "Migranten mit Potential Dossier MIRAGE def neu.pdf": "stamm2014mirage",
    "Migrationsbewegungen und Bevölkerung mit Migrationshintergrund.pdf": "bfs2022migration",
    "PISA2022-DieSchweizimFokus.pdf": "erzinger2023pisa",
    "Promising Practices for Improving Identification of English Learners for.pdf": "gubbins2020promising",
    "Reintjes_Kunze_Ossowski_2019_Begabungsfoerderung_und_Professionalisierung.pdf": None,  # Reintjes et al 2019 – NICHT in bib
    "Uslucan_-_Vortrag_zu_Begabung_-_Daten_und_Fakten.pdf": "uslucan2012begabung",
    "Utility of Psychometric and Dynamic.pdf": "alhroub2021utility",
    "Zur_Bedeutung_der_graphomotorischen_Prozesse_beim_.pdf": "sturm2016graphomotorik",
    "iPEGE_1_web.pdf": "ipege2009professionelle",
    "vonelternmitmigrationshintergrundlernen.pdf": "kosoroklabhart2021voneltern",
}


def match_file(fname: str, bib: dict[str, dict[str, str]]) -> list[tuple[str, float]]:
    """Liefert Liste (bibkey, score). Nutzt zuerst kuratiertes Mapping, dann Heuristik als Fallback."""
    # Kuratiertes Mapping hat hoechste Prioritaet
    # NFC-normalisieren fuer Unicode-Vergleich (OneDrive speichert NFD)
    fname_nfc = unicodedata.normalize("NFC", fname)
    mapping_nfc = {unicodedata.normalize("NFC", k): v for k, v in CURATED_MAPPING.items()}
    if fname_nfc in mapping_nfc:
        bk = mapping_nfc[fname_nfc]
        if bk:
            return [(bk, 10.0)]  # maximal sicher
        else:
            return []  # explizit NICHT in bib
    # Fallback: alte Heuristik
    fname_norm = _norm(fname)
    scored: list[tuple[str, float]] = []
    for key, meta in bib.items():
        score = 0.0
        surnames = _author_surnames(meta["author"])
        author_hit = sum(1 for sn in surnames if sn in fname_norm)
        if author_hit:
            score += 2.0 * author_hit / max(len(surnames), 1)
        year = meta["year"]
        if year and year in fname_norm:
            score += 1.5
        kws = _title_keywords(meta["title"])
        kw_hit = sum(1 for k in kws if k in fname_norm)
        if kw_hit:
            score += 1.0 * kw_hit / max(len(kws), 1)
        if _norm(key) in fname_norm:
            score += 3.0
        if score > 0:
            scored.append((key, round(score, 2)))
    scored.sort(key=lambda x: -x[1])
    return scored[:3]


def scan() -> list[dict[str, Any]]:
    """Scannt externen Ordner und ordnet jeder PDF einen BibKey zu."""
    if not LIT_EXTERN.exists():
        print(f"ERR: Externer Ordner existiert nicht: {LIT_EXTERN}")
        return []
    bib = parse_bib()
    out: list[dict[str, Any]] = []
    for p in sorted(LIT_EXTERN.iterdir()):
        if p.is_dir():
            continue
        ext = p.suffix.lower()
        if ext not in (".pdf", ".epub"):
            continue
        matches = match_file(p.name, bib)
        best_key = matches[0][0] if matches and matches[0][1] >= 1.5 else None
        status = "no-bibkey"
        target_path: Optional[Path] = None
        note = ""
        if best_key:
            target_dir = LIT_26MPV / best_key
            # Suche existierenden Volltext (pdf oder epub)
            existing_pdf = target_dir / "source.pdf"
            existing_epub = target_dir / "source.epub"
            existing = existing_pdf if existing_pdf.exists() else (existing_epub if existing_epub.exists() else None)
            target_path = target_dir / f"source{ext}"
            if existing:
                # Hash-Vergleich bei gleicher Endung; sonst Groessenvergleich
                if existing.suffix.lower() == ext:
                    try:
                        same = _file_hash(p) == _file_hash(existing)
                    except Exception:
                        same = p.stat().st_size == existing.stat().st_size
                    if same:
                        status = "already-in-26mpv"
                        note = "hash-identisch"
                    else:
                        # Unterschiedlicher Inhalt - pruefen ob Upgrade
                        if p.stat().st_size > existing.stat().st_size * 1.2:
                            status = "upgrade-candidate"
                            note = f"extern {p.stat().st_size//1024}KB vs. {existing.stat().st_size//1024}KB"
                        else:
                            status = "already-in-26mpv"
                            note = "aehnliche Groesse"
                else:
                    # Unterschiedliche Endung (pdf vs. epub)
                    status = "already-in-26mpv"
                    note = f"existiert als {existing.suffix}"
            else:
                status = "new-for-bibkey"
        out.append({
            "filename": p.name,
            "size_kb": p.stat().st_size // 1024,
            "ext": ext,
            "source_path": p,
            "best_key": best_key,
            "matches": matches,
            "status": status,
            "target_path": target_path,
            "note": note,
        })
    return out


def write_report(results: list[dict[str, Any]], out_path: Path) -> None:
    """Schreibt EXTERN_ABGLEICH.md."""
    by_status: dict[str, list] = {}
    for r in results:
        by_status.setdefault(r["status"], []).append(r)

    lines: list[str] = []
    lines.append("# Abgleich externer Literatur-Ordner")
    lines.append("")
    lines.append(f"Externer Ordner: `{LIT_EXTERN}`")
    lines.append("")
    lines.append(f"**Dateien gesamt:** {len(results)}")
    lines.append("")
    lines.append("| Status | Anzahl | Bedeutung |")
    lines.append("|---|---:|---|")
    lines.append(f"| `already-in-26mpv`   | {len(by_status.get('already-in-26mpv', []))} | Bereits in `26-MPV/Literatur/<key>/source.pdf` |")
    lines.append(f"| `upgrade-candidate`  | {len(by_status.get('upgrade-candidate', []))} | Externe Version ist deutlich groesser – evtl. vollstaendiger |")
    lines.append(f"| `new-for-bibkey`     | {len(by_status.get('new-for-bibkey', []))} | BibKey in bib, aber Volltext fehlt bisher – KOPIEREN |")
    lines.append(f"| `no-bibkey`          | {len(by_status.get('no-bibkey', []))} | Kein passender BibKey in `Quellen.bib` – Pascal entscheidet |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Details pro Status
    for status_key, title in [
        ("new-for-bibkey", "## Neu zu kopierende Dateien (`new-for-bibkey`)"),
        ("upgrade-candidate", "## Upgrade-Kandidaten (`upgrade-candidate`)"),
        ("no-bibkey", "## Ohne BibKey-Treffer (`no-bibkey`)"),
        ("already-in-26mpv", "## Bereits vorhanden (`already-in-26mpv`)"),
    ]:
        items = by_status.get(status_key, [])
        if not items:
            continue
        lines.append(title)
        lines.append("")
        lines.append("| Datei | Groesse | Best-Match | Ziel | Hinweis |")
        lines.append("|---|---:|---|---|---|")
        for r in items:
            bk = r["best_key"] or "–"
            matches_str = f"`{bk}`" if bk != "–" else "–"
            target = f"`Literatur/{bk}/source{r['ext']}`" if r["best_key"] else "–"
            note = r.get("note", "")
            lines.append(f"| `{r['filename']}` | {r['size_kb']} KB | {matches_str} | {target} | {note} |")
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  [OK] -> {out_path} ({out_path.stat().st_size} Bytes)")


def apply_copies(results: list[dict[str, Any]], include_upgrades: bool = False) -> tuple[int, int]:
    """Kopiert Dateien mit Status new-for-bibkey (+ optional upgrade-candidate)."""
    copied = 0
    skipped = 0
    for r in results:
        if r["status"] == "new-for-bibkey":
            pass
        elif r["status"] == "upgrade-candidate" and include_upgrades:
            pass
        else:
            continue
        target = r["target_path"]
        if not target:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            # Backup alte Datei
            backup = target.with_suffix(target.suffix + ".bak")
            target.replace(backup)
            print(f"  BACKUP: {target} -> {backup.name}")
        try:
            shutil.copy2(r["source_path"], target)
            copied += 1
            print(f"  COPY: {r['filename']} -> {target}")
        except Exception as e:
            skipped += 1
            print(f"  SKIP: {r['filename']} ({e})")
    return copied, skipped


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Kopiert Dateien mit Status 'new-for-bibkey'")
    ap.add_argument("--apply-upgrades", action="store_true", help="Zusaetzlich: upgrade-candidate kopieren (Backup wird angelegt)")
    args = ap.parse_args()

    print("match_external_pdfs.py")
    print(f"  26-MPV:  {LIT_26MPV}")
    print(f"  Extern:  {LIT_EXTERN}")
    if not LIT_EXTERN.exists():
        print("  ERR: externer Ordner fehlt")
        return 2

    results = scan()
    print(f"  Dateien externer Ordner: {len(results)}")

    from collections import Counter
    counts = Counter(r["status"] for r in results)
    for st, n in counts.most_common():
        print(f"    {st:22s} {n}")

    out_md = HERE / "EXTERN_ABGLEICH.md"
    write_report(results, out_md)

    if args.apply or args.apply_upgrades:
        print("\n  -- Kopiere Dateien --")
        copied, skipped = apply_copies(results, include_upgrades=args.apply_upgrades)
        print(f"\n  Kopiert: {copied},  Uebersprungen: {skipped}")
    else:
        print("\n  (Dry-Run – keine Dateien kopiert. Mit --apply kopieren)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
