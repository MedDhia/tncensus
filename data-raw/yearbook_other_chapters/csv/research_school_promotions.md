# École coloniale d'agriculture. b) Promotions

*Colonial school of agriculture: regular students and diplomas by promotion.*

Source: *Statistique générale de la Tunisie*, chapter *Institutions d'enseignement et de recherches*, editions sgt1935. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1935 (`bpt6k9105653t`): p. 140, f160.

Transcriptions: `../transcribed/research_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_research.py build`.

Rows: 165. Years: 1935.

Unit: students (count); value_type: count.

Selection (SPEC_ADDENDUM rule 4): each cell is stored once, from the latest edition printing it; every other printing of the same cell is compared below.

## Columns

- `census`: source edition (`sgt1922` ... `sgt1939`)
- `table_id`: section code of the transcription
- `gallica_ark`: Gallica volume ark
- `source_page`: printed page number
- `gallica_view`: Gallica view
- `year`: year of the figure (for a school year or season: the year it ends; for promotions and once-per-edition tables: the edition year)
- `promotion`: promotion number (1 = 1898-1900)
- `promotion_years`: years of the promotion as printed
- `measure`: what is counted
- `measure_fr`: column heading as printed
- `value`: printed figure (» = 0)
- `flag`: empty, or ocr_corrected / illegible / total_mismatch / derived_from_totals / not_applicable / reprint_corrected / row_realigned

Rule 4 by promotion: each promotion is stored from the latest edition printing it (`year` = that edition's year), so the figures of promotions still studying are those of the latest printing. Printed '(2) promotions en cours d'études' in place of a figure: NA, not_applicable.

Every failed check below was re-read on a zoomed native-resolution crop: they are printed inconsistencies (printed values kept). 

Survey of the whole chapter in every edition: `research_survey.md`.

## Validation

- Checks against printed totals and identities: 24; passed: 18; failed: 6.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.251 (f275) school_promotions dipl_school: lines vs Totaux: cells give 173, printed 143 (difference -30)
  - sgt1925 p.312 (f336) school_promotions dipl_eng: lines vs Totaux: cells give 457, printed 447 (difference -10)
  - sgt1925 p.312 (f336) school_promotions dipl_school: lines vs Totaux: cells give 229, printed 199 (difference -30)
  - sgt1927 p.281 (f309) school_promotions year1: lines vs Totaux: cells give 1023, printed 1028 (difference 5)
  - sgt1927 p.281 (f309) school_promotions year2: lines vs Totaux: cells give 829, printed 229 (difference -600)
  - sgt1935 p.140 (f160) school_promotions dipl_school: lines vs Totaux: cells give 295, printed 268 (difference -27)

- Overlapping printings: 1054 cell comparisons with other editions printing the same cell; 72 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1 / diploma_engineer | sgt1922 | 22 | sgt1935 | 24 |
| 1 / diploma_engineer | sgt1923 | 22 | sgt1935 | 24 |
| 1 / diploma_engineer | sgt1924 | 22 | sgt1935 | 24 |
| 1 / diploma_engineer | sgt1925 | 22 | sgt1935 | 24 |
| 1 / diploma_engineer | sgt1926 | 22 | sgt1935 | 24 |
| 1 / diploma_engineer | sgt1927 | 22 | sgt1935 | 24 |
| 10 / regular_students_year1 | sgt1922 | 15 | sgt1935 | 17 |
| 12 / diploma_engineer | sgt1922 | 28 | sgt1935 | 29 |
| 12 / diploma_engineer | sgt1923 | 28 | sgt1935 | 29 |
| 12 / diploma_engineer | sgt1924 | 28 | sgt1935 | 29 |
| 12 / diploma_engineer | sgt1925 | 28 | sgt1935 | 29 |
| 12 / diploma_engineer | sgt1926 | 28 | sgt1935 | 29 |
| 12 / diploma_engineer | sgt1927 | 28 | sgt1935 | 29 |
| 13 / regular_students_year1 | sgt1923 | 31 | sgt1935 | 32 |
| 13 / regular_students_year1 | sgt1924 | 31 | sgt1935 | 32 |
| 13 / regular_students_year1 | sgt1925 | 31 | sgt1935 | 32 |
| 13 / regular_students_year1 | sgt1926 | 31 | sgt1935 | 32 |
| 13 / regular_students_year1 | sgt1927 | 31 | sgt1935 | 32 |
| 13 / regular_students_year1 | sgt1928 | 31 | sgt1935 | 32 |
| 13 / regular_students_year1 | sgt1929 | 31 | sgt1935 | 32 |
| 13 / diploma_school | sgt1922 | 43 | sgt1935 | 13 |
| 13 / diploma_school | sgt1923 | 43 | sgt1935 | 13 |
| 13 / diploma_school | sgt1924 | 43 | sgt1935 | 13 |
| 13 / diploma_school | sgt1925 | 43 | sgt1935 | 13 |
| 13 / diploma_school | sgt1926 | 43 | sgt1935 | 13 |
| 13 / diploma_school | sgt1927 | 43 | sgt1935 | 13 |
| 17 / diploma_engineer | sgt1922 | 31 | sgt1935 | 32 |
| 17 / diploma_engineer | sgt1923 | 31 | sgt1935 | 32 |
| 17 / diploma_engineer | sgt1924 | 31 | sgt1935 | 32 |
| 17 / diploma_engineer | sgt1925 | 31 | sgt1935 | 32 |
| 17 / diploma_engineer | sgt1926 | 31 | sgt1935 | 32 |
| 17 / diploma_engineer | sgt1927 | 31 | sgt1935 | 32 |
| 17 / diploma_school | sgt1922 | 16 | sgt1935 | 41 |
| 17 / diploma_school | sgt1923 | 16 | sgt1935 | 41 |
| 17 / diploma_school | sgt1924 | 16 | sgt1935 | 41 |
| 17 / diploma_school | sgt1925 | 16 | sgt1935 | 41 |
| 17 / diploma_school | sgt1926 | 16 | sgt1935 | 41 |
| 17 / diploma_school | sgt1927 | 16 | sgt1935 | 41 |
| 17 / diploma_school | sgt1928 | 14 | sgt1935 | 41 |
| 17 / diploma_school | sgt1929 | 14 | sgt1935 | 41 |
| 17 / diploma_school | sgt1930 | 14 | sgt1935 | 41 |
| 18 / diploma_engineer | sgt1922 | 35 | sgt1935 | 36 |
| 18 / diploma_engineer | sgt1923 | 35 | sgt1935 | 36 |
| 18 / diploma_engineer | sgt1924 | 35 | sgt1935 | 36 |
| 18 / diploma_engineer | sgt1925 | 35 | sgt1935 | 36 |
| 18 / diploma_engineer | sgt1926 | 35 | sgt1935 | 36 |
| 18 / diploma_engineer | sgt1927 | 35 | sgt1935 | 36 |
| 19 / diploma_school | sgt1922 | 0 | sgt1935 | 16 |
| 20 / diploma_engineer | sgt1922 | 0 | sgt1935 | 31 |
| 20 / diploma_engineer | sgt1923 | 0 | sgt1935 | 31 |
| 20 / diploma_school | sgt1922 | 0 | sgt1935 | 11 |
| 20 / diploma_school | sgt1923 | 0 | sgt1935 | 11 |
| 20 / diploma_school | sgt1924 | 12 | sgt1935 | 11 |
| 20 / diploma_school | sgt1925 | 12 | sgt1935 | 11 |
| 20 / diploma_school | sgt1926 | 12 | sgt1935 | 11 |
| 20 / diploma_school | sgt1927 | 12 | sgt1935 | 11 |
| 22 / regular_students_year2 | sgt1924 | 54 | sgt1935 | 49 |
| 22 / diploma_engineer | sgt1924 | 0 | sgt1935 | 40 |
| 22 / diploma_school | sgt1924 | 0 | sgt1935 | 8 |
| 23 / regular_students_year2 | sgt1925 | 0 | sgt1935 | 47 |
| 23 / diploma_engineer | sgt1925 | 0 | sgt1935 | 33 |
| 23 / diploma_school | sgt1925 | 0 | sgt1935 | 12 |
| 23 / diploma_school | sgt1926 | 11 | sgt1935 | 12 |
| 23 / diploma_school | sgt1927 | 11 | sgt1935 | 12 |
| 23 / certificate_of_studies | sgt1925 | 0 | sgt1935 | 1 |
| 24 / regular_students_year2 | sgt1925 | 47 | sgt1935 | 38 |
| 24 / regular_students_year2 | sgt1926 | 0 | sgt1935 | 38 |
| 24 / diploma_engineer | sgt1925 | 0 | sgt1935 | 27 |
| 24 / diploma_school | sgt1925 | 0 | sgt1935 | 10 |
| 24 / certificate_of_studies | sgt1925 | 0 | sgt1935 | 1 |
| 27 / regular_students_year2 | sgt1929 | 0 | sgt1935 | 37 |
| 28 / regular_students_year2 | sgt1930 | 0 | sgt1935 | 43 |

- Flagged cells: not_applicable: 2, total_mismatch: 1.

  - sgt1935 p.140 1935 17 / 1919-1921 / diploma_school = 41 (total_mismatch)
  - sgt1935 p.140 1935 30 / 1932-1934 / certificate_of_studies = NA (not_applicable)
  - sgt1935 p.140 1935 31 / 1933-1935 / certificate_of_studies = NA (not_applicable)

## Image versus OCR

- Read cell by cell on the page images (10 printings): sgt1922 f275, sgt1923 f766, sgt1924 f1270, sgt1925 f336, sgt1926 f847, sgt1927 f309, sgt1928 f837, sgt1929 f314, sgt1930 f851, sgt1935 f160.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
