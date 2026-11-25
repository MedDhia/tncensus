#!/usr/bin/env python3
"""Summary tables of the public-instruction chapter ("Instruction publique et
beaux-arts", chapter VII, chapter VI in sgt1936 and sgt1939) of the 12 editions
of the Statistique générale de la Tunisie, 1922-1939 (see CHAPTERS.md).

  python3 extract_education_summary.py check   parse transcriptions, run every check, print failures
  python3 extract_education_summary.py build   ... and write csv/education_*.csv, their .md notes
                                               and csv/education_summary_validation.json

Source of truth: transcribed/education_sum_<edition>.txt, typed from the page
images (data-raw/bnf_gallica/pages/, with native-resolution crops from
data-raw/yearbook_demography/hires.py for every table of sgt1928-sgt1939 and for
every doubtful cell). Gallica OCR (data-raw/colonial_census/ocr.py) was only a
draft for sgt1922-sgt1927.

Transcription format: sections "[name key=value ...]" (view(s)=, page(s)=);
data lines "field | field | numbers"; numeric blocks are space-separated
integers; "." = cell not printed; a printed "»" is typed 0. "note:" lines hold
footnotes, "years:" the years of a two-year window, "flag: k1;k2;... = flag"
the flag of one cell, "#" comments (the evidence for every flag and every
failed check is given there).

Year-windowed tables follow SPEC_ADDENDUM rule 4 (all cells of a year from the
latest edition printing it; every other printing compared; REPRINT below for
documented exceptions); tables printed once per edition follow rule 5. Printed
totals are used for checks only. Not covered: the school-by-school lists of
public primary and private schools (transcribed/education_schools_*, another
extraction; csv/education_schools.csv belongs to it).
"""
import csv
import json
import re
import sys
from collections import defaultdict, OrderedDict
from pathlib import Path

HERE = Path(__file__).resolve().parent
TR = HERE / "transcribed"
OUT = HERE / "csv"

EDITIONS = OrderedDict([
    ("sgt1922", "bpt6k9105649x"), ("sgt1923", "bpt6k9105649x"), ("sgt1924", "bpt6k9105649x"),
    ("sgt1925", "bpt6k9105650k"), ("sgt1926", "bpt6k9105650k"), ("sgt1927", "bpt6k91056510"),
    ("sgt1928", "bpt6k91056510"), ("sgt1929", "bpt6k9105652d"), ("sgt1930", "bpt6k9105652d"),
    ("sgt1935", "bpt6k9105653t"), ("sgt1936", "bpt6k91056547"), ("sgt1939", "bpt6k9105739w"),
])
ORDER = list(EDITIONS)
YEAR = {e: int(e[3:]) for e in ORDER}
# chapter view ranges (first view = chapter heading; the view after the last is the next chapter's
# heading), confirmed on the images for all 12 editions
CHAPTER = {"sgt1922": (113, 152), "sgt1923": (597, 636), "sgt1924": (1087, 1126),
           "sgt1925": (123, 162), "sgt1926": (673, 712), "sgt1927": (135, 174),
           "sgt1928": (659, 698), "sgt1929": (137, 176), "sgt1930": (671, 710),
           "sgt1935": (99, 108), "sgt1936": (68, 77), "sgt1939": (65, 76)}

NATS = [("french", "Français", "Françaises"), ("muslim", "Musulmans", "Musulmanes"),
        ("jewish", "Israélites", "Israélites"), ("italian", "Italiens", "Italiennes"),
        ("maltese", "Maltais", "Maltaises"), ("other", "Divers", "Diverses")]
SEX = [("male", "Garçons"), ("female", "Filles")]
SEX_EXAM = [("male", "Aspirants"), ("female", "Aspirantes")]
STAGE = {"examined": "Candidats examinés", "passed": "Candidats reçus"}
COMMON = ["census", "table_id", "gallica_ark", "source_page", "gallica_view", "year"]

# ---------------------------------------------------------------- parsing


def nums(s):
    return [None if t == "." else int(t) for t in s.split()]


class Section:
    def __init__(self, name, attrs, ed):
        self.name, self.attrs, self.ed = name, attrs, ed
        self.lines, self.notes, self.years, self.flags = [], [], None, {}
        v = attrs.get("view") or attrs.get("views")
        p = attrs.get("page") or attrs.get("pages")
        self.views = [int(x) for x in v.split(",")]
        self.pages = [int(x) for x in p.split(",")]

    def base(self, which=0):
        i = min(which, len(self.views) - 1)
        return dict(census=self.ed, table_id=self.name, gallica_ark=EDITIONS[self.ed],
                    source_page=self.pages[min(i, len(self.pages) - 1)], gallica_view=self.views[i])


def read_edition(ed):
    secs, cur = [], None
    for raw in (TR / f"education_sum_{ed}.txt").read_text(encoding="utf-8").splitlines():
        l = raw.strip()
        if not l or l.startswith("#"):
            continue
        m = re.match(r"^\[(\w+)\s*(.*)\]$", l)
        if m:
            cur = Section(m.group(1), dict(re.findall(r"(\w+)=(\S+)", m.group(2))), ed)
            secs.append(cur)
        elif l.startswith("note:"):
            cur.notes.append(l[5:].strip())
        elif re.match(r"^years?:", l):
            cur.years = [int(y) for y in l.split(":", 1)[1].split()]
        elif l.startswith("flag:"):
            k, v = l[5:].rsplit("=", 1)
            cur.flags[tuple(x.strip() for x in k.split(";"))] = v.strip()
        else:
            if "?" in l:
                raise ValueError(f"{ed}: unresolved '?' in {l}")
            cur.lines.append([f.strip() for f in l.split("|")])
    return secs


# ---------------------------------------------------------------- checks


class Checks:
    def __init__(self):
        self.n = defaultdict(int)
        self.fail = defaultdict(list)

    def eq(self, topic, what, got, printed):
        if got is None or printed is None:
            return True
        self.n[topic] += 1
        if got != printed:
            self.fail[topic].append(f"{what}: cells give {got}, printed {printed}")
            return False
        return True


CHK = Checks()
XCHK = Checks()          # cross-table checks, reported in the notes of the table named as topic


def ssum(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) if xs else 0


ROWS = defaultdict(list)                 # output name -> list of row dicts (rule 5 tables)
NOTES = defaultdict(list)                # output name -> [(edition, footnote)]


def add_notes(out, sec):
    for n in sec.notes:
        NOTES[out].append((sec.ed, n))


def nat_rows(out, sec, which, year, dims, vals, sex, flagkey, extra_flag=""):
    """One row per nationality cell of a 6-cell block."""
    sx, sxfr = sex
    for k, (nat, nm, nf) in enumerate(NATS):
        v = vals[k]
        f = sec.flags.get(flagkey + (sx, nat), "") or extra_flag
        if v is None:
            f = f or "not_applicable"
        ROWS[out].append(dict(sec.base(which), year=year, **dims, sex=sx, sex_fr=sxfr, nationality=nat,
                              nationality_fr=nm if sx == "male" else nf, value=v, flag=f))


def check_block(topic, what, vals):
    """6 nationality cells + printed TOTAUX."""
    return CHK.eq(topic, what + ": nationalities vs TOTAUX", ssum(vals[:6]), vals[6])


# ---------------------------------------------------------------- rule-5 tables

TOTALS = {}            # ed -> printed total of the total page
EST_TOT = {}           # ed -> (boys7, girls7, gen) TOTAUX row of the civil-personality table
EST_PREV = {}          # ed -> {name: prev} and {name: gen}
EST_THIS = {}
POP = {}               # ed -> {code: (boys7, girls7, both6, gen, prev)}
PRIM = {}              # ed -> {code: (boys7, girls7, gen, prev)}
COMPAR = {}            # ed -> {code: {year: value}}
QUINQ = {}             # ed -> {year: (b3, g3, t)}
SEC39 = {}             # kind/name -> (b, g, gen)


def t_total(sec):
    out = "education_total_pupils"
    add_notes(out, sec)
    year = sec.years[0]
    for code, label, v in sec.lines:
        ROWS[out].append(dict(sec.base(), year=year, label_fr=label, value=int(v), flag=""))
        TOTALS[sec.ed] = int(v)


EXAM_EN = {}


def t_exams(sec):
    out = "education_exams_nationality"
    add_notes(out, sec)
    year = YEAR[sec.ed]
    for code, label, stage, boys, girls, gen in sec.lines:
        b, g, gen = nums(boys), nums(girls), nums(gen)[0]
        what = f"{sec.ed} {code} {stage}"
        ok1 = check_block(out, what + " boys", b)
        ok2 = check_block(out, what + " girls", g)
        CHK.eq(out, what + ": boys TOTAUX + girls TOTAUX vs TOTAUX GÉNÉRAUX", (b[6] or 0) + (g[6] or 0)
               if b[6] is not None and g[6] is not None else None, gen)
        CHK.eq(out, what + ": all cells vs TOTAUX GÉNÉRAUX", ssum(b[:6]) + ssum(g[:6]), gen)
        EXAM_EN[code] = label
        for sx, vals in ((SEX_EXAM[0], b), (SEX_EXAM[1], g)):
            nat_rows(out, sec, 0, year, dict(exam=code, exam_fr=label, stage=stage, stage_fr=STAGE[stage]),
                     vals, (["male", "female"][sx is SEX_EXAM[1]], sx[1]), (code, stage))


def t_establishments(sec):
    out = "education_civil_personality_establishments"
    add_notes(out, sec)
    year = YEAR[sec.ed]
    data = [l for l in sec.lines if l[0] != "TOTAUX"]
    tot = [l for l in sec.lines if l[0] == "TOTAUX"]
    col = defaultdict(int)
    EST_PREV[sec.ed], EST_THIS[sec.ed] = {}, {}
    for loc, name, classes, boys, girls, gen, prev in data:
        b, g, gen, prev, cl = nums(boys), nums(girls), nums(gen)[0], nums(prev)[0], nums(classes)[0]
        what = f"{sec.ed} {name}"
        check_block(out, what + " boys", b)
        check_block(out, what + " girls", g)
        CHK.eq(out, what + ": boys + girls TOTAUX vs TOTAUX GÉNÉRAUX", b[6] + g[6], gen)
        CHK.eq(out, what + ": all cells vs TOTAUX GÉNÉRAUX", ssum(b[:6]) + ssum(g[:6]), gen)
        d = dict(locality=loc, establishment=name)
        ROWS[out].append(dict(sec.base(), year=year, **d, measure="classes", measure_fr="Nombre de classes",
                              sex="total", sex_fr="", nationality="total", nationality_fr="", value=cl, flag=""))
        for sx, vals in ((SEX[0], b), (SEX[1], g)):
            nat_rows(out, sec, 0, year, dict(d, measure="pupils", measure_fr="Élèves"), vals, sx, (name,))
            for k in range(7):
                col[(sx[0], k)] += vals[k] or 0
        ROWS[out].append(dict(sec.base(), year=year - 1, **d, measure="pupils_total_previous_year",
                              measure_fr="Totaux généraux de l'année précédente", sex="total", sex_fr="",
                              nationality="total", nationality_fr="", value=prev, flag=""))
        col["classes"] += cl or 0
        col["gen"] += gen
        col["prev"] += prev
        EST_PREV[sec.ed][name] = prev
        EST_THIS[sec.ed][name] = gen
    for _, _, classes, boys, girls, gen, prev in tot:
        b, g = nums(boys), nums(girls)
        CHK.eq(out, f"{sec.ed} classes column vs Totaux", col["classes"], nums(classes)[0])
        for sx, vals in (("male", b), ("female", g)):
            for k in range(7):
                CHK.eq(out, f"{sec.ed} {sx} column {k} vs Totaux", col[(sx, k)], vals[k])
        CHK.eq(out, f"{sec.ed} TOTAUX GÉNÉRAUX column vs Totaux", col["gen"], nums(gen)[0])
        CHK.eq(out, f"{sec.ed} previous-year column vs Totaux", col["prev"], nums(prev)[0])
        EST_TOT[sec.ed] = (b, g, nums(gen)[0], nums(prev)[0])


def t_by_class(sec, out):
    """École de musique (one 7-cell block) or école de commerce (boys | girls | general)."""
    add_notes(out, sec)
    year = YEAR[sec.ed]
    col = defaultdict(int)
    for line in sec.lines:
        code, label, *blocks = line
        if len(blocks) == 1:
            v = nums(blocks[0])
            if code == "TOTAUX":
                for k in range(7):
                    CHK.eq(out, f"{sec.ed} column {k} vs column-total line", col[k], v[k])
                continue
            check_block(out, f"{sec.ed} {code}", v)
            if code != "enrolled":
                for k in range(7):
                    col[k] += v[k] or 0
            nat_rows(out, sec, 0, year, dict(**{"class": code}, class_fr=label), v, ("total", ""), (code,))
            for r in ROWS[out][-6:]:
                r["sex_fr"], r["nationality_fr"] = "", NATS[[n[0] for n in NATS].index(r["nationality"])][1]
        else:
            b, g, t = nums(blocks[0]), nums(blocks[1]), nums(blocks[2])[0]
            check_block(out, f"{sec.ed} {code} boys", b)
            check_block(out, f"{sec.ed} {code} girls", g)
            CHK.eq(out, f"{sec.ed} {code}: boys + girls TOTAUX vs TOTAUX GÉNÉRAUX", b[6] + g[6], t)
            CHK.eq(out, f"{sec.ed} {code}: all cells vs TOTAUX GÉNÉRAUX", ssum(b[:6]) + ssum(g[:6]), t)
            for sx, vals in ((SEX[0], b), (SEX[1], g)):
                nat_rows(out, sec, 0, year, dict(course=code, course_fr=label), vals, sx, (code,))


POP_TYPE = {"public_primary": "Écoles primaires publiques", "civil_personality": "Établissements à personnalité civile",
            "private": "Écoles privées"}


def t_population(sec, out, store_codes):
    """Population scolaire (boys7 | girls7 | both6 | gen | prev), sgt1922-1939, and the
    total of primary education (boys7 | girls7 | gen | prev)."""
    add_notes(out, sec)
    year = YEAR[sec.ed]
    rows, compare = OrderedDict(), OrderedDict()
    for line in sec.lines:
        if line[0].startswith("compare"):
            compare[int(line[0].split()[1])] = [nums(x) for x in line[1:]]
        else:
            rows[line[0]] = (line[1], [nums(x) for x in line[2:]])
    both = len(next(iter(rows.values()))[1]) == 5
    res = {}
    for code, (label, bl) in rows.items():
        b, g = bl[0], bl[1]
        gen, prev = bl[-2][0], bl[-1][0]
        what = f"{sec.ed} {code}"
        check_block(out, what + " boys", b)
        check_block(out, what + " girls", g)
        CHK.eq(out, what + ": boys + girls TOTAUX vs TOTAUX GÉNÉRAUX", b[6] + g[6], gen)
        if both:
            for k in range(6):
                CHK.eq(out, what + f" {NATS[k][0]}: boys + girls vs garçons et filles", b[k] + g[k], bl[2][k])
            CHK.eq(out, what + ": garçons et filles columns vs TOTAUX GÉNÉRAUX", ssum(bl[2]), gen)
        res[code] = (b, g, bl[2] if both else None, gen, prev)
        if code not in store_codes:
            continue
        d = dict(school_type=code, school_type_fr=label)
        for sx, vals in ((SEX[0], b), (SEX[1], g)):
            nat_rows(out, sec, 0 if sx[0] == "male" else 1, year, dict(d, measure="pupils"), vals, sx, (code,))
        ROWS[out].append(dict(sec.base(1), year=year - 1, **d, measure="pupils_total_previous_year", sex="total",
                              sex_fr="", nationality="total", nationality_fr="", value=prev, flag=""))

    def colcheck(tot, members):
        if tot not in rows or not all(m in rows for m in members):
            return
        tb = rows[tot][1]
        for bi in range(len(tb)):
            for k in range(len(tb[bi])):
                CHK.eq(out, f"{sec.ed} {tot} block {bi} column {k}: rows vs total line",
                       ssum(rows[m][1][bi][k] for m in members), tb[bi][k])
    data = [c for c in rows if not c.isupper()]
    if "TOTAUX" in rows:
        colcheck("TOTAUX", data)
    if "TOTAL" in rows:
        colcheck("TOTAL", data)
    if "TOTAL_PUBLIC" in rows:
        colcheck("TOTAL_PUBLIC", [c for c in data if c != "private"])
        colcheck("TOTAL_GENERAL", ["TOTAL_PUBLIC", "private"])
    for y, bl in compare.items():
        b, g = bl[0], bl[1]
        check_block(out, f"{sec.ed} comparison {y} boys", b)
        check_block(out, f"{sec.ed} comparison {y} girls", g)
        CHK.eq(out, f"{sec.ed} comparison {y}: boys + girls vs TOTAUX", b[6] + g[6], bl[3][0])
        for k in range(6):
            CHK.eq(out, f"{sec.ed} comparison {y} {NATS[k][0]}: boys + girls vs garçons et filles", b[k] + g[k],
                   bl[2][k])
        for sx, vals in ((SEX[0], b), (SEX[1], g)):
            for k, (nat, nm, nf) in enumerate(NATS):
                SERIES["education_school_population_series"].add(
                    sec, 0 if sx[0] == "male" else 1, y, (sx[0], nat), vals[k], dict(sex=sx[0], sex_fr=sx[1], nationality=nat,
                                                           nationality_fr=nm if sx[0] == "male" else nf),
                    sec.flags.get((f"compare {y}", sx[0], nat), ""))
    if "TOTAL_GENERAL" in rows:
        b, g = rows["TOTAL_GENERAL"][1][0], rows["TOTAL_GENERAL"][1][1]
        for sx, vals in ((SEX[0], b), (SEX[1], g)):
            for k, (nat, nm, nf) in enumerate(NATS):
                SERIES["education_school_population_series"].add(
                    sec, 0 if sx[0] == "male" else 1, year, (sx[0], nat), vals[k], dict(sex=sx[0], sex_fr=sx[1], nationality=nat,
                                                              nationality_fr=nm if sx[0] == "male" else nf),
                    sec.flags.get(("TOTAL_GENERAL", sx[0], nat), ""))
    return res


def t_vocational(sec):
    out = "education_vocational"
    add_notes(out, sec)
    year = YEAR[sec.ed]
    run, group = 0, []
    for loc, label, v in sec.lines:
        v = int(v)
        if loc == "SUBTOTAL":
            CHK.eq(out, f"{sec.ed} Tunis schools vs bracket total", ssum(r["value"] for r in group), v)
            run += v - ssum(r["value"] for r in group)      # the running total follows the printed bracket
            group = []
            continue
        if loc in ("REPORT", "TOTAL"):
            CHK.eq(out, f"{sec.ed} running sum vs '{label}'", run, v)
            continue
        run += v
        r = dict(sec.base(), year=year, locality="Tunis" if loc == "TUNIS" else loc, school_fr=label, value=v,
                 flag=sec.flags.get((label,), ""))
        ROWS[out].append(r)
        if loc == "TUNIS":
            group.append(r)


def t_quinquennial(sec):
    out = "education_quinquennial_pupils"
    add_notes(out, sec)
    QUINQ[sec.ed] = {}
    for y, boys, girls, tot in sec.lines:
        y = int(y)
        b, g, t = nums(boys), nums(girls), nums(tot)[0]
        CHK.eq(out, f"{sec.ed} {y} boys: public + private vs total", b[0] + b[1], b[2])
        CHK.eq(out, f"{sec.ed} {y} girls: public + private vs total", g[0] + g[1], g[2])
        CHK.eq(out, f"{sec.ed} {y}: boys total + girls total vs total général", b[2] + g[2], t)
        CHK.eq(out, f"{sec.ed} {y}: four cells vs total général", b[0] + b[1] + g[0] + g[1], t)
        QUINQ[sec.ed][y] = (b, g, t)
        for sx, vals in ((SEX[0], b), (SEX[1], g)):
            for k, (sc, scfr) in enumerate((("public", "Enseignement public"), ("private", "Enseignement privé"))):
                SERIES[out].add(sec, 0, y, (sx[0], sc), vals[k],
                                dict(sex=sx[0], sex_fr=sx[1], sector=sc, sector_fr=scfr),
                                sec.flags.get((str(y), sx[0], sc), ""))


def t_two_year(out, sec, groups=None):
    """Libraries, arabic courses, canteens: two-year windows (rule 4)."""
    add_notes(out, sec)
    ys = sec.years
    blocks_all = [l[2:] for l in sec.lines]
    if out == "education_canteens":
        d = {l[0]: nums(l[2]) for l in sec.lines}
        for i, y in enumerate(ys):
            CHK.eq(out, f"{sec.ed} {y}: free + paying vs Totaux", d["free"][i] + d["paying"][i], d["TOTAUX"][i])
    for line in sec.lines:
        code, label, *blocks = line
        if code.isupper():
            continue
        gl = groups or [(None, None)]
        for (gc, gfr), blk in zip(gl, blocks):
            for y, v in zip(ys, nums(blk)):
                if v is None:
                    continue
                key = (code, gc) if gc else (code,)
                dims = dict(item=code, item_fr=label)
                if gc:
                    dims = dict(library=code, library_fr=label, measure=gc, measure_fr=gfr)
                if out == "education_arabic_courses":
                    dims = dict(course=code, course_fr=label)
                if out == "education_canteens":
                    dims = dict(portions=code, portions_fr=label)
                SERIES[out].add(sec, 0, y, key, v, dims, sec.flags.get((code, str(y)), ""))


def t_comparative(sec):
    out = "education_comparative"
    add_notes(out, sec)
    ys = sec.years
    d = {l[0]: nums(l[2]) for l in sec.lines}
    COMPAR[sec.ed] = {c: dict(zip(ys, v)) for c, v in d.items()}
    incl_auditors_in_public = sec.ed != "sgt1939"
    for i, y in enumerate(ys):
        g = lambda c: d[c][i] if c in d else None
        pm = [d[c][i] for c in d if c.startswith("pupils") and c.endswith(" male")]
        pf = [d[c][i] for c in d if c.startswith("pupils") and c.endswith(" female")]
        CHK.eq(out, f"{sec.ed} {y}: boys by nationality vs comparaison par sexes, garçons", sum(pm), g("TOTAL_MALE"))
        CHK.eq(out, f"{sec.ed} {y}: girls by nationality vs comparaison par sexes, filles", sum(pf), g("TOTAL_FEMALE"))
        if incl_auditors_in_public:
            CHK.eq(out, f"{sec.ed} {y}: pupils + adult auditors vs total public", sum(pm) + sum(pf) + g("adult_auditors"),
                   g("TOTAL_PUBLIC"))
            CHK.eq(out, f"{sec.ed} {y}: total public + private vs total général", g("TOTAL_PUBLIC") + g("private_pupils"),
                   g("TOTAL_GENERAL"))
        else:
            CHK.eq(out, f"{sec.ed} {y}: pupils vs total public (auditors excluded in this edition)", sum(pm) + sum(pf),
                   g("TOTAL_PUBLIC"))
            CHK.eq(out, f"{sec.ed} {y}: total public + private + adult auditors vs total général",
                   g("TOTAL_PUBLIC") + g("private_pupils") + g("adult_auditors"), g("TOTAL_GENERAL"))
    for code, label, vals in sec.lines:
        if code.isupper():
            continue
        if code.startswith("pupils"):
            _, nat, sx = code.split()
            dims = dict(item="pupils_public", item_fr=label, sex=sx, nationality=nat)
            key = ("pupils_public", sx, nat)
        else:
            dims = dict(item=code, item_fr=label, sex="", nationality="")
            key = (code,)
        for y, v in zip(ys, nums(vals)):
            SERIES[out].add(sec, 0, y, key, v, dims, "")


def t_secondary_1939(sec):
    out = "education_secondary_establishments_sgt1939"
    add_notes(out, sec)
    year = YEAR[sec.ed]
    run = defaultdict(lambda: [[0] * 7, [0] * 7, 0])
    for kind, branch, name, boys, girls, gen in sec.lines:
        b, g, gen = nums(boys), nums(girls), nums(gen)[0]
        what = f"{sec.ed} {branch} {name}"
        check_block(out, what + " boys", b)
        check_block(out, what + " girls", g)
        CHK.eq(out, what + ": boys + girls TOTAUX vs TOTAUX GÉNÉRAUX", b[6] + g[6], gen)
        SEC39[(kind, branch)] = (b, g, gen)
        if kind == "school":
            # a school counts in the current group (the schools since the last subtotal), its branch and the
            # grand total; the running TOTAUX GÉNÉRAUX uses the cells (a misprinted school total does not propagate)
            for key in ((branch, "group"), (branch, "all"), ("all", "all")):
                for k in range(7):
                    run[key][0][k] += b[k] or 0
                    run[key][1][k] += g[k] or 0
                run[key][2] += ssum(b[:6]) + ssum(g[:6])
            for sx, vals in ((SEX[0], b), (SEX[1], g)):
                nat_rows(out, sec, _SEC39_VIEW.get((branch, name), 0), year,
                         dict(branch=branch, branch_fr=BRANCH_FR[branch], establishment=name), vals, sx, (name,))
            continue
        if kind in ("sub_boys", "sub_girls"):
            key = (branch, "group")
        elif kind == "branch_total":
            key = (branch, "all")
        elif kind == "grand_total":
            key = ("all", "all")
        else:
            if kind == "primary_classes":
                SEC39["primary_classes"] = (b, g, gen)
            if kind == "net_total":
                gt, pc = SEC39[("grand_total", "all")], SEC39["primary_classes"]
                for k in range(7):
                    CHK.eq(out, f"{sec.ed} net total boys column {k}: total général - primary classes",
                           gt[0][k] - pc[0][k], b[k])
                    CHK.eq(out, f"{sec.ed} net total girls column {k}: total général - primary classes",
                           gt[1][k] - pc[1][k], g[k])
                CHK.eq(out, f"{sec.ed} net total TOTAUX GÉNÉRAUX: total général - primary classes", gt[2] - pc[2], gen)
            continue
        for k in range(7):
            CHK.eq(out, f"{sec.ed} '{name}' ({branch}) boys column {k}: schools vs printed", run[key][0][k], b[k])
            CHK.eq(out, f"{sec.ed} '{name}' ({branch}) girls column {k}: schools vs printed", run[key][1][k], g[k])
        CHK.eq(out, f"{sec.ed} '{name}' ({branch}) TOTAUX GÉNÉRAUX: schools vs printed", run[key][2], gen)
        if kind in ("sub_boys", "sub_girls"):
            run[key] = [[0] * 7, [0] * 7, 0]


BRANCH_FR = {"secondary": "A. Enseignement secondaire", "higher_primary": "B. Enseignement primaire supérieur",
             "technical": "C. Enseignement technique"}
# view index (0 = view 70 / page 64, 1 = view 71 / page 65) of each sgt1939 secondary row
_SEC39_VIEW = defaultdict(int)


def _sec39_views():
    for n in ("École Émile-Loubet, Tunis", "École de commerce, Tunis (garçons)", "Collège de Bizerte",
              "École de commerce, Tunis (filles)", "École Paul-Cambon, Tunis", "École primaire supérieure, Bizerte",
              "École primaire supérieure, Sousse", "École primaire supérieure, Radès"):
        _SEC39_VIEW[("technical", n)] = 1


_sec39_views()


def t_first_degree_1939(sec):
    out = "education_first_degree_sgt1939"
    add_notes(out, sec)
    res = t_population(sec, out, ("estab_primary_classes", "first_degree_establishments"))
    PRIM[sec.ed] = res


# ---------------------------------------------------------------- rule-4 series

# (output, year, key) -> edition whose printing is kept instead of the latest (flag reprint_corrected)
REPRINT = {
    # sgt1927-sgt1939 print 10.999; 10.799 + 2.159 = 12.958 (the boys' total printed by every edition)
    ("education_quinquennial_pupils", 1905, ("male", "public")): "sgt1926",
    # sgt1939 prints 3.416; 16.756 + 3.419 = 20.175 (printed by every edition), as in sgt1925-sgt1936
    ("education_quinquennial_pupils", 1925, ("female", "private")): "sgt1936",
}


class Series:
    def __init__(self, out):
        self.out = out
        self.p = defaultdict(dict)      # (year, key) -> {ed: (value, base, dims, flag)}
        self.order = {}

    def add(self, sec, which, year, key, value, dims, flag):
        self.p[(year, key)][sec.ed] = (value, sec.base(which), dims, flag)
        self.order.setdefault(key, len(self.order))

    def printed_years(self):
        py = defaultdict(set)
        for (y, k), by in self.p.items():
            for e in by:
                py[e].add(y)
        return {e: sorted(py[e]) for e in ORDER if e in py}

    def resolve(self):
        year_eds = defaultdict(set)
        for (y, k), by in self.p.items():
            year_eds[y].update(by)
        rows, compared, diffs, unmatched = [], 0, [], []
        for (y, key), by in sorted(self.p.items(), key=lambda kv: (kv[0][0], self.order[kv[0][1]])):
            ed = [e for e in ORDER if e in year_eds[y]][-1]
            for e in by:
                if e != ed:
                    if ed in by:
                        compared += 1
                        if by[e][0] != by[ed][0]:
                            diffs.append((y, key, e, by[e][0], ed, by[ed][0]))
                    else:
                        unmatched.append((y, key, e, by[e][0], ed))
            if ed not in by:
                continue
            v, base, dims, flag = by[ed]
            if (self.out, y, key) in REPRINT:
                e2 = REPRINT[(self.out, y, key)]
                v, base, flag = by[e2][0], by[e2][1], "reprint_corrected"
            rows.append(dict(base, year=y, **dims, value=v, flag=flag, _key=key))
        return rows, compared, diffs, unmatched


SERIES = {n: Series(n) for n in ("education_school_population_series", "education_quinquennial_pupils",
                                 "education_libraries", "education_arabic_courses", "education_canteens",
                                 "education_comparative")}


# ---------------------------------------------------------------- outputs

OUTPUTS = OrderedDict([
    # name: (rule, dims, French title, English title)
    ("education_total_pupils", (5, ["label_fr"],
        "Total général des élèves de l'enseignement public et privé au 31 décembre",
        "Total pupils, public and private education, at 31 December")),
    ("education_exams_nationality", (5, ["exam", "exam_fr", "stage", "stage_fr", "sex", "sex_fr", "nationality",
                                         "nationality_fr"],
        "Examens : répartition des candidats par nationalité",
        "Examinations: candidates examined and passed, by exam, nationality and sex")),
    ("education_civil_personality_establishments", (5, ["locality", "establishment", "measure", "measure_fr", "sex",
                                                        "sex_fr", "nationality", "nationality_fr"],
        "Enseignements supérieur, secondaire et spécial : établissements à personnalité civile",
        "Higher, secondary and special education: establishments with civil personality (classes, pupils by "
        "nationality and sex), sgt1922–sgt1936")),
    ("education_secondary_establishments_sgt1939", (5, ["branch", "branch_fr", "establishment", "sex", "sex_fr",
                                                        "nationality", "nationality_fr"],
        "Établissements d'enseignement secondaire, primaire supérieur ou technique : population scolaire",
        "Secondary, higher-primary and technical establishments: pupils by nationality and sex (sgt1939)")),
    ("education_libraries", (4, ["library", "library_fr", "measure", "measure_fr"],
        "Bibliothèques", "Libraries: loans and volumes lent")),
    ("education_arabic_courses", (4, ["course", "course_fr"],
        "École supérieure de langue et de littérature arabes : auditeurs des cours",
        "Higher School of Arabic Language and Literature: course auditors")),
    ("education_music_school", (5, ["class", "class_fr", "sex", "sex_fr", "nationality", "nationality_fr"],
        "École de musique : répartition des élèves dans les différentes classes",
        "School of music: pupils by class and nationality")),
    ("education_commerce_school", (5, ["course", "course_fr", "sex", "sex_fr", "nationality", "nationality_fr"],
        "École de commerce : répartition des élèves dans les différents cours",
        "School of commerce: pupils by course, nationality and sex (sgt1936, sgt1939)")),
    ("education_primary_totals", (5, ["school_type", "school_type_fr", "measure", "sex", "sex_fr", "nationality",
                                      "nationality_fr"],
        "Total général de l'enseignement primaire", "Total of primary education, by type, nationality and sex "
        "(sgt1922–sgt1936)")),
    ("education_first_degree_sgt1939", (5, ["school_type", "school_type_fr", "measure", "sex", "sex_fr",
                                            "nationality", "nationality_fr"],
        "Total général de la population scolaire du premier degré",
        "Total first-degree school population (sgt1939)")),
    ("education_vocational", (5, ["locality", "school_fr"],
        "Enseignement professionnel de la population indigène (apprentissage)",
        "Vocational education of the indigenous population: apprentices by school")),
    ("education_canteens", (4, ["portions", "portions_fr"],
        "Cantines scolaires : portions délivrées", "School canteens: portions served")),
    ("education_school_population", (5, ["school_type", "school_type_fr", "measure", "sex", "sex_fr",
                                         "nationality", "nationality_fr"],
        "Statistique comparée : population scolaire au 31 décembre",
        "Comparative statistics: school population at 31 December by type of school, nationality and sex")),
    ("education_school_population_series", (4, ["sex", "sex_fr", "nationality", "nationality_fr"],
        "Population scolaire : total général des établissements scolaires français publics et privés",
        "School population, all French public and private schools, by nationality and sex (yearly series)")),
    ("education_quinquennial_pupils", (4, ["sex", "sex_fr", "sector", "sector_fr"],
        "Statistique quinquennale des élèves (depuis 1885)",
        "Quinquennial series of pupils since 1885: boys and girls, public and private")),
    ("education_comparative", (4, ["item", "item_fr", "sex", "nationality"],
        "Tableau comparatif", "Comparative table: establishments, classes, public pupils by nationality and sex, "
        "adult auditors, private pupils")),
])

COLDOC = {
    "census": "edition the value is taken from (`sgt1922` … `sgt1939`)",
    "table_id": "transcription section the value comes from",
    "gallica_ark": "Gallica volume ark (views are numbered within a volume)",
    "source_page": "printed page number; pages without a printed number are inferred from the next page. For the "
                   "two-page spreads (population, primary-education and first-degree totals) the boys' block is given "
                   "the left-hand page and the girls' block and total columns the right-hand page (the printed fold "
                   "falls near the boys' TOTAUX, so one or two boys' columns may in fact sit on the right-hand page)",
    "gallica_view": "Gallica view (fNNNN)",
    "year": "year the value refers to (31 December of that year for pupils; the school year's examinations)",
    "value": "count (integer); printed » = 0; empty where the cell is not printed (`not_applicable`)",
    "flag": "empty, or `ocr_corrected`, `derived_from_totals`, `total_mismatch`, `not_applicable`, "
            "`reprint_corrected` (see below)",
    "label_fr": "heading of the total page as printed",
    "exam": "English code of the examination", "exam_fr": "examination as printed (with its group heading)",
    "stage": "`examined` or `passed`", "stage_fr": "as printed",
    "sex": "`male`, `female`; `total` where the cell is not split by sex (empty in the comparative table for items "
           "that are not pupils)",
    "sex_fr": "column heading as printed (Aspirants / Aspirantes in the examination table, Garçons / Filles elsewhere)",
    "nationality": "`french`, `muslim`, `jewish`, `italian`, `maltese`, `other` (Divers); `total` where not split",
    "nationality_fr": "column heading as printed (masculine for boys, feminine for girls)",
    "locality": "locality as printed", "establishment": "establishment as printed",
    "measure": "what is counted (see below)", "measure_fr": "as printed",
    "branch": "`secondary`, `higher_primary`, `technical`", "branch_fr": "branch heading as printed",
    "library": "English code", "library_fr": "library as printed",
    "course": "English code", "course_fr": "course as printed",
    "class": "English code", "class_fr": "class as printed",
    "school_type": "English code (see below)", "school_type_fr": "row label as printed",
    "school_fr": "school as printed",
    "portions": "`free` (Gratuites) or `paying` (Payantes)", "portions_fr": "as printed",
    "sector": "`public` or `private`", "sector_fr": "as printed",
    "item": "English code (see below)", "item_fr": "row label as printed in the edition the value is taken from",
}

COMMENT = defaultdict(list)
COMMENT.update({
    "education_total_pupils": [
        "The chapter's opening page prints one figure: the total of pupils of public and private education at 31 "
        "December of the edition year. It equals the \"Total général des élèves de l'enseignement public et de "
        "l'enseignement privé\" of the comparative table, which includes the auditors of the adult courses, in "
        "sgt1922–sgt1936. In sgt1939 the total page prints 97.599, the total without the 677 adult auditors "
        "(= the population table's total général), while that edition's comparative table prints 98.276 with them; "
        "see the cross-checks.",
    ],
    "education_exams_nationality": [
        "Table b) \"Examens ; répartition des candidats par nationalité\": for each examination, candidates "
        "examined (`examined`) and passed (`passed`), aspirants (boys/men) and aspirantes (girls/women) by "
        "nationality. The TOTAUX per sex and the TOTAUX GÉNÉRAUX are not stored. The list of examinations changes "
        "between editions (codes): `cepe` CEPE; `brevet_elementaire`; `beps` (one line, sgt1922–sgt1926) and from "
        "sgt1927 its sections `beps_general`, `beps_commercial`, `beps_agricultural`, `beps_domestic` (ménagère), "
        "`beps_arts_crafts`, `beps_industrial`; `brevet_superieur`; `baccalaureat`; Arabic examinations "
        "`arabic_spoken_cert`, `arabic_brevet_elementaire`, `arabic_diplome_superieur`; teaching certificates "
        "`gymnastics_teaching_cert` (from sgt1935 \"éducation physique\": `physical_education_teaching_cert`) and "
        "`sewing_teaching_cert`; `sadiki_secondary_diploma`; École Émile-Loubet diploma and 3rd-year certificate; "
        "École Paul-Cambon certificates (commercial, industrial, manual work; 4th-year commercial exam in sgt1930; "
        "commerce-school diploma from sgt1935); girls' secondary certificates and diplomas "
        "(`girls_secondary_*`). An exam printed with all cells » is stored with zeros.",
        "Failed checks (listed below): every cell was re-read on native-resolution crops and the printed figures "
        "are kept; the faulty cell or total cannot be identified, so no cell is flagged. Flagged cells: sgt1923 "
        "Baccalauréat passed, boys, Italiens is blank on the page and was solved from the TOTAUX (114) "
        "(`derived_from_totals`). sgt1936 CEPE examined, boys, Maltais: broken second digit, read as 44, which "
        "closes both totals (`ocr_corrected`). sgt1927 Section ménagère examined, girls: the TOTAUX cell is "
        "printed » although the cells and the TOTAUX GÉNÉRAUX give 4 (treated as not printed). sgt1936 Brevet "
        "supérieur passed, girls: TOTAUX printed \"3\" for 31.",
    ],
    "education_civil_personality_establishments": [
        "Table a) \"Établissements à personnalité civile\" (Lycée Carnot, Collège Sadiki, Collège Alaoui, Écoles "
        "normales d'instituteurs and d'institutrices, École professionnelle Émile-Loubet, Lycée Armand-Fallières, "
        "Petit Lycée Jules-Ferry; all in Tunis), sgt1922–sgt1936. Measures: `classes` (Nombre de classes), `pupils` "
        "by sex and nationality, and `pupils_total_previous_year` (the printed \"Totaux généraux de l'année "
        "précédente\", stored with `year` = the previous year: it is the only source for 1921 and 1934, and for the "
        "other years it is compared with the previous edition's own total, see the cross-checks). The edition's own "
        "row totals and the Totaux line are not stored. From sgt1939 the table is replaced by the secondary, "
        "higher-primary and technical establishments (`education_secondary_establishments_sgt1939.csv`).",
        "The pupils include the primary (elementary) classes of these establishments (Petit Collège Sadiki, "
        "écoles d'application, Petit Lycée), which the total of primary education reprints (see "
        "`education_primary_totals.csv`). sgt1935: the classes cell of the École normale d'institutrices reads "
        "\"14 classes et 3 ateliers\" (14 stored).",
        "Failed checks: sgt1922 Petit Lycée Jules-Ferry girls' TOTAUX printed 592 for 502 (the cells, the TOTAUX "
        "GÉNÉRAUX 502 and the column total 1.411 all give 502); sgt1935 previous-year column: the eight cells sum to "
        "6.985 against the printed 6.935.",
    ],
    "education_secondary_establishments_sgt1939": [
        "sgt1939 only (views 70–71, pages 64–65): \"Établissements d'enseignement secondaire, primaire supérieur ou "
        "technique — population scolaire (y compris les classes d'enseignement du premier degré)\". One row per "
        "establishment, sex and nationality; an establishment can appear in more than one branch (e.g. Collège "
        "Stéphen-Pichon, Bizerte, in secondary and higher-primary), the cells are the pupils of that branch. The "
        "École de commerce de Tunis is printed twice in the technical branch (boys' and girls' sections); the "
        "labels carry \"(garçons)\" / \"(filles)\" to tell them apart. The subtotals (établissements de garçons / "
        "de jeunes filles), branch totals and the \"Total général du 2e degré\" (12.690) are checks only. The "
        "last two lines, \"Élèves fréquentant les classes d'enseignement primaire élémentaire de ces "
        "établissements\" (4.351) and \"Total des élèves des cours d'enseignement de 2e degré\" (8.339), are "
        "stored in `education_school_population.csv` (sgt1939 rows) and used for checks here.",
        "Failed check: the girls' row of the École primaire supérieure de Sousse (technical section) prints "
        "TOTAUX GÉNÉRAUX 127 for 177 (the cells, the girls' TOTAUX and the branch totals need 177).",
    ],
    "education_libraries": [
        "Table \"Bibliothèques\": loans (`loans`, Prêts) and volumes lent (`volumes_lent`, Volumes prêtés) for the "
        "public library of Tunis, the circulating library, the popular library of Tunis and the popular libraries "
        "of the interior, two years per edition. The popular libraries are numbered \"3°\" twice as printed. "
        "sgt1939 footnote: loans suspended from 15 September to 10 October (1939).",
    ],
    "education_arabic_courses": [
        "École supérieure de langue et de littérature arabes: auditors of the elementary spoken and written Arabic "
        "courses (1st and 2nd year) and the higher written course, two years per edition. The printing alternates "
        "between one figure bracketed across both years of a course (`elementary_spoken`, `elementary_written`) "
        "and one figure per year (`*_y1`, `*_y2`); the codes keep the printed split. Because the split differs "
        "between printings of the same year, every cell of a year is taken from the latest edition printing it "
        "(rule 4 applied per year). sgt1936, 1935, written course 1st year: first digit broken; 30 entered because "
        "30 + 30 = 60, the bracketed figure printed by sgt1935 (`derived_from_totals`).",
    ],
    "education_music_school": [
        "École de musique: pupils enrolled (`enrolled`) and pupils in each class, by nationality (Français, "
        "Musulmans, Israélites, Italiens, Maltais, Divers). Not split by sex (`sex` = `total`). A pupil can follow "
        "several classes, so the classes do not add up to the enrolment. sgt1939 prints no enrolment line but a "
        "column-total line (57), which equals the sum of its classes (check only). sgt1929 cello class: the cells "
        "(3 + 2 + 1) give 6 against a printed TOTAUX 16 (kept).",
    ],
    "education_commerce_school": [
        "École de commerce (Tunis), sgt1936 and sgt1939: pupils by course, sex and nationality. sgt1939: the "
        "secretarial course prints TOTAUX GÉNÉRAUX 13 against 18 girls, and the \"Section des bacheliers\" prints 2 "
        "Israélites in the boys' block with a boys' TOTAUX of » (TOTAUX GÉNÉRAUX 4 = the 4 girls); the cells "
        "concerned are flagged `total_mismatch`.",
    ],
    "education_primary_totals": [
        "\"Total général de l'enseignement primaire\" (sgt1922–sgt1936), printed at the end of the school lists: "
        "1° public primary schools (`public_primary`), 2° private schools (`private`), 3° primary classes of the "
        "establishments with civil personality (`estab_primary_classes`), by sex and nationality, and the totals of "
        "the previous year (`pupils_total_previous_year`, `year` = previous year). Footnote (1): these numbers are "
        "already counted in the statistics of the Collège Sadiki (petit collège), the écoles normales (écoles "
        "d'application) and the Petit Lycée Jules-Ferry; they are given only to obtain the total of pupils "
        "receiving primary education; in the school-population table they are counted only with the "
        "establishments with civil personality. The `public_primary` and `private` rows are the same cells as the "
        "corresponding rows of `education_school_population.csv` in sgt1922–sgt1930 (do not add the two files).",
        "**Cross-check with the population table**: the `public_primary` and `private` lines were compared cell "
        "by cell with the \"Écoles primaires publiques\" and \"Écoles privées\" rows of the same edition's "
        "comparative school-population table. They agree in sgt1922–sgt1929. In sgt1930 the public boys' Français "
        "cell is printed 6.667 here and 6.676 in the population table (6.676 closes this table's row and column "
        "totals: a transposition misprint, flagged `total_mismatch`). In sgt1935 and sgt1936 the private-school "
        "lines differ throughout (sgt1935: 3.595 boys / 3.588 girls here against 4.128 / 3.953; sgt1936: 3.665 / "
        "3.955 against 4.253 / 4.343): the population table's private schools are wider than the primary private "
        "schools of this line (the comparative table's private pupils, 8.081 and 8.596, agree with the population "
        "table). Both printings are kept, each in its own file. For sgt1939 see "
        "`education_first_degree_sgt1939.csv`.",
        "Cells hidden in the binding and solved from the printed totals (`derived_from_totals`): sgt1935 boys' "
        "Musulmans column (35.079, 91, 802; total 35.972 closes), sgt1936 public boys' Français (9.819, confirmed "
        "by the population table).",
    ],
    "education_first_degree_sgt1939": [
        "sgt1939 (views 72–73): \"Total général de la population scolaire du premier degré\": primary classes of "
        "the second-degree establishments (`estab_primary_classes`) and first-degree establishments "
        "(`first_degree_establishments`), by sex and nationality, with the previous year's totals "
        "(`pupils_total_previous_year`). The boys' Musulmans and Israélites columns are printed in the binding: "
        "Israélites 387 of row 1 is legible; 37.058 and 3.342 of row 2 are taken from the same row of the "
        "population table (views 74–75), which closes the row total 53.093 (`derived_from_totals`). Row 1, boys, "
        "Français is printed 1.471, against 1.171 in the population table and the secondary-establishments table; "
        "the row total (2.634) and the column total (10.372) need 1.171 (`total_mismatch`, printed value kept). "
        "Both rows are the same cells as the sgt1939 rows of `education_school_population.csv`.",
    ],
    "education_vocational": [
        "\"Enseignement professionnel de la population indigène\" (from sgt1935 \"Enseignement professionnel "
        "élémentaire\"): number of apprentices by school. In sgt1922–sgt1929 the schools of Tunis are listed one "
        "by one under a bracket total (checked, not stored); in sgt1930 only the bracket total is printed (one row, "
        "\"Tunis (ensemble des écoles, non détaillé)\"); from sgt1935 the list is by school or section. \"A reporter\""
        " / \"Report\" and Total lines are checks only. A school printed » is stored as 0 (sgt1939: two schools "
        "closed since the beginning of the war).",
        "Failed check: sgt1924 Tunis schools sum to 233 against the printed bracket 224; the carried total (383) and "
        "the general total (631) follow 224 (all cells re-read). sgt1929 Tébourba is blank on the page; 3 closes "
        "the printed total 631 (`derived_from_totals`).",
    ],
    "education_canteens": [
        "\"Cantines scolaires\": portions served, free and paying, two years per edition (the Totaux line is a "
        "check). sgt1939 footnote: the 1938 free portions (295.327) are a rectified figure.",
    ],
    "education_school_population": [
        "Comparative statistics a) \"Population scolaire au 31 décembre\": pupils by type of school, sex and "
        "nationality, with the previous year's total per type (`pupils_total_previous_year`, `year` = previous "
        "year). The \"garçons et filles\" columns, the TOTAUX, the rows \"Total de l'enseignement public\" and "
        "\"Total général\" are checks only; the \"Total général\" by sex and nationality, and the comparison lines "
        "with the three previous years, form `education_school_population_series.csv`.",
        "School types (`school_type`): sgt1922–sgt1936 `public_primary` (Écoles primaires publiques), "
        "`civil_personality` (Établissements à personnalité civile, including their primary classes), `private` "
        "(Écoles privées). sgt1939 (new layout): `secondary_courses` (a) cours secondaires, primaires supérieurs ou "
        "techniques of the second-degree establishments), `estab_primary_classes` (b) their elementary classes), "
        "`first_degree_establishments`, `private`.",
        "sgt1935 and sgt1939 print the boys' TOTAUX column in the binding; it was entered as TOTAUX GÉNÉRAUX "
        "minus the girls' TOTAUX (agreeing with every visible digit); those checks are therefore not independent. "
        "Failed checks are misprints of printed totals, kept: e.g. sgt1923 Total général, garçons, Israélites "
        "printed 5.580 (3.397 + 2.103 = 5.500), sgt1929 several \"garçons et filles\" cells (civil personality, "
        "Israélites 1.494 for 764) and sgt1939 Total général, garçons, Français 14.349 for 14.394.",
    ],
    "education_school_population_series": [
        "Yearly series of the \"Total général des établissements scolaires français publics et privés\" by sex and "
        "nationality: each edition prints its own year (row Total général of the population table) and the same "
        "totals for the three previous years (\"Comparaison avec les trois années précédentes\"). Rule 4: each year "
        "from the latest edition. No edition prints 1931 (the series of yearbooks has no 1931–1934 editions; "
        "sgt1935 compares with 1932–1934). sgt1922 compares with 1919–1921.",
        "Differences between printings are listed below; in each case the latest printing is consistent with the "
        "row totals printed with it (sgt1923 1923 Israélites boys 5.580 is a misprint of 5.500; sgt1929 1929 "
        "Diverses girls 200, sgt1930 201 closes the girls' total 23.009; sgt1935 1933 Italiennes 5.149, sgt1936 "
        "5.119 closes the 1933 row 27.914).",
    ],
    "education_quinquennial_pupils": [
        "Comparative statistics b) \"Statistique quinquennale\": pupils at 31 December, boys and girls, public and "
        "private education, every fifth year from 1885 plus the edition year (and 1934 in sgt1935). The totals "
        "per sex and the total général are checks only. sgt1935 starts at 1890; sgt1936 and sgt1939 again at "
        "1885. Public pupils exclude the auditors of adult courses (sgt1939 footnote).",
        "**1905 boys, public**: sgt1922–sgt1926 print 10.799, sgt1927–sgt1939 10.999; 10.799 + 2.159 = 12.958, the "
        "boys' total printed by all editions: kept from sgt1926 (`reprint_corrected`). **1925 girls, private**: "
        "sgt1939 prints 3.416, every earlier printing 3.419 (16.756 + 3.419 = 20.175): kept from sgt1936 "
        "(`reprint_corrected`). **1920 total général**: every edition prints 42.497 although 26.678 + 17.333 = "
        "44.011 (the population tables give 44.011 for 1920; 42.497 is their 1919 total); the four cells are "
        "consistent with the population table and are kept. **1926 boys, private**: sgt1926 (the only printing) "
        "has 5.199; 38.853 + 3.199 = 42.052 and the population table gives 3.199 (`total_mismatch`, printed "
        "value kept). sgt1930 prints the 1930 boys' total 51.545 for 52.545 (a total, not stored).",
    ],
    "education_comparative": [
        "Comparative statistics c) \"Tableau comparatif\" (two years per edition). Items: `n_public_establishments`"
        " (Nombre total d'établissements scolaires publics; footnote (1): including the school of music and the "
        "Higher School of Arabic, from sgt1939 also the school of commerce), `n_public_primary_schools`, "
        "`n_public_primary_classes`, `n_private_schools`; `pupils_public` by `sex` and `nationality` (public "
        "education, excluding adult auditors; equal to the population table's \"Total de l'enseignement public\"), "
        "`adult_auditors` (Auditeurs des cours d'adultes), `private_pupils`. The printed totals (Nombre total des "
        "élèves de l'enseignement public, Comparaison par sexes, Total général) are checks only. sgt1939 changes "
        "the establishment items: `n_second_degree_establishments`, `n_first_degree_establishments` (footnote (a): "
        "of which 11 closed because of the war), `n_public_establishments` (b: of which 61 closed), "
        "`n_first_degree_classes`, and no count of private schools; its \"Nombre total des élèves de "
        "l'enseignement public\" excludes the adult auditors and its Total général includes them, the opposite of "
        "the earlier editions for the public total (footnote (3): credits for adult courses reduced).",
        "Failed checks: sgt1922, 1921 column: the boys and girls by nationality sum to 26.020 and 14.774 against "
        "the printed comparaison par sexes 27.951 and 14.816; the cells plus the 1.973 adult auditors give the "
        "printed public total 42.767, which also equals 27.951 + 14.816: the comparaison par sexes line of 1921 "
        "includes the auditors (cells kept as printed). sgt1936, 1935 column: public pupils printed 83.914 (cells "
        "give 83.944, as sgt1935 printed), and 487 establishments / 477 primary schools against 490 / 480 in "
        "sgt1935 (rule 4 keeps sgt1936). 1929: sgt1929 prints 451 establishments and 461 primary schools, sgt1930 "
        "461 and 451; establishments exceed primary schools by 10 in every other year, so sgt1930 (kept) is "
        "consistent. 1929 Musulmanes 3.173 (both printings) against 3.179 in the population table's total public "
        "row, whose own rows sum to 3.173.",
    ],
})


def write_csv(name, rows, dims):
    cols = COMMON + dims + ["value", "flag"]
    OUT.mkdir(exist_ok=True)
    with (OUT / f"{name}.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in cols})


def fmt_views(rows):
    by = defaultdict(set)
    for r in rows:
        by[r["census"]].add((r["source_page"], r["gallica_view"]))
    return "; ".join(f"{e} (`{EDITIONS[e]}`): " + ", ".join(f"p. {p}, f{v}" for p, v in sorted(by[e]))
                     for e in ORDER if e in by)


def write_notes(name, rows, info):
    rule, dims, tfr, ten = OUTPUTS[name]
    eds = [e for e in ORDER if any(r["census"] == e for r in rows)]
    L = [f"# {tfr}", "", f"*{ten}.*", "",
         "Source: *Statistique générale de la Tunisie*, chapter \"Instruction publique et beaux-arts\" (VII; VI in "
         "sgt1936 and sgt1939), editions " + ", ".join(eds) + ". Source gallica.bnf.fr / Ministère des Affaires "
         "étrangères.", "", f"Pages and views used: {fmt_views(rows)}.", "",
         "Transcriptions: `../transcribed/education_sum_<edition>.txt`; rebuild with "
         "`python3 data-raw/yearbook_health_education/extract_education_summary.py build`. Per-check output: "
         "`education_summary_validation.json`.", ""]
    years = sorted({r["year"] for r in rows})
    L += [f"Rows: {len(rows)}. Years: {years[0]}–{years[-1]}"
          + (f" ({len(years)} years: {', '.join(map(str, years))})" if len(years) != years[-1] - years[0] + 1 else "")
          + ".", ""]
    if rule == 4:
        L += ["Printed for overlapping year windows: every cell of a year is taken from the **latest** edition that "
              "prints that year (SPEC_ADDENDUM rule 4; `census` = that edition) and every other printing of the same "
              "cell is compared below. Duplicate printings are not stored.", "",
              "Years printed by each edition: " + "; ".join(
                  f"{e} {', '.join(map(str, ys))}" for e, ys in info["printed_years"].items()) + ".", ""]
    else:
        L += ["Printed once per edition, for the edition's own year; all editions are kept (SPEC_ADDENDUM rule 5).", ""]
    L += ["## Columns", ""]
    for c in COMMON + dims + ["value", "flag"]:
        L.append(f"- `{c}`: {COLDOC.get(c, '')}")
    L += ["", "Printed totals (TOTAUX, Totaux généraux, subtotals, A reporter) are not stored unless stated; they were "
          "used for validation.", ""]
    for para in COMMENT[name]:
        L += [para, ""]
    fn = NOTES.get(name)
    if fn:
        L += ["## Footnotes printed under the table", ""]
        seen = OrderedDict()
        for e, n in fn:
            seen.setdefault(n, []).append(e)
        for n, es in seen.items():
            L.append(f"- {n} ({', '.join(es)})")
        L.append("")
    n, fail = info["checks"]
    L += ["## Validation", "", f"- Checks against printed totals: {n}; passed: {n - len(fail)}; failed: {len(fail)}."]
    if fail:
        L += ["", "Failed checks (every cell involved was re-read on a native-resolution crop; the printed figures are as "
              "transcribed; see the commentary above):", ""] + [f"  - {x}" for x in fail]
    if rule == 4:
        L += ["", f"- Overlapping printings: {info['compared']} cell comparisons between editions; "
              f"{len(info['diffs'])} differences."]
        if info["diffs"]:
            kept = {(r["year"], r["_key"]): (r["census"], r["value"], r["flag"]) for r in rows}
            L += ["", "| year | cell | edition | printed | latest edition | printed | stored (edition, flag) |",
                  "|---|---|---|---|---|---|---|"]
            for y, k, e, a, e2, b in info["diffs"]:
                st = kept.get((y, k))
                st = f"{st[1]} ({st[0]}{', ' + st[2] if st[2] else ''})" if st else "not stored"
                L.append(f"| {y} | {'/'.join(k)} | {e} | {a} | {e2} | {b} | {st} |")
        if info["unmatched"]:
            L += ["", f"- Cells printed by an earlier edition but laid out differently in the edition the year is "
                  f"taken from (not compared cell by cell): " + "; ".join(
                      f"{y} {'/'.join(k)} = {v} ({e}; year from {e2})" for y, k, e, v, e2 in info["unmatched"]) + "."]
    fl = defaultdict(int)
    for r in rows:
        if r["flag"]:
            fl[r["flag"]] += 1
    L += ["", "- Flagged cells: " + (", ".join(f"{k}: {v}" for k, v in sorted(fl.items())) if fl else "none") + "."]
    flagged = [r for r in rows if r["flag"] and r["flag"] != "not_applicable"]
    if flagged:
        L += [""] + [f"  - {r['census']} {r['year']} " + " / ".join(str(r[d]) for d in dims if r.get(d) not in (None, "")
                                                                    and not d.endswith("_fr"))
                     + f" = {r['value']} ({r['flag']})" for r in flagged]
    x = XCHK.n.get(name)
    if x:
        L += ["", "## Cross-checks with other tables of the chapter", "",
              f"- {x} comparisons; equal: {x - len(XCHK.fail[name])}; different: {len(XCHK.fail[name])}."]
        L += [f"  - {d}" for d in XCHK.fail[name]]
    (OUT / f"{name}.md").write_text("\n".join(L) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- cross-checks


def cross_checks():
    X = XCHK
    for ed in ORDER:
        y = YEAR[ed]
        c = COMPAR.get(ed, {})
        pop = POP.get(ed, {})
        t = TOTALS.get(ed)
        tg = c.get("TOTAL_GENERAL", {}).get(y)
        X.eq("education_total_pupils", f"{ed} total page vs tableau comparatif, total général {y}", tg, t)
        if "TOTAL_GENERAL" in pop:
            X.eq("education_total_pupils", f"{ed} total page vs population table total général + adult auditors",
                 pop["TOTAL_GENERAL"][3] + c["adult_auditors"][y], t)
        if "TOTAL_PUBLIC" in pop:
            b, g = pop["TOTAL_PUBLIC"][0], pop["TOTAL_PUBLIC"][1]
            for k, (nat, *_r) in enumerate(NATS):
                for sx, vals in (("male", b), ("female", g)):
                    X.eq("education_comparative", f"{ed} pupils {nat} {sx} {y} vs population table, total public",
                         c.get(f"pupils {nat} {sx}", {}).get(y), vals[k])
            X.eq("education_comparative", f"{ed} private pupils {y} vs population table, écoles privées",
                 c.get("private_pupils", {}).get(y), pop["private"][3])
        # primary-education total vs population table (public primary and private lines)
        pr = PRIM.get(ed, {})
        for code in ("public_primary", "private", "estab_primary_classes", "first_degree_establishments"):
            if code in pr and code in pop:
                for bi, sx in ((0, "boys"), (1, "girls")):
                    for k in range(7):
                        X.eq("education_primary_totals" if ed != "sgt1939" else "education_first_degree_sgt1939",
                             f"{ed} '{code}' {sx} column {k}: primary/first-degree total vs population table",
                             pr[code][bi][k], pop[code][bi][k])
        # establishments' Totaux vs population row civil_personality
        if ed in EST_TOT and "civil_personality" in pop:
            b, g, gen, prev = EST_TOT[ed]
            for bi, (sx, vals) in enumerate((("boys", b), ("girls", g))):
                for k in range(7):
                    X.eq("education_civil_personality_establishments",
                         f"{ed} Totaux {sx} column {k} vs population table, établissements à personnalité civile",
                         vals[k], pop["civil_personality"][bi][k])
            X.eq("education_civil_personality_establishments", f"{ed} previous-year Totaux vs population table",
                 prev, pop["civil_personality"][4])
        # quinquennial own-year row vs population table
        q = QUINQ.get(ed, {}).get(y)
        if q and "TOTAL_PUBLIC" in pop:
            for bi, sx in ((0, "boys"), (1, "girls")):
                X.eq("education_quinquennial_pupils", f"{ed} {y} {sx} public vs population table total public",
                     q[bi][0], pop["TOTAL_PUBLIC"][bi][6])
                X.eq("education_quinquennial_pupils", f"{ed} {y} {sx} private vs population table écoles privées",
                     q[bi][1], pop["private"][bi][6])
        # comparative sexes vs quinquennial
        if q and "TOTAL_MALE" in c:
            X.eq("education_quinquennial_pupils", f"{ed} {y} boys public vs tableau comparatif garçons", q[0][0],
                 c["TOTAL_MALE"][y])
            X.eq("education_quinquennial_pupils", f"{ed} {y} girls public vs tableau comparatif filles", q[1][0],
                 c["TOTAL_FEMALE"][y])
        # previous-year columns vs previous edition
        i = ORDER.index(ed)
        if i:
            pe = ORDER[i - 1]
            if YEAR[pe] == y - 1:
                for code in pop:
                    if code in POP.get(pe, {}):
                        X.eq("education_school_population", f"{ed} '{code}' previous-year total vs {pe} total",
                             pop[code][4], POP[pe][code][3])
                for code in pr:
                    if code in PRIM.get(pe, {}):
                        X.eq("education_primary_totals", f"{ed} '{code}' previous-year total vs {pe} total",
                             pr[code][4], PRIM[pe][code][3])
                for name, prev in EST_PREV.get(ed, {}).items():
                    X.eq("education_civil_personality_establishments",
                         f"{ed} '{name}' previous-year total vs {pe} total", prev, EST_THIS.get(pe, {}).get(name))
    # sgt1939: secondary-establishment table vs population table
    pop = POP.get("sgt1939", {})
    if SEC39 and pop:
        pc = SEC39["primary_classes"]
        nt = SEC39[("net_total", "all")]
        for bi, sx in ((0, "boys"), (1, "girls")):
            for k in range(7):
                X.eq("education_secondary_establishments_sgt1939",
                     f"sgt1939 primary classes {sx} column {k} vs population table row b)", pc[bi][k],
                     pop["estab_primary_classes"][bi][k])
                X.eq("education_secondary_establishments_sgt1939",
                     f"sgt1939 total des cours de 2e degré {sx} column {k} vs population table row a)", nt[bi][k],
                     pop["secondary_courses"][bi][k])


# ---------------------------------------------------------------- build


def build(write=True):
    for ed in ORDER:
        if not (TR / f"education_sum_{ed}.txt").exists():
            raise FileNotFoundError(f"missing transcription education_sum_{ed}.txt")
        for sec in read_edition(ed):
            n = sec.name
            if n == "total":
                t_total(sec)
            elif n == "exams":
                t_exams(sec)
            elif n == "establishments":
                t_establishments(sec)
            elif n == "libraries":
                t_two_year("education_libraries", sec, [("loans", "Prêts"), ("volumes_lent", "Volumes prêtés")])
            elif n == "arabic_courses":
                t_two_year("education_arabic_courses", sec)
            elif n == "canteens":
                t_two_year("education_canteens", sec)
            elif n == "music_school":
                t_by_class(sec, "education_music_school")
            elif n == "commerce_school":
                t_by_class(sec, "education_commerce_school")
            elif n == "primary_total":
                PRIM[ed] = t_population(sec, "education_primary_totals",
                                        ("public_primary", "private", "estab_primary_classes"))
            elif n == "population":
                POP[ed] = t_population(sec, "education_school_population",
                                       ("public_primary", "civil_personality", "private", "secondary_courses",
                                        "estab_primary_classes", "first_degree_establishments"))
            elif n == "vocational":
                t_vocational(sec)
            elif n == "quinquennial":
                t_quinquennial(sec)
            elif n == "comparative":
                t_comparative(sec)
            elif n == "secondary1939":
                t_secondary_1939(sec)
            elif n == "first_degree1939":
                t_first_degree_1939(sec)
            else:
                raise ValueError(f"{ed}: unknown section {n}")
    cross_checks()
    results = {}
    for name, (rule, dims, *_r) in OUTPUTS.items():
        if name in SERIES:
            rows, compared, diffs, unmatched = SERIES[name].resolve()
            py = SERIES[name].printed_years()
        else:
            rows, compared, diffs, unmatched, py = ROWS[name], 0, [], [], {}
        results[name] = dict(rows=rows, compared=compared, diffs=diffs, unmatched=unmatched, printed_years=py,
                             checks=(CHK.n[name], CHK.fail[name]))
    if write:
        for name, (rule, dims, *_r) in OUTPUTS.items():
            write_csv(name, results[name]["rows"], dims)
            write_notes(name, results[name]["rows"], results[name])
        val = {name: dict(rows=len(r["rows"]), checks=r["checks"][0], failed=r["checks"][1],
                          cross_checks=XCHK.n.get(name, 0), cross_differences=XCHK.fail.get(name, []),
                          overlap_compared=r["compared"], overlap_diffs=[list(map(str, d)) for d in r["diffs"]])
               for name, r in results.items()}
        val["_chapters"] = {e: list(v) for e, v in CHAPTER.items()}
        (OUT / "education_summary_validation.json").write_text(json.dumps(val, indent=1, ensure_ascii=False) + "\n",
                                                               encoding="utf-8")
    return results


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd not in ("check", "build"):
        print(__doc__)
        sys.exit(1)
    res = build(write=(cmd == "build"))
    for name, r in res.items():
        print(f"{name}: {len(r['rows'])} rows; checks {r['checks'][0]}, failed {len(r['checks'][1])}; cross "
              f"{XCHK.n.get(name, 0)}, differ {len(XCHK.fail.get(name, []))}; overlap compared {r['compared']}, "
              f"diffs {len(r['diffs'])}")
    if cmd == "check":
        for name, r in res.items():
            for f_ in r["checks"][1]:
                print("  FAIL", f_)
            for f_ in XCHK.fail.get(name, []):
                print("  XCHK", f_)
            for d in r["diffs"]:
                print("  DIFF", name, d)
            for d in r["unmatched"]:
                print("  LAYOUT", name, d)
