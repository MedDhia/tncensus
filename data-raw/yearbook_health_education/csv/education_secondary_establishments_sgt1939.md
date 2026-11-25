# Établissements d'enseignement secondaire, primaire supérieur ou technique : population scolaire

*Secondary, higher-primary and technical establishments: pupils by nationality and sex (sgt1939).*

Source: *Statistique générale de la Tunisie*, chapter "Instruction publique et beaux-arts" (VII; VI in sgt1936 and sgt1939), editions sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1939 (`bpt6k9105739w`): p. 64, f70, p. 65, f71.

Transcriptions: `../transcribed/education_sum_<edition>.txt`; rebuild with `python3 data-raw/yearbook_health_education/extract_education_summary.py build`. Per-check output: `education_summary_validation.json`.

Rows: 336. Years: 1939–1939.

Printed once per edition, for the edition's own year; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number; pages without a printed number are inferred from the next page. For the two-page spreads (population, primary-education and first-degree totals) the boys' block is given the left-hand page and the girls' block and total columns the right-hand page (the printed fold falls near the boys' TOTAUX, so one or two boys' columns may in fact sit on the right-hand page)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (31 December of that year for pupils; the school year's examinations)
- `branch`: `secondary`, `higher_primary`, `technical`
- `branch_fr`: branch heading as printed
- `establishment`: establishment as printed
- `sex`: `male`, `female`; `total` where the cell is not split by sex (empty in the comparative table for items that are not pupils)
- `sex_fr`: column heading as printed (Aspirants / Aspirantes in the examination table, Garçons / Filles elsewhere)
- `nationality`: `french`, `muslim`, `jewish`, `italian`, `maltese`, `other` (Divers); `total` where not split
- `nationality_fr`: column heading as printed (masculine for boys, feminine for girls)
- `value`: count (integer); printed » = 0; empty where the cell is not printed (`not_applicable`)
- `flag`: empty, or `ocr_corrected`, `derived_from_totals`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (TOTAUX, Totaux généraux, subtotals, A reporter) are not stored unless stated; they were used for validation.

sgt1939 only (views 70–71, pages 64–65): "Établissements d'enseignement secondaire, primaire supérieur ou technique — population scolaire (y compris les classes d'enseignement du premier degré)". One row per establishment, sex and nationality; an establishment can appear in more than one branch (e.g. Collège Stéphen-Pichon, Bizerte, in secondary and higher-primary), the cells are the pupils of that branch. The École de commerce de Tunis is printed twice in the technical branch (boys' and girls' sections); the labels carry "(garçons)" / "(filles)" to tell them apart. The subtotals (établissements de garçons / de jeunes filles), branch totals and the "Total général du 2e degré" (12.690) are checks only. The last two lines, "Élèves fréquentant les classes d'enseignement primaire élémentaire de ces établissements" (4.351) and "Total des élèves des cours d'enseignement de 2e degré" (8.339), are stored in `education_school_population.csv` (sgt1939 rows) and used for checks here.

Failed check: the girls' row of the École primaire supérieure de Sousse (technical section) prints TOTAUX GÉNÉRAUX 127 for 177 (the cells, the girls' TOTAUX and the branch totals need 177).

## Validation

- Checks against printed totals: 285; passed: 284; failed: 1.

Failed checks (every cell involved was re-read on a native-resolution crop; the printed figures are as transcribed; see the commentary above):

  - sgt1939 technical École primaire supérieure, Sousse: boys + girls TOTAUX vs TOTAUX GÉNÉRAUX: cells give 177, printed 127

- Flagged cells: none.

## Cross-checks with other tables of the chapter

- 28 comparisons; equal: 22; different: 6.
  - sgt1939 total des cours de 2e degré boys column 0 vs population table row a): cells give 2742, printed 2736
  - sgt1939 total des cours de 2e degré boys column 6 vs population table row a): cells give 5136, printed 5130
  - sgt1939 total des cours de 2e degré girls column 0 vs population table row a): cells give 2343, printed 2463
  - sgt1939 total des cours de 2e degré girls column 2 vs population table row a): cells give 570, printed 566
  - sgt1939 total des cours de 2e degré girls column 3 vs population table row a): cells give 147, printed 141
  - sgt1939 total des cours de 2e degré girls column 6 vs population table row a): cells give 3203, printed 3313
