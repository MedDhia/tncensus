# Hôpitaux et infirmeries-dispensaires de l'intérieur : situation financière

*Hospitals and infirmaries-dispensaries of the interior: receipts by source and expenditure (sgt1922–sgt1930).*

Source: *Statistique générale de la Tunisie*, chapter III (health and assistance), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / BnF.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 53, f77; sgt1923 (`bpt6k9105649x`): p. 59, f561; sgt1924 (`bpt6k9105649x`): p. 62, f1052; sgt1925 (`bpt6k9105650k`): p. 62, f86; sgt1926 (`bpt6k9105650k`): p. 71, f635; sgt1927 (`bpt6k91056510`): p. 69, f97; sgt1928 (`bpt6k91056510`): p. 69, f621; sgt1929 (`bpt6k9105652d`): p. 71, f99; sgt1930 (`bpt6k9105652d`): p. 75, f633.

Transcriptions: `../transcribed/health_finance_<edition>.txt`, sections `[hospital_finance]`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_finance.py build`. Per-check output: `health_finance_validation.json`.

Rows: 1376. Years: 1922–1930. Unit of `value`: francs; amounts are as printed, centimes kept as decimals (printed » = 0).

Printed once per edition; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (for a table over two pages, the page of the column group)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (budget year, account year or calendar year; see below)
- `hospital`: hospital as printed (day-cost table: `civil`, `sadiki`, `rabta`)
- `measure`: what the value is (see below)
- `column_fr`: column heading as printed (French)
- `value`: francs; empty where the flag says so
- `flag`: empty, or `derived_from_totals`, `total_mismatch`, `not_applicable`, `illegible`, `reprint_corrected` (see below)

a) "Situation financière" of the hospitals and infirmaries-dispensaries of the interior (sgt1922–sgt1930; from sgt1935 the interior table has no financial part). `year` = the edition's year, as for the "Renseignements généraux" table in `health_interior_hospitals.csv`. Hospital names as printed. The columns change with the edition (`measure`, with the heading in `column_fr`): sgt1922–sgt1924 subsidies from the State, temporary indigenous contributions, public assistance, Habous and municipalities; sgt1925 participation of the State, the Region and the communes; sgt1926–sgt1927 State, Regions, public assistance, Habous, municipalities; sgt1928–sgt1930 State, Region, municipality; then in every edition the proceeds of patient-days (`patient_day_receipts`), other receipts, total receipts (not stored: printed row total) and expenditure. The TOTAL line is not stored.

This table was not in the inherited draft. It was drafted from the Gallica OCR with column bands taken from the page rules and then read on the page images, every row, at native resolution (two crops per page); about 100 OCR misreadings were corrected. Flags: `derived_from_totals` for sgt1922 Enfidaville expenditure (blotted digit; 9.416,84 is what the column total needs), sgt1927 Djerba State subsidy (first digit lost in the binding; 20.000 closes the row), sgt1930 Tabarka municipality (printed "2.00"; 2.100 closes the row, the column total would need 1.750); `total_mismatch` for cells that make both their row and their column disagree and whose correction closes both: sgt1925 Kef and Djerba total receipts (not stored), sgt1927 Monastir Régions 50.000 (40.000), sgt1928 Souk-el-Arba other receipts 31.673,85 (81.673,85); `not_applicable` for sgt1925 Ferryville, whose total receipts and expenditure are printed » (its receipts are not in the printed TOTAL line either). sgt1923 Medjez-el-Bab expenditure is printed "50.8988 73" and stored as 50.898,73 (the value the column total needs). sgt1923 Gabès is printed » in every column (no account) and is not stored.

The remaining failed checks are in the print: the sgt1929 table in particular (Souk-el-Arba, Madhia, Thala, Kairouan totals that do not add up; four of seven column totals off), sgt1930 (Sousse, Kairouan, Médenine). Some rows repeat the previous edition's figures exactly: sgt1929 Bizerte = sgt1928 Bizerte, sgt1930 Medjez-el-Bab = sgt1929 Medjez-el-Bab; sgt1923 Mateur and Grombalia = sgt1924. They are kept as printed.

## Remarks recorded in the transcriptions

- sgt1922: Hospitals and infirmaries-dispensaries of the interior, a) Situation financière (francs; the year is the edition's year, as for the interior table of health_pop). Drafted from Gallica OCR with column bands taken from the page rules, then checked against the printed row and column totals and the page image.
- sgt1923: Hospitals and infirmaries-dispensaries of the interior, a) Situation financière (francs; the year is the edition's year, as for the interior table of health_pop). Drafted from Gallica OCR with column bands taken from the page rules, then checked against the printed row and column totals and the page image. Medjez-el-Bab expenditure is printed "50.8988 73" (a doubled 8); 50.898,73 is the value the column total needs.
- sgt1924: Hospitals and infirmaries-dispensaries of the interior, a) Situation financière (francs; the year is the edition's year, as for the interior table of health_pop). Drafted from Gallica OCR with column bands taken from the page rules, then checked against the printed row and column totals and the page image.
- sgt1925: Hospitals and infirmaries-dispensaries of the interior, a) Situation financière (francs; the year is the edition's year, as for the interior table of health_pop). Drafted from Gallica OCR with column bands taken from the page rules, then checked against the printed row and column totals and the page image. Ferryville: total receipts and expenditure printed » (not reported; stored NA, not_applicable); the printed TOTAL line (receipts 1.402.416,35 = 1.435.487,65 - 33.071,30) leaves Ferryville out. The column of total receipts agrees with the printed TOTAL (within 20) when Kef (Le) and Djerba are taken at the sum of their parts.
- sgt1926: Hospitals and infirmaries-dispensaries of the interior, a) Situation financière (francs; the year is the edition's year, as for the interior table of health_pop). Drafted from Gallica OCR with column bands taken from the page rules, then checked against the printed row and column totals and the page image.
- sgt1927: Hospitals and infirmaries-dispensaries of the interior, a) Situation financière (francs; the year is the edition's year, as for the interior table of health_pop). Drafted from Gallica OCR with column bands taken from the page rules, then checked against the printed row and column totals and the page image. Monastir: Régions printed 50.000; 40.000 closes both the row total (175.990,17) and the column total (554.850). Djerba: the first digit of the State subsidy is lost in the binding ("?0.000"); 20.000 closes the row total.
- sgt1928: Hospitals and infirmaries-dispensaries of the interior, a) Situation financière (francs; the year is the edition's year, as for the interior table of health_pop). Drafted from Gallica OCR with column bands taken from the page rules, then checked against the printed row and column totals and the page image. Souk-el-Arba: other receipts printed 31.673,85; 81.673,85 closes both the row total and the column total (494.421,54).
- sgt1929: Hospitals and infirmaries-dispensaries of the interior, a) Situation financière (francs; the year is the edition's year, as for the interior table of health_pop). Drafted from Gallica OCR with column bands taken from the page rules, then checked against the printed row and column totals and the page image.
- sgt1930: Hospitals and infirmaries-dispensaries of the interior, a) Situation financière (francs; the year is the edition's year, as for the interior table of health_pop). Drafted from Gallica OCR with column bands taken from the page rules, then checked against the printed row and column totals and the page image. Tabarka: municipality printed "2.00" (a digit missing); 2.100 closes the row total 14.100.

## Validation

- Checks against printed totals: 276; passed: 235; failed: 41.

Failed checks (printed values kept, unless a flag below says otherwise; `L<n>` = line of the transcription file). See the commentary above for which ones were re-read on the page images and which are repeated identically in several printings:

  - sgt1922 L228 Médenine et annexes: receipts vs total receipts: cells give 88807.34, printed 88807.37
  - sgt1922 column total_receipts: hospitals vs TOTAL: cells give 887124.93, printed 887124.9
  - sgt1924 column expenditure: hospitals vs TOTAL: cells give 1003124.89, printed 1002764.89
  - sgt1925 L263 Kef (Le): receipts vs total receipts: cells give 139221.55, printed 137076.5
  - sgt1925 L274 Djerba: receipts vs total receipts: cells give 77673.22, printed 77693.22
  - sgt1925 L285 TOTAL: receipts vs total receipts: cells give 1435487.65, printed 1402416.35
  - sgt1925 column total_receipts: hospitals vs TOTAL: cells give 1400291.3, printed 1402416.35
  - sgt1925 column expenditure: hospitals vs TOTAL: cells give 1337931.2, printed 1337976.2
  - sgt1926 L295 Médenine: receipts vs total receipts: cells give 105194.2, printed 105184.2
  - sgt1926 column other_receipts: hospitals vs TOTAUX: cells give 403513.33, printed 403503.33
  - sgt1927 L285 Monastir: receipts vs total receipts: cells give 185990.17, printed 175990.17
  - sgt1927 column regions: hospitals vs TOTAUX: cells give 564850, printed 554850
  - sgt1927 column expenditure: hospitals vs TOTAUX: cells give 2094409.26, printed 2104406.55
  - sgt1928 L295 Souk-el-Arba: receipts vs total receipts: cells give 166703.85, printed 216703.85
  - sgt1928 column other_receipts: hospitals vs TOTAUX: cells give 444421.54, printed 494421.54
  - sgt1929 L290 Souk-el-Arba: receipts vs total receipts: cells give 169956.66, printed 180694.31
  - sgt1929 L291 Grombalia: receipts vs total receipts: cells give 69116.56, printed 69117.01
  - sgt1929 L292 Nabeul: receipts vs total receipts: cells give 57363.75, printed 57360.75
  - sgt1929 L295 Tabarka: receipts vs total receipts: cells give 79907.56, printed 82907.56
  - sgt1929 L300 Madhia: receipts vs total receipts: cells give 57250, printed 84250
  - sgt1929 L302 Thala: receipts vs total receipts: cells give 25699.33, printed 16999.33
  - sgt1929 L303 Kairouan: receipts vs total receipts: cells give 228934.5, printed 268000
  - sgt1929 L306 Tozeur: receipts vs total receipts: cells give 43777.58, printed 43777.78
  - sgt1929 L308 TOTAUX: receipts vs total receipts: cells give 2453820.0, printed 2453820.5
  - sgt1929 column region: hospitals vs TOTAUX: cells give 616000, printed 611000
  - sgt1929 column municipality: hospitals vs TOTAUX: cells give 190134, printed 188734
  - sgt1929 column patient_day_receipts: hospitals vs TOTAUX: cells give 397924.9, printed 407933.9
  - sgt1929 column other_receipts: hospitals vs TOTAUX: cells give 348260.1, printed 349260.1
  - sgt1929 column total_receipts: hospitals vs TOTAUX: cells give 2520311.8, printed 2453820.5
  - sgt1929 column total_expenditure: hospitals vs TOTAUX: cells give 2325005.59, printed 2305005.59
  - sgt1930 L322 Maktar: receipts vs total receipts: cells give 97071.75, printed 97071.45
  - sgt1930 L324 Sousse: receipts vs total receipts: cells give 503297.03, printed 403297.03
  - sgt1930 L325 Enfidaville: receipts vs total receipts: cells give 17971, printed 17917
  - sgt1930 L329 Kairouan: receipts vs total receipts: cells give 200405.5, printed 255405.5
  - sgt1930 L331 Djerba: receipts vs total receipts: cells give 102868.01, printed 102873.5
  - sgt1930 L333 Médenine: receipts vs total receipts: cells give 92275.85, printed 164798.34
  - sgt1930 column state: hospitals vs TOTAUX: cells give 956415.26, printed 946415.26
  - sgt1930 column municipality: hospitals vs TOTAUX: cells give 223000, printed 222650
  - sgt1930 column other_receipts: hospitals vs TOTAUX: cells give 602393.8, printed 622393.8
  - sgt1930 column total_receipts: hospitals vs TOTAUX: cells give 2743197.19, printed 2725373.51
  - sgt1930 column total_expenditure: hospitals vs TOTAUX: cells give 2314267.91, printed 2314267.82

- Flagged cells: derived_from_totals: 3, not_applicable: 1, total_mismatch: 2.

  - sgt1922 1922 Enfidaville / expenditure / Dépenses = 9416.84 (derived_from_totals)
  - sgt1925 1925 Ferryville / expenditure / Dépenses = None (not_applicable)
  - sgt1927 1927 Monastir / regions / Subventions : Participation des Régions = 50000 (total_mismatch)
  - sgt1927 1927 Djerba / state / Subventions : État = 20000 (derived_from_totals)
  - sgt1928 1928 Souk-el-Arba / other_receipts / Autres recettes = 31673.85 (total_mismatch)
  - sgt1930 1930 Tabarka / municipality / Subventions : Municipalité = 2100 (derived_from_totals)
