# 1906 Table VII: profession, sex and nationality by circonscription

**VII. Répartition d'après la profession, le sexe et la nationalité, par
circonscriptions administratives** (Distribution by profession, sex and
nationality, by administrative district). European civilian population, 16
December 1906.

- Source: Gallica ark `bd6t53563851`, pp. 26-33 (views 29-32: four two-page fold-out spreads).
- Rows: 3,648 = 19 circonscriptions x 6 nationalities x 32 columns (7 profession groups x active/family x sex, plus rentiers and unclassified x sex).
- Script: `data-raw/colonial_census/extract_eur1906_t6_t7.py`; transcription: `transcribed/eur1906_t7.txt`.

## Columns

As in `eur1906_t6_profession_nationality.md`, plus `controle_civil`, the
circonscription (contrôle civil, or *Territoires du Sud*), spelled as printed:
Béja, Medjez-el-Bab, Bizerte, Gabès, Djerba, Gafsa, Tozeur, Grombalia, Kairouan,
Le Kef, Teboursouk, Mactar, Sfax, Souk-el-Arba, Tabarca, Sousse, Thala, Tunis,
Territoires du Sud.

## Method

Gallica's OCR placed numbers in the wrong rows and columns too often (383 of
798 checks failed on an OCR parse), so every block was transcribed by hand from
page-image crops. The IIIF server caps images at half the canvas resolution
(about 2,650 px per spread), which is still legible.

On these fold-outs, the column next to the binding is partly or wholly hidden:
transport/active/male on view 30 (Gafsa, Grombalia, Kairouan; leading digits only
for Gafsa) and views 31-32 (Teboursouk, Sfax, Souk-el-Arba), and
industry/family/female on views 31-32 (all ten circonscriptions). These 90
cells were solved with integer bound propagation from:

1. the printed circonscription total of the column pair,
2. the Table VI national total for the nationality, minus all legible cells,
3. for French cells, Table G (French men and women by profession group, active + family, per circonscription),
4. the visible last digit, where one shows.

16 cells were determined exactly (flag `derived_from_totals`): all 13 French cells and
Teboursouk's Spanish transport cell. The other 74 cells, for Italians, Maltese
and the smaller nationalities, are left empty (flag `illegible`). Their sum per
circonscription and per nationality is still known from the printed totals.

| Column hidden | Circonscriptions | Illegible cells |
|---|---|---:|
| industry / family / female | Le Kef, Teboursouk, Mactar, Sfax, Souk-el-Arba, Tabarca, Sousse, Thala, Tunis, Territoires du Sud | 50 |
| transport / active / male | Gafsa (IT, MT), Grombalia, Kairouan, Teboursouk (IT, MT), Sfax, Souk-el-Arba | 24 |

## Validation

- Every legible cell was checked against its circonscription's printed pair or column total, and every printed group total against the pair totals.
- French cells were checked against Table G for all 17 Table G units, and each column summed over circonscriptions against Table VI.
- 1,936 checks run (including those for Table VI, Table G and the commentary tables). None fail, apart from the documented cases below.

**Four printed cells contradict both their circonscription total and Table VI**
(and Table G for the French cell). They are kept as printed with flag
`total_mismatch`:

| Circonscription | Cell | Printed | Implied by the totals |
|---|---|---:|---:|
| Tunis | French, unclassified, female | 1.443 | 1.413 |
| Djerba | Greek, commerce, active, female | 7 | 0 |
| Le Kef | Italian, liberal professions, family, male | 1 | 0 |
| Souk-el-Arba | other European, agriculture, family, female | » | 1 |

**19 warnings:** for some nationality columns, Table VII summed over
circonscriptions differs from Table VI by 1 to 69 persons. Within each column the
differences cancel out across nationalities, and every circonscription total
holds. So the two printed tables disagree on how people are split between
nationalities, mostly in commerce and liberal professions; the largest case is
Italian unclassified, +69 men / -69 women. Spot checks of the largest blocks
(Tunis, Sfax, Sousse) against the image confirmed the transcription. Values
are kept as printed in Table VII.

## Notes printed with the table (p. 26-27)

See `eur1906_t6_profession_nationality.md` (the notes apply to both tables).
