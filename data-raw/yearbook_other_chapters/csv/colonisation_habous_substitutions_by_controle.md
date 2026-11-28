# Habous. Cessions par substitution aux droits du domaine. b) Récapitulation et répartition par contrôle civil

*Habous: properties ceded by substitution since 1899, by contrôle civil, with and without a colonisation clause.*

Source: *Statistique générale de la Tunisie*, chapter *Colonisation*, editions sgt1922, sgt1923. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 428, f452; sgt1923 (`bpt6k9105649x`): p. 440, f942.

Transcriptions: `../transcribed/colonisation_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_colonisation.py build`.

Rows: 144. Years: 1922, 1923.

Units: count, hectares and francs (`unit`); suggested value_type: mixed.

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
- `clause`: `without_colonisation_clause` / `with_colonisation_clause`
- `clause_fr`: printed column heading
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `row_realigned` (printed on the neighbouring line, stored on its own line)

Old layout printed only in sgt1922 and sgt1923 (chapter XIII); from sgt1924 the chapter is reorganised (installation / planting / urban lists, recapitulation by origin of the land) and this table is no longer printed. Printed total lines and total columns are checks only (not stored); » = 0.

sgt1922 f452 (1899-1922) and sgt1923 f942 (1899-1923), identical figures. Valeur globale is a check only.

Every failed check below was re-read on a native-resolution crop: the printed values are kept. Grombalia avec clause: valeur globale printed 168.610 for 142.610 + 16.000 = 158.610 (both editions, zoomed crop); the printed column total 1.960.463 agrees with 158.610, so the faulty figure is the printed line total (check only).

Survey of the whole chapter in every edition: `colonisation_survey.md`.

## Validation

- Checks against printed totals and identities: 60; passed: 56; failed: 4.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.428 (f452) hab_sub_cc Grombalia: c_tot = c_land + c_build: cells give 158610, printed 168610 (difference 10000)
  - sgt1922 p.428 (f452) hab_sub_cc c_tot: TOTAL = sum of the lines: cells give 1970463, printed 1960463 (difference -10000)
  - sgt1923 p.440 (f942) hab_sub_cc Grombalia: c_tot = c_land + c_build: cells give 158610, printed 168610 (difference 10000)
  - sgt1923 p.440 (f942) hab_sub_cc c_tot: TOTAL = sum of the lines: cells give 1970463, printed 1960463 (difference -10000)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (2 printings): sgt1922 f452, sgt1923 f942.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
