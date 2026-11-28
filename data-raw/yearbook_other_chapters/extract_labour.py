#!/usr/bin/env python3
"""Labour and social welfare chapter (*Travail et prévoyance sociale*: chapter XIV in sgt1925, XV in sgt1926-sgt1930
and sgt1936-sgt1939, XVI in sgt1935) of the Statistique générale de la Tunisie, editions sgt1925-sgt1939.
(Up to sgt1924 the labour tables sit in the economic-institutions chapter: `labour_early_*`, another script.)

Tables: habitations à bon marché (dwellings built; subsidies and capital invested), accidents du travail
(by nationality, by outcome, by material cause, per occupational category), strikes (yearly series and the detail
of each strike), Office du Placement Français (applications, offers, placements), cost-of-living indices, and
sgt1939's collective agreements, arbitration awards and immigrant-worker visas.

  python3 extract_labour.py check   parse the transcriptions, run every check, print failures
  python3 extract_labour.py build   ... and write csv/labour_*.csv, their .md notes, csv/labour_survey.md and
                                    csv/labour_validation.json

Source of truth: transcribed/labour_<edition>.txt (format in yb_tables.py, plus the section keys below). Every
cell was read on the native-resolution page images (crops); see the notes of each table.

Section keys used here (besides view/page/year/years):
  view2/page2/split   two-page spread: columns from `split` onward are printed on view2/page2
  mismatch="lab:col;..."   cell flagged total_mismatch (printed value kept; row and column totals both disagree)
  prefer="lab:col=edition;..."   cell misprinted here: the series takes it from that edition (reprint_corrected)
  derive="lab:col"     illegible cell solved from the printed column total (derived_from_totals)
  derive_row="lab:col;..."  illegible or blank cell solved from the printed row total (derived_from_totals)
  realigned="lab:cols;..." cells printed on another line, stored on the line they belong to (row_realigned;
                       '*' = every column)
"""
import re
import sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path as _Path

sys.path.insert(0, str(_Path(__file__).resolve().parent))  # shared helper yb_tables.py
from yb_tables import (COMMON, EDITIONS, ORDER, OUT, TR, Checks, coverage_lines, fmt_val, parse, ssum, where,
                       write_csv, write_notes, write_validation)

CHAPTER = "Travail et prévoyance sociale"
SCRIPT = "extract_labour.py"
PREFIX = "labour"
EDS = ["sgt1925", "sgt1926", "sgt1927", "sgt1928", "sgt1929", "sgt1930", "sgt1935", "sgt1936", "sgt1939"]

# chapter title view .. last view of the chapter (the alphabetical / analytical index that follows is not part of
# it), confirmed on the images
CHAPTER_VIEWS = {
    "sgt1925": (513, 524), "sgt1926": (1037, 1044), "sgt1927": (501, 510), "sgt1928": (1031, 1040),
    "sgt1929": (509, 518), "sgt1930": (1045, 1054), "sgt1935": (319, 328), "sgt1936": (188, 197),
    "sgt1939": (163, 175),
}
ED_YEAR = {e: int(e[3:]) for e in EDS}
CHK = Checks()


def keyval(sec, name):
    """parse 'a:b;c:d' section keys into a list of (label, rest)"""
    v = sec.get(name)
    if not v:
        return []
    out = []
    for item in v.split(";"):
        lab, rest = item.rsplit(":", 1)
        out.append((lab.strip(), rest.strip()))
    return out


def page_of(sec, col):
    if sec.get("split") and sec["cols"].index(col) >= sec["cols"].index(sec["split"]):
        return int(sec["page2"]), int(sec["view2"])
    return sec["page"], sec["view"]


def rec(sec, col, year, cell, **dims):
    page, view = page_of(sec, col)
    r = {"census": sec["ed"], "table_id": sec["table"], "gallica_ark": sec["ark"], "source_page": page,
         "gallica_view": view, "year": year}
    r.update(dims)
    r["value"] = cell.value
    r["flag"] = cell.flag
    lab = dims.get("_label")
    for l, c in keyval(sec, "mismatch"):
        if l == lab and c == col:
            r["flag"] = "total_mismatch"
    for l, rest in keyval(sec, "prefer"):
        c, ed = rest.split("=")
        if l == lab and c == col:
            r["_prefer"] = ed
    for l, cs in keyval(sec, "realigned"):
        if l == lab and (cs == "*" or col in cs.split(",")):
            if not r["flag"]:
                r["flag"] = "row_realigned"
    r.pop("_label", None)
    return r


def apply_derive(sec):
    for lab, col in keyval(sec, "derive"):
        rows = [r for r in sec["rows"] if "cells" in r]
        tot = [r for r in rows if r["label"].startswith("Tota")][0]
        others = [r["cells"][col].value for r in rows if not r["label"].startswith("Tota") and r["label"] != lab
                  and r["cells"][col].value is not None]
        cell = [r for r in rows if r["label"] == lab][0]["cells"][col]
        cell.value = tot["cells"][col].value - sum(others, Decimal(0))
        cell.flag = "derived_from_totals"
        sec.setdefault("_derived", []).append((lab, col))
    for lab, col in keyval(sec, "derive_row"):
        r = [r for r in sec["rows"] if "cells" in r and r["label"] == lab][0]["cells"]
        others = [r[c].value for c in sec["cols"] if c not in (col, "total")]
        r[col].value = r["total"].value - sum(others, Decimal(0))
        r[col].flag = "derived_from_totals"


def data_rows(sec):
    return [r for r in sec["rows"] if "cells" in r and not re.match(r"(?i)^(totaux|total)", r["label"])]


def total_row(sec, label="Totaux"):
    for r in sec["rows"]:
        if r["label"] == label:
            return r["cells"]
    return None


def chk_colsum(out, sec, cols=None, label="Totaux", skip=()):
    t = total_row(sec, label)
    if t is None:
        return
    for c in cols or sec["cols"]:
        if c in skip or t[c].value is None:
            continue
        vals = [r["cells"][c].value for r in data_rows(sec) if r["cells"][c].flag != "not_applicable"]
        if any(x is None for x in vals):
            continue
        if any(r["cells"][c].flag == "derived_from_totals" for r in data_rows(sec)):
            continue
        CHK.eq(out, f"{where(sec)} {c}: lines vs {label}", sum(vals, Decimal(0)), t[c].value)


def chk_identity(out, sec, rows=None):
    for tgt, parts in sec.get("checks", []):
        for r in (rows if rows is not None else [x for x in sec["rows"] if "cells" in x]):
            c = r["cells"]
            vals = [c[p].value for p in parts]
            if any(x is None for x in vals) or c[tgt].value is None:
                continue
            CHK.eq(out, f"{where(sec)} {r['label']}: {tgt} = {' + '.join(parts)}", sum(vals, Decimal(0)),
                   c[tgt].value)


# ----------------------------------------------------------------- selection

def select(recs, key):
    """Rule 4 (and rule 5 tables printed twice): one record per key from the latest edition printing a legible
    value (an aligned printing before a realigned one); a misprint marked `prefer` is replaced by the named
    edition's printing (reprint_corrected). Every other legible printing is compared."""
    by = defaultdict(list)
    for r in recs:
        by[tuple(r.get(k) for k in key)].append(r)
    kept, n, diffs = [], 0, []
    for k, rs in by.items():
        rs.sort(key=lambda r: ORDER.index(r["census"]))
        legible = [r for r in rs if r["value"] is not None]
        aligned = [r for r in legible if r["flag"] != "row_realigned"]
        last = (aligned or legible or rs)[-1]
        for r in rs:
            if r is last or r["value"] is None or last["value"] is None:
                continue
            n += 1
            if r["value"] != last["value"]:
                diffs.append((k, r["census"], r["value"], last["census"], last["value"]))
        if last.get("_prefer"):
            alt = [r for r in rs if r["census"] == last["_prefer"]][0]
            last = dict(alt, flag="reprint_corrected")
        kept.append(last)
    return kept, n, diffs


# ----------------------------------------------------------------- HBM

HBM_TYPE = {
    "indiv": ("individual_and_collective", "Maisons individuelles"),
    "coll": ("collective", "Maisons collectives (nombre de logements)"),
    "workers": ("workers", "Logements ouvriers (individuels)"),
    "military": ("military", "Logements militaires"),
    "maritime": ("maritime", "Logements maritimes"),
}
HBM_TYPE["indiv"] = ("individual", "Maisons individuelles")
HBM_FIN = {
    "subv": ("state_subsidy", "Subventions de l'Etat", "", ""),
    "cap": ("capital_invested", "Capitaux investis", "individual_and_collective",
            "Maisons individuelles et collectives"),
    "cap_workers": ("capital_invested", "Capitaux investis", "workers", "Logements ouvriers"),
    "cap_military": ("capital_invested", "Capitaux investis", "military", "Logements militaires"),
    "cap_maritime": ("capital_invested", "Capitaux investis", "maritime", "Logements maritimes"),
}


def span(label):
    m = re.fullmatch(r"(\d{4})(?:\s*(?:à|-)\s*(\d{4}))?", label)
    a = int(m.group(1))
    return a, int(m.group(2) or a)


def cells_hbm_built(sec):
    out = []
    for r in data_rows(sec):
        a, b = span(r["label"])
        for c in sec["cols"]:
            cell = r["cells"][c]
            if cell.flag == "not_applicable":
                continue
            t, tfr = HBM_TYPE[c]
            out.append(rec(sec, c, b, cell, _label=r["label"], year_from=a, period_fr=r["label"],
                           housing_type=t, housing_type_fr=tfr, unit="dwellings"))
    return out


def cells_hbm_finance(sec):
    out = []
    for r in data_rows(sec):
        a, b = span(r["label"])
        for c in sec["cols"]:
            cell = r["cells"][c]
            if cell.flag == "not_applicable":
                continue
            m, mfr, t, tfr = HBM_FIN[c]
            out.append(rec(sec, c, b, cell, _label=r["label"], year_from=a, period_fr=r["label"], measure=m,
                           measure_fr=mfr, housing_type=t, housing_type_fr=tfr, unit="francs"))
    return out


def select_periods(recs, group):
    """HBM: periods differ between editions (single years, bracketed pairs, '1912 à 1919/1920'). Within a group
    (measure, housing type) a printing is kept unless a later edition prints any year of its period; printings
    of the identical period are compared."""
    by = defaultdict(list)
    for r in recs:
        by[tuple(r[k] for k in group)].append(r)
    kept, n, diffs = [], 0, []
    for g, rs in by.items():
        for r in rs:
            later = [x for x in rs if ORDER.index(x["census"]) > ORDER.index(r["census"])
                     and x["year_from"] <= r["year"] and x["year"] >= r["year_from"]]
            same = [x for x in later if (x["year_from"], x["year"]) == (r["year_from"], r["year"])]
            if same:
                n += 1
                last = max(same, key=lambda x: ORDER.index(x["census"]))
                if r["value"] != last["value"] and r["value"] is not None and last["value"] is not None:
                    diffs.append((g + (r["period_fr"],), r["census"], r["value"], last["census"], last["value"]))
            if not later:
                if r.get("_prefer"):
                    alt = [x for x in rs if x["census"] == r["_prefer"]
                           and (x["year_from"], x["year"]) == (r["year_from"], r["year"])][0]
                    n += 1
                    diffs.append((g + (r["period_fr"],), alt["census"], alt["value"], r["census"], r["value"]))
                    r = dict(alt, flag="reprint_corrected")
                kept.append(r)
    return kept, n, diffs


def chk_hbm(sec):
    out = "labour_hbm_dwellings" if sec["table"] == "hbm_built" else "labour_hbm_finance"
    chk_colsum(out, sec)
    t, g = total_row(sec), total_row(sec, "Total général")
    if t is not None and g is not None:
        cols = [c for c in sec["cols"] if c != "subv"]
        CHK.eq(out, f"{where(sec)} Total général = sum of the Totaux " + "+".join(cols),
               ssum(t[c].value for c in cols), g[cols[0]].value)


def chk_hbm_pending(sec):
    out = "labour_hbm_pending"
    CHK.eq(out, f"{where(sec)} Total = sum of the items", ssum(r["cells"]["n"].value for r in data_rows(sec)),
           total_row(sec, "Total")["n"].value)


def cells_hbm_pending(sec):
    return [rec(sec, "n", int(sec["year"]), r["cells"]["n"], project_fr=r["label"], unit="dwellings")
            for r in data_rows(sec)]


# ----------------------------------------------------------------- accidents

CATEGORY = {
    # sgt1925-sgt1926 ("Professions")
    "Alimentation": "food", "Métallurgie": "metallurgy", "Tabac, Services d'Etat": "tobacco_state_services",
    "Electricité, Eau, Gaz": "electricity_water_gas", "Mines et Carrières": "mines_quarries",
    "Transports : transport": "transport_operations", "Transports : ateliers": "transport_workshops",
    "Construction": "construction", "Manutention": "handling", "Chaux et Ciment": "lime_cement",
    "Industrie du bois": "wood_industry", "Agriculture": "agriculture", "Autres": "other",
    # sgt1927-sgt1935, sgt1939 ("Catégories professionnelles")
    "Agriculture et forêts": "agriculture_forestry",
    "Alimentation (moulins, boissons, produits alimentaires, tabacs)": "food_drink_tobacco",
    "Mines": "mines", "Grande et petite métallurgie": "metallurgy",
    "Pierres et terres (carrières, pierres au feu)": "stone_earth",
    "Pierres et terres (carrières, pierres à feu)": "stone_earth",
    "Bâtiment et travaux publics, théâtre": "building_public_works", "Bois et bimbeloterie": "wood_toys",
    "Industries chimiques, services d'eau et gaz et d'électricité": "chemicals_utilities",
    "Industries chimiques, service d'eau et gaz et d'électricité": "chemicals_utilities",
    "Industrie textile, nettoyage, cuirs et peaux": "textiles_cleaning_leather",
    "Papier et industrie polygraphique": "paper_printing",
    "Transports : chemins de fer et tramways, autres transports par terre et entrepôts, poste et télégraphe, "
    "navigation aérienne et maritime": "transport",
    "Transports : chemins de fer et tramways, autres transports par terre entrepôts, poste et télégraphe, "
    "navigation aérienne et maritime": "transport",
    "Commerce de gros et de détail, banques": "commerce_banking", "Armées de terre et de mer": "armed_forces",
    # sgt1936 nationality table
    "Mines et carrières": "mines_quarries", "Bâtiments et travaux publics": "building_public_works",
    "Transports": "transport", "Commerce": "commerce", "Autres professions": "other",
}
NAT = {"french": "Français", "italian": "Italiens", "indigenous": "Indigènes", "foreign": "Etrangers"}


def nat_fr(ed, c):
    if c == "indigenous" and ed in ("sgt1935", "sgt1936", "sgt1939"):
        return "Tunisiens"
    if c == "foreign" and ed not in ("sgt1925", "sgt1926"):
        return "Autres étrangers"
    return NAT[c]


SEV = {"dead": ("dead", "Morts"),
       "inc_more1m": ("incapacity_over_1_month", "Incapacités de plus d'un mois"),
       "inc_less1m": ("incapacity_under_1_month", "Incapacités de moins d'un mois"),
       "inc_perm": ("permanent_incapacity", "Incapacité permanente"),
       "inc_temp": ("temporary_incapacity_over_4_days", "Incapacité temporaire de plus de 4 jours"),
       "unknown": ("outcome_unknown", "Suites inconnues")}
CAUSE_OLD = {
    "motors": "Moteurs", "transmission": "Transmission", "machines": "Machines outils, Métiers",
    "lifting": "Ascenseurs, Grues, Appareils de levage", "autoclaves": "Autoclaves, Chaudières à vapeur",
    "explosives": "Explosifs", "hot_matter": "Matières incandescentes, brûlantes, corrosives",
    "falling_objects": "Eboulements, chute d'objets, etc.", "worker_fall": "Chute de l'ouvrier d'une échelle, etc.",
    "handling": "Manutention de fardeaux", "traction": "Traction - Accidents occasionnés par les animaux",
    "hand_tools": "Outils à main : scies, hâches, marteaux", "miscellaneous": "Causes diverses",
    "unknown": "Causes inconnues", "footwear": "Défaut de chaussures"}
CAUSE_NEW = {
    "motors": "Machines : moteurs", "transmission": "Machines : transmission",
    "machines": "Machines : machines, outils, métiers", "lifting": "Ascenseurs, grues, appareils de levage",
    "boilers": "Chaudières, canalisations de vapeur, explosions", "explosives": "Matières explosibles",
    "hot_matter": "Matières brûlantes et corrosives", "collapse": "Rupture, renversement, éboulement d'objets",
    "falls_height": "Chutes d'endroits élevés", "loading": "Chargement et déchargement à la main",
    "vehicles": "Véhicules et animaux", "railways": "Voies ferrées", "navigation": "Navigation",
    "hand_tools": "Outils à main, éclats et fragments y compris", "miscellaneous": "Divers"}
CAUSE_CODE = {"motors": "machine_motors", "transmission": "machine_transmission",
              "machines": "machine_tools_looms"}


def acc_year(sec):
    return int(sec["year"]) if sec.get("year") else ED_YEAR[sec["ed"]]


def cells_acc_nat(sec):
    out = []
    y = acc_year(sec)
    for r in data_rows(sec):
        cat = CATEGORY[r["label"]]
        for c in sec["cols"]:
            cell = r["cells"][c]
            if c == "total":
                if not sec.get("natna"):
                    continue
                out.append(rec(sec, c, y, cell, _label=r["label"], category=cat, category_fr=r["label"],
                               nationality="TOTAL (printed)", nationality_fr="Totaux"))
                continue
            if sec.get("natna"):
                continue   # printed » throughout: nationality not counted in 1936 (footnote)
            out.append(rec(sec, c, y, cell, _label=r["label"], category=cat, category_fr=r["label"],
                           nationality=c, nationality_fr=nat_fr(sec["ed"], c)))
    return out


def cells_acc_sev(sec):
    out = []
    y = acc_year(sec)
    for r in data_rows(sec):
        cat = CATEGORY[r["label"]]
        for c in sec["cols"]:
            if c == "total":
                continue
            o, ofr = SEV[c]
            out.append(rec(sec, c, y, r["cells"][c], _label=r["label"], category=cat, category_fr=r["label"],
                           outcome=o, outcome_fr=ofr))
    return out


def cells_acc_cause(sec):
    out = []
    y = acc_year(sec)
    labels = CAUSE_OLD if sec["ed"] in ("sgt1925", "sgt1926") else CAUSE_NEW
    for r in data_rows(sec):
        cat = CATEGORY[r["label"]]
        for c in sec["cols"]:
            if c == "total":
                continue
            out.append(rec(sec, c, y, r["cells"][c], _label=r["label"], category=cat, category_fr=r["label"],
                           cause=CAUSE_CODE.get(c, c), cause_fr=labels[c]))
    return out


def chk_acc(out):
    def f(sec):
        if sec.get("natna"):
            t = total_row(sec, "Total")
            CHK.eq(out, f"{where(sec)} total: lines vs Total", ssum(r["cells"]["total"].value for r in data_rows(sec)),
                   t["total"].value)
            return
        chk_identity(out, sec, data_rows(sec))
        chk_identity(out, sec, [{"label": "Totaux", "cells": total_row(sec)}])
        chk_colsum(out, sec)
    return f


# ----------------------------------------------------------------- strikes

STRIKE_M = {"strikes": ("strikes", "Nombre de grèves", "count"),
            "days": ("duration_days", "Durée en jours des grèves", "days"),
            "establishments": ("establishments", "Nombre d'établissements atteints", "count"),
            "strikers": ("strikers", "Nombre de grévistes", "count"),
            "success": ("result_success", "Résultats : réussite", "count"),
            "transaction": ("result_compromise", "Résultats : transaction", "count"),
            "failure": ("result_failure", "Résultats : échec", "count")}


def cells_strikes(sec):
    out = []
    for r in data_rows(sec):
        for c in sec["cols"]:
            m, mfr, unit = STRIKE_M[c]
            out.append(rec(sec, c, int(r["label"]), r["cells"][c], _label=r["label"], measure=m, measure_fr=mfr,
                           unit=unit))
    return out


def chk_strikes(sec):
    chk_identity("labour_strikes", sec, data_rows(sec))


RESULT = {"Réussite": "success", "Echec": "failure", "Transaction": "compromise",
          "Reprise du travail aux anciennes conditions.": "failure",
          "Reprise du travail aux anciennes conditions": "failure",
          "Reprise du travail avec augmentation de salaires.": "compromise"}
DETAIL_M = [("duration_days", "Durée en jours des grèves", "days"),
            ("establishments", "Nombre d'établissements atteints", "count"),
            ("strikers", "Nombre de grévistes", "count")]


class _C:
    def __init__(self, v):
        self.value, self.flag = Decimal(v), ""


def cells_strike_detail(sec):
    out = []
    y = acc_year(sec)
    for r in sec["rows"]:
        occ, loc, d, e, s, goal, res = r["text"]
        for (m, mfr, unit), v in zip(DETAIL_M, (d, e, s)):
            x = rec(sec, "x", y, _C(v), strike_no=int(r["label"]), occupation_fr=occ, locality=loc, goal_fr=goal,
                    result=RESULT[res], result_fr=res, measure=m, measure_fr=mfr, unit=unit)
            if m == "duration_days":
                x["source_page"], x["gallica_view"] = sec["page"], sec["view"]
            else:
                x["source_page"], x["gallica_view"] = int(sec["page2"]), int(sec["view2"])
            out.append(x)
    return out


# ----------------------------------------------------------------- placement

OCC = {"Agriculture": "agriculture", "Commerce et Industrie": "commerce_industry",
       "Commerce et industrie": "commerce_industry", "Commerce et transports terrestres": "commerce_industry",
       "Bâtiment": "building", "Métallurgie": "metallurgy", "Mines et Carrières": "mines_quarries",
       "Mines et carrières": "mines_quarries", "Services domestiques": "domestic_services",
       "Services publics": "public_services", "Industrie hôtelière": "public_services", "Divers": "miscellaneous"}
PLACE_M = {"d": ("applications", "Demandes d'emploi"), "o": ("offers", "Offres d'emploi"),
           "p": ("placements", "Placements effectués")}


def cells_placement(sec):
    out = []
    for r in data_rows(sec):
        for c in sec["cols"]:
            m, mfr = PLACE_M[c[0]]
            out.append(rec(sec, c, int(c[1:]), r["cells"][c], _label=r["label"], occupation=OCC[r["label"]],
                           occupation_fr=r["label"], measure=m, measure_fr=mfr))
    return out


# ----------------------------------------------------------------- cost of living

GROUP = {"french": ("french", "Français"), "italian": ("italian", "Italiens"),
         "indigenous": ("indigenous", "Indigènes")}
PERIOD_FR = {"year": "année", "s1": "1er semestre", "s2": "2e semestre", "t1": "1er trimestre",
             "t2": "2e trimestre", "t3": "3e trimestre", "t4": "4e trimestre"}


def cells_col(sec):
    out = []
    for r in data_rows(sec):
        parts = r["label"].split()
        y = int(parts[0])
        per = parts[1] if len(parts) > 1 else "year"
        basis = "all_expenditure" if (y, per) >= (1928, "t4") else "food_only"
        for c in sec["cols"]:
            g, gfr = GROUP[c]
            if c == "indigenous" and sec["ed"] == "sgt1939":
                gfr = "Indigènes"
            out.append(rec(sec, c, y, r["cells"][c], period=per, period_fr=PERIOD_FR[per], group=g, group_fr=gfr,
                           basis=basis))
    return out


# ----------------------------------------------------------------- sgt1939 tables

def cells_visas(sec):
    out = []
    if sec["table"] == "visas":
        for r in sec["rows"]:
            if r["label"] in ("Visas accordés", "Renouvellements et transferts"):
                continue
            out.append(rec(sec, "n", int(sec["year"]), r["cells"]["n"], item=r["label"].lower()
                           .replace(" ", "_").replace("renouvellements", "renewals").replace("transferts", "transfers")
                           .replace("immigrants_nouveaux", "new_immigrants"), item_fr=r["label"], trade="",
                           trade_fr="", nationality="", nationality_fr=""))
        return out
    TR_ = {"Industrie forestière": "forestry", "Bâtiment et Métallurgie": "building_metallurgy",
           "Services domestiques": "domestic_services", "Divers": "miscellaneous"}
    NF = {"italian": "Italiens", "dutch": "Hollandais", "swiss": "Suisses", "other": "Autres nationalités"}
    for r in data_rows(sec):
        for c in sec["cols"]:
            if c == "total":
                continue
            out.append(rec(sec, c, int(sec["year"]), r["cells"][c], item="new_immigrants",
                           item_fr="Immigrants nouveaux (répartition des visas accordés)", trade=TR_[r["label"]],
                           trade_fr=r["label"], nationality=c, nationality_fr=NF[c]))
    return out


def chk_visas(sec):
    out = "labour_immigration_visas"
    if sec["table"] == "visas":
        v = {r["label"]: r["cells"]["n"].value for r in sec["rows"]}
        CHK.eq(out, f"{where(sec)} 259 = renewals + transfers", v["Renouvellements"] + v["Transferts"],
               v["Renouvellements et transferts"])
        CHK.eq(out, f"{where(sec)} visas = 259 + new immigrants", v["Renouvellements et transferts"]
               + v["Immigrants nouveaux"], v["Visas accordés"])
        return
    chk_identity(out, sec, [r for r in sec["rows"] if "cells" in r])
    chk_colsum(out, sec)


# ----------------------------------------------------------------- table specs

DOC = {
    "census": "edition the value is taken from (rule 4 series: the latest edition printing it; rule 5: the edition)",
    "table_id": "transcription section",
    "gallica_ark": "Gallica volume ark (views are numbered within a volume)",
    "source_page": "printed page number (two-page spreads: the page the cell is printed on)",
    "gallica_view": "Gallica view (fNNNN)",
    "year": "year of the figures (HBM: last year of the printed period)",
    "year_from": "first year of the printed period",
    "period_fr": "period as printed ('1912 à 1919'; '1925-1926' = years joined by a printed bracket)",
    "housing_type": "type of dwelling (English code)", "housing_type_fr": "printed column heading",
    "project_fr": "project as printed in the observations column",
    "measure": "measure code (English)", "measure_fr": "printed heading",
    "unit": "unit of `value`",
    "category": "occupational category (English code; the list changes in sgt1927 and sgt1936)",
    "category_fr": "category as printed",
    "nationality": "nationality of the victims / immigrants (English code)", "nationality_fr": "printed heading",
    "outcome": "outcome of the accident (English code)", "outcome_fr": "printed heading",
    "cause": "material cause (English code; the list changes in sgt1927)", "cause_fr": "printed heading",
    "strike_no": "order of the strike in the printed list", "occupation_fr": "occupation as printed",
    "locality": "locality as printed", "goal_fr": "aim of the strike as printed",
    "result": "result (English code: success, compromise, failure; sgt1935 'reprise du travail aux anciennes "
              "conditions' = failure, 'avec augmentation de salaires' = compromise, as counted in that edition's "
              "yearly line: 0 réussite, 2 transactions, 5 échecs)",
    "result_fr": "result as printed",
    "occupation": "occupational category (English code)",
    "period": "year / s1-s2 (half-years) / t1-t4 (quarters)", "period_fr": "period as printed",
    "group": "family group of the index (English code)", "group_fr": "printed heading",
    "basis": "food_only (indices up to the 3rd quarter 1928: food expenditure only) or all_expenditure (from the "
             "4th quarter 1928: food, heating and lighting, housing, clothing, miscellaneous)",
    "item": "item (English code)", "item_fr": "printed label",
    "trade": "trade (corps de métier, English code)", "trade_fr": "printed label",
    "value": "printed value (» = 0)",
    "flag": "empty, ocr_corrected, illegible, total_mismatch, derived_from_totals, not_applicable, "
            "reprint_corrected or row_realigned",
}

RULE4 = ("Printed for overlapping windows: each cell is taken from the **latest** edition that prints it "
         "(SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on its own "
         "page image, is compared below.")
RULE5 = ("Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept, with `year` (the edition year "
         "when no year is printed); a year printed by two editions is stored once, from the later one, and "
         "compared.")
RULEP = ("Printed for overlapping periods whose grouping changes between editions (single years, bracketed pairs, "
         "'1912 à 1919' / '1912 à 1920'): within each measure and housing type a printing is kept unless a later "
         "edition prints any year of its period (SPEC_ADDENDUM rule 4 applied to periods; `census` = that "
         "edition); printings of the identical period are compared below.")

TABLES = {
    "labour_hbm_dwellings": dict(
        secs=["hbm_built"], cells=cells_hbm_built, periods=["housing_type"],
        dims=["year_from", "period_fr", "housing_type", "housing_type_fr", "unit"],
        title_fr="Habitations à bon marché. a) Logements construits",
        title_en="Low-cost housing (habitations à bon marché): dwellings built, by period and type",
        unit="Unit: dwellings; value_type: count.",
        paras=["Printed sgt1927-sgt1939 (headed 1912-<edition year>; sgt1935 and sgt1936 stop at 1934, sgt1939 at "
               "1939). Columns: maisons individuelles; maisons collectives (number of dwellings); from sgt1929 "
               "logements ouvriers and logements militaires; from sgt1935 logements maritimes. The Totaux line and "
               "the Total général (sum of the Totaux) are checks only. sgt1927 prints the early years one by one "
               "(1912, 1914, 1917, 1919), later editions as '1912 à 1919' or '1912 à 1920'. Observations column: "
               "sgt1927-sgt1929 'En cours d'adjudication (ou de construction)' on the edition year; sgt1930 a list of "
               "projects under award (`labour_hbm_pending`).",
               "sgt1939 prints the 1925-1927 bracket with 104 and 204 on the line 1928; stored on 1925-1926 and "
               "1927-1928 as in every earlier edition (`row_realigned`)."]),
    "labour_hbm_finance": dict(
        secs=["hbm_finance"], cells=cells_hbm_finance, periods=["measure", "housing_type"],
        dims=["year_from", "period_fr", "measure", "measure_fr", "housing_type", "housing_type_fr", "unit"],
        title_fr="Habitations à bon marché. b) Subventions de l'Etat et capitaux investis",
        title_en="Low-cost housing: state subsidies and capital invested, by period and type of dwelling",
        unit="Unit: francs (as printed, centimes after the point); value_type: francs.",
        paras=["Printed sgt1927-sgt1936 (not in sgt1939). Subsidies are printed per year; capital invested is "
               "printed per year or for bracketed pairs of years (1925-1926, 1927-1928, 1929-1930). Capital columns "
               "stand under the housing types of table a): maisons individuelles et collectives; from sgt1929 "
               "logements ouvriers and militaires; from sgt1935 maritimes. sgt1927 observation 1912: 'Travaux "
               "réalisés avec la participation de l'Etat français'. sgt1930 prints the 1930 subsidy as '1.00.1000'; "
               "the Totaux gives 1.100.000 (`derived_from_totals`). sgt1936 prints 7.830.808 on the line 1927 and "
               "16.814.168 / 9.768.737 between 1928 and 1929: stored as in sgt1935 (`row_realigned`)."]),
    "labour_hbm_pending": dict(
        secs=["hbm_award"], cells=cells_hbm_pending, key=["year", "project_fr"],
        dims=["project_fr", "unit"],
        title_fr="Habitations à bon marché. Logements en cours d'adjudication (observations, 1930)",
        title_en="Low-cost housing: dwellings under award in 1930 (observations column of sgt1930)",
        unit="Unit: dwellings; value_type: count.",
        paras=["Printed in sgt1930 only, in the observations column of table a): 'En cours d'adjudication', four "
               "numbered projects and their total (139, a check)."]),
    "labour_accidents_nationality": dict(
        secs=["acc_nat"], cells=cells_acc_nat, key=["year", "category", "nationality"], rule5=True,
        dims=["category", "category_fr", "nationality", "nationality_fr"],
        title_fr="Accidents du travail. a) Répartition des accidents d'après la nationalité des victimes",
        title_en="Industrial accidents by occupational category and nationality of the victim",
        unit="Unit: accidents; value_type: count.",
        paras=["Printed in every edition sgt1925-sgt1939 without a year in the title: `year` = edition year. "
               "Categories: 13 'professions' in sgt1925-sgt1926, 14 'catégories professionnelles' from sgt1927, 7 "
               "in sgt1936. Nationality columns: Français, Italiens, Indigènes, Etrangers (sgt1925-sgt1926); "
               "Français, Indigènes (from sgt1935 'Tunisiens'), Italiens, Autres étrangers. The row totals and the "
               "Totaux line are checks only.",
               "sgt1936: footnote (1) 'Le dépouillement par nationalité n'a pu être effectué en 1936'; the "
               "nationality columns are printed » throughout and not stored; the category totals are stored "
               "(`nationality` = `TOTAL (printed)`). Their printed TOTAL 18.930 exceeds the sum of the seven "
               "lines (17.972) by 958; every figure re-read on a crop.",
               "Flagged `total_mismatch` (printed value kept; the row total and the column total both need the "
               "same other figure): sgt1935 Mines / autres étrangers printed 11 (511 needed); sgt1939 Transports "
               "/ Italiens printed 295 (292 needed)."]),
    "labour_accidents_outcome": dict(
        secs=["acc_sev"], cells=cells_acc_sev, key=["year", "category", "outcome"], rule5=True,
        dims=["category", "category_fr", "outcome", "outcome_fr"],
        title_fr="Accidents du travail. b) Répartition d'après la gravité / Suites connues ou probables des accidents",
        title_en="Industrial accidents by occupational category and outcome (deaths, incapacity)",
        unit="Unit: accidents; value_type: count.",
        paras=["Printed sgt1925-sgt1935 and sgt1939 (not in sgt1936). sgt1925-sgt1926 'Répartition d'après la "
               "gravité': morts, incapacités de plus d'un mois, de moins d'un mois. From sgt1927 'Suites connues ou "
               "probables': morts, incapacité permanente, incapacité temporaire de plus de 4 jours, suites "
               "inconnues. `year` = edition year. Row totals and Totaux are checks only.",
               "sgt1929 Commerce de gros, incapacité permanente: left blank in the print (stored NA, "
               "`not_applicable`; the row total gives 4, the column total 61). sgt1939: the TOTAUX column repeats "
               "the nationality table except Autres (145 / 153), three lines and three column totals do not add "
               "up (see the failed checks); every cell re-read on zoomed crops, no single faulty cell."]),
    "labour_accidents_causes": dict(
        secs=["acc_cause"], cells=cells_acc_cause, key=["year", "category", "cause"], rule5=True,
        dims=["category", "category_fr", "cause", "cause_fr"],
        title_fr="Accidents du travail. c) Causes matérielles des accidents dans les diverses catégories "
                 "professionnelles",
        title_en="Industrial accidents by occupational category and material cause",
        unit="Unit: accidents; value_type: count.",
        paras=["Printed in every edition, on a two-page spread. 15 causes in sgt1925-sgt1926 (moteurs ... défaut de "
               "chaussures), a new list of 15 from sgt1927 (machines: moteurs, transmission, machines-outils-métiers; "
               "ascenseurs; chaudières; matières explosibles; ... divers). `year` = edition year, except sgt1935 "
               "'survenues en 1935' and sgt1936 '(1935)': sgt1936 reprints the 1935 table in a new setting and is "
               "stored for 1935, with two misprints replaced by sgt1935's printing (`reprint_corrected`): Mines / "
               "véhicules 31 (sgt1935 3; totals need 3) and Industrie textile / matières brûlantes » (sgt1935 1). "
               "No 1936 causes table.",
               "Flagged `total_mismatch`: 1935 Armées / divers printed 11 in both sgt1935 and sgt1936 (61 needed); "
               "sgt1939 Transports / matières brûlantes printed 119 (109 needed). The line totals of sgt1939's "
               "causes table differ from its nationality table for several categories with the same grand total "
               "(printed as such)."]),
    "labour_strikes": dict(
        secs=["strikes"], cells=cells_strikes, key=["year", "measure"],
        dims=["measure", "measure_fr", "unit"],
        title_fr="Grèves. b) Grèves survenues de <année> à <année>",
        title_en="Strikes per year: number, duration, establishments, strikers and results",
        unit="Units: count and days (`unit`); value_type: count.",
        paras=["Ten-year window in every edition (sgt1925 1916-1925 ... sgt1939 1930-1939). 1916-1918 printed » "
               "(no strike). Check: strikes = réussite + transaction + échec. 1936 (sgt1936, sgt1939): 50 strikes, "
               "results printed » » » (not given): the identity fails for 1936 (printed values kept). The yearly "
               "line agrees with the detailed list of the edition year where both exist (see "
               "`labour_strike_details`)."]),
    "labour_strike_details": dict(
        secs=["strike_detail"], cells=cells_strike_detail, key=["year", "strike_no", "measure"], rule5=True,
        dims=["strike_no", "occupation_fr", "locality", "goal_fr", "result", "result_fr", "measure", "measure_fr",
              "unit"],
        title_fr="Grèves. a) Etat détaillé des grèves",
        title_en="Strikes: detail of each strike (occupation, locality, duration, establishments, strikers, aim, "
                 "result)",
        unit="Units: days and count (`unit`); value_type: count.",
        paras=["Printed sgt1926-sgt1930 and sgt1935 (no year in the title to sgt1928: `year` = edition year; "
               "sgt1929, sgt1930, sgt1935 'survenues en <year>'); not in sgt1925, sgt1936, sgt1939. One row per "
               "strike and measure; occupation, locality, aim and result as printed. Checks: the number of strikes, "
               "the sums of days, establishments and strikers and the counts of results equal the yearly line of "
               "`labour_strikes` (same edition)."]),
    "labour_placement": dict(
        secs=["placement"], cells=cells_placement, key=["year", "occupation", "measure"],
        dims=["occupation", "occupation_fr", "measure", "measure_fr"],
        title_fr="Placement. Opérations de l'Office du Placement Français en Tunisie",
        title_en="French Placement Office in Tunisia: job applications, offers and placements by occupation",
        unit="Unit: applications / offers / placements; value_type: count.",
        paras=["Printed sgt1926 (1920-1926) to sgt1939 (1930-1939); not in sgt1925. Eight occupational lines; the "
               "7th, 'Services publics', is headed 'Industrie hôtelière' in sgt1936 and sgt1939 with the same "
               "figures for every year printed before (stored as one line, `public_services`, `occupation_fr` as "
               "printed in the stored edition); 'Commerce et Industrie' is headed 'Commerce et transports "
               "terrestres' in sgt1939 (same figures). Totaux lines are checks only.",
               "Misprints replaced by an earlier printing (`reprint_corrected`): 1923 Métallurgie placements 84 in "
               "sgt1928-sgt1930 (sgt1926-sgt1927 34; Totaux 455 needs 34); 1928 Métallurgie placements 39 in "
               "sgt1936 (99); 1932 Services publics / Industrie hôtelière demandes 296 in sgt1936-sgt1939 (sgt1935 "
               "6.200); 1933 Divers placements '611' in sgt1936-sgt1939 (leading digit lost; sgt1935 2.611). sgt1926 "
               "1922 Bâtiment placements: first digit blotted, 11 from the Totaux (`derived_from_totals`; later "
               "editions print 11). Cells hidden in the gutter (sgt1935 1929 placements and 1930 applications) are "
               "`illegible` and taken from later printings."]),
    "labour_cost_of_living": dict(
        secs=["col"], cells=cells_col, key=["year", "period", "group"],
        dims=["period", "period_fr", "group", "group_fr", "basis"],
        title_fr="Coût de la vie. Nombres-indices du coût de la vie (base : 100 en juillet 1914)",
        title_en="Cost-of-living index numbers for French, Italian and indigenous working families "
                 "(July 1914 = 100)",
        unit="Unit: index, July 1914 = 100; value_type: rate (index numbers).",
        paras=["Printed in every edition from sgt1926 (yearly 1915-1923, half-years 1924-1926, quarters from "
               "1927). Footnote (N.B.): the indices rest on the cost of a working family of four (father, mother, "
               "two children); up to the 3rd quarter 1928 on food expenditure only, from the 4th quarter 1928 on "
               "all expenditure (food, heating and lighting, housing, clothing, miscellaneous) (`basis`); separate "
               "indices for French, Italian and indigenous families 'dont le genre de vie présente des différences "
               "notables'. sgt1939 1939 4th quarter printed » (not available): NA, `not_applicable`. No totals."]),
    "labour_immigration_visas": dict(
        secs=["visas", "visa_trade"], cells=cells_visas, key=["year", "item", "trade", "nationality"], rule5=True,
        dims=["item", "item_fr", "trade", "trade_fr", "nationality", "nationality_fr"],
        title_fr="Immigration des travailleurs. Contrats de travail visés au cours de l'année 1939 ; répartition "
                 "des visas accordés",
        title_en="Immigrant workers: labour contracts visaed in 1939 (renewals, transfers, new immigrants) and "
                 "new immigrants by trade and nationality",
        unit="Unit: visas; value_type: count.",
        paras=["Printed in sgt1939 only (application of the decree of 20 February 1930). Visas accordés 397 and "
               "the bracketed 259 (renouvellements 183 + transferts 76) are totals used as checks; the trade x "
               "nationality table distributes the 138 new immigrants (its totals are checks). Bâtiment et "
               "Métallurgie / Suisses printed '–' (stored 0)."]),
}

TEXT_TABLES = {
    "labour_collective_agreements": dict(
        secs=["conventions", "arbitration"],
        title_fr="Liste des conventions collectives rendues obligatoires par arrêtés au cours de l'année 1939 ; "
                 "Sentences arbitrales ou accords rendus obligatoires en 1939",
        title_en="Collective agreements made binding by order in 1939, and arbitration awards or agreements made "
                 "binding in 1939",
    ),
}
AGREE_COLS = ["census", "table_id", "gallica_ark", "source_page", "gallica_view", "year", "kind", "item_no",
              "award_fr", "order_date_fr", "conclusion_date_fr", "industry_fr", "scope_fr", "publication_date_fr"]


def agreements(secs):
    out = []
    for s in secs:
        for r in s["rows"]:
            t = r["text"]
            base = {"census": s["ed"], "table_id": s["table"], "gallica_ark": s["ark"], "source_page": s["page"],
                    "gallica_view": s["view"], "year": int(s["year"]), "item_no": int(r["label"])}
            if s["table"] == "conventions":
                base.update(kind="collective_agreement", award_fr="", order_date_fr=t[0], conclusion_date_fr=t[1],
                            industry_fr=t[2], scope_fr=t[3], publication_date_fr="")
            else:
                base.update(kind="arbitration_award" if t[0] != "Accord" else "conciliation_agreement",
                            award_fr=t[0], order_date_fr="", conclusion_date_fr=t[1], industry_fr=t[2],
                            scope_fr=t[3], publication_date_fr=t[4])
            out.append(base)
    return out


def write_agreements(secs):
    rows = agreements(secs)
    write_csv("labour_collective_agreements", AGREE_COLS, rows)
    sp = TEXT_TABLES["labour_collective_agreements"]
    doc = {"kind": "collective_agreement (convention collective made binding by an arrêté d'extension, decree of 4 "
                   "August 1936), arbitration_award (sentence arbitrale, named by its arbitrators) or "
                   "conciliation_agreement (accord signed during the compulsory conciliation and arbitration "
                   "procedure, decree of 22 April 1937)",
           "item_no": "order in the printed list", "award_fr": "sentence or accord as printed (arbitrators' names)",
           "order_date_fr": "date of the arrêté d'extension and of its publication in the J.O.T., as printed",
           "conclusion_date_fr": "date of conclusion of the convention / date of the sentence or accord",
           "industry_fr": "industry, trade or commerce as printed", "scope_fr": "champ d'application",
           "publication_date_fr": "date of publication in the J.O. (awards)"}
    L = [f"# {sp['title_fr']}", "", f"*{sp['title_en']}.*", "",
         f"Source: *Statistique générale de la Tunisie*, chapter *{CHAPTER}*, edition sgt1939 (`{EDITIONS['sgt1939']}`), "
         "p. 166, f172 and p. 167, f173. Source gallica.bnf.fr / Ministère des Affaires étrangères.", "",
         "Transcriptions: `../transcribed/labour_sgt1939.txt`; rebuild with "
         "`python3 data-raw/yearbook_other_chapters/extract_labour.py build`.", "",
         f"Rows: {len(rows)} (6 collective agreements, 8 awards or agreements). A text table: one row per printed "
         "line, every field as printed; no numeric values (value_type: text). Read on the page images (all fields).",
         "", "## Columns", ""]
    for c in AGREE_COLS:
        L.append(f"- `{c}`: {doc.get(c) or DOC.get(c, '')}")
    L += ["", "Printed in sgt1939 only. 'Industrie de 'ameublement' is kept as printed (missing l'). No totals: no "
          "checks.", ""]
    (OUT / "labour_collective_agreements.md").write_text("\n".join(L) + "\n")
    return rows


# ----------------------------------------------------------------- cross-table checks

def chk_strike_details(secs):
    out = "labour_strike_details"
    yearly = {}
    for s in secs:
        if s["table"] == "strikes":
            for r in data_rows(s):
                yearly[(s["ed"], int(r["label"]))] = r["cells"]
    for s in secs:
        if s["table"] != "strike_detail":
            continue
        y = acc_year(s)
        line = yearly.get((s["ed"], y))
        if line is None:
            continue
        rows = [r["text"] for r in s["rows"]]
        CHK.eq(out, f"{where(s)} number of strikes vs the yearly line", Decimal(len(rows)), line["strikes"].value)
        for i, c in ((2, "days"), (3, "establishments"), (4, "strikers")):
            CHK.eq(out, f"{where(s)} sum of {c} vs the yearly line", sum(Decimal(t[i]) for t in rows),
                   line[c].value)
        for code, c in (("success", "success"), ("compromise", "transaction"), ("failure", "failure")):
            CHK.eq(out, f"{where(s)} results '{code}' vs the yearly line",
                   Decimal(sum(1 for t in rows if RESULT[t[6]] == code)), line[c].value)


def chk_visas_total(secs):
    v = [s for s in secs if s["table"] == "visas"]
    t = [s for s in secs if s["table"] == "visa_trade"]
    if v and t:
        new = [r for r in v[0]["rows"] if r["label"] == "Immigrants nouveaux"][0]["cells"]["n"].value
        CHK.eq("labour_immigration_visas", f"{where(t[0])} Totaux vs new immigrants", total_row(t[0])["total"].value,
               new)


CHECKERS = {"hbm_built": chk_hbm, "hbm_finance": chk_hbm, "hbm_award": chk_hbm_pending,
            "acc_nat": chk_acc("labour_accidents_nationality"), "acc_sev": chk_acc("labour_accidents_outcome"),
            "acc_cause": chk_acc("labour_accidents_causes"), "strikes": chk_strikes,
            "placement": lambda s: chk_colsum("labour_placement", s), "visas": chk_visas, "visa_trade": chk_visas}

FAIL_NOTES = {
    "labour_hbm_dwellings": "sgt1930 prints the logements ouvriers Totaux 395 for lines giving 305 (its own Total "
        "général 1.826 = 1.201 + 114 + 305 + 206, so the 395 is the misprint).",
    "labour_hbm_finance": "sgt1928 prints the 1912-1919 capital as 538.000 while its Totaux keeps 27.551.897,52, "
        "which needs sgt1927's single years (86.100 + 40.000 + 113.700 + 298.700 = 538.500). sgt1930's Total général "
        "70.764.310,54 is 200 above the sum of its Totaux. sgt1935-sgt1936 print the 1930 subsidy 1.000.000 while "
        "the subsidy Totaux 14.336.000 needs sgt1930's 1.100.000 (the series stores 1.100.000, reprint_corrected); "
        "their Total général 122.856.629 equals the four capital Totaux plus the subsidy Totaux plus 10.000 (no "
        "single cell identified). sgt1936 repeats the capital Totaux 65.145.374 under logements ouvriers (sgt1935: "
        "10.500.000).",
    "labour_accidents_nationality": "sgt1935 Mines / autres étrangers 11 for 511 and sgt1939 Transports / Italiens 295 "
        "for 292 are flagged `total_mismatch`; sgt1936's printed TOTAL 18.930 against 17.972.",
    "labour_accidents_outcome": "sgt1928 Mines / morts printed 3 for 33 (flagged total_mismatch); sgt1939 (see "
        "above).",
    "labour_accidents_causes": "Each failure is one cell flagged `total_mismatch` (row and column both off by the same "
        "amount), or the sgt1936 misprints replaced from sgt1935.",
    "labour_strike_details": "sgt1929: the nine strikes of the detailed list last 62 days in all, the yearly line "
        "prints 65 (both re-read on crops).",
    "labour_strikes": "1936: 50 strikes, results printed » » » (not given), in sgt1936 and sgt1939.",
    "labour_placement": "The 1923 offres Totaux 588 for lines summing to 587 (sgt1928-sgt1930); 1934 applications "
        "Totaux 11.735 for 11.734 (sgt1935-sgt1939); 1936 applications 6.711 for 7.350 in sgt1936 (sgt1939 prints "
        "7.350) and placements 3.601 for 3.600 (both editions); 1939 offers 2.688 for 2.698; and the totals of the "
        "lines replaced from an earlier printing (failures computed on the cells as printed).",
}


# ----------------------------------------------------------------- survey

SURVEY = {
    "sgt1925": "f513 chapter XIV title (Travail et prévoyance sociale); f514 blank; f515 accidents du travail a) "
               "répartition d'après la nationalité des victimes, b) répartition d'après la gravité; f516|f517 c) "
               "causes matérielles par catégorie professionnelle; grèves survenues en Tunisie de 1916 à 1925; f518 "
               "Crédit mutuel agricole (1916-1925) a) caisses locales françaises et indigènes ...; f519 Coopérative "
               "centrale des agriculteurs (1916-1925); f520|f521 Assurances mutuelles agricoles (1916-1925); f522|f523 "
               "Sociétés indigènes de prévoyance, opérations (1916-1925) - f518-f523: see mutuality_* "
               "(extract_mutuality.py); f524 blank; f525-f539 table alphabétique of the volume; f541 front matter of "
               "sgt1926 (same volume).",
    "sgt1926": "f1037 chapter XV title; f1038 blank; f1039 accidents a) nationalité, b) gravité; f1040|f1041 c) "
               "causes matérielles, grèves a) état détaillé des grèves; f1042|f1043 b) grèves survenues de 1917 à "
               "1926, placement: opérations de l'Office de Placement Français en Tunisie (1920-1926); f1044 coût de "
               "la vie, nombres-indices 1915-1926; f1045-f1059 table alphabétique; f1060-f1061 blank (end of volume).",
    "sgt1927": "f501 chapter XV title; f502 blank; f503 habitations à bon marché a) logements construits (1912-1927), "
               "b) subventions de l'Etat et capitaux investis; f504 accidents a) nationalité (new categories); f505 "
               "b) suites connues ou probables; f506|f507 c) causes matérielles (new causes), grèves a) état "
               "détaillé; f508|f509 b) grèves survenues de 1918 à 1927, placement (1921-1927); f510 coût de la vie "
               "1915-1927; f511+ table alphabétique; the volume continues with sgt1928.",
    "sgt1928": "f1031 chapter XV title; f1032 blank; f1033 HBM a) and b) (1912-1928); f1034 accidents a); f1035 b); "
               "f1036|f1037 c), grèves a); f1038|f1039 grèves b) 1919-1928, placement 1920-1928; f1040 coût de la vie "
               "1919-1928; f1041+ table alphabétique.",
    "sgt1929": "f509 chapter XV title; f510 blank; f511 HBM a) and b) (1912-1929); f512 accidents a); f513 b); "
               "f514|f515 c), grèves a) état détaillé des grèves survenues en 1929; f516|f517 grèves b) 1920-1929, "
               "placement 1920-1929; f518 coût de la vie 1920-1929; f519+ table alphabétique.",
    "sgt1930": "f1045 chapter XV title; f1046 blank; f1047 HBM a) (with the list of projects under award) and b) "
               "(1912-1930); f1048 accidents a); f1049 b); f1050|f1051 c), grèves a) 1930; f1052|f1053 grèves b) "
               "1921-1930, placement 1921-1930; f1054 coût de la vie 1924-1930; f1055-f1071 table alphabétique "
               "(end of volume).",
    "sgt1935": "f319 chapter XVI title; f320 blank; f321 HBM a) and b) (headed 1912-1935, lines to 1934); f322 "
               "accidents a); f323 b); f324|f325 c) causes des accidents survenues en 1935, grèves a) 1935; "
               "f326|f327 grèves b) 1926-1935, placement 1926-1935; f328 coût de la vie 1931-1935; f329-f338 table "
               "alphabétique; f339-f340 blank (end of volume).",
    "sgt1936": "f182-f186 chapter XIV Mutualité agricole (not this chapter); f187 blank; f188 chapter XV title; f189 "
               "HBM logements construits (1912-1936; lines to 1934) and b) subventions et capitaux; f190 accidents, "
               "répartition d'après la nationalité (1): totals only; f191|f192 causes matérielles des accidents "
               "(1935); f193|f194 grèves survenues de 1927 à 1936, placement 1927-1936; f195 coût de la vie "
               "1932-1936; f196-f197 blank; f198-f210 tables analytique and alphabétique; f211-f212 end of volume.",
    "sgt1939": "f163 chapter XV title; f164 blank; f165 HBM logements construits (1912-1939; no subsidy table); "
               "f166 accidents, nationalité; f167 suites; f168|f169 causes matérielles; f170|f171 grèves survenues de "
               "1930 à 1939, placement 1930-1939; f172 liste des conventions collectives rendues obligatoires en "
               "1939; f173 sentences arbitrales ou accords rendus obligatoires en 1939; f174 immigration des "
               "travailleurs: contrats de travail visés en 1939, répartition des visas accordés; f175 coût de la vie "
               "1935-1939; f176-f188 tables analytique and alphabétique; f189-f190 end of volume.",
}

NOT_DONE = ("Every labour table of the chapter is transcribed in every edition that prints it, every cell read on "
            "native-resolution crops of the page images (whole-page views of every page from the chapter title to "
            "the index, then zoomed crops of every table and of every cell behind a failed check). Printed "
            "TOTAUX / TOTAL lines are used as checks only. The four agricultural mutual-credit tables printed in "
            "sgt1925's chapter (f518-f523: Crédit mutuel agricole, Coopérative centrale des agriculteurs, "
            "Assurances mutuelles agricoles, Sociétés indigènes de prévoyance, 1916-1925) are transcribed with the "
            "mutual-credit chapter: see mutuality_* (extract_mutuality.py).")


def write_survey(res):
    L = ["# Labour and social welfare chapter: survey of every edition", "",
         "Survey of the *Travail et prévoyance sociale* chapter (XIV in sgt1925, XV in sgt1926-sgt1930 and "
         "sgt1936-sgt1939, XVI in sgt1935). First and last views confirmed on the images (chapter-title page; the "
         "index or the end of the volume after the last table). Extraction: `extract_labour.py`. Up to sgt1924 the "
         "labour tables are in the economic-institutions chapter (`labour_early_*`).", "",
         "| edition | ark | chapter views | assigned range |", "|---|---|---|---|"]
    assigned = {"sgt1925": "513–564", "sgt1926": "1037–1061", "sgt1927": "501–552", "sgt1928": "1031–1057",
                "sgt1929": "509–558", "sgt1930": "1045–1071", "sgt1935": "319–340", "sgt1936": "188–212",
                "sgt1939": "163–190"}
    L += [f"| {e} | `{EDITIONS[e]}` | {a}–{b} | {assigned[e]} (the rest is the index, blank pages or the next "
          f"edition's front matter) |" for e, (a, b) in CHAPTER_VIEWS.items()]
    L += ["", "## Views per edition", ""] + [f"- **{e}**: {t}" for e, t in SURVEY.items()]
    L += ["", "## Tables (CSV)", "", "| CSV | sections | editions | read on the image |", "|---|---|---|---|"]
    for o, d in res.items():
        L.append(f"| `{o}` | {', '.join((TABLES.get(o) or TEXT_TABLES[o])['secs'])} | {', '.join(d['editions'])} "
                 f"| every printing, cell by cell |")
    L += ["", "## Coverage", "", NOT_DONE, ""]
    (OUT / "labour_survey.md").write_text("\n".join(L) + "\n")


# ----------------------------------------------------------------- build

def build(write=True):
    secs = []
    for ed in EDS:
        p = TR / f"{PREFIX}_{ed}.txt"
        if p.exists():
            secs += parse(p, ed)
    for s in secs:
        if s["cols"]:
            apply_derive(s)
        f = CHECKERS.get(s["table"])
        if f:
            f(s)
    chk_strike_details(secs)
    chk_visas_total(secs)
    res = {}
    for out, spec in TABLES.items():
        ss = [s for s in secs if s["table"] in spec["secs"]]
        eds = [e for e in ORDER if any(s["ed"] == e for s in ss)]
        recs = []
        for s in ss:
            recs += spec["cells"](s)
        if spec.get("periods"):
            kept, n, diffs = select_periods(recs, spec["periods"])
        else:
            kept, n, diffs = select(recs, spec["key"])
        order = {id(r): i for i, r in enumerate(recs)}
        kept.sort(key=lambda r: (r["year"], ORDER.index(r["census"]), order.get(id(r), 0)))
        for r in kept:
            r.pop("_prefer", None)
        flagged = [f"{r['census']} {r['year']} " + " / ".join(str(r.get(k, "")) for k in spec["dims"][:4])
                   + f" = {fmt_val(r['value'])} ({r['flag']})" for r in kept if r["flag"]]
        res[out] = dict(rows=len(kept), checks=CHK.n[out], failed=list(CHK.fail[out]), overlap_compared=n,
                        overlap_diffs=[list(x) for x in diffs], flagged=flagged, editions=eds)
        if write:
            cols = COMMON + spec["dims"] + ["value", "flag"]
            expl = []
            if CHK.fail[out]:
                expl = ["Every failed check below was re-read on a zoomed native-resolution crop (or recurs "
                        "unchanged in independent readings of several editions): printed values are kept. "
                        + FAIL_NOTES.get(out, "")]
            paras = list(spec.get("paras", [])) + expl + [
                "Survey of the whole chapter in every edition: `labour_survey.md`."]
            rule = RULEP if spec.get("periods") else (RULE5 if spec.get("rule5") else RULE4)
            write_csv(out, cols, kept)
            write_notes(out, CHAPTER, SCRIPT, kept, cols, {c: DOC[c] for c in cols}, spec["title_fr"],
                        spec["title_en"], paras, CHK.n[out], CHK.fail[out], n, diffs, coverage_lines(ss), rule,
                        spec["unit"])
    ag = [s for s in secs if s["table"] in TEXT_TABLES["labour_collective_agreements"]["secs"]]
    res["labour_collective_agreements"] = dict(rows=sum(len(s["rows"]) for s in ag), checks=0, failed=[],
                                               overlap_compared=0, overlap_diffs=[], flagged=[],
                                               editions=sorted({s["ed"] for s in ag}))
    if write:
        write_agreements(ag)
        write_validation(OUT / f"{PREFIX}_validation.json", dict(
            res, _chapter_views=CHAPTER_VIEWS, _survey=SURVEY, _not_transcribed=NOT_DONE))
        write_survey(res)
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
