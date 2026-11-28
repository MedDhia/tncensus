# Distribution d'électricité, Tableau I : abonnés et énergie livrée par les réseaux à la consommation

*Electricity distribution by distributor or region (sgt1935, sgt1936, sgt1939): subscribers and energy delivered at high and low voltage by use.*

Source: *Statistique générale de la Tunisie*, chapter *Communes*, editions sgt1935, sgt1936, sgt1939 (stored values). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR).

Pages and views of the stored values: sgt1935 (`bpt6k9105653t`): p. 34, f54, p. 35, f55; sgt1936 (`bpt6k91056547`): p. 26, f37, p. 27, f38; sgt1939 (`bpt6k9105739w`): p. 26, f32, p. 27, f33.

Rebuild: `python3 data-raw/yearbook_other_chapters/extract_communes.py build` (transcriptions `../transcribed/communes_elec_<edition>.txt`). Per-check output: `communes_validation_services.json`.

Rows: 520. Years: 1935, 1936, 1939.

Printed once per edition (SPEC_ADDENDUM rule 5); no year is printed twice, so there is no overlap comparison.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number of the cell
- `gallica_view`: Gallica view (fNNNN) of the cell
- `year`: year of the figures (see below)
- `region`: distributor or region as printed (braced names joined with ' + ')
- `measure`: English code of the printed column
- `measure_fr`: column heading as printed (French), with its group heading
- `unit`: unit of `value`: `m`, `kW`, `kWh`, `count` or `francs`
- `value`: number in `unit`, as printed (decimals kept; francs with centimes); printed » = 0
- `text_fr`: text printed instead of a number (or the two figures of a double cell)
- `flag`: empty; `not_applicable` (text instead of a number: value NA); `derived_from_totals` (cell partly in the binding, solved from the row identity and checked against its legible digits); `total_mismatch` (printed value kept; a row check and a column check, or the evident line fault described below, show it inconsistent)

**Tables.** *Distribution d'électricité, Tableau I* (sgt1935 pp. 34–35, views 54–55) and the same table without a number in sgt1936 (pp. 26–27, views 37–38) and sgt1939 (pp. 26–27, views 32–33); each a two-page spread. Rows: distributors or regions (*Compagnie des Tramways de Tunis (Banlieue de Tunis et dans un rayon de 60 km. autour de Tunis)*, *Compagnie du Gaz de Tunis (à Tunis)*, … *Gafsa*). Columns: number of subscribers (*Éclairage*, *Autres usages*, *Haute tension*, *TOTAL*), and energy delivered by the networks to consumers (*Énergie livrée par les réseaux à la consommation*, kWh): high voltage (*Traction*, *Autres usages*, *Services publics*, *TOTAL*), low voltage (*Lumière et usages domestiques*, *Force*, *Éclairage(s) publics*, *Services publics*, *TOTAL*), and *TOTAL général haute et basse tension*. The TOTAL columns and the column-total line are not stored (checks). `year` = edition year (no year printed). Braced names (*Ferryville (Fourniture C. T. T.)* / *(Centrale de Ferryville)*, *Bizerte - La Pêcherie* / *Région de Bizerte*) share one line of figures and are stored under the joined label; sgt1939 instead gives Ferryville *Continu* and *Alternatif* lines and a *Région de Ferryville* line.

**HT total without traction in sgt1939.** In sgt1939 the HT TOTAL is *Autres usages* + *Services publics* only, and the *TOTAL général* = HT TOTAL + BT TOTAL, so the traction energy (8.432.247 kWh, Tramways) is in neither (sgt1935 and sgt1936 include it). The row checks follow the printed definition of each edition.

**Cells in the binding.** sgt1935 Tramways HT *Autres usages* is printed "5.900.714" with the decimal digit in the binding; sgt1939's whole HT *Autres usages* column runs into the binding, with only its leading digits legible. These cells are solved from the row identity (HT total − the other HT cells) and checked against the legible digits (all agree; listed below), flag `derived_from_totals`.

**Other particular cells.** sgt1936 Bizerte BT *Services publics* prints two figures one above the other (106.605 and 39.060, for the two braced names): stored as their sum, 145665, with the printed text in `text_fr` (the BT total 1.050.746 includes both). sgt1936 Téboursouk's BT services publics, BT total and total général are printed on the line below its name. sgt1936 Tramways subscribers print 10.185 high-voltage subscribers (total 20.370; the column total 10.338 confirms it).

**Image versus OCR.** Every cell read on native-resolution crops (each page in two bands at 0.48–0.62 scale; the binding strips of both views stitched; faint cells checked against the row totals). OCR was a draft (it misreads e.g. sgt1936 Goulette subscribers 1.496 as 1.406).

## Validation

- Checks (row totals, column-total line, solved cells against legible digits): 271; passed 252; failed 19. Every failure was re-read on a native-resolution crop; printed values are kept.
  - sgt1935 p.34 Compagnie des Tramways de Tunis (Banlieue de Tunis et dans un rayon de 60 km. autour de Tunis): sub_l + sub_o + sub_ht vs sub_t: cells give 9843, printed 9573 (difference -270)
  - sgt1935 p.34 column sub_o vs Totaux: cells give 2637, printed 2367 (difference -270)
  - sgt1936 p.26 Compagnie des Tramways de Tunis (Banlieue de Tunis et dans un rayon de 60 km. autour de Tunis): bt_dom + bt_force + bt_publight + bt_public vs bt_t: cells give 9977968.3, printed 2440894.9 (difference -7537073.4)
  - sgt1936 p.26 column bt_force vs Totaux: cells give 11059282.5, printed 3522209.1 (difference -7537073.4)
  - sgt1939 p.26 Compagnie des Tramways de Tunis (Banlieue de Tunis et dans un rayon de 60 km. autour de Tunis): bt_dom + bt_force + bt_publight + bt_public vs bt_t: cells give 2466598.1, printed 3963064.1 (difference 1496466.0)
  - sgt1939 p.26 Ferryville (Centrale de Ferryville) Alternatif: bt_dom + bt_force + bt_publight + bt_public vs bt_t: cells give 206599.7, printed 206509.7 (difference -90.0)
  - sgt1939 p.26 Bizerte — La Pêcherie + Région de Bizerte: bt_dom + bt_force + bt_publight + bt_public vs bt_t: cells give 1098749, printed 1132769 (difference 34020)
  - sgt1939 p.26 Béja: bt_dom + bt_force + bt_publight + bt_public vs bt_t: cells give 214190.0, printed 214512 (difference 322.0)
  - sgt1939 p.26 Souk-el-Khemis: bt_dom + bt_force + bt_publight + bt_public vs bt_t: cells give 59652, printed 62786 (difference 3134)
  - sgt1939 p.26 Le Kef: bt_dom + bt_force + bt_publight + bt_public vs bt_t: cells give 76364.0, printed 79863 (difference 3499.0)
  - sgt1939 p.26 Concession d'État région Souk-el-Arba, Souk-el-Khemis, Le Kef, Téboursouk: bt_dom + bt_force + bt_publight + bt_public vs bt_t: cells give 26394.0, printed 28574 (difference 2180.0)
  - sgt1939 p.26 Sahel: bt_dom + bt_force + bt_publight + bt_public vs bt_t: cells give 646829, printed 655436 (difference 8607)
  - sgt1939 p.26 Sousse: bt_dom + bt_force + bt_publight + bt_public vs bt_t: cells give 897722, printed 1035956 (difference 138234)
  - sgt1939 p.26 Kairouan: bt_dom + bt_force + bt_publight + bt_public vs bt_t: cells give 195092, printed 215277 (difference 20185)
  - sgt1939 p.26 Sfax: bt_dom + bt_force + bt_publight + bt_public vs bt_t: cells give 1306008, printed 1448686 (difference 142678)
  - sgt1939 p.26 Gabès: bt_dom + bt_force + bt_publight + bt_public vs bt_t: cells give 302733, printed 331732 (difference 28999)
  - sgt1939 p.26 Gafsa: bt_dom + bt_force + bt_publight + bt_public vs bt_t: cells give 179387, printed 192256 (difference 12869)
  - sgt1939 p.26 Totaux: bt_dom + bt_force + bt_publight + bt_public vs bt_t: cells give 17951109.7, printed 19842302.7 (difference 1891193.0)
  - sgt1939 p.26 column bt_public vs Totaux: cells give 1211346.4, printed 1211256.4 (difference -90.0)
  Pinned cells (`total_mismatch`): sgt1935 Tramways subscribers *Autres usages* 745 (row and column checks both imply 475); sgt1936 Tramways BT *Force* 8.374.526 (both imply 837.452,6); sgt1939 Ferryville *Alternatif* BT *Services publics* 27.984,6 (both imply 27.894,6). **sgt1939 BT totals:** in 12 of the 18 lines (besides Ferryville Alternatif) the BT TOTAL exceeds the sum of the four printed BT columns (Tramways by 1.496.466, Sousse 138.234, Sfax 142.678 …; the column total by 1.891.193), while each BT column agrees with its own column total, and HT TOTAL + BT TOTAL = TOTAL général on every line. The BT TOTAL therefore includes some low-voltage energy not shown in any printed column; no cell is wrong and none is flagged.
- Cells solved from the row identity (9, `derived_from_totals` except the Totaux line, which is not stored):
  - sgt1935 Compagnie des Tramways de Tunis (Banlieue de Tunis et dans un rayon de 60 km. autour de Tunis) ht_other: 5900714.5 (legible digits 5900714)
  - sgt1939 Compagnie des Tramways de Tunis (Banlieue de Tunis et dans un rayon de 60 km. autour de Tunis) ht_other: 12050484.5 (legible digits 1205048)
  - sgt1939 Compagnie du Gaz de Tunis ht_other: 4807613 (legible digits 480761)
  - sgt1939 Bizerte — La Pêcherie + Région de Bizerte ht_other: 105077 (legible digits 10507)
  - sgt1939 Concession d'État région Souk-el-Arba, Souk-el-Khemis, Le Kef, Téboursouk ht_other: 225534 (legible digits 22553)
  - sgt1939 Sahel ht_other: 69388 (legible digits 6938)
  - sgt1939 Sousse ht_other: 63275 (legible digits 6327)
  - sgt1939 Sfax ht_other: 3327706 (legible digits 332770)
  - sgt1939 Totaux ht_other: 20649077.5 (legible digits 2064907)
- Flagged cells: not_applicable 0 (text cells, see above); derived_from_totals 8; total_mismatch 3.
  - sgt1935 Compagnie des Tramways de Tunis (Banlieue de Tunis et dans un rayon de 60 km. autour de Tunis) subscribers_other = 745 (total_mismatch)
  - sgt1935 Compagnie des Tramways de Tunis (Banlieue de Tunis et dans un rayon de 60 km. autour de Tunis) kwh_high_voltage_other = 5900714.5 (derived_from_totals)
  - sgt1936 Compagnie des Tramways de Tunis (Banlieue de Tunis et dans un rayon de 60 km. autour de Tunis) kwh_low_voltage_power = 8374526 (total_mismatch)
  - sgt1939 Compagnie des Tramways de Tunis (Banlieue de Tunis et dans un rayon de 60 km. autour de Tunis) kwh_high_voltage_other = 12050484.5 (derived_from_totals)
  - sgt1939 Compagnie du Gaz de Tunis kwh_high_voltage_other = 4807613 (derived_from_totals)
  - sgt1939 Ferryville (Centrale de Ferryville) Alternatif kwh_low_voltage_public_services = 27984.6 (total_mismatch)
  - sgt1939 Bizerte — La Pêcherie + Région de Bizerte kwh_high_voltage_other = 105077 (derived_from_totals)
  - sgt1939 Concession d'État région Souk-el-Arba, Souk-el-Khemis, Le Kef, Téboursouk kwh_high_voltage_other = 225534 (derived_from_totals)
  - sgt1939 Sahel kwh_high_voltage_other = 69388 (derived_from_totals)
  - sgt1939 Sousse kwh_high_voltage_other = 63275 (derived_from_totals)
  - sgt1939 Sfax kwh_high_voltage_other = 3327706 (derived_from_totals)
