# Prix moyen de la journée de traitement

*Average cost of a patient-day, with patient-days, staff-days and expenditure: French Civil Hospital, Sadiki Hospital, Rabta hospital (sgt1922–sgt1935).*

Source: *Statistique générale de la Tunisie*, chapter III (health and assistance), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935. Source gallica.bnf.fr / BnF.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 49, f73, p. 51, f75; sgt1923 (`bpt6k9105649x`): p. 55, f557, p. 57, f559; sgt1925 (`bpt6k9105650k`): p. 58, f82; sgt1926 (`bpt6k9105650k`): p. 67, f631, p. 69, f633; sgt1927 (`bpt6k91056510`): p. 64, f92, p. 65, f93, p. 67, f95; sgt1928 (`bpt6k91056510`): p. 65, f617, p. 67, f619; sgt1929 (`bpt6k9105652d`): p. 66, f94, p. 67, f95, p. 69, f97; sgt1930 (`bpt6k9105652d`): p. 70, f628, p. 71, f629, p. 73, f631; sgt1935 (`bpt6k9105653t`): p. 42, f62, p. 44, f64, p. 46, f66.

Transcriptions: `../transcribed/health_finance_<edition>.txt`, sections `[day_cost]`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_finance.py build`. Per-check output: `health_finance_validation.json`.

Rows: 244. Years: 1912–1935 (22 years: 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1933, 1934, 1935). Unit of `value`: days (counts), francs; amounts are as printed, centimes kept as decimals (printed » = 0).

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition) and every other printing of the same cell is compared below. Duplicate printings are not stored.

Years printed by each edition: sgt1922 1918–1922; sgt1923 1914–1923; sgt1924 1915–1924; sgt1925 1912–1925; sgt1926 1917–1926; sgt1927 1918–1927; sgt1928 1919–1928; sgt1929 1920–1929; sgt1930 1921–1930; sgt1935 1933–1935.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (for a table over two pages, the page of the column group)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (budget year, account year or calendar year; see below)
- `hospital`: hospital as printed (day-cost table: `civil`, `sadiki`, `rabta`)
- `hospital_fr`: hospital name
- `measure`: what the value is (see below)
- `measure_fr`: column heading (French)
- `value`: days (counts), francs; empty where the flag says so
- `flag`: empty, or `derived_from_totals`, `total_mismatch`, `not_applicable`, `illegible`, `reprint_corrected` (see below)

"Prix moyen de la journée de traitement" of the Hôpital civil français (e) or b) in the civil-hospital pages), the Hôpital Sadiki and the Rabta contagious-diseases hospital (b)), sgt1922–sgt1930 and sgt1935 (not printed in sgt1936 and sgt1939). Measures: `patient_days`, `staff_days_fed`, `staff_days_not_fed` (counts; the Rabta has half days), `expenditure` ("Montant des dépenses", civil hospital "dépenses ordinaires", francs), `cost_per_patient_day` (francs, as printed: two decimals for the civil hospital, three for Sadiki and the Rabta; = expenditure / patient-days). The printed "Total des journées" is not stored (checked and compared). The civil hospital prints one row ("Civils") in sgt1922–sgt1924 and one year in sgt1925, then three- to five-year windows; Sadiki five- to fourteen-year windows (from 1912); the Rabta from 1918. sgt1935 prints 1933–1935 without expenditure and cost for 1935 (blank). This table was not in the inherited draft (the population-table worker skipped it); it was transcribed from the OCR and the page images.

Rule 4 exception: 1927 Sadiki cost per day is printed 22,861 in sgt1930 (the latest printing) and 22,361 in sgt1927–sgt1929 (1.985.314,45 / 88.784 = 22,361): the sgt1929 value is stored (`reprint_corrected`; re-read on the image). Other differences between printings are kept per rule 4 (table below): civil 1924 total days printed 65.850 in sgt1924 (166.252 later; the parts give 166.252) and expenditure 1.900.816,37 (1.900.811,37 later); civil 1925 total days 148.600 in sgt1925 (164.718 later); Sadiki 1914 expenditure 221.088,07 (sgt1923) / 221.088,17 (sgt1925), 1924 expenditure 1.102.825,72 (sgt1924) / 1.102.826,62 (sgt1925–sgt1930), 1923 cost per day 10,766 (sgt1923–sgt1924) / 10,889 (sgt1925–sgt1930; computed 10,777).

Failed checks repeated identically in every printing (print errors): Sadiki 1922 total days 133.046 against parts summing to 133.041, 1916 total 110.835 against 110.825; Rabta 1928 cost per day 11,811 against 474.031,91 / 28.352 = 16,72; Sadiki 1923 cost (above). Single printings: Sadiki 1912 cost 3,237 (computed 3,466); civil 1930 total days 211.161 (parts 211.261); civil 1933 and 1934 cost 29,76 and 27,02 (computed 31,45 and 28,70); Sadiki 1935 staff days fed 16.425 (total 155.776 needs 36.625; the sgt1935 activity table also prints 16.425). All re-read on the images.

## Remarks recorded in the transcriptions

- sgt1922: Day-cost table "Prix moyen de la journée de traitement" (number of patient-days and staff-days, expenditure in francs, cost per patient-day in francs as printed: 2 or 3 decimals). Row label = year; the civil-hospital table of sgt1922-sgt1925 has one row printed "Civils" (or the year), stored as the edition's year.
- sgt1923: Day-cost table "Prix moyen de la journée de traitement" (number of patient-days and staff-days, expenditure in francs, cost per patient-day in francs as printed: 2 or 3 decimals). Row label = year; the civil-hospital table of sgt1922-sgt1925 has one row printed "Civils" (or the year), stored as the edition's year.
- sgt1924: Day-cost table "Prix moyen de la journée de traitement" (number of patient-days and staff-days, expenditure in francs, cost per patient-day in francs as printed: 2 or 3 decimals). Row label = year; the civil-hospital table of sgt1922-sgt1925 has one row printed "Civils" (or the year), stored as the edition's year.
- sgt1925: Day-cost table "Prix moyen de la journée de traitement" (number of patient-days and staff-days, expenditure in francs, cost per patient-day in francs as printed: 2 or 3 decimals). Row label = year; the civil-hospital table of sgt1922-sgt1925 has one row printed "Civils" (or the year), stored as the edition's year. Rabta: half staff-days are printed as a separate "05" after the thousands ("4.817 05" = 4.817,5; the total 23.820,50 needs 4.817,5), as in the later reprints.
- sgt1926: Day-cost table "Prix moyen de la journée de traitement" (number of patient-days and staff-days, expenditure in francs, cost per patient-day in francs as printed: 2 or 3 decimals). Row label = year; the civil-hospital table of sgt1922-sgt1925 has one row printed "Civils" (or the year), stored as the edition's year.
- sgt1927: Day-cost table "Prix moyen de la journée de traitement" (number of patient-days and staff-days, expenditure in francs, cost per patient-day in francs as printed: 2 or 3 decimals). Row label = year; the civil-hospital table of sgt1922-sgt1925 has one row printed "Civils" (or the year), stored as the edition's year.
- sgt1928: Day-cost table "Prix moyen de la journée de traitement" (number of patient-days and staff-days, expenditure in francs, cost per patient-day in francs as printed: 2 or 3 decimals). Row label = year; the civil-hospital table of sgt1922-sgt1925 has one row printed "Civils" (or the year), stored as the edition's year.
- sgt1929: Day-cost table "Prix moyen de la journée de traitement" (number of patient-days and staff-days, expenditure in francs, cost per patient-day in francs as printed: 2 or 3 decimals). Row label = year; the civil-hospital table of sgt1922-sgt1925 has one row printed "Civils" (or the year), stored as the edition's year.
- sgt1930: Day-cost table "Prix moyen de la journée de traitement" (number of patient-days and staff-days, expenditure in francs, cost per patient-day in francs as printed: 2 or 3 decimals). Row label = year; the civil-hospital table of sgt1922-sgt1925 has one row printed "Civils" (or the year), stored as the edition's year.
- sgt1935: Day-cost table "Prix moyen de la journée de traitement" (number of patient-days and staff-days, expenditure in francs, cost per patient-day in francs as printed: 2 or 3 decimals). Row label = year; the civil-hospital table of sgt1922-sgt1925 has one row printed "Civils" (or the year), stored as the edition's year.

## Validation

- Checks against printed totals: 327; passed: 298; failed: 29.

Failed checks (printed values kept, unless a flag below says otherwise; `L<n>` = line of the transcription file). See the commentary above for which ones were re-read on the page images and which are repeated identically in several printings:

  - sgt1922 sadiki 1922: patient + staff days vs total days: cells give 133041, printed 133046
  - sgt1923 sadiki 1916: patient + staff days vs total days: cells give 110825, printed 110835
  - sgt1923 sadiki 1922: patient + staff days vs total days: cells give 133041, printed 133046
  - sgt1924 civil 1924: patient + staff days vs total days: cells give 166252, printed 65850
  - sgt1924 sadiki 1916: patient + staff days vs total days: cells give 110825, printed 110835
  - sgt1924 sadiki 1922: patient + staff days vs total days: cells give 133041, printed 133046
  - sgt1925 civil 1925: patient + staff days vs total days: cells give 164718, printed 148600
  - sgt1925 sadiki 1912: expenditure / patient days vs printed cost per day: cells give 3.47, printed 3.237
  - sgt1925 sadiki 1916: patient + staff days vs total days: cells give 110825, printed 110835
  - sgt1925 sadiki 1922: patient + staff days vs total days: cells give 133041, printed 133046
  - sgt1925 sadiki 1923: expenditure / patient days vs printed cost per day: cells give 10.78, printed 10.889
  - sgt1926 sadiki 1922: patient + staff days vs total days: cells give 133041, printed 133046
  - sgt1926 sadiki 1923: expenditure / patient days vs printed cost per day: cells give 10.78, printed 10.889
  - sgt1927 sadiki 1922: patient + staff days vs total days: cells give 133041, printed 133046
  - sgt1927 sadiki 1923: expenditure / patient days vs printed cost per day: cells give 10.78, printed 10.889
  - sgt1928 sadiki 1922: patient + staff days vs total days: cells give 133041, printed 133046
  - sgt1928 sadiki 1923: expenditure / patient days vs printed cost per day: cells give 10.78, printed 10.889
  - sgt1928 rabta 1928: expenditure / patient days vs printed cost per day: cells give 16.72, printed 11.811
  - sgt1929 sadiki 1922: patient + staff days vs total days: cells give 133041, printed 133046
  - sgt1929 sadiki 1923: expenditure / patient days vs printed cost per day: cells give 10.78, printed 10.889
  - sgt1929 rabta 1928: expenditure / patient days vs printed cost per day: cells give 16.72, printed 11.811
  - sgt1930 civil 1930: patient + staff days vs total days: cells give 211261, printed 211161
  - sgt1930 sadiki 1922: patient + staff days vs total days: cells give 133041, printed 133046
  - sgt1930 sadiki 1923: expenditure / patient days vs printed cost per day: cells give 10.78, printed 10.889
  - sgt1930 sadiki 1927: expenditure / patient days vs printed cost per day: cells give 22.36, printed 22.861
  - sgt1930 rabta 1928: expenditure / patient days vs printed cost per day: cells give 16.72, printed 11.811
  - sgt1935 civil 1933: expenditure / patient days vs printed cost per day: cells give 31.45, printed 29.76
  - sgt1935 civil 1934: expenditure / patient days vs printed cost per day: cells give 28.7, printed 27.02
  - sgt1935 sadiki 1935: patient + staff days vs total days: cells give 135576, printed 155776

- Overlapping printings: 690 cell comparisons between editions; 11 differences.

| year | cell | edition | printed | latest edition | printed | stored (edition, flag) |
|---|---|---|---|---|---|---|
| 1914 | sadiki/expenditure | sgt1923 | 221088.07 | sgt1925 | 221088.17 | 221088.17 (sgt1925) |
| 1923 | sadiki/cost_per_patient_day | sgt1923 | 10.766 | sgt1930 | 10.889 | 10.889 (sgt1930) |
| 1923 | sadiki/cost_per_patient_day | sgt1924 | 10.766 | sgt1930 | 10.889 | 10.889 (sgt1930) |
| 1924 | civil/total_days | sgt1924 | 65850 | sgt1927 | 166252 | not stored (printed total) |
| 1924 | civil/expenditure | sgt1924 | 1900816.37 | sgt1927 | 1900811.37 | 1900811.37 (sgt1927) |
| 1924 | sadiki/expenditure | sgt1924 | 1102825.72 | sgt1930 | 1102826.62 | 1102826.62 (sgt1930) |
| 1925 | civil/total_days | sgt1925 | 148600 | sgt1929 | 164718 | not stored (printed total) |
| 1925 | civil/cost_per_patient_day | sgt1925 | 21.367 | sgt1929 | 21.36 | 21.36 (sgt1929) |
| 1927 | sadiki/cost_per_patient_day | sgt1927 | 22.361 | sgt1930 | 22.861 | 22.361 (sgt1929, reprint_corrected) |
| 1927 | sadiki/cost_per_patient_day | sgt1928 | 22.361 | sgt1930 | 22.861 | 22.361 (sgt1929, reprint_corrected) |
| 1927 | sadiki/cost_per_patient_day | sgt1929 | 22.361 | sgt1930 | 22.861 | 22.361 (sgt1929, reprint_corrected) |

- Flagged cells: reprint_corrected: 1.

  - sgt1929 1927 sadiki / Hôpital Sadiki / cost_per_patient_day / Prix moyen (de revient) de la journée de malade = 22.361 (reprint_corrected)

## Cross-check with the hospital activity tables

Patient-days and staff-days (fed, not fed) of every printing of the day-cost tables against `health_hospital_civil_activity.csv`, `health_sadiki_activity.csv` and `health_rabta_activity.csv` (the validated "Mouvement de la population" tables): 350 comparisons, 339 equal, 11 different.
  - sadiki 1925 staff_days_not_fed: day-cost table (sgt1925) 18505 vs activity table (sgt1926) 18501
  - sadiki 1925 staff_days_not_fed: day-cost table (sgt1926) 18505 vs activity table (sgt1926) 18501
  - sadiki 1925 staff_days_not_fed: day-cost table (sgt1927) 18505 vs activity table (sgt1926) 18501
  - sadiki 1925 staff_days_not_fed: day-cost table (sgt1928) 18505 vs activity table (sgt1926) 18501
  - sadiki 1925 staff_days_not_fed: day-cost table (sgt1929) 18505 vs activity table (sgt1926) 18501
  - sadiki 1925 staff_days_not_fed: day-cost table (sgt1930) 18505 vs activity table (sgt1926) 18501
  - civil 1927 staff_days_fed: day-cost table (sgt1927) 76147 vs activity table (sgt1928) 76900
  - civil 1927 staff_days_fed: day-cost table (sgt1928) 76147 vs activity table (sgt1928) 76900
  - civil 1927 staff_days_fed: day-cost table (sgt1929) 76147 vs activity table (sgt1928) 76900
  - civil 1927 staff_days_fed: day-cost table (sgt1930) 76147 vs activity table (sgt1928) 76900
  - sadiki 1935 staff_days_not_fed: day-cost table (sgt1935) 35645 vs activity table (sgt1936) 55645

Years of the day-cost tables with no patient-days in the activity tables: civil 1933, rabta 1918, rabta 1919, rabta 1920, rabta 1933, sadiki 1912, sadiki 1913, sadiki 1914, sadiki 1915, sadiki 1916, sadiki 1917, sadiki 1918, sadiki 1919, sadiki 1920, sadiki 1933.


The 11 differences are three cells, each printed identically in every day-cost table: Sadiki 1925 staff days not fed 18.505 (the day-cost total 137.500 needs 18.505; the sgt1926 activity table prints 18.501), civil 1927 staff days fed 76.147 (the day-cost total 225.199 needs 76.147; the sgt1928 activity table prints 76.900), Sadiki 1935 staff days not fed 35.645 (the activity tables print 55.645; neither closes the printed total 155.776). All patient-day counts agree (the 1929 civil patient-days, 110.146, equal the value the activity table took from sgt1929 as `reprint_corrected`; the sgt1930 activity table prints 110.446).
