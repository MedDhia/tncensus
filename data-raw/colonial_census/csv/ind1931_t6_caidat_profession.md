# Tableau VI — Classement, d'après la profession, des adultes mâles âgés de 18 ans au moins

*Table VI: occupations of adult males aged 18 and over, by caidat*

Source: *Dénombrement de la population civile indigène (musulmane et israélite) en Tunisie au 22 mars 1931*, Régence de Tunis, Direction générale de l'intérieur, Tunis, Impr. J. Aloccio, 1932. Gallica ark `bpt6k994559s` (Source gallica.bnf.fr / Bibliothèque nationale de France).

Pages: pp. 108–111, views 61–62. Table id: `VI`. Rows: 592.

## Content

One row per caidat × religion × occupation. The table prints no row totals, so each caidat's 8 occupations were checked against that caidat's adult men in Table V (`crosscheck_table_V_adult_men`); `row_checks` in the log is not meaningful for this table. Column totals and the carry-forward line were checked. Muslim occupations (1)–(6) are on the left page, (7)–(8) on the right page with the Jewish columns.

Columns: census, table_id, source_page, gallica_view, caidat, religion, religion_fr, sex, age_group, occupation, occupation_fr, value, flag.

## Notes and printed footnotes

Printed footnotes (translated): (1) rural landowners, farmers and agricultural workers of every kind: managers, foremen, khammès (sharecroppers), gardeners, shepherds. (2) traders, staff of all shops, commercial and bank employees, pedlars. (3) employers and workers of all trades actually engaged in manufacturing; fisheries. (4) labourers, jobbers, all those who, without a well-defined occupation, work by the day in commercial, industrial or agricultural concerns. (5) railway and tramway employees, maritime transport agents, carters, porters, camel drivers. (6) staff of the administrations and public services, including the judiciary, the police, the oudjak. (7) lawyers, oukils, doctors, business agents, experts, brokers, representatives, amines, notaries, artists, members of religious teaching and of the clergy. (8) persons not belonging in any of the previous categories: students, the infirm, people of private means. NOTA: covers only adult males aged 18 and over, i.e. 563,791 Muslims and 15,008 Jews = 578,799.

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
- `cells_corrected_from_image`: 3
- `carry_forward_checks`: 1
- `carry_forward_passed`: 1
- `column_total_checks`: 16
- `column_total_passed`: 16
- `crosscheck_table_V_adult_men`: 74
- `crosscheck_table_V_adult_men_passed`: 74
- `empty_ocr_cells_filled_0`: 3

Flags: {'ocr_corrected': 6}.
