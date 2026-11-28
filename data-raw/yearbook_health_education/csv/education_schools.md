# Écoles primaires publiques et écoles privées, école par école

*Public primary schools and private schools, school by school: classes, staff and pupils by sex and nationality (sgt1922, sgt1930).*

Source: *Statistique générale de la Tunisie*, chapter VII "Instruction publique et beaux-arts", "Enseignement primaire", a) Écoles primaires publiques, b) Écoles privées; editions sgt1922 (`bpt6k9105649x`, situation at 31 December 1922) and sgt1930 (`bpt6k9105652d`, 31 December 1930). Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views: sgt1922 public pp. 94–119, f118–f143, private pp. 120–123, f144–f147; sgt1930 public pp. 118–143, f676–f701, private pp. 144–147, f702–f705.

Transcriptions: `../transcribed/education_schools_<edition>.txt`; rebuild with `python3 data-raw/yearbook_health_education/extract_education_schools.py build`. Every check is listed in `education_schools_validation.json`.

Rows: 14960 (one per printed cell). Schools: sgt1922/public_schools 350; sgt1922/private_schools 32; sgt1930/public_schools 466; sgt1930/private_schools 31.

## Coverage

- **sgt1922, sgt1930**: the public primary schools (a) and the private schools (b) are printed school by school and are stored here. The other per-establishment lists of the chapter are already extracted elsewhere and are not repeated: the establishments with civil personality (`education_civil_personality_establishments.csv`) and the vocational schools (c) Enseignement professionnel des indigènes; `education_vocational.csv`). The "Total général de l'enseignement primaire" that follows the lists is `education_primary_totals.csv`.
- **sgt1939** (`bpt6k9105739w`, chapter VI, views 65–76) prints **no** school-by-school list of primary or private schools. Its chapter has: total pupils (f66), examinations (f67–68), libraries, Arabic courses, commerce and music schools (f69), the secondary / higher-primary / technical establishments one by one (f70–71, in `education_secondary_establishments_sgt1939.csv`), the first-degree total ("Établissements d'enseignement du premier degré", one line, f72–73, in `education_first_degree_sgt1939.csv`), vocational schools (f72, in `education_vocational.csv`), canteens (f73), the comparative population table (f74–75) and the quinquennial series (f76). No rows for sgt1939 are therefore stored here.

## Layout

Both editions print the same table: Localités | Désignation des établissements scolaires | Nombre de classes | Personnel (Maîtres pourvus de diplômes français, Maîtres arabes, Maîtres divers, Totaux) | Garçons (Français, Musulmans, Israélites, Italiens, Maltais, Divers, Totaux) | Filles (same, feminine) | Totaux généraux | Totaux généraux de l'année précédente, over two-page spreads with "A reporter" and "Report" lines, ending with "Totaux des écoles primaires publiques" / "Totaux des écoles privées". The public list carries the heading "(Circonscriptions d'inspection primaire : Bizerte, Sfax, Sousse, Tunis-Nord, Tunis-Est, Tunis-Ouest)" in sgt1922 and "(… : Bizerte, Le Kef, Sfax, Sousse, Tunis-Nord, Tunis-Est, Tunis-Ouest)" in sgt1930, but the schools are not grouped by district: Tunis comes first, then all other localities in one alphabetical sequence, with no district subtotals. No district can be read from the table, so `inspection_district` is empty (assigning districts would need an outside source). The private list is alphabetical by locality, Tunis first, with the subsidised Alliance Israélite schools last under their own heading. Printed totals (staff Totaux, pupils' Totaux, Totaux généraux, A reporter, Report, final totals) are not stored; they were used for the checks.

## Cell conventions and flags

- `derived_from_totals` (778 cells): the boys' Musulmans column is printed in the binding on most spreads (sgt1922 throughout; sgt1930 views 676–695 and the private list, partly; only the last digits or nothing are visible). Each such cell is solved as the boys' Totaux minus the other five nationalities. On the spreads where the column is legible (sgt1930 views 696–701, and some private rows) it was read and checked. One sgt1922 cell (Ghardimaou, previous-year total) is printed as two numbers, 81 for boys and 38 for girls, and stored as 119 with this flag. Derived cells were compared with the visible digit fragments where spot-checked, and their page sums agree with the printed Musulmans carry-overs where those are legible (sgt1930).
- `total_mismatch` (12 cells): a printed school cell that does not agree with its row total and its column total; the printed value is stored and the value the totals imply is used for the checks. Each was re-read on a native-resolution crop. They are listed below.
- `not_applicable` (39 cells): previous-year column printed "Création" (new school) or "Réouverture" (reopened), or left blank because a single previous-year total is printed in a bracket for two lines; in that case the bracketed figure is stored on the first line and covers both (sgt1922: Oued-Ellil Garçons + Filles = 58, Saïda Garçons + Filles = 101).
- Schools printed with » in every column are stored with 0 (sgt1922: Azib (El), Mixte (fermée); the La Manouba private secondary school for girls opened on 1 March 1923; the Bizerte Ecole Umberto Ier, see below).
- sgt1922 private schools: the printed "A reporter" of the first private spread exceeds its itemised rows by 7 classes, 8 Maîtres divers, 170 Italian boys and 108 Italian girls (278 pupils), and the final "Totaux des écoles privées" and the primary-education total count them; the only school with no figures is the Bizerte Ecole Umberto Ier (printed » throughout, 288 pupils the previous year), so the figures are apparently that school's, left out of its line. Because the printed total carries information not recoverable from the rows, the private total row of sgt1922 **is stored**, with `locality = "TOTAL (printed)"` and `school = "Totaux des écoles privées"` (SPEC rule): do not add it to the school rows.

## Columns

- `census`: edition (`sgt1922`, `sgt1930`)
- `table_id`: `public_schools` (a) Écoles primaires publiques) or `private_schools` (b) Écoles privées)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number. Each list is printed across two-page spreads: classes, staff and the boys' Français and Musulmans columns are given the left-hand page, the other pupil columns and the previous-year total the right-hand page
- `gallica_view`: Gallica view (fNNNN) of that page
- `year`: year of the edition; pupils and staff at 31 December of that year
- `school_sector`: `public` or `private`
- `inspection_district`: always empty: in sgt1922 and sgt1930 the public list is printed in one alphabetical sequence of localities (Tunis first) under a heading naming the inspection districts collectively, with no district per school or district subtotal (see below)
- `locality`: locality as printed (period spelling; the article in brackets as printed, e.g. `Ariana (L')`); `TOTAL (printed)` for the one stored total row (see below)
- `school`: designation as printed; a group word printed once for several lines (e.g. `Garçons :` followed by ditto dashes in Tunis) is repeated on every line it covers
- `school_group_fr`: printed group heading inside a table: `Ecoles de l'Alliance Israélite (subventionnées)` for the last private schools; empty otherwise
- `row_order`: order of the school within its table and edition (1, 2, …); identifies a school together with `census` and `table_id`
- `measure`: `classes` (Nombre de classes), `staff_french_diploma` (Maîtres pourvus de diplômes français), `staff_arabic` (Maîtres arabes), `staff_other` (Maîtres divers), `pupils` (Élèves), `pupils_total_previous_year` (Totaux généraux de l'année précédente: the school's total pupils a year earlier, printed only as a total)
- `measure_fr`: column heading as printed
- `sex`: `male` (Garçons), `female` (Filles) for pupils; `total` otherwise
- `sex_fr`: as printed
- `nationality`: `french`, `muslim`, `jewish`, `italian`, `maltese`, `other` (Divers) for pupils; `total` otherwise
- `nationality_fr`: column heading as printed (masculine for boys, feminine for girls)
- `value`: count (integer); printed » = 0; empty where a word is printed instead of a number (`not_applicable`)
- `flag`: empty, or `derived_from_totals`, `total_mismatch`, `not_applicable` (see below)

## Validation

- Checks against printed totals: 4190; passed: 4157; failed: 33. Kinds: row checks (staff, boys, girls, boys + girls = Totaux généraux) 2930; page column checks (printed Report + the page's rows = printed A reporter or final total, every column) 630; carry-over checks (each Report = the previous page's A reporter) 546; grand-total checks (all school rows of a table = its printed final total, every column) 84.
- Cells solved from row totals: 776 (their groups have no independent row check).

Failed checks. Every cell involved was re-read on a native-resolution crop (and against the Gallica OCR); the printed figures are kept:

  - sgt1922 primary_public l374 AREPORTER / A reporter: girls by column vs printed TOTAUX: cells give 13248, printed 13278. 4.210 printed; cells and the girls total 13.278 imply 4.240
  - sgt1922 primary_public l257 A reporter: previous-year total, printed Report + rows of the page vs printed: cells give 25577, printed 25571. previous-year total printed 25.571; the Report of this page plus its rows give 25.577 (rows re-read); the next page's Report repeats 25.571
  - sgt1922 primary_public l374 A reporter: girls italian, printed Report + rows of the page vs printed: cells give 4240, printed 4210. 4.210 printed; cells and the girls total 13.278 imply 4.240
  - sgt1922 primary_public l376 Report: Report girls italian vs previous page's A reporter: cells give 4240, printed 4210. this page's Report prints 4.240
  - sgt1922 primary_public l397 Totaux des écoles primaires publiques: previous-year total, sum of all school rows of the table vs printed total: cells give 36645, printed 36639. Musulmans in the binding, solved from the boys' total (13.280, as printed in the primary-education total). Previous-year total: the rows add to 36.645; the final total carries the 6 lost in the misprinted carry-over of view 133 (25.571 for 25.577)
  - sgt1922 primary_private l419 A reporter: classes, printed Report + rows of the page vs printed: cells give 83, printed 90. the printed carry-over exceeds the itemised rows by 7 classes, 8 other staff, 170 Italian boys and 108 Italian girls (278 pupils): apparently the Ecole Umberto Ier (Bizerte), printed as » throughout
  - sgt1922 primary_private l419 A reporter: staff other, printed Report + rows of the page vs printed: cells give 38, printed 46. the printed carry-over exceeds the itemised rows by 7 classes, 8 other staff, 170 Italian boys and 108 Italian girls (278 pupils): apparently the Ecole Umberto Ier (Bizerte), printed as » throughout
  - sgt1922 primary_private l419 A reporter: staff TOTAUX, printed Report + rows of the page vs printed: cells give 124, printed 132. the printed carry-over exceeds the itemised rows by 7 classes, 8 other staff, 170 Italian boys and 108 Italian girls (278 pupils): apparently the Ecole Umberto Ier (Bizerte), printed as » throughout
  - sgt1922 primary_private l419 A reporter: boys italian, printed Report + rows of the page vs printed: cells give 199, printed 369. the printed carry-over exceeds the itemised rows by 7 classes, 8 other staff, 170 Italian boys and 108 Italian girls (278 pupils): apparently the Ecole Umberto Ier (Bizerte), printed as » throughout
  - sgt1922 primary_private l419 A reporter: boys TOTAUX, printed Report + rows of the page vs printed: cells give 813, printed 983. the printed carry-over exceeds the itemised rows by 7 classes, 8 other staff, 170 Italian boys and 108 Italian girls (278 pupils): apparently the Ecole Umberto Ier (Bizerte), printed as » throughout
  - sgt1922 primary_private l419 A reporter: girls italian, printed Report + rows of the page vs printed: cells give 259, printed 367. the printed carry-over exceeds the itemised rows by 7 classes, 8 other staff, 170 Italian boys and 108 Italian girls (278 pupils): apparently the Ecole Umberto Ier (Bizerte), printed as » throughout
  - sgt1922 primary_private l419 A reporter: girls TOTAUX, printed Report + rows of the page vs printed: cells give 1615, printed 1723. the printed carry-over exceeds the itemised rows by 7 classes, 8 other staff, 170 Italian boys and 108 Italian girls (278 pupils): apparently the Ecole Umberto Ier (Bizerte), printed as » throughout
  - sgt1922 primary_private l419 A reporter: TOTAUX généraux, printed Report + rows of the page vs printed: cells give 2428, printed 2706. the printed carry-over exceeds the itemised rows by 7 classes, 8 other staff, 170 Italian boys and 108 Italian girls (278 pupils): apparently the Ecole Umberto Ier (Bizerte), printed as » throughout
  - sgt1922 primary_private l437 Totaux des écoles privées: classes, sum of all school rows of the table vs printed total: cells give 168, printed 175. stored (see notes): includes the 7 classes, 8 Maîtres divers, 170 Italian boys and 108 Italian girls of the first spread's carry-over that are not itemised (apparently the Ecole Umberto Ier, Bizerte); Musulmans in the binding, solved from the boys' total (37, as in the primary-education total)
  - sgt1922 primary_private l437 Totaux des écoles privées: staff other, sum of all school rows of the table vs printed total: cells give 56, printed 64. stored (see notes): includes the 7 classes, 8 Maîtres divers, 170 Italian boys and 108 Italian girls of the first spread's carry-over that are not itemised (apparently the Ecole Umberto Ier, Bizerte); Musulmans in the binding, solved from the boys' total (37, as in the primary-education total)
  - sgt1922 primary_private l437 Totaux des écoles privées: staff TOTAUX, sum of all school rows of the table vs printed total: cells give 222, printed 230. stored (see notes): includes the 7 classes, 8 Maîtres divers, 170 Italian boys and 108 Italian girls of the first spread's carry-over that are not itemised (apparently the Ecole Umberto Ier, Bizerte); Musulmans in the binding, solved from the boys' total (37, as in the primary-education total)
  - sgt1922 primary_private l437 Totaux des écoles privées: boys italian, sum of all school rows of the table vs printed total: cells give 390, printed 560. stored (see notes): includes the 7 classes, 8 Maîtres divers, 170 Italian boys and 108 Italian girls of the first spread's carry-over that are not itemised (apparently the Ecole Umberto Ier, Bizerte); Musulmans in the binding, solved from the boys' total (37, as in the primary-education total)
  - sgt1922 primary_private l437 Totaux des écoles privées: boys TOTAUX, sum of all school rows of the table vs printed total: cells give 3152, printed 3322. stored (see notes): includes the 7 classes, 8 Maîtres divers, 170 Italian boys and 108 Italian girls of the first spread's carry-over that are not itemised (apparently the Ecole Umberto Ier, Bizerte); Musulmans in the binding, solved from the boys' total (37, as in the primary-education total)
  - sgt1922 primary_private l437 Totaux des écoles privées: girls italian, sum of all school rows of the table vs printed total: cells give 426, printed 534. stored (see notes): includes the 7 classes, 8 Maîtres divers, 170 Italian boys and 108 Italian girls of the first spread's carry-over that are not itemised (apparently the Ecole Umberto Ier, Bizerte); Musulmans in the binding, solved from the boys' total (37, as in the primary-education total)
  - sgt1922 primary_private l437 Totaux des écoles privées: girls TOTAUX, sum of all school rows of the table vs printed total: cells give 3158, printed 3266. stored (see notes): includes the 7 classes, 8 Maîtres divers, 170 Italian boys and 108 Italian girls of the first spread's carry-over that are not itemised (apparently the Ecole Umberto Ier, Bizerte); Musulmans in the binding, solved from the boys' total (37, as in the primary-education total)
  - sgt1922 primary_private l437 Totaux des écoles privées: TOTAUX généraux, sum of all school rows of the table vs printed total: cells give 6310, printed 6588. stored (see notes): includes the 7 classes, 8 Maîtres divers, 170 Italian boys and 108 Italian girls of the first spread's carry-over that are not itemised (apparently the Ecole Umberto Ier, Bizerte); Musulmans in the binding, solved from the boys' total (37, as in the primary-education total)
  - sgt1930 primary_public l34 Tunis / Filles : Ecole Paul-Cambon: staff by column vs printed TOTAUX: cells give 35, printed 15. staff total printed 15; cells and column total give 35
  - sgt1930 primary_public l458 AREPORTER / A reporter: staff by column vs printed TOTAUX: cells give 1549, printed 1548. Maîtres divers printed 93; the rows give 92 and the next page's Report prints 92
  - sgt1930 primary_public l202 A reporter: classes, printed Report + rows of the page vs printed: cells give 661, printed 660. classes: the 36 printed rows of this page add to 97, the carry-over implies 96 (page re-read)
  - sgt1930 primary_public l361 A reporter: previous-year total, printed Report + rows of the page vs printed: cells give 42674, printed 42697. previous-year column of this page adds to 3.502 (re-read); the carry-over implies 3.525
  - sgt1930 primary_public l409 A reporter: classes, printed Report + rows of the page vs printed: cells give 1229, printed 1228. classes of this page add to 105 (re-read), carry-over implies 104
  - sgt1930 primary_public l458 A reporter: staff other, printed Report + rows of the page vs printed: cells give 92, printed 93. Maîtres divers printed 93; the rows give 92 and the next page's Report prints 92
  - sgt1930 primary_public l460 Report: Report staff other vs previous page's A reporter: cells give 92, printed 93. prints 92 Maîtres divers, correcting the 93 of the previous page's A reporter
  - sgt1930 primary_public l486 A reporter: previous-year total, printed Report + rows of the page vs printed: cells give 56730, printed 56816. previous-year column: the rows of this page add to 4.745 (all re-read; the OCR agrees), the carry-over 56.816 implies 4.831 (+86); the next page's Report also prints 56.816
  - sgt1930 primary_public l513 Totaux des écoles primaires publiques: classes, sum of all school rows of the table vs printed total: cells give 1567, printed 1565. Musulmans partly in the binding (29.9.8): the boys' total 45.138 gives 29.968. The rows add to 1.567 classes and 58.546 previous-year pupils: the final total carries the misprinted carry-overs (A reporter) of view 684 (classes 660 for 661), view 694 (classes 1.228 for 1.229), view 693 (previous year 42.697 for 42.674, +23) and view 699 (56.816 for 56.730, +86)
  - sgt1930 primary_public l513 Totaux des écoles primaires publiques: previous-year total, sum of all school rows of the table vs printed total: cells give 58546, printed 58655. Musulmans partly in the binding (29.9.8): the boys' total 45.138 gives 29.968. The rows add to 1.567 classes and 58.546 previous-year pupils: the final total carries the misprinted carry-overs (A reporter) of view 684 (classes 660 for 661), view 694 (classes 1.228 for 1.229), view 693 (previous year 42.697 for 42.674, +23) and view 699 (56.816 for 56.730, +86)
  - sgt1930 primary_private l552 Totaux des écoles privées: previous-year total, printed Report + rows of the page vs printed: cells give 7217, printed 7244. previous-year column: the rows of this page add to 3.708, the printed total 7.244 implies 3.735 (+27); all cells re-read, the OCR agrees
  - sgt1930 primary_private l552 Totaux des écoles privées: previous-year total, sum of all school rows of the table vs printed total: cells give 7217, printed 7244. previous-year column: the rows of this page add to 3.708, the printed total 7.244 implies 3.735 (+27); all cells re-read, the OCR agrees

Cells flagged `total_mismatch`:

  - sgt1922 public_schools Djebel-Abiod / Mixte: pupils female muslim printed 1
  - sgt1922 public_schools Sousse / Filles (école primaire supérieure), avenue Boucher: pupils female jewish printed 441
  - sgt1922 private_schools Redeyef / Ecole mixte de M. Combès: pupils female muslim printed 8
  - sgt1922 private_schools Tunis / Garçons : Rue Malta-Srira: pupils male italian printed 41
  - sgt1922 private_schools Tunis / Garçons : Rue du Tribunal: pupils female jewish printed 0
  - sgt1922 private_schools Tunis / Garçons : Rue du Tribunal: pupils female italian printed 70
  - sgt1930 public_schools Djerissa / Filles: pupils female other printed 2
  - sgt1930 public_schools Hadjeb-el-Aïoun / Mixte: pupils male italian printed 4
  - sgt1930 public_schools Masdour / Garçons (franco-arabe): pupils male italian printed 1
  - sgt1930 public_schools Masdour / Garçons (franco-arabe): pupils female italian printed 1
  - sgt1930 private_schools Ferryville / Ecole de la Société Nord-Africaine (sœurs du Sacré-Cœur de Marie): pupils male muslim printed 4
  - sgt1930 private_schools Tunis / Garçons : Rue Malta-Srira: pupils male maltese printed 3

## Cross-check with the summary tables

The school rows of each list were summed by sex and nationality and compared, cell by cell, with the same edition's "Total général de l'enseignement primaire" (`education_primary_totals.csv`, rows `public_primary`, `private`) and comparative school-population table (`education_school_population.csv`, same rows). The list's own printed final total is compared too.

- 104 comparisons (2 editions x 2 sectors x 13 cells: 12 sex x nationality cells and the previous-year total, against each of the 2 tables). Summed printed school cells equal to the other table: 75; different: 29. Summed with the values the totals imply for the `total_mismatch` cells: equal 93, different 11. The list's own printed final total equals the other table in 103 of 104.

Differences (schools summed as printed / as implied by the totals / the list's printed total / the other table):

  - sgt1922 public girls muslim vs `education_primary_totals`: 1561 / 1560 / 1560 / 1560
  - sgt1922 public girls muslim vs `education_school_population`: 1561 / 1560 / 1560 / 1560
  - sgt1922 public girls jewish vs `education_primary_totals`: 3746 / 3446 / 3446 / 3446
  - sgt1922 public girls jewish vs `education_school_population`: 3746 / 3446 / 3446 / 3446
  - sgt1922 public previous-year total vs `education_primary_totals`: 36645 / 36645 / 36639 / 36639
  - sgt1922 public previous-year total vs `education_school_population`: 36645 / 36645 / 36639 / 36639
  - sgt1922 private boys italian vs `education_primary_totals`: 420 / 390 / 560 / 560
  - sgt1922 private boys italian vs `education_school_population`: 420 / 390 / 560 / 560
  - sgt1922 private girls muslim vs `education_primary_totals`: 466 / 458 / 458 / 458
  - sgt1922 private girls muslim vs `education_school_population`: 466 / 458 / 458 / 458
  - sgt1922 private girls jewish vs `education_primary_totals`: 1286 / 1356 / 1356 / 1356
  - sgt1922 private girls jewish vs `education_school_population`: 1286 / 1356 / 1356 / 1356
  - sgt1922 private girls italian vs `education_primary_totals`: 496 / 426 / 534 / 534
  - sgt1922 private girls italian vs `education_school_population`: 496 / 426 / 534 / 534
  - sgt1930 public boys french vs `education_primary_totals`: 6676 / 6676 / 6676 / 6667
  - sgt1930 public boys italian vs `education_primary_totals`: 4185 / 4183 / 4183 / 4183
  - sgt1930 public boys italian vs `education_school_population`: 4185 / 4183 / 4183 / 4183
  - sgt1930 public girls italian vs `education_primary_totals`: 3965 / 3964 / 3964 / 3964
  - sgt1930 public girls italian vs `education_school_population`: 3965 / 3964 / 3964 / 3964
  - sgt1930 public girls other vs `education_primary_totals`: 131 / 129 / 129 / 129
  - sgt1930 public girls other vs `education_school_population`: 131 / 129 / 129 / 129
  - sgt1930 public previous-year total vs `education_primary_totals`: 58546 / 58546 / 58655 / 58655
  - sgt1930 public previous-year total vs `education_school_population`: 58546 / 58546 / 58655 / 58655
  - sgt1930 private boys muslim vs `education_primary_totals`: 88 / 85 / 85 / 85
  - sgt1930 private boys muslim vs `education_school_population`: 88 / 85 / 85 / 85
  - sgt1930 private boys maltese vs `education_primary_totals`: 42 / 39 / 39 / 39
  - sgt1930 private boys maltese vs `education_school_population`: 42 / 39 / 39 / 39
  - sgt1930 private previous-year total vs `education_primary_totals`: 7217 / 7217 / 7244 / 7244
  - sgt1930 private previous-year total vs `education_school_population`: 7217 / 7217 / 7244 / 7244

Explanation: (i) the `total_mismatch` school cells are stored as printed, so the printed sums differ from the totals by exactly those misprints (they agree once the implied values are used); (ii) sgt1922 private: the 278 pupils (170 Italian boys, 108 Italian girls) counted in the printed totals but not itemised (see above); (iii) previous-year totals: the printed carry-overs are misprinted (sgt1922 public −6; sgt1930 public +23 and +86, private +27), the summary tables copy the lists' printed final totals; (iv) sgt1930 public boys' Français: lists and population table 6.676, the primary-education total prints 6.667 (a misprint already flagged in `education_primary_totals.csv`). No other difference: every other sex x nationality cell of the summed schools agrees with both summary tables.

## Schools that changed between 1922 and 1930

Compared by locality (normalised spelling) and designation; no linking is attempted. sgt1939 prints no list. Numbers of schools: public: 350 (1922) → 466 (1930), localities 206 → 279; private: 32 (1922) → 31 (1930), localities 16 → 16.

**public**: localities only in 1922: Ben-Arous, Deggache (El-Oudiane), Fedjet Khemaken, Hamma (El), Hamaïm, Kef-Chambi, Kanguet-el-Hadjaj, Ksar-el-Ahmar, Maareth, Rebiba, Sahaline, Sers, Zeramdine. Only in 1930: Aïn-Rhellal, Aouareb (El), Aouïna (El), Attar, Bembla, Ben-Arous (Fochville), Beni-Hassen, Bir-bou-Rekba, Bir-Chaaba, Bir-Touil, Bordj-Frendj, Bou-Merdès, Camp-Servière, De Carnières, Chahal, Deggache, Djebel-Mdilla, Cédouikech (Djerba), Cédriane (Djerba), Oued-Zebib (Djerba), Mélita (Djerba), Douaria, Douz, Dra ben Djouder, El-Alem, Ellès, Fedjet-Khemakhem, Fondouk-Hafaïed, Gamart, Ghenouche, Ghomrassen, Guétar (El), Hamma (El) du Djerid, Hamma (El) de Gabès, Hammaïm, Hammam-Sousse, Hergla, Hiboun, Jama, Kasserine, Ouled-bou Ali (Kerkenna), Kesra (La), Khanguet-el-Hadjaj, Korbous, Kouba-Kebira, Krib (Le), Ksar-Lahmar, Ksiba-Sousse, La Hencha, Lamta, Mareth, Marquez-Kamoun, Masdour, Menzel-Kamel, Merira-centre, Métameur, Nebeur, Ousseltia, Raf-Raf, Rebiba, gare, Rebiba, mine, Redjich, Rohia, Saheline, Saint-Henri, Sakiet-Ed-Daïr, Sakiet-Ez-Zit, Salammbô, Sekarna, Sers-gare, Sers-village, Sidi-Abbès, Sidi-Alouane, Sidi-Ameur, Sidi-Assaker, Sidi-bou-Ali, Sidi-bou-Aouane, Sidi-Freidj, Sidi-Naceur-Allah, Sidi-Zehili, Somaâ, Toukabeur, Touireuf, Triaga, Zarat, Zéramdine.

Localities in both editions whose public schools changed (designations printed only in 1922 → only in 1930; designations printed identically in both are not repeated):

- Tunis: Garçons : Rue Ayed (Bab-Djedid); Garçons : Rue du Pacha (int. d'app.); Garçons : Rue de Tripoli; Filles : Rue Chaker; Filles : Rue de Patras; Mixte : Quartier de Franceville; Mixte : Quartier de Mutuelleville → Garçons : Avenue Bab-Djedid; Garçons : Rue Dar-el Djeld; Garçons : Quartier de Franceville; Garçons : Rue du Pacha (cours complém. d'enseignement professionnel); Garçons : Rue Sidi-Ali-Azouz; Maternelle : Rue de Tripoli; Filles : Impasse Mousmar-el-Kassah; Mixte : Rue de Patras (enfantine); Quartier de Franceville; Quartier de Mutuelleville
- Aïn-Draham: Garçons (Internat de); Filles (Internat de) → Mixte (Internat); Garçons : franco-arabe (Internat)
- Aïn-el-Asker: Garçons → Mixte
- Aroussa (El): (none) → Filles
- Azib (El): Mixte (fermée) → Mixte
- Béja: Garçons (Internat de) → Garçons (Internat de) avec cours compl.; Filles musulmanes
- Beni-Khalled: Mixte → Franco-arabe
- Bir-Halima: Mixte → Garçons; Filles
- Birine: Mixte → Garçons; Filles
- Bizerte: Enfantine : mixte → Enfantine; Maternelle; Filles musulmanes
- Bou-Arada: Mixte → Garçons; Filles
- Chebaou: Mixte → Garçons; Filles
- Crétéville: Garçons, Filles : Mixte → Mixte
- Djedeïda: (none) → Orphelinat
- Djemmal: Filles → (none)
- Djerissa: Garçons, Filles : Mixte → Garçons; Filles
- Djouggar: (none) → Pénitencier
- Dubosville: Garçons coéducation; Filles coéducation → Garçons; Filles
- Ebba-Ksour: Mixte → Garçons; Filles
- Enfidaville: Filles, Garçons : Mixte → Garçons; Filles
- Ferryville: Garçons; Ecole des apprentis de l'Arsenal → Garçons, avec cours complémentaire mixte; Garçons (franco-arabe)
- Gabès: Filles; Garçons (section agricole) → Filles, avec cours complémentaire mixte
- Gafour: (none) → Filles musulmanes
- Gafsa (gare): Mixte → Garçons; Filles
- Ghardimaou: Garçons, Filles : coéducation → Garçons; Garçons (franco-arabe); Filles
- Kalaat-Senam (Mine): Mixte → Garçons; Filles
- Kalaâ-Kebira: Garçons → Garçons (franco arabe)
- Kebili: Mixte → Garçons
- Kef (Le): Garçons (internat) avec cours complémentaire mixte; Filles → Garçons (internat) avec cours complémentaire; Filles, avec cours complémentaire
- Khanguet-gare: Mixte → Garçons; Filles
- Kram: (none) → Institut héliothérapique
- Ksour: Mixte → Franco-arabe
- La Laverie (Djebel-Reças): Mixte → Garçons; Filles
- Maharès: Mixte → Garçons; Filles musulmanes
- Mahdia: (none) → Garçons (franco-arabe) avec cours compl.
- Mateur: Garçons; Enfantine → Garçons avec cours complémentaire mixte
- Maxula-Radès: Filles (Internat de) → Filles (Ecole Primaire Supérieure)
- Meheri-Zebbeus: Mixte (coéducation) → Mixte
- Menzel-Abdarrahmane: Garçons → Garçons (franco-arabe)
- Merira: Mixte → Garçons; Filles
- Methouia: Garçons → Garçons (franco-arabe)
- Metlaoui-Mine: Garçons → Garçons (franco-arabe)
- Metline: Garçons → Garçons (franco-arabe)
- Nabeul: (none) → Garçons (franco-arabe)
- Oued-Meliz: Mixte → Garçons
- Ras-el-Djebel: (none) → Filles musulmanes
- Reyville: Mixte (coéducation) → Garçons; Filles
- Saïda: Garçons : coéducation; Filles : coéducation → Garçons; Filles
- Saint-Germain: Mixte → Garçons; Filles; Enfantine
- Sakiet-Mine: Mixte → Coéducation : Garçons; Coéducation : Filles
- Sbeïtla: Mixte → Garçons; Filles
- Sebbala-du-Mornag: Mixte → Garçons; Filles
- Sfax: Garçons (école primaire élémentaire); Filles (école primaire élémentaire); Enfantine. — Mixte; Moulinville. — Mixte → Garçons (rue Alexandre Dumas); Filles (rue Massicault); Filles musulmanes; Moulinville. — Garçons; Moulinville. — Franco-arabe; Moulinville. — Filles
- Sousse: Garçons (école primaire supérieure); Filles musulmanes → Collège de garçons; Ecole Industrielle et Commerciale; Garçons, route de Monastir; Filles, rue Léon Mougeot; Filles musulmanes, rue El-Marr; Filles musulmanes, rue Laroussi Zarrouk; Filles musulmanes, rue Souk-el-Caïd
- Tabarca: Garçons → Garçons, avec cours complémentaire mixte
- Tebourba: Filles mixte → (none)
- Thala: Garçons; Filles → Garçons (franco-arabe); Mixte
- Tindja: (none) → Garçons (franco-arabe)
- Tozeur: (none) → Filles musulmanes
- Zaghouan: Garçons (avec internat) → Garçons (avec internat et cours complémentaire)

**private**: localities only in 1922: Seillonville. Only in 1930: Sillonville.

Localities in both editions whose private schools changed (designations printed only in 1922 → only in 1930; designations printed identically in both are not repeated):

- Tunis: Ecole Mixte de Mme Bonhomme → Ecole Jeanne d'Arc
- Aïn-Moularès: Ecole de M. Carrière → Ecole de M. Merlet
- Bizerte: Ecole de Mme Médeville → Ecole de Mme Médevielle
- Le Kef: Ecole de Mlle Lo Vecchio → Ecole Dante Alighieri
- La Manouba: Ecole privée d'enseignement secondaire de jeunes filles (ouverte le 1er mars 1923) → Collège de « Notre-Dame de Carthage »
- Mehdia: Ecole de Mme Costa → Ecole Francesco Valenza
- Redeyef: Ecole mixte de M. Combès → Ecole mixte
- St-Joseph-de-Thibar: Ecole de filles → Ecole Mixte
- Sfax: Filles → (none)

Obvious correspondences (spelling or split of a locality, not linked in the data): Ben-Arous → Ben-Arous (Fochville); Deggache (El-Oudiane) → Deggache; Fedjet Khemaken → Fedjet-Khemakhem; Hamaïm → Hammaïm; Kanguet-el-Hadjaj → Khanguet-el-Hadjaj; Ksar-el-Ahmar → Ksar-Lahmar; Maareth → Mareth; Sahaline → Saheline; Zeramdine → Zéramdine; Sers → Sers-gare and Sers-village; Rebiba → Rebiba, gare and Rebiba, mine; Hamma (El) → Hamma (El) de Gabès (and a new Hamma (El) du Djerid); private: Seillonville → Sillonville, Bizerte Ecole de Mme Médeville → Médevielle. Kef-Chambi (1922, printed "Mixte (fermé)" with no pupils) is not printed in 1930. Many 1922 "Mixte" schools appear in 1930 as separate Garçons and Filles schools, and many Garçons schools are relabelled "(franco-arabe)". Every spelling is as printed in its edition.
