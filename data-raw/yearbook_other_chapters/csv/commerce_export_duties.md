# Droits de sortie perçus (exportation)

*Export duties collected, by product.*

Source: *Statistique générale de la Tunisie*, chapter *Commerce et navigation*, editions sgt1922, sgt1923, sgt1924. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 272, f296; sgt1923 (`bpt6k9105649x`): p. 272, f786; sgt1924 (`bpt6k9105649x`): p. 272, f1290, p. 273, f1291.

Transcriptions: `../transcribed/commerce_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_commerce.py build`.

Rows: 452. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924.

Unit: francs with centimes (current values). value_type: francs.

Selection (SPEC_ADDENDUM rule 4): each edition prints the last ten years; each year is stored once, from the latest edition printing it legibly (1913 from sgt1922, 1914 from sgt1923, 1915-1924 from sgt1924); every other printing of the same cell is compared and the differences listed below.

## Columns

- `census`: edition the value is taken from: the latest edition printing that year legibly (rule 4; see notes on the gutter)
- `table_id`: `export_duties` (Droits de sortie perçus, exportation)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: calendar year in which the duties were collected
- `product_group_fr`: group heading as printed (empty when the line stands alone)
- `product`: code of the line
- `product_fr`: line as printed (in the edition the value is taken from)
- `measure`: `export_duties`
- `measure_fr`: droits de sortie perçus (exportation)
- `unit`: `francs`
- `value`: duties collected, francs with centimes, as printed
- `flag`: empty

Export duties collected (droits de sortie perçus, exportation) by product line, including the duties on parcel post (Colis postaux) and the exit tax on young horses. Francs with centimes; printed » stored as 0. The TOTAL and the three averages (*Moyenne des années*) are not stored; the TOTAL was used as a check. Total export duties by year = sum of the stored rows.

Lines: sgt1922 and sgt1923 print 26 lines; sgt1924 prints 40, adding 14 lines (poultry, salted and canned meat, eggs, condensed milk pure and sweetened, potatoes, pulses, fresh and dried fruit, charcoal, other common wood, fresh vegetables, fodder) that are » in every year before 1924, and renames *Beurres et fromages* to *Beurre, fromages et graisses*. Under rule 4 every year 1915-1924 comes from sgt1924, so the added lines carry 0 (as printed) for 1915-1923; 1913 and 1914 have only the 26 lines (the added lines are absent, not zero). The animal lines refer to the decrees of 12 June and 28 August 1920 (duties on beasts of burden exported to foreign countries).

Gutter: sgt1922 f296, the last digits of the 1916 TOTAL (`?`); sgt1923 f786, the 1917 column loses its centimes on every non-zero line (`?`), and f787 the 1918 column loses leading digits on five lines and the TOTAL (`?`). Illegible printings (20 cells) are not compared; sgt1924 is legible throughout.

Explanation of the failed checks (cells re-read on native-resolution crops; the same figures in every edition printing the year): 1918, the lines exceed the TOTAL (707.645,24) by 0,05; 1922, they fall 3,00 short of the TOTAL (3.412.803,27); neither is located. 1924 (sgt1924 only): the lines sum to 2.056.475,22 against a TOTAL of 2.056.675,96 (200,74 short); the printed 1920-1924 averages are themselves inconsistent on several lines (e.g. camels, large hides, dried fruit, fodder) and do not locate the gap; nothing flagged. sgt1925 reprints 1924.

Survey of the whole chapter: `commerce_survey.md`.

## Validation

- Checks against printed totals and identities: 27; passed: 21; failed: 6.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.273 (f297) export_duties 1918: sum of lines = TOTAL: cells give 707645.29, printed 707645.24 (difference -0.05)
  - sgt1922 p.273 (f297) export_duties 1922: sum of lines = TOTAL: cells give 3412800.27, printed 3412803.27 (difference 3.00)
  - sgt1923 p.273 (f787) export_duties 1922: sum of lines = TOTAL: cells give 3412800.27, printed 3412803.27 (difference 3.00)
  - sgt1924 p.272 (f1290) export_duties 1918: sum of lines = TOTAL: cells give 707645.29, printed 707645.24 (difference -0.05)
  - sgt1924 p.273 (f1291) export_duties 1922: sum of lines = TOTAL: cells give 3412800.27, printed 3412803.27 (difference 3.00)
  - sgt1924 p.273 (f1291) export_duties 1924: sum of lines = TOTAL: cells give 2056475.22, printed 2056675.96 (difference 200.74)

- Overlapping printings: 448 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (6 printings): sgt1922 f296, sgt1922 f297, sgt1923 f786, sgt1923 f787, sgt1924 f1290, sgt1924 f1291.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
