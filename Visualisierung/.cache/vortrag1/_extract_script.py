#!/usr/bin/env python3
"""Extract page texts from all PDFs cited in Vortrag1.md, in one go.
PDF index ist 0-basiert; "printed" ist die gedruckte Buchseite.
Wir geben sowohl Index 0..N-1 als auch optional via offset eine Hypothese aus.
Strategie: Für PDFs mit deutlichem Versatz (Buchseite hinter PDF-Index) probieren wir
Heuristiken: wenn die erste Seite eine römische Zahl/Titel ist, geben wir die ersten 3
und die als "S. X" gemappten Seiten aus.
Hier: Wir extrahieren einfach den **gesamten Inhalt** der relevanten PDFs (kleiner
Kapitel-PDFs) bzw. nur eine Page-Range bei großen Source-PDFs.
"""
import fitz, os, sys, json, re

BASE = "/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV/26-MPV"

# Liste: (label, pdf_path_relative, mode, spec)
# mode = 'all' → alle Seiten; 'idx' → bestimmte 0-indexed pdf-pages
TASKS = [
    # Kernliteratur Frage 1 (außer Stamm21 → Transkript, Stamm25 → Foto-PDFs ohne OCR)
    ("preckel S.15-47 (Kap1+2)", "Literatur/preckel2013hochbegabung/Preckel_Baudson 2013hochbegabung,kap2.2 S.42-50.pdf", "all", None),
    ("gauckreimann S.239-245", "Literatur/gauckreimann2021psychdiagnostik/Gauckreimann2021päddiagnostik s.239-249.pdf", "all", None),
    # haag in maehler2018: S.153-165 (text/explanation chapter), S.187-188 (Schluss)
    ("haag/maehler S.153-165,187-188", "Literatur/maehler2018diagnostik/source.pdf", "printed", "153-165,187-188"),
    ("kellerkoller25 S.76-78", "Literatur/huser2025lichtblick/kapXX_keller_koller_helle_koepfe_migration_s076-078.pdf", "all", None),
    ("baumschader S.588-598 (Twice)", "Literatur/baumschader2021twice/Baum:schader twice exceptionality 588-600.pdf", "all", None),
    # koop S.64-67 in pauly2025
    ("koop S.64-67 in pauly", "Literatur/pauly2025wasistfair/2025_Pauly_Was_ist_fair.pdf", "printed", "64-67"),
    ("webb S.87-94 Kap2", "Literatur/webb2020doppeldiagnosen/kap02_fehldiagnosen_doppeldiagnosen_s087-094.pdf", "all", None),
    ("warneckehauke S.242-253", "Literatur/fischer2020begabungsfoerderung/excerpts/021_staerkung_der_bildungsgerechtigkeit_bei_underachie.pdf", "all", None),
    ("muelleroppliger paeddiag S.224-235", "Literatur/muelleroppliger2021paeddiagnostik/Smülleroppliger2021paedagogischediagnostik S.224-238.pdf", "all", None),
    ("kappus S.63-70,74", "Literatur/kappus2010migration/source.pdf", "printed", "63-70,74"),
    # Stützliteratur
    ("baudson21 S.115-128", "Literatur/baudson2021wasdenken/source.pdf", "printed", "115-128"),
    ("muop modelle S.204-219", "Literatur/muelleroppliger2021handbuch/Mülleroppliger2021begabungsmpdeöle S.204-219.pdf", "all", None),
    ("baudson25 besserfinden S.35-40", "Literatur/pauly2025wasistfair/2025_Pauly_Was_ist_fair.pdf", "printed", "35-40"),
    ("trautmann S.34-41", "Literatur/trautmann2016einfuehrung/Trautmann2016einführungMultiple intelligenzen s 34-41.pdf", "all", None),
    ("lehwald S.78-92", "Literatur/lehwald2017motivation/Lehwald 2017 motivation trifft begabung S.77-92.pdf", "all", None),
    ("erzinger S.45-48", "Literatur/erzinger2023pisa/source.pdf", "printed", "45-48"),
    ("bfs S.34-35", "Literatur/bfs2022migration/source.pdf", "printed", "34-35"),
]

def parse_spec(s):
    pages = []
    for part in s.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            pages.extend(range(int(a), int(b) + 1))
        else:
            pages.append(int(part))
    return pages

def find_printed_offset(doc, target_page, scan_first_n=20):
    """Try to find offset by searching the first N pages for a printed page label.
    Returns offset such that PDF index = printed - 1 - offset, or None.
    """
    # Heuristic: find a page where text contains the target_page number prominently
    # at top/bottom; not robust but helps. Fallback: try offset 0.
    return None

def extract_printed(doc, printed_pages, label):
    """Extract printed pages from the PDF, trying common offsets."""
    out = []
    total = doc.page_count
    # Try a few offsets and pick the one where pages exist
    candidates = list(range(0, 30))  # offset 0..29 (printed - 1 - offset = idx)
    # We'll just emit all candidates with text — too verbose. Better: emit
    # idx = printed - 1 (offset 0) and also idx = printed - 1 - 12 etc as fallback.
    # Simpler: for each printed, just emit idx=printed-1 (which works for most front-loaded PDFs)
    for printed in printed_pages:
        idx = printed - 1
        if 0 <= idx < total:
            try:
                txt = doc[idx].get_text("text").strip()
            except Exception as e:
                txt = f"[ERROR: {e}]"
        else:
            txt = f"[OUT OF RANGE: idx={idx}, total={total}]"
        out.append((printed, idx, txt))
    return out

def extract_all(doc):
    out = []
    for i in range(doc.page_count):
        try:
            txt = doc[i].get_text("text").strip()
        except Exception as e:
            txt = f"[ERROR: {e}]"
        out.append((None, i, txt))
    return out

print(f"# Vortrag1.md Quellenbelege — extrahierte Seitentexte\n")
print(f"Generated by /tmp/extract_vortrag1.py\n")

for label, rel, mode, spec in TASKS:
    path = os.path.join(BASE, rel)
    print(f"\n{'#'*80}\n# {label}\n# Datei: {rel}\n{'#'*80}\n")
    if not os.path.exists(path):
        print(f"!!! MISSING: {path}")
        continue
    try:
        doc = fitz.open(path)
    except Exception as e:
        print(f"!!! OPEN ERROR: {e}")
        continue
    print(f"# Total pages: {doc.page_count}\n")
    if mode == "all":
        results = extract_all(doc)
    else:
        results = extract_printed(doc, parse_spec(spec), label)
    for printed, idx, txt in results:
        head = f"--- printed S.{printed} | PDF idx {idx} ---" if printed else f"--- PDF idx {idx} ---"
        print(head)
        print(txt[:5000])  # cap each page to 5000 chars to avoid bloat
        if len(txt) > 5000:
            print("\n[... truncated ...]")
        print()
    doc.close()
