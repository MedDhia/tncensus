#!/usr/bin/env python3
"""Prisons chapter (chapter V, *Établissements pénitentiaires*; from sgt1936 printed inside chapter IV
*Justice*) of the Statistique générale de la Tunisie, 12 editions sgt1922-sgt1939.

  python3 extract_prisons.py check   parse the transcriptions, run every check, print failures
  python3 extract_prisons.py build   ... and write csv/prisons_*.csv, their .md notes, csv/prisons_survey.md
                                     and csv/prisons_validation.json

Source of truth: transcribed/prisons_<edition>.txt (format in yb_tables.py). Transcribed so far: the
"Récapitulation du chiffre des détenus" (yearly prison population: number at 1 January, entries, releases,
number at 31 December, days of detention, daily average), printed for overlapping year windows in every edition
(SPEC_ADDENDUM rule 4: each year from the latest edition printing it, every other printing compared).
The other tables of the chapter are listed in csv/prisons_survey.md and are not transcribed yet.
"""
import json
import sys
from collections import defaultdict
from decimal import Decimal

from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parent))  # shared helper yb_tables.py
from yb_tables import (COMMON, EDITIONS, ORDER, OUT, TR, Checks, check_col_totals, check_row, coverage_lines,
                       is_total, parse, select_latest, ssum, where, write_csv, write_notes, write_validation,
                       years_of)

CHAPTER = "Établissements pénitentiaires"
SCRIPT = "extract_prisons.py"
CHK = Checks()

# Views of the prisons tables (chapter title .. last view before the next chapter), confirmed on the images.
CHAPTER_VIEWS = {
    "sgt1922": (95, 102), "sgt1923": (579, 586), "sgt1924": (1069, 1076), "sgt1925": (105, 112),
    "sgt1926": (655, 664), "sgt1927": (117, 126), "sgt1928": (641, 650), "sgt1929": (119, 128),
    "sgt1930": (653, 662), "sgt1935": (81, 90), "sgt1936": (58, 61), "sgt1939": (53, 56),
}

M = {"start": "Effectif au 1er janvier", "entries": "Nombre d'entrées", "exits": "Nombre de sorties",
     "end": "Effectif au 31 décembre", "detention_days": "Nombre de journées de détention",
     "average": "Effectif moyen"}

# (year, measure) -> edition whose printing is stored instead of the latest (flag reprint_corrected)
REPRINT = {(1934, "end"): "sgt1935"}
REPRINT_WHY = {(1934, "end"): "sgt1936 prints the 31 December 1934 population with its middle digit broken "
                              "(\"2 6·8\"); sgt1935 prints 2.638, which is also sgt1935's and sgt1936's 1 January 1935 "
                              "figure"}


def run_checks(sec):
    rows = {int(r["label"]): r["cells"] for r in sec["rows"]}
    for y, c in rows.items():
        g = {k: c[k].value for k in c}
        CHK.eq("recap", f"{where(sec)} {y}: end = start + entries - exits",
               ssum([g["start"], g["entries"], None if g["exits"] is None else -g["exits"]]), g["end"])
        if g["detention_days"] is not None and g["average"] is not None:
            days = 366 if y % 4 == 0 else 365
            CHK.eq("recap", f"{where(sec)} {y}: average = detention days / {days} (to 1)",
                   (g["detention_days"] / days).quantize(Decimal(1)), g["average"], tol=Decimal(1))
        if y + 1 in rows:
            CHK.eq("recap", f"{where(sec)} start {y + 1} = end {y}", g["end"], rows[y + 1]["start"].value)


def cells(sec):
    out = []
    for r in sec["rows"]:
        for m, c in r["cells"].items():
            out.append({"census": sec["ed"], "table_id": sec["table"], "gallica_ark": sec["ark"],
                        "source_page": sec["page"], "gallica_view": sec["view"], "year": int(r["label"]),
                        "measure": m, "measure_fr": M[m], "value": c.value, "flag": c.flag})
    return out


COLDOC = {
    "census": "edition the value is taken from (`sgt1922` … `sgt1939`)",
    "table_id": "transcription section name (`recap`)",
    "gallica_ark": "Gallica volume ark (views are numbered within a volume)",
    "source_page": "printed page number",
    "gallica_view": "Gallica view (fNNNN)",
    "year": "calendar year of the figures",
    "measure": "`start`, `entries`, `exits`, `end`, `detention_days`, `average`",
    "measure_fr": "printed column heading",
    "value": "number of prisoners (start, end, average), of entries / releases, or of days of detention",
    "flag": "empty, `illegible` or `reprint_corrected`",
}

SURVEY = {
    "sgt1922": "f95 chapter title; f96 blank; f97 Administration a) répartition des condamnés d'après la nationalité, "
               "l'âge, le sexe et la catégorie pénale, b) d'après la nationalité, la nature du délit et la catégorie "
               "pénale; f98 c) journées de travail des détenus (by establishment and kind of work), Mouvement de la "
               "population a) mouvement général d'entrée et de sortie, effectif au 31 décembre (men and boys); f99 d) "
               "tableau comparatif des dépenses et des journées de détention (by prison; personnel, upkeep, food, "
               "price of the day of detention, products of the work), population au 31 décembre; f100 b) mouvement "
               "général (women), c) Prison de Tunis : transfèrements; f101 d) état numérique des décès par prison et "
               "par maladie; f102 e) état comparatif du personnel de garde avec l'effectif journalier maximum, f) "
               "récapitulation 1913-1922. Next chapter at f103.",
    "sgt1923": "f579 title; f580 blank; f581-f586 as sgt1922 (a), b) f581; c), mouvement a) f582; d) f583; mouvement "
               "b), transfèrements f584; décès f585; personnel de garde, récapitulation 1914-1923 f586).",
    "sgt1924": "f1069 title; f1070 blank; f1071-f1076 as sgt1922 (décès f1075; personnel, récapitulation 1915-1924 "
               "f1076).",
    "sgt1925": "f105 title; f106 blank; f107 a), b); f108 c) journées de travail, e) mouvement général (men); f109 d) "
               "dépenses et journées de détention; f110 f) mouvement général (women), g) Prison de Tunis : "
               "transfèrements; f111 h) décès par prison et par maladie; f112 i) personnel de garde, j) récapitulation "
               "1924-1925.",
    "sgt1926": "f655 title; f656 blank; f657 a), b); f658-f659 c) journées de travail, d) dépenses (spread); "
               "f660-f661 e), f) mouvement général (spread); f662 g) service des transfèrements, h) décès; f663 i) "
               "personnel de garde, j) récapitulation 1925-1926; f664 blank.",
    "sgt1927": "f117 title; f118 blank; f119 a), b); f120-f121 c), d) (with totaux généraux dépenses et recettes); "
               "f122-f123 e), f); f124 g), h); f125 i), j) 1926-1927; f126 blank.",
    "sgt1928": "f641 title; f642 blank; f643 a), b); f644-f645 c), d); f646-f647 e), f); f648 g), h); f649 i), j) "
               "1927-1928; f650 blank.",
    "sgt1929": "f119 title; f120 blank; f121 a), b); f122-f123 c), d); f124-f125 e), f); f126 g), h); f127 i), j) "
               "1928-1929; f128 blank.",
    "sgt1930": "f653 title; f654 blank; f655 a), b); f656-f657 c), d); f658-f659 e) mouvement général; f660 g), h); "
               "f661 i), j) 1929-1930; f662 blank.",
    "sgt1935": "f81 title; f82 blank; f83 a), b); f84-f85 d) dépenses (no c) table); f86-f87 e), f); f88 g), h); "
               "f89 i), j) 1933-1935; f90 blank.",
    "sgt1936": "inside chapter IV (Justice): f58 répartition des condamnés d'après la nationalité, l'âge, le sexe; "
               "d'après la nationalité et la nature du délit; f59-f60 mouvement général d'entrée et de sortie (two "
               "tables); f61 récapitulation du chiffre des détenus 1932-1936. f62 = chapter V Propriété foncière.",
    "sgt1939": "inside chapter IV (Justice): f53 répartition par nationalité, âge, sexe; par nationalité et nature du "
               "délit; f54-f55 mouvement général d'entrée et de sortie (two tables); f56 récapitulation 1935-1939. "
               "f57 = chapter V Propriété foncière.",
}

NOT_DONE = ("Transcribed: the récapitulation (prisons_population_recap), a) condemned prisoners by nationality, age, "
            "sex and penal category (prisons_condemned_nationality_age), b) by nationality, offence and sentence "
            "(prisons_condemned_offence), c) days of work (prisons_work_days), d) expenditure and days of detention "
            "for sgt1922-sgt1928 (prisons_expenditure). Not transcribed yet: d) for sgt1929, sgt1930 and sgt1935; "
            "mouvement général d'entrée et de sortie by establishment (two "
            "tables); transfers; deaths by prison and disease; guard staff compared with the maximum daily "
            "population. Their views are listed above, per edition.")


def write_survey():
    L = ["# Prisons chapter: survey of every edition", "",
         "Page-by-page survey of the *Établissements pénitentiaires* tables (chapter V up to sgt1935; printed at the "
         "end of chapter IV *Justice* in sgt1936 and sgt1939). Views confirmed on the images. Extraction: "
         "`extract_prisons.py`.", "", "| edition | ark | views |", "|---|---|---|"]
    L += [f"| {e} | `{EDITIONS[e]}` | {a}–{b} |" for e, (a, b) in CHAPTER_VIEWS.items()]
    L += ["", "## Tables per edition", ""] + [f"- **{e}**: {t}" for e, t in SURVEY.items()]
    L += ["", "## Not transcribed", "", NOT_DONE, ""]
    (OUT / "prisons_survey.md").write_text("\n".join(L) + "\n")


def build(write=True):
    secs = []
    for ed in ORDER:
        p = TR / f"prisons_{ed}.txt"
        if p.exists():
            secs += parse(p, ed)
    tables = defaultdict(list)
    for s in secs:
        tables[s["table"]].append(s)
    recs = []
    for s in tables["recap"]:
        run_checks(s)
        recs += cells(s)
    kept, compared, diffs = select_latest(recs, ["year", "measure"])
    reprinted = []
    for i, r in enumerate(kept):
        k = (r["year"], r["measure"])
        if k in REPRINT:
            src = [x for x in recs if x["census"] == REPRINT[k] and (x["year"], x["measure"]) == k][0]
            reprinted.append((k, r["census"], r["value"], REPRINT[k], src["value"], REPRINT_WHY[k]))
            kept[i] = dict(src, flag="reprint_corrected")
    kept.sort(key=lambda r: (r["year"], list(M).index(r["measure"])))
    fails = CHK.fail["recap"]
    if write:
        out = "prisons_population_recap"
        cols = COMMON + ["measure", "measure_fr", "value", "flag"]
        write_csv(out, cols, kept)
        paras = [
            "\"Récapitulation du chiffre des détenus\" (\"Récapitulation\" with ten years up to sgt1924, two years "
            "sgt1925-sgt1930, three in sgt1935, five in sgt1936 and sgt1939): for all the prisons of the Regency, "
            "the number of prisoners at 1 January, entries, releases, number at 31 December, days of detention and "
            "the average daily population (*effectif moyen*). The year 1931 is not printed by any edition; 1932 is "
            "printed only by sgt1936.",
            "Checks: end = start + entries − releases; start of year N+1 = end of year N; average = days of "
            "detention / days in the year (to ±1).",
            "Cells stored from an earlier printing (flag `reprint_corrected`): " + "; ".join(
                f"{k[0]} {k[1]}: {v1} from {e1} ({why})" for k, e0, v0, e1, v1, why in reprinted) + ".",
            "sgt1924 reprints 1915 with end 3.082 and 1.012.231 days (sgt1922-sgt1923: 2.874 and 1.092.231); the "
            "latest printing is stored by rule 4 (3.082 also satisfies 3.147 + 23.044 − 23.109), the earlier "
            "figures are listed among the differences.",
            "Survey of the whole chapter in every edition, and the tables not yet transcribed: `prisons_survey.md`."]
        write_notes(out, CHAPTER, SCRIPT, kept, cols, COLDOC,
                    "Récapitulation du chiffre des détenus", "Prison population: yearly summary", paras,
                    CHK.n["recap"], fails, compared, diffs, coverage_lines(tables["recap"]),
                    "Printed for overlapping year windows: each year is taken from the **latest** edition that prints "
                    "it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing is compared below.",
                    "Unit: persons (population figures and average), entries / releases (count), days of detention.")
        write_validation(OUT / "prisons_validation.json", {
            out: dict(rows=len(kept), checks=CHK.n["recap"], failed=fails, overlap_compared=compared,
                      overlap_diffs=[list(d) for d in diffs], reprint_corrected=[list(x) for x in reprinted]),
            "_chapter_views": CHAPTER_VIEWS, "_survey": SURVEY, "_not_transcribed": NOT_DONE})
        write_survey()
    others = build_tables(tables, write)
    if write:
        v = json.loads((OUT / "prisons_validation.json").read_text())
        v.update(others)
        write_validation(OUT / "prisons_validation.json", v)
    return kept, compared, diffs, fails, others


# ======================================================================= the other tables of the chapter
# Printed once per edition, for the edition year (SPEC_ADDENDUM rule 5): every edition kept, with `year`;
# a cell printed by two editions for the same year would be taken from the later one and compared
# (select_latest). Printed total lines and total columns are used for the checks only.

NAT = {  # nationality line label as printed -> code
    "Français": "french", "— (Algériens)": "algerian", "Algériens": "algerian", "Italiens": "italian",
    "Anglais (Maltais)": "maltese", "Anglo-Maltais": "maltese", "Maltais": "maltese", "Grecs": "greek",
    "Espagnols": "spanish", "Serbes": "serbian", "Danois": "danish", "Autres européens": "other_european",
    "Musulmans (sujet musulmans)": "tunisian_muslim", "Israélites (sujet musulmans)": "tunisian_jewish",
    "Tunisiens musulmans": "tunisian_muslim", "Tunisiens israélites": "tunisian_jewish",
    "Tripolitains": "tripolitanian", "Marocains": "moroccan", "Divers": "other",
}

AGE_COLS = ["age_0_10", "age_11_15", "age_16_20", "age_21_30", "age_31_40", "age_41_50", "age_51_plus"]
CONDEMNED_COLS = {  # column code -> (breakdown, printed heading)
    "age_0_10": ("age", "Catégorie par âge : 10 ans et au-dessous"),
    "age_11_15": ("age", "Catégorie par âge : 11 ans à 15 ans"),
    "age_16_20": ("age", "Catégorie par âge : 16 ans à 20 ans"),
    "age_21_30": ("age", "Catégorie par âge : 21 ans à 30 ans"),
    "age_31_40": ("age", "Catégorie par âge : 31 ans à 40 ans"),
    "age_41_50": ("age", "Catégorie par âge : 41 ans à 50 ans"),
    "age_51_plus": ("age", "Catégorie par âge : 51 ans et au-dessus"),
    "male": ("sex", "Catégorie par sexe : sexe masculin"),
    "female": ("sex", "Catégorie par sexe : sexe féminin"),
    "first_offender": ("penal_category", "Catégorie pénale : primaires"),
    "recidivist": ("penal_category", "Catégorie pénale : récidivistes"),
}

# (edition, section, row label, column) -> reason: printed cells flagged total_mismatch (printed value kept)
MISMATCH = {}
for _c in AGE_COLS:
    MISMATCH[("sgt1922", "condemned_age", "Italiens", _c)] = (
        "the seven age groups sum to 141, the printed total, the sex and the penal-category columns to 144; the "
        "age-group column totals agree with the lines, so the shortfall of 3 is in the printing of this line")
MISMATCH[("sgt1922", "condemned_offence", "Vol", "ps.Français")] = (
    "emprisonnement ≤ 1 an, Vol, Français printed 11: the line sums to 3.032 for a printed 3.035 and the Français "
    "column to 28 for a printed 31, both 3 short at this cell")
MISMATCH[("sgt1922", "work_days", "Sfax", "espadrilles_alfa")] = (
    "Sfax, Espadrilles, alfa printed 1.845: the Sfax line sums to 6.512 for a printed 6.482 and the column to "
    "34.842 for a printed 34.812, both 30 over at this cell")
MISMATCH[("sgt1923", "work_days", "Tunis", "espadrilles_alfa")] = (
    "Tunis, Espadrilles, alfa printed 1.851: neither the Tunis total (92.783, the other cells sum to exactly that) "
    "nor the column total (41.130, the other cells sum to exactly that) counts it")
for _k, _why in {
        ("sgt1923", "Bardo", "personnel"): "printed 33.532,38: the Bardo line sums to 86.421,59 for a printed total "
                                           "86.421,99 and the column to 597.547,85 for 597.548,25, both 0,40 short",
        ("sgt1923", "Béja", "food"): "printed 11.249,14: the Béja line and the nourriture column are both 0,05 short "
                                     "of their printed totals",
        ("sgt1923", "Kairouan", "price_per_day"): "printed 1,2518; 66.170,63 / 53.715 days = 1,2319",
        ("sgt1924", "Kairouan", "personnel"): "printed 16.357,56: the Kairouan line and the personnel column are "
                                              "both 200 short of their printed totals",
        ("sgt1926", "Le Kef", "food"): "printed 49.693,34: the Le Kef line and the nourriture column are both 1,00 "
                                       "short of their printed totals",
        ("sgt1926", "En Algérie", "total"): "printed 212.043,07 for a nourriture of 212.043,75 and nothing else; the "
                                            "Totaux généraux (2.863.528,66) needs 212.043,75",
        ("sgt1927", "Porto-Farina", "upkeep"): "printed 50.685,73: the Porto-Farina line and the dépenses diverses "
                                               "column are both 0,20 short of their printed totals",
        ("sgt1928", "Sfax", "upkeep"): "printed 327.485,87; the Sfax total 159.829,79 needs 37.475,87, the figure "
                                       "printed on the Sousse line below",
        ("sgt1928", "Sousse", "upkeep"): "printed 37.475,87 (the Sfax figure); the Sousse total 186.151,84 needs "
                                         "28.500,53",
        ("sgt1928", "Gabès", "total"): "printed 109.392,95 for components summing to 109.492,95; the column total "
                                       "agrees with the other cells only if Gabès or Sousse dépenses diverses "
                                       "differ by the same 100 (see the failed checks)",
}.items():
    MISMATCH[(_k[0], "expenditure", _k[1], _k[2])] = _why
MISMATCH[("sgt1929", "condemned_age", "Français", "male")] = (
    "35 men and 0 women for a printed total of 34 (the ages sum to 34) and the men column sums to 7.655 for a "
    "printed 7.654: the 35 is one too many")
for _r in ["Français", "Algériens", "Italiens", "Maltais", "Grecs", "Tunisiens israélites", "Marocains",
           "Tripolitains", "Divers"]:
    for _c in ["first_offender", "recidivist"]:
        MISMATCH[("sgt1929", "condemned_age", _r, _c)] = (
            "primaires + récidivistes do not give the line total on nine of the twelve lines and the two columns "
            "do not sum to their printed totals (4.109 for 4.035, 3.692 for 3.795); several of these cells repeat "
            "sgt1928's (Français 22 / 19, Algériens and Italiens primaires 89 and 91, Divers récidivistes 38)")


def chk_condemned(chk, topic, sec):
    has_age_total = "age_total" in sec["cols"]
    check_row(chk, topic, sec, "total", AGE_COLS)
    if has_age_total:
        check_row(chk, topic, sec, "age_total", AGE_COLS)
    check_row(chk, topic, sec, "total", ["male", "female"])
    check_row(chk, topic, sec, "total", ["first_offender", "recidivist"])
    check_col_totals(chk, topic, sec)


def cells_condemned(sec):
    out = []
    for r in sec["rows"]:
        if is_total(r["label"]):
            continue
        for col, (bd, fr) in CONDEMNED_COLS.items():
            c = r["cells"][col]
            out.append(dict(base(sec), nationality=NAT[r["label"]], nationality_fr=r["label"], breakdown=bd,
                            category=col, category_fr=fr, value=c.value, flag=c.flag, _row=r["label"], _col=col))
    return out

OFFENCE = {
    "Meurtre": "murder", "Coups, blessures, agressions": "assault", "Coups, blessures": "assault",
    "Coups, blessures et agressions": "assault", "Attentat à la pudeur": "indecent_assault", "Vol": "theft",
    "Ivresse": "drunkenness", "Délit de pacage": "grazing_offence", "Délit de paccage": "grazing_offence",
    "Evasions": "escape", "Faillis": "bankrupts", "Dettiers": "debtors", "Faillis et dettiers": "bankrupts_debtors",
    "Politiques": "political", "Divers": "other",
}
PENALTY = {"dp": ("death", "Peine capitale"), "hl": ("hard_labour", "Travaux forcés"),
           "rc": ("reclusion", "Réclusion"),
           "pl": ("prison_over_1y", "Emprisonnement à 1 an et 1 jour et au-dessus"),
           "ps": ("prison_1y_or_less", "Emprisonnement à 1 an et au-dessous")}
COLNAT = {"Français": "french", "Européens": "european", "Algériens": "algerian", "Musulmans": "tunisian_muslim",
          "Israélites": "tunisian_jewish", "Tripolitains": "tripolitanian", "Divers": "other"}

# (edition, section, line label as stored, column) -> reason: cells printed on another line (flag row_realigned)
REALIGNED = {
    **{("sgt1925", "work_days", lab, "int_scourtins_mats_brooms"): (
        f"printed one line higher, on the {up} line; on the printed line neither that line nor this one gives its "
        f"printed Total par établissement, stored here both do") for lab, up in
        [("Gabès", "Bizerte"), ("La Goulette", "Gafsa"), ("Sfax", "Porto-Farina"), ("Dj.-Djougar", "Sousse")]},
    ("sgt1929", "condemned_offence", "Attentat à la pudeur", "hl.Européens"): (
        "printed on the line above (Coups, blessures, agressions); with the 1 there neither line gives its printed "
        "total (3 for 2, 3 for 4), with it here both do"),
}


def offence_groups(sec):
    g = defaultdict(list)
    for c in sec["cols"]:
        if "." in c:
            p, n = c.split(".")
            if n != "Total":
                g[p].append(c)
    return g


def chk_offence(chk, topic, sec):
    g = offence_groups(sec)
    for p, cs in g.items():
        if f"{p}.Total" in sec["cols"]:
            extra = g["dp"] if p == "hl" and sec.get("hl_total_includes_death") else []
            check_row(chk, topic, sec, f"{p}.Total", extra + cs)
    if "grand_total" in sec["cols"]:
        check_row(chk, topic, sec, "grand_total", [c for c in g.get("dp", [])] +
                  [f"{p}.Total" for p in g if p != "dp"])
    check_col_totals(chk, topic, sec)


def cells_offence(sec):
    out = []
    g = offence_groups(sec)
    for r in sec["rows"]:
        if is_total(r["label"]):
            continue
        for p, cs in g.items():
            for col in cs:
                n = col.split(".")[1]
                if n == "Tunisiens":
                    nat = "tunisian_muslim" if f"{p}.Israélites" in sec["cols"] else "tunisian"
                else:
                    nat = COLNAT[n]
                c = r["cells"][col]
                fr = n if n not in ("Musulmans", "Israélites") or sec["ed"] < "sgt1926" else f"Tunisiens : {n}"
                out.append(dict(base(sec), offence=OFFENCE[r["label"]], offence_fr=r["label"], penalty=PENALTY[p][0],
                                penalty_fr=PENALTY[p][1], nationality=nat, nationality_fr=fr, value=c.value,
                                flag=c.flag, _row=r["label"], _col=col))
    return out


def cross_offence_age(chk, tables):
    """Every edition: grand total of the offence table = total of the nationality / age table."""
    for sb in tables.get("condemned_offence", []):
        sa = [s for s in tables.get("condemned_age", []) if s["ed"] == sb["ed"]]
        if not sa:
            continue
        tot_a = [r for r in sa[0]["rows"] if is_total(r["label"])][0]["cells"]["total"].value
        tb = [r for r in sb["rows"] if is_total(r["label"])][0]["cells"]
        g = offence_groups(sb)
        dp = [] if sb.get("hl_total_includes_death") else g.get("dp", [])
        tot_b = ssum([tb[c].value for c in dp] + [tb[f"{p}.Total"].value for p in g if p != "dp"])
        chk.eq("prisons_condemned_offence", f"{where(sb)} Totaux, all sentences vs the "
               f"nationality / age table's total ({where(sa[0])})", tot_b, tot_a)

# ----------------------------------------------------------------- c) journées de travail des détenus
EXT, MIX, INT = "Chantiers extérieurs", "Chantiers mixtes ou intérieurs", "Chantiers intérieurs"
EMP = "Chantiers extérieurs : entretien des détenus à la charge des employeurs"
ADM = "Chantiers extérieurs : entretien des détenus à la charge de l'Administration"
WORK = {  # column code -> printed heading path (the codes are per heading; several editions share a code)
    # sgt1922-sgt1923 (sgt1923 renames some)
    "ext_agriculture": f"{EXT} : Agriculture",
    "ext_agriculture_livestock": f"{EXT} : Agriculture et service de l'Élevage",
    "ext_saline": f"{EXT} : Saline",
    "ext_hopital_sadiki": f"{EXT} : Hôpital Sadiki",
    "ext_hospitals": f"{EXT} : Hôpitaux",
    "ext_controles_municipalities": f"{EXT} : Contrôles civils et Municipalités",
    "public_works": f"{MIX} : Travaux publics",
    "public_works_roads": f"{MIX} : Travaux publics : Voirie divers",
    "roads_municipality": f"{MIX} : Voirie : Municipalité",
    "roads_sweeping": f"{MIX} : Voirie : Balayages",
    "municipal_roads": f"{MIX} : Municipalités : Voirie",
    "municipal_public_gardens": f"{MIX} : Municipalités : Jardins publics",
    "agri_education": f"{MIX} : Travaux agricoles, jardinage : Enseignement public",
    "agri_agricultural_education": f"{MIX} : Travaux agricoles, jardinage : Enseignement agricoles",
    "agri_hospitals": f"{MIX} : Travaux agricoles, jardinage : Hôpitaux",
    "agri_controles": f"{MIX} : Travaux agricoles, jardinage : Contrôles civils",
    "agri_public_gardens": f"{MIX} : Travaux agricoles, jardinage : Jardins publics et d'essai",
    "agri_prisons": f"{MIX} : Travaux agricoles, jardinage : Établissements pénitentiaires",
    "agri_companies": f"{MIX} : Travaux agricoles, jardinage : Sociétés diverses",
    "agri_other": f"{MIX} : Travaux agricoles, jardinage : Divers",
    "hospitals_lazaret_asylums": f"{MIX} : Hôpitaux, Lazaret, Asiles",
    "agricultural": f"{MIX} : agricoles",
    "colleges_schools": f"{MIX} : Collèges et Écoles",
    "saline": f"{MIX} : Saline",
    "mines_phosphates": f"{MIX} : Minerais et phosphates",
    "espadrilles_alfa": f"{MIX} : Espadrilles, alfa",
    "espadrilles": f"{MIX} : Espadrilles",
    "scourtins_mats": f"{MIX} : Scourtins, Nattes",
    "controles_civils": f"{MIX} : Contrôles civils",
    "prisons": f"{MIX} : Établissements pénitentiaires",
    "other": f"{MIX} : Divers",
    # sgt1925
    "emp_agricultural": f"{EMP} : Chantiers agricoles",
    "emp_salines": f"{EMP} : Salines",
    "emp_hospitals": f"{EMP} : Hôpitaux",
    "emp_education_municipality": f"{EMP} : Enseignement, Municipalité",
    "adm_controles_fed_gaols": f"{ADM} : Contrôles civils : Détenus nourris dans les geôles",
    "adm_controles_fed_prisons": f"{ADM} : Contrôles civils : Détenus nourris dans les prisons",
    "adm_controles_gaols": f"{ADM} : Contrôles civils : Géoles",
    "adm_controles_prisons": f"{ADM} : Contrôles civils : Prisons",
    "adm_controles_detached_gaols": f"{ADM} : Contrôles civils : détenus détachés dans les geôles",
    "adm_controles_in_prisons": f"{ADM} : Contrôles civils : dans les prisons",
    "adm_municipalities": f"{ADM} : Municipalités",
    "adm_agricultural": f"{ADM} : Chantiers agricoles",
    "adm_hospitals_asylums_orphanages": f"{ADM} : Hôpitaux, asiles, orphelinats",
    "adm_education_agriculture": f"{ADM} : Enseignement, agriculture",
    "adm_public_works": f"{ADM} : Travaux publics",
    "adm_mines_phosphates": f"{ADM} : Minerais Phosphates",
    "int_espadrilles": f"{INT} : Espadrilles",
    "int_scourtins_mats_brooms": f"{INT} : Scourtins, Nattes, Balais",
    "int_other": f"{INT} : Travaux divers",
    # sgt1926-sgt1930
    "emp_municipalities": f"{EMP} : Municipalités",
    "emp_hospitals_education": f"{EMP} : Hôpitaux, Enseignement",
    "emp_agriculture_directorate": f"{EMP} : Direction générale de l'Agriculture",
    "emp_mines": f"{EMP} : Mines",
    "emp_education": f"{EMP} : Enseignement",
    "emp_beylical_works": f"{EMP} : Chantiers Beylicaux",
    "adm_municipal_gaols": f"{ADM} : Municipalités : Géoles",
    "adm_municipal_prisons": f"{ADM} : Municipalités : Prisons",
    "adm_hospitals_education_justice": f"{ADM} : Hôpitaux, Enseignement, Justice",
    "adm_agriculture_directorate": f"{ADM} : Direction générale de l'Agriculture",
    "adm_public_works_directorate": f"{ADM} : Direction générale des Travaux publics",
    "adm_hospitals_lazarets": f"{ADM} : Hôpitaux et Lazarets",
    "adm_hospitals_lazarets_asylums": f"{ADM} : Hôpitaux, Lazarets, Asiles",
    "adm_courts": f"{ADM} : Tribunaux",
    "adm_education": f"{ADM} : Enseignement",
    "adm_interior_directorate": f"{ADM} : Intérieur Direction",
    "adm_education_directorate": f"{ADM} : Direction Enseignement",
    "int_contractors_espadrilles": f"{INT} : Entrepreneurs : Espadrilles",
    "int_contractors_scourtins": f"{INT} : Entrepreneurs : Scourtins",
    "int_contractors_coffee_sorting": f"{INT} : Entrepreneurs : Triage des cafés",
    "int_state_prison_workshops": f"{INT} : État : Chantiers des Prisons",
    "int_admin_buildings_misc": f"{INT} : Administration : Bâtiments, Jardins, Cuisines, Boulangerie, Divers",
}


def base_col(sec, col):
    """base(sec), with the page / view of a column printed on the right-hand page of a spread
    (section attribute split=<first column on the right page>:<view>:<page>)."""
    b = base(sec)
    if sec.get("split"):
        first, view, page = sec["split"].split(":")
        if sec["cols"].index(col) >= sec["cols"].index(first):
            b.update(gallica_view=int(view), source_page=int(page))
    return b


def chk_work(chk, topic, sec):
    check_row(chk, topic, sec, "total", [c for c in sec["cols"] if c != "total"])
    check_col_totals(chk, topic, sec)


def cells_work(sec):
    out = []
    for r in sec["rows"]:
        if is_total(r["label"]):
            continue
        for col in sec["cols"]:
            if col == "total":
                continue
            c = r["cells"][col]
            out.append(dict(base_col(sec, col), establishment=r["label"], work=col, work_fr=WORK[col],
                            value=c.value, flag=c.flag, _row=r["label"], _col=col))
    return out

# ----------------------------------------------------------------- d) dépenses et journées de détention
EXP = {
    "days": "Nombre de journées de détention",
    "personnel": "Dépenses totales : Personnel (sgt1922 Art. 13; sgt1923 Art. 1er; sgt1924-sgt1925 Art. 9)",
    "upkeep": "Dépenses totales : entretien des détenus : entretien et dépenses diverses / dépenses diverses",
    "food": "Dépenses totales : entretien des détenus : nourriture des détenus",
    "total": "Dépenses totales : Total",
    "price_per_day": "Prix de la journée de détention",
    "products": "Produit du travail, produits divers (sgt1922: bénéfices de cantine, produit du travail, "
                "produits divers; from sgt1926: … versés au Trésor)",
    "price_personnel": "Note (1) : prix de la journée, frais de personnel",
    "price_upkeep": "Note (1) : prix de la journée, frais d'entretien",
    "price_food": "Note (1) : prix de la journée, frais de nourriture",
}
EXP_UNIT = {"days": "days", "price_per_day": "francs_per_day", "price_personnel": "francs_per_day",
            "price_upkeep": "francs_per_day", "price_food": "francs_per_day"}


def _unit(v):
    return Decimal(10) ** v.as_tuple().exponent


def chk_expenditure(chk, topic, sec):
    if sec["table"] == "expenditure_note":
        return
    block, allr = [], []
    for r in sec["rows"]:
        c = r["cells"]
        if is_total(r["label"]):
            src = allr if r["label"].endswith("*") else block
            for k in sec["cols"]:
                if k != "price_per_day":
                    chk.eq(topic, f"{where(sec)} {k}: lines vs {r['label']}", ssum(x["cells"][k].value or 0
                                                                                for x in src), c[k].value)
            block = []
        else:
            block.append(r)
            allr.append(r)
        parts = [c[k].value for k in ("personnel", "food", "upkeep")]
        if None not in parts and any(parts):
            chk.eq(topic, f"{where(sec)} {r['label']}: total = personnel + food + upkeep", ssum(parts),
                   c["total"].value)
        pr, d, t = c["price_per_day"].value, c["days"].value, c["total"].value
        if pr and d and t:
            chk.eq(topic, f"{where(sec)} {r['label']}: price per day = total / days (to the last printed "
                   f"decimal)", (t / d).quantize(_unit(pr)), pr, tol=_unit(pr))


def chk_expenditure_note(chk, topic, tables):
    for n in tables.get("expenditure_note", []):
        c = n["rows"][0]["cells"]
        chk.eq(topic, f"{where(n)} note (1): personnel + upkeep + food = price", ssum(
            c[k].value for k in ("price_personnel", "price_upkeep", "price_food")), c["price_per_day"].value)
        s = [x for x in tables["expenditure"] if x["ed"] == n["ed"]][0]
        first = []
        for r in s["rows"]:
            if is_total(r["label"]):
                break
            first.append(r["cells"])
        tot = {k: ssum(x[k].value or 0 for x in first) for k in ("days", "personnel", "upkeep", "food", "total")}
        for k in ("personnel", "upkeep", "food", "total"):
            pk = "price_per_day" if k == "total" else f"price_{k}"
            chk.eq(topic, f"{where(n)} note (1) {pk} = {k} / days, summed over the lines above the first total "
                   f"line (±0.0001)", (tot[k] / tot["days"]).quantize(Decimal("0.0001")), c[pk].value,
                   tol=Decimal("0.0001"))


def cells_expenditure(sec):
    out = []
    for r in sec["rows"]:
        if is_total(r["label"]):
            continue
        for col in sec["cols"]:
            c = r["cells"][col]
            out.append(dict(base_col(sec, col), establishment=r["label"], measure=col, measure_fr=EXP[col],
                            unit=EXP_UNIT.get(col, "francs"), value=c.value, flag=c.flag, _row=r["label"],
                            _col=col))
    return out


def base(sec):
    return {"census": sec["ed"], "table_id": sec["table"], "gallica_ark": sec["ark"], "source_page": sec["page"],
            "gallica_view": sec["view"], "year": int(sec["year"])}


T_COMMON_DOC = {
    "census": "edition the value is taken from (`sgt1922` … `sgt1939`)",
    "gallica_ark": "Gallica volume ark (views are numbered within a volume)",
    "source_page": "printed page number",
    "gallica_view": "Gallica view (fNNNN)",
    "year": "year of the figures (the edition year: each edition prints the table for its own year)",
    "value": "",
    "flag": "empty, `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable` (SPEC.md)",
}

TABLES = {
    "expenditure": dict(
        out="prisons_expenditure", check=chk_expenditure, cells=cells_expenditure,
        key=["year", "establishment", "measure"], dims=["establishment", "measure", "measure_fr", "unit"],
        doc={"table_id": "transcription section (`expenditure` = the table, `expenditure_note` = its footnote (1), "
                         "sgt1922-sgt1925)",
             "source_page": "printed page number (sgt1926-sgt1928: two-page spread; each cell has its own page)",
             "gallica_view": "Gallica view of the page the cell is printed on",
             "establishment": "line label as printed (prisons, then lines such as Chantiers extérieurs, Geôles, "
                              "En Algérie, Dans les Hôpitaux)",
             "measure": "`days`, `personnel`, `upkeep` (*entretien et dépenses diverses* / *dépenses diverses*), "
                        "`food` (*nourriture*), `total`, `price_per_day`, `products`; footnote: `price_personnel`, "
                        "`price_upkeep`, `price_food`, `price_per_day`",
             "measure_fr": "printed column heading",
             "unit": "`days`, `francs` (to the centime) or `francs_per_day`",
             "value": "number of days of detention, francs (centimes after the point) or francs per day (to the "
                      "decimals printed: 4 up to sgt1925, 3 from sgt1926)"},
        title_fr="Tableau comparatif des dépenses et des journées de détention",
        title_en="Expenditure and days of detention, by prison (cost per day of detention, products of the work)",
        unit="Units: days of detention; francs with centimes; francs per day.",
        paras=["Table d) of the chapter. Transcribed for sgt1922-sgt1928; sgt1929, sgt1930 and sgt1935 print the "
               "same table but are **not transcribed yet** (see the survey).",
               "The printed `Total` column is stored, unlike other totals, because several lines print only a "
               "total (sgt1924 En traitement dans les hôpitaux, En détention hors de Tunisie). The \"Totaux\", "
               "\"TOTAL des journées de détention\" and \"Totaux généraux (Dépenses et Recettes)\" lines are "
               "not stored; they are the checks. A total line marked `*` in the transcription sums every line "
               "above it, the others the lines since the previous total line. Cells not printed (blank price "
               "column under the lower lines) are NA with flag `not_applicable`; » = 0.",
               "Checks: every column against each total line; total = personnel + nourriture + dépenses diverses "
               "on every line that prints a component; price per day = total / days to the last printed decimal "
               "(lines and the Totaux line); footnote (1) (sgt1922-sgt1925): its three components sum to the "
               "price, and each equals the sum of its column over the lines above the first total line divided by "
               "their days (±0,0001).",
               "Footnote (1) text (sgt1922-sgt1925): \"Le prix de la journée de détention dans les prisons de la "
               "Régence est de … se décomposant ainsi : frais de personnel …, d'entretien …, de nourriture …\" "
               "(the cost of a day of detention in the prisons of the Regency, split into staff, upkeep and "
               "food); stored as establishment \"Prisons de la Régence (note 1)\".",
               "sgt1923: the price column prints \"1 4012 (1)\" on the TOTAL des journées line with \"(1) Prix "
               "moyen\" under it and 1 4012 again on the TOTAUX line; neither is stored (the footnote carries "
               "1,4012). sgt1927 Bardo total: hundreds digit broken in the printing, read as 1 (158.109,75 = the "
               "sum of its components). sgt1928 Totaux line prints » under Personnel and Produits although the "
               "lines are not »; the Totaux total 2.987.183,76 does include the personnel of the lines.",
               "Unlocated differences (failed checks without a flagged cell; printed values confirmed on crops): "
               "sgt1923 products column 0,90 short of the TOTAUX; sgt1924 days column 10 short of the Totaux; "
               "sgt1925 personnel column 0,06 over the Totaux and the Totaux line's components 0,06 under its "
               "total; price-per-day differences of 0,0003-0,0040 (sgt1924 Tunis, Gabès; sgt1925 Tunis), which "
               "look like prices computed on slightly different figures.",
               "Every cell was read on the native-resolution page images; every failing check re-read on an "
               "enlarged crop (the printed values were confirmed)."]),
    "work_days": dict(
        out="prisons_work_days", check=chk_work, cells=cells_work, key=["year", "establishment", "work"],
        dims=["establishment", "work", "work_fr"],
        doc={"table_id": "transcription section name (`work_days`); printed as table c)",
             "source_page": "printed page number (sgt1926-sgt1930: the table is a two-page spread; each cell has "
                            "the page it is printed on)",
             "gallica_view": "Gallica view (fNNNN) of the page the cell is printed on",
             "establishment": "prison (*établissement*) as printed",
             "work": "work site code, one per printed column heading (codes shared by editions whose heading is "
                     "the same); see `work_fr`",
             "work_fr": "printed column headings, from the group heading down (e.g. \"Chantiers extérieurs : "
                        "entretien des détenus à la charge des employeurs : Mines\")",
             "value": "days of work of the prisoners (*journées de travail*)"},
        title_fr="Journées de travail des détenus", title_en="Days of work of the prisoners, by prison and work site",
        unit="Unit: days of work (prisoner-days).",
        paras=["Table c) of the chapter, printed sgt1922-sgt1930 (sgt1935, sgt1936 and sgt1939 print no such "
               "table). The column headings are recast almost every edition: sgt1922-sgt1924 split *chantiers "
               "extérieurs* from *chantiers mixtes ou intérieurs*; from sgt1925 the outside work sites are split "
               "by who pays the prisoners' upkeep (*à la charge des employeurs* / *de l'Administration*) and the "
               "inside ones from sgt1926 by *Entrepreneurs* / *État* (sgt1927-sgt1930: *Administration*). Each "
               "printed column is kept with its own heading in `work_fr`; no attempt is made to harmonise them.",
               "The establishment lines also change (the Colonie des jeunes détenus line, all », sgt1922-sgt1924; "
               "La Goulette not printed sgt1927-sgt1930). Names as printed: Bardo / Le Bardo is \"Bardo\" in "
               "this table; Dj.-Djougar, Pénitencier du Djougar (sgt1926), Djebel Djougar (sgt1927-sgt1930).",
               "Not stored: the \"Total par établissement\" / \"Total général\" column and the \"Totaux\" line "
               "(the checks: each line's cells against its total, each column against the Totaux line). In "
               "sgt1922-sgt1924 the total column runs into the binding; its digits were read on enlarged crops.",
               "sgt1923 footnotes: \"Le nombre de journées des détenus employés aux scourtins du chantier mixte de "
               "La Goulette est de 2.789. Le nombre de journées des détenus employés aux minerais et phosphates du "
               "chantier mixte de La Goulette est de 12.627.\" (days of the prisoners employed on the scourtins, "
               "and on minerals and phosphates, at the mixed work site of La Goulette). These 15.416 days are not "
               "in any column but are in the printed grand total: the line totals and the column totals both sum "
               "to 407.692, the printed grand total is 423.108 = 407.692 + 2.789 + 12.627. The footnote days are "
               "not stored as cells; the grand-total check is the only failure they cause.",
               "sgt1925: the cells are printed with a vertical jitter of up to one line; each line was matched to "
               "its cells through its printed total (every line then checks, so the matching is unique).",
               "Failures involving only printed totals (no stored cell flagged; re-read on enlarged crops): "
               "sgt1925 Contrôles civils / détenus nourris dans les prisons, Totaux printed 10.070 for lines "
               "summing to 10.077 (the Totaux line's own total 412.926 needs 10.077); sgt1928 Sfax, total printed "
               "8.495 for cells summing to 8.195 (the total column's sum then gives the printed 573.680).",
               "Every cell of every edition was read on the native-resolution page images (one crop per page of "
               "the table), and each failing line or column re-read on a separate enlarged crop."]),
    "condemned_offence": dict(
        out="prisons_condemned_offence", check=chk_offence, cells=cells_offence,
        key=["year", "offence", "penalty", "nationality"],
        dims=["offence", "offence_fr", "penalty", "penalty_fr", "nationality", "nationality_fr"],
        doc={"table_id": "transcription section name (`condemned_offence`); printed as table b) up to sgt1935, "
                         "without a letter in sgt1936 and sgt1939",
             "offence": "`murder`, `assault`, `indecent_assault`, `theft`, `drunkenness`, `grazing_offence`, "
                        "`escape`, `bankrupts`, `debtors`, `bankrupts_debtors`, `political`, `other`",
             "offence_fr": "line label as printed (*nature des délits*)",
             "penalty": "`death` (*peine capitale*, printed from sgt1925), `hard_labour` (*travaux forcés*), "
                        "`reclusion`, `prison_over_1y` (*emprisonnement à 1 an et 1 jour et au-dessus*), "
                        "`prison_1y_or_less` (*emprisonnement à 1 an et au-dessous*)",
             "penalty_fr": "printed column-group heading",
             "nationality": "`french`, `european` (other Europeans), `algerian`, `tunisian` (peine capitale "
                            "\"Tunisiens\", all Tunisians), `tunisian_muslim` (\"Tunisiens\" beside an "
                            "\"Israélites\" column up to sgt1925, \"Tunisiens : Musulmans\" from sgt1926), "
                            "`tunisian_jewish`, `tripolitanian`, `other` (*divers*)",
             "nationality_fr": "printed column heading",
             "value": "number of condemned prisoners"},
        title_fr="Répartition des condamnés d'après la nationalité, la nature du délit et la catégorie pénale",
        title_en="Condemned prisoners by nationality, offence and sentence",
        unit="Unit: persons (condemned prisoners).",
        paras=["Printed once per edition, for the edition year, under the nationality / age table (b) up to "
               "sgt1935). The nationality columns differ by sentence and by edition: each sentence group has "
               "its own set (e.g. Tripolitains only under emprisonnement ≤ 1 an in sgt1922-sgt1924; no Israélites "
               "under réclusion in sgt1922-sgt1923's Divers-less set; Divers instead of Israélites under réclusion "
               "in sgt1936 and sgt1939). A column not printed has no rows. Column order changes in sgt1927 "
               "(Français, Algériens, Européens, …) but the headings are the same. The offence lines change too "
               "(Évasions only sgt1922; Faillis and Dettiers separate sgt1923-sgt1924, merged sgt1925-sgt1930, "
               "Faillis alone and a new Politiques line from sgt1935).",
               "Not stored: each group's \"Total\" column, the \"Total général\" column (sgt1935 only) and the "
               "\"Totaux\" line; they are the checks. Checks: each group's Total = sum of its nationality "
               "columns, on every line; Total général = peine capitale + the four group totals (sgt1935); every "
               "column against the Totaux line; and, per edition, the grand total of the table (death sentences "
               "included) against the \"Totaux / Total par nationalité\" of the nationality / age table.",
               "sgt1928: the travaux forcés \"Total\" column is printed half a line to a line low from Attentat à "
               "la pudeur down (3 between Attentat and Vol, 4 on the Ivresse line, 1 under Divers); it is "
               "transcribed on the lines whose cells it sums (it is a check column, not stored).",
               "sgt1924: travaux forcés, Attentat à la pudeur prints 36 under Algériens and nothing under Tunisiens; "
               "the Algériens and Tunisiens column totals (37 and 424) agree with the cells as printed, so the "
               "printed placement is kept (it may be a column slip in the original).",
               "sgt1925 and sgt1926: the travaux forcés \"Total\" includes the death sentences printed in the "
               "peine capitale columns just left of it (sgt1925: Meurtre 52 + 4 = 56, Totaux 122 + 4 = 126, and "
               "the table's grand total is then exactly the nationality table's 9.254; sgt1926: Meurtre 49 + 1 = "
               "50, Totaux 111 + 1 = 112); the checks are made that way for these two editions "
               "(`hl_total_includes_death=1` in the transcription). sgt1926's grand total is then 9.148 against "
               "the nationality table's 9.149, an unlocated difference of 1.",
               "Failures involving only printed totals (no stored cell flagged; cells re-read on crops): sgt1929 "
               "emprisonnement ≤ 1 an, Totaux Français printed 26 for lines summing to 27 (the Totaux line's "
               "Total 7.273 needs 27); sgt1935 emprisonnement ≤ 1 an, Attentat à la pudeur Total printed 205 for "
               "1 + 205 = 206 (Total général 235 and the column total 9.480 both need 206); sgt1936 emprisonnement "
               "> 1 an, Totaux Musulmans printed 330 for lines summing to 320 (the Totaux line's Total 341 needs "
               "320).",
               "Every cell of every edition was read on the native-resolution page image (two crops per table), "
               "and each failing line or column re-read on a separate enlarged crop."]),
    "condemned_age": dict(
        out="prisons_condemned_nationality_age", check=chk_condemned, cells=cells_condemned,
        key=["year", "nationality", "category"],
        dims=["nationality", "nationality_fr", "breakdown", "category", "category_fr"],
        doc={"table_id": "transcription section name (`condemned_age`); printed as table a) up to sgt1935, "
                         "without a letter in sgt1936 and sgt1939",
             "nationality": "`french`, `algerian`, `italian`, `maltese`, `greek`, `spanish`, `serbian`, `danish`, "
                            "`other_european`, `tunisian_muslim`, `tunisian_jewish`, `tripolitanian`, `moroccan`, "
                            "`other`",
             "nationality_fr": "line label as printed",
             "breakdown": "`age`, `sex` or `penal_category`: the table splits the same prisoners three ways, so "
                          "each breakdown sums to the prisoners of the nationality",
             "category": "`age_0_10` … `age_51_plus`, `male`, `female`, `first_offender` (*primaires*), "
                         "`recidivist` (*récidivistes*)",
             "category_fr": "printed column heading",
             "value": "number of condemned prisoners"},
        title_fr="Répartition des condamnés d'après la nationalité, l'âge, le sexe et la catégorie pénale",
        title_en="Condemned prisoners by nationality, age, sex and penal category",
        unit="Unit: persons (condemned prisoners; the printed tables do not say at which date they are counted).",
        paras=["Printed once per edition, for the edition year: a) on the first page of the chapter (sgt1922-sgt1935); "
               "first table of the prisons pages inside chapter IV *Justice* in sgt1936 and sgt1939. The printed "
               "\"Total par nationalité\" column, the age \"Total\" column (printed sgt1922-sgt1926 only) and the "
               "\"Totaux\" line are not stored; they are the checks.",
               "Nationality lines change between editions: sgt1922-sgt1924 print \"— (Algériens)\" (under "
               "Français), \"Anglais (Maltais)\", Serbes (sgt1922) or Danois (sgt1923-sgt1924), and the Tunisian "
               "subjects under a brace labelled \"sujet musulmans\" (as printed: Musulmans / Israélites); "
               "sgt1925 prints Anglo-Maltais and has no Grecs, Espagnols or Autres européens lines; from sgt1926 "
               "the lines are fixed (Tunisiens musulmans / israélites). A nationality not printed in an edition "
               "has no rows for it.",
               "Checks on every line, Totaux included: sum of the seven age groups = total; age \"Total\" column = "
               "sum of the age groups (sgt1922-sgt1926); male + female = total; primaires + récidivistes = total; "
               "and every column against the Totaux line.",
               "Failures that involve only printed totals (no stored cell flagged): sgt1928 Tripolitains, "
               "\"Total par nationalité\" printed 192 where the ages, the sexes and the penal categories all give "
               "198 and the Totaux line (8.282) needs 198; sgt1930 Totaux, \"51 ans et au-dessus\" printed 397 for "
               "lines summing to 387, while the Totaux line's own total 7.828 agrees with 387 (the lines' sums of "
               "ages all match their totals); sgt1922 Totaux, ages summing to 8.224 for 8.227, which is the "
               "Italiens shortfall of 3 carried into the total line.",
               "Every cell of every edition was read on the native-resolution page image (crops of the whole "
               "table), and each failing line re-read on a separate crop."]),
}


def build_tables(tables, write):
    res = {}
    by_out = defaultdict(list)
    for name, spec in TABLES.items():
        by_out[spec["out"]].append(name)
    for out, names in by_out.items():
        chk = Checks()
        secs, recs = [], []
        for name in names:
            spec = TABLES[name]
            extra = tables.get("expenditure_note", []) if name == "expenditure" else []
            for s in tables.get(name, []) + extra:
                spec["check"](chk, out, s)
                secs.append(s)
                recs += spec["cells"](s)
        if not secs:
            continue
        if out == "prisons_condemned_offence":
            cross_offence_age(chk, tables)
        if out == "prisons_expenditure":
            chk_expenditure_note(chk, out, tables)
        spec = TABLES[names[0]]
        for r in recs:
            k = (r["census"], r["table_id"], r["_row"], r["_col"])
            if k in MISMATCH and not r["flag"]:
                r["flag"] = "total_mismatch"
            if k in REALIGNED and not r["flag"]:
                r["flag"] = "row_realigned"
        kept, compared, diffs = select_latest(recs, spec["key"])
        order = {id(r): i for i, r in enumerate(recs)}
        kept.sort(key=lambda r: (ORDER.index(r["census"]), order.get(id(r), 0)))
        fails = chk.fail[out]
        res[out] = dict(rows=len(kept), checks=chk.n[out], failed=fails, overlap_compared=compared,
                        overlap_diffs=[list(d) for d in diffs])
        if write:
            cols = COMMON + spec["dims"] + ["value", "flag"]
            doc = dict(T_COMMON_DOC, **spec["doc"])
            write_csv(out, cols, kept)
            mm = defaultdict(list)
            for (e, t, row, col), why in MISMATCH.items():
                if t in names:
                    mm[(e, why)].append(f"{row} / {col}")
            paras = list(spec["paras"])
            if mm:
                paras.append("Cells flagged `total_mismatch` (printed value kept, re-read on a native-resolution "
                             "crop): " + "; ".join(f"{e}: {', '.join(c)} ({why})" for (e, why), c in mm.items())
                             + ".")
            ra = [f"{e} {row} / {col}: {why}" for (e, t, row, col), why in REALIGNED.items() if t in names]
            if ra:
                paras.append("Cells flagged `row_realigned` (stored on the line their content belongs to): "
                             + "; ".join(ra) + ".")
            write_notes(out, CHAPTER, SCRIPT, kept, cols, doc, spec["title_fr"], spec["title_en"], paras,
                        chk.n[out], fails, compared, diffs, coverage_lines(secs),
                        "Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is "
                        "kept, with `year`; no year is printed by two editions.", spec["unit"])
    return res


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    kept, compared, diffs, fails, others = build(write=(mode == "build"))
    print(f"prisons_population_recap: {len(kept)} rows, {CHK.n['recap']} checks, {len(fails)} failed, "
          f"{compared} compared, {len(diffs)} diffs")
    for f in fails:
        print("   FAIL", f)
    for d in diffs:
        print("   DIFF", d)
    for name, d in others.items():
        print(f"{name}: {d['rows']} rows, {d['checks']} checks, {len(d['failed'])} failed, "
              f"{d['overlap_compared']} compared, {len(d['overlap_diffs'])} diffs")
        for f in d["failed"]:
            print("   FAIL", f)
        for x in d["overlap_diffs"]:
            print("   DIFF", x)


if __name__ == "__main__":
    main()
