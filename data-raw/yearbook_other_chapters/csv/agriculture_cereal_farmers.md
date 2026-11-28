# Principales cultures. Céréales (blé dur, tendre, orge, avoine). Répartition de la superficie entre européens et indigènes

*Cereals (durum and soft wheat, barley, oats): sown area of European and indigenous farmers.*

Source: *Statistique générale de la Tunisie*, chapter *Agriculture*, editions sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1926 (`bpt6k9105650k`): p. 250, f814; sgt1927 (`bpt6k91056510`): p. 242, f270; sgt1928 (`bpt6k91056510`): p. 258, f794; sgt1929 (`bpt6k9105652d`): p. 244, f272; sgt1930 (`bpt6k9105652d`): p. 262, f806, p. 263, f807; sgt1935 (`bpt6k9105653t`): p. 127, f147; sgt1936 (`bpt6k91056547`): p. 97, f108; sgt1939 (`bpt6k9105739w`): p. 101, f107.

Transcriptions: `../transcribed/agriculture_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_agriculture.py build`.

Rows: 132. Years: 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Units: hectares (`unit`); value_type: hectares.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (rule 4 series: the latest edition printing that year; rule 5 tables: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (crop year = calendar year of the harvest, as printed; rule 5 tables: edition year)
- `crop`: crop code (English): `wheat` = blé dur et blé tendre (one line to sgt1936), `durum_wheat` / `soft_wheat` (sgt1939), `barley`, `oats`
- `crop_fr`: printed line heading (CLASSIFICATION)
- `farmers`: `european` or `indigenous` (CULTURES EUROPÉENNES ou indigènes)
- `farmers_fr`: printed line heading
- `measure`: measure code (English)
- `measure_fr`: printed heading of the measure
- `unit`: `hectares` (printed h. a., hectares and ares, stored with two decimals, to 1927; whole hectares from the 1928 figures)
- `value`: printed value (» = 0)
- `flag`: empty, or `derived_from_totals` (broken digit solved from the printed average), `reprint_corrected`

Printed from sgt1926 (ten years to sgt1930, three years from sgt1935), as sub-table b) of the principales cultures after the yields by zone (agriculture_cereal_zones). The printed averages (MOYENNE DES ANNÉES) are not stored; they are checked against the mean of the printed years when every year is printed in the same edition (to 0.05 % or 1 ha). sgt1930 heads its third average "1920-1929": blé and orge repeat sgt1929's 1920-1929 averages, avoine prints new figures; not checkable (1920 not printed). sgt1935-sgt1936 reprint averages over years they do not print (1931-1935, 1926-1935). sgt1939 splits blé dur and blé tendre (footnote: soft wheat distinguished only from 1937; their averages are of 1937-1939, their 1930-1939 average not printed).

Rule 4: each year from the latest edition printing it; the other printings, read independently on their own pages, are compared below. sgt1926-sgt1927 print the 1920 blé Européennes 72.914 55, sgt1928-sgt1929 72.944 55 (zoomed crops); the averages of sgt1926 (1917-1921), sgt1927 (1918-1922) and sgt1929 (1920-1924) all need 72.944 5x: sgt1926-sgt1927 misprint it (listed among the failed checks), the latest printing is kept.

Every failed check below was re-read on a zoomed native-resolution crop: they are printed inconsistencies (printed values kept). Averages that fail are printed averages not fitting the printed years (listed); the years agree across every printing.

Survey of the whole chapter in every edition: `agriculture_survey.md`.

## Validation

- Checks against printed totals and identities: 87; passed: 66; failed: 21.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1926 p.251 (f815) split wheat_eur: average 1917-1921: cells give 77167.16, printed 77173.15 (difference 5.99)
  - sgt1926 p.251 (f815) split wheat_eur: average 1917-1926: cells give 91198.43, printed 91201.42 (difference 2.99)
  - sgt1927 p.243 (f271) split wheat_eur: average 1918-1922: cells give 79864.52, printed 79870.52 (difference 6.00)
  - sgt1927 p.243 (f271) split wheat_eur: average 1918-1927: cells give 95218.92, printed 95221.91 (difference 2.99)
  - sgt1927 p.243 (f271) split barley_eur: average 1918-1922: cells give 17039.89, printed 17057.89 (difference 18.00)
  - sgt1927 p.243 (f271) split barley_eur: average 1918-1927: cells give 19481.18, printed 19490.18 (difference 9.00)
  - sgt1927 p.243 (f271) split barley_ind: average 1918-1922: cells give 421210.86, printed 421216.85 (difference 5.99)
  - sgt1927 p.243 (f271) split barley_ind: average 1918-1927: cells give 420927.50, printed 420930.50 (difference 3.00)
  - sgt1927 p.243 (f271) split oats_eur: average 1918-1922: cells give 37826.36, printed 37806.36 (difference -20.00)
  - sgt1927 p.243 (f271) split oats_eur: average 1923-1927: cells give 23544.44, printed 23544.02 (difference -0.42)
  - sgt1927 p.243 (f271) split oats_eur: average 1918-1927: cells give 30685.40, printed 30675.28 (difference -10.12)
  - sgt1927 p.243 (f271) split oats_ind: average 1918-1927: cells give 20451.88, printed 10451.88 (difference -10000.00)
  - sgt1928 p.259 (f795) split wheat_eur: average 1919-1928: cells give 102156.23, printed 112156 (difference 9999.77)
  - sgt1928 p.259 (f795) split wheat_ind: average 1919-1923: cells give 474656.67, printed 514856 (difference 40199.33)
  - sgt1928 p.259 (f795) split wheat_ind: average 1919-1928: cells give 503300.36, printed 524400 (difference 21099.64)
  - sgt1928 p.259 (f795) split barley_eur: average 1919-1923: cells give 16952.66, printed 16738 (difference -214.66)
  - sgt1928 p.259 (f795) split barley_eur: average 1919-1928: cells give 20359.06, printed 20252 (difference -107.06)
  - sgt1928 p.259 (f795) split barley_ind: average 1919-1928: cells give 421707.12, printed 401707 (difference -20000.12)
  - sgt1930 p.263 (f807) split wheat_eur: average 1926-1930: cells give 137109.05, printed 138709 (difference 1599.95)
  - sgt1939 p.101 (f107) split soft_eur: average 1937-1939: cells give 121833.33, printed 121666 (difference -167.33)
  - sgt1939 p.101 (f107) split soft_ind: average 1937-1939: cells give 38833.33, printed 37666 (difference -1167.33)

- Overlapping printings: 228 cell comparisons with other editions printing the same cell; 2 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1920 / wheat / european / area | sgt1926 | 72914.55 | sgt1929 | 72944.55 |
| 1920 / wheat / european / area | sgt1927 | 72914.55 | sgt1929 | 72944.55 |

- Flagged cells: derived_from_totals: 1.

  - sgt1926 p.250 1917 barley / european / area / hectares = 20494.88 (derived_from_totals)

## Image versus OCR

- Read cell by cell on the page images (14 printings): sgt1926 f814, sgt1926 f815, sgt1927 f270, sgt1927 f271, sgt1928 f794, sgt1928 f795, sgt1929 f272, sgt1929 f273, sgt1930 f806, sgt1930 f807, sgt1935 f147, sgt1936 f108, sgt1939 f107, sgt1939 f107.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
