# Budget annuel. a) Recettes réalisées

*Annual budget of the Regency: realised receipts by budget chapter (exercices 1915-1938).*

Source: *Statistique générale de la Tunisie*, chapter *Finances*, editions sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1925 (`bpt6k9105650k`): p. 188, f212; sgt1926 (`bpt6k9105650k`): p. 204, f768; sgt1927 (`bpt6k91056510`): p. 202, f230; sgt1928 (`bpt6k91056510`): p. 202, f754; sgt1929 (`bpt6k9105652d`): p. 204, f232; sgt1930 (`bpt6k9105652d`): p. 208, f766, p. 209, f767; sgt1935 (`bpt6k9105653t`): p. 109, f129; sgt1936 (`bpt6k91056547`): p. 84, f95; sgt1939 (`bpt6k9105739w`): p. 88, f94.

Transcriptions: `../transcribed/finance_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_finance.py build`.

Rows: 224. Years: 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1932, 1933, 1934, 1935, 1936, 1937, 1938.

Unit: francs (centimes kept); value_type: francs.

Printed for overlapping windows of exercices: each exercice is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (rule 4 tables: the latest edition printing that year)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: budget year (exercice) as printed in the column head
- `exercice_months`: length of the exercice in months: 9 for 1932 (printed "1932 (9 mois)" in sgt1935, the transition to the April-March budget year), 12 otherwise (printed "(12 mois)" for 1933 and 1934 in sgt1935, not printed elsewhere)
- `basis`: `actual` (réalisations: realised receipts, expenditure as finally settled); the chapter prints no budget forecasts (prévisions)
- `basis_fr`: printed table subtitle
- `part`: `ordinary` (Titre premier / Première partie), `exceptional` (Titre II / Deuxième partie), `closed` (Titre III / Troisième partie: exercices clos et périmés)
- `part_fr`: printed part heading
- `item`: budget line code (English). Expenditure: `<part>_<service>`, stable across the renumbering of the chapters (1932, 1938)
- `item_fr`: printed line label, with the chapter number of that edition's nomenclature
- `nomenclature_fr`: nomenclature named in the table head of the printing the value comes from
- `unit`: unit of `value`
- `value`: printed amount (» = 0), francs with centimes
- `flag`: empty, or `ocr_corrected` (image reading differs from the Gallica OCR)

Printed sgt1925-sgt1939 (not in sgt1922-sgt1924): ten exercices per edition up to sgt1930 (sgt1925: 1915-1924, ..., sgt1930: 1920-1929), three from sgt1935 (1932-1934, 1933-1935, 1936-1938). Exercices 1930 and 1931 are printed in no edition of the series (sgt1931-sgt1934 are not in the collection). Lines: Titre I (Première partie up to sgt1927) ressources ordinaires, chapitres I-V; Titre II recettes sur ressources exceptionnelles (fonds d'emprunt, recettes diverses, and recettes à la disposition des Conseils de Région, sgt1925-sgt1930); Titre III recettes affectées aux dépenses des exercices clos et périmés (» in every printing). sgt1939 uses a new detailed nomenclature for the ordinary resources (17 lines, by tax) and prints Total du Titre Ier and Total du Titre II (checks only); its exercices 1936-1938 overlap no other printing.

All figures are actual results (réalisations); the chapter prints no forecasts. The printed Total général is a check, not stored.

Printed errors (each failing figure re-read on zoomed native-resolution crops; the same standing type was reused from sgt1925 to sgt1930, so the same errors recur in every printing): receipts 1918 total 115.996.425 65 for lines summing to 110.996.425 65 (5.000.000 more; Chapitre II is printed 31.131.869 63 in every edition); 1919 total 159.571.187 15 for 159.571.097 15 (90); 1920 total 230.414.262 05 for 230.414.265 05 (-3); 1923 total 273.494.795 97 for 273.424.795 97 (70.000). sgt1929 prints 1927 Produits divers 14.055.295 30 (sgt1928 and sgt1930: 14.055.235 30, which the total requires; kept from sgt1930). Expenditure 1920 total 247.894.268 84 for 247.894.258 84 (10); 1921 total 323.893.637 49 for 323.893.837 09 (-199,60); 1922 total 358.708.699 43 for 358.708.657 43 (42); 1923 total 316.939.974 19 for 316.939.974 22 (-0,03); sgt1939 1936 total 728.768.074 68 for 729.768.074 68 (-1.000.000; only printing). The faulty cell cannot be identified in any of these (the line items agree across all independent printings), so no cell is flagged `total_mismatch`.

Survey of the whole chapter in every edition: `finance_survey.md`.

## Validation

- Checks against printed totals and identities: 75; passed: 53; failed: 22.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1925 p.189 (f213) receipts 1918: Total général = sum of the lines: cells give 110996425.65, printed 115996425.65 (difference 5000000.00)
  - sgt1925 p.189 (f213) receipts 1919: Total général = sum of the lines: cells give 159571097.15, printed 159571187.15 (difference 90.00)
  - sgt1925 p.189 (f213) receipts 1920: Total général = sum of the lines: cells give 230414265.05, printed 230414262.05 (difference -3.00)
  - sgt1925 p.189 (f213) receipts 1923: Total général = sum of the lines: cells give 273424795.97, printed 273494795.97 (difference 70000.00)
  - sgt1926 p.204 (f768) receipts 1918: Total général = sum of the lines: cells give 110996425.65, printed 115996425.65 (difference 5000000.00)
  - sgt1926 p.205 (f769) receipts 1919: Total général = sum of the lines: cells give 159571097.15, printed 159571187.15 (difference 90.00)
  - sgt1926 p.205 (f769) receipts 1920: Total général = sum of the lines: cells give 230414265.05, printed 230414262.05 (difference -3.00)
  - sgt1926 p.205 (f769) receipts 1923: Total général = sum of the lines: cells give 273424795.97, printed 273494795.97 (difference 70000.00)
  - sgt1927 p.202 (f230) receipts 1918: Total général = sum of the lines: cells give 110996425.65, printed 115996425.65 (difference 5000000.00)
  - sgt1927 p.202 (f230) receipts 1919: Total général = sum of the lines: cells give 159571097.15, printed 159571187.15 (difference 90.00)
  - sgt1927 p.203 (f231) receipts 1920: Total général = sum of the lines: cells give 230414265.05, printed 230414262.05 (difference -3.00)
  - sgt1927 p.203 (f231) receipts 1923: Total général = sum of the lines: cells give 273424795.97, printed 273494795.97 (difference 70000.00)
  - sgt1928 p.202 (f754) receipts 1918: Total général = sum of the lines: cells give 110996425.65, printed 115996425.65 (difference 5000000.00)
  - sgt1928 p.202 (f754) receipts 1919: Total général = sum of the lines: cells give 159571097.15, printed 159571187.15 (difference 90.00)
  - sgt1928 p.202 (f754) receipts 1920: Total général = sum of the lines: cells give 230414265.05, printed 230414262.05 (difference -3.00)
  - sgt1928 p.203 (f755) receipts 1923: Total général = sum of the lines: cells give 273424795.97, printed 273494795.97 (difference 70000.00)
  - sgt1929 p.204 (f232) receipts 1919: Total général = sum of the lines: cells give 159571097.15, printed 159571187.15 (difference 90.00)
  - sgt1929 p.204 (f232) receipts 1920: Total général = sum of the lines: cells give 230414265.05, printed 230414262.05 (difference -3.00)
  - sgt1929 p.205 (f233) receipts 1923: Total général = sum of the lines: cells give 273424795.97, printed 273494795.97 (difference 70000.00)
  - sgt1929 p.205 (f233) receipts 1927: Total général = sum of the lines: cells give 474113088.72, printed 474113028.72 (difference -60.00)
  - sgt1930 p.208 (f766) receipts 1920: Total général = sum of the lines: cells give 230414265.05, printed 230414262.05 (difference -3.00)
  - sgt1930 p.209 (f767) receipts 1923: Total général = sum of the lines: cells give 273424795.97, printed 273494795.97 (difference 70000.00)

- Overlapping printings: 421 cell comparisons with other editions printing the same cell; 1 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1927 / miscellaneous | sgt1929 | 14055295.30 | sgt1930 | 14055235.30 |

- Flagged cells: ocr_corrected: 1.

  - sgt1936 p.84 1935 12 / actual / ordinary / indirect_taxes / francs = 266301563.23 (ocr_corrected)

## Image versus OCR

- Read cell by cell on the page images (15 printings): sgt1925 f212, sgt1925 f213, sgt1926 f768, sgt1926 f769, sgt1927 f230, sgt1927 f231, sgt1928 f754, sgt1928 f755, sgt1929 f232, sgt1929 f233, sgt1930 f766, sgt1930 f767, sgt1935 f129, sgt1936 f95, sgt1939 f94.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 1.
