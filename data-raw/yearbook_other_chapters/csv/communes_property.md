# Biens communaux : valeurs immobilières et mobilières appartenant aux communes au 31 décembre

*Communal property: real estate and movable assets owned by each commune at 31 December.*

Source: *Statistique générale de la Tunisie*, chapter II *Communes*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 27, f51; sgt1923 (`bpt6k9105649x`): p. 27, f529; sgt1924 (`bpt6k9105649x`): p. 27, f1017; sgt1925 (`bpt6k9105650k`): p. 25, f49; sgt1926 (`bpt6k9105650k`): p. 33, f597; sgt1927 (`bpt6k91056510`): p. 33, f61; sgt1929 (`bpt6k9105652d`): p. 33, f61; sgt1930 (`bpt6k9105652d`): p. 33, f591; sgt1935 (`bpt6k9105653t`): p. 23, f43; sgt1936 (`bpt6k91056547`): p. 18, f29; sgt1939 (`bpt6k9105739w`): p. 19, f25.

Transcriptions: `../transcribed/communes_<edition>.txt`, section `@property`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_communes.py build`. Per-check output: `communes_validation.json`.

Rows: 1959. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1930, 1934, 1935, 1937.

Unit: francs (French/Tunisian franc), as printed, centimes kept.

Printed once per edition (rule 5), for 31 December of the year in the heading; the 1928 table printed twice is taken from the later edition.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section (`budget`, `property`, `gas`)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: budget year (exercice) / year of the 31 December valuation
- `commune`: commune name exactly as printed in the edition the value is taken from (footnote calls such as `Kram (Le) (1)` kept)
- `category`: `public_domain_real_estate`, `private_domain_real_estate`, `movable_assets`
- `category_fr`: column heading (French)
- `value`: francs, centimes kept (two decimals); printed » = 0.00. Gas: consumption in cubic metres (integer), receipts in francs with centimes
- `flag`: empty, `reprint_corrected`, `row_realigned`, `illegible` or `not_applicable` (see below)

"Biens communaux — Valeurs immobilières et mobilières appartenant aux Communes au 31 décembre …": per commune, real estate of the public domain (*Immeubles du domaine public*), real estate of the private domain (*Immeubles du domaine privé*), movable assets (*Valeurs mobilières*) and their sum (*Total général*, not stored; used for the row check). No column totals are printed.

Valuation dates: sgt1922 → 31.12.1922 … sgt1928 → 31.12.1928; **sgt1929 reprints the 1928 table** (heading "au 31 décembre 1928", every cell equal to sgt1928): 1928 is stored from sgt1929 and the sgt1928 printing compared (rule 4); sgt1930 → 1930; sgt1935 → 1934; sgt1936 → 1935; sgt1939 → 1937. The years 1929, 1931–1933 and 1936 are not printed.

The commune list follows the page (sgt1929, sgt1930 and sgt1935 have no Sbeïtla row; Kram and Pêcherie are listed until sgt1930). Values are often printed half a line below their label; rows were assigned by counting lines, and the row totals confirm the assignment. Printed » is stored as 0.00.

Row-check failures (below) were re-read on native-resolution crops and agree with the Gallica OCR; the print is inconsistent and no cell can be singled out, so none is flagged. Some repeat across editions (Medjez-el-Bab 38.000 + 22.000 = 60.000 printed 70.000, sgt1925–sgt1930; Maxula-Radès 99.743,97 + 10.810,40 printed 104.554,37 in sgt1924–sgt1926, corrected to 110.554,37 from sgt1927; Zarzis 142.043,59 + 9.243,65 printed 151.337,24, sgt1927–sgt1930). sgt1923: the 0,20 of Tunis's movable assets (188.475,20) is printed on Tozeur's total (102.650,20) instead of Tunis's (11.215.475 »).

## Validation

- Checks against printed totals: 713; passed: 683; failed: 30.

Failed checks (printed values kept):

  - sgt1922 p.27 Monastir: public + private + movable vs total: cells give 88500.00, printed 78500.00 (difference -10000.00)
  - sgt1923 p.27 Tozeur: public + private + movable vs total: cells give 102650.00, printed 102650.20 (difference 0.20)
  - sgt1923 p.27 Tunis: public + private + movable vs total: cells give 11215475.20, printed 11215475.00 (difference -0.20)
  - sgt1924 p.27 Gabès: public + private + movable vs total: cells give 105009.00, printed 104009.00 (difference -1000.00)
  - sgt1924 p.27 Maxula-Radès: public + private + movable vs total: cells give 110554.37, printed 104554.37 (difference -6000.00)
  - sgt1924 p.27 Sfax: public + private + movable vs total: cells give 1111767.00, printed 1111767.10 (difference 0.10)
  - sgt1924 p.27 Tozeur: public + private + movable vs total: cells give 12650.00, printed 12050.00 (difference -600.00)
  - sgt1925 p.25 Maxula-Radès: public + private + movable vs total: cells give 110554.37, printed 104554.37 (difference -6000.00)
  - sgt1925 p.25 Medjez-el-Bab: public + private + movable vs total: cells give 60000.00, printed 70000.00 (difference 10000.00)
  - sgt1925 p.25 Monastir: public + private + movable vs total: cells give 42000.00, printed 92000.00 (difference 50000.00)
  - sgt1925 p.25 Nabeul: public + private + movable vs total: cells give 706000.00, printed 106000.00 (difference -600000.00)
  - sgt1925 p.25 Tebourba: public + private + movable vs total: cells give 32483.16, printed 32483.15 (difference -0.01)
  - sgt1925 p.25 Zaghouan: public + private + movable vs total: cells give 6625.00, printed 9625.00 (difference 3000.00)
  - sgt1926 p.33 Maxula-Radès: public + private + movable vs total: cells give 110554.37, printed 104554.37 (difference -6000.00)
  - sgt1926 p.33 Medjez-el-Bab: public + private + movable vs total: cells give 60000.00, printed 70000.00 (difference 10000.00)
  - sgt1927 p.33 Medjez-el-Bab: public + private + movable vs total: cells give 60000.00, printed 70000.00 (difference 10000.00)
  - sgt1927 p.33 Zarzis: public + private + movable vs total: cells give 151287.24, printed 151337.24 (difference 50.00)
  - sgt1928 p.33 Bardo (Le): public + private + movable vs total: cells give 36000.00, printed 35000.00 (difference -1000.00)
  - sgt1928 p.33 Medjez-el-Bab: public + private + movable vs total: cells give 60000.00, printed 70000.00 (difference 10000.00)
  - sgt1928 p.33 Zarzis: public + private + movable vs total: cells give 151287.24, printed 151337.24 (difference 50.00)
  - sgt1929 p.33 Bardo (Le): public + private + movable vs total: cells give 36000.00, printed 35000.00 (difference -1000.00)
  - sgt1929 p.33 Medjez-el-Bab: public + private + movable vs total: cells give 60000.00, printed 70000.00 (difference 10000.00)
  - sgt1929 p.33 Zarzis: public + private + movable vs total: cells give 151287.24, printed 151337.24 (difference 50.00)
  - sgt1930 p.33 Medjez-el-Bab: public + private + movable vs total: cells give 60000.00, printed 70000.00 (difference 10000.00)
  - sgt1930 p.33 M'saken: public + private + movable vs total: cells give 59248.40, printed 58048.40 (difference -1200.00)
  - sgt1930 p.33 Sfax: public + private + movable vs total: cells give 1101629.95, printed 1116781.95 (difference 15152.00)
  - sgt1930 p.33 Zarzis: public + private + movable vs total: cells give 151287.24, printed 151337.24 (difference 50.00)
  - sgt1935 p.23 Souk-el-Arba: public + private + movable vs total: cells give 1594000.00, printed 1594811.00 (difference 811.00)
  - sgt1935 p.23 Tozeur: public + private + movable vs total: cells give 86000.00, printed 80000.00 (difference -6000.00)
  - sgt1935 p.23 Zarzis: public + private + movable vs total: cells give 92803.14, printed 93006.14 (difference 203.00)

- Overlapping printings: 240 cell comparisons between editions; 0 differences.

- Flagged cells: none.
