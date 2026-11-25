# Statistique sanitaire de la ville de Tunis : décès par genre de maladie (par mois)

*Health statistics of the city of Tunis: deaths by month and cause.*

Source: *Statistique générale de la Tunisie*, chapter III (health), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1922 (`bpt6k9105649x`): p. 58, f82; sgt1923 (`bpt6k9105649x`): p. 64, f566; sgt1924 (`bpt6k9105649x`): p. 67, f1057; sgt1925 (`bpt6k9105650k`): p. 67, f91; sgt1926 (`bpt6k9105650k`): p. 76, f640; sgt1927 (`bpt6k91056510`): p. 74, f102; sgt1928 (`bpt6k91056510`): p. 74, f626; sgt1929 (`bpt6k9105652d`): p. 76, f104; sgt1930 (`bpt6k9105652d`): p. 80, f638; sgt1935 (`bpt6k9105653t`): p. 50, f70; sgt1936 (`bpt6k91056547`): p. 39, f50; sgt1939 (`bpt6k9105739w`): p. 40, f46.

Transcriptions: `../transcribed/health_pop_<edition>.txt`, section `@tunis_month_cause`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_population.py build`. Per-check output: `health_validation.json`.

Rows: 1872. Years: 1922–1939 (12 years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939).

Printed once per edition, for the edition's own year; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to
- `month`: `january` … `december`; `carried_over_1_january` for patients carried over (Rabta 1935)
- `month_fr`: as printed
- `cause`: English code
- `cause_fr`: disease label exactly as printed
- `value`: count (integer), except where the notes say otherwise; printed » = 0
- `flag`: empty, or `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (row totals, TOTAUX lines, nationality brackets) and the printed "différence en plus / en moins" columns are not stored; they were used for validation.

b) "Décès par genre de maladie": deaths by month × cause (Maladies ordinaires and 12 epidemic diseases). In sgt1939 the tuberculosis column is "Tuberculose pulmonaire" and "Maladies ordinaires" (5.956) appears to include the 134 "Autres tuberculoses" that the cause × nationality table shows separately (5.827 + 134 = 5.961; the remaining 5 are the measles gap below).

Identified misprints (`total_mismatch`): sgt1925 July diphtheria printed » (the row 608 and the column 17 each need 1); sgt1928 October tuberculosis 59 (row 490 and column 613 need 51). Other failures: sgt1922 September and October rows off by −1 / +1 (columns agree); sgt1939 measles column sums to 117 against a printed 112 (the cause × nationality table also prints 112), so the TOTAUX row sums to 6.951 against 6.956.

## Validation

- Checks against printed totals: 324; passed: 316; failed: 8.

Failed checks (printed values kept; every one was re-read on the page image and the printed figures are as transcribed; see the commentary above for the cells involved):

  - sgt1922 tunis_month_cause row Septembre: cells vs row total: cells give 378, printed 379
  - sgt1922 tunis_month_cause row Octobre: cells vs row total: cells give 380, printed 379
  - sgt1925 tunis_month_cause row Juillet: cells vs row total: cells give 607, printed 608
  - sgt1925 tunis_month_cause column Diphtérie: rows vs TOTAUX: cells give 16, printed 17
  - sgt1928 tunis_month_cause row Octobre: cells vs row total: cells give 498, printed 490
  - sgt1928 tunis_month_cause column Tuberculose: rows vs TOTAUX: cells give 621, printed 613
  - sgt1939 tunis_month_cause row TOTAUX: cells vs row total: cells give 6951, printed 6956
  - sgt1939 tunis_month_cause column Rougeole: rows vs TOTAUX: cells give 117, printed 112

- Flagged cells: total_mismatch: 2.

  - sgt1925 1925 july / Juillet / diphtheria / Diphtérie = 0 (total_mismatch)
  - sgt1928 1928 october / Octobre / tuberculosis / Tuberculose = 59 (total_mismatch)

## Cross-checks

- Deaths by month vs deaths by cause and the natality table, per nationality and edition (printed totals and sums of cells): 564 comparisons, 561 equal.
  - sgt1922 total: deaths by month sum of printed row totals 4607 vs deaths by cause sum of printed row totals 4599
  - sgt1922 Janvier: month x cause total 491 vs month x nationality total 499
  - sgt1939 Maladies ordinaires: month x cause TOTAUX 5956 vs cause x nationality total 5827

The three differences are explained by two printing errors: sgt1922 January printed 499 instead of 491 in the month × nationality table (so its row totals sum to 4.607), and in sgt1939 the month × cause table counts the 134 "Autres tuberculoses" under "Maladies ordinaires" (see that file's notes). Every nationality total of deaths by month equals the one of deaths by cause and the "Nombre de décès" of the natality table, in all 12 editions.

