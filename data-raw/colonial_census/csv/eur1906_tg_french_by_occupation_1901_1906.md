# Table G: Répartition d'après la profession et le sexe, par circonscriptions administratives. Résultats comparés des recensements de 1901 et 1906

*French population by occupational group and sex, by district, censuses of 1901 and 1906*

Source: Dénombrement de la population européenne civile en Tunisie au 16 décembre 1906 (Tunis, 1907). Gallica ark bd6t53563851 (Bibliothèques de l'Université de Poitiers, NUM GIR-220). pp.62-63, view 61.

Columns: `controle_civil` (as printed; Béja and Medjez-el-Bab, and Gafsa and Tozeur, are
combined), `census_year`, `occupation_group` (agriculture, commerce, industry, transport,
public_administration, police_force, liberal_professions, independent_means, unclassified),
`sex`. Persons, counting both those exercising the profession and their families (N.B. printed
on the table). Printed group totals and the "Totaux" column were used for validation only.

Validation: each M+F against its printed total, each row of totals against the sum of the
groups, and the "Ensemble du territoire" rows against the column sums. The print itself has
inconsistencies (re-read on the image): Le Kef 1906 transport printed 52 + 30 = "582" (82,
which the regency total confirms); Souk-el-Arba 1906 police force 12 + 21 = 32; Territoires du
Sud 1906 unclassified 0 + 23 = 24. Cells in those groups are flagged `total_mismatch`. Some
printed row totals also differ from the sum of their groups (Béja et Medjez-el-Bab 1906 men,
Grombalia 1906 men/women, Djerba 1901 women, Mactar 1906 men), as does the printed regency
total. The commentary (p.60) warns that the 1901 and 1906 categories are not fully comparable.

Common columns: `census` (= eur1906), `table_id`, `source_page` (printed page),
`gallica_view` (Gallica view number), `value`, `flag` (empty, `ocr_corrected`,
`illegible`, `total_mismatch`, `not_applicable`, `derived_from_totals`; see SPEC.md).
Printed "»" is stored as 0. Printed subtotal and total rows are not stored; they
were used for validation.

Method: Gallica's OCR drops many cells on these pages, so every value was
transcribed from the page images (data-raw/bnf_gallica/pages/bd6t53563851/) and
checked against the printed totals by extract_eur1906_t4_t8_analysis.py.

Validation: 482 of 502 automated checks pass. Failing checks (all re-read on the image; printed values kept):
- Béja et Medjez-el-Bab 1906 totals col 0: computed 680 != printed 730
- Béja et Medjez-el-Bab 1906 totals col 2: computed 1202 != printed 1252
- Grombalia 1906 totals col 0: computed 591 != printed 691
- Grombalia 1906 totals col 1: computed 440 != printed 340
- Le Kef 1906 transport M+F=T: computed 82 != printed 582
- Le Kef 1906 totals col 2: computed 1281 != printed 781
- Mactar 1906 totals col 0: computed 44 != printed 46
- Mactar 1906 totals col 2: computed 73 != printed 75
- Souk-el-Arba 1906 police_force M+F=T: computed 33 != printed 32
- Souk-el-Arba 1906 totals col 2: computed 1003 != printed 1004
- Territoires du Sud 1906 unclassified M+F=T: computed 23 != printed 24
- Territoires du Sud 1906 totals col 0: computed 73 != printed 74
- Ensemble 1906 col 0: computed 2610 != printed 2660
- Ensemble 1906 col 2: computed 4393 != printed 4443
- Ensemble 1906 col 11: computed 3225 != printed 2725
- Ensemble 1906 col 17: computed 995 != printed 996
- Ensemble 1906 col 24: computed 1088 != printed 1089
- Ensemble 1906 col 27: computed 18257 != printed 18155
- Ensemble 1906 col 28: computed 17214 != printed 17314
- Ensemble 1906 col 29: computed 35471 != printed 35469
