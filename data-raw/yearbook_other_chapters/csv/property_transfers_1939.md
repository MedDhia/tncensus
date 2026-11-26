# Conservation de la propriété foncière. Mutations entre vifs en 1939 d'immeubles immatriculés

*Land registry: transfers inter vivos of registered properties in 1939, by contrôle civil (number and value).*

Source: *Statistique générale de la Tunisie*, chapter *Propriété immobilière / Tribunal mixte / Propriété foncière*, editions sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1939 (`bpt6k9105739w`): p. 57, f63.

Transcriptions: `../transcribed/property_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_property.py build`.

Rows: 38. Years: 1939.

Units: transfers (`unit` = `count`), francs with centimes (`francs`). Mixed table.

Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, with `year`; no year is printed by two editions.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: `transfers`
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (the edition year: each edition prints the table for its own year)
- `controle_civil`: contrôle civil as printed (last line: Territoire Militaire (Medenine))
- `measure`: `number` or `value`
- `measure_fr`: printed column heading
- `unit`: `count` or `francs`
- `value`: number of transfers or francs
- `flag`: empty, or `total_mismatch` (printed value kept), `derived_from_totals`, `row_realigned`, `not_applicable` (nothing printed)

Printed only in sgt1939 (f63, p. 57).

Failed check (printed error): the values sum to 209.216.237,28 for a printed Totaux 209.216.217,28 (every line re-read on a crop).

Survey of the whole chapter in every edition: `property_survey.md`.

## Validation

- Checks against printed totals and identities: 2; passed: 1; failed: 1.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1939 p.57 (f63) transfers value: lines vs Totaux: cells give 209216237.28, printed 209216217.28 (difference -20.00)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (1 printings): sgt1939 f63.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
