# Naturalisations granted, by category (table a)

Source: *Statistique générale de la Tunisie*, Régence de Tunis (annual). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR). Editions and views: see `EDITIONS.md`.

Table a) *Naturalisations individuelles*: naturalisations granted in the edition year,
by category. 98 rows; years 1922-1930, 1935, 1936, 1939 (one edition each; `year` is
the edition year).

Columns: `sex`, `item` (English code), `item_fr` (printed heading), `value` = persons.

The categories change over time, so not every `item` exists every year:

- 1922-1929: men (civilians / soldiers), women naturalised, adult children naturalised
  with their parents (sons / daughters), women reinstated, minor children naturalised
  *définitivement* (and, in 1922-1923, *conditionnellement*) by sex.
- 1930-1936: minors are no longer split definitive/conditional (`minor_boys`, `minor_girls`).
- 1939: men naturalised / reinstated (no civilian/military split); no adult children.

In 1922-1929 the printed TOTAL excludes the women reinstated, who appear only in the
TOTAL GÉNÉRAL; from 1930 the adult total includes them. The grand totals equal the
annual totals of table e (e.g. 1925: 3.298; 1930: 1.609; 1935: 668).

## Validation

36 of 36 printed-total checks pass.

Common columns: `census` (source edition, e.g. `sgt1930`), `gallica_ark` (volume ark), `table_id`, `source_page` (printed page), `gallica_view`, `value`, `flag` (empty, `ocr_corrected`, `illegible`, `total_mismatch`, `derived_from_totals`, `not_applicable`, `reprint_corrected`; see `data-raw/colonial_census/SPEC.md`). A printed `»` is stored as 0. Printed totals are not stored; they were used for validation.
