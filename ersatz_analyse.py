#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
ersatz_analyse.py - Pro ROT-Cite-Stelle die besten Split-Matches aus den
"Ersatz-Quellen" finden (Default: behrensen2016, brackmann2013, preuss2018, reintjes2019).

Ziel: Aufzeigen, welche ROT-Zitate sich durch bereits vorhandene Zusatz-Quellen
belegen lassen – damit nicht 1118 S. beschafft werden muessen, sondern evtl. 500.

Ausgabe: ERSATZ_VORSCHLAEGE.md
  - Pro ROT-BibKey: alle Cites mit Kontext
  - Pro Cite: Top-2 Ersatz-Splits aus den 4 Zusatz-Quellen (mit Score, Seitenbereich, Direct-Link)
  - Zusammenfassung: Wie viele Cites koennten ersetzt werden?
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path
from typing import Any

from claim_split_match import collect_cites_for_key, load_splits, match_claim, extract_keywords, score_split

HERE = Path(__file__).resolve().parent
LIT = HERE / "Literatur"
BIB = HERE / "Quellen.bib"

# Default: die 4 in dieser Session neu onboarded Quellen
DEFAULT_ERSATZ_KEYS = [
    "behrensen2016grundwissen",
    "brackmann2013jenseits",
    "preuss2018inklusive",
    "reintjes2019begabungsfoerderung",
]


def parse_bib() -> dict[str, dict[str, str]]:
    if not BIB.exists():
        return {}
    text = BIB.read_text(encoding="utf-8")
    entries = re.findall(r"@\w+\{([^,]+),\s*(.+?)(?=\n@|\Z)", text, re.DOTALL)
    out = {}
    for key, body in entries:
        key = key.strip()

        def f(name: str) -> str:
            m = re.search(name + r"\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}", body, re.IGNORECASE)
            return re.sub(r"[{}]", "", m.group(1)).strip() if m else ""

        out[key] = {
            "author": f("author") or f("editor"),
            "year": f("year"),
            "title": f("title"),
        }
    return out


def classify_bibkey(key: str) -> str:
    """Liefert Ampel-Status: 'volltext', 'toc', 'rot'."""
    d = LIT / key
    if not d.is_dir():
        return "unknown"
    if (d / "source.pdf").exists() or (d / "source.epub").exists():
        return "volltext"
    if list(d.glob("_TOC_*.md")):
        return "toc"
    return "rot"


def find_rot_bibkeys_with_cites(bib: dict[str, dict[str, str]]) -> list[str]:
    """Liefert alle BibKeys mit Status=rot, die mindestens einmal in den TeX-Dateien zitiert werden."""
    rot: list[str] = []
    for key in bib.keys():
        if classify_bibkey(key) != "rot":
            continue
        # Pruefen ob zitiert
        cites = collect_cites_for_key(key)
        # Ignoriere reine Literaturverzeichnis-Items
        non_list = [c for c in cites if not c.get("is_list")]
        if non_list:
            rot.append(key)
    rot.sort()
    return rot


def load_ersatz_splits(ersatz_keys: list[str]) -> list[tuple[str, list[dict[str, Any]]]]:
    """Laedt fuer jede Ersatz-Quelle die Splits (mit Volltext-Index)."""
    out: list[tuple[str, list[dict[str, Any]]]] = []
    for k in ersatz_keys:
        splits = load_splits(k)
        if splits:
            out.append((k, splits))
        else:
            print(f"  WARN: keine Splits fuer {k}")
    return out


def find_best_ersatz(claim_context: str, all_ersatz: list[tuple[str, list[dict[str, Any]]]],
                      top_n: int = 2, min_score: float = 0.25) -> list[dict[str, Any]]:
    """Findet die top_n besten Ersatz-Splits aus allen Quellen zusammen."""
    claim_kws = extract_keywords(claim_context)
    if not claim_kws:
        return []
    all_scored: list[dict[str, Any]] = []
    for key, splits in all_ersatz:
        for sp in splits:
            s = score_split(claim_kws, sp)
            if s >= min_score:
                all_scored.append({
                    "ersatz_key": key,
                    "file": sp["file"],
                    "title": sp["title"],
                    "page_start": sp["page_start"],
                    "page_end": sp["page_end"],
                    "score": round(s, 3),
                })
    all_scored.sort(key=lambda x: (-x["score"], x["ersatz_key"], x["page_start"]))
    return all_scored[:top_n]


def build_report(bib: dict[str, dict[str, str]], rot_keys: list[str],
                 ersatz_keys: list[str], all_ersatz: list[tuple[str, list[dict[str, Any]]]],
                 min_score: float = 0.25) -> str:
    lines: list[str] = []
    lines.append("# Ersatz-Analyse – ROT-Cites durch Zusatz-Quellen ersetzen")
    lines.append("")
    lines.append("Pro **ROT-Cite** (Originalquelle nicht als Volltext verfuegbar) werden die")
    lines.append(f"besten Kapitel-Splits aus folgenden **{len(ersatz_keys)} Zusatz-Quellen** gesucht:")
    lines.append("")
    for k in ersatz_keys:
        meta = bib.get(k, {})
        n_splits = len(next((s for ek, s in all_ersatz if ek == k), []))
        lines.append(f"- `{k}` – {meta.get('author','')} ({meta.get('year','')}), {n_splits} Splits")
    lines.append("")
    lines.append(f"**Threshold:** nur Matches mit Score >= {min_score} werden gelistet (empirisch kalibriert).")
    lines.append("")
    lines.append("**Score-Interpretation:**")
    lines.append("- `>= 0.5` : sehr wahrscheinlicher Ersatz, Kontext passt thematisch genau")
    lines.append("- `0.3-0.5` : plausibler Kandidat, Volltext pruefen")
    lines.append("- `0.25-0.3` : schwacher Hinweis, thematisch ungefaehr aehnlich")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Aggregierte Statistik
    stats = {"total_rot_cites": 0, "with_match": 0, "with_strong_match": 0, "by_rot_key": {}}

    # Pro ROT-BibKey
    for rk in rot_keys:
        cites = [c for c in collect_cites_for_key(rk) if not c.get("is_list")]
        if not cites:
            continue
        rk_matches = 0
        rk_strong = 0
        meta = bib.get(rk, {})
        lines.append(f"## `{rk}` – {meta.get('author','')} ({meta.get('year','')})")
        lines.append("")
        lines.append(f"Titel: {meta.get('title','')}")
        lines.append(f"**{len(cites)} Cite-Stellen**")
        lines.append("")

        for c in cites:
            stats["total_rot_cites"] += 1
            matches = find_best_ersatz(c["context"], all_ersatz, top_n=2, min_score=min_score)
            lineno = c["lineno"]
            marker = c["tex_marker"]
            tex_file = c["tex_file"]
            ctx = c["context"][-350:].replace("\n", " ")
            ctx_short = (ctx[:280] + "…") if len(ctx) > 280 else ctx

            lines.append(f"### {marker}:{lineno} ({c['cmd']})")
            lines.append(f"[`{tex_file}:{lineno}`]({tex_file}#L{lineno})")
            lines.append("")
            lines.append(f"> {ctx_short}")
            lines.append("")

            if not matches:
                lines.append("- Kein Ersatz-Match ueber Threshold gefunden.")
            else:
                stats["with_match"] += 1
                rk_matches += 1
                if matches[0]["score"] >= 0.5:
                    stats["with_strong_match"] += 1
                    rk_strong += 1
                for i, m in enumerate(matches, start=1):
                    link = f"Literatur/{m['ersatz_key']}/excerpts/{m['file']}"
                    marker_score = "**[STRONG]**" if m["score"] >= 0.5 else "[OK]"
                    lines.append(f"- {marker_score} score={m['score']}: [`{m['file']}`]({link}) S.{m['page_start']}-{m['page_end']} – {m['title']}  _({m['ersatz_key']})_")
            lines.append("")

        stats["by_rot_key"][rk] = {"cites": len(cites), "matches": rk_matches, "strong": rk_strong}
        lines.append("---")
        lines.append("")

    # Zusammenfassung oben einfuegen
    summary = []
    summary.append("## Zusammenfassung")
    summary.append("")
    summary.append(f"- **{len(rot_keys)}** ROT-BibKeys mit Cite-Stellen analysiert")
    summary.append(f"- **{stats['total_rot_cites']}** ROT-Cite-Stellen insgesamt")
    summary.append(f"- **{stats['with_match']}** davon haben mindestens einen Ersatz-Kandidaten (Score >= {min_score})")
    summary.append(f"- **{stats['with_strong_match']}** haben einen **starken** Kandidaten (Score >= 0.5)")
    summary.append("")
    summary.append("### Pro ROT-Quelle: Anteil Cites mit Ersatz-Kandidat")
    summary.append("")
    summary.append("| ROT-Quelle | Cites | mit Ersatz | davon STRONG |")
    summary.append("|---|---:|---:|---:|")
    for rk, s in sorted(stats["by_rot_key"].items(), key=lambda x: -x[1]["cites"]):
        summary.append(f"| `{rk}` | {s['cites']} | {s['matches']} | {s['strong']} |")
    summary.append("")
    summary.append("---")
    summary.append("")

    # Einfuegen nach dem Kopfteil
    header_end = next(i for i, l in enumerate(lines) if l == "---") + 2
    return "\n".join(lines[:header_end] + summary + lines[header_end:])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ersatz", nargs="+", default=DEFAULT_ERSATZ_KEYS,
                    help="Liste der Ersatz-BibKeys (Default: die 4 in dieser Session onboarded)")
    ap.add_argument("--min-score", type=float, default=0.25,
                    help="Minimum-Score fuer Matches (Default: 0.25)")
    args = ap.parse_args()

    print("ersatz_analyse.py")
    print(f"  Ersatz-Quellen: {', '.join(args.ersatz)}")
    print(f"  Min-Score: {args.min_score}")

    bib = parse_bib()
    rot_keys = find_rot_bibkeys_with_cites(bib)
    print(f"  ROT-BibKeys mit Cites: {len(rot_keys)}")

    all_ersatz = load_ersatz_splits(args.ersatz)
    total_splits = sum(len(s) for _, s in all_ersatz)
    print(f"  Ersatz-Splits geladen: {total_splits}")

    report = build_report(bib, rot_keys, args.ersatz, all_ersatz, min_score=args.min_score)
    out = HERE / "ERSATZ_VORSCHLAEGE.md"
    out.write_text(report, encoding="utf-8")
    print(f"  [OK] -> {out} ({out.stat().st_size} Bytes, {report.count(chr(10))} Zeilen)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
