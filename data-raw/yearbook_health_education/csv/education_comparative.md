# Tableau comparatif

*Comparative table: establishments, classes, public pupils by nationality and sex, adult auditors, private pupils.*

Source: *Statistique générale de la Tunisie*, chapter "Instruction publique et beaux-arts" (VII; VI in sgt1936 and sgt1939), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1922 (`bpt6k9105649x`): p. 128, f152; sgt1923 (`bpt6k9105649x`): p. 134, f636; sgt1924 (`bpt6k9105649x`): p. 136, f1126; sgt1925 (`bpt6k9105650k`): p. 138, f162; sgt1926 (`bpt6k9105650k`): p. 148, f712; sgt1927 (`bpt6k91056510`): p. 146, f174; sgt1928 (`bpt6k91056510`): p. 146, f698; sgt1929 (`bpt6k9105652d`): p. 148, f176; sgt1930 (`bpt6k9105652d`): p. 152, f710; sgt1935 (`bpt6k9105653t`): p. 88, f108; sgt1936 (`bpt6k91056547`): p. 66, f77; sgt1939 (`bpt6k9105739w`): p. 70, f76.

Transcriptions: `../transcribed/education_sum_<edition>.txt`; rebuild with `python3 data-raw/yearbook_health_education/extract_education_summary.py build`. Per-check output: `education_summary_validation.json`.

Rows: 270. Years: 1921–1939 (15 years: 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1934, 1935, 1936, 1938, 1939).

Printed for overlapping year windows: every cell of a year is taken from the **latest** edition that prints that year (SPEC_ADDENDUM rule 4; `census` = that edition) and every other printing of the same cell is compared below. Duplicate printings are not stored.

Years printed by each edition: sgt1922 1921, 1922; sgt1923 1922, 1923; sgt1924 1923, 1924; sgt1925 1924, 1925; sgt1926 1925, 1926; sgt1927 1926, 1927; sgt1928 1927, 1928; sgt1929 1928, 1929; sgt1930 1929, 1930; sgt1935 1934, 1935; sgt1936 1935, 1936; sgt1939 1938, 1939.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number; pages without a printed number are inferred from the next page. For the two-page spreads (population, primary-education and first-degree totals) the boys' block is given the left-hand page and the girls' block and total columns the right-hand page (the printed fold falls near the boys' TOTAUX, so one or two boys' columns may in fact sit on the right-hand page)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (31 December of that year for pupils; the school year's examinations)
- `item`: English code (see below)
- `item_fr`: row label as printed in the edition the value is taken from
- `sex`: `male`, `female`; `total` where the cell is not split by sex (empty in the comparative table for items that are not pupils)
- `nationality`: `french`, `muslim`, `jewish`, `italian`, `maltese`, `other` (Divers); `total` where not split
- `value`: count (integer); printed » = 0; empty where the cell is not printed (`not_applicable`)
- `flag`: empty, or `ocr_corrected`, `derived_from_totals`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (TOTAUX, Totaux généraux, subtotals, A reporter) are not stored unless stated; they were used for validation.

Comparative statistics c) "Tableau comparatif" (two years per edition). Items: `n_public_establishments` (Nombre total d'établissements scolaires publics; footnote (1): including the school of music and the Higher School of Arabic, from sgt1939 also the school of commerce), `n_public_primary_schools`, `n_public_primary_classes`, `n_private_schools`; `pupils_public` by `sex` and `nationality` (public education, excluding adult auditors; equal to the population table's "Total de l'enseignement public"), `adult_auditors` (Auditeurs des cours d'adultes), `private_pupils`. The printed totals (Nombre total des élèves de l'enseignement public, Comparaison par sexes, Total général) are checks only. sgt1939 changes the establishment items: `n_second_degree_establishments`, `n_first_degree_establishments` (footnote (a): of which 11 closed because of the war), `n_public_establishments` (b: of which 61 closed), `n_first_degree_classes`, and no count of private schools; its "Nombre total des élèves de l'enseignement public" excludes the adult auditors and its Total général includes them, the opposite of the earlier editions for the public total (footnote (3): credits for adult courses reduced).

Failed checks: sgt1922, 1921 column: the boys and girls by nationality sum to 26.020 and 14.774 against the printed comparaison par sexes 27.951 and 14.816; the cells plus the 1.973 adult auditors give the printed public total 42.767, which also equals 27.951 + 14.816: the comparaison par sexes line of 1921 includes the auditors (cells kept as printed). sgt1936, 1935 column: public pupils printed 83.914 (cells give 83.944, as sgt1935 printed), and 487 establishments / 477 primary schools against 490 / 480 in sgt1935 (rule 4 keeps sgt1936). 1929: sgt1929 prints 451 establishments and 461 primary schools, sgt1930 461 and 451; establishments exceed primary schools by 10 in every other year, so sgt1930 (kept) is consistent. 1929 Musulmanes 3.173 (both printings) against 3.179 in the population table's total public row, whose own rows sum to 3.173.

## Footnotes printed under the table

- (1) Y compris l'école de musique et l'école supérieure de langue et de littérature arabes. (2) Non compris les auditeurs des cours d'adultes. (sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936)
- (1) Y compris l'école de musique, l'école supérieure de langue et de littérature arabes et l'école de commerce. (2) Non compris les auditeurs des cours d'adultes. (3) Crédits pour cours d'adultes diminués. (a) Dont 11 fermées en raison des conditions créées par l'état de guerre. (b) Dont 61 fermées. (sgt1939)

## Validation

- Checks against printed totals: 96; passed: 92; failed: 4.

Failed checks (every cell involved was re-read on a native-resolution crop; the printed figures are as transcribed; see the commentary above):

  - sgt1922 1921: boys by nationality vs comparaison par sexes, garçons: cells give 26020, printed 27951
  - sgt1922 1921: girls by nationality vs comparaison par sexes, filles: cells give 14774, printed 14816
  - sgt1936 1935: pupils + adult auditors vs total public: cells give 83944, printed 83914
  - sgt1936 1935: total public + private vs total général: cells give 91995, printed 92025

- Overlapping printings: 162 cell comparisons between editions; 4 differences.

| year | cell | edition | printed | latest edition | printed | stored (edition, flag) |
|---|---|---|---|---|---|---|
| 1929 | n_public_establishments | sgt1929 | 451 | sgt1930 | 461 | 461 (sgt1930) |
| 1929 | n_public_primary_schools | sgt1929 | 461 | sgt1930 | 451 | 451 (sgt1930) |
| 1935 | n_public_establishments | sgt1935 | 490 | sgt1936 | 487 | 487 (sgt1936) |
| 1935 | n_public_primary_schools | sgt1935 | 480 | sgt1936 | 477 | 477 (sgt1936) |

- Flagged cells: none.

## Cross-checks with other tables of the chapter

- 156 comparisons; equal: 155; different: 1.
  - sgt1929 pupils muslim female 1929 vs population table, total public: cells give 3173, printed 3179
