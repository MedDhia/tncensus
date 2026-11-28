# Fixation au sol des indigènes (Lotissements tunisiens)

*Settlement of Tunisians on the land: families settled and land allotted (cumulative from 1920), and allotments by year (sgt1939).*

Source: *Statistique générale de la Tunisie*, chapter *Colonisation*, editions sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1925 (`bpt6k9105650k`): p. 488, f512; sgt1926 (`bpt6k9105650k`): p. 460, f1024; sgt1927 (`bpt6k91056510`): p. 460, f488; sgt1928 (`bpt6k91056510`): p. 464, f1016; sgt1929 (`bpt6k9105652d`): p. 464, f492; sgt1930 (`bpt6k9105652d`): p. 470, f1028; sgt1935 (`bpt6k9105653t`): p. 286, f306; sgt1936 (`bpt6k91056547`): p. 169, f180; sgt1939 (`bpt6k9105739w`): p. 149, f155.

Transcriptions: `../transcribed/colonisation_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_colonisation.py build`.

Rows: 87. Years: 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Units: count and hectares (`unit`); suggested value_type: mixed.

Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept (`census` = edition); the figures are the state at the edition date and are revised between editions.

## Columns

- `census`: edition the value is taken from (rule 4 tables: the latest edition printing that year)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `year_label`: year as printed (brackets such as `1920-21` kept); `year` = its first year
- `item`: `cumulative` (state since 1920 at the edition date), `allotments_of_year`, `definitive_sales`
- `item_fr`: printed line or table heading
- `observation_fr`: printed observation for the line (a brace covering several lines is repeated on each)
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible`, `not_applicable`, `total_mismatch`, `ocr_corrected`

sgt1925-sgt1929: one line *Période de 1920 à <edition year>*: number of families settled, land allotted for cultivation (sgt1927: terres de plantation et de cultures attribuées; sgt1928-sgt1929: terres de plantation et de cultures arbustives) and grazing land, in hectares, with the printed observation (footnote (1): part of the land in the Territoires du Sud and terres sialines). sgt1930-sgt1936: number of allotments, lots and area of the lotissements created since 1920 (sgt1930 adds the Gammouda lotissements created in 1930; its total line is checked). sgt1939: allotments by year 1920-1939 (`item` = `allotments_of_year`, `year` = that year; total checked). Cumulative lines carry `year` = edition year, `year_label` = the printed period. Not in sgt1922-sgt1924.

Survey of the whole chapter in every edition: `colonisation_survey.md`.

## Validation

- Checks against printed totals and identities: 6; passed: 6; failed: 0.

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (9 printings): sgt1925 f512, sgt1926 f1024, sgt1927 f488, sgt1928 f1016, sgt1929 f492, sgt1930 f1028, sgt1935 f306, sgt1936 f180, sgt1939 f155.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
