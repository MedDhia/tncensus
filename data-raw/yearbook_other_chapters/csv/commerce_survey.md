# Commerce chapter: survey of sgt1922, sgt1923, sgt1924

Chapter XII *Commerce et navigation*, volume `bpt6k9105649x`. Views confirmed on the page images: sgt1922
f281 (chapter title) to f436 (blank), f437 = chapter XIII Colonisation; sgt1923 f771 to f926 (f927 =
Colonisation); sgt1924 f1275 to f1430 (blank; f1431 = Colonisation). The three editions have the same layout
view for view (offsets +490 and +994 from sgt1922; checked on contact sheets and Gallica OCR word counts per
view). Pages are upright; most tables run across two-page spreads (even view = row headings + first years, odd
view = remaining years and, from c) on, the averages "Moyenne des années"). Each edition covers the last ten
years (1913-1922, 1914-1923, 1915-1924), so every yearly series falls under SPEC_ADDENDUM rule 4.

## Views (sgt1922 numbering; add 490 for sgt1923, 994 for sgt1924)

| views | content | layout, approx. cells per edition | proposed CSV |
|---|---|---|---|
| 281 | chapter title | – | – |
| 282-283 | Renseignements généraux: a) Mouvement global des importations et des exportations; b) Résumé ... par classe de produits (valeur en francs) | 3 + 12 lines x 10 years, ~150 | `commerce_trade_by_class` (**done**; a) used as check) |
| 284-287 | c) Résumé des importations et des exportations par catégorie de produits (valeur en francs): ~31 nomenclature categories x import/export, 10 years + 3 five-year averages | ~800 | `commerce_trade_by_category` (**done**) |
| 288-289 | d) Classement des produits par pays de provenance et de destination: by class, France et Algérie vs l'Étranger et colonies françaises, import/export, 10 years | ~400 | `commerce_trade_by_origin_group` (**done**) |
| 290-293 | e) Résumé des relations commerciales avec les différents pays (valeur en francs): ~35 countries x import/export, 10 years + 3 averages | ~900 | `commerce_trade_by_country` |
| 294-295 | f) Droits (de douane) perçus, by product category, 10 years + averages, francs with centimes | ~450 | `commerce_customs_duties` (**done**) |
| 296-297 | droits de sortie: export duties by product (animals, hides, olive oil, alfa, sponges, colis postaux, taxes ...), 10 years + averages | ~350 | `commerce_export_duties` (**done**) |
| 298-305 | Relations commerciales avec les principaux pays (1913-1922): FRANCE, a) importations, b) exportations, quantity (with unit column) and value by product line, 10 years | ~2400 | `commerce_country_products` |
| 306-309 | same, ALGÉRIE | ~1500 | idem |
| 310-313 | same, ANGLETERRE | ~1000 | idem |
| 314-317 | same, ITALIE | ~1600 | idem |
| 318-321 | same, ÉTATS-UNIS | ~800 | idem |
| 322-325 | same, BELGIQUE | ~700 | idem |
| 326-403 | Commerce des principaux produits (1913-1922): per product (livestock by species, hides, wool, eggs, fish, cereals and flours, pulses, dates, olive oil, alfa, cork, minerals: phosphates, iron, lead, zinc ore; metals; manufactures: sacks, chéchias, machines, soap, sparterie ...): import/export quantity and value by year (left page) and by country of provenance/destination for the last three years (boxed sub-tables) | ~78 views, ~15000 | `commerce_product_trade` and `commerce_product_trade_by_country` |
| 404-407 | Consommation: animals slaughtered by commune (boeufs/vaches, veaux, moutons, chèvres, porcs, chameaux, autres), one year | ~500 | `commerce_slaughter_by_commune` |
| 408-411 | Céréales: a) importation/exportation by campaign 1912-13 to 1921-22 with balance; b) stocks (production, commercial campaign, seed, consumption) 1913-1921; c) consommation moyenne 1912-1921 | ~350 | `commerce_cereals_balance`, `commerce_cereals_stocks` |
| 412-415 | same for olive oil (huile d'olive) and wine (vins) | ~150 | `commerce_oil_wine_balance` |
| 416-421 | Mercuriales: monthly prices at Tunis (meat by cut, hides, wool, eggs, cereals, pulses, olive oil ...), minimum/maximum/average | ~2500 | `commerce_prices` |
| 422-424 | Magasins généraux: mouvement des marchandises, Tunis and Sousse (existing, entries, exits, remaining; quantity and value) | ~400 | `commerce_bonded_warehouses` |
| 425-426 | Poids et mesures: vérification by circonscription, and c) résultats généraux 1913-1922 | ~300 | `commerce_weights_measures` |
| 427 | Laboratoire de chimie: analyses by nature of sample and service | ~300 | `commerce_chemistry_lab` |
| 428-429 | Navigation: a) mouvement des navires par port (21 ports): entries / exits / combined: ships, tonnage, goods, passengers, livestock | ~350 | `commerce_navigation_by_port` |
| 430-431 | b) by flag (pavillon; steam/sail), same measures | ~400 | `commerce_navigation_by_flag` |
| 432 | c) sur le littoral: ships, goods (tonnes), passengers, entries and exits, 1913-1922 | ~60 | `commerce_navigation_yearly` |
| 433 | d) Cabotage: weight of cargo by port of dispatch and destination | ~60 | `commerce_cabotage` |
| 434-435 | Pêches maritimes: by type of fishing and flag (Tunisian, Italian, French, Greek, Sicilian-Maltese): boats, tonnage, crews; recapitulation and catch (kg, francs) | ~150 | `commerce_fisheries` |
| 436 | blank | – | – |

## Work plan and status

Order: yearly summaries and by-country tables first (282-297), then navigation (428-435), then the
country-by-product tables (298-325), the principal-products section (326-403), and the remaining
consumption / prices / warehouses / weights pages.

| CSV | status | views read |
|---|---|---|
| `commerce_trade_by_class` | **done**, sgt1922-1924, 96 rows | f282-283, f772-773, f1276-1277, every cell read on native-resolution crops (img: all) |
| `commerce_trade_by_category` | **done**, sgt1922-1924, 768 rows | f284-287, f774-777, f1278-1281, every cell read on native-resolution crops (img: all); gutter cells `?` (sgt1923 1918: 21 lines; sgt1924 1918: all lines, 1919: 11 lines), stored from the latest legible printing |
| `commerce_trade_by_origin_group` | **done**, sgt1922-1924, 192 rows | f288-289, f778-779, f1282-1283, every cell read on native-resolution crops (img: all); gutter cells `?` (sgt1922 1918 France-Algérie: mineral export, TOTAL; sgt1923 1919 France-Algérie: all lines) |
| `commerce_trade_by_country` | **done**, sgt1922-1924, 696 rows | f290-293, f780-783, f1284-1287, every cell read on native-resolution crops (img: all), each printing independently; gutter cells `?` (sgt1922 1916 most lines, sgt1923 1917 f782 6 lines and 1918 larger values), stored from the latest legible printing |
| `commerce_customs_duties` | **done**, sgt1922-1924, 420 rows | f294-295, f784-785, f1288-1289, every cell read on native-resolution crops (img: all), each printing independently; gutter cells `?` (sgt1922 1917: 3 lines + TOTAL, 1916 one line + TOTAL; sgt1923 1918: 29 lines + TOTAL) |
| `commerce_export_duties` | **done**, sgt1922-1924, 452 rows | f296-297, f786-787, f1290-1291, every cell read on native-resolution crops (img: all); sgt1924 prints 40 lines (26 earlier); gutter cells `?` (sgt1922 1916 TOTAL; sgt1923 1917 all non-zero lines, 1918 five lines + TOTAL) |
| all others listed above | to do (next: navigation f428-435) | – |

## Image reading

`commerce_trade_by_class`: every cell of every printing (sgt1922 f282|f283, sgt1923 f772|f773, sgt1924
f1276|f1277) read on native-resolution crops; the OCR was not used for these values. The overlapping years
were read independently on each printing.

`commerce_trade_by_category`: every cell of every printing (sgt1922 f284-287, sgt1923 f774-777, sgt1924
f1278-1281) read on native-resolution crops; the five-year averages were read only where needed to locate the
misprints behind failing totals (not stored). The fourth year of each spread lies in the gutter (see the notes).
The sgt1923 and sgt1924 lines were re-typed in full from their own page images (f774-777, f1278-1281),
without reference to the sgt1922 transcription; differences only in gutter legibility (see the notes).

`commerce_trade_by_origin_group`: every cell of every printing (sgt1922 f288|f289, sgt1923 f778|f779,
sgt1924 f1282|f1283) read on native-resolution crops, each printing independently; OCR not used.

`commerce_trade_by_country`: every cell of every printing (sgt1922 f290-293, sgt1923 f780-783, sgt1924
f1284-1287) read on native-resolution crops, each printing typed from its own image; the printed averages were
transcribed as check columns (not stored). OCR not used.

`commerce_customs_duties` and `commerce_export_duties`: every cell of every printing (sgt1922 f294-297, sgt1923 f784-787, sgt1924 f1288-1291) read on native-resolution crops, each printing typed from its own image; the printed averages were read only to try to locate failing totals (not stored). OCR not used.
