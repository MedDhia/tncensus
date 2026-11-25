# 1936 census: European and indigenous population of the towns

**Population européenne et indigène des cinq plus grandes villes**, and **... des villes comptant
1° plus de 10.000 habitants, 2° de 5.000 à 10.000 habitants**
*Europeans by nationality, Muslims and Jews, in the five largest towns and in every town of more
than 5,000 inhabitants* (census of 1936).

Source: *Statistique générale de la Tunisie*, edition 1936 (`sgt1936`), Gallica ark `bpt6k91056547`,
printed page 6, view 17. Source gallica.bnf.fr / Ministère des Affaires étrangères.
Transcription: `transcribed/cens1936_towns_sgt1936.txt`.

One row per printed cell: town x (6 European nationalities, Muslims, Jews). `table_part` says which
of the three printed tables the row comes from; the five largest towns are printed twice (in the
first table and at the head of the list of towns over 10,000), and both printings are kept.
`controle_civil` is the "ressort du contrôle civil" as printed (empty for the five-largest table,
which has no such column, filled with the town's contrôle for convenience). `value` = persons.
Printed European, indigenous and grand totals are not stored.

## Validation

102 checks (European total, indigenous = Muslims + Jews, grand total, for every town); 4 fail.
five Bizerte european total; over_10000 Bizerte european total; over_10000 M'Saken grand total; 5000_10000 Menzel-Temim grand total


## Misprints and reprints

Compared visually, every cell, with the reprint in sgt1939 (`bpt6k9105739w`, view 12).

- Kairouan (five-largest table): sgt1936 prints Italians 7 and Maltese 171 (swapped); the list of
  towns over 10,000 and the sgt1939 reprint print Italians 171 and Maltese 7, used here
  (`reprint_corrected`).
- Zarzis Muslims: sgt1936 prints 7.244, sgt1939 prints 7.224, which the printed indigenous (7.484)
  and grand (7.641) totals require; 7.224 used (`reprint_corrected`).
- Bizerte European total printed 8.661 (Sfax's figure) in both sgt1936 tables; the cells sum to
  11.257, which sgt1939 prints in both tables. The five-largest grand total is corrected to 28.468 in
  sgt1939, but the list keeps 25.872 in both editions. Totals are not stored; the cells are the same
  in both editions.
- Totals misprinted in both editions (not stored): M'Saken grand total 20.088 for 20.089;
  Menzel-Temim grand total 8.532 for 7.832.
- Gafsa and Mahdia "other Europeans" are smudged; read as 3 and 1, as the printed European totals
  require, in both editions.
