# cens1921_profession_nationality

**g) Population européenne par profession et nationalité (sexes réunis)**  
*European population by profession, status and nationality, both sexes, 1921*

Source: *Statistique générale de la Tunisie*, 1922 edition (sgt1922), chapter I *Démographie*, printed pages 8-9, Gallica views 32-33 of ark `bpt6k9105649x`. Source gallica.bnf.fr / Ministère des Affaires étrangères.

132 rows, one per printed cell. `status`: for agriculture, commerce, industry and transport, `employer` (patrons), `worker` (ouvriers) or `family` (families of employers and workers); for civil service, police and liberal professions, `active` or `family`. For people living on independent means and the unclassified population, `sex` is given instead. Printed subtotals are not stored.

Common columns: `census` (source edition), `gallica_ark`, `table_id`, `source_page`, `gallica_view`, `census_year`, `value` (printed figure; » = 0), `flag` (see SPEC.md and SPEC_ADDENDUM.md).

## Validation

120 of 121 automated checks pass (printed row, column and grand totals, and cross-checks with the other 1921 tables and the 1906 census volume).
- failing: police_force: nationalities = Ensemble: computed [522, 1183] != printed [522, 1186] (re-read on the scan at native resolution; printed values kept)

## Reprints

sgt1923 (views 510-511), sgt1924 (views 998-999) and sgt1925 (views 32-33): every cell compared on the images, all equal. They are the same typesetting, including the police-force misprint.

OCR check (cells whose value occurs among the numbers Gallica's OCR reads on the reprint page; misses are OCR gaps, not differences):
- sgt1923 (views 510, 511): 72 of 132
- sgt1924 (views 998, 999): 86 of 132
- sgt1925 (views 32, 33): 84 of 132

## Notes and footnotes

- Police force (Force publique), family: the six nationalities sum to 1.183, but the Ensemble column prints 1.186 (and its total 1.708). Kept as printed; the family cells of that row are flagged `total_mismatch`.
