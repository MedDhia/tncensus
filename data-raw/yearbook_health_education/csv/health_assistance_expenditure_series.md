# Assistance publique : dépenses (séries décennales)

*Public assistance budget: expenditure by budget line, ten-year series (sgt1922–sgt1923).*

Source: *Statistique générale de la Tunisie*, chapter III (health and assistance), editions sgt1922, sgt1923. Source gallica.bnf.fr / BnF.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 44, f68; sgt1923 (`bpt6k9105649x`): p. 48, f550.

Transcriptions: `../transcribed/health_finance_<edition>.txt`, sections `[expenditure_series]`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_finance.py build`. Per-check output: `health_finance_validation.json`.

Rows: 875. Years: 1913–1923. Unit of `value`: francs; amounts are as printed, centimes kept as decimals (printed » = 0).

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition) and every other printing of the same cell is compared below. Duplicate printings are not stored.

Years printed by each edition: sgt1922 1913–1922; sgt1923 1914–1923.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (for a table over two pages, the page of the column group)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (budget year, account year or calendar year; see below)
- `part_fr`: part / section of the budget as printed
- `line_fr`: budget line / article label as printed (ditto marks expanded)
- `line_en`: English code built from the French label (key words translated, place names kept)
- `value`: francs; empty where the flag says so
- `flag`: empty, or `derived_from_totals`, `total_mismatch`, `not_applicable`, `illegible`, `reprint_corrected` (see below)

Table "Dépenses" of the public-assistance budget, printed in sgt1922 (1913–1922) and sgt1923 (1914–1923): credits by line (subsidies to the hospitals of the interior, upkeep of French children and of the insane in France, subsidies to each society, reserve fund, unforeseen expenses). `part_fr` = the part/section heading as printed ("Première Partie, Section A/B", "Section C"; sgt1923 also "Deuxième Partie", "Annexe"). The "A reporter" line of sgt1923 and TOTAUX are not stored.

Failed checks, sgt1922 TOTAUX: 1913 (lines 168.500, printed 168.000), 1919 (lines 238.937,50, printed 252.937,50) and 1920 (lines 350.700, printed 349.700). For 1919 and 1920 sgt1923 prints totals equal to the sum of the lines (238.937,50 and 350.700), and the sgt1922 figures are those of the receipts series: the sgt1922 totals line was set from the receipts. The 1913 difference is not resolved (only sgt1922 prints 1913; not re-read cell by cell). sgt1923 prints all years up to 1922 with the same lines and amounts as sgt1922 (585 comparisons, no difference except these two totals).

## Validation

- Checks against printed totals: 30; passed: 27; failed: 3.

Failed checks (printed values kept, unless a flag below says otherwise; `L<n>` = line of the transcription file). See the commentary above for which ones were re-read on the page images and which are repeated identically in several printings:

  - sgt1922 expenditure_series TOTAUX (line 92) group 0 col 1913: rows above vs printed: cells give 168500, printed 168000
  - sgt1922 expenditure_series TOTAUX (line 92) group 0 col 1919: rows above vs printed: cells give 238937.5, printed 252937.5
  - sgt1922 expenditure_series TOTAUX (line 92) group 0 col 1920: rows above vs printed: cells give 350700.0, printed 349700

- Overlapping printings: 585 cell comparisons between editions; 2 differences.

| year | cell | edition | printed | latest edition | printed | stored (edition, flag) |
|---|---|---|---|---|---|---|
| 1919 | TOTAUX | sgt1922 | 252937.50 | sgt1923 | 238937.50 | not stored (printed total) |
| 1920 | TOTAUX | sgt1922 | 349700 | sgt1923 | 350700 | not stored (printed total) |

- Flagged cells: none.

## Cross-check of budget totals

The total of each budget year printed in the receipt series, the expenditure series, the receipts table and the credits table of every edition that prints it, and the printed difference with the previous budget (totals line) against the two totals: 81 comparisons, 76 equal.
  - 1919: receipts series TOTAUX (sgt1922) 252937.5 vs expenditure series TOTAUX (sgt1923) 238937.5
  - 1920: receipts series TOTAUX (sgt1922) 349700 vs expenditure series TOTAUX (sgt1923) 350700
  - 1926: receipts series TOTAUX (sgt1926) 924100 vs budget receipts TOTAUX (sgt1926) 1019100
  - 1926: receipts series TOTAUX (sgt1926) 924100 vs budget receipts TOTAUX (sgt1927) 1019100
  - 1926: receipts series TOTAUX (sgt1926) 924100 vs budget credits TOTAUX (sgt1926) 1019100

