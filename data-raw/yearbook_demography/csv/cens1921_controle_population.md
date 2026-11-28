# cens1921_controle_population

**a) Superficie, populations (européenne et indigène) et densité de la population par circonscription de Contrôle civil**  
*Area, population (European and indigenous) and population density by contrôle civil, 1921 census*

Source: *Statistique générale de la Tunisie*, 1922 edition (sgt1922), chapter I *Démographie*, printed pages 2-3, Gallica views 26-27 of ark `bpt6k9105649x`. Source gallica.bnf.fr / Ministère des Affaires étrangères.

200 rows, one per printed cell. `measure`: `area_km2`, `population` or `density_per_km2` (inhabitants per km², as printed, two decimals). For `population`, `population_group` gives the nationality or religion.

Common columns: `census` (source edition), `gallica_ark`, `table_id`, `source_page`, `gallica_view`, `census_year`, `value` (printed figure; » = 0), `flag` (see SPEC.md and SPEC_ADDENDUM.md).

## Validation

47 of 51 automated checks pass (printed row, column and grand totals, and cross-checks with the other 1921 tables and the 1906 census volume).
- failing: Sousse: density = total / area (truncated to 2 decimals): computed 43.47 != printed 43.46 (re-read on the scan at native resolution; printed values kept)
- failing: Thala: groups = total: computed 88167 != printed 88267 (re-read on the scan at native resolution; printed values kept)
- failing: Tunis: groups = total: computed 269412 != printed 269312 (re-read on the scan at native resolution; printed values kept)
- failing: area column: computed 125130 != printed 125180 (re-read on the scan at native resolution; printed values kept)

## Reprints

sgt1923 (views 504-505) and sgt1924 (views 992-993): every cell compared on the images, all equal; the Spanish column, lost in the sgt1922 gutter, is legible in both and identical. sgt1925 (views 26-27): equal where the OCR reads it.

OCR check (cells whose value occurs among the numbers Gallica's OCR reads on the reprint page; misses are OCR gaps, not differences):
- sgt1923 (views 504, 505): 195 of 200
- sgt1924 (views 992, 993): 189 of 200
- sgt1925 (views 26, 27): 197 of 200

## Notes and footnotes

- The Spanish column falls in the gutter of the sgt1922 spread; its values were read from sgt1923 (flag `reprint_corrected`) and are identical in sgt1924.
- Thala and Tunis: the printed totals (88.267, 269.312) differ from the sum of their groups (88.167, 269.412) by +100 and -100; the grand total agrees with the groups. Every cell of both rows is kept as printed and flagged `total_mismatch`.
- The area column sums to 125.130 km², 50 less than the printed 125.180.
- Densities are truncated, not rounded, to two decimals; Sousse prints 43,46 where 269.534/6.200 = 43,47.
