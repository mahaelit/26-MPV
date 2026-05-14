# Open-Book-Prüfungsvorbereitung – Bedienungsanleitung

**Zweck:** Für die bevorstehende Open-Book-Prüfung sind alle Quellen-Belege aus `mpv.tex`
strukturiert, prüfbar und per Direct-Link auffindbar aufbereitet.

## Die drei zentralen Dokumente

### 1. `QUELLEN_INVENTAR.md` – Was ist da, was fehlt?
Tabellen-Übersicht aller 60 BibKeys mit Ampelfarben:
- **GRUEN** (2): Volltext + verifizierte Zitate, prüfungsfertig.
- **GELB+** (5): Volltext + Kapitel-Splits, aber Zitate noch nicht wortgetreu belegt.
- **GELB** (8): Volltext vorhanden, aber keine Splits.
- **GELB-K** (5): Volltext **zu kurz** (<15 Seiten) – vermutlich nur Auszug! **Prüfen!**
- **ROT** (25): **Kein Volltext**, Beschaffung zwingend.

### 2. `BESCHAFFUNG.md` – Was in der Bibliothek bestellen?
30 Quellen brauchen Beschaffung, nach Cite-Zahl priorisiert.
**Top-5 Prioritäten** (Hauptwerke der Arbeit):

| Prio | Cites | BibKey | Anmerkung |
|---:|---:|---|---|
| 1 | 13 | `buholzer2010allegleich` | Nur 2-Seiten-Auszug! |
| 2 | 13 | `lehwald2017motivation` | Nur 13-Seiten-Auszug! |
| 3 | 11 | `booth2019index` | Kein Volltext |
| 4 | 11 | `kappus2010migration` | Kein Volltext |
| 5 | 11 | `muelleroppliger2021handbuch` | Über `hoyer2013begabung` als Sekundärbeleg abgedeckt |

Jeder Eintrag hat einen direkten Swisscovery-Link.

### 3. `PRUEFUNGSKOMPENDIUM.md` – Das Hauptdokument für die Prüfung
**249 Cite-Stellen** (207 Lerndokument + 42 Abgabedokument), nach Arbeit-Abschnitten gruppiert.
Pro Cite-Stelle:
- Zeilennummer + Kapitelkontext der Arbeit
- Originalkontext (Satz, der die Behauptung macht)
- Liste aller zitierten Quellen mit Ampel-Status
- **Direct-Link** zum Verifikations-Dokument + Kapitel-Split-PDF
- **Automatischer Beleg-Vorschlag** (62 Stück): der wahrscheinlichste Kapitel-Split, der den Claim belegt – per Keyword-Matching aus dem Split-Volltext-Index

---

## Die Kapitel-Splits pro Quelle

Für jede Quelle mit PDF-Volltext liegen unter `Literatur/<bibkey>/excerpts/` folgende Dateien:

- `_outline.md`: Übersicht aller Kapitel mit Seitenzahlen und Titel
- `NNN_<slug>.pdf`: Ein PDF pro Kapitel, direkt öffenbar

**Gesamt: 316 Kapitel-Splits über 16 Quellen.** Erzeugt durch:
1. PDF-Bookmarks (wenn vorhanden)
2. Text-TOC-Extraktion aus den ersten Seiten (Fallback)
3. Nummerierte Überschriften im Volltext (2. Fallback)

Beispiel – für den zentralen Beleg zu Multiple Intelligenzen (Gardner):
- `Literatur/hoyer2013begabung/excerpts/018_5_1_konzepte_und_modelle.pdf` (S. 64–74, 11 Seiten)
- `Literatur/hoyer2013begabung/excerpts/027_6_6_turning_point_das_three_ring_concept.pdf` (S. 93–95)

---

## Workflow während der Prüfung

1. **Frage lesen** im Lerndokument (`mpv.tex`) oder Abgabedokument.
2. **Cite-Stelle identifizieren** (z.B. `\parencite{fischer2020begabungsfoerderung}`).
3. **`PRUEFUNGSKOMPENDIUM.md` öffnen**, nach Zeilennummer oder Keyword suchen.
4. **Direct-Link klicken** → landet direkt im passenden Kapitel-Split als PDF.
5. **Ggf. in `verified_quotes.md`** das wortgetreue Zitat mit Seitenangabe nachschlagen.

**Alternativer Arbeitspfad pro Quelle:**
- Öffne `Literatur/<bibkey>/verified_quotes.md`
- Im CLAIMS-Block siehst du alle Cite-Stellen dieser Quelle + pro Stelle den empfohlenen Kapitel-Split
- Direktlink zum Split-PDF → verifiziere das Zitat → trage unten in der Zitate-Sektion ein

---

## Pflege-Skripte (falls nochmal laufen)

Alle Skripte sind idempotent. Reihenfolge bei Änderungen:

```powershell
# 1. Cite-Kontext aktualisieren (nach Änderungen in mpv.tex)
python cite_context.py

# 2. Transkript-Integration (nach neuen Transkripten)
python analyze_transkripte.py
python integrate_transkripte.py

# 3. Kapitel-Splits aus PDFs (nach neuen Volltexten in Literatur/<key>/source.pdf)
python extract_excerpts.py          # erzeugt neue Splits (inkl. TOC- und Heading-Fallback)
python extract_excerpts.py --force  # überschreibt
python verify_excerpts.py           # validiert alle Splits

# 3b. Claim->Split-Matching refresh (nach neuen Splits):
#     - Lösche pro Quelle Literatur/<key>/excerpts/_index.json, damit neu gebaut wird
#     - Oder warte, es wird beim nächsten Aufruf automatisch neu gebaut

# 4. Rewrites sammeln und anwenden (nach neuen verified_quotes-Rewrite-Blöcken)
python collect_rewrites.py
python apply_rewrites.py              # Dry-Run
python apply_rewrites.py --apply --yes  # real

# 5. Zentrale Reports neu rendern
python build_inventar.py     # QUELLEN_INVENTAR.md + BESCHAFFUNG.md
python build_index.py        # Literatur/_INDEX.md
python build_kompendium.py   # PRUEFUNGSKOMPENDIUM.md
```

---

## Status-Quo

**Stand der Verifikation:**

- `fischer2020begabungsfoerderung` (13 Cites) · GRUEN · 32 Kapitel-Splits, Status 4
- `preckel2013hochbegabung` (13 Cites) · GRUEN · EPUB, Status 4
- `hoyer2013begabung` · GRUEN · 41 Splits + 12 wortgetreue Zitate, Status 4 (Sekundärbeleg für `muelleroppliger2021handbuch`)
- `leikhof2021jugendliche` (10 Cites) · GELB+ · 29 Splits, Verifikation offen
- `gubbins2020promising` (8 Cites) · GELB+ · 18 Splits, Verifikation offen
- `bfs2022migration` · GELB+ · 73 Splits
- `maehler2018diagnostik` · GELB+ · 8 Splits
- `erzinger2023pisa` · GELB+ · 7 Splits

**Verbleibende Aufgaben nach Priorität:**

1. **Beschaffung der GELB-K-Quellen** (Hauptwerke mit unvollständigem PDF):
   - `buholzer2010allegleich` (Klett und Balmer, CH-Schulverlag)
   - `lehwald2017motivation` (Beltz Juventa)
2. **Beschaffung der ROT-Top-5** (siehe BESCHAFFUNG.md)
3. **Optional:** `verified_quotes.md` für GELB+-Quellen auf Status 3 hochziehen (wortgetreue Zitate nachtragen)

---

## Bekannte Einschränkungen

- **PDF-Bookmarks sind bei einigen Verlagen um 1 Seite versetzt** (z.B. `hoyer2013begabung`: Kap 7.1 Bookmark zeigt auf Buch-S.101, der eigentliche Kapitelinhalt beginnt aber auf S.102). Die Kapitel-Splits enthalten den Inhalt trotzdem komplett (+ evtl. letzte Seite des Vorkapitels). **Bei Unklarheit: Nachbar-Split anschauen.**
- 8 Volltext-Quellen haben **keine PDF-Bookmarks** (Artikel/Einzelkapitel). Dort ist `source.pdf` direkt die Referenz – keine Kapitel-Splits möglich.
- Verschlüsselte PDFs (wie `erzinger2023pisa`) brauchen `cryptography` Python-Paket (ist installiert).
