# Justice française : affaires commerciales, par tribunal

*French justice: commercial cases, by court.*

Source: *Statistique générale de la Tunisie*, chapter *Justice*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 64, f88, p. 66, f90; sgt1923 (`bpt6k9105649x`): p. 73, f571, p. 75, f573; sgt1924 (`bpt6k9105649x`): p. 71, f1061, p. 73, f1063; sgt1925 (`bpt6k9105650k`): p. 71, f95; sgt1926 (`bpt6k9105650k`): p. 81, f645; sgt1927 (`bpt6k91056510`): p. 83, f107; sgt1928 (`bpt6k91056510`): p. 79, f631; sgt1929 (`bpt6k9105652d`): p. 81, f109; sgt1930 (`bpt6k9105652d`): p. 85, f643; sgt1935 (`bpt6k9105653t`): p. 52, f72; sgt1936 (`bpt6k91056547`): p. 43, f54; sgt1939 (`bpt6k9105739w`): p. 43, f49.

Transcriptions: `../transcribed/justice_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_justice.py build`.

Rows: 300. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Unit: number of judgments / cases.

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

"Affaires commerciales": commercial judgments by type, bankruptcies (faillites) and liquidations per year and court; the printed *Totaux* column is used for the row check.

sgt1939 prints » in the Tunis TOTAUX column for 1937 and 1938 (stored NA, `not_applicable`; the row check is skipped).

The page-by-page survey of the chapter in every edition (every table found, with views) is in `justice_survey.md` and in `justice_validation.json` (`_survey`).

## Validation

- Checks against printed totals and identities: 196; passed: 153; failed: 43.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.64 (f88) fr_commercial [Tunis] 1922: total = contradictory + default + preparatory + on_petition + bankruptcies + liquidations: cells give 4300, printed 2780 (difference -1520)
  - sgt1922 p.66 (f90) fr_commercial [Sousse] 1915: total = contradictory + default + preparatory + on_petition + bankruptcies + liquidations: cells give 139, printed 149 (difference 10)
  - sgt1922 p.66 (f90) fr_commercial [Sousse] 1916: total = contradictory + default + preparatory + on_petition + bankruptcies + liquidations: cells give 277, printed 377 (difference 100)
  - sgt1922 p.66 (f90) fr_commercial [Sousse] 1919: total = contradictory + default + preparatory + on_petition + bankruptcies + liquidations: cells give 335, printed 235 (difference -100)
  - sgt1922 p.66 (f90) fr_commercial [Sousse] 1920: total = contradictory + default + preparatory + on_petition + bankruptcies + liquidations: cells give 310, printed 242 (difference -68)
  - sgt1923 p.73 (f571) fr_commercial [Tunis] 1922: total = contradictory + default + preparatory + on_petition + bankruptcies + liquidations: cells give 4300, printed 2780 (difference -1520)
  - sgt1923 p.75 (f573) fr_commercial [Sousse] 1915: total = contradictory + default + preparatory + on_petition + bankruptcies + liquidations: cells give 139, printed 149 (difference 10)
  - sgt1923 p.75 (f573) fr_commercial [Sousse] 1916: total = contradictory + default + preparatory + on_petition + bankruptcies + liquidations: cells give 277, printed 377 (difference 100)
  - sgt1923 p.75 (f573) fr_commercial [Sousse] 1919: total = contradictory + default + preparatory + on_petition + bankruptcies + liquidations: cells give 335, printed 235 (difference -100)
  - sgt1923 p.75 (f573) fr_commercial [Sousse] 1920: total = contradictory + default + preparatory + on_petition + bankruptcies + liquidations: cells give 310, printed 242 (difference -68)
  - sgt1924 p.71 (f1061) fr_commercial [Tunis] 1922: total = contradictory + default + preparatory + on_petition + bankruptcies + liquidations: cells give 4300, printed 2780 (difference -1520)
  - sgt1924 p.73 (f1063) fr_commercial [Sousse] 1915: total = contradictory + default + preparatory + on_petition + bankruptcies + liquidations: cells give 139, printed 149 (difference 10)
  - sgt1924 p.73 (f1063) fr_commercial [Sousse] 1916: total = contradictory + default + preparatory + on_petition + bankruptcies + liquidations: cells give 277, printed 377 (difference 100)
  - sgt1924 p.73 (f1063) fr_commercial [Sousse] 1919: total = contradictory + default + preparatory + on_petition + bankruptcies + liquidations: cells give 335, printed 235 (difference -100)
  - sgt1924 p.73 (f1063) fr_commercial [Sousse] 1920: total = contradictory + default + preparatory + on_petition + bankruptcies + liquidations: cells give 310, printed 242 (difference -68)
  - sgt1925 p.71 (f95) fr_commercial 1916: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse + bankruptcies@Sousse + liquidations@Sousse: cells give 277, printed 377 (difference 100)
  - sgt1925 p.71 (f95) fr_commercial 1919: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse + bankruptcies@Sousse + liquidations@Sousse: cells give 335, printed 235 (difference -100)
  - sgt1925 p.71 (f95) fr_commercial 1920: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse + bankruptcies@Sousse + liquidations@Sousse: cells give 310, printed 242 (difference -68)
  - sgt1925 p.71 (f95) fr_commercial 1922: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis + bankruptcies@Tunis + liquidations@Tunis: cells give 4300, printed 2780 (difference -1520)
  - sgt1926 p.81 (f645) fr_commercial 1919: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse + bankruptcies@Sousse + liquidations@Sousse: cells give 335, printed 235 (difference -100)
  - sgt1926 p.81 (f645) fr_commercial 1920: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse + bankruptcies@Sousse + liquidations@Sousse: cells give 310, printed 242 (difference -68)
  - sgt1926 p.81 (f645) fr_commercial 1922: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis + bankruptcies@Tunis + liquidations@Tunis: cells give 4300, printed 2780 (difference -1520)
  - sgt1926 p.81 (f645) fr_commercial 1926: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis + bankruptcies@Tunis + liquidations@Tunis: cells give 3145, printed 3170 (difference 25)
  - sgt1927 p.83 (f107) fr_commercial 1919: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse + bankruptcies@Sousse + liquidations@Sousse: cells give 335, printed 235 (difference -100)
  - sgt1927 p.83 (f107) fr_commercial 1920: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse + bankruptcies@Sousse + liquidations@Sousse: cells give 310, printed 242 (difference -68)
  - sgt1927 p.83 (f107) fr_commercial 1922: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis + bankruptcies@Tunis + liquidations@Tunis: cells give 4300, printed 2780 (difference -1520)
  - sgt1927 p.83 (f107) fr_commercial 1926: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis + bankruptcies@Tunis + liquidations@Tunis: cells give 3145, printed 3170 (difference 25)
  - sgt1928 p.79 (f631) fr_commercial 1919: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse + bankruptcies@Sousse + liquidations@Sousse: cells give 335, printed 235 (difference -100)
  - sgt1928 p.79 (f631) fr_commercial 1920: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse + bankruptcies@Sousse + liquidations@Sousse: cells give 310, printed 242 (difference -68)
  - sgt1928 p.79 (f631) fr_commercial 1922: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis + bankruptcies@Tunis + liquidations@Tunis: cells give 4300, printed 2780 (difference -1520)
  - sgt1928 p.79 (f631) fr_commercial 1926: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis + bankruptcies@Tunis + liquidations@Tunis: cells give 3145, printed 3170 (difference 25)
  - sgt1929 p.81 (f109) fr_commercial 1920: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse + bankruptcies@Sousse + liquidations@Sousse: cells give 310, printed 242 (difference -68)
  - sgt1929 p.81 (f109) fr_commercial 1922: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis + bankruptcies@Tunis + liquidations@Tunis: cells give 4300, printed 2780 (difference -1520)
  - sgt1929 p.81 (f109) fr_commercial 1926: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis + bankruptcies@Tunis + liquidations@Tunis: cells give 3145, printed 3170 (difference 25)
  - sgt1929 p.81 (f109) fr_commercial 1929: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis + bankruptcies@Tunis + liquidations@Tunis: cells give 4138, printed 4128 (difference -10)
  - sgt1930 p.85 (f643) fr_commercial 1922: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis + bankruptcies@Tunis + liquidations@Tunis: cells give 4300, printed 2780 (difference -1520)
  - sgt1930 p.85 (f643) fr_commercial 1926: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis + bankruptcies@Tunis + liquidations@Tunis: cells give 3145, printed 3170 (difference 25)
  - sgt1930 p.85 (f643) fr_commercial 1929: total@Tunis = contradictory@Tunis + default@Tunis + preparatory@Tunis + on_petition@Tunis + bankruptcies@Tunis + liquidations@Tunis: cells give 4138, printed 4128 (difference -10)
  - sgt1935 p.52 (f72) fr_commercial 1933: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse + bankruptcies@Sousse + liquidations@Sousse: cells give 2388, printed 2378 (difference -10)
  - sgt1935 p.52 (f72) fr_commercial 1934: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse + bankruptcies@Sousse + liquidations@Sousse: cells give 1442, printed 1542 (difference 100)
  - sgt1936 p.43 (f54) fr_commercial 1934: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse + bankruptcies@Sousse + liquidations@Sousse: cells give 1442, printed 1542 (difference 100)
  - sgt1936 p.43 (f54) fr_commercial 1936: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse + bankruptcies@Sousse + liquidations@Sousse: cells give 685, printed 677 (difference -8)
  - sgt1939 p.43 (f49) fr_commercial 1937: total@Sousse = contradictory@Sousse + default@Sousse + preparatory@Sousse + on_petition@Sousse + bankruptcies@Sousse + liquidations@Sousse: cells give 530, printed 522 (difference -8)

- Overlapping printings: 888 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: ocr_corrected: 1.

  - sgt1925 p.71 1916 Tunis / bankruptcies = 12 (ocr_corrected)

## Image versus OCR

- Read cell by cell on the page images (4 printings): sgt1926 f645, sgt1935 f72, sgt1936 f54, sgt1939 f49.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (11 printings): sgt1922 f88 Tunis, sgt1922 f90 Sousse, sgt1923 f571 Tunis, sgt1923 f573 Sousse, sgt1924 f1061 Tunis, sgt1924 f1063 Sousse, sgt1925 f95, sgt1927 f107, sgt1928 f631 (1928 line), sgt1929 f109 (1929 line), sgt1930 f643 (1930 line).
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 18.
