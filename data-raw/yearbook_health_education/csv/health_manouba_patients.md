# Hôpital psychiatrique de la Manouba

*Manouba mental hospital: beds and patients.*

Source: *Statistique générale de la Tunisie*, chapter III (health), editions sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1935 (`bpt6k9105653t`): p. 48, f68; sgt1936 (`bpt6k91056547`): p. 37, f48; sgt1939 (`bpt6k9105739w`): p. 38, f44.

Transcriptions: `../transcribed/health_pop_<edition>.txt`, section `@manouba`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_population.py build`. Per-check output: `health_validation.json`.

Rows: 52. Years: 1935–1939 (3 years: 1935, 1936, 1939).

Printed once per edition, for the edition's own year; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to
- `measure`: what is counted (see below)
- `sex`: `male`, `female`, or `total` / empty where not split
- `nationality`: `french`, `tunisian_muslim`, `tunisian_jewish`, `italian`, `anglo_maltese`, `other`; `european` where the table groups the other Europeans; `total` for a printed all-nationality rate
- `nationality_fr`: column or row heading (French)
- `payment`: `paying` (Payants) or `free` (Gratuits)
- `payment_fr`: as printed
- `value`: count (integer), except where the notes say otherwise; printed » = 0
- `flag`: empty, or `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (row totals, TOTAUX lines, nationality brackets) and the printed "différence en plus / en moins" columns are not stored; they were used for validation.

Hôpital pour les maladies mentales de la Manouba, "Nombre de malades hospitalisés au cours de l'année" (sgt1935, sgt1936, sgt1939). sgt1935–sgt1936: patients by nationality × Payants/Gratuits × sex, and beds (Nombre de lits organisés) by sex, printed in the total row. sgt1939: paying / free / total by sex and nationality, no beds. `nationality` = `european` for "Européens". Totals not stored. sgt1936: women's cells sum to 67 against 70 printed.

## Validation

- Checks against printed totals: 43; passed: 42; failed: 1.

Failed checks (printed values kept; every one was re-read on the page image and the printed figures are as transcribed; see the commentary above for the cells involved):

  - sgt1936 manouba column patients_f: rows vs TOTAL: cells give 67, printed 70

- Flagged cells: none.
