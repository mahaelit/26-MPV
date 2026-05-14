#!/usr/bin/env python3
"""Detect idx <-> book-page mapping for collection PDFs (Pauly, Fischer, eBooks)."""
import os, fitz, re, json
BASE = "/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV/26-MPV"

# (label, rel_path, target_book_pages) – probe pages we want to find
PROBES = {
    "pauly2025_baudson": ("Literatur/pauly2025wasistfair/2025_Pauly_Was_ist_fair.pdf",
                          [35, 36, 37, 38, 39, 40]),
    "pauly2025_koop":   ("Literatur/pauly2025wasistfair/2025_Pauly_Was_ist_fair.pdf",
                          [64, 65, 66, 67]),
    "fischer2020_warnecke": ("Literatur/fischer2020begabungsfoerderung/source.pdf",
                          [241, 242, 245, 250, 253]),
    "maehler2018_haag": ("Literatur/maehler2018diagnostik/source.pdf",
                          [153, 154, 165, 187, 188]),
    "hoyer2013": ("Literatur/hoyer2013begabung/source.pdf",
                          [94, 95, 99]),
    "kellerkoller2011_erkennen": ("Literatur/kellerkoller2011erkennen/source.pdf",
                          [1, 2]),
    "kosorok": ("Literatur/kosoroklabhart2021voneltern/source.pdf",
                          [14, 15, 38, 39]),
    "macha2019": ("Literatur/macha2019gender/source.pdf",
                          [160, 161, 170, 171]),
    "udl": ("Literatur/muellerboeschschaffnermenn2021udl/source.pdf",
                          [94, 95, 103, 116]),
    "kuhl2019": ("Literatur/kuhl2019diversitaet/source.pdf",
                          [35, 36, 53, 54]),
    "behrensen2019": ("Literatur/behrensen2019inklusive/source.pdf",
                          [86, 98]),
    "evers2025": ("Literatur/evers2025stress/source.pdf",
                          [21, 22, 27]),
    "baumert2022": ("Literatur/baumert2022freundschaftwerte/source.pdf",
                          [40, 41, 49]),
    "tschopp2022": ("Literatur/tschoppgruetterbuholzer2022intergruppenkontakt/source.pdf",
                          [35, 36, 40]),
    "boos2022": ("Literatur/boosnuenning2022interethnisch/source.pdf",
                          [51, 52, 65]),
    "kessels2015": ("Literatur/kesselshannover2015gleichaltrige/source.pdf",
                          [288]),
    "hurschler2020": ("Literatur/hurschler2020handschriftbeurteilung/source.pdf",
                          [1, 2, 24]),
    "nottbusch2017": ("Literatur/nottbusch2017graphomotorik/source.pdf",
                          [128, 136]),
    "baudson2021": ("Literatur/baudson2021wasdenken/source.pdf",
                          [115, 129]),
}


def find_page_idx(doc, target_pages):
    """For each target page number, find the idx where that book page is shown.
    Heuristic: scan first 60 chars of each page, look for the printed page number.
    """
    idx_for_page = {}
    n = doc.page_count
    for i in range(n):
        t = doc[i].get_text("text").strip()
        if not t:
            continue
        # Look at the first 80 characters for header page numbers
        head = t[:80]
        # Page numbers usually appear as standalone integers near margins
        nums = re.findall(r"(?:^|\n)\s*(\d{1,3})\s*(?:\n|$|\s)", head)
        # Also try last 80 chars (footer)
        tail = t[-80:]
        nums += re.findall(r"(?:^|\n)\s*(\d{1,3})\s*(?:\n|$|\s)", tail)
        for ns in nums:
            n_int = int(ns)
            if n_int in target_pages and n_int not in idx_for_page:
                idx_for_page[n_int] = i
    return idx_for_page


report = {}
for label, (rel, targets) in PROBES.items():
    path = os.path.join(BASE, rel)
    if not os.path.exists(path):
        report[label] = {"error": "MISSING", "path": rel}
        continue
    doc = fitz.open(path)
    found = find_page_idx(doc, targets)
    # Compute offset = book_page - idx for each found
    offsets = sorted({p - i for p, i in found.items()})
    # Most consistent
    report[label] = {
        "path": rel,
        "n_pages": doc.page_count,
        "targets": targets,
        "found_idx": found,
        "offsets": offsets,
        "offset_consistent": (len(offsets) == 1),
    }
    doc.close()

with open(os.path.join(BASE, "Visualisierung/.cache/druck/_offsets.json"), "w") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

# Markdown summary
lines = ["# Auto-Offset-Detection\n"]
for k, v in report.items():
    if "error" in v:
        lines.append(f"## {k}\n  - ERROR: {v['error']}\n")
        continue
    lines.append(f"## {k}")
    lines.append(f"  - PDF: `{v['path']}` ({v['n_pages']} S.)")
    lines.append(f"  - Targets: {v['targets']}")
    lines.append(f"  - Found: {v['found_idx']}")
    lines.append(f"  - Offset(s): {v['offsets']}  {'OK' if v['offset_consistent'] else 'INCONSISTENT'}")
    lines.append("")

with open(os.path.join(BASE, "Visualisierung/.cache/druck/_offsets.md"), "w") as f:
    f.write("\n".join(lines))
print("OK")
