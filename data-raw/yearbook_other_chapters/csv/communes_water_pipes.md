# Service des eaux : développement des canalisations

*Water service: length of the water-supply pipe network of each locality, ten years per edition (two years from sgt1936).*

Source: *Statistique générale de la Tunisie*, chapter *Communes*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939 (stored values). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR).

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 38, f62; sgt1923 (`bpt6k9105649x`): p. 42, f544; sgt1924 (`bpt6k9105649x`): p. 42, f1032; sgt1925 (`bpt6k9105650k`): p. 42, f66; sgt1926 (`bpt6k9105650k`): p. 50, f614; sgt1927 (`bpt6k91056510`): p. 50, f78; sgt1928 (`bpt6k91056510`): p. 50, f602; sgt1929 (`bpt6k9105652d`): p. 50, f78; sgt1930 (`bpt6k9105652d`): p. 52, f610; sgt1935 (`bpt6k9105653t`): p. 28, f48, p. 29, f49; sgt1936 (`bpt6k91056547`): p. 21, f32; sgt1939 (`bpt6k9105739w`): p. 22, f28.

Rebuild: `python3 data-raw/yearbook_other_chapters/extract_communes.py build` (transcriptions `../transcribed/communes_water_<edition>.txt`). Per-check output: `communes_validation_services.json`.

Rows: 1084. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1938, 1939.

Printed for overlapping year windows (sgt1922: 1913–1922 … sgt1930: 1921–1930; sgt1935: 1926–1935; sgt1936: 1935–1936; sgt1939: 1938–1939): each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition) and every other printing of the same cell is compared below. 1937 is not printed. The water sales of the same tables, one year per edition, are in `communes_water_sales.csv`.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number of the cell
- `gallica_view`: Gallica view (fNNNN) of the cell
- `year`: year of the length (column heading; see the misprinted headings below)
- `locality`: locality as printed in the edition the value is taken from
- `measure`: `pipe_length_m`
- `measure_fr`: *Développement des canalisations* (printed in two sub-columns *km.* and *m.*)
- `value`: length of the pipe network in **metres** (printed km × 1000 + printed m; decimals of a metre where printed, e.g. 72.819 50 → 72819.50); printed » = 0
- `text_fr`: text printed instead of a number
- `flag`: empty; `reprint_corrected` (value taken from another printing of the same year, see below); `not_applicable` (text instead of a number, value NA)

**Editions and layout.** *Service des eaux — Développement des canalisations ; vente d'eau*: sgt1922 p. 38 (view 62), sgt1923 p. 42 (544), sgt1924 p. 42 (1032), sgt1925 p. 42 (66), sgt1926 p. 50 (614), sgt1927 p. 50 (78), sgt1928 p. 50 (602); headed *Service des eaux (Régies d'État)* in sgt1929 p. 50 (78), sgt1930 p. 52 (610), sgt1935 pp. 28–29 (views 48–49, a two-page spread), sgt1936 p. 21 (32) and sgt1939 p. 22 (28). The locality list grows from 7 (sgt1922–sgt1924) to 51 (sgt1936, sgt1939). sgt1929 and later list only the state-run (*régie*) services: Nabeul, Ferryville, Mateur, Tozeur, Le Kef, Béja, Tabarka, Kairouan, Téboursouk, Medjez-el-Bab and Gabès are dropped in sgt1929, and Béja, Tabarka, Gabès … return in sgt1935 with » for the years before they became régies. Their earlier lengths therefore come from the last edition that printed them (e.g. Nabeul 1928 from sgt1928).
**Misprinted year headings.** sgt1923 and sgt1924 head the 1923 column "1913"; sgt1925 heads 1923 "1913" and 1925 "1915". The columns are assigned by position (they continue the sequence, and the figures match the 1923/1925 columns of the later editions). sgt1927 heads its sales column "Recettes en 1926" but its amounts are new (see `communes_water_sales.md`).
**What the lengths are.** Up to 1926 every printing gives cumulative network lengths. sgt1927, sgt1928 and sgt1929 print small figures for 1927–1929 for the large towns (Bizerte 345 m, Sousse 213 m, Sfax 300 m in 1927; Bizerte 337 m, Sousse 225 m in 1928), apparently the extensions of the year, and » where nothing was added, while the other localities keep cumulative figures (Hammamet 9.017). sgt1930 and sgt1935 reprint 1927–1929 as cumulative lengths (Bizerte 12.725 / 13.062 / 19.370). The stored values are those of the latest printing (cumulative); the earlier printings are listed as differences. The Sousse series is printed as *Sousse* (to sgt1929), *Sousse-Monastir et villages* (sgt1930) and *Sousse, Kairouan et villages du Sahel* (sgt1935–sgt1939): the overlapping years agree (222.878 … 224.360), so the three labels are matched as one series; from 1927 the figure drops to 183.837 (a redefined network). Other renamings matched: *M'Rira Fouchai* (the label is cut by the column rule) = *M'Rira Fouchana (Mohamédia)*; *Dar Chabane* = *Dar Chabane El-Fehri*; *Mejez el Bab* = *Medjez-el-Bab*; *Gaffour* = *Gafour*; accents ignored (Tébourba, Fériana, Kélibia, Sbeïtla …).
**Particular cells.** Tunis 1924 is printed "281" with the metres blank in all six printings (sgt1924–sgt1930): stored as 281000. sgt1925 prints Tunis 1925 "571 107" (all later printings 287 107) and Ferryville 1925 "9 104 50" (later 9 104). sgt1929 Dar Chabane 1926 is blank (not stored; sgt1935 »). sgt1935: the 1929 column runs into the binding of the spread (views 48–49) and only its first digits are legible; its 17 non-zero cells are stored from sgt1930 (`reprint_corrected`), each agreeing with the legible digits (Tunis "319 8…" = 319.826 …). sgt1936, 1935: M'Rira-Fouchana prints *constitué en Syndicat* (formed into a syndicate; NA, `not_applicable`); sgt1936 prints the 1935 lengths of Armand Colin and Eddekhila one line low (Armand Colin 0.920 = Aïn-el-Asker's figure repeated, Eddekhila 1.303 = Armand Colin's): these two are stored from sgt1935 (1.303 and 2.274, `reprint_corrected`). sgt1936 also prints, for 1935, Thala 2.507 (sgt1935: 8.979,78), Fériana 3.994 (3.557,20), Sbeïtla 2.200 (»), Gafsa 5.001 (»), Sidi-bou-Ali 2.032 (2.052), and Souk-el-Arba / Souk-el-Khemis 12.862 / 23.187 (sgt1935: 23.187 / 12.862, which itself swaps the two towns' 1932–1933 figures); these are kept from sgt1936 as rule 4 requires (no printing can be shown wrong). sgt1939 Sfax prints 1938 "843 40" and 1939 "1.002 30" (sgt1936: 225.741 km): stored as printed (843.40 m and 1002.30 m).
**Image versus OCR.** Every cell of every edition was read on native-resolution crops of the page images (whole table at 0.45–0.6 scale, then the label column stitched to the value columns at 0.6–1.0 scale, the sgt1935 binding strip of both views at 0.75, and single cells at 1.5–2×). Gallica's OCR was used only as a draft for sgt1922–sgt1924 (where it agrees with the images); it is scrambled for sgt1925–sgt1930 and was not used there. No value rests on the OCR alone.

## Validation

- No total is printed in any of these tables (no column or row totals), so no sum check is possible; the validation is the comparison of the overlapping printings.
- Overlapping printings (rule 4): 1487 cell comparisons with the stored (latest) printing; 105 differences (a partly legible sgt1935 1929 cell counts as equal when its legible digits match):

| year | locality (latest) | other edition | printed there | latest edition | printed there |
|---|---|---|---|---|---|
| 1920 | Bizerte | sgt1922 | 15.251 | sgt1929 | 11.251 |
| 1921 | Bizerte | sgt1922 | 15.347 | sgt1930 | 11.347 |
| 1922 | Bizerte | sgt1922 | 15.514 | sgt1930 | 11.514 |
| 1925 | Tunis | sgt1925 | 571.107 | sgt1930 | 287.107 |
| 1925 | Ferryville | sgt1925 | 9.104,50 | sgt1928 | 9.104 |
| 1925 | Sbeitla | sgt1925 | 3.037 | sgt1930 | » |
| 1925 | Sbeitla | sgt1926 | 3.037 | sgt1930 | » |
| 1925 | Sbeitla | sgt1927 | 3.037 | sgt1930 | » |
| 1925 | Sbeitla | sgt1928 | 3.037 | sgt1930 | » |
| 1925 | Sbeitla | sgt1929 | 3.037 | sgt1930 | » |
| 1926 | Sbeitla | sgt1926 | 4.230 | sgt1935 | » |
| 1926 | Sbeitla | sgt1927 | 4.230 | sgt1935 | » |
| 1926 | Sbeitla | sgt1928 | 4.230 | sgt1935 | » |
| 1926 | Sbeitla | sgt1929 | 4.230 | sgt1935 | » |
| 1926 | Béja | sgt1926 | 3.000 | sgt1935 | » |
| 1926 | Béja | sgt1927 | 3.000 | sgt1935 | » |
| 1926 | Béja | sgt1928 | 3.000 | sgt1935 | » |
| 1926 | Tabarka | sgt1926 | 7.000 | sgt1935 | » |
| 1926 | Tabarka | sgt1927 | 7.000 | sgt1935 | » |
| 1926 | Tabarka | sgt1928 | 7.000 | sgt1935 | » |
| 1927 | Bizerte | sgt1927 | 0.345 | sgt1935 | 12.725 |
| 1927 | Bizerte | sgt1928 | 0.345 | sgt1935 | 12.725 |
| 1927 | Bizerte | sgt1929 | 0.345 | sgt1935 | 12.725 |
| 1927 | Sousse, Kairouan et villages du Sahel | sgt1927 | 0.213 | sgt1935 | 183.837 |
| 1927 | Sousse, Kairouan et villages du Sahel | sgt1928 | 0.213 | sgt1935 | 183.837 |
| 1927 | Sousse, Kairouan et villages du Sahel | sgt1929 | 0.213 | sgt1935 | 183.837 |
| 1927 | Mahdia | sgt1927 | » | sgt1935 | 11.220 |
| 1927 | Mahdia | sgt1928 | » | sgt1935 | 11.220 |
| 1927 | Mahdia | sgt1929 | » | sgt1935 | 11.220 |
| 1927 | Thala | sgt1927 | » | sgt1935 | 2.674 |
| 1927 | Thala | sgt1928 | » | sgt1935 | 2.674 |
| 1927 | Thala | sgt1929 | » | sgt1935 | 2.674 |
| 1927 | Sfax | sgt1927 | 0.300 | sgt1935 | 211.910 |
| 1927 | Sfax | sgt1928 | 0.300 | sgt1935 | 211.910 |
| 1927 | Sfax | sgt1929 | 0.300 | sgt1935 | 211.910 |
| 1927 | Tebourba | sgt1927 | » | sgt1935 | 1.826 |
| 1927 | Tebourba | sgt1928 | » | sgt1935 | 1.826 |
| 1927 | Tebourba | sgt1929 | » | sgt1935 | 1.826 |
| 1927 | Enfidaville | sgt1927 | » | sgt1935 | 13.610 |
| 1927 | Enfidaville | sgt1928 | » | sgt1935 | 13.610 |
| 1927 | Enfidaville | sgt1929 | » | sgt1935 | 13.610 |
| 1927 | Pichon | sgt1927 | » | sgt1935 | 1.116 |
| 1927 | Pichon | sgt1928 | » | sgt1935 | 1.116 |
| 1927 | Pichon | sgt1929 | » | sgt1935 | 1.116 |
| 1927 | Feriana | sgt1927 | » | sgt1935 | 3.414 |
| 1927 | Feriana | sgt1928 | » | sgt1935 | 3.414 |
| 1927 | Feriana | sgt1929 | » | sgt1935 | 3.414 |
| 1927 | M'Rira Fouchana (Mohamédia) | sgt1927 | » | sgt1935 | 10.060 |
| 1927 | M'Rira Fouchana (Mohamédia) | sgt1928 | » | sgt1935 | 10.060 |
| 1927 | M'Rira Fouchana (Mohamédia) | sgt1929 | » | sgt1935 | 10.060 |
| 1927 | Gafsa | sgt1927 | » | sgt1935 | 3.642 |
| 1927 | Gafsa | sgt1928 | » | sgt1935 | 3.642 |
| 1927 | Gafsa | sgt1929 | » | sgt1935 | 3.642 |
| 1927 | Béja | sgt1927 | 0.611 | sgt1935 | » |
| 1927 | Béja | sgt1928 | 0.611 | sgt1935 | » |
| 1928 | Bizerte | sgt1928 | 0.337 | sgt1935 | 13.062 |
| 1928 | Bizerte | sgt1929 | 0.337 | sgt1935 | 13.062 |
| 1928 | Sousse, Kairouan et villages du Sahel | sgt1928 | 0.225 | sgt1935 | 183.837 |
| 1928 | Sousse, Kairouan et villages du Sahel | sgt1929 | 0.225 | sgt1935 | 183.837 |
| 1928 | Thala | sgt1928 | » | sgt1935 | 2.674 |
| 1928 | Thala | sgt1929 | » | sgt1935 | 2.674 |
| 1928 | Sfax | sgt1928 | » | sgt1935 | 211.910 |
| 1928 | Sfax | sgt1929 | » | sgt1935 | 211.910 |
| 1928 | Tebourba | sgt1928 | 1.738 | sgt1935 | 1.826 |
| 1928 | Tebourba | sgt1929 | 1.738 | sgt1935 | 1.826 |
| 1928 | Enfidaville | sgt1928 | 1.210 | sgt1935 | 14.820 |
| 1928 | Enfidaville | sgt1929 | 1.210 | sgt1935 | 14.820 |
| 1928 | Pichon | sgt1928 | 0.532 | sgt1935 | 1.648 |
| 1928 | Pichon | sgt1929 | 0.532 | sgt1935 | 1.648 |
| 1928 | Feriana | sgt1928 | » | sgt1935 | 3.414 |
| 1928 | Feriana | sgt1929 | » | sgt1935 | 3.414 |
| 1928 | M'Rira Fouchana (Mohamédia) | sgt1928 | » | sgt1935 | 10.060 |
| 1928 | M'Rira Fouchana (Mohamédia) | sgt1929 | » | sgt1935 | 10.060 |
| 1928 | Hammamet | sgt1928 | 8.593 | sgt1935 | 9.017 |
| 1928 | Hammamet | sgt1929 | 8.593 | sgt1935 | 9.017 |
| 1928 | Kelibia | sgt1928 | 3.714 | sgt1935 | 2.850 |
| 1928 | Kelibia | sgt1929 | 3.714 | sgt1935 | 2.850 |
| 1928 | Gafsa | sgt1928 | » | sgt1935 | 3.642 |
| 1928 | Gafsa | sgt1929 | » | sgt1935 | 3.642 |
| 1928 | Béja | sgt1928 | 0.360 | sgt1935 | » |
| 1928 | Le Sers | sgt1928 | 0.319 | sgt1935 | » |
| 1928 | Le Sers | sgt1929 | 0.319 | sgt1935 | » |
| 1929 | Tunis | sgt1929 | 302.511 | sgt1935 | p:319.8 |
| 1929 | Sousse, Kairouan et villages du Sahel | sgt1929 | 0.642 | sgt1935 | p:183.8 |
| 1929 | Mahdia | sgt1929 | » | sgt1935 | p:11.2 |
| 1929 | Thala | sgt1929 | 0.070 | sgt1935 | p:2.7 |
| 1929 | Sfax | sgt1929 | 1.736 | sgt1935 | p:213.6 |
| 1929 | Enfidaville | sgt1929 | » | sgt1935 | p:14.8 |
| 1929 | Pichon | sgt1929 | » | sgt1935 | p:1.6 |
| 1929 | Feriana | sgt1929 | » | sgt1935 | p:3.4 |
| 1929 | Sbeitla | sgt1929 | 0.060 | sgt1935 | » |
| 1929 | Gafsa | sgt1929 | » | sgt1935 | p:3.6 |
| 1929 | Dar Chabane El-Fehri | sgt1929 | 5.044 | sgt1935 | p:4.8 |
| 1929 | Aguareb | sgt1929 | » | sgt1935 | p:9.0 |
| 1929 | Djebeniana | sgt1929 | » | sgt1935 | p:1.7 |
| 1935 | Thala | sgt1935 | 8.979,78 | sgt1936 | 2.507 |
| 1935 | Fériana | sgt1935 | 3.557,20 | sgt1936 | 3.994 |
| 1935 | M'Rira-Fouchana (Mohamédia) | sgt1935 | » | sgt1936 | T:constitué_en_Syndicat |
| 1935 | Sbeïtla | sgt1935 | » | sgt1936 | 2.200 |
| 1935 | Gafsa | sgt1935 | » | sgt1936 | 5.001 |
| 1935 | Armand Colin | sgt1935 | 1.303 | sgt1936 | 0.920 |
| 1935 | Eddekhila | sgt1935 | 2.274 | sgt1936 | 1.303 |
| 1935 | Sidi-bou-Ali | sgt1935 | 2.052 | sgt1936 | 2.032 |
| 1935 | Souk-el-Arba | sgt1935 | 23.187 | sgt1936 | 12.862 |
| 1935 | Souk-el-Khemis | sgt1935 | 12.862 | sgt1936 | 23.187 |

- Flagged cells: 20.
  - 1929 Tunis: 319826 (reprint_corrected; stored from sgt1930, latest printing sgt1935 prints `p:319.8`)
  - 1929 Bizerte: 19370 (reprint_corrected; stored from sgt1930, latest printing sgt1935 prints `p:19.3`)
  - 1929 Sousse-Monastir et villages: 183837 (reprint_corrected; stored from sgt1930, latest printing sgt1935 prints `p:183.8`)
  - 1929 Mahdia: 11245 (reprint_corrected; stored from sgt1930, latest printing sgt1935 prints `p:11.2`)
  - 1929 Thala: 2717 (reprint_corrected; stored from sgt1930, latest printing sgt1935 prints `p:2.7`)
  - 1929 Sfax: 213646 (reprint_corrected; stored from sgt1930, latest printing sgt1935 prints `p:213.6`)
  - 1929 Tebourba: 1826 (reprint_corrected; stored from sgt1930, latest printing sgt1935 prints `p:1.8`)
  - 1929 Enfidaville: 14820 (reprint_corrected; stored from sgt1930, latest printing sgt1935 prints `p:14.8`)
  - 1929 Pichon: 1648 (reprint_corrected; stored from sgt1930, latest printing sgt1935 prints `p:1.6`)
  - 1929 Feriana: 3414 (reprint_corrected; stored from sgt1930, latest printing sgt1935 prints `p:3.4`)
  - 1929 M'Rira Fouchai (Mohamédia): 15600 (reprint_corrected; stored from sgt1930, latest printing sgt1935 prints `p:15.6`)
  - 1929 Hammamet: 9017 (reprint_corrected; stored from sgt1930, latest printing sgt1935 prints `p:9.0`)
  - 1929 Kelibia: 2850 (reprint_corrected; stored from sgt1930, latest printing sgt1935 prints `p:2.8`)
  - 1929 Gafsa: 3642 (reprint_corrected; stored from sgt1930, latest printing sgt1935 prints `p:3.6`)
  - 1929 Dar Chabane: 4873 (reprint_corrected; stored from sgt1930, latest printing sgt1935 prints `p:4.8`)
  - 1929 Aguareb: 9000 (reprint_corrected; stored from sgt1930, latest printing sgt1935 prints `p:9.0`)
  - 1929 Djebeniana: 1700 (reprint_corrected; stored from sgt1930, latest printing sgt1935 prints `p:1.7`)
  - 1935 M'Rira-Fouchana (Mohamédia): NA (not_applicable; printed "constitué en Syndicat")
  - 1935 Armand Colin: 1303 (reprint_corrected; stored from sgt1935, latest printing sgt1936 prints `0.920`)
  - 1935 Eddekhila: 2274 (reprint_corrected; stored from sgt1935, latest printing sgt1936 prints `1.303`)
