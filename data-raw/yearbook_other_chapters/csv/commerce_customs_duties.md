# Renseignements généraux : droits de douane perçus (importation)

*General information: import duties collected, by category of products.*

Source: *Statistique générale de la Tunisie*, chapter *Commerce et navigation*, editions sgt1922, sgt1923, sgt1924. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 270, f294; sgt1923 (`bpt6k9105649x`): p. 270, f784; sgt1924 (`bpt6k9105649x`): p. 270, f1288, p. 271, f1289.

Transcriptions: `../transcribed/commerce_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_commerce.py build`.

Rows: 420. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924.

Unit: francs with centimes (current values). value_type: francs.

Selection (SPEC_ADDENDUM rule 4): each edition prints the last ten years; each year is stored once, from the latest edition printing it legibly (1913 from sgt1922, 1914 from sgt1923, 1915-1924 from sgt1924); every other printing of the same cell is compared and the differences listed below.

## Columns

- `census`: edition the value is taken from: the latest edition printing that year legibly (rule 4; see notes on the gutter)
- `table_id`: `general_f` (Renseignements généraux, f) Droits de douane perçus, importation)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: calendar year in which the duties were collected
- `product_class`: `animal`, `vegetal`, `mineral`, `manufactures` (the four classes of the customs nomenclature)
- `product_class_fr`: as printed
- `product_category`: code of the line (customs nomenclature category; see notes)
- `product_category_fr`: line as printed
- `measure`: `import_duties`
- `measure_fr`: droits de douane perçus (importation)
- `unit`: `francs`
- `value`: duties collected, francs with centimes, as printed
- `flag`: empty, `reprint_corrected` (see notes)

Import duties collected (droits de douane perçus, importation) by line of the customs nomenclature: the 32 categories of table c) (`commerce_trade_by_category`), with *Denrées coloniales* split into Sucres and Autres, *Poteries* and *Verres et cristaux*, *Meubles* and *Ouvrages en bois* printed on separate lines (35 lines). Francs with centimes; printed » stored as 0. The printed TOTAL and the three averages (*Moyenne des années*) are not stored; the TOTAL was used as a check (sum of lines). Total duties by year = sum of the stored rows.

Gutter: sgt1922 f295, the 1917 column loses its leading digits on Sucres, Autres, Tissus and the TOTAL, and on f294 the last digit of the 1916 TOTAL and of *Produits et déchets divers* (`?`); sgt1923 f785, the 1918 column is cut on every line except six short values (`?`). A year is stored from the latest edition printing it legibly (33 illegible printed cells, not compared). sgt1924 prints every year legibly.

Reprint difference: 1923 *Animaux vivants*, sgt1923 prints 33.773 and sgt1924 23.773 (both read on zoomed crops); the sgt1924 figure reduces the 1923 TOTAL gap and is stored (flag `reprint_corrected`).

Explanation of the failed checks (every cell of the failing columns re-read on native-resolution crops; the same figures in every edition printing the year): 1918, the lines sum to 20.00 less than the TOTAL (6.181.022,80; sgt1922 and sgt1924); 1922, 0.06 less than the TOTAL (17.637.371,81; all three editions); neither is located. 1923: sgt1923 lines exceed the TOTAL (24.371.783,13) by 19.005, sgt1924 (with Animaux vivants 23.773) by 9.005. The sgt1924 1920-1924 printed averages agree with the printed 1923 lines (within rounding) and the TOTAL average equals the mean of the printed TOTALs, so the residual 9.005 cannot be assigned to a line; nothing flagged.

Survey of the whole chapter: `commerce_survey.md`.

## Validation

- Checks against printed totals and identities: 27; passed: 20; failed: 7.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.271 (f295) customs_duties 1918: sum of lines = TOTAL: cells give 6181002.80, printed 6181022.80 (difference 20.00)
  - sgt1922 p.271 (f295) customs_duties 1922: sum of lines = TOTAL: cells give 17637371.75, printed 17637371.81 (difference 0.06)
  - sgt1923 p.271 (f785) customs_duties 1922: sum of lines = TOTAL: cells give 17637371.75, printed 17637371.81 (difference 0.06)
  - sgt1923 p.271 (f785) customs_duties 1923: sum of lines = TOTAL: cells give 24390788.13, printed 24371783.13 (difference -19005.00)
  - sgt1924 p.270 (f1288) customs_duties 1918: sum of lines = TOTAL: cells give 6181002.80, printed 6181022.80 (difference 20.00)
  - sgt1924 p.271 (f1289) customs_duties 1922: sum of lines = TOTAL: cells give 17637371.75, printed 17637371.81 (difference 0.06)
  - sgt1924 p.271 (f1289) customs_duties 1923: sum of lines = TOTAL: cells give 24380788.13, printed 24371783.13 (difference -9005.00)

- Overlapping printings: 597 cell comparisons with other editions printing the same cell; 1 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1923 / live_animals | sgt1923 | 33773 | sgt1924 | 23773 |

- Flagged cells: reprint_corrected: 1.

  - sgt1924 p.271 1923 animal / live_animals / import_duties / francs = 23773 (reprint_corrected)

## Image versus OCR

- Read cell by cell on the page images (6 printings): sgt1922 f294, sgt1922 f295, sgt1923 f784, sgt1923 f785, sgt1924 f1288, sgt1924 f1289.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
