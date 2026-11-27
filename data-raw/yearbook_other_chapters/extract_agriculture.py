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
}


def flag_of(sec, label, col, cell):
    t = sec["table"] + (":" + sec["zone"] if sec.get("zone") else "")
    return FLAGS.get((sec["ed"], t, label, col), cell.flag)


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
NOT_DONE = ("Transcribed (every printing, every cell read on native-resolution crops): Superficie (agriculture_land) "
            "and Cultures diverses (agriculture_crops), all 12 editions; cereal yields by zone (agriculture_cereal_"
            "zones, sgt1926-sgt1939). NOT YET TRANSCRIBED (views in the survey above): principales cultures of "
            "sgt1922-sgt1925 (by tax class / yield class, européennes and indigènes, sgt1925 by zone) and the "
            "répartition de la superficie entre européens et indigènes (sgt1926-sgt1939); vigne by contrôle and nationality (sgt1922-sgt1925); oliviers "
            "by caïdat / région (all editions); animaux by contrôle (sgt1927-sgt1939); dattiers by caïdat "
            "(sgt1936, sgt1939); forêts a) and b) (all editions); météorologie (sgt1922-sgt1930); école coloniale "
            "d'agriculture, service botanique, laboratoires de chimie (sgt1922-sgt1930).")


# Latest printing misprinted: keep the cell of an earlier edition (flag reprint_corrected). key -> edition kept.
PREFER = {(1935, "north", "barley", "area"): "sgt1935"}


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


CHECKERS = {"land": chk_land, "crops": chk_crops, "zones": chk_zones}
ALL_CHECKERS = {"agriculture_crops": chk_crops_all, "agriculture_cereal_zones": chk_zones_all}


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
            write_notes(out, CHAPTER, SCRIPT, kept, cols, {c: DOC[c] for c in cols}, spec["title_fr"],
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
