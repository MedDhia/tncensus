# Lotissements urbains, industriels ou d'estivage

*Urban, industrial and summer-residence lotissements: by year, area and number of lots.*

Source: *Statistique générale de la Tunisie*, chapter *Colonisation*, editions sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1924 (`bpt6k9105649x`): p. 448, f1438, p. 449, f1439; sgt1925 (`bpt6k9105650k`): p. 482, f506, p. 483, f507; sgt1926 (`bpt6k9105650k`): p. 454, f1018, p. 455, f1019; sgt1927 (`bpt6k91056510`): p. 454, f482, p. 455, f483; sgt1928 (`bpt6k91056510`): p. 458, f1010, p. 459, f1011; sgt1929 (`bpt6k9105652d`): p. 460, f488, p. 461, f489; sgt1930 (`bpt6k9105652d`): p. 466, f1024, p. 467, f1025; sgt1935 (`bpt6k9105653t`): p. 282, f302, p. 283, f303.

Transcriptions: `../transcribed/colonisation_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_colonisation.py build`.

Rows: 368. Years: 1914, 1915, 1916, 1917, 1919, 1920, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935.

Units: hectares and number of lots (`unit`); suggested value_type: mixed.

Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept (`census` = edition); the figures are the state at the edition date and are revised between editions.

## Columns

- `census`: edition the value is taken from (rule 4 tables: the latest edition printing that year)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `scheme`: `installation` (ventes avec obligation d'installation personnelle)
- `scheme_fr`: printed table title
- `property_fr`: property / lotissement as printed (footnote calls kept)
- `situation_fr`: printed situation
- `controle_civil`: contrôle civil as printed
- `observation_fr`: printed observation for the line (a brace covering several lines is repeated on each)
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible`, `not_applicable`, `total_mismatch`, `ocr_corrected`

Printed sgt1924-sgt1935 as table c) of the chapter (ten-year window; sgt1922-sgt1923 list these lotissements in the installation table). Lotissements printed » (suppressed and replaced) are kept with value 0 and their observation. sgt1928 prints its 1928 areas to the centiare (stored with four decimals). The TOTAUX line is checked.

Every failed check below was re-read on a native-resolution crop: the printed values are kept. sgt1935 prints TOTAUX 160,18 ha / 1.344 lots for lines summing to 130,90 / 1.143 (the lines agree with sgt1930 for 1926-1930; the printed total matches no subset).

Survey of the whole chapter in every edition: `colonisation_survey.md`.

## Validation

- Checks against printed totals and identities: 16; passed: 14; failed: 2.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1935 p.282 (f302) urban area: Totaux = report + lines: cells give 130.90, printed 160.18 (difference 29.28)
  - sgt1935 p.282 (f302) urban lots: Totaux = report + lines: cells give 1143, printed 1344 (difference 201)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (8 printings): sgt1924 f1438, sgt1925 f506, sgt1926 f1018, sgt1927 f482, sgt1928 f1010, sgt1929 f488, sgt1930 f1024, sgt1935 f302.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
