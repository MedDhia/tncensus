# Text table: french by origin

Source: Dénombrement de la population européenne civile en Tunisie au 16 décembre 1906 (Tunis, 1907). Gallica ark bd6t53563851 (Bibliothèques de l'Université de Poitiers, NUM GIR-220). p.55, view 54.

Small table printed in the commentary. Columns: the dimension columns, `measure` (count, or a proportion whose base is named in the column value), `value`, `flag`.

French by birth vs. French by naturalisation, option or marriage: counts and shares in 1901 and 1906. Also, for 1906, counts and percentages by sex, broad age group and marital status. The counts match Table F. Some printed percentages differ from a recomputation by more than 0.1 (flagged `total_mismatch`).

Common columns: `census` (= eur1906), `table_id`, `source_page` (printed page),
`gallica_view` (Gallica view number), `value`, `flag` (empty, `ocr_corrected`,
`illegible`, `total_mismatch`, `not_applicable`, `derived_from_table_i`; see SPEC.md).
Printed "»" is stored as 0. Printed subtotal and total rows are not stored; they
were used for validation.

Method: Gallica's OCR drops many cells on these pages, so every value was
transcribed from the page images (data-raw/bnf_gallica/pages/bd6t53563851/) and
checked against the printed totals by extract_eur1906_t4_t8_analysis.py.

Validation: the text tables share one battery of 191 checks (against Tables IV, V, F, B and the printed subtotals); 176 pass. Failing checks are listed in the extraction script output and flagged in the data where they concern a stored value.
