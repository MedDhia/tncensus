# Produit des taxes et amendes

*Proceeds of taxes and fines.*

Source: *Statistique générale de la Tunisie*, chapter *Justice*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 70, f94; sgt1923 (`bpt6k9105649x`): p. 79, f577; sgt1924 (`bpt6k9105649x`): p. 77, f1067; sgt1925 (`bpt6k9105650k`): p. 79, f103; sgt1926 (`bpt6k9105650k`): p. 89, f653; sgt1927 (`bpt6k91056510`): p. 91, f115; sgt1928 (`bpt6k91056510`): p. 87, f639; sgt1929 (`bpt6k9105652d`): p. 89, f117; sgt1930 (`bpt6k9105652d`): p. 93, f651; sgt1935 (`bpt6k9105653t`): p. 59, f79; sgt1936 (`bpt6k91056547`): p. 46, f57; sgt1939 (`bpt6k9105739w`): p. 46, f52.

Transcriptions: `../transcribed/justice_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_justice.py build`.

Rows: 363. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939.

Unit: francs, centimes kept (two decimals); printed » = 0.00.

Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, `year` = the year of the figures; no year is printed twice, except the two-year columns of the presidents' table (section `presidents`), where the earlier year is taken from the later edition and compared (rule 4).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section name
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `tribunal`: court as printed
- `measure`: English code of the printed column (see measure_fr)
- `measure_fr`: printed French heading
- `value`: count of cases (integer); money in francs with centimes; percentages as printed
- `flag`: empty, `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable`, `reprint_corrected`

"Produit des taxes et amendes": duties and fines collected per court (Ouzara, regional courts, and the caïds, kahias, khalifas and presidents of the regional courts on one line). The TOTAL GÉNÉRAL column and the TOTAUX line are checks only.

From sgt1936 the columns are printed in the order Amendes, Droits d'enrôlement, Droits de chancellerie; they are mapped to the same three measure codes (the headings change: "droits de timbre et d'enregistrement" up to sgt1930, "taxes d'enrôlement" from sgt1935; `measure_fr` gives the heading of each edition). sgt1930 prints a line without a label between Gabès and the presidents' line (by elimination Béja, the eighth regional court from 1930), stored as "(line printed without label)". sgt1939 adds the new regional courts of Bizerte, Nabeul, Moknine and Djerba.

The page-by-page survey of the chapter in every edition (every table found, with views) is in `justice_survey.md` and in `justice_validation.json` (`_survey`).

## Validation

- Checks against printed totals and identities: 181; passed: 159; failed: 22.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1924 p.77 (f1067) tn_fees Sfax: total = registration_stamp_duties + chancery_stamp_duties + fines_proportional_duties: cells give 106964.46, printed 105964.46 (difference -1000.00)
  - sgt1924 p.77 (f1067) tn_fees Gabès: total = registration_stamp_duties + chancery_stamp_duties + fines_proportional_duties: cells give 105625.60, printed 111844.60 (difference 6219.00)
  - sgt1924 p.77 (f1067) tn_fees chancery_stamp_duties: lines vs TOTAUX: cells give 119116.59, printed 125335.59 (difference 6219.00)
  - sgt1924 p.77 (f1067) tn_fees total: lines vs TOTAUX: cells give 1587018.59, printed 1588018.59 (difference 1000.00)
  - sgt1925 p.79 (f103) tn_fees Gafsa: total = registration_stamp_duties + chancery_stamp_duties + fines_proportional_duties: cells give 115971.91, printed 118971.91 (difference 3000.00)
  - sgt1925 p.79 (f103) tn_fees fines_proportional_duties: lines vs TOTAUX: cells give 1142738.47, printed 1145738.47 (difference 3000.00)
  - sgt1926 p.89 (f653) tn_fees TOTAUX: total = registration_stamp_duties + chancery_stamp_duties + fines_proportional_duties: cells give 2647336.24, printed 2650336.24 (difference 3000.00)
  - sgt1926 p.89 (f653) tn_fees fines_proportional_duties: lines vs TOTAUX: cells give 1494258.25, printed 1491258.25 (difference -3000.00)
  - sgt1927 p.91 (f115) tn_fees Ouzara: total = registration_stamp_duties + chancery_stamp_duties + fines_proportional_duties: cells give 475259.55, printed 474959.55 (difference -300.00)
  - sgt1927 p.91 (f115) tn_fees Kairouan: total = registration_stamp_duties + chancery_stamp_duties + fines_proportional_duties: cells give 128119.30, printed 128120.30 (difference 1.00)
  - sgt1927 p.91 (f115) tn_fees chancery_stamp_duties: lines vs TOTAUX: cells give 140520.70, printed 140220.70 (difference -300.00)
  - sgt1927 p.91 (f115) tn_fees total: lines vs TOTAUX: cells give 3296417.00, printed 3296416 (difference -1.00)
  - sgt1928 p.87 (f639) tn_fees Gabès: total = registration_stamp_duties + chancery_stamp_duties + fines_proportional_duties: cells give 208207.02, printed 253207.02 (difference 45000.00)
  - sgt1928 p.87 (f639) tn_fees fines_proportional_duties: lines vs TOTAUX: cells give 2448915.04, printed 2493915.04 (difference 45000.00)
  - sgt1929 p.89 (f117) tn_fees Ouzara: total = registration_stamp_duties + chancery_stamp_duties + fines_proportional_duties: cells give 782302.36, printed 728302.36 (difference -54000.00)
  - sgt1929 p.89 (f117) tn_fees total: lines vs TOTAUX: cells give 6094842.18, printed 6148842.18 (difference 54000.00)
  - sgt1930 p.93 (f651) tn_fees Driba: total = registration_stamp_duties + chancery_stamp_duties + fines_proportional_duties: cells give 1441194.25, printed 1442194.25 (difference 1000.00)
  - sgt1930 p.93 (f651) tn_fees total: lines vs TOTAUX: cells give 7014982.11, printed 7013982.11 (difference -1000.00)
  - sgt1936 p.46 (f57) tn_fees Caïds: total = fines_proportional_duties + registration_stamp_duties + chancery_stamp_duties: cells give 278833.48, printed 278833.49 (difference 0.01)
  - sgt1936 p.46 (f57) tn_fees TOTAUX: total = fines_proportional_duties + registration_stamp_duties + chancery_stamp_duties: cells give 5948607.06, printed 5948539.06 (difference -68.00)
  - sgt1936 p.46 (f57) tn_fees fines_proportional_duties: lines vs TOTAUX: cells give 4898054.74, printed 4898054.75 (difference 0.01)
  - sgt1936 p.46 (f57) tn_fees total: lines vs TOTAUX: cells give 5948607.06, printed 5948539.06 (difference -68.00)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: ocr_corrected: 3.

  - sgt1929 p.89 1929 Sfax / chancery_stamp_duties = 205.00 (ocr_corrected)
  - sgt1929 p.89 1929 Sfax / fines_proportional_duties = 295675.39 (ocr_corrected)
  - sgt1929 p.89 1929 Sfax / registration_stamp_duties = 72204.00 (ocr_corrected)

## Image versus OCR

- Read cell by cell on the page images (9 printings): sgt1924 f1067, sgt1925 f103, sgt1926 f653, sgt1927 f115, sgt1928 f639, sgt1930 f651, sgt1935 f79, sgt1936 f57, sgt1939 f52.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (3 printings): sgt1922 f94, sgt1923 f577, sgt1929 f117 (Sousse to the end).
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 4.
