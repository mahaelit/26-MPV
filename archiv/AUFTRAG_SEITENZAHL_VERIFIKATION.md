# Auftrag: Seitenzahl-Verifikation aller Zitationen in mpv.tex

**Erstellt:** 2026-04-25  
**Auftraggeber:** Inti Merolli  
**Priorität:** Kritisch (Abgabe 1. Mai 2026)

---

## Dein Auftrag

Gehe **jede einzelne Zitation mit Seitenangabe** in `mpv.tex` durch und prüfe,
ob die angegebene Seitenzahl im Volltext der Quelle tatsächlich die im Text
behauptete Aussage enthält.

## Kontext

Wir haben soeben entdeckt, dass `\parencite[S.\,14,\,17,\,36]{fischer2020begabungsfoerderung}`
falsch war — das Münchner Hochbegabungsmodell steht auf **S. 76**, nicht auf S. 14/17/36.
**Solche Fehler können überall im Dokument existieren.** Dein Job ist, sie alle zu finden.

## Vorgehen

### Schritt 1: Alle Zitationen mit Seitenangaben extrahieren

```bash
grep -nE '\\(parencite|textcite|autocite)\[.*S\.\\\,.*\]' mpv.tex
```

Das liefert dir jede Zeile mit einer Seitenangabe. Erstelle daraus eine Arbeitsliste.

### Schritt 2: Pro Zitation verifizieren

Für **jede** Zitation mit Seitenangabe:

1. **Lies den TeX-Kontext** (±3 Zeilen): Was wird behauptet?
2. **Identifiziere den BibKey** und die behauptete Seitenzahl.
3. **Öffne den Volltext** mit PyMuPDF:
   ```python
   import fitz
   doc = fitz.open(f'Literatur/{bibkey}/source.pdf')
   text = doc[seitenzahl - 1].get_text()  # 0-indexiert!
   ```
4. **Prüfe:** Steht die behauptete Aussage auf dieser Seite?
   - **Ja → ✅** Zitation korrekt, weiter.
   - **Nein → ❌** Suche die richtige Seite:
     ```python
     for i in range(len(doc)):
         if '<schlüsselbegriff>' in doc[i].get_text().lower():
             print(f'Gefunden auf S. {i+1}')
     ```
   - **Kein PDF vorhanden →** Prüfe `excerpts/_outline.md` für Kapitelspannen.
     Wenn auch das nicht hilft: markiere als `% OFFEN`.

### Schritt 3: Korrekturen durchführen

- **Falsche Seitenzahl:** Korrigiere direkt in `mpv.tex`.
- **Nicht verifizierbar (kein Volltext):** Setze `% OFFEN: kein Volltext verfügbar`.
- **Richtig:** Keine Änderung nötig.

### Schritt 4: Ergebnisbericht

Erstelle am Ende eine Tabelle:

```markdown
| Zeile | BibKey | Behauptete Seite | Status | Korrekte Seite | Aktion |
|-------|--------|-----------------|--------|----------------|--------|
| 584   | fischer2020… | S. 14,17,36 | ❌ | S. 76 | Korrigiert |
| 588   | stamm2021… | S. 576–585 | ✅ | — | — |
| …     | …      | …               | …      | …              | …      |
```

## Regeln (ZWINGEND)

1. **Lies `QUELLENAGENT_ANLEITUNG.md` und `BELEGPFLICHT.md` zuerst.** Dort stehen
   alle Konventionen und Verbote.

2. **No page without proof.** Wenn du die Seite nicht im Volltext findest, darfst
   du sie NICHT stehen lassen. Entferne die Seitenangabe und setze `% OFFEN`.

3. **Keine Schätzungen.** Wenn S. 76 das Münchner Modell enthält, aber der Text
   „S. 76–78" behauptet, prüfe auch S. 77 und 78. Nicht annehmen, dass es stimmt.

4. **PDF-Seitenzahl ≠ Buchseitenzahl.** Bei manchen PDFs gibt es Offsetseiten
   (Titelei, römische Zählung). Verifiziere immer anhand der im Text **gedruckten**
   Seitenzahl, nicht des PDF-Index.

5. **Sammelbände:** Bei `muelleroppliger2021handbuch`, `buholzer2010allegleich` und
   `reintjes2019begabungsfoerderung` liegen die Einzelkapitel als eigene BibKeys vor.
   Prüfe, ob der richtige BibKey verwendet wird (Sammelband vs. Einzelkapitel).

## Verfügbare Quellen im Repo

Für jede Quelle mit Volltext findest du:
- `Literatur/<bibkey>/source.pdf` — das PDF
- `Literatur/<bibkey>/excerpts/_outline.md` — Kapitelverzeichnis mit Seitenspannen
- `Literatur/<bibkey>/.extracted/poppler.txt` — Textextraktion (Seitentrenner: `\x0C`)
- `Literatur/<bibkey>/verified_quotes.md` — bereits verifizierte Zitate

Wenn `source.pdf` nicht existiert, gibt es keinen Volltext. Dann:
- Nutze `_outline.md` für Kapitelspannen (falls vorhanden)
- Nutze das `annotation`-Feld in `Quellen.bib`
- Markiere als `% OFFEN`

## Erwartetes Ergebnis

- Alle falschen Seitenzahlen in `mpv.tex` sind korrigiert.
- Alle nicht verifizierbaren Seitenzahlen sind als `% OFFEN` markiert.
- Ein Ergebnisbericht (Tabelle) ist erstellt.
- `mpv.tex` kompiliert weiterhin fehlerfrei.

---

*Dieser Auftrag wurde erstellt, nachdem eine halluzinierte Seitenangabe
(Fischer 2020, S. 14/17/36 statt S. 76) entdeckt wurde. Es ist davon
auszugehen, dass weitere solche Fehler existieren.*
