# Table F: Répartition de la population française d'après le sexe, l'âge et l'état civil en distinguant les Français de naissance et les Français par naturalisation, option ou mariage

*French population by sex, age and marital status, French by birth vs. by naturalisation, option or marriage*

Source: Dénombrement de la population européenne civile en Tunisie au 16 décembre 1906 (Tunis, 1907). Gallica ark bd6t53563851 (Bibliothèques de l'Université de Poitiers, NUM GIR-220). p.54, view 53.

Columns: `nationality_origin` (by_birth, naturalised), `age_group`, `marital_status`, `sex`.
Counts of persons. The two blocks add up exactly to the French block of Table V.

Common columns: `census` (= eur1906), `table_id`, `source_page` (printed page),
`gallica_view` (Gallica view number), `value`, `flag` (empty, `ocr_corrected`,
`illegible`, `total_mismatch`, `not_applicable`, `derived_from_table_i`; see SPEC.md).
Printed "»" is stored as 0. Printed subtotal and total rows are not stored; they
were used for validation.

Method: Gallica's OCR drops many cells on these pages, so every value was
transcribed from the page images (data-raw/bnf_gallica/pages/bd6t53563851/) and
checked against the printed totals by extract_eur1906_t4_t8_analysis.py.

Validation: 74 of 74 automated checks pass.
