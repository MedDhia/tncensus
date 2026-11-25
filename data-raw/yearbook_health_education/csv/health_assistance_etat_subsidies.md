# État des recettes et des dépenses du budget de l'Assistance publique : II. Dépenses (subventions)

*Public assistance budget statement: subsidies granted by society (sgt1935–sgt1939).*

Source: *Statistique générale de la Tunisie*, chapter III (health and assistance), editions sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / BnF.

Pages and views of the stored values: sgt1935 (`bpt6k9105653t`): p. 38, f58, p. 39, f59; sgt1936 (`bpt6k91056547`): p. 30, f41, p. 31, f42; sgt1939 (`bpt6k9105739w`): p. 30, f36, p. 31, f37, p. 32, f38.

Transcriptions: `../transcribed/health_finance_<edition>.txt`, sections `[etat_subsidies]`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_finance.py build`. Per-check output: `health_finance_validation.json`.

Rows: 450. Years: 1935–1939 (3 years: 1935, 1936, 1939). Unit of `value`: francs; amounts are as printed, centimes kept as decimals (printed » = 0).

Printed once per edition; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (for a table over two pages, the page of the column group)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (budget year, account year or calendar year; see below)
- `section_fr`: the last one or two headings printed above the line
- `article`: article number as printed (`-` = printed without a number; letters/prefixes added where the edition numbers sub-items or restarts numbering by section, see the transcription file)
- `line_type`: `article` (a budget line with its own amount) or `detail` (an amount printed in the label column breaking down the article above it; do not add details to articles)
- `line_fr`: budget line / article label as printed (ditto marks expanded)
- `line_en`: English code built from the French label (key words translated, place names kept)
- `measure`: what the value is (see below)
- `column_fr`: column heading as printed (French)
- `value`: francs; empty where the flag says so
- `flag`: empty, or `derived_from_totals`, `total_mismatch`, `not_applicable`, `illegible`, `reprint_corrected` (see below)

II. Dépenses of the same statement: subsidies by society and service (Titre I, Titre II; the Total column is not stored). Sub-items printed under a society heading (a), b) …) are stored with the heading prefixed to the label ("Société française de bienfaisance de Tunis : Orphelinat"). sgt1939 groups the lines by region and by kind of subsidy (ordinary, exceptional, conditional, complementary; then V. Fonds de réserve) (`section_fr`), and prints "Totaux" before the reserve-fund line and a "Total général".

Failed checks: sgt1935 TOTAL, 0,90 franc short: the Legs Joséphine Virieu and the Dépenses imprévues are printed 637,05 and 10.862,05 (637,50 and 10.862,50 close the total; both flagged `total_mismatch`); sgt1936 the lines sum to 2.058.100 against 2.050.000 printed for Titre I (8.100 more; every line re-read on the image, not resolved).

## Remarks recorded in the transcriptions

- sgt1936: The first six lines are printed under the column heads with no group heading.

## Validation

- Checks against printed totals: 241; passed: 237; failed: 4.

Failed checks (printed values kept, unless a flag below says otherwise; `L<n>` = line of the transcription file). See the commentary above for which ones were re-read on the page images and which are repeated identically in several printings:

  - sgt1935 etat_subsidies TOTAL (line 79) col 0: cells give 1849999.1, printed 1850000
  - sgt1935 etat_subsidies TOTAL (line 79) col 2: cells give 2119999.1, printed 2120000
  - sgt1936 etat_subsidies TOTAL (line 88) col 0: cells give 2058100, printed 2050000
  - sgt1936 etat_subsidies TOTAL (line 88) col 2: cells give 2145077, printed 2136977

- Flagged cells: total_mismatch: 2.

  - sgt1935 1935 Société française de bienfaisance de Tunis / - / article / Legs Joséphine Virieu / credit_title_I / Subvention proposée pour 1935, Titre I = 637.05 (total_mismatch)
  - sgt1935 1935 Société française de bienfaisance de Tunis / - / article / Dépenses imprévues / credit_title_I / Subvention proposée pour 1935, Titre I = 10862.05 (total_mismatch)
