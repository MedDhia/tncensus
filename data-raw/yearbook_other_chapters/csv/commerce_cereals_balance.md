# Céréales : a) Importation et exportation par campagne commerciale

*Cereals: imports and exports by commercial campaign.*

Source: *Statistique générale de la Tunisie*, chapter *Commerce et navigation*, editions sgt1922, sgt1923, sgt1924. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 384, f408; sgt1923 (`bpt6k9105649x`): p. 396, f898; sgt1924 (`bpt6k9105649x`): p. 412, f1402, p. 413, f1403.

Transcriptions: `../transcribed/commerce_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_commerce.py build`.

Rows: 252. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924.

Unit: metric quintals, as printed. value_type: count (quantity).

Selection (SPEC_ADDENDUM rule 4): each edition prints the last ten campaigns (sgt1922 1912-1913 to 1921-1922, sgt1923 to 1922-1923, sgt1924 to 1923-1924); each campaign is stored once, from the latest edition printing it legibly; every other printing is compared and the differences listed below.

## Columns

- `census`: edition (each prints the last ten campaigns)
- `table_id`: `cereals` (Céréales : a) Importation et exportation par campagne commerciale)
- `gallica_ark`: Gallica volume ark
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year in which the commercial campaign ends (campaign 1912-1913 -> 1913)
- `campaign`: commercial campaign as printed (e.g. `1912-1913`)
- `product`: `wheat`, `flour`, `semolina_groats`, `semolina_pasta`, `barley`, `oats`, `maize`
- `product_fr`: line heading as printed
- `flow`: `import`, `export`, `balance` (balance = import - export, printed with its sign: + = excess of imports, - = excess of exports)
- `flow_fr`: Importation, Exportation, Balance
- `measure`: `quantity`
- `measure_fr`: quantité
- `unit`: `quintals` (printed *quint*, metric quintals)
- `value`: quantity as printed (» stored as 0); balances signed as printed
- `flag`: empty, `total_mismatch` or `row_realigned` (see notes)

Imports, exports and balance of cereals and cereal products by commercial campaign (quintals). Full printed title: *Céréales (blé dur et dérivés, blé tendre et dérivés, orge, avoine, maïs) : a) Importation et exportation par campagne commerciale*. Footnote (1) (translated): the sign + indicates the excess of imports over exports; the sign -, the excess of exports over imports. The balance line is printed and is stored as printed (signed), and also used as a check (balance = import - export). The three printed averages (*Moyenne des années*, two five-campaign and one ten-campaign average) were transcribed as checks and are not stored.

Gutter: the fourth campaign of each spread lies against the binding. sgt1922 1915-1916 maize (three cells) and sgt1923 1916-1917 (whole column) have digits hidden in the fold and were typed `?`; sgt1923 flour export 1914-1915 has its first digit under an ink blot (`?`). Each of these campaigns is legible in another printing, from which it is stored (latest legible printing). sgt1922 prints the flour import of 1912-1913 (596.204) one line too high, above *Importation*; stored on the import line (the balance 596.204 - 33.024 = 563.180 agrees), flagged `row_realigned`.

Explanation of the failed balance checks (each cell re-read on native-resolution crops of every printing; every one recurs identically in the two or three printings, each typed from its own image): maize 1916-1917 is printed *+ 16.720* in all three editions while exports (18.663) exceed imports (1.943); the printed five-campaign averages of sgt1924 (+57.407, i.e. the mean with - 16.720) confirm the negative value, so the cell is flagged `total_mismatch` (printed sign kept). Wheat 1919-1920 (703 - 311.077, printed - 311.374), wheat 1920-1921 (printed 497.996 for 498.096) and maize 1920-1921 (463.985 for 472.985): the printed averages of the balance that include these campaigns are higher by exactly (1.000 + 100) / 5 = 220 (wheat, all three editions) and 9.000 / 5 = 1.800 (maize, sgt1923 and sgt1924; sgt1922 2.400), i.e. they were computed from the correct balances; the three cells are flagged `total_mismatch` (printed value kept). Flour 1920-1921 (850 for 855), semolina in pasta 1913-1914 (2.843 for 2.793) and 1915-1916 (2.099 for 2.100): the import and export lines and the balance are each clearly printed and the averages do not decide; so nothing is flagged. sgt1923 prints the maize balance 1921-1922 as 8.673 (sgt1922 and sgt1924: 8.678, which agrees with 9.113 - 435); the sgt1924 value is stored.

Explanation of the remaining failed average checks (besides those explained above by the four flagged balances): the printed averages were evidently computed from figures differing slightly from the yearly lines (differences of a few units to a few hundred quintals on most lines, larger on balances, which the printer averaged from balances that do not always equal import - export). A few are grossly wrong (sgt1922 semolina in groats export 1912-13/1916-17 printed 55.405 where the five campaigns average 1.494; sgt1923 oats import 1918-19/1922-23 5.465 for 3.465; sgt1924 semolina in pasta export 1919-20/1923-24 3.090 for 6.091). The yearly cells concerned were re-read and stand as transcribed; averages are not stored, so nothing is flagged on their account.

Survey of the whole chapter: `commerce_survey.md`.

## Validation

- Checks against printed totals and identities: 342; passed: 290; failed: 52.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 1920-1921 flour: balance = import - export: cells give 855, printed 850 (difference -5)
  - sgt1922 1916-1917 maize: balance = import - export: cells give -16720, printed 16720 (difference 33440)
  - sgt1922 1920-1921 maize: balance = import - export: cells give 472985, printed 463985 (difference -9000)
  - sgt1922 1913-1914 semolina_pasta: balance = import - export: cells give 2793, printed 2843 (difference 50)
  - sgt1922 1915-1916 semolina_pasta: balance = import - export: cells give 2100, printed 2099 (difference -1)
  - sgt1922 1919-1920 wheat: balance = import - export: cells give -310374, printed -311374 (difference -1000)
  - sgt1922 1920-1921 wheat: balance = import - export: cells give 498096, printed 497996 (difference -100)
  - sgt1923 1920-1921 flour: balance = import - export: cells give 855, printed 850 (difference -5)
  - sgt1923 1920-1921 maize: balance = import - export: cells give 472985, printed 463985 (difference -9000)
  - sgt1923 1921-1922 maize: balance = import - export: cells give 8678, printed 8673 (difference -5)
  - sgt1923 1913-1914 semolina_pasta: balance = import - export: cells give 2793, printed 2843 (difference 50)
  - sgt1923 1915-1916 semolina_pasta: balance = import - export: cells give 2100, printed 2099 (difference -1)
  - sgt1923 1919-1920 wheat: balance = import - export: cells give -310374, printed -311374 (difference -1000)
  - sgt1923 1920-1921 wheat: balance = import - export: cells give 498096, printed 497996 (difference -100)
  - sgt1924 1920-1921 flour: balance = import - export: cells give 855, printed 850 (difference -5)
  - sgt1924 1916-1917 maize: balance = import - export: cells give -16720, printed 16720 (difference 33440)
  - sgt1924 1920-1921 maize: balance = import - export: cells give 472985, printed 463985 (difference -9000)
  - sgt1924 1915-1916 semolina_pasta: balance = import - export: cells give 2100, printed 2099 (difference -1)
  - sgt1924 1919-1920 wheat: balance = import - export: cells give -310374, printed -311374 (difference -1000)
  - sgt1924 1920-1921 wheat: balance = import - export: cells give 498096, printed 497996 (difference -100)
  - sgt1922 flour balance: printed average 1912-1913/1916-1917 = mean of the years: cells give 209156, printed 200150 (difference -9006)
  - sgt1922 flour balance: printed average 1912-1913/1921-1922 = mean of the years: cells give 121675, printed 121673 (difference -2)
  - sgt1922 flour import: printed average 1912-1913/1916-1917 = mean of the years: cells give 227626, printed 227620 (difference -6)
  - sgt1922 flour import: printed average 1912-1913/1921-1922 = mean of the years: cells give 141443, printed 141440 (difference -3)
  - sgt1922 maize balance: printed average 1917-1918/1921-1922 = mean of the years: cells give 90373, printed 92773 (difference 2400)
  - sgt1922 semolina_groats balance: printed average 1912-1913/1916-1917 = mean of the years: cells give 57366, printed 3455 (difference -53911)
  - sgt1922 semolina_groats balance: printed average 1912-1913/1921-1922 = mean of the years: cells give 24517, printed -2438 (difference -26955)
  - sgt1922 semolina_groats export: printed average 1912-1913/1916-1917 = mean of the years: cells give 1494, printed 55405 (difference 53911)
  - sgt1922 semolina_groats export: printed average 1912-1913/1921-1922 = mean of the years: cells give 7602, printed 34557 (difference 26955)
  - sgt1922 semolina_pasta import: printed average 1912-1913/1916-1917 = mean of the years: cells give 2320, printed 2330 (difference 10)
  - sgt1922 semolina_pasta import: printed average 1912-1913/1921-1922 = mean of the years: cells give 1866, printed 1871 (difference 5)
  - sgt1922 wheat balance: printed average 1912-1913/1916-1917 = mean of the years: cells give 208497, printed 208297 (difference -200)
  - sgt1922 wheat balance: printed average 1912-1913/1921-1922 = mean of the years: cells give 2100, printed 2210 (difference 110)
  - sgt1922 wheat balance: printed average 1917-1918/1921-1922 = mean of the years: cells give -204298, printed -204078 (difference 220)
  - sgt1923 maize balance: printed average 1918-1919/1922-1923 = mean of the years: cells give 132376, printed 134177 (difference 1801)
  - sgt1923 oats import: printed average 1918-1919/1922-1923 = mean of the years: cells give 3465, printed 5465 (difference 2000)
  - sgt1923 wheat balance: printed average 1918-1919/1922-1923 = mean of the years: cells give -92621, printed -92401 (difference 220)
  - sgt1924 flour balance: printed average 1914-1915/1923-1924 = mean of the years: cells give 68995, printed 67998 (difference -997)
  - sgt1924 flour balance: printed average 1919-1920/1923-1924 = mean of the years: cells give 74542, printed 74545 (difference 3)
  - sgt1924 flour import: printed average 1914-1915/1923-1924 = mean of the years: cells give 90697, printed 90699 (difference 2)
  - sgt1924 flour import: printed average 1919-1920/1923-1924 = mean of the years: cells give 104449, printed 104451 (difference 2)
  - sgt1924 maize balance: printed average 1914-1915/1918-1919 = mean of the years: cells give 64095, printed 57407 (difference -6688)
  - sgt1924 maize balance: printed average 1914-1915/1923-1924 = mean of the years: cells give 96816, printed 94373 (difference -2443)
  - sgt1924 maize balance: printed average 1919-1920/1923-1924 = mean of the years: cells give 129538, printed 131338 (difference 1800)
  - sgt1924 maize import: printed average 1919-1920/1923-1924 = mean of the years: cells give 138896, printed 138806 (difference -90)
  - sgt1924 oats export: printed average 1919-1920/1923-1924 = mean of the years: cells give 241590, printed 241582 (difference -8)
  - sgt1924 semolina_pasta export: printed average 1919-1920/1923-1924 = mean of the years: cells give 6091, printed 3090 (difference -3001)
  - sgt1924 wheat balance: printed average 1914-1915/1918-1919 = mean of the years: cells give -138176, printed -138162 (difference 14)
  - sgt1924 wheat balance: printed average 1914-1915/1923-1924 = mean of the years: cells give -126491, printed -126374 (difference 117)
  - sgt1924 wheat balance: printed average 1919-1920/1923-1924 = mean of the years: cells give -114806, printed -114586 (difference 220)
  - sgt1924 wheat import: printed average 1914-1915/1918-1919 = mean of the years: cells give 78946, printed 78959 (difference 13)
  - sgt1924 wheat import: printed average 1914-1915/1923-1924 = mean of the years: cells give 180654, printed 180660 (difference 6)

- Overlapping printings: 353 cell comparisons with other editions printing the same cell; 1 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1921-1922 / maize / balance | sgt1923 | 8673 | sgt1924 | 8678 |

- Flagged cells: row_realigned: 1, total_mismatch: 4.

  - sgt1922 p.384 1913 1912-1913 / flour / import / quantity / quintals = 596204 (row_realigned)
  - sgt1924 p.412 1917 1916-1917 / maize / balance / quantity / quintals = 16720 (total_mismatch)
  - sgt1924 p.413 1920 1919-1920 / wheat / balance / quantity / quintals = -311374 (total_mismatch)
  - sgt1924 p.413 1921 1920-1921 / wheat / balance / quantity / quintals = 497996 (total_mismatch)
  - sgt1924 p.413 1921 1920-1921 / maize / balance / quantity / quintals = 463985 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (6 printings): sgt1922 f408, sgt1922 f409, sgt1923 f898, sgt1923 f899, sgt1924 f1402, sgt1924 f1403.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
