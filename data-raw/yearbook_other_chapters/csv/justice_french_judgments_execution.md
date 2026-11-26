# Exécution des jugements français

*Execution of French judgments.*

Source: *Statistique générale de la Tunisie*, chapter *Justice*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 70, f94; sgt1923 (`bpt6k9105649x`): p. 79, f577; sgt1924 (`bpt6k9105649x`): p. 77, f1067; sgt1925 (`bpt6k9105650k`): p. 80, f104; sgt1926 (`bpt6k9105650k`): p. 90, f654; sgt1927 (`bpt6k91056510`): p. 92, f116; sgt1928 (`bpt6k91056510`): p. 88, f640; sgt1929 (`bpt6k9105652d`): p. 90, f118; sgt1930 (`bpt6k9105652d`): p. 94, f652; sgt1935 (`bpt6k9105653t`): p. 58, f78.

Transcriptions: `../transcribed/justice_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_justice.py build`.

Rows: 24. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935.

Unit: number of judgments.

Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, `year` = the year of the figures; no year is printed twice, except the two-year columns of the presidents' table (section `presidents`), where the earlier year is taken from the later edition and compared (rule 4).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section name
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `measure`: English code of the printed column (see measure_fr)
- `measure_fr`: printed French heading
- `value`: count of cases (integer); money in francs with centimes; percentages as printed
- `flag`: empty, `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable`, `reprint_corrected`

"Exécution des jugements français" (Tunisian authorities executing French judgments): judgments deposited during the year and judgments executed in full; the printed *Reste* (deposited − executed) is a check only.

The page-by-page survey of the chapter in every edition (every table found, with views) is in `justice_survey.md` and in `justice_validation.json` (`_survey`).

## Validation

- Checks against printed totals and identities: 14; passed: 14; failed: 0.

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (8 printings): sgt1923 f577, sgt1924 f1067, sgt1925 f104, sgt1927 f116, sgt1928 f640, sgt1929 f118, sgt1930 f652, sgt1935 f78.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (2 printings): sgt1922 f94, sgt1926 f654.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
