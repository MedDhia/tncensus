# Table C: Population française civile. Coefficients d'accroissement par circonscriptions administratives

*French civilian population: growth coefficients by district*

Source: Dénombrement de la population européenne civile en Tunisie au 16 décembre 1906 (Tunis, 1907). Gallica ark bd6t53563851 (Bibliothèques de l'Université de Poitiers, NUM GIR-220). p.39, view 38.

Columns: `controle_civil`, `base_year`, `census_year`, value = population in census_year
divided by population in base_year (numeric, two decimals; base year = 1). Pairs printed:
1891 to 1896/1901/1906, 1896 to 1901, 1901 to 1906. Each coefficient was recomputed from
Table B; those off by more than 0.01 are flagged `total_mismatch` (printed values kept).

Common columns: `census` (= eur1906), `table_id`, `source_page` (printed page),
`gallica_view` (Gallica view number), `value`, `flag` (empty, `ocr_corrected`,
`illegible`, `total_mismatch`, `not_applicable`, `derived_from_table_i`; see SPEC.md).
Printed "»" is stored as 0. Printed subtotal and total rows are not stored; they
were used for validation.

Method: Gallica's OCR drops many cells on these pages, so every value was
transcribed from the page images (data-raw/bnf_gallica/pages/bd6t53563851/) and
checked against the printed totals by extract_eur1906_t4_t8_analysis.py.

Validation: 91 of 100 automated checks pass. Failing checks (all re-read on the image; printed values kept):
- Le Kef 1901/1896 recomputed 1.261: differs from printed value
- Le Kef 1906/1901 recomputed 2.023: differs from printed value
- Teboursouk 1896/1891 recomputed 6.118: differs from printed value
- Teboursouk 1906/1901 recomputed 2.694: differs from printed value
- Souk-el-Arba 1901/1891 recomputed 1.797: differs from printed value
- Tabarca 1906/1891 recomputed 2.859: differs from printed value
- Sousse 1906/1901 recomputed 1.320: differs from printed value
- Territoires du Sud 1896/1891 recomputed 1.571: differs from printed value
- Ensemble du territoire 1896/1891 recomputed 1.625: differs from printed value
