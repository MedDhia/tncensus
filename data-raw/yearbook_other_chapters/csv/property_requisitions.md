# Conservation foncière. Réquisitions d'immatriculation : a) Nationalité des requérants, nombre, contenances et valeurs déclarées

*Land registry: registration requisitions filed, by nationality of the claimant, with declared areas and values, by year.*

Source: *Statistique générale de la Tunisie*, chapter *Propriété immobilière / Tribunal mixte / Propriété foncière*, editions sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1930 (`bpt6k9105652d`): p. 111, f669; sgt1935 (`bpt6k9105653t`): p. 77, f97; sgt1936 (`bpt6k91056547`): p. 56, f67; sgt1939 (`bpt6k9105739w`): p. 56, f62.

Transcriptions: `../transcribed/property_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_property.py build`.

Rows: 160. Years: 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Units: requisitions (`unit` = `count`), hectares (`hectares`), francs (`francs`). Mixed table.

Printed for overlapping year windows: each year (and the opening multi-year period) is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing is compared below. Each single year is printed by every edition from its own year to sgt1930 (up to nine printings, 1910-1930); 1931 and 1932 are printed only inside the opening periods; 1933-1936 are printed by one to three of sgt1935, sgt1936 and sgt1939, 1937-1939 by sgt1939 only; the opening multi-year periods differ between edition groups and are each stored once.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: `requisitions`
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures; empty for the opening multi-year period
- `period`: year, or the opening multi-year period (`1886-1909`, from sgt1935 `1886-1932` etc.) as printed
- `period_fr`: as printed (*De 1886 à 1909*)
- `measure`: `french`, `foreign`, `tunisian` (number of requisitions by nationality of the claimant), `area` (declared area), `value` (declared value)
- `measure_fr`: printed column heading
- `unit`: `count`, `hectares` or `francs`
- `value`: requisitions, hectares or francs
- `flag`: empty, or `total_mismatch` (printed value kept), `derived_from_totals`, `row_realigned`, `not_applicable` (nothing printed)

Periods: up to sgt1930 the table opens with "De 1886 à 1909" followed by single years; sgt1935 opens with 1886-1932, sgt1936 with 1886-1933, sgt1939 with 1886-1934. These opening periods overlap the single years (e.g. 1886-1932 includes 1910-1930): do not sum across periods. The `Nombre` column (= French + foreign + Tunisian) is a check, not stored.

Failed checks: 1924 (every printing sgt1924-sgt1930) Tunisians printed 450 where Nombre 645 and every Totaux need 459 (stored 450, `total_mismatch`); sgt1922 contenances Totaux 1 ha more than the lines; sgt1927 Totaux contenances printed 1.996.340 for lines summing to 1.996.430 (the récapitulation prints 1.996.430); sgt1935 1886-1932 foreign printed 5.134 where Nombre and the Totaux need 4.834 (sgt1936's 1886-1933 4.894 = 4.834 + 60).

Flagged cells: sgt1924 requisitions 1924 / tunisian: printed 450; its line and its column are both 9 off their printed totals (printed value kept); sgt1924 requisitions 1924 / value: every printing of 1924 (sgt1924-sgt1930) prints "17.872 50", the plate missing a digit; 17.872.150 from the Totaux of sgt1924 (304.039.499); sgt1925 requisitions 1924 / tunisian: printed 450; its line and its column are both 9 off their printed totals (printed value kept); sgt1925 requisitions 1924 / value: every printing of 1924 (sgt1924-sgt1930) prints "17.872 50", the plate missing a digit; 17.872.150 from the Totaux of sgt1924 (304.039.499); sgt1926 requisitions 1924 / tunisian: printed 450; its line and its column are both 9 off their printed totals (printed value kept); sgt1926 requisitions 1924 / value: every printing of 1924 (sgt1924-sgt1930) prints "17.872 50", the plate missing a digit; 17.872.150 from the Totaux of sgt1924 (304.039.499); sgt1927 requisitions 1924 / tunisian: printed 450; its line and its column are both 9 off their printed totals (printed value kept); sgt1927 requisitions 1924 / value: every printing of 1924 (sgt1924-sgt1930) prints "17.872 50", the plate missing a digit; 17.872.150 from the Totaux of sgt1924 (304.039.499); sgt1928 requisitions 1924 / tunisian: printed 450; its line and its column are both 9 off their printed totals (printed value kept); sgt1928 requisitions 1924 / value: every printing of 1924 (sgt1924-sgt1930) prints "17.872 50", the plate missing a digit; 17.872.150 from the Totaux of sgt1924 (304.039.499); sgt1929 requisitions 1924 / tunisian: printed 450; its line and its column are both 9 off their printed totals (printed value kept); sgt1929 requisitions 1924 / value: every printing of 1924 (sgt1924-sgt1930) prints "17.872 50", the plate missing a digit; 17.872.150 from the Totaux of sgt1924 (304.039.499); sgt1930 requisitions 1924 / tunisian: printed 450; its line and its column are both 9 off their printed totals (printed value kept); sgt1930 requisitions 1924 / value: every printing of 1924 (sgt1924-sgt1930) prints "17.872 50", the plate missing a digit; 17.872.150 from the Totaux of sgt1924 (304.039.499); sgt1935 requisitions 1886-1932 / french: Français: 126 is printed on the 1886-1932 line and 5.708 on the 1933 line; with the printed values neither line gives its Nombre (5.708 + 60 + 261 = 447 needs 126; 126 + 5.134 + 10.329 = 20.871 needs 5.708), and sgt1936 prints 5.834 = 5.708 + 126 for 1886-1933; sgt1935 requisitions 1886-1932 / foreign: printed 5134; its line and its column are both -300 off their printed totals (printed value kept); sgt1935 requisitions 1933 / french: see 1886-1932.

Survey of the whole chapter in every edition: `property_survey.md`.

Overlap comparison: every printing of sgt1922-sgt1930 (and of sgt1935, sgt1936) was read independently on its own page image. The single years 1910-1930 are printed from the same standing type in every edition (the 1924 value "17.872 50" and the Tunisians 450 recur unchanged), so the printings agree cell for cell; the only differences between editions lie in the opening multi-year periods, which are distinct periods (1886-1909, 1886-1932, 1886-1933, 1886-1934) and are stored separately.

## Validation

- Checks against printed totals and identities: 260; passed: 242; failed: 18.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.86 (f110) requisitions area: lines vs Totaux: cells give 1756361, printed 1756362 (difference 1)
  - sgt1924 p.94 (f1084) requisitions 1924: number = french + foreign + tunisian: cells give 636, printed 645 (difference 9)
  - sgt1924 p.94 (f1084) requisitions tunisian: lines vs Totaux: cells give 6728, printed 6737 (difference 9)
  - sgt1925 p.96 (f120) requisitions 1924: number = french + foreign + tunisian: cells give 636, printed 645 (difference 9)
  - sgt1925 p.96 (f120) requisitions tunisian: lines vs Totaux: cells give 7019, printed 7028 (difference 9)
  - sgt1926 p.107 (f671) requisitions 1924: number = french + foreign + tunisian: cells give 636, printed 645 (difference 9)
  - sgt1926 p.107 (f671) requisitions tunisian: lines vs Totaux: cells give 7338, printed 7347 (difference 9)
  - sgt1927 p.105 (f133) requisitions 1924: number = french + foreign + tunisian: cells give 636, printed 645 (difference 9)
  - sgt1927 p.105 (f133) requisitions tunisian: lines vs Totaux: cells give 7886, printed 7895 (difference 9)
  - sgt1927 p.105 (f133) requisitions area: lines vs Totaux: cells give 1996430, printed 1996340 (difference -90)
  - sgt1928 p.105 (f657) requisitions 1924: number = french + foreign + tunisian: cells give 636, printed 645 (difference 9)
  - sgt1928 p.105 (f657) requisitions tunisian: lines vs Totaux: cells give 8425, printed 8434 (difference 9)
  - sgt1929 p.107 (f135) requisitions 1924: number = french + foreign + tunisian: cells give 636, printed 645 (difference 9)
  - sgt1929 p.107 (f135) requisitions tunisian: lines vs Totaux: cells give 8954, printed 8963 (difference 9)
  - sgt1930 p.111 (f669) requisitions 1924: number = french + foreign + tunisian: cells give 636, printed 645 (difference 9)
  - sgt1930 p.111 (f669) requisitions tunisian: lines vs Totaux: cells give 9490, printed 9499 (difference 9)
  - sgt1935 p.77 (f97) requisitions 1886-1932: number = french + foreign + tunisian: cells give 21171, printed 20871 (difference -300)
  - sgt1935 p.77 (f97) requisitions foreign: lines vs Totaux: cells give 5274, printed 4974 (difference -300)

- Overlapping printings: 720 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: derived_from_totals: 1, row_realigned: 2, total_mismatch: 2.

  - sgt1935 p.77 None 1886-1932 / french / count = 5708 (row_realigned)
  - sgt1935 p.77 None 1886-1932 / foreign / count = 5134 (total_mismatch)
  - sgt1930 p.111 1924 1924 / tunisian / count = 450 (total_mismatch)
  - sgt1930 p.111 1924 1924 / value / francs = 17872150 (derived_from_totals)
  - sgt1935 p.77 1933 1933 / french / count = 126 (row_realigned)

## Image versus OCR

- Read cell by cell on the page images (12 printings): sgt1922 f110, sgt1923 f594, sgt1924 f1084, sgt1925 f120, sgt1926 f671, sgt1927 f133, sgt1928 f657, sgt1929 f135, sgt1930 f669, sgt1935 f97, sgt1936 f67, sgt1939 f62.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
