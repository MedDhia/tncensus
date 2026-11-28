# Accidents du travail. b) Répartition d'après la gravité

*Industrial accidents by occupation and outcome (deaths, incapacity over / under one month), sgt1922-sgt1924.*

Source: *Statistique générale de la Tunisie*, chapter *Institutions économiques et sociales / Mutualité agricole*, editions sgt1922, sgt1923, sgt1924. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 435, f459; sgt1923 (`bpt6k9105649x`): p. 447, f949; sgt1924 (`bpt6k9105649x`): p. 457, f1447.

Transcriptions: `../transcribed/mutuality_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_mutuality.py build`.

Rows: 117. Years: 1922, 1923, 1924.

Unit: accidents; suggested value_type: count.

Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept (`census` = edition).

## Columns

- `census`: edition (each edition kept)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: edition year (no year printed)
- `category`: occupational category (English code, same as `labour_accidents_*` sgt1925-sgt1926)
- `category_fr`: profession as printed
- `outcome`: outcome of the accident (English code)
- `outcome_fr`: printed heading
- `value`: printed value (» = 0)
- `flag`: empty (no cell flagged)

Printed in the chapter *Institutions économiques et sociales* (XIV) of sgt1922-sgt1924 before the labour tables moved to the chapter *Travail et prévoyance sociale* (extracted by `extract_labour.py` as `labour_accidents_*` from sgt1925). No year in the titles: `year` = edition year (the same convention as `labour_accidents_*`). The 13 printed 'professions' are exactly those of sgt1925-sgt1926 and carry the same `category` codes (Transports split into transport / ateliers); row totals (Totaux column) and the Totaux line are checks only, as is the agreement of each profession's total across tables a), b) and c) (it holds in every edition). Chaux et Ciment is printed » in every column of sgt1923.

Same columns and codes as `labour_accidents_outcome` in its sgt1925-sgt1926 layout (morts, incapacités de plus d'un mois, de moins d'un mois); from sgt1927 that table uses other outcome categories (incapacité permanente / temporaire, suites inconnues), which do not line up with these.

Survey of the whole chapter in every edition: `mutuality_survey.md`.

## Validation

- Checks against printed totals and identities: 96; passed: 96; failed: 0.

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (3 printings): sgt1922 f459, sgt1923 f949, sgt1924 f1447.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
