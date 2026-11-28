# Travaux de la Chambre d'accusation (Chambre des mises en accusation)

*Work of the indictment chamber.*

Source: *Statistique générale de la Tunisie*, chapter *Justice*, editions sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1925 (`bpt6k9105650k`): p. 76, f100; sgt1926 (`bpt6k9105650k`): p. 86, f650; sgt1927 (`bpt6k91056510`): p. 88, f112; sgt1928 (`bpt6k91056510`): p. 84, f636; sgt1929 (`bpt6k9105652d`): p. 86, f114; sgt1930 (`bpt6k9105652d`): p. 90, f648.

Transcriptions: `../transcribed/justice_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_justice.py build`.

Rows: 48. Years: 1925, 1926, 1927, 1928, 1929, 1930.

Unit: number of cases.

Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, `year` = the year of the figures; no year is printed twice, except the two-year columns of the presidents' table (section `presidents`), where the earlier year is taken from the later edition and compared (rule 4).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section name
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `value`: count of cases (integer); money in francs with centimes; percentages as printed
- `flag`: empty, `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable`, `reprint_corrected`

The page-by-page survey of the chapter in every edition (every table found, with views) is in `justice_survey.md` and in `justice_validation.json` (`_survey`).

## Validation

- Checks against printed totals and identities: 12; passed: 12; failed: 0.

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (10 printings): sgt1925 f100, sgt1925 f100, sgt1927 f112, sgt1927 f112, sgt1928 f636, sgt1928 f636, sgt1929 f114, sgt1929 f114, sgt1930 f648, sgt1930 f648.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (2 printings): sgt1926 f650, sgt1926 f650.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
