#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
bib2csv.py  --  Erstellt aus einer BibLaTeX-Datei (z. B. Quellen.bib)
                eine Excel-taugliche CSV- sowie eine XLSX-Datei
                mit einer Zeile pro Literaturquelle.

Aufruf:
    python bib2csv.py [input.bib] [output_basename]

Standardwerte (ohne Argumente):
    input           = Quellen.bib                (neben diesem Skript)
    output_basename = Quellen                    (erzeugt Quellen.csv + Quellen.xlsx)

Besonderheiten
--------------
- Verarbeitet @type{key, feld = {wert}, ...}-Syntax mit
  geschachtelten Klammern und mehrzeiligen Werten.
- Entfernt LaTeX-Markup ({...}, \textit{...}, \,, ~, --, ...)
  fuer eine lesbare Tabelle.
- Erkennt Abschnittsueberschriften der Form
      %  -- Frage 1: Erkennen --
  (Trennzeichen: ASCII '-' oder die Unicode-Box-Zeichen '─' / '═')
  und schreibt den Titel in die Spalte "Kategorie".
- CSV:  UTF-8 mit BOM, Semikolon als Trenner, zusaetzlich Excel-Hinweis
        "sep=;" in Zeile 1, damit die Datei in jeder Excel-Locale mit
        korrekter Spaltentrennung oeffnet.
- XLSX: natives Excel-Format mit fixierter Kopfzeile, fetter Ueberschrift,
        passenden Spaltenbreiten, Textumbruch und klickbaren URL/DOI-Links.
        (Benoetigt das Paket `openpyxl`; faellt bei dessen Fehlen still
        auf CSV-only zurueck.)
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path


# ------------------------------- LaTeX -> Text -------------------------------

_REPLACEMENTS = [
    (re.compile(r"\\textit\{([^{}]*)\}"), r"\1"),
    (re.compile(r"\\emph\{([^{}]*)\}"),   r"\1"),
    (re.compile(r"\\guillemotleft\b"),  "\u00ab"),        # «
    (re.compile(r"\\guillemotright\b"), "\u00bb"),        # »
    (re.compile(r"\\&"), "&"),
    (re.compile(r"\\%"), "%"),
    (re.compile(r"\\,"), " "),
    (re.compile(r"\\ "), " "),
    (re.compile(r"~"),   " "),
    (re.compile(r"--"),  "\u2013"),                      # en-dash
]


def sanitize(value: str) -> str:
    """Entfernt BibTeX-/LaTeX-Steuerzeichen fuer reinen Text in der CSV."""
    if not value:
        return ""
    v = value
    for pat, rep in _REPLACEMENTS:
        v = pat.sub(rep, v)
    # Schutzklammern {...} zweimal entfernen (fuer geschachtelte Paare).
    v = re.sub(r"\{([^{}]*)\}", r"\1", v)
    v = re.sub(r"\{([^{}]*)\}", r"\1", v)
    # Whitespace normalisieren.
    v = re.sub(r"\s+", " ", v).strip()
    return v


def format_names(raw: str) -> str:
    """
    'Last, First and Last2, First2' -> 'Last, First; Last2, First2'.
    Behandelt Umbrueche innerhalb langer Autorlisten korrekt.
    """
    if not raw:
        return ""
    v = re.sub(r"\s+", " ", raw).strip()
    names = [n.strip() for n in v.split(" and ")]
    return "; ".join(sanitize(n) for n in names if n)


# ------------------------------- Bib-Parser ----------------------------------

ENTRY_RE = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", re.MULTILINE)

# Abschnittsueberschriften der Form
#     %  --- Titel ---            (ASCII)
#     %  ─── Titel ───            (Unicode Box Drawings)
#     %  ═══ Titel ═══            (Unicode Double Line)
# [ \t] statt \s verhindert, dass die Suche ueber mehrere Zeilen
# hinweg (Leerzeile zwischen Kopf und Titel) zusammenlaeuft.
# Der Titel muss mindestens ein "echtes" Zeichen (kein Trenner,
# kein Whitespace, kein '%') enthalten.
SECTION_RE = re.compile(
    r"^[ \t]*%[ \t]*[\u2500\u2550\-]{2,}[ \t]*"
    r"([^\s%\u2500\u2550\-][^\n]*?)"
    r"[ \t]*[\u2500\u2550\-]{2,}[ \t]*$",
    re.MULTILINE,
)


def find_entry_end(text: str, open_brace: int) -> int:
    """Index der passenden schliessenden `}` zum `{` an *open_brace*."""
    depth = 0
    i = open_brace
    n = len(text)
    while i < n:
        ch = text[i]
        # Kommentar nur AUSSERHALB von Feld-Werten (d. h. direkt innerhalb
        # der Entry-Klammer, depth == 1) als Zeilenkommentar interpretieren.
        if ch == "%" and depth == 1:
            j = text.find("\n", i)
            i = n if j == -1 else j + 1
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def strip_comments(text: str) -> str:
    """Entfernt `% ...`-Zeilenkommentare (fuer den Entry-Rumpf)."""
    out = []
    for line in text.splitlines():
        i = 0
        while i < len(line):
            if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
                break
            i += 1
        out.append(line[:i])
    return "\n".join(out)


def parse_fields(body: str) -> dict:
    """Zerlegt den Rumpf eines @entry{...} in ein Feld-Dictionary."""
    fields: dict = {}
    i, n = 0, len(body)
    while i < n:
        while i < n and body[i] in " \t\n\r,":
            i += 1
        if i >= n:
            break
        m = re.match(r"([A-Za-z_]+)\s*=\s*", body[i:])
        if not m:
            break
        name = m.group(1).lower()
        i += m.end()
        if i >= n:
            break
        if body[i] == "{":
            depth = 1
            i += 1
            start = i
            while i < n and depth > 0:
                if body[i] == "{":
                    depth += 1
                elif body[i] == "}":
                    depth -= 1
                    if depth == 0:
                        break
                i += 1
            value = body[start:i]
            i += 1
        elif body[i] == '"':
            i += 1
            start = i
            while i < n and body[i] != '"':
                i += 1
            value = body[start:i]
            i += 1
        else:
            start = i
            while i < n and body[i] not in ",\n":
                i += 1
            value = body[start:i].strip()
        fields[name] = value
    return fields


def parse_bib(text: str) -> list:
    # Abschnittskoepfe mit ihren Positionen im Originaltext sammeln.
    sections = sorted(
        (m.start(), m.group(1).strip()) for m in SECTION_RE.finditer(text)
    )

    def section_for(pos: int) -> str:
        current = ""
        for sp, name in sections:
            if sp <= pos:
                current = name
            else:
                break
        return current

    entries = []
    for m in ENTRY_RE.finditer(text):
        entry_type = m.group(1).lower()
        key        = m.group(2)
        open_brace = text.find("{", m.start())
        end        = find_entry_end(text, open_brace)
        if end == -1:
            continue
        body   = strip_comments(text[m.end():end])
        fields = parse_fields(body)
        fields["entry_type"] = entry_type
        fields["key"]        = key
        fields["section"]    = section_for(m.start())
        entries.append(fields)
    return entries


# ------------------------------- CSV-Export ----------------------------------

CSV_COLUMNS = [
    "Kategorie",
    "BibKey",
    "Eintragstyp",
    "AutorIn",
    "HerausgeberIn",
    "Jahr",
    "Titel",
    "Buchtitel / Journal",
    "Auflage",
    "Band",
    "Heft",
    "Seiten",
    "Verlag",
    "Ort",
    "Institution",
    "Schriftenart",
    "Reihe",
    "DOI",
    "URL",
    "Zugriffsdatum",
    "Anmerkung",
    "Umfangshinweis",
]


def entry_to_row(e: dict) -> dict:
    return {
        "Kategorie":            sanitize(e.get("section", "")),
        "BibKey":               e.get("key", ""),
        "Eintragstyp":          e.get("entry_type", ""),
        "AutorIn":              format_names(e.get("author", "")),
        "HerausgeberIn":        format_names(e.get("editor", "")),
        "Jahr":                 sanitize(e.get("year", "")),
        "Titel":                sanitize(e.get("title", "")),
        "Buchtitel / Journal":  sanitize(e.get("booktitle", "") or e.get("journal", "")),
        "Auflage":              sanitize(e.get("edition", "")),
        "Band":                 sanitize(e.get("volume", "")),
        "Heft":                 sanitize(e.get("number", "")),
        "Seiten":               sanitize(e.get("pages", "")),
        "Verlag":               sanitize(e.get("publisher", "")),
        "Ort":                  sanitize(e.get("address", "")),
        "Institution":          sanitize(e.get("institution", "")),
        "Schriftenart":         sanitize(e.get("type", "")),
        "Reihe":                sanitize(e.get("series", "")),
        "DOI":                  sanitize(e.get("doi", "")),
        "URL":                  sanitize(e.get("url", "")),
        "Zugriffsdatum":        sanitize(e.get("urldate", "")),
        "Anmerkung":            sanitize(e.get("note", "")),
        "Umfangshinweis":       sanitize(e.get("annotation", "")),
    }


# ------------------------------- Ausgabeformate ------------------------------

def write_csv(rows: list, csv_path: Path) -> None:
    """Excel-tauglich: UTF-8 mit BOM, ';' als Trenner, 'sep=;'-Praeambel."""
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        # Excel-Hinweis: forciert ';' als Spaltentrenner, unabhaengig von
        # der System-Locale (auch in EN/US-Excel funktioniert die Datei).
        f.write("sep=;\n")
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def write_xlsx(rows: list, xlsx_path: Path) -> bool:
    """Echte .xlsx-Datei schreiben. Gibt False zurueck, falls openpyxl fehlt."""
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Alignment, Font, PatternFill
        from openpyxl.utils import get_column_letter
    except ImportError:
        print("[Info] openpyxl nicht installiert  ->  nur CSV erzeugt.",
              file=sys.stderr)
        print("       Installieren mit:  pip install openpyxl", file=sys.stderr)
        return False

    wb = Workbook()
    ws = wb.active
    ws.title = "Quellen"

    # Kopfzeile.
    ws.append(CSV_COLUMNS)
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill("solid", fgColor="305496")
    header_align = Alignment(horizontal="left", vertical="center", wrap_text=True)
    for col_idx, _ in enumerate(CSV_COLUMNS, start=1):
        cell = ws.cell(row=1, column=col_idx)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_align

    # Datenzeilen inkl. Hyperlinks fuer URL- und DOI-Spalten.
    url_col = CSV_COLUMNS.index("URL") + 1
    doi_col = CSV_COLUMNS.index("DOI") + 1
    link_font = Font(color="0563C1", underline="single")

    for r_idx, row in enumerate(rows, start=2):
        for c_idx, col_name in enumerate(CSV_COLUMNS, start=1):
            value = row.get(col_name, "") or ""
            cell = ws.cell(row=r_idx, column=c_idx, value=value)
            cell.alignment = Alignment(vertical="top", wrap_text=True)

        # URL als Hyperlink.
        url_val = row.get("URL", "")
        if url_val:
            cell = ws.cell(row=r_idx, column=url_col)
            cell.hyperlink = url_val
            cell.font = link_font

        # DOI als Hyperlink (doi.org).
        doi_val = row.get("DOI", "")
        if doi_val:
            cell = ws.cell(row=r_idx, column=doi_col)
            cell.hyperlink = f"https://doi.org/{doi_val}"
            cell.font = link_font

    # Kopfzeile fixieren + Autofilter.
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions

    # Spaltenbreiten abhaengig von Inhalt (gedeckelt).
    max_widths = {
        "Kategorie":            28,
        "BibKey":               28,
        "Eintragstyp":          14,
        "AutorIn":              40,
        "HerausgeberIn":        40,
        "Jahr":                 6,
        "Titel":                55,
        "Buchtitel / Journal":  45,
        "Auflage":              8,
        "Band":                 6,
        "Heft":                 6,
        "Seiten":               12,
        "Verlag":               30,
        "Ort":                  20,
        "Institution":          30,
        "Schriftenart":         16,
        "Reihe":                20,
        "DOI":                  30,
        "URL":                  45,
        "Zugriffsdatum":        14,
        "Anmerkung":            40,
        "Umfangshinweis":       40,
    }
    for idx, col_name in enumerate(CSV_COLUMNS, start=1):
        # Inhaltsbreite ermitteln.
        content_w = max(
            (len(str(row.get(col_name, "") or "")) for row in rows),
            default=0,
        )
        header_w = len(col_name)
        # Sanfte Heuristik: min. Kopfzeile, max. gedeckelter Wert.
        width = min(max_widths.get(col_name, 30),
                    max(header_w + 2, min(content_w + 2, 60)))
        ws.column_dimensions[get_column_letter(idx)].width = width

    ws.row_dimensions[1].height = 28

    wb.save(xlsx_path)
    return True


# ------------------------------- Haupt-Einstieg ------------------------------

def main(argv) -> int:
    here = Path(__file__).resolve().parent
    bib_path = Path(argv[1]) if len(argv) >= 2 else here / "Quellen.bib"
    if len(argv) >= 3:
        base = Path(argv[2])
        base = base.with_suffix("") if base.suffix.lower() in (".csv", ".xlsx") else base
    else:
        base = here / "Quellen"
    csv_path  = base.with_suffix(".csv")
    xlsx_path = base.with_suffix(".xlsx")

    if not bib_path.is_file():
        print(f"[Fehler] Eingabedatei nicht gefunden: {bib_path}", file=sys.stderr)
        return 1

    text    = bib_path.read_text(encoding="utf-8")
    entries = parse_bib(text)
    rows    = [entry_to_row(e) for e in entries]

    try:
        write_csv(rows, csv_path)
        print(f"[OK] {len(rows):>3} Eintraege  ->  {csv_path}")
    except PermissionError:
        print(f"[Fehler] CSV ist gesperrt (in Excel offen?): {csv_path}",
              file=sys.stderr)
        return 2

    try:
        if write_xlsx(rows, xlsx_path):
            print(f"[OK] {len(rows):>3} Eintraege  ->  {xlsx_path}")
    except PermissionError:
        print(f"[Fehler] XLSX ist gesperrt (in Excel offen?): {xlsx_path}",
              file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
