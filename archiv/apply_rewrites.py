"""apply_rewrites.py - Wendet REWRITES-Bloecke aus den Dossiers auf TeX an.

Liest dieselben YAML-Bloecke wie `collect_rewrites.py` (Single Source of Truth).
Im Default-Modus laeuft das Skript als **Dry-Run** und zeigt nur an, was
passieren wuerde — es wird nichts geschrieben. Mit `--apply` werden die
Aenderungen tatsaechlich vorgenommen und der Status im Dossier von `pending`
auf `applied` umgestellt.

Sicherheits-Checks vor jedem Apply:
  1. TeX-Datei existiert.
  2. Zeile `<line>` hat ein Vorkommen von `<old>`.
  3. Das Vorkommen ist eindeutig (genau 1 Treffer in dieser Zeile).
  4. Status ist `pending` — bereits applied/rejected wird uebersprungen.

Beispiele:

    # Dry-Run ueber alle pending Rewrites
    python apply_rewrites.py

    # Nur Rewrites aus einem Dossier dry-run
    python apply_rewrites.py --bibkey preckel2013hochbegabung

    # Nur eine spezifische Zeile, dry-run
    python apply_rewrites.py --bibkey preckel2013hochbegabung --line 650

    # Alle pending Rewrites tatsaechlich anwenden (ohne Prompt)
    python apply_rewrites.py --apply --yes

    # Eine einzelne Stelle mit Prompt anwenden
    python apply_rewrites.py --bibkey fischer2020begabungsfoerderung --line 1755 --apply
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from collect_rewrites import collect_all as collect_rewrites, Rewrite


HERE      = Path(__file__).resolve().parent
LITERATUR = HERE / "Literatur"


# ---------------------------------------------------------------------------
# Outcome-Tracking
# ---------------------------------------------------------------------------
@dataclass
class Outcome:
    rewrite: Rewrite
    status:  str          # "applied" | "would-apply" | "skip-not-found" |
                          # "skip-ambiguous" | "skip-already" | "skip-no-tex" |
                          # "skip-rejected" | "error"
    detail:  str = ""


# ---------------------------------------------------------------------------
# YAML-Status-Flip im Dossier (textbasiert, formaterhaltend)
# ---------------------------------------------------------------------------
REWRITES_BLOCK_RE = re.compile(
    r"(?P<prefix><!--\s*REWRITES-START\b[^>]*-->\s*(?:```yaml\s*\n)?)"
    r"(?P<body>.*?)"
    r"(?P<suffix>(?:\n```\s*)?<!--\s*REWRITES-END\s*-->)",
    re.DOTALL,
)


def flip_status_in_dossier(
    md_path:      Path,
    tex_file:     str,
    line_number:  int,
    new_status:   str,
) -> bool:
    """Setzt im Dossier den Status des passenden Eintrags auf `new_status`.

    Eindeutige Zuordnung erfolgt ueber das Tupel `(tex_file, line)`.
    Liefert True, wenn ein Status tatsaechlich geaendert wurde.
    """
    text  = md_path.read_text(encoding="utf-8")
    block = REWRITES_BLOCK_RE.search(text)
    if not block:
        return False

    body = block.group("body")

    # YAML-Liste teilen: jeder Eintrag beginnt mit `- ` am Zeilenanfang.
    # Wir nutzen einen Lookahead, um die Trenner an den Items zu lassen.
    parts = re.split(r"(?m)(?=^- )", body)
    changed = False
    for i, part in enumerate(parts):
        if not part.lstrip().startswith("- "):
            continue
        # Erlaube optional vorangestelltes `- ` (YAML-Listen-Marker), damit
        # auch das erste Feld eines Listeneintrags gematcht wird.
        tf_m = re.search(r"^(?:-\s+)?[ \t]*tex_file:\s*([^\s#]+)",
                         part, re.MULTILINE)
        ln_m = re.search(r"^(?:-\s+)?[ \t]*line:\s*(\d+)",
                         part, re.MULTILINE)
        if not (tf_m and ln_m):
            continue
        if tf_m.group(1).strip() != tex_file:
            continue
        if int(ln_m.group(1)) != line_number:
            continue
        new_part, n = re.subn(
            r"(^[ \t]*status:[ \t]*)pending\b",
            lambda m: m.group(1) + new_status,
            part, count=1, flags=re.MULTILINE,
        )
        if n > 0:
            parts[i] = new_part
            changed  = True
            break

    if not changed:
        return False

    new_body = "".join(parts)
    new_text = (
        text[:block.start("body")]
        + new_body
        + text[block.end("body"):]
    )
    md_path.write_text(new_text, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# Apply-Engine
# ---------------------------------------------------------------------------
def _read_tex(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines(keepends=True)


def _write_tex(path: Path, lines: list[str]) -> None:
    path.write_text("".join(lines), encoding="utf-8")


def evaluate(rewrite: Rewrite, tex_root: Path) -> tuple[Outcome, list[str] | None,
                                                        int | None, str | None]:
    """Pruefe einen Rewrite ohne ihn auszufuehren.

    Liefert (Outcome, lines_buffer_or_None, line_index_or_None, new_line_or_None).
    Der Buffer ist None bei Skip; sonst die TeX-Zeilen mit der vorbereiteten Aenderung
    (line_index ist 0-basiert, new_line ist die neue Zeile inkl. Newline).
    """
    if rewrite.status == "applied":
        return Outcome(rewrite, "skip-already", "Status bereits 'applied'."), None, None, None
    if rewrite.status == "rejected":
        return Outcome(rewrite, "skip-rejected", "Status 'rejected'."), None, None, None

    tex_path = tex_root / rewrite.tex_file
    if not tex_path.is_file():
        return Outcome(rewrite, "skip-no-tex",
                       f"TeX-Datei fehlt: {tex_path}"), None, None, None

    if rewrite.line is None:
        return Outcome(rewrite, "error",
                       "Kein 'line'-Wert im Rewrite-Block."), None, None, None

    lines = _read_tex(tex_path)
    if rewrite.line < 1 or rewrite.line > len(lines):
        return Outcome(rewrite, "skip-not-found",
                       f"Zeile {rewrite.line} existiert nicht (Datei hat "
                       f"{len(lines)} Zeilen)."), None, None, None

    line_idx = rewrite.line - 1
    line     = lines[line_idx]
    count    = line.count(rewrite.old)

    if count == 0:
        return Outcome(rewrite, "skip-not-found",
                       f"`old`-String nicht in Zeile {rewrite.line} gefunden."
                       ), None, None, None
    if count > 1:
        return Outcome(rewrite, "skip-ambiguous",
                       f"`old`-String {count}x in Zeile {rewrite.line} — "
                       f"nicht eindeutig ersetzbar."), None, None, None

    new_line = line.replace(rewrite.old, rewrite.new, 1)
    return Outcome(rewrite, "would-apply", "OK"), lines, line_idx, new_line


def apply_one(rewrite: Rewrite, tex_root: Path,
              literatur_root: Path, dry_run: bool) -> Outcome:
    outcome, lines, line_idx, new_line = evaluate(rewrite, tex_root)
    if outcome.status != "would-apply":
        return outcome
    assert lines is not None and line_idx is not None and new_line is not None

    if dry_run:
        return outcome

    # Tatsaechlich schreiben.
    tex_path = tex_root / rewrite.tex_file
    lines[line_idx] = new_line
    _write_tex(tex_path, lines)

    # Status im Dossier auf 'applied' flippen.
    md_path = literatur_root / rewrite.source_dossier / "verified_quotes.md"
    flipped = flip_status_in_dossier(
        md_path, rewrite.tex_file, rewrite.line, "applied"
    )

    detail = "geschrieben"
    if not flipped:
        detail += " (WARN: Status-Flip im Dossier fehlgeschlagen)"
    return Outcome(rewrite, "applied", detail)


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------
ICON = {
    "applied":         "[OK ]",
    "would-apply":     "[DRY]",
    "skip-not-found":  "[SK!]",
    "skip-ambiguous":  "[SK?]",
    "skip-already":    "[ -- ]",
    "skip-rejected":   "[ -- ]",
    "skip-no-tex":     "[SK!]",
    "error":           "[ERR]",
}


def print_outcome(o: Outcome) -> None:
    r = o.rewrite
    head = (f"  {ICON.get(o.status, o.status):<7} {r.tex_file}:{r.line}  "
            f"<- {r.source_dossier}")
    print(head)
    if o.status in ("would-apply", "applied"):
        print(f"           old: {r.old}")
        print(f"           new: {r.new}")
        if o.detail and o.status == "applied":
            print(f"           -> {o.detail}")
    elif o.detail:
        print(f"           -> {o.detail}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Wendet REWRITES-Bloecke auf TeX-Dateien an.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("Beispiele:", 1)[-1] if "Beispiele:" in __doc__ else None,
    )
    p.add_argument("--apply", action="store_true",
                   help="Aenderungen tatsaechlich schreiben (ohne diesen "
                        "Schalter ist alles Dry-Run).")
    p.add_argument("--bibkey", metavar="KEY",
                   help="Nur Rewrites aus diesem Dossier verarbeiten.")
    p.add_argument("--line", type=int, metavar="N",
                   help="Nur Rewrites mit dieser Zeilennummer "
                        "(typisch zusammen mit --bibkey).")
    p.add_argument("--tex-root", default=str(HERE), metavar="DIR",
                   help=f"Wurzelverzeichnis fuer relative tex_file-Pfade "
                        f"(Default: {HERE}).")
    p.add_argument("--yes", action="store_true",
                   help="Bei --apply: keine interaktive Bestaetigung anfordern.")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if not LITERATUR.is_dir():
        print(f"[ERR] {LITERATUR} fehlt.", file=sys.stderr)
        return 1
    tex_root = Path(args.tex_root)
    if not tex_root.is_dir():
        print(f"[ERR] tex-root fehlt: {tex_root}", file=sys.stderr)
        return 1

    rewrites = collect_rewrites(LITERATUR)
    if args.bibkey:
        rewrites = [r for r in rewrites if r.source_dossier == args.bibkey]
    if args.line is not None:
        rewrites = [r for r in rewrites if r.line == args.line]

    pending = [r for r in rewrites if r.status == "pending"]
    other   = [r for r in rewrites if r.status != "pending"]

    print("apply_rewrites.py")
    print(f"  Modus:      {'APPLY' if args.apply else 'DRY-RUN'}")
    print(f"  Filter:     "
          f"bibkey={args.bibkey or '(alle)'}  line={args.line or '(alle)'}")
    print(f"  Rewrites:   {len(rewrites)} gefunden  "
          f"({len(pending)} pending, {len(other)} sonstige)")

    if not pending:
        print("\n  Keine pending Rewrites zu verarbeiten.")
        for r in other:
            print_outcome(Outcome(r, f"skip-{r.status}", f"Status '{r.status}'."))
        return 0

    # Dry-Run / Vorschau immer erst durchgehen.
    print("\n--- Vorschau ---")
    plan: list[tuple[Outcome, list[str] | None, int | None, str | None]] = []
    for r in pending:
        result = evaluate(r, tex_root)
        plan.append(result)
        print_outcome(result[0])
    for r in other:
        print_outcome(Outcome(r, f"skip-{r.status}", f"Status '{r.status}'."))

    will_apply = [(o, ls, li, nl) for (o, ls, li, nl) in plan
                  if o.status == "would-apply"]
    print("\n--- Zusammenfassung Vorschau ---")
    print(f"  Anwendbar:  {len(will_apply)}")
    print(f"  Skip:       {len(plan) - len(will_apply)}")

    if not args.apply:
        print("\n[Dry-Run] Keine Aenderungen geschrieben. "
              "Mit `--apply` ausfuehren.")
        return 0
    if not will_apply:
        print("\nNichts anzuwenden.")
        return 0

    if not args.yes:
        prompt = (f"\n{len(will_apply)} Rewrite(s) tatsaechlich schreiben? "
                  f"[y/N] ")
        try:
            answer = input(prompt).strip().lower()
        except EOFError:
            answer = ""
        if answer not in ("y", "yes", "j", "ja"):
            print("Abgebrochen — keine Aenderungen geschrieben.")
            return 0

    print("\n--- Anwenden ---")
    n_applied = 0
    n_failed  = 0
    for o, _ls, _li, _nl in will_apply:
        result = apply_one(o.rewrite, tex_root, LITERATUR, dry_run=False)
        print_outcome(result)
        if result.status == "applied":
            n_applied += 1
        else:
            n_failed += 1

    print("\n--- Ergebnis ---")
    print(f"  Geschrieben:  {n_applied}")
    print(f"  Fehlgeschlagen: {n_failed}")
    print("\nHinweis: Bitte `python collect_rewrites.py` und "
          "`python build_index.py` neu laufen lassen, damit `REWRITES.md` "
          "und `_INDEX.md` den neuen Status reflektieren.")
    return 0 if n_failed == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
