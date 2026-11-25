# 1931 census: population by contrôle civil, group and nationality

**Répartition, par circonscriptions de Contrôles civils, de la population civile, européenne et
indigène, d'après le recensement de 1931**
*Civilian population by contrôle civil: Europeans by nationality, Muslims and Jews by nationality.*

Source: *Statistique générale de la Tunisie*, edition 1935 (`sgt1935`), Gallica ark
`bpt6k9105653t`, printed pages 2-3, views 22-23. Source gallica.bnf.fr / Ministère des Affaires
étrangères. Transcription: `transcribed/cens1931_controle_sgt1935.txt`. Not reprinted in another
edition on Gallica.

One row per printed cell: 20 contrôles civils (the last is "Territoires militaires") x (6 European
nationalities + 7 Muslim nationalities + 6 Jewish nationalities). `population` is `european`,
`muslim` or `jewish`. `value` = persons. Printed totals (by group, indigenous, grand total, TOTAUX
row) are not stored.

The Muslim "Soudanais" column falls in the binding gutter between the two pages and is unreadable;
its 20 cells are derived as the printed Muslim total minus the other six nationalities (flag
`derived_from_totals`). The derived column sums to 445, as does the indigenous census volume.

## Validation

106 checks (every group total, indigenous = Muslim + Jewish, grand total, every column against the
TOTAUX row); 0 fail. 

Cross-check with the 1931 census volume (*Dénombrement de la population civile indigène*, Table I,
`data-raw/colonial_census/csv/ind1931_t1_controle_nationality.csv`): 260 Muslim and Jewish cells
compared, 0 differ. The national totals equal those of the census volume (2.159.151 Muslims,
56.248 Jews).
