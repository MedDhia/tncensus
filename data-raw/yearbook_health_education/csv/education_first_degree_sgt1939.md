# Total général de la population scolaire du premier degré

*Total first-degree school population (sgt1939).*

Source: *Statistique générale de la Tunisie*, chapter "Instruction publique et beaux-arts" (VII; VI in sgt1936 and sgt1939), editions sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1939 (`bpt6k9105739w`): p. 66, f72, p. 67, f73.

Transcriptions: `../transcribed/education_sum_<edition>.txt`; rebuild with `python3 data-raw/yearbook_health_education/extract_education_summary.py build`. Per-check output: `education_summary_validation.json`.

Rows: 26. Years: 1938–1939.

Printed once per edition, for the edition's own year; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number; pages without a printed number are inferred from the next page. For the two-page spreads (population, primary-education and first-degree totals) the boys' block is given the left-hand page and the girls' block and total columns the right-hand page (the printed fold falls near the boys' TOTAUX, so one or two boys' columns may in fact sit on the right-hand page)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (31 December of that year for pupils; the school year's examinations)
- `school_type`: English code (see below)
- `school_type_fr`: row label as printed
- `measure`: what is counted (see below)
- `sex`: `male`, `female`; `total` where the cell is not split by sex (empty in the comparative table for items that are not pupils)
- `sex_fr`: column heading as printed (Aspirants / Aspirantes in the examination table, Garçons / Filles elsewhere)
- `nationality`: `french`, `muslim`, `jewish`, `italian`, `maltese`, `other` (Divers); `total` where not split
- `nationality_fr`: column heading as printed (masculine for boys, feminine for girls)
- `value`: count (integer); printed » = 0; empty where the cell is not printed (`not_applicable`)
- `flag`: empty, or `ocr_corrected`, `derived_from_totals`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (TOTAUX, Totaux généraux, subtotals, A reporter) are not stored unless stated; they were used for validation.

sgt1939 (views 72–73): "Total général de la population scolaire du premier degré": primary classes of the second-degree establishments (`estab_primary_classes`) and first-degree establishments (`first_degree_establishments`), by sex and nationality, with the previous year's totals (`pupils_total_previous_year`). The boys' Musulmans and Israélites columns are printed in the binding: Israélites 387 of row 1 is legible; 37.058 and 3.342 of row 2 are taken from the same row of the population table (views 74–75), which closes the row total 53.093 (`derived_from_totals`). Row 1, boys, Français is printed 1.471, against 1.171 in the population table and the secondary-establishments table; the row total (2.634) and the column total (10.372) need 1.171 (`total_mismatch`, printed value kept). Both rows are the same cells as the sgt1939 rows of `education_school_population.csv`.

## Validation

- Checks against printed totals: 25; passed: 23; failed: 2.

Failed checks (every cell involved was re-read on a native-resolution crop; the printed figures are as transcribed; see the commentary above):

  - sgt1939 estab_primary_classes boys: nationalities vs TOTAUX: cells give 2934, printed 2634
  - sgt1939 TOTAL block 0 column 0: rows vs total line: cells give 10672, printed 10372

- Flagged cells: derived_from_totals: 2, total_mismatch: 1.

  - sgt1939 1939 estab_primary_classes / pupils / male / french = 1471 (total_mismatch)
  - sgt1939 1939 first_degree_establishments / pupils / male / muslim = 37058 (derived_from_totals)
  - sgt1939 1939 first_degree_establishments / pupils / male / jewish = 3342 (derived_from_totals)

## Cross-checks with other tables of the chapter

- 28 comparisons; equal: 27; different: 1.
  - sgt1939 'estab_primary_classes' boys column 0: primary/first-degree total vs population table: cells give 1471, printed 1171
