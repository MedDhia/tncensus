# Navigation : d) cabotage ; mouvement par port d'expédition et de destination

*Navigation: coastal trade, by port of dispatch and destination.*

Source: *Statistique générale de la Tunisie*, chapter *Commerce et navigation*, editions sgt1922, sgt1923, sgt1924. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 409, f433; sgt1923 (`bpt6k9105649x`): p. 421, f923; sgt1924 (`bpt6k9105649x`): p. 437, f1427.

Transcriptions: `../transcribed/commerce_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_commerce.py build`.

Rows: 150. Years: 1922, 1923, 1924.

Unit: quintaux métriques (100 kg), as printed, not converted. value_type: quintaux.

Selection: each edition prints a single year; no overlap.

## Columns

- `census`: edition (each edition prints one year, its reference year)
- `table_id`: `navigation_d` (d) Cabotage ; mouvement par port d'expédition et de destination)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the movement (not printed in the heading; the reference year of the edition, confirmed by c) sur le littoral)
- `port`: port as printed (*Ports non occupés* = unstaffed ports, as printed)
- `direction`: `dispatch` (port d'expédition) or `destination` (port de destination)
- `direction_fr`: as printed
- `measure`: `cargo_weight`
- `measure_fr`: poids des cargaisons
- `unit`: `quintaux` (quintaux métriques, 100 kg; not converted)
- `value`: as printed (» stored as 0)
- `flag`: empty

Coastal trade (cabotage): weight of cargoes by port of dispatch and by port of destination, 25 ports (the same list in the three editions), quintaux métriques. Each cargo is counted once at each end, so the two TOTAUX are equal; TOTAUX not stored (checked against the lines).

Year: not printed; the reference year of each edition (1922, 1923, 1924), as for a) par port. No overlap between editions.

Survey of the whole chapter: `commerce_survey.md`.

## Validation

- Checks against printed totals and identities: 6; passed: 6; failed: 0.

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (3 printings): sgt1922 f433, sgt1923 f923, sgt1924 f1427.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
