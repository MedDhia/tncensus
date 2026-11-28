# Hôpital civil français de Tunis : répartition des journées par pavillon

*French Civil Hospital of Tunis: patient-days by ward (pavilion).*

Source: *Statistique générale de la Tunisie*, chapter III (health), editions sgt1922, sgt1924, sgt1925. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1922 (`bpt6k9105649x`): p. 48, f72; sgt1924 (`bpt6k9105649x`): p. 56, f1046; sgt1925 (`bpt6k9105650k`): p. 56, f80.

Transcriptions: `../transcribed/health_pop_<edition>.txt`, section `@civil_ward_days`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_population.py build`. Per-check output: `health_validation.json`.

Rows: 97. Years: 1921–1925.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition) and every other printing of the same cell is compared below. Duplicate printings are not stored.

Years printed by each edition: sgt1922 1921–1922; sgt1923 1922–1923; sgt1924 1923–1924; sgt1925 1924–1925.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to
- `ward_fr`: as printed
- `value`: count (integer), except where the notes say otherwise; printed » = 0
- `flag`: empty, or `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (row totals, TOTAUX lines, nationality brackets) and the printed "différence en plus / en moins" columns are not stored; they were used for validation.

Table b) "Répartition des journées par pavillon", printed in sgt1922–sgt1925 only (two year columns plus differences). Ward labels are as printed and change between editions: sgt1924 and sgt1925 split the wards by sex/age (Hommes, Femmes, Enfants) and rename some (D = André Vullien, E. Ch. = Enfants Chirurgie, Isolés = Contagieux, Nx = Nerveux; Tribaudeau/Tribeaudeau). For the overlap comparison these names were matched; the stored `ward_fr` is the label of the edition the value comes from. The bracket subtotal "G" (Hommes + Femmes) and TOTAUX are not stored.

**sgt1922, 1921 column**: Maternité 14.235 and Enfants 10.556 are misprints: the printed differences (en moins 18, en plus 666) imply 10.165 and 16.556, and with them the column sums to 88.859, the 1921 patient-days of table c). The printed column total 92.929 is also wrong (cells as printed sum to 86.929). Printed values kept, flagged `total_mismatch`.

**sgt1923** reprints the 1922 column with the old wards in bold and three re-classified wards added (André Vullien 5.505, Tribaudeau 10.147, Enfants (Chirurgie) 7.844), so that the column sums to its printed 113.524 instead of the 90.028 patient-days printed in both editions; its 1923 column counts Enfants 4.667 twice (also under André Vullien), summing to 94.568 instead of 89.901 (sgt1924). Rule 4 is therefore overridden for 1922 (taken from sgt1922, whose 14 cells equal sgt1923's bold cells), and 1923 comes from sgt1924 as rule 4 says. The sgt1923 1923 cells were compared with sgt1924 after aggregation: A, B, C, G, H, K, Dispensaire, Dr Cuénod and Tribaudeau are equal; Maternité 4.096 = Enfants nés 3.345 + Enfants avec mère 751; Nerveux 4.760 = 2.802 + 1.857 + 101; Contagieux 4.861 = Isolés 1.518 + 1.678 + 1.665; André Vullien 4.694 = D 27 + 4.667; Enfants (Chirurgie) 6.865 = 218 + 6.647.

sgt1925: Tribeaudeau 9.116 → 10.996 is printed with a difference of 1.180 (1.880), and the en-plus column total 5.228 agrees with the correct 1.880, not with the printed 1.180 (re-read at full resolution).

## Validation

- Checks against printed totals: 100; passed: 91; failed: 9.

Failed checks (printed values kept; every one was re-read on the page image and the printed figures are as transcribed; see the commentary above for the cells involved):

  - sgt1922 civil_ward_days Maternité: difference: cells give -4088, printed -18
  - sgt1922 civil_ward_days Enfants: difference: cells give 6666, printed 666
  - sgt1922 civil_ward_days TOTAUX: difference: cells give -2901, printed 1169
  - sgt1922 ward days col 1: wards vs TOTAUX: cells give 86929, printed 92929
  - sgt1923 civil_ward_days Maternité: difference: cells give -6051, printed 0
  - sgt1923 civil_ward_days Enfants: difference: cells give -12555, printed 0
  - sgt1923 civil_ward_days TOTAUX: difference: cells give -18956, printed -350
  - sgt1925 civil_ward_days Tribeaudeau: difference: cells give 1880, printed 1180
  - sgt1925 ward days col 2: wards vs TOTAUX: cells give 4528, printed 5228

- Overlapping printings: 47 cell comparisons between editions; 0 differences.

- Flagged cells: total_mismatch: 2.

  - sgt1922 1921 Maternité = 14235 (total_mismatch)
  - sgt1922 1921 Enfants = 10556 (total_mismatch)
