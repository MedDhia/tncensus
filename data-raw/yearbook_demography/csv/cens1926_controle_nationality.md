# 1926 census, table a: civilian population by contrôle civil

**a) État de la population civile (européenne et indigène) par circonscription de Contrôle civil, d'après le recensement de 1926**
*Civilian population (European and indigenous) by contrôle civil, 1926 census.*

Source: *Statistique générale de la Tunisie*, 1926 edition (`sgt1926`), volume ark
`bpt6k9105650k`, views 566–567 (printed pp. 2–3). Source gallica.bnf.fr / Ministère des
Affaires étrangères. Reprinted unchanged in sgt1927 (`bpt6k91056510` views 30–31), sgt1928
(views 554–555), sgt1929 (`bpt6k9105652d` views 30–31) and sgt1930 (views 560–561).

Rows: 20 contrôles civils × (6 European nationalities + 7 Muslim nationalities + 6 Jewish
nationalities) = 380. The Jewish block has no Sudanese column. Printed totals (European,
Muslim, Jewish, indigenous, grand total, and the Totaux row) are not stored.

| Column | Content |
|---|---|
| `controle_civil` | As printed (`Kef (Le)`, `Territoires militaires`) |
| `population_group` | `european`, `muslim`, `jewish` (`_fr` as printed) |
| `nationality` | `french`, `italian`, `maltese`, `spanish`, `greek`, `other_european`; for Muslims and Jews `tunisian`, `algerian`, `moroccan`, `sudanese` (Muslims only), `syrian`, `tripolitanian`, `other` |
| `value` | Persons |

## Method
Every cell is the majority reading of Gallica's OCR across the five printings, and every
cell where a printing's OCR disagreed with the majority was read on the scans (137 cells).
All 137 were OCR misreads (`6`↔`0`, `1`↔`4`, dropped digits); the five printings are
identical. One cell was read by eye only: Thala, Muslim Sudanese = 9 (`ocr_corrected`).

## Validation
- Row checks for every contrôle and the Totaux row (European, Muslim, Jewish, indigenous,
  grand total) and all 24 column totals: 129 checks, all pass. Grand total 2,159,708
  (Europeans 173,281; Muslims 1,932,184; Jews 54,243).
- French total 71,020 = table b's 1926 total.
- **Cross-check with the 1931 census volume** (Table IV, 1926 column,
  `ind1931_t4_controle_1926_1931.csv`): Muslim and Jewish totals agree for all 20
  contrôles (40 / 40).

## Reprint comparison (OCR cells equal / different / unread, of 504)
sgt1926 313 / 93 / 98; sgt1927 473 / 1 / 30; sgt1928 356 / 36 / 112; sgt1929 460 / 4 / 40;
sgt1930 469 / 3 / 32. Every difference was checked on the image: none is a printing variant.
