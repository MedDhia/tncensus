# État des recettes et des dépenses du budget de l'Assistance publique : I. Recettes

*Public assistance budget statement: receipts, credits allotted (sgt1935–sgt1939).*

Source: *Statistique générale de la Tunisie*, chapter III (health and assistance), editions sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / BnF.

Pages and views of the stored values: sgt1935 (`bpt6k9105653t`): p. 38, f58; sgt1936 (`bpt6k91056547`): p. 30, f41; sgt1939 (`bpt6k9105739w`): p. 30, f36.

Transcriptions: `../transcribed/health_finance_<edition>.txt`, sections `[etat_receipts]`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_finance.py build`. Per-check output: `health_finance_validation.json`.

Rows: 6. Years: 1935–1939 (3 years: 1935, 1936, 1939). Unit of `value`: francs; amounts are as printed, centimes kept as decimals (printed » = 0).

Printed once per edition; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (for a table over two pages, the page of the column group)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (budget year, account year or calendar year; see below)
- `line_fr`: budget line / article label as printed (ditto marks expanded)
- `line_en`: English code built from the French label (key words translated, place names kept)
- `value`: francs; empty where the flag says so
- `flag`: empty, or `derived_from_totals`, `total_mismatch`, `not_applicable`, `illegible`, `reprint_corrected` (see below)

"État des recettes et des dépenses du budget de l'Assistance publique", I. Recettes: credits allotted, Titre I and Titre II (sgt1935, sgt1936, sgt1939; sgt1939: Titre I = special credit on the State budget, Titre II = cash available in the reserve fund). The total line is not stored; all totals check.

## Validation

- Checks against printed totals: 3; passed: 3; failed: 0.

- Flagged cells: none.
