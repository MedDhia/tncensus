# Industrie minière. Renseignements généraux sur les mines (Exploitations minières)

*Mining: concessions, mines worked, workers, working days, production and value by mineral.*

Source: *Statistique générale de la Tunisie*, chapter *Travaux publics*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 158, f182; sgt1923 (`bpt6k9105649x`): p. 170, f672; sgt1924 (`bpt6k9105649x`): p. 178, f1168; sgt1925 (`bpt6k9105650k`): p. 184, f208; sgt1926 (`bpt6k9105650k`): p. 200, f764; sgt1927 (`bpt6k91056510`): p. 198, f226; sgt1928 (`bpt6k91056510`): p. 198, f750; sgt1929 (`bpt6k9105652d`): p. 200, f228; sgt1930 (`bpt6k9105652d`): p. 204, f762; sgt1935 (`bpt6k9105653t`): p. 104, f124; sgt1936 (`bpt6k91056547`): p. 79, f90; sgt1939 (`bpt6k9105739w`): p. 84, f90.

Transcriptions: `../transcribed/publicworks_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_publicworks.py build`.

Rows: 516. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939.

Units: count, hectares, tonnes (mercury in kg) and francs; suggested value_type: mixed.

Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, with `year`.

## Columns

- `census`: edition the value is taken from: the latest edition printing that year (rule 5 tables: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `mineral`: mineral code (English); a bracketed group printed once for several minerals is coded with the joined names (e.g. `lead_zinc`)
- `mineral_fr`: printed line heading
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible`, `not_applicable` (nothing printed), `row_realigned` (printed on the wrong line, stored on the year it belongs to), `total_mismatch`

Printed once per edition for the edition year. Lead and zinc (and from sgt1936 mercury, in sgt1939 also fluorite) share one bracketed figure for concessions, mines worked, workers and working days: it is stored once on a group line (`mineral` = `lead_zinc`, ...); their production and value are printed per mineral (sgt1935 prints one bracketed production and value for lead and zinc). The Totaux of the value column is a check. Footnotes: Manganèse (1) permis d'exploitation; sgt1922 Lignites (2) dont 1 permis d'exploitation; from sgt1935 "Par mines exploitées, il faut comprendre mines productives". Lines printed with » throughout (e.g. Mixtes in sgt1928) are stored as 0.

Survey of the whole chapter in every edition: `publicworks_survey.md`.

## Validation

- Checks against printed totals and identities: 12; passed: 12; failed: 0.

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (12 printings): sgt1922 f182, sgt1923 f672, sgt1924 f1168, sgt1925 f208, sgt1926 f764, sgt1927 f226, sgt1928 f750, sgt1929 f228, sgt1930 f762, sgt1935 f124, sgt1936 f90, sgt1939 f90.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
