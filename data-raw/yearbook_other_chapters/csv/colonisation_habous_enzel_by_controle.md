# Habous. Autres cessions (cessions à enzel). b) Récapitulation et répartition par contrôle civil

*Habous: cessions à enzel since 1886, by contrôle civil, group of beneficiaries and kind of habous.*

Source: *Statistique générale de la Tunisie*, chapter *Colonisation*, editions sgt1922, sgt1923. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 430, f454, p. 431, f455; sgt1923 (`bpt6k9105649x`): p. 442, f944, p. 443, f945.

Transcriptions: `../transcribed/colonisation_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_colonisation.py build`.

Rows: 456. Years: 1922, 1923.

Units: count and francs (`unit`); suggested value_type: mixed.

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
- `buyer`: `french` or `other_european_and_indigenous` (printed groups)
- `buyer_fr`: printed column heading
- `habous`: `public` or `private` habous
- `habous_fr`: printed column heading
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `row_realigned` (printed on the neighbouring line, stored on its own line)

Old layout printed only in sgt1922 and sgt1923 (chapter XIII); from sgt1924 the chapter is reorganised (installation / planting / urban lists, recapitulation by origin of the land) and this table is no longer printed. Printed total lines and total columns are checks only (not stored); » = 0.

sgt1922 f454|f455 (1886-1922; f455 printed sideways) and sgt1923 f944|f945 (1886-1923). sgt1923 adds the 1923 cessions to Tunis and to the totals; the 1923 Français cession and the autres Européens et indigènes cessions of 1923 are all counted in Tunis. The Français habous privés capital column and the autres Européens habous publics count column run into the gutter but are legible on the crops.

Survey of the whole chapter in every edition: `colonisation_survey.md`.

## Validation

- Checks against printed totals and identities: 150; passed: 150; failed: 0.

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (2 printings): sgt1922 f454, sgt1923 f944.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
