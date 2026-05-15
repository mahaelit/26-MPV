#!/usr/bin/env python3
"""Normalisiert alle Seiten eines PDFs auf A4-Format (zentriert, skaliert, mit Rand).

Hintergrund:
  build_druck_pdf.py uebernimmt die MediaBox der Originalseiten. Foto-Scans sind
  oft 2-4x groesser als A4 -> beim Drucken auf A4 wird unten/rechts beschnitten.
  Beispiel: stamm2021 S.577 wurde unten abgeschnitten.

Verhalten:
  - Seiten, die bereits A4 sind (innerhalb 2 pt Toleranz) -> unveraendert kopiert.
  - Alle anderen Seiten -> auf neue A4-Seite skaliert eingefuegt:
    - Aspect-Ratio bleibt erhalten
    - Zentriert mit konfigurierbarem Rand (Default 5 mm)
    - Original-Inhalt bleibt vektorbasiert (kein Re-Rendering noetig)

Usage:
  python3 normalize_a4.py [margin_mm]
  python3 normalize_a4.py 5

Output:
  Druckdokument_Kernliteratur_2026_a4.pdf
"""
import os
import sys
import time
import fitz

PARENT = "/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV"
INPUT = os.path.join(PARENT, "Druckdokument_Kernliteratur_2026.pdf")
OUTPUT = os.path.join(PARENT, "Druckdokument_Kernliteratur_2026_a4.pdf")

# A4 in PDF-Punkten
A4_W, A4_H = 595.0, 842.0
TOL = 2.0

def normalize_to_a4(input_pdf: str, output_pdf: str, margin_mm: float = 5.0) -> dict:
    """Normalisiere alle Seiten auf A4. Gibt Statistik zurueck."""
    margin = margin_mm * 72.0 / 25.4
    inner_w = A4_W - 2 * margin
    inner_h = A4_H - 2 * margin

    src = fitz.open(input_pdf)
    dst = fitz.open()

    n_passthrough = 0  # bereits A4
    n_scaled = 0       # skaliert auf A4
    n_total = src.page_count

    for i, sp in enumerate(src):
        r = sp.rect
        is_a4 = abs(r.width - A4_W) < TOL and abs(r.height - A4_H) < TOL

        if is_a4:
            # 1:1 uebernehmen (z. B. Trennblaetter)
            dst.insert_pdf(src, from_page=i, to_page=i)
            n_passthrough += 1
        else:
            # Auf neue A4-Seite skaliert einfuegen
            new_page = dst.new_page(width=A4_W, height=A4_H)
            scale = min(inner_w / r.width, inner_h / r.height)
            new_w = r.width * scale
            new_h = r.height * scale
            x = (A4_W - new_w) / 2.0
            y = (A4_H - new_h) / 2.0
            target_rect = fitz.Rect(x, y, x + new_w, y + new_h)
            # show_pdf_page bettet die Originalseite vektorbasiert ein
            new_page.show_pdf_page(target_rect, src, i)
            n_scaled += 1

        if (i + 1) % 50 == 0:
            print(f"  ... {i + 1}/{n_total} Seiten verarbeitet", flush=True)

    dst.save(output_pdf, deflate=True, garbage=4)
    dst.close()
    src.close()

    return {
        "total": n_total,
        "passthrough_a4": n_passthrough,
        "scaled_to_a4": n_scaled,
        "size_in_mb": os.path.getsize(input_pdf) / 1024 / 1024,
        "size_out_mb": os.path.getsize(output_pdf) / 1024 / 1024,
    }


if __name__ == "__main__":
    margin_mm = float(sys.argv[1]) if len(sys.argv) > 1 else 5.0

    if not os.path.exists(INPUT):
        sys.exit(f"FEHLER: Input nicht gefunden: {INPUT}")

    print(f"Input:  {INPUT}")
    print(f"Output: {OUTPUT}")
    print(f"Rand:   {margin_mm} mm")
    print()

    t0 = time.time()
    stats = normalize_to_a4(INPUT, OUTPUT, margin_mm=margin_mm)
    dt = time.time() - t0

    print()
    print(f"Fertig in {dt:.1f}s")
    print(f"  Seiten gesamt:       {stats['total']}")
    print(f"  bereits A4 (1:1):    {stats['passthrough_a4']}")
    print(f"  auf A4 skaliert:     {stats['scaled_to_a4']}")
    print(f"  Datei: {stats['size_in_mb']:.1f} MB -> {stats['size_out_mb']:.1f} MB")
    print()
    print(f"-> Drucke jetzt {os.path.basename(OUTPUT)} auf A4: kein Beschnitt mehr.")
