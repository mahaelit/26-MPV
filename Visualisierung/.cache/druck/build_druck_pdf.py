#!/usr/bin/env python3
"""Build Druck-PDF (Originalseiten) + Audit-Dokument.

Output:
  - /MPV/Druckdokument_Kernliteratur_2026.pdf   (one above repo root)
  - Visualisierung/Druckdokument_Audit.md       (audit document)
  - Visualisierung/.cache/druck/_build_log.md   (full build log)

Rules:
  - Only ORIGINAL PDF pages (no AI text, no OCR).
  - Order = order of Kernliteratur per Vortrag (V1 -> V5).
  - For each source: separator page (cover) + extracted pages.
  - Sources without local PDF -> separator page only ("FEHLT - bitte beschaffen").
"""
import os, json, re, fitz

BASE = "/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV/26-MPV"
PARENT = os.path.dirname(BASE)  # /MPV
OUT_PDF = os.path.join(PARENT, "Druckdokument_Kernliteratur_2026.pdf")
OUT_AUDIT = os.path.join(BASE, "Visualisierung", "Druckdokument_Audit.md")
LOG = os.path.join(BASE, "Visualisierung/.cache/druck/_build_log.md")

# Per-source page-mapping: idx_for_book_page lookup
# offset: idx = book_page - offset    (e.g. offset=1 means S.35 -> idx 34)
# manual_map: {book_page: idx} explicit mapping
# take_all: True means use all PDF pages (when PDF == exact chapter)
MAP = {
    # V1
    "stamm2025vonuntennachoben":              {"multi_pdf_map": [
        ("Literatur/stamm2025vonuntennachoben/s035-057.pdf", 35, [36, 37]),
        ("Literatur/stamm2025vonuntennachoben/s058-079.pdf", 58, [58, 59, 60, 61, 62]),
    ]},
    "preckel2013hochbegabung":                {"offset": 42, "note": "PDF nur S.42-50 (9 S.); Vortrag fordert 15-47 - GROSSE LUECKE"},
    "gauckreimann2021psychdiagnostik":        {"offset": 239},  # 11 S., target 239-245
    "haag2018leistungsstanddiagnostik":       {"offset": -1},   # eBook
    "baumschader2021twice":                   {"offset": 588},
    "koop2025herkunft":                       {"offset": 1, "container": "pauly2025"},   # in Pauly Sammelband
    "webb2020doppeldiagnosen":                {"offset": 87},
    "warneckehauke2020bildungsgerechtigkeit": {"offset": 0, "container": "fischer2020"}, # Sammelband mit echter Buchpagination im Header
    "kellerkoller2013erkennen":               {"offset": 1, "note": "ist 2011er Auflage"},
    "muelleroppliger2021paeddiagnostik":      {"offset": 224},
    "kappus2010migration":                    {"manual_map": {63:0, 64:1, 65:2, 66:3, 67:4, 68:5, 69:6, 70:7, 74:11},
                                               "note": "Bildscan, idx-Annahme: idx 0 = S.63"},
    # V2
    "saegesserwyss2021grafinkrahmenmodell":   {"missing": True, "note": "Verzeichnis ohne PDF"},
    "nottbusch2017graphomotorik":             {"manual_map": {128:0, 129:1, 130:2, 131:3, 132:4, 133:5, 134:6, 135:7, 136:8},
                                               "note": "PDF enthaelt vermutlich gesamtes Kapitel"},
    "hurschler2020handschriftbeurteilung":    {"offset": 1},
    "gold2018lesenkannmanlernen":             {"offset": 67, "note": "3 PDFs - hier nur S67-88; S50-53 + S62 separat",
                                               "extra_files": [
                                                  "Literatur/gold2018lesenkannmanlernen/Gold2018 Migrationsprache S.50-53.pdf",
                                                  "Literatur/gold2018lesenkannmanlernen/Gold2018 schwacheleser S62-66.pdf",
                                               ]},
    "lehwald2017motivation":                  {"offset": 141},
    # V3
    "grossrieder2010anerkennung":             {"take_all": True, "note": "Kapitel-PDF, Bildscan"},
    "baudson2021wasdenken":                   {"take_all": True, "note": "Kapitel-PDF (14 S., target 15)"},
    "kuhl2021begabungbildungbeziehung":       {"offset": 185},
    "wagener2021bfhemmendfoerdernd":          {"offset": 418},
    "behrensen2019inklusive":                 {"offset": 86},
    "kuhl2019diversitaet":                    {"offset": 36, "note": "Header zeigt 36 fuer idx 0; S.35 evtl. nicht im PDF"},
    "boosnuenning2022interethnisch":          {"offset": 51},
    "kesselshannover2015gleichaltrige":       {"manual_map": {288: 5}},
    "tschoppbuholzergruetter2022intergruppenkontakt": {"offset": 35},
    "baumert2022freundschaftwerte":           {"offset": 36},
    "evers2025stress":                        {"offset": 21},
    # V4
    "buholzerkummerwyss2010reaktionen":       {"offset": 78},
    "muelleroppliger2021plurale":             {"offset": 32},
    "muelleroppliger2021begabungsmodelle":    {"offset": 204},
    "reisrenzullimueller2021sem":             {"offset": 333},
    "muelleroppliger2021adaptive":            {"offset": 374, "note": "Dateiname S.274-385 - tatsaechlich 374-385"},
    "schulteterhardt2020potenzialentwicklung": {"offset": 253, "note": "PDF S.253-272 (Sammelband-Auszug 20 S.); Target S.264-267"},
    "hoyer2013begabung":                      {"offset": 2},
    "grossenbacher2014integrative":           {"offset": 317},
    # V5
    "weigand2021person":                      {"offset": 46},   # PDF heisst 'S.59' aber enthaelt S.46-59
    "horvath2021elite":                       {"offset": 77},
    "muellerboeschschaffnermenn2021udl":      {"offset": 93},
    "macha2019gender":                        {"offset": 160},
    "groschefussangelgraesel2020kokonstruktion": {"manual_map": {
                                                  463: 2, 464: 3, 465: 4, 466: 5, 467: 6,
                                                  469: 8, 470: 9, 471: 10, 472: 11},
                                               "note": "Bildscan, idx-Mapping geschaetzt: idx 0 = S.461"},
    "nguyensliwka2021massnahmen":             {"offset": 348},
    "widmerwolf2018multiprofessionell":       {"manual_map": {
                                                  299: 0, 300: 1, 301: 2, 302: 3, 303: 4,
                                                  308: 9, 309: 10},
                                               "note": "Bildscan, idx-Mapping geschaetzt: idx 0 = S.299"},
    "kosoroklabhart2021voneltern":            {"manual_map": {14: 8, 15: 9, 38: 27, 39: 28},
                                               "note": "eigene Buch-Pagination, Mapping aus Header-Detection"},
    "baudson2025besserfinden":                {"offset": 1, "container": "pauly2025"},
    # Missing entirely
    "stamm2021fehlenderblick":                {"missing": True},
    "kellerkoller2025hellekoepfe":            {"missing": True},
    "stern2025intelligenz":                   {"missing": True, "note": "nur als docx vorhanden"},
    "greiten2021underachievement":            {"missing": True, "note": "im Handbuch Begabung 2021, kein Einzel-PDF"},
    "weigand2021separativ":                   {"missing": True, "note": "im Handbuch Begabung 2021, kein Einzel-PDF"},
    "sedmak2021bildungsgerechtigkeit":        {"missing": True, "note": "im Handbuch Begabung 2021, kein Einzel-PDF"},
}


def parse_page_spec(spec):
    pages = []
    spec = spec.replace("\\,", " ").replace("–", "-").replace("--", "-")
    for chunk in re.split(r"[,;]", spec):
        chunk = chunk.strip()
        if not chunk: continue
        if "-" in chunk:
            a, b = chunk.split("-", 1)
            try:
                pages.extend(range(int(a.strip()), int(b.strip()) + 1))
            except ValueError: pass
        else:
            try: pages.append(int(chunk))
            except ValueError: pass
    return pages


def make_separator_page(out_doc, vortrag, pos, total_in_v, bibkey, pages_spec,
                        n_pages_extracted, src_path, missing=False, note=""):
    """Insert an A4 separator page summarising the next source."""
    page = out_doc.new_page(width=595, height=842)  # A4 portrait in points
    # Header bar
    page.draw_rect(fitz.Rect(0, 0, 595, 90), color=(0.15, 0.15, 0.55), fill=(0.15, 0.15, 0.55))
    page.insert_text((40, 40), f"VORTRAG {vortrag}", fontname="helv",
                     fontsize=14, color=(1, 1, 1))
    page.insert_text((40, 65), f"Kernliteratur Position {pos} / {total_in_v}",
                     fontname="helv", fontsize=11, color=(0.95, 0.95, 0.95))
    if missing:
        page.insert_text((400, 40), "FEHLT", fontname="helv",
                         fontsize=18, color=(1, 0.6, 0.6))
        page.insert_text((400, 65), "bitte beschaffen", fontname="helv",
                         fontsize=10, color=(0.95, 0.95, 0.95))
    # Title
    page.insert_text((40, 150), bibkey, fontname="hebo", fontsize=22,
                     color=(0.1, 0.1, 0.3))
    # Pages range
    page.insert_text((40, 200), "Pflichtseiten:", fontname="helv",
                     fontsize=11, color=(0.4, 0.4, 0.4))
    page.insert_text((40, 222), f"S. {pages_spec}", fontname="hebo",
                     fontsize=14, color=(0, 0, 0))
    # Extracted info
    page.insert_text((40, 270), "Extrahierte Originalseiten:", fontname="helv",
                     fontsize=11, color=(0.4, 0.4, 0.4))
    if missing:
        page.insert_text((40, 292), "(keine Originalseiten verfuegbar)",
                         fontname="hebo", fontsize=14, color=(0.7, 0, 0))
    else:
        page.insert_text((40, 292), f"{n_pages_extracted} Seite(n) aus Original-PDF",
                         fontname="hebo", fontsize=14, color=(0, 0.4, 0))
    # Source path
    if src_path:
        page.insert_text((40, 340), "Quelle (lokal):", fontname="helv",
                         fontsize=11, color=(0.4, 0.4, 0.4))
        # wrap path
        max_chars = 75
        rest = src_path
        y = 362
        while rest:
            page.insert_text((40, y), rest[:max_chars], fontname="cour",
                             fontsize=9, color=(0, 0, 0))
            rest = rest[max_chars:]
            y += 13
    # Note
    if note:
        page.insert_text((40, 700), "Hinweis:", fontname="helv",
                         fontsize=11, color=(0.4, 0.4, 0.4))
        page.insert_text((40, 720), note[:100], fontname="heit", fontsize=10,
                         color=(0, 0, 0))
        if len(note) > 100:
            page.insert_text((40, 735), note[100:200], fontname="heit",
                             fontsize=10, color=(0, 0, 0))
    # Footer
    page.insert_text((40, 800), "Druckdokument Kernliteratur Vortraege 1-5",
                     fontname="helv", fontsize=8, color=(0.5, 0.5, 0.5))


# Load Kernliteratur
with open(os.path.join(BASE, "Visualisierung/.cache/druck/kernliteratur.json")) as f:
    KERN = json.load(f)

out_doc = fitz.open()
log_lines = ["# Druck-PDF Build Log\n"]
audit_lines = [
    "# Druckdokument – Audit der Beschaffungslücken\n",
    "Dieses Audit listet **alle Kernliteratur-Quellen, deren Originalseiten",
    "noch nicht (vollstaendig) im Workspace vorliegen** und daher fuer das",
    "Druckdokument fotografiert oder als Verlags-PDF beschafft werden muessen.\n",
    "Reihenfolge = Reihenfolge der Kernliteratur in den Vortraegen.\n",
    "**Stand:** automatisiert generiert aus Vortrag1-5.md + Workspace-Inventar.\n",
    "---\n",
]
audit_count = 0
total_extracted = 0
seen = set()

for v_num, v_key in enumerate(["V1", "V2", "V3", "V4", "V5"], 1):
    items = KERN[v_key]["items"]
    n = len(items)
    log_lines.append(f"\n## {v_key} ({n} Quellen, Soll {KERN[v_key]['total']}\u00a0S.)\n")
    audit_lines.append(f"\n## {v_key} – Vortrag {v_num}\n")
    audit_v_count = 0
    for pos, r in enumerate(items, 1):
        bk = r["bibkey"]
        spec = r["pages"]
        target_pages = parse_page_spec(spec)
        cfg = MAP.get(bk, {})

        if bk in seen:
            log_lines.append(f"  - {pos}. `{bk}` -> skip (bereits in V{seen_at[bk]} #{seen_pos[bk]})")
            continue

        # Determine extracted pages
        extracted_pages = []  # list of (path, idx)
        missing = cfg.get("missing", False)
        note = cfg.get("note", "")
        primary_path = None

        if missing:
            log_lines.append(f"  - {pos}. `{bk}` -> MISSING ({note})")
            audit_count += 1
            audit_v_count += 1
            audit_lines.append(
                f"### {audit_count}. `{bk}` (V{v_num} #{pos})\n"
                f"- **Pflichtseiten:** S. {spec} ({r['count']}\u00a0S.)\n"
                f"- **Status:** PDF nicht im Workspace\n"
                + (f"- **Hinweis:** {note}\n" if note else "")
                + "- **Auftrag:** Original-Buchseiten fotografieren / als Verlags-PDF beschaffen.\n"
            )
        elif "multi_pdf_map" in cfg:
            # list of (rel_path, offset, [target_pages])
            for rel, off, tgts in cfg["multi_pdf_map"]:
                full = os.path.join(BASE, rel)
                if not os.path.exists(full):
                    log_lines.append(f"  - {pos}. `{bk}` -> multi file missing: {rel}")
                    continue
                d = fitz.open(full)
                for p in tgts:
                    idx = p - off
                    if 0 <= idx < d.page_count:
                        extracted_pages.append((full, idx))
                d.close()
            primary_path = cfg["multi_pdf_map"][0][0]
        else:
            # Determine primary path from MAP or inventory
            inv_match = None
            with open(os.path.join(BASE, "Visualisierung/.cache/druck/kernliteratur_inventar.json")) as f:
                inv = json.load(f)
            for vv in inv.values():
                for e in vv:
                    if e["bibkey"] == bk and e.get("rel_path") and e["path_status"] == "OK":
                        inv_match = e
                        break
                if inv_match:
                    break
            if inv_match is None:
                # source path missing - treat as missing
                log_lines.append(f"  - {pos}. `{bk}` -> NO INVENTORY MATCH")
                audit_count += 1
                audit_v_count += 1
                audit_lines.append(
                    f"### {audit_count}. `{bk}` (V{v_num} #{pos})\n"
                    f"- **Pflichtseiten:** S. {spec}\n"
                    f"- **Status:** keine Inventarisierung\n"
                )
                make_separator_page(out_doc, v_num, pos, n, bk, spec, 0,
                                    None, missing=True, note=note or "no inventory")
                seen.add(bk)
                continue

            primary_path = inv_match["rel_path"]
            primary_full = inv_match["abs_path"]

            # Determine indices via cfg
            indices_to_take = []
            if cfg.get("take_all"):
                d = fitz.open(primary_full)
                indices_to_take = list(range(d.page_count))
                d.close()
            elif "manual_map" in cfg:
                d = fitz.open(primary_full)
                for p in target_pages:
                    if p in cfg["manual_map"]:
                        idx = cfg["manual_map"][p]
                        if 0 <= idx < d.page_count:
                            indices_to_take.append(idx)
                d.close()
            elif "offset" in cfg:
                d = fitz.open(primary_full)
                for p in target_pages:
                    idx = p - cfg["offset"]
                    if 0 <= idx < d.page_count:
                        indices_to_take.append(idx)
                d.close()
            else:
                # No mapping - take all
                d = fitz.open(primary_full)
                indices_to_take = list(range(d.page_count))
                d.close()

            for i in indices_to_take:
                extracted_pages.append((primary_full, i))

            # Extra files (e.g. multiple Gold PDFs)
            for ef in cfg.get("extra_files", []):
                full = os.path.join(BASE, ef)
                if os.path.exists(full):
                    d = fitz.open(full)
                    for i in range(d.page_count):
                        extracted_pages.append((full, i))
                    d.close()

        # Build cover + insert pages
        if missing or len(extracted_pages) == 0:
            make_separator_page(out_doc, v_num, pos, n, bk, spec, 0,
                                primary_path, missing=True, note=note)
        else:
            make_separator_page(out_doc, v_num, pos, n, bk, spec,
                                len(extracted_pages), primary_path,
                                missing=False, note=note)
            # Insert pages from each source file
            current_src = None
            current_doc = None
            for src, i in extracted_pages:
                if src != current_src:
                    if current_doc is not None:
                        current_doc.close()
                    current_doc = fitz.open(src)
                    current_src = src
                out_doc.insert_pdf(current_doc, from_page=i, to_page=i)
            if current_doc is not None:
                current_doc.close()

        log_lines.append(
            f"  - {pos}. `{bk}` ({spec}) -> {len(extracted_pages)} Seiten extrahiert"
            + (f"  HINWEIS: {note}" if note else "")
        )
        if not missing:
            total_extracted += len(extracted_pages)

        # Detect partial coverage -> also list in audit
        if not missing and len(extracted_pages) < r["count"] and r["count"] > 0:
            audit_count += 1
            audit_v_count += 1
            audit_lines.append(
                f"### {audit_count}. `{bk}` (V{v_num} #{pos}) – TEILWEISE\n"
                f"- **Pflichtseiten:** S. {spec} ({r['count']}\u00a0S.)\n"
                f"- **Im Druck-PDF:** {len(extracted_pages)} Seiten extrahiert\n"
                f"- **Lücke:** {r['count'] - len(extracted_pages)} Seiten fehlen\n"
                + (f"- **Hinweis:** {note}\n" if note else "")
                + f"- **Quelle (lokal):** `{primary_path}`\n"
                + "- **Auftrag:** Fehlende Buchseiten fotografieren und nachreichen.\n"
            )

        # Track first-occurrence
        seen.add(bk)
        try:
            seen_at[bk] = v_num; seen_pos[bk] = pos
        except NameError:
            seen_at = {bk: v_num}; seen_pos = {bk: pos}

    if audit_v_count == 0:
        audit_lines.append("_Keine Beschaffungsluecken._\n")

# Save outputs
out_doc.save(OUT_PDF, deflate=True, garbage=4)
out_doc.close()

audit_lines.append(f"\n---\n\n**Bilanz:** {audit_count} Quelle(n) muessen beschafft werden.\n")
audit_lines.append(f"**Erfolgreich extrahiert:** {total_extracted} Seiten in `{OUT_PDF}`.\n")
audit_lines.append(f"**Soll laut Vortraegen:** 549 Seiten Kernliteratur.\n")

with open(OUT_AUDIT, "w") as f:
    f.write("\n".join(audit_lines))
with open(LOG, "w") as f:
    f.write("\n".join(log_lines))

print(f"Druck-PDF: {OUT_PDF}")
print(f"Audit:     {OUT_AUDIT}")
print(f"Log:       {LOG}")
print(f"Total extrahiert: {total_extracted} Seiten")
print(f"Audit-Faelle:     {audit_count}")
