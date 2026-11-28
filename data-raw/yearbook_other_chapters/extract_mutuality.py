#!/usr/bin/env python3
"""Economic institutions / agricultural mutuality chapter of the Statistique générale de la Tunisie, 12 editions
sgt1922-sgt1939 (*Institutions économiques et sociales*, chapter XIV, sgt1922-sgt1924; the mutuality tables of the
*Travail et prévoyance sociale* chapter XIV of sgt1925; *Mutualité agricole et commerciale*, XIV, sgt1926-sgt1930;
*Mutualité agricole*, XV in sgt1935, XIV in sgt1936 and sgt1939).

  python3 extract_mutuality.py check   parse the transcriptions, run every check, print failures
  python3 extract_mutuality.py build   ... and write csv/mutuality_*.csv and csv/labour_early_*.csv, their .md notes,
                                       csv/mutuality_survey.md and csv/mutuality_validation.json

Source of truth: transcribed/mutuality_<edition>.txt (format in yb_tables.py). The yearly series (crédit mutuel,
coopérative centrale, assurances mutuelles, sociétés de prévoyance) are printed for overlapping ten-year windows:
SPEC_ADDENDUM rule 4 (latest edition kept, every other printing compared). The labour tables printed in this chapter
up to sgt1924 (accidents du travail) are stored here under `labour_early_*` names; the separate labour chapter of
sgt1925-sgt1939 is extracted by extract_labour.py.
"""
import sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # shared helper yb_tables.py
from yb_tables import (COMMON, EDITIONS, ORDER, OUT, TR, Checks, coverage_lines, parse, select_latest, ssum,
                       where, write_csv, write_notes, write_validation)

CHAPTER = "Institutions économiques et sociales / Mutualité agricole"
SCRIPT = "extract_mutuality.py"
PREFIX = "mutuality"
CHK = Checks()


def base(sec, year, view=None, page=None):
    return {"census": sec["ed"], "table_id": sec["table"], "gallica_ark": sec["ark"],
            "source_page": page or sec["page"], "gallica_view": view or sec["view"], "year": year}


def lines(sec, skip=("TOTAL", "TOTAUX")):
    return [r for r in sec["rows"] if "cells" in r and r["label"] not in skip]


def row(sec, label):
    for r in sec["rows"]:
        if r["label"] == label:
            return r["cells"]
    return None


def col_totals(sec, out, cols=None, label="TOTAL"):
    t = row(sec, label)
    if t is None:
        return
    for k in cols or sec["cols"]:
        CHK.eq(out, f"{where(sec)} {k}: {label} = sum of the lines", ssum(r["cells"][k].value for r in lines(sec)),
               t[k].value)


def row_totals(sec, out, groups):
    for r in sec["rows"]:
        if "cells" not in r:
            continue
        c = r["cells"]
        for t, parts in groups.items():
            CHK.eq(out, f"{where(sec)} {r['label']}: {t} = {' + '.join(parts)}", ssum(c[p].value for p in parts),
                   c[t].value)


# ----------------------------------------------------------------- crédit mutuel agricole (rule 4)

CREDIT_M = {
    "fr_caisses": ("french", "local_caisses", "Nombre de caisses", "count"),
    "fr_members": ("french", "members", "Nombre d'adhérents", "count"),
    "ind_caisses": ("indigenous", "local_caisses", "Nombre de caisses", "count"),
    "ind_members": ("indigenous", "members", "Nombre d'adhérents", "count"),
    "bills": ("all", "bills_discounted", "Effets escomptés (nombre)", "count"),
    "amount": ("all", "bills_discounted_amount", "Effets escomptés (montant)", "francs"),
}
CHECKS = {}

GROUP_FR = {
    "credit_caisses": {"french": "Caisses françaises", "indigenous": "Caisses indigènes"},
    "credit_local": {"french": "Caisses locales"},
}
GROUP_FR_1929 = {"french": "Caisses françaises et mixtes", "indigenous": "Anciennes caisses indigènes"}


def cells_credit(sec):
    out = []
    for r in lines(sec):
        for c in sec["cols"]:
            g, m, mfr, unit = CREDIT_M[c]
            if g == "all":
                gfr = ""
            elif sec["table"] == "credit_caisses" and sec["ed"] in ("sgt1929", "sgt1930"):
                gfr = GROUP_FR_1929[g]
            else:
                gfr = GROUP_FR.get(sec["table"], GROUP_FR["credit_caisses"])[g]
            if m == "members" and sec["ed"] in ("sgt1929", "sgt1930") and g == "french":
                mfr = "Nombre d'adhérents français et indigènes"
            if m == "members" and sec["table"] == "credit_local":
                mfr = "Nombre d'adhérents français et tunisiens"
            cell = r["cells"][c]
            out.append(dict(base(sec, int(r["label"])), caisse_group=g, caisse_group_fr=gfr, measure=m,
                            measure_fr=mfr, unit=unit, value=cell.value, flag=cell.flag))
    return out


# ----------------------------------------------------------------- generic yearly tables (rule 4)

def measure_cells(M, extra=None):
    """M: {column: (measure, measure_fr, unit)}; one row per year and column (skip columns mapped to None)."""
    def cells(sec):
        out = []
        for r in lines(sec):
            for c in sec["cols"]:
                if M.get(c) is None:
                    continue
                m, mfr, unit = M[c]
                cell = r["cells"][c]
                d = dict(base(sec, int(r["label"])), measure=m, measure_fr=mfr, unit=unit, value=cell.value,
                         flag=cell.flag)
                if extra:
                    d.update(extra(sec, c))
                out.append(d)
        return out
    return cells


COOP_M = {
    "p20": ("shares_20fr", "Nombre de parts à 20 fr.", "count"),
    "p50": ("shares_50fr", "Nombre de parts à 50 fr.", "count"),
    "sums": ("shares_amount", "Sommes", "francs"),
    "goods": ("goods_delivered", "Opérations commerciales : montant des marchandises livrées", "francs"),
    "seeds": ("loans_seed", "Prêts de semences", "francs"),
    "labour": ("loans_labour", "Prêts de main-d'oeuvre", "francs"),
    "spring": ("loans_spring_work", "Prêts de travaux de printemps", "francs"),
    "harvest": ("loans_harvest", "Prêts de récolte", "francs"),
    "fertiliser": ("loans_fertiliser", "Prêts d'engrais", "francs"),
    "tractors": ("loans_tractors", "Prêts de tracteurs", "francs"),
    "loans_total": ("loans_total", "Montant total des prêts", "francs"),
    "outstanding": ("loans_outstanding", "Prêts restant à rembourser", "francs"),
}
COOP2_M = {
    "capital": ("capital_paid", "Capital social versé (situation au 31 décembre)", "francs"),
    "adv_statutory": ("state_advances_statutory", "Avances de l'Etat (situation au 31 décembre) : statutaires",
                      "francs"),
    "adv_exceptional": ("state_advances_exceptional",
                        "Avances de l'Etat (situation au 31 décembre) : exceptionnelles", "francs"),
    "advances": ("state_advances", "Avances de l'Etat (situation au 31 décembre)", "francs"),
    "goods": ("goods_bought_delivered", "Montant des marchandises (du matériel) acheté(es) en commun et livré(es) "
                                        "aux coopérateurs", "francs"),
}


def chk_coop_parts(sec):
    out = "mutuality_coop_central_shares_business"
    col_totals(sec, out, label="TOTAUX")


def chk_coop_business(sec):
    out = "mutuality_coop_central_shares_business"
    row_totals(sec, out, {"loans_total": ["seeds", "labour", "spring", "harvest", "fertiliser", "tractors"]})
    col_totals(sec, out, label="TOTAUX")


CHECKS.update({"coop_parts": chk_coop_parts, "coop_business": chk_coop_business})

COOP_ORG = {"coop_central": ("coopérative_centrale", "Coopérative centrale des agriculteurs de Tunisie"),
            "coop_moto": ("coopérative_motoculture", "Coopérative de motoculture de Tunisie")}


# ----------------------------------------------------------------- assurances mutuelles agricoles (rule 4)

# measure code -> (unit, heading sgt1922, heading sgt1923-sgt1930, heading sgt1935)
INS_M = {
    "policies": ("policies", "count", "Nombre de polices", "Nombre de polices", "Nombre de polices"),
    "insured": ("insured_value", "francs", "Valeurs assurées", "Valeurs assurées", "Valeurs assurées"),
    "contrib_local": ("contributions_local", "francs", "Cotisations versées : caisses locales",
                      "Répartition des cotisations versées : caisses locales",
                      "Répartition des cotisations versées : caisses locales"),
    "contrib_regional": ("contributions_regional", "francs", "Cotisations versées : caisse régionale",
                         "Répartition des cotisations versées : caisse régionale",
                         "Répartition des cotisations versées : caisse régionale"),
    "contrib_central": ("contributions_central", "francs", "Cotisations versées : caisse centrale",
                        "Répartition des cotisations versées : réassureurs",
                        "Répartition des cotisations versées : réassureurs"),
    "subsidy_local": ("subsidies_local", "francs", "Subventions : caisses locales", "Subventions : caisses locales",
                      "Subventions : caisses locales"),
    "subsidy_regional": ("subsidies_regional", "francs", "Subventions : caisse régionale",
                         "Subventions : caisse régionale", "Subventions : caisse régionale"),
    "subsidy_central": ("subsidies_central", "francs", "Subventions : caisse centrale", None, None),
    "receipts_extra": ("receipts_extra_rebates", "francs", "Recettes supplémentaires et ristournes", None, None),
    "misc_local": ("misc_receipts_local", "francs", None, "Recettes diverses et ristournes : caisse locale", None),
    "misc_regional": ("misc_receipts_regional", "francs", None, "Recettes diverses et ristournes : caisse régionale",
                      None),
    "claims": ("claims", "count", "Nombre de sinistres", "Sinistres : nombre",
               "Sinistres et frais de sinistres : nombre"),
    "indemn_local": ("indemnities_local", "francs", "Indemnités payées : caisses locales",
                     "Sinistres, répartition des indemnités payées : caisses locales",
                     "Sinistres et frais de sinistres, répartition des sommes payées : caisses locales"),
    "indemn_regional": ("indemnities_regional", "francs", "Indemnités payées : caisse régionale",
                        "Sinistres, répartition des indemnités payées : caisse régionale",
                        "Sinistres et frais de sinistres, répartition des sommes payées : caisse régionale"),
    "indemn_central": ("indemnities_central", "francs", "Indemnités payées : caisse centrale",
                       "Sinistres, répartition des indemnités payées : réassureurs",
                       "Sinistres et frais de sinistres, répartition des sommes payées : réassureurs"),
    "costs_local": ("costs_local", "francs", "Autres frais : caisses locales",
                    "Répartition des frais de sinistre : caisses locales", None),
    "costs_regional": ("costs_regional", "francs", "Autres frais : caisse régionale",
                       "Répartition des frais de sinistre : caisse régionale", None),
    "costs_central": ("costs_central", "francs", "Autres frais : caisse centrale",
                      "Répartition des frais de sinistre : réassureurs", None),
    "deficit_local": ("deficit_local_caisses", "francs", "Autres frais : déficit des caisses locales",
                      "Déficit des caisses locales", "Déficit des caisses locales"),
    "gen_local": ("general_costs_rebates_local", "francs", None,
                  "Frais généraux divers et ristournes aux assurés : caisse locale", None),
    "gen_regional": ("general_costs_rebates_regional", "francs", None,
                     "Frais généraux divers et ristournes aux assurés : caisse régionale", None),
    "rebates": ("rebates_insured", "francs", None, None, "Ristournes aux assurés"),
}
INS_CONST_M = {
    "subsidy_regional": ("subsidies_regional_constitution", "francs",
                         "Subventions : caisse régionale, (1) frais de constitution"),
    "costs_regional": ("costs_regional_constitution", "francs",
                       "Autres frais : caisse régionale, (1) frais de constitution"),
}
INS_BRANCH = {"ins_fire": ("fire", "a) Incendie"), "ins_hail": ("hail", "b) Grêle"),
              "ins_hail_constitution": ("hail", "b) Grêle"),
              "ins_accident": ("accident_common_law", "c) Accidents [de dr]oit commun"),
              "ins_accident_work": ("accident_work", "d) Accident[...] (title lost in the binding)")}
INS_REGION = {"": ("", ""), "a": ("tunis_est", "Tunis-Est-Réassurances (a)"),
              "b": ("tunis", "Tunis-Réassurances (b)")}
INS_RECEIPTS = ["contrib_local", "contrib_regional", "contrib_central", "subsidy_local", "subsidy_regional",
                "subsidy_central", "receipts_extra"]
INS_EXPEND = ["indemn_local", "indemn_regional", "indemn_central", "costs_local", "costs_regional", "costs_central",
              "deficit_local"]


def cells_insurance(sec):
    out = []
    right = sec["cols"][sec["cols"].index(sec["split"]):] if sec.get("split") else []
    b, bfr = INS_BRANCH[sec["table"]]
    lay = 0 if sec["ed"] == "sgt1922" else 2 if sec["ed"] == "sgt1935" else 1
    for r in sec["rows"]:
        if "cells" not in r:
            continue
        y, _, reg = r["label"].partition(" ")
        rg, rgfr = INS_REGION[reg]
        for c in sec["cols"]:
            if c in ("receipts_total", "expend_total"):      # printed row totals (sgt1922): checks only
                continue
            if sec["table"] == "ins_hail_constitution":
                m, unit, mfr = INS_CONST_M[c]
            else:
                m, unit = INS_M[c][:2]
                mfr = INS_M[c][2 + lay]
            cell = r["cells"][c]
            rv = c in right
            out.append(dict(base(sec, int(y), int(sec["rview"]) if rv else None, int(sec["rpage"]) if rv else None),
                            branch=b, branch_fr=bfr, regional_caisse=rg, regional_caisse_fr=rgfr, measure=m,
                            measure_fr=mfr, unit=unit, value=cell.value, flag=cell.flag))
    return out


def chk_insurance(sec):
    out = "mutuality_insurance"
    cols = sec["cols"]
    g = {}
    if "receipts_total" in cols:
        g["receipts_total"] = [c for c in INS_RECEIPTS if c in cols]
    if "expend_total" in cols:
        g["expend_total"] = [c for c in INS_EXPEND if c in cols]
    row_totals(sec, out, g)


def fill_illegible(kept, recs, key):
    """A kept (latest) cell that is illegible in its printing takes the latest legible earlier printing, flagged
    reprint_corrected (sgt1935: cents hidden in the binding)."""
    out = []
    for k in kept:
        if k["flag"] == "illegible":
            alt = [r for r in recs if all(r.get(x) == k.get(x) for x in key) and r["value"] is not None]
            if alt:
                alt.sort(key=lambda r: ORDER.index(r["census"]))
                k = dict(alt[-1], flag="reprint_corrected")
        out.append(k)
    return out


CHECKS.update({"ins_fire": chk_insurance, "ins_hail": chk_insurance})


# ----------------------------------------------------------------- office public de crédit agricole indigène (rule 4)

OFFICE_M = {
    "office_resources": {
        "endowments": ("endowments", "Ressources : dotations"),
        "subsidies": ("subsidies", "Ressources : subventions"),
        "loans": ("loans", "Ressources : emprunts"),
        "land_sales": ("state_land_sales", "Ressources : vente de terres domaniales aux agriculteurs indigènes fixés "
                                           "au sol"),
    },
    "office_operations": {
        "medium_term": ("operations_medium_term", "Opérations de l'Office : moyen terme"),
        "short_term": ("operations_short_term", "Opérations de l'Office : court terme"),
    },
}
OFFICE_1925 = {}


def cells_office(sec):
    out = []
    for r in lines(sec):
        for c in sec["cols"]:
            if c == "total":                    # printed row totals: checks only
                continue
            m, mfr = OFFICE_M[sec["table"]][c]
            if c == "land_sales" and sec["ed"] == "sgt1929":
                mfr = "Ressources : vente des terres domaniales"
            cell = r["cells"][c]
            out.append(dict(base(sec, int(r["label"])), measure=m, measure_fr=mfr, unit="francs", value=cell.value,
                            flag=cell.flag))
    return out


def chk_office(sec):
    out = "mutuality_office_credit_agricole"
    parts = [c for c in sec["cols"] if c != "total"]
    row_totals(sec, out, {"total": parts})
    t = row(sec, "TOTAUX")
    if t is None:
        return
    if sec["ed"] == "sgt1930":
        OFFICE_1925.update({c: v.value for c, v in row(sec, "1925").items()})
    add = OFFICE_1925 if row(sec, "1925") is None else {}       # sgt1935 TOTAUX include the 1925 line
    for k in sec["cols"]:
        got = ssum(r["cells"][k].value for r in lines(sec)) + add.get(k, 0)
        CHK.eq(out, f"{where(sec)} {k}: TOTAUX = sum of the lines" + (" + 1925 line of sgt1930" if add else ""),
               got, t[k].value)


CHECKS.update({"office_resources": chk_office, "office_operations": chk_office})


# ----------------------------------------------------------------- sociétés de prévoyance (rule 4)

PREV_M = {
    "seed": ("loans_seed", "Montant des prêts : prêts de semences"),
    "chep": ("loans_livestock", "Montant des prêts : prêts de cheptel"),
    "sulph": ("loans_sulphur_copper_sulphate", "Montant des prêts : prêts de soufre et de sulfate de cuivre"),
    "camp": ("loans_campaign", "Montant des prêts : prêts de campagne"),
    "subs": ("loans_subsistence", "Montant des prêts : prêts de subsistance"),
    "mort": ("loans_mortgage", "Montant des prêts : prêts hypothécaires"),
    "gage": ("loans_pledge", "Montant des prêts : prêts sur gages"),
    "adv": ("advances_branches", "Montant des prêts : avances aux filiales"),
    "total": ("loans_total", "Montant des prêts : total"),
    "cancel": ("loans_cancelled", "Annulation : prêts de subsistance"),
    "r_seed": ("recoveries_seed", "Montant des recouvrements faits sur les prêts : prêts de semences"),
    "r_chep": ("recoveries_livestock", "Montant des recouvrements faits sur les prêts : prêts de cheptel"),
    "r_sulph": ("recoveries_sulphur_copper_sulphate",
                "Montant des recouvrements faits sur les prêts : prêts de soufre et de sulfate de cuivre"),
    "r_camp": ("recoveries_campaign", "Montant des recouvrements faits sur les prêts : prêts de campagne"),
    "r_subs": ("recoveries_subsistence", "Montant des recouvrements faits sur les prêts : prêts de subsistance"),
    "r_mort": ("recoveries_mortgage", "Montant des recouvrements faits sur les prêts : prêts hypothécaires"),
    "r_gage": ("recoveries_pledge", "Montant des recouvrements faits sur les prêts : prêts sur gages"),
    "r_adv": ("recoveries_advances_branches", "Montant des recouvrements faits sur les prêts : avances aux filiales"),
    "r_total": ("recoveries_total", "Montant des recouvrements faits sur les prêts : total"),
    "outstanding": ("loans_outstanding", "Reste à recouvrer sur les prêts"),
}
PREV_LOANS = ["seed", "chep", "sulph", "camp", "subs", "mort", "gage", "adv"]
# cells whose printed value disagrees with the printed row total and the other printings (confirmed on crops),
# and the one cell derived from the printed TOTAUX
PREV_FLAGS = {
    ("sgt1922", 1916, "seed"): "total_mismatch", ("sgt1923", 1916, "seed"): "total_mismatch",
    ("sgt1925", 1924, "r_total"): "total_mismatch", ("sgt1935", 1934, "r_total"): "total_mismatch",
    ("sgt1936", 1927, "r_sulph"): "total_mismatch", ("sgt1936", 1928, "r_seed"): "total_mismatch",
    ("sgt1936", 1928, "r_total"): "total_mismatch", ("sgt1936", 1929, "r_total"): "total_mismatch",
    ("sgt1936", 1932, "total"): "total_mismatch", ("sgt1936", 1932, "r_seed"): "total_mismatch",
    ("sgt1936", 1932, "r_camp"): "total_mismatch", ("sgt1936", 1934, "total"): "total_mismatch",
    ("sgt1936", 1934, "r_total"): "total_mismatch", ("sgt1936", 1935, "total"): "total_mismatch",
    ("sgt1936", 1936, "r_gage"): "total_mismatch",
    ("sgt1936", 1936, "cancel"): "total_mismatch", ("sgt1939", 1936, "cancel"): "derived_from_totals",
}
# TOTAUX that include a line the edition no longer prints: (edition, line) of the earlier printing
PREV_TOT_EXTRA = {"sgt1923": ("sgt1922", "1913"), "sgt1930": ("sgt1929", "1920")}
PREV_LINES = {}


def chk_prev(sec):
    out = "mutuality_provident_societies"
    c = sec["cols"]
    loans = [x for x in PREV_LOANS if x in c]
    for r in lines(sec):
        v = r["cells"]
        PREV_LINES[(sec["ed"], r["label"])] = {k: v[k].value for k in c}
        for tot, parts in (("total", loans), ("r_total", ["r_" + x for x in loans])):
            vals = [v[x].value for x in parts + [tot]]
            if None not in vals:
                CHK.eq(out, f"{where(sec)} {r['label']}: {tot} = sum of the types", ssum(vals[:-1]), vals[-1])
        if None not in (v["total"].value, v["cancel"].value, v["diff"].value):
            CHK.eq(out, f"{where(sec)} {r['label']}: différence = total - annulation",
                   v["total"].value - v["cancel"].value, v["diff"].value)
    t = row(sec, "TOTAUX")
    extra = PREV_LINES.get(PREV_TOT_EXTRA.get(sec["ed"]), {})
    for k in c:
        vals = [r["cells"][k].value for r in lines(sec) if r["cells"][k].flag != "not_applicable"]
        if t[k].value is None or None in vals:
            continue
        CHK.eq(out, f"{where(sec)} {k}: TOTAUX = sum of the lines" + (
            f" + the {PREV_TOT_EXTRA[sec['ed']][1]} line of {PREV_TOT_EXTRA[sec['ed']][0]}" if extra else ""),
            ssum(vals) + (extra.get(k) or 0), t[k].value)


CHECKS.update({"prev": chk_prev})


def prev_post(kept, recs, key):
    """A kept (latest) cell that is illegible or a confirmed misprint (total_mismatch) takes the latest earlier
    printing of the same cell, flagged reprint_corrected (SPEC_ADDENDUM rule 6); without one it stays as printed."""
    out = []
    for k in kept:
        if k["flag"] in ("illegible", "total_mismatch"):
            alt = [r for r in recs if all(r.get(x) == k.get(x) for x in key) and r["value"] is not None
                   and ORDER.index(r["census"]) < ORDER.index(k["census"])]
            if alt:
                alt.sort(key=lambda r: ORDER.index(r["census"]))
                k = dict(alt[-1], flag="reprint_corrected")
        out.append(k)
    return out


def cells_prev(sec):
    out = []
    for r in lines(sec):
        y = int(r["label"])
        for c in sec["cols"]:
            if c == "diff":
                continue
            cell = r["cells"][c]
            if c == "outstanding" and cell.flag == "not_applicable":
                continue                    # braced figure typed on the last line it covers
            m, mfr = PREV_M[c]
            if c == "cancel" and sec["ed"] in ("sgt1936", "sgt1939"):
                mfr = "Annulation : prêts de semences et de subsistance"
            flag = PREV_FLAGS.get((sec["ed"], y, c), cell.flag)
            out.append(dict(base(sec, y), measure=m, measure_fr=mfr, unit="francs", value=cell.value, flag=flag))
    return out


# ----------------------------------------------------------------- documentation

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
    "caisse_group": "`french` = caisses françaises (sgt1922-sgt1928), caisses françaises et mixtes (sgt1929-sgt1930), "
                    "caisses locales (sgt1935-sgt1939: one column, same figures for the overlapping years 1926-1930); "
                    "`indigenous` = caisses indigènes (anciennes caisses indigènes in sgt1929-sgt1930; not printed "
                    "from sgt1935); `all` = effets escomptés (not split)",
    "caisse_group_fr": "printed column heading of the edition kept",
    "institution_fr": "named institution as printed (Coopérative centrale des agriculteurs de Tunisie; Coopérative "
                      "de motoculture de Tunisie)",
    "branch": "insurance branch: `fire` (a) incendie), `hail` (b) grêle), `accident_common_law` (c) accidents de "
              "droit commun, sgt1935), `accident_work` (d), sgt1935: title lost in the binding, the table has a column "
              "on permanent infirmity and death, so presumably accidents du travail)",
    "branch_fr": "printed sub-table heading",
    "regional_caisse": "empty before 1933; from 1933 (sgt1935) the regional caisse « Tunis-Assurances » is split into "
                       "`tunis_est` (Tunis-Est-Réassurances, line a) and `tunis` (Tunis-Réassurances, line b)",
    "regional_caisse_fr": "printed name of the regional caisse (from the footnote)",
    "value": "printed value (» = 0)",
    "flag": "empty, or `illegible`, `not_applicable`, `total_mismatch`, `ocr_corrected`",
}

RULE4 = ("Printed for overlapping year windows: each year is taken from the **latest** edition that prints it "
         "(SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on its own page "
         "image, is compared below.")
RULE5 = ("Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept (`census` = edition).")

TABLES = {
    "mutuality_credit_caisses": dict(
        secs=["credit_caisses", "credit_bills", "credit_local"], cells=cells_credit,
        key=["year", "caisse_group", "measure"],
        dims=["caisse_group", "caisse_group_fr", "measure", "measure_fr", "unit"],
        title_fr="Crédit mutuel agricole. a) Caisses locales françaises et indigènes ; b) Effets escomptés",
        title_en="Agricultural mutual credit: local credit banks (caisses) and members, French and indigenous, and "
                 "bills discounted, by year (1913-1939)",
        unit="Units: count (caisses, members, bills) and francs (amount of bills discounted, centimes as decimals); "
             "suggested value_type: mixed.",
        paras=["Printed in every edition for the ten years before it (sgt1939: 1929-1939). sgt1922-sgt1930: two "
               "tables, a) caisses locales (caisses françaises / caisses indigènes: number of caisses and members; "
               "sgt1929-sgt1930: caisses françaises et mixtes, adhérents français et indigènes, and anciennes "
               "caisses indigènes) and b) effets escomptés (number and amount). sgt1935-sgt1939: one table, caisses "
               "locales (number, adhérents français et tunisiens) and effets escomptés; its caisses locales column "
               "continues the French (and mixed) column (equal figures 1926-1930), so it is stored as "
               "`caisse_group` = `french` with its printed heading.",
               "The number of effets escomptés for 1930 and 1932 is printed » (stored 0 as printed) although an "
               "amount is printed: the number was evidently not reported.",
               "sgt1922 (f460) prints the whole series one year earlier than every later edition (its 1913-1920 "
               "figures are printed for 1914-1921 from sgt1923 on; its 1921 and 1922 caisses lines are equal; its "
               "1922 effets, 2.511 / 13.465.233,15 fr., are printed by no other edition). The later, concordant "
               "editions are kept (rule 4); the sgt1922 differences are listed below. Only the 1913 line is taken "
               "from sgt1922 (1913 in sgt1922's labelling)."]),
}

TABLES.update({
    "mutuality_insurance": dict(
        secs=["ins_fire", "ins_hail", "ins_hail_constitution", "ins_accident", "ins_accident_work"],
        cells=cells_insurance, key=["year", "branch", "regional_caisse", "measure"], post=fill_illegible,
        doc={"flag": "empty, or `ocr_corrected` (the Gallica OCR token at that cell was checked against the image "
                     "and reads otherwise; cells the OCR simply misses or splits are not flagged), `illegible`, "
                     "`not_applicable` (ristournes column not printed), `reprint_corrected` (see below)"},
        dims=["branch", "branch_fr", "regional_caisse", "regional_caisse_fr", "measure", "measure_fr", "unit"],
        title_fr="Assurances mutuelles agricoles. a) Incendie ; b) Grêle ; c) et d) Accidents",
        title_en="Agricultural mutual insurance: policies, insured values, contributions, subsidies, claims and "
                 "costs by level of the mutual system (local caisses, regional caisse, reinsurers), fire, hail and "
                 "accident branches, by year (1913-1935)",
        unit="Units: count (policies, claims) and francs (everything else; centimes as decimals); suggested "
             "value_type: mixed.",
        paras=[
            "Printed in sgt1922-sgt1930 and sgt1935 (two-page spreads; not printed in sgt1936 or sgt1939) for the ten "
            "years before the edition: sgt1922 1913-1922 ... sgt1930 1921-1930, sgt1935 1926-1935. a) incendie and "
            "b) grêle in every edition; sgt1935 adds c) accidents de droit commun and d) a second accident table "
            "(title lost in the binding) for 1933-1935. `source_page`/`gallica_view` give the page of the spread "
            "each cell is printed on.",
            "Three layouts, harmonised on one set of measure codes (`measure_fr` = heading of the edition kept). "
            "sgt1922: cotisations versées and subventions by caisses locales / caisse régionale / caisse centrale, "
            "recettes supplémentaires et ristournes, total des recettes; nombre de sinistres, indemnités payées (three "
            "levels), autres frais (three levels and déficit des caisses locales), total des dépenses. sgt1923-sgt1930: "
            "the caisse centrale columns are headed *réassureurs* (same figures, so the same codes `*_central`); the "
            "subventions keep two levels; recettes diverses et ristournes split caisse locale / caisse régionale "
            "(`misc_receipts_*`; sgt1922's single column equals the régionale one, kept under its own code "
            "`receipts_extra_rebates`); the autres frais become frais de sinistre (`costs_*`, same figures as sgt1922's "
            "autres frais) and frais généraux divers et ristournes aux assurés (`general_costs_rebates_*`); no totals. "
            "sgt1935: sinistres et frais de sinistres, répartition des sommes payées (stored as `indemnities_*`: for "
            "1926-1930 they equal the indemnités payées of sgt1926-sgt1930), déficit des caisses locales and "
            "ristournes aux assurés (`rebates_insured`; blank for 1926-1932, stored NA `not_applicable`); no frais de "
            "sinistre or frais généraux columns, so those measures stop in 1930.",
            "sgt1922's total des recettes and total des dépenses columns are printed row totals: they are not stored, "
            "only checked (below). sgt1922-sgt1924 print a footnote (1) *frais de constitution* 8.150,20 above the "
            "first b) grêle line, in the subventions / caisse régionale and the autres frais / caisse régionale "
            "columns, not included in the totals; stored as year 1913 (the first year of the series) with measures "
            "`subsidies_regional_constitution` and `costs_regional_constitution`.",
            "sgt1935, a) 1931: every left-page column except the réassureurs cotisations (1.393.482,21) is printed », "
            "stored 0 as printed (evidently not reported). The réassureurs cotisations column of a) and b) in sgt1935 "
            "runs into the binding and the second centime digit is hidden on both page edges for most lines: those "
            "cells are `illegible`; for 1926-1930 the value of the latest earlier printing (sgt1930) is stored with "
            "flag `reprint_corrected` (its legible digits agree), for 1932-1935 NA. b) 1921 subventions caisses "
            "locales is printed '.600' in sgt1923-sgt1930 (2.600 in sgt1922): stored 600 as printed. a) 1923 "
            "cotisations caisses locales is printed 4.483.963 » in sgt1923-sgt1929 and corrected to 44.839,63 in "
            "sgt1930 (kept). The same subvention locale a) 1919 is printed 883 in every edition (833 the years "
            "around it).",
            "Overlap differences below the sgt1923-sgt1930 printings are few: sgt1922 prints the a) 1918 déficit des "
            "caisses locales 150,43 on its 1918 line, sgt1923 and later on 1919 (stored 1919 from sgt1930); sgt1926 "
            "prints the b) 1918 recettes diverses caisse régionale 2.428,31 (2.128,31 in every other printing; "
            "confirmed on a 4x crop of f1028, stored from sgt1927).",
            "sgt1925 and sgt1926 were re-typed in full from their own native-resolution images (f520|521, "
            "f1028|1029); every other printing was read independently on its own image."]),
    "mutuality_office_credit_agricole": dict(
        secs=["office_resources", "office_operations"], cells=cells_office, key=["year", "measure"],
        dims=["measure", "measure_fr", "unit"],
        title_fr="Office public de crédit agricole indigène. Ressources ; Opérations de l'Office",
        title_en="Public office for indigenous agricultural credit: resources (endowments, subsidies, loans, sales "
                 "of State land) and operations (medium- and short-term credit), by year (1925-1934)",
        unit="Units: francs (centimes as decimals); suggested value_type: francs.",
        paras=["Printed in sgt1929 (f495: ressources 1925-1929, opérations 1926-1929), sgt1930 (f1031: ressources au "
               "31 décembre 1930, 1925-1930, with a new emprunts column; opérations 1926-1930) and sgt1935 (f310: "
               "ressources au 31 décembre 1934, lines 1926-1934; opérations 1926-1934). Not printed in sgt1936 or "
               "sgt1939: a footnote to the sgt1935 1934 line says the Office was dissolved by decree of 21 February "
               "1934 (1934 operations printed », stored 0 as printed). sgt1929 has no emprunts column (no loans "
               "before 1930 in the later printings). Printed row totals (totaux) and TOTAUX lines are checks only; "
               "the sgt1935 TOTAUX include the 1925 line, which sgt1935 does not print (checked with the sgt1930 "
               "1925 line).",
               "The court terme operations of 1928 are printed 7.262.371 in sgt1929 and 7.626.371 in sgt1930 and "
               "sgt1935 (whose row total 9.291.171, printed in all three, agrees with 1.664.800 + 7.626.371): an "
               "evident transposition in sgt1929; the latest printing is kept."]),
    "mutuality_coop_central_shares_business": dict(
        secs=["coop_parts", "coop_business"], cells=measure_cells(COOP_M), key=["year", "measure"],
        dims=["measure", "measure_fr", "unit"],
        title_fr="Coopérative centrale des agriculteurs. a) Nombre de parts souscrites ; b) Affaires traitées",
        title_en="Central cooperative of farmers: shares subscribed, goods delivered and loans by type, by year "
                 "(1913-1929)",
        unit="Units: count (shares) and francs (centimes as decimals); suggested value_type: mixed.",
        paras=["Printed sgt1922-sgt1929 for the ten years before the edition; replaced from sgt1930 by "
               "`mutuality_coop_central_capital`. a) parts souscrites (sgt1922 also prints a parts à 20 fr. column, "
               "» throughout), b) affaires traitées: montant des marchandises livrées and prêts divers by type, "
               "montant total des prêts (= sum of the six loan types, checked on every line) and prêts restant à "
               "rembourser. TOTAUX lines (sgt1922-sgt1925) are checks only.",
               "The sgt1922 and sgt1923 printings differ from sgt1924 and later for the shares of 1915-1920 and the "
               "goods of 1915-1917 and 1919-1922 (revised figures); the latest printing is kept and every difference "
               "is listed below. The loan lines are identical in every printing."]),
    "mutuality_coop_central_capital": dict(
        secs=["coop_central", "coop_moto"], cells=measure_cells(COOP2_M, lambda sec, c: dict(
            institution_fr=COOP_ORG[sec["table"]][1])),
        key=["year", "institution_fr", "measure"],
        dims=["institution_fr", "measure", "measure_fr", "unit"],
        title_fr="Coopérative centrale des agriculteurs de Tunisie ; Coopérative de motoculture de Tunisie",
        title_en="Central cooperative of farmers and motor-cultivation cooperative of Tunisia: paid-up capital, "
                 "State advances and goods bought in common and delivered, by year (1921-1939)",
        unit="Units: francs; suggested value_type: francs.",
        paras=["Printed sgt1930-sgt1939 (sgt1930: 1921-1930; sgt1935: 1925-1935; sgt1936: 1926-1936; sgt1939: "
               "1929-1939). Two named institutions (`institution_fr` as printed). Situation at 31 December. "
               "sgt1939 prints *néant* for the motoculture State advances 1937-1939 (stored 0). No totals printed."]),
})

TABLES["mutuality_provident_societies"] = dict(
    secs=["prev"], cells=cells_prev, key=["year", "measure"], post=prev_post,
    dims=["measure", "measure_fr", "unit"],
    doc={"flag": "empty, or `total_mismatch` (printed cell contradicted by its printed row total and by the other "
                 "printings, kept as printed), `illegible`, `reprint_corrected` (illegible in the edition kept: value "
                 "of the latest earlier printing), `derived_from_totals` (sgt1939 1936 annulation: second centime "
                 "digit in the binding, = printed TOTAUX minus the other lines)"},
    title_fr="Sociétés indigènes (tunisiennes) de prévoyance. Opérations",
    title_en="Indigenous (Tunisian) provident societies: loans by type, loans cancelled, recoveries by type and "
             "loans outstanding, by year (1913-1939)",
    unit="Units: francs (centimes as decimals); suggested value_type: francs.",
    paras=[
        "Printed in every edition (two-page spread) for the ten years before it: sgt1922 1913-1922, sgt1923 1914-1923, "
        "sgt1924 1914-1924, sgt1925 1916-1925 ... sgt1930 1921-1930 (title 1920-1930), sgt1935 1926-1935, sgt1936 "
        "1927-1936, sgt1939 1930-1939. *Sociétés indigènes de prévoyance* up to sgt1930, *sociétés tunisiennes de "
        "prévoyance* from sgt1935.",
        "Columns: montant des prêts by type (semences; campagne from sgt1923; subsistance; hypothécaires; sur gages from "
        "sgt1935; cheptel and soufre et sulfate de cuivre from sgt1936; avances aux filiales) and total; annulation of "
        "prêts de subsistance (sgt1936-sgt1939: prêts de semences et de subsistance, same code `loans_cancelled`, "
        "`measure_fr` of the edition kept; footnote on 1936: of which 15.307.447,46 for seed loans); différence (= total "
        "minus annulation: a printed check column, not stored); montant des recouvrements by the same types and total; "
        "reste à recouvrer sur les prêts. A type not printed by an edition has no rows for its years from that edition.",
        "Reste à recouvrer: sgt1922-sgt1924 print it per line except a single figure 488.536,84 braced against "
        "1914-1919; sgt1925-sgt1939 print a single figure braced against every line (= the TOTAUX). Each braced figure "
        "is stored on the last year it covers (it is a balance at that date): `loans_outstanding` therefore exists for "
        "1913, 1919-1924 (sgt1922-sgt1924) and for 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936 and 1939 (one per "
        "edition).",
        "Printed row totals (total, total des recouvrements, différence) and the TOTAUX lines are checks only. The "
        "TOTAUX of sgt1923 include the 1913 line (printed only in sgt1922) and those of sgt1930 the 1920 line (title "
        "1920-1930, last printed in sgt1929); they are checked with those lines.",
        "The sgt1936 spread is badly printed (broken and misplaced type, solid black slugs where » is expected, typed "
        "0); several of its cells contradict the row totals and every other printing (see the failed checks). Where such "
        "a cell is the latest printing (1928 recouvrements de semences 31.012.273,27 and total 31.504.741,66, 1929 "
        "recouvrements total 24.476.247,63) or is illegible (1928 prêts de semences), the sgt1935 printing is stored "
        "with flag `reprint_corrected` (32.012.273,27, 34.504.741,66, 24.807.247,63, 44.240.438,47; each makes the "
        "row add up). Its 1927 recouvrements de soufre, printed 91.661,95 (the campagne figure repeated; the row total "
        "and the TOTAUX 5.348,50 imply »), has no other printing and is kept with flag `total_mismatch`. "
        "The différence column of sgt1935-sgt1939 runs into the binding (not typed). sgt1935 prints 1929 recouvrements "
        "de semences 21.173.131,91 and de subsistance 2.127.895,34 (sgt1929-sgt1930: 21.173.131,19 and 2.127.896,06; "
        "both pairs give the printed total), followed by sgt1936; the later printing is kept."])

FAIL_NOTES = {
    "mutuality_office_credit_agricole": "sgt1929 1928 operations: totaux 9.291.171 for 1.664.800 + 7.262.371 = "
        "8.927.171 (zoomed 2x on f495); sgt1930 and sgt1935 print the court terme 7.626.371, which gives the printed "
        "total (digits 26/62 transposed in sgt1929; sgt1930 kept).",
    "mutuality_insurance": "sgt1922 a) incendie: the total des recettes exceeds the seven receipt columns by 2.010,40 "
        "(1913), 3.167,40 (1914), 5.865,53 (1915) and 6.630,10 (1916), by 6,00 in 1918, and falls short by 49,91 in 1919 "
        "(the subvention locale is printed 883, not 833) and by 0,70 in 1922; b) grêle: the total des recettes falls "
        "short of the lines by 20,00 (1915) and 60,00 (1920), and the 1922 total des dépenses 80.930,06 is 3.999,90 above "
        "its lines. Every cell of these lines was re-read on zoomed crops (1.2-1.5x); the 1913-1916 differences look "
        "like receipts not shown in any column. No later edition prints totals, so they cannot be cross-checked.",
    "mutuality_coop_central_shares_business": "sgt1922 and sgt1923 print the 1914 montant total des prêts 1.213.382,55 "
        "for 880.558,10 + 332.794,45 = 1.213.352,55 (zoomed crops of both printings; sgt1924 and later no longer print "
        "1914), and the TOTAUX of the loan columns follow it (9.467.198,10); their travaux de printemps total "
        "556.483,85 is 0,10 above the lines (sgt1924-sgt1925 print 556.483,75). sgt1922's marchandises TOTAUX "
        "15.512.861,90 is 100.000 above its lines (every line re-read at 2.5x). sgt1923: sommes TOTAUX 33.050 for "
        "lines giving 23.050 (the number of parts, 461, adds up), and prêts restant à rembourser TOTAUX 1.103.297,55 "
        "for lines giving 378.063,45. sgt1925 reprints sgt1924's loan TOTAUX, which include the 1915 line it no "
        "longer prints (each difference equals the sgt1924 1915 figure).",
}

FAIL_NOTES["mutuality_provident_societies"] = (
    "sgt1922 and sgt1923 print the 1916 seed loans 1.570.483,20 (sgt1924 and later 1.570.483,26, which makes the "
    "printed row total and the TOTAUX add up; flagged `total_mismatch` in those printings). sgt1925: 1924 recouvrements "
    "total printed 3.206.471,45 for types giving 2.706.471,45 (sgt1926 and later print 2.706.471,45; flagged), and its "
    "TOTAUX of the seed and subsistence loans are 600 and 80.000 above the lines (the TOTAUX of the total column agrees "
    "with the lines, so the two column TOTAUX are misprinted). sgt1928: TOTAUX avances aux filiales 0,02 below the "
    "lines. sgt1929: TOTAUX recouvrements total 146.926.197,45, 1.000 above the lines and above the sum of its own "
    "TOTAUX by type. sgt1930: TOTAUX recouvrements avances aux filiales 4.060.222,65 and total 164.402.074,23 for lines "
    "(with the 1920 line of sgt1929) giving 4.063.222,65 and 154.402.074,23 (one digit misprinted in each). sgt1935: "
    "1934 recouvrements total 10.537.603,17 for types giving ,16 (sgt1939 ,16; flagged), TOTAUX of the total 0,03 and "
    "of the recouvrements de subsistance 0,01 off. sgt1936 (badly printed page): the row failures are its misprints "
    "listed above (1927 soufre, 1928 and 1932 recouvrements de semences, 1932 recouvrements de campagne 19.683,95 for "
    "19.683,11, 1932 total 32.738.151,54, 1934 total 32.765.588,31 and recouvrements total 10.527.603,16, 1935 total "
    "10.980.031,30, 1936 recouvrements sur gages 2.440.267,11 for 2.440.267,91; each flagged `total_mismatch` in "
    "sgt1936, the other printings agree with the row totals); its TOTAUX are computed on the correct figures (r_seed "
    "10.000.000 and r_sulph 91.661,95 off because of the misprinted lines; annulation 91.333,64 off because the 1936 "
    "line is printed 22.454.379,58 where sgt1939 and the TOTAUX give 22.545.713,2x, a digit transposition); its "
    "TOTAUX of the avances aux filiales (30,00), recouvrements de subsistance (51,00) and hypothécaires (0,30) are off "
    "by amounts no line explains (misprinted TOTAUX).")

CHAPTER_VIEWS = {
    "sgt1922": (457, 466), "sgt1923": (947, 956), "sgt1924": (1445, 1454), "sgt1925": (513, 524),
    "sgt1926": (1025, 1036), "sgt1927": (489, 500), "sgt1928": (1017, 1030), "sgt1929": (493, 508),
    "sgt1930": (1029, 1044), "sgt1935": (307, 318), "sgt1936": (182, 187), "sgt1939": (157, 162)}

SURVEY = {
    "sgt1922": "f457 chapter XIV *Institutions économiques et sociales* title; f458 blank; f459 Accidents du travail "
               "a) victims by profession and nationality, b) (lower half); f460 c) causes matérielles (upper half), "
               "Crédit mutuel agricole (1913-1922) a) caisses locales, b) effets escomptés; f461 Coopérative centrale "
               "des agriculteurs (1913-1922) a) parts souscrites, b) affaires traitées; f462|f463 Assurances "
               "mutuelles agricoles (1913-1922) a) incendie; f464|f465 Sociétés indigènes de prévoyance, opérations "
               "(1913-1922); f466 blank; f467-f477 table alphabétique (index of the volume, not tables); the views "
               "after f477 belong to the next edition. So the chapter is f457-f466 (the brief's f457-f502 runs into "
               "the index and the sgt1923 front matter).",
    "sgt1923": "f947 title; f948 blank; f949|f950|f951 Accidents du travail (a, b, c by catégorie); f950 crédit mutuel "
               "(1914-1923); f951 coopérative centrale (1914-1923); f952|f953 assurances mutuelles agricoles "
               "(1914-1923); f954 blank; f955 (with f954) sociétés indigènes de prévoyance (1914-1923); f956 blank; "
               "f957-f967 table alphabétique; f968 onwards sgt1924 front matter. Chapter f947-f956.",
    "sgt1924": "f1445 title; f1446 blank; f1447-f1449 Accidents du travail; f1448 crédit mutuel (1915-1924); f1449 "
               "coopérative centrale (1914-1924 title, lines 1915-1924); f1450|f1451 assurances mutuelles "
               "(1915-1924); f1452|f1453 sociétés indigènes de prévoyance (1914-1924); f1454 blank; f1455-f1469 "
               "table alphabétique. Chapter f1445-f1454.",
    "sgt1925": "No separate chapter: the mutuality tables are printed inside chapter XIV *Travail et prévoyance "
               "sociale* (f513 title): f515-f517 accidents du travail (labour, extract_labour.py), f518 crédit "
               "mutuel agricole (1916-1925), f519 coopérative centrale (1916-1925), f520|f521 assurances mutuelles "
               "(1916-1925), f522|f523 sociétés indigènes de prévoyance (1916-1925); f524 blank; f525 table "
               "alphabétique. The mutuality tables f518-f523 are extracted here.",
    "sgt1926": "f1025 chapter XIV *Mutualité agricole et commerciale*; f1026 crédit mutuel (1917-1926); f1027 "
               "coopérative centrale (1917-1926); f1028|f1029 assurances mutuelles (1917-1926); f1030|f1031 sociétés "
               "indigènes de prévoyance (1917-1926); f1032 banques populaires a) bilan de la Banque populaire "
               "française de Tunisie au 31 décembre 1926; f1033 blank; f1034|f1035 bilan (actif/passif, "
               "continuation / coopérative); f1036 blank. f1037 = chapter XV Travail.",
    "sgt1927": "f489 title; f490 crédit mutuel (1918-1927); f491 coopérative centrale; f492|f493 assurances mutuelles; "
               "f494|f495 prévoyance; f496 banques populaires a) bilan 1927; f497 blank; f498|f499 bilan de la Société "
               "coopérative de consommation (1926-1927); f500 blank. f501 = chapter XV.",
    "sgt1928": "f1017 title; f1018 crédit mutuel (1919-1928); f1019 coopérative centrale; f1020|f1021 assurances; "
               "f1022|f1023 prévoyance; f1024|f1025 bilan de la Banque populaire française au 31 décembre 1928; "
               "f1026|f1027 b) bilan de la Coopérative tunisienne de crédit; f1028|f1029 bilan de la Société "
               "coopérative de consommation « La Maison Française »; f1030 blank. f1031 = chapter XV.",
    "sgt1929": "f493 title; f494 crédit mutuel (1920-1929); f495 Office public de crédit agricole indigène, "
               "ressources (1925-1929) and operations; f496 coopérative centrale (1920-1929); f497 blank; f498|f499 "
               "assurances; f500|f501 prévoyance; f502|f503 bilan Banque populaire 1929; f504|f505 coopérative "
               "tunisienne de crédit; f506|f507 « La Maison Française »; f508 blank. f509 = chapter XV.",
    "sgt1930": "f1029 title; f1030 crédit mutuel (1921-1930); f1031 Office public de crédit agricole indigène; f1032 "
               "Coopérative centrale des agriculteurs de Tunisie and Coopérative de motoculture (1921-1930, new "
               "layout); f1033 blank; f1034|f1035 assurances (1921-1930); f1036|f1037 prévoyance (1920-1930); "
               "f1038|f1039 Banque populaire 1930; f1040|f1041 coopérative tunisienne de crédit; f1042|f1043 « La "
               "Maison Française »; f1044 blank. f1045 = chapter XV.",
    "sgt1935": "f307 chapter XV *Mutualité agricole*; f308 blank; f309 crédit mutuel (1926-1935, one table); f310 "
               "Office public de crédit agricole indigène (ressources au 31 décembre 1934); f311 coopérative "
               "centrale and motoculture (1925-1935); f312|f313 assurances mutuelles agricoles (1925-1935 title, "
               "lines 1926-1935) a) incendie, b) grêle; f314|f315 c) accidents [de dr]oit commun and d) accident[...] "
               "(titles partly in the binding; 1933-1935); f316|f317 sociétés tunisiennes de prévoyance "
               "(1926-1935); f318 blank. f319 = chapter XVI Travail.",
    "sgt1936": "f182 chapter XIV *Mutualité agricole*; f183 crédit mutuel (1927-1936); f184 coopérative centrale and "
               "motoculture (1926-1936); f185|f186 sociétés tunisiennes de prévoyance (1927-1936); f187 blank; f188 "
               "= chapter XV *Travail et prévoyance sociale*. So the chapter ends at f187.",
    "sgt1939": "f157 chapter XIV *Mutualité agricole*; f158 crédit mutuel (1929-1939); f159 coopérative centrale and "
               "motoculture (1929-1939); f160|f161 sociétés tunisiennes de prévoyance; f162 blank; f163 = chapter "
               "XV.",
}

NOT_DONE = ("Transcribed: crédit mutuel agricole (every edition), coopérative centrale des agriculteurs (parts and "
            "affaires traitées sgt1922-sgt1929; capital, avances and goods with the coopérative de motoculture "
            "sgt1930-sgt1939), assurances mutuelles agricoles (sgt1922 f462|f463, sgt1923 f952|f953, sgt1924 "
            "f1450|f1451, sgt1925 f520|f521, sgt1926 f1028|f1029, sgt1927 f492|f493, sgt1928 f1020|f1021, sgt1929 "
            "f498|f499, sgt1930 f1034|f1035, sgt1935 f312|f313 and f314|f315 with c) and d) accidents; every cell "
            "read on 0.75-0.85 whole-half crops of both pages of each spread, binding columns and doubtful figures "
            "zoomed at 1.2-3x; sgt1925 and sgt1926 re-typed in full from 3-4-column native crops; Gallica OCR used as a "
            "cross-check only, `ocr_corrected` only where the OCR token at the cell was checked and reads otherwise), "
            "Office public de crédit agricole indigène (sgt1929 f495, sgt1930 f1031, sgt1935 f310), "
            "sociétés indigènes / tunisiennes de prévoyance (sgt1922 f464|f465, sgt1923 f954|f955, sgt1924 "
            "f1452|f1453, sgt1925 f522|f523, sgt1926 f1030|f1031, sgt1927 f494|f495, sgt1928 f1022|f1023, sgt1929 "
            "f500|f501, sgt1930 f1036|f1037, sgt1935 f316|f317, sgt1936 f185|f186, sgt1939 f160|f161; every cell "
            "read on 0.6x whole-page and 0.75-1.5x native crops of each page). "
            "NOT yet transcribed: bilans of the Banque populaire "
            "française, Coopérative tunisienne de crédit and sociétés coopératives de consommation (sgt1926 "
            "f1032-f1035, sgt1927 f496-f499, sgt1928 f1024-f1029, sgt1929 f502-f507, sgt1930 f1038-f1043); labour "
            "tables of sgt1922-sgt1924 (accidents du travail a) victims by profession and nationality, b), c) "
            "causes matérielles by profession: sgt1922 f459-f460, sgt1923 f949-f951, sgt1924 f1447-f1449), to be "
            "stored as labour_early_*.")


def write_survey():
    L = ["# Mutuality (economic institutions) chapter: survey of every edition", "",
         "Chapter *Institutions économiques et sociales* (XIV, sgt1922-sgt1924), the mutuality part of *Travail et "
         "prévoyance sociale* (XIV, sgt1925), *Mutualité agricole et commerciale* (XIV, sgt1926-sgt1930), "
         "*Mutualité agricole* (XV in sgt1935, XIV in sgt1936 and sgt1939). First and last views confirmed on the "
         "page images (chapter title page and next chapter title). Extraction: `extract_mutuality.py`. Every "
         "transcribed cell was read on native-resolution crops of the page images (whole-table crops at 0.6-0.8 "
         "scale, zoomed crops for every doubtful figure and failed check); the Gallica OCR was used only to locate "
         "tables.", "",
         "| edition | ark | views |", "|---|---|---|"]
    L += [f"| {e} | `{EDITIONS[e]}` | {a}–{b} |" for e, (a, b) in CHAPTER_VIEWS.items()]
    L += ["", "## Views per edition", ""] + [f"- **{e}**: {t}" for e, t in SURVEY.items()]
    L += ["", "## Tables (CSV)", "", "| CSV | sections | editions |", "|---|---|---|"]
    L += [f"| `{o}` | {', '.join(sp['secs'])} | {', '.join(sp.get('_eds', []))} |" for o, sp in TABLES.items()]
    L += ["", "## Coverage", "", NOT_DONE, ""]
    (OUT / "mutuality_survey.md").write_text("\n".join(L) + "\n")


# ----------------------------------------------------------------- bilans (rule 5: one balance per edition)

INST = {"bpf": ("banque_populaire_francaise", "Banque populaire française de Tunisie"),
        "ctc": ("cooperative_tunisienne_credit", "Coopérative tunisienne de crédit"),
        "mf": ("maison_francaise", None)}
MF_FR = {"sgt1926": "« Maison Française »", "sgt1927": "« Société coopérative de consommation »",
         "sgt1928": "Société coopérative dite « La Maison Française »",
         "sgt1929": "Société coopérative dite « La Maison Française »",
         "sgt1930": "Société coopérative dite « La Maison Française »"}
STATEMENT = {"bilan": "balance_sheet", "pl": "profit_loss"}
PLACES = (("la goulette", "la_goulette"), ("franceville", "franceville"), ("tunis", "tunis"))
# (pattern searched in the lower-cased label, code); first match wins. Patterns on the full label (with headings).
ITEM_RULES = [
    (r"solde de l.exercice précédent", "@_opening_balance"), (r"avances sonsenties|remis en 1928|escomptés en 1928|"
                                                             r"reçu en dépôt", "@_entries_year"),
    (r"remboursements effectués|encaissés en 1928|payé en 1928", "@_exits_year"),
    (r"^2 — comptes-courant", "current_accounts"), (r"^3 — correspondants", "correspondents"),
    (r"^4 — effets à l.encaissement", "bills_for_collection"), (r"^5 — effets à recevoir", "bills_receivable"),
    (r"comptes de dépôts", "deposits"),
    (r"redressement valeur immeuble", "property_value_adjustment"),
    (r"compte du capital, résultats", "capital_account_inventory_result"),
    (r"résultat d.inventaire", "inventory_result"),
    (r"actions libéré|capital souscrit en circulation", "share_capital_paid"),
    (r"augmentation de capital", "capital_increase"), (r"^capital", "capital"),
    (r"caisses? et banques|caisse et banques", "cash_banks"),
    (r"caisse d.epargne|caisse d.épargne", "savings_bank"), (r"office postal", "postal_account"),
    (r"banque, solde créditeur|banquier, solde créditeur", "bank_overdraft"), (r"banquier", "banker"),
    (r"caisse, espèces|espèces en caisse|réalisables : caisse$", "cash"),
    (r"caisses prévoyance et secours", "provident_relief_funds"), (r"caisse de secours", "relief_fund"),
    (r"caisse de prévoyance", "staff_provident_fund"),
    (r"titres en dépôt à la", "securities_deposited"),
    (r"titres et marchandises en garantie", "securities_goods_pledged"),
    (r"titres et marchandises", "securities_goods"), (r"titres et valeurs", "securities"),
    (r"titres (remis )?en garantie", "securities_pledged"), (r"titres (remis )?en dépôt", "securities_deposited"),
    (r"comptes courants et clients de passage", "current_accounts_occasional_customers"),
    (r"clients de passage", "occasional_customers"),
    (r"comptes courants créditeurs", "creditor_current_accounts"),
    (r"comptes courants, avances|comptes courants : avances|comptes courants, soldes créditeurs",
     "current_account_advances"),
    (r"soldes débiteurs|clients débiteurs|débiteurs divers", "debtors"),
    (r"débiteurs douteux", "doubtful_debtors"), (r"comptes débiteurs", "debtor_accounts"),
    (r"comptes?[- ]courants?", "current_accounts"), (r"correspondants", "correspondents"),
    (r"effets escomptés", "bills_discounted"), (r"effets à l.encaissement", "bills_for_collection"),
    (r"effets à recevoir", "bills_receivable"),
    (r"effets à payer au trésor|effets à payer \(trésor\)", "bills_payable_treasury"),
    (r"effets à payer", "bills_payable"), (r"factures à payer", "invoices_payable"),
    (r"notes à payer", "notes_payable"),
    (r"bons du trésor \(amort", "treasury_bonds_redemption"), (r"bons du trésor", "treasury_bonds"),
    (r"trésor et sociétés? de prévoyance", "treasury_provident_societies"), (r"^trésor$", "treasury"),
    (r"mobiliers et frais d.installation|frais d.installation et mobilier", "furniture_installation"),
    (r"mobilier et matériel|matériel de magasin : matériel", "furniture_equipment"), (r"^mobilier$", "furniture"),
    (r"frais de première installation|frais de premier établissement", "setup_costs"),
    (r"agence de sousse", "branch_sousse_setup_costs"), (r"agence de béja", "branch_beja"),
    (r"comptes? d.ordre", "suspense_accounts"),
    (r"participation", "participations"), (r"avances de l.etat", "state_advances"),
    (r"fonds de prévoyance", "provident_fund"), (r"fonds spécial", "special_fund"),
    (r"avances sur fonds spécial", "special_fund_advances"),
    (r"réserves? légale", "legal_reserve"), (r"réserve spéciale", "special_reserve"),
    (r"réserve sur débiteurs douteux", "reserve_doubtful_debtors"), (r"réserves|fonds de réserves", "reserves"),
    (r"bénéfices reportés", "retained_profits"), (r"profits et pertes", "profit_loss_balance"),
    (r"dividendes", "dividends_payable"), (r"comptes d.encaissements?", "collection_accounts"),
    (r"réescompte et intérêts à payer", "rediscount_interest_payable"), (r"réescompte", "rediscount"),
    (r"intérêts à payer", "interest_payable"), (r"intérêts et commissions", "interest_commissions"),
    (r"crédit à l.artisanat-réserve", "artisan_credit_reserve"),
    (r"crédit à l.artisanat : prêts|avances aux artisans|^artisanat", "loans_artisans"),
    (r"crédit artisanal|crédit de l.artisanat|crédit à l.artisanat", "artisan_credit_fund"),
    (r"fonds d.etat", "government_securities"), (r"crédits par acceptations", "acceptance_credits"),
    (r"acceptations", "acceptances"), (r"actionnaires", "shareholders"),
    (r"provisions pour amortissement", "depreciation_provisions"),
    (r"frais généraux anticipés", "prepaid_expenses"), (r"fournitures de bureau", "office_supplies"),
    (r"loyer anticipé", "prepaid_rent"), (r"frais généraux", "general_expenses"),
    (r"bénéfices? nets?|bénéfices de l.exercice|solde ou bénéfice net", "net_profit"),
    (r"portefeuille", "portfolio"), (r"créditeurs$", "creditors"),
    (r"achats|stock", "stock"), (r"immeuble à tunis|immeubles|valeur actuelle immeuble", "building"),
    (r"travaux neufs", "building_works"), (r"frais d.achats? d.immeubles?|frais d.achat immeuble",
                                           "building_purchase_costs"),
    (r"fédération des coopératives", "federation_cooperatives"),
    (r"litiges maritimes", "maritime_claims"), (r"litiges à recouvrer", "claims_recoverable"),
    (r"divers manquants", "goods_shortfalls"), (r"créance de l.etat", "state_claim"),
    (r"cautionnements", "guarantees"), (r"créanciers divers|fournisseurs", "suppliers_creditors"),
]


def item_code(label):
    import re
    low = label.lower()
    for pat, code in ITEM_RULES:
        if re.search(pat, low):
            if code.startswith("@"):
                parent = label.split(" : ")[0]
                return item_code(parent) + code[1:]
            break
    else:
        raise KeyError(f"no item code for {label!r}")
    leaf = low.split(" : ")[-1]
    if code in ("stock", "guarantees", "setup_costs", "furniture_equipment", "debtors"):
        for p, c in PLACES:
            if p in leaf:
                return f"{code}_{c}"
    return code


BAL_FLAGS = {("sgt1928", "bpf", "assets", "2 — Comptes-courant (Avances en cours) : Solde de l'Exercice précédent"):
             "total_mismatch"}
BAL_SIDES = {}


def chk_bilan(sec):
    out = "mutuality_balance_sheets"
    w = f"{where(sec)} [{sec['inst']} {sec['side']}]"
    rows = [r for r in sec["rows"] if "cells" in r]
    items = [r for r in rows if r["label"] != "TOTAL" and not r["label"].startswith(("SUBTOTAL ", "DSUM ", "DETAIL "))]
    val = {id(r): r["cells"]["value"].value for r in rows}
    for i, r in enumerate(rows):
        lab = r["label"]
        if lab.startswith("SUBTOTAL "):
            g = lab[9:] + " : "
            CHK.eq(out, f"{w} subtotal {lab[9:]} = its lines", ssum(val[id(x)] for x in items
                                                                     if x["label"].startswith(g)), val[id(r)])
        elif lab.startswith("DSUM "):
            j, parts = i - 1, []
            while j >= 0 and rows[j]["label"].startswith("DETAIL "):
                parts.append(val[id(rows[j])])
                j -= 1
            CHK.eq(out, f"{w} {lab[5:]}: printed sum = solde précédent + entries", ssum(parts), val[id(r)])
            nxt, bal = rows[i + 1], rows[i + 2]
            CHK.eq(out, f"{w} {lab[5:]}: balance = printed sum - exits", val[id(r)] - val[id(nxt)], val[id(bal)])
        elif lab == "TOTAL":
            CHK.eq(out, f"{w} TOTAL = sum of the items", ssum(val[id(x)] for x in items), val[id(r)])
            BAL_SIDES[(sec["ed"], sec["inst"], sec["table"], sec["side"])] = val[id(r)]
    if sec["table"] == "pl" and sec["side"] == "debit":
        BAL_SIDES[(sec["ed"], sec["inst"], "net_profit")] = val[id(items[-1])]
    if sec["table"] == "bilan" and sec["inst"] == "bpf" and sec["side"] == "liabilities":
        BAL_SIDES[(sec["ed"], sec["inst"], "pp")] = [val[id(x)] for x in items
                                                     if x["label"].lower().startswith("profits et pertes")][0]


def chk_bilan_sides():
    out = "mutuality_balance_sheets"
    for (ed, inst, tab, side), v in list(BAL_SIDES.items()) if False else []:
        pass
    keys = sorted({(k[0], k[1], k[2]) for k in BAL_SIDES if len(k) == 4}, key=lambda k: (ORDER.index(k[0]), k[1:]))
    for ed, inst, tab in keys:
        a, b = (("assets", "liabilities") if tab == "bilan" else ("debit", "credit"))
        CHK.eq(out, f"{ed} {inst} {'bilan' if tab == 'bilan' else 'profits et pertes'}: {a} total = {b} total",
               BAL_SIDES[(ed, inst, tab, a)], BAL_SIDES[(ed, inst, tab, b)])
        if tab == "pl":
            CHK.eq(out, f"{ed} {inst}: bénéfice net (profits et pertes) = profits et pertes (bilan passif)",
                   BAL_SIDES[(ed, inst, "net_profit")], BAL_SIDES[(ed, inst, "pp")])


CHECKS.update({"bilan": chk_bilan, "pl": chk_bilan})


def cells_bilan(sec):
    out, n = [], 0
    code, ifr = INST[sec["inst"]]
    ifr = ifr or MF_FR[sec["ed"]]
    date = sec.get("date", "")
    year = int(date[-4:]) if date else int(sec["ed"][3:])
    for r in sec["rows"]:
        lab = r.get("label", "")
        if "cells" not in r or lab == "TOTAL" or lab.startswith(("SUBTOTAL ", "DSUM ")):
            continue
        n += 1
        detail = lab.startswith("DETAIL ")
        lab = lab.removeprefix("DETAIL ")
        cell = r["cells"]["value"]
        out.append(dict(base(sec, year), institution=code, institution_fr=ifr, date_fr=date,
                        statement=STATEMENT[sec["table"]], side=sec["side"], line_no=n,
                        line_type="detail" if detail else "item", item=item_code(lab), item_fr=lab,
                        unit="francs", value=cell.value,
                        flag=BAL_FLAGS.get((sec["ed"], sec["inst"], sec["side"], lab), cell.flag)))
    return out


# ----------------------------------------------------------------- labour_early_* (accidents du travail, sgt1922-sgt1924)

ACC_CAT = {"Alimentation": "food", "Métallurgie": "metallurgy", "Tabac, Services d'Etat": "tobacco_state_services",
           "Electricité, Eau, Gaz": "electricity_water_gas", "Mines et Carrières": "mines_quarries",
           "Transports : transport": "transport_operations", "Transports : ateliers": "transport_workshops",
           "Construction": "construction", "Manutention": "handling", "Chaux et Ciment": "lime_cement",
           "Industrie du bois": "wood_industry", "Agriculture": "agriculture", "Autres": "other"}
ACC_NAT = {"french": "Français", "italian": "Italiens", "indigenous": "Indigènes", "foreign": "Etrangers"}
ACC_SEV = {"dead": ("dead", "Morts"), "inc_more1m": ("incapacity_over_1_month", "Incapacités de plus d'un mois"),
           "inc_less1m": ("incapacity_under_1_month", "Incapacités de moins d'un mois")}
ACC_CAUSE = {
    "motors": ("machine_motors", "Moteurs"), "transmission": ("machine_transmission", "Transmission"),
    "machines": ("machine_tools_looms", "Machines outils, Métiers"),
    "lifting": ("lifting", "Ascenseurs, Grues, Appareils de levage"),
    "autoclaves": ("autoclaves", "Autoclaves, Chaudières à vapeur"), "explosives": ("explosives", "Explosifs"),
    "hot_matter": ("hot_matter", "Matières incandescentes, brûlantes, corrosives"),
    "falling_objects": ("falling_objects", "Eboulements, chute d'objets, etc."),
    "worker_fall": ("worker_fall", "Chute de l'ouvrier d'une échelle, etc."),
    "handling": ("handling", "Manutention de fardeaux"),
    "traction": ("traction", "Traction - Accidents occasionnés par les animaux"),
    "hand_tools": ("hand_tools", "Outils à main : scies, hâches, marteaux"),
    "miscellaneous": ("miscellaneous", "Causes diverses"), "unknown": ("unknown", "Causes inconnues"),
    "footwear": ("footwear", "Défaut de chaussures")}
ACC_TOT = defaultdict(dict)


def acc_rows(sec):
    return [r for r in sec["rows"] if "cells" in r and r["label"] != "Totaux"]


def chk_acc(sec):
    out = {"acc_nat": "labour_early_accidents_nationality", "acc_sev": "labour_early_accidents_outcome",
           "acc_cause": "labour_early_accidents_causes"}[sec["table"]]
    parts = sec["cols"][:-1]
    for r in sec["rows"]:
        if "cells" in r:
            c = r["cells"]
            CHK.eq(out, f"{where(sec)} {r['label']}: total = sum of the columns", ssum(c[p].value for p in parts),
                   c["total"].value)
    t = row(sec, "Totaux")
    for k in sec["cols"]:
        CHK.eq(out, f"{where(sec)} {k}: Totaux = sum of the lines", ssum(r["cells"][k].value for r in acc_rows(sec)),
               t[k].value)
    ACC_TOT[sec["ed"]][sec["table"]] = {r["label"]: r["cells"]["total"].value for r in sec["rows"] if "cells" in r}
    if len(ACC_TOT[sec["ed"]]) == 3:
        a = ACC_TOT[sec["ed"]]
        for lab, v in a["acc_nat"].items():
            for t2 in ("acc_sev", "acc_cause"):
                o2 = {"acc_sev": "labour_early_accidents_outcome", "acc_cause": "labour_early_accidents_causes"}[t2]
                CHK.eq(o2, f"{sec['ed']} {lab}: total of {t2} = total of acc_nat", a[t2][lab], v)


CHECKS.update({"acc_nat": chk_acc, "acc_sev": chk_acc, "acc_cause": chk_acc})


def page_of(sec, col):
    if sec.get("split") and sec["cols"].index(col) >= sec["cols"].index(sec["split"]):
        return int(sec["page2"]), int(sec["view2"])
    return sec["page"], sec["view"]


def cells_acc(sec):
    out = []
    y = int(sec["ed"][3:])
    for r in acc_rows(sec):
        for c in sec["cols"]:
            if c == "total":
                continue
            p, v = page_of(sec, c)
            d = dict(base(sec, y, v, p), category=ACC_CAT[r["label"]], category_fr=r["label"])
            if sec["table"] == "acc_nat":
                d.update(nationality=c, nationality_fr=ACC_NAT[c])
            elif sec["table"] == "acc_sev":
                d.update(outcome=ACC_SEV[c][0], outcome_fr=ACC_SEV[c][1])
            else:
                d.update(cause=ACC_CAUSE[c][0], cause_fr=ACC_CAUSE[c][1])
            cell = r["cells"][c]
            d.update(value=cell.value, flag=cell.flag)
            out.append(d)
    return out


ACC_PARA = ("Printed in the chapter *Institutions économiques et sociales* (XIV) of sgt1922-sgt1924 before the labour "
            "tables moved to the chapter *Travail et prévoyance sociale* (extracted by `extract_labour.py` as "
            "`labour_accidents_*` from sgt1925). No year in the titles: `year` = edition year (the same convention as "
            "`labour_accidents_*`). The 13 printed 'professions' are exactly those of sgt1925-sgt1926 and carry the "
            "same `category` codes (Transports split into transport / ateliers); row totals (Totaux column) and the "
            "Totaux line are checks only, as is the agreement of each profession's total across tables a), b) and c) "
            "(it holds in every edition). Chaux et Ciment is printed » in every column of sgt1923.")
EARLY = {
    "labour_early_accidents_nationality": dict(
        secs=["acc_nat"], dims=["category", "category_fr", "nationality", "nationality_fr"],
        title_fr="Accidents du travail. a) Répartition d'après la nationalité des victimes",
        title_en="Industrial accidents by occupation and nationality of the victim, sgt1922-sgt1924",
        paras=[ACC_PARA, "Same columns and codes as `labour_accidents_nationality` (sgt1925-sgt1926 layout: Français, "
               "Italiens, Indigènes, Etrangers); the two files can be stacked."]),
    "labour_early_accidents_outcome": dict(
        secs=["acc_sev"], dims=["category", "category_fr", "outcome", "outcome_fr"],
        title_fr="Accidents du travail. b) Répartition d'après la gravité",
        title_en="Industrial accidents by occupation and outcome (deaths, incapacity over / under one month), "
                 "sgt1922-sgt1924",
        paras=[ACC_PARA, "Same columns and codes as `labour_accidents_outcome` in its sgt1925-sgt1926 layout (morts, "
               "incapacités de plus d'un mois, de moins d'un mois); from sgt1927 that table uses other outcome "
               "categories (incapacité permanente / temporaire, suites inconnues), which do not line up with these."]),
    "labour_early_accidents_causes": dict(
        secs=["acc_cause"], dims=["category", "category_fr", "cause", "cause_fr"],
        title_fr="Accidents du travail. c) Causes matérielles des accidents par catégorie professionnelle",
        title_en="Industrial accidents by occupation and material cause, sgt1922-sgt1924",
        paras=[ACC_PARA, "Two-page spread in each edition (`source_page`/`gallica_view` = page of each cell; the "
               "split falls after Matières incandescentes, which sgt1922 and sgt1923 repeat on the left edge of the "
               "right-hand page with the same figures). The 15 causes and their codes are those of "
               "`labour_accidents_causes` for sgt1925-sgt1926 (moteurs ... défaut de chaussures); sgt1927 and later "
               "use a different list."]),
}
EARLY_DOC = {
    "category": "occupational category (English code, same as `labour_accidents_*` sgt1925-sgt1926)",
    "category_fr": "profession as printed", "nationality": "nationality of the victim (English code)",
    "nationality_fr": "printed heading", "outcome": "outcome of the accident (English code)",
    "outcome_fr": "printed heading", "cause": "material cause (English code)", "cause_fr": "printed heading",
    "value": "printed value (» = 0)", "flag": "empty (no cell flagged)", "year": "edition year (no year printed)",
    "census": "edition (each edition kept)",
}

BAL_DOC = {
    "census": "edition (each edition kept)",
    "year": "year of the balance date (« La Maison Française » sgt1928-sgt1930, no date printed: edition year)",
    "institution": "`banque_populaire_francaise`, `cooperative_tunisienne_credit`, `maison_francaise` (the "
                   "consumers' cooperative « La Maison Française », called « Société coopérative de consommation » in "
                   "sgt1927)",
    "institution_fr": "institution as named in the title",
    "date_fr": "balance date as printed (empty: not printed)",
    "statement": "`balance_sheet` (bilan) or `profit_loss` (compte de profits et pertes, Banque populaire only)",
    "side": "`assets` (actif) / `liabilities` (passif); `debit` / `credit` for the profit and loss account",
    "line_no": "order of the line within its side as printed (subtotals and totals not counted)",
    "line_type": "`item` (a line of the side; the items add up to the side total) or `detail` (sgt1928 Banque "
                 "populaire: movements printed in a brace inside an item: balance of the previous year, entries, "
                 "exits; not part of the side total)",
    "item": "English code of the line (shared by equivalent lines of different editions; place suffixes "
            "_tunis/_la_goulette/_franceville for the branches of « La Maison Française »)",
    "item_fr": "label as printed; nested headings joined with ' : ' (ditto dashes written out)",
    "unit": "francs", "value": "printed value (» = 0; centimes as decimals)",
    "flag": "empty or `total_mismatch` (printed cell contradicted by the printed sum it enters)",
}
BAL_SPEC = dict(
    secs=["bilan", "pl"],
    dims=["institution", "institution_fr", "date_fr", "statement", "side", "line_no", "line_type", "item", "item_fr",
          "unit"],
    title_fr="Banques populaires : bilans de la Banque populaire française de Tunisie (et compte de profits et "
             "pertes) et de la Coopérative tunisienne de crédit ; Sociétés coopératives de consommation : bilan de "
             "« La Maison Française »",
    title_en="Balance sheets of the Banque populaire française de Tunisie (with its profit and loss account), the "
             "Coopérative tunisienne de crédit and the consumers' cooperative « La Maison Française », sgt1926-sgt1930",
    paras=[
        "Printed at the end of the chapter *Mutualité agricole et commerciale* in sgt1926-sgt1930 (not before; not in "
        "sgt1935 or later). One balance per institution and edition (SPEC_ADDENDUM rule 5), stored line by line in "
        "printed order with `side` and `statement`. Banque populaire française: balance at 31 December of the edition "
        "year and its compte de profits et pertes. Coopérative tunisienne de crédit: balance at 31 December. « La "
        "Maison Française »: balance at 11 April 1926 (exercice 1925-1926), at 24 April 1927 (exercice 1926-1927), "
        "then without a date in sgt1928-sgt1930; sgt1930 reprints the sgt1929 balance unchanged (both kept, as "
        "printed in each edition).",
        "Group figures printed in an outer column (« La Maison Française »: valeurs réalisables, disponibles, "
        "immobilisées ...; Banque populaire 1928 réserves) and the side totals are checks, not rows. Checks: each "
        "group figure = its lines; each side total = its items; assets = liabilities and debit = credit; the "
        "Banque populaire bénéfice net (profit and loss) = profits et pertes (liabilities); for the sgt1928 brace "
        "movements, printed sum = previous balance + entries and balance = printed sum - exits.",
        "Item codes are translations of the printed lines; labels change between editions (e.g. Effets escomptés "
        "1926 / Effets à recevoir 1927-1930 are both `bills_*` codes as printed), so codes follow the label, not a "
        "harmonised chart of accounts. The asset line « Résultat d'inventaire » of « La Maison Française » "
        "(1928-1930) is a loss; its liability « Solde ou bénéfice net » (1926) a profit."],
)
BAL_FAIL = (
    "sgt1928 Banque populaire, comptes-courant: the solde de l'exercice précédent is printed 565.731,84 (2.5x crop), "
    "10 more than the printed sum 13.710.898,43 minus the avances 13.145.176,59 and than the comptes courants "
    "565.721,84 of the sgt1927 balance: flagged `total_mismatch`. « La Maison Française », valeurs immobilisées: "
    "sgt1928 group figure 967.961,94 for four lines giving 956.977,66 (10.984,28 short; a blank line stands between "
    "Mobilier et Matériel and Titres et Valeurs, an item evidently dropped); sgt1929 and its reprint sgt1930 "
    "1.038.953,09 for six lines giving 990.488,49 (48.464,60 short, no line identifiable); in all three the group "
    "figure gives the side total. Coopérative tunisienne de crédit: sgt1929 passif lines give 6.436.403,15 for the "
    "printed total 6.438.403,15 (2.000 short; the actif adds up); sgt1930 actif lines give 8.058.412,30 (only three "
    "lines printed: 80.000 short) and passif lines 8.138.403,30 (9,00 short) for the printed totals 8.138.412,30. "
    "Banque populaire passif totals: sgt1928 printed 9.241.999,30 for items giving 9.241.999,35 (0,05; the actif "
    "total 9.241.999,30 equals it) and sgt1929 printed 12.404.456,46 for items giving 12.404.466,46 (10,00; equal to "
    "the printed actif total); every item re-read on the crop. "
    "None of these can be assigned to one cell, so no flag.")


def build_extra(secs, res, write):
    chk_bilan_sides()
    groups = [("mutuality_balance_sheets", BAL_SPEC, cells_bilan, BAL_DOC, BAL_FAIL,
               "Unit: francs (centimes as decimals); suggested value_type: francs.")]
    groups += [(o, sp, cells_acc, EARLY_DOC, "", "Unit: accidents; suggested value_type: count.")
               for o, sp in EARLY.items()]
    for out, spec, fn, doc, fail, unit in groups:
        ss = [s for s in secs if s["table"] in spec["secs"]]
        spec["_eds"] = [e for e in ORDER if any(s["ed"] == e for s in ss)]
        kept = []
        for s in ss:
            kept += fn(s)
        flagged = [f"{r['census']} {r['year']} {r.get('item_fr', r.get('category_fr'))} = {r['value']} ({r['flag']})"
                   for r in kept if r["flag"]]
        res[out] = dict(rows=len(kept), checks=CHK.n[out], failed=list(CHK.fail[out]), overlap_compared=0,
                        overlap_diffs=[], flagged=flagged, editions=spec["_eds"])
        if write:
            cols = COMMON + spec["dims"] + ["value", "flag"]
            write_csv(out, cols, kept)
            expl = (["Every failed check below was re-read on a native-resolution crop: the printed values are kept. "
                     + fail] if CHK.fail[out] else [])
            paras = spec["paras"] + expl + ["Survey of the whole chapter in every edition: `mutuality_survey.md`."]
            write_notes(out, CHAPTER, SCRIPT, kept, cols, {c: doc.get(c) or DOC[c] for c in cols}, spec["title_fr"],
                        spec["title_en"], paras, CHK.n[out], CHK.fail[out], 0, [], coverage_lines(ss),
                        RULE5, unit)



def build(write=True):
    secs = []
    for ed in ORDER:
        p = TR / f"{PREFIX}_{ed}.txt"
        if p.exists():
            secs += parse(p, ed)
    for s in secs:
        f = CHECKS.get(s["table"])
        if f:
            f(s)
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
            if spec.get("post"):
                kept = spec["post"](kept, recs, spec["key"])
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
                "Survey of the whole chapter in every edition: `mutuality_survey.md`."]
            write_notes(out, CHAPTER, SCRIPT, kept, cols, {c: spec.get("doc", {}).get(c) or DOC[c] for c in cols},
                        spec["title_fr"], spec["title_en"], paras, CHK.n[out], CHK.fail[out], n, diffs,
                        coverage_lines(ss), RULE5 if spec.get("rule5") else RULE4, spec["unit"])
    build_extra(secs, res, write)
    if write:
        write_validation(OUT / f"{PREFIX}_validation.json", dict(res, _chapter_views=CHAPTER_VIEWS, _survey=SURVEY,
                                                                 _not_transcribed=NOT_DONE))
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
