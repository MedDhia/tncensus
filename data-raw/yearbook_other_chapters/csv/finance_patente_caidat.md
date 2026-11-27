# Droit de patente. Etat des assujettis au droit de patente (nombre et montant du bénéfice moyen par caïdat)

*Business licence tax (droit de patente): number of taxpayers and total mean profit by caïdat.*

Source: *Statistique générale de la Tunisie*, chapter *Finances*, editions sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1935 (`bpt6k9105653t`): p. 118, f138; sgt1936 (`bpt6k91056547`): p. 88, f99; sgt1939 (`bpt6k9105739w`): p. 92, f98.

Transcriptions: `../transcribed/finance_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_finance.py build`.

Rows: 204. Years: 1935, 1936, 1939.

Units: `taxpayers` count, `mean_profit_total` francs; value_type: mixed (count and francs).

Printed once per edition, each printing for its own period (cumulative to a later year, or another tax year): every edition is kept (SPEC_ADDENDUM rule 5); `census` is the edition, `year` the year the printing refers to.

## Columns

- `census`: edition (source code; every edition printing the table is kept, rule 5)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: tax year ("imposés en <year>")
- `profits_year`: year of the profits taxed ("bénéfices de <year>"), when the title prints it; empty otherwise
- `region`: chef-lieu de région as printed, or "Territoires Militaires du Sud"
- `controle_civil`: contrôle civil as printed (sgt1925 on); empty when the table lists caïdats only
- `caidat`: caïdat as printed; "Souk-el-Khemis, Souk-el-Arba" = the two caïdats bracketed with one figure
- `measure`: `taxpayers` (nombre de patentables) or `mean_profit_total` (montant du bénéfice moyen par caïdat: the sum of the bénéfices moyens of the classes of the caïdat's taxpayers)
- `measure_fr`: printed column head
- `unit`: unit of `value`
- `value`: printed value (» = 0)
- `flag`: empty, or `ocr_corrected` (image reading differs from the Gallica OCR), `total_mismatch` (printed value kept; identified by a failed check as the faulty cell, see Validation), `illegible` (value NA), `not_applicable` (nothing printed, value NA), `derived_from_totals` (digits hidden in the binding; value = the printed row total minus the other cells of the row, see the notes)

Printed in sgt1935, sgt1936 and sgt1939 (bénéfices de 1934, 1935 and 1938, imposés en 1935, 1936 and 1939), one page each: the classes of profit are no longer printed, only the Nombre de patentables and the Montant du bénéfice moyen par caïdat, by chef-lieu de région, contrôle civil and caïdat. Earlier editions print the same two columns next to the classes (`finance_patente`); they are not stored there because they are sums of the stored class cells. The Totaux line is a check, not stored.

Survey of the whole chapter in every edition: `finance_survey.md`.

## Validation

- Checks against printed totals and identities: 6; passed: 6; failed: 0.

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: ocr_corrected: 23.

  - sgt1935 p.118 1935 1934 / Tunis / Zaghouan / Zaghouan / taxpayers / taxpayers = 301 (ocr_corrected)
  - sgt1935 p.118 1935 1934 / Tunis / Zaghouan / Zaghouan / mean_profit_total / francs = 726500 (ocr_corrected)
  - sgt1935 p.118 1935 1934 / Sousse / Sousse / Madhia / mean_profit_total / francs = 743000 (ocr_corrected)
  - sgt1935 p.118 1935 1934 / Sousse / Sousse / Monastir / mean_profit_total / francs = 742000 (ocr_corrected)
  - sgt1935 p.118 1935 1934 / Sousse / Kairouan / Kairouan / mean_profit_total / francs = 1057000 (ocr_corrected)
  - sgt1935 p.118 1935 1934 / Sousse / Thala / Fraichiches / mean_profit_total / francs = 473000 (ocr_corrected)
  - sgt1935 p.118 1935 1934 / Sfax / Gabès / L'Arad / taxpayers / taxpayers = 497 (ocr_corrected)
  - sgt1935 p.118 1935 1934 / Sfax / Gabès / L'Arad / mean_profit_total / francs = 1286500 (ocr_corrected)
  - sgt1936 p.88 1936 1935 / Tunis / Grombalia / Cap-Bon / taxpayers / taxpayers = 1632 (ocr_corrected)
  - sgt1936 p.88 1936 1935 / Sousse / Sousse / Sousse / mean_profit_total / francs = 8797000 (ocr_corrected)
  - sgt1939 p.92 1939 1938 / Bizerte / Béja / Béja / mean_profit_total / francs = 3718000 (ocr_corrected)
  - sgt1939 p.92 1939 1938 / Bizerte / Tabarka / Aïn-Draham / mean_profit_total / francs = 876500 (ocr_corrected)
  - sgt1939 p.92 1939 1938 / Tunis / Zaghouan / Zaghouan / taxpayers / taxpayers = 257 (ocr_corrected)
  - sgt1939 p.92 1939 1938 / Tunis / Zaghouan / Zaghouan / mean_profit_total / francs = 883500 (ocr_corrected)
  - sgt1939 p.92 1939 1938 / Tunis / Grombalia / Cap-Bon / taxpayers / taxpayers = 1661 (ocr_corrected)
  - sgt1939 p.92 1939 1938 / Le Kef / Téboursouk / Téboursouk / taxpayers / taxpayers = 246 (ocr_corrected)
  - sgt1939 p.92 1939 1938 / Le Kef / Téboursouk / Téboursouk / mean_profit_total / francs = 558500 (ocr_corrected)
  - sgt1939 p.92 1939 1938 / Le Kef / Medjez-el-Bab / Medjez-el-Bab / taxpayers / taxpayers = 229 (ocr_corrected)
  - sgt1939 p.92 1939 1938 / Le Kef / Medjez-el-Bab / Medjez-el-Bab / mean_profit_total / francs = 770000 (ocr_corrected)
  - sgt1939 p.92 1939 1938 / Sousse / Sousse / Mahdia / mean_profit_total / francs = 1736000 (ocr_corrected)
  - sgt1939 p.92 1939 1938 / Sfax / Sfax / La Skhira / mean_profit_total / francs = 14500 (ocr_corrected)
  - sgt1939 p.92 1939 1938 / Sfax / Tozeur / Djerid / mean_profit_total / francs = 608500 (ocr_corrected)
  - sgt1939 p.92 1939 1938 / Sfax / Djerba / Djerba / mean_profit_total / francs = 987500 (ocr_corrected)

## Image versus OCR

- Read cell by cell on the page images (3 printings): sgt1935 f138, sgt1936 f99, sgt1939 f98.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 23.
