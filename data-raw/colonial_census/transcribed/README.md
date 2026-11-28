# Hand transcriptions (1906 profession tables)

Files read by `../extract_eur1906_t6_t7.py`. Every value was read from crops of
the Gallica page images (`data-raw/bnf_gallica/pages/bd6t53563851/`) and checked
against the printed totals by the script.

- `eur1906_t6.csv`: Table VI, with the printed subtotals used for checking.
- `eur1906_t7.txt`: Table VII, one line per circonscription x nationality (32 values), plus the printed `PAIR` and `GROUP` total lines. `?` marks a cell hidden in the binding; `?d` marks one whose last digit `d` is visible.
- `eur1906_tg.txt`: Table G, used only for validation and as a constraint. The published Table G file is `../csv/eur1906_tg_french_by_occupation_1901_1906.csv`.
- `eur1906_text_p57.csv`, `eur1906_text_p58.csv`, `eur1906_text_p61.csv`: the commentary tables, used only to check against Table VI (published as `../csv/eur1906_text_professional_status.csv`, `eur1906_text_occupation_groups.csv`, `eur1906_text_french_occupation_1896_1906.csv`).
