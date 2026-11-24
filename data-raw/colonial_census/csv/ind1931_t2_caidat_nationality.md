# Tableau II — État de la population indigène par Caïdats

*Table II: indigenous population by caidat, by religion and nationality*

Source: *Dénombrement de la population civile indigène (musulmane et israélite) en Tunisie au 22 mars 1931*, Régence de Tunis, Direction générale de l'intérieur, Tunis, Impr. J. Aloccio, 1932. Gallica ark `bpt6k994559s` (Source gallica.bnf.fr / Bibliothèque nationale de France).

Pages: pp. 8–11, views 9–10. Table id: `II`. Rows: 518.

## Content

One row per caidat × religion × nationality (37 caidats). Unit: persons.

Columns: census, table_id, source_page, gallica_view, caidat, religion, religion_fr, nationality, nationality_fr, value, flag.

## Method

Numbers come from Gallica's word OCR (via `ocr.py`), assigned to printed columns by right edge,
with page images used to correct the OCR. Script: `extract_ind1931_other.py`. Printed `»` = 0.
Printed subtotal, total, `A reporter` and `Report` lines are not stored; they were used for validation.
`flag = ocr_corrected` marks a cell where the OCR value was missing or wrong and the value was read
from the page image (an empty OCR cell is set to 0 only where the image shows `»` and the printed
row totals then balance; every such cell was confirmed on the image).

## Validation

- `row_checks`: 37
- `row_checks_passed`: 37
- `empty_ocr_cells_filled_0`: 6
- `cells_corrected_from_image`: 2
- `carry_forward_checks`: 1
- `carry_forward_passed`: 1
- `column_total_checks`: 17
- `column_total_passed`: 17

Flags: {'ocr_corrected': 8}.
