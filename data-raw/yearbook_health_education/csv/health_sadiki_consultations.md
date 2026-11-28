# Hôpital Sadiki : mouvement de la consultation et des pansements externes ; opérations

*Sadiki Hospital: external consultations and dressings; operations.*

Source: *Statistique générale de la Tunisie*, chapter III (health), editions sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1925 (`bpt6k9105650k`): p. 59, f83; sgt1926 (`bpt6k9105650k`): p. 68, f632; sgt1927 (`bpt6k91056510`): p. 66, f94; sgt1928 (`bpt6k91056510`): p. 66, f618; sgt1929 (`bpt6k9105652d`): p. 68, f96; sgt1930 (`bpt6k9105652d`): p. 72, f630; sgt1935 (`bpt6k9105653t`): p. 45, f65; sgt1936 (`bpt6k91056547`): p. 35, f46; sgt1939 (`bpt6k9105739w`): p. 36, f42.

Transcriptions: `../transcribed/health_pop_<edition>.txt`, section `@sadiki_consultations`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_population.py build`. Per-check output: `health_validation.json`.

Rows: 93. Years: 1905–1939 (33 years: 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1933, 1934, 1935, 1936, 1937, 1938, 1939).

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition) and every other printing of the same cell is compared below. Duplicate printings are not stored.

Years printed by each edition: sgt1922 1918–1922; sgt1923 1914–1923; sgt1924 1905–1924; sgt1925 1905–1925; sgt1926 1917–1926; sgt1927 1918–1927; sgt1928 1919–1928; sgt1929 1920–1929; sgt1930 1921–1930; sgt1935 1933–1935; sgt1936 1934–1936; sgt1939 1937–1939.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to
- `measure`: what is counted (see below)
- `measure_fr`: column heading (French)
- `value`: count (integer), except where the notes say otherwise; printed » = 0
- `flag`: empty, or `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (row totals, TOTAUX lines, nationality brackets) and the printed "différence en plus / en moins" columns are not stored; they were used for validation.

Table d) consultations, external dressings and operations. sgt1922–sgt1923 print one column "Consultations et pansements externes" (stored as `total`); sgt1924–sgt1925 go back to 1905, with only totals for 1905–1916 (parts printed »; the total is stored); from sgt1936 a third part is added, "Électrothérapie, R. ultra-violets, radiographie, radioscopie, teigne" (`electrotherapy`), and the 1934–1935 totals reprinted there include it (253.941 and 276.530 against 243.992 and 261.780 in sgt1935). Totals are stored only where the parts are not printed.

1924 external dressings are printed 898.176 in sgt1924 and sgt1925 and 88.176 in sgt1926–sgt1930 (88.176 + 27.815 = 115.991, the printed total); rule 4 keeps 88.176. 1910 total: 24.594 (sgt1924) vs 24.584 (sgt1925, kept). 1919: 63.261 + 20.389 = 83.650 against 83.640 in all five printings; 1936: parts 339.090 against 338.786.

## Validation

- Checks against printed totals: 76; passed: 68; failed: 8.

Failed checks (printed values kept; every one was re-read on the page image and the printed figures are as transcribed; see the commentary above for the cells involved):

  - sgt1924 sadiki_consultations 1919: parts vs total: cells give 83650, printed 83640
  - sgt1924 sadiki_consultations 1924: parts vs total: cells give 925991, printed 115991
  - sgt1925 sadiki_consultations 1919: parts vs total: cells give 83650, printed 83640
  - sgt1925 sadiki_consultations 1924: parts vs total: cells give 925991, printed 115991
  - sgt1926 sadiki_consultations 1919: parts vs total: cells give 83650, printed 83640
  - sgt1927 sadiki_consultations 1919: parts vs total: cells give 83650, printed 83640
  - sgt1928 sadiki_consultations 1919: parts vs total: cells give 83650, printed 83640
  - sgt1936 sadiki_consultations 1936: parts vs total: cells give 339090, printed 338786

- Overlapping printings: 298 cell comparisons between editions; 5 differences.

| year | cell | edition | printed | latest edition | printed | stored (edition, flag) |
|---|---|---|---|---|---|---|
| 1910 | total | sgt1924 | 24594 | sgt1925 | 24584 | 24584 (sgt1925) |
| 1924 | external_dressings | sgt1924 | 898176 | sgt1930 | 88176 | 88176 (sgt1930) |
| 1924 | external_dressings | sgt1925 | 898176 | sgt1930 | 88176 | 88176 (sgt1930) |
| 1934 | total | sgt1935 | 243992 | sgt1936 | 253941 | not stored (printed total) |
| 1935 | total | sgt1935 | 261780 | sgt1936 | 276530 | not stored (printed total) |

- Flagged cells: none.
