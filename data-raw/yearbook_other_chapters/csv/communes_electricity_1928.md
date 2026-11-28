# a) Électricité : longueur des canalisations ; puissance des installations ; abonnés ; consommation ; produits

*Electricity by locality, sgt1928: length of the network, installed power at 31 December 1928, subscribers, kilowatt-hours consumed and gross receipts, each split by private customers / town and lighting / power.*

Source: *Statistique générale de la Tunisie*, chapter *Communes*, editions sgt1928 (stored values). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR).

Pages and views of the stored values: sgt1928 (`bpt6k91056510`): p. 50, f602, p. 51, f603.

Rebuild: `python3 data-raw/yearbook_other_chapters/extract_communes.py build` (transcriptions `../transcribed/communes_elec_<edition>.txt`). Sections `@elec28`. Per-check output: `communes_validation_elec_1922_1928.json`.

Rows: 255. Years: 1928.

Printed once per edition (SPEC_ADDENDUM rule 5); no year is printed twice, so there is no overlap comparison. Same table, other layouts: the earlier layout is in `communes_electricity_1922_1927.csv`, the later one (sgt1929–sgt1930) in `communes_electricity_networks.csv`.

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
- `unit`: unit of `value`: `m` (metres), `kW` (as headed, *Kws*), `kWh`, `count` or `francs`
- `value`: number in `unit`, as printed (decimals kept; francs with centimes); printed » or *Néant* = 0
- `text_fr`: word printed with or instead of a number
- `flag`: empty; `not_applicable` (text instead of a number: value NA); `derived_from_totals` (cell partly hidden, solved from the row identity and checked on its legible digits); `illegible` (value NA); `total_mismatch` (printed value kept)

**Table.** sgt1928 pp. 50–51 (views 602–603, `bpt6k91056510`), lower half of the *Service des eaux* page (left) and of the *Gaz* page (right): 17 localities. The column set is that of sgt1929–sgt1930 (`communes_electricity_networks.csv`), and the measure codes are the same: left page: locality, length (mètres), power of the installations in service at 31 December 1928 (*Éclairage*, *Autres usages*, *TOTAL*, headed *Kws*), subscribers (*Éclairage*, *Autres usages*, *TOTAL*), kWh consumed (*Kilowatheures consommés*) by private customers (*Particuliers*: *Éclairage*, *Force*); right page: kWh *Ville* (*Éclairage*, *Force*), kWh *TOTAL*, *Produits bruts* (Particuliers Éclairage / Force, Ville Éclairage / Force, *TOTAL*, francs), *Redevance à la ville et droit de contrôle*, *Droits d'occupation des sous-sols*. The TOTAL columns are not stored (row checks). No column totals and no footnotes are printed. `year` = 1928, the year of the power heading.

**Units.** Length in metres; power in kW as headed (*Kws*), kept as printed although the figures look like hectowatts or watts (Tunis 122.468 + 43.418 = 165.886 Kws; sgt1929 prints 13.693 + 5.068 kW for Tunis); kWh with one decimal where printed (decimal comma, thousands point); francs with centimes. Printed » and *Néant* = 0.

**Particular cells.** The kWh *Particuliers Force* column (view 602, against the binding) is set progressively higher than its lines, the last entries about half a line high; its 17 entries were assigned in order and each is confirmed by its kWh row total (all rows check except Ariana, below). Tunis kWh *Particuliers Éclairage* 7.469.424 and Béja 1.279.977 are in smaller type (confirmed by the row totals). St-Germain kWh *Ville Éclairage* is printed "2.114 5" (2.114,5).

**Image versus OCR.** Every cell was read on native-resolution crops (each page in two parts at 0.9–1.0 scale; every failing or doubtful cell at 1.8–3×). The Gallica OCR agrees with every figure it reads; it misses the kWh *Particuliers Force* column, which rests on the image (and the row totals) only.

## Validation

- Checks (row totals; TOTAL cells partly in the binding, on their legible digits): 68; passed 63; failed 5. Every failure was re-read on a native-resolution crop; printed values are kept.

| edition | rows | checks | failed |
|---|---|---|---|
| sgt1928 | 255 | 68 | 5 |

Failed checks:

  - sgt1928 p.50 Carthage: sub_l + sub_o vs sub_t: cells give 88, printed 98 (difference 10)
  - sgt1928 p.50 Hammam-Lif: pw_l + pw_o vs pw_t: cells give 695707, printed 595707 (difference -100000)
  - sgt1928 p.50 Hammam-Lif: sub_l + sub_o vs sub_t: cells give 717, printed 617 (difference -100)
  - sgt1928 p.51 Ariana: kwh_pl + kwh_pf + kwh_vl + kwh_vf vs kwh_t: cells give 72578.5, printed 72578.0 (difference -0.5)
  - sgt1928 p.51 La Marsa: rec_pl + rec_pf + rec_vl + rec_vf vs rec_t: cells give 342602.46, printed 342512.46 (difference -90.00)
  Each failure was re-read at 1.8–3×; the stored cells are as printed and none can be singled out (only row totals are printed), so none is flagged.
- Flagged cells: none.
