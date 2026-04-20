# Uebergabebericht: Literaturverifikation MPV-Masterpruefung

Stand: **2026-04-19** (Ende der Session vom 2026-04-19/20)
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
├── REWRITES.md                  SSOT TeX-Umzitierungen (collect_rewrites.py)
├── mpv.tex                      Lerndokument (L-Label, 232 Zitationen)
├── mpv_abgabedokument.tex       Abgabedossier (A-Label, 46 Zitationen)
├── bib2csv.py                   BibLaTeX -> XLSX + Ordner + Templates
├── sync_pdfs.py                 PDF-Mapping -> Literatur/<key>/source.pdf
├── cite_context.py              TeX -> Claims-Block in verified_quotes.md
├── pdf_extract.py               Poppler/pypdf/EPUB-Extraktion + Fuzzy-Suche
├── analyze_transkripte.py       10 JSONs -> TRANSKRIPTE_UEBERSICHT.md + Index
├── integrate_transkripte.py     Index -> Transkript-Block pro verified_quotes.md
├── collect_rewrites.py          Rewrite-Bloecke aus verified_quotes.md -> REWRITES.md
├── apply_rewrites.py            Rewrites in TeX anwenden (Dry-Run / --apply / Status-Flip)
├── build_index.py               BibKey-Statusuebersicht -> Literatur/_INDEX.md
├── _archiv_phase0/              Archivierte Phase-0-Skripte (nicht aktiv genutzt)
├── Literatur/
│   ├── _INDEX.md                Auto-erzeugte Status-Uebersicht aller 59 BibKeys
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
- **Stand bei letztem Lauf:** 278 Cite-Stellen auf 45 BibKeys (aktive); 14 weitere BibKeys haben einen "Aktuell nicht im TeX zitiert"-Block (Stub-Eintraege fuer die 2021er-`@incollection`-Eintraege, die nach Umzitierungen aktiv werden).
- **Bugfix April 2026:** `re.sub`-Replacement-String interpretierte `\parencite` als Backreference und brach mit `re.PatternError` ab. Fix in `cite_context.py:270` (Callable-Replacement statt String-Template). Selbe Bugklasse praeventiv in `integrate_transkripte.py:172` behoben.

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
  - **`Literatur/_transkripte_index.json`** — maschinenlesbarer Index: BibKey -> Liste von Befunden mit Integration-Hints (Schema-Version `1.1` mit Envelope `bibkey_to_transkripte`)
- **Aufruf:** `python analyze_transkripte.py`
- **Stand bei letztem Lauf:** 10 JSONs, 59 BibKeys referenziert (alle in Quellen.bib).
- **T3-Erweiterung April 2026:** Pro-Chapter-Extraktion fuer `chapters[]`-Arrays (Teil1/Teil3) implementiert. Neue Funktionen `_chapter_bibkey`, `_collect_chapter_relevance`, `_collect_chapter_hints`, `_extract_chapter_befund` in `analyze_transkripte.py`. `analyze_file()` liefert jetzt `list[TranskriptBefund]` (Haupt-Befund + 1 pro Chapter). Ergebnis: 9 Teil1-Chapter + 5 Teil3-Chapter mit reichen Hints (key_ideas, memorable_quotes_for_oral_exam, tex_placements, recommendation_for_inti). 14 Handbuch-`@incollection`-Eintraege haben jetzt substantielle Transkript-Bloecke.

### 3.6 `integrate_transkripte.py`

- **Zweck:** Pro BibKey im `_transkripte_index.json` einen `## Transkript-Verortungen`-Block zwischen `<!-- TRANSKRIPTE-START -->` und `<!-- TRANSKRIPTE-END -->` in `Literatur/<key>/verified_quotes.md` einfuegen. Platziert sich nach `<!-- CLAIMS-END -->` oder — falls fehlend — nach dem Header-Trenner (`---`). Idempotent: Re-Run ersetzt nur den Block.
- **Aufruf:** `python integrate_transkripte.py`
- **Stand bei letztem Lauf:** 59 BibKeys, alle 59 `verified_quotes.md` haben Block.
- **Erweiterung April 2026:** Neuer Rollentyp `chapter_main` fuer Kapitel-Befunde aus Multi-Chapter-Transkripten (Teil1/Teil3). Diese werden separat unter "Verortung als Kapitel-Hauptbeleg" gerendert mit Aisha-/Lea-Vignetten und Integration-Vorschlaegen.

### 3.7 `collect_rewrites.py`

- **Zweck:** Aggregiert alle YAML-Bloecke zwischen `<!-- REWRITES-START -->` und `<!-- REWRITES-END -->` aus den 59 `verified_quotes.md` und schreibt eine zentrale `REWRITES.md` (SSOT fuer TeX-Umzitierungen). Gruppiert nach `tex_file`, sortiert nach `line`, mit Status-Breakdown pro Dossier.
- **Aufruf:** `python collect_rewrites.py`
- **Voraussetzung:** PyYAML (`pip install pyyaml`). Bereits installiert (`yaml.__version__ == '6.0.3'`).
- **YAML-Schema pro Eintrag:** `tex_file`, `line`, `action` (`replace_key`/`remove_key`/`add_key`/`modify`), `old`, `new`, `reason`, `status` (`pending`/`applied`/`rejected`).
- **Stand bei letztem Lauf:** 6 Rewrites, alle `pending`. 5 aus `preckel2013hochbegabung`, 1 aus `fischer2020begabungsfoerderung`.
- **Konvention:** Rewrite-Blocks gehoeren in das Dossier des *ersetzten* (alten) BibKeys, nicht des neuen.

### 3.8 `apply_rewrites.py`

- **Zweck:** Wendet die `pending`-Rewrites aus den Dossiers tatsaechlich auf `mpv.tex` / `mpv_abgabedokument.tex` an. Importiert `collect_rewrites.collect_all` (gleiche SSOT).
- **Default = Dry-Run:** `python apply_rewrites.py` zeigt nur an, was passieren *wuerde*, schreibt nichts.
- **Sicherheits-Checks vor jedem Apply:** TeX-Datei existiert, Zeile `<line>` enthaelt `<old>` *eindeutig* (genau 1 Vorkommen), Status ist `pending`. Bei Mismatch -> SKIP mit klarer Fehlermeldung, kein blindes Ueberschreiben.
- **Filter:** `--bibkey <key>`, `--line <N>` zur Eingrenzung (z. B. einzelne Stelle testweise applyen).
- **Apply:** `--apply` schreibt tatsaechlich; `--yes` ueberspringt den interaktiven Prompt fuer Batch-Laeufe.
- **Status-Flip:** Nach erfolgreicher Anwendung wird im Dossier des `source_dossier` der YAML-Wert `status: pending` -> `status: applied` umgestellt (formaterhaltend, ueber das `(tex_file, line)`-Tupel eindeutig).
- **Idempotent:** Re-Run sieht `status: applied` und ueberspringt; nur `pending` wird verarbeitet.
- **Aufruf-Beispiele:**
  ```powershell
  python apply_rewrites.py                                                   # Dry-Run alle
  python apply_rewrites.py --bibkey preckel2013hochbegabung                  # Dry-Run gefiltert
  python apply_rewrites.py --bibkey preckel2013hochbegabung --line 650 --apply  # 1 Stelle apply
  python apply_rewrites.py --apply --yes                                     # Bulk apply
  ```
- **Nach jedem Apply:** `python collect_rewrites.py && python build_index.py` neu laufen lassen, damit `REWRITES.md` und `_INDEX.md` den neuen Status reflektieren.

### 3.9 `build_index.py`

- **Zweck:** Aggregiert pro BibKey: Bib-Metadaten (Autor/Jahr/Titel), Status-Header aus `verified_quotes.md`, Cite-Count aus CLAIMS-Block, Transkript-Anzahl, Volltext-Status (PDF/EPUB-Groesse), Rewrite-Counts (importiert `collect_rewrites.collect_all`). Schreibt `Literatur/_INDEX.md` mit Status-Verteilung, Detailtabelle, Highlights (vollstaendig verifiziert / mit pending Rewrites / kritische Luecken).
- **Aufruf:** `python build_index.py`
- **Bib-Parser:** Header-basiert via `BIB_HEADER_RE` (robust gegen `}` in Body-Werten und EOF-ohne-Newline).
- **Stand bei letztem Lauf:** 59 BibKeys / 59 Dossiers / 59 Transkript-Verortungen / 6 pending Rewrites.

---

## 4. Stand der Verifikation nach Session-Ende

**Schneller Ueberblick:** `Literatur/_INDEX.md` (auto-erzeugt durch `build_index.py`) zeigt Status-Verteilung, Detailtabelle und Highlights ueber alle 59 BibKeys. Die folgenden Abschnitte halten den Kontext fest, der nicht aus dem Index allein hervorgeht.

### 4.1 Verifizierte Quellen

**Siehe jeweilige `Literatur/<key>/verified_quotes.md` — detaillierter Befundbericht mit Urteils-Tabellen, Wortlaut-Zitaten, Rewrite-Bloecken (siehe §6.3) und konkreten Umzitierungs-Empfehlungen.**

#### Status 4 (Volltext geprueft)

- **`preckel2013hochbegabung`** (13 Cite-Stellen, EPUB):
  - 6 wortnah belegt, 2 bibliografisch, 3 fragwuerdig, 2 nicht gefunden
  - **Kritischer Befund:** Claims L:650, L:790, L:2747, L:3179 handeln von "dynamische/prozessorientierte Diagnostik" — das behandelt aber **Preckel/Vock 2013 "Hochbegabtendiagnostik"** (Hogrefe), nicht das Beck-Buch. Teil3 der Transkripte liefert jetzt **`preckel2021tad`** (Handbuch Begabung 2021) als Ersatz.
  - **5 Rewrite-Eintraege** (alle `pending`): L:449, L:650, L:790, L:2747, L:3179. Details in `REWRITES.md`.

- **`fischer2020begabungsfoerderung`** (13 Cite-Stellen, PDF 419 Seiten):
  - 7 wortnah belegt, 4 bibliografisch, 2 schwach belegt
  - **Kritischer Kontext:** Herausgeberband mit ~30 Beitraegen; Formulierungen wie "Fischer beschreibt..." sind APA-technisch unscharf.
  - **1 Rewrite-Eintrag** (`pending`): L:1755 -> `renzullireis2021rls` (Handbuch Begabung, S. 444-454). Details in `REWRITES.md`.

#### Status 3 (Transkript-konsistent + TOC-Kapitel-Verortung)

- **`lehwald2017motivation`** (13 Cite-Stellen, PDF nur 13 Seiten = Titelei + TOC + Vorwort):
  - 9 inhaltliche Claims via Teil8-Index 1:1 auf Zitat-IDs gemappt (`F1-EINL-Z14`...`F3-KR-Z05`).
  - 4 bibliografische Claims (Item-Listen).
  - Vorwort (S. 13) stuetzt Claim 6 "intrinsische Motivation als Treiber" wortgetreu.
  - Abkuerzungsverzeichnis (S. 11-12) mit Lehwalds eigenen Messinstrumenten (BVA, FES-S, CSBT) stuetzt Claim 7 (drei Motivationsformen) operativ.
  - **Keine Umzitierungen noetig.** Volltext-Verifikation aussenstehend (Buch via Swisscovery beschaffbar).

- **`buholzer2010allegleich`** (13 Cite-Stellen, PDF nur 2 Seiten = vollstaendiges TOC):
  - 9 inhaltliche Claims via Teil8-Index 1:1 auf Zitat-IDs gemappt (`F4-EINL-Z04`...`F5-KR-Z06`).
  - 4 bibliografische Claims (Item-Listen).
  - TOC verifiziert Kapitel-Zuordnungen wortgetreu: Fischer-Kap. S. 52, Buholzer S. 97 ("Lernprozesse foerderorientiert diagnostizieren"), Kummer Wyss S. 151 ("Kooperativ unterrichten").
  - Hinweis Claim 3 (L:1696): Terminus "Paedagogik der Vielfalt" ist Prengel (1993), Sach-Claim wird aber von Buholzer getragen — keine Umzitierung noetig, ggf. Endlektorat.
  - **Keine Umzitierungen noetig.** Volltext-Verifikation aussenstehend (Sammelband via Swisscovery beschaffbar).

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

**Status-Verteilung (Stand `_INDEX.md`):**

| Status | Anzahl |
|---|---:|
| 5 (vollstaendig verifiziert) | 0 |
| 4 (Volltext geprueft) | 2 (preckel, fischer) |
| 3 (Transkript-konsistent) | 2 (lehwald, buholzer) |
| 0 (ungeprueft) | 55 |

**Volltext lokal verfuegbar (Auswahl, restliche 17 noch ungeprueft):**
```
alhroub2021utility, alodat2025equitable, bfs2022migration, brunner2021hochbegabung,
erzinger2023pisa, gubbins2020promising, ipege2009professionelle,
kellerkoller2011erkennen, kosoroklabhart2021voneltern, leikhof2021jugendliche,
maehler2018diagnostik (foxit), mun2020identifying, reutlinger2015hochbegabung,
stamm2014mirage, sturm2016graphomotorik, uslucan2012begabung
```

**Nur via Transkript belegbar (Auswahl, hochpriorisiert):**
Zentral: `muelleroppliger2021handbuch` (11 Cites, 5 Transkript-Stellen),
`booth2019index` (11 Cites, 3), `kappus2010migration` (11 Cites, 2 — Kapitel
aus buholzer-Sammelband, ueber dessen TOC verifizierbar).

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

### 6.1 Sofortmassnahmen (in dieser Session erledigt)

- ✅ **A) `cite_context.py` Bugfix + Re-Run.** Backslash-in-Replacement-Bug gefixt; 14 neue CLAIMS-Bloecke fuer die 2021er-`@incollection`-Eintraege erzeugt.
- ✅ **B) T3 Pro-Chapter-Extraktion in `analyze_transkripte.py`.** 9 Teil1- + 5 Teil3-Chapter mit reichen Hints. `integrate_transkripte.py` um `chapter_main`-Rolle erweitert.
- ✅ **C) `_tmp_*`-Skripte aufgeraeumt, `_phase0_mapping.py` archiviert.**
- ✅ **D) Rewrite-Block-Konvention eingefuehrt** + `collect_rewrites.py` + `REWRITES.md` (siehe §6.3 fuer den Workflow).
- ✅ **E) `build_index.py` + `Literatur/_INDEX.md`.** SSOT-Statusuebersicht; ersetzt langfristig die manuell gepflegten Status-Spalten in `Quellen.xlsx`.

### 6.2 Phase 2, Etappe 1 abschliessen

Die Top-zitierten-Quellen inhaltlich verifizieren. **Priorisierung angepasst** wegen Transkript-Rueckendeckung. Stand:

| Quelle | Cite-Stellen | Volltext? | Status |
|---|---|---|---|
| `preckel2013hochbegabung` | 13 | EPUB | ✅ 4 (Volltext geprueft) |
| `fischer2020begabungsfoerderung` | 13 | PDF 419 S. | ✅ 4 (Volltext geprueft) |
| `lehwald2017motivation` | 13 | PDF 13 S. (TOC + Vorwort) | ✅ 3 (Transkript-konsistent) |
| `buholzer2010allegleich` | 13 | PDF 2 S. (TOC) | ✅ 3 (Transkript-konsistent + TOC) |
| `muelleroppliger2021handbuch` | 11 | keine Datei | ⚠️ offen (5 Transkripte; Einzelbeitraege als `@incollection` vorhanden) |
| `booth2019index` | 11 | keine Datei | ⚠️ offen (3 Transkripte) |
| `kappus2010migration` | 11 | keine Datei | ⚠️ offen (2 Transkripte; Kapitel im buholzer-Sammelband, S. 63 lt. TOC) |
| `leikhof2021jugendliche` | 10 | PDF 5.6 MB | ⚠️ offen (Volltext vorhanden, hoechste Priorisierung) |

**Empfehlung fuer naechste Verifikation (Reihenfolge):**

1. **`leikhof2021jugendliche`** — 10 Cites, Volltext lokal vorhanden (5.6 MB). Direkter Verifikationsweg via `pdf_extract.py`.
2. **`muelleroppliger2021handbuch`** — 11 Cites; Sammelband. Die 14 Einzelbeitraege (`@incollection`) sind als BibKeys angelegt; jetzt fehlt die Verifikation des **Sammelband-Keys** selbst (nicht nur seiner Beitraege).
3. **`kappus2010migration`** — 11 Cites; ist Kapitel im **buholzer2010allegleich**-Sammelband (S. 63-77 laut TOC). Kann ueber denselben TOC analog zur buholzer-Verifikation auf Status 3 gehoben werden.

**Workflow pro Quelle:**
1. Dossier oeffnen: `Literatur/<key>/verified_quotes.md`.
2. CLAIMS-Block lesen (alle TeX-Stellen).
3. TRANSKRIPTE-Block lesen (Teil8-IDs, Themen, Hints).
4. Bei Volltext: `python pdf_extract.py <key> -s "<phrase>"` fuer Wortlaut-Belege.
5. Befund-Abschnitt unterhalb `<!-- TRANSKRIPTE-END -->` schreiben (Vorlage: `lehwald2017motivation` oder `buholzer2010allegleich`).
6. Bei Umzitierungen: Rewrite-Block (siehe §6.3) anlegen.
7. Status-Zeile am Ende auf 3, 4 oder 5 setzen + Datum + Bearbeitenden eintragen.
8. `python build_index.py` zum Aktualisieren von `Literatur/_INDEX.md`.

### 6.3 Etappe 2+: TeX-Umzitierung

> **SSOT: `REWRITES.md`** (automatisch erzeugt durch `collect_rewrites.py`
> aus den `<!-- REWRITES-START ... -->`-Bloecken in den Dossiers).
> Die frueher hier gefuehrte manuelle Tabelle wurde durch diese
> zentrale Uebersicht abgeloest. Neue Umzitierungen werden als YAML-Block
> in das Dossier des *ersetzten* BibKeys eingetragen und bei naechstem
> Lauf automatisch aggregiert.

**Workflow:**

1. In `Literatur/<betroffener_bibkey>/verified_quotes.md` einen
   `<!-- REWRITES-START -->`-YAML-Block mit Feldern
   `tex_file`, `line`, `action`, `old`, `new`, `reason`, `status` anlegen.
2. `python collect_rewrites.py` ausfuehren — `REWRITES.md` wird neu erzeugt.
3. Umzitierungen umsetzen: manuell oder via `apply_rewrites.py` (noch zu
   implementieren; liest dieselben Bloecke).
4. Nach Umsetzung `status: pending` -> `status: applied` im Dossier aendern,
   `collect_rewrites.py` erneut laufen lassen.

**Aktueller Stand (Snapshot, Details -> `REWRITES.md`):** 6 Rewrites,
alle `pending`. 5 aus `preckel2013hochbegabung` (L:449, L:650, L:790,
L:2747, L:3179), 1 aus `fischer2020begabungsfoerderung` (L:1755).

Diese Umzitierungen sind **nutzer-getrieben** (nicht automatisch); die
Befund-Bloecke in `verified_quotes.md` geben pro Stelle die genaue
Empfehlung.

### 6.4 Phase 3: Konsolidierung

- ✅ `Literatur/_INDEX.md` automatisch via `python build_index.py` (siehe §3.9). Re-Run nach jeder Verifikation.
- ✅ `apply_rewrites.py` implementiert (siehe §3.8). Pending Rewrites koennen jetzt per Dry-Run geprueft und einzeln/bulk angewendet werden — mit automatischem Status-Flip im Dossier.
- ⏳ **Naechster Schritt:** Pascal/Inti pruefen die 6 pending Rewrites in `REWRITES.md`, dann
  ```powershell
  python apply_rewrites.py                # Vorschau
  python apply_rewrites.py --apply --yes  # Bulk anwenden
  python collect_rewrites.py              # REWRITES.md neu rendern
  python build_index.py                   # _INDEX.md neu rendern
  ```
- ⏳ XLSX-Status auf 5 setzen fuer vollstaendig verifizierte Quellen (per Skript oder manuell). Mittelfristig macht `_INDEX.md` die Status-Spalte im XLSX redundant.
- ⏳ Liste kritischer TeX-Stellen zusammenfassen — ist bereits in `_INDEX.md` als "Kritische Luecken"-Sektion (Status 0/1 + Cites ≥ 5) automatisch erzeugt.

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
  <!-- CLAIMS-START --> ... <!-- CLAIMS-END -->          (cite_context.py)
  <!-- TRANSKRIPTE-START --> ... <!-- TRANSKRIPTE-END --> (integrate_transkripte.py)
  ## Verifikations-Zusammenfassung                       (manuell)
  ## Befunde pro Cite-Stelle                             (manuell)
  ## Handlungsbedarf / Umzitierungs-Anweisungen          (manuell, optional)
  <!-- REWRITES-START --> ... <!-- REWRITES-END -->      (manuell, YAML; collect_rewrites.py liest)
  **Status:** <0-5>
  **Verifiziert am:** <YYYY-MM-DD>
  **Bearbeitet durch:** <Name>
  ```
- **Idempotenz:** Alle 9 aktiven Scripts (`bib2csv.py`, `sync_pdfs.py`, `cite_context.py`, `pdf_extract.py`, `analyze_transkripte.py`, `integrate_transkripte.py`, `collect_rewrites.py`, `apply_rewrites.py`, `build_index.py`) sind so gebaut, dass Re-Run sicher ist. Wiederholtes Laufen ueberschreibt nur die jeweils eigenen Marker-Bloecke (`<!-- CLAIMS-... -->`, `<!-- TRANSKRIPTE-... -->`, `<!-- REWRITES-... -->`) oder regeneriert die zentralen Output-Dateien (`REWRITES.md`, `_INDEX.md`). `apply_rewrites.py` ist im Default Dry-Run und schreibt erst mit `--apply`.

---

## 8. Bekannte Probleme / Offene TODOs

### 8.1 Infrastruktur

| ID | Thema | Prio |
|---|---|---|
| - | `bib2csv.py` Warnung, wenn BibKeys in `Quellen.bib` case-kollidieren | Niedrig |
| - | `health_check.py` (gebuendelter §9.1-Lauf mit Pass/Fail-Ausgabe) | Niedrig |

**Erledigt in der April-2026-Session:** T3 (Pro-Chapter-Extraktion), T4 (cite_context.py Re-Run), `_tmp_*`-Skripte aufgeraeumt, Rewrite-Konvention + `collect_rewrites.py` + `REWRITES.md`, `build_index.py` + `_INDEX.md`, T11 (`apply_rewrites.py` mit Dry-Run / `--apply` / Status-Flip).

### 8.2 Inhaltliche Verifikation

Siehe §6.2. Stand: 4 von 59 Quellen verifiziert (2 Status 4, 2 Status 3). Restliche 55 Quellen ungeprueft — priorisierter Backlog in `Literatur/_INDEX.md` Sektion "Kritische Luecken".

### 8.3 Beschaffungsluecken (nicht beschaffte Quellen mit vielen Cite-Stellen)

- `muelleroppliger2021handbuch` (11) — 5 Transkript-Stellen + 14 Einzelbeitraege als `@incollection` bereits angelegt. Sammelband selbst noch zu beschaffen.
- `booth2019index` (11) — 3 Transkript-Stellen.
- `kappus2010migration` (11) — 2 Transkript-Stellen; **wichtiger Hinweis:** ist Kapitel im buholzer-Sammelband (S. 63-77 laut TOC). Verifikation analog zu buholzer ueber Teil8 + TOC moeglich, ohne separaten Volltext.
- `trautmann2016einfuehrung` (9) — 3 Transkript-Stellen.
- `gold2018lesenkannmanlernen` (9) — 2 Transkript-Stellen.

Beschaffungsempfehlung: `muelleroppliger2021handbuch` physisch (Bibliothek Luzern) holen — deckt gleichzeitig 14 `@incollection`-Eintraege inhaltlich ab und laesst Inti den Beltz-TOC final verifizieren.

---

## 9. Wiederaufsetzen der naechsten Session

### 9.1 Minimaler Health-Check (1 Min)

```powershell
$env:PYTHONIOENCODING='utf-8'

# 1. bib2csv sollte sauber laufen (Excel zu)
python bib2csv.py

# 2. analyze_transkripte.py sollte 10 JSONs und 59 BibKeys finden
python analyze_transkripte.py

# 3. cite_context.py sollte 278 Cite-Stellen finden
python cite_context.py

# 4. integrate_transkripte.py sollte alle 59 Dossiers updaten
python integrate_transkripte.py

# 5. collect_rewrites.py sollte 6 Rewrites finden
python collect_rewrites.py

# 6. apply_rewrites.py Dry-Run: alle 6 als [DRY] anwendbar
python apply_rewrites.py

# 7. build_index.py sollte 59 BibKeys + 59 Dossiers + 59 Transkripte finden
python build_index.py
```

Wenn alles OK: weiter mit §6.2 (Empfehlung: `leikhof2021jugendliche`).

### 9.2 Einstiegspunkt fuer LLM-Agent

**Diesen Bericht lesen** (`UEBERGABEBERICHT.md`). Dann:

1. Lies `Literatur/_INDEX.md` fuer den aktuellen Status (autoritativ).
2. Lies `REWRITES.md` fuer den aktuellen Stand der TeX-Umzitierungen.
3. Lies die bereits fertigen Befund-Bloecke als Vorlagen:
   - **Status 4 (mit Volltext):** `Literatur/preckel2013hochbegabung/verified_quotes.md` und `Literatur/fischer2020begabungsfoerderung/verified_quotes.md` (ab `<!-- CLAIMS-END -->`).
   - **Status 3 (nur TOC/Transkripte):** `Literatur/lehwald2017motivation/verified_quotes.md` und `Literatur/buholzer2010allegleich/verified_quotes.md` (Mapping-Tabelle TeX -> Teil8-ID + Befunde pro Cite-Stelle).
4. Uebernimm das Format fuer die naechste Quelle (Empfehlung: `leikhof2021jugendliche`, Volltext lokal verfuegbar).
5. Bei Unklarheit: Workflow ist in §6.2 "Workflow pro Quelle" Schritt-fuer-Schritt beschrieben.

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
