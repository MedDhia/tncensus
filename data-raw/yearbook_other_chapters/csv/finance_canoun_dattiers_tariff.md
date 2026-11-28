# Canoun des dattiers. b) Répartition des arbres imposables par catégorie du tarif

*Tax on date palms (canoun des dattiers): taxable trees by caïdat and tariff.*

Source: *Statistique générale de la Tunisie*, chapter *Finances*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views: sgt1922 (`bpt6k9105649x`): p. 190, f214, p. 191, f215; sgt1923 (`bpt6k9105649x`): p. 202, f704, p. 203, f705; sgt1924 (`bpt6k9105649x`): p. 210, f1200, p. 211, f1201; sgt1925 (`bpt6k9105650k`): p. 246, f270, p. 247, f271; sgt1926 (`bpt6k9105650k`): p. 222, f786, p. 223, f787; sgt1927 (`bpt6k91056510`): p. 220, f248, p. 221, f249; sgt1928 (`bpt6k91056510`): p. 220, f772, p. 221, f773; sgt1929 (`bpt6k9105652d`): p. 222, f250, p. 223, f251; sgt1930 (`bpt6k9105652d`): p. 222, f784, p. 223, f785.

Transcriptions: `../transcribed/finance_canoun_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_finance_canoun.py build`.

Rows: 405. Years: 1922, 1923, 1924, 1926, 1927, 1928, 1929, 1930.

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
- `tariff`: tax rate per tree, francs, as a code (`1.40`, `0.05`, ...); `former_tithe_proportional` = anciens pays à dîme, impôt proportionnel au revenu global (olive trees of the former tithe lands, taxed on their income instead of per tree)
- `tariff_fr`: printed column heading (the rate as printed)
- `value`: printed count (» = 0)
- `flag`: empty, or `total_mismatch` (printed value kept; the line TOTAL and the column Totaux, or the other tables of the same edition, identify it as the faulty cell; see the notes), `row_realigned` (figures printed on the line of another caïdat, stored under the caïdat they belong to; see the notes), `derived_from_totals` (digits lost in the gutter fold; value = line TOTAL minus the other cells of the line)

Nombre d'arbres imposés by caïdat at each tariff (francs per tree, printed in the column heads and kept in `tariff_fr`): Dattiers degla and Dattiers communs. The TOTAL column and the Totaux line are checks (TOTAL also = a) 20 ans imposables). The rates change twice: sgt1922-sgt1925 degla 1,40 / 1,80 / 2 / 2,40, communs 0,15 / 0,40 / 0,75 / 1,00 / 1,20; sgt1926-sgt1928 x 1,25 (1,75 ... 3,00; 0,1875 ... 1,50); sgt1929, sgt1930 x 1,75 of the sgt1926 rates (3,012 or 3,0625 ... 5,25; 0,328125 ... 2,625). `tariff` codes the printed rate. Not printed in sgt1935.

Footnotes: none printed under these tables.

## Validation

- Checks against printed totals and identities: 315; passed: 315; failed: 0.

- Flagged cells: none.


## Image versus OCR

- Read cell by cell on native-resolution crops of the page images (strips of rows, gutter columns on both views of the spread, every failing check re-read zoomed): sgt1922 f214, sgt1922 f215, sgt1923 f704, sgt1923 f705, sgt1924 f1200, sgt1924 f1201, sgt1925 f270, sgt1925 f271, sgt1926 f786, sgt1926 f787, sgt1927 f248, sgt1927 f249, sgt1928 f772, sgt1928 f773, sgt1929 f250, sgt1929 f251, sgt1930 f784, sgt1930 f785.
- The Gallica OCR was not used (no cell is flagged `ocr_corrected`).

Survey of the canoun tables in every edition: `finance_canoun_survey.md`.
