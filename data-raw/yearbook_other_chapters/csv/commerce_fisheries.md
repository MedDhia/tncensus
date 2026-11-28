# Pêches maritimes par nationalité et par genre de pêche

*Sea fisheries, by nationality and type of fishing.*

Source: *Statistique générale de la Tunisie*, chapter *Commerce et navigation*, editions sgt1922, sgt1923, sgt1924. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 410, f434; sgt1923 (`bpt6k9105649x`): p. 422, f924; sgt1924 (`bpt6k9105649x`): p. 438, f1428.

Transcriptions: `../transcribed/commerce_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_commerce.py build`.

Rows: 252. Years: 1922, 1923, 1924.

Units: boats, tonneaux de jauge, persons, kg, francs, as printed. value_type: count (catch in kg and francs).

Selection: each edition prints a single year; no overlap.

## Columns

- `census`: edition (each edition prints one year, its reference year)
- `table_id`: `fisheries` (Pêches maritimes par nationalité et par genre de pêche)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the movement (not printed in the heading; the reference year of the edition, confirmed by c) sur le littoral)
- `fishing_type_fr`: genre de pêche as printed
- `ship_flag`: nationality of the boats (`tunisia`, `italy`, `france`, `greece`, `anglo_maltese`); `all` for foot fishers and the catch, printed for all nationalities together
- `ship_flag_fr`: as printed (empty for `all`)
- `measure`: `boats`, `tonnage`, `crew`, `foot_fishers`, `catch_weight`, `catch_value`
- `measure_fr`: column as printed
- `unit`: `boats`, `tons register`, `persons`, `kg`, `francs`
- `value`: as printed (» stored as 0; empty when the francs were not yet received)
- `flag`: empty or `not_applicable` (value not yet received, footnote)

Sea fisheries by type of fishing and nationality of the boats: boats, register tonnage and crews for Tunisian, Italian, French, Greek and Anglo-Maltese boats; foot fishers (pêcheurs à pied) and the catch in kilograms and francs, printed for all nationalities together (`ship_flag` = `all`). The *Récapitulation* columns and the TOTAUX line are not stored; they were used as checks (nationalities = récapitulation on every line; lines = TOTAUX).

Types of fishing as printed: sgt1922 prints four lines (Sardines, Anchois, Allaches; Pêches en mer et dans les lacs; Éponges; Thonaires); sgt1923 and sgt1924 split sea and lake fishing (printed *Pêche en mer* and *— dans les lacs*, typed *Pêche dans les lacs*). No English translation is attempted.

Year: not printed; the reference year of each edition (1922, 1923, 1924), as for the navigation tables. No overlap between editions.

Missing values: sgt1922 prints `(1)` for the francs of sea/lake fishing, of the thonaires and of the total, with the footnote *Au moment de mettre sous presse ces renseignements ne nous sont pas encore parvenus*: stored empty with `not_applicable`. sgt1923 prints » » for the catch of *Pêche en mer* (stored 0 as printed, though evidently not reported). sgt1924: the kg of *Pêche en mer* carries the footnote *A l'exception des ports de : Hammamet, Monastir, Mahdia*.

Gutter: the Greek crews column lies against the binding on the left page; every cell was read on the native-resolution crop (cut digits repeated at the edge of the right page) and equals the récapitulation minus the other nationalities.

Survey of the whole chapter: `commerce_survey.md`.

## Validation

- Checks against printed totals and identities: 113; passed: 113; failed: 0.

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: not_applicable: 2.

  - sgt1922 p.410 1922 all / catch_value / francs = NA (not_applicable)
  - sgt1922 p.410 1922 all / catch_value / francs = NA (not_applicable)

## Image versus OCR

- Read cell by cell on the page images (3 printings): sgt1922 f434, sgt1923 f924, sgt1924 f1428.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
