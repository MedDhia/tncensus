# Huile d'olive ; Vins : a) Importation et exportation par campagne commerciale ; b) Stoks disponibles ; c) Consommation moyenne

*Olive oil and wine: imports and exports by commercial campaign, available stocks and average consumption.*

Source: *Statistique générale de la Tunisie*, chapter *Commerce et navigation*, editions sgt1922, sgt1923, sgt1924. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 388, f412, p. 389, f413, p. 390, f414, p. 391, f415; sgt1923 (`bpt6k9105649x`): p. 400, f902, p. 401, f903, p. 402, f904, p. 403, f905; sgt1924 (`bpt6k9105649x`): p. 416, f1406, p. 417, f1407, p. 418, f1408, p. 419, f1409.

Transcriptions: `../transcribed/commerce_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_commerce.py build`.

Rows: 156. Years: 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923.

Units as printed (see `unit`); value_type: count (quantity).

Selection (SPEC_ADDENDUM rule 4): a) and b) each edition prints the last ten campaigns or harvests; each is stored once, from the latest edition printing it; every other printing is compared and differences listed below. c) each edition prints a different ten-year average; all three are stored.

## Columns

- `census`: edition the value is taken from (a, b: latest edition printing the campaign or harvest, rule 4; c: each edition prints its own ten-year average)
- `table_id`: `oil_wine_trade` (a) Importation et exportation par campagne commerciale), `oil_wine_stocks` (b) Stoks disponibles) or `oil_wine_consumption` (c) Consommation moyenne)
- `gallica_ark`: Gallica volume ark
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: a: first year of the campaign; b: harvest year; c: last year of the averaging period
- `period`: a: commercial campaign (e.g. `1912-1913`); b: harvest year (Récolte); c: averaging period as printed
- `product`: `olive_oil` or `wine`
- `product_fr`: line heading as printed
- `measure`: `import`, `export`, `balance` (a); `production`, `campaign`, `remaining` (b); `avg_consumption_total`, `avg_consumption_per_capita` (c)
- `measure_fr`: line or column heading as printed
- `unit`: `thousand_quintals` (oil a, b), `thousand_hectolitres` (wine a, b), `kilograms`, `hectolitres`, `kilograms_per_inhabitant`, `litres_per_inhabitant` (c), as printed
- `value`: as printed; balance and campaign signed (+ = excess of imports, - = excess of exports)
- `flag`: always empty in this table

Olive oil and wine: imports and exports by commercial campaign, stocks available after each harvest, and average consumption. Printed titles: *Huile d'olive (1)* and *Vins*, each with *a) Importation et exportation par campagne commerciale*, *b) Stoks disponibles* and *c) Consommation moyenne des années 1912 à 1921* (sgt1922; sgt1923 1913 à 1922, sgt1924 1914 à 1923). Footnotes (translated): olive oil (1) not including oils and *grignons* (pomace); wine a) (1) exports include those of the Navy; the sign + indicates the excess of imports over exports, the sign -, the excess of exports over imports; olive oil b) (1) the harvest considered is the one beginning at the end of the year and continuing into the first months of the next; wine c) (2) Muslims and Jews not included (per capita figure).

a) and b) are printed in thousands of quintals (oil) and thousands of hectolitres (wine); the balance line (a) and the campaign column (b) are stored signed as printed and also used as checks (balance = import - export; production + campaign = remaining; b) campaign of harvest Y = a) balance of campaign Y-(Y+1)). The c) totals are checked against the mean of the b) *remaining* column of the same edition (1.000 quintals = 100.000 kg; 1.000 hl = 1.000 hl). The three printed averages of a) (*Moyenne des années*) were transcribed as checks (tolerance 1) and are not stored. Printed » = 0. sgt1922 prints the oil per capita figure as *7,046* (kilograms, decimal comma); sgt1923 and sgt1924 print 7.

Explanation of the failed checks (cells re-read on native-resolution crops of f412-415, f902-905 and f1406-1409; each line typed separately from its own edition's images). Olive oil 1919: production 165, campaign - 20, remaining printed 135 (165 - 20 = 145), identically in all three editions; the campaign agrees with a) (1919-1920 export 20) and the printed c) totals (14.590.000, 14.530.000, 14.680.000 kg) agree with the remaining column as printed (135), so the production figure (or the remaining figure from which consumption was computed) is misprinted; the table does not decide which, nothing flagged. Wine 1916: production 450, campaign - 212, remaining printed 288 (450 - 212 = 238), in all three editions; sgt1923 and sgt1924 c) totals agree with 288, so the same remark applies. sgt1922 wine c) total printed 218.800 hl while the ten remaining figures 1912-1921 average 226.000 (221.000 with 238 for 1916): not explained by any single cell, kept as printed. Failed average checks (three, all sgt1923 olive oil): the import average 1913-14/1917-18 is printed 1 and the ten-campaign import average 0, while the campaigns (1, 6, 4, 1, », all re-read, and printed identically in sgt1922 and sgt1924) average 2,4 and 1,2; the balance average 1913-14/1917-18 (printed - 128) equals the printed export average 129 minus that import average 1, so the printer averaged a different import figure; the yearly cells stand. No figure is flagged since averages are not stored.

Survey of the whole chapter: `commerce_survey.md`.

## Validation

- Checks against printed totals and identities: 240; passed: 230; failed: 10.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1923 olive_oil balance: printed average 1913-1914/1917-1918 = mean of the campaigns: cells give -126.8, printed -128 (difference -1.2)
  - sgt1923 olive_oil import: printed average 1913-1914/1917-1918 = mean of the campaigns: cells give 2.4, printed 1 (difference -1.4)
  - sgt1923 olive_oil import: printed average 1913-1914/1922-1923 = mean of the campaigns: cells give 1.2, printed 0 (difference -1.2)
  - sgt1922 olive_oil 1919: production + campaign = remaining: cells give 145, printed 135 (difference -10)
  - sgt1922 wine 1916: production + campaign = remaining: cells give 238, printed 288 (difference 50)
  - sgt1923 olive_oil 1919: production + campaign = remaining: cells give 145, printed 135 (difference -10)
  - sgt1923 wine 1916: production + campaign = remaining: cells give 238, printed 288 (difference 50)
  - sgt1924 olive_oil 1919: production + campaign = remaining: cells give 145, printed 135 (difference -10)
  - sgt1924 wine 1916: production + campaign = remaining: cells give 238, printed 288 (difference 50)
  - sgt1922 wine: average consumption 1912-1921 = mean of the b) remaining column, in hectolitres: cells give 226000, printed 218800 (difference -7200)

- Overlapping printings: 216 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (30 printings): sgt1922 f412, sgt1922 f413, sgt1922 f412, sgt1922 f413, sgt1922 f413, sgt1922 f414, sgt1922 f415, sgt1922 f414, sgt1922 f415, sgt1922 f415, sgt1923 f902, sgt1923 f903, sgt1923 f902, sgt1923 f903, sgt1923 f903, sgt1923 f904, sgt1923 f905, sgt1923 f904, sgt1923 f905, sgt1923 f905, sgt1924 f1406, sgt1924 f1407, sgt1924 f1406, sgt1924 f1407, sgt1924 f1407, sgt1924 f1408, sgt1924 f1409, sgt1924 f1408, sgt1924 f1409, sgt1924 f1409.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
