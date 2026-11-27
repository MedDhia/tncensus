# Industrie minière. Mines : a) Permis de recherches demandés, délivrés et en cours

*Mining: prospecting permits requested, granted and current.*

Source: *Statistique générale de la Tunisie*, chapter *Travaux publics*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 157, f181; sgt1923 (`bpt6k9105649x`): p. 169, f671; sgt1924 (`bpt6k9105649x`): p. 177, f1167; sgt1925 (`bpt6k9105650k`): p. 183, f207; sgt1926 (`bpt6k9105650k`): p. 199, f763; sgt1927 (`bpt6k91056510`): p. 197, f225; sgt1928 (`bpt6k91056510`): p. 197, f749; sgt1929 (`bpt6k9105652d`): p. 198, f226; sgt1930 (`bpt6k9105652d`): p. 202, f760.

Transcriptions: `../transcribed/publicworks_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_publicworks.py build`.

Rows: 54. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930.

Unit: number of permits; value_type: count.

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

Printed sgt1922-sgt1930 (not in sgt1935, sgt1936, sgt1939). No totals. sgt1924 prints the 1924 permits en cours "6.2" with a broken middle digit, read 652; every later edition prints 652.

Survey of the whole chapter in every edition: `publicworks_survey.md`.

## Validation

- Checks against printed totals and identities: 0; passed: 0; failed: 0.

- Overlapping printings: 216 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (9 printings): sgt1922 f181, sgt1923 f671, sgt1924 f1167, sgt1925 f207, sgt1926 f763, sgt1927 f225, sgt1928 f749, sgt1929 f226, sgt1930 f760.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
