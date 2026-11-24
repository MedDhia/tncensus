# Table E: Répartition de la population française civile d'après le lieu de naissance. Résultats comparés des recensements de 1891, 1896, 1901 et 1906

*French civilian population by place of birth, censuses of 1891-1906*

Source: Dénombrement de la population européenne civile en Tunisie au 16 décembre 1906 (Tunis, 1907). Gallica ark bd6t53563851 (Bibliothèques de l'Université de Poitiers, NUM GIR-220). pp.46-48, views 45-47.

Columns: `birthplace_fr` (Tunisia, the three Algerian départements, each French
département, colonies, abroad, unknown; as printed), `census_year`, value = persons.
Footnote (1): colonies and possessions other than Algeria and Tunisia.

Validation: the printed "à reporter" running totals were checked page by page. p.48 matches
exactly. On pp.46-47 the printed cells do not add up to the printed totals. The commentary
(pp.44-45) confirms three printing errors, all flagged `total_mismatch` with the printed
values kept: Bouches-du-Rhône 1906 printed 822 (commentary 922); Rhône 1901 printed 478
(commentary's +137 since 1901 implies 498); Loiret 1906 printed 29 (the page total implies
79). Smaller residual differences (2-10 persons) remain on pp.46-47 after re-reading the
zoomed images. Allier 1891: the first digit is broken in the scan and was read as 34
(`ocr_corrected`).

Common columns: `census` (= eur1906), `table_id`, `source_page` (printed page),
`gallica_view` (Gallica view number), `value`, `flag` (empty, `ocr_corrected`,
`illegible`, `total_mismatch`, `not_applicable`, `derived_from_table_i`; see SPEC.md).
Printed "»" is stored as 0. Printed subtotal and total rows are not stored; they
were used for validation.

Method: Gallica's OCR drops many cells on these pages, so every value was
transcribed from the page images (data-raw/bnf_gallica/pages/bd6t53563851/) and
checked against the printed totals by extract_eur1906_t4_t8_analysis.py.

Validation: 1 of 16 automated checks pass. Failing checks (all re-read on the image; printed values kept):
- running total p.46 1891: computed 6129 != printed 6131
- running total p.46 1901: computed 15416 != printed 15426
- running total p.46 1906: computed 22863 != printed 22964
- running total p.47 1891: computed 8063 != printed 8055
- running total p.47 1896: computed 13372 != printed 13362
- running total p.47 1901: computed 19942 != printed 19972
- running total p.47 1906: computed 28627 != printed 28778
- running total p.48 1891: computed 9981 != printed 9973
- running total p.48 1896: computed 16217 != printed 16207
- running total p.48 1901: computed 24171 != printed 24201
- running total p.48 1906: computed 34459 != printed 34610
- total 1891 vs Table B: computed 9981 != printed 9973
- total 1896 vs Table B: computed 16217 != printed 16207
- total 1901 vs Table B: computed 24171 != printed 24201
- total 1906 vs Table B: computed 34459 != printed 34610
