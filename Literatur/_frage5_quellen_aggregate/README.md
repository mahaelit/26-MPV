# Frage-5-Quellen-Aggregat

Dieser Ordner enthaelt quellen-uebergreifende Metadaten und Notizen zu den
Frage-5-Quellen, die im Onboarding via `onboard_frage5.py` auf einzelne
`Literatur/<bibkey>/`-Ordner verteilt wurden.

## Dateien

- **`analyze_pdf_sources.json`** — Aggregat-Analyse aller 11 Frage-5-Quellen.
  Pro PDF: Titel, Autoren, Jahr, Verlag, Quellentyp, Hauptthema,
  zentrale Thesen, Begriffe, Theoriebezuege.
- **`muellerboesch_notes.txt`** — Verifikationsnotizen zur
  `muellerboeschschaffnermenn2021udl`-Quelle, ergaenzend zur JSON.
- **`README.md`** — diese Datei.

## Quelle (extern)

Ursprung: `MPV/Literatur/Frage 5/` (Inti Merollis lokales Repository ausserhalb
des Git-Repos). Die Aggregat-Dateien sind **redundant verfuegbar**, damit
spaetere Auswertungen nicht auf den externen Pfad angewiesen sind.

## Onboarding-Stand

| Bibkey | Bib-Eintrag | PDF | JSON | verified\_quotes.md |
|--------|-------------|-----|------|---------------------|
| `booth2019index` | bestand | `zb01_01_indikatorenfragebogen.pdf` (ZB-Auszug) | `zb01_01_indikatorenfragebogen.json` | bestand |
| `marti2015kompetenzfoerdernd` | NEU | `source.pdf` | `metadata.json` | Stub (Status 0) |
| `kummerwyss2017kooperativunterrichten` | bestand | bestand | `metadata.json` (NEU) | bestand |
| `phluzern2017tzi` | NEU | `source.pdf` | `metadata.json` | Stub (Status 0) |
| `reissenauerulsess2017anerkennendhandelnd` | NEU | `source.pdf` | `metadata.json` | Stub (Status 0) |
| `widmerwolf2018multiprofessionell` | NEU | `source.pdf` | `metadata.json` | Stub (Status 0) |
| `groschefussangelgraesel2020kokonstruktion` | NEU | `source.pdf` + `zb_wirkmodell_konstruktive_kooperation.pdf` | beide JSONs | Stub (Status 0) |
| `muellerboeschschaffnermenn2021udl` | NEU | `source.pdf` | `metadata.json` | Stub (Status 0) |
| `felder2022anerkennung` | NEU | `source.pdf` | `metadata.json` | Stub (Status 0) |
| `cast2024udlguidelines` | NEU | `source.pdf` | `metadata.json` | Stub (Status 0) |

11 Quellen, 8 neue Bib-Eintraege, 8 neue verified-quotes-Stubs.

## Folge-Schritte

1. **PDF-Kompression:** `groschefussangelgraesel2020kokonstruktion/source.pdf`
   (15\,MB) wurde via `compress_pdfs.py` auf ~2\,MB reduziert.
2. **Index aktualisieren:** `python3 build_index.py`
3. **Inventar aktualisieren:** `python3 build_inventar.py`
4. **Verifikation:** Status-0-Stubs nach woertlicher Pruefung pro Quelle
   auf Status~4 hochziehen (gemaess `BELEGPFLICHT.md`).

## Konvention

Onboarding erfolgt streng nach dem Muster bestehender `Literatur/<bibkey>/`-
Ordner; vgl. `Literatur/baudson2021wasdenken/verified_quotes.md` als Vorbild
fuer ein vollstaendig auf Status~4 verifiziertes Dossier.
