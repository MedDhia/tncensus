# Profession of naturalised men, 1922-1930 (table c)

Source: *Statistique générale de la Tunisie*, Régence de Tunis (annual). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR). Editions and views: see `EDITIONS.md`.

Table c) profession part, editions 1922-1930: 81 rows in nine broad groups (army;
agriculture; commerce and industry; employees of commerce or administration; café keepers
and drink sellers; sea fishing; owners and rentiers; liberal professions; other). The 1930
edition replaces café keepers with *employés et ouvriers d'industrie*. From 1935 the
table lists individual trades instead; see `naturalisations_profession_trades.csv`.

## Validation

8 of 9 printed-total checks pass. Failing checks (each re-read on the image at full resolution; printed values kept):

- sgt1928 c_prof total: computed 955 != printed 855

Common columns: `census` (source edition, e.g. `sgt1930`), `gallica_ark` (volume ark), `table_id`, `source_page` (printed page), `gallica_view`, `value`, `flag` (empty, `ocr_corrected`, `illegible`, `total_mismatch`, `derived_from_totals`, `not_applicable`, `reprint_corrected`; see `data-raw/colonial_census/SPEC.md`). A printed `»` is stored as 0. Printed totals are not stored; they were used for validation.
