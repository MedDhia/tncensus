# Hôpital des contagieux de la Rabta (Ernest-Conseil) : mouvement des entrées et sorties

*Rabta contagious-diseases hospital (Ernest-Conseil): admissions and discharges.*

Source: *Statistique générale de la Tunisie*, chapter III (health), editions sgt1922, sgt1923, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1922 (`bpt6k9105649x`): p. 51, f75; sgt1923 (`bpt6k9105649x`): p. 57, f559; sgt1926 (`bpt6k9105650k`): p. 69, f633; sgt1927 (`bpt6k91056510`): p. 67, f95; sgt1928 (`bpt6k91056510`): p. 67, f619; sgt1929 (`bpt6k9105652d`): p. 69, f97; sgt1930 (`bpt6k9105652d`): p. 73, f631; sgt1935 (`bpt6k9105653t`): p. 46, f66; sgt1936 (`bpt6k91056547`): p. 35, f46; sgt1939 (`bpt6k9105739w`): p. 36, f42.

Transcriptions: `../transcribed/health_pop_<edition>.txt`, section `@rabta_movements`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_population.py build`. Per-check output: `health_validation.json`.

Rows: 189. Years: 1918–1939 (20 years: 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1933, 1934, 1935, 1936, 1937, 1938, 1939).

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition) and every other printing of the same cell is compared below. Duplicate printings are not stored.

Years printed by each edition: sgt1922 1918–1922; sgt1923 1919–1923; sgt1924 1922–1924; sgt1925 1922–1925; sgt1926 1922–1926; sgt1927 1923–1927; sgt1928 1924–1928; sgt1929 1925–1929; sgt1930 1926–1930; sgt1935 1933–1935; sgt1936 1934–1936; sgt1939 1937–1939.

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

Rabta contagious-diseases hospital ("Annexe de la Rabta" in sgt1922–sgt1923, then "Hôpital des contagieux de la Rabta", "Hôpital Ernest-Conseil" from sgt1935). sgt1926–sgt1928 add "restants au 31 décembre" for the edition's last year.

sgt1936 prints the year labels in reverse order (1936, 1935, 1934), but the first two rows equal the 1934 and 1935 rows of sgt1935 and the third totals 3.183, the 1936 total of the diseases table, so the rows were assigned by content. Failed checks: 1929 deaths 182 + 22 + 15 = 219 against 270 (sgt1929 and sgt1930), 1933 recoveries 1.990 vs 1.989 (sgt1935).

## Validation

- Checks against printed totals: 156; passed: 153; failed: 3.

Failed checks (printed values kept; every one was re-read on the page image and the printed figures are as transcribed; see the commentary above for the cells involved):

  - sgt1929 rabta_movements 1929 dth: m+f+c vs total: cells give 219, printed 270
  - sgt1930 rabta_movements 1929 dth: m+f+c vs total: cells give 219, printed 270
  - sgt1935 rabta_movements 1933 rec: m+f+c vs total: cells give 1990, printed 1989

- Overlapping printings: 372 cell comparisons between editions; 0 differences.

- Flagged cells: none.
