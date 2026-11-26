# Droits d'abatage (slaughter dues)

*Slaughter dues collected by each commune: tariff per head and sums collected for each kind of animal, and the total collected.*

Source: *Statistique générale de la Tunisie*, chapter *Communes*, table d) *Droits d'abatage perçus en <année>*, editions sgt1923. Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR).

Pages and views of the stored values: sgt1923 (`bpt6k9105649x`): p. 34, f536, p. 35, f537, p. 36, f538, p. 37, f539, p. 38, f540, p. 39, f541.

Rebuild: `python3 data-raw/yearbook_other_chapters/extract_communes.py build` (transcriptions `../transcribed/communes_slaughter_<edition>.txt`).

Rows: 963. Printed once per edition (SPEC_ADDENDUM rule 5); `year` = the year in the heading.

**Coverage: only sgt1923 (1923) is transcribed.** The table is printed in every edition sgt1922–sgt1930 (sgt1922 views 58–59; sgt1923 536–541; sgt1924 1024–1029; sgt1925 58–63; sgt1926 606–611; sgt1927 70–75; sgt1928 594–599, view 595 nearly blank in the OCR and to be checked; sgt1929 70–75; sgt1930 602–607) and not in sgt1935–sgt1939. The other eight editions are not done yet. sgt1922 uses a different, denser layout (one spread, many communes taxing per kilogram with the rate printed across the row).

## Columns

- `census`, `table_id`, `gallica_ark`, `source_page`, `gallica_view`, `year`: as in the other files (left page: beef to goat; right page: pig to camel and the total)
- `commune`: as printed
- `animal`: `beef` (Bœuf), `veal` (Veau), `sheep` (Mouton et agneaux), `goat` (Chèvre [et chevreaux]), `pig` (Porc), `horse` (Chevaux et mulets), `other` (Autres), `camel` (Chameau); `all` for a total stored on its own (see below)
- `animal_fr`: column heading (French)
- `measure`: `tariff_per_head` (*Tarif par tête*, francs), `sums_collected` (*Sommes perçues*, francs), `total_collected` (*Totaux*)
- `value`: francs; printed » = 0. Tariffs as printed ("0 15" = 0.15)
- `text_fr`: text printed in place of a tariff (e.g. "0,10 par kg", "1,00-1,20")
- `flag`: empty, `not_applicable` (tariff printed as text: value NA, text in `text_fr`), `illegible`

The row *Totaux* is stored only for communes whose dues are not itemised by animal (all sums » and the total printed, i.e. dues levied per kilogram: Ferryville, Gabès, La Goulette, Hammam-Lif, Mahdia, Mateur, Souk-el-Arba, Souk-el-Khemis, Sousse; and Bizerte, where only pigs are itemised, 6.180 of 118.241,40): `animal` = `all`, `measure` = `total_collected`. For the other communes it equals the sum of the animals and is used for the check only. The page totals (*A reporter*, *Report*, *Totaux*) are not stored.

**Image versus OCR.** All three spreads were read on native-resolution crops of both pages stitched at the same height (0.55–0.85 scale, every line), with separate full-scale strips of the goat column, which runs into the binding (its last digits repeat on the gutter of the right page) and of the pig tariff column; Gallica's OCR served as a draft only. Every failed check was re-read on a crop.

Observations column (printed text, translated): Bizerte (sgt1923): *La perception a lieu à raison de 0 fr. 05 par kil. poids vif, sauf pour les porcs qui paient 10 fr. par tête.*; Ferryville (sgt1923): *Pour 233.483 kil. 500 de viande.*; Gabès (sgt1923): *0 fr. 15 par kilo de viande abattue.*; Goulette (La) (sgt1923): *Droits perçus au kilo.*; Maharès (sgt1923): *Taxes instituées en 1924.*; Mateur (sgt1923): *6 fr. par 100 kil. pour toutes catégories d'animaux.*; Medjez-el-Bab (sgt1923): *Affermés.*; Sidi-bou-Saïd (sgt1923): *0 fr. 15 par kilo.*; Souk-el-Arba (sgt1923): *0 fr. 10 par kilo.*; Souk-el-Khemis (sgt1923): *0 fr. 09 par kilo.*; Sousse (sgt1923): *0 fr. 15 par kilo.*. (Béja: dues at 0 fr. 05 per kg live weight except pigs, 10 fr. per head; the others: rate per kilogram of meat, *Affermés* = farmed out, *Taxes instituées en 1924* = dues introduced in 1924.)

## Validation

- Checks: 85 (each itemised row against its *Totaux*; every column of each page against the *A reporter* / *Totaux* line, with the carried *Report*); passed 69; failed 16. Each failure was re-read on the image and the printed values are kept (e.g. Tunis 8,50 × … 329.970 + … = 536.346,35 printed 518.346,35; Tebourba 4.540 printed 3.540; La Marsa 9.954,60 printed 10.854,60):

  - sgt1923 p.34 Aïn-Draham: sums vs Totaux: cells give 2598.05, printed 2598.15 (difference 0.10)
  - sgt1923 p.36 Kalaa-Kebira: sums vs Totaux: cells give 979.50, printed 979.30 (difference -0.20)
  - sgt1923 p.36 Kef (Le): sums vs Totaux: cells give 19371.65, printed 19707.35 (difference 335.70)
  - sgt1923 p.36 Marsa (La): sums vs Totaux: cells give 9954.60, printed 10854.60 (difference 900.00)
  - sgt1923 p.36 Médenine: sums vs Totaux: cells give 3200.80, printed 3197.80 (difference -3.00)
  - sgt1923 p.36 A reporter goat_s: cells give 50082.83, printed 50073.83 (difference -9.00)
  - sgt1923 p.36 A reporter total: cells give 492663.62, printed 492654.62 (difference -9.00)
  - sgt1923 p.38 Nefta: sums vs Totaux: cells give 3623.50, printed 3622.50 (difference -1.00)
  - sgt1923 p.38 Sfax: sums vs Totaux: cells give 114290.10, printed 114390 (difference 99.90)
  - sgt1923 p.38 Sidi-bou-Saïd: sums vs Totaux: cells give 9188.30, printed 9187.30 (difference -1.00)
  - sgt1923 p.38 Tabarka: sums vs Totaux: cells give 3204.00, printed 3204.05 (difference 0.05)
  - sgt1923 p.38 Tebourba: sums vs Totaux: cells give 4540, printed 3540 (difference -1000)
  - sgt1923 p.38 Tunis: sums vs Totaux: cells give 536346.35, printed 518346.35 (difference -18000.00)
  - sgt1923 p.38 Totaux veal_s: cells give 25599.45, printed 25594.45 (difference -5.00)
  - sgt1923 p.38 Totaux goat_s: cells give 88930.58, printed 88925.56 (difference -5.02)
  - sgt1923 p.38 Totaux total: cells give 1306690.67, printed 1306790.67 (difference 100.00)

- Flagged cells: not_applicable: 3.
  - sgt1923 Ferryville beef tariff_per_head: not_applicable (printed "0,10 par kg")
  - sgt1923 Grombalia sheep tariff_per_head: not_applicable (printed "1,00-1,20")
  - sgt1923 Grombalia goat tariff_per_head: not_applicable (printed "0,60-0,50")
