# Mouvements des mandats-poste : a) Mandats-poste envoyés de Tunisie en Italie

*Money orders sent from Tunisia to Italy, by month.*

Source: *Statistique générale de la Tunisie*, chapter *Postes - Télégraphes - Téléphones*, editions sgt1922, sgt1923, sgt1924. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 134, f158; sgt1923 (`bpt6k9105649x`): p. 140, f642; sgt1924 (`bpt6k9105649x`): p. 142, f1132.

Transcriptions: `../transcribed/posts_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_posts.py build`.

Rows: 168. Years: 1918, 1919, 1920, 1921, 1922, 1923, 1924.

Units: number of money orders (`count`) and amount in francs (`francs`, centimes kept); suggested value_type: mixed.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing of the same cell, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`): the latest edition printing that year
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (network: situation at 31 December)
- `month`: month number 1-12
- `month_fr`: as printed
- `measure`: `number` (Nombre) or `amount` (Montant)
- `measure_fr`: as printed
- `unit`: `count`, `km` (kilometres) or `francs` (centimes kept as decimals)
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible` (NA, cut by the binding or broken type), `not_applicable` (nothing printed, or » in a line not yet collected; NA), `row_realigned` (printed in the wrong column or line, stored on the year / item it belongs to), `reprint_corrected` (kept from an earlier printing), `derived_from_totals`

Printed only in sgt1922 (1918-1922), sgt1923 (1919-1923; title "1913-1923") and sgt1924 (1920-1924), with a Totaux line (checks only). Amounts in francs and centimes (1919 printed in whole francs).

Failed checks, grouped (printed values kept). A failure that recurs identically in several editions was read independently on each printing, so it is the printed figure; every failure printed by one edition only was re-read on a zoomed native-resolution crop: mo_italy 1918.amt Totaux: cells 684845.86, printed 684745.86 (in sgt1922); mo_italy 1919.amt Totaux: cells 821806, printed 821816 (in sgt1922, sgt1923); mo_italy 1920.amt Totaux: cells 798611.50, printed 798611.44 (in sgt1922, sgt1923, sgt1924).

Survey of the whole chapter in every edition: `posts_survey.md`.

## Validation

- Checks against printed totals and identities: 30; passed: 24; failed: 6.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.134 (f158) mo_italy 1918.amt: Totaux = sum of the lines: cells give 684845.86, printed 684745.86 (difference -100.00)
  - sgt1922 p.134 (f158) mo_italy 1919.amt: Totaux = sum of the lines: cells give 821806, printed 821816 (difference 10)
  - sgt1922 p.134 (f158) mo_italy 1920.amt: Totaux = sum of the lines: cells give 798611.50, printed 798611.44 (difference -0.06)
  - sgt1923 p.140 (f642) mo_italy 1919.amt: Totaux = sum of the lines: cells give 821806, printed 821816 (difference 10)
  - sgt1923 p.140 (f642) mo_italy 1920.amt: Totaux = sum of the lines: cells give 798611.50, printed 798611.44 (difference -0.06)
  - sgt1924 p.142 (f1132) mo_italy 1920.amt: Totaux = sum of the lines: cells give 798611.50, printed 798611.44 (difference -0.06)

- Overlapping printings: 192 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (3 printings): sgt1922 f158, sgt1923 f642, sgt1924 f1132.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
