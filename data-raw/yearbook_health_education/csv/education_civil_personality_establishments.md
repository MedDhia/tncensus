# Enseignements supérieur, secondaire et spécial : établissements à personnalité civile

*Higher, secondary and special education: establishments with civil personality (classes, pupils by nationality and sex), sgt1922–sgt1936.*

Source: *Statistique générale de la Tunisie*, chapter "Instruction publique et beaux-arts" (VII; VI in sgt1936 and sgt1939), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1922 (`bpt6k9105649x`): p. 93, f117; sgt1923 (`bpt6k9105649x`): p. 99, f601; sgt1924 (`bpt6k9105649x`): p. 101, f1091; sgt1925 (`bpt6k9105650k`): p. 103, f127; sgt1926 (`bpt6k9105650k`): p. 113, f677; sgt1927 (`bpt6k91056510`): p. 111, f139; sgt1928 (`bpt6k91056510`): p. 111, f663; sgt1929 (`bpt6k9105652d`): p. 113, f141; sgt1930 (`bpt6k9105652d`): p. 117, f675; sgt1935 (`bpt6k9105653t`): p. 83, f103; sgt1936 (`bpt6k91056547`): p. 61, f72.

Transcriptions: `../transcribed/education_sum_<edition>.txt`; rebuild with `python3 data-raw/yearbook_health_education/extract_education_summary.py build`. Per-check output: `education_summary_validation.json`.

Rows: 1232. Years: 1921–1936 (13 years: 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1934, 1935, 1936).

Printed once per edition, for the edition's own year; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number; pages without a printed number are inferred from the next page. For the two-page spreads (population, primary-education and first-degree totals) the boys' block is given the left-hand page and the girls' block and total columns the right-hand page (the printed fold falls near the boys' TOTAUX, so one or two boys' columns may in fact sit on the right-hand page)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (31 December of that year for pupils; the school year's examinations)
- `locality`: locality as printed
- `establishment`: establishment as printed
- `measure`: what is counted (see below)
- `measure_fr`: as printed
- `sex`: `male`, `female`; `total` where the cell is not split by sex (empty in the comparative table for items that are not pupils)
- `sex_fr`: column heading as printed (Aspirants / Aspirantes in the examination table, Garçons / Filles elsewhere)
- `nationality`: `french`, `muslim`, `jewish`, `italian`, `maltese`, `other` (Divers); `total` where not split
- `nationality_fr`: column heading as printed (masculine for boys, feminine for girls)
- `value`: count (integer); printed » = 0; empty where the cell is not printed (`not_applicable`)
- `flag`: empty, or `ocr_corrected`, `derived_from_totals`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (TOTAUX, Totaux généraux, subtotals, A reporter) are not stored unless stated; they were used for validation.

Table a) "Établissements à personnalité civile" (Lycée Carnot, Collège Sadiki, Collège Alaoui, Écoles normales d'instituteurs and d'institutrices, École professionnelle Émile-Loubet, Lycée Armand-Fallières, Petit Lycée Jules-Ferry; all in Tunis), sgt1922–sgt1936. Measures: `classes` (Nombre de classes), `pupils` by sex and nationality, and `pupils_total_previous_year` (the printed "Totaux généraux de l'année précédente", stored with `year` = the previous year: it is the only source for 1921 and 1934, and for the other years it is compared with the previous edition's own total, see the cross-checks). The edition's own row totals and the Totaux line are not stored. From sgt1939 the table is replaced by the secondary, higher-primary and technical establishments (`education_secondary_establishments_sgt1939.csv`).

The pupils include the primary (elementary) classes of these establishments (Petit Collège Sadiki, écoles d'application, Petit Lycée), which the total of primary education reprints (see `education_primary_totals.csv`). sgt1935: the classes cell of the École normale d'institutrices reads "14 classes et 3 ateliers" (14 stored).

Failed checks: sgt1922 Petit Lycée Jules-Ferry girls' TOTAUX printed 592 for 502 (the cells, the TOTAUX GÉNÉRAUX 502 and the column total 1.411 all give 502); sgt1935 previous-year column: the eight cells sum to 6.985 against the printed 6.935.

## Footnotes printed under the table

- (1) Ces établissements, créés au 1er janvier 1915, comprennent : le premier, les classes secondaires ; le deuxième, les classes élémentaires de l'ancienne École Jules Ferry. (sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930)

## Validation

- Checks against printed totals: 539; passed: 535; failed: 4.

Failed checks (every cell involved was re-read on a native-resolution crop; the printed figures are as transcribed; see the commentary above):

  - sgt1922 Petit Lycée Jules-Ferry (1) girls: nationalities vs TOTAUX: cells give 502, printed 592
  - sgt1922 Petit Lycée Jules-Ferry (1): boys + girls TOTAUX vs TOTAUX GÉNÉRAUX: cells give 592, printed 502
  - sgt1922 female column 6 vs Totaux: cells give 1501, printed 1411
  - sgt1935 previous-year column vs Totaux: cells give 6985, printed 6935

- Flagged cells: none.

## Cross-checks with other tables of the chapter

- 234 comparisons; equal: 234; different: 0.
