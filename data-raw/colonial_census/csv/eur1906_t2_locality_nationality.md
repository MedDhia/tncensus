# eur1906 Table II — Répartition par nationalités et localités

*Distribution by nationality and locality.* Same source, printed pages 6–15
(views 10–19). Built from `transcriptions/eur1906_t2_f010.txt` … `f019.txt`.

Unit: 333 localities (towns, banlieues, villages, farms, mines, worksites),
grouped under the printed section headers *Contrôle de …* / *Annexe de …* /
*Territoires du Sud*. A page without a header continues the previous section.

| Column | Meaning |
|---|---|
| `controle_civil` | Contrôle civil, spelled as in Table I so the two tables join (header *Contrôle du Kef* → `Le Kef`) |
| `annexe` | Annexe, spelled as in Table I (header *Annexe de Téboursouk* → `Teboursouk`), empty otherwise |
| `locality` | Locality as printed, OCR errors fixed from the image. Names on two printed lines are joined into one. Some names occur in two contrôles (e.g. `Sidi-Ahmed` in Béja and Bizerte), so use `controle_civil` + `locality` as the key |
| `nationality` | as in Table I |
| `value` | Number of European civilians |

1,998 rows (333 localities × 6 nationalities). The printed TOTAL column is not stored.

**Validation (all passing).** 333 locality row totals checked. Every
contrôle/annexe sum matches its Table I row, in all 7 columns (19 × 7 = 133
checks), and the localities add up to the national total of 128,895.
28 cells were corrected from the page image (`flag = ocr_corrected`).
Printing quirks:
- Korbous (Grombalia): Maltese 12 is printed half a line low, level with
  Menzel-bou-Zelfa. It belongs to Korbous: 30 + 317 + 12 = 359, and
  Menzel-bou-Zelfa's printed total of 59 needs a zero there.
- Ben-Bachir (other Europeans) and Zarzis-Environs (Spanish) print `«` where a
  value belongs. The row totals show these are 0.
