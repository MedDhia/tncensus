# Justice tunisienne, Ouzara : appels en matière civile et correctionnelle, par tribunal ayant rendu les décisions frappées d'appel

*Tunisian justice, Ouzara: civil and correctional appeals, by court of first instance.*

Source: *Statistique générale de la Tunisie*, chapter *Justice*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 67, f91; sgt1923 (`bpt6k9105649x`): p. 76, f574; sgt1924 (`bpt6k9105649x`): p. 74, f1064; sgt1925 (`bpt6k9105650k`): p. 73, f97; sgt1926 (`bpt6k9105650k`): p. 83, f647; sgt1927 (`bpt6k91056510`): p. 85, f109; sgt1928 (`bpt6k91056510`): p. 81, f633; sgt1929 (`bpt6k9105652d`): p. 83, f111; sgt1930 (`bpt6k9105652d`): p. 87, f645.

Transcriptions: `../transcribed/justice_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_justice.py build`.

Rows: 686. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930.

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

"Appels en matière civile" / "Appels en matière correctionnelle" before the Ouzara, by the regional court whose decisions were appealed: cases pending at 31 December of the previous year, entered, and disposed of by confirmation, partial or total reversal, or struck off, and cases pending at 31 December. The printed TOTAL columns and TOTAUX line are checks only.

The page-by-page survey of the chapter in every edition (every table found, with views) is in `justice_survey.md` and in `justice_validation.json` (`_survey`).

## Validation

- Checks against printed totals and identities: 450; passed: 441; failed: 9.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1924 p.74 (f1064) tn_appeals_civil Gafsa: out_total = confirmed + partly_reversed + fully_reversed + struck_off: cells give 97, printed 103 (difference 6)
  - sgt1924 p.74 (f1064) tn_appeals_civil partly_reversed: lines vs TOTAUX: cells give 195, printed 201 (difference 6)
  - sgt1926 p.83 (f647) tn_appeals_civil Le Kef: total_to_judge = pending_start + entered: cells give 505, printed 605 (difference 100)
  - sgt1926 p.83 (f647) tn_appeals_civil Le Kef: pending_end = total_to_judge + -out_total: cells give 416, printed 316 (difference -100)
  - sgt1926 p.83 (f647) tn_appeals_civil total_to_judge: lines vs TOTAUX: cells give 3702, printed 3602 (difference -100)
  - sgt1928 p.81 (f633) tn_appeals_civil Le Kef: out_total = confirmed + partly_reversed + fully_reversed + struck_off: cells give 162, printed 172 (difference 10)
  - sgt1928 p.81 (f633) tn_appeals_civil TOTAUX: out_total = confirmed + partly_reversed + fully_reversed + struck_off: cells give 1123, printed 1133 (difference 10)
  - sgt1922 p.67 (f91) tn_appeals_correctional TOTAUX: pending_end = total_to_judge + -out_total: cells give 175, printed 185 (difference 10)
  - sgt1922 p.67 (f91) tn_appeals_correctional pending_end: lines vs TOTAUX: cells give 175, printed 185 (difference 10)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: ocr_corrected: 6.

  - sgt1929 p.83 1929 civil / Kairouan / confirmed = 109 (ocr_corrected)
  - sgt1924 p.74 1924 civil / Kairouan / fully_reversed = 16 (ocr_corrected)
  - sgt1924 p.74 1924 civil / Le Kef / pending_end = 180 (ocr_corrected)
  - sgt1924 p.74 1924 correctional / Kairouan / fully_reversed = 8 (ocr_corrected)
  - sgt1925 p.73 1925 correctional / Le Kef / entered = 280 (ocr_corrected)
  - sgt1925 p.73 1925 correctional / Sfax / pending_end = 48 (ocr_corrected)

## Image versus OCR

- Read cell by cell on the page images (5 printings): sgt1923 f574, sgt1926 f647, sgt1927 f109, sgt1928 f633, sgt1930 f645.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (8 printings): sgt1922 f91, sgt1922 f91, sgt1923 f574, sgt1924 f1064, sgt1924 f1064, sgt1925 f97, sgt1925 f97, sgt1929 f111.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 10.
