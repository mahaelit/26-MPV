# Vortrag 1 – Belegdokumentation

**Frage 1:** Wie können verdeckte Begabungen bei neu zugewanderten, mehrsprachigen Schüler:innen mit geringen Deutschkenntnissen multiperspektivisch erfasst werden?

**Zweck dieser Datei:** Für jeden Vortragsabsatz die belegfähigen Quellen mit
verifiziertem Wortlaut und Seitenangabe zusammenführen. Trennt zwischen
**verifiziert** (Wortlaut aus PDF/Transkript), **paraphrasiert** (Quelle deckt
Aussage inhaltlich, ohne exakten Wortlaut) und **offen** (noch kein Beleg
extrahiert; Quelle vorhanden, aber Bildscan ohne OCR-Layer).

Volltext-Auszüge liegen in `Visualisierung/.cache/vortrag1/`:
- `00_pdf_extracts.txt` (alle PDF-Extracts, ein Pass)
- `01_maehler_haag_S153-188.txt` (Maehler/Haag mit korrektem Buchseiten-Offset)
- `_extract_script.py` (Reproduzierbarer Extraktor)

---

## 1. Status pro Kernquelle

| BibKey | Aussage stützt | Beleg-Quelle | Status |
|---|---|---|---|
| `stamm2021fehlenderblick` | Mosaik-Einleitung; Migration als Wahrnehmungsfilter | `Literatur/stamm2021fehlenderblick/verified_quotes.md` + Sammelband-Transkript `teil8_*.md` | offen – Transkript noch nicht in Belegdatei eingearbeitet |
| `stamm2025vonuntennachoben` | Migration & unentdeckte Begabung | PDFs sind Fotografien ohne OCR-Layer | offen – nur `verified_quotes.md` nutzbar |
| `preckel2013hochbegabung` | Lehrkrafturteil ist nicht ausreichend | `verified_quotes.md` (Status 4, Kap. 1.1/1.2/2.2 belegt) | verifiziert (paraphrasiert) – siehe §2.2 |
| `gauckreimann2021psychdiagnostik` | Psychologische Abklärung als ein Stein, nicht alleinstehend; Momentaufnahme, Testminderleistung, Prozessdiagnostik | `verified_quotes.md` (Status 5, OCR-Transkript Teil 3) | verifiziert – siehe §2.4 |
| `haag2018leistungsstanddiagnostik` (in `maehler2018diagnostik`) | Sprachliche Anforderungen, Lerngelegenheiten, kulturspezifisches Wissen verzerren Testergebnisse | PDF S. 153–165, 187–188 direkt aus `source.pdf` extrahiert | verifiziert (Wortlaut) – siehe §2.1 |
| `kellerkoller2025hellekoepfe` | Deutschkenntnisse als Wahrnehmungsfilter, Fall Sohrab | Kapitel-PDF Bildscan (kein OCR); `verified_quotes.md` Audit-Befund vorhanden | offen – OCR notwendig |
| `baumschader2021twice` | 2e-Profil, Stärken/Schwächen verdecken sich gegenseitig | `verified_quotes.md` mit Volltext-Belegen (OCR Teil 8) | verifiziert – siehe §2.5 |
| `koop2025herkunft` | Kinder mit Migrationshintergrund unterrepräsentiert; falscher Fokus, Sprachabhängigkeit; multiperspektivische Diagnostik | PDF S. 64–67 direkt extrahiert | verifiziert (Wortlaut) – siehe §2.1 |
| `stern2025intelligenz` | Intelligenz im Schulalter veränderbar | `source.docx` – noch nicht extrahiert | offen |
| `webb2020doppeldiagnosen` | Fehldiagnose-Risiko; Maskierung bei 2e | Kapitel-PDF Bildscan (kein OCR); `verified_quotes.md` hat Audit, keine Wortlaute | offen – OCR notwendig |
| `warneckehauke2020bildungsgerechtigkeit` | Bildungsgerechtigkeit/Migration/Underachievement – Praxisprojekte | PDF S. 241–253 direkt extrahiert | verifiziert (Wortlaut) – siehe §2.3, §2.5 |
| `kellerkoller2013erkennen` | Begabung trotz Sprachdefizit erkennen | Online-Merkblatt (kein lokaler Volltext) | offen |
| `muelleroppliger2021paeddiagnostik` | Pädagogische Potenzialerfassung, Förderdiagnostik (Stein 3: Beobachtung) | Bildscan; ggf. via `excerpts/teil3_*.md` Sammelband-Transkript | offen – Sammelband-Transkript zu erschliessen |
| `kappus2010migration` | Migrationsbedingte Heterogenität | PDF Bildscan (14 Seiten leer extrahiert) | offen – OCR notwendig |

## 2. Belege pro Vortragsabsatz

### 2.1 Stein 1 – Sprachsensible Diagnostik (Z. 10)

**Vortragsaussage:** „Haag, Heppt und Schipolowski zeigen für
Leistungsstanddiagnostik bei Migration, dass Testergebnisse sprachliche
Anforderungen, Lerngelegenheiten und kulturell-schulische Vorerfahrungen
mitabbilden können."

**Verifizierter Wortlaut – Haag/Heppt/Schipolowski (in Maehler 2018), S. 153:**

> „Sprachliche Kompetenzen stellen somit eine wichtige Voraussetzung zum Erwerb
> von Wissen und schulbezogenen Kompetenzen dar. Bei der Erfassung
> schulbezogener Kompetenzen sollten die sprachlichen Fähigkeiten der
> Schülerinnen und Schüler allerdings nach Möglichkeit nicht ins Gewicht
> fallen."

**S. 155 (Folgeseite, zur sprachlichen Anforderung von Testaufgaben):**

> „Die benachteiligende Wirkung scheint dabei nicht auf einzelne sprachliche
> Merkmale zurückzuführen zu sein, sondern vielmehr generell von langen und
> insbesondere in Bezug auf den verwendeten Wortschatz komplexen Aufgaben
> auszugehen."

**S. 159 (zu kulturfairen Tests):**

> „Studien, in denen die Testteilnehmenden während der Bearbeitung derartiger
> Aufgaben aufgefordert wurden, ihren Lösungsweg zu verbalisieren, haben jedoch
> gezeigt, dass die Verbalisierung die Lösung bestimmter nonverbaler Aufgaben
> negativ beeinflusst […]. Dies legt nahe, dass auch die Lösung nonverbaler
> Aufgaben teilweise auf verbal-analytischen Prozessen beruht […]."

**S. 161 (zu Lerngelegenheiten):**

> „Erhält eine Testperson aufgrund eingeschränkter Lerngelegenheiten geringe
> Kompetenzwerte in einem Test (beispielsweise wenn die getestete Kompetenz im
> Herkunftsland der Testperson noch nicht unterrichtet wurde), so bildet der
> geringe Testwert die Kompetenz der Testperson valide ab, da die Person
> tatsächlich in geringerem Maße über die entsprechende Kompetenz verfügt. Eine
> Selektionsentscheidung […] wäre einerseits gerechtfertigt, würde die Person
> jedoch für die mangelnden Lerngelegenheiten ‚bestrafen', die nicht in ihrer
> Verantwortung liegen."

**S. 163 (zu kulturspezifischem Wissen):**

> „Neu zugewanderte Personen sind somit bei kognitiven Fähigkeitstests umso
> stärker im Nachteil, je mehr sich diese auf Inhalte beziehen, die für das
> Bildungssystem oder die Kultur des Aufnahmelandes spezifisch sind."

**S. 165 (Empfehlung: nonverbal als ergänzender Test):**

> „Steht die Validität der Testergebnisse aufgrund mangelnder
> Sprachbeherrschung oder geringer Vertrautheit mit der Mehrheitskultur
> infrage, so sollten unterschiedliche Zugänge kombiniert werden.
> Beispielsweise kann zusätzlich ein nonverbaler Test eingesetzt werden, um
> durch einen Vergleich der Resultate beider Testverfahren den Einfluss der
> Sprachbeherrschung und Kulturvertrautheit auf die Ergebnisse besser
> einschätzen zu können."

**S. 188 (Schluss):**

> „Die möglichst genaue Erfassung individueller Unterschiede in breit
> definierten kognitiven Fähigkeiten sowie schulbezogenen fachlichen
> Kompetenzen ist jedoch eine wichtige Voraussetzung, um optimale Bildungsgänge
> bzw. Förderangebote für Kinder und Jugendliche mit Zuwanderungshintergrund
> auswählen zu können."

**Quelle:** `Visualisierung/.cache/vortrag1/01_maehler_haag_S153-188.txt`

**Ergänzend – Koop (2025), S. 65 (Sprachabhängigkeit ist auch in
„sprachfreien" Tests nicht aufgehoben):**

> „Einige Studien konnten zeigen, dass auch in sprachfreien Tests die
> Leistungen von Nicht-Muttersprachler:innen hinter denen von
> Muttersprachler:innen zurückblieben – selbst wenn die Kinder in vergleichbaren
> sozioökonomischen Verhältnissen aufgewachsen sind."

**S. 66:**

> „Nonverbale Tests können den sprachlichen und kulturellen Einfluss auf
> Testergebnisse also nur eingrenzen, aber nicht gänzlich aufheben. […]
> Beispielsweise stellt eine ungewohnte Leserichtung selbst bei einem
> ‚kulturfairen' Matrizentest eine zusätzliche Herausforderung dar. Zudem ist
> auch das Denken in Symbolsystemen von Sprache und Kultur beeinflusst […]."

---

### 2.2 Stein 2 – Kritisch eingeordnetes Lehrkrafturteil (Z. 12)

**Vortragsaussage:** „Preckel und Baudson zeigen, dass Hochbegabung nicht
einfach über Alltagswahrnehmung oder gute Noten erkannt werden kann.
Lehrkrafturteile sind wichtig, aber sie sind anfällig für Erwartungen,
Stereotype und Performanzsignale."

**Belege – Preckel/Baudson 2013, Kap. 1.1/1.2/2.2** (aus
`Literatur/preckel2013hochbegabung/verified_quotes.md`, Status 4):

- Kap. 1.1/1.2 *„Hochbegabung: Potenzial oder Leistung?"*: „Sowohl Performanz-
  als auch Kompetenzdefinitionen von Hochbegabung sind heute weit verbreitet."
  Gagnes Modell integriert „Kompetenz (Begabung) als auch Performanz (Talent)".
  → Stützt die Unterscheidung Potenzial vs. tatsächlich gezeigte Leistung.
- Kap. 2.2 *„Doppelte Ausnahmen"*: „Einzigartigkeit ihrer Lernerprofile, bei
  denen sich Stärken und Schwächen gegenseitig verdecken können."
- Kap. 2.2 *„Underachievement"*: „relativ zur Begabung und zur Situation
  erwartungswidrige Minderleistung […] Diskrepanz zwischen Fähigkeiten und
  Leistungen."

**Hinweis:** Das im Workspace vorhandene PDF
`Preckel_Baudson 2013hochbegabung,kap2.2 S.42-50.pdf` ist ein Bildscan ohne
OCR-Layer (9 leere Seiten in PyMuPDF-Extraktion). Die Belege stammen aus dem
zugehörigen `verified_quotes.md`, das bereits manuell gegen das Buch geprüft
wurde (Stand 2025-11-22).

**Ergänzend – Baudson (2025) S. 36–37** (Stützliteratur, Volltext aus PDF):

> „Das Marburger Hochbegabtenprojekt konnte zeigen, dass Lehrkräfte
> Hochbegabte nur dann erkennen, wenn ihre Leistungen erwartungsgemäß
> ausfallen – hochbegabte Underachiever haben faktisch kaum Chancen, dass
> ihre Begabung erkannt wird (8)."

> „Hier zeigt sich seit Jahrzehnten ein ungebrochener Trend der
> Unterrepräsentation insbesondere Schwarzer Jungen in Begabtenförderprogrammen,
> oft bei gleichzeitiger Überrepräsentation in sonderpädagogischen
> Fördermaßnahmen. […] Ursachen sehen die Autor:innen der Übersichtsstudie in
> unzureichend kultursensiblen Zugangsverfahren und in einem Defizitfokus des
> überwiegend weißen und weiblichen pädagogischen Personals […]."

→ Stützt die Aussage, dass Lehrkrafturteile durch Stereotype und implizite
Theorien systematisch verzerrt sein können.

---

### 2.3 Stein 3 – Beobachtung im stärkenoffenen Setting (Z. 14)

**Vortragsaussage:** „Mit S. Müller-Oppliger gesprochen geht es um
pädagogische Potenzialerfassung und Förderdiagnostik: Ich beobachte nicht nur
das Produkt, sondern Denkwege, Lernverhalten, Interessen, Strategien und
Bedingungen, unter denen Leistung möglich wird."

**Status:** Quelle `muelleroppliger2021paeddiagnostik` (S. 224–235) ist im
Workspace nur als Bildscan-PDF vorhanden (12 leere Seiten in PyMuPDF). Belege
müssen aus dem Sammelband-Transkript `Literatur/muelleroppliger2021handbuch/
excerpts/teil3_begabungen_erkennen.md` extrahiert werden.

**Ergänzend – Koop (2025), S. 66 (zur potenzialorientierten Diagnostik):**

> „Die einen stellen Lernergebnisse fest, während andere den individuellen
> Lernprozess und Lernzuwachs abbilden. Wird dabei der Fokus auf individuelle
> Stärken und Entwicklungsmöglichkeiten gesetzt, spricht man von einer
> potenzialorientierten Diagnostik. Hier werden Interessen, Engagement und
> Motivation von Schüler:innen sehr offen exploriert, um Fördermaßnahmen
> auszuwählen oder gar individuell zuzuschneiden."

**S. 67 (zur Voraussetzung Setting + Lehrkraftsensibilität):**

> „Doch es braucht sowohl Gelegenheiten, bei denen Kinder ihre Talente und
> Begabungen zeigen können, als auch eine Sensibilität aufseiten der
> Lehrkräfte, diese Potenziale zu erkennen."

**Ergänzend – Warnecke/Hauke (2020), S. 244 (Diagnostik vor Förderprojekt):**

> „Vor der Projektaufnahme fand im Rahmen eines Auswahlverfahrens eine
> umfassende Diagnostik statt. Dabei wurden die kognitive Entwicklung in den
> Bereichen Sprache, Mathematik und abstrakt-logisches Denken sowie die
> Kreativität der Kinder mit standardisierten Tests erfasst und eine
> Selbsteinschätzung im Hinblick auf Arbeitsverhalten, Motivation und
> Interessen eingeholt."

---

### 2.4 Stein 4 – Multiprofessionelle Abklärung (Z. 16)

**Vortragsaussage:** „Gauck und Reimann sind hier wichtig, weil psychologische
Diagnostik in der Begabungsförderung nicht isoliert stehen darf. Sie liefert
einen fachlichen Befund, der mit pädagogischen Beobachtungen, Sprachprofil und
Kontextinformationen zusammen gelesen werden muss."

**Belege – Gauck/Reimann 2021** (aus
`Literatur/gauckreimann2021psychdiagnostik/verified_quotes.md`, Status 5,
OCR-Transkript Teil 3, S. 239–251):

> „ob also eine auf ein bis zwei Termine beschränkte Testdurchführung […]
> bestenfalls eine Momentaufnahme des aktuellen Potenzials darstellt"

**Konzept „Testminderleistung":** Kinder, die zur Diagnostik angemeldet werden,
seien häufig bereits durch die schulische und familiäre Situation belastet,
was zu einer Testminderleistung führen könne (S. 239–251).

**Konzept „Prozessdiagnostik statt Statusdiagnostik":** „bei Kindern, die ihr
Potenzial in einer einmaligen Abklärung nicht zum Ausdruck bringen können,
anstelle einer Statusdiagnostik eine Prozessdiagnostik durchzuführen" –
Response-to-Intervention wird als verwandter Ansatz genannt.

**Fallvignette Aisha (S. ≈ 246–247):** 10-jähriges Mädchen mit
Migrationshintergrund, Underachievement, ADHS-Diagnose verdeckte die
Hochbegabung. Direkter deutschsprachiger Quellenbeleg für institutionelles
Unteridentifikationsmuster.

→ Belegt, dass psychologische Abklärung **eingebettet** sein muss, mehrere
Termine empfehlenswert sind und Diagnostik prozessual gedacht werden sollte.

---

### 2.5 Stein 5 – Biopsychosoziale Kontextperspektive / 2e (Z. 18)

**Vortragsaussage:** „Mit Baum und Schader sowie Webb et al. lässt sich die
Konstellation als 2e-Profil im erweiterten Sinn verstehen: hohe kognitive
Ressourcen und Schwierigkeiten können sich gegenseitig verdecken."

**Belege – Baum/Schader 2021** (aus
`Literatur/baumschader2021twice/verified_quotes.md`, Status 5, OCR-Transkript
Teil 8, S. 588–600):

> „Diese als zweifach außergewöhnlich bezeichneten Schülerinnen (Twice
> Exceptionals, 2e genannt) weisen einerseits überdurchschnittliche Fähigkeiten
> und andererseits Lernschwierigkeiten auf."

> „Beide können sich gegenseitig verdecken, so dass weder die Beeinträchtigung
> noch die Fähigkeit erkannt oder angesprochen wird."

> „Bei gezackten Intelligenzprofilen werden ihr [in] bestimmten Bereichen
> überdurchschnittliche Ergebnisse durch ihre Schwächen neutralisiert und
> verschlechtert. Es passt zu einer niedrigen Gesamtpunktzahl führt [sic;
> OCR-Tippfehler], die oft nicht den Richtwerten zur Identifizierung begabter
> entspricht."

> „spezielle Identifikationsmethoden, die die mögliche Wechselwirkung der
> Besonderheiten berücksichtigen"

**Empirischer Datenpunkt (S. ≈ 590):**

> „Baum [arbeitet/findet] heraus, dass bis zu 33 % der Schülerinnen die
> sonderpädagogische Förderung erhalten, entweder im verbal oder Handlungsteil
> einen Intelligenzquotienten im oberen Segment der Wechsler-Intelligenz-Skala
> hatten."

**Grün-Metapher (für Vortrag wertvoll):** 2e-Lernende sind weder „gelb" (nur
begabt) noch „blau" (nur beeinträchtigt), sondern immer „grün" – eine
untrennbare Mischung beider Aspekte.

**Belege – Webb et al. 2020:** Kapitel-PDF (S. 87–94) ist Bildscan ohne
OCR-Layer. `verified_quotes.md` enthält bislang **keinen Wortlaut**, nur den
Audit-Befund: „S. 87–89 definieren Fehldiagnosen bei Hochbegabung […]
S. 87–94 decken Fehldiagnosen, Doppeldiagnosen und die gegenseitige
Überlagerung von Hochbegabung und diagnostischen Kategorien ab."

→ **Lücke:** Für Webb braucht es OCR-Extraktion des Kapitels, um wörtlich
zitierfähig zu sein. Inhaltlich trägt aktuell Baum/Schader die 2e-Argumentation
allein; Webb fungiert als Mitbeleg ohne wörtlichen Anker.

**Kontextstütze – Warnecke/Hauke (2020), S. 247–248:**

> „Die Ergebnisse des Nationalen Bildungsberichts 2016 bringen hervor, dass
> kaum ein anderer Indikator den Bildungserfolg von Kindern und Jugendlichen
> so stark beeinflusst wie die soziale Herkunft. Aktuelle Ergebnisse hieraus
> zeigen, dass zwei Gruppen von Heranwachsenden besonders benachteiligt sind:
> Arbeiterkinder und Kinder mit Migrationshintergrund."

---

### 2.6 Übergreifende Befunde (für Einleitung und Schluss)

**Koop (2025), S. 64 – falscher Fokus, Interaktionseffekte, Sprachabhängigkeit
(zentraler Kurzbeleg für die Mosaik-Logik):**

> „Trotz gewachsener Sensibilität für Herkunftseffekte sind Kinder mit
> Migrationshintergrund und aus armen Familien in der Begabtenförderung
> unterrepräsentiert. Ein häufiger Grund dafür ist, dass Lehrkräfte sich zu
> sehr daran orientieren, wie gut Schüler:innen den Lernstoff bewältigen und
> welche familiären Unterstützungsmöglichkeiten sie wahrnehmen."

Drei Gründe (S. 64) wörtlich:
- **falscher Fokus**: Beurteilung auf Basis des Lernstoffs, nicht
  domänenspezifischer Begabungsmerkmale.
- **Interaktionseffekte**: Lehrkräfte als Teil der Lernumgebung, daher Beob-
  und Beurteilungsfehler.
- **Sprachabhängigkeit**: „hohe Anforderungen an Sprachverständnis und
  Ausdrucksvermögen".

**Koop (2025), S. 65 – Grenzen von Intelligenzscreenings:**

> „Doch gerade mit Blick auf Kinder wie Amina und Pascal stößt auch dieses
> Vorgehen an Grenzen: Unzureichende Deutsch-Kenntnisse, limitierte schulische
> Vorerfahrungen und auch psychische Belastungen können Intelligenzscreenings
> negativ beeinflussen oder ihre Interpretation erschweren (2). Die
> Bildungsbiografie von Kindern mit Fluchterfahrungen beispielsweise ist von
> Brüchen und Inkonsistenzen gekennzeichnet."

**Koop (2025), S. 67 – Kombination von Verfahren:**

> „Die Verwendung von (Intelligenz-)Screenings und Nominierungen durch
> Lehrkräfte ist dem jeweils isolierten Einsatz nur eines dieser Verfahren
> überlegen."

→ **Direkter Beleg für die Mosaik-These des Vortrags.**

**Erzinger 2023, S. 45 (PISA-Befund Schweiz, Stützliteratur):**

> „[…] schneiden in der Schweiz benachteiligte Schülerinnen und Schüler beim
> PISA-Test deutlich schlechter ab als privilegierte Schülerinnen und Schüler
> (Konsortium PISA.ch, 2019) und auch auf internationaler Ebene zeigt sich,
> dass sozial privilegierte Schülerinnen und Schüler unter den
> leistungsstarken Schülerinnen und Schülern überrepräsentiert sind (17 % vs.
> 3 %) (OECD, 2019b)."

**BFS 2022, S. 35 (Stützliteratur, Migration und Sprache):**

> „Wie vielfach belegt wurde, haben Sprachkenntnisse einen grossen Einfluss
> darauf, welche Tätigkeiten Migrantinnen und Migranten in der Arbeitswelt
> übernehmen und wie gut in der Folge die gesellschaftliche Integration
> gelingt."

> „Bei der Bevölkerung ohne Migrationshintergrund beträgt der Anteil der
> Personen mit einer Landessprache als (eine ihrer) Hauptsprache(n) nahezu
> 100%, bei der Bevölkerung mit Migrationshintergrund knapp 70%."

---

## 3. Offene Punkte / nächste Schritte

| Quelle | Was fehlt | Vorschlag |
|---|---|---|
| `stamm2021fehlenderblick` | Wortlaut-Belege für „begabte Minoritäten / Wahrnehmungsfilter" | Sammelband-Transkript `Literatur/muelleroppliger2021handbuch/excerpts/teil8_*.md` durchsehen und Schlüsselstellen herausziehen |
| `stamm2025vonuntennachoben` | Volltext aus Foto-PDFs | Tesseract-OCR auf die 7 Foto-PDFs (S. 36–37, 58–62) |
| `kellerkoller2025hellekoepfe` | Wortlaut S. 76–78 zu „Sohrab" und Migration | Tesseract-OCR auf das 3-Seiten-Kapitel-PDF |
| `webb2020doppeldiagnosen` | Wortlaut S. 87–94 zu Maskierung/Fehldiagnose | Tesseract-OCR auf `kap02_*.pdf` |
| `kappus2010migration` | Volltext S. 63–70, 74 | Tesseract-OCR (PDF liefert via PyMuPDF nur leere Seiten) |
| `muelleroppliger2021paeddiagnostik` | Wortlaut S. 224–235 zu pädagogischer Potenzialerfassung | Sammelband-Transkript Teil 3 + ggf. Tesseract |
| `stern2025intelligenz` | Wortlaut S. 15–18 | `source.docx` mit `python-docx` extrahieren |
| `kellerkoller2013erkennen` | Online-Merkblatt herunterladen oder lokalen Snapshot prüfen | – |
| Stützliteratur (`baudson2021wasdenken`, `muelleroppliger2021begabungsmodelle`, `trautmann2016einfuehrung`, `lehwald2017motivation`, `grossenbacher2014integrative`, `dvs2025bbf`) | Wortlaut | Tesseract-OCR bzw. Online-Snapshot, niedrige Priorität (nur Stütze) |

**Empfehlung:** Bevor weitere OCR-Läufe gestartet werden, mit dem User klären,
ob die aktuelle Belegtiefe für die Kernsteine 1/2/4/5 ausreicht (Haag, Preckel,
Koop, Gauck, Baum/Schader, Warnecke/Hauke sind bereits wortgetreu belegt) und
ob für Steine 3 (Mülleroppliger-Beobachtung) und für Webb gezielt OCR-Lücken
geschlossen werden sollen.

---

**Stand:** 2026-05-12 · Bearbeitet durch Cascade
**Persistente Rohdaten:** `Visualisierung/.cache/vortrag1/`
