# Conservation foncière. Réquisitions d'immatriculation : b) Répartition d'après les valeurs déclarées

*Land registry: registration requisitions by bracket of declared value, by year.*

Source: *Statistique générale de la Tunisie*, chapter *Propriété immobilière / Tribunal mixte / Propriété foncière*, editions sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1930 (`bpt6k9105652d`): p. 111, f669; sgt1935 (`bpt6k9105653t`): p. 77, f97; sgt1936 (`bpt6k91056547`): p. 56, f67; sgt1939 (`bpt6k9105739w`): p. 56, f62.

Transcriptions: `../transcribed/property_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_property.py build`.

Rows: 128. Years: 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Unit: number of requisitions.

Printed for overlapping year windows: each year (and the opening multi-year period) is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing is compared below. Each single year is printed by every edition from its own year to sgt1930 (up to nine printings, 1910-1930); 1931 and 1932 are printed only inside the opening periods; 1933-1936 are printed by one to three of sgt1935, sgt1936 and sgt1939, 1937-1939 by sgt1939 only; the opening multi-year periods differ between edition groups and are each stored once.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: `value_brackets`
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures; empty for the opening multi-year period
- `period`: year, or the opening multi-year period as printed
- `period_fr`: as printed
- `measure`: `le_3000`, `3001_12000`, `12001_60000`, `ge_60001` (declared value, francs)
- `measure_fr`: printed column heading
- `unit`: `count`
- `value`: number of requisitions
- `flag`: empty, or `total_mismatch` (printed value kept), `derived_from_totals`, `row_realigned`, `not_applicable` (nothing printed)

Periods as in property_requisitions (overlapping opening periods). The TOTAUX column is a check, also against property_requisitions' Nombre.

Failed checks: sgt1926 Totaux "3.001 à 12.000" printed 6.235 for lines 6.253 and TOTAUX 15.600 for 16.500 (clear on the crop).

Survey of the whole chapter in every edition: `property_survey.md`.

Overlap comparison: every printing of sgt1922-sgt1930 (and of sgt1935, sgt1936) was read independently on its own page image. The single years 1910-1930 are printed from the same standing type in every edition (the 1924 value "17.872 50" and the Tunisians 450 recur unchanged), so the printings agree cell for cell; the only differences between editions lie in the opening multi-year periods, which are distinct periods (1886-1909, 1886-1932, 1886-1933, 1886-1934) and are stored separately.

## Validation

- Checks against printed totals and identities: 424; passed: 421; failed: 3.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1926 p.107 (f671) value_brackets Totaux: total = le_3000 + 3001_12000 + 12001_60000 + ge_60001: cells give 16482, printed 15600 (difference -882)
  - sgt1926 p.107 (f671) value_brackets 3001_12000: lines vs Totaux: cells give 6253, printed 6235 (difference -18)
  - sgt1926 p.107 (f671) value_brackets total: lines vs Totaux: cells give 16500, printed 15600 (difference -900)

- Overlapping printings: 576 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (12 printings): sgt1922 f110, sgt1923 f594, sgt1924 f1084, sgt1925 f120, sgt1926 f671, sgt1927 f133, sgt1928 f657, sgt1929 f135, sgt1930 f669, sgt1935 f97, sgt1936 f67, sgt1939 f62.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
