# Habous. Cessions par substitution aux droits du domaine. a) Propriétés cédées

*Habous: properties ceded by substitution for the rights of the Domaine, by year, with and without a colonisation clause.*

Source: *Statistique générale de la Tunisie*, chapter *Colonisation*, editions sgt1922, sgt1923. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 428, f452; sgt1923 (`bpt6k9105649x`): p. 440, f942.

Transcriptions: `../transcribed/colonisation_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_colonisation.py build`.

Rows: 88. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923.

Units: count, hectares and francs (`unit`); suggested value_type: mixed.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (rule 4 tables: the latest edition printing that year)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (yearly lists) or the edition year (cumulative recapitulations: state at the edition date, period in `period_fr`)
- `clause`: `without_colonisation_clause` / `with_colonisation_clause`
- `clause_fr`: printed column heading
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `row_realigned` (printed on the neighbouring line, stored on its own line)

Old layout printed only in sgt1922 and sgt1923 (chapter XIII); from sgt1924 the chapter is reorganised (installation / planting / urban lists, recapitulation by origin of the land) and this table is no longer printed. Printed total lines and total columns are checks only (not stored); » = 0.

sgt1922 f452 (1913-1922), sgt1923 f942 (1914-1923). The printed valeur globale des immeubles (= valeur foncière + valeur des constructions) is a check only. 1920 sans clause: 3 properties, 532 ha, valeur foncière 48.388 fr. but valeur globale printed » in both editions.

Every failed check below was re-read on a native-resolution crop: the printed values are kept. 1920 sans clause de colonisation: valeur globale printed » for valeur foncière 48.388 and constructions » (both editions; the valeur globale column is a check only).

Survey of the whole chapter in every edition: `colonisation_survey.md`.

## Validation

- Checks against printed totals and identities: 40; passed: 38; failed: 2.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.428 (f452) hab_sub 1920: s_tot = s_land + s_build: cells give 48388, printed 0 (difference -48388)
  - sgt1923 p.440 (f942) hab_sub 1920: s_tot = s_land + s_build: cells give 48388, printed 0 (difference -48388)

- Overlapping printings: 72 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (2 printings): sgt1922 f452, sgt1923 f942.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
