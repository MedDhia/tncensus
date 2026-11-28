#!/usr/bin/env python3
"""Commerce chapter (chapter XII *Commerce et navigation*) of the Statistique générale de la Tunisie.

Done so far: editions sgt1922, sgt1923, sgt1924, tables *Renseignements généraux* a) Mouvement global,
b) par classe, c) par catégorie and d) par pays de provenance et de destination (valeur en francs).
Later edition groups (sgt1925-27, sgt1928-30, sgt1935-39) extend this script: add the edition to EDITIONS_DONE,
write transcribed/commerce_<edition>.txt with the same section names and row codes, and add new tables to TABLES.

  python3 extract_commerce.py check   parse the transcriptions, run every check, print failures
  python3 extract_commerce.py build   ... and write csv/commerce_*.csv, their .md notes,
                                      csv/commerce_survey.md is hand-written (not overwritten),
                                      csv/commerce_validation.json

Source of truth: transcribed/commerce_<edition>.txt (format in yb_tables.py). Yearly series printed for
overlapping ten-year windows: SPEC_ADDENDUM rule 4 (each year from the latest edition printing it, every other
printing compared cell by cell). Printed totals are used for checks only.
"""
import sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path as _Path

sys.path.insert(0, str(_Path(__file__).resolve().parent))  # shared helper yb_tables.py
from yb_tables import (COMMON, check_col_totals, check_row, EDITIONS, ORDER, OUT, TR, Checks, coverage_lines, parse, select_latest, ssum, where,
                       write_csv, write_notes, write_validation)

CHAPTER = "Commerce et navigation"
SCRIPT = "extract_commerce.py"
PREFIX = "commerce"
EDITIONS_DONE = ["sgt1922", "sgt1923", "sgt1924"]

# chapter title view .. last view before the next chapter (Colonisation), confirmed on the images
CHAPTER_VIEWS = {"sgt1922": (281, 436), "sgt1923": (771, 926), "sgt1924": (1275, 1430)}

FLOW = {"import": "Importation", "export": "Exportation"}
PRODUCT_CLASS = {"animal": "Matières animales", "vegetal": "Matières végétales", "mineral": "Matières minérales",
                 "manufactures": "Fabrications"}

CHK = Checks()
T = "commerce_trade_by_class"

# Cells checked on the crops and found misprinted; the printed value is kept and flagged.
# (edition, section, row, column) -> note
MISPRINTS = {
    (ed, "by_class", row, "1915"): note
    for ed in EDITIONS_DONE
    for row, note in [
        ("manufactures.import", "printed 45.087.612; the a) import total and the c) categories give 45.087.412"),
    ]
}


def rows_of(sec):
    return {r["label"]: r["cells"] for r in sec["rows"] if "cells" in r}


def check_general(sec):
    R = rows_of(sec)
    for c in sec["cols"]:
        CHK.eq(T, f"{where(sec)} {c}: Total = import + export", ssum([R["import"][c].value, R["export"][c].value]),
               R["Total"][c].value)


def check_by_class(sec, general):
    R = rows_of(sec)
    for c in sec["cols"]:
        for k in PRODUCT_CLASS:
            CHK.eq(T, f"{where(sec)} {c}: {k} Total = import + export",
                   ssum([R[f"{k}.import"][c].value, R[f"{k}.export"][c].value]), R[f"Total@{k}"][c].value)
        g = general.get((sec["ed"], c))
        if g:
            for f in FLOW:
                CHK.eq(T, f"{where(sec)} {c}: sum of classes, {f} = a) Mouvement global {f}",
                       ssum(R[f"{k}.{f}"][c].value for k in PRODUCT_CLASS), g[f])


def records(sec):
    out = []
    for lab, cells in rows_of(sec).items():
        if lab.startswith("Total"):
            continue
        k, f = lab.split(".")
        for c in sec["cols"]:
            cell = cells[c]
            flag = cell.flag
            if (sec["ed"], sec["table"], lab, c) in MISPRINTS and not flag:
                flag = "total_mismatch"
            out.append({"census": sec["ed"], "table_id": "general_b", "gallica_ark": sec["ark"],
                        "source_page": sec["page"], "gallica_view": sec["view"], "year": int(c),
                        "product_class": k, "product_class_fr": PRODUCT_CLASS[k], "flow": f, "flow_fr": FLOW[f],
                        "measure": "value", "measure_fr": "valeur", "unit": "francs",
                        "value": cell.value, "flag": flag})
    return out


DIMS = ["product_class", "product_class_fr", "flow", "flow_fr", "measure", "measure_fr", "unit"]
DOC = {
    "census": "edition the value is taken from: the latest edition printing that year (rule 4)",
    "table_id": "`general_b` (Renseignements généraux, b) Résumé ... par classe de produits)",
    "gallica_ark": "Gallica volume ark (views are numbered within a volume)",
    "source_page": "printed page number",
    "gallica_view": "Gallica view (fNNNN)",
    "year": "calendar year of the trade",
    "product_class": "`animal`, `vegetal`, `mineral`, `manufactures` (the four classes of the customs nomenclature)",
    "product_class_fr": "as printed",
    "flow": "`import` or `export`",
    "flow_fr": "as printed",
    "measure": "`value`",
    "measure_fr": "valeur",
    "unit": "`francs`",
    "value": "value in francs as printed",
    "flag": "empty, or `total_mismatch` (see notes)",
}
RULE4 = ("Selection (SPEC_ADDENDUM rule 4): each edition prints the last ten years; each year is stored once, from "
         "the latest edition printing it (1913 from sgt1922, 1914 from sgt1923, 1915-1924 from sgt1924); every "
         "other printing of the same cell is compared and the differences listed below.")
PARAS = [
    "The printed a) table *Mouvement global des importations et des exportations* (importation, exportation, "
    "total) is not stored: its import and export lines equal the sums of the four classes and are used as a check "
    "(the b) table's class totals, import + export, likewise). Total trade by year = sum of the stored rows.",
    "Footnote (1), printed under the table in every edition (translated): until 1919, to make comparisons with "
    "earlier years easier, the price increases resulting from the war were not taken into account in determining "
    "values. Since 1920 these increases are included, the value of imports and exports being set by a permanent "
    "commission on the basis of valuation rates equivalent to those of Algeria.",
    "1915: the class totals of `vegetal` (91.463.545) and `manufactures` (53.968.433) do not agree with their "
    "import and export lines (37.546.533 + 53.877.012 = 91.423.545; 45.087.612 + 8.921.021 = 54.008.633), and "
    "the four import lines sum to 200 francs more than the a) Mouvement global import (107.246.504). The c) "
    "category table settles it: its vegetal categories sum to 37.546.533 (the printed vegetal import is right, so "
    "the vegetal Total is misprinted, 40.000 too high) and its manufactured categories sum to 45.087.412, which "
    "with the other three classes gives exactly 107.246.504. The manufactures import cell (45.087.612) is "
    "therefore misprinted by 200 francs (flagged `total_mismatch`), and the manufactures Total is a second "
    "misprint (40.000 too low; totals are not stored). All three editions print the same figures; re-read on "
    "zoomed crops of f1276 (sgt1924) and on f282, f772.",
]


# ----------------------------------------------------------------- c) par catégorie de produits

T_CAT = "commerce_trade_by_category"
# row code -> (product class, category as printed)
CATEGORY = {
    "live_animals": ("animal", "Animaux vivants"),
    "animal_products": ("animal", "Produits et dépouilles d'animaux"),
    "fisheries": ("animal", "Pêches"),
    "animal_medicinal": ("animal", "Substances animales propres à la médecine et à la parfumerie"),
    "hard_materials": ("animal", "Matières dures à tailler"),
    "farinaceous_foods": ("vegetal", "Farineux alimentaires"),
    "fruits_seeds": ("vegetal", "Fruits et graines"),
    "colonial_goods": ("vegetal", "Denrées coloniales de consommation"),
    "oils_saps": ("vegetal", "Huiles et sucs végétaux"),
    "medicinal_plants": ("vegetal", "Espèces médicinales"),
    "wood": ("vegetal", "Bois"),
    "fibres": ("vegetal", "Filaments, tiges et fruits à ouvrer"),
    "dyes_tannins": ("vegetal", "Teintures et tanins"),
    "vegetal_misc": ("vegetal", "Produits et déchets divers"),
    "beverages": ("vegetal", "Boissons"),
    "stones_fuels": ("mineral", "Marbres, pierres, terres et combustibles minéraux"),
    "metals": ("mineral", "Métaux"),
    "chemicals": ("manufactures", "Produits chimiques"),
    "prepared_dyes": ("manufactures", "Teintures préparées"),
    "colours": ("manufactures", "Couleurs"),
    "compositions": ("manufactures", "Compositions diverses"),
    "pottery_glass": ("manufactures", "Poteries, verres et cristaux"),
    "yarns": ("manufactures", "Fils"),
    "fabrics": ("manufactures", "Tissus"),
    "paper": ("manufactures", "Papier et ses applications"),
    "leather_goods": ("manufactures", "Peaux et pelleteries ouvrées"),
    "metal_goods": ("manufactures", "Ouvrages en métaux"),
    "arms": ("manufactures", "Armes, poudres et munitions"),
    "furniture": ("manufactures", "Meubles et ouvrages en bois"),
    "musical_instruments": ("manufactures", "Instruments de musique"),
    "basketry": ("manufactures", "Ouvrages de sparterie et de vannerie"),
    "misc_goods": ("manufactures", "Ouvrages en matières diverses"),
}
# Misprints identified by a failing check (class total of table b) or TOTAUX) together with the printed
# five-year averages; printed value kept, flagged total_mismatch. (category.flow, year) -> editions
CAT_MISPRINTS = {
    ("beverages.import", "1918"): ("sgt1922", "sgt1923"),
    ("vegetal_misc.export", "1919"): ("sgt1922", "sgt1923", "sgt1924"),
    ("pottery_glass.export", "1916"): ("sgt1922", "sgt1923", "sgt1924"),
    ("yarns.export", "1918"): ("sgt1922", "sgt1923"),
}


def check_by_category(secs, by_class):
    """secs: the by_category sections of one edition (two spreads, each split over two views)."""
    cells = defaultdict(dict)
    where_of = {}
    for s in secs:
        for lab, cs in rows_of(s).items():
            for c in s["cols"]:
                cells[c][lab] = cs[c].value
                where_of[c] = where(s)
    for c in sorted(cells):
        R = cells[c]
        for f in FLOW:
            CHK.eq(T_CAT, f"{where_of[c]} {c}: sum of categories, {f} = TOTAUX {f}",
                   ssum(R[f"{k}.{f}"] for k in CATEGORY), R[f"Total.{f}"])
            for cl in PRODUCT_CLASS:
                printed = by_class.get((secs[0]["ed"], c, f"{cl}.{f}"))
                CHK.eq(T_CAT, f"{where_of[c]} {c}: categories of class {cl}, {f} = b) class line",
                       ssum(R[f"{k}.{f}"] for k, (kc, _) in CATEGORY.items() if kc == cl), printed)


def records_cat(sec):
    out = []
    for lab, cells in rows_of(sec).items():
        if lab.startswith("Total"):
            continue
        k, f = lab.split(".")
        for c in sec["cols"]:
            cell = cells[c]
            flag = cell.flag
            if sec["ed"] in CAT_MISPRINTS.get((lab, c), ()) and not flag:
                flag = "total_mismatch"
            out.append({"census": sec["ed"], "table_id": "general_c", "gallica_ark": sec["ark"],
                        "source_page": sec["page"], "gallica_view": sec["view"], "year": int(c),
                        "product_class": CATEGORY[k][0], "product_class_fr": PRODUCT_CLASS[CATEGORY[k][0]],
                        "product_category": k, "product_category_fr": CATEGORY[k][1],
                        "flow": f, "flow_fr": FLOW[f], "measure": "value", "measure_fr": "valeur",
                        "unit": "francs", "value": cell.value, "flag": flag})
    return out


def select_legible(recs, key):
    """Rule 4 with one refinement: an illegible printing (gutter) gives way to the latest legible one."""
    by = defaultdict(list)
    for r in recs:
        by[tuple(r[k] for k in key)].append(r)
    keep, n_ill = [], 0
    for rs in by.values():
        ok = [r for r in rs if r["value"] is not None]
        n_ill += len(rs) - len(ok)
        keep += ok if ok else rs
    kept, compared, diffs = select_latest(keep, key)
    return kept, compared, diffs, n_ill


CAT_DIMS = ["product_class", "product_class_fr", "product_category", "product_category_fr", "flow", "flow_fr",
            "measure", "measure_fr", "unit"]
CAT_DOC = dict(DOC, table_id="`general_c` (Renseignements généraux, c) Résumé ... par catégorie de produits)",
               census="edition the value is taken from: the latest edition printing that year legibly (rule 4; "
                      "see notes on the gutter)",
               product_category="code of the category of the customs nomenclature (32 categories)",
               product_category_fr="category as printed",
               flag="empty, or `total_mismatch` (see notes)")


def build_category(secs, by_class, write):
    recs, used = [], []
    for ed in EDITIONS_DONE:
        es = [s for s in secs if s["table"] == "by_category" and s["ed"] == ed]
        if not es:
            continue
        check_by_category(es, by_class)
        for s in es:
            recs += records_cat(s)
            used.append(s)
    key = ["year", "product_category", "flow"]
    kept, compared, diffs, n_ill = select_legible(recs, key)
    kept.sort(key=lambda r: (r["year"], list(CATEGORY).index(r["product_category"]), r["flow"]))
    fails = CHK.fail[T_CAT]
    flagged = [f"{r['census']} {r['year']} {r['product_category']} {r['flow']}" for r in kept if r["flag"]]
    res = dict(rows=len(kept), checks=CHK.n[T_CAT], failed=list(fails), overlap_compared=compared,
               overlap_diffs=[list(d) for d in diffs], flagged=flagged, editions=EDITIONS_DONE,
               value_type="francs", illegible_printings_not_compared=n_ill)
    if write:
        cols = COMMON + CAT_DIMS + ["value", "flag"]
        write_csv(T_CAT, cols, kept)
        paras = [
            "The table prints, for each of the 32 categories of the customs nomenclature (5 animal, 10 vegetal, "
            "2 mineral, 15 manufactured), the import and export values of the last ten years, followed on the odd "
            "view by three five-year averages (*Moyenne des années*). The averages and the TOTAUX lines are not "
            "stored; they were used as checks. The sum of the categories of each class is checked against the "
            "class line of table b) (`commerce_trade_by_class`) of the same edition. The same footnote on "
            "valuation (war price rises taken into account from 1920 only) applies.",
            "Gutter. Each spread prints the first four years on the even view and the rest on the odd view; the "
            "fourth year sits against the binding. sgt1923: the 1917 column (f774, f776) loses part of its last "
            "digit but every value is readable; the 1918 column (f775, f777) loses the leading digit(s) on 25 "
            "category lines and both TOTAUX, transcribed `?` (a value is transcribed only where its first digit is "
            "wholly visible). sgt1924: the 1918 column (f1278, f1280) loses its last three digits on every "
            "line (all `?` except `arms` export, printed », i.e. nil), and the 1919 column of f1279 loses the leading digit on 11 lines (`?`). A year is "
            "stored from the latest edition printing it legibly: 1918 from sgt1923 where legible (`arms` export from sgt1924), otherwise "
            "sgt1922; 1919 vegetal/mineral lines concerned from sgt1923. Illegible printings are not compared "
            f"({n_ill} printed cells).",
            "sgt1924 f1280: the two lines of *Produits chimiques* are labelled Exportation / Importation (inverted "
            "relative to every other category and to the other editions); the figures are in the usual order "
            "(import first, identical to sgt1922-1923 for the years in common, and the class checks pass), so they "
            "are stored as import / export.",
            "Misprints identified (printed values kept, flagged `total_mismatch`): (i) `beverages` import 1918, "
            "printed 2.604.952 in sgt1922 and sgt1923: the vegetal class line (52.569.271) and TOTAUX "
            "(207.442.588) are 1.000.000 lower than the categories, and the printed 1918-1922 average (3.419.698) "
            "implies 1.604.952. (ii) `vegetal_misc` export 1919, printed 2.780.995 in all three editions: the "
            "class line and TOTAUX are 9.000 higher and the 1918-1922 average (3.746.430) implies 2.789.995. "
            "(iii) `pottery_glass` export 1916, printed 140.527 in all three editions: the manufactures line and "
            "TOTAUX are 36.000 lower, and the 1913-1917 average (148.564) implies 104.527. (iv) `yarns` export "
            "1918, printed 36.258 (sgt1922, sgt1923): the manufactures line and TOTAUX are 6.000 lower and the "
            "1918-1922 average (368.325) implies 30.258. (i) is illegible in the 1918 gutter column of both "
            "sgt1923 and sgt1924 (the leading digit, which carries the error, is hidden), so the stored value "
            "comes from sgt1922; (iv) is legible in sgt1923 and stored from it; both carry the flag.",
            "The sgt1923 and sgt1924 lines of this table were re-typed in full from the page images (f774-777, "
            "f1278-1281), independently of the sgt1922 transcription; every legible cell agrees with the earlier "
            "transcription, the only changes being legibility judgments in the gutter columns (sgt1923 1918: eight "
            "cells whose leading digit is only partly visible now `?`; sgt1924 1918 `arms` export now read as nil).",
        ]
        expl = [
            "Explanation of the other failed checks (each cell re-read on a native-resolution crop): "
            "1913 export (sgt1922): the categories sum to 300 francs less than TOTAUX and the manufactures line "
            "(178.663.605 and 12.717.715, both agreeing with tables a) and b)); the averages do not single out a "
            "cell, nothing flagged. "
            "1915 manufactures import (all editions): the categories give 45.087.412 against the b) line 45.087.612; "
            "TOTAUX (107.246.504) agrees with the categories, so the 200-franc error is in table b) (see "
            "`commerce_trade_by_class`, where this cell is already flagged). "
            "1923 animal import (sgt1923, sgt1924): categories 2.000 below the b) class line and TOTAUX; the "
            "sgt1923 1919-1923 average of `live_animals` import (11.877.863) implies 16.934.116 for the printed "
            "16.932.116, but the sgt1924 1920-1924 average (12.637.641) agrees with the printed cell, so nothing is "
            "flagged. "
            "1924 (sgt1924): the categories sum to 927.943.822 (import) and 582.343.545 (export) against TOTAUX "
            "927.943.882 and 582.353.545 (differences 60 and 10.000); the averages locate no cell. The b) class "
            "lines for 1924 disagree much more (manufactures import 606.302.506 against 604.302.406 here, export "
            "44.739.278 against 44.630.178, animal export 54.347.560 against 54.347.670): TOTAUX of this table "
            "agree with table a), so the 1924 errors are mostly in table b). Comparison with sgt1925 will settle "
            "these when that edition is added.",
            "Printed averages also disagree, without any failing total, for `fibres` import 1913-1917 (sgt1922: "
            "222.643 printed, cells give 262.644) and `colonial_goods` export 1918-1922 (1.019.121 printed, cells "
            "give 1.018.521): averages are not stored and were not used to change any cell.",
        ]
        write_notes(T_CAT, CHAPTER, SCRIPT, kept, cols, CAT_DOC,
                    "Renseignements généraux : résumé des importations et des exportations par catégorie de produits "
                    "(valeur en francs)",
                    "General information: imports and exports by category of products (value in francs)",
                    paras + expl + ["Survey of the whole chapter: `commerce_survey.md`."],
                    CHK.n[T_CAT], fails, compared, diffs, coverage_lines(used),
                    RULE4.replace("from the latest edition printing it", "from the latest edition printing it "
                                  "legibly"),
                    "Unit: francs (current values). value_type: francs.")
    return res


# ----------------------------------------------------------------- d) par pays de provenance et de destination

T_ORG = "commerce_trade_by_origin_group"
ORIGIN = {"F": ("france_algeria", "de France et d'Algérie"),
          "E": ("foreign_colonies", "de l'Étranger et des Colonies françaises")}
# Misprints located by the Récapitulation line and the b) class lines; printed value kept, flagged.
# (row, column) -> (editions, note)
ORG_MISPRINTS = {
    ("manufactures.import", "1915.E"): ("sgt1922", "sgt1923", "sgt1924"),
    ("animal.import", "1918.F"): ("sgt1922", "sgt1923", "sgt1924"),
    ("manufactures.import", "1918.E"): ("sgt1922", "sgt1923", "sgt1924"),
    ("manufactures.import", "1920.F"): ("sgt1923", "sgt1924"),
    ("manufactures.import", "1923.F"): ("sgt1923", "sgt1924"),
    ("manufactures.import", "1923.E"): ("sgt1923", "sgt1924"),
}


def check_origin(sec, by_class):
    R = rows_of(sec)
    for c in sec["cols"]:
        for f in FLOW:
            CHK.eq(T_ORG, f"{where(sec)} {c}: classes, {f} = Récapitulation",
                   ssum(R[f"{k}.{f}"][c].value for k in PRODUCT_CLASS), R[f"Recap.{f}"][c].value)
        CHK.eq(T_ORG, f"{where(sec)} {c}: Récapitulation import + export = Total",
               ssum([R["Recap.import"][c].value, R["Recap.export"][c].value]), R["Total"][c].value)
    for y in sorted({c.split(".")[0] for c in sec["cols"]}):
        for k in PRODUCT_CLASS:
            for f in FLOW:
                CHK.eq(T_ORG, f"{where(sec)} {y}: {k} {f}, France-Algérie + Étranger = b) class line",
                       ssum([R[f"{k}.{f}"][f"{y}.F"].value, R[f"{k}.{f}"][f"{y}.E"].value]),
                       by_class.get((sec["ed"], y, f"{k}.{f}")))


def records_org(sec):
    out = []
    for lab, cells in rows_of(sec).items():
        if lab.startswith(("Recap", "Total")):
            continue
        k, f = lab.split(".")
        for c in sec["cols"]:
            y, g = c.split(".")
            cell = cells[c]
            flag = cell.flag
            if sec["ed"] in ORG_MISPRINTS.get((lab, c), ()) and not flag:
                flag = "total_mismatch"
            out.append({"census": sec["ed"], "table_id": "general_d", "gallica_ark": sec["ark"],
                        "source_page": sec["page"], "gallica_view": sec["view"], "year": int(y),
                        "product_class": k, "product_class_fr": PRODUCT_CLASS[k],
                        "origin_group": ORIGIN[g][0], "origin_group_fr": ORIGIN[g][1],
                        "flow": f, "flow_fr": FLOW[f], "measure": "value", "measure_fr": "valeur",
                        "unit": "francs", "value": cell.value, "flag": flag})
    return out


ORG_DIMS = ["product_class", "product_class_fr", "origin_group", "origin_group_fr", "flow", "flow_fr",
            "measure", "measure_fr", "unit"]
ORG_DOC = dict(DOC, table_id="`general_d` (Renseignements généraux, d) Classement des produits par pays de "
                             "provenance et de destination)",
               census=CAT_DOC["census"],
               origin_group="`france_algeria` (France and Algeria) or `foreign_colonies` (foreign countries and "
                            "French colonies): country group of provenance (imports) or destination (exports)",
               origin_group_fr="column heading as printed",
               flag="empty, `illegible` (gutter, NA) or `total_mismatch` (see notes)")


def build_origin(secs, by_class, write):
    recs, used = [], []
    for s in secs:
        if s["table"] == "by_origin_group":
            check_origin(s, by_class)
            recs += records_org(s)
            used.append(s)
    key = ["year", "product_class", "origin_group", "flow"]
    kept, compared, diffs, n_ill = select_legible(recs, key)
    kept.sort(key=lambda r: (r["year"], list(PRODUCT_CLASS).index(r["product_class"]), r["origin_group"],
                             r["flow"]))
    fails = CHK.fail[T_ORG]
    flagged = [f"{r['census']} {r['year']} {r['product_class']} {r['origin_group']} {r['flow']}"
               for r in kept if r["flag"]]
    res = dict(rows=len(kept), checks=CHK.n[T_ORG], failed=list(fails), overlap_compared=compared,
               overlap_diffs=[list(d) for d in diffs], flagged=flagged, editions=EDITIONS_DONE,
               value_type="francs", illegible_printings_not_compared=n_ill)
    if write:
        cols = COMMON + ORG_DIMS + ["value", "flag"]
        write_csv(T_ORG, cols, kept)
        paras = [
            "For each of the four classes of products, the table splits imports and exports between two groups "
            "of countries: France and Algeria, and foreign countries with the French colonies. A Récapitulation "
            "(sum of the classes) and a TOTAL (imports + exports) close each column; they are not stored and "
            "were used as checks, together with the b) class lines (`commerce_trade_by_class`: France-Algérie + "
            "Étranger = class line of the same edition).",
            "Gutter: the first five years are on the even view, the last five on the odd view. sgt1922 f289: the "
            "1918 France-Algérie column loses leading digits on `mineral` export and TOTAL (`?`); sgt1923 f779: "
            "the 1919 France-Algérie column is cut on every line (all `?`); these are stored from the latest "
            f"legible printing ({n_ill} illegible printed cells, not compared).",
            "Misprints (printed values kept, flagged `total_mismatch`): (i) 1915 `manufactures` import, Étranger "
            "19.776.907 (all editions): the classes exceed the Récapitulation by 200 and the c) categories give "
            "45.087.412 for the class, so this cell (not France-Algérie) carries the 200-franc error already seen "
            "in the b) class line. (ii) 1918 `animal` import, France-Algérie 5.027.593 (all editions): the "
            "Récapitulation is 1.000.000 higher than the classes and the b) line (8.036.067) implies about "
            "6.030.000. (iii) 1918 `manufactures` import, Étranger 63.477.415 (all editions): the b) line "
            "(112.551.419) less France-Algérie gives 63.747.417 and the Récapitulation 63.747.415 (transposed "
            "digits). (iv) 1920 `manufactures` import, France-Algérie: sgt1922 prints 241.075.431, which agrees "
            "with the Récapitulation and the b) line; sgt1923 and sgt1924 print 241.507.431 (a reprint error, "
            "432.000 too high); the stored value comes from sgt1924 under rule 4 and carries the flag, the "
            "correct figure being the sgt1922 printing. (v) 1923 `manufactures` import (sgt1923, sgt1924): "
            "France-Algérie 452.548.838, 6.000.000 below the Récapitulation and the b) line (implying "
            "458.548.838), and Étranger 95.088.696, 90 above what the Récapitulation and the b) line imply.",
            "Explanation of the other failed checks (every cell re-read on a native-resolution crop): 1918 "
            "(all editions) a residual of 3.000 on `animal` import and of 2 between `mineral` and `manufactures` "
            "import against the b) lines, part of misprints (ii)-(iii), whose exact correct figures the totals do "
            "not fix. 1918 Étranger TOTAL: sgt1922 prints 171.239.679 (= Récapitulation import + export), "
            "sgt1923-1924 171.239.697 (reprint transposition; totals not stored). 1924 (sgt1924): the "
            "Récapitulation (676.369.187 + 251.574.695 import, 294.041.360 + 288.312.185 export) agrees exactly "
            "with table a) and the c) TOTAUX, but the class cells exceed it by 10 (France-Algérie import), "
            "199.910 (Étranger import) and fall 4 short (Étranger export); the France-Algérie TOTAL 970.408.547 "
            "is 2.000 below its Récapitulation. The 1924 b) class lines are themselves inconsistent with table "
            "a) (see `commerce_trade_by_class`); the c) categories of the same edition agree with these cells on "
            "`animal` export (54.347.670) and come close on `manufactures` (import 604.302.406 against 604.302.386, "
            "export 44.630.178 against 44.640.178), so the faulty cells cannot be identified; nothing is flagged. "
            "sgt1925 reprints 1924.",
            "Survey of the whole chapter: `commerce_survey.md`.",
        ]
        write_notes(T_ORG, CHAPTER, SCRIPT, kept, cols, ORG_DOC,
                    "Renseignements généraux : classement des produits par pays de provenance et de destination "
                    "(valeur en francs)",
                    "General information: products by country group of provenance and destination (value in "
                    "francs)",
                    paras, CHK.n[T_ORG], fails, compared, diffs, coverage_lines(used),
                    RULE4.replace("from the latest edition printing it", "from the latest edition printing it "
                                  "legibly"),
                    "Unit: francs (current values). value_type: francs.")
    return res


# ----------------------------------------------------------------- e) relations commerciales par pays

T_CTY = "commerce_trade_by_country"
# row code -> (English name, name as printed)
COUNTRY = {
    "france": ("France", "France"), "algeria": ("Algeria", "Algérie"), "england": ("England", "Angleterre"),
    "italy": ("Italy", "Italie"), "tripoli": ("Tripoli (Libya)", "Tripoli"), "spain": ("Spain", "Espagne"),
    "malta": ("Malta", "Malte"), "usa": ("United States", "Etats-Unis (Amérique)"), "egypt": ("Egypt", "Egypte"),
    "morocco": ("Morocco", "Maroc"), "greece": ("Greece", "Grèce"), "portugal": ("Portugal", "Portugal"),
    "switzerland": ("Switzerland", "Suisse"), "brazil": ("Brazil", "Brésil"), "china": ("China", "Chine"),
    "india": ("India: British settlements", "Indes : Comptoirs Anglais"), "netherlands": ("Netherlands", "Hollande"),
    "bulgaria": ("Bulgaria", "Bulgarie"), "sweden": ("Sweden", "Suède"), "norway": ("Norway", "Norvège"),
    "austria": ("Austria", "Autriche"), "germany": ("Germany", "Allemagne"), "russia": ("Russia", "Russie"),
    "turkey": ("Turkey", "Turquie"), "denmark": ("Denmark", "Danemark"), "belgium": ("Belgium", "Belgique"),
    "japan": ("Japan", "Japon"), "romania": ("Romania", "Roumanie"), "other": ("Other countries", "Autres pays"),
}


def build_country(secs, write):
    recs, used = [], []
    avg_fail = []
    for ed in EDITIONS_DONE:
        es = [s for s in secs if s["table"] == "by_country" and s["ed"] == ed]
        if not es:
            continue
        cells, wh = defaultdict(dict), {}
        for s in es:
            used.append(s)
            for lab, cs in rows_of(s).items():
                for c in s["cols"]:
                    cells[c][lab] = cs[c].value
                    wh[c] = where(s)
                    if c.startswith("A") or lab.startswith("Total"):
                        continue
                    k, f = lab.split(".")
                    cell = cs[c]
                    recs.append({"census": ed, "table_id": "general_e", "gallica_ark": s["ark"],
                                 "source_page": s["page"], "gallica_view": s["view"], "year": int(c),
                                 "country": COUNTRY[k][0], "country_fr": COUNTRY[k][1], "country_code": k,
                                 "flow": f, "flow_fr": FLOW[f], "measure": "value", "measure_fr": "valeur",
                                 "unit": "francs", "value": cell.value,
                                 "flag": cell.flag or ("total_mismatch" if (ed, lab, c) in CTY_MISPRINTS else "")})
        years = [c for c in cells if not c.startswith("A")]
        for c in sorted(years):
            for f in FLOW:
                CHK.eq(T_CTY, f"{wh[c]} {c}: sum of countries, {f} = TOTAUX {f}",
                       ssum(cells[c][f"{k}.{f}"] for k in COUNTRY), cells[c][f"Total.{f}"])
        for c in sorted(c for c in cells if c.startswith("A")):
            y0, y1 = map(int, c[1:].split("-"))
            for lab in cells[c]:
                vals = [cells[str(y)].get(lab) for y in range(y0, y1 + 1)]
                tot = ssum(vals)
                n0 = len(CHK.fail[T_CTY])
                CHK.eq(T_CTY, f"{wh[c]} average {y0}-{y1} {lab}: printed average x {y1 - y0 + 1} = sum of years",
                       tot, None if cells[c][lab] is None else cells[c][lab] * (y1 - y0 + 1),
                       tol=Decimal(y1 - y0 + 1))
                if len(CHK.fail[T_CTY]) > n0:
                    avg_fail.append((ed, y0, y1, lab))
    key = ["year", "country_code", "flow"]
    kept, compared, diffs, n_ill = select_legible(recs, key)
    order = list(COUNTRY)
    kept.sort(key=lambda r: (r["year"], order.index(r["country_code"]), r["flow"]))
    # an average failure is 'corroborated' when every year of its window was printed identically by every
    # edition that printed it legibly (two or three independent printings, each read on its own image)
    printed = defaultdict(set)
    for r in recs:
        if r["value"] is not None:
            printed[(r["year"], r["country_code"], r["flow"])].add(r["value"])
    fails = CHK.fail[T_CTY]
    flagged = [f"{r['census']} {r['year']} {r['country_code']} {r['flow']}" for r in kept if r["flag"]]
    res = dict(rows=len(kept), checks=CHK.n[T_CTY], failed=list(fails), overlap_compared=compared,
               overlap_diffs=[list(d) for d in diffs], flagged=flagged, editions=EDITIONS_DONE,
               value_type="francs", illegible_printings_not_compared=n_ill)
    if write:
        cols = COMMON + CTY_DIMS + ["value", "flag"]
        write_csv(T_CTY, cols, kept)
        write_notes(T_CTY, CHAPTER, SCRIPT, kept, cols, CTY_DOC,
                    "Renseignements généraux : résumé des relations commerciales avec les différents pays "
                    "(valeur en francs)",
                    "General information: trade with the different countries (value in francs)",
                    CTY_PARAS + ["Survey of the whole chapter: `commerce_survey.md`."],
                    CHK.n[T_CTY], fails, compared, diffs, coverage_lines(used),
                    RULE4.replace("from the latest edition printing it", "from the latest edition printing it "
                                  "legibly"),
                    "Unit: francs (current values; see the valuation footnote in `commerce_trade_by_class`). "
                    "value_type: francs.")
    return res


CTY_DIMS = ["country", "country_fr", "country_code", "flow", "flow_fr", "measure", "measure_fr", "unit"]
CTY_DOC = dict(DOC, table_id="`general_e` (Renseignements généraux, e) Résumé des relations commerciales avec les "
                             "différents pays)",
               census=CAT_DOC["census"],
               country="country of provenance (imports) or destination (exports), English",
               country_fr="country as printed",
               country_code="short code of the country line (`other` = Autres pays)",
               flag="empty or `total_mismatch` (see notes)")
# Misprints located by two independent printed averages and the TOTAUX gap; printed value kept, flagged.
CTY_MISPRINTS = {("sgt1924", "tripoli.export", "1924"), ("sgt1924", "egypt.import", "1924")}
CTY_PARAS = [
    "The table prints, for 28 named countries and *Autres pays*, the value of imports from and exports to each "
    "country for the last ten years, then (odd view) three printed averages (*Moyenne des années*: two five-year "
    "and one ten-year) and a TOTAUX line per flow. Averages and TOTAUX are not stored; they were used as checks "
    "(sum of countries = TOTAUX; printed average x number of years = sum of the cells, tolerance one franc per "
    "year for rounding). The TOTAUX agree with the TOTAUX of table c) (`commerce_trade_by_category`) wherever both are legible. "
    "Printed » is stored as 0. Country names are those printed; *Tripoli* is Ottoman, then Italian Tripolitania; "
    "*Indes : Comptoirs Anglais* = British India.",
    "Gutter. The fourth year of each even view lies against the binding. sgt1922: the 1916 column loses its "
    "last digit on most lines (`?`; f290 legible on 10 lines, f292 only on lines printed »), and on f293 the "
    "1917 export TOTAUX loses a middle digit. sgt1923: the 1917 column of f782 loses the last digit on 6 lines "
    "(`?`), and the 1918 column (f781, f783) loses leading digits on the larger values (`?`, a value kept only "
    "when its first digit is wholly visible). sgt1924 is legible throughout. A year is stored from the latest "
    "edition printing it legibly; illegible printings are not compared. sgt1922 f293 `other` export 1921: the "
    "last digit is damaged type (3 or 5), transcribed `?`; sgt1923 and sgt1924 print 6.910.483.",
    "Every overlapping cell agrees between the editions (each printing typed from its own image). The TOTAUX "
    "failures are therefore in the printed table itself and recur in every edition printing the year: "
    "1918 import (sum of countries 430 below TOTAUX), 1919 export (600.002 below), 1920 import (667.684 below), "
    "1921 import (300 below), 1922 import (687.602 below) and export (618.940 above), 1923 import (2.999.990 "
    "above) and export (498 above). Every cell of those columns was re-read on native-resolution crops; the "
    "printed averages locate no single cell consistently (for 1923 the sgt1923 1919-1923 averages of `usa`, "
    "`egypt` and `turkey` import would explain the 3 million, but the sgt1924 1920-1924 averages agree with the "
    "printed 1923 cells), so nothing is flagged. sgt1922 1917 export: the TOTAUX is in the gutter (`?`); sgt1923 "
    "and sgt1924 print 125.672.079 and the check passes there.",
    "1924 (sgt1924 only): the countries exceed TOTAUX import by 906 and fall 23.736 short of TOTAUX export. "
    "Both printed averages containing 1924 (1920-1924 and 1915-1924) imply 10.121.094 for `tripoli` export "
    "(printed 10.101.094, re-read on a zoomed crop) and 401 less than the printed 1.364.829 for `egypt` import; "
    "both corrections go in the direction of the TOTAUX gap, so these two cells are flagged `total_mismatch` "
    "(printed value kept). The residuals (3.736 export, 505 import) are not located. sgt1925 reprints 1924.",
    "Failed average checks (averages are not stored and were never used to change a cell). Every year of every "
    "failing average window is printed identically by two or three editions, except the 1924 cells discussed "
    "above, so the failures are misprinted or miscomputed averages: (i) round-number slips in one average only "
    "(e.g. sgt1922 `algeria` export 1913-1922, 1.000.000; sgt1923 `turkey` export 1914-1923, 300.000, `russia` "
    "export 1919-1923, 20.000; sgt1924 `usa` import 1915-1919, 10.000.000, `france` export 1915-1924, 50.000.000, "
    "`belgium` export 1915-1924, 7.000.000, `morocco` export, `india` and `romania` import 1920-1924 and "
    "1915-1924, 500.000; TOTAUX import 1915-1919 and 1915-1924, 5.000.000); (ii) small differences of a few "
    "francs to a few thousand francs (rounding or copying slips); (iii) averages computed on a different "
    "state of the figures: sgt1922 `switzerland` export 1918-1922 and 1913-1922 omit the 1922 value (308.315, "
    "confirmed by sgt1923-1924 and the sgt1923 1919-1923 average), `china` export omits 1921 (32); sgt1924 "
    "`usa` export 1920-1924 and 1915-1924 omit 1924 (7.187.353); sgt1924 `bulgaria` import 1920-1924 repeats "
    "the sgt1923 1919-1923 average (172.237) and `russia` export prints the 1915-1919 average (27.432) in the "
    "1920-1924 column. (iv) sgt1922 `algeria` import 1918-1922 and 1913-1922 both imply 11.560.684 for 1918 "
    "(printed 11.650.684 in sgt1922 and sgt1924, a possible transposition), but correcting it would widen the "
    "1918 TOTAUX gap, so the cell is not flagged.",
]


# ----------------------------------------------------------------- f) droits de douane perçus (importation)

T_CUS = "commerce_customs_duties"
# row code -> (product class, line as printed); the c) categories, with Denrées coloniales split into Sucres /
# Autres, Poteries / Verres et cristaux and Meubles / Ouvrages en bois printed on separate lines
DUTY_ROWS = dict(
    [(k, v) for k, v in CATEGORY.items() if list(CATEGORY).index(k) < list(CATEGORY).index("colonial_goods")]
    + [("colonial_sugar", ("vegetal", "Denrées coloniales de consommation : Sucres")),
       ("colonial_other", ("vegetal", "Denrées coloniales de consommation : Autres"))]
    + [(k, v) for k, v in CATEGORY.items()
       if list(CATEGORY).index("colonial_goods") < list(CATEGORY).index(k) < list(CATEGORY).index("pottery_glass")]
    + [("pottery", ("manufactures", "Poteries")), ("glass", ("manufactures", "Verres et cristaux"))]
    + [(k, v) for k, v in CATEGORY.items()
       if list(CATEGORY).index("pottery_glass") < list(CATEGORY).index(k) < list(CATEGORY).index("furniture")]
    + [("furniture", ("manufactures", "Meubles")), ("wood_goods", ("manufactures", "Ouvrages en bois"))]
    + [(k, v) for k, v in CATEGORY.items() if list(CATEGORY).index(k) > list(CATEGORY).index("furniture")])
DUTY_ROWS["paper"] = ("manufactures", "Papiers et ses applications")
# reprint differences judged on the totals: the later printing is the corrected one
CUS_REPRINT = {("1923", "live_animals"): "sgt1923 prints 33.773, sgt1924 23.773"}
CUS_DIMS = ["product_class", "product_class_fr", "product_category", "product_category_fr", "measure", "measure_fr",
            "unit"]
CUS_DOC = dict(DOC, table_id="`general_f` (Renseignements généraux, f) Droits de douane perçus, importation)",
               census=CAT_DOC["census"],
               year="calendar year in which the duties were collected",
               product_category="code of the line (customs nomenclature category; see notes)",
               product_category_fr="line as printed",
               measure="`import_duties`", measure_fr="droits de douane perçus (importation)",
               value="duties collected, francs with centimes, as printed",
               flag="empty, `reprint_corrected` (see notes)")


def build_customs(secs, write):
    recs, used = [], []
    for s in secs:
        if s["table"] != "customs_duties":
            continue
        used.append(s)
        R = rows_of(s)
        for c in s["cols"]:
            CHK.eq(T_CUS, f"{where(s)} {c}: sum of lines = TOTAL", ssum(R[k][c].value for k in DUTY_ROWS),
                   R["Total"][c].value)
            for k, (cl, fr) in DUTY_ROWS.items():
                cell = R[k][c]
                recs.append({"census": s["ed"], "table_id": "general_f", "gallica_ark": s["ark"],
                             "source_page": s["page"], "gallica_view": s["view"], "year": int(c),
                             "product_class": cl, "product_class_fr": PRODUCT_CLASS[cl], "product_category": k,
                             "product_category_fr": fr, "measure": "import_duties",
                             "measure_fr": "droits de douane perçus (importation)", "unit": "francs",
                             "value": cell.value, "flag": cell.flag})
    kept, compared, diffs, n_ill = select_legible(recs, ["year", "product_category"])
    for r in kept:
        if (str(r["year"]), r["product_category"]) in CUS_REPRINT and not r["flag"]:
            r["flag"] = "reprint_corrected"
    order = list(DUTY_ROWS)
    kept.sort(key=lambda r: (r["year"], order.index(r["product_category"])))
    fails = CHK.fail[T_CUS]
    flagged = [f"{r['census']} {r['year']} {r['product_category']}" for r in kept if r["flag"]]
    res = dict(rows=len(kept), checks=CHK.n[T_CUS], failed=list(fails), overlap_compared=compared,
               overlap_diffs=[list(d) for d in diffs], flagged=flagged, editions=EDITIONS_DONE,
               value_type="francs", illegible_printings_not_compared=n_ill)
    if write:
        cols = COMMON + CUS_DIMS + ["value", "flag"]
        write_csv(T_CUS, cols, kept)
        paras = [
            "Import duties collected (droits de douane perçus, importation) by line of the customs nomenclature: "
            "the 32 categories of table c) (`commerce_trade_by_category`), with *Denrées coloniales* split into "
            "Sucres and Autres, *Poteries* and *Verres et cristaux*, *Meubles* and *Ouvrages en bois* printed "
            "on separate lines (35 lines). Francs with centimes; printed » stored as 0. The printed TOTAL and the "
            "three averages (*Moyenne des années*) are not stored; the TOTAL was used as a check (sum of lines). "
            "Total duties by year = sum of the stored rows.",
            "Gutter: sgt1922 f295, the 1917 column loses its leading digits on Sucres, Autres, Tissus and the "
            "TOTAL, and on f294 the last digit of the 1916 TOTAL and of *Produits et déchets divers* (`?`); "
            "sgt1923 f785, the 1918 column is cut on every line except six short values (`?`). A year is stored "
            f"from the latest edition printing it legibly ({n_ill} illegible printed cells, not compared). "
            "sgt1924 prints every year legibly.",
            "Reprint difference: 1923 *Animaux vivants*, sgt1923 prints 33.773 and sgt1924 23.773 (both read on "
            "zoomed crops); the sgt1924 figure reduces the 1923 TOTAL gap and is stored (flag "
            "`reprint_corrected`).",
            "Explanation of the failed checks (every cell of the failing columns re-read on native-resolution "
            "crops; the same figures in every edition printing the year): 1918, the lines sum to 20.00 less than "
            "the TOTAL (6.181.022,80; sgt1922 and sgt1924); 1922, 0.06 less than the TOTAL (17.637.371,81; all "
            "three editions); neither is located. 1923: sgt1923 lines exceed the TOTAL (24.371.783,13) by "
            "19.005, sgt1924 (with Animaux vivants 23.773) by 9.005. The sgt1924 1920-1924 printed averages agree "
            "with the printed 1923 lines (within rounding) and the TOTAL average equals the mean of the printed "
            "TOTALs, so the residual 9.005 cannot be assigned to a line; nothing flagged.",
            "Survey of the whole chapter: `commerce_survey.md`.",
        ]
        write_notes(T_CUS, CHAPTER, SCRIPT, kept, cols, CUS_DOC,
                    "Renseignements généraux : droits de douane perçus (importation)",
                    "General information: import duties collected, by category of products",
                    paras, CHK.n[T_CUS], fails, compared, diffs, coverage_lines(used),
                    RULE4.replace("from the latest edition printing it", "from the latest edition printing it "
                                  "legibly"),
                    "Unit: francs with centimes (current values). value_type: francs.")
    return res


# ----------------------------------------------------------------- droits de sortie perçus (exportation)

T_EXP = "commerce_export_duties"
# row code -> (group as printed or '', line as printed); sgt1924-only lines marked in EXPORT_NEW_1924
EXPORT_ROWS = {
    "horses": ("Bêtes de somme exportées à destination de l'étranger", "Chevaux et juments"),
    "foals": ("Bêtes de somme exportées à destination de l'étranger", "Poulains et pouliches"),
    "mules": ("Bêtes de somme exportées à destination de l'étranger", "Mules et mulets"),
    "donkeys": ("Bêtes de somme exportées à destination de l'étranger", "Anes, ânesses et ânons"),
    "camels": ("Bêtes de somme exportées à destination de l'étranger", "Animaux de l'espèce caméline"),
    "hides_large": ("Peaux brutes", "grandes"),
    "hides_sheep": ("Peaux brutes", "de moutons et d'agneaux"),
    "hides_goat": ("Peaux brutes", "de chèvres et de chevreaux"),
    "poultry": ("", "Volailles et pigeons vivants"),
    "salted_meat": ("", "Viandes salées"),
    "canned_meat": ("", "Conserves de viandes en boîte"),
    "eggs": ("", "Œufs de volailles"),
    "butter_cheese": ("", "Beurres et fromages"),
    "condensed_milk": ("", "Lait concentré pur"),
    "octopus": ("", "Poulpes"),
    "fresh_fish": ("", "Poissons frais autres que le thon et la boutargue"),
    "sponges_washed": ("Eponges", "lavées"),
    "sponges_unwashed": ("Eponges", "non lavées"),
    "potatoes": ("", "Pommes de terre"),
    "dried_pulses": ("", "Légumes secs"),
    "fruit_fresh": ("Fruits de table", "frais"),
    "fruit_dried": ("Fruits de table", "secs"),
    "olives_fresh": ("", "Olives fraîches"),
    "condensed_milk_sweet": ("", "Lait concentré sucré"),
    "olive_oil": ("Huiles", "d'olive"),
    "pomace_oil": ("Huiles", "de grignons"),
    "charcoal": ("", "Charbon de bois"),
    "common_wood": ("", "Autres bois communs"),
    "alfa": ("", "Alfa brut"),
    "vegetables_fresh": ("", "Légumes frais"),
    "fodder": ("", "Fourrages"),
    "pomace": ("", "Grignons"),
    "rags": ("", "Chiffons"),
    "cellulose_pulp": ("", "Pâtes de cellulose (pâtes d'alfa et de diss)"),
    "lead_ore": ("", "Minerai de plomb"),
    "lead_metal": ("", "Plomb (métal)"),
    "basketry": ("", "Ouvrages de sparterie (alfa travaillé)"),
    "parcels_sponges": ("Colis postaux", "Eponges"),
    "parcels_olive_oil": ("Colis postaux", "Huiles d'olive"),
    "horse_tax": ("", "Taxes de sortie sur les jeunes chevaux"),
}
EXPORT_LABEL_ED = {("sgt1924", "butter_cheese"): "Beurre, fromages et graisses"}
EXP_DIMS = ["product_group_fr", "product", "product_fr", "measure", "measure_fr", "unit"]
EXP_DOC = dict(DOC, table_id="`export_duties` (Droits de sortie perçus, exportation)",
               census=CAT_DOC["census"],
               year="calendar year in which the duties were collected",
               product_group_fr="group heading as printed (empty when the line stands alone)",
               product="code of the line", product_fr="line as printed (in the edition the value is taken from)",
               measure="`export_duties`", measure_fr="droits de sortie perçus (exportation)",
               value="duties collected, francs with centimes, as printed", flag="empty")


def build_export(secs, write):
    recs, used = [], []
    for s in secs:
        if s["table"] != "export_duties":
            continue
        used.append(s)
        R = rows_of(s)
        lines = [k for k in R if k != "Total"]
        for c in s["cols"]:
            CHK.eq(T_EXP, f"{where(s)} {c}: sum of lines = TOTAL", ssum(R[k][c].value for k in lines),
                   R["Total"][c].value)
            for k in lines:
                g, fr = EXPORT_ROWS[k]
                cell = R[k][c]
                recs.append({"census": s["ed"], "table_id": "export_duties", "gallica_ark": s["ark"],
                             "source_page": s["page"], "gallica_view": s["view"], "year": int(c),
                             "product_group_fr": g, "product": k,
                             "product_fr": EXPORT_LABEL_ED.get((s["ed"], k), fr), "measure": "export_duties",
                             "measure_fr": "droits de sortie perçus (exportation)", "unit": "francs",
                             "value": cell.value, "flag": cell.flag})
    kept, compared, diffs, n_ill = select_legible(recs, ["year", "product"])
    order = list(EXPORT_ROWS)
    kept.sort(key=lambda r: (r["year"], order.index(r["product"])))
    fails = CHK.fail[T_EXP]
    flagged = [f"{r['census']} {r['year']} {r['product']}" for r in kept if r["flag"]]
    res = dict(rows=len(kept), checks=CHK.n[T_EXP], failed=list(fails), overlap_compared=compared,
               overlap_diffs=[list(d) for d in diffs], flagged=flagged, editions=EDITIONS_DONE,
               value_type="francs", illegible_printings_not_compared=n_ill)
    if write:
        cols = COMMON + EXP_DIMS + ["value", "flag"]
        write_csv(T_EXP, cols, kept)
        paras = [
            "Export duties collected (droits de sortie perçus, exportation) by product line, including the "
            "duties on parcel post (Colis postaux) and the exit tax on young horses. Francs with centimes; "
            "printed » stored as 0. The TOTAL and the three averages (*Moyenne des années*) are not stored; the "
            "TOTAL was used as a check. Total export duties by year = sum of the stored rows.",
            "Lines: sgt1922 and sgt1923 print 26 lines; sgt1924 prints 40, adding 14 lines (poultry, salted and "
            "canned meat, eggs, condensed milk pure and sweetened, potatoes, pulses, fresh and dried fruit, "
            "charcoal, other common wood, fresh vegetables, fodder) that are » in every year before 1924, and "
            "renames *Beurres et fromages* to *Beurre, fromages et graisses*. Under rule 4 every year 1915-1924 "
            "comes from sgt1924, so the added lines carry 0 (as printed) for 1915-1923; 1913 and 1914 have only "
            "the 26 lines (the added lines are absent, not zero). The animal lines refer to the decrees of 12 June "
            "and 28 August 1920 (duties on beasts of burden exported to foreign countries).",
            "Gutter: sgt1922 f296, the last digits of the 1916 TOTAL (`?`); sgt1923 f786, the 1917 column loses "
            "its centimes on every non-zero line (`?`), and f787 the 1918 column loses leading digits on five "
            f"lines and the TOTAL (`?`). Illegible printings ({n_ill} cells) are not compared; sgt1924 is legible "
            "throughout.",
            "Explanation of the failed checks (cells re-read on native-resolution crops; the same figures in every "
            "edition printing the year): 1918, the lines exceed the TOTAL (707.645,24) by 0,05; 1922, they fall "
            "3,00 short of the TOTAL (3.412.803,27); neither is located. 1924 (sgt1924 only): the lines sum to "
            "2.056.475,22 against a TOTAL of 2.056.675,96 (200,74 short); the printed 1920-1924 averages are "
            "themselves inconsistent on several lines (e.g. camels, large hides, dried fruit, fodder) and do not "
            "locate the gap; nothing flagged. sgt1925 reprints 1924.",
            "Survey of the whole chapter: `commerce_survey.md`.",
        ]
        write_notes(T_EXP, CHAPTER, SCRIPT, kept, cols, EXP_DOC, "Droits de sortie perçus (exportation)",
                    "Export duties collected, by product", paras, CHK.n[T_EXP], fails, compared, diffs,
                    coverage_lines(used),
                    RULE4.replace("from the latest edition printing it", "from the latest edition printing it "
                                  "legibly"),
                    "Unit: francs with centimes (current values). value_type: francs.")
    return res


# ----------------------------------------------------------------- Navigation, mouvement des navires

MOVEMENT = {"E": ("entries", "Entrées"), "S": ("exits", "Sorties")}
NAV_MEASURE = {"ships": ("Nombre de navires", "ships"), "tonnage": ("Tonneaux de jauge", "tons register"),
               "goods": ("Tonnes de marchandises", "tonnes"), "passengers": ("Passagers", "persons"),
               "livestock": ("Têtes de bétail", "head")}
T_PORT = "commerce_navigation_by_port"
# cells checked on the crops and found misprinted (row and column checks both point to them): flagged
NAV_MISPRINTS = {
    ("sgt1922", "Tunis-Goulette", "S.tonnage"): "printed 1.454.848; entries + exits = combined and the column "
    "TOTAUX both give 1.434.848",
    ("sgt1923", "Tabarka", "S.goods"): "printed 9.550; the combined line and the column TOTAUX both give 9.553",
    ("sgt1924", "Sfax", "S.tonnage"): "printed 353.802; the combined line and the column TOTAUX both give 953.802",
    ("sgt1924", "Bizerte", "E.passengers"): "printed 3.303; the combined line and the column TOTAUX both give "
    "8.303",
}
NAV_DOC = dict(DOC, census="edition (each edition prints one year, its reference year)",
               table_id="`navigation_a` (Mouvement des navires, a) Par port)",
               year="year of the movement (not printed in the heading; the reference year of the edition, "
                    "confirmed by c) sur le littoral)",
               port="port as printed", movement="`entries` or `exits`", movement_fr="as printed",
               measure="`ships`, `tonnage`, `goods`, `passengers`, `livestock`", measure_fr="column as printed",
               unit="`ships`, `tons register` (tonneaux de jauge), `tonnes`, `persons`, `head`",
               value="as printed (» stored as 0)", flag="empty or `total_mismatch` (see notes)")


def nav_matrix(secs, table, ed):
    M = defaultdict(dict)
    used = []
    for s in secs:
        if s["table"] == table and s["ed"] == ed:
            used.append(s)
            for r in s["rows"]:
                for c, cell in r["cells"].items():
                    M[r["label"]][c] = (cell, s)
    return M, used


def nav_checks(topic, M, ed, label_of=lambda l: l, total="Totaux"):
    lines = [l for l in M if l != total]
    for m in NAV_MEASURE:
        for mv in ("E", "S", "R"):
            c = f"{mv}.{m}"
            if c in M[total]:
                CHK.eq(topic, f"{ed} {c}: sum of lines = {total}", ssum(M[l][c][0].value for l in lines),
                       M[total][c][0].value)
        for l in M:
            if f"R.{m}" in M[l]:
                CHK.eq(topic, f"{ed} {label_of(l)} {m}: entries + exits = combined",
                       ssum([M[l][f"E.{m}"][0].value, M[l][f"S.{m}"][0].value]), M[l][f"R.{m}"][0].value)


def nav_records(M, ed, table_id, dims_of, total="Totaux"):
    out = []
    for l, cs in M.items():
        if l == total:
            continue
        for c, (cell, s) in cs.items():
            mv, m = c.split(".")
            if mv == "R":
                continue
            flag = cell.flag or ("total_mismatch" if (ed, l, c) in NAV_MISPRINTS else "")
            out.append(dict({"census": ed, "table_id": table_id, "gallica_ark": s["ark"], "source_page": s["page"],
                             "gallica_view": s["view"], "year": int(s["year"])}, **dims_of(l),
                            movement=MOVEMENT[mv][0], movement_fr=MOVEMENT[mv][1], measure=m,
                            measure_fr=NAV_MEASURE[m][0], unit=NAV_MEASURE[m][1], value=cell.value, flag=flag))
    return out


def build_nav_port(secs, write):
    recs, used = [], []
    for ed in EDITIONS_DONE:
        M, u = nav_matrix(secs, "nav_port", ed)
        used += u
        nav_checks(T_PORT, M, ed)
        recs += nav_records(M, ed, "navigation_a", lambda l: {"port": l})
    kept, compared, diffs = select_latest(recs, ["year", "port", "movement", "measure"])
    fails = CHK.fail[T_PORT]
    flagged = [f"{r['census']} {r['port']} {r['movement']} {r['measure']}" for r in kept if r["flag"]]
    res = dict(rows=len(kept), checks=CHK.n[T_PORT], failed=list(fails), overlap_compared=compared,
               overlap_diffs=[list(d) for d in diffs], flagged=flagged, editions=EDITIONS_DONE, value_type="count")
    if write:
        cols = COMMON + ["port", "movement", "movement_fr", "measure", "measure_fr", "unit", "value", "flag"]
        paras = [
            "Movement of ships by port (21 ports, printed in order of importance, which changes from one edition "
            "to the next): ships, register tonnage, tonnes of goods, passengers and head of livestock, entries and "
            "exits. The printed *Entrées et sorties réunies* block and the TOTAUX line are not stored; they were "
            "used as checks (entries + exits = combined on every line and measure; lines = TOTAUX).",
            "Year: the heading prints no year. Each edition prints the movement of its reference year (sgt1922: "
            "1922, sgt1923: 1923, sgt1924: 1924); the TOTAUX of entries agree with the yearly series c) *sur le "
            "littoral* of the same edition (see `commerce_navigation_yearly`). The editions do not overlap.",
            "Gutter: the entries livestock column (Têtes de bétail) lies against the binding on the left page "
            "(repeated, cut, at the edge of the right page in sgt1923 and sgt1924); every cell was read on the "
            "crop and equals combined minus exits. sgt1922: the exits ships TOTAUX is partly hidden (`?` in the "
            "transcription; check only).",
            "Explanation of the failed checks (each cell re-read on a zoomed native-resolution crop; in every case "
            "the line check and the column check fail by the same amount, which locates the misprint, flagged "
            "`total_mismatch`): "
            + "; ".join(f"{e} {l} {c}: {n}" for (e, l, c), n in NAV_MISPRINTS.items()) + ".",
            "Survey of the whole chapter: `commerce_survey.md`.",
        ]
        write_csv(T_PORT, cols, kept)
        write_notes(T_PORT, CHAPTER, SCRIPT, kept, cols, NAV_DOC, "Navigation : mouvement des navires, a) par port",
                    "Navigation: movement of ships, by port", paras, CHK.n[T_PORT], fails, compared, diffs,
                    coverage_lines(used), "Selection: each edition prints a single year; no overlap.",
                    "Units: as printed (ships, tonneaux de jauge, tonnes, passengers, head). value_type: count.")
    return res


T_FLAG = "commerce_navigation_by_flag"
SHIP_FLAG = {"Français": "france", "Italien": "italy", "Anglais": "united_kingdom", "Espagnol": "spain",
             "Yougo-Slave": "yugoslavia", "Grec": "greece", "Danois": "denmark", "Norvégien": "norway",
             "Tunisien": "tunisia", "Hollandais": "netherlands", "Américain": "united_states", "Belge": "belgium",
             "Portugais": "portugal", "Allemand": "germany", "Suédois": "sweden", "Russe": "russia",
             "Japonais": "japan", "Péruvien": "peru", "Egyptien": "egypt", "Marocain": "morocco",
             "Dantzikois": "danzig", "Esthonien": "estonia", "Roumain": "romania", "Canadien": "canada",
             "Finlandais": "finland", "Bulgare": "bulgaria", "Turc": "turkey", "Panama": "panama",
             "Argentin": "argentina", "Persan": "persia"}
PROPULSION = {"vapeurs": "steam", "voiliers": "sail", "mixtes": "mixed"}
FLAG_MISPRINTS = {
    ("sgt1922", "Italien.mixtes", "E.tonnage"): "printed 8.534; combined - exits and the column TOTAUX give 6.534",
    ("sgt1922", "Italien.voiliers", "S.passengers"): "printed 667; combined - entries gives 657 (column TOTAUX "
    "agrees with the next two corrections)",
    ("sgt1922", "Tunisien.voiliers", "S.passengers"): "printed 3.452; combined - entries gives 8.452 (with the "
    "previous cell the column TOTAUX 68.349 is reached)",
    ("sgt1922", "Yougo-Slave.vapeurs", "S.tonnage"): "printed 58.216; combined - entries and the column TOTAUX "
    "give 68.216",
    ("sgt1922", "Suédois.vapeurs", "S.goods"): "printed 14.184; combined - entries gives 14.180",
    ("sgt1922", "Japonais.vapeurs", "S.goods"): "printed 14.726; combined - entries gives 14.720 (with the "
    "previous cell the column TOTAUX 3.015.888 is reached)",
}
NAV_MISPRINTS.update(FLAG_MISPRINTS)
FLAG_DOC = dict(NAV_DOC, table_id="`navigation_b` (Mouvement des navires, b) Par pavillons)",
                ship_flag="flag (nationality) of the ships, English code", ship_flag_fr="pavillon as printed",
                propulsion="`steam`, `sail`, `mixed`", propulsion_fr="vapeurs, voiliers, mixtes (as printed)")


def build_nav_flag(secs, write):
    recs, used = [], []

    def dims(l):
        f, p = l.split(".")
        return {"ship_flag": SHIP_FLAG[f], "ship_flag_fr": f, "propulsion": PROPULSION[p], "propulsion_fr": p}
    for ed in EDITIONS_DONE:
        M, u = nav_matrix(secs, "nav_flag", ed)
        used += u
        nav_checks(T_FLAG, M, ed)
        recs += nav_records(M, ed, "navigation_b", dims)
        # the two tables a) and b) share their TOTAUX
        P, _ = nav_matrix(secs, "nav_port", ed)
        for c in M["Totaux"]:
            if c in P["Totaux"]:
                CHK.eq(T_FLAG, f"{ed} {c}: TOTAUX by flag = TOTAUX by port", P["Totaux"][c][0].value,
                       M["Totaux"][c][0].value)
    kept, compared, diffs = select_latest(recs, ["year", "ship_flag", "propulsion", "movement", "measure"])
    fails = CHK.fail[T_FLAG]
    flagged = [f"{r['census']} {r['ship_flag']} {r['propulsion']} {r['movement']} {r['measure']}"
               for r in kept if r["flag"]]
    res = dict(rows=len(kept), checks=CHK.n[T_FLAG], failed=list(fails), overlap_compared=compared,
               overlap_diffs=[list(d) for d in diffs], flagged=flagged, editions=EDITIONS_DONE, value_type="count")
    if write:
        cols = COMMON + ["ship_flag", "ship_flag_fr", "propulsion", "propulsion_fr", "movement", "movement_fr",
                         "measure", "measure_fr", "unit", "value", "flag"]
        paras = [
            "Movement of ships by flag (pavillon, in order of importance) and propulsion (vapeurs = steam, "
            "voiliers = sail, mixtes = mixed): ships, register tonnage, tonnes of goods, passengers, head of "
            "livestock, entries and exits. Only the flag / propulsion lines printed are stored (27 lines in "
            "sgt1922, 35 in sgt1923, 36 in sgt1924; a line printed with » throughout, e.g. Canadien entries 1924, "
            "is stored as 0). The *Entrées et sorties réunies* block and the TOTAUX are checks only; the TOTAUX "
            "are also compared with those of a) par port.",
            "Year: not printed; the reference year of each edition (1922, 1923, 1924), as for a) par port. No "
            "overlap between editions.",
            "Gutter: the entries livestock column lies against the binding; every cell read on the crop and equal "
            "to combined minus exits.",
            "Explanation of the failed checks (every cell re-read on a zoomed native-resolution crop): "
            "(i) sgt1922 prints 9.092 as the entries ships TOTAUX, against 9.062 for the sum of the lines, the "
            "TOTAUX of a) par port and combined (18.038) - exits (8.976): a misprinted total (not stored). "
            "(ii) sgt1924 prints 3.818.475 as the combined tonnage of French steamers, for 2.818.475 = entries + "
            "exits, and the combined TOTAUX agrees with 2.818.475: a misprint in the combined block (not stored). "
            "(iii) the remaining failures locate six misprinted sgt1922 cells, flagged `total_mismatch`: "
            + "; ".join(f"{l} {c}: {n}" for (e, l, c), n in FLAG_MISPRINTS.items()) + ".",
            "Survey of the whole chapter: `commerce_survey.md`.",
        ]
        write_csv(T_FLAG, cols, kept)
        write_notes(T_FLAG, CHAPTER, SCRIPT, kept, cols, FLAG_DOC,
                    "Navigation : mouvement des navires, b) par pavillons",
                    "Navigation: movement of ships, by flag", paras, CHK.n[T_FLAG], fails, compared, diffs,
                    coverage_lines(used), "Selection: each edition prints a single year; no overlap.",
                    "Units: as printed (ships, tonneaux de jauge, tonnes, passengers, head). value_type: count.")
    return res


T_YR = "commerce_navigation_yearly"
YR_MEASURE = {"ships": ("Navires", "ships"), "goods": ("Marchandises (Tonnes)", "tonnes"),
              "passengers": ("Passagers", "persons")}
YR_DOC = dict(NAV_DOC, census=CAT_DOC["census"],
              table_id="`navigation_c` (Mouvement des navires, c) Sur le littoral ; marchandises et passagers)",
              year="calendar year of the movement", measure="`ships`, `goods`, `passengers`",
              unit="`ships`, `tonnes`, `persons`", value="as printed", flag="empty")


def build_nav_yearly(secs, write):
    recs, used = [], []
    for s in secs:
        if s["table"] != "nav_yearly":
            continue
        used.append(s)
        P, _ = nav_matrix(secs, "nav_port", s["ed"])
        ref = s["years"].split("-")[1]
        for r in s["rows"]:
            for c, cell in r["cells"].items():
                mv, m = c.split(".")
                if r["label"] == ref:
                    CHK.eq(T_YR, f"{where(s)} {ref} {c} = TOTAUX of a) par port", P["Totaux"][c][0].value,
                           cell.value)
                recs.append({"census": s["ed"], "table_id": "navigation_c", "gallica_ark": s["ark"],
                             "source_page": s["page"], "gallica_view": s["view"], "year": int(r["label"]),
                             "movement": MOVEMENT[mv][0], "movement_fr": MOVEMENT[mv][1], "measure": m,
                             "measure_fr": YR_MEASURE[m][0], "unit": YR_MEASURE[m][1], "value": cell.value,
                             "flag": cell.flag})
    kept, compared, diffs = select_latest(recs, ["year", "movement", "measure"])
    kept.sort(key=lambda r: (r["year"], r["movement"], list(YR_MEASURE).index(r["measure"])))
    fails = CHK.fail[T_YR]
    res = dict(rows=len(kept), checks=CHK.n[T_YR], failed=list(fails), overlap_compared=compared,
               overlap_diffs=[list(d) for d in diffs], flagged=[], editions=EDITIONS_DONE, value_type="count")
    if write:
        cols = COMMON + ["movement", "movement_fr", "measure", "measure_fr", "unit", "value", "flag"]
        paras = [
            "Shipping on the Tunisian coast (all ports together), entries and exits: ships, tonnes of goods, "
            "passengers, by calendar year. The last year of each edition was checked against the TOTAUX of a) "
            "*par port* of the same edition (ships, goods and passengers, entries and exits).",
            "Explanation of the failed check and of the overlap difference: sgt1923 prints the 1923 exits of goods "
            "as 3.616.904 tonnes, while its own a) par port and b) par pavillons TOTAUX give 3.626.904; sgt1924 "
            "reprints the year as 3.626.904, which is the value stored (rule 4). Both printings re-read on "
            "native-resolution crops of f922 and f1426.",
            "Survey of the whole chapter: `commerce_survey.md`.",
        ]
        write_csv(T_YR, cols, kept)
        write_notes(T_YR, CHAPTER, SCRIPT, kept, cols, YR_DOC,
                    "Navigation : c) sur le littoral ; marchandises et passagers",
                    "Navigation: shipping on the coast, goods and passengers, by year", paras, CHK.n[T_YR], fails,
                    compared, diffs, coverage_lines(used), RULE4.replace("1915-1924", "1915-1924; every cell "
                    "1915-1923 printed by two or three editions"),
                    "Units: ships, tonnes, passengers, as printed. value_type: count.")
    return res


T_CAB = "commerce_cabotage"
CAB_DIR = {"dispatch": ("d'expédition", "port of dispatch"), "destination": ("de destination",
                                                                             "port of destination")}
CAB_DOC = dict(NAV_DOC, table_id="`navigation_d` (d) Cabotage ; mouvement par port d'expédition et de destination)",
               port="port as printed (*Ports non occupés* = unstaffed ports, as printed)",
               direction="`dispatch` (port d'expédition) or `destination` (port de destination)",
               direction_fr="as printed", measure="`cargo_weight`", measure_fr="poids des cargaisons",
               unit="`quintaux` (quintaux métriques, 100 kg; not converted)", value="as printed (» stored as 0)",
               flag="empty")


def build_cabotage(secs, write):
    recs, used = [], []
    for s in secs:
        if s["table"] != "cabotage":
            continue
        used.append(s)
        check_col_totals(CHK, T_CAB, s)
        for r in s["rows"]:
            if r["label"] == "Totaux":
                continue
            for c, cell in r["cells"].items():
                recs.append({"census": s["ed"], "table_id": "navigation_d", "gallica_ark": s["ark"],
                             "source_page": s["page"], "gallica_view": s["view"], "year": int(s["year"]),
                             "port": r["label"], "direction": c, "direction_fr": CAB_DIR[c][0],
                             "measure": "cargo_weight", "measure_fr": "poids des cargaisons",
                             "unit": "quintaux", "value": cell.value, "flag": cell.flag})
    kept, compared, diffs = select_latest(recs, ["year", "port", "direction"])
    fails = CHK.fail[T_CAB]
    res = dict(rows=len(kept), checks=CHK.n[T_CAB], failed=list(fails), overlap_compared=compared,
               overlap_diffs=[list(d) for d in diffs], flagged=[], editions=EDITIONS_DONE, value_type="quintaux")
    if write:
        cols = COMMON + ["port", "direction", "direction_fr", "measure", "measure_fr", "unit", "value", "flag"]
        paras = [
            "Coastal trade (cabotage): weight of cargoes by port of dispatch and by port of destination, 25 ports "
            "(the same list in the three editions), quintaux métriques. Each cargo is counted once at each end, "
            "so the two TOTAUX are equal; TOTAUX not stored (checked against the lines).",
            "Year: not printed; the reference year of each edition (1922, 1923, 1924), as for a) par port. No "
            "overlap between editions.",
            "Survey of the whole chapter: `commerce_survey.md`.",
        ]
        write_csv(T_CAB, cols, kept)
        write_notes(T_CAB, CHAPTER, SCRIPT, kept, cols, CAB_DOC,
                    "Navigation : d) cabotage ; mouvement par port d'expédition et de destination",
                    "Navigation: coastal trade, by port of dispatch and destination", paras, CHK.n[T_CAB], fails,
                    compared, diffs, coverage_lines(used), "Selection: each edition prints a single year; no "
                    "overlap.", "Unit: quintaux métriques (100 kg), as printed, not converted. value_type: "
                    "quintaux.")
    return res

T_FISH = "commerce_fisheries"
FISH_NAT = {"TN": ("tunisia", "Tunisiens"), "IT": ("italy", "Italiens"), "FR": ("france", "Français"),
            "GR": ("greece", "Grecs"), "AM": ("anglo_maltese", "Anglo-Maltais")}
FISH_MEASURE = {"ships": ("Navires", "boats"), "tonnage": ("Jauge", "tons register"),
                "crew": ("Équipages", "persons"), "foot": ("Pêcheurs à pied", "persons"),
                "kg": ("Produit de la pêche en kilogrammes", "kg"), "francs": ("Produit de la pêche en francs", "francs")}
FISH_DOC = dict(NAV_DOC, table_id="`fisheries` (Pêches maritimes par nationalité et par genre de pêche)",
                fishing_type_fr="genre de pêche as printed",
                ship_flag="nationality of the boats (`tunisia`, `italy`, `france`, `greece`, `anglo_maltese`); "
                          "`all` for foot fishers and the catch, printed for all nationalities together",
                ship_flag_fr="as printed (empty for `all`)",
                measure="`boats`, `tonnage`, `crew`, `foot_fishers`, `catch_weight`, `catch_value`",
                measure_fr="column as printed", unit="`boats`, `tons register`, `persons`, `kg`, `francs`",
                value="as printed (» stored as 0; empty when the francs were not yet received)",
                flag="empty or `not_applicable` (value not yet received, footnote)")
FISH_KEY = {"ships": "boats", "tonnage": "tonnage", "crew": "crew", "foot": "foot_fishers", "kg": "catch_weight",
            "francs": "catch_value"}


def build_fisheries(secs, write):
    recs, used = [], []
    for s in secs:
        if s["table"] != "fisheries":
            continue
        used.append(s)
        check_col_totals(CHK, T_FISH, s)
        for m in ("ships", "tonnage", "crew"):
            check_row(CHK, T_FISH, s, f"R.{m}", [f"{n}.{m}" for n in FISH_NAT])
        for r in s["rows"]:
            if r["label"] == "Totaux":
                continue
            for c, cell in r["cells"].items():
                if c.startswith("R."):
                    continue
                if "." in c:
                    n, m = c.split(".")
                    fl, flfr = FISH_NAT[n]
                else:
                    m, fl, flfr = c, "all", ""
                recs.append({"census": s["ed"], "table_id": "fisheries", "gallica_ark": s["ark"],
                             "source_page": s["page"], "gallica_view": s["view"], "year": int(s["year"]),
                             "fishing_type_fr": r["label"], "ship_flag": fl, "ship_flag_fr": flfr,
                             "measure": FISH_KEY[m], "measure_fr": FISH_MEASURE[m][0], "unit": FISH_MEASURE[m][1],
                             "value": cell.value, "flag": cell.flag})
    kept, compared, diffs = select_latest(recs, ["year", "fishing_type_fr", "ship_flag", "measure"])
    fails = CHK.fail[T_FISH]
    flagged = [f"{r['census']} {r['fishing_type_fr']} {r['measure']}" for r in kept if r["flag"]]
    res = dict(rows=len(kept), checks=CHK.n[T_FISH], failed=list(fails), overlap_compared=compared,
               overlap_diffs=[list(d) for d in diffs], flagged=flagged, editions=EDITIONS_DONE, value_type="count")
    if write:
        cols = COMMON + ["fishing_type_fr", "ship_flag", "ship_flag_fr", "measure", "measure_fr", "unit", "value",
                         "flag"]
        paras = [
            "Sea fisheries by type of fishing and nationality of the boats: boats, register tonnage and crews for "
            "Tunisian, Italian, French, Greek and Anglo-Maltese boats; foot fishers (pêcheurs à pied) and the "
            "catch in kilograms and francs, printed for all nationalities together (`ship_flag` = `all`). The "
            "*Récapitulation* columns and the TOTAUX line are not stored; they were used as checks (nationalities "
            "= récapitulation on every line; lines = TOTAUX).",
            "Types of fishing as printed: sgt1922 prints four lines (Sardines, Anchois, Allaches; Pêches en mer et "
            "dans les lacs; Éponges; Thonaires); sgt1923 and sgt1924 split sea and lake fishing (printed *Pêche en "
            "mer* and *— dans les lacs*, typed *Pêche dans les lacs*). No English translation is attempted.",
            "Year: not printed; the reference year of each edition (1922, 1923, 1924), as for the navigation "
            "tables. No overlap between editions.",
            "Missing values: sgt1922 prints `(1)` for the francs of sea/lake fishing, of the thonaires and of the "
            "total, with the footnote *Au moment de mettre sous presse ces renseignements ne nous sont pas encore "
            "parvenus*: stored empty with `not_applicable`. sgt1923 prints » » for the catch of *Pêche en mer* "
            "(stored 0 as printed, though evidently not reported). sgt1924: the kg of *Pêche en mer* carries the "
            "footnote *A l'exception des ports de : Hammamet, Monastir, Mahdia*.",
            "Gutter: the Greek crews column lies against the binding on the left page; every cell was read on the "
            "native-resolution crop (cut digits repeated at the edge of the right page) and equals the "
            "récapitulation minus the other nationalities.",
            "Survey of the whole chapter: `commerce_survey.md`.",
        ]
        write_csv(T_FISH, cols, kept)
        write_notes(T_FISH, CHAPTER, SCRIPT, kept, cols, FISH_DOC,
                    "Pêches maritimes par nationalité et par genre de pêche",
                    "Sea fisheries, by nationality and type of fishing", paras, CHK.n[T_FISH], fails, compared,
                    diffs, coverage_lines(used), "Selection: each edition prints a single year; no overlap.",
                    "Units: boats, tonneaux de jauge, persons, kg, francs, as printed. value_type: count "
                    "(catch in kg and francs).")
    return res


# ----------------------------------------------------------------- Consommation: animaux abattus

T_SLA = "commerce_slaughter_by_commune"
SLA_SPECIES = {"cattle": "Bœufs ou vaches", "calves": "Veaux", "sheep": "Moutons", "goats": "Chèvres",
               "pigs": "Porcs", "horses": "Chevaux, mulets", "camels": "Chameaux", "other": "Autres"}
SLA_SPECIES_1924 = {"cattle": "Bœufs, vaches", "sheep": "Moutons, agneaux", "goats": "Chèvres, chevreaux"}
SLA_LEFT = ("cattle", "calves", "sheep")  # printed on the even (left) view; the rest on view + 1
# (edition, commune) -> {column: realigned value}; printed values interchanged between two lines
SLA_REALIGN = {("sgt1924", "Tunis"): {"cattle": Decimal(37622)}, ("sgt1924", "Tozeur"): {"cattle": Decimal(228)}}
SLA_NONTOTAL = ("A reporter", "Report", "Totaux")
SLA_DOC = {
    "census": "edition (each prints one year; no overlap)",
    "table_id": "`slaughter` (Consommation : animaux abattus)",
    "gallica_ark": "Gallica volume ark", "source_page": "printed page number", "gallica_view": "Gallica view (fNNNN)",
    "year": "reference year of the edition (not printed: 1922, 1923, 1924)",
    "commune": "commune as printed in that edition",
    "species": "`cattle`, `calves`, `sheep`, `goats`, `pigs`, `horses` (sgt1924 only), `camels`, `other`",
    "species_fr": "column heading as printed",
    "measure": "`animals_slaughtered`", "measure_fr": "animaux abattus", "unit": "`head`",
    "value": "number of animals as printed (» stored as 0); empty when the slaughter dues were farmed out "
             "or not yet instituted",
    "flag": "empty, `not_applicable`, `row_realigned` or `total_mismatch` (see notes)",
}
# cells located as misprints by the row and column totals together: (edition, commune, species) -> note
SLA_MISPRINT = {("sgt1923", "Sfax", "pigs"): "printed 203; the Sfax total and the pigs TOTAUX both need 208"}


def build_slaughter(secs, write):
    recs, used = [], []
    for s in secs:
        if s["table"] != "slaughter":
            continue
        used.append(s)
        ed = s["ed"]
        sp = [c for c in s["cols"] if c != "total"]
        body = [r for r in s["rows"] if r["label"] not in SLA_NONTOTAL]
        realigned = []
        for r in body:
            vals = {c: r["cells"][c].value for c in s["cols"]}
            vals.update(SLA_REALIGN.get((ed, r["label"]), {}))
            realigned.append((r, vals))
            CHK.eq(T_SLA, f"{ed} f{s['view']} {r['label']}: total = sum of species", ssum(vals[c] for c in sp),
                   vals["total"])
        rep = [r for r in s["rows"] if r["label"] == "Report"]
        tot = [r for r in s["rows"] if r["label"] in ("A reporter", "Totaux")][0]
        for c in s["cols"]:
            got = ssum([v[c] for _, v in realigned if v[c] is not None] + [r["cells"][c].value for r in rep])
            CHK.eq(T_SLA, f"{ed} f{s['view']} {tot['label']} {c} = lines" + (" + Report" if rep else ""), got,
                   tot["cells"][c].value)
        for r, vals in realigned:
            for c in sp:
                cell = r["cells"][c]
                flag = cell.flag
                if (ed, r["label"]) in SLA_REALIGN and c in SLA_REALIGN[(ed, r["label"])]:
                    flag = "row_realigned"
                elif (ed, r["label"], c) in SLA_MISPRINT:
                    flag = "total_mismatch"
                fr = SLA_SPECIES_1924.get(c, SLA_SPECIES[c]) if ed == "sgt1924" else SLA_SPECIES[c]
                recs.append({"census": ed, "table_id": "slaughter", "gallica_ark": s["ark"],
                             "source_page": s["page"] + (0 if c in SLA_LEFT else 1),
                             "gallica_view": s["view"] + (0 if c in SLA_LEFT else 1), "year": int(s["year"]),
                             "commune": r["label"], "species": c, "species_fr": fr,
                             "measure": "animals_slaughtered", "measure_fr": "animaux abattus", "unit": "head",
                             "value": vals[c], "flag": flag})
    kept, compared, diffs = select_latest(recs, ["year", "commune", "species"])
    fails = CHK.fail[T_SLA]
    flagged = [f"{r['census']} {r['commune']} {r['species']} {r['flag']}" for r in kept if r["flag"]
               and r["flag"] != "not_applicable"]
    res = dict(rows=len(kept), checks=CHK.n[T_SLA], failed=list(fails), overlap_compared=compared,
               overlap_diffs=[list(d) for d in diffs], flagged=flagged, editions=EDITIONS_DONE, value_type="count")
    if write:
        cols = COMMON + ["commune", "species", "species_fr", "measure", "measure_fr", "unit", "value", "flag"]
        paras = [
            "Animals slaughtered, by commune and species, one year per edition (the reference year, not printed). "
            "The table runs over two spreads (A reporter / Report); the TOTAUX column and line and the A reporter "
            "/ Report lines are not stored, they were used as checks. Footnote (1) in sgt1922 and sgt1923 "
            "(translated): animals slaughtered outside the centres constituted as communes are not included.",
            "Columns: sgt1922 and sgt1923 print seven species (bœufs ou vaches, veaux, moutons, chèvres, porcs, "
            "chameaux, autres); sgt1924 adds *chevaux, mulets* and prints *moutons, agneaux* and *chèvres, "
            "chevreaux*. Communes as printed in each edition (sgt1924 writes *Ariana (L')*, *El-Hamma*, *Le Kef*, "
            "*La Marsa*, *Zazhouan* [sic] ...; sgt1923 prints Souk-el-Arba before Soliman). No English "
            "translation or harmonisation of commune names is attempted.",
            "Not applicable: sgt1923 Ksour-Essaf and Medjez-el-Bab (*Droits affermés*: slaughter dues farmed out) "
            "and Maharès (*Taxe instituée en 1924*); sgt1924 Medjez-el-Bab (*Droits d'abatage affermés*): stored "
            "empty with `not_applicable`. sgt1924 Souk-el-Arba total printed *10.358 et 829 kig. viande foraine* "
            "(829 kg of meat brought in from outside; not stored).",
            "sgt1924: the bœufs of Tunis and Tozeur are printed 228 and 37.622, evidently interchanged (the two "
            "row totals, 231.499 and 7.977, agree only with the swap); stored realigned, flagged `row_realigned`.",
            "Explanation of the failed checks (every cell concerned re-read on native-resolution crops). "
            "sgt1922: Bizerte prints total 23.799 for lines summing to 27.399, and the A reporter line prints "
            "chèvres 68.683 and total 246.632 where the lines give 67.783 and 245.732; the TOTAUX line agrees "
            "with the lines (the Report line repeats the misprinted A reporter, hence the second-spread failures "
            "of 900). Totals only, nothing stored is affected. "
            "sgt1923: Sfax pigs printed 203; the Sfax total (62.067) and the pigs TOTAUX (5.670) both need 208, "
            "so the cell is flagged `total_mismatch` (printed value kept). The moutons TOTAUX (379.833) and the "
            "grand total (668.683) are 10 below the lines; no single cell could be located (the moutons column "
            "lies against the binding but every figure is legible). "
            "sgt1924: several lines do not add to their printed totals (Ferryville +6, Foum-Tatahouine -11, "
            "Souk-el-Arba -7, Teboursouk +9) and the A reporter / TOTAUX lines differ from the column sums "
            "(moutons, chameaux, total on the first spread; bœufs 18.009 lower, veaux 100 lower, chèvres and "
            "porcs slightly higher on the second). The printed TOTAUX line is consistent with itself (the "
            "species add to 704.508 within one unit), so it was evidently set from different figures than the "
            "lines; the cells stand as printed and nothing is flagged.",
            "Survey of the whole chapter: `commerce_survey.md`.",
        ]
        write_csv(T_SLA, cols, kept)
        write_notes(T_SLA, CHAPTER, SCRIPT, kept, cols, SLA_DOC, "Consommation : animaux abattus",
                    "Consumption: animals slaughtered, by commune", paras, CHK.n[T_SLA], fails, compared, diffs,
                    coverage_lines(used), "Selection: each edition prints a single year; no overlap.",
                    "Unit: head (number of animals), as printed. value_type: count.")
    return res


# ----------------------------------------------------------------- Céréales : a) importation et exportation

T_CER = "commerce_cereals_balance"
CER_PRODUCT = {"wheat": "Blés (dur et tendre)", "flour": "Farine", "semolina_groats": "Semoules en gruaux",
               "semolina_pasta": "Semoules en pâtes", "barley": "Orge", "oats": "Avoine",
               "maize": "Maïs et sorgho"}
CER_FLOW = {"import": "Importation", "export": "Exportation", "balance": "Balance"}
# printed sign contradicted by the import/export lines and by the printed five-year averages of the balance
CER_MISPRINTS = {("1916-1917", "maize", "balance"), ("1919-1920", "wheat", "balance"),
                 ("1920-1921", "wheat", "balance"), ("1920-1921", "maize", "balance")}
# printed one line too high (above the Importation line); the balance confirms the line
CER_REALIGN = {("sgt1922", "1912-1913", "flour", "import")}
CER_DOC = {
    "census": "edition (each prints the last ten campaigns)",
    "table_id": "`cereals` (Céréales : a) Importation et exportation par campagne commerciale)",
    "gallica_ark": "Gallica volume ark", "source_page": "printed page number", "gallica_view": "Gallica view (fNNNN)",
    "year": "year in which the commercial campaign ends (campaign 1912-1913 -> 1913)",
    "campaign": "commercial campaign as printed (e.g. `1912-1913`)",
    "product": "`wheat`, `flour`, `semolina_groats`, `semolina_pasta`, `barley`, `oats`, `maize`",
    "product_fr": "line heading as printed",
    "flow": "`import`, `export`, `balance` (balance = import - export, printed with its sign: + = excess of "
            "imports, - = excess of exports)",
    "flow_fr": "Importation, Exportation, Balance",
    "measure": "`quantity`", "measure_fr": "quantité", "unit": "`quintals` (printed *quint*, metric quintals)",
    "value": "quantity as printed (» stored as 0); balances signed as printed",
    "flag": "empty, `total_mismatch` or `row_realigned` (see notes)",
}


def build_cereals(secs, write):
    recs, used, cells, avgs = [], [], {}, {}
    for s in secs:
        if s["table"] != "cereals":
            continue
        used.append(s)
        ed = s["ed"]
        for r in s["rows"]:
            prod, flow = r["label"].split(".")
            for c, cell in r["cells"].items():
                if c.startswith("avg"):
                    avgs[(ed, prod, flow, c)] = cell.value
                    continue
                cells[(ed, prod, flow, c)] = cell.value
                flag = cell.flag
                if (c, prod, flow) in CER_MISPRINTS:
                    flag = "total_mismatch"
                elif (ed, c, prod, flow) in CER_REALIGN:
                    flag = "row_realigned"
                recs.append({"census": ed, "table_id": "cereals", "gallica_ark": s["ark"], "source_page": s["page"],
                             "gallica_view": s["view"], "year": int(c[5:]), "campaign": c, "product": prod,
                             "product_fr": CER_PRODUCT[prod], "flow": flow, "flow_fr": CER_FLOW[flow],
                             "measure": "quantity", "measure_fr": "quantité", "unit": "quintals",
                             "value": cell.value, "flag": flag})
    for (ed, prod, flow, c), b in sorted(cells.items()):
        if flow == "balance":
            i, e = cells[(ed, prod, "import", c)], cells[(ed, prod, "export", c)]
            if None not in (i, e):
                CHK.eq(T_CER, f"{ed} {c} {prod}: balance = import - export", i - e, b)
    for (ed, prod, flow, a), printed in sorted(avgs.items()):
        y0, y1 = int(a[3:7]), int(a[8:12])
        vals = [v for (e2, p2, f2, c), v in cells.items() if (e2, p2, f2) == (ed, prod, flow) and y0 <= int(c[5:]) <= y1]
        if len(vals) == y1 - y0 + 1 and None not in vals:
            CHK.eq(T_CER, f"{ed} {prod} {flow}: printed average {y0 - 1}-{y0}/{y1 - 1}-{y1} = mean of the years",
                   (sum(vals) / len(vals)).quantize(Decimal(1)), printed, tol=Decimal(1))
    kept, compared, diffs, n_ill = select_legible(recs, ["campaign", "product", "flow"])
    kept.sort(key=lambda r: (r["year"], list(CER_PRODUCT).index(r["product"]), list(CER_FLOW).index(r["flow"])))
    fails = CHK.fail[T_CER]
    flagged = [f"{r['census']} {r['campaign']} {r['product']} {r['flow']} {r['flag']}" for r in kept if r["flag"]]
    res = dict(rows=len(kept), checks=CHK.n[T_CER], failed=list(fails), overlap_compared=compared,
               overlap_diffs=[list(d) for d in diffs], flagged=flagged, editions=EDITIONS_DONE, value_type="count",
               illegible_printings_skipped=n_ill)
    if write:
        cols = COMMON + ["campaign", "product", "product_fr", "flow", "flow_fr", "measure", "measure_fr", "unit",
                         "value", "flag"]
        paras = [
            "Imports, exports and balance of cereals and cereal products by commercial campaign (quintals). Full "
            "printed title: *Céréales (blé dur et dérivés, blé tendre et dérivés, orge, avoine, maïs) : a) "
            "Importation et exportation par campagne commerciale*. Footnote (1) (translated): the sign + indicates "
            "the excess of imports over exports; the sign -, the excess of exports over imports. The balance line "
            "is printed and is stored as printed (signed), and also used as a check (balance = import - export). "
            "The three printed averages (*Moyenne des années*, two five-campaign and one ten-campaign average) were "
            "transcribed as checks and are not stored.",
            "Gutter: the fourth campaign of each spread lies against the binding. sgt1922 1915-1916 maize (three "
            "cells) and sgt1923 1916-1917 (whole column) have digits hidden in the fold and were typed `?`; sgt1923 "
            "flour export 1914-1915 has its first digit under an ink blot (`?`). Each of these campaigns is legible "
            "in another printing, from which it is stored (latest legible printing). sgt1922 prints the flour import "
            "of 1912-1913 (596.204) one line too high, above *Importation*; stored on the import line (the balance "
            "596.204 - 33.024 = 563.180 agrees), flagged `row_realigned`.",
            "Explanation of the failed balance checks (each cell re-read on native-resolution crops of every printing; "
            "every one recurs identically in the two or three printings, each typed from its own image): "
            "maize 1916-1917 is printed *+ 16.720* in all three editions while exports (18.663) exceed imports "
            "(1.943); the printed five-campaign averages of sgt1924 (+57.407, i.e. the mean with - 16.720) confirm the "
            "negative value, so the cell is flagged `total_mismatch` (printed sign kept). Wheat 1919-1920 (703 - 311.077, "
            "printed - 311.374), wheat 1920-1921 (printed 497.996 for 498.096) and maize 1920-1921 (463.985 for "
            "472.985): the printed averages of the balance that include these campaigns are higher by exactly "
            "(1.000 + 100) / 5 = 220 (wheat, all three editions) and 9.000 / 5 = 1.800 (maize, sgt1923 and sgt1924; sgt1922 2.400), i.e. they were "
            "computed from the correct balances; the three cells are flagged `total_mismatch` (printed value kept). "
            "Flour 1920-1921 (850 for 855), semolina in pasta 1913-1914 (2.843 for 2.793) and 1915-1916 (2.099 for "
            "2.100): the import and export lines and the balance are each clearly printed and the averages do not "
            "decide; so nothing is flagged. sgt1923 prints the maize balance 1921-1922 as 8.673 "
            "(sgt1922 and sgt1924: 8.678, which agrees with 9.113 - 435); the sgt1924 value is stored.",
            "Explanation of the remaining failed average checks (besides those explained above by the four flagged "
            "balances): the printed averages were evidently computed from figures "
            "differing slightly from the yearly lines (differences of a few units to a few hundred quintals on most "
            "lines, larger on balances, which the printer averaged from balances that do not always equal import - "
            "export). A few are grossly wrong (sgt1922 semolina in groats export 1912-13/1916-17 printed 55.405 "
            "where the five campaigns average 1.494; sgt1923 oats import 1918-19/1922-23 5.465 for 3.465; sgt1924 "
            "semolina in pasta export 1919-20/1923-24 3.090 for 6.091). The yearly cells concerned were re-read and "
            "stand as transcribed; averages are not stored, so nothing is flagged on their account.",
            "Survey of the whole chapter: `commerce_survey.md`.",
        ]
        write_csv(T_CER, cols, kept)
        write_notes(T_CER, CHAPTER, SCRIPT, kept, cols, CER_DOC,
                    "Céréales : a) Importation et exportation par campagne commerciale",
                    "Cereals: imports and exports by commercial campaign", paras, CHK.n[T_CER], fails, compared,
                    diffs, coverage_lines(used),
                    "Selection (SPEC_ADDENDUM rule 4): each edition prints the last ten campaigns (sgt1922 "
                    "1912-1913 to 1921-1922, sgt1923 to 1922-1923, sgt1924 to 1923-1924); each campaign is stored "
                    "once, from the latest edition printing it legibly; every other printing is compared and the "
                    "differences listed below.",
                    "Unit: metric quintals, as printed. value_type: count (quantity).")
    return res


# ----------------------------------------------------------------- Céréales : b) stocks, c) consommation moyenne

T_CST = "commerce_cereals_stocks"
CST_PRODUCT = {"wheat": "Blés (1)", "barley": "Orge", "oats": "Avoine", "maize": "Maïs et sorgho"}
CST_MEASURE = {"production": ("Production", "thousand_quintals"),
               "campaign": ("Campagne commerciale consécutive", "thousand_quintals"),
               "remaining": ("Quantités restant dans le pays", "thousand_quintals"),
               "seed": ("Quantités prélevées pour les semences", "thousand_quintals"),
               "consumption": ("Quantités restant pour la consommation", "thousand_quintals"),
               "avg_consumption_total": ("Consommation moyenne totale", "quintals"),
               "avg_consumption_per_capita": ("Consommation moyenne par habitant", "kilograms_per_inhabitant")}
# printed average omits one year of the b) column (see notes)
CST_MISPRINTS = {("sgt1923", "maize", "avg_consumption_total")}
CST_DOC = {
    "census": "edition the value is taken from (b: latest edition printing the harvest, rule 4; c: each edition "
              "prints its own ten-year period)",
    "table_id": "`cereals_stocks` (b) Stoks disponibles) or `cereals_consumption` (c) Consommation moyenne)",
    "gallica_ark": "Gallica volume ark", "source_page": "printed page number", "gallica_view": "Gallica view (fNNNN)",
    "year": "b: harvest year (Récolte); c: last year of the averaging period",
    "period": "b: harvest year; c: averaging period as printed (e.g. `1912-1921`)",
    "product": "`wheat`, `barley`, `oats`, `maize` (c) has no oats line)",
    "product_fr": "line heading as printed",
    "measure": "`production`, `campaign`, `remaining`, `seed`, `consumption` (b); `avg_consumption_total`, "
               "`avg_consumption_per_capita` (c)",
    "measure_fr": "column heading (translated column codes in the notes)",
    "unit": "`thousand_quintals` (b, printed *1.000 qt*), `quintals` (c total), `kilograms_per_inhabitant` (c per "
            "capita)",
    "value": "as printed; campaign signed as printed (+ = excess of imports, - = excess of exports)",
    "flag": "empty, `not_applicable` (per capita printed », not computed) or `total_mismatch` (see notes)",
}


def build_cereals_stocks(secs, write):
    recs, used, b = [], [], {}
    for s in secs:
        if s["table"] not in ("cereals_stocks", "cereals_consumption"):
            continue
        used.append(s)
        ed = s["ed"]
        for r in s["rows"]:
            if s["table"] == "cereals_stocks":
                y, prod = r["label"].split(".")
                year, period = int(y), y
            else:
                prod, period = r["label"], s["period"]
                year = int(period[5:])
            for c, cell in r["cells"].items():
                m = c if s["table"] == "cereals_stocks" else "avg_consumption_" + c
                if s["table"] == "cereals_stocks":
                    b[(ed, year, prod, c)] = cell.value
                recs.append({"census": ed, "table_id": s["table"], "gallica_ark": s["ark"], "source_page": s["page"],
                             "gallica_view": s["view"], "year": year, "period": period, "product": prod,
                             "product_fr": CST_PRODUCT[prod] if s["table"] == "cereals_stocks"
                             else {"wheat": "Blé (1)"}.get(prod, CST_PRODUCT[prod]),
                             "measure": m, "measure_fr": CST_MEASURE[m][0], "unit": CST_MEASURE[m][1],
                             "value": cell.value,
                             "flag": "total_mismatch" if (ed, prod, m) in CST_MISPRINTS else cell.flag})
    for (ed, y, prod, c), val in sorted(b.items()):
        if c == "remaining":
            CHK.eq(T_CST, f"{ed} {y} {prod}: production + campaign = remaining",
                   b[(ed, y, prod, "production")] + b[(ed, y, prod, "campaign")], val)
        if c == "consumption":
            CHK.eq(T_CST, f"{ed} {y} {prod}: remaining - seed = consumption",
                   b[(ed, y, prod, "remaining")] - b[(ed, y, prod, "seed")], val)
    for r in recs:
        if r["measure"] == "avg_consumption_total":
            y0, y1 = int(r["period"][:4]), int(r["period"][5:])
            vals = [b[(r["census"], y, r["product"], "consumption")] for y in range(y0, y1 + 1)]
            CHK.eq(T_CST, f"{r['census']} {r['product']}: average consumption {r['period']} = mean of the b) "
                   f"consumption column x 1000", sum(vals) * 1000 / len(vals), r["value"])
    kept, compared, diffs, n_ill = select_legible(recs, ["table_id", "period", "product", "measure"])
    kept.sort(key=lambda r: (r["table_id"] != "cereals_stocks", r["year"], list(CST_PRODUCT).index(r["product"]),
                             list(CST_MEASURE).index(r["measure"])))
    fails = CHK.fail[T_CST]
    flagged = [f"{r['census']} {r['period']} {r['product']} {r['measure']} {r['flag']}" for r in kept if r["flag"]]
    res = dict(rows=len(kept), checks=CHK.n[T_CST], failed=list(fails), overlap_compared=compared,
               overlap_diffs=[list(d) for d in diffs], flagged=flagged, editions=EDITIONS_DONE, value_type="count",
               illegible_printings_skipped=n_ill)
    if write:
        cols = COMMON + ["period", "product", "product_fr", "measure", "measure_fr", "unit", "value", "flag"]
        paras = [
            "Cereal stocks available after each harvest and average consumption. Full printed titles: *Céréales : "
            "b) Stoks disponibles* (two-page spread) and *c) Consommation moyenne des années 1912 à 1921* (sgt1922; "
            "sgt1923 *1913 à 1922*, sgt1924 *1914-1923*). Footnotes (translated): (1) wheat includes flours and "
            "semolinas, counted as the corresponding weight of grain; (2) the sign + indicates the excess of imports "
            "over exports, the sign -, the excess of exports over imports; (3) seed not included.",
            "Column codes of b) (all in thousands of quintals): `production` = Production; `campaign` = Campagne "
            "commerciale consécutive (net trade of the commercial campaign following the harvest, signed); "
            "`remaining` = Quantités restant dans le pays; `seed` = Quantités prélevées pour les semences; "
            "`consumption` = Quantités restant pour la consommation. The identities production + campaign = "
            "remaining and remaining - seed = consumption are checks (all values are stored as printed). The c) "
            "totals are checked against the mean of the b) consumption column of the same edition (x 1000).",
            "c) prints a per-capita figure for wheat only; the barley and maize cells are printed » (no figure "
            "computed) and are stored as NA with flag `not_applicable` rather than 0.",
            "sgt1923 labels its last harvest *1923* (f901); the sequence runs 1913-1921 then 1923 and sgt1924 prints "
            "the same four lines under 1922 (and different ones under 1923), so the label is a misprint and the "
            "lines were transcribed as harvest 1922 (stored from sgt1924 under rule 4 in any case).",
            "Explanation of the failed checks (cells re-read on native-resolution crops of f410-411, f900-901 and "
            "f1404-1405; each recurs identically in the three printings, each typed from its own image). Oats 1916 "
            "(360 - 277 = 83, printed remaining 93) and oats 1919 (450 - 318 = 132, printed 148): the campaign "
            "figures agree with the a) table (`commerce_cereals_balance`, oats balance 1916-1917 -277.087 and "
            "1919-1920 -317.983 quintals) and remaining - seed = consumption holds (93 - 42 = 51, 148 - 38 = 110), "
            "so either the production or the remaining-and-consumption figures are misprinted; the table does not "
            "decide which, so nothing is flagged. sgt1923 c) maize total is printed 138.200 quintals while the ten "
            "harvests 1913-1922 average 154.700; 138.200 is the sum of the nine harvests 1914-1922 (1.382 thousand "
            "quintals) divided by ten, i.e. the 1913 line (165) was left out. sgt1924 (141.900) and sgt1922 "
            "(215.600) agree with their columns. The printed value is kept and flagged `total_mismatch`.",
            "Survey of the whole chapter: `commerce_survey.md`.",
        ]
        write_csv(T_CST, cols, kept)
        write_notes(T_CST, CHAPTER, SCRIPT, kept, cols, CST_DOC,
                    "Céréales : b) Stoks disponibles ; c) Consommation moyenne",
                    "Cereals: available stocks and average consumption", paras, CHK.n[T_CST], fails, compared,
                    diffs, coverage_lines(used),
                    "Selection (SPEC_ADDENDUM rule 4): b) each edition prints the last ten harvests (sgt1922 "
                    "1912-1921, sgt1923 1913-1922, sgt1924 1914-1923); each harvest is stored once, from the latest "
                    "edition printing it; every other printing is compared and differences listed below. c) each "
                    "edition prints a different ten-year average; all three are stored.",
                    "Units: thousands of quintals (b), quintals and kilograms per inhabitant (c), as printed; "
                    "value_type: count (quantity).")
    return res


# ----------------------------------------------------------------- Huile d'olive et vins : a) b) c)

T_OW = "commerce_oil_wine_balance"
OW_PRODUCT = {"olive_oil": "Huile d'olive", "wine": "Vins"}
OW_MEASURE = {"import": "Importation", "export": "Exportation", "balance": "Balance",
              "production": "Production", "campaign": "Campagne commerciale consécutive",
              "remaining": "Quantités restant dans le pays",
              "avg_consumption_total": "Consommation moyenne totale",
              "avg_consumption_per_capita": "Consommation moyenne par habitant"}
OW_UNIT = {("olive_oil", "ab"): "thousand_quintals", ("wine", "ab"): "thousand_hectolitres",
           ("olive_oil", "total"): "kilograms", ("wine", "total"): "hectolitres",
           ("olive_oil", "per_capita"): "kilograms_per_inhabitant", ("wine", "per_capita"): "litres_per_inhabitant"}
OW_DOC = {
    "census": "edition the value is taken from (a, b: latest edition printing the campaign or harvest, rule 4; "
              "c: each edition prints its own ten-year average)",
    "table_id": "`oil_wine_trade` (a) Importation et exportation par campagne commerciale), `oil_wine_stocks` "
                "(b) Stoks disponibles) or `oil_wine_consumption` (c) Consommation moyenne)",
    "gallica_ark": "Gallica volume ark", "source_page": "printed page number", "gallica_view": "Gallica view (fNNNN)",
    "year": "a: first year of the campaign; b: harvest year; c: last year of the averaging period",
    "period": "a: commercial campaign (e.g. `1912-1913`); b: harvest year (Récolte); c: averaging period as printed",
    "product": "`olive_oil` or `wine`", "product_fr": "line heading as printed",
    "measure": "`import`, `export`, `balance` (a); `production`, `campaign`, `remaining` (b); "
               "`avg_consumption_total`, `avg_consumption_per_capita` (c)",
    "measure_fr": "line or column heading as printed",
    "unit": "`thousand_quintals` (oil a, b), `thousand_hectolitres` (wine a, b), `kilograms`, `hectolitres`, "
            "`kilograms_per_inhabitant`, `litres_per_inhabitant` (c), as printed",
    "value": "as printed; balance and campaign signed (+ = excess of imports, - = excess of exports)",
    "flag": "always empty in this table",
}


def build_oil_wine(secs, write):
    recs, used, a, b, avgs = [], [], {}, {}, {}
    for s in secs:
        if not s["table"].startswith("oil_wine_"):
            continue
        used.append(s)
        ed, prod, tab = s["ed"], s["product"], s["table"]
        for r in s["rows"]:
            for c, cell in r["cells"].items():
                if tab == "oil_wine_trade":
                    if c.startswith("avg"):
                        avgs[(ed, prod, r["label"], c)] = cell.value
                        continue
                    m, period, year, unit = r["label"], c, int(c[:4]), OW_UNIT[(prod, "ab")]
                    a[(ed, prod, m, year)] = cell.value
                elif tab == "oil_wine_stocks":
                    m, period, year, unit = c, r["label"], int(r["label"]), OW_UNIT[(prod, "ab")]
                    b[(ed, prod, m, year)] = cell.value
                else:
                    m, period, year, unit = "avg_consumption_" + c, s["period"], int(s["period"][5:]), OW_UNIT[(prod, c)]
                recs.append({"census": ed, "table_id": tab, "gallica_ark": s["ark"], "source_page": s["page"],
                             "gallica_view": s["view"], "year": year, "period": period, "product": prod,
                             "product_fr": OW_PRODUCT[prod], "measure": m, "measure_fr": OW_MEASURE[m],
                             "unit": unit, "value": cell.value, "flag": cell.flag})
    for (ed, prod, m, y), v in sorted(a.items()):
        if m == "balance":
            CHK.eq(T_OW, f"{ed} {prod} {y}-{y + 1}: balance = import - export",
                   a[(ed, prod, "import", y)] - a[(ed, prod, "export", y)], v)
    for (ed, prod, m, c), printed in sorted(avgs.items()):
        y0, y1 = int(c[3:7]) - 1, int(c[8:12]) - 1
        vals = [a[(ed, prod, m, y)] for y in range(y0, y1 + 1)]
        CHK.eq(T_OW, f"{ed} {prod} {m}: printed average {y0}-{y0 + 1}/{y1}-{y1 + 1} = mean of the campaigns",
               sum(vals) / len(vals), printed, tol=Decimal(1))
    for (ed, prod, m, y), v in sorted(b.items()):
        if m == "remaining":
            CHK.eq(T_OW, f"{ed} {prod} {y}: production + campaign = remaining",
                   b[(ed, prod, "production", y)] + b[(ed, prod, "campaign", y)], v)
        if m == "campaign" and (ed, prod, "balance", y) in a:
            CHK.eq(T_OW, f"{ed} {prod} {y}: b) campaign = a) balance {y}-{y + 1}", a[(ed, prod, "balance", y)], v)
    for r in recs:
        if r["measure"] == "avg_consumption_total":
            y0, y1 = int(r["period"][:4]), int(r["period"][5:])
            vals = [b[(r["census"], r["product"], "remaining", y)] for y in range(y0, y1 + 1)]
            mult = 100000 if r["product"] == "olive_oil" else 1000
            CHK.eq(T_OW, f"{r['census']} {r['product']}: average consumption {r['period']} = mean of the b) "
                   f"remaining column, in {r['unit']}", sum(vals) * mult / len(vals), r["value"])
    kept, compared, diffs, n_ill = select_legible(recs, ["table_id", "product", "period", "measure"])
    kept.sort(key=lambda r: (list(OW_PRODUCT).index(r["product"]),
                             ["oil_wine_trade", "oil_wine_stocks", "oil_wine_consumption"].index(r["table_id"]),
                             r["year"], list(OW_MEASURE).index(r["measure"])))
    fails = CHK.fail[T_OW]
    flagged = [f"{r['census']} {r['period']} {r['product']} {r['measure']} {r['flag']}" for r in kept if r["flag"]]
    res = dict(rows=len(kept), checks=CHK.n[T_OW], failed=list(fails), overlap_compared=compared,
               overlap_diffs=[list(d) for d in diffs], flagged=flagged, editions=EDITIONS_DONE, value_type="count",
               illegible_printings_skipped=n_ill)
    if write:
        cols = COMMON + ["period", "product", "product_fr", "measure", "measure_fr", "unit", "value", "flag"]
        paras = [
            "Olive oil and wine: imports and exports by commercial campaign, stocks available after each harvest, "
            "and average consumption. Printed titles: *Huile d'olive (1)* and *Vins*, each with *a) Importation et "
            "exportation par campagne commerciale*, *b) Stoks disponibles* and *c) Consommation moyenne des années "
            "1912 à 1921* (sgt1922; sgt1923 1913 à 1922, sgt1924 1914 à 1923). Footnotes (translated): olive oil "
            "(1) not including oils and *grignons* (pomace); wine a) (1) exports include those of the Navy; the "
            "sign + indicates the excess of imports over exports, the sign -, the excess of exports over imports; "
            "olive oil b) (1) the harvest considered is the one beginning at the end of the year and continuing "
            "into the first months of the next; wine c) (2) Muslims and Jews not included (per capita figure).",
            "a) and b) are printed in thousands of quintals (oil) and thousands of hectolitres (wine); the balance "
            "line (a) and the campaign column (b) are stored signed as printed and also used as checks (balance = "
            "import - export; production + campaign = remaining; b) campaign of harvest Y = a) balance of campaign "
            "Y-(Y+1)). The c) totals are checked against the mean of the b) *remaining* column of the same edition "
            "(1.000 quintals = 100.000 kg; 1.000 hl = 1.000 hl). The three printed averages of a) (*Moyenne des "
            "années*) were transcribed as checks (tolerance 1) and are not stored. Printed » = 0. sgt1922 prints "
            "the oil per capita figure as *7,046* (kilograms, decimal comma); sgt1923 and sgt1924 print 7.",
            "Explanation of the failed checks (cells re-read on native-resolution crops of f412-415, f902-905 and "
            "f1406-1409; each line typed separately from its own edition's images). Olive oil 1919: production 165, "
            "campaign - 20, remaining printed 135 (165 - 20 = 145), identically in all three editions; the campaign "
            "agrees with a) (1919-1920 export 20) and the printed c) totals (14.590.000, 14.530.000, 14.680.000 kg) "
            "agree with the remaining column as printed (135), so the production figure (or the remaining figure "
            "from which consumption was computed) is misprinted; the table does not decide which, nothing flagged. "
            "Wine 1916: production 450, campaign - 212, remaining printed 288 (450 - 212 = 238), in all three "
            "editions; sgt1923 and sgt1924 c) totals agree with 288, so the same remark applies. sgt1922 wine c) "
            "total printed 218.800 hl while the ten remaining figures 1912-1921 average 226.000 (221.000 with 238 "
            "for 1916): not explained by any single cell, kept as printed. Failed average checks (three, all "
            "sgt1923 olive oil): the import average 1913-14/1917-18 is printed 1 and the ten-campaign import "
            "average 0, while the campaigns (1, 6, 4, 1, », all re-read, and printed identically in sgt1922 and "
            "sgt1924) average 2,4 and 1,2; the balance average 1913-14/1917-18 (printed - 128) equals the printed "
            "export average 129 minus that import average 1, so the printer averaged a different import figure; the "
            "yearly cells stand. No figure is flagged since averages are not stored.",
            "Survey of the whole chapter: `commerce_survey.md`.",
        ]
        write_csv(T_OW, cols, kept)
        write_notes(T_OW, CHAPTER, SCRIPT, kept, cols, OW_DOC,
                    "Huile d'olive ; Vins : a) Importation et exportation par campagne commerciale ; b) Stoks "
                    "disponibles ; c) Consommation moyenne",
                    "Olive oil and wine: imports and exports by commercial campaign, available stocks and average "
                    "consumption", paras, CHK.n[T_OW], fails, compared, diffs, coverage_lines(used),
                    "Selection (SPEC_ADDENDUM rule 4): a) and b) each edition prints the last ten campaigns or "
                    "harvests; each is stored once, from the latest edition printing it; every other printing is "
                    "compared and differences listed below. c) each edition prints a different ten-year average; "
                    "all three are stored.",
                    "Units as printed (see `unit`); value_type: count (quantity).")
    return res


T_PRI = "commerce_prices"
PRI_MARKET = {"tunis": "Place de Tunis", "sousse": "Place de Sousse", "sfax": "Place de Sfax"}
# column code -> (product, product_fr as printed, unit as printed)
_KG, _Q = "francs_per_kilogram", "francs_per_quintal"
PRI_PRODUCT = {
    "beef": ("beef_live", "Bœuf, sur pied", _KG), "veal": ("veal_live", "Veau, sur pied", _KG),
    "mutton": ("mutton_live", "Mouton, sur pied", _KG), "pork": ("pork_live", "Porc, sur pied", _KG),
    "beef_fillet": ("beef_fillet", "Bœuf, 1re catégorie, filets", _KG),
    "beef_sirloin": ("beef_sirloin", "Bœuf, 1re catégorie, aloyaux", _KG),
    "beef_thigh": ("beef_thigh", "Bœuf, 1re catégorie, cuisses", _KG),
    "beef_rib": ("beef_rib", "Bœuf, 1re catégorie, côtes", _KG),
    "beef_breast_neck": ("beef_breast_neck", "Bœuf, 2e catégorie, poitrine et collier", _KG),
    "beef_shoulder": ("beef_shoulder", "Bœuf, 2e catégorie, épaules", _KG),
    "beef_short_rib": ("beef_short_rib", "Bœuf, 2e catégorie, plats de côtes", _KG),
    "veal_flank": ("veal_flank", "Veau, 1re catégorie, pans", _KG),
    "veal_leg": ("veal_leg", "Veau, 1re catégorie, cuisseaux", _KG),
    "veal_rack": ("veal_rack", "Veau, 1re catégorie, carrés", _KG),
    "veal_loin": ("veal_loin", "Veau, 2e catégorie, longes", _KG),
    "veal_shoulder": ("veal_shoulder", "Veau, 2e catégorie, épaules", _KG),
    "veal_breast": ("veal_breast", "Veau, 2e catégorie, poitrines", _KG),
    "mutton_leg": ("mutton_leg", "Mouton, 1re catégorie, gigots", _KG),
    "mutton_rack": ("mutton_rack", "Mouton, 1re catégorie, carrés", _KG),
    "mutton_fillet": ("mutton_fillet", "Mouton, 1re catégorie, filets", _KG),
    "mutton_breast_neck": ("mutton_breast_neck", "Mouton, 2e catégorie, poitrine et collets", _KG),
    "mutton_scrag": ("mutton_scrag", "Mouton, 2e catégorie, bas carrés", _KG),
    "mutton_shoulder": ("mutton_shoulder", "Mouton, 2e catégorie, épaules", _KG),
    "pork_fillet": ("pork_fillet", "Porc, 1re catégorie, filets", _KG),
    "pork_loin": ("pork_loin", "Porc, 1re catégorie, reins", _KG),
    "pork_ham": ("pork_ham", "Porc, 1re catégorie, jambons", _KG),
    "pork_belly": ("pork_belly", "Porc, 1re catégorie, poitrine", _KG),
    "pork_shoulder": ("pork_shoulder", "Porc, 2e catégorie, épaules", _KG),
    "pork_chine": ("pork_chine", "Porc, 2e catégorie, échine", _KG),
    "pork_head": ("pork_head", "Porc, 2e catégorie, tête", _KG),
    "cattle_hides": ("cattle_hides", "Peaux de bœuf", _Q),
    "sheep_skins": ("sheep_skins", "Peaux de mouton", "francs_per_piece"),
    "goat_skins": ("goat_skins", "Peaux de chèvre", "francs_per_piece"),
    "greasy_wool": ("greasy_wool", "Laines en suint", _Q),
    "eggs": ("eggs", "Œufs", "francs_per_hundred"),
    "durum_wheat": ("durum_wheat", "Blé dur", _Q), "soft_wheat": ("soft_wheat", "Blé tendre", _Q),
    "barley": ("barley", "Orge", _Q), "oats": ("oats", "Avoine", _Q), "maize": ("maize", "Maïs", _Q),
    "daris": ("daris", "Daris (sorgho blanc)", _Q), "broad_beans": ("broad_beans", "Fèves et fèverolles", _Q),
    "chickpeas": ("chickpeas", "Pois chiches", _Q), "linseed": ("linseed", "Graines de lin", _Q),
    "oil_first_press": ("olive_oil_first_pressing", "Huile d'olive, 1re pression", _Q),
    "oil_second_press": ("olive_oil_second_pressing", "Huile d'olive, 2e pression", _Q),
    "oil_masri_lampante": ("olive_oil_masri_lampante", "Huile d'olive, masri lampante", _Q),
    "pomace_oil": ("pomace_oil", "Huile de grignons", _Q),
    "red_wine_deg": ("red_wine", "Vin rouge", "francs_per_degree"),
    "red_wine_hl": ("red_wine", "Vin rouge", "francs_per_hectolitre"),
    "white_wine_deg": ("white_wine", "Vin blanc", "francs_per_degree"),
    "white_wine_hl": ("white_wine", "Vin blanc", "francs_per_hectolitre"),
}
PRI_MEASURE = {"min": ("minimum", "minimum"), "max": ("maximum", "maximum"), "avg": ("average", "moyenne")}
PRI_TABLE = {"prices_live": "Animaux (viande sur pied)",
             "prices_retail": "Prix moyen mensuel du kilogr. de viande au détail par catégories et par espèces",
             "prices_animal_products": "Dépouilles et produits animaux (peaux, laine en suint et œufs)",
             "prices_cereals": "Céréales (blé; orge; avoine; maïs; sorgho; fèves, pois chiches; graine de lin)",
             "prices_oils": "Huiles végétales (huile d'olive; huile de grignons)", "prices_wine": "Vins"}
PRI_MOYEN = {"prices_live"}  # average column headed 'moyen' (elsewhere 'moyenne')
PRI_MOYEN_ED = {(ed, "sfax", "oil_masri_lampante") for ed in EDITIONS_DONE}
PRI_LABEL_ED = {("sgt1924", "veal_leg"): "Veau, 1re catégorie, cuissots"}
# cells printed with their hundreds digit missing (located by the minimum / average / maximum of the line)
PRI_MISPRINTS = {
    ("sgt1924", "durum_wheat", 12, "min"): "printed '1 38'; the maximum 146,25 and average 142,10 imply 138",
    ("sgt1924", "soft_wheat", 12, "max"): "printed '1 31'; the minimum 125,50 and average 128,25 imply 131",
}
PRI_DOC = {
    "census": "edition (each prints one year, its reference year; no overlap)",
    "table_id": "`prices_live`, `prices_retail`, `prices_animal_products`, `prices_cereals`, `prices_oils`, "
                "`prices_wine` (sub-tables of *Mercuriales*)",
    "gallica_ark": "Gallica volume ark", "source_page": "printed page number", "gallica_view": "Gallica view (fNNNN)",
    "year": "reference year of the edition (not printed in the heading: 1922, 1923, 1924)",
    "month": "month, 1-12 (printed Janvier ... Décembre)",
    "market": "`tunis`, `sousse`, `sfax`", "market_fr": "as printed (Place de ...)",
    "product": "product code (live animal, cut of meat, hide, cereal, oil, wine)",
    "product_fr": "column headings as printed, joined with commas",
    "measure": "`minimum`, `maximum`, `average` (retail meat: average only)",
    "measure_fr": "column heading as printed (retail meat: prix moyen mensuel)",
    "unit": "`francs_per_kilogram`, `francs_per_quintal`, `francs_per_piece`, `francs_per_hundred` (eggs), "
            "`francs_per_degree`, `francs_per_hectolitre` (wine), as printed",
    "value": "price in francs, with centimes (printed '1 35' = 1.35; » in the centimes column = .00)",
    "flag": "empty or `not_applicable` (printed — (1) *Aucune transaction* / *Sans affaires*)",
}


PRI_PARAS = [
    "Market prices (*Mercuriales*) for the reference year of each edition (the heading prints no year: sgt1922 "
    "1922, sgt1923 1923, sgt1924 1924; consecutive editions do not overlap). Sub-tables (table_id): `prices_live` "
    "*Animaux (Viande sur pied et viande abattue)*, live weight per kg, minimum / maximum / moyen; `prices_retail` "
    "*Prix moyen mensuel du kilogr. de viande au détail par catégories et par espèces* (beef, veal, mutton, pork "
    "by cut and category; one monthly average per cut); `prices_animal_products` *Dépouilles et produits animaux* "
    "(cattle hides per quintal, sheep and goat skins per piece, greasy wool per quintal, eggs per hundred); "
    "`prices_cereals` *Céréales* (prices per quintal: the unit is not printed in this sub-table; stored as "
    "`francs_per_quintal`, the usual unit of the Tunis cereal market and consistent with the magnitudes); "
    "`prices_oils` *Huiles végétales* a) Tunis, b) Sousse, c) Sfax, per quintal; `prices_wine` *Vins*, Tunis, per "
    "degree and (sgt1922 only) per hectolitre. All markets are *Place de Tunis* unless stated (`market`).",
    "Content differs between editions: sgt1922 prints live veal, eggs, chickpeas and the wine price per hectolitre; "
    "sgt1923 and sgt1924 do not (their live-animal table has beef, mutton and pork; the beef 'moyen' column "
    "lies against the binding and is repeated, cut, at the edge of the facing page). Products are stored only for "
    "the editions that print them.",
    "Values: francs with centimes ('1 35' = 1,35; '2 »' = 2,00), stored with two decimals. A dash with footnote "
    "(1) *Aucune transaction* / *Sans affaires* (sgt1922), or a lone » with footnote (») *Aucune transaction* / "
    "*Sans affaires* (sgt1923, sgt1924), means no transaction that month: stored empty, flag `not_applicable`. "
    "Daris (white sorghum): every edition prints the three headings as *maximum | minimum | moyenne*, but the "
    "first column is always the lower; stored as `minimum` / `maximum` by position, `measure_fr` keeping the "
    "printed heading.",
    "Gutter cells (binding): sgt1923 beef live average November and cattle-hide average September and November: "
    "centimes cut, stored empty with flag `illegible`; sgt1923 retail veal *longes* (2e catégorie): the whole "
    "column lies in the binding (only the » of some centimes visible), stored `illegible`. sgt1923 oats minimum: "
    "the tens digit is partly cut; read from its visible remnant, each reading agreeing with the printed maximum "
    "and average. The remaining gutter columns (sgt1922 veal carrés / longes, oats and maize; sgt1923 veal "
    "carrés, barley average; sgt1924 veal carrés, barley average) were read on the crops of both facing pages.",
    "Checks: on every line with minimum, maximum and average, minimum <= average <= maximum (the average is not "
    "always the midpoint, so no stricter check is made). Explanation of the failed checks (all cells re-read on "
    "native-resolution crops; the printed values are kept): sgt1922 Sfax masri lampante February, average printed "
    "236,25 between 202,50 and 210 (probably 206,25); sgt1922 cattle hides August, maximum printed 48 (probably "
    "248); sgt1923 daris November, average 58,75 below the minimum 59,25 (probably 59,75); sgt1923 durum wheat July "
    "average 71,35 (74,80-77,90, probably 76,35) and September average 79,10 (71,25-77; probably 74,10); sgt1923 "
    "greasy wool September, average 453,75 (463,75-543,75, probably 503,75); sgt1923 Tunis first-pressing oil "
    "October, average 349,35 (475-483,75, probably 479,35); sgt1924 Sfax second-pressing oil April, average "
    "675,30 above the maximum 673,10 (probably 670,30); sgt1924 barley May, average 68,50 (57,50-59,50, probably "
    "58,50); sgt1924 cattle hides September, average 568,75 above the maximum 537,50 (the minimum 400 or the "
    "average is misprinted; not decidable); sgt1924 soft wheat December, maximum printed '1 31' (hundreds digit "
    "missing). The two cells printed with the hundreds digit missing are flagged `total_mismatch`: "
    + "; ".join(f"{e} {p} month {m} {s}: {n}" for (e, p, m, s), n in PRI_MISPRINTS.items()) + " (the "
    "first passes the check only because 1,38 is below the average). Not caught by the check: sgt1922 Tunis masri "
    "lampante June maximum printed 843,75 (minimum 335, average 339,35; probably 343,75), kept as printed.",
    "The Gallica OCR was used only as a cross-check (it renders » and the centimes column unreliably).",
    "Survey of the whole chapter: `commerce_survey.md`.",
]


def build_prices(secs, write):
    recs, used = [], []
    trip = defaultdict(dict)
    for s in secs:
        if not s["table"].startswith("prices_"):
            continue
        used.append(s)
        ed, mk = s["ed"], s["market"]
        swap = s.get("heading_swap", "")
        for r in s["rows"]:
            month = int(r["label"])
            for c, cell in r["cells"].items():
                code, stat = c.split(".") if "." in c else (c, "avg")
                prod, prod_fr, unit = PRI_PRODUCT[code]
                prod_fr = PRI_LABEL_ED.get((ed, code), prod_fr)
                m, m_fr = PRI_MEASURE[stat]
                if s["table"] == "prices_retail":
                    m_fr = "prix moyen mensuel"
                elif s["table"] in PRI_MOYEN or (ed, mk, code) in PRI_MOYEN_ED:
                    m_fr = "moyen" if stat == "avg" else m_fr
                if code == swap and stat in ("min", "max"):
                    m_fr = {"min": "maximum", "max": "minimum"}[stat]
                val = None if cell.value is None else cell.value.quantize(Decimal("0.01"))
                if s["table"] != "prices_retail":
                    trip[(ed, mk, code, month, f"f{s['view']}")][stat] = val
                recs.append({"census": ed, "table_id": s["table"], "gallica_ark": s["ark"], "source_page": s["page"],
                             "gallica_view": s["view"], "year": int(ed[3:]), "month": month, "market": mk,
                             "market_fr": PRI_MARKET[mk], "product": prod, "product_fr": prod_fr, "measure": m,
                             "measure_fr": m_fr, "unit": unit, "value": val,
                             "flag": cell.flag or ("total_mismatch" if (ed, code, month, stat) in PRI_MISPRINTS else "")})
    for (ed, mk, code, month, view), d in sorted(trip.items()):
        if any(d.get(k) is None for k in ("min", "max", "avg")):
            continue
        CHK.n[T_PRI] += 1
        if not d["min"] <= d["avg"] <= d["max"]:
            CHK.fail[T_PRI].append(f"{ed} {view} {mk} {code} month {month}: minimum <= average <= maximum: printed "
                                   f"{d['min']}, {d['avg']}, {d['max']}")
    kept, compared, diffs = select_latest(recs, ["year", "market", "product", "unit", "month", "measure"])
    order = list(PRI_TABLE)
    codes = [p[0] for p in PRI_PRODUCT.values()]
    kept.sort(key=lambda r: (r["year"], order.index(r["table_id"]), list(PRI_MARKET).index(r["market"]),
                             codes.index(r["product"]), r["unit"], r["month"],
                             ["minimum", "maximum", "average"].index(r["measure"])))
    fails = CHK.fail[T_PRI]
    flagged = [f"{r['census']} {r['market']} {r['product']} {r['month']} {r['measure']} {r['flag']}"
               for r in kept if r["flag"]]
    res = dict(rows=len(kept), checks=CHK.n[T_PRI], failed=list(fails), overlap_compared=compared,
               overlap_diffs=[list(d) for d in diffs], flagged=flagged, editions=EDITIONS_DONE, value_type="francs")
    if write:
        cols = COMMON + ["month", "market", "market_fr", "product", "product_fr", "measure", "measure_fr", "unit",
                         "value", "flag"]
        write_csv(T_PRI, cols, kept)
        write_notes(T_PRI, CHAPTER, SCRIPT, kept, cols, PRI_DOC, "Mercuriales",
                    "Market prices (mercuriales): monthly minimum, maximum and average prices", PRI_PARAS,
                    CHK.n[T_PRI], fails, compared, diffs, coverage_lines(used),
                    "Selection: each edition prints a single year (its reference year); no overlap, all stored.",
                    "Unit: francs (with centimes) per unit as printed (see `unit`). value_type: francs.")
    return res


def build(write):
    secs = []
    for ed in EDITIONS_DONE:
        secs += parse(TR / f"commerce_{ed}.txt", ed)
    general = defaultdict(dict)
    for s in secs:
        if s["table"] == "general":
            check_general(s)
            R = rows_of(s)
            for c in s["cols"]:
                general[(s["ed"], c)] = {f: R[f][c].value for f in FLOW}
    recs = []
    used = []
    by_class = {}
    for s in secs:
        if s["table"] == "by_class":
            for lab, cs in rows_of(s).items():
                for c in s["cols"]:
                    by_class[(s["ed"], c, lab)] = cs[c].value
    for s in secs:
        if s["table"] == "by_class":
            check_by_class(s, general)
            recs += records(s)
            used.append(s)
    kept, compared, diffs = select_latest(recs, ["year", "product_class", "flow"])
    kept.sort(key=lambda r: (r["year"], list(PRODUCT_CLASS).index(r["product_class"]), r["flow"]))
    fails = CHK.fail[T]
    flagged = [f"{r['census']} {r['year']} {r['product_class']} {r['flow']}" for r in kept if r["flag"]]
    res = {T: dict(rows=len(kept), checks=CHK.n[T], failed=list(fails), overlap_compared=compared,
                   overlap_diffs=[list(d) for d in diffs], flagged=flagged, editions=EDITIONS_DONE,
                   value_type="francs")}
    res[T_CAT] = build_category(secs, by_class, write)
    res[T_ORG] = build_origin(secs, by_class, write)
    res[T_CTY] = build_country(secs, write)
    res[T_CUS] = build_customs(secs, write)
    res[T_EXP] = build_export(secs, write)
    res[T_PORT] = build_nav_port(secs, write)
    res[T_FLAG] = build_nav_flag(secs, write)
    res[T_YR] = build_nav_yearly(secs, write)
    res[T_CAB] = build_cabotage(secs, write)
    res[T_FISH] = build_fisheries(secs, write)
    res[T_SLA] = build_slaughter(secs, write)
    res[T_CER] = build_cereals(secs, write)
    res[T_CST] = build_cereals_stocks(secs, write)
    res[T_OW] = build_oil_wine(secs, write)
    res[T_PRI] = build_prices(secs, write)
    if write:
        cols = COMMON + DIMS + ["value", "flag"]
        write_csv(T, cols, kept)
        expl = ["Explanation of the failed checks. (i) Nine failures are the 1915 misprints described above (vegetal "
                "Total, manufactures import and Total), repeated in each of the three editions; re-read on "
                "native-resolution crops of f282, f772 and f1276. "
                "(ii) sgt1924, 1924: the four classes sum to 929.943.922 (imports) and 582.452.535 (exports), "
                "while the a) table prints 927.943.882 and 582.353.545 (differences 2.000.040 and 98.990). Every "
                "class line agrees with its class total, so the b) table is internally consistent; the a) table "
                "and the c) category TOTAUX agree with each other, so b) was probably set from a different "
                "(provisional) state of the 1924 returns. Every 1924 cell of f1277 was re-read on a zoomed "
                "native-resolution crop and stands as transcribed. The c) category table of the same edition differs "
                "from b) on manufactures import (604.302.406), manufactures export (44.630.178) and animal export "
                "(54.347.670), but the differences (2.000.100, 109.100, -110) do not equal the a) discrepancies, so "
                "no single b) cell can be identified as the misprint and nothing is flagged. The 1924 "
                "figures are reprinted in sgt1925, which will allow a comparison when that edition is added."]
        paras = PARAS + expl + ["Survey of the whole chapter: `commerce_survey.md`."]
        write_notes(T, CHAPTER, SCRIPT, kept, cols, DOC,
                    "Renseignements généraux : résumé des importations et des exportations par classe de produits "
                    "(valeur en francs)",
                    "General information: imports and exports by class of products (value in francs)",
                    paras, CHK.n[T], fails, compared, diffs, coverage_lines(used), RULE4,
                    "Unit: francs (current values; see footnote on valuation from 1920). value_type: francs.")
        write_validation(OUT / f"{PREFIX}_validation.json",
                         dict(res, _chapter_views=CHAPTER_VIEWS, _editions_done=EDITIONS_DONE,
                              _remaining="see commerce_survey.md, section 'Work plan and status'"))
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


if __name__ == "__main__":
    main()
