#!/usr/bin/env python3
"""Justice chapter (chapter IV, *Justice*) of the Statistique générale de la Tunisie, 12 editions
sgt1922-sgt1939: French courts (Tribunaux de Tunis and Sousse), Tunisian courts (Ouzara, Tribunaux
régionaux, Chambres, Présidents and caïds, Tribunal de l'Ouzara / Chambre de révision), appeals,
taxes and fines, execution of French judgments.

  python3 extract_justice.py check   parse the transcriptions, run every check, print failures
  python3 extract_justice.py build   ... and write csv/justice_*.csv, their .md notes and
                                     csv/justice_validation.json

Source of truth: transcribed/justice_<edition>.txt (format in yb_tables.py). Tables printed for
overlapping year windows follow SPEC_ADDENDUM rule 4 (each year from the latest edition printing it,
every other printing compared); tables printed once per edition follow rule 5 (all editions kept, a
year printed twice taken from the later edition and compared). Printed totals are used for checks only.
"""
import sys
from collections import defaultdict
from decimal import Decimal

from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parent))  # shared helper yb_tables.py
from yb_tables import (COMMON, EDITIONS, ORDER, OUT, TR, Checks, check_col_totals, check_row,
                       coverage_lines, is_total, parse, select_latest, ssum, where, write_csv, write_notes,
                       write_validation, years_of)

CHAPTER = "Justice"
SCRIPT = "extract_justice.py"

# Chapter view ranges (chapter title page .. last view before the next chapter), confirmed on the images.
CHAPTER_VIEWS = {
    "sgt1922": (85, 94), "sgt1923": (569, 578), "sgt1924": (1059, 1068), "sgt1925": (93, 104),
    "sgt1926": (643, 654), "sgt1927": (105, 116), "sgt1928": (629, 640), "sgt1929": (107, 118),
    "sgt1930": (641, 652), "sgt1935": (71, 80), "sgt1936": (52, 57), "sgt1939": (47, 52),
}

CHK = Checks()

# ----------------------------------------------------------------- labels

M = {  # measure code -> printed French heading
    # French courts
    "criminal": "Affaires criminelles jugées",
    "correctional_contradictory": "Affaires correctionnelles jugées contradictoirement",
    "correctional_default": "Affaires correctionnelles jugées par défaut",
    "contradictory": "Contradictoires",
    "default": "Défaut",
    "preparatory": "Préparatoires",
    "on_petition": "Sur requête",
    "bankruptcies": "Faillites",
    "liquidations": "Liquidations",
    # movement of cases
    "pending_start": "Il restait de l'année précédente / Restant à juger au 31 décembre de l'année précédente",
    "entered": "Affaires entrées dans l'année / Procédures inscrites dans l'année",
    "out_no_case": "Il est sorti : par non-lieu",
    "out_judgment": "Il est sorti : par jugement",
    "pending_end": "Reste (au 31 décembre)",
    "out_acquittal": "Il est sorti : par acquittement",
    "out_conviction": "Il est sorti : par condamnation",
    "confirmed": "Affaires sorties : par confirmation",
    "partly_reversed": "Affaires sorties : par réformation partielle",
    "fully_reversed": "Affaires sorties : par réformation totale",
    "struck_off": "Affaires sorties : rayées du rôle",
    # appeal rate
    "civil_appealable": "Affaires civiles : affaires appelables",
    "civil_appeals": "Affaires civiles : nombre d'appels",
    "civil_pct": "Affaires civiles : moyenne pour cent",
    "penal_appealable": "Affaires pénales : affaires appelables",
    "penal_appeals": "Affaires pénales : nombre d'appels",
    "penal_pct": "Affaires pénales : moyenne pour cent",
    # fees
    "registration_stamp_duties": "Montant des droits de timbre et d'enregistrement",
    "chancery_stamp_duties": "Montant des droits de timbre et de chancellerie perçus sur les grosses et expéditions",
    "fines_proportional_duties": "Montant des amendes et des droits proportionnels y afférents",
    # execution of French judgments
    "deposited": "Jugements déposés du 1er janvier au 31 décembre",
    "executed_in_full": "Jugements exécutés totalement",
    "attempted": "Tentatives d'exécution",
    "convicted": "Affaires jugées : jugements de condamnation",
    "acquitted": "Affaires jugées : jugements d'acquittement ou de relaxe",
    "conv_confirmed": "Venues sur jugements de condamnation, décisions confirmées : par confirmation pure et simple",
    "conv_confirmed_reduced": "Venues sur jugements de condamnation, décisions confirmées : avec diminution de peine",
    "conv_confirmed_increased": "Venues sur jugements de condamnation, décisions confirmées : avec augmentation de peine",
    "conv_reversed": "Venues sur jugements de condamnation : décisions infirmées",
    "acq_confirmed": "Venues sur jugements d'acquittement : confirmées",
    "acq_reversed": "Venues sur jugements d'acquittement : infirmées",
    # parquets
    "dismissed": "Sortie : affaires classées sans suite",
    "direct_summons": "Sortie : affaires réglées par citation directe devant le Tribunal",
    "to_investigation": "Sortie : affaires mises à l'instruction",
    "to_police_court": "Sortie : affaires renvoyées en simple police",
    "to_french_courts": "Dessaisissements : affaires renvoyées devant la Justice française",
    "to_other_tunisian_courts": "Dessaisissements : affaires renvoyées devant d'autres Tribunaux tunisiens",
    # chambres d'instruction
    "entered_criminal": "Entrées : affaires criminelles",
    "entered_correctional": "Entrées : affaires correctionnelles",
    "nl_criminal": "Sorties, non-lieu : affaires criminelles réglées par non-lieu",
    "nl_correctional": "Sorties, non-lieu : affaires correctionnelles réglées par non-lieu",
    "to_indictment_chamber": "Sorties, renvois : affaires correctionnelles renvoyées devant la Chambre d'accusation",
    "criminal_correctionalised": "Sorties, renvois : affaires criminelles correctionnalisées",
    "to_correctional": "Sorties, renvois : affaires correctionnelles",
    "to_other_tunisian_judges": "Dessaisissement : au profit d'autres juges tunisiens",
    # chambre d'accusation, chambre de révision
    "no_case": "Total des affaires réglées par non-lieu",
    "to_criminal_chamber": "Affaires réglées par renvoi devant la Chambre criminelle",
    "to_correctional_chamber": "Affaires réglées par renvoi devant la Chambre correctionnelle",
    "settled": "Total des affaires réglées",
    "judged": "Affaires jugées dans l'année",
    # caids / presidents
    "civil": "Affaires civiles",
    "penal": "Affaires pénales",
}
MATTER = {"civil": "Affaires civiles", "correctional": "Affaires correctionnelles", "penal": "Affaires pénales",
          "criminal": "Affaires criminelles"}


def meas(code):
    return code, M.get(code, code)


# ----------------------------------------------------------------- table definitions
# kind: how a section maps to cells
#   year_rows   rows = years (label), cols = measures
#   year_cols   rows = measures (label), cols = years
#   entity      rows = entity (label), cols = measures, year = section year
#   entity_ym   rows = entity (label), cols 'A:B' with A or B a year (the other part a measure/matter)
# totals: total columns / total rows not stored (used in checks); key: dims identifying a cell across
# editions (rule 4 / 5).

TABLES = {
    "fr_criminal": dict(out="justice_french_criminal", kind="year_rows", entity=None, totals={"total"},
                        title_fr="Justice française : affaires criminelles et correctionnelles jugées, par tribunal",
                        title_en="French justice: criminal and correctional cases judged, by court"),
    "fr_civil": dict(out="justice_french_civil", kind="year_rows", entity=None, totals={"total"},
                     title_fr="Justice française : affaires civiles, par tribunal",
                     title_en="French justice: civil cases, by court"),
    "fr_commercial": dict(out="justice_french_commercial", kind="year_rows", entity=None, totals={"total"},
                          title_fr="Justice française : affaires commerciales, par tribunal",
                          title_en="French justice: commercial cases, by court"),
    "tn_ouzara_criminal": dict(out="justice_ouzara_criminal", kind="year_cols", entity=None,
                               totals={"TOTAUX", "out_total"},
                               title_fr="Justice tunisienne, Ouzara : affaires criminelles",
                               title_en="Tunisian justice, Ouzara: criminal cases (movement)"),
    "tn_appeals_civil": dict(out="justice_ouzara_appeals", kind="entity", entity="tribunal",
                             totals={"total_to_judge", "out_total"}, matter="civil",
                             title_fr="Justice tunisienne, Ouzara : appels en matière civile et correctionnelle, "
                                      "par tribunal ayant rendu les décisions frappées d'appel",
                             title_en="Tunisian justice, Ouzara: civil and correctional appeals, by court of "
                                      "first instance"),
    "tn_appeals_correctional": dict(out="justice_ouzara_appeals", kind="entity", entity="tribunal",
                                    totals={"total_to_judge", "out_total"}, matter="correctional"),
    "tn_appeals_correctional2": dict(out="justice_ouzara_correctional_appeals_detail", kind="entity",
                                     entity="tribunal", totals={"total_to_judge", "out_total"}, matter="correctional",
                                     title_fr="Justice tunisienne, Ouzara : appels en matière correctionnelle (affaires "
                                              "sorties par nature du jugement frappé d'appel et de la décision)",
                                     title_en="Tunisian justice, Ouzara: correctional appeals, by kind of judgment "
                                              "appealed and decision"),
    "tn_regional": dict(out="justice_regional_courts", kind="entity_ym", entity="tribunal", totals=set(),
                        title_fr="Tribunaux régionaux : affaires civiles et correctionnelles (procédures)",
                        title_en="Regional courts: civil and correctional proceedings (movement)"),
    "tn_caids": dict(out="justice_caids_presidents", kind="entity_ym", entity="jurisdiction", totals=set(),
                     title_fr="Juridiction des caïds, kahias ou khalifas délégués et des présidents des "
                              "tribunaux régionaux : affaires civiles et pénales",
                     title_en="Jurisdiction of the caïds, kahias or khalifas and of the presidents of the "
                              "regional courts: civil and penal cases"),
    "tn_parquets": dict(out="justice_regional_prosecutors", kind="entity", entity="tribunal", totals=set(),
                        title_fr="Travaux des parquets des tribunaux régionaux",
                        title_en="Work of the public prosecutors' offices of the regional courts"),
    "tn_instruction": dict(out="justice_regional_investigation", kind="entity", entity="tribunal",
                           totals={"entered_total", "nl_total", "out_total"},
                           title_fr="Travaux des chambres d'instruction des tribunaux régionaux",
                           title_en="Work of the investigating chambers of the regional courts"),
    "tn_accusation": dict(out="justice_indictment_chamber", kind="entity", entity=None, totals=set(),
                          title_fr="Travaux de la Chambre d'accusation (Chambre des mises en accusation)",
                          title_en="Work of the indictment chamber"),
    "tn_revision": dict(out="justice_revision_chamber", kind="year_cols", entity=None, totals={"TOTAUX"},
                        title_fr="Travaux de la Chambre de révision", title_en="Work of the review chamber"),
    "tn_stats": dict(out="justice_tunisian_courts_1935_1939", kind="entity", entity="tribunal", totals=set(),
                     title_fr="Justice tunisienne, juridictions de droit commun : statistique annuelle (Chambre des "
                              "requêtes, Tribunaux d'appel de l'Ouzara, Tribunaux de première instance, parquets, "
                              "chambres d'instruction, présidents et officiers de police judiciaire, assistance "
                              "judiciaire)",
                     title_en="Tunisian justice, ordinary courts: yearly statistics (from sgt1935)"),
    "tn_appeal_rate": dict(out="justice_appeal_rate", kind="entity", entity="tribunal", totals=set(),
                           title_fr="Usage du droit d'appel", title_en="Use of the right of appeal"),
    "tn_fees": dict(out="justice_fees_fines", kind="entity", entity="tribunal", totals={"total"},
                    title_fr="Produit des taxes et amendes", title_en="Proceeds of taxes and fines"),
    "fr_judgments_execution": dict(out="justice_french_judgments_execution", kind="year_cols", entity=None,
                                   totals={"remaining", "TOTAUX", "out_total"},
                                   title_fr="Exécution des jugements français",
                                   title_en="Execution of French judgments"),
}


# ----------------------------------------------------------------- checks per table

def run_checks(sec):
    t = sec["table"]
    for tgt, parts in sec.get("checks", []):
        check_row(CHK, t, sec, tgt, [p if not p.startswith("-") else p for p in parts])
    if t == "tn_stats":
        check_col_totals(CHK, t, sec)
    if t in ("fr_criminal", "fr_civil", "fr_commercial"):
        courts = sorted({c.split("@")[1] for c in sec["cols"] if "@" in c}) or [None]
        for ct in courts:
            sfx = f"@{ct}" if ct else ""
            parts = [c for c in sec["cols"] if c.endswith(sfx) and not c.startswith("total")]
            if f"total{sfx}" in sec["cols"]:
                check_row(CHK, t, sec, f"total{sfx}", parts)
    elif t == "tn_ouzara_criminal":
        for y in sec["cols"]:
            g = {r["label"]: r["cells"][y].value for r in sec["rows"]}
            CHK.eq(t, f"{where(sec)} {y}: TOTAUX = pending_start + entered",
                   ssum([g["pending_start"], g["entered"]]), g["TOTAUX"])
            if "out_total" in g:
                a, b = ("out_no_case", "out_judgment") if "out_no_case" in g else ("out_acquittal", "out_conviction")
                CHK.eq(t, f"{where(sec)} {y}: out_total = {a} + {b}", ssum([g[a], g[b]]), g["out_total"])
                CHK.eq(t, f"{where(sec)} {y}: pending_end = TOTAUX - out_total",
                       ssum([g["TOTAUX"], -g["out_total"]]), g["pending_end"])
        ys = sec["cols"]
        for a, b in zip(ys, ys[1:]):
            CHK.eq(t, f"{where(sec)} pending_end {a} = pending_start {b}",
                   v_(sec, "pending_end", a), v_(sec, "pending_start", b))
    elif t in ("tn_appeals_civil", "tn_appeals_correctional"):
        check_row(CHK, t, sec, "total_to_judge", ["pending_start", "entered"])
        check_row(CHK, t, sec, "out_total", ["confirmed", "partly_reversed", "fully_reversed", "struck_off"])
        check_row(CHK, t, sec, "pending_end", ["total_to_judge", "-out_total"])
        check_col_totals(CHK, t, sec)
    elif t == "tn_appeals_correctional2":
        check_row(CHK, t, sec, "total_to_judge", ["pending_start", "entered"])
        check_row(CHK, t, sec, "out_total", ["conv_confirmed", "conv_confirmed_reduced", "conv_confirmed_increased",
                                             "conv_reversed", "acq_confirmed", "acq_reversed"])
        check_row(CHK, t, sec, "pending_end", ["total_to_judge", "-out_total"])
        check_col_totals(CHK, t, sec)
    elif t == "tn_regional":
        check_col_totals(CHK, t, sec)
        ys = sorted({c.split(":")[0] for c in sec["cols"]})
        for r in sec["rows"]:
            c = r["cells"]
            for y in ys:
                if c.get(f"{y}:convicted") is not None and c[f"{y}:convicted"].value is not None:
                    CHK.eq(t, f"{where(sec)} {r['label']} {y}: pending_end = pending_start + entered - convicted "
                              f"- acquitted", ssum([c[f"{y}:pending_start"].value, c[f"{y}:entered"].value,
                                                   -c[f"{y}:convicted"].value, -c[f"{y}:acquitted"].value]),
                           c[f"{y}:pending_end"].value)
            for a, b in zip(ys, ys[1:]):
                CHK.eq(t, f"{where(sec)} {r['label']}: pending_end {a} = pending_start {b}",
                       r["cells"][f"{a}:pending_end"].value, r["cells"][f"{b}:pending_start"].value)
    elif t == "tn_caids":
        check_col_totals(CHK, t, sec, total=lambda l: is_total(l) or l.startswith("A reporter"))
    elif t == "tn_parquets":
        check_row(CHK, t, sec, "entered", [c for c in sec["cols"] if c != "entered"])
        check_col_totals(CHK, t, sec)
    elif t == "tn_instruction":
        check_row(CHK, t, sec, "entered_total", ["entered_criminal", "entered_correctional"])
        check_row(CHK, t, sec, "nl_total", ["nl_criminal", "nl_correctional"])
        check_row(CHK, t, sec, "out_total", ["nl_total", "to_indictment_chamber", "criminal_correctionalised",
                                             "to_correctional", "to_police_court", "to_other_tunisian_judges",
                                             "to_french_courts"])
        check_row(CHK, t, sec, "pending_end", ["entered_total", "-out_total"])
        check_col_totals(CHK, t, sec)
    elif t == "tn_accusation":
        if sec.get("part") == "final":
            check_row(CHK, t, sec, "entered", ["no_case", "to_criminal_chamber", "to_correctional_chamber",
                                               "pending_end"])
        else:
            check_row(CHK, t, sec, "entered", ["settled", "pending_end"])
    elif t == "tn_revision":
        g = {r["label"]: r["cells"]["value"].value for r in sec["rows"]}
        CHK.eq(t, f"{where(sec)}: TOTAUX = pending_start + entered", ssum([g["pending_start"], g["entered"]]),
               g["TOTAUX"])
        CHK.eq(t, f"{where(sec)}: pending_end = TOTAUX - judged", ssum([g["TOTAUX"], -g["judged"]]),
               g["pending_end"])
    elif t == "tn_appeal_rate":
        check_col_totals(CHK, t, sec, cols=[c for c in sec["cols"] if not c.endswith("_pct")])
        for r in sec["rows"]:
            c = r["cells"]
            for m in ("civil", "penal"):
                a, n, p = c[f"{m}_appealable"].value, c[f"{m}_appeals"].value, c[f"{m}_pct"].value
                if a and n is not None and p is not None:
                    CHK.eq(t, f"{where(sec)} {r['label']}: {m}_pct = 100 x appeals / appealable (to 0.01)",
                           (Decimal(100) * n / a).quantize(Decimal("0.01")), p, tol=Decimal("0.011"))
    elif t == "tn_fees":
        check_row(CHK, t, sec, "total", [c for c in sec["cols"] if c != "total"])
        check_col_totals(CHK, t, sec)
    elif t == "fr_judgments_execution":
        g = {r["label"]: r["cells"]["value"].value for r in sec["rows"]}
        if "deposited" not in g:
            CHK.eq(t, f"{where(sec)}: out_total = attempted + executed_in_full",
                   ssum([g["executed_in_full"], g["attempted"]]), g["out_total"])
        elif "TOTAUX" in g:
            CHK.eq(t, f"{where(sec)}: TOTAUX = pending_start + deposited", ssum([g["pending_start"], g["deposited"]]),
                   g["TOTAUX"])
            CHK.eq(t, f"{where(sec)}: out_total = executed_in_full + attempted",
                   ssum([g["executed_in_full"], g["attempted"]]), g["out_total"])
            CHK.eq(t, f"{where(sec)}: remaining = TOTAUX - out_total", ssum([g["TOTAUX"], -g["out_total"]]),
                   g["remaining"])
        else:
            CHK.eq(t, f"{where(sec)}: remaining = deposited - executed_in_full",
                   ssum([g["deposited"], -g["executed_in_full"]]), g["remaining"])


def v_(sec, label, col):
    for r in sec["rows"]:
        if r["label"] == label:
            return r["cells"][col].value
    return None


# ----------------------------------------------------------------- cells

def base(sec, year):
    return {"census": sec["ed"], "table_id": sec["table"], "gallica_ark": sec["ark"], "source_page": sec["page"],
            "gallica_view": sec["view"], "year": year, "court": sec.get("court"),
            "matter": sec.get("matter") or TABLES[sec["table"]].get("matter"), "part": sec.get("part"), "section": sec.get("section"),
            "section_fr": sec.get("section_fr")}


import re as _re
import unicodedata as _ud

J_ALIAS = {"djemal": "djemmal", "hemmama": "hemama", "djelass": "jlass", "djelasselguebala": "jlasselguebala",
           "maknassy": "maknassi", "tataouine": "tatahouine", "skira": "skhira", "lakef": "kef", "kef": "kef",
           "sbeitlasecondline": "sbikha", "ouledaoun": "ouledaoun", "metouia": "metouia", "methouia": "metouia",
           "rohiaskerra": "rohia", "rohiaskerna": "rohia", "fahs": "fahs", "lenfida": "enfida", "oha": "rohia",
           "ousseltia": "ousseltia", "louseltia": "ousseltia", "tamerza": "tamerza", "tamerza": "tamerza",
           "feriana": "feriana", "ferina": "feriana", "djerid": "djerid", "lassira": "skhira", "laskhira": "skhira",
           "laregba": "regba", "regba": "regba", "souassi": "souassi", "mssaken": "msaken", "msaken": "msaken"}


def jkey(name):
    """Jurisdiction key for matching printings: title and articles dropped, accents and hyphens removed."""
    if name is None:
        return None
    n = _re.sub(r"\(second line\)", "second line", name)
    pres = n.startswith("Président") or n.startswith("Juge")
    n = _re.sub(r"^(Caïd|Kahia|Khalifat?|Président( du Tribunal)?|Juge cantonal)\s+(de la|de l'|de|des|du|d')\s*", "", n)
    n = _re.sub(r"^(La|Le|L')\s*", "", n) if not n.startswith("La Skhira") else n
    n = "".join(c for c in _ud.normalize("NFD", n) if _ud.category(c) != "Mn").lower()
    n = _re.sub(r"[^a-z]", "", n)
    n = J_ALIAS.get(n, n)
    return ("P:" if pres else "") + n


def cells(sec):
    spec = TABLES[sec["table"]]
    kind, tot = spec["kind"], spec["totals"]
    out = []

    def add(year, measure, cell, entity=None, extra=None):
        r = base(sec, year)
        r.update({"measure": measure, "measure_fr": sec.get("fr_" + measure, M.get(measure, measure)), "value": cell.value,
                  "flag": cell.flag, "_raw": cell.raw})
        if spec["entity"]:
            r[spec["entity"]] = entity
            r["_j"] = jkey(entity) if spec["entity"] == "jurisdiction" else entity
        if extra:
            r.update(extra)
        out.append(r)

    for row in sec["rows"]:
        lab = row["label"]
        if is_total(lab) or lab in tot or lab.startswith("A reporter") or lab == "Report":
            continue
        for c, cell in row["cells"].items():
            if c in tot:
                continue
            if kind == "year_rows":
                if "@" in c:           # one table for both courts: column 'measure@Court'
                    m, ct = c.split("@")
                    if m in tot:
                        continue
                    add(int(lab), m, cell, extra={"court": ct})
                else:
                    add(int(lab), c, cell)
            elif kind == "year_cols":
                add(int(c) if c.isdigit() else years_of(sec)[0], lab, cell)
            elif kind == "entity":
                m = _re.match(r"(\w+)_(\d{4})$", c)
                if m and sec["table"] == "tn_stats":
                    add(int(m.group(2)), m.group(1), cell, entity=lab,
                        extra={"measure_fr": sec.get("fr_" + c, c)})
                else:
                    add(years_of(sec)[0], c, cell, entity=lab)
            elif kind == "entity_ym":
                a, b = c.split(":")
                if a.isdigit():
                    add(int(a), b, cell, entity=lab)
                else:      # matter:year
                    add(int(b), a, cell, entity=lab, extra={"matter": a, "measure": "cases",
                                                             "measure_fr": "Affaires"})
    return out


# ----------------------------------------------------------------- outputs

COLDOC = {
    "census": "edition the value is taken from (`sgt1922` … `sgt1939`)",
    "table_id": "transcription section name",
    "gallica_ark": "Gallica volume ark (views are numbered within a volume)",
    "source_page": "printed page number",
    "gallica_view": "Gallica view (fNNNN)",
    "year": "year of the figures",
    "section": "part of the yearly statistics (see the notes)",
    "section_fr": "printed heading of that part",
    "court": "French court of first instance as printed (`Tunis`, `Sousse`)",
    "matter": "`civil`, `correctional`, `penal`, `criminal` (Affaires civiles / correctionnelles / pénales / criminelles)",
    "matter_fr": "printed French heading of the matter",
    "tribunal": "court as printed",
    "jurisdiction": "caïdat, kahialik, khalifalik or president of a regional court, as printed",
    "measure": "English code of the printed column (see measure_fr)",
    "measure_fr": "printed French heading",
    "value": "count of cases (integer); money in francs with centimes; percentages as printed",
    "flag": "empty, `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable`, `reprint_corrected`",
}

OUTFILES = defaultdict(lambda: dict(dims=[], paras=[], unit="Unit: number of cases."))
OUTFILES.update({
    "justice_french_criminal": dict(dims=["court", "measure", "measure_fr"], paras=[
        "\"Affaires criminelles et correctionnelles\": criminal cases judged (by the criminal court) and "
        "correctional cases judged after a hearing of both parties (contradictoirement) or by default (par "
        "défaut), per year, for the Tribunal de première instance of Tunis and of Sousse. The printed "
        "*Totaux* (not stored, used for the row check) exclude, says the footnote, \"the default cases "
        "brought back on opposition\" (affaires par défaut revenues sur opposition)."],
        unit="Unit: number of cases."),
    "justice_french_civil": dict(dims=["court", "measure", "measure_fr"], paras=[
        "\"Affaires civiles\": civil judgments by type (contradictory, by default, preparatory, on petition) "
        "per year and court; the printed *Totaux* column is used for the row check."],
        unit="Unit: number of judgments."),
    "justice_french_commercial": dict(dims=["court", "measure", "measure_fr"], paras=[
        "\"Affaires commerciales\": commercial judgments by type, bankruptcies (faillites) and liquidations "
        "per year and court; the printed *Totaux* column is used for the row check."],
        unit="Unit: number of judgments / cases."),
    "justice_ouzara_criminal": dict(dims=["measure", "measure_fr"], paras=[
        "Ouzara (Tunisian Ministry of Justice), \"Affaires criminelles\": cases pending from the previous "
        "year, entered in the year, disposed of by dismissal (non-lieu) or by judgment, and pending at the "
        "end of the year. The printed totals (pending + entered; non-lieu + judgment) are checks only."]),
    "justice_ouzara_appeals": dict(dims=["matter", "tribunal", "measure", "measure_fr"], paras=[
        "\"Appels en matière civile\" / \"Appels en matière correctionnelle\" before the Ouzara, by the "
        "regional court whose decisions were appealed: cases pending at 31 December of the previous year, "
        "entered, and disposed of by confirmation, partial or total reversal, or struck off, and cases "
        "pending at 31 December. The printed TOTAL columns and TOTAUX line are checks only."]),
    "justice_ouzara_correctional_appeals_detail": dict(dims=["matter", "tribunal", "measure", "measure_fr"], paras=[
        "From sgt1926 the Ouzara's correctional appeals table splits the disposed cases by the kind of judgment "
        "appealed (conviction or acquittal) and the decision (confirmed purely and simply, with a reduced or an "
        "increased penalty, or reversed). Earlier editions print the four-way split of "
        "`justice_ouzara_appeals.csv` instead. The TOTAL columns and the TOTAUX line are checks only."]),
    "justice_tunisian_courts_1935_1939": dict(dims=["section", "section_fr", "tribunal", "measure", "measure_fr"],
        paras=["From sgt1935 the Tunisian-justice part of the chapter is recast as one-year statistics of the "
               "\"juridictions de droit commun\" (rule 5: printed once per edition; year = the year in the heading). "
               "`section` codes: `requests_chamber` (I. Chambre des requêtes), `ouzara_civil` / `ouzara_penal` / "
               "`ouzara_indictment` (II. Tribunaux d'appel de l'Ouzara: a) affaires civiles, b) affaires pénales, "
               "c) Chambre des mises en accusation), `first_instance_civil` / `first_instance_penal` (III. "
               "Tribunaux de première instance), `prosecutors` (c) Travaux des parquets), `investigation` (d) "
               "Travaux des chambres d'instruction), `presidents` (IV. Juridictions des présidents et officiers de "
               "police judiciaire, two years per edition), `legal_aid` (Travaux du bureau de l'assistance "
               "judiciaire). Printed TOTAL columns and TOTAUX lines are checks only. The footnote to III a) says: "
               "\"there are no default judgments in Tunisian civil procedure\"."]),
    "justice_regional_courts": dict(dims=["matter", "tribunal", "measure", "measure_fr"], paras=[
        "\"Tribunaux régionaux\": per regional court and year, proceedings pending from the previous year "
        "(Il restait de l'année précédente), entered in the year (Procédures inscrites dans l'année) and "
        "pending at 31 December (Reste au 31 décembre). The TOTAUX line is a check only; the identity "
        "\"pending at the end of year N = pending at the start of N+1\" is also checked."]),
    "justice_caids_presidents": dict(dims=["matter", "jurisdiction", "measure", "measure_fr"], paras=[
        "Cases judged by the caïds, kahias or khalifas (delegated) and by the presidents of the regional "
        "courts, per jurisdiction as printed (\"Caïd de Béja\", \"Kahia de Soliman\", \"Khalifa des "
        "Beni-Zid\", \"Président de la Driba\" …), civil and penal, per year. The TOTAUX line is a check only."]),
    "justice_appeal_rate": dict(dims=["tribunal", "measure", "measure_fr"], paras=[
        "\"Usage du droit d'appel\": per regional court, appealable cases, number of appeals, and the printed "
        "percentage (moyenne pour cent, stored as printed, numeric). The TOTAUX line is a check only for the "
        "counts; the percentages are checked against 100 × appeals / appealable."],
        unit="Unit: number of cases; `*_pct` in percent (two decimals as printed)."),
    "justice_fees_fines": dict(dims=["tribunal", "measure", "measure_fr"], paras=[
        "\"Produit des taxes et amendes\": duties and fines collected per court (Ouzara, regional courts, and "
        "the caïds, kahias, khalifas and presidents of the regional courts on one line). The TOTAL GÉNÉRAL "
        "column and the TOTAUX line are checks only."],
        unit="Unit: francs, centimes kept (two decimals); printed » = 0.00."),
    "justice_french_judgments_execution": dict(dims=["measure", "measure_fr"], paras=[
        "\"Exécution des jugements français\" (Tunisian authorities executing French judgments): judgments "
        "deposited during the year and judgments executed in full; the printed *Reste* (deposited − executed) "
        "is a check only."], unit="Unit: number of judgments."),
})

KEYDIMS = ["year", "court", "matter", "part", "section", "_j", "measure"]


# Cells stored from an earlier printing (flag reprint_corrected): the latest printing fails the printed row
# total and the earlier one passes it. (output, year, court, matter, tribunal/jurisdiction, measure) -> edition.
REPRINT = {
    ("justice_french_civil", 1918, "Tunis", None, None, "preparatory"): "sgt1924",       # 177 (sgt1925+: 122)
    ("justice_french_civil", 1921, "Tunis", None, None, "contradictory"): "sgt1924",     # 857 (sgt1925+: 257)
    ("justice_french_civil", 1920, "Sousse", None, None, "default"): "sgt1924",          # 197 (sgt1925+: 192)
    ("justice_french_civil", 1924, "Sousse", None, None, "contradictory"): "sgt1924",    # 343 (sgt1925+: 363)
    ("justice_french_civil", 1934, "Tunis", None, None, "contradictory"): "sgt1935",     # 7.711 (sgt1936: 7.714)
    ("justice_ouzara_criminal", 1920, None, None, None, "pending_start"): "sgt1923",     # 494 (sgt1924: 484)
}
REPRINT_WHY = {
    ("justice_french_civil", 1918, "Tunis", None, None, "preparatory"):
        "sgt1922-sgt1924 print 177 and the 1918 Tunis total 1.223 = 521 + 293 + 177 + 232; sgt1925-sgt1930 print 122",
    ("justice_french_civil", 1921, "Tunis", None, None, "contradictory"):
        "sgt1922-sgt1924 print 857 and the 1921 Tunis total 2.485 = 857 + 589 + 217 + 822; sgt1925-sgt1930 print 257",
    ("justice_french_civil", 1920, "Sousse", None, None, "default"):
        "sgt1922-sgt1924 print 197 and the 1920 Sousse total 540 = 234 + 197 + 51 + 58; sgt1925-sgt1929 print 192",
    ("justice_french_civil", 1924, "Sousse", None, None, "contradictory"):
        "sgt1924 prints 343 and the 1924 Sousse total 1.038 = 343 + 461 + 42 + 192; sgt1925-sgt1930 print 363",
    ("justice_french_civil", 1934, "Tunis", None, None, "contradictory"):
        "sgt1935 prints 7.711 and the 1934 Tunis total 15.133 = 7.711 + 6.067 + 912 + 443; sgt1936 prints 7.714",
    ("justice_ouzara_criminal", 1920, None, None, None, "pending_start"):
        "sgt1922-sgt1923 print 494 and the 1920 total 1.385 = 494 + 891; sgt1924 prints 484",
}


def apply_reprint(out, kept, allrecs):
    done = []
    for i, r in enumerate(kept):
        k = (out, r["year"], r.get("court"), r.get("matter"), r.get("_j"), r["measure"])
        if k in REPRINT:
            src = [x for x in allrecs if x["census"] == REPRINT[k] and
                   (out, x["year"], x.get("court"), x.get("matter"), x.get("_j"), x["measure"]) == k][0]
            kept[i] = dict(src, flag="reprint_corrected")
            done.append((k, r["census"], r["value"], REPRINT[k], src["value"], REPRINT_WHY[k]))
    return done


def build(write=True):
    secs = []
    for ed in ORDER:
        p = TR / f"justice_{ed}.txt"
        if p.exists():
            secs += parse(p, ed)
    recs = defaultdict(list)
    secs_by_out = defaultdict(list)
    for s in secs:
        if s["table"] not in TABLES:
            raise ValueError(f"unknown table {s['table']} ({s['ed']} f{s['view']})")
        run_checks(s)
        out = TABLES[s["table"]]["out"]
        recs[out] += cells(s)
        secs_by_out[out].append(s)
    result = {}
    for out, rs in recs.items():
        kept, compared, diffs = select_latest(rs, KEYDIMS)
        reprinted = apply_reprint(out, kept, rs)
        topics = {s["table"] for s in secs_by_out[out]}
        n = sum(CHK.n[t] for t in topics)
        fails = [f for t in sorted(topics) for f in CHK.fail[t]]
        kept.sort(key=lambda r: tuple(str(r.get(k) or "") for k in ["matter", "court", "tribunal", "jurisdiction",
                                                                    "measure"]) + (r["year"], ORDER.index(r["census"])))
        result[out] = dict(rows=kept, compared=compared, diffs=diffs, n=n, fails=fails, secs=secs_by_out[out],
                           reprinted=reprinted)
    if write:
        val = {}
        for out, r in result.items():
            spec = dict(OUTFILES[out])
            spec.setdefault("unit", "Unit: number of cases (integer); `»` printed = 0.")
            cols = COMMON + spec["dims"] + ["value", "flag"]
            write_csv(out, cols, r["rows"])
            t0 = [t for t, s in TABLES.items() if s["out"] == out and "title_fr" in s][0]
            rule = RULE.get(out, RULE["_window"])
            paras = list(spec["paras"])
            if r["reprinted"]:
                paras.append("Cells stored from an earlier printing (flag `reprint_corrected`; the latest printing "
                             "fails the printed row total, the earlier one passes it): " + "; ".join(
                                 f"{k[1]} {k[2] or ''} {k[5]}: {fmt(v1)} from {e1} instead of {fmt(v0)} in {e0} "
                                 f"({why})" for k, e0, v0, e1, v1, why in r["reprinted"]) + ".")
            paras += EXTRA.get(out, [])
            paras.append(SURVEY_REF)
            write_notes(out, CHAPTER, SCRIPT, r["rows"], cols, COLDOC, TABLES[t0]["title_fr"],
                        TABLES[t0]["title_en"], paras, r["n"], r["fails"], r["compared"], r["diffs"],
                        coverage_lines(r["secs"]), rule, spec["unit"])
            val[out] = dict(rows=len(r["rows"]), checks=r["n"], failed=r["fails"],
                            overlap_compared=r["compared"], overlap_diffs=[list(d) for d in r["diffs"]],
                            reprint_corrected=[list(x) for x in r["reprinted"]])
        val["_chapter_views"] = CHAPTER_VIEWS
        val["_survey"] = SURVEY
        write_validation(OUT / "justice_validation.json", val)
        write_survey()
    return result


def fmt(x):
    return format(x, "f") if x is not None else "NA"


RULE = {
    "_window": ("Printed for overlapping year windows (ten years for the French courts until sgt1930, three from "
                "sgt1935; five years for the Ouzara and the regional courts; two years for the caïds and "
                "presidents): each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; "
                "`census` = that edition); every other printing of the same cell is compared below and not stored."),
}
for _o in ("justice_ouzara_appeals", "justice_ouzara_correctional_appeals_detail", "justice_appeal_rate",
           "justice_fees_fines", "justice_french_judgments_execution", "justice_regional_prosecutors",
           "justice_regional_investigation", "justice_indictment_chamber", "justice_revision_chamber",
           "justice_tunisian_courts_1935_1939"):
    RULE[_o] = ("Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, "
                "`year` = the year of the figures; no year is printed twice, except the two-year columns of the "
                "presidents' table (section `presidents`), where the earlier year is taken from the later edition "
                "and compared (rule 4).")

EXTRA = {
    "justice_ouzara_criminal": [
        "Up to sgt1923 the disposals are printed \"par non-lieu / par jugement\" (`out_no_case`, `out_judgment`); "
        "from sgt1924 the same lines read \"par acquittement / par condamnation\" (`out_acquittal`, "
        "`out_conviction`), and sgt1924-sgt1925 put all of 1922-1924 under \"condamnation\" (0 acquittals) while "
        "sgt1926-sgt1928 split them (e.g. 1922: 67 + 674). The two pairs are kept as separate measures; within each "
        "pair the latest printing is stored and the earlier ones are listed below."],
    "justice_caids_presidents": [
        "The list of jurisdictions changes almost every edition (new khalifaliks, renamings, Tamerza printed "
        "\"Supprimé\" from 1929, stored NA with flag `not_applicable`). Names are as printed in the edition the "
        "value is taken from, normalised to \"Caïd de …\", \"Kahia de …\", \"Khalifa(t) de …\", "
        "\"Président (du Tribunal) de …\" (the printed lines carry a dash for the repeated title). sgt1922-sgt1924 "
        "print \"Khalifa de Sbeitla\" twice (the second line from sgt1923; stored as \"Khalifa de Sbeitla (second "
        "line)\"; its figures continue from sgt1925 as \"Khalifat de Sbikha\" and are matched to it). Printings "
        "are matched on the place name (titles, accents and spelling variants such as Djemal / Djemmal, Djelass / "
        "Jlass normalised). In sgt1924 the 1924 column of the khalifas from Beni-Zid to Zarzis is printed one line "
        "off the 1923 column (sgt1925 prints the same figures one line lower, on Djemmal … Zarzis, consistent with "
        "its new list): 1924 is stored from sgt1925 and the sgt1924 cells appear among the differences below. "
        "sgt1924 and sgt1925 also swap the 1924 figures of the presidents of Sousse and Sfax. The \"A reporter\" / \"Report\" lines of sgt1925-sgt1930 are checks only.",
        "sgt1925 prints the 1925 figures of the khalifalik of Touazine on the Utique line (Utique 136 / 114, "
        "Touazine »); sgt1926 prints them on the Touazine line (Touazine 136 / 114, Utique » / 17): the later "
        "printing is stored and the difference is listed below."],
    "justice_fees_fines": [
        "From sgt1936 the columns are printed in the order Amendes, Droits d'enrôlement, Droits de chancellerie; "
        "they are mapped to the same three measure codes (the headings change: \"droits de timbre et "
        "d'enregistrement\" up to sgt1930, \"taxes d'enrôlement\" from sgt1935; `measure_fr` gives the heading "
        "of each edition). sgt1930 prints a line without a label between Gabès and the presidents' line (by "
        "elimination Béja, the eighth regional court from 1930), stored as \"(line printed without label)\". "
        "sgt1939 adds the new regional courts of Bizerte, Nabeul, Moknine and Djerba."],
    "justice_appeal_rate": [
        "Percentages are stored as printed (\"moyenne pour cent\"; sgt1929 Driba civil is printed 27 002, sgt1935 "
        "Driba penal 13 178, i.e. with three decimals). The TOTAUX line prints no percentage from sgt1924 (NA, "
        "`not_applicable`); Béja (opened 1925) prints » until sgt1929 (stored 0 for counts, NA for percentages)."],
    "justice_french_commercial": [
        "sgt1939 prints » in the Tunis TOTAUX column for 1937 and 1938 (stored NA, `not_applicable`; the row check "
        "is skipped)."],
}

SURVEY_REF = ("The page-by-page survey of the chapter in every edition (every table found, with views) is in "
              "`justice_survey.md` and in `justice_validation.json` (`_survey`).")

SURVEY = {
    "sgt1922": "f85 chapter title; f86 blank; f87 Tribunal de Tunis a) affaires criminelles et correctionnelles "
               "1913-1922, b) affaires civiles; f88 c) affaires commerciales, d) audiences régulières et foraines des "
               "justices de paix du ressort (text); f89 Tribunal de Sousse a), b); f90 c), d) audiences (text); f91 "
               "Justice tunisienne, Ouzara a) affaires criminelles 1918-1922, b) appels en matière civile, c) appels en "
               "matière correctionnelle; f92 Tribunaux régionaux 1918-1922, affaires civiles and correctionnelles "
               "(page printed sideways); f93 juridiction des caïds, kahias ou khalifas délégués et présidents des "
               "tribunaux régionaux 1921-1922; f94 Divers a) usage du droit d'appel, b) produit des taxes et amendes, "
               "c) exécution des jugements français. Next chapter (Établissements pénitentiaires) at f95.",
    "sgt1923": "f569 title; f570-f577 as sgt1922 (Tunis f570-f571, Sousse f572-f573, Ouzara f574, tribunaux "
               "régionaux 1919-1923 f575 sideways, caïds 1922-1923 f576, divers a)-c) f577); f578 blank.",
    "sgt1924": "f1059 title; f1060-f1067 as sgt1922 (Tunis f1060-f1061, Sousse f1062-f1063, Ouzara f1064, "
               "régionaux 1920-1924 f1065 sideways, caïds f1066, divers f1067); f1068 blank.",
    "sgt1925": "f93 title (f92 is the end of chapter III); f94 Justice française a) criminelles et correctionnelles, "
               "b) civiles 1916-1925, Tunis and Sousse side by side; f95 c) commerciales, audiences of the justices "
               "of the peace (Tunis); f96 audiences (Sousse); f97 Ouzara a) criminelles 1921-1925, b) appels civils, "
               "c) appels correctionnels; f98 tribunaux régionaux a) affaires civiles, b) affaires correctionnelles "
               "(1921-1922; 1923-1925 on f99, with jugements de condamnation / d'acquittement); f99 travaux des "
               "parquets; f100 travaux des chambres d'instruction, travaux de la Chambre d'accusation; f101-f102 "
               "juridiction des présidents des tribunaux régionaux, justices cantonales, caïdats, kahialiks et "
               "khalifaliks 1924-1925; f103 divers a) droit d'appel, b) taxes et amendes; f104 Chambre de révision "
               "a)-c), d) bureau d'exécution des jugements français.",
    "sgt1926": "f643 title; f644 a), b) 1917-1926; f645 c), audiences (Tunis); f646 audiences (Sousse); f647 Ouzara "
               "a)-c) (appels correctionnels now split by kind of judgment appealed); f648-f649 tribunaux "
               "régionaux 1922-1926; f649 parquets; f650 chambres d'instruction, Chambre d'accusation; f651-f652 "
               "présidents, caïds etc. 1925-1926; f653 divers; f654 Chambre de révision, exécution.",
    "sgt1927": "f105 title; f106 a), b) 1918-1927; f107 c), d) audiences Tunis; f108 e) audiences Sousse; f109 "
               "Ouzara; f110-f111 régionaux 1923-1927; f111 parquets; f112 instruction, accusation; f113-f114 "
               "présidents 1926-1927; f115 divers; f116 révision, exécution.",
    "sgt1928": "f629 title; f630 a), b) 1919-1928; f631 c), audiences Tunis; f632 audiences Sousse; f633 Ouzara; "
               "f634-f635 régionaux 1924-1928; f635 parquets; f636 instruction, accusation; f637-f638 présidents "
               "1927-1928; f639 divers; f640 révision, exécution.",
    "sgt1929": "f107 title; f108 a), b) 1920-1929; f109 c), audiences Tunis; f110 audiences Sousse; f111 Ouzara; "
               "f112-f113 régionaux 1925-1929; f113 parquets; f114 instruction, accusation; f115-f116 présidents "
               "1928-1929; f117 divers; f118 révision, exécution (now with judgments left from earlier years and "
               "attempts at execution).",
    "sgt1930": "f641 title; f642 a), b) 1921-1930; f643 c), audiences Tunis; f644 audiences Sousse; f645 Ouzara; "
               "f646-f647 régionaux 1926-1930 (Béja from 1930); f647 parquets; f648 instruction, accusation; "
               "f649-f650 présidents 1929-1930; f651 divers; f652 révision, exécution.",
    "sgt1935": "f71 title; f72 Tribunaux de Tunis et de Sousse a)-c) 1933-1935; f73 d) audiences (Tunis); f74 e) "
               "audiences (Sousse); f75 Justice tunisienne, juridictions de droit commun, statistique 1935: I. "
               "Chambre des requêtes, II. Tribunaux d'appel de l'Ouzara a) civiles, b) pénales, c) Chambre des "
               "mises en accusation; f76 III. Tribunaux de première instance a) civiles, b) pénales; f77 c) "
               "parquets, d) chambres d'instruction; f78 IV. juridictions des présidents et officiers de police "
               "judiciaire 1934-1935, V. bureau d'exécution des jugements français, VI. assistance judiciaire; f79 "
               "VII. usage du droit d'appel, VIII. produit des taxes et amendes; f80 blank.",
    "sgt1936": "f52 title (chapter IV Justice, which also holds the prisons tables f58-f61); f53 blank; f54 "
               "Tribunaux de Tunis et de Sousse, criminelles et correctionnelles, civiles, commerciales 1934-1936; "
               "f55 juridictions de droit commun 1936: I. Chambre des requêtes, II. Ouzara 1° civiles, 2° pénales, "
               "3° mises en accusation; f56 III. première instance 1° civiles, 2° pénales (contradictoires / par "
               "défaut), IV. présidents et officiers de police judiciaire 1935-1936; f57 V. assistance judiciaire, "
               "VI. droit d'appel, VII. taxes et amendes. No audiences table, no parquets / instruction tables.",
    "sgt1939": "f47 title (chapter IV, prisons from f53); f48 blank; f49 Tribunaux de Tunis et de Sousse 1937-1939; "
               "f50 I. Chambre des requêtes, II. Ouzara 1°-3°; f51 III. première instance 1°, 2°, IV. présidents et "
               "juges cantonaux 1938-1939; f52 V. assistance judiciaire, VI. droit d'appel, VII. taxes et amendes "
               "(with the new courts of Bizerte, Nabeul, Moknine, Djerba).",
}

NOT_DONE = ("Not transcribed: the text tables \"Audiences régulières et foraines des justices de paix du ressort\" "
            "(per justice of the peace: localities of the itinerant hearings, periodicity, days of hearing; "
            "sgt1922 f88, f90; sgt1923 f571, f573; sgt1924 f1061, f1063; sgt1925 f95-f96; sgt1926 f645-f646; "
            "sgt1927 f107-f108; sgt1928 f631-f632; sgt1929 f109-f110; sgt1930 f643-f644; sgt1935 f73-f74). "
            "They hold no counts, only schedules in running text.")


def write_survey():
    L = ["# Justice chapter: survey of every edition", "",
         "Page-by-page survey of chapter IV *Justice* of the *Statistique générale de la Tunisie* (views confirmed "
         "on the images; the view before each range is the end of the previous chapter or a blank page, the view "
         "after it the next chapter's title page). Extraction: `extract_justice.py`.", "",
         "| edition | ark | views (justice) |", "|---|---|---|"]
    L += [f"| {e} | `{EDITIONS[e]}` | {a}–{b} |" for e, (a, b) in CHAPTER_VIEWS.items()]
    L += ["", "## Tables per edition", ""]
    L += [f"- **{e}**: {t}" for e, t in SURVEY.items()]
    L += ["", "## Not transcribed", "", NOT_DONE, ""]
    (OUT / "justice_survey.md").write_text("\n".join(L) + "\n")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    res = build(write=(mode == "build"))
    tot_n = tot_f = 0
    for out, r in sorted(res.items()):
        tot_n += r["n"]
        tot_f += len(r["fails"])
        print(f"{out}: {len(r['rows'])} rows, {r['n']} checks, {len(r['fails'])} failed, "
              f"{r['compared']} compared, {len(r['diffs'])} diffs")
        for f in r["fails"]:
            print("   FAIL", f)
        for d in r["diffs"]:
            print("   DIFF", d)
    print(f"total checks {tot_n}, failed {tot_f}")


if __name__ == "__main__":
    main()
