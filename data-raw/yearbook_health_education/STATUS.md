# Status: work in progress (not in the package)

The extraction of the health and public-instruction chapters was stopped
partway. Nothing here is listed in `data-raw/colonial_census/tables.csv`, so
none of it is built into `inst/extdata/colonial` or loaded by
`load_colonial_census()`. Nothing has been validated against the printed
totals yet.

| Part | Transcribed (`transcribed/`) | Script | Validated |
|---|---|---|---|
| Health: budgets and institutes | `health_finance_*`: 1922-1930, 1935 (10 of 12 editions) | none yet | no |
| Health: hospitals and Tunis mortality | `health_pop_*`: all 12 editions | `extract_health_population.py` (draft) | no |
| Instruction: summary tables | `education_sum_*`: 1922-1927 (6 of 12) | `extract_education_summary.py` (draft) | no |
| Instruction: school lists | `education_schools_*`: 1922; 1930 in progress; 1939 not started | `extract_education_schools.py` (draft); `csv/education_schools.csv` is a draft | no |

To finish: complete the transcriptions, run each script, check every printed
total (see `data-raw/colonial_census/SPEC.md` and
`data-raw/yearbook_demography/SPEC_ADDENDUM.md`), write the notes files, then
add the tables to `tables.csv` and rebuild.
