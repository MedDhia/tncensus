# 1926 census: Europeans by profession and nationality

**f) Population européenne par profession et nationalité**
*European population by occupational category, nationality, status (persons exercising the
profession themselves, or family members of the preceding) and sex* (census of 1926).

Source: *Statistique générale de la Tunisie*, edition 1926 (`sgt1926`), Gallica ark
`bpt6k9105650k`, printed pages 10-11, views 574-575. Source gallica.bnf.fr / Ministère des
Affaires étrangères. Transcription: `transcribed/cens1926_f_sgt1926.txt`.

One row per printed cell: 6 nationalities x 9 categories x 2 statuses x 2 sexes. `value` = persons.
The printed subtotals (active, family, nationality total per category), the TOTAUX line and the
"Totaux" block for all Europeans are not stored; they were used for validation (the all-Europeans
cells equal the sum of the nationalities).

Footnotes (translated): (1) rural owners, farmers, sharecroppers, managers, foremen, gardeners and
farm workers of every kind; (2) staff of all shops (other than those of industrial
establishments), banks, insurance companies, brokerage and rental agencies, etc.; (3) masters and
workers of all trades actually engaged in manufacturing: mines, quarries, salt works, oil mills,
soap works, tanneries, factories, public-works contractors, fisheries, etc.; (4) staff of shipping
and railway companies, carriers, hauliers and their employees, car and carriage hirers and their
staff; (5) staff of all civil services of the State or the municipalities, including the
judiciary and law officers; (6) police staff; (7) lawyers, doctors, pharmacists, dentists, business
agents, expert arbitrators, artists, clergy and members of religious communities; (8) persons who,
living on income from annuities, securities, rents, etc., are assumed not to exercise a profession;
(9) persons who fit none of the preceding categories.

## Validation

335 checks (every M+F subtotal, every category total, every column against TOTAUX, each nationality
total against table e, and each all-Europeans cell against the sum of the nationalities); 18 fail.

One data cell is flagged: French industry, active women, printed 518 in all five editions; the
printed active subtotal (4.846) and the all-Europeans industry column (1.533) both imply 510
(`total_mismatch`, printed value kept). The other failures are in printed total lines, which are not
stored: the French TOTAUX line (22.825 / 10.760, where the cells give 22.856 / 10.737 and the
all-Europeans totals agree with the cells), the Maltese active total (printed 1.258 for 4.258), the
Spanish active women total (105 for 106) and the all-Europeans family-women total (65.386 for
65.387).

Failing checks:   french industry active M+F: cells 4854 != printed 4846;   french col 0 vs TOTAUX: cells 22856 != printed 22825;   french col 1 vs TOTAUX: cells 10737 != printed 10760;   maltese total active M+F: cells 4258 != printed 1258;   maltese total subtotals: cells 5396 != printed 8396;   maltese subtotal 0 vs TOTAUX: cells 4258 != printed 1258;   spanish col 1 vs TOTAUX: cells 106 != printed 105;   spanish subtotal 0 vs TOTAUX: cells 311 != printed 310;   spanish subtotal 2 vs TOTAUX: cells 518 != printed 517;   all_europeans col 3 vs TOTAUX: cells 65387 != printed 65386;   all_europeans subtotal 1 vs TOTAUX: cells 96894 != printed 96893;   all_europeans subtotal 2 vs TOTAUX: cells 173282 != printed 173281;   all industry col 1 = sum of nationalities: cells 1541 != printed 1533;   all total col 0 = sum of nationalities: cells 55461 != printed 55492;   all total col 1 = sum of nationalities: cells 20926 != printed 20896;   all total col 3 = sum of nationalities: cells 65387 != printed 65386;   all total subtotal 0 = sum of nationalities: cells 73387 != printed 76388;   all total subtotal 1 = sum of nationalities: cells 96894 != printed 96893.

## Reprints

sgt1930 (views 568-569) was compared visually in full, and sgt1927 (38-39), sgt1928 (562-563) and
sgt1929 (38-39) row by row on the rows that decide a mismatch (French industry, French TOTAUX,
Spanish unclassified and totals). No reprint changes a data cell. sgt1930 has two printing errors of
its own in subtotals (Spanish unclassified nationality total 96 for 136; Greek liberal professions
family women 8 with a family subtotal of 6); the sgt1926 values, which add up, are kept.
