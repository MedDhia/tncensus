# Coopérative centrale des agriculteurs de Tunisie ; Coopérative de motoculture de Tunisie

*Central cooperative of farmers and motor-cultivation cooperative of Tunisia: paid-up capital, State advances and goods bought in common and delivered, by year (1921-1939).*

Source: *Statistique générale de la Tunisie*, chapter *Institutions économiques et sociales / Mutualité agricole*, editions sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1930 (`bpt6k9105652d`): p. 474, f1032; sgt1935 (`bpt6k9105653t`): p. 291, f311; sgt1936 (`bpt6k91056547`): p. 173, f184; sgt1939 (`bpt6k9105739w`): p. 153, f159.

Transcriptions: `../transcribed/mutuality_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_mutuality.py build`.

Rows: 133. Years: 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Units: francs; suggested value_type: francs.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (rule 4 tables: the latest edition printing that year)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `institution_fr`: named institution as printed (Coopérative centrale des agriculteurs de Tunisie; Coopérative de motoculture de Tunisie)
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible`, `not_applicable`, `total_mismatch`, `ocr_corrected`

Printed sgt1930-sgt1939 (sgt1930: 1921-1930; sgt1935: 1925-1935; sgt1936: 1926-1936; sgt1939: 1929-1939). Two named institutions (`institution_fr` as printed). Situation at 31 December. sgt1939 prints *néant* for the motoculture State advances 1937-1939 (stored 0). No totals printed.

Survey of the whole chapter in every edition: `mutuality_survey.md`.

## Validation

- Checks against printed totals and identities: 0; passed: 0; failed: 0.

- Overlapping printings: 168 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (8 printings): sgt1930 f1032, sgt1930 f1032, sgt1935 f311, sgt1935 f311, sgt1936 f184, sgt1936 f184, sgt1939 f159, sgt1939 f159.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
