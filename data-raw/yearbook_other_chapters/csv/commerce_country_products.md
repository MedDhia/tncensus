# Relations commerciales avec les principaux pays de provenance et de destination

*Trade with the principal countries of provenance and destination, by product (quantity and value).*

Source: *Statistique générale de la Tunisie*, chapter *Commerce et navigation*, editions sgt1922. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 274, f298, p. 275, f299, p. 276, f300, p. 277, f301, p. 278, f302, p. 279, f303, p. 280, f304, p. 281, f305.

Transcriptions: `../transcribed/commerce_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_commerce.py build`.

Rows: 2740. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922.

Units: quantities in the unit printed in the UNITÉ column (Tête, Kilo, Quint = quintal métrique, Hect/Hecto = hectolitre, Pièce, Paire, Gr = gramme), never converted; values in francs. value_type: quantities and francs.

Selection (SPEC_ADDENDUM rule 4): each edition prints the last ten years; each year is stored once, from the latest edition printing it legibly (1913 from sgt1922, 1914 from sgt1923, 1915-1924 from sgt1924); every other printing of the same cell is compared and the differences listed below.

## Columns

- `census`: edition the value is taken from: the latest edition printing that year legibly (rule 4)
- `table_id`: `country_products` (Relations commerciales avec les principaux pays, by country)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: calendar year of the trade
- `country`: country of provenance (imports) or destination (exports), English
- `country_fr`: country as printed in the heading of the table
- `country_code`: short code (as in `commerce_trade_by_country`)
- `flow`: `import` or `export`
- `flow_fr`: as printed
- `product`: code derived from the printed line (ASCII slug of `product_fr`)
- `product_fr`: line as printed (ditto marks of the line heading expanded); no nomenclature number is printed in these tables
- `measure`: `quantity` or `value`
- `measure_fr`: quantité / valeur
- `unit`: unit as printed in the UNITÉ column (its ditto marks resolved), `francs` for values
- `value`: as printed; » stored as 0
- `flag`: empty or `illegible` (see notes)

Each country occupies two spreads per flow: the even view prints the product lines (grouped under Animaux et produits animaux, Produits végétaux, Produits minéraux, Fabrications; the group headings are not stored), the UNITÉ column and the quantities for ten years; the odd view the values in francs for the same lines and, at the end of each flow, a TOTAUX line of the values. TOTAUX is not stored: it is checked against the sum of the product values and against the country line of `commerce_trade_by_country` (same edition). No quantity total is printed (units differ). No nomenclature number is printed, so no `product_no` column is given; `product` is a code derived from the printed line.

Gutter. The quantity of the last year of each edition lies against the binding: its right-hand digits are hidden on both facing views (the last digit of a value such as 291.00- is lost), so every last-year quantity is typed `?` (flag `illegible`) except where » is printed. The value columns are legible.

sgt1922 France importations: the 1913 column adds to TOTAUX exactly; the other years leave residuals (sum of lines minus TOTAUX: 1914 -500, 1915 +50, 1916 -20.100, 1917 -55, 1918 -10.210, 1919 -33.600, 1920 +9.890.402, 1921 +87.295). Every value of the 1915-1917 and 1920-1921 columns was re-read on zoomed native-resolution crops and stands as transcribed, and the Gallica OCR shows no competing reading, so the residuals are in the printed table; nothing is flagged. The 1922 value of *Espèces médicinales* has a broken first digit (?58.567) and is typed `?`; the 1922 TOTAUX leaves 3.568.667 for it, which no reading of the visible digits gives, so it is not derived. Every TOTAUX equals the France import line of `commerce_trade_by_country`. *Eaux minérales* 1919 prints 254.188 hl against 293.368 francs (unit value far below the other years) and *Tissus de soie* 1920 426 quintals against 9.707.195 francs: printed values kept, not flagged (no check covers quantities).

sgt1922 France exportations: TOTAUX is reprinted unchanged by sgt1923 and sgt1924 (Gallica OCR of f795 and f1299) but differs from the France export line of `commerce_trade_by_country` in 1915 (62.782.418 against 62.182.418), 1916 (51.904.159 against 51.994.059) and 1919 (120.932.134 against 129.932.134), so the two tables of the same edition disagree in print. The product values match TOTAUX in 1922 exactly and in 1917 within 2 francs; the other years leave residuals (sum of lines minus TOTAUX: 1913 +59.997, 1914 +1.754.372, 1915 -499.909, 1916 +10.215.526, 1918 -50.590, 1919 +14.432.181, 1920 -358.000). The 1913-1916 and 1919 columns of f303 and f305 were re-read on zoomed native-resolution crops and stand as transcribed; most of the f305 values are confirmed by the later printings' OCR (not used for values). *Vins ordinaires* 1916 (11.403.490 francs for 46.779 hl, against 1.783.850 for 59.461 hl in 1915) would explain 10.000.000 of the 1916 residual if read 1.403.490, but it is printed so in all three editions' OCR and is not flagged; no single cell explains the other residuals. *Vins de liqueur* 1921: the second digit is broken (3.?60), typed `?`; TOTAUX implies about 3.360 (residual of 1 franc), not derived. *Poissons frais* 1913-1915 print the same figure as quantity (kilo) and value.

Survey of the whole chapter: `commerce_survey.md`.

## Validation

- Checks against printed totals and identities: 38; passed: 19; failed: 19.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.281 (f305) country_products france export 1913: sum of product values = TOTAUX: cells give 73170712, printed 73110715 (difference -59997)
  - sgt1922 p.281 (f305) country_products france export 1914: sum of product values = TOTAUX: cells give 35425637, printed 33671265 (difference -1754372)
  - sgt1922 p.281 (f305) country_products france export 1915: sum of product values = TOTAUX: cells give 62282509, printed 62782418 (difference 499909)
  - sgt1922 p.281 (f305) country_products france export 1915: TOTAUX = commerce_trade_by_country (same edition): cells give 62782418, printed 62182418 (difference -600000)
  - sgt1922 p.281 (f305) country_products france export 1916: sum of product values = TOTAUX: cells give 62119685, printed 51904159 (difference -10215526)
  - sgt1922 p.281 (f305) country_products france export 1916: TOTAUX = commerce_trade_by_country (same edition): cells give 51904159, printed 51994059 (difference 89900)
  - sgt1922 p.281 (f305) country_products france export 1917: sum of product values = TOTAUX: cells give 80743168, printed 80743170 (difference 2)
  - sgt1922 p.281 (f305) country_products france export 1918: sum of product values = TOTAUX: cells give 82202871, printed 82253461 (difference 50590)
  - sgt1922 p.281 (f305) country_products france export 1919: sum of product values = TOTAUX: cells give 135364315, printed 120932134 (difference -14432181)
  - sgt1922 p.281 (f305) country_products france export 1919: TOTAUX = commerce_trade_by_country (same edition): cells give 120932134, printed 129932134 (difference 9000000)
  - sgt1922 p.281 (f305) country_products france export 1920: sum of product values = TOTAUX: cells give 176377487, printed 176735487 (difference 358000)
  - sgt1922 p.277 (f301) country_products france import 1914: sum of product values = TOTAUX: cells give 58708578, printed 58709078 (difference 500)
  - sgt1922 p.277 (f301) country_products france import 1915: sum of product values = TOTAUX: cells give 47955176, printed 47955126 (difference -50)
  - sgt1922 p.277 (f301) country_products france import 1916: sum of product values = TOTAUX: cells give 54817046, printed 54837146 (difference 20100)
  - sgt1922 p.277 (f301) country_products france import 1917: sum of product values = TOTAUX: cells give 54274916, printed 54274971 (difference 55)
  - sgt1922 p.277 (f301) country_products france import 1918: sum of product values = TOTAUX: cells give 63948246, printed 63958456 (difference 10210)
  - sgt1922 p.277 (f301) country_products france import 1919: sum of product values = TOTAUX: cells give 92276145, printed 92309745 (difference 33600)
  - sgt1922 p.277 (f301) country_products france import 1920: sum of product values = TOTAUX: cells give 306465661, printed 296575259 (difference -9890402)
  - sgt1922 p.277 (f301) country_products france import 1921: sum of product values = TOTAUX: cells give 367667654, printed 367580359 (difference -87295)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: illegible: 129.

  - sgt1922 p.281 1921 France / france / export / vins_de_liqueur / value / francs = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / espece_chevaline / quantity / Tête = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / espece_mulassiere / quantity / Tête = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / espece_asine / quantity / Tête = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / espece_cameline / quantity / Tête = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / espece_bovine / quantity / Tête = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / espece_ovine / quantity / Tête = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / espece_caprine / quantity / Tête = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / espece_porcine / quantity / Tête = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / viandes_fraiches_salees_ou_autrement_conservees_charcuterie / quantity / Kilo = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / peaux_brutes_fraiches_ou_seches / quantity / Quint = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / laines_en_suint / quantity / Quint = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / laines_lavees / quantity / Quint = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / cire_animale_brute / quantity / Kilo = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / poissons_frais / quantity / Kilo = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / poissons_secs_sales_fumes_ou_autrement_conserves_thon_et_bou / quantity / Kilo = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / eponges_lavees / quantity / Kilo = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / eponges_non_lavees / quantity / Kilo = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / froment / quantity / Quint = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / orge / quantity / Quint = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / avoine / quantity / Quint = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / mais_en_grains / quantity / Quint = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / farine_de_froment / quantity / Quint = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / gruaux_semoules_en_gruaux / quantity / Quint = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / semoules_en_pates_et_pates_d_italie / quantity / Quint = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / son / quantity / Kilo = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / feves / quantity / Kilo = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / pommes_de_terre / quantity / Kilo = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / legumes_verts_sales_ou_confits / quantity / Kilo = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / dattes / quantity / Quint = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / citrons_et_cedrats_oranges_mandarines / quantity / Kilo = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / raisins_frais_ou_secs / quantity / Kilo = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / amandes / quantity / Quint = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / caroubes / quantity / Kilo = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / graine_de_lin / quantity / Quint = NA (illegible)
  - sgt1922 p.278 1922 France / france / export / marcs_de_raisins_et_mouts / quantity / Kilo = NA (illegible)
  - sgt1922 p.280 1922 France / france / export / huiles_d_olive / quantity / Quint = NA (illegible)
  - sgt1922 p.280 1922 France / france / export / huiles_de_grignons_d_olives / quantity / Quint = NA (illegible)
  - sgt1922 p.280 1922 France / france / export / huiles_volatiles_ou_essences_de_toutes_sortes / quantity / Kilo = NA (illegible)
  - sgt1922 p.280 1922 France / france / export / especes_medicinales / quantity / Kilo = NA (illegible)
  - sgt1922 p.280 1922 France / france / export / liege_brut_rape_ou_en_planches / quantity / Kilo = NA (illegible)
  - sgt1922 p.280 1922 France / france / export / alfa_et_diss / quantity / Quint = NA (illegible)
  - sgt1922 p.280 1922 France / france / export / teintures_et_tannins / quantity / Kilo = NA (illegible)
  - sgt1922 p.280 1922 France / france / export / vins_ordinaires / quantity / Hect = NA (illegible)
  - sgt1922 p.280 1922 France / france / export / mistelles / quantity / Hect = NA (illegible)
  - sgt1922 p.280 1922 France / france / export / vins_de_liqueur / quantity / Hect = NA (illegible)
  - sgt1922 p.280 1922 France / france / export / eau_de_vie / quantity / Hect = NA (illegible)
  - sgt1922 p.280 1922 France / france / export / phosphates / quantity / Quint = NA (illegible)
  - sgt1922 p.280 1922 France / france / export / fer_minerai / quantity / Quint = NA (illegible)
  - sgt1922 p.280 1922 France / france / export / plomb_minerai / quantity / Quint = NA (illegible)
  - sgt1922 p.280 1922 France / france / export / plomb_en_masses_barres_ou_plaques / quantity / Quint = NA (illegible)
  - sgt1922 p.280 1922 France / france / export / zinc_minerai / quantity / Quint = NA (illegible)
  - sgt1922 p.280 1922 France / france / export / lies_et_tartres / quantity / Kilo = NA (illegible)
  - sgt1922 p.280 1922 France / france / export / savons / quantity / Quint = NA (illegible)
  - sgt1922 p.280 1922 France / france / export / poteries / quantity / Kilo = NA (illegible)
  - sgt1922 p.280 1922 France / france / export / tissus_de_laine_tapis_et_couvertures / quantity / Kilo = NA (illegible)
  - sgt1922 p.280 1922 France / france / export / tapis_de_laine_estampilles / quantity / m2 = NA (illegible)
  - sgt1922 p.280 1922 France / france / export / papier_et_carton_de_toutes_sortes / quantity / Kilo = NA (illegible)
  - sgt1922 p.280 1922 France / france / export / peaux_preparees_pelleteries_et_ouvrages_en_peau_ou_en_cuir_d / quantity / Quint = NA (illegible)
  - sgt1922 p.280 1922 France / france / export / ouvrages_de_sparterie_et_de_vannerie / quantity / Quint = NA (illegible)
  - sgt1922 p.280 1922 France / france / export / colis_postaux_autres_que_les_huiles_et_les_eponges / quantity / Kilo = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / espece_chevaline / quantity / Tête = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / espece_asine / quantity / Tête = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / espece_bovine / quantity / Tête = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / espece_ovine / quantity / Tête = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / espece_caprine / quantity / Tête = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / viandes_fraiches_salees_ou_autrement_conservees / quantity / Kilo = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / peaux_brutes_fraiches_ou_seches / quantity / Quint = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / laines_en_masse_peignees_ou_cardees / quantity / Quint = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / graisses_animales_suifs_saindoux_margarines / quantity / Kilo = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / fromages_beurre_frais_fondu_sale / quantity / Kilo = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / poissons_secs_sales_fumes_conserves_marines_ou_autrement_pre / quantity / Kilo = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / cereales_en_grains / quantity / Quint = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / froment_farine_de / quantity / Quint = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / gruau_semoules_en_gruau / quantity / Quint = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / semoules_en_pates_et_pates_d_italie / quantity / Quint = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / riz_brisures_entier_farines_et_semoules / quantity / Kilo = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / legumes_secs_et_leurs_farines / quantity / Kilo = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / pommes_de_terre / quantity / Quint = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / fruits_et_graines / quantity / Kilo = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / sucres_bruts_et_raffines / quantity / Kilo = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / lait_concentre_pur_et_sucre_et_lait_sterilise / quantity / Kilo = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / confitures_au_sucre_et_au_miel / quantity / Kilo = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / cafe_en_feves_et_en_pellicules / quantity / Kilo = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / chocolat / quantity / Kilo = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / the / quantity / Kilo = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / huiles_d_olive / quantity / Quint = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / huiles_de_graines_sesame_arachides_colza / quantity / Kilo = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / especes_medicinales / quantity / Kilo = NA (illegible)
  - sgt1922 p.275 1922 France / france / import / especes_medicinales / value / francs = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / bois / quantity / Quint = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / teintures_et_tanins / quantity / Kilo = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / legumes_frais_sales_confits_conserves_ou_desseches / quantity / Kilo = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / tourteaux / quantity / Kilo = NA (illegible)
  - sgt1922 p.274 1922 France / france / import / vins / quantity / Hecto = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / vinaigres / quantity / Hect = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / eaux_de_vie_esprits_de_toutes_sortes_alcool_pur_et_liqueurs / quantity / Hect = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / eaux_minerales / quantity / Hect = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / bieres / quantity / Hect = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / materiaux_de_construction / quantity / Quint = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / houille / quantity / Quint = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / huiles_de_petrole_et_de_schiste / quantity / Hect = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / fer_etire_en_barres_a_rainure_rails_fer_a_t_essieux_et_banda / quantity / Kilo = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / metaux_autres / quantity / Kilo = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / produits_chimiques / quantity / Kilo = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / medicaments_parfumerie / quantity / Kilo = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / couleurs_et_vernis / quantity / Kilo = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / poteries_verres_et_cristaux / quantity / Kilo = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / fils_de_coton_de_laine_de_soie / quantity / Kilo = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / ficelles_cordages_et_fils_autres / quantity / Kilo = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / tissus_de_lin_de_chanvre_de_ramie_et_de_jute / quantity / Quint = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / chechias_ou_bonnets_rouges / quantity / Pièce = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / tissus_de_coton / quantity / Quint = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / tissus_de_laine / quantity / Quint = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / tissus_de_soie_et_de_bourre_de_soie / quantity / Quint = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / vetements_et_lingerie / quantity / Kilo = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / papier_et_ses_applications / quantity / Kilo = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / chaussures / quantity / Paire = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / peaux_et_pelleteries_ouvrees / quantity / Kilo = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / montres / quantity / Pièce = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / bijouterie_d_or_et_d_argent_orfevrerie / quantity / Gr = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / horlogerie / quantity / Kilo = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / machines_et_mecaniques_et_leurs_pieces_detachees / quantity / Quint = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / outils / quantity / Kilo = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / meubles_et_ouvrages_en_bois / quantity / Kilo = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / carrosserie / quantity / Kilo = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / ouvrages_de_sparterie_de_vannerie_et_de_corderie / quantity / Quint = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / bimbeloterie / quantity / Kilo = NA (illegible)
  - sgt1922 p.276 1922 France / france / import / colis_postaux / quantity / Kilo = NA (illegible)

## Image versus OCR

- Read cell by cell on the page images (8 printings): sgt1922 f298, sgt1922 f299, sgt1922 f300, sgt1922 f301, sgt1922 f302, sgt1922 f303, sgt1922 f304, sgt1922 f305.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
