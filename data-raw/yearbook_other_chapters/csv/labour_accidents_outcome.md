# Accidents du travail. b) Répartition d'après la gravité / Suites connues ou probables des accidents

*Industrial accidents by occupational category and outcome (deaths, incapacity).*

Source: *Statistique générale de la Tunisie*, chapter *Travail et prévoyance sociale*, editions sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1925 (`bpt6k9105650k`): p. 491, f515; sgt1926 (`bpt6k9105650k`): p. 475, f1039; sgt1927 (`bpt6k91056510`): p. 477, f505; sgt1928 (`bpt6k91056510`): p. 483, f1035; sgt1929 (`bpt6k9105652d`): p. 485, f513; sgt1930 (`bpt6k9105652d`): p. 491, f1049; sgt1935 (`bpt6k9105653t`): p. 303, f323; sgt1939 (`bpt6k9105739w`): p. 161, f167.

Transcriptions: `../transcribed/labour_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_labour.py build`.

Rows: 414. Years: 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1939.

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
- `outcome`: outcome of the accident (English code)
- `outcome_fr`: printed heading
- `value`: printed value (» = 0)
- `flag`: empty, ocr_corrected, illegible, total_mismatch, derived_from_totals, not_applicable, reprint_corrected or row_realigned

Printed sgt1925-sgt1935 and sgt1939 (not in sgt1936). sgt1925-sgt1926 'Répartition d'après la gravité': morts, incapacités de plus d'un mois, de moins d'un mois. From sgt1927 'Suites connues ou probables': morts, incapacité permanente, incapacité temporaire de plus de 4 jours, suites inconnues. `year` = edition year. Row totals and Totaux are checks only.

sgt1929 Commerce de gros, incapacité permanente: left blank in the print (stored NA, `not_applicable`; the row total gives 4, the column total 61). sgt1939: the TOTAUX column repeats the nationality table except Autres (145 / 153), three lines and three column totals do not add up (see the failed checks); every cell re-read on zoomed crops, no single faulty cell.

Every failed check below was re-read on a zoomed native-resolution crop (or recurs unchanged in independent readings of several editions): printed values are kept. sgt1928 Mines / morts printed 3 for 33 (flagged total_mismatch); sgt1939 (see above).

Survey of the whole chapter in every edition: `labour_survey.md`.

## Validation

- Checks against printed totals and identities: 155; passed: 146; failed: 9.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1928 p.483 (f1035) acc_sev Mines: total = dead + inc_perm + inc_temp + unknown: cells give 3884, printed 3914 (difference 30)
  - sgt1928 p.483 (f1035) acc_sev dead: lines vs Totaux: cells give 43, printed 73 (difference 30)
  - sgt1939 p.161 (f167) acc_sev Agriculture et forêts: total = dead + inc_perm + inc_temp + unknown: cells give 1858, printed 1866 (difference 8)
  - sgt1939 p.161 (f167) acc_sev Transports : chemins de fer et tramways, autres transports par terre et entrepôts, poste et télégraphe, navigation aérienne et maritime: total = dead + inc_perm + inc_temp + unknown: cells give 2533, printed 2539 (difference 6)
  - sgt1939 p.161 (f167) acc_sev Armées de terre et de mer: total = dead + inc_perm + inc_temp + unknown: cells give 108, printed 119 (difference 11)
  - sgt1939 p.161 (f167) acc_sev inc_perm: lines vs Totaux: cells give 169, printed 167 (difference -2)
  - sgt1939 p.161 (f167) acc_sev inc_temp: lines vs Totaux: cells give 11202, printed 11224 (difference 22)
  - sgt1939 p.161 (f167) acc_sev unknown: lines vs Totaux: cells give 703, printed 716 (difference 13)
  - sgt1939 p.161 (f167) acc_sev total: lines vs Totaux: cells give 12166, printed 12174 (difference 8)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: derived_from_totals: 2, total_mismatch: 1.

  - sgt1928 p.483 1928 mines / dead = 3 (total_mismatch)
  - sgt1929 p.485 1929 mines / permanent_incapacity = 63 (derived_from_totals)
  - sgt1929 p.485 1929 commerce_banking / permanent_incapacity = 4 (derived_from_totals)

## Image versus OCR

- Read cell by cell on the page images (8 printings): sgt1925 f515, sgt1926 f1039, sgt1927 f505, sgt1928 f1035, sgt1929 f513, sgt1930 f1049, sgt1935 f323, sgt1939 f167.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
