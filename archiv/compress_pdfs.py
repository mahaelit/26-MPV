#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""compress_pdfs.py — Fotografierte Buchscans (Smartphone-Fotos als PDF) auf
handhabbare Grösse schrumpfen, ohne die Lesbarkeit für Open-Book-Prüfung zu
opfern.

Hintergrund: Fotografien von Buchseiten liegen typischerweise als
hochauflösende JPEGs im PDF vor (3000-4000 px Breite, ~60-70 MB pro Kapitel).
Für das Archiv in `Literatur/<bibkey>/` ist das zu gross. Dieses Skript:

1. extrahiert aus jeder PDF-Seite das eingebettete Bild (ein Bild pro Seite,
   wie Foxit/Adobe-Scans es produzieren);
2. skaliert es auf eine gewählte max. Breite (Standard: 1400 px, ca. 120 DPI
   auf A4);
3. rekodiert es als JPEG mit konfigurierbarer Qualität (Standard: 70);
4. baut ein neues, kompaktes PDF mit identischer Seiten-Abmessung.

Faustregel aus dem MPV-Repo:
- 1400 px / JPEG-Q70 -> ca. 1/7 der Originalgrösse, Text klar lesbar.
- 1200 px / JPEG-Q70 -> ca. 1/10, Text-Kursivschrift leicht weicher.
- 1000 px / JPEG-Q75 -> ca. 1/12, nur für grosse Schriftgrade geeignet.

Aufruf (Beispiel):

    python3 compress_pdfs.py "$ONEDRIVE/Literatur/stamm2025vonuntennachoben" \
                             "Literatur/stamm2025vonuntennachoben" \
                             --width 1400 --quality 70

Dependencies: pymupdf (fitz), Pillow. Installation in venv:

    python3 -m venv .venv
    .venv/bin/pip install pymupdf Pillow
    .venv/bin/python3 compress_pdfs.py ...
"""

from __future__ import annotations

import argparse
import io
import os
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
    from PIL import Image
except ImportError:
    print(
        "ERR: benötigte Pakete fehlen. Installieren mit\n"
        "    pip install pymupdf Pillow",
        file=sys.stderr,
    )
    sys.exit(2)


def compress_pdf(src: Path, dst: Path, target_width: int, jpeg_q: int) -> tuple[int, int]:
    """Eine einzelne PDF-Datei komprimieren.

    Returns: (original_bytes, compressed_bytes)
    """
    doc = fitz.open(str(src))
    orig_size = src.stat().st_size

    out = fitz.open()
    for page_idx, page in enumerate(doc):
        imgs = page.get_images(full=True)
        if not imgs:
            # Fallback: Seite rendern, wenn kein eingebettetes Bild
            zoom = 120 / 72.0  # 120 DPI
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        else:
            xref = imgs[0][0]
            base = doc.extract_image(xref)
            try:
                img = Image.open(io.BytesIO(base["image"]))
            except Exception as exc:
                print(f"  Seite {page_idx + 1}: Bildextraktion fehlgeschlagen ({exc}); Fallback Rendering", file=sys.stderr)
                zoom = 120 / 72.0
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat, alpha=False)
                img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

        orig_w, orig_h = img.size
        if orig_w > target_width:
            ratio = target_width / orig_w
            new_size = (target_width, int(orig_h * ratio))
            img = img.resize(new_size, Image.LANCZOS)

        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")

        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=jpeg_q, optimize=True)
        new_page = out.new_page(width=page.rect.width, height=page.rect.height)
        new_page.insert_image(page.rect, stream=buf.getvalue())

    out.save(str(dst), deflate=True, garbage=4)
    out.close()
    doc.close()

    new_size = dst.stat().st_size
    return orig_size, new_size


def build_mapping_stamm2024() -> dict[str, str]:
    """Spezial-Mapping für stamm2025vonuntennachoben: chaotische Originaldateinamen
    auf einheitliche `sNNN-NNN.pdf` umschreiben."""
    return {
        "Stamm2025untennachoben s.13-38.pdf":     "s013-038.pdf",
        "Stamm2025vonuntennachoben S.35-57.pdf":  "s035-057.pdf",
        "Stamm2025vonuntennachoben58-79.pdf":     "s058-079.pdf",
        "Stamm2025vonuntennachoben80-104.pdf":    "s080-104.pdf",
        "Stamm2025vonuntennachoben106-129.pdf":   "s106-129.pdf",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("source_dir", type=Path, help="Quellordner mit PDFs")
    ap.add_argument("target_dir", type=Path, help="Zielordner (wird angelegt)")
    ap.add_argument("--width", type=int, default=1400, help="Max. Bildbreite in px (Standard: 1400)")
    ap.add_argument("--quality", type=int, default=70, help="JPEG-Qualität 0-100 (Standard: 70)")
    ap.add_argument(
        "--rename", choices=["none", "stamm2024"], default="none",
        help="Dateinamen umschreiben (für spezielle Quellen)",
    )
    ap.add_argument(
        "--force", action="store_true",
        help="Zieldateien überschreiben, auch wenn sie existieren",
    )
    args = ap.parse_args()

    if not args.source_dir.is_dir():
        print(f"ERR: {args.source_dir} ist kein Verzeichnis.", file=sys.stderr)
        return 2

    args.target_dir.mkdir(parents=True, exist_ok=True)

    mapping = build_mapping_stamm2024() if args.rename == "stamm2024" else {}

    total_orig = 0
    total_new = 0
    n = 0
    for src_path in sorted(args.source_dir.iterdir()):
        if src_path.suffix.lower() != ".pdf":
            continue
        if src_path.name in mapping:
            dst_name = mapping[src_path.name]
        elif args.rename == "stamm2024":
            # unbekannte Datei im stamm2024-Modus: skippen
            continue
        else:
            dst_name = src_path.name
        dst_path = args.target_dir / dst_name

        if dst_path.exists() and not args.force:
            print(f"SKIP {src_path.name} (Zieldatei existiert)")
            continue

        print(f"COMPRESS {src_path.name}")
        orig, new = compress_pdf(src_path, dst_path, args.width, args.quality)
        total_orig += orig
        total_new += new
        n += 1
        factor = orig / new if new else 0.0
        print(f"      -> {dst_name}  {orig / 1048576:>6.1f} MB -> {new / 1048576:>5.2f} MB  (Faktor {factor:.1f})")

    if n:
        overall = total_orig / total_new if total_new else 0.0
        print(f"\nGesamt {n} Dateien: {total_orig / 1048576:.1f} MB -> {total_new / 1048576:.1f} MB (Faktor {overall:.1f})")
    else:
        print("Keine PDFs gefunden oder alle bereits vorhanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
