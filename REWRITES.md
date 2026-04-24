# REWRITES.md — Zentrale TeX-Umzitierungs-Tabelle

_Automatisch erzeugt durch `collect_rewrites.py` aus den `<!-- REWRITES-... -->`-Bloecken in `Literatur/*/verified_quotes.md`._

_Nicht manuell editieren — aendern Sie den Rewrite-Block im jeweiligen Dossier und lassen Sie das Skript neu laufen._

## Uebersicht

- **Gesamt:** 13 Rewrites
- ⏳ **pending:** 13
- ✅ **applied:** 0
- ✖ **rejected:** 0

## `mpv.tex`

_13 Rewrite(s)_

| Status | Zeile | Action | Alt → Neu | Begruendung | Quelle |
|---|---:|---|---|---|---|
| ⏳ pending | 449 | add_key | `\parencite{muelleroppliger2021handbuch,trautmann2016einfuehrung,preckel2013hochbegabung}` → `\parencite{muelleroppliger2021handbuch,hoyer2013begabung,trautmann2016einfuehrung,preckel2013hochbegabung}` | Hoyer/Weigand/Mueller-Oppliger 2013, Kap. 5.1.3 (S. 74-75) enthaelt die wortgetreue Aufzaehlung der Multiplen Intelligenzen von Gardner (sprachlich, logisch-mathematisch, visuell-raeumlich, koerperlich-kinaesthetisch etc.), die in mpv.tex L:449 be... | `muelleroppliger2021handbuch` |
| ⏳ pending | 449 | remove_key | `\parencite{muelleroppliger2021handbuch,trautmann2016einfuehrung,preckel2013hochbegabung}` → `\parencite{muelleroppliger2021handbuch,trautmann2016einfuehrung}` | Gardner-Bereichsliste (logisch-mathematisch, raeumlich, koerperlich-kinaesthetisch) wird bei Preckel/Baudson nicht in dieser Form entfaltet. Nur mehrdimensionales Hochbegabungsverstaendnis ist belegt, nicht die Bereichsliste selbst. | `preckel2013hochbegabung` |
| ⏳ pending | 504 | add_key | `\parencite{muelleroppliger2021handbuch}` → `\parencite{muelleroppliger2021handbuch,hoyer2013begabung}` | Hoyer et al. 2013, Kap. 5.1.2 (S. 73-74): Kritik an der "einseitig kognitiven Ausrichtung bisheriger Intelligenztheorien" und Forderung, "weitere 'Intelligenzen' oder Begabungsdomaenen, etwa soziale und emotionale" einzubeziehen. Stuetzt mpv.tex L... | `muelleroppliger2021handbuch` |
| ⏳ pending | 650 | replace_key | `\textcite{preckel2013hochbegabung}` → `\textcite{preckel2021tad}` | Preckel/Baudson 2013 (Beck) behandelt "dynamische Verfahren" nicht (1x "dynamisch" im Buch, Kontext Renzulli). Preckel 2021 (Handbuch Begabung, Kap. "Hochbegabungsdiagnostik: Testauswahl, Durchfuehrung, Interpretation") deckt dynamische/prozessori... | `preckel2013hochbegabung` |
| ⏳ pending | 790 | remove_key | `\parencite{preckel2013hochbegabung}` → `\parencite{maehler2018diagnostik}` | Weder "wiederholte Erhebungen" noch "nonverbale Verfahren" in Preckel/Baudson. maehler2018diagnostik deckt beides wortgetreu (S. 93 wiederholte Ueberpruefung; S. 169/172 nonverbale Intelligenztests). | `preckel2013hochbegabung` |
| ⏳ pending | 800 | add_key | `\parencite{muelleroppliger2021handbuch,fischer2020begabungsfoerderung}` → `\parencite{muelleroppliger2021handbuch,hoyer2013begabung,fischer2020begabungsfoerderung}` | Hoyer et al. 2013, Kap. 7.2 (S. 104-105): Talent Pool fuer 15-20 % "ueber Potenziale verfuegen" ohne formalen Testbefund. Drehtuermodell als flexible Foerderform. Direkter Beleg fuer mpv.tex L:800 ("erweiterte Foerdermoeglichkeiten ... unabhaengig... | `muelleroppliger2021handbuch` |
| ⏳ pending | 874 | add_key | `\parencite{fischer2020begabungsfoerderung,muelleroppliger2021handbuch}` → `\parencite{fischer2020begabungsfoerderung,muelleroppliger2021handbuch,hoyer2013begabung}` | Hoyer et al. 2013, Kap. 7.3 (S. 106-107): Parallel Curriculum "regt Lernende staerkenorientiert an, verschiedene Schluesselkonzepte ... miteinander zu verbinden". Belegt Intis Formulierung, dass Staerken zum Ausgangspunkt fuer Kompetenzentwicklung... | `muelleroppliger2021handbuch` |
| ⏳ pending | 1026 | add_key | `\textcite{muelleroppliger2021handbuch}` → `\textcite{muelleroppliger2021handbuch,hoyer2013begabung}` | Hoyer et al. 2013, Kap. 7.4 (S. 112-113): "Higher Order Thinking Skills (HOTS) not More of the Same (MOTS)" (Rogers 2002, S. 271) + "Taxonomiestufen fuer hoehere Denkfaehigkeiten". Direkter Beleg fuer Intis Paraphrase "Staerken des Denkens" in L:1... | `muelleroppliger2021handbuch` |
| ⏳ pending | 1689 | add_key | `\parencite{muelleroppliger2021handbuch,fischer2020begabungsfoerderung,trautmann2016einfuehrung}` → `\parencite{muelleroppliger2021handbuch,hoyer2013begabung,fischer2020begabungsfoerderung,trautmann2016einfuehrung}` | Hoyer et al. 2013, Kap. 6.6 (S. 95-97 Three Ring Concept) + Kap. 6.7 S. 99 (expliziter Verweis: "Dieser Ansatz der Schluesselerlebnisse oder Schluesselbegegnungen findet seine Entsprechung in den Aktivitaeten zu Type I und Type III des 'Triad Mode... | `muelleroppliger2021handbuch` |
| ⏳ pending | 1755 | replace_key | `\parencite{fischer2020begabungsfoerderung}` → `\parencite{renzullireis2021rls}` | Fischer 2020 (Herausgeberband) entfaltet die drei SEM-Enrichment-Typen nicht (0 Treffer "Typ-I" / "drei Enrichment"). Renzulli/Reis 2021 (Reis Learning System) ist die Originalquelle der Drei-Typen-Taxonomie; Teil6-Transkript verortet die systemat... | `fischer2020begabungsfoerderung` |
| ⏳ pending | 1765 | add_key | `\parencite{muelleroppliger2021handbuch}` → `\parencite{muelleroppliger2021handbuch,hoyer2013begabung}` | Hoyer et al. 2013, Kap. 7.1 (S. 101-103): SEM mit drei Foerdermassnahmen (Compacting, Enrichment, Total Talent Portfolio); Schoolhouse vs. Creative-productive Giftedness. Belegt Intis SEM-Grundgedanke (Typ-III = Projektarbeit im individuellen Inte... | `muelleroppliger2021handbuch` |
| ⏳ pending | 2747 | replace_key | `\parencite{preckel2013hochbegabung,lemas2023begriffsklaerung}` → `\parencite{maehler2018diagnostik,lemas2023begriffsklaerung}` | "prozessorientierte, dynamische Diagnostik" nicht in Preckel/Baudson. maehler S. 320/325/338 belegt "Prozessdiagnostik" wortgetreu als Paraphrase. | `preckel2013hochbegabung` |
| ⏳ pending | 3179 | replace_key | `\parencite{lemas2023begriffsklaerung,preckel2013hochbegabung}` → `\parencite{lemas2023begriffsklaerung,maehler2018diagnostik}` | Gleicher Grund wie L:2747 — Prozessdiagnostik durch maehler belegt, nicht durch Preckel/Baudson. | `preckel2013hochbegabung` |

## Status-Breakdown pro Dossier

| Dossier | pending | applied | rejected | total |
|---|---:|---:|---:|---:|
| `fischer2020begabungsfoerderung` | 1 | 0 | 0 | 1 |
| `muelleroppliger2021handbuch` | 7 | 0 | 0 | 7 |
| `preckel2013hochbegabung` | 5 | 0 | 0 | 5 |
