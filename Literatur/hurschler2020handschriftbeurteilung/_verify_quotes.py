#!/usr/bin/env python3
"""Pass-2-Verifikation: Volltext-Extraktion + Wortgetreuheit der mpv.tex-Zitate gegen Volltext."""
from pathlib import Path
import re
import fitz

HERE = Path(__file__).parent
doc = fitz.open(str(HERE / "source.pdf"))
print(f"PDF: {doc.page_count} Seiten")

# Volltext pro Seite extrahieren
pages = {}
for i in range(doc.page_count):
    pages[i+1] = doc[i].get_text()

# Volltext speichern
full = "".join(f"\n\n=== Seite {i} ===\n{txt}" for i, txt in pages.items())
(HERE / "_volltext.txt").write_text(full)
print(f"Volltext gespeichert: {len(full)} chars")

def norm(s):
    """Whitespace-normalisieren für robusten Vergleich."""
    return re.sub(r"\s+", " ", s).strip().lower()

# mpv.tex-Behauptungen, die wortgetreu zu pruefen sind
behauptungen = [
    # (locator, behauptung_kurz, suchstring)
    ("S. 3", "Z01 Geläufigkeit/Arbeitsspeicher",
     "Je geläufiger die Schüler*innen verschriften, desto weniger Aufmerksamkeit muss auf die schreibmotorischen Aspekte gerichtet werden"),
    ("S. 3", "Z01b Kognitive Ressourcen frei",
     "desto mehr kognitive Ressourcen werden frei für die hierarchiehöheren Prozesse des Schreibens"),
    ("S. 1", "Z02 Abstract: Leserlichkeit/Geläufigkeit",
     "Leserlichkeit und Geläufigkeit"),
    ("S. 1", "Z02b nicht notwendigerweise zusammen",
     "diese beiden Komponenten nicht notwendigerweise zusammenhängen"),
    ("S. 4", "Z03 Unverzichtbare Grundfertigkeit",
     "Weil Handschrift also im Primarschulalter eine unverzichtbare Grundfertigkeit"),
    ("S. 11", "Z04 DASH",
     "DASH"),
    ("S. 11", "Z04b mehrdimensional fünf Teilaufgaben",
     "Geläufigkeit mehrdimensional über fünf Teilaufgaben"),
    ("S. 16", "Z05 Hattie-Effektstärke",
     "Effektstärke von d = 1,44"),
    ("S. 2-3", "Z06 prozedurale Lernprozesse",
     "prozedurale Lernprozesse"),
    ("S. 2-3", "Z06b orthografische Codes",
     "orthografische"),
    ("S. 3 oder 11", "Z07 zwei Achsen / Hauptkriterien",
     "Hauptkriterien"),
]

print("\n=== WORTGETREU-PRUEFUNG ===")
for loc, label, needle in behauptungen:
    n_needle = norm(needle)
    found_pages = []
    for pg, txt in pages.items():
        if n_needle in norm(txt):
            found_pages.append(pg)
    if found_pages:
        print(f"OK   {label} (erwartet {loc}) -> Seite(n) {found_pages}")
    else:
        print(f"MISS {label} (erwartet {loc}, nicht gefunden!)")
        print(f"     Suchstring: {needle!r}")

# Spezifisch S. 2 + 3 anzeigen, um Locator zu klaeren
print("\n=== Volltext S. 2 (Auszug) ===")
print(pages.get(2, "")[:1500])
print("\n=== Volltext S. 3 (Auszug) ===")
print(pages.get(3, "")[:1500])
print("\n=== Volltext S. 11 (Auszug) ===")
print(pages.get(11, "")[:1500])

doc.close()
