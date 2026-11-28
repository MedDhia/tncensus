# Droit de patente. Etat des assujettis au droit de patente

*Business licence tax (droit de patente): taxpayers by caïdat and class of profit.*

Source: *Statistique générale de la Tunisie*, chapter *Finances*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 198, f222, p. 199, f223; sgt1923 (`bpt6k9105649x`): p. 210, f712, p. 211, f713; sgt1924 (`bpt6k9105649x`): p. 218, f1208, p. 219, f1209; sgt1925 (`bpt6k9105650k`): p. 254, f278, p. 255, f279; sgt1926 (`bpt6k9105650k`): p. 230, f794, p. 231, f795; sgt1927 (`bpt6k91056510`): p. 228, f256, p. 229, f257; sgt1928 (`bpt6k91056510`): p. 228, f780, p. 229, f781; sgt1929 (`bpt6k9105652d`): p. 231, f259; sgt1930 (`bpt6k9105652d`): p. 235, f793.

Transcriptions: `../transcribed/finance_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_finance.py build`.

Rows: 6985. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930.

Unit: number of taxpayers (assujettis); value_type: count.

Printed once per edition, each printing for its own period (cumulative to a later year, or another tax year): every edition is kept (SPEC_ADDENDUM rule 5); `census` is the edition, `year` the year the printing refers to.

## Columns

- `census`: edition (source code; every edition printing the table is kept, rule 5)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: tax year ("imposés en <year>"; sgt1922-sgt1925 print no year: the edition year)
- `profits_year`: year of the profits taxed ("bénéfices de <year>"), when the title prints it; empty otherwise
- `region`: région as printed (sgt1925 on; "Territoires militaires du Sud" for the southern caïdats); empty when the table lists caïdats only
- `controle_civil`: contrôle civil as printed (sgt1925 on); empty when the table lists caïdats only
- `caidat`: caïdat as printed
- `profit_class`: class of profit (1 to 15)
- `profit_class_fr`: printed column head: class, bracket of profit and bénéfice moyen
- `mean_profit`: bénéfice moyen of the class (francs), as printed in the column head
- `value`: number of taxpayers (assujettis) in the class
- `flag`: empty, or `ocr_corrected` (image reading differs from the Gallica OCR), `total_mismatch` (printed value kept; identified by a failed check as the faulty cell, see Validation), `illegible` (value NA), `not_applicable` (nothing printed, value NA), `derived_from_totals` (digits hidden in the binding; value = the printed row total minus the other cells of the row, see the notes)

Printed in every edition sgt1922-sgt1930 as a two-page spread (sgt1922-sgt1924 with the right-hand page scanned sideways; sgt1929 and sgt1930 on a folding plate, f259 and f793). Rows: caïdats (sgt1922-sgt1924, 25 to 33 caïdats, labels as printed, e.g. "Kef (le)-Tadjerouine", "Tunis et Banlieue"); from sgt1925 by région (1re-5me Région and Territoires militaires du Sud; from sgt1928 named by the chef-lieu de région, Bizerte, Tunis, Le Kef, Sousse, Sfax), contrôle civil and caïdat. The tax year is printed from sgt1926 ("Bénéfices de l'année 1925 — Imposés en 1926", ...); sgt1922-sgt1925 print none (`year` = edition year, `profits_year` empty).

Columns: one per class of profit, with its bracket and bénéfice moyen. Scale A (sgt1922-sgt1928): 15 classes (1re: 0 à 1.000 fr., moyen 500 ... 15e: 3.000.001 à 4.000.000, moyen 3.500.000), a 16th (4.000.001 à 5.000.000, moyen 4.500.000) from sgt1927. Scale B (sgt1929, sgt1930): classes 1-10 as before, then brackets of 100.000 fr. (11e: 200.001 à 300.000, moyen 250.000 ... 51e: 4.200.001 à 4.300.000, moyen 4.250.000); sgt1930 prints the 1st to 50th class and a last column headed "53e classe" (4.400.001 à 4.500.000, moyen 4.450.000). `profit_class` and `mean_profit` follow the printed head, so the same class number means a different bracket in the two scales. Every printed cell is stored, » as 0 (most cells of the wide scale are 0).

sgt1927: the 4th class column is printed against the gutter and the last digit is hidden in the binding for L'Arad, Hemmama, Gafsa, Djerid, Djerba, Ouerghema and the Totaux; these cells are derived as Nombre de patentables minus the other classes of the row (flag `derived_from_totals`); the derived values agree with the visible leading digits, the Montant of each row and the column Totaux. The Nombre check is not counted for these rows.

Not stored (checks only): Nombre de patentables (row total), the Totaux line, and the Montant du bénéfice moyen par caïdat (sum over the classes of count x bénéfice moyen; left empty on the sgt1930 plate). From sgt1935 the table prints only these two columns per caïdat: see `finance_patente_caidat`.

Failed checks, each re-read on zoomed native-resolution crops (printed values kept). Every class column agrees with its printed Totaux except where a class cell is identified as faulty (flag `total_mismatch`): sgt1924 Ouerghemma 6th class printed » (the Nombre 590, the Montant 980.000 and the column Totaux 191 all require 1); sgt1925 Béja 1st class 433 (the Nombre 964 and, with Aïn-Rraham, the Totaux 15.953 require 443), Aïn-Rraham 1st class 133 (the Nombre 255 and the Montant 531.000 require 113), Djelass 2nd class 233 (the Nombre 933, the Montant 1.156.000 and the Totaux 11.819 require 238); sgt1928 Bizerte 3rd class 217 (the Nombre 1.617, the Montant 7.632.500 and the Totaux 6.160 require 257); sgt1929 Le Kef 6 in the 34th class and Ouerghemma 7 in the 50th class, sgt1930 Monastir 5 in the 34th class: isolated figures in otherwise empty columns, excluded by the Nombre, the Montant and the Totaux (stray type on the standing plate). The other failures are misprinted check figures, no stored cell involved: the Montant du bénéfice moyen of sgt1922 Gafsa (474.500; the classes give 710.500, which the Totaux montant 88.928.500 requires); sgt1923 Béja (+90.000), Monastir (-50.000), Tunis (-3.634.000) and the Totaux line (89.453.000, the sum of the printed Montants, against 93.047.000 from the classes, whose column totals all agree); sgt1925 Béja printed "2.466" (and the Totaux montant 133.429.000, which no reading of the Montant column reproduces); sgt1926 Souk-el-Arba (-3.000), Tunis banlieue (-473.000), Tadjérouine (-1.000), Mahdia (+500), La Skira (-170.000), Djebéniana (+256.500), L'Arad (-150.000) and the Totaux line; sgt1928 Souassi (291.000 for 291.500, and the Totaux montant by 500); sgt1930 Zlass Nombre printed 230 for 220 (the classes and the Totaux Nombre 36.560 require 220).

Survey of the whole chapter in every edition: `finance_survey.md`.

## Validation

- Checks against printed totals and identities: 787; passed: 746; failed: 41.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 Gafsa: Montant du bénéfice moyen = sum of count x bénéfice moyen: cells give 710500, printed 474500 (difference -236000)
  - sgt1922 Totaux montant: Totaux = sum of the caïdats: cells give 88692500, printed 88928500 (difference 236000)
  - sgt1923 Béja: Montant du bénéfice moyen = sum of count x bénéfice moyen: cells give 1502500, printed 1592500 (difference 90000)
  - sgt1923 Monastir: Montant du bénéfice moyen = sum of count x bénéfice moyen: cells give 1288000, printed 1238000 (difference -50000)
  - sgt1923 Tunis: Montant du bénéfice moyen = sum of count x bénéfice moyen: cells give 55345500, printed 51711500 (difference -3634000)
  - sgt1923 Totaux: Montant du bénéfice moyen = sum of count x bénéfice moyen: cells give 93047000, printed 89453000 (difference -3594000)
  - sgt1924 Ouerghemma: Nombre de patentables = sum of the classes: cells give 589, printed 590 (difference 1)
  - sgt1924 Ouerghemma: Montant du bénéfice moyen = sum of count x bénéfice moyen: cells give 955000, printed 980000 (difference 25000)
  - sgt1924 Totaux c6: Totaux = sum of the caïdats: cells give 190, printed 191 (difference 1)
  - sgt1925 1re Région ; Béja ; Béja: Nombre de patentables = sum of the classes: cells give 954, printed 964 (difference 10)
  - sgt1925 1re Région ; Béja ; Béja: Montant du bénéfice moyen = sum of count x bénéfice moyen: cells give 2451000, printed 2466 (difference -2448534)
  - sgt1925 1re Région ; Tabarka ; Aïn-Rraham: Nombre de patentables = sum of the classes: cells give 275, printed 255 (difference -20)
  - sgt1925 1re Région ; Tabarka ; Aïn-Rraham: Montant du bénéfice moyen = sum of count x bénéfice moyen: cells give 541000, printed 531000 (difference -10000)
  - sgt1925 4me Région ; Kairouan ; Djelass: Nombre de patentables = sum of the classes: cells give 928, printed 933 (difference 5)
  - sgt1925 4me Région ; Kairouan ; Djelass: Montant du bénéfice moyen = sum of count x bénéfice moyen: cells give 1148500, printed 1156000 (difference 7500)
  - sgt1925 Totaux c1: Totaux = sum of the caïdats: cells give 15963, printed 15953 (difference -10)
  - sgt1925 Totaux c2: Totaux = sum of the caïdats: cells give 11814, printed 11819 (difference 5)
  - sgt1925 Totaux montant: Totaux = sum of the caïdats: cells give 130975466, printed 133429000 (difference 2453534)
  - sgt1926 1re Région ; Souk-el-Arba ; Souk-el-Arba: Montant du bénéfice moyen = sum of count x bénéfice moyen: cells give 1681500, printed 1678500 (difference -3000)
  - sgt1926 2me Région ; Tunis ; Banlieue: Montant du bénéfice moyen = sum of count x bénéfice moyen: cells give 110044000, printed 109571000 (difference -473000)
  - sgt1926 3me Région ; Le Kef ; Tadjérouine: Montant du bénéfice moyen = sum of count x bénéfice moyen: cells give 554000, printed 553000 (difference -1000)
  - sgt1926 4me Région ; Sousse ; Mahdia: Montant du bénéfice moyen = sum of count x bénéfice moyen: cells give 1994000, printed 1994500 (difference 500)
  - sgt1926 5me Région ; Sfax ; La Skira: Montant du bénéfice moyen = sum of count x bénéfice moyen: cells give 357500, printed 187500 (difference -170000)
  - sgt1926 5me Région ; Sfax ; Djebéniana: Montant du bénéfice moyen = sum of count x bénéfice moyen: cells give 414500, printed 671000 (difference 256500)
  - sgt1926 5me Région ; Gabès ; L'Arad: Montant du bénéfice moyen = sum of count x bénéfice moyen: cells give 1593000, printed 1443000 (difference -150000)
  - sgt1926 Totaux: Montant du bénéfice moyen = sum of count x bénéfice moyen: cells give 165962000, printed 165422000 (difference -540000)
  - sgt1928 Bizerte ; Bizerte ; Bizerte: Nombre de patentables = sum of the classes: cells give 1577, printed 1617 (difference 40)
  - sgt1928 Bizerte ; Bizerte ; Bizerte: Montant du bénéfice moyen = sum of count x bénéfice moyen: cells give 7492500, printed 7632500 (difference 140000)
  - sgt1928 Sousse ; Sousse ; Souassi: Montant du bénéfice moyen = sum of count x bénéfice moyen: cells give 291500, printed 291000 (difference -500)
  - sgt1928 Totaux c3: Totaux = sum of the caïdats: cells give 6120, printed 6160 (difference 40)
  - sgt1928 Totaux montant: Totaux = sum of the caïdats: cells give 248960500, printed 248961000 (difference 500)
  - sgt1929 Le Kef ; Le Kef ; Le Kef: Nombre de patentables = sum of the classes: cells give 835, printed 829 (difference -6)
  - sgt1929 Le Kef ; Le Kef ; Le Kef: Montant du bénéfice moyen = sum of count x bénéfice moyen: cells give 17299000, printed 1999000 (difference -15300000)
  - sgt1929 Territoires militaire du Sud ;  ; Ouerghemma: Nombre de patentables = sum of the classes: cells give 175, printed 168 (difference -7)
  - sgt1929 Territoires militaire du Sud ;  ; Ouerghemma: Montant du bénéfice moyen = sum of count x bénéfice moyen: cells give 29387500, printed 337500 (difference -29050000)
  - sgt1929 Totaux c34: Totaux = sum of the caïdats: cells give 7, printed 1 (difference -6)
  - sgt1929 Totaux c50: Totaux = sum of the caïdats: cells give 7, printed 0 (difference -7)
  - sgt1930 Sousse ; Sousse ; Monastir: Nombre de patentables = sum of the classes: cells give 1238, printed 1233 (difference -5)
  - sgt1930 Sousse ; Kairouan ; Zlass: Nombre de patentables = sum of the classes: cells give 220, printed 230 (difference 10)
  - sgt1930 Totaux n: Totaux = sum of the caïdats: cells give 36570, printed 36560 (difference -10)
  - sgt1930 Totaux c34: Totaux = sum of the caïdats: cells give 6, printed 1 (difference -5)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: derived_from_totals: 6, ocr_corrected: 49, total_mismatch: 8.

  - sgt1922 p.198 1922  /  /  / Bizerte / 6 / 25000 = 7 (ocr_corrected)
  - sgt1922 p.198 1922  /  /  / Sousse / 6 / 25000 = 7 (ocr_corrected)
  - sgt1922 p.198 1922  /  /  / Tunis / 3 / 3500 = 1532 (ocr_corrected)
  - sgt1922 p.198 1922  /  /  / Tunis / 6 / 25000 = 118 (ocr_corrected)
  - sgt1922 p.199 1922  /  /  / Tunis / 7 / 40000 = 86 (ocr_corrected)
  - sgt1922 p.199 1922  /  /  / Tunis / 8 / 62500 = 49 (ocr_corrected)
  - sgt1923 p.210 1923  /  /  / Aïn-Draham / 1 / 500 = 88 (ocr_corrected)
  - sgt1923 p.210 1923  /  /  / Cap-Bon / 3 / 3500 = 78 (ocr_corrected)
  - sgt1923 p.210 1923  /  /  / Fraichiches-Majeurs / 2 / 1500 = 135 (ocr_corrected)
  - sgt1923 p.210 1923  /  /  / Souk-el-Arba / 4 / 7500 = 23 (ocr_corrected)
  - sgt1923 p.210 1923  /  /  / Sousse / 2 / 1500 = 1305 (ocr_corrected)
  - sgt1923 p.211 1923  /  /  / Tunis / 8 / 62500 = 52 (ocr_corrected)
  - sgt1924 p.218 1924  /  /  / Ouerghemma / 6 / 25000 = 0 (total_mismatch)
  - sgt1924 p.219 1924  /  /  / Tunis et Banlieue / 8 / 62500 = 54 (ocr_corrected)
  - sgt1925 p.254 1925  / 1re Région / Béja / Béja / 1 / 500 = 433 (total_mismatch)
  - sgt1925 p.254 1925  / 1re Région / Tabarka / Aïn-Rraham / 1 / 500 = 133 (total_mismatch)
  - sgt1925 p.254 1925  / 2me Région / Tunis / Banlieue / 2 / 1500 = 2933 (ocr_corrected)
  - sgt1925 p.254 1925  / 4me Région / Sousse / Sousse / 3 / 3500 = 505 (ocr_corrected)
  - sgt1925 p.254 1925  / 4me Région / Kairouan / Djelass / 2 / 1500 = 233 (total_mismatch)
  - sgt1925 p.254 1925  / 5me Région / Sfax / Sfax / 3 / 3500 = 417 (ocr_corrected)
  - sgt1925 p.254 1925  / 5me Région / Gabès / L'Arad / 1 / 500 = 353 (ocr_corrected)
  - sgt1925 p.254 1925  / 5me Région / Gafsa / Hemmama / 3 / 3500 = 70 (ocr_corrected)
  - sgt1925 p.254 1925  / Territoires militaires du Sud /  / Tataouine / 3 / 3500 = 61 (ocr_corrected)
  - sgt1925 p.255 1925  / 1re Région / Béja / Béja / 4 / 7500 = 37 (ocr_corrected)
  - sgt1925 p.255 1925  / 2me Région / Tunis / Banlieue / 4 / 7500 = 944 (ocr_corrected)
  - sgt1925 p.255 1925  / 2me Région / Tunis / Banlieue / 5 / 15000 = 354 (ocr_corrected)
  - sgt1925 p.255 1925  / 2me Région / Tunis / Banlieue / 6 / 25000 = 183 (ocr_corrected)
  - sgt1925 p.255 1925  / 2me Région / Tunis / Banlieue / 7 / 40000 = 128 (ocr_corrected)
  - sgt1925 p.255 1925  / 2me Région / Tunis / Banlieue / 8 / 62500 = 77 (ocr_corrected)
  - sgt1925 p.255 1925  / 2me Région / Tunis / Banlieue / 11 / 350000 = 37 (ocr_corrected)
  - sgt1925 p.255 1925  / 2me Région / Grombalia / Cap Bon / 4 / 7500 = 36 (ocr_corrected)
  - sgt1925 p.255 1925  / 4me Région / Sousse / Sousse / 4 / 7500 = 153 (ocr_corrected)
  - sgt1925 p.255 1925  / 5me Région / Sfax / Sfax / 4 / 7500 = 99 (ocr_corrected)
  - sgt1926 p.230 1926 1925 / 1re Région / Béja / Béja / 1 / 500 = 528 (ocr_corrected)
  - sgt1926 p.230 1926 1925 / 1re Région / Souk-el-Arba / Souk-el-Arba / 2 / 1500 = 235 (ocr_corrected)
  - sgt1926 p.230 1926 1925 / 2me Région / Grombalia / Cap Bon / 3 / 3500 = 320 (ocr_corrected)
  - sgt1926 p.230 1926 1925 / 4me Région / Sousse / Souassi / 3 / 3500 = 18 (ocr_corrected)
  - sgt1926 p.230 1926 1925 / 4me Région / Sousse / Sousse / 3 / 3500 = 574 (ocr_corrected)
  - sgt1926 p.230 1926 1925 / 5me Région / Gafsa / Gafsa / 1 / 500 = 180 (ocr_corrected)
  - sgt1926 p.231 1926 1925 / 2me Région / Tunis / Banlieue / 4 / 7500 = 982 (ocr_corrected)
  - sgt1926 p.231 1926 1925 / 5me Région / Gabès / L'Arad / 4 / 7500 = 26 (ocr_corrected)
  - sgt1927 p.228 1927 1926 / 1re Région / Bizerte / Bizerte / 4 / 7500 = 78 (ocr_corrected)
  - sgt1927 p.228 1927 1926 / 2me Région / Tunis / Tunis-Ville et banlieue / 2 / 1500 = 3144 (ocr_corrected)
  - sgt1927 p.228 1927 1926 / 2me Région / Tunis / Tunis-Ville et banlieue / 4 / 7500 = 936 (ocr_corrected)
  - sgt1927 p.228 1927 1926 / 5me Région / Gabès / L'Arad / 4 / 7500 = 30 (derived_from_totals)
  - sgt1927 p.228 1927 1926 / 5me Région / Gafsa / Hemmama / 4 / 7500 = 12 (derived_from_totals)
  - sgt1927 p.228 1927 1926 / 5me Région / Gafsa / Gafsa / 4 / 7500 = 33 (derived_from_totals)
  - sgt1927 p.228 1927 1926 / 5me Région / Tozeur / Djerid / 4 / 7500 = 24 (derived_from_totals)
  - sgt1927 p.228 1927 1926 / 5me Région / Djerba / Djerba / 4 / 7500 = 10 (derived_from_totals)
  - sgt1927 p.228 1927 1926 / Territoires militaires du Sud /  / Ouerghema / 4 / 7500 = 17 (derived_from_totals)
  - sgt1927 p.229 1927 1926 / 1re Région / Bizerte / Bizerte / 5 / 15000 = 48 (ocr_corrected)
  - sgt1927 p.229 1927 1926 / 2me Région / Tunis / Tunis-Ville et banlieue / 5 / 15000 = 544 (ocr_corrected)
  - sgt1928 p.228 1928 1927 / Bizerte / Bizerte / Bizerte / 3 / 3500 = 217 (total_mismatch)
  - sgt1928 p.228 1928 1927 / Tunis / Tunis / Tunis-Ville et sa banlieue / 3 / 3500 = 1997 (ocr_corrected)
  - sgt1928 p.228 1928 1927 / Tunis / Tunis / Tunis-Ville et sa banlieue / 4 / 7500 = 871 (ocr_corrected)
  - sgt1928 p.228 1928 1927 / Tunis / Zaghouan / Zaghouan / 3 / 3500 = 88 (ocr_corrected)
  - sgt1928 p.228 1928 1927 / Sfax / Djerba / Djerba / 2 / 1500 = 258 (ocr_corrected)
  - sgt1928 p.228 1928 1927 / Territoires militaires du Sud /  / Ouerghemma / 3 / 3500 = 67 (ocr_corrected)
  - sgt1929 p.231 1929 1928 / Le Kef / Le Kef / Le Kef / 34 / 2550000 = 6 (total_mismatch)
  - sgt1929 p.231 1929 1928 / Le Kef / Le Kef / Tadjerouine / 2 / 1500 = 58 (ocr_corrected)
  - sgt1929 p.231 1929 1928 / Sfax / Sfax / Sfax / 5 / 15000 = 82 (ocr_corrected)
  - sgt1929 p.231 1929 1928 / Territoires militaire du Sud /  / Ouerghemma / 50 / 4150000 = 7 (total_mismatch)
  - sgt1930 p.235 1930 1929 / Sousse / Sousse / Monastir / 34 / 2550000 = 5 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (16 printings): sgt1922 f222, sgt1922 f223, sgt1923 f712, sgt1923 f713, sgt1924 f1208, sgt1924 f1209, sgt1925 f278, sgt1925 f279, sgt1926 f794, sgt1926 f795, sgt1927 f256, sgt1927 f257, sgt1928 f780, sgt1928 f781, sgt1929 f259, sgt1930 f793.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 49.
