# Résultats des instances d'immatriculation. a) État juridique et charge des immeubles (montant des rentes d'enzel et des hypothèques)

*Results of the registration proceedings: enzel rents and mortgages on the properties, by outcome and seat; number of land titles carrying the mortgages.*

Source: *Statistique générale de la Tunisie*, chapter *Propriété immobilière / Tribunal mixte / Propriété foncière*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 83, f107; sgt1923 (`bpt6k9105649x`): p. 89, f591; sgt1924 (`bpt6k9105649x`): p. 91, f1081; sgt1925 (`bpt6k9105650k`): p. 93, f117; sgt1926 (`bpt6k9105650k`): p. 104, f668; sgt1927 (`bpt6k91056510`): p. 102, f130; sgt1928 (`bpt6k91056510`): p. 102, f654; sgt1929 (`bpt6k9105652d`): p. 104, f132; sgt1930 (`bpt6k9105652d`): p. 108, f666; sgt1935 (`bpt6k9105653t`): p. 74, f94; sgt1936 (`bpt6k91056547`): p. 54, f65; sgt1939 (`bpt6k9105739w`): p. 54, f60.

Transcriptions: `../transcribed/property_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_property.py build`.

Rows: 312. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939.

Units: francs with centimes (`unit` = `francs`); land titles (`unit` = `titles`). Mixed table.

Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, with `year`; no year is printed by two editions.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: `charges` (amounts) or `charges_summary` (the box under the table)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (the edition year: each edition prints the table for its own year)
- `charge`: `enzel_rent` or `mortgage`
- `amount`: `registered` (inscrites), `declared` (déclarées); `titles` = number of land titles over which the mortgages are spread (*Les hypothèques se répartissent sur … titres à Tunis et … à Sousse*)
- `measure_fr`: printed line heading
- `outcome`: result of the registration proceeding
- `outcome_fr`: printed column heading
- `seat`: `tunis` or `sousse` (siège of the Tribunal mixte)
- `seat_fr`: as printed
- `unit`: `francs` or `titles`
- `value`: francs (centimes after the point) or number of titles
- `flag`: empty, or `total_mismatch` (printed value kept), `derived_from_totals`, `row_realigned`, `not_applicable` (nothing printed)

The box under the table (*nombre total des immeubles*, *total des rentes d'enzel inscrites*, *total des hypothèques inscrites*) repeats totals and is used as checks; the number of land titles carrying the mortgages, by seat, is stored (`amount` = `titles`). Line totals (TOTAUX column) are checks.

Failed checks (printed errors): sgt1922 enzel rents inscrites: 21.959,35 + 1.267 = 23.226,35, Totaux and box print 33.226,35; sgt1922 enzel déclarées: 3 printed under radiation Tunis, Totaux »; sgt1924 box "nombre total des immeubles" 387 against a) Totaux 389 (see legal status); sgt1925 box total enzel 25.580,10 against the line total 28.580,10.

Survey of the whole chapter in every edition: `property_survey.md`.

## Validation

- Checks against printed totals and identities: 84; passed: 80; failed: 4.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.83 (f107) charges enzel_registered: total = imm.tunis + imm.sousse + rej.tunis + rej.sousse + rad.tunis + rad.sousse: cells give 23226.35, printed 33226.35 (difference 10000.00)
  - sgt1922 p.83 (f107) charges enzel_declared: total = imm.tunis + imm.sousse + rej.tunis + rej.sousse + rad.tunis + rad.sousse: cells give 3, printed 0 (difference -3)
  - sgt1924 p.91 (f1081) charges_summary nombre total des immeubles = a) Totaux: cells give 389, printed 387 (difference -2)
  - sgt1925 p.93 (f117) charges_summary Total enzel = enzel_registered total: cells give 28580.10, printed 25580.10 (difference -3000.00)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (24 printings): sgt1922 f107, sgt1922 f107, sgt1923 f591, sgt1923 f591, sgt1924 f1081, sgt1924 f1081, sgt1925 f117, sgt1925 f117, sgt1926 f668, sgt1926 f668, sgt1927 f130, sgt1927 f130, sgt1928 f654, sgt1928 f654, sgt1929 f132, sgt1929 f132, sgt1930 f666, sgt1930 f666, sgt1935 f94, sgt1935 f94, sgt1936 f65, sgt1936 f65, sgt1939 f60, sgt1939 f60.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
