# Institut Pasteur. a) Budget

*Institut Pasteur of Tunis: budget (receipts and expenditure).*

Source: *Statistique générale de la Tunisie*, chapter *Institutions d'enseignement et de recherches*, editions sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1935 (`bpt6k9105653t`): p. 136, f156; sgt1936 (`bpt6k91056547`): p. 106, f117; sgt1939 (`bpt6k9105739w`): p. 110, f116.

Transcriptions: `../transcribed/research_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_research.py build`.

Rows: 20. Years: 1935, 1936, 1939.

Unit: francs (centimes as decimals); value_type: francs.

Selection (SPEC_ADDENDUM rule 5): printed once per edition (the edition's year); all editions kept.

## Columns

- `census`: source edition (`sgt1922` ... `sgt1939`)
- `table_id`: section code of the transcription
- `gallica_ark`: Gallica volume ark
- `source_page`: printed page number
- `gallica_view`: Gallica view
- `year`: year of the figure (for a school year or season: the year it ends; for promotions and once-per-edition tables: the edition year)
- `side`: `receipts` or `expenditure`
- `side_fr`: Recettes / Dépenses
- `item`: ASCII slug of `item_fr`
- `item_fr`: line as printed (sub-heading prefixed, ditto marks expanded)
- `unit`: unit of the line (francs, persons, analyses, doses, flacons, cc, tubes, ampoules, litres, samples, quintals, hectares, producers, count)
- `value`: printed figure (» = 0)
- `flag`: empty, or ocr_corrected / illegible / total_mismatch / derived_from_totals / not_applicable / reprint_corrected / row_realigned

Printed totals (Total des recettes, Total des dépenses) are checks only.

Every failed check below was re-read on a zoomed native-resolution crop: they are printed inconsistencies (printed values kept). 

Survey of the whole chapter in every edition: `research_survey.md`.

## Validation

- Checks against printed totals and identities: 6; passed: 4; failed: 2.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1935 p.136 (f156) pasteur_budget [expenditure] value: lines vs Total des dépenses: cells give 1527166.69, printed 1427166.69 (difference -100000.00)
  - sgt1936 p.106 (f117) pasteur_budget [receipts] value: lines vs Total des recettes: cells give 1025939.45, printed 1630049.78 (difference 604110.33)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (6 printings): sgt1935 f156, sgt1935 f156, sgt1936 f117, sgt1936 f117, sgt1939 f116, sgt1939 f116.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
