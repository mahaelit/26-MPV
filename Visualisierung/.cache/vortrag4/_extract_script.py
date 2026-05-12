#!/usr/bin/env python3
"""Extract pages relevant to Vortrag4.md sources."""
import fitz, os
BASE = "/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV/26-MPV"

# (label, relpath, first_printed_page)
TASKS = [
    # Kernliteratur
    ("buholzerkw2010 S.78-85",
     "Literatur/buholzer2010allegleich/source_s078-085.pdf", 78),
    ("muop2021plurale S.32-42",
     "Literatur/muelleroppliger2021plurale/Vmüller2021pluralrgsinklusionbildungsgerechtigkeit.pdf", 32),
    ("muop2021begabungsmodelle S.204-219",
     "Literatur/muelleroppliger2021handbuch/Mülleroppliger2021begabungsmpdeöle S.204-219.pdf", 204),
    ("reisrenzullimuop2021sem S.333-345",
     "Literatur/reisrenzullimüller2021SEM/Reisrenzullimüller2021SEM S.333-345.pdf", 333),
    ("muop2021paeddiag S.224-235 [recap V1]",
     "Literatur/muelleroppliger2021paeddiagnostik/Smülleroppliger2021paedagogischediagnostik S.224-238.pdf", 224),
    ("muop2021adaptive S.374-385",
     "Literatur/mülleroppliger2021adaptivelernarchitektur/Mülleroppliger2021adaptivelernarchizektur S.274-385.pdf", None),  # multi-chapter file
    ("schulteterhardt2020 S.264-267",
     "Literatur/fischer2020begabungsfoerderung/excerpts/022_individuelle_potenzialentwicklung_durch_staerkenor.pdf", None),
    ("lehwald2017 S.151-158",
     "Literatur/lehwald2017motivation/Lehwald2017 motbeg S.141-165.pdf", 141),
    ("hoyer2013 S.94-99",
     "Literatur/hoyer2013begabung/source.pdf", None),  # need to find offset
    ("grossenbacher2014 S.317-325",
     "Literatur/stamm2014handbuch/Grossenbacher tettenborn 2014 in stamm Talent und Begabung in der VS der deutschsprachigen Schweiz 317-325.pdf", 317),
    # Stütze
    ("horvath2021elite S.77-85",
     "Literatur/horvath2021elite/Horvath2021elitebegabungsozialeungleichkeitgerechtigkwitsfragen S 77-85.pdf", 77),
    ("weigand2021person S.46-59",
     "Literatur/weigand2021person/Weigand2021begabungbildungperson S.59.pdf", None),
]

for label, rel, first_page in TASKS:
    path = os.path.join(BASE, rel)
    print(f"\n{'='*80}\n=== {label} | {rel}\n{'='*80}")
    if not os.path.exists(path):
        print("MISSING"); continue
    try:
        doc = fitz.open(path)
    except Exception as e:
        print(f"ERROR opening: {e}"); continue
    print(f"# pages={doc.page_count}")
    for i in range(doc.page_count):
        t = doc[i].get_text("text").strip()
        if first_page is not None:
            p = first_page + i
            hdr = f"--- Buchseite {p} (idx {i}, len={len(t)}) ---"
        else:
            hdr = f"--- idx {i} (len={len(t)}) ---"
        print(hdr)
        if t:
            print(t[:3200])
            if len(t) > 3200: print("[...trunc...]")
        else:
            print("(leer — Bildscan ohne OCR)")
    doc.close()
