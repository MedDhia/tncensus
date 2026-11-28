# Navigation : mouvement des navires, a) par port

*Navigation: movement of ships, by port.*

Source: *Statistique générale de la Tunisie*, chapter *Commerce et navigation*, editions sgt1922, sgt1923, sgt1924. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 404, f428, p. 405, f429; sgt1923 (`bpt6k9105649x`): p. 416, f918, p. 417, f919; sgt1924 (`bpt6k9105649x`): p. 432, f1422, p. 433, f1423.

Transcriptions: `../transcribed/commerce_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_commerce.py build`.

Rows: 630. Years: 1922, 1923, 1924.

Units: as printed (ships, tonneaux de jauge, tonnes, passengers, head). value_type: count.

Selection: each edition prints a single year; no overlap.

## Columns

- `census`: edition (each edition prints one year, its reference year)
- `table_id`: `navigation_a` (Mouvement des navires, a) Par port)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the movement (not printed in the heading; the reference year of the edition, confirmed by c) sur le littoral)
- `port`: port as printed
- `movement`: `entries` or `exits`
- `movement_fr`: as printed
- `measure`: `ships`, `tonnage`, `goods`, `passengers`, `livestock`
- `measure_fr`: column as printed
- `unit`: `ships`, `tons register` (tonneaux de jauge), `tonnes`, `persons`, `head`
- `value`: as printed (» stored as 0)
- `flag`: empty or `total_mismatch` (see notes)

Movement of ships by port (21 ports, printed in order of importance, which changes from one edition to the next): ships, register tonnage, tonnes of goods, passengers and head of livestock, entries and exits. The printed *Entrées et sorties réunies* block and the TOTAUX line are not stored; they were used as checks (entries + exits = combined on every line and measure; lines = TOTAUX).

Year: the heading prints no year. Each edition prints the movement of its reference year (sgt1922: 1922, sgt1923: 1923, sgt1924: 1924); the TOTAUX of entries agree with the yearly series c) *sur le littoral* of the same edition (see `commerce_navigation_yearly`). The editions do not overlap.

Gutter: the entries livestock column (Têtes de bétail) lies against the binding on the left page (repeated, cut, at the edge of the right page in sgt1923 and sgt1924); every cell was read on the crop and equals combined minus exits. sgt1922: the exits ships TOTAUX is partly hidden (`?` in the transcription; check only).

Explanation of the failed checks (each cell re-read on a zoomed native-resolution crop; in every case the line check and the column check fail by the same amount, which locates the misprint, flagged `total_mismatch`): sgt1922 Tunis-Goulette S.tonnage: printed 1.454.848; entries + exits = combined and the column TOTAUX both give 1.434.848; sgt1923 Tabarka S.goods: printed 9.550; the combined line and the column TOTAUX both give 9.553; sgt1924 Sfax S.tonnage: printed 353.802; the combined line and the column TOTAUX both give 953.802; sgt1924 Bizerte E.passengers: printed 3.303; the combined line and the column TOTAUX both give 8.303; sgt1922 Italien.mixtes E.tonnage: printed 8.534; combined - exits and the column TOTAUX give 6.534; sgt1922 Italien.voiliers S.passengers: printed 667; combined - entries gives 657 (column TOTAUX agrees with the next two corrections); sgt1922 Tunisien.voiliers S.passengers: printed 3.452; combined - entries gives 8.452 (with the previous cell the column TOTAUX 68.349 is reached); sgt1922 Yougo-Slave.vapeurs S.tonnage: printed 58.216; combined - entries and the column TOTAUX give 68.216; sgt1922 Suédois.vapeurs S.goods: printed 14.184; combined - entries gives 14.180; sgt1922 Japonais.vapeurs S.goods: printed 14.726; combined - entries gives 14.720 (with the previous cell the column TOTAUX 3.015.888 is reached).

Survey of the whole chapter: `commerce_survey.md`.

## Validation

- Checks against printed totals and identities: 373; passed: 365; failed: 8.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 S.tonnage: sum of lines = Totaux: cells give 3227897, printed 3207897 (difference -20000)
  - sgt1922 Tunis-Goulette tonnage: entries + exits = combined: cells give 2906962, printed 2886962 (difference -20000)
  - sgt1923 S.goods: sum of lines = Totaux: cells give 3626901, printed 3626904 (difference 3)
  - sgt1923 Tabarka goods: entries + exits = combined: cells give 11065, printed 11068 (difference 3)
  - sgt1924 S.tonnage: sum of lines = Totaux: cells give 2881106, printed 3481106 (difference 600000)
  - sgt1924 Sfax tonnage: entries + exits = combined: cells give 1308499, printed 1908499 (difference 600000)
  - sgt1924 E.passengers: sum of lines = Totaux: cells give 63316, printed 68316 (difference 5000)
  - sgt1924 Bizerte passengers: entries + exits = combined: cells give 11796, printed 16796 (difference 5000)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: total_mismatch: 4.

  - sgt1922 p.405 1922 Tunis-Goulette / exits / tonnage / tons register = 1454848 (total_mismatch)
  - sgt1923 p.417 1923 Tabarka / exits / goods / tonnes = 9550 (total_mismatch)
  - sgt1924 p.433 1924 Sfax / exits / tonnage / tons register = 353802 (total_mismatch)
  - sgt1924 p.432 1924 Bizerte / entries / passengers / persons = 3303 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (6 printings): sgt1922 f428, sgt1922 f429, sgt1923 f918, sgt1923 f919, sgt1924 f1422, sgt1924 f1423.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
