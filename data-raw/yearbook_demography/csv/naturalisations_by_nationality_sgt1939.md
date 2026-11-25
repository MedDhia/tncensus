# Naturalisations by nationality, legal basis and year (sgt1939 printing, table e)

Source: *Statistique générale de la Tunisie*, Régence de Tunis (annual). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR). Editions and views: see `EDITIONS.md`.

Table e) *Naturalisations accordées*, as printed in the 1939 edition (pp. 12-13):
512 rows, 32 nationalities. Same columns as the sgt1930 file;
`age_group` is always `total` (adults and minors together). Periods: 1891-1898, 1899-1910,
1911-1922, 1915-1924 (by legal basis), 1924-1928 (one column), then each year 1929-1939.
Categories differ from 1930: *Maltais* (for Anglo-Maltais), *Turcs* and *Syriens*
separately, *Yougo-Slaves* (for Serbes), Algerians and Tunisians by religion
(catholiques / musulmans / israélites), plus Marocains, Indochinois, Indigènes de
l'A.O.F. and Anglais.

Misprints confirmed on the scan:

- 1935: the cells sum to 668 but the total is printed 686 (transposed digits); the 1935
  edition's table a also gives 668.
- 1938, Suisses: printed `0` (zero is otherwise printed `»`); the column total (1.278)
  needs 10. The printed 0 is kept and flagged `total_mismatch`.

## Comparison with the 1930 printing

The two printings overlap on 1891-1930. Comparing sgt1930 (adults + minors, with its
categories mapped onto the 1939 ones: Anglo-Maltais = Maltais, Turcs et Syriens = Turcs,
Serbes = Yougo-Slaves, Norvégiens = Norvégiens et Suédois, Indigènes catholiques =
Algériens catholiques; 1911-1920 + 1921 + 1922 + 1923 = the 1939 column "1911 à 1922";
1924 + ... + 1928 = "1924 à 1928"): 238 comparisons, 188 equal,
50 different:

- 1891-1898, other: sgt1930 3, sgt1939 0
- 1891-1898, russian: sgt1930 0, sgt1939 3
- 1899-1910, other: sgt1930 5, sgt1939 0
- 1899-1910, russian: sgt1930 1, sgt1939 6
- 1924-1928, all nationalities: sgt1930 13997, sgt1939 13996
- 1924-1928, albanian: sgt1930 0, sgt1939 7
- 1924-1928, algerian_catholic: sgt1930 0, sgt1939 11
- 1924-1928, algerian_muslim: sgt1930 143, sgt1939 132
- 1924-1928, austrian: sgt1930 13, sgt1939 40
- 1924-1928, belgian: sgt1930 17, sgt1939 21
- 1924-1928, british: sgt1930 0, sgt1939 9
- 1924-1928, czechoslovak: sgt1930 0, sgt1939 4
- 1924-1928, german: sgt1930 13, sgt1939 16
- 1924-1928, greek: sgt1930 148, sgt1939 153
- 1924-1928, hungarian: sgt1930 0, sgt1939 2
- 1924-1928, maltese: sgt1930 973, sgt1939 1002
- 1924-1928, moroccan: sgt1930 0, sgt1939 11
- 1924-1928, other: sgt1930 152, sgt1939 0
- 1924-1928, polish: sgt1930 9, sgt1939 17
- 1924-1928, romanian: sgt1930 0, sgt1939 4
- 1924-1928, russian: sgt1930 211, sgt1939 212
- 1924-1928, swiss: sgt1930 42, sgt1939 63
- 1924-1928, syrian: sgt1930 0, sgt1939 17
- 1924-1928, tunisian_muslim: sgt1930 788, sgt1939 787
- 1929, all nationalities: sgt1930 2639, sgt1939 2601
- 1929, algerian_catholic: sgt1930 0, sgt1939 18
- 1929, algerian_jew: sgt1930 22, sgt1939 15
- 1929, algerian_muslim: sgt1930 13, sgt1939 18
- 1929, austrian: sgt1930 0, sgt1939 2
- 1929, belgian: sgt1930 2, sgt1939 4
- 1929, british: sgt1930 0, sgt1939 5
- 1929, czechoslovak: sgt1930 0, sgt1939 2
- 1929, dutch: sgt1930 0, sgt1939 1
- 1929, french_west_african: sgt1930 0, sgt1939 2
- 1929, german: sgt1930 1, sgt1939 9
- 1929, greek: sgt1930 47, sgt1939 48
- 1929, hungarian: sgt1930 0, sgt1939 4
- 1929, italian: sgt1930 1389, sgt1939 1330
- 1929, maltese: sgt1930 165, sgt1939 187
- 1929, moroccan: sgt1930 0, sgt1939 7
- 1929, other: sgt1930 78, sgt1939 0
- 1929, polish: sgt1930 0, sgt1939 7
- 1929, portuguese: sgt1930 0, sgt1939 1
- 1929, russian: sgt1930 58, sgt1939 54
- 1929, spanish: sgt1930 14, sgt1939 11
- 1929, swiss: sgt1930 0, sgt1939 10
- 1929, syrian: sgt1930 0, sgt1939 1
- 1929, tunisian_jew: sgt1930 742, sgt1939 747
- 1929, turkish: sgt1930 0, sgt1939 9
- 1929, yugoslav: sgt1930 0, sgt1939 1

What the differences show:

- 1911-1922, 1915-1924 and 1930 agree exactly, nationality by nationality.
- 1891-1898 and 1899-1910 differ only through reclassification: the 1939 edition counts as
  Russians the entries that the 1930 edition prints under *Indigènes catholiques* and
  *Divers* (and the 1930 *Divers* row duplicates *Indigènes catholiques*, see the sgt1930
  notes).
- 1924-1928 and 1929 were revised, not only reclassified: the period totals are close
  (13.997 vs 13.996; 2.639 or 2.636 vs 2.601), but many nationalities change (1924-1928:
  Swiss 42 vs 63, Austrians 13 vs 40, Maltese 973 vs 1.002; 1929: Italians 1.389 vs
  1.330, Swiss 0 vs 10, Turks 0 vs 9), and the 1930 *Divers* (152 and 78) is spread over
  new categories (Marocains, Syriens, Anglais, Algerian Catholics, ...).

Values are kept as each edition prints them; neither file is corrected from the other.
For 1924-1929 the two files are alternative printings; prefer the 1939 printing for
totals by nationality, and the 1930 printing for the adults/minors split.

## Comparison with the 1935 and 1936 printings

Their printed totals for every period and year (1891-1898 to 1934 in sgt1935, to 1936 in
sgt1936; 1924-1928 summed from their yearly columns: 13.996) equal this file's, except
1935: both print 668, confirming that this edition's 686 is a misprinted total (the cells
sum to 668; no value changes). They also agree with this file on the revised 1929 total
(2.601). Only the totals were compared, not every cell. 1938 (Suisses printed 0) and 1937-1939
appear in no other printing.

## Validation

54 of 58 printed-total checks pass. Failing checks (each re-read on the image at full resolution; printed values kept):

- sgt1930 1925 minors column total: computed 1726 != printed 1736
- sgt1930 1929 adults column total: computed 1348 != printed 1345
- sgt1939 1935 total column total: computed 668 != printed 686
- sgt1939 1938 total column total: computed 1268 != printed 1278

Common columns: `census` (source edition, e.g. `sgt1930`), `gallica_ark` (volume ark), `table_id`, `source_page` (printed page), `gallica_view`, `value`, `flag` (empty, `ocr_corrected`, `illegible`, `total_mismatch`, `derived_from_totals`, `not_applicable`, `reprint_corrected`; see `data-raw/colonial_census/SPEC.md`). A printed `»` is stored as 0. Printed totals are not stored; they were used for validation.

## Cell-by-cell comparison with the other printings

`compare_naturalisations_e.py` compares the sgt1935 and sgt1936 printings with
this file, cell by cell. Mappings:
- *Anglo-Maltais* = *Maltais*.
- *Divers* is compared with the sum of the rows that replace it here (Marocains, Syriens, Indochinois, A.O.F.).
- sgt1935's "1911 à 1923" = this file's "1911-1922". The values are identical; the label "1911-1922" is as printed in 1939 but covers 1911–1923.
- sgt1935's yearly 1924–1928 columns are summed.

| Edition | Views (pp.) | Cells compared | Equal | Different | Own printed totals |
|---|---|---:|---:|---:|---|
| sgt1935 | 34–35 (14–15) | 348 | 309 | 39 | 14/16 |
| sgt1936 | 23–24 (12–13) | 348 | 328 | 20 | 15/16 |

**sgt1935 vs sgt1936:** on the columns both print, 402 of 406 cells are equal.

Every difference is a revision in the 1939 edition, which keeps the same totals, or a misprint in the reprint:
- **1891–1898 and 1899–1910, both editions:** Russes 0 and 1 against 3 and 6 here; Divers 3 and 5 against 0. The 1939 edition moved those Divers to Russes.
- **1924–1928, sgt1935 (16 cells):** sgt1935's years sum to the 1930 edition's figures. The 1939 edition prints a revised breakdown with the same total (13,996). For example, Maltais 973 against 1,002 here, Suisses 42 against 63, Divers 152 against 28.
- **1929, both editions (16 cells):** the reprints put 68 under Divers. The 1939 edition spreads them over 15 nationalities, with the same total (2,601).
- **1934, sgt1935:** Tunisiens catholiques 5 and musulmans 6 against 0 here. Its cells then sum to 843 against its own printed 832, and sgt1936 and sgt1939 print `»`, so this is a sgt1935 misprint.
- **1935, sgt1935:** Tchéco-Slovaques 2 against 3 here. Its cells sum to 667 against its printed 668, and sgt1936 prints 3, so this is a sgt1935 misprint.
- **sgt1936:** 1926 Italiens is printed 1,311, against 1,341 in sgt1935. The cells then sum to 3,144 against its printed 3,174, a sgt1936 misprint. sgt1936 has no 1924 column.

For the revised years, each image supports its own value; the stored values match the 1939 scans (views 18–19). sgt1939's 1937–1939 columns appear in no other printing, so the 1938 Suisses printed 0 (its total needs 10) remains unresolved. No stored value is corrected.
