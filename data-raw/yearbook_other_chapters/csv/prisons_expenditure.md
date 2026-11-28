# Tableau comparatif des dépenses et des journées de détention

*Expenditure and days of detention, by prison (cost per day of detention, products of the work).*

Source: *Statistique générale de la Tunisie*, chapter *Établissements pénitentiaires*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 75, f99; sgt1923 (`bpt6k9105649x`): p. 81, f583; sgt1924 (`bpt6k9105649x`): p. 83, f1073; sgt1925 (`bpt6k9105650k`): p. 85, f109; sgt1926 (`bpt6k9105650k`): p. 94, f658, p. 95, f659; sgt1927 (`bpt6k91056510`): p. 92, f120, p. 93, f121; sgt1928 (`bpt6k91056510`): p. 92, f644, p. 93, f645; sgt1929 (`bpt6k9105652d`): p. 94, f122, p. 95, f123; sgt1930 (`bpt6k9105652d`): p. 98, f656, p. 99, f657; sgt1935 (`bpt6k9105653t`): p. 64, f84, p. 65, f85.

Transcriptions: `../transcribed/prisons_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_prisons.py build`.

Rows: 1094. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935.

Units: days of detention; francs with centimes; francs per day.

Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, with `year`; no year is printed by two editions.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section (`expenditure` = the table, `expenditure_note` = its footnote (1), sgt1922-sgt1925)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (sgt1926-sgt1928: two-page spread; each cell has its own page)
- `gallica_view`: Gallica view of the page the cell is printed on
- `year`: year of the figures (the edition year: each edition prints the table for its own year)
- `establishment`: line label as printed (prisons, then lines such as Chantiers extérieurs, Geôles, En Algérie, Dans les Hôpitaux)
- `measure`: `days`, `personnel`, `upkeep` (*entretien et dépenses diverses* / *dépenses diverses*), `food` (*nourriture*), `total`, `price_per_day`, `products`; footnote: `price_personnel`, `price_upkeep`, `price_food`, `price_per_day`
- `measure_fr`: printed column heading
- `unit`: `days`, `francs` (to the centime) or `francs_per_day`
- `value`: number of days of detention, francs (centimes after the point) or francs per day (to the decimals printed: 4 up to sgt1925, 3 from sgt1926)
- `flag`: empty, `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable` (SPEC.md)

Table d) of the chapter, printed sgt1922-sgt1935 (sgt1936 and sgt1939 print no such table); every edition is transcribed. sgt1929-sgt1935 keep sgt1926's columns. sgt1930 prints prices to four decimals again and prices the lower lines and the Totaux généraux; sgt1935 has Djebel Djougar and "Détachements extérieurs" above the Totaux, a last line "Détachés dans les établissements pénitentiaires d'Algérie" (only days, total and price; the other money columns printed ») and no Totaux généraux line.

The printed `Total` column is stored, unlike other totals, because several lines print only a total (sgt1924 En traitement dans les hôpitaux, En détention hors de Tunisie). The "Totaux", "TOTAL des journées de détention" and "Totaux généraux (Dépenses et Recettes)" lines are not stored; they are the checks. A total line marked `*` in the transcription sums every line above it, the others the lines since the previous total line. Cells not printed (blank price column under the lower lines) are NA with flag `not_applicable`; » = 0.

Checks: every column against each total line; total = personnel + nourriture + dépenses diverses on every line that prints a component; price per day = total / days to the last printed decimal (lines and the Totaux line); footnote (1) (sgt1922-sgt1925): its three components sum to the price, and each equals the sum of its column over the lines above the first total line divided by their days (±0,0001).

Footnote (1) text (sgt1922-sgt1925): "Le prix de la journée de détention dans les prisons de la Régence est de … se décomposant ainsi : frais de personnel …, d'entretien …, de nourriture …" (the cost of a day of detention in the prisons of the Regency, split into staff, upkeep and food); stored as establishment "Prisons de la Régence (note 1)".

sgt1923: the price column prints "1 4012 (1)" on the TOTAL des journées line with "(1) Prix moyen" under it and 1 4012 again on the TOTAUX line; neither is stored (the footnote carries 1,4012). sgt1927 Bardo total: hundreds digit broken in the printing, read as 1 (158.109,75 = the sum of its components). sgt1928 Totaux line prints » under Personnel and Produits although the lines are not »; the Totaux total 2.987.183,76 does include the personnel of the lines.

Unlocated differences (failed checks without a flagged cell; printed values confirmed on crops): sgt1923 products column 0,90 short of the TOTAUX; sgt1924 days column 10 short of the Totaux; sgt1925 personnel column 0,06 over the Totaux and the Totaux line's components 0,06 under its total; price-per-day differences of 0,0002-0,0040 (sgt1924 Tunis, Gabès; sgt1925 Tunis; sgt1930 Kairouan, En Algérie; sgt1935 Kairouan, Djebel Djougar, Détachés … d'Algérie), which look like prices computed on slightly different figures. Larger price differences are flagged (below).

sgt1929-sgt1935: amounts printed without centimes ("201.520 »", "15 »", sgt1935 Béja products "9.225") are stored as whole francs; « (ditto) under a » is stored as 0. sgt1929 Bardo personnel 85.613,20: the 2 is broken ("?0") as elsewhere on the page; 20 is the reading that gives the line and column totals.

Every cell was read on the native-resolution page images; every failing check re-read on an enlarged crop (the printed values were confirmed).

Cells flagged `total_mismatch` (printed value kept, re-read on a native-resolution crop): sgt1923: Bardo / personnel (printed 33.532,38: the Bardo line sums to 86.421,59 for a printed total 86.421,99 and the column to 597.547,85 for 597.548,25, both 0,40 short); sgt1923: Béja / food (printed 11.249,14: the Béja line and the nourriture column are both 0,05 short of their printed totals); sgt1923: Kairouan / price_per_day (printed 1,2518; 66.170,63 / 53.715 days = 1,2319); sgt1924: Kairouan / personnel (printed 16.357,56: the Kairouan line and the personnel column are both 200 short of their printed totals); sgt1926: Le Kef / food (printed 49.693,34: the Le Kef line and the nourriture column are both 1,00 short of their printed totals); sgt1926: En Algérie / total (printed 212.043,07 for a nourriture of 212.043,75 and nothing else; the Totaux généraux (2.863.528,66) needs 212.043,75); sgt1927: Porto-Farina / upkeep (printed 50.685,73: the Porto-Farina line and the dépenses diverses column are both 0,20 short of their printed totals); sgt1928: Sfax / upkeep (printed 327.485,87; the Sfax total 159.829,79 needs 37.475,87, the figure printed on the Sousse line below); sgt1928: Sousse / upkeep (printed 37.475,87 (the Sfax figure); the Sousse total 186.151,84 needs 28.500,53); sgt1928: Gabès / total (printed 109.392,95 for components summing to 109.492,95; the column total agrees with the other cells only if Gabès or Sousse dépenses diverses differ by the same 100 (see the failed checks)); sgt1930: Béja / food (printed 34.555,77: the Béja line (129.900,88) and the nourriture column (878.763,98) are both 0,04 short of the cells, at this cell); sgt1935: Bizerte / price_per_day (printed 4,982; 58.761,13 / 11.640 days = 5,048 (days, total and components all check against the Totaux)); sgt1935: Sfax / price_per_day (printed 3,885; 158.747,36 / 35.901 days = 4,422 (days, total and components all check against the Totaux)); sgt1935: Tunis / price_per_day (printed 3,222; 1.450.653,04 / 448.918 days = 3,231 (days, total and components all check against the Totaux)).

## Validation

- Checks against printed totals and identities: 406; passed: 368; failed: 38.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1923 p.81 (f583) expenditure Bardo: total = personnel + food + upkeep: cells give 86421.59, printed 86421.99 (difference 0.40)
  - sgt1923 p.81 (f583) expenditure Béja: total = personnel + food + upkeep: cells give 29456.94, printed 29456.99 (difference 0.05)
  - sgt1923 p.81 (f583) expenditure Kairouan: price per day = total / days (to the last printed decimal): cells give 1.2319, printed 1.2518 (difference 0.0199)
  - sgt1923 p.81 (f583) expenditure personnel: lines vs TOTAUX*: cells give 597547.85, printed 597548.25 (difference 0.40)
  - sgt1923 p.81 (f583) expenditure food: lines vs TOTAUX*: cells give 1058943.96, printed 1058944.01 (difference 0.05)
  - sgt1923 p.81 (f583) expenditure products: lines vs TOTAUX*: cells give 73619.23, printed 73620.13 (difference 0.90)
  - sgt1924 p.83 (f1073) expenditure Tunis: price per day = total / days (to the last printed decimal): cells give 1.8354, printed 1.8351 (difference -0.0003)
  - sgt1924 p.83 (f1073) expenditure Kairouan: total = personnel + food + upkeep: cells give 85587.97, printed 85787.97 (difference 200.00)
  - sgt1924 p.83 (f1073) expenditure Gabès: price per day = total / days (to the last printed decimal): cells give 1.8786, printed 1.8746 (difference -0.0040)
  - sgt1924 p.83 (f1073) expenditure days: lines vs Totaux: cells give 1113155, printed 1113165 (difference 10)
  - sgt1924 p.83 (f1073) expenditure personnel: lines vs Totaux: cells give 637850.85, printed 638050.85 (difference 200.00)
  - sgt1925 p.85 (f109) expenditure Tunis: price per day = total / days (to the last printed decimal): cells give 2.2646, printed 2.2640 (difference -0.0006)
  - sgt1925 p.85 (f109) expenditure personnel: lines vs Totaux: cells give 955974.78, printed 955974.72 (difference -0.06)
  - sgt1925 p.85 (f109) expenditure Totaux: total = personnel + food + upkeep: cells give 2429107.52, printed 2429107.58 (difference 0.06)
  - sgt1926 p.94 (f658) expenditure Le Kef: total = personnel + food + upkeep: cells give 96179.46, printed 96180.46 (difference 1.00)
  - sgt1926 p.94 (f658) expenditure food: lines vs Totaux: cells give 1163118.55, printed 1163119.55 (difference 1.00)
  - sgt1926 p.94 (f658) expenditure En Algérie: total = personnel + food + upkeep: cells give 212043.75, printed 212043.07 (difference -0.68)
  - sgt1926 p.94 (f658) expenditure food: lines vs Totaux généraux (Dépenses et Recettes)*: cells give 1460639.95, printed 1460640.95 (difference 1.00)
  - sgt1926 p.94 (f658) expenditure total: lines vs Totaux généraux (Dépenses et Recettes)*: cells give 2863527.98, printed 2863528.66 (difference 0.68)
  - sgt1927 p.92 (f120) expenditure Porto-Farina: total = personnel + food + upkeep: cells give 311339.10, printed 311339.30 (difference 0.20)
  - sgt1927 p.92 (f120) expenditure upkeep: lines vs Totaux: cells give 484023.76, printed 484023.96 (difference 0.20)
  - sgt1927 p.92 (f120) expenditure upkeep: lines vs Totaux généraux (Dépenses et Recettes)*: cells give 509741.35, printed 509741.55 (difference 0.20)
  - sgt1928 p.92 (f644) expenditure Gabès: total = personnel + food + upkeep: cells give 109492.95, printed 109392.95 (difference -100.00)
  - sgt1928 p.92 (f644) expenditure Sfax: total = personnel + food + upkeep: cells give 449839.79, printed 159829.79 (difference -290010.00)
  - sgt1928 p.92 (f644) expenditure Sousse: total = personnel + food + upkeep: cells give 195127.18, printed 186151.84 (difference -8975.34)
  - sgt1928 p.92 (f644) expenditure upkeep: lines vs Totaux: cells give 831992.08, printed 532906.74 (difference -299085.34)
  - sgt1928 p.92 (f644) expenditure upkeep: lines vs Totaux généraux (Dépenses et Recettes)*: cells give 1160414.06, printed 861328.72 (difference -299085.34)
  - sgt1930 p.98 (f656) expenditure Béja: total = personnel + food + upkeep: cells give 129900.92, printed 129900.88 (difference -0.04)
  - sgt1930 p.98 (f656) expenditure Kairouan: price per day = total / days (to the last printed decimal): cells give 3.7781, printed 3.7783 (difference 0.0002)
  - sgt1930 p.98 (f656) expenditure food: lines vs Totaux: cells give 878764.02, printed 878763.98 (difference -0.04)
  - sgt1930 p.98 (f656) expenditure En Algérie: price per day = total / days (to the last printed decimal): cells give 6.9336, printed 6.9303 (difference -0.0033)
  - sgt1930 p.98 (f656) expenditure food: lines vs Totaux généraux (Dépenses et Recettes)*: cells give 901820.59, printed 901820.55 (difference -0.04)
  - sgt1935 p.64 (f84) expenditure Bizerte: price per day = total / days (to the last printed decimal): cells give 5.048, printed 4.982 (difference -0.066)
  - sgt1935 p.64 (f84) expenditure Kairouan: price per day = total / days (to the last printed decimal): cells give 3.970, printed 3.972 (difference 0.002)
  - sgt1935 p.64 (f84) expenditure Sfax: price per day = total / days (to the last printed decimal): cells give 4.422, printed 3.885 (difference -0.537)
  - sgt1935 p.64 (f84) expenditure Tunis: price per day = total / days (to the last printed decimal): cells give 3.231, printed 3.222 (difference -0.009)
  - sgt1935 p.64 (f84) expenditure Djebel Djougar: price per day = total / days (to the last printed decimal): cells give 2.233, printed 2.230 (difference -0.003)
  - sgt1935 p.64 (f84) expenditure Détachés dans les établissements pénitentiaires d'Algérie: price per day = total / days (to the last printed decimal): cells give 6.384, printed 6.387 (difference 0.003)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: not_applicable: 19, total_mismatch: 14.

  - sgt1923 p.81 1923 Bardo / personnel / francs = 33532.38 (total_mismatch)
  - sgt1923 p.81 1923 Béja / food / francs = 11249.14 (total_mismatch)
  - sgt1923 p.81 1923 Kairouan / price_per_day / francs_per_day = 1.2518 (total_mismatch)
  - sgt1924 p.83 1924 Kairouan / personnel / francs = 16357.56 (total_mismatch)
  - sgt1924 p.83 1924 Sur les chantiers extérieurs / price_per_day / francs_per_day = NA (not_applicable)
  - sgt1924 p.83 1924 En traitement dans les hôpitaux / price_per_day / francs_per_day = NA (not_applicable)
  - sgt1924 p.83 1924 En détention hors de Tunisie / price_per_day / francs_per_day = NA (not_applicable)
  - sgt1926 p.95 1926 Le Kef / food / francs = 49693.34 (total_mismatch)
  - sgt1926 p.95 1926 Géôles / price_per_day / francs_per_day = NA (not_applicable)
  - sgt1926 p.95 1926 En Algérie / total / francs = 212043.07 (total_mismatch)
  - sgt1926 p.95 1926 En Algérie / price_per_day / francs_per_day = NA (not_applicable)
  - sgt1926 p.95 1926 Dans les Hôpitaux / price_per_day / francs_per_day = NA (not_applicable)
  - sgt1926 p.95 1926 Chantiers extérieurs / price_per_day / francs_per_day = NA (not_applicable)
  - sgt1927 p.93 1927 Porto-Farina / upkeep / francs = 50685.73 (total_mismatch)
  - sgt1927 p.93 1927 Pénitencier agricole du Djebel Djougar / price_per_day / francs_per_day = NA (not_applicable)
  - sgt1927 p.93 1927 Chantiers extérieurs / price_per_day / francs_per_day = NA (not_applicable)
  - sgt1927 p.93 1927 Dans les Hôpitaux / price_per_day / francs_per_day = NA (not_applicable)
  - sgt1927 p.93 1927 En Algérie / price_per_day / francs_per_day = NA (not_applicable)
  - sgt1928 p.93 1928 Gabès / total / francs = 109392.95 (total_mismatch)
  - sgt1928 p.93 1928 Sfax / upkeep / francs = 327485.87 (total_mismatch)
  - sgt1928 p.93 1928 Sousse / upkeep / francs = 37475.87 (total_mismatch)
  - sgt1928 p.93 1928 Pénitencier agricole du Djebel Djougar / price_per_day / francs_per_day = NA (not_applicable)
  - sgt1928 p.93 1928 Chantiers extérieurs / price_per_day / francs_per_day = NA (not_applicable)
  - sgt1928 p.93 1928 Dans les Hôpitaux / price_per_day / francs_per_day = NA (not_applicable)
  - sgt1928 p.93 1928 En Algérie / price_per_day / francs_per_day = NA (not_applicable)
  - sgt1929 p.95 1929 Pénitencier agricole du Djebel Djougar / price_per_day / francs_per_day = NA (not_applicable)
  - sgt1929 p.95 1929 Chantiers extérieurs / price_per_day / francs_per_day = NA (not_applicable)
  - sgt1929 p.95 1929 Dans les Hôpitaux / price_per_day / francs_per_day = NA (not_applicable)
  - sgt1929 p.95 1929 En Algérie / price_per_day / francs_per_day = NA (not_applicable)
  - sgt1930 p.99 1930 Béja / food / francs = 34555.77 (total_mismatch)
  - sgt1935 p.65 1935 Bizerte / price_per_day / francs_per_day = 4.982 (total_mismatch)
  - sgt1935 p.65 1935 Sfax / price_per_day / francs_per_day = 3.885 (total_mismatch)
  - sgt1935 p.65 1935 Tunis / price_per_day / francs_per_day = 3.222 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (14 printings): sgt1922 f99, sgt1923 f583, sgt1924 f1073, sgt1925 f109, sgt1926 f658, sgt1927 f120, sgt1928 f644, sgt1929 f122, sgt1930 f656, sgt1935 f84, sgt1922 f99, sgt1923 f583, sgt1924 f1073, sgt1925 f109.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
