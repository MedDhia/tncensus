# Oliviers. Répartition par caïdat (à partir de sgt1925 : par régions)

*Olive trees by caïdat (unproductive and wild, young untaxed, taxed).*

Source: *Statistique générale de la Tunisie*, chapter *Agriculture*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 228, f252; sgt1923 (`bpt6k9105649x`): p. 240, f742; sgt1924 (`bpt6k9105649x`): p. 254, f1244; sgt1925 (`bpt6k9105650k`): p. 282, f306; sgt1926 (`bpt6k9105650k`): p. 252, f816; sgt1927 (`bpt6k91056510`): p. 245, f273; sgt1928 (`bpt6k91056510`): p. 245, f797; sgt1929 (`bpt6k9105652d`): p. 247, f275; sgt1930 (`bpt6k9105652d`): p. 251, f809; sgt1935 (`bpt6k9105653t`): p. 129, f149; sgt1936 (`bpt6k91056547`): p. 99, f110; sgt1939 (`bpt6k9105739w`): p. 103, f109.

Transcriptions: `../transcribed/agriculture_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_agriculture.py build`.

Rows: 1234. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939.

Units: trees (`unit`); value_type: count.

Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept; `year` = edition year.

## Columns

- `census`: edition the value is taken from (rule 4 series: the latest edition printing that year; rule 5 tables: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: edition year (the table gives the trees counted for the canoun olive tax; no date printed)
- `region`: région as printed (from sgt1925), or "Territoires Militaires du Sud"; empty in sgt1922-sgt1924
- `chef_lieu`: chef-lieu de région as printed (from sgt1925); empty otherwise
- `controle_civil`: contrôle civil as printed (from sgt1925); empty otherwise
- `caidat`: caïdat as printed; "Cap-Bon > Nabeul" = caïdat printed under the Cap-Bon bracket
- `tree_class`: `unproductive_and_wild` (oliviers improductifs et oléastres), `young_untaxed` (jeunes oliviers non imposés), `taxed` (oliviers imposés); `total` only for a line printed without classes (Djerba)
- `tree_class_fr`: printed column heading
- `measure`: `trees`
- `measure_fr`: printed heading
- `unit`: `trees`
- `value`: printed value (» = 0)
- `flag`: empty, or `not_applicable` (Non recensés), `derived_from_totals`, `total_mismatch`

Printed in every edition. sgt1922-sgt1924: 30 caïdats numbered in a fixed order (Soliman and Nabeul bracketed as Cap-Bon). From sgt1925 the caïdats are grouped by région, chef-lieu and contrôle civil, with the Territoires Militaires du Sud; Aïn-Draham is printed "Non recensés" (stored NA, `not_applicable`); Djerba is printed with a total only (footnote: not subject to the canoun, not counted by category; its total is stored with `tree_class` = `total`). The line totals (TOTAL) and the TOTAUX line are checks only, except Djerba's total.

Caïdat names as printed in each edition (Ouled-Ayar / Oulad Ayar, Fraichiche / Fraichiches, Majeur / Majeurs, Banlieue / Banlieue de Tunis). sgt1925-sgt1926 print Nabeul above Soliman under Cap-Bon, with the figures that sgt1922-sgt1924 print for Soliman: kept as printed (the names may be interchanged).

sgt1935 and sgt1936 print the same figures in every cell (both printings read independently); sgt1939 adds the caïdat Djemmal (its bracket is ambiguous between the Sousse and Kairouan contrôles: stored under Sousse) and drops La Skhira and Djerba. Rule 5: each edition kept.

Every failed check below was re-read on a zoomed native-resolution crop: they are printed inconsistencies (printed values kept). Checks: classes vs each line's TOTAL, every column vs TOTAUX (Djerba's total-only line added to the TOTAUX check). Flagged `total_mismatch` where one class explains both the line and the column check (e.g. sgt1927 Sousse jeunes oliviers 122.974 for 622.974, Mahdia imposés 941.943 for 971.943; sgt1929 Mahdia jeunes 558.347 for 588.347). Other failures are misprinted line totals (sgt1923 Banlieue 224.443 for 924.443; sgt1924 Medjez-el-Bab 15.710 for 55.710; sgt1928 Souk-el-Khemis 2.193, Zaghouan 39.538), differences of a few units, or misprinted TOTAUX; sgt1923 Kef improductifs printed with a broken digit is solved from the column TOTAUX (19.873, `derived_from_totals`). The failures of sgt1935 recur identically in sgt1936.

Survey of the whole chapter in every edition: `agriculture_survey.md`.

## Validation

- Checks against printed totals and identities: 462; passed: 398; failed: 64.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.228 (f252) olive Djelass: classes vs total: cells give 412716, printed 412720 (difference 4)
  - sgt1922 p.228 (f252) olive Hammama: classes vs total: cells give 32457, printed 34457 (difference 2000)
  - sgt1922 p.228 (f252) olive TOTAUX: classes vs total: cells give 15109295, printed 15109296 (difference 1)
  - sgt1922 p.228 (f252) olive taxed: lines vs TOTAUX: cells give 9094188, printed 9094191 (difference 3)
  - sgt1922 p.228 (f252) olive total: lines vs TOTAUX: cells give 15111296, printed 15109296 (difference -2000)
  - sgt1923 p.240 (f742) olive Skhira (La): classes vs total: cells give 124403, printed 124423 (difference 20)
  - sgt1923 p.240 (f742) olive Cap-Bon > Soliman: classes vs total: cells give 1273452, printed 1273492 (difference 40)
  - sgt1923 p.240 (f742) olive Banlieue: classes vs total: cells give 924443, printed 224443 (difference -700000)
  - sgt1923 p.240 (f742) olive Kef: classes vs total: cells give 59359, printed 53359 (difference -6000)
  - sgt1923 p.240 (f742) olive Hammama: classes vs total: cells give 91635, printed 94635 (difference 3000)
  - sgt1923 p.240 (f742) olive unprod: lines vs TOTAUX: cells give 722867, printed 722887 (difference 20)
  - sgt1923 p.240 (f742) olive young: lines vs TOTAUX: cells give 5493628, printed 5493648 (difference 20)
  - sgt1923 p.240 (f742) olive total: lines vs TOTAUX: cells give 14557057, printed 15260037 (difference 702980)
  - sgt1924 p.254 (f1244) olive Medjez-el-Bab: classes vs total: cells give 55710, printed 15710 (difference -40000)
  - sgt1924 p.254 (f1244) olive Ouled-Aoun: classes vs total: cells give 48058, printed 51058 (difference 3000)
  - sgt1924 p.254 (f1244) olive unprod: lines vs TOTAUX: cells give 711312, printed 714312 (difference 3000)
  - sgt1924 p.254 (f1244) olive total: lines vs TOTAUX: cells give 15614347, printed 15654347 (difference 40000)
  - sgt1925 p.282 (f306) olive 3me Région / Le Kef / Maktar / Oulad Aoun: classes vs total: cells give 51058, printed 51088 (difference 30)
  - sgt1925 p.282 (f306) olive total: lines vs TOTAUX: cells give 16060067, printed 16060037 (difference -30)
  - sgt1927 p.245 (f273) olive 3me Région / Le Kef / Maktar / Oulad Ayar: classes vs total: cells give 48312, printed 48342 (difference 30)
  - sgt1927 p.245 (f273) olive 4me Région / Sousse / Sousse / Mahdia: classes vs total: cells give 1589078, printed 1619078 (difference 30000)
  - sgt1927 p.245 (f273) olive 4me Région / Sousse / Sousse / Sousse: classes vs total: cells give 1632627, printed 2132627 (difference 500000)
  - sgt1927 p.245 (f273) olive 5me Région / Sfax / Tozeur / Djerid: classes vs total: cells give 36011, printed 36081 (difference 70)
  - sgt1927 p.245 (f273) olive taxed: lines vs TOTAUX: cells give 10181157, printed 10211257 (difference 30100)
  - sgt1928 p.245 (f797) olive 1re Région / Bizerte / Bizerte / Mateur: classes vs total: cells give 140147, printed 142147 (difference 2000)
  - sgt1928 p.245 (f797) olive 1re Région / Bizerte / Souk-el-Arba / Souk-el-Arba: classes vs total: cells give 95113, printed 95023 (difference -90)
  - sgt1928 p.245 (f797) olive 1re Région / Bizerte / Souk-el-Arba / Souk-el-Khemis: classes vs total: cells give 8193, printed 2193 (difference -6000)
  - sgt1928 p.245 (f797) olive 2me Région / Tunis / Zaghouan / Zaghouan: classes vs total: cells give 99538, printed 39538 (difference -60000)
  - sgt1928 p.245 (f797) olive 3me Région / Le Kef / Téboursouk / Téboursouk: classes vs total: cells give 64261, printed 65261 (difference 1000)
  - sgt1928 p.245 (f797) olive 3me Région / Le Kef / Maktar / Oulad Ayar: classes vs total: cells give 48293, printed 48323 (difference 30)
  - sgt1928 p.245 (f797) olive TOTAUX: classes vs total: cells give 16317913, printed 16317983 (difference 70)
  - sgt1928 p.245 (f797) olive unprod: lines vs TOTAUX: cells give 766376, printed 766276 (difference -100)
  - sgt1928 p.245 (f797) olive young: lines vs TOTAUX: cells give 5340866, printed 5342866 (difference 2000)
  - sgt1928 p.245 (f797) olive taxed: lines vs TOTAUX: cells give 10207731, printed 10208771 (difference 1040)
  - sgt1928 p.245 (f797) olive total: lines vs TOTAUX: cells give 16251913, printed 16317983 (difference 66070)
  - sgt1929 p.247 (f275) olive 2me Région / Tunis / Grombalia / Cap-Bon > Nabeul: classes vs total: cells give 559611, printed 556611 (difference -3000)
  - sgt1929 p.247 (f275) olive 4me Région / Sousse / Sousse / Mahdia: classes vs total: cells give 1588529, printed 1618529 (difference 30000)
  - sgt1929 p.247 (f275) olive 4me Région / Sousse / Kairouan / Djelass: classes vs total: cells give 413023, printed 414023 (difference 1000)
  - sgt1929 p.247 (f275) olive 5me Région / Sfax / Sfax / Djebéniane: classes vs total: cells give 1147624, printed 1147574 (difference -50)
  - sgt1929 p.247 (f275) olive 5me Région / Sfax / Gafsa / Hammama: classes vs total: cells give 96012, printed 95612 (difference -400)
  - sgt1929 p.247 (f275) olive unprod: lines vs TOTAUX: cells give 769583, printed 769533 (difference -50)
  - sgt1929 p.247 (f275) olive young: lines vs TOTAUX: cells give 5162887, printed 5193490 (difference 30603)
  - sgt1929 p.247 (f275) olive taxed: lines vs TOTAUX: cells give 10408130, printed 10405130 (difference -3000)
  - sgt1929 p.247 (f275) olive total: lines vs TOTAUX: cells give 16368150, printed 16368153 (difference 3)
  - sgt1930 p.251 (f809) olive 1re Région / Bizerte / Bizerte / Bizerte: classes vs total: cells give 465179, printed 466179 (difference 1000)
  - sgt1930 p.251 (f809) olive Territoires Militaires du Sud /  /  / Ouerghemma: classes vs total: cells give 563950, printed 565950 (difference 2000)
  - sgt1930 p.251 (f809) olive taxed: lines vs TOTAUX: cells give 10391114, printed 10392114 (difference 1000)
  - sgt1930 p.251 (f809) olive total: lines vs TOTAUX: cells give 16371690, printed 16369690 (difference -2000)
  - sgt1935 p.129 (f149) olive 2me Région / Tunis / Grombalia / Cap-Bon > Soliman: classes vs total: cells give 1260856, printed 1261856 (difference 1000)
  - sgt1935 p.129 (f149) olive 4me Région / Sousse / Sousse / Mahdia: classes vs total: cells give 1627854, printed 1627863 (difference 9)
  - sgt1935 p.129 (f149) olive 4me Région / Sousse / Sousse / Monastir: classes vs total: cells give 2313883, printed 2313885 (difference 2)
  - sgt1935 p.129 (f149) olive 4me Région / Sousse / Thala / Sbeitla: classes vs total: cells give 32636, printed 32736 (difference 100)
  - sgt1935 p.129 (f149) olive 5me Région / Sfax / Gafsa / Hammama: classes vs total: cells give 115210, printed 115130 (difference -80)
  - sgt1935 p.129 (f149) olive young: lines vs TOTAUX: cells give 4808197, printed 4808217 (difference 20)
  - sgt1935 p.129 (f149) olive taxed: lines vs TOTAUX: cells give 11580992, printed 11581001 (difference 9)
  - sgt1935 p.129 (f149) olive total: lines vs TOTAUX: cells give 17145423, printed 17144421 (difference -1002)
  - sgt1936 p.99 (f110) olive 2me Région / Tunis / Grombalia / Cap-Bon > Soliman: classes vs total: cells give 1260856, printed 1261856 (difference 1000)
  - sgt1936 p.99 (f110) olive 4me Région / Sousse / Sousse / Mahdia: classes vs total: cells give 1627854, printed 1627863 (difference 9)
  - sgt1936 p.99 (f110) olive 4me Région / Sousse / Sousse / Monastir: classes vs total: cells give 2313883, printed 2313885 (difference 2)
  - sgt1936 p.99 (f110) olive 4me Région / Sousse / Thala / Sbeitla: classes vs total: cells give 32636, printed 32736 (difference 100)
  - sgt1936 p.99 (f110) olive 5me Région / Sfax / Gafsa / Hammama: classes vs total: cells give 115210, printed 115130 (difference -80)
  - sgt1936 p.99 (f110) olive young: lines vs TOTAUX: cells give 4808197, printed 4808217 (difference 20)
  - sgt1936 p.99 (f110) olive taxed: lines vs TOTAUX: cells give 11580992, printed 11581001 (difference 9)
  - sgt1936 p.99 (f110) olive total: lines vs TOTAUX: cells give 17145423, printed 17144421 (difference -1002)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: derived_from_totals: 1, not_applicable: 20, total_mismatch: 17.

  - sgt1923 p.240 1923  /  /  / Skhira (La) / unproductive_and_wild / trees / trees = 54 (total_mismatch)
  - sgt1923 p.240 1923  /  /  / Kef / unproductive_and_wild / trees / trees = 19873 (derived_from_totals)
  - sgt1924 p.254 1924  /  /  / Ouled-Aoun / unproductive_and_wild / trees / trees = 15581 (total_mismatch)
  - sgt1925 p.282 1925 1re Région / Bizerte / Tabarka / Aïn-Draham / unproductive_and_wild / trees / trees = NA (not_applicable)
  - sgt1925 p.282 1925 1re Région / Bizerte / Tabarka / Aïn-Draham / young_untaxed / trees / trees = NA (not_applicable)
  - sgt1925 p.282 1925 1re Région / Bizerte / Tabarka / Aïn-Draham / taxed / trees / trees = NA (not_applicable)
  - sgt1925 p.282 1925 1re Région / Bizerte / Tabarka / Aïn-Draham / total / trees / trees = NA (not_applicable)
  - sgt1926 p.252 1926 1re Région / Bizerte / Tabarka / Aïn-Draham / unproductive_and_wild / trees / trees = NA (not_applicable)
  - sgt1926 p.252 1926 1re Région / Bizerte / Tabarka / Aïn-Draham / young_untaxed / trees / trees = NA (not_applicable)
  - sgt1926 p.252 1926 1re Région / Bizerte / Tabarka / Aïn-Draham / taxed / trees / trees = NA (not_applicable)
  - sgt1926 p.252 1926 1re Région / Bizerte / Tabarka / Aïn-Draham / total / trees / trees = NA (not_applicable)
  - sgt1927 p.245 1927 1re Région / Bizerte / Tabarka / Aïn-Draham / unproductive_and_wild / trees / trees = NA (not_applicable)
  - sgt1927 p.245 1927 1re Région / Bizerte / Tabarka / Aïn-Draham / young_untaxed / trees / trees = NA (not_applicable)
  - sgt1927 p.245 1927 1re Région / Bizerte / Tabarka / Aïn-Draham / taxed / trees / trees = NA (not_applicable)
  - sgt1927 p.245 1927 1re Région / Bizerte / Tabarka / Aïn-Draham / total / trees / trees = NA (not_applicable)
  - sgt1927 p.245 1927 3me Région / Le Kef / Maktar / Oulad Ayar / taxed / trees / trees = 33633 (total_mismatch)
  - sgt1927 p.245 1927 4me Région / Sousse / Sousse / Mahdia / taxed / trees / trees = 941943 (total_mismatch)
  - sgt1927 p.245 1927 4me Région / Sousse / Sousse / Sousse / young_untaxed / trees / trees = 122974 (total_mismatch)
  - sgt1927 p.245 1927 5me Région / Sfax / Tozeur / Djerid / taxed / trees / trees = 21411 (total_mismatch)
  - sgt1927 p.245 1927 Territoires Militaires du Sud /  /  / Matmata / unproductive_and_wild / trees / trees = NA (not_applicable)
  - sgt1927 p.245 1927 Territoires Militaires du Sud /  /  / Matmata / young_untaxed / trees / trees = NA (not_applicable)
  - sgt1927 p.245 1927 Territoires Militaires du Sud /  /  / Matmata / taxed / trees / trees = NA (not_applicable)
  - sgt1927 p.245 1927 Territoires Militaires du Sud /  /  / Matmata / total / trees / trees = NA (not_applicable)
  - sgt1928 p.245 1928 1re Région / Bizerte / Bizerte / Mateur / young_untaxed / trees / trees = 16224 (total_mismatch)
  - sgt1928 p.245 1928 1re Région / Bizerte / Tabarka / Aïn-Draham / unproductive_and_wild / trees / trees = NA (not_applicable)
  - sgt1928 p.245 1928 1re Région / Bizerte / Tabarka / Aïn-Draham / young_untaxed / trees / trees = NA (not_applicable)
  - sgt1928 p.245 1928 1re Région / Bizerte / Tabarka / Aïn-Draham / taxed / trees / trees = NA (not_applicable)
  - sgt1928 p.245 1928 1re Région / Bizerte / Tabarka / Aïn-Draham / total / trees / trees = NA (not_applicable)
  - sgt1928 p.245 1928 1re Région / Bizerte / Souk-el-Arba / Souk-el-Arba / unproductive_and_wild / trees / trees = 47803 (total_mismatch)
  - sgt1928 p.245 1928 1re Région / Bizerte / Souk-el-Arba / Souk-el-Arba / taxed / trees / trees = 25112 (total_mismatch)
  - sgt1928 p.245 1928 3me Région / Le Kef / Téboursouk / Téboursouk / taxed / trees / trees = 53795 (total_mismatch)
  - sgt1928 p.245 1928 3me Région / Le Kef / Maktar / Oulad Ayar / taxed / trees / trees = 33633 (total_mismatch)
  - sgt1929 p.247 1929 2me Région / Tunis / Grombalia / Cap-Bon > Nabeul / taxed / trees / trees = 407751 (total_mismatch)
  - sgt1929 p.247 1929 4me Région / Sousse / Sousse / Mahdia / young_untaxed / trees / trees = 558347 (total_mismatch)
  - sgt1929 p.247 1929 4me Région / Sousse / Kairouan / Djelass / young_untaxed / trees / trees = 206347 (total_mismatch)
  - sgt1929 p.247 1929 5me Région / Sfax / Sfax / Djebéniane / unproductive_and_wild / trees / trees = 19692 (total_mismatch)
  - sgt1929 p.247 1929 5me Région / Sfax / Gafsa / Hammama / young_untaxed / trees / trees = 85990 (total_mismatch)
  - sgt1930 p.251 1930 1re Région / Bizerte / Bizerte / Bizerte / taxed / trees / trees = 428234 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (12 printings): sgt1922 f252, sgt1923 f742, sgt1924 f1244, sgt1925 f306, sgt1926 f816, sgt1927 f273, sgt1928 f797, sgt1929 f275, sgt1930 f809, sgt1935 f149, sgt1936 f110, sgt1939 f109.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
