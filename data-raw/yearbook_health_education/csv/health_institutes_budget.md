# Institut Pasteur et Institut Arloing : budget

*Institut Pasteur and Institut Arloing: budget receipts and expenditure (sgt1922–sgt1930).*

Source: *Statistique générale de la Tunisie*, chapter III (health and assistance), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / BnF.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 55, f79, p. 56, f80; sgt1923 (`bpt6k9105649x`): p. 61, f563, p. 62, f564; sgt1924 (`bpt6k9105649x`): p. 64, f1054, p. 65, f1055; sgt1925 (`bpt6k9105650k`): p. 64, f88, p. 65, f89; sgt1926 (`bpt6k9105650k`): p. 73, f637, p. 74, f638; sgt1927 (`bpt6k91056510`): p. 71, f99, p. 72, f100; sgt1928 (`bpt6k91056510`): p. 71, f623, p. 72, f624; sgt1929 (`bpt6k9105652d`): p. 73, f101, p. 74, f102; sgt1930 (`bpt6k9105652d`): p. 77, f635, p. 78, f636.

Transcriptions: `../transcribed/health_finance_<edition>.txt`, sections `[institute_budget]`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_finance.py build`. Per-check output: `health_finance_validation.json`.

Rows: 112. Years: 1922–1930. Unit of `value`: francs; amounts are as printed, centimes kept as decimals (printed » = 0).

Printed once per edition; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (for a table over two pages, the page of the column group)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (budget year, account year or calendar year; see below)
- `institute`: `pasteur` or `arloing`
- `institute_fr`: as printed
- `side`: `receipts` or `expenditure`
- `line_fr`: budget line / article label as printed (ditto marks expanded)
- `line_en`: English code built from the French label (key words translated, place names kept)
- `value`: francs; empty where the flag says so
- `flag`: empty, or `derived_from_totals`, `total_mismatch`, `not_applicable`, `illegible`, `reprint_corrected` (see below)

a) Budget of the Institut Pasteur de Tunis and of the Institut Arloing (sgt1922–sgt1930; not printed in sgt1935–sgt1939): receipts and expenditure lines as printed; the Arloing budget has a second part (new receipts, receipts carried forward and their use) and a third part (amounts outstanding / expenditure of closed years) in sgt1922–sgt1924. TOTAL lines not stored. Failed checks (printed figures as transcribed; the lines were compared with the Gallica OCR where it is legible): sgt1923 Arloing receipts 0,60 off; sgt1925 Pasteur receipts 3.000 off; sgt1928 Arloing expenditure 10.005,95 off; sgt1930 Arloing receipts 40 off. The budget year is the edition's year.

## Validation

- Checks against printed totals: 36; passed: 32; failed: 4.

Failed checks (printed values kept, unless a flag below says otherwise; `L<n>` = line of the transcription file). See the commentary above for which ones were re-read on the page images and which are repeated identically in several printings:

  - sgt1923 arloing receipts: lines vs total: cells give 359965.27, printed 359965.87
  - sgt1925 pasteur receipts: lines vs total: cells give 539107.21, printed 542107.21
  - sgt1928 arloing expenditure: lines vs total: cells give 559616.26, printed 569622.21
  - sgt1930 arloing receipts: lines vs total: cells give 852854.91, printed 852814.91

- Flagged cells: none.
