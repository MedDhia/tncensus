# cens1921_five_largest_towns

**o) Population des cinq plus grandes villes, avec répartition d'après la nationalité**  
*European and indigenous population of the five largest towns, 1921*

Source: *Statistique générale de la Tunisie*, 1922 edition (sgt1922), chapter I *Démographie*, printed pages 14, Gallica views 38 of ark `bpt6k9105649x`. Source gallica.bnf.fr / Ministère des Affaires étrangères.

40 rows, one per printed cell. `population_group`: European nationalities, `muslim`, `jewish`.

Common columns: `census` (source edition), `gallica_ark`, `table_id`, `source_page`, `gallica_view`, `census_year`, `value` (printed figure; » = 0), `flag` (see SPEC.md and SPEC_ADDENDUM.md).

## Validation

9 of 11 automated checks pass (printed row, column and grand totals, and cross-checks with the other 1921 tables and the 1906 census volume).
- failing: Bizerte nationalities = European total: computed 6799 != printed 6809 (re-read on the scan at native resolution; printed values kept)
- failing: Bizerte Italians: table o = table p: computed 3139 != printed 3149 (re-read on the scan at native resolution; printed values kept)

## Reprints

sgt1923 (view 516) and sgt1924 (view 1004): every cell compared on the images, all equal, including the misprints. sgt1925 (view 36): compared through the OCR.

OCR check (cells whose value occurs among the numbers Gallica's OCR reads on the reprint page; misses are OCR gaps, not differences):
- sgt1923 (views 516): 40 of 40
- sgt1924 (views 1004): 40 of 40
- sgt1925 (views 36): 40 of 40

## Notes and footnotes

- Bizerte: Italians printed 3.139 here but 3.149 in table p); the printed European total 6.809 requires 3.149. Kept as printed; Bizerte's European cells are flagged `total_mismatch`.
