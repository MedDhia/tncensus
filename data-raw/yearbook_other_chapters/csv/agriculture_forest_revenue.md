# Forêts. c) Rendement en argent des produits forestiers

*Forests: money yield of forest products, by product (1922-1923) or by sale (1924-1939), in francs.*

Source: *Statistique générale de la Tunisie*, chapter *Agriculture*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 230, f254; sgt1923 (`bpt6k9105649x`): p. 242, f744; sgt1924 (`bpt6k9105649x`): p. 256, f1246; sgt1925 (`bpt6k9105650k`): p. 284, f308; sgt1926 (`bpt6k9105650k`): p. 254, f818; sgt1927 (`bpt6k91056510`): p. 253, f281; sgt1928 (`bpt6k91056510`): p. 253, f805; sgt1929 (`bpt6k9105652d`): p. 255, f283; sgt1930 (`bpt6k9105652d`): p. 259, f817; sgt1935 (`bpt6k9105653t`): p. 133, f153; sgt1936 (`bpt6k91056547`): p. 104, f115; sgt1939 (`bpt6k9105739w`): p. 108, f114.

Transcriptions: `../transcribed/agriculture_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_agriculture.py build`.

Rows: 101. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939.

Units: francs, francs per unit, and quantity units (`unit`); value_type: money (and quantities).

Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept; `year` = edition year.

## Columns

- `census`: edition the value is taken from (rule 4 series: the latest edition printing that year; rule 5 tables: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: edition year
- `line_no`: order of the line on the page
- `item_fr`: printed line heading: product (sgt1922-sgt1923) or sale (from sgt1924), as printed
- `observation_fr`: printed observation (sgt1922-sgt1923), else empty
- `in_total`: `yes`, or `no` for the montant des condamnations (mémoire) of sgt1922, printed beside the table and not part of its TOTAUX
- `measure`: `quantity`, `unit_price`, `total_price` (sgt1922-sgt1923 columns), or `revenue` (the single amount column from sgt1924)
- `measure_fr`: printed column heading (or the table title for the single amount column)
- `unit`: `francs`, `francs_per_<unit>`, or the quantity unit (`cubic_metres`, `steres`, `quintals`, `linear_metres`, `count`); never converted
- `unit_fr`: unit as printed ("—" = ditto of the line above; fr. c = francs and centimes)
- `value`: printed value (» = 0)
- `flag`: empty, or `total_mismatch`

Printed in every edition beside b). sgt1922 and sgt1923 print one line per product (unités, quantités, prix moyen à l'unité, prix total, observations); from sgt1924 one amount per sale (adjudication, marché de gré à gré), menus produits and, from sgt1935, chasse and transactions. Amounts in francs and centimes as printed. Rule 5: each edition kept. The TOTAL / TOTAUX lines are checks only. Lines without quantity or price (» printed) store the amount only. sgt1922's souches de bruyère bracket two amounts (4e annuité; marché gré à gré): two lines; sgt1936 brackets two lines (adjudications diverses; cessions de gré à gré) to one amount: one line.

Checks: lines = TOTAL; for sgt1922-sgt1923, quantity x prix moyen = prix total (to half a centime per unit, the rounding of the printed price). Footnotes of the sale lines (sums payable the next year) are given in the transcriptions; the next edition prints them as their own lines (e.g. sgt1925 "Adjudication du 17 juin 1924 (Somme payable en 1925)" 19.920).

Every failed check below was re-read on a zoomed native-resolution crop: they are printed inconsistencies (printed values kept). sgt1923 prints the liège de reproduction price "2.872 »" (1.906.471,30 / 66.365 = 28,73: flagged `total_mismatch`) and the bois d'industrie price 39,83 where 1.036.806 / 27.283 = 38,00 (price or amount; not identifiable, kept unflagged; the amount fits the TOTAUX). sgt1936: the lines give 6.696.691,90, the TOTAL prints 6.696.688,90 (3 francs; every cell re-read, not identifiable).

Survey of the whole chapter in every edition: `agriculture_survey.md`.

## Validation

- Checks against printed totals and identities: 26; passed: 23; failed: 3.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1923 p.242 (f744) forest_c Bois d'industrie (chêne-zéen, bois de charronnage): quantity x unit price = prix total (to half a centime per unit): cells give 1086681.89, printed 1036806 (difference -49875.89)
  - sgt1923 p.242 (f744) forest_c Liège de reproduction: quantity x unit price = prix total (to half a centime per unit): cells give 190600280.00, printed 1906471.30 (difference -188693808.70)
  - sgt1936 p.104 (f115) forest_c lines vs TOTAL: cells give 6696691.90, printed 6696688.90 (difference -3.00)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: total_mismatch: 1.

  - sgt1923 p.242 1923 6 / yes / unit_price / francs_per_quintals = 2872 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (12 printings): sgt1922 f254, sgt1923 f744, sgt1924 f1246, sgt1925 f308, sgt1926 f818, sgt1927 f281, sgt1928 f805, sgt1929 f283, sgt1930 f817, sgt1935 f153, sgt1936 f115, sgt1939 f114.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
