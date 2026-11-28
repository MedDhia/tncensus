# Répartition des crédits réservés aux œuvres de protection et d'assistance de l'enfance

*Credits reserved for child-protection and child-assistance works, by work (sgt1924–sgt1930).*

Source: *Statistique générale de la Tunisie*, chapter III (health and assistance), editions sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / BnF.

Pages and views of the stored values: sgt1924 (`bpt6k9105649x`): p. 52, f1042, p. 53, f1043; sgt1925 (`bpt6k9105650k`): p. 52, f76, p. 53, f77; sgt1926 (`bpt6k9105650k`): p. 60, f624, p. 61, f625; sgt1927 (`bpt6k91056510`): p. 60, f88, p. 61, f89; sgt1928 (`bpt6k91056510`): p. 60, f612, p. 61, f613; sgt1929 (`bpt6k9105652d`): p. 62, f90; sgt1930 (`bpt6k9105652d`): p. 65, f623, p. 66, f624.

Transcriptions: `../transcribed/health_finance_<edition>.txt`, sections `[child_protection]`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_finance.py build`. Per-check output: `health_finance_validation.json`.

Rows: 266. Years: 1924–1930. Unit of `value`: francs; amounts are as printed, centimes kept as decimals (printed » = 0).

Printed once per edition; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (for a table over two pages, the page of the column group)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (budget year, account year or calendar year; see below)
- `section_fr`: the last one or two headings printed above the line
- `article`: article number as printed (`-` = printed without a number; letters/prefixes added where the edition numbers sub-items or restarts numbering by section, see the transcription file)
- `line_type`: `article` (a budget line with its own amount) or `detail` (an amount printed in the label column breaking down the article above it; do not add details to articles)
- `line_fr`: budget line / article label as printed (ditto marks expanded)
- `line_en`: English code built from the French label (key words translated, place names kept)
- `measure`: what the value is (see below)
- `column_fr`: column heading as printed (French)
- `value`: francs; empty where the flag says so
- `flag`: empty, or `derived_from_totals`, `total_mismatch`, `not_applicable`, `illegible`, `reprint_corrected` (see below)

"Tableau de répartition des crédits réservés aux œuvres de protection et d'assistance de l'enfance" (annex to the budget, sgt1924–sgt1930; decree of 15 January 1923): credit per work (Dispensaire Alapetite, Œuvre de la Crèche, orphanages, Institut héliothérapique du Kram, Gouttes de lait by region …). Columns and conventions as in `health_assistance_budget_credits` (Total and difference columns, "A reporter" and TOTAUX not stored; `detail` lines are breakdowns printed in the label column). sgt1930 adds the "Crédit global affecté par le Grand Conseil" (530.000) to a printed sub-total.

Failed checks: sgt1925 and sgt1929 articles sum to 50 less than the printed TOTAUX (234.950 vs 235.000, 464.950 vs 465.000; re-read on the images: the whole sgt1929 page and the last articles of sgt1925); sgt1928 the "A reporter" en plus 54.000 against cells summing to 51.400; sgt1930 TOTAUX Titre II printed 148.000 (148.800 in the sub-total and the recapitulation; the TOTAUX line is not stored).

## Remarks recorded in the transcriptions

- sgt1924: The nine Gouttes de lait items of 1.800 are printed in the label column under "Société de secours aux blessés militaires" and "Association des Dames françaises"; their sum, 16.200, is printed in the credits column after the last.
- sgt1925: The "A reporter" and "Reports" lines print no amounts.
- sgt1926: printed under the table: "en plus au budget de 1926 ... 20.000"
- sgt1927: The three sub-items of art. 9 (7.000, 7.000, 3.000 = 17.000) are printed in the label column; their columns print ». printed: net 85.000 ("En plus au budget de 1927 = 85.000": Art. 14, § 1 = 55.000; Titre II = 30.000).
- sgt1928: The "Report" on page 61 reprints the en plus column as 51.400 (A reporter on page 60: 54.000; cells sum to 51.400). printed below: En plus 54.900; En moins 14.000 (sic; 14.900 in the totals); En plus au budget de 1928: 40.000.
- sgt1930: The "Reports" line on page 66 prints the en moins column as 148.000 (A reporter on page 65: »). Final line: Titre II printed 148.000 (the subtotal and the summary on page 60 give 148.800). It is the sum of the subtotal and the Grand Conseil line. printed below: "En plus au budget de 1930 : 706.220 — 27.420 = 678.800 francs, à savoir : 1. Prélèvement sur le fonds de réserve de l'Assistance publique 148.800; 2. Crédit affecté par le Grand Conseil 530.000; [total] 678.800".

## Validation

- Checks against printed totals: 140; passed: 134; failed: 6.

Failed checks (printed values kept, unless a flag below says otherwise; `L<n>` = line of the transcription file). See the commentary above for which ones were re-read on the page images and which are repeated identically in several printings:

  - sgt1925 child_protection TOTAUX (line 132) col 0: cells give 234950, printed 235000
  - sgt1928 child_protection A reporter (line 116) col 1: cells give 51400, printed 54000
  - sgt1929 child_protection TOTAUX (line 135) col 0: cells give 464950, printed 465000
  - sgt1929 child_protection TOTAUX (line 135) col 2: cells give 483350, printed 483400
  - sgt1930 child_protection TOTAUX (line 156) col 1: cells give 148800, printed 148000
  - sgt1930 child_protection TOTAUX (line 156): titles vs total: cells give 1161400, printed 1162200

- Flagged cells: none.

## Cross-check with the main budget

Total of the child-protection table against the article of the main budget that reserves the credit (same edition): 7 comparisons, 6 equal.
  - sgt1929: child-protection TOTAUX 483400 vs main-budget article(s) 'Crédits réservés, suivant le tableau de répartition annexe, ' 483000; 'Versement au fonds de réserve du 5 % sur le montant du budge' 43950

