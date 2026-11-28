# Postes, Télégraphes, Téléphones. Renseignements généraux : b) Exploitation

*Posts, telegraphs and telephones: traffic (correspondence, money orders, registered items, collections, parcels, telegrams, telephone conversations, savings bank).*

Source: *Statistique générale de la Tunisie*, chapter *Postes - Télégraphes - Téléphones*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 130, f154, p. 132, f156; sgt1923 (`bpt6k9105649x`): p. 136, f638, p. 138, f640; sgt1924 (`bpt6k9105649x`): p. 138, f1128, p. 140, f1130; sgt1925 (`bpt6k9105650k`): p. 140, f164, p. 142, f166; sgt1926 (`bpt6k9105650k`): p. 150, f714, p. 152, f716; sgt1927 (`bpt6k91056510`): p. 148, f176, p. 150, f178; sgt1928 (`bpt6k91056510`): p. 148, f700, p. 150, f702; sgt1929 (`bpt6k9105652d`): p. 150, f178, p. 152, f180; sgt1930 (`bpt6k9105652d`): p. 154, f712, p. 155, f713, p. 156, f714, p. 157, f715; sgt1935 (`bpt6k9105653t`): p. 90, f110, p. 91, f111, p. 92, f112, p. 93, f113; sgt1936 (`bpt6k91056547`): p. 68, f79, p. 69, f80, p. 70, f81, p. 71, f82; sgt1939 (`bpt6k9105739w`): p. 72, f78, p. 73, f79, p. 74, f80, p. 75, f81.

Transcriptions: `../transcribed/posts_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_posts.py build`.

Rows: 1290. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Units: counts (`unit` = `count`) and francs (`francs`, centimes kept), per line; suggested value_type: mixed.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing of the same cell, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`): the latest edition printing that year
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (network: situation at 31 December)
- `service`: `posts`, `telegraphs`, `telephones`, `savings` (Caisse d'Épargne)
- `service_fr`: printed sub-heading
- `item`: item code (English)
- `item_fr`: printed line heading
- `origin`: `tunisia`, `france`, `foreign` (printed Tunisie, France, Étranger); empty when the line has no breakdown
- `origin_fr`: as printed
- `measure`: `number` (Nombre) or `amount` (Montant)
- `measure_fr`: as printed
- `unit`: `count`, `km` (kilometres) or `francs` (centimes kept as decimals)
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible` (NA, cut by the binding or broken type), `not_applicable` (nothing printed, or » in a line not yet collected; NA), `row_realigned` (printed in the wrong column or line, stored on the year / item it belongs to), `reprint_corrected` (kept from an earlier printing), `derived_from_totals`

Financial years: the columns 1930 and 1932 of the Exploitation and Situation financière tables are printed "Année 1930 (15 mois)" and "Année 1932 (9 mois)" (sgt1930 heads its last column "Année 1930 (15 mois)"); stored as years 1930 and 1932.

Lines: correspondence (départ et arrivée; from sgt1935 "Tunisie (départ seulement)"), money orders issued and paid, registered items (chargements et objets recommandés, départ), collections (recouvrements, arrivée), bills presented for acceptance, parcels, telegrams, telephone conversations, savings bank (passbooks opened, deposits, withdrawals, depositors' balance). The printed Totaux lines are used as checks only.

sgt1939 prints a new Exploitation table (1930-1939) without correspondence, registered items, collections or acceptances, and adds urban / suburban and radiotelephone conversations, subscribers, wireless sets, passbooks outstanding, advances on pensions and postal cheques (1938-1939 only; earlier columns printed », stored NA `not_applicable`). In sgt1939 1938 the money orders France and Étranger are printed as one figure across the two lines (`origin` = `ff`) and the telegrams of each direction as one figure across the three origins (`origin` = `all`).

sgt1939 money-order lines are misaligned: the column headed 1931 prints the 1927 figures and the columns headed 1932-1936 the figures of 1931-1935 (identical, cell for cell, to sgt1936's 1927 and 1931-1935); they are attached to the year they belong to, flagged `row_realigned`, and compared with the other printings; the aligned printing (sgt1936) is kept for those years. Likewise sgt1939 prints the total number of telephone conversations of 1930-1937 on its "Suburbaines" line: stored as the total (`row_realigned`).

Cells illegible because of the binding (sgt1922 1915 savings-bank lines; sgt1939 1932 column) or a broken plate (sgt1926 1926 telephone conversations, printed "7.089 11") are stored only from another printing; sgt1922's 1915 savings lines are stored from sgt1923.

Two notable revisions between editions: sgt1929 revises 1920 savings deposits (38.352 to 38.362) and balances 1920 and 1923; sgt1935 prints the 1926 telephone conversations as 7.089.111 (sgt1927-sgt1930: 7.089.114) and 1933 parcels dispatched to Tunisia / France 67.847 / 95.193 (sgt1936, sgt1939: 67.947 / 95.183).

Failed checks, grouped (printed values kept). A failure that recurs identically in several editions was read independently on each printing, so it is the printed figure; every failure printed by one edition only was re-read on a zoomed native-resolution crop: operations 1914 Total@corr: cells 86987825, printed 86987830 (in sgt1922); operations 1914 Total@mo_amt: cells 99676570, printed 99676571 (in sgt1922, sgt1923); operations 1916 Total@mo_amt: cells 119030775, printed 119130775 (in sgt1922, sgt1923, sgt1924, sgt1925); operations 1916 Total@parcels: cells 553990, printed 553670 (in sgt1922, sgt1923, sgt1924, sgt1925); operations 1918 Total@mo_amt: cells 161682540, printed 161682541 (in sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927); operations 1918 Total@mo_n: cells 1252609, printed 1312618 (in sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927); operations 1918 Total@parcels: cells 636743, printed 637743 (in sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927); operations 1918 Total@tg: cells 1788979, printed 1698777 (in sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927); operations 1919 Total@coll_amt: cells 8101523, printed 18301523 (in sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928); operations 1919 Total@coll_n: cells 160812, printed 180812 (in sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928); operations 1919 Total@mo_amt: cells 193223463, printed 193223457 (in sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928); operations 1919 Total@parcels: cells 631123, printed 687123 (in sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928); operations 1919 Total@tg: cells 1829680, printed 1830130 (in sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928); operations 1920 Total@coll_n: cells 216241, printed 216245 (in sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929); operations 1920 Total@mo_amt: cells 314851329, printed 314851330 (in sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929); operations 1920 Total@parcels: cells 632381, printed 632384 (in sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929); operations 1921 Total@mo_amt: cells 314589723, printed 318589723 (in sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930); operations 1921 Total@parcels: cells 737797, printed 737747 (in sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930); operations 1922 Total@mo_amt: cells 280797065, printed 280797060 (in sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930); operations 1923 Total@cne_n: cells 65622, printed 70394 (in sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930); operations 1923 Total@parcels: cells 861462, printed 891462 (in sgt1923); operations 1923 Total@tg: cells 1425990, printed 1426020 (in sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930); operations 1924 Total@cne_n: cells 70225, printed 74678 (in sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930); operations 1924 Total@mo_amt: cells 401427075, printed 401427074 (in sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930); operations 1925 Total@coll_amt: cells 91410305, printed 91420305 (in sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930); operations 1925 Total@tg: cells 1429080, printed 1437154 (in sgt1925); operations 1926 Total@coll_amt: cells 117304515, printed 117304535 (in sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935); operations 1926 Total@tg: cells 1368770, printed 1368767 (in sgt1926); operations 1927 Total@coll_n: cells 484966, printed 484956 (in sgt1936); operations 1928 Total@mo_amt: cells 672871104, printed 672871101 (in sgt1928, sgt1929, sgt1930, sgt1935); operations 1928 Total@mo_amt: cells 672844104, printed 672871101 (in sgt1936); operations 1929 Total@corr: cells 120791796, printed 120791696 (in sgt1936); operations 1932 Total@corr: cells 89601000, printed 89601500 (in sgt1936); operations 1933 Total@parcels: cells 1240519, printed 1241019 (in sgt1935); operations 1933 Total@parcels: cells 1240609, printed 1241019 (in sgt1936, sgt1939); operations 1934 Total@mo_amt: cells 505379525, printed 505379527 (in sgt1935, sgt1936); operations 1934 Total@parcels: cells 1042717, printed 1032717 (in sgt1935, sgt1936, sgt1939); operations 1935 Total@cne_n: cells 122303, printed 130735 (in sgt1935, sgt1936, sgt1939); operations 1935 Total@coll_amt: cells 94331974.00, printed 90331974 (in sgt1935, sgt1936); operations 1935 Total@mo_amt: cells 400182150, printed 507654550 (in sgt1935, sgt1936); operations 1935 Total@parcels: cells 838183, printed 842183 (in sgt1935, sgt1936, sgt1939); operations 1938 Total@cne_amt: cells 192146575.58, printed 192146575.08 (in sgt1939).

Printings not compared because the cell is illegible in that printing (cut by the binding): 41.

Flagged cells: (1928, 'money_orders_paid', 'foreign', 'amount'): kept sgt1935's 3685894 (reprint_corrected); sgt1936 prints 3.658.894 (transposed digits); sgt1928-sgt1935 print 3.685.894, which gives the Totaux 672.871.101 to within 3 francs (as in every other printing); (1932, 'correspondence', 'france', 'number'): kept sgt1935's 50350500 (reprint_corrected); sgt1936 prints 50.350.000; sgt1935's 50.350.500 is the value that gives the Totaux 89.601.500 printed by both; (1935, 'money_orders_issued', 'france', 'amount'): 107579990 (derived_from_totals, stored with census = sgt1936); printed "107.590" in sgt1935, sgt1936 and sgt1939 (digits missing); 107.579.990 = Totaux 507.654.550 less the five other amounts printed for 1935; (1935, 'withdrawals', '', 'amount'): kept sgt1935's 61920421.16 (reprint_corrected); sgt1936 and sgt1939 print 6.920.421 16 (a digit dropped); sgt1935 prints 61.920.421 16, the order of magnitude of the other years and of the Comptes ouverts table.

Survey of the whole chapter in every edition: `posts_survey.md`.

## Validation

- Checks against printed totals and identities: 1225; passed: 1032; failed: 193.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.130 (f154) operations 1914: Total@corr = corr_tunisia + corr_france + corr_foreign: cells give 86987825, printed 86987830 (difference 5)
  - sgt1922 p.130 (f154) operations 1914: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 99676570, printed 99676571 (difference 1)
  - sgt1922 p.131 (f155) operations 1918: Total@mo_n = mo_issued_tunisia_n + mo_issued_france_n + mo_issued_foreign_n + mo_paid_tunisia_n + mo_paid_france_n + mo_paid_foreign_n: cells give 1252609, printed 1312618 (difference 60009)
  - sgt1922 p.131 (f155) operations 1916: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 119030775, printed 119130775 (difference 100000)
  - sgt1922 p.131 (f155) operations 1918: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 161682540, printed 161682541 (difference 1)
  - sgt1922 p.131 (f155) operations 1919: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 193223463, printed 193223457 (difference -6)
  - sgt1922 p.131 (f155) operations 1920: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 314851329, printed 314851330 (difference 1)
  - sgt1922 p.131 (f155) operations 1921: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 314589723, printed 318589723 (difference 4000000)
  - sgt1922 p.131 (f155) operations 1922: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 280797065, printed 280797060 (difference -5)
  - sgt1922 p.133 (f157) operations 1919: Total@coll_n = coll_tunisia_n + coll_france_n + coll_foreign_n: cells give 160812, printed 180812 (difference 20000)
  - sgt1922 p.133 (f157) operations 1920: Total@coll_n = coll_tunisia_n + coll_france_n + coll_foreign_n: cells give 216241, printed 216245 (difference 4)
  - sgt1922 p.133 (f157) operations 1919: Total@coll_amt = coll_tunisia_amt + coll_france_amt + coll_foreign_amt: cells give 8101523, printed 18301523 (difference 10200000)
  - sgt1922 p.133 (f157) operations 1916: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 553990, printed 553670 (difference -320)
  - sgt1922 p.133 (f157) operations 1918: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 636743, printed 637743 (difference 1000)
  - sgt1922 p.133 (f157) operations 1919: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 631123, printed 687123 (difference 56000)
  - sgt1922 p.133 (f157) operations 1920: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 632381, printed 632384 (difference 3)
  - sgt1922 p.133 (f157) operations 1921: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 737797, printed 737747 (difference -50)
  - sgt1922 p.133 (f157) operations 1918: Total@tg = tg_dep_tunisia + tg_dep_france + tg_dep_foreign + tg_arr_tunisia + tg_arr_france + tg_arr_foreign + tg_official_dep + tg_official_arr: cells give 1788979, printed 1698777 (difference -90202)
  - sgt1922 p.133 (f157) operations 1919: Total@tg = tg_dep_tunisia + tg_dep_france + tg_dep_foreign + tg_arr_tunisia + tg_arr_france + tg_arr_foreign + tg_official_dep + tg_official_arr: cells give 1829680, printed 1830130 (difference 450)
  - sgt1923 p.136 (f638) operations 1914: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 99676570, printed 99676571 (difference 1)
  - sgt1923 p.136 (f638) operations 1916: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 119030775, printed 119130775 (difference 100000)
  - sgt1923 p.137 (f639) operations 1918: Total@mo_n = mo_issued_tunisia_n + mo_issued_france_n + mo_issued_foreign_n + mo_paid_tunisia_n + mo_paid_france_n + mo_paid_foreign_n: cells give 1252609, printed 1312618 (difference 60009)
  - sgt1923 p.137 (f639) operations 1918: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 161682540, printed 161682541 (difference 1)
  - sgt1923 p.137 (f639) operations 1919: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 193223463, printed 193223457 (difference -6)
  - sgt1923 p.137 (f639) operations 1920: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 314851329, printed 314851330 (difference 1)
  - sgt1923 p.137 (f639) operations 1921: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 314589723, printed 318589723 (difference 4000000)
  - sgt1923 p.137 (f639) operations 1922: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 280797065, printed 280797060 (difference -5)
  - sgt1923 p.138 (f640) operations 1916: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 553990, printed 553670 (difference -320)
  - sgt1923 p.139 (f641) operations 1919: Total@coll_n = coll_tunisia_n + coll_france_n + coll_foreign_n: cells give 160812, printed 180812 (difference 20000)
  - sgt1923 p.139 (f641) operations 1920: Total@coll_n = coll_tunisia_n + coll_france_n + coll_foreign_n: cells give 216241, printed 216245 (difference 4)
  - sgt1923 p.139 (f641) operations 1919: Total@coll_amt = coll_tunisia_amt + coll_france_amt + coll_foreign_amt: cells give 8101523, printed 18301523 (difference 10200000)
  - sgt1923 p.139 (f641) operations 1918: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 636743, printed 637743 (difference 1000)
  - sgt1923 p.139 (f641) operations 1919: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 631123, printed 687123 (difference 56000)
  - sgt1923 p.139 (f641) operations 1920: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 632381, printed 632384 (difference 3)
  - sgt1923 p.139 (f641) operations 1921: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 737797, printed 737747 (difference -50)
  - sgt1923 p.139 (f641) operations 1923: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 861462, printed 891462 (difference 30000)
  - sgt1923 p.139 (f641) operations 1918: Total@tg = tg_dep_tunisia + tg_dep_france + tg_dep_foreign + tg_arr_tunisia + tg_arr_france + tg_arr_foreign + tg_official_dep + tg_official_arr: cells give 1788979, printed 1698777 (difference -90202)
  - sgt1923 p.139 (f641) operations 1919: Total@tg = tg_dep_tunisia + tg_dep_france + tg_dep_foreign + tg_arr_tunisia + tg_arr_france + tg_arr_foreign + tg_official_dep + tg_official_arr: cells give 1829680, printed 1830130 (difference 450)
  - sgt1923 p.139 (f641) operations 1923: Total@tg = tg_dep_tunisia + tg_dep_france + tg_dep_foreign + tg_arr_tunisia + tg_arr_france + tg_arr_foreign + tg_official_dep + tg_official_arr: cells give 1425990, printed 1426020 (difference 30)
  - sgt1923 p.139 (f641) operations 1923: Total@cne_n = cne_deposits_n + cne_withdrawals_n: cells give 65622, printed 70394 (difference 4772)
  - sgt1924 p.138 (f1128) operations 1916: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 119030775, printed 119130775 (difference 100000)
  - sgt1924 p.139 (f1129) operations 1918: Total@mo_n = mo_issued_tunisia_n + mo_issued_france_n + mo_issued_foreign_n + mo_paid_tunisia_n + mo_paid_france_n + mo_paid_foreign_n: cells give 1252609, printed 1312618 (difference 60009)
  - sgt1924 p.139 (f1129) operations 1918: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 161682540, printed 161682541 (difference 1)
  - sgt1924 p.139 (f1129) operations 1919: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 193223463, printed 193223457 (difference -6)
  - sgt1924 p.139 (f1129) operations 1920: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 314851329, printed 314851330 (difference 1)
  - sgt1924 p.139 (f1129) operations 1921: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 314589723, printed 318589723 (difference 4000000)
  - sgt1924 p.139 (f1129) operations 1922: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 280797065, printed 280797060 (difference -5)
  - sgt1924 p.139 (f1129) operations 1924: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 401427075, printed 401427074 (difference -1)
  - sgt1924 p.140 (f1130) operations 1916: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 553990, printed 553670 (difference -320)
  - sgt1924 p.141 (f1131) operations 1919: Total@coll_n = coll_tunisia_n + coll_france_n + coll_foreign_n: cells give 160812, printed 180812 (difference 20000)
  - sgt1924 p.141 (f1131) operations 1920: Total@coll_n = coll_tunisia_n + coll_france_n + coll_foreign_n: cells give 216241, printed 216245 (difference 4)
  - sgt1924 p.141 (f1131) operations 1919: Total@coll_amt = coll_tunisia_amt + coll_france_amt + coll_foreign_amt: cells give 8101523, printed 18301523 (difference 10200000)
  - sgt1924 p.141 (f1131) operations 1918: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 636743, printed 637743 (difference 1000)
  - sgt1924 p.141 (f1131) operations 1919: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 631123, printed 687123 (difference 56000)
  - sgt1924 p.141 (f1131) operations 1920: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 632381, printed 632384 (difference 3)
  - sgt1924 p.141 (f1131) operations 1921: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 737797, printed 737747 (difference -50)
  - sgt1924 p.141 (f1131) operations 1918: Total@tg = tg_dep_tunisia + tg_dep_france + tg_dep_foreign + tg_arr_tunisia + tg_arr_france + tg_arr_foreign + tg_official_dep + tg_official_arr: cells give 1788979, printed 1698777 (difference -90202)
  - sgt1924 p.141 (f1131) operations 1919: Total@tg = tg_dep_tunisia + tg_dep_france + tg_dep_foreign + tg_arr_tunisia + tg_arr_france + tg_arr_foreign + tg_official_dep + tg_official_arr: cells give 1829680, printed 1830130 (difference 450)
  - sgt1924 p.141 (f1131) operations 1923: Total@tg = tg_dep_tunisia + tg_dep_france + tg_dep_foreign + tg_arr_tunisia + tg_arr_france + tg_arr_foreign + tg_official_dep + tg_official_arr: cells give 1425990, printed 1426020 (difference 30)
  - sgt1924 p.141 (f1131) operations 1923: Total@cne_n = cne_deposits_n + cne_withdrawals_n: cells give 65622, printed 70394 (difference 4772)
  - sgt1924 p.141 (f1131) operations 1924: Total@cne_n = cne_deposits_n + cne_withdrawals_n: cells give 70225, printed 74678 (difference 4453)
  - sgt1925 p.140 (f164) operations 1918: Total@mo_n = mo_issued_tunisia_n + mo_issued_france_n + mo_issued_foreign_n + mo_paid_tunisia_n + mo_paid_france_n + mo_paid_foreign_n: cells give 1252609, printed 1312618 (difference 60009)
  - sgt1925 p.140 (f164) operations 1916: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 119030775, printed 119130775 (difference 100000)
  - sgt1925 p.140 (f164) operations 1918: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 161682540, printed 161682541 (difference 1)
  - sgt1925 p.141 (f165) operations 1919: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 193223463, printed 193223457 (difference -6)
  - sgt1925 p.141 (f165) operations 1920: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 314851329, printed 314851330 (difference 1)
  - sgt1925 p.141 (f165) operations 1921: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 314589723, printed 318589723 (difference 4000000)
  - sgt1925 p.141 (f165) operations 1922: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 280797065, printed 280797060 (difference -5)
  - sgt1925 p.141 (f165) operations 1924: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 401427075, printed 401427074 (difference -1)
  - sgt1925 p.142 (f166) operations 1916: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 553990, printed 553670 (difference -320)
  - sgt1925 p.142 (f166) operations 1918: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 636743, printed 637743 (difference 1000)
  - sgt1925 p.142 (f166) operations 1918: Total@tg = tg_dep_tunisia + tg_dep_france + tg_dep_foreign + tg_arr_tunisia + tg_arr_france + tg_arr_foreign + tg_official_dep + tg_official_arr: cells give 1788979, printed 1698777 (difference -90202)
  - sgt1925 p.143 (f167) operations 1919: Total@coll_n = coll_tunisia_n + coll_france_n + coll_foreign_n: cells give 160812, printed 180812 (difference 20000)
  - sgt1925 p.143 (f167) operations 1920: Total@coll_n = coll_tunisia_n + coll_france_n + coll_foreign_n: cells give 216241, printed 216245 (difference 4)
  - sgt1925 p.143 (f167) operations 1919: Total@coll_amt = coll_tunisia_amt + coll_france_amt + coll_foreign_amt: cells give 8101523, printed 18301523 (difference 10200000)
  - sgt1925 p.143 (f167) operations 1925: Total@coll_amt = coll_tunisia_amt + coll_france_amt + coll_foreign_amt: cells give 91410305, printed 91420305 (difference 10000)
  - sgt1925 p.143 (f167) operations 1919: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 631123, printed 687123 (difference 56000)
  - sgt1925 p.143 (f167) operations 1920: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 632381, printed 632384 (difference 3)
  - sgt1925 p.143 (f167) operations 1921: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 737797, printed 737747 (difference -50)
  - sgt1925 p.143 (f167) operations 1919: Total@tg = tg_dep_tunisia + tg_dep_france + tg_dep_foreign + tg_arr_tunisia + tg_arr_france + tg_arr_foreign + tg_official_dep + tg_official_arr: cells give 1829680, printed 1830130 (difference 450)
  - sgt1925 p.143 (f167) operations 1923: Total@tg = tg_dep_tunisia + tg_dep_france + tg_dep_foreign + tg_arr_tunisia + tg_arr_france + tg_arr_foreign + tg_official_dep + tg_official_arr: cells give 1425990, printed 1426020 (difference 30)
  - sgt1925 p.143 (f167) operations 1925: Total@tg = tg_dep_tunisia + tg_dep_france + tg_dep_foreign + tg_arr_tunisia + tg_arr_france + tg_arr_foreign + tg_official_dep + tg_official_arr: cells give 1429080, printed 1437154 (difference 8074)
  - sgt1925 p.143 (f167) operations 1923: Total@cne_n = cne_deposits_n + cne_withdrawals_n: cells give 65622, printed 70394 (difference 4772)
  - sgt1925 p.143 (f167) operations 1924: Total@cne_n = cne_deposits_n + cne_withdrawals_n: cells give 70225, printed 74678 (difference 4453)
  - sgt1926 p.150 (f714) operations 1918: Total@mo_n = mo_issued_tunisia_n + mo_issued_france_n + mo_issued_foreign_n + mo_paid_tunisia_n + mo_paid_france_n + mo_paid_foreign_n: cells give 1252609, printed 1312618 (difference 60009)
  - sgt1926 p.150 (f714) operations 1918: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 161682540, printed 161682541 (difference 1)
  - sgt1926 p.150 (f714) operations 1919: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 193223463, printed 193223457 (difference -6)
  - sgt1926 p.151 (f715) operations 1920: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 314851329, printed 314851330 (difference 1)
  - sgt1926 p.151 (f715) operations 1921: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 314589723, printed 318589723 (difference 4000000)
  - sgt1926 p.151 (f715) operations 1922: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 280797065, printed 280797060 (difference -5)
  - sgt1926 p.151 (f715) operations 1924: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 401427075, printed 401427074 (difference -1)
  - sgt1926 p.152 (f716) operations 1919: Total@coll_n = coll_tunisia_n + coll_france_n + coll_foreign_n: cells give 160812, printed 180812 (difference 20000)
  - sgt1926 p.152 (f716) operations 1919: Total@coll_amt = coll_tunisia_amt + coll_france_amt + coll_foreign_amt: cells give 8101523, printed 18301523 (difference 10200000)
  - sgt1926 p.152 (f716) operations 1918: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 636743, printed 637743 (difference 1000)
  - sgt1926 p.152 (f716) operations 1919: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 631123, printed 687123 (difference 56000)
  - sgt1926 p.152 (f716) operations 1918: Total@tg = tg_dep_tunisia + tg_dep_france + tg_dep_foreign + tg_arr_tunisia + tg_arr_france + tg_arr_foreign + tg_official_dep + tg_official_arr: cells give 1788979, printed 1698777 (difference -90202)
  - sgt1926 p.152 (f716) operations 1919: Total@tg = tg_dep_tunisia + tg_dep_france + tg_dep_foreign + tg_arr_tunisia + tg_arr_france + tg_arr_foreign + tg_official_dep + tg_official_arr: cells give 1829680, printed 1830130 (difference 450)
  - sgt1926 p.153 (f717) operations 1920: Total@coll_n = coll_tunisia_n + coll_france_n + coll_foreign_n: cells give 216241, printed 216245 (difference 4)
  - sgt1926 p.153 (f717) operations 1925: Total@coll_amt = coll_tunisia_amt + coll_france_amt + coll_foreign_amt: cells give 91410305, printed 91420305 (difference 10000)
  - sgt1926 p.153 (f717) operations 1926: Total@coll_amt = coll_tunisia_amt + coll_france_amt + coll_foreign_amt: cells give 117304515, printed 117304535 (difference 20)
  - sgt1926 p.153 (f717) operations 1920: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 632381, printed 632384 (difference 3)
  - sgt1926 p.153 (f717) operations 1921: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 737797, printed 737747 (difference -50)
  - sgt1926 p.153 (f717) operations 1923: Total@tg = tg_dep_tunisia + tg_dep_france + tg_dep_foreign + tg_arr_tunisia + tg_arr_france + tg_arr_foreign + tg_official_dep + tg_official_arr: cells give 1425990, printed 1426020 (difference 30)
  - sgt1926 p.153 (f717) operations 1926: Total@tg = tg_dep_tunisia + tg_dep_france + tg_dep_foreign + tg_arr_tunisia + tg_arr_france + tg_arr_foreign + tg_official_dep + tg_official_arr: cells give 1368770, printed 1368767 (difference -3)
  - sgt1926 p.153 (f717) operations 1923: Total@cne_n = cne_deposits_n + cne_withdrawals_n: cells give 65622, printed 70394 (difference 4772)
  - sgt1926 p.153 (f717) operations 1924: Total@cne_n = cne_deposits_n + cne_withdrawals_n: cells give 70225, printed 74678 (difference 4453)
  - sgt1927 p.148 (f176) operations 1918: Total@mo_n = mo_issued_tunisia_n + mo_issued_france_n + mo_issued_foreign_n + mo_paid_tunisia_n + mo_paid_france_n + mo_paid_foreign_n: cells give 1252609, printed 1312618 (difference 60009)
  - sgt1927 p.148 (f176) operations 1918: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 161682540, printed 161682541 (difference 1)
  - sgt1927 p.148 (f176) operations 1919: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 193223463, printed 193223457 (difference -6)
  - sgt1927 p.148 (f176) operations 1920: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 314851329, printed 314851330 (difference 1)
  - sgt1927 p.149 (f177) operations 1921: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 314589723, printed 318589723 (difference 4000000)
  - sgt1927 p.149 (f177) operations 1922: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 280797065, printed 280797060 (difference -5)
  - sgt1927 p.149 (f177) operations 1924: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 401427075, printed 401427074 (difference -1)
  - sgt1927 p.150 (f178) operations 1919: Total@coll_n = coll_tunisia_n + coll_france_n + coll_foreign_n: cells give 160812, printed 180812 (difference 20000)
  - sgt1927 p.150 (f178) operations 1920: Total@coll_n = coll_tunisia_n + coll_france_n + coll_foreign_n: cells give 216241, printed 216245 (difference 4)
  - sgt1927 p.150 (f178) operations 1919: Total@coll_amt = coll_tunisia_amt + coll_france_amt + coll_foreign_amt: cells give 8101523, printed 18301523 (difference 10200000)
  - sgt1927 p.150 (f178) operations 1918: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 636743, printed 637743 (difference 1000)
  - sgt1927 p.150 (f178) operations 1919: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 631123, printed 687123 (difference 56000)
  - sgt1927 p.150 (f178) operations 1920: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 632381, printed 632384 (difference 3)
  - sgt1927 p.150 (f178) operations 1918: Total@tg = tg_dep_tunisia + tg_dep_france + tg_dep_foreign + tg_arr_tunisia + tg_arr_france + tg_arr_foreign + tg_official_dep + tg_official_arr: cells give 1788979, printed 1698777 (difference -90202)
  - sgt1927 p.150 (f178) operations 1919: Total@tg = tg_dep_tunisia + tg_dep_france + tg_dep_foreign + tg_arr_tunisia + tg_arr_france + tg_arr_foreign + tg_official_dep + tg_official_arr: cells give 1829680, printed 1830130 (difference 450)
  - sgt1927 p.151 (f179) operations 1925: Total@coll_amt = coll_tunisia_amt + coll_france_amt + coll_foreign_amt: cells give 91410305, printed 91420305 (difference 10000)
  - sgt1927 p.151 (f179) operations 1926: Total@coll_amt = coll_tunisia_amt + coll_france_amt + coll_foreign_amt: cells give 117304515, printed 117304535 (difference 20)
  - sgt1927 p.151 (f179) operations 1921: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 737797, printed 737747 (difference -50)
  - sgt1927 p.151 (f179) operations 1923: Total@tg = tg_dep_tunisia + tg_dep_france + tg_dep_foreign + tg_arr_tunisia + tg_arr_france + tg_arr_foreign + tg_official_dep + tg_official_arr: cells give 1425990, printed 1426020 (difference 30)
  - sgt1927 p.151 (f179) operations 1923: Total@cne_n = cne_deposits_n + cne_withdrawals_n: cells give 65622, printed 70394 (difference 4772)
  - sgt1927 p.151 (f179) operations 1924: Total@cne_n = cne_deposits_n + cne_withdrawals_n: cells give 70225, printed 74678 (difference 4453)
  - sgt1928 p.148 (f700) operations 1919: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 193223463, printed 193223457 (difference -6)
  - sgt1928 p.148 (f700) operations 1920: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 314851329, printed 314851330 (difference 1)
  - sgt1928 p.148 (f700) operations 1921: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 314589723, printed 318589723 (difference 4000000)
  - sgt1928 p.149 (f701) operations 1922: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 280797065, printed 280797060 (difference -5)
  - sgt1928 p.149 (f701) operations 1924: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 401427075, printed 401427074 (difference -1)
  - sgt1928 p.149 (f701) operations 1928: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 672871104, printed 672871101 (difference -3)
  - sgt1928 p.150 (f702) operations 1919: Total@coll_n = coll_tunisia_n + coll_france_n + coll_foreign_n: cells give 160812, printed 180812 (difference 20000)
  - sgt1928 p.150 (f702) operations 1920: Total@coll_n = coll_tunisia_n + coll_france_n + coll_foreign_n: cells give 216241, printed 216245 (difference 4)
  - sgt1928 p.150 (f702) operations 1919: Total@coll_amt = coll_tunisia_amt + coll_france_amt + coll_foreign_amt: cells give 8101523, printed 18301523 (difference 10200000)
  - sgt1928 p.150 (f702) operations 1919: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 631123, printed 687123 (difference 56000)
  - sgt1928 p.150 (f702) operations 1920: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 632381, printed 632384 (difference 3)
  - sgt1928 p.150 (f702) operations 1921: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 737797, printed 737747 (difference -50)
  - sgt1928 p.150 (f702) operations 1919: Total@tg = tg_dep_tunisia + tg_dep_france + tg_dep_foreign + tg_arr_tunisia + tg_arr_france + tg_arr_foreign + tg_official_dep + tg_official_arr: cells give 1829680, printed 1830130 (difference 450)
  - sgt1928 p.151 (f703) operations 1925: Total@coll_amt = coll_tunisia_amt + coll_france_amt + coll_foreign_amt: cells give 91410305, printed 91420305 (difference 10000)
  - sgt1928 p.151 (f703) operations 1926: Total@coll_amt = coll_tunisia_amt + coll_france_amt + coll_foreign_amt: cells give 117304515, printed 117304535 (difference 20)
  - sgt1928 p.151 (f703) operations 1923: Total@tg = tg_dep_tunisia + tg_dep_france + tg_dep_foreign + tg_arr_tunisia + tg_arr_france + tg_arr_foreign + tg_official_dep + tg_official_arr: cells give 1425990, printed 1426020 (difference 30)
  - sgt1928 p.151 (f703) operations 1923: Total@cne_n = cne_deposits_n + cne_withdrawals_n: cells give 65622, printed 70394 (difference 4772)
  - sgt1928 p.151 (f703) operations 1924: Total@cne_n = cne_deposits_n + cne_withdrawals_n: cells give 70225, printed 74678 (difference 4453)
  - sgt1929 p.150 (f178) operations 1920: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 314851329, printed 314851330 (difference 1)
  - sgt1929 p.150 (f178) operations 1921: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 314589723, printed 318589723 (difference 4000000)
  - sgt1929 p.150 (f178) operations 1922: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 280797065, printed 280797060 (difference -5)
  - sgt1929 p.151 (f179) operations 1924: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 401427075, printed 401427074 (difference -1)
  - sgt1929 p.151 (f179) operations 1928: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 672871104, printed 672871101 (difference -3)
  - sgt1929 p.152 (f180) operations 1920: Total@coll_n = coll_tunisia_n + coll_france_n + coll_foreign_n: cells give 216241, printed 216245 (difference 4)
  - sgt1929 p.152 (f180) operations 1920: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 632381, printed 632384 (difference 3)
  - sgt1929 p.152 (f180) operations 1921: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 737797, printed 737747 (difference -50)
  - sgt1929 p.153 (f181) operations 1925: Total@coll_amt = coll_tunisia_amt + coll_france_amt + coll_foreign_amt: cells give 91410305, printed 91420305 (difference 10000)
  - sgt1929 p.153 (f181) operations 1926: Total@coll_amt = coll_tunisia_amt + coll_france_amt + coll_foreign_amt: cells give 117304515, printed 117304535 (difference 20)
  - sgt1929 p.153 (f181) operations 1923: Total@tg = tg_dep_tunisia + tg_dep_france + tg_dep_foreign + tg_arr_tunisia + tg_arr_france + tg_arr_foreign + tg_official_dep + tg_official_arr: cells give 1425990, printed 1426020 (difference 30)
  - sgt1929 p.153 (f181) operations 1923: Total@cne_n = cne_deposits_n + cne_withdrawals_n: cells give 65622, printed 70394 (difference 4772)
  - sgt1929 p.153 (f181) operations 1924: Total@cne_n = cne_deposits_n + cne_withdrawals_n: cells give 70225, printed 74678 (difference 4453)
  - sgt1930 p.154 (f712) operations 1921: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 314589723, printed 318589723 (difference 4000000)
  - sgt1930 p.154 (f712) operations 1922: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 280797065, printed 280797060 (difference -5)
  - sgt1930 p.155 (f713) operations 1924: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 401427075, printed 401427074 (difference -1)
  - sgt1930 p.155 (f713) operations 1928: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 672871104, printed 672871101 (difference -3)
  - sgt1930 p.156 (f714) operations 1921: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 737797, printed 737747 (difference -50)
  - sgt1930 p.156 (f714) operations 1923: Total@tg = tg_dep_tunisia + tg_dep_france + tg_dep_foreign + tg_arr_tunisia + tg_arr_france + tg_arr_foreign + tg_official_dep + tg_official_arr: cells give 1425990, printed 1426020 (difference 30)
  - sgt1930 p.156 (f714) operations 1923: Total@cne_n = cne_deposits_n + cne_withdrawals_n: cells give 65622, printed 70394 (difference 4772)
  - sgt1930 p.157 (f715) operations 1925: Total@coll_amt = coll_tunisia_amt + coll_france_amt + coll_foreign_amt: cells give 91410305, printed 91420305 (difference 10000)
  - sgt1930 p.157 (f715) operations 1926: Total@coll_amt = coll_tunisia_amt + coll_france_amt + coll_foreign_amt: cells give 117304515, printed 117304535 (difference 20)
  - sgt1930 p.157 (f715) operations 1924: Total@cne_n = cne_deposits_n + cne_withdrawals_n: cells give 70225, printed 74678 (difference 4453)
  - sgt1935 p.90 (f110) operations 1928: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 672871104, printed 672871101 (difference -3)
  - sgt1935 p.91 (f111) operations 1934: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 505379525, printed 505379527 (difference 2)
  - sgt1935 p.91 (f111) operations 1935: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 400182150, printed 507654550 (difference 107472400)
  - sgt1935 p.92 (f112) operations 1926: Total@coll_amt = coll_tunisia_amt + coll_france_amt + coll_foreign_amt: cells give 117304515, printed 117304535 (difference 20)
  - sgt1935 p.93 (f113) operations 1935: Total@coll_amt = coll_tunisia_amt + coll_france_amt + coll_foreign_amt: cells give 94331974.00, printed 90331974 (difference -4000000.00)
  - sgt1935 p.93 (f113) operations 1933: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 1240519, printed 1241019 (difference 500)
  - sgt1935 p.93 (f113) operations 1934: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 1042717, printed 1032717 (difference -10000)
  - sgt1935 p.93 (f113) operations 1935: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 838183, printed 842183 (difference 4000)
  - sgt1935 p.93 (f113) operations 1935: Total@cne_n = cne_deposits_n + cne_withdrawals_n: cells give 122303, printed 130735 (difference 8432)
  - sgt1936 p.68 (f79) operations 1929: Total@corr = corr_tunisia + corr_france + corr_foreign: cells give 120791796, printed 120791696 (difference -100)
  - sgt1936 p.68 (f79) operations 1928: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 672844104, printed 672871101 (difference 26997)
  - sgt1936 p.69 (f80) operations 1932: Total@corr = corr_tunisia + corr_france + corr_foreign: cells give 89601000, printed 89601500 (difference 500)
  - sgt1936 p.69 (f80) operations 1934: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 505379525, printed 505379527 (difference 2)
  - sgt1936 p.69 (f80) operations 1935: Total@mo_amt = mo_issued_tunisia_amt + mo_issued_france_amt + mo_issued_foreign_amt + mo_paid_tunisia_amt + mo_paid_france_amt + mo_paid_foreign_amt: cells give 400182150, printed 507654550 (difference 107472400)
  - sgt1936 p.70 (f81) operations 1927: Total@coll_n = coll_tunisia_n + coll_france_n + coll_foreign_n: cells give 484966, printed 484956 (difference -10)
  - sgt1936 p.71 (f82) operations 1935: Total@coll_amt = coll_tunisia_amt + coll_france_amt + coll_foreign_amt: cells give 94331974.00, printed 90331974 (difference -4000000.00)
  - sgt1936 p.71 (f82) operations 1933: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 1240609, printed 1241019 (difference 410)
  - sgt1936 p.71 (f82) operations 1934: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 1042717, printed 1032717 (difference -10000)
  - sgt1936 p.71 (f82) operations 1935: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 838183, printed 842183 (difference 4000)
  - sgt1936 p.71 (f82) operations 1935: Total@cne_n = cne_deposits_n + cne_withdrawals_n: cells give 122303, printed 130735 (difference 8432)
  - sgt1939 p.73 (f79) operations 1933: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 1240609, printed 1241019 (difference 410)
  - sgt1939 p.73 (f79) operations 1934: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 1042717, printed 1032717 (difference -10000)
  - sgt1939 p.73 (f79) operations 1935: Total@parcels = parcels_dep_tunisia + parcels_dep_france + parcels_dep_foreign + parcels_arr_tunisia + parcels_arr_france + parcels_arr_foreign: cells give 838183, printed 842183 (difference 4000)
  - sgt1939 p.75 (f81) operations 1935: Total@cne_n = cne_deposits_n + cne_withdrawals_n: cells give 122303, printed 130735 (difference 8432)
  - sgt1939 p.75 (f81) operations 1938: Total@cne_amt = cne_deposits_amt + cne_withdrawals_amt: cells give 192146575.58, printed 192146575.08 (difference -0.50)

- Overlapping printings: 4376 cell comparisons with other editions printing the same cell; 33 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1914 / correspondence / france / number | sgt1922 | 39200953 | sgt1923 | 39200958 |
| 1920 / deposits /  / number | sgt1922 | 38352 | sgt1929 | 38362 |
| 1920 / deposits /  / number | sgt1923 | 38352 | sgt1929 | 38362 |
| 1920 / deposits /  / number | sgt1924 | 38352 | sgt1929 | 38362 |
| 1920 / deposits /  / number | sgt1925 | 38352 | sgt1929 | 38362 |
| 1920 / deposits /  / number | sgt1926 | 38352 | sgt1929 | 38362 |
| 1920 / deposits /  / number | sgt1927 | 38352 | sgt1929 | 38362 |
| 1920 / deposits /  / number | sgt1928 | 38352 | sgt1929 | 38362 |
| 1920 / depositors_balance /  / amount | sgt1922 | 15646187.93 | sgt1929 | 15643865.54 |
| 1920 / depositors_balance /  / amount | sgt1923 | 15646187.93 | sgt1929 | 15643865.54 |
| 1920 / depositors_balance /  / amount | sgt1924 | 15646187.93 | sgt1929 | 15643865.54 |
| 1920 / depositors_balance /  / amount | sgt1925 | 15646187.93 | sgt1929 | 15643865.54 |
| 1920 / depositors_balance /  / amount | sgt1926 | 15646187.93 | sgt1929 | 15643865.54 |
| 1920 / depositors_balance /  / amount | sgt1927 | 15646187.93 | sgt1929 | 15643865.54 |
| 1920 / depositors_balance /  / amount | sgt1928 | 15646187.93 | sgt1929 | 15643865.54 |
| 1923 / parcels_dispatched / france / number | sgt1923 | 57719 | sgt1930 | 87719 |
| 1923 / depositors_balance /  / amount | sgt1923 | 27376964.20 | sgt1930 | 27376761.87 |
| 1923 / depositors_balance /  / amount | sgt1924 | 27376964.20 | sgt1930 | 27376761.87 |
| 1923 / depositors_balance /  / amount | sgt1925 | 27376964.20 | sgt1930 | 27376761.87 |
| 1923 / depositors_balance /  / amount | sgt1926 | 27376964.20 | sgt1930 | 27376761.87 |
| 1923 / depositors_balance /  / amount | sgt1927 | 27376964.20 | sgt1930 | 27376761.87 |
| 1923 / depositors_balance /  / amount | sgt1928 | 27376964.20 | sgt1930 | 27376761.87 |
| 1926 / telegrams_sent / foreign / number | sgt1926 | 43924 | sgt1935 | 43921 |
| 1926 / conversations /  / number | sgt1927 | 7089114 | sgt1935 | 7089111 |
| 1926 / conversations /  / number | sgt1928 | 7089114 | sgt1935 | 7089111 |
| 1926 / conversations /  / number | sgt1929 | 7089114 | sgt1935 | 7089111 |
| 1926 / conversations /  / number | sgt1930 | 7089114 | sgt1935 | 7089111 |
| 1928 / money_orders_paid / foreign / amount | sgt1936 | 3658894 | sgt1935 | 3685894 |
| 1932 / correspondence / france / number | sgt1936 | 50350000 | sgt1935 | 50350500 |
| 1933 / parcels_dispatched / tunisia / number | sgt1935 | 67847 | sgt1939 | 67947 |
| 1933 / parcels_dispatched / france / number | sgt1935 | 95193 | sgt1939 | 95183 |
| 1935 / withdrawals /  / amount | sgt1936 | 6920421.16 | sgt1935 | 61920421.16 |
| 1935 / withdrawals /  / amount | sgt1939 | 6920421.16 | sgt1935 | 61920421.16 |

- Flagged cells: derived_from_totals: 1, not_applicable: 3, reprint_corrected: 3, row_realigned: 1.

  - sgt1935 p.90 1928 posts / money_orders_paid / foreign / amount / francs = 3685894 (reprint_corrected)
  - sgt1936 p.71 1930 savings / passbooks_opened /  / number / count = NA (not_applicable)
  - sgt1935 p.91 1932 posts / correspondence / france / number / count = 50350500 (reprint_corrected)
  - sgt1935 p.93 1935 savings / withdrawals /  / amount / francs = 61920421.16 (reprint_corrected)
  - sgt1936 p.69 1935 posts / money_orders_issued / france / amount / francs = 107579990 (derived_from_totals)
  - sgt1939 p.75 1937 telephones / conversations /  / number / count = 11019235 (row_realigned)
  - sgt1939 p.73 1938 telegraphs / telegrams_official_sent /  / number / count = NA (not_applicable)
  - sgt1939 p.73 1938 telegraphs / telegrams_official_received /  / number / count = NA (not_applicable)

## Image versus OCR

- Read cell by cell on the page images (56 printings): sgt1922 f154, sgt1922 f155, sgt1922 f156, sgt1922 f157, sgt1923 f638, sgt1923 f639, sgt1923 f640, sgt1923 f641, sgt1924 f1128, sgt1924 f1129, sgt1924 f1130, sgt1924 f1131, sgt1925 f164, sgt1925 f165, sgt1925 f166, sgt1925 f167, sgt1926 f714, sgt1926 f715, sgt1926 f716, sgt1926 f717, sgt1927 f176, sgt1927 f177, sgt1927 f178, sgt1927 f179, sgt1928 f700, sgt1928 f701, sgt1928 f702, sgt1928 f703, sgt1929 f178, sgt1929 f179, sgt1929 f180, sgt1929 f181, sgt1930 f712, sgt1930 f713, sgt1930 f714, sgt1930 f715, sgt1935 f110, sgt1935 f111, sgt1935 f112, sgt1935 f113, sgt1936 f79, sgt1936 f80, sgt1936 f81, sgt1936 f82, sgt1939 f78, sgt1939 f78, sgt1939 f79, sgt1939 f79, sgt1939 f79, sgt1939 f78, sgt1939 f79, sgt1939 f80, sgt1939 f81, sgt1939 f81, sgt1939 f80, sgt1939 f81.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
