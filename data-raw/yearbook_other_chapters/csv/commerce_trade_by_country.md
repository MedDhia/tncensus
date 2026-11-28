# Renseignements généraux : résumé des relations commerciales avec les différents pays (valeur en francs)

*General information: trade with the different countries (value in francs).*

Source: *Statistique générale de la Tunisie*, chapter *Commerce et navigation*, editions sgt1922, sgt1923, sgt1924. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 266, f290, p. 268, f292; sgt1923 (`bpt6k9105649x`): p. 278, f780, p. 280, f782; sgt1924 (`bpt6k9105649x`): p. 294, f1284, p. 295, f1285, p. 296, f1286, p. 297, f1287.

Transcriptions: `../transcribed/commerce_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_commerce.py build`.

Rows: 696. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924.

Unit: francs (current values; see the valuation footnote in `commerce_trade_by_class`). value_type: francs.

Selection (SPEC_ADDENDUM rule 4): each edition prints the last ten years; each year is stored once, from the latest edition printing it legibly (1913 from sgt1922, 1914 from sgt1923, 1915-1924 from sgt1924); every other printing of the same cell is compared and the differences listed below.

## Columns

- `census`: edition the value is taken from: the latest edition printing that year legibly (rule 4; see notes on the gutter)
- `table_id`: `general_e` (Renseignements généraux, e) Résumé des relations commerciales avec les différents pays)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: calendar year of the trade
- `country`: country of provenance (imports) or destination (exports), English
- `country_fr`: country as printed
- `country_code`: short code of the country line (`other` = Autres pays)
- `flow`: `import` or `export`
- `flow_fr`: as printed
- `measure`: `value`
- `measure_fr`: valeur
- `unit`: `francs`
- `value`: value in francs as printed
- `flag`: empty or `total_mismatch` (see notes)

The table prints, for 28 named countries and *Autres pays*, the value of imports from and exports to each country for the last ten years, then (odd view) three printed averages (*Moyenne des années*: two five-year and one ten-year) and a TOTAUX line per flow. Averages and TOTAUX are not stored; they were used as checks (sum of countries = TOTAUX; printed average x number of years = sum of the cells, tolerance one franc per year for rounding). The TOTAUX agree with the TOTAUX of table c) (`commerce_trade_by_category`) wherever both are legible. Printed » is stored as 0. Country names are those printed; *Tripoli* is Ottoman, then Italian Tripolitania; *Indes : Comptoirs Anglais* = British India.

Gutter. The fourth year of each even view lies against the binding. sgt1922: the 1916 column loses its last digit on most lines (`?`; f290 legible on 10 lines, f292 only on lines printed »), and on f293 the 1917 export TOTAUX loses a middle digit. sgt1923: the 1917 column of f782 loses the last digit on 6 lines (`?`), and the 1918 column (f781, f783) loses leading digits on the larger values (`?`, a value kept only when its first digit is wholly visible). sgt1924 is legible throughout. A year is stored from the latest edition printing it legibly; illegible printings are not compared. sgt1922 f293 `other` export 1921: the last digit is damaged type (3 or 5), transcribed `?`; sgt1923 and sgt1924 print 6.910.483.

Every overlapping cell agrees between the editions (each printing typed from its own image). The TOTAUX failures are therefore in the printed table itself and recur in every edition printing the year: 1918 import (sum of countries 430 below TOTAUX), 1919 export (600.002 below), 1920 import (667.684 below), 1921 import (300 below), 1922 import (687.602 below) and export (618.940 above), 1923 import (2.999.990 above) and export (498 above). Every cell of those columns was re-read on native-resolution crops; the printed averages locate no single cell consistently (for 1923 the sgt1923 1919-1923 averages of `usa`, `egypt` and `turkey` import would explain the 3 million, but the sgt1924 1920-1924 averages agree with the printed 1923 cells), so nothing is flagged. sgt1922 1917 export: the TOTAUX is in the gutter (`?`); sgt1923 and sgt1924 print 125.672.079 and the check passes there.

1924 (sgt1924 only): the countries exceed TOTAUX import by 906 and fall 23.736 short of TOTAUX export. Both printed averages containing 1924 (1920-1924 and 1915-1924) imply 10.121.094 for `tripoli` export (printed 10.101.094, re-read on a zoomed crop) and 401 less than the printed 1.364.829 for `egypt` import; both corrections go in the direction of the TOTAUX gap, so these two cells are flagged `total_mismatch` (printed value kept). The residuals (3.736 export, 505 import) are not located. sgt1925 reprints 1924.

Failed average checks (averages are not stored and were never used to change a cell). Every year of every failing average window is printed identically by two or three editions, except the 1924 cells discussed above, so the failures are misprinted or miscomputed averages: (i) round-number slips in one average only (e.g. sgt1922 `algeria` export 1913-1922, 1.000.000; sgt1923 `turkey` export 1914-1923, 300.000, `russia` export 1919-1923, 20.000; sgt1924 `usa` import 1915-1919, 10.000.000, `france` export 1915-1924, 50.000.000, `belgium` export 1915-1924, 7.000.000, `morocco` export, `india` and `romania` import 1920-1924 and 1915-1924, 500.000; TOTAUX import 1915-1919 and 1915-1924, 5.000.000); (ii) small differences of a few francs to a few thousand francs (rounding or copying slips); (iii) averages computed on a different state of the figures: sgt1922 `switzerland` export 1918-1922 and 1913-1922 omit the 1922 value (308.315, confirmed by sgt1923-1924 and the sgt1923 1919-1923 average), `china` export omits 1921 (32); sgt1924 `usa` export 1920-1924 and 1915-1924 omit 1924 (7.187.353); sgt1924 `bulgaria` import 1920-1924 repeats the sgt1923 1919-1923 average (172.237) and `russia` export prints the 1915-1919 average (27.432) in the 1920-1924 column. (iv) sgt1922 `algeria` import 1918-1922 and 1913-1922 both imply 11.560.684 for 1918 (printed 11.650.684 in sgt1922 and sgt1924, a possible transposition), but correcting it would widen the 1918 TOTAUX gap, so the cell is not flagged.

Survey of the whole chapter: `commerce_survey.md`.

## Validation

- Checks against printed totals and identities: 454; passed: 365; failed: 89.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.269 (f293) by_country 1918: sum of countries, import = TOTAUX import: cells give 207442158, printed 207442588 (difference 430)
  - sgt1922 p.269 (f293) by_country 1919: sum of countries, export = TOTAUX export: cells give 201428869, printed 202028871 (difference 600002)
  - sgt1922 p.269 (f293) by_country 1920: sum of countries, import = TOTAUX import: cells give 634894868, printed 635562552 (difference 667684)
  - sgt1922 p.269 (f293) by_country 1921: sum of countries, import = TOTAUX import: cells give 721699855, printed 721700155 (difference 300)
  - sgt1922 p.269 (f293) by_country 1922: sum of countries, import = TOTAUX import: cells give 855689500, printed 856377102 (difference 687602)
  - sgt1922 p.269 (f293) by_country 1922: sum of countries, export = TOTAUX export: cells give 445298584, printed 444679644 (difference -618940)
  - sgt1922 p.269 (f293) by_country average 1913-1922 algeria.import: printed average x 10 = sum of years: cells give 221561844, printed 221471840 (difference -90004)
  - sgt1922 p.269 (f293) by_country average 1913-1922 algeria.export: printed average x 10 = sum of years: cells give 119603832, printed 118603810 (difference -1000022)
  - sgt1922 p.269 (f293) by_country average 1913-1922 switzerland.export: printed average x 10 = sum of years: cells give 3590888, printed 3282570 (difference -308318)
  - sgt1922 p.269 (f293) by_country average 1913-1922 china.export: printed average x 10 = sum of years: cells give 32, printed 0 (difference -32)
  - sgt1922 p.269 (f293) by_country average 1918-1922 algeria.import: printed average x 5 = sum of years: cells give 151981684, printed 151891680 (difference -90004)
  - sgt1922 p.269 (f293) by_country average 1918-1922 algeria.export: printed average x 5 = sum of years: cells give 91094233, printed 91094210 (difference -23)
  - sgt1922 p.269 (f293) by_country average 1918-1922 egypt.import: printed average x 5 = sum of years: cells give 16220469, printed 16220560 (difference 91)
  - sgt1922 p.269 (f293) by_country average 1918-1922 morocco.import: printed average x 5 = sum of years: cells give 17256719, printed 17256710 (difference -9)
  - sgt1922 p.269 (f293) by_country average 1918-1922 switzerland.export: printed average x 5 = sum of years: cells give 3562977, printed 3254660 (difference -308317)
  - sgt1922 p.269 (f293) by_country average 1918-1922 china.export: printed average x 5 = sum of years: cells give 32, printed 0 (difference -32)
  - sgt1922 p.269 (f293) by_country average 1918-1922 india.export: printed average x 5 = sum of years: cells give 354880, printed 353980 (difference -900)
  - sgt1922 p.269 (f293) by_country average 1918-1922 norway.import: printed average x 5 = sum of years: cells give 4397934, printed 4397680 (difference -254)
  - sgt1922 p.269 (f293) by_country average 1918-1922 austria.import: printed average x 5 = sum of years: cells give 10908540, printed 10908840 (difference 300)
  - sgt1922 p.269 (f293) by_country average 1918-1922 turkey.export: printed average x 5 = sum of years: cells give 1540269, printed 1540260 (difference -9)
  - sgt1923 p.281 (f783) by_country 1919: sum of countries, export = TOTAUX export: cells give 201428869, printed 202028871 (difference 600002)
  - sgt1923 p.281 (f783) by_country 1920: sum of countries, import = TOTAUX import: cells give 634894868, printed 635562552 (difference 667684)
  - sgt1923 p.281 (f783) by_country 1921: sum of countries, import = TOTAUX import: cells give 721699855, printed 721700155 (difference 300)
  - sgt1923 p.281 (f783) by_country 1922: sum of countries, import = TOTAUX import: cells give 855689500, printed 856377102 (difference 687602)
  - sgt1923 p.281 (f783) by_country 1922: sum of countries, export = TOTAUX export: cells give 445298584, printed 444679644 (difference -618940)
  - sgt1923 p.281 (f783) by_country 1923: sum of countries, import = TOTAUX import: cells give 820459210, printed 817459220 (difference -2999990)
  - sgt1923 p.281 (f783) by_country 1923: sum of countries, export = TOTAUX export: cells give 554014882, printed 554014384 (difference -498)
  - sgt1923 p.281 (f783) by_country average 1914-1918 sweden.export: printed average x 5 = sum of years: cells give 490681, printed 490580 (difference -101)
  - sgt1923 p.281 (f783) by_country average 1914-1918 japan.import: printed average x 5 = sum of years: cells give 319727, printed 319545 (difference -182)
  - sgt1923 p.281 (f783) by_country average 1914-1923 usa.export: printed average x 10 = sum of years: cells give 23820936, printed 23820430 (difference -506)
  - sgt1923 p.281 (f783) by_country average 1914-1923 sweden.export: printed average x 10 = sum of years: cells give 1296622, printed 1296520 (difference -102)
  - sgt1923 p.281 (f783) by_country average 1914-1923 russia.import: printed average x 10 = sum of years: cells give 3100779, printed 3107790 (difference 7011)
  - sgt1923 p.281 (f783) by_country average 1914-1923 turkey.export: printed average x 10 = sum of years: cells give 3817000, printed 3517000 (difference -300000)
  - sgt1923 p.281 (f783) by_country average 1914-1923 denmark.import: printed average x 10 = sum of years: cells give 382685, printed 382590 (difference -95)
  - sgt1923 p.281 (f783) by_country average 1914-1923 japan.import: printed average x 10 = sum of years: cells give 23088152, printed 23087970 (difference -182)
  - sgt1923 p.281 (f783) by_country average 1919-1923 england.import: printed average x 5 = sum of years: cells give 345313894, printed 345303890 (difference -10004)
  - sgt1923 p.281 (f783) by_country average 1919-1923 england.export: printed average x 5 = sum of years: cells give 196620855, printed 196620505 (difference -350)
  - sgt1923 p.281 (f783) by_country average 1919-1923 usa.import: printed average x 5 = sum of years: cells give 290729771, printed 287729770 (difference -3000001)
  - sgt1923 p.281 (f783) by_country average 1919-1923 usa.export: printed average x 5 = sum of years: cells give 21514312, printed 21513810 (difference -502)
  - sgt1923 p.281 (f783) by_country average 1919-1923 egypt.import: printed average x 5 = sum of years: cells give 13999063, printed 12999060 (difference -1000003)
  - sgt1923 p.281 (f783) by_country average 1919-1923 morocco.import: printed average x 5 = sum of years: cells give 18711471, printed 18711670 (difference 199)
  - sgt1923 p.281 (f783) by_country average 1919-1923 greece.import: printed average x 5 = sum of years: cells give 3749480, printed 3749490 (difference 10)
  - sgt1923 p.281 (f783) by_country average 1919-1923 russia.export: printed average x 5 = sum of years: cells give 137160, printed 117160 (difference -20000)
  - sgt1923 p.281 (f783) by_country average 1919-1923 turkey.import: printed average x 5 = sum of years: cells give 5133678, printed 6133665 (difference 999987)
  - sgt1923 p.281 (f783) by_country average 1919-1923 denmark.import: printed average x 5 = sum of years: cells give 348573, printed 348480 (difference -93)
  - sgt1924 p.296 (f1286) by_country 1918: sum of countries, import = TOTAUX import: cells give 207442158, printed 207442588 (difference 430)
  - sgt1924 p.297 (f1287) by_country 1919: sum of countries, export = TOTAUX export: cells give 201428869, printed 202028871 (difference 600002)
  - sgt1924 p.297 (f1287) by_country 1920: sum of countries, import = TOTAUX import: cells give 634894868, printed 635562552 (difference 667684)
  - sgt1924 p.297 (f1287) by_country 1921: sum of countries, import = TOTAUX import: cells give 721699855, printed 721700155 (difference 300)
  - sgt1924 p.297 (f1287) by_country 1922: sum of countries, import = TOTAUX import: cells give 855689500, printed 856377102 (difference 687602)
  - sgt1924 p.297 (f1287) by_country 1922: sum of countries, export = TOTAUX export: cells give 445298584, printed 444679644 (difference -618940)
  - sgt1924 p.297 (f1287) by_country 1923: sum of countries, import = TOTAUX import: cells give 820459210, printed 817459220 (difference -2999990)
  - sgt1924 p.297 (f1287) by_country 1923: sum of countries, export = TOTAUX export: cells give 554014882, printed 554014384 (difference -498)
  - sgt1924 p.297 (f1287) by_country 1924: sum of countries, import = TOTAUX import: cells give 927944788, printed 927943882 (difference -906)
  - sgt1924 p.297 (f1287) by_country 1924: sum of countries, export = TOTAUX export: cells give 582329809, printed 582353545 (difference 23736)
  - sgt1924 p.297 (f1287) by_country average 1915-1919 italy.export: printed average x 5 = sum of years: cells give 71212189, printed 71210190 (difference -1999)
  - sgt1924 p.297 (f1287) by_country average 1915-1919 usa.import: printed average x 5 = sum of years: cells give 56710620, printed 66710620 (difference 10000000)
  - sgt1924 p.297 (f1287) by_country average 1915-1919 greece.import: printed average x 5 = sum of years: cells give 3475034, printed 3468035 (difference -6999)
  - sgt1924 p.297 (f1287) by_country average 1915-1919 india.import: printed average x 5 = sum of years: cells give 14484350, printed 14484370 (difference 20)
  - sgt1924 p.297 (f1287) by_country average 1915-1919 russia.export: printed average x 5 = sum of years: cells give 137160, printed 0 (difference -137160)
  - sgt1924 p.297 (f1287) by_country average 1915-1919 Total.import: printed average x 5 = sum of years: cells give 876747115, printed 871747115 (difference -5000000)
  - sgt1924 p.297 (f1287) by_country average 1915-1924 france.export: printed average x 10 = sum of years: cells give 1634219781, printed 1684219780 (difference 49999999)
  - sgt1924 p.297 (f1287) by_country average 1915-1924 italy.export: printed average x 10 = sum of years: cells give 533663362, printed 533663660 (difference 298)
  - sgt1924 p.297 (f1287) by_country average 1915-1924 tripoli.export: printed average x 10 = sum of years: cells give 57100279, printed 57120280 (difference 20001)
  - sgt1924 p.297 (f1287) by_country average 1915-1924 usa.export: printed average x 10 = sum of years: cells give 30327738, printed 23140380 (difference -7187358)
  - sgt1924 p.297 (f1287) by_country average 1915-1924 egypt.import: printed average x 10 = sum of years: cells give 33501501, printed 33501100 (difference -401)
  - sgt1924 p.297 (f1287) by_country average 1915-1924 egypt.export: printed average x 10 = sum of years: cells give 47048929, printed 47048830 (difference -99)
  - sgt1924 p.297 (f1287) by_country average 1915-1924 morocco.export: printed average x 10 = sum of years: cells give 1718613, printed 2218610 (difference 499997)
  - sgt1924 p.297 (f1287) by_country average 1915-1924 greece.import: printed average x 10 = sum of years: cells give 8424964, printed 8417960 (difference -7004)
  - sgt1924 p.297 (f1287) by_country average 1915-1924 brazil.import: printed average x 10 = sum of years: cells give 51887307, printed 51886300 (difference -1007)
  - sgt1924 p.297 (f1287) by_country average 1915-1924 india.import: printed average x 10 = sum of years: cells give 37970108, printed 38470130 (difference 500022)
  - sgt1924 p.297 (f1287) by_country average 1915-1924 bulgaria.import: printed average x 10 = sum of years: cells give 1079562, printed 861180 (difference -218382)
  - sgt1924 p.297 (f1287) by_country average 1915-1924 norway.export: printed average x 10 = sum of years: cells give 726386, printed 726370 (difference -16)
  - sgt1924 p.297 (f1287) by_country average 1915-1924 austria.import: printed average x 10 = sum of years: cells give 16068190, printed 16068290 (difference 100)
  - sgt1924 p.297 (f1287) by_country average 1915-1924 belgium.export: printed average x 10 = sum of years: cells give 123623427, printed 116623420 (difference -7000007)
  - sgt1924 p.297 (f1287) by_country average 1915-1924 Total.import: printed average x 10 = sum of years: cells give 4835790026, printed 4830790020 (difference -5000006)
  - sgt1924 p.297 (f1287) by_country average 1920-1924 algeria.export: printed average x 5 = sum of years: cells give 115747715, printed 115747515 (difference -200)
  - sgt1924 p.297 (f1287) by_country average 1920-1924 england.export: printed average x 5 = sum of years: cells give 225427970, printed 225407970 (difference -20000)
  - sgt1924 p.297 (f1287) by_country average 1920-1924 tripoli.export: printed average x 5 = sum of years: cells give 41514843, printed 41534840 (difference 19997)
  - sgt1924 p.297 (f1287) by_country average 1920-1924 usa.export: printed average x 5 = sum of years: cells give 28517283, printed 21329930 (difference -7187353)
  - sgt1924 p.297 (f1287) by_country average 1920-1924 egypt.import: printed average x 5 = sum of years: cells give 11618746, printed 11618345 (difference -401)
  - sgt1924 p.297 (f1287) by_country average 1920-1924 morocco.export: printed average x 5 = sum of years: cells give 845695, printed 1345695 (difference 500000)
  - sgt1924 p.297 (f1287) by_country average 1920-1924 brazil.import: printed average x 5 = sum of years: cells give 35396761, printed 35399760 (difference 2999)
  - sgt1924 p.297 (f1287) by_country average 1920-1924 india.import: printed average x 5 = sum of years: cells give 23485758, printed 23985760 (difference 500002)
  - sgt1924 p.297 (f1287) by_country average 1920-1924 bulgaria.import: printed average x 5 = sum of years: cells give 1079562, printed 861185 (difference -218377)
  - sgt1924 p.297 (f1287) by_country average 1920-1924 norway.export: printed average x 5 = sum of years: cells give 569079, printed 569070 (difference -9)
  - sgt1924 p.297 (f1287) by_country average 1920-1924 austria.import: printed average x 5 = sum of years: cells give 15547498, printed 15547600 (difference 102)
  - sgt1924 p.297 (f1287) by_country average 1920-1924 russia.export: printed average x 5 = sum of years: cells give 0, printed 137160 (difference 137160)
  - sgt1924 p.297 (f1287) by_country average 1920-1924 romania.import: printed average x 5 = sum of years: cells give 37993993, printed 37493990 (difference -500003)

- Overlapping printings: 975 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: total_mismatch: 2.

  - sgt1924 p.295 1924 Tripoli (Libya) / tripoli / export / value / francs = 10101094 (total_mismatch)
  - sgt1924 p.295 1924 Egypt / egypt / import / value / francs = 1364829 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (12 printings): sgt1922 f290, sgt1922 f291, sgt1922 f292, sgt1922 f293, sgt1923 f780, sgt1923 f781, sgt1923 f782, sgt1923 f783, sgt1924 f1284, sgt1924 f1285, sgt1924 f1286, sgt1924 f1287.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
