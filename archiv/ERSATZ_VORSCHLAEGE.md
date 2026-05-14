# Ersatz-Analyse – ROT-Cites durch Zusatz-Quellen ersetzen

Pro **ROT-Cite** (Originalquelle nicht als Volltext verfuegbar) werden die
besten Kapitel-Splits aus folgenden **4 Zusatz-Quellen** gesucht:

- `behrensen2016grundwissen` – Behrensen, Birgit and Solzbacher, Claudia (2016), 37 Splits
- `brackmann2013jenseits` – Brackmann, Andrea (2013), 98 Splits
- `preuss2018inklusive` – Preuß, Bianca (2018), 26 Splits
- `reintjes2019begabungsfoerderung` – Reintjes, Christian and Kunze, Ingrid and Ossowski, Ekkehard (2019), 117 Splits

**Threshold:** nur Matches mit Score >= 0.25 werden gelistet (empirisch kalibriert).

**Score-Interpretation:**
- `>= 0.5` : sehr wahrscheinlicher Ersatz, Kontext passt thematisch genau
- `0.3-0.5` : plausibler Kandidat, Volltext pruefen
- `0.25-0.3` : schwacher Hinweis, thematisch ungefaehr aehnlich

---

## Zusammenfassung

- **22** ROT-BibKeys mit Cite-Stellen analysiert
- **92** ROT-Cite-Stellen insgesamt
- **10** davon haben mindestens einen Ersatz-Kandidaten (Score >= 0.25)
- **1** haben einen **starken** Kandidaten (Score >= 0.5)

### Pro ROT-Quelle: Anteil Cites mit Ersatz-Kandidat

| ROT-Quelle | Cites | mit Ersatz | davon STRONG |
|---|---:|---:|---:|
| `booth2019index` | 7 | 0 | 0 |
| `gold2018lesenkannmanlernen` | 7 | 0 | 0 |
| `kappus2010migration` | 7 | 0 | 0 |
| `muelleroppliger2021handbuch` | 7 | 1 | 0 |
| `trautmann2016einfuehrung` | 7 | 1 | 1 |
| `rosebrock2010grundlagen` | 6 | 0 | 0 |
| `burow2021positive` | 5 | 1 | 0 |
| `lemas2023begriffsklaerung` | 5 | 0 | 0 |
| `stamm2021fehlenderblick` | 5 | 0 | 0 |
| `dvs2025bbf` | 4 | 0 | 0 |
| `grossrieder2010anerkennung` | 4 | 0 | 0 |
| `kellerkoller2021hellekoepfe` | 4 | 0 | 0 |
| `burow2020future` | 3 | 0 | 0 |
| `sedmak2021bildungsgerechtigkeit` | 3 | 2 | 0 |
| `stamm2012migranten` | 3 | 0 | 0 |
| `webb2020doppeldiagnosen` | 3 | 0 | 0 |
| `weigand2021separativ` | 3 | 2 | 0 |
| `kellerkoller2009begabte` | 2 | 0 | 0 |
| `muelleroppliger2021plurale` | 2 | 2 | 0 |
| `stamm2014handbuch` | 2 | 0 | 0 |
| `unger2010begabungsfoerderung` | 2 | 1 | 0 |
| `stern2025intelligenz` | 1 | 0 | 0 |

---

## `booth2019index` – Booth, Tony and Ainscow, Mel (2019)

Titel: Index für Inklusion: Ein Leitfaden für Schulentwicklung
**7 Cite-Stellen**

### L:1297 (parencite)
[`mpv.tex:1297`](mpv.tex#L1297)

> Booth und Ainscow beschreiben im Index für Inklusion, dass Teilhabe nicht allein durch Anwesenheit, sondern durch die Erfahrung von Akzeptanz, Mitgestaltung und Wertschätzung entsteht \parencite{booth2019index}.

- Kein Ersatz-Match ueber Threshold gefunden.

### L:1416 (parencite)
[`mpv.tex:1416`](mpv.tex#L1416)

> ugendlichen an der Gemeinschaft partizipieren, anerkannt werden und Lernangebote erhalten, die ihren Bedürfnissen und Fähigkeiten entsprechen. Drei Dimensionen strukturieren den Index: inklusive Kulturen schaffen (Dimension A), inklusive Strukturen etablieren (Dimension B) und in…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:1499 (textcite)
[`mpv.tex:1499`](mpv.tex#L1499)

> \textcite{booth2019index} betonen, dass individuelle Massnahmen für einzelne Kinder nur dann nachhaltig wirken, wenn sie in eine Schulkultur eingebettet sind, die Teilhabe für alle als Leitwert versteht. Im Fall S. bedeutet dies, dass die positive Dynamik des SOLUX-Projekts nicht…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:1585 (parencite)
[`mpv.tex:1585`](mpv.tex#L1585)

>  Ainscow fordern, dass Barrieren für Lernen und Teilhabe in den Strukturen und Praktiken der Schule identifiziert werden, nicht im Verhalten einzelner Kinder. Der Verweis lokalisiert das Problem im Kind; eine inklusive Perspektive fragt, was an der Unterrichtssituation verändert …

- Kein Ersatz-Match ueber Threshold gefunden.

### L:1658 (parencite)
[`mpv.tex:1658`](mpv.tex#L1658)

> ne solche Praxis. Sie zu verändern erfordert nicht nur individuelle Beratung, sondern eine Auseinandersetzung auf der Ebene der Schulkultur, wie sie Booth und Ainscow in Dimension A des Index für Inklusion beschreiben: die Frage, ob die Gemeinschaft so gestaltet ist, dass alle ih…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:1877 (textcite)
[`mpv.tex:1877`](mpv.tex#L1877)

> \textcite{booth2019index} formulieren in Dimension C des Index für Inklusion (Inklusive Praktiken entwickeln) Indikatoren, die sich als Qualitätskriterien für Begabungsförderungsprojekte lesen lassen: Wird der Unterricht so geplant, dass er das Lernen aller unterstützt? Werden Un…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:1971 (parencite)
[`mpv.tex:1971`](mpv.tex#L1971)

> : Es stellt eine inklusive Praktik dar, die unter günstigen Bedingungen wirksam ist. Solange diese Praktik jedoch nicht in die Kultur (A) und die Strukturen (B) der Schule eingebettet ist, bleibt sie eine Insel. Booth und Ainscow betonen, dass nachhaltige Veränderung nur gelingt,…

- Kein Ersatz-Match ueber Threshold gefunden.

---

## `burow2020future` – Burow, Olaf-Axel (2020)

Titel: Future Fridays -- Warum wir das Schulfach Zukunft brauchen
**3 Cite-Stellen**

### L:2130 (parencite)
[`mpv.tex:2130`](mpv.tex#L2130)

> g, die nicht belehrend, sondern reflexiv vorgeht. Burow beschreibt im Rahmen der Positiven Pädagogik, wie ein Fokuswechsel von Defiziten zu Stärken gelingt: nicht durch Appelle, sondern durch die gemeinsame Erfahrung, dass Kinder in geeigneten Settings Kompetenzen zeigen, die im …

- Kein Ersatz-Match ueber Threshold gefunden.

### L:2221 (parencite)
[`mpv.tex:2221`](mpv.tex#L2221)

> n bietet, in dem das SOLUX-Projekt nicht als Ausnahme, sondern als Modell für eine veränderte Unterrichtskultur legitimiert werden kann. Die Beratung gewinnt an Überzeugungskraft, wenn sie nicht nur auf Einzelfallbeobachtungen verweist, sondern diese in einen bildungstheoretisch …

- Kein Ersatz-Match ueber Threshold gefunden.

### L:2577 (parencite)
[`mpv.tex:2577`](mpv.tex#L2577)

> Burow formuliert in \textit{Future Fridays} die Forderung nach einer Schulkultur, die Eigenverantwortung und die Bereitschaft zum produktiven Dissens fördert, statt Konformität zu belohnen \parencite{burow2020future}.

- Kein Ersatz-Match ueber Threshold gefunden.

---

## `burow2021positive` – Burow, Olaf-Axel (2021)

Titel: Positive Pädagogik: Sieben Wege zu Lernfreude und Schulglück
**5 Cite-Stellen**

### L:2130 (parencite)
[`mpv.tex:2130`](mpv.tex#L2130)

> g, die nicht belehrend, sondern reflexiv vorgeht. Burow beschreibt im Rahmen der Positiven Pädagogik, wie ein Fokuswechsel von Defiziten zu Stärken gelingt: nicht durch Appelle, sondern durch die gemeinsame Erfahrung, dass Kinder in geeigneten Settings Kompetenzen zeigen, die im …

- Kein Ersatz-Match ueber Threshold gefunden.

### L:2190 (textcite)
[`mpv.tex:2190`](mpv.tex#L2190)

> \textcite{burow2021positive} entwickelt mit der Positiven Pädagogik einen Ansatz, der den Perspektivenwechsel von der Defizit- zur Ressourcenorientierung nicht als moralischen Appell formuliert, sondern als systematische Veränderung der pädagogischen Praxis.

- [OK] score=0.286: [`038_3_die_person_als_grundlage_einer_paedagogischen_th.pdf`](Literatur/reintjes2019begabungsfoerderung/excerpts/038_3_die_person_als_grundlage_einer_paedagogischen_th.pdf) S.78-78 – 3 Die ‚Person‘ als Grundlage einer pädagogischen Theorie und Praxis der Begabungs- und Begabtenförderung  _(reintjes2019begabungsfoerderung)_

### L:2211 (parencite)
[`mpv.tex:2211`](mpv.tex#L2211)

> echnik verstanden werden darf, sondern als Grundhaltung, die sich in der gesamten Interaktionskultur niederschlägt. Der dritte Weg betrifft die \textit{Potenzialentfaltung}: Schule soll nicht auf Defizitausgleich reduziert werden, sondern Räume schaffen, in denen Kinder ihre Mögl…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:2515 (parencite)
[`mpv.tex:2515`](mpv.tex#L2515)

> Positiven Pädagogik beschreibt: nicht durch Appelle oder Belehrung, sondern durch die gemeinsame Konfrontation mit konkreten Beobachtungen einen Perspektivenwechsel einleiten \parencite{burow2021positive}. Die Frage stellt die Expertise der Fachstellen nicht in Frage; sie erweite…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:3066 (parencite)
[`mpv.tex:3066`](mpv.tex#L3066)

> \enquote{Talent Scouts}} ist eine prägnante Verdichtung der gesamten Argumentation des Lernskripts. Sie lässt sich als internationale Forschungsperspektive einbringen, die Burows Positive Pädagogik empirisch stützt \parencite{burow2021positive}.

- Kein Ersatz-Match ueber Threshold gefunden.

---

## `dvs2025bbf` – Dienststelle Volksschulbildung Luzern (2025)

Titel: Integrative Begabungs- und Begabtenförderung
**4 Cite-Stellen**

### L:342 (parencite)
[`mpv.tex:342`](mpv.tex#L342)

> jedoch stark über schulpsychologische Abklärungen und schulische Leistungen. Gezielte Weiterbildungen zum Thema Begabungsförderung werden nur von einem Teil der Schulen angeboten, und das Thema hat insgesamt geringe Priorität \parencite{dvs2025bbf}. Der Fall S. ist damit nicht ra…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:2080 (parencite)
[`mpv.tex:2080`](mpv.tex#L2080)

> quote{Schulen für alle} bieten den institutionellen Rahmen, in dem diese Forderung realisiert werden kann \parencite{dvs2025bbf}. Die Aufgabe der SHP besteht darin, diesen Rahmen am konkreten Fall zu füllen und die Erfahrungen aus SOLUX als Argument für eine nachhaltige Verankeru…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:3402 (parencite)
[`mpv.tex:3402`](mpv.tex#L3402)

> m Fördersetting. Die Dokumentation aus Camps in Jordanien liefert einen internationalen Referenzpunkt für die Frage, was passiert, wenn institutionelle Identifikationsverfahren ganz fehlen -- eine Situation, die in abgeschwächter Form auch an S.' Schule besteht, wo Begabungsförde…

- Kein Ersatz-Match ueber Threshold gefunden.

### A:176 (parencite)
[`mpv_abgabedokument.tex:176`](mpv_abgabedokument.tex#L176)

> jedoch stark über schulpsychologische Abklärungen und schulische Leistungen. Gezielte Weiterbildungen zum Thema Begabungsförderung werden nur von einem Teil der Schulen angeboten, und das Thema hat insgesamt geringe Priorität \parencite{dvs2025bbf}. Der Fall S. ist damit nicht ra…

- Kein Ersatz-Match ueber Threshold gefunden.

---

## `gold2018lesenkannmanlernen` – Gold, Andreas (2018)

Titel: Lesen kann man lernen: Wie man die Lesekompetenz fördern kann
**7 Cite-Stellen**

### L:855 (parencite)
[`mpv.tex:855`](mpv.tex#L855)

> heiten: inkonsistente Buchstabenformen, erhöhter Stiftdruck, wiederholtes Absetzen. Diese Befunde deuten auf nicht automatisierte sensumotorische Grundlagen hin, die das Schreiben zu einer kognitiv hochbelastenden Tätigkeit machen und damit Ressourcen für inhaltliches Denken bloc…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:860 (textcite)
[`mpv.tex:860`](mpv.tex#L860)

>  Mehrebenenmodell des Lesens, in dem Wort- und Satzidentifikation automatisiert sein müssen, damit Ressourcen für Textverständnis verfügbar werden \parencite{rosebrock2010grundlagen}. \textcite{gold2018lesenkannmanlernen} betont die Bedeutung systematischer Leseförderung, die an …

- Kein Ersatz-Match ueber Threshold gefunden.

### L:915 (parencite)
[`mpv.tex:915`](mpv.tex#L915)

> rfähigkeiten so weit gefestigt sind, dass sie Verarbeitungskapazität für höhere Prozesse freisetzen. Kinder, bei denen diese basalen Fähigkeiten noch nicht automatisiert sind, geraten in eine Überforderungssituation, sobald gleichzeitig motorische, orthographische und inhaltliche…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:955 (textcite)
[`mpv.tex:955`](mpv.tex#L955)

> \textcite{gold2018lesenkannmanlernen} betont, dass Leseförderung bei Kindern mit gravierenden Dekodierungsschwierigkeiten konsequent auf der Wortebene ansetzen muss. Strategien des Textverstehens, die in der didaktischen Praxis häufig im Vordergrund stehen, greifen erst, wenn die…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:1099 (parencite)
[`mpv.tex:1099`](mpv.tex#L1099)

> textit{systematische Leseförderung auf Wortebene}: Parallel zur schreibmotorischen Förderung muss die Leseflüssigkeit aufgebaut werden, beginnend mit Sichtworttraining und Lautleseübungen in kurzen, regelmässigen Einheiten, die schrittweise in den SOLUX-Kontext integriert werden …

- Kein Ersatz-Match ueber Threshold gefunden.

### L:1145 (parencite)
[`mpv.tex:1145`](mpv.tex#L1145)

> nicht automatisierten basalen Fähigkeiten in eine Überforderungssituation geraten, sobald motorische, orthographische und inhaltliche Anforderungen simultan gestellt werden. Das Arbeitsgedächtnis ist in dieser Konstellation vollständig ausgelastet; für die eigentliche kognitive L…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:1205 (parencite)
[`mpv.tex:1205`](mpv.tex#L1205)

> uf Deutsch (König, Dame, Turm, Springer, Läufer, Bauer), einfache Spielanleitungen, Regelkarten für den Peer-Kurs. Gold betont, dass Leseanlässe motivational attraktiv und auf dem aktuellen Kompetenzniveau angesiedelt sein müssen, um den Matthäus-Effekt zu durchbrechen \parencite…

- Kein Ersatz-Match ueber Threshold gefunden.

---

## `grossrieder2010anerkennung` – Grossrieder, Ivo (2010)

Titel: Gleiches und Unterschiedliches anerkennen
**4 Cite-Stellen**

### L:1264 (textcite)
[`mpv.tex:1264`](mpv.tex#L1264)

> \textcite{grossrieder2010anerkennung} beschreibt Anerkennung als pädagogisches Grundprinzip, das über Lob hinausgeht: Anerkennung zweiter Ordnung meint eine Grundhaltung, in der Unterschiedlichkeit nicht defizitär gelesen, sondern respektiert wird.

- Kein Ersatz-Match ueber Threshold gefunden.

### L:1332 (textcite)
[`mpv.tex:1332`](mpv.tex#L1332)

> srieder2010anerkennung} entfaltet den Begriff der Anerkennung in einer Differenzierung, die für die Analyse von S.' Situation aufschlussreich ist. Grossrieder unterscheidet Anerkennung erster und zweiter Ordnung. Anerkennung erster Ordnung ist direkt beobachtbar: Lob, Zuwendung, …

- Kein Ersatz-Match ueber Threshold gefunden.

### L:1573 (parencite)
[`mpv.tex:1573`](mpv.tex#L1573)

> zum Dauerzustand. Grossrieder verweist auf Forschungsergebnisse, wonach ein negatives Klassenklima mit signifikant niedrigerem Selbstwertgefühl und erhöhter Hilflosigkeit bei den Betroffenen einhergeht. Der Verweis verschärft also genau jene psychische Lage, die das Verdecktbleib…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:2311 (parencite)
[`mpv.tex:2311`](mpv.tex#L2311)

> ntliches Wissensdefizit adressiert, sondern als Kollegin, die unter erschwerten Ausgangsbedingungen (Quereinstieg, neues Bildungssystem, neue Schulstufe) eine professionelle Aufgabe übernimmt. Die Anerkennung, die wir für S.\ einfordern, beginnt damit, dass wir sie auch im Umgang…

- Kein Ersatz-Match ueber Threshold gefunden.

---

## `kappus2010migration` – Kappus, Elke-Nicole (2010)

Titel: Umgang mit migrationsbedingter Heterogenität
**7 Cite-Stellen**

### L:370 (parencite)
[`mpv.tex:370`](mpv.tex#L370)

> l, das durch den am Anfang stehenden Zweitspracherwerb, schriftsprachliche Schwierigkeiten, graphomotorische Hürden und mögliche belastende Vorerfahrungen teilweise verdeckt bleibt. Damit besteht die Gefahr einer Under-Identifikation, defizitärer Zuschreibungen und institutionell…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:563 (textcite)
[`mpv.tex:563`](mpv.tex#L563)

> Drittens besteht die Gefahr institutioneller Diskriminierung. \textcite{kappus2010migration} referiert Studien, die darauf hinweisen, dass Kinder mit ausländisch klingenden Nachnamen in einzelnen Deutschschweizer Kantonen deutlich häufiger Zuweisungsempfehlungen für sonderpädagog…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:1288 (textcite)
[`mpv.tex:1288`](mpv.tex#L1288)

> {kappus2010migration} zeigt, dass institutionelle Diskriminierung nicht nur in offener Benachteiligung besteht, sondern in der alltäglichen Praxis der Defizitzuschreibung: Kinder mit Migrationshintergrund erhalten deutlich häufiger Zuweisungen zu sonderpädagogischen Settings als …

- Kein Ersatz-Match ueber Threshold gefunden.

### L:1651 (parencite)
[`mpv.tex:1651`](mpv.tex#L1651)

> vollziehbar erscheinen, in der Summe aber bestimmte Kindergruppen systematisch benachteiligen \parencite{kappus2010migration}. Der Verweis eines Kindes, das aufgrund seiner Migrationsgeschichte und seiner sensumotorischen Schwierigkeiten nicht leisten kann, was erwartet wird, ist…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:2360 (parencite)
[`mpv.tex:2360`](mpv.tex#L2360)

> nder mit einheimischen Namen, wenn Migrationshintergrund statistisch mit niedrigeren Bildungslaufbahnen korreliert und wenn Begabungsförderung faktisch überproportional Kinder aus bildungsnahen Familien erreicht, dann reicht Einzelfallberatung nicht aus. Dann muss die SHP auch in…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:2568 (parencite)
[`mpv.tex:2568`](mpv.tex#L2568)

> estiert, die für sich genommen nachvollziehbar erscheinen \parencite{kappus2010migration}. Die Empfehlung zum Abwarten bei einem neu zugewanderten Kind ist eine solche Routine. Sie ist in vielen Fällen angemessen. In Fällen wie jenem von S., wo sprachunabhängige Auffälligkeiten i…

- Kein Ersatz-Match ueber Threshold gefunden.

### A:204 (parencite)
[`mpv_abgabedokument.tex:204`](mpv_abgabedokument.tex#L204)

> l, das durch den am Anfang stehenden Zweitspracherwerb, schriftsprachliche Schwierigkeiten, graphomotorische Hürden und mögliche belastende Vorerfahrungen teilweise verdeckt bleibt. Damit besteht die Gefahr einer Under-Identifikation, defizitärer Zuschreibungen und institutionell…

- Kein Ersatz-Match ueber Threshold gefunden.

---

## `kellerkoller2009begabte` – Keller-Koller, Irène (2009)

Titel: Begabte mit Migrationshintergrund: Rahmenbedingungen und Erkennung
**2 Cite-Stellen**

### L:465 (parencite)
[`mpv.tex:465`](mpv.tex#L465)

> Keller-Koller zeigt, dass gerade die Kombination von Migrationshintergrund und schulischem Underachievement dazu führt, dass Potenziale verdeckt bleiben, weil Fachpersonen Defizite priorisieren \parencite{kellerkoller2021hellekoepfe,kellerkoller2009begabte}.

- Kein Ersatz-Match ueber Threshold gefunden.

### L:552 (textcite)
[`mpv.tex:552`](mpv.tex#L552)

> llekoepfe} zeigt, dass Kinder mit Migrationshintergrund trotz deutlich sichtbarer Ressourcen bis in die Mittelstufe hinein nie mit Begabtenförderung in Berührung kommen, weil ihre Stärken in Domänen liegen, die schulisch nicht als leistungsrelevant anerkannt werden (vgl. auch \te…

- Kein Ersatz-Match ueber Threshold gefunden.

---

## `kellerkoller2021hellekoepfe` – Keller-Koller, Irène (2021)

Titel: Helle Köpfe mit Migrationshintergrund
**4 Cite-Stellen**

### L:335 (parencite)
[`mpv.tex:335`](mpv.tex#L335)

> r zugewanderten Familien sind in anspruchsvolleren Bildungswegen und Förderangeboten häufig untervertreten; ihre Potenziale bleiben nicht selten verdeckt, insbesondere dann, wenn sprachliche Unsicherheiten, belastende Lebensumstände oder auffälliges Verhalten die Wahrnehmung domi…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:465 (parencite)
[`mpv.tex:465`](mpv.tex#L465)

> Keller-Koller zeigt, dass gerade die Kombination von Migrationshintergrund und schulischem Underachievement dazu führt, dass Potenziale verdeckt bleiben, weil Fachpersonen Defizite priorisieren \parencite{kellerkoller2021hellekoepfe,kellerkoller2009begabte}.

- Kein Ersatz-Match ueber Threshold gefunden.

### L:548 (textcite)
[`mpv.tex:548`](mpv.tex#L548)

>  Kinder am Beginn des Zweitspracherwerbs nicht verfügen. \textcite{kellerkoller2021hellekoepfe} zeigt, dass Kinder mit Migrationshintergrund trotz deutlich sichtbarer Ressourcen bis in die Mittelstufe hinein nie mit Begabtenförderung in Berührung kommen, weil ihre Stärken in Domä…

- Kein Ersatz-Match ueber Threshold gefunden.

### A:169 (parencite)
[`mpv_abgabedokument.tex:169`](mpv_abgabedokument.tex#L169)

> r zugewanderten Familien sind in anspruchsvolleren Bildungswegen und Förderangeboten häufig untervertreten; ihre Potenziale bleiben nicht selten verdeckt, insbesondere dann, wenn sprachliche Unsicherheiten, belastende Lebensumstände oder auffälliges Verhalten die Wahrnehmung domi…

- Kein Ersatz-Match ueber Threshold gefunden.

---

## `lemas2023begriffsklaerung` – Leistung macht Schule (2023)

Titel: Begriffsklärung von Begabungs-, Begabten-, Potenzial- und Talentförderung
**5 Cite-Stellen**

### L:531 (parencite)
[`mpv.tex:531`](mpv.tex#L531)

>  dieser Grundlage eine prozessbezogene Begriffsklärung, die für die vorliegende Fragestellung zentral ist: Begabung wird als entwicklungsfähiges Potenzial verstanden, das einer prozessorientierten Diagnostik bedarf. Eine einmalige Statusdiagnostik per Intelligenztest genügt diese…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:766 (parencite)
[`mpv.tex:766`](mpv.tex#L766)

> Diagnostik bedarf und eine einmalige Statusdiagnostik nicht genügt \parencite{lemas2023begriffsklaerung}. In der konkreten Situation von S. würde dies bedeuten, den Testbefund als einen Mosaikstein zu behandeln und ihn mit den Beobachtungsdaten aus anderen Kontexten zu konfrontie…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:2747 (parencite)
[`mpv.tex:2747`](mpv.tex#L2747)

>  die Forderung nach prozessorientierter, dynamischer Diagnostik \parencite{preckel2013hochbegabung,lemas2023begriffsklaerung}. Die DISCOVER-Studie und die dynamische NNAT-Modifikation liefern empirische Evidenz für genau jene multiperspektivischen Verfahren, die im Lernskript gef…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:2924 (parencite)
[`mpv.tex:2924`](mpv.tex#L2924)

> Es bestätigt empirisch, dass einmalige Statusdiagnostik nicht genügt \parencite{lemas2023begriffsklaerung} und dass wiederholte Erhebungen bei Kindern im Zweitspracherwerb nötig sind. Im Fall S. ist die schulpsychologische Testung auf Englisch ein solcher erster Screeningschritt,…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:3179 (parencite)
[`mpv.tex:3179`](mpv.tex#L3179)

> stergebnis auf Englisch ist wahrscheinlich eine Unterschätzung. Eine dynamische Diagnostik (z.\,B. mathematische Aufgaben mit gestufter Unterstützung) würde sein Potenzial vermutlich noch deutlicher zeigen. Die Forderung nach prozessorientierter Diagnostik \parencite{lemas2023beg…

- Kein Ersatz-Match ueber Threshold gefunden.

---

## `muelleroppliger2021handbuch` – Müller-Oppliger, Victor and Weigand, Gabriele (2021)

Titel: Handbuch Begabung
**7 Cite-Stellen**

### L:449 (parencite)
[`mpv.tex:449`](mpv.tex#L449)

> erdurchschnittlicher Fähigkeit, Kreativität und Aufgabenverpflichtung; Gardners Theorie der Multiplen Intelligenzen erweitert den Blick auf sprachlich nicht zugängliche Domänen wie die logisch-mathematische, räumliche oder körperlich-kinästhetische Intelligenz \parencite{muellero…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:504 (parencite)
[`mpv.tex:504`](mpv.tex#L504)

> eses Modell ist für die vorliegende Fragestellung bedeutsam, weil es Begabung nicht auf kognitive Leistung reduziert, sondern motivationale und kreative Komponenten einschliesst, die sich gerade in offenen Settings wie SOLUX zeigen können, während sie im leistungsnormierten Regel…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:800 (parencite)
[`mpv.tex:800`](mpv.tex#L800)

>  auffällige Motivation und Fachkompetenz zeigen, erweiterte Fördermöglichkeiten erhalten, unabhängig davon, ob ein formaler Testbefund vorliegt \parencite{muelleroppliger2021handbuch,fischer2020begabungsfoerderung}. S.' Teilnahme an SOLUX und die dort sichtbar gewordenen Stärken …

- Kein Ersatz-Match ueber Threshold gefunden.

### L:874 (parencite)
[`mpv.tex:874`](mpv.tex#L874)

> ognitive Anstrengung und Durchhaltevermögen wirkt. Im Enrichment-Paradigma (Renzulli) wird das individuelle Interessensgebiet zum Ausgangspunkt für Kompetenzentwicklung: S. kann als \enquote{Experte} auftreten, bevor seine schriftsprachlichen Kompetenzen dafür ausreichen würden \…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:1026 (textcite)
[`mpv.tex:1026`](mpv.tex#L1026)

> rientierung (Positionen auf dem Brett erfassen), Regelanwendung (Zugregeln einhalten) und vorausschauende Planung (Konsequenzen antizipieren). \textcite{muelleroppliger2021handbuch} betonen, dass Begabungsförderung dann wirksam ist, wenn sie an den \enquote{Stärken des Denkens} a…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:1689 (parencite)
[`mpv.tex:1689`](mpv.tex#L1689)

> stgesteuerten Lernens) und Typ~III (eigenständige Projekte in einem Interessensgebiet). SOLUX entspricht in wesentlichen Zügen einer Kombination aus Typ~I und Typ~III und verankert die Orientierung an Gardners Multiplen Intelligenzen als Zugangsstruktur \parencite{muelleroppliger…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:1765 (parencite)
[`mpv.tex:1765`](mpv.tex#L1765)

> Typ-III-Enrichment schliesslich ermöglicht eigenständige Projektarbeit in einem individuellen Interessensgebiet, in der Kinder allein oder in kleinen Gruppen als Forschende tätig werden und Expertenwissen aufbauen \parencite{muelleroppliger2021handbuch}.

- [OK] score=0.286: [`008_ii_typische_hochbegabte_kinder_und_jugendliche.pdf`](Literatur/brackmann2013jenseits/excerpts/008_ii_typische_hochbegabte_kinder_und_jugendliche.pdf) S.25-37 – II. Typische hochbegabte Kinder und Jugendliche  _(brackmann2013jenseits)_

---

## `muelleroppliger2021plurale` – Müller-Oppliger, Victor (2021)

Titel: Plurale Gesellschaft, Inklusion und Bildungsgerechtigkeit
**2 Cite-Stellen**

### L:1861 (textcite)
[`mpv.tex:1861`](mpv.tex#L1861)

> \textcite{muelleroppliger2021plurale} rahmt diese Forderung in den Kontext von Inklusion und pluraler Gesellschaft: Wenn Schule den Anspruch erhebt, alle Kinder in ihren Möglichkeiten zu fördern, muss Begabungsförderung als integraler Bestandteil inklusiver Schulentwicklung verst…

- [OK] score=0.286: [`004_einleitung.pdf`](Literatur/preuss2018inklusive/excerpts/004_einleitung.pdf) S.10-15 – Einleitung  _(preuss2018inklusive)_
- [OK] score=0.286: [`076_5_notwendige_veraenderungen_in_einer_schule_mit_be.pdf`](Literatur/reintjes2019begabungsfoerderung/excerpts/076_5_notwendige_veraenderungen_in_einer_schule_mit_be.pdf) S.157-159 – 5 Notwendige Veränderungen in einer Schule mit Begabungsförderung  _(reintjes2019begabungsfoerderung)_

### L:2077 (parencite)
[`mpv.tex:2077`](mpv.tex#L2077)

> he Aufgabe implementiert werden, nicht als Projekt einzelner Fachpersonen \parencite{muelleroppliger2021plurale}. Das Luzerner IBBF-Konzept und das Entwicklungsvorhaben \enquote{Schulen für alle} bieten den institutionellen Rahmen, in dem diese Forderung realisiert werden kann \p…

- [OK] score=0.25: [`006_1_2_inklusive_begabungsfoerderung_als_konzept_eine.pdf`](Literatur/behrensen2016grundwissen/excerpts/006_1_2_inklusive_begabungsfoerderung_als_konzept_eine.pdf) S.18-22 – 1.2 Inklusive Begabungsförderung als Konzept – Eine Gebrauchsanleitung für dieses Buch  _(behrensen2016grundwissen)_
- [OK] score=0.25: [`076_5_notwendige_veraenderungen_in_einer_schule_mit_be.pdf`](Literatur/reintjes2019begabungsfoerderung/excerpts/076_5_notwendige_veraenderungen_in_einer_schule_mit_be.pdf) S.157-159 – 5 Notwendige Veränderungen in einer Schule mit Begabungsförderung  _(reintjes2019begabungsfoerderung)_

---

## `rosebrock2010grundlagen` – Rosebrock, Cornelia and Nix, Daniel (2010)

Titel: Grundlagen der Lesedidaktik und der systematischen schulischen Leseförderung
**6 Cite-Stellen**

### L:855 (parencite)
[`mpv.tex:855`](mpv.tex#L855)

> heiten: inkonsistente Buchstabenformen, erhöhter Stiftdruck, wiederholtes Absetzen. Diese Befunde deuten auf nicht automatisierte sensumotorische Grundlagen hin, die das Schreiben zu einer kognitiv hochbelastenden Tätigkeit machen und damit Ressourcen für inhaltliches Denken bloc…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:860 (parencite)
[`mpv.tex:860`](mpv.tex#L860)

>  Mehrebenenmodell des Lesens, in dem Wort- und Satzidentifikation automatisiert sein müssen, damit Ressourcen für Textverständnis verfügbar werden \parencite{rosebrock2010grundlagen}. \textcite{gold2018lesenkannmanlernen} betont die Bedeutung systematischer Leseförderung, die an …

- Kein Ersatz-Match ueber Threshold gefunden.

### L:892 (parencite)
[`mpv.tex:892`](mpv.tex#L892)

> k2010grundlagen}. \textcite{sturm2016graphomotorik} betont, dass graphomotorische Prozesse beim Schreibenlernen eine eigenständige Entwicklungsaufgabe darstellen: Die Herausbildung stabiler, flüssiger Bewegungsmuster für einzelne Grapheme erfordert intensive Übung und gelingt nur…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:949 (textcite)
[`mpv.tex:949`](mpv.tex#L949)

> ern pro Minute für stilles Lesen. \textcite{rosebrock2010grundlagen} definieren Leseflüssigkeit als die Fähigkeit, Texte mit angemessener Geschwindigkeit, Genauigkeit und Prosodie zu lesen. Sie unterscheiden drei hierarchieniedrige Teilfähigkeiten: Dekodiergenauigkeit, Automatisi…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:1099 (parencite)
[`mpv.tex:1099`](mpv.tex#L1099)

> textit{systematische Leseförderung auf Wortebene}: Parallel zur schreibmotorischen Förderung muss die Leseflüssigkeit aufgebaut werden, beginnend mit Sichtworttraining und Lautleseübungen in kurzen, regelmässigen Einheiten, die schrittweise in den SOLUX-Kontext integriert werden …

- Kein Ersatz-Match ueber Threshold gefunden.

### L:1199 (parencite)
[`mpv.tex:1199`](mpv.tex#L1199)

> rarchieniedrigen Prozesse aufgebaut werden muss \parencite{rosebrock2010grundlagen}. Für S. eignen sich kurze, tägliche Lautleseübungen (5--10 Minuten), die an sein Interessensgebiet angebunden werden: Schachbegriffe auf Deutsch (König, Dame, Turm, Springer, Läufer, Bauer), einfa…

- Kein Ersatz-Match ueber Threshold gefunden.

---

## `sedmak2021bildungsgerechtigkeit` – Sedmak, Clemens and Kapferer, Elisabeth (2021)

Titel: Begabtenförderung und Bildungsgerechtigkeit
**3 Cite-Stellen**

### L:1705 (textcite)
[`mpv.tex:1705`](mpv.tex#L1705)

> \textcite{sedmak2021bildungsgerechtigkeit} rahmen Begabungsförderung als Gerechtigkeitsfrage: Wenn Zugang zu Förderangeboten von sprachlichen und sozioökonomischen Voraussetzungen abhängt, reproduziert Begabtenförderung Ungleichheit statt sie abzubauen.

- [OK] score=0.25: [`112_2_begabungsfoerderung_und_die_frage_nach_bildungsg.pdf`](Literatur/reintjes2019begabungsfoerderung/excerpts/112_2_begabungsfoerderung_und_die_frage_nach_bildungsg.pdf) S.219-220 – 2 Begabungsförderung und die Frage nach Bildungsgerechtigkeit  _(reintjes2019begabungsfoerderung)_

### L:1854 (textcite)
[`mpv.tex:1854`](mpv.tex#L1854)

> tcite{sedmak2021bildungsgerechtigkeit} vertiefen die Gerechtigkeitsperspektive. Sie argumentieren, dass Begabungsförderung, die faktisch nur jenen Kindern zugutekommt, deren Eltern über die kulturellen Codes verfügen, um Förderangebote zu erkennen und einzufordern, keine Begabung…

- [OK] score=0.25: [`109_ingrid_kunze_christian_reintjes_und_ekkehard_ossow.pdf`](Literatur/reintjes2019begabungsfoerderung/excerpts/109_ingrid_kunze_christian_reintjes_und_ekkehard_ossow.pdf) S.219-226 – Ingrid Kunze, Christian Reintjes und Ekkehard Ossowski: Begabungsförderung und Professionalisierung im Spiegel des Diskurses um Bildungsgerechtigkeit  _(reintjes2019begabungsfoerderung)_
- [OK] score=0.25: [`112_2_begabungsfoerderung_und_die_frage_nach_bildungsg.pdf`](Literatur/reintjes2019begabungsfoerderung/excerpts/112_2_begabungsfoerderung_und_die_frage_nach_bildungsg.pdf) S.219-220 – 2 Begabungsförderung und die Frage nach Bildungsgerechtigkeit  _(reintjes2019begabungsfoerderung)_

### L:1991 (parencite)
[`mpv.tex:1991`](mpv.tex#L1991)

> institutionell vorgesehenen Formen manifestieren \parencite{sedmak2021bildungsgerechtigkeit}. Für S. bedeutet dies, dass seine mathematischen Auffälligkeiten und seine strategischen Fähigkeiten als Argumente für einen anspruchsvolleren Schultyp gewichtet werden müssen, auch wenn …

- Kein Ersatz-Match ueber Threshold gefunden.

---

## `stamm2012migranten` – Stamm, Margrit (2012)

Titel: Migranten mit Potenzial: Begabungsreserven in der Berufsbildung ausschöpfen
**3 Cite-Stellen**

### L:370 (parencite)
[`mpv.tex:370`](mpv.tex#L370)

> l, das durch den am Anfang stehenden Zweitspracherwerb, schriftsprachliche Schwierigkeiten, graphomotorische Hürden und mögliche belastende Vorerfahrungen teilweise verdeckt bleibt. Damit besteht die Gefahr einer Under-Identifikation, defizitärer Zuschreibungen und institutionell…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:1281 (parencite)
[`mpv.tex:1281`](mpv.tex#L1281)

> Die Migrationserfahrung selbst ist ein Belastungsfaktor: der Verlust sozialer Netzwerke, mögliche traumatisierende Erfahrungen im Herkunftsland, die sprachliche Isolation in der neuen Umgebung und die fehlende schulische Anschlussfähigkeit wirken kumulativ auf die Begabungsentwic…

- Kein Ersatz-Match ueber Threshold gefunden.

### A:204 (parencite)
[`mpv_abgabedokument.tex:204`](mpv_abgabedokument.tex#L204)

> l, das durch den am Anfang stehenden Zweitspracherwerb, schriftsprachliche Schwierigkeiten, graphomotorische Hürden und mögliche belastende Vorerfahrungen teilweise verdeckt bleibt. Damit besteht die Gefahr einer Under-Identifikation, defizitärer Zuschreibungen und institutionell…

- Kein Ersatz-Match ueber Threshold gefunden.

---

## `stamm2014handbuch` – Stamm, Margrit (2014)

Titel: Handbuch Talententwicklung: Theorien, Methoden und Praxis in Psychologie und Pädagogik
**2 Cite-Stellen**

### L:462 (parencite)
[`mpv.tex:462`](mpv.tex#L462)

> te{maehler2018diagnostik}. Stamm verweist auf \enquote{begabte Minoritäten} als blinden Fleck der Begabtenförderung: Kinder aus Migrationskontexten werden aufgrund sprachlicher Hürden, sozioökonomischer Benachteiligung und stereotyper Zuschreibungen signifikant seltener als begab…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:575 (parencite)
[`mpv.tex:575`](mpv.tex#L575)

> gsreserven} gerade dort ungenutzt bleiben, wo soziale Herkunft, Migrationsgeschichte und fehlende familiäre Bildungsressourcen zusammenwirken. Die MIRAGE-Studie belegt, dass erfolgreiche Migrant:innen retrospektiv häufig berichten, ihre Potenziale seien erst spät oder gar nicht s…

- Kein Ersatz-Match ueber Threshold gefunden.

---

## `stamm2021fehlenderblick` – Stamm, Margrit (2021)

Titel: Der fehlende Blick auf begabte Minoritäten: Blinde Flecken der Begabtenförderung
**5 Cite-Stellen**

### L:330 (parencite)
[`mpv.tex:330`](mpv.tex#L330)

> \enquote{Schulen für alle} darauf ab, Teilhabe, Passung und chancengerechtere Bildung zu stärken. Bildungswissenschaftliche Befunde zeigen indessen, dass Bildungschancen in der Schweiz weiterhin stark von sozialer Herkunft, Migrationsgeschichte und familiären Ressourcen abhängen …

- Kein Ersatz-Match ueber Threshold gefunden.

### L:462 (parencite)
[`mpv.tex:462`](mpv.tex#L462)

> te{maehler2018diagnostik}. Stamm verweist auf \enquote{begabte Minoritäten} als blinden Fleck der Begabtenförderung: Kinder aus Migrationskontexten werden aufgrund sprachlicher Hürden, sozioökonomischer Benachteiligung und stereotyper Zuschreibungen signifikant seltener als begab…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:535 (textcite)
[`mpv.tex:535`](mpv.tex#L535)

> k} identifiziert \enquote{begabte Minoritäten} als systematischen blinden Fleck der Begabtenförderung. Kinder aus Migrationskontexten, aus sozioökonomisch benachteiligten Familien und aus bildungsfernen Milieus sind in Förderprogrammen für Begabte signifikant unterrepräsentiert. …

- Kein Ersatz-Match ueber Threshold gefunden.

### L:811 (parencite)
[`mpv.tex:811`](mpv.tex#L811)

>  kognitive Kapazität als über die Grenzen des Verfahrens \parencite{stamm2021fehlenderblick}. Das zweite Argument ist pädagogisch: Lehwald zeigt, dass Motivation bei begabten Kindern einbricht, wenn die Lernumgebung keine Passung bietet. Auf einen durchschnittlichen Testwert hin …

- Kein Ersatz-Match ueber Threshold gefunden.

### A:164 (parencite)
[`mpv_abgabedokument.tex:164`](mpv_abgabedokument.tex#L164)

> \enquote{Schulen für alle} darauf ab, Teilhabe, Passung und chancengerechtere Bildung zu stärken. Bildungswissenschaftliche Befunde zeigen indessen, dass Bildungschancen in der Schweiz weiterhin stark von sozialer Herkunft, Migrationsgeschichte und familiären Ressourcen abhängen …

- Kein Ersatz-Match ueber Threshold gefunden.

---

## `stern2025intelligenz` – Stern, Elsbeth (2025)

Titel: Die Intelligenz kann sich im Schulalter noch verändern
**1 Cite-Stellen**

### L:493 (textcite)
[`mpv.tex:493`](mpv.tex#L493)

> E.~\textcite{stern2025intelligenz} bestätigt diese Perspektive aus aktueller kognitionspsychologischer Forschung: Intelligenz kann sich im Schulalter noch substanziell verändern, was die Fixierung auf einen einmalig erhobenen IQ-Wert als diagnostische Grundlage zusätzlich in Frag…

- Kein Ersatz-Match ueber Threshold gefunden.

---

## `trautmann2016einfuehrung` – Trautmann, Thomas (2016)

Titel: Einführung in die Hochbegabtenpädagogik
**7 Cite-Stellen**

### L:449 (parencite)
[`mpv.tex:449`](mpv.tex#L449)

> erdurchschnittlicher Fähigkeit, Kreativität und Aufgabenverpflichtung; Gardners Theorie der Multiplen Intelligenzen erweitert den Blick auf sprachlich nicht zugängliche Domänen wie die logisch-mathematische, räumliche oder körperlich-kinästhetische Intelligenz \parencite{muellero…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:492 (textcite)
[`mpv.tex:492`](mpv.tex#L492)

> Diese Unterscheidung von Potenzial und Performanz durchzieht die gesamte aktuelle Diskussion (vgl. \textcite{preckel2013hochbegabung}; \textcite{trautmann2016einfuehrung}).

- **[STRONG]** score=0.571: [`039_4_begabung_als_potenzial_und_performanz.pdf`](Literatur/reintjes2019begabungsfoerderung/excerpts/039_4_begabung_als_potenzial_und_performanz.pdf) S.79-80 – 4 Begabung als Potenzial und Performanz  _(reintjes2019begabungsfoerderung)_
- [OK] score=0.286: [`007_2_hochbegabung_und_begabung_eine_spurensuche_zur_b.pdf`](Literatur/behrensen2016grundwissen/excerpts/007_2_hochbegabung_und_begabung_eine_spurensuche_zur_b.pdf) S.23-37 – 2 Hochbegabung und Begabung: Eine Spurensuche zur Bedeutung zentraler Begriffe  _(behrensen2016grundwissen)_

### L:513 (parencite)
[`mpv.tex:513`](mpv.tex#L513)

> rache noch am Anfang stehen, eröffnet dieser breite Begabungsbegriff die Möglichkeit, Potenziale jenseits sprachlicher Performanz wahrzunehmen. S.' auffällige Leistungen im Schach verweisen auf ausgeprägte logisch-mathematische und räumliche Fähigkeiten, die im sprachlastigen Unt…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:624 (textcite)
[`mpv.tex:624`](mpv.tex#L624)

> \textcite{trautmann2016einfuehrung} betont, dass Beobachtung als diagnostisches Instrument nur dann valide ist, wenn sie kriteriengestützt erfolgt und verschiedene Kontexte systematisch berücksichtigt.

- Kein Ersatz-Match ueber Threshold gefunden.

### L:783 (parencite)
[`mpv.tex:783`](mpv.tex#L783)

> rfassen komplexer Muster, Fähigkeit zur Strategieentwicklung und zur Erklärung eigener Denkwege, intrinsische Motivation und Durchhaltevermögen. Diese Beobachtungen sind diagnostisch mindestens so aussagekräftig wie ein Testwert, wenn sie systematisch und kriteriengestützt erhobe…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:1689 (parencite)
[`mpv.tex:1689`](mpv.tex#L1689)

> stgesteuerten Lernens) und Typ~III (eigenständige Projekte in einem Interessensgebiet). SOLUX entspricht in wesentlichen Zügen einer Kombination aus Typ~I und Typ~III und verankert die Orientierung an Gardners Multiplen Intelligenzen als Zugangsstruktur \parencite{muelleroppliger…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:2250 (parencite)
[`mpv.tex:2250`](mpv.tex#L2250)

> kumentation, die an etablierten Indikatoren der Begabungserkennung orientiert ist \parencite{trautmann2016einfuehrung,ipege2009professionelle}. Zweitens schaffe ich durch Hospitationseinladungen Gelegenheiten für Fremdbeobachtung: Die Klassenlehrperson und weitere Fachpersonen er…

- Kein Ersatz-Match ueber Threshold gefunden.

---

## `unger2010begabungsfoerderung` – Unger, Evelyn (2010)

Titel: Begabungs- und Begabtenförderung unter den Bedingungen der \guillemotleftNeuen Mittelschule\guillemotright
**2 Cite-Stellen**

### L:1869 (textcite)
[`mpv.tex:1869`](mpv.tex#L1869)

> \textcite{unger2010begabungsfoerderung} untersucht, unter welchen Bedingungen Begabungsförderung an Regelschulen gelingt, und identifiziert strukturelle Gelingensbedingungen: Unterstützung durch die Schulleitung, Verankerung im Schulprogramm, Kooperation im Kollegium und eine Kul…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:2058 (parencite)
[`mpv.tex:2058`](mpv.tex#L2058)

> Schulleitung, die Verankerung im Schulprogramm und eine Kultur der Ressourcenorientierung \parencite{unger2010begabungsfoerderung}. SOLUX wird derzeit an sieben Klassen durchgeführt; die systematische Auswertung der Erfahrungen könnte in ein schulinternes Konzept für inklusive Be…

- [OK] score=0.258: [`048_4_inklusive_begabungsfoerderung_als_gebot_der_stun.pdf`](Literatur/reintjes2019begabungsfoerderung/excerpts/048_4_inklusive_begabungsfoerderung_als_gebot_der_stun.pdf) S.97-98 – 4 Inklusive Begabungsförderung als Gebot der Stunde: Einige abschließende Überlegungen  _(reintjes2019begabungsfoerderung)_

---

## `webb2020doppeldiagnosen` – Webb, James T. and Amend, Edward R. and Beljan, Paul
               and Webb, Nadia E. and Kuzujanakis, Marianne
               and Olenchak, F. Richard and Goerss, Jean (2020)

Titel: Doppeldiagnosen und Fehldiagnosen bei Hochbegabung:
               Ein Ratgeber für Fachpersonen und Betroffene
**3 Cite-Stellen**

### L:665 (textcite)
[`mpv.tex:665`](mpv.tex#L665)

> \textcite{webb2020doppeldiagnosen} systematisieren dieses Phänomen und dokumentieren, dass hochbegabte Kinder häufig Fehldiagnosen erhalten: Verhaltensweisen, die aus der Diskrepanz zwischen Potenzial und inadäquater Lernumgebung resultieren, werden als ADHS, Oppositionelles Verh…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:1462 (textcite)
[`mpv.tex:1462`](mpv.tex#L1462)

> \textcite{webb2020doppeldiagnosen} bezeichnen diese Konstellation als diagnostische Falle: Wird das Verhalten eines Kindes ausschliesslich durch die sichtbaren Schwierigkeiten erklärt, entsteht ein defizitdominiertes Bild, das die verdeckte Begabung systematisch ausblendet.

- Kein Ersatz-Match ueber Threshold gefunden.

### L:3279 (parencite)
[`mpv.tex:3279`](mpv.tex#L3279)

> inem nicht-westlichen Kontext}, dass die Koexistenz von Hochbegabung und Lernbehinderung zu gegenseitiger Maskierung führt. Das stützt das 2E-Konzept, das im Lernskript als Deutungsrahmen für S. dient (vgl. Abschnitt~\ref{subsec:2e}), und zwar nicht nur als theoretische Heuristik…

- Kein Ersatz-Match ueber Threshold gefunden.

---

## `weigand2021separativ` – Weigand, Gabriele and Kaiser, Michaela (2021)

Titel: Separativ oder integrativ? Inklusive Begabungs- und Begabtenförderung
**3 Cite-Stellen**

### L:1702 (textcite)
[`mpv.tex:1702`](mpv.tex#L1702)

> SOLUX setzt dem ein Gegenmodell entgegen: notenfrei, interessenorientiert, sprachentlastet und mit nonverbalen Zugängen. \textcite{weigand2021separativ} beschreiben inklusive Begabungsförderung als Ansatz, der nicht nur eine ausgewählte Gruppe Hochbegabter adressiert, sondern all…

- Kein Ersatz-Match ueber Threshold gefunden.

### L:1838 (textcite)
[`mpv.tex:1838`](mpv.tex#L1838)

> {weigand2021separativ} ordnen die Debatte um Begabungsförderung in eine bildungspolitische Grundfrage ein: Soll Begabtenförderung separativ (in Sonderklassen, Pull-out-Programmen, Spezialschulen) oder integrativ (im Regelunterricht, für alle zugänglich) organisiert werden? Sie ar…

- [OK] score=0.263: [`038_3_die_person_als_grundlage_einer_paedagogischen_th.pdf`](Literatur/reintjes2019begabungsfoerderung/excerpts/038_3_die_person_als_grundlage_einer_paedagogischen_th.pdf) S.78-78 – 3 Die ‚Person‘ als Grundlage einer pädagogischen Theorie und Praxis der Begabungs- und Begabtenförderung  _(reintjes2019begabungsfoerderung)_

### L:2066 (parencite)
[`mpv.tex:2066`](mpv.tex#L2066)

>  integraler Bestandteil der Schulentwicklung verstanden werden muss \parencite{weigand2021separativ}. Für die Schule von S. bedeutet dies, dass die Frage, wie Potenziale bei Kindern mit Migrationserfahrung erkannt werden, nicht dem Zufall oder dem Engagement einzelner Lehrpersone…

- [OK] score=0.31: [`076_5_notwendige_veraenderungen_in_einer_schule_mit_be.pdf`](Literatur/reintjes2019begabungsfoerderung/excerpts/076_5_notwendige_veraenderungen_in_einer_schule_mit_be.pdf) S.157-159 – 5 Notwendige Veränderungen in einer Schule mit Begabungsförderung  _(reintjes2019begabungsfoerderung)_

---
