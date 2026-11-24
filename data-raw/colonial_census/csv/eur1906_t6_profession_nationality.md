# 1906 Table VI: profession, sex and nationality

**VI. Répartition d'après la profession, le sexe et la nationalité**
(Distribution by profession, sex and nationality). European civilian population
of Tunisia, census of 16 December 1906.

- Source: *Dénombrement de la population européenne civile en Tunisie au 16 décembre 1906* (1907), Gallica ark `bd6t53563851`, pp. 24-25 (view 28, a two-page spread).
- Rows: 192 = 9 profession groups x 6 nationalities x status x sex. Rentiers and the unclassified population have no "family" columns, so they have no `family` rows.
- Script: `data-raw/colonial_census/extract_eur1906_t6_t7.py`; transcription: `transcribed/eur1906_t6.csv`.

## Columns

| Column | Meaning |
|---|---|
| `nationality` | `french`, `italian`, `maltese`, `spanish`, `greek`, `other_european` (French label in `nationality_fr`) |
| `profession` | Profession group (see below); `profession_fr` is the printed heading |
| `status` | `active` = *personnes exerçant elles-mêmes la profession* (persons who themselves exercise the profession); `family` = *famille des précédents* (family members of the above, including domestic servants) |
| `sex` | `male` / `female` (*Masc.* / *Fém.*) |
| `value` | Number of persons |

Profession groups: `agriculture` (*Agriculteurs*: landowners, tenant farmers,
sharecroppers, managers, foremen, gardeners and farm workers), `commerce`
(*Commerçants*: shop staff, banks, insurance, brokerage and rental agencies),
`industry` (*Industriels*: employers and workers of all manufacturing trades,
incl. mines, quarries, salt works, oil mills, tanneries, metal works, public-works
contractors, fishermen), `transport` (*Entrepreneurs et agents de transports*),
`public_administration` (*Fonctionnaires et employés des administrations
publiques*, incl. municipalities, judiciary), `police` (*Représentants et agents
de la force publique*), `liberal_professions` (*Représentants des professions
libérales*: lawyers, doctors, pharmacists, dentists, experts, business agents,
artists, clergy and religious communities), `rentiers` (*Personnes vivant
exclusivement de revenus*: annuities, securities, rents), `unclassified`
(*Population non classée*: persons fitting no category).

## Validation

All 192 cells, the 4 sex/status totals per profession, the active/family
subtotals and grand totals printed for every profession x nationality, the
totals column and the totals row were checked: 317 checks, all pass.

One misprint in the original: the grand total of family males reads
**22.262**. The nationality cells and the profession rows both sum to
**22.662**, and only 22.662 is consistent with the printed totals 68.768
(family) and 128.895 (all Europeans). The same misprint is repeated on p. 57.
It affects only a printed total, not a data cell.

## Notes printed with the table

The notes under Table VII (p. 26) apply to Tables VI and VII. Translated: each
profession category counts separately (1) persons who actually exercise the
profession, and (2) persons who, living with them, exercise no profession or
work as domestic servants ("family of the above"). Family members are assigned
to the nationality of the person they live with, *even if their own nationality
differs*. When several members of a household exercise a profession, each is
classed under their own profession and nationality. Only servants of private
persons count as domestics; servants of businesses (hotels, shipping, etc.) are
counted in that business's profession group. The active/family distinction is
dropped for rentiers and the unclassified. The commentary (p. 57) warns that
the "family" rule was not always applied consistently.
