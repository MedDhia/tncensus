# Ventes avec obligation de planter. b) Récapitulation et répartition par contrôle civil

*Sales with an obligation to plant: planting authorisations and definitive sales since 1893, by contrôle civil and nationality.*

Source: *Statistique générale de la Tunisie*, chapter *Colonisation*, editions sgt1922, sgt1923. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 426, f450, p. 427, f451; sgt1923 (`bpt6k9105649x`): p. 438, f940, p. 439, f941.

Transcriptions: `../transcribed/colonisation_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_colonisation.py build`.

Rows: 144. Years: 1922, 1923.

Units: number and hectares (`unit`); suggested value_type: mixed.

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
- `operation`: `planting_authorisation` (autorisations de planter) or `definitive_sale` (ventes définitives)
- `operation_fr`: printed table heading
- `nationality`: `french`, `other_european`, `indigenous` (concessionaires / buyers)
- `nationality_fr`: printed column heading
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `row_realigned` (printed on the neighbouring line, stored on its own line)

Old layout printed only in sgt1922 and sgt1923 (chapter XIII); from sgt1924 the chapter is reorganised (installation / planting / urban lists, recapitulation by origin of the land) and this table is no longer printed. Printed total lines and total columns are checks only (not stored); » = 0.

sgt1922 f450|f451 (1893-1922) and sgt1923 f940|f941 (1893-1923, upper halves). sgt1923 reprints every sgt1922 figure unchanged although its yearly list adds 1923 sales (Terres sialines, Maknassy, Sbeïtla, Extrême-Sud): the recapitulation was not updated. The authorisations TOTAL count column runs into the gutter (check only; legible digits agree with the line sums).

Every failed check below was re-read on a native-resolution crop: the printed values are kept. Ventes définitives, indigènes, superficie: the TOTAL line prints 47.063 ha for lines summing to 47.103 (both editions); every line adds up to its printed total and the printed grand total 142.694 equals the sum of the lines, so the faulty figure is the printed column total 47.063.

Survey of the whole chapter in every edition: `colonisation_survey.md`.

## Validation

- Checks against printed totals and identities: 88; passed: 84; failed: 4.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.426 (f450) plant_cc TOTAL: s_tot_ha = s_fr_ha + s_eu_ha + s_ind_ha: cells give 142654, printed 142694 (difference 40)
  - sgt1922 p.426 (f450) plant_cc s_ind_ha: TOTAL = sum of the lines: cells give 47103, printed 47063 (difference -40)
  - sgt1923 p.438 (f940) plant_cc TOTAL: s_tot_ha = s_fr_ha + s_eu_ha + s_ind_ha: cells give 142654, printed 142694 (difference 40)
  - sgt1923 p.438 (f940) plant_cc s_ind_ha: TOTAL = sum of the lines: cells give 47103, printed 47063 (difference -40)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (2 printings): sgt1922 f450, sgt1923 f940.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
