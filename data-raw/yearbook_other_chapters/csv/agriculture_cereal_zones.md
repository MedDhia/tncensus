# Principales cultures : rendement et répartition. a) Céréales (blé dur, tendre, orge, avoine) - Rendement par zone (Nord, Centre et Sud)

*Cereals (durum and soft wheat, barley, oats): area, production and yield per hectare by zone.*

Source: *Statistique générale de la Tunisie*, chapter *Agriculture*, editions sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1926 (`bpt6k9105650k`): p. 248, f812; sgt1927 (`bpt6k91056510`): p. 240, f268; sgt1928 (`bpt6k91056510`): p. 240, f792; sgt1929 (`bpt6k9105652d`): p. 242, f270; sgt1930 (`bpt6k9105652d`): p. 246, f804, p. 247, f805; sgt1935 (`bpt6k9105653t`): p. 125, f145; sgt1936 (`bpt6k91056547`): p. 95, f106; sgt1939 (`bpt6k9105739w`): p. 99, f105.

Transcriptions: `../transcribed/agriculture_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_agriculture.py build`.

Rows: 504. Years: 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Units: hectares, quintals, quintals per hectare (`unit`); value_type: mixed.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (rule 4 series: the latest edition printing that year; rule 5 tables: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (crop year = calendar year of the harvest, as printed; rule 5 tables: edition year)
- `zone`: `tunisia` (whole country), or the zone of sgt1925's cereal tables (`north`, `centre_south`)
- `zone_fr`: printed zone heading
- `crop`: crop code (English)
- `crop_fr`: printed line heading
- `measure`: measure code (English)
- `measure_fr`: printed heading of the measure
- `unit`: unit of `value`, as printed (never converted)
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible`, `total_mismatch` (cell identified as the faulty one of a failed check, printed value kept), `derived_from_totals`, `not_applicable`

Printed from sgt1926 (ten years to sgt1930, three years from sgt1935), complementing the whole-country cereal lines of agriculture_crops (which have no yields from sgt1926). Zones as printed: Nord, and Centre et Sud. sgt1925 printed a comparable split under other headings (Tunisie septentrionale et Hauts plateaux / Tunisie centrale et méridionale) inside the cultures diverses table: it is kept in agriculture_crops (`zone`), not compared here. The printed averages are checks only (mean of the years, to 0.2 %); yields are checked against production / surface (to 5 %).

Later editions revise the latest years (1927-1928 productions, listed below); each year is stored from the latest edition printing it.

Every failed check below was re-read on a zoomed native-resolution crop: they are printed inconsistencies (printed values kept). Yield failures recur in every printing of the same year (e.g. barley Nord 1921 7,8; durum Centre et Sud 1923 printed 1,2 to sgt1928 and 2 from sgt1929; oats Centre et Sud 1922 0,1 then 1): printed figures. sgt1930 prints the 1930 orge Nord production 350.000 (zoomed crop; flag `total_mismatch`): its yield 5 and its two averages need 850.000. sgt1936 prints the 1935 orge Nord surface 450.000, against 150.000 in sgt1935 (whose yield 6 fits): the sgt1935 value is kept (`reprint_corrected`). sgt1939 1939 blé tendre Centre et Sud: surface 17.100 (confirmed by the printed 1935-1939 average) for a printed yield 8,5 (5,6 computed). Averages that fail are printed averages not fitting the printed years (several by round amounts: sgt1927 blé tendre Nord 1918-1922 474.032 for 47.403).

Survey of the whole chapter in every edition: `agriculture_survey.md`.

## Validation

- Checks against printed totals and identities: 705; passed: 645; failed: 60.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1926 p.248 (f812) zones soft_CS_yield 1920: yield = production / area: cells give 2.79, printed 3 (difference 0.21)
  - sgt1926 p.248 (f812) zones barley_CS_yield 1919: yield = production / area: cells give 1.61, printed 1.8 (difference 0.19)
  - sgt1926 p.249 (f813) zones durum_CS_yield 1923: yield = production / area: cells give 2.01, printed 1.2 (difference -0.81)
  - sgt1926 p.249 (f813) zones barley_N_yield 1921: yield = production / area: cells give 8.39, printed 7.8 (difference -0.59)
  - sgt1926 p.249 (f813) zones barley_N_yield 1924: yield = production / area: cells give 3.19, printed 3.4 (difference 0.21)
  - sgt1926 p.249 (f813) zones oats_CS_yield 1922: yield = production / area: cells give 1.02, printed 0.1 (difference -0.92)
  - sgt1927 p.240 (f268) zones soft_CS_yield 1920: yield = production / area: cells give 2.79, printed 3 (difference 0.21)
  - sgt1927 p.240 (f268) zones barley_N_yield 1921: yield = production / area: cells give 8.39, printed 7.8 (difference -0.59)
  - sgt1927 p.240 (f268) zones barley_CS_yield 1919: yield = production / area: cells give 1.61, printed 1.8 (difference 0.19)
  - sgt1927 p.241 (f269) zones durum_CS_yield 1923: yield = production / area: cells give 2.01, printed 1.2 (difference -0.81)
  - sgt1927 p.241 (f269) zones soft_CS_yield 1927: yield = production / area: cells give 4.50, printed 4.0 (difference -0.50)
  - sgt1927 p.241 (f269) zones barley_N_yield 1924: yield = production / area: cells give 3.19, printed 3.4 (difference 0.21)
  - sgt1927 p.241 (f269) zones oats_CS_yield 1922: yield = production / area: cells give 1.02, printed 0.1 (difference -0.92)
  - sgt1927 p.241 (f269) zones oats_CS_yield 1927: yield = production / area: cells give 1.70, printed 1.0 (difference -0.70)
  - sgt1928 p.240 (f792) zones soft_CS_yield 1920: yield = production / area: cells give 2.79, printed 3 (difference 0.21)
  - sgt1928 p.240 (f792) zones barley_N_yield 1921: yield = production / area: cells give 8.39, printed 7.8 (difference -0.59)
  - sgt1928 p.240 (f792) zones barley_CS_yield 1919: yield = production / area: cells give 1.61, printed 1.8 (difference 0.19)
  - sgt1928 p.240 (f792) zones oats_CS_yield 1922: yield = production / area: cells give 1.02, printed 0.1 (difference -0.92)
  - sgt1928 p.241 (f793) zones durum_CS_yield 1923: yield = production / area: cells give 2.01, printed 1.2 (difference -0.81)
  - sgt1928 p.241 (f793) zones barley_N_yield 1924: yield = production / area: cells give 3.19, printed 3.4 (difference 0.21)
  - sgt1928 p.241 (f793) zones oats_CS_yield 1927: yield = production / area: cells give 1.70, printed 1.0 (difference -0.70)
  - sgt1929 p.242 (f270) zones soft_CS_yield 1920: yield = production / area: cells give 2.79, printed 3 (difference 0.21)
  - sgt1929 p.242 (f270) zones barley_N_yield 1921: yield = production / area: cells give 8.39, printed 7.8 (difference -0.59)
  - sgt1929 p.243 (f271) zones barley_N_yield 1924: yield = production / area: cells give 3.19, printed 3.4 (difference 0.21)
  - sgt1929 p.243 (f271) zones oats_CS_yield 1927: yield = production / area: cells give 1.70, printed 1.0 (difference -0.70)
  - sgt1930 p.246 (f804) zones barley_N_yield 1921: yield = production / area: cells give 8.39, printed 7.8 (difference -0.59)
  - sgt1930 p.246 (f804) zones barley_N_yield 1924: yield = production / area: cells give 3.19, printed 3.4 (difference 0.21)
  - sgt1930 p.247 (f805) zones barley_N_yield 1930: yield = production / area: cells give 2.06, printed 5 (difference 2.94)
  - sgt1930 p.247 (f805) zones oats_CS_yield 1927: yield = production / area: cells give 1.70, printed 1.0 (difference -0.70)
  - sgt1935 p.125 (f145) zones durum_N_yield 1933: yield = production / area: cells give 3.75, printed 3.5 (difference -0.25)
  - sgt1936 p.95 (f106) zones barley_N_yield 1935: yield = production / area: cells give 2.00, printed 6 (difference 4.00)
  - sgt1939 p.99 (f105) zones durum_N_yield 1937: yield = production / area: cells give 7.39, printed 6.8 (difference -0.59)
  - sgt1939 p.99 (f105) zones soft_CS_yield 1939: yield = production / area: cells give 5.56, printed 8.5 (difference 2.94)
  - sgt1927 p.241 (f269) zones durum_CS_area: average 1923-1927: cells give 213550.40, printed 215550 (difference 1999.60)
  - sgt1927 p.241 (f269) zones durum_CS_area: average 1918-1927: cells give 214122.30, printed 215122 (difference 999.70)
  - sgt1927 p.241 (f269) zones soft_N_area: average 1918-1922: cells give 47403.20, printed 474032 (difference 426628.80)
  - sgt1927 p.241 (f269) zones soft_N_prod: average 1923-1927: cells give 497540.00, printed 459540 (difference -38000.00)
  - sgt1927 p.241 (f269) zones soft_CS_prod: average 1923-1927: cells give 4488.00, printed 4468 (difference -20.00)
  - sgt1927 p.241 (f269) zones barley_N_area: average 1923-1927: cells give 174891.40, printed 154770 (difference -20121.40)
  - sgt1927 p.241 (f269) zones barley_N_area: average 1918-1927: cells give 170972.10, printed 160911 (difference -10061.10)
  - sgt1927 p.241 (f269) zones barley_N_prod: average 1918-1922: cells give 845000.00, printed 841000 (difference -4000.00)
  - sgt1927 p.241 (f269) zones barley_N_prod: average 1918-1927: cells give 855230.00, printed 853230 (difference -2000.00)
  - sgt1927 p.241 (f269) zones barley_CS_area: average 1918-1922: cells give 271197.80, printed 251197 (difference -20000.80)
  - sgt1927 p.241 (f269) zones barley_CS_area: average 1923-1927: cells give 267674.80, printed 247674 (difference -20000.80)
  - sgt1927 p.241 (f269) zones barley_CS_area: average 1918-1927: cells give 269436.30, printed 249436 (difference -20000.30)
  - sgt1927 p.241 (f269) zones barley_CS_prod: average 1918-1927: cells give 633770.00, printed 663770 (difference 30000.00)
  - sgt1927 p.241 (f269) zones oats_N_area: average 1918-1922: cells give 54028.00, printed 53222 (difference -806.00)
  - sgt1927 p.241 (f269) zones oats_N_area: average 1923-1927: cells give 39436.60, printed 39272 (difference -164.60)
  - sgt1927 p.241 (f269) zones oats_N_area: average 1918-1927: cells give 46732.30, printed 46247 (difference -485.30)
  - sgt1928 p.241 (f793) zones durum_N_area: average 1919-1928: cells give 332310.90, printed 331310 (difference -1000.90)
  - sgt1928 p.241 (f793) zones durum_CS_area: average 1919-1923: cells give 213757.80, printed 213157 (difference -600.80)
  - sgt1928 p.241 (f793) zones soft_N_area: average 1919-1923: cells give 46502.00, printed 53102 (difference 6600.00)
  - sgt1928 p.241 (f793) zones soft_N_area: average 1919-1928: cells give 54119.90, printed 57419 (difference 3299.10)
  - sgt1928 p.241 (f793) zones soft_CS_prod: average 1919-1923: cells give 1998.00, printed 2038 (difference 40.00)
  - sgt1928 p.241 (f793) zones barley_N_area: average 1924-1928: cells give 184029.20, printed 185031 (difference 1001.80)
  - sgt1929 p.243 (f271) zones oats_N_prod: average 1920-1929: cells give 318890.00, printed 310890 (difference -8000.00)
  - sgt1930 p.247 (f805) zones barley_N_prod: average 1926-1930: cells give 976460.00, printed 1076460 (difference 100000.00)
  - sgt1930 p.247 (f805) zones barley_N_prod: average 1921-1930: cells give 904730.00, printed 954730 (difference 50000.00)
  - sgt1930 p.247 (f805) zones barley_CS_prod: average 1926-1930: cells give 756540.00, printed 766540 (difference 10000.00)
  - sgt1930 p.247 (f805) zones barley_CS_prod: average 1921-1930: cells give 706770.00, printed 711770 (difference 5000.00)

- Overlapping printings: 909 cell comparisons with other editions printing the same cell; 26 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1923 / centre_south / durum_wheat / yield_per_hectare | sgt1926 | 1.2 | sgt1930 | 2 |
| 1923 / centre_south / durum_wheat / yield_per_hectare | sgt1927 | 1.2 | sgt1930 | 2 |
| 1923 / centre_south / durum_wheat / yield_per_hectare | sgt1928 | 1.2 | sgt1930 | 2 |
| 1922 / centre_south / oats / yield_per_hectare | sgt1926 | 0.1 | sgt1930 | 1 |
| 1922 / centre_south / oats / yield_per_hectare | sgt1927 | 0.1 | sgt1930 | 1 |
| 1922 / centre_south / oats / yield_per_hectare | sgt1928 | 0.1 | sgt1930 | 1 |
| 1927 / north / durum_wheat / production | sgt1927 | 1699000 | sgt1930 | 1660000 |
| 1927 / north / durum_wheat / yield_per_hectare | sgt1927 | 4.5 | sgt1930 | 4.4 |
| 1927 / centre_south / durum_wheat / production | sgt1927 | 101000 | sgt1930 | 100000 |
| 1927 / north / soft_wheat / production | sgt1927 | 441000 | sgt1930 | 432000 |
| 1927 / north / soft_wheat / yield_per_hectare | sgt1927 | 7.8 | sgt1930 | 7.7 |
| 1927 / centre_south / soft_wheat / production | sgt1927 | 9000 | sgt1930 | 8000 |
| 1927 / north / barley / production | sgt1927 | 717300 | sgt1930 | 712300 |
| 1928 / north / durum_wheat / production | sgt1928 | 1886000 | sgt1930 | 2230000 |
| 1928 / north / durum_wheat / yield_per_hectare | sgt1928 | 4.4 | sgt1930 | 5.2 |
| 1928 / centre_south / durum_wheat / production | sgt1928 | 964000 | sgt1930 | 1000000 |
| 1928 / centre_south / durum_wheat / yield_per_hectare | sgt1928 | 2.9 | sgt1930 | 3 |
| 1928 / north / soft_wheat / production | sgt1928 | 437000 | sgt1930 | 485000 |
| 1928 / north / soft_wheat / yield_per_hectare | sgt1928 | 6.9 | sgt1930 | 7.6 |
| 1928 / centre_south / soft_wheat / production | sgt1928 | 13000 | sgt1930 | 15000 |
| 1928 / centre_south / soft_wheat / yield_per_hectare | sgt1928 | 5.0 | sgt1930 | 5.7 |
| 1928 / north / barley / production | sgt1928 | 1360000 | sgt1930 | 1320000 |
| 1928 / north / barley / yield_per_hectare | sgt1928 | 6.8 | sgt1930 | 6.5 |
| 1928 / centre_south / barley / production | sgt1928 | 1390000 | sgt1930 | 1330000 |
| 1928 / centre_south / barley / production | sgt1929 | 1380000 | sgt1930 | 1330000 |
| 1935 / north / barley / area | sgt1935 | 150000 | sgt1936 | 450000 |

- Flagged cells: reprint_corrected: 1, total_mismatch: 1.

  - sgt1930 p.247 1930 north / barley / production / quintals = 350000 (total_mismatch)
  - sgt1935 p.125 1935 north / barley / area / hectares = 150000 (reprint_corrected)

## Image versus OCR

- Read cell by cell on the page images (13 printings): sgt1926 f812, sgt1926 f813, sgt1927 f268, sgt1927 f269, sgt1928 f792, sgt1928 f793, sgt1929 f270, sgt1929 f271, sgt1930 f804, sgt1930 f805, sgt1935 f145, sgt1936 f106, sgt1939 f105.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
