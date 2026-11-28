# Habitations à bon marché. b) Subventions de l'Etat et capitaux investis

*Low-cost housing: state subsidies and capital invested, by period and type of dwelling.*

Source: *Statistique générale de la Tunisie*, chapter *Travail et prévoyance sociale*, editions sgt1930, sgt1936. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1930 (`bpt6k9105652d`): p. 489, f1047; sgt1936 (`bpt6k91056547`): p. 178, f189.

Transcriptions: `../transcribed/labour_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_labour.py build`.

Rows: 71. Years: 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934.

Unit: francs (as printed, centimes after the point); value_type: francs.

Printed for overlapping periods whose grouping changes between editions (single years, bracketed pairs, '1912 à 1919' / '1912 à 1920'): within each measure and housing type a printing is kept unless a later edition prints any year of its period (SPEC_ADDENDUM rule 4 applied to periods; `census` = that edition); printings of the identical period are compared below.

## Columns

- `census`: edition the value is taken from (rule 4 series: the latest edition printing it; rule 5: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (two-page spreads: the page the cell is printed on)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (HBM: last year of the printed period)
- `year_from`: first year of the printed period
- `period_fr`: period as printed
- `measure`: measure code (English)
- `measure_fr`: printed heading
- `housing_type`: type of dwelling (English code)
- `housing_type_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, ocr_corrected, illegible, total_mismatch, derived_from_totals, not_applicable, reprint_corrected or row_realigned

Printed sgt1927-sgt1936 (not in sgt1939). Subsidies are printed per year; capital invested is printed per year or for bracketed pairs of years (1925-1926, 1927-1928, 1929-1930). Capital columns stand under the housing types of table a): maisons individuelles et collectives; from sgt1929 logements ouvriers and militaires; from sgt1935 maritimes. sgt1927 observation 1912: 'Travaux réalisés avec la participation de l'Etat français'. sgt1930 prints the 1930 subsidy as '1.00.1000'; the Totaux gives 1.100.000 (`derived_from_totals`). sgt1936 prints 7.830.808 on the line 1927 and 16.814.168 / 9.768.737 between 1928 and 1929: stored as in sgt1935 (`row_realigned`).

Every failed check below was re-read on a zoomed native-resolution crop (or recurs unchanged in independent readings of several editions): printed values are kept. sgt1928 prints the 1912-1919 capital as 538.000 while its Totaux keeps 27.551.897,52, which needs sgt1927's single years (86.100 + 40.000 + 113.700 + 298.700 = 538.500). sgt1930's Total général 70.764.310,54 is 200 above the sum of its Totaux. sgt1935-sgt1936 print the 1930 subsidy 1.000.000 while the subsidy Totaux 14.336.000 needs sgt1930's 1.100.000 (the series stores 1.100.000, reprint_corrected); their Total général 122.856.629 equals the four capital Totaux plus the subsidy Totaux plus 10.000 (no single cell identified). sgt1936 repeats the capital Totaux 65.145.374 under logements ouvriers (sgt1935: 10.500.000).

Survey of the whole chapter in every edition: `labour_survey.md`.

## Validation

- Checks against printed totals and identities: 19; passed: 12; failed: 7.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1928 p.481 (f1033) hbm_finance cap: lines vs Totaux: cells give 27551397.52, printed 27551897.52 (difference 500.00)
  - sgt1930 p.489 (f1047) hbm_finance Total général = sum of the Totaux cap+cap_workers+cap_military: cells give 70764110.54, printed 70764310.54 (difference 200.00)
  - sgt1935 p.301 (f321) hbm_finance subv: lines vs Totaux: cells give 14236000, printed 14336000 (difference 100000)
  - sgt1935 p.301 (f321) hbm_finance Total général = sum of the Totaux cap+cap_workers+cap_military+cap_maritime: cells give 108510629, printed 122856629 (difference 14346000)
  - sgt1936 p.178 (f189) hbm_finance subv: lines vs Totaux: cells give 14236000, printed 14336000 (difference 100000)
  - sgt1936 p.178 (f189) hbm_finance cap_workers: lines vs Totaux: cells give 10500000, printed 65145374 (difference 54645374)
  - sgt1936 p.178 (f189) hbm_finance Total général = sum of the Totaux cap+cap_workers+cap_military+cap_maritime: cells give 163156003, printed 122856629 (difference -40299374)

- Overlapping printings: 175 cell comparisons with other editions printing the same cell; 10 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| state_subsidy /  / 1912 à 1919 | sgt1928 | 56000 | sgt1930 | 36000 |
| state_subsidy /  / 1930 | sgt1930 | 1100000 | sgt1936 | 1000000 |
| state_subsidy /  / 1930 | sgt1930 | 1100000 | sgt1936 | 1000000 |
| capital_invested / individual_and_collective / 1920 | sgt1927 | 5287472.52 | sgt1930 | 5287472.54 |
| capital_invested / individual_and_collective / 1920 | sgt1928 | 5287472.52 | sgt1930 | 5287472.54 |
| capital_invested / individual_and_collective / 1927-1928 | sgt1928 | 5201000 | sgt1936 | 7830808 |
| capital_invested / individual_and_collective / 1920 | sgt1929 | 5287472.52 | sgt1930 | 5287472.54 |
| capital_invested / individual_and_collective / 1929 | sgt1929 | 15980000 | sgt1936 | 16814168 |
| capital_invested / workers / 1929 | sgt1929 | 8225000 | sgt1936 | 9768737 |
| capital_invested / military / 1929 | sgt1929 | 14000000 | sgt1936 | 0 |

- Flagged cells: reprint_corrected: 1, row_realigned: 3.

  - sgt1936 p.178 1928 1927 / capital_invested / individual_and_collective / francs = 7830808 (row_realigned)
  - sgt1936 p.178 1929 1929 / capital_invested / individual_and_collective / francs = 16814168 (row_realigned)
  - sgt1936 p.178 1929 1929 / capital_invested / workers / francs = 9768737 (row_realigned)
  - sgt1930 p.489 1930 1930 / state_subsidy /  / francs = 1100000 (reprint_corrected)

## Image versus OCR

- Read cell by cell on the page images (6 printings): sgt1927 f503, sgt1928 f1033, sgt1929 f511, sgt1930 f1047, sgt1935 f321, sgt1936 f189.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
