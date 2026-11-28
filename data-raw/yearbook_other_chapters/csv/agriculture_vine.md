# Vigne. Répartition des viticulteurs par contrôle (sgt1925 : par régions) et par nationalité

*Vineyards: number of vine growers and vineyard area by contrôle civil and nationality.*

Source: *Statistique générale de la Tunisie*, chapter *Agriculture*, editions sgt1922, sgt1923, sgt1924, sgt1925. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 226, f250; sgt1923 (`bpt6k9105649x`): p. 238, f740; sgt1924 (`bpt6k9105649x`): p. 252, f1242; sgt1925 (`bpt6k9105650k`): p. 280, f304.

Transcriptions: `../transcribed/agriculture_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_agriculture.py build`.

Rows: 638. Years: 1922, 1923, 1924, 1925.

Units: growers and hectares (`unit`); value_type: mixed.

Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept; `year` = edition year.

## Columns

- `census`: edition the value is taken from (rule 4 series: the latest edition printing that year; rule 5 tables: the edition)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: edition year (the table gives the state of the vineyard; no date printed)
- `region`: région as printed (sgt1925); empty when the table lists contrôles only
- `chef_lieu`: chef-lieu de région as printed (sgt1925); empty otherwise
- `controle_civil`: contrôle civil as printed (spelling of each edition: Kef / Le Kef, Teboursouk / Téboursouk; sgt1922 also lists Gabès and Zarzis separately, sgt1925 Gabès-Zarzis)
- `nationality`: nationality of the vine growers: `french`, `italian`, `anglo_maltese`, `other_european`, `tunisian` (Tunisiens, from sgt1924)
- `nationality_fr`: printed column heading
- `measure`: `growers` (Nombre de viticulteurs) or `area` (Superficie)
- `measure_fr`: printed heading
- `unit`: `growers` or `hectares` (printed hect. a., stored with two decimals)
- `value`: printed value (» = 0)
- `flag`: empty, or `total_mismatch`

Printed in sgt1922-sgt1925 (sub-table i) of the principales cultures). The TOTAUX line and the TOTAUX columns (des viticulteurs, des superficies) are checks only. sgt1922 lists 18 contrôles (Gabès, Gafsa and Zarzis separately), sgt1923 the same in alphabetical order, sgt1924 adds the Tunisiens columns, sgt1925 groups the contrôles by région (1re-5me Région with their chefs-lieux; Gabès-Zarzis together, Thala new, Gafsa dropped).

Notes printed with the table (translated): the Muslim vineyard, planted with table grapes and scattered in many small plots over the Regency, is not counted; sgt1922 and sgt1923 estimate it at 2.200 ha (total Tunisian vineyard 25.906 and 26.895 ha; sgt1923: of which 25.821 ha in production), sgt1925 at about 2.227 ha (European vineyard 27.986 ha, total 30.213 ha).

Every failed check below was re-read on a zoomed native-resolution crop: they are printed inconsistencies (printed values kept). Checks: every column against the TOTAUX line, every line's nationalities against its TOTAUX columns. sgt1922: the Italiens superficie of Sfax (1 45) and Tabarka (10 25) are printed 46 50 and 1 20 too low (their line totals 347 80 and 37 70 and the column TOTAUX 12.889 37 all need 47 95 and 11 45): flagged `total_mismatch`; the TOTAUX des viticulteurs is printed 2.499 for 2.439 (lines and nationalities agree on 2.439). sgt1923: the Grombalia total superficie 7.565 30 and the grand total 24.695 90 (also quoted in the observations) are 100 ha above the sum of the nationalities (7.465 30, 24.595 90); the Anglo-Maltais TOTAUX is printed 25 for 26 (lines). sgt1925: TOTAUX des viticulteurs printed 2.811 for 2.941 (lines and nationalities agree). Totals are not stored.

Survey of the whole chapter in every edition: `agriculture_survey.md`.

## Validation

- Checks against printed totals and identities: 194; passed: 181; failed: 13.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.226 (f250) vine it_ha: lines vs TOTAUX: cells give 12841.67, printed 12889.37 (difference 47.70)
  - sgt1922 p.226 (f250) vine tot_n: lines vs TOTAUX: cells give 2439, printed 2499 (difference 60)
  - sgt1922 p.226 (f250) vine tot_ha: lines vs TOTAUX: cells give 23706.81, printed 23706.80 (difference -0.01)
  - sgt1922 p.226 (f250) vine TOTAUX: nationalities vs TOTAUX (n): cells give 2439, printed 2499 (difference 60)
  - sgt1922 p.226 (f250) vine Sfax: nationalities vs TOTAUX (ha): cells give 301.30, printed 347.80 (difference 46.50)
  - sgt1922 p.226 (f250) vine Tabarka: nationalities vs TOTAUX (ha): cells give 36.50, printed 37.70 (difference 1.20)
  - sgt1922 p.226 (f250) vine TOTAUX: nationalities vs TOTAUX (ha): cells give 23706.81, printed 23706.80 (difference -0.01)
  - sgt1923 p.238 (f740) vine am_n: lines vs TOTAUX: cells give 26, printed 25 (difference -1)
  - sgt1923 p.238 (f740) vine TOTAUX: nationalities vs TOTAUX (n): cells give 2571, printed 2572 (difference 1)
  - sgt1923 p.238 (f740) vine Grombalia: nationalities vs TOTAUX (ha): cells give 7465.30, printed 7565.30 (difference 100.00)
  - sgt1923 p.238 (f740) vine TOTAUX: nationalities vs TOTAUX (ha): cells give 24595.90, printed 24695.90 (difference 100.00)
  - sgt1925 p.280 (f304) vine tot_n: lines vs TOTAUX: cells give 2941, printed 2811 (difference -130)
  - sgt1925 p.280 (f304) vine TOTAUX: nationalities vs TOTAUX (n): cells give 2941, printed 2811 (difference -130)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: total_mismatch: 2.

  - sgt1922 p.226 1922  /  / Sfax / italian / area / hectares = 1.45 (total_mismatch)
  - sgt1922 p.226 1922  /  / Tabarka / italian / area / hectares = 10.25 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (4 printings): sgt1922 f250, sgt1923 f740, sgt1924 f1242, sgt1925 f304.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
