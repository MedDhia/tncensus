# Statistique générale de la Tunisie: the remaining chapters

The 12 editions of `data-raw/yearbook_demography/EDITIONS.md` (codes `sgt1922` …
`sgt1939`, same volume arks, same rules for page images, OCR and
native-resolution crops). Chapters I (Démographie), III (health) and public
instruction are already done; this folder covers all the others. Chapter
*numbers* change between editions, so chapters are listed by topic.

Ranges were found from the chapter headings: start = first view of the chapter,
end = the view before the next chapter. Ranges marked `?` were not detected
automatically and must be confirmed. **Always confirm the first and last view
of a range on the page before relying on it.**

| Topic (prefix) | 1922 | 1923 | 1924 | 1925 | 1926 | 1927 | 1928 | 1929 | 1930 | 1935 | 1936 | 1939 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Communes (`communes_`) | 49–64 | 527–546 | 1015–1034 | 47–68 | 595–616 | 59–80 | 583–604 | 59–82 | 589–614 | 41–56 | 28–39 | 23–34 |
| Justice (`justice_`) | 85–94 | 569–578 | 1059–1068 | 93–104 | 643–654 | 105–116 | 629–640 | 107–118 | 641–652 | 71–80 | 52–61 | 47–56 |
| Prisons (`prisons_`) | 95–102 | 579–586 | 1069–1076 | 105–112 | 655–664 | 117–126 | 641–650 | 119–128 | 653–662 | 81–90 | ? | ? |
| Property / Tribunal mixte / Propriété foncière (`property_`) | 103–112 | 587–596 | 1077–1086 | 113–122 | 665–672 | 127–134 | 651–658 | 129–136 | 663–670 | 91–98 | 62–67? | 57–64 |
| Posts, telegraphs, telephones (`posts_`) | 153–172 | 637–662 | 1127–1158 | 163–198 | 713–754 | 175–216 | 699–740 | 177–218 | 711–752 | 109–116 | 78–83 | 77–82 |
| Public works (`publicworks_`) | 173–184 | 663–674 | 1159–1170 | 199–210 | 755–766 | 217–228 | 741–752 | 219–230 | 753–764 | 117–126 | 84–93 | 83–92 |
| Finances (`finance_`) | 185–230 | 675–720 | 1171–1216 | 211–286 | 767–802 | 229–258 | 753–782 | 231–260 | 765–794 | 127–138 | 94–99 | 93–98 |
| Agriculture (`agriculture_`) | 231–280 | 721–770 | 1217–1274 | 287–342 | 803–852 | 259–314 | 783–842 | 261–320 | 795–856 | 139–154 | 100–115 | 99–114 |
| Teaching and research institutions (`research_`) | – | – | – | – | – | – | – | – | – | 155–184 | 116–145 | 115–122 |
| Commerce and navigation (`commerce_`) | 281–436 | 771–926 | 1275–1430 | 343–498 | 853–1008 | 315–470 | 843–998 | 321–476 | 857–1012 | 185–290 | 146–171 | 123–150 |
| Colonisation (`colonisation_`) | 437–456 | 927–946 | 1431–1444 | 499–512 | 1009–1024 | 471–488 | 999–1016 | 477–492 | 1013–1028 | 291–306 | 172–181 | 151–156 |
| Economic institutions / mutual credit (`mutuality_`) | 457–466 | 947–956 | 1445–1454 | 518–523 | 1025–1036 | 489–500 | 1017–1030 | 493–508 | 1029–1044 | 307–318 | 182–187 | 157–162 |
| Labour and social welfare (`labour_`) | – | – | – | 513–524 | 1037–1044 | 501–510 | 1031–1040 | 509–518 | 1045–1054 | 319–328 | 188–197 | 163–175 |

Notes:
- sgt1936 renumbers its chapters (II Communes, III Hygiène, IV Justice, V Propriété foncière, VI Instruction, VII Postes, …), and the automatic detection was noisy there.
- Up to sgt1924, the economic and social institutions (XIV) include labour; from sgt1925 there is a separate "Travail et prévoyance sociale" chapter.
- Volume ends: sgt1924 ends at view 1471, sgt1926 at 1061, sgt1930 at 1071, sgt1935 at 340, sgt1936 at 212, sgt1939 at 190.

## Work plan (one agent at a time)

| Step | Scope |
|---|---|
| 1 | Communes: **done** (`extract_communes.py`, all tables, surveyed page by page) |
| 2 | Justice: **done** (`extract_justice.py`; hearing-schedule text pages not transcribed). Prisons: **done** (`extract_prisons.py`, 9 tables, survey in `csv/prisons_survey.md`). Property: **done** (`extract_property.py`, 13 tables, survey in `csv/property_survey.md`) |
| 3 | Posts: **done** (`extract_posts.py`, 6 tables, survey in `csv/posts_survey.md`; exchange-rate pages to do). Public works: **done** (`extract_publicworks.py`, 12 tables, survey in `csv/publicworks_survey.md`) |
| 4 | Finances: budget, public debt, patente, taxe personnelle and livestock tax **done** (`extract_finance.py`); achour **done** (`extract_finance_achour.py`); canoun **done** (`extract_finance_canoun.py`). Finances complete (views in `csv/finance_survey.md`) |
| 5 | Agriculture: land, crops, cereal zones **done** (`extract_agriculture.py`); tax-class tables, vines, olives, dates, livestock, forests to do (views in `csv/agriculture_survey.md`); the 1922–1930 meteorology and école coloniale / botanique / laboratory pages go to `research_` |
| 6 | Colonisation: **done** (`extract_colonisation.py`, 16 tables). Economic institutions: credit and central cooperative **done** (`extract_mutuality.py`; sgt1925 tables are at f518–523 inside the labour chapter); insurance, provident societies, Office de crédit indigène, bank balance sheets, early labour tables (sgt1922–1924) to do. Labour: **done** (`extract_labour.py`, 11 tables plus the text-only `labour_collective_agreements`). Research institutions: in progress |
| 7–10 | Commerce and navigation, by edition groups (1922–24, 1925–27, 1928–30, 1935–39) |

Output: `csv/<prefix><topic>.csv` with notes `.md` files; transcriptions in
`transcribed/`; one script per step, `extract_<step>.py` (`build`/`check`).
Follow `data-raw/colonial_census/SPEC.md` and
`data-raw/yearbook_demography/SPEC_ADDENDUM.md`, and model the code on
`data-raw/yearbook_health_education/extract_health_population.py`.
