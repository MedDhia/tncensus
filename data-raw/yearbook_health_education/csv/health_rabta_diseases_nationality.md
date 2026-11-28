# Hôpital de la Rabta : maladies traitées par nationalité

*Rabta hospital: diseases treated (admissions) by nationality.*

Source: *Statistique générale de la Tunisie*, chapter III (health), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1922 (`bpt6k9105649x`): p. 52, f76; sgt1923 (`bpt6k9105649x`): p. 58, f560; sgt1924 (`bpt6k9105649x`): p. 61, f1051; sgt1925 (`bpt6k9105650k`): p. 61, f85; sgt1926 (`bpt6k9105650k`): p. 70, f634; sgt1927 (`bpt6k91056510`): p. 68, f96; sgt1928 (`bpt6k91056510`): p. 68, f620; sgt1929 (`bpt6k9105652d`): p. 70, f98; sgt1930 (`bpt6k9105652d`): p. 74, f632; sgt1935 (`bpt6k9105653t`): p. 47, f67; sgt1936 (`bpt6k91056547`): p. 36, f47; sgt1939 (`bpt6k9105739w`): p. 37, f43.

Transcriptions: `../transcribed/health_pop_<edition>.txt`, section `@rabta_diseases`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_population.py build`. Per-check output: `health_validation.json`.

Rows: 1170. Years: 1922–1939 (12 years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939).

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

"Répartition des maladies soignées (par maladie et par nationalité)": admissions by disease and nationality for the edition's year. The list of diseases changes between editions; `cause_fr` is the label as printed (spellings such as "Dyphtérie", "Encéphalée lithargique" kept), `cause` an English code. TOTAUX row and column are not stored.

Identified misprints (`total_mismatch`, printed value kept): sgt1930 diphtheria, Italians 4 (row total 1 and column total 121 both need 0); sgt1936 malaria, Muslims 47 (row total 97 and the Muslim column total 3.142 both need 97). Other failures: sgt1929 Muslim column 955 vs 956; sgt1936 typhus and typhoid row totals 15 and 6 against Muslim cells 20 and 17 (the column total agrees with the cells).

## Validation

- Checks against printed totals: 291; passed: 282; failed: 9.

Failed checks (printed values kept; every one was re-read on the page image and the printed figures are as transcribed; see the commentary above for the cells involved):

  - sgt1929 rabta_diseases column tunisian_muslim: rows vs TOTAUX: cells give 955, printed 956
  - sgt1929 rabta_diseases column total: rows vs TOTAUX: cells give 1019, printed 1020
  - sgt1930 rabta_diseases row Dyphtérie: cells vs row total: cells give 5, printed 1
  - sgt1930 rabta_diseases column italian: rows vs TOTAUX: cells give 125, printed 121
  - sgt1936 rabta_diseases row Typhus: cells vs row total: cells give 20, printed 15
  - sgt1936 rabta_diseases row Fièvre typhoïde: cells vs row total: cells give 17, printed 6
  - sgt1936 rabta_diseases row Paludisme: cells vs row total: cells give 47, printed 97
  - sgt1936 rabta_diseases column tunisian_muslim: rows vs TOTAUX: cells give 3092, printed 3142
  - sgt1936 rabta_diseases column total: rows vs TOTAUX: cells give 3167, printed 3183

- Flagged cells: total_mismatch: 2.

  - sgt1930 1930 diphtheria / Dyphtérie / italian / Italiens = 4 (total_mismatch)
  - sgt1936 1936 malaria / Paludisme / tunisian_muslim / Musulmans = 47 (total_mismatch)
