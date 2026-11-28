# Résultats des instances d'immatriculation. d) Jugement des oppositions

*Results of the registration proceedings: oppositions judged, by decision and seat.*

Source: *Statistique générale de la Tunisie*, chapter *Propriété immobilière / Tribunal mixte / Propriété foncière*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 84, f108; sgt1923 (`bpt6k9105649x`): p. 90, f592; sgt1924 (`bpt6k9105649x`): p. 92, f1082; sgt1925 (`bpt6k9105650k`): p. 94, f118; sgt1926 (`bpt6k9105650k`): p. 105, f669; sgt1927 (`bpt6k91056510`): p. 103, f131; sgt1928 (`bpt6k91056510`): p. 103, f655; sgt1929 (`bpt6k9105652d`): p. 105, f133; sgt1930 (`bpt6k9105652d`): p. 109, f667; sgt1935 (`bpt6k9105653t`): p. 75, f95.

Transcriptions: `../transcribed/property_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_property.py build`.

Rows: 94. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935.

Unit: number of oppositions.

Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, with `year`; no year is printed by two editions.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: `oppositions`
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (the edition year: each edition prints the table for its own year)
- `decision`: `accepted`, `rejected`, `withdrawn` (suivies de désistement), `not_ruled` (sur lesquelles il n'a pas été statué), `referred` (renvoyées devant les juridictions de droit commun)
- `decision_fr`: printed line heading
- `seat`: `tunis` or `sousse` (siège of the Tribunal mixte)
- `seat_fr`: as printed
- `value`: number of oppositions
- `flag`: empty, or `total_mismatch` (printed value kept), `derived_from_totals`, `row_realigned`, `not_applicable` (nothing printed)

Not printed in sgt1936 and sgt1939. sgt1935 prints the Totaux line with both seats and the grand total (no brace total). sgt1929: nothing printed under Tunis for "sur lesquelles il n'a pas été statué" (NA, `not_applicable`).

Survey of the whole chapter in every edition: `property_survey.md`.

## Validation

- Checks against printed totals and identities: 75; passed: 75; failed: 0.

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: not_applicable: 1.

  - sgt1929 p.105 1929 not_ruled / tunis = NA (not_applicable)

## Image versus OCR

- Read cell by cell on the page images (10 printings): sgt1922 f108, sgt1923 f592, sgt1924 f1082, sgt1925 f118, sgt1926 f669, sgt1927 f131, sgt1928 f655, sgt1929 f133, sgt1930 f667, sgt1935 f95.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
