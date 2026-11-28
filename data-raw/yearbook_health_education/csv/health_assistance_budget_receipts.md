# Recettes du budget de l'Assistance publique

*Public assistance budget: receipts by article, budget year and previous year (sgt1924–sgt1930).*

Source: *Statistique générale de la Tunisie*, chapter III (health and assistance), editions sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / BnF.

Pages and views of the stored values: sgt1924 (`bpt6k9105649x`): p. 48, f1038; sgt1925 (`bpt6k9105650k`): p. 48, f72; sgt1926 (`bpt6k9105650k`): p. 56, f620; sgt1927 (`bpt6k91056510`): p. 55, f83; sgt1928 (`bpt6k91056510`): p. 55, f607; sgt1929 (`bpt6k9105652d`): p. 57, f85; sgt1930 (`bpt6k9105652d`): p. 59, f617.

Transcriptions: `../transcribed/health_finance_<edition>.txt`, sections `[budget_receipts]`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_finance.py build`. Per-check output: `health_finance_validation.json`.

Rows: 16. Years: 1923–1930. Unit of `value`: francs; amounts are as printed, centimes kept as decimals (printed » = 0).

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition) and every other printing of the same cell is compared below. Duplicate printings are not stored.

Years printed by each edition: sgt1924 1923–1924; sgt1925 1924–1925; sgt1926 1925–1926; sgt1927 1926–1927; sgt1928 1927–1928; sgt1929 1928–1929; sgt1930 1929–1930.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (for a table over two pages, the page of the column group)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (budget year, account year or calendar year; see below)
- `article`: article number as printed (`-` = printed without a number; letters/prefixes added where the edition numbers sub-items or restarts numbering by section, see the transcription file)
- `line_fr`: budget line / article label as printed (ditto marks expanded)
- `line_en`: English code built from the French label (key words translated, place names kept)
- `value`: francs; empty where the flag says so
- `flag`: empty, or `derived_from_totals`, `total_mismatch`, `not_applicable`, `illegible`, `reprint_corrected` (see below)

"Recettes" of the public-assistance budget by article (sgt1924–sgt1930), printed for the budget year and the previous year; `article` = article number as printed. The "Total" sub-lines and TOTAUX GÉNÉRAUX are not stored. Cells printed "mémoire" (pour mémoire, no amount) are stored empty with `not_applicable`; the "3. Mémoire. — Dotation Joséphine Virieu" line of sgt1924–sgt1925 has no amount and is not stored.

Article 1 is the allocation on the receipts collected by the Treasury for public assistance (budget of the State, chap. III, art. 14, then Titre I art. 13 § 1); article 2 the complementary allocation / exceptional resources (from 1929 the drawing on the reserve fund).

## Remarks recorded in the transcriptions

- sgt1924: printed under the table: "En plus au budget de 1924 ... 186.400"
- sgt1925: printed under the table: "En plus au budget de 1925 ... 114.800"
- sgt1926: printed: "En plus au budget de 1926: 63.800" (1°), "95.000" (2°), "En plus ... 158.800".
- sgt1927: printed: "En plus au budget de 1927": 319.400 (against 2°) and 422.900 (général). The difference for 1° (103.500) is not printed.
- sgt1928: printed: En plus au budget de 1928: 136.500 (1°); En moins: 18.100 (2°); En plus: 118.400 (général).
- sgt1929: printed: "En plus au budget de 1928" (sic) 179.900; "En moins au budget de 1928" 293.700 (sic: an increase); "En plus" 473.600.
- sgt1930: printed: En plus au budget de 1930: 834.200 (1°), 52.050 (2°), 886.250 (général).

## Validation

- Checks against printed totals: 34; passed: 34; failed: 0.

- Overlapping printings: 19 cell comparisons between editions; 1 differences.

| year | cell | edition | printed | latest edition | printed | stored (edition, flag) |
|---|---|---|---|---|---|---|
| 1925 | 2 | sgt1925 | mémoire | sgt1926 | » | 0 (sgt1926) |

- Flagged cells: not_applicable: 1.

  - sgt1925 1924 2 / Allocation complémentaire = None (not_applicable)

## Cross-check of budget totals

The total of each budget year printed in the receipt series, the expenditure series, the receipts table and the credits table of every edition that prints it, and the printed difference with the previous budget (totals line) against the two totals: 81 comparisons, 76 equal.
  - 1919: receipts series TOTAUX (sgt1922) 252937.5 vs expenditure series TOTAUX (sgt1923) 238937.5
  - 1920: receipts series TOTAUX (sgt1922) 349700 vs expenditure series TOTAUX (sgt1923) 350700
  - 1926: receipts series TOTAUX (sgt1926) 924100 vs budget receipts TOTAUX (sgt1926) 1019100
  - 1926: receipts series TOTAUX (sgt1926) 924100 vs budget receipts TOTAUX (sgt1927) 1019100
  - 1926: receipts series TOTAUX (sgt1926) 924100 vs budget credits TOTAUX (sgt1926) 1019100

