# 1926 census, table b: French population by place of birth, 1891–1926

**b) Population française d'après le lieu de naissance (de 1891 à 1926 inclus)**
*French civilian population by place of birth, censuses of 1891, 1896, 1901, 1906, 1911, 1921 and 1926.*

Source: sgt1926, `bpt6k9105650k` views 568–569 (printed pp. 4–5). Source gallica.bnf.fr /
Ministère des Affaires étrangères. Reprinted in sgt1927 (views 32–33), sgt1928 (556–557),
sgt1929 (32–33) and sgt1930 (562–563).

Rows: 96 birthplaces × 7 censuses = 672. Birthplaces as printed: Tunisia, the three Algerian
départements, the French départements (including Moselle and Rhin (Bas-), printed `»` before
1921), colonies and possessions, abroad (`Etranger`), unknown (`Lieux inconnus`). Footnotes:
(1) colonies other than Algeria and Tunisia; (2) the `Lieux inconnus` heading was used only in
1906, not in earlier counts nor in 1911, 1921 and 1926.

## Method
Majority of the OCR of the five printings; every disagreeing cell (92) read on the scans.
All were OCR misreads. Two cells read by eye: Algérie : Oran 1891 = 162 and Drôme 1926 = 415
(`ocr_corrected`).

## Validation
Running totals (`A reporter`, `Report`) and the grand totals (`Totaux généraux`) for every
census: 14 checks, 12 pass. The two failures are misprints, identical in all five printings,
kept as printed and flagged `total_mismatch`:
- **Tarn 1906** printed 191; the totals imply 194 (the 1906 census volume prints 194).
- **Vienne (Haute-) 1921** printed 14; the totals imply 142 (1911: 135).

**Comparison with the 1906 census volume** (Table E, `eur1906_te_french_by_birthplace_1891_1906.csv`,
same birthplaces 1891–1906): 8 cells differ. Apart from Tarn 1906, the yearbook values are the
ones that make the 1906 volume's own totals add up exactly: Var 1891 110 (1906 vol. 118, −8);
Etranger 1896 679 (689, −10); Var 1901 286 (256, +30); Bouches-du-Rhône 1906 922 (822, +100),
Gironde 1906 374 (324, +50), Calvados 1906 55 (54, +1). With them the 1906 volume's computed
totals equal its printed totals for all four years (9.973, 16.207, 24.201, 34.610). These are
the same six values as in the 1922 edition (see `cens1921_french_birthplace_1891_1921.md`):
each year's changes exactly offset that year's gap, which suggests the compilers forced the
old columns to add up rather than re-reading the 1906 returns. The 1906 volume's commentary
(pp.44-45) confirms only Bouches-du-Rhône 922; it gives Gironde 324 (+58 since 1901) and Var
256 in 1901 (+147 to 403 in 1906), contradicting the yearbook. So the yearbook values do not
settle Table E's residuals, and Table E is kept as printed (see its notes).

## Reprint comparison (OCR cells equal / different / unread, of 693)
sgt1926 590 / 80 / 23; sgt1927 673 / 4 / 16; sgt1928 679 / 4 / 10; sgt1929 675 / 3 / 15;
sgt1930 670 / 1 / 22. All differences were OCR misreads; no printing variants.
