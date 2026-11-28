# Crédit mutuel agricole. a) Caisses locales françaises et indigènes ; b) Effets escomptés

*Agricultural mutual credit: local credit banks (caisses) and members, French and indigenous, and bills discounted, by year (1913-1939).*

Source: *Statistique générale de la Tunisie*, chapter *Institutions économiques et sociales / Mutualité agricole*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 436, f460; sgt1923 (`bpt6k9105649x`): p. 448, f950; sgt1924 (`bpt6k9105649x`): p. 458, f1448; sgt1925 (`bpt6k9105650k`): p. 494, f518; sgt1926 (`bpt6k9105650k`): p. 462, f1026; sgt1927 (`bpt6k91056510`): p. 462, f490; sgt1928 (`bpt6k91056510`): p. 466, f1018; sgt1929 (`bpt6k9105652d`): p. 466, f494; sgt1930 (`bpt6k9105652d`): p. 472, f1030; sgt1935 (`bpt6k9105653t`): p. 289, f309; sgt1936 (`bpt6k91056547`): p. 172, f183; sgt1939 (`bpt6k9105739w`): p. 152, f158.

Transcriptions: `../transcribed/mutuality_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_mutuality.py build`.

Rows: 144. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Units: count (caisses, members, bills) and francs (amount of bills discounted, centimes as decimals); suggested value_type: mixed.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (rule 4 tables: the latest edition printing that year)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `caisse_group`: `french` = caisses françaises (sgt1922-sgt1928), caisses françaises et mixtes (sgt1929-sgt1930), caisses locales (sgt1935-sgt1939: one column, same figures for the overlapping years 1926-1930); `indigenous` = caisses indigènes (anciennes caisses indigènes in sgt1929-sgt1930; not printed from sgt1935); `all` = effets escomptés (not split)
- `caisse_group_fr`: printed column heading of the edition kept
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible`, `not_applicable`, `total_mismatch`, `ocr_corrected`

Printed in every edition for the ten years before it (sgt1939: 1929-1939). sgt1922-sgt1930: two tables, a) caisses locales (caisses françaises / caisses indigènes: number of caisses and members; sgt1929-sgt1930: caisses françaises et mixtes, adhérents français et indigènes, and anciennes caisses indigènes) and b) effets escomptés (number and amount). sgt1935-sgt1939: one table, caisses locales (number, adhérents français et tunisiens) and effets escomptés; its caisses locales column continues the French (and mixed) column (equal figures 1926-1930), so it is stored as `caisse_group` = `french` with its printed heading.

The number of effets escomptés for 1930 and 1932 is printed » (stored 0 as printed) although an amount is printed: the number was evidently not reported.

sgt1922 (f460) prints the whole series one year earlier than every later edition (its 1913-1920 figures are printed for 1914-1921 from sgt1923 on; its 1921 and 1922 caisses lines are equal; its 1922 effets, 2.511 / 13.465.233,15 fr., are printed by no other edition). The later, concordant editions are kept (rule 4); the sgt1922 differences are listed below. Only the 1913 line is taken from sgt1922 (1913 in sgt1922's labelling).

Survey of the whole chapter in every edition: `mutuality_survey.md`.

## Validation

- Checks against printed totals and identities: 0; passed: 0; failed: 0.

- Overlapping printings: 520 cell comparisons with other editions printing the same cell; 35 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1914 / french / members | sgt1922 | 565 | sgt1923 | 556 |
| 1914 / indigenous / local_caisses | sgt1922 | 41 | sgt1923 | 27 |
| 1914 / indigenous / members | sgt1922 | 1483 | sgt1923 | 849 |
| 1915 / french / members | sgt1922 | 548 | sgt1924 | 565 |
| 1915 / indigenous / local_caisses | sgt1922 | 40 | sgt1924 | 41 |
| 1915 / indigenous / members | sgt1922 | 1470 | sgt1924 | 1483 |
| 1916 / french / members | sgt1922 | 536 | sgt1925 | 548 |
| 1916 / indigenous / members | sgt1922 | 1464 | sgt1925 | 1470 |
| 1917 / french / members | sgt1922 | 517 | sgt1926 | 536 |
| 1917 / indigenous / local_caisses | sgt1922 | 38 | sgt1926 | 40 |
| 1917 / indigenous / members | sgt1922 | 1429 | sgt1926 | 1464 |
| 1918 / french / members | sgt1922 | 514 | sgt1927 | 517 |
| 1919 / french / members | sgt1922 | 508 | sgt1928 | 514 |
| 1920 / french / local_caisses | sgt1922 | 37 | sgt1929 | 24 |
| 1920 / french / members | sgt1922 | 668 | sgt1929 | 508 |
| 1921 / french / local_caisses | sgt1922 | 40 | sgt1930 | 37 |
| 1921 / french / members | sgt1922 | 735 | sgt1930 | 668 |
| 1914 / all / bills_discounted | sgt1922 | 4119 | sgt1923 | 4131 |
| 1914 / all / bills_discounted_amount | sgt1922 | 4728235.29 | sgt1923 | 5141876.90 |
| 1915 / all / bills_discounted | sgt1922 | 968 | sgt1924 | 4119 |
| 1915 / all / bills_discounted_amount | sgt1922 | 1127997.65 | sgt1924 | 4728235.29 |
| 1916 / all / bills_discounted | sgt1922 | 81 | sgt1925 | 968 |
| 1916 / all / bills_discounted_amount | sgt1922 | 186916.35 | sgt1925 | 1127997.65 |
| 1917 / all / bills_discounted | sgt1922 | 256 | sgt1926 | 81 |
| 1917 / all / bills_discounted_amount | sgt1922 | 328950 | sgt1926 | 186916.35 |
| 1918 / all / bills_discounted | sgt1922 | 107 | sgt1927 | 256 |
| 1918 / all / bills_discounted_amount | sgt1922 | 279840.50 | sgt1927 | 328950 |
| 1919 / all / bills_discounted | sgt1922 | 12 | sgt1928 | 107 |
| 1919 / all / bills_discounted_amount | sgt1922 | 23320.30 | sgt1928 | 279840.50 |
| 1920 / all / bills_discounted | sgt1922 | 459 | sgt1929 | 12 |
| 1920 / all / bills_discounted_amount | sgt1922 | 2355656.60 | sgt1929 | 23320.30 |
| 1921 / all / bills_discounted | sgt1922 | 2510 | sgt1930 | 459 |
| 1921 / all / bills_discounted_amount | sgt1922 | 13552423.85 | sgt1930 | 2355656.60 |
| 1922 / all / bills_discounted | sgt1922 | 2511 | sgt1930 | 2510 |
| 1922 / all / bills_discounted_amount | sgt1922 | 13465233.15 | sgt1930 | 13552423.85 |

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (21 printings): sgt1922 f460, sgt1922 f460, sgt1923 f950, sgt1923 f950, sgt1924 f1448, sgt1924 f1448, sgt1925 f518, sgt1925 f518, sgt1926 f1026, sgt1926 f1026, sgt1927 f490, sgt1927 f490, sgt1928 f1018, sgt1928 f1018, sgt1929 f494, sgt1929 f494, sgt1930 f1030, sgt1930 f1030, sgt1935 f309, sgt1936 f183, sgt1939 f158.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
