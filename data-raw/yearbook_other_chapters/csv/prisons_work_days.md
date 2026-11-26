# Journées de travail des détenus

*Days of work of the prisoners, by prison and work site.*

Source: *Statistique générale de la Tunisie*, chapter *Établissements pénitentiaires*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 74, f98; sgt1923 (`bpt6k9105649x`): p. 80, f582; sgt1924 (`bpt6k9105649x`): p. 82, f1072; sgt1925 (`bpt6k9105650k`): p. 84, f108; sgt1926 (`bpt6k9105650k`): p. 94, f658, p. 95, f659; sgt1927 (`bpt6k91056510`): p. 92, f120, p. 93, f121; sgt1928 (`bpt6k91056510`): p. 92, f644, p. 93, f645; sgt1929 (`bpt6k9105652d`): p. 94, f122, p. 95, f123; sgt1930 (`bpt6k9105652d`): p. 98, f656, p. 99, f657.

Transcriptions: `../transcribed/prisons_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_prisons.py build`.

Rows: 1983. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930.

Unit: days of work (prisoner-days).

Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, with `year`; no year is printed by two editions.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section name (`work_days`); printed as table c)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (sgt1926-sgt1930: the table is a two-page spread; each cell has the page it is printed on)
- `gallica_view`: Gallica view (fNNNN) of the page the cell is printed on
- `year`: year of the figures (the edition year: each edition prints the table for its own year)
- `establishment`: prison (*établissement*) as printed
- `work`: work site code, one per printed column heading (codes shared by editions whose heading is the same); see `work_fr`
- `work_fr`: printed column headings, from the group heading down (e.g. "Chantiers extérieurs : entretien des détenus à la charge des employeurs : Mines")
- `value`: days of work of the prisoners (*journées de travail*)
- `flag`: empty, `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable` (SPEC.md)

Table c) of the chapter, printed sgt1922-sgt1930 (sgt1935, sgt1936 and sgt1939 print no such table). The column headings are recast almost every edition: sgt1922-sgt1924 split *chantiers extérieurs* from *chantiers mixtes ou intérieurs*; from sgt1925 the outside work sites are split by who pays the prisoners' upkeep (*à la charge des employeurs* / *de l'Administration*) and the inside ones from sgt1926 by *Entrepreneurs* / *État* (sgt1927-sgt1930: *Administration*). Each printed column is kept with its own heading in `work_fr`; no attempt is made to harmonise them.

The establishment lines also change (the Colonie des jeunes détenus line, all », sgt1922-sgt1924; La Goulette not printed sgt1927-sgt1930). Names as printed: Bardo / Le Bardo is "Bardo" in this table; Dj.-Djougar, Pénitencier du Djougar (sgt1926), Djebel Djougar (sgt1927-sgt1930).

Not stored: the "Total par établissement" / "Total général" column and the "Totaux" line (the checks: each line's cells against its total, each column against the Totaux line). In sgt1922-sgt1924 the total column runs into the binding; its digits were read on enlarged crops.

sgt1923 footnotes: "Le nombre de journées des détenus employés aux scourtins du chantier mixte de La Goulette est de 2.789. Le nombre de journées des détenus employés aux minerais et phosphates du chantier mixte de La Goulette est de 12.627." (days of the prisoners employed on the scourtins, and on minerals and phosphates, at the mixed work site of La Goulette). These 15.416 days are not in any column but are in the printed grand total: the line totals and the column totals both sum to 407.692, the printed grand total is 423.108 = 407.692 + 2.789 + 12.627. The footnote days are not stored as cells; the grand-total check is the only failure they cause.

sgt1925: the cells are printed with a vertical jitter of up to one line; each line was matched to its cells through its printed total (every line then checks, so the matching is unique).

Failures involving only printed totals (no stored cell flagged; re-read on enlarged crops): sgt1925 Contrôles civils / détenus nourris dans les prisons, Totaux printed 10.070 for lines summing to 10.077 (the Totaux line's own total 412.926 needs 10.077); sgt1928 Sfax, total printed 8.495 for cells summing to 8.195 (the total column's sum then gives the printed 573.680).

Every cell of every edition was read on the native-resolution page images (one crop per page of the table), and each failing line or column re-read on a separate enlarged crop.

Cells flagged `total_mismatch` (printed value kept, re-read on a native-resolution crop): sgt1922: Sfax / espadrilles_alfa (Sfax, Espadrilles, alfa printed 1.845: the Sfax line sums to 6.512 for a printed 6.482 and the column to 34.842 for a printed 34.812, both 30 over at this cell); sgt1923: Tunis / espadrilles_alfa (Tunis, Espadrilles, alfa printed 1.851: neither the Tunis total (92.783, the other cells sum to exactly that) nor the column total (41.130, the other cells sum to exactly that) counts it).

Cells flagged `row_realigned` (stored on the line their content belongs to): sgt1925 Gabès / int_scourtins_mats_brooms: printed one line higher, on the Bizerte line; on the printed line neither that line nor this one gives its printed Total par établissement, stored here both do; sgt1925 La Goulette / int_scourtins_mats_brooms: printed one line higher, on the Gafsa line; on the printed line neither that line nor this one gives its printed Total par établissement, stored here both do; sgt1925 Sfax / int_scourtins_mats_brooms: printed one line higher, on the Porto-Farina line; on the printed line neither that line nor this one gives its printed Total par établissement, stored here both do; sgt1925 Dj.-Djougar / int_scourtins_mats_brooms: printed one line higher, on the Sousse line; on the printed line neither that line nor this one gives its printed Total par établissement, stored here both do.

## Validation

- Checks against printed totals and identities: 289; passed: 279; failed: 10.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.74 (f98) work_days Sfax: total = ext_agriculture + ext_saline + ext_hopital_sadiki + public_works + roads_municipality + agri_education + agri_hospitals + agri_controles + agri_prisons + agri_other + saline + mines_phosphates + espadrilles_alfa + other: cells give 6512, printed 6482 (difference -30)
  - sgt1922 p.74 (f98) work_days espadrilles_alfa: lines vs Totaux: cells give 34842, printed 34812 (difference -30)
  - sgt1923 p.80 (f582) work_days Tunis: total = ext_agriculture_livestock + ext_saline + ext_hospitals + public_works + roads_sweeping + agri_agricultural_education + agri_hospitals + agri_public_gardens + agri_prisons + agri_companies + colleges_schools + saline + espadrilles_alfa + controles_civils + other: cells give 94634, printed 92783 (difference -1851)
  - sgt1923 p.80 (f582) work_days Totaux: total = ext_agriculture_livestock + ext_saline + ext_hospitals + public_works + roads_sweeping + agri_agricultural_education + agri_hospitals + agri_public_gardens + agri_prisons + agri_companies + colleges_schools + saline + espadrilles_alfa + controles_civils + other: cells give 407692, printed 423108 (difference 15416)
  - sgt1923 p.80 (f582) work_days espadrilles_alfa: lines vs Totaux: cells give 42981, printed 41130 (difference -1851)
  - sgt1923 p.80 (f582) work_days total: lines vs Totaux: cells give 407692, printed 423108 (difference 15416)
  - sgt1925 p.84 (f108) work_days Totaux: total = emp_agricultural + emp_salines + emp_hospitals + emp_education_municipality + adm_controles_fed_gaols + adm_controles_fed_prisons + adm_municipalities + adm_agricultural + adm_hospitals_asylums_orphanages + adm_education_agriculture + adm_public_works + adm_mines_phosphates + int_espadrilles + int_scourtins_mats_brooms + int_other: cells give 412919, printed 412926 (difference 7)
  - sgt1925 p.84 (f108) work_days adm_controles_fed_prisons: lines vs Totaux: cells give 10077, printed 10070 (difference -7)
  - sgt1928 p.92 (f644) work_days Sfax: total = emp_municipalities + emp_agricultural + emp_education + emp_hospitals + emp_agriculture_directorate + emp_salines + emp_mines + adm_controles_detached_gaols + adm_controles_in_prisons + adm_municipalities + adm_agricultural + adm_hospitals_lazarets + adm_public_works + adm_courts + adm_education + int_contractors_espadrilles + int_contractors_coffee_sorting + int_contractors_scourtins + int_admin_buildings_misc: cells give 8195, printed 8495 (difference 300)
  - sgt1928 p.92 (f644) work_days total: lines vs Totaux: cells give 573980, printed 573680 (difference -300)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: row_realigned: 4, total_mismatch: 2.

  - sgt1922 p.74 1922 Sfax / espadrilles_alfa = 1845 (total_mismatch)
  - sgt1923 p.80 1923 Tunis / espadrilles_alfa = 1851 (total_mismatch)
  - sgt1925 p.84 1925 Gabès / int_scourtins_mats_brooms = 1215 (row_realigned)
  - sgt1925 p.84 1925 La Goulette / int_scourtins_mats_brooms = 1208 (row_realigned)
  - sgt1925 p.84 1925 Sfax / int_scourtins_mats_brooms = 2922 (row_realigned)
  - sgt1925 p.84 1925 Dj.-Djougar / int_scourtins_mats_brooms = 4300 (row_realigned)

## Image versus OCR

- Read cell by cell on the page images (9 printings): sgt1922 f98, sgt1923 f582, sgt1924 f1072, sgt1925 f108, sgt1926 f658, sgt1927 f120, sgt1928 f644, sgt1929 f122, sgt1930 f656.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
