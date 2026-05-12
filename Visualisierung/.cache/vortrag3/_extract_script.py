#!/usr/bin/env python3
"""Extract pages relevant to Vortrag3.md sources."""
import fitz, os
BASE = "/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV/26-MPV"

# (label, relpath, mode, spec)
# mode: 'all' = all pages, 'auto' = printed -> idx with offset auto-detect, 'sub' = subset by PDF idx
TASKS = [
    # (label, relpath, first_printed_page) — PDF is treated as starting at first_printed_page
    ("grossrieder S.88-94", "Literatur/grossrieder2010anerkennung/Grossrieder2010Nerkennung in buholzer kummerwyss.pdf", 88),
    ("kuhl2021 S.185-202", "Literatur/Kuhl2021bildungbegabung/Kuhl2021begabildungbeziehungsusbperspsychsicht S.185-202.pdf", 185),
    ("wagener S.418-424", "Literatur/wagener2021bfförderndhemmend/Wagener2021bfhemmendförderndimklassenklntext S418-424.pdf", 418),
    ("behrensen S.86-98", "Literatur/behrensen2019inklusive/source.pdf", 86),
    ("kuhl2019 S.35-54", "Literatur/kuhl2019diversitaet/source.pdf", 35),
    ("boosnuenning S.51-65", "Literatur/boosnuenning2022interethnisch/source.pdf", 51),
    ("kesselshannover S.288", "Literatur/kesselshannover2015gleichaltrige/source.pdf", None),  # full book, scan all
    ("tschopp S.35-40", "Literatur/tschoppgruetterbuholzer2022intergruppenkontakt/source.pdf", 35),
    ("baumert S.40-49", "Literatur/baumert2022freundschaftwerte/source.pdf", 40),
    ("evers S.21-27", "Literatur/evers2025stress/source.pdf", 21),
    ("gysinscherzinger S.8-12", "Literatur/gysinscherzinger2022freundschaftenwertvoll/source.pdf", 8),
    ("baudson21 S.115-129", "Literatur/baudson2021wasdenken/source.pdf", 115),
]

def extract_all(doc):
    out = []
    for i in range(doc.page_count):
        t = doc[i].get_text("text").strip()
        out.append((None, i, t))
    return out

def extract_auto(doc, p_from, p_to):
    """Try to find the right offset by looking for a page where text is substantial."""
    best = 0
    best_len = -1
    for off in range(0, 30):
        idx = p_from - 1 + off
        if 0 <= idx < doc.page_count:
            t = doc[idx].get_text("text").strip()
            if len(t) > 50:
                best_len = len(t); best = off; break
    out = []
    for p in range(p_from, p_to + 1):
        idx = p - 1 + best
        if 0 <= idx < doc.page_count:
            t = doc[idx].get_text("text").strip()
            out.append((p, idx, t))
        else:
            out.append((p, idx, "[OUT OF RANGE]"))
    return out, best

for label, rel, first_page in TASKS:
    path = os.path.join(BASE, rel)
    print(f"\n{'='*80}\n=== {label} | {rel}\n{'='*80}")
    if not os.path.exists(path):
        print("MISSING"); continue
    doc = fitz.open(path)
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
