#!/usr/bin/env python3
"""Rendert die 9 PDF-Seiten als JPEG-Bilder fuer Vision-Verifikation."""
import fitz, os, time, glob

PDF = glob.glob('*Nerkennung*.pdf')[0]
MAX_W = 1800     # max Breite in Pixel
QUALITY = 75

print(f'[1/3] Lade PDF: {PDF}', flush=True)
doc = fitz.open(PDF)
print(f'      {doc.page_count} Seiten', flush=True)

os.makedirs('pages', exist_ok=True)
# alte Renderings (zu gross) entfernen
for old in glob.glob('pages/*.jpg'):
    os.remove(old)
print(f'[2/3] Rendere alle Seiten als JPEG (max {MAX_W}px Breite, Q{QUALITY}) ...', flush=True)
t0 = time.time()
for i in range(doc.page_count):
    buchseite = i + 87
    out = f'pages/p{i+1:02d}_S{buchseite}.jpg'
    page = doc[i]
    # Zoom so dass Breite = MAX_W
    src_w = page.rect.width
    zoom = MAX_W / src_w
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    pix.pil_save(out, format='JPEG', quality=QUALITY, optimize=True)
    sz = os.path.getsize(out) / 1024
    print(f'      PDF[{i:02d}] -> {out}  ({pix.width}x{pix.height}, {sz:.0f} KB)', flush=True)

print(f'[3/3] Fertig in {time.time()-t0:.1f}s', flush=True)
