# Postes, Télégraphes, Téléphones. Renseignements généraux : a) Réseau

*Posts, telegraphs and telephones: network at 31 December.*

Source: *Statistique générale de la Tunisie*, chapter *Postes - Télégraphes - Téléphones*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 130, f154; sgt1923 (`bpt6k9105649x`): p. 136, f638; sgt1924 (`bpt6k9105649x`): p. 138, f1128; sgt1925 (`bpt6k9105650k`): p. 140, f164; sgt1926 (`bpt6k9105650k`): p. 150, f714; sgt1927 (`bpt6k91056510`): p. 148, f176; sgt1928 (`bpt6k91056510`): p. 148, f700; sgt1929 (`bpt6k9105652d`): p. 150, f178; sgt1930 (`bpt6k9105652d`): p. 154, f712, p. 155, f713; sgt1935 (`bpt6k9105653t`): p. 90, f110; sgt1936 (`bpt6k91056547`): p. 68, f79, p. 69, f80.

Transcriptions: `../transcribed/posts_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_posts.py build`.

Rows: 312. Years: 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936.

Units: kilometres (`unit` = `km`) and counts (`count`), per line; suggested value_type: mixed.

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing of the same cell, read independently on its own page image, is compared below.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`): the latest edition printing that year
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (network: situation at 31 December)
- `service`: `posts`, `telegraphs`, `telephones`, `savings` (Caisse d'Épargne)
- `service_fr`: printed sub-heading
- `item`: item code (English)
- `item_fr`: printed line heading
- `unit`: `count`, `km` (kilometres) or `francs` (centimes kept as decimals)
- `value`: printed value (» = 0)
- `flag`: empty, or `illegible` (NA, cut by the binding or broken type), `not_applicable` (nothing printed, or » in a line not yet collected; NA), `row_realigned` (printed in the wrong column or line, stored on the year / item it belongs to), `reprint_corrected` (kept from an earlier printing), `derived_from_totals`

Printed for ten years in every edition from sgt1922 to sgt1936 (sgt1922 1913-1922 ... sgt1936 1927-1936); not printed in sgt1939. No printed totals, so no checks; every year is compared across up to nine printings.

Footnote (A) under the table (every edition): "Les différences en moins dans la longueur des fils télégraphiques s'expliquent par les suppressions de lignes et désaffectation de bureaux" (the decreases in the length of telegraph wire are explained by lines removed and offices closed).

sgt1922 prints the 1915 column in the gutter of f154; its network values are legible.

Survey of the whole chapter in every edition: `posts_survey.md`.

## Validation

- Checks against printed totals and identities: 0; passed: 0; failed: 0.

- Overlapping printings: 1118 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (22 printings): sgt1922 f154, sgt1922 f155, sgt1923 f638, sgt1923 f639, sgt1924 f1128, sgt1924 f1129, sgt1925 f164, sgt1925 f165, sgt1926 f714, sgt1926 f715, sgt1927 f176, sgt1927 f177, sgt1928 f700, sgt1928 f701, sgt1929 f178, sgt1929 f179, sgt1930 f712, sgt1930 f713, sgt1935 f110, sgt1935 f111, sgt1936 f79, sgt1936 f80.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
