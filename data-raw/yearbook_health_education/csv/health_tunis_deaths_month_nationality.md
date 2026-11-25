# Statistique sanitaire de la ville de Tunis : décès par nationalité (par mois)

*Health statistics of the city of Tunis: deaths by month and nationality.*

Source: *Statistique générale de la Tunisie*, chapter III (health), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1922 (`bpt6k9105649x`): p. 58, f82; sgt1923 (`bpt6k9105649x`): p. 64, f566; sgt1924 (`bpt6k9105649x`): p. 67, f1057; sgt1925 (`bpt6k9105650k`): p. 67, f91; sgt1926 (`bpt6k9105650k`): p. 76, f640; sgt1927 (`bpt6k91056510`): p. 74, f102; sgt1928 (`bpt6k91056510`): p. 74, f626; sgt1929 (`bpt6k9105652d`): p. 76, f104; sgt1930 (`bpt6k9105652d`): p. 80, f638; sgt1935 (`bpt6k9105653t`): p. 49, f69; sgt1936 (`bpt6k91056547`): p. 38, f49; sgt1939 (`bpt6k9105739w`): p. 39, f45.

Transcriptions: `../transcribed/health_pop_<edition>.txt`, section `@tunis_month_nationality`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_population.py build`. Per-check output: `health_validation.json`.

Rows: 864. Years: 1922–1939 (12 years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939).

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
- `nationality`: `french`, `tunisian_muslim`, `tunisian_jewish`, `italian`, `anglo_maltese`, `other`; `european` where the table groups the other Europeans; `total` for a printed all-nationality rate
- `nationality_fr`: column or row heading (French)
- `value`: count (integer), except where the notes say otherwise; printed » = 0
- `flag`: empty, or `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (row totals, TOTAUX lines, nationality brackets) and the printed "différence en plus / en moins" columns are not stored; they were used for validation.

"Statistique sanitaire de la ville de Tunis", a) "Décès par nationalité": deaths in the city of Tunis by month and nationality (Français, Musulmans, Israélites tunisiens, Italiens, Anglo-Maltais, Autres). TOTAUX row and column not stored. sgt1922: January is printed 499 against cells summing to 491 (the month × cause table also gives 491; the printed TOTAUX 4.599 is consistent with 491).

## Validation

- Checks against printed totals: 240; passed: 238; failed: 2.

Failed checks (printed values kept; every one was re-read on the page image and the printed figures are as transcribed; see the commentary above for the cells involved):

  - sgt1922 tunis_month_nationality row Janvier: cells vs row total: cells give 491, printed 499
  - sgt1922 tunis_month_nationality column total: rows vs TOTAUX: cells give 4607, printed 4599

- Flagged cells: none.

## Cross-checks

- Deaths by month vs deaths by cause and the natality table, per nationality and edition (printed totals and sums of cells): 564 comparisons, 561 equal.
  - sgt1922 total: deaths by month sum of printed row totals 4607 vs deaths by cause sum of printed row totals 4599
  - sgt1922 Janvier: month x cause total 491 vs month x nationality total 499
  - sgt1939 Maladies ordinaires: month x cause TOTAUX 5956 vs cause x nationality total 5827

The three differences are explained by two printing errors: sgt1922 January printed 499 instead of 491 in the month × nationality table (so its row totals sum to 4.607), and in sgt1939 the month × cause table counts the 134 "Autres tuberculoses" under "Maladies ordinaires" (see that file's notes). Every nationality total of deaths by month equals the one of deaths by cause and the "Nombre de décès" of the natality table, in all 12 editions.


## Comparison with the état civil (contrôle civil of Tunis)

Muslim and Jewish deaths in the city of Tunis (sum of this table's monthly cells) against deaths recorded in the contrôle civil of Tunis (`../../yearbook_demography/csv/vital_*_births_deaths.csv`). The contrôle covers more than the city (banlieue and rural cheikhats), so equality is not expected.

| population | year | city of Tunis | contrôle civil of Tunis | city / contrôle |
|---|---|---:|---:|---:|
| muslim | 1922 | 2705 | 3594 | 0.75 |
| muslim | 1923 | 3315 | 3399 | 0.98 |
| muslim | 1924 | 3319 | 3961 | 0.84 |
| muslim | 1925 | 3911 | 4600 | 0.85 |
| muslim | 1926 | 3087 | 3668 | 0.84 |
| muslim | 1927 | 3380 | 3964 | 0.85 |
| muslim | 1928 | 3078 | 3675 | 0.84 |
| muslim | 1929 | 3247 | 3817 | 0.85 |
| muslim | 1930 | 3195 | 3711 | 0.86 |
| muslim | 1935 | 3391 | 4022 | 0.84 |
| muslim | 1936 | 3758 | 4140 | 0.91 |
| muslim | 1939 | 4435 | 5406 | 0.82 |
| jewish | 1922 | 541 | 565 | 0.96 |
| jewish | 1923 | 615 | 618 | 1.00 |
| jewish | 1924 | 630 | 777 | 0.81 |
| jewish | 1925 | 652 | 718 | 0.91 |
| jewish | 1926 | 611 | 587 | 1.04 |
| jewish | 1927 | 643 | 606 | 1.06 |
| jewish | 1928 | 531 | 540 | 0.98 |
| jewish | 1929 | 586 | 571 | 1.03 |
| jewish | 1930 | 593 | 492 | 1.21 |
| jewish | 1935 | 528 | 502 | 1.05 |
| jewish | 1936 | 618 | 498 | 1.24 |
| jewish | 1939 | 623 | 800 | 0.78 |
