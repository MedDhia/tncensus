# Minerais. a) Tonnage et valeur des minerais transportés (mine à quai)

*Zinc, lead and mixed ores (from 1936 mercury): mines conceded, tonnage, value and average prices.*

Source: *Statistique générale de la Tunisie*, chapter *Travaux publics*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 159, f183; sgt1923 (`bpt6k9105649x`): p. 171, f673; sgt1924 (`bpt6k9105649x`): p. 179, f1169; sgt1925 (`bpt6k9105650k`): p. 185, f209; sgt1926 (`bpt6k9105650k`): p. 201, f765; sgt1927 (`bpt6k91056510`): p. 199, f227; sgt1928 (`bpt6k91056510`): p. 199, f751; sgt1929 (`bpt6k9105652d`): p. 201, f229; sgt1930 (`bpt6k9105652d`): p. 205, f763; sgt1935 (`bpt6k9105653t`): p. 105, f125; sgt1936 (`bpt6k91056547`): p. 81, f92; sgt1939 (`bpt6k9105739w`): p. 86, f92.

Transcriptions: `../transcribed/publicworks_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_publicworks.py build`.

Rows: 251. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Units: count, tonnes (mercury kg), francs, average prices in pounds sterling per tonne to 1930 and francs per tonne from 1931; suggested value_type: mixed.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition; an aligned printing is preferred to a realigned one); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from: the latest edition printing that year (rule 5 tables: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `ore`: `zinc`, `lead`, `mixed` (mixtes), `mercury`, or empty for the all-ores columns
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible`, `not_applicable` (nothing printed), `row_realigned` (printed on the wrong line, stored on the year it belongs to), `total_mismatch`

Every printing of 1918 (sgt1922-sgt1927) gives a total value of 14.077.870 for zinc 1.046.520 + lead 18.031.350 = 19.077.870 (printed error, recurring). Columns mixtes from sgt1925 (» before 1925). Average prices printed » in 1917-1919 and 1921 (no quotation): stored NA (`not_applicable`). sgt1930 1930 footnote (1) on the 58 mines: 3 concessions ont disparu par fusion avec des concessions voisines; sgt1935-sgt1939 footnote (1): from 1931 only the concessions of the 3rd group (lead, zinc or both) are counted; cours moyen de la Livre: 89 fr. 14.

Misprinted alignment in sgt1935, sgt1936 and sgt1939 (same standing type): the columns mines, zinc tonnage, mixtes tonnage, zinc value and mixtes value are printed one line too low on the lines up to 1934, while lead, total value and prices are aligned (the values printed on their lines 1926-1931 are sgt1930's 1925-1930; the 1931 total 11.120.000 = 120.000 printed on the 1932 line + 11.000.000; footnote (1) "en 1931" sits on the 50 printed on the 1932 line). The script stores those cells one year earlier (`row_realigned`); the line 1935 is taken as printed (the line 1936 of sgt1936 is aligned, agreeing with that edition's mines table). Consequently year 1934 has no mines / zinc values from these printings, and the 1935 check fails by 60.000 (zinc value 60.000 on the 1935 line), whichever year it is attached to. From sgt1936 the mixtes columns are headed "mercure (en kilogs)" from 1933 (no figures 1933-1935).

Every failed check below was re-read on a zoomed native-resolution crop, or recurs unchanged in independent readings of several editions: they are printed errors (printed values kept). 

Survey of the whole chapter in every edition: `publicworks_survey.md`.

## Validation

- Checks against printed totals and identities: 117; passed: 108; failed: 9.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.159 (f183) 1918: value_total = zinc + lead + mixtes/mercure values: cells give 19077870, printed 14077870 (difference -5000000)
  - sgt1923 p.171 (f673) 1918: value_total = zinc + lead + mixtes/mercure values: cells give 19077870, printed 14077870 (difference -5000000)
  - sgt1924 p.179 (f1169) 1918: value_total = zinc + lead + mixtes/mercure values: cells give 19077870, printed 14077870 (difference -5000000)
  - sgt1925 p.185 (f209) 1918: value_total = zinc + lead + mixtes/mercure values: cells give 19077870, printed 14077870 (difference -5000000)
  - sgt1926 p.201 (f765) 1918: value_total = zinc + lead + mixtes/mercure values: cells give 19077870, printed 14077870 (difference -5000000)
  - sgt1927 p.199 (f227) 1918: value_total = zinc + lead + mixtes/mercure values: cells give 19077870, printed 14077870 (difference -5000000)
  - sgt1935 p.105 (f125) 1935: value_total = zinc + lead + mixtes/mercure values: cells give 3120000, printed 3060000 (difference -60000)
  - sgt1936 p.81 (f92) 1935: value_total = zinc + lead + mixtes/mercure values: cells give 3120000, printed 3060000 (difference -60000)
  - sgt1939 p.86 (f92) 1935: value_total = zinc + lead + mixtes/mercure values: cells give 3120000, printed 3060000 (difference -60000)

- Overlapping printings: 821 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: row_realigned: 15.

  - sgt1939 p.86 1931  / mines_conceded / count = 50 (row_realigned)
  - sgt1939 p.86 1931 zinc / tonnage / tonnes = 660 (row_realigned)
  - sgt1939 p.86 1931 mixed / tonnage / tonnes = 0 (row_realigned)
  - sgt1939 p.86 1931 zinc / value / francs = 120000 (row_realigned)
  - sgt1939 p.86 1931 mixed / value / francs = 0 (row_realigned)
  - sgt1935 p.105 1932 mixed / tonnage / tonnes = 0 (row_realigned)
  - sgt1935 p.105 1932 mixed / value / francs = 0 (row_realigned)
  - sgt1939 p.86 1932  / mines_conceded / count = 51 (row_realigned)
  - sgt1939 p.86 1932 zinc / tonnage / tonnes = 0 (row_realigned)
  - sgt1939 p.86 1932 zinc / value / francs = 0 (row_realigned)
  - sgt1935 p.105 1933 mixed / tonnage / tonnes = 0 (row_realigned)
  - sgt1935 p.105 1933 mixed / value / francs = 0 (row_realigned)
  - sgt1939 p.86 1933  / mines_conceded / count = 52 (row_realigned)
  - sgt1939 p.86 1933 zinc / tonnage / tonnes = 0 (row_realigned)
  - sgt1939 p.86 1933 zinc / value / francs = 0 (row_realigned)

## Image versus OCR

- Read cell by cell on the page images (14 printings): sgt1922 f183, sgt1923 f673, sgt1924 f1169, sgt1925 f209, sgt1926 f765, sgt1927 f227, sgt1928 f751, sgt1929 f229, sgt1930 f763, sgt1935 f125, sgt1936 f92, sgt1936 f92, sgt1939 f92, sgt1939 f92.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
