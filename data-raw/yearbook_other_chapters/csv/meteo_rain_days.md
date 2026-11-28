# Relevé pluviométrique : nombre de jours de pluie, par station et par mois

*Rainfall record: number of rainy days by station and month (solar year).*

Source: *Statistique générale de la Tunisie*, *Météorologie*, editions sgt1935, sgt1936. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views: sgt1935 p. 147, f167; sgt1935 p. 149, f169; sgt1935 p. 151, f171; sgt1935 p. 153, f173; sgt1935 p. 155, f175; sgt1935 p. 157, f177; sgt1935 p. 159, f179; sgt1935 p. 161, f181; sgt1935 p. 163, f183; sgt1936 p. 113, f124; sgt1936 p. 115, f126; sgt1936 p. 117, f128; sgt1936 p. 119, f130; sgt1936 p. 121, f132; sgt1936 p. 123, f134; sgt1936 p. 125, f136; sgt1936 p. 127, f138; sgt1936 p. 129, f140; sgt1936 p. 131, f142; sgt1936 p. 133, f144.

Transcriptions: `../transcribed/meteo_<edition>.txt`; rebuild with `python3 -I data-raw/yearbook_other_chapters/extract_meteo.py build`.

Rows: 8328 (one per station, month and edition). The printed annual totals (*Année*) are checks, not rows. Each solar year is printed in one edition only, so no overlap selection is needed (SPEC_ADDENDUM rule 4 would apply to any year printed twice).

Partial coverage: Transcribed: sgt1936 f123-f144 (complete) and sgt1935 f166-f183 (complete). NOT YET TRANSCRIBED: every Météorologie page of sgt1930 (f818-f849), sgt1929 (f284-f312), sgt1928 (f806-f835), sgt1927 (f282-f307), sgt1926 (f819-f845), sgt1925 (f309-f334), sgt1924 (f1247-f1268), sgt1923 (f745-f764) and sgt1922 (f255-f273). Tables meteo_rainfall_season, meteo_climate and meteo_means are designed but have no rows yet.

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

- Annual total = sum of the twelve months, for every line whose twelve months are all observed and whose annual total is printed: 505 checks; passed 464; failed 41.

Failed checks (printed values kept; each re-read on a native-resolution crop):

  - sgt1935 p.148 (f168) Djebel Oust days: months vs Année: cells give 96, printed 101 (difference 5)
  - sgt1935 p.152 (f172) Sidi bou Becker days: months vs Année: cells give 91, printed 93 (difference 2)
  - sgt1935 p.156 (f176) Le Sers (gare) days: months vs Année: cells give 60, printed 58 (difference -2)
  - sgt1935 p.156 (f176) Tadjerouine (Aïn-Zouagha) days: months vs Année: cells give 68, printed 73 (difference 5)
  - sgt1935 p.156 (f176) Mactar days: months vs Année: cells give 68, printed 78 (difference 10)
  - sgt1936 p.112 (f123) Bizerte (Port) days: months vs Année: cells give 75, printed 77 (difference 2)
  - sgt1936 p.112 (f123) Aïn-bou-Rass (Captage) days: months vs Année: cells give 45, printed 48 (difference 3)
  - sgt1936 p.112 (f123) Mateur days: months vs Année: cells give 78, printed 81 (difference 3)
  - sgt1936 p.112 (f123) El-Oggaline (Aïn-Rhelal) days: months vs Année: cells give 59, printed 60 (difference 1)
  - sgt1936 p.112 (f123) Tamera (Aïn-Kherma) days: months vs Année: cells give 101, printed 99 (difference -2)
  - sgt1936 p.112 (f123) Utique I days: months vs Année: cells give 89, printed 96 (difference 7)
  - sgt1936 p.112 (f123) Selma days: months vs Année: cells give 78, printed 82 (difference 4)
  - sgt1936 p.112 (f123) Djebel-Abiod days: months vs Année: cells give 80, printed 82 (difference 2)
  - sgt1936 p.112 (f123) Béja days: months vs Année: cells give 131, printed 134 (difference 3)
  - sgt1936 p.112 (f123) Oum-el-Aguareb days: months vs Année: cells give 87, printed 86 (difference -1)
  - sgt1936 p.112 (f123) El-Guéria days: months vs Année: cells give 78, printed 75 (difference -3)
  - sgt1936 p.112 (f123) Aïn-Essid days: months vs Année: cells give 88, printed 87 (difference -1)
  - sgt1936 p.112 (f123) Le Munchar days: months vs Année: cells give 93, printed 95 (difference 2)
  - sgt1936 p.112 (f123) Guermanez days: months vs Année: cells give 79, printed 78 (difference -1)
  - sgt1936 p.112 (f123) M'Zourah (Sidi-Khalled) days: months vs Année: cells give 88, printed 89 (difference 1)
  - sgt1936 p.112 (f123) Tabarka days: months vs Année: cells give 124, printed 128 (difference 4)
  - sgt1936 p.112 (f123) Aïn-Sebaa days: months vs Année: cells give 64, printed 66 (difference 2)
  - sgt1936 p.112 (f123) Aïn-Draham days: months vs Année: cells give 98, printed 100 (difference 2)
  - sgt1936 p.114 (f125) Henchir-French days: months vs Année: cells give 57, printed 54 (difference -3)
  - sgt1936 p.114 (f125) Radès days: months vs Année: cells give 66, printed 65 (difference -1)
  - sgt1936 p.116 (f127) Fedjet-Khemakhem days: months vs Année: cells give 82, printed 74 (difference -8)
  - sgt1936 p.116 (f127) Dridjat days: months vs Année: cells give 91, printed 100 (difference 9)
  - sgt1936 p.116 (f127) Djebel-Oust days: months vs Année: cells give 118, printed 109 (difference -9)
  - sgt1936 p.116 (f127) Menzel-bou-Zelfa days: months vs Année: cells give 87, printed 86 (difference -1)
  - sgt1936 p.116 (f127) Beni-Aïech days: months vs Année: cells give 56, printed 57 (difference 1)
  - sgt1936 p.116 (f127) Bir-bou-Rekba days: months vs Année: cells give 58, printed 54 (difference -4)
  - sgt1936 p.120 (f131) Mell-Rechga days: months vs Année: cells give 61, printed 59 (difference -2)
  - sgt1936 p.122 (f133) Testour-Briouik days: months vs Année: cells give 102, printed 99 (difference -3)
  - sgt1936 p.122 (f133) Ksar-bou-Kriss (Ouled-Zaïr) days: months vs Année: cells give 57, printed 40 (difference -17)
  - sgt1936 p.122 (f133) Henchir-Sidi-bou-Goussa days: months vs Année: cells give 54, printed 92 (difference 38)
  - sgt1936 p.122 (f133) Henchir-el-Bey days: months vs Année: cells give 92, printed 55 (difference -37)
  - sgt1936 p.122 (f133) Sidi-bou-Rouis (Gare) days: months vs Année: cells give 40, printed 55 (difference 15)
  - sgt1936 p.124 (f135) Lorbeuss (Gare) days: months vs Année: cells give 34, printed 31 (difference -3)
  - sgt1936 p.126 (f137) Sbeïtla (Henchir-Touille) days: months vs Année: cells give 73, printed 75 (difference 2)
  - sgt1936 p.126 (f137) Sbeïtla-Nord days: months vs Année: cells give 42, printed 40 (difference -2)
  - sgt1936 p.128 (f139) El-Djem days: months vs Année: cells give 68, printed 74 (difference 6)

sgt1936 p. 113 (f124): the Mai column is printed as an exact copy of the Avril column on every line of the page, which explains all eighteen failures on that page (Mai cells flagged `total_mismatch`; the true May values are not recoverable from the annual total alone with certainty, so the printed values are kept). Every other failure below was re-read month by month on zoomed native-resolution crops; the printed values are kept and the misprinted cell cannot be identified unless stated: sgt1936 p. 115 Henchir-French, Radès; p. 117 Fedjet-Khemakhem, Dridjat, Djebel-Oust, Menzel-bou-Zelfa, Beni-Aïech, Bir-bou-Rekba; p. 121 Mell-Rechga; p. 123 Testour-Briouik; p. 123 Ksar-bou-Kriss (Ouled-Zaïr), Henchir-Sidi-bou-Goussa, Henchir-el-Bey and Sidi-bou-Rouis (Gare): the four days-Année cells at the foot of the page are printed out of line (the month sums 57, 54, 92, 40 match the printed 40/55/92/55 only after shifting), a misprint in the totals, so no row is flagged; p. 125 Lorbeuss (Gare); p. 127 Sbeïtla (Henchir-Touille), Sbeïtla-Nord; p. 129 El-Djem. sgt1935 p. 149 Djebel Oust (96 vs 101), p. 153 Sidi bou Becker (91 vs 93), p. 157 Le Sers (gare) (60 vs 58), Tadjerouine (Aïn-Zouagha) (68 vs 73) and Mactar (68 vs 78): every month re-read on zoomed crops; printed inconsistencies.

- Flags: not_applicable: 812, total_mismatch: 18.
- Observation signs: days_not_observed: 76, incomplete: 45, no_observation: 691.

## Image versus OCR

- Every cell typed from native-resolution crops of the page images; the Gallica OCR was not used.
