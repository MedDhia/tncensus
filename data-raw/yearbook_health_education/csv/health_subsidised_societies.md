# Situation des sociétés et œuvres subventionnées sur le budget de l'Assistance publique

*Accounts of the societies and charities subsidised by public assistance: receipts, expenditure, cash balance and people assisted (sgt1922–sgt1930).*

Source: *Statistique générale de la Tunisie*, chapter III (health and assistance), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / BnF.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 46, f70, p. 47, f71; sgt1923 (`bpt6k9105649x`): p. 52, f554, p. 53, f555; sgt1924 (`bpt6k9105649x`): p. 54, f1044, p. 55, f1045; sgt1925 (`bpt6k9105650k`): p. 54, f78, p. 55, f79; sgt1926 (`bpt6k9105650k`): p. 62, f626, p. 63, f627, p. 64, f628, p. 65, f629; sgt1927 (`bpt6k91056510`): p. 62, f90, p. 63, f91; sgt1928 (`bpt6k91056510`): p. 62, f614, p. 63, f615; sgt1929 (`bpt6k9105652d`): p. 64, f92, p. 65, f93; sgt1930 (`bpt6k9105652d`): p. 68, f626, p. 69, f627.

Transcriptions: `../transcribed/health_finance_<edition>.txt`, sections `[societies]`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_finance.py build`. Per-check output: `health_finance_validation.json`.

Rows: 5208. Years: 1922–1930. Unit of `value`: francs (statistics: counts); amounts are as printed, centimes kept as decimals (printed » = 0).

Printed once per edition; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (for a table over two pages, the page of the column group)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (budget year, account year or calendar year; see below)
- `society_fr`: society / charity name exactly as printed
- `society_en`: English code built from the name
- `group`: column group: `receipts`, `expenditure`, `balance`, `statistics` (`accounts` in the sgt1935 summary)
- `measure`: what the value is (see below)
- `measure_fr`: column heading (French)
- `value`: francs (statistics: counts); empty where the flag says so
- `flag`: empty, or `derived_from_totals`, `total_mismatch`, `not_applicable`, `illegible`, `reprint_corrected` (see below)

"Situation des sociétés et œuvres subventionnées sur le budget de l'Assistance publique" (sgt1922–sgt1930): one row per society as printed (names exactly as printed; sgt1926 prints them as addressees, "M. le Président de la Société …"). `year` = year of the accounts (the edition's year; cash at 1 January of that year, cash remaining at 1 January of the next). Groups and measures: `receipts` (`cash_1_january`, `festivities_and_donations`, `public_assistance_subsidies` = Subventions A. P., `other_subsidies_and_receipts`), `expenditure` (`general_expenses`, `relief_cash_or_kind`, `maintenance_orphans_elderly`, `relief_through_work`, `medical_assistance`, `other_expenses`), `balance` (`cash_remaining_end_of_year`, printed "Reste en caisse au 1er janvier" of the next year), `statistics` (`persons_assisted`, `relief_grants_cash_or_kind`, `persons_medical_assistance`, `repatriations`; sgt1925 adds `meals_distributed`). Money in francs with centimes; statistics are counts. The two printed TOTAL columns, "A reporter" (sgt1926) and TOTAUX are not stored. A dash printed in a cell is not stored. Rows printed with » in every cell (no account returned) are not stored; they are listed below.

The printed tables are internally inconsistent in many places (204 of 1.290 checks fail): row totals that do not add up (often by 0,09–0,90 francs, transposed centimes), balances that are not receipts − expenditure, and in several editions TOTAUX lines that leave out late rows (sgt1925: the Conseil de la Communauté israélite de Tunis, 608.293,32 of receipts in column 4, is not in the TOTAUX; in sgt1924 the TOTAUX of "Frais généraux", 296.057,79, repeats the sgt1923 total). sgt1923 repeats the figures of one society under another name (Cuisines populaires musulmanes = Société musulmane de Tunis; Goutte de lait Lucien Saint de Sfax = Goutte de lait de Sfax); sgt1927 prints the totals of the Cuisines populaires israélites and the Société italienne in each other's row. All are kept as printed. The draft transcription was checked against the page images for every row with a failed check in sgt1922, sgt1924, sgt1927, sgt1928, sgt1929 and sgt1930 and for part of sgt1925 and sgt1926 (row crops at native resolution), and against the Gallica OCR elsewhere; no transcription error was found in those rows (one doubtful sgt1928 cell, Goutte de lait de Thala, Subventions A. P. 1.100, is printed so).

Flagged (`total_mismatch`): balances misprinted where receipts and expenditure both agree with their parts and the next edition's cash at 1 January confirms the computed balance: sgt1926 Société française de Sfax (printed 534,40; 553,40 computed and carried into sgt1927) and de Bizerte (414,90; 14,90), sgt1927 Société musulmane de Kairouan (637; 6.377 computed). Cells marked `derived_from_totals` (sgt1923, cut off in the binding) were solved from the printed row total. sgt1925: "20 familles" (persons assisted, Société française de Kairouan) is stored as 20.

## Remarks recorded in the transcriptions

- sgt1922: groups: receipts (caisse au 1er janvier, fêtes et dons, subventions A.P., subventions et recettes diverses, TOTAL) | expenditure (frais généraux, secours en espèces ou nature, entretien d'orphelins vieillards etc., assistance par le travail, assistance médicale, dépenses diverses, TOTAL) | reste en caisse au 1er janvier suivant | statistics (personnes secourues, secours en espèces, personnes ayant bénéficié de l'assistance médicale, rapatriements) "—" = a dash printed in the cell (no figure given)
- sgt1923: Token suffixes: {d} = derived_from_totals (cell cut off in the binding, solved from the printed row total), "?" = illegible. The rows of this table are printed as listed; several rows repeat another society's figures (see notes).
- sgt1925: Statistics have a fifth column from this edition: "Repas distribués". "{familles}" = printed "20 familles".
- sgt1926: Names are printed as the addressee ("M. le Président de la Société ..."); stored as printed. Printed over two spreads; "A reporter" / "Report" lines are stored as SUBTOTAL lines and checked.
- sgt1928: The right-hand page heads its cash column "Reste en caisse au 1er janvier 1928" (sic; it is the end-of-year balance). Monastir "Nombre de secours en espèces" printed "p. 88"; stored 88.
- sgt1929: Ferryville total expenditure printed "1.275 6", stored 1275.60.
- sgt1930: Amounts are printed in whole francs in this edition. No TOTAUX line is printed. Rows printed without any figure are stored with "-" (not printed) in every cell; the build skips them and lists them in the notes.

## Validation

- Checks against printed totals: 1290; passed: 1086; failed: 204.

Failed checks (printed values kept, unless a flag below says otherwise; `L<n>` = line of the transcription file). See the commentary above for which ones were re-read on the page images and which are repeated identically in several printings:

  - sgt1922 L99 Société de Bienfaisance Française de Tunis: receipts - expenditure vs balance: cells give 7402.14, printed 7402
  - sgt1922 L117 Cantines scolaires: receipts parts vs total: cells give 88274.25, printed 88273.75
  - sgt1922 L125 Goutte de Lait Lucien Saint de Gabès: receipts parts vs total: cells give 5460, printed 3460
  - sgt1922 L131 TOTAUX: expenditure parts vs total: cells give 773592.89, printed 683592.89
  - sgt1922 L131 TOTAUX: receipts - expenditure vs balance: cells give 203072.84, printed 208688.29
  - sgt1922 societies TOTAUX (line 131) group 0 col 0: rows above vs printed: cells give 175758.27, printed 175757.77
  - sgt1922 societies TOTAUX (line 131) group 0 col 1: rows above vs printed: cells give 154204.07, printed 152204.07
  - sgt1922 societies TOTAUX (line 131) group 1 col 0: rows above vs printed: cells give 200243.45, printed 290243.45
  - sgt1922 societies TOTAUX (line 131) group 2 col 0: rows above vs printed: cells give 203638.75, printed 208688.29
  - sgt1922 societies TOTAUX (line 131) group 3 col 1: rows above vs printed: cells give 51085, printed 51075
  - sgt1923 L148 TOTAUX: expenditure parts vs total: cells give 1048516.87, printed 1048546.88
  - sgt1923 L148 TOTAUX: receipts - expenditure vs balance: cells give 294820.62, printed 300970.44
  - sgt1923 societies TOTAUX (line 148) group 1 col 5: rows above vs printed: cells give 103862.66, printed 103862.65
  - sgt1923 societies TOTAUX (line 148) group 1 col 6: rows above vs printed: cells give 1048516.88, printed 1048546.88
  - sgt1923 societies TOTAUX (line 148) group 3 col 1: rows above vs printed: cells give 16979, printed 16939
  - sgt1924 L160 Garderie israélite: receipts parts vs total: cells give 47325.2, printed 47315.2
  - sgt1924 L160 Garderie israélite: receipts - expenditure vs balance: cells give 22449.15, printed 22459.15
  - sgt1924 L161 Cantines populaires israélites: expenditure parts vs total: cells give 60916.97, printed 60946.97
  - sgt1924 L162 Cantines scolaires: receipts parts vs total: cells give 112265.56, printed 112265.55
  - sgt1924 L163 Fourneau des Pauvres: expenditure parts vs total: cells give 77734.55, printed 77634.56
  - sgt1924 L167 Dispensaire Alapetite: expenditure parts vs total: cells give 30972.19, printed 30962.19
  - sgt1924 L170 Sociétés de Secours aux blessés militaires: expenditure parts vs total: cells give 32523.85, printed 32623.85
  - sgt1924 L175 Goutte de Lait de Sousse: receipts - expenditure vs balance: cells give 10658.1, printed 10558.1
  - sgt1924 L176 Goutte de Lait de Sfax: receipts parts vs total: cells give 44057.85, printed 47057.85
  - sgt1924 L180 Goutte de Lait de Djerba: expenditure parts vs total: cells give 9296.15, printed 9326.15
  - sgt1924 L182 TOTAUX: expenditure parts vs total: cells give 1696460.54, printed 1796907.08
  - sgt1924 L182 TOTAUX: receipts - expenditure vs balance: cells give 385641.17, printed 425713.94
  - sgt1924 societies TOTAUX (line 182) group 0 col 0: rows above vs printed: cells give 421730.88, printed 421730.87
  - sgt1924 societies TOTAUX (line 182) group 0 col 1: rows above vs printed: cells give 307075.77, printed 310075.77
  - sgt1924 societies TOTAUX (line 182) group 0 col 4: rows above vs printed: cells give 2182538.25, printed 2182548.25
  - sgt1924 societies TOTAUX (line 182) group 1 col 0: rows above vs printed: cells give 396384.33, printed 296057.79
  - sgt1924 societies TOTAUX (line 182) group 1 col 1: rows above vs printed: cells give 571047.82, printed 571077.82
  - sgt1924 societies TOTAUX (line 182) group 1 col 6: rows above vs printed: cells give 1796807.09, printed 1796907.08
  - sgt1924 societies TOTAUX (line 182) group 2 col 0: rows above vs printed: cells give 425613.94, printed 425713.94
  - sgt1924 societies TOTAUX (line 182) group 3 col 0: rows above vs printed: cells give 187277, printed 187895
  - sgt1925 L138 Société française de bienfaisance de Bizerte: expenditure parts vs total: cells give 14367.6, printed 14368.1
  - sgt1925 L139 Société française de bienfaisance de Kairouan: expenditure parts vs total: cells give 2487.65, printed 2547.65
  - sgt1925 L140 Société française de bienfaisance de Sousse: receipts - expenditure vs balance: cells give 1295.7, printed 1295.76
  - sgt1925 L141 Société française de bienfaisance de Sfax: receipts parts vs total: cells give 18076.85, printed 18076.05
  - sgt1925 L141 Société française de bienfaisance de Sfax: receipts - expenditure vs balance: cells give 842.05, printed 843.05
  - sgt1925 L142 Société musulmane de bienfaisance de Tunis: receipts parts vs total: cells give 157107.05, printed 157197.05
  - sgt1925 L143 Société musulmane de bienfaisance de Bizerte: receipts - expenditure vs balance: cells give 3457.97, printed 2457.97
  - sgt1925 L144 Société musulmane de bienfaisance de Nabeul: receipts - expenditure vs balance: cells give 3822.9, printed 3832.9
  - sgt1925 L145 Société musulmane de bienfaisance de Kairouan: expenditure parts vs total: cells give 23907.0, printed 23907.6
  - sgt1925 L148 Société musulmane de bienfaisance de Tozeur: receipts parts vs total: cells give 10929.47, printed 10229.47
  - sgt1925 L148 Société musulmane de bienfaisance de Tozeur: receipts - expenditure vs balance: cells give 5765.82, printed 6456.02
  - sgt1925 L151 Clinique du Dr Cuénod: expenditure parts vs total: cells give 21936, printed 27886
  - sgt1925 L153 Asile de nuit et Maternité israélites: expenditure parts vs total: cells give 11278.0, printed 11268
  - sgt1925 L154 Garderie israélite: receipts parts vs total: cells give 59989.6, printed 59929.6
  - sgt1925 L154 Garderie israélite: receipts - expenditure vs balance: cells give 32583.45, printed 32443.45
  - sgt1925 L158 Protection de la jeune fille: receipts parts vs total: cells give 53615, printed 53715
  - sgt1925 L158 Protection de la jeune fille: receipts - expenditure vs balance: cells give 221, printed 121
  - sgt1925 L159 Vestiaire Central: receipts - expenditure vs balance: cells give 1060.0, printed 0
  - sgt1925 L160 Dispensaire Alapetite: expenditure parts vs total: cells give 32895.87, printed 32895.88
  - sgt1925 L161 Œuvre de la Crèche: expenditure parts vs total: cells give 29282.62, printed 29283.62
  - sgt1925 L162 Institut héliothérapique du Kram: expenditure parts vs total: cells give 106933.3, printed 106733.3
  - sgt1925 L163 Sociétés de Secours aux blessés militaires: receipts - expenditure vs balance: cells give 159762.15, printed 0
  - sgt1925 L164 Goutte de Lait de Maktar: receipts - expenditure vs balance: cells give 8882.35, printed 8882.85
  - sgt1925 L165 Goutte de Lait de Thala: receipts - expenditure vs balance: cells give 4660.4, printed 4658.4
  - sgt1925 L167 Goutte de Lait de Sousse: expenditure parts vs total: cells give 49117.75, printed 19117.75
  - sgt1925 L169 Goutte de Lait de Gafsa: receipts - expenditure vs balance: cells give 9311.2, printed 9811.2
  - sgt1925 L170 Goutte de Lait de Tozeur: receipts parts vs total: cells give 10556.51, printed 15556.57
  - sgt1925 L170 Goutte de Lait de Tozeur: receipts - expenditure vs balance: cells give 10804.77, printed 11366.27
  - sgt1925 L171 Goutte de Lait de Gabès: receipts - expenditure vs balance: cells give 1173.18, printed 1173.43
  - sgt1925 L172 Goutte de Lait de Djerba: receipts parts vs total: cells give 12241.05, printed 12240.05
  - sgt1925 L175 Société musulmane de bienfaisance du Kef: receipts parts vs total: cells give 33111.75, printed 32111.75
  - sgt1925 L175 Société musulmane de bienfaisance du Kef: receipts - expenditure vs balance: cells give 11772.31, printed 18772.31
  - sgt1925 L177 Société musulmane de bienfaisance de Sfax: receipts parts vs total: cells give 18661.7, printed 18662.3
  - sgt1925 L177 Société musulmane de bienfaisance de Sfax: expenditure parts vs total: cells give 13821.55, printed 13821.85
  - sgt1925 L177 Société musulmane de bienfaisance de Sfax: receipts - expenditure vs balance: cells give 4840.45, printed 4840.75
  - sgt1925 L178 Société musulmane de bienfaisance de Béja: receipts - expenditure vs balance: cells give 10755.95, printed 10748.95
  - sgt1925 L180 Sœurs missionnaires N. D. d'Afrique à Carthag: receipts - expenditure vs balance: cells give 28.25, printed 0
  - sgt1925 L182 TOTAUX: expenditure parts vs total: cells give 2189191.39, printed 2189194.39
  - sgt1925 societies TOTAUX (line 182) group 0 col 0: rows above vs printed: cells give 344597.64, printed 349598.3
  - sgt1925 societies TOTAUX (line 182) group 0 col 1: rows above vs printed: cells give 415147.18, printed 367273.38
  - sgt1925 societies TOTAUX (line 182) group 0 col 2: rows above vs printed: cells give 653061.35, printed 588561.35
  - sgt1925 societies TOTAUX (line 182) group 0 col 3: rows above vs printed: cells give 1145547.45, printed 537254.13
  - sgt1925 societies TOTAUX (line 182) group 0 col 4: rows above vs printed: cells give 2561782.48, printed 1842687.16
  - sgt1925 societies TOTAUX (line 182) group 1 col 0: rows above vs printed: cells give 486255.04, printed 456056.64
  - sgt1925 societies TOTAUX (line 182) group 1 col 1: rows above vs printed: cells give 639385.39, printed 645445.89
  - sgt1925 societies TOTAUX (line 182) group 1 col 5: rows above vs printed: cells give 421405.14, printed 421355.15
  - sgt1925 societies TOTAUX (line 182) group 1 col 6: rows above vs printed: cells give 2189181.69, printed 2189194.39
  - sgt1925 societies TOTAUX (line 182) group 2 col 0: rows above vs printed: cells give 407890.2, printed 401600.14
  - sgt1925 societies TOTAUX (line 182) group 3 col 0: rows above vs printed: cells give 399107, printed 397782
  - sgt1925 societies TOTAUX (line 182) group 3 col 1: rows above vs printed: cells give 238972, printed 239172
  - sgt1925 societies TOTAUX (line 182) group 3 col 3: rows above vs printed: cells give 1544, printed 1563
  - sgt1926 L134 M. le Président de la Société française de Bi: receipts - expenditure vs balance: cells give 553.4, printed 534.4
  - sgt1926 L135 M. le Président de la Société française de Bi: receipts - expenditure vs balance: cells give 14.9, printed 414.9
  - sgt1926 L139 M. le Président de la Société musulmane de Bi: receipts parts vs total: cells give 31155.31, printed 31175.31
  - sgt1926 L149 M. le Président de la Société de Secours aux : receipts - expenditure vs balance: cells give 244311.55, printed 242456.55
  - sgt1926 L152 M. le Président de la Société italienne de Bi: expenditure parts vs total: cells give 53881.0, printed 53921
  - sgt1926 L155 SUBTOTAL A reporter: receipts - expenditure vs balance: cells give 358626.47, printed 375714.42
  - sgt1926 L181 TOTAUX: receipts - expenditure vs balance: cells give 638261.73, printed 692576.04
  - sgt1926 societies SUBTOTAL A reporter (line 155) group 0 col 3: rows above vs printed: cells give 329011.25, printed 329031.25
  - sgt1926 societies SUBTOTAL A reporter (line 155) group 1 col 2: rows above vs printed: cells give 273836.18, printed 273876.18
  - sgt1926 societies SUBTOTAL A reporter (line 155) group 2 col 0: rows above vs printed: cells give 389695.42, printed 375714.42
  - sgt1926 societies TOTAUX (line 181) group 0 col 3: rows above vs printed: cells give 1041424.64, printed 1041444.64
  - sgt1926 societies TOTAUX (line 181) group 1 col 2: rows above vs printed: cells give 393691.53, printed 393731.53
  - sgt1926 societies TOTAUX (line 181) group 2 col 0: rows above vs printed: cells give 706557.04, printed 692576.04
  - sgt1926 societies TOTAUX (line 181) group 3 col 0: rows above vs printed: cells give 372281, printed 371979
  - sgt1926 societies TOTAUX (line 181) group 3 col 2: rows above vs printed: cells give 136247, printed 135247
  - sgt1927 L126 Société Française de Bienfaisance, Tunis: receipts parts vs total: cells give 321018.92, printed 321019.01
  - sgt1927 L127 Société Française de Bienfaisance, Sousse: receipts parts vs total: cells give 26743.2, printed 26743.02
  - sgt1927 L127 Société Française de Bienfaisance, Sousse: receipts - expenditure vs balance: cells give 47.27, printed 47.45
  - sgt1927 L128 Société Française de Bienfaisance, Sfax: receipts parts vs total: cells give 22475.47, printed 22476.01
  - sgt1927 L128 Société Française de Bienfaisance, Sfax: receipts - expenditure vs balance: cells give 3495.56, printed 3495.65
  - sgt1927 L129 Société Française de Bienfaisance, Bizerte: receipts parts vs total: cells give 30445.63, printed 30446.35
  - sgt1927 L132 Société Musulmane de Bienfaisance, Tunis: expenditure parts vs total: cells give 268869.21, printed 268870.02
  - sgt1927 L133 Société Musulmane de Bienfaisance du Kef: expenditure parts vs total: cells give 10897.58, printed 10897.94
  - sgt1927 L136 Société Musulmane de Bienfaisance de Kairouan: receipts - expenditure vs balance: cells give 6377.0, printed 637
  - sgt1927 L140 Société Musulmane de bienfaisance de Ferryvil: receipts parts vs total: cells give 5462.01, printed 5462.1
  - sgt1927 L140 Société Musulmane de bienfaisance de Ferryvil: expenditure parts vs total: cells give 4648.05, printed 4646.05
  - sgt1927 L144 Asile de nuit et Maternité israélites, Tunis: receipts parts vs total: cells give 12120.15, printed 12100.15
  - sgt1927 L145 Cuisines populaires israélites, Tunis: receipts parts vs total: cells give 100715.75, printed 22844.85
  - sgt1927 L146 Société italienne de Bienfaisance, Tunis: receipts parts vs total: cells give 48728.15, printed 100715.75
  - sgt1927 L146 Société italienne de Bienfaisance, Tunis: receipts - expenditure vs balance: cells give 53022.25, printed 1034.65
  - sgt1927 L153 Garderie Israélite, Tunis: receipts parts vs total: cells give 203627.0, printed 193627.45
  - sgt1927 L153 Garderie Israélite, Tunis: receipts - expenditure vs balance: cells give 142674.4, printed 42674.4
  - sgt1927 L154 Union des Femmes de France: receipts parts vs total: cells give 95754.99, printed 95755.8
  - sgt1927 L159 Œuvre Française de Protection du 1er âge: expenditure parts vs total: cells give 22218.15, printed 22218.25
  - sgt1927 L161 Vestiaire Central de Tunis: expenditure parts vs total: cells give 246936.7, printed 246936.07
  - sgt1927 L161 Vestiaire Central de Tunis: receipts - expenditure vs balance: cells give 6297.09, printed 6296.46
  - sgt1927 L167 Goutte de Lait, Sfax: receipts parts vs total: cells give 48548.14, printed 48548.95
  - sgt1927 L172 Caisse de secours et de Bienfaisance Israélit: expenditure parts vs total: cells give 206832.4, printed 206833.75
  - sgt1927 L174 TOTAUX: receipts parts vs total: cells give 2299614.87, printed 2399615.68
  - sgt1927 L174 TOTAUX: expenditure parts vs total: cells give 2068076.38, printed 2078342.57
  - sgt1927 L174 TOTAUX: receipts - expenditure vs balance: cells give 321273.11, printed 351750.88
  - sgt1927 societies TOTAUX (line 174) group 0 col 0: rows above vs printed: cells give 473613.96, printed 373615.22
  - sgt1927 societies TOTAUX (line 174) group 0 col 1: rows above vs printed: cells give 472035.37, printed 472036.09
  - sgt1927 societies TOTAUX (line 174) group 0 col 3: rows above vs printed: cells give 737622.69, printed 727604.31
  - sgt1927 societies TOTAUX (line 174) group 0 col 4: rows above vs printed: cells give 2373731.3, printed 2399615.68
  - sgt1927 societies TOTAUX (line 174) group 1 col 1: rows above vs printed: cells give 647775.36, printed 647776.26
  - sgt1927 societies TOTAUX (line 174) group 1 col 2: rows above vs printed: cells give 438587.29, printed 438578.01
  - sgt1927 societies TOTAUX (line 174) group 1 col 3: rows above vs printed: cells give 40508.53, printed 30241.06
  - sgt1927 societies TOTAUX (line 174) group 1 col 4: rows above vs printed: cells give 75962.35, printed 75963.07
  - sgt1927 societies TOTAUX (line 174) group 1 col 6: rows above vs printed: cells give 2078351.5, printed 2078342.57
  - sgt1927 societies TOTAUX (line 174) group 2 col 0: rows above vs printed: cells give 246000.88, printed 351750.88
  - sgt1928 L142 Hôpital israélite, Bizerte: receipts parts vs total: cells give 15731.2, printed 15631.2
  - sgt1928 L143 Société Française de Bienfaisance, Tunis: expenditure parts vs total: cells give 312629.98, printed 312626.98
  - sgt1928 L144 Société Française de Bienfaisance, Sousse: expenditure parts vs total: cells give 25736.8, printed 25781.8
  - sgt1928 L145 Société Française de Bienfaisance, Sfax: receipts - expenditure vs balance: cells give 1548.2, printed 1540.2
  - sgt1928 L149 Société Musulmane de Bienfaisance, Tunis: expenditure parts vs total: cells give 265914.36, printed 265614.36
  - sgt1928 L149 Société Musulmane de Bienfaisance, Tunis: receipts - expenditure vs balance: cells give 21163.64, printed 20863.64
  - sgt1928 L150 Société Musulmane de Bienfaisance du Kef: receipts - expenditure vs balance: cells give 35771.95, printed 10822.7
  - sgt1928 L155 Société Musulmane de Bienfaisance de Tozeur: expenditure parts vs total: cells give 6178.0, printed 6218.0
  - sgt1928 L160 Société de Secours aux Blessés militaires, Tu: receipts parts vs total: cells give 344400.15, printed 343400.15
  - sgt1928 L161 Asile de nuit et Maternité israélites, Tunis: expenditure parts vs total: cells give 20625.05, printed 21625.05
  - sgt1928 L162 Cuisines populaires israélites, Tunis: receipts - expenditure vs balance: cells give 5584.0, printed 1809.2
  - sgt1928 L175 Œuvre Française de Protection du 1er âge: receipts - expenditure vs balance: cells give 726.15, printed 0
  - sgt1928 L179 Goutte de Lait du Kef: expenditure parts vs total: cells give 38031.9, printed 28131.9
  - sgt1928 L181 Goutte de Lait, Thala: receipts parts vs total: cells give 6246.65, printed 6946.65
  - sgt1928 L184 Goutte de Lait, Sfax: receipts - expenditure vs balance: cells give 30378.1, printed 30378.2
  - sgt1928 L190 Caisse de Secours et de Bienfaisance israélit: expenditure parts vs total: cells give 37155.25, printed 33155.25
  - sgt1928 L190 Caisse de Secours et de Bienfaisance israélit: receipts - expenditure vs balance: cells give 3615.6, printed 0
  - sgt1928 L192 TOTAUX: receipts - expenditure vs balance: cells give 628517.97, printed 613253.65
  - sgt1928 societies TOTAUX (line 192) group 0 col 0: rows above vs printed: cells give 426748.2, printed 425748.2
  - sgt1928 societies TOTAUX (line 192) group 0 col 2: rows above vs printed: cells give 803599, printed 804299
  - sgt1928 societies TOTAUX (line 192) group 0 col 3: rows above vs printed: cells give 903474.61, printed 903374.61
  - sgt1928 societies TOTAUX (line 192) group 1 col 0: rows above vs printed: cells give 395776.8, printed 395916.8
  - sgt1928 societies TOTAUX (line 192) group 1 col 1: rows above vs printed: cells give 570312.93, printed 560309.93
  - sgt1928 societies TOTAUX (line 192) group 1 col 4: rows above vs printed: cells give 256845.55, printed 257845.55
  - sgt1928 societies TOTAUX (line 192) group 1 col 5: rows above vs printed: cells give 354855.35, printed 354900.35
  - sgt1928 societies TOTAUX (line 192) group 1 col 6: rows above vs printed: cells give 1956523.91, printed 1960823.91
  - sgt1928 societies TOTAUX (line 192) group 2 col 0: rows above vs printed: cells give 614245.65, printed 613253.65
  - sgt1928 societies TOTAUX (line 192) group 3 col 0: rows above vs printed: cells give 214794, printed 215804
  - sgt1928 societies TOTAUX (line 192) group 3 col 1: rows above vs printed: cells give 304853, printed 304865
  - sgt1928 societies TOTAUX (line 192) group 3 col 2: rows above vs printed: cells give 255451, printed 251951
  - sgt1929 L140 Sœurs de N.D. Espérance, Tunis: expenditure parts vs total: cells give 16090, printed 16000
  - sgt1929 L144 Société Française de Bienfaisance, Sousse: expenditure parts vs total: cells give 27773.1, printed 28773.1
  - sgt1929 L145 Société Française de Bienfaisance, Sfax: expenditure parts vs total: cells give 26746.3, printed 26746.6
  - sgt1929 L146 Société Française de Bienfaisance, Bizerte: receipts parts vs total: cells give 37268.9, printed 37198.9
  - sgt1929 L146 Société Française de Bienfaisance, Bizerte: receipts - expenditure vs balance: cells give 5881.1, printed 5881.4
  - sgt1929 L150 Société Musulmane de Bienfaisance du Kef: expenditure parts vs total: cells give 6671.4, printed 6672.1
  - sgt1929 L157 Société Musulmane de bienfaisance de Ferryvil: expenditure parts vs total: cells give 1275.0, printed 1275.6
  - sgt1929 L157 Société Musulmane de bienfaisance de Ferryvil: receipts - expenditure vs balance: cells give 1644.95, printed 1645.55
  - sgt1929 L161 Asile de nuit et Maternité israélites, Tunis: receipts - expenditure vs balance: cells give 8643.05, printed 6569.4
  - sgt1929 L164 Société Italienne de Bienfaisance de Bizerte: expenditure parts vs total: cells give 10566.95, printed 10566.7
  - sgt1929 L166 Communauté israélite de Tunis: receipts parts vs total: cells give 1458658.52, printed 1458652.52
  - sgt1929 L167 Caisse de Secours et de Bienfaisance israélit: receipts parts vs total: cells give 47645.0, printed 47845
  - sgt1929 L169 Croix Verte de Tunis: expenditure parts vs total: cells give 38111.95, printed 38117.95
  - sgt1929 L170 Croix Verte de Bizerte: expenditure parts vs total: cells give 3602.72, printed 3632.7
  - sgt1929 L180 Goutte de Lait de Zaghouan: receipts parts vs total: cells give 34153.67, printed 34153.77
  - sgt1929 L184 Goutte de Lait, Thala: expenditure parts vs total: cells give 3768.6, printed 3768.69
  - sgt1929 L184 Goutte de Lait, Thala: receipts - expenditure vs balance: cells give 907.71, printed 907.8
  - sgt1929 L186 Goutte de Lait, Sfax: receipts - expenditure vs balance: cells give 38804.2, printed 38804.4
  - sgt1929 L190 TOTAUX: receipts parts vs total: cells give 5709289.91, printed 5709559.91
  - sgt1929 L190 TOTAUX: receipts - expenditure vs balance: cells give 1013367.07, printed 1074931.09
  - sgt1929 societies TOTAUX (line 190) group 0 col 1: rows above vs printed: cells give 734544.06, printed 734474.06
  - sgt1929 societies TOTAUX (line 190) group 0 col 3: rows above vs printed: cells give 2778311.37, printed 2778241.47
  - sgt1929 societies TOTAUX (line 190) group 0 col 4: rows above vs printed: cells give 5709553.91, printed 5709559.91
  - sgt1929 societies TOTAUX (line 190) group 1 col 0: rows above vs printed: cells give 831746.76, printed 831747.76
  - sgt1929 societies TOTAUX (line 190) group 1 col 1: rows above vs printed: cells give 1118109.49, printed 1119049.49
  - sgt1929 societies TOTAUX (line 190) group 1 col 5: rows above vs printed: cells give 1280301.74, printed 1280307.72
  - sgt1929 societies TOTAUX (line 190) group 1 col 6: rows above vs printed: cells give 4696193.28, printed 4696192.84
  - sgt1929 societies TOTAUX (line 190) group 2 col 0: rows above vs printed: cells give 1074931.39, printed 1074931.09
  - sgt1929 societies TOTAUX (line 190) group 3 col 1: rows above vs printed: cells give 650639, printed 635079
  - sgt1930 L170 Société Française de Bienfaisance, Sfax: expenditure parts vs total: cells give 29980, printed 28980
  - sgt1930 L182 Société Musulmane de bienfaisance de Ferryvil: receipts - expenditure vs balance: cells give 1285, printed 1275
  - sgt1930 L186 Asile de nuit et Maternité israélites, Tunis: expenditure parts vs total: cells give 25948, printed 25958
  - sgt1930 L188 Société italienne de Bienfaisance, Tunis: receipts parts vs total: cells give 61463, printed 61461
  - sgt1930 L198 Fourneau des Pauvres de Tunis: expenditure parts vs total: cells give 198964, printed 207964
  - sgt1930 L207 Goutte de Lait du Kef: expenditure parts vs total: cells give 27717, printed 27647
  - sgt1930 L210 Goutte de Lait, Sousse: expenditure parts vs total: cells give 97014, printed 98014
  - sgt1930 L213 Goutte de Lait, Tozeur: receipts - expenditure vs balance: cells give 2, printed 0

- Flagged cells: derived_from_totals: 8, total_mismatch: 3.

  - sgt1923 1923 Société de Bienfaisance Française de Tunis / expenditure / general_expenses / Frais généraux = 33576 (derived_from_totals)
  - sgt1923 1923 Société de Bienfaisance Française de Sousse / expenditure / general_expenses / Frais généraux = 198 (derived_from_totals)
  - sgt1923 1923 Société de Bienfaisance Française de Sfax / expenditure / general_expenses / Frais généraux = 0 (derived_from_totals)
  - sgt1923 1923 Dispensaire Alapetite / expenditure / general_expenses / Frais généraux = 25806.95 (derived_from_totals)
  - sgt1923 1923 Institut Héliothérapique du Kram / expenditure / general_expenses / Frais généraux = 27995.15 (derived_from_totals)
  - sgt1923 1923 Goutte de Lait Lucien Saint de Djerba (second line) / balance / cash_remaining_end_of_year / Reste en caisse au 1er janvier suivant = 276.55 (derived_from_totals)
  - sgt1926 1926 Mme la Supérieure des Sœurs de N.-D. de l'Espérance, rue Bach Hamba, à Tunis / statistics / persons_medical_assistance / Nombre de personnes ayant bénéficié de  = 6760 (derived_from_totals)
  - sgt1926 1926 M. le Président de la Société française de Bienfaisance de Sfax / balance / cash_remaining_end_of_year / Reste en caisse au 1er janvier suivant = 534.4 (total_mismatch)
  - sgt1926 1926 M. le Président de la Société française de Bienfaisance de Bizerte / balance / cash_remaining_end_of_year / Reste en caisse au 1er janvier suivant = 414.9 (total_mismatch)
  - sgt1926 1926 Mme la Présidente de la Goutte de Lait de Sousse / expenditure / medical_assistance / Assistance médicale = 195.9 (derived_from_totals)
  - sgt1927 1927 Société Musulmane de Bienfaisance de Kairouan / balance / cash_remaining_end_of_year / Reste en caisse au 1er janvier suivant = 637 (total_mismatch)

## Rows printed with no figures (not stored)

- sgt1923: Société de Bienfaisance Française de La Goulette
- sgt1925: Société musulmane de bienfaisance de Sousse; Société Internationale la « Croix Verte » de Tunis; Cantines scolaires; Goutte de Lait de Mahdia
- sgt1926: M. le Président de la Société française de Bienfaisance de Sousse; M. le Président de la Société musulmane de Bienfaisance de Sousse; M. le Président de la Croix Verte de Tunis; Mme la Présidente de la Goutte de Lait de Mahdia
- sgt1927: Hôpital israélite, Tunis; Société Française de Bienfaisance, Kairouan; Société Musulmane de Bienfaisance de Sousse; Société Musulmane de Bienfaisance de Nabeul; Société Musulmane de Bienfaisance de Béja; Société Musulmane de Bienfaisance de Sfax; Société de Secours aux Blessés militaires, Tunis; Société Italienne de Bienfaisance de Bizerte; Société Italienne de Bienfaisance de Sfax; Croix Verte de Tunis; Clinique Châtelier oculiste; Goutte de Lait, Tunis; Goutte de Lait, Mahdia; Caisse de Secours et de Bienfaisance Israélite de Sfax
- sgt1928: Hôpital israélite, Tunis; Société Française de Bienfaisance, Kairouan; Société Française de Bienfaisance, La Goulette; Société Musulmane de Bienfaisance de Nabeul; Société Musulmane de Bienfaisance de Béja; Société Italienne de Bienfaisance de Bizerte; Société Italienne de Bienfaisance de Sfax; Croix Verte de Bizerte; Clinique Châtelier oculiste; Garderie Israélite, Tunis; Union des Femmes de France; Goutte de Lait, Tunis; Goutte de Lait, Gabès; Goutte de Lait, Gafsa; Caisse de secours et de Bienfaisance Israélite, Sousse; Caisse de Secours et de Bienfaisance Israélite de Sfax
- sgt1929: Société Française de Bienfaisance, Kairouan; Société Musulmane de Bienfaisance de Nabeul; Société Musulmane de Bienfaisance de Béja
- sgt1930: Hôpital israélite, Bizerte; Société Française de Bienfaisance, Bizerte; Société Française de Bienfaisance, Kairouan; Société Musulmane de Bienfaisance, Tunis; Société Musulmane de Bienfaisance du Kef; Société Musulmane de Bienfaisance de Nabeul; Société Musulmane de Bienfaisance de Béja; Société Musulmane de Bienfaisance de Sfax; Société Musulmane de Bienfaisance de Monastir; Société de Secours aux Blessés militaires, Tunis; Cuisines populaires israélites, Tunis; Société Italienne de Bienfaisance de Bizerte; Société Italienne de Bienfaisance de Sfax; Communauté israélite de Tunis; Caisse de Secours et de Bienfaisance israélite de Bizerte; Caisse de secours et de Bienfaisance Israélite, Sousse; Croix Verte de Tunis; Croix Verte de Bizerte; Garderie Israélite, Tunis; Union des Femmes de France; Dispensaire Alapetite, Tunis; Œuvre de la Crèche de Tunis; Institut Héliothérapique du Kram; Vestiaire Central de Tunis; Goutte de Lait de La Goulette; Goutte de Lait de Téboursouk; Goutte de Lait, Sfax; Goutte de Lait, Gafsa; Goutte de Lait, Gabès


## Cross-check between editions

Cash at 1 January of year N against the cash remaining at the end of year N−1 printed in the previous edition, for societies whose name code is the same in both editions: 229 comparisons, 121 equal.
  - central_clothing_store_tunis 1927: cash at 1 January 72866.66 vs cash remaining end 1926 6254.47
  - central_clothing_store_tunis 1929: cash at 1 January 119656.98 vs cash remaining end 1928 84772.3
  - charity_villemin 1924: cash at 1 January 26707.45 vs cash remaining end 1923 6092.25
  - clinic_dr_cuenod 1923: cash at 1 January 0 vs cash remaining end 1922 0.35
  - creche_charity_tunis 1927: cash at 1 January 2776.31 vs cash remaining end 1926 2274.05
  - creche_charity_tunis 1929: cash at 1 January 0 vs cash remaining end 1928 25162.41
  - dames_francaises_beja 1923: cash at 1 January 1315.55 vs cash remaining end 1922 1660.35
  - day_nursery_jewish 1923: cash at 1 January 11298.95 vs cash remaining end 1922 5989.45
  - day_nursery_jewish_tunis 1927: cash at 1 January 115554.05 vs cash remaining end 1926 115554.5
  - dispensary_ste_marguerite_laverie 1930: cash at 1 January 0 vs cash remaining end 1929 235
  - french_benevolent_society_bizerte 1927: cash at 1 January 14.9 vs cash remaining end 1926 414.9
  - french_benevolent_society_bizerte 1928: cash at 1 January 3112.35 vs cash remaining end 1927 3112.45
  - french_benevolent_society_goulette 1930: cash at 1 January 4815 vs cash remaining end 1929 4815.11
  - french_benevolent_society_sfax 1927: cash at 1 January 553.4 vs cash remaining end 1926 534.4
  - french_benevolent_society_sfax 1929: cash at 1 January 1548.2 vs cash remaining end 1928 1540.2
  - french_benevolent_society_sfax 1930: cash at 1 January 16284 vs cash remaining end 1929 16284.9
  - french_benevolent_society_sousse 1930: cash at 1 January 6185 vs cash remaining end 1929 6185.85
  - french_benevolent_society_tunis 1923: cash at 1 January 7402.14 vs cash remaining end 1922 7402
  - french_benevolent_society_tunis 1924: cash at 1 January 22096.05 vs cash remaining end 1923 22048.15
  - french_benevolent_society_tunis 1925: cash at 1 January 7792.13 vs cash remaining end 1924 7793.19
  - french_benevolent_society_tunis 1930: cash at 1 January 34271 vs cash remaining end 1929 34271.46
  - green_cross_bizerte 1927: cash at 1 January 350 vs cash remaining end 1926 300
  - green_cross_tunis 1923: cash at 1 January 0 vs cash remaining end 1922 106.3
  - green_cross_tunis 1929: cash at 1 January 5916.25 vs cash remaining end 1928 0
  - heliotherapy_institute_kram 1928: cash at 1 January 6861.9 vs cash remaining end 1927 6864.9
  - heliotherapy_institute_kram 1929: cash at 1 January 13172.85 vs cash remaining end 1928 12172.45
  - hospital_jewish_bizerte 1929: cash at 1 January 0 vs cash remaining end 1928 927.05
  - italian_benevolent_society_tunis 1930: cash at 1 January 13243 vs cash remaining end 1929 13243.5
  - jewish_relief_and_benevolent_fund_sousse 1927: cash at 1 January 139.53 vs cash remaining end 1926 159.53
  - milk_dispensary_gabes 1925: cash at 1 January 1641.39 vs cash remaining end 1924 1641.79
  - milk_dispensary_gafsa 1925: cash at 1 January 1571.85 vs cash remaining end 1924 1571.1
  - milk_dispensary_gafsa 1926: cash at 1 January 9311.2 vs cash remaining end 1925 9811.2
  - milk_dispensary_kef 1929: cash at 1 January 240.3 vs cash remaining end 1928 171.15
  - milk_dispensary_kef 1930: cash at 1 January 9982 vs cash remaining end 1929 8989.2
  - milk_dispensary_mactar 1928: cash at 1 January 1618.65 vs cash remaining end 1927 1678.65
  - milk_dispensary_mahdia 1923: cash at 1 January 500 vs cash remaining end 1922 91.35
  - milk_dispensary_mahdia 1924: cash at 1 January 500 vs cash remaining end 1923 1548.65
  - milk_dispensary_maktar 1926: cash at 1 January 8882.35 vs cash remaining end 1925 8882.85
  - milk_dispensary_maktar 1930: cash at 1 January 5556 vs cash remaining end 1929 4617.7
  - milk_dispensary_sousse 1925: cash at 1 January 10658.1 vs cash remaining end 1924 10558.1
  - milk_dispensary_sousse 1930: cash at 1 January 47150 vs cash remaining end 1929 47150.26
  - milk_dispensary_thala 1924: cash at 1 January 464.65 vs cash remaining end 1923 1264.65
  - milk_dispensary_thala 1927: cash at 1 January 4132.3 vs cash remaining end 1926 4072.3
  - milk_dispensary_thala 1930: cash at 1 January 907 vs cash remaining end 1929 907.8
  - milk_dispensary_tozeur 1925: cash at 1 January 4186.51 vs cash remaining end 1924 9186.57
  - milk_dispensary_tozeur 1926: cash at 1 January 12889.12 vs cash remaining end 1925 11366.27
  - milk_dispensary_tozeur 1927: cash at 1 January 12730.87 vs cash remaining end 1926 12428.87
  - milk_dispensary_tozeur 1928: cash at 1 January 690.65 vs cash remaining end 1927 2413.82
  - milk_dispensary_tozeur 1929: cash at 1 January 7639.45 vs cash remaining end 1928 1356.45
  - milk_dispensary_tozeur 1930: cash at 1 January 1360 vs cash remaining end 1929 1301.75
  - milk_dispensary_zaghouan 1930: cash at 1 January 22854 vs cash remaining end 1929 22854.27
  - muslim_benevolent_society_beja 1926: cash at 1 January 11417 vs cash remaining end 1925 10748.95
  - muslim_benevolent_society_bizerte 1923: cash at 1 January 2611.52 vs cash remaining end 1922 1343.02
  - muslim_benevolent_society_bizerte 1924: cash at 1 January 1356.62 vs cash remaining end 1923 1343.02
  - muslim_benevolent_society_bizerte 1925: cash at 1 January 2374.77 vs cash remaining end 1924 2622.77
  - muslim_benevolent_society_bizerte 1926: cash at 1 January 3457.97 vs cash remaining end 1925 2457.97
  - muslim_benevolent_society_bizerte 1930: cash at 1 January 5696 vs cash remaining end 1929 5696.47
  - muslim_benevolent_society_ferryville 1927: cash at 1 January 328.5 vs cash remaining end 1926 330
  - muslim_benevolent_society_ferryville 1928: cash at 1 January 1299 vs cash remaining end 1927 816.05
  - muslim_benevolent_society_ferryville 1929: cash at 1 January 0 vs cash remaining end 1928 953.7
  - muslim_benevolent_society_ferryville 1930: cash at 1 January 1645 vs cash remaining end 1929 1645.55
  - muslim_benevolent_society_kairouan 1923: cash at 1 January 4368.2 vs cash remaining end 1922 1227.75
  - muslim_benevolent_society_kairouan 1925: cash at 1 January 1574.75 vs cash remaining end 1924 2034.55
  - muslim_benevolent_society_kairouan 1926: cash at 1 January 7864.05 vs cash remaining end 1925 3195.5
  - muslim_benevolent_society_kairouan 1927: cash at 1 January 7864.05 vs cash remaining end 1926 16717.6
  - muslim_benevolent_society_kairouan 1928: cash at 1 January 13578.3 vs cash remaining end 1927 637
  - muslim_benevolent_society_kairouan 1930: cash at 1 January 27319 vs cash remaining end 1929 27319.45
  - muslim_benevolent_society_kef 1926: cash at 1 January 12772.31 vs cash remaining end 1925 18772.31
  - muslim_benevolent_society_kef 1927: cash at 1 January 24089.16 vs cash remaining end 1926 24088.66
  - muslim_benevolent_society_kef 1928: cash at 1 January 21369.15 vs cash remaining end 1927 20869.07
  - muslim_benevolent_society_kef 1929: cash at 1 January 12495.8 vs cash remaining end 1928 10822.7
  - muslim_benevolent_society_monastir 1923: cash at 1 January 2558.65 vs cash remaining end 1922 3744.4
  - muslim_benevolent_society_monastir 1924: cash at 1 January 0 vs cash remaining end 1923 3744.4
  - muslim_benevolent_society_monastir 1928: cash at 1 January 4109.12 vs cash remaining end 1927 2907.85
  - muslim_benevolent_society_nabeul 1923: cash at 1 January 1675.75 vs cash remaining end 1922 4274
  - muslim_benevolent_society_nabeul 1924: cash at 1 January 1027.7 vs cash remaining end 1923 1028.15
  - muslim_benevolent_society_nabeul 1926: cash at 1 January 3822.95 vs cash remaining end 1925 3832.9
  - muslim_benevolent_society_sousse 1923: cash at 1 January 4025.06 vs cash remaining end 1922 6346.51
  - muslim_benevolent_society_sousse 1924: cash at 1 January 4025.06 vs cash remaining end 1923 6346.51
  - muslim_benevolent_society_sousse 1930: cash at 1 January 21205 vs cash remaining end 1929 21204.98
  - muslim_benevolent_society_tozeur 1925: cash at 1 January 6878.52 vs cash remaining end 1924 6038.86
  - muslim_benevolent_society_tozeur 1926: cash at 1 January 3112.5 vs cash remaining end 1925 6456.02
  - muslim_benevolent_society_tozeur 1928: cash at 1 January 0 vs cash remaining end 1927 568.7
  - muslim_benevolent_society_tozeur 1929: cash at 1 January 6382.55 vs cash remaining end 1928 2385.7
  - muslim_benevolent_society_tozeur 1930: cash at 1 January 55 vs cash remaining end 1929 8.1
  - muslim_benevolent_society_tunis 1926: cash at 1 January 0 vs cash remaining end 1925 157109.05
  - muslim_benevolent_society_tunis 1928: cash at 1 January 15128.6 vs cash remaining end 1927 15128.63
  - night_shelter_maternity_jewish_tunis 1927: cash at 1 January 0 vs cash remaining end 1926 4156
  - night_shelter_maternity_jewish_tunis 1929: cash at 1 January 0 vs cash remaining end 1928 2073.65
  - night_shelter_maternity_jewish_tunis 1930: cash at 1 January 6569 vs cash remaining end 1929 6569.4
  - poor_kitchen 1923: cash at 1 January 20581.96 vs cash remaining end 1922 4949.54
  - poor_kitchen 1924: cash at 1 January 0 vs cash remaining end 1923 8472.36
  - poor_kitchen 1925: cash at 1 January 3963 vs cash remaining end 1924 0
  - poor_kitchen_tunis 1927: cash at 1 January 5805.13 vs cash remaining end 1926 5951.97
  - poor_kitchen_tunis 1928: cash at 1 January 178.92 vs cash remaining end 1927 178.16
  - poor_kitchen_tunis 1930: cash at 1 January 8867 vs cash remaining end 1929 7495.17
  - protection_of_young_girls 1925: cash at 1 January 215 vs cash remaining end 1924 315.95
  - protection_of_young_girls 1928: cash at 1 January 2292.75 vs cash remaining end 1927 2291.25
  - protection_of_young_girls 1929: cash at 1 January 2327.75 vs cash remaining end 1928 2323.75
  - protection_of_young_girls 1930: cash at 1 January 1727 vs cash remaining end 1929 1727.75
  - school_canteens 1924: cash at 1 January 30873.86 vs cash remaining end 1923 33977.95
  - societes_relief_blesses_militaires 1925: cash at 1 January 188953.2 vs cash remaining end 1924 197973.2
  - society_internationale_green_cross_bizerte 1923: cash at 1 January 0 vs cash remaining end 1922 2159.6
  - society_internationale_green_cross_bizerte 1924: cash at 1 January 17 vs cash remaining end 1923 0
  - society_internationale_green_cross_bizerte 1925: cash at 1 January 1350 vs cash remaining end 1924 317
  - soup_kitchens_jewish 1923: cash at 1 January 968.4 vs cash remaining end 1922 1943.1
  - soup_kitchens_musulmanes 1923: cash at 1 January 8062.25 vs cash remaining end 1922 704.4
  - union_of_french_women_red_cross_french_tunis 1923: cash at 1 January 35470.45 vs cash remaining end 1922 33970.45

