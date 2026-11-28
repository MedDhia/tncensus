# Service des eaux : vente d'eau (recettes)

*Water service: receipts from the sale of water, per locality, for the edition year.*

Source: *Statistique générale de la Tunisie*, chapter *Communes*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939 (stored values). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR).

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 38, f62; sgt1923 (`bpt6k9105649x`): p. 42, f544; sgt1924 (`bpt6k9105649x`): p. 42, f1032; sgt1925 (`bpt6k9105650k`): p. 42, f66; sgt1926 (`bpt6k9105650k`): p. 50, f614; sgt1927 (`bpt6k91056510`): p. 50, f78; sgt1928 (`bpt6k91056510`): p. 50, f602; sgt1929 (`bpt6k9105652d`): p. 50, f78; sgt1930 (`bpt6k9105652d`): p. 52, f610; sgt1935 (`bpt6k9105653t`): p. 29, f49; sgt1936 (`bpt6k91056547`): p. 21, f32; sgt1939 (`bpt6k9105739w`): p. 22, f28.

Rebuild: `python3 data-raw/yearbook_other_chapters/extract_communes.py build` (transcriptions `../transcribed/communes_water_<edition>.txt`). Per-check output: `communes_validation_services.json`.

Rows: 338. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939.

Printed once per edition (SPEC_ADDENDUM rule 5), as the last column of the pipe-length table (`communes_water_pipes.md`); `year` = the year of the receipts. No year is printed twice.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number of the cell
- `gallica_view`: Gallica view (fNNNN) of the cell
- `year`: year of the sales (*Recettes en <année>*)
- `locality`: locality as printed
- `measure`: `water_sales_receipts`
- `measure_fr`: column heading as printed (*Vente d'eau : Recettes en <année>*)
- `value`: francs with centimes; printed » and *néant* = 0.00
- `text_fr`: text printed instead of an amount
- `flag`: empty or `not_applicable` (text instead of an amount: value NA, text in `text_fr`)

**Headings.** sgt1922–sgt1935 *Recettes en <année>*, sgt1936 and sgt1939 *Recette en <année>*. sgt1927 heads the column "Recettes en 1926", but of the 24 localities also in sgt1926 only 2 have the same amount as sgt1926's 1926 sales (Tozeur 0.00, Le Kef 0.00; Tunis 3.478.497,30 against 2.762.081,90), so the column is taken as the 1927 receipts (`year` = 1927, heading kept in `measure_fr`). Gabès prints 19.379,80 in both sgt1927 and sgt1928 (kept as printed).

**Texts.** sgt1936: El-Aroussa, Le Goubellat and Testour, *Les régies ne fonctionnent qu'à partir du 1er janvier 1937* (the services only operate from 1 January 1937; printed across the three lines); Gafour, *Régie à partir du 1-1-37*; sgt1939: Aïn-Kerma "(1)", footnote *Ne fonctionne pas encore* (not working yet). These are NA, `not_applicable`. *Néant* (sgt1935, sgt1936) is stored as 0.00. In sgt1936 the value lines sit half a line off their names; they were assigned in order (51 lines for 51 names).

**Image versus OCR.** Every amount read on native-resolution crops (see `communes_water_pipes.md`); OCR not relied on.

## Validation

- No totals are printed, so there is no sum check; each year is printed once, so there is no overlap comparison (the sgt1927 heading was checked against sgt1926 as above).
- Rows per edition: sgt1922 7, sgt1923 7, sgt1924 7, sgt1925 23, sgt1926 24, sgt1927 29, sgt1928 34, sgt1929 23, sgt1930 34, sgt1935 49, sgt1936 51, sgt1939 50.
- Flagged cells: 5.
  - sgt1936 El-Aroussa: not_applicable ("Les régies ne fonctionnent qu'à partir du 1er janvier 1937")
  - sgt1936 Le Goubellat: not_applicable ("Les régies ne fonctionnent qu'à partir du 1er janvier 1937")
  - sgt1936 Testour: not_applicable ("Les régies ne fonctionnent qu'à partir du 1er janvier 1937")
  - sgt1936 Gafour: not_applicable ("Régie à partir du 1-1-37")
  - sgt1939 Aïn-Kerma: not_applicable ("(1) Ne fonctionne pas encore")
