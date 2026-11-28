# Assurances mutuelles agricoles. a) Incendie ; b) Grêle ; c) et d) Accidents

*Agricultural mutual insurance: policies, insured values, contributions, subsidies, claims and costs by level of the mutual system (local caisses, regional caisse, reinsurers), fire, hail and accident branches, by year (1913-1935).*

Source: *Statistique générale de la Tunisie*, chapter *Institutions économiques et sociales / Mutualité agricole*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 438, f462, p. 439, f463; sgt1923 (`bpt6k9105649x`): p. 450, f952, p. 451, f953; sgt1924 (`bpt6k9105649x`): p. 460, f1450, p. 461, f1451; sgt1925 (`bpt6k9105650k`): p. 496, f520, p. 497, f521; sgt1926 (`bpt6k9105650k`): p. 464, f1028, p. 465, f1029; sgt1927 (`bpt6k91056510`): p. 464, f492, p. 465, f493; sgt1928 (`bpt6k91056510`): p. 468, f1020, p. 469, f1021; sgt1929 (`bpt6k9105652d`): p. 470, f498, p. 471, f499; sgt1930 (`bpt6k9105652d`): p. 476, f1034, p. 477, f1035; sgt1935 (`bpt6k9105653t`): p. 292, f312, p. 293, f313, p. 294, f314, p. 295, f315.

Transcriptions: `../transcribed/mutuality_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_mutuality.py build`.

Rows: 1080. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935.

Units: count (policies, claims) and francs (everything else; centimes as decimals); suggested value_type: mixed.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (rule 4 tables: the latest edition printing that year)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `branch`: insurance branch: `fire` (a) incendie), `hail` (b) grêle), `accident_common_law` (c) accidents de droit commun, sgt1935), `accident_work` (d), sgt1935: title lost in the binding, the table has a column on permanent infirmity and death, so presumably accidents du travail)
- `branch_fr`: printed sub-table heading
- `regional_caisse`: empty before 1933; from 1933 (sgt1935) the regional caisse « Tunis-Assurances » is split into `tunis_est` (Tunis-Est-Réassurances, line a) and `tunis` (Tunis-Réassurances, line b)
- `regional_caisse_fr`: printed name of the regional caisse (from the footnote)
- `measure`: measure code (English)
- `measure_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `ocr_corrected` (the Gallica OCR token at that cell was checked against the image and reads otherwise; cells the OCR simply misses or splits are not flagged), `illegible`, `not_applicable` (ristournes column not printed), `reprint_corrected` (see below)

Printed in sgt1922-sgt1930 and sgt1935 (two-page spreads; not printed in sgt1936 or sgt1939) for the ten years before the edition: sgt1922 1913-1922 ... sgt1930 1921-1930, sgt1935 1926-1935. a) incendie and b) grêle in every edition; sgt1935 adds c) accidents de droit commun and d) a second accident table (title lost in the binding) for 1933-1935. `source_page`/`gallica_view` give the page of the spread each cell is printed on.

Three layouts, harmonised on one set of measure codes (`measure_fr` = heading of the edition kept). sgt1922: cotisations versées and subventions by caisses locales / caisse régionale / caisse centrale, recettes supplémentaires et ristournes, total des recettes; nombre de sinistres, indemnités payées (three levels), autres frais (three levels and déficit des caisses locales), total des dépenses. sgt1923-sgt1930: the caisse centrale columns are headed *réassureurs* (same figures, so the same codes `*_central`); the subventions keep two levels; recettes diverses et ristournes split caisse locale / caisse régionale (`misc_receipts_*`; sgt1922's single column equals the régionale one, kept under its own code `receipts_extra_rebates`); the autres frais become frais de sinistre (`costs_*`, same figures as sgt1922's autres frais) and frais généraux divers et ristournes aux assurés (`general_costs_rebates_*`); no totals. sgt1935: sinistres et frais de sinistres, répartition des sommes payées (stored as `indemnities_*`: for 1926-1930 they equal the indemnités payées of sgt1926-sgt1930), déficit des caisses locales and ristournes aux assurés (`rebates_insured`; blank for 1926-1932, stored NA `not_applicable`); no frais de sinistre or frais généraux columns, so those measures stop in 1930.

sgt1922's total des recettes and total des dépenses columns are printed row totals: they are not stored, only checked (below). sgt1922-sgt1924 print a footnote (1) *frais de constitution* 8.150,20 above the first b) grêle line, in the subventions / caisse régionale and the autres frais / caisse régionale columns, not included in the totals; stored as year 1913 (the first year of the series) with measures `subsidies_regional_constitution` and `costs_regional_constitution`.

sgt1935, a) 1931: every left-page column except the réassureurs cotisations (1.393.482,21) is printed », stored 0 as printed (evidently not reported). The réassureurs cotisations column of a) and b) in sgt1935 runs into the binding and the second centime digit is hidden on both page edges for most lines: those cells are `illegible`; for 1926-1930 the value of the latest earlier printing (sgt1930) is stored with flag `reprint_corrected` (its legible digits agree), for 1932-1935 NA. b) 1921 subventions caisses locales is printed '.600' in sgt1923-sgt1930 (2.600 in sgt1922): stored 600 as printed. a) 1923 cotisations caisses locales is printed 4.483.963 » in sgt1923-sgt1929 and corrected to 44.839,63 in sgt1930 (kept). The same subvention locale a) 1919 is printed 883 in every edition (833 the years around it).

Overlap differences below the sgt1923-sgt1930 printings are few: sgt1922 prints the a) 1918 déficit des caisses locales 150,43 on its 1918 line, sgt1923 and later on 1919 (stored 1919 from sgt1930); sgt1926 prints the b) 1918 recettes diverses caisse régionale 2.428,31 (2.128,31 in every other printing; confirmed on a 4x crop of f1028, stored from sgt1927).

sgt1925 and sgt1926 were re-typed in full from their own native-resolution images (f520|521, f1028|1029); every other printing was read independently on its own image.

Every failed check below was re-read on a native-resolution crop: the printed values are kept. sgt1922 a) incendie: the total des recettes exceeds the seven receipt columns by 2.010,40 (1913), 3.167,40 (1914), 5.865,53 (1915) and 6.630,10 (1916), by 6,00 in 1918, and falls short by 49,91 in 1919 (the subvention locale is printed 883, not 833) and by 0,70 in 1922; b) grêle: the total des recettes falls short of the lines by 20,00 (1915) and 60,00 (1920), and the 1922 total des dépenses 80.930,06 is 3.999,90 above its lines. Every cell of these lines was re-read on zoomed crops (1.2-1.5x); the 1913-1916 differences look like receipts not shown in any column. No later edition prints totals, so they cannot be cross-checked.

Survey of the whole chapter in every edition: `mutuality_survey.md`.

## Validation

- Checks against printed totals and identities: 40; passed: 30; failed: 10.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.438 (f462) ins_fire 1913: receipts_total = contrib_local + contrib_regional + contrib_central + subsidy_local + subsidy_regional + subsidy_central + receipts_extra: cells give 66560.29, printed 68570.69 (difference 2010.40)
  - sgt1922 p.438 (f462) ins_fire 1914: receipts_total = contrib_local + contrib_regional + contrib_central + subsidy_local + subsidy_regional + subsidy_central + receipts_extra: cells give 64977.94, printed 68145.34 (difference 3167.40)
  - sgt1922 p.438 (f462) ins_fire 1915: receipts_total = contrib_local + contrib_regional + contrib_central + subsidy_local + subsidy_regional + subsidy_central + receipts_extra: cells give 141227.08, printed 147092.61 (difference 5865.53)
  - sgt1922 p.438 (f462) ins_fire 1916: receipts_total = contrib_local + contrib_regional + contrib_central + subsidy_local + subsidy_regional + subsidy_central + receipts_extra: cells give 101247.86, printed 107877.96 (difference 6630.10)
  - sgt1922 p.438 (f462) ins_fire 1918: receipts_total = contrib_local + contrib_regional + contrib_central + subsidy_local + subsidy_regional + subsidy_central + receipts_extra: cells give 224520.19, printed 224526.19 (difference 6.00)
  - sgt1922 p.438 (f462) ins_fire 1919: receipts_total = contrib_local + contrib_regional + contrib_central + subsidy_local + subsidy_regional + subsidy_central + receipts_extra: cells give 231109.16, printed 231059.25 (difference -49.91)
  - sgt1922 p.438 (f462) ins_fire 1922: receipts_total = contrib_local + contrib_regional + contrib_central + subsidy_local + subsidy_regional + subsidy_central + receipts_extra: cells give 386656.46, printed 386655.76 (difference -0.70)
  - sgt1922 p.438 (f462) ins_hail 1915: receipts_total = contrib_local + contrib_regional + contrib_central + subsidy_local + subsidy_regional + subsidy_central + receipts_extra: cells give 94384.96, printed 94364.96 (difference -20.00)
  - sgt1922 p.438 (f462) ins_hail 1920: receipts_total = contrib_local + contrib_regional + contrib_central + subsidy_local + subsidy_regional + subsidy_central + receipts_extra: cells give 352452.22, printed 352392.22 (difference -60.00)
  - sgt1922 p.438 (f462) ins_hail 1922: expend_total = indemn_local + indemn_regional + indemn_central + costs_local + costs_regional + costs_central + deficit_local: cells give 76930.16, printed 80930.06 (difference 3999.90)

- Overlapping printings: 2788 cell comparisons with other editions printing the same cell; 26 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1918 / fire /  / deficit_local_caisses | sgt1922 | 150.43 | sgt1927 | 0 |
| 1919 / fire /  / deficit_local_caisses | sgt1922 | 0 | sgt1928 | 150.43 |
| 1921 / hail /  / subsidies_local | sgt1922 | 2600 | sgt1930 | 600 |
| 1923 / fire /  / contributions_local | sgt1923 | 4483963 | sgt1930 | 44839.63 |
| 1923 / fire /  / contributions_local | sgt1924 | 4483963 | sgt1930 | 44839.63 |
| 1923 / fire /  / contributions_local | sgt1925 | 4483963 | sgt1930 | 44839.63 |
| 1923 / fire /  / contributions_local | sgt1926 | 4483963 | sgt1930 | 44839.63 |
| 1923 / fire /  / contributions_local | sgt1927 | 4483963 | sgt1930 | 44839.63 |
| 1923 / fire /  / contributions_local | sgt1928 | 4483963 | sgt1930 | 44839.63 |
| 1923 / fire /  / contributions_local | sgt1929 | 4483963 | sgt1930 | 44839.63 |
| 1918 / hail /  / misc_receipts_regional | sgt1926 | 2428.31 | sgt1927 | 2128.31 |
| 1926 / fire /  / contributions_central | sgt1926 | 486850.43 | sgt1935 |  |
| 1926 / fire /  / contributions_central | sgt1927 | 486850.43 | sgt1935 |  |
| 1926 / fire /  / contributions_central | sgt1928 | 486850.43 | sgt1935 |  |
| 1926 / fire /  / contributions_central | sgt1929 | 486850.43 | sgt1935 |  |
| 1926 / fire /  / contributions_central | sgt1930 | 486850.43 | sgt1935 |  |
| 1927 / fire /  / contributions_central | sgt1927 | 521105.73 | sgt1935 |  |
| 1927 / fire /  / contributions_central | sgt1928 | 521105.73 | sgt1935 |  |
| 1927 / fire /  / contributions_central | sgt1929 | 521105.73 | sgt1935 |  |
| 1927 / fire /  / contributions_central | sgt1930 | 521105.73 | sgt1935 |  |
| 1928 / fire /  / contributions_central | sgt1928 | 1296977.47 | sgt1935 |  |
| 1928 / fire /  / contributions_central | sgt1929 | 1296977.47 | sgt1935 |  |
| 1928 / fire /  / contributions_central | sgt1930 | 1296977.47 | sgt1935 |  |
| 1929 / fire /  / contributions_central | sgt1929 | 1429555.84 | sgt1935 |  |
| 1929 / fire /  / contributions_central | sgt1930 | 1429555.84 | sgt1935 |  |
| 1930 / fire /  / contributions_central | sgt1930 | 1262094.27 | sgt1935 |  |

- Flagged cells: illegible: 11, not_applicable: 14, ocr_corrected: 17, reprint_corrected: 5.

  - sgt1923 p.450 1914 fire /  / misc_receipts_regional / francs = 6094.65 (ocr_corrected)
  - sgt1923 p.450 1914 hail /  / misc_receipts_regional / francs = 132.23 (ocr_corrected)
  - sgt1926 p.464 1917 fire /  / insured_value / francs = 23231069 (ocr_corrected)
  - sgt1926 p.464 1917 fire /  / misc_receipts_regional / francs = 4368.37 (ocr_corrected)
  - sgt1928 p.469 1919 fire /  / indemnities_regional / francs = 2098.58 (ocr_corrected)
  - sgt1930 p.476 1924 fire /  / contributions_regional / francs = 182566.76 (ocr_corrected)
  - sgt1930 p.477 1924 hail /  / costs_local / francs = 285.93 (ocr_corrected)
  - sgt1930 p.477 1924 hail /  / general_costs_rebates_regional / francs = 26988.60 (ocr_corrected)
  - sgt1930 p.476 1926 fire /  / contributions_central / francs = 486850.43 (reprint_corrected)
  - sgt1930 p.477 1926 fire /  / general_costs_rebates_regional / francs = 48404.94 (ocr_corrected)
  - sgt1935 p.293 1926 fire /  / rebates_insured / francs = NA (not_applicable)
  - sgt1935 p.293 1926 hail /  / rebates_insured / francs = NA (not_applicable)
  - sgt1930 p.476 1927 fire /  / contributions_central / francs = 521105.73 (reprint_corrected)
  - sgt1935 p.293 1927 fire /  / rebates_insured / francs = NA (not_applicable)
  - sgt1935 p.293 1927 hail /  / rebates_insured / francs = NA (not_applicable)
  - sgt1930 p.476 1928 fire /  / contributions_central / francs = 1296977.47 (reprint_corrected)
  - sgt1930 p.477 1928 hail /  / general_costs_rebates_regional / francs = 86036.41 (ocr_corrected)
  - sgt1935 p.293 1928 fire /  / rebates_insured / francs = NA (not_applicable)
  - sgt1935 p.292 1928 hail /  / contributions_central / francs = 1046708.57 (ocr_corrected)
  - sgt1935 p.293 1928 hail /  / rebates_insured / francs = NA (not_applicable)
  - sgt1930 p.476 1929 fire /  / contributions_central / francs = 1429555.84 (reprint_corrected)
  - sgt1935 p.293 1929 fire /  / rebates_insured / francs = NA (not_applicable)
  - sgt1935 p.292 1929 hail /  / policies / count = 1098 (ocr_corrected)
  - sgt1935 p.292 1929 hail /  / contributions_central / francs = 1021825.51 (ocr_corrected)
  - sgt1935 p.293 1929 hail /  / rebates_insured / francs = NA (not_applicable)
  - sgt1930 p.476 1930 fire /  / contributions_central / francs = 1262094.27 (reprint_corrected)
  - sgt1930 p.477 1930 fire /  / costs_regional / francs = 15192.19 (ocr_corrected)
  - sgt1935 p.293 1930 fire /  / rebates_insured / francs = NA (not_applicable)
  - sgt1935 p.293 1930 hail /  / rebates_insured / francs = NA (not_applicable)
  - sgt1935 p.293 1931 fire /  / rebates_insured / francs = NA (not_applicable)
  - sgt1935 p.293 1931 hail /  / rebates_insured / francs = NA (not_applicable)
  - sgt1935 p.292 1932 fire /  / contributions_central / francs = NA (illegible)
  - sgt1935 p.293 1932 fire /  / rebates_insured / francs = NA (not_applicable)
  - sgt1935 p.292 1932 hail /  / policies / count = 1019 (ocr_corrected)
  - sgt1935 p.293 1932 hail /  / rebates_insured / francs = NA (not_applicable)
  - sgt1935 p.292 1933 fire / tunis_est / contributions_central / francs = NA (illegible)
  - sgt1935 p.292 1933 fire / tunis / contributions_central / francs = NA (illegible)
  - sgt1935 p.294 1933 accident_work / tunis / contributions_central / francs = 98992.21 (ocr_corrected)
  - sgt1935 p.292 1934 fire / tunis_est / contributions_central / francs = NA (illegible)
  - sgt1935 p.292 1934 fire / tunis / contributions_central / francs = NA (illegible)
  - sgt1935 p.292 1934 hail / tunis_est / contributions_central / francs = NA (illegible)
  - sgt1935 p.292 1934 hail / tunis / contributions_central / francs = NA (illegible)
  - sgt1935 p.292 1935 fire / tunis_est / contributions_central / francs = NA (illegible)
  - sgt1935 p.292 1935 fire / tunis / contributions_central / francs = NA (illegible)
  - sgt1935 p.292 1935 hail / tunis_est / contributions_central / francs = NA (illegible)
  - sgt1935 p.292 1935 hail / tunis / contributions_regional / francs = 145868.87 (ocr_corrected)
  - sgt1935 p.292 1935 hail / tunis / contributions_central / francs = NA (illegible)

## Image versus OCR

- Read cell by cell on the page images (25 printings): sgt1922 f462, sgt1922 f462, sgt1922 f462, sgt1923 f952, sgt1923 f952, sgt1923 f952, sgt1924 f1450, sgt1924 f1450, sgt1924 f1450, sgt1925 f520, sgt1925 f520, sgt1926 f1028, sgt1926 f1028, sgt1927 f492, sgt1927 f492, sgt1928 f1020, sgt1928 f1020, sgt1929 f498, sgt1929 f498, sgt1930 f1034, sgt1930 f1034, sgt1935 f312, sgt1935 f312, sgt1935 f314, sgt1935 f314.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 111.
