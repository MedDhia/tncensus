# Habous. Autres cessions (cessions à enzel). a) Propriétés cédées

*Habous: other cessions (perpetual leases à enzel) by year, by group of beneficiaries and kind of habous.*

Source: *Statistique générale de la Tunisie*, chapter *Colonisation*, editions sgt1922, sgt1923. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 429, f453; sgt1923 (`bpt6k9105649x`): p. 441, f943.

Transcriptions: `../transcribed/colonisation_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_colonisation.py build`.

Rows: 132. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923.

Units: count and francs (`unit`); suggested value_type: mixed.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (rule 4 tables: the latest edition printing that year)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (yearly lists) or the edition year (cumulative recapitulations: state at the edition date, period in `period_fr`)
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

sgt1922 f453 (1913-1922), sgt1923 f943 (1914-1923), both printed sideways (rotated for reading). Français / autres Européens et indigènes × habous publics / privés: nombre de cessions, montant global des rentes d'enzel, montant global du capital. The total général columns (habous publics et privés) are checks only.

Every failed check below was re-read on a native-resolution crop: the printed values are kept. 1918: total général nombre de cessions printed 14 for 4 + 1 + 8 + 4 = 17 (both editions; the rent and capital totals add up). The faulty cell cannot be identified; nothing is flagged.

Survey of the whole chapter in every edition: `colonisation_survey.md`.

## Validation

- Checks against printed totals and identities: 60; passed: 58; failed: 2.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.429 (f453) enzel 1918: tot_n = fpub_n + fpriv_n + opub_n + opriv_n: cells give 17, printed 14 (difference -3)
  - sgt1923 p.441 (f943) enzel 1918: tot_n = fpub_n + fpriv_n + opub_n + opriv_n: cells give 17, printed 14 (difference -3)

- Overlapping printings: 108 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (2 printings): sgt1922 f453, sgt1923 f943.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
