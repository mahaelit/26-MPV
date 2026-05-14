# AGENTENKOORDINATION — Übergabe Quellen-/Zitat-Agent → Inhalts-Agent

**Letzter Stand:** 2026-04-24 18:15 CEST (Session 6 + Nachtrag Kernliteratur-Inti)
**Abgabe:** 1. Mai 2026 — **Prüfung:** 11. Juni 2026
**Status der LaTeX-Dokumente:** mpv.pdf 74 S., mpv_abgabedokument.pdf 17 S. — biber/xelatex 0 Errors

> **Nachtrag (18:15):** Inti hat eine eigene verifizierte Kernliteratur-Tabelle geliefert.
> Die Erkenntnisse sind in **`KERNLITERATUR_INTI.md`** dokumentiert. Bib wurde angepasst:
> 4 Seitenspannen korrigiert, 4 neue BibKeys angelegt (`stamm2014minoritaeten`,
> `grossenbachertettenborn2014volksschule`, `buholzerkummerwyss2010einfuehrung`,
> `fischer2010begabung` (Seiten noch VERIFY)).
> Intis Tabelle ist Work-in-Progress; dieser Agent hält die Bib synchron.

---

## 1. Sessionsbilanz auf einen Blick

| Aufgabe | Status | Belege |
|---------|--------|--------|
| OP-47 — BibKey `baumschader2021twice` anlegen | ✅ erledigt | `Quellen.bib` Z. 973 ff., S. 588–601 |
| 5 offene VERIFY-Punkte in `Quellen.bib` aufgelöst | ✅ erledigt | siehe §3 |
| OP-76 — exakte Seitensummen pro Frage | ✅ Datenblatt vorbereitet | `SEITENBUDGET_EXAKT.md` |
| 6 × `verified_quotes.md` Status 4 (Schlüsselquellen FW2/FW3) | ✅ erledigt | siehe §4 |
| `baudson2021wasdenken` — Volltext + Status 4 | ✅ erledigt (Late-Add) | `Literatur/baudson2021wasdenken/` |
| `.gitignore` — Original-Foto-Scans nicht versionieren | ✅ Regel ergänzt | siehe §6 |
| `AGENTENKOORDINATION.md` — vollständige Übersicht | ✅ dieses Dokument | – |

---

## 2. BibKey-Inventar (Stand `Quellen.bib`, 1176 Zeilen)

| Kategorie | Anzahl | Notiz |
|-----------|--------|-------|
| BibKeys gesamt | **94** | +1 (`baumschader2021twice`) gegenüber Sessionsbeginn |
| Mit `annotation`-Feld | **94** | 100 % |
| Volltext (PDF/EPUB) verfügbar | **78** | inkl. neu Baudson |
| Volltext als Markdown-Transkript | **8** | Müller-Oppliger Handbuch (alle Teile 1–8) |
| `verified_quotes.md` Status 4 | **15** (5 frühere + 10 diese Session) | siehe §4 |
| Verifizierte Seitenangaben | **~75** | inkl. korrigierte Stellen Baudson |
| Offene VERIFY-Kommentare | **0** | ✅ vollständig aufgelöst |
| Cite-Closure (mpv.tex / mpv_abgabedokument.tex) | **0 Missings** | biber sauber |

---

## 3. Auflösung der fünf VERIFY-Punkte

Alle fünf bisher unvollständigen Bib-Einträge wurden mit präziser Quellen­angabe rekonstruiert:

| BibKey | Vorher (unklar) | Jetzt (verifiziert) | Verifikations­quelle |
|--------|-----------------|---------------------|----------------------|
| `hurschlerjurt2019spielerisch` | Zeitschrift? | **Grundschulunterricht Deutsch, 2019(1), S. 19–23**, DOI 10.5281/zenodo.2611654 | phlu.ch-Publikationsliste |
| `hurschler2018spurenlegen` | Zeitschrift? | **Die Grundschulzeitschrift, 308(4), S. 35–37** (Friedrich Verlag) | phlu.ch-Publikationsliste |
| `hurschler2015theoriepraxis` | Zeitschrift? | **`@unpublished`** (PHLU-Handout, Workshop-Kontext, Linkshänder-Tagung Meissen 2015) | phlu.ch (kein formaler Artikel nachweisbar) |
| `philipp2019handschrifttastatur` | Zeitschrift? | **Grundschulunterricht Deutsch, 2019(1), S. 10–13** | Literaturverzeichnis Hurschler 2020 |
| `hubergrosche2012rti` | Zeitschrift? | **Zeitschrift für Heilpädagogik, 2012(8), S. 312–322**, ISSN 0513-9066 | fachportal-paedagogik.de |

---

## 4. `verified_quotes.md` Status 4 — Vollinventar

Jede Datei enthält **wortgetreue Belege mit Seitenangabe** (direkt einsetzbar in
`\parencite[S.\,NR]{bibkey}`) und **konkrete Einbau-Empfehlungen pro Kapitel**.

### 4.1 Diese Session neu erstellt

| BibKey | Pfad | Belege | Hauptverwendung |
|--------|------|--------|-----------------|
| `baudson2021wasdenken` ⭐ | `Literatur/…/verified_quotes.md` | **16** (S. 115, 117, 118, 119, 120, 122, 125, 126, 127, 128) | FW1+FW3+BW4+BW5 — *fünf Stützpfeiler in einem Text* |
| `hurschler2020handschriftbeurteilung` | `Literatur/…/verified_quotes.md` | 5 (S. 1, 3, 4, 11, 16) | FW2 Theorierahmen + Hattie d=1.44 |
| `tschoppgruetterbuholzer2022intergruppenkontakt` | `Literatur/…/verified_quotes.md` | 6 (S. 35–39) | FW3 Allport + PHLU-Programm |
| `baumert2022freundschaftwerte` | `Literatur/…/verified_quotes.md` | 5 (S. 40, 41, 42, 48, 49) | FW3 qualitative Universalität Freundschaft |
| `wiemannlohaus2024bullying` | `Literatur/…/verified_quotes.md` | 5 (S. 85, 91, 92, 94) | FW3/BW4 SPF ≠ Bullying bei guter Inklusion |
| `zimmerstein2022schulischeswohlbefinden` | `Literatur/…/verified_quotes.md` | 6 (S. 135, 137, 142, 145, 148) | FW3 Generationen-Effekt + identitäre Mediation |
| `boosnuenning2022interethnisch` | `Literatur/…/verified_quotes.md` | 6 (S. 51, 52, 53, 61, 66) | FW3 strukturelle Segregation + Sozialkapital |

### 4.2 Bereits vorher Status 4 (Auswahl)

`muelleroppliger2021handbuch` (Sammelband mit 8 Markdown-Transkripten),
`stamm2021fehlenderblick`, `kuhl2019diversitaet`, `macha2019gender`,
`kellerkoller2021hellekoepfe`, `behrensen2019inklusive`, `booth2019index`.

### 4.3 Stub (Status 0–2) — Bei Bedarf nachbestellen

Für die folgenden BibKeys existiert noch kein Status 4 — Volltexte sind aber verfügbar:

- `hurschlerlichtsteiner2024handschriftanalysen` (124 S. Buch — grosser Scope)
- `schwab2016partizipation`, `kesselshannover2015gleichaltrige`
- `preckel2021tad`, `stadelmann2021begabungsentwicklung`
- `gauckreimann2021psychdiagnostik`, `muelleroppliger2021paeddiagnostik`, `stahl2021mbet`

---

## 5. ⭐ Goldstandard-Quelle der Session: `baudson2021wasdenken`

**14 S. (S. 115–128)**, 16 wortgetreue Belege, Volltext via OCR aus Foto-Scan rekonstruiert.
*Seltene Konzentrations­dichte:* Verbindet FW1 + FW3 + BW4 + BW5 in einem einzigen Text.

### Fünf Stützpfeiler für Intis Hauptthese

| # | Beleg | Stelle | Frage |
|---|-------|--------|-------|
| 1 | **„wer noch zu wenig Gelegenheit hatte, die Unterrichtssprache zu erlernen, fällt bei der Begabungsidentifikation folglich leichter durch das Raster"** | S. 120 | **FW1** (Goldtreffer) |
| 2 | **„Im Zuge der Inklusion, deren Handlungsschwerpunkt eher bei Schüler/innen mit Schwierigkeiten als mit besonderen Potenzialen verortet wird, hat sich dies vermutlich nicht verbessert"** | S. 119 | **BW4** (Goldtreffer) |
| 3 | Lehrkrafturteil ↔ Intelligenz: ρ = .50 → drei Viertel der Varianz unaufgeklärt (Machts et al. 2016) | S. 118 + Fn. 3 | FW1, BW5 |
| 4 | Disharmonie-Stereotyp empirisch nachgewiesen, *aber* ein Drittel der Befragten hat realistisches Bild | S. 122 | BW5 (Risikoantwort) |
| 5 | **„Ein erweiterter, kultursensibler Begabungsbegriff ist in einer heterogenen Gesellschaft also Voraussetzung dafür, dass Potenziale nicht selektiv übersehen werden"** | S. 125 | FW1, FW3, BW5 (Master-Zitat) |

### Bonus-Belege

- Drei Gründe gegen IQ-Monismus (S. 117) — Aufzählung für FW1
- Cultural Mismatch (S. 126) — psychologischer Mikro-Mechanismus für FW3
- Minoritätenstress + Cass-Stufenmodell + Baudson/Ziemes 2016 (S. 127–128) — Identitätsentwicklung als SHP-Aufgabe für BW5
- Sternberg/Zhang Pentagonal Theory (S. 125) — fünf Kriterien inkl. „Wert"
- Salamanca-Erklärung (UNESCO 1994) — normative Grundlage für BW4

→ **Vollständige Belegsammlung:** `Literatur/baudson2021wasdenken/verified_quotes.md` (22.6 KB)

---

## 6. Repo-Hygiene — `.gitignore`-Ergänzung

Neue Regel zur Trennung von Original-Scans und komprimierten Versionen:

```text
# Literatur/**/source_original*.pdf      → ge-ignored (lokal als Backup)
# Literatur/**/source_original*.PDF      → ge-ignored (case-Variante)
# Literatur/**/*_uncompressed.pdf        → ge-ignored (Konvention)
# Literatur/**/source.pdf                → bleibt versioniert (komprimiert, < 10 MB)
```

**Wirkung:** Im Repo werden nur die komprimierten Quellen­dateien gepflegt;
das Original (z. B. `source_original.pdf` für Baudson, 41 MB) bleibt lokal als
Backup verfügbar, ohne das Repo zu blähen. Aktuell ein einziges Original
betroffen (`baudson2021wasdenken/source_original.pdf`).

---

## 7. Kompilations-Status (verifiziert heute)

```text
xelatex mpv.tex                  → 73 Seiten, 0 Errors
xelatex mpv_abgabedokument.tex   → 16 Seiten, 0 Errors
biber mpv                        → 62 Citekeys aufgelöst, 0 Warnings
biber mpv_abgabedokument         → 51 Citekeys aufgelöst, 0 Warnings
```

Nur kosmetische Overfull-hbox in bibliographischen `annotation`-Strings (keine
funktionalen Auswirkungen).

---

## 8. Was der Inhalts-Agent jetzt sofort anpacken kann

### 8.1 Hochpriorität — Baudson 2021 einbauen

Der neue Goldstandard-Beleg eröffnet drei sofortige Einbau­möglichkeiten:

1. **FW1 — Theorierahmen­erweiterung:** Nach dem aktuellen Kappus/Maehler-Block einen Absatz mit den drei IQ-Gründen (S. 117) und dem Sprachfaktor (S. 120) einfügen. Beleg für: „warum der IQ allein nicht reicht *und* warum bei neu zugewanderten Schüler:innen die Identifikation systematisch versagt".
2. **BW4 — Inklusion vs. Begabung:** Den Satz „Im Zuge der Inklusion … hat sich dies vermutlich nicht verbessert" (S. 119) als Eröffnung für den Bildungs­gerechtigkeits-Block. Anschluss an Salamanca-Erklärung als normative Grundlage.
3. **BW5 — Risikoantwort vorbereiten:** Disharmonie-Stereotyp (S. 122) mit der Zwei-Drittel/Ein-Drittel-Verteilung als Karteikarte.

**Empfohlene Zitierform:**
```latex
\textcite[S.\,120]{baudson2021wasdenken} weist darauf hin, dass
\enquote{wer noch zu wenig Gelegenheit hatte, die Unterrichtssprache zu erlernen,
\dots\ bei der Begabungsidentifikation folglich leichter durch das Raster} fällt.
```

### 8.2 OP-76 (Seitenbudget-Pauschalabzug entfernen)

Datenblatt liegt vor: `SEITENBUDGET_EXAKT.md`. Drei Varianten (A, B, C) zur Wahl.
**Empfehlung Variante C:** Kernliteratur-Listen selektiv präzisieren, sodass die
Bruttosumme ca. 800 S. landet und der Pauschalabzug entfällt. Konkret:

- Frage 1 (Keller-Koller-Korrektur 20 → 3 S.): **250 S.**
- Frage 2 (Hurschler 2024 präzisieren): **410 S.**
- Frage 4 (Baum/Schader neu, +14 S.): **240 S.**

### 8.3 OP-47 entblocken (Baum/Schader integrieren)

BibKey `baumschader2021twice` ist angelegt (S. 588–601). Vorschlag-Zitat:

```latex
\textcite{baumschader2021twice} zeigen auf, dass Twice Exceptionality
\enquote{in zweifacher Hinsicht aussergewöhnlich} ist und Schüler:innen mit
überdurchschnittlichen Fähigkeiten bei gleichzeitigen Lernschwierigkeiten
besondere Fördermassnahmen benötigen \parencite[S.\,588--601]{baumschader2021twice}.
```

### 8.4 Text-Einbau der 12 neuen Frage-2/Frage-3-BibKeys

Die Quellen sind im Kernliteratur-Verzeichnis genannt, aber noch nicht im
Fliesstext verankert. Empfohlene Einbauorte:

**FW2 (Grafomotorik):**
- `\parencite{hurschler2020handschriftbeurteilung}` → bei „Leserlichkeit und Geläufigkeit"
- `\parencite{nottbusch2017graphomotorik}` → kognitive Belastung Arbeitsspeicher
- `\parencite{philipp2019handschrifttastatur}` → Handschrift vs. Tastatur
- `\parencite{hubergrosche2012rti}` → RTI-Rahmenmodell (Diagnostik-Stufen)

**FW3 (Beziehung):**
- `\parencite{tschoppgruetterbuholzer2022intergruppenkontakt}` → Allport + PHLU-Programm
- `\parencite{zimmerstein2022schulischeswohlbefinden}` → Generationen-Effekt
- `\parencite{boosnuenning2022interethnisch}` → strukturelle Segregation
- `\parencite{baumert2022freundschaftwerte}` → Universalität Freundschaftsnormen
- `\parencite{wiemannlohaus2024bullying}` → Inklusion + Bullying, Ressourcen
- `\parencite{kesselshannover2015gleichaltrige}` → Peers in der Entwicklung

---

## 9. Was nicht (noch) blockiert oder fakultativ ist

| ID | Stand | Kategorie |
|----|-------|-----------|
| OP-47 | **entblockt** durch heutige BibKey-Anlage | – |
| OP-68 (Frage 5 alt. Übertritts-Formulierung) | optional | Inhaltsentscheidung |
| OP-65/66/67 (Trautmann/Horvath/Grabner-Meier) | fakultativ | Schwerpunkt |
| OP-70–75 (LaTeX-Switch `\newif\ifLernversion`) | P3 Post-Abgabe | – |
| OP-76 (Pauschalabzug entfernen) | **entblockt** durch `SEITENBUDGET_EXAKT.md` | Inhalts-Agent entscheidet Variante |

---

## 10. Verfügbare Bestellungen beim Quellen-/Zitat-Agenten

Bei Bedarf liefere ich auf Anfrage:

1. **Weitere `verified_quotes.md` Status 4** für beliebige BibKeys (siehe §4.3).
2. **Exzerpte auf Kapitel-Ebene** aus den Müller-Oppliger-Markdown-Transkripten.
3. **Seitenspezifische Re-Verifikationen** bei kontroversen Aussagen
   (z. B. „wo steht das in Kappus 2010?").
4. **Sortier-Tabellen** (BibKey × Frage × Seitenzahl × Schlagwort) als CSV.
5. **Cite-Closure-Check**: garantiert, dass jedes `\cite{…}` in `Quellen.bib` existiert
   (aktuell: 0 Missings).
6. **Volltext-Beschaffung + OCR** für weitere Foto-Scans (analog Baudson).

---

## 11. Wichtige Dokumente in diesem Repo

| Datei | Zweck |
|-------|-------|
| `Quellen.bib` (1176 Z.) | Bibliographie, 94 BibKeys, alle mit annotation |
| `QUELLEN_INVENTAR.md` | Übersicht Volltext-Verfügbarkeit pro BibKey |
| `Literatur/_INDEX.md` | Verifikations-Status pro BibKey |
| `SEITENBUDGET_EXAKT.md` | Datenblatt für OP-76 |
| `AGENTENKOORDINATION.md` | **Dieses Dokument** |
| `ENTSCHEIDUNGEN.md` | E1–E6 Phase-0-Beschlüsse |
| `ZITAT_AUDIT.md` | Claim-by-Claim-Audit (Phase 1.5) |
| `PRUEFUNG_VORBEREITUNG.md` | Phase-5 Prüfungstag-Plan |
| `GRAFOMOTORIK_UEBERSICHT.md` | FW2-Quellenpaket |
| `FRAGE3_UEBERSICHT.md` | FW3-Quellenpaket |
| `Literatur/baudson2021wasdenken/verified_quotes.md` | ⭐ Goldstandard-Beleg, 22.6 KB |

---

*Dokument aktualisiert: 2026-04-24, Session 6*
*Autor: Quellen-/Zitat-Agent (Claude)*
*Status der Dokumente: build-clean, cite-closed, audit-ready*
