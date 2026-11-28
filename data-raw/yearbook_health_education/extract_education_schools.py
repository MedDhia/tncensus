#!/usr/bin/env python3
"""School-by-school lists of the public-instruction chapter ("Instruction publique et beaux-arts") of the
Statistique générale de la Tunisie: a) public primary schools and b) private schools, editions sgt1922 and
sgt1930. sgt1939 prints no school-by-school primary list (see the notes); its only per-establishment tables
(secondary / higher-primary / technical establishments, vocational schools) are already extracted in
education_secondary_establishments_sgt1939.csv and education_vocational.csv, as are the 1922/1930 lists of
establishments with civil personality (education_civil_personality_establishments.csv) and of vocational
schools (education_vocational.csv), so they are not repeated here.

  python3 extract_education_schools.py check   parse the transcriptions, run every check, print the failures
  python3 extract_education_schools.py build   ... and write csv/education_schools.csv, its notes
                                               csv/education_schools.md and csv/education_schools_validation.json

Source of truth: transcribed/education_schools_<edition>.txt, typed from the page images (native-resolution
crops from data-raw/yearbook_demography/hires.py; Gallica OCR only as a draft). Format:

  @ <block> sector=<public|private> table=<French title, _ for spaces>   starts a table
  ## views <left> <right> pages <left> <right>                           starts a two-page spread
  % <label>                                                              a printed group heading inside a table
  locality | school | classes fr ar div TOT | boys fr mus isr ita mal div TOT | girls (same) | TOTAL prev
  REPORT | Report | ...  /  AREPORTER | A reporter | ...  /  TOTAL | <label> | ...   printed carry-overs/totals

Tokens: integer; "»" (printed dash) = 0; "?" = cell hidden in the binding, solved from the row total
(flag derived_from_totals); "na" = a word printed instead of a number ("Création", "Réouverture", or a
previous-year total bracketed with the line above; value NA, flag not_applicable); "a+b" = one cell printed as
two numbers (stored as their sum, flag derived_from_totals); "v#w" = printed value v kept (flag total_mismatch)
while the row and column totals imply w, which the checks use; "v#" on a printed total = misprinted total, kept
and reported. Text after "  #" is a comment (the evidence for every flag).
"""
import csv
import json
import re
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
TR = HERE / "transcribed"
OUT = HERE / "csv"
NAME = "education_schools"

EDITIONS = OrderedDict([
    ("sgt1922", dict(ark="bpt6k9105649x", year=1922, chapter=(113, 152), lists=True)),
    ("sgt1930", dict(ark="bpt6k9105652d", year=1930, chapter=(671, 710), lists=True)),
    ("sgt1939", dict(ark="bpt6k9105739w", year=1939, chapter=(65, 76), lists=False)),
])

NATS = [("french", "Français", "Françaises"), ("muslim", "Musulmans", "Musulmanes"),
        ("jewish", "Israélites", "Israélites"), ("italian", "Italiens", "Italiennes"),
        ("maltese", "Maltais", "Maltaises"), ("other", "Divers", "Diverses")]
STAFF = [("staff_french_diploma", "Maîtres pourvus de diplômes français"), ("staff_arabic", "Maîtres arabes"),
         ("staff_other", "Maîtres divers")]
TABLE_ID = {"primary_public": "public_schools", "primary_private": "private_schools"}
SPECIAL = {"REPORT", "AREPORTER", "TOTAL"}
# printed group lengths: cstaff = classes + 3 staff + staff TOTAUX; boys/girls = 6 nationalities + TOTAUX;
# genprev = TOTAUX généraux + Totaux généraux de l'année précédente
GLEN = {"cstaff": 5, "boys": 7, "girls": 7, "genprev": 2}
COLS = ["census", "table_id", "gallica_ark", "source_page", "gallica_view", "year", "school_sector",
        "inspection_district", "locality", "school", "school_group_fr", "row_order", "measure", "measure_fr",
        "sex", "sex_fr", "nationality", "nationality_fr", "value", "flag"]


# ---------------------------------------------------------------- parsing

class Cell:
    def __init__(self, tok):
        self.raw, self.flag, self.alt, self.misprint = tok, "", None, False
        t = tok
        m = re.fullmatch(r"(\d+)\+(\d+)", t)
        if m:
            self.v, self.flag = int(m.group(1)) + int(m.group(2)), "derived_from_totals"
            return
        m = re.fullmatch(r"(\d+|»)#(\d+)", t)
        if m:
            self.alt, t = int(m.group(2)), m.group(1)
            self.flag = "total_mismatch"
        elif t.endswith("#"):
            self.misprint, t = True, t[:-1]
            self.flag = "total_mismatch"
        if t == "»":
            self.v = 0
        elif t == "?":
            self.v = None
        elif t == "na":
            self.v, self.flag = None, "not_applicable"
        elif re.fullmatch(r"\d+", t):
            self.v = int(t)
        else:
            raise ValueError(f"bad token {tok!r}")

    @property
    def c(self):
        """value used by the checks"""
        return self.alt if self.alt is not None else self.v


def parse(ed):
    path = TR / f"education_schools_{ed}.txt"
    blocks, blk, spread, group = [], None, None, ""
    for ln, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        s = raw.split("  #")[0].rstrip()
        comment = raw.split("  #", 1)[1].strip() if "  #" in raw else ""
        if not s.strip() or s.startswith("# ") or s == "#":
            continue
        if s.startswith("@ "):
            parts = s[2:].split()
            kw = dict(p.split("=", 1) for p in parts[1:])
            blk = dict(name=parts[0], sector=kw["sector"], table_fr=kw["table"].replace("_", " "),
                       cols=kw["cols"].split(","), rows=[], spreads=[])
            blocks.append(blk)
            group = ""
            continue
        if s.startswith("## "):
            m = re.fullmatch(r"## views (\d+) (\d+) pages (\d+) (\d+)", s)
            spread = dict(L=(int(m.group(1)), int(m.group(3))), R=(int(m.group(2)), int(m.group(4))))
            blk["spreads"].append(spread)
            continue
        if s.startswith("% "):
            group = s[2:].strip()
            continue
        f = [x.strip() for x in s.split("|")]
        loc, school, grp = f[0], f[1], f[2:]
        if len(grp) != len(blk["cols"]):
            raise ValueError(f"{path.name}:{ln}: {len(grp)} groups")
        cells = {}
        for g, txt in zip(blk["cols"], grp):
            toks = txt.split()
            if len(toks) != GLEN[g]:
                raise ValueError(f"{path.name}:{ln}: group {g} has {len(toks)} cells")
            cells[g] = [Cell(t) for t in toks]
        blk["rows"].append(dict(kind=loc if loc in SPECIAL else "SCHOOL", loc=loc, school=school, group=group,
                                cells=cells, spread=spread, ln=ln, comment=comment))
    return blocks


# ---------------------------------------------------------------- checks

class Checks:
    def __init__(self):
        self.n = 0
        self.by_kind = defaultdict(int)
        self.items = []        # failed checks

    def eq(self, kind, what, got, printed, expl=""):
        self.n += 1
        self.by_kind[kind] += 1
        ok = got == printed
        if not ok:
            self.items.append(dict(kind=kind, check=what, cells=got, printed=printed, explanation=expl))
        return ok


def parts_total(cs):
    return cs[:-1], cs[-1]


def derive_and_check_rows(ed, blk, chk):
    """Row checks (staff, boys, girls, boys+girls); '?' cells solved from the row total."""
    derived = 0
    for r in blk["rows"]:
        c = r["cells"]
        tag = f"{ed} {blk['name']} l{r['ln']} {r['loc']} / {r['school']}"
        for g in ("cstaff", "boys", "girls"):
            cs = c[g][1:] if g == "cstaff" else c[g]
            parts, tot = parts_total(cs)
            unk = [x for x in parts if x.v is None and x.flag != "not_applicable"]
            if unk:
                if len(unk) > 1 or tot.c is None:
                    raise ValueError(f"{tag}: cannot solve {g}")
                unk[0].v = tot.c - sum(x.c for x in parts if x is not unk[0])
                unk[0].flag = "derived_from_totals"
                derived += r["kind"] == "SCHOOL"
                if unk[0].v < 0:
                    raise ValueError(f"{tag}: negative derived value")
                continue           # the total was used up: no independent check of this group
            if tot.c is None:
                continue
            expl = r["comment"] if (any(x.alt is not None or x.misprint for x in cs)) else ""
            label = {"cstaff": "staff", "boys": "boys", "girls": "girls"}[g]
            chk.eq("row", f"{tag}: {label} by column vs printed TOTAUX", sum(x.c for x in parts), tot.v, expl)
        b, gi, gp = c["boys"][-1], c["girls"][-1], c["genprev"][0]
        if None not in (b.c, gi.c, gp.c):
            chk.eq("row", f"{tag}: boys TOTAUX + girls TOTAUX vs printed TOTAUX généraux", b.c + gi.c, gp.v,
                   r["comment"] if (gp.misprint or gp.alt is not None) else "")
    return derived


def column_checks(ed, blk, chk, printed_totals):
    """Each spread: printed Report + its rows = printed A reporter / TOTAL; each Report = previous A reporter;
    the final TOTAL also against the sum of all school rows."""
    cols = blk["cols"]
    keys = [(g, i) for g in cols for i in range(GLEN[g])]
    labels = {("cstaff", 0): "classes", ("cstaff", 1): "staff fr", ("cstaff", 2): "staff arabic",
              ("cstaff", 3): "staff other", ("cstaff", 4): "staff TOTAUX", ("genprev", 0): "TOTAUX généraux",
              ("genprev", 1): "previous-year total"}
    for sx in ("boys", "girls"):
        for i, (n, *_r) in enumerate(NATS):
            labels[(sx, i)] = f"{sx} {n}"
        labels[(sx, 6)] = f"{sx} TOTAUX"
    page = {k: 0 for k in keys}
    allrows = {k: 0 for k in keys}
    last_carry = None
    for r in blk["rows"]:
        c = r["cells"]
        val = {(g, i): c[g][i] for g, i in keys}
        tag = f"{ed} {blk['name']} l{r['ln']} {r['school']}"
        if r["kind"] == "SCHOOL":
            for k in keys:
                if val[k].c is not None:
                    page[k] += val[k].c
                    allrows[k] += val[k].c
            continue
        if r["kind"] == "REPORT":
            for k in keys:
                if last_carry is not None and val[k].c is not None:
                    chk.eq("carry", f"{tag}: Report {labels[k]} vs previous page's A reporter",
                           val[k].c, last_carry[k], r["comment"])
                page[k] = val[k].c or 0
            continue
        # AREPORTER or TOTAL: compare
        for k in keys:
            if val[k].c is None:
                continue
            expl = r["comment"] if val[k].misprint else ""
            chk.eq("column", f"{tag}: {labels[k]}, printed Report + rows of the page vs printed", page[k],
                   val[k].c, expl)
        if r["kind"] == "AREPORTER":
            last_carry = {k: val[k].c for k in keys}
        else:
            for k in keys:
                if val[k].c is not None:
                    chk.eq("grand", f"{tag}: {labels[k]}, sum of all school rows of the table vs printed total",
                           allrows[k], val[k].c, r["comment"])
            printed_totals[(ed, blk["name"])] = {labels[k]: val[k].c for k in keys}
            printed_totals[(ed, blk["name"], "sum")] = {labels[k]: allrows[k] for k in keys}


# ---------------------------------------------------------------- output rows

def out_rows(ed, blk):
    e = EDITIONS[ed]
    rows, order = [], 0
    for r in blk["rows"]:
        store_total = r["kind"] == "TOTAL" and blk["sector"] == "private" and ed == "sgt1922"
        if r["kind"] != "SCHOOL" and not store_total:
            continue
        order += 1
        c = r["cells"]

        def add(side, measure, measure_fr, sex, sex_fr, nat, nat_fr, cell):
            view, page = r["spread"][side]
            flag = cell.flag
            if cell.v is None and not flag:
                flag = "illegible"
            rows.append(dict(census=ed, table_id=TABLE_ID[blk["name"]], gallica_ark=e["ark"], source_page=page,
                             gallica_view=view, year=e["year"], school_sector=blk["sector"],
                             inspection_district="",
                             locality="TOTAL (printed)" if store_total else r["loc"],
                             school=r["school"], school_group_fr=r["group"], row_order=order, measure=measure,
                             measure_fr=measure_fr, sex=sex, sex_fr=sex_fr, nationality=nat,
                             nationality_fr=nat_fr, value="" if cell.v is None else cell.v, flag=flag,
                             _c=cell.c))
        add("L", "classes", "Nombre de classes", "total", "", "total", "", c["cstaff"][0])
        for (m, mfr), cell in zip(STAFF, c["cstaff"][1:4]):
            add("L", m, mfr, "total", "", "total", "", cell)
        for sx, sxfr, g, gi in (("male", "Garçons", "boys", 1), ("female", "Filles", "girls", 2)):
            for i, nat in enumerate(NATS):
                side = "L" if (g == "boys" and i < 2) else "R"
                add(side, "pupils", "Élèves", sx, sxfr, nat[0], nat[gi], c[g][i])
        add("R", "pupils_total_previous_year", "Totaux généraux de l'année précédente", "total", "", "total", "",
            c["genprev"][1])
    return rows


# ---------------------------------------------------------------- cross-checks

def load(name):
    with open(OUT / f"{name}.csv", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def cross_checks(allrows, printed_totals):
    """Summed schools (and the lists' printed totals) vs the edition's 'Total général de l'enseignement
    primaire' (education_primary_totals.csv) and comparative population table (education_school_population.csv),
    cell by cell: 12 sex x nationality cells and the previous-year total, per sector."""
    out = []
    code = {"public": "public_primary", "private": "private"}
    printed, implied = defaultdict(int), defaultdict(int)
    for r in allrows:
        if r["measure"] in ("pupils", "pupils_total_previous_year") and r["locality"] != "TOTAL (printed)":
            k = (r["census"], r["school_sector"], r["measure"], r["sex"], r["nationality"])
            printed[k] += r["value"] or 0
            implied[k] += r["_c"] or 0
    ref = {}
    for fname in ("education_primary_totals", "education_school_population"):
        for r in load(fname):
            if r["school_type"] in ("public_primary", "private") and r["value"] != "":
                ref[(fname, r["census"], r["school_type"], r["measure"], r["sex"], r["nationality"])] = int(r["value"])
    cells = [("pupils", sx, n, f"{lab} {n}") for sx, lab in (("male", "boys"), ("female", "girls"))
             for n, *_r in NATS] + [("pupils_total_previous_year", "total", "total", "previous-year total")]
    for ed, e in EDITIONS.items():
        if not e["lists"]:
            continue
        for sector, blk in (("public", "primary_public"), ("private", "primary_private")):
            pt = printed_totals.get((ed, blk), {})
            for measure, sx, nat, plabel in cells:
                k = (ed, sector, measure, sx, nat)
                for fname in ("education_primary_totals", "education_school_population"):
                    rv = ref.get((fname, ed, code[sector], measure, sx, nat))
                    if rv is None:
                        continue
                    out.append(dict(edition=ed, sector=sector, cell=plabel, other_table=fname,
                                    schools_summed=printed[k], schools_summed_as_implied_by_totals=implied[k],
                                    list_printed_total=pt.get(plabel), other_table_value=rv,
                                    equal=printed[k] == rv, equal_implied=implied[k] == rv,
                                    list_total_equal=pt.get(plabel) == rv))
    return out


# ---------------------------------------------------------------- name comparison

def norm(s):
    s = s.lower().replace("’", "'")
    s = re.sub(r"\((el|la|le|l')\)", "", s)
    s = re.sub(r"[^a-zàâçéèêëîïôûüœ0-9]+", " ", s)
    return " ".join(s.split())


def name_changes(allrows):
    sch = defaultdict(OrderedDict)
    for r in allrows:
        if r["locality"] != "TOTAL (printed)":
            sch[(r["census"], r["school_sector"])][(r["locality"], r["school"])] = 1
    res = {}
    for sector in ("public", "private"):
        a = sch[("sgt1922", sector)]
        b = sch[("sgt1930", sector)]
        la = OrderedDict((norm(l), l) for l, _s in a)
        lb = OrderedDict((norm(l), l) for l, _s in b)
        res[sector] = dict(
            schools_1922=len(a), schools_1930=len(b),
            localities_1922=len(la), localities_1930=len(lb),
            localities_only_1922=[la[k] for k in la if k not in lb],
            localities_only_1930=[lb[k] for k in lb if k not in la],
            schools_by_locality={},
        )
        for k in la:
            if k in lb:
                sa = [s for l, s in a if norm(l) == k]
                sb = [s for l, s in b if norm(l) == k]
                na, nb = [norm(x) for x in sa], [norm(x) for x in sb]
                if na != nb:
                    res[sector]["schools_by_locality"][lb[k] if la[k] == lb[k] else f"{la[k]} / {lb[k]}"] = \
                        dict(only_sgt1922=[x for x in sa if norm(x) not in nb],
                             only_sgt1930=[x for x in sb if norm(x) not in na])
    return res


# ---------------------------------------------------------------- notes

COLDOC = OrderedDict([
    ("census", "edition (`sgt1922`, `sgt1930`)"),
    ("table_id", "`public_schools` (a) Écoles primaires publiques) or `private_schools` (b) Écoles privées)"),
    ("gallica_ark", "Gallica volume ark (views are numbered within a volume)"),
    ("source_page", "printed page number. Each list is printed across two-page spreads: classes, staff and the "
                    "boys' Français and Musulmans columns are given the left-hand page, the other pupil columns "
                    "and the previous-year total the right-hand page"),
    ("gallica_view", "Gallica view (fNNNN) of that page"),
    ("year", "year of the edition; pupils and staff at 31 December of that year"),
    ("school_sector", "`public` or `private`"),
    ("inspection_district", "always empty: in sgt1922 and sgt1930 the public list is printed in one alphabetical "
                            "sequence of localities (Tunis first) under a heading naming the inspection districts "
                            "collectively, with no district per school or district subtotal (see below)"),
    ("locality", "locality as printed (period spelling; the article in brackets as printed, e.g. `Ariana (L')`); "
                 "`TOTAL (printed)` for the one stored total row (see below)"),
    ("school", "designation as printed; a group word printed once for several lines (e.g. `Garçons :` followed by "
               "ditto dashes in Tunis) is repeated on every line it covers"),
    ("school_group_fr", "printed group heading inside a table: `Ecoles de l'Alliance Israélite (subventionnées)` "
                        "for the last private schools; empty otherwise"),
    ("row_order", "order of the school within its table and edition (1, 2, …); identifies a school together "
                  "with `census` and `table_id`"),
    ("measure", "`classes` (Nombre de classes), `staff_french_diploma` (Maîtres pourvus de diplômes français), "
                "`staff_arabic` (Maîtres arabes), `staff_other` (Maîtres divers), `pupils` (Élèves), "
                "`pupils_total_previous_year` (Totaux généraux de l'année précédente: the school's total pupils "
                "a year earlier, printed only as a total)"),
    ("measure_fr", "column heading as printed"),
    ("sex", "`male` (Garçons), `female` (Filles) for pupils; `total` otherwise"),
    ("sex_fr", "as printed"),
    ("nationality", "`french`, `muslim`, `jewish`, `italian`, `maltese`, `other` (Divers) for pupils; `total` "
                    "otherwise"),
    ("nationality_fr", "column heading as printed (masculine for boys, feminine for girls)"),
    ("value", "count (integer); printed » = 0; empty where a word is printed instead of a number "
              "(`not_applicable`)"),
    ("flag", "empty, or `derived_from_totals`, `total_mismatch`, `not_applicable` (see below)"),
])


def write_notes(res):
    s, rows, chk, x, names, derived = (res[k] for k in ("summary", "rows", "checks", "cross", "names", "derived"))
    views = defaultdict(set)
    for r in rows:
        views[(r["census"], r["table_id"])].add((r["source_page"], r["gallica_view"]))

    def vr(ed, t):
        v = sorted(views[(ed, t)])
        return f"pp. {v[0][0]}–{v[-1][0]}, f{v[0][1]}–f{v[-1][1]}"

    fl = defaultdict(int)
    for r in rows:
        if r["flag"]:
            fl[r["flag"]] += 1
    L = ["# Écoles primaires publiques et écoles privées, école par école",
         "",
         "*Public primary schools and private schools, school by school: classes, staff and pupils by sex and "
         "nationality (sgt1922, sgt1930).*",
         "",
         "Source: *Statistique générale de la Tunisie*, chapter VII \"Instruction publique et beaux-arts\", "
         "\"Enseignement primaire\", a) Écoles primaires publiques, b) Écoles privées; editions sgt1922 "
         "(`bpt6k9105649x`, situation at 31 December 1922) and sgt1930 (`bpt6k9105652d`, 31 December 1930). "
         "Source gallica.bnf.fr / Ministère des Affaires étrangères.",
         "",
         "Pages and views: sgt1922 public " + vr("sgt1922", "public_schools") + ", private " +
         vr("sgt1922", "private_schools") + "; sgt1930 public " + vr("sgt1930", "public_schools") +
         ", private " + vr("sgt1930", "private_schools") + ".",
         "",
         "Transcriptions: `../transcribed/education_schools_<edition>.txt`; rebuild with "
         "`python3 data-raw/yearbook_health_education/extract_education_schools.py build`. Every check is listed "
         "in `education_schools_validation.json`.",
         "",
         f"Rows: {len(rows)} (one per printed cell). Schools: " + "; ".join(
             f"{k} {v['schools']}" for k, v in s.items()) + ".",
         "",
         "## Coverage",
         "",
         "- **sgt1922, sgt1930**: the public primary schools (a) and the private schools (b) are printed school by "
         "school and are stored here. The other per-establishment lists of the chapter are already extracted "
         "elsewhere and are not repeated: the establishments with civil personality "
         "(`education_civil_personality_establishments.csv`) and the vocational schools "
         "(c) Enseignement professionnel des indigènes; `education_vocational.csv`). The \"Total général de "
         "l'enseignement primaire\" that follows the lists is `education_primary_totals.csv`.",
         "- **sgt1939** (`bpt6k9105739w`, chapter VI, views 65–76) prints **no** school-by-school list of primary "
         "or private schools. Its chapter has: total pupils (f66), examinations (f67–68), libraries, Arabic "
         "courses, commerce and music schools (f69), the secondary / higher-primary / technical establishments "
         "one by one (f70–71, in `education_secondary_establishments_sgt1939.csv`), the first-degree total "
         "(\"Établissements d'enseignement du premier degré\", one line, f72–73, in "
         "`education_first_degree_sgt1939.csv`), vocational schools (f72, in `education_vocational.csv`), "
         "canteens (f73), the comparative population table (f74–75) and the quinquennial series (f76). No rows "
         "for sgt1939 are therefore stored here.",
         "",
         "## Layout",
         "",
         "Both editions print the same table: Localités | Désignation des établissements scolaires | Nombre de "
         "classes | Personnel (Maîtres pourvus de diplômes français, Maîtres arabes, Maîtres divers, Totaux) | "
         "Garçons (Français, Musulmans, Israélites, Italiens, Maltais, Divers, Totaux) | Filles (same, feminine) | "
         "Totaux généraux | Totaux généraux de l'année précédente, over two-page spreads with \"A reporter\" and "
         "\"Report\" lines, ending with \"Totaux des écoles primaires publiques\" / \"Totaux des écoles privées\". "
         "The public list carries the heading \"(Circonscriptions d'inspection primaire : Bizerte, Sfax, Sousse, "
         "Tunis-Nord, Tunis-Est, Tunis-Ouest)\" in sgt1922 and \"(… : Bizerte, Le Kef, Sfax, Sousse, Tunis-Nord, "
         "Tunis-Est, Tunis-Ouest)\" in sgt1930, but the schools are not grouped by district: Tunis comes first, "
         "then all other localities in one alphabetical sequence, with no district subtotals. No district can be "
         "read from the table, so `inspection_district` is empty (assigning districts would need an outside "
         "source). The private list is alphabetical by locality, Tunis first, with the subsidised Alliance "
         "Israélite schools last under their own heading. Printed totals (staff Totaux, pupils' Totaux, Totaux "
         "généraux, A reporter, Report, final totals) are not stored; they were used for the checks.",
         "",
         "## Cell conventions and flags",
         "",
         f"- `derived_from_totals` ({fl['derived_from_totals']} cells): the boys' Musulmans column is printed in "
         "the binding on most spreads (sgt1922 throughout; sgt1930 views 676–695 and the private list, partly; "
         "only the last digits or nothing are visible). Each such cell is solved as the boys' Totaux minus the "
         "other five nationalities. On the spreads where the column is legible (sgt1930 views 696–701, and some "
         "private rows) it was read and checked. One sgt1922 cell (Ghardimaou, previous-year total) is printed "
         "as two numbers, 81 for boys and 38 for girls, and stored as 119 with this flag. Derived cells were "
         "compared with the visible digit fragments where spot-checked, and their page sums agree with the "
         "printed Musulmans carry-overs where those are legible (sgt1930).",
         f"- `total_mismatch` ({fl['total_mismatch']} cells): a printed school cell that does not agree with its "
         "row total and its column total; the printed value is stored and the value the totals imply is used for "
         "the checks. Each was re-read on a native-resolution crop. They are listed below.",
         f"- `not_applicable` ({fl['not_applicable']} cells): previous-year column printed \"Création\" (new school) "
         "or \"Réouverture\" (reopened), or left blank because a single previous-year total is printed in a "
         "bracket for two lines; in that case the bracketed figure is stored on the first line and covers both "
         "(sgt1922: Oued-Ellil Garçons + Filles = 58, Saïda Garçons + Filles = 101).",
         "- Schools printed with » in every column are stored with 0 (sgt1922: Azib (El), Mixte (fermée); "
         "the La Manouba private secondary school for girls opened on 1 March 1923; the Bizerte Ecole Umberto "
         "Ier, see below).",
         "- sgt1922 private schools: the printed \"A reporter\" of the first private spread exceeds its itemised "
         "rows by 7 classes, 8 Maîtres divers, 170 Italian boys and 108 Italian girls (278 pupils), and the final "
         "\"Totaux des écoles privées\" and the primary-education total count them; the only school with no "
         "figures is the Bizerte Ecole Umberto Ier (printed » throughout, 288 pupils the previous year), so the "
         "figures are apparently that school's, left out of its line. Because the printed total carries "
         "information not recoverable from the rows, the private total row of sgt1922 **is stored**, with "
         "`locality = \"TOTAL (printed)\"` and `school = \"Totaux des écoles privées\"` (SPEC rule): do not add "
         "it to the school rows.",
         "",
         "## Columns",
         ""]
    L += [f"- `{c}`: {COLDOC[c]}" for c in COLS]
    L += ["", "## Validation", "",
          f"- Checks against printed totals: {chk['n']}; passed: {chk['n'] - len(chk['failed'])}; failed: "
          f"{len(chk['failed'])}. Kinds: row checks (staff, boys, girls, boys + girls = Totaux généraux) "
          f"{chk['by_kind']['row']}; page column checks (printed Report + the page's rows = printed A reporter or "
          f"final total, every column) {chk['by_kind']['column']}; carry-over checks (each Report = the previous "
          f"page's A reporter) {chk['by_kind']['carry']}; grand-total checks (all school rows of a table = its "
          f"printed final total, every column) {chk['by_kind']['grand']}.",
          f"- Cells solved from row totals: {derived} (their groups have no independent row check).",
          "",
          "Failed checks. Every cell involved was re-read on a native-resolution crop (and against the Gallica "
          "OCR); the printed figures are kept:", ""]
    for f_ in chk["failed"]:
        L.append(f"  - {f_['check']}: cells give {f_['cells']}, printed {f_['printed']}"
                 + (f". {f_['explanation']}" if f_["explanation"] else ""))
    flagged = [r for r in rows if r["flag"] == "total_mismatch"]
    L += ["", "Cells flagged `total_mismatch`:", ""]
    for r in flagged:
        L.append(f"  - {r['census']} {r['table_id']} {r['locality']} / {r['school']}: {r['measure']} {r['sex']} "
                 f"{r['nationality']} printed {r['value']}")
    L += ["", "## Cross-check with the summary tables", "",
          "The school rows of each list were summed by sex and nationality and compared, cell by cell, with the "
          "same edition's \"Total général de l'enseignement primaire\" (`education_primary_totals.csv`, rows "
          "`public_primary`, `private`) and comparative school-population table "
          "(`education_school_population.csv`, same rows). The list's own printed final total is compared too.",
          ""]
    neq = [c for c in x if not c["equal"]]
    neq2 = [c for c in x if not c["equal_implied"]]
    L += [f"- {len(x)} comparisons (2 editions x 2 sectors x 13 cells: 12 sex x nationality cells and the "
          f"previous-year total, against each of the 2 tables). Summed printed school cells equal to the other "
          f"table: {len(x) - len(neq)}; different: {len(neq)}. Summed with the values the totals imply for the "
          f"`total_mismatch` cells: equal {len(x) - len(neq2)}, different {len(neq2)}. The list's own printed "
          f"final total equals the other table in {sum(c['list_total_equal'] for c in x)} of {len(x)}.", "",
          "Differences (schools summed as printed / as implied by the totals / the list's printed total / the "
          "other table):", ""]
    for c in neq:
        L.append(f"  - {c['edition']} {c['sector']} {c['cell']} vs `{c['other_table']}`: {c['schools_summed']} / "
                 f"{c['schools_summed_as_implied_by_totals']} / {c['list_printed_total']} / {c['other_table_value']}")
    L += ["", "Explanation: (i) the `total_mismatch` school cells are stored as printed, so the printed sums differ "
          "from the totals by exactly those misprints (they agree once the implied values are used); (ii) sgt1922 "
          "private: the 278 pupils (170 Italian boys, 108 Italian girls) counted in the printed totals but not "
          "itemised (see above); (iii) previous-year totals: the printed carry-overs are misprinted (sgt1922 "
          "public −6; sgt1930 public +23 and +86, private +27), the summary tables copy the lists' printed final "
          "totals; (iv) sgt1930 public boys' Français: lists and population table 6.676, the primary-education "
          "total prints 6.667 (a misprint already flagged in `education_primary_totals.csv`). No other difference: "
          "every other sex x nationality cell of the summed schools agrees with both summary tables.", ""]
    L += ["## Schools that changed between 1922 and 1930", "",
          "Compared by locality (normalised spelling) and designation; no linking is attempted. sgt1939 prints no "
          "list. Numbers of schools: " + "; ".join(
              f"{k}: {v['schools_1922']} (1922) → {v['schools_1930']} (1930), localities {v['localities_1922']} → "
              f"{v['localities_1930']}" for k, v in names.items()) + "."]
    for sector, v in names.items():
        L += ["", f"**{sector}**: localities only in 1922: " + (", ".join(v["localities_only_1922"]) or "none")
              + ". Only in 1930: " + (", ".join(v["localities_only_1930"]) or "none") + "."]
        if v["schools_by_locality"]:
            L += ["", f"Localities in both editions whose {sector} schools changed (designations printed only in "
                  "1922 → only in 1930; designations printed identically in both are not repeated):", ""]
            for loc, d in v["schools_by_locality"].items():
                L.append(f"- {loc}: {'; '.join(d['only_sgt1922']) or '(none)'} → "
                         f"{'; '.join(d['only_sgt1930']) or '(none)'}")
    L += ["", "Obvious correspondences (spelling or split of a locality, not linked in the data): Ben-Arous → "
          "Ben-Arous (Fochville); Deggache (El-Oudiane) → Deggache; Fedjet Khemaken → Fedjet-Khemakhem; Hamaïm → "
          "Hammaïm; Kanguet-el-Hadjaj → Khanguet-el-Hadjaj; Ksar-el-Ahmar → Ksar-Lahmar; Maareth → Mareth; "
          "Sahaline → Saheline; Zeramdine → Zéramdine; Sers → Sers-gare and Sers-village; Rebiba → Rebiba, gare "
          "and Rebiba, mine; Hamma (El) → Hamma (El) de Gabès (and a new Hamma (El) du Djerid); private: "
          "Seillonville → Sillonville, Bizerte Ecole de Mme Médeville → Médevielle. Kef-Chambi (1922, printed "
          "\"Mixte (fermé)\" with no pupils) is not printed in 1930. Many 1922 \"Mixte\" schools appear in 1930 as "
          "separate Garçons and Filles schools, and many Garçons schools are relabelled \"(franco-arabe)\". Every "
          "spelling is as printed in its edition."]
    (OUT / f"{NAME}.md").write_text("\n".join(L) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- build

def build(write):
    chk = Checks()
    rows, summary, printed_totals, derived = [], OrderedDict(), {}, 0
    for ed, e in EDITIONS.items():
        p = TR / f"education_schools_{ed}.txt"
        if not e["lists"]:
            if p.exists():
                raise ValueError(f"{ed} prints no school lists; unexpected {p.name}")
            continue
        for blk in parse(ed):
            n0 = chk.n
            derived += derive_and_check_rows(ed, blk, chk)
            column_checks(ed, blk, chk, printed_totals)
            br = out_rows(ed, blk)
            rows += br
            summary[f"{ed}/{TABLE_ID[blk['name']]}"] = dict(
                schools=sum(1 for r in blk["rows"] if r["kind"] == "SCHOOL"), cells=len(br), checks=chk.n - n0)
    cross = cross_checks(rows, printed_totals)
    names = name_changes(rows)
    res = dict(summary=summary, rows=rows, cross=cross, names=names, derived=derived,
               checks=dict(n=chk.n, failed=chk.items, by_kind=dict(chk.by_kind)))
    return res, chk


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd not in ("check", "build"):
        print(__doc__)
        sys.exit(1)
    res, chk = build(cmd == "build")
    kinds = chk.by_kind
    for k, v in res["summary"].items():
        print(k, v)
    fl = defaultdict(int)
    for r in res["rows"]:
        fl[r["flag"]] += 1
    print(f"{len(res['rows'])} rows; checks {chk.n}, failed {len(chk.items)}; by kind {dict(kinds)}; "
          f"flags {dict(fl)}")
    for f_ in chk.items:
        print("  FAIL", f_["check"], "cells", f_["cells"], "printed", f_["printed"], "|", f_["explanation"][:90])
    neq = [c for c in res["cross"] if not c["equal"]]
    print(f"cross-checks {len(res['cross'])}, different {len(neq)}")
    for c in neq:
        print("  XCHK", c)
    if cmd == "build":
        OUT.mkdir(exist_ok=True)
        with (OUT / f"{NAME}.csv").open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=COLS, lineterminator="\n", extrasaction="ignore")
            w.writeheader()
            w.writerows(res["rows"])
        write_notes(res)
        val = dict(summary=res["summary"], rows=len(res["rows"]), checks=chk.n, checks_by_kind=dict(kinds),
                   failed=chk.items, cells_derived_from_row_totals=res["derived"], flags=dict(fl),
                   cross_checks=res["cross"], name_changes=res["names"],
                   chapters={e: list(v["chapter"]) for e, v in EDITIONS.items()},
                   sgt1939="no school-by-school primary or private list printed (chapter VI, views 65-76)")
        (OUT / f"{NAME}_validation.json").write_text(json.dumps(val, ensure_ascii=False, indent=1) + "\n",
                                                     encoding="utf-8")


if __name__ == "__main__":
    main()
