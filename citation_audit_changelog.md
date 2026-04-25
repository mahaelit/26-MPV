# Citation Audit Changelog for `mpv.tex`

Date: 2026-04-25

## Scope

- Audited `mpv.tex` for plain-text author mentions, missing locator data,
  redundant double citations, combined citations without individual locators,
  invalid `\f` markers, and obvious LaTeX syntax artifacts.
- Read `Quellen.bib`, local `verified_quotes.md` files, `excerpts/_outline.md`
  files, and available `source.pdf` files with PyMuPDF where exact page
  verification was possible.
- Left `Quellen.bib`, `Literatur/*/source.pdf`, and `Literatur/*/excerpts/*`
  unchanged.

## Plain-Text Authors Converted to BibLaTeX

- Converted `Maehler et al.`, `Stamm`, and `Keller-Koller` in the diagnostic
  framing of Frage 1 to `\textcite` with available locators.
- Converted repeated plain-text references to Rosebrock/Nix, Gold, Sturm,
  Hurschler, Lehwald, Fischer, Grossrieder, Kuhl, Behrensen, Booth,
  Sedmak, Weigand, Buholzer/Kummer Wyss, Kosorok Labhart/Schoellhorn/
  Luginbuehl, Macha, Kappus, Burow, Webb, Al-Hroub, Alodat, Mun, and
  Gubbins where they introduced source-backed claims.
- Replaced follow-up duplicate author mentions after an initial `\textcite`
  with pronouns where appropriate, for example Webb and Burow passages.
- Kept author names in section headings and formal bibliographic quote blocks
  unchanged because they function as titles/metadata rather than in-text
  source claims.

## Locators Added or Improved

- `preckel2013hochbegabung`: added S. 3--4 and S. 4 for potential/performance
  and twice-exceptionality masking claims.
- `preckel2021tad`: added S. 274--303 for dynamic assessment claims, replacing
  weaker Preckel/Baudson references where the dynamic-diagnostics claim needed
  a better source.
- `maehler2018diagnostik`: added S. 93 and S. 169--172 for language- and
  culture-fair diagnostics; added S. 320, 325, 338 for dynamic diagnostics
  claims where used as a locator-bearing companion to LemaS.
- `stamm2021fehlenderblick`: added S. 576--585 for "begabte Minoritaeten" and
  under-identification claims.
- `kellerkoller2021hellekoepfe`: added S. 76--78 for migration plus
  underachievement masking claims.
- `fischer2020begabungsfoerderung`: added S. 14, 17, 36 for the Munich model,
  S. 242--253 for underachievement, and S. 254--273 for enrichment.
- `hoyer2013begabung`: added as a locator-bearing companion where the 2021
  handbook claim was not directly available: S. 74--75, S. 95--103,
  S. 101--105, and S. 112--113.
- `trautmann2016einfuehrung`: added S. 34--41 or Kap. 1--2 where full page
  verification was not available but the chapter location was supported.
- `gauckreimann2021psychdiagnostik`: added S. 239--251.
- `baumschader2021twice`: added S. 588--601 and removed the redundant trailing
  citation.
- `nottbusch2017graphomotorik`: added S. 125--138.
- `hurschler2020handschriftbeurteilung`: added S. 3 and S. 11.
- `sturm2016graphomotorik`: added S. 2--4.
- `rosebrock2010grundlagen` and `gold2018lesenkannmanlernen`: added Kap. 1--4
  where exact pages could not be verified from the local source state.
- `grossrieder2010anerkennung`: added S. 87--94.
- `kuhl2019diversitaet`: added S. 35--57.
- `behrensen2019inklusive`: added S. 86--98.
- `macha2019gender`: added S. 161 and S. 163\psq.
- `kappus2010migration`: added S. 63--77.
- `leikhof2021jugendliche`: added S. 7--9, S. 105--184, S. 143--184, and
  S. 185--194 depending on the claim context.
- `kosoroklabhart2021voneltern`: added S. 14--19 for professional interpreting
  and culture mediation.
- `buholzer2010allegleich`: added S. 151--161 for cooperative teaching where
  the local table of contents supported the chapter location.
- `mun2020identifying`: added S. 302--304 for review method and S. 325 for
  programme-evaluation conclusions.
- `gubbins2020promising`: added S. 9--13 and S. 23 for study method/themes,
  and S. 23--31 for the four-practice model.
- `alhroub2021utility`: added S. 5--6 for visual/auditory perception findings.
- `alodat2025equitable`: added S. 10 and S. 12 for refugee-specific
  identification constraints.
- `webb2020doppeldiagnosen`: added S. 87--94.

## Combined and Redundant Citations

- Split combined citations where different sources supported different
  aspects, especially in the Gardner/Munich-model/enrichment passages.
- Removed redundant final `\parencite` instances where a preceding `\textcite`
  already carried the same claim and source.
- Replaced weak combined references to broad handbooks with paired citations:
  the handbook key remains where useful, while a locator-bearing companion
  source carries the precise claim.

## Verification Limits

- No page numbers were invented. Where only a table of contents, transcript
  mapping, online source, institutional document, or incomplete preview was
  locally available, the citation was left broad or moved to a chapter-level
  locator.
- Remaining no-locator citations are mostly literature-list labels,
  institutional/web sources, broad overview references, or sources whose local
  full text is unavailable.
- Verified that no invalid `\f` command remains; only `\psq`/`\psqq` are used
  for following-page locators.
