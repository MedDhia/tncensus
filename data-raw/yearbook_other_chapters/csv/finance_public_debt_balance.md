# Dette tunisienne. b) Balance des opérations

*Tunisian public debt: balance of operations since 1884, breakdown of the amounts remaining to be paid.*

Source: *Statistique générale de la Tunisie*, chapter *Finances*, editions sgt1925, sgt1926, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1925 (`bpt6k9105650k`): p. 192, f216; sgt1926 (`bpt6k9105650k`): p. 208, f772; sgt1928 (`bpt6k91056510`): p. 206, f758; sgt1929 (`bpt6k9105652d`): p. 208, f236; sgt1930 (`bpt6k9105652d`): p. 213, f771; sgt1935 (`bpt6k9105653t`): p. 112, f132; sgt1936 (`bpt6k91056547`): p. 87, f98; sgt1939 (`bpt6k9105739w`): p. 91, f97.

Transcriptions: `../transcribed/finance_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_finance.py build`.

Rows: 50. Years: 1921, 1923, 1924, 1925, 1927, 1934, 1935, 1938.

Unit: francs (centimes kept); value_type: francs.

Each printing gives the operations cumulated from 1884 to a year named in its title (1921, 1923, 1924, 1924, 1925, 1927, 1934, 1935, 1938): one series by that year, each year from the **latest** edition printing it (SPEC_ADDENDUM rule 4; `census` = that edition). Only 1924 is printed twice (sgt1927 and sgt1928, same standing type): sgt1928 is stored and the sgt1927 printing, read independently on its own image, is compared below.

## Columns

- `census`: edition the value is taken from (the latest edition printing that year; 1924: sgt1928, sgt1927 compared)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: last year of the cumulative period ("de 1884 à <year>" in the title)
- `period_fr`: period covered, as printed in the title (cumulative operations since 1884)
- `status`: décomposition des restes à payer: `due_prescribed` (échus, prescrits), `due_not_prescribed` (échus, non prescrits), `due_cancelled` (échus, annulés: sgt1939 only), `not_due` (non échus)
- `status_fr`: printed line label
- `component`: `capital` or `interest` (intérêts)
- `component_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed amount (» = 0), francs with centimes
- `flag`: empty, or `ocr_corrected` (image reading differs from the Gallica OCR), `total_mismatch` (printed value kept; identified by a failed check as the faulty cell, see Validation), `illegible` (value NA), `not_applicable` (nothing printed, value NA), `derived_from_totals` (digits hidden in the binding; value = the printed row total minus the other cells of the row, see the notes)

Printed below (sgt1925-sgt1930) or on the page after (sgt1935-sgt1939) the operations table: Charges and Conversions et payements (the Totaux of the operations table), Reste à payer, its décomposition (échus: prescrits, non prescrits, and in sgt1939 annulés; non échus) and "Total égal à celui ci-dessus", in capital and intérêts, with the capital + intérêts sums under braces. Only the décomposition is stored (it is the only information not in `finance_public_debt`); the other lines are checks.

Failed checks, each re-read on zoomed native-resolution crops (printed errors): sgt1925, the brace sum under the Total égal à celui ci-dessus is printed 416.138.289 18 for 461.138.289 18 (printed correctly under Reste à payer; transposed digits). sgt1927 and sgt1928 (same standing type): the décomposition sums to 489.407.045 58 (capital) and 54.918.534 87 (intérêts), printed so in the Total line, whereas Reste à payer is 526.835.694 33 and 17.489.886 12; the brace sums agree (544.325.580 45). The difference, 37.428.648 75, moves between the capital and intérêts of the échus non prescrits line (6.548.197 02 and 54.687.225 55; 43.976.845 77 and 17.258.576 80 would balance): both cells flagged `total_mismatch`, printed values kept. sgt1929: the balance prints Charges intérêts 353.693.320 69, the operations Totaux 353.693.320 62 (see `finance_public_debt`). sgt1935: the balance prints Conversions et payements capital 1.036.109.389 14 against 1.056.109.389 14 in the operations table (whose lines give 1.056...), and Reste à payer 967.634.759 follows the 1.036 figure; the décomposition sums to the printed Reste à payer, so the stored cells are consistent with the balance but 20.000.000 short of the operations table; no cell identified. sgt1936: the capital décomposition sums to 969.423.244 85, the Reste à payer and Total print 969.432.244 85 (9.000; transposed digits somewhere in the décomposition or the total), no cell identified.

Survey of the whole chapter in every edition: `finance_survey.md`.

## Validation

- Checks against printed totals and identities: 108; passed: 99; failed: 9.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1925 p.192 (f216) debt_balance total_both: capital + intérêts (brace): cells give 461138289.18, printed 416138289.18 (difference -45000000.00)
  - sgt1927 p.206 (f234) debt_balance cap: Total égal à celui ci-dessus = Reste à payer: cells give 526835694.33, printed 489407045.58 (difference -37428648.75)
  - sgt1927 p.206 (f234) debt_balance int: Total égal à celui ci-dessus = Reste à payer: cells give 17489886.12, printed 54918534.87 (difference 37428648.75)
  - sgt1928 p.206 (f758) debt_balance cap: Total égal à celui ci-dessus = Reste à payer: cells give 526835694.33, printed 489407045.58 (difference -37428648.75)
  - sgt1928 p.206 (f758) debt_balance int: Total égal à celui ci-dessus = Reste à payer: cells give 17489886.12, printed 54918534.87 (difference 37428648.75)
  - sgt1929 p.208 (f236) debt_balance int: Charges = Totaux of a): cells give 353693320.62, printed 353693320.69 (difference 0.07)
  - sgt1935 p.112 (f132) debt_balance cap: Conversions et payements = Totaux of a): cells give 1056109389.14, printed 1036109389.14 (difference -20000000.00)
  - sgt1935 p.112 (f132) debt_balance cap: Reste à payer = Charges - Conversions et payements: cells give 987634759.00, printed 967634759 (difference -20000000.00)
  - sgt1936 p.87 (f98) debt_balance cap: Total égal à celui ci-dessus = décomposition: cells give 969423244.85, printed 969432244.85 (difference 9000.00)

- Overlapping printings: 6 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: ocr_corrected: 5, total_mismatch: 2.

  - sgt1926 p.208 1923 due_not_prescribed / capital / francs = 59293786.81 (ocr_corrected)
  - sgt1928 p.206 1924 due_not_prescribed / capital / francs = 6548197.02 (total_mismatch)
  - sgt1928 p.206 1924 due_not_prescribed / interest / francs = 54687225.55 (total_mismatch)
  - sgt1928 p.206 1924 not_due / capital / francs = 482483752.27 (ocr_corrected)
  - sgt1930 p.213 1927 due_prescribed / interest / francs = 925383.49 (ocr_corrected)
  - sgt1930 p.213 1927 due_not_prescribed / interest / francs = 13182897.46 (ocr_corrected)
  - sgt1936 p.87 1935 not_due / capital / francs = 896345835.35 (ocr_corrected)

## Image versus OCR

- Read cell by cell on the page images (9 printings): sgt1925 f216, sgt1926 f772, sgt1927 f234, sgt1928 f758, sgt1929 f236, sgt1930 f771, sgt1935 f132, sgt1936 f98, sgt1939 f97.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 6.
