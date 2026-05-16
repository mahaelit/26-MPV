#!/usr/bin/env python3
"""Volltext-Extraktion + Schluesselbegriff-Suche fuer Pass-2-Audit."""
import fitz, re, unicodedata

PDF = 'source.pdf'
PDF0_BUCHSEITE = 21

def norm(s):
    s = unicodedata.normalize('NFKC', s)
    s = re.sub(r'[\u00ad\u200b\u2006\u2009]', '', s)
    s = re.sub(r'-\s*\n\s*', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s

doc = fitz.open(PDF)
print(f'[1] PDF: {doc.page_count} Seiten = S. {PDF0_BUCHSEITE}-{PDF0_BUCHSEITE+doc.page_count-1}', flush=True)

pages = []
for i in range(doc.page_count):
    raw = doc[i].get_text()
    n = norm(raw)
    pages.append((i+PDF0_BUCHSEITE, raw, n))

with open('_volltext.txt', 'w') as f:
    for buchseite, raw, _ in pages:
        f.write(f'\n\n========== S. {buchseite} ==========\n\n')
        f.write(raw)
print('[2] Volltext -> _volltext.txt', flush=True)

# Mpv.tex-relevante Begriffe pruefen
suchbegriffe = [
    'Hippocampus', 'Hippokampus',     # KRITISCH: behauptet im mpv.tex
    'Amygdala',
    'praefrontal', 'präfrontal',
    'Cortisol', 'Kortisol',
    'IQ-Test', 'IQ',
    'Pruefung', 'Prüfung',
    'Stress',
    'chronisch',
    'Selbstregulation',
    'Gedächtnis', 'Gedaechtnis',
    'Problemlös', 'Problemloes',
    'Cortex', 'Kortex',
    # mpv.tex Z. 2179: Andauernder Stress beeintraechtigt Gedaechtnis, Lernleistung, Selbstregulation, Problemloesen
    'Lernleistung',
    # mpv.tex Z. 4781: neuronale Voraussetzungen
    'neuronal',
    # mpv.tex Z. 4789: Entlastungsfaktoren / SOLUX
    'Entlastung',
    'fair',
    'Begabungsgerecht',
]
print(f'[3] Schluesselbegriff-Suche ({len(suchbegriffe)} Begriffe):', flush=True)
for needle in suchbegriffe:
    n = norm(needle)
    hits = [bs for (bs, _, t) in pages if n in t]
    flag = 'OK ' if hits else 'XX '
    print(f'    {flag}{needle:<25} -> S. {hits}', flush=True)
