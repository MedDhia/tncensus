# Statistique comparée : population scolaire au 31 décembre

*Comparative statistics: school population at 31 December by type of school, nationality and sex.*

Source: *Statistique générale de la Tunisie*, chapter "Instruction publique et beaux-arts" (VII; VI in sgt1936 and sgt1939), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1922 (`bpt6k9105649x`): p. 126, f150, p. 127, f151; sgt1923 (`bpt6k9105649x`): p. 132, f634, p. 133, f635; sgt1924 (`bpt6k9105649x`): p. 134, f1124, p. 135, f1125; sgt1925 (`bpt6k9105650k`): p. 136, f160, p. 137, f161; sgt1926 (`bpt6k9105650k`): p. 146, f710, p. 147, f711; sgt1927 (`bpt6k91056510`): p. 144, f172, p. 145, f173; sgt1928 (`bpt6k91056510`): p. 144, f696, p. 145, f697; sgt1929 (`bpt6k9105652d`): p. 146, f174, p. 147, f175; sgt1930 (`bpt6k9105652d`): p. 150, f708, p. 151, f709; sgt1935 (`bpt6k9105653t`): p. 86, f106, p. 87, f107; sgt1936 (`bpt6k91056547`): p. 64, f75, p. 65, f76; sgt1939 (`bpt6k9105739w`): p. 68, f74, p. 69, f75.

Transcriptions: `../transcribed/education_sum_<edition>.txt`; rebuild with `python3 data-raw/yearbook_health_education/extract_education_summary.py build`. Per-check output: `education_summary_validation.json`.

Rows: 481. Years: 1921–1939 (15 years: 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1934, 1935, 1936, 1938, 1939).

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

Comparative statistics a) "Population scolaire au 31 décembre": pupils by type of school, sex and nationality, with the previous year's total per type (`pupils_total_previous_year`, `year` = previous year). The "garçons et filles" columns, the TOTAUX, the rows "Total de l'enseignement public" and "Total général" are checks only; the "Total général" by sex and nationality, and the comparison lines with the three previous years, form `education_school_population_series.csv`.

School types (`school_type`): sgt1922–sgt1936 `public_primary` (Écoles primaires publiques), `civil_personality` (Établissements à personnalité civile, including their primary classes), `private` (Écoles privées). sgt1939 (new layout): `secondary_courses` (a) cours secondaires, primaires supérieurs ou techniques of the second-degree establishments), `estab_primary_classes` (b) their elementary classes), `first_degree_establishments`, `private`.

sgt1935 and sgt1939 print the boys' TOTAUX column in the binding; it was entered as TOTAUX GÉNÉRAUX minus the girls' TOTAUX (agreeing with every visible digit); those checks are therefore not independent. Failed checks are misprints of printed totals, kept: e.g. sgt1923 Total général, garçons, Israélites printed 5.580 (3.397 + 2.103 = 5.500), sgt1929 several "garçons et filles" cells (civil personality, Israélites 1.494 for 764) and sgt1939 Total général, garçons, Français 14.349 for 14.394.

## Validation

- Checks against printed totals: 1462; passed: 1439; failed: 23.

Failed checks (every cell involved was re-read on a native-resolution crop; the printed figures are as transcribed; see the commentary above):

  - sgt1923 TOTAL_GENERAL boys: nationalities vs TOTAUX: cells give 34737, printed 34657
  - sgt1923 TOTAL_GENERAL jewish: boys + girls vs garçons et filles: cells give 10926, printed 10846
  - sgt1923 TOTAL_GENERAL block 0 column 2: rows vs total line: cells give 5500, printed 5580
  - sgt1929 civil_personality jewish: boys + girls vs garçons et filles: cells give 764, printed 1494
  - sgt1929 civil_personality: garçons et filles columns vs TOTAUX GÉNÉRAUX: cells give 6100, printed 5370
  - sgt1929 TOTAL_PUBLIC girls: nationalities vs TOTAUX: cells give 19266, printed 19260
  - sgt1929 TOTAL_PUBLIC muslim: boys + girls vs garçons et filles: cells give 31036, printed 31030
  - sgt1929 TOTAL_PUBLIC jewish: boys + girls vs garçons et filles: cells give 8770, printed 9500
  - sgt1929 TOTAL_PUBLIC: garçons et filles columns vs TOTAUX GÉNÉRAUX: cells give 64755, printed 64025
  - sgt1929 TOTAL_GENERAL girls: nationalities vs TOTAUX: cells give 23008, printed 23009
  - sgt1929 TOTAL_GENERAL french: boys + girls vs garçons et filles: cells give 16742, printed 17742
  - sgt1929 TOTAL_GENERAL jewish: boys + girls vs garçons et filles: cells give 11704, printed 12434
  - sgt1929 TOTAL_GENERAL other: boys + girls vs garçons et filles: cells give 425, printed 426
  - sgt1929 TOTAL_GENERAL: garçons et filles columns vs TOTAUX GÉNÉRAUX: cells give 72999, printed 71269
  - sgt1929 TOTAL_PUBLIC block 1 column 1: rows vs total line: cells give 3173, printed 3179
  - sgt1929 TOTAL_GENERAL block 1 column 1: rows vs total line: cells give 3783, printed 3777
  - sgt1929 TOTAL_GENERAL block 1 column 5: rows vs total line: cells give 201, printed 200
  - sgt1929 TOTAL_GENERAL block 2 column 0: rows vs total line: cells give 16742, printed 17742
  - sgt1935 comparison 1933 girls: nationalities vs TOTAUX: cells give 27944, printed 27914
  - sgt1935 comparison 1933 italian: boys + girls vs garçons et filles: cells give 10514, printed 10484
  - sgt1939 TOTAL_GENERAL boys: nationalities vs TOTAUX: cells give 65574, printed 65619
  - sgt1939 TOTAL_GENERAL french: boys + girls vs garçons et filles: cells give 28310, printed 28355
  - sgt1939 TOTAL_GENERAL block 0 column 0: rows vs total line: cells give 14394, printed 14349

- Flagged cells: none.

## Cross-checks with other tables of the chapter

- 45 comparisons; equal: 45; different: 0.
