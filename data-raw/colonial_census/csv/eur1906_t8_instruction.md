# Table VIII: Degré d'instruction

*Literacy and knowledge of French*

Source: Dénombrement de la population européenne civile en Tunisie au 16 décembre 1906 (Tunis, 1907). Gallica ark bd6t53563851 (Bibliothèques de l'Université de Poitiers, NUM GIR-220). p.34, view 33.

Columns: `nationality`, `indicator` (reads_only = "Sachant lire seulement",
reads_and_writes = "Sachant lire et écrire", speaks_french = "Parlant français"). Counts of persons.
Footnote (1): the question "speaks French" was not asked of the French, so that cell is NA
(flag `not_applicable`), not zero.

Common columns: `census` (= eur1906), `table_id`, `source_page` (printed page),
`gallica_view` (Gallica view number), `value`, `flag` (empty, `ocr_corrected`,
`illegible`, `total_mismatch`, `not_applicable`, `derived_from_totals`; see SPEC.md).
Printed "»" is stored as 0. Printed subtotal and total rows are not stored; they
were used for validation.

Method: Gallica's OCR drops many cells on these pages, so every value was
transcribed from the page images (data-raw/bnf_gallica/pages/bd6t53563851/) and
checked against the printed totals by extract_eur1906_t4_t8_analysis.py.

Validation: 3 of 3 automated checks pass.
