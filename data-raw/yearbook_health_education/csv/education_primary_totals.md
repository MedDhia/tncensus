# Total général de l'enseignement primaire

*Total of primary education, by type, nationality and sex (sgt1922–sgt1936).*

Source: *Statistique générale de la Tunisie*, chapter "Instruction publique et beaux-arts" (VII; VI in sgt1936 and sgt1939), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1922 (`bpt6k9105649x`): p. 124, f148, p. 125, f149; sgt1923 (`bpt6k9105649x`): p. 130, f632, p. 131, f633; sgt1924 (`bpt6k9105649x`): p. 132, f1122, p. 133, f1123; sgt1925 (`bpt6k9105650k`): p. 134, f158, p. 135, f159; sgt1926 (`bpt6k9105650k`): p. 144, f708, p. 145, f709; sgt1927 (`bpt6k91056510`): p. 142, f170, p. 143, f171; sgt1928 (`bpt6k91056510`): p. 142, f694, p. 143, f695; sgt1929 (`bpt6k9105652d`): p. 144, f172, p. 145, f173; sgt1930 (`bpt6k9105652d`): p. 148, f706, p. 149, f707; sgt1935 (`bpt6k9105653t`): p. 84, f104, p. 85, f105; sgt1936 (`bpt6k91056547`): p. 62, f73, p. 63, f74.

Transcriptions: `../transcribed/education_sum_<edition>.txt`; rebuild with `python3 data-raw/yearbook_health_education/extract_education_summary.py build`. Per-check output: `education_summary_validation.json`.

Rows: 429. Years: 1921–1936 (13 years: 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1934, 1935, 1936).

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

"Total général de l'enseignement primaire" (sgt1922–sgt1936), printed at the end of the school lists: 1° public primary schools (`public_primary`), 2° private schools (`private`), 3° primary classes of the establishments with civil personality (`estab_primary_classes`), by sex and nationality, and the totals of the previous year (`pupils_total_previous_year`, `year` = previous year). Footnote (1): these numbers are already counted in the statistics of the Collège Sadiki (petit collège), the écoles normales (écoles d'application) and the Petit Lycée Jules-Ferry; they are given only to obtain the total of pupils receiving primary education; in the school-population table they are counted only with the establishments with civil personality. The `public_primary` and `private` rows are the same cells as the corresponding rows of `education_school_population.csv` in sgt1922–sgt1930 (do not add the two files).

**Cross-check with the population table**: the `public_primary` and `private` lines were compared cell by cell with the "Écoles primaires publiques" and "Écoles privées" rows of the same edition's comparative school-population table. They agree in sgt1922–sgt1929. In sgt1930 the public boys' Français cell is printed 6.667 here and 6.676 in the population table (6.676 closes this table's row and column totals: a transposition misprint, flagged `total_mismatch`). In sgt1935 and sgt1936 the private-school lines differ throughout (sgt1935: 3.595 boys / 3.588 girls here against 4.128 / 3.953; sgt1936: 3.665 / 3.955 against 4.253 / 4.343): the population table's private schools are wider than the primary private schools of this line (the comparative table's private pupils, 8.081 and 8.596, agree with the population table). Both printings are kept, each in its own file. For sgt1939 see `education_first_degree_sgt1939.csv`.

Cells hidden in the binding and solved from the printed totals (`derived_from_totals`): sgt1935 boys' Musulmans column (35.079, 91, 802; total 35.972 closes), sgt1936 public boys' Français (9.819, confirmed by the population table).

## Footnotes printed under the table

- (1) Ces nombres figurent déjà dans la statistique du Collège Sadiki (petit Collège), des Écoles normales d'instituteurs et d'institutrices (Écoles d'application) et du Petit Lycée Jules-Ferry. Ils ne sont reportés ici que pour déterminer le total général des élèves qui reçoivent l'enseignement primaire. Dans le tableau de la population scolaire, ils sont comptés seulement dans le total des établissements à personnalité civile. (sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1935, sgt1936)

## Validation

- Checks against printed totals: 308; passed: 306; failed: 2.

Failed checks (every cell involved was re-read on a native-resolution crop; the printed figures are as transcribed; see the commentary above):

  - sgt1930 public_primary boys: nationalities vs TOTAUX: cells give 45129, printed 45138
  - sgt1930 TOTAUX block 0 column 0: rows vs total line: cells give 8280, printed 8289

- Flagged cells: derived_from_totals: 4, total_mismatch: 1.

  - sgt1930 1930 public_primary / pupils / male / french = 6667 (total_mismatch)
  - sgt1935 1935 public_primary / pupils / male / muslim = 35079 (derived_from_totals)
  - sgt1935 1935 private / pupils / male / muslim = 91 (derived_from_totals)
  - sgt1935 1935 estab_primary_classes / pupils / male / muslim = 802 (derived_from_totals)
  - sgt1936 1936 public_primary / pupils / male / french = 9819 (derived_from_totals)

## Cross-checks with other tables of the chapter

- 344 comparisons; equal: 315; different: 29.
  - sgt1930 'public_primary' boys column 0: primary/first-degree total vs population table: cells give 6667, printed 6676
  - sgt1935 'private' boys column 0: primary/first-degree total vs population table: cells give 770, printed 1050
  - sgt1935 'private' boys column 1: primary/first-degree total vs population table: cells give 91, printed 128
  - sgt1935 'private' boys column 2: primary/first-degree total vs population table: cells give 1977, printed 2142
  - sgt1935 'private' boys column 3: primary/first-degree total vs population table: cells give 713, printed 743
  - sgt1935 'private' boys column 4: primary/first-degree total vs population table: cells give 30, printed 38
  - sgt1935 'private' boys column 5: primary/first-degree total vs population table: cells give 14, printed 27
  - sgt1935 'private' boys column 6: primary/first-degree total vs population table: cells give 3595, printed 4128
  - sgt1935 'private' girls column 0: primary/first-degree total vs population table: cells give 1202, printed 1497
  - sgt1935 'private' girls column 1: primary/first-degree total vs population table: cells give 545, printed 546
  - sgt1935 'private' girls column 2: primary/first-degree total vs population table: cells give 1124, printed 1166
  - sgt1935 'private' girls column 3: primary/first-degree total vs population table: cells give 660, printed 682
  - sgt1935 'private' girls column 4: primary/first-degree total vs population table: cells give 41, printed 44
  - sgt1935 'private' girls column 5: primary/first-degree total vs population table: cells give 16, printed 18
  - sgt1935 'private' girls column 6: primary/first-degree total vs population table: cells give 3588, printed 3953
  - sgt1936 'private' boys column 0: primary/first-degree total vs population table: cells give 793, printed 1078
  - sgt1936 'private' boys column 1: primary/first-degree total vs population table: cells give 81, printed 148
  - sgt1936 'private' boys column 2: primary/first-degree total vs population table: cells give 1980, printed 2172
  - sgt1936 'private' boys column 3: primary/first-degree total vs population table: cells give 774, printed 803
  - sgt1936 'private' boys column 4: primary/first-degree total vs population table: cells give 19, printed 25
  - sgt1936 'private' boys column 5: primary/first-degree total vs population table: cells give 18, printed 27
  - sgt1936 'private' boys column 6: primary/first-degree total vs population table: cells give 3665, printed 4253
  - sgt1936 'private' girls column 0: primary/first-degree total vs population table: cells give 1415, printed 1757
  - sgt1936 'private' girls column 1: primary/first-degree total vs population table: cells give 538, printed 543
  - sgt1936 'private' girls column 2: primary/first-degree total vs population table: cells give 1256, printed 1265
  - sgt1936 'private' girls column 3: primary/first-degree total vs population table: cells give 677, printed 703
  - sgt1936 'private' girls column 4: primary/first-degree total vs population table: cells give 51, printed 55
  - sgt1936 'private' girls column 5: primary/first-degree total vs population table: cells give 18, printed 20
  - sgt1936 'private' girls column 6: primary/first-degree total vs population table: cells give 3955, printed 4343
