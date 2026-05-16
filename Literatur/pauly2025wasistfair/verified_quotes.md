# Verifizierte Zitate – `pauly2025wasistfair`

**Quelle:** Pauly, Claudia (Hrsg.) (2025). *Was ist fair? Begabungsgerechtigkeit auf dem Prüfstand.* Frankfurt am Main: Karg-Stiftung. Open Access (CC-Lizenz, pedocs).
**Lokaler Pfad:** `2025_Pauly_Was_ist_fair.pdf` (73 PDF-Seiten).
**Mapping Buchseite → PDF-Index:** PDF[N-1] = Buchseite N (verifiziert anhand der gedruckten Seitenzahlen, z. B. PDF[34] = Buchseite 35).

Dieser Sammelband bedient zwei Bibkeys:

- `baudson2025besserfinden` — Baudson, T. G. (2025). Wie wir Begabte besser finden können. S. 35–40.
- `koop2025herkunft` — Koop, C. (2025). Die Herkunft entscheidet zu oft über die Chancen. S. 64–69.

**Methodik:** PyMuPDF-Extraktion der zitatkritischen Buchseiten, Pass-2-Verifikationslesung gegen alle Zitatstellen in `mpv.tex` und `VISUALISIERUNG/Vortrag1_geschaerft.md`. Extrahierte Buchseiten in `pages_text/buchseite_NNN.txt` (Reproduzierbarkeits-Artefakt).

---

## Audit-Befunde (Korrekturen für `mpv.tex`)

### B1 — Locator-Fehler in `mpv.tex` L:796

```tex
\textcite[S.\,68]{koop2025herkunft} darauf hin, dass
auch nonverbale Testverfahren keine automatische Fairness garantieren
und dass Förderung selbst als diagnostische Gelegenheit gelesen werden
sollte.
```

**Problem:** Der Satz kombiniert zwei Aussagen, die auf zwei verschiedenen Seiten stehen:
- (a) „nonverbale Testverfahren keine automatische Fairness" → **S. 66** (nicht S. 68; siehe Z05).
- (b) „Förderung selbst als diagnostische Gelegenheit" → **S. 68** (siehe Z07).

**Empfohlene Korrektur:** Locator zu `[S.\,66\,f.,\,68]` oder `[S.\,66--68]` ändern, damit beide Aussagen abgedeckt sind.

### B2 — Locator-Bestätigungen

- `mpv.tex` L:4723, L:4727 `\parencite[S.\,66]{koop2025herkunft}` → **korrekt** (Z06: Lehrkräfte-Orientierung an Leistungen + Restkonfundierung sprachfreier Tests).
- `mpv.tex` L:4756 `\parencite[S.\,38--39]{baudson2025besserfinden}` → **korrekt** (Z02–Z04 abgedeckt: Pathologisierung Schwarzer Schüler, twice-exceptional Defizitfokus, „gut funktionierende Hochleister", Investition in diagnostische Kompetenz).

---

## Wortgetreue Zitate

### Baudson 2025 — `baudson2025besserfinden`

#### Z01 — Marburger Hochbegabtenprojekt (S. 36–37)

> „Schon das Marburger Hochbegabtenprojekt konnte zeigen, dass Lehrkräfte Hochbegabte nur dann erkennen, wenn ihre Leistungen erwartungsgemäß ausfallen – hochbegabte Underachiever haben faktisch kaum Chancen, dass ihre Begabung erkannt wird."

**Anker:** S. 36, Z. 39 („Schon das Mar-") + S. 37, Z. 3–5 (Fortsetzung). Seitenwechsel innerhalb des Zitats; Locator `S.\,36--37` korrekt.
**Verwendet in:** `Vortrag1_geschaerft.md` Stein 2 (★ Status 5).

#### Z02 — Pathologisierung intersektional (S. 38)

> „Bestimmte Gruppen werden daher schlechter erkannt und/oder fehldiagnostiziert: Hochbegabte Schwarze Schüler werden beispielsweise eher pathologisiert, als dass ihre Begabung erkannt wird; bei „twice-exceptional"-Schüler:innen liegt der Interventionsfokus deutlich stärker auf den Defiziten als auf der Ressource Hochbegabung."

**Anker:** S. 38, Z. 28–32 (Fazit-Abschnitt).
**Verwendet in:** `mpv.tex` Frage 5 § Baudson-Vertiefung (paraphrasiert).

#### Z03 — „Gut funktionierende Hochleister" (S. 38)

> „Fehleinschätzungen haben Folgen: für die Frage, wer als mutmaßlich hochbegabt erkannt wird (in der Regel die gut funktionierenden Hochleister:innen aus den mittleren und höheren gesellschaftlichen Schichten) und somit überhaupt eine Chance auf Förderung erhält"

**Anker:** S. 38, Z. 33–35.
**Verwendet in:** `mpv.tex` Frage 5 (paraphrasiert: „Kinder, die nicht dem Prototyp des „gut funktionierenden Hochleisters" entsprechen").
**Wortlaut-Hinweis:** Im TeX steht `\enquote{gut funktionierenden Hochleisters}` — singulär; das Original ist Plural „Hochleister:innen". Bei wörtlichem Zitat müsste das `[s]` markiert werden, sonst Plural beibehalten.

#### Z04 — Investition in diagnostische Kompetenz (S. 38–39)

> „Es lohnt sich also, in die diagnostische Kompetenz von Lehrkräften zu investieren: Was sind tatsächlich valide Indikatoren für bestimmte Schüler:innenmerkmale? Was gängige Stereotype? Wie komme ich meinen eigenen Urteilsverzerrungen auf die Spur? Wie bleibe ich trotz allem optimistisch?"

**Anker:** S. 38, Z. 41 + S. 39, Z. 3–4.
**Verwendet in:** `mpv.tex` Frage 5 § Baudson-Vertiefung (paraphrasiert).

### Koop 2025 — `koop2025herkunft`

#### Z05 — Nonverbale Tests können nicht aufheben (S. 66)

> „Nonverbale Tests können den sprachlichen und kulturellen Einfluss auf Testergebnisse also nur eingrenzen, aber nicht gänzlich aufheben."

**Anker:** S. 66, Z. 16–17.
**Verwendet in:** `Vortrag1_geschaerft.md` Stein 1 (★ Status 5; Wortlaut mit `[…]` für „auf Testergebnisse also" korrekt gekürzt).

#### Z06 — Lehrkräfte-Orientierung an Leistungen + Herkunft (S. 66)

> „Lehrkräfte orientieren sich stark an gezeigten Schulleistungen und treffen prognostische Annahmen zur weiteren Entwicklung von Kindern in Abhängigkeit von deren Herkunft."

**Anker:** S. 66, Z. 28–30 (im Kontext: „Stattdessen erfolgt die Auswahl für Förderprogramme vielfach über Empfehlungen durch Lehrkräfte, die sich ohne spezifische Kenntnisse häufig durch falsche Annahmen leiten lassen:").
**Verwendet in:** `mpv.tex` Frage 5 L:4720–4723 (paraphrasiert; Locator `S.\,66` korrekt).

#### Z07 — 15–20 % Schwellenwert + Förderung als Diagnostik (S. 68)

> „Speziell wenn sich die Frage stellt, ob Schüler:innen ihr Leistungspotenzial bisher wegen fehlender Lerngelegenheiten noch nicht ausschöpfen können, sollten Schulen zudem bei der Festlegung von Schwellenwerten für die Zuweisung zu Fördermaßnahmen großzügig sein. So könnten in einem ersten Schritt 15 bis 20 % der Kinder für eine begabungsspezifische Fördermaßnahme ausgewählt werden. Die Fördermaßnahme selbst kann dann diagnostische Erkenntnisse liefern, welche Kinder für weitere Maßnahmen der Begabtenförderung infrage kommen."

**Anker:** S. 68, Z. 3–9 (Schluss-Empfehlung des Beitrags).
**Verwendet in:** `mpv.tex` Frage 5 L:4729–4734 (paraphrasiert; Locator `S.\,68` korrekt). **Prüfungsstrategisch zentraler Befund — wortgetreu zitierbar.**

#### Z08 — Restkonfundierung sprachfreier Tests (S. 66)

> „Beispielsweise stellt eine ungewohnte Leserichtung selbst bei einem „kulturfairen" Matrizentest eine zusätzliche Herausforderung dar. Zudem ist auch das Denken in Symbolsystemen von Sprache und Kultur beeinflusst, etwa wenn abstrakte Dinge Kategorien zugeordnet werden."

**Anker:** S. 66, Z. 17–21.
**Verwendet in:** `mpv.tex` Frage 5 L:4724–4727 (paraphrasiert: „Ungewohnte Leserichtungen, fehlende Vertrautheit mit Symbolsystemen und kulturell geprägte Denkgewohnheiten beeinflussen die Testergebnisse"; Locator `S.\,66` korrekt).

---

## Audit-Status

**Status:** **5** (selektiv für alle in `mpv.tex` und Vortrag 1 zitierten Stellen).
**Verifiziert am:** 2026-05-16
**Bearbeitet durch:** Cascade / Inti
**Audit-Methode:** PyMuPDF-Volltextextraktion + Pass-2-Verifikationslesung der Buchseiten 35–40 (Baudson) und 64–68 (Koop).
