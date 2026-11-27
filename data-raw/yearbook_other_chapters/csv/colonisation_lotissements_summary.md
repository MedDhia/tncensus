# Lotissements. a) Lotissements ruraux livrés à la Colonisation ; b) Lotissements de terres à planter

*Lotissements delivered to colonisation: area by origin of the land and number of lots, before and after a cut-off year.*

Source: *Statistique générale de la Tunisie*, chapter *Colonisation*, editions sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1924 (`bpt6k9105649x`): p. 450, f1440, p. 451, f1441; sgt1925 (`bpt6k9105650k`): p. 484, f508, p. 485, f509; sgt1926 (`bpt6k9105650k`): p. 456, f1020, p. 457, f1021; sgt1927 (`bpt6k91056510`): p. 456, f484, p. 457, f485; sgt1928 (`bpt6k91056510`): p. 460, f1012, p. 461, f1013; sgt1929 (`bpt6k9105652d`): p. 462, f490, p. 463, f491; sgt1930 (`bpt6k9105652d`): p. 468, f1026, p. 469, f1027; sgt1935 (`bpt6k9105653t`): p. 284, f304, p. 285, f305; sgt1936 (`bpt6k91056547`): p. 168, f179; sgt1939 (`bpt6k9105739w`): p. 148, f154.

Transcriptions: `../transcribed/colonisation_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_colonisation.py build`.

Rows: 185. Years: 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939.

Units: hectares (area, by origin of the land) and number of lots; suggested value_type: mixed.

Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept (`census` = edition); the figures are the state at the edition date and are revised between editions.

## Columns

- `census`: edition the value is taken from (rule 4 tables: the latest edition printing that year)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `lotissement`: `rural` (a) lotissements ruraux) or `planting` (b) terres à planter)
- `lotissement_fr`: printed table title
- `period`: `before_YYYY`, `from_YYYY` (printed Postérieure à / Depuis YYYY), or the memo line
- `period_fr`: printed period label
- `origin`: origin of the land: `domaines`, `habous` (publics et privés), `purchase_fund` (achat sur le fonds de colonisation), `sialine_lands` (terres sialines); empty for lot counts
- `origin_fr`: printed origin column heading
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible`, `not_applicable`, `total_mismatch`, `ocr_corrected`

Printed sgt1924-sgt1939 after the lists; two periods split at a year that moves with the edition (Antérieure à / Postérieure à 1918 in sgt1924-sgt1927, 1919 in sgt1928, Depuis 1920 in sgt1929, 1921 in sgt1930, 1926 in sgt1935, 1927 in sgt1936, 1929 in sgt1939). `year` = edition year (state at the edition date). TOTAUX column and line are checks only. sgt1935 adds a memo line *Achats pour recasements (pour mémoire)* (6.825,28 ha, 33 rural lots), outside the totals, stored with `period` = `resettlement_purchases_memo`.

Every failed check below was re-read on a native-resolution crop: the printed values are kept. sgt1928 (f1012-f1013) is internally inconsistent, each figure confirmed on zoomed crops: habous before 1919 printed 19.245 (other editions 19.205; the column total 20.308 needs 19.205 + 1.103), after 1919 printed 1.043 (needs 1.103), rural lots 846 / 828 against line totals 1.072 / 1.200; the planting table's TOTAUX column (140.079, 42.036, 182.115) does not match its parts (128.500, 53.605, 182.105). sgt1930 prints the before-1921 total 142.233,20 for parts giving 143.233,20, the grand total area 24.065,59 for 260.065,59 (two digits dropped), habous total 20.848,60 for 20.818,60, and ares off by 0,01 (rounding).

Survey of the whole chapter in every edition: `colonisation_survey.md`.

## Validation

- Checks against printed totals and identities: 212; passed: 196; failed: 16.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1928 p.460 (f1012) recap_rural Antérieure à 1919: TOTAUX (area) = sum of origins: cells give 107571.20, printed 107531.20 (difference -40.00)
  - sgt1928 p.460 (f1012) recap_rural Antérieure à 1919: TOTAUX (lots) = ruraux + petite culture: cells give 1081, printed 1072 (difference -9)
  - sgt1928 p.460 (f1012) recap_rural Postérieure à 1919: TOTAUX (area) = sum of origins: cells give 147690.09, printed 147750.90 (difference 60.81)
  - sgt1928 p.460 (f1012) recap_rural Postérieure à 1919: TOTAUX (lots) = ruraux + petite culture: cells give 1131, printed 1200 (difference 69)
  - sgt1928 p.460 (f1012) recap_rural Totaux: TOTAUX (area) = sum of origins: cells give 255281.29, printed 255282.10 (difference 0.81)
  - sgt1928 p.460 (f1012) recap_rural hab: Totaux = the two periods: cells give 20288, printed 20308 (difference 20)
  - sgt1928 p.460 (f1012) recap_rural rural: Totaux = the two periods: cells give 1674, printed 1734 (difference 60)
  - sgt1928 p.461 (f1013) recap_plant Antérieure à 1919: TOTAUX (area) = sum of origins: cells give 128500, printed 140079 (difference 11579)
  - sgt1928 p.461 (f1013) recap_plant Postérieure à 1919: TOTAUX (area) = sum of origins: cells give 53605, printed 42036 (difference -11569)
  - sgt1928 p.461 (f1013) recap_plant Totaux: TOTAUX (area) = sum of origins: cells give 182105, printed 182115 (difference 10)
  - sgt1930 p.468 (f1026) recap_rural Antérieure à 1921: TOTAUX (area) = sum of origins: cells give 143233.20, printed 142233.20 (difference -1000.00)
  - sgt1930 p.468 (f1026) recap_rural Depuis 1921: TOTAUX (area) = sum of origins: cells give 117832.40, printed 117832.39 (difference -0.01)
  - sgt1930 p.468 (f1026) recap_rural Totaux: TOTAUX (area) = sum of origins: cells give 261095.59, printed 24065.59 (difference -237030.00)
  - sgt1930 p.468 (f1026) recap_rural hab: Totaux = the two periods: cells give 20818.60, printed 20848.60 (difference 30.00)
  - sgt1930 p.468 (f1026) recap_rural ach: Totaux = the two periods: cells give 150392.06, printed 150392.05 (difference -0.01)
  - sgt1930 p.468 (f1026) recap_rural tot: Totaux = the two periods: cells give 260065.59, printed 24065.59 (difference -236000.00)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (20 printings): sgt1924 f1440, sgt1924 f1441, sgt1925 f508, sgt1925 f509, sgt1926 f1020, sgt1926 f1021, sgt1927 f484, sgt1927 f485, sgt1928 f1012, sgt1928 f1013, sgt1929 f490, sgt1929 f491, sgt1930 f1026, sgt1930 f1027, sgt1935 f304, sgt1935 f305, sgt1936 f179, sgt1936 f179, sgt1939 f154, sgt1939 f154.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
