# Mouvements des mandats-poste : b) Mandats-poste établis en Tunisie ou à destination de la Tunisie

*Money orders issued in Tunisia for France and Italy, and issued in France and Italy for Tunisia.*

Source: *Statistique générale de la Tunisie*, chapter *Postes - Télégraphes - Téléphones*, editions sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1925 (`bpt6k9105650k`): p. 144, f168; sgt1926 (`bpt6k9105650k`): p. 154, f718; sgt1927 (`bpt6k91056510`): p. 152, f180; sgt1928 (`bpt6k91056510`): p. 152, f704; sgt1929 (`bpt6k9105652d`): p. 154, f182; sgt1930 (`bpt6k9105652d`): p. 158, f716; sgt1935 (`bpt6k9105653t`): p. 94, f114.

Transcriptions: `../transcribed/posts_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_posts.py build`.

Rows: 152. Years: 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934.

Units: number of money orders (`count`) and amount in francs (`francs`); suggested value_type: mixed.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing of the same cell, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`): the latest edition printing that year
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (network: situation at 31 December)
- `flow`: `issued_in_tunisia` or `payable_in_tunisia`
- `flow_fr`: printed column group heading
- `partner`: `france` or `italy`
- `partner_fr`: printed column heading
- `measure`: `number` (Nombre) or `amount` (Montant)
- `measure_fr`: as printed
- `unit`: `count`, `km` (kilometres) or `francs` (centimes kept as decimals)
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible` (NA, cut by the binding or broken type), `not_applicable` (nothing printed, or » in a line not yet collected; NA), `row_realigned` (printed in the wrong column or line, stored on the year / item it belongs to), `reprint_corrected` (kept from an earlier printing), `derived_from_totals`

sgt1922-sgt1924 print table b) for two or three years with the lines En plus / Soit % / En moins / Soit % (used as checks; the percentages are truncated, not rounded). From sgt1925 the table is two tables a) Mandats envoyés (de Tunisie en France, en Italie) and b) Mandats-poste à destination de la Tunisie (émis en France, en Italie), ten years (sgt1935: 1923-1934), stored together here (`flow`).

sgt1930 prints its last line "1930-31 (15 mois)"; sgt1935 prints "1930-31 (15 mois)", "1931-32 (12 mois)" and then 1932, 1933, 1934: stored as years 1930 and 1931 (financial years) and 1932-1934.

Not printed in sgt1936 and sgt1939.

Failed checks, grouped (printed values kept). A failure that recurs identically in several editions was read independently on each printing, so it is the printed figure; every failure printed by one edition only was re-read on a zoomed native-resolution crop: mo_summary to_fr.amt Soit %: cells 24.8, printed 24.7 (in sgt1922); mo_summary to_it.n plus2a + plus2b: cells 392, printed 492 (in sgt1924).

Survey of the whole chapter in every edition: `posts_survey.md`.

## Validation

- Checks against printed totals and identities: 56; passed: 54; failed: 2.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.134 (f158) mo_summary to_fr.amt: Soit % = |difference| / 1921 (truncated to 0.1): cells give 24.8, printed 24.7 (difference -0.1)
  - sgt1924 p.142 (f1132) mo_summary to_it.n: plus2a + plus2b = 1924 - 1923: cells give 392, printed 492 (difference 100)

- Overlapping printings: 480 cell comparisons with other editions printing the same cell; 4 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1922 / issued_in_tunisia / france / amount | sgt1922 | 63446900 | sgt1930 | 63466900 |
| 1924 / issued_in_tunisia / italy / amount | sgt1924 | 767166.58 | sgt1935 | 767166 |
| 1924 / payable_in_tunisia / italy / amount | sgt1924 | 79935.28 | sgt1935 | 79935 |
| 1928 / payable_in_tunisia / france / amount | sgt1928 | 63992969 | sgt1935 | 63997969 |

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (10 printings): sgt1922 f158, sgt1923 f642, sgt1924 f1132, sgt1925 f168, sgt1926 f718, sgt1927 f180, sgt1928 f704, sgt1929 f182, sgt1930 f716, sgt1935 f114.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
