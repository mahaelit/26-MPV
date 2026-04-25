# OFFEN_VERIFIKATIONEN.md — Letzte Bibliotheksstunde vor 1. Mai 2026

> **Zweck:** Diese Datei sammelt die wenigen verbleibenden Detail-Seitenverifikationen
> aus dem Fliesstext von `mpv.tex`. Sie ist **nicht Teil des Abgabedossiers** und nicht
> der mündlichen Prüfung. Sie dient ausschliesslich Inti als Checkliste für die letzte
> Bibliotheksstunde, in der die Volltexte aufgeschlagen werden.
>
> **Stand:** 2026-04-25 (nach Plan-Beschluss "Bibliotheksstunde + Pauschalaussage halten")
> **Vorher als `% OFFEN:`-Kommentare im LaTeX-Quelltext, jetzt extern.**

---

## Priorität A — Hauptverifikationen für das Abgabedokument

Diese zwei Stellen tragen die Pauschalaussage "Jede der 500 Seiten ist verifiziert
gelesen" im Abgabedokument (`mpv_abgabedokument.tex` Z. 522–525). Vor Abgabe
zwingend am physischen Buch zu prüfen.

### A.1 Fischer 2010 (`fischer2010begabung`) — F4-Korpus

- **Bib-Stand:** 17 S. (S. 97–113) im Buholzer-Sammelband, Schätzung gestützt auf
  Reihenfolge Kappus 63–77, Grossrieder 87–96.
- **Aktion:** Spanne S. 97–113 am Druck bestätigen.
- **Eintrag nach Verifikation:** ___ S. (S. ___–___)

### A.2 Baum/Schader 2021 (`baumschader2021twice`) — F4-Korpus

- **Bib-Stand:** 14 S. (S. 588–601) im Handbuch Begabung (Beltz). Volltext via
  `teil8_dysfunktionale_begabungsentwicklung.md` bereits verfügbar.
- **Aktion:** Spanne S. 588–601 am gedruckten Beltz-Band bestätigen.
- **Eintrag nach Verifikation:** ___ S. (S. ___–___)

### A.3 Stern 2025 (`stern2025intelligenz`) — F1-Korpus (NEU, OP-Plan)

- **Bib-Stand:** keine `pages`-Angabe in `Quellen.bib`; ca. 4-seitiges Interview
  in *Bildung Schweiz* 3/2025.
- **Aktion:** Exakte Seitenspanne am Heft nachschlagen, Bib-Eintrag um
  `pages = {...--...}` ergänzen, F1-Kernliteratur und Seitenbudget-Tabelle im
  Abgabedokument an die tatsächliche Seitenzahl anpassen.
- **Eintrag nach Verifikation:** ___ S. (S. ___–___)

---

## Priorität B — Detailseiten Frage 1 (für Lerndokument)

### 1.1 Drei-Ringe-Modell nach Renzulli (Z. 489–495 in `mpv.tex`)

- Inti-Vermutung: `preckel2013hochbegabung` S. 15, `trautmann2016einfuehrung` S. 52–54,
  `muelleroppliger2021handbuch` (Kap. Begabungsmodelle).
- **Aktion:** Seitenzahlen am Druck nachschlagen und in den `\parencite`-Aufruf
  ergänzen.

### 1.2 Münchner Hochbegabungsmodell (Z. 496)

- Inti-Vermutung: `muelleroppliger2021handbuch` S. 211, `trautmann2016einfuehrung`
  S. 59–62.
- **Aktion:** verifizieren.

### 1.3 Fischer 2020 — Lernarchitektur (Z. 500)

- Inti-Vermutung: konkretes Kapitel/Seitenbereich zur Lernarchitektur und
  Bildungsgerechtigkeit.
- **Aktion:** am Druck verifizieren.

### 1.4 Stern-Interview (Z. 538) — siehe Priorität A.3

(verschoben nach oben, weil für das Abgabedokument relevant.)

### 1.5 Müller-Oppliger Handbuch — dynamische Begabungs-Lesart (Z. 549)

- **Aktion:** konkretes Kapitel/Seitenbereich für die dynamische Begabungs-Lesart
  am Druck verifizieren.

### 1.6 Preckel/Baudson — nicht-kognitive Faktoren / Underachievement (Z. 567, Z. 569)

- Inti-Vermutung: `preckel2013hochbegabung` S. 43–46, `fischer2020begabungsfoerderung`
  S. 281–282 / 411–413.
- **Aktion:** verifizieren.

### 1.7 Keller-Koller-Ergänzung (Z. 607)

- **Aktion:** ergänzend wissenschaftlichere Studie zu Keller-Koller 2009/2011
  nachschlagen.

---

## Frage 1, 2e-Unterabschnitt — eine Detailseite

### 2.1 Preckel/Baudson zum 2e-Argument (Z. 526, Z. 784)

- Inti-Vermutung: `preckel2013hochbegabung` S. 47.
- **Aktion:** am Druck verifizieren; ergänzend Lehwald-Stelle prüfen.

---

## Frage 2 — eine Detailseite

### 2.2 Lehwald-Kapitel zur Underachievement-Mechanik (Z. 807, Z. 819)

- **Aktion:** Lehwald-Kapitel-Seitenangabe nachtragen.

---

## Verfahren in der Bibliotheksstunde

1. ZHB Luzern aufsuchen, folgende Werke bereitstellen:
   - **Priorität A** (zwingend): Buholzer/Kummer Wyss 2010 (für A.1 Fischer-Kap.),
     Müller-Oppliger/Weigand 2021 Handbuch Begabung (für A.2 Baum/Schader-Kap.),
     *Bildung Schweiz* Heft 3/2025 (für A.3 Stern-Interview).
   - **Priorität B/C/D**: Preckel 2013, Trautmann 2016, Fischer 2020, Lehwald 2017.
2. **Zuerst Priorität A abarbeiten** (drei Spannen verifizieren, Eintragstabelle oben füllen).
3. Anschliessend Priorität B (Punkte 1.1, 1.2, 1.3, 1.5, 1.6, 1.7) und die
   verbleibenden Detailpunkte 2.1 und 2.2 abarbeiten — die genaue Seite finden,
   in den jeweiligen Abschnitt eintragen.
4. Anschliessend:
   - Pro Stelle den `\parencite`-Aufruf in `mpv.tex` um die Seite ergänzen, z. B.
     `\parencite[S.\,15]{preckel2013hochbegabung}`.
   - Falls A.3 (Stern) eine andere Seitenzahl als 4 ergibt: F1-Summe und
     Seitenbudget-Tabelle in `mpv_abgabedokument.tex` (Z. 353 und Z. 509–515)
     auf den korrekten Wert nachjustieren.
   - Falls A.1 oder A.2 abweicht: in `Quellen.bib` `pages`/`annotation` korrigieren
     und Seitenbudget-Tabelle prüfen.
5. Diese Datei nach erfolgter Bibliotheksarbeit auf Status „erledigt" setzen
   und gegebenenfalls löschen.

---

## Bezug zu anderen Dokumenten

- `BELEGPFLICHT.md` und `BELEGPFLICHT_GREENFIELD.md`: weiteres Audit-Material.
- `ZITAT_AUDIT.md`: claim-by-claim-Audit der ersten Phase.
- `AGENTENKOORDINATION.md` Punkt 3: Auflösung der ursprünglichen VERIFY-Punkte.

Diese Punkte hier sind die **letzten verbleibenden** OFFEN-Stellen, die im
Fliesstext der Frage 1 noch ergänzt werden müssen, damit die 500-Seiten-Aussage
voll trägt.
