# eur1906 Table I — Répartition par nationalités et circonscriptions administratives

*Distribution by nationality and administrative district.* Source: *Dénombrement de
la population européenne civile en Tunisie au 16 décembre 1906* (Tunis, 1907),
Gallica `bd6t53563851`, printed page 5 (view 9). Built by
`data-raw/colonial_census/extract_eur1906_t1_t3.py build` from
`transcriptions/eur1906_t1_f009.txt`.

Unit: the 19 *circonscriptions* of Table I: 14 contrôles civils, 5 annexes and
the Territoires du Sud. For an annexe, `controle_civil` is its parent contrôle
and `annexe` is the annexe, which matches the Table II sections. A contrôle row
**excludes** its annexe; summing Table II localities confirms this.

| Column | Meaning |
|---|---|
| `controle_civil` | Contrôle civil, as printed in Table I (`Le Kef`, `Territoires du Sud`, …) |
| `annexe` | Annexe (Medjez-el-Bab, Djerba, Tozeur, Teboursouk, Tabarca), empty otherwise |
| `nationality` | `french`, `italian`, `maltese`, `spanish`, `greek`, `other_european` |
| `value` | Number of European civilians (persons) |

114 rows (19 units × 6 nationalities). The printed TOTAL column and TOTAUX row
are not stored.

**Validation.** 19 row totals and 7 column totals checked, all passing. 2 cells
were corrected from the image: Gabès Greek = 1 (OCR '•1'), and Djerba French = 187
(OCR '487'). Both are confirmed by the Table II locality sums.
National totals: 34,610 French, 81,156 Italian, 10,330 Maltese, 600 Spanish,
683 Greek, 1,516 other Europeans; 128,895 in all.

The margins carry pencilled numbers added by a later reader; they are ignored.
