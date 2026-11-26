# Conservation foncière. Titres délivrés : nombre, contenances et valeurs définitives

*Land registry: land titles issued (total, from subdivisions, after a registration judgment, with final area and value), by year.*

Source: *Statistique générale de la Tunisie*, chapter *Propriété immobilière / Tribunal mixte / Propriété foncière*, editions sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1930 (`bpt6k9105652d`): p. 112, f670; sgt1935 (`bpt6k9105653t`): p. 77, f97; sgt1936 (`bpt6k91056547`): p. 56, f67; sgt1939 (`bpt6k9105739w`): p. 56, f62.

Transcriptions: `../transcribed/property_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_property.py build`.

Rows: 160. Years: 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Units: titles (`count`), hectares as a decimal with four places (`hectares`; printed h. a. c.), francs (`francs`). Mixed table.

Printed for overlapping year windows: each year (and the opening multi-year period) is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing is compared below. Each single year is printed by every edition from its own year to sgt1930 (up to nine printings, 1910-1930); 1931 and 1932 are printed only inside the opening periods; 1933-1936 are printed by one to three of sgt1935, sgt1936 and sgt1939, 1937-1939 by sgt1939 only; the opening multi-year periods differ between edition groups and are each stored once.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: `titles`
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures; empty for the opening multi-year period
- `period`: year, or the opening multi-year period as printed
- `period_fr`: as printed
- `measure`: `total_titles`, `subdivision` (titres provenant de lotissements), `judgment` (titles issued after a registration judgment), `area` (their final area), `value` (their final value)
- `measure_fr`: printed column heading
- `unit`: `count`, `hectares` or `francs`
- `value`: titles, hectares or francs
- `flag`: empty, or `total_mismatch` (printed value kept), `derived_from_totals`, `row_realigned`, `not_applicable` (nothing printed)

Periods as in property_requisitions (overlapping opening periods). Areas in hectares with four decimals.

Identity total = lotissements + jugement fails on three lines printed alike by every edition sgt1922-sgt1930 (re-read on crops): 1886-1909 15.171 for 6.514 + 8.654 = 15.168, 1910 922 for 571 + 363 = 934, 1912 1.126 for 715 + 402 = 1.117 (the errors cancel out in the Totaux); and on the sgt1939 Totaux line (53.778 for 34.409 + 19.349; with the lines' 19.369 it holds).

Failed checks: sgt1924 Totaux valeur printed 232.114.176 for lines summing to 222.114.176 (the récapitulation prints 222.114.176); sgt1935 1886-1932 printed 1.398.823 02 59 ha and 359.173.670 fr., where the Totaux need 1.389.922 46 58 and 383.173.670 (sgt1936's 1886-1933 figures equal these plus 1933); sgt1939 Totaux titres délivrés en suite d'un jugement printed 19.349 for lines summing to 19.369 (the récapitulation prints 19.369), valeur 621.233.714 for lines summing to 621.234.214.

Flagged cells: sgt1935 titles 1886-1932 / area: printed 1.398.823 02 59 ha; the Totaux (1.449.008 42 15) need 1.389.922 46 58, which is also sgt1936's 1886-1933 (1.399.899 11 41) less 1933 (9.976 64 83); printed value kept; sgt1935 titles 1886-1932 / value: printed 359.173.670 fr.; the Totaux (513.080.640) need 383.173.670, which is also sgt1936's 1886-1933 (413.337.722) less 1933 (30.164.052); printed value kept; sgt1936 titles 1886-1933 / area: ares and centiares printed "1· 11"; 11 a 41 c from the Totaux 1.474.945 22 57.

Survey of the whole chapter in every edition: `property_survey.md`.

Overlap comparison: every printing of sgt1922-sgt1930 (and of sgt1935, sgt1936) was read independently on its own page image. The single years 1910-1930 are printed from the same standing type in every edition (the 1924 value "17.872 50" and the Tunisians 450 recur unchanged), so the printings agree cell for cell; the only differences between editions lie in the opening multi-year periods, which are distinct periods (1886-1909, 1886-1932, 1886-1933, 1886-1934) and are stored separately.

## Validation

- Checks against printed totals and identities: 248; passed: 215; failed: 33.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.87 (f111) titles 1886-1909: total_titles = subdivision + judgment: cells give 15168, printed 15171 (difference 3)
  - sgt1922 p.87 (f111) titles 1910: total_titles = subdivision + judgment: cells give 934, printed 922 (difference -12)
  - sgt1922 p.87 (f111) titles 1912: total_titles = subdivision + judgment: cells give 1117, printed 1126 (difference 9)
  - sgt1923 p.93 (f595) titles 1886-1909: total_titles = subdivision + judgment: cells give 15168, printed 15171 (difference 3)
  - sgt1923 p.93 (f595) titles 1910: total_titles = subdivision + judgment: cells give 934, printed 922 (difference -12)
  - sgt1923 p.93 (f595) titles 1912: total_titles = subdivision + judgment: cells give 1117, printed 1126 (difference 9)
  - sgt1924 p.95 (f1085) titles 1886-1909: total_titles = subdivision + judgment: cells give 15168, printed 15171 (difference 3)
  - sgt1924 p.95 (f1085) titles 1910: total_titles = subdivision + judgment: cells give 934, printed 922 (difference -12)
  - sgt1924 p.95 (f1085) titles 1912: total_titles = subdivision + judgment: cells give 1117, printed 1126 (difference 9)
  - sgt1924 p.95 (f1085) titles value: lines vs Totaux: cells give 222114176, printed 232114176 (difference 10000000)
  - sgt1925 p.97 (f121) titles 1886-1909: total_titles = subdivision + judgment: cells give 15168, printed 15171 (difference 3)
  - sgt1925 p.97 (f121) titles 1910: total_titles = subdivision + judgment: cells give 934, printed 922 (difference -12)
  - sgt1925 p.97 (f121) titles 1912: total_titles = subdivision + judgment: cells give 1117, printed 1126 (difference 9)
  - sgt1926 p.108 (f672) titles 1886-1909: total_titles = subdivision + judgment: cells give 15168, printed 15171 (difference 3)
  - sgt1926 p.108 (f672) titles 1910: total_titles = subdivision + judgment: cells give 934, printed 922 (difference -12)
  - sgt1926 p.108 (f672) titles 1912: total_titles = subdivision + judgment: cells give 1117, printed 1126 (difference 9)
  - sgt1927 p.106 (f134) titles 1886-1909: total_titles = subdivision + judgment: cells give 15168, printed 15171 (difference 3)
  - sgt1927 p.106 (f134) titles 1910: total_titles = subdivision + judgment: cells give 934, printed 922 (difference -12)
  - sgt1927 p.106 (f134) titles 1912: total_titles = subdivision + judgment: cells give 1117, printed 1126 (difference 9)
  - sgt1928 p.106 (f658) titles 1886-1909: total_titles = subdivision + judgment: cells give 15168, printed 15171 (difference 3)
  - sgt1928 p.106 (f658) titles 1910: total_titles = subdivision + judgment: cells give 934, printed 922 (difference -12)
  - sgt1928 p.106 (f658) titles 1912: total_titles = subdivision + judgment: cells give 1117, printed 1126 (difference 9)
  - sgt1929 p.108 (f136) titles 1886-1909: total_titles = subdivision + judgment: cells give 15168, printed 15171 (difference 3)
  - sgt1929 p.108 (f136) titles 1910: total_titles = subdivision + judgment: cells give 934, printed 922 (difference -12)
  - sgt1929 p.108 (f136) titles 1912: total_titles = subdivision + judgment: cells give 1117, printed 1126 (difference 9)
  - sgt1930 p.112 (f670) titles 1886-1909: total_titles = subdivision + judgment: cells give 15168, printed 15171 (difference 3)
  - sgt1930 p.112 (f670) titles 1910: total_titles = subdivision + judgment: cells give 934, printed 922 (difference -12)
  - sgt1930 p.112 (f670) titles 1912: total_titles = subdivision + judgment: cells give 1117, printed 1126 (difference 9)
  - sgt1935 p.77 (f97) titles area: lines vs Totaux: cells give 1457908.9816, printed 1449008.4215 (difference -8900.5601)
  - sgt1935 p.77 (f97) titles value: lines vs Totaux: cells give 489080640, printed 513080640 (difference 24000000)
  - sgt1939 p.56 (f62) titles Totaux: total_titles = subdivision + judgment: cells give 53758, printed 53778 (difference 20)
  - sgt1939 p.56 (f62) titles judgment: lines vs Totaux: cells give 19369, printed 19349 (difference -20)
  - sgt1939 p.56 (f62) titles value: lines vs Totaux: cells give 621234214, printed 621233714 (difference -500)

- Overlapping printings: 720 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: derived_from_totals: 1, total_mismatch: 2.

  - sgt1935 p.77 None 1886-1932 / area / hectares = 1398823.0259 (total_mismatch)
  - sgt1935 p.77 None 1886-1932 / value / francs = 359173670 (total_mismatch)
  - sgt1936 p.56 None 1886-1933 / area / hectares = 1399899.1141 (derived_from_totals)

## Image versus OCR

- Read cell by cell on the page images (12 printings): sgt1922 f111, sgt1923 f595, sgt1924 f1085, sgt1925 f121, sgt1926 f672, sgt1927 f134, sgt1928 f658, sgt1929 f136, sgt1930 f670, sgt1935 f97, sgt1936 f67, sgt1939 f62.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
