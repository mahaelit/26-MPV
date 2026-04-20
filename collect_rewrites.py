"""collect_rewrites.py - Aggregator fuer REWRITES-Bloecke aus verified_quotes.md

Scannt alle `Literatur/*/verified_quotes.md` nach YAML-Bloecken zwischen den
Markern `<!-- REWRITES-START -->` und `<!-- REWRITES-END -->` und schreibt eine
zentrale Uebersicht `REWRITES.md` im Workspace-Root.

Die zentrale Datei ersetzt die manuelle Umzitierungstabelle in
`UEBERGABEBERICHT.md` §6.3 und dient als Single Source of Truth
(SSOT) fuer Phase 3 (TeX-Umzitierung).

Konvention eines Rewrite-Blocks (innerhalb eines verified_quotes.md):

    <!-- REWRITES-START (manuell gepflegt; ...) -->
    ```yaml
    - tex_file: mpv.tex
      line: 650
      action: replace_key       # replace_key | remove_key | add_key | modify
      old: '\textcite{preckel2013hochbegabung}'
      new: '\textcite{preckel2021tad}'
      reason: >
        Kurze Begruendung (mehrzeilig erlaubt via YAML-Block-Skalar)
      status: pending           # pending | applied | rejected
    ```
    <!-- REWRITES-END -->

Ein Rewrite gehoert in das Dossier des BibKeys, der ersetzt/gestrichen wird
(der Key im `old`-Feld). So bleibt jede Umzitierungs-Empfehlung bei ihrem
Befund.

`apply_rewrites.py` (separat, noch nicht implementiert) liest dieselben
Bloecke und fuehrt die Aenderungen im TeX durch.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    import yaml  # type: ignore
except ImportError:
    print("[ERR] PyYAML fehlt. Installieren: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


HERE       = Path(__file__).resolve().parent
LITERATUR  = HERE / "Literatur"
OUT_PATH   = HERE / "REWRITES.md"

# Marker-Regex: findet YAML-Block zwischen REWRITES-START und REWRITES-END,
# egal ob darin ```yaml-Fences sind oder nicht.
BLOCK_RE = re.compile(
    r"<!--\s*REWRITES-START\b[^>]*-->\s*(.*?)<!--\s*REWRITES-END\s*-->",
    re.DOTALL,
)
FENCE_RE = re.compile(r"```(?:yaml)?\s*\n(.*?)```", re.DOTALL)


# ---------------------------------------------------------------------------
# Datenmodell
# ---------------------------------------------------------------------------
@dataclass
class Rewrite:
    source_dossier: str          # BibKey des Dossiers, in dem der Block steht
    tex_file:       str
    line:           int | None
    action:         str
    old:            str
    new:            str
    reason:         str
    status:         str          # pending | applied | rejected
    raw_index:      int          # Position innerhalb des Dossier-Blocks (fuer stabile Sortierung)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------
def _extract_yaml_from_block(block_text: str) -> str:
    """Erlaubt sowohl `yaml-Fences als auch rohen YAML-Inhalt."""
    m = FENCE_RE.search(block_text)
    return m.group(1) if m else block_text


def parse_dossier(md_path: Path) -> list[Rewrite]:
    text = md_path.read_text(encoding="utf-8")
    dossier_key = md_path.parent.name  # Literatur/<bibkey>/verified_quotes.md
    rewrites: list[Rewrite] = []
    for block_match in BLOCK_RE.finditer(text):
        yaml_text = _extract_yaml_from_block(block_match.group(1))
        if not yaml_text.strip():
            continue
        try:
            data = yaml.safe_load(yaml_text)
        except yaml.YAMLError as exc:
            print(f"[WARN] {dossier_key}: YAML-Parse-Fehler: {exc}",
                  file=sys.stderr)
            continue
        if not isinstance(data, list):
            print(f"[WARN] {dossier_key}: REWRITES-Block ist keine Liste "
                  f"(Typ: {type(data).__name__})", file=sys.stderr)
            continue
        for i, entry in enumerate(data):
            if not isinstance(entry, dict):
                continue
            rewrites.append(Rewrite(
                source_dossier = dossier_key,
                tex_file = str(entry.get("tex_file", "")).strip(),
                line     = entry.get("line") if isinstance(entry.get("line"), int) else None,
                action   = str(entry.get("action", "modify")).strip(),
                old      = str(entry.get("old", "")).strip(),
                new      = str(entry.get("new", "")).strip(),
                reason   = str(entry.get("reason", "")).strip(),
                status   = str(entry.get("status", "pending")).strip().lower(),
                raw_index = i,
            ))
    return rewrites


def collect_all(literatur_root: Path) -> list[Rewrite]:
    rewrites: list[Rewrite] = []
    for folder in sorted(literatur_root.iterdir()):
        if not folder.is_dir():
            continue
        md = folder / "verified_quotes.md"
        if not md.is_file():
            continue
        rewrites.extend(parse_dossier(md))
    return rewrites


# ---------------------------------------------------------------------------
# Markdown-Ausgabe
# ---------------------------------------------------------------------------
STATUS_ICON = {
    "pending":  "⏳",
    "applied":  "✅",
    "rejected": "✖",
}


def _escape_md_cell(s: str) -> str:
    # Pipes brechen Markdown-Tabellen; Newlines in Reason komprimieren.
    return s.replace("|", "\\|").replace("\n", " ").strip()


def render_markdown(rewrites: list[Rewrite]) -> str:
    n_total    = len(rewrites)
    n_pending  = sum(1 for r in rewrites if r.status == "pending")
    n_applied  = sum(1 for r in rewrites if r.status == "applied")
    n_rejected = sum(1 for r in rewrites if r.status == "rejected")

    lines: list[str] = []
    lines.append("# REWRITES.md — Zentrale TeX-Umzitierungs-Tabelle")
    lines.append("")
    lines.append("_Automatisch erzeugt durch `collect_rewrites.py` aus den "
                 "`<!-- REWRITES-... -->`-Bloecken in "
                 "`Literatur/*/verified_quotes.md`._")
    lines.append("")
    lines.append("_Nicht manuell editieren — aendern Sie den Rewrite-Block "
                 "im jeweiligen Dossier und lassen Sie das Skript neu laufen._")
    lines.append("")
    lines.append("## Uebersicht")
    lines.append("")
    lines.append(f"- **Gesamt:** {n_total} Rewrites")
    lines.append(f"- ⏳ **pending:** {n_pending}")
    lines.append(f"- ✅ **applied:** {n_applied}")
    lines.append(f"- ✖ **rejected:** {n_rejected}")
    lines.append("")

    if not rewrites:
        lines.append("_(Keine Rewrite-Bloecke gefunden.)_")
        lines.append("")
        return "\n".join(lines)

    # Gruppiert nach TeX-Datei, sortiert nach Zeilennummer.
    by_tex: dict[str, list[Rewrite]] = {}
    for r in rewrites:
        by_tex.setdefault(r.tex_file or "(unbekannt)", []).append(r)

    for tex_file in sorted(by_tex):
        bucket = by_tex[tex_file]
        bucket.sort(key=lambda r: (r.line if r.line is not None else 10**9,
                                   r.source_dossier, r.raw_index))
        lines.append(f"## `{tex_file}`")
        lines.append("")
        lines.append(f"_{len(bucket)} Rewrite(s)_")
        lines.append("")
        lines.append("| Status | Zeile | Action | Alt → Neu | Begruendung | Quelle |")
        lines.append("|---|---:|---|---|---|---|")
        for r in bucket:
            icon = STATUS_ICON.get(r.status, r.status)
            line_cell = str(r.line) if r.line is not None else "?"
            change = f"`{_escape_md_cell(r.old)}` → `{_escape_md_cell(r.new)}`"
            reason = _escape_md_cell(r.reason)
            if len(reason) > 250:
                reason = reason[:247] + "..."
            src = f"`{r.source_dossier}`"
            lines.append(f"| {icon} {r.status} | {line_cell} | "
                         f"{_escape_md_cell(r.action)} | {change} | "
                         f"{reason} | {src} |")
        lines.append("")

    # Status-Breakdown pro Dossier (hilfreich, um schnell zu sehen, wer
    # noch offene Rewrites hat).
    lines.append("## Status-Breakdown pro Dossier")
    lines.append("")
    lines.append("| Dossier | pending | applied | rejected | total |")
    lines.append("|---|---:|---:|---:|---:|")
    per_src: dict[str, dict[str, int]] = {}
    for r in rewrites:
        d = per_src.setdefault(r.source_dossier,
                               {"pending": 0, "applied": 0, "rejected": 0})
        d[r.status] = d.get(r.status, 0) + 1
    for src in sorted(per_src):
        s = per_src[src]
        tot = s["pending"] + s["applied"] + s["rejected"]
        lines.append(f"| `{src}` | {s['pending']} | {s['applied']} | "
                     f"{s['rejected']} | {tot} |")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    if not LITERATUR.is_dir():
        print(f"[ERR] Literatur-Ordner fehlt: {LITERATUR}", file=sys.stderr)
        return 1

    rewrites = collect_all(LITERATUR)
    print(f"collect_rewrites.py")
    print(f"  Quelle: {LITERATUR}")
    print(f"  Dossier-Ordner: {sum(1 for p in LITERATUR.iterdir() if p.is_dir())}")
    print(f"  Rewrites gefunden: {len(rewrites)}")
    by_status: dict[str, int] = {}
    for r in rewrites:
        by_status[r.status] = by_status.get(r.status, 0) + 1
    for st in sorted(by_status):
        print(f"    {st:<10} {by_status[st]}")

    md = render_markdown(rewrites)
    OUT_PATH.write_text(md, encoding="utf-8")
    print(f"  [OK] -> {OUT_PATH}  ({len(md)} Zeichen)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
