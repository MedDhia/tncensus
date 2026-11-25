# Institut Pasteur : travaux de l'Institut (vaccins et sérums distribués)

*Institut Pasteur: vaccines, serums and other products distributed, by product (sgt1922–sgt1930).*

Source: *Statistique générale de la Tunisie*, chapter III (health and assistance), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / BnF.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 55, f79; sgt1923 (`bpt6k9105649x`): p. 61, f563; sgt1924 (`bpt6k9105649x`): p. 64, f1054; sgt1925 (`bpt6k9105650k`): p. 64, f88; sgt1926 (`bpt6k9105650k`): p. 73, f637; sgt1927 (`bpt6k91056510`): p. 71, f99; sgt1928 (`bpt6k91056510`): p. 71, f623; sgt1929 (`bpt6k9105652d`): p. 73, f101; sgt1930 (`bpt6k9105652d`): p. 77, f635.

Transcriptions: `../transcribed/health_finance_<edition>.txt`, sections `[pasteur_products]`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_finance.py build`. Per-check output: `health_finance_validation.json`.

Rows: 237. Years: 1922–1930. Unit of `value`: doses or containers, as printed in unit_fr; amounts are as printed, centimes kept as decimals (printed » = 0).

Printed once per edition; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (for a table over two pages, the page of the column group)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (budget year, account year or calendar year; see below)
- `service_fr`: service heading of the Institut Pasteur report as printed
- `product_fr`: product as printed
- `product_en`: English code
- `unit_fr`: unit printed against the product (empty where none is printed)
- `value`: doses or containers, as printed in unit_fr; empty where the flag says so
- `flag`: empty, or `derived_from_totals`, `total_mismatch`, `not_applicable`, `illegible`, `reprint_corrected` (see below)

b) "Travaux de l'Institut" of the Institut Pasteur: only the lines counting vaccines, serums and other products distributed are stored (the laboratory analyses, rabies treatments and fermentation lines of the same table are not). `service_fr` = the service heading (Centre vaccinogène; Service des vaccins microbiens, nombre de doses distribuées; Service des sérums de convalescents; Sérums thérapeutiques préparés à l'Institut; Produits divers non préparés à l'Institut). `unit_fr` = the unit printed against the line (doses, flacons, flacons de 10 c.c., ampoules, échantillons); a unit printed once applies to the lines below it, which are stored with `unit_fr` empty. No totals are printed, so there is no arithmetic check; the values were compared with the Gallica OCR (every difference was an OCR gap).

## Remarks recorded in the transcriptions

- sgt1922: item | unit as printed ("-" none printed) | value ; only the vaccine and serum lines of "b) Travaux de l'Institut"
- sgt1925: antivariolique printed "1.207-994"
- sgt1927: Group prefixes: X: = Centre vaccinogène; V: = Service des vaccins microbiens, nombre de doses distribuées; C: = Service des sérums de convalescents; S: = Sérums thérapeutiques préparés à l'Institut; P: = Produits divers non préparés à l'Institut
- sgt1928: In this edition the two convalescent-serum lines are printed inside the "vaccins microbiens" list (no separate heading).
- sgt1930: "Vaccin antidiphtérique ( ampoules)": the number of ampoules is left blank in the print.

## Validation

- Checks against printed totals: 0; passed: 0; failed: 0.

- Flagged cells: none.
