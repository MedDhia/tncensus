# Relevé pluviométrique : hauteur totale de pluie en millimètres et dixièmes, par station et par mois

*Rainfall record: total rainfall in millimetres by station and month (solar year).*

Source: *Statistique générale de la Tunisie*, *Météorologie*, editions sgt1935, sgt1936. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views: sgt1935 p. 146, f166; sgt1935 p. 147, f167; sgt1935 p. 148, f168; sgt1935 p. 149, f169; sgt1935 p. 150, f170; sgt1935 p. 151, f171; sgt1935 p. 152, f172; sgt1935 p. 153, f173; sgt1935 p. 154, f174; sgt1935 p. 155, f175; sgt1935 p. 156, f176; sgt1935 p. 157, f177; sgt1935 p. 158, f178; sgt1935 p. 159, f179; sgt1935 p. 160, f180; sgt1935 p. 161, f181; sgt1935 p. 162, f182; sgt1935 p. 163, f183; sgt1936 p. 112, f123; sgt1936 p. 113, f124; sgt1936 p. 114, f125; sgt1936 p. 115, f126; sgt1936 p. 116, f127; sgt1936 p. 117, f128; sgt1936 p. 118, f129; sgt1936 p. 119, f130; sgt1936 p. 120, f131; sgt1936 p. 121, f132; sgt1936 p. 122, f133; sgt1936 p. 123, f134; sgt1936 p. 124, f135; sgt1936 p. 125, f136; sgt1936 p. 126, f137; sgt1936 p. 127, f138; sgt1936 p. 128, f139; sgt1936 p. 129, f140; sgt1936 p. 130, f141; sgt1936 p. 131, f142; sgt1936 p. 132, f143; sgt1936 p. 133, f144.

Transcriptions: `../transcribed/meteo_<edition>.txt`; rebuild with `python3 -I data-raw/yearbook_other_chapters/extract_meteo.py build`.

Rows: 8328 (one per station, month and edition). The printed annual totals (*Année*) are checks, not rows. Each solar year is printed in one edition only, so no overlap selection is needed (SPEC_ADDENDUM rule 4 would apply to any year printed twice).

Partial coverage: Transcribed: sgt1936 f123-f144 (complete), sgt1935 f166-f183 (complete) and sgt1930 part a) f818-f825 (complete). NOT YET TRANSCRIBED: sgt1930 parts b) f826-f843, c) f844-f845 and d) f846-f849; every Météorologie page of sgt1929 (f284-f312), sgt1928 (f806-f835), sgt1927 (f282-f307), sgt1926 (f819-f845), sgt1925 (f309-f334), sgt1924 (f1247-f1268), sgt1923 (f745-f764) and sgt1922 (f255-f273). Tables meteo_climate and meteo_means are designed but have no rows yet.

## Columns

- `census`: Source edition (`sgt1936` = *Statistique générale de la Tunisie*, 1936 edition).
- `table_id`: `rainfall_solar_year` = *Relevé pluviométrique, année (solaire)*.
- `gallica_ark`: Gallica ark of the volume (views are only unique within a volume).
- `source_page`: Printed page number of the cell (mm January-September on the left page; mm October-December and every rainy-days column on the right page).
- `gallica_view`: Gallica view of `source_page`.
- `year`: Calendar (solar) year of the observations.
- `region`: Region heading as printed, without its roman numeral and in one case form across editions (e.g. `Tunisie du Nord`, `Tunisie du Centre (Hautes Plaines)`, `Haute Vallée de la Medjerdah`).
- `controle`: Contrôle civil heading as printed (e.g. `Contrôle de Bizerte`).
- `station`: Rain-gauge station exactly as printed.
- `month`: Month (English); `month_fr` as printed.
- `month_fr`: Month heading as printed.
- `measure`: `rainfall` (total height of rain) or `rain_days` (number of days with rain).
- `measure_fr`: Column heading as printed.
- `unit`: `mm` (millimetres, one decimal) or `days`.
- `value`: Value as printed; NA when nothing was observed.
- `obs`: Printed observation sign: `traces` ("gttes", gouttes: rain too small to measure, value 0); `no_observation` ("—", pas d'observation, value NA); `incomplete` ("O.I.", observations incomplètes: NA when printed alone, the printed partial value when printed beside a number); `days_not_observed` ("×", nombre de jours non observés, NA). Empty otherwise.
- `flag`: Empty, `not_applicable` (no value printed: see `obs`), `illegible`, `ocr_corrected`, `total_mismatch`, `derived_from_totals` (sgt1935: cell lost in the binding gutter, value = printed Année minus the other eleven months; its integer part, where visible, agrees).

## Validation

- Annual total = sum of the twelve months, for every line whose twelve months are all observed and whose annual total is printed: 527 checks; passed 499; failed 28.

Failed checks (printed values kept; each re-read on a native-resolution crop):

  - sgt1935 p.146 (f166) Mateur mm: months vs Année: cells give 516.5, printed 516.1 (difference -0.4)
  - sgt1935 p.152 (f172) El-Akhouat (gare) mm: months vs Année: cells give 349.1, printed 348.9 (difference -0.2)
  - sgt1935 p.154 (f174) El-Aroussa (Fme-Alsacienne) mm: months vs Année: cells give 434.9, printed 437.9 (difference 3.0)
  - sgt1935 p.156 (f176) Rohia mm: months vs Année: cells give 401.7, printed 401.6 (difference -0.1)
  - sgt1935 p.160 (f180) Kundar mm: months vs Année: cells give 298.4, printed 318.4 (difference 20.0)
  - sgt1935 p.160 (f180) Ksour-Essaf mm: months vs Année: cells give 262.0, printed 163.0 (difference -99.0)
  - sgt1935 p.162 (f182) Roderiebourg mm: months vs Année: cells give 116.9, printed 113.9 (difference -3.0)
  - sgt1936 p.112 (f123) Aïn-bou-Rass (Captage) mm: months vs Année: cells give 745.0, printed 742.0 (difference -3.0)
  - sgt1936 p.116 (f127) Saint-Cyprien mm: months vs Année: cells give 444.2, printed 445.2 (difference 1.0)
  - sgt1936 p.116 (f127) Mengoub mm: months vs Année: cells give 534.2, printed 534.7 (difference 0.5)
  - sgt1936 p.118 (f129) Zaghouan (Contrôle) mm: months vs Année: cells give 520.4, printed 519.9 (difference -0.5)
  - sgt1936 p.118 (f129) Djebel-Mansour (Saint-Joseph) mm: months vs Année: cells give 430.7, printed 430.5 (difference -0.2)
  - sgt1936 p.118 (f129) Djebel-Mansour (Henchir-Karbine) mm: months vs Année: cells give 535.9, printed 526.4 (difference -9.5)
  - sgt1936 p.118 (f129) Dhomda I mm: months vs Année: cells give 454.0, printed 451.5 (difference -2.5)
  - sgt1936 p.120 (f131) Bir-el-Akhdar mm: months vs Année: cells give 583.2, printed 584.2 (difference 1.0)
  - sgt1936 p.122 (f133) Testour-Briouik mm: months vs Année: cells give 434.0, printed 494.0 (difference 60.0)
  - sgt1936 p.122 (f133) Testour (Henchir-Aïn-Milled) mm: months vs Année: cells give 440.2, printed 439.2 (difference -1.0)
  - sgt1936 p.122 (f133) Sidi-Attia mm: months vs Année: cells give 434.8, printed 435.1 (difference 0.3)
  - sgt1936 p.122 (f133) Aïn-Tounga mm: months vs Année: cells give 474.9, printed 474.6 (difference -0.3)
  - sgt1936 p.126 (f137) Sbeïtla (Henchir-Touille) mm: months vs Année: cells give 437.5, printed 438.0 (difference 0.5)
  - sgt1936 p.126 (f137) Dar-Ouled-Sidi-Ferhatt mm: months vs Année: cells give 273.1, printed 373.1 (difference 100.0)
  - sgt1936 p.128 (f139) El-Kheley mm: months vs Année: cells give 291.6, printed 291.0 (difference -0.6)
  - sgt1936 p.128 (f139) Monastir mm: months vs Année: cells give 293.5, printed 293.0 (difference -0.5)
  - sgt1936 p.128 (f139) Teboulba (Bonne-Veine) mm: months vs Année: cells give 388.4, printed 288.4 (difference -100.0)
  - sgt1936 p.130 (f141) Le Jujubier mm: months vs Année: cells give 142.1, printed 134.9 (difference -7.2)
  - sgt1936 p.130 (f141) Beauregard mm: months vs Année: cells give 134.9, printed 183.2 (difference 48.3)
  - sgt1936 p.130 (f141) La Provence (Limaya) mm: months vs Année: cells give 183.2, printed 142.1 (difference -41.1)
  - sgt1936 p.132 (f143) Tatahouine mm: months vs Année: cells give 167.8, printed 193.7 (difference 25.9)

Every failure was re-read on zoomed native-resolution crops of both pages; printed values kept; misprint cell not identifiable unless stated. sgt1936: p. 112-113 Aïn-bou-Rass (Captage); p. 116-117 Saint-Cyprien, Mengoub; p. 118-119 Zaghouan (Contrôle), Djebel-Mansour (Saint-Joseph), Djebel-Mansour (Henchir-Karbine), Dhomda I; p. 120-121 Bir-el-Akhdar; p. 122-123 Testour-Briouik (434.0 vs 494.0, October clearly 31.2, so the Année looks misprinted), Testour (Henchir-Aïn-Milled), Sidi-Attia, Aïn-Tounga; p. 126-127 Sbeïtla (Henchir-Touille) (8 of the Année overprinted), Dar-Ouled-Sidi-Ferhatt (273.1 vs 373.1: Année misprint by 100); p. 128-129 El-Kheley, Monastir, Teboulba (Bonne-Veine) (388.4 vs 288.4: Année misprint by 100); p. 130-131 Le Jujubier, Beauregard, La Provence (Limaya): the three Année cells are permuted in print (months add to 142.1, 134.9, 183.2); p. 132-133 Tatahouine (167.8 vs 193.7). sgt1935: p. 146 Mateur (Décembre clearly 108.0); p. 152-153 El-Akhouat (gare) (Décembre clearly 42.7); p. 154-155 El-Aroussa (Fme-Alsacienne); p. 156 Rohia; p. 160 Kundar (298.4 vs 318.4), Ksour-Essaf (262.0 vs 163.0, Janvier clearly 110.0, Année misprint by 99); p. 162 Roderiebourg (Novembre printed "4.0" at the gutter, possibly a lost leading digit; not derived because the fragment is complete as printed). sgt1935 cells flagged `derived_from_totals` (Novembre lost in the binding gutter, typed as Année minus the other months) cannot fail their check by construction.

- Flags: derived_from_totals: 87, illegible: 20, not_applicable: 692.
- Observation signs: incomplete: 30, no_observation: 692, traces: 312.

## Image versus OCR

- Every cell typed from native-resolution crops of the page images; the Gallica OCR was not used.

Reading notes: sgt1936 p. 114 Salammbô S.O.S, February: the second digit of "3?.9 O.I." is damaged (illegible); April printed "221 O.I." without decimal point, stored 22.1; May printed "16 O.I.", stored 16. p. 117 Bir-M'Cherga II, December: first digit overprinted, read 32.8 (confirmed by the printed annual total 506.4). sgt1935: see the header of `meteo_sgt1935.txt` for the binding-gutter re-reading (December cells of p. 146-147 and 152-153 read; November decimals derived; November column of p. 148 printed half a line high and re-aligned); Sedjenane (Gare) December read 208.0 with its first digit only partly visible (no annual total printed).
