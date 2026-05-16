# Workflow Quellenarbeit (verbindlich)

> **Stand:** 2026-05-16 · **Referenzfall:** `stamm2021fehlenderblick` (Vision-Audit Status 5)
> **Zweck:** Jede inhaltliche Behauptung im Lerndokument muss bis zum gedruckten Originalbild rückverfolgbar sein — und für eine Drittperson (oder mich in 6 Monaten) reproduzierbar.

Dieses Dokument ist der **verbindliche Standard** für jede neue Literaturquelle, die im Lerndokument oder in einem Vortrag inhaltlich verwendet wird. Abweichungen erfordern eine ausdrückliche Notiz im jeweiligen `verified_quotes.md`.

---

## 1 — Ordnerstruktur pro Quelle

Pro Bibkey ein eigener Ordner unter `Literatur/<bibkey>/` mit immer denselben Dateinamen:

```
Literatur/<bibkey>/
├── source.pdf              # komprimiertes Original (1400 px, JPEG-Q70)
├── pages/
│   ├── p01.jpg             # Bildseiten, gerendert (130 DPI Standard, JPEG-Q70)
│   ├── p02.jpg
│   └── ...
├── transcript.md           # Wortgetreues Volltext-Transkript (Pass-1 + Pass-2 verifiziert)
└── verified_quotes.md      # Kuratierte, zitierfähige Auszüge (Z01, Z02, …)
```

Diese Konvention ist Voraussetzung für die Skripte `integrate_transkripte.py` und `cite_context.py` und für das Audit-Status-Register `Literatur/_audit_status.md`.

---

## 2 — Sechs-Schritte-Workflow

### Schritt 1 — Bibliographische Verortung (→ Status 1–2)

- `Quellen.bib`-Eintrag prüfen (Autor, Jahr, Titel, Seiten, Verlag).
- Swisscovery-/DOI-Link in den Header von `verified_quotes.md` eintragen.
- Bei Sammelbänden: `_outline.md` konsultieren, um den Beitrag genau zu lokalisieren.

### Schritt 2 — Volltext beschaffen + komprimieren

> **Pflicht-Konvention** (siehe Memory `pdf_kompression`):
> Niemals unkomprimierte 20+ MB PDFs im Repo belassen.

1. Original-Bildscan-PDF lokalisieren (typisch: `MPV/Literatur/FehlendeSeiten MPV/…`).
2. Komprimieren mit dem Repo-Skript:
   ```bash
   python3 archiv/compress_pdfs.py <input.pdf> Literatur/<bibkey>/source.pdf 1400 70
   ```
   Standardparameter: **1400 px** Breite, **JPEG-Q70**. Typische Reduktion: 5–10×.
3. Originaldatei im Quellordner belassen, **nur die komprimierte Version** als `source.pdf` ins Repo.

### Schritt 3 — Seiten als Bildmaster rendern

PyMuPDF (`fitz`), 130 DPI, JPEG-Q70 als `pages/p01.jpg` … `pNN.jpg`.

```python
import fitz, io
from PIL import Image
doc = fitz.open("Literatur/<bibkey>/source.pdf")
mat = fitz.Matrix(130/72, 130/72)
for i, page in enumerate(doc, start=1):
    pix = page.get_pixmap(matrix=mat)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    img.save(f"Literatur/<bibkey>/pages/p{i:02d}.jpg",
             format="JPEG", quality=70, optimize=True)
```

Mapping PDF-Seite → Buchseite im `transcript.md`-Header dokumentieren (Tabelle).
Doppelseiten-Aufnahmen explizit als Cross-Check kennzeichnen.

### Schritt 4 — Pass 1: Transkription (→ Status 3)

- Für jede Buchseite das Bild **einmal** komplett lesen und wortgetreu in `transcript.md` übertragen.
- Kursivierungen mit `*…*`, deutsche Anführungszeichen erhalten (`„…"`, `»…«`).
- Zwischenüberschriften (`### x.y`), Absätze und Block-Zitate strukturiert übernehmen.
- **Unsichere Stellen sofort markieren**: `[?Wort1? / Wort2?]` — niemals raten.
- Pro Seite Header: `## S. NNN — Thema` plus Notiz „Pass 1 gelesen aus `pages/pNN.jpg` am DATUM".

### Schritt 5 — Pass 2: Verifikation (→ Status 4)

- Pro Seite **das Bild + die Transkript-Sektion parallel re-lesen** (Vision-Read + `read_file` mit `offset`/`limit`).
- Diskrepanzen in der Sektion `## Pass-2-Korrekturen — Protokoll` als Tabelle dokumentieren:
  | Seite | Master-Bild | Vergleich | Diskrepanz | Korrektur |
- Bei verbleibender Unsicherheit: **PDF-Re-Render mit 200–300 DPI** auf den kritischen Crop-Bereich (PyMuPDF + `Image.crop`), Auflösung dokumentieren.
- Header-Status hochsetzen auf „Pass 2 abgeschlossen am DATUM · verifiziert ≥ 99.9 %".

### Schritt 6 — Verified Quotes (→ Status 5)

- Aus `transcript.md` die zitierfähigen Stellen herauslösen und nach `verified_quotes.md` übertragen.
- Format: `Z01`, `Z02`, … mit Kurzbeschreibung + Seitenangabe + (optional) Vortragsbezug (z. B. „★ Stein 2").
- Jedes Z muss **wörtlich** aus `transcript.md` kopiert sein — keine eigene Umformulierung.
- Audit-Header: „Status 5 (Volltext sichtgelesen, wortgetreue Zitate verifiziert), Verifiziert am DATUM, Bearbeitet durch Cascade-Vision-Audit / Inti".
- **Korrekturen gegenüber früheren Ableitungen explizit markieren** (Beispiel: „Heid statt Heydorn" als Footer-Notiz in `verified_quotes.md`).

---

## 3 — Audit-Status-Hierarchie (verbindlich)

| Status | Bedeutung | Was darf zitiert werden |
|---|---|---|
| **1** | Bibkey nur in `Quellen.bib` | Bibliographie, keine Inhaltsthesen |
| **2** | Bibliographisch verortet (Outline, Swisscovery, Verlag) | Allgemeine Themenzuordnung |
| **3** | Sammelband-/Drittes-Transkript geprüft | Kapitelspanne, Paraphrase |
| **4** | Eigene Volltext-Transkription (Pass 1) | Inhaltsthesen mit Seitenangabe |
| **5** | Pass 2 verifiziert, wortgetreue Zitate | **Wörtliche Zitate** mit Seitengenauigkeit |

**Verwendungsregeln im Lerndokument:**
- `\parencite[S.\,…]{bibkey}` mit Seitenangabe → ab **Status 4**
- `\enquote{…}` (wörtliches Zitat) → ausschliesslich ab **Status 5**
- `\textcite{bibkey}` ohne Seitenangabe → ab Status 2 (Paraphrase nur grobthematisch)

---

## 4 — Goldene Regeln (nicht verhandelbar)

- **Nie raten.** Lieber `[?…?]` markieren und in Pass 2 mit Re-Render lösen.
- **Single Source of Truth.** `transcript.md` ist verbindlich — `verified_quotes.md` kopiert wörtlich daraus.
- **Datum + Methodik im Header.** Jedes Dokument muss erkennen lassen, *wann* und *wie* es geprüft wurde.
- **Korrekturen sind sichtbar.** Wenn etwas früher falsch war (Heydorn-/Heid-Fall), wird das explizit als Korrektur-Notiz dokumentiert, nicht stillschweigend überschrieben.
- **Volltext-Audit nur einmal pro Quelle.** Danach gilt das Transkript — abgeleitete Dokumente werden gegen das Transkript geprüft, nicht gegen das PDF.
- **PDF-Kompression ist Pflicht.** Nie unkomprimierte 20+ MB PDFs im Repo. Standard: 1400 px / JPEG-Q70.
- **Bildrendering immer JPEG (Q70–75), nie PNG.** PNG nur für Vektor-Diagramme.
- **Nach Verifikation grosse Zwischendateien löschen** (z. B. hochauflösende Re-Render-PNG/JPEG aus `/tmp/`).

---

## 5 — Abgeleitete Dokumente nachziehen (Reihenfolge)

Wenn `verified_quotes.md` eine Korrektur erzwingt, **müssen folgende Stellen synchron nachgezogen werden** — und zwar in dieser Reihenfolge:

1. `Literatur/<bibkey>/transcript.md` (Master)
2. `Literatur/<bibkey>/verified_quotes.md` (Z-Liste mit Korrektur-Footer)
3. `Literatur/_audit_status.md` (Status-Eintrag aktualisieren)
4. `mpv.tex` / `mpv_abgabedokument.tex` (LaTeX-Source)
5. `VISUALISIERUNG/Vortrag*_geschaerft.md` (Sprechtext-Steine)
6. `VISUALISIERUNG/Vortrag*_Quellenkanon.md` (Quellenliste je Vortrag)
7. `VISUALISIERUNG/Frage*.md` (Detailbegründung)

**Niemals umgekehrt.** Wer im Vortragstext Quellen ändert, ohne den Master zu aktualisieren, schafft Inkonsistenzen.

---

## 6 — Anwendungs-Checkliste (Copy/Paste pro neuer Quelle)

```
[ ] 1. Quellen.bib-Eintrag geprüft, Swisscovery-Link notiert
[ ] 2. Original-PDF beschafft, mit archiv/compress_pdfs.py komprimiert,
       als Literatur/<bibkey>/source.pdf abgelegt
[ ] 3. PyMuPDF-Render: pages/p01.jpg … pNN.jpg (130 DPI, JPEG-Q70)
[ ] 4. Pass 1: transcript.md komplett wortgetreu, Unsicherheiten markiert
[ ] 5. Pass 2: Bild + Transkript-Section parallel re-lesen,
       Pass-2-Korrekturen-Protokoll vollständig
[ ] 6. verified_quotes.md: Z01…ZNN, jedes Zitat wörtlich aus transcript.md
[ ] 7. Literatur/_audit_status.md: Status auf 5, Datum eintragen
[ ] 8. Falls Korrekturen: abgeleitete Dokumente nachziehen (Reihenfolge §5)
[ ] 9. Grosse Zwischendateien gelöscht (Re-Render-Crops, /tmp/-Outputs)
```

---

## 7 — Referenzen

- **Best-Practice-Beispiel:** `Literatur/stamm2021fehlenderblick/` (Status 5, vollständig nach diesem Workflow durchgeführt)
- **Komprimierungs-Skript:** `archiv/compress_pdfs.py`
- **CLI-Wrapper:** `Visualisierung/.cache/druck/compress_druck_pdf.py`
- **Audit-Register:** `Literatur/_audit_status.md`
- **Kernliteratur-Inventar:** `Visualisierung/.cache/druck/kernliteratur_inventar.md`
