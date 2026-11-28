# Forêts. a) Superficie des terrains domaniaux boisés ; délimitations

*Forests: area of the wooded state lands, delimitation and boundary-marking (bornage), by region, 1903-1930.*

Source: *Statistique générale de la Tunisie*, chapter *Agriculture*, editions sgt1930. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1930 (`bpt6k9105652d`): p. 258, f816.

Transcriptions: `../transcribed/agriculture_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_agriculture.py build`.

Rows: 168. Years: 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930.

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

Printed in sgt1922-sgt1930 (f253, f743, f1245, f307, f817, f280, f804, f282, f816), one line for 1903-1910 and one per year to the edition year; nine independent printings, each typed from its own page image. Columns: Région Nord (forêts de chênes-liège) and Région des Hauts plateaux (forêts de pins d'Alep, chênes verts, genévriers), each with the hectares délimités in the period and the superficie totale; superficie totale délimitée dans les deux régions; hectares bornés dans l'année (Nord, Hauts plateaux); superficie totale bornée au 31 décembre. The total columns are printed columns of the table (not total lines) and are stored; they are also used as checks.

From 1926 the three superficie columns are printed » (no stock printed any more): stored NA, `not_applicable`; the hectares délimités printed » are stored 0. From 1927 the last column holds the hectares bornés in the year (11.200 = 4.200 + 7.000 in 1927), not the cumulative total (143.161 at the end of 1926): the check changes accordingly; the values are stored as printed (`measure` stays `bounded_total`, see `measure_fr`).

Checks: superficie totale Nord + Hauts plateaux = total of the two regions; each superficie totale = previous line + hectares délimités of the line (not on the first line: the 1903-1910 delimitations, 49.019 and 82.846, do not account for the superficies 246.976 and 561.394); total bornée = previous line + hectares bornés of the line to 1926, = hectares bornés of the line from 1927.

The sgt1935-sgt1939 layout (domaine soumis au régime forestier, with surfaces déclassées and a first line for all earlier years, from 1931) is a different table: `agriculture_forest_domain`. It does not continue these columns (its Région Nord surface, 220.587 ha before 1931, is not the 246.976 ha délimités here; its bornages start again at 176.746 ha), so it is kept apart rather than coded as extra columns.

Every failed check below was re-read on a zoomed native-resolution crop: they are printed inconsistencies (printed values kept). sgt1924 prints the 1915 Région Nord bornage 2.460 (2.160 in the eight other printings, and its own cumulative 15.823 needs 2.160; flagged in that printing, value stored from sgt1930) and the 1924 total bornée 88.843 (87.843 = 80.343 + 7.500 in every later printing; flagged, stored from sgt1930). Both are failures of the sgt1924 printing only.

Survey of the whole chapter in every edition: `agriculture_survey.md`.

## Validation

- Checks against printed totals and identities: 540; passed: 538; failed: 2.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1924 p.255 (f1245) forest_a 1915: bornage_total = previous line + n_bornage + hp_bornage: cells give 16123, printed 15823 (difference -300)
  - sgt1924 p.255 (f1245) forest_a 1924: bornage_total = previous line + n_bornage + hp_bornage: cells give 87843, printed 88843 (difference 1000)

- Overlapping printings: 1026 cell comparisons with other editions printing the same cell; 2 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1915 / 1915 / north / bounded_in_year | sgt1924 | 2460 | sgt1930 | 2160 |
| 1924 / 1924 / both / bounded_total | sgt1924 | 88843 | sgt1930 | 87843 |

- Flagged cells: not_applicable: 15.

  - sgt1930 p.258 1926 1926 / north / total_area / hectares = NA (not_applicable)
  - sgt1930 p.258 1926 1926 / high_plateaux / total_area / hectares = NA (not_applicable)
  - sgt1930 p.258 1926 1926 / both / total_delimited / hectares = NA (not_applicable)
  - sgt1930 p.258 1927 1927 / north / total_area / hectares = NA (not_applicable)
  - sgt1930 p.258 1927 1927 / high_plateaux / total_area / hectares = NA (not_applicable)
  - sgt1930 p.258 1927 1927 / both / total_delimited / hectares = NA (not_applicable)
  - sgt1930 p.258 1928 1928 / north / total_area / hectares = NA (not_applicable)
  - sgt1930 p.258 1928 1928 / high_plateaux / total_area / hectares = NA (not_applicable)
  - sgt1930 p.258 1928 1928 / both / total_delimited / hectares = NA (not_applicable)
  - sgt1930 p.258 1929 1929 / north / total_area / hectares = NA (not_applicable)
  - sgt1930 p.258 1929 1929 / high_plateaux / total_area / hectares = NA (not_applicable)
  - sgt1930 p.258 1929 1929 / both / total_delimited / hectares = NA (not_applicable)
  - sgt1930 p.258 1930 1930 / north / total_area / hectares = NA (not_applicable)
  - sgt1930 p.258 1930 1930 / high_plateaux / total_area / hectares = NA (not_applicable)
  - sgt1930 p.258 1930 1930 / both / total_delimited / hectares = NA (not_applicable)

## Image versus OCR

- Read cell by cell on the page images (9 printings): sgt1922 f253, sgt1923 f743, sgt1924 f1245, sgt1925 f307, sgt1926 f817, sgt1927 f280, sgt1928 f804, sgt1929 f282, sgt1930 f816.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
