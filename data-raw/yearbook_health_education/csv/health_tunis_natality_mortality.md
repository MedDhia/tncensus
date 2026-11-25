# État comparatif de la natalité et de la mortalité à Tunis

*Comparative natality and mortality in Tunis, by nationality.*

Source: *Statistique générale de la Tunisie*, chapter III (health), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1922 (`bpt6k9105649x`): p. 59, f83; sgt1923 (`bpt6k9105649x`): p. 65, f567; sgt1924 (`bpt6k9105649x`): p. 68, f1058; sgt1925 (`bpt6k9105650k`): p. 68, f92; sgt1926 (`bpt6k9105650k`): p. 77, f641; sgt1927 (`bpt6k91056510`): p. 75, f103; sgt1928 (`bpt6k91056510`): p. 75, f627; sgt1929 (`bpt6k9105652d`): p. 77, f105; sgt1930 (`bpt6k9105652d`): p. 81, f639; sgt1935 (`bpt6k9105653t`): p. 49, f69; sgt1936 (`bpt6k91056547`): p. 38, f49; sgt1939 (`bpt6k9105739w`): p. 39, f45.

Transcriptions: `../transcribed/health_pop_<edition>.txt`, section `@tunis_natality_mortality`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_population.py build`. Per-check output: `health_validation.json`.

Rows: 588. Years: 1922–1939 (12 years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939).

Printed once per edition, for the edition's own year; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to
- `indicator`: row code (listed in the commentary below / in the civil-hospital file)
- `indicator_fr`: row label as printed in the edition the value is taken from
- `nationality`: `french`, `tunisian_muslim`, `tunisian_jewish`, `italian`, `anglo_maltese`, `other`; `european` where the table groups the other Europeans; `total` for a printed all-nationality rate
- `nationality_fr`: column or row heading (French)
- `value`: count (integer), except where the notes say otherwise; printed » = 0
- `flag`: empty, or `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (row totals, TOTAUX lines, nationality brackets) and the printed "différence en plus / en moins" columns are not stored; they were used for validation.

d) "État comparatif de la natalité et de la mortalité à Tunis" by nationality. Indicators: `deaths`, `stillbirths` (Morts-nés), `non_residents`, `deaths_corrected` (Mortalité rectifiée), `births` (Naissances déclarées), `births_minus_deaths` (Différence entre naissances et décès; printed with + / − signs, stored signed), `population` (Population approximative), `mortality_per_1000` (rate, 2 decimals; the printed all-nationality rate is stored with `nationality` = `total`). Other TOTAUX not stored.

Definitions vary by edition: sgt1922 rectifies deaths by non-residents only, later editions by non-residents and stillbirths; until sgt1930 the difference and the rate use rectified deaths, from sgt1935 gross deaths. sgt1935 prints the differences without signs. The population is the same in sgt1922–sgt1924 (171.676), sgt1926–sgt1928 (185.996), sgt1930–sgt1935 (202.405) and sgt1936–sgt1939 (219.277).

Flagged misprints (`total_mismatch`, printed value kept): sgt1924 differences for Muslims (printed −253; 2.999 − 2.746 = +253) and Anglo-Maltese (printed +7; 122 − 129 = −7), the row total 1.771 needing the corrected signs; sgt1928 Autres printed −10 (35 − 25 = +10; the row total 2.135 needs +10); sgt1935 Anglo-Maltese 73 (printed without sign; 35 − 108 = −73) and Autres 96 (64 − 60 = 4; with −73 and 4 the row sums to the printed 2.313); sgt1936 Anglo-Maltese 55 (45 − 90 = −45; the row total 2.445 needs −45); sgt1939 Muslim rectified deaths 373 (4.435 − 323 − 382 = 3.730, which closes the printed 5.956). Unflagged: sgt1927 rectified deaths off by −9 / −6 / +2 (total 4.853 vs 4.866); sgt1928 rates for French (15,71) and Muslims (30,87) imply 439 and 2.554 rectified deaths against the printed 429 and 2.545 (which agree with deaths − stillbirths − non-residents and with the total 4.306); sgt1930 Jewish rate 20,70 vs 522 / 25.399 = 20,55; sgt1935 Anglo-Maltese rectified 96 vs 97.

## Validation

- Checks against printed totals: 336; passed: 315; failed: 21.

Failed checks (printed values kept; every one was re-read on the page image and the printed figures are as transcribed; see the commentary above for the cells involved):

  - sgt1924 tunis_natality_mortality row Différence entre naissances et décès: cells vs row total: cells give 1279, printed 1771
  - sgt1924 natality col 1: births - deaths vs difference: cells give 253, printed -253
  - sgt1924 natality col 4: births - deaths vs difference: cells give -7, printed 7
  - sgt1927 natality col 0: deaths - non-residents (- stillbirths) vs rectified: cells give 453, printed 444
  - sgt1927 natality col 1: deaths - non-residents (- stillbirths) vs rectified: cells give 2869, printed 2863
  - sgt1927 natality col 3: deaths - non-residents (- stillbirths) vs rectified: cells give 804, printed 806
  - sgt1927 natality col 6: deaths - non-residents (- stillbirths) vs rectified: cells give 4866, printed 4853
  - sgt1928 tunis_natality_mortality row Différence entre naissances et décès: cells vs row total: cells give 2115, printed 2135
  - sgt1928 natality col 0: rate vs deaths/population: cells give 15.364, printed 15.71
  - sgt1928 natality col 1: rate vs deaths/population: cells give 30.763, printed 30.87
  - sgt1928 natality col 5: births - deaths vs difference: cells give 10, printed -10
  - sgt1930 natality col 2: rate vs deaths/population: cells give 20.552, printed 20.7
  - sgt1935 tunis_natality_mortality row Mortalité rectifiée: cells vs row total: cells give 4623, printed 4624
  - sgt1935 tunis_natality_mortality row Différence entre naissances et décès: cells vs row total: cells give 2551, printed 2313
  - sgt1935 natality col 4: deaths - non-residents (- stillbirths) vs rectified: cells give 97, printed 96
  - sgt1935 natality col 4: births - deaths vs difference: cells give -61, printed 73
  - sgt1935 natality col 5: births - deaths vs difference: cells give 11, printed 96
  - sgt1936 tunis_natality_mortality row Différence entre naissance et décès: cells vs row total: cells give 2545, printed 2445
  - sgt1936 natality col 4: births - deaths vs difference: cells give -33, printed 55
  - sgt1939 tunis_natality_mortality row Mortalité rectifiée: cells vs row total: cells give 2599, printed 5956
  - sgt1939 natality col 1: deaths - non-residents (- stillbirths) vs rectified: cells give 3730, printed 373

- Flagged cells: total_mismatch: 7.

  - sgt1924 1924 births_minus_deaths / Différence entre naissances et décès / tunisian_muslim / Musulmans = -253 (total_mismatch)
  - sgt1924 1924 births_minus_deaths / Différence entre naissances et décès / anglo_maltese / Anglo-Maltais = 7 (total_mismatch)
  - sgt1928 1928 births_minus_deaths / Différence entre naissances et décès / other / Autres = -10 (total_mismatch)
  - sgt1935 1935 births_minus_deaths / Différence entre naissances et décès / anglo_maltese / Anglo-Maltais = 73 (total_mismatch)
  - sgt1935 1935 births_minus_deaths / Différence entre naissances et décès / other / Autres = 96 (total_mismatch)
  - sgt1936 1936 births_minus_deaths / Différence entre naissance et décès / anglo_maltese / Anglo-Maltais = 55 (total_mismatch)
  - sgt1939 1939 deaths_corrected / Mortalité rectifiée / tunisian_muslim / Musulmans = 373 (total_mismatch)
