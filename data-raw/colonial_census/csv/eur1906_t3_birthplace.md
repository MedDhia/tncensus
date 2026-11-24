# eur1906 Table III — Répartition d'après le lieu de naissance

*Distribution by place of birth.* Same source, printed pages 16–17 (views 20–21).
Built from `transcriptions/eur1906_t3_f020.txt` and `f021.txt`.

Two blocks:
- **A) Français.** French citizens, by place of birth: Tunisia, the three
  Algerian départements, the 87 metropolitan départements, the French colonies,
  abroad, and unknown.
- **B) Etrangers.** All foreign Europeans, by country of birth, with Italy split
  into regions.

| Column | Meaning |
|---|---|
| `nationality_group` | `french` (block A) or `foreign` (block B) |
| `birthplace_type` | `country`, `algeria_department`, `france_department`, `french_colonies`, `abroad`, `unknown`, `italy_region`, `region` (continents and sub-regions such as *Amérique du Nord* or *Antilles anglaises*) |
| `birthplace_fr` | Place as printed. Algerian départements are written `Algérie, département d'Alger`, and Italian regions `Italie, Sicile`; on the page these are braced groups |
| `value` | Persons |

139 rows: 94 French birthplaces, 45 foreign. Printed zeros (Monténégro, Serbie)
are kept.

**Validation (all passing).** 6 running-total checks: the "A reporter" and
"Report" carry-overs between columns and pages, and the two grand totals
(French 34,610, foreigners 94,285). Both totals agree with Table I. No cell
needed correcting.

Footnote (1), on *Colonies et possessions françaises*: "Autres que l'Algérie et
la Tunisie", i.e. other than Algeria and Tunisia.
In block A, *Etranger* means French citizens born abroad; in block B, *France*
means foreigners born in France. On the scan a later reader has circled Sicily
(45,049) and pencilled sums in the margin; these are ignored.
