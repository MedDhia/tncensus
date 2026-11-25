# Status

**Done and in the package:** the health chapter's population tables
(`csv/health_*`, 20 tables, built by `extract_health_population.py`): hospitals
and Tunis mortality, all 12 editions, validated (see each notes file and
`csv/health_validation.json`).

**Work in progress, not in the package and not validated:** the rest of the
table below.

| Part | Transcribed (`transcribed/`) | Script | Validated |
|---|---|---|---|
| Health: budgets and institutes | `health_finance_*`: 1922-1930, 1935 (10 of 12 editions) | none yet | no |
| Health: hospitals and Tunis mortality | `health_pop_*`: all 12 editions | `extract_health_population.py` | **yes** (in the package) |
| Instruction: summary tables | `education_sum_*`: 1922-1927 (6 of 12) | `extract_education_summary.py` (draft) | no |
| Instruction: school lists | `education_schools_*`: 1922; 1930 in progress; 1939 not started | `extract_education_schools.py` (draft); `csv/education_schools.csv` is a draft | no |

To finish: complete the transcriptions, run each script, check every printed
total (see `data-raw/colonial_census/SPEC.md` and
`data-raw/yearbook_demography/SPEC_ADDENDUM.md`), write the notes files, then
add the tables to `tables.csv` and rebuild.
