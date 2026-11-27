# Routes et pistes. Longueurs construites et dépenses faites cumulées

*Roads and tracks: cumulative length built and cumulative expenditure.*

Source: *Statistique générale de la Tunisie*, chapter *Travaux publics*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 156, f180; sgt1923 (`bpt6k9105649x`): p. 168, f670; sgt1924 (`bpt6k9105649x`): p. 176, f1166; sgt1925 (`bpt6k9105650k`): p. 182, f206; sgt1926 (`bpt6k9105650k`): p. 198, f762; sgt1927 (`bpt6k91056510`): p. 196, f224; sgt1928 (`bpt6k91056510`): p. 196, f748; sgt1929 (`bpt6k9105652d`): p. 198, f226; sgt1930 (`bpt6k9105652d`): p. 202, f760; sgt1935 (`bpt6k9105653t`): p. 102, f122.

Transcriptions: `../transcribed/publicworks_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_publicworks.py build`.

Rows: 58. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935.

Units: kilometres (`unit` = `km`) and francs (`francs`); suggested value_type: mixed.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition; an aligned printing is preferred to a realigned one); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from: the latest edition printing that year (rule 5 tables: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `work`: work code (English)
- `work_fr`: printed heading
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible`, `not_applicable` (nothing printed), `row_realigned` (printed on the wrong line, stored on the year it belongs to), `total_mismatch`

sgt1922-sgt1924 title the table *Routes et pistes* and print three columns (routes: longueurs cumulées construites, kilomètres; dépenses cumulées, francs; pistes: dépenses cumulées, francs); from sgt1925 the title is *Routes* and the pistes column is dropped. The figures are cumulative. Not printed in sgt1935, sgt1936, sgt1939.

sgt1929 prints for 1929 5.525 km and 106.497.742 francs, the figures that sgt1930 prints for 1930; sgt1930 prints 1929 as 5.475 km and 102.316.240 francs (kept, latest edition).

Survey of the whole chapter in every edition: `publicworks_survey.md`.

## Validation

- Checks against printed totals and identities: 207; passed: 207; failed: 0.

- Overlapping printings: 172 cell comparisons with other editions printing the same cell; 2 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1929 / roads / length_built_cumulative | sgt1929 | 5525 | sgt1935 | 5475 |
| 1929 / roads / expenditure_cumulative | sgt1929 | 106497742 | sgt1935 | 102316240 |

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (10 printings): sgt1922 f180, sgt1923 f670, sgt1924 f1166, sgt1925 f206, sgt1926 f762, sgt1927 f224, sgt1928 f748, sgt1929 f226, sgt1930 f760, sgt1935 f122.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
