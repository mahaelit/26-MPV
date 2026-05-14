#!/usr/bin/env python3
"""Parse Kernliteratur from Vortrag1-5.md, write structured plan to disk."""
import re, json, os
BASE = "/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV/26-MPV"

result = {}
for n in [1, 2, 3, 4, 5]:
    fn = os.path.join(BASE, f"Visualisierung/Vortrag{n}.md")
    with open(fn) as f:
        t = f.read()
    parts = re.split(r"\\textbf\{St[uü]tzliteratur", t, maxsplit=1)
    head = parts[0]
    head = re.split(r"Kernliteratur", head, maxsplit=1)[-1]
    items = re.findall(
        r"\\item\[\\cite\{([^}]+)\}\](.*?)(?=\\item\[\\cite\{|\\end\{litdesc)",
        head, re.S)
    rows = []
    grand_total = 0
    for k, body in items:
        body_clean = re.sub(r"\s+", " ", body).strip()
        # Pages
        page_match = re.search(r"S\.[\\,\s]*([0-9\-\\,\s–]+?)\s*\(", body_clean)
        cnt_match = re.search(r"\((\d+)[\\,\s]*S\.\)", body_clean)
        pages = re.sub(r"\\,", " ", page_match.group(1)).strip() if page_match else "?"
        pages = re.sub(r"\s+", " ", pages).strip().rstrip(",")
        cnt = int(cnt_match.group(1)) if cnt_match else 0
        grand_total += cnt
        rows.append({"bibkey": k, "pages": pages, "count": cnt})
    result[f"V{n}"] = {"items": rows, "total": grand_total}

with open(os.path.join(BASE, "Visualisierung/.cache/druck/kernliteratur.json"), "w") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

# Lesbare Übersicht
with open(os.path.join(BASE, "Visualisierung/.cache/druck/kernliteratur_uebersicht.md"), "w") as f:
    grand = 0
    for v in ["V1", "V2", "V3", "V4", "V5"]:
        f.write(f"\n## {v} ({len(result[v]['items'])} Kernquellen, {result[v]['total']}\u00a0S.)\n\n")
        f.write("| # | BibKey | Seiten | Anzahl |\n|--|--|--|--|\n")
        for i, r in enumerate(result[v]["items"], 1):
            f.write(f"| {i} | `{r['bibkey']}` | {r['pages']} | {r['count']} |\n")
        grand += result[v]["total"]
    f.write(f"\n**Gesamt: {grand} Seiten**\n")
print("OK")
