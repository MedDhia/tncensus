# Ventes avec obligation d'installation : b) Récapitulation (1893-1922) ; Superficie totale des terres livrées à la colonisation de 1893 à 1923

*Lands delivered to colonisation since 1893: area and lots by type of lot (and, in sgt1922, by origin of the land).*

Source: *Statistique générale de la Tunisie*, chapter *Colonisation*, editions sgt1922, sgt1923. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 419, f443; sgt1923 (`bpt6k9105649x`): p. 431, f933.

Transcriptions: `../transcribed/colonisation_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_colonisation.py build`.

Rows: 30. Years: 1922, 1923.

Units: hectares (area, printed h. a.) and number of lots (`unit`); suggested value_type: mixed.

Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept (`census` = edition); the figures are the state at the edition date and are revised between editions.

## Columns

- `census`: edition the value is taken from (rule 4 tables: the latest edition printing that year)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (yearly lists) or the edition year (cumulative recapitulations: state at the edition date, period in `period_fr`)
- `period_fr`: period covered by the cumulative recapitulation, as printed in the title (e.g. `1893-1922`)
- `origin`: origin of the land: `state_domain` (patrimoine domanial), `purchase_fund` (achats sur le fonds de colonisation), `all` (sgt1923: no split printed)
- `origin_fr`: printed origin heading (empty for `all`)
- `lot_type`: `culture` (lots de culture / de colonisation), `suburban`, `urban_industrial`
- `lot_type_fr`: printed lot type
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `row_realigned` (printed on the neighbouring line, stored on its own line)

Old layout printed only in sgt1922 and sgt1923 (chapter XIII); from sgt1924 the chapter is reorganised (installation / planting / urban lists, recapitulation by origin of the land) and this table is no longer printed. Printed total lines and total columns are checks only (not stored); » = 0.

sgt1922 (f442|f443, lower half): Patrimoine domanial and Achats sur le fonds de colonisation, each with lots de culture / suburbains / urbains ou industriels, and superficie totale, lots créés, réservés ou disponibles en cours de vente, vendus; the TOTAL of each origin and the TOTAL GÉNÉRAL are checks, and créés = réservés + vendus is checked on every line. sgt1923 (f932|f933) prints a shorter table: lots créés and superficie totale only, by lot type, all origins together (`origin` = `all`). Not the same table as `colonisation_lotissements_summary` (sgt1924-sgt1939: by origin domaines / habous / achat / terres sialines and two periods), which replaces it: kept as a separate file because the categories do not match.

Survey of the whole chapter in every edition: `colonisation_survey.md`.

## Validation

- Checks against printed totals and identities: 20; passed: 20; failed: 0.

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (2 printings): sgt1922 f442, sgt1923 f932.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
