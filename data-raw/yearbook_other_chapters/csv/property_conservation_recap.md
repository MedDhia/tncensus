# Conservation foncière. Récapitulation : a) Nombre de demandes déposées et de titres créés ; b) Rentes d'enzel et créances hypothécaires inscrites

*Land registry: cumulative summary at 31 December (requisitions filed and finally decided, titles created) and enzel rents and mortgage claims registered.*

Source: *Statistique générale de la Tunisie*, chapter *Propriété immobilière / Tribunal mixte / Propriété foncière*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 87, f111; sgt1923 (`bpt6k9105649x`): p. 93, f595; sgt1924 (`bpt6k9105649x`): p. 95, f1085; sgt1925 (`bpt6k9105650k`): p. 97, f121; sgt1926 (`bpt6k9105650k`): p. 108, f672; sgt1927 (`bpt6k91056510`): p. 106, f134; sgt1928 (`bpt6k91056510`): p. 106, f658; sgt1929 (`bpt6k9105652d`): p. 108, f136; sgt1930 (`bpt6k9105652d`): p. 112, f670; sgt1935 (`bpt6k9105653t`): p. 77, f97; sgt1936 (`bpt6k91056547`): p. 56, f67; sgt1939 (`bpt6k9105739w`): p. 56, f62.

Transcriptions: `../transcribed/property_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_property.py build`.

Rows: 132. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939.

Units: count, hectares, francs (`unit`). Mixed table. All figures are cumulative since 1886 at 31 December of the edition year.

Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, with `year`; no year is printed by two editions.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: `recap` (a) or `registered` (b)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (31 December of the edition year)
- `measure`: `demands`, `area_declared`, `value_declared`, `solved`, `area_registered`, `value_registered`, `titles_established`, `titles_mutation`, `titles_total`; `enzel_rents`, `mortgage_claims`
- `measure_fr`: printed heading
- `unit`: `count`, `hectares` or `francs`
- `value`: count, hectares or francs
- `flag`: empty, or `total_mismatch` (printed value kept), `derived_from_totals`, `row_realigned`, `not_applicable` (nothing printed)

One row per measure and edition: cumulative figures since 1886 at 31 December of the edition year, stored as printed (the table exists only as totals). Contenances are printed in whole hectares here. Checks against the Totaux of the requisitions and titles tables (area truncated to the hectare).

Failed checks: sgt1924 valeur 222.114.176 against the titles Totaux 232.114.176 (the titles lines agree with 222.114.176); sgt1927 contenances 1.996.430 against the requisitions Totaux 1.996.340 (the lines agree with 1.996.430); sgt1930 valeurs déclarées 553.301.391 against the requisitions Totaux 553.101.391; sgt1939 valeur 621.233.914 against the titles Totaux 621.233.714 and titres établis 19.369 against 19.349.

Survey of the whole chapter in every edition: `property_survey.md`.

## Validation

- Checks against printed totals and identities: 96; passed: 91; failed: 5.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1924 p.95 (f1085) recap value_registered = titles Totaux value: cells give 232114176, printed 222114176 (difference -10000000)
  - sgt1927 p.106 (f134) recap area_declared = requisitions Totaux area: cells give 1996340, printed 1996430 (difference 90)
  - sgt1930 p.112 (f670) recap value_declared = requisitions Totaux value: cells give 553101391, printed 553301391 (difference 200000)
  - sgt1939 p.56 (f62) recap value_registered = titles Totaux value: cells give 621233714, printed 621233914 (difference 200)
  - sgt1939 p.56 (f62) recap titles_established = titles Totaux judgment: cells give 19349, printed 19369 (difference 20)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (24 printings): sgt1922 f111, sgt1922 f111, sgt1923 f595, sgt1923 f595, sgt1924 f1085, sgt1924 f1085, sgt1925 f121, sgt1925 f121, sgt1926 f672, sgt1926 f672, sgt1927 f134, sgt1927 f134, sgt1928 f658, sgt1928 f658, sgt1929 f136, sgt1929 f136, sgt1930 f670, sgt1930 f670, sgt1935 f97, sgt1935 f97, sgt1936 f67, sgt1936 f67, sgt1939 f62, sgt1939 f62.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
