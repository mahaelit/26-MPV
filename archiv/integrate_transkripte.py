"""integrate_transkripte.py - Phase T3

Fuegt pro BibKey einen Abschnitt `## Transkript-Verortungen` in die
zugehoerige `Literatur/<bibkey>/verified_quotes.md` ein. Quelle ist der
vom `analyze_transkripte.py` erzeugte `_transkripte_index.json`.

Idempotent via Markern:
    <!-- TRANSKRIPTE-START (...) -->
    ... auto-erzeugter Block ...
    <!-- TRANSKRIPTE-END -->

Platzierung: unmittelbar NACH dem `<!-- CLAIMS-END -->`-Marker von
`cite_context.py` (falls vorhanden), sonst nach dem Metadaten-Header
(erster `---`-Trenner). So bleibt der Nutzer-Bereich darunter intakt.

Usage
-----
    python integrate_transkripte.py

Optionen:
    --index  <pfad>   Pfad zur _transkripte_index.json
                      (Default: Literatur/_transkripte_index.json)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


HERE          = Path(__file__).resolve().parent
LITERATUR     = HERE / "Literatur"
DEFAULT_INDEX = LITERATUR / "_transkripte_index.json"


# ----- Marker -----------------------------------------------------------
MARK_START = ("<!-- TRANSKRIPTE-START (automatisch durch integrate_transkripte.py "
              "erzeugt; nicht manuell editieren) -->")
MARK_END   = "<!-- TRANSKRIPTE-END -->"
BLOCK_RE   = re.compile(
    r"<!-- TRANSKRIPTE-START[^>]*-->.*?<!-- TRANSKRIPTE-END -->",
    re.DOTALL,
)

CLAIMS_END_RE = re.compile(r"<!-- CLAIMS-END -->")
HEADER_SEP_RE = re.compile(r"\n\s*---\s*\n")


# ----- Helpers ----------------------------------------------------------
ROLE_LABEL = {
    "existing_main":     "Haupt-Transkript dieser Quelle",
    "chapter_main":      "Haupt-Kapitel aus Multi-Chapter-Transkript",
    "proposed_new_main": "Transkript begruendet diesen (neuen) BibKey",
    "mentioned_existing":"Verortung als Einzel-Zitatstelle",
    "mentioned_new":     "Verortung (Transkript schlaegt neuen BibKey vor)",
}


def _fmt_relevance(rel: dict[str, str]) -> str:
    if not rel:
        return ""
    items = []
    for k in sorted(rel):
        v = str(rel[k]).strip()
        if v:
            items.append(f"**{k}**: {v}")
    return "; ".join(items)


def _fmt_hint(hint: dict[str, Any]) -> str:
    loc   = hint.get("location", "")
    frage = hint.get("frage")
    text  = (hint.get("text") or "").strip()
    # Text auf max. ~400 Zeichen kappen, damit die Liste uebersichtlich bleibt
    if len(text) > 400:
        text = text[:397].rstrip() + "..."
    prefix = f"**[{frage}]** " if frage else ""
    # `location` nur als kleiner Pfad-Hinweis
    return f"- {prefix}{text}  \n  _({loc})_"


def _render_block(bibkey: str, entries: list[dict]) -> str:
    lines = [MARK_START, "", "## Transkript-Verortungen", ""]
    lines.append(
        "Automatisch aus `Literatur/_transkripte_index.json` erzeugt. "
        "**Diese Transkripte sind kuratierte Originalquellen** und "
        "sollten bei inhaltsgleichen Belegstellen bevorzugt gegenueber "
        "heuristisch gefundenen Textausschnitten verwendet werden."
    )
    lines.append("")

    # Gruppieren nach role - Haupttreffer zuerst
    role_order = ["existing_main", "chapter_main", "proposed_new_main",
                  "mentioned_existing", "mentioned_new"]
    grouped: dict[str, list[dict]] = {r: [] for r in role_order}
    for e in entries:
        r = e.get("role", "mentioned_existing")
        grouped.setdefault(r, []).append(e)

    for role in role_order:
        bucket = grouped.get(role, [])
        if not bucket:
            continue
        lines.append(f"### {ROLE_LABEL.get(role, role)}")
        lines.append("")
        for e in bucket:
            src = e.get("source_file", "?")
            lines.append(f"#### `{src}`")
            lines.append("")
            buch    = e.get("buch") or "—"
            chapter = e.get("chapter_title") or "—"
            authors = e.get("chapter_authors") or "—"
            pages   = e.get("pages") or "—"
            year    = e.get("year") or "—"
            transcript_file = e.get("transcript_file") or ""
            mention_cnt = e.get("mention_count")
            proposed = e.get("proposed_bibtex")

            lines.append(f"- **Buch:** {buch} ({year})")
            lines.append(f"- **Kapitel:** {chapter}")
            if authors != "—":
                lines.append(f"- **Autor:innen:** {authors}")
            lines.append(f"- **Seiten:** {pages}")
            if transcript_file:
                lines.append(f"- **Transkript-Datei:** `{transcript_file}`")
            if mention_cnt:
                lines.append(f"- **Anzahl Zitatstellen:** {mention_cnt}")
            rel = _fmt_relevance(e.get("relevance_per_question") or {})
            if rel:
                lines.append(f"- **Pruefungsfragen-Relevanz:** {rel}")

            hints = e.get("integration_hints") or []
            if hints:
                lines.append("")
                lines.append(
                    f"**Integration-Hints** ({e.get('integration_hints_count', len(hints))} "
                    f"gesamt, Anzeige gekappt):"
                )
                lines.append("")
                for h in hints[:12]:  # Anzeige kappen
                    lines.append(_fmt_hint(h))
            if proposed:
                lines.append("")
                lines.append("**Vorgeschlagener BibLaTeX-Eintrag (aus Transkript):**")
                lines.append("")
                lines.append("```bibtex")
                lines.append(proposed.strip())
                lines.append("```")
            lines.append("")

    lines.append(MARK_END)
    return "\n".join(lines)


def _inject(text: str, block: str) -> tuple[str, str]:
    """Ersetzt einen existierenden Transkript-Block oder fuegt ihn an
    der richtigen Stelle ein.
    Rueckgabe: (neuer_text, status) mit status in
    {'created','updated','unchanged'}.
    """
    if BLOCK_RE.search(text):
        # Callable statt String-Replacement, damit Backslash-Sequenzen
        # (z. B. `\textcite{trautmann2021haltung}` in Integration-Hints) nicht
        # als re-Template-Backreferences interpretiert werden.
        new = BLOCK_RE.sub(lambda _m: block, text, count=1)
        status = "unchanged" if new == text else "updated"
        return new, status

    # Nach CLAIMS-END einfuegen
    cm = CLAIMS_END_RE.search(text)
    if cm:
        at = cm.end()
        new = text[:at] + "\n\n" + block + "\n" + text[at:]
        return new, "created"

    # Fallback: nach Header-Trenner
    sep = HEADER_SEP_RE.search(text)
    if sep:
        at = sep.end()
        new = text[:at] + "\n" + block + "\n\n" + text[at:]
        return new, "created"

    # Defensiv: ganz oben einsetzen
    new = block + "\n\n" + text
    return new, "created"


def _ensure_folder(bibkey: str) -> Path | None:
    folder = LITERATUR / bibkey
    if not folder.is_dir():
        return None
    md = folder / "verified_quotes.md"
    if not md.is_file():
        return None
    return md


# ----- Main -------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Fuegt Transkript-Verortungen in verified_quotes.md ein.",
    )
    p.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.index.is_file():
        print(f"[Fehler] Index-Datei nicht gefunden: {args.index}",
              file=sys.stderr)
        return 2

    data = json.loads(args.index.read_text(encoding="utf-8"))
    mapping: dict[str, list[dict]] = data.get("bibkey_to_transkripte") or {}
    if not mapping:
        print("[Info] Index-Datei enthaelt kein 'bibkey_to_transkripte'.",
              file=sys.stderr)
        return 0

    print("integrate_transkripte.py")
    print(f"  Index:   {args.index}")
    print(f"  BibKeys: {len(mapping)}")
    print()

    stats = {"created": 0, "updated": 0, "unchanged": 0,
             "skipped_no_folder": 0, "skipped_empty": 0}

    for bibkey in sorted(mapping):
        entries = mapping[bibkey]
        if not entries:
            stats["skipped_empty"] += 1
            continue
        md = _ensure_folder(bibkey)
        if not md:
            stats["skipped_no_folder"] += 1
            print(f"  [skip] {bibkey:<38} (kein Ordner/verified_quotes.md)")
            continue
        text = md.read_text(encoding="utf-8")
        block = _render_block(bibkey, entries)
        new_text, status = _inject(text, block)
        if new_text != text:
            md.write_text(new_text, encoding="utf-8")
        stats[status] = stats.get(status, 0) + 1
        print(f"  [{status:<10}] {bibkey}  ({len(entries)} Transkript-Eintraege)")

    print()
    print("Zusammenfassung:")
    for k, v in stats.items():
        print(f"  {k:<22} {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
