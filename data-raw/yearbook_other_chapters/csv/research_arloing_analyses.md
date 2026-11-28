# Institut Arloing. Analyses microbiologiques en vue des diagnostics

*Institut Arloing (veterinary bacteriology): diagnostic analyses by animal group and disease, chemical and wool analyses, auto-vaccines.*

Source: *Statistique générale de la Tunisie*, chapter *Institutions d'enseignement et de recherches*, editions sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1935 (`bpt6k9105653t`): p. 138, f158; sgt1936 (`bpt6k91056547`): p. 108, f119; sgt1939 (`bpt6k9105739w`): p. 112, f118.

Transcriptions: `../transcribed/research_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_research.py build`.

Rows: 285. Years: 1935, 1936, 1939.

Units: analyses (count), doses for the auto-vaccines (`unit`); value_type: count.

Selection (SPEC_ADDENDUM rule 5): printed once per edition (the edition's year); all editions kept.

## Columns

- `census`: source edition (`sgt1922` ... `sgt1939`)
- `table_id`: section code of the transcription
- `gallica_ark`: Gallica volume ark
- `source_page`: printed page number
- `gallica_view`: Gallica view
- `year`: year of the figure (for a school year or season: the year it ends; for promotions and once-per-edition tables: the edition year)
- `group`: group heading (ASCII slug of `group_fr`)
- `group_fr`: group heading as printed
- `item`: ASCII slug of `item_fr`
- `item_fr`: line as printed (sub-heading prefixed, ditto marks expanded)
- `unit`: unit of the line (francs, persons, analyses, doses, flacons, cc, tubes, ampoules, litres, samples, quintals, hectares, producers, count)
- `value`: printed figure (» = 0)
- `flag`: empty, or ocr_corrected / illegible / total_mismatch / derived_from_totals / not_applicable / reprint_corrected / row_realigned

Survey of the whole chapter in every edition: `research_survey.md`.

## Validation

- Checks against printed totals and identities: 1; passed: 1; failed: 0.

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (31 printings): sgt1935 f158, sgt1935 f158, sgt1935 f158, sgt1935 f158, sgt1935 f158, sgt1935 f158, sgt1935 f158, sgt1935 f158, sgt1935 f158, sgt1935 f158, sgt1935 f158, sgt1935 f158, sgt1936 f119, sgt1936 f119, sgt1936 f119, sgt1936 f119, sgt1936 f119, sgt1936 f119, sgt1936 f119, sgt1936 f119, sgt1936 f119, sgt1936 f119, sgt1939 f118, sgt1939 f118, sgt1939 f118, sgt1939 f118, sgt1939 f118, sgt1939 f118, sgt1939 f118, sgt1939 f118, sgt1939 f118.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
