# Civil status, residence and birthplace of the naturalised (table b)

Source: *Statistique générale de la Tunisie*, Régence de Tunis (annual). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR). Editions and views: see `EDITIONS.md`.

Table b) *Renseignements d'état civil sur les naturalisés*, 156 rows; editions 1922-1930,
1935, 1936, 1939 (`year` = edition year). `section`:

- `civil_status`: men by marital status (single; married to a wife of French origin;
  married to a wife of foreign origin; widowed; divorced) and women by marital status.
- `residence_in_tunisia` (1922-1930): naturalised men by length of residence in Tunisia or
  French territory (more / less than 10 years) and civilian / military.
- `birthplace` (1935-1939): men and women born in French territory / abroad.

Misprints confirmed on the scans (values kept, flagged `total_mismatch` where a total fails):

- sgt1922 (b_men): the men's total 128 includes the adult son (122 + 5 + 1); table c gives 127
- sgt1924 (b_men): cells sum to 433, printed total 434
- sgt1928 (c_prof): professions sum to 955, printed total 855 (Employés 412 likely 312)
- sgt1929 (d): nationalities sum to 787, printed total 786

## Validation

38 of 39 printed-total checks pass. Failing checks (each re-read on the image at full resolution; printed values kept):

- sgt1924 b_men total: computed 433 != printed 434

Common columns: `census` (source edition, e.g. `sgt1930`), `gallica_ark` (volume ark), `table_id`, `source_page` (printed page), `gallica_view`, `value`, `flag` (empty, `ocr_corrected`, `illegible`, `total_mismatch`, `derived_from_totals`, `not_applicable`, `reprint_corrected`; see `data-raw/colonial_census/SPEC.md`). A printed `»` is stored as 0. Printed totals are not stored; they were used for validation.
