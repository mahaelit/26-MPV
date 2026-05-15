#!/usr/bin/env python3
"""Erzeugt das Umschlag-Template fuer die Klebebindung.

Spezifikation der Druckerei (Klebebindung A5 hoch, 596 Innenseiten):
  Datenformat:  33,0 x 21,6 cm  (= 30,2 + 2,8 Buchruecken,  inkl. 3 mm Beschnitt rundum)
  Endformat:    32,4 x 21,0 cm  (= 29,6 + 2,8 Buchruecken)
  Buchruecken:  2,8 cm (Toleranz bis 10 % -> 25-31 mm)
  Sicherheit:   >= 5 mm vom Endformat-Rand

Layout im Datenformat:
  [3 mm Beschnitt] [148 mm Rueckseite] [28 mm Buchruecken] [148 mm Vorderseite] [3 mm Beschnitt]
                   ^----------------- 32,4 cm Endformat ------------------^

Erzeugt:
  2026_PHLU_MPV_Umschlag_Template.pdf  (Hilfslinien-Layout, 1 Seite, 330x216 mm)
  Umschlag_README.md                    (Anleitung + Checkliste)
"""
import os
import fitz

BASE = "/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV/26-MPV"
PARENT = os.path.dirname(BASE)
OUT_PDF = os.path.join(PARENT, "2026_PHLU_MPV_Umschlag_Template.pdf")
OUT_README = os.path.join(PARENT, "2026_PHLU_MPV_Umschlag_README.md")

MM_TO_PT = 72.0 / 25.4

# Maße (alles in mm, intern in pt umgerechnet)
DATA_W_MM, DATA_H_MM = 330.0, 216.0                  # Datenformat
END_W_MM, END_H_MM   = 324.0, 210.0                  # Endformat
BLEED_MM             = 3.0                            # Beschnitt rundum
SAFE_MM              = 5.0                            # Sicherheitsabstand zum Endformat
SPINE_MM             = 28.0                           # Buchruecken (Toleranz ±10 %)
COVER_MM             = (END_W_MM - SPINE_MM) / 2.0    # = 148 mm pro Seite

# Farben
COL_TRIM   = (0.85, 0.10, 0.10)  # Magenta-rot: Beschnitt-/Endformat-Linie
COL_SAFE   = (0.10, 0.55, 0.10)  # Gruen: Sicherheits-Bereich
COL_SPINE  = (0.10, 0.30, 0.85)  # Blau: Buchruecken
COL_GUIDE  = (0.60, 0.60, 0.60)  # Hellgrau: Hilfslinien
COL_LABEL  = (0.20, 0.20, 0.20)  # Dunkelgrau: Beschriftung


def mm_box(x_mm: float, y_mm: float, w_mm: float, h_mm: float) -> fitz.Rect:
    """mm-Box (Origin oben-links) -> fitz.Rect."""
    x = x_mm * MM_TO_PT
    y = y_mm * MM_TO_PT
    return fitz.Rect(x, y, x + w_mm * MM_TO_PT, y + h_mm * MM_TO_PT)


def draw_template(page: fitz.Page) -> None:
    shape = page.new_shape()

    # 1. Endformat-Rahmen (3 mm vom Datenformat-Rand eingerueckt)
    end_rect = mm_box(BLEED_MM, BLEED_MM, END_W_MM, END_H_MM)
    shape.draw_rect(end_rect)
    shape.finish(color=COL_TRIM, fill=None, width=0.6, dashes="[4 2] 0")

    # 2. Sicherheitsrahmen (5 mm innerhalb des Endformats)
    safe_rect = mm_box(BLEED_MM + SAFE_MM, BLEED_MM + SAFE_MM,
                       END_W_MM - 2 * SAFE_MM, END_H_MM - 2 * SAFE_MM)
    shape.draw_rect(safe_rect)
    shape.finish(color=COL_SAFE, fill=None, width=0.4, dashes="[2 2] 0")

    # 3. Buchruecken-Bereich (zentriert)
    spine_x = BLEED_MM + COVER_MM
    spine_rect = mm_box(spine_x, BLEED_MM, SPINE_MM, END_H_MM)
    shape.draw_rect(spine_rect)
    shape.finish(color=COL_SPINE, fill=(0.92, 0.95, 1.0), width=0.5)

    # 4. Buchruecken-Toleranzzonen (±10 %, also ±2,8 mm)
    tol = SPINE_MM * 0.10
    # linke Toleranzkante
    for offset in [-tol, tol]:
        x = spine_x + offset
        shape.draw_line(
            fitz.Point(x * MM_TO_PT, BLEED_MM * MM_TO_PT),
            fitz.Point(x * MM_TO_PT, (BLEED_MM + END_H_MM) * MM_TO_PT),
        )
        x2 = spine_x + SPINE_MM + offset
        shape.draw_line(
            fitz.Point(x2 * MM_TO_PT, BLEED_MM * MM_TO_PT),
            fitz.Point(x2 * MM_TO_PT, (BLEED_MM + END_H_MM) * MM_TO_PT),
        )
    shape.finish(color=COL_SPINE, fill=None, width=0.2, dashes="[1 2] 0")

    # 5. Trennlinien Rueckseite/Buchruecken/Vorderseite (gesamtes Datenformat)
    for x_mm in (BLEED_MM + COVER_MM, BLEED_MM + COVER_MM + SPINE_MM):
        shape.draw_line(
            fitz.Point(x_mm * MM_TO_PT, 0),
            fitz.Point(x_mm * MM_TO_PT, DATA_H_MM * MM_TO_PT),
        )
    shape.finish(color=COL_GUIDE, fill=None, width=0.3, dashes="[3 3] 0")

    # 6. Schnittmarken in den 4 Ecken (jeweils 5 mm lang, 2 mm vom Endformat)
    mark_len = 5.0
    gap = 2.0
    corners = [
        (BLEED_MM, BLEED_MM),                          # oben links
        (BLEED_MM + END_W_MM, BLEED_MM),               # oben rechts
        (BLEED_MM, BLEED_MM + END_H_MM),               # unten links
        (BLEED_MM + END_W_MM, BLEED_MM + END_H_MM),    # unten rechts
    ]
    for cx, cy in corners:
        # horizontale Markierung
        sx = cx - mark_len if cx > DATA_W_MM / 2 else cx
        ex = cx if cx > DATA_W_MM / 2 else cx + mark_len
        y_off = -gap if cy < DATA_H_MM / 2 else gap
        shape.draw_line(
            fitz.Point(sx * MM_TO_PT, (cy + y_off - (mark_len if cy < DATA_H_MM/2 else -mark_len)) * MM_TO_PT),
            fitz.Point(sx * MM_TO_PT, (cy + y_off) * MM_TO_PT),
        )
        # vertikale Markierung
        sy = cy - mark_len if cy > DATA_H_MM / 2 else cy
        ey = cy if cy > DATA_H_MM / 2 else cy + mark_len
        x_off = -gap if cx < DATA_W_MM / 2 else gap
        shape.draw_line(
            fitz.Point((cx + x_off - (mark_len if cx < DATA_W_MM/2 else -mark_len)) * MM_TO_PT, sy * MM_TO_PT),
            fitz.Point((cx + x_off) * MM_TO_PT, sy * MM_TO_PT),
        )
    shape.finish(color=COL_TRIM, fill=None, width=0.5)

    shape.commit()

    # 7. Beschriftungen (mittig in jedem Bereich)
    def label(text: str, cx_mm: float, cy_mm: float, size: int = 10, color=COL_LABEL):
        page.insert_text(
            fitz.Point(cx_mm * MM_TO_PT, cy_mm * MM_TO_PT),
            text,
            fontsize=size,
            color=color,
        )

    # Rueckseite
    label("RUECKSEITE",
          BLEED_MM + COVER_MM / 2 - 15, DATA_H_MM / 2 - 4, size=14)
    label("(Klappentext, Autorenfoto, Verlagslogo, ISBN ...)",
          BLEED_MM + COVER_MM / 2 - 45, DATA_H_MM / 2 + 5, size=8, color=COL_GUIDE)

    # Buchruecken
    # Text muss um 90deg gedreht werden (rotate); pymupdf insert_textbox unterstuetzt rotate
    spine_text_rect = mm_box(spine_x + 2, 40, SPINE_MM - 4, DATA_H_MM - 80)
    page.insert_textbox(
        spine_text_rect,
        "BUCHRUECKEN (2,8 cm, ±10 % Toleranz)\n"
        "Empfohlen: Titel + Autor*in, in Lesrichtung von unten nach oben\n"
        "Kein wichtiger Text naeher als 3 mm an die Toleranzkante!",
        fontsize=7,
        color=COL_SPINE,
        rotate=90,
        align=fitz.TEXT_ALIGN_CENTER,
    )

    # Vorderseite
    label("VORDERSEITE",
          BLEED_MM + COVER_MM + SPINE_MM + COVER_MM / 2 - 18,
          DATA_H_MM / 2 - 4, size=14)
    label("(Haupttitel, Untertitel, Autor*in, evtl. Bild)",
          BLEED_MM + COVER_MM + SPINE_MM + COVER_MM / 2 - 40,
          DATA_H_MM / 2 + 5, size=8, color=COL_GUIDE)

    # Legende oben rechts ausserhalb Sicherheitsbereich
    legend_x = BLEED_MM + END_W_MM - 70
    legend_y = BLEED_MM + 8
    page.insert_text(fitz.Point(legend_x * MM_TO_PT, legend_y * MM_TO_PT),
                     "--- Endformat (Schnittkante)", fontsize=6, color=COL_TRIM)
    page.insert_text(fitz.Point(legend_x * MM_TO_PT, (legend_y + 3) * MM_TO_PT),
                     "--- Sicherheitsabstand 5 mm", fontsize=6, color=COL_SAFE)
    page.insert_text(fitz.Point(legend_x * MM_TO_PT, (legend_y + 6) * MM_TO_PT),
                     "--- Buchruecken-Toleranz ±10 %", fontsize=6, color=COL_SPINE)


def main() -> None:
    doc = fitz.open()
    page = doc.new_page(
        width=DATA_W_MM * MM_TO_PT,
        height=DATA_H_MM * MM_TO_PT,
    )
    draw_template(page)
    doc.save(OUT_PDF, deflate=True, garbage=4)
    doc.close()

    readme = f"""# Umschlag-Anleitung — 2026 PHLU MPV (Klebebindung Softcover A5)

## Spezifikation der Druckerei

- **Endformat:** {END_W_MM:.1f} x {END_H_MM:.1f} cm  (Buchumschlag fertig)
- **Datenformat:** {DATA_W_MM:.1f} x {DATA_H_MM:.1f} cm  (= Endformat + 3 mm Beschnitt rundum)
- **Buchruecken:** {SPINE_MM:.1f} mm  (Toleranz bis ±10 % = ±{SPINE_MM*0.1:.1f} mm)
- **Sicherheitsabstand:** mindestens {SAFE_MM:.0f} mm vom Endformat-Rand fuer wichtige Inhalte
- **Farbigkeit:** Umschlag 4/4-farbig (beidseitig CMYK)
- **Material:** Softcover mit Mattfolie

## Layout-Aufteilung (von links nach rechts im Datenformat)

| Bereich | Breite | Bemerkung |
|---|---|---|
| Beschnitt links | {BLEED_MM:.0f} mm | wird abgeschnitten |
| **Rueckseite** | {COVER_MM:.1f} mm | (= A5-Breite) |
| **Buchruecken** | {SPINE_MM:.1f} mm | zentriert, Toleranz ±{SPINE_MM*0.1:.1f} mm |
| **Vorderseite** | {COVER_MM:.1f} mm | (= A5-Breite) |
| Beschnitt rechts | {BLEED_MM:.0f} mm | wird abgeschnitten |
| **Summe** | **{DATA_W_MM:.0f} mm** | |

## Was die Template-PDF zeigt

`{os.path.basename(OUT_PDF)}` enthaelt **eine Seite im Datenformat** mit:
- **rot gestrichelt:** Endformat-Rahmen (Schnittkante)
- **gruen gestrichelt:** Sicherheitsrahmen (5 mm innen vom Endformat)
- **blauer Bereich:** Buchruecken inkl. Toleranzlinien
- **graue Trennlinien:** Aufteilung Rueckseite/Buchruecken/Vorderseite
- **rote Schnittmarken:** in den 4 Ecken
- **Beschriftungen** der Bereiche

Diese Hilfslinien sind nur Orientierung beim Gestalten. **Vor dem Hochladen
bei der Druckerei muessen sie geloescht werden** (oder du legst dein Design
in InDesign/Affinity Publisher auf einer separaten Ebene UEBER dem Template
ab und exportierst ohne Template-Layer).

## Checkliste vor Upload

- [ ] Datei-Format **{DATA_W_MM:.0f} x {DATA_H_MM:.0f} mm** (Datenformat)
- [ ] Wichtige Texte/Logos **mindestens {SAFE_MM:.0f} mm** vom Endformat-Rand
- [ ] Hintergrundgrafik bis in den Beschnitt-Bereich (3 mm) ausgedehnt, falls Vollflaechig
- [ ] Buchruecken-Beschriftung bleibt **mindestens 3 mm von der Toleranzkante** entfernt
- [ ] Farbprofil: CMYK (kein RGB), Schwarz als 100/0/0/0 K
- [ ] Schriften eingebettet oder in Pfade konvertiert
- [ ] PDF/X-3 oder PDF/X-4 Export (von der Druckerei empfohlen)
- [ ] Template-Hilfslinien entfernt
- [ ] Probedruck der Umschlag-Datei in 100 % auf A3 zur visuellen Pruefung

## Empfohlene Inhalte

### Vorderseite
- Haupttitel: "Verdeckte Begabungen bei fruehem Zweitspracherwerb"
- Untertitel: Masterpruefung Vertiefung 2026
- Autor*in: Inti Merolli
- PHLU-Logo (optional)

### Buchruecken
- Titel kurz + Autor*in (in Leserichtung von unten nach oben)
- Schriftgroesse ca. 9-11 pt

### Rueckseite
- Kurzfassung / Abstract
- Inhaltsangabe der Schwerpunkte
- Studiengang / Institution
- evtl. ISBN-Platzhalter

## Hinweise

- **2,8 cm Buchruecken**: ergibt sich aus 596 Seiten x 115 g Papier. Bei
  Aenderung der Seitenzahl oder Papierwahl muss der Buchruecken angepasst
  werden. **Vor Druckauftrag der Druckerei die Buchruecken-Staerke bestaetigen
  lassen** (mit konkreter Seitenzahl und Papierangabe).
- Bei Fadenheftung waere der Buchruecken 2,9 cm statt 2,8 cm.
"""
    with open(OUT_README, "w") as f:
        f.write(readme)

    print(f"Template:   {OUT_PDF}")
    print(f"Anleitung:  {OUT_README}")
    print(f"Datenformat: {DATA_W_MM:.0f} x {DATA_H_MM:.0f} mm (Buchruecken {SPINE_MM:.0f} mm)")


if __name__ == "__main__":
    main()
