# cens1921_circonscription_1911_1921

**m) Recensements de 1911 et de 1921 par circonscription administrative (population européenne)**  
*Europeans by circonscription and nationality, 1911 and 1921, with the French population 1891-1921*

Source: *Statistique générale de la Tunisie*, 1922 edition (sgt1922), chapter I *Démographie*, printed pages 12-13, Gallica views 36-37 of ark `bpt6k9105649x`. Source gallica.bnf.fr / Ministère des Affaires étrangères.

320 rows, one per printed cell. `census_year` 1911 or 1921 for all nationalities; the rows for 1891-1906 are the French population ("Mouvement de la population française"). The 1911 and 1921 French columns equal the movement columns and are stored once.

Common columns: `census` (source edition), `gallica_ark`, `table_id`, `source_page`, `gallica_view`, `census_year`, `value` (printed figure; » = 0), `flag` (see SPEC.md and SPEC_ADDENDUM.md).

## Validation

257 of 258 automated checks pass (printed row, column and grand totals, and cross-checks with the other 1921 tables and the 1906 census volume).
- failing: column 2 1921: computed 13520 != printed 11520 (re-read on the scan at native resolution; printed values kept)
- French 1891-1906 by circonscription vs the 1906 census volume (Table B): 76 of 76 cells equal.

## Reprints

sgt1923 (views 514-515): every cell compared on the images, all equal, including the Maltese 1921 total misprint (11.520). sgt1924 (views 1002-1003): compared through the OCR. Not reprinted in sgt1925.

OCR check (cells whose value occurs among the numbers Gallica's OCR reads on the reprint page; misses are OCR gaps, not differences):
- sgt1923 (views 514, 515): 291 of 320
- sgt1924 (views 1002, 1003): 295 of 320

## Notes and footnotes

- (1) In 1911 the population of the contrôle civil of Zaghouan was counted with Tunis (», stored 0).
- The Maltese 1921 column total is printed 11.520 (also in sgt1923); the column sums to 13.520, which tables a) and n) give.
- Spanish 1921 is in the gutter; values equal table a) (`reprint_corrected`).
