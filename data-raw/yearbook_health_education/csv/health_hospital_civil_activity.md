# Hôpital civil français de Tunis : mouvement de la population

*French Civil Hospital of Tunis: patient-days, admissions, mean stay.*

Source: *Statistique générale de la Tunisie*, chapter III (health), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1922 (`bpt6k9105649x`): p. 49, f73; sgt1923 (`bpt6k9105649x`): p. 55, f557; sgt1924 (`bpt6k9105649x`): p. 57, f1047; sgt1925 (`bpt6k9105650k`): p. 57, f81; sgt1926 (`bpt6k9105650k`): p. 66, f630; sgt1927 (`bpt6k91056510`): p. 64, f92; sgt1928 (`bpt6k91056510`): p. 64, f616; sgt1929 (`bpt6k9105652d`): p. 66, f94; sgt1930 (`bpt6k9105652d`): p. 70, f628; sgt1935 (`bpt6k9105653t`): p. 42, f62; sgt1936 (`bpt6k91056547`): p. 32, f43; sgt1939 (`bpt6k9105739w`): p. 33, f39.

Transcriptions: `../transcribed/health_pop_<edition>.txt`, section `@civil_population`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_population.py build`. Per-check output: `health_validation.json`.

Rows: 104. Years: 1921–1939 (15 years: 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1934, 1935, 1936, 1938, 1939).

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition) and every other printing of the same cell is compared below. Duplicate printings are not stored.

Years printed by each edition: sgt1922 1921–1922; sgt1923 1922–1923; sgt1924 1923–1924; sgt1925 1924–1925; sgt1926 1925–1926; sgt1927 1926–1927; sgt1928 1927–1928; sgt1929 1928–1929; sgt1930 1928–1930; sgt1935 1934–1935; sgt1936 1935–1936; sgt1939 1938–1939.

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

Table c) "Mouvement de la population": two year columns (three in sgt1930: 1928, 1929, 1930) and a "différence en plus / en moins" pair, which is not stored. Indicators: `patient_days` (Journées de malades), `patient_days_paying`, `patient_days_indigent`, `admissions` (Nombre d'admissions), `mean_daily_patients` (Effectif moyen journalier), `mean_stay_days` (Durée moyenne du séjour par malade, days), `staff_days_fed` / `staff_days_not_fed` (Journées du personnel nourri / non nourri; not printed from sgt1929 on). `mean_daily_patients` and `mean_stay_days` are rates (decimals where printed); all other values are counts. In sgt1925 the patient-days total is printed under the two parts ("Totaux").

The 1924–1935 day counts are also printed in table b) "Prix moyen de la journée de traitement", a cost table that was not extracted (out of scope: financial). It was used to settle two conflicts: **1926 staff days**: sgt1927 table c) prints 70.687 / 36.518, but its own table b) and sgt1926 (tables b and c) print 41.687 / 3.518; the sgt1926 values are kept (`reprint_corrected`). **1929 patient days**: sgt1930 prints 110.446, but 46.245 + 63.901 = 110.146, as printed in sgt1929 tables b) and c); kept from sgt1929 (`reprint_corrected`).

Other differences between printings, kept per rule 4: 1925 paying / indigent days are 51.258 / 48.893 in sgt1925 and 33.426 / 66.725 in sgt1926 (both pairs sum to the 100.151 printed in both); 1925 mean daily patients 274 (sgt1925) and 276 (sgt1926; 100.151 / 365 = 274,4).

Failed difference checks are misprints in the printed "différence" columns (e.g. sgt1927 prints +26 for 273 → 301); the stored year values were re-read on the images. sgt1936 prints 1936 patient days 150.255 against parts summing to 150.235.

## Validation

- Checks against printed totals: 107; passed: 99; failed: 8.

Failed checks (printed values kept; every one was re-read on the page image and the printed figures are as transcribed; see the commentary above for the cells involved):

  - sgt1923 civil_population Journées de malades: difference: cells give -127, printed 0
  - sgt1926 civil_population Effectif moyen journalier: difference: cells give -3, printed 3
  - sgt1926 civil_population Durée moyenne du séjour par malade: difference: cells give -0.62, printed -1.38
  - sgt1927 civil_population Effectif moyen journalier: difference: cells give 28, printed 26
  - sgt1929 civil_population Journées de malades payants: difference: cells give 5318, printed 5248
  - sgt1930 civil_population Journées de malades: difference: cells give 14128, printed 14428
  - sgt1930 civil_population 1929: patient-day categories vs patient days: cells give 110146, printed 110446
  - sgt1936 civil_population 1936: patient-day categories vs patient days: cells give 150235, printed 150255

- Overlapping printings: 72 cell comparisons between editions; 6 differences.

| year | cell | edition | printed | latest edition | printed | stored (edition, flag) |
|---|---|---|---|---|---|---|
| 1925 | patient_days_paying | sgt1925 | 51258 | sgt1926 | 33426 | 33426 (sgt1926) |
| 1925 | patient_days_indigent | sgt1925 | 48893 | sgt1926 | 66725 | 66725 (sgt1926) |
| 1925 | mean_daily_patients | sgt1925 | 274 | sgt1926 | 276 | 276 (sgt1926) |
| 1926 | staff_days_fed | sgt1926 | 41687 | sgt1927 | 70687 | 41687 (sgt1926, reprint_corrected) |
| 1926 | staff_days_not_fed | sgt1926 | 3518 | sgt1927 | 36518 | 3518 (sgt1926, reprint_corrected) |
| 1929 | patient_days | sgt1929 | 110146 | sgt1930 | 110446 | 110146 (sgt1929, reprint_corrected) |

- Flagged cells: reprint_corrected: 3.

  - sgt1926 1926 staff_days_fed / Journées du personnel nourri = 41687 (reprint_corrected)
  - sgt1926 1926 staff_days_not_fed / Journées du personnel non nourri = 3518 (reprint_corrected)
  - sgt1929 1929 patient_days / Journées de malades = 110146 (reprint_corrected)
