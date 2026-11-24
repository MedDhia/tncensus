# Table A: Proportion pour cent des Européens de chaque nationalité et densité de la population européenne par circonscriptions

*Share of each nationality in the European population, and European population density, by district*

Source: Dénombrement de la population européenne civile en Tunisie au 16 décembre 1906 (Tunis, 1907). Gallica ark bd6t53563851 (Bibliothèques de l'Université de Poitiers, NUM GIR-220). p.35, view 34.

Columns: `controle_civil`, `indicator`: pct_french, pct_italian, pct_maltese, pct_other_european
(percent of the district's Europeans, numeric with one decimal), area_myriametres2 (area in
myriamètres carrés = 100 km2), europeans_per_myriametre2 (density). Gafsa, Tozeur and Territoires
du Sud have no area ("»"): NA, flag `not_applicable`. The printed "Ensemble du territoire" row is
kept (`controle_civil` = "Ensemble du territoire (printed)") because it is not a simple sum.
Footnote (1) to the total area/density: computed without the circonscriptions whose area is not given.

Validation: every percentage and density was recomputed from Table I. Values that differ from
the recomputation by 0.1 or more are flagged `total_mismatch` (printed values kept; re-read on a
2x zoom of the image, the print is as transcribed).

Common columns: `census` (= eur1906), `table_id`, `source_page` (printed page),
`gallica_view` (Gallica view number), `value`, `flag` (empty, `ocr_corrected`,
`illegible`, `total_mismatch`, `not_applicable`, `derived_from_table_i`; see SPEC.md).
Printed "»" is stored as 0. Printed subtotal and total rows are not stored; they
were used for validation.

Method: Gallica's OCR drops many cells on these pages, so every value was
transcribed from the page images (data-raw/bnf_gallica/pages/bd6t53563851/) and
checked against the printed totals by extract_eur1906_t4_t8_analysis.py.

Validation: 90 of 98 automated checks pass. Failing checks (all re-read on the image; printed values kept):
- Bizerte pct_italian recomputed 63.29: differs from printed value
- Kairouan pct_italian recomputed 55.25: differs from printed value
- Kairouan pct_other_european recomputed 7.38: differs from printed value
- Le Kef density 53.91: differs from printed value
- Sfax density 73.75: differs from printed value
- Sousse pct_maltese recomputed 15.71: differs from printed value
- Thala pct_french recomputed 32.46: differs from printed value
- Thala pct_italian recomputed 66.59: differs from printed value
