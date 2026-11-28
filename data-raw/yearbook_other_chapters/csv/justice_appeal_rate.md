# Usage du droit d'appel

*Use of the right of appeal.*

Source: *Statistique générale de la Tunisie*, chapter *Justice*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 70, f94; sgt1923 (`bpt6k9105649x`): p. 79, f577; sgt1924 (`bpt6k9105649x`): p. 77, f1067; sgt1925 (`bpt6k9105650k`): p. 79, f103; sgt1926 (`bpt6k9105650k`): p. 89, f653; sgt1927 (`bpt6k91056510`): p. 91, f115; sgt1928 (`bpt6k91056510`): p. 87, f639; sgt1929 (`bpt6k9105652d`): p. 89, f117; sgt1930 (`bpt6k9105652d`): p. 93, f651; sgt1935 (`bpt6k9105653t`): p. 59, f79; sgt1936 (`bpt6k91056547`): p. 46, f57; sgt1939 (`bpt6k9105739w`): p. 46, f52.

Transcriptions: `../transcribed/justice_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_justice.py build`.

Rows: 558. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939.

Unit: number of cases; `*_pct` in percent (two decimals as printed).

Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, `year` = the year of the figures; no year is printed twice, except the two-year columns of the presidents' table (section `presidents`), where the earlier year is taken from the later edition and compared (rule 4).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section name
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `tribunal`: court as printed
- `measure`: English code of the printed column (see measure_fr)
- `measure_fr`: printed French heading
- `value`: count of cases (integer); money in francs with centimes; percentages as printed
- `flag`: empty, `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable`, `reprint_corrected`

"Usage du droit d'appel": per regional court, appealable cases, number of appeals, and the printed percentage (moyenne pour cent, stored as printed, numeric). The TOTAUX line is a check only for the counts; the percentages are checked against 100 × appeals / appealable.

Percentages are stored as printed ("moyenne pour cent"; sgt1929 Driba civil is printed 27 002, sgt1935 Driba penal 13 178, i.e. with three decimals). The TOTAUX line prints no percentage from sgt1924 (NA, `not_applicable`); Béja (opened 1925) prints » until sgt1929 (stored 0 for counts, NA for percentages).

The page-by-page survey of the chapter in every edition (every table found, with views) is in `justice_survey.md` and in `justice_validation.json` (`_survey`).

## Validation

- Checks against printed totals and identities: 224; passed: 203; failed: 21.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.70 (f94) tn_appeal_rate Sfax: penal_pct = 100 x appeals / appealable (to 0.01): cells give 20.23, printed 2.22 (difference -18.01)
  - sgt1922 p.70 (f94) tn_appeal_rate Gabès: penal_pct = 100 x appeals / appealable (to 0.01): cells give 12.79, printed 12.50 (difference -0.29)
  - sgt1922 p.70 (f94) tn_appeal_rate TOTAUX: civil_pct = 100 x appeals / appealable (to 0.01): cells give 17.68, printed 17.66 (difference -0.02)
  - sgt1923 p.79 (f577) tn_appeal_rate Kef: civil_pct = 100 x appeals / appealable (to 0.01): cells give 11.30, printed 11.22 (difference -0.08)
  - sgt1925 p.79 (f103) tn_appeal_rate Driba: civil_pct = 100 x appeals / appealable (to 0.01): cells give 23.93, printed 23.96 (difference 0.03)
  - sgt1925 p.79 (f103) tn_appeal_rate Gabès: civil_pct = 100 x appeals / appealable (to 0.01): cells give 26.52, printed 26.37 (difference -0.15)
  - sgt1926 p.89 (f653) tn_appeal_rate Driba: civil_pct = 100 x appeals / appealable (to 0.01): cells give 24.62, printed 24.22 (difference -0.40)
  - sgt1927 p.91 (f115) tn_appeal_rate Gabès: penal_pct = 100 x appeals / appealable (to 0.01): cells give 19.07, printed 19.19 (difference 0.12)
  - sgt1928 p.87 (f639) tn_appeal_rate penal_appealable: lines vs TOTAUX: cells give 9589, printed 10219 (difference 630)
  - sgt1928 p.87 (f639) tn_appeal_rate Sousse: civil_pct = 100 x appeals / appealable (to 0.01): cells give 29.05, printed 29.71 (difference 0.66)
  - sgt1928 p.87 (f639) tn_appeal_rate Le Kef: civil_pct = 100 x appeals / appealable (to 0.01): cells give 35.71, printed 35.91 (difference 0.20)
  - sgt1928 p.87 (f639) tn_appeal_rate Sfax: penal_pct = 100 x appeals / appealable (to 0.01): cells give 63.98, printed 14.58 (difference -49.40)
  - sgt1929 p.89 (f117) tn_appeal_rate penal_appeals: lines vs TOTAUX: cells give 2494, printed 2495 (difference 1)
  - sgt1929 p.89 (f117) tn_appeal_rate Driba: penal_pct = 100 x appeals / appealable (to 0.01): cells give 20.06, printed 20.08 (difference 0.02)
  - sgt1930 p.93 (f651) tn_appeal_rate Le Kef: civil_pct = 100 x appeals / appealable (to 0.01): cells give 83.52, printed 83.44 (difference -0.08)
  - sgt1930 p.93 (f651) tn_appeal_rate Gafsa: penal_pct = 100 x appeals / appealable (to 0.01): cells give 24.46, printed 24.70 (difference 0.24)
  - sgt1935 p.59 (f79) tn_appeal_rate Béja: penal_pct = 100 x appeals / appealable (to 0.01): cells give 10.59, printed 10.51 (difference -0.08)
  - sgt1936 p.46 (f57) tn_appeal_rate penal_appealable: lines vs TOTAUX: cells give 18578, printed 18278 (difference -300)
  - sgt1936 p.46 (f57) tn_appeal_rate Gabès: penal_pct = 100 x appeals / appealable (to 0.01): cells give 19.11, printed 23.92 (difference 4.81)
  - sgt1939 p.46 (f52) tn_appeal_rate Sfax: penal_pct = 100 x appeals / appealable (to 0.01): cells give 19.78, printed 19.72 (difference -0.06)
  - sgt1939 p.46 (f52) tn_appeal_rate Béja: penal_pct = 100 x appeals / appealable (to 0.01): cells give 15.01, printed 14.99 (difference -0.02)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: not_applicable: 10, ocr_corrected: 12.

  - sgt1925 p.79 1925 Béja / civil_pct = NA (not_applicable)
  - sgt1926 p.89 1926 Béja / civil_pct = NA (not_applicable)
  - sgt1927 p.91 1927 Béja / civil_pct = NA (not_applicable)
  - sgt1928 p.87 1928 Béja / civil_pct = NA (not_applicable)
  - sgt1929 p.89 1929 Béja / civil_pct = NA (not_applicable)
  - sgt1925 p.79 1925 Béja / penal_pct = NA (not_applicable)
  - sgt1926 p.89 1926 Béja / penal_pct = NA (not_applicable)
  - sgt1927 p.91 1927 Béja / penal_pct = NA (not_applicable)
  - sgt1928 p.87 1928 Béja / penal_pct = NA (not_applicable)
  - sgt1929 p.89 1929 Béja / penal_pct = NA (not_applicable)
  - sgt1926 p.89 1926 Gafsa / civil_pct = 20.26 (ocr_corrected)
  - sgt1926 p.89 1926 Gafsa / penal_pct = 17.66 (ocr_corrected)
  - sgt1926 p.89 1926 Le Kef / penal_appealable = 1236 (ocr_corrected)
  - sgt1927 p.91 1927 Le Kef / penal_appealable = 1038 (ocr_corrected)
  - sgt1927 p.91 1927 Sfax / civil_appealable = 363 (ocr_corrected)
  - sgt1926 p.89 1926 Sfax / civil_appeals = 226 (ocr_corrected)
  - sgt1927 p.91 1927 Sfax / civil_appeals = 153 (ocr_corrected)
  - sgt1927 p.91 1927 Sfax / civil_pct = 42.14 (ocr_corrected)
  - sgt1927 p.91 1927 Sfax / penal_appealable = 1135 (ocr_corrected)
  - sgt1927 p.91 1927 Sfax / penal_appeals = 133 (ocr_corrected)
  - sgt1926 p.89 1926 Sfax / penal_pct = 16.38 (ocr_corrected)
  - sgt1927 p.91 1927 Sfax / penal_pct = 11.71 (ocr_corrected)

## Image versus OCR

- Read cell by cell on the page images (7 printings): sgt1924 f1067, sgt1926 f653, sgt1928 f639, sgt1930 f651, sgt1935 f79, sgt1936 f57, sgt1939 f52.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (5 printings): sgt1922 f94, sgt1923 f577, sgt1925 f103, sgt1927 f115, sgt1929 f117.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 13.
