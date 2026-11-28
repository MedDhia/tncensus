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
            "Office public de crédit agricole indigène (sgt1929 f495, sgt1930 f1031, sgt1935 f310). "
            "NOT yet transcribed: sociétés "
            "indigènes / tunisiennes de prévoyance (sgt1922 f464|f465, sgt1923 f954|f955, sgt1924 f1452|f1453, "
            "sgt1925 f522|f523, sgt1926 f1030|f1031, sgt1927 f494|f495, sgt1928 f1022|f1023, sgt1929 f500|f501, "
            "sgt1930 f1036|f1037, sgt1935 f316|f317, sgt1936 f185|f186, sgt1939 f160|f161); bilans of the Banque populaire "
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
