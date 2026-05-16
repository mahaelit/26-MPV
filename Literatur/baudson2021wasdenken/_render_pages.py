#!/usr/bin/env python3
"""Rendert die 14 PDF-Seiten als JPEG-Bilder fuer Vision-Verifikation.
Mapping: PDF[0] = Buchseite 115, PDF[13] = Buchseite 128."""
import fitz, os, time, glob

PDF = 'source.pdf'
PDF0_BUCHSEITE = 115
MAX_W = 1600     # max Breite in Pixel (etwas kleiner als Grossrieder, mehr Seiten)
QUALITY = 75

print(f'[1/3] Lade PDF: {PDF}', flush=True)
doc = fitz.open(PDF)
print(f'      {doc.page_count} Seiten', flush=True)

os.makedirs('pages', exist_ok=True)
for old in glob.glob('pages/*.jpg'):
    os.remove(old)
print(f'[2/3] Rendere alle Seiten als JPEG (max {MAX_W}px Breite, Q{QUALITY}) ...', flush=True)
t0 = time.time()
for i in range(doc.page_count):
    buchseite = i + PDF0_BUCHSEITE
    out = f'pages/p{i+1:02d}_S{buchseite}.jpg'
    page = doc[i]
    src_w = page.rect.width
    zoom = MAX_W / src_w
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    pix.pil_save(out, format='JPEG', quality=QUALITY, optimize=True)
    sz = os.path.getsize(out) / 1024
    print(f'      PDF[{i:02d}] -> {out}  ({pix.width}x{pix.height}, {sz:.0f} KB)', flush=True)

print(f'[3/3] Fertig in {time.time()-t0:.1f}s', flush=True)
