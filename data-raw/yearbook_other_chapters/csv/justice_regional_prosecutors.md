# Travaux des parquets des tribunaux régionaux

*Work of the public prosecutors' offices of the regional courts.*

Source: *Statistique générale de la Tunisie*, chapter *Justice*, editions sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1925 (`bpt6k9105650k`): p. 75, f99; sgt1926 (`bpt6k9105650k`): p. 85, f649; sgt1927 (`bpt6k91056510`): p. 87, f111; sgt1928 (`bpt6k91056510`): p. 83, f635; sgt1929 (`bpt6k9105652d`): p. 85, f113; sgt1930 (`bpt6k9105652d`): p. 89, f647.

Transcriptions: `../transcribed/justice_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_justice.py build`.

Rows: 384. Years: 1925, 1926, 1927, 1928, 1929, 1930.

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

- Checks against printed totals and identities: 102; passed: 98; failed: 4.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1928 p.83 (f635) tn_parquets Kairouan: entered = dismissed + direct_summons + to_investigation + to_police_court + to_french_courts + to_other_tunisian_courts + pending_end: cells give 3864, printed 3869 (difference 5)
  - sgt1928 p.83 (f635) tn_parquets dismissed: lines vs TOTAUX: cells give 17259, printed 17264 (difference 5)
  - sgt1930 p.89 (f647) tn_parquets Le Kef: entered = dismissed + direct_summons + to_investigation + to_police_court + to_french_courts + to_other_tunisian_courts + pending_end: cells give 8206, printed 8204 (difference -2)
  - sgt1930 p.89 (f647) tn_parquets Gafsa: entered = dismissed + direct_summons + to_investigation + to_police_court + to_french_courts + to_other_tunisian_courts + pending_end: cells give 2872, printed 2874 (difference 2)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (4 printings): sgt1925 f99, sgt1927 f111, sgt1928 f635, sgt1930 f647.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (2 printings): sgt1926 f649, sgt1929 f113.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 1.
