# École de commerce : répartition des élèves dans les différents cours

*School of commerce: pupils by course, nationality and sex (sgt1936, sgt1939).*

Source: *Statistique générale de la Tunisie*, chapter "Instruction publique et beaux-arts" (VII; VI in sgt1936 and sgt1939), editions sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1936 (`bpt6k91056547`): p. 61, f72; sgt1939 (`bpt6k9105739w`): p. 63, f69.

Transcriptions: `../transcribed/education_sum_<edition>.txt`; rebuild with `python3 data-raw/yearbook_health_education/extract_education_summary.py build`. Per-check output: `education_summary_validation.json`.

Rows: 84. Years: 1936–1939 (2 years: 1936, 1939).

Printed once per edition, for the edition's own year; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number; pages without a printed number are inferred from the next page. For the two-page spreads (population, primary-education and first-degree totals) the boys' block is given the left-hand page and the girls' block and total columns the right-hand page (the printed fold falls near the boys' TOTAUX, so one or two boys' columns may in fact sit on the right-hand page)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (31 December of that year for pupils; the school year's examinations)
- `course`: English code
- `course_fr`: course as printed
- `sex`: `male`, `female`; `total` where the cell is not split by sex (empty in the comparative table for items that are not pupils)
- `sex_fr`: column heading as printed (Aspirants / Aspirantes in the examination table, Garçons / Filles elsewhere)
- `nationality`: `french`, `muslim`, `jewish`, `italian`, `maltese`, `other` (Divers); `total` where not split
- `nationality_fr`: column heading as printed (masculine for boys, feminine for girls)
- `value`: count (integer); printed » = 0; empty where the cell is not printed (`not_applicable`)
- `flag`: empty, or `ocr_corrected`, `derived_from_totals`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (TOTAUX, Totaux généraux, subtotals, A reporter) are not stored unless stated; they were used for validation.

École de commerce (Tunis), sgt1936 and sgt1939: pupils by course, sex and nationality. sgt1939: the secretarial course prints TOTAUX GÉNÉRAUX 13 against 18 girls, and the "Section des bacheliers" prints 2 Israélites in the boys' block with a boys' TOTAUX of » (TOTAUX GÉNÉRAUX 4 = the 4 girls); the cells concerned are flagged `total_mismatch`.

## Validation

- Checks against printed totals: 28; passed: 24; failed: 4.

Failed checks (every cell involved was re-read on a native-resolution crop; the printed figures are as transcribed; see the commentary above):

  - sgt1939 secretarial_y2: boys + girls TOTAUX vs TOTAUX GÉNÉRAUX: cells give 18, printed 13
  - sgt1939 secretarial_y2: all cells vs TOTAUX GÉNÉRAUX: cells give 18, printed 13
  - sgt1939 bachelors_section boys: nationalities vs TOTAUX: cells give 2, printed 0
  - sgt1939 bachelors_section: all cells vs TOTAUX GÉNÉRAUX: cells give 6, printed 4

- Flagged cells: total_mismatch: 2.

  - sgt1939 1939 secretarial_y2 / female / french = 12 (total_mismatch)
  - sgt1939 1939 bachelors_section / male / jewish = 2 (total_mismatch)
