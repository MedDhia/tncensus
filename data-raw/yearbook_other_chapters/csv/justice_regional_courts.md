# Tribunaux régionaux : affaires civiles et correctionnelles (procédures)

*Regional courts: civil and correctional proceedings (movement).*

Source: *Statistique générale de la Tunisie*, chapter *Justice*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 68, f92; sgt1923 (`bpt6k9105649x`): p. 77, f575; sgt1924 (`bpt6k9105649x`): p. 75, f1065; sgt1925 (`bpt6k9105650k`): p. 74, f98; sgt1926 (`bpt6k9105650k`): p. 84, f648; sgt1927 (`bpt6k91056510`): p. 86, f110; sgt1928 (`bpt6k91056510`): p. 82, f634; sgt1929 (`bpt6k9105652d`): p. 84, f112; sgt1930 (`bpt6k9105652d`): p. 88, f646.

Transcriptions: `../transcribed/justice_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_justice.py build`.

Rows: 766. Years: 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930.

Unit: number of cases (integer); `»` printed = 0.

Printed for overlapping year windows (ten years for the French courts until sgt1930, three from sgt1935; five years for the Ouzara and the regional courts; two years for the caïds and presidents): each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing of the same cell is compared below and not stored.

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

"Tribunaux régionaux": per regional court and year, proceedings pending from the previous year (Il restait de l'année précédente), entered in the year (Procédures inscrites dans l'année) and pending at 31 December (Reste au 31 décembre). The TOTAUX line is a check only; the identity "pending at the end of year N = pending at the start of N+1" is also checked.

The page-by-page survey of the chapter in every edition (every table found, with views) is in `justice_survey.md` and in `justice_validation.json` (`_survey`).

## Validation

- Checks against printed totals and identities: 1114; passed: 1093; failed: 21.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.68 (f92) tn_regional [civil] 1921:entered: lines vs TOTAUX: cells give 17105, printed 17125 (difference 20)
  - sgt1922 p.68 (f92) tn_regional [correctional] 1919:entered: lines vs TOTAUX: cells give 17989, printed 17980 (difference -9)
  - sgt1923 p.77 (f575) tn_regional [civil] 1921:entered: lines vs TOTAUX: cells give 17105, printed 17125 (difference 20)
  - sgt1923 p.77 (f575) tn_regional [civil] 1923:entered: lines vs TOTAUX: cells give 16183, printed 16083 (difference -100)
  - sgt1923 p.77 (f575) tn_regional [correctional] 1919:entered: lines vs TOTAUX: cells give 17989, printed 17980 (difference -9)
  - sgt1924 p.75 (f1065) tn_regional [civil] 1921:entered: lines vs TOTAUX: cells give 17105, printed 17125 (difference 20)
  - sgt1924 p.75 (f1065) tn_regional [civil] 1922:pending_start: lines vs TOTAUX: cells give 5617, printed 5647 (difference 30)
  - sgt1924 p.75 (f1065) tn_regional [civil] 1923:entered: lines vs TOTAUX: cells give 16183, printed 16083 (difference -100)
  - sgt1924 p.75 (f1065) tn_regional [civil] 1924:pending_end: lines vs TOTAUX: cells give 4407, printed 4377 (difference -30)
  - sgt1924 p.75 (f1065) tn_regional [civil] TOTAUX: pending_end 1921 = pending_start 1922: cells give 5617, printed 5647 (difference 30)
  - sgt1925 p.74 (f98) tn_regional [civil] 1921:entered: lines vs TOTAUX: cells give 17105, printed 17125 (difference 20)
  - sgt1925 p.74 (f98) tn_regional [civil] 1923:entered: lines vs TOTAUX: cells give 16183, printed 16083 (difference -100)
  - sgt1926 p.84 (f648) tn_regional [civil] 1926:entered: lines vs TOTAUX: cells give 11933, printed 12133 (difference 200)
  - sgt1929 p.84 (f112) tn_regional [correctional] 1927:convicted: lines vs TOTAUX: cells give 13587, printed 13857 (difference 270)
  - sgt1929 p.84 (f112) tn_regional [correctional] 1928:convicted: lines vs TOTAUX: cells give 11661, printed 11631 (difference -30)
  - sgt1929 p.84 (f112) tn_regional [correctional] Driba 1928: pending_end = pending_start + entered - convicted - acquitted: cells give 1144, printed 1174 (difference 30)
  - sgt1929 p.84 (f112) tn_regional [correctional] TOTAUX 1927: pending_end = pending_start + entered - convicted - acquitted: cells give 2864, printed 3134 (difference 270)
  - sgt1930 p.88 (f646) tn_regional [civil] 1930:pending_start: lines vs TOTAUX: cells give 5388, printed 5748 (difference 360)
  - sgt1930 p.88 (f646) tn_regional [civil] Driba: pending_end 1929 = pending_start 1930: cells give 2952, printed 2592 (difference -360)
  - sgt1930 p.88 (f646) tn_regional [correctional] Gafsa 1930: pending_end = pending_start + entered - convicted - acquitted: cells give 190, printed 207 (difference 17)
  - sgt1930 p.88 (f646) tn_regional [correctional] TOTAUX 1930: pending_end = pending_start + entered - convicted - acquitted: cells give 4154, printed 4171 (difference 17)

- Overlapping printings: 1784 cell comparisons with other editions printing the same cell; 3 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1924 /  / civil /  /  / Gafsa / pending_end | sgt1924 | 143 | sgt1928 | 113 |
| 1926 /  / civil /  /  / Gabès / entered | sgt1926 | 605 | sgt1930 | 805 |
| 1928 /  / correctional /  /  / Driba / convicted | sgt1929 | 3168 | sgt1930 | 3138 |

- Flagged cells: not_applicable: 64, ocr_corrected: 3.

  - sgt1929 p.84 1925 civil / Gafsa / entered = 714 (ocr_corrected)
  - sgt1929 p.84 1925 civil / Gafsa / pending_end = 206 (ocr_corrected)
  - sgt1929 p.84 1925 civil / Gafsa / pending_start = 113 (ocr_corrected)
  - sgt1925 p.74 1921 correctional / Béja / acquitted = NA (not_applicable)
  - sgt1926 p.84 1922 correctional / Béja / acquitted = NA (not_applicable)
  - sgt1927 p.86 1923 correctional / Béja / acquitted = NA (not_applicable)
  - sgt1928 p.82 1924 correctional / Béja / acquitted = NA (not_applicable)
  - sgt1925 p.74 1921 correctional / Béja / convicted = NA (not_applicable)
  - sgt1926 p.84 1922 correctional / Béja / convicted = NA (not_applicable)
  - sgt1927 p.86 1923 correctional / Béja / convicted = NA (not_applicable)
  - sgt1928 p.82 1924 correctional / Béja / convicted = NA (not_applicable)
  - sgt1925 p.74 1921 correctional / Driba / acquitted = NA (not_applicable)
  - sgt1926 p.84 1922 correctional / Driba / acquitted = NA (not_applicable)
  - sgt1927 p.86 1923 correctional / Driba / acquitted = NA (not_applicable)
  - sgt1928 p.82 1924 correctional / Driba / acquitted = NA (not_applicable)
  - sgt1925 p.74 1921 correctional / Driba / convicted = NA (not_applicable)
  - sgt1926 p.84 1922 correctional / Driba / convicted = NA (not_applicable)
  - sgt1927 p.86 1923 correctional / Driba / convicted = NA (not_applicable)
  - sgt1928 p.82 1924 correctional / Driba / convicted = NA (not_applicable)
  - sgt1925 p.74 1921 correctional / Gabès / acquitted = NA (not_applicable)
  - sgt1926 p.84 1922 correctional / Gabès / acquitted = NA (not_applicable)
  - sgt1927 p.86 1923 correctional / Gabès / acquitted = NA (not_applicable)
  - sgt1928 p.82 1924 correctional / Gabès / acquitted = NA (not_applicable)
  - sgt1925 p.74 1921 correctional / Gabès / convicted = NA (not_applicable)
  - sgt1926 p.84 1922 correctional / Gabès / convicted = NA (not_applicable)
  - sgt1927 p.86 1923 correctional / Gabès / convicted = NA (not_applicable)
  - sgt1928 p.82 1924 correctional / Gabès / convicted = NA (not_applicable)
  - sgt1925 p.74 1921 correctional / Gafsa / acquitted = NA (not_applicable)
  - sgt1926 p.84 1922 correctional / Gafsa / acquitted = NA (not_applicable)
  - sgt1927 p.86 1923 correctional / Gafsa / acquitted = NA (not_applicable)
  - sgt1928 p.82 1924 correctional / Gafsa / acquitted = NA (not_applicable)
  - sgt1925 p.74 1921 correctional / Gafsa / convicted = NA (not_applicable)
  - sgt1926 p.84 1922 correctional / Gafsa / convicted = NA (not_applicable)
  - sgt1927 p.86 1923 correctional / Gafsa / convicted = NA (not_applicable)
  - sgt1928 p.82 1924 correctional / Gafsa / convicted = NA (not_applicable)
  - sgt1925 p.74 1921 correctional / Kairouan / acquitted = NA (not_applicable)
  - sgt1926 p.84 1922 correctional / Kairouan / acquitted = NA (not_applicable)
  - sgt1927 p.86 1923 correctional / Kairouan / acquitted = NA (not_applicable)
  - sgt1928 p.82 1924 correctional / Kairouan / acquitted = NA (not_applicable)
  - sgt1925 p.74 1921 correctional / Kairouan / convicted = NA (not_applicable)
  - sgt1926 p.84 1922 correctional / Kairouan / convicted = NA (not_applicable)
  - sgt1927 p.86 1923 correctional / Kairouan / convicted = NA (not_applicable)
  - sgt1928 p.82 1924 correctional / Kairouan / convicted = NA (not_applicable)
  - sgt1925 p.74 1921 correctional / Le Kef / acquitted = NA (not_applicable)
  - sgt1926 p.84 1922 correctional / Le Kef / acquitted = NA (not_applicable)
  - sgt1927 p.86 1923 correctional / Le Kef / acquitted = NA (not_applicable)
  - sgt1928 p.82 1924 correctional / Le Kef / acquitted = NA (not_applicable)
  - sgt1925 p.74 1921 correctional / Le Kef / convicted = NA (not_applicable)
  - sgt1926 p.84 1922 correctional / Le Kef / convicted = NA (not_applicable)
  - sgt1927 p.86 1923 correctional / Le Kef / convicted = NA (not_applicable)
  - sgt1928 p.82 1924 correctional / Le Kef / convicted = NA (not_applicable)
  - sgt1925 p.74 1921 correctional / Sfax / acquitted = NA (not_applicable)
  - sgt1926 p.84 1922 correctional / Sfax / acquitted = NA (not_applicable)
  - sgt1927 p.86 1923 correctional / Sfax / acquitted = NA (not_applicable)
  - sgt1928 p.82 1924 correctional / Sfax / acquitted = NA (not_applicable)
  - sgt1925 p.74 1921 correctional / Sfax / convicted = NA (not_applicable)
  - sgt1926 p.84 1922 correctional / Sfax / convicted = NA (not_applicable)
  - sgt1927 p.86 1923 correctional / Sfax / convicted = NA (not_applicable)
  - sgt1928 p.82 1924 correctional / Sfax / convicted = NA (not_applicable)
  - sgt1925 p.74 1921 correctional / Sousse / acquitted = NA (not_applicable)
  - sgt1926 p.84 1922 correctional / Sousse / acquitted = NA (not_applicable)
  - sgt1927 p.86 1923 correctional / Sousse / acquitted = NA (not_applicable)
  - sgt1928 p.82 1924 correctional / Sousse / acquitted = NA (not_applicable)
  - sgt1925 p.74 1921 correctional / Sousse / convicted = NA (not_applicable)
  - sgt1926 p.84 1922 correctional / Sousse / convicted = NA (not_applicable)
  - sgt1927 p.86 1923 correctional / Sousse / convicted = NA (not_applicable)
  - sgt1928 p.82 1924 correctional / Sousse / convicted = NA (not_applicable)

## Image versus OCR

- Read cell by cell on the page images (13 printings): sgt1922 f92 civil, sgt1922 f92 correctional, sgt1923 f575 civil, sgt1923 f575 correctional, sgt1924 f1065 civil, sgt1924 f1065 correctional, sgt1925 f98 civil, sgt1925 f98 correctional, sgt1926 f648 civil, sgt1927 f110 civil, sgt1928 f634 civil, sgt1928 f634 correctional, sgt1930 f646 civil.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (5 printings): sgt1926 f648 correctional, sgt1927 f110 correctional (1923-1924 on f110 (the 1924 'Reste' column partly in the binding), 1925-1927 on f111), sgt1929 f112 civil, sgt1929 f112 correctional (1927-1929 (f113)), sgt1930 f646 correctional (1926-1927 on f646, 1928-1930 rows checked on f647 crops).
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 16.
