# cens1921_europeans_1881_1921

**n) Population européenne par période quinquennales (1881-1921)**  
*European population by nationality, 1881-1921*

Source: *Statistique générale de la Tunisie*, 1922 edition (sgt1922), chapter I *Démographie*, printed pages 14, Gallica views 38 of ark `bpt6k9105649x`. Source gallica.bnf.fr / Ministère des Affaires étrangères.

34 rows, one per printed cell. No breakdown of Spanish, Greek and other Europeans before 1906; in 1901 the three are printed as one bracketed value (3.214), stored as `other_european` with `nationality_fr` "Espagnols, Grecs, Autres européens".

Common columns: `census` (source edition), `gallica_ark`, `table_id`, `source_page`, `gallica_view`, `census_year`, `value` (printed figure; » = 0), `flag` (see SPEC.md and SPEC_ADDENDUM.md).

## Validation

8 of 9 automated checks pass (printed row, column and grand totals, and cross-checks with the other 1921 tables and the 1906 census volume).
- failing: column 1901: computed 111071 != printed 111101 (re-read on the scan at native resolution; printed values kept)

## Reprints

sgt1923 (view 516) and sgt1924 (view 1004): every cell compared on the images, all equal, including the misprints. sgt1925 (view 36): compared through the OCR.

OCR check (cells whose value occurs among the numbers Gallica's OCR reads on the reprint page; misses are OCR gaps, not differences):
- sgt1923 (views 516): 28 of 34
- sgt1924 (views 1004): 28 of 34
- sgt1925 (views 36): 28 of 34

## Notes and footnotes

- (1) 1881: registers of the French consulates before the Protectorate. (2) 1886: trial census. (3) From 1891: quinquennial censuses.
- (4) For all foreigners, until 1898 (when the control of foreigners was instituted) the figures were supplied by the consulates or established empirically; for 1901 the Sûreté publique figure from the register of foreigners' declarations; from 1906 the quinquennial censuses.
- 1901: the cells sum to 111.071, 30 less than the printed total 111.101; the 1901 cells are flagged `total_mismatch`.
