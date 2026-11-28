# Relevé pluviométrique de l'année agricole : pluies totales par saison et pour l'année

*Rainfall of the agricultural year: total rainfall by season and station.*

Source: *Statistique générale de la Tunisie*, *Météorologie*, editions sgt1929, sgt1930. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views: sgt1929 p. 256, f284; sgt1929 p. 257, f285; sgt1929 p. 258, f286; sgt1929 p. 259, f287; sgt1929 p. 260, f288; sgt1929 p. 261, f289; sgt1929 p. 262, f290; sgt1930 p. 260, f818; sgt1930 p. 261, f819; sgt1930 p. 262, f820; sgt1930 p. 263, f821; sgt1930 p. 264, f822; sgt1930 p. 265, f823; sgt1930 p. 266, f824; sgt1930 p. 267, f825.

Transcriptions: `../transcribed/meteo_<edition>.txt`; rebuild with `python3 -I data-raw/yearbook_other_chapters/extract_meteo.py build`.

Rows: 2477 (one per station and season of the agricultural year, plus one row per printed normal annual rainfall). The agricultural year runs September-August (Automne = September-November, Hiver = December-February, Printemps = March-May, Eté = June-August) and is coded in `year` as the year it ends (1929-1930 = 1930). The printed annual total of the year (*Année 1929-30*) is a check, not a row. The printed normal (*Année 1901-1925*) exists only as a mean: it is stored with `season` = `year`, `measure` = `rainfall_mean`, `period` = `1901-1925` and `year` NA, only where a value is printed.

Partial coverage: Transcribed: sgt1936 f123-f144 (complete), sgt1935 f166-f183 (complete), sgt1930 f818-f849 (parts a)-d), complete) and sgt1929 f284-f311 (parts a)-c)). NOT YET TRANSCRIBED: sgt1929 f312 (Manoubia rainfall by wind direction and month: fits no existing meteo_ table, would need a table of its own); every Météorologie page of sgt1928 (f806-f835), sgt1927 (f282-f307), sgt1926 (f819-f845), sgt1925 (f309-f334), sgt1924 (f1247-f1268), sgt1923 (f745-f764) and sgt1922 (f255-f273). meteo_climate holds sgt1929-sgt1930; meteo_means holds sgt1930 only.

## Columns

- `census`: Source edition (`sgt1936` = *Statistique générale de la Tunisie*, 1936 edition).
- `table_id`: `rainfall_agricultural_year` = *a) Relevé pluviométrique de l'année agricole*.
- `gallica_ark`: Gallica ark of the volume (views are only unique within a volume).
- `source_page`: Printed page number (one page per table).
- `gallica_view`: Gallica view of `source_page`.
- `year`: Year in which the agricultural year (September-August) ends (1928-1929 = 1929, 1929-1930 = 1930); NA for the normals.
- `region`: Natural-region heading as printed in sgt1930 part a) (sgt1929 prints no headings in part a): the sgt1930 names are supplied for the same groups) (e.g. `Kroumirie`, `Mogods`, `Golfe de Tunis`, `Région de Dakla`), without roman numerals, in title case with accents restored as in the solar-year tables. The part a) regions differ from the part b) regions.
- `controle`: Empty (part a) has no contrôle headings).
- `station`: Rain-gauge station exactly as printed.
- `period`: `1928-1929` / `1929-1930` for the observations of the agricultural year; `1901-1925` for the printed normal annual rainfall.
- `season`: `autumn`, `winter`, `spring`, `summer`, or `year` (normal annual rainfall).
- `season_fr`: Column heading as printed.
- `measure`: `rainfall` (total rainfall of the season) or `rainfall_mean` (normal annual rainfall, mean of the period).
- `measure_fr`: Table heading as printed.
- `unit`: `mm` (millimètres, one decimal).
- `value`: Value as printed; NA when nothing was printed (`—`).
- `obs`: `traces` ("gouttes": value 0); `no_observation` ("—", value NA). Empty otherwise.
- `flag`: Empty, `not_applicable` (dash printed: see `obs`), `illegible`, `derived_from_totals` (sgt1929: damaged digit typed as the printed Année minus the other seasons), `total_mismatch` (sgt1930 Menzel-Temime Printemps).

## Validation

- Année of the agricultural year = sum of the four seasons, for every line whose four seasons are printed and whose Année is printed: 405 checks; passed 394; failed 11.

Failed checks (printed values kept; each re-read on a native-resolution crop):

  - sgt1929 p.261 (f289) El-Alem (Henriville): seasons vs Année 1928-1929: cells give 508.0, printed 507.5 (difference -0.5)
  - sgt1929 p.261 (f289) Mahédia: seasons vs Année 1928-1929: cells give 447.5, printed 447.3 (difference -0.2)
  - sgt1929 p.262 (f290) Bordj-Lacroix: seasons vs Année 1928-1929: cells give 233.4, printed 233.7 (difference 0.3)
  - sgt1929 p.262 (f290) Maknassy (Saint-Félix): seasons vs Année 1928-1929: cells give 301.7, printed 305.7 (difference 4.0)
  - sgt1929 p.262 (f290) Gabès: seasons vs Année 1928-1929: cells give 118.9, printed 119.5 (difference 0.6)
  - sgt1930 p.260 (f818) Aïn-Sebaâ: seasons vs Année 1929-1930: cells give 1152.6, printed 1152.0 (difference -0.6)
  - sgt1930 p.262 (f820) Menzel-Temime: seasons vs Année 1929-1930: cells give 516.0, printed 410.3 (difference -105.7)
  - sgt1930 p.263 (f821) Le Kef I: seasons vs Année 1929-1930: cells give 510.9, printed 511.1 (difference 0.2)
  - sgt1930 p.265 (f823) Djebel-Mansour (Sainte-Gilberte): seasons vs Année 1929-1930: cells give 540.8, printed 510.8 (difference -30.0)
  - sgt1930 p.265 (f823) Sainte Maurice de Djebibina: seasons vs Année 1929-1930: cells give 475.0, printed 475.1 (difference 0.1)
  - sgt1930 p.265 (f823) Kundar: seasons vs Année 1929-1930: cells give 311.0, printed 311.9 (difference 0.9)

Every failure was re-read on a zoomed native-resolution crop of the line; printed values kept. sgt1930 p. 262 Menzel-Temime: Printemps (172.6) is printed identical to Hiver, the Année implies 66.9, so the Printemps cell is flagged `total_mismatch`. p. 265 Djebel-Mansour (Sainte-Gilberte) (540.8 vs 510.8, a difference of exactly 30: one digit misprinted, cell not identifiable). Small differences (p. 260 Aïn-Sebaâ -0.6, p. 263 Le Kef I +0.2, p. 265 Sainte Maurice de Djebibina +0.1, Kundar +0.9): printed inconsistencies, every digit clear. sgt1929 (every digit clear on a zoomed crop, printed inconsistencies): p. 261 El-Alem (Henriville) (seasons 508.0, Année 507.5), Mahédia (447.5 vs 447.3); p. 262 Bordj-Lacroix (233.4 vs 233.7), Maknassy (Saint-Félix) (301.7 vs 305.7), Gabès (118.9 vs 119.5).

- Flags: derived_from_totals: 2, not_applicable: 336, total_mismatch: 1.
- Observation signs: no_observation: 336, traces: 12.

## Image versus OCR

- Every cell typed from native-resolution crops of the page images; the Gallica OCR was not used.
