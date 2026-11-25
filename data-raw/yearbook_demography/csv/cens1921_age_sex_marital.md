# cens1921_age_sex_marital

**f) Population européenne d'après l'âge, le sexe et l'état civil**  
*European population by age group, sex and marital status, by nationality, 1921*

Source: *Statistique générale de la Tunisie*, 1922 edition (sgt1922), chapter I *Démographie*, printed pages 8-9, Gallica views 32-33 of ark `bpt6k9105649x`. Source gallica.bnf.fr / Ministère des Affaires étrangères.

72 rows, one per printed cell. `nationality` = `all_europeans` ("Ensemble de la population, compris européens non dénommés"), `french`, `italian` or `maltese`. Widowed and divorced are printed together.

Common columns: `census` (source edition), `gallica_ark`, `table_id`, `source_page`, `gallica_view`, `census_year`, `value` (printed figure; » = 0), `flag` (see SPEC.md and SPEC_ADDENDUM.md).

## Validation

40 of 40 automated checks pass (printed row, column and grand totals, and cross-checks with the other 1921 tables and the 1906 census volume).

## Reprints

sgt1923 (views 510-511), sgt1924 (views 998-999) and sgt1925 (views 32-33): every cell compared on the images, all equal. They are the same typesetting, including the police-force misprint.

OCR check (cells whose value occurs among the numbers Gallica's OCR reads on the reprint page; misses are OCR gaps, not differences):
- sgt1923 (views 510, 511): 33 of 72
- sgt1924 (views 998, 999): 62 of 72
- sgt1925 (views 32, 33): 46 of 72

## Notes and footnotes

- French married women (three cells) are lost in the sgt1922 gutter; read from sgt1923 (`reprint_corrected`).
- The printed percentages by marital status are not stored.
