# Hôpital de la Rabta : entrées par mois et par nationalité

*Rabta hospital: admissions by month and nationality.*

Source: *Statistique générale de la Tunisie*, chapter III (health), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1922 (`bpt6k9105649x`): p. 52, f76; sgt1923 (`bpt6k9105649x`): p. 58, f560; sgt1924 (`bpt6k9105649x`): p. 61, f1051; sgt1925 (`bpt6k9105650k`): p. 61, f85; sgt1926 (`bpt6k9105650k`): p. 70, f634; sgt1927 (`bpt6k91056510`): p. 68, f96; sgt1928 (`bpt6k91056510`): p. 68, f620; sgt1929 (`bpt6k9105652d`): p. 70, f98; sgt1930 (`bpt6k9105652d`): p. 74, f632; sgt1935 (`bpt6k9105653t`): p. 47, f67.

Transcriptions: `../transcribed/health_pop_<edition>.txt`, section `@rabta_months`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_population.py build`. Per-check output: `health_validation.json`.

Rows: 726. Years: 1922–1935 (10 years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935).

Printed once per edition, for the edition's own year; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to
- `month`: `january` … `december`; `carried_over_1_january` for patients carried over (Rabta 1935)
- `month_fr`: as printed
- `nationality`: `french`, `tunisian_muslim`, `tunisian_jewish`, `italian`, `anglo_maltese`, `other`; `european` where the table groups the other Europeans; `total` for a printed all-nationality rate
- `nationality_fr`: column or row heading (French)
- `value`: count (integer), except where the notes say otherwise; printed » = 0
- `flag`: empty, or `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (row totals, TOTAUX lines, nationality brackets) and the printed "différence en plus / en moins" columns are not stored; they were used for validation.

"Récapitulation des personnes hospitalisées par mois et par nationalité" (sgt1922–sgt1930, sgt1935; not printed in sgt1936 and sgt1939). sgt1935 adds a first row "Reports au 1er janvier 1935" (`carried_over_1_january`), which the printed TOTAUX include. sgt1930: May row total 52 against cells 62; the TOTAL column (1.126) agrees with 62.

## Validation

- Checks against printed totals: 201; passed: 199; failed: 2.

Failed checks (printed values kept; every one was re-read on the page image and the printed figures are as transcribed; see the commentary above for the cells involved):

  - sgt1930 rabta_months row Mai: cells vs row total: cells give 62, printed 52
  - sgt1930 rabta_months column total: rows vs TOTAUX: cells give 1116, printed 1126

- Flagged cells: none.
