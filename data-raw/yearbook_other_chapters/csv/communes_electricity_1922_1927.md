# a) Électricité : longueur des canalisations ; puissance des installations ; abonnés ; consommation ; produits

*Electricity by locality, earlier layout (sgt1922–sgt1927): length of the network, installed power at 31 December (hectowatts), subscribers, kilowatt-hours consumed (private customers, public lighting) and gross receipts (private customers, town).*

Source: *Statistique générale de la Tunisie*, chapter *Communes*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927 (stored values). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR).

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 38, f62, p. 39, f63; sgt1923 (`bpt6k9105649x`): p. 42, f544, p. 43, f545; sgt1924 (`bpt6k9105649x`): p. 42, f1032, p. 43, f1033; sgt1925 (`bpt6k9105650k`): p. 42, f66, p. 43, f67; sgt1926 (`bpt6k9105650k`): p. 50, f614, p. 51, f615; sgt1927 (`bpt6k91056510`): p. 50, f78, p. 51, f79.

Rebuild: `python3 data-raw/yearbook_other_chapters/extract_communes.py build` (transcriptions `../transcribed/communes_elec_<edition>.txt`). Sections `@elec22`. Per-check output: `communes_validation_elec_1922_1928.json`.

Rows: 561. Years: 1922, 1923, 1924, 1925, 1926, 1927.

Printed once per edition (SPEC_ADDENDUM rule 5); no year is printed twice, so there is no overlap comparison. Same table, other layouts: the later layouts are in `communes_electricity_1928.csv` (sgt1928) and `communes_electricity_networks.csv` (sgt1929–sgt1930).

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
- `unit`: unit of `value`: `m` (metres), `hW` (hectowatts, as headed), `kWh`, `count` or `francs`
- `value`: number in `unit`, as printed (decimals kept; francs with centimes); printed » or *Néant* = 0
- `text_fr`: word printed with or instead of a number
- `flag`: empty; `not_applicable` (text instead of a number: value NA); `derived_from_totals` (cell partly hidden, solved from the row identity and checked on its legible digits); `illegible` (value NA); `total_mismatch` (printed value kept)

**Tables.** Lower half of the *Service des eaux* page (left) and of the *Gaz* page (right) under the heading *Éclairage*: sgt1922 pp. 38–39 (views 62–63, 7 localities), sgt1923 pp. 42–43 (views 544–545, 6), sgt1924 pp. 42–43 (views 1032–1033, 6), all in `bpt6k9105649x`; sgt1925 pp. 42–43 (views 66–67, 7) and sgt1926 pp. 50–51 (views 614–615, 8), in `bpt6k9105650k`; sgt1927 pp. 50–51 (views 78–79, 17), in `bpt6k91056510`. Left page: locality, length of the network (*Longueur des canalisations*, mètres), power of the installations in service at 31 December (*Éclairage*, *Autres usages*, *TOTAL*, headed *hectowats*), number of subscribers (*Éclairage*, *Autres usages*, *TOTAL*). Right page: kilowatt-hours consumed (*Nombre de kilowats-heures consommés*: *Particuliers*, *Éclairage public*, *TOTAL*), gross receipts (*Produits bruts*: *Particuliers*, *Ville*, *TOTAL*, fr. c.), *Redevance à la ville et droit de contrôle* and *Droit d'occupation du sous-sol* (fr. c.). The column set is the same in all six editions (sgt1928 changes it: `communes_electricity_1928.csv`). The TOTAL columns are not stored (row checks). No column totals and no footnotes are printed.

**Year.** The power heading reads *au 31 décembre* with no year, and no other year is printed in the table; `year` is the edition year, as for the water sales (*Recettes en 1922*, …) and the gas table printed beside it, which run to the edition year.

**Units.** Length in metres as printed ("144.870" = 144 870 m); power in hectowatts as headed, with a decimal digit where printed (sgt1925 Ferryville 49,5 and 94,5; Sfax 7.528,3 / 1.264,8 / 8.793,1); kWh as printed, with the decimals of sgt1924–sgt1925 (kWh printed with a centimes-like sub-column, e.g. Sfax 220.535,30); francs with centimes; printed » = 0. **sgt1927 Bizerte power** is printed 4.975.820 / 2.626 / 4.278.446, a thousand times the 3.200–3.700 hW of the earlier years: apparently watts (like Sfax and Gabès in sgt1929), kept as printed in `hW`.

**Particular cells.** sgt1922: the subscribers TOTAL column runs into the binding, only its leading digits legible (Tunis "9.4" …); each is checked on those digits against the sum of its parts (all agree; listed below). sgt1924: the kWh *Particuliers* column curves into the binding; Tunis "(4.)449.733" (leading 4 faint on the curve and repeated on the edge of the facing view). sgt1926: Tunis *Redevance* "482.337 05" with the word *majoration* printed beneath it (value stored, word in `text_fr`); Tunis length "157.26?" with a broken last digit, read 157.260 (the OCR gives "157.26>"; lengths have no check). sgt1926 is faintly printed throughout; its summed figures are confirmed by the row totals, which all agree.

**Image versus OCR.** Every cell was read on native-resolution crops of `hires.py` pages (each page at 0.6–1.1 scale, the binding strips of both views stitched at 1–1.2×, every failing or doubtful cell at 1.3–4×). The Gallica OCR was used only as a cross-check; it agrees with every figure it reads except its own misreadings (e.g. sgt1922 Ferryville kWh 69.300 for 62.300, Sfax 118.888 for 178.888; sgt1926 Bizerte length 32.107 for 32.407). No stored value rests on the OCR alone.

## Validation

- Checks (row totals; TOTAL cells partly in the binding, on their legible digits): 204; passed 190; failed 14. Every failure was re-read on a native-resolution crop; printed values are kept.

| edition | rows | checks | failed |
|---|---|---|---|
| sgt1922 | 77 | 28 | 1 |
| sgt1923 | 66 | 24 | 4 |
| sgt1924 | 66 | 24 | 4 |
| sgt1925 | 77 | 28 | 2 |
| sgt1926 | 88 | 32 | 0 |
| sgt1927 | 187 | 68 | 3 |

Failed checks:

  - sgt1922 p.39 La Goulette: rec_p + rec_v vs rec_t: cells give 105399.31, printed 105399.23 (difference -0.08)
  - sgt1923 p.43 Tunis: rec_p + rec_v vs rec_t: cells give 5190051.19, printed 5190051.09 (difference -0.10)
  - sgt1923 p.42 Ferryville: pw_l + pw_o vs pw_t: cells give 820, printed 770 (difference -50)
  - sgt1923 p.42 Sousse: sub_l + sub_o vs sub_t: cells give 1120, printed 1122 (difference 2)
  - sgt1923 p.43 Sfax: kwh_p + kwh_pub vs kwh_t: cells give 280267, printed 208267 (difference -72000)
  - sgt1924 p.42 Tunis: pw_l + pw_o vs pw_t: cells give 82479, printed 82481 (difference 2)
  - sgt1924 p.43 Tunis: kwh_p + kwh_pub vs kwh_t: cells give 4635957, printed 4635997 (difference 40)
  - sgt1924 p.43 Tunis: rec_p + rec_v vs rec_t: cells give 4939282.10, printed 4939282.00 (difference -0.10)
  - sgt1924 p.43 Sfax: kwh_p + kwh_pub vs kwh_t: cells give 319466.99, printed 319446.99 (difference -20.00)
  - sgt1925 p.42 Tunis: sub_l + sub_o vs sub_t: cells give 13812, printed 13882 (difference 70)
  - sgt1925 p.43 Bizerte: rec_p + rec_v vs rec_t: cells give 490728.70, printed 540728.70 (difference 50000.00)
  - sgt1927 p.51 Tunis: rec_p + rec_v vs rec_t: cells give 11008600.12, printed 11008598.12 (difference -2.00)
  - sgt1927 p.50 Bizerte: pw_l + pw_o vs pw_t: cells give 4978446, printed 4278446 (difference -700000)
  - sgt1927 p.51 Gabès: kwh_p + kwh_pub vs kwh_t: cells give 20031, printed 20631 (difference 600)
  Each failure was re-read at 1.3–4×: the stored cells are as printed and only a row total is printed, so no stored cell can be singled out and none is flagged. Several look like misprints of the TOTAL (sgt1923 Sfax kWh 208.267 for 280.267; sgt1925 Bizerte receipts 540.728,70 for 490.728,70) or of a part (sgt1927 Bizerte lighting power 4.975.820 where the TOTAL implies 4.275.820).
- TOTAL cells partly in the binding, checked on their legible digits (7; not stored): sgt1922 Tunis sub_t "949…" = sum 9495 (agrees); sgt1922 Bizerte sub_t "109…" = sum 1098 (agrees); sgt1922 Ferryville sub_t "22…" = sum 225 (agrees); sgt1922 Sousse sub_t "97…" = sum 972 (agrees); sgt1922 Sfax sub_t "106…" = sum 1063 (agrees); sgt1922 Béja sub_t "29…" = sum 294 (agrees); sgt1922 La Goulette sub_t "38…" = sum 389 (agrees).
- Flagged cells: none.
