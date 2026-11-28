# 1936 census: population by contrôle civil, group and nationality

**Répartition, par circonscriptions de Contrôles civils, de la population civile, européenne et
indigène, d'après le recensement de 1936**
*Civilian population by contrôle civil: Muslims and Jews by nationality, Europeans by nationality.*

Source: *Statistique générale de la Tunisie*, edition 1936 (`sgt1936`), Gallica ark
`bpt6k91056547`, printed pages 2-3, views 13-14. Source gallica.bnf.fr / Ministère des Affaires
étrangères. Transcription: `transcribed/cens1936_controle_sgt1936.txt`. Reprinted in sgt1939
(`bpt6k9105739w`, views 8-9, "d'après le dernier recensement (1936)").

One row per printed cell: 20 contrôles civils x (7 Muslim + 6 Jewish + 6 European nationalities).
`value` = persons. Printed totals are not stored. The Jewish table has no "Soudanais" column.

The printed column headings are misplaced: the Jewish total is printed under "TOTAUX de la
population tunisienne" and the indigenous total (Muslims + Jews) under "TOTAUX de la population
israélite".

## Validation

129 checks (every group total, indigenous, grand total, every column against TOTAUX); 13 fail,
all printing errors present identically in sgt1936 and sgt1939:

- three data cells, each where a row and its column are off by the same amount, flagged
  `total_mismatch` (printed values kept): Bizerte Maltese printed 305 (the comparison table prints
  306, which makes the row and the Maltese column add up); Territoires militaires French printed 595
  (comparison table 596); Souk-el-Arba Moroccan Muslims printed 79 (row and column imply 78);
- printed totals only (not stored): Sousse Muslim total printed 332.192 for 322.192 (the printed
  indigenous total, 327.182, uses 322.192); TOTAUX Tripolitanian Muslims printed 23.807 for 23.907
  (the printed Muslim grand total uses 23.907); Maktar grand total printed 69.278 for 69.273.

Failing checks:   Bizerte european total: 25582 != printed 25583;   Maktar grand: 69273 != printed 69278;   Souk-el-Arba muslim total: 93940 != printed 93939;   Sousse muslim total: 322192 != printed 332192;   Sousse indigenous: 337182 != printed 327182;   Territoires militaires european total: 754 != printed 755;   TOTAUX muslim total: 2335523 != printed 2335623;   column 0.2: 4447 != printed 4446;   column 0.5: 23907 != printed 23807;   column 0.7: 2345623 != printed 2335623;   column 3.0: 108067 != printed 108068;   column 3.2: 7278 != printed 7279;   column 4.0: 2608318 != printed 2608313.

## Reprint

Every row compared with sgt1939 (OCR row matching, then image crops of each row with a difference):
identical, except sgt1939 prints Tozeur French as 78 (sgt1936: 178; the Tozeur European total, 186,
requires 178; 178 kept).
