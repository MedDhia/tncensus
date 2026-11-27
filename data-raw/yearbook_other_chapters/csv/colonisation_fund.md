# Fonds de colonisation. Achats réalisés

*Colonisation fund: endowments, annual receipts and expenditure, and area of the properties bought (1900-1928).*

Source: *Statistique générale de la Tunisie*, chapter *Colonisation*, editions sgt1928. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1928 (`bpt6k91056510`): p. 462, f1014, p. 463, f1015.

Transcriptions: `../transcribed/colonisation_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_colonisation.py build`.

Rows: 116. Years: 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928.

Units: francs (centimes as decimals) and hectares (`unit`); suggested value_type: mixed.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (rule 4 tables: the latest edition printing that year)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `endowment_origin_fr`: printed origin of the endowment (dotation lines only; » = ditto / none; footnote calls kept)
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible`, `not_applicable`, `total_mismatch`, `ocr_corrected`

Printed in sgt1922-sgt1928 (1900 to the edition year); not printed from sgt1929. Footnotes (observations column): (1) Décret du 24 septembre 1900; (2) Décret du 30 décembre 1903; (3) Décret du 28 décembre 1905; (4) Décret du 25 mai 1905; (5) Décret du 31 décembre 1907; (6) Décret du 31 décembre 1908; (7) Emprunt 1920 : 1re tranche; (8) Emprunt 1920 : 2e tranche (from sgt1924). sgt1926 prints 1926 as "Dotation accordée en 1926 (1)" with footnote (1) Inscrit au budget 1927; sgt1927-sgt1928 print "Subvention accordée en 1926" (sgt1927 keeps the footnote without its call). From 1926 the area column has ares (hectares with two decimals).

Under the TOTAL line the dotations and recettes totals are added into one printed figure (checked). sgt1922 prints the dépenses total twice.

Every failed check below was re-read on a native-resolution crop: the printed values are kept. sgt1922 recettes total 24.865.246,53 for years summing to 24.860.246,53 (5.000 more; later editions print totals consistent with the same yearly figures); sgt1922 dépenses total 38.867.034,51 for 38.867.043,51 (digits 34/43 transposed), sgt1927 65.881.547,53 for 65.881.548,53, sgt1928 93.069.400,25 for 93.069.401,15 (small printed errors; every yearly figure equal in all seven printings).

Survey of the whole chapter in every edition: `colonisation_survey.md`.

## Validation

- Checks against printed totals and identities: 35; passed: 31; failed: 4.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.426 (f450) fund rec: TOTAL = sum of the years: cells give 24860246.53, printed 24865246.53 (difference 5000.00)
  - sgt1922 p.426 (f450) fund dep: TOTAL = sum of the years: cells give 38867043.51, printed 38867034.51 (difference -9.00)
  - sgt1927 p.458 (f486) fund dep: TOTAL = sum of the years: cells give 65881548.53, printed 65881547.53 (difference -1.00)
  - sgt1928 p.462 (f1014) fund dep: TOTAL = sum of the years: cells give 93069401.15, printed 93069400.25 (difference -0.90)

- Overlapping printings: 612 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (7 printings): sgt1922 f450, sgt1923 f940, sgt1924 f1442, sgt1925 f510, sgt1926 f1022, sgt1927 f486, sgt1928 f1014.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
