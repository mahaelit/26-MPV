#!/usr/bin/env julia
# -*- coding: utf-8 -*-
"""
export_repo_snapshot.jl

Strukturierter Snapshot aller relevanten Code-, Markdown- und TeX-Dateien
des Repos in eine einzige .txt-Datei. Nuetzlich als Kontext-Export (z.B. fuer
LLM-Prompts oder als Uebergabe-Beleg).

Aufrufe:
  julia export_repo_snapshot.jl                         # Standard
  julia export_repo_snapshot.jl --output snap.txt       # anderer Zielpfad
  julia export_repo_snapshot.jl --include-literatur     # zusaetzlich Literatur/*.md
  julia export_repo_snapshot.jl --max-bytes 50000       # grosse Dateien kappen
  julia export_repo_snapshot.jl --no-toc                # ohne Inhaltsverzeichnis

Benoetigt keine externen Pakete (reine stdlib).
"""

using Dates
using Printf

const REPO_ROOT = @__DIR__

# Dateiendungen, die aufgenommen werden (ohne Punkt)
# Python-Skripte sind bewusst ausgeschlossen (siehe README-Hinweis).
const INCLUDE_EXTS = Set([
    "jl", "md", "tex", "bib",
    "toml", "yml", "yaml", "cfg", "ini",
    "sh", "ps1", "bat",
])

# Komplette Ordner, die nie betreten werden
const EXCLUDE_DIRS = Set([
    ".git", ".github", ".vscode", ".idea",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "venv", ".venv", "env", ".env",
    "node_modules", "dist", "build", ".next",
    "aptos-font", "_archiv_phase0",
])

# Einzelne Dateinamen, die ausgeschlossen werden (exakt)
const EXCLUDE_FILES = Set([
    "repo_snapshot.txt",  # Eigenes Output nicht wieder einbeziehen
])

# Auto-generierte Reports: werden bei --slim / --no-generated-reports weggelassen.
# Inhaltlich redundant, weil aus mpv.tex + verified_quotes.md + Quellen.bib ableitbar.
const GENERATED_REPORT_FILES = Set([
    "PRUEFUNGSKOMPENDIUM.md",
    "ERSATZ_VORSCHLAEGE.md",
    "BESCHAFFUNG.md",
    "QUELLEN_INVENTAR.md",
    "TRANSKRIPTE_UEBERSICHT.md",
    "REWRITES.md",
    "EXTERN_ABGLEICH.md",
    "FRAGEN_ABSTIMMUNG.md",
])

# Literatur-Ordner: standardmaessig EINGESCHLOSSEN (verified_quotes.md etc.).
# Mit --no-literatur komplett ueberspringen.
const LITERATUR_DIR = "Literatur"
const LITERATUR_INCLUDE_NAMES = Set([
    "verified_quotes.md",
    "_outline.md",
    "_INDEX.md",
])

# LaTeX-Artefakte, die zwar eine erlaubte Extension haetten, aber nicht gewollt sind
const LATEX_JUNK_EXTS = Set([
    "aux", "bbl", "bcf", "blg", "glg", "log", "out",
    "run.xml", "synctex.gz", "toc", "err", "fls", "fdb_latexmk",
])

# Default-Output
const DEFAULT_OUTPUT = "repo_snapshot.txt"

# =============================================================================
# CLI-Parsing
# =============================================================================

mutable struct Config
    output::String
    include_literatur::Bool
    include_generated_reports::Bool
    include_outlines::Bool
    max_bytes::Int            # 0 = unbegrenzt
    emit_toc::Bool
    verbose::Bool
end

function parse_args(args::Vector{String})::Config
    # Default: Literatur + Reports + Outlines AN. Mit --slim alles Redundante raus.
    cfg = Config(DEFAULT_OUTPUT, true, true, true, 0, true, false)
    i = 1
    while i <= length(args)
        a = args[i]
        if a == "--output" || a == "-o"
            i += 1
            cfg.output = args[i]
        elseif a == "--include-literatur"
            cfg.include_literatur = true  # Default; als Kompatibilitaets-Flag belassen
        elseif a == "--no-literatur"
            cfg.include_literatur = false
        elseif a == "--no-generated-reports"
            cfg.include_generated_reports = false
        elseif a == "--no-outlines"
            cfg.include_outlines = false
        elseif a == "--slim"
            # Kompakt fuer LLM-Kontexte: nur Originale + handgeschriebene Zitate
            cfg.include_generated_reports = false
            cfg.include_outlines = false
        elseif a == "--max-bytes"
            i += 1
            cfg.max_bytes = parse(Int, args[i])
        elseif a == "--no-toc"
            cfg.emit_toc = false
        elseif a == "--verbose" || a == "-v"
            cfg.verbose = true
        elseif a == "--help" || a == "-h"
            print_help()
            exit(0)
        else
            error("Unbekanntes Argument: $a (siehe --help)")
        end
        i += 1
    end
    return cfg
end

function print_help()
    println("""
    export_repo_snapshot.jl - Strukturierter Repo-Snapshot als Textdatei.

    Enthaelt per Default: .jl, .md, .tex, .bib (+ Config-Formate) im Root UND
    verified_quotes.md / _outline.md / _INDEX.md unter Literatur/.
    .py-Dateien werden bewusst NICHT einbezogen.

    Optionen:
      -o, --output PATH           Zielpfad (Default: $DEFAULT_OUTPUT)
          --slim                  Kompaktmodus fuer LLM-Kontexte:
                                   ohne auto-generierte Reports + ohne _outline.md
                                   (spart ca. 300 KB / 75k Tokens)
          --no-generated-reports  Nur die 7 auto-generierten Reports weglassen
                                   (PRUEFUNGSKOMPENDIUM, BESCHAFFUNG, ERSATZ_*, usw.)
          --no-outlines           Nur die _outline.md-Dateien unter Literatur weglassen
          --no-literatur          Literatur/ komplett weglassen
          --include-literatur     (Default an; Kompatibilitaets-Flag)
          --max-bytes N           Inhalt pro Datei auf N Bytes kappen (0 = unbegrenzt)
          --no-toc                Kein Inhaltsverzeichnis am Anfang
      -v, --verbose               Mehr Logs
      -h, --help                  Diese Hilfe

    Empfohlen fuer Claude/LLM-Kontexte:
      julia export_repo_snapshot.jl --slim
    """)
end

# =============================================================================
# Datei-Sammlung
# =============================================================================

"""Liefert `true`, wenn `path` aufgenommen werden soll."""
function is_included(relpath::String, cfg::Config)::Bool
    # Ordner-Ausschluesse greifen woanders (in walk). Hier nur Datei-Checks.
    name = basename(relpath)
    if name in EXCLUDE_FILES
        return false
    end

    # LaTeX-Junk (inkl. mehrteiliger Extensions wie .run.xml, .synctex.gz)
    namelower = lowercase(name)
    for junk in LATEX_JUNK_EXTS
        if endswith(namelower, "." * junk)
            return false
        end
    end

    # Literatur-Sonderbehandlung
    parts = splitpath(relpath)
    if !isempty(parts) && parts[1] == LITERATUR_DIR
        if !cfg.include_literatur
            return false
        end
        if !(name in LITERATUR_INCLUDE_NAMES)
            return false
        end
        if name == "_outline.md" && !cfg.include_outlines
            return false
        end
        return true
    end

    # Auto-generierte Reports (im Root) optional ausschliessen
    if !cfg.include_generated_reports && name in GENERATED_REPORT_FILES
        return false
    end

    # Standard: Extension-basiert
    ext = lowercase(last(splitext(name)))
    if startswith(ext, ".")
        ext = ext[2:end]
    end
    return ext in INCLUDE_EXTS
end

"""Rekursives Walk mit Ordner-Ausschluessen. Gibt relative Pfade (Unix-Style)."""
function collect_files(root::String, cfg::Config)::Vector{String}
    results = String[]
    for (dir, dirs, files) in walkdir(root; topdown = true)
        # Ordner-Filter: In-place auf `dirs` wirkt, weil topdown=true
        filter!(d -> !(d in EXCLUDE_DIRS), dirs)
        for f in files
            absfile = joinpath(dir, f)
            rel = relpath(absfile, root)
            rel_unix = replace(rel, '\\' => '/')
            if is_included(rel_unix, cfg)
                push!(results, rel_unix)
            end
        end
    end
    sort!(results)
    return results
end

# =============================================================================
# Schreiben
# =============================================================================

function fence_lang(relpath::String)::String
    ext = lowercase(last(splitext(relpath)))
    if startswith(ext, ".")
        ext = ext[2:end]
    end
    return get(Dict(
        "py" => "python", "jl" => "julia", "md" => "markdown",
        "tex" => "latex", "bib" => "bibtex",
        "toml" => "toml", "yml" => "yaml", "yaml" => "yaml",
        "sh" => "bash", "ps1" => "powershell", "bat" => "batch",
    ), ext, "")
end

function human_size(bytes::Integer)::String
    bytes < 1024 && return "$(bytes) B"
    kb = bytes / 1024
    kb < 1024 && return @sprintf("%.1f KB", kb)
    return @sprintf("%.2f MB", kb / 1024)
end

function write_header(io::IO, root::String, files::Vector{String}, cfg::Config)
    total = sum(filesize(joinpath(root, f)) for f in files; init = 0)
    println(io, "═"^80)
    println(io, "REPO SNAPSHOT")
    println(io, "═"^80)
    println(io, "Repo-Root        : ", root)
    println(io, "Generiert am     : ", Dates.format(now(), "yyyy-mm-dd HH:MM:SS"))
    println(io, "Julia-Version    : ", VERSION)
    println(io, "Dateien          : ", length(files))
    println(io, "Gesamtgroesse    : ", human_size(total))
    println(io, "Include-Literatur: ", cfg.include_literatur)
    println(io, "Include-Reports  : ", cfg.include_generated_reports)
    println(io, "Include-Outlines : ", cfg.include_outlines)
    if cfg.max_bytes > 0
        println(io, "Max. Bytes/Datei : ", cfg.max_bytes, " (grosse Dateien werden gekappt)")
    end
    println(io, "═"^80)
    println(io)
end

function write_toc(io::IO, root::String, files::Vector{String})
    println(io, "─"^80)
    println(io, "INHALT ($(length(files)) Dateien)")
    println(io, "─"^80)
    # Gruppiert nach Top-Level-Ordner
    grouped = Dict{String, Vector{String}}()
    for f in files
        parts = splitpath(f)
        key = length(parts) == 1 ? "." : parts[1]
        push!(get!(grouped, key, String[]), f)
    end
    for key in sort(collect(keys(grouped)))
        println(io, "\n  [", key, "]")
        for f in grouped[key]
            size_str = human_size(filesize(joinpath(root, f)))
            @printf(io, "    %-70s %10s\n", f, size_str)
        end
    end
    println(io)
end

function write_file_section(io::IO, root::String, relpath::String, cfg::Config)
    abspath_ = joinpath(root, relpath)
    fsize = filesize(abspath_)
    mtime_str = Dates.format(Dates.unix2datetime(mtime(abspath_)), "yyyy-mm-dd HH:MM")
    lang = fence_lang(relpath)

    println(io, "═"^80)
    @printf(io, "FILE: %s  (%s, mtime %s)\n", relpath, human_size(fsize), mtime_str)
    println(io, "═"^80)
    println(io)

    content = try
        read(abspath_, String)
    catch e
        "<<< FEHLER BEIM LESEN: $e >>>"
    end

    truncated = false
    if cfg.max_bytes > 0 && sizeof(content) > cfg.max_bytes
        content = first(content, cfg.max_bytes)
        truncated = true
    end

    if !isempty(lang)
        println(io, "```", lang)
    else
        println(io, "```")
    end
    # Mindestens ein newline nach content
    print(io, content)
    if !endswith(content, "\n")
        println(io)
    end
    println(io, "```")
    if truncated
        println(io, "⚠ [Inhalt gekappt bei ", cfg.max_bytes, " Bytes]")
    end
    println(io)
end

# =============================================================================
# Main
# =============================================================================

function main()
    cfg = parse_args(ARGS)
    root = REPO_ROOT

    cfg.verbose && println(stderr, "Scan von ", root)
    files = collect_files(root, cfg)
    cfg.verbose && println(stderr, "Gefunden: ", length(files), " Dateien")

    # Output-Pfad auflösen (relativ zum Repo-Root, falls nicht absolut)
    out = isabspath(cfg.output) ? cfg.output : joinpath(root, cfg.output)

    open(out, "w") do io
        write_header(io, root, files, cfg)
        if cfg.emit_toc
            write_toc(io, root, files)
        end
        for f in files
            cfg.verbose && println(stderr, "  + ", f)
            write_file_section(io, root, f, cfg)
        end
    end

    total_out = filesize(out)
    println("[OK] -> ", out, "  (", human_size(total_out), ", ", length(files), " Dateien)")
end

main()
