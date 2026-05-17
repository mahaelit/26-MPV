# Handover — Quellen-Audit-Workflow

**Letzte Aktualisierung:** 2026-05-16, nach Evers-2025-Audit
**Aktive Bearbeitung:** Cascade (KI-Pair-Programmer)

Dieses Dokument ist der **Wiederaufsatzpunkt** für die nächste Audit-Session. Es ergänzt `_audit_status.md` (Statusregister) durch Workflow-Wissen, Konventionen und konkrete nächste Schritte.

---

## 1. Was ist der Audit-Workflow

Sechs-Schritt-Standard für jede Quelle, die in `mpv.tex` zitiert wird:

1. **Beschaffung:** PDF lokal verfügbar machen (Swisscovery, OA-Repos, Beltz, Karg, pedocs).
2. **Kompression:** *Pflicht*. `archiv/compress_pdfs.py` (`compress_pdf(src, dst, width=1400, quality=70)`); typische Reduktion 5–10×. **Nie** unkomprimierte 20+ MB-PDFs im Repo lassen.
3. **Text-Layer-Test:** `fitz` aufrufen — ist `len(d[0].get_text()) > 0`? Wenn ja → Volltext-Workflow. Wenn nein → JPEG-Render (Q70–75, `pix.pil_save(..., format="JPEG")`) und Vision-Verifikation.
4. **Transkript / Volltext-Extraktion:** `transcript.md` oder Skript-basierte Extraktion (`_extract_quotes.py`).
5. **Pass-2-Verifikation:** Wortgetreuer Abgleich aller `mpv.tex`-Inline-Cites. Bei Foto-Scans: Vision-Inspektion der gerenderten JPEGs.
6. **Integration:** `verified_quotes.md` (Status 5), Locator-Korrekturen in `mpv.tex`, ggf. Bib-Korrekturen, dann `_audit_status.md` aktualisieren.

**Statusstufen:**
- 1 NO_LOCAL · 2 bibliographisch verortet · 3 Volltext vorhanden · 4 Pass 1 · **5 wortgetreu, zitierfähig**

---

## 2. Bilanz Stand 2026-05-16

| Status | Bibkeys | Anteil |
|---|---|---|
| **5** | **11** | 22 % |
| 3 | ca. 10 | 20 % |
| 2 | ca. 24 | 48 % |
| 1 | 5 | 10 % |

**Status-5-Anker pro Vortrag:**
- **V1** — komplett (5: Stamm, Mülleroppliger-pädDiagn., Maehler, Baudson 2025, Koop 2025).
- **V3** — fünf Anker (Kuhl 2019 PSI, Grossrieder 2010 Anerkennung, Baudson 2021 Inklusion, Behrensen 2019 Flucht, Evers 2025 Stress).
- **V4** — ein Anker (Wagner 2021).
- **V5** — fünf Anker (Baudson 2025, Koop 2025, Baudson 2021, Wagner 2021, Kuhl 2019).

V4 ist der dünnste Vortrag. Nächste Audit-Prio sollte V4 stärken.

---

## 3. Konventionen (Pflicht)

### PDF-Handling
- Komprimierung **vor** Repo-Commit. Standard 1400 px / JPEG Q70.
- Bild-Renderings nur als **JPEG** (Q70–75), niemals PNG für Foto-Scans.
- Skripte pro Quelle: `_render_pages.py`, `_extract_quotes.py`, `_verify_quotes.py` — wiederverwendbares Muster.

### Bibkey-Disziplin
- `@book` (Sammelband-Hrsg.) ≠ `@incollection` (einzelner Beitrag). **Konsistent unterscheiden.**
- Beispiel: `muelleroppliger2021handbuch` (gesamter Beltz-Sammelband) ≠ `muelleroppliger2021begabungsmodelle` (Beitrag S. 204–219).
- Wenn ein `@incollection` keinen eigenen Ordner hat, kann er physisch im Sammelband-Ordner liegen — `verified_quotes.md` aber **pro Bibkey** trennen.

### Quote-Disziplin
- Wortgetreu (Status 5) heisst: **Buchstabe für Buchstabe** + exakter Locator.
- Paraphrasen müssen explizit gekennzeichnet sein (Beispiel: „kumulative Belastung" bei Behrensen).
- Audit-Befunde (Locator-Verschiebungen, Author-Tippfehler, faktische Fehler) immer **mit Datum + Begründung** in `_audit_status.md` § Wichtige Audit-Befunde dokumentieren.

---

## 4. Kritische Fallen / Lessons Learned

1. **Vertrauen ist gut, Pass-2 ist besser.** Die Hippocampus-Falschattribution bei Evers blieb trotz Audit-Notiz vom 2026-04-28 stehen, weil die Notiz selbst falsch war („bereits entfernt" — war es nicht). **Jede frühere Notiz gegen Quelle re-prüfen.**
2. **Off-by-one bei Sammelband-Locatoren.** Wagner 2021: alle 4 Locator waren `S. 425` statt `S. 424` — der Beitrag endet inhaltlich auf S. 424, S. 425 ist Literaturverzeichnis. **Immer Endseite gegen Beitrag-Korpus prüfen.**
3. **Author-Tippfehler in Bib.** Wagner ≠ Wagener. Korrekt: Bib-Author korrigieren, Bibkey aus Konsistenzgründen behalten.
4. **Folder-Naming-Drift.** `kuhl2021begabungbildungbeziehung` (Bibkey) vs. `Kuhl2021bildungbegabung` (Folder). Bei `find_by_name` notfalls Glob nutzen.
5. **Inline-Cite ≠ Sammel-Cite.** Wenn ein Beitrag im Sammelband zitiert wird, **immer** `[S.\,X--Y]` davor — Sammel-Cites ohne Seitenangabe sind heuristisch schwer prüfbar (siehe `muelleroppliger2021handbuch` mit 14 Cite-Stellen).

---

## 5. Wiederaufsatzpunkt — `muelleroppliger2021begabungsmodelle`

**Status bei Übergabe:** Workflow läuft, Skript wurde abgebrochen.

### Was schon erledigt ist
- Sammelband-Ordner identifiziert: `Literatur/muelleroppliger2021handbuch/`
- PDF gefunden: `Mülleroppliger2021begabungsmpdeöle S.204-219.pdf` (44.5 MB, 16 Seiten, **Foto-Scan, kein Text-Layer**).
- Volltext-Transkript existiert bereits: `excerpts/teil2_begabung_und_begabungsfoerderung_konzepte_modelle.md` Zeile 34 (30'987 chars, der gesamte Begabungsmodelle-Beitrag in einer Zeile).
- 4 Inline-Cites in `mpv.tex` lokalisiert: Z. 574, 617, 636, 645 — alle `[S.\,204--219]`, alle zur Potenzial/Performanz-Differenzierung und Kontext-Sichtbarkeit.
- Bestehende `verified_quotes.md` ist auf Status 2 und behandelt **nicht** den Begabungsmodelle-Beitrag, sondern verweist auf Sekundärbeleg `hoyer2013begabung`.

### Was als nächstes zu tun ist
1. **PDF komprimieren** (44.5 MB → ~5 MB) via `archiv/compress_pdfs.py` und als `source.pdf` ablegen — am besten in eigenem Ordner `Literatur/muelleroppliger2021begabungsmodelle/` (Bibkey-konsistent).
2. **JPEG-Renderings** der 16 Seiten für Vision-Verifikation.
3. **Volltext-Auszug** aus `teil2_*.md` Zeile 34 als `transcript.md` ablegen.
4. **Wortgetreue Zitate** für die 4 Inline-Cites suchen — Schlüsselbegriffe: „Potenzial", „Performanz", „Renzulli", „Mönks", „Heller/Perleth", „Ziegler/Aktiotop", „Gagné/DMGT", „motivational", „Umweltmerkmal", „Zusammenspiel", „verdeckt", „sichtbar", „Kontext".
5. **Eigene `verified_quotes.md`** für Bibkey `muelleroppliger2021begabungsmodelle` erstellen — Status 5.
6. Bestehende `muelleroppliger2021handbuch/verified_quotes.md` als Sammelband-Übersicht stehenlassen (sie listet 6 Sammel-Cites ohne Seitenangabe; diese Cites müssen separat in `mpv.tex` auf konkrete `@incollection`-Bibkeys mit Locator umgestellt werden — eigener Folge-Audit).
7. `_audit_status.md` Bilanz auf 12 Status-5-Bibkeys erhöhen.

### Pending offene Folge-Audits (nach Begabungsmodelle)
| Prio | Bibkey | Begründung |
|---|---|---|
| H | `hurschler2020handschriftbeurteilung` (V2) | V2 hat noch keinen Status-5-Anker |
| H | `muelleroppliger2021plurale` (V4) | V4-Stärkung |
| M | `muelleroppliger2021handbuch` Sammel-Cite-Audit | 6 Cites ohne Locator → präzisieren auf `@incollection` |
| M | `kuhl2021begabungbildungbeziehung` (V3) | nur Kernliteratur-Tabelle, kein inline-Cite |
| L | `boosnuenning2022interethnisch` (V3) | Status 3, niedrige Cite-Dichte |

---

## 6. Werkzeuge & Pfade

- **Statusregister:** `Literatur/_audit_status.md`
- **Komprimierungs-Skript:** `archiv/compress_pdfs.py`
- **Render-Beispiel-Skript:** jedes `Literatur/<bibkey>/_render_pages.py`
- **Verify-Beispiel:** `Literatur/kuhl2019diversitaet/_verify_quotes.py`
- **Vortrags-Dokumente:** `Vortrag1_geschaerft.md`, `Vortrag3_*.md` etc. — werden **nach** jedem Audit mit den neuen wortgetreuen Zitaten angereichert.

---

## 7. Bekannte Audit-Befunde (zentrale)

Quellen mit dokumentierten Korrekturen am 2026-05-16, die in der mündlichen Verteidigung relevant werden können:

- **Evers 2025:** Hippocampus → Amygdala + präfrontaler Cortex (faktischer Fehler in `mpv.tex` Z. 4775–4781, korrigiert).
- **Wagner 2021:** Author-Korrektur (Wagener → Wagner) + 4 Locator-Korrekturen.
- **Behrensen 2019:** „kumulative Belastung" ist Paraphrase, nicht Direktzitat.
- **Kuhl 2019:** S. 35 fehlt im Repo-PDF (Z01 Caveat, Status 4 für dieses eine Zitat).
- **Pauly 2025:** Locator-Fehler `mpv.tex` L:796 korrigiert.

Vollständige Liste mit Begründungen: `_audit_status.md` § Wichtige Audit-Befunde.
