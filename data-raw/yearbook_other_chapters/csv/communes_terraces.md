# Concessions sur la voie publique : b) Terrasses et étalages

*Pavement concessions: café terraces (chairs and tables of lemonade sellers) and street stalls (goods of all kinds): number, surface and receipts, per commune.*

Source: *Statistique générale de la Tunisie*, chapter *Communes*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935. Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR).

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 37, f61; sgt1923 (`bpt6k9105649x`): p. 41, f543; sgt1924 (`bpt6k9105649x`): p. 41, f1031; sgt1925 (`bpt6k9105650k`): p. 41, f65; sgt1926 (`bpt6k9105650k`): p. 49, f613; sgt1927 (`bpt6k91056510`): p. 49, f77; sgt1928 (`bpt6k91056510`): p. 49, f601; sgt1929 (`bpt6k9105652d`): p. 49, f77; sgt1930 (`bpt6k9105652d`): p. 51, f609; sgt1935 (`bpt6k9105653t`): p. 27, f47.

Rebuild: `python3 data-raw/yearbook_other_chapters/extract_communes.py build` (transcriptions `../transcribed/communes_terraces_<edition>.txt`).

Printed once per edition (SPEC_ADDENDUM rule 5): `year` is the year the edition reports on; no year is printed twice, so there is no overlap to compare.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the edition's figures (exercice / calendar year)
- `commune`: commune as printed (for loans: the name in the block heading, e.g. `Tunis` from *Commune de Tunis*; `le Kef` from *Commune du Kef*)
- `measure`: English code of the printed column
- `measure_fr`: column heading as printed (French)
- `value`: number: integer as printed; surface: square metres (*mètre carré*), decimals as printed; receipts (*produits*): francs with centimes. Printed » and *néant* = 0
- `flag`: empty, `not_applicable` (text printed instead of a number: value NA; the text is listed below), `illegible` (value NA; for money with hidden centimes the franc part is listed below)

Table b) of the *Concessions sur la voie publique* pages, printed on the right-hand page facing table a) (building permits), **without commune labels**: each value line was matched to the commune labels of the facing page by OCR line position and by counting lines, and checked against the large communes (Bizerte, Kairouan, Sfax, Sousse, Tunis). sgt1922–sgt1930 and sgt1935; sgt1936 and sgt1939 print no such table.

**Image versus OCR.** Every cell was read on native-resolution crops of the page images (half-page crops at ~0.7 scale, re-cropped at full scale where faint); the OCR was a draft only. The sgt1926 page is faint: El-Djem stalls 35.696,10, Kef 40.200, Mateur terraces 4.321,40 and Sousse stalls 45.580,79 were read on the image where the OCR differs.

**What the numbers are.** Communes reported very differently: "number" is sometimes the surface repeated (Bizerte 42.900 / 42.900 m²) or a count of days or tickets; surfaces are sometimes rates (Nabeul 1928 "1 20", 1935 "0 30"). Values are stored as printed; the cells where the printed entry is text ("droits affermés", "divers", "variables", "concédés à l'adjudicataire", "70 m2 à 1 fr." …) are NA with flag `not_applicable` and the text is listed below. sgt1925 Tunis stalls surface is printed "965.057": the printed total (404.045,87) is consistent with 965,057 m² (the sum is then 1,26 short), not 965.057 m²; stored as printed (965057) and the column check fails. sgt1925 Médenine stalls number printed "233 50" stored 233.50.

Footnotes and remarks printed with the table: sgt1926 (1) Produits affermés; (2) Étalages (par métrés et par abonnements); (3) Concédés avec les droits de marché; (4) Adjugé avec les droits de marché; (5)–(6) adjudication / affermés avec les marchés. sgt1927: (1) Droits affermés en 1927; (2) Droits donnés en adjudication; (3) Affermé avec les droits de marché; (4) Produits affermés avec les droits de marché; (5) Droits affermés. sgt1928, under the table: *Il y a lieu d'ajouter à ces droits : 505 étalages sur façades soit 758 m2 25 : 16.476 20* (to be added: 505 façade stalls, 758,25 m², 16.476,20 fr.; not stored as a row, no commune named). sgt1929: (1)(2) Droits adjugés; (3) Montant total des droits de concession; (4) Droits affermés avec les droits de marché. sgt1930: (1) Y compris droits colportage; (2) Droits adjugés; (3)(4) Droits affermés avec ceux du marché; (5) avec droits de marché; (6) Droits affermés. sgt1935 *Observations* column: Bizerte, parking dues collected by a contractor, 38.627 fr. in 1935; Grombalia (1), dues collected by the market farmer, 19.701 fr. to the commune in 1935; Maxula-Radès, of which 2.705 fr. collected by tickets; Sidi-bou-Saïd, parking 550 fr.; Sousse, of which 3.803,30 fr. collected by tickets.

Printed totals: sgt1922–sgt1925 every column (TOTAUX), sgt1926 and sgt1927 the stalls receipts only (TOTAL), none afterwards. sgt1923 matches in all six columns. The sgt1924 mismatches (notably stalls receipts, 33.356 fr. short) were re-read line by line on the image without finding the cause; the printed cells are kept and nothing is flagged, but a misassigned or misread line in that edition cannot be excluded.

## Validation

Rows: 3510.
Checks (terraces): 26; failed: 13.
  - sgt1922 p.37 communes terr_surf: cells give 80350.30, printed total 79750.30 (difference -600.00)
  - sgt1922 p.37 communes stall_surf: cells give 118138.23, printed total 118238.23 (difference 100.00)
  - sgt1924 p.41 communes terr_surf: cells give 239618.50, printed total 239613.50 (difference -5.00)
  - sgt1924 p.41 communes terr_prod: cells give 90539.40, printed total 97609.40 (difference 7070.00)
  - sgt1924 p.41 communes stall_surf: cells give 379511, printed total 378514 (difference -997)
  - sgt1924 p.41 communes stall_prod: cells give 213671.98, printed total 247027.98 (difference 33356.00)
  - sgt1925 p.41 communes terr_n: cells give 70881, printed total 70884 (difference 3)
  - sgt1925 p.41 communes terr_prod: cells give 125988.28, printed total 125588.48 (difference -399.80)
  - sgt1925 p.41 communes stall_n: cells give 80801.50, printed total 80795.50 (difference -6.00)
  - sgt1925 p.41 communes stall_surf: cells give 1368136.55, printed total 404045.87 (difference -964090.68)
  - sgt1925 p.41 communes stall_prod: cells give 291286.46, printed total 291186.46 (difference -100.00)
  - sgt1926 p.49 communes stall_prod: cells give 262687.49, printed total 263016.49 (difference 329.00)
  - sgt1927 p.49 communes stall_prod: cells give 261758.00, printed total 261714 (difference -44.00)
Flagged cells: not_applicable: 186.
  - sgt1923 Gafsa stalls_number: not_applicable — printed text: Gafsa: stall_n printed "Divers"
  - sgt1923 Kef (Le) terraces_number: not_applicable — printed text: Kef (Le): "Concédés à l'adjudicataire" printed across the row
  - sgt1923 Kef (Le) terraces_surface_m2: not_applicable — printed text: Kef (Le): "Concédés à l'adjudicataire" printed across the row
  - sgt1923 Kef (Le) terraces_receipts: not_applicable — printed text: Kef (Le): "Concédés à l'adjudicataire" printed across the row
  - sgt1923 Kef (Le) stalls_number: not_applicable — printed text: Kef (Le): "Concédés à l'adjudicataire" printed across the row
  - sgt1923 Kef (Le) stalls_surface_m2: not_applicable — printed text: Kef (Le): "Concédés à l'adjudicataire" printed across the row
  - sgt1923 Kef (Le) stalls_receipts: not_applicable — printed text: Kef (Le): "Concédés à l'adjudicataire" printed across the row
  - sgt1923 Monastir terraces_number: not_applicable — printed text: Monastir: "Affermés" printed across the row
  - sgt1923 Monastir terraces_surface_m2: not_applicable — printed text: Monastir: "Affermés" printed across the row
  - sgt1923 Monastir terraces_receipts: not_applicable — printed text: Monastir: "Affermés" printed across the row
  - sgt1923 Monastir stalls_number: not_applicable — printed text: Monastir: "Affermés" printed across the row
  - sgt1923 Monastir stalls_surface_m2: not_applicable — printed text: Monastir: "Affermés" printed across the row
  - sgt1923 Monastir stalls_receipts: not_applicable — printed text: Monastir: "Affermés" printed across the row
  - sgt1924 Gafsa stalls_number: not_applicable — printed text: Gafsa: stall_n and stall_surf: "Divers et non comptés"
  - sgt1924 Gafsa stalls_surface_m2: not_applicable — printed text: Gafsa: stall_n and stall_surf: "Divers et non comptés"
  - sgt1924 Kairouan stalls_number: not_applicable — printed text: Kairouan: stall_n printed "variables"
  - sgt1924 Kef (Le) stalls_receipts: not_applicable — printed text: Kef (Le): stall_prod printed "Droits affermés avec les marchés"
  - sgt1924 Mahdia terraces_number: not_applicable — printed text: Mahdia: "Droits affermés" printed across the row
  - sgt1924 Mahdia terraces_surface_m2: not_applicable — printed text: Mahdia: "Droits affermés" printed across the row
  - sgt1924 Mahdia terraces_receipts: not_applicable — printed text: Mahdia: "Droits affermés" printed across the row
  - sgt1924 Mahdia stalls_number: not_applicable — printed text: Mahdia: "Droits affermés" printed across the row
  - sgt1924 Mahdia stalls_surface_m2: not_applicable — printed text: Mahdia: "Droits affermés" printed across the row
  - sgt1924 Mahdia stalls_receipts: not_applicable — printed text: Mahdia: "Droits affermés" printed across the row
  - sgt1924 Medjez-el-Bab terraces_number: not_applicable — printed text: Medjez-el-Bab: "Droits affermés (produit de l'affermage)" printed across the row
  - sgt1924 Medjez-el-Bab terraces_surface_m2: not_applicable — printed text: Medjez-el-Bab: "Droits affermés (produit de l'affermage)" printed across the row
  - sgt1924 Medjez-el-Bab terraces_receipts: not_applicable — printed text: Medjez-el-Bab: "Droits affermés (produit de l'affermage)" printed across the row
  - sgt1924 Medjez-el-Bab stalls_number: not_applicable — printed text: Medjez-el-Bab: "Droits affermés (produit de l'affermage)" printed across the row
  - sgt1924 Medjez-el-Bab stalls_surface_m2: not_applicable — printed text: Medjez-el-Bab: "Droits affermés (produit de l'affermage)" printed across the row
  - sgt1924 Medjez-el-Bab stalls_receipts: not_applicable — printed text: Medjez-el-Bab: "Droits affermés (produit de l'affermage)" printed across the row
  - sgt1924 Monastir terraces_number: not_applicable — printed text: Monastir: "Droits affermés (produit de l'affermage)" printed across the row
  - sgt1924 Monastir terraces_surface_m2: not_applicable — printed text: Monastir: "Droits affermés (produit de l'affermage)" printed across the row
  - sgt1924 Monastir terraces_receipts: not_applicable — printed text: Monastir: "Droits affermés (produit de l'affermage)" printed across the row
  - sgt1924 Monastir stalls_number: not_applicable — printed text: Monastir: "Droits affermés (produit de l'affermage)" printed across the row
  - sgt1924 Monastir stalls_surface_m2: not_applicable — printed text: Monastir: "Droits affermés (produit de l'affermage)" printed across the row
  - sgt1924 Monastir stalls_receipts: not_applicable — printed text: Monastir: "Droits affermés (produit de l'affermage)" printed across the row
  - sgt1924 Philippe-Thomas terraces_number: not_applicable — printed text: Philippe-Thomas: "Représentait les droits de stationnement" across columns 1-5, then 6.073,00
  - sgt1924 Philippe-Thomas terraces_surface_m2: not_applicable — printed text: Philippe-Thomas: "Représentait les droits de stationnement" across columns 1-5, then 6.073,00
  - sgt1924 Philippe-Thomas terraces_receipts: not_applicable — printed text: Philippe-Thomas: "Représentait les droits de stationnement" across columns 1-5, then 6.073,00
  - sgt1924 Philippe-Thomas stalls_number: not_applicable — printed text: Philippe-Thomas: "Représentait les droits de stationnement" across columns 1-5, then 6.073,00
  - sgt1924 Philippe-Thomas stalls_surface_m2: not_applicable — printed text: Philippe-Thomas: "Représentait les droits de stationnement" across columns 1-5, then 6.073,00
  - sgt1924 Thala stalls_surface_m2: not_applicable — printed text: Thala: stall_surf printed "divers"
  - sgt1924 Tebourba stalls_number: not_applicable — printed text: Tebourba: stall_n printed "divers"
  - sgt1925 Béja terraces_surface_m2: not_applicable — printed text: Béja: "Taxes affermées pour 15.000 francs" across columns 2-5, then 15.000
  - sgt1925 Béja terraces_receipts: not_applicable — printed text: Béja: "Taxes affermées pour 15.000 francs" across columns 2-5, then 15.000
  - sgt1925 Béja stalls_number: not_applicable — printed text: Béja: "Taxes affermées pour 15.000 francs" across columns 2-5, then 15.000
  - sgt1925 Béja stalls_surface_m2: not_applicable — printed text: Béja: "Taxes affermées pour 15.000 francs" across columns 2-5, then 15.000
  - sgt1925 El-Djem terraces_surface_m2: not_applicable — printed text: El-Djem: "Droits affermés" across columns 2-5, then 29.927,30
  - sgt1925 El-Djem terraces_receipts: not_applicable — printed text: El-Djem: "Droits affermés" across columns 2-5, then 29.927,30
  - sgt1925 El-Djem stalls_number: not_applicable — printed text: El-Djem: "Droits affermés" across columns 2-5, then 29.927,30
  - sgt1925 El-Djem stalls_surface_m2: not_applicable — printed text: El-Djem: "Droits affermés" across columns 2-5, then 29.927,30
  - sgt1925 Goulette (La) terraces_receipts: not_applicable — printed text: Goulette (La): "Y compris les étalages" across columns 3-5 (terraces include stalls)
  - sgt1925 Goulette (La) stalls_number: not_applicable — printed text: Goulette (La): "Y compris les étalages" across columns 3-5 (terraces include stalls)
  - sgt1925 Goulette (La) stalls_surface_m2: not_applicable — printed text: Goulette (La): "Y compris les étalages" across columns 3-5 (terraces include stalls)
  - sgt1925 Kef (Le) terraces_number: not_applicable — printed text: Kef (Le): "Affermés avec les droits de marché moyennant une somme globale de" 38.000
  - sgt1925 Kef (Le) terraces_surface_m2: not_applicable — printed text: Kef (Le): "Affermés avec les droits de marché moyennant une somme globale de" 38.000
  - sgt1925 Kef (Le) terraces_receipts: not_applicable — printed text: Kef (Le): "Affermés avec les droits de marché moyennant une somme globale de" 38.000
  - sgt1925 Kef (Le) stalls_number: not_applicable — printed text: Kef (Le): "Affermés avec les droits de marché moyennant une somme globale de" 38.000
  - sgt1925 Kef (Le) stalls_surface_m2: not_applicable — printed text: Kef (Le): "Affermés avec les droits de marché moyennant une somme globale de" 38.000
  - sgt1925 Mahdia terraces_surface_m2: not_applicable — printed text: Mahdia: "Concédés à l'adjudicataire des marchés" across columns 2-4
  - sgt1925 Mahdia terraces_receipts: not_applicable — printed text: Mahdia: "Concédés à l'adjudicataire des marchés" across columns 2-4
  - sgt1925 Mahdia stalls_number: not_applicable — printed text: Mahdia: "Concédés à l'adjudicataire des marchés" across columns 2-4
  - sgt1925 Monastir terraces_number: not_applicable — printed text: Monastir: "Produits donnés en fermage avec les marchés municipaux" across columns 1-5
  - sgt1925 Monastir terraces_surface_m2: not_applicable — printed text: Monastir: "Produits donnés en fermage avec les marchés municipaux" across columns 1-5
  - sgt1925 Monastir terraces_receipts: not_applicable — printed text: Monastir: "Produits donnés en fermage avec les marchés municipaux" across columns 1-5
  - sgt1925 Monastir stalls_number: not_applicable — printed text: Monastir: "Produits donnés en fermage avec les marchés municipaux" across columns 1-5
  - sgt1925 Monastir stalls_surface_m2: not_applicable — printed text: Monastir: "Produits donnés en fermage avec les marchés municipaux" across columns 1-5
  - sgt1925 M'saken terraces_surface_m2: not_applicable — printed text: M'saken: "Stationnement et droit de marché" across columns 2-5, then 12.560,10
  - sgt1925 M'saken terraces_receipts: not_applicable — printed text: M'saken: "Stationnement et droit de marché" across columns 2-5, then 12.560,10
  - sgt1925 M'saken stalls_number: not_applicable — printed text: M'saken: "Stationnement et droit de marché" across columns 2-5, then 12.560,10
  - sgt1925 M'saken stalls_surface_m2: not_applicable — printed text: M'saken: "Stationnement et droit de marché" across columns 2-5, then 12.560,10
  - sgt1926 Maxula-Radès stalls_number: not_applicable — printed text: Maxula-Radès: stall_n "Divers", stall_surf "0,50 et 0,10 le m²" (a rate)
  - sgt1926 Maxula-Radès stalls_surface_m2: not_applicable — printed text: Maxula-Radès: stall_n "Divers", stall_surf "0,50 et 0,10 le m²" (a rate)
  - sgt1926 Tebourba stalls_number: not_applicable — printed text: Tebourba: stall_n "Divers"
  - sgt1927 Ferryville stalls_number: not_applicable — printed text: Ferryville: stall_n "divers"
  - sgt1928 Béja terraces_number: not_applicable — printed text: Béja: "droits affermés" (whole line)
  - sgt1928 Béja terraces_surface_m2: not_applicable — printed text: Béja: "droits affermés" (whole line)
  - sgt1928 Béja terraces_receipts: not_applicable — printed text: Béja: "droits affermés" (whole line)
  - sgt1928 Béja stalls_number: not_applicable — printed text: Béja: "droits affermés" (whole line)
  - sgt1928 Béja stalls_surface_m2: not_applicable — printed text: Béja: "droits affermés" (whole line)
  - sgt1928 Béja stalls_receipts: not_applicable — printed text: Béja: "droits affermés" (whole line)
  - sgt1928 Djemmal terraces_number: not_applicable — printed text: Djemmal: "droits affermés"
  - sgt1928 Djemmal terraces_surface_m2: not_applicable — printed text: Djemmal: "droits affermés"
  - sgt1928 Djemmal terraces_receipts: not_applicable — printed text: Djemmal: "droits affermés"
  - sgt1928 Djemmal stalls_number: not_applicable — printed text: Djemmal: "droits affermés"
  - sgt1928 Djemmal stalls_surface_m2: not_applicable — printed text: Djemmal: "droits affermés"
  - sgt1928 Djemmal stalls_receipts: not_applicable — printed text: Djemmal: "droits affermés"
  - sgt1928 Ebba-Ksour terraces_number: not_applicable — printed text: Ebba-Ksour: "droits affermés"
  - sgt1928 Ebba-Ksour terraces_surface_m2: not_applicable — printed text: Ebba-Ksour: "droits affermés"
  - sgt1928 Ebba-Ksour terraces_receipts: not_applicable — printed text: Ebba-Ksour: "droits affermés"
  - sgt1928 Ebba-Ksour stalls_number: not_applicable — printed text: Ebba-Ksour: "droits affermés"
  - sgt1928 Ebba-Ksour stalls_surface_m2: not_applicable — printed text: Ebba-Ksour: "droits affermés"
  - sgt1928 Ebba-Ksour stalls_receipts: not_applicable — printed text: Ebba-Ksour: "droits affermés"
  - sgt1928 Kef (Le) terraces_receipts: not_applicable — printed text: Kef (Le): terr_prod "affermés"
  - sgt1928 Monastir terraces_number: not_applicable — printed text: Monastir: "droits affermés"
  - sgt1928 Monastir terraces_surface_m2: not_applicable — printed text: Monastir: "droits affermés"
  - sgt1928 Monastir terraces_receipts: not_applicable — printed text: Monastir: "droits affermés"
  - sgt1928 Monastir stalls_number: not_applicable — printed text: Monastir: "droits affermés"
  - sgt1928 Monastir stalls_surface_m2: not_applicable — printed text: Monastir: "droits affermés"
  - sgt1928 Monastir stalls_receipts: not_applicable — printed text: Monastir: "droits affermés"
  - sgt1928 M'saken terraces_number: not_applicable — printed text: M'saken: "droits affermés"
  - sgt1928 M'saken terraces_surface_m2: not_applicable — printed text: M'saken: "droits affermés"
  - sgt1928 M'saken terraces_receipts: not_applicable — printed text: M'saken: "droits affermés"
  - sgt1928 M'saken stalls_number: not_applicable — printed text: M'saken: "droits affermés"
  - sgt1928 M'saken stalls_surface_m2: not_applicable — printed text: M'saken: "droits affermés"
  - sgt1928 M'saken stalls_receipts: not_applicable — printed text: M'saken: "droits affermés"
  - sgt1928 Nabeul terraces_receipts: not_applicable — printed text: Nabeul: "480 | 1 20 | affermé | à 0 f. 30 le m2 | affermé | 27.000"
  - sgt1928 Nabeul stalls_number: not_applicable — printed text: Nabeul: "480 | 1 20 | affermé | à 0 f. 30 le m2 | affermé | 27.000"
  - sgt1928 Nabeul stalls_surface_m2: not_applicable — printed text: Nabeul: "480 | 1 20 | affermé | à 0 f. 30 le m2 | affermé | 27.000"
  - sgt1928 Saint-Germain terraces_receipts: not_applicable — printed text: Saint-Germain: terr_prod "d°" (ditto: affermé)
  - sgt1928 Tabarka terraces_number: not_applicable — printed text: Tabarka: "droits affermés"
  - sgt1928 Tabarka terraces_surface_m2: not_applicable — printed text: Tabarka: "droits affermés"
  - sgt1928 Tabarka terraces_receipts: not_applicable — printed text: Tabarka: "droits affermés"
  - sgt1928 Tabarka stalls_number: not_applicable — printed text: Tabarka: "droits affermés"
  - sgt1928 Tabarka stalls_surface_m2: not_applicable — printed text: Tabarka: "droits affermés"
  - sgt1928 Tabarka stalls_receipts: not_applicable — printed text: Tabarka: "droits affermés"
  - sgt1928 Zaghouan terraces_number: not_applicable — printed text: Zaghouan: "droits affermés"
  - sgt1928 Zaghouan terraces_surface_m2: not_applicable — printed text: Zaghouan: "droits affermés"
  - sgt1928 Zaghouan terraces_receipts: not_applicable — printed text: Zaghouan: "droits affermés"
  - sgt1928 Zaghouan stalls_number: not_applicable — printed text: Zaghouan: "droits affermés"
  - sgt1928 Zaghouan stalls_surface_m2: not_applicable — printed text: Zaghouan: "droits affermés"
  - sgt1928 Zaghouan stalls_receipts: not_applicable — printed text: Zaghouan: "droits affermés"
  - sgt1928 Zarzis terraces_number: not_applicable — printed text: Zarzis: "marchés affermés"
  - sgt1928 Zarzis terraces_surface_m2: not_applicable — printed text: Zarzis: "marchés affermés"
  - sgt1928 Zarzis terraces_receipts: not_applicable — printed text: Zarzis: "marchés affermés"
  - sgt1928 Zarzis stalls_number: not_applicable — printed text: Zarzis: "marchés affermés"
  - sgt1928 Zarzis stalls_surface_m2: not_applicable — printed text: Zarzis: "marchés affermés"
  - sgt1928 Zarzis stalls_receipts: not_applicable — printed text: Zarzis: "marchés affermés"
  - sgt1929 Béja terraces_surface_m2: not_applicable — printed text: Béja: terr_surf "concédés à l'adjudic."
  - sgt1929 Djemmal terraces_surface_m2: not_applicable — printed text: Djemmal: terr_surf "droits affermés"
  - sgt1929 El Djem terraces_surface_m2: not_applicable — printed text: El Djem: terr_surf "droits affermés"
  - sgt1929 Gafsa stalls_number: not_applicable — printed text: Gafsa: stall_n "divers"
  - sgt1929 Hadjeb-el-Aïoun terraces_surface_m2: not_applicable — printed text: Hadjeb-el-Aïoun: terr_surf printed "36 m. 7"
  - sgt1929 Kef (Le) terraces_receipts: not_applicable — printed text: Kef (Le): terr_prod "droits adjugés"; stall_prod "90.100 (3)" (total of the concession dues)
  - sgt1929 Maxula-Radès terraces_surface_m2: not_applicable — printed text: Maxula-Radès: terr_surf "3 m2 par jour"; stall_n "divers"
  - sgt1929 Maxula-Radès stalls_number: not_applicable — printed text: Maxula-Radès: terr_surf "3 m2 par jour"; stall_n "divers"
  - sgt1929 Monastir terraces_receipts: not_applicable — printed text: Monastir: "(4)" printed in the terr_prod column: droits affermés avec les droits de marché
  - sgt1929 M'saken terraces_surface_m2: not_applicable — printed text: M'saken: terr_surf "droits affermés"
  - sgt1929 Nabeul terraces_receipts: not_applicable — printed text: Nabeul: "droits affermés avec les droits de marché" across columns 3-5
  - sgt1929 Nabeul stalls_number: not_applicable — printed text: Nabeul: "droits affermés avec les droits de marché" across columns 3-5
  - sgt1929 Nabeul stalls_surface_m2: not_applicable — printed text: Nabeul: "droits affermés avec les droits de marché" across columns 3-5
  - sgt1929 Zarzis terraces_receipts: not_applicable — printed text: Zarzis: terr_prod "droits affermés"
  - sgt1930 Ariana terraces_surface_m2: not_applicable — printed text: Ariana: terr_surf "70 m2 à 1 fr."
  - sgt1930 Bardo (Le) terraces_surface_m2: not_applicable — printed text: Bardo (Le): terr_surf "44 m2 à 0 fr. 75"
  - sgt1930 Béja terraces_surface_m2: not_applicable — printed text: Béja: terr_surf "concédés à un adjudic."
  - sgt1930 Monastir terraces_receipts: not_applicable — printed text: Monastir: "prod. affermés avec les marchés" across columns 3-5
  - sgt1930 Monastir stalls_number: not_applicable — printed text: Monastir: "prod. affermés avec les marchés" across columns 3-5
  - sgt1930 Monastir stalls_surface_m2: not_applicable — printed text: Monastir: "prod. affermés avec les marchés" across columns 3-5
  - sgt1935 Ebba-Ksour terraces_number: not_applicable — printed text: Ebba-Ksour: "Produits affermés" across the row
  - sgt1935 Ebba-Ksour terraces_surface_m2: not_applicable — printed text: Ebba-Ksour: "Produits affermés" across the row
  - sgt1935 Ebba-Ksour terraces_receipts: not_applicable — printed text: Ebba-Ksour: "Produits affermés" across the row
  - sgt1935 Ebba-Ksour stalls_number: not_applicable — printed text: Ebba-Ksour: "Produits affermés" across the row
  - sgt1935 Ebba-Ksour stalls_surface_m2: not_applicable — printed text: Ebba-Ksour: "Produits affermés" across the row
  - sgt1935 Ebba-Ksour stalls_receipts: not_applicable — printed text: Ebba-Ksour: "Produits affermés" across the row
  - sgt1935 Gabès terraces_number: not_applicable — printed text: Gabès: "Produits affermés" across the row
  - sgt1935 Gabès terraces_surface_m2: not_applicable — printed text: Gabès: "Produits affermés" across the row
  - sgt1935 Gabès terraces_receipts: not_applicable — printed text: Gabès: "Produits affermés" across the row
  - sgt1935 Gabès stalls_number: not_applicable — printed text: Gabès: "Produits affermés" across the row
  - sgt1935 Gabès stalls_surface_m2: not_applicable — printed text: Gabès: "Produits affermés" across the row
  - sgt1935 Gabès stalls_receipts: not_applicable — printed text: Gabès: "Produits affermés" across the row
  - sgt1935 Grombalia stalls_number: not_applicable — printed text: Grombalia: stall_n and stall_surf "(1)": (1) Droits perçus par le fermier au marché général qui a rapporté à la Commune, en 1935 une somme de 19.701 frs.
  - sgt1935 Grombalia stalls_surface_m2: not_applicable — printed text: Grombalia: stall_n and stall_surf "(1)": (1) Droits perçus par le fermier au marché général qui a rapporté à la Commune, en 1935 une somme de 19.701 frs.
  - sgt1935 Menzel-Temime terraces_number: not_applicable — printed text: Menzel-Temime: "affermé" across the terrace columns
  - sgt1935 Menzel-Temime terraces_surface_m2: not_applicable — printed text: Menzel-Temime: "affermé" across the terrace columns
  - sgt1935 Menzel-Temime terraces_receipts: not_applicable — printed text: Menzel-Temime: "affermé" across the terrace columns
  - sgt1935 Monastir terraces_number: not_applicable — printed text: Monastir: "Produits affermés" across the row
  - sgt1935 Monastir terraces_surface_m2: not_applicable — printed text: Monastir: "Produits affermés" across the row
  - sgt1935 Monastir terraces_receipts: not_applicable — printed text: Monastir: "Produits affermés" across the row
  - sgt1935 Monastir stalls_number: not_applicable — printed text: Monastir: "Produits affermés" across the row
  - sgt1935 Monastir stalls_surface_m2: not_applicable — printed text: Monastir: "Produits affermés" across the row
  - sgt1935 Monastir stalls_receipts: not_applicable — printed text: Monastir: "Produits affermés" across the row
  - sgt1935 M'saken terraces_number: not_applicable — printed text: M'saken: "Produits affermés" across columns 1-5, then 31.865
  - sgt1935 M'saken terraces_surface_m2: not_applicable — printed text: M'saken: "Produits affermés" across columns 1-5, then 31.865
  - sgt1935 M'saken terraces_receipts: not_applicable — printed text: M'saken: "Produits affermés" across columns 1-5, then 31.865
  - sgt1935 M'saken stalls_number: not_applicable — printed text: M'saken: "Produits affermés" across columns 1-5, then 31.865
  - sgt1935 M'saken stalls_surface_m2: not_applicable — printed text: M'saken: "Produits affermés" across columns 1-5, then 31.865
  - sgt1935 Nabeul stalls_surface_m2: not_applicable — printed text: Nabeul: stall_surf printed "0 30" (0,30, a rate per m² rather than a surface)
  - sgt1935 Tabarka terraces_number: not_applicable — printed text: Tabarka: "Produits affermés" across columns 1-5, then 6.000
  - sgt1935 Tabarka terraces_surface_m2: not_applicable — printed text: Tabarka: "Produits affermés" across columns 1-5, then 6.000
  - sgt1935 Tabarka terraces_receipts: not_applicable — printed text: Tabarka: "Produits affermés" across columns 1-5, then 6.000
  - sgt1935 Tabarka stalls_number: not_applicable — printed text: Tabarka: "Produits affermés" across columns 1-5, then 6.000
  - sgt1935 Tabarka stalls_surface_m2: not_applicable — printed text: Tabarka: "Produits affermés" across columns 1-5, then 6.000
  - sgt1935 Zaghouan terraces_number: not_applicable — printed text: Zaghouan: "Produits affermés" across columns 1-5, then 1.350
  - sgt1935 Zaghouan terraces_surface_m2: not_applicable — printed text: Zaghouan: "Produits affermés" across columns 1-5, then 1.350
  - sgt1935 Zaghouan terraces_receipts: not_applicable — printed text: Zaghouan: "Produits affermés" across columns 1-5, then 1.350
  - sgt1935 Zaghouan stalls_number: not_applicable — printed text: Zaghouan: "Produits affermés" across columns 1-5, then 1.350
  - sgt1935 Zaghouan stalls_surface_m2: not_applicable — printed text: Zaghouan: "Produits affermés" across columns 1-5, then 1.350
