# Cantines scolaires : portions délivrées

*School canteens: portions served.*

Source: *Statistique générale de la Tunisie*, chapter "Instruction publique et beaux-arts" (VII; VI in sgt1936 and sgt1939), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1922 (`bpt6k9105649x`): p. 125, f149; sgt1923 (`bpt6k9105649x`): p. 131, f633; sgt1924 (`bpt6k9105649x`): p. 133, f1123; sgt1925 (`bpt6k9105650k`): p. 135, f159; sgt1926 (`bpt6k9105650k`): p. 145, f709; sgt1927 (`bpt6k91056510`): p. 143, f171; sgt1928 (`bpt6k91056510`): p. 143, f695; sgt1929 (`bpt6k9105652d`): p. 145, f173; sgt1930 (`bpt6k9105652d`): p. 149, f707; sgt1935 (`bpt6k9105653t`): p. 85, f105; sgt1936 (`bpt6k91056547`): p. 63, f74; sgt1939 (`bpt6k9105739w`): p. 67, f73.

Transcriptions: `../transcribed/education_sum_<edition>.txt`; rebuild with `python3 data-raw/yearbook_health_education/extract_education_summary.py build`. Per-check output: `education_summary_validation.json`.

Rows: 30. Years: 1921–1939 (15 years: 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1934, 1935, 1936, 1938, 1939).

Printed for overlapping year windows: every cell of a year is taken from the **latest** edition that prints that year (SPEC_ADDENDUM rule 4; `census` = that edition) and every other printing of the same cell is compared below. Duplicate printings are not stored.

Years printed by each edition: sgt1922 1921, 1922; sgt1923 1922, 1923; sgt1924 1923, 1924; sgt1925 1924, 1925; sgt1926 1925, 1926; sgt1927 1926, 1927; sgt1928 1927, 1928; sgt1929 1928, 1929; sgt1930 1929, 1930; sgt1935 1934, 1935; sgt1936 1935, 1936; sgt1939 1938, 1939.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number; pages without a printed number are inferred from the next page. For the two-page spreads (population, primary-education and first-degree totals) the boys' block is given the left-hand page and the girls' block and total columns the right-hand page (the printed fold falls near the boys' TOTAUX, so one or two boys' columns may in fact sit on the right-hand page)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (31 December of that year for pupils; the school year's examinations)
- `portions`: `free` (Gratuites) or `paying` (Payantes)
- `portions_fr`: as printed
- `value`: count (integer); printed » = 0; empty where the cell is not printed (`not_applicable`)
- `flag`: empty, or `ocr_corrected`, `derived_from_totals`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (TOTAUX, Totaux généraux, subtotals, A reporter) are not stored unless stated; they were used for validation.

"Cantines scolaires": portions served, free and paying, two years per edition (the Totaux line is a check). sgt1939 footnote: the 1938 free portions (295.327) are a rectified figure.

## Footnotes printed under the table

- The heading reads "Cantines scolaires (1923-1924)", but the columns are headed 1924 and 1925 and the 1924 column repeats the 1924 column of sgt1924. (sgt1925)
- (1) Chiffre rectifié (1938, portions gratuites). (sgt1939)

## Validation

- Checks against printed totals: 24; passed: 24; failed: 0.

- Overlapping printings: 18 cell comparisons between editions; 0 differences.

- Flagged cells: none.
