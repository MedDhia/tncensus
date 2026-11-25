# Bibliothèques

*Libraries: loans and volumes lent.*

Source: *Statistique générale de la Tunisie*, chapter "Instruction publique et beaux-arts" (VII; VI in sgt1936 and sgt1939), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1922 (`bpt6k9105649x`): p. 93, f117; sgt1923 (`bpt6k9105649x`): p. 99, f601; sgt1924 (`bpt6k9105649x`): p. 101, f1091; sgt1925 (`bpt6k9105650k`): p. 103, f127; sgt1926 (`bpt6k9105650k`): p. 113, f677; sgt1927 (`bpt6k91056510`): p. 111, f139; sgt1928 (`bpt6k91056510`): p. 111, f663; sgt1929 (`bpt6k9105652d`): p. 113, f141; sgt1930 (`bpt6k9105652d`): p. 117, f675; sgt1935 (`bpt6k9105653t`): p. 83, f103; sgt1936 (`bpt6k91056547`): p. 61, f72; sgt1939 (`bpt6k9105739w`): p. 63, f69.

Transcriptions: `../transcribed/education_sum_<edition>.txt`; rebuild with `python3 data-raw/yearbook_health_education/extract_education_summary.py build`. Per-check output: `education_summary_validation.json`.

Rows: 120. Years: 1921–1939 (15 years: 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1934, 1935, 1936, 1938, 1939).

Printed for overlapping year windows: every cell of a year is taken from the **latest** edition that prints that year (SPEC_ADDENDUM rule 4; `census` = that edition) and every other printing of the same cell is compared below. Duplicate printings are not stored.

Years printed by each edition: sgt1922 1921, 1922; sgt1923 1922, 1923; sgt1924 1923, 1924; sgt1925 1924, 1925; sgt1926 1925, 1926; sgt1927 1926, 1927; sgt1928 1927, 1928; sgt1929 1928, 1929; sgt1930 1929, 1930; sgt1935 1934, 1935; sgt1936 1935, 1936; sgt1939 1938, 1939.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number; pages without a printed number are inferred from the next page. For the two-page spreads (population, primary-education and first-degree totals) the boys' block is given the left-hand page and the girls' block and total columns the right-hand page (the printed fold falls near the boys' TOTAUX, so one or two boys' columns may in fact sit on the right-hand page)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (31 December of that year for pupils; the school year's examinations)
- `library`: English code
- `library_fr`: library as printed
- `measure`: what is counted (see below)
- `measure_fr`: as printed
- `value`: count (integer); printed » = 0; empty where the cell is not printed (`not_applicable`)
- `flag`: empty, or `ocr_corrected`, `derived_from_totals`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (TOTAUX, Totaux généraux, subtotals, A reporter) are not stored unless stated; they were used for validation.

Table "Bibliothèques": loans (`loans`, Prêts) and volumes lent (`volumes_lent`, Volumes prêtés) for the public library of Tunis, the circulating library, the popular library of Tunis and the popular libraries of the interior, two years per edition. The popular libraries are numbered "3°" twice as printed. sgt1939 footnote: loans suspended from 15 September to 10 October (1939).

## Footnotes printed under the table

- (1) Prêts suspendus du 15 septembre au 10 octobre. (sgt1939)

## Validation

- Checks against printed totals: 0; passed: 0; failed: 0.

- Overlapping printings: 72 cell comparisons between editions; 1 differences.

| year | cell | edition | printed | latest edition | printed | stored (edition, flag) |
|---|---|---|---|---|---|---|
| 1935 | popular_interior/loans | sgt1935 | 41501 | sgt1936 | 41500 | 41500 (sgt1936) |

- Flagged cells: none.
