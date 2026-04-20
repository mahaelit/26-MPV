#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fragen_abstimmung.py - Stimmt pro Pruefungsfrage die Quellen-Abdeckung ab.

Die Arbeit mpv.tex / mpv_abgabedokument.tex gliedert sich in 5 Pruefungsfragen
(\section{Frage 1 (...): ...} bis \section{Frage 5 (...): ...}). Jede Frage hat
im Anschluss einen \subsection{Kernliteratur zu Frage N}-Block mit kuratierten
Hauptquellen und Seitenangaben, sowie viele Cite-Stellen im Fliesstext.

Dieses Skript baut aus mpv.tex einen strategischen Report, der pro Frage zeigt:
  1. Fragestellung (aus quote-Umgebung nach der Section)
  2. Kernliteratur-Matrix (BibKey | Titel | S. laut Autor | Ampel | Splits)
  3. Weitere Cites im Fliesstext (BibKey | Anzahl | Ampel)
  4. Luecken (ROT-Quellen mit Cite-Zahl >=2 in dieser Frage)
  5. Seitenbilanz (geplante vs. verfuegbare Seiten)

Aufruf:
  python fragen_abstimmung.py

Output: FRAGEN_ABSTIMMUNG.md
"""
from __future__ import annotations
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Wiederverwendung bestehender Module
import cite_context as cc
from build_kompendium import parse_bib, coverage_for_key, ampel, clean_bib

try:
    import claim_split_match as csm
    HAS_CSM = True
except Exception:
    HAS_CSM = False

HERE = Path(__file__).resolve().parent
LIT = HERE / "Literatur"
TEX_FILES = [
    (HERE / "mpv.tex", "L", "Lerndokument"),
    (HERE / "mpv_abgabedokument.tex", "A", "Abgabedokument"),
]
OUT = HERE / "FRAGEN_ABSTIMMUNG.md"

# =============================================================================
# Frage- und Kernliteratur-Erkennung
# =============================================================================

FRAGE_SECTION_RE = re.compile(
    r"^\\section\*?\s*\{\s*Frage\s+(?P<num>\d+)\s*(?:\((?P<kuerzel>[^)]*)\))?\s*:?\s*(?P<title>[^}]+?)\}",
    re.MULTILINE,
)
SECTION_ANY_RE = re.compile(r"^\\section\*?\s*\{(?P<title>[^}]+)\}", re.MULTILINE)
KERN_SUBSEC_RE = re.compile(
    r"^\\subsection\*?\s*\{\s*Kernliteratur\s+zu\s+Frage\s+(\d+)\s*\}",
    re.MULTILINE | re.IGNORECASE,
)
SUBSEC_ANY_RE = re.compile(r"^\\subsection\*?\s*\{", re.MULTILINE)

# Kernliteratur-Eintraege: \item[\cite{KEY}] Freitext. Kapitelangabe. (ca.~NN\,S.)
KERN_ITEM_RE = re.compile(
    r"\\item\s*\[\s*\\cite\s*\{(?P<key>[^}]+)\}\s*\]"
    r"(?P<body>.*?)"
    r"\(\s*(?:ca\.?\s*~?|~)?(?P<pages>\d+)\s*[~\\,\s]*S\.?\s*\)",
    re.DOTALL,
)

# Fragestellung: quote-Umgebung direkt nach \section{Frage N}
FRAGE_QUOTE_RE = re.compile(
    r"\\begin\{quote\}(?P<q>.+?)\\end\{quote\}",
    re.DOTALL,
)

# =============================================================================
# TeX-Parsing
# =============================================================================

def parse_fragen(tex_path: Path) -> list[dict[str, Any]]:
    """Liefert pro \section{Frage N} ein Dict mit den Boundaries und Inhalt.

    Keys pro Frage:
      num, kuerzel, title, tex_file, line_start, line_end, offset_start,
      offset_end, body, kernlit_start, kernlit_end, kernlit_body, fliesstext
    """
    if not tex_path.exists():
        return []
    text = tex_path.read_text(encoding="utf-8")
    clean = cc.prepare_tex(text)
    starts = cc._line_index(text)

    # Alle \section-Offsets (jede Art)
    all_sections = [(m.start(), m.end(), m.group("title"))
                    for m in SECTION_ANY_RE.finditer(clean)]

    fragen = []
    for m in FRAGE_SECTION_RE.finditer(clean):
        num = int(m.group("num"))
        kuerzel = (m.group("kuerzel") or "").strip()
        # Titel kann im TeX ueber mehrere Zeilen umbrochen sein -> Whitespace normalisieren
        title = re.sub(r"\s+", " ", m.group("title")).strip()
        off_start = m.end()
        # Ende: Start der naechsten beliebigen \section
        off_end = len(text)
        for s_start, s_end, _title in all_sections:
            if s_start > m.start():
                off_end = s_start
                break

        body = text[off_start:off_end]
        body_clean = clean[off_start:off_end]

        line_start = cc._line_of(m.start(), starts)
        line_end = cc._line_of(off_end - 1, starts) if off_end > 0 else line_start

        # Fragestellung extrahieren
        qm = FRAGE_QUOTE_RE.search(body)
        frage_text = ""
        if qm:
            q = qm.group("q")
            # TeX-Artefakte entfernen
            q = re.sub(r"\\itshape|\\bfseries|\\upshape", "", q)
            q = re.sub(r"\\(textit|emph|textbf|enquote)\{([^}]*)\}", r"\2", q)
            q = re.sub(r"\s+", " ", q).strip()
            frage_text = q

        # Kernliteratur-Subsection finden
        km = KERN_SUBSEC_RE.search(body_clean)
        kern_body = ""
        kern_off_start = kern_off_end = 0
        if km:
            kern_off_start = km.end()
            # Ende: naechste \subsection innerhalb des body
            sub_any = SUBSEC_ANY_RE.search(body_clean, pos=kern_off_start)
            kern_off_end = sub_any.start() if sub_any else len(body_clean)
            kern_body = body[kern_off_start:kern_off_end]

        fragen.append({
            "num": num,
            "kuerzel": kuerzel,
            "title": title,
            "tex_file": tex_path.name,
            "line_start": line_start,
            "line_end": line_end,
            "offset_start": off_start,
            "offset_end": off_end,
            "body": body,
            "frage_text": frage_text,
            "kern_body": kern_body,
            "kern_off_start": off_start + kern_off_start,
            "kern_off_end": off_start + kern_off_end,
        })
    return fragen


def parse_kernliteratur(kern_body: str) -> list[dict[str, Any]]:
    """Parst die \item[\cite{KEY}] ... (ca. NN S.) Eintraege."""
    out = []
    for m in KERN_ITEM_RE.finditer(kern_body):
        key = m.group("key").strip()
        body = m.group("body").strip()
        pages = int(m.group("pages"))
        # Titel/Beschreibung aufraeumen
        desc = re.sub(r"\s+", " ", body)
        desc = re.sub(r"\\emph\{([^}]+)\}", r"\1", desc)
        desc = re.sub(r"\\textit\{([^}]+)\}", r"\1", desc)
        desc = desc.strip(" ,.;:")
        out.append({"key": key, "desc": desc, "pages_planned": pages})
    return out


def extract_cites_in_range(all_cites: list[cc.Citation],
                           tex_file: str,
                           off_start: int,
                           off_end: int,
                           tex_path: Path) -> list[cc.Citation]:
    """Filter: nur Cites in [off_start, off_end) der gegebenen TeX-Datei.

    all_cites speichert nur Zeilen, daher rechnen wir offsetbasiert neu.
    """
    # Cite-Extraktion fuer die TeX-Datei neu mit Offsets
    if not tex_path.exists():
        return []
    text = tex_path.read_text(encoding="utf-8")
    clean = cc.prepare_tex(text)
    starts = cc._line_index(text)
    hits: list[cc.Citation] = []
    for mm in cc.CITE_PATTERN.finditer(clean):
        if mm.start() < off_start or mm.start() >= off_end:
            continue
        keys_field = mm.group("keys")
        cmd = mm.group("cmd")
        opt1 = mm.group("opt1") or ""
        opt2 = mm.group("opt2") or ""
        pre, post = "", ""
        if opt1 and opt2:
            pre, post = opt1[1:-1].strip(), opt2[1:-1].strip()
        elif opt1:
            post = opt1[1:-1].strip()
        ctx_a = max(0, mm.start() - cc.CONTEXT_CHARS)
        ctx_b = min(len(text), mm.end() + cc.CONTEXT_CHARS)
        line = cc._line_of(mm.start(), starts)
        raw_cite = text[mm.start():mm.end()]
        ctx_before = cc._squash(text[ctx_a:mm.start()])
        ctx_after = cc._squash(text[mm.end():ctx_b])
        for key in (k.strip() for k in keys_field.split(",")):
            if not key or "." in key or len(key) < 3:
                continue
            hits.append(cc.Citation(
                bibkey=key, src_label=tex_file, line=line, cmd=cmd,
                pre=pre, post=post, raw=raw_cite,
                context_before=ctx_before, context_after=ctx_after,
            ))
    return hits

# =============================================================================
# Rendering
# =============================================================================

AMPEL_EMOJI = {
    "GRUEN": "🟢", "GELB+": "🟡", "GELB": "🟡", "GELB-K": "🟠", "ROT": "🔴",
}


def fmt_ampel(a: str) -> str:
    return f"{AMPEL_EMOJI.get(a, '⚪')} `{a}`"


def render_report(fragen_per_file: dict[str, list[dict[str, Any]]]) -> str:
    bib = parse_bib()
    lines: list[str] = []
    lines.append("# Quellen-Abstimmung nach Pruefungsfragen")
    lines.append("")
    lines.append("Automatisch erzeugt durch `fragen_abstimmung.py`. Nicht manuell editieren.")
    lines.append("")
    lines.append("**Quelle:** `mpv.tex` (Lerndokument). `mpv_abgabedokument.tex` nur zur Gegenprobe verwendet.")
    lines.append("")

    # Primary: mpv.tex
    fragen = fragen_per_file.get("mpv.tex", [])
    if not fragen:
        lines.append("_Keine Fragen-Sections in mpv.tex gefunden._")
        return "\n".join(lines)

    # Caches
    cov_cache: dict[str, dict] = {}
    splits_cache: dict[str, list] = {}

    def get_cov(k: str) -> dict:
        if k not in cov_cache:
            cov_cache[k] = coverage_for_key(k)
            if HAS_CSM and cov_cache[k].get("n_excerpts", 0) > 0:
                try:
                    splits_cache[k] = csm.load_splits(k)
                except Exception:
                    splits_cache[k] = []
        return cov_cache[k]

    # =====================================================================
    # Zusammenfassungs-Matrix
    # =====================================================================
    lines.append("## Uebersicht")
    lines.append("")
    lines.append("| # | Frage | Kernlit | Cites im Text | 🟢 | 🟡+/🟡 | 🟠 | 🔴 | Seiten geplant | Seiten verfuegbar |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")

    per_frage_summary = []

    for fr in fragen:
        kernlit = parse_kernliteratur(fr["kern_body"])
        # Fliesstext-Cites (ausserhalb Kernliteratur-Block)
        fliess_cites = []
        all_in_frage = extract_cites_in_range(
            [], fr["tex_file"], fr["offset_start"], fr["offset_end"],
            HERE / fr["tex_file"],
        )
        for c in all_in_frage:
            if fr["kern_off_start"] <= _offset_of(c, fr["tex_file"]) < fr["kern_off_end"]:
                continue
            fliess_cites.append(c)

        # Stats
        kern_keys = {k["key"] for k in kernlit}
        fliess_keys_all = [c.bibkey for c in fliess_cites]
        fliess_keys_unique = set(fliess_keys_all)
        all_keys = kern_keys | fliess_keys_unique

        # Ampel-Counter ueber alle unique Keys dieser Frage
        ampel_cnt = Counter()
        for k in all_keys:
            ampel_cnt[ampel(get_cov(k))] += 1

        pages_planned = sum(k["pages_planned"] for k in kernlit)
        pages_available = 0
        for k in kern_keys:
            cov = get_cov(k)
            if cov["has_pdf"] and not cov["short_pdf"]:
                # Geplante Seiten werden vom PDF bedient
                pages_available += next((kk["pages_planned"] for kk in kernlit if kk["key"] == k), 0)
            elif cov["has_pdf"] and cov["short_pdf"]:
                pages_available += min(cov["pdf_pages"],
                                       next((kk["pages_planned"] for kk in kernlit if kk["key"] == k), 0))

        title_short = fr["title"][:50] + ("…" if len(fr["title"]) > 50 else "")
        gelb_sum = ampel_cnt.get("GELB", 0) + ampel_cnt.get("GELB+", 0)
        lines.append(
            f"| {fr['num']} | {title_short} | "
            f"{len(kernlit)} | {len(fliess_cites)} | "
            f"{ampel_cnt.get('GRUEN', 0)} | {gelb_sum} | "
            f"{ampel_cnt.get('GELB-K', 0)} | {ampel_cnt.get('ROT', 0)} | "
            f"{pages_planned} | {pages_available} |"
        )
        per_frage_summary.append({
            "fr": fr, "kernlit": kernlit,
            "fliess_cites": fliess_cites,
            "ampel_cnt": ampel_cnt,
            "pages_planned": pages_planned,
            "pages_available": pages_available,
        })

    total_planned = sum(s["pages_planned"] for s in per_frage_summary)
    total_available = sum(s["pages_available"] for s in per_frage_summary)
    lines.append(
        f"| **Σ** | — | "
        f"**{sum(len(s['kernlit']) for s in per_frage_summary)}** | "
        f"**{sum(len(s['fliess_cites']) for s in per_frage_summary)}** | "
        f"— | — | — | — | "
        f"**{total_planned}** | **{total_available}** |"
    )
    lines.append("")
    lines.append("> Seiten-Spalten: _geplant_ = Summe der Seitenangaben in den Kernliteratur-Blöcken. "
                 "_verfuegbar_ = davon durch vorhandene PDFs gedeckt (vollständiges PDF oder Kapitel-Split).")
    lines.append("")

    # =====================================================================
    # Pro-Frage-Detail
    # =====================================================================
    for s in per_frage_summary:
        fr = s["fr"]
        kernlit = s["kernlit"]
        fliess_cites = s["fliess_cites"]

        lines.append("---")
        lines.append("")
        lines.append(f"## Frage {fr['num']}: {fr['title']}")
        lines.append("")
        if fr["kuerzel"]:
            lines.append(f"_Kategorien: **{fr['kuerzel']}**_")
            lines.append("")
        lines.append(f"**Pfad in TeX:** `mpv.tex` Zeile {fr['line_start']}-{fr['line_end']}  "
                     f"([`mpv.tex#L{fr['line_start']}`](mpv.tex#L{fr['line_start']}))")
        lines.append("")
        if fr["frage_text"]:
            lines.append(f"> **Fragestellung:** {fr['frage_text']}")
            lines.append("")

        # --- Kernliteratur ---
        lines.append(f"### Kernliteratur ({len(kernlit)} Quellen, {s['pages_planned']} S. geplant, {s['pages_available']} S. verfuegbar)")
        lines.append("")
        if not kernlit:
            lines.append("_Keine Kernliteratur-Eintraege erkannt._")
            lines.append("")
        else:
            lines.append("| Ampel | BibKey | Autor (Jahr) | Titel/Kapitel | S. geplant | Splits | Fliesstext-Cites |")
            lines.append("|---|---|---|---|---:|---:|---:|")
            for kl in kernlit:
                k = kl["key"]
                cov = get_cov(k)
                bib_e = bib.get(k, {})
                title = clean_bib(bib_e.get("title", ""))[:60]
                year = bib_e.get("year", "?")
                author = clean_bib(bib_e.get("author") or bib_e.get("editor") or "")[:35]
                n_fliess = sum(1 for c in fliess_cites if c.bibkey == k)
                splits_n = cov.get("n_excerpts", 0)
                dossier_link = f"[`{k}`](Literatur/{k}/verified_quotes.md)"
                lines.append(
                    f"| {fmt_ampel(ampel(cov))} | {dossier_link} | {author} ({year}) | "
                    f"{kl['desc'][:60]} | {kl['pages_planned']} | {splits_n} | {n_fliess} |"
                )
            lines.append("")

        # --- Fliesstext-Cites ---
        fliess_by_key = defaultdict(list)
        for c in fliess_cites:
            fliess_by_key[c.bibkey].append(c)

        non_kern_keys = [k for k in fliess_by_key if k not in {kl["key"] for kl in kernlit}]
        if non_kern_keys:
            lines.append(f"### Zusaetzliche Cites im Fliesstext ({len(non_kern_keys)} weitere Quellen, {sum(len(fliess_by_key[k]) for k in non_kern_keys)} Stellen)")
            lines.append("")
            # Sortiere: zuerst nach Ampel (ROT oben, GRUEN unten), dann nach Cite-Anzahl
            ampel_order = {"ROT": 0, "GELB-K": 1, "GELB": 2, "GELB+": 3, "GRUEN": 4}
            sorted_keys = sorted(
                non_kern_keys,
                key=lambda k: (ampel_order.get(ampel(get_cov(k)), 5),
                               -len(fliess_by_key[k]), k)
            )
            lines.append("| Ampel | BibKey | Autor (Jahr) | Cites | Erste Zeile in TeX |")
            lines.append("|---|---|---|---:|---:|")
            for k in sorted_keys:
                cov = get_cov(k)
                bib_e = bib.get(k, {})
                year = bib_e.get("year", "?")
                author = clean_bib(bib_e.get("author") or bib_e.get("editor") or "")[:35]
                cites_here = fliess_by_key[k]
                first_line = min(c.line for c in cites_here)
                dossier = f"[`{k}`](Literatur/{k}/verified_quotes.md)"
                lines.append(
                    f"| {fmt_ampel(ampel(cov))} | {dossier} | {author} ({year}) | "
                    f"{len(cites_here)} | `mpv.tex:{first_line}` |"
                )
            lines.append("")

        # --- Luecken-Analyse ---
        gaps = []
        for k in (set(kl["key"] for kl in kernlit) | set(fliess_by_key.keys())):
            a = ampel(get_cov(k))
            if a in ("ROT", "GELB-K"):
                n_kern = sum(1 for kl in kernlit if kl["key"] == k)
                n_fliess = len(fliess_by_key.get(k, []))
                if n_kern or n_fliess >= 2:
                    gaps.append((a, k, n_kern, n_fliess))
        if gaps:
            lines.append("### Kritische Luecken")
            lines.append("")
            for a, k, n_kern, n_fliess in sorted(gaps, key=lambda x: (x[0] != "ROT", -x[2] - x[3])):
                role = "Kernlit" if n_kern else "Fliesstext"
                cites_info = f"Kernlit={n_kern}, Fliesstext={n_fliess}"
                cov = get_cov(k)
                hint = ""
                if a == "ROT":
                    # Hat diese Quelle einen Parent via incollection?
                    parent_marker = LIT / k / ".from_parent.txt"
                    if parent_marker.exists():
                        hint = " (via Sammelband verknuepft, aber noch Status ROT)"
                    else:
                        hint = " — siehe `BESCHAFFUNG.md`"
                elif a == "GELB-K":
                    hint = f" (PDF hat nur {cov['pdf_pages']} S., evtl. unvollstaendig)"
                lines.append(f"- {fmt_ampel(a)} **`{k}`** ({role}; {cites_info}){hint}")
            lines.append("")
        else:
            lines.append("### Kritische Luecken")
            lines.append("")
            lines.append("_Keine kritischen Luecken: alle Quellen dieser Frage sind mindestens GELB+._")
            lines.append("")

    # =====================================================================
    # Globale Anhaenge
    # =====================================================================
    lines.append("---")
    lines.append("")
    lines.append("## Globale Quellen-Matrix")
    lines.append("")
    lines.append("Welche Quelle erscheint in welcher Frage? (K = Kernliteratur, F = Fliesstext)")
    lines.append("")
    lines.append("| BibKey | Ampel | Fr.1 | Fr.2 | Fr.3 | Fr.4 | Fr.5 |")
    lines.append("|---|---|:---:|:---:|:---:|:---:|:---:|")

    key_to_roles: dict[str, dict[int, set[str]]] = defaultdict(lambda: defaultdict(set))
    for s in per_frage_summary:
        fr_num = s["fr"]["num"]
        for kl in s["kernlit"]:
            key_to_roles[kl["key"]][fr_num].add("K")
        for c in s["fliess_cites"]:
            key_to_roles[c.bibkey][fr_num].add("F")

    for k in sorted(key_to_roles.keys()):
        cov = get_cov(k)
        a = ampel(cov)
        row = [f"`{k}`", fmt_ampel(a)]
        for n in (1, 2, 3, 4, 5):
            roles = key_to_roles[k].get(n, set())
            row.append("".join(sorted(roles)) or "·")
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")

    # Legende
    lines.append("## Legende")
    lines.append("")
    lines.append("- **🟢 GRUEN** — Volltext + `verified_quotes.md` Status ≥ 3")
    lines.append("- **🟡 GELB+** — Volltext + Kapitel-Splits vorhanden, aber noch nicht verifiziert")
    lines.append("- **🟡 GELB** — Volltext vorhanden, keine Splits")
    lines.append("- **🟠 GELB-K** — Nur Kurz-Auszug (<15 S.), evtl. unvollstaendig")
    lines.append("- **🔴 ROT** — Kein Volltext. Beschaffung: siehe `BESCHAFFUNG.md`")
    lines.append("- **K** = Quelle ist als Kernliteratur der Frage aufgefuehrt")
    lines.append("- **F** = Quelle wird im Fliesstext zitiert")
    lines.append("")
    return "\n".join(lines)


def _offset_of(cite: cc.Citation, tex_file: str) -> int:
    """Ermittelt den Offset einer Cite im TeX-Text aus Line+raw."""
    path = HERE / tex_file
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8")
    starts = cc._line_index(text)
    if cite.line < 1 or cite.line > len(starts):
        return 0
    line_start = starts[cite.line - 1]
    # Suche raw ab line_start
    idx = text.find(cite.raw, line_start)
    return idx if idx >= 0 else line_start


# =============================================================================
# Main
# =============================================================================

def main() -> int:
    fragen_per_file: dict[str, list] = {}
    for tex_path, marker, label in TEX_FILES:
        fragen_per_file[tex_path.name] = parse_fragen(tex_path)
        print(f"  {tex_path.name}: {len(fragen_per_file[tex_path.name])} Fragen-Sections")

    report = render_report(fragen_per_file)
    OUT.write_text(report, encoding="utf-8")
    print(f"  [OK] -> {OUT}  ({OUT.stat().st_size} Bytes, {len(report.splitlines())} Zeilen)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
