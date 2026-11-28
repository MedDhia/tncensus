# Naissances déclarées dans les contrôles civils, communes et postes d'état civil

*European births registered, by nationality and sex, 1918–1939.*

Source: *Statistique générale de la Tunisie*, editions 1922–1939, chapter I *Démographie*, "Mouvement de la population". Gallica arks in `gallica_ark` (EDITIONS.md); source gallica.bnf.fr / Ministère des Affaires étrangères. Transcriptions: `../transcribed/vital_*_<edition>.txt`; rebuild: `python3 data-raw/yearbook_demography/extract_vital.py build`. Per-check output: `vital_validation.json`.

Columns: `nationality` (french, italian, maltese, greek, spanish, other_european), `sex` (male = S. M., female = S. F.). Common columns: `census` = the edition each value was taken from (the latest one that prints that year, per SPEC_ADDENDUM rule 4), `table_id`, `gallica_ark`, `source_page` (printed page; these volumes have no page labels in their manifests, so pages were read from the headers), `gallica_view`, `year`, `value` (count), `flag`. A printed `»` is stored as 0. Printed totals are not stored as rows.

Years: 1918–1930, 1933–1936, 1938–1939 (see the marriages notes for the gaps).

## Validation
Per edition and year: each sex column against its printed subtotal, and male + female against "Totaux des sexes réunis". All pass except **1933 male**: cells sum to 3.262, printed subtotal 3.362 (and 6.370 = 3.362 + 3.008 for both sexes). The cells were re-read on the scan; 1933 is printed only in the 1935 edition, so no reprint can settle it, and the cells are kept unflagged. Overlapping printings agree on every cell.
