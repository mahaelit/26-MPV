#!/usr/bin/env python3
"""Folgepruefungen: Z01-Suche, Druck/Stress-Kontext, Extensionsgedaechtnis-Belege."""
import fitz, re, unicodedata, time

def norm(s):
    s = unicodedata.normalize('NFKC', s)
    s = re.sub(r'[\u00ad\u200b\u2006\u2009]', '', s)
    s = re.sub(r'-\s*\n\s*', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s

print('[1] Lade PDF ...', flush=True)
doc = fitz.open('source.pdf')
pages = [(i+36, doc[i].get_text(), norm(doc[i].get_text())) for i in range(doc.page_count)]
print(f'    OK ({len(pages)} Seiten 36-59)', flush=True)

print('\n[2] S. 36 (Anfang Kapitel, fuer Z01 wichtig):', flush=True)
print(pages[0][1][:1500], flush=True)

print('\n[3] Suche Stress/Druck/Reaktion-Kontext fuer mpv.tex:2255-Behauptung:', flush=True)
needles = [
    'Druck', 'Stress', 'erstarr', 'Rueckzug', 'Verweigerung',
    'Selbstoeffnung', 'Selbstoffnung', 'Affektregulation',
    'negativer Affekt', 'positiver Affekt', 'Ueberforderung',
    'Bedrohung', 'Angst',
]
needles = [n.replace('ae','\u00e4').replace('oe','\u00f6').replace('ue','\u00fc')
             .replace('ss','\u00df') for n in needles]
for n in needles:
    nn = norm(n)
    hits = [(bs, t.find(nn)) for (bs, _, t) in pages if nn in t]
    print(f'    "{n:<25}" -> {[bs for bs,_ in hits]}', flush=True)

print('\n[4] Extensionsgedaechtnis-Kontext auf S. 45 (erstes Vorkommen):', flush=True)
n = norm('Extensionsged\u00e4chtnis')
for (bs, _, t) in pages:
    idx = t.find(n)
    if idx >= 0:
        print(f'    >>> S. {bs} <<<', flush=True)
        print('    ' + t[max(0,idx-200):idx+500], flush=True)
        break

print('\n[5] Affekt + Extensionsgedaechtnis-Verbindung (S. 45-47):', flush=True)
for bs in (45, 46, 47):
    t = next(t for (b, _, t) in pages if b == bs)
    for kw in ['blockier', 'verschliess', 'verschlie\u00df', 'reduziert',
               'Modus', 'Affekt']:
        idx = t.find(kw)
        if idx >= 0:
            print(f'    S.{bs} "{kw}": ...{t[max(0,idx-60):idx+180]}...', flush=True)
            break

print('\nFERTIG.', flush=True)
