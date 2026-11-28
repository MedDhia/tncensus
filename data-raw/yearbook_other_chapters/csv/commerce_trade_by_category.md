# Renseignements généraux : résumé des importations et des exportations par catégorie de produits (valeur en francs)

*General information: imports and exports by category of products (value in francs).*

Source: *Statistique générale de la Tunisie*, chapter *Commerce et navigation*, editions sgt1922, sgt1923, sgt1924. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 260, f284, p. 261, f285, p. 262, f286, p. 263, f287; sgt1923 (`bpt6k9105649x`): p. 272, f774, p. 273, f775, p. 274, f776, p. 275, f777; sgt1924 (`bpt6k9105649x`): p. 288, f1278, p. 289, f1279, p. 290, f1280, p. 291, f1281.

Transcriptions: `../transcribed/commerce_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_commerce.py build`.

Rows: 768. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924.

Unit: francs (current values). value_type: francs.

Selection (SPEC_ADDENDUM rule 4): each edition prints the last ten years; each year is stored once, from the latest edition printing it legibly (1913 from sgt1922, 1914 from sgt1923, 1915-1924 from sgt1924); every other printing of the same cell is compared and the differences listed below.

## Columns

- `census`: edition the value is taken from: the latest edition printing that year legibly (rule 4; see notes on the gutter)
- `table_id`: `general_c` (Renseignements généraux, c) Résumé ... par catégorie de produits)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: calendar year of the trade
- `product_class`: `animal`, `vegetal`, `mineral`, `manufactures` (the four classes of the customs nomenclature)
- `product_class_fr`: as printed
- `product_category`: code of the category of the customs nomenclature (32 categories)
- `product_category_fr`: category as printed
- `flow`: `import` or `export`
- `flow_fr`: as printed
- `measure`: `value`
- `measure_fr`: valeur
- `unit`: `francs`
- `value`: value in francs as printed
- `flag`: empty, or `total_mismatch` (see notes)

The table prints, for each of the 32 categories of the customs nomenclature (5 animal, 10 vegetal, 2 mineral, 15 manufactured), the import and export values of the last ten years, followed on the odd view by three five-year averages (*Moyenne des années*). The averages and the TOTAUX lines are not stored; they were used as checks. The sum of the categories of each class is checked against the class line of table b) (`commerce_trade_by_class`) of the same edition. The same footnote on valuation (war price rises taken into account from 1920 only) applies.

Gutter. Each spread prints the first four years on the even view and the rest on the odd view; the fourth year sits against the binding. sgt1923: the 1917 column (f774, f776) loses part of its last digit but every value is readable; the 1918 column (f775, f777) loses the leading digit(s) on 25 category lines and both TOTAUX, transcribed `?` (a value is transcribed only where its first digit is wholly visible). sgt1924: the 1918 column (f1278, f1280) loses its last three digits on every line (all `?` except `arms` export, printed », i.e. nil), and the 1919 column of f1279 loses the leading digit on 11 lines (`?`). A year is stored from the latest edition printing it legibly: 1918 from sgt1923 where legible (`arms` export from sgt1924), otherwise sgt1922; 1919 vegetal/mineral lines concerned from sgt1923. Illegible printings are not compared (101 printed cells).

sgt1924 f1280: the two lines of *Produits chimiques* are labelled Exportation / Importation (inverted relative to every other category and to the other editions); the figures are in the usual order (import first, identical to sgt1922-1923 for the years in common, and the class checks pass), so they are stored as import / export.

Misprints identified (printed values kept, flagged `total_mismatch`): (i) `beverages` import 1918, printed 2.604.952 in sgt1922 and sgt1923: the vegetal class line (52.569.271) and TOTAUX (207.442.588) are 1.000.000 lower than the categories, and the printed 1918-1922 average (3.419.698) implies 1.604.952. (ii) `vegetal_misc` export 1919, printed 2.780.995 in all three editions: the class line and TOTAUX are 9.000 higher and the 1918-1922 average (3.746.430) implies 2.789.995. (iii) `pottery_glass` export 1916, printed 140.527 in all three editions: the manufactures line and TOTAUX are 36.000 lower, and the 1913-1917 average (148.564) implies 104.527. (iv) `yarns` export 1918, printed 36.258 (sgt1922, sgt1923): the manufactures line and TOTAUX are 6.000 lower and the 1918-1922 average (368.325) implies 30.258. (i) is illegible in the 1918 gutter column of both sgt1923 and sgt1924 (the leading digit, which carries the error, is hidden), so the stored value comes from sgt1922; (iv) is legible in sgt1923 and stored from it; both carry the flag.

The sgt1923 and sgt1924 lines of this table were re-typed in full from the page images (f774-777, f1278-1281), independently of the sgt1922 transcription; every legible cell agrees with the earlier transcription, the only changes being legibility judgments in the gutter columns (sgt1923 1918: eight cells whose leading digit is only partly visible now `?`; sgt1924 1918 `arms` export now read as nil).

Explanation of the other failed checks (each cell re-read on a native-resolution crop): 1913 export (sgt1922): the categories sum to 300 francs less than TOTAUX and the manufactures line (178.663.605 and 12.717.715, both agreeing with tables a) and b)); the averages do not single out a cell, nothing flagged. 1915 manufactures import (all editions): the categories give 45.087.412 against the b) line 45.087.612; TOTAUX (107.246.504) agrees with the categories, so the 200-franc error is in table b) (see `commerce_trade_by_class`, where this cell is already flagged). 1923 animal import (sgt1923, sgt1924): categories 2.000 below the b) class line and TOTAUX; the sgt1923 1919-1923 average of `live_animals` import (11.877.863) implies 16.934.116 for the printed 16.932.116, but the sgt1924 1920-1924 average (12.637.641) agrees with the printed cell, so nothing is flagged. 1924 (sgt1924): the categories sum to 927.943.822 (import) and 582.343.545 (export) against TOTAUX 927.943.882 and 582.353.545 (differences 60 and 10.000); the averages locate no cell. The b) class lines for 1924 disagree much more (manufactures import 606.302.506 against 604.302.406 here, export 44.739.278 against 44.630.178, animal export 54.347.560 against 54.347.670): TOTAUX of this table agree with table a), so the 1924 errors are mostly in table b). Comparison with sgt1925 will settle these when that edition is added.

Printed averages also disagree, without any failing total, for `fibres` import 1913-1917 (sgt1922: 222.643 printed, cells give 262.644) and `colonial_goods` export 1918-1922 (1.019.121 printed, cells give 1.018.521): averages are not stored and were not used to change any cell.

Survey of the whole chapter: `commerce_survey.md`.

## Validation

- Checks against printed totals and identities: 274; passed: 246; failed: 28.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.262 (f286) by_category 1913: sum of categories, export = TOTAUX export: cells give 178663305, printed 178663605 (difference 300)
  - sgt1922 p.262 (f286) by_category 1913: categories of class manufactures, export = b) class line: cells give 12717415, printed 12717715 (difference 300)
  - sgt1922 p.262 (f286) by_category 1915: categories of class manufactures, import = b) class line: cells give 45087412, printed 45087612 (difference 200)
  - sgt1922 p.262 (f286) by_category 1916: sum of categories, export = TOTAUX export: cells give 118830946, printed 118794946 (difference -36000)
  - sgt1922 p.262 (f286) by_category 1916: categories of class manufactures, export = b) class line: cells give 11672288, printed 11636288 (difference -36000)
  - sgt1922 p.263 (f287) by_category 1918: sum of categories, import = TOTAUX import: cells give 208442588, printed 207442588 (difference -1000000)
  - sgt1922 p.263 (f287) by_category 1918: categories of class vegetal, import = b) class line: cells give 53569271, printed 52569271 (difference -1000000)
  - sgt1922 p.263 (f287) by_category 1918: sum of categories, export = TOTAUX export: cells give 129554206, printed 129548206 (difference -6000)
  - sgt1922 p.263 (f287) by_category 1918: categories of class manufactures, export = b) class line: cells give 17350214, printed 17344214 (difference -6000)
  - sgt1922 p.263 (f287) by_category 1919: sum of categories, export = TOTAUX export: cells give 202019871, printed 202028871 (difference 9000)
  - sgt1922 p.263 (f287) by_category 1919: categories of class vegetal, export = b) class line: cells give 122514705, printed 122523705 (difference 9000)
  - sgt1923 p.274 (f776) by_category 1915: categories of class manufactures, import = b) class line: cells give 45087412, printed 45087612 (difference 200)
  - sgt1923 p.274 (f776) by_category 1916: sum of categories, export = TOTAUX export: cells give 118830946, printed 118794946 (difference -36000)
  - sgt1923 p.274 (f776) by_category 1916: categories of class manufactures, export = b) class line: cells give 11672288, printed 11636288 (difference -36000)
  - sgt1923 p.275 (f777) by_category 1919: sum of categories, export = TOTAUX export: cells give 202019871, printed 202028871 (difference 9000)
  - sgt1923 p.275 (f777) by_category 1919: categories of class vegetal, export = b) class line: cells give 122514705, printed 122523705 (difference 9000)
  - sgt1923 p.275 (f777) by_category 1923: sum of categories, import = TOTAUX import: cells give 817457220, printed 817459220 (difference 2000)
  - sgt1923 p.275 (f777) by_category 1923: categories of class animal, import = b) class line: cells give 46245152, printed 46247152 (difference 2000)
  - sgt1924 p.290 (f1280) by_category 1915: categories of class manufactures, import = b) class line: cells give 45087412, printed 45087612 (difference 200)
  - sgt1924 p.290 (f1280) by_category 1916: sum of categories, export = TOTAUX export: cells give 118830946, printed 118794946 (difference -36000)
  - sgt1924 p.290 (f1280) by_category 1916: categories of class manufactures, export = b) class line: cells give 11672288, printed 11636288 (difference -36000)
  - sgt1924 p.291 (f1281) by_category 1923: sum of categories, import = TOTAUX import: cells give 817457220, printed 817459220 (difference 2000)
  - sgt1924 p.291 (f1281) by_category 1923: categories of class animal, import = b) class line: cells give 46245152, printed 46247152 (difference 2000)
  - sgt1924 p.291 (f1281) by_category 1924: sum of categories, import = TOTAUX import: cells give 927943822, printed 927943882 (difference 60)
  - sgt1924 p.291 (f1281) by_category 1924: categories of class manufactures, import = b) class line: cells give 604302406, printed 606302506 (difference 2000100)
  - sgt1924 p.291 (f1281) by_category 1924: sum of categories, export = TOTAUX export: cells give 582343545, printed 582353545 (difference 10000)
  - sgt1924 p.291 (f1281) by_category 1924: categories of class animal, export = b) class line: cells give 54347670, printed 54347560 (difference -110)
  - sgt1924 p.291 (f1281) by_category 1924: categories of class manufactures, export = b) class line: cells give 44630178, printed 44739278 (difference 109100)

- Overlapping printings: 1051 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: total_mismatch: 4.

  - sgt1924 p.290 1916 manufactures / pottery_glass / export / value / francs = 140527 (total_mismatch)
  - sgt1922 p.261 1918 vegetal / beverages / import / value / francs = 2604952 (total_mismatch)
  - sgt1923 p.275 1918 manufactures / yarns / export / value / francs = 36258 (total_mismatch)
  - sgt1923 p.273 1919 vegetal / vegetal_misc / export / value / francs = 2780995 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (12 printings): sgt1922 f284, sgt1922 f285, sgt1922 f286, sgt1922 f287, sgt1923 f774, sgt1923 f775, sgt1923 f776, sgt1923 f777, sgt1924 f1278, sgt1924 f1279, sgt1924 f1280, sgt1924 f1281.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
