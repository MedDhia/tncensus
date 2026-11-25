# Opérations des Conseils de révision (recrutement français)

Source: *Statistique générale de la Tunisie*, Régence de Tunis (annual). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR). Editions and views: see `EDITIONS.md`.

*Opérations des Conseils de révision (recrutement français)*: 304 rows, conscription class (classe)s 1902-1939, one row per conscription and item.
Each value is taken from the latest transcribed edition that prints it (`census`).
Columns: `year` (conscription class (classe)), `item` (English code), `item_fr` (printed heading), `value`.

Check per class (1915 onwards): actually called = registered - exempted - neo-French not called - postponed - deferred - enlisted. The third column means *hommes qui, en raison de leur âge, n'ont pas été appelés* before 1913 and *néo-français* later; the pre-1915 classes do not follow the identity and are not checked. 1902-1903 are taken from sgt1925 (the 1926-1929 editions, which may also print them, were not transcribed). The 1924 class: sgt1935 prints 39 enlisted, sgt1925 and sgt1930 print 93, which the identity requires: 93 kept, flag `reprint_corrected`.

Rows of a class or year that fail a check are flagged `total_mismatch` (all items of that
row); the values are kept as printed.

## Editions used and compared

Transcribed: sgt1925 (1916-1925; draft boards 1902-1925), sgt1930 (1921-1930; draft
boards 1904-1930), sgt1935 (1926-1935; draft boards 1916-1935), sgt1936 (French classes
1933-1937; indigenous years 1932-1936), sgt1939 (1935-1939). Values for 1916-1920 come
from sgt1925, although the 1926-1929 editions also print some of these years; the
1922-1924 and 1926-1929 editions were not transcribed, and classes/years 1913-1915
(only in the 1922-1924 editions) are not covered, except the draft boards.

Every other transcribed printing of the same cell was compared: 168 comparisons,
167 equal, 1 different:

- 1924 enlisted_maritime: sgt1930 prints 93, sgt1935 prints 39

## Validation

42 of 46 printed-total checks pass. Failing checks (each re-read on the image at full resolution; printed values kept):

- sgt1930 1920 called = registered - exempted - neo-French - postponed - deferred - enlisted: computed 289 != printed 281
- sgt1930 1926 called = registered - exempted - neo-French - postponed - deferred - enlisted: computed 410 != printed 416
- sgt1935 1920 called = registered - exempted - neo-French - postponed - deferred - enlisted: computed 289 != printed 281
- sgt1935 1926 called = registered - exempted - neo-French - postponed - deferred - enlisted: computed 410 != printed 416

Common columns: `census` (source edition, e.g. `sgt1930`), `gallica_ark` (volume ark), `table_id`, `source_page` (printed page), `gallica_view`, `value`, `flag` (empty, `ocr_corrected`, `illegible`, `total_mismatch`, `derived_from_totals`, `not_applicable`, `reprint_corrected`; see `data-raw/colonial_census/SPEC.md`). A printed `»` is stored as 0. Printed totals are not stored; they were used for validation.
