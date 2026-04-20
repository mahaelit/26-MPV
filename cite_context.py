"""cite_context.py - Phase 1b: Cite-Stellen aus TeX ins Verifikationsdossier

Fuer jede Quelle in `Literatur/<BibKey>/verified_quotes.md` wird ein
auto-generierter Block eingefuegt/aufgefrischt, der *alle* cite-Stellen
aus den Haupt-TeX-Dateien enthaelt - mit Zeilennummer, optionalen
Argumenten (pre/post, z. B. Seiten) und Kontext.

Ziele
-----
- Zero-Loss: Der Nutzer pflegt Zitate unterhalb des Blocks. Die
  Ersetzung passiert atomar zwischen zwei HTML-Markern:
    <!-- CLAIMS-START ... -->   ...   <!-- CLAIMS-END -->

- Idempotent: Re-Runs sind verlustfrei, Aenderungen unterhalb bleiben.

- Robust:
    * `\\verb|...|` und `%`-Kommentare werden zeichenweise durch
      Leerzeichen ersetzt, sodass Zeilennummern und Offsets exakt
      erhalten bleiben.
    * Biblatex-Varianten werden breit abgedeckt: \\cite, \\parencite,
      \\textcite, \\autocite, \\smartcite, \\citeauthor, \\citeyear,
      \\citetitle, \\supercite, inkl. *-Sternvarianten und optionalem
      Pre-/Post-Argument.

Usage
-----
    python cite_context.py

Optionen (Env-Variablen):
    CITE_SOURCES   Semikolon-getrennte TeX-Dateien (default: mpv.tex;
                   mpv_abgabedokument.tex)
    CITE_CONTEXT   Zeichen vor/nach dem cite-Kommando (default: 220)
"""
from __future__ import annotations

import os
import re
import sys
from bisect import bisect_right
from pathlib import Path
from typing import Iterable

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


HERE         = Path(__file__).resolve().parent
LITERATUR    = HERE / "Literatur"

# Kuerzel pro Quelldatei fuer kompakte Anzeige im Claims-Block.
DEFAULT_SOURCES = {
    "mpv.tex":                "L",   # Lerndokument
    "mpv_abgabedokument.tex": "A",   # Abgabedokument
}

CONTEXT_CHARS = int(os.environ.get("CITE_CONTEXT", "220"))

# ----- Marker -----------------------------------------------------------
MARK_START = "<!-- CLAIMS-START (automatisch durch cite_context.py erzeugt; nicht manuell editieren) -->"
MARK_END   = "<!-- CLAIMS-END -->"
BLOCK_RE   = re.compile(
    r"<!-- CLAIMS-START[^>]*-->.*?<!-- CLAIMS-END -->",
    re.DOTALL,
)

# Trenner des Metadaten-Headers der verified_quotes.md
HEADER_SEP_RE = re.compile(r"\n\s*---\s*\n")


# ----- TeX-Vorbereitung -------------------------------------------------
VERB_RE    = re.compile(r"\\verb\*?(?P<delim>[^a-zA-Z0-9\s])(?:(?!(?P=delim)).)*(?P=delim)")
COMMENT_RE = re.compile(r"(?<!\\)%[^\n]*")
VERBATIM_ENV_RE = re.compile(
    r"\\begin\{(verbatim|lstlisting|minted)\*?\}.*?\\end\{\1\*?\}",
    re.DOTALL,
)


def _mask_preserving_offsets(text: str, pattern: re.Pattern) -> str:
    """Ersetzt Matches durch gleich lange Folgen von Leerzeichen/Newlines,
    sodass alle Offsets und Zeilennummern erhalten bleiben.
    """
    out = list(text)
    for m in pattern.finditer(text):
        for i in range(m.start(), m.end()):
            out[i] = "\n" if text[i] == "\n" else " "
    return "".join(out)


def prepare_tex(text: str) -> str:
    """Maskiert verbatim-Umgebungen, `\\verb|...|` und `%`-Kommentare."""
    text = _mask_preserving_offsets(text, VERBATIM_ENV_RE)
    text = _mask_preserving_offsets(text, VERB_RE)
    text = _mask_preserving_offsets(text, COMMENT_RE)
    return text


# ----- Cite-Regex -------------------------------------------------------
# Biblatex-Kommandos: alles was wir tatsaechlich nutzen wollen.
# NICHT dabei: \citealp etc. (natbib) - koennten bei Bedarf ergaenzt werden.
CITE_CMDS = (
    "cite", "Cite",
    "parencite", "Parencite",
    "textcite", "Textcite",
    "autocite", "Autocite",
    "smartcite", "Smartcite",
    "supercite",
    "footcite", "footcitetext",
    "citeauthor", "Citeauthor",
    "citeyear", "citedate", "citetitle",
    "nocite",
)
CITE_PATTERN = re.compile(
    r"\\(?P<cmd>(?:" + "|".join(CITE_CMDS) + r"))\*?"
    r"(?P<opt1>\[[^\]]*\])?"
    r"(?P<opt2>\[[^\]]*\])?"
    r"\{(?P<keys>[^{}]+)\}"
)


# ----- Datenmodell ------------------------------------------------------
class Citation:
    __slots__ = ("bibkey", "src_label", "line", "cmd", "pre", "post",
                 "raw", "context_before", "context_after")

    def __init__(self, bibkey, src_label, line, cmd, pre, post, raw,
                 context_before, context_after):
        self.bibkey         = bibkey
        self.src_label      = src_label
        self.line           = line
        self.cmd            = cmd
        self.pre            = pre
        self.post           = post
        self.raw            = raw
        self.context_before = context_before
        self.context_after  = context_after


# ----- Extraktion -------------------------------------------------------
_WS_RE = re.compile(r"\s+")


def _squash(s: str) -> str:
    return _WS_RE.sub(" ", s).strip()


def _line_index(text: str) -> list[int]:
    """Offsets der Zeilenanfaenge; Eintrag i ist Start von Zeile i+1."""
    starts = [0]
    for i, ch in enumerate(text):
        if ch == "\n":
            starts.append(i + 1)
    return starts


def _line_of(offset: int, starts: list[int]) -> int:
    # bisect_right: groesster Index mit starts[idx] <= offset
    return bisect_right(starts, offset)


def extract_citations(tex_path: Path, src_label: str) -> list[Citation]:
    if not tex_path.is_file():
        return []
    raw   = tex_path.read_text(encoding="utf-8", errors="replace")
    clean = prepare_tex(raw)
    starts = _line_index(raw)

    results: list[Citation] = []
    for m in CITE_PATTERN.finditer(clean):
        keys_field = m.group("keys")
        cmd        = m.group("cmd")
        opt1       = m.group("opt1") or ""
        opt2       = m.group("opt2") or ""

        # Biblatex-Konvention: [opt1]{keys}  -> post   (entspricht "S.~42")
        #                     [opt1][opt2]   -> pre/post
        pre  = ""
        post = ""
        if opt1 and opt2:
            pre  = opt1[1:-1].strip()
            post = opt2[1:-1].strip()
        elif opt1:
            post = opt1[1:-1].strip()

        # Kontext aus dem ORIGINAL-TeX ziehen, damit verbatim/comment
        # zwar ausgeblendet waren, aber der Originaltext angezeigt wird.
        ctx_a = max(0, m.start() - CONTEXT_CHARS)
        ctx_b = min(len(raw), m.end() + CONTEXT_CHARS)
        line  = _line_of(m.start(), starts)
        raw_cite = raw[m.start():m.end()]

        ctx_before = _squash(raw[ctx_a:m.start()])
        ctx_after  = _squash(raw[m.end():ctx_b])

        for key in (k.strip() for k in keys_field.split(",")):
            if not key:
                continue
            results.append(Citation(
                bibkey         = key,
                src_label      = src_label,
                line           = line,
                cmd            = cmd,
                pre            = pre,
                post           = post,
                raw            = raw_cite,
                context_before = ctx_before,
                context_after  = ctx_after,
            ))
    return results


# ----- Claims-Block-Rendering -------------------------------------------
def _format_claim(idx: int, c: Citation) -> str:
    """Eine nummerierte Bullet-Zeile fuer eine Cite-Stelle."""
    ref = f"[{c.src_label}:{c.line}]"
    # Optionale Argumente kompakt anzeigen (nur wenn vorhanden)
    extra = ""
    if c.pre and c.post:
        extra = f" (pre=\"{c.pre}\", post=\"{c.post}\")"
    elif c.post:
        extra = f" (post=\"{c.post}\")"
    elif c.pre:
        extra = f" (pre=\"{c.pre}\")"

    before = c.context_before[-160:] if len(c.context_before) > 160 else c.context_before
    after  = c.context_after[:160]  if len(c.context_after)  > 160 else c.context_after
    # Den cite-Befehl hervorheben, damit die Stelle schnell erkennbar ist.
    context = f"{before} **`{c.raw}`**{extra} {after}".strip()
    return f"{idx}. **{ref}** {context}"


# Optional: Claim-Split-Matching fuer automatische Beleg-Vorschlaege
try:
    import claim_split_match as _csm
    _HAS_CSM = True
except Exception:
    _HAS_CSM = False


def _split_suggestions(bibkey: str, context: str, splits: list, top_n: int = 2) -> list[str]:
    """Liefert Markdown-Zeilen mit Beleg-Vorschlaegen fuer einen Claim."""
    if not _HAS_CSM or not splits:
        return []
    matches = _csm.match_claim(context, splits, top_n=top_n, min_score=0.08)
    out: list[str] = []
    for i, m in enumerate(matches, start=1):
        out.append(
            f"   → Beleg-Vorschlag [{i}] (score {m['score']:.2f}): "
            f"[`{m['file']}`](excerpts/{m['file']}) "
            f"S. {m['page_start']}-{m['page_end']} · {m['title'][:60]}"
        )
    return out


def render_claims_block(bibkey: str, cites: list[Citation]) -> str:
    header = "## Zu verifizierende Behauptungen (aus TeX)"
    if not cites:
        body = (
            f"_Aktuell **nicht** im TeX zitiert._  "
            f"Pruefen, ob der BibKey noch benoetigt wird oder entfernt werden kann."
        )
        return f"{MARK_START}\n\n{header}\n\n{body}\n\n{MARK_END}"

    # Sortiere: erst nach Quelle, dann Zeile, damit der Block reproduzierbar ist.
    cites_sorted = sorted(cites, key=lambda c: (c.src_label, c.line))
    intro = (
        f"_Dieser BibKey wird **{len(cites_sorted)}**-mal zitiert._  "
        f"Quellen-Kuerzel: **L** = `mpv.tex` (Lerndokument), "
        f"**A** = `mpv_abgabedokument.tex` (Abgabedokument)."
    )

    # Splits dieser Quelle EINMAL laden (Cache)
    splits = []
    if _HAS_CSM:
        try:
            splits = _csm.load_splits(bibkey)
        except Exception:
            splits = []

    lines: list[str] = []
    for i, c in enumerate(cites_sorted):
        claim_line = _format_claim(i + 1, c)
        lines.append(claim_line)
        # Beleg-Vorschlaege direkt unter dem Claim
        if splits:
            # Kontext: context_before + cite + context_after
            combined_ctx = f"{c.context_before} {c.context_after}"
            sug = _split_suggestions(bibkey, combined_ctx, splits)
            if sug:
                lines.append("\n".join(sug))

    body = intro + "\n\n" + "\n\n".join(lines)
    if splits:
        hint = (
            f"\n\n**{len(splits)} Kapitel-Splits verfuegbar** unter [`excerpts/_outline.md`](excerpts/_outline.md). "
            f"Pro Cite-Stelle sind (falls erkennbar) die 1-2 wahrscheinlichsten Splits als "
            f"**Beleg-Vorschlag** angegeben (Keyword-Matching)."
        )
        body = intro + hint + "\n\n" + "\n\n".join(lines)
    return f"{MARK_START}\n\n{header}\n\n{body}\n\n{MARK_END}"


# ----- Datei-Update -----------------------------------------------------
def update_verified_quotes(md_path: Path, block: str) -> str:
    """Fuegt/ersetzt den Claims-Block in verified_quotes.md ein.

    Rueckgabe: Status-String ('created', 'updated', 'unchanged', 'missing').
    """
    if not md_path.is_file():
        return "missing"

    text = md_path.read_text(encoding="utf-8")

    if BLOCK_RE.search(text):
        # Callable statt String-Replacement, damit Python Backslash-Sequenzen
        # (`\parencite`, `\cite`, ...) im `block`-Text NICHT als Template-
        # Backreferences interpretiert.
        new_text = BLOCK_RE.sub(lambda _m: block, text, count=1)
    else:
        # Block direkt hinter dem Header-Trenner (erster '---') einfuegen.
        sep = HEADER_SEP_RE.search(text)
        if not sep:
            # Defensiv: kein Header -> ganz oben einfuegen.
            new_text = block + "\n\n" + text
        else:
            insert_at = sep.end()
            new_text  = (
                text[:insert_at]
                + "\n" + block + "\n\n"
                + text[insert_at:]
            )

    if new_text == text:
        return "unchanged"
    md_path.write_text(new_text, encoding="utf-8")
    return "created" if BLOCK_RE.search(text) is None else "updated"


# ----- Orchestrierung ---------------------------------------------------
def _resolve_sources() -> list[tuple[Path, str]]:
    spec = os.environ.get("CITE_SOURCES", "").strip()
    if not spec:
        items = [(HERE / name, label) for name, label in DEFAULT_SOURCES.items()]
    else:
        items = []
        for tok in spec.split(";"):
            tok = tok.strip()
            if not tok:
                continue
            # Optional: "path=LABEL"
            if "=" in tok:
                path, label = tok.split("=", 1)
                items.append((Path(path), label.strip() or "?"))
            else:
                items.append((Path(tok), DEFAULT_SOURCES.get(tok, "?")))
    return items


def collect_all(sources: Iterable[tuple[Path, str]]) -> dict[str, list[Citation]]:
    bucket: dict[str, list[Citation]] = {}
    for path, label in sources:
        cites = extract_citations(path, label)
        print(f"  [tex] {path.name:<26} -> {len(cites):>3} cite-Stellen "
              f"(Label {label!r})")
        for c in cites:
            bucket.setdefault(c.bibkey, []).append(c)
    return bucket


def main() -> int:
    print("cite_context.py - Phase 1b")
    print(f"  Kontext : +/-{CONTEXT_CHARS} Zeichen")
    print(f"  Ordner  : {LITERATUR}")
    print()

    sources = _resolve_sources()
    print("--- Schritt 1: TeX-Dateien scannen ---")
    bucket  = collect_all(sources)
    total   = sum(len(v) for v in bucket.values())
    print(f"  {total} cite-Stellen auf {len(bucket)} BibKeys aggregiert.")
    print()

    # Nur BibKeys mit existierendem Ordner (von bib2csv.py angelegt) beachten.
    folders = {p.name for p in LITERATUR.iterdir() if p.is_dir()} \
              if LITERATUR.exists() else set()
    unknown = [k for k in bucket if k not in folders]
    if unknown:
        print("  !! Im TeX zitierte BibKeys OHNE Ordner "
              "(fehlt in Quellen.bib oder bib2csv.py noch nicht gelaufen?):")
        for k in sorted(unknown):
            print(f"     - {k}  ({len(bucket[k])} cite-Stelle(n))")
        print()

    print("--- Schritt 2: verified_quotes.md aktualisieren ---")
    stats = {"created": 0, "updated": 0, "unchanged": 0, "missing": 0}
    # Alle bekannten Ordner anfassen, damit auch BibKeys OHNE Zitate
    # einen aufgeraeumten Block bekommen.
    for key in sorted(folders):
        block = render_claims_block(key, bucket.get(key, []))
        md = LITERATUR / key / "verified_quotes.md"
        status = update_verified_quotes(md, block)
        stats[status] = stats.get(status, 0) + 1

    print(f"  created={stats['created']}  updated={stats['updated']}  "
          f"unchanged={stats['unchanged']}  missing={stats['missing']}")

    # Kleine "Top-Listen" als Orientierung fuer die Verifikationsreihenfolge.
    ranked = sorted(bucket.items(), key=lambda kv: -len(kv[1]))[:10]
    if ranked:
        print()
        print("  Top 10 zitierte BibKeys (Prioritaet fuer Phase 2):")
        for key, cites in ranked:
            print(f"    {len(cites):>3}x  {key}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
