# Hôpitaux, annexes et infirmeries-dispensaires de l'intérieur : malades et décès

*Hospitals and dispensaries of the interior: beds, patients, patient-days, deaths, consultations.*

Source: *Statistique générale de la Tunisie*, chapter III (health), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1922 (`bpt6k9105649x`): p. 54, f78; sgt1923 (`bpt6k9105649x`): p. 60, f562; sgt1924 (`bpt6k9105649x`): p. 63, f1053; sgt1925 (`bpt6k9105650k`): p. 63, f87; sgt1926 (`bpt6k9105650k`): p. 72, f636; sgt1927 (`bpt6k91056510`): p. 70, f98; sgt1928 (`bpt6k91056510`): p. 70, f622; sgt1929 (`bpt6k9105652d`): p. 72, f100; sgt1930 (`bpt6k9105652d`): p. 76, f634; sgt1935 (`bpt6k9105653t`): p. 48, f68; sgt1936 (`bpt6k91056547`): p. 37, f48; sgt1939 (`bpt6k9105739w`): p. 38, f44.

Transcriptions: `../transcribed/health_pop_<edition>.txt`, section `@interior`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_population.py build`. Per-check output: `health_validation.json`.

Rows: 4171. Years: 1922–1939 (12 years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939).

Printed once per edition, for the edition's own year; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to
- `hospital`: hospital or infirmary-dispensary, as printed
- `measure`: what is counted (see below)
- `population`: `european`, `indigenous`, or `all` (column not split)
- `sex_age`: `male` (Hommes), `female` (Femmes), `child` (Enfants), `total` (only where the parts are not printed)
- `column_fr`: column heading (French)
- `value`: count (integer), except where the notes say otherwise; printed » = 0
- `flag`: empty, or `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (row totals, TOTAUX lines, nationality brackets) and the printed "différence en plus / en moins" columns are not stored; they were used for validation.

"Renseignements généraux" of the hospitals and infirmaries-dispensaries of the interior (and from sgt1936 the regional hospital of Sfax; sgt1939 also lists the Hôpital civil français, Sadiki, Ernest-Conseil and Manouba hospitals of Tunis and the Sfax regional hospital, kept as printed). Columns stored: Nombre de lits (`beds`), Malades hospitalisés européens / indigènes by men, women, children (`patients`), Nombre de journées d'hospitalisation (`patient_days`), Décès européens / indigènes by men, women, children (`deaths`), Nombre de consultations (`consultations`; not printed in sgt1927–sgt1930). The financial column (Prix de la journée) is not extracted; the Total columns and TOTAL row are not stored. Hospital names as printed (Kef (Le) / Le Kef, Mactar / Maktar, Médenine et annexes, Menzel-Temime …).

Printed » = 0; cells printed 0 (sgt1936) are 0. sgt1935 prints no TOTAL row; its Médenine patient days are printed 2.294,5. sgt1936: the Médenine indigenous-deaths total is blank (the 80 printed between Médenine and Sfax belongs to Sfax). In sgt1939 the Tunis hospital rows repeat figures of the hospital tables (e.g. Sadiki 1.532 / 1.953 / 606 = its 1939 admissions). Footnote (sgt1939): the 520 beds of the Hôpital civil français, printed "(a) 520", exclude (a) the 280 beds for soldiers.

The 90 failed checks are listed below. Every page was re-read on the image; the inconsistencies are in the print. They are concentrated in sgt1923 (TOTAL row whose men + women + children do not match its own totals), sgt1928, sgt1929 and above all sgt1936, whose table is visibly garbled (e.g. Sousse Europeans printed » » » 349, Monastir 69 / 199 / 81 / 8, Tabarka indigenous men 308 with a total of 0, consultations summing to 495.367 against 627.741). Cells are stored as printed and not flagged, because the faulty cell cannot be identified.

## Validation

- Checks against printed totals: 1384; passed: 1294; failed: 90.

Failed checks (printed values kept; every one was re-read on the page image and the printed figures are as transcribed; see the commentary above for the cells involved):

  - sgt1922 interior column beds: rows vs TOTAL: cells give 435, printed 438
  - sgt1922 interior column patient_days: rows vs TOTAL: cells give 68184, printed 65884
  - sgt1923 interior Béja eur: m+f+c vs total: cells give 68, printed 62
  - sgt1923 interior Tozeur eur: m+f+c vs total: cells give 6, printed 4
  - sgt1923 interior TOTAL eur: m+f+c vs total: cells give 532, printed 472
  - sgt1923 interior TOTAL ind: m+f+c vs total: cells give 3751, printed 3444
  - sgt1923 interior TOTAL din: m+f+c vs total: cells give 207, printed 195
  - sgt1923 interior column beds: rows vs TOTAL: cells give 494, printed 457
  - sgt1923 interior column eur_f: rows vs TOTAL: cells give 215, printed 275
  - sgt1923 interior column eur_c: rows vs TOTAL: cells give 76, printed 73
  - sgt1923 interior column eur_t: rows vs TOTAL: cells give 467, printed 472
  - sgt1923 interior column ind_m: rows vs TOTAL: cells give 2291, printed 2331
  - sgt1923 interior column ind_f: rows vs TOTAL: cells give 792, printed 1009
  - sgt1923 interior column ind_t: rows vs TOTAL: cells give 3494, printed 3444
  - sgt1923 interior column patient_days: rows vs TOTAL: cells give 78465, printed 77455
  - sgt1923 interior column din_m: rows vs TOTAL: cells give 171, printed 168
  - sgt1923 interior column din_t: rows vs TOTAL: cells give 210, printed 195
  - sgt1923 interior column consultations: rows vs TOTAL: cells give 157634, printed 157594
  - sgt1924 interior column patient_days: rows vs TOTAL: cells give 90099, printed 90100
  - sgt1924 interior column consultations: rows vs TOTAL: cells give 144642, printed 143742
  - sgt1926 interior column patient_days: rows vs TOTAL: cells give 105279, printed 105289
  - sgt1926 interior column consultations: rows vs TOTAL: cells give 171296, printed 172295
  - sgt1927 interior Kairouan ind: m+f+c vs total: cells give 426, printed 425
  - sgt1927 interior column ind_t: rows vs TOTAL: cells give 5440, printed 5441
  - sgt1928 interior Béja deu: m+f+c vs total: cells give 5, printed 6
  - sgt1928 interior Monastir din: m+f+c vs total: cells give 11, printed 8
  - sgt1928 interior Gabès eur: m+f+c vs total: cells give 5, printed 10
  - sgt1928 interior TOTAL eur: m+f+c vs total: cells give 941, printed 977
  - sgt1928 interior TOTAL ind: m+f+c vs total: cells give 4994, printed 4584
  - sgt1928 interior column beds: rows vs TOTAL: cells give 673, printed 732
  - sgt1928 interior column eur_f: rows vs TOTAL: cells give 479, printed 448
  - sgt1928 interior column ind_m: rows vs TOTAL: cells give 3141, printed 3151
  - sgt1928 interior column ind_t: rows vs TOTAL: cells give 4984, printed 4584
  - sgt1928 interior column patient_days: rows vs TOTAL: cells give 107355, printed 107385
  - sgt1928 interior column deu_f: rows vs TOTAL: cells give 25, printed 26
  - sgt1928 interior column din_c: rows vs TOTAL: cells give 22, printed 19
  - sgt1929 interior Béja ind: m+f+c vs total: cells give 459, printed 479
  - sgt1929 interior TOTAL eur: m+f+c vs total: cells give 948, printed 1160
  - sgt1929 interior column eur_t: rows vs TOTAL: cells give 948, printed 1160
  - sgt1929 interior column ind_f: rows vs TOTAL: cells give 1326, printed 1226
  - sgt1929 interior column ind_t: rows vs TOTAL: cells give 5277, printed 5157
  - sgt1930 interior Téboursouk ind: m+f+c vs total: cells give 41, printed 40
  - sgt1930 interior Grombalia ind: m+f+c vs total: cells give 167, printed 171
  - sgt1930 interior Maktar ind: m+f+c vs total: cells give 103, printed 106
  - sgt1930 interior Sousse ind: m+f+c vs total: cells give 750, printed 734
  - sgt1930 interior Monastir eur: m+f+c vs total: cells give 6, printed 0
  - sgt1930 interior TOTAL deu: m+f+c vs total: cells give 41, printed 40
  - sgt1930 interior column eur_t: rows vs TOTAL: cells give 868, printed 874
  - sgt1930 interior column ind_t: rows vs TOTAL: cells give 5068, printed 5078
  - sgt1930 interior column deu_t: rows vs TOTAL: cells give 41, printed 40
  - sgt1935 interior Souk-el-Khémis din: m+f+c vs total: cells give 26, printed 20
  - sgt1935 interior Nabeul ind: m+f+c vs total: cells give 252, printed 257
  - sgt1935 interior Maktar ind: m+f+c vs total: cells give 138, printed 139
  - sgt1935 interior Téboursouk din: m+f+c vs total: cells give 4, printed 9
  - sgt1935 interior Djerba ind: m+f+c vs total: cells give 160, printed 100
  - sgt1936 interior Bizerte din: m+f+c vs total: cells give 8, printed 9
  - sgt1936 interior Souk-el-Khemis ind: m+f+c vs total: cells give 360, printed 668
  - sgt1936 interior Tabarka ind: m+f+c vs total: cells give 308, printed 0
  - sgt1936 interior Tébourba din: m+f+c vs total: cells give 1, printed 0
  - sgt1936 interior Zaghouan deu: m+f+c vs total: cells give 1, printed 0
  - sgt1936 interior Maktar ind: m+f+c vs total: cells give 187, printed 197
  - sgt1936 interior Le Kef deu: m+f+c vs total: cells give 1, printed 2
  - sgt1936 interior Téboursouk eur: m+f+c vs total: cells give 0, printed 2
  - sgt1936 interior Enfidaville eur: m+f+c vs total: cells give 62, printed 0
  - sgt1936 interior Enfidaville deu: m+f+c vs total: cells give 2, printed 0
  - sgt1936 interior Kairouan eur: m+f+c vs total: cells give 18, printed 76
  - sgt1936 interior Kairouan deu: m+f+c vs total: cells give 3, printed 4
  - sgt1936 interior Mahdia eur: m+f+c vs total: cells give 3, printed 4
  - sgt1936 interior Mahdia deu: m+f+c vs total: cells give 1, printed 2
  - sgt1936 interior Monastir eur: m+f+c vs total: cells give 349, printed 8
  - sgt1936 interior Monastir ind: m+f+c vs total: cells give 704, printed 699
  - sgt1936 interior Monastir deu: m+f+c vs total: cells give 9, printed 13
  - sgt1936 interior Sousse eur: m+f+c vs total: cells give 0, printed 349
  - sgt1936 interior Sousse ind: m+f+c vs total: cells give 1241, printed 1341
  - sgt1936 interior Sousse deu: m+f+c vs total: cells give 4, printed 0
  - sgt1936 interior Thala eur: m+f+c vs total: cells give 2, printed 0
  - sgt1936 interior Gabès eur: m+f+c vs total: cells give 0, printed 2
  - sgt1936 interior Djerba ind: m+f+c vs total: cells give 76, printed 98
  - sgt1936 interior Gafsa ind: m+f+c vs total: cells give 22, printed 0
  - sgt1936 interior Hôpital Régional de Sfax eur: m+f+c vs total: cells give 396, printed 395
  - sgt1936 interior TOTAL din: m+f+c vs total: cells give 620, printed 588
  - sgt1936 interior column eur_m: rows vs TOTAL: cells give 485, printed 487
  - sgt1936 interior column eur_t: rows vs TOTAL: cells give 1495, printed 1491
  - sgt1936 interior column ind_f: rows vs TOTAL: cells give 2913, printed 2908
  - sgt1936 interior column ind_t: rows vs TOTAL: cells give 10419, printed 10309
  - sgt1936 interior column din_m: rows vs TOTAL: cells give 366, printed 350
  - sgt1936 interior column din_f: rows vs TOTAL: cells give 151, printed 179
  - sgt1936 interior column din_t: rows vs TOTAL: cells give 585, printed 588
  - sgt1936 interior column consultations: rows vs TOTAL: cells give 495367, printed 627741
  - sgt1939 interior column consultations: rows vs TOTAL: cells give 1183091, printed 1183491

- Flagged cells: none.
