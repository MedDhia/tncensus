# Forêts. b) Produits forestiers (bois, écorces à tan, lièges)

*Forests: forest products sold, by adjudication or private sale (wood, tan bark, pit props, poles, cork).*

Source: *Statistique générale de la Tunisie*, chapter *Agriculture*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 230, f254; sgt1923 (`bpt6k9105649x`): p. 242, f744; sgt1924 (`bpt6k9105649x`): p. 256, f1246; sgt1925 (`bpt6k9105650k`): p. 284, f308; sgt1926 (`bpt6k9105650k`): p. 254, f818; sgt1927 (`bpt6k91056510`): p. 253, f281; sgt1928 (`bpt6k91056510`): p. 253, f805; sgt1929 (`bpt6k9105652d`): p. 255, f283; sgt1930 (`bpt6k9105652d`): p. 259, f817; sgt1935 (`bpt6k9105653t`): p. 133, f153; sgt1936 (`bpt6k91056547`): p. 104, f115; sgt1939 (`bpt6k9105739w`): p. 108, f114.

Transcriptions: `../transcribed/agriculture_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_agriculture.py build`.

Rows: 455. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939.

Units: cubic metres, steres, quintals, linear metres, count (`unit`); value_type: quantity.

Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept; `year` = edition year.

## Columns

- `census`: edition the value is taken from (rule 4 series: the latest edition printing that year; rule 5 tables: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: edition year (the sales listed are mostly of that year; sgt1922 and sgt1923 also list earlier sales whose payments fall in the year, see the footnotes in `sale_fr`)
- `sale_no`: order of the sale line on the page
- `sale_fr`: printed line heading (date and kind of sale, footnote calls kept), as printed
- `product`: product code (English)
- `product_fr`: printed column heading
- `unit`: unit of `value` as printed under the heading (`cubic_metres`, `steres`, `quintals`, `linear_metres`, `count`), or `not_printed` (sgt1935-sgt1939 leave some units blank); never converted
- `unit_fr`: unit as printed (empty: none printed)
- `value`: printed value (» = 0)
- `flag`: empty (no cell flagged)

Printed in every edition (sgt1922-sgt1930: b) on the page after a); sgt1935-sgt1939: under the domain table), one line per adjudication or marché de gré à gré, seven product columns: bois d'industrie (m.c.), bois de chauffage (stères; printed q. in sgt1935-sgt1936, st. in sgt1939), écorces à tan (quint.), étais de mine (mètres linéaires), perches (unités), lièges de reproduction and liège mâle (quint.). Rule 5: each edition kept; » = 0. The TOTAL / TOTAUX lines (sgt1922-sgt1930) are checks only; sgt1935-sgt1939 print none.

Read as printed: sgt1923 prints the 7 juin 1923 bois d'industrie "183.58" with its thousands point misplaced; the TOTAL 27.283 needs 18.358 (stored 18358). sgt1927 prints a liège de reproduction of 14,50 quintals (TOTAUX 33.164,50). sgt1936 prints 240.172 in the écorces column of the first line (no unit printed there; it is of the order of the étais de mine of the other years, but stored where printed).

c) Rendement en argent: `agriculture_forest_revenue`; d) Poursuites des délits and e) Incendies (sgt1922-sgt1927): `agriculture_forest_offences_fires`.

Every failed check below was re-read on a zoomed native-resolution crop: they are printed inconsistencies (printed values kept). sgt1924 bois de chauffage: the lines (13.804 + 10.937 + 28.800 + 9.100) give 62.641, the TOTAL prints 62.637; every cell re-read on a zoomed crop, no line identifiable (kept unflagged).

Survey of the whole chapter in every edition: `agriculture_survey.md`.

## Validation

- Checks against printed totals and identities: 63; passed: 62; failed: 1.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1924 p.256 (f1246) forest_b fuel: lines vs Total: cells give 62641, printed 62637 (difference -4)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (12 printings): sgt1922 f254, sgt1923 f744, sgt1924 f1246, sgt1925 f308, sgt1926 f818, sgt1927 f281, sgt1928 f805, sgt1929 f283, sgt1930 f817, sgt1935 f153, sgt1936 f115, sgt1939 f114.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
