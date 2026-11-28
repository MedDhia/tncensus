# Principales cultures ; rendement et répartition (surfaces ensemencées, imposées et non imposées ; nombre d'hectares ayant produit 1 à 6 hectolitres et au-dessus ; cultures européennes ou indigènes)

*Main crops: sown, taxed and untaxed areas, and taxed area by yield class (hectolitres per hectare), European and indigenous farmers.*

Source: *Statistique générale de la Tunisie*, chapter *Agriculture*, editions sgt1922, sgt1923, sgt1924, sgt1925. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 216, f240, p. 217, f241, p. 218, f242, p. 219, f243, p. 220, f244, p. 221, f245, p. 222, f246, p. 223, f247, p. 224, f248, p. 225, f249; sgt1923 (`bpt6k9105649x`): p. 228, f730, p. 229, f731, p. 230, f732, p. 231, f733, p. 235, f737, p. 236, f738; sgt1924 (`bpt6k9105649x`): p. 236, f1226, p. 237, f1227, p. 238, f1228, p. 239, f1229, p. 240, f1230, p. 241, f1231, p. 242, f1232, p. 243, f1233, p. 244, f1234, p. 245, f1235, p. 246, f1236, p. 247, f1237, p. 248, f1238, p. 249, f1239, p. 250, f1240, p. 251, f1241; sgt1925 (`bpt6k9105650k`): p. 274, f298, p. 275, f299, p. 276, f300, p. 277, f301, p. 278, f302, p. 279, f303.

Transcriptions: `../transcribed/agriculture_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_agriculture.py build`.

Rows: 1904. Years: 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925.

Units: hectares (printed h. a., hectares and ares; sgt1925 whole hectares), ratios and percent (`unit`); value_type: mixed.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (rule 4 series: the latest edition printing that year; rule 5 tables: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: harvest year (the upper box is printed by harvest year; the lower table by agricultural year, e.g. 1914-1915 = harvest 1915, `crop_year_fr`)
- `crop_year_fr`: agricultural year as printed in the lower table (empty for the upper box)
- `zone`: `tunisia` (whole country), or the zone of sgt1925 (`north`: Tunisie septentrionale et Hauts plateaux; `centre_south`: Tunisie centrale et méridionale)
- `zone_fr`: zone heading as printed ("Tunisie (ensemble)" when the table has no zones)
- `crop`: crop code (English)
- `crop_fr`: crop as printed in the sub-table title
- `subtable`: `surfaces` (upper box: surfaces ensemencées, imposées, non imposées) or `yield_classes` (lower table: number of hectares that produced 1, 2, ... 6 hectolitres and more per hectare)
- `farmers`: `all` (upper box), `european` or `indigenous` (CULTURES EUROPÉENNES OU INDIGÈNES)
- `farmers_fr`: printed line heading (empty for the upper box)
- `area_class`: surface category (upper box) or yield class in hectolitres per hectare (lower table)
- `area_class_fr`: printed heading
- `measure`: `area`; `ratio_to_line_total` (RAPPORT avec les surfaces imposées or ensemencées, as headed: the class area over the TOTAUX of the same line); sgt1925 `percent_of_sown_area` (RAPPORT avec les surfaces ensemencées, printed in %)
- `measure_fr`: printed heading of the measure
- `unit`: `hectares` (printed h. a.: hectares and ares, stored as hectares with two decimals; sgt1925 whole hectares), `ratio`, or `percent`
- `value`: printed value (» = 0)
- `flag`: empty, or `ocr_corrected` (image reading differs from the Gallica OCR), `total_mismatch` (cell identified as the faulty one of a failed check, printed value kept), `reprint_corrected` (the latest printing is misprinted: value from the earlier edition named in `census`)

sgt1922-sgt1924: one spread per crop (blé, orge, avoine, maïs, sorgho, fèves, pois chiches, lin; sgt1922 a)-h), the lettering of the survey's "d)-f)" and "g) (h)" is a) blé ... h) lin). Upper box (`subtable` = `surfaces`, by harvest year): surfaces ensemencées, imposées (yield over 1 hl), non imposées (yield under 1 hl), non imposées sown on newly cleared land. Lower table (`yield_classes`, by agricultural year 1914-1915 ... = harvest `year`; `crop_year_fr`): hectares that produced 1, 2, 3, 4, 5, 6 hl and more per hectare, for European and indigenous farmers, each with its RAPPORT (ratio to the line's TOTAUX; headed "avec les surfaces imposées" for blé, orge, avoine, maïs, pois chiches and "avec les surfaces ensemencées" for sorgho, fèves, lin, but computed on the TOTAUX in both cases). The TOTAUX lines (Européens + Indigènes) and the TOTAUX column are checks only. The RAPPORT of the TOTAUX lines is not printed for the last two years of sgt1923-sgt1924.

sgt1925: new layout, three spreads (blé, orge, avoine), left page Tunisie septentrionale et Hauts Plateaux (1re-3e Régions, `zone` = `north`), right page Tunisie centrale et méridionale (4e-5e Régions et Territoires militaires, `centre_south`), years 1921-1925: surfaces ensemencées, hectares that produced 0 à 5 hectol. and 6 hl et au-dessus, each with its percentage of the sown area (`percent`). Not comparable cell by cell with sgt1922-sgt1924 (different classes and zones): not compared.

Overlapping years (sgt1922-sgt1924 reprint 1915/1916-1923) follow rule 4: each cell from the latest edition printing it, every other printing (read independently on its own page) compared. Cells of the TOTAUX lines are not stored, so their differences are given here: sgt1924 prints the 1919-1920 TOTAUX 5 hl of pois chiches (184 97) and of lin (256 02) interchanged with respect to sgt1922-sgt1923, the 1919-1920 TOTAUX 6 hl of fèves 6.131 36 (6.431 36) and 1 hl of pois chiches 514 11 (514 »), the 1921-1922 Indigènes TOTAUX of fèves 651 88 (9.651 88); sgt1923-sgt1924 print in the TOTAUX column of sorgho, lines 1919-1920 to 1921-1922, the totals of the year before. Stored cells that differ: see the table below (sgt1923-sgt1924 print the 1916 blé ensemencées and imposées interchanged, the TOTAUX of 1916 = 553.112 51 confirms sgt1922; sgt1924 prints fèves 1919-1920 Européens 5 hl 663 23 and lin Européens 2 hl 24 11, the line sums confirm 662 23 and 24 »: the earlier printing is kept, flag `reprint_corrected`). sgt1923 prints the avoine surfaces of 1922 and 1923 under interchanged year headings; they are compared under the year they belong to (flag `row_realigned` on that printing).

Every failed check below was re-read on a zoomed native-resolution crop: they are printed inconsistencies (printed values kept). Line sums (classes vs TOTAUX), Européens + Indigènes vs TOTAUX, TOTAUX vs surfaces imposées, imposées + non imposées vs ensemencées (the sown area includes the newly cleared land in some years only: both readings accepted), each RAPPORT vs class / TOTAUX (to 0.0005 or 1 %, also accepted against the sum of the classes when the TOTAUX is the faulty cell), and in sgt1925 the two classes vs the sown area and the percentages. Most failures recur unchanged in every printing of the same cell (sgt1922, sgt1923, sgt1924 were set from the same type). Flagged `total_mismatch` where one stored cell explains every failing check: blé 1914-1915 Indigènes 3 hl 55.309 86 (TOTAUX and RAPPORT need 55.509 86); orge 1917-1918 Indigènes 4 hl 60.181 79 (69.181 79); avoine 1918-1919 Indigènes 3 hl 144 57 (1.714 57); fèves 1918-1919 Indigènes 6 hl 1.105 13 (the line needs 11.015 13); pois chiches 1919-1920 Européens 1 hl 470 82 (70 82); RAPPORT cells with a dropped or added digit (blé 1918-1919 Indigènes 4 hl 0,1211, 1922-1923 Européens 1 hl 0,2015; orge 1915-1916 Européens 6 hl 0,0945, 1920-1921 Indigènes 6 hl 0,0762; avoine 1918-1919 Européens 3 hl 0,213; maïs 1918-1919 Européens 1 hl 0,0016, 1921-1922 Indigènes 2 hl 0,0136, 1922-1923 Européens 6 hl 0,9929; sorgho 1918-1919 Européens 4 hl 0, Indigènes 2 hl 0,1666; fèves 1919-1920 Européens 1 hl 0,5335; pois chiches 1920-1921 Européens 3 hl 0,0171, Indigènes 6 hl 0,0798; lin 1920-1921 Indigènes 1 hl 0,0960, 1922-1923 Européens and Indigènes 1 hl 0,0083 and 0,0236); sgt1925 blé Nord 1925 Indigènes 6 hl 175.582 (sown - 0-5 hl = 175.852, its percentage 60,46 fits), avoine Nord 1925 Indigènes 6 hl 14.603 (14.403), blé Centre-Sud 1922 Indigènes 13,14 % (3,13), avoine Nord 1922 Indigènes 22,33 % (12,33). The other failures are misprinted TOTAUX cells (not stored: e.g. blé 1921-1922 TOTAUX 316.818 70 for 346.818 70, orge 1916-1917 Indigènes TOTAUX 455.708 79 for 445.708 79, lin 1921-1922 TOTAUX 1.594 31 for 1.494 31), RAPPORT cells off in the last digits, differences of a few ares, or lines where no single cell can be identified (pois chiches 1923-1924 Indigènes in sgt1924: the six classes, each fitting its printed RAPPORT, sum to 3.983 45 against a printed TOTAUX of 3.542 90; sorgho 1923-1924 Européens 682 » against 678 »).

Survey of the whole chapter in every edition: `agriculture_survey.md`.

## Validation

- Checks against printed totals and identities: 3986; passed: 3677; failed: 309.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1925 p.274 (f298) zclasses wheat [north] 1922_ind: 0-5 hl + 6 hl et au-dessus vs surfaces ensemencées: cells give 255161, printed 255017 (difference -144)
  - sgt1925 p.274 (f298) zclasses wheat [north] 1922_ind: p05 = h05 / surfaces ensemencées: cells give 83.92, printed 83.96 (difference 0.04)
  - sgt1925 p.274 (f298) zclasses wheat [north] 1922_ind: p6 = h6 / surfaces ensemencées: cells give 16.13, printed 16.04 (difference -0.09)
  - sgt1925 p.274 (f298) zclasses wheat [north] 1925_ind: 0-5 hl + 6 hl et au-dessus vs surfaces ensemencées: cells give 290588, printed 290858 (difference 270)
  - sgt1925 p.274 (f298) zclasses wheat [north] 1925_ind: p6 = h6 / surfaces ensemencées: cells give 60.37, printed 60.46 (difference 0.09)
  - sgt1925 p.275 (f299) zclasses wheat [centre_south] 1922_ind: the two percentages vs 100: cells give 110.00, printed 100 (difference -10.00)
  - sgt1925 p.275 (f299) zclasses wheat [centre_south] 1922_ind: p6 = h6 / surfaces ensemencées: cells give 3.13, printed 13.14 (difference 10.01)
  - sgt1925 p.275 (f299) zclasses wheat [centre_south] 1924_eur: p05 = h05 / surfaces ensemencées: cells give 62.50, printed 62.47 (difference -0.03)
  - sgt1925 p.275 (f299) zclasses wheat [centre_south] 1924_eur: p6 = h6 / surfaces ensemencées: cells give 37.50, printed 37.53 (difference 0.03)
  - sgt1925 p.276 (f300) zclasses barley [north] 1921_ind: p05 = h05 / surfaces ensemencées: cells give 5.87, printed 6.25 (difference 0.38)
  - sgt1925 p.276 (f300) zclasses barley [north] 1921_ind: p6 = h6 / surfaces ensemencées: cells give 94.13, printed 93.75 (difference -0.38)
  - sgt1925 p.276 (f300) zclasses barley [north] 1924_ind: 0-5 hl + 6 hl et au-dessus vs surfaces ensemencées: cells give 148283, printed 148293 (difference 10)
  - sgt1925 p.277 (f301) zclasses barley [centre_south] 1921_eur: 0-5 hl + 6 hl et au-dessus vs surfaces ensemencées: cells give 5850, printed 6210 (difference 360)
  - sgt1925 p.277 (f301) zclasses barley [centre_south] 1921_eur: p6 = h6 / surfaces ensemencées: cells give 84.61, printed 90.41 (difference 5.80)
  - sgt1925 p.277 (f301) zclasses barley [centre_south] 1924_ind: p05 = h05 / surfaces ensemencées: cells give 94.48, printed 95.22 (difference 0.74)
  - sgt1925 p.277 (f301) zclasses barley [centre_south] 1924_ind: p6 = h6 / surfaces ensemencées: cells give 5.52, printed 4.78 (difference -0.74)
  - sgt1925 p.278 (f302) zclasses oats [north] 1922_ind: the two percentages vs 100: cells give 110.00, printed 100 (difference -10.00)
  - sgt1925 p.278 (f302) zclasses oats [north] 1922_ind: p6 = h6 / surfaces ensemencées: cells give 12.33, printed 22.33 (difference 10.00)
  - sgt1925 p.278 (f302) zclasses oats [north] 1924_eur: p05 = h05 / surfaces ensemencées: cells give 15.71, printed 15.75 (difference 0.04)
  - sgt1925 p.278 (f302) zclasses oats [north] 1924_eur: p6 = h6 / surfaces ensemencées: cells give 84.29, printed 84.25 (difference -0.04)
  - sgt1925 p.278 (f302) zclasses oats [north] 1925_eur: p05 = h05 / surfaces ensemencées: cells give 7.16, printed 7.11 (difference -0.05)
  - sgt1925 p.278 (f302) zclasses oats [north] 1925_eur: p6 = h6 / surfaces ensemencées: cells give 92.84, printed 92.89 (difference 0.05)
  - sgt1925 p.278 (f302) zclasses oats [north] 1925_ind: 0-5 hl + 6 hl et au-dessus vs surfaces ensemencées: cells give 17267, printed 17067 (difference -200)
  - sgt1925 p.278 (f302) zclasses oats [north] 1925_ind: p6 = h6 / surfaces ensemencées: cells give 85.56, printed 84.40 (difference -1.16)
  - sgt1925 p.279 (f303) zclasses oats [centre_south] 1924_eur: p05 = h05 / surfaces ensemencées: cells give 68.05, printed 68.01 (difference -0.04)
  - sgt1925 p.279 (f303) zclasses oats [centre_south] 1924_eur: p6 = h6 / surfaces ensemencées: cells give 31.95, printed 31.99 (difference 0.04)
  - sgt1922 p.217 (f241) classes wheat 1915_ind: classes vs TOTAUX: cells give 448180.91, printed 448380.91 (difference 200.00)
  - sgt1922 p.216 (f240) classes wheat 1915 c3: Européens + Indigènes vs TOTAUX: cells give 56218.98, printed 56418.98 (difference 200.00)
  - sgt1922 p.217 (f241) classes wheat 1916_eur: classes vs TOTAUX: cells give 63551.92, printed 63511.92 (difference -40.00)
  - sgt1922 p.217 (f241) classes wheat 1916_tot r5: c5 / TOTAUX = 0.08444, printed 0.0958
  - sgt1922 p.217 (f241) classes wheat 1916 tot: Européens + Indigènes vs TOTAUX: cells give 553072.51, printed 553112.51 (difference 40.00)
  - sgt1922 p.217 (f241) classes wheat 1918_eur: classes vs TOTAUX: cells give 81872.97, printed 81866.97 (difference -6.00)
  - sgt1922 p.217 (f241) classes wheat 1918_tot: classes vs TOTAUX: cells give 638276.59, printed 638270.59 (difference -6.00)
  - sgt1922 p.217 (f241) classes wheat 1919_ind r4: c4 / TOTAUX = 0.12618, printed 0.1211
  - sgt1922 p.217 (f241) classes wheat 1921_tot r5: c5 / TOTAUX = 0.05493, printed 0.0565
  - sgt1922 p.217 (f241) classes wheat 1922_ind: classes vs TOTAUX: cells give 271553.62, printed 271513.62 (difference -40.00)
  - sgt1922 p.217 (f241) classes wheat 1922_ind r4: c4 / TOTAUX = 0.13507, printed 0.1316
  - sgt1922 p.217 (f241) classes wheat 1922_tot: classes vs TOTAUX: cells give 346857.70, printed 316818.70 (difference -30039.00)
  - sgt1922 p.216 (f240) classes wheat 1922 c1: Européens + Indigènes vs TOTAUX: cells give 51914.27, printed 51913.27 (difference -1.00)
  - sgt1922 p.217 (f241) classes wheat 1922 tot: Européens + Indigènes vs TOTAUX: cells give 346818.70, printed 316818.70 (difference -30000.00)
  - sgt1922 p.217 (f241) classes wheat 1922: TOTAUX vs surfaces imposées: cells give 316818.70, printed 346818.70 (difference 30000.00)
  - sgt1922 p.219 (f243) classes barley 1916_eur r6: c6 / TOTAUX = 0.69648, printed 0.0945
  - sgt1922 p.219 (f243) classes barley 1917_eur: classes vs TOTAUX: cells give 20223.77, printed 20233.77 (difference 10.00)
  - sgt1922 p.219 (f243) classes barley 1917_ind: classes vs TOTAUX: cells give 445708.79, printed 455708.79 (difference 10000.00)
  - sgt1922 p.218 (f242) classes barley 1917_tot r1: c1 / TOTAUX = 0.05408, printed 0.0548
  - sgt1922 p.219 (f243) classes barley 1917 tot: Européens + Indigènes vs TOTAUX: cells give 475942.56, printed 465932.56 (difference -10010.00)
  - sgt1922 p.219 (f243) classes barley 1918_ind: classes vs TOTAUX: cells give 534695.24, printed 543695.24 (difference 9000.00)
  - sgt1922 p.219 (f243) classes barley 1918_ind r4: c4 / TOTAUX = 0.11069, printed 0.1272
  - sgt1922 p.219 (f243) classes barley 1918_tot: classes vs TOTAUX: cells give 566011.71, printed 565011.77 (difference -999.94)
  - sgt1922 p.219 (f243) classes barley 1918_tot r6: c6 / TOTAUX = 0.62815, printed 0.6821
  - sgt1922 p.218 (f242) classes barley 1918 c1: Européens + Indigènes vs TOTAUX: cells give 12828.85, printed 12828.79 (difference -0.06)
  - sgt1922 p.219 (f243) classes barley 1918 c4: Européens + Indigènes vs TOTAUX: cells give 60662.80, printed 69662.80 (difference 9000.00)
  - sgt1922 p.219 (f243) classes barley 1918 c6: Européens + Indigènes vs TOTAUX: cells give 353912.02, printed 354912.02 (difference 1000.00)
  - sgt1922 p.218 (f242) classes barley 1919_eur r2: c2 / TOTAUX = 0.06609, printed 0.0647
  - sgt1922 p.219 (f243) classes barley 1919_ind r6: c6 / TOTAUX = 0.26261, printed 0.2655
  - sgt1922 p.219 (f243) classes barley 1919_tot: classes vs TOTAUX: cells give 351081.45, printed 351281.45 (difference 200.00)
  - sgt1922 p.218 (f242) classes barley 1919 c2: Européens + Indigènes vs TOTAUX: cells give 77358.81, printed 77158.81 (difference -200.00)
  - sgt1922 p.219 (f243) classes barley 1921_ind r6: c6 / TOTAUX = 0.77621, printed 0.0762
  - sgt1922 p.221 (f245) classes oats 1918_eur: classes vs TOTAUX: cells give 36544.55, printed 36544.75 (difference 0.20)
  - sgt1922 p.221 (f245) classes oats 1918_tot: classes vs TOTAUX: cells give 65055.36, printed 65055.56 (difference 0.20)
  - sgt1922 p.220 (f244) classes oats 1918_tot r2: c2 / TOTAUX = 0.00869, printed 0.0040
  - sgt1922 p.221 (f245) classes oats 1918_tot r5: c5 / TOTAUX = 0.01555, printed 0.0170
  - sgt1922 p.220 (f244) classes oats 1919_eur r3: c3 / TOTAUX = 0.02136, printed 0.213
  - sgt1922 p.221 (f245) classes oats 1919_ind: classes vs TOTAUX: cells give 16965.37, printed 18535.37 (difference 1570.00)
  - sgt1922 p.220 (f244) classes oats 1919_ind r3: c3 / TOTAUX = 0.00780, printed 0.0925
  - sgt1922 p.220 (f244) classes oats 1919 c3: Européens + Indigènes vs TOTAUX: cells give 833.01, printed 2403.01 (difference 1570.00)
  - sgt1922 p.221 (f245) classes oats 1920_ind: classes vs TOTAUX: cells give 18873.03, printed 18873.13 (difference 0.10)
  - sgt1922 p.221 (f245) classes oats 1920 tot: Européens + Indigènes vs TOTAUX: cells give 56770.45, printed 56770.35 (difference -0.10)
  - sgt1922 p.221 (f245) classes oats 1921_tot: classes vs TOTAUX: cells give 63426.30, printed 63426.20 (difference -0.10)
  - sgt1922 p.221 (f245) classes oats 1921 c5: Européens + Indigènes vs TOTAUX: cells give 636.57, printed 636.67 (difference 0.10)
  - sgt1922 p.220 (f244) classes maize 1919_eur r1: c1 / TOTAUX = 0.01641, printed 0.0016
  - sgt1922 p.221 (f245) classes maize 1921_eur: classes vs TOTAUX: cells give 495.30, printed 494.80 (difference -0.50)
  - sgt1922 p.221 (f245) classes maize 1921_tot: classes vs TOTAUX: cells give 20498.10, printed 20497.60 (difference -0.50)
  - sgt1922 p.220 (f244) classes maize 1922_ind r2: c2 / TOTAUX = 0.13611, printed 0.0136
  - sgt1922 p.221 (f245) classes maize 1922_tot: classes vs TOTAUX: cells give 4122.32, printed 4121.32 (difference -1.00)
  - sgt1922 p.221 (f245) classes maize 1922 tot: Européens + Indigènes vs TOTAUX: cells give 4122.32, printed 4121.32 (difference -1.00)
  - sgt1922 p.221 (f245) classes maize 1922: TOTAUX vs surfaces imposées: cells give 4121.32, printed 4122.32 (difference 1.00)
  - sgt1922 p.223 (f247) classes sorghum 1919_eur r4: c4 / TOTAUX = 0.00194, printed 0
  - sgt1922 p.222 (f246) classes sorghum 1919_ind r2: c2 / TOTAUX = 0.15748, printed 0.1666
  - sgt1922 p.222 (f246) classes sorghum 1919_tot r3: c3 / TOTAUX = 0.00414, printed 0.0049
  - sgt1922 p.223 (f247) classes sorghum 1921_ind: classes vs TOTAUX: cells give 985.43, printed 985.47 (difference 0.04)
  - sgt1922 p.223 (f247) classes sorghum 1921_tot: classes vs TOTAUX: cells give 1451.74, printed 1451.78 (difference 0.04)
  - sgt1922 p.222 (f246) classes sorghum 1921_tot r1: c1 / TOTAUX = 0.00197, printed 0.0012
  - sgt1922 p.223 (f247) classes sorghum 1921_tot r6: c6 / TOTAUX = 0.94540, printed 0.0946
  - sgt1922 p.223 (f247) classes sorghum 1921: TOTAUX vs surfaces imposées: cells give 1451.78, printed 1451.74 (difference -0.04)
  - sgt1922 p.223 (f247) classes beans 1919_ind: classes vs TOTAUX: cells give 11303.36, printed 21213.36 (difference 9910.00)
  - sgt1922 p.223 (f247) classes beans 1919_tot: classes vs TOTAUX: cells give 16246.41, printed 26156.41 (difference 9910.00)
  - sgt1922 p.223 (f247) classes beans 1920_eur: classes vs TOTAUX: cells give 4495.75, printed 4495.65 (difference -0.10)
  - sgt1922 p.222 (f246) classes beans 1920_eur r1: c1 / TOTAUX = 0.03351, printed 0.5335
  - sgt1922 p.223 (f247) classes beans 1920_ind r6: c6 / TOTAUX = 0.26585, printed 0.2688
  - sgt1922 p.223 (f247) classes beans 1920 tot: Européens + Indigènes vs TOTAUX: cells give 20770.08, printed 20770.18 (difference 0.10)
  - sgt1922 p.223 (f247) classes beans 1921: TOTAUX vs surfaces imposées: cells give 23183.28, printed 23183.20 (difference -0.08)
  - sgt1922 p.223 (f247) classes beans 1922_eur r4: c4 / TOTAUX = 0.14614, printed 0.1429
  - sgt1922 p.224 (f248) classes chickpeas 1919_eur r3: c3 / TOTAUX = 0.03771, printed 0.0371
  - sgt1922 p.225 (f249) classes chickpeas 1920_eur: classes vs TOTAUX: cells give 1328.34, printed 928.34 (difference -400.00)
  - sgt1922 p.224 (f248) classes chickpeas 1920_eur r1: c1 / TOTAUX = 0.50716, printed 0.0762
  - sgt1922 p.224 (f248) classes chickpeas 1920 c1: Européens + Indigènes vs TOTAUX: cells give 914.00, printed 514 (difference -400.00)
  - sgt1922 p.224 (f248) classes chickpeas 1921_eur r3: c3 / TOTAUX = 0.01131, printed 0.0171
  - sgt1922 p.225 (f249) classes chickpeas 1921_ind r6: c6 / TOTAUX = 0.79811, printed 0.0798
  - sgt1922 p.225 (f249) classes chickpeas 1922: TOTAUX vs surfaces imposées: cells give 1017.03, printed 1017 (difference -0.03)
  - sgt1922 p.225 (f249) classes flax 1919_eur: classes vs TOTAUX: cells give 754.21, printed 751.21 (difference -3.00)
  - sgt1922 p.225 (f249) classes flax 1919_ind: classes vs TOTAUX: cells give 2299.03, printed 2308.03 (difference 9.00)
  - sgt1922 p.224 (f248) classes flax 1919_tot r1: c1 / TOTAUX = 0.02643, printed 0.0206
  - sgt1922 p.225 (f249) classes flax 1919 c6: Européens + Indigènes vs TOTAUX: cells give 1913.36, printed 1922.36 (difference 9.00)
  - sgt1922 p.225 (f249) classes flax 1919 tot: Européens + Indigènes vs TOTAUX: cells give 3059.24, printed 3062.24 (difference 3.00)
  - sgt1922 p.224 (f248) classes flax 1921_ind r1: c1 / TOTAUX = 0.00964, printed 0.0960
  - sgt1922 p.225 (f249) classes flax 1922_tot: classes vs TOTAUX: cells give 1494.31, printed 1594.31 (difference 100.00)
  - sgt1922 p.225 (f249) classes flax 1922 tot: Européens + Indigènes vs TOTAUX: cells give 1494.31, printed 1594.31 (difference 100.00)
  - sgt1922 p.225 (f249) classes flax 1922: TOTAUX vs surfaces imposées: cells give 1594.31, printed 1494.31 (difference -100.00)
  - sgt1923 p.229 (f731) classes wheat 1916_eur: classes vs TOTAUX: cells give 63551.92, printed 63511.92 (difference -40.00)
  - sgt1923 p.229 (f731) classes wheat 1916_tot r5: c5 / TOTAUX = 0.08444, printed 0.0958
  - sgt1923 p.229 (f731) classes wheat 1916 tot: Européens + Indigènes vs TOTAUX: cells give 553072.51, printed 553112.51 (difference 40.00)
  - sgt1923 p.229 (f731) classes wheat 1916: TOTAUX vs surfaces imposées: cells give 553112.51, printed 600029.48 (difference 46916.97)
  - sgt1923 p.229 (f731) classes wheat 1918_eur: classes vs TOTAUX: cells give 81872.97, printed 81866.97 (difference -6.00)
  - sgt1923 p.229 (f731) classes wheat 1918_tot: classes vs TOTAUX: cells give 638276.59, printed 638270.59 (difference -6.00)
  - sgt1923 p.229 (f731) classes wheat 1919_ind r4: c4 / TOTAUX = 0.12618, printed 0.1211
  - sgt1923 p.229 (f731) classes wheat 1921_tot r5: c5 / TOTAUX = 0.05493, printed 0.0565
  - sgt1923 p.229 (f731) classes wheat 1922_ind: classes vs TOTAUX: cells give 271553.62, printed 271513.62 (difference -40.00)
  - sgt1923 p.229 (f731) classes wheat 1922_ind r4: c4 / TOTAUX = 0.13507, printed 0.1316
  - sgt1923 p.229 (f731) classes wheat 1922_tot: classes vs TOTAUX: cells give 346857.70, printed 316818.70 (difference -30039.00)
  - sgt1923 p.228 (f730) classes wheat 1922 c1: Européens + Indigènes vs TOTAUX: cells give 51914.27, printed 51913.27 (difference -1.00)
  - sgt1923 p.229 (f731) classes wheat 1922 tot: Européens + Indigènes vs TOTAUX: cells give 346818.70, printed 316818.70 (difference -30000.00)
  - sgt1923 p.229 (f731) classes wheat 1922: TOTAUX vs surfaces imposées: cells give 316818.70, printed 346818.70 (difference 30000.00)
  - sgt1923 p.228 (f730) classes wheat 1923_eur r1: c1 / TOTAUX = 0.00152, printed 0.2015
  - sgt1923 p.231 (f733) classes barley 1916_eur r6: c6 / TOTAUX = 0.69648, printed 0.0945
  - sgt1923 p.231 (f733) classes barley 1917_eur: classes vs TOTAUX: cells give 20223.77, printed 20233.77 (difference 10.00)
  - sgt1923 p.231 (f733) classes barley 1917_ind: classes vs TOTAUX: cells give 445708.79, printed 455708.79 (difference 10000.00)
  - sgt1923 p.230 (f732) classes barley 1917_tot r1: c1 / TOTAUX = 0.05408, printed 0.0548
  - sgt1923 p.231 (f733) classes barley 1917 tot: Européens + Indigènes vs TOTAUX: cells give 475942.56, printed 465932.56 (difference -10010.00)
  - sgt1923 p.231 (f733) classes barley 1918_ind: classes vs TOTAUX: cells give 534695.24, printed 543695.24 (difference 9000.00)
  - sgt1923 p.231 (f733) classes barley 1918_ind r4: c4 / TOTAUX = 0.11069, printed 0.1272
  - sgt1923 p.231 (f733) classes barley 1918_tot: classes vs TOTAUX: cells give 566011.71, printed 565011.77 (difference -999.94)
  - sgt1923 p.231 (f733) classes barley 1918_tot r6: c6 / TOTAUX = 0.62815, printed 0.6821
  - sgt1923 p.230 (f732) classes barley 1918 c1: Européens + Indigènes vs TOTAUX: cells give 12828.85, printed 12828.79 (difference -0.06)
  - sgt1923 p.231 (f733) classes barley 1918 c4: Européens + Indigènes vs TOTAUX: cells give 60662.80, printed 69662.80 (difference 9000.00)
  - sgt1923 p.231 (f733) classes barley 1918 c6: Européens + Indigènes vs TOTAUX: cells give 353912.02, printed 354912.02 (difference 1000.00)
  - sgt1923 p.230 (f732) classes barley 1919_eur r2: c2 / TOTAUX = 0.06609, printed 0.0647
  - sgt1923 p.231 (f733) classes barley 1919_ind r6: c6 / TOTAUX = 0.26261, printed 0.2655
  - sgt1923 p.231 (f733) classes barley 1919_tot: classes vs TOTAUX: cells give 351081.45, printed 351281.45 (difference 200.00)
  - sgt1923 p.230 (f732) classes barley 1919 c2: Européens + Indigènes vs TOTAUX: cells give 77358.81, printed 77158.81 (difference -200.00)
  - sgt1923 p.231 (f733) classes barley 1921_ind r6: c6 / TOTAUX = 0.77621, printed 0.0762
  - sgt1923 p.232 (f734) classes oats 1919_eur r3: c3 / TOTAUX = 0.02136, printed 0.213
  - sgt1923 p.233 (f735) classes oats 1919_ind: classes vs TOTAUX: cells give 16965.37, printed 18535.37 (difference 1570.00)
  - sgt1923 p.232 (f734) classes oats 1919_ind r3: c3 / TOTAUX = 0.00780, printed 0.0925
  - sgt1923 p.232 (f734) classes oats 1919 c3: Européens + Indigènes vs TOTAUX: cells give 833.01, printed 2403.01 (difference 1570.00)
  - sgt1923 p.233 (f735) classes oats 1920_ind: classes vs TOTAUX: cells give 18873.03, printed 18873.13 (difference 0.10)
  - sgt1923 p.233 (f735) classes oats 1920 tot: Européens + Indigènes vs TOTAUX: cells give 56770.45, printed 56770.35 (difference -0.10)
  - sgt1923 p.233 (f735) classes oats 1921_tot: classes vs TOTAUX: cells give 63426.30, printed 63426.20 (difference -0.10)
  - sgt1923 p.233 (f735) classes oats 1921 c5: Européens + Indigènes vs TOTAUX: cells give 636.57, printed 636.67 (difference 0.10)
  - sgt1923 p.232 (f734) classes oats 1923_eur r2: c2 / TOTAUX = 0.00374, printed 0.0030
  - sgt1923 p.233 (f735) classes maize 1921_eur: classes vs TOTAUX: cells give 495.30, printed 494.80 (difference -0.50)
  - sgt1923 p.233 (f735) classes maize 1921_tot: classes vs TOTAUX: cells give 20498.10, printed 20497.60 (difference -0.50)
  - sgt1923 p.232 (f734) classes maize 1922_ind r2: c2 / TOTAUX = 0.13611, printed 0.0136
  - sgt1923 p.233 (f735) classes maize 1922_tot: classes vs TOTAUX: cells give 4122.32, printed 4121.32 (difference -1.00)
  - sgt1923 p.233 (f735) classes maize 1922 tot: Européens + Indigènes vs TOTAUX: cells give 4122.32, printed 4121.32 (difference -1.00)
  - sgt1923 p.233 (f735) classes maize 1922: TOTAUX vs surfaces imposées: cells give 4121.32, printed 4122.32 (difference 1.00)
  - sgt1923 p.233 (f735) classes maize 1923_eur r6: c6 / TOTAUX = 0.96182, printed 0.9929
  - sgt1923 p.235 (f737) classes sorghum 1920_eur: classes vs TOTAUX: cells give 123.81, printed 206.65 (difference 82.84)
  - sgt1923 p.235 (f737) classes sorghum 1920_ind: classes vs TOTAUX: cells give 1425.48, printed 1094.34 (difference -331.14)
  - sgt1923 p.235 (f737) classes sorghum 1920_tot: classes vs TOTAUX: cells give 1549.29, printed 1300.99 (difference -248.30)
  - sgt1923 p.235 (f737) classes sorghum 1920: TOTAUX vs surfaces imposées: cells give 1300.99, printed 1549.29 (difference 248.30)
  - sgt1923 p.235 (f737) classes sorghum 1921_eur: classes vs TOTAUX: cells give 466.31, printed 123.81 (difference -342.50)
  - sgt1923 p.235 (f737) classes sorghum 1921_ind: classes vs TOTAUX: cells give 985.43, printed 1425.48 (difference 440.05)
  - sgt1923 p.235 (f737) classes sorghum 1921_tot: classes vs TOTAUX: cells give 1451.74, printed 1549.29 (difference 97.55)
  - sgt1923 p.234 (f736) classes sorghum 1921_tot r1: c1 / TOTAUX = 0.00185, printed 0.0012
  - sgt1923 p.235 (f737) classes sorghum 1921_tot r6: c6 / TOTAUX = 0.88590, printed 0.0946
  - sgt1923 p.235 (f737) classes sorghum 1921: TOTAUX vs surfaces imposées: cells give 1549.29, printed 1451.74 (difference -97.55)
  - sgt1923 p.235 (f737) classes sorghum 1922_eur: classes vs TOTAUX: cells give 76.70, printed 466.31 (difference 389.61)
  - sgt1923 p.235 (f737) classes sorghum 1922_ind: classes vs TOTAUX: cells give 1234.32, printed 985.47 (difference -248.85)
  - sgt1923 p.235 (f737) classes sorghum 1922_tot: classes vs TOTAUX: cells give 1311.02, printed 1451.78 (difference 140.76)
  - sgt1923 p.235 (f737) classes sorghum 1922: TOTAUX vs surfaces imposées: cells give 1451.78, printed 1311.02 (difference -140.76)
  - sgt1923 p.235 (f737) classes sorghum 1923_ind r4: c4 / TOTAUX = 0.01970, printed 0.0188
  - sgt1923 p.235 (f737) classes beans 1920_eur: classes vs TOTAUX: cells give 4495.75, printed 4495.65 (difference -0.10)
  - sgt1923 p.234 (f736) classes beans 1920_eur r1: c1 / TOTAUX = 0.03351, printed 0.5335
  - sgt1923 p.235 (f737) classes beans 1920_ind r6: c6 / TOTAUX = 0.26585, printed 0.2688
  - sgt1923 p.235 (f737) classes beans 1920 tot: Européens + Indigènes vs TOTAUX: cells give 20770.08, printed 20770.18 (difference 0.10)
  - sgt1923 p.235 (f737) classes beans 1921: TOTAUX vs surfaces imposées: cells give 23183.28, printed 23183.20 (difference -0.08)
  - sgt1923 p.235 (f737) classes beans 1922_eur r4: c4 / TOTAUX = 0.14614, printed 0.1429
  - sgt1923 p.237 (f739) classes chickpeas 1920_eur: classes vs TOTAUX: cells give 1328.34, printed 928.34 (difference -400.00)
  - sgt1923 p.236 (f738) classes chickpeas 1920_eur r1: c1 / TOTAUX = 0.50716, printed 0.0762
  - sgt1923 p.236 (f738) classes chickpeas 1920 c1: Européens + Indigènes vs TOTAUX: cells give 914.00, printed 514 (difference -400.00)
  - sgt1923 p.236 (f738) classes chickpeas 1921_eur r3: c3 / TOTAUX = 0.01131, printed 0.0171
  - sgt1923 p.237 (f739) classes chickpeas 1921_ind r6: c6 / TOTAUX = 0.79811, printed 0.0798
  - sgt1923 p.237 (f739) classes chickpeas 1922: TOTAUX vs surfaces imposées: cells give 1017.03, printed 1017 (difference -0.03)
  - sgt1923 p.236 (f738) classes flax 1921_ind r1: c1 / TOTAUX = 0.00964, printed 0.0960
  - sgt1923 p.237 (f739) classes flax 1922_tot: classes vs TOTAUX: cells give 1494.31, printed 1594.31 (difference 100.00)
  - sgt1923 p.237 (f739) classes flax 1922 tot: Européens + Indigènes vs TOTAUX: cells give 1494.31, printed 1594.31 (difference 100.00)
  - sgt1923 p.237 (f739) classes flax 1922: TOTAUX vs surfaces imposées: cells give 1594.31, printed 1494.31 (difference -100.00)
  - sgt1923 p.236 (f738) classes flax 1923_eur r1: c1 / TOTAUX = 0.08835, printed 0.0083
  - sgt1923 p.236 (f738) classes flax 1923_ind r1: c1 / TOTAUX = 0.00293, printed 0.0236
  - sgt1924 p.237 (f1227) classes wheat 1918_eur: classes vs TOTAUX: cells give 81872.97, printed 81866.97 (difference -6.00)
  - sgt1924 p.237 (f1227) classes wheat 1918_tot: classes vs TOTAUX: cells give 638276.59, printed 638270.59 (difference -6.00)
  - sgt1924 p.237 (f1227) classes wheat 1919_ind r4: c4 / TOTAUX = 0.12618, printed 0.1211
  - sgt1924 p.237 (f1227) classes wheat 1921_tot r5: c5 / TOTAUX = 0.05493, printed 0.0565
  - sgt1924 p.237 (f1227) classes wheat 1922_ind: classes vs TOTAUX: cells give 271553.62, printed 271513.62 (difference -40.00)
  - sgt1924 p.237 (f1227) classes wheat 1922_ind r4: c4 / TOTAUX = 0.13507, printed 0.1316
  - sgt1924 p.237 (f1227) classes wheat 1922_tot: classes vs TOTAUX: cells give 346857.70, printed 316818.70 (difference -30039.00)
  - sgt1924 p.236 (f1226) classes wheat 1922 c1: Européens + Indigènes vs TOTAUX: cells give 51914.27, printed 51913.27 (difference -1.00)
  - sgt1924 p.237 (f1227) classes wheat 1922 tot: Européens + Indigènes vs TOTAUX: cells give 346818.70, printed 316818.70 (difference -30000.00)
  - sgt1924 p.237 (f1227) classes wheat 1922: TOTAUX vs surfaces imposées: cells give 316818.70, printed 346818.70 (difference 30000.00)
  - sgt1924 p.236 (f1226) classes wheat 1923_eur r1: c1 / TOTAUX = 0.00152, printed 0.2015
  - sgt1924 p.239 (f1229) classes barley 1917_eur: classes vs TOTAUX: cells give 20223.77, printed 20233.77 (difference 10.00)
  - sgt1924 p.239 (f1229) classes barley 1917_ind: classes vs TOTAUX: cells give 445708.79, printed 455708.79 (difference 10000.00)
  - sgt1924 p.238 (f1228) classes barley 1917_tot r1: c1 / TOTAUX = 0.05408, printed 0.0548
  - sgt1924 p.239 (f1229) classes barley 1917 tot: Européens + Indigènes vs TOTAUX: cells give 475942.56, printed 465932.56 (difference -10010.00)
  - sgt1924 p.239 (f1229) classes barley 1918_ind: classes vs TOTAUX: cells give 534695.24, printed 543695.24 (difference 9000.00)
  - sgt1924 p.239 (f1229) classes barley 1918_ind r4: c4 / TOTAUX = 0.11069, printed 0.1272
  - sgt1924 p.239 (f1229) classes barley 1918_tot: classes vs TOTAUX: cells give 566011.71, printed 565011.77 (difference -999.94)
  - sgt1924 p.239 (f1229) classes barley 1918_tot r6: c6 / TOTAUX = 0.62815, printed 0.6821
  - sgt1924 p.238 (f1228) classes barley 1918 c1: Européens + Indigènes vs TOTAUX: cells give 12828.85, printed 12828.79 (difference -0.06)
  - sgt1924 p.239 (f1229) classes barley 1918 c4: Européens + Indigènes vs TOTAUX: cells give 60662.80, printed 69662.80 (difference 9000.00)
  - sgt1924 p.239 (f1229) classes barley 1918 c6: Européens + Indigènes vs TOTAUX: cells give 353912.02, printed 354912.02 (difference 1000.00)
  - sgt1924 p.238 (f1228) classes barley 1919_eur r2: c2 / TOTAUX = 0.06609, printed 0.0647
  - sgt1924 p.239 (f1229) classes barley 1919_ind r6: c6 / TOTAUX = 0.26261, printed 0.2655
  - sgt1924 p.239 (f1229) classes barley 1919_tot: classes vs TOTAUX: cells give 351081.45, printed 351281.45 (difference 200.00)
  - sgt1924 p.238 (f1228) classes barley 1919 c2: Européens + Indigènes vs TOTAUX: cells give 77358.81, printed 77158.81 (difference -200.00)
  - sgt1924 p.239 (f1229) classes barley 1921_ind r6: c6 / TOTAUX = 0.77621, printed 0.0762
  - sgt1924 p.240 (f1230) classes oats 1919_eur r3: c3 / TOTAUX = 0.02136, printed 0.213
  - sgt1924 p.241 (f1231) classes oats 1919_ind: classes vs TOTAUX: cells give 16965.37, printed 18535.37 (difference 1570.00)
  - sgt1924 p.240 (f1230) classes oats 1919_ind r3: c3 / TOTAUX = 0.00780, printed 0.0925
  - sgt1924 p.240 (f1230) classes oats 1919 c3: Européens + Indigènes vs TOTAUX: cells give 833.01, printed 2403.01 (difference 1570.00)
  - sgt1924 p.241 (f1231) classes oats 1920_ind: classes vs TOTAUX: cells give 18873.03, printed 18873.13 (difference 0.10)
  - sgt1924 p.241 (f1231) classes oats 1920 tot: Européens + Indigènes vs TOTAUX: cells give 56770.45, printed 56770.35 (difference -0.10)
  - sgt1924 p.241 (f1231) classes oats 1921_tot: classes vs TOTAUX: cells give 63426.30, printed 63426.20 (difference -0.10)
  - sgt1924 p.241 (f1231) classes oats 1921 c5: Européens + Indigènes vs TOTAUX: cells give 636.57, printed 636.67 (difference 0.10)
  - sgt1924 p.240 (f1230) classes oats 1923_eur r2: c2 / TOTAUX = 0.00374, printed 0.0030
  - sgt1924 p.243 (f1233) classes maize 1921_eur: classes vs TOTAUX: cells give 495.30, printed 494.80 (difference -0.50)
  - sgt1924 p.243 (f1233) classes maize 1921_tot: classes vs TOTAUX: cells give 20498.10, printed 20497.60 (difference -0.50)
  - sgt1924 p.242 (f1232) classes maize 1922_ind r2: c2 / TOTAUX = 0.13611, printed 0.0136
  - sgt1924 p.243 (f1233) classes maize 1922_tot: classes vs TOTAUX: cells give 4122.32, printed 4121.32 (difference -1.00)
  - sgt1924 p.243 (f1233) classes maize 1922 tot: Européens + Indigènes vs TOTAUX: cells give 4122.32, printed 4121.32 (difference -1.00)
  - sgt1924 p.243 (f1233) classes maize 1922: TOTAUX vs surfaces imposées: cells give 4121.32, printed 4122.32 (difference 1.00)
  - sgt1924 p.243 (f1233) classes maize 1923_eur r6: c6 / TOTAUX = 0.96182, printed 0.9929
  - sgt1924 p.245 (f1235) classes sorghum 1920_eur: classes vs TOTAUX: cells give 123.81, printed 206.65 (difference 82.84)
  - sgt1924 p.245 (f1235) classes sorghum 1920_ind: classes vs TOTAUX: cells give 1425.48, printed 1094.34 (difference -331.14)
  - sgt1924 p.245 (f1235) classes sorghum 1920_tot: classes vs TOTAUX: cells give 1549.29, printed 1300.99 (difference -248.30)
  - sgt1924 p.245 (f1235) classes sorghum 1920: TOTAUX vs surfaces imposées: cells give 1300.99, printed 1549.29 (difference 248.30)
  - sgt1924 p.245 (f1235) classes sorghum 1921_eur: classes vs TOTAUX: cells give 466.31, printed 123.81 (difference -342.50)
  - sgt1924 p.245 (f1235) classes sorghum 1921_ind: classes vs TOTAUX: cells give 985.43, printed 1425.48 (difference 440.05)
  - sgt1924 p.245 (f1235) classes sorghum 1921_tot: classes vs TOTAUX: cells give 1451.74, printed 1549.29 (difference 97.55)
  - sgt1924 p.244 (f1234) classes sorghum 1921_tot r1: c1 / TOTAUX = 0.00185, printed 0.0012
  - sgt1924 p.245 (f1235) classes sorghum 1921_tot r6: c6 / TOTAUX = 0.88590, printed 0.0946
  - sgt1924 p.245 (f1235) classes sorghum 1921: TOTAUX vs surfaces imposées: cells give 1549.29, printed 1451.74 (difference -97.55)
  - sgt1924 p.245 (f1235) classes sorghum 1922_eur: classes vs TOTAUX: cells give 76.70, printed 466.31 (difference 389.61)
  - sgt1924 p.245 (f1235) classes sorghum 1922_ind: classes vs TOTAUX: cells give 1234.32, printed 985.47 (difference -248.85)
  - sgt1924 p.245 (f1235) classes sorghum 1922_tot: classes vs TOTAUX: cells give 1311.02, printed 1451.78 (difference 140.76)
  - sgt1924 p.245 (f1235) classes sorghum 1922: TOTAUX vs surfaces imposées: cells give 1451.78, printed 1311.02 (difference -140.76)
  - sgt1924 p.245 (f1235) classes sorghum 1923_ind r4: c4 / TOTAUX = 0.01970, printed 0.0188
  - sgt1924 p.245 (f1235) classes sorghum 1924_eur: classes vs TOTAUX: cells give 682.00, printed 678.00 (difference -4.00)
  - sgt1924 p.245 (f1235) classes sorghum 1924_tot: classes vs TOTAUX: cells give 2361.77, printed 2357.77 (difference -4.00)
  - sgt1924 p.245 (f1235) classes sorghum 1924: TOTAUX vs surfaces imposées: cells give 2357.77, printed 2361.77 (difference 4.00)
  - sgt1924 p.247 (f1237) classes beans 1920_eur: classes vs TOTAUX: cells give 4496.75, printed 4495.65 (difference -1.10)
  - sgt1924 p.246 (f1236) classes beans 1920_eur r1: c1 / TOTAUX = 0.03351, printed 0.5335
  - sgt1924 p.247 (f1237) classes beans 1920_ind r6: c6 / TOTAUX = 0.26585, printed 0.2688
  - sgt1924 p.247 (f1237) classes beans 1920_tot: classes vs TOTAUX: cells give 20470.18, printed 20770.18 (difference 300.00)
  - sgt1924 p.247 (f1237) classes beans 1920_tot r6: c6 / TOTAUX = 0.29520, printed 0.3096
  - sgt1924 p.247 (f1237) classes beans 1920 c5: Européens + Indigènes vs TOTAUX: cells give 1278.05, printed 1277.05 (difference -1.00)
  - sgt1924 p.247 (f1237) classes beans 1920 c6: Européens + Indigènes vs TOTAUX: cells give 6431.36, printed 6131.36 (difference -300.00)
  - sgt1924 p.247 (f1237) classes beans 1920 tot: Européens + Indigènes vs TOTAUX: cells give 20770.08, printed 20770.18 (difference 0.10)
  - sgt1924 p.247 (f1237) classes beans 1921: TOTAUX vs surfaces imposées: cells give 23183.28, printed 23183.20 (difference -0.08)
  - sgt1924 p.247 (f1237) classes beans 1922_eur r4: c4 / TOTAUX = 0.14614, printed 0.1429
  - sgt1924 p.247 (f1237) classes beans 1922_ind: classes vs TOTAUX: cells give 9651.88, printed 651.88 (difference -9000.00)
  - sgt1924 p.247 (f1237) classes beans 1922 tot: Européens + Indigènes vs TOTAUX: cells give 6968.34, printed 15968.34 (difference 9000.00)
  - sgt1924 p.246 (f1236) classes beans 1924_ind r2: c2 / TOTAUX = 0.03046, printed 0.0310
  - sgt1924 p.249 (f1239) classes chickpeas 1920_eur: classes vs TOTAUX: cells give 1328.34, printed 928.34 (difference -400.00)
  - sgt1924 p.248 (f1238) classes chickpeas 1920_eur r1: c1 / TOTAUX = 0.50716, printed 0.0762
  - sgt1924 p.249 (f1239) classes chickpeas 1920_tot: classes vs TOTAUX: cells give 6483.93, printed 6554.87 (difference 70.94)
  - sgt1924 p.249 (f1239) classes chickpeas 1920_tot r5: c5 / TOTAUX = 0.02822, printed 0.0390
  - sgt1924 p.248 (f1238) classes chickpeas 1920 c1: Européens + Indigènes vs TOTAUX: cells give 914.00, printed 514.11 (difference -399.89)
  - sgt1924 p.249 (f1239) classes chickpeas 1920 c5: Européens + Indigènes vs TOTAUX: cells give 256.02, printed 184.97 (difference -71.05)
  - sgt1924 p.248 (f1238) classes chickpeas 1921_eur r3: c3 / TOTAUX = 0.01131, printed 0.0171
  - sgt1924 p.249 (f1239) classes chickpeas 1921_ind r6: c6 / TOTAUX = 0.79811, printed 0.0798
  - sgt1924 p.249 (f1239) classes chickpeas 1922: TOTAUX vs surfaces imposées: cells give 1017.03, printed 1017 (difference -0.03)
  - sgt1924 p.249 (f1239) classes chickpeas 1924_ind: classes vs TOTAUX: cells give 3983.45, printed 3542.90 (difference -440.55)
  - sgt1924 p.249 (f1239) classes chickpeas 1924_tot: classes vs TOTAUX: cells give 4920.40, printed 4479.85 (difference -440.55)
  - sgt1924 p.251 (f1241) classes flax 1920_eur: classes vs TOTAUX: cells give 992.27, printed 992.16 (difference -0.11)
  - sgt1924 p.251 (f1241) classes flax 1920_tot: classes vs TOTAUX: cells give 3060.25, printed 2989.20 (difference -71.05)
  - sgt1924 p.251 (f1241) classes flax 1920_tot r5: c5 / TOTAUX = 0.08565, printed 0.0618
  - sgt1924 p.250 (f1240) classes flax 1920 c2: Européens + Indigènes vs TOTAUX: cells give 494.05, printed 493.94 (difference -0.11)
  - sgt1924 p.251 (f1241) classes flax 1920 c5: Européens + Indigènes vs TOTAUX: cells give 184.97, printed 256.02 (difference 71.05)
  - sgt1924 p.250 (f1240) classes flax 1921_ind r1: c1 / TOTAUX = 0.00964, printed 0.0960
  - sgt1924 p.251 (f1241) classes flax 1922_tot: classes vs TOTAUX: cells give 1494.31, printed 1594.31 (difference 100.00)
  - sgt1924 p.251 (f1241) classes flax 1922 tot: Européens + Indigènes vs TOTAUX: cells give 1494.31, printed 1594.31 (difference 100.00)
  - sgt1924 p.251 (f1241) classes flax 1922: TOTAUX vs surfaces imposées: cells give 1594.31, printed 1494.31 (difference -100.00)
  - sgt1924 p.250 (f1240) classes flax 1923_eur r1: c1 / TOTAUX = 0.08835, printed 0.0083
  - sgt1924 p.250 (f1240) classes flax 1923_ind r1: c1 / TOTAUX = 0.00293, printed 0.0236
  - sgt1922 p.216 (f240) surfaces wheat 1914: imposées + non imposées (with or without the terres nouvellement défrichées) vs ensemencées: cells give 405965.06, printed 405965.66 (difference 0.60)
  - sgt1922 p.217 (f241) surfaces wheat 1919: imposées + non imposées (with or without the terres nouvellement défrichées) vs ensemencées: cells give 568110.78, printed 508110.78 (difference -60000.00)
  - sgt1922 p.219 (f243) surfaces barley 1917: imposées + non imposées (with or without the terres nouvellement défrichées) vs ensemencées: cells give 478849.58, printed 478849.68 (difference 0.10)
  - sgt1922 p.219 (f243) surfaces barley 1918: imposées + non imposées (with or without the terres nouvellement défrichées) vs ensemencées: cells give 573737.97, printed 573738.06 (difference 0.09)
  - sgt1922 p.221 (f245) surfaces maize 1922: imposées + non imposées (with or without the terres nouvellement défrichées) vs ensemencées: cells give 4888.83, printed 4888.03 (difference -0.80)
  - sgt1922 p.223 (f247) surfaces beans 1921: imposées + non imposées (with or without the terres nouvellement défrichées) vs ensemencées: cells give 23513.46, printed 23477.37 (difference -36.09)
  - sgt1923 p.228 (f730) surfaces wheat 1916: imposées + non imposées (with or without the terres nouvellement défrichées) vs ensemencées: cells give 646946.45, printed 553112.51 (difference -93833.94)
  - sgt1923 p.229 (f731) surfaces wheat 1919: imposées + non imposées (with or without the terres nouvellement défrichées) vs ensemencées: cells give 568110.78, printed 508110.78 (difference -60000.00)
  - sgt1923 p.231 (f733) surfaces barley 1917: imposées + non imposées (with or without the terres nouvellement défrichées) vs ensemencées: cells give 478849.58, printed 478849.68 (difference 0.10)
  - sgt1923 p.231 (f733) surfaces barley 1918: imposées + non imposées (with or without the terres nouvellement défrichées) vs ensemencées: cells give 573737.97, printed 573738.06 (difference 0.09)
  - sgt1923 p.233 (f735) surfaces maize 1922: imposées + non imposées (with or without the terres nouvellement défrichées) vs ensemencées: cells give 4888.83, printed 4888.03 (difference -0.80)
  - sgt1923 p.233 (f735) surfaces maize 1923: imposées + non imposées (with or without the terres nouvellement défrichées) vs ensemencées: cells give 15661.65, printed 15841.65 (difference 180.00)
  - sgt1923 p.235 (f737) surfaces beans 1921: imposées + non imposées (with or without the terres nouvellement défrichées) vs ensemencées: cells give 23513.46, printed 23477.37 (difference -36.09)
  - sgt1923 p.237 (f739) surfaces flax 1923: imposées + non imposées (with or without the terres nouvellement défrichées) vs ensemencées: cells give 1745.63, printed 1747.63 (difference 2.00)
  - sgt1924 p.236 (f1226) surfaces wheat 1916: imposées + non imposées (with or without the terres nouvellement défrichées) vs ensemencées: cells give 646946.45, printed 553112.51 (difference -93833.94)
  - sgt1924 p.237 (f1227) surfaces wheat 1919: imposées + non imposées (with or without the terres nouvellement défrichées) vs ensemencées: cells give 568110.78, printed 508110.78 (difference -60000.00)
  - sgt1924 p.237 (f1227) surfaces wheat 1924: imposées + non imposées (with or without the terres nouvellement défrichées) vs ensemencées: cells give 484568.34, printed 484568.36 (difference 0.02)
  - sgt1924 p.239 (f1229) surfaces barley 1917: imposées + non imposées (with or without the terres nouvellement défrichées) vs ensemencées: cells give 478849.58, printed 478849.68 (difference 0.10)
  - sgt1924 p.239 (f1229) surfaces barley 1918: imposées + non imposées (with or without the terres nouvellement défrichées) vs ensemencées: cells give 573737.97, printed 573738.06 (difference 0.09)
  - sgt1924 p.243 (f1233) surfaces maize 1922: imposées + non imposées (with or without the terres nouvellement défrichées) vs ensemencées: cells give 4888.83, printed 4888.03 (difference -0.80)
  - sgt1924 p.243 (f1233) surfaces maize 1923: imposées + non imposées (with or without the terres nouvellement défrichées) vs ensemencées: cells give 15661.65, printed 15841.65 (difference 180.00)
  - sgt1924 p.247 (f1237) surfaces beans 1921: imposées + non imposées (with or without the terres nouvellement défrichées) vs ensemencées: cells give 23513.46, printed 23477.37 (difference -36.09)
  - sgt1924 p.251 (f1241) surfaces flax 1923: imposées + non imposées (with or without the terres nouvellement défrichées) vs ensemencées: cells give 1745.63, printed 1747.63 (difference 2.00)

- Overlapping printings: 2088 cell comparisons with other editions printing the same cell; 6 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1916 / tunisia / wheat / surfaces / all / sown / area | sgt1922 | 600029.48 | sgt1924 | 553112.51 |
| 1916 / tunisia / wheat / surfaces / all / taxed / area | sgt1922 | 553112.51 | sgt1924 | 600029.48 |
| 1920 / tunisia / broad_beans / yield_classes / european / yield_5_hl / area | sgt1922 | 662.23 | sgt1924 | 663.23 |
| 1920 / tunisia / broad_beans / yield_classes / european / yield_5_hl / area | sgt1923 | 662.23 | sgt1924 | 663.23 |
| 1920 / tunisia / flax / yield_classes / european / yield_2_hl / area | sgt1922 | 24 | sgt1924 | 24.11 |
| 1920 / tunisia / flax / yield_classes / european / yield_2_hl / area | sgt1923 | 24 | sgt1924 | 24.11 |

- Flagged cells: ocr_corrected: 2, reprint_corrected: 4, total_mismatch: 25.

  - sgt1922 p.216 1915 tunisia / wheat / yield_classes / indigenous / yield_3_hl / area / hectares = 55309.86 (total_mismatch)
  - sgt1922 p.216 1915 tunisia / wheat / yield_classes / indigenous / yield_3_hl / ratio_to_line_total / ratio = 0.1238 (ocr_corrected)
  - sgt1922 p.217 1916 tunisia / wheat / surfaces / all / sown / area / hectares = 600029.48 (reprint_corrected)
  - sgt1922 p.217 1916 tunisia / wheat / surfaces / all / taxed / area / hectares = 553112.51 (reprint_corrected)
  - sgt1923 p.231 1916 tunisia / barley / yield_classes / european / yield_6_hl_plus / ratio_to_line_total / ratio = 0.0945 (total_mismatch)
  - sgt1924 p.239 1918 tunisia / barley / yield_classes / indigenous / yield_4_hl / area / hectares = 60181.79 (total_mismatch)
  - sgt1922 p.220 1919 tunisia / maize / yield_classes / european / yield_1_hl / ratio_to_line_total / ratio = 0.0016 (total_mismatch)
  - sgt1922 p.220 1919 tunisia / maize / yield_classes / indigenous / yield_1_hl / ratio_to_line_total / ratio = 0.0095 (ocr_corrected)
  - sgt1922 p.222 1919 tunisia / sorghum / yield_classes / indigenous / yield_2_hl / ratio_to_line_total / ratio = 0.1666 (total_mismatch)
  - sgt1922 p.223 1919 tunisia / sorghum / yield_classes / european / yield_4_hl / ratio_to_line_total / ratio = 0 (total_mismatch)
  - sgt1922 p.223 1919 tunisia / broad_beans / yield_classes / indigenous / yield_6_hl_plus / area / hectares = 1105.13 (total_mismatch)
  - sgt1924 p.237 1919 tunisia / wheat / yield_classes / indigenous / yield_4_hl / ratio_to_line_total / ratio = 0.1211 (total_mismatch)
  - sgt1924 p.240 1919 tunisia / oats / yield_classes / european / yield_3_hl / ratio_to_line_total / ratio = 0.213 (total_mismatch)
  - sgt1924 p.240 1919 tunisia / oats / yield_classes / indigenous / yield_3_hl / area / hectares = 144.57 (total_mismatch)
  - sgt1923 p.235 1920 tunisia / broad_beans / yield_classes / european / yield_5_hl / area / hectares = 662.23 (reprint_corrected)
  - sgt1923 p.236 1920 tunisia / flax / yield_classes / european / yield_2_hl / area / hectares = 24 (reprint_corrected)
  - sgt1924 p.246 1920 tunisia / broad_beans / yield_classes / european / yield_1_hl / ratio_to_line_total / ratio = 0.5335 (total_mismatch)
  - sgt1924 p.248 1920 tunisia / chickpeas / yield_classes / european / yield_1_hl / area / hectares = 470.82 (total_mismatch)
  - sgt1924 p.239 1921 tunisia / barley / yield_classes / indigenous / yield_6_hl_plus / ratio_to_line_total / ratio = 0.0762 (total_mismatch)
  - sgt1924 p.248 1921 tunisia / chickpeas / yield_classes / european / yield_3_hl / ratio_to_line_total / ratio = 0.0171 (total_mismatch)
  - sgt1924 p.249 1921 tunisia / chickpeas / yield_classes / indigenous / yield_6_hl_plus / ratio_to_line_total / ratio = 0.0798 (total_mismatch)
  - sgt1924 p.250 1921 tunisia / flax / yield_classes / indigenous / yield_1_hl / ratio_to_line_total / ratio = 0.0960 (total_mismatch)
  - sgt1924 p.242 1922 tunisia / maize / yield_classes / indigenous / yield_2_hl / ratio_to_line_total / ratio = 0.0136 (total_mismatch)
  - sgt1925 p.275 1922 centre_south / wheat / yield_classes / indigenous / yield_6_hl_plus / percent_of_sown_area / percent = 13.14 (total_mismatch)
  - sgt1925 p.278 1922 north / oats / yield_classes / indigenous / yield_6_hl_plus / percent_of_sown_area / percent = 22.33 (total_mismatch)
  - sgt1924 p.236 1923 tunisia / wheat / yield_classes / european / yield_1_hl / ratio_to_line_total / ratio = 0.2015 (total_mismatch)
  - sgt1924 p.243 1923 tunisia / maize / yield_classes / european / yield_6_hl_plus / ratio_to_line_total / ratio = 0.9929 (total_mismatch)
  - sgt1924 p.250 1923 tunisia / flax / yield_classes / european / yield_1_hl / ratio_to_line_total / ratio = 0.0083 (total_mismatch)
  - sgt1924 p.250 1923 tunisia / flax / yield_classes / indigenous / yield_1_hl / ratio_to_line_total / ratio = 0.0236 (total_mismatch)
  - sgt1925 p.274 1925 north / wheat / yield_classes / indigenous / yield_6_hl_plus / area / hectares = 175582 (total_mismatch)
  - sgt1925 p.278 1925 north / oats / yield_classes / indigenous / yield_6_hl_plus / area / hectares = 14603 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (84 printings): sgt1922 f240, sgt1922 f241, sgt1922 f240, sgt1922 f241, sgt1922 f242, sgt1922 f243, sgt1922 f242, sgt1922 f243, sgt1922 f245, sgt1922 f244, sgt1922 f245, sgt1922 f245, sgt1922 f244, sgt1922 f245, sgt1922 f247, sgt1922 f246, sgt1922 f247, sgt1922 f247, sgt1922 f246, sgt1922 f247, sgt1922 f249, sgt1922 f248, sgt1922 f249, sgt1922 f249, sgt1922 f248, sgt1922 f249, sgt1923 f730, sgt1923 f731, sgt1923 f730, sgt1923 f731, sgt1923 f732, sgt1923 f733, sgt1923 f732, sgt1923 f733, sgt1923 f735, sgt1923 f734, sgt1923 f735, sgt1923 f735, sgt1923 f734, sgt1923 f735, sgt1923 f737, sgt1923 f736, sgt1923 f737, sgt1923 f737, sgt1923 f736, sgt1923 f737, sgt1923 f739, sgt1923 f738, sgt1923 f739, sgt1923 f739, sgt1923 f738, sgt1923 f739, sgt1924 f1226, sgt1924 f1227, sgt1924 f1226, sgt1924 f1227, sgt1924 f1228, sgt1924 f1229, sgt1924 f1228, sgt1924 f1229, sgt1924 f1231, sgt1924 f1230, sgt1924 f1231, sgt1924 f1233, sgt1924 f1232, sgt1924 f1233, sgt1924 f1235, sgt1924 f1234, sgt1924 f1235, sgt1924 f1237, sgt1924 f1236, sgt1924 f1237, sgt1924 f1239, sgt1924 f1238, sgt1924 f1239, sgt1924 f1241, sgt1924 f1240, sgt1924 f1241, sgt1925 f298, sgt1925 f299, sgt1925 f300, sgt1925 f301, sgt1925 f302, sgt1925 f303.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 45.
