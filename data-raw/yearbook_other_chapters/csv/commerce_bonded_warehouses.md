# Magasins généraux : mouvement des marchandises

*General (bonded) warehouses: movement of goods at Tunis, Sousse and Sfax.*

Source: *Statistique générale de la Tunisie*, chapter *Commerce et navigation*, editions sgt1922, sgt1923, sgt1924. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 398, f422, p. 399, f423, p. 400, f424; sgt1923 (`bpt6k9105649x`): p. 410, f912, p. 411, f913, p. 412, f914; sgt1924 (`bpt6k9105649x`): p. 426, f1416, p. 427, f1417, p. 428, f1418.

Transcriptions: `../transcribed/commerce_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_commerce.py build`.

Rows: 1040. Years: 1922, 1923, 1924.

Units: quantities as printed (quintaux at Tunis and Sfax; the unit column at Sousse), values in francs; never converted. The TOTAL column (existing + entries) and the Tunis TOTAUX line are checks only, not stored. value_type: mixed.

Selection: each edition prints a single year (its reference year); no overlap, all stored. The opening stock of each year is compared with the closing stock printed the year before (check only).

## Columns

- `census`: edition (each edition prints one year, its reference year)
- `table_id`: `warehouses_a` (Tunis), `warehouses_b` (Sousse), `warehouses_c` (Sfax)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the movement (entries and exits during that year)
- `port`: `tunis`, `sousse`, `sfax`
- `port_fr`: sub-table heading as printed
- `warehouse`: `general` (Magasins généraux) or `bonded` (Entrepôt réel, Sousse only)
- `warehouse_fr`: as printed
- `product`: row code (see product_fr)
- `product_fr`: désignation as printed
- `measure`: `existing_quantity`, `existing_value` (stock on 1 January), `entries_*`, `exits_*` (during the year), `remaining_*` (stock on 1 January of the next year)
- `measure_fr`: column heading as printed
- `unit`: quantity: `quintaux` (Tunis, Sfax) or the Sousse unit column as printed (`kilo`, `pièces`, `douzaines`, `caisses`, `hectolitres`, `balles`; empty for Articles divers, printed without quantity); value: `francs`
- `value`: as printed (» stored as 0; Sfax quantities with centièmes)
- `flag`: empty or `total_mismatch` (misprinted cell, see notes)

Three sub-tables per edition: a) Magasins de Tunis, b) Magasins de Sousse (Magasins généraux and Entrepôt réel), c) Magasins de Sfax. For each line the printed columns are the stock on 1 January, entries and exits during the year, the TOTAL (stock + entries) and the stock remaining on 1 January of the next year, each as quantity and value. Product lists differ between editions (Sousse adds Entrepôt réel scourtins, huile minérale and thé in 1923; prints no Articles divers in 1924); every line printed is stored. At Sfax several lines print » for the quantity but a value (goods counted only in francs); » is stored as 0 as printed.

Explanation of the failed checks (every cell involved re-read on a native-resolution crop; printed values kept). The TOTAL column is not stored, so a misprint located there needs no flag. sgt1922 Tunis: céréales TOTAL value 11.573.105 (stock + entries and the TOTAUX line give 11.573.015). sgt1922 Sousse: céréales quantities (TOTAL 3.706.640 for 3.706.040; remaining 189.000) cannot be reconciled to one cell, not flagged; laines and savons remaining values 22.202 and 57.285 (32.199 and 58.275 by difference) are reprinted unchanged as the 1923 opening stock, not flagged; café et thé entries value 532.048 (88.557 - 35.353 = 53.204, an extra digit; flagged) and TOTAL quantity 17.738 for 17.733; métaux TOTAL value 11.640 for 41.640, and the remaining value 31.790 agrees with neither; futailles remaining 84 / 13.689 for 74 / 24.688 (reprinted in 1923); vins remaining 16 hl for 558 - 442 = 116 (flagged); Articles divers TOTAL value 120.937 for 123.937; Entrepôt réel céréales remaining 6.277 for 3.710.100 - 3.082.400 = 627.700 kg (flagged; apparently quintaux, reprinted as the 1923 opening stock). sgt1922 Sfax: café et thé TOTAL 368.40 q for 300 + 88.40 = 388.40 (exits + remaining = 388.40). sgt1923 Sousse: the TOTAL column omits the opening stock on every line without entries (café et thé, métaux, futailles, vins, Articles divers, Entrepôt réel céréales: TOTAL printed », exits equal to the stock), and the Entrepôt réel céréales stock 6.277 / 961.222 francs is neither taken out nor carried over; céréales, huiles, laines and savons TOTAL values do not equal stock + entries (céréales entries value 2.183.160 against TOTAL 229.656 and exits 128.380; the value columns of that line are mutually inconsistent and no cell can be located); céréales remaining quantity 260.020 for 280.020. Not flagged. sgt1923 Sfax: sucre 3.92 + 10209 = 10212.92, printed 10.213 (rounded); sucre remaining value 102.000 for 2.655.320 - 2.653.320 = 2.000 (102.000 reprinted as the 1924 opening stock; the exits value is probably misprinted), not flagged. sgt1924 Tunis: céréales opening-stock value 341.723 (sgt1923 closing 3.111.723; the TOTAL 6.080.643 and the TOTAUX line need 3.111.723; leading digits dropped; flagged); produits chimiques TOTAL value 126.696 for 162.696 (transposed digits; the remaining 116.926 agrees with 162.696 - 45.770); produits alimentaires exits 5.079 q (the exits TOTAUX and the remaining 820 need 5.075; flagged). sgt1924 Sousse: tissus TOTAL value 70.000 for 7.000, and the remaining 2.250 does not equal 7.000 - 3.750. sgt1924 Sfax: céréales remaining value 292.040 for 297.040; amandes entries value printed 440.50 (thousands point misplaced; 298.883 - 254.833 = 44.050; flagged); sparteries TOTAL and exits printed » although the stock 72.630 francs is carried to the remaining. Opening-stock continuity: Sfax huiles d'olive 1924 opening 2.133 q against 8.133 closing in sgt1923 (each printing internally consistent); Sfax tissus 56.186 against 56.181 francs; Tunis céréales (misprint above).

Survey of the whole chapter: `commerce_survey.md`.

## Validation

- Checks against printed totals and identities: 732; passed: 670; failed: 62.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.398 (f422) warehouses total.v: lines vs Totaux: cells give 25457568, printed 25457478 (difference -90)
  - sgt1922 p.398 (f422) warehouses cereals: total.v = existing + entries: cells give 11573015, printed 11573105 (difference 90)
  - sgt1922 p.398 (f422) warehouses cereals: remaining.v = total - exits: cells give 1817913, printed 1817823 (difference -90)
  - sgt1922 p.399 (f423) warehouses cereals: total.q = existing + entries: cells give 3706040, printed 3706640 (difference 600)
  - sgt1922 p.399 (f423) warehouses cereals: remaining.q = total - exits: cells give 189640, printed 189000 (difference -640)
  - sgt1922 p.399 (f423) warehouses wool: remaining.v = total - exits: cells give 32199, printed 22202 (difference -9997)
  - sgt1922 p.399 (f423) warehouses soap: remaining.v = total - exits: cells give 58275, printed 57285 (difference -990)
  - sgt1922 p.399 (f423) warehouses coffee_tea: total.q = existing + entries: cells give 17733, printed 17738 (difference 5)
  - sgt1922 p.399 (f423) warehouses coffee_tea: total.v = existing + entries: cells give 567401, printed 88557 (difference -478844)
  - sgt1922 p.399 (f423) warehouses metals: total.v = existing + entries: cells give 41640, printed 11640 (difference -30000)
  - sgt1922 p.399 (f423) warehouses metals: remaining.v = total - exits: cells give -19190, printed 31790 (difference 50980)
  - sgt1922 p.399 (f423) warehouses casks: remaining.q = total - exits: cells give 74, printed 84 (difference 10)
  - sgt1922 p.399 (f423) warehouses casks: remaining.v = total - exits: cells give 24688, printed 13689 (difference -10999)
  - sgt1922 p.399 (f423) warehouses wine: remaining.q = total - exits: cells give 116, printed 16 (difference -100)
  - sgt1922 p.399 (f423) warehouses misc: total.v = existing + entries: cells give 123937, printed 120937 (difference -3000)
  - sgt1922 p.399 (f423) warehouses cereals: remaining.q = total - exits: cells give 627700, printed 6277 (difference -621423)
  - sgt1922 p.400 (f424) warehouses coffee_tea: total.q = existing + entries: cells give 388.40, printed 368.40 (difference -20.00)
  - sgt1922 p.400 (f424) warehouses coffee_tea: remaining.q = total - exits: cells give -3.15, printed 16.85 (difference 20.00)
  - sgt1923 p.411 (f913) warehouses cereals: remaining.q = total - exits: cells give 280020, printed 260020 (difference -20000)
  - sgt1923 p.411 (f913) warehouses cereals: total.v = existing + entries: cells give 2296560, printed 229656 (difference -2066904)
  - sgt1923 p.411 (f913) warehouses cereals: remaining.v = total - exits: cells give 101276, printed 171276 (difference 70000)
  - sgt1923 p.411 (f913) warehouses oils: total.v = existing + entries: cells give 5379434, printed 5460350 (difference 80916)
  - sgt1923 p.411 (f913) warehouses wool: total.v = existing + entries: cells give 70702, printed 105000 (difference 34298)
  - sgt1923 p.411 (f913) warehouses soap: total.v = existing + entries: cells give 183285, printed 202500 (difference 19215)
  - sgt1923 p.411 (f913) warehouses coffee_tea: total.q = existing + entries: cells give 9063, printed 0 (difference -9063)
  - sgt1923 p.411 (f913) warehouses coffee_tea: remaining.q = total - exits: cells give -9063, printed 0 (difference 9063)
  - sgt1923 p.411 (f913) warehouses coffee_tea: total.v = existing + entries: cells give 36507, printed 0 (difference -36507)
  - sgt1923 p.411 (f913) warehouses coffee_tea: remaining.v = total - exits: cells give -36507, printed 0 (difference 36507)
  - sgt1923 p.411 (f913) warehouses metals: total.q = existing + entries: cells give 10050, printed 0 (difference -10050)
  - sgt1923 p.411 (f913) warehouses metals: remaining.q = total - exits: cells give -10050, printed 0 (difference 10050)
  - sgt1923 p.411 (f913) warehouses metals: total.v = existing + entries: cells give 31790, printed 0 (difference -31790)
  - sgt1923 p.411 (f913) warehouses metals: remaining.v = total - exits: cells give -31790, printed 0 (difference 31790)
  - sgt1923 p.411 (f913) warehouses casks: total.q = existing + entries: cells give 84, printed 0 (difference -84)
  - sgt1923 p.411 (f913) warehouses casks: remaining.q = total - exits: cells give -84, printed 0 (difference 84)
  - sgt1923 p.411 (f913) warehouses casks: total.v = existing + entries: cells give 13689, printed 0 (difference -13689)
  - sgt1923 p.411 (f913) warehouses casks: remaining.v = total - exits: cells give -13689, printed 0 (difference 13689)
  - sgt1923 p.411 (f913) warehouses wine: total.q = existing + entries: cells give 16, printed 0 (difference -16)
  - sgt1923 p.411 (f913) warehouses wine: remaining.q = total - exits: cells give -16, printed 0 (difference 16)
  - sgt1923 p.411 (f913) warehouses wine: total.v = existing + entries: cells give 8700, printed 0 (difference -8700)
  - sgt1923 p.411 (f913) warehouses wine: remaining.v = total - exits: cells give -8700, printed 0 (difference 8700)
  - sgt1923 p.411 (f913) warehouses misc: total.v = existing + entries: cells give 59195, printed 0 (difference -59195)
  - sgt1923 p.411 (f913) warehouses misc: remaining.v = total - exits: cells give -59195, printed 0 (difference 59195)
  - sgt1923 p.411 (f913) warehouses cereals: total.q = existing + entries: cells give 6277, printed 0 (difference -6277)
  - sgt1923 p.411 (f913) warehouses cereals: total.v = existing + entries: cells give 961222, printed 0 (difference -961222)
  - sgt1923 p.412 (f914) warehouses sugar: total.q = existing + entries: cells give 10212.92, printed 10213 (difference 0.08)
  - sgt1923 p.412 (f914) warehouses sugar: remaining.v = total - exits: cells give 2000, printed 102000 (difference 100000)
  - sgt1924 p.426 (f1416) warehouses existing.v: lines vs Totaux: cells give 3209677, printed 5979677 (difference 2770000)
  - sgt1924 p.426 (f1416) warehouses total.v: lines vs Totaux: cells give 15694449, printed 15730449 (difference 36000)
  - sgt1924 p.426 (f1416) warehouses exits.q: lines vs Totaux: cells give 245060, printed 245056 (difference -4)
  - sgt1924 p.426 (f1416) warehouses food: remaining.q = total - exits: cells give 816, printed 820 (difference 4)
  - sgt1924 p.426 (f1416) warehouses chemicals: total.v = existing + entries: cells give 162696, printed 126696 (difference -36000)
  - sgt1924 p.426 (f1416) warehouses chemicals: remaining.v = total - exits: cells give 80926, printed 116926 (difference 36000)
  - sgt1924 p.426 (f1416) warehouses cereals: total.v = existing + entries: cells give 3310643, printed 6080643 (difference 2770000)
  - sgt1924 p.427 (f1417) warehouses textiles: total.v = existing + entries: cells give 7000, printed 70000 (difference 63000)
  - sgt1924 p.427 (f1417) warehouses textiles: remaining.v = total - exits: cells give 66250, printed 2250 (difference -64000)
  - sgt1924 p.428 (f1418) warehouses cereals: remaining.v = total - exits: cells give 297040, printed 292040 (difference -5000)
  - sgt1924 p.428 (f1418) warehouses esparto_goods: total.v = existing + entries: cells give 72630, printed 0 (difference -72630)
  - sgt1924 p.428 (f1418) warehouses esparto_goods: remaining.v = total - exits: cells give 0, printed 72630 (difference 72630)
  - sgt1924 p.428 (f1418) warehouses almonds: total.v = existing + entries: cells give 255273.50, printed 298883 (difference 43609.50)
  - sfax general olive_oil q: existing 1 Jan 1924 (sgt1924 f1418) = remaining (sgt1923 f914): cells give 8133, printed 2133 (difference -6000)
  - sfax general textiles v: existing 1 Jan 1924 (sgt1924 f1418) = remaining (sgt1923 f914): cells give 56181, printed 56186 (difference 5)
  - tunis general cereals v: existing 1 Jan 1924 (sgt1924 f1416) = remaining (sgt1923 f912): cells give 3111723, printed 341723 (difference -2770000)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: total_mismatch: 6.

  - sgt1922 p.399 1922 sousse / general / coffee_tea / entries_value / francs = 532048 (total_mismatch)
  - sgt1922 p.399 1922 sousse / general / wine / remaining_quantity / hectolitres = 16 (total_mismatch)
  - sgt1922 p.399 1922 sousse / bonded / cereals / remaining_quantity / kilo = 6277 (total_mismatch)
  - sgt1924 p.426 1924 tunis / general / food / exits_quantity / quintaux = 5079 (total_mismatch)
  - sgt1924 p.426 1924 tunis / general / cereals / existing_value / francs = 341723 (total_mismatch)
  - sgt1924 p.428 1924 sfax / general / almonds / entries_value / francs = 440.50 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (12 printings): sgt1922 f422, sgt1922 f423, sgt1922 f423, sgt1922 f424, sgt1923 f912, sgt1923 f913, sgt1923 f913, sgt1923 f914, sgt1924 f1416, sgt1924 f1417, sgt1924 f1417, sgt1924 f1418.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
