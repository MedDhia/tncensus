# Poids et mesures

*Weights and measures: first and periodic verification of instruments.*

Source: *Statistique générale de la Tunisie*, chapter *Commerce et navigation*, editions sgt1922, sgt1923, sgt1924. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 401, f425, p. 402, f426; sgt1923 (`bpt6k9105649x`): p. 413, f915, p. 414, f916; sgt1924 (`bpt6k9105649x`): p. 429, f1419, p. 430, f1420.

Transcriptions: `../transcribed/commerce_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_commerce.py build`.

Rows: 368. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924.

Units: counts as printed (see `unit`); fees and stamp duty in francs with centimes; never converted. value_type: mixed.

Selection: a) and b) print the edition's reference year only (all stored). c) prints the last ten years (SPEC_ADDENDUM rule 4): each year stored once, from the latest edition printing it; every other printing compared cell by cell.

## Columns

- `census`: edition the value is taken from (a), b): the edition's reference year; c): rule 4)
- `table_id`: `weights_a` (a) Vérification première des instruments), `weights_b` (b) Vérification périodique), `weights_c` (c) Résultats généraux, ten years)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the verification
- `circonscription`: verification district code; `all` for the c) country totals
- `circonscription_fr`: as printed (Tunis 1re/2e, and 3e from 1924, bracketed in a))
- `measure`: column code (see measure_fr)
- `measure_fr`: column heading as printed
- `unit`: `makers`, `instruments`, `persons` (assujettis), `establishments`, `reports` (procès-verbaux) or `francs`
- `value`: as printed (» stored as 0; francs with centimes)
- `flag`: empty or `total_mismatch` (misprinted cell, see notes)

Three tables per edition: a) Vérification première des instruments (makers who deposited their mark and who practised in the year, instruments presented: made in Tunisia, renovated, imported; instruments admitted and refused) and b) Vérification périodique (persons subject to verification, amount of fees and stamp duty in francs, public establishments verified free of charge, defective instruments adjusted or taken out of service, reports drawn up), both by circonscription for the edition's reference year; c) Résultats généraux, the country totals of both for the last ten years. In a) the Tunis circonscriptions are bracketed into one line (1re and 2e; 1re, 2e and 3e in sgt1924, which adds a 3e Tunis to b)). The a) heading reads 'exercé leur profession en 1921' in sgt1922 (1923 and 1924 in the later editions), stored as printed. Footnote (1) to Importés: weights and measures that passed the first verification in France are exempt in Tunisia. The TOTAUX lines are checks only; c) for the reference year repeats the a) and b) TOTAUX (compared, stored once in each table as printed).

Checks: column totals (TOTAUX) of a) and b); in a) on every line made + renovated + imported = admitted + refused; c) reference year = TOTAUX of a) (instruments presented) and b). Explanation of the failed checks (re-read on native-resolution crops; printed values kept and flagged `total_mismatch`): sgt1922 a) 1re-2e Tunis admitted printed 13.073 (column admitted sums to 20.918 against TOTAUX 21.021, and the line is short by the same 103); sgt1923 a) 1re-2e Tunis renovated printed 1.423 (column sums to 8.667 against TOTAUX 9.667, the line short by the same 1.000). The TOTAUX and c) agree with the corrected values. sgt1924 b) Rajustés: the seven lines sum to 22.005, TOTAUX (and c) 1924) 22.004; every cell re-read on a zoomed crop, the misprint cannot be located, nothing flagged.

Survey of the whole chapter: `commerce_survey.md`.

## Validation

- Checks against printed totals and identities: 93; passed: 88; failed: 5.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.401 (f425) weights_a admitted: lines vs Totaux: cells give 20918, printed 21021 (difference 103)
  - sgt1922 p.401 (f425) weights_a tunis_1_2: admitted = made_tunisia + renovated + imported + -refused: cells give 13176, printed 13073 (difference -103)
  - sgt1923 p.413 (f915) weights_a renovated: lines vs Totaux: cells give 8667, printed 9667 (difference 1000)
  - sgt1923 p.413 (f915) weights_a tunis_1_2: admitted = made_tunisia + renovated + imported + -refused: cells give 15001, printed 16001 (difference 1000)
  - sgt1924 p.429 (f1419) weights_b adjusted: lines vs Totaux: cells give 22005, printed 22004 (difference -1)

- Overlapping printings: 198 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: total_mismatch: 2.

  - sgt1922 p.401 1922 tunis_1_2 / admitted / instruments = 13073 (total_mismatch)
  - sgt1923 p.413 1923 tunis_1_2 / renovated / instruments = 1423 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (9 printings): sgt1922 f425, sgt1922 f425, sgt1922 f426, sgt1923 f915, sgt1923 f915, sgt1923 f916, sgt1924 f1419, sgt1924 f1419, sgt1924 f1420.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
