# Navigation : mouvement des navires, b) par pavillons

*Navigation: movement of ships, by flag.*

Source: *Statistique générale de la Tunisie*, chapter *Commerce et navigation*, editions sgt1922, sgt1923, sgt1924. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 406, f430, p. 407, f431; sgt1923 (`bpt6k9105649x`): p. 418, f920, p. 419, f921; sgt1924 (`bpt6k9105649x`): p. 434, f1424, p. 435, f1425.

Transcriptions: `../transcribed/commerce_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_commerce.py build`.

Rows: 980. Years: 1922, 1923, 1924.

Units: as printed (ships, tonneaux de jauge, tonnes, passengers, head). value_type: count.

Selection: each edition prints a single year; no overlap.

## Columns

- `census`: edition (each edition prints one year, its reference year)
- `table_id`: `navigation_b` (Mouvement des navires, b) Par pavillons)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the movement (not printed in the heading; the reference year of the edition, confirmed by c) sur le littoral)
- `ship_flag`: flag (nationality) of the ships, English code
- `ship_flag_fr`: pavillon as printed
- `propulsion`: `steam`, `sail`, `mixed`
- `propulsion_fr`: vapeurs, voiliers, mixtes (as printed)
- `movement`: `entries` or `exits`
- `movement_fr`: as printed
- `measure`: `ships`, `tonnage`, `goods`, `passengers`, `livestock`
- `measure_fr`: column as printed
- `unit`: `ships`, `tons register` (tonneaux de jauge), `tonnes`, `persons`, `head`
- `value`: as printed (» stored as 0)
- `flag`: empty or `total_mismatch` (see notes)

Movement of ships by flag (pavillon, in order of importance) and propulsion (vapeurs = steam, voiliers = sail, mixtes = mixed): ships, register tonnage, tonnes of goods, passengers, head of livestock, entries and exits. Only the flag / propulsion lines printed are stored (27 lines in sgt1922, 35 in sgt1923, 36 in sgt1924; a line printed with » throughout, e.g. Canadien entries 1924, is stored as 0). The *Entrées et sorties réunies* block and the TOTAUX are checks only; the TOTAUX are also compared with those of a) par port.

Year: not printed; the reference year of each edition (1922, 1923, 1924), as for a) par port. No overlap between editions.

Gutter: the entries livestock column lies against the binding; every cell read on the crop and equal to combined minus exits.

Explanation of the failed checks (every cell re-read on a zoomed native-resolution crop): (i) sgt1922 prints 9.092 as the entries ships TOTAUX, against 9.062 for the sum of the lines, the TOTAUX of a) par port and combined (18.038) - exits (8.976): a misprinted total (not stored). (ii) sgt1924 prints 3.818.475 as the combined tonnage of French steamers, for 2.818.475 = entries + exits, and the combined TOTAUX agrees with 2.818.475: a misprint in the combined block (not stored). (iii) the remaining failures locate six misprinted sgt1922 cells, flagged `total_mismatch`: Italien.mixtes E.tonnage: printed 8.534; combined - exits and the column TOTAUX give 6.534; Italien.voiliers S.passengers: printed 667; combined - entries gives 657 (column TOTAUX agrees with the next two corrections); Tunisien.voiliers S.passengers: printed 3.452; combined - entries gives 8.452 (with the previous cell the column TOTAUX 68.349 is reached); Yougo-Slave.vapeurs S.tonnage: printed 58.216; combined - entries and the column TOTAUX give 68.216; Suédois.vapeurs S.goods: printed 14.184; combined - entries gives 14.180; Japonais.vapeurs S.goods: printed 14.726; combined - entries gives 14.720 (with the previous cell the column TOTAUX 3.015.888 is reached).

Survey of the whole chapter: `commerce_survey.md`.

## Validation

- Checks against printed totals and identities: 594; passed: 579; failed: 15.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 E.ships: sum of lines = Totaux: cells give 9062, printed 9092 (difference 30)
  - sgt1922 Totaux ships: entries + exits = combined: cells give 18068, printed 18038 (difference -30)
  - sgt1922 E.tonnage: sum of lines = Totaux: cells give 3225861, printed 3223861 (difference -2000)
  - sgt1922 S.tonnage: sum of lines = Totaux: cells give 3197897, printed 3207897 (difference 10000)
  - sgt1922 Italien.mixtes tonnage: entries + exits = combined: cells give 15068, printed 13068 (difference -2000)
  - sgt1922 Yougo-Slave.vapeurs tonnage: entries + exits = combined: cells give 124987, printed 134987 (difference 10000)
  - sgt1922 S.goods: sum of lines = Totaux: cells give 3015898, printed 3015888 (difference -10)
  - sgt1922 Suédois.vapeurs goods: entries + exits = combined: cells give 26927, printed 26923 (difference -4)
  - sgt1922 Japonais.vapeurs goods: entries + exits = combined: cells give 14726, printed 14720 (difference -6)
  - sgt1922 S.passengers: sum of lines = Totaux: cells give 63359, printed 68349 (difference 4990)
  - sgt1922 Italien.voiliers passengers: entries + exits = combined: cells give 1179, printed 1169 (difference -10)
  - sgt1922 Tunisien.voiliers passengers: entries + exits = combined: cells give 12036, printed 17036 (difference 5000)
  - sgt1922 E.ships: TOTAUX by flag = TOTAUX by port: cells give 9062, printed 9092 (difference 30)
  - sgt1924 R.tonnage: sum of lines = Totaux: cells give 7973863, printed 6973863 (difference -1000000)
  - sgt1924 Français.vapeurs tonnage: entries + exits = combined: cells give 2818475, printed 3818475 (difference 1000000)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: total_mismatch: 6.

  - sgt1922 p.407 1922 italy / sail / exits / passengers / persons = 667 (total_mismatch)
  - sgt1922 p.406 1922 italy / mixed / entries / tonnage / tons register = 8534 (total_mismatch)
  - sgt1922 p.407 1922 yugoslavia / steam / exits / tonnage / tons register = 58216 (total_mismatch)
  - sgt1922 p.407 1922 tunisia / sail / exits / passengers / persons = 3452 (total_mismatch)
  - sgt1922 p.407 1922 sweden / steam / exits / goods / tonnes = 14184 (total_mismatch)
  - sgt1922 p.407 1922 japan / steam / exits / goods / tonnes = 14726 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (6 printings): sgt1922 f430, sgt1922 f431, sgt1923 f920, sgt1923 f921, sgt1924 f1424, sgt1924 f1425.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
