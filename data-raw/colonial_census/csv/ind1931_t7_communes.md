# Tableau VII — Population musulmane et israélite des localités érigées en Commune

*Table VII: Muslim and Jewish population of the localities constituted as communes (municipalities)*

Source: *Dénombrement de la population civile indigène (musulmane et israélite) en Tunisie au 22 mars 1931*, Régence de Tunis, Direction générale de l'intérieur, Tunis, Impr. J. Aloccio, 1932. Gallica ark `bpt6k994559s` (Source gallica.bnf.fr / Bibliothèque nationale de France).

Pages: pp. 113–114, views 64–65. Table id: `VII`. Rows: 116.

## Content

One row per commune × religion (58 communes). `caidat` as printed in the table's last column; empty where the table prints '—' (Bardo, Monastir). The OCR has no commune names on p.113, so names were read from the images; the printed total column is not stored but was checked (Muslim + Jewish = total) and equals the 1931 column of Annex VII for every commune.

Columns: census, table_id, source_page, gallica_view, commune, caidat, religion, religion_fr, value, flag.

## Notes and printed footnotes

Tébourba is printed 3.107 + 42 = 3.128 (should be 3.149); printed values kept, flagged `total_mismatch`; Annex VII also gives 3.128 for 1931. Saint-Germain is printed '»' in all columns.

## Method

Numbers come from Gallica's word OCR (via `ocr.py`), assigned to printed columns by right edge,
with page images used to correct the OCR. Script: `extract_ind1931_other.py`. Printed `»` = 0.
Printed subtotal, total, `A reporter` and `Report` lines are not stored; they were used for validation.
`flag = ocr_corrected` marks a cell where the OCR value was missing or wrong and the value was read
from the page image (an empty OCR cell is set to 0 only where the image shows `»` and the printed
row totals then balance; every such cell was confirmed on the image).

## Validation

- `row_checks`: 58
- `row_checks_passed`: 57
- `cells_corrected_from_image`: 2
- `printed_inconsistencies_kept`: 1

Flags: {'ocr_corrected': 1, 'total_mismatch': 2}.
