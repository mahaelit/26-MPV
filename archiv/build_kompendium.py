#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
build_kompendium.py - Zentrales Prüfungs-Kompendium für Open-Book.

Für jede Cite-Stelle in `mpv.tex` + `mpv_abgabedokument.tex`:
  - Welcher Satz/Abschnitt in der Arbeit macht die Behauptung?
  - Welche Quelle(n) werden zitiert?
  - Welcher Kapitel-Auszug belegt das (Pfad zum PDF-Split mit Seite)?
  - Ist der Beleg verifiziert (aus verified_quotes.md)?

Ausgabe: `PRUEFUNGSKOMPENDIUM.md` mit:
  1. Inhaltsverzeichnis nach Arbeit (Lern- + Abgabedokument)
  2. Pro Fragebereich des Lerndokuments: Claim -> Cite -> Excerpt -> Page
  3. Ampelqualität pro Claim
  4. Fehlende Belege explizit benannt

Aufruf:
  python build_kompendium.py
"""

from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from typing import Any, Optional

# Optionales Modul fuer Claim->Split-Matching
try:
    import claim_split_match as _csm
    HAS_CSM = True
except Exception:
    HAS_CSM = False

HERE = Path(__file__).resolve().parent
LIT = HERE / "Literatur"
TEX_FILES = [
    (HERE / "mpv.tex", "L", "Lerndokument"),
    (HERE / "mpv_abgabedokument.tex", "A", "Abgabedokument"),
]
BIB = HERE / "Quellen.bib"
OUT = HERE / "PRUEFUNGSKOMPENDIUM.md"

CITE_RE = re.compile(r"\\(?P<cmd>parencite|textcite|cite|citeauthor|citeyear)\s*\{(?P<keys>[^}]+)\}")
BIB_ENTRY_RE = re.compile(r"@(?P<type>\w+)\s*\{\s*(?P<key>[^,\s]+)\s*,", re.MULTILINE)
BIB_FIELD_RE = re.compile(r"(\w+)\s*=\s*[\{\"]([^\}\"]*)[\}\"]", re.MULTILINE)

# Regex fuer Abschnittserkennung in mpv.tex (section/subsection/subsubsection)
SECTION_RE = re.compile(r"^\\(?P<level>section|subsection|subsubsection)\*?\s*\{(?P<title>[^}]+)\}", re.MULTILINE)


def parse_bib() -> dict[str, dict[str, str]]:
    if not BIB.exists():
        return {}
    txt = BIB.read_text(encoding="utf-8")
    result = {}
    entries = list(BIB_ENTRY_RE.finditer(txt))
    for i, m in enumerate(entries):
        start = m.start()
        end = entries[i + 1].start() if i + 1 < len(entries) else len(txt)
        chunk = txt[start:end]
        fields = {"__type": m.group("type").lower()}
        for fm in BIB_FIELD_RE.finditer(chunk):
            fields[fm.group(1).lower()] = fm.group(2).strip()
        result[m.group("key").strip()] = fields
    return result


def clean_bib(s: str) -> str:
    return s.replace("{", "").replace("}", "").replace("\n", " ").strip()


def scan_tex(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    """Liefert (cite_entries, lines_of_tex).

    cite_entries: liste von {lineno, keys:list, cmd, context:str, section:str}
    """
    if not path.exists():
        return [], []
    lines = path.read_text(encoding="utf-8").splitlines()
    # Abschnittsrahmen durch lineno -> title
    sections = []  # [(lineno, level, title)]
    for lineno, line in enumerate(lines, start=1):
        m = SECTION_RE.match(line)
        if m:
            sections.append((lineno, m.group("level"), m.group("title").strip()))

    def section_for(lineno: int) -> str:
        cur = ""
        for ln, lvl, title in sections:
            if ln > lineno:
                break
            if lvl == "section":
                cur = f"§ {title}"
            elif lvl == "subsection":
                cur = cur.split(" | ")[0] + f" | {title}"
            elif lvl == "subsubsection":
                base = " | ".join(cur.split(" | ")[:2])
                cur = base + f" | {title}"
        return cur or "(keine Section)"

    cite_entries: list[dict[str, Any]] = []
    for lineno, line in enumerate(lines, start=1):
        # Skip Zeilen, die Cite-Kommandos innerhalb von \verb|...| enthalten (Code-Beispiele)
        # Strategie: entferne \verb|...|-Inhalte vor dem Cite-Match
        scan_line = re.sub(r"\\verb\|[^|]*\|", "", line)
        for m in CITE_RE.finditer(scan_line):
            keys = [k.strip() for k in m.group("keys").split(",") if k.strip()]
            # Filter: Wenn einer der Keys "..." oder ähnliches Pseudo-Platzhalter ist, skip
            if any("." in k or len(k) < 3 for k in keys):
                continue
            # Kontext: ganzer Satz um den Cite (via claim_split_match._sentence_context_around)
            if HAS_CSM:
                ctx = _csm._sentence_context_around(lines, lineno)
            else:
                ctx_lines = lines[max(0, lineno - 3):lineno]
                ctx = " ".join(l.strip() for l in ctx_lines if l.strip()).replace("  ", " ")
            # Leere/Literaturliste-Zeilen (`\item[\cite{...}]`) als solche markieren
            is_list = bool(re.search(r"\\item\[\\cite", line))
            cite_entries.append({
                "lineno": lineno,
                "cmd": m.group("cmd"),
                "keys": keys,
                "context": ctx[-700:],  # letzte 700 Zeichen (ganzer Satz)
                "section": section_for(lineno),
                "is_list": is_list,
                "full_line": line.strip()[:200],
            })
    return cite_entries, lines


def load_excerpts_outline(key: str) -> list[dict[str, Any]]:
    """Liest Literatur/<key>/excerpts/_outline.md und extrahiert Splits."""
    outline = LIT / key / "excerpts" / "_outline.md"
    if not outline.exists():
        return []
    txt = outline.read_text(encoding="utf-8")
    row_re = re.compile(
        r"^\|\s*\d+\s*\|\s*S\.\s*(\d+)[\s\u2013-]+(\d+)\s*\((\d+)\)\s*\|\s*\[`([^`]+)`\]\([^)]+\)\s*\|\s*(.+?)\s*\|",
        re.MULTILINE,
    )
    rows = []
    for m in row_re.finditer(txt):
        title = m.group(5).strip()
        title = re.sub(r"&nbsp;", "", title).strip()
        rows.append({
            "file": m.group(4),
            "title": title,
            "page_start": int(m.group(1)),
            "page_end": int(m.group(2)),
        })
    return rows


def find_verified_quotes_status(key: str) -> tuple[int | None, bool]:
    """(Status, has_verified_file)."""
    vq = LIT / key / "verified_quotes.md"
    if not vq.exists():
        return None, False
    try:
        txt = vq.read_text(encoding="utf-8")
        m = re.search(r"^\*\*Status:\*\*\s*(\d)", txt, re.MULTILINE)
        return (int(m.group(1)) if m else None), True
    except Exception:
        return None, True


def coverage_for_key(key: str) -> dict[str, Any]:
    """Ermittelt Belegqualität einer Quelle."""
    status, has_vq = find_verified_quotes_status(key)
    excerpts = load_excerpts_outline(key)
    pdf = LIT / key / "source.pdf"
    epub = LIT / key / "source.epub"
    has_pdf = pdf.exists()
    has_epub = epub.exists()
    pdf_pages = 0
    if has_pdf:
        try:
            from pypdf import PdfReader
            pdf_pages = len(PdfReader(str(pdf)).pages)
        except Exception:
            pass
    return {
        "has_fulltext": has_pdf or has_epub,
        "has_pdf": has_pdf,
        "has_epub": has_epub,
        "pdf_pages": pdf_pages,
        "short_pdf": has_pdf and 0 < pdf_pages < 15,
        "n_excerpts": len(excerpts),
        "excerpts": excerpts,
        "vq_status": status,
        "has_vq": has_vq,
    }


def ampel(cov: dict[str, Any]) -> str:
    if not cov["has_fulltext"]:
        return "ROT"
    if cov["short_pdf"]:
        return "GELB-K"
    if cov["vq_status"] is not None and cov["vq_status"] >= 3:
        return "GRUEN"
    if cov["n_excerpts"] > 0:
        return "GELB+"
    return "GELB"


def render_kompendium() -> str:
    bib = parse_bib()
    out: list[str] = []
    out.append("# Prüfungskompendium (Open-Book)")
    out.append("")
    out.append("Automatisch erzeugt von `build_kompendium.py`. Nicht manuell editieren.")
    out.append("")
    out.append("**Zweck:** Für jede Zitat-Stelle in `mpv.tex` und `mpv_abgabedokument.tex` zeigt dieses Dokument,")
    out.append("wo der Beleg im Original-PDF zu finden ist (Kapitel-Auszug + Seitenzahl) und ob der Beleg verifiziert ist.")
    out.append("")
    out.append("**Spalten:** `Zeile` = Zeile in TeX-Datei · `Section` = Kapitel der Arbeit · `Belege` = zitierte Quellen mit Ampel")
    out.append("")

    # Zusammenfassung
    all_cites: list[dict[str, Any]] = []
    for tex_path, marker, tex_label in TEX_FILES:
        entries, _ = scan_tex(tex_path)
        for e in entries:
            e["tex_marker"] = marker
            e["tex_label"] = tex_label
            e["tex_file"] = tex_path.name
        all_cites.extend(entries)

    out.append("## Zusammenfassung")
    out.append("")
    out.append(f"- Cite-Stellen gesamt: **{len(all_cites)}**")
    out.append(f"- Davon im Lerndokument: **{sum(1 for c in all_cites if c['tex_marker']=='L')}**")
    out.append(f"- Davon im Abgabedokument: **{sum(1 for c in all_cites if c['tex_marker']=='A')}**")
    list_cites = sum(1 for c in all_cites if c["is_list"])
    out.append(f"- Literatur-Listen-Einträge (keine Inhaltszitate): **{list_cites}**")
    content_cites = len(all_cites) - list_cites
    out.append(f"- Inhaltszitate: **{content_cites}**")
    out.append("")

    # Ampel-Zusammenfassung pro Quelle
    cov_cache = {}
    splits_cache: dict[str, list] = {}
    unique_keys = set()
    for c in all_cites:
        for k in c["keys"]:
            unique_keys.add(k)
    for k in unique_keys:
        cov_cache[k] = coverage_for_key(k)
        if HAS_CSM and cov_cache[k].get("n_excerpts", 0) > 0:
            try:
                splits_cache[k] = _csm.load_splits(k)
            except Exception:
                splits_cache[k] = []
    from collections import Counter
    amp_counter = Counter(ampel(cov_cache[k]) for k in unique_keys)
    out.append(f"- Quellen-Ampel: GRUEN={amp_counter.get('GRUEN', 0)}, GELB+={amp_counter.get('GELB+', 0)}, GELB={amp_counter.get('GELB', 0)}, GELB-K={amp_counter.get('GELB-K', 0)}, ROT={amp_counter.get('ROT', 0)}")
    out.append("")
    out.append("---")
    out.append("")

    # Pro TeX-Datei
    for tex_path, marker, tex_label in TEX_FILES:
        entries_here = [e for e in all_cites if e["tex_marker"] == marker]
        if not entries_here:
            continue
        out.append(f"## {tex_label} (`{tex_path.name}`)")
        out.append("")
        out.append(f"{len(entries_here)} Cite-Stellen.")
        out.append("")

        # Nach Section gruppieren
        section_order: list[str] = []
        by_section: dict[str, list] = {}
        for e in entries_here:
            sec = e["section"]
            if sec not in by_section:
                section_order.append(sec)
                by_section[sec] = []
            by_section[sec].append(e)

        for sec in section_order:
            out.append(f"### {sec}")
            out.append("")
            for e in by_section[sec]:
                marker_label = f"**{marker}:{e['lineno']}**"
                cmd = e["cmd"]
                is_list = e["is_list"]
                if is_list:
                    out.append(f"- {marker_label} `\\{cmd}` in Literatur-Liste:")
                else:
                    out.append(f"- {marker_label} `\\{cmd}`:")
                # Kontext (oder Full Line) in Zitat
                ctx = e["context"].replace("\\parencite", "\\pc").replace("\\textcite", "\\tc")
                if len(ctx) > 250:
                    ctx = "..." + ctx[-250:]
                out.append(f"  > {ctx}")
                # Belege pro Key
                for k in e["keys"]:
                    cov = cov_cache.get(k, {})
                    if not cov:
                        out.append(f"  - `{k}` – **NICHT in Quellen.bib!**")
                        continue
                    a = ampel(cov)
                    bib_entry = bib.get(k, {})
                    title = clean_bib(bib_entry.get("title", ""))[:70]
                    year = bib_entry.get("year", "?")
                    author = clean_bib(bib_entry.get("author") or bib_entry.get("editor") or "")[:50]
                    if is_list:
                        # Liste: nur Kurzeintrag
                        out.append(f"  - **{a}** `{k}` – {author} ({year}): {title}")
                        continue
                    # Ampel + Titel + Beleg-Pfad
                    pieces = [f"**{a}**", f"`{k}`", f"{author} ({year})"]
                    out.append(f"  - " + " · ".join(pieces) + f": {title}")
                    # Beleg-Quelle
                    if cov["has_vq"] and cov["vq_status"] is not None:
                        out.append(f"    - Verifikation: [`Literatur/{k}/verified_quotes.md`](Literatur/{k}/verified_quotes.md) (Status {cov['vq_status']})")
                    if cov["n_excerpts"] > 0:
                        out.append(f"    - Kapitel-Splits: [`Literatur/{k}/excerpts/_outline.md`](Literatur/{k}/excerpts/_outline.md) ({cov['n_excerpts']} Splits)")
                        # Automatischer Split-Vorschlag via Keyword-Matching
                        if HAS_CSM and splits_cache.get(k):
                            try:
                                matches = _csm.match_claim(e["context"], splits_cache[k], top_n=2, min_score=0.08)
                                for im, mt in enumerate(matches, start=1):
                                    out.append(
                                        f"    - Beleg-Vorschlag [{im}] (score {mt['score']:.2f}): "
                                        f"[`{mt['file']}`](Literatur/{k}/excerpts/{mt['file']}) "
                                        f"S. {mt['page_start']}-{mt['page_end']} · {mt['title'][:60]}"
                                    )
                            except Exception:
                                pass
                    elif cov["has_pdf"]:
                        out.append(f"    - Volltext: [`Literatur/{k}/source.pdf`](Literatur/{k}/source.pdf) ({cov['pdf_pages']} Seiten)")
                    elif cov["has_epub"]:
                        out.append(f"    - Volltext: [`Literatur/{k}/source.epub`](Literatur/{k}/source.epub)")
                    else:
                        out.append(f"    - **Volltext fehlt** – Beschaffung: siehe [`BESCHAFFUNG.md`](BESCHAFFUNG.md)")
                out.append("")
        out.append("---")
        out.append("")

    # Legende
    out.append("## Legende Ampelfarben")
    out.append("")
    out.append("- **GRUEN** · Volltext vorhanden + `verified_quotes.md` auf Status ≥3 (wortgetreue Zitate mit Seitenangaben).")
    out.append("- **GELB+** · Volltext + Kapitel-Splits vorhanden, aber keine Zitat-Verifikation.")
    out.append("- **GELB** · Volltext vorhanden, aber keine Splits und keine Verifikation.")
    out.append("- **GELB-K** · Volltext nur als Kurz-Auszug (<15 Seiten) – möglicherweise unvollständig, bitte prüfen.")
    out.append("- **ROT** · Kein Volltext im Dossier. Für die Prüfung beschaffen (siehe `BESCHAFFUNG.md`).")
    out.append("")
    return "\n".join(out)


def main() -> int:
    print("build_kompendium.py")
    content = render_kompendium()
    OUT.write_text(content, encoding="utf-8")
    print(f"  [OK] -> {OUT}  ({OUT.stat().st_size} Bytes, {len(content.splitlines())} Zeilen)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
