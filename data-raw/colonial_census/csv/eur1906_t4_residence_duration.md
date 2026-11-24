# Table IV: Répartition d'après le temps de séjour en Tunisie, par nationalités et circonscriptions administratives

*Distribution by length of residence in Tunisia, by nationality and administrative district*

Source: Dénombrement de la population européenne civile en Tunisie au 16 décembre 1906 (Tunis, 1907). Gallica ark bd6t53563851 (Bibliothèques de l'Université de Poitiers, NUM GIR-220). pp.18-21, views 22-25.

Columns: `controle_civil` (19 circonscriptions as printed), `nationality`, `residence_duration`
(12 classes: passing_through = "de passage en Tunisie", lt_1y, 1_2y ... 9_10y, gt_10y). Counts of persons.

Footnote (1): people temporarily away from their locality but domiciled in Tunisia are counted
as inhabitants of that locality; "de passage" covers only persons whose usual residence is outside Tunisia.

On pp.18 and 20 (Béja, Medjez-el-Bab, Bizerte, Gabès, Djerba, Téboursouk, Mactar, Sfax,
Souk-el-Arba, Tabarca) the last column ("de plus de 10 ans") is lost in the binding of the
scan. Those 60 cells are derived as Table I nationality total minus the sum of the 11 visible
columns (flag `derived_from_totals`). The derived values, summed with the printed pp.19/21
values, reproduce the printed regency totals ("Ensemble du territoire") for every nationality
and duration class, which validates them.

Common columns: `census` (= eur1906), `table_id`, `source_page` (printed page),
`gallica_view` (Gallica view number), `value`, `flag` (empty, `ocr_corrected`,
`illegible`, `total_mismatch`, `not_applicable`, `derived_from_totals`; see SPEC.md).
Printed "»" is stored as 0. Printed subtotal and total rows are not stored; they
were used for validation.

Method: Gallica's OCR drops many cells on these pages, so every value was
transcribed from the page images (data-raw/bnf_gallica/pages/bd6t53563851/) and
checked against the printed totals by extract_eur1906_t4_t8_analysis.py.

Validation: 362 of 362 automated checks pass.
