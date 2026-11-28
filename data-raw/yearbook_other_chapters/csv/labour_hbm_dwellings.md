# Habitations à bon marché. a) Logements construits

*Low-cost housing (habitations à bon marché): dwellings built, by period and type.*

Source: *Statistique générale de la Tunisie*, chapter *Travail et prévoyance sociale*, editions sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1939 (`bpt6k9105739w`): p. 159, f165.

Transcriptions: `../transcribed/labour_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_labour.py build`.

Rows: 90. Years: 1920, 1921, 1922, 1923, 1924, 1926, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Unit: dwellings; value_type: count.

Printed for overlapping periods whose grouping changes between editions (single years, bracketed pairs, '1912 à 1919' / '1912 à 1920'): within each measure and housing type a printing is kept unless a later edition prints any year of its period (SPEC_ADDENDUM rule 4 applied to periods; `census` = that edition); printings of the identical period are compared below.

## Columns

- `census`: edition the value is taken from (rule 4 series: the latest edition printing it; rule 5: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (two-page spreads: the page the cell is printed on)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (HBM: last year of the printed period)
- `year_from`: first year of the printed period
- `period_fr`: period as printed
- `housing_type`: type of dwelling (English code)
- `housing_type_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, ocr_corrected, illegible, total_mismatch, derived_from_totals, not_applicable, reprint_corrected or row_realigned

Printed sgt1927-sgt1939 (headed 1912-<edition year>; sgt1935 and sgt1936 stop at 1934, sgt1939 at 1939). Columns: maisons individuelles; maisons collectives (number of dwellings); from sgt1929 logements ouvriers and logements militaires; from sgt1935 logements maritimes. The Totaux line and the Total général (sum of the Totaux) are checks only. sgt1927 prints the early years one by one (1912, 1914, 1917, 1919), later editions as '1912 à 1919' or '1912 à 1920'. Observations column: sgt1927-sgt1929 'En cours d'adjudication (ou de construction)' on the edition year; sgt1930 a list of projects under award (`labour_hbm_pending`).

sgt1939 prints the 1925-1927 bracket with 104 and 204 on the line 1928; stored on 1925-1926 and 1927-1928 as in every earlier edition (`row_realigned`).

Every failed check below was re-read on a zoomed native-resolution crop (or recurs unchanged in independent readings of several editions): printed values are kept. sgt1930 prints the logements ouvriers Totaux 395 for lines giving 305 (its own Total général 1.826 = 1.201 + 114 + 305 + 206, so the 395 is the misprint).

Survey of the whole chapter in every edition: `labour_survey.md`.

## Validation

- Checks against printed totals and identities: 31; passed: 29; failed: 2.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1930 p.489 (f1047) hbm_built workers: lines vs Totaux: cells give 305, printed 395 (difference 90)
  - sgt1930 p.489 (f1047) hbm_built Total général = sum of the Totaux indiv+coll+workers+military: cells give 1916, printed 1826 (difference -90)

- Overlapping printings: 218 cell comparisons with other editions printing the same cell; 4 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| individual / 1927-1928 | sgt1928 | 145 | sgt1939 | 204 |
| individual / 1929 | sgt1929 | 253 | sgt1939 | 291 |
| workers / 1929 | sgt1929 | 235 | sgt1939 | 301 |
| military / 1929 | sgt1929 | 206 | sgt1939 | 0 |

- Flagged cells: row_realigned: 10.

  - sgt1939 p.159 1926 1925 / individual / dwellings = 104 (row_realigned)
  - sgt1939 p.159 1926 1925 / collective / dwellings = 0 (row_realigned)
  - sgt1939 p.159 1926 1925 / workers / dwellings = 0 (row_realigned)
  - sgt1939 p.159 1926 1925 / military / dwellings = 0 (row_realigned)
  - sgt1939 p.159 1926 1925 / maritime / dwellings = 0 (row_realigned)
  - sgt1939 p.159 1928 1927 / individual / dwellings = 204 (row_realigned)
  - sgt1939 p.159 1928 1927 / collective / dwellings = 0 (row_realigned)
  - sgt1939 p.159 1928 1927 / workers / dwellings = 0 (row_realigned)
  - sgt1939 p.159 1928 1927 / military / dwellings = 0 (row_realigned)
  - sgt1939 p.159 1928 1927 / maritime / dwellings = 0 (row_realigned)

## Image versus OCR

- Read cell by cell on the page images (7 printings): sgt1927 f503, sgt1928 f1033, sgt1929 f511, sgt1930 f1047, sgt1935 f321, sgt1936 f189, sgt1939 f165.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
