# Ventes avec obligation d'installation personnelle (propriétés livrées à la colonisation)

*Sales with an obligation of personal settlement: lotissements delivered to colonisation, by year, with area and number of lots.*

Source: *Statistique générale de la Tunisie*, chapter *Colonisation*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 415, f439, p. 417, f441, p. 419, f443; sgt1923 (`bpt6k9105649x`): p. 427, f929, p. 429, f931, p. 431, f933; sgt1924 (`bpt6k9105649x`): p. 442, f1432, p. 443, f1433, p. 444, f1434, p. 445, f1435; sgt1925 (`bpt6k9105650k`): p. 476, f500, p. 477, f501, p. 478, f502, p. 479, f503; sgt1926 (`bpt6k9105650k`): p. 446, f1010, p. 447, f1011, p. 448, f1012, p. 449, f1013, p. 450, f1014, p. 451, f1015; sgt1927 (`bpt6k91056510`): p. 444, f472, p. 445, f473, p. 446, f474, p. 447, f475, p. 448, f476, p. 449, f477, p. 450, f478, p. 451, f479; sgt1928 (`bpt6k91056510`): p. 448, f1000, p. 449, f1001, p. 450, f1002, p. 451, f1003, p. 452, f1004, p. 453, f1005, p. 454, f1006, p. 455, f1007; sgt1929 (`bpt6k9105652d`): p. 450, f478, p. 451, f479, p. 452, f480, p. 453, f481, p. 454, f482, p. 455, f483, p. 456, f484, p. 457, f485; sgt1930 (`bpt6k9105652d`): p. 456, f1014, p. 457, f1015, p. 458, f1016, p. 459, f1017, p. 460, f1018, p. 461, f1019, p. 462, f1020, p. 463, f1021; sgt1935 (`bpt6k9105653t`): p. 272, f292, p. 273, f293, p. 274, f294, p. 275, f295, p. 276, f296, p. 277, f297; sgt1936 (`bpt6k91056547`): p. 162, f173, p. 163, f174, p. 164, f175, p. 165, f176, p. 166, f177, p. 167, f178; sgt1939 (`bpt6k9105739w`): p. 146, f152, p. 147, f153.

Transcriptions: `../transcribed/colonisation_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_colonisation.py build`.

Rows: 4591. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Units: hectares (area, printed h. a.) and number of lots (`unit`); suggested value_type: mixed.

Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept (`census` = edition); the figures are the state at the edition date and are revised between editions.

## Columns

- `census`: edition the value is taken from (rule 4 tables: the latest edition printing that year)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `scheme`: `installation` (ventes avec obligation d'installation personnelle)
- `scheme_fr`: printed table title
- `property_fr`: property / lotissement as printed (footnote calls kept)
- `origin_fr`: printed origin column heading
- `nature_fr`: sgt1922-sgt1923 only: printed nature de l'immeuble ou du lotissement (ditto marks resolved)
- `situation_fr`: printed situation
- `controle_civil`: contrôle civil as printed
- `observation_fr`: printed observation for the line (a brace covering several lines is repeated on each)
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible`, `not_applicable`, `total_mismatch`, `ocr_corrected`

Printed in every edition for the ten years before the edition (sgt1939: 1929-1939). One row per printed figure of a lotissement line, with the property name, situation and contrôle civil as printed. Two layouts: sgt1922-sgt1923 (*Ventes avec obligation d'installation : a) Propriétés livrées à la colonisation*: nature, superficie totale, lots créés / réservés ou disponibles / vendus; urban, suburban and summer lotissements are in this list) and sgt1924-sgt1939 (*a) Ventes avec obligation d'installation personnelle*: superficie, lots ruraux / maraîchers / suburbains / d'artisans / totaux; urban lotissements in a separate table). The printed TOTAUX column of the second layout is a check only (not stored); A reporter / Reports / Totaux lines are checks only. From sgt1935 an origin code follows each name (A. = achat sur le fonds de colonisation, D. = domaines, H. = habous, by the headings of the recapitulation table; not explained on the page). sgt1939 drops the artisans column and prints TOTAUX before SUBURBAINS.

The lists are revised from edition to edition (areas and lot counts of the same lotissement change; lots taken back, lines regrouped), so every edition is kept. A line printed in brace with two names (e.g. Henchir Chouichia / Aïn-el-Merdja, one area) is one row with both names.

Binding: sgt1935 f294-f297 lose the ares of the area column in the gutter; those cells are taken from sgt1930's printing of the same lotissement after checking that the legible hectares agree (`reprint_corrected`), and the cut printed totals are checked on the hectares. sgt1939 Transvaal ares '9?' solved from the total (`derived_from_totals`).

Every failed check below was re-read on a native-resolution crop: the printed values are kept. créés = réservés + vendus fails on lines "en cours d'attribution" (lots created, none yet reserved or sold: » printed) and on sgt1922-sgt1923 Klédia (35 created, 9 + 4) and sgt1922 Lagrenée-Chaouat (31, 3 + 0). sgt1926-sgt1927 print "Reports 64.861,22" for the 64.861,32 carried. sgt1928 prints » in the TOTAUX column of the 1928 lines while the column total (1.191) counts them. sgt1936: Djedeïda 1930 prints » for maraîchers but 4 in TOTAUX (other editions: 4 maraîchers; flag total_mismatch on the maraîchers cell), and the TOTAUX lot total 517 leaves them out; the area total 49.611,84 and sgt1939's 20.674,91 are both 1.000 ha below the sum of their lines.

Survey of the whole chapter in every edition: `colonisation_survey.md`.

## Validation

- Checks against printed totals and identities: 1240; passed: 1224; failed: 16.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.418 (f442) install22 Khang-Mourou: créés = réservés ou disponibles + vendus: cells give 0, printed 14 (difference 14)
  - sgt1922 p.418 (f442) install22 Saouaf-Djebibina: créés = réservés ou disponibles + vendus: cells give 0, printed 89 (difference 89)
  - sgt1922 p.418 (f442) install22 Lagrenée-Chaouat: créés = réservés ou disponibles + vendus: cells give 3, printed 31 (difference 28)
  - sgt1922 p.418 (f442) install22 Klédia: créés = réservés ou disponibles + vendus: cells give 13, printed 35 (difference 22)
  - sgt1923 p.430 (f932) install22 Klédia: créés = réservés ou disponibles + vendus: cells give 13, printed 35 (difference 22)
  - sgt1923 p.430 (f932) install22 Ousseltia: créés = réservés ou disponibles + vendus: cells give 0, printed 64 (difference 64)
  - sgt1923 p.430 (f932) install22 Bou-Ficha: créés = réservés ou disponibles + vendus: cells give 0, printed 66 (difference 66)
  - sgt1923 p.430 (f932) install22 De Carnières: créés = réservés ou disponibles + vendus: cells give 0, printed 20 (difference 20)
  - sgt1923 p.430 (f932) install22 Lynx: créés = réservés ou disponibles + vendus: cells give 0, printed 34 (difference 34)
  - sgt1926 p.448 (f1012) install area: Reports = previous page's A reporter: cells give 64861.32, printed 64861.22 (difference -0.10)
  - sgt1927 p.446 (f474) install area: Reports = previous page's A reporter: cells give 64861.32, printed 64861.22 (difference -0.10)
  - sgt1928 p.454 (f1006) install total: Totaux = report + lines: cells give 1083, printed 1191 (difference 108)
  - sgt1936 p.166 (f177) install35 Djedeïda: TOTAUX = sum of the lot types: cells give 0, printed 4 (difference 4)
  - sgt1936 p.166 (f177) install35 area: Totaux = report + lines: cells give 50611.84, printed 49611.84 (difference -1000.00)
  - sgt1936 p.166 (f177) install35 total: Totaux = report + lines: cells give 521, printed 517 (difference -4)
  - sgt1939 p.146 (f152) install35 area: Totaux = report + lines: cells give 21674.91, printed 20674.91 (difference -1000.00)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: derived_from_totals: 1, not_applicable: 12, reprint_corrected: 34, total_mismatch: 1.

  - sgt1922 p.419 1922 installation / Zaghouan / lots_reserved_or_available / count = NA (not_applicable)
  - sgt1922 p.419 1922 installation / Zaghouan / lots_sold / count = NA (not_applicable)
  - sgt1922 p.419 1922 installation / Zaghouan / lots_reserved_or_available / count = NA (not_applicable)
  - sgt1922 p.419 1922 installation / Zaghouan / lots_sold / count = NA (not_applicable)
  - sgt1922 p.419 1922 installation / Zaghouan / lots_reserved_or_available / count = NA (not_applicable)
  - sgt1922 p.419 1922 installation / Zaghouan / lots_sold / count = NA (not_applicable)
  - sgt1922 p.419 1922 installation / Sousse / lots_reserved_or_available / count = NA (not_applicable)
  - sgt1922 p.419 1922 installation / Sousse / lots_sold / count = NA (not_applicable)
  - sgt1922 p.419 1922 installation / Medjez-el-Bab / lots_reserved_or_available / count = NA (not_applicable)
  - sgt1922 p.419 1922 installation / Medjez-el-Bab / lots_sold / count = NA (not_applicable)
  - sgt1922 p.419 1922 installation / Medjez-el-Bab / lots_reserved_or_available / count = NA (not_applicable)
  - sgt1922 p.419 1922 installation / Medjez-el-Bab / lots_sold / count = NA (not_applicable)
  - sgt1935 p.274 1928 installation / Tunis / area / hectares = 3163.80 (reprint_corrected)
  - sgt1935 p.274 1928 installation / Tunis / area / hectares = 1718.65 (reprint_corrected)
  - sgt1935 p.274 1928 installation / Souk-el-Arba / area / hectares = 2149 (reprint_corrected)
  - sgt1935 p.274 1928 installation / Souk-el-Arba / area / hectares = 924.50 (reprint_corrected)
  - sgt1935 p.274 1928 installation / Zaghouan / area / hectares = 1850 (reprint_corrected)
  - sgt1935 p.274 1928 installation / Souk-el-Arba / area / hectares = 1990 (reprint_corrected)
  - sgt1935 p.274 1928 installation / Tunis / area / hectares = 283.20 (reprint_corrected)
  - sgt1935 p.274 1928 installation / Mdejez-el-Bab / area / hectares = 847.40 (reprint_corrected)
  - sgt1935 p.274 1928 installation / Bizerte / area / hectares = 804.47 (reprint_corrected)
  - sgt1935 p.274 1928 installation / Téboursouk / area / hectares = 492.50 (reprint_corrected)
  - sgt1935 p.274 1929 installation / Medjez-el-Bab / area / hectares = 1607.70 (reprint_corrected)
  - sgt1935 p.274 1929 installation / Grombalia / area / hectares = 34 (reprint_corrected)
  - sgt1935 p.274 1929 installation / Tunis / area / hectares = 216.70 (reprint_corrected)
  - sgt1935 p.274 1929 installation / Bizerte / area / hectares = 500.30 (reprint_corrected)
  - sgt1935 p.274 1929 installation / Le Kef / area / hectares = 147.87 (reprint_corrected)
  - sgt1935 p.274 1929 installation / Medjez-el-Bab / area / hectares = 567 (reprint_corrected)
  - sgt1935 p.274 1929 installation / Tunis / area / hectares = 760.10 (reprint_corrected)
  - sgt1935 p.274 1929 installation / Tunis / area / hectares = 2743.55 (reprint_corrected)
  - sgt1935 p.274 1929 installation / Grombalia / area / hectares = 244 (reprint_corrected)
  - sgt1935 p.274 1929 installation / Souk-el-Arba / area / hectares = 198 (reprint_corrected)
  - sgt1935 p.276 1930 installation / Tunis / area / hectares = 659.15 (reprint_corrected)
  - sgt1935 p.276 1930 installation / Medjez-el-Bab / area / hectares = 462 (reprint_corrected)
  - sgt1935 p.276 1930 installation / Medjez-el-Bab / area / hectares = 718.50 (reprint_corrected)
  - sgt1935 p.276 1930 installation / Grombalia / area / hectares = 266.60 (reprint_corrected)
  - sgt1935 p.276 1930 installation / Bizerte / area / hectares = 30.30 (reprint_corrected)
  - sgt1935 p.276 1930 installation / Bizerte / area / hectares = 96.72 (reprint_corrected)
  - sgt1935 p.276 1930 installation / Béja / area / hectares = 270 (reprint_corrected)
  - sgt1935 p.276 1930 installation / Tunis / area / hectares = 22.25 (reprint_corrected)
  - sgt1935 p.276 1930 installation / Zaghouan / area / hectares = 283.40 (reprint_corrected)
  - sgt1935 p.276 1930 installation / Medjez-el-Bab / area / hectares = 659 (reprint_corrected)
  - sgt1935 p.276 1930 installation / Medjez-el-Bab / area / hectares = 687.20 (reprint_corrected)
  - sgt1935 p.276 1930 installation / Tunis / area / hectares = 807.99 (reprint_corrected)
  - sgt1935 p.276 1930 installation / Tunis / area / hectares = 1963.04 (reprint_corrected)
  - sgt1935 p.276 1930 installation / Zaghouan / area / hectares = 867.75 (reprint_corrected)
  - sgt1936 p.167 1930 installation / Tunis / lots_market_garden / count = 0 (total_mismatch)
  - sgt1939 p.146 1939 installation / Bizerte / area / hectares = 0.90 (derived_from_totals)

## Image versus OCR

- Read cell by cell on the page images (36 printings): sgt1922 f438, sgt1922 f440, sgt1922 f442, sgt1923 f928, sgt1923 f930, sgt1923 f932, sgt1924 f1432, sgt1924 f1434, sgt1925 f500, sgt1925 f502, sgt1926 f1010, sgt1926 f1012, sgt1926 f1014, sgt1927 f472, sgt1927 f474, sgt1927 f476, sgt1927 f478, sgt1928 f1000, sgt1928 f1002, sgt1928 f1004, sgt1928 f1006, sgt1929 f478, sgt1929 f480, sgt1929 f482, sgt1929 f484, sgt1930 f1014, sgt1930 f1016, sgt1930 f1018, sgt1930 f1020, sgt1935 f292, sgt1935 f294, sgt1935 f296, sgt1936 f173, sgt1936 f175, sgt1936 f177, sgt1939 f152.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
