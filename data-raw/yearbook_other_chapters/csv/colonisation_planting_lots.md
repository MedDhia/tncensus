# Terres à planter (Ventes avec obligation d'installation dans la Régence)

*Land for planting sold with an obligation of settlement in the Regency: lotissements by year, area and number of lots.*

Source: *Statistique générale de la Tunisie*, chapter *Colonisation*, editions sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1924 (`bpt6k9105649x`): p. 446, f1436, p. 447, f1437; sgt1925 (`bpt6k9105650k`): p. 480, f504, p. 481, f505; sgt1926 (`bpt6k9105650k`): p. 452, f1016, p. 453, f1017; sgt1927 (`bpt6k91056510`): p. 452, f480, p. 453, f481; sgt1928 (`bpt6k91056510`): p. 456, f1008, p. 457, f1009; sgt1929 (`bpt6k9105652d`): p. 458, f486, p. 459, f487; sgt1930 (`bpt6k9105652d`): p. 464, f1022, p. 465, f1023; sgt1935 (`bpt6k9105653t`): p. 280, f300, p. 281, f301.

Transcriptions: `../transcribed/colonisation_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_colonisation.py build`.

Rows: 124. Years: 1920, 1921, 1924, 1925, 1926, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935.

Units: hectares and number of lots (`unit`); suggested value_type: mixed.

Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept (`census` = edition); the figures are the state at the edition date and are revised between editions.

## Columns

- `census`: edition the value is taken from (rule 4 tables: the latest edition printing that year)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `year_label`: year as printed (brackets such as `1920-21` kept); `year` = its first year
- `scheme`: `installation` (ventes avec obligation d'installation personnelle)
- `scheme_fr`: printed table title
- `property_fr`: property / lotissement as printed (footnote calls kept)
- `situation_fr`: printed situation
- `controle_civil`: contrôle civil as printed
- `observation_fr`: printed observation for the line (a brace covering several lines is repeated on each)
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible`, `not_applicable`, `total_mismatch`, `ocr_corrected`

Printed sgt1924-sgt1935 as table b) of the chapter (ten-year window; not in sgt1936, sgt1939: see the recapitulation table). `year` is the first year of the printed label; `year_label` keeps the printed bracket (e.g. `1920-21`, sgt1930 prints `1921`). Years printed with » in every column are kept as rows with value 0 and property `»`. sgt1935 prints a 1935 line without name (534 ha, 3 lots) and adds Gamouda (1932) after it. The TOTAUX line is checked. Observation from sgt1926 to sgt1928: "Pour les années 1917 à 1919 inclus aucune vente n'a été effectuée".

Survey of the whole chapter in every edition: `colonisation_survey.md`.

## Validation

- Checks against printed totals and identities: 16; passed: 16; failed: 0.

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (8 printings): sgt1924 f1436, sgt1925 f504, sgt1926 f1016, sgt1927 f480, sgt1928 f1008, sgt1929 f486, sgt1930 f1022, sgt1935 f300.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
