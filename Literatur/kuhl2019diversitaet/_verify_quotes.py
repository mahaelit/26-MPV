#!/usr/bin/env python3
"""Verifiziert die in verified_quotes.md hinterlegten Zitate gegen source.pdf.
Mapping: PDF[0] entspricht Buchseite 36 (im PDF-Header sichtbar)."""
import fitz, re, unicodedata, time, sys

PDF = 'source.pdf'
PDF0_BUCHSEITE = 36  # aus Header der ersten Seite verifiziert

def norm(s):
    s = unicodedata.normalize('NFKC', s)
    s = re.sub(r'[\u00ad\u200b\u2006\u2009]', '', s)  # weiche Trenner / schmale Spaces
    s = re.sub(r'-\s*\n\s*', '', s)                  # Silbentrennung am Zeilenende
    s = re.sub(r'\s+', ' ', s)
    return s

def main():
    print(f'[1/4] Oeffne {PDF} ...', flush=True)
    doc = fitz.open(PDF)
    print(f'      OK - {doc.page_count} PDF-Seiten', flush=True)

    print('[2/4] Extrahiere + normalisiere alle Seiten ...', flush=True)
    t0 = time.time()
    pages = []
    for i in range(doc.page_count):
        raw = doc[i].get_text()
        pages.append((i + PDF0_BUCHSEITE, raw, norm(raw)))
        print(f'      PDF[{i:02d}] = S.{i + PDF0_BUCHSEITE}  ({len(raw)} chars)', flush=True)
    print(f'      OK - {time.time() - t0:.1f}s', flush=True)

    print('[3/4] Suche Kernfragmente der Zitate Z01-Z04 + Folgemotive ...', flush=True)
    zitate = [
        ('Z01-a', 'Die Qualitaet der paedagogischen Beziehung ist aus mehreren Gruenden als ein Schluessel'.replace('ae','\u00e4').replace('oe','\u00f6').replace('ue','\u00fc').replace('ss','\u00df')),
        ('Z01-b', 'funktionsanalytischen Persoenlichkeitstheorie (PSI-Theorie)'.replace('oe','\u00f6')),
        ('Z01-c', 'Selbstmotivierung und Selbstberuhigung bedeutsam'),
        ('Z02-a', 'Beziehungserfahrungen so wichtig fuer die Begabungsentfaltung'.replace('ue','\u00fc')),
        ('Z02-b', 'haengt massgeblich von der Qualitaet der Beziehung'.replace('ae','\u00e4').replace('ss','\u00df')),
        ('Z03-a', 'Erfolg aller noch so guten paedagogischen Massnahmen'.replace('ae','\u00e4').replace('ss','\u00df')),
        ('Z03-b', 'massgeblich von der Qualitaet der Beziehung abhaengt'.replace('ae','\u00e4').replace('ss','\u00df')),
        ('Z04-a', 'verschliesst'.replace('ss','\u00df')),
        ('Z04-b', 'nicht ins Selbst integriert'),
        ('PSI-1', 'Extensionsgedaechtnis'.replace('ae','\u00e4')),
        ('PSI-2', 'negativer Affekt'),
        ('Druck', 'Druck'),
        ('Erstarrung', 'Erstarrung'),
        ('Rueckzug', 'Rueckzug'.replace('ue','\u00fc')),
    ]
    for label, needle in zitate:
        n = norm(needle)
        hits = [bs for (bs, _, t) in pages if n in t]
        flag = 'OK ' if hits else 'XX '
        print(f'      {flag}{label:<10} "{needle[:55]:<55}" -> S. {hits}', flush=True)

    print('[4/4] Kontext-Auszuege (erstes Vorkommen) ...', flush=True)
    for label, needle in [('Z01', zitate[0][1]),
                          ('Z02', zitate[3][1]),
                          ('Z03', zitate[5][1]),
                          ('Z04', zitate[7][1])]:
        n = norm(needle)
        for (bs, _, t) in pages:
            idx = t.find(n)
            if idx >= 0:
                ctx = t[max(0, idx-80):idx+360]
                print(f'\n  >>> {label}  S. {bs} <<<', flush=True)
                print('  ' + ctx, flush=True)
                break
        else:
            print(f'\n  >>> {label}  NICHT GEFUNDEN <<<', flush=True)

    print('\nFERTIG.', flush=True)

if __name__ == '__main__':
    main()
