# Placement. Opérations de l'Office du Placement Français en Tunisie

*French Placement Office in Tunisia: job applications, offers and placements by occupation.*

Source: *Statistique générale de la Tunisie*, chapter *Travail et prévoyance sociale*, editions sgt1927, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1927 (`bpt6k91056510`): p. 480, f508; sgt1929 (`bpt6k9105652d`): p. 488, f516; sgt1930 (`bpt6k9105652d`): p. 494, f1052, p. 495, f1053; sgt1935 (`bpt6k9105653t`): p. 306, f326, p. 307, f327; sgt1936 (`bpt6k91056547`): p. 182, f193; sgt1939 (`bpt6k9105739w`): p. 164, f170, p. 165, f171.

Transcriptions: `../transcribed/labour_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_labour.py build`.

Rows: 480. Years: 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Unit: applications / offers / placements; value_type: count.

Printed for overlapping windows: each cell is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (rule 4 series: the latest edition printing it; rule 5: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (two-page spreads: the page the cell is printed on)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (HBM: last year of the printed period)
- `occupation`: occupational category (English code)
- `occupation_fr`: occupation as printed
- `measure`: measure code (English)
- `measure_fr`: printed heading
- `value`: printed value (» = 0)
- `flag`: empty, ocr_corrected, illegible, total_mismatch, derived_from_totals, not_applicable, reprint_corrected or row_realigned

Printed sgt1926 (1920-1926) to sgt1939 (1930-1939); not in sgt1925. Eight occupational lines; the 7th, 'Services publics', is headed 'Industrie hôtelière' in sgt1936 and sgt1939 with the same figures for every year printed before (stored as one line, `public_services`, `occupation_fr` as printed in the stored edition); 'Commerce et Industrie' is headed 'Commerce et transports terrestres' in sgt1939 (same figures). Totaux lines are checks only.

Misprints replaced by an earlier printing (`reprint_corrected`): 1923 Métallurgie placements 84 in sgt1928-sgt1930 (sgt1926-sgt1927 34; Totaux 455 needs 34); 1928 Métallurgie placements 39 in sgt1936 (99); 1932 Services publics / Industrie hôtelière demandes 296 in sgt1936-sgt1939 (sgt1935 6.200); 1933 Divers placements '611' in sgt1936-sgt1939 (leading digit lost; sgt1935 2.611). sgt1926 1922 Bâtiment placements: first digit blotted, 11 from the Totaux (`derived_from_totals`; later editions print 11). Cells hidden in the gutter (sgt1935 1929 placements and 1930 applications) are `illegible` and taken from later printings.

Every failed check below was re-read on a zoomed native-resolution crop (or recurs unchanged in independent readings of several editions): printed values are kept. The 1923 offres Totaux 588 for lines summing to 587 (sgt1928-sgt1930); 1934 applications Totaux 11.735 for 11.734 (sgt1935-sgt1939); 1936 applications 6.711 for 7.350 in sgt1936 (sgt1939 prints 7.350) and placements 3.601 for 3.600 (both editions); 1939 offers 2.688 for 2.698; and the totals of the lines replaced from an earlier printing (failures computed on the cells as printed).

Survey of the whole chapter in every edition: `labour_survey.md`.

## Validation

- Checks against printed totals and identities: 213; passed: 196; failed: 17.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1928 p.486 (f1038) placement o1923: lines vs Totaux: cells give 587, printed 588 (difference 1)
  - sgt1928 p.486 (f1038) placement p1923: lines vs Totaux: cells give 505, printed 455 (difference -50)
  - sgt1929 p.488 (f516) placement o1923: lines vs Totaux: cells give 587, printed 588 (difference 1)
  - sgt1929 p.488 (f516) placement p1923: lines vs Totaux: cells give 505, printed 455 (difference -50)
  - sgt1930 p.494 (f1052) placement o1923: lines vs Totaux: cells give 587, printed 588 (difference 1)
  - sgt1930 p.494 (f1052) placement p1923: lines vs Totaux: cells give 505, printed 455 (difference -50)
  - sgt1935 p.306 (f326) placement d1934: lines vs Totaux: cells give 11734, printed 11735 (difference 1)
  - sgt1936 p.182 (f193) placement p1928: lines vs Totaux: cells give 1412, printed 1472 (difference 60)
  - sgt1936 p.182 (f193) placement d1932: lines vs Totaux: cells give 6067, printed 11971 (difference 5904)
  - sgt1936 p.182 (f193) placement d1934: lines vs Totaux: cells give 11734, printed 11735 (difference 1)
  - sgt1936 p.182 (f193) placement d1936: lines vs Totaux: cells give 7350, printed 6711 (difference -639)
  - sgt1936 p.182 (f193) placement p1936: lines vs Totaux: cells give 3600, printed 3601 (difference 1)
  - sgt1939 p.164 (f170) placement d1932: lines vs Totaux: cells give 6067, printed 11971 (difference 5904)
  - sgt1939 p.164 (f170) placement p1933: lines vs Totaux: cells give 2716, printed 716 (difference -2000)
  - sgt1939 p.164 (f170) placement d1934: lines vs Totaux: cells give 11734, printed 11735 (difference 1)
  - sgt1939 p.164 (f170) placement p1936: lines vs Totaux: cells give 3600, printed 3601 (difference 1)
  - sgt1939 p.164 (f170) placement o1939: lines vs Totaux: cells give 2698, printed 2688 (difference -10)

- Overlapping printings: 1253 cell comparisons with other editions printing the same cell; 8 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1923 / metallurgy / placements | sgt1926 | 34 | sgt1930 | 84 |
| 1923 / metallurgy / placements | sgt1927 | 34 | sgt1930 | 84 |
| 1928 / metallurgy / placements | sgt1928 | 99 | sgt1936 | 39 |
| 1928 / metallurgy / placements | sgt1929 | 99 | sgt1936 | 39 |
| 1928 / metallurgy / placements | sgt1930 | 99 | sgt1936 | 39 |
| 1928 / metallurgy / placements | sgt1935 | 99 | sgt1936 | 39 |
| 1932 / public_services / applications | sgt1935 | 6200 | sgt1939 | 296 |
| 1933 / miscellaneous / placements | sgt1935 | 2611 | sgt1939 | 611 |

- Flagged cells: reprint_corrected: 4.

  - sgt1927 p.480 1923 metallurgy / placements = 34 (reprint_corrected)
  - sgt1935 p.306 1928 metallurgy / placements = 99 (reprint_corrected)
  - sgt1935 p.307 1932 public_services / applications = 6200 (reprint_corrected)
  - sgt1935 p.307 1933 miscellaneous / placements = 2611 (reprint_corrected)

## Image versus OCR

- Read cell by cell on the page images (8 printings): sgt1926 f1042, sgt1927 f508, sgt1928 f1038, sgt1929 f516, sgt1930 f1052, sgt1935 f326, sgt1936 f193, sgt1939 f170.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
