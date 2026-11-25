# Institut Arloing : doses de sérums et de vaccins distribuées

*Institut Arloing (veterinary): doses of serums and vaccines distributed, by product and month (sgt1922–sgt1930).*

Source: *Statistique générale de la Tunisie*, chapter III (health and assistance), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / BnF.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 57, f81; sgt1923 (`bpt6k9105649x`): p. 63, f565; sgt1924 (`bpt6k9105649x`): p. 66, f1056; sgt1925 (`bpt6k9105650k`): p. 66, f90; sgt1926 (`bpt6k9105650k`): p. 75, f639; sgt1927 (`bpt6k91056510`): p. 73, f101; sgt1928 (`bpt6k91056510`): p. 73, f625; sgt1929 (`bpt6k9105652d`): p. 75, f103; sgt1930 (`bpt6k9105652d`): p. 79, f637.

Transcriptions: `../transcribed/health_finance_<edition>.txt`, sections `[arloing_doses]`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_finance.py build`. Per-check output: `health_finance_validation.json`.

Rows: 1152. Years: 1922–1930. Unit of `value`: doses (or cc. / grammes where unit_fr says so); amounts are as printed, centimes kept as decimals (printed » = 0).

Printed once per edition; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (for a table over two pages, the page of the column group)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (budget year, account year or calendar year; see below)
- `kind`: `serum` (c) Doses de sérums distribuées) or `vaccine` (d) Doses de vaccins distribuées)
- `product_fr`: product as printed
- `product_en`: English code
- `unit_fr`: unit printed against the product (empty where none is printed)
- `month`: `january` … `december`
- `month_fr`: as printed
- `value`: doses (or cc. / grammes where unit_fr says so); empty where the flag says so
- `flag`: empty, or `derived_from_totals`, `total_mismatch`, `not_applicable`, `illegible`, `reprint_corrected` (see below)

c) "Doses de sérums distribuées" (`kind` = `serum`) and d) "Doses de vaccins distribuées" (`kind` = `vaccine`) of the Institut Arloing (veterinary products: sheep-pox, anthrax, blackleg, fowl diseases, piroplasmosis …), by month. Products change between editions; `product_fr` as printed. `unit_fr` from the units printed in the totals line (cc., d. = doses, gr.); empty where none is printed. TOTAUX not stored.

Failed checks (cells re-read on the images for sgt1922 and sgt1926; printed as transcribed): sgt1922 antistreptococcal serum 66 vs 60 cc. and blackleg vaccine 5.575 vs 5.845; sgt1923 anticlaveleux serum, printed in two sub-columns (e.g. "100 40") and stored as decimals (100.40), sums to 424,07 against 405,26; sgt1926 sheep-pox vaccine 199.973 vs 200.973 and anthrax vaccine 14.705 vs 13.705; sgt1930 anthrax vaccine 11.370 vs 11.376.

## Remarks recorded in the transcriptions

- sgt1922: totals printed "620 cc." and "60 cc."
- sgt1923: Anticlaveleux is printed in two sub-columns (e.g. "100 40"); stored as 100.40 (unit not printed).
- sgt1925: "Typanblaï" printed for trypan blue ("Trypanbleu"); "typhon aviaire" as printed (fowl typhoid).
- sgt1928: Trypanblau: "5 1/2" and "100 1/2" stored as 5.5 and 100.5.
- sgt1929: Trypanblau printed "0 5" and "16 5" (decimal), stored 0.5 and 16.5.
- sgt1930: Trypanblau printed in two sub-columns ("29 10", "35 20"); stored as decimals of a gram.

## Validation

- Checks against printed totals: 96; passed: 90; failed: 6.

Failed checks (printed values kept, unless a flag below says otherwise; `L<n>` = line of the transcription file). See the commentary above for which ones were re-read on the page images and which are repeated identically in several printings:

  - sgt1922 arloing_doses serum Antistreptococcique: months vs TOTAUX: cells give 66, printed 60
  - sgt1922 arloing_doses vaccine Contre le charbon symptomatique: months vs TOTAUX: cells give 5575, printed 5845
  - sgt1923 arloing_doses serum Anticlaveleux: months vs TOTAUX: cells give 424.07, printed 405.26
  - sgt1926 arloing_doses vaccine Vaccin anticlaveleux: months vs TOTAUX: cells give 199973, printed 200973
  - sgt1926 arloing_doses vaccine Vaccin contre la fièvre charbonneuse: months vs TOTAUX: cells give 14705, printed 13705
  - sgt1930 arloing_doses vaccine Vaccin anticharbonneux: months vs TOTAUX: cells give 11370, printed 11376

- Flagged cells: none.
