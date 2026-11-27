# Superficie : superficie territoriale ; répartition en superficie productive et improductive ; répartition de la superficie productive ; répartition de la superficie labourable

*Land area: territorial area and population density; productive and unproductive area; use of the productive area; use of the arable area.*

Source: *Statistique générale de la Tunisie*, chapter *Agriculture*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 209, f233; sgt1923 (`bpt6k9105649x`): p. 221, f723; sgt1924 (`bpt6k9105649x`): p. 229, f1219; sgt1925 (`bpt6k9105650k`): p. 265, f289; sgt1926 (`bpt6k9105650k`): p. 241, f805; sgt1927 (`bpt6k91056510`): p. 233, f261; sgt1928 (`bpt6k91056510`): p. 233, f785; sgt1929 (`bpt6k9105652d`): p. 235, f263; sgt1930 (`bpt6k9105652d`): p. 239, f797; sgt1935 (`bpt6k9105653t`): p. 121, f141; sgt1936 (`bpt6k91056547`): p. 91, f102; sgt1939 (`bpt6k9105739w`): p. 94, f100.

Transcriptions: `../transcribed/agriculture_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_agriculture.py build`.

Rows: 348. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939.

Units: km2, persons, persons per km2, hectares and percent (`unit`); value_type: mixed.

Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept; `year` = edition year.

## Columns

- `census`: edition the value is taken from (rule 4 series: the latest edition printing that year; rule 5 tables: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (crop year = calendar year of the harvest, as printed; rule 5 tables: edition year)
- `part`: sub-table letter as printed (a-d)
- `part_fr`: printed sub-table title
- `item`: item code (English)
- `item_fr`: printed column heading
- `measure`: measure code (English)
- `measure_fr`: printed heading of the measure
- `unit`: unit of `value`, as printed (never converted)
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible`, `total_mismatch` (cell identified as the faulty one of a failed check, printed value kept), `derived_from_totals`, `not_applicable`

Printed on the first page of the chapter in every edition. The territorial area is 125.130 km2 in sgt1922 and 125.180 km2 from sgt1923; the density stays printed 16.72 through sgt1936 although the number of inhabitants changes with the censuses (2.093.939, 1921; 2.159.708, 1926; 2.410.692, 1931); sgt1939 prints 2.608.313 and 21.25. Totals (TOTAL de la superficie territoriale / productive / labourable, and their 100 %) are checks only.

Checks: hectares of the parts = printed total; percentages sum to 100 (to 0.2); each percentage = hectares / total (to 0.15 point). Percentages printed inconsistently with the hectares are kept as printed; they are listed among the failed checks.

Every failed check below was re-read on a zoomed native-resolution crop: they are printed inconsistencies (printed values kept). sgt1922 and sgt1936: the jachères are printed 100.000 ha too high (1.947.136 and 1.770.898; their own percentages fit 1.847.136 and 1.870.898): flagged `total_mismatch`. sgt1923 prints the terres de parcours at 59,4 % (50,9 % computed; flagged) and a labourable total of 2.840.000 for parts summing to 2.820.000. sgt1927 prints percentages of d) that do not fit the hectares (prairies 9,2 % flagged; others listed). sgt1928-sgt1929 print the 100 of the b) total as "00" (total line, not stored). sgt1936 prints the productive area with a broken digit ("9.?00.000"), stored 9.000.000 = 12.500.000 - 3.500.000 (`derived_from_totals`). The other failures are rounding of the printed percentages or differences of 1-180 ha.

Survey of the whole chapter in every edition: `agriculture_survey.md`.

## Validation

- Checks against printed totals and identities: 264; passed: 238; failed: 26.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.209 (f233) land_c forest: % = hectares / total: cells give 12.11, printed 11.1 (difference -1.01)
  - sgt1922 p.209 (f233) land_c rangeland: % = hectares / total: cells give 51.22, printed 52.4 (difference 1.18)
  - sgt1922 p.209 (f233) land_d hectares: parts vs total: cells give 2920000, printed 2820000 (difference -100000)
  - sgt1922 p.209 (f233) land_d fallow: % = hectares / total: cells give 69.05, printed 65.5 (difference -3.55)
  - sgt1923 p.221 (f723) land_c %: parts vs 100: cells give 108.3, printed 100 (difference -8.3)
  - sgt1923 p.221 (f723) land_c rangeland: % = hectares / total: cells give 50.94, printed 59.4 (difference 8.46)
  - sgt1923 p.221 (f723) land_d hectares: parts vs total: cells give 2820000, printed 2840000 (difference 20000)
  - sgt1923 p.221 (f723) land_d %: parts vs 100: cells give 99.3, printed 100 (difference 0.7)
  - sgt1925 p.265 (f289) land_d hectares: parts vs total: cells give 2844820, printed 2845000 (difference 180)
  - sgt1927 p.233 (f261) land_d hectares: parts vs total: cells give 2913001, printed 2913000 (difference -1)
  - sgt1927 p.233 (f261) land_d cereals: % = hectares / total: cells give 33.31, printed 32.3 (difference -1.01)
  - sgt1927 p.233 (f261) land_d fodder: % = hectares / total: cells give 1.03, printed 9.2 (difference 8.17)
  - sgt1927 p.233 (f261) land_d food_plants: % = hectares / total: cells give 1.36, printed 3.2 (difference 1.84)
  - sgt1927 p.233 (f261) land_d industrial_plants: % = hectares / total: cells give 0.16, printed 2.16 (difference 2.00)
  - sgt1927 p.233 (f261) land_d other_products: % = hectares / total: cells give 4.12, printed 3.1 (difference -1.02)
  - sgt1927 p.233 (f261) land_d fallow: % = hectares / total: cells give 60.02, printed 50.1 (difference -9.92)
  - sgt1928 p.233 (f785) land_b % of the total line: cells give 0, printed 100 (difference 100)
  - sgt1928 p.233 (f785) land_c %: parts vs 100: cells give 99.7, printed 100 (difference 0.3)
  - sgt1928 p.233 (f785) land_c arable: % = hectares / total: cells give 32.61, printed 32.4 (difference -0.21)
  - sgt1929 p.235 (f263) land_b % of the total line: cells give 0, printed 100 (difference 100)
  - sgt1930 p.239 (f797) land_d %: parts vs 100: cells give 99.0, printed 100 (difference 1.0)
  - sgt1930 p.239 (f797) land_d fallow: % = hectares / total: cells give 47.94, printed 47 (difference -0.94)
  - sgt1935 p.121 (f141) land_d %: parts vs 100: cells give 99.73, printed 100 (difference 0.27)
  - sgt1935 p.121 (f141) land_d fallow: % = hectares / total: cells give 46.19, printed 45.9 (difference -0.29)
  - sgt1936 p.91 (f102) land_d hectares: parts vs total: cells give 2834000, printed 2934000 (difference 100000)
  - sgt1936 p.91 (f102) land_d fallow: % = hectares / total: cells give 60.36, printed 63.77 (difference 3.41)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: derived_from_totals: 1, total_mismatch: 4.

  - sgt1922 p.209 1922 d / fallow_grazed / area / hectares = 1947136 (total_mismatch)
  - sgt1923 p.221 1923 c / rangeland_uncultivated / percent / percent = 59.4 (total_mismatch)
  - sgt1927 p.233 1927 d / artificial_meadows_fodder / percent / percent = 9.2 (total_mismatch)
  - sgt1936 p.91 1936 b / productive / area / hectares = 9000000 (derived_from_totals)
  - sgt1936 p.91 1936 d / fallow_grazed / area / hectares = 1770898 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (48 printings): sgt1922 f233, sgt1922 f233, sgt1922 f233, sgt1922 f233, sgt1923 f723, sgt1923 f723, sgt1923 f723, sgt1923 f723, sgt1924 f1219, sgt1924 f1219, sgt1924 f1219, sgt1924 f1219, sgt1925 f289, sgt1925 f289, sgt1925 f289, sgt1925 f289, sgt1926 f805, sgt1926 f805, sgt1926 f805, sgt1926 f805, sgt1927 f261, sgt1927 f261, sgt1927 f261, sgt1927 f261, sgt1928 f785, sgt1928 f785, sgt1928 f785, sgt1928 f785, sgt1929 f263, sgt1929 f263, sgt1929 f263, sgt1929 f263, sgt1930 f797, sgt1930 f797, sgt1930 f797, sgt1930 f797, sgt1935 f141, sgt1935 f141, sgt1935 f141, sgt1935 f141, sgt1936 f102, sgt1936 f102, sgt1936 f102, sgt1936 f102, sgt1939 f100, sgt1939 f100, sgt1939 f100, sgt1939 f100.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
