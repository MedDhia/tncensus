# a) Électricité : longueur des canalisations ; puissance des installations ; abonnés ; consommation ; produits

*Electricity by locality (sgt1929, sgt1930): length of the network, installed power at 31 December, subscribers, kilowatt-hours consumed and gross receipts.*

Source: *Statistique générale de la Tunisie*, chapter *Communes*, editions sgt1929, sgt1930 (stored values). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR).

Pages and views of the stored values: sgt1929 (`bpt6k9105652d`): p. 52, f80, p. 53, f81; sgt1930 (`bpt6k9105652d`): p. 54, f612, p. 55, f613.

Rebuild: `python3 data-raw/yearbook_other_chapters/extract_communes.py build` (transcriptions `../transcribed/communes_elec_<edition>.txt`). Per-check output: `communes_validation_services.json`.

Rows: 1190. Years: 1929, 1930.

Printed once per edition (SPEC_ADDENDUM rule 5); no year is printed twice, so there is no overlap comparison.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number of the cell
- `gallica_view`: Gallica view (fNNNN) of the cell
- `year`: year of the figures (see below)
- `locality`: locality as printed
- `measure`: English code of the printed column
- `measure_fr`: column heading as printed (French), with its group heading
- `unit`: unit of `value`: `m`, `kW`, `kWh`, `count` or `francs`
- `value`: number in `unit`, as printed (decimals kept; francs with centimes); printed » = 0
- `text_fr`: text printed instead of a number (or the two figures of a double cell)
- `flag`: empty; `not_applicable` (text instead of a number: value NA); `derived_from_totals` (cell partly in the binding, solved from the row identity and checked against its legible digits); `total_mismatch` (printed value kept; a row check and a column check, or the evident line fault described below, show it inconsistent)

**Tables.** sgt1929 pp. 52–53 (views 80–81) and sgt1930 pp. 54–55 (views 612–613), each a two-page spread headed *a) Électricité : longueur des canalisations ; puissance des installations ; abonnés ; consommation ; produits* in the *Éclairage* pages. Left page: locality, length (mètres), power of the installations in service at 31 December (kW: *Éclairage*, *Autres usages*, *TOTAL*), subscribers (*Éclairage*, *Autres usages*, *TOTAL*), kWh consumed by private customers (*Particuliers*: *Éclairage*, *Force*). Right page: kWh consumed by the town (*Ville*: *Éclairage*, *Force*), kWh *TOTAL*, gross receipts (*Produits bruts*: Particuliers Éclairage / Force, Ville Éclairage / Force, *TOTAL*, francs), *Redevance à la ville et droit de contrôle* and *Droits d'occupation des sous-sols* (francs). The row totals (power, subscribers, kWh, receipts) are not stored; they are used for the row checks. No column totals are printed. `year` = the year of the power heading (*au 31 décembre 1929 / 1930*), taken for the whole table.

**Units.** Length in metres as printed ("160.700" = 160 700 m; sgt1929 prints some short lengths as "0.850" = 850 m, as the table header says *mètres*); power in kW as printed (Mateur 1929 "236.92" kept as 236.92 kW; Sfax 1929 prints 1.384.490 / 1.002.600 / 2.387.090 and Gabès 221.260 / 5.500 / 226.760, apparently watts, kept as printed); kWh with one decimal where printed; francs with centimes.

**Text cells.** In sgt1929 several localities print a text across the consumption and receipts columns instead of figures: La Goulette *Région Bac compris dans Djebel-Djelloud*, Ste-Monique and Archevêché *Compris dans Sidi-bou-Saïd*, La Soukra and Cherguia *Compris dans Montplaisir*, Forgemol *Compris dans Le Bardo*, Mégrine *Compris dans Djebel-Djelloud* (consumption counted with that locality); Salammbo's town lighting *Compris dans Carthage* and Dermech's *id.*: each covered cell is NA, `not_applicable`, with the text in `text_fr`. Hammam-Lif and Mornag are braced in the kWh and receipts columns (sgt1929): those cells are stored under `Hammam-Lif et Mornag`. sgt1930 braces Ste-Monique, Sidi-bou-Saïd, Archevêché and La Soukra, Chergula in all columns (one row each, joined label).

**sgt1930 layout faults.** (1) The kWh *Force* column of view 612 curves into the binding and its lower lines sit up to half a line above their names; they were assigned in order and every line was confirmed by kWh TOTAL − the three other kWh cells (St-Germain "4 8" = 4,8 kWh). (2) In the power columns, from Beni-Khalled the TOTAL column runs one line late (Beni-Khalled 12 + » printed 13 = Beni-Khiar's total; Fondouk-Djedid 2 + » printed 12 …), and the lighting cells of Oued-Sahil and Bizerte carry 550 and 221.260 (Bizerte 550 + 400 = 950, its printed total; 221.260 is Gabès's 1929 figure, a line of type left standing). Printed values are stored; Oued-Sahil and Bizerte lighting power are flagged `total_mismatch`.

**Image versus OCR.** Every cell was read on native-resolution crops (each page in three bands at 0.62–0.7 scale, the label column stitched to the value columns; small-type kWh cells at 2–5×). The OCR was used as a draft and to locate lines. Doubtful reading: sgt1929 Tunis kWh *Particuliers Force* "3.467,748 8" in condensed type (stored 3467748.8); a reading 3.167.748,8 would reduce Tunis's kWh row failure from 300.230,8 to 230,8, but the glyph matches the 4 of "748".

## Validation

- Checks (row totals, column-total line, solved cells against legible digits): 302; passed 272; failed 30. Every failure was re-read on a native-resolution crop; printed values are kept.
  - sgt1929 p.52 Tunis: kwh_pl + kwh_pf + kwh_vl + kwh_vf vs kwh_t: cells give 9145969.8, printed 8845739.0 (difference -300230.8)
  - sgt1929 p.52 Carthage: kwh_pl + kwh_pf + kwh_vl + kwh_vf vs kwh_t: cells give 29006.3, printed 29606.3 (difference 600.0)
  - sgt1929 p.52 Carthage: rec_pl + rec_pf + rec_vl + rec_vf vs rec_t: cells give 59815.61, printed 59575.01 (difference -240.60)
  - sgt1929 p.52 St-Henri: rec_pl + rec_pf + rec_vl + rec_vf vs rec_t: cells give 69967.39, printed 69867.30 (difference -100.09)
  - sgt1929 p.52 Djebel-Djelloud: kwh_pl + kwh_pf + kwh_vl + kwh_vf vs kwh_t: cells give 1600394.0, printed 1600314.0 (difference -80.0)
  - sgt1929 p.52 Hammam-Lif et Mornag: rec_pl + rec_pf + rec_vl + rec_vf vs rec_t: cells give 714115.13, printed 714116.13 (difference 1.00)
  - sgt1929 p.52 Bizerte: rec_pl + rec_pf + rec_vl + rec_vf vs rec_t: cells give 1077443.45, printed 1076443.45 (difference -1000.00)
  - sgt1929 p.52 Mateur: rec_pl + rec_pf + rec_vl + rec_vf vs rec_t: cells give 292562.52, printed 22562.52 (difference -270000.00)
  - sgt1929 p.52 Zarzouna: kwh_pl + kwh_pf + kwh_vl + kwh_vf vs kwh_t: cells give 2484.00, printed 3084.00 (difference 600.00)
  - sgt1929 p.52 Béja: rec_pl + rec_pf + rec_vl + rec_vf vs rec_t: cells give 353929.89, printed 353923.89 (difference -6.00)
  - sgt1929 p.52 Sousse: kwh_pl + kwh_pf + kwh_vl + kwh_vf vs kwh_t: cells give 723925.00, printed 323925.00 (difference -400000.00)
  - sgt1929 p.52 Sousse: rec_pl + rec_pf + rec_vl + rec_vf vs rec_t: cells give 1514954.17, printed 1494954.17 (difference -20000.00)
  - sgt1929 p.52 Sfax: kwh_pl + kwh_pf + kwh_vl + kwh_vf vs kwh_t: cells give 1437120.90, printed 527120.9 (difference -910000.00)
  - sgt1929 p.52 Sfax: rec_pl + rec_pf + rec_vl + rec_vf vs rec_t: cells give 2221011.68, printed 2221811.68 (difference 800.00)
  - sgt1930 p.54 La Goulette: pw_l + pw_o vs pw_t: cells give 613, printed 663 (difference 50)
  - sgt1930 p.54 Tunis: kwh_pl + kwh_pf + kwh_vl + kwh_vf vs kwh_t: cells give 10093568.0, printed 10090268 (difference -3300.0)
  - sgt1930 p.54 La Soukra, Chergula: rec_pl + rec_pf + rec_vl + rec_vf vs rec_t: cells give 132496.33, printed 132496.30 (difference -0.03)
  - sgt1930 p.54 Mornag: rec_pl + rec_pf + rec_vl + rec_vf vs rec_t: cells give 75868.75, printed 67868.75 (difference -8000.00)
  - sgt1930 p.54 Soliman: kwh_pl + kwh_pf + kwh_vl + kwh_vf vs kwh_t: cells give 8556.9, printed 8556.6 (difference -0.3)
  - sgt1930 p.54 Menzel-bou-Zelfa: kwh_pl + kwh_pf + kwh_vl + kwh_vf vs kwh_t: cells give 5456.8, printed 6456.8 (difference 1000.0)
  - sgt1930 p.54 Beni-Khalled: pw_l + pw_o vs pw_t: cells give 12, printed 13 (difference 1)
  - sgt1930 p.54 Fondouk-Djedid: pw_l + pw_o vs pw_t: cells give 2, printed 12 (difference 10)
  - sgt1930 p.54 Creteville: pw_l + pw_o vs pw_t: cells give 4, printed 2 (difference -2)
  - sgt1930 p.54 Cebala du Mornag: pw_l + pw_o vs pw_t: cells give 3, printed 4 (difference 1)
  - sgt1930 p.54 Oued-Sahil: pw_l + pw_o vs pw_t: cells give 550, printed 3 (difference -547)
  - sgt1930 p.54 Bizerte: pw_l + pw_o vs pw_t: cells give 221660, printed 950 (difference -220710)
  - sgt1930 p.54 Bizerte: kwh_pl + kwh_pf + kwh_vl + kwh_vf vs kwh_t: cells give 462910.0, printed 522910.0 (difference 60000.0)
  - sgt1930 p.54 Ferryville: sub_l + sub_o vs sub_t: cells give 337, printed 327 (difference -10)
  - sgt1930 p.54 Ferryville: kwh_pl + kwh_pf + kwh_vl + kwh_vf vs kwh_t: cells give 108211.8, printed 108210.0 (difference -1.8)
  - sgt1930 p.54 Sousse: rec_pl + rec_pf + rec_vl + rec_vf vs rec_t: cells give 1593608.21, printed 1593598.21 (difference -10.00)
  The failures are in the print: e.g. sgt1929 Mateur receipts TOTAL 22.562,52 (= its town-lighting cell) for 292.562,52, Sousse kWh TOTAL 323.925 for 723.925, Sfax 527.120,9 for 1.437.120,9; sgt1930 the power-column line fault described above (Beni-Khalled to Bizerte). Except for the two sgt1930 lighting cells, no stored cell can be singled out (only row totals are printed), so none is flagged.
- Flagged cells: not_applicable 72 (text cells, see above); total_mismatch 2.
  - sgt1930 Oued-Sahil installed_power_lighting_kw = 550 (total_mismatch)
  - sgt1930 Bizerte installed_power_lighting_kw = 221260 (total_mismatch)
