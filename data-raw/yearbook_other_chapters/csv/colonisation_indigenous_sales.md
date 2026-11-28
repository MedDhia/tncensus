# Ventes définitives consenties aux attributaires ayant rempli leurs obligations de mise en valeur

*Definitive sales to Tunisian allottees who fulfilled their development obligations, by year.*

Source: *Statistique générale de la Tunisie*, chapter *Colonisation*, editions sgt1930, sgt1935, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1930 (`bpt6k9105652d`): p. 470, f1028; sgt1935 (`bpt6k9105653t`): p. 286, f306; sgt1939 (`bpt6k9105739w`): p. 149, f155.

Transcriptions: `../transcribed/colonisation_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_colonisation.py build`.

Rows: 57. Years: 1920, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Units: count and hectares (`unit`); suggested value_type: mixed.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (rule 4 tables: the latest edition printing that year)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `year_label`: year as printed (brackets such as `1920-21` kept); `year` = its first year
- `item`: `cumulative` (state since 1920 at the edition date), `allotments_of_year`, `definitive_sales`
- `item_fr`: printed line or table heading
- `observation_fr`: printed observation for the line (a brace covering several lines is repeated on each)
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible`, `not_applicable`, `total_mismatch`, `ocr_corrected`

Printed sgt1930-sgt1939. The first line groups the early years differently in each edition (sgt1930: 1920 à 1923, 1924, 1925 separately; sgt1935: 1920 à 1925; sgt1936-sgt1939: 1920 à 1926); each printed grouping is kept as its own `year_label` from the latest edition printing it (`year` = its first year), so the groupings overlap: do not add the 1920-1926 rows across labels. The TOTAUX line of every printing is checked. Every other printing of the same label is compared below.

Every failed check below was re-read on a native-resolution crop: the printed values are kept. sgt1935 and sgt1936 print the ventes proposées total 4 above the sum of their lines (2.283 for 2.279; 2.452 for 2.448); sgt1939's area total 35.175,31 is 0,10 below its lines.

Survey of the whole chapter in every edition: `colonisation_survey.md`.

## Validation

- Checks against printed totals and identities: 12; passed: 9; failed: 3.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1935 p.286 (f306) sales proposed: Totaux = sum of the lines: cells give 2279, printed 2283 (difference 4)
  - sgt1936 p.169 (f180) sales proposed: Totaux = sum of the lines: cells give 2448, printed 2452 (difference 4)
  - sgt1939 p.149 (f155) sales area: Totaux = sum of the lines: cells give 35175.41, printed 35175.31 (difference -0.10)

- Overlapping printings: 75 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (4 printings): sgt1930 f1028, sgt1935 f306, sgt1936 f180, sgt1939 f155.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
