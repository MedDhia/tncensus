# Hôpital Sadiki : mouvement de la population

*Sadiki Hospital: patient-days, admissions, mean stay.*

Source: *Statistique générale de la Tunisie*, chapter III (health), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1922 (`bpt6k9105649x`): p. 50, f74; sgt1923 (`bpt6k9105649x`): p. 56, f558; sgt1924 (`bpt6k9105649x`): p. 59, f1049; sgt1925 (`bpt6k9105650k`): p. 59, f83; sgt1926 (`bpt6k9105650k`): p. 68, f632; sgt1927 (`bpt6k91056510`): p. 66, f94; sgt1928 (`bpt6k91056510`): p. 66, f618; sgt1929 (`bpt6k9105652d`): p. 68, f96; sgt1930 (`bpt6k9105652d`): p. 72, f630; sgt1935 (`bpt6k9105653t`): p. 44, f64; sgt1936 (`bpt6k91056547`): p. 34, f45; sgt1939 (`bpt6k9105739w`): p. 35, f41.

Transcriptions: `../transcribed/health_pop_<edition>.txt`, section `@sadiki_population`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_population.py build`. Per-check output: `health_validation.json`.

Rows: 126. Years: 1921–1939 (15 years: 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1934, 1935, 1936, 1938, 1939).

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition) and every other printing of the same cell is compared below. Duplicate printings are not stored.

Years printed by each edition: sgt1922 1921–1922; sgt1923 1922–1923; sgt1924 1923–1924; sgt1925 1924–1925; sgt1926 1925–1926; sgt1927 1926–1927; sgt1928 1927–1928; sgt1929 1928–1929; sgt1930 1929–1930; sgt1935 1934–1935; sgt1936 1935–1936; sgt1939 1938–1939.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to
- `indicator`: row code (listed in the commentary below / in the civil-hospital file)
- `indicator_fr`: row label as printed in the edition the value is taken from
- `value`: count (integer), except where the notes say otherwise; printed » = 0
- `flag`: empty, or `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (row totals, TOTAUX lines, nationality brackets) and the printed "différence en plus / en moins" columns are not stored; they were used for validation.

Table c) "Mouvement de la population" (two year columns plus differences, not stored). Indicators as in the civil hospital file; sgt1922 adds three patient-day categories (administrations, accidents de travail, blessés militaires; all »). Mean daily patients and mean stay are decimals.

1935 paying patient-days: sgt1936 prints 8.205, sgt1935 8.209 (8.209 + 75.297 = 83.506, printed in both): kept from sgt1935 (`reprint_corrected`). 1934 (sgt1935 only): paying 7.072 + indigent 78.134 = 85.206 against 85.226 printed (also 85.226 in table b). Most failed checks are misprinted difference columns (e.g. sgt1922 en moins 3.582 for 14.497 → 11.915; sgt1926 prints 398 for 1.398 and 465 for 4,65); the sgt1936 difference column is garbled throughout.

## Validation

- Checks against printed totals: 123; passed: 107; failed: 16.

Failed checks (printed values kept; every one was re-read on the page image and the printed figures are as transcribed; see the commentary above for the cells involved):

  - sgt1922 sadiki_population Journées de malades payants: difference: cells give -2582, printed -3582
  - sgt1924 sadiki_population Journées du personnel nourri: difference: cells give 565, printed 365
  - sgt1926 sadiki_population Journées de malades indigents: difference: cells give 1398, printed 398
  - sgt1926 sadiki_population Effectif moyen journalier: difference: cells give 4.65, printed 465
  - sgt1926 sadiki_population Journées du personnel non nourri: difference: cells give 1924, printed 1920
  - sgt1929 sadiki_population Journées de malades payants: difference: cells give 933, printed 1003
  - sgt1929 sadiki_population Journées du personnel nourri: difference: cells give 9490, printed 10510
  - sgt1935 sadiki_population Effectif moyen journalier: difference: cells give -4.71, printed -4.69
  - sgt1935 sadiki_population Journées du personnel non nourri: difference: cells give 24620, printed 24820
  - sgt1935 sadiki_population 1934: patient-day categories vs patient days: cells give 85206, printed 85226
  - sgt1936 sadiki_population Journées de malades: difference: cells give 6905, printed 0
  - sgt1936 sadiki_population Journées de malades payants: difference: cells give -1201, printed 5700
  - sgt1936 sadiki_population Journées de malades indigents: difference: cells give 8110, printed 6110
  - sgt1936 sadiki_population Durée moyenne du séjour par malade: difference: cells give -0.96, printed -0.46
  - sgt1936 sadiki_population Journées du personnel non nourri: difference: cells give 353, printed 155
  - sgt1936 sadiki_population 1935: patient-day categories vs patient days: cells give 83502, printed 83506

- Overlapping printings: 72 cell comparisons between editions; 1 differences.

| year | cell | edition | printed | latest edition | printed | stored (edition, flag) |
|---|---|---|---|---|---|---|
| 1935 | patient_days_paying | sgt1935 | 8209 | sgt1936 | 8205 | 8209 (sgt1935, reprint_corrected) |

- Flagged cells: reprint_corrected: 1.

  - sgt1935 1935 patient_days_paying / Journées de malades payants = 8209 (reprint_corrected)
