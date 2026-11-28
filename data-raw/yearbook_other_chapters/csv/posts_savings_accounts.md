# Caisse nationale d'épargne. Comptes ouverts

*National savings bank (Caisse nationale d'épargne): accounts opened by depositor group, deposits, withdrawals and depositors' balance.*

Source: *Statistique générale de la Tunisie*, chapter *Postes - Télégraphes - Téléphones*, editions sgt1922, sgt1923, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 148, f172; sgt1923 (`bpt6k9105649x`): p. 160, f662; sgt1925 (`bpt6k9105650k`): p. 174, f198; sgt1926 (`bpt6k9105650k`): p. 189, f753; sgt1927 (`bpt6k91056510`): p. 187, f215; sgt1928 (`bpt6k91056510`): p. 187, f739; sgt1929 (`bpt6k9105652d`): p. 189, f217; sgt1930 (`bpt6k9105652d`): p. 193, f751; sgt1936 (`bpt6k91056547`): p. 72, f83; sgt1939 (`bpt6k9105739w`): p. 76, f82.

Transcriptions: `../transcribed/posts_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_posts.py build`.

Rows: 191. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Units: accounts opened (`count`) and francs (`francs`); suggested value_type: mixed.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing of the same cell, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`): the latest edition printing that year
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (network: situation at 31 December)
- `item`: item code (English)
- `item_fr`: printed line heading
- `unit`: `count`, `km` (kilometres) or `francs` (centimes kept as decimals)
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible` (NA, cut by the binding or broken type), `not_applicable` (nothing printed, or » in a line not yet collected; NA), `row_realigned` (printed in the wrong column or line, stored on the year / item it belongs to), `reprint_corrected` (kept from an earlier printing), `derived_from_totals`

Comptes ouverts: accounts (passbooks) opened by depositor group, with the amounts of deposits and withdrawals and the depositors' balance. The TOTAL column is used as a check only. sgt1939 prints the amounts only (1930-1939).

This table and the savings lines of the Exploitation table (in `posts_operations`) are printed separately and often disagree: sgt1923-sgt1928 keep 1923 deposits / withdrawals of 17.905.102 / 13.622.763 (Exploitation: 18.331.195 / 12.837.933) and print 1926-1928 amounts that differ from the Exploitation table; sgt1929 and later reprint the Exploitation figures. sgt1935 and sgt1936 print a table headed 1923-1934 whose 1932 deposits (19.584.818 06) and balance (18.940.606 76) and 1933 balance (130.473.218 88) differ from the Exploitation table (49.584.818 06, 118.939.778 24, 124.810.682 88), and whose line 1934 carries the 1935 Exploitation figures (8.432 passbooks; its depositor columns sum to 7.432); sgt1939 repeats these. Values are stored as printed (latest printing); see the comparison counts below and `posts_validation.json`.

Failed checks, grouped (printed values kept). A failure that recurs identically in several editions was read independently on each printing, so it is the printed figure; every failure printed by one edition only was re-read on a zoomed native-resolution crop: savings 1934 total: cells 7432, printed 8432 (in sgt1935, sgt1936).

Comparison with the Exploitation table of the same edition (not a check): 448 cells compared, 86 differ: sgt1922 1920 deposits: Comptes ouverts 12553210, Exploitation 12558210; sgt1922 1920 balance: Comptes ouverts 15643865, Exploitation 15646187; sgt1923 1920 deposits: Comptes ouverts 12553210, Exploitation 12558210; sgt1923 1920 balance: Comptes ouverts 15643865, Exploitation 15646187; sgt1923 1923 deposits: Comptes ouverts 17905102, Exploitation 18331195; sgt1923 1923 withdrawals: Comptes ouverts 13622763, Exploitation 12837933; sgt1923 1923 balance: Comptes ouverts 27376761, Exploitation 27376964; sgt1924 1920 deposits: Comptes ouverts 12553210, Exploitation 12558210; sgt1924 1920 balance: Comptes ouverts 15643865, Exploitation 15646187; sgt1924 1923 deposits: Comptes ouverts 17905102, Exploitation 18331195; sgt1924 1923 withdrawals: Comptes ouverts 13622763, Exploitation 12837933; sgt1924 1923 balance: Comptes ouverts 27376761, Exploitation 27376964; sgt1924 1924 deposits: Comptes ouverts 18204574, Exploitation 18204575; sgt1924 1924 withdrawals: Comptes ouverts 15355195, Exploitation 15355196; sgt1925 1920 deposits: Comptes ouverts 12553210, Exploitation 12558210; sgt1925 1920 balance: Comptes ouverts 15643865, Exploitation 15646187; sgt1925 1923 deposits: Comptes ouverts 17905102, Exploitation 18331195; sgt1925 1923 withdrawals: Comptes ouverts 13622763, Exploitation 12837933; sgt1925 1923 balance: Comptes ouverts 27376761, Exploitation 27376964; sgt1925 1924 deposits: Comptes ouverts 18204574, Exploitation 18204575; sgt1925 1924 withdrawals: Comptes ouverts 15355195, Exploitation 15355196; sgt1926 1920 deposits: Comptes ouverts 12553210, Exploitation 12558210; sgt1926 1920 balance: Comptes ouverts 15643865, Exploitation 15646187; sgt1926 1923 deposits: Comptes ouverts 17905102, Exploitation 18331195; sgt1926 1923 withdrawals: Comptes ouverts 13622763, Exploitation 12837933; sgt1926 1923 balance: Comptes ouverts 27376761, Exploitation 27376964; sgt1926 1924 deposits: Comptes ouverts 18204574, Exploitation 18204575; sgt1926 1924 withdrawals: Comptes ouverts 15355195, Exploitation 15355196; sgt1926 1926 deposits: Comptes ouverts 27749420.43, Exploitation 28191139.89; sgt1926 1926 withdrawals: Comptes ouverts 23075589.70, Exploitation 21563242.43; sgt1926 1926 balance: Comptes ouverts 39944497.25, Exploitation 39944197.25; sgt1927 1920 deposits: Comptes ouverts 12553210, Exploitation 12558210; sgt1927 1920 balance: Comptes ouverts 15643865, Exploitation 15646187; sgt1927 1923 deposits: Comptes ouverts 17905102, Exploitation 18331195; sgt1927 1923 withdrawals: Comptes ouverts 13622763, Exploitation 12837933; sgt1927 1923 balance: Comptes ouverts 27376761, Exploitation 27376964; sgt1927 1924 deposits: Comptes ouverts 18204574, Exploitation 18204575; sgt1927 1924 withdrawals: Comptes ouverts 15355195, Exploitation 15355196; sgt1927 1926 deposits: Comptes ouverts 27749420.43, Exploitation 28191139.89; sgt1927 1926 withdrawals: Comptes ouverts 23075589.70, Exploitation 21563242.43; sgt1927 1926 balance: Comptes ouverts 39944497.25, Exploitation 39944197.25; sgt1927 1927 deposits: Comptes ouverts 33948855.21, Exploitation 34454462.23; sgt1927 1927 withdrawals: Comptes ouverts 25748649.92, Exploitation 24635572.30; sgt1928 1920 deposits: Comptes ouverts 12553210, Exploitation 12558210; sgt1928 1920 balance: Comptes ouverts 15643865, Exploitation 15646187; sgt1928 1923 deposits: Comptes ouverts 17905102, Exploitation 18331195; sgt1928 1923 withdrawals: Comptes ouverts 13622763, Exploitation 12837933; sgt1928 1923 balance: Comptes ouverts 27376761, Exploitation 27376964; sgt1928 1924 deposits: Comptes ouverts 18204574, Exploitation 18204575; sgt1928 1924 withdrawals: Comptes ouverts 15355195, Exploitation 15355196; sgt1928 1926 deposits: Comptes ouverts 27749420.43, Exploitation 28191139.89; sgt1928 1926 withdrawals: Comptes ouverts 23075589.70, Exploitation 21563242.43; sgt1928 1926 balance: Comptes ouverts 39944497.25, Exploitation 39944197.25; sgt1928 1927 deposits: Comptes ouverts 33948855.21, Exploitation 34454462.23; sgt1928 1927 withdrawals: Comptes ouverts 25748649.92, Exploitation 24635572.30; sgt1928 1928 deposits: Comptes ouverts 40344601.79, Exploitation 40752109.41; sgt1928 1928 withdrawals: Comptes ouverts 32342445.65, Exploitation 29907758.35; sgt1928 1928 balance: Comptes ouverts 56580713.96, Exploitation 59580713.96; sgt1929 1924 deposits: Comptes ouverts 18204574, Exploitation 18204575; sgt1929 1924 withdrawals: Comptes ouverts 15355195, Exploitation 15355196; sgt1930 1924 deposits: Comptes ouverts 18204574, Exploitation 18204575; sgt1930 1924 withdrawals: Comptes ouverts 15355195, Exploitation 15355196; sgt1935 1932 deposits: Comptes ouverts 19584818.06, Exploitation 49584818.06; sgt1935 1932 balance: Comptes ouverts 18940606.76, Exploitation 118939778.24; sgt1935 1933 balance: Comptes ouverts 130473218.88, Exploitation 124810682.88; sgt1935 1934 deposits: Comptes ouverts 69419552.92, Exploitation 70750560.30; sgt1935 1934 withdrawals: Comptes ouverts 61920421.16, Exploitation 55119637.45; sgt1935 1934 balance: Comptes ouverts 156460180.65, Exploitation 125270197.75; sgt1935 1934 total: Comptes ouverts 8432, Exploitation 7920; sgt1936 1932 deposits: Comptes ouverts 19584818.06, Exploitation 49584818.06; sgt1936 1932 balance: Comptes ouverts 18940606.76, Exploitation 118939778.24; sgt1936 1933 balance: Comptes ouverts 130473218.88, Exploitation 124810682.88; sgt1936 1934 deposits: Comptes ouverts 69419552.92, Exploitation 70750560.30; sgt1936 1934 withdrawals: Comptes ouverts 61920421.16, Exploitation 55119637.45; sgt1936 1934 balance: Comptes ouverts 156460180.65, Exploitation 125270197.75; sgt1936 1934 total: Comptes ouverts 8432, Exploitation 7920; sgt1939 1933 balance: Comptes ouverts 130473218.88, Exploitation 124810682.88; sgt1939 1934 deposits: Comptes ouverts 69419552.92, Exploitation 70750560.30; sgt1939 1934 withdrawals: Comptes ouverts 61920421.16, Exploitation 55119637.45; sgt1939 1934 balance: Comptes ouverts 156460180.65, Exploitation 125270197.75; sgt1939 1935 withdrawals: Comptes ouverts 61930421.16, Exploitation 6920421.16; sgt1939 1936 deposits: Comptes ouverts 62995998.91, Exploitation 62992349.01; sgt1939 1936 withdrawals: Comptes ouverts 71009711.65, Exploitation 71006961.14; sgt1939 1937 deposits: Comptes ouverts 75306683.54, Exploitation 75306183.54; sgt1939 1937 withdrawals: Comptes ouverts 71326676.38, Exploitation 71325676.38; sgt1939 1937 balance: Comptes ouverts 160665339.95, Exploitation 160665844.50.

Survey of the whole chapter in every edition: `posts_survey.md`.

## Validation

- Checks against printed totals and identities: 115; passed: 113; failed: 2.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1935 p.95 (f115) savings 1934: total = french + muslim + jewish + italian + other_foreign: cells give 7432, printed 8432 (difference 1000)
  - sgt1936 p.72 (f83) savings 1934: total = french + muslim + jewish + italian + other_foreign: cells give 7432, printed 8432 (difference 1000)

- Overlapping printings: 759 cell comparisons with other editions printing the same cell; 71 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1920 / deposits | sgt1922 | 12553210 | sgt1929 | 12558210 |
| 1920 / deposits | sgt1923 | 12553210 | sgt1929 | 12558210 |
| 1920 / deposits | sgt1924 | 12553210 | sgt1929 | 12558210 |
| 1920 / deposits | sgt1925 | 12553210 | sgt1929 | 12558210 |
| 1920 / deposits | sgt1926 | 12553210 | sgt1929 | 12558210 |
| 1920 / deposits | sgt1927 | 12553210 | sgt1929 | 12558210 |
| 1920 / deposits | sgt1928 | 12553210 | sgt1929 | 12558210 |
| 1920 / depositors_balance | sgt1922 | 15643865 | sgt1929 | 15643865.54 |
| 1920 / depositors_balance | sgt1923 | 15643865 | sgt1929 | 15643865.54 |
| 1920 / depositors_balance | sgt1924 | 15643865 | sgt1929 | 15643865.54 |
| 1920 / depositors_balance | sgt1925 | 15643865 | sgt1929 | 15643865.54 |
| 1920 / depositors_balance | sgt1926 | 15643865 | sgt1929 | 15643865.54 |
| 1920 / depositors_balance | sgt1927 | 15643865 | sgt1929 | 15643865.54 |
| 1920 / depositors_balance | sgt1928 | 15643865 | sgt1929 | 15643865.54 |
| 1921 / depositors_balance | sgt1922 | 19153246 | sgt1930 | 19153246.25 |
| 1921 / depositors_balance | sgt1923 | 19153246 | sgt1930 | 19153246.25 |
| 1921 / depositors_balance | sgt1924 | 19153246 | sgt1930 | 19153246.25 |
| 1921 / depositors_balance | sgt1925 | 19153246 | sgt1930 | 19153246.25 |
| 1921 / depositors_balance | sgt1926 | 19153246 | sgt1930 | 19153246.25 |
| 1921 / depositors_balance | sgt1927 | 19153246 | sgt1930 | 19153246.25 |
| 1921 / depositors_balance | sgt1928 | 19153246 | sgt1930 | 19153246.25 |
| 1922 / depositors_balance | sgt1922 | 22123831 | sgt1930 | 22123831.99 |
| 1922 / depositors_balance | sgt1923 | 22123831 | sgt1930 | 22123831.99 |
| 1922 / depositors_balance | sgt1924 | 22123831 | sgt1930 | 22123831.99 |
| 1922 / depositors_balance | sgt1925 | 22123831 | sgt1930 | 22123831.99 |
| 1922 / depositors_balance | sgt1926 | 22123831 | sgt1930 | 22123831.99 |
| 1922 / depositors_balance | sgt1927 | 22123831 | sgt1930 | 22123831.99 |
| 1922 / depositors_balance | sgt1928 | 22123831 | sgt1930 | 22123831.99 |
| 1923 / deposits | sgt1923 | 17905102 | sgt1936 | 18331195 |
| 1923 / deposits | sgt1924 | 17905102 | sgt1936 | 18331195 |
| 1923 / deposits | sgt1925 | 17905102 | sgt1936 | 18331195 |
| 1923 / deposits | sgt1926 | 17905102 | sgt1936 | 18331195 |
| 1923 / deposits | sgt1927 | 17905102 | sgt1936 | 18331195 |
| 1923 / deposits | sgt1928 | 17905102 | sgt1936 | 18331195 |
| 1923 / withdrawals | sgt1923 | 13622763 | sgt1936 | 12837933 |
| 1923 / withdrawals | sgt1924 | 13622763 | sgt1936 | 12837933 |
| 1923 / withdrawals | sgt1925 | 13622763 | sgt1936 | 12837933 |
| 1923 / withdrawals | sgt1926 | 13622763 | sgt1936 | 12837933 |
| 1923 / withdrawals | sgt1927 | 13622763 | sgt1936 | 12837933 |
| 1923 / withdrawals | sgt1928 | 13622763 | sgt1936 | 12837933 |
| 1923 / depositors_balance | sgt1923 | 27376761 | sgt1936 | 27376761.87 |
| 1923 / depositors_balance | sgt1924 | 27376761 | sgt1936 | 27376761.87 |
| 1923 / depositors_balance | sgt1925 | 27376761 | sgt1936 | 27376761.87 |
| 1923 / depositors_balance | sgt1926 | 27376761 | sgt1936 | 27376761.87 |
| 1923 / depositors_balance | sgt1927 | 27376761 | sgt1936 | 27376761.87 |
| 1923 / depositors_balance | sgt1928 | 27376761 | sgt1936 | 27376761.87 |
| 1924 / depositors_balance | sgt1924 | 29912171 | sgt1936 | 29912171.27 |
| 1924 / depositors_balance | sgt1925 | 29912171 | sgt1936 | 29912171.27 |
| 1924 / depositors_balance | sgt1926 | 29912171 | sgt1936 | 29912171.27 |
| 1924 / depositors_balance | sgt1927 | 29912171 | sgt1936 | 29912171.27 |
| 1924 / depositors_balance | sgt1928 | 29912171 | sgt1936 | 29912171.27 |
| 1925 / depositors_balance | sgt1925 | 33880879 | sgt1936 | 33880879.61 |
| 1925 / depositors_balance | sgt1926 | 33880879 | sgt1936 | 33880879.61 |
| 1925 / depositors_balance | sgt1927 | 33880879 | sgt1936 | 33880879.61 |
| 1925 / depositors_balance | sgt1928 | 33880879 | sgt1936 | 33880879.61 |
| 1926 / deposits | sgt1926 | 27749420.43 | sgt1936 | 28191139 |
| 1926 / deposits | sgt1927 | 27749420.43 | sgt1936 | 28191139 |
| 1926 / deposits | sgt1928 | 27749420.43 | sgt1936 | 28191139 |
| 1926 / withdrawals | sgt1926 | 23075589.70 | sgt1936 | 21563242 |
| 1926 / withdrawals | sgt1927 | 23075589.70 | sgt1936 | 21563242 |
| 1926 / withdrawals | sgt1928 | 23075589.70 | sgt1936 | 21563242 |
| 1926 / depositors_balance | sgt1926 | 39944497.25 | sgt1936 | 39944197.25 |
| 1926 / depositors_balance | sgt1927 | 39944497.25 | sgt1936 | 39944197.25 |
| 1926 / depositors_balance | sgt1928 | 39944497.25 | sgt1936 | 39944197.25 |
| 1927 / deposits | sgt1927 | 33948855.21 | sgt1936 | 34454462 |
| 1927 / deposits | sgt1928 | 33948855.21 | sgt1936 | 34454462 |
| 1927 / withdrawals | sgt1927 | 25748649.92 | sgt1936 | 24635572 |
| 1927 / withdrawals | sgt1928 | 25748649.92 | sgt1936 | 24635572 |
| 1928 / deposits | sgt1928 | 40344601.79 | sgt1936 | 40752109 |
| 1928 / withdrawals | sgt1928 | 32342445.65 | sgt1936 | 29907758 |
| 1928 / depositors_balance | sgt1928 | 56580713.96 | sgt1936 | 59580713.96 |

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (12 printings): sgt1922 f172, sgt1923 f662, sgt1924 f1157, sgt1925 f198, sgt1926 f753, sgt1927 f215, sgt1928 f739, sgt1929 f217, sgt1930 f751, sgt1935 f115, sgt1936 f83, sgt1939 f82.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
