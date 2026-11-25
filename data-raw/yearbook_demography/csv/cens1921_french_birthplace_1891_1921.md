# cens1921_french_birthplace_1891_1921

**b) Population civile française d'après le lieu de naissance (recensements de 1891 à 1921)**  
*French civilian population by place of birth (Tunisia, Algerian départements, French départements, colonies, abroad), censuses 1891-1921*

Source: *Statistique générale de la Tunisie*, 1922 edition (sgt1922), chapter I *Démographie*, printed pages 4-6, Gallica views 28-30 of ark `bpt6k9105649x`. Source gallica.bnf.fr / Ministère des Affaires étrangères.

576 rows, one per printed cell. `birthplace_fr` as printed; `census_year` the census.

Common columns: `census` (source edition), `gallica_ark`, `table_id`, `source_page`, `gallica_view`, `census_year`, `value` (printed figure; » = 0), `flag` (see SPEC.md and SPEC_ADDENDUM.md).

## Validation

7 of 7 automated checks pass (printed row, column and grand totals, and cross-checks with the other 1921 tables and the 1906 census volume).
- 1891-1906 columns vs the 1906 census volume (Table E): 376 cells compared, 370 equal. Differences: Bouches-du-Rhône 1906: 1922 edition 922, 1906 volume 822; Calvados 1906: 1922 edition 55, 1906 volume 54; Gironde 1906: 1922 edition 374, 1906 volume 324; Var 1891: 1922 edition 110, 1906 volume 118; Var 1901: 1922 edition 286, 1906 volume 256; Etranger 1896: 1922 edition 679, 1906 volume 689. Each year's differences add up exactly to the gap between the 1906 volume's departement rows and its printed total (1891 +8, 1896 +10, 1901 -30, 1906 -151): the 1922 compilers appear to have made the old columns add up by adjusting one or a few cells, so these values are not independent evidence. The 1906 volume's commentary (pp.44-45) gives Bouches-du-Rhône 922 (supports this edition), but also Gironde 324 with +58 since 1901 and Var +147 since 1901 to 403, i.e. 256 in 1901 (both support the 1906 volume). Calvados, Var 1891 and Etranger 1896 cannot be checked against an independent source. Values are kept as printed in this edition and not flagged; for 1891-1906 prefer the 1906 volume's Table E (eur1906_te_french_by_birthplace_1891_1906), whose notes discuss the same cells.

## Reprints

sgt1923 and sgt1924 reprint all six census columns; sgt1925 reprints the 1921 column only. Compared through the OCR; every cell the OCR misses was checked on sgt1922 at native resolution.

OCR check (cells whose value occurs among the numbers Gallica's OCR reads on the reprint page; misses are OCR gaps, not differences):
- sgt1923 (views 506, 507, 508): 560 of 576
- sgt1924 (views 994, 995, 996): 561 of 576
- sgt1925 (views 28, 29, 30): 94 of 96

## Notes and footnotes

- (1) Moselle and Bas-Rhin were counted with the foreign population for 1891-1911 (printed as », stored 0).
- (2) Colonies and possessions other than Algeria and Tunisia. "Lieux inconnus" was used only in 1906.
- The 1921 grand total reads 54.426 in the half-resolution scan and in Gallica's OCR; at native resolution it is 54.476, which the column sums to and which equals the French total of table a).
- Five cells misread by the OCR were corrected from the image (`ocr_corrected`).
