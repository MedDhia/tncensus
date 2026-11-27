#!/usr/bin/env python3
"""Finances chapter (*Finances*: chapter X up to sgt1935, chapter IX in sgt1936 and sgt1939) of the Statistique
générale de la Tunisie, 12 editions sgt1922-sgt1939.

  python3 extract_finance.py check   parse the transcriptions, run every check, print failures
  python3 extract_finance.py build   ... and write csv/finance_*.csv, their .md notes,
                                     csv/finance_survey.md and csv/finance_validation.json

Source of truth: transcribed/finance_<edition>.txt (format in yb_tables.py). See csv/finance_survey.md for what
the chapter prints in every edition and which tables are transcribed.

Budget tables (sgt1925-sgt1939): annual budget, actual results (recettes réalisées; dépenses = droits constatés
définitivement liquidés lors des règlements des budgets), printed for overlapping ten-year (sgt1925-sgt1930) or
three-year (sgt1935-sgt1939) windows of exercices: SPEC_ADDENDUM rule 4 (each exercice from the latest edition
printing it, every other printing compared cell by cell). No budget forecasts (prévisions) are printed in the
chapter.
"""
import sys
from collections import defaultdict
from decimal import Decimal

from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parent))  # shared helper yb_tables.py
from yb_tables import (COMMON, EDITIONS, ORDER, OUT, TR, Checks, check_col_totals, coverage_lines, is_total, parse,
                       ssum, where, write_csv,
                       write_notes, write_validation)

CHAPTER = "Finances"
SCRIPT = "extract_finance.py"
PREFIX = "finance"

# Views of the chapter (chapter title .. last view before the next chapter title, Agriculture), confirmed on the
# page images (title pages "CHAPITRE X / FINANCES" and "CHAPITRE XI / AGRICULTURE"; IX and X in sgt1936-sgt1939).
CHAPTER_VIEWS = {
    "sgt1922": (185, 230), "sgt1923": (675, 720), "sgt1924": (1171, 1216), "sgt1925": (211, 286),
    "sgt1926": (767, 802), "sgt1927": (229, 258), "sgt1928": (753, 782), "sgt1929": (231, 260),
    "sgt1930": (765, 794), "sgt1935": (127, 138), "sgt1936": (94, 99), "sgt1939": (93, 98),
}

CHK = Checks()

# ----------------------------------------------------------------- budget: labels

PART = {"ordinary": "Titre premier (Première partie). Ressources ordinaires / Dépenses sur ressources ordinaires",
        "exceptional": "Titre II (Deuxième partie). Recettes sur ressources exceptionnelles / Dépenses sur "
                       "ressources exceptionnelles ou spéciales",
        "closed": "Titre III (Troisième partie)"}

# receipts, nomenclature used sgt1925-sgt1936 (code: item, part, printed label)
REC = {
    "ch1": ("direct_taxes", "ordinary", "Chapitre Ier. — Impôts directs et taxes assimilées"),
    "ch2": ("indirect_taxes", "ordinary", "Chapitre II. — Impôts et revenus indirects"),
    "ch3": ("monopolies_state_enterprises", "ordinary",
            "Chapitre III. — Produits des Monopoles et exploitations industrielles de l'Etat"),
    "ch4": ("state_domain", "ordinary", "Chapitre IV. — Produit du Domaine de l'Etat"),
    "ch5": ("miscellaneous", "ordinary", "Chapitre V. — Produits divers"),
    "loans": ("loan_funds", "exceptional", "Fonds d'emprunt"),
    "misc_exc": ("miscellaneous_receipts", "exceptional", "Recettes diverses"),
    "regions": ("regional_councils", "exceptional", "Recettes à la disposition des Conseils de Région"),
    "closed": ("closed_exercises", "closed", "Recettes affectées aux dépenses des exercices clos et périmés"),
    # sgt1939 nomenclature (budgets 1936-1938)
    "r_income": ("general_income_tax", "ordinary", "Impôt général sur les divers revenus : taxe personnelle et "
                 "contribution personnelle d'Etat"),
    "r_land_unbuilt": ("land_tax_unbuilt", "ordinary", "Impôts fonciers et sur les revenus d'immeubles : 1° "
                       "Propriété non bâtie (canouns, mradjas, khodors, achours, vigne et bétail)"),
    "r_land_built": ("land_tax_built", "ordinary", "Impôts fonciers et sur les revenus d'immeubles : 2° Propriété "
                     "bâtie : taxe locative des immeubles"),
    "r_patents": ("business_profits_patents", "ordinary", "Impôts sur les bénéfices commerciaux et industriels : "
                  "1° Patentes, bénéfices de guerre, redevance des mines"),
    "r_wages": ("wages_salaries", "ordinary", "Impôts sur les bénéfices commerciaux et industriels : 2° Impôt sur "
                "les traitements et salaires"),
    "r_securities": ("securities_income", "ordinary", "Impôt sur les revenus des valeurs mobilières, rentes "
                     "d'enzel, etc."),
    "r_assimilated": ("assimilated_taxes", "ordinary", "Taxes assimilées aux Contributions directes : poids et "
                      "mesures, visite des pharmacies, véhicules, etc."),
    "r_stamp": ("stamp_duties", "ordinary", "Droits de timbre"),
    "r_registration": ("registration_duties", "ordinary", "Droits d'enregistrement et de chancellerie"),
    "r_customs": ("customs_duties", "ordinary", "Droits de douane et droits maritimes"),
    "r_consumption": ("consumption_duties", "ordinary", "Droits de consommation"),
    "r_other_indirect": ("other_indirect_taxes", "ordinary", "Autres contributions indirectes"),
    "r_monopolies": ("monopolies", "ordinary", "Produit des Monopoles"),
    "r_posts": ("posts", "ordinary", "Produit des Postes"),
    "r_industrial": ("industrial_enterprises", "ordinary", "Produit d'exploitations industrielles"),
    "r_domain": ("state_domain", "ordinary", "Produit du Domaine"),
    "r_misc": ("miscellaneous", "ordinary", "Produits divers"),
}

SERVICE = {"fin": "finance", "sec": "general_secretariat", "int": "interior", "agr": "agriculture_economy",
           "edu": "education_fine_arts", "army": "army", "pw": "public_works", "just": "justice",
           "post": "posts_telegraphs", "unf": "unforeseen", "equip": "economic_equipment",
           "adm": "tunisian_administration"}
# nomenclatures 1926-1929 (sgt1925-sgt1930): chapter number -> service
OLD_ORD = {"o1": "fin", "o2": "post", "o3": "int", "o4": "agr", "o5": "edu", "o6": "army", "o7": "pw", "o8": "just",
           "o9": "unf", "o10": "equip"}
OLD_EXC = {"x1": "fin", "x2": "post", "x3": "int", "x4": "agr", "x5": "edu", "x6": "army", "x7": "pw", "x8": "just"}
LBL_OLD = {"fin": "Direction générale des Finances", "post": "Office des Postes et des Télégraphes",
           "int": "Direction générale de l'Intérieur",
           "agr": "Direction générale de l'Agriculture, du Commerce et de la Colonisation",
           "edu": "Direction générale de l'Instruction publique et des Beaux-Arts", "army": "Armée tunisienne",
           "pw": "Direction générale des Travaux Publics", "just": "Direction de la Justice",
           "unf": "Dépenses imprévues", "equip": "Dépenses d'outillage économique"}
ROMAN = ["Ier", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
# nomenclatures 1932 (sgt1935), 1935 (sgt1936), 1938 (sgt1939): chapter order and labels
NEW_ORDER = {"1932": ["fin", "sec", "int", "agr", "edu", "army", "pw", "just", "post", "unf"],
             "1935": ["fin", "sec", "int", "agr", "edu", "army", "pw", "just", "post", "unf"],
             "1938": ["fin", "sec", "post", "agr", "edu", "army", "pw", "just"]}
LBL_NEW = {"fin": "Direction générale des Finances", "sec": "Secrétariat général du Gouvernement tunisien",
           "int": "Direction générale de l'Intérieur",
           "agr": "Direction générale de l'Agriculture, du Commerce et de la Colonisation",
           "edu": "Direction générale de l'Instruction publique et des Beaux-Arts", "army": "Armée tunisienne",
           "pw": "Direction des Travaux Publics", "just": "Justice tunisienne",
           "post": "Office des Postes et des Télégraphes", "unf": "Dépenses imprévues"}
LBL_1935 = dict(LBL_NEW, fin="Direction des Finances", int="Direction de l'Intérieur",
                agr="Direction des Affaires Économiques", edu="Direction de l'Instruction publique et des Beaux-Arts")
LBL_1938 = dict(LBL_1935, int="Mémoire. — Direction de l'Intérieur", adm="Mémoire. — Administration tunisienne")

NOMENCLATURE = {  # printed in the heading of the designation column
    ("sgt1925", "receipts"): "nomenclature des budgets de 1916 à 1926", ("sgt1925", "expenditure"): "nomenclature de 1926",
    ("sgt1926", "receipts"): "nomenclature des budgets de 1916 à 1925", ("sgt1926", "expenditure"): "nomenclature de 1926",
    ("sgt1927", "receipts"): "nomenclature des budgets de 1917 à 1926", ("sgt1927", "expenditure"): "nomenclature de 1926",
    ("sgt1928", "receipts"): "nomenclature des budgets de 1918 à 1927", ("sgt1928", "expenditure"): "nomenclature de 1927",
    ("sgt1929", "receipts"): "nomenclature des budgets de 1919 à 1928", ("sgt1929", "expenditure"): "nomenclature de 1928",
    ("sgt1930", "receipts"): "nomenclature des budgets de 1920 à 1929", ("sgt1930", "expenditure"): "nomenclature de 1929",
    ("sgt1935", "receipts"): "nomenclature des budgets de 1932 à 1934", ("sgt1935", "expenditure"): "nomenclature de 1932",
    ("sgt1936", "receipts"): "nomenclature des budgets de 1933 à 1935", ("sgt1936", "expenditure"): "nomenclature de 1935",
    ("sgt1939", "receipts39"): "nomenclature des budgets de 1936 à 1938", ("sgt1939", "expenditure"): "nomenclature de 1938",
}
EXP_NOM = {"sgt1935": "1932", "sgt1936": "1935", "sgt1939": "1938"}
BASIS = {"receipts": ("actual", "Recettes réalisées"),
         "expenditure": ("actual", "Dépenses : droits constatés définitivement liquidés lors des règlements des "
                                   "budgets des exercices")}


def exp_item(sec, code):
    """(item, part, printed label) of an expenditure line."""
    ed = sec["ed"]
    if code == "closed":
        return "closed_exercises", "closed", "Dépenses des exercices clos et périmés"
    if code in OLD_ORD or code in OLD_EXC:
        part = "ordinary" if code.startswith("o") else "exceptional"
        svc = (OLD_ORD if part == "ordinary" else OLD_EXC)[code]
        n = int(code[1:])
        return f"{part}_{SERVICE[svc]}", part, f"Chapitre {ROMAN[n - 1]}. — {LBL_OLD[svc]}"
    part = "ordinary" if code.startswith("o_") else "exceptional"
    svc = code[2:]
    nom = EXP_NOM[ed]
    lbl = {"1932": LBL_NEW, "1935": LBL_1935, "1938": LBL_1938}[nom]
    order = NEW_ORDER[nom]
    if svc in order:
        txt = f"Chapitre {ROMAN[order.index(svc)]}. — {lbl[svc]}"
    else:
        txt = lbl[svc]
    return f"{part}_{SERVICE[svc]}", part, txt


def dl(sec):
    return [r for r in sec["rows"] if "cells" in r and not r["label"].startswith("Total")]


def row(sec, label):
    for r in sec["rows"]:
        if r["label"] == label:
            return r["cells"]
    return None


def base(sec, year):
    return {"census": sec["ed"], "table_id": sec["table"], "gallica_ark": sec["ark"], "source_page": sec["page"],
            "gallica_view": sec["view"], "year": year}


def mk(sec, cell, year, **dims):
    return dict(base(sec, year), **dims, value=cell.value, flag=cell.flag)


def months(year):
    return 9 if year == 1932 else 12


def cells_budget(sec):
    out = []
    t = "receipts" if sec["table"].startswith("receipts") else "expenditure"
    basis, basis_fr = BASIS[t]
    nom = NOMENCLATURE[(sec["ed"], sec["table"])]
    for r in dl(sec):
        if t == "receipts":
            item, part, lbl = REC[r["label"]]
        else:
            item, part, lbl = exp_item(sec, r["label"])
        for c in sec["cols"]:
            y = int(c)
            out.append(mk(sec, r["cells"][c], y, exercice_months=months(y), basis=basis, basis_fr=basis_fr,
                          part=part, part_fr=PART[part], item=item, item_fr=lbl, nomenclature_fr=nom,
                          unit="francs"))
    return out


def chk_budget(sec):
    out = "finance_budget_receipts" if sec["table"].startswith("receipts") else "finance_budget_expenditure"
    for c in sec["cols"]:
        if sec["table"] == "receipts39":
            ordin = [r for r in dl(sec) if REC[r["label"]][1] == "ordinary"]
            exc = [r for r in dl(sec) if REC[r["label"]][1] != "ordinary"]
            t1, t2, t = row(sec, "TotalI")[c].value, row(sec, "TotalII")[c].value, row(sec, "Total")[c].value
            CHK.eq(out, f"{where(sec)} {c}: Total du Titre Ier = ordinary lines",
                   ssum(r["cells"][c].value for r in ordin), t1)
            CHK.eq(out, f"{where(sec)} {c}: Total du Titre II = exceptional lines",
                   ssum(r["cells"][c].value for r in exc), t2)
            CHK.eq(out, f"{where(sec)} {c}: Total général = Titre Ier + Titre II", ssum([t1, t2]), t)
        else:
            CHK.eq(out, f"{where(sec)} {c}: Total général = sum of the lines",
                   ssum(r["cells"][c].value for r in dl(sec)), row(sec, "Total")[c].value)


# ----------------------------------------------------------------- dette tunisienne

DEBT_ACC = {"ch_cap": ("charges", "Charges", "capital", "Capital"),
            "ch_int": ("charges", "Charges", "interest", "Intérêts"),
            "pay_cap": ("payments", "Paiements ou conversions consommés depuis l'échéance jusqu'à la date de la "
                                    "prescription au profit de l'Etat", "capital", "Capital"),
            "pay_int": ("payments", "Paiements ou conversions consommés depuis l'échéance jusqu'à la date de la "
                                    "prescription au profit de l'Etat", "interest", "Intérêts")}
DEBT_ITEM = {
    "cert1870": "coupon_certificates_pre1870", "d5_1880": "debt_5pct_1880", "d4_1884": "perpetual_4pct_1884",
    "d35_1889": "redeemable_3_5pct_1889", "d3_1892": "redeemable_3pct_1892", "d3_1902": "redeemable_3pct_1902_1907",
    "d35_1903": "redeemable_3_5pct_1903", "d4_1912": "redeemable_4pct_1912", "d_1920": "loan_1920",
    "d_1932": "loan_1932", "d_1934": "loan_1934", "d_1937": "loan_1937_1938",
    "banque_algerie": "banque_algerie_advance",
    "rail_loans": "railway_loan_charges", "road_loans": "road_network_loan_charges",
    "mortgage_credit": "agricultural_mortgage_credit", "consolidation": "consolidation_expenditure",
    "regional_communal": "regional_communal_expenditure", "archeveche": "carthage_archbishopric_subsidy",
    "t_bizerte": "bizerte_fisheries_buyback", "t_medjerda": "medjerda_lines_guarantee",
    "t_tgm": "tgm_railway_buyback", "t_rail_deficit": "railway_operating_deficit",
    "t_military": "metropole_military_contribution", "t_postal": "postal_office_telephone_advances",
    "t_cheminots_1925": "railwaymen_allowance_1925", "t_rail_reserve": "railway_reserve_fund_reconstitution",
    "t_rail_past_deficits": "railway_past_deficits_settlement", "t_cheminots_mobilised": "mobilised_railwaymen_pay",
    "t_rail_reserve_payment": "railway_reserve_fund_payment", "t_work_accidents": "work_accident_annuities",
    "t_enzel": "enzel_annuities", "t_transport_tax": "rail_transport_tax_surplus",
    "t_other": "other_temporary_charges",
}
DEBT_GROUP_FR = "Charges temporaires diverses incombant au budget beylical"
BAL_ROWS = {"due_prescribed": ("due_prescribed", "Décomposition des restes à payer : échus, prescrits"),
            "due_cancelled": ("due_cancelled", "Décomposition des restes à payer : échus, annulés (sgt1939 only)"),
            "due_not_prescribed": ("due_not_prescribed", "Décomposition des restes à payer : échus, non prescrits"),
            "not_due": ("not_due", "Décomposition des restes à payer : non échus")}
DEBT_CHECK_ROWS = {"Totaux", "Totaux2", "A_reporter", "Report"}


# cells whose printed value is identified as the faulty one by a failed check (flag total_mismatch; value kept)
FLAGS = {("sgt1925", "debt", "cert1870", "pay_cap"): "total_mismatch",
         ("sgt1927", "debt_balance", "due_not_prescribed", "cap"): "total_mismatch",
         ("sgt1927", "debt_balance", "due_not_prescribed", "int"): "total_mismatch",
         ("sgt1928", "debt_balance", "due_not_prescribed", "cap"): "total_mismatch",
         ("sgt1928", "debt_balance", "due_not_prescribed", "int"): "total_mismatch",
         ("sgt1924", "patente", "Ouerghemma", "c6"): "total_mismatch",
         ("sgt1925", "patente", "1re Région ; Béja ; Béja", "c1"): "total_mismatch",
         ("sgt1925", "patente", "1re Région ; Tabarka ; Aïn-Rraham", "c1"): "total_mismatch",
         ("sgt1925", "patente", "4me Région ; Kairouan ; Djelass", "c2"): "total_mismatch",
         ("sgt1928", "patente", "Bizerte ; Bizerte ; Bizerte", "c3"): "total_mismatch",
         ("sgt1929", "patente", "Le Kef ; Le Kef ; Le Kef", "c34"): "total_mismatch",
         ("sgt1929", "patente", "Territoires militaire du Sud ;  ; Ouerghemma", "c50"): "total_mismatch",
         ("sgt1930", "patente", "Sousse ; Sousse ; Monastir", "c34"): "total_mismatch",
         ("sgt1930", "taxe", "5me Région ; Sfax ; La Skhira", "fr"): "total_mismatch"}


def with_flag(rec, sec, code, col):
    f = FLAGS.get((sec["ed"], sec["table"], code, col))
    if f:
        rec["flag"] = f
    return rec


def split_label(label):
    code, _, fr = label.partition(" = ")
    return code.strip(), fr.strip()


def debt_rows(sec):
    return [r for r in sec["rows"] if "cells" in r and r["label"].split(" = ")[0] not in DEBT_CHECK_ROWS]


def cells_debt(sec):
    out = []
    for r in debt_rows(sec):
        code, fr = split_label(r["label"])
        tmp = code.startswith("t_")
        for c in sec["cols"]:
            acc, acc_fr, comp, comp_fr = DEBT_ACC[c]
            out.append(with_flag(mk(sec, r["cells"][c], int(sec["year"]), period_fr=sec["period"],
                                  group="temporary_charges" if tmp else "debt",
                                  group_fr=DEBT_GROUP_FR if tmp else "", item=DEBT_ITEM[code], item_fr=fr,
                                  account=acc, account_fr=acc_fr, component=comp, component_fr=comp_fr,
                                  unit="francs"), sec, code, c))
    return out


def cells_debt_balance(sec):
    out = []
    for r in sec["rows"]:
        if "cells" not in r or r["label"] not in BAL_ROWS:
            continue
        st, st_fr = BAL_ROWS[r["label"]]
        for c, comp, comp_fr in (("cap", "capital", "Capital"), ("int", "interest", "Intérêts")):
            out.append(with_flag(mk(sec, r["cells"][c], int(sec["year"]), period_fr=sec["period"], status=st,
                                  status_fr=st_fr, component=comp, component_fr=comp_fr, unit="francs"),
                               sec, r["label"], c))
    return out


def chk_debt(secs):
    """Operations: Totaux = lines (with A reporter / Report across the two pages of sgt1930); the sums printed
    under the braces = capital + intérêts. Balance: Charges and Conversions et payements = Totaux of a); Reste à
    payer = Charges - Conversions; Total égal à celui ci-dessus = décomposition = Reste à payer; brace sums."""
    o, ob = "finance_public_debt", "finance_public_debt_balance"
    tot = {}
    for sec in [s for s in secs if s["table"] == "debt"]:
        carried = row(sec, "Report")
        if carried is not None:
            prev = tot.get(sec["ed"])
            for c in sec["cols"]:
                CHK.eq(o, f"{where(sec)} {c}: Report = A reporter of the previous page", prev[c].value,
                       carried[c].value)
        for t in ("A_reporter", "Totaux"):
            tr = row(sec, t)
            if tr is None:
                continue
            for c in sec["cols"]:
                parts = [r["cells"][c].value for r in debt_rows(sec)] + ([carried[c].value] if carried else [])
                CHK.eq(o, f"{where(sec)} {c}: {t} = lines" + (" + Report" if carried else ""), ssum(parts),
                       tr[c].value)
            tot[sec["ed"]] = tr
        t2 = row(sec, "Totaux2")
        if t2 is not None:
            tt = row(sec, "Totaux")
            CHK.eq(o, f"{where(sec)} charges: capital + intérêts (brace)", tt["ch_cap"].value + tt["ch_int"].value,
                   t2["ch_cap"].value)
            CHK.eq(o, f"{where(sec)} paiements: capital + intérêts (brace)",
                   tt["pay_cap"].value + tt["pay_int"].value, t2["pay_cap"].value)
    for sec in [s for s in secs if s["table"] == "debt_balance"]:
        tt = tot[sec["ed"]]
        g = {lab: row(sec, lab) for lab in ("charges", "payments", "remaining", "remaining_both", "Total",
                                            "total_both")}
        for c, a, b in (("cap", "ch_cap", "pay_cap"), ("int", "ch_int", "pay_int")):
            CHK.eq(ob, f"{where(sec)} {c}: Charges = Totaux of a)", tt[a].value, g["charges"][c].value)
            CHK.eq(ob, f"{where(sec)} {c}: Conversions et payements = Totaux of a)", tt[b].value,
                   g["payments"][c].value)
            CHK.eq(ob, f"{where(sec)} {c}: Reste à payer = Charges - Conversions et payements",
                   g["charges"][c].value - g["payments"][c].value, g["remaining"][c].value)
            CHK.eq(ob, f"{where(sec)} {c}: Total égal à celui ci-dessus = décomposition",
                   ssum(row(sec, k)[c].value for k in BAL_ROWS if row(sec, k) is not None), g["Total"][c].value)
            CHK.eq(ob, f"{where(sec)} {c}: Total égal à celui ci-dessus = Reste à payer", g["remaining"][c].value,
                   g["Total"][c].value)
        for lab, src in (("remaining_both", "remaining"), ("total_both", "Total")):
            CHK.eq(ob, f"{where(sec)} {lab}: capital + intérêts (brace)",
                   g[src]["cap"].value + g[src]["int"].value, g[lab]["cap"].value)


# ----------------------------------------------------------------- droit de patente

# class: (lower bound, upper bound, bénéfice moyen), francs, as printed in the column heads. Scale A (sgt1922-sgt1928):
# 15 classes, a 16th from sgt1927; scale B (sgt1929 on): 51 classes, brackets of 100.000 fr. from the 11th.
PAT_A = {1: (0, 1000, 500), 2: (1001, 2000, 1500), 3: (2001, 5000, 3500), 4: (5001, 10000, 7500),
         5: (10001, 20000, 15000), 6: (20001, 30000, 25000), 7: (30001, 50000, 40000),
         8: (50001, 75000, 62500), 9: (75001, 100000, 87500), 10: (100001, 200000, 150000),
         11: (200001, 500000, 350000), 12: (500001, 1000000, 750000), 13: (1000001, 2000000, 1500000),
         14: (2000001, 3000000, 2500000), 15: (3000001, 4000000, 3500000), 16: (4000001, 5000000, 4500000)}
PAT_B = {k: PAT_A[k] if k <= 10 else ((k - 9) * 100000 + 1, (k - 8) * 100000, (k - 9) * 100000 + 50000)
         for k in range(1, 54)}
SCALE_B = {"sgt1929", "sgt1930", "sgt1935", "sgt1936", "sgt1939"}


def pat_scale(ed):
    return PAT_B if ed in SCALE_B else PAT_A


PAT_CHECK = {"n", "montant"}


def fr_num(x):
    return f"{x:,}".replace(",", ".")


def pat_class_fr(k, ed):
    lo, hi, m = pat_scale(ed)[k]
    return (f"{k}{'re' if k == 1 else 'e'} classe : bénéfice de {fr_num(lo)} à {fr_num(hi)} fr., bénéfice moyen "
            f"{fr_num(m)} fr.")


def geo(label):
    """Row label 'région ; contrôle civil ; caïdat' (sgt1925 on) or 'caïdat' (sgt1922-sgt1924)."""
    parts = [x.strip() for x in label.split(" ; ")]
    if len(parts) == 1:
        return {"region": "", "controle_civil": "", "caidat": parts[0]}
    return {"region": parts[0], "controle_civil": parts[1], "caidat": parts[2]}


def pat_rows(secs, ed):
    """Merge the pages of one printing: {label: {col: (Cell, sec)}} in printed order."""
    rows = {}
    for sec in secs:
        if sec["ed"] != ed:
            continue
        for r in sec["rows"]:
            if "cells" in r:
                d = rows.setdefault(r["label"], {})
                for c, cell in r["cells"].items():
                    d[c] = (cell, sec)
    return rows


DERIVED = set()


def derive_patente(secs):
    """A class cell left '?' (digits hidden in the binding) = Nombre de patentables - the other classes of its row
    (flag derived_from_totals). Runs before the checks, so derived cells only enter the Totaux and Montant checks."""
    ps = [s for s in secs if s["table"] == "patente"]
    for ed in ORDER:
        for l, d in pat_rows(ps, ed).items():
            miss = [c for c, (cell, _) in d.items() if cell.value is None and c not in PAT_CHECK]
            if len(miss) == 1 and "n" in d and d["n"][0].value is not None:
                cell = d[miss[0]][0]
                cell.value = d["n"][0].value - ssum(x.value for c, (x, _) in d.items()
                                                    if c not in PAT_CHECK and c != miss[0])
                cell.flag = "derived_from_totals"
                DERIVED.add(id(cell))


def cells_patente(sec):
    out = []
    for r in sec["rows"]:
        if "cells" not in r or is_total(r["label"]) or r["label"].startswith("Sous-total"):
            continue
        g = geo(r["label"])
        for c, cell in r["cells"].items():
            if c in PAT_CHECK:
                continue
            k = int(c[1:])
            out.append(with_flag(mk(sec, cell, int(sec["year"]), profits_year=int(sec.get("profits", 0)) or None,
                                    **g, profit_class=k, profit_class_fr=pat_class_fr(k, sec["ed"]),
                                    mean_profit=pat_scale(sec["ed"])[k][2]), sec, r["label"], c))
    return out


def chk_patente(secs):
    """Nombre = sum of the classes (skipped for rows with a derived cell); Montant = sum of count x bénéfice moyen;
    Totaux = sum of the caïdats."""
    o = "finance_patente"
    ps = [s for s in secs if s["table"] == "patente"]
    for ed in ORDER:
        rows = pat_rows(ps, ed)
        if not rows:
            continue
        cls = sorted({int(c[1:]) for d in rows.values() for c in d if c not in PAT_CHECK})
        data = {l: d for l, d in rows.items() if not is_total(l) and not l.startswith("Sous-total")}
        for l, d in rows.items():
            w = f"{ed} {l}"
            if "n" in d and not any(id(x) in DERIVED for x, _ in d.values()):
                CHK.eq(o, f"{w}: Nombre de patentables = sum of the classes",
                       ssum(d[f"c{k}"][0].value for k in cls), d["n"][0].value)
            if "montant" in d:
                CHK.eq(o, f"{w}: Montant du bénéfice moyen = sum of count x bénéfice moyen",
                       ssum(d[f"c{k}"][0].value * pat_scale(ed)[k][2] for k in cls), d["montant"][0].value)
        tot = [l for l in rows if is_total(l)]
        for t in tot:
            for c in rows[t]:
                CHK.eq(o, f"{ed} {t} {c}: Totaux = sum of the caïdats",
                       ssum(d[c][0].value for d in data.values()), rows[t][c][0].value)


PATC_M = {"n": ("taxpayers", "Nombre de patentables", "taxpayers"),
          "montant": ("mean_profit_total", "Montant du bénéfice moyen par caïdat", "francs")}


def cells_patente_caidat(sec):
    out = []
    for r in sec["rows"]:
        if "cells" not in r or is_total(r["label"]):
            continue
        for c, (m, mfr, u) in PATC_M.items():
            out.append(mk(sec, r["cells"][c], int(sec["year"]), profits_year=int(sec["profits"]), **geo(r["label"]),
                          measure=m, measure_fr=mfr, unit=u))
    return out


def chk_patente_caidat(secs):
    o = "finance_patente_caidat"
    for sec in [s for s in secs if s["table"] == "patente_caidat"]:
        check_col_totals(CHK, o, sec)


# ----------------------------------------------------------------- taxe personnelle

TAXE_NAT = {"fr": ("french", "Français"), "it": ("italian", "Italiens"), "uk": ("british_maltese", "Anglais et Maltais"),
            "es": ("spanish", "Espagnols"), "gr": ("greek", "Grecs"), "oth": ("other_european", "Autres Européens"),
            "tun": ("tunisian", "Sujets tunisiens")}
TAXE_EUR = ["fr", "it", "uk", "es", "gr", "oth"]


def cells_taxe(sec):
    out = []
    for r in sec["rows"]:
        if "cells" not in r or is_total(r["label"]):
            continue
        for c, cell in r["cells"].items():
            if c not in TAXE_NAT or cell.flag == "not_applicable":
                continue          # '-': nothing printed in that cell for that line (bracketed caïdats)
            nat, nat_fr = TAXE_NAT[c]
            out.append(with_flag(mk(sec, cell, int(sec["year"]), **geo(r["label"]), nationality=nat,
                                    nationality_fr=nat_fr), sec, r["label"], c))
    return out


def chk_taxe(secs):
    """Total des Européens = the six European columns; Total = Européens + Sujets tunisiens (for bracketed caïdats:
    over the lines of the bracket); Totaux = sum of the lines; sous-totaux de région/contrôle where printed."""
    o = "finance_taxe_personnelle"
    for sec in [s for s in secs if s["table"] == "taxe"]:
        rows = [r for r in sec["rows"] if "cells" in r]
        for r in rows:
            c = r["cells"]
            if c["eur"].value is not None and all(c[k].value is not None for k in TAXE_EUR):
                CHK.eq(o, f"{where(sec)} {r['label']}: Total des Européens = six nationalities",
                       ssum(c[k].value for k in TAXE_EUR), c["eur"].value)
            if c["tot"].value is not None:
                grp = [r] + ([x for x in rows if x["label"] in r["label"].split(", ")] if ", " in r["label"] else [])
                CHK.eq(o, f"{where(sec)} {r['label']}: Total = Européens + Sujets tunisiens",
                       ssum(x["cells"][k].value for x in grp for k in ("eur", "tun")
                            if x["cells"][k].value is not None), c["tot"].value)
        data = [r for r in rows if not is_total(r["label"]) and not r["label"].startswith("Sous-total")]
        for t in [r for r in rows if is_total(r["label"])]:
            for k in sec["cols"]:
                CHK.eq(o, f"{where(sec)} {t['label']} {k}: Totaux = sum of the lines",
                       ssum(x["cells"][k].value for x in data if x["cells"][k].value is not None), t["cells"][k].value)


# ----------------------------------------------------------------- selection (rule 4)

def select(recs, key):
    """Rule 4: latest edition printing the cell (a legible, aligned printing first)."""
    by = defaultdict(list)
    for r in recs:
        by[tuple(r[k] for k in key)].append(r)
    kept, n, diffs = [], 0, []
    for k, rs in by.items():
        rs.sort(key=lambda r: ORDER.index(r["census"]))
        legible = [r for r in rs if r["value"] is not None]
        aligned = [r for r in legible if r["flag"] != "row_realigned"]
        last = (aligned or legible or rs)[-1]
        for r in rs:
            if r is last or r["value"] is None:
                continue
            n += 1
            if r["value"] != last["value"]:
                diffs.append((k, r["census"], r["value"], last["census"], last["value"]))
        kept.append(last)
    return kept, n, diffs


def select_all(recs, key):
    """Rule 5: every edition kept."""
    return list(recs), 0, []


# ----------------------------------------------------------------- documentation

DOC = {
    "census": "edition the value is taken from (rule 4 tables: the latest edition printing that year)",
    "table_id": "transcription section",
    "gallica_ark": "Gallica volume ark (views are numbered within a volume)",
    "source_page": "printed page number",
    "gallica_view": "Gallica view (fNNNN)",
    "year": "budget year (exercice) as printed in the column head",
    "exercice_months": "length of the exercice in months: 9 for 1932 (printed \"1932 (9 mois)\" in sgt1935, the "
                       "transition to the April-March budget year), 12 otherwise (printed \"(12 mois)\" for 1933 "
                       "and 1934 in sgt1935, not printed elsewhere)",
    "basis": "`actual` (réalisations: realised receipts, expenditure as finally settled); the chapter prints no "
             "budget forecasts (prévisions)",
    "basis_fr": "printed table subtitle",
    "part": "`ordinary` (Titre premier / Première partie), `exceptional` (Titre II / Deuxième partie), `closed` "
            "(Titre III / Troisième partie: exercices clos et périmés)",
    "part_fr": "printed part heading",
    "item": "budget line code (English). Expenditure: `<part>_<service>`, stable across the renumbering of the "
            "chapters (1932, 1938)",
    "item_fr": "printed line label, with the chapter number of that edition's nomenclature",
    "nomenclature_fr": "nomenclature named in the table head of the printing the value comes from",
    "unit": "unit of `value`",
    "value": "printed amount (» = 0), francs with centimes",
    "flag": "empty, or `ocr_corrected` (image reading differs from the Gallica OCR)",
}

RULE4 = ("Printed for overlapping windows of exercices: each exercice is taken from the **latest** edition that "
         "prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on "
         "its own page image, is compared below.")

BUDGET_FAILS = (
    "Printed errors (each failing figure re-read on zoomed native-resolution crops; the same standing type was "
    "reused from sgt1925 to sgt1930, so the same errors recur in every printing): receipts 1918 total "
    "115.996.425 65 for lines summing to 110.996.425 65 (5.000.000 more; Chapitre II is printed 31.131.869 63 in "
    "every edition); 1919 total 159.571.187 15 for 159.571.097 15 (90); 1920 total 230.414.262 05 for "
    "230.414.265 05 (-3); 1923 total 273.494.795 97 for 273.424.795 97 (70.000). sgt1929 prints 1927 Produits divers "
    "14.055.295 30 (sgt1928 and sgt1930: 14.055.235 30, which the total requires; kept from sgt1930). Expenditure "
    "1920 total 247.894.268 84 for 247.894.258 84 (10); 1921 total 323.893.637 49 for 323.893.837 09 (-199,60); 1922 "
    "total 358.708.699 43 for 358.708.657 43 (42); 1923 total 316.939.974 19 for 316.939.974 22 (-0,03); sgt1939 "
    "1936 total 728.768.074 68 for 729.768.074 68 (-1.000.000; only printing). The faulty cell cannot be "
    "identified in any of these (the line items agree across all independent printings), so no cell is flagged "
    "`total_mismatch`.")

TABLES = {
    "finance_budget_receipts": dict(
        secs=["receipts", "receipts39"], cells=cells_budget, key=["year", "item"], select=select,
        dims=["exercice_months", "basis", "basis_fr", "part", "part_fr", "item", "item_fr", "nomenclature_fr",
              "unit"],
        title_fr="Budget annuel. a) Recettes réalisées",
        title_en="Annual budget of the Regency: realised receipts by budget chapter (exercices 1915-1938)",
        unit="Unit: francs (centimes kept); value_type: francs.",
        rule=RULE4,
        paras=["Printed sgt1925-sgt1939 (not in sgt1922-sgt1924): ten exercices per edition up to sgt1930 (sgt1925: "
               "1915-1924, ..., sgt1930: 1920-1929), three from sgt1935 (1932-1934, 1933-1935, 1936-1938). Exercices "
               "1930 and 1931 are printed in no edition of the series (sgt1931-sgt1934 are not in the collection). "
               "Lines: Titre I (Première partie up to sgt1927) ressources ordinaires, chapitres I-V; Titre II "
               "recettes sur ressources exceptionnelles (fonds d'emprunt, recettes diverses, and recettes à la "
               "disposition des Conseils de Région, sgt1925-sgt1930); Titre III recettes affectées aux dépenses des "
               "exercices clos et périmés (» in every printing). sgt1939 uses a new detailed nomenclature for the "
               "ordinary resources (17 lines, by tax) and prints Total du Titre Ier and Total du Titre II "
               "(checks only); its exercices 1936-1938 overlap no other printing.",
               "All figures are actual results (réalisations); the chapter prints no forecasts. The printed Total "
               "général is a check, not stored."]),
    "finance_budget_expenditure": dict(
        secs=["expenditure"], cells=cells_budget, key=["year", "item"], select=select,
        dims=["exercice_months", "basis", "basis_fr", "part", "part_fr", "item", "item_fr", "nomenclature_fr",
              "unit"],
        title_fr="Budget annuel. b) Dépenses : droits constatés définitivement liquidés lors des règlements des "
                 "budgets des exercices",
        title_en="Annual budget of the Regency: expenditure as finally settled, by service (exercices 1915-1938)",
        unit="Unit: francs (centimes kept); value_type: francs.",
        rule=RULE4,
        paras=["Printed sgt1925-sgt1939, same windows as the receipts. Lines: Titre I dépenses sur ressources "
               "ordinaires and Titre II dépenses sur ressources exceptionnelles ou spéciales, by service (chapitre), "
               "and Titre III dépenses des exercices clos et périmés. The chapters are renumbered twice: nomenclature "
               "1926-1929 (I Finances, II Postes et Télégraphes, III Intérieur, IV Agriculture-Commerce-"
               "Colonisation, V Instruction publique, VI Armée, VII Travaux publics, VIII Justice, IX Dépenses "
               "imprévues, from the 1927 nomenclature X Dépenses d'outillage économique), nomenclature 1932 and 1935 "
               "(II Secrétariat général du Gouvernement tunisien, VIII Justice tunisienne, IX Postes, X imprévues; "
               "from 1935 IV is the Direction des Affaires Économiques) and 1938 (III Postes; Intérieur and "
               "Administration tunisienne as \"Mémoire\" lines with 1936 figures only). `item` names the service, "
               "so the same service keeps its code across renumberings; `item_fr` keeps the printed chapter "
               "number. The Affaires Économiques line is coded with the Agriculture line it replaces "
               "(`agriculture_economy`).",
               "All figures are actual results; the printed Total général is a check, not stored."]),
}

# ----------------------------------------------------------------- tables after the budget

FLAGDOC = ("empty, or `ocr_corrected` (image reading differs from the Gallica OCR), `total_mismatch` (printed value "
           "kept; identified by a failed check as the faulty cell, see Validation), `illegible` (value NA), "
           "`not_applicable` (nothing printed, value NA), `derived_from_totals` (digits hidden in the binding; value = "
           "the printed row total minus the other cells of the row, see the notes)")
RULE5 = ("Printed once per edition, each printing for its own period (cumulative to a later year, or another "
         "tax year): every edition is kept (SPEC_ADDENDUM rule 5); `census` is the edition, `year` the year the "
         "printing refers to.")
DOC5 = {"flag": FLAGDOC, "census": "edition (source code; every edition printing the table is kept, rule 5)"}

DOC.update({
    "period_fr": "period covered, as printed in the title (cumulative operations since 1884)",
    "group": "`temporary_charges` for the lines printed under \"Charges temporaires diverses incombant au budget "
             "beylical\" (a brace up to sgt1930, a heading in sgt1935), `debt` otherwise",
    "group_fr": "printed group heading (empty for the debt lines proper)",
    "account": "`charges` (charges: amounts due since the origin) or `payments` (paiements ou conversions "
               "consommés depuis l'échéance jusqu'à la date de la prescription au profit de l'Etat)",
    "account_fr": "printed column-group heading",
    "component": "`capital` or `interest` (intérêts)",
    "component_fr": "printed column heading",
    "status": "décomposition des restes à payer: `due_prescribed` (échus, prescrits), `due_not_prescribed` "
              "(échus, non prescrits), `due_cancelled` (échus, annulés: sgt1939 only), `not_due` (non échus)",
    "status_fr": "printed line label",
})

RULE4_DEBT = ("Each printing gives the operations cumulated from 1884 to a year named in its title (1921, 1923, "
              "1924, 1924, 1925, 1927, 1934, 1935, 1938): one series by that year, each year from the **latest** "
              "edition printing it (SPEC_ADDENDUM rule 4; `census` = that edition). Only 1924 is printed twice "
              "(sgt1927 and sgt1928, same standing type): sgt1928 is stored and the sgt1927 printing, read "
              "independently on its own image, is compared below.")
DOC4 = {"flag": FLAGDOC, "census": "edition the value is taken from (the latest edition printing that year; 1924: sgt1928, "
                  "sgt1927 compared)",
        "year": "last year of the cumulative period (\"de 1884 à <year>\" in the title)"}

DEBT_PARAS = [
    "Printed sgt1925-sgt1939 (not in sgt1922-sgt1924, whose Finances chapter opens with the taxe personnelle). "
    "sgt1925: \"Tableau récapitulatif et balance des opérations auxquelles a donné lieu le service de la dette "
    "tunisienne de 1884 à 1921\" (one page); sgt1926-sgt1935: \"a) Opérations auxquelles a donné lieu le service de "
    "la dette tunisienne de 1884 à <year>\"; sgt1936-sgt1939: \"Opérations relatives au service de la dette "
    "tunisienne de 1884 à <year>\". sgt1930 spreads the table over two pages (A reporter / Report).",
    "One row per printed cell: debt or charge line x account (charges; paiements ou conversions) x component "
    "(capital; intérêts). The lines change across editions: new loans (1920, 1932, 1934, 1937-1938), new charges "
    "under the brace \"Charges temporaires diverses incombant au budget beylical\" up to sgt1930, and from sgt1935 a "
    "regrouping (railway loan charges, road network loans, agricultural mortgage credit, State participation in "
    "consolidation and in regional and communal expenditure, subsidy to the Archbishopric of Carthage; the remaining "
    "temporary charges as \"Avances à l'Office Postal\" and \"Autres charges temporaires diverses\", sgt1939 "
    "\"Autres charges temporaires diverses incombant au budget beylical\" alone). `item` codes are stable where the "
    "printed line is the same; regrouped lines get new codes. The printed Totaux, the A reporter / Report lines "
    "(sgt1930) and the sums printed under the braces (charges capital + intérêts; paiements capital + intérêts) are "
    "checks, not stored. Part b) (balance) is in `finance_public_debt_balance`.",
]
DEBT_FAILS = (
    "Failed checks, each re-read on zoomed native-resolution crops (printed errors): sgt1925, paiements capital: the "
    "lines sum to 518.887.615 13 against the printed Totaux 521.887.985 13 (3.000.370 more). The Certificats de "
    "coupons line is printed 6.884.838 70 here and 9.884.838 70 in every later edition: the 3.000.000 is that cell "
    "(flagged `total_mismatch`, printed value kept); the remaining 370 cannot be placed. sgt1929, charges intérêts: "
    "the lines sum to 353.693.320 69 (also printed in the balance), the Totaux line prints 353.693.320 62 (zoomed), "
    "and the brace sum 1.465.949.248 51 follows the 62; a misprinted total, no cell flagged. sgt1936, charges "
    "capital: the lines sum to 2.108.586.561 67, the Totaux (and the balance) print 2.107.586.561 67 (1.000.000 "
    "less); every line re-read, no cell can be identified.")
BAL_PARAS = [
    "Printed below (sgt1925-sgt1930) or on the page after (sgt1935-sgt1939) the operations table: Charges and "
    "Conversions et payements (the Totaux of the operations table), Reste à payer, its décomposition (échus: "
    "prescrits, non prescrits, and in sgt1939 annulés; non échus) and \"Total égal à celui ci-dessus\", in capital "
    "and intérêts, with the capital + intérêts sums under braces. Only the décomposition is stored (it is the only "
    "information not in `finance_public_debt`); the other lines are checks.",
]
BAL_FAILS = (
    "Failed checks, each re-read on zoomed native-resolution crops (printed errors): sgt1925, the brace sum under "
    "the Total égal à celui ci-dessus is printed 416.138.289 18 for 461.138.289 18 (printed correctly under Reste à "
    "payer; transposed digits). sgt1927 and sgt1928 (same standing type): the décomposition sums to 489.407.045 58 "
    "(capital) and 54.918.534 87 (intérêts), printed so in the Total line, whereas Reste à payer is 526.835.694 33 "
    "and 17.489.886 12; the brace sums agree (544.325.580 45). The difference, 37.428.648 75, moves between the "
    "capital and intérêts of the échus non prescrits line (6.548.197 02 and 54.687.225 55; 43.976.845 77 and "
    "17.258.576 80 would balance): both cells flagged `total_mismatch`, printed values kept. sgt1929: the balance "
    "prints Charges intérêts 353.693.320 69, the operations Totaux 353.693.320 62 (see `finance_public_debt`). "
    "sgt1935: the balance prints Conversions et payements capital 1.036.109.389 14 against 1.056.109.389 14 in the "
    "operations table (whose lines give 1.056...), and Reste à payer 967.634.759 follows the 1.036 figure; the "
    "décomposition sums to the printed Reste à payer, so the stored cells are consistent with the balance but "
    "20.000.000 short of the operations table; no cell identified. sgt1936: the capital décomposition sums to "
    "969.423.244 85, the Reste à payer and Total print 969.432.244 85 (9.000; transposed digits somewhere in the "
    "décomposition or the total), no cell identified.")

TABLES.update({
    "finance_public_debt": dict(
        secs=["debt"], cells=cells_debt, key=["year", "item", "account", "component"], select=select,
        fails=DEBT_FAILS,
        dims=["period_fr", "group", "group_fr", "item", "item_fr", "account", "account_fr", "component",
              "component_fr", "unit"],
        doc=dict(DOC4,
                 item="debt or charge line code (English), stable across editions",
                 item_fr="printed line label",
                 value="printed amount (» = 0), francs with centimes, cumulative since 1884"),
        title_fr="Dette tunisienne. a) Opérations auxquelles a donné lieu le service de la dette tunisienne "
                 "depuis 1884",
        title_en="Tunisian public debt: cumulative charges and payments (capital, interest) by loan and charge, "
                 "since 1884",
        unit="Unit: francs (centimes kept); value_type: francs.",
        rule=RULE4_DEBT, paras=DEBT_PARAS),
    "finance_public_debt_balance": dict(
        secs=["debt_balance"], cells=cells_debt_balance, key=["year", "status", "component"], select=select,
        fails=BAL_FAILS,
        dims=["period_fr", "status", "status_fr", "component", "component_fr", "unit"],
        doc=dict(DOC4, value="printed amount (» = 0), francs with centimes"),
        title_fr="Dette tunisienne. b) Balance des opérations",
        title_en="Tunisian public debt: balance of operations since 1884, breakdown of the amounts remaining to "
                 "be paid",
        unit="Unit: francs (centimes kept); value_type: francs.",
        rule=RULE4_DEBT, paras=BAL_PARAS),
})

DOC.update({
    "nationality": "", "nationality_fr": "",
    "measure": "what `value` counts", "measure_fr": "printed column head",
    "profits_year": "year of the profits taxed (\"bénéfices de <year>\"), when the title prints it; empty otherwise",
    "region": "région as printed (sgt1925 on; \"Territoires militaires du Sud\" for the southern caïdats); empty "
              "when the table lists caïdats only",
    "controle_civil": "contrôle civil as printed (sgt1925 on); empty when the table lists caïdats only",
    "caidat": "caïdat as printed",
    "profit_class": "class of profit (1 to 15)",
    "profit_class_fr": "printed column head: class, bracket of profit and bénéfice moyen",
    "mean_profit": "bénéfice moyen of the class (francs), as printed in the column head",
})
PAT_PARAS = [
    "Printed in every edition sgt1922-sgt1930 as a two-page spread (sgt1922-sgt1924 with the right-hand page "
    "scanned sideways; sgt1929 and sgt1930 on a folding plate, f259 and f793). Rows: caïdats (sgt1922-sgt1924, 25 "
    "to 33 caïdats, labels as printed, e.g. \"Kef (le)-Tadjerouine\", \"Tunis et Banlieue\"); from sgt1925 by région "
    "(1re-5me Région and Territoires militaires du Sud; from sgt1928 named by the chef-lieu de région, Bizerte, Tunis, "
    "Le Kef, Sousse, Sfax), contrôle civil and caïdat. The tax year is printed from sgt1926 (\"Bénéfices de l'année "
    "1925 — Imposés en 1926\", ...); sgt1922-sgt1925 print none (`year` = edition year, `profits_year` empty).",
    "Columns: one per class of profit, with its bracket and bénéfice moyen. Scale A (sgt1922-sgt1928): 15 classes "
    "(1re: 0 à 1.000 fr., moyen 500 ... 15e: 3.000.001 à 4.000.000, moyen 3.500.000), a 16th (4.000.001 à 5.000.000, "
    "moyen 4.500.000) from sgt1927. Scale B (sgt1929, sgt1930): classes 1-10 as before, then brackets of 100.000 fr. "
    "(11e: 200.001 à 300.000, moyen 250.000 ... 51e: 4.200.001 à 4.300.000, moyen 4.250.000); sgt1930 prints the 1st to "
    "50th class and a last column headed \"53e classe\" (4.400.001 à 4.500.000, moyen 4.450.000). `profit_class` and "
    "`mean_profit` follow the printed head, so the same class number means a different bracket in the two scales. "
    "Every printed cell is stored, » as 0 (most cells of the wide scale are 0).",
    "sgt1927: the 4th class column is printed against the gutter and the last digit is hidden in the binding for "
    "L'Arad, Hemmama, Gafsa, Djerid, Djerba, Ouerghema and the Totaux; these cells are derived as Nombre de "
    "patentables minus the other classes of the row (flag `derived_from_totals`); the derived values agree with the "
    "visible leading digits, the Montant of each row and the column Totaux. The Nombre check is not counted for "
    "these rows.",
    "Not stored (checks only): Nombre de patentables (row total), the Totaux line, and the Montant du bénéfice moyen "
    "par caïdat (sum over the classes of count x bénéfice moyen; left empty on the sgt1930 plate). From sgt1935 the "
    "table prints only these two columns per caïdat: see `finance_patente_caidat`.",
]
PAT_FAILS = (
    "Failed checks, each re-read on zoomed native-resolution crops (printed values kept). Every class column agrees "
    "with its printed Totaux except where a class cell is identified as faulty (flag `total_mismatch`): sgt1924 "
    "Ouerghemma 6th class printed » (the Nombre 590, the Montant 980.000 and the column Totaux 191 all require 1); "
    "sgt1925 Béja 1st class 433 (the Nombre 964 and, with Aïn-Rraham, the Totaux 15.953 require 443), Aïn-Rraham "
    "1st class 133 (the Nombre 255 and the Montant 531.000 require 113), Djelass 2nd class 233 (the Nombre 933, the "
    "Montant 1.156.000 and the Totaux 11.819 require 238); sgt1928 Bizerte 3rd class 217 (the Nombre 1.617, the "
    "Montant 7.632.500 and the Totaux 6.160 require 257); sgt1929 Le Kef 6 in the 34th class and Ouerghemma 7 in the "
    "50th class, sgt1930 Monastir 5 in the 34th class: isolated figures in otherwise empty columns, excluded by the "
    "Nombre, the Montant and the Totaux (stray type on the standing plate). The other failures are misprinted "
    "check figures, no stored cell involved: the Montant du bénéfice moyen of sgt1922 Gafsa (474.500; the classes "
    "give 710.500, which the Totaux montant 88.928.500 requires); sgt1923 Béja (+90.000), Monastir (-50.000), Tunis "
    "(-3.634.000) and the Totaux line (89.453.000, the sum of the printed Montants, against 93.047.000 from the "
    "classes, whose column totals all agree); sgt1925 Béja printed \"2.466\" (and the Totaux montant 133.429.000, "
    "which no reading of the Montant column reproduces); sgt1926 Souk-el-Arba (-3.000), Tunis banlieue (-473.000), "
    "Tadjérouine (-1.000), Mahdia (+500), La Skira (-170.000), Djebéniana (+256.500), L'Arad (-150.000) and the Totaux "
    "line; sgt1928 Souassi (291.000 for 291.500, and the Totaux montant by 500); sgt1930 Zlass Nombre printed 230 "
    "for 220 (the classes and the Totaux Nombre 36.560 require 220).")
TABLES["finance_patente"] = dict(
    secs=["patente"], cells=cells_patente, key=["census", "year", "caidat", "profit_class"], select=select_all,
    fails=PAT_FAILS,
    dims=["profits_year", "region", "controle_civil", "caidat", "profit_class", "profit_class_fr", "mean_profit"],
    doc=dict(DOC5, year="tax year (\"imposés en <year>\"; sgt1922-sgt1925 print no year: the edition year)",
             value="number of taxpayers (assujettis) in the class"),
    title_fr="Droit de patente. Etat des assujettis au droit de patente",
    title_en="Business licence tax (droit de patente): taxpayers by caïdat and class of profit",
    unit="Unit: number of taxpayers (assujettis); value_type: count.",
    rule=RULE5, paras=PAT_PARAS)

TAXE_PARAS = [
    "Printed in every edition sgt1922-sgt1930 (not from sgt1935): one page in sgt1922-sgt1924 (\"Etat des "
    "contribuables imposés à la taxe personnelle\", caïdats only), a two-page spread from sgt1925 (by région, "
    "contrôle civil and caïdat; \"soumis à\" from sgt1926). No year is printed: `year` is the edition year. The list "
    "of caïdats changes (Djerba from sgt1923, Djebeniana from sgt1927, Tatahouine from sgt1928; sgt1922-sgt1924 "
    "bracket Ouled-Aoun and Ouled-Ayar, with the European columns and the Total printed once for both and the Sujets "
    "tunisiens separately: stored as caïdat \"Ouled-Aoun, Ouled-Ayar\" for the European nationalities and under each "
    "caïdat for the Tunisians).",
    "Columns stored: Français, Italiens, Anglais et Maltais, Espagnols, Grecs, Autres Européens, Sujets tunisiens. "
    "Total des Européens, Total and the Totaux line are checks, not stored.",
]
TAXE_FAILS = (
    "Failed checks, each re-read on zoomed native-resolution crops. sgt1930 La Skhira: Français printed 49 (legible "
    "on both sides of the gutter), the Total des Européens 56, the Total 7.667 and the Totaux of the Français column "
    "(24.490) all require 40: the Français cell is flagged `total_mismatch` (printed value kept). Misprinted check "
    "figures, no stored cell involved: sgt1925 Total of Zaghouan printed 11.166 for 11.156 and of L'Arad 18.504 for "
    "18.514 (the two errors cancel in the Totaux); sgt1929 Total of Sfax printed 26.350 for 26.530 (the Totaux "
    "623.943 is right).")
TABLES["finance_taxe_personnelle"] = dict(
    secs=["taxe"], cells=cells_taxe, key=["census", "year", "caidat", "nationality"], select=select_all,
    fails=TAXE_FAILS,
    dims=["region", "controle_civil", "caidat", "nationality", "nationality_fr"],
    doc=dict(DOC5, year="year of the roll (no year printed: the edition year)",
             caidat="caïdat as printed; two caïdats joined by \", \" = a figure printed once for both (bracket)",
             nationality="nationality of the taxpayers: `french`, `italian`, `british_maltese` (Anglais et "
                         "Maltais), `spanish`, `greek`, `other_european`, `tunisian` (sujets tunisiens)",
             nationality_fr="printed column head", value="number of taxpayers (contribuables imposés)"),
    title_fr="Taxe personnelle. Etat des contribuables imposés à la taxe personnelle",
    title_en="Personal tax (taxe personnelle): taxpayers by caïdat and nationality",
    unit="Unit: number of taxpayers (contribuables imposés); value_type: count.",
    rule=RULE5, paras=TAXE_PARAS)

TABLES["finance_patente_caidat"] = dict(
    secs=["patente_caidat"], cells=cells_patente_caidat, key=["census", "year", "caidat", "measure"],
    select=select_all,
    dims=["profits_year", "region", "controle_civil", "caidat", "measure", "measure_fr", "unit"],
    doc=dict(DOC5, year="tax year (\"imposés en <year>\")",
             region="chef-lieu de région as printed, or \"Territoires Militaires du Sud\"",
             caidat="caïdat as printed; \"Souk-el-Khemis, Souk-el-Arba\" = the two caïdats bracketed with one "
                    "figure",
             measure="`taxpayers` (nombre de patentables) or `mean_profit_total` (montant du bénéfice moyen par "
                     "caïdat: the sum of the bénéfices moyens of the classes of the caïdat's taxpayers)",
             measure_fr="printed column head", value="printed value (» = 0)"),
    title_fr="Droit de patente. Etat des assujettis au droit de patente (nombre et montant du bénéfice moyen par "
             "caïdat)",
    title_en="Business licence tax (droit de patente): number of taxpayers and total mean profit by caïdat",
    unit="Units: `taxpayers` count, `mean_profit_total` francs; value_type: mixed (count and francs).",
    rule=RULE5,
    paras=["Printed in sgt1935, sgt1936 and sgt1939 (bénéfices de 1934, 1935 and 1938, imposés en 1935, 1936 and "
           "1939), one page each: the classes of profit are no longer printed, only the Nombre de patentables and "
           "the Montant du bénéfice moyen par caïdat, by chef-lieu de région, contrôle civil and caïdat. Earlier "
           "editions print the same two columns next to the classes (`finance_patente`); they are not stored "
           "there because they are sums of the stored class cells. The Totaux line is a check, not stored."])

GROUP_CHECKS = [chk_debt, chk_patente, chk_patente_caidat, chk_taxe]


SURVEY = {
    "sgt1922": "f185 chapter X title (Finances); f186 blank; f187 taxe personnelle (contribuables imposés by caïdat "
               "and nationality) [transcribed]; f188-f211 achour: superficies ensemencées by caïdat and yield class, for blé, "
               "orge, avoine, fèves, pois chiches, maïs, sorgho, lin, each in three tables a) européens, b) "
               "indigènes, c) récapitulation (one page each); f212|f213 canoun des dattiers a) relevé par caïdat du "
               "nombre d'arbres d'après leur âge au 1er novembre 1922; f214|f215 b) répartition des arbres "
               "imposables par catégorie du tarif (degla, communs); f216|f217 canoun des oliviers a) relevé par "
               "caïdat d'après l'âge; f218|f219 b) répartition par catégorie du tarif; f220|f221 c) répartition "
               "entre européens et indigènes (arbres, articles de matrice, comptes individuels); f222|f223 droit de "
               "patente (état des assujettis by class of profit) [transcribed]; f224|f225 taxe sur le bétail a) rôles européens "
               "(by caïdat and species, imposables / non imposables); f226|f227 b) rôles indigènes; f228|f229 c) "
               "récapitulation; f230 blank. f231 = chapter XI Agriculture.",
    "sgt1923": "f675 title; f676 blank; f677 taxe personnelle [transcribed]; f678-f701 achour (8 crops x a/b/c); f702|f703 canoun "
               "dattiers a) (1923); f704|f705 b); f706|f707 canoun oliviers a); f708 blank (verso); f709 b) "
               "(second page); f710|f711 c); f712|f713 droit de patente [transcribed]; f714|f715 bétail a); f716|f717 b); "
               "f718|f719 c); f720 blank. f721 = chapter XI.",
    "sgt1924": "f1171 title; f1172 blank; f1173 taxe personnelle [transcribed]; f1174-f1197 achour (8 crops x a/b/c); f1198|f1199 "
               "canoun dattiers a) (1924); f1200|f1201 b); f1202|f1203 canoun oliviers a); f1204|f1205 b); "
               "f1206|f1207 c); f1208|f1209 droit de patente [transcribed]; f1210|f1211 bétail a); f1212|f1213 b); f1214|f1215 "
               "c); f1216 blank. f1217 = chapter XI.",
    "sgt1925": "f211 title; f212|f213 budget annuel (1915-1924) a) recettes réalisées [transcribed]; f214|f215 b) "
               "dépenses [transcribed]; f216 dette tunisienne (récapitulatif et balance des opérations 1884-1921) "
               "[transcribed]; "
               "f217 blank; f218|f219 taxe personnelle (by région, contrôle civil, caïdat and nationality) [transcribed]; "
               "f220-f267 achour, 8 crops x a) européens, b) indigènes, c) récapitulation, each a two-page spread "
               "(by région / contrôle civil / caïdat); f268|f269 canoun dattiers a) (1924); f270|f271 b); f272|f273 "
               "canoun oliviers a) (1925); f274|f275 b); f276|f277 c); f278|f279 droit de patente [transcribed]; f280|f281 "
               "bétail a) européens; f282|f283 b) indigènes; f284|f285 c) récapitulation; f286 blank. f287 = "
               "chapter XI.",
    "sgt1926": "f767 title; f768|f769 budget (1916-1925) a) [transcribed]; f770|f771 b) [transcribed]; f772 dette "
               "tunisienne a) opérations 1884-1923 (b) balance) [transcribed]; f773 blank; f774|f775 taxe personnelle [transcribed]; f776-f783 "
               "achour, one page per crop (a) blé ... h) lin), européens and indigènes in one table; f784|f785 canoun "
               "dattiers a); f786|f787 b); f788|f789 canoun oliviers a) (1926); f790|f791 b); f792|f793 c); "
               "f794|f795 droit de patente (bénéfices de 1925, imposés en 1926) [transcribed]; f796|f797 bétail a); f798|f799 b); "
               "f800|f801 c); f802 blank. f803 = chapter XI.",
    "sgt1927": "f229 title; f230|f231 budget (1917-1926) a) [transcribed]; f232|f233 b) [transcribed]; f234 dette "
               "tunisienne (1884-1924) [transcribed]; f235 blank; f236|f237 taxe personnelle [transcribed]; f238-f245 achour (one page per "
               "crop); f246|f247 canoun dattiers a) (1927); f248|f249 b); f250|f251 canoun oliviers a); f252|f253 "
               "b); f254|f255 c); f256|f257 droit de patente (1926 / 1927) [transcribed]; f258 blank. f259 = chapter XI. No "
               "taxe sur le bétail from this edition.",
    "sgt1928": "f753 title; f754|f755 budget (1918-1927) a) [transcribed]; f756|f757 b) [transcribed]; f758 dette "
               "(1884-1924, same figures as sgt1927) [transcribed]; f759 blank; f760|f761 taxe personnelle [transcribed]; f762-f769 achour; f770|f771 canoun dattiers "
               "a) (1928); f772|f773 b); f774|f775 canoun oliviers a); f776|f777 b); f778|f779 c); f780|f781 droit "
               "de patente (1927 / 1928) [transcribed]; f782 blank. f783 = chapter XI.",
    "sgt1929": "f231 title; f232|f233 budget (1919-1928) a) [transcribed]; f234|f235 b) [transcribed]; f236 dette "
               "(1884-1925) [transcribed]; f237 blank; f238|f239 taxe personnelle [transcribed]; f240-f247 achour; f248|f249 canoun dattiers "
               "a) (1929); f250|f251 b) (the f251 OCR also shows an européens / indigènes heading, to be checked on the image); f252|f253 canoun oliviers a); f254|f255 b); "
               "f256|f257 c); f258 blank; f259 droit de patente on a folding plate (1928 / 1929) [transcribed]; f260 back of the "
               "plate. f261 = chapter XI.",
    "sgt1930": "f765 title; f766|f767 budget (1920-1929) a) [transcribed]; f768|f769 b) [transcribed]; f770|f771 "
               "dette (1884-1927, two pages) [transcribed]; f772|f773 taxe personnelle [transcribed]; f774-f781 achour; f782|f783 canoun "
               "dattiers a) (1930); f784|f785 b); f786|f787 canoun oliviers a); f788|f789 b); f790|f791 c); f792 "
               "and f793 droit de patente (folding plate f793, 1929 / 1930; f792 is the blank back of the plate) [transcribed]; f794 blank. f795 = chapter XI.",
    "sgt1935": "f127 chapter X title; f128 blank; f129 budget annuel (1932-1934) a) recettes réalisées "
               "[transcribed]; f130 b) dépenses [transcribed]; f131 dette tunisienne a) opérations 1884-1934 [transcribed]; f132 "
               "b) balance des opérations [transcribed]; f133 achour (1935), superficies ensemencées par les Européens et les "
               "Tunisiens (all crops in one table); f134|f135 canoun des dattiers (1935); f136|f137 canoun des "
               "oliviers (1935); f138 droit de patente (bénéfices de 1934, imposés en 1935), by région, contrôle "
               "and caïdat [transcribed]. f139 = chapter XI.",
    "sgt1936": "f94 chapter IX title; f95 budget annuel (1933-1935) a) [transcribed]; f96 b) [transcribed]; f97 dette "
               "tunisienne (opérations 1884-1935) [transcribed]; f98 balance des opérations [transcribed]; f99 droit de patente (1935 / 1936) [transcribed]. "
               "f100 = chapter X Agriculture.",
    "sgt1939": "f93 chapter IX title; f94 budget annuel (1936-1938) a) [transcribed]; f95 b) [transcribed]; f96 dette "
               "tunisienne (1884-1938) [transcribed]; f97 balance des opérations [transcribed]; f98 droit de patente (1938 / 1939) [transcribed]. f99 = "
               "chapter X Agriculture.",
}

NOT_DONE = (
    "Transcribed, every printing, every cell read on native-resolution crops of the page images (OCR used only as a "
    "cross-check, flag `ocr_corrected`): the two budget tables (finance_budget_receipts, finance_budget_expenditure, "
    "sgt1925-sgt1939); the dette tunisienne (finance_public_debt, finance_public_debt_balance, sgt1925-sgt1939; not "
    "printed in sgt1922-sgt1924, whose chapters f185-f230, f675-f720 and f1171-f1216 open with the taxe "
    "personnelle); the droit de patente by class of profit (finance_patente, sgt1922-sgt1930; the folding plates "
    "sgt1929 f259 and sgt1930 f793 read in vertical strips) and by caïdat (finance_patente_caidat, sgt1935, sgt1936, "
    "sgt1939); the taxe personnelle (finance_taxe_personnelle, sgt1922-sgt1930). Not yet transcribed (see the survey "
    "above for views): taxe sur le bétail (sgt1922-sgt1926: a) rôles européens, b) rôles indigènes, c) "
    "récapitulation, each a two-page spread by caïdat x 7 species x jeunes non imposables / imposables / total), "
    "achour (sgt1922-sgt1935), canoun des dattiers and des oliviers (sgt1922-sgt1935). The chapter reprints neither "
    "the public assistance / health budgets nor the communal budgets.")


def write_survey():
    L = ["# Finances chapter: survey of every edition", "",
         "Survey of the *Finances* chapter (chapter X up to sgt1935, chapter IX in sgt1936 and sgt1939), view by "
         "view, from whole-page images of every view (page headings checked against the Gallica OCR). First and "
         "last views confirmed on the page images for every edition (chapter-title page, and the next chapter "
         "title Agriculture). Extraction: `extract_finance.py`.", "",
         "| edition | ark | views |", "|---|---|---|"]
    L += [f"| {e} | `{EDITIONS[e]}` | {a}–{b} |" for e, (a, b) in CHAPTER_VIEWS.items()]
    L += ["", "## Views per edition", "", "[transcribed] marks the views stored in a CSV.", ""]
    L += [f"- **{e}**: {t}" for e, t in SURVEY.items()]
    L += ["", "## Tables (CSV)", "", "| CSV | sections | editions and views | read on the image |",
          "|---|---|---|---|"]
    for o, sp in TABLES.items():
        L.append(f"| `{o}` | {', '.join(sp['secs'])} | " + "; ".join(
            f"{e} f{', f'.join(str(v) for v in sp['_views'][e])}" for e in sp.get("_eds", []))
            + " | every printing, cell by cell |")
    L += ["", "## Coverage", "", NOT_DONE, ""]
    (OUT / "finance_survey.md").write_text("\n".join(L) + "\n")


def build(write=True):
    secs = []
    for ed in ORDER:
        p = TR / f"{PREFIX}_{ed}.txt"
        if p.exists():
            secs += parse(p, ed)
    for s in secs:
        if s["table"] in ("receipts", "receipts39", "expenditure"):
            chk_budget(s)
    derive_patente(secs)
    for f in GROUP_CHECKS:
        f(secs)
    res = {}
    for out, spec in TABLES.items():
        ss = [s for s in secs if s["table"] in spec["secs"]]
        spec["_eds"] = [e for e in ORDER if any(s["ed"] == e for s in ss)]
        spec["_views"] = {e: sorted({s["view"] for s in ss if s["ed"] == e}) for e in spec["_eds"]}
        recs = []
        for s in ss:
            recs += spec["cells"](s)
        kept, n, diffs = spec["select"](recs, spec["key"])
        order = {id(r): i for i, r in enumerate(recs)}
        kept.sort(key=lambda r: (r["year"], order.get(id(r), 0)))
        flagged = [f"{r['census']} {r['year']} " + " / ".join(str(r.get(k, "")) for k in spec["key"][1:])
                   + f" = {r['value']} ({r['flag']})" for r in kept if r["flag"]]
        res[out] = dict(rows=len(kept), checks=CHK.n[out], failed=list(CHK.fail[out]), overlap_compared=n,
                        overlap_diffs=[list(x) for x in diffs], flagged=flagged, editions=spec["_eds"],
                        read_on_image={e: "every cell, native-resolution crops" for e in spec["_eds"]})
        if write:
            cols = COMMON + spec["dims"] + ["value", "flag"]
            write_csv(out, cols, kept)
            expl = [spec.get("fails", BUDGET_FAILS)] if CHK.fail[out] else []
            paras = list(spec.get("paras", [])) + expl + [
                "Survey of the whole chapter in every edition: `finance_survey.md`."]
            write_notes(out, CHAPTER, SCRIPT, kept, cols, {c: spec.get("doc", {}).get(c, DOC[c]) for c in cols}, spec["title_fr"],
                        spec["title_en"], paras, CHK.n[out], CHK.fail[out], n, diffs, coverage_lines(ss),
                        spec["rule"], spec["unit"])
    if write:
        write_validation(OUT / f"{PREFIX}_validation.json", dict(
            res, _chapter_views=CHAPTER_VIEWS, _survey=SURVEY, _not_transcribed=NOT_DONE))
        write_survey()
    return res


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    res = build(write=(mode == "build"))
    for out, d in res.items():
        print(f"{out}: {d['rows']} rows, {d['checks']} checks, {len(d['failed'])} failed, "
              f"{d['overlap_compared']} compared, {len(d['overlap_diffs'])} diffs, {len(d['flagged'])} flagged "
              f"[{' '.join(d['editions'])}]")
        for f in d["failed"]:
            print("   FAIL", f)
        for x in d["overlap_diffs"]:
            print("   DIFF", x)


if __name__ == "__main__":
    main()
