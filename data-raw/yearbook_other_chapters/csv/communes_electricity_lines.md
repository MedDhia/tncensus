# Distribution d'électricité, Tableau II : longueurs des lignes

*Length of the high- and low-voltage lines by power station and town or region electrified (sgt1935, sgt1936, sgt1939).*

Source: *Statistique générale de la Tunisie*, chapter *Communes*, editions sgt1935, sgt1936, sgt1939 (stored values). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR).

Pages and views of the stored values: sgt1935 (`bpt6k9105653t`): p. 36, f56; sgt1936 (`bpt6k91056547`): p. 25, f36; sgt1939 (`bpt6k9105739w`): p. 25, f31.

Rebuild: `python3 data-raw/yearbook_other_chapters/extract_communes.py build` (transcriptions `../transcribed/communes_elec_<edition>.txt`). Per-check output: `communes_validation_services.json`.

Rows: 108. Years: 1935, 1936, 1939.

Printed once per edition (SPEC_ADDENDUM rule 5); no year is printed twice, so there is no overlap comparison.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number of the cell
- `gallica_view`: Gallica view (fNNNN) of the cell
- `year`: year of the figures (see below)
- `centrale`: power station as printed
- `area`: town or region electrified, as printed
- `measure`: English code of the printed column
- `measure_fr`: column heading as printed (French), with its group heading
- `unit`: unit of `value`: `m`, `kW`, `kWh`, `count` or `francs`
- `value`: number in `unit`, as printed (decimals kept; francs with centimes); printed » = 0
- `text_fr`: text printed instead of a number (or the two figures of a double cell)
- `flag`: empty; `not_applicable` (text instead of a number: value NA); `derived_from_totals` (cell partly in the binding, solved from the row identity and checked against its legible digits); `total_mismatch` (printed value kept; a row check and a column check, or the evident line fault described below, show it inconsistent)

**Tables.** *Distribution d'électricité, Tableau II* (sgt1935 p. 36, view 56), and the same table without a number in sgt1936 (p. 25, view 36) and sgt1939 (p. 25, view 31): length of the lines (*Longueurs des lignes*, metres) at high voltage (*Haute tension*) and low voltage (*Basse tension*), by power station (*Centrales*, braced over the towns it serves) and town or region electrified (*Villes ou régions électrifiées*). Column totals (and in sgt1936 a grand total HT + BT, 2.168.093) are not stored. `year` = edition year (no year printed). sgt1935 braces *Bizerte-Pêcherie* and *Région de Bizerte* into one line (joined label); sgt1936 and sgt1939 give them separately.

**Image versus OCR.** Every cell read on native-resolution crops (0.45–0.5 scale); OCR was a draft only (it is poor on sgt1939).

## Validation

- Checks (row totals, column-total line, solved cells against legible digits): 7; passed 7; failed 0. Every failure was re-read on a native-resolution crop; printed values are kept.
- Flagged cells: not_applicable 0 (text cells, see above).
