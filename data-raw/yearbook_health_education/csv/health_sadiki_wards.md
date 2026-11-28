# Hôpital Sadiki : statistiques par service

*Sadiki Hospital: patients by ward.*

Source: *Statistique générale de la Tunisie*, chapter III (health), editions sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1935 (`bpt6k9105653t`): p. 45, f65; sgt1936 (`bpt6k91056547`): p. 35, f46; sgt1939 (`bpt6k9105739w`): p. 36, f42.

Transcriptions: `../transcribed/health_pop_<edition>.txt`, section `@sadiki_wards`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_population.py build`. Per-check output: `health_validation.json`.

Rows: 189. Years: 1935–1939 (3 years: 1935, 1936, 1939).

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

"Statistiques par pavillon" (sgt1935, sgt1936, sgt1939): patients by service (Chirurgie, Yeux, Oto-rhino, Médecine: H/F; Maternité: F), nationality and Payants / Gratuits; `beds` = Nombre de lits organisés per service and sex. The printed TOTAL row is not stored; all column checks pass.

sgt1936: the heading repeats the 1935 heading of sgt1935 ("au cours de l'année 1935 : 4.116", 251 beds) but the cells differ from sgt1935 and their column totals sum to 4.680, the 1936 admissions of the Sadiki population table, so they are stored as 1936. In the same table the French rows are both labelled Payants and the Jewish rows both Gratuits; the second French row is stored as free and the first Jewish row as paying.

## Validation

- Checks against printed totals: 27; passed: 27; failed: 0.

- Flagged cells: none.
