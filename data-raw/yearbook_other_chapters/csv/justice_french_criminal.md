# Justice française : affaires criminelles et correctionnelles jugées, par tribunal

*French justice: criminal and correctional cases judged, by court.*

Source: *Statistique générale de la Tunisie*, chapter *Justice*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 63, f87, p. 65, f89; sgt1923 (`bpt6k9105649x`): p. 72, f570, p. 74, f572; sgt1924 (`bpt6k9105649x`): p. 70, f1060, p. 72, f1062; sgt1925 (`bpt6k9105650k`): p. 70, f94; sgt1926 (`bpt6k9105650k`): p. 80, f644; sgt1927 (`bpt6k91056510`): p. 82, f106; sgt1928 (`bpt6k91056510`): p. 78, f630; sgt1929 (`bpt6k9105652d`): p. 80, f108; sgt1930 (`bpt6k9105652d`): p. 84, f642; sgt1935 (`bpt6k9105653t`): p. 52, f72; sgt1936 (`bpt6k91056547`): p. 43, f54; sgt1939 (`bpt6k9105739w`): p. 43, f49.

Transcriptions: `../transcribed/justice_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_justice.py build`.

Rows: 150. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Unit: number of cases.

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

"Affaires criminelles et correctionnelles": criminal cases judged (by the criminal court) and correctional cases judged after a hearing of both parties (contradictoirement) or by default (par défaut), per year, for the Tribunal de première instance of Tunis and of Sousse. The printed *Totaux* (not stored, used for the row check) exclude, says the footnote, "the default cases brought back on opposition" (affaires par défaut revenues sur opposition).

The page-by-page survey of the chapter in every edition (every table found, with views) is in `justice_survey.md` and in `justice_validation.json` (`_survey`).

## Validation

- Checks against printed totals and identities: 198; passed: 142; failed: 56.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.63 (f87) fr_criminal [Tunis] 1917: total = criminal + correctional_contradictory + correctional_default: cells give 1305, printed 1287 (difference -18)
  - sgt1922 p.63 (f87) fr_criminal [Tunis] 1919: total = criminal + correctional_contradictory + correctional_default: cells give 1495, printed 1473 (difference -22)
  - sgt1922 p.63 (f87) fr_criminal [Tunis] 1921: total = criminal + correctional_contradictory + correctional_default: cells give 2242, printed 2198 (difference -44)
  - sgt1922 p.65 (f89) fr_criminal [Sousse] 1920: total = criminal + correctional_contradictory + correctional_default: cells give 538, printed 520 (difference -18)
  - sgt1923 p.72 (f570) fr_criminal [Tunis] 1917: total = criminal + correctional_contradictory + correctional_default: cells give 1305, printed 1287 (difference -18)
  - sgt1923 p.72 (f570) fr_criminal [Tunis] 1919: total = criminal + correctional_contradictory + correctional_default: cells give 1495, printed 1473 (difference -22)
  - sgt1923 p.72 (f570) fr_criminal [Tunis] 1921: total = criminal + correctional_contradictory + correctional_default: cells give 2242, printed 2198 (difference -44)
  - sgt1923 p.74 (f572) fr_criminal [Sousse] 1920: total = criminal + correctional_contradictory + correctional_default: cells give 538, printed 520 (difference -18)
  - sgt1923 p.74 (f572) fr_criminal [Sousse] 1923: total = criminal + correctional_contradictory + correctional_default: cells give 449, printed 432 (difference -17)
  - sgt1924 p.70 (f1060) fr_criminal [Tunis] 1917: total = criminal + correctional_contradictory + correctional_default: cells give 1305, printed 1287 (difference -18)
  - sgt1924 p.70 (f1060) fr_criminal [Tunis] 1919: total = criminal + correctional_contradictory + correctional_default: cells give 1495, printed 1473 (difference -22)
  - sgt1924 p.70 (f1060) fr_criminal [Tunis] 1921: total = criminal + correctional_contradictory + correctional_default: cells give 2242, printed 2198 (difference -44)
  - sgt1924 p.72 (f1062) fr_criminal [Sousse] 1920: total = criminal + correctional_contradictory + correctional_default: cells give 538, printed 520 (difference -18)
  - sgt1924 p.72 (f1062) fr_criminal [Sousse] 1923: total = criminal + correctional_contradictory + correctional_default: cells give 449, printed 432 (difference -17)
  - sgt1925 p.70 (f94) fr_criminal 1920: total@Sousse = criminal@Sousse + correctional_contradictory@Sousse + correctional_default@Sousse: cells give 638, printed 520 (difference -118)
  - sgt1925 p.70 (f94) fr_criminal 1923: total@Sousse = criminal@Sousse + correctional_contradictory@Sousse + correctional_default@Sousse: cells give 449, printed 432 (difference -17)
  - sgt1925 p.70 (f94) fr_criminal 1917: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 1305, printed 1287 (difference -18)
  - sgt1925 p.70 (f94) fr_criminal 1919: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 1495, printed 1473 (difference -22)
  - sgt1925 p.70 (f94) fr_criminal 1921: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 2242, printed 2198 (difference -44)
  - sgt1925 p.70 (f94) fr_criminal 1925: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 2079, printed 2050 (difference -29)
  - sgt1926 p.80 (f644) fr_criminal 1920: total@Sousse = criminal@Sousse + correctional_contradictory@Sousse + correctional_default@Sousse: cells give 638, printed 520 (difference -118)
  - sgt1926 p.80 (f644) fr_criminal 1923: total@Sousse = criminal@Sousse + correctional_contradictory@Sousse + correctional_default@Sousse: cells give 449, printed 432 (difference -17)
  - sgt1926 p.80 (f644) fr_criminal 1917: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 1305, printed 1287 (difference -18)
  - sgt1926 p.80 (f644) fr_criminal 1919: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 1495, printed 1473 (difference -22)
  - sgt1926 p.80 (f644) fr_criminal 1921: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 2242, printed 2198 (difference -44)
  - sgt1926 p.80 (f644) fr_criminal 1925: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 2079, printed 2050 (difference -29)
  - sgt1926 p.80 (f644) fr_criminal 1926: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 1824, printed 1787 (difference -37)
  - sgt1927 p.82 (f106) fr_criminal 1920: total@Sousse = criminal@Sousse + correctional_contradictory@Sousse + correctional_default@Sousse: cells give 638, printed 520 (difference -118)
  - sgt1927 p.82 (f106) fr_criminal 1923: total@Sousse = criminal@Sousse + correctional_contradictory@Sousse + correctional_default@Sousse: cells give 449, printed 432 (difference -17)
  - sgt1927 p.82 (f106) fr_criminal 1919: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 1495, printed 1473 (difference -22)
  - sgt1927 p.82 (f106) fr_criminal 1921: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 2242, printed 2198 (difference -44)
  - sgt1927 p.82 (f106) fr_criminal 1925: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 2079, printed 2050 (difference -29)
  - sgt1927 p.82 (f106) fr_criminal 1926: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 1824, printed 1787 (difference -37)
  - sgt1928 p.78 (f630) fr_criminal 1920: total@Sousse = criminal@Sousse + correctional_contradictory@Sousse + correctional_default@Sousse: cells give 638, printed 520 (difference -118)
  - sgt1928 p.78 (f630) fr_criminal 1923: total@Sousse = criminal@Sousse + correctional_contradictory@Sousse + correctional_default@Sousse: cells give 449, printed 432 (difference -17)
  - sgt1928 p.78 (f630) fr_criminal 1928: total@Sousse = criminal@Sousse + correctional_contradictory@Sousse + correctional_default@Sousse: cells give 702, printed 704 (difference 2)
  - sgt1928 p.78 (f630) fr_criminal 1919: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 1495, printed 1473 (difference -22)
  - sgt1928 p.78 (f630) fr_criminal 1921: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 2242, printed 2198 (difference -44)
  - sgt1928 p.78 (f630) fr_criminal 1925: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 2079, printed 2050 (difference -29)
  - sgt1928 p.78 (f630) fr_criminal 1926: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 1824, printed 1787 (difference -37)
  - sgt1929 p.80 (f108) fr_criminal 1920: total@Sousse = criminal@Sousse + correctional_contradictory@Sousse + correctional_default@Sousse: cells give 638, printed 520 (difference -118)
  - sgt1929 p.80 (f108) fr_criminal 1923: total@Sousse = criminal@Sousse + correctional_contradictory@Sousse + correctional_default@Sousse: cells give 449, printed 432 (difference -17)
  - sgt1929 p.80 (f108) fr_criminal 1928: total@Sousse = criminal@Sousse + correctional_contradictory@Sousse + correctional_default@Sousse: cells give 702, printed 704 (difference 2)
  - sgt1929 p.80 (f108) fr_criminal 1929: total@Sousse = criminal@Sousse + correctional_contradictory@Sousse + correctional_default@Sousse: cells give 711, printed 712 (difference 1)
  - sgt1929 p.80 (f108) fr_criminal 1921: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 2242, printed 2198 (difference -44)
  - sgt1929 p.80 (f108) fr_criminal 1925: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 2079, printed 2050 (difference -29)
  - sgt1929 p.80 (f108) fr_criminal 1926: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 1824, printed 1787 (difference -37)
  - sgt1929 p.80 (f108) fr_criminal 1929: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 2269, printed 2236 (difference -33)
  - sgt1930 p.84 (f642) fr_criminal 1923: total@Sousse = criminal@Sousse + correctional_contradictory@Sousse + correctional_default@Sousse: cells give 449, printed 432 (difference -17)
  - sgt1930 p.84 (f642) fr_criminal 1928: total@Sousse = criminal@Sousse + correctional_contradictory@Sousse + correctional_default@Sousse: cells give 702, printed 704 (difference 2)
  - sgt1930 p.84 (f642) fr_criminal 1929: total@Sousse = criminal@Sousse + correctional_contradictory@Sousse + correctional_default@Sousse: cells give 711, printed 712 (difference 1)
  - sgt1930 p.84 (f642) fr_criminal 1921: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 2242, printed 2198 (difference -44)
  - sgt1930 p.84 (f642) fr_criminal 1925: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 2079, printed 2050 (difference -29)
  - sgt1930 p.84 (f642) fr_criminal 1926: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 1824, printed 1787 (difference -37)
  - sgt1930 p.84 (f642) fr_criminal 1929: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 2269, printed 2236 (difference -33)
  - sgt1935 p.52 (f72) fr_criminal 1933: total@Tunis = criminal@Tunis + correctional_contradictory@Tunis + correctional_default@Tunis: cells give 3390, printed 3384 (difference -6)

- Overlapping printings: 444 cell comparisons with other editions printing the same cell; 3 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1920 / Sousse /  /  /  /  / correctional_contradictory | sgt1922 | 416 | sgt1929 | 516 |
| 1920 / Sousse /  /  /  /  / correctional_contradictory | sgt1923 | 416 | sgt1929 | 516 |
| 1920 / Sousse /  /  /  /  / correctional_contradictory | sgt1924 | 416 | sgt1929 | 516 |

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (6 printings): sgt1924 f1060 Tunis, sgt1925 f94, sgt1926 f644, sgt1935 f72, sgt1936 f54, sgt1939 f49.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (9 printings): sgt1922 f87 Tunis, sgt1922 f89 Sousse, sgt1923 f570 Tunis, sgt1923 f572 Sousse, sgt1924 f1062 Sousse, sgt1927 f106, sgt1928 f630 (1928 line), sgt1929 f108 (1929 line), sgt1930 f642 (1930 line).
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 1.
