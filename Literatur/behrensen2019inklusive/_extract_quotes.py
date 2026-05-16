#!/usr/bin/env python3
"""Volltext-Extraktion + Schluesselbegriff-Suche fuer Pass-2-Audit."""
import fitz, re, unicodedata

PDF = 'source.pdf'
PDF0_BUCHSEITE = 86  # PDF[0] = Buchseite 86

def norm(s):
    s = unicodedata.normalize('NFKC', s)
    s = re.sub(r'[\u00ad\u200b\u2006\u2009]', '', s)
    s = re.sub(r'-\s*\n\s*', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s

doc = fitz.open(PDF)
print(f'[1] PDF: {doc.page_count} Seiten = S. {PDF0_BUCHSEITE}-{PDF0_BUCHSEITE+doc.page_count-1}', flush=True)

# Ganzen Volltext extrahieren
pages = []
for i in range(doc.page_count):
    raw = doc[i].get_text()
    n = norm(raw)
    pages.append((i+PDF0_BUCHSEITE, raw, n))
    print(f'    PDF[{i:02d}] = S. {i+PDF0_BUCHSEITE}  ({len(raw)} chars)', flush=True)

# Volltext speichern
with open('_volltext.txt', 'w') as f:
    for buchseite, raw, _ in pages:
        f.write(f'\n\n========== S. {buchseite} ==========\n\n')
        f.write(raw)
print('[2] Volltext -> _volltext.txt', flush=True)

# Schluesselbegriffe fuer mpv.tex-Argumentation
suchbegriffe = [
    # Kumulative Belastung (mpv.tex Z. 1832, 1941, 2038, 2371)
    'kumulativ',
    'Belastung',
    'Bewaeltigungsressourcen',
    'Bewältigungsressourcen',
    'Resilienz',
    # Migrationsbezug (Z. 1942, 2039, 2373)
    'Fluchtmigration',
    'Geflüchtet',
    'Geflüchtete',
    'sprachliche Isolation',
    'soziale Netzwerke',
    'Verlust',
    # Defizit vs. Ressourcen (Z. 2027, 4533)
    'Defizit',
    'Ressourcen',
    'Schatzkiste',
    # Inklusive Begabungsfoerderung als Antwort
    'Antwort',
    'Bildungsherausforderung',
    'Gebot der Stunde',
    # Verhalten als Ergebnis (Z. 2371)
    'Verweigerung',
    'Trauma',
    'traumasensibel',
    'traumasensible',
    # Pathologisierung
    'Pathologie',
    'Pathologisierung',
    # Selbstkompetenz
    'Selbstkompetenz',
]
print(f'[3] Schluesselbegriff-Suche ({len(suchbegriffe)} Begriffe):', flush=True)
for needle in suchbegriffe:
    n = norm(needle)
    hits = [bs for (bs, _, t) in pages if n in t]
    flag = 'OK ' if hits else 'XX '
    print(f'    {flag}{needle:<30} -> S. {hits}', flush=True)
