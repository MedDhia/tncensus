# Total général des élèves de l'enseignement public et privé au 31 décembre

*Total pupils, public and private education, at 31 December.*

Source: *Statistique générale de la Tunisie*, chapter "Instruction publique et beaux-arts" (VII; VI in sgt1936 and sgt1939), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1922 (`bpt6k9105649x`): p. 90, f114; sgt1923 (`bpt6k9105649x`): p. 96, f598; sgt1924 (`bpt6k9105649x`): p. 98, f1088; sgt1925 (`bpt6k9105650k`): p. 100, f124; sgt1926 (`bpt6k9105650k`): p. 110, f674; sgt1927 (`bpt6k91056510`): p. 108, f136; sgt1928 (`bpt6k91056510`): p. 108, f660; sgt1929 (`bpt6k9105652d`): p. 110, f138; sgt1930 (`bpt6k9105652d`): p. 114, f672; sgt1935 (`bpt6k9105653t`): p. 80, f100; sgt1936 (`bpt6k91056547`): p. 57, f69; sgt1939 (`bpt6k9105739w`): p. 60, f66.

Transcriptions: `../transcribed/education_sum_<edition>.txt`; rebuild with `python3 data-raw/yearbook_health_education/extract_education_summary.py build`. Per-check output: `education_summary_validation.json`.

Rows: 12. Years: 1922–1939 (12 years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939).

Printed once per edition, for the edition's own year; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number; pages without a printed number are inferred from the next page. For the two-page spreads (population, primary-education and first-degree totals) the boys' block is given the left-hand page and the girls' block and total columns the right-hand page (the printed fold falls near the boys' TOTAUX, so one or two boys' columns may in fact sit on the right-hand page)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (31 December of that year for pupils; the school year's examinations)
- `label_fr`: heading of the total page as printed
- `value`: count (integer); printed » = 0; empty where the cell is not printed (`not_applicable`)
- `flag`: empty, or `ocr_corrected`, `derived_from_totals`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (TOTAUX, Totaux généraux, subtotals, A reporter) are not stored unless stated; they were used for validation.

The chapter's opening page prints one figure: the total of pupils of public and private education at 31 December of the edition year. It equals the "Total général des élèves de l'enseignement public et de l'enseignement privé" of the comparative table, which includes the auditors of the adult courses, in sgt1922–sgt1936. In sgt1939 the total page prints 97.599, the total without the 677 adult auditors (= the population table's total général), while that edition's comparative table prints 98.276 with them; see the cross-checks.

## Validation

- Checks against printed totals: 0; passed: 0; failed: 0.

- Flagged cells: none.

## Cross-checks with other tables of the chapter

- 24 comparisons; equal: 22; different: 2.
  - sgt1939 total page vs tableau comparatif, total général 1939: cells give 98276, printed 97599
  - sgt1939 total page vs population table total général + adult auditors: cells give 98276, printed 97599
