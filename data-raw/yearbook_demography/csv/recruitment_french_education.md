# Degré d'instruction des jeunes gens recrutés (recrutement français)

Source: *Statistique générale de la Tunisie*, Régence de Tunis (annual). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR). Editions and views: see `EDITIONS.md`.

*Degré d'instruction des jeunes gens recrutés (recrutement français)*: 168 rows, conscription class (classe)s 1916-1939, one row per conscription and item.
Each value is taken from the latest transcribed edition that prints it (`census`).
Columns: `year` (conscription class (classe)), `item` (English code), `item_fr` (printed heading), `value`.

Check per class: the seven categories sum to the printed total (printed totals are the registered men, or from 1933 the remaining men, of the allocation table).

Rows of a class or year that fail a check are flagged `total_mismatch` (all items of that
row); the values are kept as printed.

## Editions used and compared

Transcribed: sgt1925 (1916-1925; draft boards 1902-1925), sgt1930 (1921-1930; draft
boards 1904-1930), sgt1935 (1926-1935; draft boards 1916-1935), sgt1936 (French classes
1933-1937; indigenous years 1932-1936), sgt1939 (1935-1939). Values for 1916-1920 come
from sgt1925, although the 1926-1929 editions also print some of these years; the
1922-1924 and 1926-1929 editions were not transcribed, and classes/years 1913-1915
(only in the 1922-1924 editions) are not covered, except the draft boards.

Every other transcribed printing of the same cell was compared: 112 comparisons,
112 equal, 0 different:

## Validation

38 of 40 printed-total checks pass. Failing checks (each re-read on the image at full resolution; printed values kept):

- sgt1925 1924 row total: computed 792 != printed 791
- sgt1930 1924 row total: computed 792 != printed 791

Common columns: `census` (source edition, e.g. `sgt1930`), `gallica_ark` (volume ark), `table_id`, `source_page` (printed page), `gallica_view`, `value`, `flag` (empty, `ocr_corrected`, `illegible`, `total_mismatch`, `derived_from_totals`, `not_applicable`, `reprint_corrected`; see `data-raw/colonial_census/SPEC.md`). A printed `»` is stored as 0. Printed totals are not stored; they were used for validation.
