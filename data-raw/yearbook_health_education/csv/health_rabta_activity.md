# Hôpital de la Rabta : mouvement de la population

*Rabta hospital: patient-days, admissions, mean stay.*

Source: *Statistique générale de la Tunisie*, chapter III (health), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1922 (`bpt6k9105649x`): p. 52, f76; sgt1923 (`bpt6k9105649x`): p. 58, f560; sgt1924 (`bpt6k9105649x`): p. 60, f1050; sgt1925 (`bpt6k9105650k`): p. 60, f84; sgt1926 (`bpt6k9105650k`): p. 69, f633; sgt1927 (`bpt6k91056510`): p. 67, f95; sgt1928 (`bpt6k91056510`): p. 67, f619; sgt1929 (`bpt6k9105652d`): p. 69, f97; sgt1930 (`bpt6k9105652d`): p. 73, f631; sgt1935 (`bpt6k9105653t`): p. 46, f66; sgt1936 (`bpt6k91056547`): p. 36, f47; sgt1939 (`bpt6k9105739w`): p. 37, f43.

Transcriptions: `../transcribed/health_pop_<edition>.txt`, section `@rabta_population`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_population.py build`. Per-check output: `health_validation.json`.

Rows: 120. Years: 1921–1939 (15 years: 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1934, 1935, 1936, 1938, 1939).

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

Table c) "Mouvement de la population" of the Rabta (indicators as in the civil hospital file; staff days include half days, e.g. 4.817,5).

**sgt1935, 1934 column**: admissions and mean daily patients are printed in each other's row (admissions 196,147, mean daily 2.408; the 1935 column and the differences, +112 admissions, show the intended order). Kept as printed and flagged `total_mismatch`.

**Paying / indigent rows from sgt1936**: sgt1936 and sgt1939 print the row "indigents" first with a small figure (1935: 2.973; 1938: 4.146) and "payants" second with the large one (68.698; 77.366), the reverse of every earlier edition (sgt1935: payants 2.973, indigents 68.698). For 1935 the sgt1935 values are kept (`reprint_corrected`, both rows); 1936, 1938 and 1939, printed only there, are stored under the labels as printed, which are very probably swapped. 1935 mean stay: sgt1936 prints 28,410; 71.671 / 2.520 = 28,44 as in sgt1935 (kept, `reprint_corrected`). 1925 mean stay: 27,051 (sgt1925) vs 27,031 (sgt1926, kept; 16.543 / 612 = 27,03).

1939: paying 64.161 + indigent 6.659 = 70.820 against 70.730 patient days.

## Validation

- Checks against printed totals: 120; passed: 110; failed: 10.

Failed checks (printed values kept; every one was re-read on the page image and the printed figures are as transcribed; see the commentary above for the cells involved):

  - sgt1922 rabta_population Journées du personnel nourri: difference: cells give -578, printed -576
  - sgt1923 rabta_population Journées du personnel non nourri: difference: cells give 2, printed 12
  - sgt1926 rabta_population Journées de malades: difference: cells give 9548, printed 9458
  - sgt1927 rabta_population Journées de malades payants: difference: cells give 204, printed 214
  - sgt1935 rabta_population Nombre d'admissions: difference: cells give 2323.853, printed 112
  - sgt1935 rabta_population Effectif moyen journalier: difference: cells give -2211.642, printed 1211
  - sgt1936 rabta_population Durée moyenne de séjour par malade: difference: cells give -3.31, printed -2.34
  - sgt1936 rabta_population Journées du personnel nourri: difference: cells give -281, printed -381
  - sgt1939 rabta_population Journées de malades indigents: difference: cells give 2513, printed 2423
  - sgt1939 rabta_population 1939: patient-day categories vs patient days: cells give 70820, printed 70730

- Overlapping printings: 72 cell comparisons between editions; 4 differences.

| year | cell | edition | printed | latest edition | printed | stored (edition, flag) |
|---|---|---|---|---|---|---|
| 1925 | mean_stay_days | sgt1925 | 27.051 | sgt1926 | 27.031 | 27.031 (sgt1926) |
| 1935 | patient_days_paying | sgt1935 | 2973 | sgt1936 | 68698 | 2973 (sgt1935, reprint_corrected) |
| 1935 | patient_days_indigent | sgt1935 | 68698 | sgt1936 | 2973 | 68698 (sgt1935, reprint_corrected) |
| 1935 | mean_stay_days | sgt1935 | 28.440 | sgt1936 | 28.410 | 28.44 (sgt1935, reprint_corrected) |

- Flagged cells: reprint_corrected: 3, total_mismatch: 2.

  - sgt1935 1934 admissions / Nombre d'admissions = 196.147 (total_mismatch)
  - sgt1935 1934 mean_daily_patients / Effectif moyen journalier = 2408 (total_mismatch)
  - sgt1935 1935 patient_days_paying / Journées de malades payants = 2973 (reprint_corrected)
  - sgt1935 1935 patient_days_indigent / Journées de malades indigents = 68698 (reprint_corrected)
  - sgt1935 1935 mean_stay_days / Durée moyenne de séjour par malade = 28.44 (reprint_corrected)
