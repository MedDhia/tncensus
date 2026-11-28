# Résultats des instances d'immatriculation. e) Nombre et qualité juridique, f) Nationalité des personnes dont la réquisition a reçu une solution définitive

*Results of the registration proceedings: claimants whose requisition was finally decided, by legal quality and by nationality, outcome and seat.*

Source: *Statistique générale de la Tunisie*, chapter *Propriété immobilière / Tribunal mixte / Propriété foncière*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 84, f108, p. 85, f109; sgt1923 (`bpt6k9105649x`): p. 90, f592, p. 91, f593; sgt1924 (`bpt6k9105649x`): p. 92, f1082, p. 93, f1083; sgt1925 (`bpt6k9105650k`): p. 94, f118, p. 95, f119; sgt1926 (`bpt6k9105650k`): p. 105, f669, p. 106, f670; sgt1927 (`bpt6k91056510`): p. 103, f131, p. 104, f132; sgt1928 (`bpt6k91056510`): p. 103, f655, p. 104, f656; sgt1929 (`bpt6k9105652d`): p. 105, f133, p. 106, f134; sgt1930 (`bpt6k9105652d`): p. 109, f667, p. 110, f668; sgt1935 (`bpt6k9105653t`): p. 75, f95, p. 76, f96; sgt1936 (`bpt6k91056547`): p. 55, f66; sgt1939 (`bpt6k9105739w`): p. 55, f61.

Transcriptions: `../transcribed/property_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_property.py build`.

Rows: 666. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939.

Unit: number of claimants (requérants).

Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, with `year`; no year is printed by two editions.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: `claimant_status` (e, by legal quality) or `claimant_nationality` (f, by nationality); the two are alternative breakdowns of the same claimants
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (the edition year: each edition prints the table for its own year)
- `legal_quality`: e) only: `owners`, `enzel_holders`, `real_right_holders`
- `legal_quality_fr`: printed line heading
- `nationality`: f) only: `french`, `italian`, `british` (*Anglais*), `greek`, `tunisian`, `german`, `spanish`, `swiss`, `belgian`, `foreign` (*Étrangers*, sgt1936), `other` (*Divers*)
- `nationality_fr`: as printed
- `outcome`: result of the registration proceeding
- `outcome_fr`: printed column heading
- `seat`: `tunis` or `sousse` (siège of the Tribunal mixte)
- `seat_fr`: as printed
- `value`: number of claimants
- `flag`: empty, or `total_mismatch` (printed value kept), `derived_from_totals`, `row_realigned`, `not_applicable` (nothing printed)

e) (legal quality) is printed up to sgt1935; f) (nationality) in every edition (labelled d) in sgt1936 and D. in sgt1939; sgt1936 prints three nationality lines (Français, Tunisiens, Étrangers) and no renounced column). Nationality lines vary between editions; lines printed with all cells » are stored as 0.

Failed checks (printed errors): sgt1923 e) Totaux rejet Tunis printed 48 for lines summing to 30 (f) prints 30; the Totaux général 604 agrees with 30); sgt1930 f) Espagnols printed 2 and 1 with a line total 1, and the immatriculation Tunis column total 863 needs Espagnols 0.

Flagged cells: sgt1930 claimant_nationality Espagnols / imm.tunis: printed 2; its line and its column are both -2 off their printed totals (printed value kept); sgt1936 claimant_nationality Français / rej.tunis: cell left blank in the printing; 6 from the line total 185 and the column total 68.

Survey of the whole chapter in every edition: `property_survey.md`.

## Validation

- Checks against printed totals and identities: 443; passed: 437; failed: 6.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1923 p.90 (f592) claimant_status Total: total = imm.tunis + imm.sousse + rej.tunis + rej.sousse + ren.tunis + ren.sousse: cells give 622, printed 604 (difference -18)
  - sgt1923 p.90 (f592) claimant_status rej.tunis: lines vs Total: cells give 30, printed 48 (difference 18)
  - sgt1923 p.90 (f592) claimant_status Total@pair rej.tunis+rej.sousse: cells give 95, printed 77 (difference -18)
  - sgt1930 p.110 (f668) claimant_nationality Espagnols: total = imm.tunis + imm.sousse + rej.tunis + rej.sousse + ren.tunis + ren.sousse: cells give 3, printed 1 (difference -2)
  - sgt1930 p.110 (f668) claimant_nationality imm.tunis: lines vs Total: cells give 865, printed 863 (difference -2)
  - sgt1923 p.91 (f593) claimant_nationality rej.tunis: f) Totaux = e) Totaux: cells give 48, printed 30 (difference -18)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: derived_from_totals: 1, total_mismatch: 1.

  - sgt1930 p.110 1930  / spanish / registration_obtained / tunis = 2 (total_mismatch)
  - sgt1936 p.55 1936  / french / requisition_rejected / tunis = 6 (derived_from_totals)

## Image versus OCR

- Read cell by cell on the page images (22 printings): sgt1922 f108, sgt1922 f109, sgt1923 f592, sgt1923 f593, sgt1924 f1082, sgt1924 f1083, sgt1925 f118, sgt1925 f119, sgt1926 f669, sgt1926 f670, sgt1927 f131, sgt1927 f132, sgt1928 f655, sgt1928 f656, sgt1929 f133, sgt1929 f134, sgt1930 f667, sgt1930 f668, sgt1935 f95, sgt1935 f96, sgt1936 f66, sgt1939 f61.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
