# Meteorology: survey of every edition

Survey of the meteorology pages of the *Statistique générale de la Tunisie*, view by view. Extraction: `extract_meteo.py`. Agricultural years run September-August and are coded by the year they end (1921-1922 = 1922).

| edition | ark | views |
|---|---|---|
| sgt1922 | `bpt6k9105649x` | 255-273 |
| sgt1923 | `bpt6k9105649x` | 745-764 |
| sgt1924 | `bpt6k9105649x` | 1247-1268 |
| sgt1925 | `bpt6k9105650k` | 309-334 |
| sgt1926 | `bpt6k9105650k` | 819-845 |
| sgt1927 | `bpt6k91056510` | 282-307 |
| sgt1928 | `bpt6k91056510` | 806-835 |
| sgt1929 | `bpt6k9105652d` | 284-312 |
| sgt1930 | `bpt6k9105652d` | 818-849 |
| sgt1935 | `bpt6k9105653t` | 166-183 |
| sgt1936 | `bpt6k91056547` | 123-144 |

## Parts per edition (newest first)

- **sgt1936**: f116-f122 research institutions (extract_research.py). f123-f144 *Relevé pluviométrique - année 1936*, eleven two-page spreads (left page: stations and mm January-September; right page: mm October-December, Année, then nombre de jours January-December, Année), stations grouped by region and contrôle; N.B. signes conventionnels: — pas d'observation, × nombre de jours non observés, O.I. observations incomplètes; "gttes" = gouttes. Only part b) (solar year) is printed. f145 blank.
- **sgt1935**: f165 (p. 145) Laboratoire de chimie (Sfax), analyses 1935 (not meteorology). f166-f183 *b) Relevé pluviométrique de l'année 1935*, nine two-page spreads (left page: stations and mm January-November, December in the binding gutter; right page: Total mm, then nombre de jours January-December, Total), same signes conventionnels as sgt1936; only part b) printed. The binding gutter hides the decimals of the November column on most spreads (cells derived from the annual total, flagged `derived_from_totals`). f184 blank.
- **sgt1930**: Météorologie at the end of chapter XI Agriculture, printed pages 260-291. f818-f825 (p. 260-267) *a) Relevé pluviométrique de l'année agricole (1929-1930)*, one table per page: Automne, Hiver, Printemps, Eté, Année 1929-30, Année 1901-1925 (p. 266 head misprinted "1901-1905"), stations grouped by natural region (Kroumirie ... Extrême Sud), no contrôle headings; transcribed (meteo_rainfall_season). f826-f843 (p. 268-285) *b) Relevé pluviométrique de l'année 1930*, nine two-page spreads (left page: stations and Millimètres de pluie by month; right page: the rest of the mm and Total, then Nombre de jours by month and Total; the exact split column is to be confirmed when transcribing), key "Signes conventionnels : — pas d'observation; × ..." across the top of the spread; NOT YET TRANSCRIBED. f844|f845 (p. 286-287) *c) Données climatologiques essentielles fournies par les principales régions tunisiennes (année 1930)*, one spread: localités grouped by region, Pluies (millimètres, nombre de jours), Température moyenne du mois le plus chaud / le plus froid (moyennes, maxima, minima), Température absolue (maxima, minima, with dates), nombre de jours au cours de l'année pendant lesquels le vent a soufflé de N, NE, E, SE, S, SW, W, NW, calme, vent dominant; footnotes (1)-(3) on missing months; NOT YET TRANSCRIBED. f846-f849 (p. 288-291) *Pluies moyennes mensuelles, par saison et annuelles pour les périodes : 1926-1930 et 1901-1930*, two lines (1926-1930, 1901-1930) per station (Tabarka ... Tatahouine), columns Septembre-Août, Automne, Hiver, Printemps, Eté, Année; NOT YET TRANSCRIBED (means only: meteo_means).
- **sgt1929**: f284-f312 Météorologie, parts a)-d) (views per part not yet surveyed page by page).
- **sgt1928**: f806-f835 Météorologie, parts a)-d) (views per part not yet surveyed page by page).
- **sgt1927**: f282-f287 a) relevé pluviométrique de l'année agricole 1926-1927; f288-f303 b) année solaire 1927 (mm | jours spreads); f304|f305 c) données climatologiques essentielles 1927; f306|f307 d) période 1901-1925, pluies moyennes mensuelles, saisonnières et annuelles (année agricole à partir de septembre).
- **sgt1926**: f819-f825 a) année agricole 1925-1926; f826-f839 b) année solaire 1926; f840|f841 c) données climatologiques essentielles 1926; f842-f845 d) températures moyennes et extrêmes mensuelles, saisonnières et annuelles 1901-1925.
- **sgt1925**: f309-f315 a) année agricole 1924-1925; f316-f329 b) année solaire 1925; f330|f331 c) données climatologiques 1925; f332-f334 d) pluviométrie agricole 1900-1901 à 1924-1925 (five-year means).
- **sgt1924**: f1247-f1251 a) année agricole 1923-1924; f1252-f1263 b) année solaire 1924; f1264|f1265 c) données climatologiques 1924; f1266-f1268 d) moyennes pluviométriques mensuelles, saisonnières et annuelles de la période décennale 1911-1920.
- **sgt1923**: f745-f749 a) année agricole 1922-1923 (with the 1901-1910 normal); f750-f759 b) année solaire 1923; f760|f761 c) données climatologiques essentielles 1923; f762-f764 d) pluviométrie agricole 1900-1901 à 1919-1920 (five-year means).
- **sgt1922**: f255-f259 a) année agricole 1921-1922; f260-f269 b) année solaire 1922; f270|f271 c) données climatologiques 1922; f272|f273 d) statistique thermométrique 1911-1920.

## Table design

- `meteo_rainfall_season`: a) agricultural-year rainfall by season (autumn, winter, spring, summer, year) per station, sgt1922-sgt1930; `year` = the year the agricultural year (September-August) ends, e.g. 1929-1930 coded 1930; the printed normals stored with `period`.
- `meteo_rainfall_monthly`: b) solar-year rainfall in mm per station and month, every edition.
- `meteo_rain_days`: b) solar-year number of rainy days per station and month, every edition.
- `meteo_climate`: c) données climatologiques essentielles (temperatures, pressure, humidity, wind ... by region/station and month, with `measure`/`measure_fr` and `unit`), sgt1922-sgt1930.
- `meteo_means`: d) retrospective tables that exist only as means (five-year means 1900-1920 / 1900-1925, decade means 1911-1920, temperatures 1901-1925, rainfall means 1901-1925), stored with `period`.

Common columns: census, table_id, gallica_ark, source_page, gallica_view, year, region, controle, station (as printed), month/season/period, measure, measure_fr, unit, value, obs, flag.

## Tables built

| CSV | editions | rows | checks | failed |
|---|---|---|---|---|
| `meteo_rainfall_season` | sgt1930 | 1292 | 212 | 6 |
| `meteo_rainfall_monthly` | sgt1935, sgt1936 | 8328 | 527 | 28 |
| `meteo_rain_days` | sgt1935, sgt1936 | 8328 | 505 | 41 |

## Coverage

Transcribed: sgt1936 f123-f144 (complete), sgt1935 f166-f183 (complete) and sgt1930 part a) f818-f825 (complete). NOT YET TRANSCRIBED: sgt1930 parts b) f826-f843, c) f844-f845 and d) f846-f849; every Météorologie page of sgt1929 (f284-f312), sgt1928 (f806-f835), sgt1927 (f282-f307), sgt1926 (f819-f845), sgt1925 (f309-f334), sgt1924 (f1247-f1268), sgt1923 (f745-f764) and sgt1922 (f255-f273). Tables meteo_climate and meteo_means are designed but have no rows yet.

