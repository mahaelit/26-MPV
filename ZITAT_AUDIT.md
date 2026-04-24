# ZITAT_AUDIT.md — Phase 1.5: Claim-by-Claim-Audit

> **Zweck:** Pro Cite-Stelle wird gefragt: *Ist die empirische oder konzeptuelle Behauptung an eine konkrete Stelle (Seitenzahl, Kapitel, Abschnitt) gebunden, die Inti am Prüfungstag aufschlagen kann?* Wo die Antwort *Nein* lautet, gibt es drei Aktionen: (1) Seite nachtragen, (2) Behauptung weicher formulieren, (3) Behauptung streichen.
>
> **Stand:** 2026-04-24 · **Reihenfolge:** Erst Abgabedokument (Korpus A), dann Lerndokument (Korpus B / mündlich).
>
> **Methodische Vorgabe (aus [`ENTSCHEIDUNGEN.md`](ENTSCHEIDUNGEN.md) E6):** Jeder Eintrag erhält eine **exakte** Seiten-/Kapitelangabe — *nicht* „ca. 80 S.", sondern „S. 17–84 (= 68 S.) Kap. 3" o. ä.

---

## Bewertungsskala pro Cite-Stelle

| Status | Bedeutung | Aktion |
|---|---|---|
| **OK** | Behauptung ist an konkrete Seite/Stelle gebunden, Volltext liegt vor, im Prüfungsgespräch aufschlagbar | nichts |
| **SEITE** | Quelle stimmt, aber Seite/Kapitel fehlt im Text und/oder in `Quellen.bib` | Seite nachtragen |
| **BELEG** | Behauptung weiter als die Quelle hergibt (Generalisierung, „systematisch", „signifikant") | weicher formulieren oder Quelle ergänzen |
| **VOLLTEXT** | Quelle ist passend, aber kein lokaler Volltext → Inti kann am Prüfungstag nicht aufschlagen | Volltext beschaffen (Phase 2) oder Behauptung weicher |
| **NEU** | Quelle muss ergänzt werden (z. B. weil Behauptung aus zwei Quellen besser belegt wäre) | Quelle einfügen + Bib-Eintrag prüfen |
| **STREICHEN** | Behauptung trägt nichts und/oder ist nicht belegbar | streichen |

---

# Teil A · Abgabedokument (Korpus A) — vollständiger Audit

> **Geltungsbereich:** [`mpv_abgabedokument.tex`](mpv_abgabedokument.tex). Vier `\parencite`-Stellen in der Einleitung; danach nur noch `\cite{}` in Kernliteratur-Listen pro Frage. Die Kernliteratur-Listen werden in einem eigenen Block (Teil A.5) abgedeckt.

## A.1 Einleitung — Ausgangslage (Z. 161–169)

### Cite-Stelle 1 · Z. 164

**Behauptung:** „Bildungschancen in der Schweiz [hängen] weiterhin stark von sozialer Herkunft, Migrationsgeschichte und familiären Ressourcen ab"
**Belege:** `\parencite{erzinger2023pisa, stamm2021fehlenderblick, bfs2022migration}`

| Quelle | Volltext lokal? | Aktueller Beleg-Stand | Aktion |
|---|---|---|---|
| `erzinger2023pisa` | PDF 2.5 MB / 119 S. | keine spezifische Seite | **SEITE** — Inti-Randkommentar fragt nach den genauen Seiten zu Migrations-/Sozialherkunfts-Befunden in PISA 2022. Konkret: S. 5–7 (Executive Summary), Kap. „Soziale Herkunft" (vermutlich S. 60–80) im Volltext nachschlagen. |
| `stamm2021fehlenderblick` | KEIN Volltext | keine Seitenangabe | **SEITE + VOLLTEXT** — Stamm-Kapitel ist S. 576–588 im Handbuch Begabung 2021 (durch Inhaltsverzeichnis-Recherche bestätigt). Volltext muss beschafft werden. |
| `bfs2022migration` | PDF 1.9 MB / 60 S. | keine Seite | **SEITE** — Konkrete Seiten/Tabellen der BFS-Statistik einfügen, oder weicher formulieren („… belegt durch laufende Statistiken des BFS, vgl. BFS 2022."). Inti-Randkommentar erwägt sogar neuere BFS-Quelle. |

**Empfehlung:** Stelle bleibt textlich wie sie ist; in `Quellen.bib`-`note` jeweils die belegrelevanten Seitenbereiche einfügen, sodass Inti am Prüfungstag direkt aufschlagen kann.

### Cite-Stelle 2 · Z. 169

**Behauptung:** „Kinder aus sozioökonomisch benachteiligten oder zugewanderten Familien sind in anspruchsvolleren Bildungswegen und Förderangeboten häufig untervertreten; ihre Potenziale bleiben nicht selten verdeckt, insbesondere dann, wenn sprachliche Unsicherheiten, belastende Lebensumstände oder auffälliges Verhalten die Wahrnehmung dominieren"
**Belege:** `\parencite{kellerkoller2021hellekoepfe, leikhof2021jugendliche}`

| Quelle | Volltext lokal? | Aktueller Beleg-Stand | Aktion |
|---|---|---|---|
| `kellerkoller2021hellekoepfe` | KEIN Volltext | `pages = {XXX--XXX}` in Bib | **SEITE + VOLLTEXT** — Inti-Randkommentar verweist auf S. 76–78 in Huser 2021. Bib korrigieren auf `pages = {76--78}`, Volltext beschaffen. |
| `leikhof2021jugendliche` | PDF 5.6 MB / 365 S. | keine Seite | **SEITE** — Inti-Randkommentar fragt nach genauen Seiten. Vermutlich Kap. 1–3 (S. ~25–80). Im Volltext belegen, Bib-`note` ergänzen. |

### Cite-Stelle 3 · Z. 176

**Behauptung:** „Gezielte Weiterbildungen zum Thema Begabungsförderung werden nur von einem Teil der Schulen angeboten, und das Thema hat insgesamt geringe Priorität"
**Beleg:** `\parencite{dvs2025bbf}`

| Quelle | Volltext lokal? | Aktueller Beleg-Stand | Aktion |
|---|---|---|---|
| `dvs2025bbf` | KEIN Volltext (Online-Quelle) | `urldate = {2026-03-30}` | **BELEG** — Inti-Randkommentar fragt: „wo steht, dass es wenig Priorität hat?" Antwort: Die DVS-Webseite enthält das nicht so wörtlich. **Aktion:** Behauptung weicher formulieren („… und das Thema wird in der Praxis selten als Schwerpunkt gesetzt") oder zusätzlichen Beleg ergänzen (Brunner/Lienhard, Weigand, Kanton-Statistiken). |

### Cite-Stelle 4 · Z. 204

**Behauptung:** „Damit besteht die Gefahr einer Under-Identifikation, defizitärer Zuschreibungen und institutioneller Diskriminierung"
**Belege:** `\parencite{kappus2010migration, stamm2012migranten}`

| Quelle | Volltext lokal? | Aktueller Beleg-Stand | Aktion |
|---|---|---|---|
| `kappus2010migration` | KEIN Volltext | `pages = {63--77}` in Bib | **SEITE + VOLLTEXT** — Inti-Randkommentar fragt nach genauen Seiten zur Under-Identifikation. Volltext muss beschafft werden, dann konkrete S. (vermutlich S. 70–74) einfügen. |
| `stamm2012migranten` | KEIN Volltext (Dossier 12/4) | keine Seite | **SEITE + VOLLTEXT** — Stamm-Dossier ist online via SwissEducation. Volltext beschaffen + spezifische S. zur Under-Identifikation einfügen. |

---

## A.2 Einleitung — Fall S. (Z. 179–195) und Heilpädagogischer Bezug (Z. 197–213)

**Status:** Hier sind keine Cite-Stellen, sondern Fall-Beschreibung und ICF-Rahmung. Audit-Aktion: **inhaltliche Präzisierung** gemäss [`ENTSCHEIDUNGEN.md`](ENTSCHEIDUNGEN.md) E3 — Migrationsform im Fall S. explizit benennen (Familiennachzug? Asyl? Arbeitsmigration aus Albanien?).

**Empfehlung Inti:** In Z. 181 nach „Schweiz." einen Halbsatz einfügen, der die Migrationsform präzisiert, soweit faktisch belegbar.

---

## A.3 Erkenntnisinteresse und Fragestellungen (Z. 215–251) — Schärfungen aus Feedback

### FW1 · Z. 228–230

**Aktuelle Formulierung:**
> „Wie können verdeckte Begabungen bei neu zugewanderten, **mehrsprachigen** Schüler:innen mit **geringen Deutschkenntnissen** multiperspektivisch und sprachsensibel erfasst werden?"

**Audit:** Doppelung *mehrsprachig + geringe Deutschkenntnisse* (Inti-Randkommentar). „Mehrsprachig" beschreibt das Sprachprofil, „geringe Deutschkenntnisse" beschreibt den Zweitspracherwerbsstand — das ist nicht dasselbe, kann aber redundant wirken.

**Aktion:** Umformulieren auf:
> „Wie können verdeckte Begabungen bei neu zugewanderten Schüler:innen **im frühen Zweitspracherwerb** multiperspektivisch und sprachsensibel erfasst werden?"

Die Mehrsprachigkeit (Albanisch, Englisch, Deutsch im Fall S.) wird im Fall-Abschnitt detailliert; in der Frage selbst wird sie auf den diagnostisch entscheidenden Punkt (Zweitspracherwerb) konzentriert.

### FW2 · Z. 231–233

**Aktuelle Formulierung:**
> „Welche **sensumotorischen** und schriftsprachlichen Faktoren …"

**Audit:** [`ENTSCHEIDUNGEN.md`](ENTSCHEIDUNGEN.md) E2 = B → *sensomotorisch* konsistent. Hier und in Kap. 4-Überschrift ändern.

**Aktion:** Ersetze „sensumotorisch" → „sensomotorisch" (an dieser Stelle und in der Kapitel-Überschrift Z. 285).

### FW3 · Z. 234–236

**Aktuelle Formulierung:**
> „Wie beeinflussen Ausgrenzungs-, **Belastungs**- und Migrationserfahrungen die Begabungsentwicklung und soziale Teilhabe, und welche Beziehungsgestaltungen wirken förderlich?"

**Audit:** Inti-Randkommentar wirft drei Probleme auf:
- *Belastung* klingt pathologisierend
- die Frage zielt auf *Beziehungsgestaltungen*, der Lerndokument-Text entfaltet aber Anerkennungstheorie, Inklusionsstrukturen, Schulkultur
- „Belastungs- und Migrationserfahrungen" verschmelzt zwei Dimensionen, die man trennen sollte

**Aktion:** Umformulieren auf eine der zwei vom Feedback empfohlenen Varianten:
> Variante *Weit* (empfohlen): „Welche **relationalen und strukturellen Bedingungen** ermöglichen die Sichtbarkeit und Entfaltung von Begabung bei Schüler:innen mit Migrationserfahrung?"

Diese Formulierung deckt Beziehung, Anerkennung, Teilhabe und Schulkultur konsistent ab und entwaffnet den Beziehungs-Engführungs-Widerspruch.

### BW4 · Z. 237–239

**Aktuelle Formulierung:**
> „Inwiefern können offene, enrichment-orientierte Begabungsförderungssettings wie SOLUX Potenziale sichtbar machen, die im Regelunterricht **systematisch übersehen** werden?"

**Audit:** Inti-Randkommentare:
- „warum systematisch übersehen?" — die Aussage ist stark, muss empirisch tragen (Stamm 2021, Mun 2020 als Beleg).
- „warum nicht mehr bei Kindern mit Migrationserfahrung?" — die Migrationsperspektive fehlt in der Frage.
- „hebt es sich deutlich von FW1 ab?" — Abgrenzung zu FW1 muss klar sein.

**Aktion:** Migrationsperspektive zurückholen + Abgrenzung zu FW1 schärfen:
> „Inwiefern können offene, enrichment-orientierte Begabungsförderungssettings wie SOLUX Potenziale sichtbar machen, die im Regelunterricht **bei Schüler:innen mit Migrationserfahrung** systematisch verdeckt bleiben?"

**Merksatz für mündliche Abgrenzung:** *FW1 antwortet mit Verfahren und Instrumenten (Tests, Beobachtung, dynamische Diagnostik), BW4 antwortet mit Settings und Prinzipien (Notenfreiheit, Interessenorientierung, Sprachentlastung, Expertenrolle).* (in `PRUEFUNG_VORBEREITUNG.md` ablegen, nicht im Abgabedokument).

### BW5 · Z. 240–243

**Aktuelle Formulierung (akzeptiert):** keine Änderung nötig — Inti-Randkommentar „muss es bei neu zugewanderten sein?" wird im Feedback verteidigt: *Die MPV hat einen klaren thematischen Fokus, und BW5 ist die Professionsfrage zu diesem Thema.*

**Aktion:** keine Änderung am Text. Im mündlichen Repertoire den Verteidigungssatz vorbereiten („Die hier beschriebenen Beratungsprinzipien sind übertragbar, gelten aber mit besonderer Schärfe bei neu zugewanderten Kindern wegen der kumulativen institutionellen Intransparenz.").

---

## A.4 Neue Einleitungs-Bausteine (E1, E3, E4)

Aus den Phase-0-Entscheidungen entstehen drei kurze Einfügungen in die Einleitung des Abgabedokuments:

### A.4.1 · Begriffsdefinitions-Absatz (E1 = C) — neu am Ende von 1.1 *Ausgangslage* oder am Anfang von 1.4 *Erkenntnisinteresse*

**Vorschlagsformulierung (~70 Wörter):**
> „In dieser Arbeit werden *Begabung* und *Potenzial* mit Stern (2025) und Müller-Oppliger (2021) als entwicklungsfähige Möglichkeiten zur Leistung verstanden, nicht als statische Eigenschaften. Diese Lesart hebt die Bedeutung des Kontexts hervor: Begabung wird zur Performanz nur unter günstigen Bedingungen, Potenzial bleibt verdeckt, wenn diese Bedingungen fehlen. Die Begriffe werden im Folgenden weitgehend synonym verwendet; *Potenzial* dort, wo der Möglichkeitscharakter betont werden soll, *Begabung* in der Diktion der zitierten Modelle (Renzulli, Heller/Perleth)."

**Cite-Stellen:** `\textcite{stern2025intelligenz}` + `\textcite{muelleroppliger2021handbuch}`.

**Audit-Status:** **NEU** — beide Quellen sind in `Quellen.bib`, `stern2025intelligenz` ist Interview/Zeitschriftenbeitrag (Status 0, kein Volltext), `muelleroppliger2021handbuch` Status 2 (Volltext fehlt; Inhaltsverzeichnis aber recherchiert in [`ENTSCHEIDUNGEN.md`](ENTSCHEIDUNGEN.md)).

### A.4.2 · Migrationsbegriffs-Absatz (E3 = C) — neu am Anfang von 1.4 *Erkenntnisinteresse*, vor der Aufzählung der Fragen

**Vorschlagsformulierung (~120 Wörter):**
> „Unter *Migrationserfahrung* wird in dieser Arbeit verstanden: das Aufwachsen bzw. der Neuzugang in einem Schulsystem, das nicht die primäre Sozialisationssprache spricht. Diese Erfahrung geht in der Schweizer Volksschule typischerweise mit sozioökonomischer Benachteiligung (BFS 2022) und unterbrochener Bildungsbiographie einher. Der Fall S. liegt an der Schnittstelle zwischen [Inti: Migrationsform präzisieren] und möglicher Fluchterfahrung; die exakte Form ist für die heilpädagogische Fragestellung sekundär, weil die wirksamen Mechanismen — sprachliche Isolation, kumulative Belastung, defizitäre Wahrnehmung — über Migrationstypen hinweg greifen \\parencite\\{alodat2025equitable\\}."

**Cite-Stellen:** `\parencite{bfs2022migration, alodat2025equitable}`.

**Audit-Status:**
- `bfs2022migration` — **SEITE** + Volltext liegt vor.
- `alodat2025equitable` — **NEU im Abgabedokument** (bislang nur im Lerndokument). Achtung: Aufnahme verändert die A-Korpus-Trennung (E4). **Alternative:** Statt Alodat kann die Aussage auf die deutschsprachigen Quellen Behrensen 2019 + Stamm 2014 gestützt werden, dann bleibt das A-Korpus unverändert.

### A.4.3 · Vorwortabsatz zur Korpus-Trennung (E4 = A) — am Ende von 1.4 *Erkenntnisinteresse* oder als kurzer Hinweis vor dem Literaturverzeichnis

**Vorschlagsformulierung (~50 Wörter):**
> „Die im Folgenden zitierte Literatur (siehe Literaturverzeichnis) bildet das Studien- und Beleg-Korpus dieser Vertiefungsarbeit. Im Prüfungsgespräch wird zur internationalen Vertiefung ergänzend auf vier englischsprachige Fachartikel (Mun et al. 2020; Gubbins et al. 2020; Al-Hroub 2021; Alodat 2025) Bezug genommen, die nicht zum schriftlichen Korpus gehören."

**Audit-Status:** **OK** — alle vier Artikel sind im `Quellen.bib` definiert, werden hier nur namentlich genannt (kein `\cite`).

---

## A.5 Kernliteratur-Listen pro Frage — Audit nach E5 + E6

> **Aktion E5:** `brunner2021hochbegabung` aus den Listen entfernen, ersetzen durch `muelleroppliger2021handbuch` (Schweizer Förderkontext-Kapitel) und `stamm2014handbuch` (Talententwicklungs-Kapitel).
> **Aktion E6:** „ca. X S." durch *exakte* Seitenangaben mit Kapitelreferenz ersetzen, basierend auf den Inhaltsverzeichnis-Recherchen aus [`ENTSCHEIDUNGEN.md`](ENTSCHEIDUNGEN.md). Wird in **Phase 1** (Bibliographie) abgeschlossen.

### Frage 1 (Z. 268–279)

| Quelle | Aktueller Beleg | E6-Aktion (Phase 1) |
|---|---|---|
| `stamm2021fehlenderblick` | „ca. 15 S." | S. 576–588, Handbuch Begabung 2021 (= **13 S.**, nicht 15) |
| `kellerkoller2021hellekoepfe` | „ca. 20 S." | S. 76–78 in Huser 2021 (= **3 S.**, nicht 20!) ← Gravierende Korrektur |
| `maehler2018diagnostik` | „Kap. 1–3, 9–10 (ca. 80 S.)" | exakte Kap.-Seiten verifizieren |
| `preckel2013hochbegabung` | „Kap. 1–2 (ca. 40 S.)" | exakte Kap.-Seiten verifizieren (EPUB liegt vor) |
| `muelleroppliger2021handbuch` | „Kap. Begabungsbegriff, Diagnostik (ca. 40 S.)" | Müller-Oppliger 2021 *Begabungsmodelle* S. 204–223 (=20 S.) + S.-Müller-Oppliger *Päd. Diagnostik* S. 224–238 (=15 S.) + Gauck/Reimann *Psych. Diagnostik* S. 239–251 (=13 S.) = **48 S.** |
| `trautmann2016einfuehrung` | „Kap. 1–2 (ca. 40 S.)" | Volltext fehlt (ROT) — exakte Seiten müssen aus Buch verifiziert werden |
| `reutlinger2015hochbegabung` | „ca. 15 S." | PDF 32 S., genaue Reichweite verifizieren |
| `ipege2009professionelle` | „Kap. Diagnostik (ca. 20 S.)" | PDF 53 S., exakte Diagnostik-Kap.-Seiten |
| `webb2020doppeldiagnosen` | „Kap. 1–2, 10 (ca. 25 S.)" | Volltext fehlt (ROT) — beschaffen |

**Inti-Randkommentar:** Verweis auf zusätzliche Handbuch-Begabung-Kapitel (Stahl mBET, Müller-Oppliger pädagogische Diagnostik, Gauck/Reimann psychologische Diagnostik) für Frage 1. Diese sind bereits in `Quellen.bib` als `stahl2021mbet`, `muelleroppliger2021paeddiagnostik`, `gauckreimann2021psychdiagnostik` vorhanden. **Empfehlung:** Im Lerndokument-Fliesstext ergänzen, im Abgabedokument-Kernliteratur-Liste optional aufnehmen, wenn Frage 1 stärker auf Diagnostik fokussiert.

### Frage 2 (Z. 298–305)

| Quelle | Aktueller Beleg | E6-Aktion |
|---|---|---|
| `rosebrock2010grundlagen` | „Kap. 1–4 (ca. 60 S.)" | Volltext fehlt (ROT) — beschaffen |
| `gold2018lesenkannmanlernen` | „Kap. 1–4 (ca. 70 S.)" | Volltext fehlt (ROT) — beschaffen |
| `sturm2016graphomotorik` | „ca. 20 S." | S. 183–198 (= **16 S.**) |
| `lehwald2017motivation` | „Kap. 2–4 (ca. 60 S.)" | Volltext nur 13-S.-Auszug — beschaffen |
| `fischer2020begabungsfoerderung` | „ca. 30 S." | Volltext liegt vor (419 S.), Beiträge zu Enrichment + Sprache verorten |

### Frage 3 (Z. 324–334)

| Quelle | Aktueller Beleg | E6-Aktion |
|---|---|---|
| `grossrieder2010anerkennung` | „ca. 10 S." | S. 87–96 = **10 S.** ✓ |
| `kuhl2019diversitaet` | „ca. 23 S." | S. 35–57 = **23 S.** (Bib-VERIFY auf 35–59 prüfen) |
| `behrensen2019inklusive` | „ca. 12 S." | S. 86–98 = **13 S.** |
| `booth2019index` | „Dim. A und B (ca. 60 S.)" | Volltext fehlt (ROT) — beschaffen, exakte Dim.-A/B-Seiten |
| `lehwald2017motivation` | „Kap. 5–6 (ca. 30 S.)" | Volltext-Auszug — beschaffen |
| `kappus2010migration` | „ca. 15 S." | S. 63–77 = **15 S.** ✓ — Volltext fehlt, beschaffen |
| `stamm2012migranten` | „ca. 15 S." | Dossier 12/4, Volltext beschaffen |
| `webb2020doppeldiagnosen` | „Kap. 1–2 (bereits gezählt)" | s. Frage 1 |

### Frage 4 (Z. 354–363) — **E5-Korrektur erforderlich**

**Aktuelle Liste (Auszug):**
```latex
\item[\cite{brunner2021hochbegabung}] Hochbegabung (k)ein Problem?
  Kap. Identifikation, Fördermodelle im Schweizer Kontext. (ca.~25\,S.)
```

**E5-Aktion:** ersetzen durch:
```latex
\item[\cite{muelleroppliger2021handbuch}] Handbuch Begabung. Weigand/Kaiser
  »Separativ oder integrativ« (S.\,290--301) und Anderegg/Wilhelm
  »Begabungsfördernde Schulentwicklung« (S.\,302--318) zum Schweizer
  Förderkontext. (ca.~28\,S.)
\item[\cite{stamm2014handbuch}] Handbuch Talententwicklung. Kap. zu
  Schweizer Bildungssystem und Talentförderung. (Seiten verifizieren)
```

Damit ist `brunner2021hochbegabung` aus der Frage-4-Liste entfernt; es bleibt zu prüfen, ob die Frage-5-Liste analog angepasst wird.

### Frage 5 (Z. 384–393) — **E5-Korrektur erforderlich**

**Aktuelle Liste (Auszug):**
```latex
\item[\cite{brunner2021hochbegabung}] Hochbegabung (k)ein Problem?
  Kap. Schweizer Förderkontext. (bereits bei Fr.~4 gezählt)
```

**E5-Aktion:** Eintrag streichen (kein Ersatz nötig, weil Frage 5 ihren Schweizer Bezug bereits über Buholzer/Kummer Wyss + Leikhof + Kosorok-Labhart hat).

### Frage 4 + 5 Seitenbudget — Konsequenz

Brunner-Streichung und Müller-Oppliger-Erweiterung verändern die Bruttozahlen der Fragen 4 + 5. Wird in **Phase 4** (Seitenbudget-Tabelle) endgültig nachgerechnet.

---

# Teil B · Lerndokument (Korpus B / mündlich)

> **Geltungsbereich:** [`mpv.tex`](mpv.tex) — nur die Inti-Randkommentare und High-Cite-Quellen werden audited. Vollständiger Audit ist für die schriftliche Abgabe nicht erforderlich, weil das Lerndokument nicht abgegeben wird. Aber für die mündliche Prüfung ist relevant, wo der Text starke Behauptungen macht, die Inti situativ verteidigen können muss.

## B.1 Methodisches Vorgehen

Die Inti-Randkommentare im Lerndokument sind die Audit-Liste. Sie werden gruppiert nach drei Kategorien:

- **B.1.1 Seite/Stelle nachtragen** — der Text macht eine Aussage, Inti weiss, in welcher Quelle es steht, aber die Seite fehlt.
- **B.1.2 Mehrquellen-Bündelung** — die Aussage könnte besser belegt werden, wenn 2–3 Quellen kombiniert werden.
- **B.1.3 Behauptung weicher** — die Aussage geht über das hinaus, was die Quellen hergeben (z. B. „systematisch", „signifikant", „durchgängig").

## B.1.1 · Seite/Stelle nachtragen — konkrete Inti-Randkommentare

| Z. (im Lerndokument) | Behauptung | Quelle | Inti-Frage | Aktion |
|---|---|---|---|---|
| 330 | Bildungschancen hängen von sozialer Herkunft ab | `erzinger2023pisa` | „welche genauen Seiten sind aus erzinger2023pisa relevant?" | Volltext, exakte Seiten in PISA-Bericht 2022 (vermutlich Kap. zu Migrationshintergrund S. 60–80) |
| 335 | Helle Köpfe / Migrationshintergrund | `kellerkoller2021hellekoepfe` | „kellerkoller2021hellekoepfe ist S. 76–78" | Bib korrigieren, Lerndokument-Zitat unverändert |
| 335 | leikhof2021jugendliche | `leikhof2021jugendliche` | „welche Seiten?" | Volltext, Kap. 1–3 verorten |
| 370 | Under-Identifikation in Kappus | `kappus2010migration` | „auf welchen Seiten?" | Volltext beschaffen, S. 70–74 verorten |
| 449 | Renzulli Drei-Ringe-Modell | `preckel2013hochbegabung` etc. | „bei preckel2013hochbegabung S. 15, bei trautmann2016einfuehrung S. 52–54, bei muelleroppliger2021handbuch auf S. ?" | Müller-Oppliger 2021 *Begabungsmodelle* S. 204–223 ist die zentrale Stelle |
| 459 | Münchner Hochbegabungsmodell | `muelleroppliger2021handbuch` | „in muelleroppliger2021handbuch auf S. 211, in trautmann2016einfuehrung S. 59–62" | exakte Bib-Notes ergänzen |
| 465 | Fischer Begabungsförderung Lernarchitekturen | `fischer2020begabungsfoerderung`, `muelleroppliger2021handbuch` | „auf welchen Seiten in fischer2020begabungsfoerderung S. 253–267? Geht es dabei auch um Lernarchitekturen wie in muelleroppliger2021handbuch S. 374–387?" | Beide Stellen in Bib-Notes ergänzen |
| 470 | Maehler sprach-/kulturfair | `maehler2018diagnostik` | „auf welchen Seiten?" | Volltext liegt vor (PDF 402 S.), exakte Stellen verorten |
| 475 | Stamm „begabte Minoritäten" | `stamm2021fehlenderblick` | „auf welchen Seiten?" | Volltext beschaffen, Stamm-Zitat S. 580–585 verorten |
| 478 | Keller-Koller Underachievement + Migration | `kellerkoller2021hellekoepfe` | „in kellerkoller2021hellekoepfe S. 76–78" | Bib + Lerndokument konsistent |
| 481 | iPEGE 5 Strategien | `ipege2009professionelle` | „auf welcher Seite stehen diese?" | Volltext liegt vor (PDF 53 S.), exakte Seite verorten |
| 481 | Reutlinger | `reutlinger2015hochbegabung` | „in reutlinger2015hochbegabung S. 11–22?" | Bib + exakte Seite |
| 489 | 2e bei Preckel | `preckel2013hochbegabung` | „auf S. ca. 36–50?" | EPUB liegt vor, exakte Seiten verifizieren |
| 489 | Lehwald Motivation | `lehwald2017motivation` | „auf welcher Seite?" | Volltext-Auszug, beschaffen |
| 494 | Stern 2025 | `stern2025intelligenz` | „beStern ist es ein Interview ca. 4 Seiten lang" | Bib `pages = {?}` ergänzen |
| 504 | Renzulli SEM | `muelleroppliger2021handbuch` | „auf welcher Seite?" | Renzulli/Reis SEM-Kapitel S. 333–347 |
| 511 | Gardner Multiple Intelligenzen | — | „huser2025 S. 8–11, 88–94" | Hoyer 2013 hat MI-Kapitel als Sekundärbeleg, oder Trautmann 2016 |
| 525 | Münchner Modell — nicht-kognitive Faktoren | — | „was ist mit nicht-kognitive Faktoren gemeint?" | Müller-Oppliger 2021 S. 211, Heller/Perleth-Originalstelle einarbeiten |
| 535 | LemaS Begriffsklärung | `lemas2023begriffsklaerung` | „sind das insgesamt nur 5 Seiten?" | Online-PDF, Bib-`note` ergänzen |
| 562 | Reutlinger Verhaltensauffälligkeiten | `reutlinger2015hochbegabung` | „Steht dies auf Seite 7?" | exakte Seite verifizieren |
| 564 | Webb Doppeldiagnosen | `webb2020doppeldiagnosen` | „wenn ja auf welcher Seite?" | Volltext beschaffen |
| 580 | Stamm MIRAGE | `stamm2014mirage`, `stamm2014handbuch` | „S. 11–22 und 375–382?" | Volltext liegt vor, exakte Seiten |
| 588 | Maehler Test-Empfehlungen | `maehler2018diagnostik` | „auf welchen Seiten? aktuell mit genauer Seitenanzahl" | Volltext, max. 10–20 Seiten ausweisen |
| 600 | Lehwald antizipatorische Vermeidung | `lehwald2017motivation` | „auf welchen Seiten und Kapitel?" | Volltext beschaffen |
| 1313 | Webb diagnostische Falle | `webb2020doppeldiagnosen` | „Kap. 2 + Kap. 12 S. 376?" | Volltext, exakte Stellen |
| 1356 | Maskierungs-Stellen 2e | `preckel2013hochbegabung` | „in preckel2013hochbegabung S. 47" | EPUB, exakte Seite |
| 1356 | Stamm Migration in 2e | `stamm2014handbuch` | „passt hier S. 393–400 hinein?" | Bib + Stelle dokumentieren |
| 1620 | Lehwald Antizipatorische Vermeidung — Underachievement | `lehwald2017motivation` | „Hinweis auf Underachievement?" | Volltext, Underachievement-Stelle markieren |

(Die vollständige Liste umfasst ~70 Inti-Randkommentare im Lerndokument und ist als **Arbeitsliste** zu verstehen, nicht als Abgabe-Pflicht. Phase 3 trägt die wichtigsten 20 in `verified_quotes.md` ein.)

## B.1.2 · Mehrquellen-Bündelung — Beispiele

| Behauptung | Aktuell | Vorschlag |
|---|---|---|
| Renzulli Drei-Ringe-Modell | `\parencite{muelleroppliger2021handbuch, trautmann2016einfuehrung, preckel2013hochbegabung}` | OK — Mehrquellen-Bündelung bereits gegeben, exakte Seiten ergänzen |
| 5 iPEGE-Strategien | `\parencite{ipege2009professionelle, reutlinger2015hochbegabung, uslucan2012begabung}` | Inti-Frage: „sind das wirklich 5 oder 3?" → Volltext-Stelle suchen, ggf. auf 3 reduzieren |
| Stamm 2025 „von unten nach oben" | nicht zitiert | Inti-Vorschlag: ergänzend bei Frage 1 zu Migrationsreserven aufnehmen, falls Volltext beschaffbar |

## B.1.3 · Behauptungen weicher formulieren

| Z. | Aktuelle Behauptung | Problem | Aktion |
|---|---|---|---|
| 162 (mpv.tex) / 161 (Abgabe) | „Bildungschancen hängen weiterhin **stark** ab" | Stark = wertend | OK so, wenn PISA-Beleg in `note` |
| 175 (Abgabe) | „Thema hat **insgesamt geringe Priorität**" | DVS-Webseite belegt das nicht so wörtlich | weicher: „… und ist nur in einem Teil der Schulen institutionell verankert" |
| FW3 / 234 | „Belastungs-Erfahrungen" | pathologisierend | wegnehmen, dafür „kumulative Belastungen im Sinne von Behrensen 2019" im Fliesstext |
| BW4 / 238 | „**systematisch** übersehen" | starke Behauptung | belegen mit Stamm 2021 + Mun 2020 (mündlich), oder „häufig übersehen" |

---

# Aktionsliste (Konsequenzen für Phase 1, 2, 3)

## Für Phase 1 (Bibliographie schliessen)

1. `kellerkoller2021hellekoepfe`: `pages = {76--78}` (statt `XXX--XXX`).
2. `stamm2021fehlenderblick`: `pages = {576--588}` (verifiziert via Beltz-Inhaltsverzeichnis).
3. `kuhl2019diversitaet`: `pages = {35--57}` belassen (Inhaltsverzeichnis bestätigt).
4. `macha2019gender`: `pages = {160--172}` belassen.
5. `brunner2021hochbegabung`: **Eintrag löschen** (E5 = C).
6. Ergänze in den `note`-Feldern der High-Cite-Quellen die exakten Belegstellen aus B.1.1.
7. Handbuch-Begabung-Nebeneinträge (`baudson2021wasdenken` S. 115–131, `grabnermeier2021expertise` S. 149–167, `trautmann2021haltung` S. 496–510): durch Beltz-Inhaltsverzeichnis bereits verifiziert; VERIFY-Kommentare entfernen.

## Für Phase 2 (Volltextbeschaffung A-Korpus)

**ROT-Keys mit hoher Cite-Zahl im Abgabedokument** (Priorität für Bibliotheks-Bestellung):

1. `booth2019index` (11 cites) — Index für Inklusion
2. `kappus2010migration` (11 cites) — Umgang mit Heterogenität
3. `muelleroppliger2021handbuch` (11 cites) — Handbuch Begabung
4. `gold2018lesenkannmanlernen` (9 cites) — Lesen kann man lernen
5. `trautmann2016einfuehrung` (9 cites) — Einführung Hochbegabtenpädagogik
6. `rosebrock2010grundlagen` (8 cites) — Grundlagen Lesedidaktik
7. `burow2021positive` (7 cites) — Positive Pädagogik
8. `stamm2021fehlenderblick` (7 cites) — Handbuch Begabung Kap.
9. `webb2020doppeldiagnosen` (7 cites) — Doppeldiagnosen
10. `grossrieder2010anerkennung` (6 cites) — Anerkennung Kap.
11. `kellerkoller2021hellekoepfe` (6 cites) — Huser Kap.
12. `burow2020future` (5 cites) — Future Fridays
13. `lemas2023begriffsklaerung` (5 cites) — Online-PDF
14. `sedmak2021bildungsgerechtigkeit` (5 cites) — Handbuch Begabung Kap.
15. `stamm2012migranten` (5 cites) — Dossier 12/4
16. `weigand2021separativ` (5 cites) — Handbuch Begabung Kap.

**GELB-K-Fälle** (kurzer PDF-Auszug — vollständigen Band beschaffen):

17. `buholzer2010allegleich` (13 cites) — nur 2-S.-PDF
18. `lehwald2017motivation` (13 cites) — nur 13-S.-PDF
19. `behrensen2019inklusive` (6 cites) — 13 S.-PDF könnte vollständiger Kapitel-Auszug sein
20. `macha2019gender` (7 cites) — 13 S.-PDF könnte vollständiger Kapitel-Auszug sein

## Für Phase 3 (verified_quotes.md)

Pro Top-10-Key aus Phase-2-Liste: konkretes Belegzitat mit Seite in `Literatur/<key>/verified_quotes.md` eintragen, sodass Status mindestens 3 (Transkript-konsistent) erreicht.

---

**Bearbeitet durch:** _______ Datum: _______
