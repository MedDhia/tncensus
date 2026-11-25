# Hôpital Sadiki : mouvement des entrées et sorties

*Sadiki Hospital: admissions and discharges.*

Source: *Statistique générale de la Tunisie*, chapter III (health), editions sgt1923, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1923 (`bpt6k9105649x`): p. 56, f558; sgt1925 (`bpt6k9105650k`): p. 58, f82; sgt1926 (`bpt6k9105650k`): p. 67, f631; sgt1927 (`bpt6k91056510`): p. 65, f93; sgt1928 (`bpt6k91056510`): p. 65, f617; sgt1929 (`bpt6k9105652d`): p. 67, f95; sgt1930 (`bpt6k9105652d`): p. 71, f629; sgt1935 (`bpt6k9105653t`): p. 44, f64; sgt1936 (`bpt6k91056547`): p. 34, f45; sgt1939 (`bpt6k9105739w`): p. 35, f41.

Transcriptions: `../transcribed/health_pop_<edition>.txt`, section `@sadiki_movements`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_population.py build`. Per-check output: `health_validation.json`.

Rows: 247. Years: 1912–1939 (26 years: 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1933, 1934, 1935, 1936, 1937, 1938, 1939).

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition) and every other printing of the same cell is compared below. Duplicate printings are not stored.

Years printed by each edition: sgt1922 1918–1922; sgt1923 1914–1923; sgt1924 1915–1924; sgt1925 1912–1925; sgt1926 1917–1926; sgt1927 1918–1927; sgt1928 1919–1928; sgt1929 1920–1929; sgt1930 1921–1930; sgt1935 1933–1935; sgt1936 1934–1936; sgt1939 1937–1939.

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

Table a) "Mouvement des entrées et sorties" of the Hôpital Sadiki, printed for long windows (5 to 14 years). The first group is "Report au 1er janvier et entrées". sgt1922 and sgt1923 add a column "Nouveau-nés morts-nés" (all », stored as 0, `stillborn` / `total`).

**1935 women admitted**: sgt1936 prints 1.448, but 2.393 + 1.488 + 428 = 4.309 (printed in both); the sgt1935 value 1.488 is kept (`reprint_corrected`). Failed group checks, all re-read: sgt1925 1912 deaths (243 vs 245) and 1913 admissions (2.950 vs 2.951), 1934 recoveries 3.830 vs 3.930 (sgt1935 and sgt1936), and the 1936 row of sgt1936 (admissions 4.882 vs 4.874, recoveries 4.531 vs 4.331, deaths 323 vs 343; the population table gives 4.680 admissions). No cell identifiable; none flagged.

## Validation

- Checks against printed totals: 295; passed: 287; failed: 8.

Failed checks (printed values kept; every one was re-read on the page image and the printed figures are as transcribed; see the commentary above for the cells involved):

  - sgt1925 sadiki_movements 1912 dth: m+f+c vs total: cells give 243, printed 245
  - sgt1925 sadiki_movements 1913 adm: m+f+c vs total: cells give 2950, printed 2951
  - sgt1935 sadiki_movements 1934 rec: m+f+c vs total: cells give 3830, printed 3930
  - sgt1936 sadiki_movements 1934 rec: m+f+c vs total: cells give 3830, printed 3930
  - sgt1936 sadiki_movements 1935 adm: m+f+c vs total: cells give 4269, printed 4309
  - sgt1936 sadiki_movements 1936 adm: m+f+c vs total: cells give 4882, printed 4874
  - sgt1936 sadiki_movements 1936 rec: m+f+c vs total: cells give 4531, printed 4331
  - sgt1936 sadiki_movements 1936 dth: m+f+c vs total: cells give 323, printed 343

- Overlapping printings: 869 cell comparisons between editions; 1 differences.

| year | cell | edition | printed | latest edition | printed | stored (edition, flag) |
|---|---|---|---|---|---|---|
| 1935 | adm/f | sgt1935 | 1488 | sgt1936 | 1448 | 1488 (sgt1935, reprint_corrected) |

- Flagged cells: reprint_corrected: 1.

  - sgt1935 1935 carried_over_and_admitted / Report au 1er janvier et entrées / female / Femmes = 1488 (reprint_corrected)
