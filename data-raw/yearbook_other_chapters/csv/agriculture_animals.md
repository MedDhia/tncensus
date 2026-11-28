# Animaux. Nombre d'animaux de chaque espèce (possédés par des européens, des indigènes ; total), par contrôle civil et caïdat

*Livestock by species, contrôle civil and caïdat (European-owned, indigenous-owned, total).*

Source: *Statistique générale de la Tunisie*, chapter *Agriculture*, editions sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1927 (`bpt6k91056510`): p. 246, f274, p. 248, f276, p. 250, f278; sgt1928 (`bpt6k91056510`): p. 246, f798, p. 248, f800, p. 250, f802; sgt1929 (`bpt6k9105652d`): p. 248, f276, p. 250, f278, p. 252, f280; sgt1930 (`bpt6k9105652d`): p. 252, f810, p. 254, f812, p. 256, f814; sgt1935 (`bpt6k9105653t`): p. 130, f150; sgt1936 (`bpt6k91056547`): p. 102, f113; sgt1939 (`bpt6k9105739w`): p. 106, f112.

Transcriptions: `../transcribed/agriculture_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_agriculture.py build`.

Rows: 4336. Years: 1927, 1928, 1929, 1930, 1935, 1936, 1939.

Units: head of livestock (`unit`); value_type: count.

Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept; `year` = edition year.

## Columns

- `census`: edition the value is taken from (rule 4 series: the latest edition printing that year; rule 5 tables: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: edition year (sgt1936 and sgt1939 print "rôle de 1936" / "rôle de 1939"; no date printed in sgt1927-sgt1935)
- `region`: région as printed, or "Territoires militaires du Sud"
- `chef_lieu`: chef-lieu de région as printed; empty for the Territoires militaires
- `controle_civil`: contrôle civil as printed; empty for the Territoires militaires
- `caidat`: caïdat as printed; "Cap-Bon > Nabeul" = caïdat printed under the Cap-Bon bracket
- `owner`: `european`, `indigenous` (sgt1927-sgt1930 sub-tables a and b) or `total` (sub-table c; the only table in sgt1935-sgt1939)
- `owner_fr`: printed sub-table title
- `animal`: species code (English)
- `animal_fr`: printed column heading
- `measure`: `head`
- `measure_fr`: printed heading
- `unit`: `head`
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible`, `derived_from_totals`, `total_mismatch`

sgt1927-sgt1930 print three sub-tables (a) possédés par des européens, b) par des indigènes, c) total), sgt1935 only the total (européens et tunisiens), sgt1936 and sgt1939 the total of the animaux jeunes et imposables of the rôle de 1936 / rôle de 1939 (printed). Species: chevaux, chameaux, bovins, mulets, porcs, ânes, chèvres, moutons. Geography as in `agriculture_olive` (région / chef-lieu / contrôle civil / caïdat); Tunis-Ville is printed from sgt1935; sgt1935 prints Médenine-Tatahouine as one caïdat; sgt1939 adds Djemmal and drops La Skhira. The TOTAUX lines are checks only.

Rule 5: each edition kept. Some sgt1928 and sgt1929 cells are identical (the European sub-table is almost a reprint of the previous year), as printed.

Every failed check below was re-read on a zoomed native-resolution crop: they are printed inconsistencies (printed values kept). Flagged `total_mismatch` where one cell explains both its column (TOTAUX) and its row (européens + indigènes = total) check: sgt1927 européens chevaux Béja (634, both 50 short), total chevaux Ouerghemma (310 for 910); sgt1928 européens moutons Soliman (665, both 6 over), total moutons Béja (14.518 for 74.521), total mulets Fraichiches (985 for 685); sgt1929 indigènes bovins Nabeul (36.065, both 800 short), indigènes chèvres L'Aradh (29.106, both 600 short), total chameaux Oulad Ayar (1.380 for 1.580), total mulets Banlieue (5.395 for 5.305) and Téboursouk (4.997 for 1.997), total chèvres Ouerghemma (37.900 for 73.900); sgt1930 total chameaux Djebéniana (9.084 for 8.084), total mulets Tatahouine (50 for 60). Not identifiable (cell kept unflagged): sgt1927 total chevaux TOTAUX includes the Béja difference; sgt1928 differences of 1-6 units (Bizerte and Kairouan chameaux, Medjez-el-Bab moutons, total moutons TOTAUX 3 over after Béja); sgt1929 chevaux Tatahouine / Matmata (1 moved between the two lines); sgt1930 Sfax / La Skhira chèvres (570 moved between the two lines, column total right), ânes TOTAUX (20 over); sgt1935 chevaux TOTAUX 3 short; sgt1936 moutons TOTAUX 3.532.388 for the lines' 3.611.388 (no line identifiable; every cell re-read); sgt1939 chameaux TOTAUX 10 over. Checks with an illegible cell are skipped (sgt1935 chèvres Téboursouk "27.31" and Kairouan "46.92?": the column TOTAUX implies 74.357 for the two; sgt1939 chevaux Nabeul "3.63?", TOTAUX implies 3.638).

Survey of the whole chapter in every edition: `agriculture_survey.md`.

## Validation

- Checks against printed totals and identities: 1302; passed: 1265; failed: 37.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1927 p.246 (f274) animals european horses: lines vs TOTAUX: cells give 9911, printed 9961 (difference 50)
  - sgt1927 p.250 (f278) animals total horses: lines vs TOTAUX: cells give 91748, printed 92348 (difference 600)
  - sgt1928 p.246 (f798) animals european sheep: lines vs TOTAUX: cells give 103563, printed 103557 (difference -6)
  - sgt1928 p.250 (f802) animals total mules: lines vs TOTAUX: cells give 40543, printed 40243 (difference -300)
  - sgt1928 p.250 (f802) animals total sheep: lines vs TOTAUX: cells give 2112814, printed 2172820 (difference 60006)
  - sgt1929 p.250 (f278) animals indigenous cattle: lines vs TOTAUX: cells give 442720, printed 443520 (difference 800)
  - sgt1929 p.250 (f278) animals indigenous goats: lines vs TOTAUX: cells give 1633843, printed 1634443 (difference 600)
  - sgt1929 p.252 (f280) animals total camels: lines vs TOTAUX: cells give 155642, printed 155842 (difference 200)
  - sgt1929 p.252 (f280) animals total mules: lines vs TOTAUX: cells give 43982, printed 40892 (difference -3090)
  - sgt1929 p.252 (f280) animals total goats: lines vs TOTAUX: cells give 1628926, printed 1664926 (difference 36000)
  - sgt1930 p.256 (f814) animals total camels: lines vs TOTAUX: cells give 165038, printed 164038 (difference -1000)
  - sgt1930 p.256 (f814) animals total mules: lines vs TOTAUX: cells give 43673, printed 43683 (difference 10)
  - sgt1930 p.256 (f814) animals total donkeys: lines vs TOTAUX: cells give 180133, printed 180153 (difference 20)
  - sgt1935 p.130 (f150) animals total horses: lines vs TOTAUX: cells give 101948, printed 101945 (difference -3)
  - sgt1936 p.102 (f113) animals total sheep: lines vs TOTAUX: cells give 3611388, printed 3532388 (difference -79000)
  - sgt1939 p.106 (f112) animals total camels: lines vs TOTAUX: cells give 152216, printed 152226 (difference 10)
  - sgt1927 p.250 (f278) animals 1re Région / Bizerte / Béja / Béja horses: européens + indigènes vs total: cells give 8953, printed 9003 (difference 50)
  - sgt1927 p.250 (f278) animals Territoires militaires du Sud /  /  / Ouerghemma horses: européens + indigènes vs total: cells give 910, printed 310 (difference -600)
  - sgt1928 p.250 (f802) animals 1re Région / Bizerte / Béja / Béja sheep: européens + indigènes vs total: cells give 74521, printed 14518 (difference -60003)
  - sgt1928 p.250 (f802) animals 1re Région / Bizerte / Bizerte / Bizerte camels: européens + indigènes vs total: cells give 338, printed 339 (difference 1)
  - sgt1928 p.250 (f802) animals 2me Région / Tunis / Grombalia / Cap-Bon > Soliman sheep: européens + indigènes vs total: cells give 14807, printed 14801 (difference -6)
  - sgt1928 p.250 (f802) animals 3me Région / Le Kef / Medjez-el-Bab / Medjez-el-Bab sheep: européens + indigènes vs total: cells give 45182, printed 45179 (difference -3)
  - sgt1928 p.250 (f802) animals 4me Région / Sousse / Kairouan / Kairouan camels: européens + indigènes vs total: cells give 7266, printed 7265 (difference -1)
  - sgt1928 p.250 (f802) animals 4me Région / Sousse / Thala / Fraichiches mules: européens + indigènes vs total: cells give 685, printed 985 (difference 300)
  - sgt1929 p.252 (f280) animals 2me Région / Tunis / Tunis / Banlieue mules: européens + indigènes vs total: cells give 5305, printed 5395 (difference 90)
  - sgt1929 p.252 (f280) animals 2me Région / Tunis / Grombalia / Cap-Bon > Nabeul cattle: européens + indigènes vs total: cells give 37226, printed 38026 (difference 800)
  - sgt1929 p.252 (f280) animals 3me Région / Le Kef / Téboursouk / Téboursouk mules: européens + indigènes vs total: cells give 1997, printed 4997 (difference 3000)
  - sgt1929 p.252 (f280) animals 3me Région / Le Kef / Mactar / Oulad Ayar camels: européens + indigènes vs total: cells give 1580, printed 1380 (difference -200)
  - sgt1929 p.252 (f280) animals 5me Région / Sfax / Gabès / L'Aradh goats: européens + indigènes vs total: cells give 29378, printed 29978 (difference 600)
  - sgt1929 p.252 (f280) animals Territoires militaires du Sud /  /  / Ouerghemma goats: européens + indigènes vs total: cells give 73900, printed 37900 (difference -36000)
  - sgt1929 p.252 (f280) animals Territoires militaires du Sud /  /  / Tatahouine horses: européens + indigènes vs total: cells give 465, printed 464 (difference -1)
  - sgt1929 p.252 (f280) animals Territoires militaires du Sud /  /  / Matmata horses: européens + indigènes vs total: cells give 41, printed 42 (difference 1)
  - sgt1930 p.256 (f814) animals 5me Région / Sfax / Sfax / Sfax goats: européens + indigènes vs total: cells give 11333, printed 11903 (difference 570)
  - sgt1930 p.256 (f814) animals 5me Région / Sfax / Sfax / La Skhira goats: européens + indigènes vs total: cells give 37919, printed 37349 (difference -570)
  - sgt1930 p.256 (f814) animals 5me Région / Sfax / Sfax / Djebéniana camels: européens + indigènes vs total: cells give 8084, printed 9084 (difference 1000)
  - sgt1930 p.256 (f814) animals Territoires militaires du Sud /  /  / Tatahouine mules: européens + indigènes vs total: cells give 60, printed 50 (difference -10)
  - sgt1930 p.256 (f814) animals TOTAUX donkeys: européens + indigènes vs total: cells give 180133, printed 180153 (difference 20)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: derived_from_totals: 2, illegible: 3, total_mismatch: 13.

  - sgt1927 p.246 1927 1re Région / Bizerte / Béja / Béja / european / horses / head / head = 634 (total_mismatch)
  - sgt1927 p.250 1927 Territoires militaires du Sud /  /  / Ouerghemma / total / horses / head / head = 310 (total_mismatch)
  - sgt1928 p.246 1928 2me Région / Tunis / Grombalia / Cap-Bon > Soliman / european / sheep / head / head = 2553 (total_mismatch)
  - sgt1928 p.250 1928 1re Région / Bizerte / Béja / Béja / total / sheep / head / head = 14518 (total_mismatch)
  - sgt1928 p.250 1928 4me Région / Sousse / Thala / Fraichiches / total / mules / head / head = 985 (total_mismatch)
  - sgt1928 p.250 1928 4me Région / Sousse / Thala / Madjeurs / total / pigs / head / head = 16 (derived_from_totals)
  - sgt1929 p.250 1929 2me Région / Tunis / Grombalia / Cap-Bon > Nabeul / indigenous / cattle / head / head = 36065 (total_mismatch)
  - sgt1929 p.250 1929 5me Région / Sfax / Gabès / L'Aradh / indigenous / goats / head / head = 29106 (total_mismatch)
  - sgt1929 p.252 1929 2me Région / Tunis / Tunis / Banlieue / total / mules / head / head = 5395 (total_mismatch)
  - sgt1929 p.252 1929 3me Région / Le Kef / Téboursouk / Téboursouk / total / mules / head / head = 4997 (total_mismatch)
  - sgt1929 p.252 1929 3me Région / Le Kef / Mactar / Oulad Ayar / total / camels / head / head = 1380 (total_mismatch)
  - sgt1929 p.252 1929 4me Région / Sousse / Thala / Madjeurs / total / pigs / head / head = 16 (derived_from_totals)
  - sgt1929 p.252 1929 Territoires militaires du Sud /  /  / Ouerghemma / total / goats / head / head = 37900 (total_mismatch)
  - sgt1930 p.256 1930 5me Région / Sfax / Sfax / Djebéniana / total / camels / head / head = 9084 (total_mismatch)
  - sgt1930 p.256 1930 Territoires militaires du Sud /  /  / Tatahouine / total / mules / head / head = 50 (total_mismatch)
  - sgt1935 p.130 1935 3me Région / Le Kef / Téboursouk / Téboursouk / total / goats / head / head = NA (illegible)
  - sgt1935 p.130 1935 4me Région / Sousse / Kairouan / Kairouan / total / goats / head / head = NA (illegible)
  - sgt1939 p.106 1939 2me Région / Tunis / Grombalia / Cap-Bon > Nabeul / total / horses / head / head = NA (illegible)

## Image versus OCR

- Read cell by cell on the page images (15 printings): sgt1927 f274, sgt1927 f276, sgt1927 f278, sgt1928 f798, sgt1928 f800, sgt1928 f802, sgt1929 f276, sgt1929 f278, sgt1929 f280, sgt1930 f810, sgt1930 f812, sgt1930 f814, sgt1935 f150, sgt1936 f113, sgt1939 f112.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
