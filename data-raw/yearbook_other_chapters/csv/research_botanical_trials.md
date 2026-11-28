# Service botanique. a) Nature et nombre des essais de variétés nouvelles

*Botanical service: number of trials of new varieties, by nature of the plants and season.*

Source: *Statistique générale de la Tunisie*, chapter *Institutions d'enseignement et de recherches*, editions sgt1922, sgt1923, sgt1924, sgt1925. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 253, f277; sgt1923 (`bpt6k9105649x`): p. 266, f768; sgt1924 (`bpt6k9105649x`): p. 282, f1272; sgt1925 (`bpt6k9105650k`): p. 314, f338.

Transcriptions: `../transcribed/research_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_research.py build`.

Rows: 187. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925.

Unit: trials (count); value_type: count.

Selection (SPEC_ADDENDUM rule 4): each cell is stored once, from the latest edition printing it; every other printing of the same cell is compared below.

## Columns

- `census`: source edition (`sgt1922` ... `sgt1939`)
- `table_id`: section code of the transcription
- `gallica_ark`: Gallica volume ark
- `source_page`: printed page number
- `gallica_view`: Gallica view
- `year`: year of the figure (for a school year or season: the year it ends; for promotions and once-per-edition tables: the edition year)
- `section`: section of the trials table (agricole, horticole)
- `section_fr`: section heading
- `season`: season (année) as printed
- `plant`: ASCII slug of `plant_fr`
- `plant_fr`: nature des plantes as printed
- `value`: printed figure (» = 0)
- `flag`: empty, or ocr_corrected / illegible / total_mismatch / derived_from_totals / not_applicable / reprint_corrected / row_realigned

The 'Total antérieur' column (all trials before the first season printed) is stored with `year` empty and `season` naming the edition's first season; it changes from edition to edition and is compared only between editions printing the same first season. Total général and Totaux are checks only.

Every failed check below was re-read on a zoomed native-resolution crop: they are printed inconsistencies (printed values kept). 

Survey of the whole chapter in every edition: `research_survey.md`.

## Validation

- Checks against printed totals and identities: 148; passed: 142; failed: 6.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1923 p.266 (f768) bot_trials Sorghos: total = sum: cells give 23, printed 12 (difference -11)
  - sgt1923 p.266 (f768) bot_trials Plantes médicinales: total = sum: cells give 58, printed 47 (difference -11)
  - sgt1923 p.266 (f768) bot_trials 1923: lines vs Totaux: cells give 161, printed 139 (difference -22)
  - sgt1924 p.282 (f1272) bot_trials Sorghos: total = sum: cells give 27, printed 16 (difference -11)
  - sgt1924 p.282 (f1272) bot_trials Plantes médicinales: total = sum: cells give 58, printed 47 (difference -11)
  - sgt1924 p.282 (f1272) bot_trials 1923: lines vs Totaux: cells give 161, printed 139 (difference -22)

- Overlapping printings: 297 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (8 printings): sgt1922 f277, sgt1922 f277, sgt1923 f768, sgt1923 f768, sgt1924 f1272, sgt1924 f1272, sgt1925 f338, sgt1925 f338.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
