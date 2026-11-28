# Mouvement général d'entrée et de sortie. Effectif au 31 décembre

*Prison population movement by prison: population at 1 January, entries and exits by kind, population at 31 December, days of detention (men and boys; women and girls).*

Source: *Statistique générale de la Tunisie*, chapter *Établissements pénitentiaires*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 74, f98, p. 75, f99, p. 76, f100, p. 77, f101; sgt1923 (`bpt6k9105649x`): p. 80, f582, p. 81, f583, p. 82, f584, p. 83, f585; sgt1924 (`bpt6k9105649x`): p. 82, f1072, p. 83, f1073, p. 84, f1074, p. 85, f1075; sgt1925 (`bpt6k9105650k`): p. 84, f108, p. 85, f109, p. 86, f110, p. 87, f111; sgt1926 (`bpt6k9105650k`): p. 96, f660, p. 97, f661; sgt1927 (`bpt6k91056510`): p. 94, f122, p. 95, f123; sgt1928 (`bpt6k91056510`): p. 94, f646, p. 95, f647; sgt1929 (`bpt6k9105652d`): p. 96, f124, p. 97, f125; sgt1930 (`bpt6k9105652d`): p. 100, f658, p. 101, f659; sgt1935 (`bpt6k9105653t`): p. 66, f86, p. 67, f87; sgt1936 (`bpt6k91056547`): p. 48, f59, p. 49, f60; sgt1939 (`bpt6k9105739w`): p. 48, f54, p. 49, f55.

Transcriptions: `../transcribed/prisons_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_prisons.py build`.

Rows: 6382. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939.

Units: persons; days of detention.

Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, with `year`; no year is printed by two editions.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section: `movement_men` (*Hommes et jeunes garçons*), `movement_women` (*Femmes et jeunes filles*)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (the table is a two-page spread; each cell has its own page)
- `gallica_view`: Gallica view of the page the cell is printed on
- `year`: year of the figures (the edition year: each edition prints the table for its own year)
- `sex_group`: `men_boys` or `women_girls` (one table each)
- `sex_group_fr`: as printed in the table heading
- `establishment`: prison as printed
- `flow`: `stock` (population at 31 December of the previous year / of the year), `entry`, `exit`, `days`
- `measure`: column code: `start`, entries (`in_free`, `in_other_prisons`, `re_escape`, `re_colons`, `re_hospital`, `re_conditional`, `re_provisional`), exits (`out_sentence`, `out_pardon_amnesty`, `out_pardon`, `out_provisional`, `out_acquittal`, `out_conditional`, `out_administrative`, transfers `tr_central`, `tr_correction`, `tr_convict_depots`, `tr_other_prisons`, `tr_work_sites`, `tr_various`, `tr_hospitals`, `out_colons_controles`, `out_escaped`, `out_died`, `out_executed`), `end`, `detention_days`
- `measure_fr`: printed column heading (group heading, then column)
- `value`: persons (stocks, entries, exits) or days of detention
- `flag`: empty, `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable` (SPEC.md)

Two tables per edition, printed in every edition sgt1922-sgt1939 (a) and b) of *Mouvement de la population* sgt1922-sgt1924, e) and f) sgt1925-sgt1935, without a letter in sgt1936 and sgt1939, inside chapter IV): men and boys, women and girls, by prison. Each is a two-page spread (sgt1926-sgt1939: both tables on the same spread, men above, women below); every cell has the page and view it is printed on. sgt1936 and sgt1939 keep sgt1935's layout (transfers split en Algérie / en Tunisie; sgt1936-sgt1939 add *par amnistie* and *dépôt de forçats* en Algérie).

The columns are recast several times; each printed column has its own code and heading (`measure`, `measure_fr`), and a column not printed in an edition has no rows: réintégrés colons and *colons et contrôles* (sgt1922-sgt1923, men), transfers to *diverses localités* and *expulsés dirigés sur la frontière algérienne* (sgt1923-sgt1925), *maisons de correction* / *dépôts de forçats* / *chantiers extérieurs* / *diverses destinations* (sgt1926-sgt1930), the Algeria / Tunisia split of transfers and *venant des hôpitaux* (sgt1935). The prisons also change: La Goulette up to sgt1927 (sgt1927: all transferred out, no days), an "Hôpitaux" line with days only (sgt1930), Détachements extérieurs (sgt1935); the women's tables print only the nine prisons holding women from sgt1926.

Several headings print a wrong year (sgt1922-sgt1923 women "Entrées pendant l'année 1921 / 1922"; sgt1927 every heading one year behind; sgt1928-sgt1929 "Sorties pendant l'année 1927 / 1928", "Population au 31 décembre 1926"); the figures are those of the edition year (the starting population equals the previous edition's population at 31 December, below). sgt1929: the two halves of p. 97 carry each other's headings (Femmes above, Hommes below); stored by content.

Not stored: the "Total des entrées" and "Total des sorties" columns and the "Totaux" lines; they are the checks. Stored: population at 31 December of the previous year (`start`) and of the year (`end`), each kind of entry and exit, and the days of detention.

Checks: Total des entrées = the entry columns and Total des sorties = the exit columns on every line (Totaux included); population at 31 December = previous population + entries − exits on every line; every column against the Totaux line; per edition, men's + women's Totaux against the récapitulation's line for the year (start, entries, exits, end, days); per edition and prison, men's + women's days of detention against the days of table d) (*prisons_expenditure*; sgt1930: the "Hôpitaux" line is counted with Tunis, whose table d) days include it).

Failures involving only printed totals (not stored; re-read on enlarged crops): sgt1922 Totaux, transférés dans les maisons centrales printed 695 for lines summing to 605 (the Totaux line's Total des sorties 14.890 needs 605); sgt1928 and sgt1929 Totaux, par expiration de peine printed 7.468 and 6.459 for lines summing to 7.168 and 6.159 (both Totaux lines' Total des sorties need the sums); sgt1929 Totaux, de l'état de liberté printed 19.325 for 10.325; sgt1935 Sfax, Total des entrées printed 1.669 for cells summing to 1.569 (which gives Sfax's 31 December population and the column's printed 19.557).

sgt1935 men, unlocated: the bagnes tunisiens column prints 51 on the Tunis line and » on every other line, but 2.557 on the Totaux line; and six lines are short of their printed Total des sorties (Sousse 2, Tunis 18, Le Bardo 3, Porto-Farina 14, Djebel Djougar 8, Détachements extérieurs 6: 51 in all) while their 31 December populations check with the printed totals. The printed cells are kept, unflagged.

sgt1936 men, Tunis, transférés dans les maisons d'arrêt printed 345 where the line and the column total need 145 (flagged). sgt1939 men: the Totaux line's days of detention (1.267.582) are the men's lines (1.245.734) plus the women's (21.848), and the récapitulation prints the same 1.267.582 for 1939; the two failures this causes (men's days column, men + women days against the récapitulation) are the printing, not a cell.

Cross-table finding outside this file: sgt1924 Porto-Farina, men's days of detention 133.096 here against 133.086 in table d), whose days column is 10 short of its printed Totaux (an unlocated difference in *prisons_expenditure*): the table d) figure is the misprint; it is left as printed and unflagged there.

Every cell of every edition was read on the native-resolution page images (one crop per page half, the binding columns on separate enlarged crops), and each failing line or column re-read on a separate enlarged crop.

Cells flagged `total_mismatch` (printed value kept, re-read on a native-resolution crop): sgt1923: Béja / re_provisional (printed »: the Béja Total des entrées (256) and the column total (97) are both 5 more than the cells); sgt1925: Sousse / end (printed 183; 193 + 1.711 − 1.715 = 189, and the column total 3.094 (with the women's 70 the récapitulation's 3.164) needs 189); sgt1925: Sousse / out_provisional (printed »: the Sousse Total des sorties (38) and the column total (66) are both 7 more than the cells); sgt1929: Kairouan / out_provisional (printed 32: the Kairouan exits sum to 824 for a printed Total des sorties 866 (which gives the 31 December population), Le Kef's to 1.102 for 1.120, and the libération provisoire column to 960 for a printed 1.020 = 960 + 42 + 18; no other column is short); sgt1929: Le Kef / out_provisional (printed »: see Kairouan (Le Kef is 18 short)); sgt1929: Gabès / end (printed 57; 89 + 584 − 606 = 67, and the column total 1.921 needs 67); sgt1929: Bizerte / detention_days (printed 7.657: the days column sums to 927.134 for a printed 927.135, and men's + women's days (7.657 + 166) are 1 short of the 7.824 days of table d)); sgt1936: Tunis / tr_tun_remand (printed 345 (clear on an enlarged crop): the Tunis Total des sorties (9.782, which gives the 31 December population) and the column total (3.386) both need 145); sgt1929: Gabès / in_free (printed 3: the Gabès Total des entrées (10) and the column total (335) are both 6 more than the cells); sgt1935: Kairouan / detention_days (printed 12.986: the days column sums to 1.057.661 for a printed 1.077.661, and men's + women's days (12.986 + 2.101) are 20.000 short of the 35.087 days of table d)); sgt1929: Gabès / end, Gafsa / end, Kairouan / end, Le Kef / end, Sfax / end, Sousse / end, Tunis / end (the "Population au 31 décembre 1929" column repeats the "au 31 décembre 1928" column on every line (Totaux 67 for both); start + entries − exits gives 58 for all prisons, which with the men's 1.921 is the récapitulation's 1.979).

Continuity (each edition's population at 31 December of the previous year against the previous edition's population at 31 December, per table and prison, Totaux included): 225 comparisons, 10 differences (the stored cells among them are flagged `total_mismatch` in the earlier printing): men_boys Sousse: sgt1926 prints 189 at 31 December 1925, sgt1925 printed 183; men_boys Gabès: sgt1930 prints 67 at 31 December 1929, sgt1929 printed 57; women_girls Gabès: sgt1930 prints 0 at 31 December 1929, sgt1929 printed 2; women_girls Gafsa: sgt1930 prints 0 at 31 December 1929, sgt1929 printed 3; women_girls Kairouan: sgt1930 prints 4 at 31 December 1929, sgt1929 printed 0; women_girls Le Kef: sgt1930 prints 5 at 31 December 1929, sgt1929 printed 4; women_girls Sfax: sgt1930 prints 4 at 31 December 1929, sgt1929 printed 3; women_girls Sousse: sgt1930 prints 5 at 31 December 1929, sgt1929 printed 2; women_girls Tunis: sgt1930 prints 40 at 31 December 1929, sgt1929 printed 53; women_girls Totaux: sgt1930 prints 58 at 31 December 1929, sgt1929 printed 67.

Cells flagged `derived_from_totals`: sgt1939 movement_men / out_amnesty, 13 lines (column hidden under the fold of the binding (heading and figures; sgt1936 prints "par amnistie" at this place): each line's Total des sorties less its other printed exits (Béja 2, Bizerte 2, Sousse 18, Tunis 116, Djebel-Djougar 1, the other lines 0; 139 in all, the difference between the Totaux line's Total des sorties 19.724 and the sum of the printed column totals 19.585)).

Cells flagged `row_realigned` (stored on the line their content belongs to): sgt1922 Tunis / out_conditional: the 9 is printed on the line below (Pénitencier Agricole du Djebel-Djougar, whose label takes two lines); with it there neither line gives its printed Total des sorties, with it here both do; sgt1929 Tunis / out_died: the 97 is printed on the Sousse line (Sousse stored 0); with it there neither line gives its Total des sorties (1.454 for 1.357, 5.902 for 5.999), with it here both do.

## Validation

- Checks against printed totals and identities: 1682; passed: 1632; failed: 50.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.74 (f98) movement_men Totaux: out_total = out_sentence + out_pardon_amnesty + out_provisional + out_acquittal + out_conditional + out_administrative + tr_central + tr_other_prisons + tr_convict_depots + tr_hospitals + out_colons_controles + out_escaped + out_died + out_executed: cells give 14980, printed 14890 (difference -90)
  - sgt1922 p.74 (f98) movement_men tr_central: lines vs Totaux: cells give 605, printed 695 (difference 90)
  - sgt1923 p.80 (f582) movement_men Béja: in_total = in_free + in_other_prisons + re_escape + re_colons + re_hospital + re_provisional: cells give 251, printed 256 (difference 5)
  - sgt1923 p.80 (f582) movement_men re_provisional: lines vs Totaux: cells give 92, printed 97 (difference 5)
  - sgt1925 p.84 (f108) movement_men Sousse: end = start + in_total + -out_total: cells give 189, printed 183 (difference -6)
  - sgt1925 p.84 (f108) movement_men end: lines vs Totaux: cells give 3088, printed 3094 (difference 6)
  - sgt1928 p.94 (f646) movement_men Totaux: out_total = out_sentence + out_pardon + out_conditional + out_provisional + out_acquittal + out_administrative + tr_central + tr_correction + tr_convict_depots + tr_other_prisons + tr_work_sites + tr_various + out_escaped + out_died + out_executed: cells give 16365, printed 16065 (difference -300)
  - sgt1928 p.94 (f646) movement_men out_sentence: lines vs Totaux: cells give 7168, printed 7468 (difference 300)
  - sgt1929 p.96 (f124) movement_men Totaux: in_total = in_free + in_other_prisons + re_escape + re_conditional + re_provisional: cells give 22642, printed 13642 (difference -9000)
  - sgt1929 p.96 (f124) movement_men Kairouan: out_total = out_sentence + out_pardon + out_conditional + out_provisional + out_acquittal + out_administrative + tr_central + tr_correction + tr_convict_depots + tr_other_prisons + tr_work_sites + tr_various + out_escaped + out_died + out_executed: cells give 824, printed 866 (difference 42)
  - sgt1929 p.96 (f124) movement_men Le Kef: out_total = out_sentence + out_pardon + out_conditional + out_provisional + out_acquittal + out_administrative + tr_central + tr_correction + tr_convict_depots + tr_other_prisons + tr_work_sites + tr_various + out_escaped + out_died + out_executed: cells give 1102, printed 1120 (difference 18)
  - sgt1929 p.96 (f124) movement_men Totaux: out_total = out_sentence + out_pardon + out_conditional + out_provisional + out_acquittal + out_administrative + tr_central + tr_correction + tr_convict_depots + tr_other_prisons + tr_work_sites + tr_various + out_escaped + out_died + out_executed: cells give 14654, printed 14354 (difference -300)
  - sgt1929 p.96 (f124) movement_men Gabès: end = start + in_total + -out_total: cells give 67, printed 57 (difference -10)
  - sgt1929 p.96 (f124) movement_men in_free: lines vs Totaux: cells give 10325, printed 19325 (difference 9000)
  - sgt1929 p.96 (f124) movement_men out_sentence: lines vs Totaux: cells give 6159, printed 6459 (difference 300)
  - sgt1929 p.96 (f124) movement_men out_provisional: lines vs Totaux: cells give 960, printed 1020 (difference 60)
  - sgt1929 p.96 (f124) movement_men end: lines vs Totaux: cells give 1911, printed 1921 (difference 10)
  - sgt1929 p.96 (f124) movement_men detention_days: lines vs Totaux: cells give 927134, printed 927135 (difference 1)
  - sgt1935 p.66 (f86) movement_men Sfax: in_total = in_free + in_other_prisons + in_hospitals + re_escape + re_conditional + re_provisional: cells give 1569, printed 1669 (difference 100)
  - sgt1935 p.66 (f86) movement_men Sousse: out_total = out_sentence + out_pardon + out_conditional + out_provisional + out_acquittal + out_administrative + tr_alg_appellants + tr_alg_central + tr_alg_el_harrach + tr_tun_remand + tr_correction + tr_tun_bagnes + tr_work_sites + tr_various + out_escaped + out_died + out_executed: cells give 2082, printed 2084 (difference 2)
  - sgt1935 p.66 (f86) movement_men Tunis: out_total = out_sentence + out_pardon + out_conditional + out_provisional + out_acquittal + out_administrative + tr_alg_appellants + tr_alg_central + tr_alg_el_harrach + tr_tun_remand + tr_correction + tr_tun_bagnes + tr_work_sites + tr_various + out_escaped + out_died + out_executed: cells give 9152, printed 9170 (difference 18)
  - sgt1935 p.66 (f86) movement_men Le Bardo: out_total = out_sentence + out_pardon + out_conditional + out_provisional + out_acquittal + out_administrative + tr_alg_appellants + tr_alg_central + tr_alg_el_harrach + tr_tun_remand + tr_correction + tr_tun_bagnes + tr_work_sites + tr_various + out_escaped + out_died + out_executed: cells give 246, printed 249 (difference 3)
  - sgt1935 p.66 (f86) movement_men Porto-Farina: out_total = out_sentence + out_pardon + out_conditional + out_provisional + out_acquittal + out_administrative + tr_alg_appellants + tr_alg_central + tr_alg_el_harrach + tr_tun_remand + tr_correction + tr_tun_bagnes + tr_work_sites + tr_various + out_escaped + out_died + out_executed: cells give 169, printed 183 (difference 14)
  - sgt1935 p.66 (f86) movement_men Pénitencier Agricole du Djebel Djougar: out_total = out_sentence + out_pardon + out_conditional + out_provisional + out_acquittal + out_administrative + tr_alg_appellants + tr_alg_central + tr_alg_el_harrach + tr_tun_remand + tr_correction + tr_tun_bagnes + tr_work_sites + tr_various + out_escaped + out_died + out_executed: cells give 663, printed 671 (difference 8)
  - sgt1935 p.66 (f86) movement_men Détachements extérieurs: out_total = out_sentence + out_pardon + out_conditional + out_provisional + out_acquittal + out_administrative + tr_alg_appellants + tr_alg_central + tr_alg_el_harrach + tr_tun_remand + tr_correction + tr_tun_bagnes + tr_work_sites + tr_various + out_escaped + out_died + out_executed: cells give 648, printed 654 (difference 6)
  - sgt1935 p.66 (f86) movement_men Totaux: out_total = out_sentence + out_pardon + out_conditional + out_provisional + out_acquittal + out_administrative + tr_alg_appellants + tr_alg_central + tr_alg_el_harrach + tr_tun_remand + tr_correction + tr_tun_bagnes + tr_work_sites + tr_various + out_escaped + out_died + out_executed: cells give 21656, printed 19201 (difference -2455)
  - sgt1935 p.66 (f86) movement_men Sfax: end = start + in_total + -out_total: cells give 213, printed 113 (difference -100)
  - sgt1935 p.66 (f86) movement_men in_total: lines vs Totaux: cells give 19657, printed 19557 (difference -100)
  - sgt1935 p.66 (f86) movement_men tr_tun_bagnes: lines vs Totaux: cells give 51, printed 2557 (difference 2506)
  - sgt1935 p.66 (f86) movement_men detention_days: lines vs Totaux: cells give 1057661, printed 1077661 (difference 20000)
  - sgt1936 p.48 (f59) movement_men Tunis: out_total = out_sentence + out_pardon + out_conditional + out_amnesty + out_provisional + out_acquittal + out_administrative + tr_alg_appellants + tr_alg_central + tr_alg_convict_depot + tr_tun_remand + tr_correction + tr_tun_bagnes + tr_work_sites + tr_various + out_escaped + out_died + out_executed: cells give 9982, printed 9782 (difference -200)
  - sgt1936 p.48 (f59) movement_men tr_tun_remand: lines vs Totaux: cells give 3586, printed 3386 (difference -200)
  - sgt1939 p.48 (f54) movement_men detention_days: lines vs Totaux: cells give 1245734, printed 1267582 (difference 21848)
  - sgt1925 p.86 (f110) movement_women Sousse: out_total = out_sentence + out_pardon + out_provisional + out_conditional + out_acquittal + out_administrative + tr_central + tr_other_prisons + tr_convict_depots + tr_localities + tr_expelled_algeria + out_evacuated_hospitals + out_escaped + out_died + out_executed: cells give 31, printed 38 (difference 7)
  - sgt1925 p.86 (f110) movement_women out_provisional: lines vs Totaux: cells give 59, printed 66 (difference 7)
  - sgt1929 p.96 (f124) movement_women Gabès: in_total = in_free + in_other_prisons + re_escape + re_conditional + re_provisional: cells give 4, printed 10 (difference 6)
  - sgt1929 p.96 (f124) movement_women Gabès: end = start + in_total + -out_total: cells give 0, printed 2 (difference 2)
  - sgt1929 p.96 (f124) movement_women Gafsa: end = start + in_total + -out_total: cells give 0, printed 3 (difference 3)
  - sgt1929 p.96 (f124) movement_women Kairouan: end = start + in_total + -out_total: cells give 4, printed 0 (difference -4)
  - sgt1929 p.96 (f124) movement_women Le Kef: end = start + in_total + -out_total: cells give 5, printed 4 (difference -1)
  - sgt1929 p.96 (f124) movement_women Sfax: end = start + in_total + -out_total: cells give 4, printed 3 (difference -1)
  - sgt1929 p.96 (f124) movement_women Sousse: end = start + in_total + -out_total: cells give 5, printed 2 (difference -3)
  - sgt1929 p.96 (f124) movement_women Tunis: end = start + in_total + -out_total: cells give 40, printed 53 (difference 13)
  - sgt1929 p.96 (f124) movement_women Totaux: end = start + in_total + -out_total: cells give 58, printed 67 (difference 9)
  - sgt1929 p.96 (f124) movement_women in_free: lines vs Totaux: cells give 329, printed 335 (difference 6)
  - sgt1929 1929 end: men's + women's Totaux vs the récapitulation (sgt1929 p.99 (f127) recap): cells give 1988, printed 1979 (difference -9)
  - sgt1939 1939 detention_days: men's + women's Totaux vs the récapitulation (sgt1939 p.50 (f56) recap): cells give 1289430, printed 1267582 (difference -21848)
  - sgt1924 Porto-Farina: men's + women's days of detention vs table d) (sgt1924 p.83 (f1073) expenditure): cells give 133096, printed 133086 (difference -10)
  - sgt1929 Bizerte: men's + women's days of detention vs table d) (sgt1929 p.94 (f122) expenditure): cells give 7823, printed 7824 (difference 1)
  - sgt1935 Kairouan: men's + women's days of detention vs table d) (sgt1935 p.64 (f84) expenditure): cells give 15087, printed 35087 (difference 20000)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: derived_from_totals: 13, row_realigned: 2, total_mismatch: 17.

  - sgt1922 p.75 1922 men_boys / Tunis / exit / out_conditional = 9 (row_realigned)
  - sgt1923 p.80 1923 men_boys / Béja / entry / re_provisional = 0 (total_mismatch)
  - sgt1925 p.85 1925 men_boys / Sousse / stock / end = 183 (total_mismatch)
  - sgt1925 p.86 1925 women_girls / Sousse / exit / out_provisional = 0 (total_mismatch)
  - sgt1929 p.97 1929 men_boys / Bizerte / days / detention_days = 7657 (total_mismatch)
  - sgt1929 p.97 1929 men_boys / Gabès / stock / end = 57 (total_mismatch)
  - sgt1929 p.97 1929 men_boys / Kairouan / exit / out_provisional = 32 (total_mismatch)
  - sgt1929 p.97 1929 men_boys / Le Kef / exit / out_provisional = 0 (total_mismatch)
  - sgt1929 p.97 1929 men_boys / Tunis / exit / out_died = 97 (row_realigned)
  - sgt1929 p.96 1929 women_girls / Gabès / entry / in_free = 3 (total_mismatch)
  - sgt1929 p.97 1929 women_girls / Gabès / stock / end = 2 (total_mismatch)
  - sgt1929 p.97 1929 women_girls / Gafsa / stock / end = 3 (total_mismatch)
  - sgt1929 p.97 1929 women_girls / Kairouan / stock / end = 0 (total_mismatch)
  - sgt1929 p.97 1929 women_girls / Le Kef / stock / end = 4 (total_mismatch)
  - sgt1929 p.97 1929 women_girls / Sfax / stock / end = 3 (total_mismatch)
  - sgt1929 p.97 1929 women_girls / Sousse / stock / end = 2 (total_mismatch)
  - sgt1929 p.97 1929 women_girls / Tunis / stock / end = 53 (total_mismatch)
  - sgt1935 p.67 1935 men_boys / Kairouan / days / detention_days = 12986 (total_mismatch)
  - sgt1936 p.49 1936 men_boys / Tunis / exit / tr_tun_remand = 345 (total_mismatch)
  - sgt1939 p.48 1939 men_boys / Béja / exit / out_amnesty = 2 (derived_from_totals)
  - sgt1939 p.48 1939 men_boys / Bizerte / exit / out_amnesty = 2 (derived_from_totals)
  - sgt1939 p.48 1939 men_boys / Gabès / exit / out_amnesty = 0 (derived_from_totals)
  - sgt1939 p.48 1939 men_boys / Gafsa / exit / out_amnesty = 0 (derived_from_totals)
  - sgt1939 p.48 1939 men_boys / Kairouan / exit / out_amnesty = 0 (derived_from_totals)
  - sgt1939 p.48 1939 men_boys / Le Kef / exit / out_amnesty = 0 (derived_from_totals)
  - sgt1939 p.48 1939 men_boys / Sfax / exit / out_amnesty = 0 (derived_from_totals)
  - sgt1939 p.48 1939 men_boys / Sousse / exit / out_amnesty = 18 (derived_from_totals)
  - sgt1939 p.48 1939 men_boys / Tunis / exit / out_amnesty = 116 (derived_from_totals)
  - sgt1939 p.48 1939 men_boys / Le Bardo / exit / out_amnesty = 0 (derived_from_totals)
  - sgt1939 p.48 1939 men_boys / Porto-Farina / exit / out_amnesty = 0 (derived_from_totals)
  - sgt1939 p.48 1939 men_boys / Pénitencier agricole du Djebel-Djougar / exit / out_amnesty = 1 (derived_from_totals)
  - sgt1939 p.48 1939 men_boys / Détachements extérieurs / exit / out_amnesty = 0 (derived_from_totals)

## Image versus OCR

- Read cell by cell on the page images (24 printings): sgt1922 f98, sgt1923 f582, sgt1924 f1072, sgt1925 f108, sgt1926 f660, sgt1927 f122, sgt1928 f646, sgt1929 f124, sgt1930 f658, sgt1935 f86, sgt1936 f59, sgt1939 f54, sgt1922 f100, sgt1923 f584, sgt1924 f1074, sgt1925 f110, sgt1926 f660, sgt1927 f122, sgt1928 f646, sgt1929 f124, sgt1930 f658, sgt1935 f86, sgt1936 f59, sgt1939 f54.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
