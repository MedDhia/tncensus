#!/usr/bin/env python3
"""Teaching and research institutions (*Institutions d'enseignement et de recherches*) of the Statistique
générale de la Tunisie: the separate chapter of sgt1935 (XII), sgt1936 and sgt1939 (XI), and the same institutions
printed at the end of the Agriculture chapter in sgt1922-sgt1930 (École coloniale d'agriculture, service botanique,
laboratoires de chimie), plus the meteorology pages.

  python3 extract_research.py check   parse the transcriptions, run every check, print failures
  python3 extract_research.py build   ... and write csv/research_*.csv, their .md notes,
                                      csv/research_survey.md and csv/research_validation.json

Source of truth: transcribed/research_<edition>.txt. Format as in yb_tables.py, with two additions:
  - a row label may end with '{unit}' (unit of that line, ditto marks resolved);
  - meteorology cell tokens: 'g' = printed "gouttes" (traces; stored 0 with printed = gouttes), 'oi' = printed
    "O. I." (observations incomplètes; NA, not_applicable), 'x' = printed "×" (jours non observés; NA,
    not_applicable); '-' = printed dash (pas d'observation; NA, not_applicable).
Yearly series printed for overlapping windows follow SPEC_ADDENDUM rule 4 (each cell from the latest edition
printing it, every other printing compared); tables printed once per edition follow rule 5.
"""
import re
import sys
import unicodedata
from collections import defaultdict
from decimal import Decimal
from pathlib import Path as _Path

sys.path.insert(0, str(_Path(__file__).resolve().parent))  # shared helper yb_tables.py
from yb_tables import (COMMON, EDITIONS, ORDER, OUT, TR, Checks, coverage_lines, ssum,  # noqa: E402
                       write_csv, write_notes, write_validation)

CHAPTER = "Institutions d'enseignement et de recherches"
SCRIPT = "extract_research.py"
PREFIX = "research"
CHK = Checks()

# ----------------------------------------------------------------- parsing

PRINTED = {"g": "gouttes", "oi": "O. I.", "x": "×", "-": "—"}


class Cell:
    __slots__ = ("raw", "value", "flag", "printed")

    def __init__(self, raw):
        self.raw, self.flag, self.printed = raw, "", ""
        t = raw
        if t.endswith("!") and len(t) > 1:
            self.flag, t = "ocr_corrected", t[:-1]
        if t.endswith("*") and len(t) > 1:          # derived from the printed total (cell hidden or cut)
            self.flag, t = "derived_from_totals", t[:-1]
        if t == "?":
            self.value, self.flag = None, "illegible"
        elif t in ("-", "oi", "x"):
            self.value, self.flag, self.printed = None, "not_applicable", PRINTED[t]
        elif t == "g":
            self.value, self.printed = Decimal(0), PRINTED[t]
        else:
            self.value = Decimal(t)

    def __repr__(self):
        return self.raw


UNIT_RE = re.compile(r"\s*\{([^}]*)\}\s*$")


def parse(path, ed):
    secs, cur = [], None
    for n, line in enumerate(path.read_text().splitlines(), 1):
        line = line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("@"):
            head = line[1:]
            name = head.split()[0]
            cur = {"table": name, "ed": ed, "ark": EDITIONS[ed], "rows": [], "cols": None, "img": "", "line": n}
            for k, v1, v2 in re.findall(r'(\w+)=(?:"([^"]*)"|(\S+))', head[len(name):]):
                cur[k] = v1 or v2
            cur["view"], cur["page"] = int(cur["view"]), int(cur["page"])
            secs.append(cur)
            continue
        if line.startswith("img:"):
            cur["img"] = line[4:].strip()
            continue
        if line.startswith("cols:"):
            cur["cols"] = line[5:].split()
            continue
        label, vals = line.rsplit("|", 1)
        label = label.strip()
        unit = None
        m = UNIT_RE.search(label)
        if m:
            unit, label = m.group(1), label[:m.start()].strip()
        cells = [Cell(x) for x in vals.split()]
        if len(cells) != len(cur["cols"]):
            raise ValueError(f"{path.name}:{n} {cur['table']} row {label!r}: "
                             f"{len(cells)} values for {len(cur['cols'])} columns")
        cur["rows"].append({"label": label, "unit": unit, "cells": dict(zip(cur["cols"], cells)), "line": n})
    return secs


# Cells whose flag is not expressible in the transcription tokens: (edition, section, line, column) -> flag.
FLAGS = {
    ("sgt1935", "school_origin", "1931", "tunisia"): "total_mismatch",
    ("sgt1936", "school_origin", "1931", "tunisia"): "total_mismatch",
    ("sgt1939", "school_origin", "1931", "tunisia"): "total_mismatch",
    ("sgt1935", "school_promotions", "17 1919-1921", "dipl_school"): "total_mismatch",
    ("sgt1923", "bot_trials", "Sorghos", "1923"): "total_mismatch",
    ("sgt1923", "bot_seedsales", "Mekki", "1910-18"): "total_mismatch",
    ("sgt1924", "bot_seedsales", "Mekki", "1910-19"): "total_mismatch",
    ("sgt1927", "bot_seedsales", "Biskri glabre", "1910-22"): "total_mismatch",
    ("sgt1922", "bot_trees", "Poirier", "1922p"): "total_mismatch",
    ("sgt1923", "bot_trees", "Poirier", "1922p"): "total_mismatch",
    ("sgt1924", "bot_trees", "Poirier", "1922p"): "total_mismatch",
    ("sgt1923", "bot_trials", "Plantes médicinales", "1923"): "total_mismatch",
    ("sgt1936", "chemlab", "Mouts mutés", "customs"): "row_realigned",
    ("sgt1936", "chemlab", "Pétroles, mazouts, essences", "customs"): "row_realigned",
    ("sgt1936", "chemlab", "Produits alimentaires divers", "customs"): "row_realigned",
    ("sgt1936", "chemlab", "Goudrons, huiles de goudron", "customs"): "total_mismatch",
    ("sgt1927", "chemlab", "Huiles essentielles", "public"): "total_mismatch",
    ("sgt1926", "bot_seedsales", "Huguenot", "1926"): "total_mismatch",
    ("sgt1926", "bot_seedsales", "Jenah Rhetifa", "1926"): "total_mismatch",
    ("sgt1927", "bot_seedsales", "Huguenot", "1926"): "total_mismatch",
    ("sgt1927", "bot_seedsales", "Jenah Rhetifa", "1926"): "total_mismatch",
    ("sgt1928", "school_origin", "1927", "france"): "total_mismatch",
    ("sgt1928", "bot_seedsales", "Biskri glabre", "1910-23"): "total_mismatch",
    ("sgt1928", "bot_seedsales", "Medjerdah", "1910-23"): "total_mismatch",
    ("sgt1928", "bot_seedsales", "Huguenot", "1926"): "total_mismatch",
    ("sgt1928", "bot_seedsales", "Jenah Rhetifa", "1926"): "total_mismatch",
    ("sgt1928", "chemlab", "Spiritueux et liqueurs", "public"): "total_mismatch",
    ("sgt1929", "bot_seedsales", "Biskri glabre", "1910-24"): "total_mismatch",
    ("sgt1929", "bot_seedsales", "Huguenot", "1926"): "total_mismatch",
    ("sgt1929", "bot_seedsales", "Jenah Rhetifa", "1926"): "total_mismatch",
    ("sgt1929", "bot_trees", "Abricotier", "1928p"): "total_mismatch",
    ("sgt1929", "bot_seedsales", "Sbéi", "1910-24"): "total_mismatch",
    ("sgt1929", "bot_seedsales", "Souri", "1910-24"): "total_mismatch",
    ("sgt1929", "chemlab", "Engrais, produits anticryptogamiques", "fraud_good"): "row_realigned",
    ("sgt1929", "chemlab", "Engrais, produits anticryptogamiques", "fraud_suspect"): "row_realigned",
    ("sgt1929", "chemlab", "Epices", "fraud_good"): "row_realigned",
    ("sgt1929", "chemlab", "Epices", "fraud_suspect"): "row_realigned",
    ("sgt1929", "chemlab", "Farines et farineux alimentaires", "fraud_good"): "row_realigned",
    ("sgt1929", "chemlab", "Farines et farineux alimentaires", "fraud_suspect"): "row_realigned",
    ("sgt1930", "bot_seedsales", "Biskri glabre", "1910-25"): "total_mismatch",
    ("sgt1930", "bot_seedsales", "Sbéi", "1910-25"): "total_mismatch",
    ("sgt1930", "bot_seedsales", "Souri", "1910-25"): "total_mismatch",
    ("sgt1930", "bot_seedsales", "Jenah Rhetifa", "1926"): "total_mismatch",
    ("sgt1930", "bot_seedsales", "Huguenot", "1926"): "total_mismatch",
    ("sgt1930", "bot_trees", "Abricotier", "1928p"): "total_mismatch",
    ("sgt1930", "school_enrolment", "1924-1925", "year2"): "total_mismatch",
}


def fl(sec, r, c):
    return FLAGS.get((sec["ed"], sec["table"], r["label"], c), r["cells"][c].flag)


def where(sec):
    return f"{sec['ed']} p.{sec['page']} (f{sec['view']}) {sec['table']}" + "".join(
        f" [{sec[k]}]" for k in ("side", "service", "group", "lab", "part", "region", "controle") if sec.get(k))


TOT = re.compile(r"(?i)^(totaux|total)\b")


def is_tot(label):
    return TOT.match(label) is not None


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+", "_", s.lower()).strip("_")
    return s


def base(sec, year):
    return {"census": sec["ed"], "table_id": sec["table"], "gallica_ark": sec["ark"], "source_page": sec["page"],
            "gallica_view": sec["view"], "year": year}


def data_rows(sec):
    return [r for r in sec["rows"] if not is_tot(r["label"])]


def check_block_total(out, sec, cols=None, skip=lambda r: False):
    """Every printed Total line = sum of the data lines above it (since the previous total line)."""
    cols = cols or sec["cols"]
    block = []
    for r in sec["rows"]:
        if is_tot(r["label"]):
            blk = [x for x in block if x["unit"] == r["unit"]]   # a total adds up the lines in its own unit
            for c in cols:
                CHK.eq(out, f"{where(sec)} {c}: lines vs {r['label']}",
                       ssum(x["cells"][c].value for x in blk), r["cells"][c].value)
            block = []
        elif not skip(r):
            block.append(r)


def check_row_total(out, sec, parts, total="total"):
    for r in sec["rows"]:
        c = r["cells"]
        CHK.eq(out, f"{where(sec)} {r['label']}: {total} = sum", ssum(c[p].value for p in parts if p in c),
               c[total].value)


# ----------------------------------------------------------------- tables

def cells_items(sec, dim, dim_fr_key):
    """Item tables (one value per line): Institut Pasteur budget / work, Institut Arloing."""
    out = []
    for r in data_rows(sec):
        cell = r["cells"]["value"]
        d = {dim: slug(sec[dim_fr_key]) if sec.get(dim_fr_key) else "", f"{dim}_fr": sec.get(dim_fr_key, "")}
        out.append(dict(base(sec, int(sec["year"])), **d, item=slug(r["label"]), item_fr=r["label"],
                        unit=r["unit"], value=cell.value, flag=fl(sec, r, "value")))
    return out


SIDE = {"receipts": "Recettes", "expenditure": "Dépenses"}


def cells_budget(sec):
    out = []
    for r in data_rows(sec):
        cell = r["cells"]["value"]
        out.append(dict(base(sec, int(sec["year"])), side=sec["side"], side_fr=SIDE[sec["side"]],
                        item=slug(r["label"]), item_fr=r["label"], unit=r["unit"], value=cell.value, flag=fl(sec, r, "value")))
    return out


def chk_items(out):
    def f(sec):
        # 'Nombre total des analyses pratiquées' is not the sum of the principal analyses printed: not a total line
        check_block_total(out, sec, skip=lambda r: r["label"].startswith("Nombre total des analyses"))
    return f


ORIGIN = {"france": "France", "tunisia": "Tunisie", "algeria": "Algérie", "colonies": "Colonies",
          "abroad": "Étranger"}


def cells_origin(sec):
    out = []
    for r in data_rows(sec):
        for c, cfr in ORIGIN.items():
            cell = r["cells"][c]
            per = r["label"].replace("-", " à ")
            out.append(dict(base(sec, int(r["label"].split("-")[-1])), period=per, origin=c, origin_fr=cfr, value=cell.value, flag=fl(sec, r, c)))
    return out


def chk_origin(sec):
    o = "research_school_origin"
    check_row_total(o, sec, list(ORIGIN))
    check_block_total(o, sec)


PROMO = {"year1": ("regular_students_year1", "Élèves réguliers pendant la 1re année d'études"),
         "year2": ("regular_students_year2", "Élèves réguliers pendant la 2e année d'études"),
         "dipl_eng": ("diploma_engineer", "Élèves diplômés : diplôme d'ingénieur"),
         "dipl_school": ("diploma_school", "Élèves diplômés : diplôme de l'École"),
         "certificate": ("certificate_of_studies", "Élèves diplômés : certificat d'études")}


def cells_promotions(sec):
    out = []
    for r in data_rows(sec):
        num, period = r["label"].split()
        for c in sec["cols"]:
            m, mfr = PROMO[c]
            cell = r["cells"][c]
            out.append(dict(base(sec, int(sec["year"])), promotion=int(num), promotion_years=period, measure=m,
                            measure_fr=mfr, value=cell.value, flag=fl(sec, r, c)))
    return out


def chk_promotions(sec):
    check_block_total("research_school_promotions", sec)


ENROL = {"year1": ("regular_students_year1", "Élèves réguliers en 1re année"),
         "year2": ("regular_students_year2", "Élèves réguliers en 2e année"),
         "auditors": ("auditors", "Auditeurs libres")}


def cells_enrolment(sec):
    out = []
    for r in data_rows(sec):
        for c, (m, mfr) in ENROL.items():
            cell = r["cells"][c]
            out.append(dict(base(sec, int(r["label"].split("-")[1])), school_year=r["label"], measure=m,
                            measure_fr=mfr, value=cell.value, flag=fl(sec, r, c)))
    return out


def chk_enrolment(sec):
    o = "research_school_enrolment"
    check_row_total(o, sec, list(ENROL))
    check_block_total(o, sec, cols=list(ENROL) + (["total"] if any(
        r["cells"]["total"].value is not None for r in sec["rows"] if is_tot(r["label"])) else []))


SEED_PART = {"seeds": "Semences pédigrées produites par le Service",
             "controlled": "Cultures pédigrées pour semences soumises au contrôle",
             "analyses": "Analyses de la qualité des blés et farines"}


def ycols(sec):
    return [c for c in sec["cols"] if c.isdigit()]


def cells_seeds(sec):
    out = []
    for r in data_rows(sec):
        for c in ycols(sec):
            cell = r["cells"][c]
            out.append(dict(base(sec, int(c)), part=sec["part"], part_fr=SEED_PART[sec["part"]],
                            item=slug(re.sub(r"\s*\((Ha\.|hectares|quintaux)\)", "", r["label"])), item_fr=r["label"], unit=r["unit"], value=cell.value,
                            flag=fl(sec, r, c)))
    return out


def chk_seeds(sec, allsecs=None):
    o = "research_botanical_seeds"
    check_block_total(o, sec, cols=ycols(sec))
    for c in sec["cols"]:
        m = re.match(r"m(\d{4})_(\d{4})$", c)
        if not m:
            continue
        a, b = int(m.group(1)), int(m.group(2))
        yrs = [str(y) for y in range(a, b + 1)]
        if not all(y in sec["cols"] for y in yrs):
            continue
        for r in sec["rows"]:
            vals = [r["cells"][y].value for y in yrs]
            s = ssum(vals)
            if s is None or r["cells"][c].value is None:
                continue
            pv = r["cells"][c].value
            q = Decimal(1).scaleb(pv.as_tuple().exponent)       # printed precision
            CHK.eq(o, f"{where(sec)} {r['label']}: average {a}-{b}", (s / len(yrs)).quantize(q), pv,
                   tol=q / 2 + Decimal("0.01"))


def season_of(col):
    y = int(col[:4])
    return f"{y - 1}-{str(y)[2:]}", y


TREE_M = {"p": ("plants", "Plants"), "g": ("grafts", "Greffons")}


def cells_trees(sec):
    out = []
    grp = "other" if sec["table"] == "bot_trees_other" else "fruit"
    grp_fr = "Arbres, arbustes et plantes diverses" if grp == "other" else "Arbres fruitiers"
    for r in data_rows(sec):
        for c in sec["cols"]:
            season, y = season_of(c)
            m, mfr = TREE_M[c[4]]
            cell = r["cells"][c]
            sk = "other_species" if grp == "other" else r["label"]
            out.append(dict(base(sec, y), group=grp, group_fr=grp_fr, season=season, species=r["label"], _sk=sk,
                            measure=m, measure_fr=mfr, unit="count", value=cell.value, flag=fl(sec, r, c)))
    return out


def chk_trees(sec):
    check_block_total("research_botanical_trees", sec)


CHEM = {"customs": ("customs", "Douanes"),
        "fraud_good": ("fraud_repression_good", "Répression des fraudes : échantillons reconnus bons"),
        "fraud_suspect": ("fraud_repression_suspect", "Répression des fraudes : échantillons reconnus suspects"),
        "indirect_good": ("indirect_taxes_good", "Contributions indirectes : échantillons reconnus bons"),
        "indirect_suspect": ("indirect_taxes_suspect", "Contributions indirectes : échantillons reconnus suspects"),
        "other_admin": ("other_administrations", "Autres administrations"),
        "studies": ("studies_research", "Études et recherches"),
        "public": ("paid_public", "Analyses payantes pour le public")}


def cells_chem(sec):
    out = []
    for r in data_rows(sec):
        for c in sec["cols"]:
            if c == "total":
                continue
            s, sfr = CHEM[c]
            cell = r["cells"][c]
            out.append(dict(base(sec, int(sec["year"])), laboratory=sec["lab"], sample=slug(r["label"]),
                            sample_fr=r["label"], service=s, service_fr=sfr, value=cell.value, flag=fl(sec, r, c)))
    return out


def chk_chem(sec):
    o = "research_chemistry_lab"
    check_row_total(o, sec, [c for c in sec["cols"] if c != "total"])
    check_block_total(o, sec)


TRIAL_SEC = {"agricole": "Section agricole", "horticole": "Section horticole"}


def cells_trials(sec):
    out = []
    for r in data_rows(sec):
        for c in sec["cols"]:
            if c == "total":
                continue
            cell = r["cells"][c]
            if c == "prior":
                y, season = None, "Total antérieur (avant " + sec["first"] + ")"
            else:
                season, y = season_of(c)
            out.append(dict(base(sec, y), section=sec["section"], section_fr=TRIAL_SEC[sec["section"]],
                            season=season, plant=slug(r["label"]), plant_fr=r["label"], value=cell.value,
                            flag=fl(sec, r, c)))
    return out


def chk_trials(sec):
    o = "research_botanical_trials"
    check_row_total(o, sec, [c for c in sec["cols"] if c != "total"])
    check_block_total(o, sec)


def cells_seedsales(sec):
    out = []
    for r in data_rows(sec):
        for c in sec["cols"]:
            if c == "total":
                continue
            cell = r["cells"][c]
            if "-" in c:
                a, b = c.split("-")
                season, y = c, int(a[:2] + b)
            else:
                season, y = season_of(c)
            out.append(dict(base(sec, y), crop_group=sec["group"], season=season, variety=r["label"],
                            unit="kilogrammes", value=cell.value, flag=fl(sec, r, c)))
    return out


def chk_seedsales(sec):
    o = "research_botanical_seed_sales"
    check_row_total(o, sec, [c for c in sec["cols"] if c != "total"])
    check_block_total(o, sec, cols=[c for c in sec["cols"] if c != "total"])


RULE4 = ("Selection (SPEC_ADDENDUM rule 4): each cell is stored once, from the latest edition printing it; every "
         "other printing of the same cell is compared below.")
RULE5 = ("Selection (SPEC_ADDENDUM rule 5): printed once per edition (the edition's year); all editions kept.")

DOC = {
    "census": "source edition (`sgt1922` ... `sgt1939`)",
    "table_id": "section code of the transcription",
    "gallica_ark": "Gallica volume ark", "source_page": "printed page number", "gallica_view": "Gallica view",
    "year": "year of the figure (for a school year or season: the year it ends; for promotions and once-per-edition "
            "tables: the edition year)",
    "side": "`receipts` or `expenditure`", "side_fr": "Recettes / Dépenses",
    "service": "service of the Institut (ASCII slug of `service_fr`)", "service_fr": "service heading as printed",
    "group": "group heading (ASCII slug of `group_fr`)", "group_fr": "group heading as printed",
    "item": "ASCII slug of `item_fr`", "item_fr": "line as printed (sub-heading prefixed, ditto marks expanded)",
    "unit": "unit of the line (francs, persons, analyses, doses, flacons, cc, tubes, ampoules, litres, samples, "
            "quintals, hectares, producers, count)",
    "period": "year of entry as printed (sgt1939 prints 1899-1913 as one line, '1899 à 1913')",
    "origin": "place of origin (france, tunisia, algeria, colonies, abroad)", "origin_fr": "column heading",
    "promotion": "promotion number (1 = 1898-1900)", "promotion_years": "years of the promotion as printed",
    "measure": "what is counted", "measure_fr": "column heading as printed",
    "school_year": "school year as printed",
    "part": "part of the table", "part_fr": "part heading as printed",
    "season": "season (année) as printed", "species": "species as printed",
    "section": "section of the trials table (agricole, horticole)", "section_fr": "section heading",
    "plant": "ASCII slug of `plant_fr`", "plant_fr": "nature des plantes as printed",
    "crop_group": "crop heading as printed (Blés durs, Blés tendres, Orges, Avoines)",
    "variety": "variety as printed",
    "laboratory": "laboratory (Tunis, Sfax)", "sample": "ASCII slug of `sample_fr`",
    "sample_fr": "nature des échantillons, as printed",
    "value": "printed figure (» = 0)",
    "flag": "empty, or ocr_corrected / illegible / total_mismatch / derived_from_totals / not_applicable / "
            "reprint_corrected / row_realigned",
}

TABLES = {
    "research_pasteur_budget": dict(
        secs=["pasteur_budget"], cells=cells_budget, check=chk_items("research_pasteur_budget"), rule5=True,
        key=["year", "side", "item"], dims=["side", "side_fr", "item", "item_fr", "unit"],
        title_fr="Institut Pasteur. a) Budget", title_en="Institut Pasteur of Tunis: budget (receipts and "
        "expenditure)", unit="Unit: francs (centimes as decimals); value_type: francs.",
        paras=["Printed totals (Total des recettes, Total des dépenses) are checks only."]),
    "research_pasteur_activity": dict(
        secs=["pasteur_work"], cells=lambda s: cells_items(s, "service", "service"),
        check=chk_items("research_pasteur_activity"), rule5=True,
        key=["year", "service", "item"], dims=["service", "service_fr", "item", "item_fr", "unit"],
        title_fr="Institut Pasteur. b) Travaux de l'Institut ; c) Service vétérinaire",
        title_en="Institut Pasteur of Tunis: work of the institute (rabies treatments, analyses, vaccines and sera "
                 "distributed, veterinary service)",
        unit="Units per line (`unit`): persons, analyses, doses, flacons, cc, ampoules, tubes, litres, samples; "
             "value_type: mixed (counts in the printed unit).",
        paras=["The 'Nombre total des analyses pratiquées' is printed with only the principal analyses itemised "
               "('les principales ont été'): it is stored as its own line and not checked. Printed sub-totals "
               "(Mordues: total; Vaccin anticlaveleux: au total) are checks only."]),
    "research_arloing_analyses": dict(
        secs=["arloing"], cells=lambda s: cells_items(s, "group", "group"), check=chk_items("research_arloing_analyses"),
        rule5=True, key=["year", "group", "item"], dims=["group", "group_fr", "item", "item_fr", "unit"],
        title_fr="Institut Arloing. Analyses microbiologiques en vue des diagnostics",
        title_en="Institut Arloing (veterinary bacteriology): diagnostic analyses by animal group and disease, "
                 "chemical and wool analyses, auto-vaccines",
        unit="Units: analyses (count), doses for the auto-vaccines (`unit`); value_type: count.", paras=[]),
    "research_school_origin": dict(
        secs=["school_origin"], cells=cells_origin, check=chk_origin, key=["period", "origin"],
        dims=["period", "origin", "origin_fr"],
        title_fr="École coloniale d'agriculture. a) Lieu d'origine des élèves entrés à l'École",
        title_en="Colonial school of agriculture (Tunis): students entering the school, by place of origin",
        unit="Unit: students (count); value_type: count.",
        fail_note='sgt1928 prints 1927 France 72 for 27 (sgt1927 and sgt1929 print 27; the row total 46 and the column total 789 need 27): flagged total_mismatch.',
        paras=["The school was closed during the 1914-1918 war (no line 1914-1918). Row totals (Totaux column) and "
               "the column totals since 1899 are checks only."]),
    "research_school_promotions": dict(
        secs=["school_promotions"], cells=cells_promotions, check=chk_promotions,
        key=["promotion", "measure"], dims=["promotion", "promotion_years", "measure", "measure_fr"],
        title_fr="École coloniale d'agriculture. b) Promotions",
        title_en="Colonial school of agriculture: regular students and diplomas by promotion",
        unit="Unit: students (count); value_type: count.",
        paras=["Rule 4 by promotion: each promotion is stored from the latest edition printing it (`year` = that "
               "edition's year), so the figures of promotions still studying are those of the latest printing. "
               "Printed '(2) promotions en cours d'études' in place of a figure: NA, not_applicable."]),
    "research_school_enrolment": dict(
        secs=["school_enrolment"], cells=cells_enrolment, check=chk_enrolment, key=["school_year", "measure"],
        dims=["school_year", "measure", "measure_fr"],
        title_fr="École coloniale d'agriculture. c) Effectif par année scolaire",
        title_en="Colonial school of agriculture: enrolment by school year (regular students in first and second "
                 "year, auditors)",
        unit="Unit: students (count); value_type: count.",
        fail_note='Auditeurs libres: the printed column total runs 9-10 short in sgt1923-sgt1927 (sgt1922 adds up; from sgt1923 the printed total grows by less than the new lines, and every edition carries the shortfall forward), and is 5 over in sgt1935; every auditor cell agrees with its printed row total, so the faulty figure is the printed column total (not stored). sgt1924 1re année total 977 for 877 and sgt1935 2e année total 1.061 for 1.069: printed column-total errors (cells agree with the row totals). The same 10-short auditor total is carried in sgt1928-sgt1930. sgt1930: 1924-1925 row total printed 116 for 124 (2e année 59 read on the crop; the 2e année column total 907 also leaves out 8). ',
        paras=["Row totals (Totaux column) and column totals are checks only."]),
    "research_botanical_seeds": dict(
        secs=["bot_seeds"], cells=cells_seeds, check=chk_seeds, key=["year", "part", "item"],
        dims=["part", "part_fr", "item", "item_fr", "unit"],
        title_fr="Service botanique et agronomique. a) Semences pédigrées produites par le Service",
        title_en="Botanical and agronomic service: pedigree seed produced, controlled pedigree seed crops, wheat "
                 "and flour analyses",
        unit="Units: quintals, hectares, producers, analyses (`unit`); value_type: mixed.",
        fail_note='sgt1935: Moyenne 1931-1935 of Blés durs (100.1 for 100.6) and of the hectare Total (868.4 for 869.6) and the hectare Total of 1935 (471 for 465) are printed errors in the averages/total lines (not stored). Blés tendres de force (Ha.) 1934 reads 90 on the zoomed crop (earlier transcribed 99): it fits the 1934 total 702 and the average 105.2.',
        paras=["Printed averages (Moyenne) are checks only, against the mean of the printed years (to 0.1); "
               "an average whose years are not all printed in the same table is not stored."]),
    "research_botanical_trials": dict(
        secs=["bot_trials"], cells=cells_trials, check=chk_trials, key=["season", "section", "plant"],
        dims=["section", "section_fr", "season", "plant", "plant_fr"],
        title_fr="Service botanique. a) Nature et nombre des essais de variétés nouvelles",
        title_en="Botanical service: number of trials of new varieties, by nature of the plants and season",
        unit="Unit: trials (count); value_type: count.",
        paras=["The 'Total antérieur' column (all trials before the first season printed) is stored with `year` "
               "empty and `season` naming the edition's first season; it changes from edition to edition and is "
               "compared only between editions printing the same first season. Total général and Totaux are checks "
               "only."]),
    "research_botanical_seed_sales": dict(
        secs=["bot_seedsales"], cells=cells_seedsales, check=chk_seedsales, key=["season", "crop_group", "variety"],
        dims=["crop_group", "season", "variety", "unit"],
        title_fr="Service botanique. b) Vente de semences de variétés pédigrées",
        title_en="Botanical service: sales of pedigree seed, by variety and season (kilogrammes)",
        unit="Unit: kilogrammes; value_type: count (weight in kg).",
        fail_note='Row totals printed wrongly, cells agreeing with the neighbouring editions: sgt1922 Hamira (10.320 for 10.380), sgt1923 Autres variétés (6.690 for 6.670), sgt1922 Richelle hâtive (44.702 for 47.702), sgt1924 Biskri glabre (6.550 for 6.450), Hamira (11.260 for 11.360), Avoines de Perse (100 for 300), sgt1925 Azizi (2.355 for 1.355); sgt1924 Totaux of 1923-24 (11.725 for 11.825; sgt1925 prints 11.825). sgt1924 Adjini: the first column 2.750 (carried on in sgt1925-sgt1927) exceeds sgt1923 1.350 + 800 = 2.150 by 600, and the row total 3.640 fits neither; printed, kept unflagged as the faulty figure cannot be told. Cells contradicting the neighbouring editions are flagged total_mismatch (sgt1923/1924 Mekki first column, sgt1927 Biskri glabre 1910-22 3.360 for 3.350). sgt1926 and sgt1927, season 1925-26: Huguenot prints 500 and Jenah Rhetifa 50, whereas both row totals (3.441, 4.400) need 550 and 0; both cells are flagged total_mismatch. sgt1928-sgt1930 carry the Huguenot/Jenah Rhetifa 1925-26 cells (flagged in every printing) and the Biskri glabre first-column error (3.860, 6.460, 8.810, flagged); sgt1929 first column Sbéi 8.175 and Souri 14.705 (for 8.195, 14.765; carried in sgt1930 as 8.885, 15.205), flagged. Printed row or column totals only: sgt1928 Blés durs Totaux 1910-23 (92.555 for 92.955), Florence (7.830 for 7.810), Blés tendres Totaux 1927-28 (8.800 for 8.880, repeated in sgt1929 and sgt1930); sgt1928 Medjerdah 1910-23 360 against 300 everywhere else (flagged); sgt1929 Huguenot (3.814 for 3.841, repeated in sgt1930), de Laconie (1.150); sgt1930 three Blés tendres row totals printed one line off (Pusa Florence 67.097, Richelle hâtive 2.740, Richelle tardive 1.190), Autres variétés 2.500 for 2.590, Blés tendres Totaux 1910-25 128.782 for 118.782, Avoines Crême 113.460 for 121.770, de Laconie 1.400 for 1.250, Totaux 1929-30 1.800 for 1.300.',
        paras=["The first column groups several seasons as printed (e.g. 1910-17); `year` is its last year. Total "
               "par variété and the Totaux lines are checks only."]),
    "research_botanical_trees": dict(
        secs=["bot_trees", "bot_trees_other"], cells=cells_trees, check=chk_trees,
        key=["season", "group", "_sk", "measure"],
        dims=["group", "group_fr", "season", "species", "measure", "measure_fr", "unit"],
        title_fr="Service botanique et agronomique. b) Ventes d'arbres et de plantes diverses",
        title_en="Botanical and agronomic service: sales of fruit trees (plants and grafts) and other plants, by "
                 "species and season",
        unit="Unit: plants or grafts (count); value_type: count.",
        fail_note='sgt1927: the greffons of 1926-27 add up to 676 against a printed total of 726 (and the livraisons 3.171 use 726); the faulty species cell cannot be identified. sgt1927 cumulative plants: livraisons printed 29.662 whereas the season totals give 29.462 and the Total général 371.270 = 29.462 + 341.808, so the livraisons figure is misprinted; greffons: the livraisons antérieures are misprinted 283.047 for 183.047 (Total général 186.218 = 3.171 + 183.047; likewise sgt1924 Total général 285.055 for 185.055): printed. All re-read on zoomed crops. sgt1928 repeats the 726; sgt1929 and sgt1930 print 676 but their livraisons (2.828, 6.008) still include the 50. sgt1928-sgt1930: the plants livraisons exceed the season totals by 3.943 in each edition (printed). sgt1929 and sgt1930 print Abricotier 1927-28 plants 57 for 572 (column total 5.181): flagged total_mismatch, the cell kept from sgt1928 (reprint_corrected).',
        paras=["The cumulative deliveries printed under the table (livraisons of the five seasons, antérieures since "
               "1893, total général) are checks only; the antérieures figures are reported in the validation "
               "file."]),
    "research_chemistry_lab": dict(
        secs=["chemlab"], cells=cells_chem, check=chk_chem, rule5=True, key=["year", "laboratory", "sample",
                                                                             "service"],
        dims=["laboratory", "sample", "sample_fr", "service", "service_fr"],
        title_fr="Laboratoire de chimie. Analyses effectuées",
        title_en="Chemistry laboratories (Tunis, Sfax): analyses made, by nature of the sample and requesting "
                 "service",
        unit="Unit: analyses (count); value_type: count.",
        fail_note='sgt1927 Tunis Huiles essentielles: the 1 printed under Analyses payantes contradicts both the row total (6) and the column total (2.337); flagged total_mismatch. sgt1928 Tunis Spiritueux et liqueurs: row total printed 10 and the public cell », where the column totals need public 10 and row total 73 (public flagged total_mismatch). sgt1929 Tunis: grand total 6.674 for 6.666 (sum of the service totals). sgt1929 Tunis Engrais/Epices/Farines fraud cells printed one line high (realigned, row_realigned). sgt1930 Sfax: Études column total 185 for 183 and grand total 2.939 for 2.941.',
        paras=["Row totals (Totaux par catégories) and column totals (Totaux par service) are checks only."]),
}

# Views confirmed on the page images (first and last view of the pages surveyed; next chapter title noted).
CHAPTER_VIEWS = {
    "sgt1922": "255-279 (météorologie f255-f273; institutions f274-f279; f280 blank; f281 chapter XII)",
    "sgt1923": "745-770", "sgt1924": "1247-1274", "sgt1925": "309-341", "sgt1926": "819-851",
    "sgt1927": "282-313", "sgt1928": "806-841", "sgt1929": "284-319", "sgt1930": "818-856",
    "sgt1935": "155-184 (f185 chapter XIII Commerce et navigation)",
    "sgt1936": "116-145 (f146 chapter XII Commerce et navigation)",
    "sgt1939": "115-122 (f123 chapter XII Commerce et navigation)",
}

SURVEY = {
    "sgt1922": "Inside chapter XI Agriculture. f255-f259 Météorologie a) relevé pluviométrique de l'année agricole "
               "1921-1922; f260-f269 b) année solaire 1922 (mm and days per month); f270|f271 c) données "
               "climatologiques 1922; f272|f273 d) statistique thermométrique 1911-1920 [météorologie not yet "
               "transcribed]. f274 École coloniale d'agriculture a) lieu d'origine des élèves (1898-1922) "
               "[transcribed]; f275 b) promotions (1898-1922) [transcribed]; f276 c) effectif par année scolaire "
               "[transcribed]; f277 Service botanique a) nature et nombre des essais de variétés nouvelles "
               "(1912-1922) [transcribed]; f278 b) vente de semences de variétés pédigrées (1910-1922) "
               "[transcribed]; f279 c) ventes d'arbres et de plantes diverses (1917-1922) [transcribed]; f280 "
               "blank; f281 chapter XII.",
    "sgt1923": "Inside chapter XI Agriculture. f745-f749 Météorologie a) relevé pluviométrique de l'année agricole 1922-1923 (pluies totales par saison et pour l'année, with the 1901-1910 normal); f750-f759 b) relevé pluviométrique de l'année solaire 1923 (millimètres de pluie on the left page, nombre de jours on the right, per station and month); f760|f761 c) données climatologiques essentielles 1923 par les principales régions; f762-f764 d) pluviométrie agricole des années 1900-1901 à 1919-1920 (seasonal and annual means by five-year period) [météorologie not yet transcribed]. f765 École coloniale d'agriculture a) lieu d'origine (1898-1923); f766 b) promotions; f767 c) effectif; f768 Service botanique a) essais de variétés nouvelles (1913-1923); f769 b) vente de semences (1910-1923); f770 c) ventes d'arbres et de plantes (1918-1923) [all transcribed]; f771 chapter XII.",
    "sgt1924": "Inside chapter XI Agriculture. f1247-f1251 Météorologie a) relevé pluviométrique de l'année agricole 1923-1924; f1252-f1263 b) année solaire 1924 (mm | jours spreads); f1264|f1265 c) données climatologiques essentielles 1924; f1266-f1268 d) moyennes pluviométriques mensuelles, saisonnières et annuelles pour la période décennale 1911-1920 [météorologie not yet transcribed]. f1269 École coloniale a) lieu d'origine; f1270 b) promotions; f1271 c) effectif; f1272 Service botanique a) essais (1914-1924); f1273 b) vente de semences (1910-1924); f1274 c) ventes d'arbres (1919-1924) [all transcribed]; f1275 chapter XII.",
    "sgt1925": "Inside chapter XI Agriculture. f309-f315 Météorologie a) relevé pluviométrique de l'année agricole 1924-1925; f316-f329 b) année solaire 1925 (mm | jours spreads); f330|f331 c) données climatologiques essentielles 1925; f332-f334 d) pluviométrie agricole des années 1900-1901 à 1924-1925 (five-year means) [météorologie not yet transcribed]. f335 École coloniale a) lieu d'origine; f336 b) promotions; f337 c) effectif; f338 Service botanique a) essais (1915-1925); f339 b) vente de semences (1910-1925); f340 c) ventes d'arbres (1920-1925); f341 laboratoire de chimie (Tunis) 1925 [all transcribed]; f342 blank; f343 chapter XII.",
    "sgt1926": "Inside chapter XI Agriculture. f819-f825 Météorologie a) relevé pluviométrique de l'année agricole 1925-1926; f826-f839 b) année solaire 1926 (mm | jours spreads; signes conventionnels — pas d'observation, × pluie non mesurée, O gouttes, OI observations incomplètes); f840|f841 c) données climatologiques essentielles 1926; f842-f845 d) températures moyennes et extrêmes mensuelles, saisonnières et annuelles de la période 1901-1925 [météorologie not yet transcribed]. f846 École coloniale a) lieu d'origine; f847 b) promotions; f848 c) effectif; f849 Service botanique a) vente de semences (1910-1926); f850 b) ventes d'arbres (1921-1926); f851 laboratoire de chimie (Tunis) 1926 [all transcribed]; f852 blank; f853 chapter XII.",
    "sgt1927": "Inside chapter XI Agriculture. f282-f287 Météorologie a) relevé pluviométrique de l'année agricole 1926-1927; f288-f303 b) année solaire 1927 (mm | jours spreads); f304|f305 c) données climatologiques essentielles 1927; f306|f307 d) période 1901-1925, pluies moyennes mensuelles, saisonnières et annuelles (année agricole à partir de septembre) [météorologie not yet transcribed]. f308 École coloniale a) lieu d'origine; f309 b) promotions; f310 c) effectif; f311 Service botanique a) vente de semences (1910-1927); f312 b) ventes d'arbres (1922-1927); f313 laboratoire de chimie (Tunis) 1927 [all transcribed]; f314 blank; f315 chapter XII.",
    "sgt1928": "Inside chapter XI Agriculture. f806-f835 Météorologie [not yet transcribed]. f836 École coloniale a) lieu d'origine (1898-1928); f837 b) promotions; f838 c) effectif; f839 Service botanique a) vente de semences (1910-1928); f840 b) ventes d'arbres (1923-1928); f841 laboratoire de chimie (Tunis) 1928 [all transcribed].",
    "sgt1929": "Inside chapter XI Agriculture. f284-f312 Météorologie [not yet transcribed]. f313 École coloniale a) lieu d'origine (1898-1929); f314 b) promotions; f315 c) effectif; f316 Service botanique a) vente de semences (1910-1929); f317 b) ventes d'arbres (1924-1929); f318 laboratoire de chimie (Tunis) 1929; f319 laboratoire de chimie (Sfax) 1929 [all transcribed].",
    "sgt1930": "Inside chapter XI Agriculture. f818-f849 Météorologie [not yet transcribed]. f850 Institutions d'enseignement et de recherches: École coloniale a) lieu d'origine (1898-1930); f851 b) promotions; f852 c) effectif; f853 Service botanique a) vente de semences (1910-1930); f854 b) ventes d'arbres (1925-1930); f855 laboratoire de chimie (Tunis) 1930 (with Contributions indirectes columns); f856 laboratoire de chimie (Sfax) 1930 [all transcribed].",
    "sgt1935": "f155 chapter XII title (Institutions d'enseignement et de recherches); f156 Institut Pasteur a) "
               "budget, b) travaux de l'Institut [transcribed]; f157 c) service vétérinaire [transcribed]; f158 "
               "Institut Arloing, analyses microbiologiques [transcribed]; f159 École coloniale d'agriculture a) "
               "lieu d'origine (1899-1935) [transcribed]; f160 b) promotions [transcribed]; f161 c) effectif "
               "[transcribed]; f162 Service botanique et agronomique a) semences pédigrées (1931-1935) "
               "[transcribed]; f163 b) ventes d'arbres et de plantes (1930-31 à 1934-35) [transcribed]; f164 "
               "laboratoire de chimie (Tunis) 1935 [transcribed]; f165 laboratoire de chimie (Sfax) 1935 "
               "[transcribed]; f166-f183 relevé pluviométrique de l'année 1935 (nine two-page spreads, by "
               "station and month) [not yet transcribed]; f184 blank; f185 chapter XIII Commerce et navigation.",
    "sgt1936": "f116 chapter XI title; f117 Institut Pasteur a) budget, b) travaux [transcribed]; f118 c) service "
               "vétérinaire [transcribed]; f119 Institut Arloing [transcribed]; f120 École coloniale, lieu "
               "d'origine (1899-1936) [transcribed]; f121 Service botanique et agronomique, semences pédigrées "
               "(1934-1936) [transcribed]; f122 laboratoires de chimie Tunis et Sfax 1936 [transcribed]; "
               "f123-f144 relevé pluviométrique 1936 (eleven two-page spreads) [not yet transcribed]; f145 blank; "
               "f146 chapter XII Commerce et navigation.",
    "sgt1939": "f115 chapter XI title; f116 Institut Pasteur a) budget, b) travaux [transcribed]; f117 c) service "
               "vétérinaire [transcribed]; f118 Institut Arloing [transcribed]; f119 École coloniale, lieu "
               "d'origine (1899-1913 as one line, 1919-1939) [transcribed]; f120 Service botanique et agronomique, "
               "semences pédigrées (1935-1939) [transcribed]; f121 statistique des analyses du laboratoire de "
               "chimie, 13 rue de Rome, 1939 [transcribed]; f122 blank; f123 chapter XII Commerce et navigation. "
               "No meteorology printed.",
}
NOT_DONE = ('Transcribed (every cell read on native-resolution crops): the separate chapter of sgt1935 (f156-f165), sgt1936 (f117-f122) and sgt1939 (f116-f121), and the institutions inside the Agriculture chapter of sgt1922 (f274-f279), sgt1923 (f765-f770), sgt1924 (f1269-f1274), sgt1925 (f335-f341), sgt1926 (f846-f851), sgt1927 (f308-f313), sgt1928 (f836-f841), sgt1929 (f313-f319) and sgt1930 (f850-f856). NOT YET TRANSCRIBED: all meteorology: rainfall 1935 (sgt1935 f166-f183), 1936 (sgt1936 f123-f144), and the Météorologie pages of sgt1922 (f255-f273), sgt1923 (f745-f764), sgt1924 (f1247-f1268), sgt1925 (f309-f334), sgt1926 (f819-f845), sgt1927 (f282-f307), sgt1928 (f806-f835), sgt1929 (f284-f312), sgt1930 (f818-f849).')

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
            if r is last or r["value"] is None or last["value"] is None:
                continue
            n += 1
            if r["value"] != last["value"]:
                diffs.append((k, r["census"], r["value"], last["census"], last["value"]))
        pe = PREFER.get(k)
        if pe:
            last = dict([r for r in rs if r["census"] == pe][0], flag="reprint_corrected")
        kept.append(last)
    return kept, n, diffs


PREFER = {("1927-28", "fruit", "Abricotier", "plants"): "sgt1928"}  # sgt1929 prints 57 for 572
EXTRA_CHECKS = []


def chk_cum(secs):
    """Cumulative deliveries under the tree-sales table: livraisons of the printed seasons = sum of the season
    totals; total général = livraisons + antérieures."""
    o = "research_botanical_trees"
    info = []
    for s in secs:
        if s["table"] != "bot_trees_cum":
            continue
        rows = s["rows"]
        liv, ant, tg = rows[0]["cells"], rows[1]["cells"], rows[2]["cells"]
        for c in s["cols"]:
            CHK.eq(o, f"{where(s)} {c}: total général = livraisons + antérieures",
                   ssum([liv[c].value, ant[c].value]), tg[c].value)
        tab = [x for x in secs if x["ed"] == s["ed"] and x["table"] == (
            "bot_trees_other" if s["group"] == "other" else "bot_trees")]
        if tab:
            t = tab[0]
            if s["group"] == "other":
                tot = ssum(t["rows"][0]["cells"][c].value for c in t["cols"])
                CHK.eq(o, f"{where(s)} plants: livraisons vs sum of seasons", tot, liv["plants"].value)
            else:
                trow = [r for r in t["rows"] if is_tot(r["label"])][0]["cells"]
                for c, suf in (("plants", "p"), ("grafts", "g")):
                    if c in s["cols"]:
                        tot = ssum(trow[x].value for x in t["cols"] if x.endswith(suf))
                        CHK.eq(o, f"{where(s)} {c}: livraisons vs sum of season totals", tot, liv[c].value)
        info.append(f"{s['ed']} {s['group']}: " + "; ".join(
            f"{r['label']} " + "/".join(str(r['cells'][c].value) for c in s["cols"]) for r in rows))
    return info


def build(write=True):
    secs = []
    for ed in ORDER:
        p = TR / f"{PREFIX}_{ed}.txt"
        if p.exists():
            secs += parse(p, ed)
    res = {}
    cum_info = chk_cum(secs)
    for out, spec in TABLES.items():
        ss = [s for s in secs if s["table"] in spec["secs"]]
        if not ss:
            continue
        for s in ss:
            spec["check"](s)
        spec["_eds"] = [e for e in ORDER if any(s["ed"] == e for s in ss)]
        recs = []
        for s in ss:
            recs += spec["cells"](s)
        kept, n, diffs = select(recs, spec["key"])
        order = {id(r): i for i, r in enumerate(recs)}
        kept.sort(key=lambda r: (r["year"] if r["year"] is not None else 0, ORDER.index(r["census"]),
                                 order.get(id(r), 0)))
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
            res, _chapter_views=CHAPTER_VIEWS, _cumulative_deliveries=cum_info, _survey=SURVEY,
            _not_transcribed=NOT_DONE))
        write_survey()
    return res


def write_survey():
    L = ["# Teaching and research institutions: survey of every edition", "",
         "Survey of the *Institutions d'enseignement et de recherches* pages, view by view: the separate chapter "
         "of sgt1935, sgt1936 and sgt1939, and the same institutions and the meteorology printed at the end of the "
         "Agriculture chapter in sgt1922-sgt1930. First and last views confirmed on the page images. Extraction: "
         "`extract_research.py`.", "",
         "| edition | ark | views |", "|---|---|---|"]
    L += [f"| {e} | `{EDITIONS[e]}` | {v} |" for e, v in CHAPTER_VIEWS.items()]
    L += ["", "## Views per edition", ""] + [f"- **{e}**: {t}" for e, t in SURVEY.items()]
    L += ["", "## Tables (CSV)", "", "| CSV | sections | editions | read on the image |", "|---|---|---|---|"]
    L += [f"| `{o}` | {', '.join(sp['secs'])} | {', '.join(sp.get('_eds', []))} | every printing, cell by cell |"
          for o, sp in TABLES.items() if sp.get("_eds")]
    L += ["", "## Coverage", "", NOT_DONE, ""]
    (OUT / f"{PREFIX}_survey.md").write_text("\n".join(L) + "\n")


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
