# Annexe au Tableau VII — Statistique comparée des dénombrements de 1921, 1926 et 1931 concernant la population indigène des localités érigées en commune

*Annex to Table VII: indigenous population of the communes at the 1921, 1926 and 1931 censuses*

Source: *Dénombrement de la population civile indigène (musulmane et israélite) en Tunisie au 22 mars 1931*, Régence de Tunis, Direction générale de l'intérieur, Tunis, Impr. J. Aloccio, 1932. Gallica ark `bpt6k994559s` (Source gallica.bnf.fr / Bibliothèque nationale de France).

Pages: pp. 115–116, views 66–67. Table id: `VII_annex`. Rows: 174.

## Content

One row per commune × census year (total indigenous population). Names spelled as printed in the annex (e.g. 'Ariana', 'Fériana', 'Kalaâ-Kébira'), in the same order as Table VII. 1931 values equal the Table VII totals for all 58 communes; 1921 and 1926 values have no printed total and were compared line by line with the page images. '»' printed for a year (e.g. El-Djem, Hadjeb-El-Aïoun, Ksour-Essaf in 1921; Sbeïtla in 1921 and 1926; Saint-Germain in 1921 and 1931) is stored as 0 per the spec; it likely means the locality was not a commune or not counted separately that year.

Columns: census, table_id, source_page, gallica_view, commune, census_year, value, flag.

## Method

Numbers come from Gallica's word OCR (via `ocr.py`), assigned to printed columns by right edge,
with page images used to correct the OCR. Script: `extract_ind1931_other.py`. Printed `»` = 0.
Printed subtotal, total, `A reporter` and `Report` lines are not stored; they were used for validation.
`flag = ocr_corrected` marks a cell where the OCR value was missing or wrong and the value was read
from the page image (an empty OCR cell is set to 0 only where the image shows `»` and the printed
row totals then balance; every such cell was confirmed on the image).

## Validation

- `cells_corrected_from_image`: 7
- `crosscheck_1931_vs_table_VII`: 58
- `crosscheck_1931_vs_table_VII_passed`: 58
- `rows_compared_with_image`: 58

Flags: {'ocr_corrected': 7}.
