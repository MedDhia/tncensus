# Renseignements généraux : résumé des importations et des exportations par classe de produits (valeur en francs)

*General information: imports and exports by class of products (value in francs).*

Source: *Statistique générale de la Tunisie*, chapter *Commerce et navigation*, editions sgt1922, sgt1923, sgt1924. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 258, f282; sgt1923 (`bpt6k9105649x`): p. 270, f772; sgt1924 (`bpt6k9105649x`): p. 286, f1276, p. 287, f1277.

Transcriptions: `../transcribed/commerce_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_commerce.py build`.

Rows: 96. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924.

Unit: francs (current values; see footnote on valuation from 1920). value_type: francs.

Selection (SPEC_ADDENDUM rule 4): each edition prints the last ten years; each year is stored once, from the latest edition printing it (1913 from sgt1922, 1914 from sgt1923, 1915-1924 from sgt1924); every other printing of the same cell is compared and the differences listed below.

## Columns

- `census`: edition the value is taken from: the latest edition printing that year (rule 4)
- `table_id`: `general_b` (Renseignements généraux, b) Résumé ... par classe de produits)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: calendar year of the trade
- `product_class`: `animal`, `vegetal`, `mineral`, `manufactures` (the four classes of the customs nomenclature)
- `product_class_fr`: as printed
- `flow`: `import` or `export`
- `flow_fr`: as printed
- `measure`: `value`
- `measure_fr`: valeur
- `unit`: `francs`
- `value`: value in francs as printed
- `flag`: empty, or `total_mismatch` (see notes)

The printed a) table *Mouvement global des importations et des exportations* (importation, exportation, total) is not stored: its import and export lines equal the sums of the four classes and are used as a check (the b) table's class totals, import + export, likewise). Total trade by year = sum of the stored rows.

Footnote (1), printed under the table in every edition (translated): until 1919, to make comparisons with earlier years easier, the price increases resulting from the war were not taken into account in determining values. Since 1920 these increases are included, the value of imports and exports being set by a permanent commission on the basis of valuation rates equivalent to those of Algeria.

1915: the class totals of `vegetal` (91.463.545) and `manufactures` (53.968.433) do not agree with their import and export lines (37.546.533 + 53.877.012 = 91.423.545; 45.087.612 + 8.921.021 = 54.008.633), and the four import lines sum to 200 francs more than the a) Mouvement global import (107.246.504). The c) category table settles it: its vegetal categories sum to 37.546.533 (the printed vegetal import is right, so the vegetal Total is misprinted, 40.000 too high) and its manufactured categories sum to 45.087.412, which with the other three classes gives exactly 107.246.504. The manufactures import cell (45.087.612) is therefore misprinted by 200 francs (flagged `total_mismatch`), and the manufactures Total is a second misprint (40.000 too low; totals are not stored). All three editions print the same figures; re-read on zoomed crops of f1276 (sgt1924) and on f282, f772.

Explanation of the failed checks. (i) Nine failures are the 1915 misprints described above (vegetal Total, manufactures import and Total), repeated in each of the three editions; re-read on native-resolution crops of f282, f772 and f1276. (ii) sgt1924, 1924: the four classes sum to 929.943.922 (imports) and 582.452.535 (exports), while the a) table prints 927.943.882 and 582.353.545 (differences 2.000.040 and 98.990). Every class line agrees with its class total, so the b) table is internally consistent; the a) table and the c) category TOTAUX agree with each other, so b) was probably set from a different (provisional) state of the 1924 returns. Every 1924 cell of f1277 was re-read on a zoomed native-resolution crop and stands as transcribed. The c) category table of the same edition differs from b) on manufactures import (604.302.406), manufactures export (44.630.178) and animal export (54.347.670), but the differences (2.000.100, 109.100, -110) do not equal the a) discrepancies, so no single b) cell can be identified as the misprint and nothing is flagged. The 1924 figures are reprinted in sgt1925, which will allow a comparison when that edition is added.

Survey of the whole chapter: `commerce_survey.md`.

## Validation

- Checks against printed totals and identities: 210; passed: 199; failed: 11.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.258 (f282) by_class 1915: vegetal Total = import + export: cells give 91423545, printed 91463545 (difference 40000)
  - sgt1922 p.258 (f282) by_class 1915: manufactures Total = import + export: cells give 54008633, printed 53968433 (difference -40200)
  - sgt1922 p.258 (f282) by_class 1915: sum of classes, import = a) Mouvement global import: cells give 107246704, printed 107246504 (difference -200)
  - sgt1923 p.270 (f772) by_class 1915: vegetal Total = import + export: cells give 91423545, printed 91463545 (difference 40000)
  - sgt1923 p.270 (f772) by_class 1915: manufactures Total = import + export: cells give 54008633, printed 53968433 (difference -40200)
  - sgt1923 p.270 (f772) by_class 1915: sum of classes, import = a) Mouvement global import: cells give 107246704, printed 107246504 (difference -200)
  - sgt1924 p.286 (f1276) by_class 1915: vegetal Total = import + export: cells give 91423545, printed 91463545 (difference 40000)
  - sgt1924 p.286 (f1276) by_class 1915: manufactures Total = import + export: cells give 54008633, printed 53968433 (difference -40200)
  - sgt1924 p.286 (f1276) by_class 1915: sum of classes, import = a) Mouvement global import: cells give 107246704, printed 107246504 (difference -200)
  - sgt1924 p.287 (f1277) by_class 1924: sum of classes, import = a) Mouvement global import: cells give 929943922, printed 927943882 (difference -2000040)
  - sgt1924 p.287 (f1277) by_class 1924: sum of classes, export = a) Mouvement global export: cells give 582452535, printed 582353545 (difference -98990)

- Overlapping printings: 144 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: total_mismatch: 1.

  - sgt1924 p.286 1915 manufactures / import / value / francs = 45087612 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (6 printings): sgt1922 f282, sgt1922 f283, sgt1923 f772, sgt1923 f773, sgt1924 f1276, sgt1924 f1277.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
