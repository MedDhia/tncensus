#!/usr/bin/env python3
"""Finances chapter (*Finances*: chapter X up to sgt1935, chapter IX in sgt1936 and sgt1939) of the Statistique
générale de la Tunisie, 12 editions sgt1922-sgt1939.

  python3 extract_finance.py check   parse the transcriptions, run every check, print failures
  python3 extract_finance.py build   ... and write csv/finance_*.csv, their .md notes,
                                     csv/finance_survey.md and csv/finance_validation.json

Source of truth: transcribed/finance_<edition>.txt (format in yb_tables.py). See csv/finance_survey.md for what
the chapter prints in every edition and which tables are transcribed.

Budget tables (sgt1925-sgt1939): annual budget, actual results (recettes réalisées; dépenses = droits constatés
définitivement liquidés lors des règlements des budgets), printed for overlapping ten-year (sgt1925-sgt1930) or
three-year (sgt1935-sgt1939) windows of exercices: SPEC_ADDENDUM rule 4 (each exercice from the latest edition
printing it, every other printing compared cell by cell). No budget forecasts (prévisions) are printed in the
chapter.
"""
import sys
from collections import defaultdict
from decimal import Decimal

from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parent))  # shared helper yb_tables.py
from yb_tables import (COMMON, EDITIONS, ORDER, OUT, TR, Checks, coverage_lines, parse, ssum, where, write_csv,
                       write_notes, write_validation)

CHAPTER = "Finances"
SCRIPT = "extract_finance.py"
PREFIX = "finance"

# Views of the chapter (chapter title .. last view before the next chapter title, Agriculture), confirmed on the
# page images (title pages "CHAPITRE X / FINANCES" and "CHAPITRE XI / AGRICULTURE"; IX and X in sgt1936-sgt1939).
CHAPTER_VIEWS = {
    "sgt1922": (185, 230), "sgt1923": (675, 720), "sgt1924": (1171, 1216), "sgt1925": (211, 286),
    "sgt1926": (767, 802), "sgt1927": (229, 258), "sgt1928": (753, 782), "sgt1929": (231, 260),
    "sgt1930": (765, 794), "sgt1935": (127, 138), "sgt1936": (94, 99), "sgt1939": (93, 98),
}

CHK = Checks()

# ----------------------------------------------------------------- budget: labels

PART = {"ordinary": "Titre premier (Première partie). Ressources ordinaires / Dépenses sur ressources ordinaires",
        "exceptional": "Titre II (Deuxième partie). Recettes sur ressources exceptionnelles / Dépenses sur "
                       "ressources exceptionnelles ou spéciales",
        "closed": "Titre III (Troisième partie)"}

# receipts, nomenclature used sgt1925-sgt1936 (code: item, part, printed label)
REC = {
    "ch1": ("direct_taxes", "ordinary", "Chapitre Ier. — Impôts directs et taxes assimilées"),
    "ch2": ("indirect_taxes", "ordinary", "Chapitre II. — Impôts et revenus indirects"),
    "ch3": ("monopolies_state_enterprises", "ordinary",
            "Chapitre III. — Produits des Monopoles et exploitations industrielles de l'Etat"),
    "ch4": ("state_domain", "ordinary", "Chapitre IV. — Produit du Domaine de l'Etat"),
    "ch5": ("miscellaneous", "ordinary", "Chapitre V. — Produits divers"),
    "loans": ("loan_funds", "exceptional", "Fonds d'emprunt"),
    "misc_exc": ("miscellaneous_receipts", "exceptional", "Recettes diverses"),
    "regions": ("regional_councils", "exceptional", "Recettes à la disposition des Conseils de Région"),
    "closed": ("closed_exercises", "closed", "Recettes affectées aux dépenses des exercices clos et périmés"),
    # sgt1939 nomenclature (budgets 1936-1938)
    "r_income": ("general_income_tax", "ordinary", "Impôt général sur les divers revenus : taxe personnelle et "
                 "contribution personnelle d'Etat"),
    "r_land_unbuilt": ("land_tax_unbuilt", "ordinary", "Impôts fonciers et sur les revenus d'immeubles : 1° "
                       "Propriété non bâtie (canouns, mradjas, khodors, achours, vigne et bétail)"),
    "r_land_built": ("land_tax_built", "ordinary", "Impôts fonciers et sur les revenus d'immeubles : 2° Propriété "
                     "bâtie : taxe locative des immeubles"),
    "r_patents": ("business_profits_patents", "ordinary", "Impôts sur les bénéfices commerciaux et industriels : "
                  "1° Patentes, bénéfices de guerre, redevance des mines"),
    "r_wages": ("wages_salaries", "ordinary", "Impôts sur les bénéfices commerciaux et industriels : 2° Impôt sur "
                "les traitements et salaires"),
    "r_securities": ("securities_income", "ordinary", "Impôt sur les revenus des valeurs mobilières, rentes "
                     "d'enzel, etc."),
    "r_assimilated": ("assimilated_taxes", "ordinary", "Taxes assimilées aux Contributions directes : poids et "
                      "mesures, visite des pharmacies, véhicules, etc."),
    "r_stamp": ("stamp_duties", "ordinary", "Droits de timbre"),
    "r_registration": ("registration_duties", "ordinary", "Droits d'enregistrement et de chancellerie"),
    "r_customs": ("customs_duties", "ordinary", "Droits de douane et droits maritimes"),
    "r_consumption": ("consumption_duties", "ordinary", "Droits de consommation"),
    "r_other_indirect": ("other_indirect_taxes", "ordinary", "Autres contributions indirectes"),
    "r_monopolies": ("monopolies", "ordinary", "Produit des Monopoles"),
    "r_posts": ("posts", "ordinary", "Produit des Postes"),
    "r_industrial": ("industrial_enterprises", "ordinary", "Produit d'exploitations industrielles"),
    "r_domain": ("state_domain", "ordinary", "Produit du Domaine"),
    "r_misc": ("miscellaneous", "ordinary", "Produits divers"),
}

SERVICE = {"fin": "finance", "sec": "general_secretariat", "int": "interior", "agr": "agriculture_economy",
           "edu": "education_fine_arts", "army": "army", "pw": "public_works", "just": "justice",
           "post": "posts_telegraphs", "unf": "unforeseen", "equip": "economic_equipment",
           "adm": "tunisian_administration"}
# nomenclatures 1926-1929 (sgt1925-sgt1930): chapter number -> service
OLD_ORD = {"o1": "fin", "o2": "post", "o3": "int", "o4": "agr", "o5": "edu", "o6": "army", "o7": "pw", "o8": "just",
           "o9": "unf", "o10": "equip"}
OLD_EXC = {"x1": "fin", "x2": "post", "x3": "int", "x4": "agr", "x5": "edu", "x6": "army", "x7": "pw", "x8": "just"}
LBL_OLD = {"fin": "Direction générale des Finances", "post": "Office des Postes et des Télégraphes",
           "int": "Direction générale de l'Intérieur",
           "agr": "Direction générale de l'Agriculture, du Commerce et de la Colonisation",
           "edu": "Direction générale de l'Instruction publique et des Beaux-Arts", "army": "Armée tunisienne",
           "pw": "Direction générale des Travaux Publics", "just": "Direction de la Justice",
           "unf": "Dépenses imprévues", "equip": "Dépenses d'outillage économique"}
ROMAN = ["Ier", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
# nomenclatures 1932 (sgt1935), 1935 (sgt1936), 1938 (sgt1939): chapter order and labels
NEW_ORDER = {"1932": ["fin", "sec", "int", "agr", "edu", "army", "pw", "just", "post", "unf"],
             "1935": ["fin", "sec", "int", "agr", "edu", "army", "pw", "just", "post", "unf"],
             "1938": ["fin", "sec", "post", "agr", "edu", "army", "pw", "just"]}
LBL_NEW = {"fin": "Direction générale des Finances", "sec": "Secrétariat général du Gouvernement tunisien",
           "int": "Direction générale de l'Intérieur",
           "agr": "Direction générale de l'Agriculture, du Commerce et de la Colonisation",
           "edu": "Direction générale de l'Instruction publique et des Beaux-Arts", "army": "Armée tunisienne",
           "pw": "Direction des Travaux Publics", "just": "Justice tunisienne",
           "post": "Office des Postes et des Télégraphes", "unf": "Dépenses imprévues"}
LBL_1935 = dict(LBL_NEW, fin="Direction des Finances", int="Direction de l'Intérieur",
                agr="Direction des Affaires Économiques", edu="Direction de l'Instruction publique et des Beaux-Arts")
LBL_1938 = dict(LBL_1935, int="Mémoire. — Direction de l'Intérieur", adm="Mémoire. — Administration tunisienne")

NOMENCLATURE = {  # printed in the heading of the designation column
    ("sgt1925", "receipts"): "nomenclature des budgets de 1916 à 1926", ("sgt1925", "expenditure"): "nomenclature de 1926",
    ("sgt1926", "receipts"): "nomenclature des budgets de 1916 à 1925", ("sgt1926", "expenditure"): "nomenclature de 1926",
    ("sgt1927", "receipts"): "nomenclature des budgets de 1917 à 1926", ("sgt1927", "expenditure"): "nomenclature de 1926",
    ("sgt1928", "receipts"): "nomenclature des budgets de 1918 à 1927", ("sgt1928", "expenditure"): "nomenclature de 1927",
    ("sgt1929", "receipts"): "nomenclature des budgets de 1919 à 1928", ("sgt1929", "expenditure"): "nomenclature de 1928",
    ("sgt1930", "receipts"): "nomenclature des budgets de 1920 à 1929", ("sgt1930", "expenditure"): "nomenclature de 1929",
    ("sgt1935", "receipts"): "nomenclature des budgets de 1932 à 1934", ("sgt1935", "expenditure"): "nomenclature de 1932",
    ("sgt1936", "receipts"): "nomenclature des budgets de 1933 à 1935", ("sgt1936", "expenditure"): "nomenclature de 1935",
    ("sgt1939", "receipts39"): "nomenclature des budgets de 1936 à 1938", ("sgt1939", "expenditure"): "nomenclature de 1938",
}
EXP_NOM = {"sgt1935": "1932", "sgt1936": "1935", "sgt1939": "1938"}
BASIS = {"receipts": ("actual", "Recettes réalisées"),
         "expenditure": ("actual", "Dépenses : droits constatés définitivement liquidés lors des règlements des "
                                   "budgets des exercices")}


def exp_item(sec, code):
    """(item, part, printed label) of an expenditure line."""
    ed = sec["ed"]
    if code == "closed":
        return "closed_exercises", "closed", "Dépenses des exercices clos et périmés"
    if code in OLD_ORD or code in OLD_EXC:
        part = "ordinary" if code.startswith("o") else "exceptional"
        svc = (OLD_ORD if part == "ordinary" else OLD_EXC)[code]
        n = int(code[1:])
        return f"{part}_{SERVICE[svc]}", part, f"Chapitre {ROMAN[n - 1]}. — {LBL_OLD[svc]}"
    part = "ordinary" if code.startswith("o_") else "exceptional"
    svc = code[2:]
    nom = EXP_NOM[ed]
    lbl = {"1932": LBL_NEW, "1935": LBL_1935, "1938": LBL_1938}[nom]
    order = NEW_ORDER[nom]
    if svc in order:
        txt = f"Chapitre {ROMAN[order.index(svc)]}. — {lbl[svc]}"
    else:
        txt = lbl[svc]
    return f"{part}_{SERVICE[svc]}", part, txt


def dl(sec):
    return [r for r in sec["rows"] if "cells" in r and not r["label"].startswith("Total")]


def row(sec, label):
    for r in sec["rows"]:
        if r["label"] == label:
            return r["cells"]
    return None


def base(sec, year):
    return {"census": sec["ed"], "table_id": sec["table"], "gallica_ark": sec["ark"], "source_page": sec["page"],
            "gallica_view": sec["view"], "year": year}


def mk(sec, cell, year, **dims):
    return dict(base(sec, year), **dims, value=cell.value, flag=cell.flag)


def months(year):
    return 9 if year == 1932 else 12


def cells_budget(sec):
    out = []
    t = "receipts" if sec["table"].startswith("receipts") else "expenditure"
    basis, basis_fr = BASIS[t]
    nom = NOMENCLATURE[(sec["ed"], sec["table"])]
    for r in dl(sec):
        if t == "receipts":
            item, part, lbl = REC[r["label"]]
        else:
            item, part, lbl = exp_item(sec, r["label"])
        for c in sec["cols"]:
            y = int(c)
            out.append(mk(sec, r["cells"][c], y, exercice_months=months(y), basis=basis, basis_fr=basis_fr,
                          part=part, part_fr=PART[part], item=item, item_fr=lbl, nomenclature_fr=nom,
                          unit="francs"))
    return out


def chk_budget(sec):
    out = "finance_budget_receipts" if sec["table"].startswith("receipts") else "finance_budget_expenditure"
    for c in sec["cols"]:
        if sec["table"] == "receipts39":
            ordin = [r for r in dl(sec) if REC[r["label"]][1] == "ordinary"]
            exc = [r for r in dl(sec) if REC[r["label"]][1] != "ordinary"]
            t1, t2, t = row(sec, "TotalI")[c].value, row(sec, "TotalII")[c].value, row(sec, "Total")[c].value
            CHK.eq(out, f"{where(sec)} {c}: Total du Titre Ier = ordinary lines",
                   ssum(r["cells"][c].value for r in ordin), t1)
            CHK.eq(out, f"{where(sec)} {c}: Total du Titre II = exceptional lines",
                   ssum(r["cells"][c].value for r in exc), t2)
            CHK.eq(out, f"{where(sec)} {c}: Total général = Titre Ier + Titre II", ssum([t1, t2]), t)
        else:
            CHK.eq(out, f"{where(sec)} {c}: Total général = sum of the lines",
                   ssum(r["cells"][c].value for r in dl(sec)), row(sec, "Total")[c].value)


# ----------------------------------------------------------------- selection (rule 4)

def select(recs, key):
    """Rule 4: latest edition printing the cell (a legible, aligned printing first)."""
    by = defaultdict(list)
    for r in recs:
        by[tuple(r[k] for k in key)].append(r)
    kept, n, diffs = [], 0, []
    for k, rs in by.items():
        rs.sort(key=lambda r: ORDER.index(r["census"]))
        legible = [r for r in rs if r["value"] is not None]
        aligned = [r for r in legible if r["flag"] != "row_realigned"]
        last = (aligned or legible or rs)[-1]
        for r in rs:
            if r is last or r["value"] is None:
                continue
            n += 1
            if r["value"] != last["value"]:
                diffs.append((k, r["census"], r["value"], last["census"], last["value"]))
        kept.append(last)
    return kept, n, diffs


def select_all(recs, key):
    """Rule 5: every edition kept."""
    return list(recs), 0, []


# ----------------------------------------------------------------- documentation

DOC = {
    "census": "edition the value is taken from (rule 4 tables: the latest edition printing that year)",
    "table_id": "transcription section",
    "gallica_ark": "Gallica volume ark (views are numbered within a volume)",
    "source_page": "printed page number",
    "gallica_view": "Gallica view (fNNNN)",
    "year": "budget year (exercice) as printed in the column head",
    "exercice_months": "length of the exercice in months: 9 for 1932 (printed \"1932 (9 mois)\" in sgt1935, the "
                       "transition to the April-March budget year), 12 otherwise (printed \"(12 mois)\" for 1933 "
                       "and 1934 in sgt1935, not printed elsewhere)",
    "basis": "`actual` (réalisations: realised receipts, expenditure as finally settled); the chapter prints no "
             "budget forecasts (prévisions)",
    "basis_fr": "printed table subtitle",
    "part": "`ordinary` (Titre premier / Première partie), `exceptional` (Titre II / Deuxième partie), `closed` "
            "(Titre III / Troisième partie: exercices clos et périmés)",
    "part_fr": "printed part heading",
    "item": "budget line code (English). Expenditure: `<part>_<service>`, stable across the renumbering of the "
            "chapters (1932, 1938)",
    "item_fr": "printed line label, with the chapter number of that edition's nomenclature",
    "nomenclature_fr": "nomenclature named in the table head of the printing the value comes from",
    "unit": "unit of `value`",
    "value": "printed amount (» = 0), francs with centimes",
    "flag": "empty, or `ocr_corrected` (image reading differs from the Gallica OCR)",
}

RULE4 = ("Printed for overlapping windows of exercices: each exercice is taken from the **latest** edition that "
         "prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on "
         "its own page image, is compared below.")

BUDGET_FAILS = (
    "Printed errors (each failing figure re-read on zoomed native-resolution crops; the same standing type was "
    "reused from sgt1925 to sgt1930, so the same errors recur in every printing): receipts 1918 total "
    "115.996.425 65 for lines summing to 110.996.425 65 (5.000.000 more; Chapitre II is printed 31.131.869 63 in "
    "every edition); 1919 total 159.571.187 15 for 159.571.097 15 (90); 1920 total 230.414.262 05 for "
    "230.414.265 05 (-3); 1923 total 273.494.795 97 for 273.424.795 97 (70.000). sgt1929 prints 1927 Produits divers "
    "14.055.295 30 (sgt1928 and sgt1930: 14.055.235 30, which the total requires; kept from sgt1930). Expenditure "
    "1920 total 247.894.268 84 for 247.894.258 84 (10); 1921 total 323.893.637 49 for 323.893.837 09 (-199,60); 1922 "
    "total 358.708.699 43 for 358.708.657 43 (42); 1923 total 316.939.974 19 for 316.939.974 22 (-0,03); sgt1939 "
    "1936 total 728.768.074 68 for 729.768.074 68 (-1.000.000; only printing). The faulty cell cannot be "
    "identified in any of these (the line items agree across all independent printings), so no cell is flagged "
    "`total_mismatch`.")

TABLES = {
    "finance_budget_receipts": dict(
        secs=["receipts", "receipts39"], cells=cells_budget, key=["year", "item"], select=select,
        dims=["exercice_months", "basis", "basis_fr", "part", "part_fr", "item", "item_fr", "nomenclature_fr",
              "unit"],
        title_fr="Budget annuel. a) Recettes réalisées",
        title_en="Annual budget of the Regency: realised receipts by budget chapter (exercices 1915-1938)",
        unit="Unit: francs (centimes kept); value_type: francs.",
        rule=RULE4,
        paras=["Printed sgt1925-sgt1939 (not in sgt1922-sgt1924): ten exercices per edition up to sgt1930 (sgt1925: "
               "1915-1924, ..., sgt1930: 1920-1929), three from sgt1935 (1932-1934, 1933-1935, 1936-1938). Exercices "
               "1930 and 1931 are printed in no edition of the series (sgt1931-sgt1934 are not in the collection). "
               "Lines: Titre I (Première partie up to sgt1927) ressources ordinaires, chapitres I-V; Titre II "
               "recettes sur ressources exceptionnelles (fonds d'emprunt, recettes diverses, and recettes à la "
               "disposition des Conseils de Région, sgt1925-sgt1930); Titre III recettes affectées aux dépenses des "
               "exercices clos et périmés (» in every printing). sgt1939 uses a new detailed nomenclature for the "
               "ordinary resources (17 lines, by tax) and prints Total du Titre Ier and Total du Titre II "
               "(checks only); its exercices 1936-1938 overlap no other printing.",
               "All figures are actual results (réalisations); the chapter prints no forecasts. The printed Total "
               "général is a check, not stored."]),
    "finance_budget_expenditure": dict(
        secs=["expenditure"], cells=cells_budget, key=["year", "item"], select=select,
        dims=["exercice_months", "basis", "basis_fr", "part", "part_fr", "item", "item_fr", "nomenclature_fr",
              "unit"],
        title_fr="Budget annuel. b) Dépenses : droits constatés définitivement liquidés lors des règlements des "
                 "budgets des exercices",
        title_en="Annual budget of the Regency: expenditure as finally settled, by service (exercices 1915-1938)",
        unit="Unit: francs (centimes kept); value_type: francs.",
        rule=RULE4,
        paras=["Printed sgt1925-sgt1939, same windows as the receipts. Lines: Titre I dépenses sur ressources "
               "ordinaires and Titre II dépenses sur ressources exceptionnelles ou spéciales, by service (chapitre), "
               "and Titre III dépenses des exercices clos et périmés. The chapters are renumbered twice: nomenclature "
               "1926-1929 (I Finances, II Postes et Télégraphes, III Intérieur, IV Agriculture-Commerce-"
               "Colonisation, V Instruction publique, VI Armée, VII Travaux publics, VIII Justice, IX Dépenses "
               "imprévues, from the 1927 nomenclature X Dépenses d'outillage économique), nomenclature 1932 and 1935 "
               "(II Secrétariat général du Gouvernement tunisien, VIII Justice tunisienne, IX Postes, X imprévues; "
               "from 1935 IV is the Direction des Affaires Économiques) and 1938 (III Postes; Intérieur and "
               "Administration tunisienne as \"Mémoire\" lines with 1936 figures only). `item` names the service, "
               "so the same service keeps its code across renumberings; `item_fr` keeps the printed chapter "
               "number. The Affaires Économiques line is coded with the Agriculture line it replaces "
               "(`agriculture_economy`).",
               "All figures are actual results; the printed Total général is a check, not stored."]),
}

SURVEY = {
    "sgt1922": "f185 chapter X title (Finances); f186 blank; f187 taxe personnelle (contribuables imposés by caïdat "
               "and nationality); f188-f211 achour: superficies ensemencées by caïdat and yield class, for blé, "
               "orge, avoine, fèves, pois chiches, maïs, sorgho, lin, each in three tables a) européens, b) "
               "indigènes, c) récapitulation (one page each); f212|f213 canoun des dattiers a) relevé par caïdat du "
               "nombre d'arbres d'après leur âge au 1er novembre 1922; f214|f215 b) répartition des arbres "
               "imposables par catégorie du tarif (degla, communs); f216|f217 canoun des oliviers a) relevé par "
               "caïdat d'après l'âge; f218|f219 b) répartition par catégorie du tarif; f220|f221 c) répartition "
               "entre européens et indigènes (arbres, articles de matrice, comptes individuels); f222|f223 droit de "
               "patente (état des assujettis by class of profit); f224|f225 taxe sur le bétail a) rôles européens "
               "(by caïdat and species, imposables / non imposables); f226|f227 b) rôles indigènes; f228|f229 c) "
               "récapitulation; f230 blank. f231 = chapter XI Agriculture.",
    "sgt1923": "f675 title; f676 blank; f677 taxe personnelle; f678-f701 achour (8 crops x a/b/c); f702|f703 canoun "
               "dattiers a) (1923); f704|f705 b); f706|f707 canoun oliviers a); f708 blank (verso); f709 b) "
               "(second page); f710|f711 c); f712|f713 droit de patente; f714|f715 bétail a); f716|f717 b); "
               "f718|f719 c); f720 blank. f721 = chapter XI.",
    "sgt1924": "f1171 title; f1172 blank; f1173 taxe personnelle; f1174-f1197 achour (8 crops x a/b/c); f1198|f1199 "
               "canoun dattiers a) (1924); f1200|f1201 b); f1202|f1203 canoun oliviers a); f1204|f1205 b); "
               "f1206|f1207 c); f1208|f1209 droit de patente; f1210|f1211 bétail a); f1212|f1213 b); f1214|f1215 "
               "c); f1216 blank. f1217 = chapter XI.",
    "sgt1925": "f211 title; f212|f213 budget annuel (1915-1924) a) recettes réalisées [transcribed]; f214|f215 b) "
               "dépenses [transcribed]; f216 dette tunisienne (récapitulatif et balance des opérations 1884-1921); "
               "f217 blank; f218|f219 taxe personnelle (by région, contrôle civil, caïdat and nationality); "
               "f220-f267 achour, 8 crops x a) européens, b) indigènes, c) récapitulation, each a two-page spread "
               "(by région / contrôle civil / caïdat); f268|f269 canoun dattiers a) (1924); f270|f271 b); f272|f273 "
               "canoun oliviers a) (1925); f274|f275 b); f276|f277 c); f278|f279 droit de patente; f280|f281 "
               "bétail a) européens; f282|f283 b) indigènes; f284|f285 c) récapitulation; f286 blank. f287 = "
               "chapter XI.",
    "sgt1926": "f767 title; f768|f769 budget (1916-1925) a) [transcribed]; f770|f771 b) [transcribed]; f772 dette "
               "tunisienne a) opérations 1884-1923 (b) balance); f773 blank; f774|f775 taxe personnelle; f776-f783 "
               "achour, one page per crop (a) blé ... h) lin), européens and indigènes in one table; f784|f785 canoun "
               "dattiers a); f786|f787 b); f788|f789 canoun oliviers a) (1926); f790|f791 b); f792|f793 c); "
               "f794|f795 droit de patente (bénéfices de 1925, imposés en 1926); f796|f797 bétail a); f798|f799 b); "
               "f800|f801 c); f802 blank. f803 = chapter XI.",
    "sgt1927": "f229 title; f230|f231 budget (1917-1926) a) [transcribed]; f232|f233 b) [transcribed]; f234 dette "
               "tunisienne (1884-1924); f235 blank; f236|f237 taxe personnelle; f238-f245 achour (one page per "
               "crop); f246|f247 canoun dattiers a) (1927); f248|f249 b); f250|f251 canoun oliviers a); f252|f253 "
               "b); f254|f255 c); f256|f257 droit de patente (1926 / 1927); f258 blank. f259 = chapter XI. No "
               "taxe sur le bétail from this edition.",
    "sgt1928": "f753 title; f754|f755 budget (1918-1927) a) [transcribed]; f756|f757 b) [transcribed]; f758 dette "
               "(1884-1924); f759 blank; f760|f761 taxe personnelle; f762-f769 achour; f770|f771 canoun dattiers "
               "a) (1928); f772|f773 b); f774|f775 canoun oliviers a); f776|f777 b); f778|f779 c); f780|f781 droit "
               "de patente (1927 / 1928); f782 blank. f783 = chapter XI.",
    "sgt1929": "f231 title; f232|f233 budget (1919-1928) a) [transcribed]; f234|f235 b) [transcribed]; f236 dette "
               "(1884-1925); f237 blank; f238|f239 taxe personnelle; f240-f247 achour; f248|f249 canoun dattiers "
               "a) (1929); f250|f251 b) (the f251 OCR also shows an européens / indigènes heading, to be checked on the image); f252|f253 canoun oliviers a); f254|f255 b); "
               "f256|f257 c); f258 blank; f259 droit de patente on a folding plate (1928 / 1929); f260 back of the "
               "plate. f261 = chapter XI.",
    "sgt1930": "f765 title; f766|f767 budget (1920-1929) a) [transcribed]; f768|f769 b) [transcribed]; f770|f771 "
               "dette (1884-1927, two pages); f772|f773 taxe personnelle; f774-f781 achour; f782|f783 canoun "
               "dattiers a) (1930); f784|f785 b); f786|f787 canoun oliviers a); f788|f789 b); f790|f791 c); f792 "
               "and f793 droit de patente (folding plate, 1929 / 1930); f794 blank. f795 = chapter XI.",
    "sgt1935": "f127 chapter X title; f128 blank; f129 budget annuel (1932-1934) a) recettes réalisées "
               "[transcribed]; f130 b) dépenses [transcribed]; f131 dette tunisienne a) opérations 1884-1934; f132 "
               "b) balance des opérations; f133 achour (1935), superficies ensemencées par les Européens et les "
               "Tunisiens (all crops in one table); f134|f135 canoun des dattiers (1935); f136|f137 canoun des "
               "oliviers (1935); f138 droit de patente (bénéfices de 1934, imposés en 1935), by région, contrôle "
               "and caïdat. f139 = chapter XI.",
    "sgt1936": "f94 chapter IX title; f95 budget annuel (1933-1935) a) [transcribed]; f96 b) [transcribed]; f97 dette "
               "tunisienne (opérations 1884-1935); f98 balance des opérations; f99 droit de patente (1935 / 1936). "
               "f100 = chapter X Agriculture.",
    "sgt1939": "f93 chapter IX title; f94 budget annuel (1936-1938) a) [transcribed]; f95 b) [transcribed]; f96 dette "
               "tunisienne (1884-1938); f97 balance des opérations; f98 droit de patente (1938 / 1939). f99 = "
               "chapter X Agriculture.",
}

NOT_DONE = (
    "Transcribed so far: the two budget tables (finance_budget_receipts, finance_budget_expenditure), every "
    "printing (sgt1925-sgt1939), every cell read on native-resolution crops of the page images. Not yet "
    "transcribed (see the survey above for views): dette tunisienne (sgt1925-sgt1939), taxe personnelle "
    "(sgt1922-sgt1930), achour (sgt1922-sgt1935), canoun des dattiers and des oliviers (sgt1922-sgt1935), droit de "
    "patente (sgt1922-sgt1939), taxe sur le bétail (sgt1922-sgt1926). The chapter reprints neither the public "
    "assistance / health budgets nor the communal budgets.")


def write_survey():
    L = ["# Finances chapter: survey of every edition", "",
         "Survey of the *Finances* chapter (chapter X up to sgt1935, chapter IX in sgt1936 and sgt1939), view by "
         "view, from whole-page images of every view (page headings checked against the Gallica OCR). First and "
         "last views confirmed on the page images for every edition (chapter-title page, and the next chapter "
         "title Agriculture). Extraction: `extract_finance.py`.", "",
         "| edition | ark | views |", "|---|---|---|"]
    L += [f"| {e} | `{EDITIONS[e]}` | {a}–{b} |" for e, (a, b) in CHAPTER_VIEWS.items()]
    L += ["", "## Views per edition", "", "[transcribed] marks the views stored in a CSV.", ""]
    L += [f"- **{e}**: {t}" for e, t in SURVEY.items()]
    L += ["", "## Tables (CSV)", "", "| CSV | sections | editions and views | read on the image |",
          "|---|---|---|---|"]
    for o, sp in TABLES.items():
        L.append(f"| `{o}` | {', '.join(sp['secs'])} | " + "; ".join(
            f"{e} f{', f'.join(str(v) for v in sp['_views'][e])}" for e in sp.get("_eds", []))
            + " | every printing, cell by cell |")
    L += ["", "## Coverage", "", NOT_DONE, ""]
    (OUT / "finance_survey.md").write_text("\n".join(L) + "\n")


def build(write=True):
    secs = []
    for ed in ORDER:
        p = TR / f"{PREFIX}_{ed}.txt"
        if p.exists():
            secs += parse(p, ed)
    for s in secs:
        if s["table"] in ("receipts", "receipts39", "expenditure"):
            chk_budget(s)
    res = {}
    for out, spec in TABLES.items():
        ss = [s for s in secs if s["table"] in spec["secs"]]
        spec["_eds"] = [e for e in ORDER if any(s["ed"] == e for s in ss)]
        spec["_views"] = {e: sorted({s["view"] for s in ss if s["ed"] == e}) for e in spec["_eds"]}
        recs = []
        for s in ss:
            recs += spec["cells"](s)
        kept, n, diffs = spec["select"](recs, spec["key"])
        order = {id(r): i for i, r in enumerate(recs)}
        kept.sort(key=lambda r: (r["year"], order.get(id(r), 0)))
        flagged = [f"{r['census']} {r['year']} " + " / ".join(str(r.get(k, "")) for k in spec["key"][1:])
                   + f" = {r['value']} ({r['flag']})" for r in kept if r["flag"]]
        res[out] = dict(rows=len(kept), checks=CHK.n[out], failed=list(CHK.fail[out]), overlap_compared=n,
                        overlap_diffs=[list(x) for x in diffs], flagged=flagged, editions=spec["_eds"],
                        read_on_image={e: "every cell, native-resolution crops" for e in spec["_eds"]})
        if write:
            cols = COMMON + spec["dims"] + ["value", "flag"]
            write_csv(out, cols, kept)
            expl = [BUDGET_FAILS] if CHK.fail[out] else []
            paras = list(spec.get("paras", [])) + expl + [
                "Survey of the whole chapter in every edition: `finance_survey.md`."]
            write_notes(out, CHAPTER, SCRIPT, kept, cols, {c: DOC[c] for c in cols}, spec["title_fr"],
                        spec["title_en"], paras, CHK.n[out], CHK.fail[out], n, diffs, coverage_lines(ss),
                        spec["rule"], spec["unit"])
    if write:
        write_validation(OUT / f"{PREFIX}_validation.json", dict(
            res, _chapter_views=CHAPTER_VIEWS, _survey=SURVEY, _not_transcribed=NOT_DONE))
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
