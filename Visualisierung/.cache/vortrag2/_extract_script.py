#!/usr/bin/env python3
"""Extract pages relevant to Vortrag2.md sources."""
import fitz, os
BASE = "/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV/26-MPV"

# (label, relpath, mode, spec)
#  mode 'all' = all pages, 'sub' = subset by PDF idx, 'auto' = printed -> idx with offset auto-detect
TASKS = [
    # Kernliteratur
    ("nottbusch S.125-138", "Literatur/nottbusch2017graphomotorik/source.pdf", "all", None),
    ("hurschler S.1-24", "Literatur/hurschler2020handschriftbeurteilung/source.pdf", "all", None),
    ("gold S.50-53", "Literatur/gold2018lesenkannmanlernen/Gold2018 Migrationsprache S.50-53.pdf", "all", None),
    ("gold S.62-66", "Literatur/gold2018lesenkannmanlernen/Gold2018 schwacheleser S62-66.pdf", "all", None),
    ("gold S.67-88", "Literatur/gold2018lesenkannmanlernen/Gold2018lesenkannmanlernen S67-88.pdf", "all", None),
    ("lehwald S.77-92", "Literatur/lehwald2017motivation/Lehwald 2017 motivation trifft begabung S.77-92.pdf", "all", None),
    ("lehwald S.47-75", "Literatur/lehwald2017motivation/Lehwald 2017 motivation trifft begabung S. 47-75.pdf", "all", None),
    # Stützliteratur
    ("hoyer S.111-113", "Literatur/hoyer2013begabung/source.pdf", "auto", (111, 113)),
    ("sturm S.183-198", "Literatur/sturm2016graphomotorik/source.pdf", "auto", (183, 198)),
]

def extract_all(doc):
    out = []
    for i in range(doc.page_count):
        t = doc[i].get_text("text").strip()
        out.append((None, i, t))
    return out

def extract_auto(doc, p_from, p_to):
    """Try a few offsets; pick the one where the first page has the largest text length."""
    best = None
    best_len = -1
    for off in range(0, 20):
        idx = p_from - 1 + off  # try idx = printed-1, +1, +2, ...
        if 0 <= idx < doc.page_count:
            t = doc[idx].get_text("text").strip()
            if len(t) > best_len and len(t) > 50:
                best_len = len(t)
                best = off
                break  # first plausible
    if best is None:
        best = 0
    out = []
    for p in range(p_from, p_to + 1):
        idx = p - 1 + best
        if 0 <= idx < doc.page_count:
            t = doc[idx].get_text("text").strip()
            out.append((p, idx, t))
        else:
            out.append((p, idx, "[OUT OF RANGE]"))
    return out, best

for label, rel, mode, spec in TASKS:
    path = os.path.join(BASE, rel)
    print(f"\n{'='*80}\n=== {label} | {rel}\n{'='*80}")
    if not os.path.exists(path):
        print("MISSING"); continue
    doc = fitz.open(path)
    print(f"# pages={doc.page_count}")
    if mode == "all":
        results = extract_all(doc)
        offset = None
    elif mode == "auto":
        results, offset = extract_auto(doc, spec[0], spec[1])
        print(f"# auto-offset={offset}")
    for p, idx, t in results:
        hdr = f"--- printed S.{p} (idx {idx}, len={len(t)}) ---" if p else f"--- idx {idx} (len={len(t)}) ---"
        print(hdr)
        if t:
            print(t[:3000])
            if len(t) > 3000: print("[...trunc...]")
        else:
            print("(leer — Bildscan ohne OCR)")
    doc.close()
