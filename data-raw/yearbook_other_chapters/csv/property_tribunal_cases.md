# Tribunal mixte. Travaux du Tribunal : a) Statistique des affaires

*Tribunal mixte (land registration court): cases and work of the court, by seat.*

Source: *Statistique générale de la Tunisie*, chapter *Propriété immobilière / Tribunal mixte / Propriété foncière*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 81, f105; sgt1923 (`bpt6k9105649x`): p. 87, f589; sgt1924 (`bpt6k9105649x`): p. 89, f1079; sgt1925 (`bpt6k9105650k`): p. 91, f115; sgt1926 (`bpt6k9105650k`): p. 102, f666; sgt1927 (`bpt6k91056510`): p. 100, f128; sgt1928 (`bpt6k91056510`): p. 100, f652; sgt1929 (`bpt6k9105652d`): p. 102, f130; sgt1930 (`bpt6k9105652d`): p. 106, f664; sgt1935 (`bpt6k9105653t`): p. 72, f92; sgt1936 (`bpt6k91056547`): p. 52, f63; sgt1939 (`bpt6k9105739w`): p. 52, f58.

Transcriptions: `../transcribed/property_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_property.py build`.

Rows: 306. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939.

Unit: number of cases (affaires, réquisitions), hearings, judgments, inspections, expert reports.

Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, with `year`; no year is printed by two editions.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section: `cases` (upper part: cases pending, entered, judged), `activity` (lower part: requisitions, hearings, judgments, inspections, expert reports)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (the edition year: each edition prints the table for its own year)
- `seat`: `tunis` or `sousse` (siège of the Tribunal mixte)
- `seat_fr`: as printed
- `measure`: `pending_start`, `entered`, `judged`, `pending_end` (cases); `requisitions`, `hearings`, `judg_registration`, `judg_rejection`, `judg_radiation`, `interlocutory`, `rectification`, `inspections`, `expertises`
- `measure_fr`: printed line heading (the wording of the upper part changes in sgt1925; both given)
- `value`: count
- `flag`: empty, or `total_mismatch` (printed value kept), `derived_from_totals`, `row_realigned`, `not_applicable` (nothing printed)

Failed checks, all printed errors confirmed on native-resolution crops: sgt1923 line 4° (jugements avant faire droit) Tunis 254 + Sousse 76 = 330, Total printed 334, and line 5° Tunis printed 7 with Total »; sgt1924 Tunis Total printed 1.058 for 956 + 552 = 1.508 (the general total 1.912 = 1.508 + 404 agrees with the cells); sgt1925 line 5° Tunis 1 with Total »; sgt1928 Sousse: 306 + 157 = 463, Total printed 453, and Tunis 1.670 + 591 − 536 = 1.725 for a printed 1.727 (Sousse: 342 printed, 352 by the identity; sgt1929 opens 1929 with 1.727 and 350).

Continuity (comparison, not a check): cases pending at 31 December of year N−1 as printed by edition N against cases pending at 31 December as printed by edition N−1 (consecutive years only): see `property_validation.json` (`continuity`).

Continuity: 18 comparisons, 3 differences: tunis: sgt1925 pending at 31 Dec 1925 = 1149, sgt1926 pending at the start = 1151; tunis: sgt1927 pending at 31 Dec 1927 = 1672, sgt1928 pending at the start = 1670; sousse: sgt1928 pending at 31 Dec 1928 = 342, sgt1929 pending at the start = 350.

Survey of the whole chapter in every edition: `property_survey.md`.

## Validation

- Checks against printed totals and identities: 171; passed: 164; failed: 7.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1923 p.87 (f589) activity interlocutory: total = tunis + sousse: cells give 330, printed 334 (difference 4)
  - sgt1923 p.87 (f589) activity rectification: total = tunis + sousse: cells give 7, printed 0 (difference -7)
  - sgt1924 p.89 (f1079) cases tunis: Total = pending_start + entered: cells give 1508, printed 1058 (difference -450)
  - sgt1925 p.91 (f115) activity rectification: total = tunis + sousse: cells give 1, printed 0 (difference -1)
  - sgt1928 p.100 (f652) cases tunis: pending_end = pending_start + entered - judged: cells give 1725, printed 1727 (difference 2)
  - sgt1928 p.100 (f652) cases sousse: pending_end = pending_start + entered - judged: cells give 352, printed 342 (difference -10)
  - sgt1928 p.100 (f652) cases sousse: Total = pending_start + entered: cells give 463, printed 453 (difference -10)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (24 printings): sgt1922 f105, sgt1922 f105, sgt1923 f589, sgt1923 f589, sgt1924 f1079, sgt1924 f1079, sgt1925 f115, sgt1925 f115, sgt1926 f666, sgt1926 f666, sgt1927 f128, sgt1927 f128, sgt1928 f652, sgt1928 f652, sgt1929 f130, sgt1929 f130, sgt1930 f664, sgt1930 f664, sgt1935 f92, sgt1935 f92, sgt1936 f63, sgt1936 f63, sgt1939 f58, sgt1939 f58.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
