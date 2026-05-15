#!/usr/bin/env python3
"""Erzeugt den finalen Buchumschlag fuer die Klebebindung.

Layout im Datenformat 33,0 x 21,6 cm:
  [Beschnitt 3 mm] [Rueckseite 148 mm] [Buchruecken 28 mm] [Vorderseite 148 mm] [Beschnitt 3 mm]

Inhalt:
  Vorderseite: Titelblatt aus 2026_PHLU_MPV_Inti_Merolli.pdf (Seite 1, vektorbasiert)
  Buchruecken: schlichter Titel + Autor + Jahr, in Leserichtung von unten nach oben
  Rueckseite:  ermutigender Spruch fuer die Pruefungssituation
"""
import os
import fitz

BASE = "/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV/26-MPV"
PARENT = os.path.dirname(BASE)
TITLE_PDF = os.path.join(BASE, "2026_PHLU_MPV_Inti_Merolli.pdf")
OUT_PDF = os.path.join(PARENT, "2026_PHLU_MPV_Umschlag.pdf")

MM = 72.0 / 25.4

# Layout (alles in pt nach mm-Umrechnung)
DATA_W = 330.0 * MM
DATA_H = 216.0 * MM
BLEED  = 3.0   * MM
SAFE   = 5.0   * MM
SPINE  = 28.0  * MM
COVER  = 148.0 * MM

# Bereiche im Datenformat (x-Achse)
RUECK_X0 = BLEED
RUECK_X1 = BLEED + COVER
SPINE_X0 = RUECK_X1
SPINE_X1 = SPINE_X0 + SPINE
VORDER_X0 = SPINE_X1
VORDER_X1 = VORDER_X0 + COVER

# y-Achse: Endformat
END_Y0 = BLEED
END_Y1 = BLEED + 210.0 * MM

# Schriftfarben
COL_DARK    = (0.10, 0.10, 0.10)
COL_MEDIUM  = (0.28, 0.28, 0.28)
COL_SOFT    = (0.45, 0.45, 0.45)
COL_QUIET   = (0.60, 0.60, 0.60)


def draw_vorderseite(page: fitz.Page, src_title: fitz.Document) -> None:
    """Titelblatt vektorbasiert auf die Vorderseite einbetten (zentriert)."""
    safe_x0 = VORDER_X0 + SAFE
    safe_x1 = VORDER_X1 - SAFE
    safe_y0 = END_Y0 + SAFE
    safe_y1 = END_Y1 - SAFE
    inner_w = safe_x1 - safe_x0
    inner_h = safe_y1 - safe_y0

    sp = src_title[0]
    r = sp.rect
    scale = min(inner_w / r.width, inner_h / r.height)
    new_w = r.width * scale
    new_h = r.height * scale
    cx = (safe_x0 + safe_x1) / 2
    cy = (safe_y0 + safe_y1) / 2
    target = fitz.Rect(cx - new_w / 2, cy - new_h / 2,
                       cx + new_w / 2, cy + new_h / 2)
    page.show_pdf_page(target, src_title, 0)


def draw_buchruecken(page: fitz.Page) -> None:
    """Schlichte Beschriftung des Buchruecken, in Leserichtung von unten nach oben.

    Toleranz +/- 10 % am Buchruecken -> wir bleiben +/- 4 mm von den Kanten weg
    (3 mm Toleranz + 1 mm Sicherheit).
    """
    # Inhalts-Box: zentriert, mit grosszuegigem Sicherheits-Abstand
    inset_x = 4.0 * MM
    inset_y = 12.0 * MM
    rect = fitz.Rect(SPINE_X0 + inset_x, END_Y0 + inset_y,
                     SPINE_X1 - inset_x, END_Y1 - inset_y)

    spine_text = (
        "Verdeckte Begabungen bei frühem Zweitspracherwerb"
        "      ·      "
        "Inti Merolli"
        "      ·      "
        "PHLU MPV 2026"
    )
    # rotate=90 -> Text liest sich von unten nach oben (Standard fuer Buchruecken)
    page.insert_textbox(
        rect, spine_text,
        fontsize=8.5,
        fontname="helv",
        color=COL_DARK,
        rotate=90,
        align=fitz.TEXT_ALIGN_CENTER,
    )


def draw_rueckseite(page: fitz.Page) -> None:
    """Ermutigender Spruch zentriert auf der Rueckseite."""
    # Etwas mehr Atemraum als das reine 5 mm Sicherheits-Minimum
    safe_x0 = RUECK_X0 + SAFE + 12.0 * MM
    safe_x1 = RUECK_X1 - SAFE - 12.0 * MM
    safe_y0 = END_Y0 + SAFE
    safe_y1 = END_Y1 - SAFE
    H = safe_y1 - safe_y0

    # 1) Hauptzitat (gross, kursiv, leicht ins obere Drittel gesetzt)
    main_top = safe_y0 + H * 0.28
    main_box = fitz.Rect(safe_x0, main_top, safe_x1, main_top + 50)
    page.insert_textbox(
        main_box,
        "Begabungen zeigen sich,\nwenn die Bedingungen stimmen.",
        fontsize=15,
        fontname="heit",  # Helvetica-Oblique (italic)
        color=COL_DARK,
        align=fitz.TEXT_ALIGN_CENTER,
    )

    # 2) Brueckensatz (mittel)
    bridge_top = safe_y0 + H * 0.50
    bridge_box = fitz.Rect(safe_x0, bridge_top, safe_x1, bridge_top + 28)
    page.insert_textbox(
        bridge_box,
        "Auch deine.",
        fontsize=12,
        fontname="helv",
        color=COL_MEDIUM,
        align=fitz.TEXT_ALIGN_CENTER,
    )

    # 3) Atem-Pausen + Schluss-Satz (klein, ruhig)
    breath_top = safe_y0 + H * 0.65
    breath_box = fitz.Rect(safe_x0, breath_top, safe_x1, breath_top + 90)
    page.insert_textbox(
        breath_box,
        "Atme ein.\nAtme aus.\n\nVertrau auf dein Mosaik.",
        fontsize=10.5,
        fontname="helv",
        color=COL_SOFT,
        align=fitz.TEXT_ALIGN_CENTER,
    )

    # 4) Signatur unten
    sig_box = fitz.Rect(safe_x0, safe_y1 - 14 * MM, safe_x1, safe_y1 - 5 * MM)
    page.insert_textbox(
        sig_box,
        "PHLU Masterprüfung Vertiefung 2026  ·  Inti Merolli",
        fontsize=7.5,
        fontname="helv",
        color=COL_QUIET,
        align=fitz.TEXT_ALIGN_CENTER,
    )


def main() -> None:
    if not os.path.exists(TITLE_PDF):
        raise SystemExit(f"FEHLER: Titelblatt nicht gefunden: {TITLE_PDF}")

    doc = fitz.open()
    page = doc.new_page(width=DATA_W, height=DATA_H)

    src_title = fitz.open(TITLE_PDF)
    draw_vorderseite(page, src_title)
    draw_buchruecken(page)
    draw_rueckseite(page)
    src_title.close()

    doc.save(OUT_PDF, deflate=True, garbage=4)
    doc.close()

    sz_kb = os.path.getsize(OUT_PDF) / 1024
    print(f"Umschlag erstellt: {OUT_PDF}")
    print(f"  Datenformat: 330 x 216 mm  (Endformat 324 x 210 mm)")
    print(f"  Buchruecken: 28 mm")
    print(f"  Groesse:     {sz_kb:.1f} KB")


if __name__ == "__main__":
    main()
