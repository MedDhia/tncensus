# Gaz : consommation (ville de Tunis)

*Gas consumption and receipts, city of Tunis, public and private lighting.*

Source: *Statistique générale de la Tunisie*, chapter II *Communes*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 39, f63; sgt1923 (`bpt6k9105649x`): p. 43, f545; sgt1924 (`bpt6k9105649x`): p. 43, f1033; sgt1925 (`bpt6k9105650k`): p. 43, f67; sgt1926 (`bpt6k9105650k`): p. 51, f615; sgt1927 (`bpt6k91056510`): p. 51, f79; sgt1928 (`bpt6k91056510`): p. 51, f603; sgt1929 (`bpt6k9105652d`): p. 51, f79; sgt1930 (`bpt6k9105652d`): p. 53, f611; sgt1935 (`bpt6k9105653t`): p. 30, f50; sgt1936 (`bpt6k91056547`): p. 22, f33.

Transcriptions: `../transcribed/communes_<edition>.txt`, section `@gas`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_communes.py build`. Per-check output: `communes_validation.json`.

Rows: 96. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936.

Unit: francs (French/Tunisian franc), as printed, centimes kept.

Printed for overlapping ten-year windows: each year is taken from the **latest** edition that prints it (rule 4) and every other printing compared.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section (`budget`, `property`, `gas`)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: budget year (exercice) / year of the 31 December valuation
- `commune`: commune name exactly as printed in the edition the value is taken from (footnote calls such as `Kram (Le) (1)` kept)
- `lighting`: `public_lighting` (Éclairage public) or `private_lighting` (Éclairage privé)
- `lighting_fr`: column heading (French)
- `measure`: `receipts` (Recettes) or `expenditure` (Dépenses)
- `measure_fr`: column heading as printed
- `value`: francs, centimes kept (two decimals); printed » = 0.00. Gas: consumption in cubic metres (integer), receipts in francs with centimes
- `flag`: empty, `reprint_corrected`, `row_realigned`, `illegible` or `not_applicable` (see below)

"Gaz : consommation (ville de Tunis)" (table b) of the *Service des eaux* pages in sgt1922–sgt1929, "GAZ — Consommation (ville de Tunis)" from sgt1930): for ten years (sgt1936: 1932–1936), the gas consumed (*Consommation*, cubic metres) and the receipts (*Recettes*, francs) for public lighting (*Éclairage public*) and private lighting (*Éclairage privé*); the TOTAL GÉNÉRAL columns are not stored (used for the row checks). sgt1939 prints no such series (only *Exploitation du gaz à Tunis* 1938–1939, not extracted).

**How the cells were read.** Each printing was drafted from Gallica's OCR; every cell where the OCR of the 2–8 printings of a year disagreed, or did not parse, was read on a native-resolution crop of that printing (48 cells), and the rows missed by the OCR (sgt1926 1924–1925, sgt1927 1925, sgt1930 1921, sgt1936 1932–1936) were read on the images. Cells on which the OCR of all printings agreed were not looked at one by one; the overlap comparison is therefore only as independent as the OCR.

The only difference between printings is sgt1928, 1925 public consumption, printed 812.614 (every other printing 312.614; 312.614 + 2.200.875 = 2.513.489, the printed total), stored from sgt1930 (312.614) as rule 4 says. 1934 receipts are printed » in sgt1935 and sgt1936 while consumption is given: stored as NA, `not_applicable` (not reported). 1926 repeats the 1925 consumption figures (312.614 / 2.200.875 / 2.513.489) in all five printings, with different receipts; kept as printed. 1922 private consumption is printed "1.459 904" (1.459.904).

Row-check failures repeat identically in every printing (they are in the print): e.g. 1919 receipts 32.080,83 + 417.468,30 = 449.549,13 printed 469.549,13; 1920 68.636,98 + 472.404,90 printed 496.041,88; 1925 539.725,47 + 1.964.968,81 printed 2.484.694,28; 1936 (sgt1936) 47.340,43 + 7.788.430,21 printed 4.835.770,64.

## Validation

- Checks against printed totals: 208; passed: 168; failed: 40.

Failed checks (printed values kept):

  - sgt1922 p.39 1916 rec: public + private vs total: cells give 512652.99, printed 512752.99 (difference 100.00)
  - sgt1922 p.39 1919 rec: public + private vs total: cells give 449549.13, printed 469549.13 (difference 20000.00)
  - sgt1922 p.39 1920 rec: public + private vs total: cells give 541041.88, printed 496041.88 (difference -45000.00)
  - sgt1923 p.43 1916 rec: public + private vs total: cells give 512652.99, printed 512752.99 (difference 100.00)
  - sgt1923 p.43 1919 rec: public + private vs total: cells give 449549.13, printed 469549.13 (difference 20000.00)
  - sgt1923 p.43 1920 rec: public + private vs total: cells give 541041.88, printed 496041.88 (difference -45000.00)
  - sgt1924 p.43 1916 rec: public + private vs total: cells give 512652.99, printed 512752.99 (difference 100.00)
  - sgt1924 p.43 1919 rec: public + private vs total: cells give 449549.13, printed 469549.13 (difference 20000.00)
  - sgt1924 p.43 1920 rec: public + private vs total: cells give 541041.88, printed 496041.88 (difference -45000.00)
  - sgt1924 p.43 1924 rec: public + private vs total: cells give 1880594.00, printed 1880595.00 (difference 1.00)
  - sgt1925 p.43 1916 rec: public + private vs total: cells give 512652.99, printed 512752.99 (difference 100.00)
  - sgt1925 p.43 1919 rec: public + private vs total: cells give 449549.13, printed 469549.13 (difference 20000.00)
  - sgt1925 p.43 1920 rec: public + private vs total: cells give 541041.88, printed 496041.88 (difference -45000.00)
  - sgt1925 p.43 1924 rec: public + private vs total: cells give 1880594.00, printed 1880595.00 (difference 1.00)
  - sgt1925 p.43 1925 rec: public + private vs total: cells give 2504694.28, printed 2484694.28 (difference -20000.00)
  - sgt1926 p.51 1919 rec: public + private vs total: cells give 449549.13, printed 469549.13 (difference 20000.00)
  - sgt1926 p.51 1920 rec: public + private vs total: cells give 541041.88, printed 496041.88 (difference -45000.00)
  - sgt1926 p.51 1924 rec: public + private vs total: cells give 1880594.00, printed 1880595.00 (difference 1.00)
  - sgt1926 p.51 1925 rec: public + private vs total: cells give 2504694.28, printed 2484694.28 (difference -20000.00)
  - sgt1927 p.51 1919 rec: public + private vs total: cells give 449549.13, printed 469549.13 (difference 20000.00)
  - sgt1927 p.51 1920 rec: public + private vs total: cells give 541041.88, printed 496041.88 (difference -45000.00)
  - sgt1927 p.51 1924 rec: public + private vs total: cells give 1880594.00, printed 1880595.00 (difference 1.00)
  - sgt1927 p.51 1925 rec: public + private vs total: cells give 2504694.28, printed 2484694.28 (difference -20000.00)
  - sgt1928 p.51 1919 rec: public + private vs total: cells give 449549.13, printed 469549.13 (difference 20000.00)
  - sgt1928 p.51 1920 rec: public + private vs total: cells give 541041.88, printed 496041.88 (difference -45000.00)
  - sgt1928 p.51 1924 rec: public + private vs total: cells give 1880594.00, printed 1880595.00 (difference 1.00)
  - sgt1928 p.51 1925 cons: public + private vs total: cells give 3013489, printed 2513489 (difference -500000)
  - sgt1928 p.51 1925 rec: public + private vs total: cells give 2504694.28, printed 2484694.28 (difference -20000.00)
  - sgt1928 p.51 1928 rec: public + private vs total: cells give 3527778.40, printed 3527778.35 (difference -0.05)
  - sgt1929 p.51 1920 rec: public + private vs total: cells give 541041.88, printed 496041.88 (difference -45000.00)
  - sgt1929 p.51 1924 rec: public + private vs total: cells give 1880594.00, printed 1880595.00 (difference 1.00)
  - sgt1929 p.51 1925 rec: public + private vs total: cells give 2504694.28, printed 2484694.28 (difference -20000.00)
  - sgt1929 p.51 1928 rec: public + private vs total: cells give 3527778.40, printed 3527778.35 (difference -0.05)
  - sgt1930 p.53 1924 rec: public + private vs total: cells give 1880594.00, printed 1880595.00 (difference 1.00)
  - sgt1930 p.53 1925 rec: public + private vs total: cells give 2504694.28, printed 2484694.28 (difference -20000.00)
  - sgt1930 p.53 1928 rec: public + private vs total: cells give 3527778.40, printed 3527778.35 (difference -0.05)
  - sgt1930 p.53 1930 rec: public + private vs total: cells give 4257608.03, printed 4277608.03 (difference 20000.00)
  - sgt1935 p.30 1928 rec: public + private vs total: cells give 3527778.40, printed 3527778.35 (difference -0.05)
  - sgt1935 p.30 1930 rec: public + private vs total: cells give 4257608.03, printed 4277608.03 (difference 20000.00)
  - sgt1936 p.22 1936 rec: public + private vs total: cells give 7835770.64, printed 4835770.64 (difference -3000000.00)

- Overlapping printings: 486 cell comparisons between editions; 1 differences.

| year | commune | column | edition | printed | latest edition | printed |
|---|---|---|---|---|---|---|
| 1925 | Tunis | cons_public | sgt1928 | 812614 | sgt1930 | 312614 |

- Flagged cells: not_applicable: 2.

  - sgt1936 1934 Tunis receipts = NA (not_applicable)
  - sgt1936 1934 Tunis receipts = NA (not_applicable)
