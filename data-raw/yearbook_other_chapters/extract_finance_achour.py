#!/usr/bin/env python3
"""Achour (tithe on cereals): areas sown, from the Finances chapter of the Statistique générale de la Tunisie,
editions sgt1922-sgt1930 and sgt1935.

  python3 extract_finance_achour.py check   parse the transcriptions, run every check, print failures
  python3 extract_finance_achour.py build   ... and write csv/finance_achour.csv, its .md notes,
                                            csv/finance_achour_survey.md and csv/finance_achour_validation.json

Source of truth: transcribed/finance_achour_<edition>.txt (format in yb_tables.py). Three layouts:

  achour       sgt1922-sgt1925: per crop a) européens, b) indigènes, c) récapitulation, by caïdat (sgt1925: by
               région, contrôle civil and caïdat, on a two-page spread) x yield class (6 hectolitres and over ..
               under 1 hectolitre), TOTAL, and the area of new land exempted from the achour.
               cols y6 y5 y4 y3 y2 y1 y0 tot new (a spread: one section per view, rows matched by label).
  achour_roll  sgt1926-sgt1930: one page per crop, by région, contrôle civil and caïdat: areas sown by the
               européens, the indigènes, Récapitulation, and the exempted new land (both rolls together).
               cols eur ind rec new.
  achour_nat   sgt1935: one page, all crops, the Tunisia totals only (cols eur ind rec new).

Stored: the européens and indigènes cells (and the exempted new land); TOTAL, Récapitulation tables and columns and
the Totaux lines are checks.
"""
import sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # shared helper yb_tables.py
from yb_tables import (COMMON, EDITIONS, ORDER, OUT, TR, Checks, coverage_lines, is_total, parse, ssum,
                       write_csv, write_notes, write_validation)

CHAPTER = "Finances"
SCRIPT = "extract_finance_achour.py"
NAME = "finance_achour"
EDS = ["sgt1922", "sgt1923", "sgt1924", "sgt1925", "sgt1926", "sgt1927", "sgt1928", "sgt1929", "sgt1930",
       "sgt1935"]

CROPS = {  # code: (printed name in the sgt1922-sgt1925 titles, letter and name in sgt1926-sgt1930, sgt1935 row)
    "wheat": ("Blé", "a) Blé", "Blé"), "barley": ("Orge", "b) Orge", "Orge"),
    "oats": ("Avoine", "c) Avoine", "Avoine"), "broad_beans": ("Fèves", "d) Fèves", "Fèves"),
    "chickpeas": ("Pois chiches", "e) Pois chiches", "Pois chiches"), "maize": ("Maïs", "f) Maïs", "Maïs"),
    "sorghum": ("Sorgho", "g) Sorgho", "Sorgho"), "flax": ("Lin", "h) Lin", "Lin"),
}
YIELD = {"y6": ("6_plus", "6 hectol. et au-dessus"), "y5": ("5", "5 hectol."), "y4": ("4", "4 hectol."),
         "y3": ("3", "3 hectol."), "y2": ("2", "2 hectol."), "y1": ("1", "1 hectol."),
         "y0": ("under_1", "moins d'un hectolitre")}
YCOLS = list(YIELD)
ROLL = {"a": ("european", "a) Superficies ensemencées par des européens"),
        "b": ("indigenous", "b) Superficies ensemencées par des indigènes"),
        "c": ("recap", "c) Récapitulation")}
ROLLCOL = {"eur": ("european", "par les européens"), "ind": ("indigenous", "par les indigènes")}
M_SOWN = ("area_sown", "Nombre d'hectares d'un rendement de :")
M_SOWN2 = ("area_sown", "Nombre d'hectares ensemencés")
M_NEW = ("area_new_land_exempt", "Cultures effectuées sur terrains nouvellement défrichés et exemptées de l'achour")

CHK = Checks()
O = NAME

# Cells identified as faulty by the checks (printed value kept, flag total_mismatch): (edition, view, label, col)
FLAGS = {
    ("sgt1926", 776, "4e Région (Sousse) ; Sfax ; La Skhira", "eur"): "total_mismatch",
    ("sgt1926", 783, "2e Région (Tunis) ; Grombalia ; Cap-Bon", "ind"): "total_mismatch",
    ("sgt1928", 762, "5e Région (Sfax) ; Gafsa ; Gafsa", "ind"): "row_realigned",
    ("sgt1928", 762, "5e Région (Sfax) ; Tozeur ; Djerid", "ind"): "row_realigned",
    ("sgt1929", 242, "4e Région (Sousse) ; Kairouan ; Kairouan", "ind"): "total_mismatch",
    ("sgt1929", 244, "1re Région (Bizerte) ; Bizerte ; Mateur", "ind"): "total_mismatch",
    ("sgt1930", 777, "1re Région (Bizerte) ; Tabarka ; Aïn-Draham", "ind"): "total_mismatch",
    ("sgt1922", 188, "Banlieue", "y6"): "total_mismatch",
    ("sgt1922", 188, "Banlieue", "y3"): "total_mismatch",
    ("sgt1922", 188, "Souk-el-Arba", "y2"): "total_mismatch",
    ("sgt1922", 189, "Ouled-Ayar", "y4"): "total_mismatch",
    ("sgt1922", 194, "Zaghouan", "y0"): "total_mismatch",
    ("sgt1922", 195, "Tadjerouine", "y0"): "total_mismatch",
    ("sgt1922", 201, "Mateur", "y4"): "total_mismatch",
    ("sgt1922", 210, "Ouled-Aoun", "y6"): "total_mismatch",
    ("sgt1922", 210, "Ouled-Aoun", "y1"): "row_realigned",
    ("sgt1925", 263, "4me Région (Sousse) ; Sousse ; Sousse", "y0"): "total_mismatch",
    ("sgt1925", 233, "4me Région (Sousse) ; Thala ; Fraichiches", "new"): "total_mismatch",
    ("sgt1925", 238, "2me Région (Tunis) ; Grombalia ; Cap-Bon, Soliman", "y6"): "derived_from_totals",
    ("sgt1925", 239, "2me Région (Tunis) ; Grombalia ; Cap-Bon, Soliman", "y2"): "total_mismatch",
    ("sgt1925", 238, "3me Région (Le Kef) ; Medjez-el-Bab ; Medjez-el-Bab", "y6"): "total_mismatch",
    ("sgt1925", 240, "1re Région (Bizerte) ; Béja ; Béja", "y6"): "total_mismatch",
    ("sgt1925", 241, "5me Région (Sfax) ; Gafsa ; Hemmama", "y2"): "total_mismatch",
    ("sgt1925", 233, "1re Région (Bizerte) ; Bizerte ; Bizerte", "y0"): "total_mismatch",
    ("sgt1925", 234, "4me Région (Sousse) ; Kairouan ; Djelass", "y6"): "total_mismatch",
    ("sgt1925", 235, "1re Région (Bizerte) ; Souk-el-Arba ; Souk-el-Arba", "y3"): "total_mismatch",
    ("sgt1925", 226, "2me Région (Tunis) ; Grombalia ; Cap-Bon, Nabeul", "y6"): "total_mismatch",
    ("sgt1925", 227, "5me Région (Sfax) ; Gafsa ; Hemmama", "new"): "total_mismatch",
    ("sgt1925", 228, "4me Région (Sousse) ; Sousse ; Souassi", "y6"): "total_mismatch",
    ("sgt1925", 229, "1re Région (Bizerte) ; Souk-el-Arba ; Souk-el-Arba", "y4"): "total_mismatch",
    ("sgt1925", 229, "3me Région (Le Kef) ; Téboursouk ; Téboursouk", "y2"): "total_mismatch",
    ("sgt1923", 679, "Djelass", "y0"): "total_mismatch",
    ("sgt1923", 687, "Mahdia", "y6"): "total_mismatch",
    ("sgt1924", 1184, "Béja", "y6"): "total_mismatch",
    ("sgt1925", 221, "1re Région (Bizerte) ; Souk-el-Arba ; Souk-el-Arba", "y4"): "total_mismatch",
    ("sgt1925", 221, "4me Région (Sousse) ; Sfax ; Djebéniana", "new"): "total_mismatch",
    ("sgt1925", 223, "1re Région (Bizerte) ; Tabarka ; Aïn-Draham", "y1"): "total_mismatch",
    ("sgt1925", 223, "1re Région (Bizerte) ; Tabarka ; Aïn-Draham", "y0"): "total_mismatch",
    ("sgt1925", 223, "2me Région (Tunis) ; Grombalia ; Cap-Bon, Soliman", "y5"): "total_mismatch",
    ("sgt1925", 222, "2me Région (Tunis) ; Grombalia ; Cap-Bon, Soliman", "y6"): "derived_from_totals",
    ("sgt1925", 222, "4me Région (Sousse) ; Thala ; Fraichiches", "y6"): "total_mismatch",
}
# Cells hidden in the binding, solved from the printed totals: filled by derive()
DERIVED = set()


def geo(label):
    parts = [x.strip() for x in label.split(" ; ")]
    if len(parts) == 1:
        return {"region": "", "controle_civil": "", "caidat": parts[0]}
    return {"region": parts[0], "controle_civil": parts[1], "caidat": parts[2]}


def base(sec):
    return {"census": sec["ed"], "table_id": sec["table"] + ("_" + sec["letter"] if sec.get("letter") else ""),
            "gallica_ark": sec["ark"], "source_page": sec["page"], "gallica_view": sec["view"],
            "year": int(sec.get("year") or sec["ed"][3:])}


def rec(sec, label, col, cell, **dims):
    r = dict(base(sec), **dims, unit="hectares", value=cell.value, flag=cell.flag)
    f = FLAGS.get((sec["ed"], sec["view"], label, col))
    if f:
        r["flag"] = f
    return r


def v0(cell):
    """Value for the checks: a blank cell ('-', nothing printed) counts as 0."""
    return Decimal(0) if cell.flag == "not_applicable" else cell.value


def data_rows(sec):
    return [r for r in sec["rows"] if "cells" in r and not is_total(r["label"])]


# ----------------------------------------------------------------- cells

def cells(sec):
    out = []
    t = sec["table"]
    if t == "achour":
        roll, roll_fr = ROLL[sec["letter"]]
        if roll == "recap":
            return out
        crop = sec["crop"]
        for r in data_rows(sec):
            g = geo(r["label"])
            for c, cell in r["cells"].items():
                if c in YIELD:
                    y, yfr = YIELD[c]
                    out.append(rec(sec, r["label"], c, cell, **g, crop=crop, crop_fr=CROPS[crop][0], roll=roll,
                                   roll_fr=roll_fr, yield_class=y, yield_class_fr=yfr, measure=M_SOWN[0],
                                   measure_fr=M_SOWN[1]))
                elif c == "new":
                    out.append(rec(sec, r["label"], c, cell, **g, crop=crop, crop_fr=CROPS[crop][0], roll=roll,
                                   roll_fr=roll_fr, yield_class="", yield_class_fr="", measure=M_NEW[0],
                                   measure_fr=M_NEW[1]))
    elif t in ("achour_roll", "achour_nat"):
        for r in data_rows(sec):
            if t == "achour_roll":
                g, crop = geo(r["label"]), sec["crop"]
                crop_fr = CROPS[crop][1]
                rfr = dict(ROLLCOL)
            else:
                g, crop = {"region": "", "controle_civil": "", "caidat": "TOTAL (printed)"}, r["label"]
                crop_fr = CROPS[crop][2]
                rfr = dict(ROLLCOL, ind=("indigenous", "par les tunisiens"))
            for c in ("eur", "ind"):
                out.append(rec(sec, r["label"], c, r["cells"][c], **g, crop=crop, crop_fr=crop_fr, roll=rfr[c][0],
                               roll_fr=rfr[c][1], yield_class="", yield_class_fr="", measure=M_SOWN2[0],
                               measure_fr=M_SOWN2[1]))
            out.append(rec(sec, r["label"], "new", r["cells"]["new"], **g, crop=crop, crop_fr=crop_fr, roll="all",
                           roll_fr="Européens et Indigènes" if t == "achour_roll" else "européens et tunisiens",
                           yield_class="", yield_class_fr="", measure=M_NEW[0], measure_fr=M_NEW[1]))
    return out


# ----------------------------------------------------------------- merging spreads and checks

def merged(secs):
    """achour sections of one printed table (edition, crop, roll letter), the views of a spread joined:
    {label: {col: Cell}} in printed order, and the list of sections."""
    groups = defaultdict(list)
    for s in secs:
        if s["table"] == "achour":
            groups[(s["ed"], s["crop"], s["letter"])].append(s)
    out = {}
    for k, ss in groups.items():
        rows = {}
        for s in ss:
            for r in s["rows"]:
                if "cells" in r:
                    rows.setdefault(r["label"], {}).update(r["cells"])
        out[k] = (rows, ss)
    return out


# Caïdat printed under another name in one of the a) b) c) tables of a crop: (edition, printed label) -> the label
# of the other tables, for the c) = a) + b) check only (labels are stored as printed)
ALIAS = {("sgt1922", "Banlieue (Tunis)"): "Banlieue", ("sgt1923", "Banlieue (Tunis)"): "Banlieue",
         ("sgt1924", "Banlieue (Tunis)"): "Banlieue"}


def key(ed, label):
    return "TOTAUX" if is_total(label) else ALIAS.get((ed, label), label)


def tag(ed, crop, letter, ss):
    return f"{ed} f{'|f'.join(str(s['view']) for s in ss)} {crop} {letter})"


def derive(secs):
    """A cell left '?' (hidden in the binding) = TOTAL - the other yield classes of its line (flag
    derived_from_totals). Runs before the checks; derived cells then enter the column and récapitulation checks."""
    for (ed, crop, letter), (rows, ss) in merged(secs).items():
        for lab, d in rows.items():
            miss = [c for c in YCOLS if c in d and d[c].value is None and d[c].flag == "illegible"]
            if len(miss) == 1 and d.get("tot") is not None and d["tot"].value is not None:
                cell = d[miss[0]]
                cell.value = d["tot"].value - ssum(d[c].value for c in YCOLS if c != miss[0])
                cell.flag = "derived_from_totals"
                DERIVED.add(id(cell))
    for s in secs:  # achour_roll / achour_nat: européens or indigènes = Récapitulation - the other roll
        if s["table"] in ("achour_roll", "achour_nat"):
            for r in s["rows"]:
                c = r.get("cells", {})
                miss = [k for k in ("eur", "ind") if k in c and c[k].flag == "illegible"]
                if len(miss) == 1 and c["rec"].value is not None:
                    other = "ind" if miss[0] == "eur" else "eur"
                    c[miss[0]].value = c["rec"].value - c[other].value
                    c[miss[0]].flag = "derived_from_totals"
                    DERIVED.add(id(c[miss[0]]))


def checks(secs):
    m = merged(secs)
    for (ed, crop, letter), (rows, ss) in m.items():
        w = tag(ed, crop, letter, ss)
        cols = [c for c in YCOLS + ["tot", "new"] if any(c in d for d in rows.values())]
        for lab, d in rows.items():
            if any(id(d[c]) in DERIVED for c in YCOLS if c in d):
                continue
            if "tot" in d and all(c in d for c in YCOLS):
                CHK.eq(O, f"{w} {lab}: TOTAL = sum of the yield classes", ssum(d[c].value for c in YCOLS),
                       d["tot"].value)
        data = {l: d for l, d in rows.items() if not is_total(l)}
        for t in [l for l in rows if is_total(l)]:
            for c in cols:
                CHK.eq(O, f"{w} {c}: Totaux = sum of the lines", ssum(v0(d[c]) for d in data.values()),
                       rows[t][c].value)
        if letter == "c":
            a, b = m.get((ed, crop, "a")), m.get((ed, crop, "b"))
            if not a or not b:
                continue
            ka = {key(ed, l): l for l in a[0]}
            kb = {key(ed, l): l for l in b[0]}
            for lab, d in rows.items():
                k = key(ed, lab)
                la, lb = ka.get(k), kb.get(k)
                if la is None and lb is None:
                    CHK.fail[O].append(f"{w} {lab}: no matching line in a) or b)")
                    continue
                for c in cols:
                    # a line not printed in a) or b) (e.g. sgt1922 blé: Djerid, indigènes only) counts as 0
                    va = v0(a[0][la][c]) if la is not None and c in a[0][la] else (None if la else Decimal(0))
                    vb = v0(b[0][lb][c]) if lb is not None and c in b[0][lb] else (None if lb else Decimal(0))
                    if va is None or vb is None:
                        CHK.fail[O].append(f"{w} {lab} {c}: no matching cell in a) or b)")
                        continue
                    CHK.eq(O, f"{w} {lab} {c}: Récapitulation = européens + indigènes", ssum([va, vb]), d[c].value)
    for s in secs:
        if s["table"] not in ("achour_roll", "achour_nat"):
            continue
        w = f"{s['ed']} f{s['view']} {s.get('crop', '')}"
        rows = [r for r in s["rows"] if "cells" in r]
        for r in rows:
            c = r["cells"]
            if id(c["eur"]) in DERIVED or id(c["ind"]) in DERIVED:
                continue
            CHK.eq(O, f"{w} {r['label']}: Récapitulation = européens + indigènes", ssum([c["eur"].value,
                                                                                          c["ind"].value]),
                   c["rec"].value)
        data = [r for r in rows if not is_total(r["label"])]
        for t in [r for r in rows if is_total(r["label"])]:
            for k in s["cols"]:
                CHK.eq(O, f"{w} {k}: Totaux = sum of the lines", ssum(v0(x["cells"][k]) for x in data),
                       t["cells"][k].value)


# ----------------------------------------------------------------- notes

DIMS = ["region", "controle_civil", "caidat", "crop", "crop_fr", "roll", "roll_fr", "yield_class", "yield_class_fr",
        "measure", "measure_fr", "unit"]
DOC = {
    "census": "source edition (`sgt1922` ... `sgt1935`)",
    "table_id": "printed layout: `achour_roll` (sgt1926-sgt1930, one page per crop, européens and indigènes "
                "columns), `achour_nat` (sgt1935, Tunisia totals), or (sgt1922-sgt1925, yield-class tables) `achour_a` "
                "(a) européens) and `achour_b` (b) indigènes)",
    "gallica_ark": "Gallica ark of the volume",
    "source_page": "printed page number (for a two-page spread, the page the cell is printed on)",
    "gallica_view": "Gallica view",
    "year": "year of the roll: the edition year (sgt1922-sgt1930 print no year; sgt1935 prints \"ACHOUR (1935)\")",
    "region": "région as printed, with its chef-lieu in brackets (sgt1925: \"1re Région (Bizerte)\" ... \"5me "
              "Région (Sfax)\", the chef-lieu printed in its own column; sgt1926-sgt1930: \"1re Région (Bizerte)\"); "
              "\"Territoires Militaires du Sud\"; empty when the table lists caïdats only (sgt1922-sgt1924)",
    "controle_civil": "contrôle civil as printed (sgt1925-sgt1930); empty otherwise",
    "caidat": "caïdat as printed (sgt1925: the caïdat of Cap-Bon, printed in two lines, as \"Cap-Bon, Nabeul\" and "
              "\"Cap-Bon, Soliman\"); `TOTAL (printed)` for the sgt1935 table, which prints only the totals for Tunisia",
    "crop": "`wheat` (blé), `barley` (orge), `oats` (avoine), `broad_beans` (fèves), `chickpeas` (pois chiches), "
            "`maize` (maïs), `sorghum` (sorgho), `flax` (lin)",
    "crop_fr": "crop as printed",
    "roll": "`european`, `indigenous` (sgt1935: \"par les tunisiens\"), or `all` for the exempted new land of "
            "sgt1926-sgt1935, printed for both together",
    "roll_fr": "printed table title or column head",
    "yield_class": "yield class of the area, in hectolitres (sgt1922-sgt1925 only): `6_plus` (6 hectolitres and "
                   "over), `5`, `4`, `3`, `2`, `1`, `under_1` (less than one hectolitre); empty for the exempted new "
                   "land and where no yield class is printed",
    "yield_class_fr": "printed column head (under \"Nombre d'hectares d'un rendement de :\")",
    "measure": "`area_sown` (hectares sown, liable to the achour) or `area_new_land_exempt` (cultures effectuées sur "
               "terrains nouvellement défrichés et exemptées de l'achour)",
    "measure_fr": "printed column head",
    "unit": "`hectares`",
    "value": "area in hectares (printed in hectares and ares, \"h. a.\": \"7.912 09\" = 7912.09 ha); printed » = 0",
    "flag": "empty, or `derived_from_totals` (figure broken or not printed, solved as Récapitulation minus the "
            "other roll, or, sgt1922-sgt1925, as the line's TOTAL minus its other yield classes), `total_mismatch` "
            "(printed value kept; the line's Récapitulation and the column Totaux (sgt1922-sgt1925: also the "
            "line's TOTAL) require another value), `row_realigned` (printed one line too high or too low, "
            "stored on its own line), "
            "`not_applicable` (nothing printed in the cell, NA)",
}
TITLE_FR = "Achour. Superficies ensemencées par les européens et par les indigènes"
TITLE_EN = "Achour (tithe on cereals): areas sown by caïdat, crop, roll (Europeans / indigenous) and yield class"
UNIT = ("Unit: hectares (printed \"h. a.\", hectares and ares, the ares as two figures after a space; stored as "
        "decimal hectares, ares / 100: no other conversion). value_type: hectares.")
RULE = ("Each edition prints the rolls of its own year (no overlapping printings): every edition is stored. No "
        "year is printed in sgt1922-sgt1930; `year` is the edition year.")
PARAS = [
    "Printed layouts. sgt1922-sgt1925: for each of the eight crops three tables, a) Superficies ensemencées par "
    "des européens, b) par des indigènes, c) Récapitulation, by caïdat (sgt1922-sgt1924, one page each) or by "
    "région, chef-lieu de région, contrôle civil and caïdat (sgt1925, two-page spreads), with the columns "
    "Nombre d'hectares d'un rendement de : 6 hectol. et au-dessus, 5, 4, 3, 2, 1 hectol., moins d'un hectolitre, "
    "TOTAL, and Cultures effectuées sur terrains nouvellement défrichés et exemptées de l'achour. Stored: the "
    "yield classes and the exempted new land of tables a) and b); TOTAL (= the seven yield classes; the exempted "
    "land is outside it, e.g. sgt1922 blé européens L'Arad: TOTAL 6.50, new land 21.50), the c) tables and the "
    "Totaux lines are checks. sgt1926-sgt1930: one page per crop (a) Blé ... h) Lin), by région (chef-lieu in "
    "brackets), contrôle civil and caïdat, with the Nombre d'hectares ensemencés par les européens, par les "
    "indigènes, Récapitulation, and the exempted new land for Européens et Indigènes together (roll `all`); no "
    "yield classes. sgt1935: one page, \"ACHOUR (1935)\", the same four columns (\"par les tunisiens\") for the "
    "eight crops, Tunisia totals only (caïdat `TOTAL (printed)`).",
    "Footnote (sgt1935), translated: (1) The figures of this column [exempted new land] are included in those of "
    "the preceding column, Récapitulation.",
    "Rows of each caïdat as printed. Blank cells (nothing printed, e.g. sgt1927 maïs Soliman, new land) are "
    "stored as NA with flag `not_applicable` and count as 0 in the column checks (the printed Totaux agree). "
    "Several small figures are printed in the ares place only, with no hectares figure (e.g. sgt1928 sorgho, "
    "Nabeul européens \"45\"): read as ares (0.45 ha); every such reading agrees with the printed Totaux.",
    "sgt1928 blé (f762): in the indigènes column of the 5e Région the figures 8.067 96 and 296 49 are printed one "
    "line too high (on the Hemmama and Gafsa lines; » on the Djerid line) and no figure is printed for Hemmama; "
    "the Récapitulation of each line places them (Gafsa 8.073 21 = 5 25 + 8.067 96, Djerid 296 53 = 0 04 + 296 49): "
    "stored on Gafsa and Djerid (flag `row_realigned`), Hemmama derived as 13.261 85 - 233 71 = 13.028 14 (flag "
    "`derived_from_totals`). sgt1926 fèves (f779): Sousse européens printed \"104 8\" with the last figure broken, "
    "derived as 993 48 - 888 67 = 104 81.",
    "sgt1922-sgt1925 (yield-class tables): caïdats as printed in each table; where a table prints a caïdat under "
    "another name (sgt1922-sgt1924: \"Banlieue (Tunis)\" in some tables, \"Banlieue\" "
    "elsewhere; stored as printed) the c) = a) + b) check matches the lines (ALIAS in the script), and a line printed in one roll only (sgt1922 blé: Djerid, "
    "not printed in a)) counts as 0 in the other. A few » are printed inverted (\"«\"; e.g. sgt1922 fèves a) "
    "Tadjerouine 1 hectol., sgt1923 orge c) Gafsa new land): read as 0, as the totals confirm. No year is printed: "
    "`year` is the edition year.",
    "`ocr_corrected` is not used: every cell was read from the native-resolution image (the Gallica OCR of these "
    "pages is poor and served only as a typing aid and cross-check); the agreement of the European, indigenous "
    "and récapitulation figures and of the column Totaux was checked for every line and column.",
]
FAILS = (
    "Failed checks, each re-read on zoomed native-resolution crops (printed values kept). Cells identified as "
    "faulty (flag `total_mismatch`; the Récapitulation of the line and the column Totaux both require another "
    "value): sgt1926 blé, La Skhira européens printed 44.95 (both require 411.95); sgt1926 lin, Cap-Bon indigènes "
    "129.92 (129.97); sgt1929 avoine, Kairouan indigènes 375.70 (373.70); sgt1929 pois chiches, Mateur indigènes "
    "567.84 (569.84); sgt1930 fèves, Aïn-Draham indigènes 228.54 (228.64). Misprinted check figures (no stored cell "
    "involved; the European and indigenous columns agree with their Totaux, or the other checks place the error "
    "in the check figure): sgt1926 pois chiches, Récapitulation of Mateur printed 1.166 31 for 1.166 35; sgt1928 "
    "blé, Récapitulation of Ouerghemma printed 8.339 96 for 8.939 96, and the Totaux of the Récapitulation "
    "797.816 » for 797.816 11; sgt1928 pois chiches, Récapitulation of the Caïdat de la banlieue 153.70 for 155.70; "
    "sgt1929 maïs, Totaux of the européens printed 659 41 for 569 41 (the Totaux Récapitulation 17.268 02 = 569 41 + "
    "16.698 61); sgt1929 sorgho, Récapitulation of Téboursouk 3 75 for 3 73 (the Totaux Récapitulation agrees with "
    "3 73); sgt1930 avoine, Totaux of the indigènes printed 35.713 52 for 25.713 52 (the Totaux Récapitulation "
    "49.240 72 = 23.527 20 + 25.713 52). Unresolved: sgt1929 orge, exempted new land, the lines sum to 4.509 01 "
    "against the printed Totaux 4.514 01 (every line re-read; no line can be identified, no Récapitulation "
    "exists for this column; values kept unflagged).")
FAILS_YIELD = {  # sgt1922-sgt1925, yield-class tables: every failed check re-read on a zoomed native-resolution crop
    "sgt1922": (
        "sgt1922. Faulty cells (flag `total_mismatch`; the line's TOTAL, the column Totaux and the c) "
        "Récapitulation all require another value): blé a) Banlieue 6 hectol. printed 7.912 09 (7.942 09) and 3 "
        "hectol. 2.041 36 (2.041 34), Souk-el-Arba 2 hectol. 74 75 (74 55); blé b) Ouled-Ayar 4 hectol. 2.348 41 "
        "(2.348 44); avoine a) Zaghouan moins d'un hectolitre 1.153 60 (1.153 06); avoine b) Tadjerouine moins "
        "d'un hectolitre 75 77 (75 17); pois chiches b) Mateur 4 hectol. 47 79 (45 79); lin b) Ouled-Aoun 6 "
        "hectol. 0 69 (0 09). Lin b) (f210): the 1 hectol. figure 0 60 of Ouled-Aoun is printed one line too low, "
        "on Fraichiches (whose TOTAL is »): stored on Ouled-Aoun (`row_realigned`; its TOTAL 2 39 and the "
        "Récapitulation place it), Fraichiches derived as 0. Misprinted check figures (the stored cells agree "
        "with the other checks): blé c) Cap-Bon 1 hectol. 1.760 57 for 1.780 57, Aïn-Draham 1 hectol. 401 36 for "
        "404 36, Fraichiches moins d'un hectolitre 2.677 19 for 2.677 79 (their TOTAL and the Totaux agree with "
        "a) + b)); orge a) TOTAL of Ouled-Ayar 80 29 for 80 20; orge b) TOTAL of Ouled-Aoun 8.206 39 for 8.296 39 "
        "and Totaux 4 hectol. 23.375 45 for 23.371 45 (the Récapitulation agrees with 8.296 39 and 23.371 45); "
        "avoine a) TOTAL of Souk-el-Arba 1.802 44 for 1.802 84; avoine b) TOTAL of Fraichiches 9 68 for 9 63; "
        "avoine c) Ouled-Ayar 6 hectol. 45 71 for 45 74 and Totaux 6 hectol. 13.070 07 for 13.090 07; lin c) "
        "(f211): the moins d'un hectolitre and TOTAL figures of Majeur, Kairouan and Djelass printed one line "
        "too high (Majeur 2 40 for 13 43, Kairouan 11 03 for 4, Djelass 4 for »; the c) Totaux agree with a) + "
        "b)). Failures of the TOTAL, Totaux and c) checks not listed here are consequences of the cells above."),
    "sgt1923": (
        "sgt1923. Faulty cells (flag `total_mismatch`; the line's TOTAL, the column Totaux and the c) "
        "Récapitulation all require another value): blé b) Djelass moins d'un hectolitre printed 1.275 84 "
        "(1.075 84); fèves a) Mahdia 6 hectol. 1 50 (4 50). Misprinted check figures: blé c) (f680) the 5 hectol. "
        "figure 6 34 of Ouerghemma (5 + 1 34) printed on the Matmata line (the TOTAL of each line places it); "
        "fèves c) Bizerte moins d'un hectolitre 2 97 for 4 97 (its TOTAL and the Totaux agree with a) + b)). "
        "The other failures of the TOTAL, Totaux and c) checks are consequences of these cells."),
    "sgt1924": (
        "sgt1924. Faulty cell (flag `total_mismatch`; the line's TOTAL, the column Totaux and the c) "
        "Récapitulation all require another value): fèves b) Béja 6 hectol. printed 1.445 59 (1.445 69). "
        "Misprinted check figures: blé b) Totaux moins d'un hectolitre 118.184 09 for 110.184 09 (the Totaux "
        "TOTAL 378.607 62 and the c) Totaux 113.367 67 = 3.183 58 + 110.184 09 agree with the lines); orge c) "
        "L'Arad 6 hectol. 192 85 for 192 89 (its TOTAL and the Totaux agree with a) + b)). Avoine c) Totaux 2 "
        "hectol. printed \"1.31  21\" with a figure missing (read '?', not checked); lin c) Ouled-Ayar TOTAL "
        "printed as a dash."),
    "sgt1925": (
        "sgt1925 (two-page spreads; the 6 hectol. column is printed against the gutter). Faulty cells (flag "
        "`total_mismatch`; the line's TOTAL, the column Totaux and the c) Récapitulation require another value): "
        "blé a) Souk-el-Arba 4 hectol. printed 36 (»), Djebéniana new land 9 (5); blé b) Aïn-Draham 1 hectol. and "
        "moins d'un hectolitre printed \"69 »\" and \"20 »\" (0 69, 0 20), Soliman 5 hectol. \"90 »\" (0 90), "
        "Fraichiches 6 hectol. 881 41 (481 41); orge a) Nabeul 6 hectol. 359 88 (359 98), Hemmama new land 4 40 "
        "(4); orge b) Souassi 6 hectol. 7.297 » (7.200 97), Souk-el-Arba 4 hectol. 485 23 (485 28), Téboursouk 2 "
        "hectol. 208 82 (208 88); avoine a) Bizerte moins d'un hectolitre 47 37 (46 37), Fraichiches new land » "
        "(23: the c) line and the column Totaux 3.022 57; a further 0 50 of the Totaux, probably Djelass, stays "
        "unplaced); avoine b) Djelass 6 hectol. \"130 »\" (1 30), Souk-el-Arba 3 hectol. 6 64 (8 64); fèves a) "
        "Soliman 2 hectol. 16 » (16 50), Medjez-el-Bab 6 hectol. 1.292 93 (1.292 13); fèves b) Béja 6 hectol. "
        "2.006 45 (2.600 45), Hemmama 2 hectol. 0 08 (1 08); lin a) Sousse moins d'un hectolitre 12 75 (18 75). "
        "Figures whose last digit is hidden in the gutter were read where the TOTAL or the c) table fixes them "
        "(blé b) Soliman 6 hectol. \"5.420 6\" = 5.420 60, fèves a) Soliman \"125 8\" = 125 84; flag "
        "`derived_from_totals`), otherwise '?' and solved as TOTAL - the other classes (flag "
        "`derived_from_totals`; every solved value agrees with the visible figures). Misprinted check figures "
        "(the stored cells agree with the other checks): blé a) TOTAL of Monastir 58 56 (58 66); blé c) Souk-el-"
        "Arba moins d'un hectolitre 74 84, Tadjérouine 991 29, Oulad Aoun 6 hectol. 9.757 71, Djerid 5 hectol. 17 "
        "» (0 17) and 1 hectol. 60 09; orge c) Béja 2 hectol. 0 91, Medjez-el-Bab moins d'un hectolitre 151 64, "
        "Djebéniana TOTAL 37.795 48 (35.795 48), L'Arad moins d'un hectolitre 366 97 (336 97), Oulad Ayar new "
        "land 50 » (0 50); avoine c) Aïn-Draham TOTAL 225 70, banlieue 1 hectol. 16 20, Téboursouk 3 hectol. 41 "
        "70, Oulad Aoun 1 hectol. », Sousse 4 hectol. 44 83 (84 83), Djelass 6 hectol. 0 30 and TOTAL 175 25, "
        "and Totaux off by a few ares; fèves c) Bizerte TOTAL 4.093 74 (4.096 74), Soliman 5 and 3 hectol., "
        "Sousse moins d'un hectolitre, Totaux 1 hectol. 1.672 05 (1.679 05) and TOTAL; pois chiches a) Totaux 3 "
        "hectol. 14 74 (14 75); pois chiches c) Zaghouan 2 hectol. 10 50 (10 54), Tadjérouine TOTAL 14 95; maïs "
        "b) Totaux TOTAL 17.739 95 (17.939 95); maïs c) Mateur 5 hectol. 31 21 (35 21); sorgho c) Béja new land "
        "» (4); lin c) banlieue moins d'un hectolitre 3 27, Nabeul TOTAL 46 90, Medjez-el-Bab moins d'un "
        "hectolitre 0 29 (0 09), Fraichiches new land » (10), Totaux TOTAL 2.557 63 (2.257 63). The other "
        "failures of the TOTAL, Totaux and c) checks are consequences of these cells."),
}


# ----------------------------------------------------------------- survey

SURVEY = {
    "sgt1922": "f188-f211 (pp. 164-187), three pages per crop (a) européens, b) indigènes, c) Récapitulation; "
               "Blé ... Lin), 31 caïdats as printed (Nefzaoua ... Djerid; Cap-Bon one caïdat; blé a) without "
               "Djerid) x 7 yield classes, TOTAL and exempted new land [transcribed, every cell read on the "
               "image]. Faulty cells (total_mismatch): blé a) Banlieue 6 hectol. and 3 hectol., Souk-el-Arba "
               "2 hectol.; blé b) Ouled-Ayar 4 hectol.; avoine a) Zaghouan and avoine b) Tadjerouine moins d'un "
               "hectolitre; pois chiches b) Mateur 4 hectol.; lin b) Ouled-Aoun 6 hectol. Lin b): a figure "
               "printed one line too low (row_realigned). Several misprinted TOTAL, Totaux and c) figures.",
    "sgt1923": "f678-f701 (pp. 176-199), same layout as sgt1922 (31 caïdats; blé a) without Djerid) [transcribed, "
               "every cell read on the image]. Faulty cells (total_mismatch): blé b) Djelass moins d'un "
               "hectolitre, fèves a) Mahdia 6 hectol.; misprinted check figures in blé c) and fèves c).",
    "sgt1924": "f1174-f1197 (pp. 184-207), same layout as sgt1922 (31 caïdats; blé a) without Djerid) "
               "[transcribed, every cell read on the image]. Faulty cell (total_mismatch): fèves b) Béja 6 "
               "hectol.; misprinted check figures in blé b) Totaux and orge c).",
    "sgt1925": "f220-f267 (pp. 196-243), two-page spreads (left page: région, contrôle civil, caïdat and the 6 "
               "hectol. column; right page: 5 hectol. ... new land), joined as one table per crop and roll; 36 "
               "caïdats (Cap-Bon printed in two lines, Nabeul and Soliman) [transcribed, every cell read on the "
               "image]. The 6 hectol. figures against the gutter are partly hidden: solved from the TOTAL "
               "(derived_from_totals). 18 faulty cells (total_mismatch), many misprinted c) figures.",
    "sgt1926": "f776-f783 (pp. 212-219), one page per crop, a) Blé ... h) Lin, européens and indigènes in one "
               "table (35 caïdats; Cap-Bon one caïdat) [transcribed, every cell read on the image]. f776 blé: "
               "La Skhira européens misprinted (total_mismatch); f779 fèves: Sousse européens, last figure "
               "broken, derived from the Récapitulation; f783 lin: Cap-Bon indigènes misprinted (total_mismatch).",
    "sgt1927": "f238-f245 (pp. 210-217), same layout, 36 caïdats (Cap-Bon printed as Nabeul and Soliman) "
               "[transcribed, every cell read on the image]; every check passes.",
    "sgt1928": "f762-f769 (pp. 210-217), same layout as sgt1927 [transcribed, every cell read on the image]. f762 "
               "blé: indigènes of Gafsa and Djerid printed one line too high and none for Hemmama (stored on "
               "their lines, row_realigned; Hemmama derived from the Récapitulation).",
    "sgt1929": "f240-f247 (pp. 212-219), same layout as sgt1927 [transcribed, every cell read on the image]. "
               "Faulty cells: avoine Kairouan and pois chiches Mateur indigènes (total_mismatch); misprinted "
               "check figures in maïs, sorgho; orge new-land Totaux 5.00 off (unresolved).",
    "sgt1930": "f774-f781 (pp. 216-223), same layout as sgt1927 [transcribed, every cell read on the image]. "
               "Faulty cell: fèves Aïn-Draham indigènes (total_mismatch); avoine indigènes Totaux misprinted.",
    "sgt1935": "f133 (p. 113), ACHOUR (1935), one table, the eight crops, Tunisia totals [transcribed, every cell "
               "read on the image].",
}
NOT_DONE = (
    "Every achour table of the ten editions is transcribed, every cell read on native-resolution crops: the "
    "yield-class tables of sgt1922 (f188-f211), sgt1923 (f678-f701), sgt1924 (f1174-f1197) and sgt1925 (two-page "
    "spreads f220-f267; per crop a) européens, b) indigènes, c) récapitulation x 7 yield classes, TOTAL and the "
    "exempted new land; a) and b) stored, TOTAL, Totaux and c) checked), the one-page-per-crop tables of "
    "sgt1926-sgt1930 (f776-f783, f238-f245, f762-f769, f240-f247, f774-f781) and sgt1935 (f133).")


def write_survey(secs, res):
    L = ["# Achour: survey of every edition", "",
         "The achour (tithe on cereals) tables of the *Finances* chapter, view by view. Views from "
         "`finance_survey.md`, confirmed on the page images. Extraction: `extract_finance_achour.py`.", ""]
    L += [f"- **{e}**: {t}" for e, t in SURVEY.items()]
    L += ["", "## Image reading", ""] + coverage_lines(secs)
    L += ["", "## Coverage", "", NOT_DONE, ""]
    (OUT / f"{NAME}_survey.md").write_text("\n".join(L) + "\n")


def build(write=True):
    secs = []
    for ed in EDS:
        p = TR / f"finance_achour_{ed}.txt"
        if p.exists():
            secs += parse(p, ed)
    derive(secs)
    checks(secs)
    recs = []
    for s in secs:
        recs += cells(s)
    eds = [e for e in ORDER if any(r["census"] == e for r in recs)]
    flagged = [f"{r['census']} f{r['gallica_view']} {r['caidat']} / {r['crop']} / {r['roll']} / {r['yield_class']} / "
               f"{r['measure']} = {r['value']} ({r['flag']})" for r in recs if r["flag"]]
    res = {NAME: dict(rows=len(recs), checks=CHK.n[O], failed=list(CHK.fail[O]), editions=eds, flagged=flagged,
                      read_on_image={s["ed"] + " f" + str(s["view"]): s["img"] for s in secs})}
    if write:
        cols = COMMON + DIMS + ["value", "flag"]
        write_csv(NAME, cols, recs)
        paras = PARAS + ([FAILS] if CHK.fail[O] else []) + [FAILS_YIELD[e] for e in eds if e in FAILS_YIELD] + ["Survey of the tables in every edition: "
                                                             "`finance_achour_survey.md`."]
        write_notes(NAME, CHAPTER, SCRIPT, recs, cols, DOC, TITLE_FR, TITLE_EN, paras, CHK.n[O], CHK.fail[O], 0, [],
                    coverage_lines(secs), RULE, UNIT)
        md = OUT / f"{NAME}.md"
        md.write_text(md.read_text().replace("`../transcribed/finance_<edition>.txt`",
                                             "`../transcribed/finance_achour_<edition>.txt`"))
        write_validation(OUT / f"{NAME}_validation.json", dict(res, _survey=SURVEY, _coverage=NOT_DONE))
        write_survey(secs, res)
    return res


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
