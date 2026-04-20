# Anleitung für Inti – Manuelle Arbeiten an der MPV-Abgabe

_Stand: 20. April 2026 · Autor: Pascal_

Hallo Inti 👋

Dieses Dokument erklärt dir **genau**, was du ohne KI-Hilfe beitragen kannst.
Du brauchst dafür nur:

- einen **Texteditor** (VS Code ist schon installiert, aber auch Word/Notepad++ geht),
- einen **PDF-Viewer** (Adobe Reader, Chrome, Edge …),
- einen **Browser** für Online-Recherche (Swisscovery, Google Scholar),
- **keine Programmiersprache**, **keinen Terminal**, **keine KI**.

Alles, was du unten machst, sind **Lese-, Recherche- und kleine Text-Edit-Aufgaben**.

---

## 1. Worum geht es überhaupt?

Pascal schreibt seine **Vertiefungsarbeit für den MAS-Heilpädagogik**.
Am **1. Mai 2026** wird das finale **Abgabedokument** eingereicht. Parallel führt er
ein viel ausführlicheres **Lerndokument** für die mündliche Prüfung.

```
Lerndokument (mpv.tex)         =  ausführlich, darf etwas "weicher" sein
Abgabedokument (mpv_abgabedokument.tex)  =  MUSS formal wasserdicht sein
```

Ein externer Gutachter hat den aktuellen Stand reviewt und klar gesagt:

> **„Für die Abgabe gilt: lieber weniger Quellen, aber jede einzelne formal und inhaltlich belastbar, als ein grosses Literaturfeld mit ROT/GELB-K/Proxy-Belegen."**

Genau hier kannst **du** helfen, ohne KI.

---

## 2. Die drei Quellen-Ebenen (wichtig zum Verständnis)

Der Review trennt die Quellen in drei Schichten:

| Ebene | Was heisst das | Beispiel |
|---|---|---|
| 1. **Prüfungsnützlich** | Pascal kennt und mag die Quelle, nutzt sie für die mündliche Prüfung | viele GELB-Quellen |
| 2. **Bibliografisch korrekt** | Autor/Jahr/Titel/Seitenzahlen sind nachprüfbar richtig (APA 7) | z. B. ISBN stimmt |
| 3. **Seitenbeleg verifiziert** | Die konkrete Behauptung ist durch ein wortgetreues Zitat mit Seitenangabe aus dem Original belegt | `verified_quotes.md` Status 4 |

**Für die Abgabe muss Ebene 2 und Ebene 3 bei allen tragenden Zitaten stimmen.**
Deine Arbeit hilft uns genau dabei.

---

## 3. Die wichtigste Regel der nächsten zwei Wochen

Das Abgabedokument hat **nur 4 inhaltlich kritische Zitat-Stellen** in der Einleitung:

| Stelle | Zeile in `mpv_abgabedokument.tex` | Aktuelle Quellen |
|---|---|---|
| A1 | 164 | `erzinger2023pisa`, `stamm2021fehlenderblick`, `bfs2022migration` |
| A2 | 169 | `kellerkoller2021hellekoepfe`, `leikhof2021jugendliche` |
| A3 | 176 | `dvs2025bbf` |
| A4 | 204 | `kappus2010migration`, `stamm2012migranten` |

> **Wenn diese 4 Stellen sauber sind, ist die Abgabe praktisch sicher.**

Alles andere ist „nice to have" oder Fliesstext ohne tragende Behauptung.

---

## 4. Wie du vorgehen sollst – Überblick

Vier Aufgaben, in dieser Reihenfolge. Starte mit **Aufgabe A**, weil sie am schnellsten Sicherheit schafft.

- **Aufgabe A** – Bibliografische Fehler in `Quellen.bib` korrigieren *(ca. 2-3 Std.)*
- **Aufgabe B** – Die 4 Intro-Cites physisch in den PDFs belegen *(ca. 2-4 Std.)*
- **Aufgabe C** – Je einen Zitat-Beleg in die `verified_quotes.md`-Dateien schreiben *(ca. 2 Std.)*
- **Aufgabe D** – Quellen aus `BESCHAFFUNG.md` priorisiert besorgen *(optional, zeitabhängig)*

**Wichtig:** Jede Aufgabe protokollierst du in einer neuen Datei `Inti_Protokoll.md` (siehe Abschnitt 10). Damit sieht Pascal genau, was du gemacht hast, ohne dass du die Skripte neu laufen lassen musst.

---

## 5. Aufgabe A – Bibliografische Korrekturen in `Quellen.bib`

### Was ist `Quellen.bib`?

Die zentrale Bibliografie-Datei. Ein Eintrag sieht so aus:

```bibtex
@incollection{stamm2021fehlenderblick,
  author    = {Stamm, Margrit},
  title     = {Der fehlende {Blick} auf begabte {Minoritäten}: ...},
  booktitle = {Handbuch {Begabung}},
  year      = {2021},
  pages     = {576--588},
  ...
}
```

Du öffnest die Datei mit VS Code (Doppelklick auf `Quellen.bib` im Explorer).

### Sicherheitsregeln für diese Aufgabe

1. **Vorher Kopie machen:** Rechtsklick auf `Quellen.bib` → "Kopie erstellen". Nenn sie `Quellen_Backup_vor_Inti.bib`.
2. **Nur die Werte in `{ ... }` ändern**, nie die Struktur (keine Klammern, Kommas oder `@`-Zeichen löschen).
3. **Keine Einträge komplett löschen.** Wenn ein Eintrag „komplett falsch" scheint, kommentier ihn aus mit `%` am Zeilenanfang und frag Pascal.
4. **Nach jeder Korrektur speichern** (Strg+S) und in VS Code prüfen, dass die Zeile nicht rot unterstrichen ist.

### Die 9 konkreten Korrekturen

Jedes Mal: **In `Quellen.bib` mit Strg+F den Key suchen** (z. B. `stamm2021fehlenderblick`), dann die Felder anpassen.

---

#### A1 · `stamm2021fehlenderblick` (Seiten korrigieren)

**Zu finden:** ca. Zeile 9 in `Quellen.bib`

**Problem:** `pages = {576--588}` ist falsch. Der nächste Beitrag („Twice Exceptionality") beginnt auf S. 588, Stamms Beitrag endet auf S. 587.

**So ändern:**

```bibtex
pages = {576--587},
```

**Beleg:** Lehmanns-Katalog zum *Handbuch Begabung* (2021), Inhaltsverzeichnis.

---

#### A2 · `kuhl2019diversitaet` (Seiten korrigieren)

**Zu finden:** ca. Zeile 210

**Problem:** Vermutlich `pages = {35--57}`. Richtig ist 35–59 (Literaturverzeichnis auf S. 59 gehört noch zum Beitrag; nächster Beitrag beginnt erst auf S. 60).

**So ändern:**

```bibtex
pages = {35--59},
```

**Beleg:** pedocs-PDF `Reintjes_Kunze_Ossowski_2019_Begabungsfoerderung_und_Professionalisierung.pdf`, Inhaltsverzeichnis.

---

#### A3 · `macha2019gender` (Seiten korrigieren)

**Zu finden:** ca. Zeile 383

**Problem:** Vermutlich `pages = {160--172}`. Richtig ist 160–173.

**So ändern:**

```bibtex
pages = {160--173},
```

**Beleg:** gleiche pedocs-Quelle wie A2.

---

#### A4 · `brunner2021hochbegabung` (Jahr/Verlag/Auflage komplett falsch!)

**Zu finden:** ca. Zeile 330

**Problem:** Dieser Eintrag modelliert das Buch als Ausgabe 2021/3. Auflage/Haupt-Verlag. Das ist falsch. Das Buch ist:

- **Jahr:** 2005
- **Verlag:** Klett und Balmer
- **Ort:** Zug
- **ISBN:** 978-3-264-83605-9
- **Umfang:** 112 Seiten

**Bitte Pascal fragen, bevor du etwas änderst.** Schreib in dein Protokoll nur:

> ⚠️ `brunner2021hochbegabung` hat falsches Jahr/Verlag. Korrektur wartet auf Pascal.
> Belege:
> - https://www.klett.ch/shop/reihe/spektrum-schule/artikel/978-3-264-83605-9
> - https://www.lehmanns.de/shop/schulbuch-lexikon-woerterbuch/6521003-9783264836059

**Hintergrund:** Die Korrektur ändert auch den BibKey-Namen (`brunner2005hochbegabung`), was andere Stellen im TeX brechen kann. Pascal muss das zentral lösen.

---

#### A5 · `kellerkoller2011erkennen` (URL-Ziel korrigieren)

**Zu finden:** ca. Zeile 432

**Problem:** `url = {...}` zeigt wahrscheinlich auf die LISSA-Website. Das direkte PDF ist:

```
https://stadt.winterthur.ch/themen/leben-in-winterthur/bildung-und-schule/fur-lehrpersonen-und-schulklassen/exploratio-begabungs-und-begabtenfoerderung/zentrales-angebot/exploratio-pdfs-zentrales-angebot/begabte-migration-infoblatt-i-keller-110621.pdf
```

**So ändern:**

```bibtex
url      = {https://stadt.winterthur.ch/themen/leben-in-winterthur/bildung-und-schule/fur-lehrpersonen-und-schulklassen/exploratio-begabungs-und-begabtenfoerderung/zentrales-angebot/exploratio-pdfs-zentrales-angebot/begabte-migration-infoblatt-i-keller-110621.pdf},
title    = {Begabte mit {Migrationshintergrund} -- {Erkennen} und {Fördern}: {Informationen} für {Lehrpersonen} von {QUIMS}-{Schulen}},
date     = {2011-06-15},
```

Falls das Feld `date` schon existiert, den Wert anpassen. Falls nur `year = {2011}` drin steht, dann `year` belassen und `date = {2011-06-15},` als neue Zeile darunter einfügen.

---

#### A6 · `stern2025intelligenz` (komplett falscher Entry-Typ!)

**Zu finden:** ca. Zeile 422

**Problem:** Der Eintrag ist als `@article` modelliert mit Stern als Autorin. Aber es ist ein **Webartikel von Alex Rudolf** (Journalist) *über* ein Interview mit Stern.

**Bitte Pascal fragen.** Schreib in dein Protokoll:

> ⚠️ `stern2025intelligenz` ist ein Web-Interview von Alex Rudolf (19.03.2025), nicht ein Artikel von Elsbeth Stern. Type muss von `@article` auf `@online` geändert werden. Richtiger Autor: Alex Rudolf.
> Beleg: https://www.bildungschweiz.ch/detail/die-intelligenz-kann-sichim-schulalter-noch-veraendern

---

#### A7 · `unger2010begabungsfoerderung` (Institution falsch)

**Zu finden:** ca. Zeile 315

**Problem:** Der Eintrag schreibt als Institution vermutlich „Universität Salzburg / özbf". Korrekt:

- **Institution:** Donau-Universität Krems
- **Typ:** Master Thesis
- **Datum:** November 2010

**So ändern (falls einfach zu finden):** Im `@thesis`-Eintrag das Feld `institution` auf `{Donau-Universität Krems}` ändern. Falls es noch `type = {...}` gibt, auf `{Master Thesis}` setzen.

**Beleg:** https://oezbf.at/wp-content/uploads/2018/03/unger_evelyn_endversion.pdf

---

#### A8 · `kellerkoller2021hellekoepfe` (⚠ nicht selbst ändern)

**Zu finden:** ca. Zeile 22

**Problem:** Aktuell als `@incollection` modelliert mit Keller-Koller als Kapitelautorin von *Lichtblick für helle Köpfe* (2021). Öffentlich belegt ist **Joëlle Huser** als Hauptautorin. Ohne Buchinnenseite/TOC ist die Zuordnung „Kapitel von Keller-Koller" nicht sicher.

**Aktion:** Nur protokollieren:

> ⚠️ `kellerkoller2021hellekoepfe` – unklar, ob Keller-Koller wirklich Kapitelautorin ist. Buch ist von Joëlle Huser. Pascal muss Buchinnenseite beschaffen oder Eintrag entfernen.

---

#### A9 · `preckel2021tad` (Seiten korrigieren)

**Zu finden:** ca. Zeile 666

**Problem:** Vermutlich `pages = {274--303}`. Teil IV des Handbuchs beginnt aber auf S. 290, also kann der Preckel-Beitrag nicht bis S. 303 gehen.

**So ändern:** Öffne das Original-TOC im Handbuch (falls wir das PDF haben). Wenn nicht verfügbar, schreib ins Protokoll:

> ⚠️ `preckel2021tad` – `pages = {274--303}` nicht plausibel, Teil IV beginnt S. 290. Korrigiere auf `274--289` **oder** prüfe im Handbuch-PDF.

---

#### A10 · `dvs2025bbf` (schlechter Beleg für Abgabe-Cite)

**Zu finden:** ca. Zeile 447

**Problem:** `dvs2025bbf` zeigt auf eine allgemeine Landingpage ("Integrative Begabungs- und Begabtenförderung"). Für Stelle **A3 (Zeile 176)** im Abgabedokument ist das zu dünn. Es gibt einen konkreteren Luzerner Evaluationsbericht:

```
https://volksschulbildung.lu.ch/-/media/Volksschulbildung/Dokumente/aufsicht_evaluation/systemevaluation/Evaluationsberichte/eval_massnahmen_bbf.pdf
```

**Aktion:**

1. **PDF herunterladen** und in `Literatur/dvs2025bbf/source.pdf` speichern (oder einen neuen BibKey vorschlagen).
2. Im Protokoll notieren:

> ✅ Konkreter Luzerner Evaluationsbericht gefunden und abgespeichert unter
> `Literatur/dvs2025bbf/source_evaluationsbericht.pdf`. Pascal muss entscheiden,
> ob der BibKey `dvs2025bbf` umgebogen oder ein neuer Key (`dvs2025eval`) angelegt wird.

---

## 6. Aufgabe B – Die 4 Intro-Cites im PDF physisch belegen

Ziel: Für jede der 4 kritischen Cite-Stellen (A1–A4 aus Abschnitt 3) findest du im **PDF der zitierten Quelle** eine **Stelle**, die den Satz im Abgabedokument tatsächlich belegt. Mit **Seitenzahl** und **wortgetreuem Zitat**.

### So gehst du bei EINER Cite-Stelle vor

**Beispiel: A4 (Zeile 204), Quelle `kappus2010migration`**

1. Öffne `mpv_abgabedokument.tex` mit VS Code. Springe zu Zeile 204.
2. Lies den Satz: _"Damit besteht die Gefahr einer Under-Identifikation, defizitärer Zuschreibungen und institutioneller Diskriminierung."_
3. Öffne das PDF der Quelle: `Literatur/kappus2010migration/source.pdf` (falls vorhanden – sonst siehe Aufgabe D).
4. Suche mit **Strg+F im PDF** nach Begriffen wie: "Unteridentifikation", "Diskriminierung", "Migrationshintergrund".
5. Sobald du eine passende Textstelle findest:
   - **Seitenzahl notieren** (oben oder unten auf der PDF-Seite).
   - **Ein bis drei Sätze wortgetreu** herauskopieren.
6. In dein Protokoll eintragen (Format siehe unten).

### Vorlage pro Cite-Stelle

Füge in `Inti_Protokoll.md` unter einer Überschrift `## Aufgabe B – Intro-Cite-Belege` folgendes ein:

```markdown
### A4 (mpv_abgabedokument.tex Zeile 204)

**Behauptung im Text:** "Damit besteht die Gefahr einer Under-Identifikation,
defizitärer Zuschreibungen und institutioneller Diskriminierung."

**Quelle:** `kappus2010migration`

**Beleg-Zitat (wortgetreu):**
> "Schülerinnen und Schüler mit Migrationshintergrund werden systematisch
> unterrepräsentiert in Angeboten der Begabungsförderung, da diagnostische
> Instrumente sprachlich voraussetzungsvoll sind …"
>
> — Kappus 2010, S. 42

**Mein Urteil:** ✅ passt / ⚠️ passt nur teilweise / ❌ passt nicht

**Bemerkung:** ...
```

### Die 4 Stellen im Überblick

| Stelle | Zeile | Satz-Gist (verkürzt) | Primär zu prüfende Quellen |
|---|---|---|---|
| A1 | 164 | Bildungschancen hängen von Herkunft/Migration/Ressourcen ab | **`erzinger2023pisa`**, `stamm2021fehlenderblick`, `bfs2022migration` |
| A2 | 169 | Kinder aus benachteiligten Familien: Potenziale bleiben verdeckt, wenn Sprache/Verhalten dominieren | `kellerkoller2021hellekoepfe`, **`leikhof2021jugendliche`** |
| A3 | 176 | DVS Luzern, Begabungsförderung hat geringe Priorität | `dvs2025bbf` (ersetzen – siehe A10) |
| A4 | 204 | Gefahr von Under-Identifikation, Diskriminierung | `kappus2010migration`, `stamm2012migranten` |

**Fettgedruckt** sind die „Primärbelege" laut Review – fokussiere dich auf diese zuerst. Die anderen Quellen pro Stelle sind sekundär.

### Was tun, wenn die Quelle kein PDF hat?

Manche Quellen haben aktuell kein PDF im Repo (sogenannte ROT-Quellen). Dann:

- Im Protokoll als **"PDF fehlt"** markieren.
- Übergehen und mit der nächsten Quelle weitermachen.
- Diese Quellen landen dann in Aufgabe D (Beschaffung).

### Hinweis zum Review-Urteil

Der Review empfiehlt für jede der 4 Stellen auch **alternative Quellen**, die ohne Umwege belegt werden könnten:

- **A1:** `erzinger2023pisa` + `bfs2022migration` reichen (Stamm rauslöschen? Pascal entscheidet).
- **A2:** primär `leikhof2021jugendliche`.
- **A3:** durch den konkreten DVS-Evaluationsbericht ersetzen.
- **A4:** alternativ `kellerkoller2011erkennen`, `reutlinger2015hochbegabung`, `maehler2018diagnostik`.

**Das sind Optionen für Pascal** – du musst diese alternativen Quellen nicht selbst einbauen, aber wenn du bei deinem Beleg-Check feststellst, dass eine dieser Alternativen besser passt, notier das im Protokoll.

---

## 7. Aufgabe C – Verified-Quotes-Einträge schreiben

### Was ist `verified_quotes.md`?

Für jede Quelle gibt es einen Ordner in `Literatur/<BibKey>/`. Darin eine Datei `verified_quotes.md`, in die die verifizierten Zitate kommen.

Beispiel: `Literatur/kappus2010migration/verified_quotes.md`

Struktur (vereinfacht):

```markdown
# Verifizierte Zitate – kappus2010migration

**Status:** 4
**Verifiziert am:** 2026-04-20
**Verifiziert durch:** Inti

---

## Zitat 1 (Beleg für Abgabedokument Zeile 204)

> "Schülerinnen und Schüler mit Migrationshintergrund werden systematisch
> unterrepräsentiert …"

**Seite:** 42
**Kontext:** Kapitel 3 "Diagnostik unter sprachlichen Voraussetzungen"

<!-- CLAIMS-START (automatisch durch cite_context.py erzeugt; nicht manuell editieren) -->
...
<!-- CLAIMS-END -->
```

### Was du konkret tust

Für jede Quelle, für die du in Aufgabe B einen Beleg gefunden hast:

1. Öffne `Literatur/<BibKey>/verified_quotes.md`.
2. Suche die Zeile mit `**Status:**` und setze sie auf `4`.
3. Setze `**Verifiziert am:**` auf das heutige Datum (Format: `2026-04-20`).
4. Füge ein Feld `**Verifiziert durch:** Inti` hinzu, falls es noch nicht existiert.
5. **Oberhalb** der Zeile `<!-- CLAIMS-START ...` fügst du einen Block ein wie:

```markdown
## Zitat 1 (Beleg für Abgabedokument Zeile 204)

> "Hier wortgetreues Zitat …"

**Seite:** 42
**Kontext:** Kapitel X
```

**Niemals** den Bereich zwischen `<!-- CLAIMS-START -->` und `<!-- CLAIMS-END -->` anfassen. Der wird automatisch neu generiert.

### Wichtige Regeln für Zitate

- **Wortgetreu**, keine Kürzungen mitten im Satz. Auslassungen nur mit `…`.
- **Seitenzahl zwingend**. Ohne Seite ist es kein Status-4-Beleg.
- **Eigene Formulierungen** gehen in den Abschnitt „Kontext", nicht ins Zitat.
- **Umlaute und Sonderzeichen** genau so übernehmen wie im Original.

---

## 8. Aufgabe D – `BESCHAFFUNG.md` priorisiert abarbeiten (optional)

Wenn du Zeit hast: Öffne `BESCHAFFUNG.md`. Dort sind 22 ROT-Quellen nach Priorität sortiert.

### Die wichtigsten Quellen für uns

Aus der strategischen Analyse (siehe `FRAGEN_ABSTIMMUNG.md`, wenn du neugierig bist):

| Priorität | BibKey | Warum wichtig |
|---|---|---|
| 1 | `muelleroppliger2021handbuch` | Hebt 18 weitere Quellen mit, Kernlit in 3 Fragen |
| 2 | `buholzer2010allegleich` | Kernlit in 2 Fragen, aktuell nur 2 S. im PDF! |
| 3 | `trautmann2016einfuehrung` | Kernlit Fr. 1, betrifft 3 Fragen |
| 4 | `lehwald2017motivation` | Vollversion (nur 13 S. im Repo), betrifft 3 Fragen |
| 5 | `kappus2010migration` | Intro A4 + 3 Fragen |

### So besorgst du eine Quelle

1. In `BESCHAFFUNG.md` den Eintrag suchen. Dort ist ein Swisscovery-Link.
2. Swisscovery öffnet den SLSP-Katalog ganzer CH-Bibliotheken.
3. Standort prüfen (z. B. PH Luzern, ZHB Luzern).
4. Bestellen/ausleihen/vor Ort fotografieren.
5. PDF erstellen und in `Literatur/<BibKey>/source.pdf` speichern.
6. Im Protokoll festhalten, welche Quellen du besorgt hast.

### Hinweis
- **Bitte keine Piraterie-Seiten** (libgen, sci-hub) – die Abgabe muss sauber sein.
- Wenn ein Buch nur als E-Book bestellbar ist, ruf Pascal an, bevor du kaufst.

---

## 9. Werkzeug-Liste

| Werkzeug | Wofür | Download/Ort |
|---|---|---|
| VS Code | `.bib`-/`.md`-Dateien editieren | Bereits installiert |
| Adobe Reader / Chrome | PDFs mit Strg+F durchsuchen | Bereits installiert |
| Browser | Recherche, Swisscovery | Bereits installiert |
| Swisscovery | https://swisscovery.slsp.ch | Konto Pascal? Im Zweifel fragen |

**VS Code-Tipps:**

- `Strg+F` → Suche in aktueller Datei
- `Strg+Shift+F` → Suche im ganzen Repo
- `Strg+Klick` auf `\label{...}` oder `\cite{...}` → Sprung zur Definition
- `Strg+Z` → Rückgängig (beliebig oft)
- Rechts unten: Markdown-Vorschau-Icon (`Strg+Shift+V`) zum Anschauen von `.md`-Dateien

---

## 10. Dein Arbeits-Protokoll

Erstelle im Root-Ordner die neue Datei `Inti_Protokoll.md`. Darin dokumentierst du **alles**, was du machst. Vorlage:

```markdown
# Inti-Protokoll

_Beginn: 2026-04-20 · Status: in Bearbeitung_

## Aufgabe A – Bibliografische Korrekturen

### A1 · stamm2021fehlenderblick
- ✅ Seiten von 576--588 auf 576--587 geändert.
- Quelle geprüft: Lehmanns-Katalog (URL)

### A2 · kuhl2019diversitaet
- ✅ Seiten auf 35--59 geändert.

### A4 · brunner2021hochbegabung
- ⚠️ NICHT geändert. Komplexe Korrektur, wartet auf Pascal.
- Beleg-URLs notiert.

...

## Aufgabe B – Intro-Cite-Belege

### A1 (Zeile 164) · erzinger2023pisa
- ✅ Belegt mit Zitat von S. 87.
- Sektion 3.2 "Soziale Herkunft und Bildungserfolg"
...

## Aufgabe C – Verified-Quotes

- ✅ `Literatur/erzinger2023pisa/verified_quotes.md` auf Status 4 gesetzt.
- ✅ `Literatur/kappus2010migration/verified_quotes.md` auf Status 4 gesetzt.
...

## Aufgabe D – Beschaffung

- ✅ `muelleroppliger2021handbuch` aus PH Luzern ausgeliehen, PDF erstellt.
...

## Fragen an Pascal

1. `brunner2021hochbegabung`: Soll ich den Key umbenennen?
2. `stern2025intelligenz`: neuer Key als @online?
...
```

So weiss Pascal immer, wo du stehst, ohne dass du irgendein Skript laufen lassen musst.

---

## 11. Sicherheitsregeln (wichtig!)

| Regel | Warum |
|---|---|
| **Immer vorher Backup** der Datei, die du änderst | Falls etwas schiefgeht, ist die Originalversion noch da |
| **Keine `.tex`-Dateien editieren** (weder `mpv.tex` noch `mpv_abgabedokument.tex`) | Das sind die Hauptdokumente, da gehen Änderungen schnell schief |
| **Keine Python/Julia-Skripte ausführen** | Dafür ist Pascal zuständig |
| **Keine Dateien im Unterordner `excerpts/` ändern** | Die werden automatisch generiert |
| **Bei Unsicherheit: Pascal fragen** | Lieber einmal zu viel als zu wenig |

### Was passiert, wenn du etwas kaputt machst?

**Nichts Schlimmes.** Das Projekt ist unter Git-Versionsverwaltung. Pascal kann jede Änderung rückgängig machen, solange du vorher ein Backup gemacht hast.

---

## 12. Checkliste für den Abschluss

Wenn du fertig bist:

- [ ] `Inti_Protokoll.md` existiert und ist vollständig.
- [ ] Mindestens **Aufgabe A1, A2, A3, A5** (die einfachen Seiten-/URL-Korrekturen) in `Quellen.bib` sind umgesetzt.
- [ ] Für mindestens **2 der 4 Intro-Cites** (A1–A4) gibt es einen wortgetreuen Beleg im Protokoll.
- [ ] Die entsprechenden `verified_quotes.md`-Dateien sind auf Status 4.
- [ ] Offene Fragen an Pascal sind gesammelt.

**Bonus:**

- [ ] Alle 10 `Quellen.bib`-Korrekturen (A1–A10) sind erledigt oder eindeutig protokolliert.
- [ ] Alle 4 Intro-Cites haben Belege.
- [ ] Eine der Top-5-Beschaffungs-Quellen ist besorgt.

---

## 13. Was du **nicht** tun sollst (um Pascal zu schützen)

- ❌ Keine Inhalte in `mpv.tex` oder `mpv_abgabedokument.tex` ändern (das macht Pascal).
- ❌ Keine Dateien löschen.
- ❌ Keine `git push`/`git commit` ausführen.
- ❌ Kein Skript (`.py`, `.jl`) laufen lassen.
- ❌ Keine neuen Ordner in `Literatur/` anlegen ohne Rücksprache.
- ❌ Keine Zitate „ausdenken" oder „rekonstruieren" – nur wortgetreu aus Originaltext.

---

## 14. Kurze FAQ

**Q: Ich finde den BibKey nicht in `Quellen.bib`.**
A: Strg+F drücken und exakt den Key-Namen eingeben (ohne `@...{` und ohne Komma dahinter). Falls immer noch nicht: Pascal fragen.

**Q: Der PDF-Viewer zeigt die Seitenzahl anders als die gedruckte Seite.**
A: Nimm die **gedruckte** Seitenzahl (die aus dem Buch), nicht den Scroll-Zähler. Oft gibt's im PDF sowohl eine Dokument-interne Nummerierung als auch eine gedruckte.

**Q: Der Satz im Abgabedokument steht so **exakt** nicht in der Quelle.**
A: Das ist normal. Eine Behauptung darf paraphrasiert zitiert werden. Wichtig ist, dass die **Kernaussage** im Zitat auffindbar ist. Wenn du nur eine halbwegs passende Stelle findest, markier im Protokoll „passt teilweise" und schreib deine Begründung dazu. Pascal kann dann entscheiden.

**Q: Ich will eine Quelle ganz aus einem Zitat entfernen.**
A: Nicht selbst machen – nur im Protokoll vorschlagen. Pascal entscheidet.

**Q: Eine PDF-Datei ist riesig (>500 Seiten) und ich finde nichts.**
A: Lass sie. Markiere im Protokoll „zu umfangreich ohne TOC". Pascal hat Skripte, die Kapitel-Splits erzeugen können.

**Q: Swisscovery braucht eine Anmeldung.**
A: Frag Pascal nach seinem SLSP-Login. Oder registriere dich mit deinem eigenen – das ist kostenlos.

---

## 15. Schlusswort

Inti, alles was du in Aufgabe A und B machst, bringt die Abgabe deutlich näher ans wasserdichte Ziel. Die Skripte und die KI können vieles, aber sie können **nicht** in einem gedruckten Buch auf Seite 42 nachschauen. Genau das tust du, und das ist der Punkt, an dem diese Arbeit steht.

Bei Fragen: Pascal ist da. Bei technischen Problemen mit VS Code: im Zweifel zuerst `Strg+Z` drücken, dann Pascal fragen.

**Viel Erfolg!** 💙

---

### Anhang: Der Gutachter-Review in einem Satz

> „Das Lerndokument darf breit bleiben. Das Abgabedokument muss schmal und hart geprüft sein."

Das ist der Leitsatz für deine Arbeit.
