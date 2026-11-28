# Voitures automobiles immatriculées ; Autres transports publics ; Mouvement du port aérien de Tunis

*Registered motor vehicles, other public transport operators and Tunis airport traffic (sgt1939).*

Source: *Statistique générale de la Tunisie*, chapter *Travaux publics*, editions sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1939 (`bpt6k9105739w`): p. 82, f88, p. 83, f89.

Transcriptions: `../transcribed/publicworks_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_publicworks.py build`.

Rows: 47. Years: 1936, 1937, 1938, 1939.

Units: count, thousands, thousand francs, kg (`unit`); suggested value_type: mixed.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition; an aligned printing is preferred to a realigned one); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from: the latest edition printing that year (rule 5 tables: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `item`: item code
- `item_fr`: printed heading
- `category`: category code
- `category_fr`: printed line
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible`, `not_applicable` (nothing printed), `row_realigned` (printed on the wrong line, stored on the year it belongs to), `total_mismatch`

Printed in sgt1939 only (f88-f89): motor vehicles registered at 31 December 1936-1939 by category (TOTAL used as check) and transfers of registered vehicles; other public transport 1938-1939 (thousands of passengers and of francs; no figures for the Tunisienne Automobile Transports, autonomous since the end of the Convention tripartite, 1 January 1938); Tunis airport (Tunis-Carthage and El-Aouina bases, public transport) 1937-1939.

Every failed check below was re-read on a zoomed native-resolution crop, or recurs unchanged in independent readings of several editions: they are printed errors (printed values kept). 1936 vehicles: the four categories sum to 28.512, TOTAL printed 28.962.

Survey of the whole chapter in every edition: `publicworks_survey.md`.

## Validation

- Checks against printed totals and identities: 4; passed: 3; failed: 1.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1939 p.82 (f88) vehicles 1936: TOTAL = four categories: cells give 28512, printed 28962 (difference 450)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (3 printings): sgt1939 f88, sgt1939 f89, sgt1939 f89.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
