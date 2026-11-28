# Office public de crédit agricole indigène. Ressources ; Opérations de l'Office

*Public office for indigenous agricultural credit: resources (endowments, subsidies, loans, sales of State land) and operations (medium- and short-term credit), by year (1925-1934).*

Source: *Statistique générale de la Tunisie*, chapter *Institutions économiques et sociales / Mutualité agricole*, editions sgt1930, sgt1935. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1930 (`bpt6k9105652d`): p. 473, f1031; sgt1935 (`bpt6k9105653t`): p. 290, f310.

Transcriptions: `../transcribed/mutuality_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_mutuality.py build`.

Rows: 58. Years: 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934.

Units: francs (centimes as decimals); suggested value_type: francs.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (rule 4 tables: the latest edition printing that year)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible`, `not_applicable`, `total_mismatch`, `ocr_corrected`

Printed in sgt1929 (f495: ressources 1925-1929, opérations 1926-1929), sgt1930 (f1031: ressources au 31 décembre 1930, 1925-1930, with a new emprunts column; opérations 1926-1930) and sgt1935 (f310: ressources au 31 décembre 1934, lines 1926-1934; opérations 1926-1934). Not printed in sgt1936 or sgt1939: a footnote to the sgt1935 1934 line says the Office was dissolved by decree of 21 February 1934 (1934 operations printed », stored 0 as printed). sgt1929 has no emprunts column (no loans before 1930 in the later printings). Printed row totals (totaux) and TOTAUX lines are checks only; the sgt1935 TOTAUX include the 1925 line, which sgt1935 does not print (checked with the sgt1930 1925 line).

The court terme operations of 1928 are printed 7.262.371 in sgt1929 and 7.626.371 in sgt1930 and sgt1935 (whose row total 9.291.171, printed in all three, agrees with 1.664.800 + 7.626.371): an evident transposition in sgt1929; the latest printing is kept.

Every failed check below was re-read on a native-resolution crop: the printed values are kept. sgt1929 1928 operations: totaux 9.291.171 for 1.664.800 + 7.262.371 = 8.927.171 (zoomed 2x on f495); sgt1930 and sgt1935 print the court terme 7.626.371, which gives the printed total (digits 26/62 transposed in sgt1929; sgt1930 kept).

Survey of the whole chapter in every edition: `mutuality_survey.md`.

## Validation

- Checks against printed totals and identities: 55; passed: 54; failed: 1.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1929 p.467 (f495) office_operations 1928: total = medium_term + short_term: cells give 8927171, printed 9291171 (difference 364000)

- Overlapping printings: 53 cell comparisons with other editions printing the same cell; 1 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1928 / operations_short_term | sgt1929 | 7262371 | sgt1935 | 7626371 |

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (6 printings): sgt1929 f495, sgt1929 f495, sgt1930 f1031, sgt1930 f1031, sgt1935 f310, sgt1935 f310.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
