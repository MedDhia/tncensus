# Industrie minière. Mines exploitées et valeur globale des produits exportés

*Mining: number of mines worked and value of the ore exported (fob Tunis).*

Source: *Statistique générale de la Tunisie*, chapter *Travaux publics*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 157, f181; sgt1923 (`bpt6k9105649x`): p. 169, f671; sgt1924 (`bpt6k9105649x`): p. 177, f1167; sgt1925 (`bpt6k9105650k`): p. 183, f207; sgt1926 (`bpt6k9105650k`): p. 199, f763; sgt1927 (`bpt6k91056510`): p. 197, f225; sgt1928 (`bpt6k91056510`): p. 197, f749; sgt1929 (`bpt6k9105652d`): p. 199, f227; sgt1930 (`bpt6k9105652d`): p. 203, f761; sgt1935 (`bpt6k9105653t`): p. 103, f123; sgt1936 (`bpt6k91056547`): p. 79, f90; sgt1939 (`bpt6k9105739w`): p. 84, f90.

Transcriptions: `../transcribed/publicworks_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_publicworks.py build`.

Rows: 54. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Units: count and francs; suggested value_type: mixed.

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

Printed in every edition. The value of the latest year is not the value of production of the *Renseignements généraux sur les mines* (it equals it only in sgt1922-sgt1923 and sgt1930).

Survey of the whole chapter in every edition: `publicworks_survey.md`.

## Validation

- Checks against printed totals and identities: 0; passed: 0; failed: 0.

- Overlapping printings: 186 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (12 printings): sgt1922 f181, sgt1923 f671, sgt1924 f1167, sgt1925 f207, sgt1926 f763, sgt1927 f225, sgt1928 f749, sgt1929 f227, sgt1930 f761, sgt1935 f123, sgt1936 f90, sgt1939 f90.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
