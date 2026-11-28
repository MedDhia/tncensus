#!/usr/bin/env python3
"""Property chapter (chapter VI *Propriété immobilière* up to sgt1930; chapter VI *Tribunal mixte* in sgt1935;
chapter V *Propriété foncière* in sgt1936 and sgt1939) of the Statistique générale de la Tunisie, 12 editions
sgt1922-sgt1939: works of the Tribunal mixte immobilier (cases, pending registration requisitions, results of the
registration proceedings: legal status and charges, urban / rural properties, areas, oppositions, claimants) and
the Conservation de la propriété foncière (registration requisitions, titles issued, recapitulation, enzel rents
and mortgage claims registered, sgt1939 transfers inter vivos).

  python3 extract_property.py check   parse the transcriptions, run every check, print failures
  python3 extract_property.py build   ... and write csv/property_*.csv, their .md notes, csv/property_survey.md
                                      and csv/property_validation.json

Source of truth: transcribed/property_<edition>.txt (format in yb_tables.py; areas in hectares as decimals,
money in francs with centimes). The Conservation foncière yearly series (requisitions by nationality, by declared
value, titles issued) are printed for overlapping year windows (SPEC_ADDENDUM rule 4: each year from the latest
edition printing it, every other printing compared); every other table is printed once per edition for the edition
year (rule 5). Printed totals are used for checks only (the recapitulation, a table of cumulative totals, is
stored).
"""
import sys
from collections import defaultdict
from decimal import Decimal

from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parent))  # shared helper yb_tables.py
from yb_tables import (COMMON, EDITIONS, ORDER, OUT, TR, Checks, coverage_lines, is_total, parse, select_latest,
                       ssum, where, write_csv, write_notes, write_validation)

CHAPTER = "Propriété immobilière / Tribunal mixte / Propriété foncière"
SCRIPT = "extract_property.py"
TOPIC2OUT = {"cases": "property_tribunal_cases", "pending": "property_pending_requisitions",
             "legal_status": "property_results_legal_status", "location": "property_results_location",
             "charges": "property_results_charges", "areas": "property_results_areas",
             "oppositions": "property_oppositions", "claimants": "property_claimants",
             "requisitions": "property_requisitions", "value_brackets": "property_requisitions_value",
             "titles": "property_titles", "recap": "property_conservation_recap",
             "transfers": "property_transfers_1939"}


class _Checks(Checks):
    def eq(self, topic, what, got, printed, tol=Decimal(0)):
        super().eq(TOPIC2OUT[topic], what, got, printed, tol)


CHK = _Checks()
Q4 = Decimal("0.0001")

# Views of the chapter (chapter title .. last view before the next chapter), confirmed on the images.
CHAPTER_VIEWS = {
    "sgt1922": (103, 112), "sgt1923": (587, 596), "sgt1924": (1077, 1086), "sgt1925": (113, 122),
    "sgt1926": (665, 672), "sgt1927": (127, 134), "sgt1928": (651, 658), "sgt1929": (129, 136),
    "sgt1930": (663, 670), "sgt1935": (91, 98), "sgt1936": (62, 67), "sgt1939": (57, 64),
}

# ----------------------------------------------------------------- labels

SEAT = {"tunis": ("tunis", "Siège de Tunis"), "sousse": ("sousse", "Siège de Sousse")}
OUTCOME = {"imm": ("registration", "Immatriculation"), "rej": ("rejection", "Rejet"),
           "rad": ("radiation", "Radiation")}
OUTCOME_AREA = {"imm": ("registered", "Surfaces immatriculées"),
                "ref": ("refused_or_abandoned", "Surfaces dont l'immatriculation a été refusée par le Tribunal ou "
                                                "abandonnée par les parties")}
OUTCOME_CLAIM = {"imm": ("registration_obtained", "Qui ont obtenu l'immatriculation"),
                 "rej": ("requisition_rejected", "Dont la réquisition a été rejetée"),
                 "ren": ("requisition_renounced", "Qui ont renoncé à leur réquisition")}
STATUS = {"melk": "melk", "enzel": "enzel", "habous": "habous"}
LOCATION = {"urban": ("urban", "Immeubles urbains"), "rural": ("rural", "Immeubles ruraux")}

CASES_M = {
    "pending_start": "Restant au 31 décembre de l'année précédente / Affaires en cours au 31 décembre de l'année "
                     "précédente",
    "entered": "Entrées pendant l'année / Réquisitions reçues (affaires entrées) pendant l'année",
    "judged": "Jugées pendant l'année / Affaires jugées pendant l'année",
    "pending_end": "Restant à juger au 31 décembre / Affaires en cours au 31 décembre",
    "requisitions": "1° Réquisitions d'immatriculation dont le Tribunal mixte a été saisi depuis le 1er janvier",
    "hearings": "2° Audiences tenues depuis le 1er janvier",
    "judg_registration": "3° Jugements définitifs : a) prononçant l'immatriculation",
    "judg_rejection": "3° Jugements définitifs : b) prononçant le rejet de la réquisition",
    "judg_radiation": "3° Jugements définitifs : c) prononçant la radiation de la réquisition à la demande des "
                      "parties",
    "interlocutory": "4° Jugements avant faire droit, ordonnant des mesures préparatoires ou des justifications "
                     "complémentaires",
    "rectification": "5° Jugements sur requête tendant à la rectification d'erreurs matérielles (décrets des 15 "
                     "février et 19 mars 1897)",
    "inspections": "6° Enquêtes sur les lieux effectuées par les magistrats",
    "expertises": "7° Expertises effectuées par des hommes de l'art",
}

PENDING_M = {
    "I.1": "I. Réquisitions en suspens pour des causes indépendantes du Tribunal mixte : 1° Procédure préliminaire "
           "de publicité et de bornage en cours à la Conservation de la Propriété foncière et au Service "
           "topographique",
    "I.2": "I. Réquisitions en suspens : 2° Instances pendantes devant une autre juridiction",
    "I.3": "I. Réquisitions en suspens : 3° Causes diverses (établissement du plan définitif par le Service "
           "topographique ; bornage complémentaire ; nouvelle publicité, etc.)",
    "II.1": "II. Réquisitions à l'instruction après accomplissement des formalités préliminaires de publicité et de "
            "bornage ou après un jugement avant faire droit : 1° Procédure d'oppositions en cours, recherches et "
            "formalités diverses en vue du renvoi à l'audience",
    "II.2": "II. Réquisitions à l'instruction : 2° Exécution de mesures préparatoires ordonnées par jugement",
    "III.1": "III. Réquisitions à l'audience : 1° Fixées au rôle",
    "III.2": "III. Réquisitions à l'audience : 2° En délibéré",
    "III": "III. Réquisitions à l'audience (fixées au rôle ou en délibéré)",
    "V": "V. Requêtes pour rectifications d'erreurs matérielles (décrets des 25 février et 19 mars 1897)",
}
JUDGE_GROUP = {"T": ("rapporteur_tunis", "Juges rapporteurs, siège de Tunis"),
               "S": ("rapporteur_sousse", "Juges rapporteurs, siège de Sousse"),
               "D": ("delegated", "Magistrats du siège délégués à l'instruction par le Président en remplacement "
                                  "d'un juge rapporteur empêché (art. 6 du décret du 30 avril 1903)"),
               "C": ("commissioned", "Magistrats du siège spécialement commis par jugement pour certaines "
                                     "formalités ou enquêtes"),
               "M": ("delegated_or_commissioned", "Magistrats du siège délégués à l'instruction par le Président en "
                                                  "remplacement d'un juge rapporteur empêché ou spécialement commis "
                                                  "par jugement pour certaines formalités ou enquêtes (art. 6 du "
                                                  "décret du 30 avril 1903)"),
               "seat": ("seat", "Siège")}

OPPOSITION = {"accepted": "accueillies", "rejected": "rejetées", "withdrawn": "suivies de désistement",
              "not_ruled": "sur lesquelles il n'a pas été statué",
              "referred": "renvoyées devant les juridictions de droit commun"}
CLAIMANT = {"owners": "Propriétaires ou co-propriétaires", "enzel_holders": "Enzélistes ou co-enzélistes",
            "real_right_holders": "Détenteurs de droits réels divers (art. 22 de la loi foncière)"}
NATIONALITY = {"Français": "french", "Italiens": "italian", "Anglais": "british", "Grecs": "greek",
               "Tunisiens": "tunisian", "Allemands": "german", "Espagnols": "spanish", "Divers": "other",
               "Suisses": "swiss", "Belges": "belgian", "Étrangers": "foreign", "Etrangers": "foreign"}
CHARGE = {"enzel_registered": ("enzel_rent", "registered", "Montant des rentes d'enzel : inscrites"),
          "enzel_declared": ("enzel_rent", "declared", "Montant des rentes d'enzel : déclarées"),
          "mortgage_registered": ("mortgage", "registered", "Montant des hypothèques : inscrites"),
          "mortgage_declared": ("mortgage", "declared", "Montant des hypothèques : déclarées")}

REQ_M = {"french": ("Français", "count"), "foreign": ("Étrangers", "count"), "tunisian": ("Tunisiens", "count"),
         "number": ("Nombre", "count"), "area": ("Contenances déclarées (hectares)", "hectares"),
         "value": ("Valeurs déclarées (francs)", "francs")}
BRACKET = {"le_3000": "De 3.000 fr. et au-dessous", "3001_12000": "De 3.001 fr. à 12.000",
           "12001_60000": "De 12.001 fr. à 60.000", "ge_60001": "De 60.001 fr. et au-dessus"}
TITLE_M = {"total_titles": ("Nombre total des titres délivrés", "count"),
           "subdivision": ("Titres provenant de lotissements", "count"),
           "judgment": ("Titres délivrés en suite d'un jugement d'immatriculation : nombre", "count"),
           "area": ("Titres délivrés en suite d'un jugement d'immatriculation : contenance définitive (hectares)",
                    "hectares"),
           "value": ("Titres délivrés en suite d'un jugement d'immatriculation : valeur définitive (francs)",
                     "francs")}
RECAP_M = {"demands": ("Nombre de demandes déposées", "count"),
           "area_declared": ("Contenances déclarées (hectares)", "hectares"),
           "value_declared": ("Valeurs déclarées (francs)", "francs"),
           "solved": ("Nombre de demandes ayant reçu une solution définitive", "count"),
           "area_registered": ("Contenance des immeubles immatriculés (hectares)", "hectares"),
           "value_registered": ("Valeur (francs)", "francs"),
           "titles_established": ("Nombre de titres établis", "count"),
           "titles_mutation": ("Titres nouveaux créés par suite de mutation partielle", "count"),
           "titles_total": ("Nombre total des titres au 31 décembre", "count"),
           "enzel_rents": ("Rentes d'enzel inscrites au 31 décembre", "francs"),
           "mortgage_claims": ("Créances hypothécaires inscrites au 31 décembre", "francs")}


def period(label):
    if "-" in label:
        a, b = label.split("-")
        return None, label, f"De {a} à {b}"
    return int(label), label, label


def dl(sec):
    """data lines (not printed totals)"""
    return [r for r in sec["rows"] if "cells" in r and not is_total(r["label"])]


def row(sec, label):
    for r in sec["rows"]:
        if r["label"] == label:
            return r["cells"]
    return None


def val(c):
    return None if c is None else c.value


# ----------------------------------------------------------------- checks

FAILREC = []   # (edition, section, 'row'|'col', row label or column, difference printed - cells)


def _rec_fail(sec, kind, key, got, printed):
    if got is not None and printed is not None and got != printed:
        FAILREC.append((sec["ed"], sec["table"], kind, key, printed - got))


def chk_rowsum(t, sec, target, parts, rows=None):
    for r in sec["rows"]:
        if "cells" not in r or (rows is not None and r["label"] not in rows):
            continue
        c = r["cells"]
        if c[target].value is None:
            continue
        got = ssum(c[p].value for p in parts)
        CHK.eq(t, f"{where(sec)} {r['label']}: {target} = {' + '.join(parts)}", got, c[target].value)
        if not is_total(r["label"]):
            _rec_fail(sec, "row", r["label"], got, c[target].value)


def chk_total_line(t, sec, label, rows, cols):
    tot = row(sec, label)
    if tot is None:
        return
    for c in cols:
        if tot[c].value is None:
            continue
        got = ssum(row(sec, r)[c].value for r in rows)
        CHK.eq(t, f"{where(sec)} {c}: lines vs {label}", got, tot[c].value)
        _rec_fail(sec, "col", c, got, tot[c].value)


def chk_pairs(t, sec, label, src_label, pairs):
    """brace totals: label[first] = src_label[first] + src_label[second]"""
    p = row(sec, label)
    s = row(sec, src_label)
    if p is None or s is None:
        return
    for a, b in pairs:
        CHK.eq(t, f"{where(sec)} {label} {a}+{b}", ssum([s[a].value, s[b].value]), p[a].value)


def pairs_of(cols):
    out = []
    groups = defaultdict(list)
    for c in cols:
        if "." in c:
            groups[c.split(".")[0]].append(c)
    for g, cs in groups.items():
        if len(cs) == 2:
            out.append(tuple(cs))
    return out


def chk_cases(sec):
    t = "cases"
    g = {r["label"]: r["cells"] for r in sec["rows"]}
    for s in ("tunis", "sousse"):
        if "pending_end" in g:
            CHK.eq(t, f"{where(sec)} {s}: pending_end = pending_start + entered - judged",
                   ssum([g["pending_start"][s].value, g["entered"][s].value, -g["judged"][s].value]),
                   g["pending_end"][s].value)
        if "Total@in" in g:
            CHK.eq(t, f"{where(sec)} {s}: Total = pending_start + entered",
                   ssum([g["pending_start"][s].value, g["entered"][s].value]), g["Total@in"][s].value)
        if "Total@out" in g:
            CHK.eq(t, f"{where(sec)} {s}: Total = judged + pending_end",
                   ssum([g["judged"][s].value, g["pending_end"][s].value]), g["Total@out"][s].value)
    for lab, rows_ in (("Total@all", ["pending_start", "entered"]), ("Total@judged", ["judged"]),
                       ("Total@pending", ["pending_end"])):
        if lab in g:
            CHK.eq(t, f"{where(sec)} {lab}", ssum(g[r][s].value for r in rows_ for s in ("tunis", "sousse")),
                   g[lab]["tunis"].value)


def chk_activity(sec, cases):
    t = "cases"
    chk_rowsum(t, sec, "total", ["tunis", "sousse"])
    g = {r["label"]: r["cells"] for r in sec["rows"]}
    jl = [x for x in ("judg_registration", "judg_rejection", "judg_radiation") if x in g]
    if "Total@judgments" in g:
        CHK.eq(t, f"{where(sec)} Total jugements définitifs", ssum(g[x][s].value for x in jl for s in ("tunis", "sousse")),
               g["Total@judgments"]["total"].value)
    if cases is not None:
        c = {r["label"]: r["cells"] for r in cases["rows"]}
        for s in ("tunis", "sousse"):
            CHK.eq(t, f"{where(sec)} {s}: cases judged = jugements définitifs a + b + c",
                   ssum(g[x][s].value for x in jl), c["judged"][s].value)


def judge_cols(sec):
    return [c for c in sec["cols"] if c not in ("partial", "general")]


def chk_pending(sec):
    t = "pending"
    jc = judge_cols(sec)
    chk_rowsum(t, sec, "partial", jc)
    chk_total_line(t, sec, "Total", [r["label"] for r in dl(sec) if r["label"] != "V"], sec["cols"])


def chk_pending_groups(sec, pend):
    t = "pending"
    g = {r["label"]: r["cells"]["general"].value for r in sec["rows"]}
    p = {r["label"]: r["cells"]["partial"].value for r in dl(pend)}
    for grp, v in g.items():
        CHK.eq(t, f"{where(sec)} group {grp} = sum of its lines",
               ssum(x for k, x in p.items() if k == grp or k.startswith(grp + ".")), v)


def chk_pending_age(sec, pend):
    t = "pending"
    jc = judge_cols(sec)
    chk_rowsum(t, sec, "partial", jc)
    chk_total_line(t, sec, "Total", [r["label"] for r in dl(sec) if r["label"] != "V"], sec["cols"])
    if pend is not None and row(pend, "Total") is not None and row(sec, "Total") is not None:
        for c in sec["cols"]:
            CHK.eq(t, f"{where(sec)} {c}: Total IV = Total I-III", row(pend, "Total")[c].value,
                   row(sec, "Total")[c].value)


def chk_grid(t, sec):
    """row total column, total lines (blocks of lines between total lines), brace pair totals, total général."""
    cols = [c for c in sec["cols"] if c != "total"]
    if "total" in sec["cols"]:
        chk_rowsum(t, sec, "total", cols)
    block, blocks = [], []
    last_total = None
    for r in sec["rows"]:
        if "cells" not in r:
            continue
        lab = r["label"]
        if lab.startswith("Total@pair"):
            chk_pairs(t, sec, lab, last_total, pairs_of(sec["cols"]))
        elif lab.startswith("Total général"):
            for c in sec["cols"]:
                if r["cells"][c].value is not None:
                    CHK.eq(t, f"{where(sec)} {c}: Total général = sum of total lines",
                           ssum(row(sec, b)[c].value for b in blocks), r["cells"][c].value)
        elif lab.startswith("Total@"):
            continue
        elif is_total(lab):
            chk_total_line(t, sec, lab, block, sec["cols"])
            blocks.append(lab)
            last_total = lab
            block = []
        else:
            block.append(lab)


def chk_charges(sec):
    t = "charges"
    chk_rowsum(t, sec, "total", [c for c in sec["cols"] if c != "total"])


def chk_charges_summary(sec, legal, charges):
    t = "charges"
    g = {r["label"]: r["cells"]["value"].value for r in sec["rows"]}
    if legal is not None and "n_properties" in g:
        CHK.eq(t, f"{where(sec)} nombre total des immeubles = a) Totaux", row(legal, "Total")["total"].value,
               g["n_properties"])
    for lab, src in (("Total enzel", "enzel_registered"), ("Total mortgage", "mortgage_registered")):
        if lab in g and charges is not None:
            CHK.eq(t, f"{where(sec)} {lab} = {src} total", row(charges, src)["total"].value, g[lab])


def chk_location_vs_legal(sec, legal):
    t = "location"
    if legal is None:
        return
    for st in STATUS:
        lr = row(legal, st)
        for c in legal["cols"]:
            u, r_ = row(sec, f"urban.{st}"), row(sec, f"rural.{st}")
            CHK.eq(t, f"{where(sec)} {st} {c}: urban + rural = a)", ssum([u[c].value, r_[c].value]), lr[c].value)


def chk_series(t, sec):
    if t == "requisitions":
        chk_rowsum(t, sec, "number", ["french", "foreign", "tunisian"])
    if t == "value_brackets":
        chk_rowsum(t, sec, "total", list(BRACKET))
    if t == "titles":
        chk_rowsum(t, sec, "total_titles", ["subdivision", "judgment"])
    chk_total_line(t, sec, "Totaux", [r["label"] for r in dl(sec)], sec["cols"])


def chk_cross_series(secs_by_table, ed):
    req = secs_by_table.get(("requisitions", ed))
    vb = secs_by_table.get(("value_brackets", ed))
    ti = secs_by_table.get(("titles", ed))
    rc = secs_by_table.get(("recap", ed))
    if req and vb:
        for r in dl(vb):
            CHK.eq("value_brackets", f"{where(vb)} {r['label']}: total = a) number",
                   row(req, r["label"])["number"].value, r["cells"]["total"].value)
    if rc:
        c = dl(rc)[0]["cells"]
        pairs = []
        if req:
            pairs += [("demands", req, "number"), ("area_declared", req, "area"), ("value_declared", req, "value")]
        if ti:
            pairs += [("area_registered", ti, "area"), ("value_registered", ti, "value"),
                      ("titles_established", ti, "judgment"), ("titles_mutation", ti, "subdivision"),
                      ("titles_total", ti, "total_titles")]
        for m, s, col in pairs:
            if m not in c or row(s, "Totaux") is None:
                continue
            tot = row(s, "Totaux")[col].value
            got = c[m].value
            if m.startswith("area") and got is not None and tot is not None and got == got.to_integral_value():
                tot = tot.to_integral_value(rounding="ROUND_DOWN")
            CHK.eq("recap", f"{where(rc)} {m} = {s['table']} Totaux {col}", tot, got)


# ----------------------------------------------------------------- cells

def base(sec):
    return {"census": sec["ed"], "table_id": sec["table"], "gallica_ark": sec["ark"], "source_page": sec["page"],
            "gallica_view": sec["view"], "year": int(sec["year"]) if sec.get("year") else None}


def rec(sec, r, col, **dims):
    c = r["cells"][col]
    return dict(base(sec), **dims, value=c.value, flag=c.flag, _row=r["label"], _col=col)


def cells_cases(sec):
    out = []
    for r in dl(sec):
        for s in ("tunis", "sousse"):
            out.append(rec(sec, r, s, seat=s, seat_fr=SEAT[s][1], measure=r["label"],
                           measure_fr=CASES_M[r["label"]]))
    return out


def cells_pending(sec):
    out = []
    heads = sec.get("heads", "").split()
    jc = judge_cols(sec)
    hd = dict(zip(jc, heads)) if heads else {}
    for r in dl(sec):
        lab = r["label"]
        if sec["table"] == "pending_age" and lab != "V":
            cat, cat_fr = "IV", f"IV. Nombre de réquisitions remontant à l'année {lab}"
            fy = lab
        else:
            cat, cat_fr, fy = lab, PENDING_M[lab], ""
        for c in jc:
            g, j = c.split(".")
            out.append(rec(sec, r, c, category=cat, category_fr=cat_fr, filing_year=fy,
                           judge_group=JUDGE_GROUP[g][0], judge_group_fr=JUDGE_GROUP[g][1], judge=j,
                           judge_fr=hd.get(c, j)))
    return out


def cells_legal(sec):
    out = []
    for r in dl(sec):
        for c in sec["cols"]:
            if c == "total":
                continue
            o, s = c.split(".")
            out.append(rec(sec, r, c, legal_status=r["label"], legal_status_fr=r["label"], outcome=OUTCOME[o][0],
                           outcome_fr=OUTCOME[o][1], seat=s, seat_fr=s.capitalize()))
    return out


def cells_location(sec):
    out = []
    for r in dl(sec):
        loc, st = r["label"].split(".")
        for c in sec["cols"]:
            if c == "total":
                continue
            o, s = c.split(".")
            out.append(rec(sec, r, c, location=loc, location_fr=LOCATION[loc][1], legal_status=st,
                           legal_status_fr=st, outcome=OUTCOME[o][0], outcome_fr=OUTCOME[o][1], seat=s,
                           seat_fr=s.capitalize()))
    return out


def cells_areas(sec):
    out = []
    for r in dl(sec):
        loc, st = r["label"].split(".")
        for c in sec["cols"]:
            if c == "total":
                continue
            o, s = c.split(".")
            x = rec(sec, r, c, location=loc, location_fr=LOCATION[loc][1], legal_status=st, legal_status_fr=st,
                    outcome=OUTCOME_AREA[o][0], outcome_fr=OUTCOME_AREA[o][1], seat=s, seat_fr=s.capitalize())
            if x["value"] is not None:
                x["value"] = x["value"].quantize(Q4)
            out.append(x)
    return out


def cells_charges(sec):
    out = []
    for r in dl(sec):
        ch, kind, fr = CHARGE[r["label"]]
        for c in sec["cols"]:
            if c == "total":
                continue
            o, s = c.split(".")
            out.append(rec(sec, r, c, charge=ch, amount=kind, measure_fr=fr, outcome=OUTCOME[o][0],
                           outcome_fr=OUTCOME[o][1], seat=s, seat_fr=s.capitalize(), unit="francs"))
    return out


def cells_charges_summary(sec):
    out = []
    for r in dl(sec):
        if r["label"].startswith("mortgage_titles_"):
            s = r["label"].split("_")[-1]
            out.append(rec(sec, r, "value", charge="mortgage", amount="titles",
                           measure_fr="Les hypothèques se répartissent sur … titres", outcome="", outcome_fr="",
                           seat=s, seat_fr=s.capitalize(), unit="titles"))
    return out


def cells_oppositions(sec):
    out = []
    for r in dl(sec):
        for s in ("tunis", "sousse"):
            out.append(rec(sec, r, s, decision=r["label"], decision_fr=OPPOSITION[r["label"]], seat=s,
                           seat_fr=s.capitalize()))
    return out


def cells_claimants(sec):
    out = []
    nat = sec["table"] == "claimant_nationality"
    for r in dl(sec):
        for c in sec["cols"]:
            if c == "total":
                continue
            o, s = c.split(".")
            if nat:
                dims = dict(nationality=NATIONALITY[r["label"]], nationality_fr=r["label"])
            else:
                dims = dict(legal_quality=r["label"], legal_quality_fr=CLAIMANT[r["label"]])
            out.append(rec(sec, r, c, **dims, outcome=OUTCOME_CLAIM[o][0], outcome_fr=OUTCOME_CLAIM[o][1], seat=s,
                           seat_fr=s.capitalize()))
    return out


def cells_series(sec):
    out = []
    t = sec["table"]
    for r in dl(sec):
        y, p, pfr = period(r["label"])
        for c in sec["cols"]:
            if t == "value_brackets":
                if c == "total":
                    continue
                m_fr, unit = BRACKET[c], "count"
            elif t == "requisitions":
                if c == "number":
                    continue
                m_fr, unit = REQ_M[c]
            else:
                m_fr, unit = TITLE_M[c]
            x = rec(sec, r, c, period=p, period_fr=pfr, measure=c, measure_fr=m_fr, unit=unit)
            x["year"] = y
            if unit == "hectares" and x["value"] is not None and t == "titles":
                x["value"] = x["value"].quantize(Q4)
            out.append(x)
    return out


def cells_recap(sec):
    out = []
    for r in dl(sec):
        for c in sec["cols"]:
            m_fr, unit = RECAP_M[r["label"] if c == "value" else c]
            m = r["label"] if c == "value" else c
            out.append(rec(sec, r, c, measure=m, measure_fr=m_fr, unit=unit))
    return out


# ----------------------------------------------------------------- tables

T_DOC = {
    "census": "edition the value is taken from (`sgt1922` … `sgt1939`)",
    "gallica_ark": "Gallica volume ark (views are numbered within a volume)",
    "source_page": "printed page number",
    "gallica_view": "Gallica view (fNNNN)",
    "year": "year of the figures (the edition year: each edition prints the table for its own year)",
    "seat": "`tunis` or `sousse` (siège of the Tribunal mixte)",
    "seat_fr": "as printed",
    "outcome": "result of the registration proceeding",
    "outcome_fr": "printed column heading",
    "legal_status": "`melk` (freehold), `enzel` (perpetual-rent tenure), `habous` (mortmain endowment)",
    "legal_status_fr": "as printed",
    "location": "`urban` or `rural`",
    "location_fr": "as printed",
    "flag": "empty, or `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable` (SPEC.md)",
}

RULE5 = ("Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, with "
         "`year`; no year is printed by two editions.")
RULE4 = ("Printed for overlapping year windows: each year (and the opening multi-year period) is taken from the "
         "**latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing "
         "is compared below.")

TABLES = {
    "property_tribunal_cases": dict(
        secs=["cases", "activity"], cells={"cases": cells_cases, "activity": cells_cases},
        key=["year", "seat", "measure"], dims=["seat", "seat_fr", "measure", "measure_fr"], topic="cases",
        title_fr="Tribunal mixte. Travaux du Tribunal : a) Statistique des affaires",
        title_en="Tribunal mixte (land registration court): cases and work of the court, by seat",
        unit="Unit: number of cases (affaires, réquisitions), hearings, judgments, inspections, expert reports.",
        doc={"table_id": "transcription section: `cases` (upper part: cases pending, entered, judged), `activity` "
                         "(lower part: requisitions, hearings, judgments, inspections, expert reports)",
             "measure": "`pending_start`, `entered`, `judged`, `pending_end` (cases); `requisitions`, `hearings`, "
                        "`judg_registration`, `judg_rejection`, `judg_radiation`, `interlocutory`, `rectification`, "
                        "`inspections`, `expertises`",
             "measure_fr": "printed line heading (the wording of the upper part changes in sgt1925; both given)",
             "value": "count"},
        paras=[]),
    "property_pending_requisitions": dict(
        secs=["pending", "pending_age"], cells={"pending": cells_pending, "pending_age": cells_pending},
        key=["year", "category", "filing_year", "judge_group", "judge"],
        dims=["category", "category_fr", "filing_year", "judge_group", "judge_group_fr", "judge", "judge_fr"],
        topic="pending",
        title_fr="Tribunal mixte. b) Situation des affaires d'immatriculation en cours au 31 décembre",
        title_en="Tribunal mixte: registration requisitions pending at 31 December, by stage of the proceeding "
                 "and by year of filing, by judge",
        unit="Unit: number of requisitions.",
        doc={"table_id": "transcription section: `pending` (I-III and V, by stage), `pending_age` (IV, by year of "
                         "filing)",
             "category": "`I.1` … `III.2` (stage of the proceeding), `IV` (by year of filing), `V` (requests for "
                         "rectification of material errors)",
             "category_fr": "printed line heading",
             "filing_year": "IV only: the year the requisition dates back to, as printed (first line: the year printed "
                            "at its head, the line covering all earlier years where the heading says so)",
             "judge_group": "`rapporteur_tunis`, `rapporteur_sousse` (juges rapporteurs), `delegated` (magistrats "
                            "délégués à l'instruction), `commissioned` (magistrats spécialement commis); `seat` when "
                            "the edition prints seats only",
             "judge_group_fr": "printed column group heading",
             "judge": "column code within the group (judge letter or number as printed; a column printed without "
                      "heading gets its position)",
             "judge_fr": "column heading as printed",
             "value": "count"},
        paras=[]),
    "property_results_legal_status": dict(
        secs=["legal_status"], cells={"legal_status": cells_legal},
        key=["year", "legal_status", "outcome", "seat"],
        dims=["legal_status", "legal_status_fr", "outcome", "outcome_fr", "seat", "seat_fr"], topic="results",
        title_fr="Résultats des instances d'immatriculation. a) État juridique et charge des immeubles (nombre "
                 "d'immeubles)",
        title_en="Results of the registration proceedings: properties by legal status, outcome and seat",
        unit="Unit: number of properties (immeubles).",
        doc={"table_id": "`legal_status`", "value": "number of properties"},
        paras=[]),
    "property_results_charges": dict(
        secs=["charges", "charges_summary"], cells={"charges": cells_charges, "charges_summary": cells_charges_summary},
        key=["year", "charge", "amount", "outcome", "seat"],
        dims=["charge", "amount", "measure_fr", "outcome", "outcome_fr", "seat", "seat_fr", "unit"], topic="charges",
        title_fr="Résultats des instances d'immatriculation. a) État juridique et charge des immeubles (montant des "
                 "rentes d'enzel et des hypothèques)",
        title_en="Results of the registration proceedings: enzel rents and mortgages on the properties, by outcome "
                 "and seat; number of land titles carrying the mortgages",
        unit="Units: francs with centimes (`unit` = `francs`); land titles (`unit` = `titles`). Mixed table.",
        doc={"table_id": "`charges` (amounts) or `charges_summary` (the box under the table)",
             "charge": "`enzel_rent` or `mortgage`",
             "amount": "`registered` (inscrites), `declared` (déclarées); `titles` = number of land titles over which "
                       "the mortgages are spread (*Les hypothèques se répartissent sur … titres à Tunis et … à "
                       "Sousse*)",
             "measure_fr": "printed line heading",
             "unit": "`francs` or `titles`",
             "value": "francs (centimes after the point) or number of titles"},
        paras=[]),
    "property_results_location": dict(
        secs=["location"], cells={"location": cells_location},
        key=["year", "location", "legal_status", "outcome", "seat"],
        dims=["location", "location_fr", "legal_status", "legal_status_fr", "outcome", "outcome_fr", "seat",
              "seat_fr"], topic="results",
        title_fr="Résultats des instances d'immatriculation. b) Situation des immeubles",
        title_en="Results of the registration proceedings: urban and rural properties by legal status, outcome and "
                 "seat",
        unit="Unit: number of properties.", doc={"table_id": "`location`", "value": "number of properties"},
        paras=[]),
    "property_results_areas": dict(
        secs=["areas"], cells={"areas": cells_areas},
        key=["year", "location", "legal_status", "outcome", "seat"],
        dims=["location", "location_fr", "legal_status", "legal_status_fr", "outcome", "outcome_fr", "seat",
              "seat_fr"], topic="areas",
        title_fr="Résultats des instances d'immatriculation. c) Superficies",
        title_en="Results of the registration proceedings: areas registered and areas refused or abandoned, by "
                 "urban / rural, legal status and seat",
        unit="Unit: hectares, as a decimal with four places (printed in hectares, ares and centiares: "
             "\"4 30 43\" = 4.3043 ha).",
        doc={"table_id": "`areas`", "value": "hectares (4 decimals = ares and centiares)"},
        paras=[]),
    "property_oppositions": dict(
        secs=["oppositions"], cells={"oppositions": cells_oppositions},
        key=["year", "decision", "seat"], dims=["decision", "decision_fr", "seat", "seat_fr"], topic="oppositions",
        title_fr="Résultats des instances d'immatriculation. d) Jugement des oppositions",
        title_en="Results of the registration proceedings: oppositions judged, by decision and seat",
        unit="Unit: number of oppositions.",
        doc={"table_id": "`oppositions`",
             "decision": "`accepted`, `rejected`, `withdrawn` (suivies de désistement), `not_ruled` (sur lesquelles il "
                         "n'a pas été statué), `referred` (renvoyées devant les juridictions de droit commun)",
             "decision_fr": "printed line heading", "value": "number of oppositions"},
        paras=[]),
    "property_claimants": dict(
        secs=["claimant_status", "claimant_nationality"],
        cells={"claimant_status": cells_claimants, "claimant_nationality": cells_claimants},
        key=["year", "table_id", "legal_quality", "nationality", "outcome", "seat"],
        dims=["legal_quality", "legal_quality_fr", "nationality", "nationality_fr", "outcome", "outcome_fr", "seat",
              "seat_fr"], topic="claimants",
        title_fr="Résultats des instances d'immatriculation. e) Nombre et qualité juridique, f) Nationalité des "
                 "personnes dont la réquisition a reçu une solution définitive",
        title_en="Results of the registration proceedings: claimants whose requisition was finally decided, by "
                 "legal quality and by nationality, outcome and seat",
        unit="Unit: number of claimants (requérants).",
        doc={"table_id": "`claimant_status` (e, by legal quality) or `claimant_nationality` (f, by nationality); the "
                         "two are alternative breakdowns of the same claimants",
             "legal_quality": "e) only: `owners`, `enzel_holders`, `real_right_holders`",
             "legal_quality_fr": "printed line heading",
             "nationality": "f) only: `french`, `italian`, `british` (*Anglais*), `greek`, `tunisian`, `german`, "
                            "`spanish`, `swiss`, `belgian`, `foreign` (*Étrangers*, sgt1936), `other` (*Divers*)",
             "nationality_fr": "as printed", "value": "number of claimants"},
        paras=[]),
    "property_requisitions": dict(
        secs=["requisitions"], cells={"requisitions": cells_series}, series=True,
        key=["period", "measure"], dims=["period", "period_fr", "measure", "measure_fr", "unit"],
        topic="requisitions",
        title_fr="Conservation foncière. Réquisitions d'immatriculation : a) Nationalité des requérants, nombre, "
                 "contenances et valeurs déclarées",
        title_en="Land registry: registration requisitions filed, by nationality of the claimant, with declared "
                 "areas and values, by year",
        unit="Units: requisitions (`unit` = `count`), hectares (`hectares`), francs (`francs`). Mixed table.",
        doc={"table_id": "`requisitions`",
             "year": "year of the figures; empty for the opening multi-year period",
             "period": "year, or the opening multi-year period (`1886-1909`, from sgt1935 `1886-1932` etc.) as printed",
             "period_fr": "as printed (*De 1886 à 1909*)",
             "measure": "`french`, `foreign`, `tunisian` (number of requisitions by nationality of the claimant), "
                        "`area` (declared area), `value` (declared value)",
             "measure_fr": "printed column heading", "unit": "`count`, `hectares` or `francs`",
             "value": "requisitions, hectares or francs"},
        paras=[]),
    "property_requisitions_value": dict(
        secs=["value_brackets"], cells={"value_brackets": cells_series}, series=True,
        key=["period", "measure"], dims=["period", "period_fr", "measure", "measure_fr", "unit"],
        topic="value_brackets",
        title_fr="Conservation foncière. Réquisitions d'immatriculation : b) Répartition d'après les valeurs "
                 "déclarées",
        title_en="Land registry: registration requisitions by bracket of declared value, by year",
        unit="Unit: number of requisitions.",
        doc={"table_id": "`value_brackets`", "year": "year of the figures; empty for the opening multi-year period",
             "period": "year, or the opening multi-year period as printed", "period_fr": "as printed",
             "measure": "`le_3000`, `3001_12000`, `12001_60000`, `ge_60001` (declared value, francs)",
             "measure_fr": "printed column heading", "unit": "`count`", "value": "number of requisitions"},
        paras=[]),
    "property_titles": dict(
        secs=["titles"], cells={"titles": cells_series}, series=True,
        key=["period", "measure"], dims=["period", "period_fr", "measure", "measure_fr", "unit"], topic="titles",
        title_fr="Conservation foncière. Titres délivrés : nombre, contenances et valeurs définitives",
        title_en="Land registry: land titles issued (total, from subdivisions, after a registration judgment, with "
                 "final area and value), by year",
        unit="Units: titles (`count`), hectares as a decimal with four places (`hectares`; printed h. a. c.), "
             "francs (`francs`). Mixed table.",
        doc={"table_id": "`titles`", "year": "year of the figures; empty for the opening multi-year period",
             "period": "year, or the opening multi-year period as printed", "period_fr": "as printed",
             "measure": "`total_titles`, `subdivision` (titres provenant de lotissements), `judgment` (titles issued "
                        "after a registration judgment), `area` (their final area), `value` (their final value)",
             "measure_fr": "printed column heading", "unit": "`count`, `hectares` or `francs`",
             "value": "titles, hectares or francs"},
        paras=[]),
    "property_conservation_recap": dict(
        secs=["recap", "registered"], cells={"recap": cells_recap, "registered": cells_recap},
        key=["year", "measure"], dims=["measure", "measure_fr", "unit"], topic="recap",
        title_fr="Conservation foncière. Récapitulation : a) Nombre de demandes déposées et de titres créés ; "
                 "b) Rentes d'enzel et créances hypothécaires inscrites",
        title_en="Land registry: cumulative summary at 31 December (requisitions filed and finally decided, titles "
                 "created) and enzel rents and mortgage claims registered",
        unit="Units: count, hectares, francs (`unit`). Mixed table. All figures are cumulative since 1886 at 31 "
             "December of the edition year.",
        doc={"table_id": "`recap` (a) or `registered` (b)",
             "year": "year of the figures (31 December of the edition year)",
             "measure": "`demands`, `area_declared`, `value_declared`, `solved`, `area_registered`, "
                        "`value_registered`, `titles_established`, `titles_mutation`, `titles_total`; `enzel_rents`, "
                        "`mortgage_claims`",
             "measure_fr": "printed heading", "unit": "`count`, `hectares` or `francs`",
             "value": "count, hectares or francs"},
        paras=[]),
}

def cells_transfers(sec):
    out = []
    for r in dl(sec):
        for c in sec["cols"]:
            out.append(rec(sec, r, c, controle_civil=r["label"], measure=c,
                           measure_fr={"number": "Nombre", "value": "Valeur (francs)"}[c],
                           unit={"number": "count", "value": "francs"}[c]))
    return out


TABLES["property_transfers_1939"] = dict(
    secs=["transfers"], cells={"transfers": cells_transfers},
    key=["year", "controle_civil", "measure"], dims=["controle_civil", "measure", "measure_fr", "unit"],
    title_fr="Conservation de la propriété foncière. Mutations entre vifs en 1939 d'immeubles immatriculés",
    title_en="Land registry: transfers inter vivos of registered properties in 1939, by contrôle civil (number and "
             "value)",
    unit="Units: transfers (`unit` = `count`), francs with centimes (`francs`). Mixed table.",
    doc={"table_id": "`transfers`", "controle_civil": "contrôle civil as printed (last line: Territoire Militaire "
                                                      "(Medenine))",
         "measure": "`number` or `value`", "measure_fr": "printed column heading", "unit": "`count` or `francs`",
         "value": "number of transfers or francs"},
    paras=["Printed only in sgt1939 (f63, p. 57)."])

# ----------------------------------------------------------------- flags set by hand
# (edition, section, row label, column) -> (flag, reason). Cells flagged `total_mismatch` automatically: a printed
# cell whose line check and column check both fail by the same amount (the printing error is at that cell; the
# printed value is kept).
D = "derived_from_totals"
FLAGS = {
    ("sgt1935", "requisitions", "1886-1932", "french"): (
        "row_realigned", "Français: 126 is printed on the 1886-1932 line and 5.708 on the 1933 line; with the printed "
        "values neither line gives its Nombre (5.708 + 60 + 261 = 447 needs 126; 126 + 5.134 + 10.329 = 20.871 needs "
        "5.708), and sgt1936 prints 5.834 = 5.708 + 126 for 1886-1933"),
    ("sgt1935", "requisitions", "1933", "french"): ("row_realigned", "see 1886-1932"),
    ("sgt1930", "pending", "III", "T.C"): (
        D, "printed \"7·\" with its second digit broken; 73 from the column total 887 and the line total 228"),
    ("sgt1936", "areas", "urban.enzel", "imm.tunis"): (
        D, "printed \"2.84.·1\" with a broken digit; 2 ha 84 a 51 c from the line total 3.03.46"),
    ("sgt1936", "claimant_nationality", "Français", "rej.tunis"): (
        D, "cell left blank in the printing; 6 from the line total 185 and the column total 68"),
    ("sgt1936", "titles", "1886-1933", "area"): (
        D, "ares and centiares printed \"1· 11\"; 11 a 41 c from the Totaux 1.474.945 22 57"),
}
for _m, _why in (("area", "printed 1.398.823 02 59 ha; the Totaux (1.449.008 42 15) need 1.389.922 46 58, which is also "
                           "sgt1936's 1886-1933 (1.399.899 11 41) less 1933 (9.976 64 83)"),
                  ("value", "printed 359.173.670 fr.; the Totaux (513.080.640) need 383.173.670, which is also sgt1936's "
                            "1886-1933 (413.337.722) less 1933 (30.164.052)")):
    FLAGS[("sgt1935", "titles", "1886-1932", _m)] = ("total_mismatch", _why + "; printed value kept")
for _e in ["sgt1924", "sgt1925", "sgt1926", "sgt1927", "sgt1928", "sgt1929", "sgt1930"]:
    FLAGS[(_e, "requisitions", "1924", "value")] = (
        D, "every printing of 1924 (sgt1924-sgt1930) prints \"17.872 50\", the plate missing a digit; 17.872.150 from "
           "the Totaux of sgt1924 (304.039.499)")


def auto_mismatch():
    """cells whose line check and column check fail by the same amount"""
    rows_ = defaultdict(list)
    cols_ = defaultdict(list)
    for ed, t, kind, key, diff in FAILREC:
        (rows_ if kind == "row" else cols_)[(ed, t)].append((key, diff))
    out = {}
    for k in rows_:
        for lab, d1 in rows_[k]:
            for col, d2 in cols_.get(k, []):
                if d1 == d2:
                    out[(k[0], k[1], lab, col)] = d1
    return out


# ----------------------------------------------------------------- explanations of the failed checks (notes)
EXPLAIN = {
    "property_transfers_1939": [
        "Failed check (printed error): the values sum to 209.216.237,28 for a printed Totaux 209.216.217,28 (every "
        "line re-read on a crop)."],
    "property_tribunal_cases": [
        "Failed checks, all printed errors confirmed on native-resolution crops: sgt1923 line 4° (jugements avant "
        "faire droit) Tunis 254 + Sousse 76 = 330, Total printed 334, and line 5° Tunis printed 7 with Total »; "
        "sgt1924 Tunis Total printed 1.058 for 956 + 552 = 1.508 (the general total 1.912 = 1.508 + 404 agrees with "
        "the cells); sgt1925 line 5° Tunis 1 with Total »; sgt1928 Sousse: 306 + 157 = 463, Total printed 453, and "
        "Tunis 1.670 + 591 − 536 = 1.725 for a printed 1.727 (Sousse: 342 printed, 352 by the identity; sgt1929 "
        "opens 1929 with 1.727 and 350).",
        "Continuity (comparison, not a check): cases pending at 31 December of year N−1 as printed by edition N "
        "against cases pending at 31 December as printed by edition N−1 (consecutive years only): see "
        "`property_validation.json` (`continuity`)."],
    "property_pending_requisitions": [
        "Printed column codes: juges rapporteurs of the Tunis seat (`rapporteur_tunis`, judges A, B, C) and of the "
        "Sousse seat (`rapporteur_sousse`; one judge printed over two or three columns, stored as `C1`, `C2`, … or "
        "`D1`, `D2`; sgt1925 prints three Sousse columns without heading, stored `1`-`3`; sgt1936 prints judges D "
        "and E), the magistrates delegated by the President (`delegated`, 1-3) and those commissioned by judgment "
        "(`commissioned`, 1-3) up to sgt1928; from sgt1929 one group of seven magistrates delegated or commissioned "
        "(`delegated_or_commissioned`, 1-7; sgt1935 prints the last two columns without number). sgt1939 prints the "
        "table by seat only (`judge_group` = `seat`, `judge` = `tunis` / `sousse`). The partial and general total "
        "columns and the total lines are not stored (checks).",
        "Section III is printed as two lines (fixées au rôle, en délibéré) up to sgt1928, as one line from sgt1929 "
        "(category `III`). Section IV (requisitions by year of filing) prints no line totals in sgt1927 and sgt1928 "
        "(stored cells unaffected). The first line of IV covers all earlier years where printed so (sgt1922: \"1904 "
        "et jusqu'à 1911 inclus\" printed on the first line — the following lines 1905-1911 are also printed, so the "
        "first line is stored with filing_year 1904); from sgt1935 the first lines cover two years (`1909-1910`). "
        "Line V (rectification requests) is printed up to sgt1935 (all », except sgt1927 Tunis A 1).",
        "Failed checks, all printed errors re-read on crops: sgt1922 II.2 line total 284 and Sousse C(3) column "
        "total 19 are both 19 more than the cells (the 19 requisitions of that column appear in IV by year, so the "
        "printed » on II.2 should be 19); sgt1922 IV 1911 line 25 and C(1) column 254 are both 5 more than the "
        "cells; sgt1925 IV 1923 Tunis A printed 53 where the line (154) and the column (363) need 35; sgt1926 I.3 "
        "printed partial 31 for cells summing to 91 (the general total I 831 and the grand total 1.594 need 91); "
        "sgt1927 I-III total line prints delegated 2 = 104 for lines summing to 204 (the IV total line prints 204) "
        "and IV is inconsistent in several columns (B 426 and Sousse C 282 printed for 395 and 296, as in sgt1926's "
        "totals; commissioned 1: lines 197 for 143; the line 1924 C.1 86 is clear); sgt1928 I.3 partial 116 for "
        "cells 115 (commissioned 1 column 22 for 21) and line V general total 1 with all cells »; sgt1930 IV Tunis A "
        "total 114 for lines 113."],
    "property_results_legal_status": [
        "Failed checks (printed errors, re-read on crops): sgt1923 brace total immatriculation printed 796 for 223 + "
        "73 = 296; sgt1924 Totaux printed 389 for lines and columns summing to 387 (the jugements définitifs and "
        "\"nombre total des immeubles\" give 387)."],
    "property_results_charges": [
        "The box under the table (*nombre total des immeubles*, *total des rentes d'enzel inscrites*, *total des "
        "hypothèques inscrites*) repeats totals and is used as checks; the number of land titles carrying the "
        "mortgages, by seat, is stored (`amount` = `titles`). Line totals (TOTAUX column) are checks.",
        "Failed checks (printed errors): sgt1922 enzel rents inscrites: 21.959,35 + 1.267 = 23.226,35, Totaux and "
        "box print 33.226,35; sgt1922 enzel déclarées: 3 printed under radiation Tunis, Totaux »; sgt1924 box "
        "\"nombre total des immeubles\" 387 against a) Totaux 389 (see legal status); sgt1925 box total enzel "
        "25.580,10 against the line total 28.580,10."],
    "property_results_location": [
        "Check against a): urban + rural = legal status a) for each status, outcome and seat.",
        "Failed checks (printed errors): sgt1924 brace total rural immatriculation 173 for 139 + 44 = 183, and the "
        "radiation Tunis 2 is printed under enzel (urban) here but under melk in a); sgt1926 urban melk printed total "
        "108 with a radiation Sousse 1 that neither the urban Totaux (») nor a) counts; sgt1930 rejet Sousse: melk 5 "
        "+ 4 = 9 for a) 8 and habous 0 + 1 for a) 2; sgt1936 immatriculation Tunis: melk 136 + 144 = 280 for a) "
        "279, enzel 45 + 21 = 66 for a) 67."],
    "property_results_areas": [
        "Totals: the TOTAUX column, the Totaux line, the brace totals and the *total des surfaces* are checks. "
        "Areas printed in hectares, ares, centiares (h. a. c.; sgt1936 heads \"h. a.\" but prints three groups).",
        "Failed checks (printed errors; every failing cell re-read on a crop): sgt1922 rural melk total and the "
        "Totaux total are 0,03 ha (3 a) more than the cells, the brace immatriculées 13.314 38 13 for cells summing "
        "to 13.314 37 23; sgt1926 Totaux: Tunis immatriculées 1 c short, the TOTAUX cell 64.064 37 52 for 64.064 37 "
        "25 (the total des surfaces prints 64.064 37 25); sgt1927 Totaux line: Sousse immatriculées printed 3.723 12 "
        "73 (the Tunis refused figure) and Tunis refused 5.093 39 13 (sgt1926's), with brace totals that agree with "
        "neither; sgt1928 urban enzel line and Sousse immatriculées column 1 c off; sgt1930 rural melk refusée Sousse "
        "printed 1.412 67 65 where the line total (22.741 20 93) and the column total (11.205 79 52) both need "
        "11.142 67 65, and Sousse immatriculées column 0,05 short; sgt1935 rural enzel TOTAUX 824 22 03 for cells "
        "804 22 03 (the grand total agrees with the cells); sgt1936 Totaux refusée Sousse printed 2.518 35 84 for "
        "cells 2.548 35 84 (the brace and grand totals need 2.548)."],
    "property_oppositions": [
        "Not printed in sgt1936 and sgt1939. sgt1935 prints the Totaux line with both seats and the grand total "
        "(no brace total). sgt1929: "
        "nothing printed under Tunis for \"sur lesquelles il n'a pas été statué\" (NA, `not_applicable`)."],
    "property_claimants": [
        "e) (legal quality) is printed up to sgt1935; f) (nationality) in every edition (labelled d) in sgt1936 and "
        "D. in sgt1939; sgt1936 prints three nationality lines (Français, Tunisiens, Étrangers) and no renounced "
        "column). Nationality lines vary between editions; lines printed with all cells » are stored as 0.",
        "Failed checks (printed errors): sgt1923 e) Totaux rejet Tunis printed 48 for lines summing to 30 (f) prints "
        "30; the Totaux général 604 agrees with 30); sgt1930 f) Espagnols printed 2 and 1 with a line total 1, and "
        "the immatriculation Tunis column total 863 needs Espagnols 0."],
    "property_requisitions": [
        "Periods: up to sgt1930 the table opens with \"De 1886 à 1909\" followed by single years; sgt1935 opens with "
        "1886-1932, sgt1936 with 1886-1933, sgt1939 with 1886-1934. These opening periods overlap the single years "
        "(e.g. 1886-1932 includes 1910-1930): do not sum across periods. The `Nombre` column (= French + foreign + "
        "Tunisian) is a check, not stored.",
        "Failed checks: 1924 (every printing sgt1924-sgt1930) Tunisians printed 450 where Nombre 645 and every "
        "Totaux need 459 (stored 450, `total_mismatch`); sgt1922 contenances Totaux 1 ha more than the lines; sgt1927 "
        "Totaux contenances printed 1.996.340 for lines summing to 1.996.430 (the récapitulation prints 1.996.430); "
        "sgt1935 1886-1932 foreign printed 5.134 where Nombre and the Totaux need 4.834 (sgt1936's 1886-1933 4.894 = "
        "4.834 + 60)."],
    "property_requisitions_value": [
        "Periods as in property_requisitions (overlapping opening periods). The TOTAUX column is a check, also "
        "against property_requisitions' Nombre.",
        "Failed checks: sgt1926 Totaux \"3.001 à 12.000\" printed 6.235 for lines 6.253 and TOTAUX 15.600 for 16.500 "
        "(clear on the crop)."],
    "property_titles": [
        "Periods as in property_requisitions (overlapping opening periods). Areas in hectares with four decimals.",
        "Identity total = lotissements + jugement fails on three lines printed alike by every edition sgt1922-sgt1930 "
        "(re-read on crops): 1886-1909 15.171 for 6.514 + 8.654 = 15.168, 1910 922 for 571 + 363 = 934, 1912 1.126 "
        "for 715 + 402 = 1.117 (the errors cancel out in the Totaux); and on the sgt1939 Totaux line (53.778 for "
        "34.409 + 19.349; with the lines' 19.369 it holds).",
        "Failed checks: sgt1924 Totaux valeur printed 232.114.176 for lines summing to 222.114.176 (the "
        "récapitulation prints 222.114.176); sgt1935 1886-1932 printed 1.398.823 02 59 ha and 359.173.670 fr., where "
        "the Totaux need 1.389.922 46 58 and 383.173.670 (sgt1936's 1886-1933 figures equal these plus 1933); "
        "sgt1939 Totaux titres délivrés en suite d'un jugement printed 19.349 for lines summing to 19.369 (the "
        "récapitulation prints 19.369), valeur 621.233.714 for lines summing to 621.234.214."],
    "property_conservation_recap": [
        "One row per measure and edition: cumulative figures since 1886 at 31 December of the edition year, stored "
        "as printed (the table exists only as totals). Contenances are printed in whole hectares here. Checks against "
        "the Totaux of the requisitions and titles tables (area truncated to the hectare).",
        "Failed checks: sgt1924 valeur 222.114.176 against the titles Totaux 232.114.176 (the titles lines agree "
        "with 222.114.176); sgt1927 contenances 1.996.430 against the requisitions Totaux 1.996.340 (the lines "
        "agree with 1.996.430); sgt1930 valeurs déclarées 553.301.391 against the requisitions Totaux 553.101.391; "
        "sgt1939 valeur 621.233.914 against the titles Totaux 621.233.714 and titres établis 19.369 against 19.349."],
}

SURVEY = {
    "sgt1922": "f103 chapter VI title (Propriété immobilière); f104 blank; f105 Tribunal mixte, travaux du tribunal: "
               "a) statistique des affaires (cases) and the work of the court (activity); f106 b) situation des "
               "affaires d'immatriculation en cours au 31 décembre (pending, I-V); f107 résultats des instances "
               "d'immatriculation: a) état juridique et charge des immeubles (legal_status, charges, box), b) "
               "situation des immeubles (location); f108 c) superficies (areas), d) jugement des oppositions, e) "
               "nombre et qualité juridique des requérants; f109 f) nationalité des requérants; f110 Conservation "
               "foncière: réquisitions d'immatriculation (1886-1922) a) nationalité, nombre, contenances, valeurs, b) "
               "répartition d'après les valeurs; f111 titres délivrés (1886-1922), récapitulation a) and b); f112 "
               "blank. f113 = chapter VII.",
    "sgt1923": "f587 title; f588 blank; f589 a) cases and activity; f590 b) pending; f591 a) legal status, charges, b) "
               "location; f592 c) areas, d) oppositions, e) claimants; f593 f) nationality; f594 Conservation "
               "foncière a), b) (1886-1923); f595 titres délivrés, récapitulation; f596 blank. f597 = chapter VII.",
    "sgt1924": "f1077 title; f1078 blank; f1079 a); f1080 b) pending; f1081 a), b); f1082 c), d), e); f1083 f); f1084 "
               "Conservation foncière a), b) (1886-1924); f1085 titres délivrés, récapitulation; f1086 blank. "
               "f1087 = chapter VII.",
    "sgt1925": "f113 title; f114 blank; f115 a) (upper part now printed as lines); f116 b); f117 a), b); f118 c), d) "
               "(new line \"renvoyées devant les juridictions de droit commun\"), e); f119 f); f120 Conservation "
               "foncière a), b) (1886-1925); f121 titres délivrés, récapitulation; f122 blank. f123 = chapter VII.",
    "sgt1926": "f665 title; f666 a); f667 b); f668 a), b); f669 c), d), e); f670 f); f671 Conservation foncière a), b) "
               "(1886-1926); f672 titres délivrés, récapitulation. f673 = chapter VII. Faint print throughout.",
    "sgt1927": "f127 title; f128 a); f129 b); f130 a), b); f131 c), d), e); f132 f); f133 Conservation foncière a), b) "
               "(1886-1927); f134 titres délivrés, récapitulation. f135 = chapter VII.",
    "sgt1928": "f651 title; f652 a); f653 b); f654 a), b); f655 c), d), e); f656 f); f657 Conservation foncière a), b) "
               "(1886-1928); f658 titres délivrés, récapitulation. f659 = chapter VII.",
    "sgt1929": "f129 title; f130 a); f131 b) (new layout: judges A-C Tunis, D Sousse, seven magistrates; III one "
               "line); f132 a), b); f133 c), d), e); f134 f); f135 Conservation foncière a), b) (1886-1929); f136 "
               "titres délivrés, récapitulation. f137 = chapter VII.",
    "sgt1930": "f663 title; f664 a); f665 b); f666 a), b); f667 c), d), e); f668 f); f669 Conservation foncière a), b) "
               "(1886-1930); f670 titres délivrés, récapitulation. f671 = chapter VII.",
    "sgt1935": "f91 chapter VI title (Tribunal mixte); f92 a); f93 b); f94 a), b); f95 c), d) (Totaux only), e); f96 "
               "f); f97 Conservation foncière a), b) (1886-1932 then 1933-1935), titres délivrés, récapitulation, all "
               "on one page; f98 blank. f99 = chapter VII.",
    "sgt1936": "f62 chapter V title (Propriété foncière); f63 a) travaux du Tribunal mixte; f64 b) pending (judges "
               "A-C Tunis, D-E Sousse, seven magistrates); f65 a) état juridique et charges, b) situation des "
               "immeubles; f66 c) superficie, d) nationalité des requérants (no oppositions, no legal quality); f67 "
               "Conservation foncière (1886-1933 then 1934-1936), titres délivrés, récapitulation. f68 = chapter VI "
               "Instruction publique. The range 62-67 of CHAPTERS.md is confirmed.",
    "sgt1939": "f57 chapter V title; f58 travaux du Tribunal mixte; f59 pending by seat only; f60 A. état juridique "
               "et charge, B. situation; f61 C. superficies, D. nationalité des requérants; f62 Conservation "
               "foncière (1886-1934 then 1935-1939), titres délivrés, récapitulation; f63 Conservation de la "
               "propriété foncière: mutations entre vifs en 1939 d'immeubles immatriculés, by contrôle civil "
               "(property_transfers_1939); f64 blank. f65 = chapter VI.",
}

NOT_DONE = ("Every table of the chapter is transcribed in every edition that prints it, every cell read on "
            "native-resolution crops of the page images (contact sheets of every view from the view before the "
            "chapter title to the next chapter title); the yearly "
            "Conservation foncière series of sgt1923-sgt1930 were re-read in full on each printing. Nothing in the chapter is left out: the views not listed as tables are the chapter title "
            "and blank pages. The boxes printed under a) (totals repeating the table) and the TOTAUX columns and "
            "lines are used as checks only; the récapitulation, which exists only as cumulative totals, is stored.")


def continuity(secs):
    out, n = [], 0
    cs = {s["ed"]: s for s in secs if s["table"] == "cases"}
    for e0, e1 in zip(ORDER, ORDER[1:]):
        if e0 in cs and e1 in cs and int(cs[e1]["year"]) == int(cs[e0]["year"]) + 1:
            for st in ("tunis", "sousse"):
                n += 1
                a = row(cs[e0], "pending_end")[st].value
                b = row(cs[e1], "pending_start")[st].value
                if a != b:
                    out.append(f"{st}: {e0} pending at 31 Dec {cs[e0]['year']} = {a}, {e1} pending at the start = {b}")
    return n, out


def write_survey():
    L = ["# Property chapter: survey of every edition", "",
         "Page-by-page survey of the *Propriété immobilière / Tribunal mixte / Propriété foncière* chapter (chapter "
         "VI up to sgt1935, chapter V in sgt1936 and sgt1939). Views confirmed on the page images; every table read "
         "cell by cell on native-resolution crops. Extraction: `extract_property.py`.", "",
         "| edition | ark | views |", "|---|---|---|"]
    L += [f"| {e} | `{EDITIONS[e]}` | {a}–{b} |" for e, (a, b) in CHAPTER_VIEWS.items()]
    L += ["", "## Views per edition", ""] + [f"- **{e}**: {t}" for e, t in SURVEY.items()]
    L += ["", "## Tables (CSV) and the sections they hold", "",
          "| CSV | transcription sections | editions |", "|---|---|---|"]
    for out, spec in TABLES.items():
        L.append(f"| `{out}` | {', '.join(spec['secs'])} | {', '.join(spec.get('_eds', []))} |")
    L += ["", "## Image versus OCR", "", "Every section of every edition is marked `img: all` in the transcriptions: every value was read on "
          "native-resolution crops of the page image. The yearly Conservation foncière series (requisitions, value "
          "brackets, titles) of sgt1923-sgt1930, first drafted by carrying earlier years over from the previous "
          "edition, were then re-read in full, line by line, on crops of each printing (24 printings, 2.496 cells "
          "including the Totaux lines and columns): no cell differed from the transcription. The Gallica word OCR was "
          "used only as a cross-check (the 135 cells whose OCR token differed are all OCR misreadings).",
          "", "## Coverage", "", NOT_DONE, ""]
    (OUT / "property_survey.md").write_text("\n".join(L) + "\n")


def build(write=True):
    secs = []
    for ed in ORDER:
        p = TR / f"property_{ed}.txt"
        if p.exists():
            secs += parse(p, ed)
    by = {(s["table"], s["ed"]): s for s in secs}
    for s in secs:
        t, ed = s["table"], s["ed"]
        if t == "cases":
            chk_cases(s)
        elif t == "activity":
            chk_activity(s, by.get(("cases", ed)))
        elif t == "pending":
            chk_pending(s)
        elif t == "pending_groups":
            chk_pending_groups(s, by.get(("pending", ed)))
        elif t == "pending_age":
            chk_pending_age(s, by.get(("pending", ed)))
        elif t == "legal_status":
            chk_grid("legal_status", s)
        elif t == "charges":
            chk_charges(s)
        elif t == "charges_summary":
            chk_charges_summary(s, by.get(("legal_status", ed)), by.get(("charges", ed)))
        elif t == "location":
            chk_grid("location", s)
            chk_location_vs_legal(s, by.get(("legal_status", ed)))
        elif t == "areas":
            chk_grid("areas", s)
        elif t == "oppositions":
            chk_grid("oppositions", s)
            ta = row(s, "Total@all")
            if ta is not None:
                CHK.eq("oppositions", f"{where(s)} Total@all = all lines, both seats",
                       ssum(r["cells"][x].value for r in dl(s) for x in ("tunis", "sousse")), ta["tunis"].value)
        elif t in ("claimant_status", "claimant_nationality"):
            chk_grid("claimants", s)
        elif t in ("requisitions", "value_brackets", "titles"):
            chk_series(t, s)
        elif t == "transfers":
            chk_total_line("transfers", s, "Totaux", [r["label"] for r in dl(s)], s["cols"])
    for ed in ORDER:
        chk_cross_series(by, ed)
        st, na = by.get(("claimant_status", ed)), by.get(("claimant_nationality", ed))
        if st and na and row(st, "Total") and row(na, "Total"):
            for c in st["cols"]:
                CHK.eq("claimants", f"{where(na)} {c}: f) Totaux = e) Totaux", row(st, "Total")[c].value,
                       row(na, "Total")[c].value)
    auto = auto_mismatch()
    ncont, dcont = continuity(secs)
    res = {}
    for out, spec in TABLES.items():
        ss = [s for s in secs if s["table"] in spec["secs"]]
        spec["_eds"] = [e for e in ORDER if any(s["ed"] == e for s in ss)]
        recs = []
        for s in ss:
            recs += spec["cells"][s["table"]](s)
        flagged = []
        for r in recs:
            k = (r["census"], r["table_id"], r["_row"], r["_col"])
            if r["flag"]:
                continue
            if k in FLAGS:
                r["flag"] = FLAGS[k][0]
                flagged.append(f"{k[0]} {k[1]} {k[2]} / {k[3]}: {FLAGS[k][1]}")
            elif k in auto:
                r["flag"] = "total_mismatch"
                flagged.append(f"{k[0]} {k[1]} {k[2]} / {k[3]}: printed {r['value']}; its line and its column "
                               f"are both {auto[k]} off their printed totals (printed value kept)")
        kept, compared, diffs = select_latest(recs, spec["key"])
        order = {id(r): i for i, r in enumerate(recs)}
        if spec.get("series"):
            kept.sort(key=lambda r: (r["year"] is not None, r["year"] or 0, r["period"], ORDER.index(r["census"]),
                                     order.get(id(r), 0)))
        else:
            kept.sort(key=lambda r: (ORDER.index(r["census"]), order.get(id(r), 0)))
        fails = CHK.fail[out]
        res[out] = dict(rows=len(kept), checks=CHK.n[out], failed=list(fails), overlap_compared=compared,
                        overlap_diffs=[list(d) for d in diffs], flagged=flagged)
        if out == "property_tribunal_cases":
            res[out]["continuity_compared"] = ncont
            res[out]["continuity_diffs"] = dcont
        if write:
            cols = COMMON + spec["dims"] + ["value", "flag"]
            doc = dict(T_DOC, **spec["doc"])
            doc.setdefault("measure", "measure code")
            doc["flag"] = ("empty, or `total_mismatch` (printed value kept), `derived_from_totals`, `row_realigned`, "
                           "`not_applicable` (nothing printed)")
            write_csv(out, cols, kept)
            paras = list(spec.get("paras", [])) + EXPLAIN.get(out, [])
            if out == "property_tribunal_cases":
                paras.append(f"Continuity: {ncont} comparisons, {len(dcont)} differences" +
                             (": " + "; ".join(dcont) if dcont else "") + ".")
            if flagged:
                paras.append("Flagged cells: " + "; ".join(flagged) + ".")
            paras.append("Survey of the whole chapter in every edition: `property_survey.md`.")
            rule = RULE4 if spec.get("series") else RULE5
            if spec.get("series"):
                paras.append("Overlap comparison: every printing of sgt1922-sgt1930 (and of sgt1935, sgt1936) was "
                             "read independently on its own page image. The single years 1910-1930 are printed "
                             "from the same standing type in every edition (the 1924 value \"17.872 50\" and the "
                             "Tunisians 450 recur unchanged), so the printings agree cell for cell; the only "
                             "differences between editions lie in the opening multi-year periods, which are distinct "
                             "periods (1886-1909, 1886-1932, 1886-1933, 1886-1934) and are stored separately.")
            if spec.get("series"):
                rule += (" Each single year is printed by every edition from its own year to sgt1930 (up to nine "
                         "printings, 1910-1930); 1931 and 1932 are printed only inside the opening periods; 1933-1936 "
                         "are printed by one to three of sgt1935, sgt1936 and sgt1939, 1937-1939 by sgt1939 only; the opening multi-year "
                         "periods differ between edition groups and are each stored once.")
            write_notes(out, CHAPTER, SCRIPT, kept, cols, doc, spec["title_fr"], spec["title_en"], paras,
                        CHK.n[out], fails, compared, diffs, coverage_lines(ss), rule, spec["unit"])
    if write:
        write_validation(OUT / "property_validation.json", dict(
            res, _chapter_views=CHAPTER_VIEWS, _survey=SURVEY, _not_transcribed=NOT_DONE))
        write_survey()
    return res


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    res = build(write=(mode == "build"))
    for out, d in res.items():
        print(f"{out}: {d['rows']} rows, {d['checks']} checks, {len(d['failed'])} failed, "
              f"{d['overlap_compared']} compared, {len(d['overlap_diffs'])} diffs, {len(d['flagged'])} flagged")
        for f in d["failed"]:
            print("   FAIL", f)
        for x in d["overlap_diffs"]:
            print("   DIFF", x)
        for x in d["flagged"]:
            print("   FLAG", x)
        for x in d.get("continuity_diffs", []):
            print("   CONT", x)


if __name__ == "__main__":
    main()
