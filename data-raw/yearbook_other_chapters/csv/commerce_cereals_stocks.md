# Céréales : b) Stoks disponibles ; c) Consommation moyenne

*Cereals: available stocks and average consumption.*

Source: *Statistique générale de la Tunisie*, chapter *Commerce et navigation*, editions sgt1922, sgt1923, sgt1924. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 386, f410, p. 387, f411; sgt1923 (`bpt6k9105649x`): p. 398, f900, p. 399, f901; sgt1924 (`bpt6k9105649x`): p. 414, f1404, p. 415, f1405.

Transcriptions: `../transcribed/commerce_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_commerce.py build`.

Rows: 258. Years: 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923.

Units: thousands of quintals (b), quintals and kilograms per inhabitant (c), as printed; value_type: count (quantity).

Selection (SPEC_ADDENDUM rule 4): b) each edition prints the last ten harvests (sgt1922 1912-1921, sgt1923 1913-1922, sgt1924 1914-1923); each harvest is stored once, from the latest edition printing it; every other printing is compared and differences listed below. c) each edition prints a different ten-year average; all three are stored.

## Columns

- `census`: edition the value is taken from (b: latest edition printing the harvest, rule 4; c: each edition prints its own ten-year period)
- `table_id`: `cereals_stocks` (b) Stoks disponibles) or `cereals_consumption` (c) Consommation moyenne)
- `gallica_ark`: Gallica volume ark
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: b: harvest year (Récolte); c: last year of the averaging period
- `period`: b: harvest year; c: averaging period as printed (e.g. `1912-1921`)
- `product`: `wheat`, `barley`, `oats`, `maize` (c) has no oats line)
- `product_fr`: line heading as printed
- `measure`: `production`, `campaign`, `remaining`, `seed`, `consumption` (b); `avg_consumption_total`, `avg_consumption_per_capita` (c)
- `measure_fr`: column heading (translated column codes in the notes)
- `unit`: `thousand_quintals` (b, printed *1.000 qt*), `quintals` (c total), `kilograms_per_inhabitant` (c per capita)
- `value`: as printed; campaign signed as printed (+ = excess of imports, - = excess of exports)
- `flag`: empty, `not_applicable` (per capita printed », not computed) or `total_mismatch` (see notes)

Cereal stocks available after each harvest and average consumption. Full printed titles: *Céréales : b) Stoks disponibles* (two-page spread) and *c) Consommation moyenne des années 1912 à 1921* (sgt1922; sgt1923 *1913 à 1922*, sgt1924 *1914-1923*). Footnotes (translated): (1) wheat includes flours and semolinas, counted as the corresponding weight of grain; (2) the sign + indicates the excess of imports over exports, the sign -, the excess of exports over imports; (3) seed not included.

Column codes of b) (all in thousands of quintals): `production` = Production; `campaign` = Campagne commerciale consécutive (net trade of the commercial campaign following the harvest, signed); `remaining` = Quantités restant dans le pays; `seed` = Quantités prélevées pour les semences; `consumption` = Quantités restant pour la consommation. The identities production + campaign = remaining and remaining - seed = consumption are checks (all values are stored as printed). The c) totals are checked against the mean of the b) consumption column of the same edition (x 1000).

c) prints a per-capita figure for wheat only; the barley and maize cells are printed » (no figure computed) and are stored as NA with flag `not_applicable` rather than 0.

sgt1923 labels its last harvest *1923* (f901); the sequence runs 1913-1921 then 1923 and sgt1924 prints the same four lines under 1922 (and different ones under 1923), so the label is a misprint and the lines were transcribed as harvest 1922 (stored from sgt1924 under rule 4 in any case).

Explanation of the failed checks (cells re-read on native-resolution crops of f410-411, f900-901 and f1404-1405; each recurs identically in the three printings, each typed from its own image). Oats 1916 (360 - 277 = 83, printed remaining 93) and oats 1919 (450 - 318 = 132, printed 148): the campaign figures agree with the a) table (`commerce_cereals_balance`, oats balance 1916-1917 -277.087 and 1919-1920 -317.983 quintals) and remaining - seed = consumption holds (93 - 42 = 51, 148 - 38 = 110), so either the production or the remaining-and-consumption figures are misprinted; the table does not decide which, so nothing is flagged. sgt1923 c) maize total is printed 138.200 quintals while the ten harvests 1913-1922 average 154.700; 138.200 is the sum of the nine harvests 1914-1922 (1.382 thousand quintals) divided by ten, i.e. the 1913 line (165) was left out. sgt1924 (141.900) and sgt1922 (215.600) agree with their columns. The printed value is kept and flagged `total_mismatch`.

Survey of the whole chapter: `commerce_survey.md`.

## Validation

- Checks against printed totals and identities: 249; passed: 242; failed: 7.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 1916 oats: production + campaign = remaining: cells give 83, printed 93 (difference 10)
  - sgt1922 1919 oats: production + campaign = remaining: cells give 132, printed 148 (difference 16)
  - sgt1923 1916 oats: production + campaign = remaining: cells give 83, printed 93 (difference 10)
  - sgt1923 1919 oats: production + campaign = remaining: cells give 132, printed 148 (difference 16)
  - sgt1924 1916 oats: production + campaign = remaining: cells give 83, printed 93 (difference 10)
  - sgt1924 1919 oats: production + campaign = remaining: cells give 132, printed 148 (difference 16)
  - sgt1923 maize: average consumption 1913-1922 = mean of the b) consumption column x 1000: cells give 154700, printed 138200 (difference -16500)

- Overlapping printings: 360 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: not_applicable: 6, total_mismatch: 1.

  - sgt1922 p.387 1921 1912-1921 / barley / avg_consumption_per_capita / kilograms_per_inhabitant = NA (not_applicable)
  - sgt1922 p.387 1921 1912-1921 / maize / avg_consumption_per_capita / kilograms_per_inhabitant = NA (not_applicable)
  - sgt1923 p.399 1922 1913-1922 / barley / avg_consumption_per_capita / kilograms_per_inhabitant = NA (not_applicable)
  - sgt1923 p.399 1922 1913-1922 / maize / avg_consumption_total / quintals = 138200 (total_mismatch)
  - sgt1923 p.399 1922 1913-1922 / maize / avg_consumption_per_capita / kilograms_per_inhabitant = NA (not_applicable)
  - sgt1924 p.415 1923 1914-1923 / barley / avg_consumption_per_capita / kilograms_per_inhabitant = NA (not_applicable)
  - sgt1924 p.415 1923 1914-1923 / maize / avg_consumption_per_capita / kilograms_per_inhabitant = NA (not_applicable)

## Image versus OCR

- Read cell by cell on the page images (9 printings): sgt1922 f410, sgt1922 f411, sgt1922 f411, sgt1923 f900, sgt1923 f901, sgt1923 f901, sgt1924 f1404, sgt1924 f1405, sgt1924 f1405.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
