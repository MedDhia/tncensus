# Renseignements généraux : classement des produits par pays de provenance et de destination (valeur en francs)

*General information: products by country group of provenance and destination (value in francs).*

Source: *Statistique générale de la Tunisie*, chapter *Commerce et navigation*, editions sgt1922, sgt1923, sgt1924. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 264, f288; sgt1923 (`bpt6k9105649x`): p. 276, f778; sgt1924 (`bpt6k9105649x`): p. 292, f1282, p. 293, f1283.

Transcriptions: `../transcribed/commerce_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_commerce.py build`.

Rows: 192. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924.

Unit: francs (current values). value_type: francs.

Selection (SPEC_ADDENDUM rule 4): each edition prints the last ten years; each year is stored once, from the latest edition printing it legibly (1913 from sgt1922, 1914 from sgt1923, 1915-1924 from sgt1924); every other printing of the same cell is compared and the differences listed below.

## Columns

- `census`: edition the value is taken from: the latest edition printing that year legibly (rule 4; see notes on the gutter)
- `table_id`: `general_d` (Renseignements généraux, d) Classement des produits par pays de provenance et de destination)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: calendar year of the trade
- `product_class`: `animal`, `vegetal`, `mineral`, `manufactures` (the four classes of the customs nomenclature)
- `product_class_fr`: as printed
- `origin_group`: `france_algeria` (France and Algeria) or `foreign_colonies` (foreign countries and French colonies): country group of provenance (imports) or destination (exports)
- `origin_group_fr`: column heading as printed
- `flow`: `import` or `export`
- `flow_fr`: as printed
- `measure`: `value`
- `measure_fr`: valeur
- `unit`: `francs`
- `value`: value in francs as printed
- `flag`: empty, `illegible` (gutter, NA) or `total_mismatch` (see notes)

For each of the four classes of products, the table splits imports and exports between two groups of countries: France and Algeria, and foreign countries with the French colonies. A Récapitulation (sum of the classes) and a TOTAL (imports + exports) close each column; they are not stored and were used as checks, together with the b) class lines (`commerce_trade_by_class`: France-Algérie + Étranger = class line of the same edition).

Gutter: the first five years are on the even view, the last five on the odd view. sgt1922 f289: the 1918 France-Algérie column loses leading digits on `mineral` export and TOTAL (`?`); sgt1923 f779: the 1919 France-Algérie column is cut on every line (all `?`); these are stored from the latest legible printing (9 illegible printed cells, not compared).

Misprints (printed values kept, flagged `total_mismatch`): (i) 1915 `manufactures` import, Étranger 19.776.907 (all editions): the classes exceed the Récapitulation by 200 and the c) categories give 45.087.412 for the class, so this cell (not France-Algérie) carries the 200-franc error already seen in the b) class line. (ii) 1918 `animal` import, France-Algérie 5.027.593 (all editions): the Récapitulation is 1.000.000 higher than the classes and the b) line (8.036.067) implies about 6.030.000. (iii) 1918 `manufactures` import, Étranger 63.477.415 (all editions): the b) line (112.551.419) less France-Algérie gives 63.747.417 and the Récapitulation 63.747.415 (transposed digits). (iv) 1920 `manufactures` import, France-Algérie: sgt1922 prints 241.075.431, which agrees with the Récapitulation and the b) line; sgt1923 and sgt1924 print 241.507.431 (a reprint error, 432.000 too high); the stored value comes from sgt1924 under rule 4 and carries the flag, the correct figure being the sgt1922 printing. (v) 1923 `manufactures` import (sgt1923, sgt1924): France-Algérie 452.548.838, 6.000.000 below the Récapitulation and the b) line (implying 458.548.838), and Étranger 95.088.696, 90 above what the Récapitulation and the b) line imply.

Explanation of the other failed checks (every cell re-read on a native-resolution crop): 1918 (all editions) a residual of 3.000 on `animal` import and of 2 between `mineral` and `manufactures` import against the b) lines, part of misprints (ii)-(iii), whose exact correct figures the totals do not fix. 1918 Étranger TOTAL: sgt1922 prints 171.239.679 (= Récapitulation import + export), sgt1923-1924 171.239.697 (reprint transposition; totals not stored). 1924 (sgt1924): the Récapitulation (676.369.187 + 251.574.695 import, 294.041.360 + 288.312.185 export) agrees exactly with table a) and the c) TOTAUX, but the class cells exceed it by 10 (France-Algérie import), 199.910 (Étranger import) and fall 4 short (Étranger export); the France-Algérie TOTAL 970.408.547 is 2.000 below its Récapitulation. The 1924 b) class lines are themselves inconsistent with table a) (see `commerce_trade_by_class`); the c) categories of the same edition agree with these cells on `animal` export (54.347.670) and come close on `manufactures` (import 604.302.406 against 604.302.386, export 44.630.178 against 44.640.178), so the faulty cells cannot be identified; nothing is flagged. sgt1925 reprints 1924.

Survey of the whole chapter: `commerce_survey.md`.

## Validation

- Checks against printed totals and identities: 406; passed: 366; failed: 40.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.264 (f288) by_origin_group 1915.E: classes, import = Récapitulation: cells give 45614812, printed 45614612 (difference -200)
  - sgt1922 p.265 (f289) by_origin_group 1918.F: classes, import = Récapitulation: cells give 74609140, printed 75609140 (difference 1000000)
  - sgt1922 p.265 (f289) by_origin_group 1918.E: classes, import = Récapitulation: cells give 131560448, printed 131833448 (difference 273000)
  - sgt1922 p.265 (f289) by_origin_group 1918: animal import, France-Algérie + Étranger = b) class line: cells give 7033067, printed 8036067 (difference 1003000)
  - sgt1922 p.265 (f289) by_origin_group 1918: mineral import, France-Algérie + Étranger = b) class line: cells give 34285833, printed 34285831 (difference -2)
  - sgt1922 p.265 (f289) by_origin_group 1918: manufactures import, France-Algérie + Étranger = b) class line: cells give 112281417, printed 112551419 (difference 270002)
  - sgt1923 p.276 (f778) by_origin_group 1915.E: classes, import = Récapitulation: cells give 45614812, printed 45614612 (difference -200)
  - sgt1923 p.276 (f778) by_origin_group 1918.F: classes, import = Récapitulation: cells give 74609140, printed 75609140 (difference 1000000)
  - sgt1923 p.276 (f778) by_origin_group 1918.E: classes, import = Récapitulation: cells give 131560448, printed 131833448 (difference 273000)
  - sgt1923 p.276 (f778) by_origin_group 1918.E: Récapitulation import + export = Total: cells give 171239679, printed 171239697 (difference 18)
  - sgt1923 p.276 (f778) by_origin_group 1918: animal import, France-Algérie + Étranger = b) class line: cells give 7033067, printed 8036067 (difference 1003000)
  - sgt1923 p.276 (f778) by_origin_group 1918: mineral import, France-Algérie + Étranger = b) class line: cells give 34285833, printed 34285831 (difference -2)
  - sgt1923 p.276 (f778) by_origin_group 1918: manufactures import, France-Algérie + Étranger = b) class line: cells give 112281417, printed 112551419 (difference 270002)
  - sgt1923 p.277 (f779) by_origin_group 1920.F: classes, import = Récapitulation: cells give 329178447, printed 328746447 (difference -432000)
  - sgt1923 p.277 (f779) by_origin_group 1923.F: classes, import = Récapitulation: cells give 572476490, printed 578476490 (difference 6000000)
  - sgt1923 p.277 (f779) by_origin_group 1923.E: classes, import = Récapitulation: cells give 238982820, printed 238982730 (difference -90)
  - sgt1923 p.277 (f779) by_origin_group 1920: manufactures import, France-Algérie + Étranger = b) class line: cells give 401492263, printed 401060263 (difference -432000)
  - sgt1923 p.277 (f779) by_origin_group 1923: manufactures import, France-Algérie + Étranger = b) class line: cells give 547637534, printed 553637444 (difference 5999910)
  - sgt1924 p.292 (f1282) by_origin_group 1915.E: classes, import = Récapitulation: cells give 45614812, printed 45614612 (difference -200)
  - sgt1924 p.292 (f1282) by_origin_group 1918.F: classes, import = Récapitulation: cells give 74609140, printed 75609140 (difference 1000000)
  - sgt1924 p.292 (f1282) by_origin_group 1918.E: classes, import = Récapitulation: cells give 131560448, printed 131833448 (difference 273000)
  - sgt1924 p.292 (f1282) by_origin_group 1918.E: Récapitulation import + export = Total: cells give 171239679, printed 171239697 (difference 18)
  - sgt1924 p.292 (f1282) by_origin_group 1918: animal import, France-Algérie + Étranger = b) class line: cells give 7033067, printed 8036067 (difference 1003000)
  - sgt1924 p.292 (f1282) by_origin_group 1918: mineral import, France-Algérie + Étranger = b) class line: cells give 34285833, printed 34285831 (difference -2)
  - sgt1924 p.292 (f1282) by_origin_group 1918: manufactures import, France-Algérie + Étranger = b) class line: cells give 112281417, printed 112551419 (difference 270002)
  - sgt1924 p.293 (f1283) by_origin_group 1920.F: classes, import = Récapitulation: cells give 329178447, printed 328746447 (difference -432000)
  - sgt1924 p.293 (f1283) by_origin_group 1923.F: classes, import = Récapitulation: cells give 572476490, printed 578476490 (difference 6000000)
  - sgt1924 p.293 (f1283) by_origin_group 1923.E: classes, import = Récapitulation: cells give 238982820, printed 238982730 (difference -90)
  - sgt1924 p.293 (f1283) by_origin_group 1924.F: classes, import = Récapitulation: cells give 676369197, printed 676369187 (difference -10)
  - sgt1924 p.293 (f1283) by_origin_group 1924.F: Récapitulation import + export = Total: cells give 970410547, printed 970408547 (difference -2000)
  - sgt1924 p.293 (f1283) by_origin_group 1924.E: classes, import = Récapitulation: cells give 251774605, printed 251574695 (difference -199910)
  - sgt1924 p.293 (f1283) by_origin_group 1924.E: classes, export = Récapitulation: cells give 288312181, printed 288312185 (difference 4)
  - sgt1924 p.293 (f1283) by_origin_group 1920: manufactures import, France-Algérie + Étranger = b) class line: cells give 401492263, printed 401060263 (difference -432000)
  - sgt1924 p.293 (f1283) by_origin_group 1923: manufactures import, France-Algérie + Étranger = b) class line: cells give 547637534, printed 553637444 (difference 5999910)
  - sgt1924 p.293 (f1283) by_origin_group 1924: animal import, France-Algérie + Étranger = b) class line: cells give 39641922, printed 39541922 (difference -100000)
  - sgt1924 p.293 (f1283) by_origin_group 1924: animal export, France-Algérie + Étranger = b) class line: cells give 54347670, printed 54347560 (difference -110)
  - sgt1924 p.293 (f1283) by_origin_group 1924: vegetal import, France-Algérie + Étranger = b) class line: cells give 190896469, printed 190796469 (difference -100000)
  - sgt1924 p.293 (f1283) by_origin_group 1924: vegetal export, France-Algérie + Étranger = b) class line: cells give 225896478, printed 225896482 (difference 4)
  - sgt1924 p.293 (f1283) by_origin_group 1924: manufactures import, France-Algérie + Étranger = b) class line: cells give 604302386, printed 606302506 (difference 2000120)
  - sgt1924 p.293 (f1283) by_origin_group 1924: manufactures export, France-Algérie + Étranger = b) class line: cells give 44640178, printed 44739278 (difference 99100)

- Overlapping printings: 279 cell comparisons with other editions printing the same cell; 1 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1920 / manufactures / france_algeria / import | sgt1922 | 241075431 | sgt1924 | 241507431 |

- Flagged cells: total_mismatch: 6.

  - sgt1924 p.292 1915 manufactures / foreign_colonies / import / value / francs = 19776907 (total_mismatch)
  - sgt1924 p.292 1918 animal / france_algeria / import / value / francs = 5027593 (total_mismatch)
  - sgt1924 p.292 1918 manufactures / foreign_colonies / import / value / francs = 63477415 (total_mismatch)
  - sgt1924 p.293 1920 manufactures / france_algeria / import / value / francs = 241507431 (total_mismatch)
  - sgt1924 p.293 1923 manufactures / foreign_colonies / import / value / francs = 95088696 (total_mismatch)
  - sgt1924 p.293 1923 manufactures / france_algeria / import / value / francs = 452548838 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (6 printings): sgt1922 f288, sgt1922 f289, sgt1923 f778, sgt1923 f779, sgt1924 f1282, sgt1924 f1283.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
