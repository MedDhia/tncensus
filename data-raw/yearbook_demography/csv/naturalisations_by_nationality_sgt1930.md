# Naturalisations by nationality, legal basis and year (sgt1930 printing, table e)

Source: *Statistique générale de la Tunisie*, Régence de Tunis (annual). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR). Editions and views: see `EDITIONS.md`.

Table e) *Naturalisations accordées (1891-1930)*, as printed in the 1930 edition
(pp. 24-25): 729 rows, 27 nationalities. Columns `period` (a year, or
a range printed as one column), `legal_basis` (the decree or law the naturalisations were
granted under, as printed above each column group), `age_group` (`adults` = majeurs,
`minors` = mineurs, `total` where only a total is printed), `nationality`.

This is the last edition with the adults/minors split and the per-year columns for
1921-1930. Later editions (1935, 1936, 1939) regroup the early years and drop the split;
the 1939 printing is in `naturalisations_by_nationality_sgt1939.csv`.

Misprints confirmed on the scan:

- *Indigènes catholiques* and *Divers* both print 3 (1891-1898) and 3 / 2 (1899-1910
  adults / minors), and the printed totals (296, 733, 639) only add up with one of them.
  The 1924 edition prints these figures once (as *Musulmans marocains*, with no
  *Indigènes catholiques* row), and the 1935 and 1936 editions keep them under *Divers*
  (3 and 5). The three *Indigènes catholiques* cells are set to 0 (`reprint_corrected`);
  the totals then check.
- 1925 minors: the cells sum to 1.726, printed total 1.736; the year total (3.298) and
  table a (1.726 minors) confirm the cells.
- 1929 adults: the cells sum to 1.348, printed total 1.345; the year total (2.636) and
  table a agree with 1.345, so one cell is printed 3 too high; it cannot be identified.
- The 1922 minors column runs into the binding; it was read from the visible digits and
  checks against the printed total (283).

## Comparison with the other printings

- **sgt1924, cell by cell** (1891-1924, the first fifteen columns): 405
  cells compared, 405 equal, 0 different:


  (sgt1924's *Musulmans marocains* matched with this file's *Divers*; with the
  *Indigènes catholiques* correction above, every cell agrees.)
- **sgt1922, sgt1923, sgt1925-sgt1929, printed totals** (each period and year, adults
  and minors): all equal to this file's printed totals, with one exception. The 1925
  minors total is printed 1.726 in the 1925-1928 editions and 1.736 in the 1929 and 1930
  editions; 1.726 is right (it is the sum of the cells and table a's figure). Totals are
  not stored, so no value changes.
- **sgt1929, 1929 column, cell by cell:** identical to this file, including the adults
  that sum to 1.348 against a printed 1.345. No printing locates the cell that is 3 too
  high.
- The 1922-1923 and 1925-1929 printings were compared at the level of their printed
  totals only, not cell by cell.

## Validation

54 of 58 printed-total checks pass. Failing checks (each re-read on the image at full resolution; printed values kept):

- sgt1930 1925 minors column total: computed 1726 != printed 1736
- sgt1930 1929 adults column total: computed 1348 != printed 1345
- sgt1939 1935 total column total: computed 668 != printed 686
- sgt1939 1938 total column total: computed 1268 != printed 1278

Common columns: `census` (source edition, e.g. `sgt1930`), `gallica_ark` (volume ark), `table_id`, `source_page` (printed page), `gallica_view`, `value`, `flag` (empty, `ocr_corrected`, `illegible`, `total_mismatch`, `derived_from_totals`, `not_applicable`, `reprint_corrected`; see `data-raw/colonial_census/SPEC.md`). A printed `»` is stored as 0. Printed totals are not stored; they were used for validation.
