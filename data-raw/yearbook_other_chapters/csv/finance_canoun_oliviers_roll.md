# Canoun des oliviers. c) Répartition entre les européens et les indigènes

*Tax on olive trees (canoun des oliviers): trees taxed and not taxed on the European and indigenous rolls, articles and individual accounts.*

Source: *Statistique générale de la Tunisie*, chapter *Finances*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views: sgt1922 (`bpt6k9105649x`): p. 196, f220, p. 197, f221; sgt1923 (`bpt6k9105649x`): p. 208, f710, p. 209, f711; sgt1924 (`bpt6k9105649x`): p. 216, f1206, p. 217, f1207; sgt1925 (`bpt6k9105650k`): p. 252, f276, p. 253, f277; sgt1926 (`bpt6k9105650k`): p. 228, f792, p. 229, f793; sgt1927 (`bpt6k91056510`): p. 226, f254, p. 227, f255; sgt1928 (`bpt6k91056510`): p. 226, f778, p. 227, f779; sgt1929 (`bpt6k9105652d`): p. 228, f256, p. 229, f257; sgt1930 (`bpt6k9105652d`): p. 228, f790, p. 229, f791.

Transcriptions: `../transcribed/finance_canoun_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_finance_canoun.py build`.

Rows: 2336. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930.

Units: trees, articles and accounts, see `unit`; value_type: mixed (counts of three kinds).

Printed once per edition, each printing for its own year: every edition is kept (SPEC_ADDENDUM rule 5); `census` is the edition, `year` the year of the tree census (1er novembre <year>, printed in the title of a)).

## Columns

- `census`: edition (source code, see EDITIONS.md)
- `table_id`: transcription section (table a), b) or c))
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN) of the page the cell is printed on
- `year`: year of the census of the trees: the year of the "1er novembre <year>" printed in the title of a) (the edition year, except sgt1925 dattiers, titled 1924); b) and c) take the year of their a)
- `region`: région as printed, with its chef-lieu in brackets for the olive tables (from sgt1925: "1re Région (Bizerte)" ... "5me Région (Sfax)", "Territoires militaires du Sud"; date-palm tables: "5e Région", "Territoires militaires"); empty in sgt1922-sgt1924, which list caïdats only
- `controle_civil`: contrôle civil as printed (olive tables from sgt1925; empty otherwise)
- `caidat`: caïdat as printed in that table (spelling varies between editions and between a), b), c): Majeur / Madjeurs, Hammama / Hemmama, Ouled-Ayar / Oulad Ayar, Kef / Le Kef...); "Cap-Bon - Nabeul" and "Cap-Bon - Soliman" = the two lines printed under the brace of the caïdat Cap-Bon
- `measure`: `trees` (nombre d'arbres), `articles` (nombre d'articles de matrice: entries on the tax roll), `accounts` (nombre de comptes individuels: individual taxpayer accounts)
- `measure_fr`: printed column-group heading
- `unit`: unit of `value`
- `roll`: `european` (Européens) or `indigenous` (Indigènes)
- `roll_fr`: printed column heading
- `status`: `taxed` (imposés) or `not_taxed` (non imposés: young trees, mâles / sauvages); empty for articles and accounts
- `status_fr`: printed column heading
- `value`: printed count (» = 0)
- `flag`: empty, or `total_mismatch` (printed value kept; the line TOTAL and the column Totaux, or the other tables of the same edition, identify it as the faulty cell; see the notes), `row_realigned` (figures printed on the line of another caïdat, stored under the caïdat they belong to; see the notes), `derived_from_totals` (digits lost in the gutter fold; value = line TOTAL minus the other cells of the line)

Nombre d'arbres imposés and non imposés (jeunes et sauvages), each Européens, Indigènes, TOTAL; Nombre d'articles de matrice and Nombre de comptes individuels, each Européens, Indigènes, TOTAL. TOTAL columns and Totaux are checks; imposés TOTAL = a) 20 ans imposables, non imposés TOTAL = a) sauvages + Total des jeunes. Not printed in sgt1935.

Footnotes: none printed under these tables.

## Validation

- Checks against printed totals and identities: 1912; passed: 1840; failed: 72.

Every failure was re-read on zoomed native-resolution crops; printed values are kept. Explanation, by edition:

  - sgt1922: L'Arad comptes TOTAL 1.876 for 4.876 (the Totaux 192.497 requires 4.876); Mahdia non imposés TOTAL 713.758 against a) 712.748 (Européens + Indigènes = 713.758; the a) figures agree with each other); Cap-Bon - Nabeul imposés TOTAL 376.253 against a) and b) 376.369, Gafsa 135.029 against 135.030; the Totaux follow these lines.
  - sgt1923: Non imposés Totaux = a) sauvages Totaux misprint (822.887 for 722.887) plus Total des jeunes.
  - sgt1925: Souassi indigènes imposés 53.045 (58.045) and Sfax articles indigènes 22.803 (22.893), flagged; small unattributed differences in check figures (Zaghouan comptes TOTAL, Le Kef imposés TOTAL 29.906, Sousse comptes TOTAL, Gafsa articles TOTAL 11.482, Totaux non imposés and comptes indigènes); differences with a) follow the a) misprints (Cap-Bon - Nabeul, La Skhira, Djebéniana, Tataouine).
  - sgt1926: La Skhira comptes européens printed 333 (zoomed; the line TOTAL 2.899 and the column Totaux 5.096 require 343), flagged; Souassi articles TOTAL printed 6.889 for 6.689 (the Totaux 458.545 requires 6.689; check column).
  - sgt1928: Zaghouan non imposés printed 7.984 / 155.189 / 163.173: a) gives 14.225 and the column Totaux imply 14.153 (both cells flagged; no correction attempted). Nefzaoua indigènes imposés 9.600 (a), b) and the Totaux require 9.672), flagged; its non imposés carry the 72 trees. Check figures: Téboursouk articles TOTAL 1.231 (1.131), Kairouan 1.073 (1.373), Gafsa 11.756 (11.760; printed in the Hemmama cell), Béja comptes TOTAL partly printed; Totaux of articles and comptes off by small amounts (not attributable).
  - sgt1929: Flagged (zoomed; the line TOTAL, b) and the column Totaux all point to the cell): Bizerte Européens imposés 38.046 (38.446), Béja indigènes imposés 11.752 (11.852), Banlieue indigènes imposés 730.080 (730.089). Not attributable: Matmata imposés TOTAL 108.806 with Européens » and Indigènes 108.713, Ouerghema 194.604 with 9.891 + 184.806 (93 trees on the wrong line, the Totaux unaffected); Le Kef imposés TOTAL 29.993 (= a)) for 29.994; Bizerte non imposés TOTAL 36.946 = a) for 36.949; Mahdia follows the a) misprint.
  - sgt1927: Flagged (line TOTAL and column Totaux both point to the cell; each zoomed): Cap-Bon - Nabeul Européens imposés 10.580 (10.508), Sfax Européens imposés 226.238 (226.231), Oulad Aoun indigènes imposés 23.932 (23.939), Mahdia indigènes non imposés 128.407 (628.407), Ouerghema articles européens 19 (119). Check figures: Cap-Bon - Soliman imposés TOTAL 1.057.995 for 1.157.995 (a) and b)), Tataouine non imposés TOTAL 84.749 for 34.749, Totaux imposés TOTAL 9.909.456 = a) (the lines carry the Soliman misprint), non imposés TOTAL 5.859.552; Djerid follows the a) misprint.

Failed checks:

  - sgt1922 oliviers_roll Totaux co_t: sum of the lines (f221): cells give 189497, printed 192497 (difference 3000)
  - sgt1925 oliviers_roll Totaux imp_i: sum of the lines (f276): cells give 8375696, printed 8380696 (difference 5000)
  - sgt1925 oliviers_roll Totaux imp_t: sum of the lines (f276): cells give 9103807, printed 9103897 (difference 90)
  - sgt1925 oliviers_roll Totaux non_i: sum of the lines (f277): cells give 5208291, printed 5208293 (difference 2)
  - sgt1925 oliviers_roll Totaux ar_i: sum of the lines (f277): cells give 441408, printed 441498 (difference 90)
  - sgt1925 oliviers_roll Totaux ar_t: sum of the lines (f277): cells give 451653, printed 451753 (difference 100)
  - sgt1925 oliviers_roll Totaux co_i: sum of the lines (f277): cells give 210361, printed 210364 (difference 3)
  - sgt1926 oliviers_roll Totaux ar_t: sum of the lines (f793): cells give 458745, printed 458545 (difference -200)
  - sgt1926 oliviers_roll Totaux co_e: sum of the lines (f793): cells give 5086, printed 5096 (difference 10)
  - sgt1927 oliviers_roll Totaux imp_e: sum of the lines (f254): cells give 861996, printed 861917 (difference -79)
  - sgt1927 oliviers_roll Totaux imp_i: sum of the lines (f254): cells give 9047532, printed 9047539 (difference 7)
  - sgt1927 oliviers_roll Totaux imp_t: sum of the lines (f254): cells give 9809456, printed 9909456 (difference 100000)
  - sgt1927 oliviers_roll Totaux non_i: sum of the lines (f255): cells give 4396119, printed 4896119 (difference 500000)
  - sgt1927 oliviers_roll Totaux non_t: sum of the lines (f255): cells give 5909552, printed 5859552 (difference -50000)
  - sgt1927 oliviers_roll Totaux ar_e: sum of the lines (f255): cells give 10638, printed 10738 (difference 100)
  - sgt1928 oliviers_roll Totaux imp_i: sum of the lines (f778): cells give 8920335, printed 8920407 (difference 72)
  - sgt1928 oliviers_roll Totaux imp_t: sum of the lines (f778): cells give 9798128, printed 9798200 (difference 72)
  - sgt1928 oliviers_roll Totaux non_e: sum of the lines (f779): cells give 1144380, printed 1142916 (difference -1464)
  - sgt1928 oliviers_roll Totaux non_i: sum of the lines (f779): cells give 4979928, printed 4832372 (difference -147556)
  - sgt1928 oliviers_roll Totaux non_t: sum of the lines (f779): cells give 6124308, printed 5975288 (difference -149020)
  - sgt1928 oliviers_roll Totaux ar_i: sum of the lines (f779): cells give 454759, printed 454855 (difference 96)
  - sgt1928 oliviers_roll Totaux ar_t: sum of the lines (f779): cells give 465188, printed 465488 (difference 300)
  - sgt1928 oliviers_roll Totaux co_e: sum of the lines (f779): cells give 5287, printed 5289 (difference 2)
  - sgt1929 oliviers_roll Totaux imp_e: sum of the lines (f256): cells give 905477, printed 905876 (difference 399)
  - sgt1929 oliviers_roll Totaux imp_i: sum of the lines (f256): cells give 9197344, printed 9197453 (difference 109)
  - sgt1929 oliviers_roll Totaux non_t: sum of the lines (f257): cells give 5880840, printed 5880843 (difference 3)
  - sgt1922 oliviers_roll L'Arad: co TOTAL = Européens + Indigènes: cells give 4876, printed 1876 (difference -3000)
  - sgt1925 oliviers_roll 2me Région (Tunis) ; Zaghouan ; Zaghouan: co TOTAL = Européens + Indigènes: cells give 768, printed 778 (difference 10)
  - sgt1925 oliviers_roll 2me Région (Tunis) ; Grombalia ; Cap-Bon - Soliman: non TOTAL = Européens + Indigènes: cells give 110965, printed 110967 (difference 2)
  - sgt1925 oliviers_roll 3me Région (Le Kef) ; Le Kef ; Le Kef: imp TOTAL = Européens + Indigènes: cells give 29996, printed 29906 (difference -90)
  - sgt1925 oliviers_roll 4me Région (Sousse) ; Sousse ; Souassi: imp TOTAL = Européens + Indigènes: cells give 53193, printed 58193 (difference 5000)
  - sgt1925 oliviers_roll 4me Région (Sousse) ; Sousse ; Sousse: co TOTAL = Européens + Indigènes: cells give 33322, printed 33315 (difference -7)
  - sgt1925 oliviers_roll 5me Région (Sfax) ; Sfax ; Sfax: ar TOTAL = Européens + Indigènes: cells give 24646, printed 24736 (difference 90)
  - sgt1925 oliviers_roll 5me Région (Sfax) ; Gafsa ; Gafsa: ar TOTAL = Européens + Indigènes: cells give 11582, printed 11482 (difference -100)
  - sgt1926 oliviers_roll 4me Région (Sousse) ; Sousse ; Souassi: ar TOTAL = Européens + Indigènes: cells give 6689, printed 6889 (difference 200)
  - sgt1926 oliviers_roll 5me Région (Sfax) ; Sfax ; La Skhira: co TOTAL = Européens + Indigènes: cells give 2889, printed 2899 (difference 10)
  - sgt1927 oliviers_roll 2me Région (Tunis) ; Grombalia ; Cap-Bon - Nabeul: imp TOTAL = Européens + Indigènes: cells give 404014, printed 403942 (difference -72)
  - sgt1927 oliviers_roll 2me Région (Tunis) ; Grombalia ; Cap-Bon - Soliman: imp TOTAL = Européens + Indigènes: cells give 1157995, printed 1057995 (difference -100000)
  - sgt1927 oliviers_roll 3me Région (Le Kef) ; Mactar ; Oulad Aoun: imp TOTAL = Européens + Indigènes: cells give 24050, printed 24057 (difference 7)
  - sgt1927 oliviers_roll 4me Région (Sousse) ; Sousse ; Mahdia: non TOTAL = Européens + Indigènes: cells give 147135, printed 647135 (difference 500000)
  - sgt1927 oliviers_roll 5me Région (Sfax) ; Sfax ; Sfax: imp TOTAL = Européens + Indigènes: cells give 1349698, printed 1349691 (difference -7)
  - sgt1927 oliviers_roll Territoires militaires du Sud ;  ; Ouerghema: ar TOTAL = Européens + Indigènes: cells give 24561, printed 24661 (difference 100)
  - sgt1927 oliviers_roll Territoires militaires du Sud ;  ; Tataouine: non TOTAL = Européens + Indigènes: cells give 34749, printed 84749 (difference 50000)
  - sgt1928 oliviers_roll 3me Région (Le Kef) ; Téboursouk ; Téboursouk: ar TOTAL = Européens + Indigènes: cells give 1131, printed 1231 (difference 100)
  - sgt1928 oliviers_roll 4me Région (Sousse) ; Kairouan ; Kairouan: ar TOTAL = Européens + Indigènes: cells give 1373, printed 1073 (difference -300)
  - sgt1928 oliviers_roll 5me Région (Sfax) ; Gafsa ; Gafsa: ar TOTAL = Européens + Indigènes: cells give 11760, printed 11756 (difference -4)
  - sgt1929 oliviers_roll 1re Région (Bizerte) ; Béja ; Béja: imp TOTAL = Européens + Indigènes: cells give 12789, printed 12889 (difference 100)
  - sgt1929 oliviers_roll 1re Région (Bizerte) ; Bizerte ; Bizerte: imp TOTAL = Européens + Indigènes: cells give 429050, printed 429450 (difference 400)
  - sgt1929 oliviers_roll 1re Région (Bizerte) ; Bizerte ; Bizerte: non TOTAL = Européens + Indigènes: cells give 36949, printed 36946 (difference -3)
  - sgt1929 oliviers_roll 2me Région (Tunis) ; Tunis ; Banlieue: imp TOTAL = Européens + Indigènes: cells give 814306, printed 814315 (difference 9)
  - sgt1929 oliviers_roll 3me Région (Le Kef) ; Le Kef ; Le Kef: imp TOTAL = Européens + Indigènes: cells give 29994, printed 29993 (difference -1)
  - sgt1929 oliviers_roll Territoires militaires du Sud ;  ; Matmata: imp TOTAL = Européens + Indigènes: cells give 108713, printed 108806 (difference 93)
  - sgt1929 oliviers_roll Territoires militaires du Sud ;  ; Ouerghema: imp TOTAL = Européens + Indigènes: cells give 194697, printed 194604 (difference -93)
  - sgt1922 oliviers_roll Mahdia: non imposés TOTAL = a) sauvages + Total des jeunes: cells give 712748, printed 713758 (difference 1010)
  - sgt1922 oliviers_roll Cap-Bon - Nabeul: imposés TOTAL = a) 20 ans imposables: cells give 376369, printed 376253 (difference -116)
  - sgt1922 oliviers_roll Gafsa: imposés TOTAL = a) 20 ans imposables: cells give 135030, printed 135029 (difference -1)
  - sgt1922 oliviers_roll Totaux: imposés TOTAL = a) 20 ans imposables: cells give 9094191, printed 9094075 (difference -116)
  - sgt1922 oliviers_roll Totaux: non imposés TOTAL = a) sauvages + Total des jeunes: cells give 6015104, printed 6016114 (difference 1010)
  - sgt1923 oliviers_roll Totaux: non imposés TOTAL = a) sauvages + Total des jeunes: cells give 6316505, printed 6216535 (difference -99970)
  - sgt1925 oliviers_roll 2me Région (Tunis) ; Grombalia ; Cap-Bon - Nabeul: imposés TOTAL = a) 20 ans imposables: cells give 337466, printed 377466 (difference 40000)
  - sgt1925 oliviers_roll 3me Région (Le Kef) ; Le Kef ; Le Kef: imposés TOTAL = a) 20 ans imposables: cells give 29996, printed 29906 (difference -90)
  - sgt1925 oliviers_roll 5me Région (Sfax) ; Sfax ; La Skhira: non imposés TOTAL = a) sauvages + Total des jeunes: cells give 598013, printed 498013 (difference -100000)
  - sgt1925 oliviers_roll 5me Région (Sfax) ; Sfax ; Djebéniana: non imposés TOTAL = a) sauvages + Total des jeunes: cells give 652603, printed 661603 (difference 9000)
  - sgt1925 oliviers_roll Territoires militaires du Sud ;  ; Tataouine: non imposés TOTAL = a) sauvages + Total des jeunes: cells give 34748, printed 34749 (difference 1)
  - sgt1927 oliviers_roll 2me Région (Tunis) ; Grombalia ; Cap-Bon - Soliman: imposés TOTAL = a) 20 ans imposables: cells give 1157995, printed 1057995 (difference -100000)
  - sgt1927 oliviers_roll 5me Région (Sfax) ; Tozeur ; Djerid: imposés TOTAL = a) 20 ans imposables: cells give 21411, printed 21481 (difference 70)
  - sgt1927 oliviers_roll Territoires militaires du Sud ;  ; Tataouine: non imposés TOTAL = a) sauvages + Total des jeunes: cells give 34749, printed 84749 (difference 50000)
  - sgt1928 oliviers_roll 2me Région (Tunis) ; Zaghouan ; Zaghouan: non imposés TOTAL = a) sauvages + Total des jeunes: cells give 14225, printed 163173 (difference 148948)
  - sgt1928 oliviers_roll Territoires militaires du Sud ;  ; Nefzaoua: imposés TOTAL = a) 20 ans imposables: cells give 9672, printed 9600 (difference -72)
  - sgt1928 oliviers_roll Territoires militaires du Sud ;  ; Nefzaoua: non imposés TOTAL = a) sauvages + Total des jeunes: cells give 23810, printed 23882 (difference 72)
  - sgt1929 oliviers_roll 1re Région (Bizerte) ; Bizerte ; Bizerte: non imposés TOTAL = a) sauvages + Total des jeunes: cells give 36949, printed 36946 (difference -3)
  - sgt1929 oliviers_roll 4me Région (Sousse) ; Sousse ; Mahdia: non imposés TOTAL = a) sauvages + Total des jeunes: cells give 617237, printed 647237 (difference 30000)

- Flagged cells: row_realigned: 8, total_mismatch: 14.

  - sgt1923 p.208 Fraichiches / trees / european / taxed = 2 (row_realigned)
  - sgt1923 p.208 Fraichiches / trees / indigenous / taxed = 2758 (row_realigned)
  - sgt1923 p.208 Fraichiches / trees / european / not_taxed = 44 (row_realigned)
  - sgt1923 p.208 Fraichiches / trees / indigenous / not_taxed = 11937 (row_realigned)
  - sgt1923 p.208 Majeur / trees / european / taxed = 0 (row_realigned)
  - sgt1923 p.208 Majeur / trees / indigenous / taxed = 1938 (row_realigned)
  - sgt1923 p.208 Majeur / trees / european / not_taxed = 10005 (row_realigned)
  - sgt1923 p.208 Majeur / trees / indigenous / not_taxed = 5661 (row_realigned)
  - sgt1925 p.252 Souassi / trees / indigenous / taxed = 53045 (total_mismatch)
  - sgt1925 p.253 Sfax / articles / indigenous /  = 22803 (total_mismatch)
  - sgt1926 p.229 La Skhira / accounts / european /  = 333 (total_mismatch)
  - sgt1927 p.226 Cap-Bon - Nabeul / trees / european / taxed = 10580 (total_mismatch)
  - sgt1927 p.226 Oulad Aoun / trees / indigenous / taxed = 23932 (total_mismatch)
  - sgt1927 p.227 Mahdia / trees / indigenous / not_taxed = 128407 (total_mismatch)
  - sgt1927 p.226 Sfax / trees / european / taxed = 226238 (total_mismatch)
  - sgt1927 p.227 Ouerghema / articles / european /  = 19 (total_mismatch)
  - sgt1928 p.227 Zaghouan / trees / european / not_taxed = 7984 (total_mismatch)
  - sgt1928 p.227 Zaghouan / trees / indigenous / not_taxed = 155189 (total_mismatch)
  - sgt1928 p.226 Nefzaoua / trees / indigenous / taxed = 9600 (total_mismatch)
  - sgt1929 p.228 Béja / trees / indigenous / taxed = 11752 (total_mismatch)
  - sgt1929 p.228 Bizerte / trees / european / taxed = 38046 (total_mismatch)
  - sgt1929 p.228 Banlieue / trees / indigenous / taxed = 730080 (total_mismatch)

## Image versus OCR

- Read cell by cell on native-resolution crops of the page images (strips of rows, gutter columns on both views of the spread, every failing check re-read zoomed): sgt1922 f220, sgt1922 f221, sgt1923 f710, sgt1923 f711, sgt1924 f1206, sgt1924 f1207, sgt1925 f276, sgt1925 f277, sgt1926 f792, sgt1926 f793, sgt1927 f254, sgt1927 f255, sgt1928 f778, sgt1928 f779, sgt1929 f256, sgt1929 f257, sgt1930 f790, sgt1930 f791.
- The Gallica OCR was not used (no cell is flagged `ocr_corrected`).

Survey of the canoun tables in every edition: `finance_canoun_survey.md`.
