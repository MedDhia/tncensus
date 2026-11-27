# Phosphates de chaux. b) Renseignements généraux sur les exploitations de phosphates

*Calcium phosphates: workings on state and private land, workers, working days, production, value.*

Source: *Statistique générale de la Tunisie*, chapter *Travaux publics*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 158, f182; sgt1923 (`bpt6k9105649x`): p. 170, f672; sgt1924 (`bpt6k9105649x`): p. 178, f1168; sgt1925 (`bpt6k9105650k`): p. 184, f208; sgt1926 (`bpt6k9105650k`): p. 200, f764; sgt1927 (`bpt6k91056510`): p. 198, f226; sgt1928 (`bpt6k91056510`): p. 198, f750; sgt1929 (`bpt6k9105652d`): p. 200, f228; sgt1930 (`bpt6k9105652d`): p. 204, f762; sgt1935 (`bpt6k9105653t`): p. 104, f124; sgt1936 (`bpt6k91056547`): p. 80, f91; sgt1939 (`bpt6k9105739w`): p. 85, f91.

Transcriptions: `../transcribed/publicworks_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_publicworks.py build`.

Rows: 132. Years: 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Units: count, tonnes, francs; suggested value_type: mixed.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition; an aligned printing is preferred to a realigned one); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from: the latest edition printing that year (rule 5 tables: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible`, `not_applicable` (nothing printed), `row_realigned` (printed on the wrong line, stored on the year it belongs to), `total_mismatch`

Printed for five years in every edition.

Survey of the whole chapter in every edition: `publicworks_survey.md`.

## Validation

- Checks against printed totals and identities: 0; passed: 0; failed: 0.

- Overlapping printings: 228 cell comparisons with other editions printing the same cell; 2 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1935 / workings_state_land | sgt1935 | 0 | sgt1939 | 7 |
| 1935 / workings_private_land | sgt1935 | 0 | sgt1939 | 1 |

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (12 printings): sgt1922 f182, sgt1923 f672, sgt1924 f1168, sgt1925 f208, sgt1926 f764, sgt1927 f226, sgt1928 f750, sgt1929 f228, sgt1930 f762, sgt1935 f124, sgt1936 f91, sgt1939 f91.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
