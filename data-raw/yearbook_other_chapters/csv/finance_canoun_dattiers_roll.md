# Canoun des dattiers. c) Répartition des dattiers entre les européens et les indigènes

*Tax on date palms (canoun des dattiers): trees taxed and not taxed on the European and indigenous rolls, articles and individual accounts.*

Source: *Statistique générale de la Tunisie*, chapter *Finances*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views: sgt1922 (`bpt6k9105649x`): p. 190, f214, p. 191, f215; sgt1923 (`bpt6k9105649x`): p. 202, f704, p. 203, f705; sgt1924 (`bpt6k9105649x`): p. 210, f1200, p. 211, f1201; sgt1925 (`bpt6k9105650k`): p. 246, f270, p. 247, f271; sgt1926 (`bpt6k9105650k`): p. 222, f786, p. 223, f787; sgt1927 (`bpt6k91056510`): p. 220, f248, p. 221, f249; sgt1928 (`bpt6k91056510`): p. 220, f772, p. 221, f773; sgt1929 (`bpt6k9105652d`): p. 222, f250, p. 223, f251; sgt1930 (`bpt6k9105652d`): p. 222, f784, p. 223, f785.

Transcriptions: `../transcribed/finance_canoun_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_finance_canoun.py build`.

Rows: 540. Years: 1922, 1923, 1924, 1926, 1927, 1928, 1929, 1930.

Units: trees, articles (entries of the matrice) and accounts (comptes individuels), see `unit`; value_type: mixed (counts of three kinds).

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
- `tree_kind`: `degla` (dattiers degla, the deglet nour palms) or `common` (dattiers communs)
- `tree_kind_fr`: printed block / column heading
- `roll`: `european` (Européens) or `indigenous` (Indigènes)
- `roll_fr`: printed column heading
- `status`: `taxed` (imposés) or `not_taxed` (non imposés: young trees, mâles / sauvages); empty for articles and accounts
- `status_fr`: printed column heading
- `value`: printed count (» = 0)
- `flag`: empty, or `total_mismatch` (printed value kept; the line TOTAL and the column Totaux, or the other tables of the same edition, identify it as the faulty cell; see the notes), `row_realigned` (figures printed on the line of another caïdat, stored under the caïdat they belong to; see the notes), `derived_from_totals` (digits lost in the gutter fold; value = line TOTAL minus the other cells of the line)

Printed under b) on the same spread: Européens and Indigènes x Dattiers degla / Dattiers communs x Imposés / non Imposés (trees), then Nombre d'articles de matrice and Nombre de comptes individuels (Européens, Indigènes, TOTAL). The TOTAL columns and the Totaux line are checks; imposés E + I = a) 20 ans imposables and non imposés E + I = a) mâles + Total des jeunes are checked line by line (in sgt1928 the communs non imposés equal a) Total des jeunes, i.e. exclude the mâles; checked so). Not printed in sgt1935.

Footnotes: none printed under these tables.

## Validation

- Checks against printed totals and identities: 450; passed: 443; failed: 7.

Every failure was re-read on zoomed native-resolution crops; printed values are kept. Explanation, by edition:

  - sgt1922: Totaux indigènes degla non imposés printed 60.135, the lines sum to 60.136 (and a) gives 62.551 - 2.415 = 60.136); misprint of the check line.
  - sgt1925: Nefzaoua indigènes communs imposés printed 224.361 (b), a) and the column Totaux require 224.363; flagged); Gafsa communs non imposés 63 + 19.429 = 19.492 against a) 25.492, which carries the misprinted Total des jeunes of a).
  - sgt1927: Ouerghemma indigènes communs imposés printed 23.269 (zoomed; the column Totaux 1.083.149 adds it as printed) while a) and b) give 74.562 - 1.293 = 73.269: flagged; the Totaux follow it.

Failed checks:

  - sgt1922 dattiers_roll Totaux i_dg_n: sum of the lines (f214): cells give 60136, printed 60135 (difference -1)
  - sgt1925 dattiers_roll Totaux i_cm_i: sum of the lines (f270): cells give 1130479, printed 1130481 (difference 2)
  - sgt1922 dattiers_roll Totaux degla: non imposés E + I = a) mâles + Total des jeunes: cells give 62550, printed 62551 (difference 1)
  - sgt1925 dattiers_roll 5e Région ;  ; Gafsa communs: non imposés E + I = a) mâles + Total des jeunes: cells give 19492, printed 25492 (difference 6000)
  - sgt1925 dattiers_roll Territoires militaires ;  ; Nefzaoua communs: imposés E + I = a) 20 ans imposables: cells give 224428, printed 224430 (difference 2)
  - sgt1927 dattiers_roll Territoires militaires ;  ; Ouerghemma communs: imposés E + I = a) 20 ans imposables: cells give 24562, printed 74562 (difference 50000)
  - sgt1927 dattiers_roll Totaux communs: imposés E + I = a) 20 ans imposables: cells give 1088003, printed 1138003 (difference 50000)

- Flagged cells: total_mismatch: 2.

  - sgt1925 p.246 Nefzaoua / trees / common / indigenous / taxed = 224361 (total_mismatch)
  - sgt1927 p.220 Ouerghemma / trees / common / indigenous / taxed = 23269 (total_mismatch)

## Image versus OCR

- Read cell by cell on native-resolution crops of the page images (strips of rows, gutter columns on both views of the spread, every failing check re-read zoomed): sgt1922 f214, sgt1922 f215, sgt1923 f704, sgt1923 f705, sgt1924 f1200, sgt1924 f1201, sgt1925 f270, sgt1925 f271, sgt1926 f786, sgt1926 f787, sgt1927 f248, sgt1927 f249, sgt1928 f772, sgt1928 f773, sgt1929 f250, sgt1929 f251, sgt1930 f784, sgt1930 f785.
- The Gallica OCR was not used (no cell is flagged `ocr_corrected`).

Survey of the canoun tables in every edition: `finance_canoun_survey.md`.
