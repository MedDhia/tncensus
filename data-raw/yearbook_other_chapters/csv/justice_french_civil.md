# Justice française : affaires civiles, par tribunal

*French justice: civil cases, by court.*

Source: *Statistique générale de la Tunisie*, chapter *Justice*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 63, f87, p. 65, f89; sgt1923 (`bpt6k9105649x`): p. 72, f570, p. 74, f572; sgt1924 (`bpt6k9105649x`): p. 70, f1060, p. 72, f1062; sgt1925 (`bpt6k9105650k`): p. 70, f94; sgt1926 (`bpt6k9105650k`): p. 80, f644; sgt1927 (`bpt6k91056510`): p. 82, f106; sgt1928 (`bpt6k91056510`): p. 78, f630; sgt1929 (`bpt6k9105652d`): p. 80, f108; sgt1930 (`bpt6k9105652d`): p. 84, f642; sgt1935 (`bpt6k9105653t`): p. 52, f72; sgt1936 (`bpt6k91056547`): p. 43, f54; sgt1939 (`bpt6k9105739w`): p. 43, f49.

Transcriptions: `../transcribed/justice_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_justice.py build`.

Rows: 200. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Unit: number of judgments.

Printed for overlapping year windows (ten years for the French courts until sgt1930, three from sgt1935; five years for the Ouzara and the regional courts; two years for the caïds and presidents): each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing of the same cell is compared below and not stored.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section name
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `court`: French court of first instance as printed (`Tunis`, `Sousse`)
- `measure`: English code of the printed column (see measure_fr)
- `measure_fr`: printed French heading
- `value`: count of cases (integer); money in francs with centimes; percentages as printed
- `flag`: empty, `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable`, `reprint_corrected`

"Affaires civiles": civil judgments by type (contradictory, by default, preparatory, on petition) per year and court; the printed *Totaux* column is used for the row check.

Cells stored from an earlier printing (flag `reprint_corrected`; the latest printing fails the printed row total, the earlier one passes it): 1918 Tunis preparatory: 177 from sgt1924 instead of 122 in sgt1927 (sgt1922-sgt1924 print 177 and the 1918 Tunis total 1.223 = 521 + 293 + 177 + 232; sgt1925-sgt1930 print 122); 1921 Tunis contradictory: 857 from sgt1924 instead of 257 in sgt1930 (sgt1922-sgt1924 print 857 and the 1921 Tunis total 2.485 = 857 + 589 + 217 + 822; sgt1925-sgt1930 print 257); 1920 Sousse default: 197 from sgt1924 instead of 192 in sgt1929 (sgt1922-sgt1924 print 197 and the 1920 Sousse total 540 = 234 + 197 + 51 + 58; sgt1925-sgt1929 print 192); 1924 Sousse contradictory: 343 from sgt1924 instead of 363 in sgt1930 (sgt1924 prints 343 and the 1924 Sousse total 1.038 = 343 + 461 + 42 + 192; sgt1925-sgt1930 print 363); 1934 Tunis contradictory: 7711 from sgt1935 instead of 7714 in sgt1936 (sgt1935 prints 7.711 and the 1934 Tunis total 15.133 = 7.711 + 6.067 + 912 + 443; sgt1936 prints 7.714).

The page-by-page survey of the chapter in every edition (every table found, with views) is in `justice_survey.md` and in `justice_validation.json` (`_survey`).

## Validation

- Checks against printed totals and identities: 195; passed: 139; failed: 56.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.63 (f87) fr_civil [Tunis] 1914: total = contradictory + default + preparatory + on_petition: cells give 2611, printed 2619 (difference 8)
  - sgt1922 p.63 (f87) fr_civil [Tunis] 1917: total = contradictory + default + preparatory + on_petition: cells give 1160, printed 1150 (difference -10)
  - sgt1922 p.65 (f89) fr_civil [Sousse] 1916: total = contradictory + default + preparatory + on_petition: cells give 350, printed 400 (difference 50)
  - sgt1923 p.72 (f570) fr_civil [Tunis] 1917: total = contradictory + default + preparatory + on_petition: cells give 1160, printed 1150 (difference -10)
  - sgt1923 p.74 (f572) fr_civil [Sousse] 1916: total = contradictory + default + preparatory + on_petition: cells give 350, printed 400 (difference 50)
  - sgt1924 p.70 (f1060) fr_civil [Tunis] 1917: total = contradictory + default + preparatory + on_petition: cells give 1160, printed 1150 (difference -10)
  - sgt1924 p.72 (f1062) fr_civil [Sousse] 1916: total = contradictory + default + preparatory + on_petition: cells give 350, printed 400 (difference 50)
  - sgt1925 p.70 (f94) fr_civil 1916: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 350, printed 400 (difference 50)
  - sgt1925 p.70 (f94) fr_civil 1920: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 535, printed 540 (difference 5)
  - sgt1925 p.70 (f94) fr_civil 1922: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 607, printed 602 (difference -5)
  - sgt1925 p.70 (f94) fr_civil 1924: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 1058, printed 1038 (difference -20)
  - sgt1925 p.70 (f94) fr_civil 1917: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis: cells give 1160, printed 1150 (difference -10)
  - sgt1925 p.70 (f94) fr_civil 1918: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis: cells give 1168, printed 1223 (difference 55)
  - sgt1925 p.70 (f94) fr_civil 1921: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis: cells give 1885, printed 2485 (difference 600)
  - sgt1925 p.70 (f94) fr_civil 1924: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis: cells give 3075, printed 3025 (difference -50)
  - sgt1926 p.80 (f644) fr_civil 1920: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 535, printed 540 (difference 5)
  - sgt1926 p.80 (f644) fr_civil 1922: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 607, printed 602 (difference -5)
  - sgt1926 p.80 (f644) fr_civil 1924: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 1058, printed 1038 (difference -20)
  - sgt1926 p.80 (f644) fr_civil 1917: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis: cells give 1160, printed 1150 (difference -10)
  - sgt1926 p.80 (f644) fr_civil 1918: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis: cells give 1168, printed 1223 (difference 55)
  - sgt1926 p.80 (f644) fr_civil 1921: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis: cells give 1885, printed 2485 (difference 600)
  - sgt1926 p.80 (f644) fr_civil 1924: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis: cells give 3075, printed 3025 (difference -50)
  - sgt1927 p.82 (f106) fr_civil 1920: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 535, printed 540 (difference 5)
  - sgt1927 p.82 (f106) fr_civil 1922: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 607, printed 602 (difference -5)
  - sgt1927 p.82 (f106) fr_civil 1924: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 1058, printed 1038 (difference -20)
  - sgt1927 p.82 (f106) fr_civil 1927: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 1224, printed 1233 (difference 9)
  - sgt1927 p.82 (f106) fr_civil 1918: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis: cells give 1168, printed 1223 (difference 55)
  - sgt1927 p.82 (f106) fr_civil 1921: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis: cells give 1885, printed 2485 (difference 600)
  - sgt1927 p.82 (f106) fr_civil 1924: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis: cells give 3075, printed 3025 (difference -50)
  - sgt1928 p.78 (f630) fr_civil 1920: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 535, printed 540 (difference 5)
  - sgt1928 p.78 (f630) fr_civil 1922: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 607, printed 602 (difference -5)
  - sgt1928 p.78 (f630) fr_civil 1924: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 1058, printed 1038 (difference -20)
  - sgt1928 p.78 (f630) fr_civil 1927: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 1224, printed 1233 (difference 9)
  - sgt1928 p.78 (f630) fr_civil 1928: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 1467, printed 1489 (difference 22)
  - sgt1928 p.78 (f630) fr_civil 1921: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis: cells give 1885, printed 2485 (difference 600)
  - sgt1928 p.78 (f630) fr_civil 1924: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis: cells give 3075, printed 3025 (difference -50)
  - sgt1929 p.80 (f108) fr_civil 1920: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 535, printed 540 (difference 5)
  - sgt1929 p.80 (f108) fr_civil 1922: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 607, printed 602 (difference -5)
  - sgt1929 p.80 (f108) fr_civil 1924: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 1058, printed 1038 (difference -20)
  - sgt1929 p.80 (f108) fr_civil 1927: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 1224, printed 1233 (difference 9)
  - sgt1929 p.80 (f108) fr_civil 1928: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 1467, printed 1489 (difference 22)
  - sgt1929 p.80 (f108) fr_civil 1929: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 2004, printed 1933 (difference -71)
  - sgt1929 p.80 (f108) fr_civil 1921: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis: cells give 1885, printed 2485 (difference 600)
  - sgt1929 p.80 (f108) fr_civil 1924: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis: cells give 3075, printed 3025 (difference -50)
  - sgt1929 p.80 (f108) fr_civil 1929: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis: cells give 5825, printed 5225 (difference -600)
  - sgt1930 p.84 (f642) fr_civil 1922: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 607, printed 602 (difference -5)
  - sgt1930 p.84 (f642) fr_civil 1924: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 1058, printed 1038 (difference -20)
  - sgt1930 p.84 (f642) fr_civil 1927: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 1224, printed 1233 (difference 9)
  - sgt1930 p.84 (f642) fr_civil 1928: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 1467, printed 1489 (difference 22)
  - sgt1930 p.84 (f642) fr_civil 1929: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse: cells give 2004, printed 1933 (difference -71)
  - sgt1930 p.84 (f642) fr_civil 1921: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis: cells give 1885, printed 2485 (difference 600)
  - sgt1930 p.84 (f642) fr_civil 1924: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis: cells give 3075, printed 3025 (difference -50)
  - sgt1930 p.84 (f642) fr_civil 1929: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis: cells give 5825, printed 5225 (difference -600)
  - sgt1935 p.52 (f72) fr_civil 1933: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis: cells give 13629, printed 12953 (difference -676)
  - sgt1936 p.43 (f54) fr_civil 1934: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis: cells give 15136, printed 15133 (difference -3)
  - sgt1936 p.43 (f54) fr_civil 1936: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis: cells give 9825, printed 11456 (difference 1631)

- Overlapping printings: 592 cell comparisons with other editions printing the same cell; 11 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1918 / Tunis /  /  /  /  / preparatory | sgt1922 | 177 | sgt1927 | 122 |
| 1918 / Tunis /  /  /  /  / preparatory | sgt1923 | 177 | sgt1927 | 122 |
| 1918 / Tunis /  /  /  /  / preparatory | sgt1924 | 177 | sgt1927 | 122 |
| 1921 / Tunis /  /  /  /  / contradictory | sgt1922 | 857 | sgt1930 | 257 |
| 1921 / Tunis /  /  /  /  / contradictory | sgt1923 | 857 | sgt1930 | 257 |
| 1921 / Tunis /  /  /  /  / contradictory | sgt1924 | 857 | sgt1930 | 257 |
| 1920 / Sousse /  /  /  /  / default | sgt1922 | 197 | sgt1929 | 192 |
| 1920 / Sousse /  /  /  /  / default | sgt1923 | 197 | sgt1929 | 192 |
| 1920 / Sousse /  /  /  /  / default | sgt1924 | 197 | sgt1929 | 192 |
| 1924 / Sousse /  /  /  /  / contradictory | sgt1924 | 343 | sgt1930 | 363 |
| 1934 / Tunis /  /  /  /  / contradictory | sgt1935 | 7711 | sgt1936 | 7714 |

- Flagged cells: reprint_corrected: 5.

  - sgt1924 p.72 1924 Sousse / contradictory = 343 (reprint_corrected)
  - sgt1924 p.72 1920 Sousse / default = 197 (reprint_corrected)
  - sgt1924 p.70 1921 Tunis / contradictory = 857 (reprint_corrected)
  - sgt1935 p.52 1934 Tunis / contradictory = 7711 (reprint_corrected)
  - sgt1924 p.70 1918 Tunis / preparatory = 177 (reprint_corrected)

## Image versus OCR

- Read cell by cell on the page images (5 printings): sgt1925 f94, sgt1926 f644, sgt1935 f72, sgt1936 f54, sgt1939 f49.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (10 printings): sgt1922 f87 Tunis, sgt1922 f89 Sousse, sgt1923 f570 Tunis, sgt1923 f572 Sousse, sgt1924 f1060 Tunis, sgt1924 f1062 Sousse, sgt1927 f106, sgt1928 f630 (1928 line), sgt1929 f108 (1929 line), sgt1930 f642 (1928 and 1930 lines).
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 1.
