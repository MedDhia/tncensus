# Navigation : c) sur le littoral ; marchandises et passagers

*Navigation: shipping on the coast, goods and passengers, by year.*

Source: *Statistique générale de la Tunisie*, chapter *Commerce et navigation*, editions sgt1922, sgt1923, sgt1924. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 408, f432; sgt1923 (`bpt6k9105649x`): p. 420, f922; sgt1924 (`bpt6k9105649x`): p. 436, f1426.

Transcriptions: `../transcribed/commerce_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_commerce.py build`.

Rows: 72. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924.

Units: ships, tonnes, passengers, as printed. value_type: count.

Selection (SPEC_ADDENDUM rule 4): each edition prints the last ten years; each year is stored once, from the latest edition printing it (1913 from sgt1922, 1914 from sgt1923, 1915-1924; every cell 1915-1923 printed by two or three editions from sgt1924); every other printing of the same cell is compared and the differences listed below.

## Columns

- `census`: edition the value is taken from: the latest edition printing that year legibly (rule 4; see notes on the gutter)
- `table_id`: `navigation_c` (Mouvement des navires, c) Sur le littoral ; marchandises et passagers)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: calendar year of the movement
- `movement`: `entries` or `exits`
- `movement_fr`: as printed
- `measure`: `ships`, `goods`, `passengers`
- `measure_fr`: column as printed
- `unit`: `ships`, `tonnes`, `persons`
- `value`: as printed
- `flag`: empty

Shipping on the Tunisian coast (all ports together), entries and exits: ships, tonnes of goods, passengers, by calendar year. The last year of each edition was checked against the TOTAUX of a) *par port* of the same edition (ships, goods and passengers, entries and exits).

Explanation of the failed check and of the overlap difference: sgt1923 prints the 1923 exits of goods as 3.616.904 tonnes, while its own a) par port and b) par pavillons TOTAUX give 3.626.904; sgt1924 reprints the year as 3.626.904, which is the value stored (rule 4). Both printings re-read on native-resolution crops of f922 and f1426.

Survey of the whole chapter: `commerce_survey.md`.

## Validation

- Checks against printed totals and identities: 17; passed: 16; failed: 1.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1923 p.420 (f922) nav_yearly 1923 S.goods = TOTAUX of a) par port: cells give 3626904, printed 3616904 (difference -10000)

- Overlapping printings: 108 cell comparisons with other editions printing the same cell; 1 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1923 / exits / goods | sgt1923 | 3616904 | sgt1924 | 3626904 |

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (3 printings): sgt1922 f432, sgt1923 f922, sgt1924 f1426.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
