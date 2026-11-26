# Prisons chapter: survey of every edition

Page-by-page survey of the *Établissements pénitentiaires* tables (chapter V up to sgt1935; printed at the end of chapter IV *Justice* in sgt1936 and sgt1939). Views confirmed on the images. Extraction: `extract_prisons.py`.

| edition | ark | views |
|---|---|---|
| sgt1922 | `bpt6k9105649x` | 95–102 |
| sgt1923 | `bpt6k9105649x` | 579–586 |
| sgt1924 | `bpt6k9105649x` | 1069–1076 |
| sgt1925 | `bpt6k9105650k` | 105–112 |
| sgt1926 | `bpt6k9105650k` | 655–664 |
| sgt1927 | `bpt6k91056510` | 117–126 |
| sgt1928 | `bpt6k91056510` | 641–650 |
| sgt1929 | `bpt6k9105652d` | 119–128 |
| sgt1930 | `bpt6k9105652d` | 653–662 |
| sgt1935 | `bpt6k9105653t` | 81–90 |
| sgt1936 | `bpt6k91056547` | 58–61 |
| sgt1939 | `bpt6k9105739w` | 53–56 |

## Tables per edition

- **sgt1922**: f95 chapter title; f96 blank; f97 Administration a) répartition des condamnés d'après la nationalité, l'âge, le sexe et la catégorie pénale, b) d'après la nationalité, la nature du délit et la catégorie pénale; f98 c) journées de travail des détenus (by establishment and kind of work), then Mouvement de la population a) mouvement général d'entrée et de sortie, effectif au 31 décembre (men and boys; spread f98-f99, lower halves); f99 d) tableau comparatif des dépenses et des journées de détention (by prison; personnel, upkeep, food, price of the day of detention, products of the work) with its footnote (1); f100-f101 b) mouvement général (women, upper halves of the spread); f100 c) Prison de Tunis : transfèrements; f101 d) état numérique des décès par prison et par maladie; f102 e) état comparatif du personnel de garde avec l'effectif journalier maximum (footnote (1)), f) récapitulation 1913-1922. f103 = chapter VI Propriété immobilière.
- **sgt1923**: f579 title; f580 blank; f581 a), b); f582 c), mouvement a) (men, spread f582-f583); f583 d) with footnote (1); f584-f585 b) (women); f584 c) transfèrements; f585 d) décès; f586 e) personnel de garde, f) récapitulation 1914-1923. f587 = chapter VI.
- **sgt1924**: f1069 title; f1070 blank; f1071 a), b); f1072 c), mouvement a) (men, spread f1072-f1073); f1073 d) with footnote (1); f1074-f1075 b) (women; f1075 printed sideways); f1074 c) transfèrements; f1075 d) décès (sideways); f1076 e) personnel de garde, f) récapitulation 1915-1924. f1077 = chapter VI.
- **sgt1925**: f105 title; f106 blank; f107 a), b); f108 c) journées de travail, e) mouvement général (men, spread f108-f109); f109 d) dépenses with footnote (1); f110-f111 f) mouvement général (women); f110 g) Prison de Tunis : transfèrements; f111 h) décès par prison et par maladie; f112 i) personnel de garde, j) récapitulation 1924-1925. f113 = chapter VI.
- **sgt1926**: f655 title; f656 blank; f657 a), b); f658-f659 c) journées de travail, d) dépenses (spread); f660-f661 e), f) mouvement général (spread, men above, women below); f662 g) service des transfèrements, h) décès; f663 i) personnel de garde (Totaux line empty), j) récapitulation 1925-1926; f664 blank. f665 = chapter VI.
- **sgt1927**: f117 title; f118 blank; f119 a), b); f120-f121 c), d) (with totaux généraux dépenses et recettes); f122-f123 e), f); f124 g), h); f125 i), j) 1926-1927; f126 blank. f127 = chapter VI.
- **sgt1928**: f641 title; f642 blank; f643 a), b); f644-f645 c), d); f646-f647 e), f); f648 g), h); f649 i), j) 1927-1928; f650 blank. f651 = chapter VI.
- **sgt1929**: f119 title; f120 blank; f121 a), b); f122-f123 c), d); f124-f125 e), f) (the two halves of f125 carry each other's headings); f126 g), h); f127 i), j) 1928-1929; f128 blank. f129 = chapter VI.
- **sgt1930**: f653 title; f654 blank; f655 a), b); f656-f657 c), d); f658-f659 e), f) mouvement général (men, women); f660 g), h); f661 i), j) 1929-1930; f662 blank. f663 = chapter VI.
- **sgt1935**: f81 title; f82 blank; f83 a), b); f84-f85 c) journées de travail (upper half) and d) dépenses (lower half) on one spread; f86-f87 e), f); f88 g), h); f89 i), j) 1933-1935; f90 blank. f91 = chapter VI Tribunal mixte.
- **sgt1936**: inside chapter IV (Justice), after its section VII (f56-f57): f58 répartition des condamnés d'après la nationalité, l'âge, le sexe; d'après la nationalité et la nature du délit; f59-f60 mouvement général d'entrée et de sortie (men above, women below, one spread); f61 récapitulation du chiffre des détenus 1932-1936. f62 = chapter V Propriété foncière.
- **sgt1939**: inside chapter IV (Justice), after its section VII (f51-f52): f53 répartition par nationalité, âge, sexe; par nationalité et nature du délit; f54-f55 mouvement général d'entrée et de sortie (men, women; the right page folded over the binding hides one men's exit column); f56 récapitulation 1935-1939. f57 = chapter V Propriété foncière.

## Coverage

Every table of the chapter is transcribed, in every edition that prints it: the récapitulation (prisons_population_recap), condemned prisoners by nationality, age, sex and penal category (prisons_condemned_nationality_age), by nationality, offence and sentence (prisons_condemned_offence), c) days of work (prisons_work_days, sgt1922-sgt1935), d) expenditure and days of detention (prisons_expenditure, sgt1922-sgt1935), the two mouvement général tables (prisons_movement, sgt1922-sgt1939), transfers (prisons_transfers, sgt1922-sgt1935), deaths by prison and disease (prisons_deaths, sgt1922-sgt1935) and guard staff against the maximum daily population (prisons_guard_staff, sgt1922-sgt1935). The page-by-page re-survey of every view listed above (contact sheets of every view from the chapter title to the next chapter, each table then read on native-resolution crops) found one table the first survey had missed, sgt1935 c) journées de travail (f84-f85, now in prisons_work_days), and nothing else: the remaining views are titles, blank pages and the next chapter. Footnotes are kept in the notes files (expenditure and guard-staff footnotes (1) are also stored as cells).

