# Concessions sur la voie publique : a) Autorisations de bâtir

*Building permits issued by each commune: constructions or reconstructions, raisings (surélévations) and number of permits.*

Source: *Statistique générale de la Tunisie*, chapter *Communes*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936. Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR).

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 36, f60; sgt1923 (`bpt6k9105649x`): p. 40, f542; sgt1924 (`bpt6k9105649x`): p. 40, f1030; sgt1925 (`bpt6k9105650k`): p. 40, f64; sgt1926 (`bpt6k9105650k`): p. 48, f612; sgt1927 (`bpt6k91056510`): p. 48, f76; sgt1928 (`bpt6k91056510`): p. 48, f600; sgt1929 (`bpt6k9105652d`): p. 48, f76; sgt1930 (`bpt6k9105652d`): p. 50, f608; sgt1935 (`bpt6k9105653t`): p. 26, f46; sgt1936 (`bpt6k91056547`): p. 20, f31.

Rebuild: `python3 data-raw/yearbook_other_chapters/extract_communes.py build` (transcriptions `../transcribed/communes_permits_<edition>.txt`).

Printed once per edition (SPEC_ADDENDUM rule 5): `year` is the year the edition reports on; no year is printed twice, so there is no overlap to compare.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the edition's figures (exercice / calendar year)
- `commune`: commune as printed (for loans: the name in the block heading, e.g. `Tunis` from *Commune de Tunis*; `le Kef` from *Commune du Kef*)
- `measure`: English code of the printed column
- `measure_fr`: column heading as printed (French)
- `value`: count (integer); printed » and printed *néant* are stored as 0
- `flag`: empty, `not_applicable` (text printed instead of a number: value NA; the text is listed below), `illegible` (value NA; for money with hidden centimes the franc part is listed below)

Table a) of the *Concessions sur la voie publique* pages (sgt1922–sgt1935), "Autorisations de bâtir délivrées en 1936" in sgt1936. Columns: *Constructions ou reconstructions*, *Surélévation*, *Nombre d'autorisations* (sgt1936: footnote (1) on the last column, *Toutes opérations comprises*). The number of permits is often not the sum of the first two columns (e.g. Gabès 1924: 8 + 2, 65 permits); this is how the table is printed, so no row identity is checked. sgt1939 prints a different table (`communes_building_values_1939.csv`). sgt1935 page 26 of view 46.

**Image versus OCR.** Every cell of every edition was read on native-resolution crops of the page image (half-page strips of the label column and the three value columns); Gallica's OCR was only used as a draft and to locate lines. In sgt1928, sgt1929 and sgt1930 the values are printed half a line to a full line below their labels and the OCR assigns them to the wrong commune; the rows were assigned by counting the 58 value lines against the 58 labels. Uncertain readings: sgt1928 Hammam-Lif permits 83 (last digit damaged, or 88); sgt1929 Tunis permits printed with a broken middle digit (7?7) → NA, `illegible`. sgt1935: the permits column is curved into the binding on view 46; Ariana 34, Grombalia 22, Kalaa-Kebira 112 and Maxula-Radès 62 were read on the gutter strip visible at the left edge of view 47 (view 46 alone suggests 31/23/113/63).

Not applicable cells: sgt1924 El-Djem ("Il n'existe pas de droits de voirie à El-Djem" printed across the row); sgt1930 Foum-Tatahouine raising printed "3 m. 50" (a length, not a count).

Printed totals: sgt1922–sgt1925 all three columns; sgt1926 and sgt1927 the permits column only; none from sgt1928. Failed checks were re-read on the images (the printed cells are as transcribed); no single cell explains them, so no cell is flagged.

Footnotes (calls kept in the commune names): sgt1922 (1) El-Djem, (2) Hadjeb-el-Aïoun, (3) Ksour-Essaf: *Commune créée le 29 mars 1922 / 9 mai 1922 / 29 mars 1922*. sgt1926–sgt1930 calls on Béja, El-Djem, Kairouan, Kef, Monastir, Tabarka, Tunis, Ferryville, Menzel-bou-Zelfa, Soliman, Zarzis refer to notes on the stalls/terraces of the facing page (see `communes_terraces.md`).

## Validation

Rows: 1932.
Checks (permits): 14; failed: 4.
  - sgt1923 p.40 communes n_auth: cells give 1115, printed total 1120 (difference 5)
  - sgt1924 p.40 communes constructions: cells give 1141, printed total 1129 (difference -12)
  - sgt1926 p.48 communes n_auth: cells give 1482, printed total 1433 (difference -49)
  - sgt1927 p.48 communes n_auth: cells give 1267, printed total 1258 (difference -9)
Flagged cells: illegible: 1, not_applicable: 4.
  - sgt1929 Tunis permits_issued: illegible
  - sgt1924 El-Djem constructions: not_applicable — printed text: El-Djem: "Il n'existe pas de droits de voirie à El-Djem" printed across the row
  - sgt1924 El-Djem raising: not_applicable — printed text: El-Djem: "Il n'existe pas de droits de voirie à El-Djem" printed across the row
  - sgt1924 El-Djem permits_issued: not_applicable — printed text: El-Djem: "Il n'existe pas de droits de voirie à El-Djem" printed across the row
  - sgt1930 Foum-Tatahouine raising: not_applicable
