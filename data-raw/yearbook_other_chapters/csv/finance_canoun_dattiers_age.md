# Canoun des dattiers. a) Relevé par caïdat du nombre d'arbres d'après leur âge

*Tax on date palms (canoun des dattiers): trees by caïdat, kind and age.*

Source: *Statistique générale de la Tunisie*, chapter *Finances*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views: sgt1922 (`bpt6k9105649x`): p. 188, f212, p. 189, f213; sgt1923 (`bpt6k9105649x`): p. 200, f702, p. 201, f703; sgt1924 (`bpt6k9105649x`): p. 208, f1198, p. 209, f1199; sgt1925 (`bpt6k9105650k`): p. 244, f268, p. 245, f269; sgt1926 (`bpt6k9105650k`): p. 220, f784, p. 221, f785; sgt1927 (`bpt6k91056510`): p. 218, f246, p. 219, f247; sgt1928 (`bpt6k91056510`): p. 218, f770, p. 219, f771; sgt1929 (`bpt6k9105652d`): p. 220, f248, p. 221, f249; sgt1930 (`bpt6k9105652d`): p. 220, f782, p. 221, f783; sgt1935 (`bpt6k9105653t`): p. 114, f134, p. 115, f135.

Transcriptions: `../transcribed/finance_canoun_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_finance_canoun.py build`.

Rows: 2244. Years: 1922, 1923, 1924, 1926, 1927, 1928, 1929, 1930, 1935.

Unit: number of trees; value_type: count.

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
- `tree_kind`: `degla` (dattiers degla, the deglet nour palms) or `common` (dattiers communs)
- `tree_kind_fr`: printed block / column heading
- `age_class`: `male` (mâles, date palms), `wild` (arbres sauvages, olive trees), `under_1` (moins d'un an), `age_01` .. `age_19` (1 an .. 19 ans: young trees, not taxed), `taxable_20_plus` (20 ans imposables)
- `age_class_fr`: printed column heading
- `value`: printed count (» = 0)
- `flag`: empty, or `total_mismatch` (printed value kept; the line TOTAL and the column Totaux, or the other tables of the same edition, identify it as the faulty cell; see the notes), `row_realigned` (figures printed on the line of another caïdat, stored under the caïdat they belong to; see the notes), `derived_from_totals` (digits lost in the gutter fold; value = line TOTAL minus the other cells of the line)

Two blocks, Dattiers degla and Dattiers communs, each by caïdat (the date-palm caïdats of the south: Nefzaoua, Ouerghemma, L'Arad / Gabès, Gafsa, Djerid / Tozeur) with columns 2 Mâles (male palms, not taxed), 3 Moins d'un an, 4-22 1 an .. 19 ans, 23 Total des jeunes, 24 20 ans imposables, 25 Total des colonnes 2, 23 et 24. Stored: columns 2-22 and 24; Total des jeunes, Total and the Totaux lines are checks. A palm becomes taxable at 20 years; the young trees move one age column per edition. Printed sgt1922-sgt1930 and sgt1935 (from sgt1925 grouped under 5e Région / Territoires militaires; Gabès and Tozeur replace L'Arad and Djerid; Matmata added in sgt1935). The sgt1925 title still reads "1er novembre 1924" (year coded 1924; figures differ from sgt1924).

Footnotes: none printed under these tables.

## Validation

- Checks against printed totals and identities: 724; passed: 714; failed: 10.

Every failure was re-read on zoomed native-resolution crops; printed values are kept. Explanation, by edition:

  - sgt1922: Djerid degla Total des jeunes printed 57.352, the ages sum to 56.352; the column Totaux 62.551 follows the misprint (c) non imposés 2.338 + 55.014 = 57.352 also; check column, not stored).
  - sgt1928: Degla Tozeur 18 ans printed 8.138 (Total des jeunes requires 8.183, as in sgt1927): flagged; the column Totaux 9.500 and Total des jeunes 113.524 are 1 off their lines (check line).
  - sgt1925: Communs: Nefzaoua moins d'un an printed 91.022 (Total des jeunes, the column Totaux and c) require 71.022; flagged); Gafsa Total des jeunes printed 18.923 for 12.923 (check column).

Failed checks:

  - sgt1925 dattiers_age communs Totaux a0: sum of the lines (f268): cells give 551990, printed 531990 (difference -20000)
  - sgt1925 dattiers_age communs Totaux tj: sum of the lines (f269): cells give 1036473, printed 1030473 (difference -6000)
  - sgt1928 dattiers_age degla Totaux a18: sum of the lines (f771): cells give 9456, printed 9500 (difference 44)
  - sgt1922 dattiers_age degla Djerid: Total des jeunes = moins d'un an + 1 .. 19 ans: cells give 56352, printed 57352 (difference 1000)
  - sgt1922 dattiers_age degla Totaux: Total des jeunes = moins d'un an + 1 .. 19 ans: cells give 61551, printed 62551 (difference 1000)
  - sgt1925 dattiers_age communs 5e Région ;  ; Gafsa: Total des jeunes = moins d'un an + 1 .. 19 ans: cells give 12923, printed 18923 (difference 6000)
  - sgt1925 dattiers_age communs 5e Région ;  ; Gafsa: Total = col. 2 + Total des jeunes + 20 ans imposables: cells give 79483, printed 73483 (difference -6000)
  - sgt1925 dattiers_age communs Territoires militaires ;  ; Nefzaoua: Total des jeunes = moins d'un an + 1 .. 19 ans: cells give 249311, printed 229311 (difference -20000)
  - sgt1928 dattiers_age degla 5e Région ;  ; Tozeur: Total des jeunes = moins d'un an + 1 .. 19 ans: cells give 98190, printed 98235 (difference 45)
  - sgt1928 dattiers_age degla Totaux: Total des jeunes = moins d'un an + 1 .. 19 ans: cells give 113523, printed 113524 (difference 1)

- Flagged cells: total_mismatch: 2.

  - sgt1925 p.244 Nefzaoua / common / under_1 = 91022 (total_mismatch)
  - sgt1928 p.219 Tozeur / degla / age_18 = 8138 (total_mismatch)

## Image versus OCR

- Read cell by cell on native-resolution crops of the page images (strips of rows, gutter columns on both views of the spread, every failing check re-read zoomed): sgt1922 f212, sgt1922 f213, sgt1922 f212, sgt1922 f213, sgt1923 f702, sgt1923 f703, sgt1923 f702, sgt1923 f703, sgt1924 f1198, sgt1924 f1199, sgt1924 f1198, sgt1924 f1199, sgt1925 f268, sgt1925 f269, sgt1925 f268, sgt1925 f269, sgt1926 f784, sgt1926 f785, sgt1926 f784, sgt1926 f785, sgt1927 f246, sgt1927 f247, sgt1927 f246, sgt1927 f247, sgt1928 f770, sgt1928 f771, sgt1928 f770, sgt1928 f771, sgt1929 f248, sgt1929 f249, sgt1929 f248, sgt1929 f249, sgt1930 f782, sgt1930 f783, sgt1930 f782, sgt1930 f783, sgt1935 f134, sgt1935 f135, sgt1935 f134, sgt1935 f135.
- The Gallica OCR was not used (no cell is flagged `ocr_corrected`).

Survey of the canoun tables in every edition: `finance_canoun_survey.md`.
