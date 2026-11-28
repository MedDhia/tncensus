#!/usr/bin/env python3
"""Colonisation chapter (*Colonisation*: chapter XIII, XIV in sgt1935) of the Statistique générale de la Tunisie,
12 editions sgt1922-sgt1939.

  python3 extract_colonisation.py check   parse the transcriptions, run every check, print failures
  python3 extract_colonisation.py build   ... and write csv/colonisation_*.csv, their .md notes,
                                          csv/colonisation_survey.md and csv/colonisation_validation.json

Source of truth: transcribed/colonisation_<edition>.txt (format in yb_tables.py; labels holding ';;' carry the
printed text fields of a line, split here). The colonisation fund is a yearly series reprinted in every edition
sgt1922-sgt1928 (SPEC_ADDENDUM rule 4). The lists of lotissements are printed by each edition for a ten-year
window, with lot counts and areas as known at the edition date (they are revised between editions): every edition
is kept (rule 5, `census` = edition).
"""
import sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # shared helper yb_tables.py
import yb_tables
from yb_tables import (COMMON, EDITIONS, ORDER, OUT, TR, Checks, coverage_lines, parse, select_latest, ssum,
                       where, write_csv, write_notes, write_validation)

CHAPTER = "Colonisation"
SCRIPT = "extract_colonisation.py"
PREFIX = "colonisation"
CHK = Checks()

CHAPTER_VIEWS = {}   # filled below (SURVEY section)


class PCell(yb_tables.Cell):
    """yb_tables cell tokens plus two binding cases (sgt1935 and later, superficie column in the gutter):
    'value~' = hectares legible, ares lost in the fold: value taken from the printing of the edition named by the
    section's `fill=` (checked in fill_check), flag reprint_corrected; 'value#' = a figure partly lost, solved from the printed totals (flag derived_from_totals); 'NNN^' = a printed total of which only the
    hectares are legible (checked on the hectares)."""
    __slots__ = ("cut",)

    def __init__(self, raw):
        self.cut = ""
        if raw.endswith("~"):
            super().__init__(raw[:-1])
            self.raw, self.flag, self.cut = raw, "reprint_corrected", "fill"
        elif raw.endswith("#"):
            super().__init__(raw[:-1])
            self.raw, self.flag = raw, "derived_from_totals"
        elif raw.endswith("^"):
            super().__init__(raw[:-1])
            self.raw, self.flag, self.cut = raw, "illegible", "hectares"
        else:
            super().__init__(raw)


yb_tables.Cell = PCell   # parse() builds its cells through the module-level name


def split(label):
    return [t.strip() for t in label.split(";;")]


def base(sec, year, view=None, page=None):
    return {"census": sec["ed"], "table_id": sec["table"], "gallica_ark": sec["ark"],
            "source_page": page or sec["page"], "gallica_view": view or sec["view"], "year": year}


def data_rows(sec, skip=("TOTAL", "grand", "Totaux", "TOTAUX", "report", "reporter")):
    return [r for r in sec["rows"] if "cells" in r and r["label"].split(";;")[0].strip() not in skip]


def row(sec, label):
    for r in sec["rows"]:
        if r["label"] == label:
            return r["cells"]
    return None


# ----------------------------------------------------------------- colonisation fund (rule 4)

FUND_M = {"dot": ("endowment", "Dotations : montant", "francs"),
          "rec": ("receipts", "Recettes annuelles", "francs"),
          "dep": ("expenditure", "Dépenses annuelles", "francs"),
          "ha": ("area_acquired", "Superficie des immeubles acquis sur le fonds de colonisation (en hectares)",
                 "hectares")}


def cells_fund(sec):
    out = []
    for r in data_rows(sec):
        year, origin = split(r["label"])
        for c in sec["cols"]:
            m, mfr, unit = FUND_M[c]
            cell = r["cells"][c]
            out.append(dict(base(sec, int(year), *((int(sec["view2"]), int(sec["page2"])) if c in ("dep", "ha")
                                                  else (None, None))),
                            measure=m, measure_fr=mfr, unit=unit,
                            endowment_origin_fr=origin if c == "dot" else "", value=cell.value, flag=cell.flag))
    return out


def chk_fund(sec):
    out = "colonisation_fund"
    t = row(sec, "TOTAL")
    for c in sec["cols"]:
        CHK.eq(out, f"{where(sec)} {c}: TOTAL = sum of the years", ssum(r["cells"][c].value for r in data_rows(sec)),
               t[c].value)
    g = row(sec, "grand")
    CHK.eq(out, f"{where(sec)} dotations + recettes = printed grand total", t["dot"].value + t["rec"].value,
           g["dot"].value)


# ----------------------------------------------------------------- lists of lotissements (rule 5)

LOT_M = {"area": ("area", "Superficie du lotissement", "hectares"),
         "created": ("lots_created", "Nombre de lots créés", "count"),
         "reserved": ("lots_reserved_or_available", "Nombre de lots réservés ou disponibles", "count"),
         "sold": ("lots_sold", "Nombre de lots vendus", "count"),
         "rural": ("lots_rural", "Nombre de lots ruraux", "count"),
         "market": ("lots_market_garden", "Nombre de lots maraîchers", "count"),
         "suburban": ("lots_suburban", "Nombre de lots suburbains", "count"),
         "artisan": ("lots_artisan", "Nombre de lots d'artisans", "count"),
         "lots": ("lots", "Nombre de lots", "count")}
CARRY = ("report", "reporter", "Totaux")


def cells_list(sec):
    """one line = one lotissement; sgt1922-sgt1923 labels carry nature too"""
    out = []
    last_nature = ""
    for r in sec["rows"]:
        if "cells" not in r or r["label"] in CARRY:
            continue
        f = split(r["label"])
        origin = ""
        if sec["table"] == "install22":
            year, name, nature, situation, cc, obs = f
            if nature in ("—", "-"):
                nature = last_nature
            last_nature = nature
        elif sec["table"].endswith("35"):
            year, name, origin, situation, cc, obs = f
            nature = ""
        else:
            year, name, situation, cc, obs = f
            nature = ""
        for c in sec["cols"]:
            if c == "total":
                continue          # printed line total: check only
            m, mfr, unit = LOT_M[c]
            cell = r["cells"][c]
            flag = cell.flag
            if f"{name}:{c}" in sec.get("mismatch", "").split(","):
                flag = "total_mismatch"
            right = c != "area" or sec["table"] == "install22"
            vw, pg = (int(sec["view2"]), int(sec["page2"])) if right and sec.get("view2") else (None, None)
            out.append(dict(base(sec, int(year[:4]), vw, pg), year_label=year, scheme=SCHEME[sec["table"]][0], scheme_fr=SCHEME[sec["table"]][1],
                            property_fr=name, origin_fr=origin, nature_fr=nature, situation_fr=situation, controle_civil=cc,
                            observation_fr=obs, measure=m, measure_fr=mfr, unit=unit, value=cell.value,
                            flag=flag))
    return out


SCHEME = {"install22": ("installation", "Ventes avec obligation d'installation : a) Propriétés livrées à la "
                                        "colonisation"),
          "install": ("installation", "a) Ventes avec obligation d'installation personnelle"),
          "install35": ("installation", "a) Ventes avec obligation d'installation personnelle"),
          "planting": ("planting", "b) Terres à planter (Ventes avec obligation d'installation dans la Régence)"),
          "urban": ("urban_industrial_summer", "c) Lotissements urbains, industriels ou d'estivage")}


LAST_CARRY = {}


def chk_list(sec, out):
    """carried totals ('A reporter' / 'Reports' / 'Totaux' = report + lines; a 'Reports' line = the previous page's
    'A reporter', which is the figure carried), line totals, and in the sgt1922-sgt1923 layout the identity
    créés = réservés ou disponibles + vendus"""
    acc, lines = None, []
    key = (sec["ed"], sec["table"])
    for r in sec["rows"]:
        if "cells" not in r:
            continue
        c = r["cells"]
        if r["label"] == "report":
            acc = {k: c[k].value for k in sec["cols"]}
            prev = LAST_CARRY.get(key)
            if prev:
                for k in sec["cols"]:
                    cmpv = prev[k] if c[k].cut != "hectares" else Decimal(int(prev[k]))
                    CHK.eq(out, f"{where(sec)} {k}: Reports = previous page's A reporter", cmpv, c[k].value)
                acc = dict(prev)
            continue
        if r["label"] in ("reporter", "Totaux"):
            carry = {}
            for k in sec["cols"]:
                got = ssum([acc[k] if acc else Decimal(0)] + [x["cells"][k].value or Decimal(0) for x in lines])
                carry[k] = got
                if c[k].value is None:
                    continue
                if c[k].cut == "hectares":
                    CHK.eq(out, f"{where(sec)} {k}: {r['label']} (hectares legible) = report + lines",
                           Decimal(int(got)), c[k].value)
                else:
                    CHK.eq(out, f"{where(sec)} {k}: {r['label']} = report + lines", got, c[k].value)
                    carry[k] = c[k].value
            if r["label"] == "reporter":
                LAST_CARRY[key] = carry
            continue
        lines.append(r)
        name = split(r["label"])[1]
        if "total" in sec["cols"]:
            parts = [c[k].value for k in sec["cols"] if k not in ("area", "total")]
            if all(x is not None for x in parts):
                CHK.eq(out, f"{where(sec)} {name}: TOTAUX = sum of the lot types", ssum(parts), c["total"].value)
        if sec["table"] == "install22" and c["reserved"].value is not None and c["sold"].value is not None:
            CHK.eq(out, f"{where(sec)} {name}: créés = réservés ou disponibles + vendus",
                   c["reserved"].value + c["sold"].value, c["created"].value)


RECAP_C = {"dom": ("domaines", "Domaines", "area", "hectares"),
           "hab": ("habous", "Habous publics et privés", "area", "hectares"),
           "ach": ("purchase_fund", "Achat sur le fonds de colonisation", "area", "hectares"),
           "sial": ("sialine_lands", "Terres sialines", "area", "hectares"),
           "rural": ("", "Nombre de lots : ruraux", "lots_rural", "count"),
           "small": ("", "Nombre de lots : petite culture", "lots_small_farming", "count"),
           "lots": ("", "Nombre de lots", "lots", "count")}
RECAP_T = {"recap_rural": ("rural", "a) Lotissements ruraux livrés à la Colonisation"),
           "recap_plant": ("planting", "b) Lotissements de terres à planter")}


def period_code(label, split):
    if label.startswith("Antérieure"):
        return f"before_{split}"
    if label.startswith("Achats pour recasements"):
        return "resettlement_purchases_memo"
    return f"from_{split}"


def cells_recap(sec):
    out = []
    kind, kind_fr = RECAP_T[sec["table"]]
    for r in sec["rows"]:
        if "cells" not in r or r["label"] == "Totaux":
            continue
        for c in sec["cols"]:
            if c in ("tot", "lotstot"):
                continue
            o, ofr, m, unit = RECAP_C[c]
            cell = r["cells"][c]
            out.append(dict(base(sec, int(sec["year"]) if sec.get("year") else ED_YEAR[sec["ed"]]),
                            lotissement=kind, lotissement_fr=kind_fr, period=period_code(r["label"], sec["split"]),
                            period_fr=r["label"], origin=o, origin_fr=ofr if o else "", measure=m,
                            measure_fr=ofr if not o else "Origine du lotissement (superficie)", unit=unit,
                            value=cell.value, flag=cell.flag))
    return out


ED_YEAR = {e: int(e[3:]) for e in EDITIONS}


def chk_recap(sec):
    out = "colonisation_lotissements_summary"
    area = [c for c in sec["cols"] if c in ("dom", "hab", "ach", "sial")]
    lots = [c for c in sec["cols"] if c in ("rural", "small")]
    for r in sec["rows"]:
        if "cells" not in r:
            continue
        c = r["cells"]
        CHK.eq(out, f"{where(sec)} {r['label']}: TOTAUX (area) = sum of origins", ssum(c[k].value for k in area),
               c["tot"].value)
        if lots:
            CHK.eq(out, f"{where(sec)} {r['label']}: TOTAUX (lots) = ruraux + petite culture",
                   ssum(c[k].value for k in lots), c["lotstot"].value)
    t = row(sec, "Totaux")
    parts = [r for r in sec["rows"] if "cells" in r and r["label"] != "Totaux" and
             not r["label"].startswith("Achats pour")]
    for k in sec["cols"]:
        CHK.eq(out, f"{where(sec)} {k}: Totaux = the two periods", ssum(r["cells"][k].value for r in parts),
               t[k].value)


FIX_M = {"families": ("families_settled", "Nombre de familles installées", "count"),
         "cultivated": ("land_cultivation_allotted", "Terres de culture (de plantation et de cultures) attribuées",
                        "hectares"),
         "grazing": ("land_grazing", "Terres de parcours", "hectares"),
         "attrib": ("allotments", "Nombre d'attributions", "count"),
         "lots": ("lots", "Nombre de lots", "count"),
         "area": ("area", "Superficie", "hectares"),
         "proposed": ("sales_proposed", "Ventes proposées aux attributaires", "count"),
         "sold": ("sales_realised", "Ventes réalisées : nombre", "count")}
SALES_AREA = ("sales_realised_area", "Ventes réalisées : superficie", "hectares")


def cells_fixation(sec):
    out = []
    for r in sec["rows"]:
        if "cells" not in r or r["label"] == "Totaux":
            continue
        f = split(r["label"])
        label, obs = f[0], (f[1] if len(f) > 1 else "")
        if sec["table"] == "fixation_years":
            year, item, item_fr = int(label), "allotments_of_year", "Fixation des Tunisiens au sol (année)"
        elif sec["table"] == "sales":
            year, item, item_fr = int(label[:4]), "definitive_sales", ("Ventes définitives consenties aux "
                                                                       "attributaires")
        else:
            year, item, item_fr = ED_YEAR[sec["ed"]], "cumulative", label if sec["table"] == "fixation" else \
                f"Période de {sec['period']}"
        for c in sec["cols"]:
            m, mfr, unit = SALES_AREA if (sec["table"] == "sales" and c == "area") else FIX_M[c]
            cell = r["cells"][c]
            out.append(dict(base(sec, year), year_label=label, item=item, item_fr=item_fr, observation_fr=obs,
                            measure=m, measure_fr=mfr, unit=unit, value=cell.value, flag=cell.flag))
    return out


def chk_fixation(sec, out):
    t = row(sec, "Totaux")
    if t is None:
        return
    lines = [r for r in sec["rows"] if "cells" in r and r["label"] != "Totaux"]
    for k in sec["cols"]:
        CHK.eq(out, f"{where(sec)} {k}: Totaux = sum of the lines", ssum(r["cells"][k].value for r in lines),
               t[k].value)


REG_M = {"taken": ("lots_taken_back", "Nombre de lots repris", "count"),
         "colons": ("settlers_reinstalled", "Colons réinstallés", "count"),
         "diff": ("difference", "Différence", "count"),
         "area": ("area", "Superficie", "hectares")}


def cells_regroup(sec):
    out = []
    op = ("regrouping", "Opérations de regroupement réalisées au 31 décembre 1935") if sec["table"] == "regroup" \
        else ("reinstallation_domain_purchases", "Réinstallations effectuées sur des propriétés achetées par le "
                                                 "Domaine")
    for r in sec["rows"]:
        if "cells" not in r or r["label"] in CARRY:
            continue
        for c in sec["cols"]:
            cell = r["cells"][c]
            if r["label"] == "TOTAL (printed)" and cell.value is None:
                continue
            m, mfr, unit = REG_M[c]
            out.append(dict(base(sec, 1935), operation=op[0], operation_fr=op[1], lotissement_fr=r["label"],
                            measure=m, measure_fr=mfr, unit=unit, value=cell.value,
                            flag="" if r["label"] == "TOTAL (printed)" else cell.flag))
    return out


def chk_regroup(sec):
    out = "colonisation_regrouping_1935"
    for r in sec["rows"]:
        if "cells" in r and r["label"] not in ("TOTAL (printed)",) and sec["table"] == "regroup":
            c = r["cells"]
            CHK.eq(out, f"{where(sec)} {r['label']}: différence = lots repris - colons réinstallés",
                   c["taken"].value - c["colons"].value, c["diff"].value)
    sub = dict(sec, rows=[r for r in sec["rows"] if r["label"] != "TOTAL (printed)"])
    chk_list(sub, out) if False else None
    acc = None
    lines = []
    for r in sub["rows"]:
        if "cells" not in r:
            continue
        if r["label"] == "report":
            acc = LAST_CARRY.get((sec["ed"], "regroup"))
            for k in sec["cols"]:
                CHK.eq(out, f"{where(sec)} {k}: Report = A reporter", acc[k], r["cells"][k].value)
            continue
        if r["label"] in ("reporter", "Totaux"):
            for k in sec["cols"]:
                if r["cells"][k].value is None:
                    continue
                got = ssum([acc[k] if acc else Decimal(0)] + [x["cells"][k].value for x in lines])
                CHK.eq(out, f"{where(sec)} {k}: {r['label']} = sum", got, r["cells"][k].value)
            if r["label"] == "reporter":
                LAST_CARRY[(sec["ed"], "regroup")] = {k: r["cells"][k].value for k in sec["cols"]}
            continue
        lines.append(r)


FILLED = []


def fill_check(secs):
    """every 'value~' cell must equal a value printed for the same year and column by the `fill=` edition"""
    for s in secs:
        if not s.get("fill"):
            continue
        other = [o for o in secs if o["ed"] == s["fill"] and o["table"].rstrip("35").rstrip("22") ==
                 s["table"].rstrip("35").rstrip("22")]
        for r in s["rows"]:
            if "cells" not in r:
                continue
            for k, c in r["cells"].items():
                if c.cut != "fill":
                    continue
                year = split(r["label"])[0]
                ok = any(split(x["label"])[0] == year and x["cells"][k].value == c.value
                         for o in other for x in o["rows"] if "cells" in x)
                FILLED.append(f"{s['ed']} f{s['view']} {year} {split(r['label'])[1]}: {k} {c.value} from "
                              f"{s['fill']}" + ("" if ok else " (NOT FOUND)"))
                if not ok:
                    raise ValueError(f"fill value not printed by {s['fill']}: {where(s)} {r['label']} {c.raw}")


# ----------------------------------------------------------------- old-layout tables (sgt1922-sgt1923, second pass)

LOT_TYPE = {"culture": ("culture", "Lots de culture"), "suburban": ("suburban", "Lots suburbains"),
            "urban": ("urban_industrial", "Lots urbains ou industriels")}
LAND_ORIGIN = {"domanial": ("state_domain", "Patrimoine domanial"),
               "fund": ("purchase_fund", "Achats sur le fonds de colonisation"),
               "all": ("all", "")}
RECAP_OLD_M = {"area": ("area", "Superficie totale", "hectares"),
               "created": ("lots_created", "Nombre de lots créés", "count"),
               "reserved": ("lots_reserved_or_available", "Nombre de lots réservés ou disponibles en cours de vente",
                            "count"),
               "sold": ("lots_sold", "Nombre de lots vendus", "count")}
NAT = {"fr": ("french", "Français"), "eu": ("other_european", "Autres Européens"), "ind": ("indigenous", "Indigènes")}
PLANT_OP = {"plant_auth": ("planting_authorisation", "Autorisations de planter"),
            "plant_sale": ("definitive_sale", "Ventes définitives"),
            "a": ("planting_authorisation", "Autorisations de planter"), "s": ("definitive_sale", "Ventes définitives")}
PLANT_M = {("planting_authorisation", "n"): ("concessions", "Nombre de concessions délivrées", "count"),
           ("planting_authorisation", "ha"): ("area", "Superficies concédées (en hectares)", "hectares"),
           ("definitive_sale", "n"): ("sales", "Nombre de ventes", "count"),
           ("definitive_sale", "ha"): ("area", "Superficies vendues (en hectares)", "hectares")}
CLAUSE = {"s": ("without_colonisation_clause", "Substitutions consenties sans clause de colonisation"),
          "c": ("with_colonisation_clause", "Substitutions consenties avec clause de colonisation")}
SUB_M = {"n": ("properties_ceded", "Nombre d'immeubles cédés", "count"),
         "ha": ("area", "Superficie globale (en hectares)", "hectares"),
         "land": ("land_value", "Valeur foncière des immeubles", "francs"),
         "build": ("buildings_value", "Valeur des constructions édifiées", "francs")}
BUYER = {"f": ("french", "Français"), "o": ("other_european_and_indigenous", "Autres Européens et indigènes")}
HABOUS = {"pub": ("public", "Habous publics"), "priv": ("private", "Habous privés")}
ENZ_M = {"n": ("cessions", "Nombre de cessions consenties", "count"),
         "rent": ("enzel_rent", "Montant global des rentes d'enzel", "francs"),
         "cap": ("capital", "Montant global du capital", "francs")}


def where_printed(sec, col):
    """(view, page) of the page that prints a column of an old-layout spread (None, None = the section's view)"""
    t = sec["table"]
    if not sec.get("view2"):
        return None, None
    left = {"soldcc": ("cult_n", "cult_ha"), "plant_cc": tuple(f"a_{n}_{m}" for n in NAT for m in ("n", "ha")),
            "enzel_cc": tuple(f"f{h}_{m}" for h in HABOUS for m in ENZ_M)}.get(t, ())
    if col in left:
        return None, None
    return int(sec["view2"]), int(sec["page2"])


def period_of(sec):
    return sec.get("years", "")


def cells_old_recap(sec):
    out = []
    for r in sec["rows"]:
        if "cells" not in r or r["label"].startswith("TOTAL"):
            continue
        org, lt = split(r["label"])
        for c in sec["cols"]:
            m, mfr, unit = RECAP_OLD_M[c]
            cell = r["cells"][c]
            out.append(dict(base(sec, ED_YEAR[sec["ed"]], *where_printed(sec, c)), period_fr=period_of(sec),
                            origin=LAND_ORIGIN[org][0],
                            origin_fr=LAND_ORIGIN[org][1], lot_type=LOT_TYPE[lt][0], lot_type_fr=LOT_TYPE[lt][1],
                            measure=m, measure_fr=mfr, unit=unit, value=cell.value, flag=cell.flag))
    return out


def chk_old_recap(sec):
    out = "colonisation_lands_delivered_summary"
    acc, groups = [], {}
    for r in sec["rows"]:
        if "cells" not in r:
            continue
        c = r["cells"]
        org, lt = split(r["label"])
        if org == "TOTAL":
            if lt == "general":
                parts = list(groups.values()) if groups else [x["cells"] for x in acc]
                for k in sec["cols"]:
                    CHK.eq(out, f"{where(sec)} {k}: TOTAL GÉNÉRAL = sum", ssum(x[k].value for x in parts),
                           c[k].value)
            else:
                for k in sec["cols"]:
                    CHK.eq(out, f"{where(sec)} {k}: TOTAL {lt} = sum of its lines",
                           ssum(x["cells"][k].value for x in acc), c[k].value)
                groups[lt] = c
                acc = []
            continue
        acc.append(r)
        if "reserved" in c:
            CHK.eq(out, f"{where(sec)} {r['label']}: créés = réservés ou disponibles + vendus",
                   c["reserved"].value + c["sold"].value, c["created"].value)


def cells_soldcc(sec):
    out = []
    for r in sec["rows"]:
        if "cells" not in r or r["label"] == "TOTAL":
            continue
        for c in sec["cols"]:
            if c.startswith("tot"):
                continue
            kind, meas = c.split("_")
            lt = {"cult": "culture", "sub": "suburban", "urb": "urban"}[kind]
            m = ("lots_sold", "Nombre de lots vendus", "count") if meas == "n" else ("area", "Superficie", "hectares")
            cell = r["cells"][c]
            out.append(dict(base(sec, ED_YEAR[sec["ed"]], *where_printed(sec, c)), period_fr=period_of(sec),
                            controle_civil=r["label"], lot_type=LOT_TYPE[lt][0], lot_type_fr=LOT_TYPE[lt][1] if lt != "urban" else
                            "Lots urbains et industriels", measure=m[0], measure_fr=m[1], unit=m[2],
                            value=cell.value, flag=cell.flag))
    return out


def row_totals(sec, out, groups):
    """groups: {total column: [part columns]} checked on every line (data and TOTAL)"""
    for r in sec["rows"]:
        if "cells" not in r:
            continue
        c = r["cells"]
        for t, parts in groups.items():
            CHK.eq(out, f"{where(sec)} {r['label'].replace(' ;; ', ' / ')}: {t} = {' + '.join(parts)}",
                   ssum(c[p].value for p in parts), c[t].value)


def col_totals(sec, out):
    t = row(sec, "TOTAL")
    lines = [r for r in sec["rows"] if "cells" in r and r["label"] != "TOTAL"]
    for k in sec["cols"]:
        CHK.eq(out, f"{where(sec)} {k}: TOTAL = sum of the lines", ssum(r["cells"][k].value for r in lines),
               t[k].value)


def cells_plant_list(sec):
    out = []
    op, opfr = PLANT_OP[sec["table"]]
    realign = {x.split(":")[0]: x.split(":")[1] for x in sec.get("realign", "").split(",") if x}
    last_cc = ""
    for r in sec["rows"]:
        if "cells" not in r:
            continue
        year, prop, cc = split(r["label"])
        note = ""
        if cc in ("—", "-"):
            cc = last_cc
        if prop == "»":
            prop, cc, note = "", "", "néant"
        last_cc = cc
        for c in sec["cols"]:
            if c.startswith("tot"):
                continue
            nat, meas = c.split("_")
            m, mfr, unit = PLANT_M[(op, meas)]
            cell = r["cells"][c]
            flag = cell.flag
            if realign.get(f"{year};;{prop}") == c:
                flag = "row_realigned"
            out.append(dict(base(sec, int(year), *where_printed(sec, c)), operation=op, operation_fr=opfr, property_fr=prop,
                            controle_civil=cc, note_fr=note, nationality=NAT[nat][0], nationality_fr=NAT[nat][1],
                            measure=m, measure_fr=mfr, unit=unit, value=cell.value, flag=flag))
    return out


def cells_plant_cc(sec):
    out = []
    for r in sec["rows"]:
        if "cells" not in r or r["label"] == "TOTAL":
            continue
        for c in sec["cols"]:
            o, nat, meas = c.split("_")
            if nat == "tot":
                continue
            op, opfr = PLANT_OP[o]
            m, mfr, unit = PLANT_M[(op, meas)]
            cell = r["cells"][c]
            out.append(dict(base(sec, ED_YEAR[sec["ed"]], *where_printed(sec, c)), period_fr=period_of(sec),
                            controle_civil=r["label"], operation=op, operation_fr=opfr, nationality=NAT[nat][0], nationality_fr=NAT[nat][1],
                            measure=m, measure_fr=mfr, unit=unit, value=cell.value, flag=cell.flag))
    return out


def cells_hab_sub(sec):
    out = []
    by_cc = sec["table"].endswith("_cc")
    for r in sec["rows"]:
        if "cells" not in r or r["label"] == "TOTAL":
            continue
        for c in sec["cols"]:
            cl, meas = c.split("_")
            if meas == "tot":
                continue
            m, mfr, unit = SUB_M[meas]
            cell = r["cells"][c]
            d = dict(base(sec, ED_YEAR[sec["ed"]] if by_cc else int(r["label"])), clause=CLAUSE[cl][0],
                     clause_fr=CLAUSE[cl][1], measure=m, measure_fr=mfr, unit=unit, value=cell.value, flag=cell.flag)
            if by_cc:
                d.update(period_fr=period_of(sec), controle_civil=r["label"])
            out.append(d)
    return out


def cells_enzel(sec):
    out = []
    by_cc = sec["table"].endswith("_cc")
    for r in sec["rows"]:
        if "cells" not in r or r["label"] == "TOTAL":
            continue
        for c in sec["cols"]:
            grp, meas = c.split("_")
            if grp == "tot":
                continue
            b, h = grp[0], grp[1:]
            m, mfr, unit = ENZ_M[meas]
            cell = r["cells"][c]
            d = dict(base(sec, ED_YEAR[sec["ed"]] if by_cc else int(r["label"]), *where_printed(sec, c)), buyer=BUYER[b][0],
                     buyer_fr=BUYER[b][1], habous=HABOUS[h][0], habous_fr=HABOUS[h][1], measure=m, measure_fr=mfr,
                     unit=unit, value=cell.value, flag=cell.flag)
            if by_cc:
                d.update(period_fr=period_of(sec), controle_civil=r["label"])
            out.append(d)
    return out


def chk_old(sec):
    t = sec["table"]
    if t in ("recap22", "recap23"):
        chk_old_recap(sec)
    elif t == "soldcc":
        out = "colonisation_lots_sold_by_controle"
        row_totals(sec, out, {"tot_n": ["cult_n", "sub_n", "urb_n"], "tot_ha": ["cult_ha", "sub_ha", "urb_ha"]})
        col_totals(sec, out)
    elif t in ("plant_auth", "plant_sale"):
        row_totals(sec, "colonisation_planting_concessions", {"tot_n": ["fr_n", "eu_n", "ind_n"],
                                                               "tot_ha": ["fr_ha", "eu_ha", "ind_ha"]})
    elif t == "plant_cc":
        out = "colonisation_planting_by_controle"
        row_totals(sec, out, {f"{o}_tot_{m}": [f"{o}_{n}_{m}" for n in NAT] for o in "as" for m in ("n", "ha")})
        col_totals(sec, out)
    elif t in ("hab_sub", "hab_sub_cc"):
        out = "colonisation_habous_substitutions" + ("_by_controle" if t.endswith("_cc") else "")
        row_totals(sec, out, {f"{c}_tot": [f"{c}_land", f"{c}_build"] for c in CLAUSE})
        if t.endswith("_cc"):
            col_totals(sec, out)
    elif t in ("enzel", "enzel_cc"):
        out = "colonisation_habous_enzel" + ("_by_controle" if t.endswith("_cc") else "")
        row_totals(sec, out, {f"tot_{m}": [f"{b}{h}_{m}" for b in BUYER for h in HABOUS] for m in ENZ_M})
        if t.endswith("_cc"):
            col_totals(sec, out)


OLD_SECS = ("recap22", "recap23", "soldcc", "plant_auth", "plant_sale", "plant_cc", "hab_sub", "hab_sub_cc",
            "enzel", "enzel_cc")

DOC_OLD = {
    "year": "year of the figures (yearly lists) or the edition year (cumulative recapitulations: state at the "
            "edition date, period in `period_fr`)",
    "period_fr": "period covered by the cumulative recapitulation, as printed in the title (e.g. `1893-1922`)",
    "origin": "origin of the land: `state_domain` (patrimoine domanial), `purchase_fund` (achats sur le fonds de "
              "colonisation), `all` (sgt1923: no split printed)",
    "origin_fr": "printed origin heading (empty for `all`)",
    "lot_type": "`culture` (lots de culture / de colonisation), `suburban`, `urban_industrial`",
    "lot_type_fr": "printed lot type",
    "controle_civil": "contrôle civil as printed (`Territ. milit.` = territoires militaires; a ditto '—' is "
                      "resolved to the line above; empty for a néant line)",
    "operation": "`planting_authorisation` (autorisations de planter) or `definitive_sale` (ventes définitives)",
    "operation_fr": "printed table heading",
    "property_fr": "nom de la propriété ou désignation des régions, as printed (`Extrême-Sud : Telmine` for the "
                   "braced 1919 line; empty for a néant line)",
    "note_fr": "`néant` when the year is printed with » in every cell",
    "nationality": "`french`, `other_european`, `indigenous` (concessionaires / buyers)",
    "nationality_fr": "printed column heading",
    "clause": "`without_colonisation_clause` / `with_colonisation_clause`",
    "clause_fr": "printed column heading",
    "buyer": "`french` or `other_european_and_indigenous` (printed groups)",
    "buyer_fr": "printed column heading",
    "habous": "`public` or `private` habous",
    "habous_fr": "printed column heading",
    "flag": "empty, or `row_realigned` (printed on the neighbouring line, stored on its own line)",
}

# ----------------------------------------------------------------- tables

DOC = {
    "census": "edition the value is taken from (rule 4 tables: the latest edition printing that year)",
    "table_id": "transcription section",
    "gallica_ark": "Gallica volume ark (views are numbered within a volume)",
    "source_page": "printed page number",
    "gallica_view": "Gallica view (fNNNN)",
    "year": "year of the figures",
    "measure": "measure code (English)",
    "measure_fr": "printed column heading",
    "unit": "unit of `value`",
    "year_label": "year as printed (brackets such as `1920-21` kept); `year` = its first year",
    "scheme": "`installation` (ventes avec obligation d'installation personnelle)",
    "scheme_fr": "printed table title",
    "property_fr": "property / lotissement as printed (footnote calls kept)",
    "origin_fr": "from sgt1935: printed origin code after the name (A., D., H.; e.g. `A. 500, D. 892`)",
    "nature_fr": "sgt1922-sgt1923 only: printed nature de l'immeuble ou du lotissement (ditto marks resolved)",
    "situation_fr": "printed situation",
    "controle_civil": "contrôle civil as printed",
    "observation_fr": "printed observation for the line (a brace covering several lines is repeated on each)",
    "item": "`cumulative` (state since 1920 at the edition date), `allotments_of_year`, `definitive_sales`",
    "item_fr": "printed line or table heading",
    "operation": "`regrouping` or `reinstallation_domain_purchases`",
    "operation_fr": "printed table title",
    "lotissement_fr": "lotissement / property as printed",
    "lotissement": "`rural` (a) lotissements ruraux) or `planting` (b) terres à planter)",
    "lotissement_fr": "printed table title",
    "period": "`before_YYYY`, `from_YYYY` (printed Postérieure à / Depuis YYYY), or the memo line",
    "period_fr": "printed period label",
    "origin": "origin of the land: `domaines`, `habous` (publics et privés), `purchase_fund` (achat sur le fonds de "
              "colonisation), `sialine_lands` (terres sialines); empty for lot counts",
    "origin_fr": "printed origin column heading",
    "endowment_origin_fr": "printed origin of the endowment (dotation lines only; » = ditto / none; footnote "
                           "calls kept)",
    "value": "printed value (» = 0)",
    "flag": "empty, or `illegible`, `not_applicable`, `total_mismatch`, `ocr_corrected`",
}

RULE4 = ("Printed for overlapping year windows: each year is taken from the **latest** edition that prints it "
         "(SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on its own page "
         "image, is compared below.")
RULE5 = ("Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept (`census` = edition); the figures "
         "are the state at the edition date and are revised between editions.")

TABLES = {
    "colonisation_installation_lots": dict(
        secs=["install22", "install", "install35"], cells=cells_list, key=["year", "property_fr", "measure"], rule5=True,
        dims=["scheme", "scheme_fr", "property_fr", "origin_fr", "nature_fr", "situation_fr", "controle_civil", "observation_fr",
              "measure", "measure_fr", "unit"],
        title_fr="Ventes avec obligation d'installation personnelle (propriétés livrées à la colonisation)",
        title_en="Sales with an obligation of personal settlement: lotissements delivered to colonisation, by year, "
                 "with area and number of lots",
        unit="Units: hectares (area, printed h. a.) and number of lots (`unit`); suggested value_type: mixed.",
        paras=["Printed in every edition for the ten years before the edition (sgt1939: 1929-1939). One row per "
               "printed figure of a lotissement line, with the property name, situation and contrôle civil as "
               "printed. Two layouts: sgt1922-sgt1923 (*Ventes avec obligation d'installation : a) Propriétés "
               "livrées à la colonisation*: nature, superficie totale, lots créés / réservés ou disponibles / vendus; "
               "urban, suburban and summer lotissements are in this list) and sgt1924-sgt1939 (*a) Ventes avec "
               "obligation d'installation personnelle*: superficie, lots ruraux / maraîchers / suburbains / "
               "d'artisans / totaux; urban lotissements in a separate table). The printed TOTAUX column of the "
               "second layout is a check only (not stored); A reporter / Reports / Totaux lines are checks only. "
               "From sgt1935 an origin code follows each name (A. = achat sur le fonds de colonisation, D. = "
               "domaines, H. = habous, by the headings of the recapitulation table; not explained on the page). "
               "sgt1939 drops the artisans column and prints TOTAUX before SUBURBAINS.",
               "The lists are revised from edition to edition (areas and lot counts of the same lotissement change; "
               "lots taken back, lines regrouped), so every edition is kept. A line printed in brace with two names "
               "(e.g. Henchir Chouichia / Aïn-el-Merdja, one area) is one row with both names.",
               "Binding: sgt1935 f294-f297 lose the ares of the area column in the gutter; those cells are taken "
               "from sgt1930's printing of the same lotissement after checking that the legible hectares agree "
               "(`reprint_corrected`), and the cut printed totals are checked on the hectares. sgt1939 Transvaal "
               "ares '9?' solved from the total (`derived_from_totals`)."]),
    "colonisation_planting_lots": dict(
        secs=["planting"], cells=cells_list, key=["year", "property_fr", "measure"], rule5=True,
        dims=["year_label", "scheme", "scheme_fr", "property_fr", "situation_fr", "controle_civil", "observation_fr",
              "measure", "measure_fr", "unit"],
        title_fr="Terres à planter (Ventes avec obligation d'installation dans la Régence)",
        title_en="Land for planting sold with an obligation of settlement in the Regency: lotissements by year, "
                 "area and number of lots",
        unit="Units: hectares and number of lots (`unit`); suggested value_type: mixed.",
        paras=["Printed sgt1924-sgt1935 as table b) of the chapter (ten-year window; not in sgt1936, sgt1939: see "
               "the recapitulation table). `year` is the first year of the printed label; `year_label` keeps the "
               "printed bracket (e.g. `1920-21`, sgt1930 prints `1921`). Years printed with » in every column are "
               "kept as rows with value 0 and property `»`. sgt1935 prints a 1935 line without name (534 ha, 3 "
               "lots) and adds Gamouda (1932) after it. The TOTAUX line is checked. Observation from sgt1926 to "
               "sgt1928: \"Pour les années 1917 à 1919 inclus aucune vente n'a été effectuée\"."]),
    "colonisation_urban_lots": dict(
        secs=["urban"], cells=cells_list, key=["year", "property_fr", "measure"], rule5=True,
        dims=["scheme", "scheme_fr", "property_fr", "situation_fr", "controle_civil", "observation_fr",
              "measure", "measure_fr", "unit"],
        title_fr="Lotissements urbains, industriels ou d'estivage",
        title_en="Urban, industrial and summer-residence lotissements: by year, area and number of lots",
        unit="Units: hectares and number of lots (`unit`); suggested value_type: mixed.",
        paras=["Printed sgt1924-sgt1935 as table c) of the chapter (ten-year window; sgt1922-sgt1923 list these "
               "lotissements in the installation table). Lotissements printed » (suppressed and replaced) are kept "
               "with value 0 and their observation. sgt1928 prints its 1928 areas to the centiare (stored with four "
               "decimals). The TOTAUX line is checked."]),
    "colonisation_lotissements_summary": dict(
        secs=["recap_rural", "recap_plant"], cells=cells_recap, key=["lotissement", "period_fr", "origin", "measure"],
        rule5=True,
        dims=["lotissement", "lotissement_fr", "period", "period_fr", "origin", "origin_fr", "measure", "measure_fr",
              "unit"],
        title_fr="Lotissements. a) Lotissements ruraux livrés à la Colonisation ; b) Lotissements de terres à planter",
        title_en="Lotissements delivered to colonisation: area by origin of the land and number of lots, before and "
                 "after a cut-off year",
        unit="Units: hectares (area, by origin of the land) and number of lots; suggested value_type: mixed.",
        paras=["Printed sgt1924-sgt1939 after the lists; two periods split at a year that moves with the edition "
               "(Antérieure à / Postérieure à 1918 in sgt1924-sgt1927, 1919 in sgt1928, Depuis 1920 in sgt1929, 1921 "
               "in sgt1930, 1926 in sgt1935, 1927 in sgt1936, 1929 in sgt1939). `year` = edition year (state at the "
               "edition date). TOTAUX column and line are checks only. sgt1935 adds a memo line *Achats pour "
               "recasements (pour mémoire)* (6.825,28 ha, 33 rural lots), outside the totals, stored with "
               "`period` = `resettlement_purchases_memo`."]),
    "colonisation_indigenous_settlement": dict(
        secs=["fixation_old", "fixation", "fixation_years"], cells=cells_fixation,
        key=["item", "year_label", "measure"], rule5=True,
        dims=["year_label", "item", "item_fr", "observation_fr", "measure", "measure_fr", "unit"],
        title_fr="Fixation au sol des indigènes (Lotissements tunisiens)",
        title_en="Settlement of Tunisians on the land: families settled and land allotted (cumulative from 1920), "
                 "and allotments by year (sgt1939)",
        unit="Units: count and hectares (`unit`); suggested value_type: mixed.",
        paras=["sgt1925-sgt1929: one line *Période de 1920 à <edition year>*: number of families settled, land "
               "allotted for cultivation (sgt1927: terres de plantation et de cultures attribuées; sgt1928-sgt1929: "
               "terres de plantation et de cultures arbustives) and grazing land, in hectares, with the printed "
               "observation (footnote (1): part of the land in the Territoires du Sud and terres sialines). "
               "sgt1930-sgt1936: number of allotments, lots and area of the lotissements created since 1920 (sgt1930 "
               "adds the Gammouda lotissements created in 1930; its total line is checked). sgt1939: allotments by "
               "year 1920-1939 (`item` = `allotments_of_year`, `year` = that year; total checked). Cumulative lines "
               "carry `year` = edition year, `year_label` = the printed period. Not in sgt1922-sgt1924."]),
    "colonisation_indigenous_sales": dict(
        secs=["sales"], cells=cells_fixation, key=["year_label", "measure"],
        dims=["year_label", "item", "item_fr", "observation_fr", "measure", "measure_fr", "unit"],
        title_fr="Ventes définitives consenties aux attributaires ayant rempli leurs obligations de mise en valeur",
        title_en="Definitive sales to Tunisian allottees who fulfilled their development obligations, by year",
        unit="Units: count and hectares (`unit`); suggested value_type: mixed.",
        paras=["Printed sgt1930-sgt1939. The first line groups the early years differently in each edition "
               "(sgt1930: 1920 à 1923, 1924, 1925 separately; sgt1935: 1920 à 1925; sgt1936-sgt1939: 1920 à "
               "1926); each printed grouping is kept as its own `year_label` from the latest edition printing it "
               "(`year` = its first year), so the groupings overlap: do not add the 1920-1926 rows across labels. "
               "The TOTAUX line of every printing is checked. Every other printing of the same label is compared "
               "below."]),
    "colonisation_regrouping_1935": dict(
        secs=["regroup", "reinstall"], cells=cells_regroup, key=["operation", "lotissement_fr", "measure"],
        rule5=True, dims=["operation", "operation_fr", "lotissement_fr", "measure", "measure_fr", "unit"],
        title_fr="Opérations de regroupement réalisées au 31 décembre 1935 ; Réinstallations effectuées sur des "
                 "propriétés achetées par le Domaine",
        title_en="Regrouping of colonisation lotissements at 31 December 1935: lots taken back, settlers "
                 "reinstalled, and reinstallations on properties bought by the Domaine",
        unit="Units: count and hectares; suggested value_type: mixed.",
        paras=["Printed in sgt1935 only (f298-f299). Footnote (1): the regrouping programme of the rural colonisation "
               "lotissements is in progress. Lots taken back printed as sums for Djebel-Mansour (1 + 6 = 7) and "
               "Ousseltia (2 + 13 = 15): the results are stored. The second table's TOTAUX difference \"151 (2)\" "
               "is not a column sum (footnote (2): lots available for the enlargement programme) and is stored as "
               "`lotissement_fr` = `TOTAL (printed)`. Checks: différence = repris - réinstallés on every line, A "
               "reporter / Report / TOTAUX."]),
    "colonisation_fund": dict(
        secs=["fund"], cells=cells_fund, key=["year", "measure"],
        dims=["measure", "measure_fr", "unit", "endowment_origin_fr"],
        title_fr="Fonds de colonisation. Achats réalisés",
        title_en="Colonisation fund: endowments, annual receipts and expenditure, and area of the properties "
                 "bought (1900-1928)",
        unit="Units: francs (centimes as decimals) and hectares (`unit`); suggested value_type: mixed.",
        paras=["Printed in sgt1922-sgt1928 (1900 to the edition year); not printed from sgt1929. Footnotes "
               "(observations column): (1) Décret du 24 septembre 1900; (2) Décret du 30 décembre 1903; (3) Décret "
               "du 28 décembre 1905; (4) Décret du 25 mai 1905; (5) Décret du 31 décembre 1907; (6) Décret du 31 "
               "décembre 1908; (7) Emprunt 1920 : 1re tranche; (8) Emprunt 1920 : 2e tranche (from sgt1924). "
               "sgt1926 prints 1926 as \"Dotation accordée en 1926 (1)\" with footnote (1) Inscrit au budget "
               "1927; sgt1927-sgt1928 print \"Subvention accordée en 1926\" (sgt1927 keeps the footnote without "
               "its call). From 1926 the area column has ares (hectares with two decimals).",
               "Under the TOTAL line the dotations and recettes totals are added into one printed figure "
               "(checked). sgt1922 prints the dépenses total twice."]),
}

OLD_PARA = ("Old layout printed only in sgt1922 and sgt1923 (chapter XIII); from sgt1924 the chapter is "
            "reorganised (installation / planting / urban lists, recapitulation by origin of the land) and this "
            "table is no longer printed. Printed total lines and total columns are checks only (not stored); » = 0.")

TABLES.update({
    "colonisation_lands_delivered_summary": dict(
        secs=["recap22", "recap23"], cells=cells_old_recap, rule5=True,
        key=["origin", "lot_type", "measure"],
        dims=["period_fr", "origin", "origin_fr", "lot_type", "lot_type_fr", "measure", "measure_fr", "unit"],
        title_fr="Ventes avec obligation d'installation : b) Récapitulation (1893-1922) ; Superficie totale des "
                 "terres livrées à la colonisation de 1893 à 1923",
        title_en="Lands delivered to colonisation since 1893: area and lots by type of lot (and, in sgt1922, by "
                 "origin of the land)",
        unit="Units: hectares (area, printed h. a.) and number of lots (`unit`); suggested value_type: mixed.",
        paras=[OLD_PARA, "sgt1922 (f442|f443, lower half): Patrimoine domanial and Achats sur le fonds de "
               "colonisation, each with lots de culture / suburbains / urbains ou industriels, and superficie "
               "totale, lots créés, réservés ou disponibles en cours de vente, vendus; the TOTAL of each origin and "
               "the TOTAL GÉNÉRAL are checks, and créés = réservés + vendus is checked on every line. sgt1923 "
               "(f932|f933) prints a shorter table: lots créés and superficie totale only, by lot type, all "
               "origins together (`origin` = `all`). Not the same table as `colonisation_lotissements_summary` "
               "(sgt1924-sgt1939: by origin domaines / habous / achat / terres sialines and two periods), which "
               "replaces it: kept as a separate file because the categories do not match."],
        doc=DOC_OLD),
    "colonisation_lots_sold_by_controle": dict(
        secs=["soldcc"], cells=cells_soldcc, rule5=True, key=["controle_civil", "lot_type", "measure"],
        dims=["period_fr", "controle_civil", "lot_type", "lot_type_fr", "measure", "measure_fr", "unit"],
        title_fr="Ventes avec obligation d'installation : c) Répartition par contrôle civil des lots vendus de 1893 "
                 "à 1922 (1923)",
        title_en="Colonisation lots sold since 1893, by contrôle civil and type of lot: number and area",
        unit="Units: number of lots and hectares (`unit`); suggested value_type: mixed.",
        paras=[OLD_PARA, "f444|f445 (sgt1922) and f934|f935 (sgt1923), cumulative from 1893 to the edition year "
               "(`year` = edition year). Lots de culture areas are printed to the hectare (» in the ares column) "
               "except a few sgt1923 lines. The TOTAL columns (lots, area) are checked on every line and the TOTAL "
               "GÉNÉRAL line on every column. The sgt1923 totals equal the lots créés of its summary table."],
        doc=DOC_OLD),
    "colonisation_planting_concessions": dict(
        secs=["plant_auth", "plant_sale"], cells=cells_plant_list,
        key=["operation", "year", "property_fr", "controle_civil", "nationality", "measure"],
        dims=["operation", "operation_fr", "property_fr", "controle_civil", "note_fr", "nationality",
              "nationality_fr", "measure", "measure_fr", "unit"],
        title_fr="Ventes avec obligation de planter. a) Propriétés livrées à la colonisation (autorisations de "
                 "planter ; ventes définitives)",
        title_en="Sales with an obligation to plant: planting authorisations and definitive sales by year, region "
                 "and nationality of the beneficiaries (1913-1923)",
        unit="Units: number of concessions / sales and hectares (`unit`); suggested value_type: mixed.",
        paras=[OLD_PARA, "Autorisations de planter (sgt1922 f446|f447, 1913-1922; sgt1923 f936|f937, 1913-1923) "
               "and ventes définitives (sgt1922 f448|f449, 1913-1922; sgt1923 f938|f939, 1914-1923), by année de "
               "la concession / de la vente, nom de la propriété ou désignation des régions, contrôle civil, and "
               "Français / autres Européens / indigènes (number, hectares). The TOTAL columns are checked on every "
               "line. Years printed » in every cell are kept as rows with value 0, empty property and `note_fr` = "
               "`néant`.",
               "Relation to `colonisation_planting_lots`: not the same table. That file (sgt1924-sgt1935, *b) "
               "Terres à planter*) lists lotissements of land to plant by year with area and number of lots; this "
               "one lists authorisations and definitive sales of the old *obligation de planter* regime (mostly "
               "terres sialines of Sfax and the South) by nationality, which the later editions no longer print. "
               "It is therefore a new file rather than an extension.",
               "Row realignment: in both editions the Français area 99 ha of the 1917 Maknassy sale is printed one "
               "line down, on the Sbeïtla line (Maknassy: 1 sale, area », total 1 sale / 99 ha; Sbeïtla: "
               "Français », 99; indigènes 1 / 8 ha; total 1 / 8 ha); it is stored on the Maknassy line, flag "
               "`row_realigned`."],
        doc=DOC_OLD),
    "colonisation_planting_by_controle": dict(
        secs=["plant_cc"], cells=cells_plant_cc, rule5=True,
        key=["controle_civil", "operation", "nationality", "measure"],
        dims=["period_fr", "controle_civil", "operation", "operation_fr", "nationality", "nationality_fr", "measure",
              "measure_fr", "unit"],
        title_fr="Ventes avec obligation de planter. b) Récapitulation et répartition par contrôle civil",
        title_en="Sales with an obligation to plant: planting authorisations and definitive sales since 1893, by "
                 "contrôle civil and nationality",
        unit="Units: number and hectares (`unit`); suggested value_type: mixed.",
        paras=[OLD_PARA, "sgt1922 f450|f451 (1893-1922) and sgt1923 f940|f941 (1893-1923, upper halves). sgt1923 "
               "reprints every sgt1922 figure unchanged although its yearly list adds 1923 sales (Terres sialines, "
               "Maknassy, Sbeïtla, Extrême-Sud): the recapitulation was not updated. The authorisations TOTAL "
               "count column runs into the gutter (check only; legible digits agree with the line sums)."],
        doc=DOC_OLD),
    "colonisation_habous_substitutions": dict(
        secs=["hab_sub"], cells=cells_hab_sub, key=["year", "clause", "measure"],
        dims=["clause", "clause_fr", "measure", "measure_fr", "unit"],
        title_fr="Habous. Cessions par substitution aux droits du domaine. a) Propriétés cédées",
        title_en="Habous: properties ceded by substitution for the rights of the Domaine, by year, with and "
                 "without a colonisation clause",
        unit="Units: count, hectares and francs (`unit`); suggested value_type: mixed.",
        paras=[OLD_PARA, "sgt1922 f452 (1913-1922), sgt1923 f942 (1914-1923). The printed valeur globale des "
               "immeubles (= valeur foncière + valeur des constructions) is a check only. 1920 sans clause: 3 "
               "properties, 532 ha, valeur foncière 48.388 fr. but valeur globale printed » in both editions."],
        doc=DOC_OLD),
    "colonisation_habous_substitutions_by_controle": dict(
        secs=["hab_sub_cc"], cells=cells_hab_sub, rule5=True, key=["controle_civil", "clause", "measure"],
        dims=["period_fr", "controle_civil", "clause", "clause_fr", "measure", "measure_fr", "unit"],
        title_fr="Habous. Cessions par substitution aux droits du domaine. b) Récapitulation et répartition par "
                 "contrôle civil",
        title_en="Habous: properties ceded by substitution since 1899, by contrôle civil, with and without a "
                 "colonisation clause",
        unit="Units: count, hectares and francs (`unit`); suggested value_type: mixed.",
        paras=[OLD_PARA, "sgt1922 f452 (1899-1922) and sgt1923 f942 (1899-1923), identical figures. Valeur "
               "globale is a check only."],
        doc=DOC_OLD),
    "colonisation_habous_enzel": dict(
        secs=["enzel"], cells=cells_enzel, key=["year", "buyer", "habous", "measure"],
        dims=["buyer", "buyer_fr", "habous", "habous_fr", "measure", "measure_fr", "unit"],
        title_fr="Habous. Autres cessions (cessions à enzel). a) Propriétés cédées",
        title_en="Habous: other cessions (perpetual leases à enzel) by year, by group of beneficiaries and kind of "
                 "habous",
        unit="Units: count and francs (`unit`); suggested value_type: mixed.",
        paras=[OLD_PARA, "sgt1922 f453 (1913-1922), sgt1923 f943 (1914-1923), both printed sideways (rotated for "
               "reading). Français / autres Européens et indigènes × habous publics / privés: nombre de cessions, "
               "montant global des rentes d'enzel, montant global du capital. The total général columns (habous "
               "publics et privés) are checks only."],
        doc=DOC_OLD),
    "colonisation_habous_enzel_by_controle": dict(
        secs=["enzel_cc"], cells=cells_enzel, rule5=True, key=["controle_civil", "buyer", "habous", "measure"],
        dims=["period_fr", "controle_civil", "buyer", "buyer_fr", "habous", "habous_fr", "measure", "measure_fr",
              "unit"],
        title_fr="Habous. Autres cessions (cessions à enzel). b) Récapitulation et répartition par contrôle civil",
        title_en="Habous: cessions à enzel since 1886, by contrôle civil, group of beneficiaries and kind of habous",
        unit="Units: count and francs (`unit`); suggested value_type: mixed.",
        paras=[OLD_PARA, "sgt1922 f454|f455 (1886-1922; f455 printed sideways) and sgt1923 f944|f945 "
               "(1886-1923). sgt1923 adds the 1923 cessions to Tunis and to the totals; the 1923 Français cession "
               "and the autres Européens et indigènes cessions of 1923 are all counted in Tunis. The Français "
               "habous privés capital column and the autres Européens habous publics count column run into the "
               "gutter but are legible on the crops."],
        doc=DOC_OLD),
})

FAIL_NOTES = {
    "colonisation_lots_sold_by_controle": "sgt1923 Thala prints the line TOTAL area 1.446,89 for 1.353 + 82,23 + "
        "10,66 = 1.445,89; the column totals agree with the lines, so the faulty figure is the printed line total "
        "(check only, not stored; sgt1922's Thala line adds up).",
    "colonisation_planting_concessions": "1917 Terres sialines (Sfax) ventes définitives: Français 6.313 ha + "
        "indigènes 324 ha = 6.637 ha, printed TOTAL 6.037 ha in both editions (zoomed crops); the faulty cell "
        "(a Français area 5.713 or the total) cannot be identified, so nothing is flagged.",
    "colonisation_planting_by_controle": "Ventes définitives, indigènes, superficie: the TOTAL line prints 47.063 "
        "ha for lines summing to 47.103 (both editions); every line adds up to its printed total and the printed "
        "grand total 142.694 equals the sum of the lines, so the faulty figure is the printed column total 47.063.",
    "colonisation_habous_substitutions": "1920 sans clause de colonisation: valeur globale printed » for valeur "
        "foncière 48.388 and constructions » (both editions; the valeur globale column is a check only).",
    "colonisation_habous_substitutions_by_controle": "Grombalia avec clause: valeur globale printed 168.610 for "
        "142.610 + 16.000 = 158.610 (both editions, zoomed crop); the printed column total 1.960.463 agrees with "
        "158.610, so the faulty figure is the printed line total (check only).",
    "colonisation_habous_enzel": "1918: total général nombre de cessions printed 14 for 4 + 1 + 8 + 4 = 17 (both "
        "editions; the rent and capital totals add up). The faulty cell cannot be identified; nothing is flagged.",
    "colonisation_installation_lots": "créés = réservés + vendus fails on lines \"en cours d'attribution\" "
        "(lots created, none yet reserved or sold: » printed) and on sgt1922-sgt1923 Klédia (35 created, 9 + 4) and "
        "sgt1922 Lagrenée-Chaouat (31, 3 + 0). sgt1926-sgt1927 print \"Reports 64.861,22\" for the 64.861,32 "
        "carried. sgt1928 prints » in the TOTAUX column of the 1928 lines while the column total (1.191) counts "
        "them. sgt1936: Djedeïda 1930 prints » for maraîchers but 4 in TOTAUX (other editions: 4 maraîchers; "
        "flag total_mismatch on the maraîchers cell), and the TOTAUX lot total 517 leaves them out; the area "
        "total 49.611,84 and sgt1939's 20.674,91 are both 1.000 ha below the sum of their lines.",
    "colonisation_lotissements_summary": "sgt1928 (f1012-f1013) is internally inconsistent, each figure confirmed "
        "on zoomed crops: habous before 1919 printed 19.245 (other editions 19.205; the column total 20.308 needs "
        "19.205 + 1.103), after 1919 printed 1.043 (needs 1.103), rural lots 846 / 828 against line totals 1.072 / "
        "1.200; the planting table's TOTAUX column (140.079, 42.036, 182.115) does not match its parts (128.500, "
        "53.605, 182.105). sgt1930 prints the before-1921 total 142.233,20 for parts giving 143.233,20, the grand "
        "total area 24.065,59 for 260.065,59 (two digits dropped), habous total 20.848,60 for 20.818,60, and "
        "ares off by 0,01 (rounding).",
    "colonisation_indigenous_sales": "sgt1935 and sgt1936 print the ventes proposées total 4 above the sum of their "
        "lines (2.283 for 2.279; 2.452 for 2.448); sgt1939's area total 35.175,31 is 0,10 below its lines.",
    "colonisation_urban_lots": "sgt1935 prints TOTAUX 160,18 ha / 1.344 lots for lines summing to 130,90 / 1.143 "
        "(the lines agree with sgt1930 for 1926-1930; the printed total matches no subset).",
    "colonisation_regrouping_1935": "Réinstallations: TOTAUX superficie 6.825,28 ha for lines summing to 6.725,28 "
        "(every line re-read; the same areas are printed in sgt1936's installation list; the recapitulation of "
        "sgt1935 repeats 6.825,28).",
    "colonisation_fund": "sgt1922 recettes total 24.865.246,53 for years summing to 24.860.246,53 (5.000 more; "
        "later editions print totals consistent with the same yearly figures); sgt1922 dépenses total 38.867.034,51 "
        "for 38.867.043,51 (digits 34/43 transposed), sgt1927 65.881.547,53 for 65.881.548,53, sgt1928 "
        "93.069.400,25 for 93.069.401,15 (small printed errors; every yearly figure equal in all seven printings).",
}


CHAPTER_VIEWS.update({
    "sgt1922": (437, 456), "sgt1923": (927, 946), "sgt1924": (1431, 1444), "sgt1925": (499, 512),
    "sgt1926": (1009, 1024), "sgt1927": (471, 488), "sgt1928": (999, 1016), "sgt1929": (477, 492),
    "sgt1930": (1013, 1028), "sgt1935": (291, 306), "sgt1936": (172, 181), "sgt1939": (151, 156)})

SURVEY = {
    "sgt1922": "f437 chapter XIII title; f438|f439 to f442|f443 Ventes avec obligation d'installation a) propriétés "
               "livrées à la colonisation (1913-1922), f442|f443 lower half b) récapitulation (1893-1922: patrimoine "
               "domanial / achats sur le fonds de colonisation; lots de colonisation, suburbains, urbains); f444|f445 "
               "c) répartition par contrôle civil des lots vendus de 1893 à 1922; f446|f447 Ventes avec obligation de "
               "planter a) autorisations de planter (1913-1922); f448|f449 ventes définitives (1913-1922); f450|f451 b) "
               "récapitulation et répartition par contrôle civil (1893-1922) and Fonds de colonisation (1900-1922); "
               "f452 Habous: cessions par substitution aux droits du domaine a) 1913-1922, b) par contrôle civil "
               "(1899-1922); f453 (rotated) cessions à enzel a) 1913-1922; f454|f455 b) répartition par contrôle "
               "civil (1886-1922); f456 blank. f457 = chapter XIV.",
    "sgt1923": "f927 title; f928-f933 a) propriétés livrées (1914-1923) and, f932|f933 lower half, superficie "
               "totale des terres livrées (1893-1923); f934|f935 c) répartition par contrôle civil (1893-1923); "
               "f936|f937 obligation de planter: autorisations (1913-1923; title says 1914-1923); f938|f939 ventes "
               "définitives (1914-1923); f940|f941 récapitulation par contrôle civil (1893-1923) and Fonds de "
               "colonisation (1900-1923); f942 Habous substitutions a) 1914-1923 and b) 1899-1923; f943 (sideways) "
               "cessions à enzel a) 1914-1923; f944|f945 b) 1886-1923 (upright); f946 blank. f947 = chapter XIV.",
    "sgt1924": "f1431 title; f1432-f1435 a) Ventes avec obligation d'installation personnelle (1914-1924); f1436|f1437 "
               "b) Terres à planter (1914-1924); f1438|f1439 c) Lotissements urbains, industriels ou d'estivage "
               "(1914-1924); f1440 a) lotissements ruraux livrés à la colonisation (recap.), f1441 b) terres à "
               "planter (recap.); f1442|f1443 Fonds de colonisation (1900-1924); f1444 blank. f1445 = chapter XIV.",
    "sgt1925": "f499 title; f500-f503 a) (1916-1925); f504|f505 b); f506|f507 c); f508-f509 recap.; f510|f511 fonds; "
               "f512 Fixation au sol des indigènes (1920-1925). f513 = chapter Travail.",
    "sgt1926": "f1009 title; f1010-f1015 a) (1917-1926); f1016|f1017 b); f1018|f1019 c); f1020-f1021 recap.; "
               "f1022|f1023 fonds; f1024 fixation (1920-1926). f1025 = chapter XIV.",
    "sgt1927": "f471 title; f472-f479 a) (1918-1927); f480|f481 b); f482|f483 c); f484-f485 recap.; f486|f487 fonds; "
               "f488 fixation (1920-1927). f489 = chapter XIV.",
    "sgt1928": "f999 title; f1000-f1007 a) (1919-1928); f1008|f1009 b); f1010|f1011 c); f1012-f1013 recap.; "
               "f1014|f1015 fonds (1900-1928); f1016 fixation (1920-1928). f1017 = chapter XIV.",
    "sgt1929": "f477 title; f478-f485 a) (1920-1929); f486|f487 b); f488|f489 c); f490-f491 recap.; f492 fixation "
               "(1920-1929); no colonisation fund from this edition. f493 = chapter XIV.",
    "sgt1930": "f1013 title; f1014-f1021 a) (1921-1930); f1022|f1023 b); f1024|f1025 c); f1026-f1027 recap.; f1028 "
               "fixation a) and b) ventes définitives. f1029 = chapter XIV.",
    "sgt1935": "f291 chapter XIV title; f292-f297 a) (1926-1935); f298|f299 opérations de regroupement au 31 "
               "décembre 1935 and réinstallations sur des propriétés achetées par le Domaine; "
               "f300|f301 b) (1926-1935); f302|f303 c) (1926-1935); f304-f305 recap.; f306 fixation a) and b). "
               "f307 = chapter XV.",
    "sgt1936": "f172 chapter XIII title; f173-f178 a) (1927-1936); f179 recap. a) and b); f180 fixation and ventes "
               "définitives; f181 blank; f182 = chapter XIV Mutualité agricole (so the colonisation chapter is "
               "f172-f181, not f172-f187 as CHAPTERS.md had it). No b) or c) lists.",
    "sgt1939": "f151 chapter XIII title; f152|f153 Ventes avec obligation d'installation personnelle (1929-1939); "
               "f154 recap. a) and b); f155 Lotissements tunisiens: fixation by year 1920-1939 and ventes "
               "définitives; f156 blank. f157 = next chapter.",
}

NOT_DONE = ("Every table of the chapter is transcribed in every edition. sgt1922-sgt1923 old-layout tables (second "
            "pass): b) récapitulation / superficie totale des terres livrées (f442|f443, f932|f933) -> "
            "colonisation_lands_delivered_summary; c) répartition par contrôle civil des lots vendus (f444|f445, "
            "f934|f935) -> colonisation_lots_sold_by_controle; ventes avec obligation de planter, autorisations and "
            "ventes définitives (f446-f449, f936-f939) -> colonisation_planting_concessions, récapitulation par "
            "contrôle civil (f450|f451, f940|f941 upper halves) -> colonisation_planting_by_controle; Habous "
            "substitutions (f452, f942) -> colonisation_habous_substitutions and _by_controle; cessions à enzel "
            "(f453-f455, f943-f945; f453 and f455 printed sideways, f945 upright) -> colonisation_habous_enzel and "
            "_by_controle.")


def write_survey():
    L = ["# Colonisation chapter: survey of every edition", "",
         "Chapter *Colonisation* (XIII; XIV in sgt1935). First and last views confirmed on the page images "
         "(chapter title and next chapter title). Extraction: `extract_colonisation.py`. Every transcribed cell "
         "was read on native-resolution crops of the page images (spreads stitched side by side, zoomed crops for "
         "every doubtful figure and every failed check); the Gallica OCR was used only to locate lines.", "",
         "| edition | ark | views |", "|---|---|---|"]
    L += [f"| {e} | `{EDITIONS[e]}` | {a}–{b} |" for e, (a, b) in CHAPTER_VIEWS.items()]
    L += ["", "## Views per edition", ""] + [f"- **{e}**: {t}" for e, t in SURVEY.items()]
    L += ["", "## Tables (CSV)", "", "| CSV | sections | editions |", "|---|---|---|"]
    L += [f"| `{o}` | {', '.join(sp['secs'])} | {', '.join(sp.get('_eds', []))} |" for o, sp in TABLES.items()]
    L += ["", "## Coverage", "", NOT_DONE, ""]
    (OUT / "colonisation_survey.md").write_text("\n".join(L) + "\n")


def build(write=True):
    secs = []
    for ed in ORDER:
        p = TR / f"{PREFIX}_{ed}.txt"
        if p.exists():
            secs += parse(p, ed)
    for s in secs:
        if s["table"] == "fund":
            chk_fund(s)
        elif s["table"] in ("install22", "install", "install35"):
            chk_list(s, "colonisation_installation_lots")
        elif s["table"] == "planting":
            chk_list(s, "colonisation_planting_lots")
        elif s["table"] == "urban":
            chk_list(s, "colonisation_urban_lots")
        elif s["table"] in RECAP_T:
            chk_recap(s)
        elif s["table"] in ("regroup", "reinstall"):
            chk_regroup(s)
        elif s["table"] == "sales":
            chk_fixation(s, "colonisation_indigenous_sales")
        elif s["table"] in ("fixation", "fixation_years"):
            chk_fixation(s, "colonisation_indigenous_settlement")
        elif s["table"] in OLD_SECS:
            chk_old(s)
    fill_check(secs)
    res = {}
    for out, spec in TABLES.items():
        ss = [s for s in secs if s["table"] in spec["secs"]]
        spec["_eds"] = [e for e in ORDER if any(s["ed"] == e for s in ss)]
        recs = []
        for s in ss:
            recs += spec["cells"](s)
        if spec.get("rule5"):
            kept, n, diffs = recs, 0, []
        else:
            kept, n, diffs = select_latest(recs, spec["key"])
        order = {id(r): i for i, r in enumerate(recs)}
        kept.sort(key=lambda r: (ORDER.index(r["census"]) if spec.get("rule5") else 0, r["year"] or 0,
                                 order.get(id(r), 0)))
        flagged = [f"{r['census']} {r['year']} " + " / ".join(str(r.get(k, "")) for k in spec["key"][1:])
                   + f" = {r['value']} ({r['flag']})" for r in kept if r["flag"]]
        res[out] = dict(rows=len(kept), checks=CHK.n[out], failed=list(CHK.fail[out]), overlap_compared=n,
                        overlap_diffs=[list(x) for x in diffs], flagged=flagged, editions=spec["_eds"])
        if write:
            cols = COMMON + spec["dims"] + ["value", "flag"]
            write_csv(out, cols, kept)
            expl = []
            if CHK.fail[out]:
                expl = ["Every failed check below was re-read on a native-resolution crop: the printed values are "
                        "kept. " + FAIL_NOTES.get(out, "")]
            paras = list(spec.get("paras", [])) + expl + [
                "Survey of the whole chapter in every edition: `colonisation_survey.md`."]
            write_notes(out, CHAPTER, SCRIPT, kept, cols, {c: spec.get("doc", {}).get(c) or DOC[c] for c in cols}, spec["title_fr"],
                        spec["title_en"], paras, CHK.n[out], CHK.fail[out], n, diffs, coverage_lines(ss),
                        RULE5 if spec.get("rule5") else RULE4, spec["unit"])
    if write:
        write_validation(OUT / f"{PREFIX}_validation.json", dict(res, _chapter_views=CHAPTER_VIEWS, _survey=SURVEY,
                                                                 _not_transcribed=NOT_DONE, _filled=FILLED))
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
