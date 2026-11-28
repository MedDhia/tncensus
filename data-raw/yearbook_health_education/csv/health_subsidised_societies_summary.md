# Situation des sociétés et œuvres subventionnées (récapitulation, sgt1935)

*Subsidised societies and charities: total receipts, expenditure, balance and people assisted (sgt1935 layout).*

Source: *Statistique générale de la Tunisie*, chapter III (health and assistance), editions sgt1935. Source gallica.bnf.fr / BnF.

Pages and views of the stored values: sgt1935 (`bpt6k9105653t`): p. 40, f60, p. 41, f61.

Transcriptions: `../transcribed/health_finance_<edition>.txt`, sections `[societies_summary]`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_finance.py build`. Per-check output: `health_finance_validation.json`.

Rows: 293. Years: 1935–1935. Unit of `value`: francs (statistics: counts); amounts are as printed, centimes kept as decimals (printed » = 0).

Printed once per edition; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (for a table over two pages, the page of the column group)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (budget year, account year or calendar year; see below)
- `society_fr`: society / charity name exactly as printed
- `society_en`: English code built from the name
- `group`: column group: `receipts`, `expenditure`, `balance`, `statistics` (`accounts` in the sgt1935 summary)
- `measure`: what the value is (see below)
- `measure_fr`: column heading (French)
- `value`: francs (statistics: counts); empty where the flag says so
- `flag`: empty, or `derived_from_totals`, `total_mismatch`, `not_applicable`, `illegible`, `reprint_corrected` (see below)

sgt1935 layout of the societies table: total receipts, total expenditure, "reste en caisse au 1er janvier 1935" and the four statistics, by society (no TOTAUX line). The year printed in the heading is 1935 for the balance; the accounts are stored with `year` = 1935. Where the balance is printed "déficit" it is stored empty with `not_applicable`. The "Nombre de secours" of the Caisse israélite de Bizerte is printed "7.210 95" (a money amount, apparently misplaced) and stored as 7210.95. Failed checks: three balances that are not receipts − expenditure (Nabeul 3.815,16 vs 3.815,46; Bizerte musulmane 9.347,66 vs 8.347,66; Œuvre de la Crèche 46.286,30 vs 46.291,30). Not printed in sgt1936 and sgt1939. The Société française de Kairouan, printed » in every column, is not stored.

## Remarks recorded in the transcriptions

- sgt1935: Layout from this edition: total receipts | total expenditure | reste en caisse au 1er janvier 1935 (printed "déficit" where expenditure exceeds receipts: stored as the word) | statistics (personnes secourues, secours en espèces ou en nature, personnes ayant bénéficié de l'assistance, rapatriements). "—" = dash printed. No total line. Caisse israélite de Bizerte: "Nombre de secours" printed "7.210 95" (a money amount, apparently misplaced), stored 7210.95.

## Validation

- Checks against printed totals: 33; passed: 30; failed: 3.

Failed checks (printed values kept, unless a flag below says otherwise; `L<n>` = line of the transcription file). See the commentary above for which ones were re-read on the page images and which are repeated identically in several printings:

  - sgt1935 L95 Société Musulmane de Bienfaisance de Nabeul: receipts - expenditure vs balance: cells give 3815.46, printed 3815.16
  - sgt1935 L98 Société Musulmane de Bienfaisance de Bizerte: receipts - expenditure vs balance: cells give 8347.66, printed 9347.66
  - sgt1935 L120 Œuvre de la Crèche de Tunis: receipts - expenditure vs balance: cells give 46291.3, printed 46286.3

- Flagged cells: not_applicable: 9.

  - sgt1935 1935 Sœurs Mission. N.D. d'Afrique, Carthage / accounts / cash_remaining_1_january_next / Reste en caisse au 1er janvier 1935 = None (not_applicable)
  - sgt1935 1935 Sœurs de N.D. Espérance, Tunis / accounts / cash_remaining_1_january_next / Reste en caisse au 1er janvier 1935 = None (not_applicable)
  - sgt1935 1935 Asile de nuit et Maternité israélites, Tunis / accounts / cash_remaining_1_january_next / Reste en caisse au 1er janvier 1935 = None (not_applicable)
  - sgt1935 1935 Société Italienne de Bienfaisance de Sfax / accounts / cash_remaining_1_january_next / Reste en caisse au 1er janvier 1935 = None (not_applicable)
  - sgt1935 1935 Communauté israélite de Tunis / accounts / cash_remaining_1_january_next / Reste en caisse au 1er janvier 1935 = None (not_applicable)
  - sgt1935 1935 Garderie Israélite, Tunis / accounts / cash_remaining_1_january_next / Reste en caisse au 1er janvier 1935 = None (not_applicable)
  - sgt1935 1935 Comité Central de protection et d'assistance de l'enfance / accounts / cash_remaining_1_january_next / Reste en caisse au 1er janvier 1935 = None (not_applicable)
  - sgt1935 1935 Dispensaire du Fourneau des Pauvres, Tunis / accounts / cash_remaining_1_january_next / Reste en caisse au 1er janvier 1935 = None (not_applicable)
  - sgt1935 1935 Œuvre israélite des couvertures, Tunis / accounts / cash_remaining_1_january_next / Reste en caisse au 1er janvier 1935 = None (not_applicable)
