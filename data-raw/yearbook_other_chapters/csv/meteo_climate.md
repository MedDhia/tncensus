# Données climatologiques essentielles fournies par les principales régions tunisiennes

*Essential climatological data of the main Tunisian regions: rainfall, temperatures and winds by station.*

Source: *Statistique générale de la Tunisie*, *Météorologie*, editions sgt1929, sgt1930. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views: sgt1929 p. 282, f310; sgt1929 p. 283, f311; sgt1930 p. 286, f844; sgt1930 p. 287, f845.

Transcriptions: `../transcribed/meteo_<edition>.txt`; rebuild with `python3 -I data-raw/yearbook_other_chapters/extract_meteo.py build`.

Rows: 1403 (one per station and measure: rainfall and rainy days of the year; maxima, minima and moyenne of the hottest and of the coldest month; absolute (extrême annuelle) maxima and minima with their dates; annual mean maxima, minima and moyenne; days of the year by dominant wind direction N ... NW and calm; plus one `dominant_wind` row per station). The dominant wind (*vent dominant*) is a direction, not a number: its row has `value` NA, flag `not_applicable`, and the printed direction in `text_fr` (e.g. `NW`, `SE - SW`).

Partial coverage: Transcribed: sgt1936 f123-f144 (complete), sgt1935 f166-f183 (complete), sgt1930 f818-f849 (parts a)-d), complete) and sgt1929 f284-f311 (parts a)-c)). NOT YET TRANSCRIBED: sgt1929 f312 (Manoubia rainfall by wind direction and month: fits no existing meteo_ table, would need a table of its own); every Météorologie page of sgt1928 (f806-f835), sgt1927 (f282-f307), sgt1926 (f819-f845), sgt1925 (f309-f334), sgt1924 (f1247-f1268), sgt1923 (f745-f764) and sgt1922 (f255-f273). meteo_climate holds sgt1929-sgt1930; meteo_means holds sgt1930 only.

## Columns

- `census`: Source edition (`sgt1936` = *Statistique générale de la Tunisie*, 1936 edition).
- `table_id`: `climate_essentials` = *c) Données climatologiques essentielles fournies par les principales régions tunisiennes*.
- `gallica_ark`: Gallica ark of the volume (views are only unique within a volume).
- `source_page`: Printed page of the cell (rainfall and the hottest / coldest month on the left page, the rest on the right page).
- `gallica_view`: Gallica view of `source_page`.
- `year`: Calendar year of the observations.
- `region`: Region heading as printed (vertical, without accents in print: `REGION DES OASIS`), typed with accents restored (`Région du Nord`, `Région du Nord-Est`, `Région Centrale`, `Sahel`, `Région des Oasis`, `Extrême Sud`, `Sahara`).
- `station`: Localité as printed, without its footnote marker.
- `note_fr`: Footnote of the station as printed (missing months), empty otherwise.
- `measure`: `rainfall`, `rain_days`, `temp_hottest_month_max|min|mean`, `temp_coldest_month_max|min|mean`, `temp_absolute_max|min`, `temp_annual_mean_max|min`, `temp_annual_mean`, `wind_days_n` ... `wind_days_nw`, `calm_days`, `dominant_wind`.
- `measure_fr`: Column heading as printed (group : column).
- `unit`: `mm`, `days`, `degC` (degrees Celsius, one decimal) or `direction`.
- `date_fr`: For `temp_absolute_max|min`: month(s) of the extreme as printed (`Juil.`, `J. F.` = janvier and février, `J. D.` = janvier and décembre); empty otherwise.
- `text_fr`: For `dominant_wind`: the printed direction; empty otherwise.
- `value`: Value as printed; NA when a dash is printed and for `dominant_wind`.
- `obs`: `no_observation` ("—" printed, value NA); `traces` (sgt1929 Fort Saint rainfall printed "0" = gouttes, value 0). Empty otherwise.
- `flag`: Empty, `not_applicable` (dash printed, or the text row `dominant_wind`), `derived_from_totals` (sgt1930 Fort Saint coldest-month moyenne: decimal smudged, typed (maxima + minima) / 2), `illegible` (sgt1929 Tabarca annual moyenne printed "18°" without its decimal), `row_realigned` (sgt1929 Ben-Gardane extrême maxima, printed one line low).

## Validation

- moyenne = (maxima + minima) / 2 within 0.3 degree (an approximate identity: at 0.1 degree eleven sgt1930 cells differ by 0.15-0.3, so the printed moyenne is not exactly the midpoint; in sgt1929 the hottest-month moyenne is printed systematically below the midpoint), for the hottest month, the coldest month and the annual mean, where both are printed; wind days N ... NW + calm at most the days of the year (sgt1930: they add to exactly 365 at only 17 of the 31 stations: days without observation are not counted, so equality is not an identity); printed vent dominant = direction(s) with the most days (calm aside): 299 checks; passed 283; failed 16.

Failed checks (printed values kept; each re-read on a native-resolution crop):

  - sgt1929 p.282 (f310) Souk-el-Arba: hottest month moyenne vs (maxima + minima) / 2: cells give 29.8, printed 28.6 (difference -1.2)
  - sgt1929 p.282 (f310) Bizerte (Carouba): hottest month moyenne vs (maxima + minima) / 2: cells give 26.2, printed 25.5 (difference -0.7)
  - sgt1929 p.282 (f310) Bizerte (Carouba): coldest month moyenne vs (maxima + minima) / 2: cells give 8.85, printed 9.2 (difference 0.35)
  - sgt1929 p.282 (f310) Tunis (Manoubia): hottest month moyenne vs (maxima + minima) / 2: cells give 25.85, printed 25.5 (difference -0.35)
  - sgt1929 p.282 (f310) Grombalia: hottest month moyenne vs (maxima + minima) / 2: cells give 26.3, printed 25.6 (difference -0.7)
  - sgt1929 p.282 (f310) Medjez-el-Bab: hottest month moyenne vs (maxima + minima) / 2: cells give 27.55, printed 27.1 (difference -0.45)
  - sgt1929 p.282 (f310) Medjez-el-Bab: coldest month moyenne vs (maxima + minima) / 2: cells give 8.15, printed 8.5 (difference 0.35)
  - sgt1929 p.282 (f310) Thala: hottest month moyenne vs (maxima + minima) / 2: cells give 25.1, printed 24.7 (difference -0.4)
  - sgt1929 p.282 (f310) Kairouan: hottest month moyenne vs (maxima + minima) / 2: cells give 27.95, printed 27.6 (difference -0.35)
  - sgt1929 p.282 (f310) Sousse: hottest month moyenne vs (maxima + minima) / 2: cells give 25.15, printed 24.8 (difference -0.35)
  - sgt1929 p.282 (f310) Bou-Thadi: hottest month moyenne vs (maxima + minima) / 2: cells give 28.55, printed 28.1 (difference -0.45)
  - sgt1929 p.282 (f310) Zarzis: hottest month moyenne vs (maxima + minima) / 2: cells give 29.45, printed 28.9 (difference -0.55)
  - sgt1929 p.282 (f310) Kébili: hottest month moyenne vs (maxima + minima) / 2: cells give 34.2, printed 33.7 (difference -0.5)
  - sgt1929 p.282 (f310) Fort Saint: coldest month moyenne vs (maxima + minima) / 2: cells give 6.5, printed 7.5 (difference 1.0)
  - sgt1930 p.286 (f844) Béja: coldest month moyenne vs (maxima + minima) / 2: cells give 9.35, printed 10.3 (difference 0.95)
  - sgt1930 p.286 (f844) Djerba: vent dominant printed W, most days E

Both failures re-read on zoomed native-resolution crops; printed values kept. sgt1930 p. 286 Béja, mois le plus froid: maxima 14.6, minima 4.1, moyenne 10.3, every digit clear (the midpoint is 9.35; misprinted cell not identifiable). p. 287 Djerba: wind days N 41, NE 31, E 108, SE 44, S 27, SW 32, W 44, NW 38, calm 0, vent dominant printed W (E has the most days): printed as such. sgt1929 p. 282 (f310), every cell re-read on native-resolution crops, printed values kept: the hottest-month moyenne is printed 0.35-0.7 below the midpoint of maxima and minima at Bizerte (Carouba), Tunis (Manoubia), Grombalia, Medjez-el-Bab, Thala, Kairouan, Sousse, Bou-Thadi, Zarzis and Kébili, and 1.2 below at Souk-el-Arba (40.1 / 19.5 / 28.6, every digit clear); the coldest-month moyenne is 0.35 above the midpoint at Bizerte (Carouba) and Medjez-el-Bab. In sgt1929 the printed moyenne is evidently computed from the daily means, not the midpoint, so these are not misprints. Fort Saint coldest month: maxima 14.2, minima printed "— 1.2" (dash as at Mactar and Thala, typed -1.2), moyenne 7.5: the midpoint is 6.5 (7.7 if the dash were a stray mark); kept as printed.

- Flags: derived_from_totals: 1, illegible: 1, not_applicable: 70, row_realigned: 1.
- Observation signs: no_observation: 9, traces: 1.

## Image versus OCR

- Every cell typed from native-resolution crops of the page images; the Gallica OCR was not used.
