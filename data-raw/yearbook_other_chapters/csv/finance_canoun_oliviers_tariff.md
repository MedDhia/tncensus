# Canoun des oliviers. b) Répartition des arbres imposables par catégorie du tarif

*Tax on olive trees (canoun des oliviers): taxable trees by caïdat and tariff.*

Source: *Statistique générale de la Tunisie*, chapter *Finances*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views: sgt1922 (`bpt6k9105649x`): p. 194, f218, p. 195, f219; sgt1923 (`bpt6k9105649x`): p. 206, f708, p. 207, f709; sgt1924 (`bpt6k9105649x`): p. 214, f1204, p. 215, f1205; sgt1925 (`bpt6k9105650k`): p. 250, f274, p. 251, f275; sgt1926 (`bpt6k9105650k`): p. 226, f790, p. 227, f791; sgt1927 (`bpt6k91056510`): p. 224, f252, p. 225, f253; sgt1928 (`bpt6k91056510`): p. 224, f776, p. 225, f777; sgt1929 (`bpt6k9105652d`): p. 226, f254, p. 227, f255; sgt1930 (`bpt6k9105652d`): p. 226, f788, p. 227, f789.

Transcriptions: `../transcribed/finance_canoun_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_finance_canoun.py build`.

Rows: 3272. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930.

Unit: number of trees; value_type: count.

Printed once per edition, each printing for its own year: every edition is kept (SPEC_ADDENDUM rule 5); `census` is the edition, `year` the year of the tree census (1er novembre <year>, printed in the title of a)).

## Columns

- `census`: edition (source code, see EDITIONS.md)
- `table_id`: transcription section (table a), b) or c))
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN) of the page the cell is printed on
- `year`: year of the census of the trees: the year of the "1er novembre <year>" printed in the title of a) (the edition year, except sgt1925 dattiers, titled 1924); b) and c) take the year of their a)
- `region`: région as printed, with its chef-lieu in brackets for the olive tables (from sgt1925: "1re Région (Bizerte)" ... "5me Région (Sfax)", "Territoires militaires du Sud"; date-palm tables: "5e Région", "Territoires militaires"); empty in sgt1922-sgt1924, which list caïdats only
- `controle_civil`: contrôle civil as printed (olive tables from sgt1925; empty otherwise)
- `caidat`: caïdat as printed in that table (spelling varies between editions and between a), b), c): Majeur / Madjeurs, Hammama / Hemmama, Ouled-Ayar / Oulad Ayar, Kef / Le Kef...); "Cap-Bon - Nabeul" and "Cap-Bon - Soliman" = the two lines printed under the brace of the caïdat Cap-Bon
- `tariff`: tax rate per tree, francs, as a code (`1.40`, `0.05`, ...); `former_tithe_proportional` = anciens pays à dîme, impôt proportionnel au revenu global (olive trees of the former tithe lands, taxed on their income instead of per tree)
- `tariff_fr`: printed column heading (the rate as printed)
- `value`: printed count (» = 0)
- `flag`: empty, or `total_mismatch` (printed value kept; the line TOTAL and the column Totaux, or the other tables of the same edition, identify it as the faulty cell; see the notes), `row_realigned` (figures printed on the line of another caïdat, stored under the caïdat they belong to; see the notes), `derived_from_totals` (digits lost in the gutter fold; value = line TOTAL minus the other cells of the line)

Nombre d'arbres imposés à each rate (sgt1922: twelve rates 0,05 .. 1,00 fr. per tree; from sgt1923 ten rates, without 0,35 and 0,45), and the column Anciens pays à dîme, impôt proportionnel au revenu global (trees of the former tithe lands of the north, taxed in proportion to their income), TOTAL (check, also = a) 20 ans imposables). From sgt1929 a new scale: 0,05 0,10 0,25 0,50 0,75 1,00 1,25 1,50 1,75 2,00. Not printed in sgt1935.

Footnotes: none printed under these tables.

## Validation

- Checks against printed totals and identities: 706; passed: 657; failed: 49.

Every failure was re-read on zoomed native-resolution crops; printed values are kept. Explanation, by edition:

  - sgt1922: Monastir 0,25 147.390 and 0,30 441.916 exceed the TOTAL 1.520.543 by 10; the 0,30 Totaux is 10 under its lines, so the 0,30 cell is flagged. Totaux TOTAL 9.094.192 against a) 9.094.191 (a) Totaux misprint). Souk-el-Arba 0,25 lost in the fold: derived from the TOTAL (285); the 0,25 Totaux is partly hidden (not checked).
  - sgt1923: Totaux 0,30 printed 103.643 (a digit dropped; the lines give 1.036.430), 0,75 1.988.190 and TOTAL 9.043.502 (= a) 20 ans imposables) against lines 1.987.890 and 9.043.802: the line Majeur 0,75 1.110 is 300 short of its TOTAL 1.938 (flagged), Kairouan TOTAL 15.415 for 15.115 (= a)). Zaghouan: 0,20 26, 0,30 877, 0,50 340, 0,75 4 printed besides an old-tithe figure equal to the TOTAL 82.972 (the same in sgt1924); not resolvable. Fraichiches and Majeur lines exchanged (row_realigned).
  - sgt1924: Monastir 0,20 123.275 (TOTAL and Totaux require 123.257, as in sgt1923) and Ouled-Aoun 0,25 6.940 (2.940, as in sgt1923), flagged; Zaghouan as in sgt1923.
  - sgt1925: Flagged (line TOTAL and column Totaux point to the same cell): Djerid 0,15 2.888 (2.848), Medjez-el-Bab 0,75 1.729 (3.729), Sousse 0,25 26.443 (26.433), Kairouan 0,20 252 (258); Fraichiches and Madjeurs 0,75 1.410 and 1.353 (sgt1924 prints them the other way round) fit neither TOTAL. Not attributable: Zaghouan (+10), Ouerghema (-10), Le Kef TOTAL 29.987 (a): 29.996), Madjeurs 0,50, Totaux 0,15, 0,20, 0,50, dime and TOTAL.
  - sgt1926: Medjez-el-Bab 0,75 1.729 (3.729, as in sgt1925), flagged; the Totaux 0,75 2.023.103 requires 3.729. The 0,15 figure 7 printed on the Fraichiches line belongs to Madjeurs (row_realigned).
  - sgt1929: New rates from this edition (0,05 .. 2,00). Souk-el-Khemis TOTAL 4.656 for 4.657 (a) and the tariff cells); the Totaux TOTAL follows it.
  - sgt1930: Bizerte old-tithe figure 429.239 (TOTAL 429.234 = a) imposables; the column Totaux 2.486.318 also requires 429.234) and Cap-Bon - Nabeul 0,75 91.643 (TOTAL and Totaux require 91.642): flagged.
  - sgt1927: Téboursouk 0,10 printed 1.079 (zoomed; the line TOTAL and the column Totaux require 1.179, as in sgt1926): flagged. Djerid TOTAL 21.481 against the misprinted a) 21.411 (see a)). The 0,15 Totaux is partly hidden in the fold (not checked).

Failed checks:

  - sgt1922 oliviers_tariff Totaux t6: sum of the lines (f219): cells give 1011961, printed 1011951 (difference -10)
  - sgt1923 oliviers_tariff Totaux t6: sum of the lines (f709): cells give 1036430, printed 103643 (difference -932787)
  - sgt1923 oliviers_tariff Totaux t9: sum of the lines (f709): cells give 1987890, printed 1988190 (difference 300)
  - sgt1923 oliviers_tariff Totaux tot: sum of the lines (f709): cells give 9043802, printed 9043502 (difference -300)
  - sgt1924 oliviers_tariff Totaux t4: sum of the lines (f1204): cells give 495748, printed 495730 (difference -18)
  - sgt1924 oliviers_tariff Totaux t5: sum of the lines (f1205): cells give 370492, printed 366492 (difference -4000)
  - sgt1925 oliviers_tariff Totaux t3: sum of the lines (f274): cells give 261091, printed 261051 (difference -40)
  - sgt1925 oliviers_tariff Totaux t4: sum of the lines (f275): cells give 495735, printed 495741 (difference 6)
  - sgt1925 oliviers_tariff Totaux t5: sum of the lines (f275): cells give 366496, printed 366486 (difference -10)
  - sgt1925 oliviers_tariff Totaux t8: sum of the lines (f275): cells give 1060410, printed 1060403 (difference -7)
  - sgt1925 oliviers_tariff Totaux t9: sum of the lines (f275): cells give 1986836, printed 1988836 (difference 2000)
  - sgt1925 oliviers_tariff Totaux dime: sum of the lines (f275): cells give 2471533, printed 2470343 (difference -1190)
  - sgt1925 oliviers_tariff Totaux tot: sum of the lines (f275): cells give 9103898, printed 9103897 (difference -1)
  - sgt1926 oliviers_tariff Totaux t9: sum of the lines (f791): cells give 2021103, printed 2023103 (difference 2000)
  - sgt1927 oliviers_tariff Totaux t2: sum of the lines (f252): cells give 201850, printed 201950 (difference 100)
  - sgt1929 oliviers_tariff Totaux tot: sum of the lines (f255): cells give 10103328, printed 10103329 (difference 1)
  - sgt1930 oliviers_tariff Totaux t5: sum of the lines (f789): cells give 1059222, printed 1059221 (difference -1)
  - sgt1930 oliviers_tariff Totaux dime: sum of the lines (f789): cells give 2486323, printed 2486318 (difference -5)
  - sgt1922 oliviers_tariff Monastir: TOTAL = tariff columns: cells give 1520553, printed 1520543 (difference -10)
  - sgt1923 oliviers_tariff Zaghouan: TOTAL = tariff columns: cells give 84219, printed 82972 (difference -1247)
  - sgt1923 oliviers_tariff Majeur: TOTAL = tariff columns: cells give 1638, printed 1938 (difference 300)
  - sgt1923 oliviers_tariff Kairouan: TOTAL = tariff columns: cells give 15115, printed 15415 (difference 300)
  - sgt1923 oliviers_tariff Totaux: TOTAL = tariff columns: cells give 8111962, printed 9043502 (difference 931540)
  - sgt1924 oliviers_tariff Monastir: TOTAL = tariff columns: cells give 1520575, printed 1520557 (difference -18)
  - sgt1924 oliviers_tariff Zaghouan: TOTAL = tariff columns: cells give 84255, printed 83008 (difference -1247)
  - sgt1924 oliviers_tariff Ouled-Aoun: TOTAL = tariff columns: cells give 27031, printed 23031 (difference -4000)
  - sgt1924 oliviers_tariff Totaux: TOTAL = tariff columns: cells give 9118767, printed 9117520 (difference -1247)
  - sgt1925 oliviers_tariff 2me Région (Tunis) ; Zaghouan ; Zaghouan: TOTAL = tariff columns: cells give 82998, printed 83008 (difference 10)
  - sgt1925 oliviers_tariff 3me Région (Le Kef) ; Le Kef ; Le Kef: TOTAL = tariff columns: cells give 29996, printed 29987 (difference -9)
  - sgt1925 oliviers_tariff 3me Région (Le Kef) ; Medjez-el-Bab ; Medjez-el-Bab: TOTAL = tariff columns: cells give 34967, printed 36977 (difference 2010)
  - sgt1925 oliviers_tariff 4me Région (Sousse) ; Sousse ; Sousse: TOTAL = tariff columns: cells give 1378984, printed 1378974 (difference -10)
  - sgt1925 oliviers_tariff 4me Région (Sousse) ; Kairouan ; Kairouan: TOTAL = tariff columns: cells give 15109, printed 15115 (difference 6)
  - sgt1925 oliviers_tariff 4me Région (Sousse) ; Thala ; Fraichiches: TOTAL = tariff columns: cells give 2811, printed 2754 (difference -57)
  - sgt1925 oliviers_tariff 4me Région (Sousse) ; Thala ; Madjeurs: TOTAL = tariff columns: cells give 1878, printed 1938 (difference 60)
  - sgt1925 oliviers_tariff 5me Région (Sfax) ; Tozeur ; Djerid: TOTAL = tariff columns: cells give 21521, printed 21481 (difference -40)
  - sgt1925 oliviers_tariff Territoires militaires du Sud ;  ; Ouerghema: TOTAL = tariff columns: cells give 149220, printed 149210 (difference -10)
  - sgt1925 oliviers_tariff Totaux: TOTAL = tariff columns: cells give 9102697, printed 9103897 (difference 1200)
  - sgt1926 oliviers_tariff 3me Région (Le Kef) ; Medjez-el-Bab ; Medjez-el-Bab: TOTAL = tariff columns: cells give 34967, printed 36967 (difference 2000)
  - sgt1927 oliviers_tariff 3me Région (Le Kef) ; Téboursouk ; Téboursouk: TOTAL = tariff columns: cells give 53387, printed 53487 (difference 100)
  - sgt1929 oliviers_tariff 1re Région (Bizerte) ; Souk-el-Arba ; Souk-el-Khemis: TOTAL = tariff columns: cells give 4657, printed 4656 (difference -1)
  - sgt1930 oliviers_tariff 1re Région (Bizerte) ; Bizerte ; Bizerte: TOTAL = tariff columns: cells give 429239, printed 429234 (difference -5)
  - sgt1930 oliviers_tariff 2me Région (Tunis) ; Grombalia ; Cap-Bon - Nabeul: TOTAL = tariff columns: cells give 404739, printed 404738 (difference -1)
  - sgt1922 oliviers_tariff Totaux: TOTAL = a) 20 ans imposables: cells give 9094191, printed 9094192 (difference 1)
  - sgt1923 oliviers_tariff Kairouan: TOTAL = a) 20 ans imposables: cells give 15115, printed 15415 (difference 300)
  - sgt1925 oliviers_tariff 2me Région (Tunis) ; Grombalia ; Cap-Bon - Nabeul: TOTAL = a) 20 ans imposables: cells give 337466, printed 377466 (difference 40000)
  - sgt1925 oliviers_tariff 3me Région (Le Kef) ; Le Kef ; Le Kef: TOTAL = a) 20 ans imposables: cells give 29996, printed 29987 (difference -9)
  - sgt1925 oliviers_tariff 3me Région (Le Kef) ; Medjez-el-Bab ; Medjez-el-Bab: TOTAL = a) 20 ans imposables: cells give 36967, printed 36977 (difference 10)
  - sgt1927 oliviers_tariff 5me Région (Sfax) ; Tozeur ; Djerid: TOTAL = a) 20 ans imposables: cells give 21411, printed 21481 (difference 70)
  - sgt1929 oliviers_tariff 1re Région (Bizerte) ; Souk-el-Arba ; Souk-el-Khemis: TOTAL = a) 20 ans imposables: cells give 4657, printed 4656 (difference -1)

- Flagged cells: derived_from_totals: 1, row_realigned: 23, total_mismatch: 14.

  - sgt1922 p.195 Monastir / 0.30 = 441916 (total_mismatch)
  - sgt1922 p.194 Souk-el-Arba / 0.25 = 285 (derived_from_totals)
  - sgt1923 p.206 Fraichiches / 0.05 = 0 (row_realigned)
  - sgt1923 p.206 Fraichiches / 0.10 = 0 (row_realigned)
  - sgt1923 p.206 Fraichiches / 0.15 = 7 (row_realigned)
  - sgt1923 p.206 Fraichiches / 0.20 = 0 (row_realigned)
  - sgt1923 p.207 Fraichiches / 0.25 = 0 (row_realigned)
  - sgt1923 p.207 Fraichiches / 0.30 = 236 (row_realigned)
  - sgt1923 p.207 Fraichiches / 0.40 = 0 (row_realigned)
  - sgt1923 p.207 Fraichiches / 0.50 = 1158 (row_realigned)
  - sgt1923 p.207 Fraichiches / 0.75 = 1359 (row_realigned)
  - sgt1923 p.207 Fraichiches / 1.00 = 0 (row_realigned)
  - sgt1923 p.207 Fraichiches / former_tithe_proportional = 0 (row_realigned)
  - sgt1923 p.206 Majeur / 0.05 = 0 (row_realigned)
  - sgt1923 p.206 Majeur / 0.10 = 0 (row_realigned)
  - sgt1923 p.206 Majeur / 0.15 = 0 (row_realigned)
  - sgt1923 p.206 Majeur / 0.20 = 0 (row_realigned)
  - sgt1923 p.207 Majeur / 0.25 = 0 (row_realigned)
  - sgt1923 p.207 Majeur / 0.30 = 0 (row_realigned)
  - sgt1923 p.207 Majeur / 0.40 = 0 (row_realigned)
  - sgt1923 p.207 Majeur / 0.50 = 528 (row_realigned)
  - sgt1923 p.207 Majeur / 0.75 = 1110 (total_mismatch)
  - sgt1923 p.207 Majeur / 1.00 = 0 (row_realigned)
  - sgt1923 p.207 Majeur / former_tithe_proportional = 0 (row_realigned)
  - sgt1924 p.214 Monastir / 0.20 = 123275 (total_mismatch)
  - sgt1924 p.215 Ouled-Aoun / 0.25 = 6940 (total_mismatch)
  - sgt1925 p.251 Medjez-el-Bab / 0.75 = 1729 (total_mismatch)
  - sgt1925 p.251 Sousse / 0.25 = 26443 (total_mismatch)
  - sgt1925 p.251 Kairouan / 0.20 = 252 (total_mismatch)
  - sgt1925 p.251 Fraichiches / 0.75 = 1410 (total_mismatch)
  - sgt1925 p.251 Madjeurs / 0.75 = 1353 (total_mismatch)
  - sgt1925 p.250 Djerid / 0.15 = 2888 (total_mismatch)
  - sgt1926 p.227 Medjez-el-Bab / 0.75 = 1729 (total_mismatch)
  - sgt1926 p.226 Fraichiches / 0.15 = 0 (row_realigned)
  - sgt1926 p.226 Madjeurs / 0.15 = 7 (row_realigned)
  - sgt1927 p.224 Téboursouk / 0.10 = 1079 (total_mismatch)
  - sgt1930 p.227 Bizerte / former_tithe_proportional = 429239 (total_mismatch)
  - sgt1930 p.227 Cap-Bon - Nabeul / 0.75 = 91643 (total_mismatch)

## Image versus OCR

- Read cell by cell on native-resolution crops of the page images (strips of rows, gutter columns on both views of the spread, every failing check re-read zoomed): sgt1922 f218, sgt1922 f219, sgt1923 f708, sgt1923 f709, sgt1924 f1204, sgt1924 f1205, sgt1925 f274, sgt1925 f275, sgt1926 f790, sgt1926 f791, sgt1927 f252, sgt1927 f253, sgt1928 f776, sgt1928 f777, sgt1929 f254, sgt1929 f255, sgt1930 f788, sgt1930 f789.
- The Gallica OCR was not used (no cell is flagged `ocr_corrected`).

Survey of the canoun tables in every edition: `finance_canoun_survey.md`.
