#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
build_inventar.py - Quellen-Inventar fuer Open-Book-Pruefung.

Erhebt fuer jeden BibKey in Quellen.bib:
  - Cite-Stellen in mpv.tex (aus cite_context.py-Logik; liest _INDEX.md)
  - Dossier-Inhalt: source.pdf | source.epub | _TOC_*.md | verified_quotes.md
  - Ist Volltext vorhanden? TOC? nur bib-Eintrag?
  - Transkript-Verortung (aus Literatur/_transkripte_index.json)
  - Status (aus verified_quotes.md "Status: N")

Schreibt:
  - QUELLEN_INVENTAR.md   (zentrale Inventar-Uebersicht, sortiert nach Cite-Zahl)
  - BESCHAFFUNG.md        (Quellen ohne Volltext mit Cite-Stellen, bibliothekstauglich)

Aufruf:
  python build_inventar.py
"""

from __future__ import annotations
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

# ---------- PATHS ------------------------------------------------------------

HERE = Path(__file__).resolve().parent
BIB = HERE / "Quellen.bib"
TEX_FILES = [HERE / "mpv.tex", HERE / "mpv_abgabedokument.tex"]
LIT = HERE / "Literatur"
INDEX_JSON = LIT / "_transkripte_index.json"
OUT_INVENTAR = HERE / "QUELLEN_INVENTAR.md"
OUT_BESCHAFFUNG = HERE / "BESCHAFFUNG.md"


# ---------- BIB PARSING ------------------------------------------------------

BIB_ENTRY_RE = re.compile(r"@(?P<type>\w+)\s*\{\s*(?P<key>[^,\s]+)\s*,", re.MULTILINE)
BIB_FIELD_RE = re.compile(r"(\w+)\s*=\s*[\{\"]([^\}\"]*)[\}\"]", re.MULTILINE)


def parse_bib(path: Path) -> dict[str, dict[str, str]]:
    """Rudimentaerer .bib-Parser: BibKey -> {type, title, author, year, ...}"""
    if not path.exists():
        return {}
    txt = path.read_text(encoding="utf-8")
    result: dict[str, dict[str, str]] = {}
    # Teile den Text an @<type>{-Stellen
    # Einfacher Ansatz: finde alle Entries und parse jeweils zwischen ihnen
    entries = list(BIB_ENTRY_RE.finditer(txt))
    for i, m in enumerate(entries):
        start = m.start()
        end = entries[i + 1].start() if i + 1 < len(entries) else len(txt)
        chunk = txt[start:end]
        btype = m.group("type").lower()
        bkey = m.group("key").strip()
        fields: dict[str, str] = {"__type": btype}
        for fm in BIB_FIELD_RE.finditer(chunk):
            fields[fm.group(1).lower()] = fm.group(2).strip()
        result[bkey] = fields
    return result


# ---------- TEX CITE-SCAN ----------------------------------------------------

CITE_RE = re.compile(r"\\(?:parencite|textcite|cite|citeauthor|citeyear)\s*\{([^}]+)\}")


def scan_tex_cites(paths: list[Path]) -> dict[str, list[tuple[str, int]]]:
    """Liest alle .tex-Dateien. BibKey -> [(filename_marker, lineno), ...]

    filename_marker: 'L' fuer mpv.tex (Lerndokument), 'A' fuer mpv_abgabedokument.tex (Abgabedokument).
    """
    out: dict[str, list[tuple[str, int]]] = {}
    for path in paths:
        if not path.exists():
            continue
        marker = "A" if "abgabe" in path.name.lower() else "L"
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            for m in CITE_RE.finditer(line):
                for k in [x.strip() for x in m.group(1).split(",")]:
                    if k:
                        out.setdefault(k, []).append((marker, lineno))
    return out


# ---------- DOSSIER-SCAN ------------------------------------------------------

STATUS_RE = re.compile(r"^\*\*Status:\*\*\s*(\d)", re.MULTILINE)


def _count_pdf_pages(pdf_path: Path) -> int:
    """Seitenanzahl per pypdf; 0 bei Fehler."""
    try:
        from pypdf import PdfReader
        return len(PdfReader(str(pdf_path)).pages)
    except Exception:
        return 0


def scan_dossier(key: str) -> dict[str, Any]:
    """Pro Dossier: welche Dateien vorhanden, hat Volltext etc."""
    dd = LIT / key
    info: dict[str, Any] = {
        "dossier_exists": dd.exists(),
        "has_source_pdf": False,
        "has_source_epub": False,
        "has_toc": False,
        "has_verified_quotes": False,
        "has_excerpts_dir": False,
        "n_excerpts_pdf": 0,       # Anzahl PDF-Splits
        "n_excerpts_md": 0,        # Anzahl Markdown-Transkripte (z.B. teil1.md)
        "has_outline_md": False,    # _outline.md vorhanden?
        "n_chapter_pdfs": 0,       # PDFs am Bibkey-Root, die nicht source.* sind
        "chapter_pages": 0,         # Summe Seiten der Kapitel-PDFs
        "chapter_size_mb": 0.0,     # Summe Groesse der Kapitel-PDFs
        "has_outline_root_md": False,  # _outline.md am Bibkey-Root?
        "source_size_mb": 0.0,
        "source_pages": 0,
        "short_pdf": False,         # <15 Seiten: vermutlich nur Auszug/Artikel
        "status": None,
    }
    if not dd.exists():
        return info
    for f in dd.iterdir():
        n = f.name
        if f.is_file():
            if n == "source.pdf":
                info["has_source_pdf"] = True
                info["source_size_mb"] = round(f.stat().st_size / (1024 * 1024), 2)
                info["source_pages"] = _count_pdf_pages(f)
                info["short_pdf"] = 0 < info["source_pages"] < 15
            elif n == "source.epub":
                info["has_source_epub"] = True
                info["source_size_mb"] = round(f.stat().st_size / (1024 * 1024), 2)
            elif n.startswith("_TOC_") and n.endswith(".md"):
                info["has_toc"] = True
            elif n == "_outline.md":
                info["has_outline_root_md"] = True
            elif n == "verified_quotes.md":
                info["has_verified_quotes"] = True
                try:
                    vq = f.read_text(encoding="utf-8")
                    m = STATUS_RE.search(vq)
                    if m:
                        info["status"] = int(m.group(1))
                except Exception:
                    pass
            elif (n.lower().endswith(".pdf") and not n.startswith("source")
                  and not n.startswith(".")):
                # Foto-Kapitel-PDF am Bibkey-Root (z.B. "kap02_...pdf",
                # "s013-038.pdf"). Wird als alternative Volltext-Quelle gezählt,
                # damit die Inventar-Ampel die Realität widerspiegelt.
                info["n_chapter_pdfs"] += 1
                info["chapter_pages"] += _count_pdf_pages(f)
                info["chapter_size_mb"] += round(f.stat().st_size / (1024 * 1024), 2)
        elif f.is_dir() and n == "excerpts":
            info["has_excerpts_dir"] = True
            info["n_excerpts_pdf"] = sum(1 for _ in f.glob("*.pdf"))
            # Markdown-Transkripte (z.B. bei muelleroppliger2021handbuch mit
            # teil1...teil8.md) zählen auch als Volltext-Ersatz.
            info["n_excerpts_md"] = sum(
                1 for p in f.glob("*.md") if p.name != "_outline.md"
            )
            info["has_outline_md"] = (f / "_outline.md").exists()
    return info


# ---------- TRANSKRIPT-INDEX --------------------------------------------------

def load_transkript_index() -> dict[str, dict[str, Any]]:
    if not INDEX_JSON.exists():
        return {}
    try:
        return json.loads(INDEX_JSON.read_text(encoding="utf-8"))
    except Exception:
        return {}


# ---------- FORMATTING --------------------------------------------------------

def fmt_files(info: dict[str, Any]) -> str:
    parts = []
    if info["has_source_pdf"]:
        p = info["source_pages"]
        tag = f"PDF {info['source_size_mb']}MB/{p}S."
        if info["short_pdf"]:
            tag += " (kurz!)"
        parts.append(tag)
    if info["has_source_epub"]:
        parts.append(f"EPUB {info['source_size_mb']}MB")
    if info["n_chapter_pdfs"]:
        # Kapitel-PDFs am Bibkey-Root (z.B. komprimierte Foto-Auszüge)
        parts.append(
            f"{info['n_chapter_pdfs']} Kapitel-PDFs "
            f"({info['chapter_size_mb']:.1f}MB/{info['chapter_pages']}S.)"
        )
    if info["has_toc"]:
        parts.append("TOC")
    if info["has_excerpts_dir"] and info["n_excerpts_pdf"]:
        parts.append(f"{info['n_excerpts_pdf']} Splits")
    if info["has_excerpts_dir"] and info["n_excerpts_md"]:
        parts.append(f"{info['n_excerpts_md']} MD-Transkripte")
    if info["has_verified_quotes"] and info["status"] is not None:
        parts.append(f"vq={info['status']}")
    return ", ".join(parts) if parts else "(leer)"


def coverage_tag(info: dict[str, Any], cite_count: int) -> str:
    """Ampelfarben-Logik fuer das Inventar."""
    if cite_count == 0:
        return "-"
    has_fulltext = (
        info["has_source_pdf"]
        or info["has_source_epub"]
        or info["n_chapter_pdfs"] > 0
        or info["n_excerpts_md"] > 0
    )
    if not has_fulltext:
        return "ORANGE" if info["has_toc"] else "ROT"
    # Volltext vorhanden
    if info["short_pdf"] and info["n_chapter_pdfs"] == 0 and info["n_excerpts_md"] == 0:
        return "GELB-K"  # kurzes PDF - evtl. nur Auszug, vollständigkeit unklar
    s = info["status"]
    if s is not None and s >= 3:
        return "GRUEN"
    if info["n_excerpts_pdf"] > 0 or info["n_chapter_pdfs"] > 0 or info["n_excerpts_md"] > 0:
        return "GELB+"   # Volltext + Splits vorhanden, aber nicht verifiziert
    return "GELB"


# ---------- MAIN --------------------------------------------------------------

def main() -> int:
    print("build_inventar.py")
    bib = parse_bib(BIB)
    if not bib:
        print(f"  [ERR] Quellen.bib nicht lesbar: {BIB}")
        return 1
    print(f"  BibKeys in Quellen.bib:   {len(bib)}")

    cites = scan_tex_cites(TEX_FILES)
    print(f"  BibKeys mit Cites in TeX: {len(cites)}")

    tindex = load_transkript_index()
    print(f"  BibKeys im Transkript-Index: {len(tindex)}")

    rows: list[dict[str, Any]] = []
    def clean_bibstr(s: str) -> str:
        return s.replace("{", "").replace("}", "").replace("\n", " ").strip()

    for key in sorted(bib.keys()):
        ci = cites.get(key, [])
        di = scan_dossier(key)
        ti = tindex.get(key, {}) if tindex else {}
        author_raw = bib[key].get("author") or bib[key].get("editor") or ""
        entry = {
            "key": key,
            "type": bib[key].get("__type", "?"),
            "title": clean_bibstr(bib[key].get("title", ""))[:90],
            "year": bib[key].get("year", "?"),
            "author": clean_bibstr(author_raw)[:70],
            "isbn": clean_bibstr(bib[key].get("isbn", "")),
            "doi": clean_bibstr(bib[key].get("doi", "")),
            "url": clean_bibstr(bib[key].get("url", "")),
            "publisher": clean_bibstr(bib[key].get("publisher", "")),
            "cite_lines": ci,
            "cite_count": len(ci),
            "cite_in_lern": sum(1 for mk, _ in ci if mk == "L"),
            "cite_in_abgabe": sum(1 for mk, _ in ci if mk == "A"),
            "dossier": di,
            "transkript_eintraege": ti.get("n_zitate", 0) if isinstance(ti, dict) else 0,
        }
        entry["coverage"] = coverage_tag(di, len(ci))
        rows.append(entry)

    # --- QUELLEN_INVENTAR.md --------------------------------------------------
    lines: list[str] = []
    lines.append("# Quellen-Inventar (Open-Book-Vorbereitung)")
    lines.append("")
    lines.append("Automatisch erzeugt von `build_inventar.py`. Nicht manuell editieren.")
    lines.append("")
    # Zusammenfassung
    total = len(rows)
    with_cites = sum(1 for r in rows if r["cite_count"] > 0)
    def _has_fulltext(r):
        d = r["dossier"]
        return (
            d["has_source_pdf"]
            or d["has_source_epub"]
            or d["n_chapter_pdfs"] > 0
            or d["n_excerpts_md"] > 0
        )
    with_pdf = sum(1 for r in rows if _has_fulltext(r))
    with_cites_and_pdf = sum(1 for r in rows if r["cite_count"] > 0 and _has_fulltext(r))
    with_cites_no_pdf = sum(1 for r in rows if r["cite_count"] > 0 and not _has_fulltext(r))
    lines.append("## Zusammenfassung")
    lines.append("")
    lines.append(f"- BibKeys gesamt:                 **{total}**")
    lines.append(f"- mit Cite-Stellen in `mpv.tex`:  **{with_cites}**")
    lines.append(f"- mit Volltext (PDF/EPUB):        **{with_pdf}**")
    lines.append(f"- mit Cites UND Volltext:         **{with_cites_and_pdf}**  (gruen-tauglich)")
    lines.append(f"- mit Cites OHNE Volltext:        **{with_cites_no_pdf}**  (zu beschaffen!)")
    lines.append("")
    # Ampel-Verteilung
    from collections import Counter
    amp = Counter(r["coverage"] for r in rows if r["cite_count"] > 0)
    lines.append(f"- Ampel: GRUEN={amp.get('GRUEN', 0)}, GELB+={amp.get('GELB+', 0)}, GELB={amp.get('GELB', 0)}, GELB-K={amp.get('GELB-K', 0)}, ORANGE={amp.get('ORANGE', 0)}, ROT={amp.get('ROT', 0)}")
    lines.append("")
    lines.append("**Legende Ampelfarben:**")
    lines.append("- **GRUEN**: Volltext + Kapitel-Splits + verifiziert (Status >=3). Prüfungsfertig.")
    lines.append("- **GELB+**: Volltext + Kapitel-Splits vorhanden, aber `verified_quotes.md` noch nicht auf Status >=3.")
    lines.append("- **GELB**: Volltext vorhanden, aber weder Kapitel-Splits noch Zitat-Verifikation.")
    lines.append("- **GELB-K**: Volltext vorhanden, aber **kurz (<15 Seiten)** - möglicherweise nur Auszug statt vollständig. **Prüfen!**")
    lines.append("- **ORANGE**: nur `_TOC_*.md` (Inhaltsverzeichnis) vorhanden, Volltext fehlt.")
    lines.append("- **ROT**: weder Volltext noch TOC. **Beschaffung zwingend** falls zitiert.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Tabelle 1: nach Cite-Zahl sortiert, nur relevante Quellen
    lines.append("## Quellen mit Cite-Stellen (sortiert nach Cite-Zahl)")
    lines.append("")
    lines.append("Spalte `L/A`: Zitate im **L**erndokument (`mpv.tex`) / **A**bgabedokument (`mpv_abgabedokument.tex`).")
    lines.append("")
    lines.append("| Cites | L/A | Ampel | BibKey | Jahr | Titel | Dossier |")
    lines.append("|---:|:---:|:---:|---|:---:|---|---|")
    for r in sorted(rows, key=lambda x: (-x["cite_count"], x["key"])):
        if r["cite_count"] == 0:
            continue
        title = r["title"][:70].replace("|", "/")
        files = fmt_files(r["dossier"]).replace("|", "/")
        la = f"{r['cite_in_lern']}/{r['cite_in_abgabe']}"
        lines.append(f"| {r['cite_count']} | {la} | {r['coverage']} | `{r['key']}` | {r['year']} | {title} | {files} |")
    lines.append("")

    # Tabelle 2: nicht-zitierte Quellen (kuratorisch)
    lines.append("## Nicht-zitierte Quellen in `Quellen.bib`")
    lines.append("")
    nc = [r for r in rows if r["cite_count"] == 0]
    if nc:
        lines.append(f"_{len(nc)} BibKeys stehen in `Quellen.bib`, aber werden in `mpv.tex` nicht zitiert._")
        lines.append("")
        lines.append("| BibKey | Jahr | Titel | Dossier |")
        lines.append("|---|:---:|---|---|")
        for r in sorted(nc, key=lambda x: x["key"]):
            title = r["title"][:70].replace("|", "/")
            files = fmt_files(r["dossier"]).replace("|", "/")
            lines.append(f"| `{r['key']}` | {r['year']} | {title} | {files} |")
        lines.append("")
    else:
        lines.append("_Keine unzitierten BibKeys._")
        lines.append("")

    OUT_INVENTAR.write_text("\n".join(lines), encoding="utf-8")
    print(f"  [OK] -> {OUT_INVENTAR}  ({OUT_INVENTAR.stat().st_size} Bytes)")

    # --- BESCHAFFUNG.md -------------------------------------------------------
    proc_rows = [r for r in rows if r["cite_count"] > 0 and r["coverage"] in ("ORANGE", "ROT", "GELB-K")]
    blines: list[str] = []
    blines.append("# Beschaffungsliste fuer Open-Book-Pruefung")
    blines.append("")
    n_rot_orange = sum(1 for r in proc_rows if r["coverage"] in ("ORANGE", "ROT"))
    n_gelb_k = sum(1 for r in proc_rows if r["coverage"] == "GELB-K")
    blines.append(f"_{n_rot_orange} Quellen haben keinen Volltext (ROT/ORANGE) und {n_gelb_k} haben nur kurzen PDF-Auszug (GELB-K, vermutlich unvollständig)._")
    blines.append("")
    blines.append("Nach Priorität (Cite-Zahl) sortiert. Je hoeher die Cite-Zahl, desto kritischer fuer die Pruefung.")
    blines.append("")
    import urllib.parse as _up
    blines.append("| Prio | Cites | BibKey | Jahr | Titel | Dossier | Suchen |")
    blines.append("|---:|---:|---|:---:|---|---|---|")
    for i, r in enumerate(sorted(proc_rows, key=lambda x: (-x["cite_count"], x["key"])), start=1):
        title = r["title"][:70].replace("|", "/")
        files = fmt_files(r["dossier"]).replace("|", "/")
        # Swisscovery-Search-URL: bevorzugt ISBN/DOI, sonst Author+Titel
        if r["isbn"]:
            q = _up.quote_plus(r["isbn"].replace("-", "").replace(" ", ""))
        elif r["doi"]:
            q = _up.quote_plus(r["doi"])
        else:
            q = _up.quote_plus((r["author"][:35] + " " + r["title"][:35]).strip())
        swisscov = f"[Swisscovery](https://swisscovery.slsp.ch/discovery/search?query=any,contains,{q}&tab=41SLSP_NETWORK&search_scope=DN_and_CI&vid=41SLSP_NETWORK:VU1_UNION)"
        blines.append(f"| {i} | {r['cite_count']} | `{r['key']}` | {r['year']} | {title} | {files} | {swisscov} |")
    blines.append("")
    blines.append("---")
    blines.append("")
    blines.append("## Detail je Quelle")
    blines.append("")
    for r in sorted(proc_rows, key=lambda x: (-x["cite_count"], x["key"])):
        blines.append(f"### `{r['key']}`  ({r['cite_count']} Cite-Stellen: L={r['cite_in_lern']} / A={r['cite_in_abgabe']})")
        blines.append("")
        blines.append(f"- **Titel:** {r['title']}")
        blines.append(f"- **Autor(en):** {r['author'] or '(leer in Quellen.bib!)'}")
        blines.append(f"- **Jahr:** {r['year']}")
        blines.append(f"- **Verlag:** {r['publisher'] or '–'}")
        if r["isbn"]:
            blines.append(f"- **ISBN:** {r['isbn']}")
        if r["doi"]:
            blines.append(f"- **DOI:** {r['doi']}")
        if r["url"]:
            blines.append(f"- **URL:** {r['url']}")
        blines.append(f"- **Typ:** `@{r['type']}`")
        blines.append(f"- **Dossier:** `Literatur/{r['key']}/`  ({fmt_files(r['dossier'])})")
        cl = ", ".join(f"{mk}:{ln}" for mk, ln in r["cite_lines"])
        blines.append(f"- **Cite-Zeilen:** {cl}")
        blines.append(f"- **Ampel:** {r['coverage']}")
        blines.append("")
    OUT_BESCHAFFUNG.write_text("\n".join(blines), encoding="utf-8")
    print(f"  [OK] -> {OUT_BESCHAFFUNG}  ({OUT_BESCHAFFUNG.stat().st_size} Bytes)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
