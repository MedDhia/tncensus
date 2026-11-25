# Assistance publique : recettes (séries décennales)

*Public assistance budget: receipts by budget line, ten-year series (sgt1922–sgt1926).*

Source: *Statistique générale de la Tunisie*, chapter III (health and assistance), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926. Source gallica.bnf.fr / BnF.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 42, f66; sgt1923 (`bpt6k9105649x`): p. 46, f548; sgt1925 (`bpt6k9105650k`): p. 46, f70; sgt1926 (`bpt6k9105650k`): p. 54, f618.

Transcriptions: `../transcribed/health_finance_<edition>.txt`, sections `[receipts_series]`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_finance.py build`. Per-check output: `health_finance_validation.json`.

Rows: 86. Years: 1913–1926. Unit of `value`: francs; amounts are as printed, centimes kept as decimals (printed » = 0).

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition) and every other printing of the same cell is compared below. Duplicate printings are not stored.

Years printed by each edition: sgt1922 1913–1922; sgt1923 1914–1923; sgt1924 1915–1924; sgt1925 1915–1925; sgt1926 1917–1926.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (for a table over two pages, the page of the column group)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (budget year, account year or calendar year; see below)
- `line_fr`: budget line / article label as printed (ditto marks expanded)
- `line_en`: English code built from the French label (key words translated, place names kept)
- `value`: francs; empty where the flag says so
- `flag`: empty, or `derived_from_totals`, `total_mismatch`, `not_applicable`, `illegible`, `reprint_corrected` (see below)

Table "Recettes" of the public-assistance budget, printed in sgt1922–sgt1926 for ten budget years (sgt1925: eleven), one row per receipt line (tax on gunpowder and arms permits, Nichan-Iftikhar decorations, court fines, cemetery concessions, theatre tax, etc.). `year` = budget year. Cells printed without an amount ("-": a bracket groups the line with lines carrying the amount) are not stored; printed » = 0. TOTAUX is not stored (checked, and compared between printings).

From the 1923 budget the receipts are one lump-sum allocation: sgt1923 prints 559.100 across the first nine lines with a footnote splitting it into "1° Allocation forfaitaire …" (529.100) and "2° Allocations complémentaires" (30.000), stored as those two lines; sgt1924 keeps that split for 1923 and prints 745.500 for 1924 as one bracketed amount; sgt1925 and sgt1926 print each year from 1923 as one bracketed amount, stored as the line "Montant unique imprimé en accolade sur les neuf premières lignes" (a label written by the transcriber, not printed). The two differences between printings below come from this change of presentation (1923: split in sgt1924–sgt1925, bracketed in sgt1926, same total). sgt1926 prints 924.100 for 1926, the lump-sum allocation only; the 1926 budget also had a complementary allocation of 95.000 (`health_assistance_budget_receipts`).

## Remarks recorded in the transcriptions

- sgt1923: 1923: one amount, 559.100, is printed across the first nine lines with a bracket and call (1); the footnote splits it into the two allocations above (Total égal 559.100). The two footnote lines are stored as lines of the 1923 column.
- sgt1924: 1923 as in sgt1923 (559.100 bracketed with call (1), split in the footnote). 1924: 745.500 bracketed across the first nine lines, with no footnote; stored as one line.
- sgt1925: The title says (1916-1925) but the first column printed is 1915.
- sgt1926: 1923 is printed as one bracketed amount in this edition (no footnote).

## Validation

- Checks against printed totals: 51; passed: 51; failed: 0.

- Overlapping printings: 464 cell comparisons between editions; 2 differences.

| year | cell | edition | printed | latest edition | printed | stored (edition, flag) |
|---|---|---|---|---|---|---|
| 1923 | montant unique imprime en accolade sur les neuf premieres li | sgt1924 | - | sgt1926 | 559100 | 559100 (sgt1926) |
| 1923 | montant unique imprime en accolade sur les neuf premieres li | sgt1925 | - | sgt1926 | 559100 | 559100 (sgt1926) |

- Flagged cells: none.

## Cross-check of budget totals

The total of each budget year printed in the receipt series, the expenditure series, the receipts table and the credits table of every edition that prints it, and the printed difference with the previous budget (totals line) against the two totals: 81 comparisons, 76 equal.
  - 1919: receipts series TOTAUX (sgt1922) 252937.5 vs expenditure series TOTAUX (sgt1923) 238937.5
  - 1920: receipts series TOTAUX (sgt1922) 349700 vs expenditure series TOTAUX (sgt1923) 350700
  - 1926: receipts series TOTAUX (sgt1926) 924100 vs budget receipts TOTAUX (sgt1926) 1019100
  - 1926: receipts series TOTAUX (sgt1926) 924100 vs budget receipts TOTAUX (sgt1927) 1019100
  - 1926: receipts series TOTAUX (sgt1926) 924100 vs budget credits TOTAUX (sgt1926) 1019100

