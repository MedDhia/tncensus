# Service botanique et agronomique. b) Ventes d'arbres et de plantes diverses

*Botanical and agronomic service: sales of fruit trees (plants and grafts) and other plants, by species and season.*

Source: *Statistique générale de la Tunisie*, chapter *Institutions d'enseignement et de recherches*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 255, f279; sgt1923 (`bpt6k9105649x`): p. 268, f770; sgt1924 (`bpt6k9105649x`): p. 284, f1274; sgt1925 (`bpt6k9105650k`): p. 316, f340; sgt1926 (`bpt6k9105650k`): p. 286, f850; sgt1927 (`bpt6k91056510`): p. 284, f312; sgt1928 (`bpt6k91056510`): p. 288, f840; sgt1929 (`bpt6k9105652d`): p. 289, f317; sgt1930 (`bpt6k9105652d`): p. 296, f854; sgt1935 (`bpt6k9105653t`): p. 143, f163.

Transcriptions: `../transcribed/research_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_research.py build`.

Rows: 666. Years: 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935.

Unit: plants or grafts (count); value_type: count.

Selection (SPEC_ADDENDUM rule 4): each cell is stored once, from the latest edition printing it; every other printing of the same cell is compared below.

## Columns

- `census`: source edition (`sgt1922` ... `sgt1939`)
- `table_id`: section code of the transcription
- `gallica_ark`: Gallica volume ark
- `source_page`: printed page number
- `gallica_view`: Gallica view
- `year`: year of the figure (for a school year or season: the year it ends; for promotions and once-per-edition tables: the edition year)
- `group`: group heading (ASCII slug of `group_fr`)
- `group_fr`: group heading as printed
- `season`: season (année) as printed
- `species`: species as printed
- `measure`: what is counted
- `measure_fr`: column heading as printed
- `unit`: unit of the line (francs, persons, analyses, doses, flacons, cc, tubes, ampoules, litres, samples, quintals, hectares, producers, count)
- `value`: printed figure (» = 0)
- `flag`: empty, or ocr_corrected / illegible / total_mismatch / derived_from_totals / not_applicable / reprint_corrected / row_realigned

The cumulative deliveries printed under the table (livraisons of the five seasons, antérieures since 1893, total général) are checks only; the antérieures figures are reported in the validation file.

Every failed check below was re-read on a zoomed native-resolution crop: they are printed inconsistencies (printed values kept). sgt1927: the greffons of 1926-27 add up to 676 against a printed total of 726 (and the livraisons 3.171 use 726); the faulty species cell cannot be identified. sgt1927 cumulative plants: livraisons printed 29.662 whereas the season totals give 29.462 and the Total général 371.270 = 29.462 + 341.808, so the livraisons figure is misprinted; greffons: the livraisons antérieures are misprinted 283.047 for 183.047 (Total général 186.218 = 3.171 + 183.047; likewise sgt1924 Total général 285.055 for 185.055): printed. All re-read on zoomed crops. sgt1928 repeats the 726; sgt1929 and sgt1930 print 676 but their livraisons (2.828, 6.008) still include the 50. sgt1928-sgt1930: the plants livraisons exceed the season totals by 3.943 in each edition (printed). sgt1929 and sgt1930 print Abricotier 1927-28 plants 57 for 572 (column total 5.181): flagged total_mismatch, the cell kept from sgt1928 (reprint_corrected).

Survey of the whole chapter in every edition: `research_survey.md`.

## Validation

- Checks against printed totals and identities: 160; passed: 141; failed: 19.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1924 p.284 (f1274) bot_trees_cum [fruit] grafts: total général = livraisons + antérieures: cells give 185055, printed 285055 (difference 100000)
  - sgt1927 p.284 (f312) bot_trees_cum [fruit] plants: total général = livraisons + antérieures: cells give 371470, printed 371270 (difference -200)
  - sgt1927 p.284 (f312) bot_trees_cum [fruit] grafts: total général = livraisons + antérieures: cells give 286218, printed 186218 (difference -100000)
  - sgt1927 p.284 (f312) bot_trees_cum [fruit] plants: livraisons vs sum of season totals: cells give 29462, printed 29662 (difference 200)
  - sgt1928 p.288 (f840) bot_trees_cum [fruit] plants: livraisons vs sum of season totals: cells give 30181, printed 34124 (difference 3943)
  - sgt1929 p.289 (f317) bot_trees_cum [fruit] plants: livraisons vs sum of season totals: cells give 27465, printed 31408 (difference 3943)
  - sgt1929 p.289 (f317) bot_trees_cum [fruit] grafts: livraisons vs sum of season totals: cells give 2778, printed 2828 (difference 50)
  - sgt1930 p.296 (f854) bot_trees_cum [fruit] plants: livraisons vs sum of season totals: cells give 28304, printed 32247 (difference 3943)
  - sgt1930 p.296 (f854) bot_trees_cum [fruit] grafts: livraisons vs sum of season totals: cells give 5958, printed 6008 (difference 50)
  - sgt1935 p.143 (f163) bot_trees_cum [fruit] plants: livraisons vs sum of season totals: cells give 25267, printed 25067 (difference -200)
  - sgt1935 p.143 (f163) bot_trees_cum [fruit] grafts: livraisons vs sum of season totals: cells give 3639, printed 7196 (difference 3557)
  - sgt1922 p.255 (f279) bot_trees 1922p: lines vs Total: cells give 4623, printed 4183 (difference -440)
  - sgt1923 p.268 (f770) bot_trees 1922p: lines vs Total: cells give 4623, printed 4183 (difference -440)
  - sgt1924 p.284 (f1274) bot_trees 1922p: lines vs Total: cells give 4623, printed 4183 (difference -440)
  - sgt1927 p.284 (f312) bot_trees 1927g: lines vs Total: cells give 676, printed 726 (difference 50)
  - sgt1928 p.288 (f840) bot_trees 1927g: lines vs Total: cells give 676, printed 726 (difference 50)
  - sgt1929 p.289 (f317) bot_trees 1928p: lines vs Total: cells give 4666, printed 5181 (difference 515)
  - sgt1930 p.296 (f854) bot_trees 1928p: lines vs Total: cells give 4666, printed 5181 (difference 515)
  - sgt1935 p.143 (f163) bot_trees 1931p: lines vs Total: cells give 5308, printed 5306 (difference -2)

- Overlapping printings: 1184 cell comparisons with other editions printing the same cell; 4 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1921-22 / fruit / Poirier / plants | sgt1922 | 1445 | sgt1926 | 1005 |
| 1921-22 / fruit / Poirier / plants | sgt1923 | 1445 | sgt1926 | 1005 |
| 1921-22 / fruit / Poirier / plants | sgt1924 | 1445 | sgt1926 | 1005 |
| 1927-28 / fruit / Abricotier / plants | sgt1928 | 572 | sgt1930 | 57 |

- Flagged cells: reprint_corrected: 1.

  - sgt1928 p.288 1928 fruit / 1927-28 / Abricotier / plants / count = 572 (reprint_corrected)

## Image versus OCR

- Read cell by cell on the page images (20 printings): sgt1922 f279, sgt1922 f279, sgt1923 f770, sgt1923 f770, sgt1924 f1274, sgt1924 f1274, sgt1925 f340, sgt1925 f340, sgt1926 f850, sgt1926 f850, sgt1927 f312, sgt1927 f312, sgt1928 f840, sgt1928 f840, sgt1929 f317, sgt1929 f317, sgt1930 f854, sgt1930 f854, sgt1935 f163, sgt1935 f163.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
