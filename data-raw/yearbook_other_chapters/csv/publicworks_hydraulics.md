# Travaux hydrauliques. Alimentation en eau potable, hydraulique agricole, forages artésiens, assainissement

*Hydraulic works: drinking water supply, agricultural hydraulics, artesian wells and sanitation (cumulative flows and expenditure).*

Source: *Statistique générale de la Tunisie*, chapter *Travaux publics*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 156, f180, p. 157, f181; sgt1923 (`bpt6k9105649x`): p. 168, f670, p. 169, f671; sgt1924 (`bpt6k9105649x`): p. 176, f1166, p. 177, f1167; sgt1925 (`bpt6k9105650k`): p. 182, f206, p. 183, f207; sgt1926 (`bpt6k9105650k`): p. 198, f762, p. 199, f763; sgt1927 (`bpt6k91056510`): p. 196, f224, p. 197, f225; sgt1928 (`bpt6k91056510`): p. 196, f748, p. 197, f749; sgt1929 (`bpt6k9105652d`): p. 199, f227; sgt1930 (`bpt6k9105652d`): p. 203, f761; sgt1935 (`bpt6k9105653t`): p. 103, f123; sgt1936 (`bpt6k91056547`): p. 78, f89.

Transcriptions: `../transcribed/publicworks_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_publicworks.py build`.

Rows: 134. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936.

Units: m3 per day, litres per second and francs (`unit`); suggested value_type: mixed.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition; an aligned printing is preferred to a realigned one); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from: the latest edition printing that year (rule 5 tables: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `work`: work code (English)
- `work_fr`: printed heading
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible`, `not_applicable` (nothing printed), `row_realigned` (printed on the wrong line, stored on the year it belongs to), `total_mismatch`

Four small tables printed side by side: a) Alimentation en eau potable des centres habités (débits moyens journaliers cumulés, m3; dépenses cumulées) and b) Aménagement d'hydraulique agricole (volume utilisable des eaux d'irrigation permanente, m3 journaliers; dépenses cumulées), sgt1922-sgt1928 only; c) Forages artésiens (débit en litres par seconde; dépenses cumulées) and d) Installation d'assainissement des centres habités (dépenses cumulées), sgt1922-sgt1935 (lettered a) and b) from sgt1929). Not printed in sgt1936 and sgt1939.

Printed oddities, kept as printed: drinking water 1927 is printed 1.144.660 m3 (sgt1927, sgt1928; 1926 141.011, 1928 1.803.442), a jump the expenditure does not show. sgt1935 prints the artesian-well flows one line too low for 1926-1931 (its 1926 = 1.396 is sgt1930's 1925, ..., its 1931 = 1.722 is sgt1930's 1930), and sgt1928-sgt1935 print 1927 as 1.451 l/s (sgt1927: 1.564): listed in the overlap differences below.

Every failed check below was re-read on a zoomed native-resolution crop, or recurs unchanged in independent readings of several editions: they are printed errors (printed values kept). 

Survey of the whole chapter in every edition: `publicworks_survey.md`.

## Validation

- Checks against printed totals and identities: 540; passed: 533; failed: 7.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.156 (f180) water m3: 1920 (56000) below 1919 (56600) in a cumulative series
  - sgt1923 p.168 (f670) water m3: 1920 (56000) below 1919 (56600) in a cumulative series
  - sgt1924 p.176 (f1166) water m3: 1920 (56000) below 1919 (56600) in a cumulative series
  - sgt1925 p.182 (f206) water m3: 1920 (56000) below 1919 (56600) in a cumulative series
  - sgt1926 p.198 (f762) water m3: 1920 (56000) below 1919 (56600) in a cumulative series
  - sgt1927 p.196 (f224) water m3: 1920 (56000) below 1919 (56600) in a cumulative series
  - sgt1928 p.196 (f748) water m3: 1920 (56000) below 1919 (56600) in a cumulative series

- Overlapping printings: 466 cell comparisons with other editions printing the same cell; 1 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1927 / artesian_wells / flow | sgt1927 | 1564 | sgt1930 | 1451 |

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (35 printings): sgt1922 f180, sgt1922 f180, sgt1922 f181, sgt1922 f181, sgt1923 f670, sgt1923 f670, sgt1923 f671, sgt1923 f671, sgt1924 f1166, sgt1924 f1166, sgt1924 f1167, sgt1924 f1167, sgt1925 f206, sgt1925 f206, sgt1925 f207, sgt1925 f207, sgt1926 f762, sgt1926 f762, sgt1926 f763, sgt1926 f763, sgt1927 f224, sgt1927 f224, sgt1927 f225, sgt1927 f225, sgt1928 f748, sgt1928 f748, sgt1928 f749, sgt1928 f749, sgt1929 f227, sgt1929 f227, sgt1930 f761, sgt1930 f761, sgt1935 f123, sgt1935 f123, sgt1936 f89.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
