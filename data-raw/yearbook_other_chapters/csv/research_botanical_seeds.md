# Service botanique et agronomique. a) Semences pédigrées produites par le Service

*Botanical and agronomic service: pedigree seed produced, controlled pedigree seed crops, wheat and flour analyses.*

Source: *Statistique générale de la Tunisie*, chapter *Institutions d'enseignement et de recherches*, editions sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1935 (`bpt6k9105653t`): p. 142, f162; sgt1936 (`bpt6k91056547`): p. 110, f121; sgt1939 (`bpt6k9105739w`): p. 114, f120.

Transcriptions: `../transcribed/research_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_research.py build`.

Rows: 90. Years: 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Units: quintals, hectares, producers, analyses (`unit`); value_type: mixed.

Selection (SPEC_ADDENDUM rule 4): each cell is stored once, from the latest edition printing it; every other printing of the same cell is compared below.

## Columns

- `census`: source edition (`sgt1922` ... `sgt1939`)
- `table_id`: section code of the transcription
- `gallica_ark`: Gallica volume ark
- `source_page`: printed page number
- `gallica_view`: Gallica view
- `year`: year of the figure (for a school year or season: the year it ends; for promotions and once-per-edition tables: the edition year)
- `part`: part of the table
- `part_fr`: part heading as printed
- `item`: ASCII slug of `item_fr`
- `item_fr`: line as printed (sub-heading prefixed, ditto marks expanded)
- `unit`: unit of the line (francs, persons, analyses, doses, flacons, cc, tubes, ampoules, litres, samples, quintals, hectares, producers, count)
- `value`: printed figure (» = 0)
- `flag`: empty, or ocr_corrected / illegible / total_mismatch / derived_from_totals / not_applicable / reprint_corrected / row_realigned

Printed averages (Moyenne) are checks only, against the mean of the printed years (to 0.1); an average whose years are not all printed in the same table is not stored.

Every failed check below was re-read on a zoomed native-resolution crop: they are printed inconsistencies (printed values kept). sgt1935: Moyenne 1931-1935 of Blés durs (100.1 for 100.6) and of the hectare Total (868.4 for 869.6) and the hectare Total of 1935 (471 for 465) are printed errors in the averages/total lines (not stored). Blés tendres de force (Ha.) 1934 reads 90 on the zoomed crop (earlier transcribed 99): it fits the 1934 total 702 and the average 105.2.

Survey of the whole chapter in every edition: `research_survey.md`.

## Validation

- Checks against printed totals and identities: 34; passed: 31; failed: 3.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1935 p.142 (f162) bot_seeds [seeds] Blés durs: average 1931-1935: cells give 100.6, printed 100.1 (difference -0.5)
  - sgt1935 p.142 (f162) bot_seeds [controlled] 1935: lines vs Total (Ha.): cells give 465, printed 471 (difference 6)
  - sgt1935 p.142 (f162) bot_seeds [controlled] Total (Ha.): average 1931-1935: cells give 869.6, printed 868.4 (difference -1.2)

- Overlapping printings: 40 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (9 printings): sgt1935 f162, sgt1935 f162, sgt1935 f162, sgt1936 f121, sgt1936 f121, sgt1936 f121, sgt1939 f120, sgt1939 f120, sgt1939 f120.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
