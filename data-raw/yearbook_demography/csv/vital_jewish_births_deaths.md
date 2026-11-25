# Naissances et décès constatés dans la population israélite

*Jewish births and deaths recorded (état civil indigène), by contrôle civil, 1918–1939.*

Source: *Statistique générale de la Tunisie*, editions 1922–1939, chapter I *Démographie*, "Mouvement de la population". Gallica arks in `gallica_ark` (EDITIONS.md); source gallica.bnf.fr / Ministère des Affaires étrangères. Transcriptions: `../transcribed/vital_*_<edition>.txt`; rebuild: `python3 data-raw/yearbook_demography/extract_vital.py build`. Per-check output: `vital_validation.json`.

Columns as in `vital_muslim_births_deaths`, with `religion` = jewish. Common columns: `census` = the edition each value was taken from (the latest one that prints that year, per SPEC_ADDENDUM rule 4), `table_id`, `gallica_ark`, `source_page` (printed page; these volumes have no page labels in their manifests, so pages were read from the headers), `gallica_view`, `year`, `value` (count), `flag`. A printed `»` is stored as 0. Printed totals are not stored as rows.

## Method
As for the Muslim table. The OCR drops most `»` (zero) marks on these sparse pages; every page was read on the full-resolution scan.

Header misprint: the 1923 edition (view 520) heads its last column "1924"; its values are those of 1923 in every other printing, and it is stored as 1923.

## Validation
- Column totals: 122 checks; 120 pass.
- Overlapping printings: 1,638 comparisons; **0 differences**.
- The only failure is **1935 deaths**: cells sum to 964, printed total 957 (−7), identical in the 1936 and 1939 editions. No cell can be identified; unflagged.
