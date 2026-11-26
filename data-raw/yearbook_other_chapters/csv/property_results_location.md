# Résultats des instances d'immatriculation. b) Situation des immeubles

*Results of the registration proceedings: urban and rural properties by legal status, outcome and seat.*

Source: *Statistique générale de la Tunisie*, chapter *Propriété immobilière / Tribunal mixte / Propriété foncière*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 83, f107; sgt1923 (`bpt6k9105649x`): p. 89, f591; sgt1924 (`bpt6k9105649x`): p. 91, f1081; sgt1925 (`bpt6k9105650k`): p. 93, f117; sgt1926 (`bpt6k9105650k`): p. 104, f668; sgt1927 (`bpt6k91056510`): p. 102, f130; sgt1928 (`bpt6k91056510`): p. 102, f654; sgt1929 (`bpt6k9105652d`): p. 104, f132; sgt1930 (`bpt6k9105652d`): p. 108, f666; sgt1935 (`bpt6k9105653t`): p. 74, f94; sgt1936 (`bpt6k91056547`): p. 54, f65; sgt1939 (`bpt6k9105739w`): p. 54, f60.

Transcriptions: `../transcribed/property_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_property.py build`.

Rows: 432. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939.

Unit: number of properties.

Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, with `year`; no year is printed by two editions.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: `location`
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (the edition year: each edition prints the table for its own year)
- `location`: `urban` or `rural`
- `location_fr`: as printed
- `legal_status`: `melk` (freehold), `enzel` (perpetual-rent tenure), `habous` (mortmain endowment)
- `legal_status_fr`: as printed
- `outcome`: result of the registration proceeding
- `outcome_fr`: printed column heading
- `seat`: `tunis` or `sousse` (siège of the Tribunal mixte)
- `seat_fr`: as printed
- `value`: number of properties
- `flag`: empty, or `total_mismatch` (printed value kept), `derived_from_totals`, `row_realigned`, `not_applicable` (nothing printed)

Check against a): urban + rural = legal status a) for each status, outcome and seat.

Failed checks (printed errors): sgt1924 brace total rural immatriculation 173 for 139 + 44 = 183, and the radiation Tunis 2 is printed under enzel (urban) here but under melk in a); sgt1926 urban melk printed total 108 with a radiation Sousse 1 that neither the urban Totaux (») nor a) counts; sgt1930 rejet Sousse: melk 5 + 4 = 9 for a) 8 and habous 0 + 1 for a) 2; sgt1936 immatriculation Tunis: melk 136 + 144 = 280 for a) 279, enzel 45 + 21 = 66 for a) 67.

Flagged cells: sgt1926 location urban.melk / rad.sousse: printed 1; its line and its column are both -1 off their printed totals (printed value kept).

Survey of the whole chapter in every edition: `property_survey.md`.

## Validation

- Checks against printed totals and identities: 600; passed: 584; failed: 16.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1924 p.91 (f1081) location Total@pair rural imm.tunis+imm.sousse: cells give 183, printed 173 (difference -10)
  - sgt1924 p.91 (f1081) location melk rad.tunis: urban + rural = a): cells give 0, printed 2 (difference 2)
  - sgt1924 p.91 (f1081) location melk total: urban + rural = a): cells give 236, printed 238 (difference 2)
  - sgt1924 p.91 (f1081) location enzel rad.tunis: urban + rural = a): cells give 2, printed 0 (difference -2)
  - sgt1924 p.91 (f1081) location enzel total: urban + rural = a): cells give 136, printed 134 (difference -2)
  - sgt1926 p.104 (f668) location urban.melk: total = imm.tunis + imm.sousse + rej.tunis + rej.sousse + rad.tunis + rad.sousse: cells give 109, printed 108 (difference -1)
  - sgt1926 p.104 (f668) location rad.sousse: lines vs Total urban: cells give 1, printed 0 (difference -1)
  - sgt1926 p.104 (f668) location melk rad.sousse: urban + rural = a): cells give 1, printed 0 (difference -1)
  - sgt1930 p.108 (f666) location melk rej.sousse: urban + rural = a): cells give 9, printed 8 (difference -1)
  - sgt1930 p.108 (f666) location melk total: urban + rural = a): cells give 355, printed 354 (difference -1)
  - sgt1930 p.108 (f666) location habous rej.sousse: urban + rural = a): cells give 1, printed 2 (difference 1)
  - sgt1930 p.108 (f666) location habous total: urban + rural = a): cells give 63, printed 64 (difference 1)
  - sgt1936 p.54 (f65) location melk imm.tunis: urban + rural = a): cells give 280, printed 279 (difference -1)
  - sgt1936 p.54 (f65) location melk total: urban + rural = a): cells give 395, printed 394 (difference -1)
  - sgt1936 p.54 (f65) location enzel imm.tunis: urban + rural = a): cells give 66, printed 67 (difference 1)
  - sgt1936 p.54 (f65) location enzel total: urban + rural = a): cells give 76, printed 77 (difference 1)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: total_mismatch: 1.

  - sgt1926 p.104 1926 urban / melk / radiation / sousse = 1 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (12 printings): sgt1922 f107, sgt1923 f591, sgt1924 f1081, sgt1925 f117, sgt1926 f668, sgt1927 f130, sgt1928 f654, sgt1929 f132, sgt1930 f666, sgt1935 f94, sgt1936 f65, sgt1939 f60.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
