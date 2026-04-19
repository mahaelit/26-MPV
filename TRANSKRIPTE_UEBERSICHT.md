# Transkripte-Uebersicht (Verortung im Lerndokument)

Dieser Bericht aggregiert die JSON-Verortungen aus `MPV/Literatur/Transkripte/einordnung/`. Die Transkripte sind **kuratierte Zitatstellen aus Originalquellen** (Handbuch Begabung, Renzulli/Reis, Trautmann u. a.) und sollten bei inhaltsgleichen Belegstellen **bevorzugt verwendet werden** gegenueber heuristischen Suchergebnissen.

- Quellordner: `MPV/Literatur/Transkripte/einordnung/`
- Anzahl JSON-Dateien: **10**
- Existierende BibKeys in `Quellen.bib`: **59**

## 1. Uebersicht

| JSON | Titel / Zweck | Buch / Quelle | Kapitel | BibKey bestehend | BibKey Vorschlag | Integration-Hints |
| --- | --- | --- | --- | --- | --- | --- |
| `Teil1_Verortung_Transkripte_HandbuchBegabung.json` | Verortung der Transkripte aus dem Handbuch Begabung im Lerndokument | Handbuch Begabung (2021) |  | `muelleroppliger2021handbuch` |  | 0 |
| `Teil2_verortung_transkripte.json` |  |  |  |  |  | 0 |
| `Teil3_Verortung_Teil3_BegabungenErkennen.json` |  |  |  |  |  | 0 |
| `Teil4_Transkript_Verortung_Handbuch_Begabung.json` | Verortung der Transkripte im Lerndokument | Handbuch Begabungsförderung (2021) |  |  |  | 0 |
| `Teil5_verortung_lerndokument.json` |  |  |  |  |  | 0 |
| `Teil6_Verortung_Transkript_Teil6_Renzulli_Reis.json` |  | Handbuch Begabung (2021) | Das »Renzulli-Lernsystem« (RLS) (444--454) |  | `renzullireis2021rls` | 0 |
| `Teil7_trautmann_verortung.json` | Verortung des Transkriptinhalts im Lerndokument und im Abgabedossier; Identifika... | Handbuch Begabung (2021) | Pädagogische Haltung des Akteurs (496-506) | `muelleroppliger2021handbuch` | `trautmann2021haltung` | 12 |
| `Teil8_lerndokument_struktur.json` |  |  |  |  |  | 0 |
| `Transkript_Verortung_Lerndokument_schema.json` |  |  |  |  |  | 0 |
| `Transkript_Verortung_Lerndokument_strukturiert.json` | Maschinenlesbare, normalisierte Verortung der transkribierten Handbuch-Kapitel i... |  |  |  |  | 0 |

## 2. Vorgeschlagene neue BibKeys (vorrangig @incollection)

Die Transkripte schlagen in mehreren Faellen **praezise Einzelbeitraege** innerhalb bestehender Sammelbaende vor. Diese sollten in `Quellen.bib` ergaenzt werden, damit konkrete Kapitel-Aussagen nicht ungenau dem ganzen Herausgeberband zugeordnet sind.

### `renzullireis2021rls` (aus `Teil6_Verortung_Transkript_Teil6_Renzulli_Reis.json`)

- **Kapitel:** Das »Renzulli-Lernsystem« (RLS)
- **Autor:innen:** Renzulli / Reis
- **Seiten:** 444--454
- **In:** Handbuch Begabung (2021) — Hrsg. Müller-Oppliger / Weigand

### `trautmann2021haltung` (aus `Teil7_trautmann_verortung.json`)

- **Kapitel:** Pädagogische Haltung des Akteurs
- **Autor:innen:** Trautmann, Thomas
- **Seiten:** 496-506
- **In:** Handbuch Begabung (2021) — Hrsg. Müller-Oppliger, Victor / Weigand, Gabriele
- **Status:** ergaenzt `muelleroppliger2021handbuch` (Sammelband-BibKey) durch @incollection-Variante

```bibtex
@incollection{trautmann2021haltung,
  author    = {Trautmann, Thomas},
  title     = {P{\"a}dagogische Haltung des Akteurs},
  booktitle = {Handbuch Begabung},
  editor    = {M{\"u}ller-Oppliger, Victor and Weigand, Gabriele},
  publisher = {Beltz},
  address   = {Weinheim and Basel},
  year      = {2021},
  pages     = {496--510},
  isbn      = {978-3-407-25806-9}
}
```

## 3. Transkripte pro bestehendem BibKey

### `muelleroppliger2021handbuch`
- `Teil1_Verortung_Transkripte_HandbuchBegabung.json` — Verortung der Transkripte aus dem Handbuch Begabung im Lerndokument
  - Kapitel: — (?)
  - Integration-Hints: 0; Issues: 0
  - Zielordner: ✅ Literatur-Ordner vorhanden
- `Teil7_trautmann_verortung.json` — Verortung des Transkriptinhalts im Lerndokument und im Abgabedossier; Identifika
  - Kapitel: Pädagogische Haltung des Akteurs (496-506)
  - Integration-Hints: 12; Issues: 0
  - Zielordner: ✅ Literatur-Ordner vorhanden

## 4. Offene Issues / Verifikationsauftraege

### [MEDIUM] ISS-01 — OCR/Seitenfehler (Transkript_Verortung_Lerndokument_strukturiert.json)

- **Beobachtung:** Die Uploads enthalten teils verkürzte oder fehlerhafte Seitenangaben (z.B. Kapitelenden).
- **Empfehlung:** Im Workbook wurden Startseiten aus dem TOC genutzt; Endseiten wurden aus der Folgestartseite minus 1 abgeleitet.

### [HIGH] ISS-02 — Metakommentar im Dateitext (Transkript_Verortung_Lerndokument_strukturiert.json)

- **Beobachtung:** Abschnitte wie „Dieses Kapitel ist für dich besonders wichtig …“ sind Bearbeitungskommentare, keine zitierfähigen Quellentexte.
- **Empfehlung:** Nicht bibliographisch verwerten; nur als Arbeitsnotiz lesen.

### [MEDIUM] ISS-03 — Dubletten (Transkript_Verortung_Lerndokument_strukturiert.json)

- **Beobachtung:** Baudson, Stadelmann, Grabner und Urban tauchen in mehreren Dateien erneut auf.
- **Empfehlung:** Für das Lerndokument nur einmal verorten und im Lesebudget nicht doppelt zählen.

### [MEDIUM] ISS-04 — Nur erwähnte Kapitel (Transkript_Verortung_Lerndokument_strukturiert.json)

- **Beobachtung:** Frühstudium, Netzwerke, Stipendien und Ressourcenorientierte Hochbegabtenberatung sind nur erwähnt, aber nicht transkribiert.
- **Empfehlung:** Nur als Lücke markieren; vor Nutzung erst Buch oder sauberen Transkripttext beschaffen.

### [HIGH] ISS-05 — Wichtige Handbuch-Lücken (Transkript_Verortung_Lerndokument_strukturiert.json)

- **Beobachtung:** Für dein Thema besonders einschlägig wären im selben Handbuch auch Stamm („begabte Minoritäten“) und Baum/Schader („Twice Exceptionality“).
- **Empfehlung:** Bei Gelegenheit gezielt diese beiden Handbuchkapitel ergänzend sichern.

### [INFO] ISS-06 — Buchzuordnung (Transkript_Verortung_Lerndokument_strukturiert.json)

- **Beobachtung:** Alle sieben Upload-Teile lassen sich sehr plausibel demselben Sammelband zuordnen: Handbuch Begabung.
- **Empfehlung:** Für die Bibliographie Kapitel einzeln nachführen, wenn du Kapitel direkt zitierst.

## 5. BibKey-Erwaehnungen pro Transkript (Kernsignal)

Die kuratierten Transkripte enthalten pro Zitatstelle einen `bib_key`. Haeufigkeit = Anzahl Zitatstellen, an denen der BibKey im Lerndokument verwendet werden soll. **Hohe Zahlen = hoher Transkript-Nutzen** bei der Verifikation dieser Quelle.

### 5a. Bestehende BibKeys (vorhanden in `Quellen.bib`)

| BibKey | Gesamt | Pro JSON (Datei : Anzahl) |
| --- | --- | --- |
| `lehwald2017motivation` | 26 | Teil5_verortung_lerndokument:12; Teil8_lerndokument_struktur:12; Teil2_verortung_transkripte:2 |
| `muelleroppliger2021handbuch` | 26 | Teil8_lerndokument_struktur:10; Teil5_verortung_lerndokument:8; Teil2_verortung_transkripte:6; Teil1_Verortung_Transkripte_HandbuchBegabung:1; Teil7_trautmann_verortung:1 |
| `booth2019index` | 23 | Teil5_verortung_lerndokument:12; Teil8_lerndokument_struktur:10; Teil2_verortung_transkripte:1 |
| `fischer2020begabungsfoerderung` | 23 | Teil8_lerndokument_struktur:12; Teil5_verortung_lerndokument:10; Teil2_verortung_transkripte:1 |
| `buholzer2010allegleich` | 22 | Teil5_verortung_lerndokument:11; Teil8_lerndokument_struktur:11 |
| `preckel2013hochbegabung` | 21 | Teil8_lerndokument_struktur:10; Teil5_verortung_lerndokument:8; Teil2_verortung_transkripte:3 |
| `trautmann2016einfuehrung` | 19 | Teil8_lerndokument_struktur:9; Teil5_verortung_lerndokument:7; Teil2_verortung_transkripte:3 |
| `gold2018lesenkannmanlernen` | 17 | Teil8_lerndokument_struktur:9; Teil5_verortung_lerndokument:8 |
| `kappus2010migration` | 17 | Teil8_lerndokument_struktur:9; Teil5_verortung_lerndokument:8 |
| `leikhof2021jugendliche` | 16 | Teil8_lerndokument_struktur:9; Teil5_verortung_lerndokument:7 |
| `grossrieder2010anerkennung` | 15 | Teil5_verortung_lerndokument:8; Teil8_lerndokument_struktur:6; Teil2_verortung_transkripte:1 |
| `kuhl2019diversitaet` | 15 | Teil5_verortung_lerndokument:7; Teil8_lerndokument_struktur:7; Teil2_verortung_transkripte:1 |
| `rosebrock2010grundlagen` | 14 | Teil8_lerndokument_struktur:8; Teil5_verortung_lerndokument:6 |
| `macha2019gender` | 13 | Teil8_lerndokument_struktur:7; Teil5_verortung_lerndokument:6 |
| `maehler2018diagnostik` | 12 | Teil5_verortung_lerndokument:6; Teil8_lerndokument_struktur:6 |
| `stamm2021fehlenderblick` | 12 | Teil8_lerndokument_struktur:7; Teil5_verortung_lerndokument:5 |
| `sturm2016graphomotorik` | 12 | Teil5_verortung_lerndokument:6; Teil8_lerndokument_struktur:6 |
| `behrensen2019inklusive` | 11 | Teil5_verortung_lerndokument:6; Teil8_lerndokument_struktur:5 |
| `burow2021positive` | 11 | Teil5_verortung_lerndokument:5; Teil8_lerndokument_struktur:5; Teil2_verortung_transkripte:1 |
| `ipege2009professionelle` | 11 | Teil8_lerndokument_struktur:6; Teil5_verortung_lerndokument:5 |
| `sedmak2021bildungsgerechtigkeit` | 11 | Teil8_lerndokument_struktur:5; Teil5_verortung_lerndokument:4; Teil1_Verortung_Transkripte_HandbuchBegabung:1; Teil2_verortung_transkripte:1 |
| `webb2020doppeldiagnosen` | 11 | Teil5_verortung_lerndokument:6; Teil8_lerndokument_struktur:5 |
| `kellerkoller2021hellekoepfe` | 10 | Teil8_lerndokument_struktur:6; Teil5_verortung_lerndokument:4 |
| `kosoroklabhart2021voneltern` | 10 | Teil5_verortung_lerndokument:5; Teil8_lerndokument_struktur:5 |
| `weigand2021separativ` | 10 | Teil8_lerndokument_struktur:5; Teil5_verortung_lerndokument:4; Teil2_verortung_transkripte:1 |
| `brunner2021hochbegabung` | 9 | Teil5_verortung_lerndokument:5; Teil8_lerndokument_struktur:4 |
| `burow2020future` | 9 | Teil8_lerndokument_struktur:5; Teil5_verortung_lerndokument:4 |
| `reutlinger2015hochbegabung` | 9 | Teil8_lerndokument_struktur:5; Teil5_verortung_lerndokument:4 |
| `unger2010begabungsfoerderung` | 8 | Teil5_verortung_lerndokument:4; Teil8_lerndokument_struktur:4 |
| `muelleroppliger2021plurale` | 7 | Teil8_lerndokument_struktur:3; Teil5_verortung_lerndokument:2; Teil1_Verortung_Transkripte_HandbuchBegabung:1; Teil2_verortung_transkripte:1 |
| `stamm2014mirage` | 7 | Teil8_lerndokument_struktur:4; Teil5_verortung_lerndokument:3 |
| `lemas2023begriffsklaerung` | 6 | Teil8_lerndokument_struktur:3; Teil5_verortung_lerndokument:2; Teil2_verortung_transkripte:1 |
| `stamm2012migranten` | 6 | Teil8_lerndokument_struktur:4; Teil5_verortung_lerndokument:2 |
| `dvs2025bbf` | 4 | Teil8_lerndokument_struktur:3; Teil5_verortung_lerndokument:1 |
| `kellerkoller2009begabte` | 4 | Teil8_lerndokument_struktur:3; Teil5_verortung_lerndokument:1 |
| `stamm2014handbuch` | 4 | Teil8_lerndokument_struktur:3; Teil5_verortung_lerndokument:1 |
| `stern2025intelligenz` | 4 | Teil8_lerndokument_struktur:2; Teil2_verortung_transkripte:1; Teil5_verortung_lerndokument:1 |
| `uslucan2012begabung` | 4 | Teil8_lerndokument_struktur:3; Teil5_verortung_lerndokument:1 |
| `baudson2021wasdenken` | 3 | Teil1_Verortung_Transkripte_HandbuchBegabung:3 |
| `grabnermeier2021expertise` | 3 | Teil1_Verortung_Transkripte_HandbuchBegabung:3 |
| `horvath2021elite` | 3 | Teil1_Verortung_Transkripte_HandbuchBegabung:3 |
| `kellerkoller2011erkennen` | 3 | Teil8_lerndokument_struktur:2; Teil5_verortung_lerndokument:1 |
| `stadelmann2021begabungsentwicklung` | 3 | Teil1_Verortung_Transkripte_HandbuchBegabung:3 |
| `urban2021kreativitaet` | 3 | Teil1_Verortung_Transkripte_HandbuchBegabung:3 |
| `weigand2021person` | 3 | Teil1_Verortung_Transkripte_HandbuchBegabung:3 |
| `wollersheim2021konstrukt` | 3 | Teil1_Verortung_Transkripte_HandbuchBegabung:3 |
| `alhroub2021utility` | 2 | Teil8_lerndokument_struktur:2 |
| `alodat2025equitable` | 2 | Teil8_lerndokument_struktur:2 |
| `bfs2022migration` | 2 | Teil8_lerndokument_struktur:2 |
| `erzinger2023pisa` | 2 | Teil8_lerndokument_struktur:2 |
| `gubbins2020promising` | 2 | Teil8_lerndokument_struktur:2 |
| `mun2020identifying` | 2 | Teil8_lerndokument_struktur:2 |
| `renzullireis2021rls` | 2 | Teil6_Verortung_Transkript_Teil6_Renzulli_Reis:2 |
| `gauckreimann2021psychdiagnostik` | 1 | Teil3_Verortung_Teil3_BegabungenErkennen:1 |
| `koopseddig2021frueheserkennen` | 1 | Teil3_Verortung_Teil3_BegabungenErkennen:1 |
| `muelleroppliger2021paeddiagnostik` | 1 | Teil3_Verortung_Teil3_BegabungenErkennen:1 |
| `preckel2021tad` | 1 | Teil3_Verortung_Teil3_BegabungenErkennen:1 |
| `stahl2021mbet` | 1 | Teil3_Verortung_Teil3_BegabungenErkennen:1 |
| `trautmann2021haltung` | 1 | Teil7_trautmann_verortung:1 |

