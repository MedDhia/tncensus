# École coloniale d'agriculture. a) Lieu d'origine des élèves entrés à l'École

*Colonial school of agriculture (Tunis): students entering the school, by place of origin.*

Source: *Statistique générale de la Tunisie*, chapter *Institutions d'enseignement et de recherches*, editions sgt1930, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1930 (`bpt6k9105652d`): p. 292, f850; sgt1936 (`bpt6k91056547`): p. 109, f120; sgt1939 (`bpt6k9105739w`): p. 113, f119.

Transcriptions: `../transcribed/research_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_research.py build`.

Rows: 190. Years: 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Unit: students (count); value_type: count.

Selection (SPEC_ADDENDUM rule 4): each cell is stored once, from the latest edition printing it; every other printing of the same cell is compared below.

## Columns

- `census`: source edition (`sgt1922` ... `sgt1939`)
- `table_id`: section code of the transcription
- `gallica_ark`: Gallica volume ark
- `source_page`: printed page number
- `gallica_view`: Gallica view
- `year`: year of the figure (for a school year or season: the year it ends; for promotions and once-per-edition tables: the edition year)
- `period`: year of entry as printed (sgt1939 prints 1899-1913 as one line, '1899 à 1913')
- `origin`: place of origin (france, tunisia, algeria, colonies, abroad)
- `origin_fr`: column heading
- `value`: printed figure (» = 0)
- `flag`: empty, or ocr_corrected / illegible / total_mismatch / derived_from_totals / not_applicable / reprint_corrected / row_realigned

The school was closed during the 1914-1918 war (no line 1914-1918). Row totals (Totaux column) and the column totals since 1899 are checks only.

Every failed check below was re-read on a zoomed native-resolution crop: they are printed inconsistencies (printed values kept). sgt1928 prints 1927 France 72 for 27 (sgt1927 and sgt1929 print 27; the row total 46 and the column total 789 need 27): flagged total_mismatch.

Survey of the whole chapter in every edition: `research_survey.md`.

## Validation

- Checks against printed totals and identities: 380; passed: 356; failed: 24.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.250 (f274) school_origin 1907: total = sum: cells give 17, printed 15 (difference -2)
  - sgt1922 p.250 (f274) school_origin abroad: lines vs Totaux: cells give 33, printed 31 (difference -2)
  - sgt1923 p.263 (f765) school_origin 1910: total = sum: cells give 32, printed 31 (difference -1)
  - sgt1923 p.263 (f765) school_origin algeria: lines vs Totaux: cells give 43, printed 44 (difference 1)
  - sgt1923 p.263 (f765) school_origin abroad: lines vs Totaux: cells give 36, printed 34 (difference -2)
  - sgt1928 p.284 (f836) school_origin 1927: total = sum: cells give 91, printed 46 (difference -45)
  - sgt1928 p.284 (f836) school_origin france: lines vs Totaux: cells give 834, printed 789 (difference -45)
  - sgt1935 p.139 (f159) school_origin 1931: total = sum: cells give 21, printed 37 (difference 16)
  - sgt1935 p.139 (f159) school_origin Totaux: total = sum: cells give 1257, printed 1269 (difference 12)
  - sgt1935 p.139 (f159) school_origin france: lines vs Totaux: cells give 893, printed 883 (difference -10)
  - sgt1935 p.139 (f159) school_origin tunisia: lines vs Totaux: cells give 233, printed 249 (difference 16)
  - sgt1935 p.139 (f159) school_origin colonies: lines vs Totaux: cells give 29, printed 27 (difference -2)
  - sgt1936 p.109 (f120) school_origin 1931: total = sum: cells give 21, printed 37 (difference 16)
  - sgt1936 p.109 (f120) school_origin Totaux: total = sum: cells give 1285, printed 1297 (difference 12)
  - sgt1936 p.109 (f120) school_origin france: lines vs Totaux: cells give 901, printed 891 (difference -10)
  - sgt1936 p.109 (f120) school_origin tunisia: lines vs Totaux: cells give 248, printed 264 (difference 16)
  - sgt1936 p.109 (f120) school_origin colonies: lines vs Totaux: cells give 30, printed 28 (difference -2)
  - sgt1939 p.113 (f119) school_origin 1931: total = sum: cells give 21, printed 37 (difference 16)
  - sgt1939 p.113 (f119) school_origin Totaux: total = sum: cells give 1357, printed 1369 (difference 12)
  - sgt1939 p.113 (f119) school_origin france: lines vs Totaux: cells give 921, printed 911 (difference -10)
  - sgt1939 p.113 (f119) school_origin tunisia: lines vs Totaux: cells give 287, printed 303 (difference 16)
  - sgt1939 p.113 (f119) school_origin algeria: lines vs Totaux: cells give 64, printed 63 (difference -1)
  - sgt1939 p.113 (f119) school_origin colonies: lines vs Totaux: cells give 33, printed 31 (difference -2)
  - sgt1939 p.113 (f119) school_origin total: lines vs Totaux: cells give 1370, printed 1369 (difference -1)

- Overlapping printings: 1330 cell comparisons with other editions printing the same cell; 11 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1925 / france | sgt1925 | 33 | sgt1939 | 35 |
| 1925 / france | sgt1926 | 33 | sgt1939 | 35 |
| 1925 / france | sgt1927 | 33 | sgt1939 | 35 |
| 1925 / france | sgt1928 | 33 | sgt1939 | 35 |
| 1925 / france | sgt1929 | 33 | sgt1939 | 35 |
| 1925 / abroad | sgt1925 | 2 | sgt1939 | 3 |
| 1925 / abroad | sgt1926 | 2 | sgt1939 | 3 |
| 1925 / abroad | sgt1927 | 2 | sgt1939 | 3 |
| 1925 / abroad | sgt1928 | 2 | sgt1939 | 3 |
| 1925 / abroad | sgt1929 | 2 | sgt1939 | 3 |
| 1927 / france | sgt1928 | 72 | sgt1939 | 27 |

- Flagged cells: derived_from_totals: 1, total_mismatch: 1.

  - sgt1936 p.109 1900 1900 / france = 32 (derived_from_totals)
  - sgt1939 p.113 1931 1931 / tunisia = 1 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (12 printings): sgt1922 f274, sgt1923 f765, sgt1924 f1269, sgt1925 f335, sgt1926 f846, sgt1927 f308, sgt1928 f836, sgt1929 f313, sgt1930 f850, sgt1935 f159, sgt1936 f120, sgt1939 f119.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
