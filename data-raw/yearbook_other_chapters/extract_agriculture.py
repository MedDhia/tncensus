#!/usr/bin/env python3
"""Agriculture chapter (*Agriculture*: chapter XI up to sgt1935, chapter X in sgt1936 and sgt1939) of the
Statistique générale de la Tunisie, 12 editions sgt1922-sgt1939.

  python3 extract_agriculture.py check   parse the transcriptions, run every check, print failures
  python3 extract_agriculture.py build   ... and write csv/agriculture_*.csv, their .md notes,
                                         csv/agriculture_survey.md and csv/agriculture_validation.json

Source of truth: transcribed/agriculture_<edition>.txt (format in yb_tables.py). Yearly series printed for
overlapping windows (cultures diverses) follow SPEC_ADDENDUM rule 4 (each year from the latest edition printing
it, every other printing compared cell by cell); tables printed once per edition follow rule 5.
"""
import sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path as _Path

sys.path.insert(0, str(_Path(__file__).resolve().parent))  # shared helper yb_tables.py
from yb_tables import (COMMON, EDITIONS, ORDER, OUT, TR, Checks, coverage_lines, parse, ssum, where,  # noqa: E402
                       write_csv, write_notes, write_validation)

CHAPTER = "Agriculture"
SCRIPT = "extract_agriculture.py"
PREFIX = "agriculture"

# Views of the chapter (chapter title .. last view before the next chapter), confirmed on the page images.
CHAPTER_VIEWS = {
    "sgt1922": (231, 280), "sgt1923": (721, 770), "sgt1924": (1217, 1274), "sgt1925": (287, 342),
    "sgt1926": (803, 852), "sgt1927": (259, 314), "sgt1928": (783, 842), "sgt1929": (261, 320),
    "sgt1930": (795, 856), "sgt1935": (139, 154), "sgt1936": (100, 115), "sgt1939": (99, 114),
}

CHK = Checks()

# Cells whose flag is not expressible in the transcription tokens: (edition, section, line, column) -> flag.
FLAGS = {
    ("sgt1922", "land_d", "fallow", "ha"): "total_mismatch",
    ("sgt1936", "land_d", "fallow", "ha"): "total_mismatch",
    ("sgt1936", "land_b", "productive", "ha"): "derived_from_totals",
    ("sgt1923", "land_c", "rangeland", "pct"): "total_mismatch",
    ("sgt1927", "land_d", "fodder", "pct"): "total_mismatch",
    ("sgt1928", "land_b", "Total", "pct"): "total_mismatch",
    ("sgt1929", "land_b", "Total", "pct"): "total_mismatch",
    ("sgt1926", "crops_d", "otherdates_prod", "1925"): "derived_from_totals",
    ("sgt1928", "crops_d", "otherdates_prod", "1925"): "derived_from_totals",
    ("sgt1929", "crops_d", "otherdates_prod", "1925"): "derived_from_totals",
    ("sgt1930", "crops_d", "otherdates_prod", "1925"): "derived_from_totals",
    ("sgt1930", "crops_d", "orange_trees", "1930"): "total_mismatch",
    ("sgt1930", "zones", "barley_N_prod", "1930"): "total_mismatch",
    ("sgt1925", "crops_a:north", "durum_area", "1925"): "total_mismatch",
    # principales cultures by yield class: cells identified as the faulty one of a failed check (every printing
    # of the cell, "*"; reasons in TABLES["agriculture_yield_classes"]["fail_note"])
    ("*", "classes:wheat", "1915_ind", "c3"): "total_mismatch",
    ("*", "classes:wheat", "1919_ind", "r4"): "total_mismatch",
    ("*", "classes:wheat", "1923_eur", "r1"): "total_mismatch",
    ("*", "classes:barley", "1916_eur", "r6"): "total_mismatch",
    ("*", "classes:barley", "1918_ind", "c4"): "total_mismatch",
    ("*", "classes:barley", "1921_ind", "r6"): "total_mismatch",
    ("*", "classes:oats", "1919_eur", "r3"): "total_mismatch",
    ("*", "classes:oats", "1919_ind", "c3"): "total_mismatch",
    ("*", "classes:maize", "1919_eur", "r1"): "total_mismatch",
    ("*", "classes:maize", "1922_ind", "r2"): "total_mismatch",
    ("*", "classes:maize", "1923_eur", "r6"): "total_mismatch",
    ("*", "classes:sorghum", "1919_eur", "r4"): "total_mismatch",
    ("*", "classes:sorghum", "1919_ind", "r2"): "total_mismatch",
    ("*", "classes:beans", "1919_ind", "c6"): "total_mismatch",
    ("*", "classes:beans", "1920_eur", "r1"): "total_mismatch",
    ("*", "classes:chickpeas", "1920_eur", "c1"): "total_mismatch",
    ("*", "classes:chickpeas", "1921_eur", "r3"): "total_mismatch",
    ("*", "classes:chickpeas", "1921_ind", "r6"): "total_mismatch",
    ("*", "classes:flax", "1921_ind", "r1"): "total_mismatch",
    ("*", "classes:flax", "1923_eur", "r1"): "total_mismatch",
    ("*", "classes:flax", "1923_ind", "r1"): "total_mismatch",
    ("sgt1923", "surfaces:oats", "sown", "1922"): "row_realigned",
    ("sgt1923", "surfaces:oats", "taxed", "1922"): "row_realigned",
    ("sgt1923", "surfaces:oats", "untaxed_low", "1922"): "row_realigned",
    ("sgt1923", "surfaces:oats", "untaxed_new", "1922"): "row_realigned",
    ("sgt1923", "surfaces:oats", "sown", "1923"): "row_realigned",
    ("sgt1923", "surfaces:oats", "taxed", "1923"): "row_realigned",
    ("sgt1923", "surfaces:oats", "untaxed_low", "1923"): "row_realigned",
    ("sgt1923", "surfaces:oats", "untaxed_new", "1923"): "row_realigned",
    ("sgt1925", "zclasses:wheat:north", "1925_ind", "h6"): "total_mismatch",
    ("sgt1925", "zclasses:wheat:centre_south", "1922_ind", "p6"): "total_mismatch",
    ("sgt1925", "zclasses:oats:north", "1922_ind", "p6"): "total_mismatch",
    ("sgt1925", "zclasses:oats:north", "1925_ind", "h6"): "total_mismatch",
    ("sgt1922", "vine", "Sfax", "it_ha"): "total_mismatch",
    ("sgt1922", "vine", "Tabarka", "it_ha"): "total_mismatch",
    ("sgt1923", "olive", "Skhira (La)", "unprod"): "total_mismatch",
    ("sgt1924", "olive", "Ouled-Aoun", "unprod"): "total_mismatch",
    ("sgt1930", "olive", "1re Région / Bizerte / Bizerte / Bizerte", "taxed"): "total_mismatch",
    ("sgt1929", "olive", "2me Région / Tunis / Grombalia / Cap-Bon > Nabeul", "taxed"): "total_mismatch",
    ("sgt1929", "olive", "4me Région / Sousse / Sousse / Mahdia", "young"): "total_mismatch",
    ("sgt1929", "olive", "4me Région / Sousse / Kairouan / Djelass", "young"): "total_mismatch",
    ("sgt1929", "olive", "5me Région / Sfax / Sfax / Djebéniane", "unprod"): "total_mismatch",
    ("sgt1929", "olive", "5me Région / Sfax / Gafsa / Hammama", "young"): "total_mismatch",
    ("sgt1928", "olive", "1re Région / Bizerte / Bizerte / Mateur", "young"): "total_mismatch",
    ("sgt1928", "olive", "1re Région / Bizerte / Souk-el-Arba / Souk-el-Arba", "unprod"): "total_mismatch",
    ("sgt1928", "olive", "1re Région / Bizerte / Souk-el-Arba / Souk-el-Arba", "taxed"): "total_mismatch",
    ("sgt1928", "olive", "3me Région / Le Kef / Téboursouk / Téboursouk", "taxed"): "total_mismatch",
    ("sgt1928", "olive", "3me Région / Le Kef / Maktar / Oulad Ayar", "taxed"): "total_mismatch",
    ("sgt1927", "olive", "3me Région / Le Kef / Maktar / Oulad Ayar", "taxed"): "total_mismatch",
    ("sgt1927", "olive", "4me Région / Sousse / Sousse / Mahdia", "taxed"): "total_mismatch",
    ("sgt1927", "olive", "4me Région / Sousse / Sousse / Sousse", "young"): "total_mismatch",
    ("sgt1927", "olive", "5me Région / Sfax / Tozeur / Djerid", "taxed"): "total_mismatch",
}


def flag_of(sec, label, col, cell):
    t = sec["table"] + (":" + sec["crop"] if sec.get("crop") else "") + (":" + sec["zone"] if sec.get("zone") else "")
    return FLAGS.get((sec["ed"], t, label, col)) or FLAGS.get(("*", t, label, col), cell.flag)


def dl(sec):
    return [r for r in sec["rows"] if "cells" in r and r["label"] not in ("Total", "Totaux")]


def row(sec, label):
    for r in sec["rows"]:
        if r["label"] == label:
            return r["cells"]
    return None


def base(sec, year):
    return {"census": sec["ed"], "table_id": sec["table"], "gallica_ark": sec["ark"], "source_page": sec["page"],
            "gallica_view": sec["view"], "year": year}


# ----------------------------------------------------------------- land (superficie)

LAND_ITEM = {
    "area_km2": ("a", "territorial_area", "Superficie territoriale", "km2"),
    "inhabitants": ("a", "inhabitants", "Habitants", "persons"),
    "density": ("a", "density", "Densité de la population par kilomètre carré", "persons_per_km2"),
    "productive": ("b", "productive", "Superficie productive cultivée et non cultivée", None),
    "unproductive": ("b", "unproductive", "Superficie improductive", None),
    "arable": ("c", "arable_land", "Terres labourables", None),
    "meadows": ("c", "natural_meadows_pasture", "Prairies naturelles et pâturages", None),
    "tree_crops": ("c", "tree_and_shrub_crops", "Cultures arborescentes et arbustives", None),
    "forest": ("c", "woods_forests", "Bois et forêts", None),
    "rangeland": ("c", "rangeland_uncultivated", "Terres de parcours et terres non cultivées productives", None),
    "cereals": ("d", "cereals", "Céréales", None),
    "fodder": ("d", "artificial_meadows_fodder", "Prairies artificielles et autres cultures fourragères", None),
    "food_plants": ("d", "food_plants", "Plantes alimentaires", None),
    "industrial_plants": ("d", "industrial_plants", "Plantes industrielles", None),
    "other_products": ("d", "other_products", "Productions diverses", None),
    "fallow": ("d", "fallow_grazed", "Jachères champs pâturés", None),
}
LAND_PART = {"a": "Superficie territoriale", "b": "Répartition en superficie productive et improductive",
             "c": "Répartition de la superficie productive", "d": "Répartition de la superficie labourable"}
LAND_TOTAL = {"b": "territoriale", "c": "productive", "d": "labourable"}


def cells_land(sec):
    out = []
    part = sec["table"][-1]
    for r in dl(sec):
        p, item, item_fr, unit = LAND_ITEM[r["label"]]
        for c in sec["cols"]:
            cell = r["cells"][c]
            if c == "value":
                m, mfr, u = "value", "", unit
            elif c == "ha":
                m, mfr, u = "area", "Hectares", "hectares"
            else:
                m, mfr, u = "percent", f"% de la superficie {LAND_TOTAL[part]}", "percent"
            out.append(dict(base(sec, int(sec["year"])), part=part, part_fr=LAND_PART[part], item=item,
                            item_fr=item_fr, measure=m, measure_fr=mfr, unit=u, value=cell.value,
                            flag=flag_of(sec, r["label"], c, cell)))
    return out


def chk_land(sec):
    out = "agriculture_land"
    if sec["table"] == "land_a":
        return
    rows = dl(sec)
    t = row(sec, "Total")
    CHK.eq(out, f"{where(sec)} hectares: parts vs total", ssum(r["cells"]["ha"].value for r in rows), t["ha"].value)
    CHK.eq(out, f"{where(sec)} %: parts vs 100", ssum(r["cells"]["pct"].value for r in rows), Decimal(100),
           tol=Decimal("0.2"))
    CHK.eq(out, f"{where(sec)} % of the total line", t["pct"].value, Decimal(100))
    for r in rows:
        ha, pct = r["cells"]["ha"].value, r["cells"]["pct"].value
        got = (ha * 100 / t["ha"].value).quantize(Decimal("0.01"))
        CHK.eq(out, f"{where(sec)} {r['label']}: % = hectares / total", got, pct, tol=Decimal("0.15"))


# ----------------------------------------------------------------- crops (cultures diverses)

CROP = {  # code: (crop, crop_fr, group)
    "wheat": ("wheat", "Blé dur et blé tendre (accolade)", "a"),
    "durum": ("durum_wheat", "Blé dur", "a"), "soft": ("soft_wheat", "Blé tendre", "a"),
    "barley": ("barley", "Orge", "a"), "oats": ("oats", "Avoine", "a"),
    "maize": ("maize_sorghum", "Maïs et sorgho", "a"),
    "beans": ("broad_beans", "Fèves", "b"), "chickpeas": ("chickpeas", "Pois chiches", "b"),
    "potatoes": ("potatoes", "Pommes de terre", "b"),
    "flax": ("flax", "Lin", "c"), "tobacco": ("tobacco", "Tabac", "c"),
    "vine": ("vine", "Vigne", "d"), "olive": ("olive", "Oliviers", "d"), "carob": ("carob", "Caroubiers", "d"),
    "almond": ("almond", "Amandiers", "d"), "degla": ("dates_degla", "Dattiers Dégla", "d"),
    "otherdates": ("dates_other", "Dattiers autres", "d"), "orange": ("orange", "Orangers", "d"),
    "lemon": ("lemon", "Citronniers", "d"),
    "peaschickpeas": ("peas_chickpeas", "Pois et pois chiches", "b"),
    "commondates": ("dates_other", "Dattiers communes", "d"),
    "fig": ("fig", "Figuiers", "d"), "mandarin": ("mandarin", "Mandariniers", "d"),
    "apricot": ("apricot", "Abricotiers", "d"), "quince": ("quince", "Cognassiers", "d"),
    "pomegranate": ("pomegranate", "Grenadiers", "d"), "peach": ("peach", "Pêchers", "d"),
    "pear": ("pear", "Poiriers", "d"), "apple": ("apple", "Pommiers", "d"), "plum": ("plum", "Pruniers", "d"),
}
CROP_GROUP = {"a": "Céréales", "b": "Autres plantes alimentaires", "c": "Plantes industrielles",
              "d": "Plantes arbustives"}
MEASURE = {  # suffix: (measure, measure_fr, unit)
    "area": ("area", "Surface", "hectares"),
    "prod": ("production", "Production", "quintals"),
    "yield": ("yield_per_hectare", "Rendement à l'hectare", "quintals_per_hectare"),
    "wine": ("wine_production", "Production : vin", "hectolitres"),
    "grapes": ("table_grape_production", "Production : raisins de table", "quintals"),
    "trees": ("trees", "Nombre (pieds)", "trees"),
    "bearing": ("trees_bearing", "En production (pieds)", "trees"),
    "oil": ("olive_oil_production", "Production en huile d'olive", "quintals"),
    "pomace": ("pomace_oil_production", "Production en huile de grignons", "quintals"),
    "treestotal": ("trees", "Nombre total (pieds)", "trees"),
    "young": ("trees_young", "Nombre : jeunes (pieds)", "trees"),
}
MEASURE_CROP = {("vine", "yield"): ("yield_per_hectare", "Rendement à l'hectare (en vin)", "hectolitres_per_hectare"),
                ("degla", "trees"): ("trees_taxable", "Pieds (1) : pieds imposables", "trees"),
                ("commondates", "trees"): ("trees_taxable", "Nombre imposable (pieds)", "trees")}


ZONE = {"tunisia": "Tunisie (ensemble)",
        "north": "Tunisie septentrionale et Hauts plateaux (1re, 2e et 3e Régions)",
        "centre_south": "Tunisie centrale et méridionale (4e et 5e Régions et Territoires militaires)"}


def crop_meta(label):
    code, suf = label.rsplit("_", 1)
    crop, crop_fr, g = CROP[code]
    m = MEASURE_CROP.get((code, suf)) or MEASURE[suf]
    return dict(crop_group=g, crop_group_fr=CROP_GROUP[g], crop=crop, crop_fr=crop_fr, measure=m[0],
                measure_fr=m[1], unit=m[2])


def cells_crops(sec):
    out = []
    for r in dl(sec):
        meta = crop_meta(r["label"])
        for c in sec["cols"]:
            if c.startswith("m"):
                continue           # printed averages: checks only
            cell = r["cells"][c]
            if cell.flag == "not_applicable":
                continue           # nothing printed (bracketed figure stored on the group line)
            z = sec.get("zone", "tunisia")
            out.append(dict(base(sec, int(c)), zone=z, zone_fr=ZONE[z], **meta, value=cell.value,
                            flag=flag_of(sec, r["label"], c, cell)))
    return out


def chk_crops_all(secs):
    """Printed averages (m<a>_<b> columns) against the mean of the years, across the two pages of a spread."""
    out = "agriculture_crops"
    by = defaultdict(dict)    # (ed, table, label) -> {year/m-col: value}
    secof = {}
    for s in secs:
        for r in dl(s):
            for c in s["cols"]:
                by[(s["ed"], s["table"] + s.get("zone", ""), r["label"])][c] = r["cells"][c].value
                secof[(s["ed"], s["table"] + s.get("zone", ""), r["label"], c)] = s
    for (ed, t, label), d in by.items():
        code, suf = label.rsplit("_", 1)
        for c, printed in d.items():
            if not c.startswith("m") or printed is None:
                continue
            a, b = map(int, c[1:].split("_"))
            yrs = [str(y) for y in range(a, b + 1)]
            vals = []
            for y in yrs:
                v = d.get(y)
                if v is None and code in ("durum",) and (ed, t, f"wheat_{suf}") in by:
                    v = by[(ed, t, f"wheat_{suf}")].get(y)
                vals.append(v)
            if any(v is None for v in vals):
                continue
            if suf == "yield":
                continue           # averages of yields are ratios of the averages, not means
            got = sum(vals, Decimal(0)) / len(vals)
            tol = max(Decimal(1), abs(printed) * Decimal("0.002"))
            CHK.eq(out, f"{where(secof[(ed, t, label, c)])} {label}: average {a}-{b}", got.quantize(Decimal("0.01")),
                   printed, tol=tol)


def chk_crops(sec):
    """Printed yield per hectare against production / area (to 5 %, half a unit of the last printed digit)."""
    out = "agriculture_crops"
    for r in dl(sec):
        code, suf = r["label"].rsplit("_", 1)
        if suf != "yield" or code == "vine":
            continue           # vine yield: computed on the vineyard over 3 years old (footnote), not checkable
        num = row(sec, f"{code}_wine" if code == "vine" else f"{code}_prod")
        den = row(sec, f"{code}_area")
        for c in sec["cols"]:
            if c.startswith("m"):
                continue
            y, p, a = r["cells"][c].value, num[c].value, den[c].value
            if None in (y, p, a) or a == 0 or y == 0:
                continue
            got = (p / a).quantize(Decimal("0.01"))
            CHK.eq(out, f"{where(sec)} {r['label']} {c}: yield = production / area", got, y,
                   tol=max(Decimal("0.11"), y * Decimal("0.05")))


# ----------------------------------------------------------------- cereal yields by zone

ZCROP = {"durum": ("durum_wheat", "Blé dur"), "soft": ("soft_wheat", "Blé tendre"), "barley": ("barley", "Orge"),
         "oats": ("oats", "Avoine")}
ZZONE = {"N": ("north", "Nord"), "C": ("centre", "Centre"), "S": ("south", "Sud"),
         "CS": ("centre_south", "Centre et Sud")}
ZMEAS = {"area": ("area", "Surface", "hectares"), "prod": ("production", "Production", "quintals"),
         "yield": ("yield_per_hectare", "Rendement à l'hectare", "quintals_per_hectare")}


def cells_zones(sec):
    out = []
    for r in dl(sec):
        c0, z, m = r["label"].split("_")
        crop, crop_fr = ZCROP[c0]
        zone, zone_fr = ZZONE[z]
        meas, meas_fr, unit = ZMEAS[m]
        for c in sec["cols"]:
            if c.startswith("m"):
                continue
            cell = r["cells"][c]
            if cell.flag == "not_applicable":
                continue
            out.append(dict(base(sec, int(c)), crop=crop, crop_fr=crop_fr, zone=zone, zone_fr=zone_fr,
                            measure=meas, measure_fr=meas_fr, unit=unit, value=cell.value,
                            flag=flag_of(sec, r["label"], c, cell)))
    return out


def chk_zones(sec):
    out = "agriculture_cereal_zones"
    for r in dl(sec):
        c0, z, m = r["label"].split("_")
        if m != "yield":
            continue
        p, a = row(sec, f"{c0}_{z}_prod"), row(sec, f"{c0}_{z}_area")
        for c in sec["cols"]:
            if c.startswith("m"):
                continue
            y, pv, av = r["cells"][c].value, p[c].value, a[c].value
            if None in (y, pv, av) or av == 0:
                continue
            CHK.eq(out, f"{where(sec)} {r['label']} {c}: yield = production / area", (pv / av).quantize(
                Decimal("0.01")), y, tol=max(Decimal("0.11"), y * Decimal("0.05")))


def chk_zones_all(secs):
    out = "agriculture_cereal_zones"
    by, secof = defaultdict(dict), {}
    for s in secs:
        for r in dl(s):
            for c in s["cols"]:
                by[(s["ed"], r["label"])][c] = r["cells"][c].value
                secof[(s["ed"], r["label"], c)] = s
    for (ed, label), d in by.items():
        if label.endswith("_yield"):
            continue
        for c, printed in d.items():
            if not c.startswith("m") or printed is None:
                continue
            a, b = map(int, c[1:].split("_"))
            vals = [d.get(str(y)) for y in range(a, b + 1)]
            if any(v is None for v in vals):
                continue
            got = sum(vals, Decimal(0)) / len(vals)
            CHK.eq(out, f"{where(secof[(ed, label, c)])} {label}: average {a}-{b}", got.quantize(Decimal("0.01")),
                   printed, tol=max(Decimal(1), abs(printed) * Decimal("0.002")))



# ----------------------------------------------------------------- principales cultures by yield class (sgt1922-1925)

YC_CROP = {"wheat": ("wheat", "Blé"), "durum": ("durum_wheat", "Blé dur"), "soft": ("soft_wheat", "Blé tendre"),
           "barley": ("barley", "Orge"), "oats": ("oats", "Avoine"), "beans": ("broad_beans", "Fèves"),
           "maize": ("maize", "Maïs"), "sorghum": ("sorghum", "Sorgho"), "chickpeas": ("chickpeas", "Pois chiches"),
           "flax": ("flax", "Lin")}
YC_SURF = {"sown": ("sown", "Surfaces ensemencées"),
           "taxed": ("taxed", "Surfaces imposées (d'un rendement supérieur à 1 hectolitre)"),
           "untaxed_low": ("untaxed_low_yield", "Surfaces non imposées (d'un rendement inférieur à 1 hectolitre)"),
           "untaxed_new": ("untaxed_new_land", "Surfaces non imposées (ensemencées sur terres nouvellement "
                                               "défrichées)")}
YC_CLASS = {f"c{k}": (f"yield_{k}_hl", f"{k} hectolitre" + ("s" if k > 1 else "")) for k in range(1, 6)}
YC_CLASS["c6"] = ("yield_6_hl_plus", "6 hectolitres et au-dessus")
YC_FARM = {"eur": ("european", "Européens"), "ind": ("indigenous", "Indigènes")}
YC_ZONE = {"tunisia": "Tunisie (ensemble)", **{k: v for k, v in ZONE.items() if k != "tunisia"}}


def yc_zone(sec):
    z = sec.get("zone", "tunisia")
    return dict(zone=z, zone_fr=YC_ZONE[z])


def cells_yc(sec):
    out = []
    crop, crop_fr = YC_CROP[sec["crop"]]
    if sec["table"] == "surfaces":
        for r in sec["rows"]:
            cl, cl_fr = YC_SURF[r["label"]]
            for c in sec["cols"]:
                cell = r["cells"][c]
                out.append(dict(base(sec, int(c)), **yc_zone(sec), crop=crop, crop_fr=crop_fr, subtable="surfaces",
                                farmers="all", farmers_fr="", crop_year_fr="", area_class=cl, area_class_fr=cl_fr,
                                measure="area", measure_fr="Surfaces (h. a.)", unit="hectares", value=cell.value,
                                flag=flag_of(sec, r["label"], c, cell)))
        return out
    if sec["table"] == "zclasses":
        ZC = {"h05": ("yield_0_5_hl", "0 à 5 hectol.", "area", "Nombre d'hectares ayant produit", "hectares"),
              "p05": ("yield_0_5_hl", "0 à 5 hectol.", "percent_of_sown_area", "Rapport avec les surfaces "
                      "ensemencées (%)", "percent"),
              "h6": ("yield_6_hl_plus", "6 hectolitres et au-dessus", "area", "Nombre d'hectares ayant produit",
                     "hectares"),
              "p6": ("yield_6_hl_plus", "6 hectolitres et au-dessus", "percent_of_sown_area", "Rapport avec les "
                     "surfaces ensemencées (%)", "percent"),
              "sown": ("sown", "Surfaces ensemencées", "area", "Surfaces ensemencées", "hectares")}
        for r in sec["rows"]:
            y, g = r["label"].split("_")
            fa, fa_fr = YC_FARM[g]
            for c in sec["cols"]:
                cell = r["cells"][c]
                cl, cl_fr, m, mfr, u = ZC[c]
                out.append(dict(base(sec, int(y)), **yc_zone(sec), crop=crop, crop_fr=crop_fr,
                                subtable="surfaces" if c == "sown" else "yield_classes", farmers=fa,
                                farmers_fr=fa_fr + "s", crop_year_fr="", area_class=cl, area_class_fr=cl_fr,
                                measure=m, measure_fr=mfr, unit=u, value=cell.value,
                                flag=flag_of(sec, r["label"], c, cell)))
        return out
    for r in sec["rows"]:
        y, g = r["label"].split("_")
        if g == "tot":
            continue
        fa, fa_fr = YC_FARM[g]
        for c in sec["cols"]:
            if c == "tot":
                continue
            cell = r["cells"][c]
            cl, cl_fr = YC_CLASS["c" + c[1:]]
            if c.startswith("c"):
                m, mfr, u = "area", "Nombre d'hectares ayant produit (h. a.)", "hectares"
            else:
                m, mfr, u = "ratio_to_line_total", "Rapport avec les surfaces " + (
                    "ensemencées" if sec.get("rapport") == "ensemencees" else "imposées"), "ratio"
            out.append(dict(base(sec, int(y)), **yc_zone(sec), crop=crop, crop_fr=crop_fr, subtable="yield_classes",
                            farmers=fa, farmers_fr=fa_fr, crop_year_fr=f"{int(y) - 1}-{y}", area_class=cl,
                            area_class_fr=cl_fr, measure=m, measure_fr=mfr, unit=u, value=cell.value,
                            flag=flag_of(sec, r["label"], c, cell)))
    return out


def chk_yc_all(secs):
    """Per edition and crop (and zone): join the two pages of the spread, then check every printed total."""
    out = "agriculture_yield_classes"
    lines, surf, where_of = defaultdict(dict), defaultdict(dict), {}
    for s in [x for x in secs if x["table"] == "zclasses"]:
        for r in s["rows"]:
            d = {c: x.value for c, x in r["cells"].items()}
            w = f"{where(s)} {s['crop']} [{s['zone']}] {r['label']}"
            CHK.eq(out, f"{w}: 0-5 hl + 6 hl et au-dessus vs surfaces ensemencées", d["h05"] + d["h6"], d["sown"])
            CHK.eq(out, f"{w}: the two percentages vs 100", d["p05"] + d["p6"], Decimal(100), tol=Decimal("0.02"))
            for h, pc in (("h05", "p05"), ("h6", "p6")):
                CHK.eq(out, f"{w}: {pc} = {h} / surfaces ensemencées", (d[h] * 100 / d["sown"]).quantize(
                    Decimal("0.01")), d[pc], tol=Decimal("0.6") if d[pc] == d[pc].to_integral() else Decimal("0.02"))
    secs = [x for x in secs if x["table"] != "zclasses"]
    for s in secs:
        k = (s["ed"], s["crop"], s.get("zone", "tunisia"))
        for r in s["rows"]:
            for c in s["cols"]:
                if s["table"] == "surfaces":
                    surf[k].setdefault(c, {})[r["label"]] = r["cells"][c].value
                else:
                    lines[k].setdefault(r["label"], {})[c] = r["cells"][c].value
                where_of[(k, r["label"], c)] = s
    one = Decimal("0.0001")
    for k, ls in lines.items():
        w = lambda lab, c: where(where_of[(k, lab, c)]) + f" {k[1]}" + (f" [{k[2]}]" if k[2] != "tunisia" else "")
        for lab, d in ls.items():
            cs = [f"c{i}" for i in range(1, 7)]
            if all(c in d for c in cs + ["tot"]):
                CHK.eq(out, f"{w(lab, 'tot')} {lab}: classes vs TOTAUX", ssum(d[c] for c in cs), d["tot"])
                for i in range(1, 7):
                    if d["tot"] and d.get(f"r{i}") is not None and d[f"c{i}"] is not None:
                        x = d[f"c{i}"] / d["tot"]
                        p = d[f"r{i}"]
                        tol = max(Decimal("0.0005"), p * Decimal("0.01"))
                        ok = abs(x - p) <= tol
                        sc = ssum(d[c] for c in cs)
                        if not ok and sc:      # the printed TOTAUX itself may be the faulty cell
                            ok = abs(d[f"c{i}"] / sc - p) <= tol
                        CHK.n[out] += 1
                        if not ok:
                            CHK.fail[out].append(f"{w(lab, f'r{i}')} {lab} r{i}: c{i} / TOTAUX = "
                                                 f"{x.quantize(Decimal('0.00001'))}, printed {p}")
            y = lab.split("_")[0]
            if lab.endswith("_tot"):
                e, i_ = ls.get(f"{y}_eur"), ls.get(f"{y}_ind")
                for c in d:
                    if c.startswith("r") or e is None or i_ is None:
                        continue
                    CHK.eq(out, f"{w(lab, c)} {y} {c}: Européens + Indigènes vs TOTAUX", ssum([e[c], i_[c]]), d[c])
                sv = surf.get(k, {}).get(y)
                if sv and "tot" in d:
                    CHK.eq(out, f"{w(lab, 'tot')} {y}: TOTAUX vs surfaces imposées", d["tot"], sv["taxed"])
    for k, ys in surf.items():
        for y, d in ys.items():
            s = where_of[(k, "sown", y)]
            a = ssum([d["taxed"], d["untaxed_low"]])
            b = ssum([d["taxed"], d["untaxed_low"], d.get("untaxed_new", Decimal(0))])
            # the sown area is printed with or without the newly cleared land, depending on the year
            CHK.eq(out, f"{where(s)} {k[1]} {y}: imposées + non imposées (with or without the terres nouvellement "
                        f"défrichées) vs ensemencées", a if a == d["sown"] else b, d["sown"])



# ----------------------------------------------------------------- répartition européens / indigènes (sgt1926-1939)

SPLIT_CROP = {"wheat": ("wheat", "Blé dur et blé tendre"), "durum": ("durum_wheat", "Blé dur"),
              "soft": ("soft_wheat", "Blé tendre"), "barley": ("barley", "Orge"), "oats": ("oats", "Avoine")}
SPLIT_FARM = {"eur": ("european", "Européennes"), "ind": ("indigenous", "Indigènes")}


def cells_split(sec):
    out = []
    for r in sec["rows"]:
        c0, g = r["label"].split("_")
        crop, crop_fr = SPLIT_CROP[c0]
        fa, fa_fr = SPLIT_FARM[g]
        if sec["ed"] == "sgt1939" and r["label"] == "soft_eur":
            fa_fr = "Européens"
        for c in sec["cols"]:
            if c.startswith("m"):
                continue
            cell = r["cells"][c]
            v, fl = cell.value, flag_of(sec, r["label"], c, cell)
            if (sec["ed"], r["label"], c) in SPLIT_DERIVED:
                v, fl = SPLIT_DERIVED[(sec["ed"], r["label"], c)], "derived_from_totals"
            out.append(dict(base(sec, int(c)), crop=crop, crop_fr=crop_fr, farmers=fa, farmers_fr=fa_fr,
                            measure="area", measure_fr="Surface", unit="hectares", value=v, flag=fl))
    return out


# sgt1926 1917 orge Européennes printed "20.4'4 88": 5 x 18.280 53 (printed 1917-1921 average) - the four other
# years = 20.494 85, i.e. the broken digit is 9 (20.494 88, average 18.280 54 to the centiare).
SPLIT_DERIVED = {("sgt1926", "barley_eur", "1917"): Decimal("20494.88")}


def chk_split_all(secs):
    out = "agriculture_cereal_farmers"
    by, secof = defaultdict(dict), {}
    for s in secs:
        for r in s["rows"]:
            for c in s["cols"]:
                v = SPLIT_DERIVED.get((s["ed"], r["label"], c), r["cells"][c].value)
                by[(s["ed"], r["label"])][c] = v
                secof[(s["ed"], r["label"], c)] = s
    for (ed, label), d in by.items():
        for c, printed in d.items():
            if not c.startswith("m") or printed is None:
                continue
            a, b = map(int, c[1:].split("_"))
            vals = [d.get(str(y)) for y in range(a, b + 1)]
            if any(v is None for v in vals):
                continue
            got = sum(vals, Decimal(0)) / len(vals)
            CHK.eq(out, f"{where(secof[(ed, label, c)])} {label}: average {a}-{b}", got.quantize(Decimal("0.01")),
                   printed, tol=Decimal("0.05") if printed != printed.to_integral() else Decimal(1))



# ----------------------------------------------------------------- vigne by contrôle and nationality (sgt1922-1925)

VINE_NAT = {"fr": ("french", "Français"), "it": ("italian", "Italiens"), "am": ("anglo_maltese", "Anglo-Maltais"),
            "ae": ("other_european", "Autres Européens"), "tn": ("tunisian", "Tunisiens")}


def geo_of(sec, label):
    if sec.get("geo") == "region":
        r, chef, c = label.split("/")
        return dict(region=r, chef_lieu=chef, controle_civil=c)
    return dict(region="", chef_lieu="", controle_civil=label)


def cells_vine(sec):
    out = []
    for r in sec["rows"]:
        if r["label"] == "TOTAUX":
            continue
        for c in sec["cols"]:
            nat, m = c.split("_")
            if nat == "tot":
                continue
            cell = r["cells"][c]
            n, nfr = VINE_NAT[nat]
            meas = ("growers", "Nombre", "growers") if m == "n" else ("area", "Superficie (hect. a.)", "hectares")
            out.append(dict(base(sec, int(sec["ed"][3:])), **geo_of(sec, r["label"]), nationality=n,
                            nationality_fr=nfr, measure=meas[0], measure_fr=meas[1], unit=meas[2],
                            value=cell.value, flag=flag_of(sec, r["label"], c, cell)))
    return out


def chk_vine(sec):
    out = "agriculture_vine"
    rows = [r for r in sec["rows"] if r["label"] != "TOTAUX"]
    tot = row(sec, "TOTAUX")
    for c in sec["cols"]:
        CHK.eq(out, f"{where(sec)} {c}: lines vs TOTAUX", ssum(r["cells"][c].value for r in rows), tot[c].value)
    for m in ("n", "ha"):
        parts = [c for c in sec["cols"] if c.endswith("_" + m) and not c.startswith("tot")]
        for r in sec["rows"]:
            CHK.eq(out, f"{where(sec)} {r['label']}: nationalities vs TOTAUX ({m})",
                   ssum(r["cells"][c].value for c in parts), r["cells"]["tot_" + m].value)



# ----------------------------------------------------------------- oliviers by caïdat / région

OLIVE_COL = {"unprod": ("unproductive_and_wild", "Oliviers improductifs et oléastres"),
             "young": ("young_untaxed", "Jeunes oliviers non imposés"),
             "taxed": ("taxed", "Oliviers imposés"),
             "total": ("total", "Total")}


def olive_geo(sec, label):
    if sec.get("geo") == "4":
        r, chef, c, k = [x.strip() for x in label.split(" / ")]
        return dict(region=r, chef_lieu=chef, controle_civil=c, caidat=k)
    return dict(region="", chef_lieu="", controle_civil="", caidat=label)


def cells_olive(sec):
    out = []
    for r in sec["rows"]:
        if r["label"].startswith("TOTAUX"):
            continue
        cl = [c for c in sec["cols"]]
        # the line total is stored only where the classes are not printed (Djerba, from sgt1925)
        has_classes = any(r["cells"][c].value is not None for c in cl if c != "total")
        for c in cl:
            cell = r["cells"][c]
            if c == "total" and has_classes:
                continue
            if c != "total" and not has_classes and cell.flag == "not_applicable" and \
                    r["cells"]["total"].value is not None:
                continue
            code, fr = OLIVE_COL[c]
            v, fl = cell.value, flag_of(sec, r["label"], c, cell)
            if (sec["ed"], r["label"], c) in OLIVE_DERIVED:
                v, fl = OLIVE_DERIVED[(sec["ed"], r["label"], c)], "derived_from_totals"
            out.append(dict(base(sec, int(sec["ed"][3:])), **olive_geo(sec, r["label"]), tree_class=code,
                            tree_class_fr=fr, measure="trees", measure_fr="Nombre d'arbres", unit="trees",
                            value=v, flag=fl))
    return out


# broken digits solved from the printed totals: sgt1923 Kef improductifs "19.?73": the column TOTAUX needs 19.873
# (the line total 53.359 needs 13.873 but is itself 6.000 short: 59.359, cf. sgt1924's 59.284)
OLIVE_DERIVED = {("sgt1923", "Kef", "unprod"): Decimal(19873)}


def chk_olive(sec):
    out = "agriculture_olive"
    cs = [c for c in sec["cols"] if c != "total"]
    rows = [r for r in sec["rows"] if not r["label"].startswith("TOTAUX")]
    val = lambda r, c: OLIVE_DERIVED.get((sec["ed"], r["label"], c), r["cells"][c].value)
    noclass = ssum(r["cells"]["total"].value for r in rows if all(r["cells"][c].value is None for c in cs)
                   and r["cells"]["total"].value is not None)
    for r in sec["rows"]:
        if all(r["cells"][c].value is None for c in cs):
            continue
        extra = noclass if r["label"].startswith("TOTAUX") else Decimal(0)   # Djerba: total only
        CHK.eq(out, f"{where(sec)} {r['label']}: classes vs total" + (" (+ lines printed without classes)"
               if extra else ""), None if ssum(val(r, c) for c in cs) is None else
               ssum(val(r, c) for c in cs) + extra, r["cells"]["total"].value)
    tot = row(sec, "TOTAUX")
    for c in sec["cols"]:
        CHK.eq(out, f"{where(sec)} {c}: lines vs TOTAUX", ssum(val(r, c) or Decimal(0) for r in rows), tot[c].value)


# ----------------------------------------------------------------- tables

DOC = {
    "census": "edition the value is taken from (rule 4 series: the latest edition printing that year; rule 5 "
              "tables: the edition)",
    "table_id": "transcription section",
    "gallica_ark": "Gallica volume ark (views are numbered within a volume)",
    "source_page": "printed page number",
    "gallica_view": "Gallica view (fNNNN)",
    "year": "year of the figures (crop year = calendar year of the harvest, as printed; rule 5 tables: edition "
            "year)",
    "part": "sub-table letter as printed (a-d)", "part_fr": "printed sub-table title",
    "item": "item code (English)", "item_fr": "printed column heading",
    "crop_group": "sub-table letter (a cereals, b other food plants, c industrial plants, d shrub and tree crops)",
    "crop_group_fr": "printed sub-table title",
    "zone": "`tunisia` (whole country), or the zone of sgt1925's cereal tables (`north`, `centre_south`)",
    "zone_fr": "printed zone heading",
    "crop": "crop code (English)", "crop_fr": "printed line heading",
    "measure": "measure code (English)", "measure_fr": "printed heading of the measure",
    "unit": "unit of `value`, as printed (never converted)",
    "value": "printed value (» = 0)",
    "flag": "empty, or `illegible`, `total_mismatch` (cell identified as the faulty one of a failed check, printed "
            "value kept), `derived_from_totals`, `not_applicable`",
}

RULE4 = ("Printed for overlapping year windows: each year is taken from the **latest** edition that prints it "
         "(SPEC_ADDENDUM rule 4; `census` = that edition); every other printing, read independently on its own page "
         "image, is compared below.")
RULE5 = ("Printed once per edition (SPEC_ADDENDUM rule 5): every edition is kept; `year` = edition year.")

TABLES = {
    "agriculture_land": dict(
        secs=["land_a", "land_b", "land_c", "land_d"], cells=cells_land, key=["census", "part", "item", "measure"],
        rule5=True, dims=["part", "part_fr", "item", "item_fr", "measure", "measure_fr", "unit"],
        title_fr="Superficie : superficie territoriale ; répartition en superficie productive et improductive ; "
                 "répartition de la superficie productive ; répartition de la superficie labourable",
        title_en="Land area: territorial area and population density; productive and unproductive area; use of "
                 "the productive area; use of the arable area",
        unit="Units: km2, persons, persons per km2, hectares and percent (`unit`); value_type: mixed.",
        paras=["Printed on the first page of the chapter in every edition. The territorial area is 125.130 km2 in "
               "sgt1922 and 125.180 km2 from sgt1923; the density stays printed 16.72 through sgt1936 although the "
               "number of inhabitants changes with the censuses (2.093.939, 1921; 2.159.708, 1926; 2.410.692, 1931); "
               "sgt1939 prints 2.608.313 and 21.25. Totals (TOTAL de la superficie territoriale / productive / "
               "labourable, and their 100 %) are checks only.",
               "Checks: hectares of the parts = printed total; percentages sum to 100 (to 0.2); each percentage = "
               "hectares / total (to 0.15 point). Percentages printed inconsistently with the hectares are kept as "
               "printed; they are listed among the failed checks."],
        fail_note="sgt1922 and sgt1936: the jachères are printed 100.000 ha too high (1.947.136 and 1.770.898; "
                  "their own percentages fit 1.847.136 and 1.870.898): flagged `total_mismatch`. sgt1923 prints "
                  "the terres de parcours at 59,4 % (50,9 % computed; flagged) and a labourable total of 2.840.000 "
                  "for parts summing to 2.820.000. sgt1927 prints percentages of d) that do not fit the hectares "
                  "(prairies 9,2 % flagged; others listed). sgt1928-sgt1929 print the 100 of the b) total as \"00\" "
                  "(total line, not stored). sgt1936 prints the productive area with a broken digit (\"9.?00.000\"), "
                  "stored 9.000.000 = 12.500.000 - 3.500.000 (`derived_from_totals`). The other failures are "
                  "rounding of the printed percentages or differences of 1-180 ha."),
    "agriculture_crops": dict(
        secs=["crops_a", "crops_b", "crops_c", "crops_d"], cells=cells_crops, key=["year", "zone", "crop", "measure"],
        dims=["zone", "zone_fr", "crop_group", "crop_group_fr", "crop", "crop_fr", "measure", "measure_fr", "unit"],
        title_fr="Productions végétales. Cultures diverses ; superficie et production",
        title_en="Crop production: area, production and yield of cereals, other food plants, industrial plants "
                 "and tree crops",
        unit="Units: hectares, quintals, hectolitres (wine), quintals or hectolitres per hectare, trees "
             "(`unit`); value_type: mixed.",
        fail_note="Yield failures recur unchanged in every printing of the same year (oats 1915-1916, soft wheat "
                  "1921, potatoes 1920, maize 1923, and sgt1925's zone yields): printed figures. sgt1924 prints the "
                  "1924 blé dur production 2.350.000 (= 1923); its own yield 2,4 and its 1920-1924 average 1.474.700 "
                  "need 1.040.000, printed by every later edition (kept). sgt1925 prints the 1925 blé dur surface of "
                  "the northern zone 129.774 (flag `total_mismatch`): its yield 6,6 and its averages need 329.774. "
                  "sgt1930 prints the 1930 orange trees 19.000 (flag `total_mismatch`): its averages need about "
                  "90.000. The other failures are printed averages that do not fit the printed years (the years "
                  "themselves agree across up to ten independent printings); several are off by a round amount "
                  "(e.g. sgt1923 autres dattiers 1919-1923 774.859 for 974.859, sgt1927 1923-1927 olive trees "
                  "1.586.183 for 15.861.830), i.e. misprinted averages.",
        paras=["Printed in every edition: ten years to sgt1930 (two pages per sub-table: five years on the left, five "
               "years and the averages of the two half-periods and of the ten years on the right), three years and "
               "two averages from sgt1935. `year` = crop year (calendar year of the harvest) as printed. The "
               "printed averages (MOYENNE DES ANNÉES) are not stored; they are used as checks (mean of the printed "
               "years, to 0.2 %; averages of yields are not checked). Yields are checked against production / "
               "surface (to 5 %). The vine yield is not checked: footnote (2) computes it on the vineyard over 3 "
               "years old.",
               "a) Céréales: blé dur and blé tendre are printed as one bracketed figure for 1913-1915 (crop "
               "`wheat`). In sgt1925 the cereals are printed for two zones only (`zone` = `north`: Tunisie "
               "septentrionale et Hauts plateaux, 1re-3e Régions; `centre_south`: Tunisie centrale et méridionale, "
               "4e-5e Régions et Territoires militaires), with no whole-country figures; from sgt1926 the "
               "whole-country table returns without yields (footnote: the yield varies too much from one zone to "
               "another and is given per zone in the next table). b) c) d) are whole-country throughout. "
               "Dattiers: the Dégla trees are pieds imposables (footnote), and from sgt1926 so are the other "
               "dates; sgt1939 prints total and taxable trees (`trees` / `trees_taxable`), surfaces, and renames "
               "the autres dattiers communes (`crop_fr`). sgt1939 also renames the table Cultures arbustives et "
               "fruitières and adds figs, mandarins, apricots, quinces, pomegranates, peaches, pears, apples, "
               "plums, surfaces and young trees; 'pois et pois chiches' replaces 'pois chiches' (crop "
               "`peas_chickpeas`).",
               "» is stored 0 as printed, except where it marks a figure not collected next to printed figures: "
               "flax surface and yield 1913-1915 (production printed), the vine yield of sgt1936 (» in every "
               "column) and the new lines of sgt1939 in 1937 (stored NA, `not_applicable`). Asterisks "
               "(provisional figures, usually the edition year) are not stored. sgt1926-sgt1930 print the 1925 "
               "autres dattiers production with a broken first digit (\":52.000\"): 352.000, as sgt1925 and the "
               "printed averages (`derived_from_totals`). Illegible cells cut by the binding (sgt1922 1917 potatoes "
               "surface and tobacco; sgt1923 1918 tobacco and olive trees; sgt1939 poiriers 1938 \"100.00\") are "
               "taken from a later printing where one exists.",
               "Footnotes of d): (1) the Muslim vineyard, planted with table grapes (about 2.200 ha in sgt1926-"
               "sgt1929, 4.000 ha from sgt1930, 4.500 ha in sgt1939), scattered in small plots, is not counted; "
               "sgt1935: grubbing of 2.800 ha in 1935-36 not deducted. (3) oliviers en production = trees of 15 "
               "years and more. sgt1929-sgt1930: the 1929 almond trees (660.000) come from a recent census of fruit "
               "trees for the tax. sgt1939: the 1938 almond trees from the declarations collected by the Direction "
               "des Finances; the 1936-1937 orange trees estimated from declarations, 1938 from an unfinished "
               "survey; caroubiers mostly scattered trees, no surface."]),
    "agriculture_cereal_zones": dict(
        secs=["zones"], cells=cells_zones, key=["year", "zone", "crop", "measure"],
        dims=["zone", "zone_fr", "crop", "crop_fr", "measure", "measure_fr", "unit"],
        title_fr="Principales cultures : rendement et répartition. a) Céréales (blé dur, tendre, orge, avoine) - "
                 "Rendement par zone (Nord, Centre et Sud)",
        title_en="Cereals (durum and soft wheat, barley, oats): area, production and yield per hectare by zone",
        unit="Units: hectares, quintals, quintals per hectare (`unit`); value_type: mixed.",
        fail_note="Yield failures recur in every printing of the same year (e.g. barley Nord 1921 7,8; durum "
                  "Centre et Sud 1923 printed 1,2 to sgt1928 and 2 from sgt1929; oats Centre et Sud 1922 0,1 then "
                  "1): printed figures. sgt1930 prints the 1930 orge Nord production 350.000 (zoomed crop; flag "
                  "`total_mismatch`): its yield 5 and its two averages need 850.000. sgt1936 prints the 1935 orge "
                  "Nord surface 450.000, against 150.000 in sgt1935 (whose yield 6 fits): the sgt1935 value is kept "
                  "(`reprint_corrected`). sgt1939 1939 blé tendre Centre et Sud: surface 17.100 (confirmed by the "
                  "printed 1935-1939 average) for a printed yield 8,5 (5,6 computed). Averages that fail are "
                  "printed averages not fitting the printed years (several by round amounts: sgt1927 blé tendre "
                  "Nord 1918-1922 474.032 for 47.403).",
        paras=["Printed from sgt1926 (ten years to sgt1930, three years from sgt1935), complementing the "
               "whole-country cereal lines of agriculture_crops (which have no yields from sgt1926). Zones as "
               "printed: Nord, and Centre et Sud. sgt1925 printed a comparable split under other headings (Tunisie "
               "septentrionale et Hauts plateaux / Tunisie centrale et méridionale) inside the cultures diverses "
               "table: it is kept in agriculture_crops (`zone`), not compared here. The printed averages are "
               "checks only (mean of the years, to 0.2 %); yields are checked against production / surface (to "
               "5 %).",
               "Later editions revise the latest years (1927-1928 productions, listed below); each year is "
               "stored from the latest edition printing it."]),
}
TABLES["agriculture_yield_classes"] = dict(
    secs=["surfaces", "classes", "zclasses"], cells=cells_yc, key=["year", "zone", "crop", "subtable", "farmers", "area_class",
                                                       "measure"],
    dims=["crop_year_fr", "zone", "zone_fr", "crop", "crop_fr", "subtable", "farmers", "farmers_fr", "area_class",
          "area_class_fr", "measure", "measure_fr", "unit"],
    doc=dict(
        year="harvest year (the upper box is printed by harvest year; the lower table by agricultural year, "
             "e.g. 1914-1915 = harvest 1915, `crop_year_fr`)",
        crop_year_fr="agricultural year as printed in the lower table (empty for the upper box)",
        zone="`tunisia` (whole country), or the zone of sgt1925 (`north`: Tunisie septentrionale et Hauts plateaux; "
             "`centre_south`: Tunisie centrale et méridionale)",
        zone_fr="zone heading as printed (\"Tunisie (ensemble)\" when the table has no zones)",
        crop="crop code (English)", crop_fr="crop as printed in the sub-table title",
        subtable="`surfaces` (upper box: surfaces ensemencées, imposées, non imposées) or `yield_classes` (lower "
                 "table: number of hectares that produced 1, 2, ... 6 hectolitres and more per hectare)",
        farmers="`all` (upper box), `european` or `indigenous` (CULTURES EUROPÉENNES OU INDIGÈNES)",
        farmers_fr="printed line heading (empty for the upper box)",
        area_class="surface category (upper box) or yield class in hectolitres per hectare (lower table)",
        area_class_fr="printed heading", measure="`area`; `ratio_to_line_total` (RAPPORT avec les surfaces imposées "
                                                 "or ensemencées, as headed: the class area over the TOTAUX of the "
                                                 "same line); sgt1925 `percent_of_sown_area` (RAPPORT avec les surfaces "
                                                 "ensemencées, printed in %)",
        measure_fr="printed heading of the measure",
        unit="`hectares` (printed h. a.: hectares and ares, stored as hectares with two decimals; sgt1925 whole "
             "hectares), `ratio`, or `percent`",
        value="printed value (» = 0)",
        flag="empty, or `ocr_corrected` (image reading differs from the Gallica OCR), `total_mismatch` (cell "
             "identified as the faulty one of a failed check, printed value kept), `reprint_corrected` (the latest "
             "printing is misprinted: value from the earlier edition named in `census`)"),
    title_fr="Principales cultures ; rendement et répartition (surfaces ensemencées, imposées et non imposées ; nombre "
             "d'hectares ayant produit 1 à 6 hectolitres et au-dessus ; cultures européennes ou indigènes)",
    title_en="Main crops: sown, taxed and untaxed areas, and taxed area by yield class (hectolitres per hectare), "
             "European and indigenous farmers",
    unit="Units: hectares (printed h. a., hectares and ares; sgt1925 whole hectares), ratios and percent "
         "(`unit`); value_type: mixed.",
    paras=["sgt1922-sgt1924: one spread per crop (blé, orge, avoine, maïs, sorgho, fèves, pois chiches, lin; sgt1922 "
           "a)-h), the lettering of the survey's \"d)-f)\" and \"g) (h)\" is a) blé ... h) lin). Upper box "
           "(`subtable` = `surfaces`, by harvest year): surfaces ensemencées, imposées (yield over 1 hl), non "
           "imposées (yield under 1 hl), non imposées sown on newly cleared land. Lower table (`yield_classes`, "
           "by agricultural year 1914-1915 ... = harvest `year`; `crop_year_fr`): hectares that produced 1, 2, 3, "
           "4, 5, 6 hl and more per hectare, for European and indigenous farmers, each with its RAPPORT (ratio to "
           "the line's TOTAUX; headed \"avec les surfaces imposées\" for blé, orge, avoine, maïs, pois chiches and "
           "\"avec les surfaces ensemencées\" for sorgho, fèves, lin, but computed on the TOTAUX in both cases). "
           "The TOTAUX lines (Européens + Indigènes) and the TOTAUX column are checks only. The RAPPORT of the "
           "TOTAUX lines is not printed for the last two years of sgt1923-sgt1924.",
           "sgt1925: new layout, three spreads (blé, orge, avoine), left page Tunisie septentrionale et Hauts "
           "Plateaux (1re-3e Régions, `zone` = `north`), right page Tunisie centrale et méridionale (4e-5e Régions "
           "et Territoires militaires, `centre_south`), years 1921-1925: surfaces ensemencées, hectares that "
           "produced 0 à 5 hectol. and 6 hl et au-dessus, each with its percentage of the sown area (`percent`). "
           "Not comparable cell by cell with sgt1922-sgt1924 (different classes and zones): not compared.",
           "Overlapping years (sgt1922-sgt1924 reprint 1915/1916-1923) follow rule 4: each cell from the latest "
           "edition printing it, every other printing (read independently on its own page) compared. Cells of the "
           "TOTAUX lines are not stored, so their differences are given here: sgt1924 prints the 1919-1920 TOTAUX "
           "5 hl of pois chiches (184 97) and of lin (256 02) interchanged with respect to sgt1922-sgt1923, the "
           "1919-1920 TOTAUX 6 hl of fèves 6.131 36 (6.431 36) and 1 hl of pois chiches 514 11 (514 »), the "
           "1921-1922 Indigènes TOTAUX of fèves 651 88 (9.651 88); sgt1923-sgt1924 print in the TOTAUX column of "
           "sorgho, lines 1919-1920 to 1921-1922, the totals of the year before. Stored cells that differ: see "
           "the table below (sgt1923-sgt1924 print the 1916 blé ensemencées and imposées interchanged, the TOTAUX "
           "of 1916 = 553.112 51 confirms sgt1922; sgt1924 prints fèves 1919-1920 Européens 5 hl 663 23 and lin "
           "Européens 2 hl 24 11, the line sums confirm 662 23 and 24 »: the earlier printing is kept, flag "
           "`reprint_corrected`). sgt1923 prints the avoine surfaces of 1922 and 1923 under interchanged year "
           "headings; they are compared under the year they belong to (flag `row_realigned` on that printing)."],
    fail_note=("Line sums (classes vs TOTAUX), Européens + Indigènes vs TOTAUX, TOTAUX vs surfaces imposées, "
               "imposées + non imposées vs ensemencées (the sown area includes the newly cleared land in some years "
               "only: both readings accepted), each RAPPORT vs class / TOTAUX (to 0.0005 or 1 %, also accepted "
               "against the sum of the classes when the TOTAUX is the faulty cell), and in sgt1925 the two classes "
               "vs the sown area and the percentages. Most failures recur unchanged in every printing of the same "
               "cell (sgt1922, sgt1923, sgt1924 were set from the same type). Flagged `total_mismatch` where one "
               "stored cell explains every failing check: blé 1914-1915 Indigènes 3 hl 55.309 86 (TOTAUX and "
               "RAPPORT need 55.509 86); orge 1917-1918 Indigènes 4 hl 60.181 79 (69.181 79); avoine 1918-1919 "
               "Indigènes 3 hl 144 57 (1.714 57); fèves 1918-1919 Indigènes 6 hl 1.105 13 (the line needs 11.015 "
               "13); pois chiches 1919-1920 Européens 1 hl 470 82 (70 82); RAPPORT cells with a dropped or added "
               "digit (blé 1918-1919 Indigènes 4 hl 0,1211, 1922-1923 Européens 1 hl 0,2015; orge 1915-1916 "
               "Européens 6 hl 0,0945, 1920-1921 Indigènes 6 hl 0,0762; avoine 1918-1919 Européens 3 hl 0,213; maïs "
               "1918-1919 Européens 1 hl 0,0016, 1921-1922 Indigènes 2 hl 0,0136, 1922-1923 Européens 6 hl 0,9929; "
               "sorgho 1918-1919 Européens 4 hl 0, Indigènes 2 hl 0,1666; fèves 1919-1920 Européens 1 hl 0,5335; "
               "pois chiches 1920-1921 Européens 3 hl 0,0171, Indigènes 6 hl 0,0798; lin 1920-1921 Indigènes 1 hl "
               "0,0960, 1922-1923 Européens and Indigènes 1 hl 0,0083 and 0,0236); sgt1925 blé Nord 1925 "
               "Indigènes 6 hl 175.582 (sown - 0-5 hl = 175.852, its percentage 60,46 fits), avoine Nord 1925 "
               "Indigènes 6 hl 14.603 (14.403), blé Centre-Sud 1922 Indigènes 13,14 % (3,13), avoine Nord 1922 "
               "Indigènes 22,33 % (12,33). The other failures are misprinted TOTAUX cells (not stored: e.g. blé "
               "1921-1922 TOTAUX 316.818 70 for 346.818 70, orge 1916-1917 Indigènes TOTAUX 455.708 79 for "
               "445.708 79, lin 1921-1922 TOTAUX 1.594 31 for 1.494 31), RAPPORT cells off in the last digits, "
               "differences of a few ares, or lines where no single cell can be identified (pois chiches 1923-1924 "
               "Indigènes in sgt1924: the six classes, each fitting its printed RAPPORT, sum to 3.983 45 against a "
               "printed TOTAUX of 3.542 90; sorgho 1923-1924 Européens 682 » against 678 »)."))

TABLES["agriculture_cereal_farmers"] = dict(
    secs=["split"], cells=cells_split, key=["year", "crop", "farmers", "measure"],
    dims=["crop", "crop_fr", "farmers", "farmers_fr", "measure", "measure_fr", "unit"],
    doc=dict(crop="crop code (English): `wheat` = blé dur et blé tendre (one line to sgt1936), `durum_wheat` / "
                  "`soft_wheat` (sgt1939), `barley`, `oats`",
             crop_fr="printed line heading (CLASSIFICATION)",
             farmers="`european` or `indigenous` (CULTURES EUROPÉENNES ou indigènes)",
             farmers_fr="printed line heading",
             unit="`hectares` (printed h. a., hectares and ares, stored with two decimals, to 1927; whole hectares "
                  "from the 1928 figures)",
             flag="empty, or `derived_from_totals` (broken digit solved from the printed average), "
                  "`reprint_corrected`"),
    title_fr="Principales cultures. Céréales (blé dur, tendre, orge, avoine). Répartition de la superficie entre "
             "européens et indigènes",
    title_en="Cereals (durum and soft wheat, barley, oats): sown area of European and indigenous farmers",
    unit="Units: hectares (`unit`); value_type: hectares.",
    paras=["Printed from sgt1926 (ten years to sgt1930, three years from sgt1935), as sub-table b) of the principales "
           "cultures after the yields by zone (agriculture_cereal_zones). The printed averages (MOYENNE DES ANNÉES) "
           "are not stored; they are checked against the mean of the printed years when every year is printed in "
           "the same edition (to 0.05 % or 1 ha). sgt1930 heads its third average \"1920-1929\": blé and orge "
           "repeat sgt1929's 1920-1929 averages, avoine prints new figures; not checkable (1920 not printed). "
           "sgt1935-sgt1936 reprint averages over years they do not print (1931-1935, 1926-1935). sgt1939 splits "
           "blé dur and blé tendre (footnote: soft wheat distinguished only from 1937; their averages are of "
           "1937-1939, their 1930-1939 average not printed).",
           "Rule 4: each year from the latest edition printing it; the other printings, read independently on "
           "their own pages, are compared below. sgt1926-sgt1927 print the 1920 blé Européennes 72.914 55, "
           "sgt1928-sgt1929 72.944 55 (zoomed crops); the averages of sgt1926 (1917-1921), sgt1927 (1918-1922) and "
           "sgt1929 (1920-1924) all need 72.944 5x: sgt1926-sgt1927 misprint it (listed among the failed checks), "
           "the latest printing is kept.", ],
    fail_note="Averages that fail are printed averages not fitting the printed years (listed); the years agree "
              "across every printing.")

TABLES["agriculture_vine"] = dict(
    secs=["vine"], cells=cells_vine, key=["census", "region", "controle_civil", "nationality", "measure"], rule5=True,
    dims=["region", "chef_lieu", "controle_civil", "nationality", "nationality_fr", "measure", "measure_fr", "unit"],
    doc=dict(year="edition year (the table gives the state of the vineyard; no date printed)",
             region="région as printed (sgt1925); empty when the table lists contrôles only",
             chef_lieu="chef-lieu de région as printed (sgt1925); empty otherwise",
             controle_civil="contrôle civil as printed (spelling of each edition: Kef / Le Kef, Teboursouk / "
                            "Téboursouk; sgt1922 also lists Gabès and Zarzis separately, sgt1925 Gabès-Zarzis)",
             nationality="nationality of the vine growers: `french`, `italian`, `anglo_maltese`, `other_european`, "
                         "`tunisian` (Tunisiens, from sgt1924)",
             nationality_fr="printed column heading",
             measure="`growers` (Nombre de viticulteurs) or `area` (Superficie)",
             measure_fr="printed heading", unit="`growers` or `hectares` (printed hect. a., stored with two decimals)",
             flag="empty, or `total_mismatch`"),
    title_fr="Vigne. Répartition des viticulteurs par contrôle (sgt1925 : par régions) et par nationalité",
    title_en="Vineyards: number of vine growers and vineyard area by contrôle civil and nationality",
    unit="Units: growers and hectares (`unit`); value_type: mixed.",
    paras=["Printed in sgt1922-sgt1925 (sub-table i) of the principales cultures). The TOTAUX line and the TOTAUX "
           "columns (des viticulteurs, des superficies) are checks only. sgt1922 lists 18 contrôles (Gabès, Gafsa "
           "and Zarzis separately), sgt1923 the same in alphabetical order, sgt1924 adds the Tunisiens columns, "
           "sgt1925 groups the contrôles by région (1re-5me Région with their chefs-lieux; Gabès-Zarzis together, "
           "Thala new, Gafsa dropped).",
           "Notes printed with the table (translated): the Muslim vineyard, planted with table grapes and scattered "
           "in many small plots over the Regency, is not counted; sgt1922 and sgt1923 estimate it at 2.200 ha "
           "(total Tunisian vineyard 25.906 and 26.895 ha; sgt1923: of which 25.821 ha in production), sgt1925 at "
           "about 2.227 ha (European vineyard 27.986 ha, total 30.213 ha)."],
    fail_note="Checks: every column against the TOTAUX line, every line's nationalities against its TOTAUX columns. "
              "sgt1922: the Italiens superficie of Sfax (1 45) and Tabarka (10 25) are printed 46 50 and 1 20 too "
              "low (their line totals 347 80 and 37 70 and the column TOTAUX 12.889 37 all need 47 95 and 11 45): "
              "flagged `total_mismatch`; the TOTAUX des viticulteurs is printed 2.499 for 2.439 (lines and "
              "nationalities agree on 2.439). sgt1923: the Grombalia total superficie 7.565 30 and the grand total "
              "24.695 90 (also quoted in the observations) are 100 ha above the sum of the nationalities (7.465 30, "
              "24.595 90); the Anglo-Maltais TOTAUX is printed 25 for 26 (lines). sgt1925: TOTAUX des viticulteurs "
              "printed 2.811 for 2.941 (lines and nationalities agree). Totals are not stored.")

TABLES["agriculture_olive"] = dict(
    secs=["olive"], cells=cells_olive, key=["census", "region", "controle_civil", "caidat", "tree_class"],
    rule5=True,
    dims=["region", "chef_lieu", "controle_civil", "caidat", "tree_class", "tree_class_fr", "measure",
          "measure_fr", "unit"],
    doc=dict(year="edition year (the table gives the trees counted for the canoun olive tax; no date printed)",
             region="région as printed (from sgt1925), or \"Territoires Militaires du Sud\"; empty in sgt1922-sgt1924",
             chef_lieu="chef-lieu de région as printed (from sgt1925); empty otherwise",
             controle_civil="contrôle civil as printed (from sgt1925); empty otherwise",
             caidat="caïdat as printed; \"Cap-Bon > Nabeul\" = caïdat printed under the Cap-Bon bracket",
             tree_class="`unproductive_and_wild` (oliviers improductifs et oléastres), `young_untaxed` (jeunes "
                        "oliviers non imposés), `taxed` (oliviers imposés); `total` only for a line printed without "
                        "classes (Djerba)",
             tree_class_fr="printed column heading", measure="`trees`", measure_fr="printed heading",
             unit="`trees`",
             flag="empty, or `not_applicable` (Non recensés), `derived_from_totals`, `total_mismatch`"),
    title_fr="Oliviers. Répartition par caïdat (à partir de sgt1925 : par régions)",
    title_en="Olive trees by caïdat (unproductive and wild, young untaxed, taxed)",
    unit="Units: trees (`unit`); value_type: count.",
    paras=["Printed in every edition. sgt1922-sgt1924: 30 caïdats numbered in a fixed order (Soliman and Nabeul "
           "bracketed as Cap-Bon). From sgt1925 the caïdats are grouped by région, chef-lieu and contrôle civil, "
           "with the Territoires Militaires du Sud; Aïn-Draham is printed \"Non recensés\" (stored NA, "
           "`not_applicable`); Djerba is printed with a total only (footnote: not subject to the canoun, not "
           "counted by category; its total is stored with `tree_class` = `total`). The line totals (TOTAL) and the "
           "TOTAUX line are checks only, except Djerba's total.",
           "Caïdat names as printed in each edition (Ouled-Ayar / Oulad Ayar, Fraichiche / Fraichiches, Majeur / "
           "Majeurs, Banlieue / Banlieue de Tunis). sgt1925-sgt1926 print Nabeul above Soliman under Cap-Bon, with "
           "the figures that sgt1922-sgt1924 print for Soliman: kept as printed (the names may be interchanged).",
           "sgt1935 and sgt1936 print the same figures in every cell (both printings read independently); sgt1939 "
           "adds the caïdat Djemmal (its bracket is ambiguous between the Sousse and Kairouan contrôles: stored "
           "under Sousse) and drops La Skhira and Djerba. Rule 5: each edition kept."],
    fail_note="Checks: classes vs each line's TOTAL, every column vs TOTAUX (Djerba's total-only line added to "
              "the TOTAUX check). Flagged `total_mismatch` where one class explains both the line and the column "
              "check (e.g. sgt1927 Sousse jeunes oliviers 122.974 for 622.974, Mahdia imposés 941.943 for 971.943; "
              "sgt1929 Mahdia jeunes 558.347 for 588.347). Other failures are misprinted line totals (sgt1923 "
              "Banlieue 224.443 for 924.443; sgt1924 Medjez-el-Bab 15.710 for 55.710; sgt1928 Souk-el-Khemis 2.193, "
              "Zaghouan 39.538), differences of a few units, or misprinted TOTAUX; sgt1923 Kef improductifs printed "
              "with a broken digit is solved from the column TOTAUX (19.873, `derived_from_totals`). The failures of "
              "sgt1935 recur identically in sgt1936.")


SURVEY = {
    "sgt1922": "f231 chapter XI title (Agriculture); f232 blank; f233 Superficie a)-d) [transcribed]; f234|f235 "
               "Productions végétales, cultures diverses, superficie et production (1913-1922) a) céréales "
               "[transcribed]; f236|f237 b) autres plantes alimentaires, c) plantes industrielles [transcribed]; "
               "f238|f239 d) plantes arbustives [transcribed]; f240|f241 Principales cultures, rendement et "
               "répartition a) blé (1914-1922; surfaces ensemencées, imposées, non imposées, by yield class, "
               "européennes / indigènes); f242|f243 b) orge; f244|f245 c) avoine; f246|f247 d)-f) (fèves, maïs, "
               "sorgho); f248|f249 g) pois chiches (h) lin); f250|f251 i) vigne, répartition des viticulteurs par "
               "contrôle et par nationalité; f252 j) oliviers, répartition par caïdat; f253 Forêts a) superficie "
               "des terrains domaniaux boisés, délimitations (1903-1922); f254 b) produits forestiers "
               "(adjudications); f255-f259 Météorologie a) relevé pluviométrique de l'année agricole 1921-1922 "
               "(pluies par saison, by station); f260-f269 b) relevé pluviométrique de l'année solaire (mm and "
               "days per month, by station); f270|f271 c) données climatologiques 1922 par région; f272|f273 d) "
               "statistique thermométrique 1911-1920; f274 École coloniale d'agriculture a) lieu d'origine des "
               "élèves (1898-1922); f275 b) promotions; f276 c) effectif par année scolaire; f277 Service "
               "botanique a) essais de variétés nouvelles (1912-1922); f278 b) vente de semences pédigrées "
               "(1910-1922); f279 c) ventes d'arbres et de plantes (1917-1922); f280 blank. f281 = chapter XII "
               "Commerce et navigation.",
    "sgt1923": "f721 title; f722 blank; f723 Superficie [transcribed]; f724|f725, f726|f727, f728|f729 cultures "
               "diverses 1914-1923 [transcribed]; f730|f731 principales cultures a) blé (1915-1923); f732|f733 b) "
               "orge; f734|f735 c) avoine (1918-1923); f736|f737 e) sorgho...; f738|f739 g) pois chiches "
               "(1919-1923); f740|f741 i) vigne par contrôle et nationalité; f742 l) oliviers par caïdat; f743 "
               "forêts a) (1903-1923); f744 b) produits forestiers; f745-f749 météorologie a) année agricole "
               "1922-1923; f750-f759 b) année solaire; f760|f761 c) données climatologiques 1923; f762-f764 d) "
               "pluviométrie agricole 1900-1901 à 1919-1920 (moyennes par période quinquennale); f765-f767 école "
               "coloniale a)-c) (1898-1923); f768-f770 service botanique a)-c). f771 = chapter XII.",
    "sgt1924": "f1217 title; f1218 blank; f1219 Superficie [transcribed]; f1220-f1225 cultures diverses 1915-1924 "
               "[transcribed]; f1226-f1241 principales cultures a) blé ... (eight two-page spreads, 1915/1918/"
               "1919-1924; f1240 without OCR); f1242|f1243 i) vigne par contrôle et nationalité; f1244 j) oliviers "
               "par caïdat; f1245 forêts a) (1903-1924); f1246 b); f1247-f1251 météorologie a) 1923-1924; "
               "f1252-f1263 b) année solaire; f1264|f1265 c); f1266-f1268 d) moyennes pluviométriques 1911-1920; "
               "f1269-f1271 école coloniale a)-c); f1272-f1274 service botanique a)-c). f1275 = chapter XII.",
    "sgt1925": "f287 title; f288 blank; f289 Superficie [transcribed]; f290|f291 cultures diverses a) céréales 1° "
               "Tunisie septentrionale et Hauts plateaux [transcribed]; f292|f293 2° Tunisie centrale et "
               "méridionale [transcribed]; f294|f295 b), c) [transcribed]; f296|f297 d) [transcribed]; f298|f299 "
               "principales cultures a) blé (1921-1925); f300|f301 by zone (Tunisie septentrionale / centrale et "
               "méridionale); f302|f303 c) avoine...; f304|f305 i) vigne par régions et nationalité; f306 oliviers "
               "par régions; f307 forêts a) (1903-1925); f308 b); f309-f315 météorologie a) 1924-1925; f316-f329 "
               "b) année solaire; f330|f331 c); f332-f334 pluviométrie agricole 1900-1901 à 1924-1925; f335-f337 "
               "Institutions d'enseignement et de recherches: école coloniale a)-c); f338-f340 service botanique "
               "a)-c); f341 laboratoire de chimie, analyses effectuées; f342 blank. f343 = chapter XII.",
    "sgt1926": "f803 title; f804 blank; f805 Superficie [transcribed]; f806-f811 cultures diverses 1917-1926 "
               "[transcribed]; f812|f813 principales cultures a) céréales, rendement par zone (Nord, Centre et "
               "Sud, 1917-1926); f814|f815 b) céréales, répartition de la superficie entre européens et indigènes; "
               "f816 d) oliviers par régions; f817 forêts a) (1903-1926); f818 b); f819-f825 météorologie a) "
               "1925-1926; f826-f839 b); f840|f841 c); f842-f845 d) températures moyennes et extrêmes 1901-1925; "
               "f846-f848 école coloniale a)-c); f849|f850 service botanique a) semences, b) arbres; f851 "
               "laboratoire de chimie; f852 blank. f853 = chapter XII.",
    "sgt1927": "f259 title; f260 blank; f261 Superficie [transcribed]; f262-f267 cultures diverses 1918-1927 "
               "[transcribed]; f268|f269 principales cultures a) rendement par zone (1918-1927); f270|f271 b) "
               "répartition européens / indigènes; f272|f273 d) oliviers par régions; f274-f279 Animaux a) nombre "
               "d'animaux de chaque espèce des européens, b) des indigènes, c) total (by contrôle civil); f280 "
               "forêts a); f281 b); f282-f287 météorologie a) 1926-1927; f288-f303 b); f304|f305 c); f306|f307 d) "
               "1901-1925; f308-f310 école coloniale; f311|f312 service botanique; f313 laboratoire de chimie; "
               "f314 blank. f315 = chapter XII.",
    "sgt1928": "f783 title; f784 blank; f785 Superficie [transcribed]; f786-f791 cultures diverses 1919-1928 "
               "[transcribed; f787, f789 without OCR]; f792|f793 principales cultures a) rendement par zone; "
               "f794|f795 b) répartition; f796|f797 d) oliviers par régions; f798-f803 animaux a)-c); f804 forêts "
               "a); f805 b); f806-f812 météorologie a) 1927-1928; f813-f829 b); f830|f831 c); f832-f835 humidité "
               "relative 1901-1925; f836-f838 école coloniale; f839|f840 service botanique; f841 laboratoire de "
               "chimie; f842 blank. f843 = chapter XII.",
    "sgt1929": "f261 title; f262 blank; f263 Superficie [transcribed]; f264-f269 cultures diverses 1920-1929 "
               "[transcribed]; f270|f271 principales cultures a); f272|f273 b); f274|f275 d) oliviers par régions; "
               "f276-f281 animaux a)-c); f282 forêts a); f283 b); f284-f290 météorologie a) 1928-1929; f291-f309 "
               "b); f310|f311 c) (année 1929); f312 station centrale de la Manoubia (année 1929); f313-f315 école "
               "coloniale; f316|f317 service botanique; f318 laboratoire de chimie (Tunis); f319 (Sfax); f320 "
               "blank. f321 = chapter XII.",
    "sgt1930": "f795 title; f796 blank; f797 Superficie [transcribed]; f798-f803 cultures diverses 1921-1930 "
               "[transcribed]; f804|f805 principales cultures a); f806|f807 b); f808|f809 d) oliviers par régions; "
               "f810-f815 animaux a)-c); f816 forêts a); f817 b); f818-f825 météorologie a) 1929-1930; f826-f843 "
               "b) année 1930; f844|f845 c); f846-f849 pluies moyennes 1926-1930 et 1901-1930; f850-f852 école "
               "coloniale; f853|f854 service botanique; f855 laboratoire de chimie (Tunis); f856 (Sfax). f857 = "
               "chapter XII.",
    "sgt1935": "f139 chapter XI title; f140 blank; f141 Superficie [transcribed]; f142 cultures diverses a) "
               "(1933-1935) [transcribed]; f143 b), c) [transcribed]; f144 d) [transcribed]; f145 principales "
               "cultures a) rendement par zone (1933-1935); f146|f147 b) répartition européens / indigènes; "
               "f148|f149 d) oliviers par régions; f150|f151 animaux, nombre total (européens et tunisiens) by "
               "contrôle; f152 blank?; f153 forêts a) superficie et modifications du domaine soumis au régime "
               "forestier; f154 blank. f155 = chapter XII Institutions d'enseignement et de recherches (with the "
               "school, the laboratories and the meteorology: research_ chapter).",
    "sgt1936": "f100 chapter X title; f101 blank; f102 Superficie [transcribed]; f103-f105 cultures diverses "
               "(1934-1936) [transcribed]; f106 rendement par zone; f107|f108 répartition européens / indigènes; "
               "f109|f110 oliviers par régions; f111|f112 dattiers, relevé par caïdat du nombre d'arbres d'après "
               "leur âge au 1er novembre 1936; f113|f114 animaux jeunes et imposables (rôle de 1936) by contrôle; "
               "f115 forêts, consistance du domaine soumis au régime forestier. f116 = chapter XI Institutions "
               "d'enseignement et de recherches (Institut Pasteur, Institut Arloing, école coloniale, service "
               "botanique, laboratoires, f123-f144 relevé pluviométrique 1936); f146 = chapter XII Commerce. The "
               "range 100-145 of CHAPTERS.md is 100-115 for Agriculture.",
    "sgt1939": "f99 chapter X title; f100 Superficie [transcribed]; f101 céréales (1937-1939) [transcribed]; f102 "
               "autres plantes alimentaires, plantes industrielles [transcribed]; f103|f104 cultures arbustives et "
               "fruitières [transcribed]; f105 rendement par zone; f106|f107 répartition européens / indigènes; "
               "f108|f109 oliviers par régions; f110|f111 dattiers par caïdat; f112|f113 animaux (rôle de 1939?); "
               "f114 forêts, consistance du domaine soumis au régime forestier. f115 = chapter XI Institutions "
               "d'enseignement et de recherches.",
}
NOT_DONE = ("Transcribed (every printing, every cell read on native-resolution crops): Superficie (agriculture_land), "
            "Cultures diverses (agriculture_crops), cereal yields by zone (agriculture_cereal_zones), principales "
            "cultures by yield class sgt1922-sgt1925 (agriculture_yield_classes), répartition européens / indigènes "
            "sgt1926-sgt1939 (agriculture_cereal_farmers), vigne by contrôle and nationality sgt1922-sgt1925 "
            "(agriculture_vine), oliviers by caïdat / région, all editions (agriculture_olive). NOT YET TRANSCRIBED "
            "(views in the survey above): dattiers by caïdat (sgt1936 f111-112, sgt1939 f110-111); animaux by "
            "contrôle (sgt1927-sgt1939); forêts a) and b) (all editions; sgt1935 f152 to check). Météorologie, école "
            "coloniale d'agriculture, service botanique and laboratoires de chimie belong to the research_ "
            "extraction.")


# Latest printing misprinted: keep the cell of an earlier edition (flag reprint_corrected). key -> edition kept.
PREFER = {(1935, "north", "barley", "area"): "sgt1935",
          (1916, "tunisia", "wheat", "surfaces", "all", "sown", "area"): "sgt1922",
          (1916, "tunisia", "wheat", "surfaces", "all", "taxed", "area"): "sgt1922",
          (1920, "tunisia", "broad_beans", "yield_classes", "european", "yield_5_hl", "area"): "sgt1923",
          (1920, "tunisia", "flax", "yield_classes", "european", "yield_2_hl", "area"): "sgt1923"}


def select(recs, key):
    by = defaultdict(list)
    for r in recs:
        by[tuple(r.get(k) for k in key)].append(r)
    kept, n, diffs = [], 0, []
    for k, rs in by.items():
        rs.sort(key=lambda r: ORDER.index(r["census"]))
        good = [r for r in rs if r["flag"] not in ("illegible",)]
        last = good[-1] if good else rs[-1]
        for r in rs:
            if r is last:
                continue
            if r["value"] is None or last["value"] is None:
                continue
            n += 1
            if r["value"] != last["value"]:
                diffs.append((k, r["census"], r["value"], last["census"], last["value"]))
        pe = PREFER.get(k)
        if pe:
            last = dict([r for r in rs if r["census"] == pe][0], flag="reprint_corrected")
        kept.append(last)
    return kept, n, diffs


def write_survey():
    L = ["# Agriculture chapter: survey of every edition", "",
         "Survey of the *Agriculture* chapter (chapter XI up to sgt1935, chapter X in sgt1936 and sgt1939), view by "
         "view. First and last views confirmed on the page images for every edition (chapter-title page, and the "
         "next chapter title). Extraction: `extract_agriculture.py`.", "",
         "| edition | ark | views |", "|---|---|---|"]
    L += [f"| {e} | `{EDITIONS[e]}` | {a}–{b} |" for e, (a, b) in CHAPTER_VIEWS.items()]
    L += ["", "## Views per edition", ""] + [f"- **{e}**: {t}" for e, t in SURVEY.items()]
    L += ["", "## Tables (CSV)", "", "| CSV | sections | editions | read on the image |", "|---|---|---|---|"]
    L += [f"| `{o}` | {', '.join(sp['secs'])} | {', '.join(sp.get('_eds', []))} | every printing, cell by cell |"
          for o, sp in TABLES.items()]
    L += ["", "## Coverage", "", NOT_DONE, ""]
    (OUT / f"{PREFIX}_survey.md").write_text("\n".join(L) + "\n")


CHECKERS = {"land": chk_land, "crops": chk_crops, "zones": chk_zones, "vine": chk_vine, "olive": chk_olive}
ALL_CHECKERS = {"agriculture_crops": chk_crops_all, "agriculture_cereal_zones": chk_zones_all,
                "agriculture_yield_classes": chk_yc_all, "agriculture_cereal_farmers": chk_split_all}


def build(write=True):
    secs = []
    for ed in ORDER:
        p = TR / f"{PREFIX}_{ed}.txt"
        if p.exists():
            secs += parse(p, ed)
    for s in secs:
        f = CHECKERS.get(s["table"].split("_")[0])
        if f:
            f(s)
    res = {}
    for out, spec in TABLES.items():
        ss = [s for s in secs if s["table"] in spec["secs"]]
        if out in ALL_CHECKERS:
            ALL_CHECKERS[out](ss)
        spec["_eds"] = [e for e in ORDER if any(s["ed"] == e for s in ss)]
        recs = []
        for s in ss:
            recs += spec["cells"](s)
        kept, n, diffs = select(recs, spec["key"])
        order = {id(r): i for i, r in enumerate(recs)}
        kept.sort(key=lambda r: (r["year"], ORDER.index(r["census"]), order.get(id(r), 0)))
        flagged = [f"{r['census']} {r['year']} " + " / ".join(str(r.get(k, "")) for k in spec["key"][1:])
                   + f" = {r['value']} ({r['flag']})" for r in kept if r["flag"]]
        res[out] = dict(rows=len(kept), checks=CHK.n[out], failed=list(CHK.fail[out]), overlap_compared=n,
                        overlap_diffs=[list(x) for x in diffs], flagged=flagged, editions=spec["_eds"])
        if write:
            cols = COMMON + spec["dims"] + ["value", "flag"]
            write_csv(out, cols, kept)
            paras = list(spec.get("paras", []))
            if CHK.fail[out]:
                paras.append("Every failed check below was re-read on a zoomed native-resolution crop: they are "
                             "printed inconsistencies (printed values kept). " + spec.get("fail_note", ""))
            paras.append(f"Survey of the whole chapter in every edition: `{PREFIX}_survey.md`.")
            write_notes(out, CHAPTER, SCRIPT, kept, cols, {c: spec.get("doc", {}).get(c, DOC.get(c)) for c in cols}, spec["title_fr"],
                        spec["title_en"], paras, CHK.n[out], CHK.fail[out], n, diffs, coverage_lines(ss),
                        RULE5 if spec.get("rule5") else RULE4, spec["unit"])
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
