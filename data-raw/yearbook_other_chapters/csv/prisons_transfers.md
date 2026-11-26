# Prison de Tunis : transfèrements (sgt1922-sgt1925); Service des transfèrements (sgt1926-sgt1935)

*Transfers of prisoners by destination.*

Source: *Statistique générale de la Tunisie*, chapter *Établissements pénitentiaires*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 76, f100; sgt1923 (`bpt6k9105649x`): p. 82, f584; sgt1924 (`bpt6k9105649x`): p. 84, f1074; sgt1925 (`bpt6k9105650k`): p. 86, f110; sgt1926 (`bpt6k9105650k`): p. 98, f662; sgt1927 (`bpt6k91056510`): p. 96, f124; sgt1928 (`bpt6k91056510`): p. 96, f648; sgt1929 (`bpt6k9105652d`): p. 98, f126; sgt1930 (`bpt6k9105652d`): p. 102, f660; sgt1935 (`bpt6k9105653t`): p. 68, f88.

Transcriptions: `../transcribed/prisons_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_prisons.py build`.

Rows: 168. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935.

Units: transfer operations; prisoners.

Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, with `year`; no year is printed by two editions.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section name (`transfers`); printed as table c) (sgt1922-sgt1924) or g) (sgt1925-sgt1935)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (the edition year: each edition prints the table for its own year)
- `destination`: code of the receiving establishment (*établissement destinataire*): `departmental_prisons`, `tunisian_prisons`, `algerian_prisons`, `central_prisons`, `central_prison_algeria`, `central_prisons_algeria`, `central_correction_algeria`, `algiers_remand_prison`, `marseille`, `el_harrach`, `algerian_border`, `correction_house`, `correction_houses`, `correction_houses_tunisia`, `controles_colons`, `french_algerian_judicial_remand`, `various_localities`, `convict_depots_algeria`, `convict_depots_tunisia`, `outside_work_sites`, `various_destinations` (one code per printed wording)
- `destination_fr`: line label as printed (the two dépôts de forçats lines as "Dépôts de forçats : Algérie / Tunisie")
- `observations_fr`: the *Observations* column as printed on the line (empty if blank); it tells apart the two Maison d'arrêt Alger lines (Appelants / Mandats d'arrêt)
- `measure`: `transfers` (*nombre de transfèrements*, transport operations) or `prisoners` (*nombre de détenus transférés*)
- `measure_fr`: printed column heading
- `value`: number of transfer operations or of prisoners transferred
- `flag`: empty, `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable` (SPEC.md)

Printed once per edition, sgt1922-sgt1935 (sgt1936 and sgt1939 print no such table). sgt1922-sgt1925 count the transfers out of the Prison de Tunis ("Prison de Tunis ; transfèrements"); from sgt1926 the table is the "Service des transfèrements" of all prisons, with other destinations. The two are kept in one file with `table_id` `transfers` and the edition telling them apart; the destination lines are as printed, one code per wording.

Not stored: the "Totaux" line (the check: both columns against it). Every printed total checks.

sgt1922 Prisons départementales: no number of transfers (») for 1.650 prisoners.

Every cell was read on the native-resolution page images (crop of the table, and each cell checked on an enlarged crop where a digit was faint).

Comparison (not a check: the two tables classify transfers differently): prisoners transferred (Totaux) against the sum of every transfer cell (`tr_*`, prison lines) of the *mouvement général* tables, men and women, all prisons (prisons_movement), from sgt1926 when this table covers all prisons: sgt1926 6103 / 6103; sgt1927 6134 / 6134; sgt1928 5559 / 5559; sgt1929 5215 / 5221; sgt1930 4661 / 4667; sgt1935 7284 / 7284. Equal in sgt1926-sgt1928 and sgt1935 (where the dépôts de forçats Tunisie line, 51, also equals the bagnes tunisiens column of the men's movement table as printed on its lines, not its printed Totaux 2.557); the movement tables give 6 more in sgt1929 and in sgt1930.

## Validation

- Checks against printed totals and identities: 20; passed: 20; failed: 0.

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (10 printings): sgt1922 f100, sgt1923 f584, sgt1924 f1074, sgt1925 f110, sgt1926 f662, sgt1927 f124, sgt1928 f648, sgt1929 f126, sgt1930 f660, sgt1935 f88.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
