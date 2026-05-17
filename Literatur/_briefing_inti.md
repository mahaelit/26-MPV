# Briefing für Inti — Zusammenarbeit mit dem AI-Agenten

**Stand:** 17.05.2026 · **Repo:** `26-MPV` · **Letzter Audit:** Lehwald 2017 (V2+V3+V4)

Dieses Dokument hilft dir, **selbständig mit dem AI-Agenten** an deinem Audit-Workflow weiterzuarbeiten. Es ist absichtlich kurz — alle Details stehen in `_audit_status.md`.

---

## 1. Was der Agent für dich macht

Pro Quelle ein 5-stufiger Audit:

1. **PDF aufbereiten:** Konsolidieren mehrerer Kapitel-PDFs, Kompression von Foto-Scans (`archiv/compress_pdfs.py`, 1400 px / Q70).
2. **Cite-Stellen finden:** Alle `\cite{bibkey}` / `\textcite{...}` / `\parencite{...}` in `mpv.tex` und `mpv_abgabedokument.tex`.
3. **Wortgetreu verifizieren:** Volltext-Extraktion (Text-PDFs) oder Vision-Inspektion gerenderter JPEGs (Foto-Scans).
4. **Locator korrigieren:** Wenn die Seitenangabe in `mpv.tex` nicht zur Quelle passt (Off-by-1, Off-by-3 etc.), wird sie direkt korrigiert.
5. **Dokumentieren:** `verified_quotes.md` pro Quelle (Status 5 = wortgetreu zitierfähig); `_audit_status.md` als zentrale Übersicht.

**Status-Skala:**
- **5** = wortgetreu, zitierfähig (alle Cite-Stellen abgesichert)
- 4 = Volltext extrahiert, aber nicht systematisch verglichen
- 3 = Sammelband-/Text-PDF vorhanden, aber nur paraphrasiert
- 2 = bibliographisch verortet (PDF da, aber kein Audit)
- 1 = NO_LOCAL (PDF muss noch beschafft werden)

---

## 2. Wie du einen neuen Audit anstösst

**Einfachster Satz:**
> „Mach Audit für `bibkey`."

oder

> „Nächste Prio."  (dann nimmt der Agent den nächsten Punkt aus `_audit_status.md` § Audit-Prioritäten)

**Was der Agent automatisch macht:**
- Stand prüfen (PDF-Status, Anzahl `mpv.tex`-Cites)
- Plan zeigen, dann durchziehen
- Bei langen PDFs: pragmatische Entscheidung (komplett vs. nur Cite-Seiten)

**Was du **vor**her klären solltest, wenn relevant:**
- Soll ich Originale löschen nach Konsolidierung? (Default: ja, sind in OneDrive-Versionierung)
- Renderings auf `/tmp` (schnell, flüchtig) oder `pages/` im Repo (langsam, persistent)?

---

## 3. Wenn dir sprachlich/inhaltlich etwas nicht passt

### A) An einem fertigen `verified_quotes.md`-Eintrag

> „Im Lehwald-`verified_quotes.md`, Z03: ‚Wandel der Attribuierung' — schreib das doch um in eine prägnantere Formulierung für meinen Vortrag."

Der Agent macht dann eine **separate** „Vortragsformulierung"-Sektion im selben Dokument, ohne die wortgetreuen Zitate zu verändern. So bleibt die Quellentreue erhalten.

### B) An einem mpv.tex-Absatz

> „Z. 2185 — die Pawel-Stelle wirkt zu lehrbuchmäßig. Mach das fallnaher zu S."

Der Agent zeigt dir den aktuellen Absatz, schlägt 2-3 Varianten vor, du wählst.

### C) An einem Locator

> „Bei `\parencite[S.\,X]{quelle}` bin ich unsicher — bitte verifizieren."

Der Agent öffnet die Quelle, prüft, korrigiert wenn nötig + dokumentiert den Befund.

---

## 4. Wenn eine Quelle fehlt

### Status 1 (NO_LOCAL) — PDF nicht im Repo

Der Agent kann nichts verifizieren, kann aber:
- Swisscovery-Suchlink generieren
- Open-Access-Quelle prüfen (pedocs, Karg-Stiftung, Pauly-Sammelband etc.)
- Vorschlag: temporär aus dem `mpv.tex`-Cite ausbauen oder durch verfügbare Quelle ersetzen

**Aktuelle NO_LOCAL-Quellen** (5):
- `weigand2021separativ` (V4)
- `sedmak2021bildungsgerechtigkeit` (V4)
- `greiten2021underachievement` (V2/V3)
- `trautmann2016einfuehrung` (V4)
- `boehm2017unterrichtsstoerungen` (V2)

Wenn du eine davon brauchst: PDF beschaffen, in `Literatur/<bibkey>/source.pdf` ablegen, dann „mach Audit".

### Quelle nicht im Repo, aber inhaltlich gewünscht

> „Ich brauche etwas zu [Thema]. Hast du Vorschläge?"

Der Agent kann ähnliche Quellen aus dem bestehenden Korpus vorschlagen oder neue identifizieren.

---

## 5. Wenn der Agent etwas Faktisches falsch macht

**Sag es direkt:**

> „Du hast Z03 als wortgetreu markiert, aber bei mir steht ‚X' und in der Quelle ‚Y'. Bitte nochmal verifizieren."

Der Agent geht dann **immer zur Quelle zurück** (nicht zum Memo). Das ist ein wichtiges Prinzip im Workflow.

**Bekannte Fehlerquellen, die du im Auge behalten solltest:**
- **Audio-Transkripte sind nicht zitierfähig** — Hörfehler bei Eigennamen („Renzoli" statt „Renzulli", „Stachoviak" statt „Stachowiak"). Verwende sie nur als Themen-Übersicht.
- **OCR-Fehler bei Foto-Scans** — Vision-Verifikation am Bild ist immer der Goldstandard, nicht OCR-Text.
- **Off-by-N-Locator** — wenn der Agent einen Locator findet, prüf ihn doppelt, wenn die Aussage besonders zentral ist (z.B. konkrete Zahlen, Master-Zitate).

---

## 6. Wartezeit-Diagnose

| Symptom | Vermutliche Ursache | Was du tun kannst |
|---|---|---|
| Skript-Aufruf hängt 30-60 s nach „DONE"-Meldung | OneDrive-Sync der neuen Datei | Warten — keine Aktion |
| Vision-Call braucht ~10 s pro Bild | Bilderkennung (normal) | Tipp: dem Agenten sagen „rendere auf /tmp" |
| Mehrere Minuten ohne Output | Langer Vision-Call oder PDF-Compress läuft | Den Agenten fragen: „was machst du gerade?" |
| Vom Agenten Fragen-Liste mit 3-4 Optionen | Du sollst eine strategische Wahl treffen | Wähle bewusst — kein Zeitdruck |

---

## 7. Aktuelle Prio-Liste (Stand 17.05.2026)

**Multi-Cite-Hebel zuerst:**
1. **`gold2018lesenkannmanlernen`** (V2, **11 Cites**) — größter offener V2-Hebel
2. **`nottbusch2017graphomotorik`** (V2, 5 Cites) — V2-Schreibförderung
3. **`saegesserwyss2021grafinkrahmenmodell`** (V2, 5 Cites) — V2-Schreibförderung

**Niedrige Prio (kein Inline-Cite):**
- `kuhl2021begabungbildungbeziehung` (V3) — nur in Kernliteratur-Tabelle

**NO_LOCAL beschaffen** (siehe § 4).

---

## 8. Konventionen, die der Agent automatisch befolgt

- **Wortgetreue Zitate** in `>` (Markdown-Blockquote) mit Locator in Klammern dahinter
- **Locator-Notation:** `S.\,N` (geschütztes Leerzeichen LaTeX), Bereiche mit `--` (Endash)
- **Status-Updates** in `_audit_status.md` — niemals lautloses Downgrade
- **Backups** vor destruktiven Änderungen (`*.backup`-Suffix)
- **Status-Downgrade** muss mit Datum + Begründung dokumentiert werden, nie still
- **`@book` vs. `@incollection`:** konkrete Beiträge bekommen eigenen Bibkey mit Locator, Sammelband-Hülse nur als `crossref`

---

## 9. Pro-Tipps

- **Multi-Vortrag-Quellen** maximieren den Hebel (Lehwald 2017 brachte 3 Anker auf einmal). Wenn du eine Quelle hast, die in V2+V3+V4 mehrfach zitiert wird, lohnt sich der Audit doppelt.
- **Master-Direktzitate** kennzeichnen — das sind die 1-2 Stellen pro Quelle, die du im Vortrag laut vorlesen kannst.
- **„Differenzierung" vs. „Lehwalds Klassifikation"** — der Agent dokumentiert in `verified_quotes.md` immer, ob deine `mpv.tex`-Aufzählung **wortgetreu** aus der Quelle kommt oder eine **legitime Auswahl** ist. Beides ist OK, aber der Unterschied ist wichtig für die mündliche Verteidigung.
- **Heutige Renaming-Konvention:** alle Quellen-PDFs heißen `source.pdf` (nicht der Originalname). Das ist konsistent über das ganze Repo.
- **Tagesabschluss:** Lass dir am Ende einer Session einen Commit mit einer Zusammenfassung wie heute „seit gestern" generieren — das ist Gold wert für die mündliche Verteidigung.

---

## 10. Wichtige Dateien zum Selbst-Nachsehen

| Datei | Zweck |
|---|---|
| `Literatur/_audit_status.md` | **Zentrale Übersicht** — Status, Prio, Audit-Befunde |
| `Literatur/<bibkey>/verified_quotes.md` | **Pro Quelle** — wortgetreue Zitate |
| `Literatur/<bibkey>/source.pdf` | **Pro Quelle** — komprimierte Quellen-PDF |
| `Literatur/_handover.md` | Workflow-Handover (älter, ggf. als Referenz) |
| `mpv.tex` / `mpv_abgabedokument.tex` | Deine Lerndokumente |
| `Quellen.bib` | BibTeX-Datenbank |

---

**Wenn etwas unklar ist, frag den Agenten direkt — er kann dir jeden seiner Schritte erklären, ohne neue Aktionen anzustoßen.**
