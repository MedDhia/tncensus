# Ventes avec obligation de planter. a) Propriétés livrées à la colonisation (autorisations de planter ; ventes définitives)

*Sales with an obligation to plant: planting authorisations and definitive sales by year, region and nationality of the beneficiaries (1913-1923).*

Source: *Statistique générale de la Tunisie*, chapter *Colonisation*, editions sgt1922, sgt1923. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 425, f449; sgt1923 (`bpt6k9105649x`): p. 435, f937, p. 437, f939.

Transcriptions: `../transcribed/colonisation_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_colonisation.py build`.

Rows: 360. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923.

Units: number of concessions / sales and hectares (`unit`); suggested value_type: mixed.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (rule 4 tables: the latest edition printing that year)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (yearly lists) or the edition year (cumulative recapitulations: state at the edition date, period in `period_fr`)
- `operation`: `planting_authorisation` (autorisations de planter) or `definitive_sale` (ventes définitives)
- `operation_fr`: printed table heading
- `property_fr`: nom de la propriété ou désignation des régions, as printed (`Extrême-Sud : Telmine` for the braced 1919 line; empty for a néant line)
- `controle_civil`: contrôle civil as printed (`Territ. milit.` = territoires militaires; a ditto '—' is resolved to the line above; empty for a néant line)
- `note_fr`: `néant` when the year is printed with » in every cell
- `nationality`: `french`, `other_european`, `indigenous` (concessionaires / buyers)
- `nationality_fr`: printed column heading
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `row_realigned` (printed on the neighbouring line, stored on its own line)

Old layout printed only in sgt1922 and sgt1923 (chapter XIII); from sgt1924 the chapter is reorganised (installation / planting / urban lists, recapitulation by origin of the land) and this table is no longer printed. Printed total lines and total columns are checks only (not stored); » = 0.

Autorisations de planter (sgt1922 f446|f447, 1913-1922; sgt1923 f936|f937, 1913-1923) and ventes définitives (sgt1922 f448|f449, 1913-1922; sgt1923 f938|f939, 1914-1923), by année de la concession / de la vente, nom de la propriété ou désignation des régions, contrôle civil, and Français / autres Européens / indigènes (number, hectares). The TOTAL columns are checked on every line. Years printed » in every cell are kept as rows with value 0, empty property and `note_fr` = `néant`.

Relation to `colonisation_planting_lots`: not the same table. That file (sgt1924-sgt1935, *b) Terres à planter*) lists lotissements of land to plant by year with area and number of lots; this one lists authorisations and definitive sales of the old *obligation de planter* regime (mostly terres sialines of Sfax and the South) by nationality, which the later editions no longer print. It is therefore a new file rather than an extension.

Row realignment: in both editions the Français area 99 ha of the 1917 Maknassy sale is printed one line down, on the Sbeïtla line (Maknassy: 1 sale, area », total 1 sale / 99 ha; Sbeïtla: Français », 99; indigènes 1 / 8 ha; total 1 / 8 ha); it is stored on the Maknassy line, flag `row_realigned`.

Every failed check below was re-read on a native-resolution crop: the printed values are kept. 1917 Terres sialines (Sfax) ventes définitives: Français 6.313 ha + indigènes 324 ha = 6.637 ha, printed TOTAL 6.037 ha in both editions (zoomed crops); the faulty cell (a Français area 5.713 or the total) cannot be identified, so nothing is flagged.

Survey of the whole chapter in every edition: `colonisation_survey.md`.

## Validation

- Checks against printed totals and identities: 226; passed: 224; failed: 2.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.424 (f448) plant_sale 1917 / Terres sialines / Sfax: tot_ha = fr_ha + eu_ha + ind_ha: cells give 6637, printed 6037 (difference -600)
  - sgt1923 p.436 (f938) plant_sale 1917 / Terres sialines / Sfax: tot_ha = fr_ha + eu_ha + ind_ha: cells give 6637, printed 6037 (difference -600)

- Overlapping printings: 318 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: row_realigned: 1.

  - sgt1923 p.437 1917 definitive_sale / Gafsa / french / area / hectares = 99 (row_realigned)

## Image versus OCR

- Read cell by cell on the page images (4 printings): sgt1922 f446, sgt1922 f448, sgt1923 f936, sgt1923 f938.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
