# Grèves. a) Etat détaillé des grèves

*Strikes: detail of each strike (occupation, locality, duration, establishments, strikers, aim, result).*

Source: *Statistique générale de la Tunisie*, chapter *Travail et prévoyance sociale*, editions sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1926 (`bpt6k9105650k`): p. 476, f1040, p. 477, f1041; sgt1927 (`bpt6k91056510`): p. 478, f506, p. 479, f507; sgt1928 (`bpt6k91056510`): p. 484, f1036, p. 485, f1037; sgt1929 (`bpt6k9105652d`): p. 486, f514, p. 487, f515; sgt1930 (`bpt6k9105652d`): p. 492, f1050, p. 493, f1051; sgt1935 (`bpt6k9105653t`): p. 304, f324, p. 305, f325.

Transcriptions: `../transcribed/labour_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_labour.py build`.

Rows: 153. Years: 1926, 1927, 1928, 1929, 1930, 1935.

Units: days and count (`unit`); value_type: count.

Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept, with `year` (the edition year when no year is printed); a year printed by two editions is stored once, from the later one, and compared.

## Columns

- `census`: edition the value is taken from (rule 4 series: the latest edition printing it; rule 5: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (two-page spreads: the page the cell is printed on)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (HBM: last year of the printed period)
- `strike_no`: order of the strike in the printed list
- `occupation_fr`: occupation as printed
- `locality`: locality as printed
- `goal_fr`: aim of the strike as printed
- `result`: result (English code: success, compromise, failure; sgt1935 'reprise du travail aux anciennes conditions' = failure, 'avec augmentation de salaires' = compromise, as counted in that edition's yearly line: 0 réussite, 2 transactions, 5 échecs)
- `result_fr`: result as printed
- `measure`: measure code (English)
- `measure_fr`: printed heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, ocr_corrected, illegible, total_mismatch, derived_from_totals, not_applicable, reprint_corrected or row_realigned

Printed sgt1926-sgt1930 and sgt1935 (no year in the title to sgt1928: `year` = edition year; sgt1929, sgt1930, sgt1935 'survenues en <year>'); not in sgt1925, sgt1936, sgt1939. One row per strike and measure; occupation, locality, aim and result as printed. Checks: the number of strikes, the sums of days, establishments and strikers and the counts of results equal the yearly line of `labour_strikes` (same edition).

Every failed check below was re-read on a zoomed native-resolution crop (or recurs unchanged in independent readings of several editions): printed values are kept. sgt1929: the nine strikes of the detailed list last 62 days in all, the yearly line prints 65 (both re-read on crops).

Survey of the whole chapter in every edition: `labour_survey.md`.

## Validation

- Checks against printed totals and identities: 42; passed: 41; failed: 1.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1929 p.486 (f514) strike_detail sum of days vs the yearly line: cells give 62, printed 65 (difference 3)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (6 printings): sgt1926 f1040, sgt1927 f506, sgt1928 f1036, sgt1929 f514, sgt1930 f1050, sgt1935 f324.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
