# Budget annuel. b) Dépenses : droits constatés définitivement liquidés lors des règlements des budgets des exercices

*Annual budget of the Regency: expenditure as finally settled, by service (exercices 1915-1938).*

Source: *Statistique générale de la Tunisie*, chapter *Finances*, editions sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1925 (`bpt6k9105650k`): p. 190, f214; sgt1926 (`bpt6k9105650k`): p. 206, f770; sgt1927 (`bpt6k91056510`): p. 204, f232; sgt1928 (`bpt6k91056510`): p. 204, f756; sgt1929 (`bpt6k9105652d`): p. 206, f234; sgt1930 (`bpt6k9105652d`): p. 210, f768, p. 211, f769; sgt1935 (`bpt6k9105653t`): p. 110, f130; sgt1936 (`bpt6k91056547`): p. 85, f96; sgt1939 (`bpt6k9105739w`): p. 89, f95.

Transcriptions: `../transcribed/finance_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_finance.py build`.

Rows: 425. Years: 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1932, 1933, 1934, 1935, 1936, 1937, 1938.

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

Printed sgt1925-sgt1939, same windows as the receipts. Lines: Titre I dépenses sur ressources ordinaires and Titre II dépenses sur ressources exceptionnelles ou spéciales, by service (chapitre), and Titre III dépenses des exercices clos et périmés. The chapters are renumbered twice: nomenclature 1926-1929 (I Finances, II Postes et Télégraphes, III Intérieur, IV Agriculture-Commerce-Colonisation, V Instruction publique, VI Armée, VII Travaux publics, VIII Justice, IX Dépenses imprévues, from the 1927 nomenclature X Dépenses d'outillage économique), nomenclature 1932 and 1935 (II Secrétariat général du Gouvernement tunisien, VIII Justice tunisienne, IX Postes, X imprévues; from 1935 IV is the Direction des Affaires Économiques) and 1938 (III Postes; Intérieur and Administration tunisienne as "Mémoire" lines with 1936 figures only). `item` names the service, so the same service keeps its code across renumberings; `item_fr` keeps the printed chapter number. The Affaires Économiques line is coded with the Agriculture line it replaces (`agriculture_economy`).

All figures are actual results; the printed Total général is a check, not stored.

Printed errors (each failing figure re-read on zoomed native-resolution crops; the same standing type was reused from sgt1925 to sgt1930, so the same errors recur in every printing): receipts 1918 total 115.996.425 65 for lines summing to 110.996.425 65 (5.000.000 more; Chapitre II is printed 31.131.869 63 in every edition); 1919 total 159.571.187 15 for 159.571.097 15 (90); 1920 total 230.414.262 05 for 230.414.265 05 (-3); 1923 total 273.494.795 97 for 273.424.795 97 (70.000). sgt1929 prints 1927 Produits divers 14.055.295 30 (sgt1928 and sgt1930: 14.055.235 30, which the total requires; kept from sgt1930). Expenditure 1920 total 247.894.268 84 for 247.894.258 84 (10); 1921 total 323.893.637 49 for 323.893.837 09 (-199,60); 1922 total 358.708.699 43 for 358.708.657 43 (42); 1923 total 316.939.974 19 for 316.939.974 22 (-0,03); sgt1939 1936 total 728.768.074 68 for 729.768.074 68 (-1.000.000; only printing). The faulty cell cannot be identified in any of these (the line items agree across all independent printings), so no cell is flagged `total_mismatch`.

Survey of the whole chapter in every edition: `finance_survey.md`.

## Validation

- Checks against printed totals and identities: 69; passed: 44; failed: 25.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1925 p.191 (f215) expenditure 1920: Total général = sum of the lines: cells give 247894258.84, printed 247894268.84 (difference 10.00)
  - sgt1925 p.191 (f215) expenditure 1921: Total général = sum of the lines: cells give 323893837.09, printed 323893637.49 (difference -199.60)
  - sgt1925 p.191 (f215) expenditure 1922: Total général = sum of the lines: cells give 358708657.43, printed 358708699.43 (difference 42.00)
  - sgt1925 p.191 (f215) expenditure 1923: Total général = sum of the lines: cells give 316939974.22, printed 316939974.19 (difference -0.03)
  - sgt1926 p.207 (f771) expenditure 1920: Total général = sum of the lines: cells give 247894258.84, printed 247894268.84 (difference 10.00)
  - sgt1926 p.207 (f771) expenditure 1921: Total général = sum of the lines: cells give 323893837.09, printed 323893637.49 (difference -199.60)
  - sgt1926 p.207 (f771) expenditure 1922: Total général = sum of the lines: cells give 358708657.43, printed 358708699.43 (difference 42.00)
  - sgt1926 p.207 (f771) expenditure 1923: Total général = sum of the lines: cells give 316939974.22, printed 316939974.19 (difference -0.03)
  - sgt1927 p.205 (f233) expenditure 1920: Total général = sum of the lines: cells give 247894258.84, printed 247894268.84 (difference 10.00)
  - sgt1927 p.205 (f233) expenditure 1921: Total général = sum of the lines: cells give 323893837.09, printed 323893637.49 (difference -199.60)
  - sgt1927 p.205 (f233) expenditure 1922: Total général = sum of the lines: cells give 358708657.43, printed 358708699.43 (difference 42.00)
  - sgt1927 p.205 (f233) expenditure 1923: Total général = sum of the lines: cells give 316939974.22, printed 316939974.19 (difference -0.03)
  - sgt1928 p.204 (f756) expenditure 1920: Total général = sum of the lines: cells give 247894258.84, printed 247894268.84 (difference 10.00)
  - sgt1928 p.205 (f757) expenditure 1921: Total général = sum of the lines: cells give 323893837.09, printed 323893637.49 (difference -199.60)
  - sgt1928 p.205 (f757) expenditure 1922: Total général = sum of the lines: cells give 358708657.43, printed 358708699.43 (difference 42.00)
  - sgt1928 p.205 (f757) expenditure 1923: Total général = sum of the lines: cells give 316939974.22, printed 316939974.19 (difference -0.03)
  - sgt1929 p.206 (f234) expenditure 1920: Total général = sum of the lines: cells give 247894258.84, printed 247894268.84 (difference 10.00)
  - sgt1929 p.206 (f234) expenditure 1921: Total général = sum of the lines: cells give 323893837.09, printed 323893637.49 (difference -199.60)
  - sgt1929 p.207 (f235) expenditure 1922: Total général = sum of the lines: cells give 358708657.43, printed 358708699.43 (difference 42.00)
  - sgt1929 p.207 (f235) expenditure 1923: Total général = sum of the lines: cells give 316939974.22, printed 316939974.19 (difference -0.03)
  - sgt1930 p.210 (f768) expenditure 1920: Total général = sum of the lines: cells give 247894258.84, printed 247894268.84 (difference 10.00)
  - sgt1930 p.210 (f768) expenditure 1921: Total général = sum of the lines: cells give 323893837.09, printed 323893637.49 (difference -199.60)
  - sgt1930 p.210 (f768) expenditure 1922: Total général = sum of the lines: cells give 358708657.43, printed 358708699.43 (difference 42.00)
  - sgt1930 p.211 (f769) expenditure 1923: Total général = sum of the lines: cells give 316939974.22, printed 316939974.19 (difference -0.03)
  - sgt1939 p.89 (f95) expenditure 1936: Total général = sum of the lines: cells give 729768074.68, printed 728768074.68 (difference -1000000.00)

- Overlapping printings: 868 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (15 printings): sgt1925 f214, sgt1925 f215, sgt1926 f770, sgt1926 f771, sgt1927 f232, sgt1927 f233, sgt1928 f756, sgt1928 f757, sgt1929 f234, sgt1929 f235, sgt1930 f768, sgt1930 f769, sgt1935 f130, sgt1936 f96, sgt1939 f95.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
