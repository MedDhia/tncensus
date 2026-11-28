# Mercuriales

*Market prices (mercuriales): monthly minimum, maximum and average prices.*

Source: *Statistique générale de la Tunisie*, chapter *Commerce et navigation*, editions sgt1922, sgt1923, sgt1924. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 392, f416, p. 393, f417, p. 394, f418, p. 395, f419, p. 396, f420, p. 397, f421; sgt1923 (`bpt6k9105649x`): p. 404, f906, p. 405, f907, p. 406, f908, p. 407, f909, p. 408, f910, p. 409, f911; sgt1924 (`bpt6k9105649x`): p. 420, f1410, p. 421, f1411, p. 422, f1412, p. 423, f1413, p. 424, f1414, p. 425, f1415.

Transcriptions: `../transcribed/commerce_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_commerce.py build`.

Rows: 4032. Years: 1922, 1923, 1924.

Unit: francs (with centimes) per unit as printed (see `unit`). value_type: francs.

Selection: each edition prints a single year (its reference year); no overlap, all stored.

## Columns

- `census`: edition (each prints one year, its reference year; no overlap)
- `table_id`: `prices_live`, `prices_retail`, `prices_animal_products`, `prices_cereals`, `prices_oils`, `prices_wine` (sub-tables of *Mercuriales*)
- `gallica_ark`: Gallica volume ark
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: reference year of the edition (not printed in the heading: 1922, 1923, 1924)
- `month`: month, 1-12 (printed Janvier ... Décembre)
- `market`: `tunis`, `sousse`, `sfax`
- `market_fr`: as printed (Place de ...)
- `product`: product code (live animal, cut of meat, hide, cereal, oil, wine)
- `product_fr`: column headings as printed, joined with commas
- `measure`: `minimum`, `maximum`, `average` (retail meat: average only)
- `measure_fr`: column heading as printed (retail meat: prix moyen mensuel)
- `unit`: `francs_per_kilogram`, `francs_per_quintal`, `francs_per_piece`, `francs_per_hundred` (eggs), `francs_per_degree`, `francs_per_hectolitre` (wine), as printed
- `value`: price in francs, with centimes (printed '1 35' = 1.35; » in the centimes column = .00)
- `flag`: empty or `not_applicable` (printed — (1) *Aucune transaction* / *Sans affaires*)

Market prices (*Mercuriales*) for the reference year of each edition (the heading prints no year: sgt1922 1922, sgt1923 1923, sgt1924 1924; consecutive editions do not overlap). Sub-tables (table_id): `prices_live` *Animaux (Viande sur pied et viande abattue)*, live weight per kg, minimum / maximum / moyen; `prices_retail` *Prix moyen mensuel du kilogr. de viande au détail par catégories et par espèces* (beef, veal, mutton, pork by cut and category; one monthly average per cut); `prices_animal_products` *Dépouilles et produits animaux* (cattle hides per quintal, sheep and goat skins per piece, greasy wool per quintal, eggs per hundred); `prices_cereals` *Céréales* (prices per quintal: the unit is not printed in this sub-table; stored as `francs_per_quintal`, the usual unit of the Tunis cereal market and consistent with the magnitudes); `prices_oils` *Huiles végétales* a) Tunis, b) Sousse, c) Sfax, per quintal; `prices_wine` *Vins*, Tunis, per degree and (sgt1922 only) per hectolitre. All markets are *Place de Tunis* unless stated (`market`).

Content differs between editions: sgt1922 prints live veal, eggs, chickpeas and the wine price per hectolitre; sgt1923 and sgt1924 do not (their live-animal table has beef, mutton and pork; the beef 'moyen' column lies against the binding and is repeated, cut, at the edge of the facing page). Products are stored only for the editions that print them.

Values: francs with centimes ('1 35' = 1,35; '2 »' = 2,00), stored with two decimals. A dash with footnote (1) *Aucune transaction* / *Sans affaires* (sgt1922), or a lone » with footnote (») *Aucune transaction* / *Sans affaires* (sgt1923, sgt1924), means no transaction that month: stored empty, flag `not_applicable`. Daris (white sorghum): every edition prints the three headings as *maximum | minimum | moyenne*, but the first column is always the lower; stored as `minimum` / `maximum` by position, `measure_fr` keeping the printed heading.

Gutter cells (binding): sgt1923 beef live average November and cattle-hide average September and November: centimes cut, stored empty with flag `illegible`; sgt1923 retail veal *longes* (2e catégorie): the whole column lies in the binding (only the » of some centimes visible), stored `illegible`. sgt1923 oats minimum: the tens digit is partly cut; read from its visible remnant, each reading agreeing with the printed maximum and average. The remaining gutter columns (sgt1922 veal carrés / longes, oats and maize; sgt1923 veal carrés, barley average; sgt1924 veal carrés, barley average) were read on the crops of both facing pages.

Checks: on every line with minimum, maximum and average, minimum <= average <= maximum (the average is not always the midpoint, so no stricter check is made). Explanation of the failed checks (all cells re-read on native-resolution crops; the printed values are kept): sgt1922 Sfax masri lampante February, average printed 236,25 between 202,50 and 210 (probably 206,25); sgt1922 cattle hides August, maximum printed 48 (probably 248); sgt1923 daris November, average 58,75 below the minimum 59,25 (probably 59,75); sgt1923 durum wheat July average 71,35 (74,80-77,90, probably 76,35) and September average 79,10 (71,25-77; probably 74,10); sgt1923 greasy wool September, average 453,75 (463,75-543,75, probably 503,75); sgt1923 Tunis first-pressing oil October, average 349,35 (475-483,75, probably 479,35); sgt1924 Sfax second-pressing oil April, average 675,30 above the maximum 673,10 (probably 670,30); sgt1924 barley May, average 68,50 (57,50-59,50, probably 58,50); sgt1924 cattle hides September, average 568,75 above the maximum 537,50 (the minimum 400 or the average is misprinted; not decidable); sgt1924 soft wheat December, maximum printed '1 31' (hundreds digit missing). The two cells printed with the hundreds digit missing are flagged `total_mismatch`: sgt1924 durum_wheat month 12 min: printed '1 38'; the maximum 146,25 and average 142,10 imply 138; sgt1924 soft_wheat month 12 max: printed '1 31'; the minimum 125,50 and average 128,25 imply 131 (the first passes the check only because 1,38 is below the average). Not caught by the check: sgt1922 Tunis masri lampante June maximum printed 843,75 (minimum 335, average 339,35; probably 343,75), kept as printed.

The Gallica OCR was used only as a cross-check (it renders » and the centimes column unreliably).

Survey of the whole chapter: `commerce_survey.md`.

## Validation

- Checks against printed totals and identities: 988; passed: 977; failed: 11.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 f421 sfax oil_masri_lampante month 2: minimum <= average <= maximum: printed 202.50, 236.25, 210.00
  - sgt1922 f418 tunis cattle_hides month 8: minimum <= average <= maximum: printed 218.00, 233.00, 48.00
  - sgt1923 f909 tunis daris month 11: minimum <= average <= maximum: printed 59.25, 58.75, 60.25
  - sgt1923 f908 tunis durum_wheat month 7: minimum <= average <= maximum: printed 74.80, 71.35, 77.90
  - sgt1923 f908 tunis durum_wheat month 9: minimum <= average <= maximum: printed 71.25, 79.10, 77.00
  - sgt1923 f909 tunis greasy_wool month 9: minimum <= average <= maximum: printed 463.75, 453.75, 543.75
  - sgt1923 f910 tunis oil_first_press month 10: minimum <= average <= maximum: printed 475.00, 349.35, 483.75
  - sgt1924 f1415 sfax oil_second_press month 4: minimum <= average <= maximum: printed 667.50, 675.30, 673.10
  - sgt1924 f1412 tunis barley month 5: minimum <= average <= maximum: printed 57.50, 68.50, 59.50
  - sgt1924 f1412 tunis cattle_hides month 9: minimum <= average <= maximum: printed 400.00, 568.75, 537.50
  - sgt1924 f1412 tunis soft_wheat month 12: minimum <= average <= maximum: printed 125.50, 128.25, 1.31

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: illegible: 15, not_applicable: 123, total_mismatch: 2.

  - sgt1922 p.395 1922 7 / tunis / daris / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.395 1922 7 / tunis / daris / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.395 1922 7 / tunis / daris / average / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.395 1922 8 / tunis / daris / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.395 1922 8 / tunis / daris / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.395 1922 8 / tunis / daris / average / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.396 1922 8 / sousse / olive_oil_second_pressing / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.396 1922 8 / sousse / olive_oil_second_pressing / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.396 1922 8 / sousse / olive_oil_second_pressing / average / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.396 1922 9 / sousse / olive_oil_second_pressing / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.396 1922 9 / sousse / olive_oil_second_pressing / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.396 1922 9 / sousse / olive_oil_second_pressing / average / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.396 1922 1 / sousse / pomace_oil / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.396 1922 1 / sousse / pomace_oil / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.396 1922 1 / sousse / pomace_oil / average / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.396 1922 2 / sousse / pomace_oil / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.396 1922 2 / sousse / pomace_oil / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.396 1922 2 / sousse / pomace_oil / average / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.397 1922 6 / sfax / olive_oil_second_pressing / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.397 1922 6 / sfax / olive_oil_second_pressing / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.397 1922 6 / sfax / olive_oil_second_pressing / average / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.397 1922 7 / sfax / olive_oil_second_pressing / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.397 1922 7 / sfax / olive_oil_second_pressing / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.397 1922 7 / sfax / olive_oil_second_pressing / average / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.397 1922 8 / sfax / olive_oil_second_pressing / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.397 1922 8 / sfax / olive_oil_second_pressing / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.397 1922 8 / sfax / olive_oil_second_pressing / average / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.397 1922 9 / sfax / olive_oil_second_pressing / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.397 1922 9 / sfax / olive_oil_second_pressing / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.397 1922 9 / sfax / olive_oil_second_pressing / average / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.397 1922 10 / sfax / olive_oil_masri_lampante / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.397 1922 10 / sfax / olive_oil_masri_lampante / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1922 p.397 1922 10 / sfax / olive_oil_masri_lampante / average / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.404 1923 11 / tunis / beef_live / average / francs_per_kilogram = NA (illegible)
  - sgt1923 p.405 1923 1 / tunis / veal_loin / average / francs_per_kilogram = NA (illegible)
  - sgt1923 p.405 1923 2 / tunis / veal_loin / average / francs_per_kilogram = NA (illegible)
  - sgt1923 p.405 1923 3 / tunis / veal_loin / average / francs_per_kilogram = NA (illegible)
  - sgt1923 p.405 1923 4 / tunis / veal_loin / average / francs_per_kilogram = NA (illegible)
  - sgt1923 p.405 1923 5 / tunis / veal_loin / average / francs_per_kilogram = NA (illegible)
  - sgt1923 p.405 1923 6 / tunis / veal_loin / average / francs_per_kilogram = NA (illegible)
  - sgt1923 p.405 1923 7 / tunis / veal_loin / average / francs_per_kilogram = NA (illegible)
  - sgt1923 p.405 1923 8 / tunis / veal_loin / average / francs_per_kilogram = NA (illegible)
  - sgt1923 p.405 1923 9 / tunis / veal_loin / average / francs_per_kilogram = NA (illegible)
  - sgt1923 p.405 1923 10 / tunis / veal_loin / average / francs_per_kilogram = NA (illegible)
  - sgt1923 p.405 1923 11 / tunis / veal_loin / average / francs_per_kilogram = NA (illegible)
  - sgt1923 p.405 1923 12 / tunis / veal_loin / average / francs_per_kilogram = NA (illegible)
  - sgt1923 p.406 1923 9 / tunis / cattle_hides / average / francs_per_quintal = NA (illegible)
  - sgt1923 p.406 1923 11 / tunis / cattle_hides / average / francs_per_quintal = NA (illegible)
  - sgt1923 p.406 1923 3 / tunis / soft_wheat / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.406 1923 3 / tunis / soft_wheat / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.406 1923 3 / tunis / soft_wheat / average / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.406 1923 4 / tunis / soft_wheat / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.406 1923 4 / tunis / soft_wheat / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.406 1923 4 / tunis / soft_wheat / average / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.406 1923 5 / tunis / soft_wheat / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.406 1923 5 / tunis / soft_wheat / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.406 1923 5 / tunis / soft_wheat / average / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 5 / tunis / oats / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 5 / tunis / oats / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 5 / tunis / oats / average / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 5 / tunis / maize / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 5 / tunis / maize / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 5 / tunis / maize / average / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 6 / tunis / maize / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 6 / tunis / maize / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 6 / tunis / maize / average / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 7 / tunis / maize / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 7 / tunis / maize / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 7 / tunis / maize / average / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 8 / tunis / maize / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 8 / tunis / maize / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 8 / tunis / maize / average / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 5 / tunis / daris / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 5 / tunis / daris / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 5 / tunis / daris / average / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 6 / tunis / daris / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 6 / tunis / daris / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 6 / tunis / daris / average / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 7 / tunis / daris / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 7 / tunis / daris / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 7 / tunis / daris / average / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 8 / tunis / daris / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 8 / tunis / daris / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 8 / tunis / daris / average / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 3 / tunis / broad_beans / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 3 / tunis / broad_beans / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 3 / tunis / broad_beans / average / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 4 / tunis / broad_beans / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 4 / tunis / broad_beans / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 4 / tunis / broad_beans / average / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 5 / tunis / broad_beans / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 5 / tunis / broad_beans / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 5 / tunis / broad_beans / average / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 4 / tunis / linseed / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 4 / tunis / linseed / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.407 1923 4 / tunis / linseed / average / francs_per_quintal = NA (not_applicable)
  - sgt1923 p.409 1923 8 / tunis / white_wine / minimum / francs_per_degree = NA (not_applicable)
  - sgt1923 p.409 1923 8 / tunis / white_wine / maximum / francs_per_degree = NA (not_applicable)
  - sgt1923 p.409 1923 8 / tunis / white_wine / average / francs_per_degree = NA (not_applicable)
  - sgt1924 p.422 1924 12 / tunis / durum_wheat / minimum / francs_per_quintal = 1.38 (total_mismatch)
  - sgt1924 p.422 1924 12 / tunis / soft_wheat / maximum / francs_per_quintal = 1.31 (total_mismatch)
  - sgt1924 p.423 1924 6 / tunis / maize / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1924 p.423 1924 6 / tunis / maize / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1924 p.423 1924 6 / tunis / maize / average / francs_per_quintal = NA (not_applicable)
  - sgt1924 p.423 1924 7 / tunis / maize / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1924 p.423 1924 7 / tunis / maize / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1924 p.423 1924 7 / tunis / maize / average / francs_per_quintal = NA (not_applicable)
  - sgt1924 p.423 1924 6 / tunis / daris / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1924 p.423 1924 6 / tunis / daris / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1924 p.423 1924 6 / tunis / daris / average / francs_per_quintal = NA (not_applicable)
  - sgt1924 p.423 1924 7 / tunis / daris / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1924 p.423 1924 7 / tunis / daris / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1924 p.423 1924 7 / tunis / daris / average / francs_per_quintal = NA (not_applicable)
  - sgt1924 p.423 1924 8 / tunis / daris / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1924 p.423 1924 8 / tunis / daris / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1924 p.423 1924 8 / tunis / daris / average / francs_per_quintal = NA (not_applicable)
  - sgt1924 p.423 1924 3 / tunis / linseed / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1924 p.423 1924 3 / tunis / linseed / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1924 p.423 1924 3 / tunis / linseed / average / francs_per_quintal = NA (not_applicable)
  - sgt1924 p.423 1924 4 / tunis / linseed / minimum / francs_per_quintal = NA (not_applicable)
  - sgt1924 p.423 1924 4 / tunis / linseed / maximum / francs_per_quintal = NA (not_applicable)
  - sgt1924 p.423 1924 4 / tunis / linseed / average / francs_per_quintal = NA (not_applicable)
  - sgt1924 p.425 1924 6 / tunis / white_wine / minimum / francs_per_degree = NA (not_applicable)
  - sgt1924 p.425 1924 6 / tunis / white_wine / maximum / francs_per_degree = NA (not_applicable)
  - sgt1924 p.425 1924 6 / tunis / white_wine / average / francs_per_degree = NA (not_applicable)
  - sgt1924 p.425 1924 7 / tunis / white_wine / minimum / francs_per_degree = NA (not_applicable)
  - sgt1924 p.425 1924 7 / tunis / white_wine / maximum / francs_per_degree = NA (not_applicable)
  - sgt1924 p.425 1924 7 / tunis / white_wine / average / francs_per_degree = NA (not_applicable)
  - sgt1924 p.425 1924 8 / tunis / white_wine / minimum / francs_per_degree = NA (not_applicable)
  - sgt1924 p.425 1924 8 / tunis / white_wine / maximum / francs_per_degree = NA (not_applicable)
  - sgt1924 p.425 1924 8 / tunis / white_wine / average / francs_per_degree = NA (not_applicable)
  - sgt1924 p.425 1924 9 / tunis / white_wine / minimum / francs_per_degree = NA (not_applicable)
  - sgt1924 p.425 1924 9 / tunis / white_wine / maximum / francs_per_degree = NA (not_applicable)
  - sgt1924 p.425 1924 9 / tunis / white_wine / average / francs_per_degree = NA (not_applicable)
  - sgt1924 p.425 1924 11 / tunis / white_wine / minimum / francs_per_degree = NA (not_applicable)
  - sgt1924 p.425 1924 11 / tunis / white_wine / maximum / francs_per_degree = NA (not_applicable)
  - sgt1924 p.425 1924 11 / tunis / white_wine / average / francs_per_degree = NA (not_applicable)
  - sgt1924 p.425 1924 12 / tunis / white_wine / minimum / francs_per_degree = NA (not_applicable)
  - sgt1924 p.425 1924 12 / tunis / white_wine / maximum / francs_per_degree = NA (not_applicable)
  - sgt1924 p.425 1924 12 / tunis / white_wine / average / francs_per_degree = NA (not_applicable)

## Image versus OCR

- Read cell by cell on the page images (36 printings): sgt1922 f416, sgt1922 f417, sgt1922 f416, sgt1922 f417, sgt1922 f418, sgt1922 f419, sgt1922 f418, sgt1922 f419, sgt1922 f420, sgt1922 f420, sgt1922 f421, sgt1922 f421, sgt1923 f906, sgt1923 f907, sgt1923 f906, sgt1923 f907, sgt1923 f908, sgt1923 f909, sgt1923 f908, sgt1923 f909, sgt1923 f910, sgt1923 f910, sgt1923 f911, sgt1923 f911, sgt1924 f1410, sgt1924 f1411, sgt1924 f1410, sgt1924 f1411, sgt1924 f1412, sgt1924 f1413, sgt1924 f1412, sgt1924 f1413, sgt1924 f1414, sgt1924 f1414, sgt1924 f1415, sgt1924 f1415.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
