# Population scolaire : total général des établissements scolaires français publics et privés

*School population, all French public and private schools, by nationality and sex (yearly series).*

Source: *Statistique générale de la Tunisie*, chapter "Instruction publique et beaux-arts" (VII; VI in sgt1936 and sgt1939), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1922 (`bpt6k9105649x`): p. 126, f150, p. 127, f151; sgt1923 (`bpt6k9105649x`): p. 132, f634, p. 133, f635; sgt1924 (`bpt6k9105649x`): p. 134, f1124, p. 135, f1125; sgt1925 (`bpt6k9105650k`): p. 136, f160, p. 137, f161; sgt1926 (`bpt6k9105650k`): p. 146, f710, p. 147, f711; sgt1927 (`bpt6k91056510`): p. 144, f172, p. 145, f173; sgt1928 (`bpt6k91056510`): p. 144, f696, p. 145, f697; sgt1929 (`bpt6k9105652d`): p. 146, f174, p. 147, f175; sgt1930 (`bpt6k9105652d`): p. 150, f708, p. 151, f709; sgt1935 (`bpt6k9105653t`): p. 86, f106, p. 87, f107; sgt1936 (`bpt6k91056547`): p. 64, f75, p. 65, f76; sgt1939 (`bpt6k9105739w`): p. 68, f74, p. 69, f75.

Transcriptions: `../transcribed/education_sum_<edition>.txt`; rebuild with `python3 data-raw/yearbook_health_education/extract_education_summary.py build`. Per-check output: `education_summary_validation.json`.

Rows: 240. Years: 1919–1939 (20 years: 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939).

Printed for overlapping year windows: every cell of a year is taken from the **latest** edition that prints that year (SPEC_ADDENDUM rule 4; `census` = that edition) and every other printing of the same cell is compared below. Duplicate printings are not stored.

Years printed by each edition: sgt1922 1919, 1920, 1921, 1922; sgt1923 1920, 1921, 1922, 1923; sgt1924 1921, 1922, 1923, 1924; sgt1925 1922, 1923, 1924, 1925; sgt1926 1923, 1924, 1925, 1926; sgt1927 1924, 1925, 1926, 1927; sgt1928 1925, 1926, 1927, 1928; sgt1929 1926, 1927, 1928, 1929; sgt1930 1927, 1928, 1929, 1930; sgt1935 1932, 1933, 1934, 1935; sgt1936 1933, 1934, 1935, 1936; sgt1939 1936, 1937, 1938, 1939.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number; pages without a printed number are inferred from the next page. For the two-page spreads (population, primary-education and first-degree totals) the boys' block is given the left-hand page and the girls' block and total columns the right-hand page (the printed fold falls near the boys' TOTAUX, so one or two boys' columns may in fact sit on the right-hand page)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (31 December of that year for pupils; the school year's examinations)
- `sex`: `male`, `female`; `total` where the cell is not split by sex (empty in the comparative table for items that are not pupils)
- `sex_fr`: column heading as printed (Aspirants / Aspirantes in the examination table, Garçons / Filles elsewhere)
- `nationality`: `french`, `muslim`, `jewish`, `italian`, `maltese`, `other` (Divers); `total` where not split
- `nationality_fr`: column heading as printed (masculine for boys, feminine for girls)
- `value`: count (integer); printed » = 0; empty where the cell is not printed (`not_applicable`)
- `flag`: empty, or `ocr_corrected`, `derived_from_totals`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (TOTAUX, Totaux généraux, subtotals, A reporter) are not stored unless stated; they were used for validation.

Yearly series of the "Total général des établissements scolaires français publics et privés" by sex and nationality: each edition prints its own year (row Total général of the population table) and the same totals for the three previous years ("Comparaison avec les trois années précédentes"). Rule 4: each year from the latest edition. No edition prints 1931 (the series of yearbooks has no 1931–1934 editions; sgt1935 compares with 1932–1934). sgt1922 compares with 1919–1921.

Differences between printings are listed below; in each case the latest printing is consistent with the row totals printed with it (sgt1923 1923 Israélites boys 5.580 is a misprint of 5.500; sgt1929 1929 Diverses girls 200, sgt1930 201 closes the girls' total 23.009; sgt1935 1933 Italiennes 5.149, sgt1936 5.119 closes the 1933 row 27.914).

## Validation

- Checks against printed totals: 0; passed: 0; failed: 0.

- Overlapping printings: 336 cell comparisons between editions; 3 differences.

| year | cell | edition | printed | latest edition | printed | stored (edition, flag) |
|---|---|---|---|---|---|---|
| 1923 | male/jewish | sgt1923 | 5580 | sgt1926 | 5500 | 5500 (sgt1926) |
| 1929 | female/other | sgt1929 | 200 | sgt1930 | 201 | 201 (sgt1930) |
| 1933 | female/italian | sgt1935 | 5149 | sgt1936 | 5119 | 5119 (sgt1936) |

- Flagged cells: total_mismatch: 1.

  - sgt1939 1939 male / french = 14349 (total_mismatch)
