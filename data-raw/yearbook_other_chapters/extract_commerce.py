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
from yb_tables import (COMMON, EDITIONS, ORDER, OUT, TR, Checks, coverage_lines, parse, select_latest, ssum, where,
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
