# Expulsions by nationality, 1913-1934

Source: *Statistique générale de la Tunisie*, Régence de Tunis (annual). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR). Editions and views: see `EDITIONS.md`.

*Expulsions prononcées*, by nationality, 1913-1934. 308 rows: one per
nationality and year. Each edition prints the last ten years (sgt1922: 1913-1922 ...
sgt1935: 1925-1934; the 1936 and 1939 editions print no expulsions table). Each year
is taken from the latest edition that prints it (`census` names that edition).

Columns: `year`, `nationality` (English code), `nationality_fr` (as printed: Allemands,
Anglais, Anglo-Maltais, Autrichiens, Belges, Egyptiens, Espagnols, Grecs, Italiens,
Marocains, Ottomans, Russes, Suisses, Divers = `other`), `value` = persons expelled.

## Comparison of the overlapping printings

Every cell of every other printing of the same year was compared with the kept value:
1092 comparisons, 1066 equal, 26 different:

- 1915 Russes: sgt1922 prints 0, sgt1924 prints 2
- 1915 Russes: sgt1923 prints 0, sgt1924 prints 2
- 1915 Suisses: sgt1922 prints 2, sgt1924 prints 0
- 1915 Suisses: sgt1923 prints 2, sgt1924 prints 0
- 1916 Russes: sgt1922 prints 0, sgt1925 prints 4
- 1916 Russes: sgt1923 prints 0, sgt1925 prints 4
- 1916 Suisses: sgt1922 prints 4, sgt1925 prints 0
- 1916 Suisses: sgt1923 prints 4, sgt1925 prints 0
- 1917 Russes: sgt1922 prints 0, sgt1926 prints 2
- 1917 Russes: sgt1923 prints 0, sgt1926 prints 2
- 1917 Suisses: sgt1922 prints 2, sgt1926 prints 0
- 1917 Suisses: sgt1923 prints 2, sgt1926 prints 0
- 1918 Russes: sgt1922 prints 2, sgt1927 prints 1
- 1918 Russes: sgt1923 prints 2, sgt1927 prints 1
- 1918 Suisses: sgt1922 prints 1, sgt1927 prints 2
- 1918 Suisses: sgt1923 prints 1, sgt1927 prints 2
- 1920 Russes: sgt1922 prints 4, sgt1929 prints 1
- 1920 Russes: sgt1923 prints 4, sgt1929 prints 1
- 1920 Suisses: sgt1922 prints 1, sgt1929 prints 4
- 1920 Suisses: sgt1923 prints 1, sgt1929 prints 4
- 1922 Italiens: sgt1922 prints 33, sgt1930 prints 35
- 1922 Italiens: sgt1923 prints 33, sgt1930 prints 35
- 1922 Italiens: sgt1924 prints 33, sgt1930 prints 35
- 1922 Italiens: sgt1925 prints 33, sgt1930 prints 35
- 1923 Russes: sgt1923 prints 2, sgt1930 prints 0
- 1923 Suisses: sgt1923 prints 0, sgt1930 prints 2

What the differences mean:

- **Swiss and Russians, 1913-1923.** The 1922 and 1923 editions print under *Russes* the
  figures that the 1924 and later editions print under *Suisses*, and vice versa. Every
  later edition uses the 1924 assignment, which is kept here; but 1913 and 1914 are
  printed only in the 1922/1923 editions, so their Swiss and Russian values follow the
  1922/1923 labels and may be swapped. Use the two together if in doubt.
- **Italians, 1922.** The 1922-1925 editions print 33 (1922 total 44). The 1926 and
  1927 editions print 35 but leave the totals at the values implied by 33 (row totals
  463 and 475, 1922 total 44); from 1928 the totals are corrected (1922 total 46). The
  kept value is 35 (sgt1930), consistent with its own totals.
- **1917, Ottomans:** blank in the 1922-1925 editions, `»` from 1926; stored as 0.

## Printed totals

- The 1919 column total is printed 102 in the 1922-1926 editions, but its cells sum to
  80 in every printing; the 1924 edition's grand total (771) agrees with 80, and the
  1927 and later editions print 80.
- In sgt1935 the TOTAUX column covers 1924-1934 (eleven years) although the table shows
  only 1925-1934; the row and grand totals check once the 1924 values (from sgt1930)
  are added.

## Validation

209 of 220 printed-total checks pass. Failing checks (each re-read on the image at full resolution; printed values kept):

- sgt1922 1919 column total: computed 80 != printed 102
- sgt1923 1919 column total: computed 80 != printed 102
- sgt1924 1919 column total: computed 80 != printed 102
- sgt1925 1919 column total: computed 80 != printed 102
- sgt1926 Italiens row total: computed 465 != printed 463
- sgt1926 1919 column total: computed 80 != printed 102
- sgt1926 1922 column total: computed 46 != printed 44
- sgt1926 grand total: computed 810 != printed 808
- sgt1927 Italiens row total: computed 477 != printed 475
- sgt1927 1922 column total: computed 46 != printed 44
- sgt1927 grand total: computed 845 != printed 843

Common columns: `census` (source edition, e.g. `sgt1930`), `gallica_ark` (volume ark), `table_id`, `source_page` (printed page), `gallica_view`, `value`, `flag` (empty, `ocr_corrected`, `illegible`, `total_mismatch`, `derived_from_totals`, `not_applicable`, `reprint_corrected`; see `data-raw/colonial_census/SPEC.md`). A printed `»` is stored as 0. Printed totals are not stored; they were used for validation.
