# ind1931_t3_cheikhat_nationality

**Tableau III. — État de la population indigène par Cheikhats**
(Table III. Indigenous population by cheikhat.)

Source: *Dénombrement de la population civile indigène (musulmane et israélite)
en Tunisie au 22 mars 1931*, Régence de Tunis, Direction générale de
l'Intérieur (Tunis: Impr. J. Aloccio, 1932). Gallica ark `bpt6k994559s`
(Source gallica.bnf.fr / Bibliothèque nationale de France, NoC-NC). Printed
pages 12–97, Gallica views 11–53 (two-page spreads: view *v* holds pages
2*v*−10 and 2*v*−9).

Built by `data-raw/colonial_census/extract_ind1931_t3.py`.

## Content

The 1931 census counted the "indigenous" (non-European) civilian population of
Tunisia, Muslim and Jewish, by nationality. Table III gives these counts for
each **cheikhat** (the smallest administrative unit, under a sheikh), grouped by
**caïdat** (37) and by **contrôle civil** or military territory.

Each row of the CSV is one cell of the printed table: one cheikhat × religion ×
nationality. 804 cheikhats × 2 religions × 7 nationalities = 11,256 rows.

| Column | Meaning |
|---|---|
| `census` | `ind1931` |
| `table_id` | `III` |
| `source_page` | Printed page of the cell: the left page (even number) for Muslim cells, the right page for Jewish cells |
| `gallica_view` | Gallica view number of the spread |
| `controle_civil` | Contrôle civil as printed in the caïdat header, e.g. `Gabès`, `Le Kef`. The four southern caïdats are under military rule; their header names the territory instead: `Territoire militaire de Matmata`, `Territoire militaire de Kebili` (Nefzaoua), `Cercles de Médenine, Ben-Gardane et Zarzis` (Ouerghemma), `Cercle militaire de Tatahouine` |
| `caidat` | Caïdat name as in the table of contents (pp. 4–5), without the preposition: `Aradh` for "Caïdat de l'Aradh", `Kef` for "du Kef", `Madjeurs` for "des Madjeurs", `Tunis-Ville` for "Tunis-Ville (Médina)" |
| `cheikhat` | Cheikhat name as printed (period French transliteration). Where the table repeats a name with a ditto dash ("—") for "(partie rurale)" or "(partie communale)", the qualifier is written out |
| `cheikhat_note` | Footnote marker printed after the name, e.g. `(1)`, and/or the label of the bracket that groups the row, e.g. `Gabès commune (3)`, `Kairouan-Ville (2)`, `Commune de Sfax (2)`, `Cercle de Zarzis - Khalifalik des Accara (1); Commune de Zarzis (2)`. The footnotes are translated below |
| `duplicate` | `1` for the four Tunis-Ville rows that repeat groups already listed under Tunis-Banlieue (see "Double counting" below); `0` otherwise |
| `religion` / `religion_fr` | `muslim` (Population musulmane) or `jewish` (Population israélite) |
| `nationality` / `nationality_fr` | `tunisian` (Tunisiens), `algerian` (Algériens), `moroccan` (Marocains), `sudanese` (Soudanais), `syrian` (Syriens), `tripolitanian` (Tripolitains), `other` (Autres nationalités) |
| `value` | Number of persons (integer). A printed `»` is 0 |
| `flag` | `ocr_corrected` where the value differs from the raw Gallica OCR (see "Method"); empty otherwise |

The printed totals (Muslim total, Jewish total, grand total per cheikhat, and
the caïdat "Totaux", "A reporter" and "Report" lines) are not stored. They can
be recomputed by summing, and were used for validation.

## Method

1. Words and their positions come from Gallica's OCR, served by the BnF IIIF
   gateway (`ocr.py`). Each spread is split at the spine. Rows are grouped on
   each page separately and the two pages are aligned, since spreads are often
   scanned with a vertical shift between them. The alignment uses position and
   the requirement that the seven Muslim cells sum to the right page's Muslim
   total. Columns are assigned by the right edge of the (right-aligned)
   numbers, using a template fitted to each page.
2. Caïdats follow the table of contents. Each ends at its printed "Totaux" row
   (there are exactly 37), and every caïdat starts on the page the table of
   contents gives.
3. Every row was checked three ways (Muslim cells = Muslim total, Jewish cells =
   Jewish total, both = grand total). Every caïdat was checked column by column
   against its "A reporter", "Report" and "Totaux" lines.
4. Rows that failed a check, or that differed from the independent transcription
   in `data/colonial_tunisian_pop.rda` (Ben Salah, Chambru & Fourati 2024), were
   read from the page images, and the values were entered by hand
   (`CORRECTIONS` in the script). The right pages of views 14, 47, 48 and 50
   (pp. 19, 85, 87, 91) have no Gallica OCR, so both pages of those four spreads
   were transcribed from the images.
5. Two OCR misreadings were fixed by rule, but only when the fix makes all three
   row checks pass: a `»` read as `9` (or `8`) was set to 0; and a single cell
   the OCR missed was filled from the row's printed totals. These cells carry
   `ocr_corrected` too.
6. All 804 names and their bracket labels were compared with the page images
   (`NAMEFIX` in the script).

## Validation

| Check | Result |
|---|---|
| Row checks (3 × 872 printed rows: 804 cheikhats + 37 Totaux + 31 carry lines) | 2,615 / 2,616 pass. The one failure is a printing error (below) |
| Caïdat checks (17 columns × 54 "A reporter" / "Report" / "Totaux" lines) | 917 / 918 pass. Same printing error |
| Totals by contrôle civil vs Table I (pp. 6–7), Muslim / Jewish / grand total | 20 / 20 equal (excluding the 4 duplicate rows) |
| National totals vs Table I, all 17 columns | equal: Muslim 2,159,151; Jewish 56,248; total 2,215,399 |
| Agreement with Ben Salah et al. (2024) on Tunisian Muslims, Tunisian Jews, other Muslims and other Jews | 763 / 804 cheikhats. All 41 differences were checked on the images. They come from the reference's own regrouping: it merges communal and rural parts and the duplicate Tunis groups, splits combined cheikhats, and swaps Kairouan-Ville/Banlieue and El-Ghorfa Nord/Sud. One is a reference error: Driât has 3 Tripolitanians, not 0 |
| Cells changed from the raw OCR | 842 of 11,256 (`flag = ocr_corrected`), of which about 600 are on the four pages without OCR |

**Printing error.** In the Mahdia "Totaux" (p. 49), the "Autres nationalités"
(Muslim) cell is printed `»`. Yet the printed Muslim total (70,491) and the
"A reporter" line on p. 46 both include the 1 person listed under Bou-Merdas.
The cheikhat values are therefore consistent and are kept as printed.

**Double counting.** Footnote (4) on p. 91 and footnote (1) on p. 95 say that
four groups, "Tripolitains et Tiaches", "Djerbiens", "Gens de Gabès et de
Nefzaoua" and "Gens d'Ouerghemma et de Matmata" (13,440 persons), live in the
city of Tunis but fall administratively under the caïdat of Tunis-Banlieue. The
table lists them under both caïdats, and both caïdat "Totaux" include them.
Table I counts them once. Drop the rows with `duplicate == 1` to reproduce
Table I. Summing all rows gives 2,228,839 instead of 2,215,399.

## Footnotes (translated)

The markers apply within each page; `cheikhat_note` records the marker together
with the caïdat, so it is unambiguous.

| Pages | Caïdat | Footnote |
|---|---|---|
| 12–13 | Aïn-Draham | (1) Including the commune of Tabarka. (2) Including the commune of Aïn-Draham. |
| 14–15 | Aradh | (1) Total population of Chenini: 2,450. (2) Of the commune of El-Hamma: 5,123. (3) Of Gabès-Ville: 14,587; (4) of Gabès-Banlieue: 2,247; urban and rural population of Gabès: 16,834. |
| 16–17 | Béja | (1) Total population of Béja-Ville: 9,541. (2) Of Béja-Banlieue: 1,671. Total: 11,212. |
| 20–21 | Bizerte | (1) Total population of Bizerte-Ville: 15,235; of Bizerte-Banlieue: 3,204; total: 18,439. (2) Including the commune of Ferryville. |
| 24–25 | Djelass | (1) This cheikhat contains the commune of Hajeb-el-Aïoun. (2) This cheikhat contains Pichon, seat of the caïdat. |
| 26–27 | Djerba | (1) Population of the commune of Djerba: Muslims 243, Jews 4,098, total 4,341. (2) Communal part of the cheikhat of Taourit, and seat of the caïdat. |
| 28–29 | Djerid | (1) Total population of Degache: 4,795. (2) Population of the commune of Nefta: 12,976. (3) Population of the commune of Tozeur: 11,407. |
| 30–31 | Fraichiches, Gafsa | (1) Urban and rural population of Thala: 5,766. (2) Total population of El-Guettar: 4,208. (3) Urban and rural population of Gafsa: 8,649. |
| 32–33 | Gafsa | (1) Urban and rural population of Gafsa: 8,649. (2) Commune of Philippe-Thomas (Metlaoui). |
| 34–35 | Hammama | (1) This cheikhat contains the centre of Sidi-bou-Zid, seat of the caïdat. |
| 38–39 | Kairouan | (1) Total population of Kairouan-Banlieue: 4,366. (2) Of Kairouan-Ville: 20,738. Total: 25,104. |
| 40–41 | La Skhira | (1) Seat of the caïdat. |
| 42–43 | Kef | (1) Total population of Ebba-Ksour: 3,324. (2) Of El-Ghorfa: 7,040. (3) Of Kef-Ville: 7,226; (4) of Kef-Banlieue: 2,123 (urban and rural population of Le Kef). |
| 46–47 | Madjeurs, Mahdia | (1) Seat of the caïdat (Sbeïtla). (2) Total population of Teboulba: 6,265. (3) Urban and rural population of Mahdia: 8,551. (4) Total population of El-Djem: 5,949. |
| 48–49 | Mahdia | (1) Total population of Ksour-Essaf: 10,086. |
| 50–51 | Mateur, Matmata | (1) Urban and rural population of Mateur: 6,614. (2) This cheikhat (Achaches) contains Matmata, seat of the caïdat. |
| 52–53 | Medjez-el-Bab | (1) Rural and urban population of Medjez-el-Bab: 4,415. |
| 54–55 | Monastir | (1) Total population of Djemmal: 8,732. (2) Of the centre of Amira: 5,933. (3) Of Ksar-Helal: 7,319. |
| 56–57 | Monastir | (1) Total population of Moknine: 13,464. (2) Of Monastir: 9,396. (3) Of Touza: 1,758. (4) Of Zarmedine: 4,480. |
| 58–59 | Nabeul | (1) Urban and rural population of Nabeul: 12,839. |
| 60–61 | Nefzaoua | (1) Total population of Douz: 3,691. (2) Seat of the caïdat. |
| 62–63 | Ouerghemma | (1) Population of the cercle of Ben-Gardane: Muslims 26,177, Jews 458, total 26,635. (2) Of the cercle of Médenine: Muslims 26,436, Jews 594, total 27,030. |
| 64–65 | Ouerghemma | (1) Population of the cercle of Zarzis: Muslims 17,456, Jews 802, total 18,258. (2) Commune of Zarzis: Muslims 6,185, Jews 802, total 6,987. |
| 66–67 | Oulad-Aoun | (1) This cheikhat contains the centre of Siliana, seat of the caïdat. |
| 68–69 | Oulad-Ayar | (1) This cheikhat contains Maktar, seat of the caïdat. |
| 70–73 | Sfax | (1) Population of the Kerkenah islands: 14,071. (2) Population of Sfax-Ville: 31,792. |
| 74–75 | Souassi | (1) This cheikhat contains the small settlement of La Smala, seat of the caïdat. |
| 76–77 | Souk-el-Arba | (1) Urban and rural population of Ghardimaou: 5,710. (2) Of Souk-el-Arba: 4,608. |
| 78–79 | Souk-el-Khemis | (1) Urban and rural population of Souk-el-Khemis: 3,796. |
| 80–81 | Sousse | (1) Total population of Kalaâ-Kebira: 13,715. (2) Of M'Saken: 18,493. |
| 82–83 | Sousse | (1) Urban and rural population of Sousse: 17,529. |
| 88–89 | Téboursouk | (1) Urban and rural population of Téboursouk: 8,904. |
| 90–91 | Tunis-Banlieue | (1) Including the commune of Le Bardo. (2) Including the commune of Carthage. (3) Including the commune of Saint-Germain. (4) These groups, numbering 13,440 souls, live within the municipal boundary of Tunis while falling administratively under the caïdat of Tunis-Banlieue. |
| 94–95 | Tunis-Ville | (1) These 4 groups, numbering 13,440 souls, live in the city of Tunis but fall administratively under the caïdat of Tunis-Banlieue. |
| 96–97 | Zaghouan | (1) Urban and rural population of Zaghouan: 8,167. |

## Caveats

- Names are as printed, in the period's French transliteration and with its
  inconsistencies (e.g. `Ouled`/`Oulad`). They are not harmonised to modern
  names.
- The bracket label of the Médenine cercle is printed "Khalifalik des Khzours"
  on p. 62 and "Khalifalik des Ksours (suite)" on p. 64; both are kept as
  printed.
- The server delivers the page images at about half the canvas resolution
  (2,566 px per spread). Every value is legible at that resolution, but a few
  small superscript footnote markers could be misread.
