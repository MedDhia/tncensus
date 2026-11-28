# Grèves. b) Grèves survenues de <année> à <année>

*Strikes per year: number, duration, establishments, strikers and results.*

Source: *Statistique générale de la Tunisie*, chapter *Travail et prévoyance sociale*, editions sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1925 (`bpt6k9105650k`): p. 492, f516, p. 493, f517; sgt1926 (`bpt6k9105650k`): p. 478, f1042, p. 479, f1043; sgt1927 (`bpt6k91056510`): p. 480, f508, p. 481, f509; sgt1928 (`bpt6k91056510`): p. 486, f1038, p. 487, f1039; sgt1929 (`bpt6k9105652d`): p. 488, f516, p. 489, f517; sgt1930 (`bpt6k9105652d`): p. 494, f1052, p. 495, f1053; sgt1935 (`bpt6k9105653t`): p. 306, f326, p. 307, f327; sgt1936 (`bpt6k91056547`): p. 182, f193, p. 183, f194; sgt1939 (`bpt6k9105739w`): p. 164, f170, p. 165, f171.

Transcriptions: `../transcribed/labour_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_labour.py build`.

Rows: 168. Years: 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Units: count and days (`unit`); value_type: count.

Printed for overlapping windows: each cell is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (rule 4 series: the latest edition printing it; rule 5: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (two-page spreads: the page the cell is printed on)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (HBM: last year of the printed period)
- `measure`: measure code (English)
- `measure_fr`: printed heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, ocr_corrected, illegible, total_mismatch, derived_from_totals, not_applicable, reprint_corrected or row_realigned

Ten-year window in every edition (sgt1925 1916-1925 ... sgt1939 1930-1939). 1916-1918 printed » (no strike). Check: strikes = réussite + transaction + échec. 1936 (sgt1936, sgt1939): 50 strikes, results printed » » » (not given): the identity fails for 1936 (printed values kept). The yearly line agrees with the detailed list of the edition year where both exist (see `labour_strike_details`).

Every failed check below was re-read on a zoomed native-resolution crop (or recurs unchanged in independent readings of several editions): printed values are kept. 1936: 50 strikes, results printed » » » (not given), in sgt1936 and sgt1939.

Survey of the whole chapter in every edition: `labour_survey.md`.

## Validation

- Checks against printed totals and identities: 90; passed: 88; failed: 2.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1936 p.182 (f193) strikes 1936: strikes = success + transaction + failure: cells give 0, printed 50 (difference 50)
  - sgt1939 p.164 (f170) strikes 1936: strikes = success + transaction + failure: cells give 0, printed 50 (difference 50)

- Overlapping printings: 462 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (9 printings): sgt1925 f516, sgt1926 f1042, sgt1927 f508, sgt1928 f1038, sgt1929 f516, sgt1930 f1052, sgt1935 f326, sgt1936 f193, sgt1939 f170.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
