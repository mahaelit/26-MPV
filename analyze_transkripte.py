"""analyze_transkripte.py - Aggregiert die 8 Transkript-Verortungs-JSONs
aus `MPV/Literatur/Transkripte/einordnung/` in einen strukturierten
Markdown-Bericht + ein Mapping pro bestehenden BibKey.

Die JSONs sind heterogen aufgebaut (unterschiedliche Schemas pro Datei),
deshalb arbeitet dieser Analyzer *defensiv mit Best-Effort-Extraktion*:
er sucht in jeder Datei nach gemeinsamen Schluesselinformationen und
liefert eine Uebersicht, ohne bei Abweichungen zu brechen.

Output
------
1. `TRANSKRIPTE_UEBERSICHT.md` (Workspace-Root):
   - Tabelle: Transkript -> Quelle -> BibKey (bestehend/vorgeschlagen) ->
     Pruefungsfragen-Relevanz -> Anzahl Integration-Vorschlaege
   - Sektion: neue `@incollection`-BibKey-Vorschlaege (gesammelt)
   - Sektion: bestehende BibKeys mit Transkript-Rueckendeckung
   - Sektion: offene Issues / Verifikationsauftraege

2. `Literatur/_transkripte_index.json` (Maschinenlesbar):
   - pro BibKey die Liste der relevanten Transkripte + Integration-Snippets
   - damit in einem spaeteren Durchgang die verified_quotes.md pro Quelle
     um einen `## Transkript-Verortungen`-Block ergaenzt werden koennen.

Usage
-----
    python analyze_transkripte.py

Optionen:
    --json-dir  <pfad>   Verzeichnis der JSON-Dateien
                         (Default: ../Literatur/Transkripte/einordnung relativ
                         zu diesem Script)
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


HERE               = Path(__file__).resolve().parent
LITERATUR          = HERE / "Literatur"
DEFAULT_JSON_DIR   = HERE.parent / "Literatur" / "Transkripte" / "einordnung"
OUT_OVERVIEW_MD    = HERE / "TRANSKRIPTE_UEBERSICHT.md"
OUT_INDEX_JSON     = LITERATUR / "_transkripte_index.json"
BIB_PATH           = HERE / "Quellen.bib"


# -----------------------------------------------------------------------
# Existierende BibKeys ermitteln (aus Quellen.bib)
# -----------------------------------------------------------------------
import re as _re
_ENTRY_RE = _re.compile(r"@([A-Za-z]+)\s*\{\s*([A-Za-z0-9_:\-]+)\s*,", _re.MULTILINE)


def load_existing_bibkeys(bib_path: Path) -> set[str]:
    if not bib_path.is_file():
        return set()
    text = bib_path.read_text(encoding="utf-8")
    return {m.group(2) for m in _ENTRY_RE.finditer(text)}


# -----------------------------------------------------------------------
# Datenmodell
# -----------------------------------------------------------------------
@dataclass
class TranskriptBefund:
    """Vereinheitlichte Sicht auf den Befund einer JSON-Datei.

    Ein JSON kann genau einen Haupt-Befund (``is_chapter=False``) oder -
    bei Multi-Chapter-Dateien (z. B. Teil1, Teil3) - zusaetzlich pro
    ``chapters[i]`` einen Chapter-Befund mit ``is_chapter=True`` liefern.
    Der Chapter-Befund gehoert zu einem eigenen BibKey und wird spaeter
    als ``role='chapter_main'`` in den Index eingetragen.
    """
    source_file: str
    title: str = ""
    transcript_file: str | None = None
    buch: str = ""
    editors_authors: str = ""
    chapter_title: str | None = None
    chapter_authors: str | None = None
    pages: str | None = None
    year: int | None = None
    existing_bibkey: str | None = None
    proposed_bibkey: str | None = None
    proposed_bibtex_raw: str | None = None
    relevance_per_question: dict[str, str] = field(default_factory=dict)
    integration_hints: list[dict] = field(default_factory=list)
    issues: list[dict] = field(default_factory=list)
    records_count: int | None = None
    notes: list[str] = field(default_factory=list)
    # key -> Anzahl Erwaehnungen (z. B. zitatstellen[].bib_key == "kappus2010migration")
    bibkey_mentions: dict[str, int] = field(default_factory=dict)
    # True fuer per-chapter extrahierte Befunde (aus Teil1/Teil3 chapters[])
    is_chapter: bool = False


# -----------------------------------------------------------------------
# Extraktions-Helfer (robust, Best-Effort)
# -----------------------------------------------------------------------
def _as_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        parts = [_as_str(v) for v in value]
        return " / ".join(p for p in parts if p)
    if isinstance(value, dict):
        # Kompakte Darstellung der haeufigsten Teilfelder
        for key in ("title", "surname", "family", "name", "label", "short_title"):
            if key in value:
                return _as_str(value[key])
        # Namen-Strukturen "family, given"
        fam = value.get("family") or value.get("surname")
        giv = value.get("given")
        if fam:
            return f"{fam}, {giv}" if giv else _as_str(fam)
    return str(value)


def _first_of(data: dict, *keys: str, default: Any = None) -> Any:
    for k in keys:
        if k in data and data[k] not in (None, ""):
            return data[k]
    return default


def _walk_strings(obj: Any) -> Iterable[str]:
    """Generator ueber alle String-Werte in einem JSON-Baum."""
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk_strings(v)
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _walk_strings(v)


_BIBKEY_RE = _re.compile(r"^[a-z][a-zA-Z0-9_]*[0-9][a-zA-Z0-9_]*$")


def _count_bibkey_mentions(obj: Any) -> dict[str, int]:
    """Zaehlt alle `bib_key`/`bibtex_key`-aehnlichen Werte in der Struktur.

    Erkennt (case-insensitive) Schluesselnamen:
      bib_key, bibtex_key, existing_bibtex_key, bestehender_key,
      key (wenn Value wie ein BibKey aussieht)

    BibKey-Muster: beginnt mit Kleinbuchstabe, enthaelt mindestens eine
    Ziffer (Jahresbestandteil), besteht aus [a-zA-Z0-9_]. Camel-Case-Keys
    wie `muelleroppliger2021paedDiagnostik` werden auf lowercase
    normalisiert, damit sie zu BibTeX-Konvention (case-insensitive) passen.

    Rueckgabe: { bibkey (lowercase) -> anzahl_vorkommen }.
    """
    counts: dict[str, int] = {}

    def _bump(k: str | None):
        if not k or not isinstance(k, str):
            return
        k = k.strip()
        if not _BIBKEY_RE.match(k):
            return
        norm = k.lower()
        counts[norm] = counts.get(norm, 0) + 1

    def _recurse(node: Any):
        if isinstance(node, dict):
            for k, v in node.items():
                lk = k.lower()
                if lk in ("bib_key", "bibtex_key", "existing_bibtex_key",
                          "bestehender_key"):
                    if isinstance(v, str):
                        _bump(v)
                elif lk == "key" and isinstance(v, str):
                    _bump(v)
                _recurse(v)
        elif isinstance(node, list):
            for v in node:
                _recurse(v)

    _recurse(obj)
    return counts


def _collect_relevance(obj: Any) -> dict[str, str]:
    """Findet eine Relevanz-pro-Frage-Map, wenn strukturell vorhanden.

    Erkennt zwei Muster:
    - "relevanzmatrix_pruefungsfragen": {"frage_1_...": {"relevanz":"HOCH",...}}
    - "by_primary_target": {"FW1": 12, "BW4": 3}
    """
    result: dict[str, str] = {}
    if not isinstance(obj, dict):
        return result

    rmx = obj.get("relevanzmatrix_pruefungsfragen")
    if isinstance(rmx, dict):
        for key, val in rmx.items():
            if not isinstance(val, dict):
                continue
            # Normalisierten Fragen-Key ableiten (frage_1_... -> F1)
            k_lower = key.lower()
            if k_lower.startswith("frage_"):
                digit = k_lower.split("_", 2)[1][:1]
                normal = f"F{digit}"
            elif k_lower.startswith("frage"):
                normal = key.upper()
            else:
                normal = key
            result[normal] = _as_str(val.get("relevanz") or val.get("rank") or val.get("label"))
        if result:
            return result

    summary = obj.get("summary", {})
    by_primary = summary.get("by_primary_target") if isinstance(summary, dict) else None
    if isinstance(by_primary, dict):
        for k, v in by_primary.items():
            result[str(k)] = str(v)

    return result


def _collect_integration_hints(obj: Any) -> list[dict]:
    """Sammelt Integration-/Einbau-Vorschlaege aus allen Stellen im JSON.

    Typische Felder:
    - "integration_vorschlag"
    - "integration_vorschlag_frage_N"
    - "tex_recommendation"
    - "placement" + "tex_recommendation" innerhalb "records[]"
    """
    hints: list[dict] = []

    def _push(location: str, text: str, frage: str | None = None):
        text = (text or "").strip()
        if text:
            hints.append({"location": location, "frage": frage, "text": text})

    def _recurse(node: Any, path: str = ""):
        if isinstance(node, dict):
            for k, v in node.items():
                lk = k.lower()
                full = f"{path}.{k}" if path else k
                if isinstance(v, str):
                    if lk == "integration_vorschlag":
                        _push(full, v)
                    elif lk.startswith("integration_vorschlag_frage_"):
                        frage = lk.rsplit("_", 1)[-1]
                        _push(full, v, frage=f"F{frage}")
                    elif lk in ("tex_snippet", "tex_einbau", "tex_example"):
                        _push(full, v)
                elif isinstance(v, (dict, list)):
                    _recurse(v, full)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                _recurse(v, f"{path}[{i}]")

    _recurse(obj)
    return hints


def _collect_issues(obj: Any) -> list[dict]:
    if not isinstance(obj, dict):
        return []
    issues = obj.get("issues")
    if isinstance(issues, list):
        return [i for i in issues if isinstance(i, dict)]
    return []


def _extract_bibtex(obj: Any) -> tuple[str | None, str | None]:
    """Liefert (vorgeschlagener_key, bibtex_raw)."""
    if not isinstance(obj, dict):
        return None, None
    cand_path_keys = ("bibtex_vorschlag", "biblatex_entry", "bibtex_entry",
                      "biblatex_vorschlag")
    for ck in cand_path_keys:
        node = obj.get(ck)
        if not isinstance(node, dict):
            continue
        key = node.get("key")
        raw = node.get("eintrag_roh") or node.get("raw")
        if not raw and isinstance(node.get("fields"), dict):
            raw = _render_bibtex_from_fields(
                node.get("type", "incollection"),
                key or "UNKNOWN",
                node["fields"],
            )
        return key, raw
    return None, None


def _render_bibtex_from_fields(entry_type: str, key: str, fields: dict) -> str:
    lines = [f"@{entry_type}{{{key},"]
    for fk, fv in fields.items():
        lines.append(f"  {fk:<10} = {{{fv}}},")
    lines.append("}")
    return "\n".join(lines)


# -----------------------------------------------------------------------
# Chapter-Level-Extraktion (Teil1 / Teil3 Handbuch-JSONs, T3-Erweiterung)
# -----------------------------------------------------------------------
def _format_pages(pages: Any) -> str | None:
    """Normalisiert verschiedene Seiten-Strukturen zu 'start--end'."""
    if isinstance(pages, dict):
        s = pages.get("start") or pages.get("page_start")
        e = pages.get("end")   or pages.get("page_end")
        if s and e:
            return f"{s}--{e}"
        if s:
            return str(s)
        return None
    if isinstance(pages, (int, str)) and str(pages).strip():
        return str(pages)
    return None


def _chapter_bibkey(chapter: dict) -> str | None:
    """Liest den normalisierten BibKey aus chapters[i].bibtex.key heraus.

    Akzeptiert CamelCase (z. B. 'muelleroppliger2021paedDiagnostik'
    aus Teil3) und gibt konsequent lowercase zurueck, weil BibTeX
    case-insensitive matcht und die Literatur/-Ordner lowercase sind.
    """
    bx = chapter.get("bibtex")
    if isinstance(bx, dict):
        key = bx.get("key")
        if isinstance(key, str) and key.strip():
            return key.strip().lower()
    return None


def _collect_chapter_relevance(chapter: dict) -> dict[str, str]:
    """Extrahiert die Relevanz-Angaben eines Chapter-Eintrags.

    Teil1 nutzt `primary_questions` (Plural), Teil3 `primary_question`
    (Singular). Beide werden unter Schluesseln 'priority', 'primary',
    'secondary' abgelegt.
    """
    rel = chapter.get("relevance")
    if not isinstance(rel, dict):
        return {}
    out: dict[str, str] = {}
    prio = rel.get("priority")
    if prio:
        out["priority"] = str(prio)
    prim = rel.get("primary_questions") or rel.get("primary_question")
    if prim:
        out["primary"] = (
            ", ".join(str(x) for x in prim) if isinstance(prim, list) else str(prim)
        )
    sec = rel.get("secondary_questions") or rel.get("secondary_question")
    if sec:
        out["secondary"] = (
            ", ".join(str(x) for x in sec) if isinstance(sec, list) else str(sec)
        )
    return out


def _collect_chapter_hints(chapter: dict) -> list[dict]:
    """Sammelt alle Integration-relevanten Textbausteine eines Kapitels.

    Deckt sowohl das Teil1-Schema (proposed_usage, recommendation_for_inti,
    memorable_quotes_for_oral_exam, key_ideas) als auch das Teil3-Schema
    (integration_hints, case_vignettes, content.summary) ab.
    """
    hints: list[dict] = []

    def _push(loc: str, text: str, frage: str | None = None, prefix: str = ""):
        text = (text or "").strip()
        if not text:
            return
        if prefix and not text.startswith(prefix):
            text = f"{prefix}{text}"
        hints.append({"location": loc, "frage": frage, "text": text})

    # (a) Teil3: integration_hints = list[str] oder list[dict]
    ih = chapter.get("integration_hints")
    if isinstance(ih, list):
        for i, h in enumerate(ih):
            loc = f"chapters[].integration_hints[{i}]"
            if isinstance(h, str):
                _push(loc, h)
            elif isinstance(h, dict):
                frage = h.get("question_id") or h.get("frage")
                text  = h.get("text") or h.get("content") or _as_str(h)
                _push(loc, text, frage=(str(frage) if frage else None))

    # (b) Teil1: proposed_usage = list[{question_id, tex_anchor, action, rationale}]
    pu = chapter.get("proposed_usage")
    if isinstance(pu, list):
        for i, u in enumerate(pu):
            if not isinstance(u, dict):
                continue
            qid    = u.get("question_id")
            anchor = u.get("tex_anchor") or ""
            action = u.get("action") or ""
            rationale = u.get("rationale") or ""
            parts = []
            if anchor:    parts.append(f"Anker: {anchor}")
            if action:    parts.append(action)
            if rationale: parts.append(f"(Grund: {rationale})")
            text = " — ".join(parts)
            _push(
                f"chapters[].proposed_usage[{i}]",
                text,
                frage=(str(qid) if qid else None),
            )

    # (c) recommendation_for_inti (Teil1) - strategische Empfehlung
    rec = chapter.get("recommendation_for_inti")
    if isinstance(rec, str):
        _push("chapters[].recommendation_for_inti", rec, prefix="[Empfehlung] ")

    # (d) memorable_quotes_for_oral_exam (Teil1) - Zitatvorschlaege fuer muendl. Pruefung
    mq = chapter.get("memorable_quotes_for_oral_exam")
    if isinstance(mq, list):
        for i, q in enumerate(mq):
            if isinstance(q, str):
                _push(
                    f"chapters[].memorable_quotes[{i}]",
                    q,
                    prefix="[Zitat muendl.] ",
                )

    # (e) key_ideas (Teil1) - Kernkonzepte des Kapitels
    ki = chapter.get("key_ideas")
    if isinstance(ki, list):
        for i, idea in enumerate(ki):
            if isinstance(idea, str):
                _push(
                    f"chapters[].key_ideas[{i}]",
                    idea,
                    prefix="[Kernidee] ",
                )

    # (f) case_vignettes (Teil3) - strukturierte Fallbeispiele (Aisha-Vignette etc.)
    cv = chapter.get("case_vignettes")
    if isinstance(cv, list):
        for i, vig in enumerate(cv):
            if not isinstance(vig, dict):
                continue
            name = vig.get("name", "?")
            age  = vig.get("age_years")
            ctx  = vig.get("context") or ""
            rel_s = (
                vig.get("relevance_to_case_s")
                or vig.get("relevance_to_fall_s")
                or ""
            )
            tex_anchor = vig.get("tex_anchor_question") or ""
            head = f"Fall-Vignette {name}"
            if age is not None:
                head += f", {age}\u202FJ."
            pieces = [head]
            if ctx:   pieces.append(_as_str(ctx))
            if rel_s: pieces.append(f"Relevanz fuer Fall S.: {_as_str(rel_s)}")
            _push(
                f"chapters[].case_vignettes[{i}]",
                " — ".join(pieces),
                frage=(str(tex_anchor) if tex_anchor else None),
                prefix="[Vignette] ",
            )

    # (g) content.summary (Teil3) - Kapitel-Abstract
    content = chapter.get("content")
    if isinstance(content, dict):
        summary = content.get("summary")
        if isinstance(summary, str):
            _push(
                "chapters[].content.summary",
                summary,
                prefix="[Abstract] ",
            )

    return hints


def _extract_chapter_befund(parent: TranskriptBefund,
                            chapter: dict) -> TranskriptBefund | None:
    """Erzeugt einen eigenstaendigen TranskriptBefund fuer ein Chapter.

    Rueckgabe None, wenn keine BibKey-Zuordnung vorliegt.
    """
    if not isinstance(chapter, dict):
        return None
    bibkey = _chapter_bibkey(chapter)
    if not bibkey:
        return None

    b = TranskriptBefund(source_file=parent.source_file, is_chapter=True)
    b.transcript_file = parent.transcript_file
    b.buch = parent.buch
    b.editors_authors = parent.editors_authors
    b.year = parent.year
    b.existing_bibkey = bibkey
    b.chapter_title   = _as_str(chapter.get("title") or chapter.get("titel"))
    b.chapter_authors = _as_str(chapter.get("authors") or chapter.get("autoren"))
    b.pages = _format_pages(chapter.get("pages"))
    # Titel fuer die Uebersicht klar kennzeichnen
    b.title = f"[Chapter] {b.chapter_title}" if b.chapter_title else "[Chapter]"

    b.relevance_per_question = _collect_chapter_relevance(chapter)
    b.integration_hints      = _collect_chapter_hints(chapter)
    return b


# -----------------------------------------------------------------------
# Normalisierung pro Datei
# -----------------------------------------------------------------------
def analyze_file(path: Path) -> list[TranskriptBefund]:
    data = json.loads(path.read_text(encoding="utf-8"))
    b = TranskriptBefund(source_file=path.name)

    meta = data.get("meta") if isinstance(data.get("meta"), dict) else {}
    document = data.get("document") if isinstance(data.get("document"), dict) else {}
    dataset_meta = data.get("dataset_meta") if isinstance(data.get("dataset_meta"), dict) else {}

    b.title = _as_str(_first_of(meta, "title", "zweck")
                      or _first_of(document, "title")
                      or _first_of(dataset_meta, "design_goal"))
    b.transcript_file = _as_str(_first_of(meta, "transkript_datei")) or None

    # Herkunftsbuch
    quelle_id = data.get("quelle_identifikation", {}) if isinstance(data.get("quelle_identifikation"), dict) else {}
    source     = data.get("source", {})             if isinstance(data.get("source"), dict)             else {}
    source_book= data.get("source_book", {})        if isinstance(data.get("source_book"), dict)        else {}

    # Buch-Titel + Herausgeber
    if source_book:
        b.buch = _as_str(source_book.get("title"))
        eds = source_book.get("editors") or source_book.get("authors")
        b.editors_authors = _as_str(eds)
        b.year = source_book.get("year")
        b.existing_bibkey = source_book.get("bibtex_key") or source_book.get("bibtex_key_status")
        if source_book.get("bibtex_key"):
            b.existing_bibkey = source_book["bibtex_key"]
    elif quelle_id:
        sb = quelle_id.get("sammelband") or {}
        b.buch = _as_str(sb.get("titel"))
        b.editors_authors = _as_str(sb.get("herausgeber"))
        b.year = sb.get("jahr")
        bbex = quelle_id.get("bezug_zu_bestehender_bib") or {}
        b.existing_bibkey = bbex.get("bestehender_key")
    elif source:
        # Teil3-Schema: source ist selbst schon der Band (enthaelt title/
        # editors/year). Aeltere Schemas haben stattdessen source.book.
        book = source.get("book") if isinstance(source.get("book"), dict) else source
        b.buch = _as_str(book.get("title"))
        b.editors_authors = _as_str(book.get("editors"))
        b.year = book.get("year")

    # Kapitel
    ch = (source.get("chapter") if isinstance(source.get("chapter"), dict) else None) \
         or (quelle_id.get("kapitel") if isinstance(quelle_id.get("kapitel"), dict) else None)
    if ch:
        b.chapter_title = _as_str(ch.get("title") or ch.get("titel"))
        aut = ch.get("authors") or ch.get("autor") or ch.get("autoren")
        b.chapter_authors = _as_str(aut)
        ps = ch.get("page_start") or ch.get("pages") or ch.get("seitenbereich_transkriptangabe")
        pe = ch.get("page_end")
        if isinstance(ps, int) and isinstance(pe, int):
            b.pages = f"{ps}--{pe}"
        elif ps:
            b.pages = _as_str(ps)

    # Vorgeschlagener BibKey / Eintrag
    key, raw = _extract_bibtex(data)
    if key:
        b.proposed_bibkey = key
    if raw:
        b.proposed_bibtex_raw = raw

    # Falls nur source.biblatex_entry vorhanden, den Key sammeln
    if not b.proposed_bibkey and isinstance(source.get("biblatex_entry"), dict):
        be = source["biblatex_entry"]
        b.proposed_bibkey = be.get("key")

    # Relevanz + Integration
    b.relevance_per_question = _collect_relevance(data)
    b.integration_hints = _collect_integration_hints(data)
    b.issues = _collect_issues(data)

    # Datensatz-Zaehler (wenn records[] vorhanden)
    records = data.get("records")
    if isinstance(records, list):
        b.records_count = len(records)

    # BibKey-Vorkommnisse mit Haeufigkeiten (Kernsignal!)
    b.bibkey_mentions = _count_bibkey_mentions(data)

    # Chapter-Befunde extrahieren (T3): Teil1/Teil3 Multi-Chapter-JSONs.
    # Jedes Kapitel bekommt seinen eigenen BibKey und einen reichen
    # Integration-Hint-Block. Die Chapter-BibKeys werden aus den generischen
    # `bibkey_mentions` des Haupt-Befunds entfernt, damit sie nicht doppelt
    # (einmal als "mentioned_existing", einmal als "chapter_main") im Index
    # erscheinen.
    chapter_befunde: list[TranskriptBefund] = []
    chapters = data.get("chapters")
    if isinstance(chapters, list):
        for ch in chapters:
            cb = _extract_chapter_befund(b, ch)
            if cb is None:
                continue
            chapter_befunde.append(cb)
            b.bibkey_mentions.pop(cb.existing_bibkey, None)

    return [b, *chapter_befunde]


# -----------------------------------------------------------------------
# Aggregation und Output
# -----------------------------------------------------------------------
def _md_table_row(*cells: str) -> str:
    return "| " + " | ".join((c or "").replace("\n", " ").replace("|", "\\|") for c in cells) + " |"


def build_markdown(befunde: list[TranskriptBefund], existing_keys: set[str]) -> str:
    lines: list[str] = []
    lines.append("# Transkripte-Uebersicht (Verortung im Lerndokument)")
    lines.append("")
    lines.append(
        "Dieser Bericht aggregiert die JSON-Verortungen aus "
        "`MPV/Literatur/Transkripte/einordnung/`. Die Transkripte sind **kuratierte "
        "Zitatstellen aus Originalquellen** (Handbuch Begabung, Renzulli/Reis, "
        "Trautmann u. a.) und sollten bei inhaltsgleichen Belegstellen **bevorzugt "
        "verwendet werden** gegenueber heuristischen Suchergebnissen."
    )
    lines.append("")
    lines.append(f"- Quellordner: `MPV/Literatur/Transkripte/einordnung/`")
    lines.append(f"- Anzahl JSON-Dateien: **{len(befunde)}**")
    lines.append(f"- Existierende BibKeys in `Quellen.bib`: **{len(existing_keys)}**")
    lines.append("")

    # --- Uebersichtstabelle -----------------------------------------
    lines.append("## 1. Uebersicht")
    lines.append("")
    lines.append(_md_table_row(
        "JSON", "Titel / Zweck", "Buch / Quelle",
        "Kapitel", "BibKey bestehend", "BibKey Vorschlag",
        "Integration-Hints",
    ))
    lines.append(_md_table_row("---", "---", "---", "---", "---", "---", "---"))
    for b in befunde:
        lines.append(_md_table_row(
            f"`{b.source_file}`",
            (b.title[:80] + "...") if len(b.title) > 80 else b.title,
            f"{b.buch} ({b.year})" if b.year else b.buch,
            f"{b.chapter_title} ({b.pages})" if b.chapter_title and b.pages else (b.chapter_title or ""),
            f"`{b.existing_bibkey}`" if b.existing_bibkey else "",
            f"`{b.proposed_bibkey}`" if b.proposed_bibkey else "",
            str(len(b.integration_hints)),
        ))
    lines.append("")

    # --- Neue BibKey-Vorschlaege -----------------------------------
    new_keys = [b for b in befunde if b.proposed_bibkey and b.proposed_bibkey != b.existing_bibkey]
    if new_keys:
        lines.append("## 2. Vorgeschlagene neue BibKeys (vorrangig @incollection)")
        lines.append("")
        lines.append(
            "Die Transkripte schlagen in mehreren Faellen **praezise "
            "Einzelbeitraege** innerhalb bestehender Sammelbaende vor. Diese "
            "sollten in `Quellen.bib` ergaenzt werden, damit konkrete Kapitel-"
            "Aussagen nicht ungenau dem ganzen Herausgeberband zugeordnet sind."
        )
        lines.append("")
        for b in new_keys:
            lines.append(f"### `{b.proposed_bibkey}` (aus `{b.source_file}`)")
            lines.append("")
            if b.chapter_title:
                lines.append(f"- **Kapitel:** {b.chapter_title}")
            if b.chapter_authors:
                lines.append(f"- **Autor:innen:** {b.chapter_authors}")
            if b.pages:
                lines.append(f"- **Seiten:** {b.pages}")
            if b.buch:
                lines.append(f"- **In:** {b.buch} ({b.year or '?'}) — Hrsg. {b.editors_authors}")
            if b.existing_bibkey:
                lines.append(
                    f"- **Status:** ergaenzt `{b.existing_bibkey}` "
                    f"(Sammelband-BibKey) durch @incollection-Variante"
                )
            if b.proposed_bibtex_raw:
                lines.append("")
                lines.append("```bibtex")
                lines.append(b.proposed_bibtex_raw.strip())
                lines.append("```")
            lines.append("")

    # --- Pro bestehenden BibKey ------------------------------------
    by_existing: dict[str, list[TranskriptBefund]] = defaultdict(list)
    for b in befunde:
        key = b.existing_bibkey or ""
        if key:
            by_existing[key].append(b)
    if by_existing:
        lines.append("## 3. Transkripte pro bestehendem BibKey")
        lines.append("")
        for key in sorted(by_existing):
            lines.append(f"### `{key}`")
            for b in by_existing[key]:
                src_folder = LITERATUR / key
                has_folder = src_folder.is_dir()
                existence = "✅ Literatur-Ordner vorhanden" if has_folder else "❌ Kein Ordner unter Literatur/"
                lines.append(f"- `{b.source_file}` — {b.title[:80]}")
                lines.append(f"  - Kapitel: {b.chapter_title or '—'} ({b.pages or '?'})")
                lines.append(f"  - Integration-Hints: {len(b.integration_hints)}; Issues: {len(b.issues)}")
                lines.append(f"  - Zielordner: {existence}")
            lines.append("")

    # --- Issues-Sammlung -------------------------------------------
    all_issues: list[tuple[str, dict]] = []
    for b in befunde:
        for iss in b.issues:
            all_issues.append((b.source_file, iss))
    if all_issues:
        lines.append("## 4. Offene Issues / Verifikationsauftraege")
        lines.append("")
        for src, iss in all_issues:
            sev = iss.get("severity", "info")
            pid = iss.get("issue_id", "—")
            typ = iss.get("problem_type", "—")
            obs = _as_str(iss.get("observation"))
            rec = _as_str(iss.get("recommendation"))
            lines.append(f"### [{sev.upper()}] {pid} — {typ} ({src})")
            lines.append("")
            lines.append(f"- **Beobachtung:** {obs}")
            lines.append(f"- **Empfehlung:** {rec}")
            lines.append("")

    # --- BibKey-Haeufigkeiten pro Transkript-JSON ------------------
    # Aggregiert: bibkey -> { source_file -> count }
    agg: dict[str, dict[str, int]] = defaultdict(dict)
    for b in befunde:
        for k, c in b.bibkey_mentions.items():
            agg[k][b.source_file] = c

    known   = {k: v for k, v in agg.items() if k in existing_keys}
    unknown = {k: v for k, v in agg.items() if k not in existing_keys}

    lines.append("## 5. BibKey-Erwaehnungen pro Transkript (Kernsignal)")
    lines.append("")
    lines.append(
        "Die kuratierten Transkripte enthalten pro Zitatstelle einen `bib_key`. "
        "Haeufigkeit = Anzahl Zitatstellen, an denen der BibKey im Lerndokument "
        "verwendet werden soll. **Hohe Zahlen = hoher Transkript-Nutzen** bei "
        "der Verifikation dieser Quelle."
    )
    lines.append("")

    if known:
        lines.append("### 5a. Bestehende BibKeys (vorhanden in `Quellen.bib`)")
        lines.append("")
        lines.append(_md_table_row("BibKey", "Gesamt", "Pro JSON (Datei : Anzahl)"))
        lines.append(_md_table_row("---", "---", "---"))
        for k in sorted(known, key=lambda x: (-sum(known[x].values()), x)):
            total = sum(known[k].values())
            per = "; ".join(f"{src.replace('.json', '')}:{n}"
                           for src, n in sorted(known[k].items(),
                                                key=lambda kv: -kv[1]))
            lines.append(_md_table_row(f"`{k}`", str(total), per))
        lines.append("")

    if unknown:
        lines.append("### 5b. NEUE BibKeys (nicht in `Quellen.bib` - muessen ergaenzt werden)")
        lines.append("")
        lines.append(
            "Der Analyst hat diese Keys vorgeschlagen, sie fehlen aber noch in "
            "`Quellen.bib`. Sie entsprechen meist **Einzelbeitraegen aus Sammel-"
            "baenden** (`@incollection`) - genau das gewuenschte Zitations-"
            "Granularitaetsniveau."
        )
        lines.append("")
        lines.append(_md_table_row("Neuer BibKey", "Gesamt", "Pro JSON (Datei : Anzahl)"))
        lines.append(_md_table_row("---", "---", "---"))
        for k in sorted(unknown, key=lambda x: (-sum(unknown[x].values()), x)):
            total = sum(unknown[k].values())
            per = "; ".join(f"{src.replace('.json', '')}:{n}"
                           for src, n in sorted(unknown[k].items(),
                                                key=lambda kv: -kv[1]))
            lines.append(_md_table_row(f"`{k}`", str(total), per))
        lines.append("")

    # --- Hinweise / Notes ------------------------------------------
    any_notes = [(b.source_file, n) for b in befunde for n in b.notes]
    if any_notes:
        lines.append("## 6. Zusatzhinweise aus den JSONs")
        lines.append("")
        for src, note in any_notes:
            lines.append(f"- **{src}:** {note}")
        lines.append("")

    return "\n".join(lines) + "\n"


def build_index(befunde: list[TranskriptBefund],
                existing_keys: set[str]) -> dict:
    """Pro BibKey (existing + proposed + mentions) eine Liste der relevanten
    Transkript-Befunde als JSON-Index fuer spaetere Skripte (z. B.
    Integration in verified_quotes.md).
    """
    idx: dict[str, list[dict]] = defaultdict(list)
    for b in befunde:
        base_entry = {
            "source_file": b.source_file,
            "title": b.title,
            "transcript_file": b.transcript_file,
            "buch": b.buch,
            "chapter_title": b.chapter_title,
            "chapter_authors": b.chapter_authors,
            "pages": b.pages,
            "year": b.year,
            "relevance_per_question": b.relevance_per_question,
            "integration_hints_count": len(b.integration_hints),
            "integration_hints": b.integration_hints[:20],  # Kappen
            "issues_count": len(b.issues),
        }
        # Top-Level-Verknuepfung (Haupt-BibKey der Datei).
        # Chapter-Befunde (is_chapter=True) bekommen eine eigene Rolle,
        # damit `integrate_transkripte.py` sie als "Haupt-Kapitel aus
        # Multi-Chapter-Transkript" rendern kann.
        if b.existing_bibkey:
            role = "chapter_main" if b.is_chapter else "existing_main"
            idx[b.existing_bibkey].append({**base_entry, "role": role})
        if b.proposed_bibkey and b.proposed_bibkey != b.existing_bibkey:
            idx[b.proposed_bibkey].append({
                **base_entry,
                "role": "proposed_new_main",
                "proposed_bibtex": b.proposed_bibtex_raw,
            })
        # BibKey-Erwaehnungen innerhalb des JSONs (Zitatstellen)
        for k, cnt in b.bibkey_mentions.items():
            if k == b.existing_bibkey or k == b.proposed_bibkey:
                continue  # schon via Top-Level
            role = "mentioned_existing" if k in existing_keys else "mentioned_new"
            idx[k].append({
                **base_entry,
                "role": role,
                "mention_count": cnt,
            })
    return {
        "schema_version": "1.1",
        "bibkey_to_transkripte": dict(idx),
    }


# -----------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Aggregiert Transkript-Verortungs-JSONs zu einem "
                    "Markdown-Bericht + Index.",
    )
    p.add_argument("--json-dir", type=Path, default=DEFAULT_JSON_DIR,
                   help=f"Quellverzeichnis (Default: {DEFAULT_JSON_DIR})")
    p.add_argument("--out-md", type=Path, default=OUT_OVERVIEW_MD,
                   help=f"Markdown-Ausgabe (Default: {OUT_OVERVIEW_MD})")
    p.add_argument("--out-index", type=Path, default=OUT_INDEX_JSON,
                   help=f"Index-JSON (Default: {OUT_INDEX_JSON})")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    json_dir: Path = args.json_dir
    if not json_dir.is_dir():
        print(f"[Fehler] Quellverzeichnis nicht gefunden: {json_dir}",
              file=sys.stderr)
        return 2

    files = sorted(p for p in json_dir.glob("*.json") if p.is_file())
    if not files:
        print(f"[Fehler] Keine JSON-Dateien in {json_dir}", file=sys.stderr)
        return 2

    print(f"analyze_transkripte.py")
    print(f"  Quelle: {json_dir}")
    print(f"  JSONs : {len(files)}")
    print()

    existing_keys = load_existing_bibkeys(BIB_PATH)
    print(f"  BibKeys in {BIB_PATH.name}: {len(existing_keys)}")
    print()

    befunde: list[TranskriptBefund] = []
    chapter_count_by_file: dict[str, int] = {}
    for f in files:
        print(f"  [read] {f.name}")
        try:
            produced = analyze_file(f)
            befunde.extend(produced)
            n_chapter = sum(1 for x in produced if x.is_chapter)
            if n_chapter:
                chapter_count_by_file[f.name] = n_chapter
        except Exception as exc:
            print(f"     !! Fehler beim Parsen: {exc}")
    if chapter_count_by_file:
        print()
        print("  Chapter-Befunde extrahiert (T3):")
        for name, n in chapter_count_by_file.items():
            print(f"    {n:3d}x  {name}")
    print()

    md = build_markdown(befunde, existing_keys)
    args.out_md.write_text(md, encoding="utf-8")
    print(f"  [OK] -> {args.out_md}  ({len(md)} Zeichen)")

    idx = build_index(befunde, existing_keys)
    args.out_index.parent.mkdir(parents=True, exist_ok=True)
    args.out_index.write_text(
        json.dumps(idx, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    keys = idx["bibkey_to_transkripte"].keys()
    known   = sum(1 for k in keys if k in existing_keys)
    unknown = sum(1 for k in keys if k not in existing_keys)
    print(f"  [OK] -> {args.out_index}  "
          f"({len(list(keys))} BibKeys: {known} existierend, {unknown} NEU)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
