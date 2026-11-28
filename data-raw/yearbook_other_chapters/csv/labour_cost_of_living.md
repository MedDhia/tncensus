# Coût de la vie. Nombres-indices du coût de la vie (base : 100 en juillet 1914)

*Cost-of-living index numbers for French, Italian and indigenous working families (July 1914 = 100).*

Source: *Statistique générale de la Tunisie*, chapter *Travail et prévoyance sociale*, editions sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1927 (`bpt6k91056510`): p. 482, f510; sgt1928 (`bpt6k91056510`): p. 488, f1040; sgt1929 (`bpt6k9105652d`): p. 490, f518; sgt1930 (`bpt6k9105652d`): p. 496, f1054; sgt1935 (`bpt6k9105653t`): p. 308, f328; sgt1936 (`bpt6k91056547`): p. 184, f195; sgt1939 (`bpt6k9105739w`): p. 169, f175.

Transcriptions: `../transcribed/labour_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_labour.py build`.

Rows: 201. Years: 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Unit: index, July 1914 = 100; value_type: rate (index numbers).

Printed for overlapping windows: each cell is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (rule 4 series: the latest edition printing it; rule 5: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (two-page spreads: the page the cell is printed on)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (HBM: last year of the printed period)
- `period`: year / s1-s2 (half-years) / t1-t4 (quarters)
- `period_fr`: period as printed
- `group`: family group of the index (English code)
- `group_fr`: printed heading
- `basis`: food_only (indices up to the 3rd quarter 1928: food expenditure only) or all_expenditure (from the 4th quarter 1928: food, heating and lighting, housing, clothing, miscellaneous)
- `value`: printed value (» = 0)
- `flag`: empty, ocr_corrected, illegible, total_mismatch, derived_from_totals, not_applicable, reprint_corrected or row_realigned

Printed in every edition from sgt1926 (yearly 1915-1923, half-years 1924-1926, quarters from 1927). Footnote (N.B.): the indices rest on the cost of a working family of four (father, mother, two children); up to the 3rd quarter 1928 on food expenditure only, from the 4th quarter 1928 on all expenditure (food, heating and lighting, housing, clothing, miscellaneous) (`basis`); separate indices for French, Italian and indigenous families 'dont le genre de vie présente des différences notables'. sgt1939 1939 4th quarter printed » (not available): NA, `not_applicable`. No totals.

Survey of the whole chapter in every edition: `labour_survey.md`.

## Validation

- Checks against printed totals and identities: 0; passed: 0; failed: 0.

- Overlapping printings: 270 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: not_applicable: 3.

  - sgt1939 p.169 1939 t4 / french / all_expenditure = NA (not_applicable)
  - sgt1939 p.169 1939 t4 / italian / all_expenditure = NA (not_applicable)
  - sgt1939 p.169 1939 t4 / indigenous / all_expenditure = NA (not_applicable)

## Image versus OCR

- Read cell by cell on the page images (8 printings): sgt1926 f1044, sgt1927 f510, sgt1928 f1040, sgt1929 f518, sgt1930 f1054, sgt1935 f328, sgt1936 f195, sgt1939 f175.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
