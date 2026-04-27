#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""onboard_frage5.py - Datei-Operationen fuer Frage-5-Onboarding.

Kopiert PDFs+JSONs aus MPV/Literatur/Frage 5/ in Literatur/<bibkey>/.
Idempotent (skip falls Zieldatei existiert).

BibTeX-Eintraege und verified_quotes.md-Stubs werden separat erzeugt
(via Quellen.bib-Edit und write_to_file aus dem Cascade-Workflow).
"""
from __future__ import annotations
import shutil
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIT_REPO = HERE / "Literatur"
LIT_EXTERN = HERE.parent / "Literatur" / "Frage 5"
AGG_DIR = LIT_REPO / "_frage5_quellen_aggregate"

# (bibkey, ext_pdf, ext_json, dst_pdf_name, dst_json_name)
KANDIDATEN = [
    ("booth2019index",
     "IndexfürInklusion_Indikatoren_ZB01.01.pdf",
     "2003_BoothAinscow_IndexFuerInklusion_Indikatoren.json",
     "zb01_01_indikatorenfragebogen.pdf",
     "zb01_01_indikatorenfragebogen.json"),
    ("marti2015kompetenzfoerdernd",
     "2015_Marti_AchtMerkmaleeineskompetenzförderndenUnterrichts.pdf",
     "2015_Marti_AchtMerkmaleKompetenzfoerdernderUnterricht.json",
     "source.pdf", "metadata.json"),
    ("kummerwyss2017kooperativunterrichten",
     "2017_KummerWyss_Kooperativunterrichten.pdf",
     "2017_KummerWyss_KooperativUnterrichten.json",
     "source.pdf", "metadata.json"),
    ("phluzern2017tzi",
     "ZB_TZI.pdf",
     "2017_PHLuzern_TZI_ThemenzentrierteInteraktion.json",
     "source.pdf", "metadata.json"),
    ("reissenauerulsess2017anerkennendhandelnd",
     "ReissenauerUlsess-Schurda(2017)_LPhandelnanerkennend-2.pdf",
     "2017_ReissenauerUlsessSchurda_LPhandelnAnerkennend.json",
     "source.pdf", "metadata.json"),
    ("widmerwolf2018multiprofessionell",
     "2018_Widmer-Wolf_KooperationinmultiprofessionellenTeams.pdf",
     "2018_WidmerWolf_KooperationMultiprofessionelleTeams.json",
     "source.pdf", "metadata.json"),
    ("groschefussangelgraesel2020kokonstruktion",
     "2020_Groscheetal._ZfP_KokonstruktiveZA-Inklusion-2.pdf",
     "2020_Groscheetal_KokonstruktiveKooperation.json",
     "source.pdf", "metadata.json"),
    ("groschefussangelgraesel2020kokonstruktion",
     "ZB_WirkmodellderkonstruktivenKooperation.pdf",
     "2020_Groscheetal_WirkmodellKonstruktiveKooperation_ZB.json",
     "zb_wirkmodell_konstruktive_kooperation.pdf",
     "zb_wirkmodell_konstruktive_kooperation.json"),
    ("muellerboeschschaffnermenn2021udl",
     "2021_MüllerBösch_SchaffnerMenn_InklusiverUnterricht_UDL.pdf",
     "2021_MuellerBoesch_SchaffnerMenn_InklusiverUnterricht_UDL.json",
     "source.pdf", "metadata.json"),
    ("felder2022anerkennung",
     "Hedderichetal.2022-Felder-anerkennung-kpt15(2).pdf",
     "2022_Felder_Anerkennung.json",
     "source.pdf", "metadata.json"),
    ("cast2024udlguidelines",
     "UDLGuidelines2024.pdf",
     "2024_CAST_UDLGuidelines.json",
     "source.pdf", "metadata.json"),
]

AGGREGATE_FILES = ["analyze_pdf_sources.json", "muellerboesch_notes.txt"]


def find_extern(name: str) -> Path | None:
    nfc = unicodedata.normalize("NFC", name)
    for p in LIT_EXTERN.iterdir():
        if unicodedata.normalize("NFC", p.name) == nfc:
            return p
    return None


def copy_safe(src: Path, dst: Path) -> str:
    if dst.exists():
        return f"skip ({dst.stat().st_size // 1024} KB)"
    shutil.copy2(src, dst)
    return f"copied ({dst.stat().st_size // 1024} KB)"


def main() -> int:
    if not LIT_EXTERN.exists():
        print(f"ERR: extern fehlt: {LIT_EXTERN}", file=sys.stderr)
        return 2
    print(f"onboard_frage5.py")
    print(f"  extern: {LIT_EXTERN}")
    print(f"  ziel:   {LIT_REPO}\n")

    errors = 0
    for bibkey, ext_pdf, ext_json, dst_pdf, dst_json in KANDIDATEN:
        target_dir = LIT_REPO / bibkey
        target_dir.mkdir(parents=True, exist_ok=True)
        print(f"-- {bibkey}/{dst_pdf}")
        for label, ext_name, dst_name in [
            ("pdf ", ext_pdf, dst_pdf),
            ("json", ext_json, dst_json),
        ]:
            ext_path = find_extern(ext_name)
            if not ext_path:
                print(f"  {label}: MISSING extern: {ext_name}", file=sys.stderr)
                errors += 1
                continue
            status = copy_safe(ext_path, target_dir / dst_name)
            print(f"  {label}: {status}")

    # Aggregat
    AGG_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\n-- _frage5_quellen_aggregate/")
    for fname in AGGREGATE_FILES:
        src = LIT_EXTERN / fname
        if not src.exists():
            print(f"  {fname}: MISSING extern", file=sys.stderr)
            errors += 1
            continue
        status = copy_safe(src, AGG_DIR / fname)
        print(f"  {fname}: {status}")

    print(f"\nDone. errors={errors}")
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
