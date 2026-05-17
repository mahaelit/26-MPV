# Verifizierte Zitate – muelleroppliger2021plurale

**Quelle:** Müller-Oppliger, Victor (2021). Plurale Gesellschaft, Inklusion und Bildungsgerechtigkeit. In: Müller-Oppliger, Victor & Weigand, Gabriele (Hrsg.), *Handbuch Begabung* (S. 32–45). Weinheim und Basel: Beltz. ISBN 978-3-407-25806-9.
**Lokaler Pfad:** `source.pdf` (1400 px / Q70 komprimiert, 4.49 MB; Original 37.4 MB Foto-Scan)
**Renderings:** `pages/p01_S32.jpg` … `pages/p12_S43.jpg` (1600 px Q75)

**Status:** **5** (wortgetreu, zitierfähig)
**Verifiziert am:** 2026-05-17 (Pass-2 Vision-Verifikation)

> **Vortragsrelevanz:** V4 Theorie-Anker (Inklusive Begabungsförderung als bildungspolitischer Auftrag, „Gleichheit ≠ Gerechtigkeit", drei Ebenen inklusiver Begabungsförderung). Jetzt 3. Status-5-Anker für Vortrag 4.

---

## 1. Locator-Verifikation der mpv.tex-Inline-Cites — KRITISCHE BEFUNDE

In `mpv.tex` wird `muelleroppliger2021plurale` an 4 Stellen zitiert. **Zwei Locator-Befunde.**

| mpv.tex-Zeile | Locator | Aussage | Verifikation |
|---|---|---|---|
| **L:2752** | `[S.\,32--45]` | „Begabungsförderung als integraler Bestandteil inklusiver Schulentwicklung, nicht als Zusatzangebot" | ✓ funktional korrekt (Gesamtbeitrag-Argument) — **Z01 + Z05 + Z06** |
| **L:3062** | `[S.\,32--45]` | „Wenn Schule alle Kinder fördern will, gesamtschulische Aufgabe" | ✓ funktional korrekt — **Z05 + Z06** (drei Ebenen S. 40) |
| **L:3179** | `[vgl.][S.\,41\psq]` | „15 Prozent ... fremdsprachiger Knaben ... 88 Prozent deutschsprachiger Mädchen" | **❌ LOCATOR FALSCH** — Zahlen stehen exakt auf **S. 38**, nicht S. 41ff. → korrigiere zu `[vgl.][S.\,38]` |
| **L:3326** | `[vgl.][S.\,40--42]` | „Begabungsförderung erreicht überproportional Kinder aus bildungsnahen Familien" | ⚠ funktional ungenau: Diagnose der sozialen Selektivität steht auf **S. 36** (Z03); S. 40-42 trägt die Lösung (drei Ebenen, Z06). Präziser wäre `[vgl.][S.\,36,\,40--42]` |

**Korrekturen in `mpv.tex` umzusetzen:**
1. L:3179: `[vgl.][S.\,41\psq]` → `[vgl.][S.\,38]`
2. L:3326 (optional): `[vgl.][S.\,40--42]` → `[vgl.][S.\,36,\,40--42]`

---

## 2. Wortgetreue Zitate

### Z01 — Salamanca-Erklärung der UNESCO als bildungspolitisches Fundament (S. 32)

> „Ausdruck dieses Bekenntnisses ist die internationale *Erklärung von Salamanca* der UNESCO (1994) zur Bildung junger Menschen, die eine zentrale Grundlage für die Bildungsgesetzgebung westlicher Wissensgesellschaften darstellt und den Anspruch jedes Menschen auf eine Bildung, die seinen Fähigkeiten und Möglichkeiten angemessen ist, als demokratisches Grundrecht proklamiert."
> *(Müller-Oppliger 2021, S. 32)*

**Trägt:** mpv.tex L:2752 (bildungspolitische Rahmung der Inklusion + plurale Gesellschaft).

### Z02 — Gleichheits-Gerechtigkeits-Fehlschluss (S. 37, §4.3)

> „Diese verhängnisvolle Verwechslung von Gleichheit und Gerechtigkeit prägt nach wie vor weite Teile einer noch immer verbreiteten Unterrichtsdidaktik der »Gleichmacherei« und Organisation von uniformen Lernstrukturen. Anstatt dem Schüler bzw. der Schülerin gerecht zu werden, steht oft der Grundgedanke »Für alle das Gleiche« im Zentrum didaktischen Handelns. Allerdings führt dieser Grundsatz bei der Leistungsbewertung — und dies mag zynisch erscheinen — zum genauen Gegenteil, nämlich zur Verstärkung von Unterschieden zwecks Selektion. Ungleiche werden gleich behandelt, was — als Paradoxie — zu verstärkter Ungleichheit führt."
> *(Müller-Oppliger 2021, S. 37)*

**Verwendung:** Theoretische Grundlage für die V4-Argumentation, dass formale Gleichbehandlung (gleiche Aufgaben, gleiche Tests) bei ungleichen Voraussetzungen Ungleichheit verstärkt. Direkt anschlussfähig an S.s Situation als sprachlich Benachteiligter.

### Z03 — Soziale Selektivität: Gymnasialbesuch (S. 36, §4.1)

> „Während der Gymnasialbesuch überproportional häufig deutschsprachigen Schüler/innen aus höheren Sozialschichten ermöglicht wird, finden sich in der Hauptschule zahlreiche Schüler/innen aus »bildungsfernen« Familien als Bildungsverlierer (Baumert/Stanat/Watermann 2006, S. 174; Ditton 2007)."
> *(Müller-Oppliger 2021, S. 36)*

**Trägt:** mpv.tex L:3326 (Begabungsförderung erreicht überproportional bildungsnahe Familien) — **dies ist der eigentliche Diagnose-Beleg**, nicht S. 40-42.

### Z04 — Risikogruppen unerkannter Begabungen (S. 36, §4.2)

> „Eine breite Forschungsliteratur identifiziert verschiedene Risikogruppen, denen es aus unterschiedlichen Gründen — die in der Person oder in der Ignoranz des Bildungssystems angelegt sein können — nicht gelingt, ihr Potenzial in adäquate Leistungen umzusetzen: Fremdsprachige (Stamm 2009), sozial Benachteiligte und Bildungsferne, stille Lernende mit wenig Selbstvertrauen, die sich nicht äußern, um nicht aufzufallen, Lernende, die unter dysfunktionalem Perfektionismus leiden (Schuler 2000; Greenspon 2012), besonders originelle und lebhafte Kinder, denen Unerwartetes in den Sinn kommt, das eher als Störung denn als kreativer Beitrag zum Unterricht gewertet wird, Minderleister/innen (»Underachiever«) aus Unterforderung oder mit mangelhaften Fähigkeiten zur Selbststeuerung (Siegle/McCoach 2005; Reis/McCoach 2000), manchmal auch hochsensible oder hypersensible Kinder (»Overexcitabilities«) [...] Besonderes Augenmerk verdienen auch die sogenannten »Twice Exceptionals«, also Schüler/innen, die trotz Hochbegabungspotenzialen zugleich Lern- oder Verhaltensdefizite aufweisen (Baum/Schader/Oven 2017; Baum/Schader auf S. 588 ff. in diesem Band)."
> *(Müller-Oppliger 2021, S. 36)*

**Trägt:** Direkter Beleg für mpv.tex-Argument, dass S. **als neu zugewanderter, fremdsprachiger Knabe** zentrale Merkmale dieser Risikokonstellation aufweist. Inti zitiert Stamm 2009 (= `stamm2021fehlenderblick`-Vorgänger) bereits ausführlich; hier wird der Sammelbegriff der „unerkannten Begabungen" systematisiert.

### Z05 — KERN-ZAHLEN: 15 % vs. 88 % (S. 38, §4.5) ⭐ Locator-Korrektur

> „Die Daten dieser Untersuchung stammen aus 112 Klassen aus allen Kantonen der deutschsprachigen Schweiz mit insgesamt 2.104 Schüler/innen. Besonders dramatisch hinsichtlich (zu) niedriger Zuweisungsentscheide zeigt sich die Situation für fremdsprachige männliche Schüler. Lediglich 15 Prozent der männlichen Schüler mit Fremdsprachenhintergrund wurden aufgrund ihrer Leistungen für höhere Schulstufen qualifiziert; demgegenüber wurden 88 Prozent der deutschsprachigen Mädchen anspruchsvolleren Schulstufen zugewiesen."
> *(Müller-Oppliger 2021, S. 38)*

**KRITISCHER LOCATOR-BEFUND:** mpv.tex L:3179 zitiert mit `[S.\,41\psq]` — **die Zahlen stehen aber exakt auf S. 38** (Off-by-3-Fehler). Korrektur in mpv.tex erforderlich.

**Trägt:** mpv.tex L:3179 (S.s Risikokonstellation als „neu zugewanderter, fremdsprachiger Knabe" anhand harter Zahlen).

**Kontext (auch S. 38, §4.5 Beginn):**

> „Unter dem Aspekt teilweise noch gegliederter Sekundarschulstufen weist Kronig (2007) mit seiner Forschung zur »systematischen Zufälligkeit des Bildungssystems« auf die prekäre Situation hin, dass die Schulartzuweisung an Sekundarschulen aufgrund unterschiedlicher und teilweise fragwürdiger Bewertungspraktiken und Verzerrungen mehrheitlich zufällig ist. Die Leistungen der untersuchten Schüler/innen zeigten eine Überlappung der Schulstufen von 85 Prozent. Trotz gleicher Leistungen fanden sich Lernende in unterschiedlichen schulischen Bildungsgängen zwischen Gymnasium und Hauptschule. Die »meritokratische Grauzone« — so zeigte sich — ist abhängig von Lehrpersonen mit unterschiedlichen Erwartungen und Bewertungsmethoden, unterschiedlichen Lern- und Bezugsgruppen sowie weiteren lokalen und institutionellen Gegebenheiten."
> *(Müller-Oppliger 2021, S. 38)*

### Z06 — Drei Ebenen inklusiver Begabungsförderung (S. 40, §5.3)

> „Der Begriff der Inklusion steht für den Anspruch auf »Barrierefreiheit«. Diese Leitvorstellung gilt auch für die Umsetzung der Inklusion in der Bildung, die sich in drei Ebenen verwirklichen lässt:
> - leistungsdifferenzierender Unterricht, der die unterschiedlichen Potenziale und Interessen der einzelnen Lernenden mitberücksichtigt;
> - den regulären Unterricht ergänzende Förderangebote, die spezifische Talente besonderer Lernenden innerhalb der eigenen Schule fördern, verstärken und anerkennen, sowie
> - zunehmende Kooperation der Schule mit außerschulischen Förderorten oder Institutionen (z. B. Mentorate oder Frühstudium)."
> *(Müller-Oppliger 2021, S. 40)*

**Trägt:** mpv.tex L:2752 + L:3062 (Begabungsförderung als gesamtschulische Aufgabe in drei Ebenen). **Direkter Beleg für die V4-Schulentwicklungs-Argumentation** und für die SHP-Triade-Forderung nach Multiprofessionalität (Ebene 3).

### Z07 — Demokratie und Inklusion (S. 39, §5.1)

> „Dabei schließt Inklusion an humanistische Grundsätze und demokratische Prinzipien an. Mit den Worten John Dewey (1993, S. 121) ist die Demokratie »mehr als eine Regierungsform; sie ist in erster Linie eine Form des Zusammenlebens, der gemeinsamen und miteinander geteilten Erfahrung«. Oder wie Kersten Reich (2014, S. 11) definiert: »Demokratie und Inklusion bedingen einander«."
> *(Müller-Oppliger 2021, S. 39)*

**Trägt:** Theoretische Grundlage „Inklusion ≠ Sonderpädagogik" — Inklusion als demokratisches Prinzip aller Schüler:innen. Direkter Anschluss an mpv.tex-Inklusions-Argumentation in V3 + V4.

### Z08 — Inklusionskritik der Sonderpädagogik-Verengung (S. 39)

> „Auftrieb erhielt der Inklusionsansatz vor allem durch die Arbeiten von Ainscow, Armstrong und Barton (1999) vom britischen *Centre for Studies on Inclusive Education* und dem daraus hervorgegangenen *Index for Inclusion* von Booth und Ainscow (1998), der von Ines Boban und Andreas Hinz (2003) für den deutschsprachigen Raum bearbeitet wurde. Dabei wurde leider versäumt, Inklusion so breit zu definieren, dass auch Hochleistende und Hochbegabte mit ihren spezifischen Bedürfnissen inkludiert sind. Nur allzu oft wird Inklusion von Lehrpersonen, Schulbehörden und Bildungsverantwortlichen noch einseitig durch die Brille der Lern-, Körper- oder sozialen Beeinträchtigung verstanden und damit im heil- oder sonderpädagogischen Feld der Pädagogik verortet."
> *(Müller-Oppliger 2021, S. 39)*

**Verwendung:** Direkter Beleg für die SHP-Selbstkritik in V4/V5: Inklusion darf nicht auf Defizit-Sonderpädagogik verengt werden, sondern muss auch Hochbegabte einschließen. Anschlussfähig an Intis SHP-Triade.

---

## 3. Audit-Befunde

### 3.1 Locator-Korrektur erforderlich (kritisch)

**mpv.tex L:3179** zitiert die Zahlen „15 Prozent fremdsprachiger Knaben" und „88 Prozent deutschsprachiger Mädchen" mit `[vgl.][S.\,41\psq]`. Vision-Verifikation am komprimierten PDF zeigt: Diese Zahlen stehen exakt auf **S. 38** (§4.5 „Fragwürdige und ungerechte Selektionsentscheidungen"). Off-by-3-Locator-Fehler. **Korrektur:** `[vgl.][S.\,41\psq]` → `[vgl.][S.\,38]`.

### 3.2 Locator-Präzisierung empfohlen (optional)

**mpv.tex L:3326** zitiert die These „Begabungsförderung erreicht überproportional Kinder aus bildungsnahen Familien" mit `[vgl.][S.\,40--42]`. Vision-Verifikation zeigt: Die **Diagnose** der sozialen Selektivität steht auf **S. 36** (§4.1, Z03). S. 40-42 trägt die **Lösungsstrategie** (drei Ebenen, Z06). Funktional vertretbar, aber präziser wäre `[vgl.][S.\,36,\,40--42]`.

### 3.3 PDF-Vollständigkeit

PDF endet auf S. 43 (Bibliographie-Mitte bei „Müller-Oppliger, V. (2015)"). **Beitrag-Inhalt** ist vollständig (S. 32–42); fehlend sind nur 2 Bibliographie-Seiten (S. 44–45) mit Einträgen M-Z. Für die wissenschaftliche Argumentation **unkritisch**.

### 3.4 PDF-Kompression

Original 37.4 MB Foto-Scan → komprimiert auf 4.49 MB (Faktor 8.3) via `archiv/compress_pdfs.py` (1400 px / Q70). Original gelöscht.

### 3.5 Audio-Transkript ist nicht zitierfähig (gleiche Befund wie bei `muelleroppliger2021begabungsmodelle`)

Im Sammelband-Ordner `Literatur/muelleroppliger2021handbuch/excerpts/teil1_*.md` liegt das Audio-Transkript des Beitrags. Die thematische Übersicht ist nützlich, der Wortlaut wegen Hörfehlern aber **nicht zitierfähig**. Alle wortgetreuen Zitate dieser Datei stammen aus der Vision-Inspektion der JPEG-Renderings.

---

## 4. Vortrags-Verwendung

- **Vortrag 4 (Begabungsförderung als Schulentwicklungsaufgabe):**
  - Bildungspolitische Rahmung: **Z01** (Salamanca-Erklärung)
  - Theoretische Grundlage: **Z02** (Gleichheits-Gerechtigkeits-Fehlschluss)
  - Diagnose: **Z03 + Z05** (soziale Selektivität, harte Zahlen 15%/88%)
  - Risikogruppen-Systematik: **Z04** (Fremdsprachige, Underachiever, Twice Exceptionals)
  - Lösungsstruktur: **Z06** (drei Ebenen inklusiver Begabungsförderung)
  - Demokratie-Bezug: **Z07** (Dewey-Reich)
  - SHP-Selbstkritik: **Z08** (Inklusion ≠ Sonderpädagogik-Verengung)

- **Vortrag 3 (Anerkennung):** **Z02 + Z08** als Stützliteratur für Anerkennungs-Argumentation.

---

**Bearbeitet durch:** Cascade · 2026-05-17
**Methode:** Pass-2 Vision-Inspektion der JPEG-Renderings (1600 px Q75) der 12 PDF-Seiten. Status 0 (Template) → 5. Alte Status-0-Vorlage als `verified_quotes.md.status0-template-backup` archiviert.
