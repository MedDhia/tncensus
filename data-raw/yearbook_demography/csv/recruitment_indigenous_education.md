# Degré d'instruction des jeunes gens recrutés (recrutement indigène)

Source: *Statistique générale de la Tunisie*, Régence de Tunis (annual). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR). Editions and views: see `EDITIONS.md`.

*Degré d'instruction des jeunes gens recrutés (recrutement indigène)*: 96 rows, years 1916-1939, one row per year and item.
Each value is taken from the latest transcribed edition that prints it (`census`).
Columns: `year` (year), `item` (English code), `item_fr` (printed heading), `value`.

Check per year: the four categories sum to the printed total.

Rows of a class or year that fail a check are flagged `total_mismatch` (all items of that
row); the values are kept as printed.

## Editions used and compared

Transcribed (printed window, Gallica view and printed page per edition): sgt1922 1916-1922 (view 47, p. 23), sgt1923 1916-1923 (view 525, p. 23), sgt1924 1916-1924 (view 1013, p. 23), sgt1925 1916-1925 (view 46, p. 22), sgt1926 1917-1926 (view 593, p. 29), sgt1927 1918-1927 (view 57, p. 29), sgt1928 1919-1928 (view 581, p. 29), sgt1929 1920-1929 (view 57, p. 29), sgt1930 1921-1930 (view 587, p. 29), sgt1935 1926-1935 (view 40, p. 20), sgt1936 1932-1936 (view 27, p. 16), sgt1939 1935-1939 (view 22, p. 16). Transcriptions:
`transcribed/recruitment.txt` (sgt1925, sgt1930, sgt1935, sgt1936, sgt1939) and
`transcribed/recruitment_1922_1929.txt` (sgt1922-sgt1924, sgt1926-sgt1929). Each edition
prints the French tables on one page and the indigenous tables on the facing page.

Source edition of each year (the latest edition that prints it, rule 4 of
`SPEC_ADDENDUM.md`): 1916 from sgt1925, 1917 from sgt1926, 1918 from sgt1927, 1919 from sgt1928, 1920 from sgt1929, 1921-1925 from sgt1930, 1926-1931 from sgt1935, 1932-1934 from sgt1936, 1935-1939 from sgt1939.

Footnote printed under the table (sgt1922-sgt1930), on every 1918 cell: *(1) Le remplacement administratif a été supprimé en 1918* (administrative replacement was abolished in 1918).

Every other printing of the same cell was compared with the kept (latest) printing:
320 comparisons, 320 equal, 0 different. Per edition (cells compared,
equal, differences):

- sgt1922: 28 compared, 28 equal
- sgt1923: 32 compared, 32 equal
- sgt1924: 36 compared, 36 equal
- sgt1925: 36 compared, 36 equal
- sgt1926: 36 compared, 36 equal
- sgt1927: 36 compared, 36 equal
- sgt1928: 36 compared, 36 equal
- sgt1929: 36 compared, 36 equal
- sgt1930: 20 compared, 20 equal
- sgt1935: 16 compared, 16 equal
- sgt1936: 8 compared, 8 equal

## Validation

104 of 104 printed-total checks pass.

Common columns: `census` (source edition, e.g. `sgt1930`), `gallica_ark` (volume ark), `table_id`, `source_page` (printed page), `gallica_view`, `value`, `flag` (empty, `ocr_corrected`, `illegible`, `total_mismatch`, `derived_from_totals`, `not_applicable`, `reprint_corrected`; see `data-raw/colonial_census/SPEC.md`). A printed `»` is stored as 0. Printed totals are not stored; they were used for validation.
