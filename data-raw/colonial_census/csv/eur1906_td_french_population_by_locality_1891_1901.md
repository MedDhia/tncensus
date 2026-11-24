# Table D: Répartition de la population française civile par localités. Résultats comparés des recensements de 1891, 1896 et 1901

*French civilian population by locality, censuses of 1891, 1896 and 1901*

Source: Dénombrement de la population européenne civile en Tunisie au 16 décembre 1906 (Tunis, 1907). Gallica ark bd6t53563851 (Bibliothèques de l'Université de Poitiers, NUM GIR-220). pp.41-45, views 40-44.

Columns: `controle_civil` (the contrôle civil or annexe heading as printed), `locality`
(as printed; city quarters written "Ville de Sfax, quartier : X"), `census_year`, value = persons.
The table prints no subtotals. "Maxula-Radès et Megrine" share one bracketed value in 1891
and 1896, and are separate in 1901. The 1891 Béja row "Djebel-ben-Drahar, ... et Sidi-Ahmed"
groups eight places.

The commentary (p.38) warns that the same place was often recorded under different names
at successive censuses, so localities are not strictly comparable over time.

Validation: unit sums were compared with Table B. They match for 14 of 19 units. For
Bizerte, Djerba, Teboursouk, Thala and Tunis, and so for the regency total, they do not:
Table D lists only named localities, while Table B regroups the population by 1906
boundaries. The source gives no reconciliation, and no value was changed.

Common columns: `census` (= eur1906), `table_id`, `source_page` (printed page),
`gallica_view` (Gallica view number), `value`, `flag` (empty, `ocr_corrected`,
`illegible`, `total_mismatch`, `not_applicable`, `derived_from_table_i`; see SPEC.md).
Printed "»" is stored as 0. Printed subtotal and total rows are not stored; they
were used for validation.

Method: Gallica's OCR drops many cells on these pages, so every value was
transcribed from the page images (data-raw/bnf_gallica/pages/bd6t53563851/) and
checked against the printed totals by extract_eur1906_t4_t8_analysis.py.

Validation: 0 of 3 automated checks pass. Failing checks (all re-read on the image; printed values kept):
- Regency total 1891 vs Table B total: computed 9824 != printed 9973
- Regency total 1896 vs Table B total: computed 15917 != printed 16207
- Regency total 1901 vs Table B total: computed 24147 != printed 24201
