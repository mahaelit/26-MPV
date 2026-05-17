#!/usr/bin/env python3
"""Render alle Seiten von source.pdf als JPEG (Q75, max 1600 px) für Vision-Verifikation."""
from pathlib import Path
import fitz

HERE = Path(__file__).parent
PDF = HERE / "source.pdf"
OUT = HERE / "pages"
OUT.mkdir(exist_ok=True)

# Buchseiten S. 204-219 (16 PDF-Seiten)
START_PAGE = 204
MAX_W = 1600
QUALITY = 75

doc = fitz.open(str(PDF))
print(f"PDF: {doc.page_count} Seiten")

for i, page in enumerate(doc):
    book_page = START_PAGE + i
    # Berechne Zoom für max. 1600 px Breite
    rect = page.rect
    zoom = min(MAX_W / rect.width, 3.0)
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    out_file = OUT / f"p{i+1:02d}_S{book_page}.jpg"
    pix.pil_save(str(out_file), format="JPEG", quality=QUALITY, optimize=True)
    print(f"  S.{book_page} -> {out_file.name} ({out_file.stat().st_size/1024:.0f} KB)")

doc.close()
print("Done.")
