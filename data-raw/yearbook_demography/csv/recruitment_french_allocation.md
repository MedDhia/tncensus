# Répartition du recrutement (recrutement français)

Source: *Statistique générale de la Tunisie*, Régence de Tunis (annual). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR). Editions and views: see `EDITIONS.md`.

*Répartition du recrutement (recrutement français)*: 240 rows, conscription class (classe)s 1916-1939, one row per conscription and item.
Each value is taken from the latest transcribed edition that prints it (`census`).
Columns: `year` (conscription class (classe)), `item` (English code), `item_fr` (printed heading), `value`.

Checks per class: registered - exempted = remaining; the seven parts sum to the printed total; printed total = remaining.

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
800 comparisons, 788 equal, 12 different. Per edition (cells compared,
equal, differences):

- sgt1922: 70 compared, 70 equal
- sgt1923: 80 compared, 80 equal
- sgt1924: 90 compared, 90 equal
- sgt1925: 90 compared, 90 equal
- sgt1926: 90 compared, 90 equal
- sgt1927: 90 compared, 86 equal: 1921 part4_excluded_art4: 0 (latest printing, sgt1930: 1); 1922 part4_excluded_art4: 1 (latest printing, sgt1930: 0); 1923 part4_excluded_art4: 0 (latest printing, sgt1930: 1); 1924 part4_excluded_art4: 1 (latest printing, sgt1930: 0)
- sgt1928: 90 compared, 86 equal: 1921 part4_excluded_art4: 0 (latest printing, sgt1930: 1); 1922 part4_excluded_art4: 1 (latest printing, sgt1930: 0); 1923 part4_excluded_art4: 0 (latest printing, sgt1930: 1); 1924 part4_excluded_art4: 1 (latest printing, sgt1930: 0)
- sgt1929: 90 compared, 86 equal: 1921 part4_excluded_art4: 0 (latest printing, sgt1930: 1); 1922 part4_excluded_art4: 1 (latest printing, sgt1930: 0); 1923 part4_excluded_art4: 0 (latest printing, sgt1930: 1); 1924 part4_excluded_art4: 1 (latest printing, sgt1930: 0)
- sgt1930: 50 compared, 50 equal
- sgt1935: 30 compared, 30 equal
- sgt1936: 30 compared, 30 equal

The only differences: sgt1927, sgt1928 and sgt1929 print the single man of the 4th part
(*exclus*) on the 1922 and 1924 rows; sgt1922-sgt1926 and sgt1930 print it on the 1921 and
1923 rows. Each image was read at full resolution and shows what is transcribed. The row
totals decide for the 1921/1923 placement: with the 1922/1924 placement the parts of
sgt1927-sgt1929 add to 514, 620, 674 and 762 against printed totals of 515, 619, 675 and
761 (listed under Validation). The kept values (sgt1930, the latest printing) are the
consistent ones, so no flag is needed.

## Validation

277 of 312 printed-total checks pass. Failing checks (each re-read on the image at full resolution; printed values kept):

- sgt1922 1921 registered - exempted = remaining: computed 515 != printed 517
- sgt1922 1921 printed total = remaining: computed 515 != printed 517
- sgt1923 1921 registered - exempted = remaining: computed 515 != printed 517
- sgt1923 1921 printed total = remaining: computed 515 != printed 517
- sgt1924 1921 registered - exempted = remaining: computed 515 != printed 517
- sgt1924 1921 printed total = remaining: computed 515 != printed 517
- sgt1925 1921 registered - exempted = remaining: computed 515 != printed 517
- sgt1925 1921 printed total = remaining: computed 515 != printed 517
- sgt1926 1921 registered - exempted = remaining: computed 515 != printed 517
- sgt1926 1921 printed total = remaining: computed 515 != printed 517
- sgt1927 1921 registered - exempted = remaining: computed 515 != printed 517
- sgt1927 1921 parts = printed total: computed 514 != printed 515
- sgt1927 1921 printed total = remaining: computed 515 != printed 517
- sgt1927 1922 parts = printed total: computed 620 != printed 619
- sgt1927 1923 parts = printed total: computed 674 != printed 675
- sgt1927 1924 parts = printed total: computed 762 != printed 761
- sgt1927 1927 parts = printed total: computed 1835 != printed 1815
- sgt1928 1921 registered - exempted = remaining: computed 515 != printed 517
- sgt1928 1921 parts = printed total: computed 514 != printed 515
- sgt1928 1921 printed total = remaining: computed 515 != printed 517
- sgt1928 1922 parts = printed total: computed 620 != printed 619
- sgt1928 1923 parts = printed total: computed 674 != printed 675
- sgt1928 1924 parts = printed total: computed 762 != printed 761
- sgt1928 1927 parts = printed total: computed 1835 != printed 1815
- sgt1929 1921 registered - exempted = remaining: computed 515 != printed 517
- sgt1929 1921 parts = printed total: computed 514 != printed 515
- sgt1929 1921 printed total = remaining: computed 515 != printed 517
- sgt1929 1922 parts = printed total: computed 620 != printed 619
- sgt1929 1923 parts = printed total: computed 674 != printed 675
- sgt1929 1924 parts = printed total: computed 762 != printed 761
- sgt1929 1927 parts = printed total: computed 1835 != printed 1815
- sgt1930 1921 registered - exempted = remaining: computed 515 != printed 517
- sgt1930 1921 printed total = remaining: computed 515 != printed 517
- sgt1930 1927 parts = printed total: computed 1835 != printed 1815
- sgt1935 1927 parts = printed total: computed 1835 != printed 1815

Common columns: `census` (source edition, e.g. `sgt1930`), `gallica_ark` (volume ark), `table_id`, `source_page` (printed page), `gallica_view`, `value`, `flag` (empty, `ocr_corrected`, `illegible`, `total_mismatch`, `derived_from_totals`, `not_applicable`, `reprint_corrected`; see `data-raw/colonial_census/SPEC.md`). A printed `»` is stored as 0. Printed totals are not stored; they were used for validation.
