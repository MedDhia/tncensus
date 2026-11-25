# Examens : répartition des candidats par nationalité

*Examinations: candidates examined and passed, by exam, nationality and sex.*

Source: *Statistique générale de la Tunisie*, chapter "Instruction publique et beaux-arts" (VII; VI in sgt1936 and sgt1939), editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1922 (`bpt6k9105649x`): p. 92, f116; sgt1923 (`bpt6k9105649x`): p. 98, f600; sgt1924 (`bpt6k9105649x`): p. 100, f1090; sgt1925 (`bpt6k9105650k`): p. 101, f125, p. 102, f126; sgt1926 (`bpt6k9105650k`): p. 111, f675, p. 112, f676; sgt1927 (`bpt6k91056510`): p. 109, f137, p. 110, f138; sgt1928 (`bpt6k91056510`): p. 109, f661, p. 110, f662; sgt1929 (`bpt6k9105652d`): p. 111, f139, p. 112, f140; sgt1930 (`bpt6k9105652d`): p. 115, f673, p. 116, f674; sgt1935 (`bpt6k9105653t`): p. 81, f101, p. 82, f102; sgt1936 (`bpt6k91056547`): p. 58, f70, p. 60, f71; sgt1939 (`bpt6k9105739w`): p. 61, f67, p. 62, f68.

Transcriptions: `../transcribed/education_sum_<edition>.txt`; rebuild with `python3 data-raw/yearbook_health_education/extract_education_summary.py build`. Per-check output: `education_summary_validation.json`.

Rows: 5400. Years: 1922–1939 (12 years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939).

Printed once per edition, for the edition's own year; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number; pages without a printed number are inferred from the next page. For the two-page spreads (population, primary-education and first-degree totals) the boys' block is given the left-hand page and the girls' block and total columns the right-hand page (the printed fold falls near the boys' TOTAUX, so one or two boys' columns may in fact sit on the right-hand page)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (31 December of that year for pupils; the school year's examinations)
- `exam`: English code of the examination
- `exam_fr`: examination as printed (with its group heading)
- `stage`: `examined` or `passed`
- `stage_fr`: as printed
- `sex`: `male`, `female`; `total` where the cell is not split by sex (empty in the comparative table for items that are not pupils)
- `sex_fr`: column heading as printed (Aspirants / Aspirantes in the examination table, Garçons / Filles elsewhere)
- `nationality`: `french`, `muslim`, `jewish`, `italian`, `maltese`, `other` (Divers); `total` where not split
- `nationality_fr`: column heading as printed (masculine for boys, feminine for girls)
- `value`: count (integer); printed » = 0; empty where the cell is not printed (`not_applicable`)
- `flag`: empty, or `ocr_corrected`, `derived_from_totals`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (TOTAUX, Totaux généraux, subtotals, A reporter) are not stored unless stated; they were used for validation.

Table b) "Examens ; répartition des candidats par nationalité": for each examination, candidates examined (`examined`) and passed (`passed`), aspirants (boys/men) and aspirantes (girls/women) by nationality. The TOTAUX per sex and the TOTAUX GÉNÉRAUX are not stored. The list of examinations changes between editions (codes): `cepe` CEPE; `brevet_elementaire`; `beps` (one line, sgt1922–sgt1926) and from sgt1927 its sections `beps_general`, `beps_commercial`, `beps_agricultural`, `beps_domestic` (ménagère), `beps_arts_crafts`, `beps_industrial`; `brevet_superieur`; `baccalaureat`; Arabic examinations `arabic_spoken_cert`, `arabic_brevet_elementaire`, `arabic_diplome_superieur`; teaching certificates `gymnastics_teaching_cert` (from sgt1935 "éducation physique": `physical_education_teaching_cert`) and `sewing_teaching_cert`; `sadiki_secondary_diploma`; École Émile-Loubet diploma and 3rd-year certificate; École Paul-Cambon certificates (commercial, industrial, manual work; 4th-year commercial exam in sgt1930; commerce-school diploma from sgt1935); girls' secondary certificates and diplomas (`girls_secondary_*`). An exam printed with all cells » is stored with zeros.

Failed checks (listed below): every cell was re-read on native-resolution crops and the printed figures are kept; the faulty cell or total cannot be identified, so no cell is flagged. Flagged cells: sgt1923 Baccalauréat passed, boys, Italiens is blank on the page and was solved from the TOTAUX (114) (`derived_from_totals`). sgt1936 CEPE examined, boys, Maltais: broken second digit, read as 44, which closes both totals (`ocr_corrected`). sgt1927 Section ménagère examined, girls: the TOTAUX cell is printed » although the cells and the TOTAUX GÉNÉRAUX give 4 (treated as not printed). sgt1936 Brevet supérieur passed, girls: TOTAUX printed "3" for 31.

## Validation

- Checks against printed totals: 1798; passed: 1772; failed: 26.

Failed checks (every cell involved was re-read on a native-resolution crop; the printed figures are as transcribed; see the commentary above):

  - sgt1922 baccalaureat examined boys: nationalities vs TOTAUX: cells give 280, printed 180
  - sgt1922 baccalaureat examined: boys TOTAUX + girls TOTAUX vs TOTAUX GÉNÉRAUX: cells give 234, printed 334
  - sgt1922 arabic_spoken_cert examined boys: nationalities vs TOTAUX: cells give 54, printed 51
  - sgt1922 arabic_spoken_cert examined: boys TOTAUX + girls TOTAUX vs TOTAUX GÉNÉRAUX: cells give 78, printed 81
  - sgt1922 arabic_brevet_elementaire examined boys: nationalities vs TOTAUX: cells give 102, printed 103
  - sgt1922 arabic_brevet_elementaire examined: all cells vs TOTAUX GÉNÉRAUX: cells give 104, printed 105
  - sgt1923 cepe passed boys: nationalities vs TOTAUX: cells give 838, printed 868
  - sgt1923 cepe passed: all cells vs TOTAUX GÉNÉRAUX: cells give 1333, printed 1363
  - sgt1923 arabic_spoken_cert examined girls: nationalities vs TOTAUX: cells give 26, printed 25
  - sgt1923 arabic_spoken_cert examined: all cells vs TOTAUX GÉNÉRAUX: cells give 105, printed 104
  - sgt1924 baccalaureat examined boys: nationalities vs TOTAUX: cells give 363, printed 359
  - sgt1924 baccalaureat examined: all cells vs TOTAUX GÉNÉRAUX: cells give 441, printed 437
  - sgt1927 cepe examined boys: nationalities vs TOTAUX: cells give 2242, printed 2342
  - sgt1927 cepe examined: all cells vs TOTAUX GÉNÉRAUX: cells give 3132, printed 3232
  - sgt1927 arabic_diplome_superieur examined: boys TOTAUX + girls TOTAUX vs TOTAUX GÉNÉRAUX: cells give 28, printed 29
  - sgt1927 arabic_diplome_superieur examined: all cells vs TOTAUX GÉNÉRAUX: cells give 28, printed 29
  - sgt1929 cepe examined boys: nationalities vs TOTAUX: cells give 2739, printed 2736
  - sgt1929 cepe examined: all cells vs TOTAUX GÉNÉRAUX: cells give 3623, printed 3620
  - sgt1929 sewing_teaching_cert passed girls: nationalities vs TOTAUX: cells give 41, printed 42
  - sgt1929 sewing_teaching_cert passed: all cells vs TOTAUX GÉNÉRAUX: cells give 41, printed 42
  - sgt1930 baccalaureat examined boys: nationalities vs TOTAUX: cells give 547, printed 549
  - sgt1930 baccalaureat examined: all cells vs TOTAUX GÉNÉRAUX: cells give 659, printed 661
  - sgt1930 arabic_spoken_cert examined boys: nationalities vs TOTAUX: cells give 56, printed 60
  - sgt1930 arabic_spoken_cert examined: all cells vs TOTAUX GÉNÉRAUX: cells give 99, printed 103
  - sgt1936 brevet_superieur passed girls: nationalities vs TOTAUX: cells give 31, printed 3
  - sgt1936 brevet_superieur passed: boys TOTAUX + girls TOTAUX vs TOTAUX GÉNÉRAUX: cells give 27, printed 55

- Flagged cells: derived_from_totals: 1, ocr_corrected: 1.

  - sgt1923 1923 baccalaureat / passed / male / italian = 3 (derived_from_totals)
  - sgt1936 1936 cepe / examined / male / maltese = 44 (ocr_corrected)
