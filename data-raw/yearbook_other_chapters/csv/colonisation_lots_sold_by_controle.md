# Ventes avec obligation d'installation : c) Répartition par contrôle civil des lots vendus de 1893 à 1922 (1923)

*Colonisation lots sold since 1893, by contrôle civil and type of lot: number and area.*

Source: *Statistique générale de la Tunisie*, chapter *Colonisation*, editions sgt1922, sgt1923. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 420, f444, p. 421, f445; sgt1923 (`bpt6k9105649x`): p. 432, f934, p. 433, f935.

Transcriptions: `../transcribed/colonisation_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_colonisation.py build`.

Rows: 240. Years: 1922, 1923.

Units: number of lots and hectares (`unit`); suggested value_type: mixed.

Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept (`census` = edition); the figures are the state at the edition date and are revised between editions.

## Columns

- `census`: edition the value is taken from (rule 4 tables: the latest edition printing that year)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (yearly lists) or the edition year (cumulative recapitulations: state at the edition date, period in `period_fr`)
- `period_fr`: period covered by the cumulative recapitulation, as printed in the title (e.g. `1893-1922`)
- `controle_civil`: contrôle civil as printed (`Territ. milit.` = territoires militaires; a ditto '—' is resolved to the line above; empty for a néant line)
- `lot_type`: `culture` (lots de culture / de colonisation), `suburban`, `urban_industrial`
- `lot_type_fr`: printed lot type
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `row_realigned` (printed on the neighbouring line, stored on its own line)

Old layout printed only in sgt1922 and sgt1923 (chapter XIII); from sgt1924 the chapter is reorganised (installation / planting / urban lists, recapitulation by origin of the land) and this table is no longer printed. Printed total lines and total columns are checks only (not stored); » = 0.

f444|f445 (sgt1922) and f934|f935 (sgt1923), cumulative from 1893 to the edition year (`year` = edition year). Lots de culture areas are printed to the hectare (» in the ares column) except a few sgt1923 lines. The TOTAL columns (lots, area) are checked on every line and the TOTAL GÉNÉRAL line on every column. The sgt1923 totals equal the lots créés of its summary table.

Every failed check below was re-read on a native-resolution crop: the printed values are kept. sgt1923 Thala prints the line TOTAL area 1.446,89 for 1.353 + 82,23 + 10,66 = 1.445,89; the column totals agree with the lines, so the faulty figure is the printed line total (check only, not stored; sgt1922's Thala line adds up).

Survey of the whole chapter in every edition: `colonisation_survey.md`.

## Validation

- Checks against printed totals and identities: 100; passed: 98; failed: 2.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1923 p.432 (f934) soldcc Thala: tot_ha = cult_ha + sub_ha + urb_ha: cells give 1445.89, printed 1446.89 (difference 1.00)
  - sgt1923 p.432 (f934) soldcc tot_ha: TOTAL = sum of the lines: cells give 177732.87, printed 177731.87 (difference -1.00)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (2 printings): sgt1922 f444, sgt1923 f934.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
