# Production d'électricité

*Electricity production by power station (sgt1935, sgt1936, sgt1939): installed power and energy of steam turbines and internal-combustion engines, maximum power produced.*

Source: *Statistique générale de la Tunisie*, chapter *Communes*, editions sgt1935, sgt1936, sgt1939 (stored values). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR).

Pages and views of the stored values: sgt1935 (`bpt6k9105653t`): p. 32, f52; sgt1936 (`bpt6k91056547`): p. 24, f35; sgt1939 (`bpt6k9105739w`): p. 24, f30.

Rebuild: `python3 data-raw/yearbook_other_chapters/extract_communes.py build` (transcriptions `../transcribed/communes_elec_<edition>.txt`). Per-check output: `communes_validation_services.json`.

Rows: 135. Years: 1935, 1936, 1939.

Printed once per edition (SPEC_ADDENDUM rule 5); no year is printed twice, so there is no overlap comparison.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number of the cell
- `gallica_view`: Gallica view (fNNNN) of the cell
- `year`: year of the figures (see below)
- `centrale`: power station as printed
- `measure`: English code of the printed column
- `measure_fr`: column heading as printed (French), with its group heading
- `unit`: unit of `value`: `m`, `kW`, `kWh`, `count` or `francs`
- `value`: number in `unit`, as printed (decimals kept; francs with centimes); printed » = 0
- `text_fr`: text printed instead of a number (or the two figures of a double cell)
- `flag`: empty; `not_applicable` (text instead of a number: value NA); `derived_from_totals` (cell partly in the binding, solved from the row identity and checked against its legible digits); `total_mismatch` (printed value kept; a row check and a column check, or the evident line fault described below, show it inconsistent)

**Tables.** *Production d'électricité*: sgt1935 p. 32 (view 52; view 53, given in the scope as part of the table, is a blank page), sgt1936 p. 24 (view 35), sgt1939 p. 24 (view 30). Rows: power stations (*Centrale de La Goulette, de Ferryville, de Bizerte, de Béja, de Souk-el-Arba, de Sousse, de Sfax, de Gabès, de Gafsa*). Columns: *Production thermique d'énergie électrique* by steam turbines (*Turbines à vapeur*: installed power of the plants, kW; energy supplied to the networks at the plant terminals, kWh) and by internal-combustion engines (*Moteurs à combustion interne*: same two columns), and *Production totale d'énergie électrique aux bornes de sortie de l'usine* (installed power, kW; maximum power produced, kW; energy produced, kWh). The total installed power and total energy are row totals (not stored); the column-total line is not stored either. Only La Goulette has steam turbines.

**Year.** No year is printed in the headings; `year` is the edition year (1935, 1936, 1939), as for the other once-per-edition tables of these editions. Printed once per edition (rule 5), so there is no overlap.

**Image versus OCR.** Every cell read on native-resolution crops (0.45–0.6 scale). The OCR was a draft; it misreads sgt1936 46.914.360 as 40.914.300 and 1.692.517 as 1.092.517.

## Validation

- Checks (row totals, column-total line, solved cells against legible digits): 81; passed 79; failed 2. Every failure was re-read on a native-resolution crop; printed values are kept.
  - sgt1939 p.24 Totaux: st_kwh + ic_kwh vs tot_kwh: cells give 70715636, printed 68715636 (difference -2000000)
  - sgt1939 p.24 column tot_kwh vs Totaux: cells give 70715636, printed 68715636 (difference -2000000)
  sgt1939: the printed column total of the energy produced, 68.715.636 kWh, is 2.000.000 below the sum of the stations (70.715.636) and below the sum of its own line (57.966.290 + 12.749.346); it is a total line (not stored), so no stored cell is flagged.
- Flagged cells: not_applicable 0 (text cells, see above).
