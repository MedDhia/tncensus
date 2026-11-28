# Tableau V — Répartition de la population musulmane et israélite d'après le sexe et l'âge

*Table V: Muslim and Jewish population by sex and age group, by caidat*

Source: *Dénombrement de la population civile indigène (musulmane et israélite) en Tunisie au 22 mars 1931*, Régence de Tunis, Direction générale de l'intérieur, Tunis, Impr. J. Aloccio, 1932. Gallica ark `bpt6k994559s` (Source gallica.bnf.fr / Bibliothèque nationale de France).

Pages: pp. 102–105, views 57–58. Table id: `V`. Rows: 296.

## Content

One row per caidat × religion × category. Categories: Hommes / Femmes = adults aged 18 and over (`age_group = adult_18_plus`); Garçons / Filles = children (`child_under_18`). Caidat totals were cross-checked against Table II. Overlaps the package's existing `colonial_age_caidat_1931`.

Columns: census, table_id, source_page, gallica_view, caidat, religion, religion_fr, sex, age_group, category_fr, value, flag.

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
- `cells_corrected_from_image`: 1
- `carry_forward_checks`: 2
- `carry_forward_passed`: 2
- `column_total_checks`: 11
- `column_total_passed`: 11
- `crosscheck_table_II`: 74
- `crosscheck_table_II_passed`: 74

Flags: none.
