# Sociétés indigènes (tunisiennes) de prévoyance. Opérations

*Indigenous (Tunisian) provident societies: loans by type, loans cancelled, recoveries by type and loans outstanding, by year (1913-1939).*

Source: *Statistique générale de la Tunisie*, chapter *Institutions économiques et sociales / Mutualité agricole*, editions sgt1922, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 440, f464; sgt1924 (`bpt6k9105649x`): p. 462, f1452; sgt1925 (`bpt6k9105650k`): p. 498, f522; sgt1926 (`bpt6k9105650k`): p. 466, f1030; sgt1927 (`bpt6k91056510`): p. 466, f494; sgt1928 (`bpt6k91056510`): p. 470, f1022; sgt1929 (`bpt6k9105652d`): p. 472, f500; sgt1930 (`bpt6k9105652d`): p. 480, f1036; sgt1935 (`bpt6k9105653t`): p. 296, f316; sgt1936 (`bpt6k91056547`): p. 174, f185; sgt1939 (`bpt6k9105739w`): p. 154, f160.

Transcriptions: `../transcribed/mutuality_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_mutuality.py build`.

Rows: 445. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Units: francs (centimes as decimals); suggested value_type: francs.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (rule 4 tables: the latest edition printing that year)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `total_mismatch` (printed cell contradicted by its printed row total and by the other printings, kept as printed), `illegible`, `reprint_corrected` (illegible in the edition kept: value of the latest earlier printing), `derived_from_totals` (sgt1939 1936 annulation: second centime digit in the binding, = printed TOTAUX minus the other lines)

Printed in every edition (two-page spread) for the ten years before it: sgt1922 1913-1922, sgt1923 1914-1923, sgt1924 1914-1924, sgt1925 1916-1925 ... sgt1930 1921-1930 (title 1920-1930), sgt1935 1926-1935, sgt1936 1927-1936, sgt1939 1930-1939. *Sociétés indigènes de prévoyance* up to sgt1930, *sociétés tunisiennes de prévoyance* from sgt1935.

Columns: montant des prêts by type (semences; campagne from sgt1923; subsistance; hypothécaires; sur gages from sgt1935; cheptel and soufre et sulfate de cuivre from sgt1936; avances aux filiales) and total; annulation of prêts de subsistance (sgt1936-sgt1939: prêts de semences et de subsistance, same code `loans_cancelled`, `measure_fr` of the edition kept; footnote on 1936: of which 15.307.447,46 for seed loans); différence (= total minus annulation: a printed check column, not stored); montant des recouvrements by the same types and total; reste à recouvrer sur les prêts. A type not printed by an edition has no rows for its years from that edition.

Reste à recouvrer: sgt1922-sgt1924 print it per line except a single figure 488.536,84 braced against 1914-1919; sgt1925-sgt1939 print a single figure braced against every line (= the TOTAUX). Each braced figure is stored on the last year it covers (it is a balance at that date): `loans_outstanding` therefore exists for 1913, 1919-1924 (sgt1922-sgt1924) and for 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936 and 1939 (one per edition).

Printed row totals (total, total des recouvrements, différence) and the TOTAUX lines are checks only. The TOTAUX of sgt1923 include the 1913 line (printed only in sgt1922) and those of sgt1930 the 1920 line (title 1920-1930, last printed in sgt1929); they are checked with those lines.

The sgt1936 spread is badly printed (broken and misplaced type, solid black slugs where » is expected, typed 0); several of its cells contradict the row totals and every other printing (see the failed checks). Where such a cell is the latest printing (1928 recouvrements de semences 31.012.273,27 and total 31.504.741,66, 1929 recouvrements total 24.476.247,63) or is illegible (1928 prêts de semences), the sgt1935 printing is stored with flag `reprint_corrected` (32.012.273,27, 34.504.741,66, 24.807.247,63, 44.240.438,47; each makes the row add up). Its 1927 recouvrements de soufre, printed 91.661,95 (the campagne figure repeated; the row total and the TOTAUX 5.348,50 imply »), has no other printing and is kept with flag `total_mismatch`. The différence column of sgt1935-sgt1939 runs into the binding (not typed). sgt1935 prints 1929 recouvrements de semences 21.173.131,91 and de subsistance 2.127.895,34 (sgt1929-sgt1930: 21.173.131,19 and 2.127.896,06; both pairs give the printed total), followed by sgt1936; the later printing is kept.

Every failed check below was re-read on a native-resolution crop: the printed values are kept. sgt1922 and sgt1923 print the 1916 seed loans 1.570.483,20 (sgt1924 and later 1.570.483,26, which makes the printed row total and the TOTAUX add up; flagged `total_mismatch` in those printings). sgt1925: 1924 recouvrements total printed 3.206.471,45 for types giving 2.706.471,45 (sgt1926 and later print 2.706.471,45; flagged), and its TOTAUX of the seed and subsistence loans are 600 and 80.000 above the lines (the TOTAUX of the total column agrees with the lines, so the two column TOTAUX are misprinted). sgt1928: TOTAUX avances aux filiales 0,02 below the lines. sgt1929: TOTAUX recouvrements total 146.926.197,45, 1.000 above the lines and above the sum of its own TOTAUX by type. sgt1930: TOTAUX recouvrements avances aux filiales 4.060.222,65 and total 164.402.074,23 for lines (with the 1920 line of sgt1929) giving 4.063.222,65 and 154.402.074,23 (one digit misprinted in each). sgt1935: 1934 recouvrements total 10.537.603,17 for types giving ,16 (sgt1939 ,16; flagged), TOTAUX of the total 0,03 and of the recouvrements de subsistance 0,01 off. sgt1936 (badly printed page): the row failures are its misprints listed above (1927 soufre, 1928 and 1932 recouvrements de semences, 1932 recouvrements de campagne 19.683,95 for 19.683,11, 1932 total 32.738.151,54, 1934 total 32.765.588,31 and recouvrements total 10.527.603,16, 1935 total 10.980.031,30, 1936 recouvrements sur gages 2.440.267,11 for 2.440.267,91; each flagged `total_mismatch` in sgt1936, the other printings agree with the row totals); its TOTAUX are computed on the correct figures (r_seed 10.000.000 and r_sulph 91.661,95 off because of the misprinted lines; annulation 91.333,64 off because the 1936 line is printed 22.454.379,58 where sgt1939 and the TOTAUX give 22.545.713,2x, a digit transposition); its TOTAUX of the avances aux filiales (30,00), recouvrements de subsistance (51,00) and hypothécaires (0,30) are off by amounts no line explains (misprinted TOTAUX).

Survey of the whole chapter in every edition: `mutuality_survey.md`.

## Validation

- Checks against printed totals and identities: 509; passed: 478; failed: 31.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.440 (f464) prev 1916: total = sum of the types: cells give 1773251.16, printed 1773251.22 (difference 0.06)
  - sgt1922 p.440 (f464) prev seed: TOTAUX = sum of the lines: cells give 31230180.59, printed 31230180.65 (difference 0.06)
  - sgt1923 p.452 (f954) prev 1916: total = sum of the types: cells give 1773251.16, printed 1773251.22 (difference 0.06)
  - sgt1923 p.452 (f954) prev seed: TOTAUX = sum of the lines + the 1913 line of sgt1922: cells give 50254432.24, printed 50254432.30 (difference 0.06)
  - sgt1925 p.498 (f522) prev 1924: r_total = sum of the types: cells give 2706471.45, printed 3206471.45 (difference 500000.00)
  - sgt1925 p.498 (f522) prev seed: TOTAUX = sum of the lines: cells give 73938723.66, printed 73939323.66 (difference 600.00)
  - sgt1925 p.498 (f522) prev subs: TOTAUX = sum of the lines: cells give 22925933.64, printed 23005933.64 (difference 80000.00)
  - sgt1925 p.498 (f522) prev r_total: TOTAUX = sum of the lines: cells give 63891641.86, printed 63391641.86 (difference -500000.00)
  - sgt1928 p.470 (f1022) prev adv: TOTAUX = sum of the lines: cells give 4449077.38, printed 4449077.36 (difference -0.02)
  - sgt1929 p.472 (f500) prev r_total: TOTAUX = sum of the lines: cells give 146925197.45, printed 146926197.45 (difference 1000.00)
  - sgt1930 p.480 (f1036) prev r_adv: TOTAUX = sum of the lines + the 1920 line of sgt1929: cells give 4063222.65, printed 4060222.65 (difference -3000.00)
  - sgt1930 p.480 (f1036) prev r_total: TOTAUX = sum of the lines + the 1920 line of sgt1929: cells give 154402074.23, printed 164402074.23 (difference 10000000.00)
  - sgt1935 p.296 (f316) prev 1934: r_total = sum of the types: cells give 10537603.16, printed 10537603.17 (difference 0.01)
  - sgt1935 p.296 (f316) prev total: TOTAUX = sum of the lines: cells give 234810485.81, printed 234810485.84 (difference 0.03)
  - sgt1935 p.296 (f316) prev r_subs: TOTAUX = sum of the lines: cells give 8174602.59, printed 8174602.60 (difference 0.01)
  - sgt1936 p.174 (f185) prev 1927: r_total = sum of the types: cells give 4223002.07, printed 4131340.12 (difference -91661.95)
  - sgt1936 p.174 (f185) prev 1928: r_total = sum of the types: cells give 33504741.66, printed 31504741.66 (difference -2000000.00)
  - sgt1936 p.174 (f185) prev 1929: r_total = sum of the types: cells give 24807247.63, printed 24476247.63 (difference -331000.00)
  - sgt1936 p.174 (f185) prev 1932: total = sum of the types: cells give 32738152.54, printed 32738151.54 (difference -1.00)
  - sgt1936 p.174 (f185) prev 1932: r_total = sum of the types: cells give 12883705.26, printed 21883704.42 (difference 8999999.16)
  - sgt1936 p.174 (f185) prev 1934: total = sum of the types: cells give 35765288.31, printed 32765588.31 (difference -2999700.00)
  - sgt1936 p.174 (f185) prev 1934: r_total = sum of the types: cells give 10537603.16, printed 10527603.16 (difference -10000.00)
  - sgt1936 p.174 (f185) prev 1935: total = sum of the types: cells give 10980031.31, printed 10980031.30 (difference -0.01)
  - sgt1936 p.174 (f185) prev 1936: r_total = sum of the types: cells give 5387759.70, printed 5387760.50 (difference 0.80)
  - sgt1936 p.174 (f185) prev adv: TOTAUX = sum of the lines: cells give 4227758.29, printed 4227728.29 (difference -30.00)
  - sgt1936 p.174 (f185) prev cancel: TOTAUX = sum of the lines: cells give 34169045.94, printed 34260379.58 (difference 91333.64)
  - sgt1936 p.174 (f185) prev r_seed: TOTAUX = sum of the lines: cells give 119710186.66, printed 129710186.66 (difference 10000000.00)
  - sgt1936 p.174 (f185) prev r_sulph: TOTAUX = sum of the lines: cells give 97010.45, printed 5348.50 (difference -91661.95)
  - sgt1936 p.174 (f185) prev r_camp: TOTAUX = sum of the lines: cells give 1018771.64, printed 1018770.80 (difference -0.84)
  - sgt1936 p.174 (f185) prev r_subs: TOTAUX = sum of the lines: cells give 5703276.70, printed 5703327.70 (difference 51.00)
  - sgt1936 p.174 (f185) prev r_mort: TOTAUX = sum of the lines: cells give 4138729.35, printed 4138729.65 (difference 0.30)

- Overlapping printings: 1273 cell comparisons with other editions printing the same cell; 62 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1916 / loans_seed | sgt1922 | 1570483.20 | sgt1925 | 1570483.26 |
| 1916 / loans_seed | sgt1923 | 1570483.20 | sgt1925 | 1570483.26 |
| 1921 / loans_subsistence | sgt1922 | 0 | sgt1930 | 9254466.72 |
| 1921 / loans_subsistence | sgt1923 | 0 | sgt1930 | 9254466.72 |
| 1921 / loans_total | sgt1922 | 15764627.56 | sgt1930 | 25019094.28 |
| 1921 / loans_total | sgt1923 | 15764627.56 | sgt1930 | 25019094.28 |
| 1921 / recoveries_subsistence | sgt1922 | 32807.67 | sgt1930 | 3443662.63 |
| 1921 / recoveries_subsistence | sgt1923 | 32807.67 | sgt1930 | 3443662.63 |
| 1921 / recoveries_total | sgt1922 | 13038261.16 | sgt1930 | 16449116.12 |
| 1921 / recoveries_total | sgt1923 | 13038261.16 | sgt1930 | 16449116.12 |
| 1921 / loans_outstanding | sgt1922 | 2726366.40 | sgt1924 | 8569978.16 |
| 1921 / loans_outstanding | sgt1923 | 2726366.40 | sgt1924 | 8569978.16 |
| 1922 / loans_cancelled | sgt1922 | 10676 | sgt1930 | 347533.40 |
| 1922 / loans_cancelled | sgt1923 | 10676 | sgt1930 | 347533.40 |
| 1922 / recoveries_subsistence | sgt1922 | 5442.73 | sgt1930 | 966407.78 |
| 1922 / recoveries_subsistence | sgt1923 | 5442.73 | sgt1930 | 966407.78 |
| 1922 / recoveries_total | sgt1922 | 2802397.40 | sgt1930 | 3763362.45 |
| 1922 / recoveries_total | sgt1923 | 2802397.40 | sgt1930 | 3763362.45 |
| 1922 / loans_outstanding | sgt1922 | 1853065.83 | sgt1924 | 555243.38 |
| 1922 / loans_outstanding | sgt1923 | 1853065.83 | sgt1924 | 555243.38 |
| 1923 / loans_subsistence | sgt1923 | 0 | sgt1930 | 6584987.05 |
| 1923 / loans_total | sgt1923 | 23146171.49 | sgt1930 | 29731158.54 |
| 1923 / loans_cancelled | sgt1923 | 0 | sgt1930 | 144841.13 |
| 1923 / recoveries_subsistence | sgt1923 | 2402.27 | sgt1930 | 2492970.87 |
| 1923 / recoveries_total | sgt1923 | 16978137.50 | sgt1930 | 19468706.10 |
| 1923 / loans_outstanding | sgt1923 | 6168033.99 | sgt1924 | 10117611.31 |
| 1924 / recoveries_seed | sgt1924 | 1427025.51 | sgt1930 | 1748821.05 |
| 1924 / recoveries_total | sgt1924 | 2384675.91 | sgt1930 | 2706471.45 |
| 1924 / recoveries_total | sgt1925 | 3206471.45 | sgt1930 | 2706471.45 |
| 1928 / loans_seed | sgt1928 | 44240438.47 | sgt1936 |  |
| 1928 / loans_seed | sgt1929 | 44240438.47 | sgt1936 |  |
| 1928 / loans_seed | sgt1930 | 44240438.47 | sgt1936 |  |
| 1928 / loans_seed | sgt1935 | 44240438.47 | sgt1936 |  |
| 1928 / recoveries_seed | sgt1928 | 32012273.27 | sgt1936 | 31012273.27 |
| 1928 / recoveries_seed | sgt1929 | 32012273.27 | sgt1936 | 31012273.27 |
| 1928 / recoveries_seed | sgt1930 | 32012273.27 | sgt1936 | 31012273.27 |
| 1928 / recoveries_seed | sgt1935 | 32012273.27 | sgt1936 | 31012273.27 |
| 1928 / recoveries_total | sgt1928 | 34504741.66 | sgt1936 | 31504741.66 |
| 1928 / recoveries_total | sgt1929 | 34504741.66 | sgt1936 | 31504741.66 |
| 1928 / recoveries_total | sgt1930 | 34504741.66 | sgt1936 | 31504741.66 |
| 1928 / recoveries_total | sgt1935 | 34504741.66 | sgt1936 | 31504741.66 |
| 1929 / recoveries_seed | sgt1929 | 21173131.19 | sgt1936 | 21173131.91 |
| 1929 / recoveries_seed | sgt1930 | 21173131.19 | sgt1936 | 21173131.91 |
| 1929 / recoveries_subsistence | sgt1929 | 2127896.06 | sgt1936 | 2127895.34 |
| 1929 / recoveries_subsistence | sgt1930 | 2127896.06 | sgt1936 | 2127895.34 |
| 1929 / recoveries_total | sgt1929 | 24807247.63 | sgt1936 | 24476247.63 |
| 1929 / recoveries_total | sgt1930 | 24807247.63 | sgt1936 | 24476247.63 |
| 1929 / recoveries_total | sgt1935 | 24807247.63 | sgt1936 | 24476247.63 |
| 1930 / loans_total | sgt1936 |  | sgt1939 | 11352233.56 |
| 1931 / recoveries_total | sgt1936 |  | sgt1939 | 11999494.06 |
| 1932 / loans_total | sgt1936 | 32738151.54 | sgt1939 | 32738152.54 |
| 1932 / recoveries_seed | sgt1936 | 10788203.75 | sgt1939 | 19788203.75 |
| 1932 / recoveries_campaign | sgt1936 | 19683.95 | sgt1939 | 19683.11 |
| 1933 / loans_total | sgt1936 |  | sgt1939 | 6701208.26 |
| 1933 / recoveries_pledge | sgt1936 |  | sgt1939 | 82662 |
| 1933 / recoveries_advances_branches | sgt1936 |  | sgt1939 | 465618.88 |
| 1934 / loans_total | sgt1936 | 32765588.31 | sgt1939 | 35765288.31 |
| 1934 / recoveries_total | sgt1935 | 10537603.17 | sgt1939 | 10537603.16 |
| 1934 / recoveries_total | sgt1936 | 10527603.16 | sgt1939 | 10537603.16 |
| 1935 / loans_total | sgt1936 | 10980031.30 | sgt1939 | 10980031.31 |
| 1936 / loans_cancelled | sgt1936 | 22454379.58 | sgt1939 | 22545713.26 |
| 1936 / recoveries_pledge | sgt1936 | 2440267.11 | sgt1939 | 2440267.91 |

- Flagged cells: derived_from_totals: 1, reprint_corrected: 4, total_mismatch: 1.

  - sgt1936 p.174 1927 recoveries_sulphur_copper_sulphate / francs = 91661.95 (total_mismatch)
  - sgt1935 p.296 1928 loans_seed / francs = 44240438.47 (reprint_corrected)
  - sgt1935 p.296 1928 recoveries_seed / francs = 32012273.27 (reprint_corrected)
  - sgt1935 p.296 1928 recoveries_total / francs = 34504741.66 (reprint_corrected)
  - sgt1935 p.296 1929 recoveries_total / francs = 24807247.63 (reprint_corrected)
  - sgt1939 p.154 1936 loans_cancelled / francs = 22545713.26 (derived_from_totals)

## Image versus OCR

- Read cell by cell on the page images (12 printings): sgt1922 f464, sgt1923 f954, sgt1924 f1452, sgt1925 f522, sgt1926 f1030, sgt1927 f494, sgt1928 f1022, sgt1929 f500, sgt1930 f1036, sgt1935 f316, sgt1936 f185, sgt1939 f160.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
