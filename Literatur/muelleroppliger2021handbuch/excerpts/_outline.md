# Volltext-Transkripte: `muelleroppliger2021handbuch`

Quelle: Müller-Oppliger, Victor & Weigand, Gabriele (Hrsg., 2021). *Handbuch Begabung.* Weinheim und Basel: Beltz. ISBN 978-3-407-25806-9, 608 Seiten.

## Art des Volltexts

**Textbasierte Transkripte**, nicht Foto-Scans. Inti (oder ein Transkriptionswerkzeug) hat das komplette Handbuch als acht Markdown-Dateien aufbereitet -- eine pro Buchteil. Die Transkripte sind **volltextsuchbar** und decken alle acht Teile des Handbuchs ab. Gesamtumfang: ca. 1,0 MB Text.

## Dateiübersicht

| # | Datei | Buchseiten (ca.) | Größe | Enthaltene Beiträge (BibKeys im Repo) |
|---:|---|---|---:|---|
| 1 | [`teil1_begabung_bildung_gesellschaft.md`](teil1_begabung_bildung_gesellschaft.md) | S. 32--102 | 261 KB | `muelleroppliger2021plurale` (S. 32--45), `weigand2021person` (S. 46--64), `sedmak2021bildungsgerechtigkeit` (S. 65--76), `horvath2021elite` (S. 77--87), `wollersheim2021konstrukt` (S. 88--102) |
| 2 | [`teil2_begabung_und_begabungsfoerderung_konzepte_modelle.md`](teil2_begabung_und_begabungsfoerderung_konzepte_modelle.md) | S. 104--221 | 180 KB | Ziegler/Stern (S. 104--113), `baudson2021wasdenken` (S. 115--131), `stadelmann2021begabungsentwicklung` (S. 133--147), `grabnermeier2021expertise` (S. 149--167), `urban2021kreativitaet` (S. 168--183), Kuhl (S. 185--203), Müller-Oppliger Begabungsmodelle (S. 204--221) |
| 3 | [`teil3_begabungen_erkennen.md`](teil3_begabungen_erkennen.md) | S. 224--289 | 131 KB | `muelleroppliger2021paeddiagnostik` (S. 224--238), `gauckreimann2021psychdiagnostik` (S. 239--251), `stahl2021mbet` (S. 252--258), `koopseddig2021frueheserkennen` (S. 260--273), `preckel2021tad` (S. 274--303) |
| 4 | [`teil4_begabende_schule.md`](teil4_begabende_schule.md) | S. 290--373 | 178 KB | `weigand2021separativ` (S. 290--301), Anderegg/Wilhelm (S. 302--318), Vock (S. 319--332), Reis/Renzulli/Müller-Oppliger SEM (S. 333--347), Nguyen/Sliwka (S. 348--358), Fischer/Müller-Oppliger (S. 359--373) |
| 5 | [`teil5_begabender_unterricht.md`](teil5_begabender_unterricht.md) | S. 374--442 | 132 KB | Müller-Oppliger Lernarchitekturen (S. 374--389), Stöger/Balestrini/Ziegler (S. 390--401), Fischer et al. Lernstrategien (S. 402--417), Wagner (S. 418--426), Müller-Oppliger Leistungsbeurteilung (S. 427--442) |
| 6 | [`teil6_begabende_unterstuetzungssysteme.md`](teil6_begabende_unterstuetzungssysteme.md) | S. 444--497 | 26 KB | `renzullireis2021rls` (S. 444--454), Stumpf (S. 455--467), Miceli/Steenbuck (S. 468--479), Schenk (S. 480--497) |
| 7 | [`teil7_begabte_begleiten.md`](teil7_begabte_begleiten.md) | S. 496--545 | 28 KB | `trautmann2021haltung` (S. 496--510), Arnold/Großgasteiger (S. 511--527), Ziegler et al. Mentoring (S. 528--545) |
| 8 | [`teil8_dysfunktionale_begabungsentwicklung.md`](teil8_dysfunktionale_begabungsentwicklung.md) | S. 546--601 | 121 KB | Greiten (S. 546--555), Gyseler (S. 556--563), Kempter (S. 564--575), `stamm2021fehlenderblick` (S. 576--587), Baum/Schader 2e (S. 588--601) |

**Gesamt:** 1,0 MB Textmaterial, deckt das **komplette Handbuch** (608 Seiten, 8 Teile, 33 Beiträge) ab.

## Verortungsdaten

Der Unterordner [`einordnung/`](einordnung/) enthält strukturelle JSON-Zuordnungen, die Zitat- und Verortungsstellen im Lerndokument mit den Handbuch-Teilen verknüpfen:

- `Teil1_Verortung_Transkripte_HandbuchBegabung.json` (56 KB)
- `Teil2_verortung_transkripte.json` (48 KB)
- `Teil3_Verortung_Teil3_BegabungenErkennen.json` (55 KB)
- `Teil4_Transkript_Verortung_Handbuch_Begabung.json` (49 KB)
- `Teil5_verortung_lerndokument.json` (301 KB) -- verknüpft Lerndokument-Cite-Stellen mit Handbuch-Textstellen
- `Teil6_Verortung_Transkript_Teil6_Renzulli_Reis.json` (43 KB)
- `Teil7_trautmann_verortung.json` (42 KB)
- `Teil8_lerndokument_struktur.json` (144 KB)
- `Transkript_Verortung_Lerndokument_schema.json` (7 KB) -- Schema-Definition
- `Transkript_Verortung_Lerndokument_strukturiert.json` (149 KB)

Diese JSONs werden von `analyze_transkripte.py` und `integrate_transkripte.py` genutzt, um Transkript-Positionen mit BibKey-Cite-Stellen zu verknüpfen.

## Verwendung in der MPV

`muelleroppliger2021handbuch` ist mit **14 Cite-Stellen** (10 Lerndokument, 4 Abgabedokument) die meistzitierte Sekundärquelle der Arbeit. Mit den Transkripten wird sie:

- **Volltextsuchbar** für die Open-Book-Prüfung (einfache `Grep`-Suche über alle Teile)
- **Präzise zitierbar** -- die Transkripte enthalten Seitenangaben pro Kapitel (z.\,B. "S. 32-34 (S. 10)")
- **Strukturell erschlossen** -- die `einordnung/`-JSONs geben an, welche Lerndokument-Stelle welchem Handbuch-Beitrag entspricht

Dies löst den vormals ROT-markierten Status (`muelleroppliger2021handbuch: Cites=14, vq=2, vorher keine Volltext-Verfügbarkeit`) zu **GELB+**: Volltext-Transkripte + Inhalts-Verortung vorhanden, aber `verified_quotes.md` noch nicht auf Status 3.

## Nächste Schritte

1. `verified_quotes.md` auf Basis der Transkripte verifizieren (Phase 3).
2. Optional: Original-PDF des Handbuchs (Beltz, 608 S.) beschaffen, falls exakte Zitate nicht aus den Transkripten extrahierbar sind.
3. Die einzelnen `@incollection`-Einträge (baudson, stadelmann, grabner/meier, etc.) haben jeweils Zugriff auf ihre spezifische Kapitel-Stelle über das entsprechende Transkript-Teil.
