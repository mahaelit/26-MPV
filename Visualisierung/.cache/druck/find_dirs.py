#!/usr/bin/env python3
"""Find Literatur/* dirs for each missing bibkey using local list."""
import os, json
BASE = "/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV/26-MPV"

with open(os.path.join(BASE, "Visualisierung/.cache/druck/_lit_dirs.txt")) as f:
    dirs = [l.strip() for l in f if l.strip()]
dirs_lower = {d.lower(): d for d in dirs}

# All bibkeys missing or NO_LOCAL from inventar
keys = [
    "stamm2021fehlenderblick","stamm2025vonuntennachoben","gauckreimann2021psychdiagnostik",
    "kellerkoller2025hellekoepfe","baumschader2021twice","koop2025herkunft","stern2025intelligenz",
    "webb2020doppeldiagnosen","warneckehauke2020bildungsgerechtigkeit","kellerkoller2013erkennen",
    "saegesserwyss2021grafinkrahmenmodell","nottbusch2017graphomotorik","hurschler2020handschriftbeurteilung",
    "gold2018lesenkannmanlernen","greiten2021underachievement",
    "grossrieder2010anerkennung","baudson2021wasdenken","wagener2021bfhemmendfoerdernd",
    "behrensen2019inklusive","kuhl2019diversitaet","boosnuenning2022interethnisch",
    "kesselshannover2015gleichaltrige","tschoppbuholzergruetter2022intergruppenkontakt",
    "baumert2022freundschaftwerte","evers2025stress","weigand2021separativ",
    "sedmak2021bildungsgerechtigkeit",
]

# Aliases: bibkey -> tatsächlicher Verzeichnisname im Workspace (Schreibvarianten)
ALIAS = {
    "saegesserwyss2021grafinkrahmenmodell": "sägesserwyssetal2022grafomotorikschulischeinklusion",
    "tschoppbuholzergruetter2022intergruppenkontakt": "tschoppgruetterbuholzer2022intergruppenkontakt",
    "kellerkoller2013erkennen": "kellerkoller2011erkennen",
    "koop2025herkunft": "koopseddig2021frueheserkennen",
}

result = {}
for k in keys:
    if k in ALIAS:
        d = ALIAS[k]
        if d in dirs:
            result[k] = [d]
            continue
    # exact prefix or contains key
    matches = [d for d in dirs if d.lower().startswith(k.lower())]
    if not matches:
        kk = k[:12].lower()
        matches = [d for d in dirs if kk in d.lower()]
    result[k] = matches

# Write report and inspect contents per match
lines = []
for k, ms in result.items():
    if not ms:
        lines.append(f"## {k}\nNO MATCH")
        continue
    lines.append(f"## {k}")
    for m in ms:
        p = os.path.join(BASE, "Literatur", m)
        try:
            files = sorted(os.listdir(p))
        except Exception as e:
            lines.append(f"  - {m}/ (ERR: {e})")
            continue
        pdfs = [f for f in files if f.lower().endswith((".pdf", ".docx", ".epub"))]
        lines.append(f"  - `{m}/`")
        for f in pdfs[:6]:
            sz = os.path.getsize(os.path.join(p, f))
            lines.append(f"     - {f}  ({sz:,} B)")
    lines.append("")

with open(os.path.join(BASE, "Visualisierung/.cache/druck/_pdf_search.md"), "w") as f:
    f.write("\n".join(lines))
with open(os.path.join(BASE, "Visualisierung/.cache/druck/_pdf_search.json"), "w") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
print("OK")
