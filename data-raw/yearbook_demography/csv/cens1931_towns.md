# 1931 census: European and indigenous population of the towns

**Population européenne et indigène des cinq plus grandes villes**, and **... des villes comptant
1° plus de 10.000 habitants, 2° de 5.000 à 10.000 habitants**
*Europeans by nationality, Muslims and Jews, in the five largest towns and in every town of more
than 5,000 inhabitants* (census of 1931).

Source: *Statistique générale de la Tunisie*, edition 1935 (`sgt1935`), Gallica ark `bpt6k9105653t`,
printed page 6, view 26. Source gallica.bnf.fr / Ministère des Affaires étrangères.
Transcription: `transcribed/cens1931_towns_sgt1935.txt`.

One row per printed cell: town x (6 European nationalities, Muslims, Jews). `table_part` says which
of the three printed tables the row comes from; the five largest towns are printed twice (in the
first table and at the head of the list of towns over 10,000), and both printings are kept.
`controle_civil` is the "ressort du contrôle civil" as printed (empty for the five-largest table,
which has no such column, filled with the town's contrôle for convenience). `value` = persons.
Printed European, indigenous and grand totals are not stored.

## Validation

102 checks (European total, indigenous = Muslims + Jews, grand total, for every town); 2 fail.
five Sfax european total; over_10000 Béja grand total


## Misprints and reprints

- Sfax French: printed 4.135 in the five-largest table and 4.435 in the list of towns over 10,000;
  the printed European total (8.177) requires 4.435. Both printings are kept as printed; the
  five-largest cell is flagged `total_mismatch`.
- Béja grand total printed 1.612 for 11.612 (a total, not stored).
- Not reprinted in another edition on Gallica.
