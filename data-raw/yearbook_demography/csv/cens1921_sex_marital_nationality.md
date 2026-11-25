# cens1921_sex_marital_nationality

**l) Population européenne d'après le sexe et l'état civil et par nationalité d'après le sexe**  
*European population by sex and marital status, and by nationality and sex, 1921*

Source: *Statistique générale de la Tunisie*, 1922 edition (sgt1922), chapter I *Démographie*, printed pages 11, Gallica views 35 of ark `bpt6k9105649x`. Source gallica.bnf.fr / Ministère des Affaires étrangères.

16 rows, one per printed cell. Rows with `marital_status` give the first panel; rows with empty `marital_status` the second (by nationality).

Common columns: `census` (source edition), `gallica_ark`, `table_id`, `source_page`, `gallica_view`, `census_year`, `value` (printed figure; » = 0), `flag` (see SPEC.md and SPEC_ADDENDUM.md).

## Validation

8 of 13 automated checks pass (printed row, column and grand totals, and cross-checks with the other 1921 tables and the 1906 census volume).
- failing: single: male + female: computed 85748 != printed 85757 (re-read on the scan at native resolution; printed values kept)
- failing: marital status column male: computed 76821 != printed 76830 (re-read on the scan at native resolution; printed values kept)
- failing: nationality column male: computed 77030 != printed 76830 (re-read on the scan at native resolution; printed values kept)
- failing: single males = table f: computed 44300 != printed 44309 (re-read on the scan at native resolution; printed values kept)
- failing: other: male + female = table a: computed 3520 != printed 3320 (re-read on the scan at native resolution; printed values kept)

## Reprints

sgt1923 (view 513), sgt1924 (view 1001) and sgt1925 (view 35): every cell compared on the images, all equal, including the misprints 44.300 and 1.901.

OCR check (cells whose value occurs among the numbers Gallica's OCR reads on the reprint page; misses are OCR gaps, not differences):
- sgt1923 (views 513): 0 of 16
- sgt1924 (views 1001): 11 of 16
- sgt1925 (views 35): 10 of 16

## Notes and footnotes

- Single males are printed 44.300; the row total (85.757), the column total (76.830) and table f) (44.309) all require 44.309.
- "Autres" males are printed 1.901; the column total (76.830) and table a) (3.320 other Europeans) require 1.701.
- Both are identical in every reprint. Kept as printed, flagged `total_mismatch`.
