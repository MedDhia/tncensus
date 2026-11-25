# Table E: Répartition de la population française civile d'après le lieu de naissance. Résultats comparés des recensements de 1891, 1896, 1901 et 1906

*French civilian population by place of birth, censuses of 1891-1906*

Source: Dénombrement de la population européenne civile en Tunisie au 16 décembre 1906 (Tunis, 1907). Gallica ark bd6t53563851 (Bibliothèques de l'Université de Poitiers, NUM GIR-220). pp.46-48, views 45-47.

Columns: `birthplace_fr` (Tunisia, the three Algerian départements, each French
département, colonies, abroad, unknown; as printed), `census_year`, value = persons.
Footnote (1): colonies and possessions other than Algeria and Tunisia.

Validation: the printed "à reporter" running totals were checked page by page. p.48 matches
exactly; on pp.46-47 the printed cells do not add up to the printed totals.

Every cell on pp.46-47 was re-read on the scans (views 45-46) and matches the transcription,
so the remaining differences are in the 1906 printing itself, not in the transcription.

The printed totals are right. The commentary's own summary table (p.40) gives the French
born in Tunisia, Algeria and France for each census. Its Tunisia and Algeria figures equal
this table's, and with the colonies, abroad and unknown rows it reproduces this table's
printed grand totals (9.973, 16.207, 24.201, 34.610). So every discrepancy is in the rows
for the French départements: their printed cells sum to 6.115, 9.778, 14.006 and 18.288,
against 6.107, 9.768, 14.036 and 18.439 born in France per p.40.

Three cells are identified as misprints and flagged `total_mismatch` (printed values kept):
- Bouches-du-Rhône 1906, printed 822: the commentary (p.45) gives 922, and an increase of
  143 since 1901 (779 + 143 = 922).
- Rhône 1901, printed 478: the commentary gives 635 in 1906 and +137 since 1901, so 498.
- Loiret 1906, printed 29: the p.47 page total implies 79 (not confirmed by the commentary).
The commentary's other ten 1901-1906 increases (Corse, Seine, Gard, Var, Isère, Ardèche,
Hautes-Alpes, Aude, Hérault, Gironde) all agree with this table.

After these three, small differences remain that the sources cannot assign to a cell.
They are given as the département cells' sum minus the printed page total:
- p.46: 1891 -2, 1901 -10, 1906 -1 (1896 agrees)
- p.47: 1891 +10, 1896 +10 (1901 and 1906 agree once Rhône and Loiret are corrected)
These cells are not flagged. Sums over départements therefore differ from the printed
totals by up to 10 persons a year; use the printed totals (or Table B) for the French
total.

The 1922 *Statistique générale* reprints these columns (cens1921_french_birthplace_1891_1921,
table b) with six different cells: Bouches-du-Rhône 1906 922, Calvados 1906 55, Gironde
1906 374, Var 1891 110, Var 1901 286, Etranger 1896 679. Each year's changes (1891 -8,
1896 -10, 1901 +30, 1906 +151) exactly offset the gaps between the départements and the
printed totals, so the 1922 compilers appear to have forced the columns to add up. Only Bouches-du-Rhône 922 agrees with this volume's
commentary; Gironde 324 (+58 since 1901) and Var 256 in 1901 (+147 to 403) are confirmed
by it, which contradicts the 1922 adjustments. The 1922 reprint therefore does not locate
the remaining residuals. Allier 1891: the first digit is broken in the scan and was read as 34
(`ocr_corrected`).

Common columns: `census` (= eur1906), `table_id`, `source_page` (printed page),
`gallica_view` (Gallica view number), `value`, `flag` (empty, `ocr_corrected`,
`illegible`, `total_mismatch`, `not_applicable`, `derived_from_totals`; see SPEC.md).
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
