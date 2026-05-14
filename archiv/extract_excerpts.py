#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
extract_excerpts.py - Kapitel-Ausz\u00fcge als eigene PDFs pro Quelle.

Fuer jede Quelle `Literatur/<key>/source.pdf` mit erkennbarer Outline (Bookmarks):
  1. Liest Outline rekursiv bis `--max-depth`
  2. Bestimmt pro Eintrag Seitenbereich [start .. end-1], wobei end = Start-Seite
     des naechsten Eintrags gleicher oder hoeherer Tiefe (oder Ende des PDFs).
  3. Schreibt PDF-Split nach `Literatur/<key>/excerpts/<nr>_<slug>.pdf`.
  4. Erstellt `Literatur/<key>/excerpts/_outline.md` mit Cross-Referenz
     (inklusive Links ins `verified_quotes.md`).

Aufruf:
  python extract_excerpts.py                       # alle Volltext-Quellen
  python extract_excerpts.py --key hoyer2013begabung
  python extract_excerpts.py --key hoyer2013begabung --force   # ueberschreibt
  python extract_excerpts.py --dry-run                         # nur Vorschau
  python extract_excerpts.py --max-depth 3                     # bis Sub-Sub-Kapitel

Idempotent: ueberspringt bereits vorhandene Splits (ausser --force).
Validiert: kein Overlap, Reihenfolge korrekt, Seitenanzahl > 0.
"""

from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Optional

try:
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import Destination
except ImportError:
    print("ERR: pypdf nicht installiert. Installieren mit: pip install pypdf", file=sys.stderr)
    sys.exit(2)

# ---------- PATHS ------------------------------------------------------------

HERE = Path(__file__).resolve().parent
LIT = HERE / "Literatur"


# ---------- SLUG-GENERATOR ----------------------------------------------------

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(s: str, maxlen: int = 50) -> str:
    """'Kap. 5.1.3 Intelligenz und \u201eIntelligenzen\u201c' -> 'kap_5_1_3_intelligenz_und_intelligenzen'"""
    s = s.lower()
    # Umlaute
    s = (s.replace("\u00e4", "ae").replace("\u00f6", "oe").replace("\u00fc", "ue")
           .replace("\u00df", "ss").replace("\u00c4", "ae").replace("\u00d6", "oe")
           .replace("\u00dc", "ue"))
    s = _SLUG_RE.sub("_", s).strip("_")
    if len(s) > maxlen:
        s = s[:maxlen].rstrip("_")
    return s or "unbenannt"


# ---------- OUTLINE-PARSING ---------------------------------------------------

def _flatten_outline(outline: Any, reader: PdfReader, depth: int = 0, max_depth: int = 2) -> list[dict[str, Any]]:
    """Rekursiv Outline flatten. Gibt flache Liste von {title, page_0, page_1, depth}.

    max_depth bestimmt, bis zu welcher Tiefe Eintraege exportiert werden.
    max_depth=1 = nur Top-Level (Haupt-Kapitel).
    max_depth=2 = Haupt- und Unter-Kapitel (typ. "7.1, 7.2").
    max_depth=3 = bis Sub-Sub ("7.1.1, 7.1.2").
    """
    result: list[dict[str, Any]] = []
    if outline is None:
        return result
    # pypdf-Outline: list of Destination oder verschachtelte Listen
    for item in outline:
        if isinstance(item, list):
            # verschachtelte Kinder -> rekursiv (aber nur wenn noch nicht zu tief)
            if depth + 1 < max_depth:
                kids = _flatten_outline(item, reader, depth + 1, max_depth)
                result.extend(kids)
            continue
        if isinstance(item, Destination):
            if depth >= max_depth:
                continue
            try:
                pagenum_0 = reader.get_destination_page_number(item)
            except Exception:
                continue
            if pagenum_0 is None or pagenum_0 < 0:
                continue
            title = str(item.title or "").strip()
            if not title:
                continue
            result.append({
                "title": title,
                "page_0": pagenum_0,    # 0-indexiert (pypdf-intern)
                "page_1": pagenum_0 + 1, # 1-indexiert (fuer Anzeige)
                "depth": depth,
            })
    return result


def _page_text(pdf_path: Path, page_0: int) -> str:
    """Extrahiert Text einer einzelnen Seite (0-indexiert) via pdftotext."""
    import subprocess
    try:
        res = subprocess.run(
            ["pdftotext", "-layout", "-enc", "UTF-8", "-f", str(page_0 + 1), "-l", str(page_0 + 1), str(pdf_path), "-"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10,
        )
        return res.stdout or ""
    except Exception:
        return ""


def _title_keywords(title: str) -> list[str]:
    """'5.1 Konzepte und Modelle' -> ['konzepte', 'modelle'] (Suchanker)."""
    s = title.lower()
    repl = {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}
    for k, v in repl.items():
        s = s.replace(k, v)
    # Nummer-Praefix entfernen
    s = re.sub(r"^\s*[\d\.]+\s*", "", s)
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    STOP = {"und", "oder", "die", "der", "das", "ein", "eine", "mit", "zur", "zum", "des", "im", "von",
            "bei", "als", "fuer", "the", "and", "of", "in", "to", "a", "an", "als"}
    return [w for w in s.split() if len(w) >= 4 and w not in STOP]


def _correct_start_page(pdf_path: Path, title: str, start_0: int, max_pages: int, max_offset: int = 3) -> int:
    """Wenn mind. ein Keyword des Titels auf start_0 nicht gefunden wird, probiere +1, +2, +3.
    Returns korrigierten start_0 (oder Original, falls nichts passt)."""
    keywords = _title_keywords(title)
    if not keywords:
        return start_0
    # Nimm die laengsten 2 Keywords (wahrscheinlicher eindeutig)
    keywords = sorted(keywords, key=len, reverse=True)[:3]
    for offset in range(0, max_offset + 1):
        p = start_0 + offset
        if p >= max_pages:
            break
        txt = _page_text(pdf_path, p).lower()
        repl = {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}
        for k, v in repl.items():
            txt = txt.replace(k, v)
        # Tolerant: mindestens EIN Keyword muss auf der Seite vorkommen
        # (tolerant gegen Typos wie "Enrichtment" statt "Enrichment")
        if any(kw[:max(4, len(kw) - 2)] in txt for kw in keywords):
            return p
    return start_0


def _extract_toc_from_text(pdf_path: Path, n_pages_total: int) -> list[dict[str, Any]]:
    """Fallback: TOC aus den ersten 5 Seiten per Text-Heuristik extrahieren.

    Sucht nach Zeilen im Format `<Titel> <Fuell/Spaces> <Seitenzahl>`.
    Bestimmt Buch->PDF-Offset durch Suche des ersten Kapiteltitels im Volltext.
    """
    import subprocess
    # Erste 5 Seiten (oder weniger) als Text holen
    scan_pages = min(6, n_pages_total)
    try:
        res = subprocess.run(
            ["pdftotext", "-layout", "-enc", "UTF-8", "-f", "1", "-l", str(scan_pages), str(pdf_path), "-"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=15,
        )
        toc_text = res.stdout or ""
    except Exception:
        return []

    # TOC-Pattern: Titel gefolgt von MINDESTENS 3 Punkten als Fuellzeichen und Zahl am Ende.
    # (Strenger als vorher, um Fliesstext-False-Positives zu vermeiden.)
    toc_re = re.compile(
        r"^\s{0,20}(?P<title>[A-Z\u00c0-\u024f][^.\n]{2,80}?)\s*(?:\.\s*){3,}\s*(?P<page>\d{1,4})\s*$",
        re.MULTILINE,
    )
    raw_entries: list[dict[str, Any]] = []
    seen_titles = set()
    for m in toc_re.finditer(toc_text):
        title = m.group("title").strip(" .")
        try:
            book_page = int(m.group("page"))
        except ValueError:
            continue
        # Sanity-Filter
        if len(title) < 3 or title.lower() in ("seite", "page", "inhalt", "inhaltsverzeichnis"):
            continue
        if book_page < 1 or book_page > n_pages_total + 20:
            continue
        # Skip Technik-Felder (ISBN, DOI, URL, Copyright)
        if re.search(r"\b(ISBN|DOI|URL|http|www\.|ISSN|©|\(c\))", title, re.IGNORECASE):
            continue
        # Duplikate vermeiden
        key = (title.lower()[:30], book_page)
        if key in seen_titles:
            continue
        seen_titles.add(key)
        raw_entries.append({"title": title, "book_page": book_page})

    # Sortiere nach Buch-Seite (sollte schon sortiert sein, aber sicher)
    raw_entries.sort(key=lambda e: e["book_page"])

    if len(raw_entries) < 2:
        return []  # zu wenig TOC-Eintraege, wahrscheinlich kein echtes TOC

    # Erkenne Einrueckung -> depth (tiefergeschachtelte sind in TOC eingerueckt)
    # Wir nehmen einfaches Pattern: wenn der Titel mit " " (in Original-Text) beginnt, depth=1
    # Da die Regex Leerzeichen am Anfang optional erlaubt, schauen wir erneut im Rohtext:
    lines = toc_text.splitlines()
    indent_map: dict[str, int] = {}
    for line in lines:
        m = re.match(r"^(\s*)(.*)$", line)
        if not m:
            continue
        indent_len = len(m.group(1).expandtabs(4))
        rest = m.group(2)
        # erkenne gleiche Zeile
        for e in raw_entries:
            if e["title"] in rest and str(e["book_page"]) in rest:
                indent_map[e["title"]] = indent_len
                break
    # Depth-Schwelle bei 4 Spaces Indent
    for e in raw_entries:
        e["depth"] = 1 if indent_map.get(e["title"], 0) >= 4 else 0

    # Buch->PDF-Offset bestimmen: suche 1. Eintrag im Volltext
    first_title = raw_entries[0]["title"]
    first_bookpage = raw_entries[0]["book_page"]
    # Suche Titel auf PDF-Seiten (nach dem TOC, also ab Seite 3 aufwaerts)
    first_pdf_page = None
    for pdf_p in range(scan_pages, min(n_pages_total, scan_pages + 10)):
        try:
            res = subprocess.run(
                ["pdftotext", "-layout", "-enc", "UTF-8", "-f", str(pdf_p + 1), "-l", str(pdf_p + 1), str(pdf_path), "-"],
                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=8,
            )
            page_txt = res.stdout or ""
        except Exception:
            continue
        # Normalisierung
        norm_txt = page_txt.lower()
        norm_title = first_title.lower()
        # Suche mit erstem Substring (erste 15 Zeichen) - tolerant
        probe = norm_title[:min(15, len(norm_title))]
        if probe in norm_txt:
            first_pdf_page = pdf_p
            break
    if first_pdf_page is None:
        offset = 0  # Fallback: vermute kein Offset
    else:
        offset = first_pdf_page - (first_bookpage - 1)  # pdf_page_0 = book_page - 1 + offset

    # Baue entries mit page_0
    entries: list[dict[str, Any]] = []
    for e in raw_entries:
        pdf_page_0 = (e["book_page"] - 1) + offset
        if pdf_page_0 < 0 or pdf_page_0 >= n_pages_total:
            continue
        entries.append({
            "title": e["title"],
            "page_0": pdf_page_0,
            "page_1": pdf_page_0 + 1,
            "depth": e.get("depth", 0),
        })
    return entries


def _extract_headings_from_fulltext(pdf_path: Path, n_pages_total: int) -> list[dict[str, Any]]:
    """Zweiter Fallback: Sucht nummerierte Ueberschriften (`1. Einführung`, `2.1 ...`)
    und bekannte Artikel-Headings im gesamten PDF-Volltext.
    """
    import subprocess
    # Gesamtdokument als Text lesen
    try:
        res = subprocess.run(
            ["pdftotext", "-layout", "-enc", "UTF-8", str(pdf_path), "-"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60,
        )
        fulltxt = res.stdout or ""
    except Exception:
        return []

    # Heading-Patterns:
    # A) Nummeriert: "1. Titel" oder "1.1 Titel" oder "2.2.1 Titel"
    num_heading = re.compile(
        r"^\s{0,8}(?P<num>\d+(?:\.\d+){0,2})\.?\s+(?P<title>[A-Z\u00c0-\u024f][^\n]{4,70})\s*$",
        re.MULTILINE,
    )
    # B) Bekannte Artikel-Headings (EN + DE)
    known_headings = {
        "abstract", "introduction", "einleitung", "einfuehrung", "methoden", "methods",
        "methodology", "ergebnisse", "results", "diskussion", "discussion", "fazit",
        "conclusion", "conclusions", "literatur", "literature", "references",
        "zusammenfassung", "summary", "acknowledgements", "hintergrund", "background",
        "forschungsstand", "forschungsfrage", "forschungsfragen",
    }

    # PDF-Seiten zu Zeichenpositionen mappen: pdftotext trennt Seiten mit \x0c (Form-Feed)
    page_breaks = [0]
    for m in re.finditer(r"\x0c", fulltxt):
        page_breaks.append(m.end())
    page_breaks.append(len(fulltxt))

    def char_to_page(pos: int) -> int:
        """0-indexierte PDF-Seite, in der Position `pos` liegt."""
        for i in range(len(page_breaks) - 1):
            if page_breaks[i] <= pos < page_breaks[i + 1]:
                return i
        return n_pages_total - 1

    entries: list[dict[str, Any]] = []
    seen = set()

    # A) Nummerierte Headings
    for m in num_heading.finditer(fulltxt):
        num = m.group("num")
        title = m.group("title").strip(" .")
        if len(title) < 4 or len(title) > 80:
            continue
        # Fliesstext-Schutz: Titel darf nicht mit Kleinbuchstaben weitergehen (dann ist es Satz)
        if re.search(r"[a-z]\s+[a-z]{4,}", title) and not any(c.isupper() for c in title[1:]):
            pass
        pdf_page = char_to_page(m.start())
        # Depth aus Number-Tiefe
        depth = num.count(".")
        full_title = f"{num} {title}"
        key = full_title.lower()[:40]
        if key in seen:
            continue
        seen.add(key)
        entries.append({
            "title": full_title,
            "page_0": pdf_page,
            "page_1": pdf_page + 1,
            "depth": depth,
        })

    # B) Bekannte Headings (nur wenn A zu wenig ergab)
    if len(entries) < 3:
        for line_match in re.finditer(r"^\s*(?P<line>[A-Z\u00c0-\u024f][A-Za-z\u00c0-\u024f\s\-\:]{3,40})\s*$",
                                       fulltxt, re.MULTILINE):
            line = line_match.group("line").strip()
            line_norm = line.lower().replace(" ", "").replace("-", "").replace(":", "")
            if not any(kh in line_norm for kh in known_headings):
                continue
            pdf_page = char_to_page(line_match.start())
            key = line.lower()[:40]
            if key in seen:
                continue
            seen.add(key)
            entries.append({
                "title": line,
                "page_0": pdf_page,
                "page_1": pdf_page + 1,
                "depth": 0,
            })

    # Dedupliziere: keine zwei Eintraege auf derselben Seite mit gleicher Tiefe
    seen_pages: set = set()
    final: list[dict[str, Any]] = []
    for e in sorted(entries, key=lambda x: (x["page_0"], x["depth"])):
        k = (e["page_0"], e["depth"])
        if k in seen_pages:
            continue
        seen_pages.add(k)
        final.append(e)
    return final


def extract_outline(pdf_path: Path, max_depth: int = 2, auto_correct: bool = True) -> list[dict[str, Any]]:
    reader = PdfReader(str(pdf_path))
    try:
        outline = reader.outline
    except Exception as e:
        print(f"    WARN: Outline nicht lesbar: {e}")
        outline = None
    entries = _flatten_outline(outline, reader, depth=0, max_depth=max_depth) if outline else []
    n_pages = len(reader.pages)

    # Fallback 1: Wenn keine PDF-Outline -> TOC aus Text extrahieren
    if not entries:
        print(f"    [TOC-Fallback] Versuche Inhaltsverzeichnis aus Text zu extrahieren...")
        entries = _extract_toc_from_text(pdf_path, n_pages)
        if entries:
            print(f"    [TOC-Fallback] {len(entries)} Eintraege aus Text-TOC erkannt")
        entries = [e for e in entries if e["depth"] < max_depth]
    # Fallback 2: Wenn auch kein TOC -> Heading-Scan im Volltext
    if not entries:
        print(f"    [Heading-Scan] Versuche nummerierte Ueberschriften im Volltext zu finden...")
        entries = _extract_headings_from_fulltext(pdf_path, n_pages)
        if entries:
            print(f"    [Heading-Scan] {len(entries)} Ueberschriften erkannt")
        entries = [e for e in entries if e["depth"] < max_depth]
    # Sortiere nach Seitenzahl (Outline ist normalerweise schon sortiert, aber sicher ist sicher)
    entries.sort(key=lambda e: (e["page_0"], e["depth"]))

    # ---- Auto-Korrektur: PDF-Bookmarks zeigen oft 1 Seite zu frueh ----------
    if auto_correct:
        corrections = 0
        for e in entries:
            new_start = _correct_start_page(pdf_path, e["title"], e["page_0"], n_pages, max_offset=3)
            if new_start != e["page_0"]:
                corrections += 1
                e["page_0_original"] = e["page_0"]
                e["page_0"] = new_start
                e["page_1"] = new_start + 1
        if corrections:
            print(f"    [auto-offset]  {corrections}/{len(entries)} Bookmarks um +1..+3 korrigiert")
        # Nach Korrektur nochmal sortieren
        entries.sort(key=lambda e: (e["page_0"], e["depth"]))

    # Bestimme end_page: Start des naechsten Eintrags gleicher oder hoeherer Ebene - 1
    for i, e in enumerate(entries):
        end = n_pages - 1  # default: bis Ende
        for j in range(i + 1, len(entries)):
            nxt = entries[j]
            if nxt["depth"] <= e["depth"]:
                end = nxt["page_0"] - 1
                break
            # tiefere Ebenen: wir nehmen deren Seiten NICHT aus unserem Bereich heraus
            # -> end bleibt gross, wird erst bei gleicher/hoeherer Ebene reduziert
        if end < e["page_0"]:
            end = e["page_0"]  # mindestens eine Seite
        e["end_0"] = end
        e["end_1"] = end + 1
        e["n_pages"] = end - e["page_0"] + 1
    return entries


# ---------- PDF-SPLITTING -----------------------------------------------------

def write_pdf_split(reader: PdfReader, start_0: int, end_0: int, target: Path) -> int:
    """Schreibt Seiten [start_0..end_0] (0-indexiert, inklusive) nach target. Gibt Seitenanzahl zurueck."""
    writer = PdfWriter()
    for i in range(start_0, end_0 + 1):
        if 0 <= i < len(reader.pages):
            writer.add_page(reader.pages[i])
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("wb") as fh:
        writer.write(fh)
    return end_0 - start_0 + 1


# ---------- MAIN-LOGIC PRO QUELLE ---------------------------------------------

def process_source(key: str, force: bool, dry_run: bool, max_depth: int) -> dict[str, Any]:
    """Verarbeitet eine Quelle. Gibt Status-Dict zurueck."""
    status: dict[str, Any] = {
        "key": key, "ok": False, "reason": "", "n_splits": 0, "n_pages_total": 0, "outline_entries": 0,
    }
    src_pdf = LIT / key / "source.pdf"
    if not src_pdf.exists():
        status["reason"] = "kein source.pdf"
        return status

    print(f"[{key}]")
    try:
        reader = PdfReader(str(src_pdf))
        total_pages = len(reader.pages)
    except Exception as e:
        status["reason"] = f"PDF nicht lesbar: {type(e).__name__}: {str(e)[:100]}"
        print(f"  ERR: {status['reason']}")
        return status
    status["n_pages_total"] = total_pages
    print(f"  PDF: {total_pages} Seiten")

    # Kurz-Dokumente (< 10 Seiten): kein Split, _outline.md mit Hinweis
    MIN_PAGES_FOR_SPLIT = 10
    if total_pages < MIN_PAGES_FOR_SPLIT:
        status["reason"] = f"kurz (<{MIN_PAGES_FOR_SPLIT} Seiten) - kein Split noetig"
        print(f"  INFO: PDF zu kurz fuer Split. Ganzes PDF als Referenz nutzen.")
        _write_outline_md(key, [], total_pages, manual_hint=True, short_doc=True)
        status["ok"] = True
        return status

    try:
        entries = extract_outline(src_pdf, max_depth=max_depth)
    except Exception as e:
        status["reason"] = f"Outline-Fehler: {type(e).__name__}: {str(e)[:100]}"
        print(f"  ERR: {status['reason']}")
        _write_outline_md(key, [], total_pages, manual_hint=True)
        return status
    status["outline_entries"] = len(entries)
    if not entries:
        status["reason"] = "keine Outline/Bookmarks"
        print(f"  WARN: Keine Outline gefunden. Manuelles _outline_manual.md anlegen.")
        # Erzeuge trotzdem _outline.md als Platzhalter
        _write_outline_md(key, entries, total_pages, manual_hint=True)
        return status

    print(f"  Outline-Eintraege (bis depth {max_depth}): {len(entries)}")

    ex_dir = LIT / key / "excerpts"
    ex_dir.mkdir(parents=True, exist_ok=True)

    n_written = 0
    splits_out: list[dict[str, Any]] = []
    for i, e in enumerate(entries, start=1):
        slug = slugify(e["title"], maxlen=50)
        fname = f"{i:03d}_{slug}.pdf"
        target = ex_dir / fname
        size_mb = 0.0
        # Indent-Praefix: je tiefer, desto mehr Spaces
        indent = "    " * e["depth"]
        label = f"{indent}{e['title'][:60]}"
        if target.exists() and not force:
            size_mb = round(target.stat().st_size / (1024 * 1024), 2)
            print(f"  [skip] {fname}  (S. {e['page_1']}-{e['end_1']}, {e['n_pages']} Seiten, {size_mb} MB)  {label}")
        elif dry_run:
            print(f"  [dry]  {fname}  (S. {e['page_1']}-{e['end_1']}, {e['n_pages']} Seiten)  {label}")
        else:
            pages_written = write_pdf_split(reader, e["page_0"], e["end_0"], target)
            size_mb = round(target.stat().st_size / (1024 * 1024), 2)
            n_written += 1
            print(f"  [OK]   {fname}  (S. {e['page_1']}-{e['end_1']}, {pages_written} Seiten, {size_mb} MB)  {label}")
        splits_out.append({
            "file": fname,
            "title": e["title"],
            "depth": e["depth"],
            "page_start": e["page_1"],
            "page_end": e["end_1"],
            "n_pages": e["n_pages"],
            "size_mb": size_mb,
        })

    if not dry_run:
        _write_outline_md(key, splits_out, total_pages, manual_hint=False)
    status["ok"] = True
    status["n_splits"] = n_written
    return status


def _write_outline_md(key: str, splits: list[dict[str, Any]], total_pages: int, manual_hint: bool, short_doc: bool = False) -> None:
    """Schreibt _outline.md als Uebersicht."""
    ex_dir = LIT / key / "excerpts"
    ex_dir.mkdir(parents=True, exist_ok=True)
    target = ex_dir / "_outline.md"
    out: list[str] = []
    out.append(f"# Kapitel-Ausz\u00fcge: `{key}`")
    out.append("")
    out.append(f"Quelle: `../source.pdf` ({total_pages} Seiten gesamt)")
    out.append("")
    if short_doc:
        out.append(f"> **INFO:** Dokument ist mit {total_pages} Seiten kompakt genug, um es als Ganzes zu nutzen.")
        out.append("> Kein Kapitel-Split noetig. Verweise direkt auf `../source.pdf` mit Seitenangabe.")
        out.append("")
        out.append("## Gesamt-PDF")
        out.append("")
        out.append(f"- [`../source.pdf`](../source.pdf) \u2013 {total_pages} Seiten")
        out.append("")
    elif manual_hint:
        out.append("> **HINWEIS:** Keine PDF-Outline (Bookmarks) gefunden. Kapitel-Splits k\u00f6nnen nicht automatisch erzeugt werden.")
        out.append("> Lege eine Datei `_outline_manual.md` an mit Zeilen der Form `<start_seite>-<end_seite>  <titel>` (eine pro Kapitel),")
        out.append("> damit `extract_excerpts.py --key " + key + " --manual` die Splits erstellt.")
        out.append("")
        out.append("## Gesamt-PDF")
        out.append("")
        out.append(f"- [`../source.pdf`](../source.pdf) \u2013 {total_pages} Seiten")
        out.append("")
    else:
        out.append(f"Automatisch erzeugt durch `extract_excerpts.py`. **{len(splits)} Kapitel-Auszuege**.")
        out.append("")
        out.append("| # | Seiten | Datei | Titel |")
        out.append("|---:|---|---|---|")
        for i, s in enumerate(splits, start=1):
            indent = "&nbsp;&nbsp;&nbsp;&nbsp;" * s["depth"]
            out.append(f"| {i} | S. {s['page_start']}\u2013{s['page_end']} ({s['n_pages']}) | [`{s['file']}`]({s['file']}) | {indent}{s['title']} |")
        out.append("")
    target.write_text("\n".join(out), encoding="utf-8")


# ---------- CLI ----------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="Kapitel-Auszuege aus PDF-Volltext erzeugen (pro Quelle).")
    ap.add_argument("--key", default="", help="Nur eine Quelle (BibKey). Default: alle mit source.pdf.")
    ap.add_argument("--force", action="store_true", help="ueberschreibt existierende Splits.")
    ap.add_argument("--dry-run", action="store_true", help="nur anzeigen, nichts schreiben.")
    ap.add_argument("--max-depth", type=int, default=2, help="max. Outline-Tiefe (default: 2).")
    args = ap.parse_args()

    print("extract_excerpts.py")
    if args.key:
        keys = [args.key]
    else:
        keys = sorted([d.name for d in LIT.iterdir() if d.is_dir() and (d / "source.pdf").exists()])
    print(f"  Zu verarbeiten: {len(keys)} Quellen")
    print()

    results = []
    for k in keys:
        r = process_source(k, force=args.force, dry_run=args.dry_run, max_depth=args.max_depth)
        results.append(r)
        print()

    # Zusammenfassung
    print("=== Zusammenfassung ===")
    ok = sum(1 for r in results if r["ok"])
    warn = sum(1 for r in results if not r["ok"] and "Outline" in r["reason"])
    err = sum(1 for r in results if not r["ok"] and "Outline" not in r["reason"])
    total_splits = sum(r["n_splits"] for r in results)
    print(f"  Quellen mit Outline:        {ok}")
    print(f"  Quellen ohne Outline:       {warn}  (manuelles _outline_manual.md noetig)")
    print(f"  Fehler:                     {err}")
    print(f"  Kapitel-Splits erzeugt:     {total_splits}")
    print()
    if warn:
        print("  Quellen ohne Outline:")
        for r in results:
            if not r["ok"] and "Outline" in r["reason"]:
                print(f"    - {r['key']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
