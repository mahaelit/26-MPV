# Verifikation Vorträge ↔ `mpv_abgabedokument.tex`

**Stand:** 2026-05-17 · **Geprüft:** Fragen-Wortlaute, Kernliteratur-
Locator, Inline-Cites, Konsistenz mit korrigierten `mpv.tex`-Stellen

---

## 1. Fragen-Wortlaute (FW 1 – BW 5)

**Quelle der Wahrheit:** `mpv_abgabedokument.tex` Z. 316–332 (FW-Liste),
Z. 339–635 (5 Frage-Sektionen).

| Vortrag | Wortlaut in `Vortrag*_geschaerft.md` / `Vortrag1_final.md` | Identisch zum Abgabedokument |
|---|---|---|
| **V1 / FW 1** | „Wie können verdeckte Begabungen bei neu zugewanderten, mehrsprachigen Schüler:innen mit geringen Deutschkenntnissen multiperspektivisch erfasst werden?" | ✓ identisch |
| **V2 / FW 2** | „Welche sensomotorischen und schriftsprachlichen Faktoren können dazu beitragen, dass kognitive Potenziale verdeckt bleiben und wie lassen sie sich ressourcenorientiert bearbeiten?" | ✓ identisch |
| **V3 / FW 3** | „Unter welchen relationalen Bedingungen werden die Potenziale (von S.) sichtbar und welche Rolle spielt soziale Teilhabe dabei?" | ✓ identisch |
| **V4 / BW 4** | „Inwiefern können offene, enrichment-orientierte Begabungsförderungssettings wie SOLUX Potenziale sichtbar machen, die im Regelunterricht systematisch übersehen werden?" | ✓ identisch |
| **V5 / BW 5** | „Wie gestalte ich als SHP die Beratung und Zusammenarbeit so, dass defizitorientierte Wahrnehmungen von Schüler:innen mit verdeckten Begabungen gemeinsam reflektiert und ressourcenorientiert erweitert werden?" | ✓ identisch |

**Befund:** Alle fünf Fragen-Wortlaute in den geschärften Vortragsfassungen
und in `Vortrag1_final.md` sind **wortidentisch** zum Abgabedokument
(inklusive Zeichensetzung und kursivem Innen-Einschub bei FW 3 „(von S.)").

---

## 2. Inline-Cites im Abgabedokument (Einleitung)

Das Abgabedokument enthält **keine eigentlichen Antwort-Texte** — es
bündelt die fünf Fragen samt Kernliteratur-Tabellen. Inhaltliche
Beantwortung passiert in `mpv.tex`. Die einzigen Inline-Cites stehen in
der Einleitung Z. 184–296 und sind alle bibliographisch konsistent:

| Zeile | Cite | Locator | Audit-Befund |
|---|---|---|---|
| Z. 184 | `\parencites{erzinger2023pisa}[S.\,576--580]{stamm2021fehlenderblick}{bfs2022migration}…` | S. 576–580 | ✓ deckt Z01/Z02 (S. 576/577) ab |
| Z. 189 | `\parencites[S.\,76--78]{kellerkoller2025hellekoepfe}` | S. 76–78 | ✓ konsistent mit V1-Kernliteratur |
| Z. 195 | `\parencite{dvs2025bbf}` | (online) | ✓ keine Seitenangabe erforderlich |
| Z. 257 | `\parencite[S.\,63--77]{kappus2010migration}` | S. 63–77 | ⚠️ **Inkonsistenz:** Kernliteratur-Tabelle nennt S. 63–70, 74 (9 S.). Inline-Span ist größer als Tabelle. |
| **Z. 274** | `\textcite{stern2025intelligenz} sowie \textcite[S.\,218]{muelleroppliger2021begabungsmodelle}` | S. 218 | ✓ **Audit-Korrektur konsistent angewendet** (Master-Direktzitat Fazit, 2026-05-17) |
| Z. 291 | `\parencite{bfs2022migration}` | (keine) | ✓ Statistik-Quelle, OK |
| Z. 296 | `\parencite{behrensen2019inklusive,stamm2021fehlenderblick}` | (keine) | ⚠️ **Verbesserungsvorschlag:** Sammelreferenz ohne Locator. Könnte präzisiert werden zu `\parencite[S.\,89]{behrensen2019inklusive,…[S.\,576]{stamm2021fehlenderblick}}` (Konzept des guten Grundes + defizitorientierte Wahrnehmung). Aber Sammelreferenz für den Gesamtansatz ist im aktuellen Stand vertretbar. |

---

## 3. Konsistenz mit korrigierten `mpv.tex`-Stellen

Folgende Korrekturen wurden seit 2026-05-15 in `mpv.tex` umgesetzt und
sollen mit dem Abgabedokument konsistent sein:

| Korrektur in `mpv.tex` | Im Abgabedokument | Befund |
|---|---|---|
| `[S.\,218]{muelleroppliger2021begabungsmodelle}` (statt Sammel-Cite zu `muelleroppliger2021handbuch`) | Z. 274 identisch | ✓ konsistent angewendet |
| Hippocampus → Amygdala (Z. 4775–4781 `mpv.tex`) bei `evers2025stress` | keine Inline-Cite zu Evers im Abgabedokument | ✓ kein Konsistenzproblem |
| 4 Wagner-Locator-Korrekturen (S. 425 → S. 424; S. 424\psq → S. 423\psq) | keine Inline-Cite zu Wagner im Abgabedokument | ✓ kein Konsistenzproblem |
| Stamm 5 Locator-Korrekturen für Kuhl/Hofmann 2019 | keine Inline-Cite zu Kuhl 2019 im Abgabedokument | ✓ kein Konsistenzproblem |
| Müller-Oppliger-Plurale: L:3179 `S.\,41\psq` → `S.\,38` (Off-by-3) | Kernliteratur-Tabelle Z. 581 `S.\,32--42` (Komplettspan) | ✓ Komplettspan deckt S. 38 ab |
| Bibkey-Disziplin `muelleroppliger2021handbuch` → konkrete `@incollection` | Abgabedokument verwendet bereits konkrete Bibkeys | ✓ kein Sammel-Cite zur `@book`-Hülse im Abgabedokument |

**Befund:** Alle für die Vorträge relevanten Audit-Korrekturen aus
`mpv.tex` sind im Abgabedokument entweder bereits konsistent angewendet
(Müller-Oppliger S. 218) oder schlicht nicht relevant, weil das
Abgabedokument an dieser Stelle keinen Inline-Cite enthält.

---

## 4. Kernliteratur-Tabellen: Locator-Konsistenz V1–V5

| Quelle | Abgabedokument | `Vortrag*.md` Kernliteratur | Befund |
|---|---|---|---|
| `stamm2021fehlenderblick` (V1) | S. 576–585 (10 S.) | S. 576–585 (10 S.) | ✓ identisch |
| `haag2018leistungsstanddiagnostik` (V1) | S. 153–165, 187–188 (15 S.) | S. 153–165, 187–188 (15 S.) | ✓ identisch |
| `muelleroppliger2021paeddiagnostik` (V1) | S. 224–235 (12 S.) | S. 224–235 (12 S.) | ✓ identisch |
| `kappus2010migration` (V1) | S. 63–70, 74 (9 S.) | S. 63–70, 74 (9 S.) | ✓ identisch (Tabelle) |
| `hurschler2020handschriftbeurteilung` (V2) | S. 1–24 (24 S.) | S. 1–24 (24 S.) | ✓ identisch |
| `lehwald2017motivation` (V2) | S. 70–72, 84–89 (9 S.) | S. 70–72, 84–89 (9 S.) | ✓ identisch |
| `grossrieder2010anerkennung` (V3) | S. 88–94 (7 S.) | S. 88–94 (7 S.) | ✓ identisch |
| `kuhl2019diversitaet` (V3) | S. 35–54 (20 S.) | S. 35–54 (20 S.) | ✓ identisch |
| `behrensen2019inklusive` (V3) | S. 86–98 (13 S.) | S. 86–98 (13 S.) | ✓ identisch |
| `lehwald2017motivation` (V3) | S. 57–63 (7 S.) | S. 57–63 (7 S.) | ✓ identisch |
| `evers2025stress` (V3) | S. 21–27 (7 S.) | S. 21–27 (7 S.) | ✓ identisch |
| `wagener2021bfhemmendfoerdernd` (V3+V5) | S. 418–424 (7 S.) | S. 418–424 (7 S.) | ✓ identisch (Audit-Hinweis: PDF endet inhaltlich auf S. 424) |
| `reisrenzullimueller2021sem` (V4 Kern) | S. 333–345 (13 S.) | (V4-Stütze) S. 333–347 | ⚠️ **Kleininkonsistenz innerhalb Abgabedokument:** Z. 584 Kern `S.\,333--345`, Z. 679 Stütze `S.\,333--347`. Beitrag endet auf S. 345 (vgl. `Literatur/reisrenzullimueller2021sem/`). Empfehlung: Z. 679 auf S. 333–345 angleichen. |
| `lehwald2017motivation` (V4) | S. 151–158 (8 S.) | S. 151–158 (8 S.) | ✓ identisch |
| `baudson2025besserfinden` (V5) | S. 35–40 (6 S.) | S. 35–40 (6 S.) | ✓ identisch |

---

## 5. Befund-Zusammenfassung

### ✓ Konsistent (kein Handlungsbedarf)

- **Alle 5 Fragen-Wortlaute** sind in den geschärften Vorträgen wortidentisch
  zum Abgabedokument übernommen.
- **Alle Kernliteratur-Locator** für die im Audit auf Status 5 gehobenen
  Quellen (Stamm, Müller-Oppliger paeddiagnostik, Hurschler, Lehwald,
  Grossrieder, Kuhl, Behrensen, Evers, Wagner, Baudson) sind zwischen
  Abgabedokument und Vortragsfassungen identisch.
- **Müller-Oppliger Begabungsmodelle S. 218** (heutige Audit-Präzisierung)
  ist im Abgabedokument Z. 274 bereits konsistent eingebaut.
- **Faktische Korrekturen** (Hippocampus → Amygdala bei Evers; Wagner-
  Locator) sind nicht im Abgabedokument enthalten und stellen daher kein
  Konsistenzproblem dar.

### ⚠️ Kleine Inkonsistenzen im Abgabedokument selbst (nicht vortragskritisch)

1. **Kappus 2010 S. 63–77 (Z. 257)** vs. **S. 63–70, 74 (Z. 402-Tabelle)** —
   der Inline-Span ist größer als der Tabellen-Span. Beide Locator decken
   den Kernbereich. **Empfehlung:** Z. 257 auf `S.\,63--70, 74` angleichen,
   oder Tabelle erweitern. Niedrige Priorität (Stütz-Quelle).
2. **reisrenzullimueller2021sem** Z. 584 `S.\,333--345` vs. Z. 679
   `S.\,333--347` — innerhalb desselben Dokuments doppelt angegeben.
   **Empfehlung:** Z. 679 auf `S.\,333--345` angleichen (Beitrag endet
   inhaltlich auf S. 345). Niedrige Priorität.

### 💡 Optionale Präzisierung

3. **Z. 296 Sammel-Cite `\parencite{behrensen2019inklusive,stamm2021fehlenderblick}`**
   ohne Locator. Vertretbar als Sammelreferenz für den Gesamtansatz; bei
   höherer Präzisionsanforderung Locator nachreichen
   (`[S.\,89]{behrensen2019inklusive}` für „Konzept des guten Grundes" +
   `[S.\,576]{stamm2021fehlenderblick}` für defizitorientierte Wahrnehmung).
   Niedrige Priorität.

---

## 6. Bedeutung für die Vortragsfassungen

**Keine** der drei kleinen Inkonsistenzen im Abgabedokument betrifft die
Vortragsfassungen V1_final / V2-V5_geschaerft. Die Vorträge nutzen
durchgängig die im Audit verifizierten Locator (Status 5 in
`Literatur/<bibkey>/verified_quotes.md`), und diese sind mit den
Abgabedokument-Locator konsistent.

**Konkret heisst das:** Inti kann die geschärften Vorträge halten und
sich in der mündlichen Verteidigung sicher auf das Abgabedokument
berufen. Die drei Kleininkonsistenzen sind cosmetisch und können bei
einer späteren Druckversion korrigiert werden, müssen es aber nicht.

---

**Stand:** 2026-05-17 · Bearbeitet durch Cascade
