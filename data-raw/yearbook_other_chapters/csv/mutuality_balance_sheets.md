# Banques populaires : bilans de la Banque populaire française de Tunisie (et compte de profits et pertes) et de la Coopérative tunisienne de crédit ; Sociétés coopératives de consommation : bilan de « La Maison Française »

*Balance sheets of the Banque populaire française de Tunisie (with its profit and loss account), the Coopérative tunisienne de crédit and the consumers' cooperative « La Maison Française », sgt1926-sgt1930.*

Source: *Statistique générale de la Tunisie*, chapter *Institutions économiques et sociales / Mutualité agricole*, editions sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1926 (`bpt6k9105650k`): p. 468, f1032, p. 470, f1034, p. 471, f1035; sgt1927 (`bpt6k91056510`): p. 468, f496, p. 470, f498, p. 471, f499; sgt1928 (`bpt6k91056510`): p. 472, f1024, p. 473, f1025, p. 474, f1026, p. 475, f1027, p. 476, f1028, p. 477, f1029; sgt1929 (`bpt6k9105652d`): p. 474, f502, p. 475, f503, p. 476, f504, p. 477, f505, p. 478, f506, p. 479, f507; sgt1930 (`bpt6k9105652d`): p. 480, f1038, p. 481, f1039, p. 482, f1040, p. 483, f1041, p. 484, f1042, p. 485, f1043.

Transcriptions: `../transcribed/mutuality_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_mutuality.py build`.

Rows: 365. Years: 1926, 1927, 1928, 1929, 1930.

Unit: francs (centimes as decimals); suggested value_type: francs.

Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept (`census` = edition).

## Columns

- `census`: edition (each edition kept)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the balance date (« La Maison Française » sgt1928-sgt1930, no date printed: edition year)
- `institution`: `banque_populaire_francaise`, `cooperative_tunisienne_credit`, `maison_francaise` (the consumers' cooperative « La Maison Française », called « Société coopérative de consommation » in sgt1927)
- `institution_fr`: institution as named in the title
- `date_fr`: balance date as printed (empty: not printed)
- `statement`: `balance_sheet` (bilan) or `profit_loss` (compte de profits et pertes, Banque populaire only)
- `side`: `assets` (actif) / `liabilities` (passif); `debit` / `credit` for the profit and loss account
- `line_no`: order of the line within its side as printed (subtotals and totals not counted)
- `line_type`: `item` (a line of the side; the items add up to the side total) or `detail` (sgt1928 Banque populaire: movements printed in a brace inside an item: balance of the previous year, entries, exits; not part of the side total)
- `item`: English code of the line (shared by equivalent lines of different editions; place suffixes _tunis/_la_goulette/_franceville for the branches of « La Maison Française »)
- `item_fr`: label as printed; nested headings joined with ' : ' (ditto dashes written out)
- `unit`: francs
- `value`: printed value (» = 0; centimes as decimals)
- `flag`: empty or `total_mismatch` (printed cell contradicted by the printed sum it enters)

Printed at the end of the chapter *Mutualité agricole et commerciale* in sgt1926-sgt1930 (not before; not in sgt1935 or later). One balance per institution and edition (SPEC_ADDENDUM rule 5), stored line by line in printed order with `side` and `statement`. Banque populaire française: balance at 31 December of the edition year and its compte de profits et pertes. Coopérative tunisienne de crédit: balance at 31 December. « La Maison Française »: balance at 11 April 1926 (exercice 1925-1926), at 24 April 1927 (exercice 1926-1927), then without a date in sgt1928-sgt1930; sgt1930 reprints the sgt1929 balance unchanged (both kept, as printed in each edition).

Group figures printed in an outer column (« La Maison Française »: valeurs réalisables, disponibles, immobilisées ...; Banque populaire 1928 réserves) and the side totals are checks, not rows. Checks: each group figure = its lines; each side total = its items; assets = liabilities and debit = credit; the Banque populaire bénéfice net (profit and loss) = profits et pertes (liabilities); for the sgt1928 brace movements, printed sum = previous balance + entries and balance = printed sum - exits.

Item codes are translations of the printed lines; labels change between editions (e.g. Effets escomptés 1926 / Effets à recevoir 1927-1930 are both `bills_*` codes as printed), so codes follow the label, not a harmonised chart of accounts. The asset line « Résultat d'inventaire » of « La Maison Française » (1928-1930) is a loss; its liability « Solde ou bénéfice net » (1926) a profit.

Every failed check below was re-read on a native-resolution crop: the printed values are kept. sgt1928 Banque populaire, comptes-courant: the solde de l'exercice précédent is printed 565.731,84 (2.5x crop), 10 more than the printed sum 13.710.898,43 minus the avances 13.145.176,59 and than the comptes courants 565.721,84 of the sgt1927 balance: flagged `total_mismatch`. « La Maison Française », valeurs immobilisées: sgt1928 group figure 967.961,94 for four lines giving 956.977,66 (10.984,28 short; a blank line stands between Mobilier et Matériel and Titres et Valeurs, an item evidently dropped); sgt1929 and its reprint sgt1930 1.038.953,09 for six lines giving 990.488,49 (48.464,60 short, no line identifiable); in all three the group figure gives the side total. Coopérative tunisienne de crédit: sgt1929 passif lines give 6.436.403,15 for the printed total 6.438.403,15 (2.000 short; the actif adds up); sgt1930 actif lines give 8.058.412,30 (only three lines printed: 80.000 short) and passif lines 8.138.403,30 (9,00 short) for the printed totals 8.138.412,30. Banque populaire passif totals: sgt1928 printed 9.241.999,30 for items giving 9.241.999,35 (0,05; the actif total 9.241.999,30 equals it) and sgt1929 printed 12.404.456,46 for items giving 12.404.466,46 (10,00; equal to the printed actif total); every item re-read on the crop. None of these can be assigned to one cell, so no flag.

Survey of the whole chapter in every edition: `mutuality_survey.md`.

## Validation

- Checks against printed totals and identities: 117; passed: 105; failed: 12.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1928 p.472 (f1024) bilan [bpf assets] 2 — Comptes-courant (Avances en cours): printed sum = solde précédent + entries: cells give 13710908.43, printed 13710898.43 (difference -10.00)
  - sgt1928 p.473 (f1025) bilan [bpf liabilities] TOTAL = sum of the items: cells give 9241999.35, printed 9241999.30 (difference -0.05)
  - sgt1928 p.476 (f1028) bilan [mf assets] subtotal Valeurs immobilisées = its lines: cells give 956977.66, printed 967961.94 (difference 10984.28)
  - sgt1928 p.476 (f1028) bilan [mf assets] TOTAL = sum of the items: cells give 1303600.92, printed 1314585.20 (difference 10984.28)
  - sgt1929 p.475 (f503) bilan [bpf liabilities] TOTAL = sum of the items: cells give 12404466.46, printed 12404456.46 (difference -10.00)
  - sgt1929 p.477 (f505) bilan [ctc liabilities] TOTAL = sum of the items: cells give 6436403.15, printed 6438403.15 (difference 2000.00)
  - sgt1929 p.478 (f506) bilan [mf assets] subtotal Valeurs immobilisées = its lines: cells give 990488.49, printed 1038953.09 (difference 48464.60)
  - sgt1929 p.478 (f506) bilan [mf assets] TOTAL = sum of the items: cells give 1279564.75, printed 1328029.35 (difference 48464.60)
  - sgt1930 p.482 (f1040) bilan [ctc assets] TOTAL = sum of the items: cells give 8058412.30, printed 8138412.30 (difference 80000.00)
  - sgt1930 p.483 (f1041) bilan [ctc liabilities] TOTAL = sum of the items: cells give 8138403.30, printed 8138412.30 (difference 9.00)
  - sgt1930 p.484 (f1042) bilan [mf assets] subtotal Valeurs immobilisées = its lines: cells give 990488.49, printed 1038953.09 (difference 48464.60)
  - sgt1930 p.484 (f1042) bilan [mf assets] TOTAL = sum of the items: cells give 1279564.75, printed 1328029.35 (difference 48464.60)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: total_mismatch: 1.

  - sgt1928 p.472 1928 banque_populaire_francaise / balance_sheet / assets / 2 / detail / current_accounts_opening_balance / francs = 565731.84 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (40 printings): sgt1926 f1032, sgt1926 f1032, sgt1926 f1032, sgt1926 f1032, sgt1926 f1032, sgt1926 f1032, sgt1926 f1034, sgt1926 f1035, sgt1927 f496, sgt1927 f496, sgt1927 f496, sgt1927 f496, sgt1927 f496, sgt1927 f496, sgt1927 f498, sgt1927 f499, sgt1928 f1024, sgt1928 f1025, sgt1928 f1024, sgt1928 f1025, sgt1928 f1026, sgt1928 f1027, sgt1928 f1028, sgt1928 f1029, sgt1929 f502, sgt1929 f503, sgt1929 f502, sgt1929 f503, sgt1929 f504, sgt1929 f505, sgt1929 f506, sgt1929 f507, sgt1930 f1038, sgt1930 f1039, sgt1930 f1038, sgt1930 f1039, sgt1930 f1040, sgt1930 f1041, sgt1930 f1042, sgt1930 f1043.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
