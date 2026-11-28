# Statistique quinquennale des élèves (depuis 1885)

*Quinquennial series of pupils since 1885: boys and girls, public and private.*

Source: *Statistique générale de la Tunisie*, chapter "Instruction publique et beaux-arts" (VII; VI in sgt1936 and sgt1939), editions sgt1922, sgt1923, sgt1924, sgt1926, sgt1927, sgt1929, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1922 (`bpt6k9105649x`): p. 128, f152; sgt1923 (`bpt6k9105649x`): p. 134, f636; sgt1924 (`bpt6k9105649x`): p. 136, f1126; sgt1926 (`bpt6k9105650k`): p. 148, f712; sgt1927 (`bpt6k91056510`): p. 146, f174; sgt1929 (`bpt6k9105652d`): p. 148, f176; sgt1935 (`bpt6k9105653t`): p. 88, f108; sgt1936 (`bpt6k91056547`): p. 66, f77; sgt1939 (`bpt6k9105739w`): p. 70, f76.

Transcriptions: `../transcribed/education_sum_<edition>.txt`; rebuild with `python3 data-raw/yearbook_health_education/extract_education_summary.py build`. Per-check output: `education_summary_validation.json`.

Rows: 84. Years: 1885–1939 (21 years: 1885, 1890, 1895, 1900, 1905, 1910, 1915, 1920, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1934, 1935, 1936, 1939).

Printed for overlapping year windows: every cell of a year is taken from the **latest** edition that prints that year (SPEC_ADDENDUM rule 4; `census` = that edition) and every other printing of the same cell is compared below. Duplicate printings are not stored.

Years printed by each edition: sgt1922 1885, 1890, 1895, 1900, 1905, 1910, 1915, 1920, 1922; sgt1923 1885, 1890, 1895, 1900, 1905, 1910, 1915, 1920, 1923; sgt1924 1885, 1890, 1895, 1900, 1905, 1910, 1915, 1920, 1924; sgt1925 1885, 1890, 1895, 1900, 1905, 1910, 1915, 1920, 1925; sgt1926 1885, 1890, 1895, 1900, 1905, 1910, 1915, 1920, 1925, 1926; sgt1927 1885, 1890, 1895, 1900, 1905, 1910, 1915, 1920, 1925, 1927; sgt1928 1885, 1890, 1895, 1900, 1905, 1910, 1915, 1920, 1925, 1928; sgt1929 1885, 1890, 1895, 1900, 1905, 1910, 1915, 1920, 1925, 1928, 1929; sgt1930 1885, 1890, 1895, 1900, 1905, 1910, 1915, 1920, 1925, 1930; sgt1935 1890, 1895, 1900, 1905, 1910, 1915, 1920, 1925, 1930, 1934, 1935; sgt1936 1885, 1890, 1895, 1900, 1905, 1910, 1915, 1920, 1925, 1930, 1936; sgt1939 1885, 1890, 1895, 1900, 1905, 1910, 1915, 1920, 1925, 1930, 1935, 1939.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number; pages without a printed number are inferred from the next page. For the two-page spreads (population, primary-education and first-degree totals) the boys' block is given the left-hand page and the girls' block and total columns the right-hand page (the printed fold falls near the boys' TOTAUX, so one or two boys' columns may in fact sit on the right-hand page)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (31 December of that year for pupils; the school year's examinations)
- `sex`: `male`, `female`; `total` where the cell is not split by sex (empty in the comparative table for items that are not pupils)
- `sex_fr`: column heading as printed (Aspirants / Aspirantes in the examination table, Garçons / Filles elsewhere)
- `sector`: `public` or `private`
- `sector_fr`: as printed
- `value`: count (integer); printed » = 0; empty where the cell is not printed (`not_applicable`)
- `flag`: empty, or `ocr_corrected`, `derived_from_totals`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (TOTAUX, Totaux généraux, subtotals, A reporter) are not stored unless stated; they were used for validation.

Comparative statistics b) "Statistique quinquennale": pupils at 31 December, boys and girls, public and private education, every fifth year from 1885 plus the edition year (and 1934 in sgt1935). The totals per sex and the total général are checks only. sgt1935 starts at 1890; sgt1936 and sgt1939 again at 1885. Public pupils exclude the auditors of adult courses (sgt1939 footnote).

**1905 boys, public**: sgt1922–sgt1926 print 10.799, sgt1927–sgt1939 10.999; 10.799 + 2.159 = 12.958, the boys' total printed by all editions: kept from sgt1926 (`reprint_corrected`). **1925 girls, private**: sgt1939 prints 3.416, every earlier printing 3.419 (16.756 + 3.419 = 20.175): kept from sgt1936 (`reprint_corrected`). **1920 total général**: every edition prints 42.497 although 26.678 + 17.333 = 44.011 (the population tables give 44.011 for 1920; 42.497 is their 1919 total); the four cells are consistent with the population table and are kept. **1926 boys, private**: sgt1926 (the only printing) has 5.199; 38.853 + 3.199 = 42.052 and the population table gives 3.199 (`total_mismatch`, printed value kept). sgt1930 prints the 1930 boys' total 51.545 for 52.545 (a total, not stored).

## Footnotes printed under the table

- (1) Non compris les auditeurs des cours d'adultes. (sgt1939)

## Validation

- Checks against printed totals: 484; passed: 440; failed: 44.

Failed checks (every cell involved was re-read on a native-resolution crop; the printed figures are as transcribed; see the commentary above):

  - sgt1922 1920: boys total + girls total vs total général: cells give 44011, printed 42497
  - sgt1922 1920: four cells vs total général: cells give 44011, printed 42497
  - sgt1923 1920: boys total + girls total vs total général: cells give 44011, printed 42497
  - sgt1923 1920: four cells vs total général: cells give 44011, printed 42497
  - sgt1924 1920: boys total + girls total vs total général: cells give 44011, printed 42497
  - sgt1924 1920: four cells vs total général: cells give 44011, printed 42497
  - sgt1925 1920: boys total + girls total vs total général: cells give 44011, printed 42497
  - sgt1925 1920: four cells vs total général: cells give 44011, printed 42497
  - sgt1926 1920: boys total + girls total vs total général: cells give 44011, printed 42497
  - sgt1926 1920: four cells vs total général: cells give 44011, printed 42497
  - sgt1926 1926 boys: public + private vs total: cells give 44052, printed 42052
  - sgt1926 1926: four cells vs total général: cells give 64667, printed 62667
  - sgt1927 1905 boys: public + private vs total: cells give 13158, printed 12958
  - sgt1927 1905: four cells vs total général: cells give 21959, printed 21759
  - sgt1927 1920: boys total + girls total vs total général: cells give 44011, printed 42497
  - sgt1927 1920: four cells vs total général: cells give 44011, printed 42497
  - sgt1928 1905 boys: public + private vs total: cells give 13158, printed 12958
  - sgt1928 1905: four cells vs total général: cells give 21959, printed 21759
  - sgt1928 1920: boys total + girls total vs total général: cells give 44011, printed 42497
  - sgt1928 1920: four cells vs total général: cells give 44011, printed 42497
  - sgt1929 1905 boys: public + private vs total: cells give 13158, printed 12958
  - sgt1929 1905: four cells vs total général: cells give 21959, printed 21759
  - sgt1929 1920: boys total + girls total vs total général: cells give 44011, printed 42497
  - sgt1929 1920: four cells vs total général: cells give 44011, printed 42497
  - sgt1930 1905 boys: public + private vs total: cells give 13158, printed 12958
  - sgt1930 1905: four cells vs total général: cells give 21959, printed 21759
  - sgt1930 1920: boys total + girls total vs total général: cells give 44011, printed 42497
  - sgt1930 1920: four cells vs total général: cells give 44011, printed 42497
  - sgt1930 1930 boys: public + private vs total: cells give 52545, printed 51545
  - sgt1930 1930: boys total + girls total vs total général: cells give 75752, printed 76752
  - sgt1935 1905 boys: public + private vs total: cells give 13158, printed 12958
  - sgt1935 1905: four cells vs total général: cells give 21959, printed 21759
  - sgt1935 1920: boys total + girls total vs total général: cells give 44011, printed 42497
  - sgt1935 1920: four cells vs total général: cells give 44011, printed 42497
  - sgt1936 1905 boys: public + private vs total: cells give 13158, printed 12958
  - sgt1936 1905: four cells vs total général: cells give 21959, printed 21759
  - sgt1936 1920: boys total + girls total vs total général: cells give 44011, printed 42497
  - sgt1936 1920: four cells vs total général: cells give 44011, printed 42497
  - sgt1939 1905 boys: public + private vs total: cells give 13158, printed 12958
  - sgt1939 1905: four cells vs total général: cells give 21959, printed 21759
  - sgt1939 1920: boys total + girls total vs total général: cells give 44011, printed 42497
  - sgt1939 1920: four cells vs total général: cells give 44011, printed 42497
  - sgt1939 1925 girls: public + private vs total: cells give 20172, printed 20175
  - sgt1939 1925: four cells vs total général: cells give 59594, printed 59597

- Overlapping printings: 400 cell comparisons between editions; 13 differences.

| year | cell | edition | printed | latest edition | printed | stored (edition, flag) |
|---|---|---|---|---|---|---|
| 1905 | male/public | sgt1922 | 10799 | sgt1939 | 10999 | 10799 (sgt1926, reprint_corrected) |
| 1905 | male/public | sgt1923 | 10799 | sgt1939 | 10999 | 10799 (sgt1926, reprint_corrected) |
| 1905 | male/public | sgt1924 | 10799 | sgt1939 | 10999 | 10799 (sgt1926, reprint_corrected) |
| 1905 | male/public | sgt1925 | 10799 | sgt1939 | 10999 | 10799 (sgt1926, reprint_corrected) |
| 1905 | male/public | sgt1926 | 10799 | sgt1939 | 10999 | 10799 (sgt1926, reprint_corrected) |
| 1925 | female/private | sgt1925 | 3419 | sgt1939 | 3416 | 3419 (sgt1936, reprint_corrected) |
| 1925 | female/private | sgt1926 | 3419 | sgt1939 | 3416 | 3419 (sgt1936, reprint_corrected) |
| 1925 | female/private | sgt1927 | 3419 | sgt1939 | 3416 | 3419 (sgt1936, reprint_corrected) |
| 1925 | female/private | sgt1928 | 3419 | sgt1939 | 3416 | 3419 (sgt1936, reprint_corrected) |
| 1925 | female/private | sgt1929 | 3419 | sgt1939 | 3416 | 3419 (sgt1936, reprint_corrected) |
| 1925 | female/private | sgt1930 | 3419 | sgt1939 | 3416 | 3419 (sgt1936, reprint_corrected) |
| 1925 | female/private | sgt1935 | 3419 | sgt1939 | 3416 | 3419 (sgt1936, reprint_corrected) |
| 1925 | female/private | sgt1936 | 3419 | sgt1939 | 3416 | 3419 (sgt1936, reprint_corrected) |

- Flagged cells: reprint_corrected: 2, total_mismatch: 1.

  - sgt1926 1905 male / public = 10799 (reprint_corrected)
  - sgt1936 1925 female / private = 3419 (reprint_corrected)
  - sgt1926 1926 male / private = 5199 (total_mismatch)

## Cross-checks with other tables of the chapter

- 72 comparisons; equal: 71; different: 1.
  - sgt1926 1926 boys private vs population table écoles privées: cells give 5199, printed 3199
