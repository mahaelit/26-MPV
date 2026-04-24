# Notiz zu `hoyer2013begabung/`

## Versehentliche Dublette im OneDrive

Im OneDrive-Quellordner liegt unter diesem BibKey eine PDF-Datei

> `Helle köpfe mit migkellerkoller 2025 3auflagerationshitnergrund warum sie oft unerkannt bleiben.pdf`  
> (6,86 MB, MD5 `757fd5cd62bf5e0559b79e4658482b52`)

die **byte-identisch** ist mit der Datei

> `Literatur/huser2025lichtblick/KellerKollerHelle köpfe mit migkellerkoller 2025 3auflagerationshitnergrund warum sie oft unerkannt bleiben.pdf`  
> (6,86 MB, gleicher MD5)

und thematisch zur Huser 2025-Quelle (3. Aufl., *Lichtblick für helle Köpfe*) gehört, **nicht** zu Hoyer/Weigand/Müller-Oppliger 2013 (*Begabung: Eine Einführung*).

## Konsequenz

Die Datei wird im lokalen Repo **nicht doppelt abgelegt**. Sie ist im
komprimierten Zustand verfügbar unter

> [`../huser2025lichtblick/kapXX_keller_koller_helle_koepfe_migration_s076-078.pdf`](../huser2025lichtblick/kapXX_keller_koller_helle_koepfe_migration_s076-078.pdf)
> (0,95 MB nach Kompression mit `compress_pdfs.py` -- 1400 px / JPEG-Q70).

Verifikation Stand 2026-04-24 durch MD5-Vergleich.

## Zusätzlich: alternative PDF-Ausgabe im OneDrive

Im OneDrive liegt eine **zweite PDF-Version** des gleichen Buchs:

> `Begabung_ Eine Einführung (Erziehungswissenschaft kompakt) -- Timo Hoyer, Gabriele Weigand, Victor Müller-Oppliger, -- Erziehungswissenschaft kompakt.pdf`
> (3,87 MB, MD5 `1064347e7fab32618d6553058dffb3d3`)

Das ist die **eBook-Ausgabe** (ISBN 978-3-534-73632-4) desselben Werks. Die lokale
`source.pdf` (MD5 `1d3ff03af70e2e6e89ee4f6b036416e6`, 3,88 MB) entspricht der
Print-Ausgabe (ISBN 978-3-534-23506-3). Inhaltlich identisch, unterschiedliches
PDF-Layout. Die eBook-Ausgabe wird nicht doppelt ins Repo übernommen.
