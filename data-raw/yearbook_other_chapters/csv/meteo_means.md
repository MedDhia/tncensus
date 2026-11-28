# Pluies moyennes mensuelles, par saison et annuelles

*Mean monthly, seasonal and annual rainfall by station and period.*

Source: *Statistique générale de la Tunisie*, *Météorologie*, editions sgt1930. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views: sgt1930 p. 288, f846; sgt1930 p. 289, f847; sgt1930 p. 290, f848; sgt1930 p. 291, f849.

Transcriptions: `../transcribed/meteo_<edition>.txt`; rebuild with `python3 -I data-raw/yearbook_other_chapters/extract_meteo.py build`.

Rows: 1360 (one per station, period and printed column: twelve months September-August, four seasons, the year). These retrospective means exist only as means (the yearly values behind them are not printed in the same edition), so every printed cell is stored, the seasons and the year included; `year` is NA.

Partial coverage: Transcribed: sgt1936 f123-f144 (complete), sgt1935 f166-f183 (complete), sgt1930 f818-f849 (parts a)-d), complete) and sgt1929 f284-f311 (parts a)-c)). NOT YET TRANSCRIBED: sgt1929 f312 (Manoubia rainfall by wind direction and month: fits no existing meteo_ table, would need a table of its own); every Météorologie page of sgt1928 (f806-f835), sgt1927 (f282-f307), sgt1926 (f819-f845), sgt1925 (f309-f334), sgt1924 (f1247-f1268), sgt1923 (f745-f764) and sgt1922 (f255-f273). meteo_climate holds sgt1929-sgt1930; meteo_means holds sgt1930 only.

## Columns

- `census`: Source edition (`sgt1936` = *Statistique générale de la Tunisie*, 1936 edition).
- `table_id`: `rainfall_means` = *d) Pluies moyennes mensuelles, par saison et annuelles pour les périodes : 1926-1930 et 1901-1930*.
- `gallica_ark`: Gallica ark of the volume (views are only unique within a volume).
- `source_page`: Printed page number (one page per table).
- `gallica_view`: Gallica view of `source_page`.
- `year`: NA (means of a period: see `period`).
- `station`: Station heading as printed.
- `period`: Period of the mean as printed (`1926-1930`, `1901-1930`).
- `level`: `month`, `season` or `year`.
- `month`: Month (English), season (`autumn` = September-November, `winter`, `spring`, `summer`) or `year` (agricultural year September-August).
- `month_fr`: Column heading as printed.
- `measure`: `rainfall_mean` (mean rainfall over the period).
- `measure_fr`: Table heading as printed.
- `unit`: `mm` (whole millimetres).
- `value`: Mean as printed; 0 for "gttes"; NA when a dash is printed.
- `obs`: `traces` ("gttes", gouttes: value 0); `no_observation` ("—", value NA).
- `flag`: Empty, `not_applicable` (dash printed), `derived_from_totals` (sgt1930 p. 290 Sfax 1926-1930 Hiver, broken type, typed as the sum of its three months).

## Validation

- each season = sum of its three months within 1 mm and the Année = sum of the four seasons within 2 mm (the means are printed rounded to whole millimetres), where every cell is printed: 395 checks; passed 393; failed 2.

Failed checks (printed values kept; each re-read on a native-resolution crop):

  - sgt1930 p.288 (f846) Mabtouha (St-Victor) 1926-1930: months vs win: cells give 239, printed 199 (difference -40)
  - sgt1930 p.290 (f848) Sousse 1926-1930: months vs aut: cells give 104, printed 106 (difference 2)

Both failures re-read on zoomed native-resolution crops; printed values kept. sgt1930 p. 288 Mabtouha (St-Victor) 1926-1930: Décembre 84, Janvier 113, Février 42 give 239, Hiver printed 199, and the printed Année 423 = 110 + 199 + 111 + 3 agrees with the Hiver: one of the three month cells is misprinted (likely Janvier 113 for 73), not identifiable with certainty. p. 290 Sousse 1926-1930: Septembre 64, Octobre 15, Novembre 25 give 104, Automne printed 106 (the Année 257 agrees with 106): a printed inconsistency beyond rounding.

- Flags: derived_from_totals: 1, not_applicable: 5.
- Observation signs: no_observation: 5, traces: 16.

## Image versus OCR

- Every cell typed from native-resolution crops of the page images; the Gallica OCR was not used.
