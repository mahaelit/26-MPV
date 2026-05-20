


















# Onboarding-Briefing: Quellenarbeit im Repo [26-MPV](cci:9://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV:0:0-0:0)

> **Adressat:** ein neuer Agent (oder ein anderes Modell), das im Repo Literatur belegen, prüfen oder absichern soll.
> **Pfad-Konvention:** Alle Pfade unten sind relativ zu [/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV/26-MPV/](cci:9://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV:0:0-0:0).

---

## 0. TL;DR — Was du in 60 Sekunden wissen musst

1. **Single Source of Truth** für jede Behauptung ist `Literatur/<bibkey>/verified_quotes.md`. Wenn dort ein Zitat als **Status 5** markiert ist, kannst du es wörtlich zitieren. Sonst nicht.
2. **Status-Skala 1–5** entscheidet, was du in `\parencite{}` und `\enquote{}` schreiben darfst — die Hierarchie steht in [docs/workflow_quellenarbeit.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/docs/workflow_quellenarbeit.md:0:0-0:0) und in [Literatur/_audit_status.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/_audit_status.md:0:0-0:0).
3. **Zentrale Karte:** [Literatur/_audit_status.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/_audit_status.md:0:0-0:0) zeigt dir pro Vortrag (V1–V5) und pro Bibkey den aktuellen Verifikationsstand (PDF da? transcript da? verified_quotes da? Status-Stufe?).
4. **Geh immer zur Quelle zurück.** Wenn du etwas neu zitierst oder nachprüfst: Volltext (PDF / transcript.md) ansehen, nicht Memos / Vortragsdokumente.
5. **[Quellen.bib](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Quellen.bib:0:0-0:0) ist die Bib-Datenbank** — alle Bibkeys, korrekte Seitenangaben, Zählung pro Frage in den `annotation`-Feldern.

---

## 1. Repo-Topologie der Quellenarbeit

```
26-MPV/
├── Quellen.bib                              # ← Bib-DB (alle Schlüssel, Seiten, Annotationen pro Frage)
├── mpv.tex                                  # Lerndokument (lang)
├── mpv_abgabedokument.tex                   # Abgabedokument (kurz)
├── docs/
│   └── workflow_quellenarbeit.md            # ← VERBINDLICHER 6-Schritte-Workflow
├── Literatur/
│   ├── _INDEX.md                            # Auto-generiert: Statusübersicht 94 Bibkeys
│   ├── _audit_status.md                     # ← ZENTRALE Karte je Vortrag + je Bibkey
│   ├── _briefing_inti.md                    # Briefing für Inti (Userin)
│   ├── _handover.md                         # Workflow-Handover für nächsten Agenten
│   ├── _transkripte_index.json              # Bibkey → Transkripte-Mapping
│   └── <bibkey>/
│       ├── source.pdf                       # komprimiertes Original (1400 px / JPEG-Q70)
│       ├── pages/p01.jpg … pNN.jpg          # gerenderte Bildseiten (130 DPI)
│       ├── transcript.md                    # wortgetreues Volltext-Transkript
│       ├── verified_quotes.md               # ← zitierfähige Z-Liste (Z01, Z02 …)
│       └── excerpts/                        # ggf. Kapitel-Splits aus Sammelband
└── archiv/                                  # Helper-Scripts (Python)
    ├── compress_pdfs.py                     # PDF-Foto-Scans schrumpfen
    ├── pdf_extract.py                       # seitengenaue Textextraktion + Suche
    ├── extract_excerpts.py                  # Sammelband nach Outline splitten
    ├── verify_excerpts.py                   # Splits gegen Outline prüfen
    ├── cite_context.py                      # Cite-Stellen aus .tex in verified_quotes.md
    ├── integrate_transkripte.py             # Transkript-Mapping in verified_quotes.md
    ├── analyze_transkripte.py               # baut _transkripte_index.json
    ├── build_index.py                       # erzeugt _INDEX.md
    ├── match_external_pdfs.py               # OneDrive-Externalia ↔ Repo abgleichen
    └── compress_pdfs.py                     # JPEG-Q70-Kompression
```

---

## 2. Die Status-Hierarchie (Pflichtwissen)

| Status | Bedeutung                                                                                                                                                                             | Was darf zitiert werden                                                   |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| **1**  | NO_LOCAL — Bibkey nur in [Quellen.bib](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Quellen.bib:0:0-0:0) | nur Bibliographie, **keine** Inhaltsthese                                 |
| **2**  | bibliographisch verortet (Outline / Verlag)                                                                                                                                           | `\textcite{}` ohne Seitenangabe (grobthematisch)                          |
| **3**  | Sammelband-/Drittes-Transkript geprüft                                                                                                                                                | Paraphrase mit Kapitelspanne                                              |
| **4**  | Eigene Volltext-Transkription (Pass 1)                                                                                                                                                | `\parencite[S.\,N]{}` mit Seitenangabe                                    |
| **5**  | Pass 2 verifiziert, wortgetreue Zitate                                                                                                                                                | `\enquote{…}` wörtlich, Status 5 ist die einzige Stufe für direkte Zitate |

**Verbindliche Verwendungsregeln:**
- `\parencite[S.\,…]{bibkey}` → ab Status **4**
- `\enquote{…}` → ausschliesslich ab Status **5**
- `\textcite{bibkey}` ohne Seitenangabe → ab Status **2**

Die Skala kommt aus `@/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV/26-MPV/docs/workflow_quellenarbeit.md:97-108`.

---

## 3. Die zwei wichtigsten Dateien für jede Sitzung

### 3.1 [Literatur/_audit_status.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/_audit_status.md:0:0-0:0)

Ist die **Karte**, mit der du anfängst. Sie enthält:

- **Statusregister je Vortrag (V1–V5)** mit pro Bibkey: Seitenspanne, ob [source.pdf](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/macha2019gender/source.pdf:0:0-0:0) da ist, ob [transcript.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/muelleroppliger2021paeddiagnostik/transcript.md:0:0-0:0) da ist, ob [verified_quotes.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/dvs2025bbf/verified_quotes.md:0:0-0:0) mit Z01–ZNN existiert, aktueller Status (1–5), Audit-Datum.
- **Aktuelle Bilanz** (z. B. Stand 2026-05-17: 15 Bibkeys auf Status 5, 9 auf Status 3, 21 auf Status 2, 5 NO_LOCAL).
- **Audit-Befunde-Liste** mit zentralen Korrekturen (z. B. *Evers 2025: Hippocampus → Amygdala in [mpv.tex](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/mpv.tex:0:0-0:0) Z. 4775–4781 korrigiert*).

**Beim Start einer Audit-Session immer als Erstes lesen.**

### 3.2 `Literatur/<bibkey>/verified_quotes.md`

Pro Quelle. Drei Sektionen, durch HTML-Marker getrennt:

```markdown
# Verifizierte Zitate – <bibkey>
**Quelle:** Autor (Jahr). Titel. In: …
**Swisscovery/Verifikationslink:** …

<!-- CLAIMS-START (automatisch durch cite_context.py erzeugt; nicht manuell editieren) -->
## Zu verifizierende Behauptungen (aus TeX)
1. **[L:586]** … `\textcite[S.\,576--585]{stamm2021fehlenderblick}` …
2. **[A:164]** … `\parencite{erzinger2023pisa}` …
<!-- CLAIMS-END -->

<!-- TRANSKRIPTE-START (automatisch durch integrate_transkripte.py erzeugt; nicht manuell editieren) -->
## Transkript-Verortungen
…
<!-- TRANSKRIPTE-END -->

## Zitate (gegen die Quelle gegengeprueft)
### Zitat Z01 (S. 160)
> „Das Thema gender- und diversitätssensible Begabungsförderung …" (S. 160)
**Kontext / Paraphrase:** …
**Verwendet in:** mpv.tex Z. 2280, …
**Status:** 5 — verifiziert am 2026-05-16
```

**Drei Bereiche, drei Regeln:**
- **CLAIMS-Block:** auto-generiert von [cite_context.py](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/archiv/cite_context.py:0:0-0:0). Listet **alle** Cite-Stellen in [mpv.tex](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/mpv.tex:0:0-0:0) (Marker `[L:…]`) und [mpv_abgabedokument.tex](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/mpv_abgabedokument.tex:0:0-0:0) (`[A:…]`) mit Zeilennummer und Kontext. **Niemals von Hand editieren.**
- **TRANSKRIPTE-Block:** auto-generiert von [integrate_transkripte.py](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/archiv/integrate_transkripte.py:0:0-0:0) aus [_transkripte_index.json](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/_transkripte_index.json:0:0-0:0). Verweist auf Sammelband-Excerpts. **Niemals von Hand editieren.**
- **Z-Liste unten:** das ist der **Mensch-kuratierte** Bereich. Z01, Z02, … sind wortgetreue Zitate mit Locator + Verwendungsstellen + Status. Hier passiert die eigentliche Verifikationsarbeit.

---

## 4. Werkzeuge — was du benutzt, um Quellen zu prüfen

### 4.1 Cascade-Tools (deine Hauptwerkzeuge)

| Tool                                                 | Wann verwenden                                                                                                                                                                                                                                                                                                                                                                                              | Beispiel                                                                                                                                                                                                             |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `read_file`                                          | wenn Pfad bekannt — Volltext-PDF-Transkripte, [verified_quotes.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/dvs2025bbf/verified_quotes.md:0:0-0:0), [mpv.tex](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/mpv.tex:0:0-0:0)-Stellen | Z. 4670–4838 in [mpv.tex](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/mpv.tex:0:0-0:0) lesen                                           |
| `grep_search` (FixedStrings=true bei Spezialzeichen) | Cite-Stellen finden, Wortlaut suchen                                                                                                                                                                                                                                                                                                                                                                        | `\\textcite\\{baudson2025`, „Marburger Hochbegabten"                                                                                                                                                                 |
| `find_by_name`                                       | PDFs / Ordner lokalisieren                                                                                                                                                                                                                                                                                                                                                                                  | Pattern [verified_quotes.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/dvs2025bbf/verified_quotes.md:0:0-0:0), Type `file` |
| `list_dir`                                           | Ordnerinhalt einer Quelle                                                                                                                                                                                                                                                                                                                                                                                   | [Literatur/macha2019gender/](cci:9://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/macha2019gender:0:0-0:0)                            |
| `code_search`                                        | breite, semantische Suche im Repo                                                                                                                                                                                                                                                                                                                                                                           | „wo wird die SHP-Trias begründet?"                                                                                                                                                                                   |
| `run_command`                                        | Bib-Einträge mit awk extrahieren, biber/lualatex laufen lassen, PDF-Hash prüfen                                                                                                                                                                                                                                                                                                                             | `awk` über [Quellen.bib](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Quellen.bib:0:0-0:0)                                              |
| `read_url_content`                                   | Open-Access-Verlagsseiten / DOI für Verifikation                                                                                                                                                                                                                                                                                                                                                            | pedocs, Karg-Stiftung, Beltz                                                                                                                                                                                         |

### 4.2 Python-Skripte (Repo-Tooling, in [archiv/](cci:9://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/archiv:0:0-0:0))

| Skript                                                                                                                                                                                            | Zweck                                                                                                                                                                                                                                   | Aufruf                                                                                 |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| **[compress_pdfs.py](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/archiv/compress_pdfs.py:0:0-0:0)**                 | Foto-Scans (20–60 MB) → 1400 px / JPEG-Q70 (Faktor 5–10×)                                                                                                                                                                               | `python3 archiv/compress_pdfs.py <input.pdf> Literatur/<bibkey>/source.pdf 1400 70`    |
| **[pdf_extract.py](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/archiv/pdf_extract.py:0:0-0:0)**                     | Seitengenaue Textextraktion + Phrasen-Suche, drei Engines (Poppler/pypdf/EPUB)                                                                                                                                                          | `python3 archiv/pdf_extract.py <bibkey> --page 42` oder `--search "Begabungsreserven"` |
| **[extract_excerpts.py](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/archiv/extract_excerpts.py:0:0-0:0)**           | Sammelband nach Bookmark-Outline splitten                                                                                                                                                                                               | `python3 archiv/extract_excerpts.py --key muelleroppliger2021handbuch`                 |
| **[verify_excerpts.py](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/archiv/verify_excerpts.py:0:0-0:0)**             | Splits gegen [_outline.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/macha2019gender/excerpts/_outline.md:0:0-0:0) validieren                 | `python3 archiv/verify_excerpts.py --key <bibkey>`                                     |
| **[cite_context.py](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/archiv/cite_context.py:0:0-0:0)**                   | Aktualisiert CLAIMS-Block in allen [verified_quotes.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/dvs2025bbf/verified_quotes.md:0:0-0:0)      | `python3 archiv/cite_context.py`                                                       |
| **[integrate_transkripte.py](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/archiv/integrate_transkripte.py:0:0-0:0)** | Aktualisiert TRANSKRIPTE-Block in allen [verified_quotes.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/dvs2025bbf/verified_quotes.md:0:0-0:0) | `python3 archiv/integrate_transkripte.py`                                              |
| **[build_index.py](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/archiv/build_index.py:0:0-0:0)**                     | Aktualisiert [Literatur/_INDEX.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/_INDEX.md:0:0-0:0) (Statusübersicht 94 Bibkeys)                  | `python3 archiv/build_index.py`                                                        |
| **[match_external_pdfs.py](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/archiv/match_external_pdfs.py:0:0-0:0)**     | Findet PDFs im OneDrive-Parent-Ordner und ordnet sie Bibkeys zu (Dry-Run by default)                                                                                                                                                    | `python3 archiv/match_external_pdfs.py --apply`                                        |

### 4.3 PyMuPDF-Render-Pattern (im Workflow §3)

Wenn [pdf_extract.py](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/archiv/pdf_extract.py:0:0-0:0) keinen Text-Layer findet (Foto-Scan), rendere die Seiten als JPEG für Vision-Inspektion:

```python
import fitz, io
from PIL import Image
doc = fitz.open("Literatur/<bibkey>/source.pdf")
mat = fitz.Matrix(130/72, 130/72)        # 130 DPI
for i, page in enumerate(doc, start=1):
    pix = page.get_pixmap(matrix=mat)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    img.save(f"Literatur/<bibkey>/pages/p{i:02d}.jpg",
             format="JPEG", quality=70, optimize=True)
```

---

## 5. Der 6-Schritte-Workflow (verbindlich)

Quelle: `@/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV/26-MPV/docs/workflow_quellenarbeit.md:29-92`.

| Schritt                                   | Was du tust                                                                                                                                                                                                                                                                                                                                                                                                                | Ergebnis                                                                                                                                                                                                            | Status danach |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| **1. Bibliographische Verortung**         | [Quellen.bib](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Quellen.bib:0:0-0:0) prüfen (Autor/Jahr/Seiten/Verlag), Swisscovery-Link in [verified_quotes.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/dvs2025bbf/verified_quotes.md:0:0-0:0)-Header | Header ausgefüllt                                                                                                                                                                                                   | 1–2           |
| **2. Volltext beschaffen + komprimieren** | Original-PDF lokalisieren, mit [compress_pdfs.py](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/archiv/compress_pdfs.py:0:0-0:0) schrumpfen, als [source.pdf](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/macha2019gender/source.pdf:0:0-0:0) ablegen  | `Literatur/<bibkey>/source.pdf`                                                                                                                                                                                     | 2             |
| **3. Bildmaster rendern**                 | PyMuPDF → `pages/p01.jpg` … `pNN.jpg` (130 DPI / JPEG-Q70)                                                                                                                                                                                                                                                                                                                                                                 | `pages/*.jpg`                                                                                                                                                                                                       | 2             |
| **4. Pass 1 — Transkription**             | Jede Buchseite einmal komplett wortgetreu in [transcript.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/muelleroppliger2021paeddiagnostik/transcript.md:0:0-0:0) übertragen, Unsicherheiten als `[?Wort?]` markieren                                                                                                              | [transcript.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/muelleroppliger2021paeddiagnostik/transcript.md:0:0-0:0) Pass 1 | 3             |
| **5. Pass 2 — Verifikation**              | Bild + Transkript-Section parallel re-lesen, Diskrepanzen in „Pass-2-Korrekturen-Protokoll"-Tabelle dokumentieren                                                                                                                                                                                                                                                                                                          | Header „Pass 2 abgeschlossen am DATUM, ≥ 99.9 % verifiziert"                                                                                                                                                        | 4             |
| **6. Verified Quotes**                    | Z01…ZNN aus [transcript.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/muelleroppliger2021paeddiagnostik/transcript.md:0:0-0:0) herauslösen, Locator + Verwendungsstelle + Status 5 dokumentieren                                                                                                                                 | [verified_quotes.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/dvs2025bbf/verified_quotes.md:0:0-0:0) Z-Liste             | 5             |

**Wichtig:** ab Schritt 6 ist die Quelle zitierfähig. Vorher nicht.

---

## 6. Goldene Regeln (nicht verhandelbar)

Aus `@/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV/26-MPV/docs/workflow_quellenarbeit.md:112-122`:

1. **Nie raten.** Lieber `[?Wort1?/Wort2?]` markieren und in Pass 2 mit Re-Render lösen.
2. **Single Source of Truth.** [transcript.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/muelleroppliger2021paeddiagnostik/transcript.md:0:0-0:0) ist verbindlich — [verified_quotes.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/dvs2025bbf/verified_quotes.md:0:0-0:0) kopiert wortwörtlich daraus.
3. **Datum + Methodik im Header.** Jedes Audit-Dokument muss erkennen lassen, wann + wie geprüft wurde.
4. **Korrekturen sind sichtbar.** Kein stillschweigendes Überschreiben — alte Fehler als Korrektur-Notiz im Footer (Beispiel: *„Heid statt Heydorn"* in [verified_quotes.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/dvs2025bbf/verified_quotes.md:0:0-0:0)).
5. **Volltext-Audit nur einmal pro Quelle.** Danach gilt das Transkript — abgeleitete Dokumente ([mpv.tex](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/mpv.tex:0:0-0:0), Vortragsdokumente) werden gegen das Transkript geprüft, nicht gegen das PDF.
6. **PDF-Kompression ist Pflicht.** Nie unkomprimierte 20+ MB PDFs im Repo. Standard: 1400 px / JPEG-Q70.
7. **Bildrendering immer JPEG (Q70–75), nie PNG.** PNG nur für Vektor-Diagramme.
8. **Nach Verifikation grosse Zwischendateien löschen** (z. B. hochauflösende Re-Render-Crops aus [/tmp/](cci:9://file:///tmp:0:0-0:0)).

---

## 7. Häufige Aufgaben — Rezepte

### Rezept A: „Stimmt der Locator `\parencite[S.\,X]{bibkey}` in [mpv.tex](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/mpv.tex:0:0-0:0)?"

```
1. read_file Literatur/<bibkey>/verified_quotes.md
   → Status-Stufe + Z-Liste prüfen
2. Wenn Status ≥ 4: Z-Liste auf S. X durchsuchen
   → Wenn Treffer wortgetreu: Locator OK
   → Wenn Off-by-N: in mpv.tex korrigieren + Audit-Befund in _audit_status.md
3. Wenn Status < 4: Workflow-Schritte 4–6 durchführen
```

### Rezept B: „Ich brauche eine wörtliche Stütze für Behauptung X"

```
1. grep_search "X" über Literatur/*/verified_quotes.md
2. Treffer in Z-Listen → Status 5 prüfen → wortgetreuer Locator
3. Falls kein Status-5-Treffer: code_search über Literatur/*/transcript.md
4. Falls auch dort nichts: pdf_extract.py --search "X" über Kandidaten-Bibkey
5. Letzte Eskalation: Foto-Scan rendern + Vision lesen
```

### Rezept C: „Neue Quelle ist eingetroffen — onboarden!"

```
1. Quellen.bib um Bibkey ergänzen (Autor, Jahr, Titel, Pages, ISBN/DOI)
2. Ordner Literatur/<bibkey>/ anlegen
3. compress_pdfs.py: Original → source.pdf
4. PyMuPDF-Render → pages/*.jpg (nur wenn Foto-Scan, sonst überspringen)
5. transcript.md: Pass 1 schreiben
6. transcript.md: Pass 2 verifizieren
7. verified_quotes.md: Header + Z-Liste
8. cite_context.py + integrate_transkripte.py + build_index.py laufen lassen
9. _audit_status.md: neuen Eintrag (Vortrag-Tabelle + Status 5)
10. mpv.tex: ggf. \parencite[]{} einbauen, danach LaTeX rebuilden
```

### Rezept D: „LaTeX-Build bricht wegen undefinierter Citation ab"

```
1. grep_search im .tex auf den unbekannten Bibkey
2. awk auf Quellen.bib: existiert der Bibkey?
   → wenn nein: Bibkey-Tippfehler oder fehlender Bib-Eintrag
   → wenn ja: biber wurde nicht neu gerunnt
3. Build-Reihenfolge:
   lualatex mpv.tex          (regeneriert .bcf)
   biber mpv                 (.bbl aus Quellen.bib)
   lualatex mpv.tex          (Citations auflösen)
   lualatex mpv.tex          (Page-Refs settlen)
```

(Diese Reihenfolge ist nötig, weil [mpv.tex](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/mpv.tex:0:0-0:0) `fontspec` nutzt → muss mit `lualatex` oder `xelatex` gebaut werden, nicht `pdflatex`.)

---

## 8. Bekannte Fallen — Lessons Learned

Aus `@/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV/26-MPV/Literatur/_handover.md:64-71` und `_briefing_inti.md:104-108`:

1. **Audio-Transkripte sind nicht zitierfähig.** Hörfehler bei Eigennamen („Renzoli" statt „Renzulli", „Stachoviak" statt „Stachowiak"). Verwende sie nur als Themen-Übersicht.
2. **OCR-Fehler bei Foto-Scans.** Vision-Verifikation am Bild ist immer der Goldstandard, nicht OCR-Text.
3. **Off-by-N-Locator.** Sammelband-Beiträge enden oft auf einer Seite, deren letzter Inhalt schon Literaturverzeichnis ist. *Wagner 2021* hatte 4 Locator auf S. 425 — der Beitrag endet aber inhaltlich auf S. 424.
4. **Author-Tippfehler in Bib.** Beispiel *Wagner ≠ Wagener*. Korrekt: Bib-Author korrigieren, Bibkey aus Konsistenzgründen behalten.
5. **Folder-Naming-Drift.** Beispiel: Bibkey `kuhl2021begabungbildungbeziehung`, Ordner [Kuhl2021bildungbegabung](cci:9://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/Kuhl2021bildungbegabung:0:0-0:0). Bei `find_by_name` nötigenfalls Glob-Pattern nutzen.
6. **Inline-Cite vs. Sammel-Cite.** Wenn ein Beitrag im Sammelband zitiert wird, **immer** `[S.\,X--Y]` davor. Sammel-Cites ohne Seitenangabe sind heuristisch schwer prüfbar (siehe [muelleroppliger2021handbuch](cci:9://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/muelleroppliger2021handbuch:0:0-0:0) mit 14 Cite-Stellen ohne klare Locator).
7. **`@book` ≠ `@incollection`.** Sammelband-Hülse vs. einzelner Beitrag konsequent unterscheiden. Beispiel: [muelleroppliger2021handbuch](cci:9://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/muelleroppliger2021handbuch:0:0-0:0) (gesamter Beltz-Sammelband) ≠ [muelleroppliger2021begabungsmodelle](cci:9://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/muelleroppliger2021begabungsmodelle:0:0-0:0) (Beitrag S. 204–219).
8. **Frühere Audit-Notizen sind nicht selbst-verifizierend.** Die Hippocampus-Falschattribution bei [evers2025stress](cci:9://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/evers2025stress:0:0-0:0) blieb trotz Notiz vom 28.04. stehen, weil die Notiz selbst falsch war („bereits entfernt" — war es nicht). **Jede frühere Notiz gegen Quelle re-prüfen.**

---

## 9. Wo wird welche Information gepflegt? (Reihenfolge bei Korrekturen)

Aus `@/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV/26-MPV/docs/workflow_quellenarbeit.md:127-137`:

Wenn eine Korrektur in einer Quelle erforderlich ist, müssen folgende Stellen **synchron in dieser Reihenfolge** nachgezogen werden:

1. `Literatur/<bibkey>/transcript.md` (Master)
2. `Literatur/<bibkey>/verified_quotes.md` (Z-Liste mit Korrektur-Footer)
3. [Literatur/_audit_status.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/_audit_status.md:0:0-0:0) (Status-Eintrag aktualisieren)
4. [mpv.tex](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/mpv.tex:0:0-0:0) und/oder [mpv_abgabedokument.tex](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/mpv_abgabedokument.tex:0:0-0:0)
5. `VISUALISIERUNG/Vortrag*_geschaerft.md` (Sprechtext-Steine)
6. `VISUALISIERUNG/Vortrag*_Quellenkanon.md` (Quellenliste je Vortrag)
7. `VISUALISIERUNG/Frage*.md` (Detailbegründung)

**Niemals umgekehrt.** Wer im Vortragstext Quellen ändert, ohne den Master zu aktualisieren, schafft Inkonsistenzen.

---

## 10. Quick-Reference: Wo schlage ich was nach?

| Frage                                                                                                                                                                                   | Datei                                                                                                                                                                                                                                                                                                                                                     |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Was ist der Verifikationsstand pro Quelle?**                                                                                                                                          | [Literatur/_audit_status.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/_audit_status.md:0:0-0:0)                                                                                                                                                                |
| **Wie sieht ein perfekter Audit aus?**                                                                                                                                                  | `Literatur/stamm2021fehlenderblick/verified_quotes.md` (Status 5, vollständig)                                                                                                                                                                                                                                                                            |
| **Welche Bibkeys hat das Repo überhaupt?**                                                                                                                                              | [Literatur/_INDEX.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/_INDEX.md:0:0-0:0) (auto-gen) oder [Quellen.bib](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Quellen.bib:0:0-0:0) |
| **Wo wird ein Bibkey in [mpv.tex](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/mpv.tex:0:0-0:0) zitiert?** | CLAIMS-Block in `Literatur/<bibkey>/verified_quotes.md`                                                                                                                                                                                                                                                                                                   |
| **Welche Sammelband-Transkripte gibt es?**                                                                                                                                              | [Literatur/_transkripte_index.json](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/_transkripte_index.json:0:0-0:0)                                                                                                                                                  |
| **Welcher Verlag / DOI für Bibkey X?**                                                                                                                                                  | [Quellen.bib](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Quellen.bib:0:0-0:0)-Eintrag (mit `annotation`-Feld)                                                                                                                                                              |
| **Wie ist der verbindliche Workflow?**                                                                                                                                                  | [docs/workflow_quellenarbeit.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/docs/workflow_quellenarbeit.md:0:0-0:0)                                                                                                                                                        |
| **Wie kommuniziere ich mit der Userin?**                                                                                                                                                | [Literatur/_briefing_inti.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/_briefing_inti.md:0:0-0:0) (das ist Inti's Briefing, nicht deins, aber zeigt den erwarteten Stil)                                                                                       |
| **Was ist der nächste Audit-Auftrag?**                                                                                                                                                  | [Literatur/_handover.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/_handover.md:0:0-0:0) § 5 (Wiederaufsatzpunkt) und § 4-Pendings                                                                                                                              |

---

## 11. Konkretes Beispiel — wie du mit einer Behauptung umgehst

**Situation:** Inti behauptet im Vortrag, *„Lehrkräfte erkennen Hochbegabte nur dann, wenn ihre Leistungen erwartungsgemäss ausfallen — hochbegabte Underachiever fallen durchs Raster"*. Du sollst das belegen.

```
Schritt 1 — Karte konsultieren
  read_file Literatur/_audit_status.md
  → Vortrag 5 - Tabelle:
    | baudson2025besserfinden | 35–40 | ✓ in pauly2025 | … | ✓ Z01–Z04 | 5 | 2026-05-16 |

Schritt 2 — Verified Quotes lesen
  read_file Literatur/pauly2025wasistfair/verified_quotes.md
  → suche „Marburger Hochbegabten"
  → finde Z02 mit wortgetreuem Zitat von S. 36-37

Schritt 3 — Locator absichern
  grep_search "baudson2025besserfinden" über mpv.tex
  → prüfe: ist Locator [S.\,36--37] korrekt? (er ist es)

Schritt 4 — Antwort an Userin formulieren
  „Beleg: Baudson 2025, S. 36–37, Status 5, in Z02 von
  Literatur/pauly2025wasistfair/verified_quotes.md wortgetreu hinterlegt."
```

Wenn an irgendeinem Punkt etwas Ungereimtes auftaucht (Status-Mismatch, Locator-Drift, fehlendes verified_quotes.md), **gehst du immer zur Quelle zurück** (PDF / transcript.md), nicht zu Sekundär-Memos.

---

## 12. Was du nicht tun darfst

- **Nicht** Quotes aus Sekundärliteratur als Direktzitate ausgeben (z. B. Borland 2005 → in Wahrheit zitiert Müller-Oppliger 2021 S. 219 ihn).
- **Nicht** Status-5-Verifikation behaupten, ohne [verified_quotes.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/dvs2025bbf/verified_quotes.md:0:0-0:0) mit Z-Liste zu haben.
- **Nicht** den CLAIMS-Block oder TRANSKRIPTE-Block manuell editieren — die werden auto-regeneriert.
- **Nicht** ungeprüft auf Vortragstexten / Memos / Plakat-Beschreibungen aufbauen — die spiegeln einen früheren Stand und können durch nachträgliche Audits überholt sein.
- **Nicht** unkomprimierte PDFs (>20 MB) ins Repo committen.
- **Nicht** Korrekturen still überschreiben — Korrektur-Notizen mit Datum + Begründung sind Pflicht.

---

## 13. Wenn du nicht weiterkommst

| Symptom                                                                                                                                                                                                               | Vorgehen                                                                                                                                                                                                                                                                                                                                                                                                                         |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Bibkey existiert in Bib, aber kein Ordner unter [Literatur/](cci:9://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur:0:0-0:0)             | Status 1 (NO_LOCAL) — Userin kontaktieren oder OA-Beschaffung versuchen (pedocs, Karg-Stiftung, Beltz, Pauly-Sammelband)                                                                                                                                                                                                                                                                                                         |
| [verified_quotes.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/dvs2025bbf/verified_quotes.md:0:0-0:0) ist leer / nur Header | Status 1–2 — Workflow Schritt 1 starten oder Userin um PDF bitten                                                                                                                                                                                                                                                                                                                                                                |
| Locator stimmt nicht mit Inhalt überein                                                                                                                                                                               | Off-by-N-Falle — Workflow Schritt 5 (Pass 2) re-prüfen, dann [mpv.tex](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/mpv.tex:0:0-0:0) korrigieren + Audit-Befund in [_audit_status.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/_audit_status.md:0:0-0:0) |
| Mehrere Locator widersprechen sich (z. B. `S. 576-580` vs. `S. 576-585`)                                                                                                                                              | Auf vollständige Kapitelspanne vereinheitlichen, Begründung in [verified_quotes.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/dvs2025bbf/verified_quotes.md:0:0-0:0)                                                                                                                                                                   |
| Foto-Scan ohne Text-Layer                                                                                                                                                                                             | Vision-Inspektion am Bild (`pages/pNN.jpg`), nicht OCR vertrauen                                                                                                                                                                                                                                                                                                                                                                 |
| Du findest die Quelle nicht im Bib                                                                                                                                                                                    | `code_search "<Autor> <Jahr>"` über das ganze Repo — möglicherweise alter Bibkey, der umbenannt wurde                                                                                                                                                                                                                                                                                                                            |

---

**Zusammenfassung:** In diesem Repo ist Quellenarbeit ein 6-Schritte-Workflow, der von einer 5-stufigen Status-Hierarchie gesteuert wird. Die zentrale Karte ist [Literatur/_audit_status.md](cci:7://file:///Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit%20Vertiefung%20OneDrive/MPV/26-MPV/Literatur/_audit_status.md:0:0-0:0). Die operative Wahrheit pro Quelle steht in `Literatur/<bibkey>/verified_quotes.md`. Tools sind in `archiv/*.py` (Python) und in den Cascade-Standardtools. Goldene Regel: **immer zur Quelle zurück**, nie raten, nie still überschreiben.