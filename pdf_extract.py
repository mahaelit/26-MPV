"""pdf_extract.py - Phase 1c: seitengenaue Textextraktion fuer Zitatpruefung

Wrapper um drei Text-Engines:
  * Poppler `pdftotext -layout`   (layout-treu, erhaelt Spalten; PDF)
  * `pypdf`                       (Python-Extraktion, Fallback; PDF)
  * `epub` (stdlib only)          (ZIP + HTML-Parser fuer EPUBs; pseudo-Seiten
                                   entsprechen den XHTML-Kapiteln in Spine-Reihenfolge)

Alle Engines liefern eine Liste von Texten pro Seite. Das Skript bietet drei Modi:

  1. DUMP     -  ganze Seite(n) auf stdout oder in Datei
  2. SEARCH   -  Fuzzy-/Exact-Suche nach einer Phrase, mit Seitennummer +
                 kurzem Kontext-Snippet und Markierung der Fundstelle
  3. LIST     -  nur Seitenzahlen + Laenge pro Engine (Sanity-Check)

Die Extraktion wird gecacht unter
`Literatur/<bibkey>/.extracted/<engine>.txt` (0x0C als Seitentrenner).
Ein Re-Lauf ist schnell und liefert reproduzierbar das gleiche Ergebnis.

Beispiele
---------
  # gesamten Text nach pypdf ausgeben, Seite 42:
  python pdf_extract.py preckel2013hochbegabung --page 42

  # Seitenbereich mit Poppler:
  python pdf_extract.py preckel2013hochbegabung -p 10-20 --engine poppler

  # nach Phrase suchen (beide Engines, Fuzzy-Whitespace):
  python pdf_extract.py preckel2013hochbegabung -s "Twice Exceptional"

  # Uebersicht ueber Seitenzahlen beider Engines:
  python pdf_extract.py preckel2013hochbegabung --list

Voraussetzungen
---------------
  * Poppler:  `pdftotext` in PATH (choco install poppler).
  * pypdf  :  `pip install pypdf`.
Fehlt eine Engine, wird sie uebersprungen (Warnung + Exit-Code bleibt 0,
solange mindestens eine Engine geliefert hat).
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


HERE      = Path(__file__).resolve().parent
LITERATUR = HERE / "Literatur"
PAGE_SEP  = "\x0c"   # Form Feed - Standard-Seitentrenner fuer pdftotext


# ----- Engines ----------------------------------------------------------
@dataclass
class Engine:
    name: str
    available: bool
    reason: str = ""


def _check_pdftotext() -> Engine:
    path = shutil.which("pdftotext")
    if not path:
        return Engine("poppler", False,
                      "pdftotext nicht im PATH (Poppler installieren).")
    return Engine("poppler", True)


def _check_pypdf() -> Engine:
    try:
        import pypdf  # noqa: F401
    except ImportError as exc:
        return Engine("pypdf", False, f"pypdf nicht importierbar ({exc}).")
    return Engine("pypdf", True)


def extract_with_pdftotext(pdf: Path) -> list[str]:
    """Ruft `pdftotext -layout -enc UTF-8 pdf -` und splittet in Seiten."""
    try:
        proc = subprocess.run(
            ["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), "-"],
            check=True, capture_output=True, text=True, encoding="utf-8",
            errors="replace",
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise RuntimeError(f"pdftotext schlug fehl: {exc}") from exc
    pages = proc.stdout.split(PAGE_SEP)
    # pdftotext haengt oft einen leeren Trailer-String an - entfernen.
    if pages and pages[-1] == "":
        pages = pages[:-1]
    return pages


def extract_with_pypdf(pdf: Path) -> list[str]:
    from pypdf import PdfReader
    reader = PdfReader(str(pdf))
    pages: list[str] = []
    for i, page in enumerate(reader.pages, start=1):
        try:
            pages.append(page.extract_text() or "")
        except Exception as exc:  # pragma: no cover - Layout-Edge-Cases
            pages.append(f"[pypdf-Fehler auf Seite {i}: {exc}]")
    return pages


# ----- EPUB-Extraktion (stdlib only) -----------------------------------
def _epub_spine_order(zf) -> list[str]:
    """Liefert die XHTML-Dateien in Spine-Reihenfolge (Lese-Reihenfolge).

    Faellt bei fehlender/unvollstaendiger OPF auf eine alphabetische
    Sortierung aller *.xhtml / *.html-Eintraege zurueck.
    """
    import posixpath
    import re as _re
    try:
        container = zf.read("META-INF/container.xml").decode("utf-8", "replace")
        m = _re.search(r'full-path="([^"]+)"', container)
        if not m:
            raise KeyError
        opf_path = m.group(1)
        opf      = zf.read(opf_path).decode("utf-8", "replace")
        opf_dir  = posixpath.dirname(opf_path)
        # manifest: id -> href
        manifest = dict(_re.findall(
            r'<item\b[^>]*\bid="([^"]+)"[^>]*\bhref="([^"]+)"', opf,
        ))
        # spine: itemref in order
        spine_ids = _re.findall(r'<itemref\b[^>]*\bidref="([^"]+)"', opf)
        ordered   = []
        for sid in spine_ids:
            href = manifest.get(sid)
            if href:
                full = posixpath.normpath(posixpath.join(opf_dir, href))
                ordered.append(full)
        # Filtere auf Dateien, die wirklich im ZIP existieren
        names  = set(zf.namelist())
        result = [n for n in ordered if n in names]
        if result:
            return result
    except Exception:
        pass
    # Fallback: alphabetisch
    return sorted(n for n in zf.namelist()
                  if n.lower().endswith((".xhtml", ".html", ".htm")))


def extract_with_epub(src: Path) -> list[str]:
    """Extrahiert Text aus einem EPUB. Pseudo-Seiten == Spine-Dokumente."""
    import zipfile
    from html.parser import HTMLParser

    class _HtmlToText(HTMLParser):
        BLOCKS = {
            "p", "div", "h1", "h2", "h3", "h4", "h5", "h6",
            "li", "tr", "br", "section", "article", "blockquote",
        }
        SKIP_TAGS = {"script", "style", "head"}

        def __init__(self) -> None:
            super().__init__(convert_charrefs=True)
            self.buf: list[str] = []
            self._skip = 0

        def handle_starttag(self, tag, attrs):
            if tag in self.SKIP_TAGS:
                self._skip += 1

        def handle_endtag(self, tag):
            if tag in self.SKIP_TAGS and self._skip > 0:
                self._skip -= 1
            if tag in self.BLOCKS:
                self.buf.append("\n")

        def handle_startendtag(self, tag, attrs):
            if tag in self.BLOCKS:
                self.buf.append("\n")

        def handle_data(self, data):
            if not self._skip:
                self.buf.append(data)

        def text(self) -> str:
            return "".join(self.buf)

    pages: list[str] = []
    with zipfile.ZipFile(src) as zf:
        for name in _epub_spine_order(zf):
            raw = zf.read(name).decode("utf-8", "replace")
            parser = _HtmlToText()
            parser.feed(raw)
            text = parser.text()
            # Whitespace einstampfen, ohne inhaltliche Absaetze zu verlieren.
            text = re.sub(r"[ \t]+", " ", text)
            text = re.sub(r"\n{3,}", "\n\n", text)
            pages.append(text.strip())
    # Leere Kapitel (z. B. reine Bild-XHTMLs) entfernen - sie verzerren nur die Seitennummerierung.
    pages = [p for p in pages if p]
    return pages


# ----- Cache ------------------------------------------------------------
def _cache_path(bibkey: str, engine: str) -> Path:
    return LITERATUR / bibkey / ".extracted" / f"{engine}.txt"


def _load_cache(path: Path, source: Path) -> list[str] | None:
    if not path.is_file():
        return None
    if path.stat().st_mtime < source.stat().st_mtime:
        return None  # Cache ist aelter als die PDF -> neu extrahieren.
    text = path.read_text(encoding="utf-8")
    pages = text.split(PAGE_SEP)
    if pages and pages[-1] == "":
        pages = pages[:-1]
    return pages


def _save_cache(path: Path, pages: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(PAGE_SEP.join(pages), encoding="utf-8")


def get_pages(bibkey: str, src: Path, engine: str) -> list[str]:
    """Liefert Seitenliste fuer eine Engine; nutzt Disk-Cache."""
    cache = _cache_path(bibkey, engine)
    cached = _load_cache(cache, src)
    if cached is not None:
        return cached
    if engine == "poppler":
        pages = extract_with_pdftotext(src)
    elif engine == "pypdf":
        pages = extract_with_pypdf(src)
    elif engine == "epub":
        pages = extract_with_epub(src)
    else:
        raise ValueError(f"Unbekannte Engine: {engine}")
    _save_cache(cache, pages)
    return pages


# ----- Suche ------------------------------------------------------------
_WS_RE = re.compile(r"\s+")


def _fuzzy_regex(query: str) -> re.Pattern:
    """Erzeugt ein Regex, das Whitespace / Zeilenumbrueche zwischen Woertern
    toleriert. Auch weiche Bindestriche (U+00AD) und Silbentrennung am
    Zeilenende werden grosszuegig ignoriert.
    """
    tokens = [re.escape(tok) for tok in query.split() if tok]
    if not tokens:
        raise ValueError("Leere Suchanfrage.")
    # Zwischen den Tokens: beliebiges Whitespace ODER Trennstrich+Whitespace
    between = r"(?:[-\u00AD]?\s+)"
    return re.compile(between.join(tokens), re.IGNORECASE)


def search_pages(pages: list[str], query: str, ctx: int = 80) -> list[tuple[int, str]]:
    rx = _fuzzy_regex(query)
    hits: list[tuple[int, str]] = []
    for i, page in enumerate(pages, start=1):
        for m in rx.finditer(page):
            a = max(0, m.start() - ctx)
            b = min(len(page), m.end() + ctx)
            snippet = _WS_RE.sub(" ", page[a:b]).strip()
            # Markiere den Treffer im Snippet durch **...**
            local_rx = _fuzzy_regex(query)
            snippet  = local_rx.sub(lambda mo: f"**{mo.group(0)}**", snippet, count=1)
            hits.append((i, snippet))
    return hits


# ----- CLI --------------------------------------------------------------
def _parse_pages(spec: str | None, total: int) -> list[int]:
    if not spec:
        return list(range(1, total + 1))
    out: set[int] = set()
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            lo, hi = chunk.split("-", 1)
            out.update(range(int(lo), int(hi) + 1))
        else:
            out.add(int(chunk))
    return sorted(p for p in out if 1 <= p <= total)


def _find_source_pdf(bibkey: str, override: str | None = None) -> Path:
    """Findet die Quelldatei unter Literatur/<bibkey>/.

    Bei *override* wird exakt diese Datei verwendet (relativ oder absolut).

    Prioritaets-Reihenfolge (ohne Override):
        1. source_foxit.pdf   - manuell mit Foxit re-gedruckt, i. d. R. qualitativ besser
        2. source_ocr.pdf     - nachtraeglich per OCR erstellt
        3. source.pdf         - Original
        4. source.epub        - EPUB-Fallback
        5. irgendeine *.pdf / *.epub im Ordner

    Damit wird ein neu beschafftes Foxit- oder OCR-PDF automatisch verwendet,
    ohne dass `source.pdf` ueberschrieben werden muss.
    """
    folder = LITERATUR / bibkey
    if not folder.is_dir():
        raise SystemExit(f"[Fehler] Ordner nicht gefunden: {folder}")

    if override:
        candidate = Path(override)
        if not candidate.is_absolute():
            candidate = folder / candidate
        if not candidate.is_file():
            raise SystemExit(f"[Fehler] --source-Datei nicht gefunden: {candidate}")
        return candidate

    preferred = ("source_foxit.pdf", "source_ocr.pdf", "source.pdf", "source.epub")
    for name in preferred:
        p = folder / name
        if p.is_file():
            return p
    for ext in ("*.pdf", "*.epub"):
        found = sorted(folder.glob(ext))
        if found:
            return found[0]
    raise SystemExit(f"[Fehler] Keine PDF/EPUB in {folder} gefunden.")


def _select_engines(src: Path, choice: str) -> list[Engine]:
    """Waehlt die zulaessigen Engines passend zum Dateiformat.

    - .pdf  -> poppler und/oder pypdf
    - .epub -> epub (stdlib)
    `choice` = 'poppler' | 'pypdf' | 'both' filtert zusaetzlich.
    """
    ext = src.suffix.lower()

    if ext == ".epub":
        if choice in ("poppler", "pypdf"):
            raise SystemExit(
                f"[Fehler] EPUB-Quelle, aber Engine '{choice}' erzwungen. "
                "Bitte --engine weglassen oder die Quelle vorher in PDF konvertieren."
            )
        return [Engine("epub", True)]

    if ext != ".pdf":
        raise SystemExit(f"[Fehler] Unbekanntes Format: {ext!r} ({src.name})")

    poppler = _check_pdftotext()
    pypdf   = _check_pypdf()
    if choice == "poppler":
        if not poppler.available:
            raise SystemExit(f"[Fehler] {poppler.reason}")
        return [poppler]
    if choice == "pypdf":
        if not pypdf.available:
            raise SystemExit(f"[Fehler] {pypdf.reason}")
        return [pypdf]
    # both
    avail = [e for e in (poppler, pypdf) if e.available]
    if not avail:
        raise SystemExit(
            "[Fehler] Keine Extraktions-Engine verfuegbar.\n"
            f"  poppler: {poppler.reason}\n  pypdf  : {pypdf.reason}"
        )
    return avail


def _run_list(bibkey: str, pdf: Path, engines: Iterable[Engine]) -> int:
    print(f"{bibkey}  <-  {pdf.name}")
    for eng in engines:
        try:
            pages = get_pages(bibkey, pdf, eng.name)
        except Exception as exc:
            print(f"  [{eng.name:<7}] FEHLER: {exc}")
            continue
        total_chars = sum(len(p) for p in pages)
        print(f"  [{eng.name:<7}] {len(pages):>4} Seiten, {total_chars:>8} Zeichen")
    return 0


def _run_dump(bibkey: str, pdf: Path, engines: list[Engine],
              page_spec: str | None, outfile: Path | None) -> int:
    chunks: list[str] = []
    for eng in engines:
        try:
            pages = get_pages(bibkey, pdf, eng.name)
        except Exception as exc:
            print(f"[{eng.name}] FEHLER: {exc}", file=sys.stderr)
            continue
        selected = _parse_pages(page_spec, len(pages))
        header   = f"\n===== {bibkey} :: {eng.name} "
        header  += f"(Seiten {selected[0]}-{selected[-1]} von {len(pages)}) =====\n" \
                   if selected else f"(0 von {len(pages)}) =====\n"
        chunks.append(header)
        for p in selected:
            chunks.append(f"\n----- Seite {p} ({eng.name}) -----\n")
            chunks.append(pages[p - 1])

    output = "".join(chunks)
    if outfile:
        outfile.write_text(output, encoding="utf-8")
        print(f"[OK] -> {outfile}  ({len(output)} Zeichen)")
    else:
        sys.stdout.write(output)
    return 0


def _run_search(bibkey: str, pdf: Path, engines: list[Engine],
                query: str, ctx: int) -> int:
    any_hit = False
    for eng in engines:
        try:
            pages = get_pages(bibkey, pdf, eng.name)
        except Exception as exc:
            print(f"[{eng.name}] FEHLER: {exc}", file=sys.stderr)
            continue
        hits = search_pages(pages, query, ctx=ctx)
        print(f"\n[{eng.name}]  Anfrage: {query!r}  -  {len(hits)} Treffer")
        for page_no, snippet in hits:
            any_hit = True
            print(f"  S.{page_no:>4}: {snippet}")
    return 0 if any_hit else 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pdf_extract.py",
        description="Seitengenaue PDF-Textextraktion fuer die Zitatpruefung.",
    )
    p.add_argument("bibkey", help="BibKey (entspricht dem Ordnernamen unter Literatur/).")
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("-p", "--page", dest="pages",
                      help="Seite(n): z.B. 42, 10-20, 1,3,5-7. Default: ganze PDF.")
    mode.add_argument("-s", "--search",
                      help="Fuzzy-Suche nach Phrase (Whitespace-tolerant).")
    mode.add_argument("--list", action="store_true",
                      help="Nur Seitenzahl + Zeichenzahl pro Engine anzeigen.")
    p.add_argument("--engine", choices=("both", "poppler", "pypdf"),
                   default="both",
                   help="Welche Engine(s) verwenden (Default: beide).")
    p.add_argument("--context", type=int, default=80,
                   help="Kontextzeichen pro Seite fuer --search (Default: 80).")
    p.add_argument("--out", type=Path,
                   help="Dump in Datei schreiben statt stdout.")
    p.add_argument("--source",
                   help="Pfad zur Quelldatei (absolut oder relativ zu "
                        "Literatur/<bibkey>/), ueberschreibt die "
                        "Priorisierung source_foxit.pdf > source_ocr.pdf > "
                        "source.pdf > source.epub.")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    src  = _find_source_pdf(args.bibkey, args.source)
    engines = _select_engines(src, args.engine)

    if args.list:
        return _run_list(args.bibkey, src, engines)
    if args.search:
        return _run_search(args.bibkey, src, engines, args.search, args.context)
    return _run_dump(args.bibkey, src, engines, args.pages, args.out)


if __name__ == "__main__":
    sys.exit(main())
