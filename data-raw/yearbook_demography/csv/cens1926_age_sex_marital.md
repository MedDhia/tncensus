# 1926 census: Europeans by age, sex and marital status

**e) Population européenne d'après l'âge, le sexe et l'état civil**
*European population by age group, sex and marital status, by nationality* (census of 1926).

Source: *Statistique générale de la Tunisie*, edition 1926 (`sgt1926`), Gallica ark
`bpt6k9105650k`, printed pages 7-9, views 571-573. Source gallica.bnf.fr / Ministère des
Affaires étrangères. Transcription: `transcribed/cens1926_e_sgt1926.txt`.

One row per printed cell: 6 nationalities x 13 age groups x 4 marital statuses x 2 sexes.
`value` = persons. Printed row totals, "Totaux par sexe", "Totaux" and "Totaux généraux" are not
stored; they were used for validation.

## Validation

167 checks (every row total, every column total per nationality, the Totaux by marital status, the
nationality totals and the Totaux généraux); 10 fail. Every failure is a misprint confirmed on all
five printings and flagged `total_mismatch` (printed value kept):

- french De 0 à 4 ans, column 1 (single female): `total_mismatch`. printed 3.718 in sgt1926-sgt1930; row total and column total imply 3.778
- french 60 ans et au-dessus, column 2 (married male): `total_mismatch`. printed 2.479 in all five editions; row and column totals imply 1.479
- spanish 5 à 9 ans, column 1 (single female): `total_mismatch`. printed 25 in all editions; row and column totals imply 24
- other_european 60 ans et au-dessus, column 5 (widowed female): `total_mismatch`. printed 41 in all five editions; row and column totals imply 44
- spanish 60 ans et au-dessus, column 2 (married male): `reprint_corrected`. printed 94 in sgt1926-sgt1929; sgt1930 prints 14, which the row and column totals require

Failing checks:   french 0_4 row: cells 7678 != printed 7738;   french 60_plus row: cells 5317 != printed 4317;   french col 0 vs Totaux par sexe: cells 18318 != printed 18348;   french col 1 vs Totaux par sexe: cells 17629 != printed 17689;   french col 2 vs Totaux par sexe: cells 15834 != printed 14834;   french Totaux 0 = M+F: cells 36037 != printed 36007;   spanish 5_9 row: cells 50 != printed 49;   spanish col 1 vs Totaux par sexe: cells 136 != printed 135;   other_european 60_plus row: cells 229 != printed 232;   other_european col 5 vs Totaux par sexe: cells 101 != printed 104.

## Reprints

Every cell was compared with the reprints in sgt1927 (views 35-37), sgt1928 (559-561), sgt1929
(35-37) and sgt1930 (565-567): OCR row matching followed by image crops of every row where the OCR
differed (30 rows), and a visual read of every page of sgt1930.

- sgt1927, sgt1928, sgt1929: identical to sgt1926 in every cell (all OCR differences were OCR errors).
- sgt1930: identical except (1) Spanish 60 and over, married men: 14 (sgt1926-29 print 94; the row
  and column totals require 14), used here and flagged `reprint_corrected`; (2) Greek 40-44 single
  men printed 7 (8 elsewhere; the row total requires 8, kept 8); (3) the Italian married-women column
  is garbled in sgt1930 (11 of 13 cells differ and no longer add up to the printed row totals); the
  sgt1926 column, which adds up, is kept.
- The other misprints listed above appear identically in all five editions.
