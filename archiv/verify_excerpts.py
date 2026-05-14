#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
verify_excerpts.py - Pruefe jede .pdf in Literatur/<key>/excerpts/:
  - enthaelt Seite 1 den Kapiteltitel aus _outline.md?
  - Seitenanzahl == im outline erwartete Anzahl?
  - Dateigroesse > 0?

Druckt Bericht mit Warnungen fuer auffaellige Splits.

Aufruf:
  python verify_excerpts.py --key hoyer2013begabung
  python verify_excerpts.py          # alle Quellen
"""

from __future__ import annotations
import argparse
import re
import subprocess
import sys
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    print("ERR: pypdf nicht installiert.", file=sys.stderr)
    sys.exit(2)

HERE = Path(__file__).resolve().parent
LIT = HERE / "Literatur"


def normalize(s: str) -> str:
    """Fuer robusten Vergleich: Kleinschrift, Umlaute normalisiert, Whitespace gestrippt."""
    s = s.lower()
    repl = {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss",
            "\u201e": '"', "\u201c": '"', "\u2013": "-", "\u2014": "-",
            "\u2019": "'", "\u2018": "'"}
    for k, v in repl.items():
        s = s.replace(k, v)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def get_title_from_slug(fname: str) -> str:
    """001_front_cover.pdf -> 'front_cover' -> grob als Titel."""
    m = re.match(r"\d+_(.+)\.pdf$", fname)
    return m.group(1).replace("_", " ") if m else fname


def parse_outline_md(path: Path) -> list[dict[str, str]]:
    """Liest die Tabelle aus _outline.md. Returns list of {file, title, page_start, page_end, n_pages}."""
    if not path.exists():
        return []
    rows = []
    txt = path.read_text(encoding="utf-8")
    # Zeile-Format:  | N | S. X-Y (Z) | [`file.pdf`](file.pdf) | Titel |
    row_re = re.compile(
        r"^\|\s*\d+\s*\|\s*S\.\s*(\d+)[\s\u2013-]+(\d+)\s*\((\d+)\)\s*\|\s*\[`([^`]+)`\]\([^)]+\)\s*\|\s*(.+?)\s*\|",
        re.MULTILINE,
    )
    for m in row_re.finditer(txt):
        title = m.group(5).strip()
        # HTML-Entities (Indent) entfernen
        title = re.sub(r"&nbsp;", "", title)
        title = re.sub(r"&amp;", "&", title)
        title = title.strip()
        rows.append({
            "file": m.group(4),
            "title": title,
            "page_start": int(m.group(1)),
            "page_end": int(m.group(2)),
            "n_pages": int(m.group(3)),
        })
    return rows


def extract_pdf_text(pdf_path: Path, first_n_pages: int = 2) -> str:
    """Mit pdftotext die ersten N Seiten extrahieren (robust gegenueber Unicode)."""
    try:
        res = subprocess.run(
            ["pdftotext", "-layout", "-enc", "UTF-8", "-f", "1", "-l", str(first_n_pages), str(pdf_path), "-"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=15,
        )
        return res.stdout or ""
    except Exception as e:
        return f"[ERR: {e}]"


def verify_one(key: str) -> int:
    ex_dir = LIT / key / "excerpts"
    outline = ex_dir / "_outline.md"
    if not outline.exists():
        print(f"[{key}] WARN: kein _outline.md")
        return 1
    rows = parse_outline_md(outline)
    print(f"[{key}]  {len(rows)} Splits laut _outline.md")
    n_ok = 0
    n_warn = 0
    n_err = 0
    for r in rows:
        fpath = ex_dir / r["file"]
        if not fpath.exists():
            print(f"  [FEHLT]  {r['file']}")
            n_err += 1
            continue
        # Seitenanzahl
        try:
            reader = PdfReader(str(fpath))
            actual_pages = len(reader.pages)
        except Exception as e:
            print(f"  [ERR]    {r['file']} konnte nicht gelesen werden: {e}")
            n_err += 1
            continue
        if actual_pages != r["n_pages"]:
            print(f"  [WARN]   {r['file']}: erwartet {r['n_pages']} Seiten, hat {actual_pages}")
            n_warn += 1
            continue
        # Titel-Check tolerant: durchsuche die ersten 3 Seiten des Splits
        pdf_text = extract_pdf_text(fpath, first_n_pages=min(3, actual_pages))
        norm_title = normalize(r["title"])
        norm_page = normalize(pdf_text)
        # Sammle Titel-Keywords (>=4 Zeichen, keine Stoppwoerter)
        STOP = {"und", "oder", "die", "der", "das", "ein", "eine", "mit", "zur", "zum", "des",
                "im", "von", "bei", "als", "fuer", "the", "and", "of", "in", "to"}
        keywords = [w for w in re.sub(r"[^a-z0-9 ]", " ", norm_title).split()
                    if len(w) >= 4 and w not in STOP]
        # Tolerant: mind. 1 Keyword-Stamm (len-2) im Split-Text
        hits = sum(1 for kw in keywords if kw[:max(4, len(kw) - 2)] in norm_page)
        if hits >= 1 or not keywords:
            n_ok += 1
        else:
            kw_str = ", ".join(keywords[:3])
            print(f"  [?TITEL] {r['file']}: keywords=[{kw_str}] NICHT im Split gefunden")
            n_warn += 1
    print(f"  -> OK: {n_ok},  Warnungen: {n_warn},  Fehler: {n_err}")
    return n_warn + n_err


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", default="")
    args = ap.parse_args()
    print("verify_excerpts.py")
    if args.key:
        keys = [args.key]
    else:
        keys = sorted([d.name for d in LIT.iterdir() if d.is_dir() and (d / "excerpts" / "_outline.md").exists()])
    total = 0
    for k in keys:
        total += verify_one(k)
        print()
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
