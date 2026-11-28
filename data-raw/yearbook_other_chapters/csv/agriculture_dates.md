# Canoun des dattiers. Relevé par caïdat du nombre d'arbres d'après leur âge au 1er novembre

*Date palms (canoun) by caïdat and age, degla and common, at 1 November.*

Source: *Statistique générale de la Tunisie*, chapter *Agriculture*, editions sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1936 (`bpt6k91056547`): p. 100, f111; sgt1939 (`bpt6k9105739w`): p. 104, f110.

Transcriptions: `../transcribed/agriculture_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_agriculture.py build`.

Rows: 528. Years: 1936, 1939.

Units: trees (`unit`); value_type: count.

Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept; `year` = edition year.

## Columns

- `census`: edition the value is taken from (rule 4 series: the latest edition printing that year; rule 5 tables: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: edition year (count at 1 November of that year, as printed)
- `region`: empty (not printed)
- `chef_lieu`: empty (not printed)
- `controle_civil`: empty (not printed)
- `caidat`: caïdat as printed (two bracketed groups of three, without a group name)
- `date_type`: `deglet_nour` (dattiers degla) or `common` (dattiers communs)
- `date_type_fr`: printed sub-heading
- `age_class`: `male` (mâles), `under_1` (moins d'un an), `age_1`..`age_19` (young trees by age), `taxable_20` (imposables, 20 ans)
- `age_class_fr`: printed column heading
- `measure`: `trees`
- `measure_fr`: printed heading
- `unit`: `trees`
- `value`: printed value (» = 0)
- `flag`: empty, or `derived_from_totals`, `total_mismatch`

Printed in sgt1936 (at 1 November 1936, f111|f112) and sgt1939 (at 1 November 1939, f110|f111), for the six caïdats of the south (Gabès, Gafsa, Tozeur; Nefzaoua, Ouerghemma, Matmata). The columns TOTAL des jeunes (col. 23) and TOTAL des colonnes 2, 23 et 24 (col. 25) and the TOTAUX lines are checks only.

sgt1939: the 9 ans and 10 ans columns run into the binding gutter; they were read on zoomed crops of both views. Communs Tozeur 9 ans "23.24?" (last digit hidden) = 23.241 from its TOTAL des jeunes (`derived_from_totals`; the column TOTAUX 32.678 agrees). The age columns move by three years between the two editions (e.g. 1936 11 ans = 1939 14 ans), as expected.

Every failed check below was re-read on a zoomed native-resolution crop: they are printed inconsistencies (printed values kept). Flagged `total_mismatch` where one cell explains both its line (TOTAL des jeunes) and its column (TOTAUX) check: sgt1936 communs Gafsa 16 ans 5.582 (both checks 3.000 over: 2.582); sgt1939 degla Gafsa 4 ans 8 (both 20 short: 28); sgt1939 degla Nefzaoua 9 ans 465 (both 10 short: 475; printed at the gutter); sgt1939 communs Gabès 19 ans 100.356 (both 180 short: 100.536). sgt1939 degla Tozeur TOTAL 196.261 is a misprinted line total (0 + 113.496 + 83.465 = 196.961; the TOTAUX 216.693 agrees with 196.961).

Survey of the whole chapter in every edition: `agriculture_survey.md`.

## Validation

- Checks against printed totals and identities: 152; passed: 142; failed: 10.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1936 p.100 (f111) dates common a16: lines vs TOTAUX: cells give 252060, printed 249060 (difference -3000)
  - sgt1936 p.100 (f111) dates common Gafsa: ages vs TOTAL des jeunes: cells give 10352, printed 7352 (difference -3000)
  - sgt1939 p.104 (f110) dates degla a4: lines vs TOTAUX: cells give 16548, printed 16568 (difference 20)
  - sgt1939 p.104 (f110) dates degla a9: lines vs TOTAUX: cells give 15923, printed 15933 (difference 10)
  - sgt1939 p.104 (f110) dates degla total: lines vs TOTAUX: cells give 215993, printed 216693 (difference 700)
  - sgt1939 p.104 (f110) dates degla Gafsa: ages vs TOTAL des jeunes: cells give 567, printed 587 (difference 20)
  - sgt1939 p.104 (f110) dates degla Tozeur: mâles + jeunes + imposables vs TOTAL: cells give 196961, printed 196261 (difference -700)
  - sgt1939 p.104 (f110) dates degla Nefzaoua: ages vs TOTAL des jeunes: cells give 11297, printed 11307 (difference 10)
  - sgt1939 p.104 (f110) dates common a19: lines vs TOTAUX: cells give 247873, printed 248053 (difference 180)
  - sgt1939 p.104 (f110) dates common Gabès: ages vs TOTAL des jeunes: cells give 394114, printed 394294 (difference 180)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: derived_from_totals: 1, total_mismatch: 4.

  - sgt1936 p.100 1936  /  /  / Gafsa / common / age_16 / trees / trees = 5582 (total_mismatch)
  - sgt1939 p.104 1939  /  /  / Gafsa / deglet_nour / age_4 / trees / trees = 8 (total_mismatch)
  - sgt1939 p.104 1939  /  /  / Nefzaoua / deglet_nour / age_9 / trees / trees = 465 (total_mismatch)
  - sgt1939 p.104 1939  /  /  / Gabès / common / age_19 / trees / trees = 100356 (total_mismatch)
  - sgt1939 p.104 1939  /  /  / Tozeur / common / age_9 / trees / trees = 23241 (derived_from_totals)

## Image versus OCR

- Read cell by cell on the page images (4 printings): sgt1936 f111, sgt1936 f111, sgt1939 f110, sgt1939 f110.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
