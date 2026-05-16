#!/usr/bin/env python3
"""Extrahiert wortgetreue Snippets fuer neue Belegzitate Z05/Z06."""
import fitz, re, unicodedata

def norm(s):
    s = unicodedata.normalize('NFKC', s)
    s = re.sub(r'[\u00ad\u200b\u2006\u2009]', '', s)
    s = re.sub(r'-\s*\n\s*', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s

doc = fitz.open('source.pdf')
pages = [(i+36, doc[i].get_text(), norm(doc[i].get_text())) for i in range(doc.page_count)]
def page(bs):
    return next(t for (b, _, t) in pages if b == bs)

# Volltext der Schluesselseiten
for bs in (38, 41, 42, 43, 45, 46, 47, 53):
    print(f'\n========== S. {bs} ==========', flush=True)
    print(page(bs), flush=True)
