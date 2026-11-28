# Tableau VIII — Population musulmane et israélite des localités non érigées en Commune et comptant plus de 25 foyers

*Table VIII: Muslim and Jewish population of localities not constituted as communes and having more than 25 households*

Source: *Dénombrement de la population civile indigène (musulmane et israélite) en Tunisie au 22 mars 1931*, Régence de Tunis, Direction générale de l'intérieur, Tunis, Impr. J. Aloccio, 1932. Gallica ark `bpt6k994559s` (Source gallica.bnf.fr / Bibliothèque nationale de France).

Pages: pp. 117–127, views 68–78. Table id: `VIII`. Rows: 562.

## Content

One row per locality × religion (281 localities). `caidat` as printed; empty where the table prints '—'. Caidat spellings follow the print ('Oulad-Aoun' on p.118, 'Ouled-Aoun'/'Ouled-Ayar' elsewhere). Hassi-Djerbi's caidat is printed 'Ouerghemma (Terr. de Zarzis)'; Beni-Kheddache and Métameur 'Ouerghemma (Terr. de Médenine)'. Hencha (El)'s caidat is misprinted 'Madhia' and stored as 'Mahdia'. Duplicate names (Aouina (El), Chenini, Gueliâ (El), Mansoura (El), Zriba) are distinct localities in different caidats. Every row was checked (Muslim + Jewish = printed total); all names and caidats were compared with the page images (the OCR names on p.125 were unusable and were read from the image; a library stamp covers part of that page).

Columns: census, table_id, source_page, gallica_view, locality, caidat, note, religion, religion_fr, value, flag.

## Notes and printed footnotes

Printed footnotes: localities marked (1), (2), (3) are in the Kerkennah islands; stored in `note`.

## Method

Numbers come from Gallica's word OCR (via `ocr.py`), assigned to printed columns by right edge,
with page images used to correct the OCR. Script: `extract_ind1931_other.py`. Printed `»` = 0.
Printed subtotal, total, `A reporter` and `Report` lines are not stored; they were used for validation.
`flag = ocr_corrected` marks a cell where the OCR value was missing or wrong and the value was read
from the page image (an empty OCR cell is set to 0 only where the image shows `»` and the printed
row totals then balance; every such cell was confirmed on the image).

## Validation

- `row_checks`: 281
- `row_checks_passed`: 281
- `empty_ocr_cells_filled_0`: 4
- `cells_corrected_from_image`: 3
- `stamp_fragments_dropped`: 1
- `pages_compared_with_image`: 11

Flags: {'ocr_corrected': 5}.
