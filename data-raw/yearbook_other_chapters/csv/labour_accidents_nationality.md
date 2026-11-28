# Accidents du travail. a) Répartition des accidents d'après la nationalité des victimes

*Industrial accidents by occupational category and nationality of the victim.*

Source: *Statistique générale de la Tunisie*, chapter *Travail et prévoyance sociale*, editions sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1925 (`bpt6k9105650k`): p. 491, f515; sgt1926 (`bpt6k9105650k`): p. 475, f1039; sgt1927 (`bpt6k91056510`): p. 476, f504; sgt1928 (`bpt6k91056510`): p. 482, f1034; sgt1929 (`bpt6k9105652d`): p. 484, f512; sgt1930 (`bpt6k9105652d`): p. 490, f1048; sgt1935 (`bpt6k9105653t`): p. 302, f322; sgt1936 (`bpt6k91056547`): p. 179, f190; sgt1939 (`bpt6k9105739w`): p. 160, f166.

Transcriptions: `../transcribed/labour_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_labour.py build`.

Rows: 447. Years: 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939.

Unit: accidents; value_type: count.

Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept, with `year` (the edition year when no year is printed); a year printed by two editions is stored once, from the later one, and compared.

## Columns

- `census`: edition the value is taken from (rule 4 series: the latest edition printing it; rule 5: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (two-page spreads: the page the cell is printed on)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (HBM: last year of the printed period)
- `category`: occupational category (English code; the list changes in sgt1927 and sgt1936)
- `category_fr`: category as printed
- `nationality`: nationality of the victims / immigrants (English code)
- `nationality_fr`: printed heading
- `value`: printed value (» = 0)
- `flag`: empty, ocr_corrected, illegible, total_mismatch, derived_from_totals, not_applicable, reprint_corrected or row_realigned

Printed in every edition sgt1925-sgt1939 without a year in the title: `year` = edition year. Categories: 13 'professions' in sgt1925-sgt1926, 14 'catégories professionnelles' from sgt1927, 7 in sgt1936. Nationality columns: Français, Italiens, Indigènes, Etrangers (sgt1925-sgt1926); Français, Indigènes (from sgt1935 'Tunisiens'), Italiens, Autres étrangers. The row totals and the Totaux line are checks only.

sgt1936: footnote (1) 'Le dépouillement par nationalité n'a pu être effectué en 1936'; the nationality columns are printed » throughout and not stored; the category totals are stored (`nationality` = `TOTAL (printed)`). Their printed TOTAL 18.930 exceeds the sum of the seven lines (17.972) by 958; every figure re-read on a crop.

Flagged `total_mismatch` (printed value kept; the row total and the column total both need the same other figure): sgt1935 Mines / autres étrangers printed 11 (511 needed); sgt1939 Transports / Italiens printed 295 (292 needed).

Every failed check below was re-read on a zoomed native-resolution crop (or recurs unchanged in independent readings of several editions): printed values are kept. sgt1935 Mines / autres étrangers 11 for 511 and sgt1939 Transports / Italiens 295 for 292 are flagged `total_mismatch`; sgt1936's printed TOTAL 18.930 against 17.972.

Survey of the whole chapter in every edition: `labour_survey.md`.

## Validation

- Checks against printed totals and identities: 159; passed: 152; failed: 7.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1925 p.491 (f515) acc_nat Mines et Carrières: total = french + italian + indigenous + foreign: cells give 3715, printed 3735 (difference 20)
  - sgt1925 p.491 (f515) acc_nat indigenous: lines vs Totaux: cells give 8922, printed 8942 (difference 20)
  - sgt1935 p.302 (f322) acc_nat Mines: total = french + indigenous + italian + foreign: cells give 1264, printed 1764 (difference 500)
  - sgt1935 p.302 (f322) acc_nat foreign: lines vs Totaux: cells give 120, printed 620 (difference 500)
  - sgt1936 p.179 (f190) acc_nat total: lines vs Total: cells give 17972, printed 18930 (difference 958)
  - sgt1939 p.160 (f166) acc_nat Transports : chemins de fer et tramways, autres transports par terre et entrepôts, poste et télégraphe, navigation aérienne et maritime: total = french + indigenous + italian + foreign: cells give 2542, printed 2539 (difference -3)
  - sgt1939 p.160 (f166) acc_nat italian: lines vs Totaux: cells give 1642, printed 1639 (difference -3)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: total_mismatch: 3.

  - sgt1925 p.491 1925 mines_quarries / indigenous = 3335 (total_mismatch)
  - sgt1935 p.302 1935 mines / foreign = 11 (total_mismatch)
  - sgt1939 p.160 1939 transport / italian = 295 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (9 printings): sgt1925 f515, sgt1926 f1039, sgt1927 f504, sgt1928 f1034, sgt1929 f512, sgt1930 f1048, sgt1935 f322, sgt1936 f190, sgt1939 f166.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
