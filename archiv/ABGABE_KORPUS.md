# Abgabe-Korpus: Single Source of Truth

Die definitive Literatur- und Seitenzaehlung wird nicht mehr aus Excel
zurueckgelesen. Massgeblich sind nur:

1. `mpv.tex`
2. `abgabe_korpus.tex`
3. `Quellen.bib`

`mpv.tex` bindet `abgabe_korpus.tex` als stummen Datenblock ein. Die sichtbare
Seitenbudget-Tabelle wird aus `build/abgabe_seitenbudget.tex` geladen; diese Datei
wird automatisch erzeugt.

## Workflow

Nach jeder Aenderung an einer gezaehlten Quelle:

```bash
python3 abgabe_korpus.py
lualatex -interaction=nonstopmode -halt-on-error mpv.tex
```

Der Generator erzeugt:

- `Abgabe_Quellen.csv`
- `Abgabe_Quellen.xlsx`
- `build/abgabe_seitenbudget.tex`
- `build/abgabe_quellenliste.tex`
- `build/abgabe_korpus_audit.md`

## Korpus-Format

```latex
\AbgabeQuelle{F1}{K}{stamm2021fehlenderblick}{576--585}{10}
\AbgabeQuelle{F3}{S}{kappus2010migration}{67--70}{4}
\AbgabeQuelle{F4}{N}{cast2024udlguidelines}{online}{0}
```

Status:

- `K`: Kernliteratur, gezaehlt
- `S`: gezaehlte Stuetzliteratur
- `N`: nicht gezaehlt

Die letzte Klammer muss eine reine Zahl sein. `N` muss `0` Seiten haben.

## Pruefungen

`abgabe_korpus.py` bricht ab, wenn:

- ein BibTeX-Key aus `abgabe_korpus.tex` nicht in `Quellen.bib` existiert,
- eine Seitenzahl nicht numerisch ist,
- `N`-Eintraege trotzdem Seiten zaehlen,
- gezaehlte Eintraege 0 Seiten haben,
- die `Umfang Frage~...`-Angaben in `mpv.tex` nicht zu den Korpusdaten passen,
- die ausgeschlossenen englischsprachigen Fachartikel versehentlich gezaehlt werden,
- eine bestehende generierte Excel-Datei andere Korpuszeilen enthaelt.

Bei bewusst geaendertem Korpus kann die bestehende Excel-Datei neu geschrieben
werden mit:

```bash
python3 abgabe_korpus.py --force
```

Zusaetzlich kann eine harte Ueberlappungspruefung eingeschaltet werden:

```bash
python3 abgabe_korpus.py --strict-overlap
```

Der aktuelle Korpus enthaelt mehrere fragespezifisch wiederverwendete Quellen; die
Details stehen in `build/abgabe_korpus_audit.md`.
