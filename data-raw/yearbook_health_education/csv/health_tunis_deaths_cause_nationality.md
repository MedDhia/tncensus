# Statistique sanitaire de la ville de Tunis : décès par genre de maladie et par nationalité

*Health statistics of the city of Tunis: deaths by cause and nationality.*

Source: *Statistique générale de la Tunisie*, chapter III (health), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1922 (`bpt6k9105649x`): p. 59, f83; sgt1923 (`bpt6k9105649x`): p. 65, f567; sgt1924 (`bpt6k9105649x`): p. 68, f1058; sgt1925 (`bpt6k9105650k`): p. 68, f92; sgt1926 (`bpt6k9105650k`): p. 77, f641; sgt1927 (`bpt6k91056510`): p. 75, f103; sgt1928 (`bpt6k91056510`): p. 75, f627; sgt1929 (`bpt6k9105652d`): p. 77, f105; sgt1930 (`bpt6k9105652d`): p. 81, f639; sgt1935 (`bpt6k9105653t`): p. 50, f70; sgt1936 (`bpt6k91056547`): p. 39, f50; sgt1939 (`bpt6k9105739w`): p. 40, f46.

Transcriptions: `../transcribed/health_pop_<edition>.txt`, section `@tunis_cause_nationality`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_population.py build`. Per-check output: `health_validation.json`.

Rows: 942. Years: 1922–1939 (12 years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939).

Printed once per edition, for the edition's own year; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to
- `cause`: English code
- `cause_fr`: disease label exactly as printed
- `nationality`: `french`, `tunisian_muslim`, `tunisian_jewish`, `italian`, `anglo_maltese`, `other`; `european` where the table groups the other Europeans; `total` for a printed all-nationality rate
- `nationality_fr`: column or row heading (French)
- `value`: count (integer), except where the notes say otherwise; printed » = 0
- `flag`: empty, or `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (row totals, TOTAUX lines, nationality brackets) and the printed "différence en plus / en moins" columns are not stored; they were used for validation.

c) "Décès par genre de maladie et par nationalité" (in sgt1935–sgt1939 printed before the month × cause table). sgt1939 splits tuberculosis into "Tuberculose de l'appareil respiratoire" and "Autres tuberculoses" and names "Typhus exanthématique", "Paludisme (malaria)". All checks pass.

## Validation

- Checks against printed totals: 253; passed: 253; failed: 0.

- Flagged cells: none.

## Cross-checks

- Deaths by month vs deaths by cause and the natality table, per nationality and edition (printed totals and sums of cells): 564 comparisons, 561 equal.
  - sgt1922 total: deaths by month sum of printed row totals 4607 vs deaths by cause sum of printed row totals 4599
  - sgt1922 Janvier: month x cause total 491 vs month x nationality total 499
  - sgt1939 Maladies ordinaires: month x cause TOTAUX 5956 vs cause x nationality total 5827

The three differences are explained by two printing errors: sgt1922 January printed 499 instead of 491 in the month × nationality table (so its row totals sum to 4.607), and in sgt1939 the month × cause table counts the 134 "Autres tuberculoses" under "Maladies ordinaires" (see that file's notes). Every nationality total of deaths by month equals the one of deaths by cause and the "Nombre de décès" of the natality table, in all 12 editions.

