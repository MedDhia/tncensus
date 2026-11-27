# Productions végétales. Cultures diverses ; superficie et production

*Crop production: area, production and yield of cereals, other food plants, industrial plants and tree crops.*

Source: *Statistique générale de la Tunisie*, chapter *Agriculture*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 210, f234, p. 212, f236, p. 214, f238; sgt1923 (`bpt6k9105649x`): p. 222, f724, p. 224, f726, p. 226, f728; sgt1924 (`bpt6k9105649x`): p. 230, f1220, p. 231, f1221, p. 232, f1222, p. 234, f1224; sgt1925 (`bpt6k9105650k`): p. 266, f290, p. 267, f291, p. 268, f292, p. 269, f293, p. 270, f294, p. 272, f296; sgt1926 (`bpt6k9105650k`): p. 242, f806, p. 244, f808, p. 246, f810; sgt1927 (`bpt6k91056510`): p. 234, f262, p. 236, f264, p. 238, f266; sgt1928 (`bpt6k91056510`): p. 234, f786, p. 236, f788, p. 238, f790; sgt1929 (`bpt6k9105652d`): p. 236, f264, p. 238, f266, p. 240, f268; sgt1930 (`bpt6k9105652d`): p. 240, f798, p. 241, f799, p. 242, f800, p. 243, f801, p. 244, f802, p. 245, f803; sgt1935 (`bpt6k9105653t`): p. 122, f142, p. 123, f143, p. 124, f144; sgt1936 (`bpt6k91056547`): p. 92, f103, p. 93, f104, p. 94, f105; sgt1939 (`bpt6k9105739w`): p. 95, f101, p. 96, f102, p. 97, f103, p. 98, f104.

Transcriptions: `../transcribed/agriculture_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_agriculture.py build`.

Rows: 1492. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Units: hectares, quintals, hectolitres (wine), quintals or hectolitres per hectare, trees (`unit`); value_type: mixed.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (rule 4 series: the latest edition printing that year; rule 5 tables: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (crop year = calendar year of the harvest, as printed; rule 5 tables: edition year)
- `zone`: `tunisia` (whole country), or the zone of sgt1925's cereal tables (`north`, `centre_south`)
- `zone_fr`: printed zone heading
- `crop_group`: sub-table letter (a cereals, b other food plants, c industrial plants, d shrub and tree crops)
- `crop_group_fr`: printed sub-table title
- `crop`: crop code (English)
- `crop_fr`: printed line heading
- `measure`: measure code (English)
- `measure_fr`: printed heading of the measure
- `unit`: unit of `value`, as printed (never converted)
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible`, `total_mismatch` (cell identified as the faulty one of a failed check, printed value kept), `derived_from_totals`, `not_applicable`

Printed in every edition: ten years to sgt1930 (two pages per sub-table: five years on the left, five years and the averages of the two half-periods and of the ten years on the right), three years and two averages from sgt1935. `year` = crop year (calendar year of the harvest) as printed. The printed averages (MOYENNE DES ANNÉES) are not stored; they are used as checks (mean of the printed years, to 0.2 %; averages of yields are not checked). Yields are checked against production / surface (to 5 %). The vine yield is not checked: footnote (2) computes it on the vineyard over 3 years old.

a) Céréales: blé dur and blé tendre are printed as one bracketed figure for 1913-1915 (crop `wheat`). In sgt1925 the cereals are printed for two zones only (`zone` = `north`: Tunisie septentrionale et Hauts plateaux, 1re-3e Régions; `centre_south`: Tunisie centrale et méridionale, 4e-5e Régions et Territoires militaires), with no whole-country figures; from sgt1926 the whole-country table returns without yields (footnote: the yield varies too much from one zone to another and is given per zone in the next table). b) c) d) are whole-country throughout. Dattiers: the Dégla trees are pieds imposables (footnote), and from sgt1926 so are the other dates; sgt1939 prints total and taxable trees (`trees` / `trees_taxable`), surfaces, and renames the autres dattiers communes (`crop_fr`). sgt1939 also renames the table Cultures arbustives et fruitières and adds figs, mandarins, apricots, quinces, pomegranates, peaches, pears, apples, plums, surfaces and young trees; 'pois et pois chiches' replaces 'pois chiches' (crop `peas_chickpeas`).

» is stored 0 as printed, except where it marks a figure not collected next to printed figures: flax surface and yield 1913-1915 (production printed), the vine yield of sgt1936 (» in every column) and the new lines of sgt1939 in 1937 (stored NA, `not_applicable`). Asterisks (provisional figures, usually the edition year) are not stored. sgt1926-sgt1930 print the 1925 autres dattiers production with a broken first digit (":52.000"): 352.000, as sgt1925 and the printed averages (`derived_from_totals`). Illegible cells cut by the binding (sgt1922 1917 potatoes surface and tobacco; sgt1923 1918 tobacco and olive trees; sgt1939 poiriers 1938 "100.00") are taken from a later printing where one exists.

Footnotes of d): (1) the Muslim vineyard, planted with table grapes (about 2.200 ha in sgt1926-sgt1929, 4.000 ha from sgt1930, 4.500 ha in sgt1939), scattered in small plots, is not counted; sgt1935: grubbing of 2.800 ha in 1935-36 not deducted. (3) oliviers en production = trees of 15 years and more. sgt1929-sgt1930: the 1929 almond trees (660.000) come from a recent census of fruit trees for the tax. sgt1939: the 1938 almond trees from the declarations collected by the Direction des Finances; the 1936-1937 orange trees estimated from declarations, 1938 from an unfinished survey; caroubiers mostly scattered trees, no surface.

Every failed check below was re-read on a zoomed native-resolution crop: they are printed inconsistencies (printed values kept). Yield failures recur unchanged in every printing of the same year (oats 1915-1916, soft wheat 1921, potatoes 1920, maize 1923, and sgt1925's zone yields): printed figures. sgt1924 prints the 1924 blé dur production 2.350.000 (= 1923); its own yield 2,4 and its 1920-1924 average 1.474.700 need 1.040.000, printed by every later edition (kept). sgt1925 prints the 1925 blé dur surface of the northern zone 129.774 (flag `total_mismatch`): its yield 6,6 and its averages need 329.774. sgt1930 prints the 1930 orange trees 19.000 (flag `total_mismatch`): its averages need about 90.000. The other failures are printed averages that do not fit the printed years (the years themselves agree across up to ten independent printings); several are off by a round amount (e.g. sgt1923 autres dattiers 1919-1923 774.859 for 974.859, sgt1927 1923-1927 olive trees 1.586.183 for 15.861.830), i.e. misprinted averages.

Survey of the whole chapter in every edition: `agriculture_survey.md`.

## Validation

- Checks against printed totals and identities: 1658; passed: 1537; failed: 121.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.210 (f234) crops_a oats_yield 1915: yield = production / area: cells give 10.67, printed 8.0 (difference -2.67)
  - sgt1922 p.210 (f234) crops_a oats_yield 1916: yield = production / area: cells give 5.43, printed 4.6 (difference -0.83)
  - sgt1922 p.210 (f234) crops_a maize_yield 1913: yield = production / area: cells give 3.00, printed 2 (difference -1.00)
  - sgt1922 p.211 (f235) crops_a soft_yield 1921: yield = production / area: cells give 9.19, printed 9.9 (difference 0.71)
  - sgt1922 p.213 (f237) crops_b potatoes_yield 1920: yield = production / area: cells give 33.90, printed 36 (difference 2.10)
  - sgt1923 p.222 (f724) crops_a oats_yield 1915: yield = production / area: cells give 10.67, printed 8.0 (difference -2.67)
  - sgt1923 p.222 (f724) crops_a oats_yield 1916: yield = production / area: cells give 5.43, printed 4.6 (difference -0.83)
  - sgt1923 p.223 (f725) crops_a soft_yield 1921: yield = production / area: cells give 9.19, printed 9.9 (difference 0.71)
  - sgt1923 p.223 (f725) crops_a maize_yield 1923: yield = production / area: cells give 3.34, printed 3.9 (difference 0.56)
  - sgt1923 p.225 (f727) crops_b potatoes_yield 1920: yield = production / area: cells give 33.90, printed 36 (difference 2.10)
  - sgt1924 p.230 (f1220) crops_a oats_yield 1915: yield = production / area: cells give 10.67, printed 8.0 (difference -2.67)
  - sgt1924 p.230 (f1220) crops_a oats_yield 1916: yield = production / area: cells give 5.43, printed 4.6 (difference -0.83)
  - sgt1924 p.231 (f1221) crops_a durum_yield 1924: yield = production / area: cells give 5.63, printed 2.4 (difference -3.23)
  - sgt1924 p.231 (f1221) crops_a soft_yield 1921: yield = production / area: cells give 9.19, printed 9.9 (difference 0.71)
  - sgt1924 p.231 (f1221) crops_a maize_yield 1923: yield = production / area: cells give 3.34, printed 3.9 (difference 0.56)
  - sgt1924 p.233 (f1223) crops_b potatoes_yield 1920: yield = production / area: cells give 33.90, printed 36 (difference 2.10)
  - sgt1925 p.266 (f290) crops_a barley_yield 1916: yield = production / area: cells give 2.94, printed 4 (difference 1.06)
  - sgt1925 p.267 (f291) crops_a durum_yield 1921: yield = production / area: cells give 5.76, printed 5 (difference -0.76)
  - sgt1925 p.267 (f291) crops_a durum_yield 1925: yield = production / area: cells give 16.95, printed 6.6 (difference -10.35)
  - sgt1925 p.267 (f291) crops_a barley_yield 1921: yield = production / area: cells give 8.39, printed 7.8 (difference -0.59)
  - sgt1925 p.267 (f291) crops_a barley_yield 1924: yield = production / area: cells give 3.19, printed 3.4 (difference 0.21)
  - sgt1925 p.268 (f292) crops_a soft_yield 1920: yield = production / area: cells give 2.79, printed 3 (difference 0.21)
  - sgt1925 p.268 (f292) crops_a barley_yield 1919: yield = production / area: cells give 1.61, printed 1.8 (difference 0.19)
  - sgt1925 p.269 (f293) crops_a durum_yield 1923: yield = production / area: cells give 2.01, printed 1.2 (difference -0.81)
  - sgt1925 p.269 (f293) crops_a oats_yield 1922: yield = production / area: cells give 1.02, printed 0.1 (difference -0.92)
  - sgt1925 p.270 (f294) crops_b potatoes_yield 1920: yield = production / area: cells give 33.90, printed 36 (difference 2.10)
  - sgt1926 p.244 (f808) crops_b potatoes_yield 1920: yield = production / area: cells give 33.90, printed 36 (difference 2.10)
  - sgt1927 p.236 (f264) crops_b potatoes_yield 1920: yield = production / area: cells give 33.90, printed 36 (difference 2.10)
  - sgt1928 p.236 (f788) crops_b potatoes_yield 1920: yield = production / area: cells give 33.90, printed 36 (difference 2.10)
  - sgt1929 p.238 (f266) crops_b potatoes_yield 1920: yield = production / area: cells give 33.90, printed 36 (difference 2.10)
  - sgt1922 p.211 (f235) crops_a durum_area: average 1913-1922: cells give 524861.40, printed 514858 (difference -10003.40)
  - sgt1922 p.211 (f235) crops_a durum_prod: average 1918-1922: cells give 1623420.00, printed 1663420 (difference 40000.00)
  - sgt1922 p.211 (f235) crops_a durum_prod: average 1913-1922: cells give 1614710.00, printed 1634710 (difference 20000.00)
  - sgt1922 p.211 (f235) crops_a barley_prod: average 1913-1917: cells give 1564000.00, printed 1782000 (difference 218000.00)
  - sgt1922 p.211 (f235) crops_a oats_area: average 1913-1917: cells give 56610.20, printed 56210 (difference -400.20)
  - sgt1922 p.213 (f237) crops_b beans_area: average 1913-1917: cells give 14440.00, printed 14400 (difference -40.00)
  - sgt1922 p.213 (f237) crops_b beans_prod: average 1913-1917: cells give 72200.00, printed 72600 (difference 400.00)
  - sgt1922 p.213 (f237) crops_b beans_prod: average 1913-1922: cells give 92500.00, printed 92700 (difference 200.00)
  - sgt1922 p.213 (f237) crops_c flax_prod: average 1918-1922: cells give 10700.00, printed 11160 (difference 460.00)
  - sgt1922 p.215 (f239) crops_d olive_bearing: average 1918-1922: cells give 8470674.80, printed 8670674 (difference 199999.20)
  - sgt1922 p.215 (f239) crops_d olive_bearing: average 1913-1922: cells give 8055359.90, printed 8155359 (difference 99999.10)
  - sgt1922 p.215 (f239) crops_d olive_pomace: average 1913-1917: cells give 36447.60, printed 20160 (difference -16287.60)
  - sgt1922 p.215 (f239) crops_d olive_pomace: average 1913-1922: cells give 38073.80, printed 29930 (difference -8143.80)
  - sgt1923 p.223 (f725) crops_a barley_area: average 1914-1918: cells give 463473.40, printed 475473 (difference 11999.60)
  - sgt1923 p.223 (f725) crops_a barley_area: average 1914-1923: cells give 442473.40, printed 448473 (difference 5999.60)
  - sgt1923 p.225 (f727) crops_b potatoes_prod: average 1919-1923: cells give 40500.00, printed 40400 (difference -100.00)
  - sgt1923 p.227 (f729) crops_d otherdates_trees: average 1919-1923: cells give 974859.20, printed 774859 (difference -200000.20)
  - sgt1923 p.227 (f729) crops_d otherdates_prod: average 1919-1923: cells give 357200.00, printed 377200 (difference 20000.00)
  - sgt1923 p.227 (f729) crops_d otherdates_prod: average 1914-1923: cells give 306962.00, printed 316962 (difference 10000.00)
  - sgt1924 p.231 (f1221) crops_a durum_prod: average 1920-1924: cells give 1734700.00, printed 1474700 (difference -260000.00)
  - sgt1924 p.231 (f1221) crops_a durum_prod: average 1915-1924: cells give 1802710.00, printed 1672710 (difference -130000.00)
  - sgt1924 p.231 (f1221) crops_a maize_area: average 1920-1924: cells give 14662.00, printed 16652 (difference 1990.00)
  - sgt1924 p.231 (f1221) crops_a maize_area: average 1915-1924: cells give 16407.10, printed 17402 (difference 994.90)
  - sgt1924 p.233 (f1223) crops_b chickpeas_prod: average 1920-1924: cells give 16540.00, printed 16500 (difference -40.00)
  - sgt1924 p.235 (f1225) crops_d almond_prod: average 1915-1919: cells give 20960.00, printed 20900 (difference -60.00)
  - sgt1924 p.235 (f1225) crops_d degla_prod: average 1920-1924: cells give 15460.00, printed 15400 (difference -60.00)
  - sgt1924 p.235 (f1225) crops_d degla_prod: average 1915-1924: cells give 13830.00, printed 13800 (difference -30.00)
  - sgt1925 p.267 (f291) crops_a durum_area: average 1916-1920: cells give 297950.00, printed 293950 (difference -4000.00)
  - sgt1925 p.267 (f291) crops_a durum_area: average 1921-1925: cells give 278577.80, printed 318577 (difference 39999.20)
  - sgt1925 p.267 (f291) crops_a durum_area: average 1916-1925: cells give 288263.90, printed 306263 (difference 17999.10)
  - sgt1925 p.267 (f291) crops_a maize_prod: average 1916-1920: cells give 54462.00, printed 54862 (difference 400.00)
  - sgt1925 p.267 (f291) crops_a maize_prod: average 1916-1925: cells give 53022.00, printed 53222 (difference 200.00)
  - sgt1925 p.271 (f295) crops_b chickpeas_area: average 1916-1920: cells give 5577.40, printed 5977 (difference 399.60)
  - sgt1925 p.271 (f295) crops_b chickpeas_area: average 1916-1925: cells give 5104.40, printed 5304 (difference 199.60)
  - sgt1925 p.271 (f295) crops_c flax_prod: average 1921-1925: cells give 7740.00, printed 7540 (difference -200.00)
  - sgt1925 p.271 (f295) crops_c flax_prod: average 1916-1925: cells give 9130.00, printed 9020 (difference -110.00)
  - sgt1925 p.271 (f295) crops_c tobacco_prod: average 1921-1925: cells give 4167.00, printed 3987 (difference -180.00)
  - sgt1925 p.271 (f295) crops_c tobacco_prod: average 1916-1925: cells give 3212.10, printed 3122.2 (difference -89.90)
  - sgt1925 p.273 (f297) crops_d carob_trees: average 1921-1925: cells give 20540.00, printed 20400 (difference -140.00)
  - sgt1925 p.273 (f297) crops_d carob_trees: average 1916-1925: cells give 20270.00, printed 20200 (difference -70.00)
  - sgt1925 p.273 (f297) crops_d carob_prod: average 1916-1920: cells give 10460.00, printed 10200 (difference -260.00)
  - sgt1925 p.273 (f297) crops_d carob_prod: average 1916-1925: cells give 14730.00, printed 14600 (difference -130.00)
  - sgt1925 p.273 (f297) crops_d almond_prod: average 1916-1920: cells give 23520.00, printed 20300 (difference -3220.00)
  - sgt1925 p.273 (f297) crops_d almond_prod: average 1921-1925: cells give 20300.00, printed 23520 (difference 3220.00)
  - sgt1925 p.273 (f297) crops_d degla_prod: average 1916-1920: cells give 13600.00, printed 15600 (difference 2000.00)
  - sgt1925 p.273 (f297) crops_d degla_prod: average 1916-1925: cells give 14830.00, printed 15830 (difference 1000.00)
  - sgt1925 p.273 (f297) crops_d otherdates_prod: average 1916-1925: cells give 348300.00, printed 345800 (difference -2500.00)
  - sgt1925 p.273 (f297) crops_d orange_prod: average 1921-1925: cells give 14320.00, printed 14800 (difference 480.00)
  - sgt1925 p.273 (f297) crops_d orange_prod: average 1916-1925: cells give 13960.00, printed 14200 (difference 240.00)
  - sgt1925 p.273 (f297) crops_d lemon_trees: average 1916-1920: cells give 50500.00, printed 50120 (difference -380.00)
  - sgt1925 p.273 (f297) crops_d lemon_trees: average 1916-1925: cells give 51250.00, printed 51060 (difference -190.00)
  - sgt1926 p.243 (f807) crops_a durum_prod: average 1917-1926: cells give 1855650.00, printed 1885650 (difference 30000.00)
  - sgt1926 p.245 (f809) crops_b potatoes_prod: average 1922-1926: cells give 41480.00, printed 43480 (difference 2000.00)
  - sgt1926 p.245 (f809) crops_b potatoes_prod: average 1917-1926: cells give 40990.00, printed 41990 (difference 1000.00)
  - sgt1926 p.247 (f811) crops_d olive_trees: average 1917-1921: cells give 12153890.40, printed 12193890 (difference 39999.60)
  - sgt1926 p.247 (f811) crops_d olive_pomace: average 1922-1926: cells give 32600.00, printed 32200 (difference -400.00)
  - sgt1926 p.247 (f811) crops_d olive_pomace: average 1917-1926: cells give 36150.00, printed 35950 (difference -200.00)
  - sgt1927 p.235 (f263) crops_a soft_area: average 1918-1922: cells give 47893.20, printed 239466 (difference 191572.80)
  - sgt1927 p.235 (f263) crops_a barley_area: average 1918-1927: cells give 440408.00, printed 420408 (difference -20000.00)
  - sgt1927 p.235 (f263) crops_a oats_area: average 1918-1922: cells give 59947.00, printed 603347 (difference 543400.00)
  - sgt1927 p.235 (f263) crops_a oats_area: average 1923-1927: cells give 42326.60, printed 37561 (difference -4765.60)
  - sgt1927 p.235 (f263) crops_a oats_area: average 1918-1927: cells give 51136.80, printed 51336 (difference 199.20)
  - sgt1927 p.237 (f265) crops_b chickpeas_area: average 1918-1922: cells give 5580.60, printed 5460 (difference -120.60)
  - sgt1927 p.237 (f265) crops_b chickpeas_area: average 1918-1927: cells give 5619.20, printed 5559 (difference -60.20)
  - sgt1927 p.237 (f265) crops_c flax_area: average 1918-1927: cells give 2620.70, printed 1685 (difference -935.70)
  - sgt1927 p.237 (f265) crops_c tobacco_prod: average 1923-1927: cells give 4410.80, printed 4510 (difference 99.20)
  - sgt1927 p.239 (f267) crops_d vine_grapes: average 1918-1922: cells give 47800.00, printed 48200 (difference 400.00)
  - sgt1927 p.239 (f267) crops_d vine_grapes: average 1918-1927: cells give 50900.00, printed 51100 (difference 200.00)
  - sgt1927 p.239 (f267) crops_d olive_trees: average 1923-1927: cells give 15861830.20, printed 1586183 (difference -14275647.20)
  - sgt1927 p.239 (f267) crops_d degla_trees: average 1923-1927: cells give 65834.20, printed 62834 (difference -3000.20)
  - sgt1927 p.239 (f267) crops_d degla_trees: average 1918-1927: cells give 62185.00, printed 60685 (difference -1500.00)
  - sgt1928 p.235 (f787) crops_a durum_prod: average 1919-1928: cells give 1882350.00, printed 1860350 (difference -22000.00)
  - sgt1928 p.235 (f787) crops_a barley_area: average 1919-1928: cells give 442064.50, printed 432064 (difference -10000.50)
  - sgt1928 p.235 (f787) crops_a maize_area: average 1924-1928: cells give 17470.20, printed 17670 (difference 199.80)
  - sgt1928 p.235 (f787) crops_a maize_area: average 1919-1928: cells give 16257.30, printed 16157 (difference -100.30)
  - sgt1928 p.237 (f789) crops_b chickpeas_area: average 1924-1928: cells give 6046.80, printed 6246 (difference 199.20)
  - sgt1928 p.237 (f789) crops_b chickpeas_area: average 1919-1928: cells give 5588.50, printed 5688 (difference 99.50)
  - sgt1928 p.237 (f789) crops_b potatoes_area: average 1924-1928: cells give 1070.00, printed 1050 (difference -20.00)
  - sgt1928 p.237 (f789) crops_b potatoes_area: average 1919-1928: cells give 1033.00, printed 1023 (difference -10.00)
  - sgt1928 p.237 (f789) crops_b potatoes_prod: average 1924-1928: cells give 40480.00, printed 40880 (difference 400.00)
  - sgt1928 p.237 (f789) crops_c flax_area: average 1924-1928: cells give 2550.20, printed 2556 (difference 5.80)
  - sgt1928 p.237 (f789) crops_c tobacco_area: average 1919-1923: cells give 303.80, printed 803 (difference 499.20)
  - sgt1928 p.237 (f789) crops_c tobacco_prod: average 1919-1923: cells give 3469.00, printed 3669 (difference 200.00)
  - sgt1928 p.239 (f791) crops_d orange_trees: average 1924-1928: cells give 67960.00, printed 69960 (difference 2000.00)
  - sgt1928 p.239 (f791) crops_d orange_trees: average 1919-1928: cells give 66720.00, printed 67720 (difference 1000.00)
  - sgt1929 p.241 (f269) crops_d orange_prod: average 1925-1929: cells give 14340.00, printed 12340 (difference -2000.00)
  - sgt1929 p.241 (f269) crops_d orange_prod: average 1920-1929: cells give 14310.00, printed 13310 (difference -1000.00)
  - sgt1929 p.241 (f269) crops_d lemon_prod: average 1925-1929: cells give 8300.00, printed 8100 (difference -200.00)
  - sgt1930 p.241 (f799) crops_a durum_area: average 1926-1930: cells give 649848.20, printed 651448 (difference 1599.80)
  - sgt1930 p.245 (f803) crops_d orange_trees: average 1926-1930: cells give 61509.80, printed 75709 (difference 14199.20)
  - sgt1930 p.245 (f803) crops_d orange_trees: average 1921-1930: cells give 64324.90, printed 71424 (difference 7099.10)

- Overlapping printings: 3288 cell comparisons with other editions printing the same cell; 55 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1919 / tunisia / durum_wheat / area | sgt1922 | 514861 | sgt1928 | 513110 |
| 1919 / tunisia / durum_wheat / area | sgt1923 | 514861 | sgt1928 | 513110 |
| 1919 / tunisia / durum_wheat / area | sgt1924 | 514861 | sgt1928 | 513110 |
| 1920 / tunisia / durum_wheat / area | sgt1922 | 481766 | sgt1929 | 481786 |
| 1920 / tunisia / durum_wheat / area | sgt1923 | 481766 | sgt1929 | 481786 |
| 1920 / tunisia / durum_wheat / area | sgt1924 | 481766 | sgt1929 | 481786 |
| 1921 / tunisia / durum_wheat / area | sgt1922 | 566609 | sgt1930 | 570031 |
| 1921 / tunisia / durum_wheat / area | sgt1923 | 566609 | sgt1930 | 570031 |
| 1921 / tunisia / durum_wheat / area | sgt1924 | 566609 | sgt1930 | 570031 |
| 1918 / tunisia / durum_wheat / production | sgt1922 | 2693600 | sgt1927 | 2693000 |
| 1918 / tunisia / durum_wheat / production | sgt1923 | 2693600 | sgt1927 | 2693000 |
| 1918 / tunisia / durum_wheat / production | sgt1924 | 2693600 | sgt1927 | 2693000 |
| 1921 / tunisia / barley / area | sgt1922 | 497046 | sgt1930 | 497828 |
| 1921 / tunisia / barley / area | sgt1923 | 497046 | sgt1930 | 497828 |
| 1921 / tunisia / barley / area | sgt1924 | 497046 | sgt1930 | 497828 |
| 1921 / tunisia / oats / area | sgt1922 | 64146 | sgt1930 | 66646 |
| 1921 / tunisia / oats / area | sgt1923 | 64146 | sgt1930 | 66646 |
| 1921 / tunisia / oats / area | sgt1924 | 64146 | sgt1930 | 66646 |
| 1921 / tunisia / maize_sorghum / area | sgt1922 | 22161 | sgt1930 | 22177 |
| 1921 / tunisia / maize_sorghum / area | sgt1923 | 22161 | sgt1930 | 22177 |
| 1921 / tunisia / maize_sorghum / area | sgt1924 | 22161 | sgt1930 | 22177 |
| 1921 / tunisia / broad_beans / area | sgt1922 | 23477 | sgt1930 | 23513 |
| 1921 / tunisia / broad_beans / area | sgt1923 | 23477 | sgt1930 | 23513 |
| 1921 / tunisia / broad_beans / area | sgt1924 | 23477 | sgt1930 | 23513 |
| 1921 / tunisia / broad_beans / area | sgt1925 | 23477 | sgt1930 | 23513 |
| 1921 / tunisia / chickpeas / area | sgt1922 | 6954 | sgt1930 | 6980 |
| 1921 / tunisia / chickpeas / area | sgt1923 | 6954 | sgt1930 | 6980 |
| 1921 / tunisia / chickpeas / area | sgt1924 | 6954 | sgt1930 | 6980 |
| 1921 / tunisia / chickpeas / area | sgt1925 | 6954 | sgt1930 | 6980 |
| 1921 / tunisia / flax / area | sgt1922 | 3715 | sgt1930 | 3730 |
| 1921 / tunisia / flax / area | sgt1923 | 3715 | sgt1930 | 3730 |
| 1921 / tunisia / flax / area | sgt1924 | 3715 | sgt1930 | 3730 |
| 1921 / tunisia / flax / area | sgt1925 | 3715 | sgt1930 | 3730 |
| 1922 / tunisia / flax / area | sgt1922 | 1939 | sgt1930 | 1962 |
| 1922 / tunisia / flax / area | sgt1923 | 1939 | sgt1930 | 1962 |
| 1922 / tunisia / flax / area | sgt1924 | 1939 | sgt1930 | 1962 |
| 1922 / tunisia / flax / area | sgt1925 | 1939 | sgt1930 | 1962 |
| 1923 / tunisia / durum_wheat / area | sgt1923 | 598977 | sgt1930 | 598997 |
| 1923 / tunisia / durum_wheat / area | sgt1924 | 598977 | sgt1930 | 598997 |
| 1924 / tunisia / durum_wheat / area | sgt1924 | 417607 | sgt1930 | 433139 |
| 1924 / tunisia / durum_wheat / production | sgt1924 | 2350000 | sgt1930 | 1040000 |
| 1924 / tunisia / soft_wheat / production | sgt1924 | 360000 | sgt1930 | 360140 |
| 1924 / tunisia / maize_sorghum / area | sgt1924 | 16465 | sgt1930 | 16645 |
| 1925 / tunisia / vine / area | sgt1925 | 30213 | sgt1930 | 27986 |
| 1925 / tunisia / dates_other / trees | sgt1925 | 1030473 | sgt1930 | 1138283 |
| 1927 / tunisia / durum_wheat / production | sgt1927 | 1800000 | sgt1930 | 1760000 |
| 1927 / tunisia / soft_wheat / production | sgt1927 | 450000 | sgt1930 | 440000 |
| 1927 / tunisia / barley / production | sgt1927 | 900800 | sgt1930 | 895000 |
| 1928 / tunisia / durum_wheat / production | sgt1928 | 2850000 | sgt1930 | 3230000 |
| 1928 / tunisia / soft_wheat / production | sgt1928 | 450000 | sgt1930 | 500000 |
| 1928 / tunisia / barley / production | sgt1928 | 2750000 | sgt1930 | 2700000 |
| 1928 / tunisia / oats / production | sgt1928 | 325000 | sgt1930 | 445000 |
| 1928 / tunisia / maize_sorghum / production | sgt1928 | 68000 | sgt1930 | 65000 |
| 1935 / tunisia / olive / trees_bearing | sgt1935 | 11581001 | sgt1936 | 12581001 |
| 1935 / tunisia / dates_other / trees | sgt1935 | 1285304 | sgt1936 | 1284789 |

- Flagged cells: derived_from_totals: 1, illegible: 1, total_mismatch: 2.

  - sgt1925 p.267 1925 north / a / durum_wheat / area / hectares = 129774 (total_mismatch)
  - sgt1930 p.244 1925 tunisia / d / dates_other / production / quintals = 352000 (derived_from_totals)
  - sgt1930 p.245 1930 tunisia / d / orange / trees / trees = 19000 (total_mismatch)
  - sgt1939 p.98 1938 tunisia / d / pear / trees / trees = NA (illegible)

## Image versus OCR

- Read cell by cell on the page images (87 printings): sgt1922 f234, sgt1922 f235, sgt1922 f236, sgt1922 f237, sgt1922 f236, sgt1922 f237, sgt1922 f238, sgt1922 f239, sgt1923 f724, sgt1923 f725, sgt1923 f726, sgt1923 f727, sgt1923 f726, sgt1923 f727, sgt1923 f728, sgt1923 f729, sgt1924 f1220, sgt1924 f1221, sgt1924 f1222, sgt1924 f1223, sgt1924 f1222, sgt1924 f1223, sgt1924 f1224, sgt1924 f1225, sgt1925 f290, sgt1925 f291, sgt1925 f292, sgt1925 f293, sgt1925 f294, sgt1925 f295, sgt1925 f294, sgt1925 f295, sgt1925 f296, sgt1925 f297, sgt1926 f806, sgt1926 f807, sgt1926 f808, sgt1926 f809, sgt1926 f808, sgt1926 f809, sgt1926 f810, sgt1926 f811, sgt1927 f262, sgt1927 f263, sgt1927 f264, sgt1927 f265, sgt1927 f264, sgt1927 f265, sgt1927 f266, sgt1927 f267, sgt1928 f786, sgt1928 f787, sgt1928 f788, sgt1928 f789, sgt1928 f788, sgt1928 f789, sgt1928 f790, sgt1928 f791, sgt1929 f264, sgt1929 f265, sgt1929 f266, sgt1929 f267, sgt1929 f266, sgt1929 f267, sgt1929 f268, sgt1929 f269, sgt1930 f798, sgt1930 f799, sgt1930 f800, sgt1930 f801, sgt1930 f800, sgt1930 f801, sgt1930 f802, sgt1930 f803, sgt1935 f142, sgt1935 f143, sgt1935 f143, sgt1935 f144, sgt1936 f103, sgt1936 f104, sgt1936 f104, sgt1936 f105, sgt1939 f101, sgt1939 f102, sgt1939 f102, sgt1939 f103, sgt1939 f104.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
