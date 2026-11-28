# Voies ferrées. Résultats financiers de l'exploitation du réseau (Bône-Guelma / Compagnie Fermière des Chemins de fer tunisiens)

*Railways: financial results (guaranteed Medjerdah line, unguaranteed lines, whole network under the Convention of 22 June 1922).*

Source: *Statistique générale de la Tunisie*, chapter *Travaux publics*, editions sgt1923, sgt1924, sgt1925, sgt1926, sgt1928, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1923 (`bpt6k9105649x`): p. 166, f668; sgt1924 (`bpt6k9105649x`): p. 174, f1164; sgt1925 (`bpt6k9105650k`): p. 180, f204; sgt1926 (`bpt6k9105650k`): p. 196, f760; sgt1928 (`bpt6k91056510`): p. 194, f746; sgt1930 (`bpt6k9105652d`): p. 200, f758; sgt1935 (`bpt6k9105653t`): p. 102, f122; sgt1936 (`bpt6k91056547`): p. 78, f89; sgt1939 (`bpt6k9105739w`): p. 82, f88.

Transcriptions: `../transcribed/publicworks_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_publicworks.py build`.

Rows: 200. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Unit: francs; value_type: francs.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition; an aligned printing is preferred to a realigned one); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from: the latest edition printing that year (rule 5 tables: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `scheme`: financial scheme code
- `scheme_fr`: printed table title
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible`, `not_applicable` (nothing printed), `row_realigned` (printed on the wrong line, stored on the year it belongs to), `total_mismatch`

c) Ligne de la Medjerdah and d) lignes non garanties, 1913-1921 (printed in every edition to sgt1930); NOTA: from 1922 all lines are worked by the Compagnie Fermière on actual expenses. e) Ensemble du réseau sous le régime de la Convention du 22 juin 1922, from sgt1923 (c) in sgt1935-sgt1939); the latest year of each edition is printed "résultats provisoires" up to sgt1928. Footnote from sgt1928: the interest line represents only the interest on sums paid from the State reserve fund for complementary works (3e Avenant du 28 avril 1928).

Every failed check below was re-read on a zoomed native-resolution crop, or recurs unchanged in independent readings of several editions: they are printed errors (printed values kept). 1928 Trésor total 2.294.158 for parts summing to 2.294.150 (sgt1928-sgt1930); 1935 total 4.998.823 for 4.998.883 (sgt1935-sgt1939).

Survey of the whole chapter in every edition: `publicworks_survey.md`.

## Validation

- Checks against printed totals and identities: 161; passed: 155; failed: 6.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1928 p.194 (f746) fin_convention 1928: versements totaux = travaux + contrôle + intérêts: cells give 2294150, printed 2294158 (difference 8)
  - sgt1929 p.196 (f224) fin_convention 1928: versements totaux = travaux + contrôle + intérêts: cells give 2294150, printed 2294158 (difference 8)
  - sgt1930 p.200 (f758) fin_convention 1928: versements totaux = travaux + contrôle + intérêts: cells give 2294150, printed 2294158 (difference 8)
  - sgt1935 p.102 (f122) fin_convention 1935: versements totaux = travaux + contrôle + intérêts: cells give 4998883, printed 4998823 (difference -60)
  - sgt1936 p.78 (f89) fin_convention 1935: versements totaux = travaux + contrôle + intérêts: cells give 4998883, printed 4998823 (difference -60)
  - sgt1939 p.82 (f88) fin_convention 1935: versements totaux = travaux + contrôle + intérêts: cells give 4998883, printed 4998823 (difference -60)

- Overlapping printings: 700 cell comparisons with other editions printing the same cell; 13 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1923 / whole_network_convention_1922 / operating_deficit | sgt1923 | 9345555 | sgt1930 | 9311616 |
| 1923 / whole_network_convention_1922 / company_remuneration | sgt1923 | 905481 | sgt1930 | 905922 |
| 1924 / whole_network_convention_1922 / operating_deficit | sgt1924 | 12291742 | sgt1930 | 12283386 |
| 1924 / whole_network_convention_1922 / company_remuneration | sgt1924 | 853650 | sgt1930 | 853116 |
| 1924 / whole_network_convention_1922 / treasury_financial_charges | sgt1924 | 1492470 | sgt1930 | 1544459 |
| 1924 / whole_network_convention_1922 / treasury_total | sgt1924 | 2599434 | sgt1930 | 2651423 |
| 1925 / whole_network_convention_1922 / operating_deficit | sgt1925 | 12701196 | sgt1930 | 12676679 |
| 1925 / whole_network_convention_1922 / company_remuneration | sgt1925 | 925178 | sgt1930 | 925497 |
| 1926 / whole_network_convention_1922 / operating_deficit | sgt1926 | 15290365 | sgt1930 | 15256932 |
| 1926 / whole_network_convention_1922 / company_remuneration | sgt1926 | 1094667 | sgt1930 | 1095101 |
| 1927 / whole_network_convention_1922 / company_remuneration | sgt1927 | 1391330 | sgt1930 | 1391122 |
| 1929 / whole_network_convention_1922 / operating_deficit | sgt1929 | 24500714 | sgt1930 | 24487374 |
| 1929 / whole_network_convention_1922 / company_remuneration | sgt1929 | 2014151 | sgt1930 | 2013999 |

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (29 printings): sgt1922 f178, sgt1922 f178, sgt1923 f668, sgt1923 f668, sgt1923 f668, sgt1924 f1164, sgt1924 f1164, sgt1924 f1164, sgt1925 f204, sgt1925 f204, sgt1925 f204, sgt1926 f760, sgt1926 f760, sgt1926 f760, sgt1927 f222, sgt1927 f222, sgt1927 f222, sgt1928 f746, sgt1928 f746, sgt1928 f746, sgt1929 f224, sgt1929 f224, sgt1929 f224, sgt1930 f758, sgt1930 f758, sgt1930 f758, sgt1935 f122, sgt1936 f89, sgt1939 f88.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
