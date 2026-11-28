#!/usr/bin/env python3
"""Canoun des dattiers and canoun des oliviers (tax on date palms and olive trees), from the Finances chapter of the
Statistique générale de la Tunisie, editions sgt1922-sgt1930 and sgt1935.

  python3 extract_finance_canoun.py check   parse the transcriptions, run every check, print failures
  python3 extract_finance_canoun.py build   ... and write csv/finance_canoun_*.csv, their .md notes,
                                            csv/finance_canoun_survey.md and csv/finance_canoun_validation.json

Source of truth: transcribed/finance_canoun_<edition>.txt (format in yb_tables.py; printed » written 0). Sections:

  dattiers_age     a) relevé par caïdat du nombre d'arbres d'après leur âge (kind=degla|communs; one section per
                   view of the spread, rows matched by label). cols m (Mâles), a0 (moins d'un an), a1..a19,
                   tj (Total des jeunes, check), imp (20 ans imposables), tot (Total, check)
  dattiers_tariff  b) répartition des arbres imposables par catégorie du tarif (kind=degla|communs,
                   tariffs="label;label;..." = the printed column heads). cols t1..tN, tot (check)
  dattiers_roll    c) répartition entre les européens et les indigènes. cols e_dg_i e_dg_n e_cm_i e_cm_n i_dg_i
                   i_dg_n i_cm_i i_cm_n (roll x kind x imposés / non imposés), ar_e ar_i ar_t (articles de
                   matrice), co_e co_i co_t (comptes individuels); *_t = TOTAL, check
  oliviers_age     a), as dattiers_age with sv (arbres sauvages) for m
  oliviers_tariff  b), cols t1..tN (tariffs="..."), dime (anciens pays à dîme, impôt proportionnel au revenu
                   global), tot (check)
  oliviers_roll    c), cols imp_e imp_i imp_t non_e non_i non_t (nombre d'arbres imposés / non imposés by roll),
                   ar_e ar_i ar_t, co_e co_i co_t

Stored: every printed cell except the TOTAL columns and the Totaux lines (checks).
"""
import re
import sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # shared helper yb_tables.py
from yb_tables import (COMMON, EDITIONS, ORDER, OUT, TR, Checks, coverage_lines, is_total, parse, ssum,
                       write_csv, write_notes, write_validation)

CHAPTER = "Finances"
SCRIPT = "extract_finance_canoun.py"
PREFIX = "finance_canoun"
EDS = ["sgt1922", "sgt1923", "sgt1924", "sgt1925", "sgt1926", "sgt1927", "sgt1928", "sgt1929", "sgt1930",
       "sgt1935"]

CHK = Checks()

# ----------------------------------------------------------------- labels

KIND = {"degla": ("degla", "Dattiers degla"), "communs": ("common", "Dattiers communs")}
AGE = {"m": ("male", "Mâles"), "sv": ("wild", "Arbres sauvages"), "a0": ("under_1", "Moins d'un an"),
       "a1": ("age_01", "1 an")}
for _i in range(2, 20):
    AGE[f"a{_i}"] = (f"age_{_i:02d}", f"{_i} ans")
AGE["imp"] = ("taxable_20_plus", "20 ans imposables")
AGES = [f"a{i}" for i in range(20)]
ROLL = {"e": ("european", "Européens"), "i": ("indigenous", "Indigènes")}
STATUS = {"i": ("taxed", "Imposés"), "n": ("not_taxed", "Non imposés")}
MEASURE = {"trees": ("Nombre d'arbres", "trees"), "articles": ("Nombre d'articles de matrice", "articles"),
           "accounts": ("Nombre de comptes individuels", "accounts")}
DIME_FR = "Anciens pays à dîme. Impôt proportionnel au revenu global"

TITLES = {
    "dattiers_age": "Canoun des dattiers. a) Relevé par caïdat du nombre d'arbres d'après leur âge",
    "dattiers_tariff": "Canoun des dattiers. b) Répartition des arbres imposables par catégorie du tarif",
    "dattiers_roll": "Canoun des dattiers. c) Répartition des dattiers entre les européens et les indigènes",
    "oliviers_age": "Canoun des oliviers. a) Relevé par caïdat du nombre d'arbres d'après leur âge",
    "oliviers_tariff": "Canoun des oliviers. b) Répartition des arbres imposables par catégorie du tarif",
    "oliviers_roll": "Canoun des oliviers. c) Répartition entre les européens et les indigènes",
}

# Cells identified by the checks as the faulty one (printed value kept): (edition, table, kind, label, col) -> flag
FLAGS = {
    ("sgt1922", "oliviers_tariff", "", "Monastir", "t6"): "total_mismatch",
    ("sgt1923", "oliviers_age", "", "Cap-Bon - Soliman", "a15"): "row_realigned",
    ("sgt1923", "oliviers_age", "", "Cap-Bon - Nabeul", "a15"): "row_realigned",
}
# editions whose c) counts the dattiers communs non imposés without the male palms (= a) Total des jeunes)
COMMUNS_NO_MALES = {"sgt1928"}
# Whole printed lines stored under another caïdat (flag row_realigned on every cell, unless FLAGS says otherwise)
FLAG_ROWS = {
    ("sgt1923", "oliviers_tariff", "", "Fraichiches"): "row_realigned",
    ("sgt1923", "oliviers_tariff", "", "Majeur"): "row_realigned",
}
FLAGS[("sgt1923", "oliviers_tariff", "", "Majeur", "t9")] = "total_mismatch"
FLAGS[("sgt1924", "oliviers_tariff", "", "Monastir", "t4")] = "total_mismatch"
FLAGS[("sgt1924", "oliviers_tariff", "", "Ouled-Aoun", "t5")] = "total_mismatch"
FLAGS[("sgt1925", "dattiers_age", "communs", "Territoires militaires ;  ; Nefzaoua", "a0")] = "total_mismatch"
FLAGS[("sgt1925", "dattiers_roll", "", "Territoires militaires ;  ; Nefzaoua", "i_cm_i")] = "total_mismatch"
for _l, _c in (("3me Région (Le Kef) ; Téboursouk ; Téboursouk", "a2"), ("1re Région (Bizerte) ; Bizerte ; Mateur", "a18"),
               ("1re Région (Bizerte) ; Souk-el-Arba ; Souk-el-Khemis", "a18"),
               ("2me Région (Tunis) ; Zaghouan ; Zaghouan", "a14"), ("4me Région (Sousse) ; Sousse ; Souassi", "a19"),
               ("5me Région (Sfax) ; Sfax ; Djebéniana", "a19"), ("5me Région (Sfax) ; Sfax ; Djebéniana", "sv"),
               ("Territoires militaires du Sud ;  ; Tataouine", "sv"),
               ("2me Région (Tunis) ; Grombalia ; Cap-Bon - Nabeul", "imp")):
    FLAGS[("sgt1925", "oliviers_age", "", _l, _c)] = "total_mismatch"
for _l in ("Cap-Bon - Nabeul", "Cap-Bon - Soliman"):
    FLAG_ROWS[("sgt1925", "oliviers_age", "", "2me Région (Tunis) ; Grombalia ; " + _l)] = "row_realigned"
for _l, _c in (("5me Région (Sfax) ; Tozeur ; Djerid", "t3"), ("3me Région (Le Kef) ; Medjez-el-Bab ; Medjez-el-Bab", "t9"),
               ("4me Région (Sousse) ; Sousse ; Sousse", "t5"), ("4me Région (Sousse) ; Kairouan ; Kairouan", "t4"),
               ("4me Région (Sousse) ; Thala ; Fraichiches", "t9"), ("4me Région (Sousse) ; Thala ; Madjeurs", "t9")):
    FLAGS[("sgt1925", "oliviers_tariff", "", _l, _c)] = "total_mismatch"
FLAGS[("sgt1925", "oliviers_roll", "", "4me Région (Sousse) ; Sousse ; Souassi", "imp_i")] = "total_mismatch"
FLAGS[("sgt1925", "oliviers_roll", "", "5me Région (Sfax) ; Sfax ; Sfax", "ar_i")] = "total_mismatch"
FLAGS[("sgt1926", "oliviers_age", "", "Territoires militaires du Sud ;  ; Ouerghema", "a2")] = "total_mismatch"
FLAGS[("sgt1926", "oliviers_tariff", "", "4me Région (Sousse) ; Thala ; Fraichiches", "t3")] = "row_realigned"
FLAGS[("sgt1926", "oliviers_tariff", "", "4me Région (Sousse) ; Thala ; Madjeurs", "t3")] = "row_realigned"
FLAGS[("sgt1926", "oliviers_tariff", "", "3me Région (Le Kef) ; Medjez-el-Bab ; Medjez-el-Bab", "t9")] = "total_mismatch"
FLAGS[("sgt1926", "oliviers_roll", "", "5me Région (Sfax) ; Sfax ; La Skhira", "co_e")] = "total_mismatch"
FLAGS[("sgt1927", "dattiers_roll", "", "Territoires militaires ;  ; Ouerghemma", "i_cm_i")] = "total_mismatch"
FLAGS[("sgt1927", "oliviers_age", "", "4me Région (Sousse) ; Sousse ; Monastir", "a1")] = "total_mismatch"
FLAGS[("sgt1927", "oliviers_age", "", "5me Région (Sfax) ; Tozeur ; Djerid", "imp")] = "total_mismatch"
FLAGS[("sgt1927", "oliviers_tariff", "", "3me Région (Le Kef) ; Téboursouk ; Téboursouk", "t2")] = "total_mismatch"
for _l, _c in (("2me Région (Tunis) ; Grombalia ; Cap-Bon - Nabeul", "imp_e"), ("5me Région (Sfax) ; Sfax ; Sfax", "imp_e"),
               ("3me Région (Le Kef) ; Mactar ; Oulad Aoun", "imp_i"), ("4me Région (Sousse) ; Sousse ; Mahdia", "non_i"),
               ("Territoires militaires du Sud ;  ; Ouerghema", "ar_e")):
    FLAGS[("sgt1927", "oliviers_roll", "", _l, _c)] = "total_mismatch"
FLAGS[("sgt1928", "dattiers_age", "degla", "5e Région ;  ; Tozeur", "a18")] = "total_mismatch"
for _l, _c in (("2me Région (Tunis) ; Zaghouan ; Zaghouan", "non_e"), ("2me Région (Tunis) ; Zaghouan ; Zaghouan", "non_i"),
               ("Territoires militaires du Sud ;  ; Nefzaoua", "imp_i")):
    FLAGS[("sgt1928", "oliviers_roll", "", _l, _c)] = "total_mismatch"
FLAGS[("sgt1929", "oliviers_age", "", "2me Région (Tunis) ; Grombalia ; Cap-Bon - Nabeul", "a12")] = "total_mismatch"
for _l, _c in (("1re Région (Bizerte) ; Bizerte ; Bizerte", "imp_e"), ("1re Région (Bizerte) ; Béja ; Béja", "imp_i"),
               ("2me Région (Tunis) ; Tunis ; Banlieue", "imp_i")):
    FLAGS[("sgt1929", "oliviers_roll", "", _l, _c)] = "total_mismatch"
FLAGS[("sgt1930", "oliviers_age", "", "2me Région (Tunis) ; Zaghouan ; Zaghouan", "a4")] = "total_mismatch"
FLAGS[("sgt1930", "oliviers_age", "", "Territoires militaires du Sud ;  ; Tataouine", "a15")] = "total_mismatch"
FLAGS[("sgt1930", "oliviers_tariff", "", "1re Région (Bizerte) ; Bizerte ; Bizerte", "dime")] = "total_mismatch"
FLAGS[("sgt1930", "oliviers_tariff", "", "2me Région (Tunis) ; Grombalia ; Cap-Bon - Nabeul", "t5")] = "total_mismatch"
FLAGS[("sgt1935", "oliviers_age", "", "1re Région (Bizerte) ; Bizerte ; Mateur", "a13")] = "total_mismatch"
for _l in ("Fraichiches", "Majeur"):
    for _c in ("imp_e", "imp_i", "non_e", "non_i"):
        FLAGS[("sgt1923", "oliviers_roll", "", _l, _c)] = "row_realigned"
# Cells hidden in the gutter fold ('?' in the transcription), derived as the printed row TOTAL minus the other cells
# of the row (flag derived_from_totals): (edition, table, kind, label, col)
DERIVE = {
    ("sgt1922", "oliviers_tariff", "", "Souk-el-Arba", "t5"),
}


def geo(label):
    parts = [x.strip() for x in label.split(" ; ")]
    if len(parts) == 1:
        return {"region": "", "controle_civil": "", "caidat": parts[0]}
    return {"region": parts[0], "controle_civil": parts[1], "caidat": parts[2]}


def tariff_code(fr):
    """'à 1,40' -> '1.40'; 'à 2 fr.' -> '2.00'; '3,012' -> '3.012'."""
    m = re.search(r"(\d+)(?:,(\d+))?", fr)
    a, b = m.group(1), m.group(2) or "00"
    return f"{a}.{b}"


# ----------------------------------------------------------------- merging the views of a spread

def merged(secs):
    """{(ed, table, kind): {label: {col: (Cell, sec)}}} in printed order."""
    out = {}
    for s in secs:
        d = out.setdefault((s["ed"], s["table"], s.get("kind", "")), {})
        for r in s["rows"]:
            if "cells" in r:
                e = d.setdefault(r["label"], {})
                for c, cell in r["cells"].items():
                    if c in e and e[c][0].value != cell.value:
                        raise ValueError(f"{s['ed']} {s['table']} {r['label']} {c}: two views disagree")
                    e.setdefault(c, (cell, s))
    return out


def derive(M):
    for (ed, t, kind, lab, col) in DERIVE:
        d = M[(ed, t, kind)]
        cell = d[lab][col][0]
        others = [c for c in d[lab] if c not in (col, "tot", "tj")]
        cell.value = d[lab]["tot"][0].value - ssum(d[lab][c][0].value for c in others)
        cell.flag = "derived_from_totals"


def val(d, lab, col):
    x = d[lab].get(col)
    return None if x is None else x[0].value


# ----------------------------------------------------------------- cells

def base(sec, cell, label):
    return dict(census=sec["ed"], table_id=sec["table"], gallica_ark=sec["ark"], source_page=sec["page"],
                gallica_view=sec["view"], year=int(sec["year"]), **geo(label), value=cell.value, flag=cell.flag)


def flagged(rec, key):
    f = FLAGS.get(key) or FLAG_ROWS.get(key[:4])
    if f:
        rec["flag"] = f
    return rec


def cells(M, table):
    out = []
    for (ed, t, kind), d in M.items():
        if t != table:
            continue
        for lab, cols in d.items():
            if is_total(lab):
                continue
            for c, (cell, sec) in cols.items():
                if c in ("tj", "tot") or c.endswith("_t"):
                    continue
                r = base(sec, cell, lab)
                if table.endswith("_age"):
                    if table.startswith("dattiers"):
                        r.update(tree_kind=KIND[kind][0], tree_kind_fr=KIND[kind][1])
                    r.update(age_class=AGE[c][0], age_class_fr=AGE[c][1])
                elif table.endswith("_tariff"):
                    if table.startswith("dattiers"):
                        r.update(tree_kind=KIND[kind][0], tree_kind_fr=KIND[kind][1])
                    if c == "dime":
                        r.update(tariff="former_tithe_proportional", tariff_fr=DIME_FR)
                    else:
                        fr = sec["tariffs"].split(";")[int(c[1:]) - 1].strip()
                        r.update(tariff=tariff_code(fr), tariff_fr=fr)
                else:
                    p = c.split("_")
                    if p[0] in ("ar", "co"):
                        m = "articles" if p[0] == "ar" else "accounts"
                        r.update(measure=m, measure_fr=MEASURE[m][0], unit=MEASURE[m][1], roll=ROLL[p[1]][0],
                                 roll_fr=ROLL[p[1]][1], tree_kind="", tree_kind_fr="", status="", status_fr="")
                    else:
                        if table.startswith("dattiers"):
                            roll, k, st = p
                            kk = "degla" if k == "dg" else "communs"
                            r.update(tree_kind=KIND[kk][0], tree_kind_fr=KIND[kk][1])
                        else:
                            st, roll = ("i" if p[0] == "imp" else "n"), p[1]
                        r.update(measure="trees", measure_fr=MEASURE["trees"][0], unit="trees",
                                 roll=ROLL[roll][0], roll_fr=ROLL[roll][1], status=STATUS[st][0],
                                 status_fr=STATUS[st][1])
                out.append(flagged(r, (ed, table, kind, lab, c)))
    return out


# ----------------------------------------------------------------- checks

def w(ed, t, kind, lab=""):
    return f"{ed} {t}{' ' + kind if kind else ''}{' ' + lab if lab else ''}"


def chk_totals(M):
    """Every Totaux line = sum of the lines above it, every column."""
    for (ed, t, kind), d in M.items():
        o = PREFIX + "_" + t
        data = [l for l in d if not is_total(l)]
        for tl in [l for l in d if is_total(l)]:
            for c, (cell, sec) in d[tl].items():
                CHK.eq(o, f"{w(ed, t, kind)} Totaux {c}: sum of the lines (f{sec['view']})",
                       ssum(val(d, l, c) for l in data), cell.value)


def chk_rows(M):
    for (ed, t, kind), d in M.items():
        o = PREFIX + "_" + t
        for lab, cols in d.items():
            g = lambda c: val(d, lab, c)
            if t.endswith("_age"):
                first = "m" if t.startswith("dattiers") else "sv"
                CHK.eq(o, f"{w(ed, t, kind, lab)}: Total des jeunes = moins d'un an + 1 .. 19 ans",
                       ssum(g(a) for a in AGES if a in cols), g("tj"))
                CHK.eq(o, f"{w(ed, t, kind, lab)}: Total = col. 2 + Total des jeunes + 20 ans imposables",
                       ssum([g(first), g("tj"), g("imp")]), g("tot"))
            elif t.endswith("_tariff"):
                parts = [c for c in cols if c != "tot"]
                CHK.eq(o, f"{w(ed, t, kind, lab)}: TOTAL = tariff columns", ssum(g(c) for c in parts), g("tot"))
            else:
                for p in ("ar", "co") + (("imp", "non") if t.startswith("oliviers") else ()):
                    if p + "_t" in cols:
                        CHK.eq(o, f"{w(ed, t, kind, lab)}: {p} TOTAL = Européens + Indigènes",
                               ssum([g(p + "_e"), g(p + "_i")]), g(p + "_t"))


def chk_cross(M):
    """b) TOTAL = a) 20 ans imposables; c) imposés (Européens + Indigènes) = a) 20 ans imposables; c) non imposés =
    a) col. 2 (mâles / sauvages) + Total des jeunes; per line, Totaux included."""
    for (ed, t, kind), d in M.items():
        if t == "dattiers_tariff":
            a = M.get((ed, "dattiers_age", kind))
            o = PREFIX + "_dattiers_tariff"
            for lab in d:
                CHK.eq(o, f"{w(ed, t, kind, lab)}: TOTAL = a) 20 ans imposables", val(a, lab, "imp"), val(d, lab, "tot"))
        if t == "oliviers_tariff":
            a = M.get((ed, "oliviers_age", ""))
            o = PREFIX + "_oliviers_tariff"
            for lab in d:
                CHK.eq(o, f"{w(ed, t, kind, lab)}: TOTAL = a) 20 ans imposables", val(a, lab, "imp"), val(d, lab, "tot"))
        if t == "dattiers_roll":
            o = PREFIX + "_dattiers_roll"
            for k, kk in (("dg", "degla"), ("cm", "communs")):
                a = M.get((ed, "dattiers_age", kk))
                for lab in d:
                    CHK.eq(o, f"{w(ed, t, kind, lab)} {kk}: imposés E + I = a) 20 ans imposables",
                           ssum([val(d, lab, f"e_{k}_i"), val(d, lab, f"i_{k}_i")]), val(a, lab, "imp"))
                    nm = kk == "communs" and ed in COMMUNS_NO_MALES
                    CHK.eq(o, f"{w(ed, t, kind, lab)} {kk}: non imposés E + I = a) "
                              + ("Total des jeunes" if nm else "mâles + Total des jeunes"),
                           ssum([val(d, lab, f"e_{k}_n"), val(d, lab, f"i_{k}_n")]),
                           val(a, lab, "tj") if nm else ssum([val(a, lab, "m"), val(a, lab, "tj")]))
        if t == "oliviers_roll":
            o = PREFIX + "_oliviers_roll"
            a = M.get((ed, "oliviers_age", ""))
            for lab in d:
                CHK.eq(o, f"{w(ed, t, kind, lab)}: imposés TOTAL = a) 20 ans imposables", val(a, lab, "imp"),
                       val(d, lab, "imp_t"))
                CHK.eq(o, f"{w(ed, t, kind, lab)}: non imposés TOTAL = a) sauvages + Total des jeunes",
                       ssum([val(a, lab, "sv"), val(a, lab, "tj")]), val(d, lab, "non_t"))


# ----------------------------------------------------------------- documentation

GEO_DOC = dict(
    region="région as printed, with its chef-lieu in brackets for the olive tables (from sgt1925: \"1re Région "
           "(Bizerte)\" ... \"5me Région (Sfax)\", \"Territoires militaires du Sud\"; date-palm tables: \"5e "
           "Région\", \"Territoires militaires\"); empty in sgt1922-sgt1924, which list caïdats only",
    controle_civil="contrôle civil as printed (olive tables from sgt1925; empty otherwise)",
    caidat="caïdat as printed in that table (spelling varies between editions and between a), b), c): Majeur / "
           "Madjeurs, Hammama / Hemmama, Ouled-Ayar / Oulad Ayar, Kef / Le Kef...); \"Cap-Bon - Nabeul\" and "
           "\"Cap-Bon - Soliman\" = the two lines printed under the brace of the caïdat Cap-Bon")
DOC = dict(
    census="edition (source code, see EDITIONS.md)", table_id="transcription section (table a), b) or c))",
    gallica_ark="Gallica volume ark (views are numbered within a volume)", source_page="printed page number",
    gallica_view="Gallica view (fNNNN) of the page the cell is printed on",
    year="year of the census of the trees: the year of the \"1er novembre <year>\" printed in the title of a) "
         "(the edition year, except sgt1925 dattiers, titled 1924); b) and c) take the year of their a)",
    tree_kind="`degla` (dattiers degla, the deglet nour palms) or `common` (dattiers communs)",
    tree_kind_fr="printed block / column heading",
    age_class="`male` (mâles, date palms), `wild` (arbres sauvages, olive trees), `under_1` (moins d'un an), "
              "`age_01` .. `age_19` (1 an .. 19 ans: young trees, not taxed), `taxable_20_plus` (20 ans "
              "imposables)",
    age_class_fr="printed column heading",
    tariff="tax rate per tree, francs, as a code (`1.40`, `0.05`, ...); `former_tithe_proportional` = anciens pays "
           "à dîme, impôt proportionnel au revenu global (olive trees of the former tithe lands, taxed on their "
           "income instead of per tree)",
    tariff_fr="printed column heading (the rate as printed)",
    measure="`trees` (nombre d'arbres), `articles` (nombre d'articles de matrice: entries on the tax roll), "
            "`accounts` (nombre de comptes individuels: individual taxpayer accounts)",
    measure_fr="printed column-group heading", unit="unit of `value`",
    roll="`european` (Européens) or `indigenous` (Indigènes)", roll_fr="printed column heading",
    status="`taxed` (imposés) or `not_taxed` (non imposés: young trees, mâles / sauvages); empty for articles and "
           "accounts",
    status_fr="printed column heading",
    value="printed count (» = 0)",
    flag="empty, or `total_mismatch` (printed value kept; the line TOTAL and the column Totaux, or the other tables of "
         "the same edition, identify it as the faulty cell; see the notes), `row_realigned` (figures printed on the "
         "line of another caïdat, stored under the caïdat they belong to; see the notes), `derived_from_totals` "
         "(digits lost in the gutter fold; value = line TOTAL minus the other cells of the line)",
    **GEO_DOC)

SPECS = {
    "dattiers_age": dict(
        dims=["tree_kind", "tree_kind_fr", "age_class", "age_class_fr"],
        title_en="Tax on date palms (canoun des dattiers): trees by caïdat, kind and age",
        unit="Unit: number of trees; value_type: count.",
        paras=["Two blocks, Dattiers degla and Dattiers communs, each by caïdat (the date-palm caïdats of the south: "
               "Nefzaoua, Ouerghemma, L'Arad / Gabès, Gafsa, Djerid / Tozeur) with columns 2 Mâles (male palms, "
               "not taxed), 3 Moins d'un an, 4-22 1 an .. 19 ans, 23 Total des jeunes, 24 20 ans imposables, 25 "
               "Total des colonnes 2, 23 et 24. Stored: columns 2-22 and 24; Total des jeunes, Total and the Totaux "
               "lines are checks. A palm becomes taxable at 20 years; the young trees move one age column per "
               "edition. Printed sgt1922-sgt1930 and sgt1935 (from sgt1925 grouped under 5e Région / Territoires "
               "militaires; Gabès and Tozeur replace L'Arad and Djerid; Matmata added in sgt1935). The sgt1925 title "
               "still reads \"1er novembre 1924\" (year coded 1924; figures differ from sgt1924)."]),
    "dattiers_tariff": dict(
        dims=["tree_kind", "tree_kind_fr", "tariff", "tariff_fr"],
        title_en="Tax on date palms (canoun des dattiers): taxable trees by caïdat and tariff",
        unit="Unit: number of trees; value_type: count.",
        paras=["Nombre d'arbres imposés by caïdat at each tariff (francs per tree, printed in the column heads and kept "
               "in `tariff_fr`): Dattiers degla and Dattiers communs. The TOTAL column and the Totaux line are "
               "checks (TOTAL also = a) 20 ans imposables). The rates change twice: sgt1922-sgt1925 degla 1,40 / 1,80 / 2 / "
               "2,40, communs 0,15 / 0,40 / 0,75 / 1,00 / 1,20; sgt1926-sgt1928 x 1,25 (1,75 ... 3,00; 0,1875 ... 1,50); "
               "sgt1929, sgt1930 x 1,75 of the sgt1926 rates (3,012 or 3,0625 ... 5,25; 0,328125 ... 2,625). `tariff` "
               "codes the printed rate. Not printed in sgt1935."]),
    "dattiers_roll": dict(
        dims=["measure", "measure_fr", "unit", "tree_kind", "tree_kind_fr", "roll", "roll_fr", "status",
              "status_fr"],
        title_en="Tax on date palms (canoun des dattiers): trees taxed and not taxed on the European and indigenous "
                 "rolls, articles and individual accounts",
        unit="Units: trees, articles (entries of the matrice) and accounts (comptes individuels), see `unit`; "
             "value_type: mixed (counts of three kinds).",
        paras=["Printed under b) on the same spread: Européens and Indigènes x Dattiers degla / Dattiers communs x "
               "Imposés / non Imposés (trees), then Nombre d'articles de matrice and Nombre de comptes individuels "
               "(Européens, Indigènes, TOTAL). The TOTAL columns and the Totaux line are checks; imposés E + I = a) "
               "20 ans imposables and non imposés E + I = a) mâles + Total des jeunes are checked line by line (in "
               "sgt1928 the communs non imposés equal a) Total des jeunes, i.e. exclude the mâles; checked so). Not "
               "printed in sgt1935."]),
    "oliviers_age": dict(
        dims=["age_class", "age_class_fr"],
        title_en="Tax on olive trees (canoun des oliviers): trees by caïdat and age",
        unit="Unit: number of trees; value_type: count.",
        paras=["By caïdat (sgt1922-sgt1924, 30 lines; from sgt1925 by région, chef-lieu de région, contrôle civil and "
               "caïdat, 33 lines): Arbres sauvages (wild trees, not taxed), Moins d'un an, 1 an .. 19 ans, Total des "
               "jeunes, 20 ans imposables, Total. Stored: every column except the two totals; the Totaux line is a "
               "check. sgt1927-sgt1930 print no Moins d'un an column (no `under_1` rows for those editions). New "
               "lines: Aïn-Draham and Matmata from sgt1929; in sgt1935 Thala and Sbeïtla replace Fraichiches and "
               "Madjeurs. The two lines under the Cap-Bon brace are stored as Cap-Bon - Nabeul and Cap-Bon - "
               "Soliman."]),
    "oliviers_tariff": dict(
        dims=["tariff", "tariff_fr"],
        title_en="Tax on olive trees (canoun des oliviers): taxable trees by caïdat and tariff",
        unit="Unit: number of trees; value_type: count.",
        paras=["Nombre d'arbres imposés à each rate (sgt1922: twelve rates 0,05 .. 1,00 fr. per tree; from sgt1923 ten "
               "rates, without 0,35 and 0,45), and the column Anciens pays à dîme, impôt proportionnel au revenu "
               "global (trees of the former tithe lands of the north, taxed in proportion to their income), TOTAL "
               "(check, also = a) 20 ans imposables). From sgt1929 a new scale: 0,05 0,10 0,25 0,50 0,75 1,00 1,25 1,50 "
               "1,75 2,00. Not printed in sgt1935."]),
    "oliviers_roll": dict(
        dims=["measure", "measure_fr", "unit", "roll", "roll_fr", "status", "status_fr"],
        title_en="Tax on olive trees (canoun des oliviers): trees taxed and not taxed on the European and indigenous "
                 "rolls, articles and individual accounts",
        unit="Units: trees, articles and accounts, see `unit`; value_type: mixed (counts of three kinds).",
        paras=["Nombre d'arbres imposés and non imposés (jeunes et sauvages), each Européens, Indigènes, TOTAL; Nombre "
               "d'articles de matrice and Nombre de comptes individuels, each Européens, Indigènes, TOTAL. TOTAL "
               "columns and Totaux are checks; imposés TOTAL = a) 20 ans imposables, non imposés TOTAL = a) "
               "sauvages + Total des jeunes. Not printed in sgt1935."]),
}
for _t in SPECS:
    SPECS[_t]["title_fr"] = TITLES[_t]

# per-table explanation of every failed check (filled from the transcription comments, where each is described)
FAILS = {
    "dattiers_age": {
        "sgt1922": "Djerid degla Total des jeunes printed 57.352, the ages sum to 56.352; the column Totaux 62.551 "
                   "follows the misprint (c) non imposés 2.338 + 55.014 = 57.352 also; check column, not stored).",
        "sgt1928": "Degla Tozeur 18 ans printed 8.138 (Total des jeunes requires 8.183, as in sgt1927): flagged; the "
                   "column Totaux 9.500 and Total des jeunes 113.524 are 1 off their lines (check line).",
        "sgt1925": "Communs: Nefzaoua moins d'un an printed 91.022 (Total des jeunes, the column Totaux and c) require "
                   "71.022; flagged); Gafsa Total des jeunes printed 18.923 for 12.923 (check column).",
    },
    "dattiers_roll": {
        "sgt1922": "Totaux indigènes degla non imposés printed 60.135, the lines sum to 60.136 (and a) gives 62.551 - "
                   "2.415 = 60.136); misprint of the check line.",
        "sgt1925": "Nefzaoua indigènes communs imposés printed 224.361 (b), a) and the column Totaux require 224.363; "
                   "flagged); Gafsa communs non imposés 63 + 19.429 = 19.492 against a) 25.492, which carries the "
                   "misprinted Total des jeunes of a).",
        "sgt1927": "Ouerghemma indigènes communs imposés printed 23.269 (zoomed; the column Totaux 1.083.149 adds it "
                   "as printed) while a) and b) give 74.562 - 1.293 = 73.269: flagged; the Totaux follow it.",
    },
    "oliviers_age": {
        "sgt1922": "Totaux 20 ans imposables and Total printed 1 under the sum of the lines (b) Totaux prints 9.094.192 "
                   "= the lines); misprint of the check line.",
        "sgt1923": "Totaux arbres sauvages printed 822.887 for 722.887 (the lines; the Total of the Totaux line "
                   "15.260.037 is consistent with neither), Total des jeunes 5.493.618 for 5.493.648; Bizerte Total "
                   "467.071 for 467.171 (check column). Cap-Bon 15 ans 3.554 printed on the Nabeul line, stored on "
                   "the Soliman line (row_realigned, see the transcription).",
        "sgt1925": "Printed errors, each figure confirmed zoomed (flagged total_mismatch where the line Total and the "
                   "column Totaux both point to the cell): Téboursouk 2 ans 3.864 (2.864); Mateur 18 ans 1.712 (2.712) "
                   "and Souk-el-Khemis 18 ans 843 (813); Zaghouan 14 ans 238 (338); Souassi 19 ans 26.983 (26.985), "
                   "Djebéniana 19 ans 2.055 (2.005); Djebéniana sauvages 10.095 (19.095), Tataouine sauvages 1.967 "
                   "(1.968); Cap-Bon - Nabeul 20 ans imposables 337.466 (377.466, = b) and c)). La Skhira Total des "
                   "jeunes 597.729 for 497.729 (check column). The two Cap-Bon lines of a) carry each other's figures "
                   "(row_realigned).",
        "sgt1926": "Ouerghema 2 ans printed 194.685 (zoomed; Total des jeunes, the column Totaux and sgt1925 (1 an "
                   "191.685) require 191.685; flagged). Totaux 9 ans 766.637 for the lines' 766.537 and Totaux Total "
                   "des jeunes 5.714.272 against its columns' 5.714.372 (check line).",
        "sgt1927": "No moins d'un an column in this printing. Monastir 1 an printed 14.438 (zoomed; Total des jeunes "
                   "and the column Totaux require 14.488, as printed in sgt1926) and Djerid 20 ans imposables 21.411 "
                   "(the line Total and the column Totaux require 21.481): flagged. Totaux 10 ans 766.637 and Total "
                   "des jeunes 5.146.071 repeat the sgt1926 Totaux misprints (check line).",
        "sgt1929": "Cap-Bon - Nabeul 12 ans printed 83.231 (Total des jeunes and the column Totaux require 33.231): "
                   "flagged. Mahdia Total des jeunes 558.347 for 588.347 (check column); Totaux 10 ans 97.756 (lines "
                   "97.736) and Total des jeunes 5.160.146 (lines 5.130.146) are check-line misprints.",
        "sgt1930": "Zaghouan 4 ans printed 1.202 (Total des jeunes and the column Totaux require 1.204, as in sgt1929) "
                   "and Tataouine 15 ans 8.265 (8.295): flagged. Totaux 8 ans 1.242.540 (lines 1.212.510), 14 ans and "
                   "18 ans 300 over their lines, and Total des jeunes 5.174.785 against its columns: check-line "
                   "misprints.",
        "sgt1935": "Mateur 13 ans printed 18.380 (Total des jeunes and the column Totaux require 18.388): flagged. "
                   "Zaghouan Total 128.544 for 128.554 and the Totaux Total 16.801.750 (lines 16.801.740) are check "
                   "figures. Totaux 7 ans hidden in the fold (not checked).",
    },
    "oliviers_tariff": {
        "sgt1922": "Monastir 0,25 147.390 and 0,30 441.916 exceed the TOTAL 1.520.543 by 10; the 0,30 Totaux is 10 "
                   "under its lines, so the 0,30 cell is flagged. Totaux TOTAL 9.094.192 against a) 9.094.191 (a) "
                   "Totaux misprint). Souk-el-Arba 0,25 lost in the fold: derived from the TOTAL (285); the 0,25 "
                   "Totaux is partly hidden (not checked).",
        "sgt1923": "Totaux 0,30 printed 103.643 (a digit dropped; the lines give 1.036.430), 0,75 1.988.190 and TOTAL "
                   "9.043.502 (= a) 20 ans imposables) against lines 1.987.890 and 9.043.802: the line Majeur 0,75 "
                   "1.110 is 300 short of its TOTAL 1.938 (flagged), Kairouan TOTAL 15.415 for 15.115 (= a)). Zaghouan: "
                   "0,20 26, 0,30 877, 0,50 340, 0,75 4 printed besides an old-tithe figure equal to the TOTAL "
                   "82.972 (the same in sgt1924); not resolvable. Fraichiches and Majeur lines exchanged "
                   "(row_realigned).",
        "sgt1924": "Monastir 0,20 123.275 (TOTAL and Totaux require 123.257, as in sgt1923) and Ouled-Aoun 0,25 6.940 "
                   "(2.940, as in sgt1923), flagged; Zaghouan as in sgt1923.",
        "sgt1925": "Flagged (line TOTAL and column Totaux point to the same cell): Djerid 0,15 2.888 (2.848), Medjez-el-"
                   "Bab 0,75 1.729 (3.729), Sousse 0,25 26.443 (26.433), Kairouan 0,20 252 (258); Fraichiches and "
                   "Madjeurs 0,75 1.410 and 1.353 (sgt1924 prints them the other way round) fit neither TOTAL. Not "
                   "attributable: Zaghouan (+10), Ouerghema (-10), Le Kef TOTAL 29.987 (a): 29.996), Madjeurs 0,50, "
                   "Totaux 0,15, 0,20, 0,50, dime and TOTAL.",
        "sgt1926": "Medjez-el-Bab 0,75 1.729 (3.729, as in sgt1925), flagged; the Totaux 0,75 2.023.103 requires "
                   "3.729. The 0,15 figure 7 printed on the Fraichiches line belongs to Madjeurs (row_realigned).",
        "sgt1929": "New rates from this edition (0,05 .. 2,00). Souk-el-Khemis TOTAL 4.656 for 4.657 (a) and the "
                   "tariff cells); the Totaux TOTAL follows it.",
        "sgt1930": "Bizerte old-tithe figure 429.239 (TOTAL 429.234 = a) imposables; the column Totaux 2.486.318 also "
                   "requires 429.234) and Cap-Bon - Nabeul 0,75 91.643 (TOTAL and Totaux require 91.642): flagged.",
        "sgt1927": "Téboursouk 0,10 printed 1.079 (zoomed; the line TOTAL and the column Totaux require 1.179, as in "
                   "sgt1926): flagged. Djerid TOTAL 21.481 against the misprinted a) 21.411 (see a)). The 0,15 Totaux "
                   "is partly hidden in the fold (not checked).",
    },
    "oliviers_roll": {
        "sgt1922": "L'Arad comptes TOTAL 1.876 for 4.876 (the Totaux 192.497 requires 4.876); Mahdia non imposés TOTAL "
                   "713.758 against a) 712.748 (Européens + Indigènes = 713.758; the a) figures agree with each "
                   "other); Cap-Bon - Nabeul imposés TOTAL 376.253 against a) and b) 376.369, Gafsa 135.029 against "
                   "135.030; the Totaux follow these lines.",
        "sgt1923": "Non imposés Totaux = a) sauvages Totaux misprint (822.887 for 722.887) plus Total des jeunes.",
        "sgt1925": "Souassi indigènes imposés 53.045 (58.045) and Sfax articles indigènes 22.803 (22.893), flagged; "
                   "small unattributed differences in check figures (Zaghouan comptes TOTAL, Le Kef imposés TOTAL "
                   "29.906, Sousse comptes TOTAL, Gafsa articles TOTAL 11.482, Totaux non imposés and comptes "
                   "indigènes); differences with a) follow the a) misprints (Cap-Bon - Nabeul, La Skhira, "
                   "Djebéniana, Tataouine).",
        "sgt1926": "La Skhira comptes européens printed 333 (zoomed; the line TOTAL 2.899 and the column Totaux 5.096 "
                   "require 343), flagged; Souassi articles TOTAL printed 6.889 for 6.689 (the Totaux 458.545 "
                   "requires 6.689; check column).",
        "sgt1928": "Zaghouan non imposés printed 7.984 / 155.189 / 163.173: a) gives 14.225 and the column Totaux "
                   "imply 14.153 (both cells flagged; no correction attempted). Nefzaoua indigènes imposés 9.600 (a), "
                   "b) and the Totaux require 9.672), flagged; its non imposés carry the 72 trees. Check figures: "
                   "Téboursouk articles TOTAL 1.231 (1.131), Kairouan 1.073 (1.373), Gafsa 11.756 (11.760; printed in "
                   "the Hemmama cell), Béja comptes TOTAL partly printed; Totaux of articles and comptes off by small "
                   "amounts (not attributable).",
        "sgt1929": "Flagged (zoomed; the line TOTAL, b) and the column Totaux all point to the cell): Bizerte "
                   "Européens imposés 38.046 (38.446), Béja indigènes imposés 11.752 (11.852), Banlieue indigènes "
                   "imposés 730.080 (730.089). Not attributable: Matmata imposés TOTAL 108.806 with Européens » and "
                   "Indigènes 108.713, Ouerghema 194.604 with 9.891 + 184.806 (93 trees on the wrong line, the Totaux "
                   "unaffected); Le Kef imposés TOTAL 29.993 (= a)) for 29.994; Bizerte non imposés TOTAL 36.946 = a) "
                   "for 36.949; Mahdia follows the a) misprint.",
        "sgt1927": "Flagged (line TOTAL and column Totaux both point to the cell; each zoomed): Cap-Bon - Nabeul "
                   "Européens imposés 10.580 (10.508), Sfax Européens imposés 226.238 (226.231), Oulad Aoun indigènes "
                   "imposés 23.932 (23.939), Mahdia indigènes non imposés 128.407 (628.407), Ouerghema articles "
                   "européens 19 (119). Check figures: Cap-Bon - Soliman imposés TOTAL 1.057.995 for 1.157.995 (a) and "
                   "b)), Tataouine non imposés TOTAL 84.749 for 34.749, Totaux imposés TOTAL 9.909.456 = a) (the lines "
                   "carry the Soliman misprint), non imposés TOTAL 5.859.552; Djerid follows the a) misprint.",
    },
}

COLS_GEO = ["region", "controle_civil", "caidat"]


def views(rows):
    by = defaultdict(set)
    for r in rows:
        by[r["census"]].add((r["source_page"], r["gallica_view"]))
    return "; ".join(f"{e} (`{EDITIONS[e]}`): " + ", ".join(f"p. {p}, f{v}" for p, v in sorted(by[e]))
                     for e in ORDER if e in by)


def notes(name, t, spec, rows, cols, secs):
    o = PREFIX + "_" + t
    fails = CHK.fail[o]
    eds = [e for e in ORDER if e in {r["census"] for r in rows}]
    L = [f"# {spec['title_fr']}", "", f"*{spec['title_en']}.*", "",
         f"Source: *Statistique générale de la Tunisie*, chapter *{CHAPTER}*, editions {', '.join(eds)}. "
         "Source gallica.bnf.fr / Ministère des Affaires étrangères.", "",
         f"Pages and views: {views(rows)}.", "",
         f"Transcriptions: `../transcribed/finance_canoun_<edition>.txt`; rebuild with "
         f"`python3 data-raw/yearbook_other_chapters/{SCRIPT} build`.", "",
         f"Rows: {len(rows)}. Years: {', '.join(map(str, sorted({r['year'] for r in rows})))}.", "",
         spec["unit"], "",
         "Printed once per edition, each printing for its own year: every edition is kept (SPEC_ADDENDUM rule 5); "
         "`census` is the edition, `year` the year of the tree census (1er novembre <year>, printed in the title of "
         "a)).", "", "## Columns", ""]
    L += [f"- `{c}`: {DOC[c]}" for c in cols]
    L += [""]
    for p in spec["paras"]:
        L += [p, ""]
    L += ["Footnotes: none printed under these tables.", "", "## Validation", "",
          f"- Checks against printed totals and identities: {CHK.n[o]}; passed: {CHK.n[o] - len(fails)}; "
          f"failed: {len(fails)}."]
    if fails:
        L += ["", "Every failure was re-read on zoomed native-resolution crops; printed values are kept. Explanation, "
              "by edition:", ""]
        L += [f"  - {e}: {x}" for e, x in FAILS.get(t, {}).items() if e in eds]
        L += ["", "Failed checks:", ""] + [f"  - {x}" for x in fails]
    fl = defaultdict(int)
    for r in rows:
        if r["flag"]:
            fl[r["flag"]] += 1
    L += ["", "- Flagged cells: " + (", ".join(f"{k}: {n}" for k, n in sorted(fl.items())) if fl else "none") + "."]
    dims = [c for c in cols if c not in COMMON + ["value", "flag", "gallica_ark", "table_id", "unit", "region",
                                                  "controle_civil"] and not c.endswith("_fr")]
    L += [""] + [f"  - {r['census']} p.{r['source_page']} " + " / ".join(str(r.get(d, "")) for d in dims)
                 + f" = {r['value'] if r['value'] is not None else 'NA'} ({r['flag']})" for r in rows if r["flag"]]
    L += ["", "## Image versus OCR", ""]
    L += [f"- Read cell by cell on native-resolution crops of the page images (strips of rows, gutter columns on both "
          f"views of the spread, every failing check re-read zoomed): "
          + ", ".join(f"{s['ed']} f{s['view']}" for s in secs) + ".",
          "- The Gallica OCR was not used (no cell is flagged `ocr_corrected`).", "",
          "Survey of the canoun tables in every edition: `finance_canoun_survey.md`."]
    (OUT / f"{name}.md").write_text("\n".join(L) + "\n")


SURVEY = {
    "sgt1922": "f212|f213 dattiers a) (1er novembre 1922); f214|f215 b) (upper half) and c) (lower half); f216|f217 "
               "oliviers a); f218|f219 b); f220|f221 c)",
    "sgt1923": "f702|f703 dattiers a) (1923); f704|f705 b) and c); f706|f707 oliviers a); f708|f709 b); f710|f711 c)",
    "sgt1924": "f1198|f1199 dattiers a) (1924); f1200|f1201 b) and c); f1202|f1203 oliviers a); f1204|f1205 b); "
               "f1206|f1207 c)",
    "sgt1925": "f268|f269 dattiers a) (titled 1er novembre 1924); f270|f271 b) and c); f272|f273 oliviers a) (1925), "
               "by région, contrôle civil and caïdat; f274|f275 b); f276|f277 c)",
    "sgt1926": "f784|f785 dattiers a); f786|f787 b) and c); f788|f789 oliviers a) (1926); f790|f791 b); f792|f793 c)",
    "sgt1927": "f246|f247 dattiers a) (1927); f248|f249 b) and c); f250|f251 oliviers a); f252|f253 b); f254|f255 c)",
    "sgt1928": "f770|f771 dattiers a) (1928); f772|f773 b) and c); f774|f775 oliviers a); f776|f777 b); f778|f779 c)",
    "sgt1929": "f248|f249 dattiers a) (1929); f250|f251 b) and c); f252|f253 oliviers a); f254|f255 b); f256|f257 c)",
    "sgt1930": "f782|f783 dattiers a) (1930); f784|f785 b) and c); f786|f787 oliviers a); f788|f789 b); f790|f791 c)",
    "sgt1935": "f134|f135 canoun des dattiers (1935); f136|f137 canoun des oliviers (1935)",
}


# ----------------------------------------------------------------- build

def load():
    secs = []
    for ed in EDS:
        p = TR / f"{PREFIX}_{ed}.txt"
        if p.exists():
            secs += parse(p, ed)
    return secs


def build(write=True):
    secs = load()
    done = sorted({s["ed"] for s in secs}, key=ORDER.index)
    M = merged(secs)
    derive(M)
    chk_totals(M)
    chk_rows(M)
    chk_cross(M)
    res = {}
    for t in TITLES:
        o = PREFIX + "_" + t
        recs = cells(M, t)
        res[o] = dict(rows=len(recs), checks=CHK.n[o], failed=list(CHK.fail[o]),
                      editions=sorted({r["census"] for r in recs}, key=ORDER.index),
                      flagged=[f"{r['census']} {r['caidat']} {r.get('tree_kind', '')} {r.get('age_class', '')}"
                               f"{r.get('tariff', '')}{r.get('roll', '')} {r.get('status', '')} = {r['value']} "
                               f"({r['flag']})" for r in recs if r["flag"]])
        if write:
            cols = COMMON + COLS_GEO + SPECS[t]["dims"] + ["value", "flag"]
            write_csv(o, cols, recs)
            notes(o, t, SPECS[t], recs, cols, [s for s in secs if s["table"] == t])
    if write:
        write_validation(OUT / f"{PREFIX}_validation.json", dict(res, _views=SURVEY, _transcribed=done,
                                                                  _not_transcribed=[e for e in EDS if e not in done]))
        write_survey(res, done)
    return res


def write_survey(res, done):
    L = ["# Canoun des dattiers and canoun des oliviers: survey", "",
         "Tables of the tax on date palms and olive trees in the *Finances* chapter (see `finance_survey.md` for the "
         "whole chapter), view by view; every view confirmed on the page images. Extraction: "
         f"`{SCRIPT}`; transcriptions `../transcribed/finance_canoun_<edition>.txt`.", "",
         "| edition | ark | views | transcribed |", "|---|---|---|---|"]
    L += [f"| {e} | `{EDITIONS[e]}` | {SURVEY[e].replace('|', ' / ')} | {'yes, every cell read on the image' if e in done else 'no'} |"
          for e in EDS]
    L += ["", "## CSV", "", "| CSV | rows | editions | checks | failed | flagged |", "|---|---|---|---|---|---|"]
    L += [f"| `{o}` | {d['rows']} | {' '.join(d['editions'])} | {d['checks']} | {len(d['failed'])} | "
          f"{len(d['flagged'])} |" for o, d in res.items()]
    L += ["", "## Image reading", "",
          "Every cell of every transcribed printing was read on native-resolution crops of the page images (row "
          "strips of each page, the columns at the gutter fold on both views of the spread, every failing check "
          "re-read zoomed). The Gallica OCR was not used. Not yet transcribed: "
          + (", ".join(e for e in EDS if e not in done) or "none") + ".", ""]
    (OUT / f"{PREFIX}_survey.md").write_text("\n".join(L) + "\n")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    res = build(write=(mode == "build"))
    for out, d in res.items():
        print(f"{out}: {d['rows']} rows, {d['checks']} checks, {len(d['failed'])} failed, {len(d['flagged'])} "
              f"flagged [{' '.join(d['editions'])}]")
        for f in d["failed"]:
            print("   FAIL", f)


if __name__ == "__main__":
    main()
