# OFFEN_VERIFIKATIONEN.md — Letzte Bibliotheksstunde vor 1. Mai 2026

> **Zweck:** Diese Datei sammelt die wenigen verbleibenden Detail-Seitenverifikationen
> aus dem Fliesstext von `mpv.tex`. Sie ist **nicht Teil des Abgabedossiers** und nicht
> der mündlichen Prüfung. Sie dient ausschliesslich Inti als Checkliste für die letzte
> Bibliotheksstunde, in der die Volltexte aufgeschlagen werden.
>
> **Stand:** 2026-04-24 (nach PI-Endkontrolle)
> **Vorher als `% OFFEN:`-Kommentare im LaTeX-Quelltext, jetzt extern.**

---

## Frage 1 — sieben Detailseiten

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

### 1.4 Stern-Interview (Z. 538)

- Inti-Vermutung: ca. 4-seitiges Interview.
- **Aktion:** exakte Seitenangabe ergänzen.

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

1. ZHB Luzern aufsuchen, alle drei Bücher (Preckel 2013, Trautmann 2016,
   Müller-Oppliger 2021) sowie Fischer 2020 und Stern 2025 bereitstellen.
2. Pro Punkt 1.1–2.2 die genaue Seite finden, in eine Tabelle schreiben.
3. Anschliessend pro Stelle den `\parencite`-Aufruf in `mpv.tex` um die Seite
   ergänzen, z. B.:

   ```tex
   \parencite[S.\,15]{preckel2013hochbegabung}
   ```
4. Diese Datei nach erfolgter Bibliotheksarbeit auf Status „erledigt" setzen
   und gegebenenfalls löschen.

---

## Bezug zu anderen Dokumenten

- `BELEGPFLICHT.md` und `BELEGPFLICHT_GREENFIELD.md`: weiteres Audit-Material.
- `ZITAT_AUDIT.md`: claim-by-claim-Audit der ersten Phase.
- `AGENTENKOORDINATION.md` Punkt 3: Auflösung der ursprünglichen VERIFY-Punkte.

Diese Punkte hier sind die **letzten verbleibenden** OFFEN-Stellen, die im
Fliesstext der Frage 1 noch ergänzt werden müssen, damit die 500-Seiten-Aussage
voll trägt.
