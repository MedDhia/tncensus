# Mariages déclarés dans les contrôles civils, communes et postes d'état civil

*European marriages registered, by nationality of the groom (`spouse` = groom) and of the bride (`spouse` = bride), 1918–1939.*

Source: *Statistique générale de la Tunisie*, editions 1922–1939, chapter I *Démographie*, "Mouvement de la population". Gallica arks in `gallica_ark` (EDITIONS.md); source gallica.bnf.fr / Ministère des Affaires étrangères. Transcriptions: `../transcribed/vital_*_<edition>.txt`; rebuild: `python3 data-raw/yearbook_demography/extract_vital.py build`. Per-check output: `vital_validation.json`.

Columns: `nationality` (french, italian, maltese, greek, spanish, other_european, not_stated = "Époux dont la nationalité n'a pas été signalée"), `spouse` (groom / bride). Common columns: `census` = the edition each value was taken from (the latest one that prints that year, per SPEC_ADDENDUM rule 4), `table_id`, `gallica_ark`, `source_page` (printed page; these volumes have no page labels in their manifests, so pages were read from the headers), `gallica_view`, `year`, `value` (count), `flag`. A printed `»` is stored as 0. Printed totals are not stored as rows.

Years: 1918–1930, 1933–1936, 1938–1939. 1931–1932 and 1937 are not printed in any edition on Gallica (the 1931–1934 and 1937–1938 editions are missing).

Footnote (1922–1923 editions): the small number of marriages involving foreigners is explained by their usually marrying before their own country's representative.

## Validation
- Of 396 European checks (marriages, mixed marriages, births, deaths), 393 pass. 38 are marriage-total checks (grooms against "Totaux des mariages"); 36 pass. The printed total counts marriages, i.e. grooms. Brides of European nationality are fewer than grooms because European men marrying Jewish or Muslim Tunisian women are counted among grooms only (see `vital_mixed_marriages`).
- The two failures are misprinted totals corrected in the next edition. Totals are not stored as data, so no value is affected: 1921 printed 1.107 in the 1922 edition (grooms + brides), 558 from 1923 on; 1927 printed 1.068 in the 1927 edition, 534 in 1928.
- Overlapping printings: 574 comparisons across the European tables (cells and totals of every year printed in two or more editions); the only 2 differences are the two corrected marriage totals above. Every cell agrees.
