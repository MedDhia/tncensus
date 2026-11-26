# GAZ — Consommations (Ville de Tunis), 1937–1939

*Gas consumption and receipts, city of Tunis, public lighting and subscribers: the years 1937–1939, printed only in sgt1939.*

Source: *Statistique générale de la Tunisie*, chapter *Communes*, editions sgt1939 (stored values). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR).

Pages and views of the stored values: sgt1939 (`bpt6k9105739w`): p. 23, f29.

Rebuild: `python3 data-raw/yearbook_other_chapters/extract_communes.py build` (transcriptions `../transcribed/communes_gasop_sgt1939.txt, section `@gastunis``). Per-check output: `communes_validation_services.json`.

Rows: 12. Years: 1937, 1938, 1939.

Continuation of `communes_gas_tunis.csv` (same columns and codes), kept in a separate file so that file stays unchanged. sgt1939 prints 1935–1939; only 1937–1939 are stored here.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number of the cell
- `gallica_view`: Gallica view (fNNNN) of the cell
- `year`: year
- `commune`: `Tunis`
- `lighting`: `public_lighting` (*Éclairage public*) or `private_lighting` (*Abonnés*: subscribers, the *Éclairage privé* of the earlier editions)
- `lighting_fr`: column heading as printed in sgt1939
- `measure`: `consumption_m3` or `receipts`
- `measure_fr`: column heading (French)
- `value`: consumption in cubic metres (integer); receipts in francs with centimes (printed » in the centimes = .00)
- `flag`: empty (no cell is flagged)

sgt1939 p. 23, view 29, lower table. Read on a native-resolution crop (0.6 scale); OCR agrees. The TOTAL GÉNÉRAL columns are not stored (row checks).

## Validation

- Row checks (public + subscribers vs total, consumption and receipts, 1935–1939): 10; failed 1:
  - sgt1939 p.23 1936 rec: public + subscribers vs total: cells give 7835770.64, printed 4835770.64 (difference -3000000.00)
  The 1936 receipts failure is the same misprint as in sgt1936 (7.835.770,64 printed 4.835.770,64), see `communes_gas_tunis.md`.
- Overlap with `communes_gas_tunis` (1935–1936, sgt1939 against every earlier printing): 18 cells compared, 18 equal.
- Cross-check with *Exploitation du gaz à Tunis* (same page): 1938 and 1939 public, subscriber and total consumption agree (see `communes_gas_operation.md`).
- Flagged cells: none.
