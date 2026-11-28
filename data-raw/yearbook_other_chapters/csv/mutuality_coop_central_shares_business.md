# Coopérative centrale des agriculteurs. a) Nombre de parts souscrites ; b) Affaires traitées

*Central cooperative of farmers: shares subscribed, goods delivered and loans by type, by year (1913-1929).*

Source: *Statistique générale de la Tunisie*, chapter *Institutions économiques et sociales / Mutualité agricole*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 437, f461; sgt1923 (`bpt6k9105649x`): p. 449, f951; sgt1924 (`bpt6k9105649x`): p. 459, f1449; sgt1925 (`bpt6k9105650k`): p. 495, f519; sgt1926 (`bpt6k9105650k`): p. 463, f1027; sgt1927 (`bpt6k91056510`): p. 463, f491; sgt1928 (`bpt6k91056510`): p. 467, f1019; sgt1929 (`bpt6k9105652d`): p. 468, f496.

Transcriptions: `../transcribed/mutuality_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_mutuality.py build`.

Rows: 197. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929.

Units: count (shares) and francs (centimes as decimals); suggested value_type: mixed.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (rule 4 tables: the latest edition printing that year)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible`, `not_applicable`, `total_mismatch`, `ocr_corrected`

Printed sgt1922-sgt1929 for the ten years before the edition; replaced from sgt1930 by `mutuality_coop_central_capital`. a) parts souscrites (sgt1922 also prints a parts à 20 fr. column, » throughout), b) affaires traitées: montant des marchandises livrées and prêts divers by type, montant total des prêts (= sum of the six loan types, checked on every line) and prêts restant à rembourser. TOTAUX lines (sgt1922-sgt1925) are checks only.

The sgt1922 and sgt1923 printings differ from sgt1924 and later for the shares of 1915-1920 and the goods of 1915-1917 and 1919-1922 (revised figures); the latest printing is kept and every difference is listed below. The loan lines are identical in every printing.

Every failed check below was re-read on a native-resolution crop: the printed values are kept. sgt1922 and sgt1923 print the 1914 montant total des prêts 1.213.382,55 for 880.558,10 + 332.794,45 = 1.213.352,55 (zoomed crops of both printings; sgt1924 and later no longer print 1914), and the TOTAUX of the loan columns follow it (9.467.198,10); their travaux de printemps total 556.483,85 is 0,10 above the lines (sgt1924-sgt1925 print 556.483,75). sgt1922's marchandises TOTAUX 15.512.861,90 is 100.000 above its lines (every line re-read at 2.5x). sgt1923: sommes TOTAUX 33.050 for lines giving 23.050 (the number of parts, 461, adds up), and prêts restant à rembourser TOTAUX 1.103.297,55 for lines giving 378.063,45. sgt1925 reprints sgt1924's loan TOTAUX, which include the 1915 line it no longer prints (each difference equals the sgt1924 1915 figure).

Survey of the whole chapter in every edition: `mutuality_survey.md`.

## Validation

- Checks against printed totals and identities: 124; passed: 109; failed: 15.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.437 (f461) coop_business 1914: loans_total = seeds + labour + spring + harvest + fertiliser + tractors: cells give 1213352.55, printed 1213382.55 (difference 30.00)
  - sgt1922 p.437 (f461) coop_business TOTAUX: loans_total = seeds + labour + spring + harvest + fertiliser + tractors: cells give 9467168.20, printed 9467198.10 (difference 29.90)
  - sgt1922 p.437 (f461) coop_business goods: TOTAUX = sum of the lines: cells give 15412861.90, printed 15512861.90 (difference 100000.00)
  - sgt1922 p.437 (f461) coop_business spring: TOTAUX = sum of the lines: cells give 556483.75, printed 556483.85 (difference 0.10)
  - sgt1923 p.449 (f951) coop_parts sums: TOTAUX = sum of the lines: cells give 23050, printed 33050 (difference 10000)
  - sgt1923 p.449 (f951) coop_business 1914: loans_total = seeds + labour + spring + harvest + fertiliser + tractors: cells give 1213352.55, printed 1213382.55 (difference 30.00)
  - sgt1923 p.449 (f951) coop_business TOTAUX: loans_total = seeds + labour + spring + harvest + fertiliser + tractors: cells give 9467168.20, printed 9467198.10 (difference 29.90)
  - sgt1923 p.449 (f951) coop_business spring: TOTAUX = sum of the lines: cells give 556483.75, printed 556483.85 (difference 0.10)
  - sgt1923 p.449 (f951) coop_business outstanding: TOTAUX = sum of the lines: cells give 378063.45, printed 1103297.55 (difference 725234.10)
  - sgt1925 p.495 (f519) coop_business seeds: TOTAUX = sum of the lines: cells give 3433559.70, printed 3515011.15 (difference 81451.45)
  - sgt1925 p.495 (f519) coop_business labour: TOTAUX = sum of the lines: cells give 756418.05, printed 922453.90 (difference 166035.85)
  - sgt1925 p.495 (f519) coop_business spring: TOTAUX = sum of the lines: cells give 444208.75, printed 556483.75 (difference 112275.00)
  - sgt1925 p.495 (f519) coop_business harvest: TOTAUX = sum of the lines: cells give 1324096.90, printed 1599609.50 (difference 275512.60)
  - sgt1925 p.495 (f519) coop_business loans_total: TOTAUX = sum of the lines: cells give 7618540.65, printed 8253815.55 (difference 635274.90)
  - sgt1925 p.495 (f519) coop_business outstanding: TOTAUX = sum of the lines: cells give 363633.40, printed 378063.45 (difference 14430.05)

- Overlapping printings: 693 cell comparisons with other editions printing the same cell; 39 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1916 / shares_50fr | sgt1922 | 6 | sgt1925 | 10 |
| 1916 / shares_50fr | sgt1923 | 6 | sgt1925 | 10 |
| 1916 / shares_amount | sgt1922 | 300 | sgt1925 | 500 |
| 1916 / shares_amount | sgt1923 | 300 | sgt1925 | 500 |
| 1917 / shares_50fr | sgt1922 | 8 | sgt1926 | 0 |
| 1917 / shares_50fr | sgt1923 | 8 | sgt1926 | 0 |
| 1917 / shares_amount | sgt1922 | 400 | sgt1926 | 0 |
| 1917 / shares_amount | sgt1923 | 400 | sgt1926 | 0 |
| 1918 / shares_50fr | sgt1922 | 20 | sgt1927 | 0 |
| 1918 / shares_50fr | sgt1923 | 20 | sgt1927 | 0 |
| 1918 / shares_amount | sgt1922 | 1000 | sgt1927 | 0 |
| 1918 / shares_amount | sgt1923 | 1000 | sgt1927 | 0 |
| 1919 / shares_50fr | sgt1922 | 21 | sgt1928 | 0 |
| 1919 / shares_50fr | sgt1923 | 21 | sgt1928 | 0 |
| 1919 / shares_amount | sgt1922 | 1050 | sgt1928 | 0 |
| 1919 / shares_amount | sgt1923 | 1050 | sgt1928 | 0 |
| 1920 / shares_50fr | sgt1922 | 10 | sgt1929 | 0 |
| 1920 / shares_50fr | sgt1923 | 10 | sgt1929 | 0 |
| 1920 / shares_amount | sgt1922 | 500 | sgt1929 | 0 |
| 1920 / shares_amount | sgt1923 | 500 | sgt1929 | 0 |
| 1921 / shares_50fr | sgt1922 | 12 | sgt1929 | 61 |
| 1921 / shares_50fr | sgt1923 | 12 | sgt1929 | 61 |
| 1921 / shares_amount | sgt1922 | 600 | sgt1929 | 3050 |
| 1921 / shares_amount | sgt1923 | 600 | sgt1929 | 3050 |
| 1915 / goods_delivered | sgt1922 | 472348.65 | sgt1924 | 430803.25 |
| 1915 / goods_delivered | sgt1923 | 472348.65 | sgt1924 | 430803.25 |
| 1916 / goods_delivered | sgt1922 | 1020837.20 | sgt1925 | 574769.75 |
| 1916 / goods_delivered | sgt1923 | 1020837.20 | sgt1925 | 574769.75 |
| 1917 / goods_delivered | sgt1922 | 847599.15 | sgt1926 | 808768.45 |
| 1917 / goods_delivered | sgt1923 | 847599.15 | sgt1926 | 808768.45 |
| 1919 / goods_delivered | sgt1922 | 1492456.11 | sgt1928 | 1494406.11 |
| 1919 / goods_delivered | sgt1923 | 1402456.11 | sgt1928 | 1494406.11 |
| 1920 / goods_delivered | sgt1922 | 2982705.30 | sgt1929 | 2840290 |
| 1920 / goods_delivered | sgt1923 | 2982705.30 | sgt1929 | 2840290 |
| 1921 / goods_delivered | sgt1922 | 2397469.25 | sgt1929 | 2461269.75 |
| 1921 / goods_delivered | sgt1923 | 2307469.25 | sgt1929 | 2461269.75 |
| 1922 / goods_delivered | sgt1922 | 3109047.17 | sgt1929 | 4266075.62 |
| 1922 / goods_delivered | sgt1923 | 3109047.17 | sgt1929 | 4266075.62 |
| 1923 / goods_delivered | sgt1923 | 4797481.15 | sgt1929 | 6942374.25 |

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (16 printings): sgt1922 f461, sgt1922 f461, sgt1923 f951, sgt1923 f951, sgt1924 f1449, sgt1924 f1449, sgt1925 f519, sgt1925 f519, sgt1926 f1027, sgt1926 f1027, sgt1927 f491, sgt1927 f491, sgt1928 f1019, sgt1928 f1019, sgt1929 f496, sgt1929 f496.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
