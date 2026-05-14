#!/usr/bin/env python3
"""Extract pages relevant to Vortrag5.md sources."""
import fitz, os
BASE = "/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV/26-MPV"

# (label, relpath, first_printed_page)
TASKS = [
    # Kernliteratur (eigene PDFs)
    ("muellerboeschschaffnermenn2021udl S.94-116",
     "Literatur/muellerboeschschaffnermenn2021udl/source.pdf", None),
    ("macha2019gender S.160-171",
     "Literatur/macha2019gender/source.pdf", None),
    ("groschefussangelgraesel2020kokonstruktion S.463-472",
     "Literatur/groschefussangelgraesel2020kokonstruktion/source.pdf", None),
    ("widmerwolf2018multiprofessionell S.299-309",
     "Literatur/widmerwolf2018multiprofessionell/source.pdf", None),
    ("kosoroklabhart2021voneltern S.14-39",
     "Literatur/kosoroklabhart2021voneltern/source.pdf", None),
    ("baudson2025besserfinden in pauly2025 S.35-40",
     "Literatur/pauly2025wasistfair/2025_Pauly_Was_ist_fair.pdf", None),
    ("nguyensliwka2021massnahmen S.348-356",
     "Literatur/nguyensliwka2021massnahmenkompetenzlp/Nguyensliwka2021massnahmenlpbf S 348-356.pdf", 348),
    # Stützliteratur (V5)
    ("kummerwyss2017kooperativunterrichten S.151-160",
     "Literatur/kummerwyss2017kooperativunterrichten/source.pdf", None),
    # Bildscans (Hand- und Buchscans nur fürs Abprüfen, OCR liefert i.d.R. nichts)
    ("weigand2021person S.46-59 (Bildscan)",
     "Literatur/weigand2021person/Weigand2021begabungbildungperson S.59.pdf", None),
    ("horvath2021elite S.77-85 (Bildscan)",
     "Literatur/horvath2021elite/Horvath2021elitebegabungsozialeungleichkeitgerechtigkwitsfragen S 77-85.pdf", 77),
]

for label, rel, first_page in TASKS:
    path = os.path.join(BASE, rel)
    print(f"\n{'='*80}\n=== {label} | {rel}\n{'='*80}")
    if not os.path.exists(path):
        print("MISSING"); continue
    try:
        doc = fitz.open(path)
    except Exception as e:
        print(f"ERROR: {e}"); continue
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
