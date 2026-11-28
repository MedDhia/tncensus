# Justice tunisienne, Ouzara : appels en matière correctionnelle (affaires sorties par nature du jugement frappé d'appel et de la décision)

*Tunisian justice, Ouzara: correctional appeals, by kind of judgment appealed and decision.*

Source: *Statistique générale de la Tunisie*, chapter *Justice*, editions sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1926 (`bpt6k9105650k`): p. 83, f647; sgt1927 (`bpt6k91056510`): p. 85, f109; sgt1928 (`bpt6k91056510`): p. 81, f633; sgt1929 (`bpt6k9105652d`): p. 83, f111; sgt1930 (`bpt6k9105652d`): p. 87, f645.

Transcriptions: `../transcribed/justice_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_justice.py build`.

Rows: 360. Years: 1926, 1927, 1928, 1929, 1930.

Unit: number of cases (integer); `»` printed = 0.

Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, `year` = the year of the figures; no year is printed twice, except the two-year columns of the presidents' table (section `presidents`), where the earlier year is taken from the later edition and compared (rule 4).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section name
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `matter`: `civil`, `correctional`, `penal`, `criminal` (Affaires civiles / correctionnelles / pénales / criminelles)
- `tribunal`: court as printed
- `measure`: English code of the printed column (see measure_fr)
- `measure_fr`: printed French heading
- `value`: count of cases (integer); money in francs with centimes; percentages as printed
- `flag`: empty, `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable`, `reprint_corrected`

From sgt1926 the Ouzara's correctional appeals table splits the disposed cases by the kind of judgment appealed (conviction or acquittal) and the decision (confirmed purely and simply, with a reduced or an increased penalty, or reversed). Earlier editions print the four-way split of `justice_ouzara_appeals.csv` instead. The TOTAL columns and the TOTAUX line are checks only.

The page-by-page survey of the chapter in every edition (every table found, with views) is in `justice_survey.md` and in `justice_validation.json` (`_survey`).

## Validation

- Checks against printed totals and identities: 190; passed: 190; failed: 0.

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (5 printings): sgt1926 f647, sgt1927 f109, sgt1928 f633, sgt1929 f111, sgt1930 f645.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
