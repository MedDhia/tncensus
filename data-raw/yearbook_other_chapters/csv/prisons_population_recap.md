# Récapitulation du chiffre des détenus

*Prison population: yearly summary.*

Source: *Statistique générale de la Tunisie*, chapter *Établissements pénitentiaires*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 78, f102; sgt1923 (`bpt6k9105649x`): p. 84, f586; sgt1924 (`bpt6k9105649x`): p. 86, f1076; sgt1925 (`bpt6k9105650k`): p. 88, f112; sgt1926 (`bpt6k9105650k`): p. 99, f663; sgt1927 (`bpt6k91056510`): p. 101, f125; sgt1928 (`bpt6k91056510`): p. 97, f649; sgt1929 (`bpt6k9105652d`): p. 99, f127; sgt1930 (`bpt6k9105652d`): p. 103, f661; sgt1935 (`bpt6k9105653t`): p. 69, f89; sgt1936 (`bpt6k91056547`): p. 50, f61; sgt1939 (`bpt6k9105739w`): p. 50, f56.

Transcriptions: `../transcribed/prisons_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_prisons.py build`.

Rows: 156. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Unit: persons (population figures and average), entries / releases (count), days of detention.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing is compared below.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section name (`recap`)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: calendar year of the figures
- `measure`: `start`, `entries`, `exits`, `end`, `detention_days`, `average`
- `measure_fr`: printed column heading
- `value`: number of prisoners (start, end, average), of entries / releases, or of days of detention
- `flag`: empty, `illegible` or `reprint_corrected`

"Récapitulation du chiffre des détenus" ("Récapitulation" with ten years up to sgt1924, two years sgt1925-sgt1930, three in sgt1935, five in sgt1936 and sgt1939): for all the prisons of the Regency, the number of prisoners at 1 January, entries, releases, number at 31 December, days of detention and the average daily population (*effectif moyen*). The year 1931 is not printed by any edition; 1932 is printed only by sgt1936.

Checks: end = start + entries − releases; start of year N+1 = end of year N; average = days of detention / days in the year (to ±1).

Cells stored from an earlier printing (flag `reprint_corrected`): 1934 end: 2638 from sgt1935 (sgt1936 prints the 31 December 1934 population with its middle digit broken ("2 6·8"); sgt1935 prints 2.638, which is also sgt1935's and sgt1936's 1 January 1935 figure).

sgt1924 reprints 1915 with end 3.082 and 1.012.231 days (sgt1922-sgt1923: 2.874 and 1.092.231); the latest printing is stored by rule 4 (3.082 also satisfies 3.147 + 23.044 − 23.109), the earlier figures are listed among the differences.

Survey of the whole chapter in every edition, and the tables not yet transcribed: `prisons_survey.md`.

## Validation

- Checks against printed totals and identities: 151; passed: 111; failed: 40.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.78 (f102) recap 1913: end = start + entries - exits: cells give 2824, printed 2724 (difference -100)
  - sgt1922 p.78 (f102) recap 1913: average = detention days / 365 (to 1): cells give 2508, printed 2510 (difference 2)
  - sgt1922 p.78 (f102) recap start 1914 = end 1913: cells give 2724, printed 2726 (difference 2)
  - sgt1922 p.78 (f102) recap 1914: end = start + entries - exits: cells give 2363, printed 3147 (difference 784)
  - sgt1922 p.78 (f102) recap 1914: average = detention days / 365 (to 1): cells give 2782, printed 2773 (difference -9)
  - sgt1922 p.78 (f102) recap 1915: end = start + entries - exits: cells give 3082, printed 2874 (difference -208)
  - sgt1922 p.78 (f102) recap 1915: average = detention days / 365 (to 1): cells give 2992, printed 2969 (difference -23)
  - sgt1922 p.78 (f102) recap 1917: end = start + entries - exits: cells give 4128, printed 3128 (difference -1000)
  - sgt1922 p.78 (f102) recap start 1918 = end 1917: cells give 3128, printed 3012 (difference -116)
  - sgt1922 p.78 (f102) recap start 1919 = end 1918: cells give 2730, printed 2732 (difference 2)
  - sgt1922 p.78 (f102) recap 1919: average = detention days / 365 (to 1): cells give 2847, printed 2751 (difference -96)
  - sgt1922 p.78 (f102) recap start 1920 = end 1919: cells give 2770, printed 2735 (difference -35)
  - sgt1922 p.78 (f102) recap 1920: average = detention days / 366 (to 1): cells give 3303, printed 3087 (difference -216)
  - sgt1922 p.78 (f102) recap start 1921 = end 1920: cells give 3440, printed 3457 (difference 17)
  - sgt1922 p.78 (f102) recap start 1922 = end 1921: cells give 3335, printed 3322 (difference -13)
  - sgt1923 p.84 (f586) recap 1914: end = start + entries - exits: cells give 2363, printed 3147 (difference 784)
  - sgt1923 p.84 (f586) recap 1914: average = detention days / 365 (to 1): cells give 2782, printed 2773 (difference -9)
  - sgt1923 p.84 (f586) recap 1915: end = start + entries - exits: cells give 3082, printed 2874 (difference -208)
  - sgt1923 p.84 (f586) recap 1915: average = detention days / 365 (to 1): cells give 2992, printed 2969 (difference -23)
  - sgt1923 p.84 (f586) recap 1917: end = start + entries - exits: cells give 4128, printed 3128 (difference -1000)
  - sgt1923 p.84 (f586) recap start 1918 = end 1917: cells give 3128, printed 3012 (difference -116)
  - sgt1923 p.84 (f586) recap start 1919 = end 1918: cells give 2730, printed 2732 (difference 2)
  - sgt1923 p.84 (f586) recap 1919: average = detention days / 365 (to 1): cells give 2847, printed 2751 (difference -96)
  - sgt1923 p.84 (f586) recap start 1920 = end 1919: cells give 2770, printed 2735 (difference -35)
  - sgt1923 p.84 (f586) recap 1920: average = detention days / 366 (to 1): cells give 3303, printed 3087 (difference -216)
  - sgt1923 p.84 (f586) recap start 1921 = end 1920: cells give 3440, printed 3457 (difference 17)
  - sgt1923 p.84 (f586) recap start 1922 = end 1921: cells give 3335, printed 3322 (difference -13)
  - sgt1924 p.86 (f1076) recap 1915: average = detention days / 365 (to 1): cells give 2773, printed 2969 (difference 196)
  - sgt1924 p.86 (f1076) recap start 1916 = end 1915: cells give 3082, printed 2874 (difference -208)
  - sgt1924 p.86 (f1076) recap 1917: end = start + entries - exits: cells give 4128, printed 3128 (difference -1000)
  - sgt1924 p.86 (f1076) recap start 1918 = end 1917: cells give 3128, printed 3012 (difference -116)
  - sgt1924 p.86 (f1076) recap start 1919 = end 1918: cells give 2730, printed 2732 (difference 2)
  - sgt1924 p.86 (f1076) recap 1919: average = detention days / 365 (to 1): cells give 2847, printed 2751 (difference -96)
  - sgt1924 p.86 (f1076) recap start 1920 = end 1919: cells give 2770, printed 2735 (difference -35)
  - sgt1924 p.86 (f1076) recap 1920: average = detention days / 366 (to 1): cells give 3303, printed 3087 (difference -216)
  - sgt1924 p.86 (f1076) recap start 1921 = end 1920: cells give 3440, printed 3457 (difference 17)
  - sgt1924 p.86 (f1076) recap start 1922 = end 1921: cells give 3335, printed 3322 (difference -13)
  - sgt1930 p.103 (f661) recap 1930: average = detention days / 365 (to 1): cells give 2487, printed 2479 (difference -8)
  - sgt1936 p.50 (f61) recap 1936: average = detention days / 366 (to 1): cells give 3190, printed 3198 (difference 8)
  - sgt1939 p.50 (f56) recap 1936: average = detention days / 366 (to 1): cells give 3190, printed 3198 (difference 8)

- Overlapping printings: 174 cell comparisons with other editions printing the same cell; 5 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1915 / end | sgt1922 | 2874 | sgt1924 | 3082 |
| 1915 / end | sgt1923 | 2874 | sgt1924 | 3082 |
| 1915 / detention_days | sgt1922 | 1092231 | sgt1924 | 1012231 |
| 1915 / detention_days | sgt1923 | 1092231 | sgt1924 | 1012231 |
| 1934 / end | sgt1935 | 2638 | sgt1936 |  |

- Flagged cells: reprint_corrected: 1.

  - sgt1935 p.69 1934 end = 2638 (reprint_corrected)

## Image versus OCR

- Read cell by cell on the page images (10 printings): sgt1923 f586, sgt1925 f112, sgt1926 f663, sgt1927 f125, sgt1928 f649, sgt1929 f127, sgt1930 f661, sgt1935 f89, sgt1936 f61, sgt1939 f56.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (2 printings): sgt1922 f102, sgt1924 f1076.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
