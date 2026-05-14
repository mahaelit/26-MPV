#!/usr/bin/env python3
"""Per Kernquelle: PDF lokalisieren, Seiten extrahieren, Status ermitteln.

Output: kernliteratur_inventar.json (für Druck-PDF + Audit)
"""
import os, json, re, glob
import fitz  # PyMuPDF

BASE = "/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV/26-MPV"
LIT = os.path.join(BASE, "Literatur")

# Manuelles Mapping bibkey -> (relativer PDF-Pfad, first_book_page_at_idx_0)
# first_book_page_at_idx_0 = die Buchseite, die in idx 0 des PDF steht (None = unbekannt/Bildscan)
MANUAL = {
    # V1
    "stamm2021fehlenderblick":              (None, None),  # nicht im Workspace; nur _outline + verified_quotes
    "stamm2025vonuntennachoben":            ("stamm2025vonuntennachoben/s035-057.pdf", 35),  # zusätzl. s058-079.pdf
    "preckel2013hochbegabung":              ("preckel2013hochbegabung/Preckel_Baudson 2013hochbegabung,kap2.2 S.42-50.pdf", 42),
    "gauckreimann2021psychdiagnostik":      ("gauckreimann2021psychdiagnostik/Gauckreimann2021päddiagnostik s.239-249.pdf", 239),
    "haag2018leistungsstanddiagnostik":     ("maehler2018diagnostik/source.pdf", None),  # eBook, Buchseite muss aus Inhalt erkannt werden
    "kellerkoller2025hellekoepfe":          (None, None),  # nicht im Workspace
    "baumschader2021twice":                 ("baumschader2021twice/Baum:schader twice exceptionality 588-600.pdf", 588),
    "koop2025herkunft":                     ("pauly2025wasistfair/2025_Pauly_Was_ist_fair.pdf", None),  # idx-mapping nötig (Sammelband)
    "stern2025intelligenz":                 (None, None),  # nur docx
    "webb2020doppeldiagnosen":              ("webb2020doppeldiagnosen/kap02_fehldiagnosen_doppeldiagnosen_s087-094.pdf", 87),
    "warneckehauke2020bildungsgerechtigkeit": ("fischer2020begabungsfoerderung/source.pdf", None),  # Sammelband
    "kellerkoller2013erkennen":             ("kellerkoller2011erkennen/source.pdf", None),  # andere Auflage
    "muelleroppliger2021paeddiagnostik":    ("muelleroppliger2021paeddiagnostik/Smülleroppliger2021paedagogischediagnostik S.224-238.pdf", 224),
    "kappus2010migration":                  ("kappus2010migration/source.pdf", None),
    # V2
    "saegesserwyss2021grafinkrahmenmodell": ("sägesserwyssetal2022grafomotorikschulischeinklusion", None),  # Verzeichnis prüfen
    "nottbusch2017graphomotorik":           ("nottbusch2017graphomotorik/source.pdf", None),
    "hurschler2020handschriftbeurteilung":  ("hurschler2020handschriftbeurteilung/source.pdf", None),
    "gold2018lesenkannmanlernen":           ("gold2018lesenkannmanlernen/Gold2018lesenkannmanlernen S67-88.pdf", 67),
    "lehwald2017motivation":                ("lehwald2017motivation/Lehwald2017 motbeg S.141-165.pdf", 141),
    "greiten2021underachievement":          (None, None),  # Handbuch S.546-553, kein Einzel-PDF
    # V3
    "grossrieder2010anerkennung":           ("grossrieder2010anerkennung/Grossrieder2010Nerkennung in buholzer kummerwyss.pdf", None),
    "baudson2021wasdenken":                 ("baudson2021wasdenken/source.pdf", None),
    "kuhl2021begabungbildungbeziehung":     ("Kuhl2021bildungbegabung/Kuhl2021begabildungbeziehungsusbperspsychsicht S.185-202.pdf", 185),
    "wagener2021bfhemmendfoerdernd":        ("wagener2021bfförderndhemmend/Wagener2021bfhemmendförderndimklassenklntext S418-424.pdf", 418),
    "behrensen2019inklusive":               ("behrensen2019inklusive/source.pdf", None),
    "kuhl2019diversitaet":                  ("kuhl2019diversitaet/source.pdf", None),
    "boosnuenning2022interethnisch":        ("boosnuenning2022interethnisch/source.pdf", None),
    "kesselshannover2015gleichaltrige":     ("kesselshannover2015gleichaltrige/source.pdf", None),
    "tschoppbuholzergruetter2022intergruppenkontakt": ("tschoppgruetterbuholzer2022intergruppenkontakt/source.pdf", None),
    "baumert2022freundschaftwerte":         ("baumert2022freundschaftwerte/source.pdf", None),
    "evers2025stress":                      ("evers2025stress/source.pdf", None),
    # V4
    "buholzerkummerwyss2010reaktionen":     ("buholzer2010allegleich/source_s078-085.pdf", 78),
    "muelleroppliger2021plurale":           ("muelleroppliger2021plurale/Vmüller2021pluralrgsinklusionbildungsgerechtigkeit.pdf", 32),
    "muelleroppliger2021begabungsmodelle":  ("muelleroppliger2021handbuch/Mülleroppliger2021begabungsmpdeöle S.204-219.pdf", 204),
    "reisrenzullimueller2021sem":           ("reisrenzullimüller2021SEM/Reisrenzullimüller2021SEM S.333-345.pdf", 333),
    "weigand2021separativ":                 (None, None),  # nur Outline + Notes
    "muelleroppliger2021adaptive":          ("mülleroppliger2021adaptivelernarchitektur/Mülleroppliger2021adaptivelernarchizektur S.274-385.pdf", 374),
    "schulteterhardt2020potenzialentwicklung": ("fischer2020begabungsfoerderung/excerpts/022_individuelle_potenzialentwicklung_durch_staerkenor.pdf", None),
    "hoyer2013begabung":                    ("hoyer2013begabung/source.pdf", None),
    "sedmak2021bildungsgerechtigkeit":      (None, None),  # nur Outline + Notes
    "grossenbacher2014integrative":         ("stamm2014handbuch/Grossenbacher tettenborn 2014 in stamm Talent und Begabung in der VS der deutschsprachigen Schweiz 317-325.pdf", 317),
    # V5
    "weigand2021person":                    ("weigand2021person/Weigand2021begabungbildungperson S.59.pdf", 46),
    "horvath2021elite":                     ("horvath2021elite/Horvath2021elitebegabungsozialeungleichkeitgerechtigkwitsfragen S 77-85.pdf", 77),
    "muellerboeschschaffnermenn2021udl":    ("muellerboeschschaffnermenn2021udl/source.pdf", 93),
    "macha2019gender":                      ("macha2019gender/source.pdf", None),
    "groschefussangelgraesel2020kokonstruktion": ("groschefussangelgraesel2020kokonstruktion/source.pdf", None),
    "nguyensliwka2021massnahmen":           ("nguyensliwka2021massnahmenkompetenzlp/Nguyensliwka2021massnahmenlpbf S 348-356.pdf", 348),
    "widmerwolf2018multiprofessionell":     ("widmerwolf2018multiprofessionell/source.pdf", None),
    "kosoroklabhart2021voneltern":          ("kosoroklabhart2021voneltern/source.pdf", None),
    "baudson2025besserfinden":              ("pauly2025wasistfair/2025_Pauly_Was_ist_fair.pdf", None),
}


def detect_book_page(pdf_path):
    """Try to detect first_page heuristically by reading text from idx 0."""
    try:
        doc = fitz.open(pdf_path)
        for i in range(min(3, doc.page_count)):
            t = doc[i].get_text("text").strip()
            if t:
                # Find first standalone integer near start that could be a page number
                m = re.search(r"(?:^|\n)\s*(\d{1,3})\s*(?:\n|$)", t[:300])
                if m:
                    n = int(m.group(1))
                    if 10 <= n <= 800:
                        return i, n
        return None, None
    except Exception:
        return None, None


def page_status(pdf_path):
    """Return list of (idx, has_text:bool, first_chars)."""
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        return None, str(e)
    pages = []
    for i in range(doc.page_count):
        t = doc[i].get_text("text").strip()
        pages.append({"idx": i, "has_text": bool(t), "len": len(t), "snippet": t[:60]})
    return pages, None


def parse_page_spec(spec):
    """'46--59' -> [46..59]; '14--15, 38--39' -> [14,15,38,39]"""
    pages = []
    spec = spec.replace("\\,", " ").replace("–", "-").replace("--", "-")
    for chunk in re.split(r"[,;]", spec):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            a, b = chunk.split("-", 1)
            try:
                a, b = int(a.strip()), int(b.strip())
                pages.extend(range(a, b + 1))
            except ValueError:
                pass
        else:
            try:
                pages.append(int(chunk))
            except ValueError:
                pass
    return pages


# Load Kernliteratur
with open(os.path.join(BASE, "Visualisierung/.cache/druck/kernliteratur.json")) as f:
    KERN = json.load(f)

inventar = {}
already_seen = set()  # to track first occurrence (count=0 means double-counting)
for v in ["V1", "V2", "V3", "V4", "V5"]:
    inventar[v] = []
    for r in KERN[v]["items"]:
        bk = r["bibkey"]
        spec = r["pages"]
        cnt = r["count"]
        target_pages = parse_page_spec(spec)
        rel, first = MANUAL.get(bk, (None, None))
        path = os.path.join(LIT, rel) if rel else None
        if path and not os.path.exists(path):
            path_status = "MISSING"
        elif not path:
            path_status = "NO_LOCAL"
        else:
            path_status = "OK"

        entry = {
            "vortrag": v,
            "bibkey": bk,
            "spec": spec,
            "target_pages": target_pages,
            "count": cnt,
            "first_occurrence": bk not in already_seen,
            "rel_path": rel,
            "abs_path": path,
            "path_status": path_status,
            "first_book_page_at_idx_0": first,
        }
        already_seen.add(bk)

        if path and path_status == "OK":
            pages, err = page_status(path)
            if err:
                entry["error"] = err
            else:
                entry["pdf_pages_total"] = len(pages)
                entry["pdf_pages_with_text"] = sum(1 for p in pages if p["has_text"])
                # Auto-detect first page if not provided
                if first is None:
                    auto_idx, auto_pg = detect_book_page(path)
                    entry["auto_detected_first"] = (auto_idx, auto_pg)
                    if auto_pg is not None:
                        first = auto_pg - auto_idx
                # Compute target idx range
                if first is not None:
                    target_idx = [p - first for p in target_pages]
                    valid = [i for i in target_idx if 0 <= i < len(pages)]
                    entry["resolved_first_book_page_at_idx_0"] = first
                    entry["target_idx"] = valid
                    entry["coverage_ok"] = len(valid) == len(target_pages)
                else:
                    # Fall back: use all pages or none
                    entry["target_idx"] = list(range(len(pages)))
                    entry["coverage_ok"] = (len(pages) >= len(target_pages))
                entry["pages_have_text_at_target"] = (
                    [pages[i]["has_text"] for i in entry.get("target_idx", [])]
                    if entry.get("target_idx") else []
                )
        inventar[v].append(entry)

with open(os.path.join(BASE, "Visualisierung/.cache/druck/kernliteratur_inventar.json"), "w") as f:
    json.dump(inventar, f, indent=2, ensure_ascii=False)

# Lesbares Audit-Vorbereitungs-Markdown
lines = ["# Inventar Kernliteratur (Phase 2)\n"]
total_first_occ_ok = 0
total_first_occ_missing = 0
for v in ["V1", "V2", "V3", "V4", "V5"]:
    lines.append(f"\n## {v}\n")
    lines.append("| # | bibkey | Seiten | n | first | PDF | Status | Text? |")
    lines.append("|--|--|--|--|--|--|--|--|")
    for i, e in enumerate(inventar[v], 1):
        if not e["first_occurrence"]:
            note = "(2. Auftreten – Doppelzählung)"
        else:
            note = ""
        text_ok = ""
        if "pages_have_text_at_target" in e and e["pages_have_text_at_target"]:
            n_ok = sum(e["pages_have_text_at_target"])
            n_total = len(e["pages_have_text_at_target"])
            text_ok = f"{n_ok}/{n_total}"
        rel = e["rel_path"] or "—"
        lines.append(
            f"| {i} | `{e['bibkey']}` | {e['spec']} | {e['count']} | "
            f"{e.get('first_book_page_at_idx_0', '?')} | "
            f"`{rel}` | {e['path_status']} | {text_ok} {note} |"
        )
        if e["first_occurrence"]:
            if e["path_status"] == "OK":
                total_first_occ_ok += 1
            else:
                total_first_occ_missing += 1

lines.append(f"\n**Bilanz Erstauftreten:** {total_first_occ_ok} OK, {total_first_occ_missing} fehlend/online.\n")

with open(os.path.join(BASE, "Visualisierung/.cache/druck/kernliteratur_inventar.md"), "w") as f:
    f.write("\n".join(lines))

print("OK")
