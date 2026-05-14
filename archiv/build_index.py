"""build_index.py - Erzeugt `Literatur/_INDEX.md` mit Status-Uebersicht pro BibKey.

Aggregiert pro Eintrag in `Quellen.bib`:
  - Titel / Autor / Jahr / Typ
  - Verifikations-Status (aus verified_quotes.md)
  - Cite-Count in mpv.tex / mpv_abgabedokument.tex (aus CLAIMS-Block)
  - Transkript-Verortungen (Anzahl aus _transkripte_index.json)
  - Volltext-Status (source.pdf / source.epub vorhanden? Groesse)
  - Pending-Rewrites (aus collect_rewrites.py)

Schreibt `Literatur/_INDEX.md` mit:
  - Top-level Status-Zusammenfassung (Bucket-Counts pro Status 0-5)
  - Sortierbare Tabelle ueber alle BibKeys
  - Highlights-Abschnitt: Status 5 fertig, Status 4 mit pending Rewrites,
    kritische Luecken (Status 0/1 + hohe Cite-Counts).
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Eigener Aggregator wird als Modul importiert — eine gemeinsame Quelle der
# Wahrheit fuer Rewrite-Zaehlungen vermeidet Drift zwischen den beiden
# Skripten.
from collect_rewrites import collect_all as collect_rewrites  # noqa: E402


HERE       = Path(__file__).resolve().parent
LITERATUR  = HERE / "Literatur"
BIB_PATH   = HERE / "Quellen.bib"
TRANS_IDX  = LITERATUR / "_transkripte_index.json"
OUT_PATH   = LITERATUR / "_INDEX.md"


# ---------------------------------------------------------------------------
# Quellen.bib-Parser (leichtgewichtig, eigener Ansatz statt pybtex-Dependency)
# ---------------------------------------------------------------------------
# Einstieg jedes Eintrags: `@type{key,` am Zeilenanfang. Der Eintrags-Body
# laeuft dann bis zum naechsten solchen Einstieg oder EOF. Das ist robuster
# als das Ende ueber `\n}\n` zu finden, weil manche Body-Werte selbst `}`
# und ggf. `\n@` (in Kommentaren/Annotations) enthalten koennen.
BIB_HEADER_RE = re.compile(
    r"^@(?P<type>\w+)\s*\{\s*(?P<key>[^,\s]+)\s*,",
    re.MULTILINE,
)


def _bib_field(body: str, name: str) -> str:
    m = re.search(rf"\b{name}\s*=\s*\{{(.*?)\}}\s*,", body,
                  re.IGNORECASE | re.DOTALL)
    return m.group(1).strip() if m else ""


@dataclass
class BibEntry:
    key:    str
    etype:  str          # article, book, incollection, ...
    author: str
    year:   str
    title:  str


def parse_bib(path: Path) -> list[BibEntry]:
    text = path.read_text(encoding="utf-8")
    headers = list(BIB_HEADER_RE.finditer(text))
    out: list[BibEntry] = []
    for i, m in enumerate(headers):
        body_start = m.end()
        body_end   = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        body = text[body_start:body_end]
        out.append(BibEntry(
            key    = m.group("key").strip(),
            etype  = m.group("type").strip().lower(),
            author = _bib_field(body, "author") or _bib_field(body, "editor"),
            year   = _bib_field(body, "year"),
            title  = _bib_field(body, "title"),
        ))
    return out


# ---------------------------------------------------------------------------
# Dossier-Parser: Status, Cite-Count, Verifiziert-am
# ---------------------------------------------------------------------------
STATUS_RE     = re.compile(r"^\*\*Status:\*\*\s*(\d+)", re.MULTILINE)
VERIFIED_RE   = re.compile(r"^\*\*Verifiziert am:\*\*\s*(\S.*?)\s*$",
                           re.MULTILINE)
CITE_COUNT_RE = re.compile(r"wird\s+\*\*(\d+)\*\*-mal\s+zitiert", re.IGNORECASE)


@dataclass
class DossierInfo:
    exists:      bool = False
    status:      int | None = None
    verified_at: str = ""
    cite_count:  int | None = None
    has_pdf:     bool = False
    has_epub:    bool = False
    pdf_bytes:   int = 0


def inspect_dossier(key: str) -> DossierInfo:
    d = LITERATUR / key
    info = DossierInfo()
    if not d.is_dir():
        return info
    info.exists = True

    md = d / "verified_quotes.md"
    if md.is_file():
        text = md.read_text(encoding="utf-8")
        m = STATUS_RE.search(text)
        if m:
            try:
                info.status = int(m.group(1))
            except ValueError:
                pass
        vm = VERIFIED_RE.search(text)
        if vm:
            v = vm.group(1).strip()
            # Placeholder "<YYYY-MM-DD>" ignorieren
            if not v.startswith("<") and v:
                info.verified_at = v
        cc = CITE_COUNT_RE.search(text)
        if cc:
            info.cite_count = int(cc.group(1))

    for ext in (".pdf", ".epub"):
        p = d / f"source{ext}"
        if p.is_file():
            if ext == ".pdf":
                info.has_pdf = True
                info.pdf_bytes = p.stat().st_size
            else:
                info.has_epub = True
    return info


# ---------------------------------------------------------------------------
# Transkript-Index: Anzahl Eintraege pro BibKey
# ---------------------------------------------------------------------------
def load_transcript_counts(idx_path: Path) -> dict[str, int]:
    """Liefert {bibkey: anzahl_eintraege} aus dem Transkript-Index.

    Das aktuelle Schema (`schema_version: 1.1`) verpackt die Map unter dem
    Schluessel `bibkey_to_transkripte`. Altere (schemalose) Varianten legten
    die Map direkt auf Top-Level ab — beide werden unterstuetzt.
    """
    if not idx_path.is_file():
        return {}
    data = json.loads(idx_path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        inner = data.get("bibkey_to_transkripte")
        if isinstance(inner, dict):
            return {k: len(v) if isinstance(v, list) else 0
                    for k, v in inner.items()}
        # Fallback: altes, flaches Schema (keine schema_version).
        if "schema_version" not in data:
            return {k: len(v) if isinstance(v, list) else 0
                    for k, v in data.items()}
    return {}


# ---------------------------------------------------------------------------
# Rewrite-Zaehlungen
# ---------------------------------------------------------------------------
def rewrite_counts_by_key() -> dict[str, dict[str, int]]:
    """{bibkey: {"pending": n, "applied": n, "rejected": n}}.

    Zaehlt Rewrites nach ihrem *source_dossier* (der BibKey, in dessen Dossier
    der Rewrite-Block liegt — typischerweise der gestrichene/ersetzte Key).
    """
    out: dict[str, dict[str, int]] = {}
    for r in collect_rewrites(LITERATUR):
        d = out.setdefault(r.source_dossier,
                           {"pending": 0, "applied": 0, "rejected": 0})
        d[r.status] = d.get(r.status, 0) + 1
    return out


# ---------------------------------------------------------------------------
# Markdown-Ausgabe
# ---------------------------------------------------------------------------
STATUS_LABEL = {
    0: "ungeprueft",
    1: "begonnen",
    2: "angefangen",
    3: "Transkript-konsistent",
    4: "Volltext geprueft",
    5: "vollstaendig verifiziert",
}


def _fmt_bytes(n: int) -> str:
    if n <= 0:
        return "—"
    if n < 1024:
        return f"{n} B"
    if n < 1024**2:
        return f"{n/1024:.0f} kB"
    return f"{n/1024**2:.1f} MB"


def _status_label(st: int | None) -> str:
    if st is None:
        return "— (kein Dossier)"
    return f"{st} ({STATUS_LABEL.get(st, '?')})"


def render_markdown(
    entries:    list[BibEntry],
    dossiers:   dict[str, DossierInfo],
    transcripts: dict[str, int],
    rewrites:    dict[str, dict[str, int]],
) -> str:
    lines: list[str] = []
    lines.append("# `_INDEX.md` — Verifikations-Statusuebersicht pro BibKey")
    lines.append("")
    lines.append("_Automatisch erzeugt durch `build_index.py`. Nicht manuell "
                 "editieren — aendern Sie die Quelldateien (`Quellen.bib`, "
                 "`Literatur/<key>/verified_quotes.md`, "
                 "`Literatur/_transkripte_index.json`, die Rewrite-Bloecke) "
                 "und lassen Sie das Skript neu laufen._")
    lines.append("")

    # --- Status-Summary -----------------------------------------------------
    status_counts: dict[str, int] = {}
    for e in entries:
        info = dossiers.get(e.key, DossierInfo())
        if not info.exists:
            status_counts["ohne Ordner"] = status_counts.get("ohne Ordner", 0) + 1
            continue
        st = info.status
        key = _status_label(st)
        status_counts[key] = status_counts.get(key, 0) + 1

    lines.append("## Status-Verteilung")
    lines.append("")
    lines.append(f"- **BibKeys gesamt:** {len(entries)}")
    for k in sorted(status_counts):
        lines.append(f"- **{k}:** {status_counts[k]}")
    lines.append("")

    # --- Sortierte Haupttabelle --------------------------------------------
    # Sortierreihenfolge: nach Status aufsteigend (0 unten = niedrige
    # Verifikation oben), bei gleichem Status nach Cite-Count absteigend.
    def sort_key(e: BibEntry):
        info = dossiers.get(e.key, DossierInfo())
        st = info.status if info.status is not None else 99
        cc = -(info.cite_count or 0)
        return (st, cc, e.key)

    lines.append("## Detailtabelle")
    lines.append("")
    lines.append("| Status | BibKey | Autor/Jahr | Cites | Transkripte | "
                 "Volltext | Rewrites (P/A/R) | Verifiziert am |")
    lines.append("|---|---|---|---:|---:|---|---:|---|")
    for e in sorted(entries, key=sort_key):
        info = dossiers.get(e.key, DossierInfo())
        tc = transcripts.get(e.key, 0)
        rw = rewrites.get(e.key, {})
        st_cell  = _status_label(info.status)
        key_cell = f"`{e.key}`"
        ay_cell  = f"{e.author.split(' and ')[0] if e.author else '—'} ({e.year or '—'})"
        cc_cell  = "—" if info.cite_count is None else str(info.cite_count)
        tc_cell  = "—" if tc == 0 else str(tc)
        vt_parts = []
        if info.has_pdf:
            vt_parts.append(f"PDF {_fmt_bytes(info.pdf_bytes)}")
        if info.has_epub:
            vt_parts.append("EPUB")
        if not vt_parts:
            if info.exists:
                vt_parts.append("—")
            else:
                vt_parts.append("_(kein Ordner)_")
        vt_cell = ", ".join(vt_parts)
        p = rw.get("pending", 0)
        a = rw.get("applied", 0)
        rj = rw.get("rejected", 0)
        if p + a + rj == 0:
            rw_cell = "—"
        else:
            rw_cell = f"{p}/{a}/{rj}"
        va_cell = info.verified_at or "—"
        lines.append(f"| {st_cell} | {key_cell} | {ay_cell} | {cc_cell} | "
                     f"{tc_cell} | {vt_cell} | {rw_cell} | {va_cell} |")
    lines.append("")

    # --- Highlights ---------------------------------------------------------
    lines.append("## Highlights")
    lines.append("")

    done = [e for e in entries
            if (dossiers.get(e.key, DossierInfo()).status or 0) >= 5]
    if done:
        lines.append("### ✅ Vollstaendig verifiziert (Status 5)")
        lines.append("")
        for e in sorted(done, key=lambda x: x.key):
            lines.append(f"- `{e.key}`")
        lines.append("")

    with_pending = [e for e in entries
                    if rewrites.get(e.key, {}).get("pending", 0) > 0]
    if with_pending:
        lines.append("### ⏳ Mit offenen Rewrites")
        lines.append("")
        for e in sorted(with_pending, key=lambda x: x.key):
            p = rewrites[e.key]["pending"]
            lines.append(f"- `{e.key}` — {p} pending rewrite(s)")
        lines.append("")

    # Kritische Luecken: Status 0 mit hohem Cite-Count (Abgabe-Risiko).
    critical = [
        e for e in entries
        if (dossiers.get(e.key, DossierInfo()).status or 0) <= 1
        and (dossiers.get(e.key, DossierInfo()).cite_count or 0) >= 5
    ]
    if critical:
        lines.append("### ⚠ Kritische Luecken (Status 0/1 + Cites ≥ 5)")
        lines.append("")
        lines.append("_Hohe Zitatdichte ohne Verifikation = Abgabe-Risiko._")
        lines.append("")
        for e in sorted(critical,
                        key=lambda x: -(dossiers[x.key].cite_count or 0)):
            cc = dossiers[e.key].cite_count
            tc = transcripts.get(e.key, 0)
            lines.append(f"- `{e.key}` — {cc} Cites, {tc} Transkript-Stellen")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    if not BIB_PATH.is_file():
        print(f"[ERR] {BIB_PATH} fehlt.", file=sys.stderr)
        return 1
    if not LITERATUR.is_dir():
        print(f"[ERR] {LITERATUR} fehlt.", file=sys.stderr)
        return 1

    print("build_index.py")
    print(f"  Bib   : {BIB_PATH.name}")
    print(f"  Index : {TRANS_IDX.name if TRANS_IDX.is_file() else '(fehlt)'}")

    entries = parse_bib(BIB_PATH)
    print(f"  BibKeys: {len(entries)}")

    dossiers = {e.key: inspect_dossier(e.key) for e in entries}
    have_dossier = sum(1 for d in dossiers.values() if d.exists)
    print(f"  Dossiers vorhanden: {have_dossier} / {len(entries)}")

    transcripts = load_transcript_counts(TRANS_IDX)
    print(f"  BibKeys mit Transkript-Eintraegen: {len(transcripts)}")

    rewrites = rewrite_counts_by_key()
    n_pending = sum(v.get("pending", 0) for v in rewrites.values())
    print(f"  Pending Rewrites: {n_pending}")

    md = render_markdown(entries, dossiers, transcripts, rewrites)
    OUT_PATH.write_text(md, encoding="utf-8")
    print(f"  [OK] -> {OUT_PATH}  ({len(md)} Zeichen)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
