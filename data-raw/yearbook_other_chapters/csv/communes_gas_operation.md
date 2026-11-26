# Exploitation du gaz à Tunis

*Operation of the Tunis gas works: gas emitted, subscribers, gas consumed by use, and length of the mains in service by diameter.*

Source: *Statistique générale de la Tunisie*, chapter *Communes*, editions sgt1935, sgt1936, sgt1939 (stored values). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR).

Pages and views of the stored values: sgt1935 (`bpt6k9105653t`): p. 31, f51; sgt1936 (`bpt6k91056547`): p. 23, f34; sgt1939 (`bpt6k9105739w`): p. 23, f29.

Rebuild: `python3 data-raw/yearbook_other_chapters/extract_communes.py build` (transcriptions `../transcribed/communes_gasop_<edition>.txt`). Per-check output: `communes_validation_services.json`.

Rows: 72. Years: 1934, 1935, 1936, 1938, 1939.

Printed for two-year windows (sgt1935: 1934–1935; sgt1936: 1935–1936; sgt1939: 1938–1939): each year is taken from the latest edition printing it (rule 4); 1935, printed twice, is stored from sgt1936 and the sgt1935 printing compared. 1937 is not printed.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number of the cell
- `gallica_view`: Gallica view (fNNNN) of the cell
- `year`: year of the figures (column heading)
- `commune`: `Tunis`
- `measure`: English code of the printed line (`gas_emitted_m3`, `subscribers`, `consumed_m3_*`, `mains_length_m_diameter_<d>mm`, `mains_length_m_all_diameters`)
- `measure_fr`: line label as printed (French)
- `unit`: `m3` (mètres cubes), `m` (mètres) or `count`
- `value`: integer, in the unit as printed
- `flag`: empty (no cell is flagged)

**Tables.** sgt1935 p. 31 (view 51) *Exploitation du gaz à Tunis (1934-1935)*; sgt1936 p. 23 (view 34) and sgt1939 p. 23 (view 29) *Exploitation du gaz à Tunis*. Lines: *Émission totale de l'année en mètres cubes*; *Nombre d'abonnés au 31 décembre*; *Nombre de mètres cubes consommés*: *Éclairage public*, *— voies privées* (lighting of private roads; not printed in sgt1939), *Particuliers (tarif ordinaire)*, *Administration et divers (tarif réduit)*, *Total* (not stored, used for the check); *Longueur totale des canalisations en service au 31 décembre* by diameter 500 … 50 m/m with a *Total* (sgt1935, sgt1936; the total is not stored), or as a single figure (sgt1939, stored as `mains_length_m_all_diameters`).

**Image versus OCR.** Every cell was read on native-resolution crops (0.5–1.0 scale); the OCR (which agrees except for the sgt1936 "50" line, read "90") was a draft only.

**Overlap with `communes_gas_tunis`.** The gas consumption series (*Gaz : consommation (ville de Tunis)*) gives the same gas in two columns: its *Éclairage public* consumption equals *Éclairage public* + *voies privées* here, its *Éclairage privé* / *Abonnés* consumption equals *Particuliers* + *Administration*, and its total equals the *Total* here. These identities were checked for every year both tables print in the same edition (sgt1935: 1934, 1935; sgt1936: 1935, 1936; sgt1939: 1938, 1939; result below). Only the breakdown (voies privées; ordinary / reduced tariff), the gas emitted, the subscribers and the mains are new; receipts are only in `communes_gas_tunis`.

**sgt1939 also prints the consumption series** (*GAZ — Consommations (Ville de Tunis)*, 1935–1939, on the same page 23, view 29, headed *Éclairage public / Abonnés / Total général*), which `communes_gas_tunis.md` says is absent. Its 1935–1936 cells equal the sgt1936 printing stored there (compared below); 1937–1939 are stored in `communes_gas_tunis_1937_1939.csv`, because `communes_gas_tunis.csv` is kept unchanged. Under rule 4 the 1935–1936 rows of `communes_gas_tunis.csv` would carry `census` = sgt1939 (same values).

## Validation

- Printed totals (m3 consumed by use vs *Total*; lengths by diameter vs *Total*): 10; passed 8; failed 2:
  - sgt1936 p.23 1936: m3 consumed by use vs TOTAL: cells give 5558049, printed 5548049 (difference -10000)
  - sgt1936 p.23 1936: lengths by diameter vs TOTAL: cells give 149960, printed 150007 (difference 47)
  Both failures were re-read on a native-resolution crop and are as printed (no cell flagged): the 1936 consumption *Total* 5.548.049 is 10.000 below the sum of its lines, which the consumption series prints as 5.558.049 (in sgt1936 and sgt1939); the 1936 lengths sum to 149.960 against the printed 150.007.
- Cross-table identities with the consumption series, same edition and year: 18; passed 17; failed 1:
  - sgt1936 1936: Exploitation TOTAL vs GAZ Consommations cons_total: cells give 5548049, printed 5558049 (difference 10000)
- Overlapping printings (1935: sgt1935 and sgt1936): 22 cells compared (totals included); 0 differences.
- Note: in 1935 the 70 mm and 60 mm lines read 5.080 / 33.403 in both printings, while 1934 reads 30.996 / 5.080; kept as printed.
- Flagged cells: none.
