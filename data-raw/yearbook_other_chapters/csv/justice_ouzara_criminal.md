# Justice tunisienne, Ouzara : affaires criminelles

*Tunisian justice, Ouzara: criminal cases (movement).*

Source: *Statistique générale de la Tunisie*, chapter *Justice*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 67, f91; sgt1923 (`bpt6k9105649x`): p. 76, f574; sgt1924 (`bpt6k9105649x`): p. 74, f1064; sgt1925 (`bpt6k9105650k`): p. 73, f97; sgt1926 (`bpt6k9105650k`): p. 83, f647; sgt1927 (`bpt6k91056510`): p. 85, f109; sgt1928 (`bpt6k91056510`): p. 81, f633; sgt1929 (`bpt6k9105652d`): p. 83, f111; sgt1930 (`bpt6k9105652d`): p. 87, f645.

Transcriptions: `../transcribed/justice_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_justice.py build`.

Rows: 73. Years: 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930.

Unit: number of cases (integer); `»` printed = 0.

Printed for overlapping year windows (ten years for the French courts until sgt1930, three from sgt1935; five years for the Ouzara and the regional courts; two years for the caïds and presidents): each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing of the same cell is compared below and not stored.

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

Ouzara (Tunisian Ministry of Justice), "Affaires criminelles": cases pending from the previous year, entered in the year, disposed of by dismissal (non-lieu) or by judgment, and pending at the end of the year. The printed totals (pending + entered; non-lieu + judgment) are checks only.

Cells stored from an earlier printing (flag `reprint_corrected`; the latest printing fails the printed row total, the earlier one passes it): 1920  pending_start: 494 from sgt1923 instead of 484 in sgt1924 (sgt1922-sgt1923 print 494 and the 1920 total 1.385 = 494 + 891; sgt1924 prints 484).

Up to sgt1923 the disposals are printed "par non-lieu / par jugement" (`out_no_case`, `out_judgment`); from sgt1924 the same lines read "par acquittement / par condamnation" (`out_acquittal`, `out_conviction`), and sgt1924-sgt1925 put all of 1922-1924 under "condamnation" (0 acquittals) while sgt1926-sgt1928 split them (e.g. 1922: 67 + 674). The two pairs are kept as separate measures; within each pair the latest printing is stored and the earlier ones are listed below.

The page-by-page survey of the chapter in every edition (every table found, with views) is in `justice_survey.md` and in `justice_validation.json` (`_survey`).

## Validation

- Checks against printed totals and identities: 171; passed: 169; failed: 2.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1924 p.74 (f1064) tn_ouzara_criminal 1920: TOTAUX = pending_start + entered: cells give 1375, printed 1385 (difference 10)
  - sgt1926 p.83 (f647) tn_ouzara_criminal 1923: out_total = out_acquittal + out_conviction: cells give 197, printed 237 (difference 40)

- Overlapping printings: 152 cell comparisons with other editions printing the same cell; 15 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1920 /  /  /  /  /  / pending_start | sgt1922 | 494 | sgt1924 | 484 |
| 1920 /  /  /  /  /  / pending_start | sgt1923 | 494 | sgt1924 | 484 |
| 1922 /  /  /  /  /  / out_acquittal | sgt1924 | 0 | sgt1926 | 67 |
| 1922 /  /  /  /  /  / out_acquittal | sgt1925 | 0 | sgt1926 | 67 |
| 1923 /  /  /  /  /  / out_acquittal | sgt1924 | 0 | sgt1927 | 56 |
| 1923 /  /  /  /  /  / out_acquittal | sgt1925 | 0 | sgt1927 | 56 |
| 1923 /  /  /  /  /  / out_acquittal | sgt1926 | 16 | sgt1927 | 56 |
| 1924 /  /  /  /  /  / out_acquittal | sgt1924 | 0 | sgt1928 | 51 |
| 1924 /  /  /  /  /  / out_acquittal | sgt1925 | 0 | sgt1928 | 51 |
| 1922 /  /  /  /  /  / out_conviction | sgt1924 | 741 | sgt1926 | 674 |
| 1922 /  /  /  /  /  / out_conviction | sgt1925 | 741 | sgt1926 | 674 |
| 1923 /  /  /  /  /  / out_conviction | sgt1924 | 237 | sgt1927 | 181 |
| 1923 /  /  /  /  /  / out_conviction | sgt1925 | 237 | sgt1927 | 181 |
| 1924 /  /  /  /  /  / out_conviction | sgt1924 | 265 | sgt1928 | 214 |
| 1924 /  /  /  /  /  / out_conviction | sgt1925 | 265 | sgt1928 | 214 |

- Flagged cells: ocr_corrected: 2, reprint_corrected: 1.

  - sgt1923 p.76 1923 out_judgment = 237 (ocr_corrected)
  - sgt1923 p.76 1923 out_no_case = 0 (ocr_corrected)
  - sgt1923 p.76 1920 pending_start = 494 (reprint_corrected)

## Image versus OCR

- Read cell by cell on the page images (6 printings): sgt1924 f1064, sgt1926 f647, sgt1927 f109, sgt1928 f633, sgt1929 f111, sgt1930 f645.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (3 printings): sgt1922 f91, sgt1923 f574, sgt1925 f97.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 4.
