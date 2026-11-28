# Laboratoire de chimie : analyses effectuées

*Chemistry laboratory: analyses made, by nature of sample and service.*

Source: *Statistique générale de la Tunisie*, chapter *Commerce et navigation*, editions sgt1922, sgt1923, sgt1924. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 403, f427; sgt1923 (`bpt6k9105649x`): p. 415, f917; sgt1924 (`bpt6k9105649x`): p. 431, f1421.

Transcriptions: `../transcribed/commerce_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_commerce.py build`.

Rows: 842. Years: 1922, 1923, 1924.

Unit: number of analyses. value_type: counts.

Selection: each edition prints a single year; no overlap, all stored.

## Columns

- `census`: edition (each edition prints one year)
- `table_id`: `chemistry` (Laboratoire de chimie, analyses effectuées)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: edition reference year (the table prints no year; assumed to be the edition's year)
- `sample`: row code (see sample_fr)
- `sample_fr`: nature des échantillons as printed (sub-lines of the Huiles and Produits brackets prefixed with the bracket heading)
- `service`: `customs`, `fraud_good`, `fraud_suspect`, `excise`, `other_admin`, `studies`, `public`
- `service_fr`: service column heading as printed
- `measure`: `analyses`
- `measure_fr`: analyses effectuées
- `unit`: `analyses`
- `value`: number of analyses as printed (» stored as 0)
- `flag`: empty or `total_mismatch` (misprinted cell, see notes)

Analyses made by the chemistry laboratory, by nature of the sample (rows) and requesting service (columns): customs (samples examined), fraud repression (samples found good / suspect), Contributions (headed *Contributions diverses* in sgt1922 and *Contributions indirectes* in sgt1923; the column is absent in sgt1924), other administrations, studies and research, paid analyses for the public. The line totals (TOTAUX par catégories) and the column totals (TOTAUX par service) are checks only, not stored. The list of samples changes between editions (sgt1922 prints alcohols and denatured alcohols, milk and condensed milk separately and essential oils; sgt1923 adds beets, cereals, glues; sgt1924 merges fertilisers and phosphates and adds products for pharmacies); every line printed is stored, with its designation as printed. No year is printed in the heading; the year stored is the edition's reference year.

Explanation of the failed checks (all cells re-read on zoomed native-resolution crops; printed values kept): sgt1922 marine_insurance public: printed », line TOTAL 216; the public column is short by 216 + 20; sgt1922 urines public: printed 5; line TOTAL 51 and the public column need 25; sgt1923 alcohol_denat customs: printed 55; line TOTAL 54 and the customs column need 53; sgt1924 prod_other fraud_good: printed 55; line TOTAL 126 and the Bons column need 5 (these four flagged `total_mismatch`). sgt1922: the customs column sums to 1.878 against TOTAUX 1.879 and the line totals sum to 5.007 against 5.008; every line agrees with its total apart from the two above, so the one-unit difference cannot be located (not flagged). sgt1924: the grand total is printed 5.255; the corrected columns and the line totals give 5.265 (the grand total is not stored).

Survey of the whole chapter: `commerce_survey.md`.

## Validation

- Checks against printed totals and identities: 152; passed: 141; failed: 11.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.403 (f427) chemistry customs: lines vs Totaux: cells give 1878, printed 1879 (difference 1)
  - sgt1922 p.403 (f427) chemistry public: lines vs Totaux: cells give 1034, printed 1270 (difference 236)
  - sgt1922 p.403 (f427) chemistry total: lines vs Totaux: cells give 5007, printed 5008 (difference 1)
  - sgt1922 p.403 (f427) chemistry marine_insurance: total = customs + fraud_good + fraud_suspect + excise + other_admin + studies + public: cells give 0, printed 216 (difference 216)
  - sgt1922 p.403 (f427) chemistry urines: total = customs + fraud_good + fraud_suspect + excise + other_admin + studies + public: cells give 31, printed 51 (difference 20)
  - sgt1923 p.415 (f917) chemistry customs: lines vs Totaux: cells give 1730, printed 1728 (difference -2)
  - sgt1923 p.415 (f917) chemistry alcohol_denat: total = customs + fraud_good + fraud_suspect + excise + other_admin + studies + public: cells give 56, printed 54 (difference -2)
  - sgt1924 p.431 (f1421) chemistry fraud_good: lines vs Totaux: cells give 350, printed 300 (difference -50)
  - sgt1924 p.431 (f1421) chemistry total: lines vs Totaux: cells give 5265, printed 5255 (difference -10)
  - sgt1924 p.431 (f1421) chemistry prod_other: total = customs + fraud_good + fraud_suspect + other_admin + studies + public: cells give 176, printed 126 (difference -50)
  - sgt1924 p.431 (f1421) chemistry Totaux: total = customs + fraud_good + fraud_suspect + other_admin + studies + public: cells give 5265, printed 5255 (difference -10)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: total_mismatch: 4.

  - sgt1922 p.403 1922 marine_insurance / public / analyses / analyses = 0 (total_mismatch)
  - sgt1922 p.403 1922 urines / public / analyses / analyses = 5 (total_mismatch)
  - sgt1923 p.415 1923 alcohol_denat / customs / analyses / analyses = 55 (total_mismatch)
  - sgt1924 p.431 1924 prod_other / fraud_good / analyses / analyses = 55 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (3 printings): sgt1922 f427, sgt1923 f917, sgt1924 f1421.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
