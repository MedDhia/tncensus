# Accidents du travail. c) Causes matérielles des accidents dans les diverses catégories professionnelles

*Industrial accidents by occupational category and material cause.*

Source: *Statistique générale de la Tunisie*, chapter *Travail et prévoyance sociale*, editions sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1925 (`bpt6k9105650k`): p. 492, f516, p. 493, f517; sgt1926 (`bpt6k9105650k`): p. 476, f1040, p. 477, f1041; sgt1927 (`bpt6k91056510`): p. 478, f506, p. 479, f507; sgt1928 (`bpt6k91056510`): p. 484, f1036, p. 485, f1037; sgt1929 (`bpt6k9105652d`): p. 486, f514, p. 487, f515; sgt1930 (`bpt6k9105652d`): p. 492, f1050, p. 493, f1051; sgt1935 (`bpt6k9105653t`): p. 305, f325; sgt1936 (`bpt6k91056547`): p. 180, f191, p. 181, f192; sgt1939 (`bpt6k9105739w`): p. 162, f168, p. 163, f169.

Transcriptions: `../transcribed/labour_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_labour.py build`.

Rows: 1650. Years: 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1939.

Unit: accidents; value_type: count.

Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept, with `year` (the edition year when no year is printed); a year printed by two editions is stored once, from the later one, and compared.

## Columns

- `census`: edition the value is taken from (rule 4 series: the latest edition printing it; rule 5: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (two-page spreads: the page the cell is printed on)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (HBM: last year of the printed period)
- `category`: occupational category (English code; the list changes in sgt1927 and sgt1936)
- `category_fr`: category as printed
- `cause`: material cause (English code; the list changes in sgt1927)
- `cause_fr`: printed heading
- `value`: printed value (» = 0)
- `flag`: empty, ocr_corrected, illegible, total_mismatch, derived_from_totals, not_applicable, reprint_corrected or row_realigned

Printed in every edition, on a two-page spread. 15 causes in sgt1925-sgt1926 (moteurs ... défaut de chaussures), a new list of 15 from sgt1927 (machines: moteurs, transmission, machines-outils-métiers; ascenseurs; chaudières; matières explosibles; ... divers). `year` = edition year, except sgt1935 'survenues en 1935' and sgt1936 '(1935)': sgt1936 reprints the 1935 table in a new setting and is stored for 1935, with two misprints replaced by sgt1935's printing (`reprint_corrected`): Mines / véhicules 31 (sgt1935 3; totals need 3) and Industrie textile / matières brûlantes » (sgt1935 1). No 1936 causes table.

Flagged `total_mismatch`: 1935 Armées / divers printed 11 in both sgt1935 and sgt1936 (61 needed); sgt1939 Transports / matières brûlantes printed 119 (109 needed). The line totals of sgt1939's causes table differ from its nationality table for several categories with the same grand total (printed as such).

Every failed check below was re-read on a zoomed native-resolution crop (or recurs unchanged in independent readings of several editions): printed values are kept. Each failure is one cell flagged `total_mismatch` (row and column both off by the same amount), or the sgt1936 misprints replaced from sgt1935.

Survey of the whole chapter in every edition: `labour_survey.md`.

## Validation

- Checks against printed totals and identities: 277; passed: 263; failed: 14.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1926 p.476 (f1040) acc_cause Agriculture: total = motors + transmission + machines + lifting + autoclaves + explosives + hot_matter + falling_objects + worker_fall + handling + traction + hand_tools + miscellaneous + unknown + footwear: cells give 1246, printed 1245 (difference -1)
  - sgt1926 p.476 (f1040) acc_cause handling: lines vs Totaux: cells give 2113, printed 2112 (difference -1)
  - sgt1928 p.484 (f1036) acc_cause Agriculture et forêts: total = motors + transmission + machines + lifting + boilers + explosives + hot_matter + collapse + falls_height + loading + vehicles + railways + navigation + hand_tools + miscellaneous: cells give 1456, printed 1515 (difference 59)
  - sgt1928 p.484 (f1036) acc_cause vehicles: lines vs Totaux: cells give 1411, printed 1470 (difference 59)
  - sgt1935 p.304 (f324) acc_cause Autres: total = motors + transmission + machines + lifting + boilers + explosives + hot_matter + collapse + falls_height + loading + vehicles + railways + navigation + hand_tools + miscellaneous: cells give 139, printed 189 (difference 50)
  - sgt1935 p.304 (f324) acc_cause miscellaneous: lines vs Totaux: cells give 2448, printed 2498 (difference 50)
  - sgt1936 p.180 (f191) acc_cause Mines: total = motors + transmission + machines + lifting + boilers + explosives + hot_matter + collapse + falls_height + loading + vehicles + railways + navigation + hand_tools + miscellaneous: cells give 1792, printed 1764 (difference -28)
  - sgt1936 p.180 (f191) acc_cause Industrie textile, nettoyage, cuirs et peaux: total = motors + transmission + machines + lifting + boilers + explosives + hot_matter + collapse + falls_height + loading + vehicles + railways + navigation + hand_tools + miscellaneous: cells give 10, printed 11 (difference 1)
  - sgt1936 p.180 (f191) acc_cause Autres: total = motors + transmission + machines + lifting + boilers + explosives + hot_matter + collapse + falls_height + loading + vehicles + railways + navigation + hand_tools + miscellaneous: cells give 139, printed 189 (difference 50)
  - sgt1936 p.180 (f191) acc_cause hot_matter: lines vs Totaux: cells give 706, printed 707 (difference 1)
  - sgt1936 p.180 (f191) acc_cause vehicles: lines vs Totaux: cells give 887, printed 859 (difference -28)
  - sgt1936 p.180 (f191) acc_cause miscellaneous: lines vs Totaux: cells give 2448, printed 2498 (difference 50)
  - sgt1939 p.162 (f168) acc_cause Transports : chemins de fer et tramways, autres transports par terre et entrepôts, poste et télégraphe, navigation aérienne et maritime: total = motors + transmission + machines + lifting + boilers + explosives + hot_matter + collapse + falls_height + loading + vehicles + railways + navigation + hand_tools + miscellaneous: cells give 2549, printed 2539 (difference -10)
  - sgt1939 p.162 (f168) acc_cause hot_matter: lines vs Totaux: cells give 375, printed 365 (difference -10)

- Overlapping printings: 210 cell comparisons with other editions printing the same cell; 2 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1935 / mines / vehicles | sgt1935 | 3 | sgt1936 | 31 |
| 1935 / textiles_cleaning_leather / hot_matter | sgt1935 | 1 | sgt1936 | 0 |

- Flagged cells: reprint_corrected: 2, total_mismatch: 5.

  - sgt1926 p.477 1926 agriculture / handling = 103 (total_mismatch)
  - sgt1928 p.485 1928 agriculture_forestry / vehicles = 428 (total_mismatch)
  - sgt1935 p.305 1935 mines / vehicles = 3 (reprint_corrected)
  - sgt1935 p.305 1935 textiles_cleaning_leather / hot_matter = 1 (reprint_corrected)
  - sgt1936 p.181 1935 armed_forces / miscellaneous = 11 (total_mismatch)
  - sgt1936 p.181 1935 other / miscellaneous = 6 (total_mismatch)
  - sgt1939 p.163 1939 transport / hot_matter = 119 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (9 printings): sgt1925 f516, sgt1926 f1040, sgt1927 f506, sgt1928 f1036, sgt1929 f514, sgt1930 f1050, sgt1935 f324, sgt1936 f191, sgt1939 f168.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
