# Forêts. d) Poursuites des délits ; e) Incendies

*Forests: offences reported to the courts; forest fires (reports, area burnt, damage).*

Source: *Statistique générale de la Tunisie*, chapter *Agriculture*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 230, f254; sgt1923 (`bpt6k9105649x`): p. 242, f744; sgt1924 (`bpt6k9105649x`): p. 256, f1246; sgt1925 (`bpt6k9105650k`): p. 284, f308; sgt1926 (`bpt6k9105650k`): p. 254, f818; sgt1927 (`bpt6k91056510`): p. 253, f281.

Transcriptions: `../transcribed/agriculture_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_agriculture.py build`.

Rows: 29. Years: 1922, 1923, 1924, 1925, 1926, 1927.

Units: count, hectares / ares / centiares, francs (`unit`); value_type: mixed.

Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept; `year` = edition year.

## Columns

- `census`: edition the value is taken from (rule 4 series: the latest edition printing that year; rule 5 tables: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: edition year (the figures are those of the year, as printed)
- `part`: sub-table letter (`d` poursuites des délits, `e` incendies)
- `part_fr`: printed sub-table title
- `measure`: measure code (English)
- `measure_fr`: printed line heading
- `unit`: `count`, `francs`, or the unit of each printed part of the burnt area (`hectares`, `ares`, `centiares`: sgt1925 prints "607 hect. 95 ares", sgt1926-sgt1927 "8.231 h. 66 a. 78"; the parts are stored as printed, not combined)
- `value`: printed value (» = 0)
- `flag`: empty (no cell flagged)

Printed in sgt1922-sgt1927 only (one figure for d), three lines for e)), below c). Rule 5: each edition kept. No totals, hence no checks. sgt1922-sgt1924 print the burnt area in hectares only; the ares (sgt1925-sgt1927) and centiares (sgt1926-sgt1927) are stored as separate rows (`unit`). sgt1923's d) "909" has a faint last digit (read 9).

Survey of the whole chapter in every edition: `agriculture_survey.md`.

## Validation

- Checks against printed totals and identities: 0; passed: 0; failed: 0.

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (6 printings): sgt1922 f254, sgt1923 f744, sgt1924 f1246, sgt1925 f308, sgt1926 f818, sgt1927 f281.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
