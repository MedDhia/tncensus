#!/usr/bin/env python3
"""Build the 1926 (tables e, f, g), 1931 and 1936 census tables from the
Statistique générale de la Tunisie yearbooks.

Every value was transcribed from the native-resolution page scans (see
hires.py) into data-raw/yearbook_demography/transcribed/*.txt, checked against
every printed total, and compared cell by cell with each reprint (see the notes
files). This script parses those transcriptions, reruns all checks, and writes
tidy CSVs plus a notes file per table to data-raw/yearbook_demography/csv/.

Usage:  python3 data-raw/yearbook_demography/extract_cens1926_b_1931_1936.py
"""
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_cmp  # noqa: E402
import check_ctl36  # noqa: E402
import check_e  # noqa: E402
import check_f  # noqa: E402
import check_towns  # noqa: E402

T = HERE / "transcribed"
OUT = HERE / "csv"
ARK = {"sgt1926": "bpt6k9105650k", "sgt1935": "bpt6k9105653t", "sgt1936": "bpt6k91056547"}

NAT_FR = {"french": "Français", "italian": "Italiens", "maltese": "Maltais", "spanish": "Espagnols",
          "greek": "Grecs", "other_european": "Autres européens"}
EUR = list(NAT_FR)
IND_NAT = [("tunisian", "Tunisiens"), ("algerian", "Algériens"), ("moroccan", "Marocains"),
           ("sudanese", "Soudanais"), ("syrian", "Syriens"), ("tripolitanian", "Tripolitains"),
           ("other", "Autres nationalités")]
JEW_NAT = [n for n in IND_NAT if n[0] != "sudanese"]
AGE_FR = {"0_4": "De 0 à 4 ans", "5_9": "5 à 9 ans", "10_14": "10 à 14 ans", "15_19": "15 à 19 ans",
          "20_24": "20 à 24 ans", "25_29": "25 à 29 ans", "30_34": "30 à 34 ans", "35_39": "35 à 39 ans",
          "40_44": "40 à 44 ans", "45_49": "45 à 49 ans", "50_54": "50 à 54 ans", "55_59": "55 à 59 ans",
          "60_plus": "60 ans et au-dessus"}
MARITAL = [("single", "Célibataires"), ("married", "Mariés"), ("widowed", "Veufs"), ("divorced", "Divorcés")]
SEX = [("male", "Sexe masculin"), ("female", "Sexe féminin")]
PROF_FR = {"agriculture": "Agriculteurs", "commerce": "Commerçants", "industry": "Industriels",
           "transport": "Entrepreneurs et Agents de transports",
           "public_administration": "Fonctionnaires et Employés des Administrations publiques",
           "police_force": "Représentants et Agents de la force publique",
           "liberal_professions": "Représentants des professions libérales",
           "independent_means": "Personnes vivant exclusivement de revenus",
           "unclassified": "Population non classée"}
STATUS = [("active", "Personnes exerçant elles-mêmes la profession"), ("family", "Famille des précédents")]

LOG = []


def note(msg):
    LOG.append(msg)


def write(name, header, rows, notes):
    OUT.mkdir(exist_ok=True)
    with open(OUT / f"{name}.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    (OUT / f"{name}.md").write_text(notes.strip() + "\n", encoding="utf-8")
    print(f"{name}: {len(rows)} rows")


def run(label, fn, *a):
    fails = []
    n, bad = fn(*a, out=fails.append) if fn is not check_towns.check else fn(*a, out=fails.append)[:2]
    print(f"  {label}: {n} checks, {bad} failing")
    return n, bad, fails


# ---------------------------------------------------------------- 1926 e
def cens1926_e():
    B, G = check_e.parse(T / "cens1926_e_sgt1926.txt")
    n, bad, fails = run("1926 e", check_e.check, B, G)
    flags = {k: v for k, v in check_e.FLAGS.items()}
    rows = []
    for b in B:
        for a in check_e.AGES:
            vals = b["rows"][a][:8]
            for m, (ms, ms_fr) in enumerate(MARITAL):
                for s, (sx, sx_fr) in enumerate(SEX):
                    k = 2 * m + s
                    fl = flags.get((b["nat"], a, k), ("", ""))[0]
                    rows.append(["sgt1926", ARK["sgt1926"], "e", 1926, b["page"], b["view"], b["nat"],
                                 NAT_FR[b["nat"]], a, AGE_FR[a], ms, ms_fr, sx, sx_fr, vals[k], fl])
    hdr = ["census", "gallica_ark", "table_id", "census_year", "source_page", "gallica_view",
           "nationality", "nationality_fr", "age_group", "age_group_fr", "marital_status",
           "marital_status_fr", "sex", "sex_fr", "value", "flag"]
    flag_lines = "\n".join(f"- {nat} {AGE_FR[a]}, column {k} ({MARITAL[k // 2][0]} {SEX[k % 2][0]}): "
                           f"`{fl}`. {txt}" for (nat, a, k), (fl, txt) in flags.items())
    write("cens1926_age_sex_marital", hdr, rows, f"""
# 1926 census: Europeans by age, sex and marital status

**e) Population européenne d'après l'âge, le sexe et l'état civil**
*European population by age group, sex and marital status, by nationality* (census of 1926).

Source: *Statistique générale de la Tunisie*, edition 1926 (`sgt1926`), Gallica ark
`{ARK['sgt1926']}`, printed pages 7-9, views 571-573. Source gallica.bnf.fr / Ministère des
Affaires étrangères. Transcription: `transcribed/cens1926_e_sgt1926.txt`.

One row per printed cell: 6 nationalities x 13 age groups x 4 marital statuses x 2 sexes.
`value` = persons. Printed row totals, "Totaux par sexe", "Totaux" and "Totaux généraux" are not
stored; they were used for validation.

## Validation

{n} checks (every row total, every column total per nationality, the Totaux by marital status, the
nationality totals and the Totaux généraux); {bad} fail. Every failure is a misprint confirmed on all
five printings and flagged `total_mismatch` (printed value kept):

{flag_lines}

Failing checks: {'; '.join(fails)}.

## Reprints

Every cell was compared with the reprints in sgt1927 (views 35-37), sgt1928 (559-561), sgt1929
(35-37) and sgt1930 (565-567): OCR row matching followed by image crops of every row where the OCR
differed (30 rows), and a visual read of every page of sgt1930.

- sgt1927, sgt1928, sgt1929: identical to sgt1926 in every cell (all OCR differences were OCR errors).
- sgt1930: identical except (1) Spanish 60 and over, married men: 14 (sgt1926-29 print 94; the row
  and column totals require 14), used here and flagged `reprint_corrected`; (2) Greek 40-44 single
  men printed 7 (8 elsewhere; the row total requires 8, kept 8); (3) the Italian married-women column
  is garbled in sgt1930 (11 of 13 cells differ and no longer add up to the printed row totals); the
  sgt1926 column, which adds up, is kept.
- The other misprints listed above appear identically in all five editions.
""")
    return len(rows)


# ---------------------------------------------------------------- 1926 f
def cens1926_f():
    B = check_f.parse(T / "cens1926_f_sgt1926.txt")
    n, bad, fails = run("1926 f", check_f.check, B)
    flags = dict(check_f.FLAGS)
    rows = []
    for nat in check_f.NATS:
        b = B[nat]
        for cat in check_f.CATS:
            v = b["rows"][cat][0]
            for st, (s, s_fr) in enumerate(STATUS):
                for sx, (x, x_fr) in enumerate(SEX):
                    k = 2 * st + sx
                    fl = flags.get((nat, cat, k), ("", ""))[0]
                    rows.append(["sgt1926", ARK["sgt1926"], "f", 1926, b["page"], b["view"], nat,
                                 NAT_FR[nat], cat, PROF_FR[cat], s, s_fr, x, x_fr.replace("Sexe ", ""), v[k], fl])
    hdr = ["census", "gallica_ark", "table_id", "census_year", "source_page", "gallica_view",
           "nationality", "nationality_fr", "profession", "profession_fr", "status", "status_fr",
           "sex", "sex_fr", "value", "flag"]
    write("cens1926_profession_nationality", hdr, rows, f"""
# 1926 census: Europeans by profession and nationality

**f) Population européenne par profession et nationalité**
*European population by occupational category, nationality, status (persons exercising the
profession themselves, or family members of the preceding) and sex* (census of 1926).

Source: *Statistique générale de la Tunisie*, edition 1926 (`sgt1926`), Gallica ark
`{ARK['sgt1926']}`, printed pages 10-11, views 574-575. Source gallica.bnf.fr / Ministère des
Affaires étrangères. Transcription: `transcribed/cens1926_f_sgt1926.txt`.

One row per printed cell: 6 nationalities x 9 categories x 2 statuses x 2 sexes. `value` = persons.
The printed subtotals (active, family, nationality total per category), the TOTAUX line and the
"Totaux" block for all Europeans are not stored; they were used for validation (the all-Europeans
cells equal the sum of the nationalities).

Footnotes (translated): (1) rural owners, farmers, sharecroppers, managers, foremen, gardeners and
farm workers of every kind; (2) staff of all shops (other than those of industrial
establishments), banks, insurance companies, brokerage and rental agencies, etc.; (3) masters and
workers of all trades actually engaged in manufacturing: mines, quarries, salt works, oil mills,
soap works, tanneries, factories, public-works contractors, fisheries, etc.; (4) staff of shipping
and railway companies, carriers, hauliers and their employees, car and carriage hirers and their
staff; (5) staff of all civil services of the State or the municipalities, including the
judiciary and law officers; (6) police staff; (7) lawyers, doctors, pharmacists, dentists, business
agents, expert arbitrators, artists, clergy and members of religious communities; (8) persons who,
living on income from annuities, securities, rents, etc., are assumed not to exercise a profession;
(9) persons who fit none of the preceding categories.

## Validation

{n} checks (every M+F subtotal, every category total, every column against TOTAUX, each nationality
total against table e, and each all-Europeans cell against the sum of the nationalities); {bad} fail.

One data cell is flagged: French industry, active women, printed 518 in all five editions; the
printed active subtotal (4.846) and the all-Europeans industry column (1.533) both imply 510
(`total_mismatch`, printed value kept). The other failures are in printed total lines, which are not
stored: the French TOTAUX line (22.825 / 10.760, where the cells give 22.856 / 10.737 and the
all-Europeans totals agree with the cells), the Maltese active total (printed 1.258 for 4.258), the
Spanish active women total (105 for 106) and the all-Europeans family-women total (65.386 for
65.387).

Failing checks: {'; '.join(fails)}.

## Reprints

sgt1930 (views 568-569) was compared visually in full, and sgt1927 (38-39), sgt1928 (562-563) and
sgt1929 (38-39) row by row on the rows that decide a mismatch (French industry, French TOTAUX,
Spanish unclassified and totals). No reprint changes a data cell. sgt1930 has two printing errors of
its own in subtotals (Spanish unclassified nationality total 96 for 136; Greek liberal professions
family women 8 with a family subtotal of 6); the sgt1926 values, which add up, are kept.
""")
    return len(rows)


# ---------------------------------------------------------------- 1926 g
def cens1926_g():
    R = {}
    for ln in open(T / "cens1926_g_sgt1926.txt", encoding="utf-8"):
        ln = ln.split("#")[0].strip()
        if ln:
            p = ln.split()
            R[p[0]] = [None if x == "NA" else float(x) for x in p[1:]]
    checks = bad = 0
    fails = []

    def c(nm, a, b, tol=0.0):
        nonlocal checks, bad
        checks += 1
        if abs(a - b) > tol:
            bad += 1
            fails.append(f"{nm}: {a} != {b}")
    nats = EUR
    for nat in nats + ["TOTAL"]:
        v = R[nat]
        c(f"{nat} illiterate+literate=total", v[0] + v[2], v[4])
        c(f"{nat} illiterate %", round(100 * v[0] / v[4], 1), v[1], 0.11)
        c(f"{nat} literate %", round(100 * v[2] / v[4], 1), v[3], 0.11)
        if v[5] is not None:
            c(f"{nat} French-speaking %", round(100 * v[5] / v[4], 1), v[6], 0.11)
        c(f"{nat} Arabic-speaking %", round(100 * v[7] / v[4], 1), v[8], 0.11)
    for k in (0, 2, 4, 7, 9):
        c(f"column {k}", sum(R[nat][k] for nat in nats), R["TOTAL"][k])
    for k in (5, 10):
        c(f"column {k}", sum(R[nat][k] for nat in nats if R[nat][k] is not None), R["TOTAL"][k])
    c("total vs table e", R["TOTAL"][4], 173281)
    print(f"  1926 g: {checks} checks, {bad} failing")
    ind = [("illiterate", "Illettrés", 0, "count", 1926), ("illiterate", "Illettrés", 1, "pct_of_nationality", 1926),
           ("literate", "Sachant lire et écrire", 2, "count", 1926),
           ("literate", "Sachant lire et écrire", 3, "pct_of_nationality", 1926),
           ("speaks_french", "Parlant français", 5, "count", 1926),
           ("speaks_french", "Parlant français", 6, "pct_of_nationality", 1926),
           ("speaks_arabic", "Parlant arabe", 7, "count", 1926),
           ("speaks_arabic", "Parlant arabe", 8, "pct_of_nationality", 1926),
           ("literate", "Sachant lire et écrire (répartition d'après l'instruction en 1921)", 9, "count", 1921),
           ("speaks_french", "Parlant français (répartition d'après l'instruction en 1921)", 10, "count", 1921)]
    rows = []
    for nat in nats:
        for code, fr, k, meas, yr in ind:
            v = R[nat][k]
            fl = "not_applicable" if v is None else ""
            if nat == "maltese" and code == "illiterate" and meas == "pct_of_nationality":
                fl = "total_mismatch"
            val = "" if v is None else (int(v) if meas == "count" else v)
            rows.append(["sgt1926", ARK["sgt1926"], "g", yr, 12, 576, nat, NAT_FR[nat], code, fr, meas, val, fl])
    hdr = ["census", "gallica_ark", "table_id", "census_year", "source_page", "gallica_view",
           "nationality", "nationality_fr", "indicator", "indicator_fr", "measure", "value", "flag"]
    write("cens1926_instruction", hdr, rows, f"""
# 1926 census: Europeans by instruction (1921 and 1926)

**g) Population européenne d'après l'instruction (recensements de 1921 et 1926)**
*European population by literacy, knowledge of French and of Arabic, 1926; with the 1921
distribution by instruction.*

Source: *Statistique générale de la Tunisie*, edition 1926 (`sgt1926`), Gallica ark
`{ARK['sgt1926']}`, printed page 12, view 576. Source gallica.bnf.fr / Ministère des Affaires
étrangères. Transcription: `transcribed/cens1926_g_sgt1926.txt`.

One row per printed cell. `measure` is `count` (persons) or `pct_of_nationality` (percentage of the
nationality's 1926 total, as printed, with one decimal). `census_year` is 1926, except the two
columns "Répartition d'après l'instruction en 1921" (1921). The printed nationality totals (equal
to the 1926 census totals) and the TOTAUX row are not stored.

Footnote (translated): (1) the question [speaking French] does not apply to the French; those cells
are NA with flag `not_applicable`. Under the table: "the percentage is calculated on the total
of each nationality".

## Validation

{checks} checks (illiterate + literate = total; each percentage recomputed within 0.1; every column
against the TOTAUX row; the total against table e); {bad} fail. {'; '.join(fails)}

The Maltese illiterate share is printed 55,1 in all five editions; 4.268 / 8.396 gives 50,8 (and
50,8 + 49,1 = 99,9), so the cell is flagged `total_mismatch` (printed value kept). The three other
failures are the shares printed in the TOTAUX row (not stored), which do not match the printed
counts (34,5 / 65,8 / 25,5 printed; 34,7 / 65,3 / 25,7 recomputed).

## Reprints

Compared visually, every cell, with sgt1927 (view 40), sgt1928 (564), sgt1929 (40) and sgt1930
(570): identical.
""")
    return len(rows)


# ---------------------------------------------------------------- shared readers
def read_ctl31():
    R = {}
    for ln in open(T / "cens1931_controle_sgt1935.txt", encoding="utf-8"):
        ln = ln.split("#")[0].strip()
        if ln:
            name, rest = ln.split(None, 1)
            R[name.replace("_", " ")] = [s.split() for s in rest.split("|")]
    return R


CTL_NAME = {"Kef (Le)": "Le Kef", "Teboursouk": "Téboursouk"}


# ---------------------------------------------------------------- 1931 contrôle
def cens1931_controle():
    import pandas as pd
    R = read_ctl31()
    n = bad = 0
    fails = []

    def c(nm, a, b):
        nonlocal n, bad
        n += 1
        if a != b:
            bad += 1
            fails.append(f"{nm}: {a} != {b}")
    sud = {}
    for k, (e, m, j, it, gt) in R.items():
        e = list(map(int, e)); j = list(map(int, j))
        mm = [None if x == "?" else int(x) for x in m]
        sud[k] = mm[7] - sum(x for i, x in enumerate(mm[:7]) if i != 3)
        c(f"{k} european total", sum(e[:6]), e[6]); c(f"{k} jewish total", sum(j[:6]), j[6])
        c(f"{k} indigenous = muslim + jewish", mm[7] + j[6], int(it[0])); c(f"{k} grand", e[6] + int(it[0]), int(gt[0]))
    rows_ = [k for k in R if k != "TOTAUX"]
    for gi in range(3):
        for kk in range(len(R["TOTAUX"][gi])):
            if R["TOTAUX"][gi][kk] == "?":
                c("sudanese column (derived) vs printed Muslim total", sum(sud[r] for r in rows_), sud["TOTAUX"])
                continue
            c(f"column {gi}.{kk}", sum(int(R[r][gi][kk]) if R[r][gi][kk] != "?" else sud[r] for r in rows_),
              int(R["TOTAUX"][gi][kk]))
    # cross-check with the 1931 indigenous census volume
    t1 = pd.read_csv(HERE.parent / "colonial_census" / "csv" / "ind1931_t1_controle_nationality.csv", encoding="utf-8-sig")
    P = t1.pivot_table(index="controle_civil", columns=["religion", "nationality"], values="value", aggfunc="sum")
    xn = xbad = 0
    for k in rows_:
        kk = CTL_NAME.get(k, k)
        mm = [sud[k] if x == "?" else int(x) for x in R[k][1]]
        for i, (nat, _) in enumerate(IND_NAT):
            xn += 1; xbad += mm[i] != int(P.loc[kk, ("muslim", nat)])
        for i, (nat, _) in enumerate(JEW_NAT):
            xn += 1; xbad += int(R[k][2][i]) != int(P.loc[kk, ("jewish", nat)])
    print(f"  1931 contrôle: {n} checks, {bad} failing; cross-check {xn} cells, {xbad} differ")
    rows = []
    for k in rows_:
        e, m, j = R[k][0], R[k][1], R[k][2]
        ck = CTL_NAME.get(k, k)
        for i, nat in enumerate(EUR):
            rows.append(["sgt1935", ARK["sgt1935"], "controle", 1931, 2, 22, ck, "european", "Population européenne",
                         nat, NAT_FR[nat], int(e[i]), ""])
        for i, (nat, fr) in enumerate(IND_NAT):
            v = sud[k] if m[i] == "?" else int(m[i])
            rows.append(["sgt1935", ARK["sgt1935"], "controle", 1931, 2 if i < 3 else 3, 22 if i < 3 else 23, ck,
                         "muslim", "Population musulmane", nat, fr, v, "derived_from_totals" if m[i] == "?" else ""])
        for i, (nat, fr) in enumerate(JEW_NAT):
            rows.append(["sgt1935", ARK["sgt1935"], "controle", 1931, 3, 23, ck, "jewish", "Population israélite",
                         nat, fr, int(j[i]), ""])
    hdr = ["census", "gallica_ark", "table_id", "census_year", "source_page", "gallica_view", "controle_civil",
           "population", "population_fr", "nationality", "nationality_fr", "value", "flag"]
    write("cens1931_controle_nationality", hdr, rows, f"""
# 1931 census: population by contrôle civil, group and nationality

**Répartition, par circonscriptions de Contrôles civils, de la population civile, européenne et
indigène, d'après le recensement de 1931**
*Civilian population by contrôle civil: Europeans by nationality, Muslims and Jews by nationality.*

Source: *Statistique générale de la Tunisie*, edition 1935 (`sgt1935`), Gallica ark
`{ARK['sgt1935']}`, printed pages 2-3, views 22-23. Source gallica.bnf.fr / Ministère des Affaires
étrangères. Transcription: `transcribed/cens1931_controle_sgt1935.txt`. Not reprinted in another
edition on Gallica.

One row per printed cell: 20 contrôles civils (the last is "Territoires militaires") x (6 European
nationalities + 7 Muslim nationalities + 6 Jewish nationalities). `population` is `european`,
`muslim` or `jewish`. `value` = persons. Printed totals (by group, indigenous, grand total, TOTAUX
row) are not stored.

The Muslim "Soudanais" column falls in the binding gutter between the two pages and is unreadable;
its 20 cells are derived as the printed Muslim total minus the other six nationalities (flag
`derived_from_totals`). The derived column sums to 445, as does the indigenous census volume.

## Validation

{n} checks (every group total, indigenous = Muslim + Jewish, grand total, every column against the
TOTAUX row); {bad} fail. {'; '.join(fails)}

Cross-check with the 1931 census volume (*Dénombrement de la population civile indigène*, Table I,
`data-raw/colonial_census/csv/ind1931_t1_controle_nationality.csv`): {xn} Muslim and Jewish cells
compared, {xbad} differ. The national totals equal those of the census volume (2.159.151 Muslims,
56.248 Jews).
""")
    return len(rows)


# ---------------------------------------------------------------- comparison tables
def compare_table(path, ed, views, pages, years, out_name, title_fr, title_en, swap=None, pant_year=None,
                  extra_notes="", mt_change=True):
    R = check_cmp.parse(path)
    n, bad, fails = run(out_name, check_cmp.check, R)
    rows = []
    for k, g in R.items():
        if k == "TOTAUX":
            continue
        ck = swap.get(k, k) if swap else k
        for i, nat in enumerate(EUR):
            for yi, yr in enumerate(years):
                page, view = (pages[0], views[0]) if i < 3 else (pages[1], views[1])
                fl = ""
                if ed == "sgt1936" and k == "Sousse" and nat == "maltese" and yr == 1936:
                    fl = "reprint_corrected"
                rows.append([ed, ARK[ed], "compare", yr, page, view, ck, k, nat, NAT_FR[nat], g[i][yi], fl])
        rows.append([ed, ARK[ed], "compare", pant_year, pages[1], views[1], ck, k, "italian_pantelleria",
                     "Italiens originaires de l'île de Pantelleria", g[7][0], ""])
    hdr = ["census", "gallica_ark", "table_id", "census_year", "source_page", "gallica_view", "controle_civil",
           "controle_civil_printed", "nationality", "nationality_fr", "value", "flag"]
    write(out_name, hdr, rows, f"""
# {title_en}

**{title_fr}**

Source: *Statistique générale de la Tunisie*, edition {ed[3:]} (`{ed}`), Gallica ark `{ARK[ed]}`,
printed pages {pages[0]}-{pages[1]}, views {views[0]}-{views[1]}. Source gallica.bnf.fr / Ministère
des Affaires étrangères. Transcription: `transcribed/{Path(path).name}`.

One row per printed count: 20 circonscriptions x 6 nationalities x 2 censuses ({years[0]}, {years[1]}),
plus one row per circonscription for the Italians originating from the island of Pantelleria
(`nationality = italian_pantelleria`, census {pant_year}; printed footnote: "the number of Italians
from the island of Pantelleria is included in the Italians"). `value` = persons. The printed
changes ("augmentation ou diminution"), the totals and the TOTAUX row are not stored; they were used
for validation. `controle_civil` gives the circonscription the figures belong to;
`controle_civil_printed` the row label as printed.

## Validation

{n} checks (each printed change = later census - earlier census, each total, every column against
the TOTAUX row){'' if mt_change else '; the Maltese change column is lost in the binding gutter'};
{bad} fail. {'; '.join(fails)}

{extra_notes}
""")
    return len(rows)


def cens1931_compare():
    R = check_cmp.parse(T / "cens1931_compare_1926_sgt1935.txt")
    C = read_ctl31()
    m31 = {"Le Kef": "Kef (Le)", "Téboursouk": "Teboursouk", "Territoires du Sud": "Territoires militaires"}
    swap = {"Tabarka": "Souk-el-Arba", "Souk-el-Arba": "Tabarka"}
    diff = []
    for k, g in R.items():
        if k == "TOTAUX":
            continue
        v31 = [g[i][1] for i in range(7)]
        real = swap.get(k, k)
        if v31 != [int(x) for x in C[m31.get(real, real)][0]]:
            diff.append(k)
    print(f"  1931 compare vs 1931 contrôle (after the label swap): {len(R) - 1} rows, {len(diff)} differ {diff}")
    return compare_table(T / "cens1931_compare_1926_sgt1935.txt", "sgt1935", (24, 25), (4, 5), (1926, 1931),
                         "cens1931_compare_1926_1931",
                         "Statistique comparée des dénombrements de 1926 et 1931 concernant la population "
                         "européenne de la Tunisie, répartie par circonscriptions administratives",
                         "European population by circonscription and nationality, 1926 and 1931",
                         swap=swap, pant_year=1931, mt_change=False, extra_notes=f"""
## Row labels and cross-checks

The rows printed "Tabarka" and "Souk-el-Arba" carry each other's figures: the 1931 columns of the
row printed "Tabarka" equal Souk-el-Arba in the 1931 contrôle table, and vice versa, for all seven
columns (and the 1926 Souk-el-Arba and Tabarka rows of the 1931-1936 comparison in sgt1936 agree).
`controle_civil` is corrected accordingly; `controle_civil_printed` keeps the printed label.

After that correction, the 1931 columns of all 20 rows equal the 1931 contrôle table
(`cens1931_controle_nationality`, Europeans): {len(diff)} rows differ. The 1926 totals by nationality
equal the 1926 census totals of table e (71.020 French, 89.216 Italians, 8.396 Maltese, 517 Spanish,
646 Greeks, 3.486 others).

Not reprinted in another edition on Gallica.
""")


def cens1936_compare():
    R = check_cmp.parse(T / "cens1936_compare_1931_sgt1936.txt")
    C = read_ctl31()
    m31 = {"Le Kef": "Kef (Le)", "Téboursouk": "Teboursouk", "Territoires du Sud": "Territoires militaires"}
    d31 = [k for k, g in R.items() if k != "TOTAUX" and [g[i][0] for i in range(7)] != [int(x) for x in C[m31.get(k, k)][0]]]
    C36 = check_ctl36.parse(T / "cens1936_controle_sgt1936.txt")
    d36 = [k for k, g in R.items() if k != "TOTAUX" and [g[i][1] for i in range(7)] != C36[{"Territoires du Sud": "Territoires militaires"}.get(k, k)][3]]
    print(f"  1936 compare: 1931 columns differing from the 1931 table: {d31}; 1936 columns differing from the 1936 table: {d36}")
    return compare_table(T / "cens1936_compare_1931_sgt1936.txt", "sgt1936", (15, 16), (4, 5), (1931, 1936),
                         "cens1936_compare_1931_1936",
                         "Statistique comparée des dénombrements de 1931 et 1936 concernant la population "
                         "européenne de la Tunisie, répartie par circonscriptions administratives",
                         "European population by circonscription and nationality, 1931 and 1936",
                         pant_year=1936, extra_notes=f"""
## Reprint and cross-checks

- **Reprint in sgt1939** (`bpt6k9105739w`, views 10-11): every row compared (OCR row matching, then
  image crops of every row with a difference). Identical, except Sousse Maltese 1936: sgt1936 prints
  370, sgt1939 prints 379, which the printed change (-158), the Sousse total (11.006) and the column
  total (7.279) require; 379 is used, flagged `reprint_corrected`.
- **1931 columns** equal the 1931 contrôle table (`cens1931_controle_nationality`) in all 20 rows,
  all 7 columns (rows differing: {d31 or 'none'}). Here Tabarka and Souk-el-Arba are printed
  correctly.
- **1936 columns** against the 1936 contrôle table (`cens1936_controle_nationality`): rows differing
  {d36}. Bizerte Maltese (306 here, 305 there) and Territoires du Sud French (596 here, 595 there):
  this table's values make both tables' row and column totals add up, so the contrôle table carries
  the misprints (flagged there). Sousse Maltese: 379 in both after the reprint correction.
""")


# ---------------------------------------------------------------- 1936 contrôle
def cens1936_controle():
    R = check_ctl36.parse(T / "cens1936_controle_sgt1936.txt")
    n, bad, fails = run("1936 contrôle", check_ctl36.check, R)
    FL = {("Bizerte", "european", "maltese"): "total_mismatch",
          ("Territoires militaires", "european", "french"): "total_mismatch",
          ("Souk-el-Arba", "muslim", "moroccan"): "total_mismatch"}
    rows = []
    for k, (m, j, it, e, g) in R.items():
        if k == "TOTAUX":
            continue
        for i, (nat, fr) in enumerate(IND_NAT):
            rows.append(["sgt1936", ARK["sgt1936"], "controle", 1936, 2, 13, k, "muslim", "Population musulmane",
                         nat, fr, m[i], FL.get((k, "muslim", nat), "")])
        for i, (nat, fr) in enumerate(JEW_NAT):
            pg, vw = (2, 13) if i < 3 else (3, 14)
            rows.append(["sgt1936", ARK["sgt1936"], "controle", 1936, pg, vw, k, "jewish", "Population israélite",
                         nat, fr, j[i], ""])
        for i, nat in enumerate(EUR):
            rows.append(["sgt1936", ARK["sgt1936"], "controle", 1936, 3, 14, k, "european", "Population européenne",
                         nat, NAT_FR[nat], e[i], FL.get((k, "european", nat), "")])
    hdr = ["census", "gallica_ark", "table_id", "census_year", "source_page", "gallica_view", "controle_civil",
           "population", "population_fr", "nationality", "nationality_fr", "value", "flag"]
    write("cens1936_controle_nationality", hdr, rows, f"""
# 1936 census: population by contrôle civil, group and nationality

**Répartition, par circonscriptions de Contrôles civils, de la population civile, européenne et
indigène, d'après le recensement de 1936**
*Civilian population by contrôle civil: Muslims and Jews by nationality, Europeans by nationality.*

Source: *Statistique générale de la Tunisie*, edition 1936 (`sgt1936`), Gallica ark
`{ARK['sgt1936']}`, printed pages 2-3, views 13-14. Source gallica.bnf.fr / Ministère des Affaires
étrangères. Transcription: `transcribed/cens1936_controle_sgt1936.txt`. Reprinted in sgt1939
(`bpt6k9105739w`, views 8-9, "d'après le dernier recensement (1936)").

One row per printed cell: 20 contrôles civils x (7 Muslim + 6 Jewish + 6 European nationalities).
`value` = persons. Printed totals are not stored. The Jewish table has no "Soudanais" column.

The printed column headings are misplaced: the Jewish total is printed under "TOTAUX de la
population tunisienne" and the indigenous total (Muslims + Jews) under "TOTAUX de la population
israélite".

## Validation

{n} checks (every group total, indigenous, grand total, every column against TOTAUX); {bad} fail,
all printing errors present identically in sgt1936 and sgt1939:

- three data cells, each where a row and its column are off by the same amount, flagged
  `total_mismatch` (printed values kept): Bizerte Maltese printed 305 (the comparison table prints
  306, which makes the row and the Maltese column add up); Territoires militaires French printed 595
  (comparison table 596); Souk-el-Arba Moroccan Muslims printed 79 (row and column imply 78);
- printed totals only (not stored): Sousse Muslim total printed 332.192 for 322.192 (the printed
  indigenous total, 327.182, uses 322.192); TOTAUX Tripolitanian Muslims printed 23.807 for 23.907
  (the printed Muslim grand total uses 23.907); Maktar grand total printed 69.278 for 69.273.

Failing checks: {'; '.join(fails)}.

## Reprint

Every row compared with sgt1939 (OCR row matching, then image crops of each row with a difference):
identical, except sgt1939 prints Tozeur French as 78 (sgt1936: 178; the Tozeur European total, 186,
requires 178; 178 kept).
""")
    return len(rows)


# ---------------------------------------------------------------- towns
TOWN_PART = {"five": ("five_largest", "Population européenne et indigène des cinq plus grandes villes"),
             "over_10000": ("over_10000", "Villes comptant plus de 10.000 habitants"),
             "5000_10000": ("5000_to_10000", "Villes comptant de 5.000 à 10.000 habitants")}


def towns(path, ed, year, out_name, flags, extra):
    B = check_towns.parse(path)
    n, bad, fails = check_towns.check(B, out=lambda s: None)
    print(f"  {out_name}: {n} checks, {bad} failing")
    rows = []
    for b in B:
        part, part_fr = TOWN_PART[b["group"]]
        for r in b["rows"]:
            vals = [(nat, NAT_FR[nat], "european", r["eur"][i]) for i, nat in enumerate(EUR)]
            vals += [("muslims", "Musulmans", "muslim", r["ind"][0]), ("jews", "Israélites", "jewish", r["ind"][1])]
            for nat, fr, pop, v in vals:
                rows.append([ed, ARK[ed], "towns", year, b["page"], b["view"], part, part_fr, r["town"], r["controle"],
                             pop, nat, fr, v, flags.get((b["group"], r["town"], nat), "")])
    hdr = ["census", "gallica_ark", "table_id", "census_year", "source_page", "gallica_view", "table_part",
           "table_part_fr", "town", "controle_civil", "population", "group", "group_fr", "value", "flag"]
    write(out_name, hdr, rows, f"""
# {year} census: European and indigenous population of the towns

**Population européenne et indigène des cinq plus grandes villes**, and **... des villes comptant
1° plus de 10.000 habitants, 2° de 5.000 à 10.000 habitants**
*Europeans by nationality, Muslims and Jews, in the five largest towns and in every town of more
than 5,000 inhabitants* (census of {year}).

Source: *Statistique générale de la Tunisie*, edition {ed[3:]} (`{ed}`), Gallica ark `{ARK[ed]}`,
printed page 6, view {B[0]['view']}. Source gallica.bnf.fr / Ministère des Affaires étrangères.
Transcription: `transcribed/{Path(path).name}`.

One row per printed cell: town x (6 European nationalities, Muslims, Jews). `table_part` says which
of the three printed tables the row comes from; the five largest towns are printed twice (in the
first table and at the head of the list of towns over 10,000), and both printings are kept.
`controle_civil` is the "ressort du contrôle civil" as printed (empty for the five-largest table,
which has no such column, filled with the town's contrôle for convenience). `value` = persons.
Printed European, indigenous and grand totals are not stored.

## Validation

{n} checks (European total, indigenous = Muslims + Jews, grand total, for every town); {bad} fail.
{'; '.join(fails)}

{extra}
""")
    return len(rows)


def main():
    n = 0
    n += cens1926_e()
    n += cens1926_f()
    n += cens1926_g()
    n += cens1931_controle()
    n += cens1931_compare()
    n += cens1936_controle()
    n += cens1936_compare()
    n += towns(T / "cens1931_towns_sgt1935.txt", "sgt1935", 1931, "cens1931_towns",
               {("five", "Sfax", "french"): "total_mismatch"}, """
## Misprints and reprints

- Sfax French: printed 4.135 in the five-largest table and 4.435 in the list of towns over 10,000;
  the printed European total (8.177) requires 4.435. Both printings are kept as printed; the
  five-largest cell is flagged `total_mismatch`.
- Béja grand total printed 1.612 for 11.612 (a total, not stored).
- Not reprinted in another edition on Gallica.
""")
    n += towns(T / "cens1936_towns_sgt1936.txt", "sgt1936", 1936, "cens1936_towns",
               {("five", "Kairouan", "italian"): "reprint_corrected", ("five", "Kairouan", "maltese"): "reprint_corrected",
                ("5000_10000", "Zarzis", "muslims"): "reprint_corrected"}, """
## Misprints and reprints

Compared visually, every cell, with the reprint in sgt1939 (`bpt6k9105739w`, view 12).

- Kairouan (five-largest table): sgt1936 prints Italians 7 and Maltese 171 (swapped); the list of
  towns over 10,000 and the sgt1939 reprint print Italians 171 and Maltese 7, used here
  (`reprint_corrected`).
- Zarzis Muslims: sgt1936 prints 7.244, sgt1939 prints 7.224, which the printed indigenous (7.484)
  and grand (7.641) totals require; 7.224 used (`reprint_corrected`).
- Bizerte European total printed 8.661 (Sfax's figure) in both sgt1936 tables; the cells sum to
  11.257, which sgt1939 prints in both tables. The five-largest grand total is corrected to 28.468 in
  sgt1939, but the list keeps 25.872 in both editions. Totals are not stored; the cells are the same
  in both editions.
- Totals misprinted in both editions (not stored): M'Saken grand total 20.088 for 20.089;
  Menzel-Temim grand total 8.532 for 7.832.
- Gafsa and Mahdia "other Europeans" are smudged; read as 3 and 1, as the printed European totals
  require, in both editions.
""")
    print(f"total rows: {n}")


if __name__ == "__main__":
    main()
