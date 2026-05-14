#!/usr/bin/env python3
"""Compare new V4 supplementary PDFs vs current workspace state."""
import os, fitz

NEW_DIR = "/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV/Literatur/FehlendeSeiten MPV/Definitiv MPV Literatur Frage 4"
OLD_BASE = "/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV/26-MPV/Literatur"

# Map new file -> existing workspace counterpart (rel. to OLD_BASE) or None
MAPPING = {
    "Baudson2021 Was Menschen über Hochbegabung und Hochbegabte denken s.117-118.pdf":
        "baudson2021wasdenken/source.pdf",
    "Grossenbacher tettenborn 2014 in stamm Talent und Begabung in der VS der deutschsprachigen Schweiz 317-325.pdf":
        "stamm2014handbuch/Grossenbacher tettenborn 2014 in stamm Talent und Begabung in der VS der deutschsprachigen Schweiz 317-325.pdf",
    "Horvath2021elitebegabungsozialeungleichkeitgerechtigkwitsfragen S 77-85.pdf":
        "horvath2021elite/Horvath2021elitebegabungsozialeungleichkeitgerechtigkwitsfragen S 77-85.pdf",
    "Kummerwyssbuholzer2010heterogenität S.7-12_S.78-85.pdf":
        "buholzer2010allegleich/source_s078-085.pdf",
    "Lehwald2017förderungerkenntnisstreben S.151-158.pdf":
        "lehwald2017motivation/Lehwald2017 motbeg S.141-165.pdf",
    "Mülleroppliger2021adaptivelernarchitektur S.274-385.pdf":
        "mülleroppliger2021adaptivelernarchitektur/Mülleroppliger2021adaptivelernarchizektur S.274-385.pdf",
    "Mülleroppliger2021begabungsmodelle S.204-219.pdf":
        "muelleroppliger2021handbuch/Mülleroppliger2021begabungsmpdeöle S.204-219.pdf",
    "Reisrenzullimüller2021SEM S.333-345.pdf":
        "reisrenzullimüller2021SEM/Reisrenzullimüller2021SEM S.333-345.pdf",
    "Schulteetal2020infischeretalindividuellepotenzialentwicklunglernarchitektur 254-273.pdf":
        "fischer2020begabungsfoerderung/excerpts/022_individuelle_potenzialentwicklung_durch_staerkenor.pdf",
    "Sedmakkapferer2021begabtenförderungalsgerechtigkeitsfragehandbuchbegabunginmüllrroplliger S. 65-75.pdf":
        None,  # FEHLTE!
    "Smülleroppliger2021paedagogischediagnostik S.224-238.pdf":
        "muelleroppliger2021paeddiagnostik/Smülleroppliger2021paedagogischediagnostik S.224-238.pdf",
    "Vmüller2021pluralrgsinklusionbildungsgerechtigkeit.pdf":
        "muelleroppliger2021plurale/Vmüller2021pluralrgsinklusionbildungsgerechtigkeit.pdf",
    "Weigand2021begabungbildungperson S.46-59.pdf":
        "weigand2021person/Weigand2021begabungbildungperson S.59.pdf",
    "Weigandkaiser2021separstiv oderintegrativ handbuchbegabungmülleropp S. 290298.pdf":
        None,  # FEHLTE!
    "hoyer2013ausoppligereinführung94-99.pdf":
        "hoyer2013begabung/source.pdf",
}

print(f"{'STATUS':<10} {'NEW (P)':>8} {'OLD (P)':>8}  FILE")
print("-" * 110)
for new_name, old_rel in MAPPING.items():
    new_path = os.path.join(NEW_DIR, new_name)
    new_doc = fitz.open(new_path)
    new_pages = new_doc.page_count
    new_doc.close()
    if old_rel is None:
        status = "  NEU!"
        old_pages = "-"
    else:
        old_path = os.path.join(OLD_BASE, old_rel)
        if not os.path.exists(old_path):
            status = "  ERS."
            old_pages = "MISSING"
        else:
            old_doc = fitz.open(old_path)
            old_pages = str(old_doc.page_count)
            old_doc.close()
            if new_pages > int(old_pages):
                status = "  +ERW."
            elif new_pages == int(old_pages):
                status = "  =="
            else:
                status = "  --"
    print(f"{status:<10} {new_pages:>8} {old_pages:>8}  {new_name[:80]}")
