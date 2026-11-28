# Yearbook extraction: rules in addition to `data-raw/colonial_census/SPEC.md`

Everything in SPEC.md applies (tidy CSV, one row per printed cell, columns,
flags, validation against every printed total, a notes `.md` per CSV, a
rebuild script). These rules replace or extend it for the yearbooks:

1. **Output** goes to `data-raw/yearbook_demography/csv/`, scripts to
   `data-raw/yearbook_demography/extract_<name>.py`, hand transcriptions to
   `data-raw/yearbook_demography/transcribed/`.
2. **`census` column** holds the source edition code, e.g. `sgt1927` (see
   EDITIONS.md). Add `gallica_ark` (the volume ark), because views are only
   unique within a volume.
3. **Census tables reprinted in several editions:** extract **one** copy, from
   the earliest edition that prints it legibly, and compare **every cell** with
   every other edition that reprints it. In the notes, report per reprint: cells
   compared, cells equal, and each difference (cell, values, which the image
   supports, which you kept). If a reprint corrects an obvious misprint in
   the copy you extract, keep the corrected value, flag it
   `reprint_corrected`, and say which edition in the notes. Name the file
   `cens<year>_<topic>.csv` (e.g. `cens1926_controle_nationality.csv`), with a
   `census_year` column.
4. **Vital statistics and expulsions** are printed for overlapping year
   windows. Build one series per table (e.g. `vital_european_births.csv`)
   with a `year` column and one row per cell per year, taken from the **latest
   edition** that prints that year (most revised), with `census` = that
   edition. Compare every other printing of the same year and cell; report
   the differences in the notes. Don't store the duplicate printings.
5. **Naturalisations** are printed once per edition year; keep all editions
   in one file per table, with `year`.
6. **Flags** allowed: empty, `ocr_corrected`, `illegible`, `total_mismatch`,
   `derived_from_totals`, `not_applicable`, and `reprint_corrected` (value taken
   from another edition's printing because this one is misprinted or unreadable).
7. Translate labels to English codes with a `*_fr` column, as before. Place
   names exactly as printed.
