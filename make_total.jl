#!/usr/bin/env julia
# make_total.jl
# Schreibt alle relevanten Projektdateien in eine einzige TOTAL.txt

const PROJEKTVERZEICHNIS = @__DIR__

const DATEIEN = [
    # Karten Fragen 1–5
    joinpath(PROJEKTVERZEICHNIS, "KARTEN", "karten frage 1.tex"),
    joinpath(PROJEKTVERZEICHNIS, "KARTEN", "karten frage 2.tex"),
    joinpath(PROJEKTVERZEICHNIS, "KARTEN", "karten frage 3.tex"),
    joinpath(PROJEKTVERZEICHNIS, "KARTEN", "karten frage 4.tex"),
    joinpath(PROJEKTVERZEICHNIS, "KARTEN", "karten frage 5.tex"),
    # Vorträge 1–5
    joinpath(PROJEKTVERZEICHNIS, "VISUALISIERUNG", "VORTRAG_1.md"),
    joinpath(PROJEKTVERZEICHNIS, "VISUALISIERUNG", "VORTRAG_2.md"),
    joinpath(PROJEKTVERZEICHNIS, "VISUALISIERUNG", "VORTRAG_3.md"),
    joinpath(PROJEKTVERZEICHNIS, "VISUALISIERUNG", "VORTRAG_4.md"),
    joinpath(PROJEKTVERZEICHNIS, "VISUALISIERUNG", "VORTRAG_5.md"),
    # Hauptdokumente
    joinpath(PROJEKTVERZEICHNIS, "mpv.tex"),
    joinpath(PROJEKTVERZEICHNIS, "mpv_abgabedokument.tex"),
    # Bibliographie
    joinpath(PROJEKTVERZEICHNIS, "Quellen.bib"),
]

const AUSGABEDATEI = joinpath(PROJEKTVERZEICHNIS, "TOTAL.txt")

function trennlinie(dateiname::String)
    linie = "=" ^ 80
    return "\n$linie\n### $dateiname\n$linie\n\n"
end

function main()
    println("MPV → TOTAL.txt")
    println("Ausgabe: $AUSGABEDATEI\n")

    open(AUSGABEDATEI, "w") do out
        write(out, "TOTAL.txt – Alle Projektdateien\n")
        write(out, "Erstellt: $(Dates.now())\n")
        write(out, "=" ^ 80 * "\n")

        for pfad in DATEIEN
            relativ = relpath(pfad, PROJEKTVERZEICHNIS)

            if !isfile(pfad)
                @warn "Datei nicht gefunden, wird übersprungen: $relativ"
                write(out, trennlinie(relativ))
                write(out, "[DATEI NICHT GEFUNDEN]\n")
                continue
            end

            inhalt = try
                read(pfad, String)
            catch e
                @warn "Lesefehler bei $relativ: $e"
                "[LESEFEHLER: $e]\n"
            end

            write(out, trennlinie(relativ))
            write(out, inhalt)

            # Sicherstellen dass die letzte Zeile mit Zeilenumbruch endet
            if !endswith(inhalt, "\n")
                write(out, "\n")
            end

            groesse_kb = round(filesize(pfad) / 1024; digits=1)
            println("  ✓  $relativ  ($groesse_kb KB)")
        end

        write(out, "\n" * "=" ^ 80 * "\n")
        write(out, "### ENDE TOTAL.txt\n")
        write(out, "=" ^ 80 * "\n")
    end

    gesamt_kb = round(filesize(AUSGABEDATEI) / 1024; digits=1)
    println("\nFertig! TOTAL.txt → $gesamt_kb KB")
end

# Dates wird in der Standardbibliothek mitgeliefert
import Dates

main()
