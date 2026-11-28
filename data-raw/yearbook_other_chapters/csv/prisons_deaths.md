# État numérique des décès par prison et par maladie

*Deaths of prisoners by prison and by disease.*

Source: *Statistique générale de la Tunisie*, chapter *Établissements pénitentiaires*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 77, f101; sgt1923 (`bpt6k9105649x`): p. 83, f585; sgt1924 (`bpt6k9105649x`): p. 85, f1075; sgt1925 (`bpt6k9105650k`): p. 87, f111; sgt1926 (`bpt6k9105650k`): p. 98, f662; sgt1927 (`bpt6k91056510`): p. 96, f124; sgt1928 (`bpt6k91056510`): p. 96, f648; sgt1929 (`bpt6k9105652d`): p. 98, f126; sgt1930 (`bpt6k9105652d`): p. 102, f660; sgt1935 (`bpt6k9105653t`): p. 68, f88.

Transcriptions: `../transcribed/prisons_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_prisons.py build`.

Rows: 3054. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935.

Unit: deaths.

Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, with `year`; no year is printed by two editions.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section name (`deaths`); printed as table d) (sgt1922-sgt1924) or h) (sgt1925-sgt1935)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (the edition year: each edition prints the table for its own year)
- `establishment`: line label as printed; the lines braced under Tunis are stored as "Tunis : <line>" (sgt1924-sgt1925 print the brace without the word Tunis)
- `disease`: code of the printed disease column (snake_case of the French heading, one code per disease; spelling variants of the same heading share a code)
- `disease_fr`: printed column heading of this edition (misprints kept, with the reading in brackets)
- `value`: number of deaths
- `flag`: empty, `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable` (SPEC.md)

Printed once per edition, sgt1922-sgt1935 (sgt1936 and sgt1939 print no such table). The disease columns are recast every edition (17 to 29 columns; only those with a death in the year, plus a few with none); a disease not printed in an edition has no rows. Prison lines change too (the Tunis lines: infirmerie pénitentiaire / de la prison / des femmes sgt1922-sgt1925, infirmerie centrale / de la prison / hôpitaux sgt1926-sgt1927, infirmerie centrale / de la prison and a separate Hôpitaux line sgt1928-sgt1930, infirmerie pénitentiaire / détention et hôpitaux sgt1935; Hôpital Sadiki et hôpital civil sgt1922-sgt1925; Chantiers extérieurs sgt1935).

Not stored: the "TOTAUX" column and line (the checks: each line's cells against its total, each column against the Totaux line).

sgt1930 failures, kept as printed (re-read on enlarged crops): Tunis Infirmerie centrale cells sum to 48 for a printed total 47 (its congestion pulmonaire 1 is printed on that line; the column total 2 counts it); Infirmerie de la prison cells sum to 25 for 22, including an "Affectation cardiaque" 4 whose column total is printed » (flagged). The printed line totals sum to the grand total 95, and so do the printed column totals.

Every cell was read on the native-resolution page images (one crop per half of the table).

Cells flagged `total_mismatch` (printed value kept, re-read on a native-resolution crop): sgt1930: Tunis : Infirmerie de la prison / affection_cardiaque (printed 4 under Affectation cardiaque, whose Totaux is printed »; the line's cells sum to 25 for a printed 22).

Comparison (not a check): deaths (Totaux) against the décédés of the mouvement général tables, men + women Totaux (prisons_movement), per edition: sgt1922 203 / 196; sgt1923 138 / 124; sgt1924 112 / 102; sgt1925 114 / 105; sgt1926 74 / 69; sgt1927 134 / 134; sgt1928 136 / 116; sgt1929 115 / 114; sgt1930 95 / 88; sgt1935 61 / 62. Equal in sgt1927; in sgt1922 and sgt1928 the difference is exactly the hospital line of this table (Hôpital Sadiki et hôpital civil 7; Hôpitaux 20); the other editions are not reconciled.

## Validation

- Checks against printed totals and identities: 373; passed: 370; failed: 3.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1930 p.102 (f660) deaths Tunis : Infirmerie centrale: total = tuberculose + grippe + pneumonie + bronchite + affection_cardiaque + cachexie + syphilis + fievre_typhoide + paludisme + typhus + dysenterie + nephrite + traumatisme_cranien + pachymeningite + chlorose + enterite_tuberculeuse + pleuresie + congestion_pulmonaire: cells give 48, printed 47 (difference -1)
  - sgt1930 p.102 (f660) deaths Tunis : Infirmerie de la prison: total = tuberculose + grippe + pneumonie + bronchite + affection_cardiaque + cachexie + syphilis + fievre_typhoide + paludisme + typhus + dysenterie + nephrite + traumatisme_cranien + pachymeningite + chlorose + enterite_tuberculeuse + pleuresie + congestion_pulmonaire: cells give 25, printed 22 (difference -3)
  - sgt1930 p.102 (f660) deaths affection_cardiaque: lines vs Totaux: cells give 4, printed 0 (difference -4)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: total_mismatch: 1.

  - sgt1930 p.102 1930 Tunis : Infirmerie de la prison / affection_cardiaque = 4 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (10 printings): sgt1922 f101, sgt1923 f585, sgt1924 f1075, sgt1925 f111, sgt1926 f662, sgt1927 f124, sgt1928 f648, sgt1929 f126, sgt1930 f660, sgt1935 f88.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
