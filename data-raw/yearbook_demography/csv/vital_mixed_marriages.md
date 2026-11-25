# Relevé par nationalité des mariages entre européens et indigènes (tunisiens)

*Marriages between Europeans and indigenous Tunisians, by group of the groom and of the bride, for the edition year.*

Source: *Statistique générale de la Tunisie*, editions 1922–1939, chapter I *Démographie*, "Mouvement de la population". Gallica arks in `gallica_ark` (EDITIONS.md); source gallica.bnf.fr / Ministère des Affaires étrangères. Transcriptions: `../transcribed/vital_*_<edition>.txt`; rebuild: `python3 data-raw/yearbook_demography/extract_vital.py build`. Per-check output: `vital_validation.json`.

Columns: `groom_group` (french, italian, maltese, other_foreign = "Etrangers autres", muslim, jewish), `bride_group` (muslim, jewish for European grooms; french, italian, maltese, other_foreign for Muslim and Jewish grooms). Combinations the table leaves blank are not stored; `»` is 0. Common columns: `census` = the edition each value was taken from (the latest one that prints that year, per SPEC_ADDENDUM rule 4), `table_id`, `gallica_ark`, `source_page` (printed page; these volumes have no page labels in their manifests, so pages were read from the headers), `gallica_view`, `year`, `value` (count), `flag`. A printed `»` is stored as 0. Printed totals are not stored as rows.

Each edition prints this table for its own last year only: 1922–1930, 1934, 1936, 1939. From 1936 the title reads "entre européens et tunisiens".

## Validation
For each edition: the European grooms' column totals and the indigenous grooms' column totals against their printed totals, and each row's number against the sum of its brides' columns. All pass.
