# Constructions immobilières en 1939 (Villes de plus de 5.000 habitants)

*Building in 1939, towns of more than 5,000 inhabitants: number of building permits and value of the buildings (housing, commercial and industrial, other).*

Source: *Statistique générale de la Tunisie*, chapter *Communes*, editions sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR).

Pages and views of the stored values: sgt1939 (`bpt6k9105739w`): p. 21, f27.

Rebuild: `python3 data-raw/yearbook_other_chapters/extract_communes.py build` (transcriptions `../transcribed/communes_constructions_sgt1939.txt`).

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
- `value`: permits: integer count (*néant* = 0); values: francs (no centimes printed, stored with .00 only where printed so: here integers)
- `flag`: empty, `not_applicable` (text printed instead of a number: value NA; the text is listed below), `illegible` (value NA; for money with hidden centimes the franc part is listed below)

sgt1939 page 21 (view 27) only; it replaces the *Autorisations de bâtir* table of the earlier editions. 30 towns, in the printed order (not alphabetical). No total is printed, so there is no check. All cells read on a native-resolution crop of the page (OCR as draft). Gabès housing is printed "860.000" (OCR "8(50.000").

## Validation

Rows: 120.
Flagged cells: none.
