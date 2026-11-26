# Postes, Télégraphes, Téléphones. Renseignements généraux : c) Situation financière

*Posts, telegraphs and telephones: revenue, expenditure and balance.*

Source: *Statistique générale de la Tunisie*, chapter *Postes - Télégraphes - Téléphones*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 132, f156; sgt1923 (`bpt6k9105649x`): p. 138, f640; sgt1924 (`bpt6k9105649x`): p. 140, f1130; sgt1925 (`bpt6k9105650k`): p. 142, f166; sgt1926 (`bpt6k9105650k`): p. 152, f716; sgt1927 (`bpt6k91056510`): p. 150, f178; sgt1928 (`bpt6k91056510`): p. 150, f702; sgt1929 (`bpt6k9105652d`): p. 152, f180; sgt1930 (`bpt6k9105652d`): p. 156, f714, p. 157, f715; sgt1935 (`bpt6k9105653t`): p. 92, f112, p. 93, f113; sgt1936 (`bpt6k91056547`): p. 70, f81, p. 71, f82.

Transcriptions: `../transcribed/posts_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_posts.py build`.

Rows: 192. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936.

Unit: francs; value_type: francs.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing of the same cell, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`): the latest edition printing that year
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (network: situation at 31 December)
- `item`: item code (English)
- `item_fr`: printed line heading
- `kind`: `revenue` (Produits), `expenses` (Dépenses), `balance` (Produit net / Déficit)
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible` (NA, cut by the binding or broken type), `not_applicable` (nothing printed, or » in a line not yet collected; NA), `row_realigned` (printed in the wrong column or line, stored on the year / item it belongs to), `reprint_corrected` (kept from an earlier printing), `derived_from_totals`

Financial years: the columns 1930 and 1932 of the Exploitation and Situation financière tables are printed "Année 1930 (15 mois)" and "Année 1932 (9 mois)" (sgt1930 heads its last column "Année 1930 (15 mois)"); stored as years 1930 and 1932.

Footnote (1) of sgt1922-sgt1926: "Y compris la subvention aux services maritimes postaux" (including the subsidy to the postal shipping services), attached to the Dépenses line.

Line Loyers payés par le Gouvernement Tunisien printed » in every year (stored 0). sgt1922 prints Dépenses, Produit net and Déficit » for 1922 (stored 0 in that printing, superseded by sgt1923-sgt1930). From 1933 the Dépenses, Produit net and Déficit lines are printed » (no figure): stored NA (`not_applicable`). sgt1930 prints for 1930 (15 months) Dépenses 11.375.053 and Déficit 23.113.851 (the revenue total less 11.375.053 is a surplus of 23.113.851, not a deficit); sgt1935 and sgt1936 print 50.072.598 and 15.583.694, which are kept.

Not printed in sgt1939.

Failed checks, grouped (printed values kept). A failure that recurs identically in several editions was read independently on each printing, so it is the printed figure; every failure printed by one edition only was re-read on a zoomed native-resolution crop: finance 1917 Totaux - Dépenses: cells -608481, printed 57197 (in sgt1922, sgt1923, sgt1924, sgt1925, sgt1926); finance 1918 Total@rev: cells 3997579, printed 3997539 (in sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927); finance 1918 Totaux - Dépenses: cells -25199, printed -690877 (in sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927); finance 1920 Total@rev: cells 6540484, printed 6462255 (in sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928); finance 1920 Total@rev: cells 6540473, printed 6462255 (in sgt1929); finance 1921 Totaux - Dépenses: cells -5462291, printed -5462309 (in sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930); finance 1922 Total@rev: cells 8459455, printed 8348837 (in sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930); finance 1922 Totaux - Dépenses: cells 8348837, printed 0 (in sgt1922); finance 1929 Total@rev: cells 26624652, printed 26276902 (in sgt1929, sgt1930, sgt1935, sgt1936); finance 1930 Totaux - Dépenses: cells 23113851, printed -23113851 (in sgt1930); finance 1931 Total@rev: cells 30528188, printed 29075474 (in sgt1935, sgt1936); finance 1933 Total@rev: cells 30326668, printed 30320668 (in sgt1935, sgt1936); finance 1935 Total@rev: cells 29488508.79, printed 29538508.79 (in sgt1936).

Printings not compared because the cell is illegible in that printing (cut by the binding): 13.

Flagged cells: (1935, 'rev_telephones'): kept sgt1935's 9055617.29 (reprint_corrected); sgt1936 prints 9.005.617 29; sgt1935's 9.055.617 29 gives the Totaux 29.538.508 79 printed by both.

Survey of the whole chapter in every edition: `posts_survey.md`.

## Validation

- Checks against printed totals and identities: 211; passed: 157; failed: 54.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.133 (f157) finance 1918: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 3997579, printed 3997539 (difference -40)
  - sgt1922 p.133 (f157) finance 1920: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 6540484, printed 6462255 (difference -78229)
  - sgt1922 p.133 (f157) finance 1922: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 8459455, printed 8348837 (difference -110618)
  - sgt1922 p.133 (f157) finance 1917: Totaux - Dépenses = Produit net - Déficit: cells give -608481, printed 57197 (difference 665678)
  - sgt1922 p.133 (f157) finance 1918: Totaux - Dépenses = Produit net - Déficit: cells give -25199, printed -690877 (difference -665678)
  - sgt1922 p.133 (f157) finance 1921: Totaux - Dépenses = Produit net - Déficit: cells give -5462291, printed -5462309 (difference -18)
  - sgt1922 p.133 (f157) finance 1922: Totaux - Dépenses = Produit net - Déficit: cells give 8348837, printed 0 (difference -8348837)
  - sgt1923 p.139 (f641) finance 1918: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 3997579, printed 3997539 (difference -40)
  - sgt1923 p.139 (f641) finance 1920: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 6540484, printed 6462255 (difference -78229)
  - sgt1923 p.139 (f641) finance 1922: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 8459455, printed 8348837 (difference -110618)
  - sgt1923 p.139 (f641) finance 1917: Totaux - Dépenses = Produit net - Déficit: cells give -608481, printed 57197 (difference 665678)
  - sgt1923 p.139 (f641) finance 1918: Totaux - Dépenses = Produit net - Déficit: cells give -25199, printed -690877 (difference -665678)
  - sgt1923 p.139 (f641) finance 1921: Totaux - Dépenses = Produit net - Déficit: cells give -5462291, printed -5462309 (difference -18)
  - sgt1924 p.140 (f1130) finance 1917: Totaux - Dépenses = Produit net - Déficit: cells give -608481, printed 57197 (difference 665678)
  - sgt1924 p.141 (f1131) finance 1918: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 3997579, printed 3997539 (difference -40)
  - sgt1924 p.141 (f1131) finance 1920: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 6540484, printed 6462255 (difference -78229)
  - sgt1924 p.141 (f1131) finance 1922: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 8459455, printed 8348837 (difference -110618)
  - sgt1924 p.141 (f1131) finance 1918: Totaux - Dépenses = Produit net - Déficit: cells give -25199, printed -690877 (difference -665678)
  - sgt1924 p.141 (f1131) finance 1921: Totaux - Dépenses = Produit net - Déficit: cells give -5462291, printed -5462309 (difference -18)
  - sgt1925 p.142 (f166) finance 1918: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 3997579, printed 3997539 (difference -40)
  - sgt1925 p.142 (f166) finance 1917: Totaux - Dépenses = Produit net - Déficit: cells give -608481, printed 57197 (difference 665678)
  - sgt1925 p.142 (f166) finance 1918: Totaux - Dépenses = Produit net - Déficit: cells give -25199, printed -690877 (difference -665678)
  - sgt1925 p.143 (f167) finance 1920: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 6540484, printed 6462255 (difference -78229)
  - sgt1925 p.143 (f167) finance 1922: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 8459455, printed 8348837 (difference -110618)
  - sgt1925 p.143 (f167) finance 1921: Totaux - Dépenses = Produit net - Déficit: cells give -5462291, printed -5462309 (difference -18)
  - sgt1926 p.152 (f716) finance 1918: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 3997579, printed 3997539 (difference -40)
  - sgt1926 p.152 (f716) finance 1917: Totaux - Dépenses = Produit net - Déficit: cells give -608481, printed 57197 (difference 665678)
  - sgt1926 p.152 (f716) finance 1918: Totaux - Dépenses = Produit net - Déficit: cells give -25199, printed -690877 (difference -665678)
  - sgt1926 p.153 (f717) finance 1920: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 6540484, printed 6462255 (difference -78229)
  - sgt1926 p.153 (f717) finance 1922: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 8459455, printed 8348837 (difference -110618)
  - sgt1926 p.153 (f717) finance 1921: Totaux - Dépenses = Produit net - Déficit: cells give -5462291, printed -5462309 (difference -18)
  - sgt1927 p.150 (f178) finance 1918: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 3997579, printed 3997539 (difference -40)
  - sgt1927 p.150 (f178) finance 1920: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 6540484, printed 6462255 (difference -78229)
  - sgt1927 p.150 (f178) finance 1918: Totaux - Dépenses = Produit net - Déficit: cells give -25199, printed -690877 (difference -665678)
  - sgt1927 p.151 (f179) finance 1922: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 8459455, printed 8348837 (difference -110618)
  - sgt1927 p.151 (f179) finance 1921: Totaux - Dépenses = Produit net - Déficit: cells give -5462291, printed -5462309 (difference -18)
  - sgt1928 p.150 (f702) finance 1920: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 6540484, printed 6462255 (difference -78229)
  - sgt1928 p.150 (f702) finance 1921: Totaux - Dépenses = Produit net - Déficit: cells give -5462291, printed -5462309 (difference -18)
  - sgt1928 p.151 (f703) finance 1922: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 8459455, printed 8348837 (difference -110618)
  - sgt1929 p.152 (f180) finance 1920: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 6540473, printed 6462255 (difference -78218)
  - sgt1929 p.152 (f180) finance 1922: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 8459455, printed 8348837 (difference -110618)
  - sgt1929 p.152 (f180) finance 1921: Totaux - Dépenses = Produit net - Déficit: cells give -5462291, printed -5462309 (difference -18)
  - sgt1929 p.153 (f181) finance 1929: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 26624652, printed 26276902 (difference -347750)
  - sgt1930 p.156 (f714) finance 1922: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 8459455, printed 8348837 (difference -110618)
  - sgt1930 p.156 (f714) finance 1921: Totaux - Dépenses = Produit net - Déficit: cells give -5462291, printed -5462309 (difference -18)
  - sgt1930 p.157 (f715) finance 1929: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 26624652, printed 26276902 (difference -347750)
  - sgt1930 p.157 (f715) finance 1930: Totaux - Dépenses = Produit net - Déficit: cells give 23113851, printed -23113851 (difference -46227702)
  - sgt1935 p.93 (f113) finance 1929: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 26624652, printed 26276902 (difference -347750)
  - sgt1935 p.93 (f113) finance 1931: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 30528188, printed 29075474 (difference -1452714)
  - sgt1935 p.93 (f113) finance 1933: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 30326668, printed 30320668 (difference -6000)
  - sgt1936 p.70 (f81) finance 1929: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 26624652, printed 26276902 (difference -347750)
  - sgt1936 p.71 (f82) finance 1931: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 30528188, printed 29075474 (difference -1452714)
  - sgt1936 p.71 (f82) finance 1933: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 30326668, printed 30320668 (difference -6000)
  - sgt1936 p.71 (f82) finance 1935: Total@rev = rev_posts + rev_telegraphs + rev_telephones + rev_rents + rev_cne_subsidy: cells give 29488508.79, printed 29538508.79 (difference 50000.00)

- Overlapping printings: 675 cell comparisons with other editions printing the same cell; 12 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1920 / rev_cne_subsidy | sgt1922 | 78230 | sgt1929 | 78219 |
| 1920 / rev_cne_subsidy | sgt1923 | 78230 | sgt1929 | 78219 |
| 1920 / rev_cne_subsidy | sgt1924 | 78230 | sgt1929 | 78219 |
| 1920 / rev_cne_subsidy | sgt1925 | 78230 | sgt1929 | 78219 |
| 1920 / rev_cne_subsidy | sgt1926 | 78230 | sgt1929 | 78219 |
| 1920 / rev_cne_subsidy | sgt1927 | 78230 | sgt1929 | 78219 |
| 1920 / rev_cne_subsidy | sgt1928 | 78230 | sgt1929 | 78219 |
| 1922 / expenses | sgt1922 | 0 | sgt1930 | 14374897 |
| 1922 / deficit | sgt1922 | 0 | sgt1930 | 6026060 |
| 1930 / expenses | sgt1930 | 11375053 | sgt1936 | 50072598 |
| 1930 / deficit | sgt1930 | 23113851 | sgt1936 | 15583694 |
| 1935 / rev_telephones | sgt1936 | 9005617.29 | sgt1935 | 9055617.29 |

- Flagged cells: not_applicable: 12, reprint_corrected: 1.

  - sgt1936 p.71 1933 expenses / expenses = NA (not_applicable)
  - sgt1936 p.71 1933 net_product / balance = NA (not_applicable)
  - sgt1936 p.71 1933 deficit / balance = NA (not_applicable)
  - sgt1936 p.71 1934 expenses / expenses = NA (not_applicable)
  - sgt1936 p.71 1934 net_product / balance = NA (not_applicable)
  - sgt1936 p.71 1934 deficit / balance = NA (not_applicable)
  - sgt1935 p.93 1935 rev_telephones / revenue = 9055617.29 (reprint_corrected)
  - sgt1936 p.71 1935 expenses / expenses = NA (not_applicable)
  - sgt1936 p.71 1935 net_product / balance = NA (not_applicable)
  - sgt1936 p.71 1935 deficit / balance = NA (not_applicable)
  - sgt1936 p.71 1936 expenses / expenses = NA (not_applicable)
  - sgt1936 p.71 1936 net_product / balance = NA (not_applicable)
  - sgt1936 p.71 1936 deficit / balance = NA (not_applicable)

## Image versus OCR

- Read cell by cell on the page images (22 printings): sgt1922 f156, sgt1922 f157, sgt1923 f640, sgt1923 f641, sgt1924 f1130, sgt1924 f1131, sgt1925 f166, sgt1925 f167, sgt1926 f716, sgt1926 f717, sgt1927 f178, sgt1927 f179, sgt1928 f702, sgt1928 f703, sgt1929 f180, sgt1929 f181, sgt1930 f714, sgt1930 f715, sgt1935 f112, sgt1935 f113, sgt1936 f81, sgt1936 f82.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
