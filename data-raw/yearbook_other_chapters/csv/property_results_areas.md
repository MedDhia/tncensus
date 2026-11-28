# Résultats des instances d'immatriculation. c) Superficies

*Results of the registration proceedings: areas registered and areas refused or abandoned, by urban / rural, legal status and seat.*

Source: *Statistique générale de la Tunisie*, chapter *Propriété immobilière / Tribunal mixte / Propriété foncière*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 84, f108; sgt1923 (`bpt6k9105649x`): p. 90, f592; sgt1924 (`bpt6k9105649x`): p. 92, f1082; sgt1925 (`bpt6k9105650k`): p. 94, f118; sgt1926 (`bpt6k9105650k`): p. 105, f669; sgt1927 (`bpt6k91056510`): p. 103, f131; sgt1928 (`bpt6k91056510`): p. 103, f655; sgt1929 (`bpt6k9105652d`): p. 105, f133; sgt1930 (`bpt6k9105652d`): p. 109, f667; sgt1935 (`bpt6k9105653t`): p. 75, f95; sgt1936 (`bpt6k91056547`): p. 55, f66; sgt1939 (`bpt6k9105739w`): p. 55, f61.

Transcriptions: `../transcribed/property_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_property.py build`.

Rows: 288. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939.

Unit: hectares, as a decimal with four places (printed in hectares, ares and centiares: "4 30 43" = 4.3043 ha).

Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, with `year`; no year is printed by two editions.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: `areas`
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
- `value`: hectares (4 decimals = ares and centiares)
- `flag`: empty, or `total_mismatch` (printed value kept), `derived_from_totals`, `row_realigned`, `not_applicable` (nothing printed)

Totals: the TOTAUX column, the Totaux line, the brace totals and the *total des surfaces* are checks. Areas printed in hectares, ares, centiares (h. a. c.; sgt1936 heads "h. a." but prints three groups).

Failed checks (printed errors; every failing cell re-read on a crop): sgt1922 rural melk total and the Totaux total are 0,03 ha (3 a) more than the cells, the brace immatriculées 13.314 38 13 for cells summing to 13.314 37 23; sgt1926 Totaux: Tunis immatriculées 1 c short, the TOTAUX cell 64.064 37 52 for 64.064 37 25 (the total des surfaces prints 64.064 37 25); sgt1927 Totaux line: Sousse immatriculées printed 3.723 12 73 (the Tunis refused figure) and Tunis refused 5.093 39 13 (sgt1926's), with brace totals that agree with neither; sgt1928 urban enzel line and Sousse immatriculées column 1 c off; sgt1930 rural melk refusée Sousse printed 1.412 67 65 where the line total (22.741 20 93) and the column total (11.205 79 52) both need 11.142 67 65, and Sousse immatriculées column 0,05 short; sgt1935 rural enzel TOTAUX 824 22 03 for cells 804 22 03 (the grand total agrees with the cells); sgt1936 Totaux refusée Sousse printed 2.518 35 84 for cells 2.548 35 84 (the brace and grand totals need 2.548).

Flagged cells: sgt1928 areas urban.enzel / imm.sousse: printed 0.5253; its line and its column are both -0.0001 off their printed totals (printed value kept); sgt1930 areas rural.melk / ref.sousse: printed 1412.6765; its line and its column are both 9730.0000 off their printed totals (printed value kept); sgt1936 areas urban.enzel / imm.tunis: printed "2.84.·1" with a broken digit; 2 ha 84 a 51 c from the line total 3.03.46.

Survey of the whole chapter in every edition: `property_survey.md`.

## Validation

- Checks against printed totals and identities: 177; passed: 152; failed: 25.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.84 (f108) areas rural.melk: total = imm.tunis + imm.sousse + ref.tunis + ref.sousse: cells give 23873.7985, printed 23873.8285 (difference 0.0300)
  - sgt1922 p.84 (f108) areas Total: total = imm.tunis + imm.sousse + ref.tunis + ref.sousse: cells give 28542.0503, printed 28542.0803 (difference 0.0300)
  - sgt1922 p.84 (f108) areas Total@pair imm.tunis+imm.sousse: cells give 13314.3723, printed 13314.3813 (difference 0.0090)
  - sgt1926 p.105 (f669) areas Total: total = imm.tunis + imm.sousse + ref.tunis + ref.sousse: cells give 64064.3724, printed 64064.3752 (difference 0.0028)
  - sgt1926 p.105 (f669) areas imm.tunis: lines vs Total: cells give 19961.4304, printed 19961.4303 (difference -0.0001)
  - sgt1926 p.105 (f669) areas total: lines vs Total: cells give 64064.3725, printed 64064.3752 (difference 0.0027)
  - sgt1926 p.105 (f669) areas Total@pair imm.tunis+imm.sousse: cells give 44336.9515, printed 44336.9516 (difference 0.0001)
  - sgt1926 p.105 (f669) areas total: Total général = sum of total lines: cells give 64064.3752, printed 64064.3725 (difference -0.0027)
  - sgt1927 p.103 (f131) areas Total: total = imm.tunis + imm.sousse + ref.tunis + ref.sousse: cells give 26849.0683, printed 22883.8498 (difference -3965.2185)
  - sgt1927 p.103 (f131) areas imm.sousse: lines vs Total: cells give 1128.1728, printed 3723.1273 (difference 2594.9545)
  - sgt1927 p.103 (f131) areas ref.tunis: lines vs Total: cells give 3723.1273, printed 5093.3913 (difference 1370.2640)
  - sgt1927 p.103 (f131) areas Total@pair imm.tunis+imm.sousse: cells give 19561.3212, printed 16966.3667 (difference -2594.9545)
  - sgt1927 p.103 (f131) areas Total@pair ref.tunis+ref.sousse: cells give 7287.7471, printed 5917.4831 (difference -1370.2640)
  - sgt1928 p.103 (f655) areas urban.enzel: total = imm.tunis + imm.sousse + ref.tunis + ref.sousse: cells give 15.0985, printed 15.0984 (difference -0.0001)
  - sgt1928 p.103 (f655) areas imm.sousse: lines vs Total: cells give 3793.9464, printed 3793.9463 (difference -0.0001)
  - sgt1930 p.109 (f667) areas rural.melk: total = imm.tunis + imm.sousse + ref.tunis + ref.sousse: cells give 13011.2093, printed 22741.2093 (difference 9730.0000)
  - sgt1930 p.109 (f667) areas Total: total = imm.tunis + imm.sousse + ref.tunis + ref.sousse: cells give 26403.4468, printed 26403.4968 (difference 0.0500)
  - sgt1930 p.109 (f667) areas imm.sousse: lines vs Total: cells give 4723.2532, printed 4723.2032 (difference -0.0500)
  - sgt1930 p.109 (f667) areas ref.sousse: lines vs Total: cells give 1475.7952, printed 11205.7952 (difference 9730.0000)
  - sgt1930 p.109 (f667) areas Total@pair imm.tunis+imm.sousse: cells give 13403.6173, printed 13403.6673 (difference 0.0500)
  - sgt1935 p.75 (f95) areas rural.enzel: total = imm.tunis + imm.sousse + ref.tunis + ref.sousse: cells give 804.2203, printed 824.2203 (difference 20.0000)
  - sgt1935 p.75 (f95) areas total: lines vs Total: cells give 36481.1338, printed 36461.1338 (difference -20.0000)
  - sgt1936 p.55 (f66) areas Total: total = imm.tunis + imm.sousse + ref.tunis + ref.sousse: cells give 32555.9391, printed 32585.9391 (difference 30.0000)
  - sgt1936 p.55 (f66) areas ref.sousse: lines vs Total: cells give 2548.3584, printed 2518.3584 (difference -30.0000)
  - sgt1936 p.55 (f66) areas Total@pair ref.tunis+ref.sousse: cells give 9591.6902, printed 9621.6902 (difference 30.0000)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: derived_from_totals: 1, total_mismatch: 2.

  - sgt1928 p.103 1928 urban / enzel / registered / sousse = 0.5253 (total_mismatch)
  - sgt1930 p.109 1930 rural / melk / refused_or_abandoned / sousse = 1412.6765 (total_mismatch)
  - sgt1936 p.55 1936 urban / enzel / registered / tunis = 2.8451 (derived_from_totals)

## Image versus OCR

- Read cell by cell on the page images (12 printings): sgt1922 f108, sgt1923 f592, sgt1924 f1082, sgt1925 f118, sgt1926 f669, sgt1927 f131, sgt1928 f655, sgt1929 f133, sgt1930 f667, sgt1935 f95, sgt1936 f66, sgt1939 f61.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
