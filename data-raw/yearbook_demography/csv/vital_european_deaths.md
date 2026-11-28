# Décès déclarés dans les contrôles civils, communes et postes d'état civil

*European deaths registered, by nationality and sex, 1918–1939.*

Source: *Statistique générale de la Tunisie*, editions 1922–1939, chapter I *Démographie*, "Mouvement de la population". Gallica arks in `gallica_ark` (EDITIONS.md); source gallica.bnf.fr / Ministère des Affaires étrangères. Transcriptions: `../transcribed/vital_*_<edition>.txt`; rebuild: `python3 data-raw/yearbook_demography/extract_vital.py build`. Per-check output: `vital_validation.json`.

Columns as in `vital_european_births`. Common columns: `census` = the edition each value was taken from (the latest one that prints that year, per SPEC_ADDENDUM rule 4), `table_id`, `gallica_ark`, `source_page` (printed page; these volumes have no page labels in their manifests, so pages were read from the headers), `gallica_view`, `year`, `value` (count), `flag`. A printed `»` is stored as 0. Printed totals are not stored as rows.

Note: the 1918 and 1919 "Autres Européens" male deaths (368, 130) are high compared with later years; they are printed so in the 1922 and 1923 editions (wartime and post-war years).

## Validation
Every sex column matches its printed subtotal and every male + female sum matches the printed total, in every edition. Overlapping printings agree on every cell.
