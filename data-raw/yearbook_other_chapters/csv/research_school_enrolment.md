# École coloniale d'agriculture. c) Effectif par année scolaire

*Colonial school of agriculture: enrolment by school year (regular students in first and second year, auditors).*

Source: *Statistique générale de la Tunisie*, chapter *Institutions d'enseignement et de recherches*, editions sgt1935. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1935 (`bpt6k9105653t`): p. 141, f161.

Transcriptions: `../transcribed/research_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_research.py build`.

Rows: 99. Years: 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936.

Unit: students (count); value_type: count.

Selection (SPEC_ADDENDUM rule 4): each cell is stored once, from the latest edition printing it; every other printing of the same cell is compared below.

## Columns

- `census`: source edition (`sgt1922` ... `sgt1939`)
- `table_id`: section code of the transcription
- `gallica_ark`: Gallica volume ark
- `source_page`: printed page number
- `gallica_view`: Gallica view
- `year`: year of the figure (for a school year or season: the year it ends; for promotions and once-per-edition tables: the edition year)
- `school_year`: school year as printed
- `measure`: what is counted
- `measure_fr`: column heading as printed
- `value`: printed figure (» = 0)
- `flag`: empty, or ocr_corrected / illegible / total_mismatch / derived_from_totals / not_applicable / reprint_corrected / row_realigned

Row totals (Totaux column) and column totals are checks only.

Every failed check below was re-read on a zoomed native-resolution crop: they are printed inconsistencies (printed values kept). Auditeurs libres: the printed column total runs 9-10 short in sgt1923-sgt1927 (sgt1922 adds up; from sgt1923 the printed total grows by less than the new lines, and every edition carries the shortfall forward), and is 5 over in sgt1935; every auditor cell agrees with its printed row total, so the faulty figure is the printed column total (not stored). sgt1924 1re année total 977 for 877 and sgt1935 2e année total 1.061 for 1.069: printed column-total errors (cells agree with the row totals). The same 10-short auditor total is carried in sgt1928-sgt1930. sgt1930: 1924-1925 row total printed 116 for 124 (2e année 59 read on the crop; the 2e année column total 907 also leaves out 8). 

Survey of the whole chapter in every edition: `research_survey.md`.

## Validation

- Checks against printed totals and identities: 282; passed: 269; failed: 13.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1923 p.265 (f767) school_enrolment auditors: lines vs Totaux: cells give 159, printed 150 (difference -9)
  - sgt1924 p.281 (f1271) school_enrolment year1: lines vs Totaux: cells give 877, printed 977 (difference 100)
  - sgt1924 p.281 (f1271) school_enrolment auditors: lines vs Totaux: cells give 167, printed 157 (difference -10)
  - sgt1925 p.313 (f337) school_enrolment auditors: lines vs Totaux: cells give 187, printed 177 (difference -10)
  - sgt1926 p.284 (f848) school_enrolment auditors: lines vs Totaux: cells give 187, printed 177 (difference -10)
  - sgt1927 p.282 (f310) school_enrolment auditors: lines vs Totaux: cells give 196, printed 186 (difference -10)
  - sgt1928 p.286 (f838) school_enrolment auditors: lines vs Totaux: cells give 204, printed 194 (difference -10)
  - sgt1929 p.287 (f315) school_enrolment auditors: lines vs Totaux: cells give 216, printed 206 (difference -10)
  - sgt1930 p.294 (f852) school_enrolment 1924-1925: total = sum: cells give 124, printed 116 (difference -8)
  - sgt1930 p.294 (f852) school_enrolment year2: lines vs Totaux: cells give 915, printed 907 (difference -8)
  - sgt1930 p.294 (f852) school_enrolment auditors: lines vs Totaux: cells give 232, printed 222 (difference -10)
  - sgt1935 p.141 (f161) school_enrolment year2: lines vs Totaux: cells give 1069, printed 1061 (difference -8)
  - sgt1935 p.141 (f161) school_enrolment auditors: lines vs Totaux: cells give 257, printed 262 (difference 5)

- Overlapping printings: 651 cell comparisons with other editions printing the same cell; 25 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1898-1899 / auditors | sgt1922 | 15 | sgt1935 | 0 |
| 1898-1899 / auditors | sgt1923 | 15 | sgt1935 | 0 |
| 1898-1899 / auditors | sgt1924 | 15 | sgt1935 | 0 |
| 1898-1899 / auditors | sgt1925 | 15 | sgt1935 | 0 |
| 1898-1899 / auditors | sgt1926 | 15 | sgt1935 | 0 |
| 1898-1899 / auditors | sgt1927 | 15 | sgt1935 | 0 |
| 1898-1899 / auditors | sgt1928 | 15 | sgt1935 | 0 |
| 1898-1899 / auditors | sgt1929 | 15 | sgt1935 | 0 |
| 1898-1899 / auditors | sgt1930 | 15 | sgt1935 | 0 |
| 1907-1908 / regular_students_year1 | sgt1922 | 15 | sgt1935 | 17 |
| 1910-1911 / regular_students_year1 | sgt1923 | 31 | sgt1935 | 32 |
| 1910-1911 / regular_students_year1 | sgt1924 | 31 | sgt1935 | 32 |
| 1910-1911 / regular_students_year1 | sgt1925 | 31 | sgt1935 | 32 |
| 1910-1911 / regular_students_year1 | sgt1926 | 31 | sgt1935 | 32 |
| 1910-1911 / regular_students_year1 | sgt1927 | 31 | sgt1935 | 32 |
| 1910-1911 / regular_students_year1 | sgt1928 | 31 | sgt1935 | 32 |
| 1910-1911 / regular_students_year1 | sgt1929 | 31 | sgt1935 | 32 |
| 1924-1925 / regular_students_year2 | sgt1924 | 54 | sgt1935 | 59 |
| 1924-1925 / regular_students_year2 | sgt1925 | 54 | sgt1935 | 59 |
| 1924-1925 / regular_students_year2 | sgt1926 | 54 | sgt1935 | 59 |
| 1924-1925 / regular_students_year2 | sgt1927 | 54 | sgt1935 | 59 |
| 1924-1925 / regular_students_year2 | sgt1928 | 54 | sgt1935 | 59 |
| 1924-1925 / regular_students_year2 | sgt1929 | 54 | sgt1935 | 59 |
| 1928-1929 / regular_students_year2 | sgt1928 | 46 | sgt1935 | 47 |
| 1928-1929 / regular_students_year2 | sgt1929 | 46 | sgt1935 | 47 |

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (10 printings): sgt1922 f276, sgt1923 f767, sgt1924 f1271, sgt1925 f337, sgt1926 f848, sgt1927 f310, sgt1928 f838, sgt1929 f315, sgt1930 f852, sgt1935 f161.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
