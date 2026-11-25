# Enseignement professionnel de la population indigène (apprentissage)

*Vocational education of the indigenous population: apprentices by school.*

Source: *Statistique générale de la Tunisie*, chapter "Instruction publique et beaux-arts" (VII; VI in sgt1936 and sgt1939), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1922 (`bpt6k9105649x`): p. 124, f148; sgt1923 (`bpt6k9105649x`): p. 130, f632; sgt1924 (`bpt6k9105649x`): p. 132, f1122; sgt1925 (`bpt6k9105650k`): p. 134, f158; sgt1926 (`bpt6k9105650k`): p. 144, f708; sgt1927 (`bpt6k91056510`): p. 142, f170; sgt1928 (`bpt6k91056510`): p. 142, f694; sgt1929 (`bpt6k9105652d`): p. 144, f172; sgt1930 (`bpt6k9105652d`): p. 148, f706; sgt1935 (`bpt6k9105653t`): p. 84, f104; sgt1936 (`bpt6k91056547`): p. 62, f73; sgt1939 (`bpt6k9105739w`): p. 66, f72.

Transcriptions: `../transcribed/education_sum_<edition>.txt`; rebuild with `python3 data-raw/yearbook_health_education/extract_education_summary.py build`. Per-check output: `education_summary_validation.json`.

Rows: 255. Years: 1922–1939 (12 years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939).

Printed once per edition, for the edition's own year; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number; pages without a printed number are inferred from the next page. For the two-page spreads (population, primary-education and first-degree totals) the boys' block is given the left-hand page and the girls' block and total columns the right-hand page (the printed fold falls near the boys' TOTAUX, so one or two boys' columns may in fact sit on the right-hand page)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (31 December of that year for pupils; the school year's examinations)
- `locality`: locality as printed
- `school_fr`: school as printed
- `value`: count (integer); printed » = 0; empty where the cell is not printed (`not_applicable`)
- `flag`: empty, or `ocr_corrected`, `derived_from_totals`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (TOTAUX, Totaux généraux, subtotals, A reporter) are not stored unless stated; they were used for validation.

"Enseignement professionnel de la population indigène" (from sgt1935 "Enseignement professionnel élémentaire"): number of apprentices by school. In sgt1922–sgt1929 the schools of Tunis are listed one by one under a bracket total (checked, not stored); in sgt1930 only the bracket total is printed (one row, "Tunis (ensemble des écoles, non détaillé)"); from sgt1935 the list is by school or section. "A reporter" / "Report" and Total lines are checks only. A school printed » is stored as 0 (sgt1939: two schools closed since the beginning of the war).

Failed check: sgt1924 Tunis schools sum to 233 against the printed bracket 224; the carried total (383) and the general total (631) follow 224 (all cells re-read). sgt1929 Tébourba is blank on the page; 3 closes the printed total 631 (`derived_from_totals`).

## Footnotes printed under the table

- * Fermée depuis le début de la guerre. (sgt1939)

## Validation

- Checks against printed totals: 32; passed: 31; failed: 1.

Failed checks (every cell involved was re-read on a native-resolution crop; the printed figures are as transcribed; see the commentary above):

  - sgt1924 Tunis schools vs bracket total: cells give 233, printed 224

- Flagged cells: derived_from_totals: 1.

  - sgt1929 1929 Tébourba = 3 (derived_from_totals)
