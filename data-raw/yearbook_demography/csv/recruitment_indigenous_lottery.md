# Opérations des Commissions de tirage au sort, répartition des conscrits (recrutement indigène)

Source: *Statistique générale de la Tunisie*, Régence de Tunis (annual). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR). Editions and views: see `EDITIONS.md`.

*Opérations des Commissions de tirage au sort, répartition des conscrits (recrutement indigène)*: 324 rows, years 1913-1939, one row per year and item.
Each value is taken from the latest transcribed edition that prints it (`census`).
Columns: `year` (year), `item` (English code), `item_fr` (printed heading), `value`.

No totals are printed and no identity holds between the columns, so this table has no total checks; only the overlapping printings were compared.

Rows of a class or year that fail a check are flagged `total_mismatch` (all items of that
row); the values are kept as printed.

## Editions used and compared

Transcribed (printed window, Gallica view and printed page per edition): sgt1922 1913-1922 (view 47, p. 23), sgt1923 1914-1923 (view 525, p. 23), sgt1924 1915-1924 (view 1013, p. 23), sgt1925 1916-1925 (view 46, p. 22), sgt1926 1917-1926 (view 593, p. 29), sgt1927 1918-1927 (view 57, p. 29), sgt1928 1919-1928 (view 581, p. 29), sgt1929 1920-1929 (view 57, p. 29), sgt1930 1921-1930 (view 587, p. 29), sgt1935 1926-1935 (view 40, p. 20), sgt1936 1932-1936 (view 27, p. 16), sgt1939 1935-1939 (view 22, p. 16). Transcriptions:
`transcribed/recruitment.txt` (sgt1925, sgt1930, sgt1935, sgt1936, sgt1939) and
`transcribed/recruitment_1922_1929.txt` (sgt1922-sgt1924, sgt1926-sgt1929). Each edition
prints the French tables on one page and the indigenous tables on the facing page.

Source edition of each year (the latest edition that prints it, rule 4 of
`SPEC_ADDENDUM.md`): 1913 from sgt1922, 1914 from sgt1923, 1915 from sgt1924, 1916 from sgt1925, 1917 from sgt1926, 1918 from sgt1927, 1919 from sgt1928, 1920 from sgt1929, 1921-1925 from sgt1930, 1926-1931 from sgt1935, 1932-1934 from sgt1936, 1935-1939 from sgt1939.

Footnote printed under the table (sgt1922-sgt1930), on the 1917 and 1918 cells of the surplus and family-support columns (the marks sit slightly differently from one edition to the next): *(1) Envoyés en France : travailleurs agricoles réquisitionnés* (sent to France: requisitioned agricultural workers).

Every other printing of the same cell was compared with the kept (latest) printing:
996 comparisons, 993 equal, 3 different. Per edition (cells compared,
equal, differences):

- sgt1922: 108 compared, 108 equal
- sgt1923: 108 compared, 108 equal
- sgt1924: 108 compared, 107 equal: 1924 exempt_family_support: 3683 (latest printing, sgt1930: 3684)
- sgt1925: 108 compared, 108 equal
- sgt1926: 108 compared, 107 equal: 1926 volunteers: 880 (latest printing, sgt1935: 261)
- sgt1927: 108 compared, 108 equal
- sgt1928: 108 compared, 108 equal
- sgt1929: 108 compared, 108 equal
- sgt1930: 60 compared, 60 equal
- sgt1935: 48 compared, 47 equal: 1932 unfit_illness: 11104 (latest printing, sgt1936: 11404)
- sgt1936: 24 compared, 24 equal

- 1924, family support: sgt1924 prints 3.683; sgt1925-sgt1930 print 3.684. Both images
  are clear at full resolution. No total or identity decides; the latest printing (3.684,
  sgt1930) is kept, unflagged.
- 1926, volunteers: sgt1926 prints 880; sgt1927-sgt1930 and sgt1935 print 261. The sgt1926
  image clearly reads 880. No check decides; the latest printing (261, sgt1935) is kept,
  unflagged.
- 1932, unfit for illness: sgt1935 prints 11.104, sgt1936 (the latest) 11.404; kept 11.404.

The columns follow no identity that could be checked: designated = incorporated +
exonerated holds for 1913-1916, 1918-1922 and 1925 only (from 1923 the designated are a
round quota).

## Validation

0 of 0 printed-total checks pass.

Common columns: `census` (source edition, e.g. `sgt1930`), `gallica_ark` (volume ark), `table_id`, `source_page` (printed page), `gallica_view`, `value`, `flag` (empty, `ocr_corrected`, `illegible`, `total_mismatch`, `derived_from_totals`, `not_applicable`, `reprint_corrected`; see `data-raw/colonial_census/SPEC.md`). A printed `»` is stored as 0. Printed totals are not stored; they were used for validation.
