# Répartition des condamnés d'après la nationalité, la nature du délit et la catégorie pénale

*Condemned prisoners by nationality, offence and sentence.*

Source: *Statistique générale de la Tunisie*, chapter *Établissements pénitentiaires*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 73, f97; sgt1923 (`bpt6k9105649x`): p. 79, f581; sgt1924 (`bpt6k9105649x`): p. 81, f1071; sgt1925 (`bpt6k9105650k`): p. 83, f107; sgt1926 (`bpt6k9105650k`): p. 93, f657; sgt1927 (`bpt6k91056510`): p. 91, f119; sgt1928 (`bpt6k91056510`): p. 91, f643; sgt1929 (`bpt6k9105652d`): p. 93, f121; sgt1930 (`bpt6k9105652d`): p. 97, f655; sgt1935 (`bpt6k9105653t`): p. 63, f83; sgt1936 (`bpt6k91056547`): p. 47, f58; sgt1939 (`bpt6k9105739w`): p. 47, f53.

Transcriptions: `../transcribed/prisons_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_prisons.py build`.

Rows: 2496. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939.

Unit: persons (condemned prisoners).

Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, with `year`; no year is printed by two editions.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section name (`condemned_offence`); printed as table b) up to sgt1935, without a letter in sgt1936 and sgt1939
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (the edition year: each edition prints the table for its own year)
- `offence`: `murder`, `assault`, `indecent_assault`, `theft`, `drunkenness`, `grazing_offence`, `escape`, `bankrupts`, `debtors`, `bankrupts_debtors`, `political`, `other`
- `offence_fr`: line label as printed (*nature des délits*)
- `penalty`: `death` (*peine capitale*, printed from sgt1925), `hard_labour` (*travaux forcés*), `reclusion`, `prison_over_1y` (*emprisonnement à 1 an et 1 jour et au-dessus*), `prison_1y_or_less` (*emprisonnement à 1 an et au-dessous*)
- `penalty_fr`: printed column-group heading
- `nationality`: `french`, `european` (other Europeans), `algerian`, `tunisian` (peine capitale "Tunisiens", all Tunisians), `tunisian_muslim` ("Tunisiens" beside an "Israélites" column up to sgt1925, "Tunisiens : Musulmans" from sgt1926), `tunisian_jewish`, `tripolitanian`, `other` (*divers*)
- `nationality_fr`: printed column heading
- `value`: number of condemned prisoners
- `flag`: empty, `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable` (SPEC.md)

Printed once per edition, for the edition year, under the nationality / age table (b) up to sgt1935). The nationality columns differ by sentence and by edition: each sentence group has its own set (e.g. Tripolitains only under emprisonnement ≤ 1 an in sgt1922-sgt1924; no Israélites under réclusion in sgt1922-sgt1923's Divers-less set; Divers instead of Israélites under réclusion in sgt1936 and sgt1939). A column not printed has no rows. Column order changes in sgt1927 (Français, Algériens, Européens, …) but the headings are the same. The offence lines change too (Évasions only sgt1922; Faillis and Dettiers separate sgt1923-sgt1924, merged sgt1925-sgt1930, Faillis alone and a new Politiques line from sgt1935).

Not stored: each group's "Total" column, the "Total général" column (sgt1935 only) and the "Totaux" line; they are the checks. Checks: each group's Total = sum of its nationality columns, on every line; Total général = peine capitale + the four group totals (sgt1935); every column against the Totaux line; and, per edition, the grand total of the table (death sentences included) against the "Totaux / Total par nationalité" of the nationality / age table.

sgt1928: the travaux forcés "Total" column is printed half a line to a line low from Attentat à la pudeur down (3 between Attentat and Vol, 4 on the Ivresse line, 1 under Divers); it is transcribed on the lines whose cells it sums (it is a check column, not stored).

sgt1924: travaux forcés, Attentat à la pudeur prints 36 under Algériens and nothing under Tunisiens; the Algériens and Tunisiens column totals (37 and 424) agree with the cells as printed, so the printed placement is kept (it may be a column slip in the original).

sgt1925 and sgt1926: the travaux forcés "Total" includes the death sentences printed in the peine capitale columns just left of it (sgt1925: Meurtre 52 + 4 = 56, Totaux 122 + 4 = 126, and the table's grand total is then exactly the nationality table's 9.254; sgt1926: Meurtre 49 + 1 = 50, Totaux 111 + 1 = 112); the checks are made that way for these two editions (`hl_total_includes_death=1` in the transcription). sgt1926's grand total is then 9.148 against the nationality table's 9.149, an unlocated difference of 1.

Failures involving only printed totals (no stored cell flagged; cells re-read on crops): sgt1929 emprisonnement ≤ 1 an, Totaux Français printed 26 for lines summing to 27 (the Totaux line's Total 7.273 needs 27); sgt1935 emprisonnement ≤ 1 an, Attentat à la pudeur Total printed 205 for 1 + 205 = 206 (Total général 235 and the column total 9.480 both need 206); sgt1936 emprisonnement > 1 an, Totaux Musulmans printed 330 for lines summing to 320 (the Totaux line's Total 341 needs 320).

Every cell of every edition was read on the native-resolution page image (two crops per table), and each failing line or column re-read on a separate enlarged crop.

Cells flagged `total_mismatch` (printed value kept, re-read on a native-resolution crop): sgt1922: Vol / ps.Français (emprisonnement ≤ 1 an, Vol, Français printed 11: the line sums to 3.032 for a printed 3.035 and the Français column to 28 for a printed 31, both 3 short at this cell).

Cells flagged `row_realigned` (stored on the line their content belongs to): sgt1929 Attentat à la pudeur / hl.Européens: printed on the line above (Coups, blessures, agressions); with the 1 there neither line gives its printed total (3 for 2, 3 for 4), with it here both do.

## Validation

- Checks against printed totals and identities: 821; passed: 811; failed: 10.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.73 (f97) condemned_offence Vol: ps.Total = ps.Français + ps.Européens + ps.Algériens + ps.Tunisiens + ps.Tripolitains + ps.Israélites: cells give 3032, printed 3035 (difference 3)
  - sgt1922 p.73 (f97) condemned_offence ps.Français: lines vs Totaux: cells give 28, printed 31 (difference 3)
  - sgt1929 p.93 (f121) condemned_offence Totaux: ps.Total = ps.Français + ps.Algériens + ps.Européens + ps.Musulmans + ps.Israélites + ps.Divers: cells give 7272, printed 7273 (difference 1)
  - sgt1929 p.93 (f121) condemned_offence ps.Français: lines vs Totaux: cells give 27, printed 26 (difference -1)
  - sgt1935 p.63 (f83) condemned_offence Attentat à la pudeur: ps.Total = ps.Français + ps.Algériens + ps.Européens + ps.Musulmans + ps.Israélites + ps.Divers: cells give 206, printed 205 (difference -1)
  - sgt1935 p.63 (f83) condemned_offence Attentat à la pudeur: grand_total = dp.Européens + dp.Tunisiens + hl.Total + rc.Total + pl.Total + ps.Total: cells give 234, printed 235 (difference 1)
  - sgt1935 p.63 (f83) condemned_offence ps.Total: lines vs Totaux: cells give 9479, printed 9480 (difference 1)
  - sgt1936 p.47 (f58) condemned_offence Totaux: pl.Total = pl.Français + pl.Algériens + pl.Européens + pl.Musulmans + pl.Israélites + pl.Divers: cells give 351, printed 341 (difference -10)
  - sgt1936 p.47 (f58) condemned_offence pl.Musulmans: lines vs Totaux: cells give 320, printed 330 (difference 10)
  - sgt1926 p.93 (f657) condemned_offence Totaux, all sentences vs the nationality / age table's total (sgt1926 p.93 (f657) condemned_age): cells give 9148, printed 9149 (difference 1)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: row_realigned: 1, total_mismatch: 1.

  - sgt1922 p.73 1922 theft / prison_1y_or_less / french = 11 (total_mismatch)
  - sgt1929 p.93 1929 indecent_assault / hard_labour / european = 1 (row_realigned)

## Image versus OCR

- Read cell by cell on the page images (12 printings): sgt1922 f97, sgt1923 f581, sgt1924 f1071, sgt1925 f107, sgt1926 f657, sgt1927 f119, sgt1928 f643, sgt1929 f121, sgt1930 f655, sgt1935 f83, sgt1936 f58, sgt1939 f53.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
