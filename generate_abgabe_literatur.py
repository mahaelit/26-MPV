#!/usr/bin/env python3
"""
generate_abgabe_literatur.py
============================
Liest die Single Source of Truth (abgabe_korpus.tex) und die BibTeX-Datei
(Quellen.bib), erzeugt daraus die Kern- und Stuetzliteratur-Bloecke fuer
mpv_abgabedokument.tex.

Prinzip:
  - abgabe_korpus.tex wird Zeile fuer Zeile geparst
  - Jede AbgabeQuelle{Frage}{Status}{Key}{Seitenbereich}{Seitenzahl}
    wird extrahiert
  - Aus Quellen.bib werden die Metadaten (Autor, Titel, Booktitle, Jahr,
    Verlag, Ort, Seiten, Journal, etc.) gelesen
  - Daraus werden APA-7-aehnliche cite-Eintraege fuer die description-
    Umgebungen im Abgabedokument generiert
  - Duplikate innerhalb einer Frage werden eliminiert (erster Eintrag zaehlt)
  - Die Ausgabe ist direkt als LaTeX-Fragment verwendbar

Aufruf:
  python generate_abgabe_literatur.py

Ausgabe:
  mpv_abgabe_literatur_generated.tex  (LaTeX-Fragment)
  + Konsolenausgabe mit Statistik
"""

import re
import sys
from pathlib import Path
from collections import OrderedDict

# ── Pfade ──────────────────────────────────────────────────────────────
BASE = Path(__file__).parent
KORPUS = BASE / "abgabe_korpus.tex"
BIB    = BASE / "Quellen.bib"
OUTPUT = BASE / "mpv_abgabe_literatur_generated.tex"


# ══════════════════════════════════════════════════════════════════════
#  1. Parser: abgabe_korpus.tex
# ══════════════════════════════════════════════════════════════════════

def parse_korpus(path: Path) -> list[dict]:
    """Parse alle \\AbgabeQuelle-Eintraege aus der Korpusdatei."""
    pattern = re.compile(
        r"\\AbgabeQuelle\{(\w+)\}\{(\w)\}\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}"
    )
    entries = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = pattern.search(line)
            if m:
                entries.append({
                    "frage":  m.group(1),        # F1..F5
                    "status": m.group(2),         # K, S, N
                    "key":    m.group(3),         # BibTeX-Key
                    "seiten": m.group(4),         # Seitenbereich
                    "anzahl": int(m.group(5)),    # Seitenzahl
                })
    return entries


# ══════════════════════════════════════════════════════════════════════
#  2. Parser: Quellen.bib (minimaler BibTeX-Parser)
# ══════════════════════════════════════════════════════════════════════

def clean_latex(s: str) -> str:
    """Entferne LaTeX-Kommandos fuer die Anzeige im generierten LaTeX."""
    # Wir behalten das LaTeX weitgehend, da es in LaTeX-Output eingebettet wird
    # Nur geschweifte Klammern um Woerter entfernen (BibTeX title casing)
    s = re.sub(r"\{([^{}]*)\}", r"\1", s)
    s = s.replace("\\&", "&")
    return s.strip()


def parse_bib(path: Path) -> dict:
    """Parse BibTeX-Datei und gib dict[key] -> {type, fields} zurueck."""
    with open(path, encoding="utf-8") as f:
        content = f.read()

    entries = {}
    # Finde alle @type{key, ...} Bloecke
    # Robust: Finde den Start jedes Eintrags
    entry_starts = list(re.finditer(
        r"@(\w+)\s*\{([^,\s]+)\s*,", content
    ))

    for i, match in enumerate(entry_starts):
        entry_type = match.group(1).lower()
        key = match.group(2).strip()
        # Block bis zum naechsten Eintrag oder Dateiende
        start = match.end()
        if i + 1 < len(entry_starts):
            end = entry_starts[i + 1].start()
        else:
            end = len(content)
        block = content[start:end]

        # Felder extrahieren
        fields = {}
        # Einfacher Feld-Parser: feldname = {wert} oder feldname = wert
        field_pattern = re.compile(
            r"(\w+)\s*=\s*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}",
            re.DOTALL
        )
        for fm in field_pattern.finditer(block):
            fname = fm.group(1).lower().strip()
            fval = fm.group(2).strip()
            # Mehrzeilige Werte zusammenfuehren
            fval = re.sub(r"\s+", " ", fval)
            fields[fname] = fval

        entries[key] = {"type": entry_type, "fields": fields}

    return entries


# ══════════════════════════════════════════════════════════════════════
#  3. APA-7-aehnliche Kurzreferenz generieren
# ══════════════════════════════════════════════════════════════════════

def make_short_title(bib_entry: dict) -> str:
    """Erzeuge eine Kurzform des Titels fuer die Beschreibung."""
    fields = bib_entry.get("fields", {})
    title = fields.get("title", "")
    # Entferne {}-Klammerung
    title = re.sub(r"\{([^{}]*)\}", r"\1", title)
    # Kuerze bei Doppelpunkt
    if ":" in title:
        title = title.split(":")[0].strip()
    # Entferne TeX-Sonderzeichen
    title = title.replace("\\enquote", "").replace("\\textit", "")
    title = title.replace("\\\"a", "ä").replace("\\\"o", "ö").replace("\\\"u", "ü")
    title = title.replace("\\\"A", "Ä").replace("\\\"O", "Ö").replace("\\\"U", "Ü")
    return title


def make_booktitle_ref(bib_entry: dict) -> str:
    """Erzeuge In: Editor, Buchtitel. falls vorhanden."""
    fields = bib_entry.get("fields", {})
    bt = fields.get("booktitle", "")
    editor = fields.get("editor", "")
    if not bt:
        return ""
    # Bereinige Buchtitel
    bt = re.sub(r"\{([^{}]*)\}", r"\1", bt)
    # Kuerze bei : fuer Lesbarkeit
    if len(bt) > 80 and ":" in bt:
        bt = bt.split(":")[0].strip()
    return bt


def make_journal_ref(bib_entry: dict) -> str:
    """Erzeuge Zeitschriftenreferenz falls vorhanden."""
    fields = bib_entry.get("fields", {})
    journal = fields.get("journal", "") or fields.get("journaltitle", "")
    if not journal:
        return ""
    journal = re.sub(r"\{([^{}]*)\}", r"\1", journal)
    return journal


def format_entry_latex(entry: dict, bib_data: dict, is_kern: bool) -> str:
    """
    Erzeugt einen \\item[\\cite{key}] Block fuer das Abgabedokument.

    Fuer Kernliteratur: mit Seitenzahl in Klammern
    Fuer Stuetzliteratur: nur Seitenbereich, keine Seitenzahl
    """
    key = entry["key"]
    seiten = entry["seiten"]
    anzahl = entry["anzahl"]

    bib = bib_data.get(key, None)
    if bib is None:
        # Fallback: nur key und Seiten
        if is_kern:
            return f"  \\item[\\cite{{{key}}}] [BibTeX-Eintrag nicht gefunden]. S.\\,{seiten} ({anzahl}\\,S.)"
        else:
            return f"  \\item[\\cite{{{key}}}] [BibTeX-Eintrag nicht gefunden]. S.\\,{seiten}."

    fields = bib.get("fields", {})
    btype = bib.get("type", "")

    # Titel
    title = make_short_title(bib)

    # Kontextinfo (Booktitle/Journal)
    booktitle = make_booktitle_ref(bib)
    journal = make_journal_ref(bib)

    # Baue Beschreibung
    desc_parts = []
    desc_parts.append(title)

    if booktitle and btype in ("incollection",):
        # Entferne {}-Klammerung
        bt_clean = re.sub(r"\{([^{}]*)\}", r"\1", booktitle)
        desc_parts.append(f"\n    In: \\textit{{{bt_clean}}}")
    elif journal:
        j_clean = re.sub(r"\{([^{}]*)\}", r"\1", journal)
        desc_parts.append(f"\n    \\textit{{{j_clean}}}")

    desc = ".\n    ".join(p for p in desc_parts if p)

    # Seitenangabe
    if is_kern:
        if seiten == "online":
            seitentext = "Online"
        else:
            seitentext = f"S.\\,{seiten} ({anzahl}\\,S.)"
        return f"  \\item[\\cite{{{key}}}] {desc}.\n    {seitentext}"
    else:
        if seiten == "online":
            seitentext = "Online."
        else:
            seitentext = f"S.\\,{seiten}."
        return f"  \\item[\\cite{{{key}}}] {desc}.\n    {seitentext}"


# ══════════════════════════════════════════════════════════════════════
#  4. Hauptlogik: Generiere LaTeX-Fragment
# ══════════════════════════════════════════════════════════════════════

FRAGE_TITEL = {
    "F1": "Frage 1",
    "F2": "Frage 2",
    "F3": "Frage 3",
    "F4": "Frage 4",
    "F5": "Frage 5",
}


def generate_literatur_blocks(korpus_entries: list[dict], bib_data: dict) -> str:
    """Erzeugt den vollstaendigen LaTeX-Inhalt fuer alle 5 Fragen."""
    output_lines = []

    output_lines.append("% " + "=" * 60)
    output_lines.append("% AUTOMATISCH GENERIERT aus abgabe_korpus.tex + Quellen.bib")
    output_lines.append("% Skript: generate_abgabe_literatur.py")
    output_lines.append("% Golden Source: abgabe_korpus.tex")
    output_lines.append("% Keine manuellen Aenderungen! Bei Korrekturen:")
    output_lines.append("%   1. abgabe_korpus.tex anpassen")
    output_lines.append("%   2. python generate_abgabe_literatur.py ausfuehren")
    output_lines.append("% " + "=" * 60)
    output_lines.append("")

    for frage in ["F1", "F2", "F3", "F4", "F5"]:
        frage_entries = [e for e in korpus_entries if e["frage"] == frage]
        if not frage_entries:
            continue

        # Kern (K) und Stuetz (S) – beide gezaehlt
        kern = []
        seen_kern = set()
        for e in frage_entries:
            if e["status"] == "K" and e["key"] not in seen_kern:
                kern.append(e)
                seen_kern.add(e["key"])

        # N = nicht gezaehlt / Hinweis
        stuetz = []
        seen_stuetz = set()
        for e in frage_entries:
            if e["status"] == "N" and e["key"] not in seen_stuetz:
                stuetz.append(e)
                seen_stuetz.add(e["key"])

        # S-Status (gezaehlte Stuetzliteratur) – falls vorhanden, zu Kern
        for e in frage_entries:
            if e["status"] == "S" and e["key"] not in seen_kern:
                kern.append(e)
                seen_kern.add(e["key"])

        # Seitensumme berechnen
        total_kern = sum(e["anzahl"] for e in kern)

        frage_label = FRAGE_TITEL[frage]

        output_lines.append(f"\\subsection{{Kernliteratur zu {frage_label}}}")
        output_lines.append("")
        output_lines.append("\\textbf{Gezählte Kernliteratur}")
        output_lines.append("")
        output_lines.append("\\begin{description}")

        for e in kern:
            latex_item = format_entry_latex(e, bib_data, is_kern=True)
            output_lines.append(latex_item)
            output_lines.append("")

        output_lines.append("\\end{description}")
        output_lines.append("")

        if stuetz:
            output_lines.append("\\textbf{Stützliteratur (nicht gezählt)}")
            output_lines.append("")
            output_lines.append("\\begin{description}")

            for e in stuetz:
                latex_item = format_entry_latex(e, bib_data, is_kern=False)
                output_lines.append(latex_item)
                output_lines.append("")

            output_lines.append("\\end{description}")
            output_lines.append("")

        output_lines.append(
            f"\\textit{{Umfang {frage_label}: {total_kern}\\,Seiten "
            f"gezählte Kernliteratur; Stützliteratur nicht eingerechnet.}}"
        )
        output_lines.append("")
        output_lines.append("")

    return "\n".join(output_lines)


# ══════════════════════════════════════════════════════════════════════
#  5. Konsistenzcheck: Alle BibTeX-Keys aus Korpus muessen in .bib sein
# ══════════════════════════════════════════════════════════════════════

def check_consistency(korpus_entries: list[dict], bib_data: dict):
    """Pruefe ob alle Keys aus dem Korpus in der .bib existieren."""
    missing = []
    all_keys = set()
    for e in korpus_entries:
        all_keys.add(e["key"])
    for key in sorted(all_keys):
        if key not in bib_data:
            missing.append(key)
    if missing:
        print(f"\n!!  WARNUNG: {len(missing)} BibTeX-Key(s) nicht in Quellen.bib gefunden:")
        for k in missing:
            print(f"   - {k}")
    else:
        print(f"\n[OK]  Alle {len(all_keys)} BibTeX-Keys aus abgabe_korpus.tex in Quellen.bib vorhanden.")
    return missing


def print_stats(korpus_entries: list[dict]):
    """Statistik ausgeben."""
    print("\n" + "=" * 60)
    print("QUELLENKORPUS-STATISTIK (aus abgabe_korpus.tex)")
    print("=" * 60)

    for frage in ["F1", "F2", "F3", "F4", "F5"]:
        frage_entries = [e for e in korpus_entries if e["frage"] == frage]
        kern = [e for e in frage_entries if e["status"] in ("K", "S")]
        stuetz = [e for e in frage_entries if e["status"] == "N"]
        total_s = sum(e["anzahl"] for e in kern)
        print(f"  {frage}: {len(kern):2d} Kern/Stuetz, {len(stuetz):2d} N-Quellen, "
              f"Sum = {total_s:3d} Seiten")

    # Globale Deduplizierung
    unique_kern = {}
    for e in korpus_entries:
        if e["status"] in ("K", "S"):
            if e["key"] not in unique_kern:
                unique_kern[e["key"]] = e["anzahl"]
    global_total = sum(unique_kern.values())
    print(f"\n  Globale Summe (dedupliziert): {global_total} Seiten")
    print(f"  Unique Kern/Stuetz-Keys: {len(unique_kern)}")
    print("=" * 60)


# ══════════════════════════════════════════════════════════════════════
#  6. Main
# ══════════════════════════════════════════════════════════════════════

def main():
    print(f"Lese Korpus: {KORPUS}")
    korpus = parse_korpus(KORPUS)
    print(f"  -> {len(korpus)} Eintraege gefunden")

    print(f"Lese BibTeX: {BIB}")
    bib = parse_bib(BIB)
    print(f"  -> {len(bib)} Eintraege gefunden")

    check_consistency(korpus, bib)
    print_stats(korpus)

    latex = generate_literatur_blocks(korpus, bib)

    OUTPUT.write_text(latex, encoding="utf-8")
    print(f"\n[OK]  LaTeX-Fragment geschrieben: {OUTPUT}")
    print(f"   ({len(latex)} Zeichen, {latex.count(chr(10))} Zeilen)")

    # Auch Inhalt ausgeben
    print("\n" + "-" * 60)
    print("GENERIERTER LATEX-INHALT:")
    print("-" * 60)
    print(latex)


if __name__ == "__main__":
    main()
