#!/usr/bin/env python3
"""Posts chapter (*Postes - Télégraphes - Téléphones*: chapter VIII up to sgt1935, chapter VII in sgt1936 and
sgt1939) of the Statistique générale de la Tunisie, 12 editions sgt1922-sgt1939: general information (network,
operations, financial situation) for the last ten years, money orders (to Italy by month; money orders issued in
Tunisia and payable in Tunisia), and the Caisse nationale d'épargne (accounts opened).

  python3 extract_posts.py check   parse the transcriptions, run every check, print failures
  python3 extract_posts.py build   ... and write csv/posts_*.csv, their .md notes, csv/posts_survey.md and
                                   csv/posts_validation.json

Source of truth: transcribed/posts_<edition>.txt (format in yb_tables.py; money in francs, centimes kept as
decimals). Every table is a yearly series printed for overlapping year windows (SPEC_ADDENDUM rule 4: each year
from the latest edition printing it, every other printing compared cell by cell). Printed totals are used for
checks only.
"""
import sys
from collections import defaultdict
from decimal import Decimal, ROUND_DOWN

from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parent))  # shared helper yb_tables.py
from yb_tables import (COMMON, EDITIONS, ORDER, OUT, TR, Checks, coverage_lines, is_total, parse, ssum, where,
                       write_csv, write_notes, write_validation)

CHAPTER = "Postes - Télégraphes - Téléphones"
SCRIPT = "extract_posts.py"
PREFIX = "posts"

# Views of the chapter (chapter title .. last view before the next chapter), confirmed on the images.
CHAPTER_VIEWS = {
    "sgt1922": (153, 172), "sgt1923": (637, 662), "sgt1924": (1127, 1158), "sgt1925": (163, 198),
    "sgt1926": (713, 754), "sgt1927": (175, 216), "sgt1928": (699, 740), "sgt1929": (177, 218),
    "sgt1930": (711, 752), "sgt1935": (109, 116), "sgt1936": (78, 83), "sgt1939": (77, 82),
}

# ----------------------------------------------------------------- labels

ORIGIN = {"tunisia": "Tunisie", "france": "France", "foreign": "Étranger",
          "ff": "France et Étranger (one figure printed across both lines)",
          "all": "Tunisie, France, Étranger (one figure printed across the three lines)"}
MEAS = {"n": ("number", "Nombre", "count"), "amt": ("amount", "Montant", "francs")}

NETWORK = {  # code: (service, item_fr, unit)
    "route_km": ("posts", "Longueur des chemins de fer et des routes parcourues par les courriers", "km"),
    "courier_km": ("posts", "Parcours quotidiens des courriers de terre et par chemins de fer", "km"),
    "post_offices": ("posts", "Bureaux de poste", "count"),
    "postal_agencies": ("posts", "Agences postales", "count"),
    "distributions": ("posts", "Distribution des postes", "count"),
    "letter_boxes": ("posts", "Boîtes aux lettres", "count"),
    "tg_lines_km": ("telegraphs", "Longueur des lignes", "km"),
    "tg_wires_km": ("telegraphs", "Longueur des fils", "km"),
    "tg_offices": ("telegraphs", "Bureaux de télégraphe", "count"),
    "tg_stations": ("telegraphs", "Gares ouvertes à la télégraphie", "count"),
    "tel_lines_km": ("telephones", "Longueur des lignes d'abonnés", "km"),
    "tel_wires_km": ("telephones", "Longueur des fils des circuits interurbains", "km"),
    "tel_sets": ("telephones", "Postes d'abonnés", "count"),
}
SERVICE_FR = {"posts": "Postes", "telegraphs": "Télégraphes", "telephones": "Téléphones",
              "savings": "Caisse d'Épargne", "pension_advances": "Avances sur pensions",
              "postal_cheques": "Chèques postaux"}

# operations: prefix -> (service, item, item_fr)
OPS_ITEM = {
    "corr": ("posts", "correspondence", "Nombre de correspondances (départ et arrivée)"),
    "mo_issued": ("posts", "money_orders_issued", "Mandats de poste émis"),
    "mo_paid": ("posts", "money_orders_paid", "Mandats de poste payés"),
    "reg": ("posts", "registered_items", "Chargements et objets recommandés (départ)"),
    "coll": ("posts", "collections", "Recouvrements (arrivée)"),
    "acceptance": ("posts", "bills_for_acceptance", "Valeurs présentées à l'acceptation"),
    "parcels_dep": ("posts", "parcels_dispatched", "Colis postaux : départ"),
    "parcels_arr": ("posts", "parcels_received", "Colis postaux : arrivée"),
    "tg_dep": ("telegraphs", "telegrams_sent", "Télégrammes de départ"),
    "tg_arr": ("telegraphs", "telegrams_received", "Télégrammes d'arrivée"),
    "tg_official_dep": ("telegraphs", "telegrams_official_sent", "Service officiel : départ"),
    "tg_official_arr": ("telegraphs", "telegrams_official_received", "Service officiel : arrivée"),
    "tel_conversations": ("telephones", "conversations", "Nombre de conversations"),
    "cne_books": ("savings", "passbooks_opened", "Nombre de livrets ouverts"),
    "cne_deposits": ("savings", "deposits", "Versements"),
    "cne_withdrawals": ("savings", "withdrawals", "Remboursements"),
    "cne_balance": ("savings", "depositors_balance", "Avoir des déposants"),
    "tel_urban": ("telephones", "conversations_urban", "Nombre de conversations : urbaines"),
    "tel_suburban": ("telephones", "conversations_suburban", "Nombre de conversations : suburbaines"),
    "radio_tf": ("telephones", "radiotelephone_tunisia_france",
                 "Nombre de conversations radio-téléphoniques : sens Tunisie-France"),
    "radio_ft": ("telephones", "radiotelephone_france_tunisia",
                 "Nombre de conversations radio-téléphoniques : sens France-Tunisie"),
    "tel_subscribers": ("telephones", "subscribers", "Nombre d'abonnés au téléphone au 31 décembre"),
    "tsf_sets": ("telephones", "radio_receivers", "Nombre de postes récepteurs de T.S.F. déclarés au 31 décembre"),
    "cne_passbooks_stock": ("savings", "passbooks_outstanding", "Nombre de livrets ouverts au 31 décembre"),
    "pension_adv": ("pension_advances", "advances_granted", "Avances sur pensions : avances consenties"),
    "pension_arrears": ("pension_advances", "arrears_paid", "Avances sur pensions : solde d'arrérages payés"),
    "cheque_accounts": ("postal_cheques", "current_accounts", "Chèques postaux : nombre de comptes courants au 31 "
                                                              "décembre"),
    "cheque_debit": ("postal_cheques", "operations_debit", "Chèques postaux : montant des opérations, débit"),
    "cheque_credit": ("postal_cheques", "operations_credit", "Chèques postaux : montant des opérations, crédit"),
}
OPS_UNIT_DEFAULT = {"corr": "count", "acceptance": "count", "parcels_dep": "count", "parcels_arr": "count",
                    "tg_dep": "count", "tg_arr": "count", "tg_official_dep": "count", "tg_official_arr": "count",
                    "tel_conversations": "count", "cne_books": "count", "cne_balance": "francs",
                    "tel_urban": "count", "tel_suburban": "count", "radio_tf": "count", "radio_ft": "count",
                    "tel_subscribers": "count", "tsf_sets": "count", "cne_passbooks_stock": "count",
                    "cheque_accounts": "count", "cheque_debit": "francs", "cheque_credit": "francs"}

FINANCE = {  # code: (item_fr, kind)
    "rev_posts": ("Produits : Postes", "revenue"),
    "rev_telegraphs": ("Produits : Télégraphes", "revenue"),
    "rev_telephones": ("Produits : Téléphones", "revenue"),
    "rev_rents": ("Produits : Loyers payés par le Gouvernement Tunisien", "revenue"),
    "rev_cne_subsidy": ("Produits : Subvention de la Caisse d'Épargne", "revenue"),
    "expenses": ("Dépenses", "expenses"),
    "net_product": ("Produit net", "balance"),
    "deficit": ("Déficit", "balance"),
}

MONTH = {"01": "Janvier", "02": "Février", "03": "Mars", "04": "Avril", "05": "Mai", "06": "Juin",
         "07": "Juillet", "08": "Août", "09": "Septembre", "10": "Octobre", "11": "Novembre", "12": "Décembre"}

MO_FLOW = {"to_fr": ("issued_in_tunisia", "Mandats-poste établis en Tunisie", "france",
                     "A destination de la France"),
           "to_it": ("issued_in_tunisia", "Mandats-poste établis en Tunisie", "italy", "A destination de l'Italie"),
           "from_fr": ("payable_in_tunisia", "Mandats-poste à destination de la Tunisie", "france",
                       "Émis en France"),
           "from_it": ("payable_in_tunisia", "Mandats-poste à destination de la Tunisie", "italy",
                       "Émis en Italie")}

SAV_COL = {"french": ("depositor", "french", "A des Français", "count"),
           "muslim": ("depositor", "muslim", "A des Musulmans", "count"),
           "jewish": ("depositor", "jewish", "A des Israélites", "count"),
           "italian": ("depositor", "italian", "A des étrangers : Italiens", "count"),
           "other_foreign": ("depositor", "other_foreign", "A des étrangers : autres étrangers", "count"),
           "deposits": ("amount", "deposits", "Montant des versements", "francs"),
           "withdrawals": ("amount", "withdrawals", "Montant des remboursements", "francs"),
           "balance": ("amount", "depositors_balance", "Avoir des déposants", "francs")}


class _Checks(Checks):
    def eq(self, topic, what, got, printed, tol=Decimal(0)):
        super().eq(TOPIC2OUT[topic], what, got, printed, tol)


TOPIC2OUT = {"network": "posts_network", "operations": "posts_operations", "finance": "posts_finance",
             "mo_italy": "posts_money_orders_italy", "mo_summary": "posts_money_orders_summary",
             "savings": "posts_savings_accounts"}
CHK = _Checks()


def dl(sec):
    return [r for r in sec["rows"] if "cells" in r and not is_total(r["label"]) and r["label"] not in NONDATA]


NONDATA = {"plus", "plus_pct", "minus", "minus_pct", "plus2a", "plus2b"}


def row(sec, label):
    for r in sec["rows"]:
        if r["label"] == label:
            return r["cells"]
    return None


# ----------------------------------------------------------------- checks

OPS_TOTALS = {
    "Total@corr": ["corr_tunisia", "corr_france", "corr_foreign"],
    "Total@mo_n": [f"mo_{a}_{o}_n" for a in ("issued", "paid") for o in ("tunisia", "france", "foreign")],
    "Total@mo_amt": [f"mo_{a}_{o}_amt" for a in ("issued", "paid") for o in ("tunisia", "france", "foreign")],
    "Total@reg_n": [f"reg_{o}_n" for o in ("tunisia", "france", "foreign")],
    "Total@reg_amt": [f"reg_{o}_amt" for o in ("tunisia", "france", "foreign")],
    "Total@coll_n": [f"coll_{o}_n" for o in ("tunisia", "france", "foreign")],
    "Total@coll_amt": [f"coll_{o}_amt" for o in ("tunisia", "france", "foreign")],
    "Total@parcels": [f"parcels_{d}_{o}" for d in ("dep", "arr") for o in ("tunisia", "france", "foreign")],
    "Total@tg": [f"tg_{d}_{o}" for d in ("dep", "arr") for o in ("tunisia", "france", "foreign")]
                + ["tg_official_dep", "tg_official_arr"],
    "Total@cne_n": ["cne_deposits_n", "cne_withdrawals_n"],
    "Total@cne_amt": ["cne_deposits_amt", "cne_withdrawals_amt"],
}


def chk_lines(topic, sec, totals):
    for tl, parts in totals.items():
        t = row(sec, tl)
        if t is None:
            continue
        have = [p for p in parts if row(sec, p) is not None]
        for c in sec["cols"]:
            CHK.eq(topic, f"{where(sec)} {c}: {tl} = {' + '.join(have)}",
                   ssum(row(sec, p)[c].value for p in have), t[c].value)


def chk_finance(sec):
    revs = [r["label"] for r in dl(sec) if r["label"].startswith("rev_")]
    chk_lines("finance", sec, {"Total@rev": revs})
    t, e, n, d = row(sec, "Total@rev"), row(sec, "expenses"), row(sec, "net_product"), row(sec, "deficit")
    if t and e and n and d:
        for c in sec["cols"]:
            vals = [t[c].value, e[c].value, n[c].value, d[c].value]
            if None in vals:
                continue
            CHK.eq("finance", f"{where(sec)} {c}: Totaux - Dépenses = Produit net - Déficit",
                   vals[0] - vals[1], vals[2] - vals[3])


def chk_col_total(topic, sec, label="Totaux"):
    t = row(sec, label)
    if t is None:
        return
    for c in sec["cols"]:
        CHK.eq(topic, f"{where(sec)} {c}: {label} = sum of the lines", ssum(r["cells"][c].value for r in dl(sec)),
               t[c].value)


def chk_mo_summary(sec):
    """En plus / En moins lines = difference of the first two years printed; Soit % = |difference| / earlier
    year (truncated to 0.1); sgt1924's two extra 'En plus' lines (plus2a + plus2b) = difference of years 3 and 2."""
    ys = dl(sec)
    groups = [(0, 1, ["plus"], ["minus"], "plus_pct", "minus_pct"), (1, 2, ["plus2a", "plus2b"], [], None, None)]
    for i, j, pl, mi, pp, mp in groups:
        if j >= len(ys) or row(sec, pl[0]) is None:
            continue
        a, b = ys[i]["cells"], ys[j]["cells"]
        for c in sec["cols"]:
            if a[c].value is None or b[c].value is None:
                continue
            d = b[c].value - a[c].value
            got = ssum([row(sec, x)[c].value for x in pl]) - ssum([row(sec, x)[c].value for x in mi] or [Decimal(0)])
            CHK.eq("mo_summary", f"{where(sec)} {c}: {' + '.join(pl)}{' - ' + mi[0] if mi else ''} = "
                   f"{ys[j]['label']} - {ys[i]['label']}", d, got)
            if pp and row(sec, pp) is not None and a[c].value:
                pct = (abs(d) * 100 / a[c].value).quantize(Decimal("0.1"), ROUND_DOWN)
                CHK.eq("mo_summary", f"{where(sec)} {c}: Soit % = |difference| / {ys[i]['label']} (truncated to 0.1)", pct,
                       row(sec, pp)[c].value + row(sec, mp)[c].value)


def chk_savings(sec):
    parts = [c for c in ("french", "muslim", "jewish", "italian", "other_foreign") if c in sec["cols"]]
    for r in dl(sec):
        c = r["cells"]
        if "total" in c:
            CHK.eq("savings", f"{where(sec)} {r['label']}: total = {' + '.join(parts)}", ssum(c[p].value for p in parts),
                   c["total"].value)
    chk_col_total("savings", sec)


CROSS = {"n": 0, "diffs": []}   # comparison (not a check): Comptes ouverts table vs Exploitation table
SAV_OPS = {"deposits": "cne_deposits_amt", "withdrawals": "cne_withdrawals_amt", "balance": "cne_balance",
           "total": "cne_books"}


def chk_savings_vs_ops(secs):
    """Comptes ouverts table against the same edition's Exploitation table (whole francs when the Comptes ouverts
    table prints no centimes)."""
    ops = defaultdict(dict)
    for s in secs:
        if s["table"] == "operations":
            for r in s["rows"]:
                if "cells" in r and r["label"] in SAV_OPS.values():
                    for c, cell in r["cells"].items():
                        if cell.value is not None:
                            ops[s["ed"]][(r["label"], int(c))] = cell.value
    for s in secs:
        if s["table"] != "savings":
            continue
        for r in dl(s):
            y = int(r["label"])
            for c, oc in SAV_OPS.items():
                if c not in r["cells"] or r["cells"][c].value is None or (oc, y) not in ops[s["ed"]]:
                    continue
                a, b = r["cells"][c].value, ops[s["ed"]][(oc, y)]
                if a == a.to_integral_value() and b != b.to_integral_value():
                    b = b.to_integral_value(rounding=ROUND_DOWN)
                CROSS["n"] += 1
                if a != b:
                    CROSS["diffs"].append(f"{s['ed']} {y} {c}: Comptes ouverts {a}, Exploitation {b}")


# ----------------------------------------------------------------- records

def base(sec, year):
    return {"census": sec["ed"], "table_id": sec["table"], "gallica_ark": sec["ark"], "source_page": sec["page"],
            "gallica_view": sec["view"], "year": year}


def rec(sec, r, col, year, **dims):
    c = r["cells"][col]
    flag = c.flag
    if sec.get("realigned") and not flag:
        flag = "row_realigned"
    return dict(base(sec, year), **dims, value=c.value, flag=flag, _row=r["label"], _col=col)


def cells_network(sec):
    out = []
    for r in dl(sec):
        s, fr, unit = NETWORK[r["label"]]
        for c in sec["cols"]:
            out.append(rec(sec, r, c, int(c), service=s, service_fr=SERVICE_FR[s], item=r["label"], item_fr=fr,
                           unit=unit))
    return out


def ops_parse(code):
    """corr_tunisia, mo_issued_france_amt, parcels_dep_foreign, tel_conversations ..."""
    meas = None
    parts = code.split("_")
    if parts[-1] in MEAS:
        meas = parts[-1]
        parts = parts[:-1]
    origin = None
    if parts[-1] in ORIGIN and "_".join(parts) not in OPS_ITEM:
        origin = parts[-1]
        parts = parts[:-1]
    key = "_".join(parts)
    return key, origin, meas


def cells_operations(sec):
    out = []
    for r in dl(sec):
        key, origin, meas = ops_parse(r["label"])
        s, item, fr = OPS_ITEM[key]
        if meas:
            m, mfr, unit = MEAS[meas]
        else:
            m, mfr, unit = ("number", "Nombre", OPS_UNIT_DEFAULT[key]) if OPS_UNIT_DEFAULT[key] == "count" else (
                "amount", "Montant", "francs")
        for c in sec["cols"]:
            out.append(rec(sec, r, c, int(c), service=s, service_fr=SERVICE_FR[s], item=item, item_fr=fr,
                           origin=origin or "", origin_fr=ORIGIN.get(origin, ""), measure=m, measure_fr=mfr,
                           unit=unit))
    return out


def cells_finance(sec):
    out = []
    for r in dl(sec):
        fr, kind = FINANCE[r["label"]]
        for c in sec["cols"]:
            out.append(rec(sec, r, c, int(c), item=r["label"], item_fr=fr, kind=kind))
    return out


def cells_mo_italy(sec):
    out = []
    for r in dl(sec):
        for c in sec["cols"]:
            y, m = c.split(".")
            mm, mfr, unit = MEAS[m]
            out.append(rec(sec, r, c, int(y), month=int(r["label"]), month_fr=MONTH[r["label"]], measure=mm,
                           measure_fr=mfr, unit=unit))
    return out


def cells_mo_summary(sec):
    out = []
    for r in dl(sec):
        for c in sec["cols"]:
            f, m = c.split(".")
            flow, flow_fr, partner, partner_fr = MO_FLOW[f]
            mm, mfr, unit = MEAS[m]
            out.append(rec(sec, r, c, int(r["label"]), flow=flow, flow_fr=flow_fr, partner=partner,
                           partner_fr=partner_fr, measure=mm, measure_fr=mfr, unit=unit))
    return out


def cells_savings(sec):
    out = []
    for r in dl(sec):
        for c in sec["cols"]:
            if c == "total":
                continue
            kind, item, fr, unit = SAV_COL[c]
            out.append(rec(sec, r, c, int(r["label"]), item=item, item_fr=fr, unit=unit))
    return out


# ----------------------------------------------------------------- tables

T_DOC = {
    "census": "edition the value is taken from (`sgt1922` … `sgt1939`): the latest edition printing that year",
    "table_id": "transcription section",
    "gallica_ark": "Gallica volume ark (views are numbered within a volume)",
    "source_page": "printed page number",
    "gallica_view": "Gallica view (fNNNN)",
    "year": "year of the figures (network: situation at 31 December)",
    "service": "`posts`, `telegraphs`, `telephones`, `savings` (Caisse d'Épargne)",
    "service_fr": "printed sub-heading",
    "item": "item code (English)",
    "item_fr": "printed line heading",
    "origin": "`tunisia`, `france`, `foreign` (printed Tunisie, France, Étranger); empty when the line has no "
              "breakdown",
    "origin_fr": "as printed",
    "measure": "`number` (Nombre) or `amount` (Montant)",
    "measure_fr": "as printed",
    "unit": "`count`, `km` (kilometres) or `francs` (centimes kept as decimals)",
    "kind": "`revenue` (Produits), `expenses` (Dépenses), `balance` (Produit net / Déficit)",
    "month": "month number 1-12",
    "month_fr": "as printed",
    "flow": "`issued_in_tunisia` or `payable_in_tunisia`",
    "flow_fr": "printed column group heading",
    "partner": "`france` or `italy`",
    "partner_fr": "printed column heading",
    "value": "printed value (» = 0)",
    "flag": "empty, or `illegible` (NA, cut by the binding or broken type), `not_applicable` (nothing printed, or » in a "
            "line not yet collected; NA), `row_realigned` (printed in the wrong column or line, stored on the year / item it "
            "belongs to), `reprint_corrected` (kept from an earlier printing), `derived_from_totals`",
}

RULE4 = ("Printed for overlapping year windows: each year is taken from the **latest** edition that prints it "
         "(SPEC_ADDENDUM rule 4; `census` = that edition); every other printing of the same cell, read "
         "independently on its own page image, is compared below.")

TABLES = {
    "posts_network": dict(
        secs=["network"], cells=cells_network, key=["year", "item"],
        dims=["service", "service_fr", "item", "item_fr", "unit"],
        title_fr="Postes, Télégraphes, Téléphones. Renseignements généraux : a) Réseau",
        title_en="Posts, telegraphs and telephones: network at 31 December",
        unit="Units: kilometres (`unit` = `km`) and counts (`count`), per line; suggested value_type: mixed."),
    "posts_operations": dict(
        secs=["operations"], cells=cells_operations, key=["year", "item", "origin", "measure"],
        dims=["service", "service_fr", "item", "item_fr", "origin", "origin_fr", "measure", "measure_fr", "unit"],
        title_fr="Postes, Télégraphes, Téléphones. Renseignements généraux : b) Exploitation",
        title_en="Posts, telegraphs and telephones: traffic (correspondence, money orders, registered items, "
                 "collections, parcels, telegrams, telephone conversations, savings bank)",
        unit="Units: counts (`unit` = `count`) and francs (`francs`, centimes kept), per line; suggested "
             "value_type: mixed."),
    "posts_finance": dict(
        secs=["finance"], cells=cells_finance, key=["year", "item"], dims=["item", "item_fr", "kind"],
        title_fr="Postes, Télégraphes, Téléphones. Renseignements généraux : c) Situation financière",
        title_en="Posts, telegraphs and telephones: revenue, expenditure and balance",
        unit="Unit: francs; value_type: francs."),
    "posts_money_orders_italy": dict(
        secs=["mo_italy"], cells=cells_mo_italy, key=["year", "month", "measure"],
        dims=["month", "month_fr", "measure", "measure_fr", "unit"],
        title_fr="Mouvements des mandats-poste : a) Mandats-poste envoyés de Tunisie en Italie",
        title_en="Money orders sent from Tunisia to Italy, by month",
        unit="Units: number of money orders (`count`) and amount in francs (`francs`, centimes kept); suggested "
             "value_type: mixed."),
    "posts_money_orders_summary": dict(
        secs=["mo_summary"], cells=cells_mo_summary, key=["year", "flow", "partner", "measure"],
        dims=["flow", "flow_fr", "partner", "partner_fr", "measure", "measure_fr", "unit"],
        title_fr="Mouvements des mandats-poste : b) Mandats-poste établis en Tunisie ou à destination de la Tunisie",
        title_en="Money orders issued in Tunisia for France and Italy, and issued in France and Italy for Tunisia",
        unit="Units: number of money orders (`count`) and amount in francs (`francs`); suggested value_type: "
             "mixed."),
    "posts_savings_accounts": dict(
        secs=["savings"], cells=cells_savings, key=["year", "item"], dims=["item", "item_fr", "unit"],
        title_fr="Caisse nationale d'épargne. Comptes ouverts",
        title_en="National savings bank (Caisse nationale d'épargne): accounts opened by depositor group, deposits, "
                 "withdrawals and depositors' balance",
        unit="Units: accounts opened (`count`) and francs (`francs`); suggested value_type: mixed."),
}

EXPLAIN = {}
FLAGS = {}   # (edition, section, row, col) -> (flag, why); none needed so far
PERIODS = ("Financial years: the columns 1930 and 1932 of the Exploitation and Situation financière tables are printed "
           "\"Année 1930 (15 mois)\" and \"Année 1932 (9 mois)\" (sgt1930 heads its last column \"Année 1930 (15 mois)\"); "
           "stored as years 1930 and 1932.")
PARAS = {
    "posts_network": [
        "Printed for ten years in every edition from sgt1922 to sgt1936 (sgt1922 1913-1922 ... sgt1936 1927-1936); not "
        "printed in sgt1939. No printed totals, so no checks; every year is compared across up to nine printings.",
        "Footnote (A) under the table (every edition): \"Les différences en moins dans la longueur des fils "
        "télégraphiques s'expliquent par les suppressions de lignes et désaffectation de bureaux\" (the decreases in "
        "the length of telegraph wire are explained by lines removed and offices closed).",
        "sgt1922 prints the 1915 column in the gutter of f154; its network values are legible."],
    "posts_operations": [
        PERIODS,
        "Lines: correspondence (départ et arrivée; from sgt1935 \"Tunisie (départ seulement)\"), money orders issued "
        "and paid, registered items (chargements et objets recommandés, départ), collections (recouvrements, arrivée), "
        "bills presented for acceptance, parcels, telegrams, telephone conversations, savings bank (passbooks opened, "
        "deposits, withdrawals, depositors' balance). The printed Totaux lines are used as checks only.",
        "sgt1939 prints a new Exploitation table (1930-1939) without correspondence, registered items, collections or "
        "acceptances, and adds urban / suburban and radiotelephone conversations, subscribers, wireless sets, "
        "passbooks outstanding, advances on pensions and postal cheques (1938-1939 only; earlier columns printed », "
        "stored NA `not_applicable`). In sgt1939 1938 the money orders France and Étranger are printed as one figure "
        "across the two lines (`origin` = `ff`) and the telegrams of each direction as one figure across the three "
        "origins (`origin` = `all`).",
        "sgt1939 money-order lines are misaligned: the column headed 1931 prints the 1927 figures and the columns "
        "headed 1932-1936 the figures of 1931-1935 (identical, cell for cell, to sgt1936's 1927 and 1931-1935); they "
        "are attached to the year they belong to, flagged `row_realigned`, and compared with the other printings; "
        "the aligned printing (sgt1936) is kept for those years. Likewise sgt1939 prints the total number of "
        "telephone conversations of 1930-1937 on its \"Suburbaines\" line: stored as the total (`row_realigned`).",
        "Cells illegible because of the binding (sgt1922 1915 savings-bank lines; sgt1939 1932 column) or a broken "
        "plate (sgt1926 1926 telephone conversations, printed \"7.089 11\") are stored only from another printing; "
        "sgt1922's 1915 savings lines are stored from sgt1923.",
        "Two notable revisions between editions: sgt1929 revises 1920 savings deposits (38.352 to 38.362) and "
        "balances 1920 and 1923; sgt1935 prints the 1926 telephone conversations as 7.089.111 (sgt1927-sgt1930: "
        "7.089.114) and 1933 parcels dispatched to Tunisia / France 67.847 / 95.193 (sgt1936, sgt1939: 67.947 / "
        "95.183)."],
    "posts_finance": [
        PERIODS,
        "Footnote (1) of sgt1922-sgt1926: \"Y compris la subvention aux services maritimes postaux\" (including the "
        "subsidy to the postal shipping services), attached to the Dépenses line.",
        "Line Loyers payés par le Gouvernement Tunisien printed » in every year (stored 0). sgt1922 prints Dépenses, "
        "Produit net and Déficit » for 1922 (stored 0 in that printing, superseded by sgt1923-sgt1930). From 1933 the "
        "Dépenses, Produit net and Déficit lines are printed » (no figure): stored NA (`not_applicable`). sgt1930 "
        "prints for 1930 (15 months) Dépenses 11.375.053 and Déficit 23.113.851 (the revenue total less 11.375.053 "
        "is a surplus of 23.113.851, not a deficit); sgt1935 and sgt1936 print 50.072.598 and 15.583.694, which "
        "are kept.",
        "Not printed in sgt1939."],
    "posts_money_orders_italy": [
        "Printed only in sgt1922 (1918-1922), sgt1923 (1919-1923; title \"1913-1923\") and sgt1924 (1920-1924), with a "
        "Totaux line (checks only). Amounts in francs and centimes (1919 printed in whole francs)."],
    "posts_money_orders_summary": [
        "sgt1922-sgt1924 print table b) for two or three years with the lines En plus / Soit % / En moins / Soit % "
        "(used as checks; the percentages are truncated, not rounded). From sgt1925 the table is two tables a) "
        "Mandats envoyés (de Tunisie en France, en Italie) and b) Mandats-poste à destination de la Tunisie (émis en "
        "France, en Italie), ten years (sgt1935: 1923-1934), stored together here (`flow`).",
        "sgt1930 prints its last line \"1930-31 (15 mois)\"; sgt1935 prints \"1930-31 (15 mois)\", \"1931-32 (12 "
        "mois)\" and then 1932, 1933, 1934: stored as years 1930 and 1931 (financial years) and 1932-1934.",
        "Not printed in sgt1936 and sgt1939."],
    "posts_savings_accounts": [
        "Comptes ouverts: accounts (passbooks) opened by depositor group, with the amounts of deposits and "
        "withdrawals and the depositors' balance. The TOTAL column is used as a check only. sgt1939 prints the "
        "amounts only (1930-1939).",
        "This table and the savings lines of the Exploitation table (in `posts_operations`) are printed separately "
        "and often disagree: sgt1923-sgt1928 keep 1923 deposits / withdrawals of 17.905.102 / 13.622.763 (Exploitation: "
        "18.331.195 / 12.837.933) and print 1926-1928 amounts that differ from the Exploitation table; sgt1929 and "
        "later reprint the Exploitation figures. sgt1935 and sgt1936 print a table headed 1923-1934 whose 1932 "
        "deposits (19.584.818 06) and balance (18.940.606 76) and 1933 balance (130.473.218 88) differ from the "
        "Exploitation table (49.584.818 06, 118.939.778 24, 124.810.682 88), and whose line 1934 carries the 1935 "
        "Exploitation figures (8.432 passbooks; its depositor columns sum to 7.432); sgt1939 repeats these. Values "
        "are stored as printed (latest printing); see the comparison counts below and `posts_validation.json`."],
}
SURVEY = {
    "sgt1922": "f153 chapter VIII title (Postes - Télégraphes - Téléphones); f154|f155 renseignements généraux "
               "(1913-1922): a) réseau, b) exploitation (first part: correspondence, money orders, registered "
               "items); f156|f157 b) exploitation continued (collections, acceptances, parcels, telegrams, "
               "telephones, caisse d'épargne) and c) situation financière (the 1915 column in the gutter, its lower "
               "cells cut); f158 mouvement des mandats-poste a) to Italy by month 1918-1922, b) 1921-1922; f159-f171 "
               "c) taux de change (dated conversion rates for international money orders, not transcribed); f172 "
               "Caisse nationale d'épargne, comptes ouverts 1913-1922. f173 = chapter IX Travaux publics.",
    "sgt1923": "f637 title; f638|f639 a) réseau, b) exploitation (1914-1923); f640|f641 b) continued, c) situation "
               "financière; f642 mandats-poste a) Italy by month 1919-1923, b) 1922-1923; f643-f661 taux de change "
               "(not transcribed); f662 caisse d'épargne 1914-1923. f663 = chapter IX.",
    "sgt1924": "f1127 title; f1128|f1129 a), b) (1915-1924); f1130|f1131 b) continued, c); f1132 mandats-poste a) "
               "Italy 1920-1924, b) 1922-1924; f1133-f1156 taux de change (not transcribed); f1157 caisse d'épargne "
               "1915-1924; f1158 blank. f1159 = chapter IX.",
    "sgt1925": "f163 title; f164|f165 a), b) (1916-1925); f166|f167 b) continued, c); f168 mandats-poste a) envoyés, "
               "b) à destination de la Tunisie (1916-1925); f169-f197 taux de change (not transcribed); f198 caisse "
               "d'épargne 1915-1925. f199 = chapter IX.",
    "sgt1926": "f713 title; f714|f715 a), b) (1917-1926); f716|f717 b) continued, c); f718 mandats-poste "
               "(1917-1926); f719-f752 taux de change (not transcribed); f753 caisse d'épargne 1917-1926; f754 blank. "
               "f755 = chapter IX.",
    "sgt1927": "f175 title; f176|f177 a), b) (1918-1927); f178|f179 b) continued, c); f180 mandats-poste "
               "(1918-1927); f181-f214 taux de change (not transcribed); f215 caisse d'épargne 1918-1927; f216 blank. "
               "f217 = chapter IX.",
    "sgt1928": "f699 title; f700|f701 a), b) (1919-1928); f702|f703 b) continued, c); f704 mandats-poste "
               "(1919-1928); f705-f738 taux de change (not transcribed); f739 caisse d'épargne 1919-1928; f740 blank. "
               "f741 = chapter IX.",
    "sgt1929": "f177 title; f178|f179 a), b) (1920-1929); f180|f181 b) continued, c); f182 mandats-poste "
               "(1920-1929); f183-f216 taux de change (not transcribed); f217 caisse d'épargne 1920-1929; f218 blank. "
               "f219 = chapter IX.",
    "sgt1930": "f711 title; f712|f713 a), b) (1921-1930, heading printed 1920-1929); f714|f715 b) continued, c); "
               "f716 mandats-poste (1921-1930); f717-f750 taux de change (not transcribed); f751 caisse d'épargne "
               "1921-1930; f752 blank. f753 = chapter IX.",
    "sgt1935": "f109 title; f110|f111 a), b) (1926-1935); f112|f113 b) continued, c); f114 mandats-poste "
               "(1923-1934); f115 caisse d'épargne (1923-1934); f116 blank. f117 = chapter IX. No exchange rates.",
    "sgt1936": "f78 chapter VII title (Postes - Télégraphes - Téléphones); f79|f80 a), b) (1927-1936); f81|f82 b) "
               "continued, situation financière; f83 caisse d'épargne (1923-1934, sgt1935's table reprinted). f84 = "
               "chapter VIII Travaux publics. No money-order table. The range is 78-83.",
    "sgt1939": "f77 chapter VII title; f78|f79 exploitation (1930-1939): postes (mandats émis / payés, colis), "
               "télégraphes; f80|f81 exploitation continued: téléphones, caisse d'épargne, avances sur pensions, "
               "chèques postaux; f82 caisse d'épargne, comptes ouverts (1930-1939, amounts only). f83 = chapter VIII "
               "Travaux publics. No réseau, no situation financière, no money-order tables.",
}
NOT_DONE = ("Not transcribed: the exchange-rate tables (\"c) Taux de change\" / conversion rates applied to "
            "international money orders, dated rates by country, 13 to 34 pages per edition in sgt1922-sgt1930: "
            "sgt1922 f159-f171, sgt1923 f643-f661, sgt1924 f1133-f1156, sgt1925 f169-f197, sgt1926 f719-f752, "
            "sgt1927 f181-f214, sgt1928 f705-f738, sgt1929 f183-f216, sgt1930 f717-f750). They are lists of dated "
            "rates, not statistics of the service, and were left for a separate pass. Everything else in the "
            "chapter is transcribed in every edition that prints it, every cell read on native-resolution crops.")


def explain_failures(out):
    """Group failed checks by (section, column, identity, values) and list the editions in which they recur."""
    import re as _re
    g = defaultdict(list)
    for f in CHK.fail[out]:
        m = _re.match(r"(sgt\d+) p\.\d+ \(f\d+\) (\w+) (\S+): (.*?): cells give (\S+), printed (\S+)", f)
        if m:
            ed, t, col, what, got, pr = m.groups()
            g[(t, col, what.split(" = ")[0].split(":")[0], got, pr)].append(ed)
    if not g:
        return []
    L = ["Failed checks, grouped (printed values kept). A failure that recurs identically in several editions was "
         "read independently on each printing, so it is the printed figure; every failure printed by one edition "
         "only was re-read on a zoomed native-resolution crop:"]
    for (t, col, what, got, pr), eds in sorted(g.items(), key=lambda kv: (kv[0][1], kv[0][2])):
        L.append(f"{t} {col} {what}: cells {got}, printed {pr} (in {', '.join(eds)})")
    return ["; ".join(L[1:]).join([L[0] + " ", "."])]


RC = "reprint_corrected"
# (output, key): (edition whose printing is kept, why) -- the latest printing is a misprint
PREFER = {
    ("posts_operations", (1932, "correspondence", "france", "number")): (
        "sgt1935", "sgt1936 prints 50.350.000; sgt1935's 50.350.500 is the value that gives the Totaux 89.601.500 "
                   "printed by both"),
    ("posts_operations", (1928, "money_orders_paid", "foreign", "amount")): (
        "sgt1935", "sgt1936 prints 3.658.894 (transposed digits); sgt1928-sgt1935 print 3.685.894, which gives the "
                   "Totaux 672.871.101 to within 3 francs (as in every other printing)"),
    ("posts_operations", (1935, "withdrawals", "", "amount")): (
        "sgt1935", "sgt1936 and sgt1939 print 6.920.421 16 (a digit dropped); sgt1935 prints 61.920.421 16, the "
                   "order of magnitude of the other years and of the Comptes ouverts table"),
    ("posts_finance", (1935, "rev_telephones")): (
        "sgt1935", "sgt1936 prints 9.005.617 29; sgt1935's 9.055.617 29 gives the Totaux 29.538.508 79 printed by "
                   "both"),
}
# (output, key): (value, why) -- value solved from the printed totals
DERIVE = {
    ("posts_operations", (1935, "money_orders_issued", "france", "amount")): (
        Decimal("107579990"), "printed \"107.590\" in sgt1935, sgt1936 and sgt1939 (digits missing); 107.579.990 = "
                              "Totaux 507.654.550 less the five other amounts printed for 1935"),
}


def select(recs, key_dims, out=None):
    """Rule 4: one record per key from the latest edition printing it legibly (an aligned printing before a
    realigned one); other printings compared. PREFER / DERIVE overrides as documented."""
    by = defaultdict(list)
    for r in recs:
        by[tuple(r.get(k) for k in key_dims)].append(r)
    kept, compared, diffs, skipped = [], 0, [], 0
    for k, rs in by.items():
        rs.sort(key=lambda r: ORDER.index(r["census"]))
        legible = [r for r in rs if r["value"] is not None]
        aligned = [r for r in legible if r["flag"] != "row_realigned"]
        last = (aligned or legible or rs)[-1]
        if (out, k) in PREFER:
            ed, why = PREFER[(out, k)]
            alt = [r for r in rs if r["census"] == ed][0]
            NOTES_FLAG.append((out, f"{k}: kept {ed}'s {alt['value']} ({RC}); {why}"))
            last = alt
        for r in rs:
            if r is last:
                continue
            if r["value"] is None:
                skipped += 1
                continue
            compared += 1
            if r["value"] != last["value"]:
                diffs.append((k, r["census"], r["value"], last["census"], last["value"]))
        if (out, k) in PREFER:
            last = dict(last, flag=RC)
        if (out, k) in DERIVE:
            v, why = DERIVE[(out, k)]
            NOTES_FLAG.append((out, f"{k}: {v} (derived_from_totals, stored with census = {last['census']}); {why}"))
            last = dict(last, value=v, flag="derived_from_totals")
        kept.append(last)
    return kept, compared, diffs, skipped


NOTES_FLAG = []


def build(write=True):
    secs = []
    for ed in ORDER:
        p = TR / f"{PREFIX}_{ed}.txt"
        if p.exists():
            secs += parse(p, ed)
    for s in secs:
        t = s["table"]
        if t == "operations":
            chk_lines("operations", s, OPS_TOTALS)
        elif t == "finance":
            chk_finance(s)
        elif t == "mo_italy":
            chk_col_total("mo_italy", s)
        elif t == "mo_summary":
            chk_mo_summary(s)
        elif t == "savings":
            chk_savings(s)
    chk_savings_vs_ops(secs)
    res = {}
    for out, spec in TABLES.items():
        ss = [s for s in secs if s["table"] in spec["secs"]]
        spec["_eds"] = [e for e in ORDER if any(s["ed"] == e for s in ss)]
        recs = []
        for s in ss:
            recs += spec["cells"](s)
        flagged = []
        for r in recs:
            k = (r["census"], r["table_id"], r["_row"], r["_col"])
            if k in FLAGS and not r["flag"]:
                r["flag"] = FLAGS[k][0]
                flagged.append(f"{k[0]} {k[1]} {k[2]} / {k[3]}: {FLAGS[k][1]}")
        kept, compared, diffs, skipped = select(recs, spec["key"], out)
        flagged += [x for o, x in NOTES_FLAG if o == out]
        order = {id(r): i for i, r in enumerate(recs)}
        kept.sort(key=lambda r: (r["year"], ORDER.index(r["census"]), order.get(id(r), 0)))
        fails = CHK.fail[out]
        res[out] = dict(rows=len(kept), checks=CHK.n[out], failed=list(fails), overlap_compared=compared,
                        overlap_not_legible=skipped, overlap_diffs=[list(d) for d in diffs], flagged=flagged,
                        editions=spec["_eds"])
        if write:
            cols = COMMON + spec["dims"] + ["value", "flag"]
            doc = {c: T_DOC[c] for c in cols if c in T_DOC}
            write_csv(out, cols, kept)
            paras = list(PARAS.get(out, [])) + explain_failures(out)
            if out == "posts_savings_accounts":
                paras.append(f"Comparison with the Exploitation table of the same edition (not a check): "
                             f"{CROSS['n']} cells compared, {len(CROSS['diffs'])} differ: " + "; ".join(CROSS["diffs"])
                             + ".")
            if skipped:
                paras.append(f"Printings not compared because the cell is illegible in that printing (cut by the "
                             f"binding): {skipped}.")
            if flagged:
                paras.append("Flagged cells: " + "; ".join(flagged) + ".")
            paras.append("Survey of the whole chapter in every edition: `posts_survey.md`.")
            write_notes(out, CHAPTER, SCRIPT, kept, cols, doc, spec["title_fr"], spec["title_en"], paras,
                        CHK.n[out], fails, compared, diffs, coverage_lines(ss), RULE4, spec["unit"])
    if write:
        res["posts_savings_accounts"]["comparison_with_exploitation"] = dict(compared=CROSS["n"],
                                                                              diffs=CROSS["diffs"])
        write_validation(OUT / f"{PREFIX}_validation.json", dict(
            res, _chapter_views=CHAPTER_VIEWS, _survey=SURVEY, _not_transcribed=NOT_DONE,
            _between_property_and_posts=BETWEEN))
        write_survey()
    return res


BETWEEN = ("Between the Property chapter and Posts, sgt1922-sgt1935 print chapter VII Instruction publique (sgt1922 "
           "f113-f152; it is the public-instruction chapter already extracted elsewhere, not transcribed here); "
           "sgt1936 and sgt1939 print chapter VI Instruction publique between Propriété foncière and Postes "
           "(sgt1936 f68-f77, sgt1939 f65-f76).")


def write_survey():
    L = ["# Posts chapter: survey of every edition", "",
         "Page-by-page survey of the *Postes - Télégraphes - Téléphones* chapter (chapter VIII up to sgt1935, chapter "
         "VII in sgt1936 and sgt1939). Views confirmed on the page images (contact sheets from the view before the "
         "chapter title to the next chapter title); every table read cell by cell on native-resolution crops. "
         "Extraction: `extract_posts.py`.", "",
         "| edition | ark | views |", "|---|---|---|"]
    L += [f"| {e} | `{EDITIONS[e]}` | {a}–{b} |" for e, (a, b) in CHAPTER_VIEWS.items()]
    L += ["", "## Views per edition", ""] + [f"- **{e}**: {t}" for e, t in SURVEY.items()]
    L += ["", "## Tables (CSV) and the sections they hold", "",
          "| CSV | transcription sections | editions | read on the image |", "|---|---|---|---|"]
    for out, spec in TABLES.items():
        L.append(f"| `{out}` | {', '.join(spec['secs'])} | {', '.join(spec.get('_eds', []))} | every printing, "
                 f"cell by cell |")
    L += ["", "## Image versus OCR", "", "Every section of every edition is marked `img: all` in the transcriptions. "
          "For some printings the Gallica word OCR was used to lay out a draft, which was then corrected line by line "
          "against crops of the page image; the image is the source of every value. The overlapping years were read "
          "anew on each printing (not copied from another edition), so the overlap comparisons compare independent "
          "readings.", "", "## Between Property and Posts", "", BETWEEN, "", "## Coverage", "", NOT_DONE, ""]
    (OUT / "posts_survey.md").write_text("\n".join(L) + "\n")


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
        for x in d["flagged"]:
            print("   FLAG", x)


if __name__ == "__main__":
    main()
