# Résultats des instances d'immatriculation. a) État juridique et charge des immeubles (nombre d'immeubles)

*Results of the registration proceedings: properties by legal status, outcome and seat.*

Source: *Statistique générale de la Tunisie*, chapter *Propriété immobilière / Tribunal mixte / Propriété foncière*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 83, f107; sgt1923 (`bpt6k9105649x`): p. 89, f591; sgt1924 (`bpt6k9105649x`): p. 91, f1081; sgt1925 (`bpt6k9105650k`): p. 93, f117; sgt1926 (`bpt6k9105650k`): p. 104, f668; sgt1927 (`bpt6k91056510`): p. 102, f130; sgt1928 (`bpt6k91056510`): p. 102, f654; sgt1929 (`bpt6k9105652d`): p. 104, f132; sgt1930 (`bpt6k9105652d`): p. 108, f666; sgt1935 (`bpt6k9105653t`): p. 74, f94; sgt1936 (`bpt6k91056547`): p. 54, f65; sgt1939 (`bpt6k9105739w`): p. 54, f60.

Transcriptions: `../transcribed/property_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_property.py build`.

Rows: 216. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939.

Unit: number of properties (immeubles).

Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, with `year`; no year is printed by two editions.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: `legal_status`
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (the edition year: each edition prints the table for its own year)
- `legal_status`: `melk` (freehold), `enzel` (perpetual-rent tenure), `habous` (mortmain endowment)
- `legal_status_fr`: as printed
- `outcome`: result of the registration proceeding
- `outcome_fr`: printed column heading
- `seat`: `tunis` or `sousse` (siège of the Tribunal mixte)
- `seat_fr`: as printed
- `value`: number of properties
- `flag`: empty, or `total_mismatch` (printed value kept), `derived_from_totals`, `row_realigned`, `not_applicable` (nothing printed)

Failed checks (printed errors, re-read on crops): sgt1923 brace total immatriculation printed 796 for 223 + 73 = 296; sgt1924 Totaux printed 389 for lines and columns summing to 387 (the jugements définitifs and "nombre total des immeubles" give 387).

Survey of the whole chapter in every edition: `property_survey.md`.

## Validation

- Checks against printed totals and identities: 168; passed: 165; failed: 3.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1923 p.89 (f591) legal_status Total@pair imm.tunis+imm.sousse: cells give 296, printed 796 (difference 500)
  - sgt1924 p.91 (f1081) legal_status Total: total = imm.tunis + imm.sousse + rej.tunis + rej.sousse + rad.tunis + rad.sousse: cells give 387, printed 389 (difference 2)
  - sgt1924 p.91 (f1081) legal_status total: lines vs Total: cells give 387, printed 389 (difference 2)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (12 printings): sgt1922 f107, sgt1923 f591, sgt1924 f1081, sgt1925 f117, sgt1926 f668, sgt1927 f130, sgt1928 f654, sgt1929 f132, sgt1930 f666, sgt1935 f94, sgt1936 f65, sgt1939 f60.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
