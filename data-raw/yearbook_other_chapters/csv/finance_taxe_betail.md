# Taxe sur le bétail. Nombre d'animaux de chaque espèce

*Livestock tax (taxe sur le bétail): animals on the rolls by caïdat and species, young exempt and taxable, European and indigenous rolls.*

Source: *Statistique générale de la Tunisie*, chapter *Finances*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 200, f224, p. 201, f225, p. 202, f226, p. 203, f227; sgt1923 (`bpt6k9105649x`): p. 212, f714, p. 213, f715, p. 214, f716, p. 215, f717; sgt1924 (`bpt6k9105649x`): p. 220, f1210, p. 221, f1211, p. 222, f1212, p. 223, f1213; sgt1925 (`bpt6k9105650k`): p. 256, f280, p. 257, f281, p. 258, f282, p. 259, f283; sgt1926 (`bpt6k9105650k`): p. 232, f796, p. 233, f797, p. 234, f798, p. 235, f799.

Transcriptions: `../transcribed/finance_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_finance.py build`.

Rows: 5360. Years: 1922, 1923, 1924, 1925, 1926.

Unit: number of animals (head); value_type: count.

Printed once per edition, each printing for its own period (cumulative to a later year, or another tax year): every edition is kept (SPEC_ADDENDUM rule 5); `census` is the edition, `year` the year the printing refers to.

## Columns

- `census`: edition (source code; every edition printing the table is kept, rule 5)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the rolls (no year printed: the edition year)
- `region`: région as printed (sgt1925, sgt1926: 1re-5me Région, Territoires militaires du Sud); empty in sgt1922-sgt1924, which list caïdats only
- `controle_civil`: contrôle civil as printed (sgt1925, sgt1926; empty for the Territoires militaires du Sud and in sgt1922-sgt1924)
- `caidat`: caïdat as printed in that roll (the two rolls of one edition do not always use the same lines: see the notes); "Cap-Bon - Nabeul" and "Cap-Bon - Soliman" = the two lines printed under the brace of the caïdat Cap-Bon (contrôle civil of Grombalia, sgt1925, sgt1926)
- `roll`: `european` (a) Rôles européens) or `indigenous` (b) Rôles indigènes)
- `roll_fr`: printed table heading
- `species`: `horse` (chevaline), `camel` (cameline), `cattle` (bovine), `mule` (mulassière), `pig` (porcine), `donkey` (asine), `goat` (caprine), `sheep` (ovine)
- `species_fr`: printed column-group heading
- `age_class`: `young_exempt` (jeunes non imposables) or `taxable` (imposables)
- `age_class_fr`: printed column heading
- `value`: number of animals on the rolls
- `flag`: empty, or `total_mismatch` (printed value kept; identified by the row Total, the column Totaux and the Récapitulation as the faulty cell), `derived_from_totals` (sgt1925 a) Banlieue and Zaghouan: value = c) Récapitulation - b), see the notes)

Printed in sgt1922-sgt1926 only (no taxe sur le bétail from sgt1927), as three two-page spreads: a) Rôles européens, b) Rôles indigènes, c) Récapitulation, each "Nombre d'animaux de chaque espèce" by caïdat (sgt1922-sgt1924, 31 or 32 lines; sgt1925, sgt1926 by région, contrôle civil and caïdat, 36 lines) for eight species (chevaline, cameline, bovine, mulassière, porcine, asine, caprine, ovine), each in Jeunes non imposables, Imposables and Total. No year is printed: `year` is the edition year. sgt1922-sgt1924 add an Observations column, filled only in b): "L'impôt est dû pour les porcins à partir du 1er janvier qui suit le sevrage et pour les animaux des autres espèces, à partir du 1er janvier qui suit le commencement de la perte des dents de lait" (the tax is due for pigs from the 1 January after weaning, for the other species from the 1 January after the first milk teeth are lost).

Stored: a) and b), Jeunes non imposables and Imposables, every printed line. Not stored (checks only): the species Total columns, the Totaux line, and c) the Récapitulation, which is a) + b) cell by cell and carries nothing that the two rolls do not (it groups some lines differently: sgt1922 "L'Arad et Djerba" = a) L'Arad et Djerba + b) Gabès and Djerba; sgt1923, sgt1924 "L'Arad" = a) L'Arad + b) Gabès; its labels Majeurs, Hammama, Djérid are the Madjeurs, Hemmama/Hammama, Djerid of the rolls). The two rolls of one edition do not always print the same lines (sgt1922 a) L'Arad et Djerba, b) Gabès and Djerba; b) Gabès where a) prints L'Arad in sgt1923, sgt1924) and spell some caïdats differently (Hemmama / Hammama; sgt1925, sgt1926 contrôle "Teboursouk" in a), "Téboursouk" in b)): `caidat` keeps the label printed in each roll. sgt1925, sgt1926: the caïdat Cap-Bon (contrôle civil of Grombalia) is printed as a brace over two lines, Nabeul and Soliman, stored as "Cap-Bon - Nabeul" and "Cap-Bon - Soliman".

The mulassière Total of sgt1922 and sgt1923 is printed in the gutter and cut on both views of the spread; it is a check column only (left '?', the Jeunes + Imposables = Total check is skipped there; its Totaux are legible). The bold figures of the Totaux lines (1 and 4 alike) were read with the column sums.

sgt1925 a), f281: the porcine, asine, caprine and ovine cells of Banlieue and Zaghouan are printed identical, figure for figure, to those of Cap-Bon - Nabeul and Cap-Bon - Soliman two lines below (a line pair set twice); the column Totaux and the Récapitulation do not include them. These cells are derived as c) Récapitulation - b) Rôles indigènes (Jeunes and Total; Imposables = Total - Jeunes; flag `derived_from_totals`): Banlieue porcine 904 / 1.831, asine 25 / 350, caprine 709 / 3.312; Zaghouan porcine 114 / 143, asine 15 / 98, caprine 326 / 953, ovine 702 / 1.928; with them the a) column Totaux of porcine, asine and caprine agree. Banlieue ovine cannot be derived (the Récapitulation line prints 11.918 + 34.793 = 45.715, which does not add up; the a) Totaux point to about 2.503 + 5.425 = 7.929): the printed 156 and 328 are kept, flagged `total_mismatch`.

Image reading: every cell of a), b) and c) of every edition read on native-resolution crops of the page images (whole rows in strips, every failing check re-read zoomed). The Gallica OCR served only to draft the grids of sgt1922 and sgt1923; no cell is flagged `ocr_corrected` (no token-by-token OCR comparison was made).

Every failure was re-read on zoomed native-resolution crops. Stored cells identified as faulty (printed value kept, flag `total_mismatch`; the row Total, the column Totaux and the Récapitulation all point to the same cell): sgt1922 a) Bizerte ovine jeunes 1.614 (1.644), b) Ouerghemma caprine imposables 26.756 (26.576); sgt1923 b) Ouerghemma cameline imposables 1.735 (17.735); sgt1925 a) Aïn-Draham bovine imposables 4.122 (422), Medjez-el-Bab caprine imposables 822 (1.822), Banlieue ovine jeunes and imposables (see above); sgt1925 b) Mateur caprine imposables 1.855 (18.555), Banlieue bovine jeunes 2.003 (2.300) and caprine imposables 17.100 (17.110), Oulad Aoun bovine imposables 1.382 (10.382), Kairouan cameline imposables 5.006 (5.600), Matmata cameline jeunes 92 (62) and caprine jeunes 2.005 (2.500), Souk-el-Khemis ovine jeunes 5.772 (5.752), Souassi ovine jeunes 11.625 (11.626); sgt1926 a) Oulad Ayar chevaline jeunes 43 (13), Béja porcine imposables 2.697 (2.607). The other failures involve check figures only: misprinted species Totals (sgt1922 a) Banlieue caprine 3.528, Bizerte caprine 141; sgt1924 a) Gafsa ovine 334, b) Nefzaoua caprine 30.223; sgt1925 b) Zaghouan cameline 1.576, Sousse mulassière 2.363, Ourghemma asine 3.938, Madjeurs ovine 62.125; sgt1926 a) Mateur chevaline 797, Djelass bovine 408), misprinted Totaux (sgt1922 a) caprine total and ovine jeunes follow the faulty cells; sgt1924 a) bovine imposables 44.150 for 41.150; sgt1925 a) mulassière total 107.665 for 10.765, ovine total 70.713; the sgt1925 b) Totaux are right once the faulty cells and Totals are corrected), the Totaux of a) ovine in sgt1925 (the Banlieue line), and misprints of the Récapitulation itself (sgt1922 Monastir chevaline jeunes 55, Sousse cameline total 5.683, Kairouan chevaline imposables 2.204, Béja ovine imposables 35.611; sgt1923 L'Arad porcine total 2, Souassi ovine imposables 47.694, Téboursouk ovine imposables 12.782, and the Totaux line, where asine total 167.421 and caprine jeunes 123.034 are printed in each other's column; sgt1924 none beyond those following a) and b); sgt1925 Souk-el-Arba bovine jeunes 2.197, Nabeul chevaline total 3.563, Téboursouk cameline imposables 147, Tadjérouine bovine total 6.121, Mahdia cameline jeunes 304, Djebéniana bovine imposables 1.498, caprine jeunes 183 and total 2.317, Aïn-Draham porcine total 4.007, Fraichiches asine imposables 311, Zaghouan mulassière total 1.670, Madjeurs ovine jeunes 20.171, Banlieue ovine, and Totaux lines following these; sgt1925 c) Totaux mulassière 33.016 = 10.765 + 22.251, i.e. the correct sum, against the misprinted a) Totaux). Where a Récapitulation cell differs from a) + b) because a stored cell is faulty, it confirms the corrected figure given above in every case.

Survey of the whole chapter in every edition: `finance_survey.md`.

## Validation

- Checks against printed totals and identities: 8297; passed: 8142; failed: 155.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 european Banlieue (Tunis) Caprine: Jeunes + Imposables = Total: cells give 3523, printed 3528 (difference 5)
  - sgt1922 european Bizerte Caprine: Jeunes + Imposables = Total: cells give 441, printed 141 (difference -300)
  - sgt1922 european Bizerte Ovine: Jeunes + Imposables = Total: cells give 6132, printed 6162 (difference 30)
  - sgt1922 european Totaux cpt: sum of the lines: cells give 16620, printed 16915 (difference 295)
  - sgt1922 european Totaux ovj: sum of the lines: cells give 20445, printed 20475 (difference 30)
  - sgt1922 indigenous Ouerghemma Caprine: Jeunes + Imposables = Total: cells give 34991, printed 34811 (difference -180)
  - sgt1922 indigenous Totaux cpi: sum of the lines: cells give 734448, printed 734268 (difference -180)
  - sgt1922 recap Monastir Chevaline: Jeunes + Imposables = Total: cells give 684, printed 644 (difference -40)
  - sgt1922 recap Sousse Cameline: Jeunes + Imposables = Total: cells give 5863, printed 5683 (difference -180)
  - sgt1922 recap Béja Ovine: Jeunes + Imposables = Total: cells give 46652, printed 46682 (difference 30)
  - sgt1922 recap Kairouan Chevaline: Jeunes + Imposables = Total: cells give 2507, printed 2543 (difference 36)
  - sgt1922 recap Totaux chj: sum of the lines: cells give 4489, printed 4449 (difference -40)
  - sgt1922 recap Totaux chi: sum of the lines: cells give 70705, printed 70741 (difference 36)
  - sgt1922 recap Totaux cat: sum of the lines: cells give 121720, printed 121900 (difference 180)
  - sgt1922 recap Totaux ovi: sum of the lines: cells give 1395427, printed 1395457 (difference 30)
  - sgt1922 recap Ouerghemma cpi: Récapitulation = a) + b): cells give 26889, printed 26709 (difference -180)
  - sgt1922 recap Monastir chj: Récapitulation = a) + b): cells give 15, printed 55 (difference 40)
  - sgt1922 recap Sousse cat: Récapitulation = a) + b): cells give 5863, printed 5683 (difference -180)
  - sgt1922 recap Banlieue (Tunis) cpt: Récapitulation = a) + b): cells give 24716, printed 24711 (difference -5)
  - sgt1922 recap Béja ovi: Récapitulation = a) + b): cells give 35641, printed 35611 (difference -30)
  - sgt1922 recap Bizerte cpt: Récapitulation = a) + b): cells give 11116, printed 11416 (difference 300)
  - sgt1922 recap Bizerte ovj: Récapitulation = a) + b): cells give 7768, printed 7798 (difference 30)
  - sgt1922 recap Kairouan chi: Récapitulation = a) + b): cells give 2240, printed 2204 (difference -36)
  - sgt1923 indigenous Ouerghemma Cameline: Jeunes + Imposables = Total: cells give 3874, printed 19874 (difference 16000)
  - sgt1923 indigenous Totaux cai: sum of the lines: cells give 90108, printed 106108 (difference 16000)
  - sgt1923 recap L'Arad Porcine: Jeunes + Imposables = Total: cells give 7, printed 2 (difference -5)
  - sgt1923 recap Souassi Ovine: Jeunes + Imposables = Total: cells give 54123, printed 54128 (difference 5)
  - sgt1923 recap Téboursouk Ovine: Jeunes + Imposables = Total: cells give 18318, printed 18324 (difference 6)
  - sgt1923 recap Totaux Asine: Jeunes + Imposables = Total: cells give 123034, printed 167421 (difference 44387)
  - sgt1923 recap Totaux Caprine: Jeunes + Imposables = Total: cells give 733000, printed 777387 (difference 44387)
  - sgt1923 recap Totaux pot: sum of the lines: cells give 12516, printed 12521 (difference 5)
  - sgt1923 recap Totaux ast: sum of the lines: cells give 123034, printed 167421 (difference 44387)
  - sgt1923 recap Totaux cpj: sum of the lines: cells give 167421, printed 123034 (difference -44387)
  - sgt1923 recap Totaux ovi: sum of the lines: cells give 1152079, printed 1152090 (difference 11)
  - sgt1923 recap Ouerghemma cai: Récapitulation = a) + b): cells give 1779, printed 17779 (difference 16000)
  - sgt1923 recap L'Arad pot: Récapitulation = a) + b): cells give 7, printed 2 (difference -5)
  - sgt1923 recap Souassi ovi: Récapitulation = a) + b): cells give 47699, printed 47694 (difference -5)
  - sgt1923 recap Téboursouk ovi: Récapitulation = a) + b): cells give 12788, printed 12782 (difference -6)
  - sgt1923 recap Totaux ast: Récapitulation = a) + b): cells give 123034, printed 167421 (difference 44387)
  - sgt1923 recap Totaux cpj: Récapitulation = a) + b): cells give 167421, printed 123034 (difference -44387)
  - sgt1924 european Gafsa Ovine: Jeunes + Imposables = Total: cells give 324, printed 334 (difference 10)
  - sgt1924 european Totaux Bovine: Jeunes + Imposables = Total: cells give 51890, printed 48890 (difference -3000)
  - sgt1924 european Totaux boi: sum of the lines: cells give 41150, printed 44150 (difference 3000)
  - sgt1924 european Totaux ovt: sum of the lines: cells give 62139, printed 62129 (difference -10)
  - sgt1924 indigenous Nefzaoua Caprine: Jeunes + Imposables = Total: cells give 30323, printed 30223 (difference -100)
  - sgt1924 indigenous Totaux cpt: sum of the lines: cells give 781937, printed 782037 (difference 100)
  - sgt1924 recap Nefzaoua cpt: Récapitulation = a) + b): cells give 30223, printed 30323 (difference 100)
  - sgt1924 recap Gafsa ovt: Récapitulation = a) + b): cells give 31780, printed 31770 (difference -10)
  - sgt1924 recap Totaux boi: Récapitulation = a) + b): cells give 326427, printed 323427 (difference -3000)
  - sgt1925 european 1re Région ; Tabarka ; Aïn-Draham Bovine: Jeunes + Imposables = Total: cells give 4316, printed 616 (difference -3700)
  - sgt1925 european 3me Région ; Medjez-el-Bab ; Medjez-el-Bab Caprine: Jeunes + Imposables = Total: cells give 1507, printed 2507 (difference 1000)
  - sgt1925 european Totaux Mulassière: Jeunes + Imposables = Total: cells give 10765, printed 107665 (difference 96900)
  - sgt1925 european Totaux Ovine: Jeunes + Imposables = Total: cells give 70712, printed 70713 (difference 1)
  - sgt1925 european Totaux boi: sum of the lines: cells give 45278, printed 41578 (difference -3700)
  - sgt1925 european Totaux mut: sum of the lines: cells give 10765, printed 107665 (difference 96900)
  - sgt1925 european Totaux cpi: sum of the lines: cells give 14853, printed 15853 (difference 1000)
  - sgt1925 european Totaux ovj: sum of the lines: cells give 17299, printed 19646 (difference 2347)
  - sgt1925 european Totaux ovi: sum of the lines: cells give 45969, printed 51066 (difference 5097)
  - sgt1925 european Totaux ovt: sum of the lines: cells give 63268, printed 70713 (difference 7445)
  - sgt1925 indigenous 1re Région ; Bizerte ; Mateur Caprine: Jeunes + Imposables = Total: cells give 10949, printed 27649 (difference 16700)
  - sgt1925 indigenous 1re Région ; Souk-el-Arba ; Souk-el-Khemis Ovine: Jeunes + Imposables = Total: cells give 16545, printed 16525 (difference -20)
  - sgt1925 indigenous 2me Région ; Tunis ; Banlieue Bovine: Jeunes + Imposables = Total: cells give 21620, printed 21917 (difference 297)
  - sgt1925 indigenous 2me Région ; Tunis ; Banlieue Caprine: Jeunes + Imposables = Total: cells give 23111, printed 23121 (difference 10)
  - sgt1925 indigenous 2me Région ; Zaghouan ; Zaghouan Cameline: Jeunes + Imposables = Total: cells give 1574, printed 1576 (difference 2)
  - sgt1925 indigenous 3me Région ; Mactar ; Oulad Aoun Bovine: Jeunes + Imposables = Total: cells give 2792, printed 11792 (difference 9000)
  - sgt1925 indigenous 4me Région ; Sousse ; Souassi Ovine: Jeunes + Imposables = Total: cells give 49880, printed 49881 (difference 1)
  - sgt1925 indigenous 4me Région ; Sousse ; Sousse Mulassière: Jeunes + Imposables = Total: cells give 2369, printed 2363 (difference -6)
  - sgt1925 indigenous 4me Région ; Kairouan ; Kairouan Cameline: Jeunes + Imposables = Total: cells give 5524, printed 6118 (difference 594)
  - sgt1925 indigenous 4me Région ; Thala ; Madjeurs Ovine: Jeunes + Imposables = Total: cells give 62126, printed 62125 (difference -1)
  - sgt1925 indigenous Territoires militaires du Sud ;  ; Ourghemma Asine: Jeunes + Imposables = Total: cells give 3948, printed 3938 (difference -10)
  - sgt1925 indigenous Territoires militaires du Sud ;  ; Matmata Cameline: Jeunes + Imposables = Total: cells give 3373, printed 3343 (difference -30)
  - sgt1925 indigenous Territoires militaires du Sud ;  ; Matmata Caprine: Jeunes + Imposables = Total: cells give 18305, printed 18800 (difference 495)
  - sgt1925 indigenous Totaux caj: sum of the lines: cells give 8600, printed 8570 (difference -30)
  - sgt1925 indigenous Totaux cai: sum of the lines: cells give 108253, printed 108847 (difference 594)
  - sgt1925 indigenous Totaux cat: sum of the lines: cells give 117419, printed 117417 (difference -2)
  - sgt1925 indigenous Totaux boj: sum of the lines: cells give 53098, printed 53395 (difference 297)
  - sgt1925 indigenous Totaux boi: sum of the lines: cells give 257479, printed 266479 (difference 9000)
  - sgt1925 indigenous Totaux mut: sum of the lines: cells give 22245, printed 22251 (difference 6)
  - sgt1925 indigenous Totaux ast: sum of the lines: cells give 116456, printed 116466 (difference 10)
  - sgt1925 indigenous Totaux cpj: sum of the lines: cells give 250205, printed 250700 (difference 495)
  - sgt1925 indigenous Totaux cpi: sum of the lines: cells give 562380, printed 579090 (difference 16710)
  - sgt1925 indigenous Totaux ovj: sum of the lines: cells give 337081, printed 337062 (difference -19)
  - sgt1925 indigenous Totaux ovt: sum of the lines: cells give 1257973, printed 1257974 (difference 1)
  - sgt1925 recap 1re Région ; Tabarka ; Aïn-Draham Porcine: Jeunes + Imposables = Total: cells give 4700, printed 4007 (difference -693)
  - sgt1925 recap 1re Région ; Souk-el-Arba ; Souk-el-Arba Bovine: Jeunes + Imposables = Total: cells give 18362, printed 18352 (difference -10)
  - sgt1925 recap 2me Région ; Tunis ; Banlieue Ovine: Jeunes + Imposables = Total: cells give 46711, printed 45715 (difference -996)
  - sgt1925 recap 2me Région ; Zaghouan ; Zaghouan Mulassière: Jeunes + Imposables = Total: cells give 1672, printed 1670 (difference -2)
  - sgt1925 recap 2me Région ; Grombalia ; Cap-Bon - Nabeul Chevaline: Jeunes + Imposables = Total: cells give 2563, printed 3563 (difference 1000)
  - sgt1925 recap 3me Région ; Téboursouk ; Téboursouk Cameline: Jeunes + Imposables = Total: cells give 164, printed 163 (difference -1)
  - sgt1925 recap 3me Région ; Le Kef ; Tadjérouine Bovine: Jeunes + Imposables = Total: cells give 6721, printed 6121 (difference -600)
  - sgt1925 recap 4me Région ; Sousse ; Mahdia Cameline: Jeunes + Imposables = Total: cells give 5895, printed 5905 (difference 10)
  - sgt1925 recap 4me Région ; Thala ; Fraichiches Asine: Jeunes + Imposables = Total: cells give 502, printed 3202 (difference 2700)
  - sgt1925 recap 4me Région ; Thala ; Madjeurs Ovine: Jeunes + Imposables = Total: cells give 64334, printed 64339 (difference 5)
  - sgt1925 recap 5me Région ; Sfax ; Djebéniana Bovine: Jeunes + Imposables = Total: cells give 1728, printed 1718 (difference -10)
  - sgt1925 recap 5me Région ; Sfax ; Djebéniana Caprine: Jeunes + Imposables = Total: cells give 2013, printed 2317 (difference 304)
  - sgt1925 recap Territoires militaires du Sud ;  ; Matmata Caprine: Jeunes + Imposables = Total: cells give 18305, printed 18800 (difference 495)
  - sgt1925 recap Totaux Cameline: Jeunes + Imposables = Total: cells give 117694, printed 117703 (difference 9)
  - sgt1925 recap Totaux cht: sum of the lines: cells give 73456, printed 72456 (difference -1000)
  - sgt1925 recap Totaux caj: sum of the lines: cells give 8569, printed 8570 (difference 1)
  - sgt1925 recap Totaux cai: sum of the lines: cells give 109125, printed 109124 (difference -1)
  - sgt1925 recap Totaux boj: sum of the lines: cells give 61600, printed 61590 (difference -10)
  - sgt1925 recap Totaux boi: sum of the lines: cells give 308067, printed 308057 (difference -10)
  - sgt1925 recap Totaux bot: sum of the lines: cells give 369047, printed 369647 (difference 600)
  - sgt1925 recap Totaux mut: sum of the lines: cells give 33014, printed 33016 (difference 2)
  - sgt1925 recap Totaux pot: sum of the lines: cells give 19014, printed 19707 (difference 693)
  - sgt1925 recap Totaux asi: sum of the lines: cells give 110737, printed 113437 (difference 2700)
  - sgt1925 recap Totaux cpj: sum of the lines: cells give 254657, printed 255452 (difference 795)
  - sgt1925 recap Totaux cpt: sum of the lines: cells give 850399, printed 850395 (difference -4)
  - sgt1925 recap Totaux ovj: sum of the lines: cells give 356704, printed 356709 (difference 5)
  - sgt1925 recap Totaux ovi: sum of the lines: cells give 971974, printed 971978 (difference 4)
  - sgt1925 recap Totaux ovt: sum of the lines: cells give 1327687, printed 1328687 (difference 1000)
  - sgt1925 recap 1re Région ; Bizerte ; Mateur cpi: Récapitulation = a) + b): cells give 3334, printed 20034 (difference 16700)
  - sgt1925 recap 1re Région ; Tabarka ; Aïn-Draham boi: Récapitulation = a) + b): cells give 18012, printed 14312 (difference -3700)
  - sgt1925 recap 1re Région ; Tabarka ; Aïn-Draham pot: Récapitulation = a) + b): cells give 4700, printed 4007 (difference -693)
  - sgt1925 recap 1re Région ; Souk-el-Arba ; Souk-el-Arba boj: Récapitulation = a) + b): cells give 2187, printed 2197 (difference 10)
  - sgt1925 recap 1re Région ; Souk-el-Arba ; Souk-el-Khemis ovj: Récapitulation = a) + b): cells give 6577, printed 6557 (difference -20)
  - sgt1925 recap 2me Région ; Tunis ; Banlieue boj: Récapitulation = a) + b): cells give 3773, printed 4070 (difference 297)
  - sgt1925 recap 2me Région ; Tunis ; Banlieue cpi: Récapitulation = a) + b): cells give 20412, printed 20422 (difference 10)
  - sgt1925 recap 2me Région ; Tunis ; Banlieue ovj: Récapitulation = a) + b): cells give 9570, printed 11918 (difference 2348)
  - sgt1925 recap 2me Région ; Tunis ; Banlieue ovi: Récapitulation = a) + b): cells give 29700, printed 34793 (difference 5093)
  - sgt1925 recap 2me Région ; Tunis ; Banlieue ovt: Récapitulation = a) + b): cells give 39270, printed 45715 (difference 6445)
  - sgt1925 recap 2me Région ; Zaghouan ; Zaghouan cat: Récapitulation = a) + b): cells give 1578, printed 1576 (difference -2)
  - sgt1925 recap 2me Région ; Zaghouan ; Zaghouan mut: Récapitulation = a) + b): cells give 1672, printed 1670 (difference -2)
  - sgt1925 recap 2me Région ; Grombalia ; Cap-Bon - Nabeul cht: Récapitulation = a) + b): cells give 2563, printed 3563 (difference 1000)
  - sgt1925 recap 3me Région ; Téboursouk ; Téboursouk cai: Récapitulation = a) + b): cells give 146, printed 147 (difference 1)
  - sgt1925 recap 3me Région ; Le Kef ; Tadjérouine bot: Récapitulation = a) + b): cells give 6721, printed 6121 (difference -600)
  - sgt1925 recap 3me Région ; Mactar ; Oulad Aoun boi: Récapitulation = a) + b): cells give 1452, printed 10452 (difference 9000)
  - sgt1925 recap 3me Région ; Medjez-el-Bab ; Medjez-el-Bab cpi: Récapitulation = a) + b): cells give 40386, printed 41386 (difference 1000)
  - sgt1925 recap 4me Région ; Sousse ; Souassi ovj: Récapitulation = a) + b): cells give 11625, printed 11626 (difference 1)
  - sgt1925 recap 4me Région ; Sousse ; Mahdia caj: Récapitulation = a) + b): cells give 314, printed 304 (difference -10)
  - sgt1925 recap 4me Région ; Sousse ; Sousse mut: Récapitulation = a) + b): cells give 2608, printed 2614 (difference 6)
  - sgt1925 recap 4me Région ; Kairouan ; Kairouan cai: Récapitulation = a) + b): cells give 5013, printed 5607 (difference 594)
  - sgt1925 recap 4me Région ; Thala ; Fraichiches asi: Récapitulation = a) + b): cells give 3011, printed 311 (difference -2700)
  - sgt1925 recap 4me Région ; Thala ; Madjeurs ovj: Récapitulation = a) + b): cells give 20176, printed 20171 (difference -5)
  - sgt1925 recap 4me Région ; Thala ; Madjeurs ovt: Récapitulation = a) + b): cells give 64338, printed 64339 (difference 1)
  - sgt1925 recap 5me Région ; Sfax ; Djebéniana boi: Récapitulation = a) + b): cells give 1488, printed 1498 (difference 10)
  - sgt1925 recap 5me Région ; Sfax ; Djebéniana cpj: Récapitulation = a) + b): cells give 483, printed 183 (difference -300)
  - sgt1925 recap 5me Région ; Sfax ; Djebéniana cpt: Récapitulation = a) + b): cells give 2313, printed 2317 (difference 4)
  - sgt1925 recap Territoires militaires du Sud ;  ; Ourghemma ast: Récapitulation = a) + b): cells give 3948, printed 3958 (difference 10)
  - sgt1925 recap Territoires militaires du Sud ;  ; Matmata caj: Récapitulation = a) + b): cells give 92, printed 62 (difference -30)
  - sgt1925 recap Totaux caj: Récapitulation = a) + b): cells give 8579, printed 8570 (difference -9)
  - sgt1925 recap Totaux mut: Récapitulation = a) + b): cells give 129916, printed 33016 (difference -96900)
  - sgt1925 recap Totaux ovj: Récapitulation = a) + b): cells give 356708, printed 356709 (difference 1)
  - sgt1926 european 1re Région ; Béja ; Béja Porcine: Jeunes + Imposables = Total: cells give 4533, printed 4443 (difference -90)
  - sgt1926 european 1re Région ; Bizerte ; Mateur Chevaline: Jeunes + Imposables = Total: cells give 697, printed 797 (difference 100)
  - sgt1926 european 3me Région ; Mactar ; Oulad Ayar Chevaline: Jeunes + Imposables = Total: cells give 75, printed 45 (difference -30)
  - sgt1926 european 4me Région ; Kairouan ; Djelass Bovine: Jeunes + Imposables = Total: cells give 400, printed 408 (difference 8)
  - sgt1926 european Totaux chj: sum of the lines: cells give 966, printed 936 (difference -30)
  - sgt1926 european Totaux cht: sum of the lines: cells give 10082, printed 9982 (difference -100)
  - sgt1926 european Totaux bot: sum of the lines: cells give 55887, printed 55879 (difference -8)
  - sgt1926 european Totaux poi: sum of the lines: cells give 14372, printed 14282 (difference -90)
  - sgt1926 recap 1re Région ; Béja ; Béja poi: Récapitulation = a) + b): cells give 2697, printed 2607 (difference -90)
  - sgt1926 recap 1re Région ; Bizerte ; Mateur cht: Récapitulation = a) + b): cells give 6231, printed 6131 (difference -100)
  - sgt1926 recap 3me Région ; Mactar ; Oulad Ayar chj: Récapitulation = a) + b): cells give 56, printed 26 (difference -30)
  - sgt1926 recap 4me Région ; Kairouan ; Djelass bot: Récapitulation = a) + b): cells give 12398, printed 12390 (difference -8)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: derived_from_totals: 14, total_mismatch: 18.

  - sgt1922 p.201 1922  /  / Bizerte / european / sheep / young_exempt = 1614 (total_mismatch)
  - sgt1922 p.203 1922  /  / Ouerghemma / indigenous / goat / taxable = 26756 (total_mismatch)
  - sgt1923 p.214 1923  /  / Ouerghemma / indigenous / camel / taxable = 1735 (total_mismatch)
  - sgt1925 p.256 1925 1re Région / Tabarka / Aïn-Draham / european / cattle / taxable = 4122 (total_mismatch)
  - sgt1925 p.257 1925 2me Région / Tunis / Banlieue / european / pig / young_exempt = 904 (derived_from_totals)
  - sgt1925 p.257 1925 2me Région / Tunis / Banlieue / european / pig / taxable = 1831 (derived_from_totals)
  - sgt1925 p.257 1925 2me Région / Tunis / Banlieue / european / donkey / young_exempt = 25 (derived_from_totals)
  - sgt1925 p.257 1925 2me Région / Tunis / Banlieue / european / donkey / taxable = 350 (derived_from_totals)
  - sgt1925 p.257 1925 2me Région / Tunis / Banlieue / european / goat / young_exempt = 709 (derived_from_totals)
  - sgt1925 p.257 1925 2me Région / Tunis / Banlieue / european / goat / taxable = 3312 (derived_from_totals)
  - sgt1925 p.257 1925 2me Région / Tunis / Banlieue / european / sheep / young_exempt = 156 (total_mismatch)
  - sgt1925 p.257 1925 2me Région / Tunis / Banlieue / european / sheep / taxable = 328 (total_mismatch)
  - sgt1925 p.257 1925 2me Région / Zaghouan / Zaghouan / european / pig / young_exempt = 114 (derived_from_totals)
  - sgt1925 p.257 1925 2me Région / Zaghouan / Zaghouan / european / pig / taxable = 143 (derived_from_totals)
  - sgt1925 p.257 1925 2me Région / Zaghouan / Zaghouan / european / donkey / young_exempt = 15 (derived_from_totals)
  - sgt1925 p.257 1925 2me Région / Zaghouan / Zaghouan / european / donkey / taxable = 98 (derived_from_totals)
  - sgt1925 p.257 1925 2me Région / Zaghouan / Zaghouan / european / goat / young_exempt = 326 (derived_from_totals)
  - sgt1925 p.257 1925 2me Région / Zaghouan / Zaghouan / european / goat / taxable = 953 (derived_from_totals)
  - sgt1925 p.257 1925 2me Région / Zaghouan / Zaghouan / european / sheep / young_exempt = 702 (derived_from_totals)
  - sgt1925 p.257 1925 2me Région / Zaghouan / Zaghouan / european / sheep / taxable = 1928 (derived_from_totals)
  - sgt1925 p.257 1925 3me Région / Medjez-el-Bab / Medjez-el-Bab / european / goat / taxable = 822 (total_mismatch)
  - sgt1925 p.258 1925 2me Région / Tunis / Banlieue / indigenous / cattle / young_exempt = 2003 (total_mismatch)
  - sgt1925 p.258 1925 3me Région / Mactar / Oulad Aoun / indigenous / cattle / taxable = 1382 (total_mismatch)
  - sgt1925 p.258 1925 4me Région / Kairouan / Kairouan / indigenous / camel / taxable = 5006 (total_mismatch)
  - sgt1925 p.258 1925 Territoires militaires du Sud /  / Matmata / indigenous / camel / young_exempt = 92 (total_mismatch)
  - sgt1925 p.259 1925 1re Région / Bizerte / Mateur / indigenous / goat / taxable = 1855 (total_mismatch)
  - sgt1925 p.259 1925 1re Région / Souk-el-Arba / Souk-el-Khemis / indigenous / sheep / young_exempt = 5772 (total_mismatch)
  - sgt1925 p.259 1925 2me Région / Tunis / Banlieue / indigenous / goat / taxable = 17100 (total_mismatch)
  - sgt1925 p.259 1925 4me Région / Sousse / Souassi / indigenous / sheep / young_exempt = 11625 (total_mismatch)
  - sgt1925 p.259 1925 Territoires militaires du Sud /  / Matmata / indigenous / goat / young_exempt = 2005 (total_mismatch)
  - sgt1926 p.232 1926 3me Région / Mactar / Oulad Ayar / european / horse / young_exempt = 43 (total_mismatch)
  - sgt1926 p.233 1926 1re Région / Béja / Béja / european / pig / taxable = 2697 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (30 printings): sgt1922 f224, sgt1922 f225, sgt1922 f226, sgt1922 f227, sgt1922 f228, sgt1922 f229, sgt1923 f714, sgt1923 f715, sgt1923 f716, sgt1923 f717, sgt1923 f718, sgt1923 f719, sgt1924 f1210, sgt1924 f1211, sgt1924 f1212, sgt1924 f1213, sgt1924 f1214, sgt1924 f1215, sgt1925 f280, sgt1925 f281, sgt1925 f282, sgt1925 f283, sgt1925 f284, sgt1925 f285, sgt1926 f796, sgt1926 f797, sgt1926 f798, sgt1926 f799, sgt1926 f800, sgt1926 f801.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
