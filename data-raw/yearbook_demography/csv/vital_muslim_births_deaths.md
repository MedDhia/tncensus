# Naissances et décès constatés dans la population musulmane

*Muslim births and deaths recorded (état civil indigène), by contrôle civil, 1918–1939.*

Source: *Statistique générale de la Tunisie*, editions 1922–1939, chapter I *Démographie*, "Mouvement de la population". Gallica arks in `gallica_ark` (EDITIONS.md); source gallica.bnf.fr / Ministère des Affaires étrangères. Transcriptions: `../transcribed/vital_*_<edition>.txt`; rebuild: `python3 data-raw/yearbook_demography/extract_vital.py build`. Per-check output: `vital_validation.json`.

Columns: `controle_civil` (20 units as printed: 19 contrôles civils plus `Territoires du Sud`; `Kef` is printed `Kef (Le)` in some editions), `religion` = muslim, `event` = births / deaths. Common columns: `census` = the edition each value was taken from (the latest one that prints that year, per SPEC_ADDENDUM rule 4), `table_id`, `gallica_ark`, `source_page` (printed page; these volumes have no page labels in their manifests, so pages were read from the headers), `gallica_view`, `year`, `value` (count), `flag`. A printed `»` is stored as 0. Printed totals are not stored as rows.

Each edition prints a 5-year window (6 in 1923): 1918–22, 1918–23, 1920–24, 1921–25, 1922–26, 1923–27, 1924–28, 1925–29, 1926–30, 1930–34, 1932–36, 1935–39. Every year 1918–1939 is covered; geography is the same 20 units throughout.

## Method
OCR word positions (Gallica) gave a first draft; every page was then read on the full-resolution scan (IIIF region requests at native size) and every cell that the OCR missed or that disagreed with another printing was set from the image. Values the OCR misread (dropped leading digits, `»` lost) were corrected silently in the transcriptions, since the image is the source of truth.

## Validation
- Column totals: 122 checks (each year × births/deaths column of every edition against its printed TOTAUX); 90 pass.
- Overlapping printings: 1,638 cell and total comparisons between editions printing the same year; **0 differences**. Every cell and every printed total is identical in all printings, so the 32 failing column checks are 12 distinct printing errors, repeated in each reprint:

| Year | Event | Cells sum to | Printed total | Difference |
|---|---|---:|---:|---:|
| 1920 | deaths | 29.375 | 29.381 | −6 |
| 1923 | deaths | 31.956 | 32.556 | −600 |
| 1924 | deaths | 38.390 | 39.393 | −1.003 |
| 1927 | births | 52.551 | 52.571 | −20 |
| 1929 | births | 54.045 | 59.121 | −5.076 |
| 1929 | deaths | 33.404 | 33.384 | +20 |
| 1932 | births | 62.071 | 61.951 | +120 |
| 1934 | deaths | 38.261 | 38.870 | −609 |
| 1935 | births | 66.476 | 65.477 | +999 |
| 1935 | deaths | 32.703 | 33.123 | −420 |
| 1936 | births | 80.829 | 77.829 | +3.000 |
| 1938 | births | 65.979 | 65.679 | +300 |

Two of these are evidently misprinted cells and are flagged `total_mismatch` (printed value kept): **Territoires du Sud 1929 births**, printed 564 (5.640 closes the gap exactly; 1928: 5.399, 1930: 6.211); **Medjez-el-Bab 1936 births**, printed 4.741 (1.741 closes the gap exactly; 1935: 1.296, 1937: 1.451). The others cannot be assigned to a cell and are left unflagged: sums over contrôles differ from the printed national total in those years.
