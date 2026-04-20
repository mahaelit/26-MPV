#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
onboard_kandidaten.py - Nimmt die 4 externen Zusatz-Quellen in die Infrastruktur auf:
- Quellen.bib: haengt BibTeX-Eintraege an (idempotent)
- Literatur/<key>/source.pdf: kopiert PDF aus externem Ordner
- Literatur/<key>/verified_quotes.md: Stub im Standardformat

Nach Ausfuehrung sollten noch laufen:
  python extract_excerpts.py
  python cite_context.py
  python build_inventar.py
  python build_index.py
  python build_kompendium.py
"""
from __future__ import annotations
import shutil
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIT_26MPV = HERE / "Literatur"
LIT_EXTERN = HERE.parent / "Literatur"
BIB = HERE / "Quellen.bib"

# Format: (bibkey, externer_dateiname, bibtex_entry, verified_quotes_header)
KANDIDATEN = [
    (
        "behrensen2016grundwissen",
        "Grundwissen Hochbegabung in der Schule -- Behrensen, Solzbacher -- 2016.pdf",
        """
@book{behrensen2016grundwissen,
  author    = {Behrensen, Birgit and Solzbacher, Claudia},
  title     = {Grundwissen {Hochbegabung} in der {Schule}: {Theorie} und {Praxis}},
  year      = {2016},
  publisher = {Beltz},
  address   = {Weinheim und Basel},
  annotation = {Zusatz-Quelle aus MPV/Literatur. 177\\,S. Potentieller Ersatz fuer ROT-Stellen zu Diagnostik und schulischer Foerderung.},
}
""".strip(),
        {
            "authors": "Behrensen, Birgit; Solzbacher, Claudia",
            "year": "2016",
            "title_full": "Grundwissen Hochbegabung in der Schule. Theorie und Praxis",
        },
    ),
    (
        "preuss2018inklusive",
        "Inklusive Bildung im schulischen Mehrebenensystem_ -- Bianca Preuß (auth_) -- 1_ Auflage 2018, Wiesbaden, 2018 -- VS Verlag für Sozialwisse.pdf",
        """
@book{preuss2018inklusive,
  author    = {Preuß, Bianca},
  title     = {Inklusive {Bildung} im schulischen {Mehrebenensystem}: {Behinderung}, {Flüchtlinge}, {Migration} und {Begabung}},
  year      = {2018},
  publisher = {Springer VS},
  address   = {Wiesbaden},
  annotation = {Zusatz-Quelle aus MPV/Literatur. 164\\,S. Integriert Diskurs zu Inklusion, Migration und Begabung im Mehrebenenmodell der Schule.},
}
""".strip(),
        {
            "authors": "Preuß, Bianca",
            "year": "2018",
            "title_full": "Inklusive Bildung im schulischen Mehrebenensystem. Behinderung, Flüchtlinge, Migration und Begabung",
        },
    ),
    (
        "brackmann2013jenseits",
        "Jenseits der Norm - hochbegabt und hoch sensibel_ (Leben -- Andrea Brackmann.pdf",
        """
@book{brackmann2013jenseits,
  author    = {Brackmann, Andrea},
  title     = {Jenseits der {Norm} -- hochbegabt und hoch sensibel? {Die} seelischen und sozialen {Aspekte} der {Hochbegabung} bei {Kindern} und {Erwachsenen}},
  year      = {2013},
  publisher = {Klett-Cotta},
  address   = {Stuttgart},
  series    = {Leben Lernen},
  annotation = {Zusatz-Quelle aus MPV/Literatur. 237\\,S. Hochsensibilitaet, emotionale/sensorische Besonderheiten Hochbegabter.},
}
""".strip(),
        {
            "authors": "Brackmann, Andrea",
            "year": "2013",
            "title_full": "Jenseits der Norm – hochbegabt und hoch sensibel? Die seelischen und sozialen Aspekte der Hochbegabung bei Kindern und Erwachsenen",
        },
    ),
    (
        "reintjes2019begabungsfoerderung",
        "Reintjes_Kunze_Ossowski_2019_Begabungsfoerderung_und_Professionalisierung.pdf",
        """
@book{reintjes2019begabungsfoerderung,
  editor    = {Reintjes, Christian and Kunze, Ingrid and Ossowski, Ekkehard},
  title     = {Begabungsförderung und {Professionalisierung}: {Befunde}, {Perspektiven}, {Herausforderungen}},
  year      = {2019},
  publisher = {Klinkhardt},
  address   = {Bad Heilbrunn},
  annotation = {Zusatz-Quelle aus MPV/Literatur. 231\\,S. Sammelband zu Professionalisierung von Lehrpersonen in der Begabungsfoerderung.},
}
""".strip(),
        {
            "authors": "Reintjes, Christian; Kunze, Ingrid; Ossowski, Ekkehard (Hrsg.)",
            "year": "2019",
            "title_full": "Begabungsförderung und Professionalisierung. Befunde, Perspektiven, Herausforderungen",
        },
    ),
]

VQ_TEMPLATE = """# Verifizierte Zitate – {key}

**Quelle:** {authors} ({year}). {title_full}.
**Swisscovery/Verifikationslink:** https://swisscovery.slsp.ch/discovery/search?query=any,contains,{search_query}&tab=41SLSP_NETWORK&search_scope=DN_and_CI&vid=41SLSP_NETWORK:VU1_UNION&offset=0
**Identifikator:** –
**Lokaler Pfad:** `source.pdf`

---


## Zitate (gegen die Quelle gegengeprueft)

### Zitat 1 (S. XX)

> „Wortgetreues Zitat hier einfuegen."

**Kontext / Paraphrase:**
<eigene Zusammenfassung in 1-2 Saetzen>

**Verwendet in:**
- Lerndokument: §<Abschnitt>
- Abgabedokument: §<Abschnitt>

---

**Status:** 0 (ungeprueft)
**Verifiziert am:** <YYYY-MM-DD>
**Bearbeitet durch:** Inti Merolli
"""


def _find_external_file(fname: str) -> Path | None:
    """Finde Datei im externen Ordner mit NFC/NFD-Toleranz."""
    fname_nfc = unicodedata.normalize("NFC", fname)
    for p in LIT_EXTERN.iterdir():
        if unicodedata.normalize("NFC", p.name) == fname_nfc:
            return p
    return None


def _is_bibkey_in_bib(bibkey: str) -> bool:
    text = BIB.read_text(encoding="utf-8")
    return f"@book{{{bibkey}," in text or f"@article{{{bibkey}," in text or f"@{{{bibkey}," in text


def _append_to_bib(entry: str) -> None:
    current = BIB.read_text(encoding="utf-8")
    # Sicherstellen, dass mit Newline getrennt
    if not current.endswith("\n"):
        current += "\n"
    BIB.write_text(current + "\n" + entry + "\n", encoding="utf-8")


def _urlencode_minimal(s: str) -> str:
    import urllib.parse
    return urllib.parse.quote(s, safe="")


def main() -> int:
    print("onboard_kandidaten.py")
    if not LIT_EXTERN.exists():
        print(f"  ERR: Externer Ordner fehlt: {LIT_EXTERN}")
        return 2
    added = 0
    skipped = 0
    for key, ext_fname, bib_entry, meta in KANDIDATEN:
        print(f"\n-- {key} --")
        # 1. BibTeX-Eintrag
        if _is_bibkey_in_bib(key):
            print(f"  bib   : schon vorhanden")
        else:
            _append_to_bib(bib_entry)
            print(f"  bib   : hinzugefuegt")

        # 2. PDF kopieren
        target_dir = LIT_26MPV / key
        target_dir.mkdir(parents=True, exist_ok=True)
        target_pdf = target_dir / "source.pdf"
        if target_pdf.exists():
            print(f"  pdf   : schon vorhanden")
        else:
            ext_path = _find_external_file(ext_fname)
            if not ext_path:
                print(f"  pdf   : FEHLER - externe Datei nicht gefunden: {ext_fname}")
                skipped += 1
                continue
            shutil.copy2(ext_path, target_pdf)
            print(f"  pdf   : kopiert ({target_pdf.stat().st_size // 1024} KB)")

        # 3. verified_quotes.md
        vq = target_dir / "verified_quotes.md"
        if vq.exists():
            print(f"  vq    : schon vorhanden")
        else:
            search_query = _urlencode_minimal(f"{meta['authors']} {meta['title_full']}")
            vq.write_text(
                VQ_TEMPLATE.format(
                    key=key,
                    authors=meta["authors"],
                    year=meta["year"],
                    title_full=meta["title_full"],
                    search_query=search_query,
                ),
                encoding="utf-8",
            )
            print(f"  vq    : Stub erstellt")
        added += 1

    print(f"\nAbgeschlossen. Onboarded: {added}, Skipped: {skipped}")
    print("Naechste Schritte:")
    print("  python extract_excerpts.py      # Kapitel-Splits")
    print("  python cite_context.py          # CLAIMS-Block in verified_quotes")
    print("  python build_inventar.py        # Inventar aktualisieren")
    print("  python build_index.py           # Index aktualisieren")
    print("  python build_kompendium.py      # Pruefungskompendium")
    return 0


if __name__ == "__main__":
    sys.exit(main())
