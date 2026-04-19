# Uebergabebericht: Literaturverifikation MPV-Masterpruefung

Stand: **2025-04-19** (Ende der Session)
Autor dieses Berichts: Cascade (LLM-Assistent)
Empfaenger: Naechste Session (Mensch oder LLM-Agent)

---

## 1. Vorhaben und Kontext

### 1.1 Wer und was

- **Autorin der Masterarbeit:** Inti Merolli, MA Schulische Heilpaedagogik, PH Luzern
- **Pruefungstermin:** 11. Juni 2026 (muendlich, Vertiefung)
- **Abgabefrist Abgabedossier:** 1. Mai 2026
- **Lerndokument-Thema:** *"Verdeckte Potenziale bei Schueler:innen mit Migrationserfahrung — Chancen inklusiver Begabungsfoerderung im Rahmen des Pilotprojekts SOLUX (IBBF)"*
- **Examinatorin:** Sabine Tanner Merlo
- **Fuenf Pruefungsfragen:**
  - FW1 (KS/DG): Multiperspektivische Erfassung verdeckter Begabungen
  - FW2 (MW/KS): Sensumotorische/schriftsprachliche Barrieren, ressourcenorientierte Foerderung
  - FW3 (PB): Ausgrenzungs-/Belastungs-/Migrationserfahrungen; Beziehungsgestaltung
  - BW4 (DG/PV): Inklusive Begabungsfoerderung am Beispiel SOLUX
  - BW5 (ZB/PV): Beratung und Zusammenarbeit aus SHP-Perspektive

### 1.2 Das Grundproblem

Die Arbeit bearbeitet Pascal Schmid (SHP-Ehemann, dxy GmbH). Das Lerndokument und das Abgabedokument enthalten zusammen **278 LaTeX-Zitationen** auf **59 BibKeys** (nach Session-Ende). Forderung: **keine einzige Zitat-Halluzination**. Jede `\cite{...}`-Stelle muss sich entweder in der Originalquelle (PDF/EPUB) oder in einem kuratierten Transkript wiederfinden lassen.

### 1.3 Gesamtansatz

1. Infrastruktur bauen (Scripts, Ordnerstruktur, Index-Dateien).
2. Pro BibKey eine `verified_quotes.md` fuehren mit drei Bloecken:
   - **Header** (automatisch refreshed von `bib2csv.py`)
   - **`<!-- CLAIMS-START ... END -->`** (automatisch von `cite_context.py`: alle Cite-Stellen aus `mpv.tex`/`mpv_abgabedokument.tex` mit Zeilennummer + Kontext)
   - **`<!-- TRANSKRIPTE-START ... END -->`** (automatisch von `integrate_transkripte.py`: kuratierte Verortungen mit Integration-Snippets)
   - **User-Bereich** (manuell: Befunde, wortgetreue Zitate, Urteile)
3. Phase 2: Quelle fuer Quelle verifizieren, Befunde im User-Bereich dokumentieren.
4. Phase 3: Abschluss-Index `_INDEX.md` + XLSX-Status auf 5.

---

## 2. Arbeitsverzeichnis und Dateien

### 2.1 Projektpfad

```
c:\Users\PascalSchmid\OneDrive - dxy\Kunden\fxyz\SHP\Masterarbeit Vertiefung OneDrive\MPV\26-MPV
```

(Das ist ein Git-Repo. Der Elternordner `..\MPV\` enthaelt die externen Daten — siehe 2.2.)

### 2.2 Wichtigste Dateien und Verzeichnisse

```
26-MPV/                          Git-Repo mit Arbeits-Artefakten
├── Quellen.bib                  BibLaTeX-Quelle (59 Eintraege)
├── Quellen.xlsx                 Tracking-Excel (per bib2csv.py generiert, idempotent)
├── Quellen.csv                  CSV-Variante (Excel-kompatibel, sep=; UTF-8-BOM)
├── TRANSKRIPTE_UEBERSICHT.md    Aggregierter Bericht zu den 10 Transkript-JSONs
├── UEBERGABEBERICHT.md          DIESER BERICHT
├── mpv.tex                      Lerndokument (L-Label, 232 Zitationen)
├── mpv_abgabedokument.tex       Abgabedossier (A-Label, 46 Zitationen)
├── bib2csv.py                   BibLaTeX -> XLSX + Ordner + Templates
├── sync_pdfs.py                 PDF-Mapping -> Literatur/<key>/source.pdf
├── cite_context.py              TeX -> Claims-Block in verified_quotes.md
├── pdf_extract.py               Poppler/pypdf/EPUB-Extraktion + Fuzzy-Suche
├── analyze_transkripte.py       10 JSONs -> TRANSKRIPTE_UEBERSICHT.md + Index
├── integrate_transkripte.py     Index -> Transkript-Block pro verified_quotes.md
├── _tmp_analyze.py              Temp-Script (nicht wichtig, kann geloescht werden)
├── Literatur/
│   ├── _transkripte_index.json  Maschinenlesbares Mapping BibKey -> Transkripte
│   └── <bibkey>/                  Ein Ordner pro BibKey (aktuell 59)
│       ├── source.pdf              Original (falls beschafft)
│       ├── source_foxit.pdf        Bevorzugt, falls Original defekt war (nur maehler)
│       ├── source.epub             Alternativ-Format (nur preckel2013)
│       ├── .extracted/             PDF-Text-Cache von pdf_extract.py
│       └── verified_quotes.md      Arbeitsdossier pro Quelle (3-Block-Struktur)

MPV/Literatur/                   Extern (ausserhalb Git): Quell-PDFs
├── (20 PDFs von den Original-Quellen, von sync_pdfs.py in 26-MPV/ kopiert)
└── Transkripte/einordnung/      Die 10 kuratierten Verortungs-JSONs
    ├── Teil1_Verortung_Transkripte_HandbuchBegabung.json
    ├── Teil2_verortung_transkripte.json
    ├── Teil3_Verortung_Teil3_BegabungenErkennen.json
    ├── Teil4_Transkript_Verortung_Handbuch_Begabung.json
    ├── Teil5_verortung_lerndokument.json
    ├── Teil6_Verortung_Transkript_Teil6_Renzulli_Reis.json
    ├── Teil7_trautmann_verortung.json
    ├── Teil8_lerndokument_struktur.json
    ├── Transkript_Verortung_Lerndokument_schema.json
    └── Transkript_Verortung_Lerndokument_strukturiert.json
```

---

## 3. Tools (in der Reihenfolge der typischen Ausfuehrung)

Alle Scripts sind in Python 3.13 geschrieben, Stand-Alone, **idempotent** (mehrfaches Ausfuehren ist sicher). Standard-Aufrufverzeichnis: `26-MPV/`. Alle erwarten `PYTHONIOENCODING=utf-8`.

### 3.1 `bib2csv.py`

- **Zweck:** Liest `Quellen.bib`, schreibt `Quellen.csv` + `Quellen.xlsx`, legt `Literatur/<bibkey>/` an, erzeugt/refresht `verified_quotes.md`-Templates.
- **Aufruf:** `python bib2csv.py`
- **Wichtig:** Excel muss geschlossen sein (sonst PermissionError).
- **Ergebnis aktuell:** 59 Eintraege, 59 Ordner, 59 verified_quotes.md.
- **Erhaltene manuelle Spalten:** Status, Swisscovery_URL, ISBN_ISSN_DOI, Suche_URL, Beschaffung, Pfad_lokal, Verifiziert_am, Bemerkung (145 Zellen in 45 Zeilen wurden beim letzten Lauf uebernommen).

### 3.2 `sync_pdfs.py`

- **Zweck:** Kopiert die 20 bestaetigten PDFs aus `MPV/Literatur/` nach `Literatur/<key>/source.pdf`. Aktualisiert XLSX-Status nur fuer Dateien, die tatsaechlich kopiert wurden (NFC-Unicode-Normalisierung gegen OneDrive-NFD-Quirks).
- **Aufruf:** `python sync_pdfs.py`
- **Mapping-Tabelle:** fest einkodiert in der `MAPPING`-Konstante. 20 Files. 2 davon sind "Inhaltsverzeichnis-only" (lehwald2017motivation, buholzer2010allegleich).
- **Erweiterung noetig, wenn neue PDFs beschafft werden:** `MAPPING`-Dict erweitern.

### 3.3 `cite_context.py`

- **Zweck:** Parst `mpv.tex` + `mpv_abgabedokument.tex` (strippt `\verb|...|` + `%`-Kommentare offset-preserving), sammelt alle `\cite/\parencite/\textcite/\autocite/...`-Kommandos mit Zeilennummer + Kontext (+/- 220 Zeichen). Schreibt pro BibKey einen Block zwischen `<!-- CLAIMS-START -->` und `<!-- CLAIMS-END -->` in `Literatur/<key>/verified_quotes.md`.
- **Aufruf:** `python cite_context.py`
- **Stand bei letztem Lauf:** 278 Cite-Stellen auf 45 BibKeys.
- **NOCH OFFEN nach Session-Ende:** Nach dem Anlegen der 14 neuen BibKeys in Quellen.bib muss `cite_context.py` erneut laufen, damit auch die 14 neuen `verified_quotes.md` einen Claims-Block bekommen ("Aktuell nicht im TeX zitiert." — das ist das gewuenschte Verhalten, weil die mpv.tex noch nicht umzitiert ist).

### 3.4 `pdf_extract.py`

- **Zweck:** Textextraktion aus Quellen mit drei Engines:
  - **poppler** (`pdftotext -layout -enc UTF-8`) — layout-treu
  - **pypdf** (Python-Bibliothek) — robust als Fallback
  - **epub** (stdlib `zipfile`+`html.parser`) — EPUB-Pseudoseiten nach Spine-Reihenfolge
- **Quelldatei-Priorisierung:** `source_foxit.pdf > source_ocr.pdf > source.pdf > source.epub`. Override per `--source <datei>` moeglich.
- **Modi:**
  - `--list` — Sanity-Check (Seiten + Zeichen pro Engine)
  - `-p 42` oder `-p 10-20` — Seiten dumpen
  - `-s "Phrase"` — Whitespace-tolerante Fuzzy-Suche mit `**...**`-Markierung
- **Cache:** `Literatur/<key>/.extracted/<engine>.txt` (Form-Feed 0x0C als Seitentrenner; Invalidierung per mtime).
- **Aufruf-Beispiele:**
  ```
  python pdf_extract.py preckel2013hochbegabung --list
  python pdf_extract.py maehler2018diagnostik -s "nonverbal" --context 120
  python pdf_extract.py fischer2020begabungsfoerderung -p 257-268 --engine poppler --out tmp.txt
  ```

### 3.5 `analyze_transkripte.py`

- **Zweck:** Liest die 10 Transkript-JSONs in `MPV/Literatur/Transkripte/einordnung/`, extrahiert heterogene Metadaten (jedes JSON hat eigenen Aufbau) und erzeugt:
  - **`TRANSKRIPTE_UEBERSICHT.md`** — menschenlesbarer Report mit Tabellen, BibKey-Vorschlaegen, Issues
  - **`Literatur/_transkripte_index.json`** — maschinenlesbarer Index: BibKey -> Liste von Befunden mit Integration-Hints
- **Aufruf:** `python analyze_transkripte.py`
- **Stand bei letztem Lauf:** 10 JSONs, 59 BibKeys referenziert (alle in Quellen.bib).
- **Bekannte Schwaeche:** Sammel-JSONs wie Teil1/Teil3 haben ein `chapters[]`-Array mit reichen pro-Chapter-Metadaten (key_ideas, instruments_mentioned, tex_placements). Mein Analyzer zieht diese pro-Chapter-Metadaten noch NICHT heraus — er behandelt das ganze JSON als einen Befund. Folge: der Transkript-Block in 13 Handbuch-Einzelbeitraegen ist duenn (nur Zitatstellen-Anzahl). TODO: siehe Abschnitt 8.

### 3.6 `integrate_transkripte.py`

- **Zweck:** Pro BibKey im `_transkripte_index.json` einen `## Transkript-Verortungen`-Block zwischen `<!-- TRANSKRIPTE-START -->` und `<!-- TRANSKRIPTE-END -->` in `Literatur/<key>/verified_quotes.md` einfuegen. Platziert sich nach `<!-- CLAIMS-END -->` oder — falls fehlend — nach dem Header-Trenner (`---`). Idempotent: Re-Run ersetzt nur den Block.
- **Aufruf:** `python integrate_transkripte.py`
- **Stand bei letztem Lauf:** 59 BibKeys, alle 59 `verified_quotes.md` haben Block.

---

## 4. Stand der Verifikation nach Session-Ende

### 4.1 Vollstaendig verifizierte Quellen (Status 4)

**Siehe jeweilige `Literatur/<key>/verified_quotes.md` — detaillierter Befundbericht mit Urteils-Tabellen, Wortlaut-Zitaten, konkreten Umzitierungs-Empfehlungen.**

- **`preckel2013hochbegabung`** (13 Cite-Stellen, EPUB):
  - 6 wortnah belegt, 2 bibliografisch, 3 fragwuerdig, 2 nicht gefunden
  - **Kritischer Befund:** Claims L:650, L:790, L:2747, L:3179 handeln von "dynamische/prozessorientierte Diagnostik" — das behandelt aber **Preckel/Vock 2013 "Hochbegabtendiagnostik"** (Hogrefe), nicht das Beck-Buch. Teil3 der Transkripte liefert jetzt **`preckel2021tad`** (Handbuch Begabung 2021) als Ersatz.
  - **Teil-Loesung bereits dokumentiert:** L:790 und L:2747/L:3179 koennen mit `maehler2018diagnostik` allein tragen (siehe `verified_quotes.md`, Abschnitt "Konkrete Umzitierungs-Anweisungen").

- **`fischer2020begabungsfoerderung`** (13 Cite-Stellen, PDF 419 Seiten):
  - 7 wortnah belegt, 4 bibliografisch, 2 schwach belegt
  - **Kritischer Kontext:** Herausgeberband mit ~30 Beitraegen; Formulierungen wie "Fischer beschreibt..." sind APA-technisch unscharf.
  - **Claim L:1755 (3 SEM-Typen)** ist in fischer2020 nicht systematisch entfaltet. Der neue **`renzullireis2021rls`** (Handbuch Begabung, S. 444-454) ist der bessere Beleg.

### 4.2 Neu angelegte BibKeys (Struktur-Stubs, Inhalte via Transkript verifizierbar)

14 `@incollection`-Eintraege aus dem Handbuch Begabung (Mueller-Oppliger/Weigand 2021, Beltz) wurden in `Quellen.bib:503-694` hinzugefuegt. Herkunft: aus den Transkripten abgeleitet, Seitenangaben gegen Beltz-TOC verifiziert.

| BibKey | Seiten | Pruefungsfrage-Hauptrelevanz |
|---|---|---|
| `weigand2021person` | 46-63 | BW5 (Professionsfundament), FW3 |
| `horvath2021elite` | 77-86 | BW5, BW4 |
| `wollersheim2021konstrukt` | 88-102 | FW1 (optional) |
| `baudson2021wasdenken` | 115-131 | BW5, FW3 — ⚠️ Transkript unvollstaendig |
| `stadelmann2021begabungsentwicklung` | 133-147 | FW1, FW2 — 🟢 **hochrelevant** (neurobiolog. Fundament) |
| `grabnermeier2021expertise` | 149-167 | FW2 (optional) — ⚠️ Transkript unvollstaendig |
| `urban2021kreativitaet` | 168-183 | BW4, FW1 |
| `muelleroppliger2021paeddiagnostik` | 224-238 | FW1 |
| `gauckreimann2021psychdiagnostik` | 239-251 | FW1, FW3 — 🟢 **Aisha-Vignette** (dt. Fallbeleg Unteridentifikation) |
| `stahl2021mbet` | 252-258 | FW1, BW5 |
| `koopseddig2021frueheserkennen` | 260-273 | BW4 (peripher) |
| `preckel2021tad` | 274-303 | FW1, BW4 — 🟢 **loest Preckel-Probleme** |
| `renzullireis2021rls` | 444-454 | BW4 — 🟢 **loest Fischer-Claim 11** |
| `trautmann2021haltung` | 496-510 | **BW5 (sehr hoch)**, FW3 (hoch) |

### 4.3 Nebenbefund: maehler-PDF repariert

`maehler2018diagnostik/source.pdf` hatte kaputte Font-Encoding (Ligaturen wie `D/i.geragnost/i.gerk` statt `Diagnostik`, Poppler lieferte 5960 Zeichen / 402 Seiten). Der Nutzer hat das PDF mit Foxit neu gedruckt. Die neue Datei `source_foxit.pdf` liefert **1.42 Mio Zeichen**, Ligaturen sauber. `pdf_extract.py` bevorzugt sie automatisch.

### 4.4 Status der restlichen Quellen

**Volltext lokal verfuegbar (19 weitere):**
```
alhroub2021utility, alodat2025equitable, bfs2022migration, brunner2021hochbegabung,
buholzer2010allegleich (⚠️ nur TOC), erzinger2023pisa, gubbins2020promising,
ipege2009professionelle, kellerkoller2011erkennen, kosoroklabhart2021voneltern,
lehwald2017motivation (⚠️ nur TOC), leikhof2021jugendliche, maehler2018diagnostik (foxit),
mun2020identifying, reutlinger2015hochbegabung, stamm2014mirage, sturm2016graphomotorik,
uslucan2012begabung
```
**Bisher nur via Transkript belegbar (restliche 26):**
Zentral: `booth2019index`, `kappus2010migration`, `muelleroppliger2021handbuch` — aber: fast alle haben mehrfache Verortung in den Transkripten, wodurch inhaltliche Verifikation moeglich ist.

---

## 5. Die 10 Transkript-JSONs: Rolle und Wert

Pascal hat per Claude-Analyst eine hochwertige Vor-Verortung aller Lerndokument-Zitate erstellt. Die JSONs sind **kuratiert und vertrauenswuerdig** — daher Priorisierung: **"Transkripte bevorzugen, heuristische Suche nur als Backup"**.

| JSON | Inhalt | Relevanz fuer Verifikation |
|---|---|---|
| Teil1 (56 KB) | Teil I+II Handbuch Begabung, 9 Chapters mit reichen Metadaten | 🟢🟢 Kernquelle fuer 7 neue BibKeys |
| Teil2 (48 KB) | Uebergreifende Verortungen, existierende BibKeys | Mittel |
| Teil3 (55 KB) | Teil III Handbuch Begabung, 5 Chapters mit Aisha-/Lea-Vignetten | 🟢🟢 Kernquelle fuer 5 neue BibKeys |
| Teil4 (49 KB) | Noch nicht detailliert analysiert | Unbekannt |
| Teil5 (144 KB) | Lerndokument-Zitate pro Abschnitt | 🟢 Power-JSON (viele Zitatstellen) |
| Teil6 (43 KB) | Renzulli/Reis RLS, vollstaendiges Einzel-Transkript | 🟢 Fertige Integration-Hints |
| Teil7 (42 KB) | Trautmann Haltung, vollstaendiges Einzel-Transkript | 🟢🟢 Goldene Qualitaet |
| Teil8 (144 KB) | Lerndokument-Skelett mit stabilen Zitatstellen-IDs | 🟢 Referenz-Dokument |
| Schema (7 KB) | JSON-Schema (nur formal) | Irrelevant fuer Verifikation |
| strukturiert (?) | Nicht detailliert analysiert (neu) | Unbekannt |

---

## 6. Naechste Schritte — konkret, in Reihenfolge

### 6.1 Sofortmassnahmen (5-30 Min je)

**A) cite_context.py erneut laufen lassen** (WICHTIG, noch nicht erfolgt):
```powershell
cd "c:\Users\PascalSchmid\OneDrive - dxy\Kunden\fxyz\SHP\Masterarbeit Vertiefung OneDrive\MPV\26-MPV"
$env:PYTHONIOENCODING='utf-8'; python cite_context.py
```
Erwartung: 14 neue Claims-Bloecke mit "_Aktuell nicht im TeX zitiert_", 45 unveraenderte. Die Claims-Zahl bleibt bei 278 (oder hoeher, falls mpv.tex in der Zwischenzeit umzitiert wurde).

**B) analyze_transkripte.py auf pro-Chapter erweitern** (TODO T3):
Fuer reiche Transkript-Bloecke bei den 13 Handbuch-Einzelbeitraegen. Konkret:
- `analyze_file()` so anpassen, dass bei `chapters[]`-Arrays (Teil1, Teil3) pro Chapter ein **zusaetzlicher** TranskriptBefund erzeugt wird — gebunden an den Chapter-BibKey mit den Feldern `title`, `pages`, `key_ideas`, `memorable_quotes_for_oral_exam`, `tex_placements`, `recommendation_for_inti`.
- `build_index()` speichert diese pro-Chapter-Befunde unter den entsprechenden BibKeys.
- `integrate_transkripte.py` kann unveraendert bleiben — die neuen Felder werden automatisch ausgegeben.
- Schaetzung: 30-45 Min inkl. Tests.

### 6.2 Phase 2, Etappe 1 abschliessen

Die Top-5-zitierten-Quellen inhaltlich verifizieren. **Priorisierung angepasst** wegen Transkript-Rueckendeckung:

| Quelle | Cite-Stellen | Volltext? | Strategie |
|---|---|---|---|
| `preckel2013hochbegabung` | 13 | EPUB | ✅ erledigt |
| `fischer2020begabungsfoerderung` | 13 | PDF | ✅ erledigt |
| `lehwald2017motivation` | 13 | nur TOC | ⚠️ Transkript-Verortungen (26) pruefen, inhaltlich via Teil5/8 verifizieren |
| `buholzer2010allegleich` | 13 | nur TOC | ⚠️ Transkript-Verortungen (22) pruefen |
| `kappus2010migration` | 11 | keine Datei | Via Transkripte (17 Verortungen) |
| `muelleroppliger2021handbuch` | 11 | keine Datei | Via Transkripte (26 Verortungen) — Sammelband, aber Einzelbeitraege jetzt als `@incollection` vorhanden |
| `booth2019index` | 11 | keine Datei | Via Transkripte (23 Verortungen) |

**Empfehlung fuer naechste Verifikation:** `lehwald2017motivation` — 26 Transkript-Stellen = maximale Transkript-Rueckendeckung bei fehlendem Volltext. Workflow:
1. Transkript-Block in `Literatur/lehwald2017motivation/verified_quotes.md` lesen (zeigt 3 Transkript-Befunde: Teil2, Teil5, Teil8).
2. In den JSON-Dateien gezielt nach `"bib_key": "lehwald2017motivation"` suchen und die zugehoerigen `kontextsatz`/`integration_vorschlag`-Werte mit den Claims aus `mpv.tex` abgleichen.
3. Befund-Abschnitt analog zu `preckel2013hochbegabung/verified_quotes.md` unterhalb `<!-- TRANSKRIPTE-END -->` schreiben.

### 6.3 Etappe 2+: TeX-Umzitierung

Das Lerndokument sollte die neuen BibKeys nutzen. Konkrete TODO-Liste (aus den verified_quotes.md-Befunden abgeleitet):

| TeX-Stelle | Aktuell | Empfohlen |
|---|---|---|
| `mpv.tex:449` | `\parencite{muelleroppliger2021handbuch,trautmann2016einfuehrung,preckel2013hochbegabung}` | Preckel streichen (Gardner-Bereiche sind dort nicht entfaltet) |
| `mpv.tex:650` | `\textcite{preckel2013hochbegabung}` ("dynamische Verfahren") | Auf `\textcite{preckel2021tad}` umstellen |
| `mpv.tex:790` | `\parencite{preckel2013hochbegabung}` ("wiederholte Erhebungen, nonverbal") | Preckel streichen (maehler2018 am Satzanfang traegt allein) |
| `mpv.tex:1755` | `\parencite{fischer2020begabungsfoerderung}` (drei Enrichment-Typen) | Auf `\parencite{renzullireis2021rls}` umstellen |
| `mpv.tex:2747` | `\parencite{preckel2013hochbegabung,lemas2023begriffsklaerung}` | Zu `\parencite{maehler2018diagnostik,lemas2023begriffsklaerung}` |
| `mpv.tex:3179` | `\parencite{lemas2023begriffsklaerung,preckel2013hochbegabung}` | Zu `\parencite{lemas2023begriffsklaerung,maehler2018diagnostik}` |

Diese Umzitierungen sind **nutzer-getrieben** (nicht automatisch); die Befund-Bloecke in `verified_quotes.md` geben pro Stelle die genaue Empfehlung.

### 6.4 Phase 3: Konsolidierung

- `Literatur/_INDEX.md` erzeugen mit Status-Uebersicht pro BibKey (Urteil, Seiten, Volltext-Status, Transkript-Verfuegbarkeit).
- XLSX-Status auf 5 setzen fuer vollstaendig verifizierte Quellen (per Skript oder manuell).
- Liste kritischer TeX-Stellen zusammenfassen (Abgabe-Risiken).

---

## 7. Wichtige Konventionen und Regeln

- **Keine Zitat-Halluzination:** Jede `\cite{...}`-Stelle braucht entweder PDF/EPUB oder Transkript-Verortung. Befund bei "nicht gefunden": im User-Bereich der verified_quotes.md dokumentieren, TeX-Autor entscheidet Umzitierung oder Streichung.
- **BibKey-Konvention:** alles lowercase, snake-artig, Jahresbestandteil ("muelleroppliger2021paeddiagnostik", nicht Camel-Case). BibTeX ist case-insensitive, aber Tools/JSON-Analyst matchen nur exakt.
- **Umlaute in LaTeX:** UTF-8 im Source ok; bei Bedarf `\"{a}` oder `\"{o}`. `biblatex+biber` faengt Umlaute korrekt.
- **Transkripte bevorzugen:** Die Transkripte sind kuratiert. Wenn ein Transkript eine Zitatstelle verortet und inhaltlich passt, **das Transkript zitieren** und den zugehoerigen BibKey nutzen, statt Heuristik-Suche im PDF.
- **`verified_quotes.md` Struktur fest:**
  ```
  # Verifizierte Zitate – <bibkey>
  <Header-Block mit Quelle/Link/Lokaler Pfad>
  ---
  <!-- CLAIMS-START --> ... <!-- CLAIMS-END -->    (cite_context.py)
  <!-- TRANSKRIPTE-START --> ... <!-- TRANSKRIPTE-END -->  (integrate_transkripte.py)
  ## Verifikations-Zusammenfassung                   (manuell)
  ## Befunde pro Cite-Stelle                         (manuell)
  ## Konkrete Umzitierungs-Anweisungen (wenn noetig) (manuell)
  **Status:** <0-5>
  **Verifiziert am:** <YYYY-MM-DD>
  **Bearbeitet durch:** <Name>
  ```
- **Idempotenz:** Alle 6 Scripts sind so gebaut, dass Re-Run sicher ist. Wiederholtes Laufen ueberschreibt nur die jeweils eigenen Marker-Bloecke.

---

## 8. Bekannte Probleme / Offene TODOs

### 8.1 Infrastruktur

| ID | Thema | Prio |
|---|---|---|
| T3 | `analyze_transkripte.py`: pro-Chapter-Extraktion fuer `chapters[]`-Arrays, damit die 13 Handbuch-Einzelbeitraege reiche Transkript-Bloecke bekommen | Mittel |
| T4 | `cite_context.py` erneut ausfuehren (fuer 14 neue BibKeys) | Niedrig (selbsterledigend beim Re-Run) |
| - | `_tmp_analyze.py` aufraeumen (war Debugging-Script in Phase 0) | Niedrig |
| - | `bib2csv.py` Warnung, wenn BibKeys in `Quellen.bib` case-kollidieren | Niedrig |

### 8.2 Inhaltliche Verifikation

Siehe 6.2 und 6.3. Noch nicht begonnen: 57 von 59 Quellen.

### 8.3 Beschaffungsluecken (nicht beschaffte Quellen mit vielen Cite-Stellen)

- `booth2019index` (11 Cites) — Transkript-Rueckendeckung 23
- `muelleroppliger2021handbuch` (11) — Transkript-Rueckendeckung 26 + 14 Einzelbeitraege
- `kappus2010migration` (11) — Transkript-Rueckendeckung 17
- `trautmann2016einfuehrung` (9) — keine lokale Datei
- `gold2018lesenkannmanlernen` (9) — keine lokale Datei

Beschaffungsempfehlung: `muelleroppliger2021handbuch` physisch (Bibliothek Luzern) holen — deckt gleichzeitig 14 `@incollection`-Eintraege inhaltlich ab und laesst Inti den Beltz-TOC final verifizieren.

---

## 9. Wiederaufsetzen der naechsten Session

### 9.1 Minimaler Health-Check (1 Min)

```powershell
cd "c:\Users\PascalSchmid\OneDrive - dxy\Kunden\fxyz\SHP\Masterarbeit Vertiefung OneDrive\MPV\26-MPV"
$env:PYTHONIOENCODING='utf-8'

# 1. bib2csv sollte sauber laufen
python bib2csv.py

# 2. analyze_transkripte.py sollte 10 JSONs und 59 BibKeys finden
python analyze_transkripte.py

# 3. pdf_extract.py sollte fuer preckel EPUB und fischer PDF laufen
python pdf_extract.py preckel2013hochbegabung --list
python pdf_extract.py fischer2020begabungsfoerderung --list
```

Wenn alles OK: weiter mit Sofortmassnahme A (cite_context.py) und dann mit 6.2.

### 9.2 Einstiegspunkt fuer LLM-Agent

**Diesen Bericht lesen** (`UEBERGABEBERICHT.md`). Dann:

1. Lies die bereits fertigen Befund-Bloecke:
   - `Literatur/preckel2013hochbegabung/verified_quotes.md` (ab `<!-- CLAIMS-END -->`)
   - `Literatur/fischer2020begabungsfoerderung/verified_quotes.md` (ab `<!-- CLAIMS-END -->`)
2. Uebernimm das Format fuer die naechste Quelle (Empfehlung: `lehwald2017motivation`).
3. Bei Unklarheit: Die Todo-Liste aus der letzten Session ist im Chat-Verlauf; dieser Bericht ersetzt sie konzeptionell.

### 9.3 Fuer den Nutzer zur Hand

Wenn etwas klemmt oder neue Daten kommen:

- **Neue PDF beschafft?** `MAPPING`-Dict in `sync_pdfs.py` erweitern, `python sync_pdfs.py` ausfuehren.
- **TeX umzitiert?** `python cite_context.py`, dann in den betroffenen `verified_quotes.md` den Claims-Block pruefen.
- **Neues Transkript-JSON?** In `MPV/Literatur/Transkripte/einordnung/` ablegen, `python analyze_transkripte.py`, dann `python integrate_transkripte.py`.
- **Neue BibKeys via Transkript?** `TRANSKRIPTE_UEBERSICHT.md` → Abschnitt "5b. NEUE BibKeys" zeigt, welche noch fehlen.
- **XLSX lockierung?** Excel schliessen.

---

## 10. Kontakt-/Kontextnotizen

- **Ordnerstruktur:** Der Nutzer arbeitet in einem OneDrive-Pfad. Unicode-Varianten (NFC vs. NFD) haben beim File-Zugriff einmal Probleme gemacht — Fix in `sync_pdfs.py:88-109` eingebaut.
- **Excel-Konflikte:** Mehrmals PermissionError, wenn `Quellen.xlsx` in Excel offen war. Scripts brechen sauber ab mit Hinweis. Excel schliessen, erneut ausfuehren.
- **Cache in `.extracted/`:** Nimmt bei vielen Quellen schnell Platz weg. Fuer maehler mit 1.42M Zeichen sind das ~3 MB. Kann bei Bedarf geloescht werden, wird beim naechsten Extract-Lauf neu erzeugt.

---

_Ende des Berichts._
