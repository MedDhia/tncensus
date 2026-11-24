# Table B: Population française civile par circonscriptions administratives. Résultats comparés des recensements de 1891, 1896, 1901 et 1906

*French civilian population by district, censuses of 1891, 1896, 1901 and 1906*

Source: Dénombrement de la population européenne civile en Tunisie au 16 décembre 1906 (Tunis, 1907). Gallica ark bd6t53563851 (Bibliothèques de l'Université de Poitiers, NUM GIR-220). p.37, view 36.

Columns: `controle_civil`, `census_year`, value = persons. Districts follow the 1906
boundaries (footnote 1: figures regrouped by current territorial divisions). Footnote (2): add
57 French (transient and prison population) counted in 1891 but not included here.
The printed differences (1891-96, 1896-1901, 1901-06, 1891-1906) were used as checks.

Common columns: `census` (= eur1906), `table_id`, `source_page` (printed page),
`gallica_view` (Gallica view number), `value`, `flag` (empty, `ocr_corrected`,
`illegible`, `total_mismatch`, `not_applicable`, `derived_from_table_i`; see SPEC.md).
Printed "»" is stored as 0. Printed subtotal and total rows are not stored; they
were used for validation.

Method: Gallica's OCR drops many cells on these pages, so every value was
transcribed from the page images (data-raw/bnf_gallica/pages/bd6t53563851/) and
checked against the printed totals by extract_eur1906_t4_t8_analysis.py.

Validation: 101 of 103 automated checks pass. Failing checks (all re-read on the image; printed values kept):
- Tunis 1896-1891: computed 3427 != printed 3327
- Total col 4: computed 6134 != printed 6234
