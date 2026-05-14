#!/usr/bin/env python3
"""Compare new V1 supplementary PDFs vs current workspace state."""
import os, fitz

NEW_DIR = "/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV/Literatur/FehlendeSeiten MPV/Definitiv MPV Literatur Frage 1"
OLD_BASE = "/Users/i/Library/CloudStorage/OneDrive-dxy/Kunden/fxyz/SHP/Masterarbeit Vertiefung OneDrive/MPV/26-MPV/Literatur"

# bibkey -> (new_filename, old_rel_path or None, current_audit_status)
ITEMS = [
    # Critical missing
    ("stamm2021fehlenderblick", "stamm2021fehlenderblick aufbegabteminoritäten 576-585.pdf", None, "MISSING"),
    ("kellerkoller2025hellekoepfe", "kellerkoller2025Helle köpfe mit migrationshintergrund S. 76-78.pdf", None, "MISSING"),
    # Critical partial -> now complete
    ("preckel2013hochbegabung_part1", "Preckelbaudson2013hbS.15-38.pdf", "preckel2013hochbegabung/Preckel_Baudson 2013hochbegabung,kap2.2 S.42-50.pdf", "TEILWEISE 6/33"),
    ("preckel2013hochbegabung_part2", "Preckelbaudson2013hb S.39-47.pdf", "preckel2013hochbegabung/Preckel_Baudson 2013hochbegabung,kap2.2 S.42-50.pdf", "TEILWEISE 6/33"),
    # Haag two precise files
    ("haag2018_part1", "haag2018diagnostik_bei_migrantinnen_und_migranten 153-165.pdf", "maehler2018diagnostik/source.pdf", "OK 13/15"),
    ("haag2018_part2", "haag2013diagnostik_bei_migrantinnen_und_migranten-187-188.pdf", "maehler2018diagnostik/source.pdf", "OK 13/15"),
    # Stern still only docx
    ("stern2025intelligenz", "Stern2025InterviewIntelligenzforscherin.docx", None, "MISSING (docx only)"),
    # Already covered
    ("baumschader2021twice", "Baum:schader twice exceptionality 588-600.pdf", "baumschader2021twice/Baum:schader twice exceptionality 588-600.pdf", "OK"),
    ("gauckreimann2021", "Gauckreimann2021psychologischeagnostik s.239-249.pdf", "gauckreimann2021psychdiagnostik/Gauckreimann2021päddiagnostik s.239-249.pdf", "OK"),
    ("kappus2010", "Kappus2010Umgangmitmigrationsbedingterheteroinkummerwyssbuholzer S.63-70.pdf", "kappus2010migration/source.pdf", "OK 9/9"),
    ("kellerkoller2013", "Kellerkoller2013BegabtemitMigration_Infoblatt.pdf", "kellerkoller2011erkennen/source.pdf", "OK"),
    ("muelleroppliger2021bm", "Mülleroppliger2021begabungsmodelle S.204-219.pdf", "muelleroppliger2021handbuch/Mülleroppliger2021begabungsmpdeöle S.204-219.pdf", "OK"),
    ("muelleroppliger2021pd", "Smülleroppliger2021paedagogischediagnostik S.224-238.pdf", "muelleroppliger2021paeddiagnostik/Smülleroppliger2021paedagogischediagnostik S.224-238.pdf", "OK"),
    ("stamm2025_part1", "Stamm2025vonuntennachoben S.37-38.pdf", "stamm2025vonuntennachoben/s035-057.pdf", "OK"),
    ("stamm2025_part2", "Stamm2025vonuntennachoben58-62.pdf", "stamm2025vonuntennachoben/s058-079.pdf", "OK"),
    ("webb2020", "Webb2020doppeldiagnosenkap2. S.87-94.pdf", "webb2020doppeldiagnosen/kap02_fehldiagnosen_doppeldiagnosen_s087-094.pdf", "OK"),
    ("koop2025", "koop2025_Pauly_Was_ist_fair S.64-67.pdf", "pauly2025wasistfair/2025_Pauly_Was_ist_fair.pdf", "OK"),
    ("warneckehauke2020", "warnekehauke2020inFischer_et_al_2020_Begabungsfoerderung242-253.pdf", "fischer2020begabungsfoerderung/source.pdf", "OK"),
]

print(f"{'STATUS':<8} {'NEW':>4} {'OLD':>5}  BIBKEY  ->  AUDIT-STATUS  ->  EFFECT")
print("=" * 100)
for label, new_name, old_rel, audit in ITEMS:
    new_path = os.path.join(NEW_DIR, new_name)
    if not os.path.exists(new_path):
        print(f"NOTFOUND  -    -      {label}")
        continue
    if new_name.endswith(".docx"):
        n = "doc"
    else:
        d = fitz.open(new_path)
        n = d.page_count
        d.close()
    if old_rel is None:
        eff = "+++ FÜLLT KOMPLETT-LÜCKE"
        old = "-"
    else:
        old_path = os.path.join(OLD_BASE, old_rel)
        if os.path.exists(old_path):
            d = fitz.open(old_path)
            old = d.page_count
            d.close()
        else:
            old = "missing"
        eff = "(bereits abgedeckt)" if "OK" in audit else "+ erweitert/präziser"
    print(f"{audit[:8]:<8} {str(n):>4} {str(old):>5}  {label}  ->  {eff}")
