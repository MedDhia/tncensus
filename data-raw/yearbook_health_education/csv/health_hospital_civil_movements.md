# Hôpital civil français de Tunis : mouvement des entrées et sorties

*French Civil Hospital of Tunis: admissions and discharges.*

Source: *Statistique générale de la Tunisie*, chapter III (health), editions sgt1925, sgt1927, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1925 (`bpt6k9105650k`): p. 56, f80; sgt1927 (`bpt6k91056510`): p. 64, f92; sgt1929 (`bpt6k9105652d`): p. 66, f94; sgt1930 (`bpt6k9105652d`): p. 70, f628; sgt1935 (`bpt6k9105653t`): p. 42, f62; sgt1936 (`bpt6k91056547`): p. 32, f43; sgt1939 (`bpt6k9105739w`): p. 33, f39.

Transcriptions: `../transcribed/health_pop_<edition>.txt`, section `@civil_movements`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_population.py build`. Per-check output: `health_validation.json`.

Rows: 154. Years: 1921–1939 (17 years: 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1933, 1934, 1935, 1936, 1937, 1938, 1939).

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition) and every other printing of the same cell is compared below. Duplicate printings are not stored.

Years printed by each edition: sgt1922 1921–1922; sgt1923 1921–1923; sgt1924 1921–1924; sgt1925 1921–1925; sgt1926 1924–1926; sgt1927 1924–1927; sgt1928 1925–1928; sgt1929 1925–1929; sgt1930 1926–1930; sgt1935 1933–1935; sgt1936 1934–1936; sgt1939 1937–1939.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to
- `movement`: `carried_over_and_admitted` (patients present on 1 January plus admissions during the year), `discharged_recovered`, `discharged_died`, `remaining_31_december`, `stillborn`
- `movement_fr`: column heading as printed
- `sex_age`: `male` (Hommes), `female` (Femmes), `child` (Enfants), `total` (only where the parts are not printed)
- `sex_age_fr`: as printed
- `value`: count (integer), except where the notes say otherwise; printed » = 0
- `flag`: empty, or `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (row totals, TOTAUX lines, nationality brackets) and the printed "différence en plus / en moins" columns are not stored; they were used for validation.

Table a) "Mouvement des entrées et sorties". The first column group is headed "Restants et entrées" (sgt1922–sgt1925) and "Report au 1er janvier et entrées" (from sgt1926): patients present on 1 January plus admissions during the year. sgt1925 adds a single column "Observations et restants au 31 décembre 1925" for 1925 only (stored as `remaining_31_december` / `total`). Printed totals per group are not stored.

Checks: each group's men + women + children against its printed TOTAL. Failures (all re-read on the images, printed as transcribed): 1926 deaths 69 + 73 + 47 = 189 against a printed 201, repeated identically in all five editions that print 1926 (sgt1926–sgt1930); 1933 admissions 1.551 + 2.129 + 1.402 = 5.082 against 5.182 (sgt1935); 1934 deaths 123 + 130 + 119 = 372 against 312 (sgt1935 and sgt1936). The faulty cell cannot be identified, so no cell is flagged.

No edition prints 1931–1932 (there are no 1931–1934 yearbooks in the series).

## Validation

- Checks against printed totals: 132; passed: 124; failed: 8.

Failed checks (printed values kept; every one was re-read on the page image and the printed figures are as transcribed; see the commentary above for the cells involved):

  - sgt1926 civil_movements 1926 dth: m+f+c vs total: cells give 189, printed 201
  - sgt1927 civil_movements 1926 dth: m+f+c vs total: cells give 189, printed 201
  - sgt1928 civil_movements 1926 dth: m+f+c vs total: cells give 189, printed 201
  - sgt1929 civil_movements 1926 dth: m+f+c vs total: cells give 189, printed 201
  - sgt1930 civil_movements 1926 dth: m+f+c vs total: cells give 189, printed 201
  - sgt1935 civil_movements 1933 adm: m+f+c vs total: cells give 5082, printed 5182
  - sgt1935 civil_movements 1934 dth: m+f+c vs total: cells give 372, printed 312
  - sgt1936 civil_movements 1934 dth: m+f+c vs total: cells give 372, printed 312

- Overlapping printings: 324 cell comparisons between editions; 0 differences.

- Flagged cells: none.
