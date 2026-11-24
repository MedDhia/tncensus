# Text table: sex

Source: Dénombrement de la population européenne civile en Tunisie au 16 décembre 1906 (Tunis, 1907). Gallica ark bd6t53563851 (Bibliothèques de l'Université de Poitiers, NUM GIR-220). pp.49-50, views 48-49.

Small table printed in the commentary. Columns: the dimension columns, `measure` (count, or a proportion whose base is named in the column value), `value`, `flag`.

Sex distribution: counts, percent of all Europeans (`pct_of_europeans`) and percent within each group (`pct_of_group`), for all Europeans, French, Italians and Maltese. Also from the prose: share of males among children under 10 and among people aged 10 and over (`pct_male_age_lt_10`, `pct_male_age_10_plus`), and the male share of the French population in 1896, 1901 and 1906. Maltese percentages of all Europeans are printed 14.1 / 13.9, where the counts imply 4.1 / 3.9 (flagged `total_mismatch`).

Common columns: `census` (= eur1906), `table_id`, `source_page` (printed page),
`gallica_view` (Gallica view number), `value`, `flag` (empty, `ocr_corrected`,
`illegible`, `total_mismatch`, `not_applicable`, `derived_from_table_i`; see SPEC.md).
Printed "»" is stored as 0. Printed subtotal and total rows are not stored; they
were used for validation.

Method: Gallica's OCR drops many cells on these pages, so every value was
transcribed from the page images (data-raw/bnf_gallica/pages/bd6t53563851/) and
checked against the printed totals by extract_eur1906_t4_t8_analysis.py.

Validation: the text tables share one battery of 191 checks (against Tables IV, V, F, B and the printed subtotals); 176 pass. Failing checks are listed in the extraction script output and flagged in the data where they concern a stored value.
