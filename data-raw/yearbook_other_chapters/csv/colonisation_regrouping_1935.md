# Opérations de regroupement réalisées au 31 décembre 1935 ; Réinstallations effectuées sur des propriétés achetées par le Domaine

*Regrouping of colonisation lotissements at 31 December 1935: lots taken back, settlers reinstalled, and reinstallations on properties bought by the Domaine.*

Source: *Statistique générale de la Tunisie*, chapter *Colonisation*, editions sgt1935. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1935 (`bpt6k9105653t`): p. 278, f298, p. 279, f299.

Transcriptions: `../transcribed/colonisation_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_colonisation.py build`.

Rows: 204. Years: 1935.

Units: count and hectares; suggested value_type: mixed.

Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept (`census` = edition); the figures are the state at the edition date and are revised between editions.

## Columns

- `census`: edition the value is taken from (rule 4 tables: the latest edition printing that year)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `operation`: `regrouping` or `reinstallation_domain_purchases`
- `operation_fr`: printed table title
- `lotissement_fr`: printed table title
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible`, `not_applicable`, `total_mismatch`, `ocr_corrected`

Printed in sgt1935 only (f298-f299). Footnote (1): the regrouping programme of the rural colonisation lotissements is in progress. Lots taken back printed as sums for Djebel-Mansour (1 + 6 = 7) and Ousseltia (2 + 13 = 15): the results are stored. The second table's TOTAUX difference "151 (2)" is not a column sum (footnote (2): lots available for the enlargement programme) and is stored as `lotissement_fr` = `TOTAL (printed)`. Checks: différence = repris - réinstallés on every line, A reporter / Report / TOTAUX.

Every failed check below was re-read on a native-resolution crop: the printed values are kept. Réinstallations: TOTAUX superficie 6.825,28 ha for lines summing to 6.725,28 (every line re-read; the same areas are printed in sgt1936's installation list; the recapitulation of sgt1935 repeats 6.825,28).

Survey of the whole chapter in every edition: `colonisation_survey.md`.

## Validation

- Checks against printed totals and identities: 56; passed: 55; failed: 1.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1935 p.279 (f299) reinstall area: Totaux = sum: cells give 6725.28, printed 6825.28 (difference 100.00)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (3 printings): sgt1935 f298, sgt1935 f299, sgt1935 f299.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
