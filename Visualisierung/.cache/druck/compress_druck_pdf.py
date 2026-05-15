#!/usr/bin/env python3
"""Wendet das bestehende archiv/compress_pdfs.py auf das Druckdokument an.

Strategie: nutzt compress_pdf() aus archiv/compress_pdfs.py, schreibt eine
komprimierte Kopie neben das Original.

Default: 1400 px / JPEG-Q70 (laut Faustregel im Original-Skript).
"""
import sys, os, importlib.util, time

BASE = "/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV/26-MPV"
PARENT = os.path.dirname(BASE)
SRC = os.path.join(PARENT, "Druckdokument_Kernliteratur_2026.pdf")
# Suffix optional via 3. CLI-Arg
suffix = sys.argv[3] if len(sys.argv) > 3 else "compressed"
DST = os.path.join(PARENT, f"Druckdokument_Kernliteratur_2026_{suffix}.pdf")

# compress_pdf() aus archiv/compress_pdfs.py importieren
spec = importlib.util.spec_from_file_location(
    "compress_pdfs", os.path.join(BASE, "archiv/compress_pdfs.py"))
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

WIDTH   = int(sys.argv[1]) if len(sys.argv) > 1 else 1400
QUALITY = int(sys.argv[2]) if len(sys.argv) > 2 else 70

print(f"Komprimiere: {SRC}")
print(f"             -> {DST}")
print(f"Parameter:   width={WIDTH}px, JPEG-Q={QUALITY}")
t0 = time.time()
orig, new = mod.compress_pdf(__import__("pathlib").Path(SRC),
                              __import__("pathlib").Path(DST),
                              WIDTH, QUALITY)
dt = time.time() - t0
factor = orig / new if new else 0
print(f"\nFertig in {dt:.1f}s: {orig/1048576:.1f} MB -> {new/1048576:.1f} MB (Faktor {factor:.1f})")
