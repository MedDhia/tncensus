# cens1921_towns_european_population

**p) Population européenne des villes comptant 1° plus de 1.000 habitants, 2° de 500 à 1.000 habitants**  
*European population of towns with over 1,000 and 500-1,000 Europeans, 1921*

Source: *Statistique générale de la Tunisie*, 1922 edition (sgt1922), chapter I *Démographie*, printed pages 14, Gallica views 38 of ark `bpt6k9105649x`. Source gallica.bnf.fr / Ministère des Affaires étrangères.

174 rows, one per printed cell. `size_class` and `town_rank` as printed.

Common columns: `census` (source edition), `gallica_ark`, `table_id`, `source_page`, `gallica_view`, `census_year`, `value` (printed figure; » = 0), `flag` (see SPEC.md and SPEC_ADDENDUM.md).

## Validation

28 of 29 automated checks pass (printed row, column and grand totals, and cross-checks with the other 1921 tables and the 1906 census volume).
- failing: Souk-el-Khemis nationalities = total: computed 474 != printed 584 (re-read on the scan at native resolution; printed values kept)

## Reprints

sgt1923 (view 516) and sgt1924 (view 1004): every cell compared on the images, all equal, including the misprints. sgt1925 (view 36): compared through the OCR.

OCR check (cells whose value occurs among the numbers Gallica's OCR reads on the reprint page; misses are OCR gaps, not differences):
- sgt1923 (views 516): 151 of 174
- sgt1924 (views 1004): 165 of 174
- sgt1925 (views 36): 166 of 174

## Notes and footnotes

- Souk-el-Khemis: the cells sum to 474 against a printed total of 584 (checked at native resolution and in two reprints). Kept as printed, flagged `total_mismatch`.
