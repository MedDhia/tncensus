# 1926 census: Europeans by instruction (1921 and 1926)

**g) Population européenne d'après l'instruction (recensements de 1921 et 1926)**
*European population by literacy, knowledge of French and of Arabic, 1926; with the 1921
distribution by instruction.*

Source: *Statistique générale de la Tunisie*, edition 1926 (`sgt1926`), Gallica ark
`bpt6k9105650k`, printed page 12, view 576. Source gallica.bnf.fr / Ministère des Affaires
étrangères. Transcription: `transcribed/cens1926_g_sgt1926.txt`.

One row per printed cell. `measure` is `count` (persons) or `pct_of_nationality` (percentage of the
nationality's 1926 total, as printed, with one decimal). `census_year` is 1926, except the two
columns "Répartition d'après l'instruction en 1921" (1921). The printed nationality totals (equal
to the 1926 census totals) and the TOTAUX row are not stored.

Footnote (translated): (1) the question [speaking French] does not apply to the French; those cells
are NA with flag `not_applicable`. Under the table: "the percentage is calculated on the total
of each nationality".

## Validation

42 checks (illiterate + literate = total; each percentage recomputed within 0.1; every column
against the TOTAUX row; the total against table e); 4 fail. maltese illiterate %: 50.8 != 55.1; TOTAL illiterate %: 34.7 != 34.5; TOTAL literate %: 65.3 != 65.8; TOTAL French-speaking %: 25.7 != 25.5

The Maltese illiterate share is printed 55,1 in all five editions; 4.268 / 8.396 gives 50,8 (and
50,8 + 49,1 = 99,9), so the cell is flagged `total_mismatch` (printed value kept). The three other
failures are the shares printed in the TOTAUX row (not stored), which do not match the printed
counts (34,5 / 65,8 / 25,5 printed; 34,7 / 65,3 / 25,7 recomputed).

## Reprints

Compared visually, every cell, with sgt1927 (view 40), sgt1928 (564), sgt1929 (40) and sgt1930
(570): identical.
