# Canoun des oliviers. a) Relevé par caïdat du nombre d'arbres d'après leur âge

*Tax on olive trees (canoun des oliviers): trees by caïdat and age.*

Source: *Statistique générale de la Tunisie*, chapter *Finances*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views: sgt1922 (`bpt6k9105649x`): p. 192, f216, p. 193, f217; sgt1923 (`bpt6k9105649x`): p. 204, f706, p. 205, f707; sgt1924 (`bpt6k9105649x`): p. 212, f1202, p. 213, f1203; sgt1925 (`bpt6k9105650k`): p. 248, f272, p. 249, f273; sgt1926 (`bpt6k9105650k`): p. 224, f788, p. 225, f789; sgt1927 (`bpt6k91056510`): p. 222, f250, p. 223, f251; sgt1928 (`bpt6k91056510`): p. 222, f774, p. 223, f775; sgt1929 (`bpt6k9105652d`): p. 224, f252, p. 225, f253; sgt1930 (`bpt6k9105652d`): p. 224, f786, p. 225, f787; sgt1935 (`bpt6k9105653t`): p. 116, f136, p. 117, f137.

Transcriptions: `../transcribed/finance_canoun_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_finance_canoun.py build`.

Rows: 7058. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935.

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
- `age_class`: `male` (mâles, date palms), `wild` (arbres sauvages, olive trees), `under_1` (moins d'un an), `age_01` .. `age_19` (1 an .. 19 ans: young trees, not taxed), `taxable_20_plus` (20 ans imposables)
- `age_class_fr`: printed column heading
- `value`: printed count (» = 0)
- `flag`: empty, or `total_mismatch` (printed value kept; the line TOTAL and the column Totaux, or the other tables of the same edition, identify it as the faulty cell; see the notes), `row_realigned` (figures printed on the line of another caïdat, stored under the caïdat they belong to; see the notes), `derived_from_totals` (digits lost in the gutter fold; value = line TOTAL minus the other cells of the line)

By caïdat (sgt1922-sgt1924, 30 lines; from sgt1925 by région, chef-lieu de région, contrôle civil and caïdat, 33 lines): Arbres sauvages (wild trees, not taxed), Moins d'un an, 1 an .. 19 ans, Total des jeunes, 20 ans imposables, Total. Stored: every column except the two totals; the Totaux line is a check. sgt1927-sgt1930 print no Moins d'un an column (no `under_1` rows for those editions). New lines: Aïn-Draham and Matmata from sgt1929; in sgt1935 Thala and Sbeïtla replace Fraichiches and Madjeurs. The two lines under the Cap-Bon brace are stored as Cap-Bon - Nabeul and Cap-Bon - Soliman.

Footnotes: none printed under these tables.

## Validation

- Checks against printed totals and identities: 906; passed: 852; failed: 54.

Every failure was re-read on zoomed native-resolution crops; printed values are kept. Explanation, by edition:

  - sgt1922: Totaux 20 ans imposables and Total printed 1 under the sum of the lines (b) Totaux prints 9.094.192 = the lines); misprint of the check line.
  - sgt1923: Totaux arbres sauvages printed 822.887 for 722.887 (the lines; the Total of the Totaux line 15.260.037 is consistent with neither), Total des jeunes 5.493.618 for 5.493.648; Bizerte Total 467.071 for 467.171 (check column). Cap-Bon 15 ans 3.554 printed on the Nabeul line, stored on the Soliman line (row_realigned, see the transcription).
  - sgt1925: Printed errors, each figure confirmed zoomed (flagged total_mismatch where the line Total and the column Totaux both point to the cell): Téboursouk 2 ans 3.864 (2.864); Mateur 18 ans 1.712 (2.712) and Souk-el-Khemis 18 ans 843 (813); Zaghouan 14 ans 238 (338); Souassi 19 ans 26.983 (26.985), Djebéniana 19 ans 2.055 (2.005); Djebéniana sauvages 10.095 (19.095), Tataouine sauvages 1.967 (1.968); Cap-Bon - Nabeul 20 ans imposables 337.466 (377.466, = b) and c)). La Skhira Total des jeunes 597.729 for 497.729 (check column). The two Cap-Bon lines of a) carry each other's figures (row_realigned).
  - sgt1926: Ouerghema 2 ans printed 194.685 (zoomed; Total des jeunes, the column Totaux and sgt1925 (1 an 191.685) require 191.685; flagged). Totaux 9 ans 766.637 for the lines' 766.537 and Totaux Total des jeunes 5.714.272 against its columns' 5.714.372 (check line).
  - sgt1927: No moins d'un an column in this printing. Monastir 1 an printed 14.438 (zoomed; Total des jeunes and the column Totaux require 14.488, as printed in sgt1926) and Djerid 20 ans imposables 21.411 (the line Total and the column Totaux require 21.481): flagged. Totaux 10 ans 766.637 and Total des jeunes 5.146.071 repeat the sgt1926 Totaux misprints (check line).
  - sgt1929: Cap-Bon - Nabeul 12 ans printed 83.231 (Total des jeunes and the column Totaux require 33.231): flagged. Mahdia Total des jeunes 558.347 for 588.347 (check column); Totaux 10 ans 97.756 (lines 97.736) and Total des jeunes 5.160.146 (lines 5.130.146) are check-line misprints.
  - sgt1930: Zaghouan 4 ans printed 1.202 (Total des jeunes and the column Totaux require 1.204, as in sgt1929) and Tataouine 15 ans 8.265 (8.295): flagged. Totaux 8 ans 1.242.540 (lines 1.212.510), 14 ans and 18 ans 300 over their lines, and Total des jeunes 5.174.785 against its columns: check-line misprints.
  - sgt1935: Mateur 13 ans printed 18.380 (Total des jeunes and the column Totaux require 18.388): flagged. Zaghouan Total 128.544 for 128.554 and the Totaux Total 16.801.750 (lines 16.801.740) are check figures. Totaux 7 ans hidden in the fold (not checked).

Failed checks:

  - sgt1922 oliviers_age Totaux imp: sum of the lines (f217): cells give 9094192, printed 9094191 (difference -1)
  - sgt1922 oliviers_age Totaux tot: sum of the lines (f217): cells give 15109296, printed 15109295 (difference -1)
  - sgt1923 oliviers_age Totaux sv: sum of the lines (f706): cells give 722887, printed 822887 (difference 100000)
  - sgt1923 oliviers_age Totaux tj: sum of the lines (f707): cells give 5493648, printed 5493618 (difference -30)
  - sgt1923 oliviers_age Totaux tot: sum of the lines (f707): cells give 15259937, printed 15260037 (difference 100)
  - sgt1925 oliviers_age Totaux sv: sum of the lines (f272): cells give 704647, printed 713648 (difference 9001)
  - sgt1925 oliviers_age Totaux a2: sum of the lines (f272): cells give 204952, printed 203952 (difference -1000)
  - sgt1925 oliviers_age Totaux a14: sum of the lines (f273): cells give 292916, printed 293016 (difference 100)
  - sgt1925 oliviers_age Totaux a18: sum of the lines (f273): cells give 567050, printed 568020 (difference 970)
  - sgt1925 oliviers_age Totaux a19: sum of the lines (f273): cells give 224415, printed 224367 (difference -48)
  - sgt1925 oliviers_age Totaux tj: sum of the lines (f273): cells give 5929764, printed 5829764 (difference -100000)
  - sgt1925 oliviers_age Totaux imp: sum of the lines (f273): cells give 9063897, printed 9103897 (difference 40000)
  - sgt1926 oliviers_age Totaux a2: sum of the lines (f788): cells give 203042, printed 200042 (difference -3000)
  - sgt1926 oliviers_age Totaux a9: sum of the lines (f789): cells give 766537, printed 766637 (difference 100)
  - sgt1927 oliviers_age Totaux a1: sum of the lines (f250): cells give 136405, printed 136455 (difference 50)
  - sgt1927 oliviers_age Totaux a10: sum of the lines (f251): cells give 766537, printed 766637 (difference 100)
  - sgt1927 oliviers_age Totaux imp: sum of the lines (f251): cells give 9909386, printed 9909456 (difference 70)
  - sgt1929 oliviers_age Totaux a10: sum of the lines (f253): cells give 97736, printed 97756 (difference 20)
  - sgt1929 oliviers_age Totaux a12: sum of the lines (f253): cells give 652927, printed 602927 (difference -50000)
  - sgt1929 oliviers_age Totaux tj: sum of the lines (f253): cells give 5130146, printed 5160146 (difference 30000)
  - sgt1930 oliviers_age Totaux a4: sum of the lines (f786): cells give 141752, printed 141754 (difference 2)
  - sgt1930 oliviers_age Totaux a8: sum of the lines (f787): cells give 1212510, printed 1242540 (difference 30030)
  - sgt1930 oliviers_age Totaux a14: sum of the lines (f787): cells give 452165, printed 452465 (difference 300)
  - sgt1930 oliviers_age Totaux a16: sum of the lines (f787): cells give 90441, printed 90471 (difference 30)
  - sgt1930 oliviers_age Totaux a18: sum of the lines (f787): cells give 622156, printed 622456 (difference 300)
  - sgt1935 oliviers_age Totaux a13: sum of the lines (f137): cells give 1056829, printed 1056837 (difference 8)
  - sgt1935 oliviers_age Totaux tot: sum of the lines (f137): cells give 16801740, printed 16801750 (difference 10)
  - sgt1923 oliviers_age Bizerte: Total = col. 2 + Total des jeunes + 20 ans imposables: cells give 467171, printed 467071 (difference -100)
  - sgt1923 oliviers_age Totaux: Total des jeunes = moins d'un an + 1 .. 19 ans: cells give 5493648, printed 5493618 (difference -30)
  - sgt1923 oliviers_age Totaux: Total = col. 2 + Total des jeunes + 20 ans imposables: cells give 15360007, printed 15260037 (difference -99970)
  - sgt1925 oliviers_age 1re Région (Bizerte) ; Bizerte ; Mateur: Total des jeunes = moins d'un an + 1 .. 19 ans: cells give 18691, printed 19691 (difference 1000)
  - sgt1925 oliviers_age 1re Région (Bizerte) ; Souk-el-Arba ; Souk-el-Khemis: Total des jeunes = moins d'un an + 1 .. 19 ans: cells give 3604, printed 3574 (difference -30)
  - sgt1925 oliviers_age 2me Région (Tunis) ; Zaghouan ; Zaghouan: Total des jeunes = moins d'un an + 1 .. 19 ans: cells give 8211, printed 8311 (difference 100)
  - sgt1925 oliviers_age 2me Région (Tunis) ; Grombalia ; Cap-Bon - Nabeul: Total = col. 2 + Total des jeunes + 20 ans imposables: cells give 516206, printed 556206 (difference 40000)
  - sgt1925 oliviers_age 3me Région (Le Kef) ; Téboursouk ; Téboursouk: Total des jeunes = moins d'un an + 1 .. 19 ans: cells give 10404, printed 9404 (difference -1000)
  - sgt1925 oliviers_age 4me Région (Sousse) ; Sousse ; Souassi: Total des jeunes = moins d'un an + 1 .. 19 ans: cells give 276964, printed 276966 (difference 2)
  - sgt1925 oliviers_age 5me Région (Sfax) ; Sfax ; La Skhira: Total des jeunes = moins d'un an + 1 .. 19 ans: cells give 497729, printed 597729 (difference 100000)
  - sgt1925 oliviers_age 5me Région (Sfax) ; Sfax ; La Skhira: Total = col. 2 + Total des jeunes + 20 ans imposables: cells give 678202, printed 578202 (difference -100000)
  - sgt1925 oliviers_age 5me Région (Sfax) ; Sfax ; Djebéniana: Total des jeunes = moins d'un an + 1 .. 19 ans: cells give 642558, printed 642508 (difference -50)
  - sgt1925 oliviers_age 5me Région (Sfax) ; Sfax ; Djebéniana: Total = col. 2 + Total des jeunes + 20 ans imposables: cells give 1129564, printed 1138564 (difference 9000)
  - sgt1925 oliviers_age Territoires militaires du Sud ;  ; Tataouine: Total = col. 2 + Total des jeunes + 20 ans imposables: cells give 74695, printed 74696 (difference 1)
  - sgt1926 oliviers_age Territoires militaires du Sud ;  ; Ouerghema: Total des jeunes = moins d'un an + 1 .. 19 ans: cells give 410157, printed 407157 (difference -3000)
  - sgt1926 oliviers_age Totaux: Total des jeunes = moins d'un an + 1 .. 19 ans: cells give 5714372, printed 5714272 (difference -100)
  - sgt1927 oliviers_age 4me Région (Sousse) ; Sousse ; Monastir: Total des jeunes = moins d'un an + 1 .. 19 ans: cells give 610520, printed 610570 (difference 50)
  - sgt1927 oliviers_age 5me Région (Sfax) ; Tozeur ; Djerid: Total = col. 2 + Total des jeunes + 20 ans imposables: cells give 36011, printed 36081 (difference 70)
  - sgt1927 oliviers_age Totaux: Total des jeunes = moins d'un an + 1 .. 19 ans: cells give 5146171, printed 5146071 (difference -100)
  - sgt1929 oliviers_age 2me Région (Tunis) ; Grombalia ; Cap-Bon - Nabeul: Total des jeunes = moins d'un an + 1 .. 19 ans: cells give 193376, printed 143376 (difference -50000)
  - sgt1929 oliviers_age 4me Région (Sousse) ; Sousse ; Mahdia: Total des jeunes = moins d'un an + 1 .. 19 ans: cells give 588347, printed 558347 (difference -30000)
  - sgt1929 oliviers_age 4me Région (Sousse) ; Sousse ; Mahdia: Total = col. 2 + Total des jeunes + 20 ans imposables: cells give 1588529, printed 1618529 (difference 30000)
  - sgt1930 oliviers_age 2me Région (Tunis) ; Zaghouan ; Zaghouan: Total des jeunes = moins d'un an + 1 .. 19 ans: cells give 11040, printed 11042 (difference 2)
  - sgt1930 oliviers_age Territoires militaires du Sud ;  ; Tataouine: Total des jeunes = moins d'un an + 1 .. 19 ans: cells give 26688, printed 26718 (difference 30)
  - sgt1930 oliviers_age Totaux: Total des jeunes = moins d'un an + 1 .. 19 ans: cells give 5205415, printed 5174785 (difference -30630)
  - sgt1935 oliviers_age 1re Région (Bizerte) ; Bizerte ; Mateur: Total des jeunes = moins d'un an + 1 .. 19 ans: cells give 53540, printed 53548 (difference 8)
  - sgt1935 oliviers_age 2me Région (Tunis) ; Zaghouan ; Zaghouan: Total = col. 2 + Total des jeunes + 20 ans imposables: cells give 128554, printed 128544 (difference -10)

- Flagged cells: row_realigned: 45, total_mismatch: 16.

  - sgt1923 p.205 Cap-Bon - Soliman / age_15 = 3554 (row_realigned)
  - sgt1923 p.205 Cap-Bon - Nabeul / age_15 = 0 (row_realigned)
  - sgt1925 p.249 Mateur / age_18 = 1712 (total_mismatch)
  - sgt1925 p.249 Souk-el-Khemis / age_18 = 843 (total_mismatch)
  - sgt1925 p.249 Zaghouan / age_14 = 238 (total_mismatch)
  - sgt1925 p.248 Cap-Bon - Soliman / wild = 72898 (row_realigned)
  - sgt1925 p.248 Cap-Bon - Soliman / under_1 = 0 (row_realigned)
  - sgt1925 p.248 Cap-Bon - Soliman / age_01 = 0 (row_realigned)
  - sgt1925 p.248 Cap-Bon - Soliman / age_02 = 15086 (row_realigned)
  - sgt1925 p.248 Cap-Bon - Soliman / age_03 = 0 (row_realigned)
  - sgt1925 p.248 Cap-Bon - Soliman / age_04 = 0 (row_realigned)
  - sgt1925 p.248 Cap-Bon - Soliman / age_05 = 0 (row_realigned)
  - sgt1925 p.248 Cap-Bon - Soliman / age_06 = 0 (row_realigned)
  - sgt1925 p.248 Cap-Bon - Soliman / age_07 = 11187 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Soliman / age_08 = 0 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Soliman / age_09 = 0 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Soliman / age_10 = 0 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Soliman / age_11 = 0 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Soliman / age_12 = 8367 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Soliman / age_13 = 0 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Soliman / age_14 = 0 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Soliman / age_15 = 0 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Soliman / age_16 = 0 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Soliman / age_17 = 3429 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Soliman / age_18 = 0 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Soliman / age_19 = 0 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Soliman / taxable_20_plus = 1157941 (row_realigned)
  - sgt1925 p.248 Cap-Bon - Nabeul / wild = 8477 (row_realigned)
  - sgt1925 p.248 Cap-Bon - Nabeul / under_1 = 0 (row_realigned)
  - sgt1925 p.248 Cap-Bon - Nabeul / age_01 = 0 (row_realigned)
  - sgt1925 p.248 Cap-Bon - Nabeul / age_02 = 276 (row_realigned)
  - sgt1925 p.248 Cap-Bon - Nabeul / age_03 = 86838 (row_realigned)
  - sgt1925 p.248 Cap-Bon - Nabeul / age_04 = 0 (row_realigned)
  - sgt1925 p.248 Cap-Bon - Nabeul / age_05 = 0 (row_realigned)
  - sgt1925 p.248 Cap-Bon - Nabeul / age_06 = 0 (row_realigned)
  - sgt1925 p.248 Cap-Bon - Nabeul / age_07 = 106 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Nabeul / age_08 = 33551 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Nabeul / age_09 = 0 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Nabeul / age_10 = 0 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Nabeul / age_11 = 0 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Nabeul / age_12 = 145 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Nabeul / age_13 = 22732 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Nabeul / age_14 = 0 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Nabeul / age_15 = 0 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Nabeul / age_16 = 0 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Nabeul / age_17 = 125 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Nabeul / age_18 = 26490 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Nabeul / age_19 = 0 (row_realigned)
  - sgt1925 p.249 Cap-Bon - Nabeul / taxable_20_plus = 337466 (total_mismatch)
  - sgt1925 p.248 Téboursouk / age_02 = 3864 (total_mismatch)
  - sgt1925 p.249 Souassi / age_19 = 26983 (total_mismatch)
  - sgt1925 p.248 Djebéniana / wild = 10095 (total_mismatch)
  - sgt1925 p.249 Djebéniana / age_19 = 2055 (total_mismatch)
  - sgt1925 p.248 Tataouine / wild = 1967 (total_mismatch)
  - sgt1926 p.224 Ouerghema / age_02 = 194685 (total_mismatch)
  - sgt1927 p.222 Monastir / age_01 = 14438 (total_mismatch)
  - sgt1927 p.223 Djerid / taxable_20_plus = 21411 (total_mismatch)
  - sgt1929 p.225 Cap-Bon - Nabeul / age_12 = 83231 (total_mismatch)
  - sgt1930 p.224 Zaghouan / age_04 = 1202 (total_mismatch)
  - sgt1930 p.225 Tataouine / age_15 = 0 (total_mismatch)
  - sgt1935 p.117 Mateur / age_13 = 18380 (total_mismatch)

## Image versus OCR

- Read cell by cell on native-resolution crops of the page images (strips of rows, gutter columns on both views of the spread, every failing check re-read zoomed): sgt1922 f216, sgt1922 f217, sgt1923 f706, sgt1923 f707, sgt1924 f1202, sgt1924 f1203, sgt1925 f272, sgt1925 f273, sgt1926 f788, sgt1926 f789, sgt1927 f250, sgt1927 f251, sgt1928 f774, sgt1928 f775, sgt1929 f252, sgt1929 f253, sgt1930 f786, sgt1930 f787, sgt1935 f136, sgt1935 f137.
- The Gallica OCR was not used (no cell is flagged `ocr_corrected`).

Survey of the canoun tables in every edition: `finance_canoun_survey.md`.
