# Hôpital civil français de Tunis : statistiques par pavillon

*French Civil Hospital of Tunis: patients by ward, sex, nationality and payment status.*

Source: *Statistique générale de la Tunisie*, chapter III (health), editions sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1935 (`bpt6k9105653t`): p. 43, f63; sgt1936 (`bpt6k91056547`): p. 33, f44; sgt1939 (`bpt6k9105739w`): p. 34, f40.

Transcriptions: `../transcribed/health_pop_<edition>.txt`, section `@civil_wards`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_population.py build`. Per-check output: `health_validation.json`.

Rows: 235. Years: 1935–1939 (3 years: 1935, 1936, 1939).

Printed once per edition, for the edition's own year; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to
- `measure`: what is counted (see below)
- `ward`: ward / service (English code)
- `ward_fr`: as printed
- `sex`: `male`, `female`, or `total` / empty where not split
- `nationality`: `french`, `tunisian_muslim`, `tunisian_jewish`, `italian`, `anglo_maltese`, `other`; `european` where the table groups the other Europeans; `total` for a printed all-nationality rate
- `nationality_fr`: column or row heading (French)
- `payment`: `paying` (Payants) or `free` (Gratuits)
- `payment_fr`: as printed
- `value`: count (integer), except where the notes say otherwise; printed » = 0
- `flag`: empty, or `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (row totals, TOTAUX lines, nationality brackets) and the printed "différence en plus / en moins" columns are not stored; they were used for validation.

"Statistiques par pavillon" (sgt1935, sgt1936, sgt1939): patients by ward (Médecine générale, Chirurgie, Maladies contagieuses, Nerveux: men/women; Maternité: not split, `sex` empty), by nationality (Français, Musulmans, Israélites, Européens = other Europeans; sgt1939 "Tunisiens musulmans", "Tunisiens israélites", "Étrangers européens") and Payants / Gratuits. `measure` = `patients`; `beds` (Nombre de lits organisés, per ward, printed in the TOTAL row); `births` (sgt1939 only: "Nombre de naissances" in the maternity, printed in the Gratuits rows; these births are included in the Gratuits row totals and in the 7.530 admissions). Row totals, nationality brackets and the TOTAL row are not stored.

Identified misprints (printed values kept, `total_mismatch`): sgt1935 French paying, médecine générale women 39 (99 closes both the row total 922 and the column total 791); sgt1936 Jewish free, médecine générale women 22 (222 closes the row total 1.404 and the column total 766). sgt1935 also has row totals that disagree with their cells while every column total agrees (French free 2.876 vs 2.861; Jewish paying 105 vs 108; Jewish free 1.120 vs 1.132); no cell can be singled out.

## Validation

- Checks against printed totals: 70; passed: 63; failed: 7.

Failed checks (printed values kept; every one was re-read on the page image and the printed figures are as transcribed; see the commentary above for the cells involved):

  - sgt1935 civil_wards french paying: cells vs row total: cells give 862, printed 922
  - sgt1935 civil_wards french free: cells vs row total: cells give 2876, printed 2861
  - sgt1935 civil_wards tunisian_jewish paying: cells vs row total: cells give 105, printed 108
  - sgt1935 civil_wards tunisian_jewish free: cells vs row total: cells give 1120, printed 1132
  - sgt1935 civil_wards column medg_f: rows vs TOTAL: cells give 731, printed 791
  - sgt1936 civil_wards tunisian_jewish free: cells vs row total: cells give 1204, printed 1404
  - sgt1936 civil_wards column medg_f: rows vs TOTAL: cells give 566, printed 766

- Flagged cells: total_mismatch: 2.

  - sgt1935 1935 patients / general_medicine / Médecine générale / female / french / Français / paying / Payants = 39 (total_mismatch)
  - sgt1936 1936 patients / general_medicine / Médecine générale / female / tunisian_jewish / Israélites tunisiens / free / Gratuits = 22 (total_mismatch)
