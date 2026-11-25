# Degré d'instruction des jeunes gens recrutés (recrutement français)

Source: *Statistique générale de la Tunisie*, Régence de Tunis (annual). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR). Editions and views: see `EDITIONS.md`.

*Degré d'instruction des jeunes gens recrutés (recrutement français)*: 168 rows, conscription class (classe)s 1916-1939, one row per conscription and item.
Each value is taken from the latest transcribed edition that prints it (`census`).
Columns: `year` (conscription class (classe)), `item` (English code), `item_fr` (printed heading), `value`.

Check per class: the seven categories sum to the printed total (printed totals are the registered men, or from 1933 the remaining men, of the allocation table).

Rows of a class or year that fail a check are flagged `total_mismatch` (all items of that
row); the values are kept as printed.

## Editions used and compared

Transcribed (printed window, Gallica view and printed page per edition): sgt1922 1916-1922 (view 46, p. 22), sgt1923 1916-1923 (view 524, p. 22), sgt1924 1916-1924 (view 1012, p. 22), sgt1925 1916-1925 (view 45, p. 21), sgt1926 1917-1926 (view 592, p. 28), sgt1927 1918-1927 (view 56, p. 28), sgt1928 1919-1928 (view 580, p. 28), sgt1929 1920-1929 (view 56, p. 28), sgt1930 1921-1930 (view 586, p. 28), sgt1935 1926-1935 (view 38, p. 18), sgt1936 1933-1937 (view 26, p. 15), sgt1939 1935-1939 (view 21, p. 15). Transcriptions:
`transcribed/recruitment.txt` (sgt1925, sgt1930, sgt1935, sgt1936, sgt1939) and
`transcribed/recruitment_1922_1929.txt` (sgt1922-sgt1924, sgt1926-sgt1929). Each edition
prints the French tables on one page and the indigenous tables on the facing page.

Source edition of each conscription class (classe) (the latest edition that prints it, rule 4 of
`SPEC_ADDENDUM.md`): 1916 from sgt1925, 1917 from sgt1926, 1918 from sgt1927, 1919 from sgt1928, 1920 from sgt1929, 1921-1925 from sgt1930, 1926-1932 from sgt1935, 1933-1934 from sgt1936, 1935-1939 from sgt1939.



Every other printing of the same cell was compared with the kept (latest) printing:
560 comparisons, 560 equal, 0 different. Per edition (cells compared,
equal, differences):

- sgt1922: 49 compared, 49 equal
- sgt1923: 56 compared, 56 equal
- sgt1924: 63 compared, 63 equal
- sgt1925: 63 compared, 63 equal
- sgt1926: 63 compared, 63 equal
- sgt1927: 63 compared, 63 equal
- sgt1928: 63 compared, 63 equal
- sgt1929: 63 compared, 63 equal
- sgt1930: 35 compared, 35 equal
- sgt1935: 21 compared, 21 equal
- sgt1936: 21 compared, 21 equal

## Validation

97 of 104 printed-total checks pass. Failing checks (each re-read on the image at full resolution; printed values kept):

- sgt1924 1924 row total: computed 792 != printed 791
- sgt1925 1924 row total: computed 792 != printed 791
- sgt1926 1924 row total: computed 792 != printed 791
- sgt1927 1924 row total: computed 792 != printed 791
- sgt1928 1924 row total: computed 792 != printed 791
- sgt1929 1924 row total: computed 792 != printed 791
- sgt1930 1924 row total: computed 792 != printed 791

Common columns: `census` (source edition, e.g. `sgt1930`), `gallica_ark` (volume ark), `table_id`, `source_page` (printed page), `gallica_view`, `value`, `flag` (empty, `ocr_corrected`, `illegible`, `total_mismatch`, `derived_from_totals`, `not_applicable`, `reprint_corrected`; see `data-raw/colonial_census/SPEC.md`). A printed `»` is stored as 0. Printed totals are not stored; they were used for validation.
