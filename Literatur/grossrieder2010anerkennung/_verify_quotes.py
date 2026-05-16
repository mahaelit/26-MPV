#!/usr/bin/env python3
"""Audit fuer grossrieder2010anerkennung.
Pruefung: PDF-Text-Extraktion, Locator-Verifikation, Bauer-These S. 91."""
import fitz, re, unicodedata, time, sys, glob

PDF_GLOB = '*.pdf'
PDF0_BUCHSEITE = 87  # erste Seite des Beitrags

def norm(s):
    s = unicodedata.normalize('NFKC', s)
    s = re.sub(r'[\u00ad\u200b\u2006\u2009]', '', s)
    s = re.sub(r'-\s*\n\s*', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s

print('[1/4] PDF lokalisieren ...', flush=True)
pdfs = [p for p in glob.glob(PDF_GLOB) if 'rossrieder' in p or 'rossrieder' in p.lower()]
if not pdfs:
    pdfs = glob.glob(PDF_GLOB)
pdf = pdfs[0]
print(f'      PDF = {pdf}', flush=True)
doc = fitz.open(pdf)
print(f'      {doc.page_count} PDF-Seiten', flush=True)

print('[2/4] Text-Extraktion pruefen ...', flush=True)
total = 0
for i in range(doc.page_count):
    raw = doc[i].get_text()
    total += len(raw)
    print(f'      PDF[{i:02d}] = ca. S.{i+PDF0_BUCHSEITE}  ({len(raw)} chars)', flush=True)
print(f'      Summe Textzeichen: {total}', flush=True)
if total < 200:
    print('      !!! BILDSCAN ohne Text-Layer - OCR/Vision noetig !!!', flush=True)
    sys.exit(0)

pages = [(i+PDF0_BUCHSEITE, doc[i].get_text(), norm(doc[i].get_text()))
         for i in range(doc.page_count)]

print('[3/4] Suche bestehende Zitatfragmente Z1-Z4 + neue Kandidaten ...', flush=True)
zitate = [
    ('Z1-a', 'Anerkennung zweiter Ordnung'),
    ('Z1-b', 'egalit\u00e4ren Differenz'),
    ('Z1-c', 'Grundhaltung der Anerkennung'),
    ('Z2-a', 'unabh\u00e4ngig von Leistungen'),
    ('Z2-b', 'mit je eigenen W\u00fcnschen'),
    ('Z3-a', 'Komplimente, Lob'),
    ('Z3-b', 'l\u00e4chelnd zunicken'),
    ('Z3-c', 'direkter Beobachtung nicht zug\u00e4nglich'),
    ('Z4-a', 'Schulklima'),
    ('Z4-b', 'Selbstwertgef\u00fchl'),
    ('Z4-b2','Selbstwertgef\u00fchl'),
    ('Z4-c', 'Hilflosigkeit'),
    # Bauer-These S. 91 fuer mpv.tex Z. 2220 (`parencite[S.,91]`)
    ('Bauer','Bauer'),
    ('Bauer-Beziehung', 'Beziehung'),
    ('Bauer-Motivation', 'Motivation'),
    # Peer/Anerkennungsdynamik S. 88, 91
    ('Peer-1', 'Peer'),
    ('Anerkennung-erster','Anerkennung erster Ordnung'),
    # Ordnungs-Begriff fundamental
    ('Prengel','Prengel'),
]
for label, needle in zitate:
    n = norm(needle)
    hits = [bs for (bs, _, t) in pages if n in t]
    flag = 'OK' if hits else 'XX'
    print(f'      {flag} {label:<18} "{needle[:35]:<35}" -> S. {hits}', flush=True)

print('[4/4] Kontext-Auszuege fuer Schluesselbegriffe (erstes Vorkommen):', flush=True)
for label, needle in [('Anerkennung 2.O.', 'Anerkennung zweiter Ordnung'),
                       ('Komplimente/Lob', 'Komplimente, Lob'),
                       ('Bauer', 'Bauer'),
                       ('Peer/Beziehung', 'Peer'),
                       ('Selbstwertgefuehl','Selbstwertgef\u00fchl')]:
    n = norm(needle)
    found = False
    for (bs, _, t) in pages:
        idx = t.find(n)
        if idx >= 0:
            ctx = t[max(0, idx-100):idx+400]
            print(f'\n  >>> {label}  S. {bs} <<<', flush=True)
            print('  ' + ctx, flush=True)
            found = True
            break
    if not found:
        print(f'\n  >>> {label}  NICHT GEFUNDEN <<<', flush=True)

print('\nFERTIG.', flush=True)
