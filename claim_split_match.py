#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
claim_split_match.py - Automatisches Matching von Cite-Stellen zu Kapitel-Splits.

Fuer jede Cite-Stelle in `mpv.tex` / `mpv_abgabedokument.tex`:
  - Extrahiere Keywords aus dem Kontext (Satz vor/mit dem Cite)
  - Fuer jeden zitierten BibKey: finde die Top-3 Kapitel-Splits der Quelle,
    deren Titel am besten zu den Keywords passen.

Das Modul stellt nur Funktionen bereit. Integration in build_kompendium.py
und scaffold_verified_quotes.py.

Aufruf (CLI, optional):
  python claim_split_match.py                # gibt Matches als JSON aus
  python claim_split_match.py --key leikhof2021jugendliche   # nur diese Quelle
"""

from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
LIT = HERE / "Literatur"

# ---------- STOPPWORTLISTEN ---------------------------------------------------

DE_STOPWORDS = {
    "aber", "alle", "aller", "als", "am", "an", "auch", "auf", "aus", "bei",
    "beim", "bezeichnen", "bezeichnet", "bis", "da", "damit", "dann", "daraus",
    "darueber", "darum", "das", "dass", "dem", "den", "der", "deren", "des",
    "deshalb", "dessen", "die", "dies", "diese", "diesem", "diesen", "dieser",
    "dieses", "doch", "dort", "durch", "ein", "eine", "einem", "einen", "einer",
    "eines", "einige", "einigen", "einiger", "einiges", "es", "etwa", "etwas",
    "fuer", "ganz", "geben", "gegen", "gesamt", "hat", "hatte", "hatten", "hier",
    "hin", "ihre", "ihrem", "ihren", "ihrer", "ihres", "im", "in", "ins", "ist",
    "ja", "jede", "jedem", "jeden", "jeder", "jedes", "jene", "jenem", "jenen",
    "jener", "jenes", "kann", "kein", "keine", "keinem", "keinen", "keiner",
    "kommt", "koennen", "koennte", "lassen", "macht", "mal", "man", "mehr",
    "mit", "nach", "nicht", "nichts", "noch", "nun", "nur", "ob", "oben", "oder",
    "ohne", "pro", "rund", "schon", "sehr", "sein", "seine", "seinem", "seinen",
    "seiner", "seit", "sich", "sie", "sind", "so", "solche", "solchem", "solchen",
    "solcher", "solches", "soll", "sollen", "sollte", "sollten", "sondern",
    "sonst", "soviel", "spaeter", "teil", "teils", "trotz", "tun", "ueber",
    "um", "und", "uns", "unser", "unsere", "unter", "vom", "von", "vor", "waere",
    "waeren", "war", "waren", "was", "weil", "welche", "welchem", "welchen",
    "welcher", "welches", "wenig", "weniger", "wenn", "wer", "werde", "werden",
    "wider", "wie", "wieder", "wies", "will", "wir", "wird", "wo", "wohl", "zu",
    "zum", "zur", "zwar", "zwischen",
    # Fachbegriff-unspezifische Woerter
    "etwa", "insbesondere", "beispielsweise", "dennoch", "gegebenenfalls",
    "grundsaetzlich", "vielmehr", "weitgehend", "zudem", "schliesslich", "naemlich",
    # TeX-Artefakte
    "parencite", "textcite", "cite", "citeauthor", "citeyear", "eg", "vgl", "etc",
    "cf", "siehe", "ebd",
}
EN_STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "of", "to", "for",
    "with", "without", "from", "by", "is", "are", "was", "were", "be", "been",
    "being", "has", "have", "had", "it", "its", "this", "that", "these", "those",
    "they", "them", "their", "which", "who", "whom", "as", "not", "no", "yes",
    "can", "could", "should", "would", "may", "might", "will", "shall", "do",
    "does", "did", "done", "also", "only", "just", "very", "more", "most", "some",
    "any", "all", "such", "each", "every", "both", "either", "neither", "other",
    "another", "than", "then", "so", "if", "while", "during", "since", "until",
    "because", "although", "though", "when", "where", "why", "how",
}
STOPWORDS = DE_STOPWORDS | EN_STOPWORDS

# Normalisierungstabelle: Umlaute -> ae/oe/ue
UMLAUT_MAP = str.maketrans({
    "ä": "ae", "Ä": "ae", "ö": "oe", "Ö": "oe", "ü": "ue", "Ü": "ue",
    "ß": "ss", "é": "e", "è": "e", "ê": "e", "à": "a", "â": "a",
})

# ---------- KEYWORD-EXTRAKTION ------------------------------------------------

TOKEN_RE = re.compile(r"[a-zA-Z\u00c0-\u024f]{4,30}")


def _normalize(s: str) -> str:
    return s.translate(UMLAUT_MAP).lower()


def extract_keywords(text: str, min_len: int = 4) -> list[str]:
    """Extrahiert normalisierte Keywords aus Text. Nomen-Heuristik: alle >=4 Zeichen,
    keine Stoppwoerter, keine Zahlen."""
    if not text:
        return []
    # TeX-Commands wegwerfen
    text = re.sub(r"\\[a-zA-Z]+\{[^}]*\}", " ", text)
    text = re.sub(r"\\[a-zA-Z]+", " ", text)
    tokens = TOKEN_RE.findall(text)
    out: list[str] = []
    seen = set()
    for t in tokens:
        if len(t) < min_len:
            continue
        norm = _normalize(t)
        if norm in STOPWORDS:
            continue
        if norm in seen:
            continue
        seen.add(norm)
        out.append(norm)
    return out


# ---------- SPLIT-INDEX -------------------------------------------------------

_OUTLINE_ROW_RE = re.compile(
    r"^\|\s*\d+\s*\|\s*S\.\s*(\d+)[\s\u2013-]+(\d+)\s*\(\d+\)\s*\|\s*\[`([^`]+)`\]\([^)]+\)\s*\|\s*(.+?)\s*\|",
    re.MULTILINE,
)


def _extract_split_text(pdf_file: Path) -> str:
    """Extrahiert Text aus einer Split-PDF via pdftotext."""
    import subprocess
    try:
        res = subprocess.run(
            ["pdftotext", "-enc", "UTF-8", str(pdf_file), "-"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30,
        )
        return res.stdout or ""
    except Exception:
        return ""


def _build_split_index(key: str) -> dict[str, Any]:
    """Baut oder laedt den Split-Text-Index fuer eine Quelle.

    Cache: Literatur/<key>/excerpts/_index.json (pro Split: title + keywords).
    """
    ex_dir = LIT / key / "excerpts"
    cache_file = ex_dir / "_index.json"
    if cache_file.exists():
        try:
            return json.loads(cache_file.read_text(encoding="utf-8"))
        except Exception:
            pass

    # Index bauen
    index: dict[str, Any] = {"_version": 1, "splits": {}}
    outline = ex_dir / "_outline.md"
    if not outline.exists():
        return index
    txt = outline.read_text(encoding="utf-8")
    for m in _OUTLINE_ROW_RE.finditer(txt):
        filename = m.group(3)
        title = re.sub(r"&nbsp;", "", m.group(4).strip()).strip()
        page_start = int(m.group(1))
        page_end = int(m.group(2))
        pdf_path = ex_dir / filename
        if pdf_path.exists():
            fulltext = _extract_split_text(pdf_path)
            # Keywords aus Titel + Volltext
            title_kws = extract_keywords(title, min_len=3)
            # Keywords aus Volltext: haeufigste nach Frequenz
            text_tokens = [t for t in extract_keywords(fulltext, min_len=5) if t]
            # Top 40 Keywords (nach Frequenz)
            from collections import Counter
            freq = Counter(text_tokens)
            top_kws = [w for w, _c in freq.most_common(40)]
            index["splits"][filename] = {
                "title": title,
                "title_keywords": title_kws,
                "text_keywords": top_kws,
                "page_start": page_start,
                "page_end": page_end,
            }
    # Cache schreiben
    try:
        cache_file.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass
    return index


def load_splits(key: str) -> list[dict[str, Any]]:
    """Liest alle Kapitel-Splits einer Quelle inkl. Volltext-Index."""
    idx = _build_split_index(key)
    out: list[dict[str, Any]] = []
    for filename, data in idx.get("splits", {}).items():
        out.append({
            "file": filename,
            "title": data["title"],
            "title_keywords": data.get("title_keywords", []),
            "text_keywords": data.get("text_keywords", []),
            "page_start": data["page_start"],
            "page_end": data["page_end"],
        })
    out.sort(key=lambda s: s["page_start"])
    return out


# ---------- MATCHING ----------------------------------------------------------

def score_split(claim_keywords: list[str], split: dict[str, Any]) -> float:
    """Score wie gut ein Split zu den Claim-Keywords passt.

    Strategie (kombiniert):
    - Titel-Match: Doppelt gewichtet (ein Treffer im Titel = 2 Punkte).
    - Volltext-Match: Einfach gewichtet (ein Treffer in den Top-40-Keywords = 1 Punkt).
    - Substring-Match: 0.5 Punkte fuer Teilueberlapp.
    - Normalisiert auf Claim-Keyword-Zahl.
    """
    if not claim_keywords:
        return 0.0
    title_kws = set(split.get("title_keywords") or [])
    text_kws = set(split.get("text_keywords") or [])
    claim_set = set(claim_keywords)

    # Exakte Treffer
    title_exact = len(claim_set & title_kws)
    text_exact = len(claim_set & text_kws) - title_exact  # Titel zaehlt nicht doppelt
    if text_exact < 0:
        text_exact = 0

    # Partial-Match nur gegen Titel
    partial = 0.0
    remain = claim_set - title_kws - text_kws
    for ck in remain:
        for tk in title_kws:
            if len(ck) >= 5 and len(tk) >= 5 and (ck in tk or tk in ck):
                partial += 0.5
                break

    raw = 2.0 * title_exact + 1.0 * text_exact + partial
    # Normalisieren: doppelte Cap um viele kurze Claims nicht zu uebervorteilen
    denom = max(len(claim_set), 4)
    return raw / denom


def match_claim(claim_context: str, splits: list[dict[str, Any]], top_n: int = 3,
                min_score: float = 0.15) -> list[dict[str, Any]]:
    """Liefert die Top-N Splits, sortiert nach Score. Nur Splits mit Score >= min_score."""
    if not splits:
        return []
    claim_kws = extract_keywords(claim_context)
    scored = []
    for sp in splits:
        s = score_split(claim_kws, sp)
        if s >= min_score:
            scored.append({**sp, "score": round(s, 3)})
    scored.sort(key=lambda x: (-x["score"], x["page_start"]))
    return scored[:top_n]


# ---------- CITE-SAMMLUNG aus TeX ---------------------------------------------

CITE_RE = re.compile(r"\\(?P<cmd>parencite|textcite|cite|citeauthor|citeyear)\s*\{(?P<keys>[^}]+)\}")


def _sentence_context_around(lines: list[str], lineno: int) -> str:
    """Extrahiert den Satz, in dem der Cite steht, inklusive Vorsatz.

    Strategie: Gehe von `lineno` zurueck bis ein Zeilenumbruch + Satzende-Punkt
    gefunden ist, ggf. bis max 12 Zeilen zurueck. Dann auch bis max 2 Zeilen nach
    vorne (falls der Cite nicht am Satzende steht).
    """
    start_idx = max(0, lineno - 1)
    # Zurueckscannen bis wir einen Satzanfang finden (Punkt+Leerzeichen oder Zeilenanfang)
    back_idx = start_idx
    for i in range(start_idx - 1, max(-1, start_idx - 12), -1):
        prev_line = lines[i].strip() if i >= 0 else ""
        if not prev_line:
            back_idx = i + 1
            break
        # Wenn die vorige Zeile mit einem typischen Satzende-Punkt endet
        if re.search(r"[\.\!\?][\s\}\)\]]*$", prev_line):
            back_idx = i + 1
            break
        back_idx = i
    # Vorwaerts bis zur naechsten Zeile mit Satzende
    fwd_idx = start_idx
    for i in range(start_idx, min(len(lines), start_idx + 4)):
        fwd_idx = i
        cur = lines[i]
        if re.search(r"[\.\!\?][\s\}\)\]]*$", cur.rstrip()):
            break
    snippet_lines = lines[back_idx:fwd_idx + 1]
    return " ".join(l.strip() for l in snippet_lines if l.strip())


def collect_cites_for_key(bib_key: str) -> list[dict[str, Any]]:
    """Liefert alle Cite-Stellen in mpv.tex + mpv_abgabedokument.tex, die
    `bib_key` enthalten, mit Kontext (vollstaendiger Satz)."""
    tex_files = [
        (HERE / "mpv.tex", "L"),
        (HERE / "mpv_abgabedokument.tex", "A"),
    ]
    out: list[dict[str, Any]] = []
    for tex_path, marker in tex_files:
        if not tex_path.exists():
            continue
        lines = tex_path.read_text(encoding="utf-8").splitlines()
        for lineno, line in enumerate(lines, start=1):
            scan = re.sub(r"\\verb\|[^|]*\|", "", line)
            for m in CITE_RE.finditer(scan):
                keys = [k.strip() for k in m.group("keys").split(",") if k.strip()]
                if bib_key not in keys:
                    continue
                # Satz-Kontext extrahieren (nicht nur 3 Zeilen davor)
                ctx = _sentence_context_around(lines, lineno)
                is_list = bool(re.search(r"\\item\[\\cite", line))
                out.append({
                    "tex_marker": marker,
                    "tex_file": tex_path.name,
                    "lineno": lineno,
                    "cmd": m.group("cmd"),
                    "keys": keys,
                    "context": ctx[-800:],  # bis zu 800 Zeichen
                    "is_list": is_list,
                })
    return out


# ---------- CLI ---------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", help="Nur fuer diese Quelle")
    ap.add_argument("--json", action="store_true", help="JSON-Output")
    args = ap.parse_args()

    # Liste aller Quellen mit Splits
    keys: list[str] = []
    if args.key:
        keys = [args.key]
    else:
        for d in LIT.iterdir():
            if not d.is_dir():
                continue
            if (d / "excerpts" / "_outline.md").exists():
                keys.append(d.name)
    keys.sort()

    all_results: dict[str, Any] = {}
    for k in keys:
        splits = load_splits(k)
        cites = collect_cites_for_key(k)
        if not cites:
            continue
        per_key: list[dict[str, Any]] = []
        for c in cites:
            if c["is_list"]:
                continue  # Literatur-Listen bei Matching irrelevant
            matches = match_claim(c["context"], splits, top_n=3)
            per_key.append({
                "tex_marker": c["tex_marker"],
                "lineno": c["lineno"],
                "context": c["context"],
                "matches": matches,
            })
        if per_key:
            all_results[k] = {
                "n_splits": len(splits),
                "n_cites": len(per_key),
                "claims": per_key,
            }

    if args.json:
        print(json.dumps(all_results, indent=2, ensure_ascii=False))
    else:
        for k, data in all_results.items():
            print(f"\n[{k}]  ({data['n_splits']} Splits, {data['n_cites']} Cites)")
            for claim in data["claims"]:
                print(f"  {claim['tex_marker']}:{claim['lineno']}")
                ctx = claim["context"][-120:].replace("\n", " ")
                print(f"    ctx: ...{ctx}")
                if not claim["matches"]:
                    print(f"    -> KEIN Match")
                    continue
                for i, m in enumerate(claim["matches"], start=1):
                    print(f"    -> [{i}] score={m['score']}  S.{m['page_start']}-{m['page_end']}  {m['title'][:60]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
