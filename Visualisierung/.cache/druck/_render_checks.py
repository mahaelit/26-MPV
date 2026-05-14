#!/usr/bin/env python3
import fitz, os
out = "/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV/26-MPV/Visualisierung/.cache/druck/_renders"
os.makedirs(out, exist_ok=True)
BASE = "/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV"
F2 = os.path.join(BASE, "Literatur/FehlendeSeiten MPV/Definitiv MPV Literatur Frage 2")
F3 = os.path.join(BASE, "Literatur/FehlendeSeiten MPV/Definitiv MPV Literatur Frage 3")
WS = os.path.join(BASE, "26-MPV/Literatur")

targets = [
    ("lehwald_70-72_foto.png",  os.path.join(F2, "lehwald2017motivation S.70-72.pdf"), 0),
    ("baudson_p1.png",          os.path.join(F3, "Baudson Was Menschen über Hochbegabung und Hochbegabte denken s.115-132.pdf"), 0),
    ("baudson_p2.png",          os.path.join(F3, "Baudson Was Menschen über Hochbegabung und Hochbegabte denken s.115-132.pdf"), 1),
    ("baudson_p13_last.png",    os.path.join(F3, "Baudson Was Menschen über Hochbegabung und Hochbegabte denken s.115-132.pdf"), 13),
    ("lehwald_47-75_first.png", os.path.join(WS, "lehwald2017motivation/Lehwald 2017 motivation trifft begabung S. 47-75.pdf"), 0),
    ("lehwald_47-75_last.png",  os.path.join(WS, "lehwald2017motivation/Lehwald 2017 motivation trifft begabung S. 47-75.pdf"), 23),
]
for name, path, idx in targets:
    if not os.path.exists(path):
        print(f"MISSING: {path}")
        continue
    d = fitz.open(path)
    if idx >= d.page_count:
        print(f"OOB: idx {idx} >= {d.page_count} ({name})")
        d.close(); continue
    pix = d[idx].get_pixmap(dpi=110)
    pix.save(os.path.join(out, name))
    print(f"OK {name}  ({pix.width}x{pix.height})")
    d.close()
