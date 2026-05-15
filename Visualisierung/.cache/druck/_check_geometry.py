#!/usr/bin/env python3
"""Diagnose: Welche Seiten im Druck-PDF sind nicht A4?"""
import os, fitz

PARENT = "/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV"
PDF = os.path.join(PARENT, "Druckdokument_Kernliteratur_2026.pdf")

# A4 in PDF-Punkten (1 pt = 1/72 inch)
A4_W, A4_H = 595.0, 842.0
TOL = 2.0  # 2 pt Toleranz

doc = fitz.open(PDF)
print(f"Dokument: {os.path.basename(PDF)}  ({doc.page_count} Seiten)\n")

# Statistik
sizes = {}
oversized = []  # Seiten, die A4 überschreiten

for i, page in enumerate(doc):
    r = page.rect
    w, h = round(r.width, 1), round(r.height, 1)
    key = (w, h)
    sizes[key] = sizes.get(key, 0) + 1

    # Über A4 hinaus?
    over_w = w - A4_W
    over_h = h - A4_H
    if over_w > TOL or over_h > TOL:
        oversized.append((i + 1, w, h, over_w, over_h))

# Ausgabe: Größenverteilung
print("=== Seitengrößen-Verteilung ===")
for (w, h), count in sorted(sizes.items(), key=lambda kv: -kv[1]):
    is_a4 = abs(w - A4_W) < TOL and abs(h - A4_H) < TOL
    flag = "  [A4]" if is_a4 else ""
    print(f"  {w:6.1f} x {h:6.1f} pt   ({w/72*25.4:5.1f} x {h/72*25.4:5.1f} mm)  -> {count:4d} Seiten{flag}")

# Über A4 hinausragende
print(f"\n=== {len(oversized)} Seiten überschreiten A4 (= werden beim Druck beschnitten) ===")
for pno, w, h, ow, oh in oversized[:30]:
    over_w_mm = ow / 72 * 25.4
    over_h_mm = oh / 72 * 25.4
    print(f"  Seite {pno:4d}: {w:.1f} x {h:.1f} pt  | über A4: +{ow:.1f} pt breit (+{over_w_mm:.1f} mm), +{oh:.1f} pt hoch (+{oh/72*25.4:.1f} mm)")
if len(oversized) > 30:
    print(f"  ... und {len(oversized) - 30} weitere")

doc.close()
