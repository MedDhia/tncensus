# Service botanique. b) Vente de semences de variétés pédigrées

*Botanical service: sales of pedigree seed, by variety and season (kilogrammes).*

Source: *Statistique générale de la Tunisie*, chapter *Institutions d'enseignement et de recherches*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 254, f278; sgt1923 (`bpt6k9105649x`): p. 267, f769; sgt1924 (`bpt6k9105649x`): p. 283, f1273; sgt1925 (`bpt6k9105650k`): p. 315, f339; sgt1926 (`bpt6k9105650k`): p. 285, f849; sgt1927 (`bpt6k91056510`): p. 283, f311; sgt1928 (`bpt6k91056510`): p. 287, f839; sgt1929 (`bpt6k9105652d`): p. 288, f316; sgt1930 (`bpt6k9105652d`): p. 295, f853.

Transcriptions: `../transcribed/research_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_research.py build`.

Rows: 715. Years: 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930.

Unit: kilogrammes; value_type: count (weight in kg).

Selection (SPEC_ADDENDUM rule 4): each cell is stored once, from the latest edition printing it; every other printing of the same cell is compared below.

## Columns

- `census`: source edition (`sgt1922` ... `sgt1939`)
- `table_id`: section code of the transcription
- `gallica_ark`: Gallica volume ark
- `source_page`: printed page number
- `gallica_view`: Gallica view
- `year`: year of the figure (for a school year or season: the year it ends; for promotions and once-per-edition tables: the edition year)
- `crop_group`: crop heading as printed (Blés durs, Blés tendres, Orges, Avoines)
- `season`: season (année) as printed
- `variety`: variety as printed
- `unit`: unit of the line (francs, persons, analyses, doses, flacons, cc, tubes, ampoules, litres, samples, quintals, hectares, producers, count)
- `value`: printed figure (» = 0)
- `flag`: empty, or ocr_corrected / illegible / total_mismatch / derived_from_totals / not_applicable / reprint_corrected / row_realigned

The first column groups several seasons as printed (e.g. 1910-17); `year` is its last year. Total par variété and the Totaux lines are checks only.

Every failed check below was re-read on a zoomed native-resolution crop: they are printed inconsistencies (printed values kept). Row totals printed wrongly, cells agreeing with the neighbouring editions: sgt1922 Hamira (10.320 for 10.380), sgt1923 Autres variétés (6.690 for 6.670), sgt1922 Richelle hâtive (44.702 for 47.702), sgt1924 Biskri glabre (6.550 for 6.450), Hamira (11.260 for 11.360), Avoines de Perse (100 for 300), sgt1925 Azizi (2.355 for 1.355); sgt1924 Totaux of 1923-24 (11.725 for 11.825; sgt1925 prints 11.825). sgt1924 Adjini: the first column 2.750 (carried on in sgt1925-sgt1927) exceeds sgt1923 1.350 + 800 = 2.150 by 600, and the row total 3.640 fits neither; printed, kept unflagged as the faulty figure cannot be told. Cells contradicting the neighbouring editions are flagged total_mismatch (sgt1923/1924 Mekki first column, sgt1927 Biskri glabre 1910-22 3.360 for 3.350). sgt1926 and sgt1927, season 1925-26: Huguenot prints 500 and Jenah Rhetifa 50, whereas both row totals (3.441, 4.400) need 550 and 0; both cells are flagged total_mismatch. sgt1928-sgt1930 carry the Huguenot/Jenah Rhetifa 1925-26 cells (flagged in every printing) and the Biskri glabre first-column error (3.860, 6.460, 8.810, flagged); sgt1929 first column Sbéi 8.175 and Souri 14.705 (for 8.195, 14.765; carried in sgt1930 as 8.885, 15.205), flagged. Printed row or column totals only: sgt1928 Blés durs Totaux 1910-23 (92.555 for 92.955), Florence (7.830 for 7.810), Blés tendres Totaux 1927-28 (8.800 for 8.880, repeated in sgt1929 and sgt1930); sgt1928 Medjerdah 1910-23 360 against 300 everywhere else (flagged); sgt1929 Huguenot (3.814 for 3.841, repeated in sgt1930), de Laconie (1.150); sgt1930 three Blés tendres row totals printed one line off (Pusa Florence 67.097, Richelle hâtive 2.740, Richelle tardive 1.190), Autres variétés 2.500 for 2.590, Blés tendres Totaux 1910-25 128.782 for 118.782, Avoines Crême 113.460 for 121.770, de Laconie 1.400 for 1.250, Totaux 1929-30 1.800 for 1.300.

Survey of the whole chapter in every edition: `research_survey.md`.

## Validation

- Checks against printed totals and identities: 482; passed: 438; failed: 44.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.254 (f278) bot_seedsales [Blés durs] Hamira: total = sum: cells give 10380, printed 10320 (difference -60)
  - sgt1922 p.254 (f278) bot_seedsales [Blés tendres] Richelle hâtive: total = sum: cells give 47702, printed 44702 (difference -3000)
  - sgt1923 p.267 (f769) bot_seedsales [Blés durs] Mekki: total = sum: cells give 5455, printed 4855 (difference -600)
  - sgt1923 p.267 (f769) bot_seedsales [Blés durs] Autres variétés: total = sum: cells give 6670, printed 6690 (difference 20)
  - sgt1923 p.267 (f769) bot_seedsales [Blés durs] 1910-18: lines vs Totaux: cells give 54150, printed 53550 (difference -600)
  - sgt1924 p.283 (f1273) bot_seedsales [Blés durs] Adjini: total = sum: cells give 4340, printed 3640 (difference -700)
  - sgt1924 p.283 (f1273) bot_seedsales [Blés durs] Biskri glabre: total = sum: cells give 6450, printed 6550 (difference 100)
  - sgt1924 p.283 (f1273) bot_seedsales [Blés durs] Hamira: total = sum: cells give 11360, printed 11260 (difference -100)
  - sgt1924 p.283 (f1273) bot_seedsales [Blés durs] Mekki: total = sum: cells give 7005, printed 6905 (difference -100)
  - sgt1924 p.283 (f1273) bot_seedsales [Blés durs] 1910-19: lines vs Totaux: cells give 63850, printed 63150 (difference -700)
  - sgt1924 p.283 (f1273) bot_seedsales [Blés durs] 1924: lines vs Totaux: cells give 11825, printed 11725 (difference -100)
  - sgt1924 p.283 (f1273) bot_seedsales [Avoines] de Perse: total = sum: cells give 300, printed 100 (difference -200)
  - sgt1925 p.315 (f339) bot_seedsales [Blés durs] Azizi: total = sum: cells give 1355, printed 2355 (difference 1000)
  - sgt1926 p.285 (f849) bot_seedsales [Blés durs] Huguenot: total = sum: cells give 3391, printed 3441 (difference 50)
  - sgt1926 p.285 (f849) bot_seedsales [Blés durs] Jenah Rhetifa: total = sum: cells give 4450, printed 4400 (difference -50)
  - sgt1927 p.283 (f311) bot_seedsales [Blés durs] Biskri glabre: total = sum: cells give 12810, printed 12800 (difference -10)
  - sgt1927 p.283 (f311) bot_seedsales [Blés durs] Huguenot: total = sum: cells give 3841, printed 3891 (difference 50)
  - sgt1927 p.283 (f311) bot_seedsales [Blés durs] Jenah Rhetifa: total = sum: cells give 4450, printed 4400 (difference -50)
  - sgt1927 p.283 (f311) bot_seedsales [Blés durs] 1910-22: lines vs Totaux: cells give 81270, printed 81260 (difference -10)
  - sgt1928 p.287 (f839) bot_seedsales [Blés durs] Biskri glabre: total = sum: cells give 15720, printed 15710 (difference -10)
  - sgt1928 p.287 (f839) bot_seedsales [Blés durs] Huguenot: total = sum: cells give 3841, printed 3891 (difference 50)
  - sgt1928 p.287 (f839) bot_seedsales [Blés durs] Jenah Rhetifa: total = sum: cells give 4450, printed 4400 (difference -50)
  - sgt1928 p.287 (f839) bot_seedsales [Blés durs] 1910-23: lines vs Totaux: cells give 92955, printed 92555 (difference -400)
  - sgt1928 p.287 (f839) bot_seedsales [Blés tendres] Florence: total = sum: cells give 7810, printed 7830 (difference 20)
  - sgt1928 p.287 (f839) bot_seedsales [Blés tendres] 1928: lines vs Totaux: cells give 8880, printed 8800 (difference -80)
  - sgt1928 p.287 (f839) bot_seedsales [Avoines] Medjerdah: total = sum: cells give 360, printed 300 (difference -60)
  - sgt1928 p.287 (f839) bot_seedsales [Avoines] 1910-23: lines vs Totaux: cells give 138385, printed 138325 (difference -60)
  - sgt1929 p.288 (f316) bot_seedsales [Blés durs] Huguenot: total = sum: cells give 3841, printed 3814 (difference -27)
  - sgt1929 p.288 (f316) bot_seedsales [Blés durs] Sbéi: total = sum: cells give 10285, printed 10305 (difference 20)
  - sgt1929 p.288 (f316) bot_seedsales [Blés durs] Souri: total = sum: cells give 15205, printed 15265 (difference 60)
  - sgt1929 p.288 (f316) bot_seedsales [Blés durs] 1910-24: lines vs Totaux: cells give 104700, printed 104780 (difference 80)
  - sgt1929 p.288 (f316) bot_seedsales [Blés tendres] 1928: lines vs Totaux: cells give 8880, printed 8800 (difference -80)
  - sgt1929 p.288 (f316) bot_seedsales [Avoines] de Laconie: total = sum: cells give 1000, printed 1150 (difference 150)
  - sgt1930 p.295 (f853) bot_seedsales [Blés durs] Huguenot: total = sum: cells give 3841, printed 3814 (difference -27)
  - sgt1930 p.295 (f853) bot_seedsales [Blés durs] Sbéi: total = sum: cells give 14285, printed 14305 (difference 20)
  - sgt1930 p.295 (f853) bot_seedsales [Blés tendres] Pusa Florence: total = sum: cells give 1190, printed 67097 (difference 65907)
  - sgt1930 p.295 (f853) bot_seedsales [Blés tendres] Richelle hâtive: total = sum: cells give 67097, printed 2740 (difference -64357)
  - sgt1930 p.295 (f853) bot_seedsales [Blés tendres] Richelle tardive: total = sum: cells give 2740, printed 1190 (difference -1550)
  - sgt1930 p.295 (f853) bot_seedsales [Blés tendres] Autres variétés: total = sum: cells give 2590, printed 2500 (difference -90)
  - sgt1930 p.295 (f853) bot_seedsales [Blés tendres] 1910-25: lines vs Totaux: cells give 118782, printed 128782 (difference 10000)
  - sgt1930 p.295 (f853) bot_seedsales [Blés tendres] 1928: lines vs Totaux: cells give 8880, printed 8800 (difference -80)
  - sgt1930 p.295 (f853) bot_seedsales [Avoines] Crême: total = sum: cells give 121770, printed 113460 (difference -8310)
  - sgt1930 p.295 (f853) bot_seedsales [Avoines] de Laconie: total = sum: cells give 1250, printed 1400 (difference 150)
  - sgt1930 p.295 (f853) bot_seedsales [Avoines] 1930: lines vs Totaux: cells give 1300, printed 1800 (difference 500)

- Overlapping printings: 893 cell comparisons with other editions printing the same cell; 1 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1921-22 / Orges / Escourgeons | sgt1922 | 22 | sgt1926 | 2400 |

- Flagged cells: total_mismatch: 13.

  - sgt1923 p.267 1918 Blés durs / 1910-18 / Mekki / kilogrammes = 1650 (total_mismatch)
  - sgt1924 p.283 1919 Blés durs / 1910-19 / Mekki / kilogrammes = 2500 (total_mismatch)
  - sgt1927 p.283 1922 Blés durs / 1910-22 / Biskri glabre / kilogrammes = 3360 (total_mismatch)
  - sgt1928 p.287 1923 Blés durs / 1910-23 / Biskri glabre / kilogrammes = 3860 (total_mismatch)
  - sgt1928 p.287 1923 Avoines / 1910-23 / Medjerdah / kilogrammes = 360 (total_mismatch)
  - sgt1929 p.288 1924 Blés durs / 1910-24 / Biskri glabre / kilogrammes = 6460 (total_mismatch)
  - sgt1929 p.288 1924 Blés durs / 1910-24 / Sbéi / kilogrammes = 8175 (total_mismatch)
  - sgt1929 p.288 1924 Blés durs / 1910-24 / Souri / kilogrammes = 14705 (total_mismatch)
  - sgt1930 p.295 1925 Blés durs / 1910-25 / Biskri glabre / kilogrammes = 8810 (total_mismatch)
  - sgt1930 p.295 1925 Blés durs / 1910-25 / Sbéi / kilogrammes = 8885 (total_mismatch)
  - sgt1930 p.295 1925 Blés durs / 1910-25 / Souri / kilogrammes = 15205 (total_mismatch)
  - sgt1930 p.295 1926 Blés durs / 1925-26 / Huguenot / kilogrammes = 500 (total_mismatch)
  - sgt1930 p.295 1926 Blés durs / 1925-26 / Jenah Rhetifa / kilogrammes = 50 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (36 printings): sgt1922 f278, sgt1922 f278, sgt1922 f278, sgt1922 f278, sgt1923 f769, sgt1923 f769, sgt1923 f769, sgt1923 f769, sgt1924 f1273, sgt1924 f1273, sgt1924 f1273, sgt1924 f1273, sgt1925 f339, sgt1925 f339, sgt1925 f339, sgt1925 f339, sgt1926 f849, sgt1926 f849, sgt1926 f849, sgt1926 f849, sgt1927 f311, sgt1927 f311, sgt1927 f311, sgt1927 f311, sgt1928 f839, sgt1928 f839, sgt1928 f839, sgt1928 f839, sgt1929 f316, sgt1929 f316, sgt1929 f316, sgt1929 f316, sgt1930 f853, sgt1930 f853, sgt1930 f853, sgt1930 f853.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
