#!/usr/bin/env python3
"""Erzeugt das finale Abgabedokument: 2026_PHLU_MPV_Quellen_IM[_A5|_Druck].pdf

- Seite 1: Titelblatt aus 2026_PHLU_MPV_Inti_Merolli.pdf (vektorbasiert)
- Seiten 2..N: komprimierte Originalseiten aus Druckdokument_Kernliteratur_2026.pdf
- Zielgroesse: <= 100 MB

Modi:
  (default)   A4, 595 Seiten, ohne Beschnitt           -> ..._Quellen_IM.pdf
  --a5        A5, 595 Seiten, ohne Beschnitt           -> ..._Quellen_IM_A5.pdf
  --druck     A5-Datenformat (154x216 mm), 596 Seiten, -> ..._Quellen_IM_Druck.pdf
              Graustufen, 5 mm Sicherheitsabstand +
              3 mm Beschnitt = 8 mm Rand. Konform zur
              Klebebindungs-Spezifikation der Druckerei.

Strategie: iterativ Komprimierungsprofil waehlen, das die 100-MB-Grenze
einhaelt. Vektor-Seiten (Trennblaetter, Verlags-PDFs) bleiben 1:1; nur
Foto-Scans werden gerastert.

Aufruf:
  python3 build_quellen_pdf.py              # A4
  python3 build_quellen_pdf.py --a5         # A5
  python3 build_quellen_pdf.py --druck      # Druckerei-konform A5 mit Bleed
  python3 build_quellen_pdf.py --a5 900 75  # manuell width/Q
"""
import io
import os
import sys
import time
from pathlib import Path

import fitz
from PIL import Image

BASE = "/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV/26-MPV"
PARENT = os.path.dirname(BASE)

TITLE_PDF = os.path.join(BASE, "2026_PHLU_MPV_Inti_Merolli.pdf")
DRUCK_PDF = os.path.join(PARENT, "Druckdokument_Kernliteratur_2026.pdf")
TMP_RESIZED = os.path.join(BASE, "Visualisierung/.cache/druck/_quellen_a5resized.pdf")
TMP_PDF = os.path.join(BASE, "Visualisierung/.cache/druck/_quellen_compressed.pdf")

TARGET_MAX_MB = 100
HEADROOM_MB = 1.0  # Puffer fuer Titelblatt + Container-Overhead

# Seitenformate (in PDF-Punkten, 1 pt = 1/72 inch)
A4_W, A4_H = 595.0, 842.0
A5_W, A5_H = 420.0, 595.0  # exakt halbe A4-Flaeche
# Druckerei-Datenformat: A5 Endformat (148x210) + 3 mm Beschnitt rundum
MM_TO_PT = 72.0 / 25.4
DRUCK_W = 154.0 * MM_TO_PT  # ~436.5 pt
DRUCK_H = 216.0 * MM_TO_PT  # ~612.3 pt
# Margin: 3 mm Beschnitt + 5 mm Sicherheit = 8 mm vom Datenformat-Rand
# -> effektive Inhaltsflaeche 138x200 mm
DRUCK_MARGIN_MM = 8.0

# Smart-Compress: vektorbasierte Seiten (Trennblaetter, Verlags-PDFs) bleiben 1:1
# (perfekte Lesbarkeit, minimale Groesse). Nur Foto-Scan-Seiten werden gerastert.
# Heuristik: Eine Seite gilt als "Foto-Scan", wenn ihr groesstes eingebettetes
# Bild >= IMAGE_PIXEL_THRESHOLD Pixel hat.
IMAGE_PIXEL_THRESHOLD = 1_500_000  # 1.5 MP -> typischer Smartphone-Foto-Scan


def _max_image_pixels(doc: fitz.Document, page: fitz.Page) -> int:
    """Gibt die Pixelflaeche des groessten eingebetteten Bildes zurueck."""
    max_px = 0
    for img in page.get_images(full=True):
        xref = img[0]
        try:
            info = doc.extract_image(xref)
        except Exception:
            continue
        px = info.get("width", 0) * info.get("height", 0)
        if px > max_px:
            max_px = px
    return max_px


def smart_compress(src_path: Path, dst_path: Path, target_width: int,
                   jpeg_q: int, grayscale: bool = False) -> dict:
    """Komprimiert nur photographische Seiten; vektorbasierte 1:1 weiterreichen.

    grayscale=True: Foto-Scan-Seiten in 8-Bit Graustufen ("L") konvertieren.
    Vektor-Seiten bleiben unveraendert (Farbinformation egal, Drucker druckt 1/1 s/w).
    """
    doc = fitz.open(str(src_path))
    out = fitz.open()

    n_pass = 0  # vektorbasiert uebernommen
    n_jpeg = 0  # gerastert + JPEG

    for i, page in enumerate(doc):
        max_px = _max_image_pixels(doc, page)

        if max_px < IMAGE_PIXEL_THRESHOLD:
            # vektor-dominiert: 1:1 uebernehmen
            out.insert_pdf(doc, from_page=i, to_page=i)
            n_pass += 1
            continue

        # Foto-Scan: ganze Seite rastern + JPEG
        scale = target_width / page.rect.width
        zoom = max(scale, 0.1)
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False, colorspace=fitz.csGRAY if grayscale else fitz.csRGB)
        mode = "L" if grayscale else "RGB"
        img = Image.frombytes(mode, (pix.width, pix.height), pix.samples)

        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=jpeg_q, optimize=True)

        new_page = out.new_page(width=page.rect.width, height=page.rect.height)
        new_page.insert_image(page.rect, stream=buf.getvalue())
        n_jpeg += 1

    out.save(str(dst_path), deflate=True, garbage=4)
    out.close()
    doc.close()

    return {
        "vector_passthrough": n_pass,
        "rastered_jpeg": n_jpeg,
        "total": n_pass + n_jpeg,
        "size_mb": dst_path.stat().st_size / 1048576,
        "grayscale": grayscale,
    }


def resize_pdf(src_path: Path, dst_path: Path, page_w: float, page_h: float,
               margin_mm: float = 4.0) -> int:
    """Skaliere jede Seite eines PDF auf ein Zielformat (vektorbasiert).
    Aspect-Ratio wird erhalten, zentriert mit margin_mm Rand."""
    margin = margin_mm * 72.0 / 25.4
    inner_w = page_w - 2 * margin
    inner_h = page_h - 2 * margin

    src = fitz.open(str(src_path))
    dst = fitz.open()
    for i, sp in enumerate(src):
        r = sp.rect
        new_page = dst.new_page(width=page_w, height=page_h)
        scale = min(inner_w / r.width, inner_h / r.height)
        new_w = r.width * scale
        new_h = r.height * scale
        x = (page_w - new_w) / 2.0
        y = (page_h - new_h) / 2.0
        target = fitz.Rect(x, y, x + new_w, y + new_h)
        new_page.show_pdf_page(target, src, i)

    dst.save(str(dst_path), deflate=True, garbage=4)
    n = dst.page_count
    dst.close()
    src.close()
    return n


# Komprimierungsprofile - sobald eines unter dem Limit bleibt, Abbruch.
# A4-Profile: Bildbreite ueber A4-Druckflaeche (210 mm)
PROFILES_A4 = [
    (1600, 75, "1600 px / Q75  (exzellent, ~194 dpi)"),
    (1400, 72, "1400 px / Q72  (sehr lesbar, ~169 dpi)"),
    (1300, 70, "1300 px / Q70  (gut lesbar, ~157 dpi)"),
    (1200, 68, "1200 px / Q68  (lesbar, ~145 dpi)"),
    (1100, 65, "1100 px / Q65  (knapp lesbar, ~133 dpi)"),
    (1000, 62, "1000 px / Q62  (Notbremse, ~121 dpi)"),
]

# A5-Profile: A5 ist nur 148 mm breit -> selbe Pixelbreite = doppelte DPI.
# Wir koennen also viel hoehere Qualitaet halten.
PROFILES_A5 = [
    (1400, 80, "1400 px / Q80  (Premium, ~240 dpi)"),
    (1200, 78, "1200 px / Q78  (sehr gut, ~206 dpi)"),
    (1100, 75, "1100 px / Q75  (gut, ~189 dpi)"),
    (1000, 72, "1000 px / Q72  (lesbar, ~172 dpi)"),
    (900,  70, "900 px / Q70   (knapp lesbar, ~154 dpi)"),
    (800,  68, "800 px / Q68   (Notbremse, ~137 dpi)"),
]


def _parse_args(argv: list) -> tuple:
    """Parse: [--a5|--druck] [width quality]. Returns (mode, manual_profile_or_None).

    mode: 'a4' (default) | 'a5' | 'druck'
    """
    args = list(argv)
    mode = "a4"
    if "--druck" in args:
        mode = "druck"
        args.remove("--druck")
    elif "--a5" in args:
        mode = "a5"
        args.remove("--a5")
    manual = None
    if len(args) >= 2:
        w, q = int(args[0]), int(args[1])
        manual = (w, q, f"{w} px / Q{q} (manuell)")
    return mode, manual


def main() -> int:
    if not os.path.exists(TITLE_PDF):
        sys.exit(f"FEHLER: Titelblatt nicht gefunden: {TITLE_PDF}")
    if not os.path.exists(DRUCK_PDF):
        sys.exit(f"FEHLER: Druckdokument nicht gefunden: {DRUCK_PDF}")

    mode, manual = _parse_args(sys.argv[1:])
    grayscale = False
    insert_blank_after_title = False

    if mode == "druck":
        page_w, page_h = DRUCK_W, DRUCK_H
        resize_margin_mm = DRUCK_MARGIN_MM
        out_pdf = os.path.join(PARENT, "2026_PHLU_MPV_Quellen_IM_Druck.pdf")
        profiles = [manual] if manual else PROFILES_A5
        fmt_label = (
            f"Druck-A5  Datenformat 154x216 mm  | "
            f"Endformat 148x210 mm  | 5 mm Sicherheit + 3 mm Beschnitt | "
            f"Graustufen 1/1 s/w  | 596 Seiten (mit Leerseite nach Titel)"
        )
        grayscale = True
        insert_blank_after_title = True
    elif mode == "a5":
        page_w, page_h = A5_W, A5_H
        resize_margin_mm = 3.0
        out_pdf = os.path.join(PARENT, "2026_PHLU_MPV_Quellen_IM_A5.pdf")
        profiles = [manual] if manual else PROFILES_A5
        fmt_label = "A5 (148x210 mm)"
    else:
        page_w, page_h = A4_W, A4_H
        resize_margin_mm = None  # kein Resize fuer A4
        out_pdf = os.path.join(PARENT, "2026_PHLU_MPV_Quellen_IM.pdf")
        profiles = [manual] if manual else PROFILES_A4
        fmt_label = "A4 (210x297 mm)"

    print(f"Format:     {fmt_label}")
    print(f"Titelblatt: {TITLE_PDF}")
    print(f"Druckdok.:  {DRUCK_PDF}  ({os.path.getsize(DRUCK_PDF) / 1048576:.0f} MB)")
    print(f"Output:     {out_pdf}")
    print(f"Limit:      {TARGET_MAX_MB} MB (mit {HEADROOM_MB:.1f} MB Puffer)\n")

    # Bei A5- und Druck-Modus: vor der Komprimierung das Druckdokument resizen
    if mode in ("a5", "druck"):
        size_lbl = "A5" if mode == "a5" else "Druck-Datenformat"
        print(f"Verkleinere Druckdokument auf {size_lbl} (vektorbasiert) ...")
        t0 = time.time()
        n_resized = resize_pdf(Path(DRUCK_PDF), Path(TMP_RESIZED), page_w, page_h, margin_mm=resize_margin_mm)
        resized_mb = os.path.getsize(TMP_RESIZED) / 1048576
        print(f"  -> {n_resized} Seiten, {resized_mb:.1f} MB in {time.time()-t0:.1f}s\n")
        source_for_compress = TMP_RESIZED
    else:
        source_for_compress = DRUCK_PDF

    chosen = None
    last_stats = None
    budget = TARGET_MAX_MB - HEADROOM_MB

    for width, quality, label in profiles:
        print(f"Probiere: {label}{' (Graustufen)' if grayscale else ''}")
        t0 = time.time()
        stats = smart_compress(Path(source_for_compress), Path(TMP_PDF), width, quality, grayscale=grayscale)
        dt = time.time() - t0
        last_stats = stats
        print(
            f"  -> {stats['size_mb']:.1f} MB in {dt:.1f}s   "
            f"(vektor: {stats['vector_passthrough']}, JPEG: {stats['rastered_jpeg']})"
        )
        if stats["size_mb"] <= budget:
            chosen = (width, quality, label, stats)
            break

    if chosen is None:
        width, quality, label = profiles[-1][:3]
        chosen = (width, quality, label, last_stats)
        print(
            f"WARN: Auch '{label}' liegt bei {last_stats['size_mb']:.1f} MB "
            f"(> Budget {budget:.1f} MB)."
        )

    print(
        f"\n>>> Gewaehlt: {chosen[2]} -> {chosen[3]['size_mb']:.1f} MB komprimiertes Druckdok.\n"
    )

    # Final zusammenbauen: Titelblatt (Seite 1) [+ Leerseite] + komprimiertes Druckdok.
    # Bei A5/Druck wird das A4-Titelblatt vektorbasiert auf das Zielformat skaliert.
    print("Fuege Titelblatt voran ...")
    final = fitz.open()

    src_title = fitz.open(TITLE_PDF)
    if mode in ("a5", "druck"):
        margin = resize_margin_mm * 72.0 / 25.4
        inner_w = page_w - 2 * margin
        inner_h = page_h - 2 * margin
        tp = src_title[0]
        r = tp.rect
        scale = min(inner_w / r.width, inner_h / r.height)
        new_w = r.width * scale
        new_h = r.height * scale
        x = (page_w - new_w) / 2.0
        y = (page_h - new_h) / 2.0
        np_page = final.new_page(width=page_w, height=page_h)
        np_page.show_pdf_page(fitz.Rect(x, y, x + new_w, y + new_h), src_title, 0)
    else:
        final.insert_pdf(src_title, from_page=0, to_page=0)
    src_title.close()

    # Druck-Modus: leere Seite nach Titelblatt (Rueckseite Titel),
    # damit das erste Trennblatt auf einer rechten Seite (ungerade) landet
    # und die Seitenzahl auf 596 kommt (Druckerei-Vorgabe).
    if insert_blank_after_title:
        final.new_page(width=page_w, height=page_h)

    src_compressed = fitz.open(TMP_PDF)
    final.insert_pdf(src_compressed)
    src_compressed.close()

    final.save(out_pdf, deflate=True, garbage=4)
    final.close()

    # Aufraeumen
    for tmp in (TMP_PDF, TMP_RESIZED):
        if os.path.exists(tmp):
            os.remove(tmp)

    # Verifikation
    final_doc = fitz.open(out_pdf)
    n_pages = final_doc.page_count
    p0 = final_doc[0].rect
    final_doc.close()
    final_mb = os.path.getsize(out_pdf) / 1048576

    print(f"\nFertig: {out_pdf}")
    print(f"  Seiten:  {n_pages}  (1 Titelblatt + {n_pages - 1} Quellen)")
    print(f"  Format:  {p0.width:.0f}x{p0.height:.0f} pt  ({p0.width/72*25.4:.0f}x{p0.height/72*25.4:.0f} mm)")
    print(f"  Groesse: {final_mb:.1f} MB")
    if final_mb > TARGET_MAX_MB:
        print(f"  ACHTUNG: ueberschreitet das 100-MB-Limit!")
        return 1
    else:
        print(f"  OK: unter 100-MB-Limit (Reserve: {TARGET_MAX_MB - final_mb:.1f} MB)")
        return 0


if __name__ == "__main__":
    sys.exit(main())
