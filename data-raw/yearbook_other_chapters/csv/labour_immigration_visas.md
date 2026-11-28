# Immigration des travailleurs. Contrats de travail visés au cours de l'année 1939 ; répartition des visas accordés

*Immigrant workers: labour contracts visaed in 1939 (renewals, transfers, new immigrants) and new immigrants by trade and nationality.*

Source: *Statistique générale de la Tunisie*, chapter *Travail et prévoyance sociale*, editions sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1939 (`bpt6k9105739w`): p. 168, f174.

Transcriptions: `../transcribed/labour_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_labour.py build`.

Rows: 19. Years: 1939.

Unit: visas; value_type: count.

Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept, with `year` (the edition year when no year is printed); a year printed by two editions is stored once, from the later one, and compared.

## Columns

- `census`: edition the value is taken from (rule 4 series: the latest edition printing it; rule 5: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (two-page spreads: the page the cell is printed on)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (HBM: last year of the printed period)
- `item`: item (English code)
- `item_fr`: printed label
- `trade`: trade (corps de métier, English code)
- `trade_fr`: printed label
- `nationality`: nationality of the victims / immigrants (English code)
- `nationality_fr`: printed heading
- `value`: printed value (» = 0)
- `flag`: empty, ocr_corrected, illegible, total_mismatch, derived_from_totals, not_applicable, reprint_corrected or row_realigned

Printed in sgt1939 only (application of the decree of 20 February 1930). Visas accordés 397 and the bracketed 259 (renouvellements 183 + transferts 76) are totals used as checks; the trade x nationality table distributes the 138 new immigrants (its totals are checks). Bâtiment et Métallurgie / Suisses printed '–' (stored 0).

Survey of the whole chapter in every edition: `labour_survey.md`.

## Validation

- Checks against printed totals and identities: 13; passed: 13; failed: 0.

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (2 printings): sgt1939 f174, sgt1939 f174.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
