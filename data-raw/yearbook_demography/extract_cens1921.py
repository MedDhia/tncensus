#!/usr/bin/env python3
"""Build the 1921 census tables of the Statistique générale de la Tunisie.

Source: the Démographie chapter of the 1922 edition (sgt1922, Gallica volume
bpt6k9105649x, views 26-38, pp.2-14), which reprints the 1921 census results
(tables a to p). Values were transcribed from the page images (with Gallica's
OCR as a draft) into transcribed/cens1921_*.txt. This script

  1. parses the transcriptions into tidy CSVs in csv/cens1921_*.csv,
  2. checks every printed row, column and grand total, and cross-checks
     between tables and against the 1906 census volume
     (data-raw/colonial_census/csv/eur1906_te_*, eur1906_tb_*),
  3. compares every cell with the reprints of the same tables in the 1923,
     1924 and 1925 editions, using Gallica's OCR of those pages (a cell counts
     as confirmed by a reprint when its value occurs among the numbers the OCR
     reads on the corresponding reprint page; see compare_reprints()),
  4. writes one notes file per CSV with the validation results.

Usage:  python3 data-raw/yearbook_demography/extract_cens1921.py
"""
import collections
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE.parent / "colonial_census"))
import ocr  # noqa: E402

T = HERE / "transcribed"
OUT = HERE / "csv"
ARK = "bpt6k9105649x"
ARK25 = "bpt6k9105650k"
SRC = "sgt1922"
CREDIT = "Source gallica.bnf.fr / Ministère des Affaires étrangères"

# Reprint views of each group of tables: edition -> (ark, views)
REPRINTS = {
    "a": {"sgt1923": (ARK, [504, 505]), "sgt1924": (ARK, [992, 993]), "sgt1925": (ARK25, [26, 27])},
    "b": {"sgt1923": (ARK, [506, 507, 508]), "sgt1924": (ARK, [994, 995, 996]), "sgt1925": (ARK25, [28, 29, 30])},
    "cde": {"sgt1923": (ARK, [509]), "sgt1924": (ARK, [997]), "sgt1925": (ARK25, [31])},
    "fg": {"sgt1923": (ARK, [510, 511]), "sgt1924": (ARK, [998, 999]), "sgt1925": (ARK25, [32, 33])},
    "hi": {"sgt1923": (ARK, [512]), "sgt1924": (ARK, [1000]), "sgt1925": (ARK25, [34])},
    "jkl": {"sgt1923": (ARK, [513]), "sgt1924": (ARK, [1001]), "sgt1925": (ARK25, [35])},
    "m": {"sgt1923": (ARK, [514, 515]), "sgt1924": (ARK, [1002, 1003])},
    "nop": {"sgt1923": (ARK, [516]), "sgt1924": (ARK, [1004]), "sgt1925": (ARK25, [36])},
}

NAT = {"french": "Français", "italian": "Italiens", "maltese": "Maltais", "spanish": "Espagnols",
       "greek": "Grecs", "other_european": "Autres Européens", "muslim": "Musulmans",
       "jewish": "Israélites", "all_europeans": "Ensemble de la population européenne",
       "other": "Autres", "all_foreigners": "Étrangers (ensemble)"}
NAT6 = ["french", "italian", "maltese", "spanish", "greek", "other_european"]

CHECKS = collections.defaultdict(list)  # table -> [(label, ok, detail)]


def check(table, label, got, want):
    ok = got == want
    CHECKS[table].append((label, ok, "" if ok else f"computed {got} != printed {want}"))
    return ok


def lines(name):
    for ln in (T / name).read_text(encoding="utf-8").splitlines():
        if ln.strip() and not ln.startswith("#"):
            yield [x.strip() for x in ln.split("|")]


def ints(s):
    return [None if x == "-" else int(x.rstrip("*+")) for x in s.split()]


def marks(s):
    return [("ocr_corrected" if x.endswith("*") else "reprint_corrected" if x.endswith("+") else "")
            for x in s.split()]


def rec(table_id, page, view, **kw):
    r = {"census": SRC, "gallica_ark": ARK, "table_id": table_id, "source_page": page,
         "gallica_view": view, "census_year": kw.pop("census_year", 1921)}
    r.update(kw)
    r.setdefault("flag", "")
    return r


# ---------------------------------------------------------------- table a
def table_a():
    rows, tot = [], None
    for p in lines("cens1921_a_controle.txt"):
        area, pops, total, dens = int(p[2]), ints(p[3]), int(p[4]), float(p[5])
        if p[0] == "=":
            tot = (area, pops, total, dens)
            continue
        rows.append((p[1], area, pops, total, dens))
    groups = NAT6 + ["muslim", "jewish"]
    out = []
    for name, area, pops, total, dens in rows:
        ok = check("a", f"{name}: groups = total", sum(pops), total)
        check("a", f"{name}: density = total / area (truncated to 2 decimals)", int(total / area * 100) / 100, dens)
        out.append(rec("a", 2, 26, controle_civil=name, measure="area_km2", population_group="",
                       population_group_fr="", value=area))
        for g, v in zip(groups, pops):
            page, view = (2, 26) if g in ("french", "italian", "maltese", "spanish") else (3, 27)
            flag = "reprint_corrected" if g == "spanish" else ""
            if not ok:
                flag = "total_mismatch"
            out.append(rec("a", page, view, controle_civil=name, measure="population",
                           population_group=g, population_group_fr=NAT[g], value=v, flag=flag))
        out.append(rec("a", 3, 27, controle_civil=name, measure="density_per_km2", population_group="",
                       population_group_fr="", value=dens))
    check("a", "area column", sum(r[1] for r in rows), tot[0])
    for k, g in enumerate(groups):
        check("a", f"column {g}", sum(r[2][k] for r in rows), tot[1][k])
    check("a", "grand total", sum(r[3] for r in rows), tot[2])
    check("a", "national density (truncated)", int(tot[2] / tot[0] * 100) / 100, tot[3])
    return out, {"french": tot[1][0], "europeans": sum(tot[1][:6]), "pops": dict(zip(groups, tot[1])),
                 "rows": {r[0]: dict(zip(groups, r[2])) for r in rows}}


# ---------------------------------------------------------------- table b
def table_b(a_info):
    years = [1891, 1896, 1901, 1906, 1911, 1921]
    rows, tot = [], None
    for p in lines("cens1921_b_french_birthplace.txt"):
        if p[0] == "=":
            tot = ints(p[2])
            continue
        rows.append((int(p[0]), p[1], ints(p[2]), marks(p[2])))
    out = []
    for view, name, vals, fl in rows:
        for y, v, f in zip(years, vals, fl):
            out.append(rec("b", view - 24, view, census_year=y, birthplace_fr=name, value=v, flag=f))
    for k, y in enumerate(years):
        check("b", f"column {y}", sum(r[2][k] for r in rows), tot[k])
    check("b", "1921 column vs French total of table a", sum(r[2][5] for r in rows), a_info["french"])
    # 1891-1906 vs the 1906 census volume (Table E)
    te = {}
    for r in csv.DictReader(open(ROOT / "data-raw/colonial_census/csv/eur1906_te_french_by_birthplace_1891_1906.csv",
                                 encoding="utf-8-sig")):
        te.setdefault(r["birthplace_fr"], {})[int(r["census_year"])] = int(r["value"])
    alias = {"Eure-et-Loir": "Eure-et-Loire", "Ille-et-Vilaine": "Ile-et-Vilaine",
             "Loir-et-Cher": "Loire-et-Cher", "Rhin (Haut-), Belfort": "Rhin (Haut-) Belfort",
             "Colonies et Possessions françaises": "Colonies et Possessions Françaises",
             "Lieux inconnus": "Lieu inconnu"}
    diffs, n = [], 0
    for _, name, vals, _ in rows:
        t = te.get(alias.get(name, name))
        if t is None:
            continue
        for k, y in enumerate(years[:4]):
            n += 1
            if t[y] != vals[k]:
                diffs.append(f"{name} {y}: 1922 edition {vals[k]}, 1906 volume {t[y]}")
    return out, {"te_compared": n, "te_diffs": diffs}


# ---------------------------------------------------------------- tables c, d, e
def tables_cde():
    out_c, out_d, out_e = [], [], []
    d_rows, e_rows, d_tot, e_tot = [], [], None, None
    for p in lines("cens1921_cde_naturalised_foreign_birthplace.txt"):
        if p[0] == "c":
            m, f, t, orig, pct = p[1].split()
            m, f, t, orig = map(int, (m, f, t, orig))
            check("c", "male + female = total naturalised", m + f, t)
            out_c += [rec("c", 7, 31, category="naturalised", category_fr="Français par naturalisation",
                          sex="male", sex_fr="Sexe masculin", value=m),
                      rec("c", 7, 31, category="naturalised", category_fr="Français par naturalisation",
                          sex="female", sex_fr="Sexe féminin", value=f),
                      rec("c", 7, 31, category="french_by_origin",
                          category_fr="Population française d'origine", sex="", sex_fr="", value=orig)]
            c_tot = orig + t
        elif p[0] == "d":
            d_rows.append((p[1], ints(p[2])))
        elif p[0] == "d=":
            d_tot = ints(p[2])
        elif p[0] == "e":
            e_rows.append((p[1], ints(p[2])))
        elif p[0] == "e=":
            e_tot = ints(p[2])
    for k, y in enumerate((1911, 1921)):
        check("d", f"column {y}", sum(r[1][k] for r in d_rows), d_tot[k])
        check("e", f"column {y}", sum(r[1][k] for r in e_rows), e_tot[k])
        italy = dict(d_rows)["Italie"][k]
        check("e", f"total {y} = Italie in table d", e_tot[k], italy)
    for name, v in d_rows:
        for y, x in zip((1911, 1921), v):
            out_d.append(rec("d", 7, 31, census_year=y, birthplace_fr=name, value=x))
    for name, v in e_rows:
        for y, x in zip((1911, 1921), v):
            out_e.append(rec("e", 7, 31, census_year=y, province_fr=name, value=x))
    return out_c, out_d, out_e, c_tot


# ---------------------------------------------------------------- table f
AGE_F = {"lt20": "De moins de 20 ans", "20_39": "De 20 à 39 ans", "40plus": "De 40 ans et plus"}
MAR = [("single", "Célibataires"), ("married", "Mariés"), ("widowed_divorced", "Veufs et divorcés")]
SEX = [("male", "S. M."), ("female", "S. F.")]


def table_f(a_info):
    out, acc, subs = [], {}, {}
    for p in lines("cens1921_f_age_sex_marital.txt"):
        nat = p[0].split()[0]
        if "=" in p[0]:
            subs[nat] = (ints(p[1]), ints(p[2]))
            continue
        vals, fl = ints(p[2]), marks(p[2])
        acc[nat] = [a + b for a, b in zip(acc.get(nat, [0] * 6), vals)]
        for k, v in enumerate(vals):
            m, mfr = MAR[k // 2]
            s, sfr = SEX[k % 2]
            if nat == "ensemble":
                page, view = 8, 32
            elif nat == "french":
                page, view = (8, 32) if k < 4 else (9, 33)
            else:
                page, view = 9, 33
            n = "all_europeans" if nat == "ensemble" else nat
            out.append(rec("f", page, view, nationality=n, nationality_fr=NAT[n], age_group=p[1],
                           age_group_fr=AGE_F[p[1]], marital_status=m, marital_status_fr=mfr,
                           sex=s, sex_fr=sfr, value=v, flag=fl[k]))
    for nat, (sub, tot) in subs.items():
        for k in range(6):
            check("f", f"{nat} subtotal {MAR[k // 2][0]} {SEX[k % 2][0]}", acc[nat][k], sub[k])
        for j in range(3):
            check("f", f"{nat} total {MAR[j][0]}", sub[2 * j] + sub[2 * j + 1], tot[j])
    check("f", "all Europeans = table a Europeans", sum(subs["ensemble"][1]), a_info["europeans"])
    for nat in ("french", "italian", "maltese"):
        check("f", f"{nat} = table a", sum(subs[nat][1]), a_info["pops"][nat])
    return out, acc


# ---------------------------------------------------------------- table g
ECON = ["agriculture", "commerce", "industry", "transport"]
PUB = ["civil_service", "police_force", "liberal_professions"]
PROF_FR = {"agriculture": "Agriculteurs", "commerce": "Commerçants", "industry": "Industriels",
           "transport": "Transports", "civil_service": "Fonctionnaires", "police_force": "Force publique",
           "liberal_professions": "Professions libérales",
           "independent_means": "Personnes vivant exclusivement de revenus",
           "unclassified": "Population non classée"}
STATUS_FR = {"employer": "Patrons", "worker": "Ouvriers", "family": "Familles des patrons et ouvriers",
             "active": "Personnes exerçant la profession", "": ""}


def table_g():
    data = collections.defaultdict(dict)
    sub = collections.defaultdict(dict)
    for p in lines("cens1921_g_profession_nationality.txt"):
        nat, *kind = p[0].split()
        if kind:
            sub[nat][kind[0]] = [ints(x) for x in p[1:]]
        else:
            data[nat][p[1]] = (ints(p[2]), int(p[3]))
    out = []
    for nat, rows in data.items():
        for prof, (vals, tot) in rows.items():
            check("g", f"{nat} {prof} row total", sum(vals), tot)
        e = [sum(rows[x][0][k] for x in ECON) for k in range(3)]
        check("g", f"{nat} economic subtotal", e, sub[nat]["=econ"][0])
        check("g", f"{nat} economic total", sum(e), sub[nat]["=econ"][1][0])
        check("g", f"{nat} employers + workers", e[0] + e[1], sub[nat]["=econ"][2][0])
        pb = [sum(rows[x][0][k] for x in PUB) for k in range(2)]
        check("g", f"{nat} public subtotal", pb, sub[nat]["=public"][0])
        check("g", f"{nat} public total", sum(pb), sub[nat]["=public"][1][0])
        af = [e[0] + e[1] + pb[0], e[2] + pb[1]]
        check("g", f"{nat} active and family", af, sub[nat]["=active_family"][0])
        check("g", f"{nat} active and family total", sum(af), sub[nat]["=active_family"][1][0])
    for prof in ECON + PUB + ["independent_means", "unclassified"]:
        s = [sum(data[n][prof][0][k] for n in NAT6) for k in range(len(data["french"][prof][0]))]
        check("g", f"{prof}: nationalities = Ensemble", s, data["ensemble"][prof][0])
    for nat in NAT6:
        page, view = (8, 32) if nat in ("french", "italian", "maltese") else (9, 33)
        for prof, (vals, _) in data[nat].items():
            if prof in ECON:
                parts = list(zip(["employer", "worker", "family"], [""] * 3, vals))
            elif prof in PUB:
                parts = list(zip(["active", "family"], [""] * 2, vals))
            else:
                parts = list(zip(["", ""], ["male", "female"], vals))
            for st, sx, v in parts:
                flag = "total_mismatch" if prof == "police_force" and st == "family" else ""
                out.append(rec("g", page, view, nationality=nat, nationality_fr=NAT[nat], profession=prof,
                               profession_fr=PROF_FR[prof], status=st, status_fr=STATUS_FR[st], sex=sx,
                               sex_fr={"male": "S. M.", "female": "S. F.", "": ""}[sx], value=v, flag=flag))
    return out, data


# ---------------------------------------------------------------- tables h to l
def tables_hijkl(a_info, f_acc, c_tot):
    H, I, JF, JE, K, L1, L2 = [], [], [], [], [], [], []
    h_rows, h_tot, jf_rows, je_rows, je_tot, k_rows, k_tot = [], None, [], [], None, [], None
    l1_rows, l1_tot, l2_rows, l2_tot = [], None, [], None
    for p in lines("cens1921_hijkl.txt"):
        t = p[0]
        if t == "h":
            h_rows.append((p[1], ints(p[2]), int(p[3])))
        elif t == "h=":
            h_tot = (ints(p[2]), int(p[3]))
        elif t == "i":
            I.append(rec("i", 10, 34, nationality=p[1], nationality_fr=NAT[p[1]], measure="illiterate",
                         value=int(p[2])))
        elif t == "jF":
            jf_rows.append((p[1], int(p[2])))
        elif t == "jF=":
            jf_tot = int(p[2])
        elif t == "jE":
            je_rows.append((p[1], int(p[2]), int(p[3])))
        elif t == "jE=":
            je_tot = (int(p[2]), int(p[3]), ints(p[4]))
        elif t == "k":
            k_rows.append((p[1], ints(p[2])))
        elif t == "k=":
            k_tot = ints(p[2])
        elif t == "l1":
            l1_rows.append((p[1], ints(p[2]), int(p[3])))
        elif t == "l1=":
            l1_tot = (ints(p[2]), int(p[3]))
        elif t == "l2":
            l2_rows.append((p[1], ints(p[2])))
        elif t == "l2=":
            l2_tot = ints(p[2])
    # h
    hn = NAT6
    for prof, vals, tot in h_rows:
        check("h", f"{prof} nationalities = Ensemble", sum(vals), tot)
        for n, v in zip(hn, vals):
            H.append(rec("h", 10, 34, nationality=n, nationality_fr=NAT[n], profession=prof,
                         profession_fr=PROF_FR[prof].replace("Agriculteurs", "Agriculture")
                         .replace("Commerçants", "Commerce").replace("Industriels", "Industrie")
                         .replace("Transports", "Transport"), sex="female", value=v))
    for k, n in enumerate(hn):
        check("h", f"column {n}", sum(r[1][k] for r in h_rows), h_tot[0][k])
    check("h", "Ensemble column", sum(r[2] for r in h_rows), h_tot[1])
    # j
    check("j", "French birthplaces = total", sum(v for _, v in jf_rows), jf_tot)
    check("j", "French total = table a", jf_tot, a_info["french"])
    bp = {"Tunisie": "tunisia", "Algérie": "algeria", "France": "france", "Etranger": "abroad",
          "Possessions françaises": "french_possessions"}
    for name, v in jf_rows:
        JF.append(rec("j", 11, 35, nationality="french", nationality_fr="Français", birthplace=bp[name],
                      birthplace_fr=name, value=v))
    check("j", "foreign population", sum(r[1] for r in je_rows), je_tot[0])
    check("j", "foreigners born outside North Africa", sum(r[2] for r in je_rows), je_tot[1])
    check("j", "foreigners: outside + North Africa = total", je_tot[1] + je_tot[2][2], je_tot[0])
    check("j", "foreigners born in Tunisia + Algeria = North Africa", je_tot[2][0] + je_tot[2][1], je_tot[2][2])
    jn = {"Italiens": "italian", "Maltais": "maltese", "Autres": "other"}
    for name, pop, outside in je_rows:
        JE.append(rec("j", 11, 35, nationality=jn[name], nationality_fr=name,
                      birthplace="italy_malta_or_outside_north_africa",
                      birthplace_fr="Nés en Italie, à Malte et hors de l'Afrique du Nord", value=outside))
    JE.append(rec("j", 11, 35, nationality="all_foreigners", nationality_fr="Étrangers", birthplace="tunisia",
                  birthplace_fr="Nés en Tunisie", value=je_tot[2][0]))
    JE.append(rec("j", 11, 35, nationality="all_foreigners", nationality_fr="Étrangers", birthplace="algeria",
                  birthplace_fr="Nés en Algérie", value=je_tot[2][1]))
    # k
    kn = ["all_europeans", "french", "italian", "maltese"]
    kfr = {"0_9": "0 à 9 ans", "10_19": "10 à 19", "20_29": "20 à 29", "30_39": "30 à 39",
           "40_49": "40 à 49", "50_59": "50 à 59", "60plus": "60 ans et plus"}
    for k, n in enumerate(kn):
        check("k", f"column {n}", sum(r[1][k] for r in k_rows), k_tot[k])
    check("k", "all Europeans = table a", k_tot[0], a_info["europeans"])
    for age, vals in k_rows:
        for n, v in zip(kn, vals):
            K.append(rec("k", 11, 35, nationality=n, nationality_fr=NAT[n], age_group=age,
                         age_group_fr=kfr[age], value=v))
    # l
    lfr = {"single": "Célibataires", "married": "Mariés", "widowed": "Veufs", "divorced": "Divorcés"}
    for ms, (m, f), tot in l1_rows:
        ok = check("l", f"{ms}: male + female", m + f, tot)
        for sx, v in (("male", m), ("female", f)):
            L1.append(rec("l", 11, 35, nationality="all_europeans", nationality_fr=NAT["all_europeans"],
                          marital_status=ms, marital_status_fr=lfr[ms], sex=sx,
                          sex_fr={"male": "Sexe masculin", "female": "Sexe féminin"}[sx], value=v,
                          flag="" if ok or sx == "female" else "total_mismatch"))
    for k in range(2):
        check("l", f"marital status column {SEX[k][0]}", sum(r[1][k] for r in l1_rows), l1_tot[0][k])
        check("l", f"nationality column {SEX[k][0]}", sum(r[1][k] for r in l2_rows), l2_tot[k])
    check("l", "single males = table f", dict((r[0], r[1]) for r in l1_rows)["single"][0],
          f_acc["ensemble"][0])
    pops = a_info["pops"]
    for nat, (m, f) in l2_rows:
        want = pops.get(nat, sum(pops[x] for x in ("spanish", "greek", "other_european")))
        ok = check("l", f"{nat}: male + female = table a", m + f, want)
        for sx, v in (("male", m), ("female", f)):
            L2.append(rec("l", 11, 35, nationality=nat, nationality_fr=NAT[nat], marital_status="",
                          marital_status_fr="", sex=sx,
                          sex_fr={"male": "Sexe masculin", "female": "Sexe féminin"}[sx], value=v,
                          flag="" if ok or sx == "female" else "total_mismatch"))
    return H, I, JF + JE, K, L1 + L2


# ---------------------------------------------------------------- table m
def table_m(a_info):
    natm = NAT6
    rows, tot = [], None
    for p in lines("cens1921_m_circonscription_1911_1921.txt"):
        left, right = "|".join(p).split("||")
        q = [x.strip() for x in left.split("|")]
        vals = [ints(x) for x in q[2:9]]
        mv = ints(right.strip(" |"))
        if q[0] == "=":
            tot = (vals, mv)
            continue
        rows.append((q[1], vals, mv))
    out = []
    for name, vals, mv in rows:
        for y in (0, 1):
            check("m", f"{name} {(1911, 1921)[y]} nationalities = total",
                  sum(vals[k][y] for k in range(6)), vals[6][y])
        check("m", f"{name} French 1911/1921 = movement columns", [vals[0][0], vals[0][1]], mv[4:6])
        key = name.replace(" (1)", "")
        if key in a_info["rows"]:
            for k, n in enumerate(natm):
                check("m", f"{name} 1921 {n} = table a", vals[k][1], a_info["rows"][key][n])
        for k, n in enumerate(natm):
            for y, yr in ((0, 1911), (1, 1921)):
                page, view = (12, 36) if k < 4 else (13, 37)
                flag = "reprint_corrected" if (n == "spanish" and yr == 1921) else ""
                out.append(rec("m", page, view, census_year=yr, controle_civil=key, nationality=n,
                               nationality_fr=NAT[n], value=vals[k][y], flag=flag))
        for j, yr in enumerate((1891, 1896, 1901, 1906)):
            out.append(rec("m", 13, 37, census_year=yr, controle_civil=key, nationality="french",
                           nationality_fr="Français (mouvement de la population française)", value=mv[j]))
    for k in range(7):
        for y, yr in ((0, 1911), (1, 1921)):
            check("m", f"column {k} {yr}", sum(r[1][k][y] for r in rows), tot[0][k][y])
    for j in range(6):
        check("m", f"French movement column {j}", sum(r[2][j] for r in rows), tot[1][j])
    # French 1891-1906 by circonscription vs the 1906 census volume (Table B)
    tb = {}
    for r in csv.DictReader(open(ROOT / "data-raw/colonial_census/csv/eur1906_tb_french_population_1891_1906.csv",
                                 encoding="utf-8-sig")):
        tb.setdefault(r["controle_civil"], {})[int(r["census_year"])] = int(r["value"])
    alias = {"Kef (Le)": "Le Kef", "Téboursouk": "Teboursouk"}
    n_eq = n = 0
    for name, _, mv in rows:
        t = tb.get(alias.get(name, name))
        if not t:
            continue
        for j, yr in enumerate((1891, 1896, 1901, 1906)):
            n += 1
            n_eq += check("m", f"{name} French {yr} = 1906 volume Table B", mv[j], t[yr])
    return out, (n_eq, n)


# ---------------------------------------------------------------- tables n, o, p
def tables_nop(a_info):
    years = [1881, 1886, 1891, 1896, 1901, 1906, 1911, 1921]
    N, O, P = [], [], []
    n_rows, n_tot = [], None
    for p in lines("cens1921_nop.txt"):
        t = p[0]
        if t == "n":
            n_rows.append((p[1], ints(p[2])))
        elif t == "n=":
            n_tot = ints(p[2])
        elif t == "o":
            vals, eur, mj, tot = ints(p[2]), int(p[3]), ints(p[4]), int(p[5])
            ok = check("o", f"{p[1]} nationalities = European total", sum(vals), eur)
            check("o", f"{p[1]} European + Muslim + Jewish = total", eur + sum(mj), tot)
            for n, v in zip(NAT6 + ["muslim", "jewish"], vals + mj):
                O.append(rec("o", 14, 38, town=p[1], population_group=n, population_group_fr=NAT[n],
                             value=v, flag="" if ok or n in ("muslim", "jewish") else "total_mismatch"))
        elif t == "p":
            vals, tot = ints(p[4]), int(p[5])
            ok = check("p", f"{p[3]} nationalities = total", sum(vals), tot)
            for n, v in zip(NAT6, vals):
                P.append(rec("p", 14, 38, town=p[3], size_class=p[1],
                             size_class_fr={"gt1000": "Plus de 1.000 habitants",
                                            "500_1000": "De 500 à 1.000 habitants"}[p[1]],
                             town_rank=int(p[2]), nationality=n, nationality_fr=NAT[n], value=v,
                             flag="" if ok else "total_mismatch"))
    for k, yr in enumerate(years):
        col = [r[1][k] for r in n_rows if r[1][k] is not None]
        ok = check("n", f"column {yr}", sum(col), n_tot[k])
        for name, vals in n_rows:
            if vals[k] is None:
                continue
            fr = NAT[name]
            if yr == 1901 and name == "other_european":
                fr = "Espagnols, Grecs, Autres européens"
            N.append(rec("n", 14, 38, census_year=yr, nationality=name, nationality_fr=fr, value=vals[k],
                         flag="" if ok else "total_mismatch"))
    check("n", "1921 = table a", [r[1][7] for r in n_rows], [a_info["pops"][x] for x in NAT6])
    # Bizerte's Italians: table o vs table p
    o_biz = [r["value"] for r in O if r["town"] == "Bizerte" and r["population_group"] == "italian"][0]
    p_biz = [r["value"] for r in P if r["town"] == "Bizerte" and r["nationality"] == "italian"][0]
    check("o", "Bizerte Italians: table o = table p", o_biz, p_biz)
    return N, O, P


# ---------------------------------------------------------------- reprint comparison
def page_numbers(ark, view):
    """All numbers Gallica's OCR reads on a page (» and similar = 0)."""
    nums = collections.Counter()
    for w in ocr.words(ark, view):
        t = w["text"].strip("!|;:'_()[]{}").rstrip(".")
        if t in ("»", "))", "»»", "»."):
            nums[0] += 1
            continue
        t = t.replace(",", ".")
        if re.fullmatch(r"\d{1,3}(\.\d{3})*", t):
            nums[int(t.replace(".", ""))] += 1
        elif re.fullmatch(r"\d+\.\d{1,2}", t):  # decimals (densities)
            nums[float(t)] += 1
    return nums


def compare_reprints(group, records):
    """Per reprint edition: how many of the extracted cells are found on the reprint page."""
    res = {}
    for ed, (ark, views) in REPRINTS[group].items():
        recs = records
        if ed == "sgt1925" and group in ("b", "cde"):
            # the 1925 edition reprints only the 1921 column of tables b, d and e
            recs = [r for r in records if r["census_year"] == 1921]
        want = collections.Counter(r["value"] for r in recs if r["value"] is not None)
        have = collections.Counter()
        for v in views:
            have += page_numbers(ark, v)
        found = sum(min(c, have[x]) for x, c in want.items())
        missing = []
        for x, c in sorted(want.items(), key=lambda kv: str(kv[0])):
            if have[x] < c:
                missing.append((x, c - have[x]))
        res[ed] = {"views": views, "cells": sum(want.values()), "found": found, "missing": missing}
    return res


# ---------------------------------------------------------------- output
def write(name, rows):
    cols = []
    for r in rows:
        for k in r:
            if k not in cols:
                cols.append(k)
    order = ["census", "gallica_ark", "table_id", "source_page", "gallica_view", "census_year"]
    cols = order + [c for c in cols if c not in order and c not in ("value", "flag")] + ["value", "flag"]
    with open(OUT / f"{name}.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, cols, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k, "")) for k in cols})
    return len(rows)

TABLES = {}
VISUAL = {
    "a": "sgt1923 (views 504-505) and sgt1924 (views 992-993): every cell compared on the images, all equal; the Spanish column, lost in the sgt1922 gutter, is legible in both and identical. sgt1925 (views 26-27): equal where the OCR reads it.",
    "b": "sgt1923 and sgt1924 reprint all six census columns; sgt1925 reprints the 1921 column only. Compared through the OCR; every cell the OCR misses was checked on sgt1922 at native resolution.",
    "cde": "sgt1923 (view 509), sgt1924 (view 997) and sgt1925 (view 31, 1921 column only): every cell compared on the images, all equal.",
    "fg": "sgt1923 (views 510-511), sgt1924 (views 998-999) and sgt1925 (views 32-33): every cell compared on the images, all equal. They are the same typesetting, including the police-force misprint.",
    "hi": "sgt1923 (view 512), sgt1924 (view 1000) and sgt1925 (view 34): every cell compared on the images, all equal.",
    "jkl": "sgt1923 (view 513), sgt1924 (view 1001) and sgt1925 (view 35): every cell compared on the images, all equal, including the misprints 44.300 and 1.901.",
    "m": "sgt1923 (views 514-515): every cell compared on the images, all equal, including the Maltese 1921 total misprint (11.520). sgt1924 (views 1002-1003): compared through the OCR. Not reprinted in sgt1925.",
    "nop": "sgt1923 (view 516) and sgt1924 (view 1004): every cell compared on the images, all equal, including the misprints. sgt1925 (view 36): compared through the OCR.",
}
NOTES = {
 "cens1921_controle_population": ("a) Superficie, populations (européenne et indigène) et densité de la population par circonscription de Contrôle civil",
   "Area, population (European and indigenous) and population density by contrôle civil, 1921 census", "2-3", "26-27",
   "`measure`: `area_km2`, `population` or `density_per_km2` (inhabitants per km², as printed, two decimals). For `population`, `population_group` gives the nationality or religion.",
   ["The Spanish column falls in the gutter of the sgt1922 spread; its values were read from sgt1923 (flag `reprint_corrected`) and are identical in sgt1924.",
    "Thala and Tunis: the printed totals (88.267, 269.312) differ from the sum of their groups (88.167, 269.412) by +100 and -100; the grand total agrees with the groups. Every cell of both rows is kept as printed and flagged `total_mismatch`.",
    "The area column sums to 125.130 km², 50 less than the printed 125.180.",
    "Densities are truncated, not rounded, to two decimals; Sousse prints 43,46 where 269.534/6.200 = 43,47."]),
 "cens1921_french_birthplace_1891_1921": ("b) Population civile française d'après le lieu de naissance (recensements de 1891 à 1921)",
   "French civilian population by place of birth (Tunisia, Algerian départements, French départements, colonies, abroad), censuses 1891-1921", "4-6", "28-30",
   "`birthplace_fr` as printed; `census_year` the census.",
   ["(1) Moselle and Bas-Rhin were counted with the foreign population for 1891-1911 (printed as », stored 0).",
    "(2) Colonies and possessions other than Algeria and Tunisia. \"Lieux inconnus\" was used only in 1906.",
    "The 1921 grand total reads 54.426 in the half-resolution scan and in Gallica's OCR; at native resolution it is 54.476, which the column sums to and which equals the French total of table a).",
    "Five cells misread by the OCR were corrected from the image (`ocr_corrected`)."]),
 "cens1921_french_naturalised": ("c) Français par naturalisation", "French by naturalisation, 1921", "7", "31",
   "`category`: `naturalised` (by sex) or `french_by_origin`. The printed proportion (5,8 % = naturalised / French by origin) is not stored.", []),
 "cens1921_foreign_birthplace_1911_1921": ("d) Population étrangère d'après le lieu de naissance", "Foreign population by place of birth, 1911 and 1921", "7", "31",
   "`birthplace_fr` as printed (Africa sub-rows prefixed \"Afrique : \").",
   ["(1) Alsace-Lorraine: counted with the French population in 1921.", "(2) Italy: by province in table e)."]),
 "cens1921_italian_provinces_1911_1921": ("e) Répartition par province des habitants originaires de l'Italie", "Residents born in Italy by Italian province, 1911 and 1921", "7", "31",
   "`province_fr` as printed.", []),
 "cens1921_age_sex_marital": ("f) Population européenne d'après l'âge, le sexe et l'état civil", "European population by age group, sex and marital status, by nationality, 1921", "8-9", "32-33",
   "`nationality` = `all_europeans` (\"Ensemble de la population, compris européens non dénommés\"), `french`, `italian` or `maltese`. Widowed and divorced are printed together.",
   ["French married women (three cells) are lost in the sgt1922 gutter; read from sgt1923 (`reprint_corrected`).",
    "The printed percentages by marital status are not stored."]),
 "cens1921_profession_nationality": ("g) Population européenne par profession et nationalité (sexes réunis)", "European population by profession, status and nationality, both sexes, 1921", "8-9", "32-33",
   "`status`: for agriculture, commerce, industry and transport, `employer` (patrons), `worker` (ouvriers) or `family` (families of employers and workers); for civil service, police and liberal professions, `active` or `family`. For people living on independent means and the unclassified population, `sex` is given instead. Printed subtotals are not stored.",
   ["Police force (Force publique), family: the six nationalities sum to 1.183, but the Ensemble column prints 1.186 (and its total 1.708). Kept as printed; the family cells of that row are flagged `total_mismatch`."]),
 "cens1921_profession_female": ("h) Population européenne par profession et nationalité (sexe féminin)", "Women by profession and nationality, 1921", "10", "34",
   "Women exercising a profession, by category.", []),
 "cens1921_illiterates": ("i) Nombre et proportion des européens illettrés", "Number of illiterate Europeans, 1921", "10", "34",
   "`all_europeans` includes the nationalities not listed. The printed proportions (15,5; 50,3; 50,9; 37,7 %) are not stored.", []),
 "cens1921_birthplace_recap": ("j) Récapitulation de la population européenne d'après le lieu de naissance", "Europeans by place of birth: French by birthplace, foreigners born outside North Africa, in Tunisia and in Algeria, 1921", "11", "35",
   "For foreigners, the split by nationality is printed only for those born in Italy, Malta or outside North Africa; births in Tunisia and Algeria are printed for all foreigners together (`all_foreigners`).", []),
 "cens1921_age_nationality": ("k) Population européenne d'après l'âge", "European population by age group and nationality, 1921", "11", "35",
   "Ages 0-2 and 2-9 are bracketed into one printed value (`0_9`). The printed proportions are not stored.", []),
 "cens1921_sex_marital_nationality": ("l) Population européenne d'après le sexe et l'état civil et par nationalité d'après le sexe", "European population by sex and marital status, and by nationality and sex, 1921", "11", "35",
   "Rows with `marital_status` give the first panel; rows with empty `marital_status` the second (by nationality).",
   ["Single males are printed 44.300; the row total (85.757), the column total (76.830) and table f) (44.309) all require 44.309.",
    "\"Autres\" males are printed 1.901; the column total (76.830) and table a) (3.320 other Europeans) require 1.701.",
    "Both are identical in every reprint. Kept as printed, flagged `total_mismatch`."]),
 "cens1921_circonscription_1911_1921": ("m) Recensements de 1911 et de 1921 par circonscription administrative (population européenne)", "Europeans by circonscription and nationality, 1911 and 1921, with the French population 1891-1921", "12-13", "36-37",
   "`census_year` 1911 or 1921 for all nationalities; the rows for 1891-1906 are the French population (\"Mouvement de la population française\"). The 1911 and 1921 French columns equal the movement columns and are stored once.",
   ["(1) In 1911 the population of the contrôle civil of Zaghouan was counted with Tunis (», stored 0).",
    "The Maltese 1921 column total is printed 11.520 (also in sgt1923); the column sums to 13.520, which tables a) and n) give.",
    "Spanish 1921 is in the gutter; values equal table a) (`reprint_corrected`)."]),
 "cens1921_europeans_1881_1921": ("n) Population européenne par période quinquennales (1881-1921)", "European population by nationality, 1881-1921", "14", "38",
   "No breakdown of Spanish, Greek and other Europeans before 1906; in 1901 the three are printed as one bracketed value (3.214), stored as `other_european` with `nationality_fr` \"Espagnols, Grecs, Autres européens\".",
   ["(1) 1881: registers of the French consulates before the Protectorate. (2) 1886: trial census. (3) From 1891: quinquennial censuses.",
    "(4) For all foreigners, until 1898 (when the control of foreigners was instituted) the figures were supplied by the consulates or established empirically; for 1901 the Sûreté publique figure from the register of foreigners' declarations; from 1906 the quinquennial censuses.",
    "1901: the cells sum to 111.071, 30 less than the printed total 111.101; the 1901 cells are flagged `total_mismatch`."]),
 "cens1921_five_largest_towns": ("o) Population des cinq plus grandes villes, avec répartition d'après la nationalité", "European and indigenous population of the five largest towns, 1921", "14", "38",
   "`population_group`: European nationalities, `muslim`, `jewish`.",
   ["Bizerte: Italians printed 3.139 here but 3.149 in table p); the printed European total 6.809 requires 3.149. Kept as printed; Bizerte's European cells are flagged `total_mismatch`."]),
 "cens1921_towns_european_population": ("p) Population européenne des villes comptant 1° plus de 1.000 habitants, 2° de 500 à 1.000 habitants", "European population of towns with over 1,000 and 500-1,000 Europeans, 1921", "14", "38",
   "`size_class` and `town_rank` as printed.",
   ["Souk-el-Khemis: the cells sum to 474 against a printed total of 584 (checked at native resolution and in two reprints). Kept as printed, flagged `total_mismatch`."]),
}


def write_notes(report):
    for name, (fr, en, pages, views, cols, extra) in NOTES.items():
        r = report[name]
        grp = {v[0]: v[2] for v in TABLES.values()}
        lines = [f"# {name}", "", f"**{fr}**  ", f"*{en}*", "",
                 f"Source: *Statistique générale de la Tunisie*, 1922 edition (sgt1922), chapter I *Démographie*, "
                 f"printed pages {pages}, Gallica views {views} of ark `{ARK}`. {CREDIT}.", "",
                 f"{r['rows']} rows, one per printed cell. {cols}", "",
                 "Common columns: `census` (source edition), `gallica_ark`, `table_id`, `source_page`, `gallica_view`, "
                 "`census_year`, `value` (printed figure; » = 0), `flag` (see SPEC.md and SPEC_ADDENDUM.md).", "",
                 "## Validation", "",
                 f"{r['passed']} of {r['checks']} automated checks pass (printed row, column and grand totals, and "
                 "cross-checks with the other 1921 tables and the 1906 census volume)."]
        for x in r["failed"]:
            lines.append(f"- failing: {x} (re-read on the scan at native resolution; printed values kept)")
        if r.get("vs_1906_volume"):
            v = r["vs_1906_volume"]
            lines.append(f"- 1891-1906 columns vs the 1906 census volume (Table E): {v['te_compared']} cells compared, "
                         f"{v['te_compared'] - len(v['te_diffs'])} equal. Differences: " + "; ".join(v["te_diffs"]) + ". "
                         "Each year's differences add up exactly to the gap between the 1906 volume's departement "
                         "rows and its printed total (1891 +8, 1896 +10, 1901 -30, 1906 -151): the 1922 compilers "
                         "appear to have made the old columns add up by adjusting one or a few cells, so these "
                         "values are not independent evidence. The 1906 volume's commentary (pp.44-45) gives "
                         "Bouches-du-Rhône 922 (supports this edition), but also Gironde 324 with +58 since 1901 and "
                         "Var +147 since 1901 to 403, i.e. 256 in 1901 (both support the 1906 volume). Calvados, "
                         "Var 1891 and Etranger 1896 cannot be checked against an independent source. Values are "
                         "kept as printed in this edition and not flagged; for 1891-1906 prefer the 1906 volume's "
                         "Table E (eur1906_te_french_by_birthplace_1891_1906), whose notes discuss the same cells.")
        if r.get("vs_1906_volume_table_b"):
            a, b = r["vs_1906_volume_table_b"]
            lines.append(f"- French 1891-1906 by circonscription vs the 1906 census volume (Table B): {a} of {b} cells equal.")
        lines += ["", "## Reprints", "", VISUAL[[t for t, (tid, _, g) in TABLES.items() if t == name][0] and TABLES[name][2]], "",
                  "OCR check (cells whose value occurs among the numbers Gallica's OCR reads on the reprint page; "
                  "misses are OCR gaps, not differences):"]
        for ed, x in r["reprints"].items():
            lines.append(f"- {ed} (views {', '.join(map(str, x['views']))}): {x['found']} of {x['cells']}")
        if extra:
            lines += ["", "## Notes and footnotes", ""] + [f"- {x}" for x in extra]
        (OUT / f"{name}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    OUT.mkdir(exist_ok=True)
    a, a_info = table_a()
    b, b_info = table_b(a_info)
    c, d, e, c_tot = tables_cde()
    check("c", "French by origin + naturalised = table a French", c_tot, a_info["french"])
    f, f_acc = table_f(a_info)
    g, _ = table_g()
    h, i, j, k, l = tables_hijkl(a_info, f_acc, c_tot)
    m, m_tb = table_m(a_info)
    n, o, p = tables_nop(a_info)
    global TABLES
    tables = {
        "cens1921_controle_population": ("a", a, "a"),
        "cens1921_french_birthplace_1891_1921": ("b", b, "b"),
        "cens1921_french_naturalised": ("c", c, "cde"),
        "cens1921_foreign_birthplace_1911_1921": ("d", d, "cde"),
        "cens1921_italian_provinces_1911_1921": ("e", e, "cde"),
        "cens1921_age_sex_marital": ("f", f, "fg"),
        "cens1921_profession_nationality": ("g", g, "fg"),
        "cens1921_profession_female": ("h", h, "hi"),
        "cens1921_illiterates": ("i", i, "hi"),
        "cens1921_birthplace_recap": ("j", j, "jkl"),
        "cens1921_age_nationality": ("k", k, "jkl"),
        "cens1921_sex_marital_nationality": ("l", l, "jkl"),
        "cens1921_circonscription_1911_1921": ("m", m, "m"),
        "cens1921_europeans_1881_1921": ("n", n, "nop"),
        "cens1921_five_largest_towns": ("o", o, "nop"),
        "cens1921_towns_european_population": ("p", p, "nop"),
    }
    TABLES = tables
    report = {}
    for name, (tid, rows, grp) in tables.items():
        nrows = write(name, rows)
        chk = CHECKS[tid]
        report[name] = {"table": tid, "rows": nrows, "checks": len(chk), "passed": sum(x[1] for x in chk),
                        "failed": [f"{x[0]}: {x[2]}" for x in chk if not x[1]],
                        "flags": dict(collections.Counter(r["flag"] for r in rows if r["flag"])),
                        "reprints": compare_reprints(grp, rows)}
    report["cens1921_french_birthplace_1891_1921"]["vs_1906_volume"] = b_info
    report["cens1921_circonscription_1911_1921"]["vs_1906_volume_table_b"] = m_tb
    write_notes(report)
    json.dump(report, open(HERE / "cens1921_validation.json", "w", encoding="utf-8"), ensure_ascii=False,
              indent=1, default=str)
    for name, r in report.items():
        rp = ", ".join(f"{ed} {x['found']}/{x['cells']}" for ed, x in r["reprints"].items())
        print(f"{name}: {r['rows']} rows; checks {r['passed']}/{r['checks']}; flags {r['flags']}; reprints {rp}")
        for x in r["failed"]:
            print("   FAIL", x)


if __name__ == "__main__":
    main()
