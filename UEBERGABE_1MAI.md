# Übergabe an Inti — Letzte Schritte bis zum 1. Mai 2026

**Stand:** Sa, 25. April 2026, 10:20 Uhr
**Frist:** Fr, 1. Mai 2026, Moodle-Upload
**Datei zur Abgabe:** `mpv_abgabedokument.pdf`

---

## Status: Was bereits fertig ist

Das Abgabedokument ist substantiell abgabefertig. Erledigt am 25. April:

- Stern 2025 als 12. Eintrag in F1-Kernliteratur eingefügt (4 S. angenommen).
- F1-Umfang von 110 → 114 S., Seitenbudget-Tabelle Summe von 500 → 504 S.
- F1-Kennzeichnung präzisiert: "FW 1 (KS primär, DG sekundär)".
- Aufzählungs-Layout per `enumitem` so angepasst, dass alle Frage-Labels sauber linksbündig stehen.
- Pauschalaussage zum Seitenbudget um einen Absatz erweitert: amtliche und statistische Hintergrundquellen (BFS, DVS Luzern, PISA-Konsortium) sind explizit aus dem Studienkorpus ausgenommen.
- `OFFEN_VERIFIKATIONEN.md` umstrukturiert: neue Sektion "Priorität A" mit Eintragsfeldern für Fischer 2010, Baum/Schader 2021, Stern 2025.
- Final-Build sauber: 0 Errors, 0 Warnings, 44 Citekeys aufgelöst, 15 Seiten PDF.

---

## Was du noch machen musst

Genau drei Dinge. In dieser Reihenfolge.

### 1. Bibliotheksstunde ZHB Luzern (1–2 h, Mo 27.4. oder Di 28.4.)

Geh in die ZHB und arbeite `OFFEN_VERIFIKATIONEN.md` von oben nach unten ab. Beginne mit den drei Punkten unter "Priorität A". Das sind die Spannen, von denen das Abgabedokument abhängt:

- **A.1 Fischer 2010** im Buholzer-Sammelband: Spanne S. 97–113 bestätigen.
- **A.2 Baum/Schader 2021** im Beltz-Handbuch Begabung: Spanne S. 588–601 bestätigen.
- **A.3 Stern 2025** in *Bildung Schweiz* Heft 3/2025: exakte Seitenspanne notieren (Annahme bisher: 4 S.).

Trage die gefundenen Spannen direkt in die Eintragsfelder in `OFFEN_VERIFIKATIONEN.md` ein. Anschliessend Priorität B (Detail-Punkte 1.1, 1.2, 1.3, 1.5–1.7, 2.1, 2.2) für das Lerndokument.

### 2. Eintragen, falls Verifikation Abweichung ergibt

**Wenn A.1 oder A.2 stimmen** wie angenommen: keine Aktion nötig.

**Wenn A.3 (Stern) andere Seitenzahl als 4 ergibt**, zum Beispiel 3 oder 6 Seiten: zwei Stellen in `mpv_abgabedokument.tex` anpassen.

- Z. 353: `4\,S.` → tatsächliche Seitenzahl.
- Z. 356: `Umfang Frage~1: 114\,Seiten.` → 110 + tatsächliche Stern-Seiten.
- Z. 512: `Frage 1 (FW, KS/DG: Erkennen)   & 114` → gleicher Wert.
- Z. 519: `\textbf{Summe}                  & \textbf{504}` → 400 + neue F1-Summe.
- Z. 525 (im Pauschalaussage-Absatz): `Jede der 504~Seiten` → neue Summe.

Danach `Quellen.bib` Zeile 611–619 (Eintrag `stern2025intelligenz`) um `pages = {...--...}` ergänzen.

### 3. Final-Build und Upload (Fr 1.5.)

Im Workspace-Verzeichnis:

```bash
latexmk -xelatex -interaction=nonstopmode mpv_abgabedokument.tex
```

Erfolgskriterien (in der Konsolenausgabe und in `mpv_abgabedokument.log`):

- Kein "Error" und kein "Undefined".
- "Found 44 citekeys" (oder eine höhere Zahl, falls du noch etwas hinzugefügt hast).
- Output: 15 Seiten PDF.

Danach `mpv_abgabedokument.pdf` einmal ganz durchklicken: Titelseite stimmt, alle fünf Fragen vorhanden, Seitenbudget-Tabelle zeigt die richtige Summe, Stern 2025 steht als letzter Eintrag in der F1-Kernliteratur, Literaturverzeichnis vollständig.

Dann auf Moodle hochladen: **nur** `mpv_abgabedokument.pdf`. Nicht `mpv.pdf` (das ist das interne Lerndokument).

---

## Falls etwas schiefgeht

- **Build bricht ab mit Cite-Error:** Schau im Log nach dem Citekey, prüfe ob er in `Quellen.bib` existiert (Tippfehler), dann nochmal `latexmk` laufen lassen.
- **Bibliotheksstunde fällt aus:** Die Pauschalaussage "Jede der 504 Seiten ist verifiziert gelesen" im Abgabedokument (Z. 522–531) muss dann abgeschwächt oder gestrichen werden, sonst ist sie nicht haltbar. Schreib mir, wenn das passiert — ich passe den Satz dann auf eine schwächere Formulierung an.
- **Stern-Heft nicht in der ZHB:** Stern bleibt mit 4 S. Schätzwert im Korpus, kein Eintrag in `Quellen.bib` `pages`. Im Prüfungsgespräch sagst du auf Nachfrage: "Heft-Seitenangabe ergänze ich nach". Das ist akzeptabel, aber unsauberer.

---

## Was du bewusst NICHT machst

- Kein weiteres Schreiben am Abgabedokument oder am Lerndokument. Inhaltlich ist beides fertig.
- Englische Artikel (Mun, Gubbins, Al-Hroub, Alodat) NICHT in den Korpus aufnehmen — die Korpus-Trennung-Klausel (Z. 294–301) ist ausreichend.
- Lerndokument `mpv.tex` NICHT bereinigen — nicht prüfungsrelevant für die Abgabe, gehört nicht hochgeladen.
- Visualisierungen, mündliche Verdichtung, Drei-Aussagen-Struktur: das sind alles Aufgaben für den Block 1. Mai – 11. Juni und nicht Teil der Abgabe.

---

## Zeitplan-Vorschlag

| Tag | Aufgabe | Dauer |
|---|---|---|
| Mo 27.4. oder Di 28.4. | Bibliotheksstunde ZHB | 1–2 h |
| Direkt danach | ggf. Stern-Seitenzahl in tex und bib eintragen | 10 Min |
| Mi 29.4. oder Do 30.4. | Final-Build, PDF-Sichtkontrolle | 15 Min |
| Fr 1.5. nachmittags | Moodle-Upload `mpv_abgabedokument.pdf` | 5 Min |

Mehr ist nicht zu tun. Viel Erfolg.
