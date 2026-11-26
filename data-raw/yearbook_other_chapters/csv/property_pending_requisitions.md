# Tribunal mixte. b) Situation des affaires d'immatriculation en cours au 31 décembre

*Tribunal mixte: registration requisitions pending at 31 December, by stage of the proceeding and by year of filing, by judge.*

Source: *Statistique générale de la Tunisie*, chapter *Propriété immobilière / Tribunal mixte / Propriété foncière*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 82, f106; sgt1923 (`bpt6k9105649x`): p. 88, f590; sgt1924 (`bpt6k9105649x`): p. 90, f1080; sgt1925 (`bpt6k9105650k`): p. 92, f116; sgt1926 (`bpt6k9105650k`): p. 103, f667; sgt1927 (`bpt6k91056510`): p. 101, f129; sgt1928 (`bpt6k91056510`): p. 101, f653; sgt1929 (`bpt6k9105652d`): p. 103, f131; sgt1930 (`bpt6k9105652d`): p. 107, f665; sgt1935 (`bpt6k9105653t`): p. 73, f93; sgt1936 (`bpt6k91056547`): p. 53, f64; sgt1939 (`bpt6k9105739w`): p. 53, f59.

Transcriptions: `../transcribed/property_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_property.py build`.

Rows: 3606. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939.

Unit: number of requisitions.

Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, with `year`; no year is printed by two editions.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section: `pending` (I-III and V, by stage), `pending_age` (IV, by year of filing)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (the edition year: each edition prints the table for its own year)
- `category`: `I.1` … `III.2` (stage of the proceeding), `IV` (by year of filing), `V` (requests for rectification of material errors)
- `category_fr`: printed line heading
- `filing_year`: IV only: the year the requisition dates back to, as printed (first line: the year printed at its head, the line covering all earlier years where the heading says so)
- `judge_group`: `rapporteur_tunis`, `rapporteur_sousse` (juges rapporteurs), `delegated` (magistrats délégués à l'instruction), `commissioned` (magistrats spécialement commis); `seat` when the edition prints seats only
- `judge_group_fr`: printed column group heading
- `judge`: column code within the group (judge letter or number as printed; a column printed without heading gets its position)
- `judge_fr`: column heading as printed
- `value`: count
- `flag`: empty, or `total_mismatch` (printed value kept), `derived_from_totals`, `row_realigned`, `not_applicable` (nothing printed)

Printed column codes: juges rapporteurs of the Tunis seat (`rapporteur_tunis`, judges A, B, C) and of the Sousse seat (`rapporteur_sousse`; one judge printed over two or three columns, stored as `C1`, `C2`, … or `D1`, `D2`; sgt1925 prints three Sousse columns without heading, stored `1`-`3`; sgt1936 prints judges D and E), the magistrates delegated by the President (`delegated`, 1-3) and those commissioned by judgment (`commissioned`, 1-3) up to sgt1928; from sgt1929 one group of seven magistrates delegated or commissioned (`delegated_or_commissioned`, 1-7; sgt1935 prints the last two columns without number). sgt1939 prints the table by seat only (`judge_group` = `seat`, `judge` = `tunis` / `sousse`). The partial and general total columns and the total lines are not stored (checks).

Section III is printed as two lines (fixées au rôle, en délibéré) up to sgt1928, as one line from sgt1929 (category `III`). Section IV (requisitions by year of filing) prints no line totals in sgt1927 and sgt1928 (stored cells unaffected). The first line of IV covers all earlier years where printed so (sgt1922: "1904 et jusqu'à 1911 inclus" printed on the first line — the following lines 1905-1911 are also printed, so the first line is stored with filing_year 1904); from sgt1935 the first lines cover two years (`1909-1910`). Line V (rectification requests) is printed up to sgt1935 (all », except sgt1927 Tunis A 1).

Failed checks, all printed errors re-read on crops: sgt1922 II.2 line total 284 and Sousse C(3) column total 19 are both 19 more than the cells (the 19 requisitions of that column appear in IV by year, so the printed » on II.2 should be 19); sgt1922 IV 1911 line 25 and C(1) column 254 are both 5 more than the cells; sgt1925 IV 1923 Tunis A printed 53 where the line (154) and the column (363) need 35; sgt1926 I.3 printed partial 31 for cells summing to 91 (the general total I 831 and the grand total 1.594 need 91); sgt1927 I-III total line prints delegated 2 = 104 for lines summing to 204 (the IV total line prints 204) and IV is inconsistent in several columns (B 426 and Sousse C 282 printed for 395 and 296, as in sgt1926's totals; commissioned 1: lines 197 for 143; the line 1924 C.1 86 is clear); sgt1928 I.3 partial 116 for cells 115 (commissioned 1 column 22 for 21) and line V general total 1 with all cells »; sgt1930 IV Tunis A total 114 for lines 113.

Flagged cells: sgt1922 pending II.2 / S.C3: printed 0; its line and its column are both 19 off their printed totals (printed value kept); sgt1922 pending_age 1911 / S.C1: printed 3; its line and its column are both 5 off their printed totals (printed value kept); sgt1925 pending_age 1923 / T.A: printed 53; its line and its column are both -18 off their printed totals (printed value kept); sgt1928 pending I.3 / C.1: printed 0; its line and its column are both 1 off their printed totals (printed value kept); sgt1930 pending III / T.C: printed "7·" with its second digit broken; 73 from the column total 887 and the line total 228.

Survey of the whole chapter in every edition: `property_survey.md`.

## Validation

- Checks against printed totals and identities: 769; passed: 746; failed: 23.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.82 (f106) pending II.2: partial = T.A + T.B + S.C1 + S.C2 + S.C3 + D.1 + D.2 + D.3 + C.1 + C.2 + C.3: cells give 265, printed 284 (difference 19)
  - sgt1922 p.82 (f106) pending S.C3: lines vs Total: cells give 0, printed 19 (difference 19)
  - sgt1922 p.82 (f106) pending_age 1911: partial = T.A + T.B + S.C1 + S.C2 + S.C3 + D.1 + D.2 + D.3 + C.1 + C.2 + C.3: cells give 20, printed 25 (difference 5)
  - sgt1922 p.82 (f106) pending_age S.C1: lines vs Total: cells give 249, printed 254 (difference 5)
  - sgt1925 p.92 (f116) pending_age 1923: partial = T.A + T.B + S.1 + S.2 + S.3 + D.1 + D.2 + D.3 + C.1 + C.2 + C.3: cells give 172, printed 154 (difference -18)
  - sgt1925 p.92 (f116) pending_age T.A: lines vs Total: cells give 381, printed 363 (difference -18)
  - sgt1926 p.103 (f667) pending I.3: partial = T.A + T.B + S.C1 + S.C2 + D.1 + D.2 + D.3 + C.1 + C.2 + C.3: cells give 91, printed 31 (difference -60)
  - sgt1926 p.103 (f667) pending partial: lines vs Total: cells give 1534, printed 1594 (difference 60)
  - sgt1926 p.103 (f667) pending_groups group I = sum of its lines: cells give 771, printed 831 (difference 60)
  - sgt1927 p.101 (f129) pending Total: partial = T.A + T.B + S.C + D.1 + D.2 + D.3 + C.1 + C.2 + C.3: cells give 1878, printed 1978 (difference 100)
  - sgt1927 p.101 (f129) pending D.2: lines vs Total: cells give 204, printed 104 (difference -100)
  - sgt1927 p.101 (f129) pending_age Total: partial = T.A + T.B + S.C + D.1 + D.2 + D.3 + C.1 + C.2 + C.3: cells give 1995, printed 1978 (difference -17)
  - sgt1927 p.101 (f129) pending_age T.B: lines vs Total: cells give 395, printed 426 (difference 31)
  - sgt1927 p.101 (f129) pending_age S.C: lines vs Total: cells give 296, printed 282 (difference -14)
  - sgt1927 p.101 (f129) pending_age C.1: lines vs Total: cells give 197, printed 143 (difference -54)
  - sgt1927 p.101 (f129) pending_age T.B: Total IV = Total I-III: cells give 395, printed 426 (difference 31)
  - sgt1927 p.101 (f129) pending_age S.C: Total IV = Total I-III: cells give 296, printed 282 (difference -14)
  - sgt1927 p.101 (f129) pending_age D.2: Total IV = Total I-III: cells give 104, printed 204 (difference 100)
  - sgt1928 p.101 (f653) pending I.3: partial = T.A + T.B + S.C1 + S.C2 + D.1 + D.2 + D.3 + C.1 + C.2 + C.3: cells give 115, printed 116 (difference 1)
  - sgt1928 p.101 (f653) pending C.1: lines vs Total: cells give 21, printed 22 (difference 1)
  - sgt1928 p.101 (f653) pending_age V: partial = T.A + T.B + S.C1 + S.C2 + D.1 + D.2 + D.3 + C.1 + C.2 + C.3: cells give 0, printed 1 (difference 1)
  - sgt1930 p.107 (f665) pending_age T.A: lines vs Total: cells give 113, printed 114 (difference 1)
  - sgt1930 p.107 (f665) pending_age partial: lines vs Total: cells give 2640, printed 2641 (difference 1)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: derived_from_totals: 1, total_mismatch: 4.

  - sgt1922 p.82 1922 II.2 /  / rapporteur_sousse / C3 = 0 (total_mismatch)
  - sgt1922 p.82 1922 IV / 1911 / rapporteur_sousse / C1 = 3 (total_mismatch)
  - sgt1925 p.92 1925 IV / 1923 / rapporteur_tunis / A = 53 (total_mismatch)
  - sgt1928 p.101 1928 I.3 /  / commissioned / 1 = 0 (total_mismatch)
  - sgt1930 p.107 1930 III /  / rapporteur_tunis / C = 73 (derived_from_totals)

## Image versus OCR

- Read cell by cell on the page images (24 printings): sgt1922 f106, sgt1922 f106, sgt1923 f590, sgt1923 f590, sgt1924 f1080, sgt1924 f1080, sgt1925 f116, sgt1925 f116, sgt1926 f667, sgt1926 f667, sgt1927 f129, sgt1927 f129, sgt1928 f653, sgt1928 f653, sgt1929 f131, sgt1929 f131, sgt1930 f665, sgt1930 f665, sgt1935 f93, sgt1935 f93, sgt1936 f64, sgt1936 f64, sgt1939 f59, sgt1939 f59.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
