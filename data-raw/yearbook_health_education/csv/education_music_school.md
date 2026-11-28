# École de musique : répartition des élèves dans les différentes classes

*School of music: pupils by class and nationality.*

Source: *Statistique générale de la Tunisie*, chapter "Instruction publique et beaux-arts" (VII; VI in sgt1936 and sgt1939), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1922 (`bpt6k9105649x`): p. 93, f117; sgt1923 (`bpt6k9105649x`): p. 99, f601; sgt1924 (`bpt6k9105649x`): p. 101, f1091; sgt1925 (`bpt6k9105650k`): p. 103, f127; sgt1926 (`bpt6k9105650k`): p. 113, f677; sgt1927 (`bpt6k91056510`): p. 111, f139; sgt1928 (`bpt6k91056510`): p. 111, f663; sgt1929 (`bpt6k9105652d`): p. 113, f141; sgt1930 (`bpt6k9105652d`): p. 117, f675; sgt1935 (`bpt6k9105653t`): p. 83, f103; sgt1936 (`bpt6k91056547`): p. 61, f72; sgt1939 (`bpt6k9105739w`): p. 63, f69.

Transcriptions: `../transcribed/education_sum_<edition>.txt`; rebuild with `python3 data-raw/yearbook_health_education/extract_education_summary.py build`. Per-check output: `education_summary_validation.json`.

Rows: 672. Years: 1922–1939 (12 years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939).

Printed once per edition, for the edition's own year; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number; pages without a printed number are inferred from the next page. For the two-page spreads (population, primary-education and first-degree totals) the boys' block is given the left-hand page and the girls' block and total columns the right-hand page (the printed fold falls near the boys' TOTAUX, so one or two boys' columns may in fact sit on the right-hand page)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (31 December of that year for pupils; the school year's examinations)
- `class`: English code
- `class_fr`: class as printed
- `sex`: `male`, `female`; `total` where the cell is not split by sex (empty in the comparative table for items that are not pupils)
- `sex_fr`: column heading as printed (Aspirants / Aspirantes in the examination table, Garçons / Filles elsewhere)
- `nationality`: `french`, `muslim`, `jewish`, `italian`, `maltese`, `other` (Divers); `total` where not split
- `nationality_fr`: column heading as printed (masculine for boys, feminine for girls)
- `value`: count (integer); printed » = 0; empty where the cell is not printed (`not_applicable`)
- `flag`: empty, or `ocr_corrected`, `derived_from_totals`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (TOTAUX, Totaux généraux, subtotals, A reporter) are not stored unless stated; they were used for validation.

École de musique: pupils enrolled (`enrolled`) and pupils in each class, by nationality (Français, Musulmans, Israélites, Italiens, Maltais, Divers). Not split by sex (`sex` = `total`). A pupil can follow several classes, so the classes do not add up to the enrolment. sgt1939 prints no enrolment line but a column-total line (57), which equals the sum of its classes (check only). sgt1929 cello class: the cells (3 + 2 + 1) give 6 against a printed TOTAUX 16 (kept).

## Validation

- Checks against printed totals: 119; passed: 118; failed: 1.

Failed checks (every cell involved was re-read on a native-resolution crop; the printed figures are as transcribed; see the commentary above):

  - sgt1929 cello: nationalities vs TOTAUX: cells give 6, printed 16

- Flagged cells: none.
