# Consommation : animaux abattus

*Consumption: animals slaughtered, by commune.*

Source: *Statistique générale de la Tunisie*, chapter *Commerce et navigation*, editions sgt1922, sgt1923, sgt1924. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 380, f404, p. 381, f405, p. 382, f406, p. 383, f407; sgt1923 (`bpt6k9105649x`): p. 392, f894, p. 393, f895, p. 394, f896, p. 395, f897; sgt1924 (`bpt6k9105649x`): p. 408, f1398, p. 409, f1399, p. 410, f1400, p. 411, f1401.

Transcriptions: `../transcribed/commerce_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_commerce.py build`.

Rows: 1298. Years: 1922, 1923, 1924.

Unit: head (number of animals), as printed. value_type: count.

Selection: each edition prints a single year; no overlap.

## Columns

- `census`: edition (each prints one year; no overlap)
- `table_id`: `slaughter` (Consommation : animaux abattus)
- `gallica_ark`: Gallica volume ark
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: reference year of the edition (not printed: 1922, 1923, 1924)
- `commune`: commune as printed in that edition
- `species`: `cattle`, `calves`, `sheep`, `goats`, `pigs`, `horses` (sgt1924 only), `camels`, `other`
- `species_fr`: column heading as printed
- `measure`: `animals_slaughtered`
- `measure_fr`: animaux abattus
- `unit`: `head`
- `value`: number of animals as printed (» stored as 0); empty when the slaughter dues were farmed out or not yet instituted
- `flag`: empty, `not_applicable`, `row_realigned` or `total_mismatch` (see notes)

Animals slaughtered, by commune and species, one year per edition (the reference year, not printed). The table runs over two spreads (A reporter / Report); the TOTAUX column and line and the A reporter / Report lines are not stored, they were used as checks. Footnote (1) in sgt1922 and sgt1923 (translated): animals slaughtered outside the centres constituted as communes are not included.

Columns: sgt1922 and sgt1923 print seven species (bœufs ou vaches, veaux, moutons, chèvres, porcs, chameaux, autres); sgt1924 adds *chevaux, mulets* and prints *moutons, agneaux* and *chèvres, chevreaux*. Communes as printed in each edition (sgt1924 writes *Ariana (L')*, *El-Hamma*, *Le Kef*, *La Marsa*, *Zazhouan* [sic] ...; sgt1923 prints Souk-el-Arba before Soliman). No English translation or harmonisation of commune names is attempted.

Not applicable: sgt1923 Ksour-Essaf and Medjez-el-Bab (*Droits affermés*: slaughter dues farmed out) and Maharès (*Taxe instituée en 1924*); sgt1924 Medjez-el-Bab (*Droits d'abatage affermés*): stored empty with `not_applicable`. sgt1924 Souk-el-Arba total printed *10.358 et 829 kig. viande foraine* (829 kg of meat brought in from outside; not stored).

sgt1924: the bœufs of Tunis and Tozeur are printed 228 and 37.622, evidently interchanged (the two row totals, 231.499 and 7.977, agree only with the swap); stored realigned, flagged `row_realigned`.

Explanation of the failed checks (every cell concerned re-read on native-resolution crops). sgt1922: Bizerte prints total 23.799 for lines summing to 27.399, and the A reporter line prints chèvres 68.683 and total 246.632 where the lines give 67.783 and 245.732; the TOTAUX line agrees with the lines (the Report line repeats the misprinted A reporter, hence the second-spread failures of 900). Totals only, nothing stored is affected. sgt1923: Sfax pigs printed 203; the Sfax total (62.067) and the pigs TOTAUX (5.670) both need 208, so the cell is flagged `total_mismatch` (printed value kept). The moutons TOTAUX (379.833) and the grand total (668.683) are 10 below the lines; no single cell could be located (the moutons column lies against the binding but every figure is legible). sgt1924: several lines do not add to their printed totals (Ferryville +6, Foum-Tatahouine -11, Souk-el-Arba -7, Teboursouk +9) and the A reporter / TOTAUX lines differ from the column sums (moutons, chameaux, total on the first spread; bœufs 18.009 lower, veaux 100 lower, chèvres and porcs slightly higher on the second). The printed TOTAUX line is consistent with itself (the species add to 704.508 within one unit), so it was evidently set from different figures than the lines; the cells stand as printed and nothing is flagged.

Survey of the whole chapter: `commerce_survey.md`.

## Validation

- Checks against printed totals and identities: 223; passed: 202; failed: 21.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 f404 Bizerte: total = sum of species: cells give 27399, printed 23799 (difference -3600)
  - sgt1922 f404 A reporter goats = lines: cells give 67783, printed 68683 (difference 900)
  - sgt1922 f404 A reporter total = lines: cells give 242132, printed 246632 (difference 4500)
  - sgt1922 f406 Totaux goats = lines + Report: cells give 175007, printed 174107 (difference -900)
  - sgt1922 f406 Totaux total = lines + Report: cells give 775487, printed 774587 (difference -900)
  - sgt1923 f896 Sfax: total = sum of species: cells give 62062, printed 62067 (difference 5)
  - sgt1923 f896 Totaux sheep = lines + Report: cells give 379843, printed 379833 (difference -10)
  - sgt1923 f896 Totaux pigs = lines + Report: cells give 5665, printed 5670 (difference 5)
  - sgt1923 f896 Totaux total = lines + Report: cells give 668693, printed 668683 (difference -10)
  - sgt1924 f1398 Ferryville: total = sum of species: cells give 5803, printed 5797 (difference -6)
  - sgt1924 f1398 Foum-Tatahouine: total = sum of species: cells give 13574, printed 13585 (difference 11)
  - sgt1924 f1398 A reporter sheep = lines: cells give 133590, printed 133600 (difference 10)
  - sgt1924 f1398 A reporter camels = lines: cells give 876, printed 877 (difference 1)
  - sgt1924 f1398 A reporter total = lines: cells give 239261, printed 239267 (difference 6)
  - sgt1924 f1400 Souk-el-Arba: total = sum of species: cells give 10351, printed 10358 (difference 7)
  - sgt1924 f1400 Teboursouk: total = sum of species: cells give 8476, printed 8467 (difference -9)
  - sgt1924 f1400 Totaux cattle = lines + Report: cells give 71362, printed 53353 (difference -18009)
  - sgt1924 f1400 Totaux calves = lines + Report: cells give 8997, printed 8897 (difference -100)
  - sgt1924 f1400 Totaux goats = lines + Report: cells give 184916, printed 184926 (difference 10)
  - sgt1924 f1400 Totaux pigs = lines + Report: cells give 5053, printed 5056 (difference 3)
  - sgt1924 f1400 Totaux total = lines + Report: cells give 722603, printed 704508 (difference -18095)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: not_applicable: 29, row_realigned: 2, total_mismatch: 1.

  - sgt1923 p.392 1923 Ksour-Essaf / cattle / animals_slaughtered / head = NA (not_applicable)
  - sgt1923 p.392 1923 Ksour-Essaf / calves / animals_slaughtered / head = NA (not_applicable)
  - sgt1923 p.392 1923 Ksour-Essaf / sheep / animals_slaughtered / head = NA (not_applicable)
  - sgt1923 p.393 1923 Ksour-Essaf / goats / animals_slaughtered / head = NA (not_applicable)
  - sgt1923 p.393 1923 Ksour-Essaf / pigs / animals_slaughtered / head = NA (not_applicable)
  - sgt1923 p.393 1923 Ksour-Essaf / camels / animals_slaughtered / head = NA (not_applicable)
  - sgt1923 p.393 1923 Ksour-Essaf / other / animals_slaughtered / head = NA (not_applicable)
  - sgt1923 p.392 1923 Maharès / cattle / animals_slaughtered / head = NA (not_applicable)
  - sgt1923 p.392 1923 Maharès / calves / animals_slaughtered / head = NA (not_applicable)
  - sgt1923 p.392 1923 Maharès / sheep / animals_slaughtered / head = NA (not_applicable)
  - sgt1923 p.393 1923 Maharès / goats / animals_slaughtered / head = NA (not_applicable)
  - sgt1923 p.393 1923 Maharès / pigs / animals_slaughtered / head = NA (not_applicable)
  - sgt1923 p.393 1923 Maharès / camels / animals_slaughtered / head = NA (not_applicable)
  - sgt1923 p.393 1923 Maharès / other / animals_slaughtered / head = NA (not_applicable)
  - sgt1923 p.394 1923 Medjez-el-Bab / cattle / animals_slaughtered / head = NA (not_applicable)
  - sgt1923 p.394 1923 Medjez-el-Bab / calves / animals_slaughtered / head = NA (not_applicable)
  - sgt1923 p.394 1923 Medjez-el-Bab / sheep / animals_slaughtered / head = NA (not_applicable)
  - sgt1923 p.395 1923 Medjez-el-Bab / goats / animals_slaughtered / head = NA (not_applicable)
  - sgt1923 p.395 1923 Medjez-el-Bab / pigs / animals_slaughtered / head = NA (not_applicable)
  - sgt1923 p.395 1923 Medjez-el-Bab / camels / animals_slaughtered / head = NA (not_applicable)
  - sgt1923 p.395 1923 Medjez-el-Bab / other / animals_slaughtered / head = NA (not_applicable)
  - sgt1923 p.395 1923 Sfax / pigs / animals_slaughtered / head = 203 (total_mismatch)
  - sgt1924 p.410 1924 Medjez-el-Bab / cattle / animals_slaughtered / head = NA (not_applicable)
  - sgt1924 p.410 1924 Medjez-el-Bab / calves / animals_slaughtered / head = NA (not_applicable)
  - sgt1924 p.410 1924 Medjez-el-Bab / sheep / animals_slaughtered / head = NA (not_applicable)
  - sgt1924 p.411 1924 Medjez-el-Bab / goats / animals_slaughtered / head = NA (not_applicable)
  - sgt1924 p.411 1924 Medjez-el-Bab / pigs / animals_slaughtered / head = NA (not_applicable)
  - sgt1924 p.411 1924 Medjez-el-Bab / horses / animals_slaughtered / head = NA (not_applicable)
  - sgt1924 p.411 1924 Medjez-el-Bab / camels / animals_slaughtered / head = NA (not_applicable)
  - sgt1924 p.411 1924 Medjez-el-Bab / other / animals_slaughtered / head = NA (not_applicable)
  - sgt1924 p.410 1924 Tunis / cattle / animals_slaughtered / head = 37622 (row_realigned)
  - sgt1924 p.410 1924 Tozeur / cattle / animals_slaughtered / head = 228 (row_realigned)

## Image versus OCR

- Read cell by cell on the page images (6 printings): sgt1922 f404, sgt1922 f406, sgt1923 f894, sgt1923 f896, sgt1924 f1398, sgt1924 f1400.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
