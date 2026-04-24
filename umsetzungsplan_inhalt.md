# Umsetzungsplan Inhaltsschärfung MPV Inti Merolli

## Präambel

- **Datum der Plangenerierung:** 24. April 2026, 15:30 (Stand 2, nach Zwischenarbeit Kollegen-Agent)
- **Referenzdokumente:**
  - [ueberarbeitungsplan_mpv.md](ueberarbeitungsplan_mpv.md) (strategische Gutachten-Synthese, Teile I–VI)
  - [mpv.tex](mpv.tex) (Lerndokument, 3608 Zeilen, Arbeitsstand 24.04.2026 15:28)
  - [mpv_abgabedokument.tex](mpv_abgabedokument.tex) (schlankes Abgabedossier, Arbeitsstand 24.04.2026 15:25)
  - [Quellen.bib](Quellen.bib) (Arbeitsstand 24.04.2026 15:49; Edits delegiert an Zitat-Audit-Agenten, Ausnahme OP-47 Baum/Schader als Koordinationspunkt)
  - [ZITAT_AUDIT.md](ZITAT_AUDIT.md) (Claim-by-Claim-Audit des Zitat-Audit-Agenten, 24.04.2026 15:22)
  - [ENTSCHEIDUNGEN.md](ENTSCHEIDUNGEN.md) (Phase-0-Grundsatzentscheidungen E1–E6)
- **Abgrenzung:** Dieser Plan adressiert ausschliesslich Fliesstext, Kapitelüberblick-Boxen, Titelseite, Einleitung, Fragestellungen, Kapitelüberschriften und LaTeX-Strukturelemente. Seitenzahlen in `\cite`/`\parencite`, Auflagen, VERIFY-/TODO-Marker und Bibliographie-Einträge sind Zuständigkeit des parallelen Zitat-Audit-Agenten.
- **Gesamtzahl Operationen:** **76** (P1: 20, P2: 40, P3: 16) plus 4 globale Suchen-und-Ersetzen-Regeln und 6 LaTeX-Strukturoperationen.
- **Konvention:** Zielstellen werden als `Datei: mpv.tex`, `Abschnitt: Einleitung → Ausgangslage`, Anker als 8–14 Wörter `old_str`-äquivalent, zusätzlich mit Zeilennummer dokumentiert. **Zeilennummern gelten für Stand 24.04.2026 15:28; nach weiteren Änderungen reverifizieren (per Grep auf den zitierten Anker, nicht per Zeilensprung).**
- **Schweizer Hochdeutsch:** Alle Textbausteine verwenden ss statt ß, keine Geviertstriche, keine Floskeln.

---

## Status-Update 24.04.2026 15:30 (Delta-Analyse nach Zwischenarbeit)

Der Kollegen-Agent (Zitat-Audit und Text-Revision gemäss [ENTSCHEIDUNGEN.md](ENTSCHEIDUNGEN.md) E1–E6) hat in der Zwischenzeit signifikant in `mpv.tex`, `mpv_abgabedokument.tex` und `Quellen.bib` gearbeitet. Die folgende Delta-Matrix zeigt, welche Operationen dieses Plans bereits vollständig, teilweise oder nicht erfüllt sind. **Ausführungsreihenfolge und OP-Texte aus dem Hauptteil bleiben gültig**; nur Anker und Arbeitsaufwand sind angepasst.

### Legende

- **erledigt:** Text entspricht bereits dem Plan-Zielzustand. OP übersprungen, Idempotenz-Check dokumentieren.
- **teilerfüllt:** Zielzustand teilweise erreicht; Rest-Textersatz gemäss OP-Textbaustein.
- **offen:** Keine Änderung seit Plangenerierung; OP vollständig auszuführen.
- **blockiert:** Wartet auf Zitat-Audit-Agent (BibKey, Seiten o. Ä.).

### Delta-Matrix (OPs aus P1/P2/P3)

| OP | Priorität | Status nach 24.04.2026 15:30 | Neue Ankerzeile in `mpv.tex` / `mpv_abgabedokument.tex` | Bemerkung |
|---|---|---|---|---|
| OP-01 | P1 | **teilerfüllt** | L:430–436 in `mpv.tex` | Progressionsabsatz wurde auf „Settings inklusiver Begabungsförderung, die Potenziale sichtbar machen" gestrafft, aber die volle Sichtbarkeitsformel (fünf Dimensionen, Grundfrage, SHP-Aufgabe) **fehlt**. OP-01-Textbaustein integral einspielen. |
| OP-02 | P1 | **teilerfüllt** | L:271–277 in `mpv_abgabedokument.tex` | analog zu OP-01. |
| OP-03 | P1 | **offen** | Titelseite `mpv.tex` L:133–137 | Untertitel noch „Verdeckte Potenziale bei Schüler:innen mit Migrationserfahrung". |
| OP-04 | P1 | **offen** | Titelseite `mpv_abgabedokument.tex` L:87–89 und `pdftitle` L:61 | analog. |
| OP-05 | P1 | **offen** | Frage-1-Quote `mpv.tex` L:447–450 | Wortlaut unverändert („mehrsprachigen Schüler:innen mit geringen Deutschkenntnissen multiperspektivisch und sprachsensibel"). |
| OP-06 | P1 | **teilerfüllt** | Frage-1-Quote `mpv_abgabedokument.tex` L:306–310 | Enumerate bereits auf „im frühen Zweitspracherwerb" umgestellt; Quote-Block noch unverändert. Neuformulierung mit „ohne Sprachleistung, Anpassungsverhalten und Begabung verwechseln" fehlt weiterhin. |
| OP-07 | P1 | **teilerfüllt** | FW1-Enumerate `mpv.tex` L:413–415 | „mehrsprachigen" bereits entfernt; Zusatz „ohne Sprachleistung, Anpassungsverhalten und Begabung verwechseln" noch nicht eingefügt. |
| OP-08 | P1 | **teilerfüllt** | FW1-Enumerate `mpv_abgabedokument.tex` L:252–254 | analog. |
| OP-09 | P1 | **offen** (Lerndokument) / **teilerfüllt** (Abgabedokument) | FW3-Quote `mpv.tex` L:1257–1261 / `mpv_abgabedokument.tex` L:351–354 | In `mpv_abgabedokument.tex` ist die Fassung bereits „Welche relationalen und strukturellen Bedingungen ermöglichen die Sichtbarkeit und Entfaltung von Begabung bei Schüler:innen mit Migrationserfahrung?"; Zusatz „und wie lassen sich Anerkennungserfahrungen und Teilhabe gestalten?" fehlt aber in beiden Dateien. In `mpv.tex` noch alt: „Wie beeinflussen Ausgrenzungs-, Belastungs- und Migrationserfahrungen …". |
| OP-10 | P1 | **offen** (Lerndokument) / **erledigt** (Abgabedokument) | FW3-Section-Heading `mpv.tex` L:1252–1253 / `mpv_abgabedokument.tex` L:346–347 | Abgabedokument bereits auf „Relationale und strukturelle Bedingungen der Begabungsentfaltung"; Lerndokument noch „Ausgrenzungs- und Migrationserfahrungen, Beziehungsgestaltung und Begabungsentwicklung". |
| OP-11 | P1 | **teilerfüllt** | FW2-Section-Heading `mpv.tex` L:841 | Abgabedokument bereits auf „Sensomotorische" umgestellt (L:320–321). Lerndokument L:841 noch „Sensumotorische". Zusätzlich eine verpasste Vorkommen L:1096 „Sensumotorische Defizite" im Fliesstext. |
| OP-12 | P1 | **offen** | Frage-4-Quote `mpv.tex` L:1680–1684 | „systematisch übersehen" noch vorhanden. |
| OP-13 | P1 | **teilerfüllt** | Frage-4-Quote `mpv_abgabedokument.tex` L:379–382 | „Schüler:innen mit Migrationserfahrung" bereits ergänzt; Zielwort „diagnostische Fenster" und „leicht verdeckt bleiben" noch nicht eingefügt (weiterhin „systematisch verdeckt bleiben"). |
| OP-14 | P1 | **teilerfüllt** | BW4-Enumerate `mpv.tex` L:417–421 | Migrationsperspektive zurückgeholt, aber Formulierung „systematisch verdeckt bleiben" steht weiterhin. |
| OP-15 | P1 | **teilerfüllt** | BW4-Enumerate `mpv_abgabedokument.tex` L:261–264 | analog zu OP-14. |
| OP-16 | P1 | **offen** | Einleitung `mpv.tex` nach L:361 (Ende *Der Fall S.*) | Abgabedokument hat bereits den Migrationsbegriffs-Absatz als `\paragraph{Begriffsklärung: Migrationserfahrung.}` (L:228–239). Lerndokument fehlt er weiterhin. |
| OP-17 | P1 | **teilerfüllt** | Einleitungsabsatz `mpv.tex` L:387–390 | Wortlaut „Der Fall S. dient im Folgenden als exemplarische Fallvignette" bereits vorhanden; Gruppenbezug-Schärfung aus Plan-Textbaustein noch nicht eingesetzt. |
| OP-18 | P1 | **teilerfüllt** | Einleitungsabsatz `mpv_abgabedokument.tex` L:246–249 | Abgabedokument hat „im frühen Zweitspracherwerb" bereits ergänzt; vollständige Schärfung nach OP-17-Textbaustein fehlt. |
| OP-19 / G-01 | P1 | **teilerfüllt** | Globale sensomotorisch-Ersetzung | Abgabedokument vollständig umgestellt; in `mpv.tex` **zwei verbleibende Vorkommen:** L:841 („Sensumotorische und …") und L:1096 („Sensumotorische Defizite …"). |
| OP-20 | P1 | **offen** | Einleitung `mpv.tex` L:368 | „defizitärer Zuschreibungen" unverändert. |
| OP-21–OP-24 | P2 | **offen** | FW2-Quote/Enumerate in beiden Dateien | Optionale Schärfung durch „über ein bedeutsames Interessensgebiet" nicht umgesetzt. |
| OP-25 | P2 | **offen** | Kapitelüberblick FW1 `mpv.tex` L:453–457 | Rückanker-Absatz fehlt. |
| OP-26 | P2 | **offen** | Kapitelüberblick FW3 `mpv.tex` L:1263–1266 | Rückanker-Absatz fehlt; Kapitelüberblick-Text noch mit „Belastungsperspektive". |
| OP-27 | P2 | **offen** | Kapitelüberblick BW4 `mpv.tex` L:1686–1690 | Abgrenzungs-Absatz FW1 vs.\ BW4 fehlt. |
| OP-28 | P2 | **offen** | Kapitelüberblick BW5 `mpv.tex` L:2127–2131 | Rückanker-Absatz fehlt. |
| OP-29 | P2 | **offen** | Gesamtüberblick-Box `mpv.tex` L:322–330 | Frage-3-Paraphrase „Welche Beziehungserfahrungen machen Sichtbarkeit möglich oder unmöglich?" noch alt. |
| OP-30 | P2 | **offen** | Gesamtüberblick-Box `mpv.tex` L:322–330 | Frage-4-Paraphrase noch alt. |
| OP-31–OP-37 | P2 | **offen** | „systematisch"-Stellen in FW1/FW3/BW4 | Wort „systematisch" unverändert an den in OPs 31–37 genannten Stellen; Zeilennummern um ca.\ 20 verschoben (Delta-Offset). |
| OP-38 | P2 | **offen** | FW3-Fliesstext `mpv.tex` L:1293–1296 | „Die Migrationserfahrung selbst ist ein Belastungsfaktor" unverändert. |
| OP-39 | P2 | **offen** | FW3-Kapitelüberblick `mpv.tex` L:1264 | „Belastungsperspektive" unverändert. |
| OP-40 | P2 | **offen** | Einleitungs-Kapitelüberblick `mpv.tex` L:336 | „eher defizitär gesehen" mit Geviertstrich unverändert. |
| OP-41 | P2 | **offen** | Einleitung `mpv.tex` L:378 | „defizitären Haltung" unverändert. |
| OP-42 | P2 | **offen** | Einleitung `mpv.tex` L:341–342 | „geringe Priorität" unverändert, aber ZITAT_AUDIT.md A.1-Stelle 3 fordert ohnehin Weicher-Formulierung (kompatibel). |
| OP-43 | P2 | **offen** | Einleitung `mpv_abgabedokument.tex` L:176 (ca.) | analog. |
| OP-44 | P2 | **offen** | Migrationsbegriffs-Absatz `mpv_abgabedokument.tex` L:228–239 | Absatz bereits vollständig; Ebikon-Satz aus Plan-Textbaustein fehlt noch. |
| OP-45 | P3 | **erledigt** (nicht nötig) | n/a | Einleitung ist als `\section*` mit `\subsection*` geführt; Konsistenz gegeben. |
| OP-46 | P3 | **offen** | `mpv.tex` L:1049–1061 (Schach-Abgrenzung) | „Nahtransfer"-Merkformel nicht eingefügt; Originalabsatz formal ausreichend (Referenzplan Teil II.2 markiert diesen Punkt als bereits erfüllt). |
| OP-47 | P2 | **blockiert** | 2e-Unterabschnitt `mpv.tex` ab L:671 | BibKey `baumschader2021twice` in `Quellen.bib` **fehlt weiterhin**; Koordination mit Zitat-Audit-Agent offen. |
| OP-48 | P3 | **offen** | `mpv.tex` ab L:622 (*Multiperspektivische und dynamische Erfassung*) | BibKey existiert; Einbau noch nicht erfolgt. |
| OP-49 | P3 | **offen** | `mpv.tex` ab L:595 (*Grenzen sprachlastiger Diagnostik*) | analog. |
| OP-50 | P3 | **offen** | `mpv.tex` ab L:622 | analog. |
| OP-51 | P2 | **offen** | Einleitung `mpv.tex` L:368 (nach OP-20) | Kappus-Zusatz nicht gesetzt. |
| OP-52 | P2 | **offen** | Einleitung `mpv_abgabedokument.tex` L:204 (ca.) | analog. |
| OP-53 | P2 | **offen** | Einleitung `mpv_abgabedokument.tex` L:213 (ca.) | analog. |
| OP-54 | P2 | **erledigt** (nicht ändern) | Einleitung `mpv.tex` L:365–368 | Formulierung „mögliche belastende Vorerfahrungen" wird als fachlich angemessen eingestuft; Idempotenz-Entscheidung dokumentiert. |
| OP-55 | P2 | **erledigt** (nicht nötig) | `mpv.tex` L:852 | „sensomotorisch-kognitiver Prozess" bereits konform. |
| OP-56 | P2 | **erledigt** (nicht ändern) | Gesamtüberblick-Box Frage-5-Zeile | Paraphrase bleibt. |
| OP-57 | P2 | **teilerfüllt** | FW3-Enumerate `mpv.tex` L:418–420 | Relationale/strukturelle-Formulierung bereits gesetzt; „Potenzialen" statt „Begabung" und Zusatz „Anerkennungserfahrungen und Teilhabe" fehlen. |
| OP-58 | P2 | **teilerfüllt** | FW3-Enumerate `mpv_abgabedokument.tex` L:258–260 | analog. |
| OP-59 | P2 | **teilerfüllt** | FW3-Quote `mpv_abgabedokument.tex` L:351–354 | Quote-Block bereits neu, Anerkennungs-Zusatz fehlt. |
| OP-60 | P2 | **erledigt** (durch OP-01 abgedeckt) | n/a | Dokumentation. |
| OP-61 | P3 | **offen** | `mpv.tex` ab L:504 (*Begabung als dynamisches Potenzial*) | preckel2021tad einbauen. |
| OP-62 | P3 | **offen** | `mpv.tex` ab L:504 | stadelmann2021begabungsentwicklung einbauen. |
| OP-63 | P3 | **entfällt** (delegiert) | REWRITES.md L:1689/L:1755 | Zitat-Audit-Rewrite zuständig. |
| OP-64 | P3 | **entfällt** (delegiert) | REWRITES.md | Zitat-Audit-Rewrite zuständig. |
| OP-65 | P3 | **offen** | `mpv.tex` BW5 | Nur auf ausdrückliche Intis-Entscheidung. |
| OP-66 | P3 | **offen** | `mpv.tex` Einleitung oder BW4 | Nur auf ausdrückliche Intis-Entscheidung. |
| OP-67 | P3 | **offen** | `mpv.tex` FW2 | Nur auf ausdrückliche Intis-Entscheidung. |
| OP-68 | P3 | **offen** (nicht empfohlen) | FW5 Quote und Enumerate beide Dateien | Alternative Schärfung. |
| OP-69 | P3 | **offen** | Kapitelüberblick BW5 `mpv.tex` L:2127–2131 | Transferrede-Kurzform einfügen nach OP-28. |
| OP-70–OP-75 | P3 | **offen** | Präambel und Boxen `mpv.tex` | LaTeX-Switch-Einführung; Ankerzeilen: `\usepackage{etoolbox}` L:22, Kapitelüberblicke L:315, 335, 453, 852, 1263, 1686, 2127, 2659, Kritische-Reflexion-Sections L:729, 1113, 1524, 1945, 2425, Fachartikel-Section L:2619, To-dos L:227 und L:280. |
| OP-76 | P3 | **offen** (nach Audit) | Seitenbudget-Tabelle `mpv_abgabedokument.tex` L:477–483 | Pauschalabzug von 188 auf 203 angepasst, aber nicht entfernt; Variante A gemäss Teil VI.2 nicht umgesetzt. |

### Zusätzliche Beobachtung (aus `Quellen.bib`-Delta)

Der Kollegen-Agent hat folgende VERIFY-Marker bereits geschlossen:
- `kellerkoller2021hellekoepfe`: `pages = {76--78}`, 3. Aufl. 2025
- `stamm2021fehlenderblick`: `pages = {576--587}` (statt 576–588)
- `kuhl2019diversitaet`: `pages = {35--59}`
- `macha2019gender`: `pages = {160--173}`
- `baudson2021wasdenken`, `grabnermeier2021expertise`, `trautmann2021haltung`: verifiziert.
- `brunner2021hochbegabung`: **gelöscht** (gemäss E5); im Fliesstext beider Dokumente durch `muelleroppliger2021handbuch` (Anderegg/Wilhelm + Nguyen/Sliwka) und `stamm2014handbuch` ersetzt.

**Offen für OP-47:** Der Eintrag `baumschader2021twice` ist auch im neuen Stand **nicht** vorhanden. Dieser Koordinationspunkt mit dem Zitat-Audit-Agent besteht fort.

### Konsequenzen für die Ausführungsreihenfolge

Die sechs Sessions der Ausführungsreihenfolge bleiben strukturell gleich, aber:
- **Session 1** reduziert sich um OP-45 (erledigt); die LaTeX-Switch-Einführung (OP-70–OP-74) ist weiterhin P3 und wird nach Abgabe empfohlen.
- **Session 2**: OPs 05–09 und 12–15 sind teilweise bereits erledigt; die OP-Textbausteine liefern jetzt die **Ergänzungen** (nicht mehr den vollständigen Ersatz), weil der Kollegen-Agent den Grobanteil schon gesetzt hat. **Ausnahme OP-09, OP-10 und OP-12**, die im Lerndokument unverändert sind und vollständig gemäss Plan-Textbaustein zu setzen sind.
- **Session 3** bleibt gültig; OP-16 muss im Lerndokument nachgezogen werden, OP-17/OP-18 sind vollständig zu schärfen.
- **Session 4** reduziert sich um OP-11 (teilerfüllt, nur noch L:841 und L:1096 in `mpv.tex`) und OP-19 (teilerfüllt).
- **Session 5 (Handbuchintegrationen, P3)** und **Session 6 (Post-Abgabe)** bleiben unverändert.
- **OP-47 bleibt blockiert**, bis Zitat-Audit-Agent den BibKey `baumschader2021twice` angelegt hat.

Nach Fertigstellung der P1- und P2-Operationen ist eine Grep-Verifikation pro Zieldokument sinnvoll:

```
rg -n 'mehrsprachigen Schüler:innen mit geringen' mpv.tex mpv_abgabedokument.tex
rg -n 'Sensumotor|sensumotor' mpv.tex mpv_abgabedokument.tex
rg -n 'Ausgrenzungs-, Belastungs-' mpv.tex
rg -n 'systematisch übersehen' mpv.tex mpv_abgabedokument.tex
rg -n 'defizitärer Zuschreibungen' mpv.tex mpv_abgabedokument.tex
rg -n 'baumschader2021twice' Quellen.bib mpv.tex mpv_abgabedokument.tex
```

Jeder Befehl soll **null Treffer** liefern (ausser `baumschader2021twice` nach OP-47-Abschluss mindestens einen Treffer pro Dokument plus Bib).

---

## Operationen

### P1 Operationen (vor Abgabe zwingend)

#### OP-01 Sichtbarkeitsformel in Einleitung `mpv.tex` einbauen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Einleitung → Abschnitt *Erkenntnisinteresse und Fragestellungen*, nach dem Absatz der fünf Pfeile und vor `\newpage`. Anker (ca. Zeile 411–418): `Die fünf Fragestellungen folgen einer Progression: von der multiperspektivischen Erkennung verdeckter Potenziale` … `dem professionellen Handeln der SHP im multiprofessionellen Team (BW\,5).`
- **Art des Eingriffs:** Absatzersatz (Progressionsabsatz durch Sichtbarkeits-Progressionsabsatz).
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** `ueberarbeitungsplan_mpv.md`, Teil I.1 und Teil II.6 (Hauptthese als roter Faden, Progressionsabsatz um Sichtbarkeitsformel verdichten).
- **Textbaustein:**

```
Die fünf Fragestellungen folgen einer Progression, die das Sichtbarkeitsproblem in fünf Dimensionen entfaltet: die diagnostische Methode (FW\,1), die kognitive und motorische Anforderungsstruktur (FW\,2), die relationalen und strukturellen Bedingungen (FW\,3), das Fördersetting als diagnostisches Fenster (BW\,4) und das professionelle Handeln im Team (BW\,5). Jede Frage beantwortet einen Teil der Grundfrage: Welche Bedingungen ermöglichen es, dass ein Potenzial sichtbar wird? Der Fall S.\ zeigt, dass Potenziale unter bestimmten Bedingungen sichtbar und unter anderen unsichtbar werden; die Aufgabe der SHP besteht darin, diese Bedingungen zu erkennen, zu gestalten und institutionell zu sichern.
```
- **Ausführungshinweise:** `\,` für schmales Leerzeichen bei `FW\,1` usw. verwenden (vorhandene Konvention).

#### OP-02 Sichtbarkeitsformel in Einleitung `mpv_abgabedokument.tex` einbauen
- **Zieldatei:** `mpv_abgabedokument.tex`
- **Zielstelle:** Einleitung → nach dem Progressionsabsatz `Die fünf Fragestellungen folgen einer Progression`, vor `\paragraph{Korpus-Trennung`. Anker ca. Zeile 271–277.
- **Art des Eingriffs:** Absatzersatz analog zu OP-01.
- **Abhängigkeiten:** keine (parallel zu OP-01 ausführbar)
- **Koordinationshinweis:** keiner
- **Begründung:** Teil I.1, Teil II.6.
- **Textbaustein:** identisch mit OP-01.
- **Ausführungshinweise:** Nach Implementierung LaTeX-Switch (OP-70ff.) ggf. obsolet; bis dahin separat pflegen.

#### OP-03 Titelseite `mpv.tex` auf Option A anpassen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Titelseite, Anker (ca. Zeile 133–138): `\textit{Verdeckte Potenziale bei Schüler:innen\\` `mit Migrationserfahrung}`.
- **Art des Eingriffs:** Textersatz im `\textit{...}`-Block und im Untertitel.
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil I.2 (Option A, moderate Schärfung).
- **Textbaustein:**

```
\textit{Verdeckte Potenziale bei neu zugewanderten,\\
mehrsprachigen Schüler:innen}\\[12pt]}
{\fontsize{16}{20}\selectfont
Chancen inklusiver Begabungsförderung\\
im Rahmen des Pilotprojekts SOLUX (IBBF)\par}
```
- **Ausführungshinweise:** Zeilenumbruch `\\` beibehalten. PDF-Titel-Metadatum `pdftitle` bleibt in der Präambel unverändert; optional OP-04.

#### OP-04 Titelseite `mpv_abgabedokument.tex` auf Option A anpassen
- **Zieldatei:** `mpv_abgabedokument.tex`
- **Zielstelle:** Titelseite Anker (ca. Zeile 88–89) `\textit{Verdeckte Potenziale bei Schüler:innen\\` `mit Migrationserfahrung}`. Zusätzlich `pdftitle` in der Präambel (Zeile 61).
- **Art des Eingriffs:** Textersatz, zweistellig (Titel + pdftitle).
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil I.2.
- **Textbaustein (Titel):** wie OP-03.
- **Textbaustein (pdftitle):**

```
  pdftitle={Masterprüfung Vertiefung – Verdeckte Potenziale bei neu zugewanderten, mehrsprachigen Schüler:innen}
```
- **Ausführungshinweise:** Im `pdftitle`-String den bestehenden Gedankenstrich (`–` U+2013) beibehalten; dies ist Metadatenfeld, nicht Fliesstext.

#### OP-05 Fragestellung FW1 im Quote-Block Frage 1 `mpv.tex` neu formulieren
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Frage-1-Kapitel, Anker (ca. Zeile 427–430): `\begin{quote}\itshape` `Wie können verdeckte Begabungen bei neu zugewanderten, mehrsprachigen` `Schüler:innen mit geringen Deutschkenntnissen multiperspektivisch und` `sprachsensibel erfasst werden?` `\end{quote}`.
- **Art des Eingriffs:** Textersatz im Quote-Block.
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil II.1 (Entdopplung, Begabungen → Potenziale).
- **Textbaustein:**

```
\begin{quote}\itshape
Wie können kognitive Potenziale bei neu zugewanderten Schüler:innen im
frühen Zweitspracherwerb multiperspektivisch erfasst werden, ohne
Sprachleistung, Anpassungsverhalten und Begabung miteinander zu verwechseln?
\end{quote}
```

#### OP-06 Fragestellung FW1 im Quote-Block `mpv_abgabedokument.tex` neu formulieren
- **Zieldatei:** `mpv_abgabedokument.tex`
- **Zielstelle:** Frage-1-Kapitel, Anker (ca. Zeile 295–299): `\begin{quote}\itshape` `Wie können verdeckte Begabungen bei neu zugewanderten, mehrsprachigen` `Schüler:innen mit geringen Deutschkenntnissen multiperspektivisch und` `sprachsensibel erfasst werden?`.
- **Art des Eingriffs:** Textersatz.
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil II.1.
- **Textbaustein:** identisch mit OP-05.

#### OP-07 Fragestellung FW1 im Enumerate `mpv.tex` auf „Potenziale" umstellen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Einleitung → Enumerate, Anker (ca. Zeile 393–395): `\item[\textbf{FW\,1 (KS/DG)}] Wie können verdeckte Begabungen bei neu` `zugewanderten Schüler:innen im frühen Zweitspracherwerb` `multiperspektivisch und sprachsensibel erfasst werden?`.
- **Art des Eingriffs:** Textersatz.
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil I.3 (Begabungen → Potenziale in Titel und Fragestellungen), Teil II.1.
- **Textbaustein:**

```
  \item[\textbf{FW\,1 (KS/DG)}] Wie können kognitive Potenziale bei neu
    zugewanderten Schüler:innen im frühen Zweitspracherwerb
    multiperspektivisch erfasst werden, ohne Sprachleistung,
    Anpassungsverhalten und Begabung miteinander zu verwechseln?
```
- **Ausführungshinweise:** bestehenden `% Revidiert (Phase 1.5, ENTSCHEIDUNGEN.md)`-Kommentar entfernen (Stand ist nun überholt), um Konfusion zu vermeiden.

#### OP-08 Fragestellung FW1 im Enumerate `mpv_abgabedokument.tex` auf „Potenziale" umstellen
- **Zieldatei:** `mpv_abgabedokument.tex`
- **Zielstelle:** Einleitung → Enumerate, Anker (ca. Zeile 252–255) analog zu OP-07.
- **Art des Eingriffs:** Textersatz.
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil I.3, Teil II.1.
- **Textbaustein:** identisch mit OP-07.

#### OP-09 Fragestellung FW3 im Quote-Block `mpv.tex` neu formulieren
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Frage-3-Kapitel, Anker (ca. Zeile 1257–1261): `\begin{quote}\itshape` `Wie beeinflussen Ausgrenzungs-, Belastungs- und Migrationserfahrungen die` `Begabungsentwicklung und soziale Teilhabe, und welche Beziehungsgestaltungen` `wirken förderlich?`.
- **Art des Eingriffs:** Textersatz (Widerspruchsauflösung, Eliminierung pathologisierender Formulierung).
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil II.3 (gravierendster inhaltlicher Bruch, Belastungserfahrungen-Pathologisierung, Widerspruchsauflösung).
- **Textbaustein:**

```
\begin{quote}\itshape
Welche relationalen und strukturellen Bedingungen ermöglichen die
Sichtbarkeit und Entfaltung von Potenzialen bei Schüler:innen mit
Migrationserfahrung, und wie lassen sich Anerkennungserfahrungen
und Teilhabe gestalten?
\end{quote}
```

#### OP-10 Section-Heading Frage 3 `mpv.tex` an Neuformulierung angleichen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Anker (ca. Zeile 1252–1253): `\section{Frage 3 (FW, PB): Ausgrenzungs- und Migrationserfahrungen,` `Beziehungsgestaltung und Begabungsentwicklung}`.
- **Art des Eingriffs:** Subsection-/Section-Umbenennung.
- **Abhängigkeiten:** OP-09 (konsistenter Wortlaut)
- **Koordinationshinweis:** keiner
- **Begründung:** Teil II.3 (Titel-Frage-Kohärenz).
- **Textbaustein:**

```
\section{Frage 3 (FW, PB): Relationale und strukturelle Bedingungen
  der Begabungsentfaltung}
```
- **Ausführungshinweise:** `\label{sec:frage3}` unverändert lassen (Querverweise bleiben stabil).

#### OP-11 Section-Heading Frage 2 `mpv.tex` Schreibweise vereinheitlichen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Anker (ca. Zeile 821–822): `\section{Frage 2 (FW, MW/KS): Sensumotorische und schriftsprachliche Barrieren` `und ressourcenorientierte Förderung}`.
- **Art des Eingriffs:** Textersatz (Terminologie).
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner; siehe Globale Regel G-01 für den gesamten Fliesstext.
- **Begründung:** Teil II.2 (sensomotorisch konsequent).
- **Textbaustein:**

```
\section{Frage 2 (FW, MW/KS): Sensomotorische und schriftsprachliche Barrieren
  und ressourcenorientierte Förderung}
```

#### OP-12 Fragestellung BW4 im Quote-Block `mpv.tex` neu formulieren
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Frage-4-Kapitel, Anker (ca. Zeile 1680–1684): `\begin{quote}\itshape` `Inwiefern können offene, enrichment-orientierte Begabungsförderungssettings` `wie SOLUX Potenziale sichtbar machen, die im Regelunterricht systematisch` `übersehen werden?`.
- **Art des Eingriffs:** Textersatz (Entschärfung „systematisch", Ergänzung „diagnostische Fenster").
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil II.4 (Entschärfung von „systematisch übersehen", Abgrenzung zu FW1), Teil IV.3.
- **Textbaustein:**

```
\begin{quote}\itshape
Inwiefern können offene, enrichment-orientierte Begabungsförderungssettings
wie SOLUX diagnostische Fenster für Potenziale schaffen, die in sprach-
und schriftlastigen Unterrichtsformaten leicht verdeckt bleiben?
\end{quote}
```

#### OP-13 Fragestellung BW4 im Quote-Block `mpv_abgabedokument.tex` neu formulieren
- **Zieldatei:** `mpv_abgabedokument.tex`
- **Zielstelle:** Frage-4-Kapitel, Anker (ca. Zeile 379–383): `\begin{quote}\itshape` `Inwiefern können offene, enrichment-orientierte Begabungsförderungssettings` `wie SOLUX Potenziale sichtbar machen, die im Regelunterricht bei` `Schüler:innen mit Migrationserfahrung systematisch verdeckt bleiben?`.
- **Art des Eingriffs:** Textersatz.
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil II.4, Teil IV.3.
- **Textbaustein:**

```
\begin{quote}\itshape
Inwiefern können offene, enrichment-orientierte Begabungsförderungssettings
wie SOLUX diagnostische Fenster für Potenziale schaffen, die in sprach-
und schriftlastigen Unterrichtsformaten bei Schüler:innen mit
Migrationserfahrung leicht verdeckt bleiben?
\end{quote}
```

#### OP-14 Fragestellung BW4 im Enumerate `mpv.tex` angleichen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Einleitung → Enumerate, Anker (ca. Zeile 402–406): `\item[\textbf{BW\,4 (DG/PV)}] Inwiefern können offene, enrichment-orientierte` `Begabungsförderungssettings wie SOLUX Potenziale sichtbar machen, die im` `Regelunterricht bei Schüler:innen mit Migrationserfahrung systematisch` `verdeckt bleiben?`.
- **Art des Eingriffs:** Textersatz.
- **Abhängigkeiten:** OP-12 (konsistente Formulierung).
- **Koordinationshinweis:** keiner
- **Begründung:** Teil II.4, Teil IV.3.
- **Textbaustein:**

```
  \item[\textbf{BW\,4 (DG/PV)}] Inwiefern können offene, enrichment-orientierte
    Begabungsförderungssettings wie SOLUX diagnostische Fenster für
    Potenziale schaffen, die in sprach- und schriftlastigen
    Unterrichtsformaten bei Schüler:innen mit Migrationserfahrung
    leicht verdeckt bleiben?
```

#### OP-15 Fragestellung BW4 im Enumerate `mpv_abgabedokument.tex` angleichen
- **Zieldatei:** `mpv_abgabedokument.tex`
- **Zielstelle:** Einleitung → Enumerate, Anker (ca. Zeile 261–265) analog zu OP-14.
- **Art des Eingriffs:** Textersatz.
- **Abhängigkeiten:** OP-13
- **Koordinationshinweis:** keiner
- **Begründung:** Teil II.4.
- **Textbaustein:** identisch mit OP-14.

#### OP-16 Einleitungsabsatz Migrationsbegriff in `mpv.tex` einsetzen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Einleitung → nach `\subsection*{Der Fall S.}`-Absatz (endend mit `Leseflüssigkeit liegt bei 17 Wörtern pro Minute.`, ca. Zeile 360) und vor `\subsection*{Heilpädagogischer Bezug}` (ca. Zeile 362).
- **Art des Eingriffs:** Absatzeinschub (neuer Absatz unter neuer Subsection-Überschrift).
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil I.4 (Migrationsbegriff in Einleitung, löst vier Randkommentare: Expats, Ebikon, Breite, Behrensen/Alodat).
- **Textbaustein:**

```
\subsection*{Begriffsklärung: Migrationserfahrung}

Unter \textit{Migrationserfahrung} wird in der vorliegenden Arbeit das
Aufwachsen beziehungsweise der Neuzugang in ein Schulsystem verstanden,
das nicht die primäre Sozialisationssprache des Kindes spricht,
typischerweise verbunden mit sozioökonomischer Benachteiligung
\parencite{bfs2022migration} und häufig mit unterbrochener Bildungsbiographie.
Der Fall S. liegt an der Schnittstelle zwischen Familiennachzug aus einem
Nicht-EU-Staat und möglicher Fluchterfahrung; die exakte Form ist für die
heilpädagogische Fragestellung sekundär, weil die wirksamen Mechanismen
(sprachliche Isolation, kumulative Belastung, defizitorientierte
Wahrnehmung) über Migrationstypen hinweg greifen
\parencite{behrensen2019inklusive,stamm2014handbuch}. Die Gemeinde Ebikon,
in der sich der Fall abspielt, zeichnet sich durch eine sozioökonomisch
heterogene Bevölkerung mit einem überdurchschnittlichen Anteil an Familien
mit Migrationsgeschichte aus; diese lokale Kontextbedingung ist für die
schulische Realität mitbestimmend.
```
- **Ausführungshinweise:** `\subsection*` analog zu den anderen Einleitungs-Subsections (ohne Nummerierung). `\parencite`-Keys bereits in `Quellen.bib` vorhanden und im Abgabedossier entsprechend zitiert (OP-20 Stichprobe-Koordination mit Zitat-Audit).

#### OP-17 Fall-vs-Vignette-Schärfung im Einleitungsabsatz `mpv.tex`
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Einleitung → *Erkenntnisinteresse und Fragestellungen*, Anker (ca. Zeile 387–390): `Der Fall S. dient im Folgenden als exemplarische Fallvignette: Er konkretisiert` `die allgemeinere Frage, wie verdeckte Potenziale bei neu zugewanderten,` `mehrsprachigen Schüler:innen erkannt, sichtbar gemacht und gefördert werden` `können.`.
- **Art des Eingriffs:** Textersatz (Schärfung, Gruppenbezug explizieren).
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil I.5 (Vignette versus Einzelfall, schriftliche Antwortlogik für mündliche Prüfung).
- **Textbaustein:**

```
Der Fall S.\ ist kein Einzelfall, der analysiert wird, sondern eine
Vignette, die ein strukturelles Muster konkretisiert. Die Gruppe, über
die die Arbeit spricht, sind neu zugewanderte Schüler:innen im frühen
Zweitspracherwerb, deren kognitive Potenziale durch die Kumulation
sprachlicher, schriftsprachlicher, sozialer und institutioneller
Barrieren verdeckt bleiben können. S.\ konkretisiert dieses Muster;
die theoretischen Aussagen gelten für die Gruppe.
```
- **Ausführungshinweise:** Bestehenden Randkommentar `%muss hier erklärt werden, was unter Migrationserfahrung verstanden wird …` entfernen (durch OP-16 beantwortet).

#### OP-18 Fall-vs-Vignette-Schärfung im Einleitungsabsatz `mpv_abgabedokument.tex`
- **Zieldatei:** `mpv_abgabedokument.tex`
- **Zielstelle:** Einleitung → *Erkenntnisinteresse*, Anker (ca. Zeile 246–249): `Der Fall S. dient im Folgenden als exemplarische Fallvignette: Er konkretisiert` `die allgemeinere Frage, wie verdeckte Potenziale bei neu zugewanderten Schüler:innen` `im frühen Zweitspracherwerb erkannt, sichtbar gemacht und gefördert werden können.`.
- **Art des Eingriffs:** Textersatz analog zu OP-17.
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil I.5.
- **Textbaustein:** identisch mit OP-17.

#### OP-19 Globale Suchen-und-Ersetzen-Operation „sensumotorisch" → „sensomotorisch" (Fliesstext)
- **Zieldatei:** `mpv.tex`, `mpv_abgabedokument.tex`
- **Zielstelle:** Alle Vorkommen von `sensumotorisch`, `sensumotorische`, `sensumotorischer`, `sensumotorischen`, `Sensumotorische`, `Sensumotorischen` im Fliesstext, **nicht** in Originalzitaten.
- **Art des Eingriffs:** Globale Suche-und-Ersetzen-Operation (siehe Globale Regel G-01).
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** **Ausnahme:** Innerhalb von wörtlichen Sturm-Zitaten (falls solche eingeführt werden) Originalform beibehalten. Zum Stand 24.04.2026 enthält `mpv.tex` keine Wortlautzitate Sturms, daher globales Ersetzen unproblematisch. Ergebnis mit Grep verifizieren.
- **Begründung:** Teil II.2 (Terminologie-Vereinheitlichung).
- **Textbaustein:** n/a (globales Pattern, siehe G-01).
- **Ausführungshinweise:** Nach Durchführung Grep `sensu` auf 0 Treffer prüfen.

#### OP-20 Entschärfung „defizitärer Zuschreibungen" → „defizitorientierter Deutungsmuster" in Einleitung `mpv.tex`
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Einleitung → *Heilpädagogischer Bezug*, Anker (ca. Zeile 368): `Under-Identifikation, defizitärer Zuschreibungen und institutioneller Diskriminierung`.
- **Art des Eingriffs:** Textersatz (Entschärfung gemäss Teil IV.3 Grundsatz: Struktur-Ebene statt Handlungs-Ebene).
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil IV.3 (*defizitäre Zuschreibung* → *defizitorientierte Deutungsmuster*).
- **Textbaustein:**

```
Under-Identifikation, defizitorientierter Deutungsmuster und institutioneller
Diskriminierung im Sinne Kappus~2010
```
- **Ausführungshinweise:** `im Sinne Kappus~2010`-Zusatz wird fakultativ (siehe OP-51); wenn OP-51 separat ausgeführt wird, hier nur Begriff ersetzen, nicht Anhang.

---

### P2 Operationen (vor Abgabe stark empfohlen)

#### OP-21 Frageformulierung FW2 im Quote-Block `mpv.tex` optional schärfen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Frage-2-Kapitel, Anker (ca. Zeile 826–829): `\begin{quote}\itshape` `Welche sensomotorischen und schriftsprachlichen Faktoren können dazu beitragen,` `dass kognitive Potenziale verdeckt bleiben, und wie lassen sie sich` `ressourcenorientiert fördern?`.
- **Art des Eingriffs:** Textersatz (Hinzufügen „über ein bedeutsames Interessensgebiet").
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil II.2 (Neuformulierung der Frage optional, entlastet Beweispflicht eines generischen Transfers).
- **Textbaustein:**

```
\begin{quote}\itshape
Welche sensomotorischen und schriftsprachlichen Faktoren können dazu
beitragen, dass kognitive Potenziale verdeckt bleiben, und wie lassen
sie sich über ein bedeutsames Interessensgebiet ressourcenorientiert
bearbeiten?
\end{quote}
```

#### OP-22 Frageformulierung FW2 im Enumerate `mpv.tex` angleichen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Einleitung → Enumerate, Anker (ca. Zeile 396–398): `\item[\textbf{FW\,2 (MW/KS)}] Welche sensomotorischen und schriftsprachlichen` `Faktoren können dazu beitragen, dass kognitive Potenziale verdeckt bleiben,` `und wie lassen sie sich ressourcenorientiert fördern?`.
- **Art des Eingriffs:** Textersatz.
- **Abhängigkeiten:** OP-21 (konsistente Formulierung)
- **Koordinationshinweis:** keiner
- **Begründung:** Teil II.2.
- **Textbaustein:**

```
  \item[\textbf{FW\,2 (MW/KS)}] Welche sensomotorischen und schriftsprachlichen
    Faktoren können dazu beitragen, dass kognitive Potenziale verdeckt bleiben,
    und wie lassen sie sich über ein bedeutsames Interessensgebiet
    ressourcenorientiert bearbeiten?
```

#### OP-23 Frageformulierung FW2 im Quote-Block `mpv_abgabedokument.tex` schärfen
- **Zieldatei:** `mpv_abgabedokument.tex`
- **Zielstelle:** Anker (ca. Zeile 325–329) analog zu OP-21.
- **Art des Eingriffs:** Textersatz.
- **Abhängigkeiten:** OP-21
- **Koordinationshinweis:** keiner
- **Begründung:** Teil II.2.
- **Textbaustein:** identisch mit OP-21.

#### OP-24 Frageformulierung FW2 im Enumerate `mpv_abgabedokument.tex` angleichen
- **Zieldatei:** `mpv_abgabedokument.tex`
- **Zielstelle:** Anker (ca. Zeile 255–258) analog zu OP-22.
- **Art des Eingriffs:** Textersatz.
- **Abhängigkeiten:** OP-23
- **Koordinationshinweis:** keiner
- **Begründung:** Teil II.2.
- **Textbaustein:** identisch mit OP-22.

#### OP-25 Kapitelüberblick Frage 1 um Sichtbarkeitsformel ergänzen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Kapitelüberblick-Box Frage 1, Anker (ca. Zeile 432–436): `\begin{kapitelueberblick}` `Das ist der \textbf{diagnostische Kern} der ganzen Arbeit.` … `Ein einzelner Test darf nie das letzte Wort haben.` `\end{kapitelueberblick}`.
- **Art des Eingriffs:** Absatzergänzung am Ende der Box, vor `\end{kapitelueberblick}`.
- **Abhängigkeiten:** OP-01 (Sichtbarkeitsformel definiert)
- **Koordinationshinweis:** keiner
- **Begründung:** Teil I.1 (Rückanker in FW1).
- **Textbaustein (einfügen vor `\end{kapitelueberblick}`):**

```
\medskip\textbf{Rückanker zur Hauptthese:} Frage~1 entfaltet die erste
Dimension des Sichtbarkeitsproblems: Welche diagnostische Methode macht
ein Potenzial sichtbar, das unter sprachlastigen Standardverfahren
unsichtbar bleibt?
```

#### OP-26 Kapitelüberblick Frage 3 an neue Frageformulierung anpassen und Sichtbarkeitsformel ergänzen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Kapitelüberblick-Box Frage 3, Anker (ca. Zeile 1263–1266): `\begin{kapitelueberblick}` `Dieses Kapitel verschiebt den Blick von der Diagnose zur \textbf{emotionalen und relationalen Bedingtheit von Entwicklung}.` …
- **Art des Eingriffs:** Absatzergänzung am Ende der Box vor `\end{kapitelueberblick}`, Beibehalten des bestehenden Kapitelüberblicks-Texts.
- **Abhängigkeiten:** OP-09, OP-10
- **Koordinationshinweis:** keiner
- **Begründung:** Teil I.1 (Rückanker FW3), Teil II.3 (Kapitelüberblick an neue Frage anpassen).
- **Textbaustein (einfügen vor `\end{kapitelueberblick}`):**

```
\medskip\textbf{Rückanker zur Hauptthese:} Frage~3 entfaltet die dritte
Dimension des Sichtbarkeitsproblems: Welche relationalen und strukturellen
Bedingungen ermöglichen, dass ein Potenzial sichtbar wird? Die Antwort
arbeitet mit Anerkennung, Teilhabe und kumulativer Belastung im Sinne
Behrensens~2019, nicht mit individueller Pathologisierung.
```

#### OP-27 Kapitelüberblick Frage 4 um Abgrenzung FW1 ergänzen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Kapitelüberblick-Box Frage 4, Anker (ca. Zeile 1686–1690): `\begin{kapitelueberblick}` `Dieses Kapitel hebt die Perspektive auf die \textbf{Ebene des Settings und der Schulstruktur}.` …
- **Art des Eingriffs:** Absatzergänzung am Ende vor `\end{kapitelueberblick}`.
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil II.4 (Kernunterscheidung FW1 vs.\ BW4 mündlich sitzen machen).
- **Textbaustein (einfügen vor `\end{kapitelueberblick}`):**

```
\medskip\textbf{Abgrenzung zu Frage~1:} Frage~1 fragt nach der
\textbf{diagnostischen Methode} (Verfahren, Instrumente, Mosaiksteine);
Frage~4 fragt nach der \textbf{strukturellen Lernumgebung} (Notenfreiheit,
Interessenorientierung, Sprachentlastung, Expertenrolle). SOLUX ist kein
zusätzliches Testinstrument, sondern ein Setting, das Potenziale zur
Darstellung kommen lässt, die in sprach- und schriftlastigen Formaten
leicht verdeckt bleiben.
```

#### OP-28 Kapitelüberblick Frage 5 um Sichtbarkeitsformel ergänzen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Kapitelüberblick-Box Frage 5, Anker (ca. Zeile 2102–2104): `\begin{kapitelueberblick}` `Dieses Kapitel beantwortet die Frage: \textbf{Was macht die SHP professionell in so einer Situation?}` …
- **Art des Eingriffs:** Absatzergänzung am Ende vor `\end{kapitelueberblick}`.
- **Abhängigkeiten:** OP-01
- **Koordinationshinweis:** keiner
- **Begründung:** Teil I.1 (Rückanker BW5).
- **Textbaustein (einfügen vor `\end{kapitelueberblick}`):**

```
\medskip\textbf{Rückanker zur Hauptthese:} Frage~5 entfaltet die fünfte
Dimension des Sichtbarkeitsproblems: Wie verhindert das multiprofessionelle
Team, dass ein Potenzial nach der Sichtbarwerdung im Projektsetting in den
Regelbetrieb und in Übertrittsentscheide unsichtbar zurückfällt?
```

#### OP-29 Kapitelüberblick Gesamtüberblick Frage 3 an neue Frageformulierung angleichen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Kapitelüberblick-Box [Prüfungsstrategie: Gesamtüberblick], Anker (ca. Zeile 306): `\textbf{Frage 3:} Welche Beziehungserfahrungen machen Sichtbarkeit möglich oder unmöglich?\\`.
- **Art des Eingriffs:** Textersatz (Paraphrase an neue Formulierung angleichen).
- **Abhängigkeiten:** OP-09
- **Koordinationshinweis:** keiner
- **Begründung:** Teil II.3 (Kapitelüberblicke an neue Fragen anpassen).
- **Textbaustein:**

```
\textbf{Frage 3:} Welche relationalen und strukturellen Bedingungen machen Sichtbarkeit möglich oder unmöglich?\\
```

#### OP-30 Kapitelüberblick Gesamtüberblick Frage 4 an neue Formulierung angleichen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Kapitelüberblick-Box [Prüfungsstrategie: Gesamtüberblick], Anker (ca. Zeile 307): `\textbf{Frage 4:} Welches Setting macht Potenziale sichtbar?\\`.
- **Art des Eingriffs:** Textersatz.
- **Abhängigkeiten:** OP-12
- **Koordinationshinweis:** keiner
- **Begründung:** Teil II.4.
- **Textbaustein:**

```
\textbf{Frage 4:} Welches Setting öffnet diagnostische Fenster für leicht verdeckte Potenziale?\\
```

#### OP-31 Entschärfung „systematisch übersehen" in Frage-1-Fliesstext
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Frage-1-Kapitel, Anker (ca. Zeile 440–442): `fragt danach, warum Begabungen bei Kindern mit Migrationsgeschichte systematisch` `übersehen werden und welche diagnostischen Zugänge geeignet sind, verdeckte Potenziale` `sichtbar zu machen.`.
- **Art des Eingriffs:** Textersatz (nur ein lokales Vorkommen, kein globales Ersetzen).
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil IV.3 (systematisch übersehen → strukturell erschwert erkennbar, ausser Stamm-Referenzen).
- **Textbaustein:**

```
fragt danach, warum Begabungen bei Kindern mit Migrationsgeschichte
strukturell erschwert erkennbar sind und welche diagnostischen Zugänge
geeignet sind, verdeckte Potenziale sichtbar zu machen.
```

#### OP-32 Entschärfung „systematisch übersehen" im Kapitelüberblick-FW3-Vorspann (Überleitung zu Frage 4)
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Anker (ca. Zeile 1662–1663): `wie SOLUX Potenziale sichtbar machen, die im Regelunterricht systematisch` `übersehen werden?`.
- **Art des Eingriffs:** Textersatz.
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil IV.3.
- **Textbaustein:**

```
wie SOLUX Potenziale sichtbar machen, die im Regelunterricht leicht
verdeckt bleiben?
```

#### OP-33 Entschärfung „systematische Unsichtbarkeit" in BW4-Fliesstext
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Anker (ca. Zeile 1712–1714): `Anforderungen, seiner Selektionslogik und seiner Orientierung an messbarer Leistung` `produziert für Kinder wie S. systematische Unsichtbarkeit: Wo Beteiligung an Schriftsprache` `geknüpft ist, kann sich kognitives Potenzial nicht zeigen.`.
- **Art des Eingriffs:** Textersatz.
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil IV.3 (weniger anklagende Formulierung).
- **Textbaustein:**

```
produziert für Kinder wie S. eine strukturelle Unsichtbarkeit: Wo Beteiligung
an Schriftsprache geknüpft ist, kann sich kognitives Potenzial nicht zeigen.
```

#### OP-34 Subsection-Überschrift „Homogenitätslogik und systematische Unsichtbarkeit" entschärfen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Anker (ca. Zeile 1731): `\subsection{Homogenitätslogik und systematische Unsichtbarkeit}`.
- **Art des Eingriffs:** Subsection-Umbenennung.
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil IV.3.
- **Textbaustein:**

```
\subsection{Homogenitätslogik und strukturelle Unsichtbarkeit}
```

#### OP-35 Entschärfung „Homogenitätslogik systematische Unsichtbarkeit" in Fliesstext
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Anker (ca. Zeile 1754–1756): `Für Kinder wie S. erzeugt diese Homogenitätslogik systematische Unsichtbarkeit.`.
- **Art des Eingriffs:** Textersatz.
- **Abhängigkeiten:** OP-34
- **Koordinationshinweis:** keiner
- **Begründung:** Teil IV.3.
- **Textbaustein:**

```
Für Kinder wie S. erzeugt diese Homogenitätslogik eine strukturelle
Unsichtbarkeit.
```

#### OP-36 Entschärfung „Zuschreibungen systematisch verzerrt" in BW4-Fliesstext
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Anker (ca. Zeile 1862–1864): `Zuschreibungen systematisch verzerrt ist. Kinder, die nicht identifiziert werden,`.
- **Art des Eingriffs:** Textersatz.
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil IV.3.
- **Textbaustein:**

```
Zuschreibungen strukturell verzerrt ist. Kinder, die nicht identifiziert werden,
```

#### OP-37 Entschärfung „Übertrittsverfahren systematisch benachteiligt" in BW4-Fliesstext
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Anker (ca. Zeile 2014–2016): `Übertrittsverfahren systematisch benachteiligt werden, weil Lehrpersonen`.
- **Art des Eingriffs:** Textersatz.
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil IV.3.
- **Textbaustein:**

```
Übertrittsverfahren strukturell benachteiligt werden, weil Lehrpersonen
```

#### OP-38 Entschärfung „Belastungsfaktor Migrationserfahrung" in FW3-Fliesstext
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Anker (ca. Zeile 1293–1296): `Die Migrationserfahrung selbst ist ein Belastungsfaktor: der Verlust sozialer Netzwerke,` `mögliche traumatisierende Erfahrungen im Herkunftsland, die sprachliche Isolation in der` `neuen Umgebung und die fehlende schulische Anschlussfähigkeit wirken kumulativ auf die` `Begabungsentwicklung \parencite{behrensen2019inklusive,stamm2012migranten}.`.
- **Art des Eingriffs:** Textersatz (Umformulierung zu „kumulative Belastungen im Sinne Behrensens").
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil II.3 (Belastungserfahrung → kumulative Belastung im Sinne Behrensens), Teil IV.3.
- **Textbaustein:**

```
Die Migrationserfahrung bringt kumulative Belastungen im Sinne Behrensens~2019
mit sich: nicht individuelle Pathologie des Kindes, sondern Überlagerung
strukturell-biographischer Faktoren wie Verlust sozialer Netzwerke, mögliche
belastende Vorerfahrungen im Herkunftsland, sprachliche Isolation in der
neuen Umgebung und fehlende schulische Anschlussfähigkeit. Diese
Überlagerung wirkt kumulativ auf die Begabungsentwicklung
\parencite{behrensen2019inklusive,stamm2012migranten}.
```

#### OP-39 Kapitelüberblick Frage 3 „Belastungsperspektive" präzisieren
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Anker (ca. Zeile 1264): `Das Kapitel arbeitet mit Anerkennungstheorie, Belastungsperspektive und Inklusionsverständnis:`.
- **Art des Eingriffs:** Textersatz (Präzisierung).
- **Abhängigkeiten:** OP-38
- **Koordinationshinweis:** keiner
- **Begründung:** Teil IV.3 (Belastung strukturell, nicht individuell).
- **Textbaustein:**

```
Das Kapitel arbeitet mit Anerkennungstheorie, der Perspektive kumulativer
Belastung im Sinne Behrensens~2019 und Inklusionsverständnis:
```

#### OP-40 Einleitungs-Kapitelüberblick „eher defizitär gesehen" entschärfen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Anker (ca. Zeile 316): `sozial wenig eingebunden, wird eher defizitär gesehen~-- und gleichzeitig zeigt er im SOLUX-Projekt`.
- **Art des Eingriffs:** Textersatz (Passiv-Regel aus Teil IV.3).
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil IV.3 (defizitäre Zuschreibungen im Passiv, Deutungsmuster statt Eigenschaft).
- **Textbaustein:**

```
sozial wenig eingebunden, wird durch defizitorientierte Deutungsmuster wahrgenommen, und gleichzeitig zeigt er im SOLUX-Projekt
```
- **Ausführungshinweise:** Geviertstrich `~--` wird durch Komma ersetzt (Schweizer Hochdeutsch, Teil IV.3 Grundsatz 1).

#### OP-41 Einleitung „defizitäre Haltung" → „defizitorientierte Deutungsmuster"
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Anker (ca. Zeile 377–378): `gestalten, Lernbarrieren durch barrierearme Zugänge abbauen und das multiprofessionelle` `Team von einer defizitären Haltung in eine ressourcenorientierte Sicht unterstützen.`.
- **Art des Eingriffs:** Textersatz.
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil IV.3.
- **Textbaustein:**

```
Team von defizitorientierten Deutungsmustern zu ressourcenorientierten Perspektiven zu begleiten.
```

#### OP-42 „Begabungsförderung hat geringe Priorität" einrahmen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Einleitung Ausgangslage, Anker (ca. Zeile 340–342): `Begabungsförderung werden nur von einem Teil der Schulen angeboten, und das` `Thema hat insgesamt geringe Priorität \parencite{dvs2025bbf}.`.
- **Art des Eingriffs:** Textersatz (Einrahmung als eigene Einschätzung im Fallkontext).
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** **Koordinationspunkt Zitat-Audit:** DVS-Aktualitätscheck der Formulierung ist Aufgabe des Zitat-Audit-Agenten; die sprachliche Einrahmung hier ist davon unabhängig.
- **Begründung:** Teil IV.3 (Einleitung-Begabungsförderung-Priorität entschärfen).
- **Textbaustein:**

```
Begabungsförderung werden nur von einem Teil der Schulen angeboten. Im
schulischen Alltag, wie die vorliegende Fallbeobachtung zeigt, ist die
Priorität in der Wahrnehmung der beteiligten Fachpersonen unterschiedlich
\parencite{dvs2025bbf}.
```

#### OP-43 Einleitung `mpv_abgabedokument.tex` parallele Anpassung Ausgangslage-Priorität
- **Zieldatei:** `mpv_abgabedokument.tex`
- **Zielstelle:** Einleitung → Ausgangslage, Anker parallel zu OP-42 (im Abgabedokument bei ca. Zeile 173–177; vor Umsetzung mit Grep `geringe Priorität` lokalisieren).
- **Art des Eingriffs:** Textersatz analog zu OP-42.
- **Abhängigkeiten:** OP-42
- **Koordinationshinweis:** Koordinationspunkt Zitat-Audit wie in OP-42.
- **Begründung:** Teil IV.3, Kohärenz beider Dokumente.
- **Textbaustein:** identisch mit OP-42.

#### OP-44 Einleitungsabsatz Migrationsbegriff in `mpv_abgabedokument.tex`: Begriff „Familiennachzug aus Nicht-EU-Staat" abgleichen
- **Zieldatei:** `mpv_abgabedokument.tex`
- **Zielstelle:** Anker (ca. Zeile 228–239): `\paragraph{Begriffsklärung: Migrationserfahrung.}` … `Der Fall S.\ liegt an der Schnittstelle zwischen Familiennachzug aus einem` `Nicht-EU-Staat und möglicher Fluchterfahrung`.
- **Art des Eingriffs:** Textersatz (Gemeinde Ebikon ergänzen zur Kohärenz mit OP-16).
- **Abhängigkeiten:** OP-16
- **Koordinationshinweis:** keiner
- **Begründung:** Teil I.4 (Migrationsbegriff vollständig, inkl.\ Ebikon-Kontextbedingung).
- **Textbaustein (letzten Satz hinzufügen, nach `über Migrationstypen hinweg greifen \parencite{behrensen2019inklusive,stamm2014handbuch}.`):**

```
Die Gemeinde Ebikon, in der sich der Fall abspielt, zeichnet sich durch
eine sozioökonomisch heterogene Bevölkerung mit einem überdurchschnittlichen
Anteil an Familien mit Migrationsgeschichte aus; diese lokale
Kontextbedingung ist für die schulische Realität mitbestimmend.
```

#### OP-45 Alle Einleitungs-Subsections im `mpv.tex` von `\subsection*` zu `\subsection` konsistent machen (bereits nummeriert)
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Einleitung, Anker (ca. Zeilen 321, 344, 362, 380): `\subsection*{Ausgangslage}`, `\subsection*{Der Fall S.}`, `\subsection*{Heilpädagogischer Bezug}`, `\subsection*{Erkenntnisinteresse und Fragestellungen}`.
- **Art des Eingriffs:** **Prüfung**: Formatierung so belassen wie bisher, falls der Rest der Arbeit ebenfalls `\subsection*` nutzt. Die Operation ist nur auszuführen, falls die übrigen Sections nummerierte `\subsection` verwenden; sonst **verzichten** (Idempotenz-Regel).
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil VI.1 (Kohärenz im Lerndokument; nicht Scope-erweiternd).
- **Textbaustein:** n/a (Prüfoperation)
- **Ausführungshinweise:** Falls die Einleitung als `\section*` (unnumeriert) geführt wird — was aktuell in `mpv.tex` Zeile 223 der Fall ist — ist `\subsection*` konsistent; OP entfällt.

#### OP-46 Textsicherung Ferntransfer-Absatz prüfen und explizite Scharnier-Formulierung einfügen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Frage-2-Kapitel, Unterabschnitt *Schach als Fördermedium*, Anker (ca. Zeile 1026–1038): `Eine wichtige Abgrenzung ist dabei zu treffen: Die kognitionspsychologische` `Forschung zeigt, dass Schachtraining keinen nachweisbaren Ferntransfer` … `keine Ferntransfer-Hypothesen.`.
- **Art des Eingriffs:** **Prüfoperation**. Der Absatz ist inhaltlich korrekt formuliert. Empfohlener **Minimal-Eingriff**: einen Bezeichnungssatz voranstellen, der die „Nahtransfer vs.\ Ferntransfer"-Formel explizit als Merkformel markiert.
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil II.2 (Schach-Ferntransfer-Absatz bereits genügend klar; nur minimale Schärfung), Teil V.1 (mündliche Abrufbarkeit der Formel).
- **Textbaustein (unmittelbar vor `Eine wichtige Abgrenzung ist dabei zu treffen:` einfügen):**

```
Diese Wirkungsweise lässt sich als \textit{Nahtransfer} zusammenfassen:
Die Schachnotation wirkt innerhalb derselben Anforderungssituation, die
sie stützt, nicht über sie hinaus.
```
- **Ausführungshinweise:** Dieser Einschub ist idempotent, weil er unabhängig vom folgenden Text steht; bei Ablehnung dieser Ergänzung durch Inti bleibt der Originalabsatz unverändert gültig.

#### OP-47 Baum/Schader als Primärreferenz im 2e-Unterabschnitt integrieren
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Frage-1-Kapitel, `\subsection{Twice Exceptionality als Deutungsrahmen}` (ca. Zeile 671), Anker im ersten Absatz direkt nach `Das Konzept der \textit{twice exceptionality} (\textit{2e}) beschreibt Kinder, bei denen`.
- **Art des Eingriffs:** Absatzeinschub mit neuer `\parencite{baumschader2021twice}`-Referenz (BibKey noch nicht vorhanden; siehe Koordinationspunkt).
- **Abhängigkeiten:** keine technisch, aber **blockiert durch Zitat-Audit-Agent**, bis BibKey `baumschader2021twice` angelegt ist.
- **Koordinationshinweis:** **Koordinationspunkt mit Zitat-Audit-Agent.** Neuer `@incollection{baumschader2021twice, ...}`-Eintrag (Handbuch Begabung, Kap. S.\ 588–598) muss in `Quellen.bib` angelegt werden. BibKey-Benennung verbindlich `baumschader2021twice`.
- **Begründung:** Teil II.1, Teil IV.2 Nr.\ 7 (Baum/Schader neu aufnehmen, fast zwingend).
- **Textbaustein (Absatzeinschub nach dem ersten Satz des Unterabschnitts):**

```
Die Darstellung von Baum und Schader im Handbuch Begabung expliziert die
doppelte Ausnahmesituation als Überlagerung von hoher kognitiver Fähigkeit
und lern- oder verhaltensbezogenen Erschwernissen, die sich wechselseitig
maskieren können \parencite{baumschader2021twice}. Für den Fall~S. dient
dieser Rahmen ausdrücklich nicht als Diagnose, sondern als heuristische
Denkfolie, die verhindert, dass Stärken und Schwierigkeiten sequentiell
statt simultan gelesen werden.
```
- **Ausführungshinweise:** Nach Ausführung durch Zitat-Audit-Agent (BibKey-Anlage) kann diese Operation ohne Linksbruch kompiliert werden. Bis dahin `% TODO OP-47 warten auf baumschader2021twice` als Platzhalter-Kommentar.

#### OP-48 muelleroppliger2021paeddiagnostik im Unterabschnitt *Multiperspektivische und dynamische Erfassung* einbauen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Frage-1-Kapitel, Anker (ca. Zeile 622): `\subsection{Multiperspektivische und dynamische Erfassung}` und der erste Textabsatz unter dieser Überschrift.
- **Art des Eingriffs:** Absatzeinschub am Beginn des Unterabschnitts (2–4 Sätze mit funktionaler Einbettung).
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** **Koordinationspunkt mit Zitat-Audit-Agent:** BibKey `muelleroppliger2021paeddiagnostik` existiert bereits in `Quellen.bib` (verifiziert); Seitenangaben (S.~224–238) delegiert.
- **Begründung:** Teil IV.2 Nr.\ 1 (Phasenmodell vermuten/wahrnehmen/erkennen, Förder- vs.\ Statusdiagnostik).
- **Textbaustein (Absatzeinschub nach Überschrift, vor bestehendem ersten Absatz):**

```
Müller-Oppliger differenziert einen multiperspektivischen diagnostischen
Prozess in die Phasen Vermuten, Wahrnehmen und Erkennen und unterscheidet
Förderdiagnostik von Statusdiagnostik: Erstere rekonstruiert Potenziale
prozessbegleitend unter variierenden Bedingungen, letztere stellt einen
stabilen Merkmalsbefund fest \parencite{muelleroppliger2021paeddiagnostik}.
Für den Fall~S. gilt die Priorität der Förderdiagnostik, weil ein stabiler
Statusbefund unter migrationsbedingten Störfaktoren derzeit nicht valide
gewonnen werden kann.
```

#### OP-49 gauckreimann2021psychdiagnostik im Unterabschnitt *Grenzen sprachlastiger Diagnostik* einbauen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Frage-1-Kapitel, Anker (ca. Zeile 595): `\subsection{Grenzen sprachlastiger Diagnostik}`.
- **Art des Eingriffs:** Absatzeinschub am Beginn des Unterabschnitts.
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** **Koordinationspunkt Zitat-Audit:** BibKey `gauckreimann2021psychdiagnostik` existiert; Seiten (S.~239–251) delegiert.
- **Begründung:** Teil IV.2 Nr.\ 2 (deutschsprachige Fallbelege Aisha/Lea als Pendant zu Mun/Gubbins).
- **Textbaustein (neuer erster Absatz des Unterabschnitts):**

```
Gauck und Reimann dokumentieren an den deutschsprachigen Fallvignetten Aisha
und Lea einen vierschrittigen psychodiagnostischen Prozess, in dem
sprachliche Unsicherheit, Deckeneffekte in Standardtests und
kultursensible Beobachtung gemeinsam erfasst werden
\parencite{gauckreimann2021psychdiagnostik}. Dieser Prozess spiegelt die
Befunde Maehlers zur sprach- und kulturfairen Diagnostik
\parencite{maehler2018diagnostik} im Schweizer und deutschen Schulkontext
und liefert eine deutschsprachige Referenz für das im internationalen
Diskurs breiter entwickelte Mehrebenenverfahren.
```

#### OP-50 stahl2021mbet im Unterabschnitt *Multiperspektivische und dynamische Erfassung* einbauen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Frage-1-Kapitel, `\subsection{Multiperspektivische und dynamische Erfassung}`, nach OP-48-Einschub.
- **Art des Eingriffs:** Absatzeinschub (mBET als konkretes Instrument).
- **Abhängigkeiten:** OP-48
- **Koordinationshinweis:** **Koordinationspunkt Zitat-Audit:** BibKey `stahl2021mbet` existiert.
- **Begründung:** Teil IV.2 Nr.\ 3.
- **Textbaustein:**

```
Als konkretes Instrument der Multiperspektivität etabliert das Münchner
Begabungstestsystem mBET eine strukturierte Triangulation zwischen
Lehrperson, Eltern und Lernenden \parencite{stahl2021mbet}. Im Fall~S.
wäre mBET, kombiniert mit nonverbalen Testanteilen und einer
dolmetschergestützten Elternrückmeldung, ein Beispiel dafür, wie eine
schulpsychologische Abklärung um mehrere Perspektiven erweitert werden
kann, ohne die sprachliche Schlagseite des Einzeltests zu replizieren.
```

### P2 Operationen Fortsetzung

(Fortsetzung ab OP-51)

#### OP-51 „Institutionelle Diskriminierung" durchgängig mit Kappus-Zusatz einrahmen (Einleitung)
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Einleitung, Anker (ca. Zeile 368): `Under-Identifikation, defizitorientierter Deutungsmuster und institutioneller Diskriminierung` (nach OP-20).
- **Art des Eingriffs:** Textergänzung (Zusatz `im Sinne Kappus~2010` nach „Diskriminierung").
- **Abhängigkeiten:** OP-20
- **Koordinationshinweis:** keiner
- **Begründung:** Teil IV.3 (Einleitung/FW1 Institutionelle Diskriminierung immer mit Kappus-Zusatz versehen).
- **Textbaustein:**

```
Under-Identifikation, defizitorientierter Deutungsmuster und
institutioneller Diskriminierung im Sinne Kappus~2010
```

#### OP-52 Abgabedokument: Einleitung „defizitärer Zuschreibungen" parallel entschärfen
- **Zieldatei:** `mpv_abgabedokument.tex`
- **Zielstelle:** Anker (ca. Zeile 203–204, Abschnitt *Heilpädagogischer Bezug*): `Under-Identifikation, defizitärer Zuschreibungen und institutioneller Diskriminierung`.
- **Art des Eingriffs:** Textersatz analog zu OP-20 und OP-51.
- **Abhängigkeiten:** OP-20, OP-51
- **Koordinationshinweis:** keiner
- **Begründung:** Teil IV.3, Kohärenz beider Dokumente.
- **Textbaustein:**

```
Under-Identifikation, defizitorientierter Deutungsmuster und
institutioneller Diskriminierung im Sinne Kappus~2010
```

#### OP-53 Abgabedokument: „defizitären Haltung" parallel ersetzen
- **Zieldatei:** `mpv_abgabedokument.tex`
- **Zielstelle:** Anker (ca. Zeile 212–213): `Team von einer defizitären Haltung in eine ressourcenorientierte Sicht unterstützen.`.
- **Art des Eingriffs:** Textersatz analog zu OP-41.
- **Abhängigkeiten:** OP-41
- **Koordinationshinweis:** keiner
- **Begründung:** Teil IV.3.
- **Textbaustein:** identisch mit OP-41.

#### OP-54 Fall-S.-Absatz: „mögliche belastende Vorerfahrungen" beibehalten, Umgebung glätten
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Einleitung → *Heilpädagogischer Bezug*, Anker (ca. Zeile 365–368): `überlagern: kognitives Potenzial, das durch den am Anfang stehenden Zweitspracherwerb,` `schriftsprachliche Schwierigkeiten, graphomotorische Hürden und mögliche belastende` `Vorerfahrungen teilweise verdeckt bleibt.`.
- **Art des Eingriffs:** **Prüfoperation** / minimaler Textersatz nur falls tatsächlich die Formel „mögliche belastende Vorerfahrungen" irgendwo kollidiert; Referenzplan bestätigt Formulierung explizit als angemessen.
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil IV.3 (*mögliche belastende Vorerfahrungen* ist fachlich angemessen, beibehalten).
- **Textbaustein:** n/a (Operation besteht in der Entscheidung „nicht ändern"; Begründung wird als Kommentar neben Ort vermerkt).

#### OP-55 Kapitelüberblick Frage 2: Wort „sensomotorisch-kognitiver Prozess" Prüfung
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Anker (ca. Zeile 833): `komplexer sensomotorisch-kognitiver Prozess`.
- **Art des Eingriffs:** **Prüfoperation**: bestehende Formulierung bereits konform mit Globalregel G-01. Keine Änderung nötig.
- **Abhängigkeiten:** OP-19
- **Koordinationshinweis:** keiner
- **Begründung:** Idempotenzprinzip; Operation dokumentiert, dass OP-19 hier keine Änderung triggert.
- **Textbaustein:** n/a.

#### OP-56 Kapitelüberblick Frage 4 Gesamtüberblick-Box aktualisieren
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Kapitelüberblick-Box [Prüfungsstrategie: Gesamtüberblick], Anker (ca. Zeile 308): `\textbf{Frage 5:} Wie handle ich professionell mit anderen zusammen?\\`.
- **Art des Eingriffs:** **Prüfoperation** (bleibt). Keine Änderung nötig, wenn Frage-5-Kernformulierung unverändert.
- **Abhängigkeiten:** OP-12
- **Koordinationshinweis:** keiner
- **Begründung:** Dokumentation, dass Zeile 308 nach OP-30 nicht angefasst wird.
- **Textbaustein:** n/a.

#### OP-57 Fragestellung FW3 im Enumerate `mpv.tex` minimaler Schliff (Kohärenzprüfung)
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Anker (ca. Zeile 399–401): `\item[\textbf{FW\,3 (PB)}] Welche relationalen und strukturellen Bedingungen` `ermöglichen die Sichtbarkeit und Entfaltung von Begabung bei Schüler:innen` `mit Migrationserfahrung?`.
- **Art des Eingriffs:** Textersatz (Begabung → Potenzialen gemäss Regel I.3; Ergänzung um Anerkennung/Teilhabe zur Kohärenz mit OP-09).
- **Abhängigkeiten:** OP-09
- **Koordinationshinweis:** keiner
- **Begründung:** Teil I.3, Teil II.3.
- **Textbaustein:**

```
  \item[\textbf{FW\,3 (PB)}] Welche relationalen und strukturellen Bedingungen
    ermöglichen die Sichtbarkeit und Entfaltung von Potenzialen bei
    Schüler:innen mit Migrationserfahrung, und wie lassen sich
    Anerkennungserfahrungen und Teilhabe gestalten?
```

#### OP-58 Fragestellung FW3 im Enumerate `mpv_abgabedokument.tex` analog schärfen
- **Zieldatei:** `mpv_abgabedokument.tex`
- **Zielstelle:** Anker (ca. Zeile 258–260): `\item[\textbf{FW\,3 (PB)}] Welche relationalen und strukturellen Bedingungen` `ermöglichen die Sichtbarkeit und Entfaltung von Begabung bei Schüler:innen` `mit Migrationserfahrung?`.
- **Art des Eingriffs:** Textersatz analog zu OP-57.
- **Abhängigkeiten:** OP-09, OP-57
- **Koordinationshinweis:** keiner
- **Begründung:** Teil I.3, Teil II.3.
- **Textbaustein:** identisch mit OP-57.

#### OP-59 Fragestellung FW3 im Quote-Block `mpv_abgabedokument.tex` abgleichen
- **Zieldatei:** `mpv_abgabedokument.tex`
- **Zielstelle:** Anker (ca. Zeile 351–354): `\begin{quote}\itshape` `Welche relationalen und strukturellen Bedingungen ermöglichen die Sichtbarkeit` `und Entfaltung von Begabung bei Schüler:innen mit Migrationserfahrung?`.
- **Art des Eingriffs:** Textersatz gemäss OP-09.
- **Abhängigkeiten:** OP-09
- **Koordinationshinweis:** keiner
- **Begründung:** Teil I.3, Teil II.3.
- **Textbaustein:** identisch mit OP-09.

#### OP-60 Einleitungsabsatz zur Progression `mpv.tex` Begabung → Potenzial
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Anker (ca. Zeile 412–418): `Die fünf Fragestellungen folgen einer Progression: von der multiperspektivischen` `Erkennung verdeckter Potenziale (FW\,1) über die sensomotorischen und` `schriftsprachlichen Barrieren, die diese Potenziale verdecken (FW\,2), und die` `relationalen und strukturellen Bedingungen der Begabungsentfaltung (FW\,3) bis` `zu den Settings inklusiver Begabungsförderung, die Potenziale sichtbar machen` `(BW\,4), und dem professionellen Handeln der SHP im multiprofessionellen Team` `(BW\,5).`.
- **Art des Eingriffs:** Wird durch OP-01 (kompletter Absatzersatz) überschrieben. **Operation entfällt**, wenn OP-01 ausgeführt.
- **Abhängigkeiten:** OP-01
- **Koordinationshinweis:** keiner
- **Begründung:** Kohärenz; Idempotenz-Dokumentation.
- **Textbaustein:** n/a.

---

### P3 Operationen (fakultativ oder nach Abgabe)

#### OP-61 preckel2021tad in *Begabung als dynamisches Potenzial* einbauen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Frage-1-Kapitel, Anker (ca. Zeile 504): `\subsection{Begabung als dynamisches Potenzial}` und folgender Absatz.
- **Art des Eingriffs:** Absatzeinschub (TAD-Framework, vier Phasen der Talententwicklung).
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** **Koordinationspunkt Zitat-Audit:** BibKey `preckel2021tad` existiert. Seiten S.~274–303 delegiert.
- **Begründung:** Teil IV.2 Nr.\ 4.
- **Textbaustein:**

```
Preckel und Kolleginnen entfalten im TAD-Framework (Talent Development
Framework) die Talententwicklung in vier Phasen, in denen sich Potenzial
über die Zeit in Leistung transformiert, bedingt durch Lern- und
Umweltbedingungen und durch individuelle Entwicklungsprozesse
\parencite{preckel2021tad}. Dieses dynamische Verständnis legitimiert die
hier eingenommene Lesart: Begabung wird als Verlaufsgrösse gedacht, nicht
als stabile Eigenschaft, und der Fall~S.\ befindet sich in einer frühen
Phase, in der Potenziale durch Kontextbedingungen erst zur Darstellung
kommen.
```

#### OP-62 stadelmann2021begabungsentwicklung in *Begabung als dynamisches Potenzial* einbauen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Frage-1-Kapitel, `\subsection{Begabung als dynamisches Potenzial}`, nach OP-61.
- **Art des Eingriffs:** Absatzeinschub (neuropsychologische Unterfütterung Stern-Position).
- **Abhängigkeiten:** OP-61
- **Koordinationshinweis:** **Koordinationspunkt Zitat-Audit:** BibKey `stadelmann2021begabungsentwicklung` existiert. Seiten S.~133–147 delegiert.
- **Begründung:** Teil IV.2 Nr.\ 6.
- **Textbaustein:**

```
Stadelmann ergänzt diesen Zugang aus neuropsychologischer Perspektive:
Kognitive Potenziale reifen in Abhängigkeit von neuronaler Plastizität
und Erfahrungsangeboten, was eine entwicklungssensitive Diagnostik statt
einer Momentaufnahme erforderlich macht \parencite{stadelmann2021begabungsentwicklung}.
Für S. bedeutet das, dass die unter sprachlichen Erschwernissen gewonnenen
Testwerte weniger sein kognitives Potenzial abbilden als den Zustand einer
frühen Adaptationsphase.
```

#### OP-63 renzullireis2021rls in BW4 als primäre SEM-Referenz einbauen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Frage-4-Kapitel, Anker (ca. Zeile 1698–1704): `Das Schoolwide Enrichment Model (SEM) nach Renzulli bildet den zentralen` `Referenzrahmen. Es unterscheidet drei Enrichment-Typen` … `\parencite{muelleroppliger2021handbuch,fischer2020begabungsfoerderung,trautmann2016einfuehrung}.`.
- **Art des Eingriffs:** Cite-Ergänzung (**kollidiert mit Zitat-Audit-Rewrites**; siehe REWRITES.md L:1689 und L:1765).
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** **Koordinationspunkt Zitat-Audit (Konflikt):** `REWRITES.md` enthält bereits pending Rewrites an L:1689 und L:1755 (rewrite `fischer2020begabungsfoerderung` → `renzullireis2021rls`). Diese Operation **muss nach** Abschluss des Zitat-Audit-Rewrites ausgeführt werden, um Doppeländerungen zu vermeiden. Empfehlung: **Operation entfällt** und wird vollständig durch den Zitat-Audit-Rewrite abgedeckt.
- **Begründung:** Teil IV.2 Nr.\ 5, Teil III.2 Redundanzen.
- **Textbaustein:** n/a (delegiert).
- **Ausführungshinweise:** Nach Audit-Abschluss Grep `renzullireis2021rls` in `mpv.tex` auf mindestens zwei Treffer verifizieren.

#### OP-64 Müller-Oppliger-Kapitelverweise spezifizieren (Handbuch-Begabung-Feinaufschlüsselung)
- **Zieldatei:** `mpv.tex`, `mpv_abgabedokument.tex`
- **Zielstelle:** Alle `\parencite{muelleroppliger2021handbuch}`-Vorkommen, die inhaltlich spezifische Kapitel betreffen (siehe REWRITES.md-Einträge L:449, 504, 800, 874, 1026, 1689, 1765).
- **Art des Eingriffs:** Cite-Key-Umstellung (pauschaler Band → spezifisches Kapitel).
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** **Koordinationspunkt Zitat-Audit:** Diese Umstellungen sind **bereits vollständig** in [REWRITES.md](REWRITES.md) als 7 pending Rewrites dokumentiert. **Operation entfällt** und wird durch den Zitat-Audit-Agenten ausgeführt.
- **Begründung:** Teil III.2 (APA-Konformität Sammelbandbeiträge).
- **Textbaustein:** n/a (delegiert).

#### OP-65 trautmann2021haltung in BW5 fakultativ einbauen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Frage-5-Kapitel, geeignete Einbaustelle im Unterabschnitt zur professionellen Haltung (mit Grep `professionelle Haltung|reflexive Partnerschaftlichkeit` zu lokalisieren).
- **Art des Eingriffs:** Absatzeinschub oder Cite-Ergänzung.
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** **Koordinationspunkt Zitat-Audit:** BibKey `trautmann2021haltung` existiert, Seiten S.~496–510 delegiert.
- **Begründung:** Teil IV.2 fakultativ (nicht zwingend, weil Burow diese Funktion bereits erfüllt).
- **Textbaustein:** 2–3 Sätze, nur auszuführen auf ausdrückliche Intis-Entscheidung. **Standard-Empfehlung: nicht ausführen**.

#### OP-66 horvath2021elite in der Einleitung oder BW4 fakultativ einbauen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Einleitung → *Ausgangslage* (Gerechtigkeitsargument) oder Frage-4-Kapitel.
- **Art des Eingriffs:** Absatzeinschub fakultativ.
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** **Koordinationspunkt Zitat-Audit:** BibKey existiert; Seiten S.~77–86 delegiert.
- **Begründung:** Teil IV.2 fakultativ (starke Ergänzung zum Gerechtigkeitsargument).
- **Textbaustein:** n/a (nur bei ausdrücklicher Intis-Entscheidung).

#### OP-67 grabnermeier2021expertise in FW2 fakultativ einbauen
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Frage-2-Kapitel, geeigneter Unterabschnitt zur Expertiseentwicklung.
- **Art des Eingriffs:** Absatzeinschub fakultativ.
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** Koordinationspunkt Zitat-Audit.
- **Begründung:** Teil IV.2 fakultativ (nur falls 10 000-Stunden-Regel explizit thematisiert wird).
- **Textbaustein:** n/a (fakultativ, nicht empfohlen).

#### OP-68 Frage-5 alternative Schärfung (Übertritt-Fokus) fakultativ
- **Zieldatei:** `mpv.tex`, `mpv_abgabedokument.tex`
- **Zielstelle:** Frage-5-Enumerate (ca. Zeile 406–409 in `mpv.tex`) und Quote-Block (ca. Zeile 2095–2100 in `mpv.tex`), analog in Abgabedokument (ca. Zeile 265–268 und 413–417).
- **Art des Eingriffs:** Textersatz (alternative Formulierung mit Übertrittsfokus).
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil II.5 (alternative Schärfung fakultativ; bisherige Formulierung bleibt als Standard).
- **Textbaustein (Quote-Block):**

```
\begin{quote}\itshape
Wie gestaltet die SHP Beratung, Elternarbeit und Zusammenarbeit im
multiprofessionellen Team so, dass die in offenen Settings sichtbar
gewordenen Potenziale neu zugewanderter Schüler:innen institutionell
gesichert und in den Übertritt überführt werden?
\end{quote}
```
- **Ausführungshinweise:** **Standard-Empfehlung: nicht ausführen** (Verengung aus Teil II.5 beibehalten). Operation nur bei ausdrücklicher Intis-Entscheidung.

#### OP-69 BW5-Kapitelüberblick erweitern
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Kapitelüberblick Frage 5, bestehender Text (ca. Zeile 2102–2104).
- **Art des Eingriffs:** Absatzergänzung mit Transferrede-Kurzform.
- **Abhängigkeiten:** OP-28
- **Koordinationshinweis:** keiner
- **Begründung:** Teil II.5 (Transferrede auf Kapitelüberblick spiegeln, P3 gemäss Referenzplan).
- **Textbaustein (einfügen nach OP-28-Textbaustein vor `\end{kapitelueberblick}`):**

```
\medskip\textbf{Transfer in andere Gruppen:} Die Beratungsprinzipien
fachliche Unabhängigkeit, reflexive Partnerschaftlichkeit und
institutionelle Wachsamkeit sind grundsätzlich übertragbar. Sie gelten
bei neu zugewanderten Kindern mit besonderer Schärfe, weil dort
institutionelle Intransparenz kumulativ wirkt.
```

#### OP-70 LaTeX-Switch `\newif\ifLernversion` in der Präambel einführen
- **Zieldatei:** `mpv.tex` (Lerndokument; Abgabedokument bleibt zunächst separat)
- **Zielstelle:** Präambel, nach `\usepackage{etoolbox}` (ca. Zeile 22).
- **Art des Eingriffs:** LaTeX-Strukturänderung (Präambel-Schalter).
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** keiner
- **Begründung:** Teil VI.1 (Switch `\newif\ifLernversion` für gemeinsame Pflege).
- **Textbaustein (unmittelbar nach `\usepackage{etoolbox}`):**

```
% Switch Lerndokument (gelbe Kapitelüberblicke, kritische Reflexionen,
% To-do-Boxen, ergänzende Fachartikel) vs. Abgabedossier (schlank).
\newif\ifLernversion
\Lernversiontrue  % Standard: Lerndokument; für Abgabe auf \Lernversionfalse setzen.
```
- **Ausführungshinweise:** Kompiliert mit TeX Live 2024; keine zusätzlichen Pakete nötig. Siehe OP-71 für die Anwendung auf Inhaltsbereiche.

#### OP-71 Kapitelüberblick-Boxen in `\ifLernversion ... \fi` einklammern
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Alle `\begin{kapitelueberblick} ... \end{kapitelueberblick}`-Umgebungen, ca. Zeilen 295, 315, 432, 832, 1263, 1686, 2102, 2639.
- **Art des Eingriffs:** LaTeX-Strukturänderung (bedingtes Rendering).
- **Abhängigkeiten:** OP-70
- **Koordinationshinweis:** keiner
- **Begründung:** Teil VI.1 (Kapitelüberblicke gehören nicht ins Abgabedossier).
- **Textbaustein (pro Box):**

```
\ifLernversion
\begin{kapitelueberblick}
  ... (bestehender Inhalt) ...
\end{kapitelueberblick}
\fi
```

#### OP-72 Kritische-Reflexion-Subsections in `\ifLernversion ... \fi` einklammern
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Alle `\subsection{Kritische Reflexion: ...}` und die darauffolgenden `\begin{tcolorbox}[...title=Weiterführende Diskurslinie]`-Blöcke bis zum Ende des jeweiligen Diskussionsabschnitts. Ankerzeilen: 729, 1113, 1524, 1945, 2425.
- **Art des Eingriffs:** LaTeX-Strukturänderung (bedingtes Rendering jeweils um den kompletten Unterabschnitt inkl.\ Fliesstext der Diskussion).
- **Abhängigkeiten:** OP-70
- **Koordinationshinweis:** keiner
- **Begründung:** Teil VI.1 (Kritische Reflexionen gehören nicht ins Abgabedossier).
- **Textbaustein:**

```
\ifLernversion
\subsection{Kritische Reflexion: <Titel>}
... (Box + Fliesstext bis vor nächste \section) ...
\fi
```
- **Ausführungshinweise:** Nächste Section-Grenze pro Fall verifizieren (teilweise folgt unmittelbar `\newpage\section{Frage N+1 ...}`; das `\fi` vor `\newpage` schliessen).

#### OP-73 Ergänzende-Fachartikel-Section in `\ifLernversion ... \fi` einklammern
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** Ankerzeile 2599: `\section*{Ergänzende Fachartikel: Empirische Evidenz zur Prüfungsvorbereitung}` bis unmittelbar vor `\section*{Seitenbudget: Übersicht}` (ca. Zeile 3521).
- **Art des Eingriffs:** LaTeX-Strukturänderung.
- **Abhängigkeiten:** OP-70
- **Koordinationshinweis:** keiner
- **Begründung:** Teil VI.1.
- **Textbaustein:**

```
\ifLernversion
\section*{Ergänzende Fachartikel: Empirische Evidenz zur Prüfungsvorbereitung}
... (gesamter Fachartikel-Abschnitt bis vor \section*{Seitenbudget: Übersicht}) ...
\fi
```

#### OP-74 To-do-Boxen in `\ifLernversion ... \fi` einklammern
- **Zieldatei:** `mpv.tex`
- **Zielstelle:** `\begin{todomai} ... \end{todomai}` (ca. Zeile 227–258) und `\begin{todojuni} ... \end{todojuni}` (ca. Zeile 260–293).
- **Art des Eingriffs:** LaTeX-Strukturänderung.
- **Abhängigkeiten:** OP-70
- **Koordinationshinweis:** keiner
- **Begründung:** Teil VI.1 (To-do-Boxen gehören nicht ins Abgabedossier).
- **Textbaustein:**

```
\ifLernversion
\begin{todomai}
  ...
\end{todomai}

\begin{todojuni}
  ...
\end{todojuni}
\fi
```

#### OP-75 Abgabedokument-Variante direkt aus `mpv.tex` erzeugen (optional nach Switch)
- **Zieldatei:** neue Datei `mpv_abgabe.tex` (Wrapper) oder Neuadaption von `mpv_abgabedokument.tex`
- **Zielstelle:** Neu erzeugte Wrapper-Datei, die `\Lernversionfalse` setzt und `mpv.tex` per `\input{mpv.tex}` oder gleichwertig einbindet.
- **Art des Eingriffs:** Strukturelle LaTeX-Änderung (Dateisystem).
- **Abhängigkeiten:** OP-70 bis OP-74
- **Koordinationshinweis:** **Koordinationspunkt Inti:** Diese Umstellung erlaubt die Pflege in einer Quelle und erzeugt zwei PDFs; ob der bestehende Stand `mpv_abgabedokument.tex` (separate gekürzte Kopie) oder der Wrapper bevorzugt wird, entscheidet Inti.
- **Begründung:** Teil VI.1 (gemeinsame Pflege).
- **Textbaustein (Wrapper-Datei `mpv_abgabe.tex`):**

```
\input{mpv_presets.tex}  % falls gemeinsamer Präambelteil ausgelagert wird
\Lernversionfalse
\input{mpv_body.tex}     % falls Inhalt in separater Datei liegt
```
- **Ausführungshinweise:** **Standard-Empfehlung: Wrapper-Umstellung verschieben** (P3). Bis zur Abgabe am 01.05.2026 zwei getrennte Dateien weiterführen und synchron halten; Wrapper ist eine post-Abgabe-Aufgabe.

#### OP-76 Seitenbudget-Tabelle Abgabedokument: Pauschalabzug entfernen (Variante A Light)
- **Zieldatei:** `mpv_abgabedokument.tex`
- **Zielstelle:** Tabelle „Seitenbudget: Übersicht" am Ende, Anker `Konservative Abrundung (Kapitelgrenzen, Inhaltsverz., Bibliographien) & --ca.\,188\,S. \\`.
- **Art des Eingriffs:** Tabellenzeile entfernen und Nettosumme neu rechnen.
- **Abhängigkeiten:** keine
- **Koordinationshinweis:** **Koordinationspunkt Zitat-Audit:** Der Zitat-Audit-Agent verifiziert die Seitenangaben pro Quelle. Die Endsumme hängt davon ab. Empfehlung: **Operation ausführen nach** Abschluss des Zitat-Audits; bis dahin als P3 markiert.
- **Begründung:** Teil VI.2 (Pauschalabzug argumentativ schwach).
- **Textbaustein:** Tabelle rekalkulieren (siehe Globale Regel G-04).

---

## Globale Operationen (Suche und Ersetze)

### G-01 `sensumotorisch` → `sensomotorisch`
- **Regel:** Alle morphologischen Varianten (`sensumotorisch`, `-e`, `-er`, `-en`, `-es`, `Sensumotorische`, `Sensumotorisch-`) im Fliesstext beider Dateien.
- **Ausnahme:** Innerhalb wörtlicher Zitate von Sturm 2016 oder anderer Autor:innen, die die Form explizit verwenden, Originalform beibehalten. Stand 24.04.2026 enthält das Dossier **keine** wörtlichen Sturm-Zitate; daher globales Ersetzen ohne Ausnahmefall möglich.
- **Umsetzungsweg:** LaTeX-konformes Suchen-Ersetzen in `mpv.tex` und `mpv_abgabedokument.tex`.
- **Verifikation:** `rg -n 'sensu' mpv.tex mpv_abgabedokument.tex` liefert nach Abschluss null Treffer.
- **Bezug zu OPs:** OP-11, OP-19, OP-55.
- **Referenz:** Teil II.2.

### G-02 `systematisch (übersehen|verdeckt)` → kontextspezifisch entschärfen
- **Regel:** Im Fliesstext von **FW3 und BW4** die Kombinationen `systematisch übersehen`, `systematische Unsichtbarkeit`, `systematisch verdeckt`, `systematisch verzerrt`, `systematisch benachteiligt` durch kontextangemessene Formulierungen ersetzen: `leicht verdeckt`, `strukturell erschwert erkennbar`, `strukturelle Unsichtbarkeit`, `strukturell benachteiligt`, `strukturell verzerrt`.
- **Ausnahme:** Stellen, an denen `systematisch` explizit auf Stamm~2021 oder Leikhof~2021 als Quelle verweist (z.B.\ `Leikhof zeigt, dass systematisch` in BW5 ca.\ Zeile 2138, `Stamm belegt ... systematisch`). Dort Formulierung beibehalten.
- **Umsetzungsweg:** Pro Treffer Einzelfall-Prüfung, kein blindes Ersetzen. OP-31, OP-32, OP-33, OP-34, OP-35, OP-36, OP-37 decken die konkreten Einzelfälle ab.
- **Verifikation:** Nach Umsetzung der OPs `rg -n 'systematisch' mpv.tex` durchgehen und verbliebene Treffer jeweils explizit als „Stamm/Leikhof-Referenz" oder „bewusst erhalten" markieren.
- **Referenz:** Teil IV.3.

### G-03 `defizitäre Zuschreibungen` / `defizitäre Haltung` → `defizitorientierte Deutungsmuster`
- **Regel:** Wo *defizitär* als Eigenschaft oder Handlungsmuster eingesetzt wird, durch *defizitorientierte Deutungsmuster* ersetzen.
- **Ausnahme:** Wenn `defizitär` innerhalb einer Bewertungsaussage mit Negation steht (z.B.\ `nicht defizitär gelesen, sondern respektiert` Zeile 1281), Formulierung beibehalten.
- **Umsetzungsweg:** Pro Treffer Einzelfall; OP-20, OP-40, OP-41, OP-52, OP-53 konkrete Stellen.
- **Verifikation:** `rg -n 'defizitär' mpv.tex mpv_abgabedokument.tex` und pro Treffer als „ersetzt" oder „bewahrt" markieren.
- **Referenz:** Teil IV.3.

### G-04 Seitenbudget-Tabelle rekalkulieren (Variante A Light)
- **Regel:** Pauschalabzug `Konservative Abrundung – ca.\,188\,S.` aus der Tabelle entfernen; Bruttosumme und Mehrfachzuordnungs-Tabelle belassen, Nettosumme neu ausweisen als `Bruttosumme – 175 – 55 = ca.\,888\,S.` (Hinweis: in `mpv.tex` L:3565ff. und `mpv_abgabedokument.tex` analog; exakte Zeile pro Dokument prüfen).
- **Ausnahme:** Wenn Zitat-Audit die Bruttoangaben pro Quelle revidiert (Variante A gemäss Referenzplan), stattdessen diese neuen Werte einspeisen; Pauschalabzug entfällt dann ohnehin.
- **Umsetzungsweg:** OP-76 (Abgabedokument) und analog in `mpv.tex` (ggf.\ nur im Abgabedokument, falls Lerndokument die Tabelle identisch führt).
- **Verifikation:** Summe der fünf Fragezeilen minus Abzugstabelle = Nettosumme.
- **Referenz:** Teil VI.2.

---

## LaTeX-Strukturoperationen

### S-01 Präambel-Schalter `\newif\ifLernversion`
- Siehe OP-70.

### S-02 Kapitelüberblick-Boxen konditional
- Siehe OP-71.

### S-03 Kritische-Reflexion-Unterabschnitte konditional
- Siehe OP-72.

### S-04 Ergänzende-Fachartikel-Section konditional
- Siehe OP-73.

### S-05 To-do-Boxen konditional
- Siehe OP-74.

### S-06 Wrapper-Abgabedokument (Post-Abgabe-Aufgabe)
- Siehe OP-75.

---

## Koordinationspunkte mit Zitat-Audit-Agent

Die folgenden Operationen berühren Bereiche, die der parallele Zitat-Audit-Agent bearbeitet. Pro Eintrag wird das Handling festgelegt.

| OP | Kurzbeschrieb | Kollision | Auflösung |
|---|---|---|---|
| OP-16 | Einleitung Migrationsbegriff mit `\parencite{bfs2022migration,behrensen2019inklusive,stamm2014handbuch}` | Zitat-Audit prüft Aktualität BFS und stamm2014-Seiten | **Nach** Audit-Abschluss ausführen; Operation selbst ändert nur Fliesstext, nicht BibKey. Wenn Audit BFS-Key umbenennt, `bfs2022migration` durch neuen Key ersetzen. |
| OP-42 / OP-43 | Einleitung DVS-Priorität-Formulierung | Zitat-Audit verifiziert DVS-Stand | Parallel möglich; bei Audit-Ergebnis ggf.\ Formulierung minimal angleichen. |
| OP-47 | Baum/Schader in 2e-Unterabschnitt | **Harter Konflikt:** neuer BibKey `baumschader2021twice` muss in `Quellen.bib` angelegt werden | **Blockiert** bis Zitat-Audit BibKey anlegt; bis dahin als Platzhalter-Kommentar `% TODO OP-47 wartet auf baumschader2021twice`. |
| OP-48–OP-50, OP-61–OP-62 | Handbuch-Begabung-Feinkapitel integrieren | Keine Kollision; BibKeys existieren bereits, nur Seiten-Audit läuft | Parallel ausführbar; Zitat-Audit liefert nach Abgabe präzise Seiten. |
| OP-63 | SEM-Primärreferenz auf `renzullireis2021rls` | **Harter Konflikt:** `REWRITES.md` enthält diesen Rewrite bereits als pending (L:1755) | **Operation entfällt** und wird vollständig durch Audit-Rewrite ausgeführt. |
| OP-64 | Müller-Oppliger-Feinaufschlüsselung | **Harter Konflikt:** 7 pending Rewrites in `REWRITES.md` | **Operation entfällt**, delegiert an Audit. |
| OP-65–OP-67 | Fakultative Handbuch-Kapitel (trautmann2021haltung, horvath2021elite, grabnermeier2021expertise) | Kein harter Konflikt; BibKeys existieren | Nur bei ausdrücklicher Intis-Entscheidung ausführen; Standard: nicht ausführen. |
| OP-76 | Seitenbudget-Tabelle Pauschalabzug entfernen | Zitat-Audit revidiert ggf.\ Bruttoangaben | **Nach** Audit-Abschluss ausführen. |
| Sämtliche `\cite`-/`\parencite`-betreffenden OPs | Dieser Plan **ändert keine Seitenzahlen** in `\cite`-Aufrufen | strikte Abgrenzung | Zitat-Audit-Agent alleinig zuständig für Seiten und bib-Einträge. |

---

## Abdeckungsmatrix

Tabelle: Teil aus `ueberarbeitungsplan_mpv.md` × abdeckende Operationen.

| Referenz | Inhalt | Abdeckende OPs |
|---|---|---|
| Teil I.1 | Sichtbarkeitsformel / Hauptthese, Rückanker FW1/FW3/BW5 | OP-01, OP-02, OP-25, OP-26, OP-28 |
| Teil I.2 | Titel Option A | OP-03, OP-04 |
| Teil I.3 | Begriff Begabung vs.\ Potenzial (Fragen und Titel) | OP-03, OP-04, OP-07, OP-08, OP-14, OP-15, OP-57, OP-58 |
| Teil I.4 | Migrationsbegriffs-Absatz | OP-16, OP-44 |
| Teil I.5 | Fall versus Vignette | OP-17, OP-18 |
| Teil II.1 | Frage 1 neu (Entdopplung) | OP-05, OP-06, OP-07, OP-08 |
| Teil II.2 | Frage 2 Terminologie und Schach | OP-11, OP-19, OP-21, OP-22, OP-23, OP-24, OP-46, OP-55, Globalregel G-01 |
| Teil II.3 | Frage 3 Widerspruchsauflösung | OP-09, OP-10, OP-26, OP-29, OP-38, OP-39, OP-57, OP-58, OP-59 |
| Teil II.4 | Frage 4 Abgrenzung FW1 + „systematisch" entschärfen | OP-12, OP-13, OP-14, OP-15, OP-27, OP-30, OP-32, OP-33, OP-34, OP-35, OP-36, OP-37, Globalregel G-02 |
| Teil II.5 | Frage 5 Verengung beibehalten, Transferrede | OP-28 (Kapitelüberblick-Rückanker), OP-69 (P3 Transferrede-Kurzform), OP-68 (fakultative Alternative) |
| Teil II.6 | Progressionsabsatz mit Sichtbarkeitsformel | OP-01, OP-02 (OP-60 markiert dokumentiert als „durch OP-01 abgedeckt") |
| Teil III.1 | Funktionenregister (nur Prüfungsvorbereitung, nicht LaTeX-Scope) | *nicht im Scope dieses Plans* (Teil VII analog delegiert an Inti) |
| Teil III.2 | Müller-Oppliger-Feinaufschlüsselung | delegiert OP-64 (→ `REWRITES.md`) |
| Teil IV.1 | Seitenzahl-Verifikationen | **delegiert an Zitat-Audit-Agent** |
| Teil IV.2 | Handbuch-Begabung-Kapitel | OP-47 (P2, Baum/Schader), OP-48, OP-49, OP-50, OP-61, OP-62; fakultativ OP-65, OP-66, OP-67 |
| Teil IV.3 | Formulierungen entschärfen | OP-20, OP-31–OP-38, OP-40, OP-41, OP-42, OP-43, OP-51, OP-52, OP-53, Globalregeln G-02 und G-03 |
| Teil IV.4 | Aktualitätschecks BFS/DVS/PISA | **delegiert an Zitat-Audit-Agent**; Fliesstext-Einrahmung durch OP-42, OP-43 |
| Teil IV.5 | A-/B-/C-Korpus | **delegiert an Zitat-Audit-Agent** (bib-Ebene) und OP-73 (Ausklammern Fachartikel für Abgabe) |
| Teil V.1 | Schach kein Ferntransfer (mündlich) | OP-46 (minimale textuelle Präzisierung); Teil V.1 als mündliche Defensive bleibt bei Inti |
| Teil V.2–V.4 | Mündliche Defensiv-Strategien | *nicht im Scope dieses Plans* |
| Teil VI.1 | LaTeX-Switch für Lern- vs.\ Abgabedokument | OP-70, OP-71, OP-72, OP-73, OP-74, OP-75 (P3, Post-Abgabe) |
| Teil VI.2 | Seitenbudget Variante A | OP-76, Globalregel G-04 |
| Teil VI.3 | Quellen-Stichprobe | **delegiert an Zitat-Audit-Agent** |
| Teil VII | Prüfungsvorbereitung (Visualisierungen, Karteikarten) | *nicht im Scope dieses Plans* (explizite Abgrenzung im Vorwort) |

---

## Ausdrücklich nicht adressierte Punkte

| Punkt | Grund |
|---|---|
| Seitenzahlen in `\cite`/`\parencite` | Zuständigkeit Zitat-Audit-Agent |
| VERIFY-/TODO-Marker in `Quellen.bib` | Zuständigkeit Zitat-Audit-Agent |
| Brunner-Auflage 2021 vs.\ 2005 | Zuständigkeit Zitat-Audit-Agent (E5 in ENTSCHEIDUNGEN.md) |
| BFS-Aktualität, DVS-Website-Stand, PISA-2022-Updates | Zuständigkeit Zitat-Audit-Agent |
| Bibliographie-Neueinträge | Abgelehnt, ausser OP-47 Baum/Schader als Koordinationspunkt |
| Funktionenregister (Teil III.1) | Mündliche Prüfungsvorbereitung, kein Textartefakt im Dossier |
| Visualisierungen (Teil VII.1) | Mündliche Prüfungsvorbereitung, eigene Arbeitsspur nach Abgabe |
| Drei-Satz-Strukturen (Teil VII.2) | Mündliche Prüfungsvorbereitung |
| Karteikarten für Fachartikel (Teil VII.3) | Mündliche Prüfungsvorbereitung |
| Kondensierung auf 6–7 Minuten (Teil VII.4) | Mündliche Prüfungsvorbereitung |
| Defensiv-Strategien (Teil V.2 bis V.4) | Mündliche Ebene, Sache Intis |
| Seitenangaben-Verifikation E1 Fall S., E3 Begriff Potenzial, E6 Budget-Ebene | Bereits in ENTSCHEIDUNGEN.md dokumentiert; Inti-Entscheidungen getroffen, Umsetzung durch OPs 03, 04, 16, 42–44 |
| Stilistische Korrekturen ausserhalb der oben genannten Regeln | Scope-Grenze: Schärfung, nicht Umstilisierung (vgl.\ Vorwort) |

---

## Reihenfolge der Ausführung

### Session 1: Strategische Grundsätze (ca. 90 Minuten)

1. OP-70 (Präambel-Switch)
2. OP-71 (Kapitelüberblick-Boxen konditional)
3. OP-72 (Kritische-Reflexion konditional)
4. OP-73 (Ergänzende-Fachartikel konditional)
5. OP-74 (To-do-Boxen konditional)
6. OP-03 (Titel `mpv.tex`)
7. OP-04 (Titel `mpv_abgabedokument.tex`)

### Session 2: Fragen-Neuformulierungen (ca. 90 Minuten)

8. OP-05 (FW1 Quote `mpv.tex`)
9. OP-06 (FW1 Quote `mpv_abgabedokument.tex`)
10. OP-07 (FW1 Enumerate `mpv.tex`)
11. OP-08 (FW1 Enumerate `mpv_abgabedokument.tex`)
12. OP-09 (FW3 Quote `mpv.tex`)
13. OP-10 (FW3 Section-Heading `mpv.tex`)
14. OP-57 (FW3 Enumerate `mpv.tex`)
15. OP-58 (FW3 Enumerate `mpv_abgabedokument.tex`)
16. OP-59 (FW3 Quote `mpv_abgabedokument.tex`)
17. OP-12 (BW4 Quote `mpv.tex`)
18. OP-13 (BW4 Quote `mpv_abgabedokument.tex`)
19. OP-14 (BW4 Enumerate `mpv.tex`)
20. OP-15 (BW4 Enumerate `mpv_abgabedokument.tex`)
21. OP-21–OP-24 (FW2 optional schärfen, 4 OPs)

### Session 3: Einleitung und Sichtbarkeitsformel (ca. 60 Minuten)

22. OP-16 (Einleitung Migrationsbegriff `mpv.tex`)
23. OP-44 (Abgabedokument Migrationsbegriff Ebikon ergänzen)
24. OP-17 (Fall-Vignette `mpv.tex`)
25. OP-18 (Fall-Vignette `mpv_abgabedokument.tex`)
26. OP-01 (Sichtbarkeitsformel `mpv.tex`)
27. OP-02 (Sichtbarkeitsformel `mpv_abgabedokument.tex`)
28. OP-29 (Gesamtüberblick Frage 3 Paraphrase)
29. OP-30 (Gesamtüberblick Frage 4 Paraphrase)
30. OP-25 (Kapitelüberblick Frage 1 Rückanker)
31. OP-26 (Kapitelüberblick Frage 3 Rückanker + Präzisierung)
32. OP-27 (Kapitelüberblick Frage 4 Abgrenzung)
33. OP-28 (Kapitelüberblick Frage 5 Rückanker)

### Session 4: Entschärfungen und Globale Operationen (ca. 60 Minuten)

34. OP-19 / G-01 (sensomotorisch global)
35. OP-11 (Section-Heading Frage 2)
36. OP-20 (defizitär Einleitung)
37. OP-41 (defizitäre Haltung Einleitung)
38. OP-40 (Kapitelüberblick Einleitung defizitär im Passiv)
39. OP-52 (Abgabedokument defizitär parallel)
40. OP-53 (Abgabedokument defizitäre Haltung parallel)
41. OP-38 (Belastungsfaktor FW3)
42. OP-39 (Kapitelüberblick FW3 Belastungsperspektive präzisieren)
43. OP-31 (systematisch FW1)
44. OP-32 (systematisch FW3/BW4-Übergang)
45. OP-33 (systematische Unsichtbarkeit BW4)
46. OP-34 (Homogenitätslogik Subsection)
47. OP-35 (Homogenitätslogik Fliesstext)
48. OP-36 (Zuschreibungen BW4)
49. OP-37 (Übertrittsverfahren BW4)
50. OP-51 (Kappus-Zusatz Einleitung)
51. OP-42 (DVS-Priorität Einleitung)
52. OP-43 (Abgabedokument DVS-Priorität)

### Session 5: Handbuch-Begabung-Integrationen (ca. 90 Minuten, P3)

53. OP-47 (Baum/Schader — blockiert bis Zitat-Audit BibKey anlegt)
54. OP-48 (muelleroppliger2021paeddiagnostik)
55. OP-49 (gauckreimann2021psychdiagnostik)
56. OP-50 (stahl2021mbet)
57. OP-61 (preckel2021tad)
58. OP-62 (stadelmann2021begabungsentwicklung)
59. OP-46 (Ferntransfer minimale Schärfung)
60. OP-69 (BW5-Kapitelüberblick Transfer-Ergänzung)

### Session 6: Post-Abgabe (nach 01.05.2026)

61. OP-63 (delegiert an Zitat-Audit)
62. OP-64 (delegiert an Zitat-Audit)
63. OP-65, OP-66, OP-67 (fakultativ, nur auf Intis Entscheidung)
64. OP-68 (alternative Schärfung Frage 5, nicht empfohlen)
65. OP-75 (Wrapper-Umstellung Lern-/Abgabedokument)
66. OP-76 (Seitenbudget nach Audit-Abschluss)

### Verifikationen (am Ende jeder Session)

- Nach Session 1: `pdflatex mpv.tex` kompilierbar, `\ifLernversion`-Logik visuell geprüft.
- Nach Session 2: Grep `Begabungen bei neu zugewanderten, mehrsprachigen Schüler:innen mit geringen` liefert null Treffer in beiden Dateien.
- Nach Session 3: Grep `Die fünf Fragestellungen folgen einer Progression` liefert in `mpv.tex` einen Treffer und in `mpv_abgabedokument.tex` einen Treffer; beide im neuen Wortlaut.
- Nach Session 4: Grep `sensu` liefert null Treffer. Grep `systematisch (übersehen|verdeckt)` nur noch in Stamm-/Leikhof-Kontexten.
- Nach Session 5: Grep `muelleroppliger2021paeddiagnostik|gauckreimann2021psychdiagnostik|stahl2021mbet|preckel2021tad|stadelmann2021begabungsentwicklung|baumschader2021twice` liefert pro Key mindestens einen Treffer.
- Finalverifikation: `pdflatex && biber && pdflatex && pdflatex` auf beiden Dokumenten ohne Warnungen, LaTeX-Log auf Undefined References scannen.
