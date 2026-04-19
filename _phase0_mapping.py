"""Phase 0: Mapping PDF -> BibKey.

Liefert eine Tabelle, die der Nutzer zeilenweise bestaetigen kann.
Fuer PDFs, deren Dateiname unklar ist, wird Seite 1 mittels pdftotext
extrahiert und als Kontroll-Snippet mitgegeben.
"""
from __future__ import annotations
import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE          = Path(__file__).resolve().parent
EXTERNAL_LIT  = HERE.parent / "Literatur"
BIB_PATH      = HERE / "Quellen.bib"

# ------------- BibKeys aus .bib einsammeln (mit Metadaten) ----------------
bib_text = BIB_PATH.read_text(encoding="utf-8")
ENTRY_RE = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,(.*?)\n\}\n",
                      re.IGNORECASE | re.DOTALL)
bib_meta = {}
for m in ENTRY_RE.finditer(bib_text):
    key = m.group(2).strip()
    body = m.group(3)
    def f(name, body=body):
        mm = re.search(rf"\b{name}\s*=\s*\{{(.*?)\}}\s*,", body,
                       re.IGNORECASE | re.DOTALL)
        return mm.group(1).strip() if mm else ""
    bib_meta[key] = {
        "author": f("author") or f("editor"),
        "year":   f("year"),
        "title":  f("title"),
    }


# ------------- Manuelles Mapping (anhand Dateinamen offensichtlich) -------
CONFIDENT_MAPPING = {
    "Begabungsförderung und Migrationshintergrund_Dissertation Ulrike Leikhof_Online.pdf":
        ("leikhof2021jugendliche", "Dateiname nennt Leikhof-Dissertation"),
    "Diagnostik bei Migrantinnen und Migranten _ ein Handbuch  1_ Auflage 2018, Göttingen, 2018 -- Hogrefe Verlag GmbH & Co.pdf":
        ("maehler2018diagnostik", "Titel + Jahr 2018 + Hogrefe matcht"),
    "Equitable Identification Practices for.pdf":
        ("alodat2025equitable", "Titel enthaelt 'Equitable Identification'"),
    "Fischer_et_al_2020_Begabungsfoerderung_II.pdf":
        ("fischer2020begabungsfoerderung", "Dateiname Fischer 2020"),
    "Hochbegabung _ Erkennen, Verstehen, Fördern -- Preckel, Franzis; Baudson, Tanja Gabriele -- Verlag C_H_ Beck, München, 2013 -- Verlag C_H_.epub":
        ("preckel2013hochbegabung", "Preckel/Baudson 2013, Beck-Verlag"),
    "Identifying and Serving English Learners in Gifted Education Looking Back and Moving Forward.pdf":
        ("mun2020identifying", "Titel 'Identifying ... English Learners'"),
    "Inhaltsverzeichnis Alle gleich alle unterschiedlich Zum Umgang mit Heterogenität in Schule und Unterricht.pdf":
        ("buholzer2010allegleich", "Buchtitel 'Alle gleich alle unterschiedlich' (NUR Inhaltsverz.)"),
    "Inhaltsverzeichnis Motivation trifft Begabung Begabte Kinder und Jugendliche verstehen und gezielt fördern.pdf":
        ("lehwald2017motivation", "Buchtitel 'Motivation trifft Begabung' (NUR Inhaltsverz.)"),
    "iPEGE_1_web.pdf":
        ("ipege2009professionelle", "iPEGE-Panel"),
    "Migranten mit Potential Dossier MIRAGE def neu.pdf":
        ("stamm2014mirage", "MIRAGE-Dossier Stamm"),
    "Migrationsbewegungen und Bevölkerung mit Migrationshintergrund.pdf":
        ("bfs2022migration", "BFS Migrationsbericht"),
    "PISA2022-DieSchweizimFokus.pdf":
        ("erzinger2023pisa", "PISA 2022 Schweiz"),
    "Promising Practices for Improving Identification of English Learners for.pdf":
        ("gubbins2020promising", "Titel 'Promising Practices ... English Learners'"),
    "Uslucan_-_Vortrag_zu_Begabung_-_Daten_und_Fakten.pdf":
        ("uslucan2012begabung", "Uslucan-Vortrag"),
    "Utility of Psychometric and Dynamic.pdf":
        ("alhroub2021utility", "Al-Hroub Artikel 'Utility of Psychometric'"),
    "vonelternmitmigrationshintergrundlernen.pdf":
        ("kosoroklabhart2021voneltern", "Titel 'von Eltern mit Migrationshintergrund lernen'"),
    "Zur_Bedeutung_der_graphomotorischen_Prozesse_beim_.pdf":
        ("sturm2016graphomotorik", "Titel 'Zur Bedeutung ... graphomotorischen Prozesse'"),
}

# Dateien, bei denen Dateiname nicht eindeutig ist -> Seite 1 extrahieren
UNCLEAR = [
    "Begabte_Migration_Infoblatt_I_Keller_110621.pdf",
    "Begabung _ Eine Einführung -- Gabriele Weigand; Victor Müller-Oppliger; Timo Hoyer -- Bookwire GmbH, Darmstadt, 2013 -- WBG Academic --.pdf",
    "Begabung_ Eine Einführung (Erziehungswissenschaft kompakt) -- Timo Hoyer, Gabriele Weigand, Victor Müller-Oppliger, -- Erziehungswissenschaft kompakt.pdf",
    "Grundwissen Hochbegabung in der Schule -- Behrensen, Solzbacher -- 2016.pdf",
    "HOCHBEGABUNG UND MIGRATIONSHINTERGRUND.pdf",
    "Hochbegabung_k_ein_Problem.pdf",
    "Inklusive Bildung im schulischen Mehrebenensystem_ -- Bianca Preuß (auth_) -- 1_ Auflage 2018, Wiesbaden, 2018 -- VS Verlag für Sozialwisse.pdf",
    "Jenseits der Norm - hochbegabt und hoch sensibel_ (Leben -- Andrea Brackmann.pdf",
    "Reintjes_Kunze_Ossowski_2019_Begabungsfoerderung_und_Professionalisierung.pdf",
]


def first_page_text(pdf_path: Path, pages: str = "1-2") -> str:
    """Extrahiert Seite 1-2 per pdftotext; gibt bereinigten Text zurueck."""
    first, last = pages.split("-")
    with tempfile.NamedTemporaryFile("r", suffix=".txt", delete=False,
                                     encoding="utf-8") as tmp:
        out = tmp.name
    try:
        subprocess.run(
            ["pdftotext", "-f", first, "-l", last, "-layout",
             "-enc", "UTF-8", str(pdf_path), out],
            check=False, capture_output=True, timeout=30,
        )
        text = Path(out).read_text(encoding="utf-8", errors="replace")
    finally:
        Path(out).unlink(missing_ok=True)
    # Mehrfach-Whitespace und lange Leerzeilen zusammenschieben
    text = re.sub(r"\s+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ------------- Ausgabe ----------------------------------------------------
pdfs = sorted(p for p in EXTERNAL_LIT.iterdir()
              if p.is_file() and p.suffix.lower() in (".pdf", ".epub"))

print("=" * 72)
print("SICHERE Zuordnungen (Dateiname eindeutig):")
print("=" * 72)
for p in pdfs:
    if p.name in CONFIDENT_MAPPING:
        key, reason = CONFIDENT_MAPPING[p.name]
        print(f"\n  PDF     : {p.name}")
        print(f"  BibKey  : {key}")
        print(f"  Begrund.: {reason}")

print()
print("=" * 72)
print("UNKLARE Faelle (Seite 1-2 Auszug zur Bestaetigung):")
print("=" * 72)
for p in pdfs:
    if p.name not in UNCLEAR:
        continue
    print(f"\n  PDF: {p.name}")
    print("  ---- Seite 1-2 (Auszug, erste ~1500 Zeichen) ----")
    try:
        text = first_page_text(p)
        print(text[:1500])
    except Exception as exc:
        print(f"  !! Extraktion fehlgeschlagen: {exc}")
    print("  ---- Ende Auszug ----")

print()
print("=" * 72)
print("BibKeys in .bib OHNE beschafftes PDF (nach Priorisierung):")
print("=" * 72)
pdf_bibkeys = {v[0] for v in CONFIDENT_MAPPING.values()}
missing = sorted(set(bib_meta) - pdf_bibkeys)
for k in missing:
    m = bib_meta[k]
    author = re.sub(r"\s*and\s*.*", "", m["author"]).strip()[:30]
    title  = m["title"][:55]
    print(f"  {k:32}  {author:30}  {m['year']:4}  {title}")
