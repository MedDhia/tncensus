# État comparatif du personnel de garde avec l'effectif journalier maximum de chaque établissement de détention

*Guard staff compared with the maximum daily number of prisoners, by prison.*

Source: *Statistique générale de la Tunisie*, chapter *Établissements pénitentiaires*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 78, f102; sgt1923 (`bpt6k9105649x`): p. 84, f586; sgt1924 (`bpt6k9105649x`): p. 86, f1076; sgt1925 (`bpt6k9105650k`): p. 88, f112; sgt1926 (`bpt6k9105650k`): p. 99, f663; sgt1927 (`bpt6k91056510`): p. 97, f125; sgt1928 (`bpt6k91056510`): p. 97, f649; sgt1929 (`bpt6k9105652d`): p. 99, f127; sgt1930 (`bpt6k9105652d`): p. 103, f661; sgt1935 (`bpt6k9105653t`): p. 69, f89.

Transcriptions: `../transcribed/prisons_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_prisons.py build`.

Rows: 896. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935.

Units: prisoners (maximum daily population); staff members.

Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, with `year`; no year is printed by two editions.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section: `guard` (the table; printed as e) sgt1922-sgt1924, i) sgt1925-sgt1935) or `guard_note` (its footnote (1), sgt1922-sgt1925)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (the edition year: each edition prints the table for its own year)
- `establishment`: prison as printed
- `line`: `men`, `women`, `juveniles` (*Pupilles*, Djougar from sgt1928), `mine_detachment` (sgt1930), or empty for a prison printed on a single line without a sex label (sgt1922-sgt1925)
- `line_fr`: the line label as printed (Hommes, Femmes, Pupilles, détachement mines)
- `measure`: `max_daily` (*effectif maximum journalier*, the highest daily number of prisoners), `agents_french`, `agents_indigenous`, `wardresses` (*surveillantes*), `agents_indigenous_temporary` (footnote)
- `measure_fr`: printed column heading
- `value`: prisoners (max_daily) or staff (persons)
- `flag`: empty, `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable` (SPEC.md)

Printed once per edition, sgt1922-sgt1935 (sgt1936 and sgt1939 print no such table).

The prisons holding women are printed on two braced lines, Hommes and Femmes (Djougar from sgt1928: Hommes and Pupilles). The maximum daily population is given per line. The staff columns belong to the prison as a whole: they are printed beside one of the two lines, with » on the other (agents usually on the Hommes line and surveillantes on the Femmes line; sgt1923 prints all the staff of the smaller prisons on the Femmes line, and Tunis's two surveillantes on the Hommes line). Each printed cell is stored on the line it is printed on, so the staff of a prison is the sum over its lines; `line` is not a sex breakdown of the staff.

Footnote (1) to "Agents indigènes" (sgt1922-sgt1925): "N agents indigènes temporaires au Djebel-Djougar" (20, 20, 25, 27); stored as table_id `guard_note`. sgt1923 prints only the call "(1)" in the Djebel-Djougar agents indigènes cell (stored NA, not_applicable).

Not stored: the "Totaux" line; it is the check (every column against it). sgt1926 prints the Totaux line empty (no check possible). sgt1935 prints « under effectif maximum journalier on the Totaux line (no total; the lines sum to 3.874). sgt1922 Salahia: a line with » everywhere.

Every cell was read on the native-resolution page images (crop of the table).

## Validation

- Checks against printed totals and identities: 35; passed: 35; failed: 0.

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: not_applicable: 1.

  - sgt1923 p.84 1923 Djebel-Djougar /  / agents_indigenous = NA (not_applicable)

## Image versus OCR

- Read cell by cell on the page images (14 printings): sgt1922 f102, sgt1923 f586, sgt1924 f1076, sgt1925 f112, sgt1926 f663, sgt1927 f125, sgt1928 f649, sgt1929 f127, sgt1930 f661, sgt1935 f89, sgt1922 f102, sgt1923 f586, sgt1924 f1076, sgt1925 f112.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
