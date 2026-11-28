# Text table: occupation groups

Source: Dénombrement de la population européenne civile en Tunisie au 16 décembre 1906 (Tunis, 1907). Gallica ark bd6t53563851 (Bibliothèques de l'Université de Poitiers, NUM GIR-220). p.58, view 57.

Small table printed in the commentary. Columns: the dimension columns, `measure` (count, or a proportion whose base is named in the column value), `value`, `flag`.

Occupational groups by nationality: persons exercising the profession and their families, counts and percent of each group's population (footnote 1). 'Personnes vivant de leurs revenus' and 'Population non classée' are single lines. Printed group subtotals were checked (all pass). The grand totals are larger than the Table I populations for the French and smaller for the Italians and Maltese, because servants and dependants were attached to the head of household's nationality (commentary p.60).

Common columns: `census` (= eur1906), `table_id`, `source_page` (printed page),
`gallica_view` (Gallica view number), `value`, `flag` (empty, `ocr_corrected`,
`illegible`, `total_mismatch`, `not_applicable`, `derived_from_totals`; see SPEC.md).
Printed "»" is stored as 0. Printed subtotal and total rows are not stored; they
were used for validation.

Method: Gallica's OCR drops many cells on these pages, so every value was
transcribed from the page images (data-raw/bnf_gallica/pages/bd6t53563851/) and
checked against the printed totals by extract_eur1906_t4_t8_analysis.py.

Validation: the text tables share one battery of 191 checks (against Tables IV, V, F, B and the printed subtotals); 176 pass. Failing checks are listed in the extraction script output and flagged in the data where they concern a stored value.
