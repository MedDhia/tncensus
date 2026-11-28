# Forêts. Superficie et modifications dans la consistance du domaine soumis au régime forestier

*Forests: area of the domain under the forest regime (land newly brought under it, declassified, total) and administrative boundary-marking, by region, before 1931 to 1939.*

Source: *Statistique générale de la Tunisie*, chapter *Agriculture*, editions sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1935 (`bpt6k9105653t`): p. 133, f153; sgt1936 (`bpt6k91056547`): p. 104, f115; sgt1939 (`bpt6k9105739w`): p. 108, f114.

Transcriptions: `../transcribed/agriculture_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_agriculture.py build`.

Rows: 110. Years: 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939.

Units: hectares (`unit`); value_type: area.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (rule 4 series: the latest edition printing that year; rule 5 tables: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: last year covered by the line (`period` 1903-1910: 1910; `before_1931`: 1930; `before_1932`: 1931)
- `period`: printed line: a year, the group 1903-1910, or `before_1931` / `before_1932` (Antérieures à 1931 / 1932)
- `period_fr`: printed line heading
- `region`: `north` (Région Nord), `high_plateaux` (Région des Hauts plateaux) or `both` (the two regions)
- `region_fr`: printed region heading
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: `hectares`
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible`, `not_applicable`, `total_mismatch` (cell identified as the faulty one of a failed check, printed value kept), `reprint_corrected`

Printed in sgt1935 (f153, a) Superficie et modifications ...: Antérieures à 1931, 1931-1935), sgt1936 (f115, Consistance du domaine ...: Antérieures à 1932, 1932-1936) and sgt1939 (f114: 1932-1939). Columns per region (Région Nord: forêts de chênes-liège et zéen; Hauts plateaux: pins, chênes verts, genévriers): surfaces nouvellement soumises au régime forestier, surfaces déclassées, surface du domaine soumis; superficie totale des terrains domaniaux soumis; bornages administratifs (sgt1939: ou surfaces immatriculées): surfaces nouvellement bornées per region and surface totale des forêts bornée (cumulative). » = 0. Separate from `agriculture_forest_area` (sgt1922-sgt1930), whose columns and stocks it does not continue (see that file).

Checks: Nord + Hauts plateaux = superficie totale; surface of the domain = previous line + nouvellement soumises - déclassées; surface totale bornée = previous line + surfaces bornées. Each year is taken from the latest printing (rule 4); sgt1939's misprints of 1932 and 1934 are replaced by sgt1936's cells (`reprint_corrected`).

Every failed check below was re-read on a zoomed native-resolution crop: they are printed inconsistencies (printed values kept). sgt1935 prints the 1931 Hauts plateaux surface 718.990 for 781.990 (790.018 - 8.028; its own total 1.001.040 and the 1932 line need 781.990): flagged; it fails two checks (total, and 1932 = 1931 - 1.036). Its 1931 surface totale bornée 198.415 is 21.669 above 176.746 although the line prints 1.020 + 6.300 bornés: the difference, 14.349, is the 1930 bornage of `agriculture_forest_area` (sgt1930), and 176.746 = 143.161 (end of 1926) + 11.200 + 11.682 + 10.703 (1927-1929), i.e. the line Antérieures à 1931 stops at 1929 and 1930 is counted in 1931 (cells kept as printed, unflagged). sgt1936's line Antérieures à 1932 adds sgt1935's Antérieures à 1931 and 1931 lines column by column, stocks included (439.637 = 220.587 + 219.050, 1.509.008 = 790.018 + 718.990, 2.011.645, 375.161 = 176.746 + 198.415): the surfaces and the total bornée of that line are flagged `total_mismatch` (the déclassées 7.139 and 8.178 are correct sums of 1903-1931). sgt1939 prints the 1934 Hauts plateaux surface 778.309 (778.302 in sgt1935 and sgt1936 = 778.700 - 398; three failed checks) and the 1932 Région Nord bornage 2.110 (1.110 in sgt1935 and sgt1936; 198.415 + 1.110 + 9.000 = 208.525): both flagged in that printing and stored from sgt1936. sgt1935's 1933 surface totale bornée has its last digit cut by the column rule ("214.19?", illegible; 214.190 in sgt1936 and sgt1939, stored from sgt1939).

Survey of the whole chapter in every edition: `agriculture_survey.md`.

## Validation

- Checks against printed totals and identities: 69; passed: 58; failed: 11.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1935 p.133 (f153) forest_domain 1931: total = Nord + Hauts plateaux: cells give 938040, printed 1001040 (difference 63000)
  - sgt1935 p.133 (f153) forest_domain 1931: hp_total = previous line + hp_new - declassed: cells give 781990, printed 718990 (difference -63000)
  - sgt1935 p.133 (f153) forest_domain 1931: bornage_total = previous line + n_bornage + hp_bornage: cells give 184066, printed 198415 (difference 14349)
  - sgt1935 p.133 (f153) forest_domain 1932: hp_total = previous line + hp_new - declassed: cells give 717954, printed 780954 (difference 63000)
  - sgt1936 p.104 (f115) forest_domain before_1932: total = Nord + Hauts plateaux: cells give 1948645, printed 2011645 (difference 63000)
  - sgt1936 p.104 (f115) forest_domain 1932: n_total = previous line + n_new - declassed: cells give 438580, printed 217993 (difference -220587)
  - sgt1936 p.104 (f115) forest_domain 1932: hp_total = previous line + hp_new - declassed: cells give 1507972, printed 780954 (difference -727018)
  - sgt1936 p.104 (f115) forest_domain 1932: bornage_total = previous line + n_bornage + hp_bornage: cells give 385271, printed 208525 (difference -176746)
  - sgt1939 p.108 (f114) forest_domain 1934: total = Nord + Hauts plateaux: cells give 996269, printed 996262 (difference -7)
  - sgt1939 p.108 (f114) forest_domain 1934: hp_total = previous line + hp_new - declassed: cells give 778302, printed 778309 (difference 7)
  - sgt1939 p.108 (f114) forest_domain 1935: hp_total = previous line + hp_new - declassed: cells give 778061, printed 778054 (difference -7)

- Overlapping printings: 89 cell comparisons with other editions printing the same cell; 4 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1932 / 1932 / north / newly_bounded | sgt1935 | 1110 | sgt1939 | 2110 |
| 1932 / 1932 / north / newly_bounded | sgt1936 | 1110 | sgt1939 | 2110 |
| 1934 / 1934 / high_plateaux / domain_area | sgt1935 | 778302 | sgt1939 | 778309 |
| 1934 / 1934 / high_plateaux / domain_area | sgt1936 | 778302 | sgt1939 | 778309 |

- Flagged cells: reprint_corrected: 2, total_mismatch: 5.

  - sgt1935 p.133 1931 1931 / high_plateaux / domain_area / hectares = 718990 (total_mismatch)
  - sgt1936 p.104 1931 before_1932 / north / domain_area / hectares = 439637 (total_mismatch)
  - sgt1936 p.104 1931 before_1932 / high_plateaux / domain_area / hectares = 1509008 (total_mismatch)
  - sgt1936 p.104 1931 before_1932 / both / domain_area_total / hectares = 2011645 (total_mismatch)
  - sgt1936 p.104 1931 before_1932 / both / bounded_total / hectares = 375161 (total_mismatch)
  - sgt1936 p.104 1932 1932 / north / newly_bounded / hectares = 1110 (reprint_corrected)
  - sgt1936 p.104 1934 1934 / high_plateaux / domain_area / hectares = 778302 (reprint_corrected)

## Image versus OCR

- Read cell by cell on the page images (3 printings): sgt1935 f153, sgt1936 f115, sgt1939 f114.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
