#!/usr/bin/env python3
"""Summary tables of the public-instruction chapter ("Instruction publique et
beaux-arts") of the 12 editions of the Statistique générale de la Tunisie,
1922-1939 (see CHAPTERS.md).

  python3 extract_education_summary.py build    parse transcribed/education_sum_<edition>.txt,
                                                run every check, write csv/education_*.csv,
                                                their .md notes and csv/education_summary_validation.json
  python3 extract_education_summary.py check    same checks, print the failures, write nothing

The transcriptions in transcribed/ are the source of truth. They were typed from
the page images (data-raw/bnf_gallica/pages/, and native-resolution crops from
data-raw/yearbook_demography/hires.py for every doubtful cell); Gallica's OCR
(data-raw/colonial_census/ocr.py) was only used as a draft.

Transcription format: sections "[name key=value ...]"; data lines "field | field |
numbers"; numeric blocks are space-separated integers, "." = not printed. A
printed "»" is typed as 0. Lines starting with "note:" hold footnotes, "years:"
the years of a two-year window, "#" comments.

Not covered here: the school-by-school lists of public primary and private
schools (another extraction).
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
    ("sgt1922", ("bpt6k9105649x", 1922)), ("sgt1923", ("bpt6k9105649x", 1923)),
    ("sgt1924", ("bpt6k9105649x", 1924)), ("sgt1925", ("bpt6k9105650k", 1925)),
    ("sgt1926", ("bpt6k9105650k", 1926)), ("sgt1927", ("bpt6k91056510", 1927)),
    ("sgt1928", ("bpt6k91056510", 1928)), ("sgt1929", ("bpt6k9105652d", 1929)),
    ("sgt1930", ("bpt6k9105652d", 1930)), ("sgt1935", ("bpt6k9105653t", 1935)),
    ("sgt1936", ("bpt6k91056547", 1936)), ("sgt1939", ("bpt6k9105739w", 1939)),
])
ED_ORDER = list(EDITIONS)
# chapter view ranges, first and last view checked on the images
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

# ---------------------------------------------------------------- parsing


def nums(s):
    out = []
    for t in s.split():
        out.append(None if t == "." else int(t))
    return out


class Section:
    def __init__(self, name, attrs, ed):
        self.name, self.attrs, self.ed = name, attrs, ed
        self.lines, self.notes, self.years = [], [], None

    @property
    def views(self):
        v = self.attrs.get("view") or self.attrs.get("views")
        return [int(x) for x in v.split(",")]

    @property
    def pages(self):
        v = self.attrs.get("page") or self.attrs.get("pages")
        return [int(x) for x in v.split(",")]

    def src(self, which=0):
        """(gallica_view, source_page) of the given page of the section."""
        return self.views[min(which, len(self.views) - 1)], self.pages[min(which, len(self.pages) - 1)]


def read_edition(ed):
    p = TR / f"education_sum_{ed}.txt"
    secs, cur = [], None
    for raw in p.read_text(encoding="utf-8").splitlines():
        l = raw.strip()
        if not l or l.startswith("#"):
            continue
        m = re.match(r"^\[(\w+)\s*(.*)\]$", l)
        if m:
            attrs = dict(re.findall(r"(\w+)=(\S+)", m.group(2)))
            cur = Section(m.group(1), attrs, ed)
            secs.append(cur)
            continue
        if l.startswith("note:"):
            cur.notes.append(l[5:].strip())
        elif re.match(r"^years?:", l):
            cur.years = [int(y) for y in l.split(":", 1)[1].split()]
        elif l.startswith("flag:"):
            cur.attrs.setdefault("flags", []).append(l[5:].strip())
        else:
            if "?" in l:
                raise ValueError(f"{ed}: unresolved '?' in {l}")
            cur.lines.append([f.strip() for f in l.split("|")])
    return secs


# ---------------------------------------------------------------- checks


class Checks:
    def __init__(self):
        self.n = 0
        self.fail = []

    def eq(self, what, got, printed):
        self.n += 1
        if got != printed:
            self.fail.append(f"{what}: cells give {got}, printed {printed}")
            return False
        return True


def ssum(xs):
    return sum(x or 0 for x in xs)


CHK = defaultdict(Checks)          # table -> Checks
COMP = defaultdict(lambda: {"compared": 0, "diffs": []})   # table -> reprint comparison
FLAGS = {}                          # (table, edition, key...) -> flag  (from flag: lines)
NOTES = defaultdict(list)           # table -> [(edition, footnote)]
SOURCES = defaultdict(dict)         # table -> {edition: (views, pages)}


def cell_flags(sec):
    """'flag: key1;key2;... = flag' lines of a section -> {tuple(keys): flag}."""
    out = {}
    for f in sec.attrs.get("flags", []):
        k, v = f.rsplit("=", 1)
        out[tuple(x.strip() for x in k.split(";"))] = v.strip()
    return out


def meta(sec, which=0):
    ark, _ = EDITIONS[sec.ed]
    v, p = sec.src(which)
    return [sec.ed, ark, p, v]


def add_source(table, sec):
    SOURCES[table][sec.ed] = (sec.views, sec.pages)
    for n in sec.notes:
        NOTES[table].append((sec.ed, n))


def nat_block(vals, what, chk):
    """6 nationality cells + printed total -> check, return cells."""
    *cells, tot = vals
    assert len(cells) == 6, (what, vals)
    chk.eq(what, ssum(cells), tot)
    return cells


# ---------------------------------------------------------------- tables

ROWS = defaultdict(list)


def t_total(sec):
    year = sec.years[0] if sec.years else EDITIONS[sec.ed][1]
    add_source("education_total_pupils", sec)
    for code, label, v in sec.lines:
        ROWS["education_total_pupils"].append(meta(sec) + ["total_eleves", year, label, int(v), ""])
    return int(sec.lines[0][2])


def t_exams(sec, which):
    chk = CHK["education_exams_nationality"]
    fl = cell_flags(sec)
    add_source("education_exams_nationality", sec)
    year = EDITIONS[sec.ed][1]
    for code, label, stage, boys, girls, gen in sec.lines:
        b, g, gen = nums(boys), nums(girls), nums(gen)[0]
        what = f"{sec.ed} {code} {stage}"
        ok_b = chk.eq(what + " boys: nationalities vs TOTAUX", ssum(b[:6]), b[6])
        ok_g = chk.eq(what + " girls: nationalities vs TOTAUX", ssum(g[:6]), g[6])
        chk.eq(what + ": boys + girls vs TOTAUX GÉNÉRAUX", (b[6] or 0) + (g[6] or 0), gen)
        chk.eq(what + ": all cells vs TOTAUX GÉNÉRAUX", ssum(b[:6]) + ssum(g[:6]), gen)
        for (sx, sxfr), vals, ok in ((SEX_EXAM[0], b, ok_b), (SEX_EXAM[1], g, ok_g)):
            for k, (nat, nfr_m, nfr_f) in enumerate(NATS):
                f = fl.get((code, stage, sx, nat), "")
                if not f and not (ok_b and ok_g and ssum(b[:6]) + ssum(g[:6]) == gen):
                    f = "total_mismatch"
                ROWS["education_exams_nationality"].append(
                    meta(sec, which) + ["examens", year, code, label, stage, STAGE[stage], sx, sxfr,
                                        nat, nfr_m if sx == "male" else nfr_f, vals[k], f])


def t_establishments(sec, prev_totals):
    """Établissements à personnalité civile (sgt1922-1936)."""
    tab = "education_civil_personality_establishments"
    chk = CHK[tab]
    add_source(tab, sec)
    year = EDITIONS[sec.ed][1]
    fl = cell_flags(sec)
    data = [l for l in sec.lines if l[0] != "TOTAUX"]
    tot = [l for l in sec.lines if l[0] == "TOTAUX"]
    colsum = defaultdict(int)
    this = {}
    for loc, name, classes, boys, girls, gen, prev in data:
        b, g, gen, prev = nums(boys), nums(girls), nums(gen)[0], nums(prev)[0]
        what = f"{sec.ed} {name}"
        okb = chk.eq(what + " boys vs TOTAUX", ssum(b[:6]), b[6] or 0)
        okg = chk.eq(what + " girls vs TOTAUX", ssum(g[:6]), g[6] or 0)
        okt = chk.eq(what + " boys + girls vs TOTAUX GÉNÉRAUX", (b[6] or 0) + (g[6] or 0), gen)
        bad = not (okb and okg and okt)
        cl = nums(classes)[0] if classes not in ("", ".") else None
        r0 = meta(sec) + ["personnalite_civile", year, loc, name]
        ROWS[tab].append(r0 + ["classes", "Nombre de classes", "total", "", "total", "", cl,
                               fl.get((name, "classes"), "" if cl is not None else "not_applicable")])
        for (sx, sxfr), vals in ((SEX[0], b), (SEX[1], g)):
            for k, (nat, nm, nf) in enumerate(NATS):
                f = fl.get((name, sx, nat), "total_mismatch" if bad else "")
                ROWS[tab].append(r0 + ["pupils", "Élèves", sx, sxfr, nat, nm if sx == "male" else nf, vals[k] or 0, f])
                colsum[(sx, k)] += vals[k] or 0
            colsum[(sx, 6)] += vals[6] or 0
        colsum["classes"] += cl or 0
        colsum["gen"] += gen
        colsum["prev"] += prev or 0
        ROWS[tab].append(r0 + ["pupils_total_previous_year", "Totaux généraux de l'année précédente",
                               "total", "", "total", "", prev, ""])
        this[name] = gen
        if prev is not None:
            prev_totals[(year - 1, name)] = (prev, sec.ed)
    for _, _, classes, boys, girls, gen, prev in tot:
        b, g = nums(boys), nums(girls)
        if classes not in ("", "."):
            chk.eq(f"{sec.ed} classes column vs TOTAUX", colsum["classes"], nums(classes)[0])
        for (sx, _), vals in ((SEX[0], b), (SEX[1], g)):
            for k in range(7):
                chk.eq(f"{sec.ed} {sx} col {k} vs TOTAUX row", colsum[(sx, k)], vals[k])
        chk.eq(f"{sec.ed} TOTAUX GÉNÉRAUX column", colsum["gen"], nums(gen)[0])
        chk.eq(f"{sec.ed} previous-year column", colsum["prev"], nums(prev)[0])
    return year, this


# Rule 4 exceptions: (table, key, year) -> (edition whose printing is kept, flag). Used only where
# the latest printing is an evident misprint and an earlier printing is consistent with the printed
# totals; the notes give each case.
SERIES_OVERRIDE = {}


def window_series(tab, items, label):
    """Rule 4: items = list of (key_tuple, year, edition, value, rowmeta); keep latest edition."""
    by = defaultdict(dict)
    for key, year, ed, v, rm in items:
        by[(key, year)][ed] = (v, rm)
    out = []
    for (key, year), d in by.items():
        eds = [e for e in ED_ORDER if e in d]
        latest = eds[-1]
        ov = SERIES_OVERRIDE.get((tab, key, year))
        if ov:
            latest = ov[0]
            SERIES_FLAGS[(tab, key, year)] = ov[1]
        for e in eds[:-1]:
            COMP[tab]["compared"] += 1
            if d[e][0] != d[latest][0]:
                COMP[tab]["diffs"].append(f"{label(key)} {year}: {e} prints {d[e][0]}, {latest} prints {d[latest][0]}")
        out.append((key, year, latest, d[latest][0], d[latest][1], {e: d[e][0] for e in eds}))
    return out


SERIES = defaultdict(list)


def t_two_year(tab, sec, groups=None):
    """Tables printed for a two-year window: libraries, arabic courses, canteens, comparative."""
    add_source(tab, sec)
    ys = sec.years
    for line in sec.lines:
        code, label, *blocks = line
        if groups:
            for (g, gfr), blk in zip(groups, blocks):
                for y, v in zip(ys, nums(blk)):
                    SERIES[tab].append(((code, label, g, gfr), y, sec.ed, v, meta(sec)))
        else:
            for y, v in zip(ys, nums(blocks[0])):
                SERIES[tab].append(((code, label), y, sec.ed, v, meta(sec)))


def t_music(sec, tab):
    chk = CHK[tab]
    add_source(tab, sec)
    year = EDITIONS[sec.ed][1]
    for line in sec.lines:
        code, label, *blocks = line
        if len(blocks) == 1:
            v = nums(blocks[0])
            cells = nat_block(v, f"{sec.ed} {code}", chk)
            for k, (nat, nm, _) in enumerate(NATS):
                ROWS[tab].append(meta(sec) + [tab.replace("education_", ""), year, code, label, "total", "",
                                              nat, nm, cells[k], ""])
        else:   # boys | girls | total (école de commerce)
            b, g, t = nums(blocks[0]), nums(blocks[1]), nums(blocks[2])[0]
            okb = chk.eq(f"{sec.ed} {code} boys", ssum(b[:6]), b[6])
            okg = chk.eq(f"{sec.ed} {code} girls", ssum(g[:6]), g[6])
            chk.eq(f"{sec.ed} {code} total", b[6] + g[6], t)
            for (sx, sxfr), vals in ((SEX[0], b), (SEX[1], g)):
                for k, (nat, nm, nf) in enumerate(NATS):
                    ROWS[tab].append(meta(sec) + [tab.replace("education_", ""), year, code, label, sx, sxfr,
                                                  nat, nm if sx == "male" else nf, vals[k], ""])


POP_TYPES = {"public_primary": "public_primary", "civil_personality": "civil_personality",
             "private": "private", "estab_primary_classes": "civil_personality_primary_classes"}


def t_bysex_table(tab, sec, both_cols, result):
    """primary_total (boys7 | girls7 | gen | prev) and population (boys7 | girls7 | both6 | gen | prev)."""
    chk = CHK[tab]
    add_source(tab, sec)
    year = EDITIONS[sec.ed][1]
    fl = cell_flags(sec)
    rows = OrderedDict()
    compare = OrderedDict()
    for line in sec.lines:
        if line[0].startswith("compare"):
            compare[int(line[0].split()[1])] = [nums(x) for x in line[1:]]
        else:
            rows[line[0]] = (line[1], [nums(x) for x in line[2:]])
    for code, (label, blocks) in rows.items():
        b, g = blocks[0], blocks[1]
        gen = blocks[-2][0]
        what = f"{sec.ed} {code}"
        okb = chk.eq(what + " boys vs TOTAUX", ssum(b[:6]), b[6])
        okg = chk.eq(what + " girls vs TOTAUX", ssum(g[:6]), g[6])
        chk.eq(what + " boys + girls vs TOTAUX GÉNÉRAUX", b[6] + g[6], gen)
        if both_cols:
            both = blocks[2]
            for k in range(6):
                chk.eq(what + f" {NATS[k][0]}: boys + girls vs garçons et filles", b[k] + g[k], both[k])
            chk.eq(what + " garçons et filles columns vs TOTAUX GÉNÉRAUX", ssum(both), gen)
        result[code] = (b, g, gen, blocks[-1][0])
        if code.isupper():
            continue
        r0 = meta(sec) + [tab.replace("education_", ""), year, POP_TYPES.get(code, code), label]
        for (sx, sxfr), vals, ok in ((SEX[0], b, okb), (SEX[1], g, okg)):
            for k, (nat, nm, nf) in enumerate(NATS):
                f = fl.get((code, sx, nat), "" if ok else "total_mismatch")
                ROWS[tab].append(r0 + ["pupils", sx, sxfr, nat, nm if sx == "male" else nf, vals[k], f])
        ROWS[tab].append(r0 + ["pupils_total_previous_year", "total", "", "total", "", blocks[-1][0], ""])
    # column totals
    data = [c for c in rows if not c.isupper()]
    def colcheck(total_code, members):
        if total_code not in rows:
            return
        tb = rows[total_code][1]
        for bi in range(len(tb)):
            for k in range(len(tb[bi])):
                if tb[bi][k] is None:
                    continue
                chk.eq(f"{sec.ed} {total_code} block {bi} col {k}",
                       ssum(rows[m][1][bi][k] for m in members), tb[bi][k])
    if tab == "education_primary_totals":
        colcheck("TOTAUX", data)
    else:
        colcheck("TOTAL_PUBLIC", [c for c in data if c != "private"])
        colcheck("TOTAL_GENERAL", ["TOTAL_PUBLIC", "private"] if "TOTAL_PUBLIC" in rows else data)
        for y, blocks in compare.items():
            b, g = blocks[0], blocks[1]
            chk.eq(f"{sec.ed} comparison {y} boys", ssum(b[:6]), b[6])
            chk.eq(f"{sec.ed} comparison {y} girls", ssum(g[:6]), g[6])
            chk.eq(f"{sec.ed} comparison {y} boys + girls", b[6] + g[6], blocks[-1][0])
            if both_cols:
                for k in range(6):
                    chk.eq(f"{sec.ed} comparison {y} {NATS[k][0]} both", b[k] + g[k], blocks[2][k])
            for (sx, sxfr), vals in ((SEX[0], b), (SEX[1], g)):
                for k, (nat, nm, nf) in enumerate(NATS):
                    key = (sx, sxfr, nat, nm if sx == "male" else nf)
                    SERIES["education_school_population_series"].append((key, y, sec.ed, vals[k], meta(sec)))
                    f = fl.get((f"compare {y}", sx, nat))
                    if f:
                        DERIVED[("education_school_population_series", sec.ed, key, y)] = f
        if "TOTAL_GENERAL" in rows:
            b, g = rows["TOTAL_GENERAL"][1][0], rows["TOTAL_GENERAL"][1][1]
            for (sx, sxfr), vals in ((SEX[0], b), (SEX[1], g)):
                for k, (nat, nm, nf) in enumerate(NATS):
                    key = (sx, sxfr, nat, nm if sx == "male" else nf)
                    SERIES["education_school_population_series"].append((key, year, sec.ed, vals[k], meta(sec)))
                    f = fl.get(("TOTAL_GENERAL", sx, nat))
                    if f:
                        DERIVED[("education_school_population_series", sec.ed, key, year)] = f
    return compare


def t_vocational(sec):
    tab = "education_vocational"
    chk = CHK[tab]
    add_source(tab, sec)
    year = EDITIONS[sec.ed][1]
    run, group = 0, []
    for loc, label, v in sec.lines:
        v = int(v)
        if loc == "SUBTOTAL":
            if not chk.eq(f"{sec.ed} subtotal {label}", ssum(r[-2] for r in group), v):
                for r in group:
                    r[-1] = "total_mismatch"
            run += v - ssum(r[-2] for r in group)   # running total follows the printed subtotal
            group = []
            continue
        if loc in ("REPORT", "TOTAL"):
            chk.eq(f"{sec.ed} {label}", run, v)
            continue
        if loc.isupper() and loc not in ("TUNIS",):
            raise ValueError(loc)
        run += v
        ROWS[tab].append(meta(sec) + ["apprentissage", year, "Tunis" if loc == "TUNIS" else loc, label, v, ""])
        if loc == "TUNIS":
            group.append(ROWS[tab][-1])


def t_quinquennial(sec):
    tab = "education_quinquennial_pupils"
    chk = CHK[tab]
    add_source(tab, sec)
    fl = cell_flags(sec)
    for y, boys, girls, tot in sec.lines:
        y = int(y)
        b, g, t = nums(boys), nums(girls), nums(tot)[0]
        okb = chk.eq(f"{sec.ed} {y} boys public + private vs total", b[0] + b[1], b[2])
        okg = chk.eq(f"{sec.ed} {y} girls public + private vs total", g[0] + g[1], g[2])
        chk.eq(f"{sec.ed} {y} boys + girls vs total général", b[2] + g[2], t)
        for (sx, sxfr), vals in ((SEX[0], b), (SEX[1], g)):
            for k, (sec_, secfr) in enumerate((("public", "Enseignement public"), ("private", "Enseignement privé"))):
                key = (sx, sxfr, sec_, secfr)
                SERIES[tab].append((key, y, sec.ed, vals[k], meta(sec)))
                f = fl.get((str(y), sx, sec_))
                if f:
                    DERIVED[(tab, sec.ed, key, y)] = f
        SERIES[tab + "#totals"].append((("total",), y, sec.ed, t, meta(sec)))


def t_comparative(sec):
    tab = "education_comparative"
    chk = CHK[tab]
    add_source(tab, sec)
    ys = sec.years
    d = {l[0]: nums(l[2]) for l in sec.lines}
    for i, y in enumerate(ys):
        def g(c):
            return d[c][i] if c in d and d[c][i] is not None else 0
        pm = [d[c][i] for c in d if c.startswith("pupils") and c.endswith(" male")]
        pf = [d[c][i] for c in d if c.startswith("pupils") and c.endswith(" female")]
        if "TOTAL_MALE" in d:
            chk.eq(f"{sec.ed} {y} boys by nationality vs garçons", ssum(pm), g("TOTAL_MALE"))
            chk.eq(f"{sec.ed} {y} girls by nationality vs filles", ssum(pf), g("TOTAL_FEMALE"))
        if "TOTAL_PUBLIC" in d:
            chk.eq(f"{sec.ed} {y} pupils + adult auditors vs total public", ssum(pm) + ssum(pf) + g("adult_auditors"),
                   g("TOTAL_PUBLIC"))
        if "TOTAL_GENERAL" in d:
            chk.eq(f"{sec.ed} {y} public + private vs total général", g("TOTAL_PUBLIC") + g("private_pupils"),
                   g("TOTAL_GENERAL"))
    for code, label, vals in sec.lines:
        if code.isupper():
            continue
        for y, v in zip(ys, nums(vals)):
            SERIES[tab].append(((code, label), y, sec.ed, v, meta(sec)))
    for code, label, vals in sec.lines:
        if code.isupper():
            for y, v in zip(ys, nums(vals)):
                SERIES[tab + "#totals"].append(((code,), y, sec.ed, v, meta(sec)))
    return {c: dict(zip(ys, nums(l))) for c, _, l in sec.lines}


def t_budget(sec):
    tab = "education_budget"
    add_source(tab, sec)
    cols = sec.attrs["cols"].split(",")
    for line in sec.lines:
        y = int(line[0])
        for c, v in zip(cols, line[1:]):
            v = v.strip()
            SERIES[tab].append(((c,), y, sec.ed, None if v == "." else v, meta(sec)))


def t_secondary_1939(sec, which):
    """sgt1939: établissements d'enseignement secondaire, primaire supérieur ou technique."""
    tab = "education_secondary_establishments_sgt1939"
    chk = CHK[tab]
    add_source(tab, sec)
    year = EDITIONS[sec.ed][1]
    for line in sec.lines:
        kind, branch, name, boys, girls, gen = line
        b, g, gen = nums(boys), nums(girls), nums(gen)[0]
        what = f"{sec.ed} {branch} {name}"
        okb = chk.eq(what + " boys", ssum(b[:6]), b[6] or 0)
        okg = chk.eq(what + " girls", ssum(g[:6]), g[6] or 0)
        chk.eq(what + " boys + girls", (b[6] or 0) + (g[6] or 0), gen)
        SEC1939.append((kind, branch, name, b, g, gen, meta(sec, which)))
        if kind != "school":
            continue
        for (sx, sxfr), vals in ((SEX[0], b), (SEX[1], g)):
            for k, (nat, nm, nf) in enumerate(NATS):
                v = vals[k]
                ROWS[tab].append(meta(sec, which) + ["second_degre", year, branch, name, sx, sxfr, nat,
                                                     nm if sx == "male" else nf, v if v is not None else "",
                                                     "" if v is not None else "not_applicable"])


SEC1939 = []


def check_sec1939():
    chk = CHK["education_secondary_establishments_sgt1939"]
    run = defaultdict(lambda: [[0] * 7, [0] * 7, 0])
    for kind, branch, name, b, g, gen, _ in SEC1939:
        if kind == "school":
            for key in (branch, "ALL"):
                for k in range(7):
                    run[key][0][k] += b[k] or 0
                    run[key][1][k] += g[k] or 0
                run[key][2] += gen
        elif kind in ("branch_total", "grand_total"):
            key = branch if kind == "branch_total" else "ALL"
            for k in range(7):
                if b[k] is not None:
                    chk.eq(f"sgt1939 {name} boys col {k}", run[key][0][k], b[k])
                if g[k] is not None:
                    chk.eq(f"sgt1939 {name} girls col {k}", run[key][1][k], g[k])
            chk.eq(f"sgt1939 {name} total", run[key][2], gen)


def t_first_degree_1939(sec):
    tab = "education_first_degree_sgt1939"
    chk = CHK[tab]
    add_source(tab, sec)
    year = EDITIONS[sec.ed][1]
    rows = OrderedDict((l[0], (l[1], [nums(x) for x in l[2:]])) for l in sec.lines)
    for code, (label, blocks) in rows.items():
        b, g, gen = blocks[0], blocks[1], blocks[2][0]
        chk.eq(f"sgt1939 {code} boys", ssum(b[:6]), b[6])
        chk.eq(f"sgt1939 {code} girls", ssum(g[:6]), g[6])
        chk.eq(f"sgt1939 {code} boys + girls", b[6] + g[6], gen)
        if code.isupper():
            continue
        for (sx, sxfr), vals in ((SEX[0], b), (SEX[1], g)):
            for k, (nat, nm, nf) in enumerate(NATS):
                ROWS[tab].append(meta(sec) + ["premier_degre", year, code, label, sx, sxfr, nat,
                                              nm if sx == "male" else nf, vals[k], ""])
        if len(blocks) > 3:
            ROWS[tab].append(meta(sec) + ["premier_degre", year, code, label, "total", "", "total", "",
                                          blocks[3][0], ""])
    data = [c for c in rows if not c.isupper()]
    if "TOTAL" in rows:
        tb = rows["TOTAL"][1]
        for bi in range(3):
            for k in range(len(tb[bi])):
                chk.eq(f"sgt1939 first degree TOTAL block {bi} col {k}", ssum(rows[c][1][bi][k] for c in data), tb[bi][k])
    return rows


# ---------------------------------------------------------------- build


def build(write=True):
    totals, comparatives, populations, primaries = {}, {}, {}, {}
    prev_totals, est_this = {}, {}
    for ed in ED_ORDER:
        p = TR / f"education_sum_{ed}.txt"
        if not p.exists():
            print("missing transcription", p.name)
            continue
        exam_i = 0
        for sec in read_edition(ed):
            n = sec.name
            if n == "total":
                totals[ed] = t_total(sec)
            elif n == "exams":
                t_exams(sec, 0)
            elif n == "establishments":
                y, this = t_establishments(sec, prev_totals)
                for k, v in this.items():
                    est_this[(y, k)] = (v, ed)
            elif n == "libraries":
                t_two_year("education_libraries", sec, [("loans", "Prêts"), ("volumes_lent", "Volumes prêtés")])
            elif n == "arabic_courses":
                t_two_year("education_arabic_courses", sec)
            elif n == "canteens":
                t_two_year("education_canteens", sec)
            elif n == "music_school":
                t_music(sec, "education_music_school")
            elif n == "commerce_school":
                t_music(sec, "education_commerce_school")
            elif n == "primary_total":
                primaries[ed] = {}
                t_bysex_table("education_primary_totals", sec, False, primaries[ed])
            elif n == "population":
                populations[ed] = {}
                t_bysex_table("education_school_population", sec, True, populations[ed])
            elif n == "vocational":
                t_vocational(sec)
            elif n == "quinquennial":
                t_quinquennial(sec)
            elif n == "comparative":
                comparatives[ed] = t_comparative(sec)
            elif n == "budget":
                t_budget(sec)
            elif n == "secondary1939":
                t_secondary_1939(sec, 0)
            elif n == "first_degree1939":
                primaries[ed] = t_first_degree_1939(sec)
            else:
                raise ValueError(f"{ed}: unknown section {n}")
    check_sec1939()
    cross = Checks()
    # total pupils vs comparative table and population table
    for ed, tot in totals.items():
        y = EDITIONS[ed][1]
        c = comparatives.get(ed, {})
        if "TOTAL_GENERAL" in c:
            cross.eq(f"{ed} total pupils page vs tableau comparatif total général {y}", c["TOTAL_GENERAL"][y], tot)
        if ed in populations and "TOTAL_GENERAL" in populations[ed] and "adult_auditors" in c:
            cross.eq(f"{ed} population total général + adult auditors vs total pupils",
                     populations[ed]["TOTAL_GENERAL"][2] + c["adult_auditors"][y], tot)
    # comparative pupils (public, by nationality and sex) vs population table TOTAL_PUBLIC
    for ed, c in comparatives.items():
        y = EDITIONS[ed][1]
        pop = populations.get(ed, {})
        if "TOTAL_PUBLIC" in pop:
            b, g = pop["TOTAL_PUBLIC"][0], pop["TOTAL_PUBLIC"][1]
            for k, (nat, *_r) in enumerate(NATS):
                for sx, vals in (("male", b), ("female", g)):
                    key = f"pupils {nat} {sx}"
                    if key in c:
                        cross.eq(f"{ed} tableau comparatif {key} {y} vs population total public", c[key][y], vals[k])
        if "private" in pop and "private_pupils" in c:
            cross.eq(f"{ed} tableau comparatif private pupils vs population private", c["private_pupils"][y],
                     pop["private"][2])
    # primary totals vs population: public primary and private rows; and prev-year column vs previous edition
    for ed, pr in primaries.items():
        pop = populations.get(ed, {})
        for code in ("public_primary", "private"):
            if code in pr and code in pop and isinstance(pr[code], tuple):
                for bi, sx in ((0, "boys"), (1, "girls")):
                    for k in range(7):
                        cross.eq(f"{ed} primary total '{code}' {sx} col {k} vs population table",
                                 pr[code][bi][k], pop[code][bi][k])
    for ed, pop in populations.items():
        i = ED_ORDER.index(ed)
        if i == 0:
            continue
        pe = ED_ORDER[i - 1]
        if EDITIONS[pe][1] != EDITIONS[ed][1] - 1 or pe not in populations:
            continue
        for code in pop:
            if code in populations[pe] and pop[code][3] is not None:
                cross.eq(f"{ed} population '{code}' previous-year total vs {pe} total", pop[code][3],
                         populations[pe][code][2])
        for code in primaries.get(ed, {}):
            if code in primaries.get(pe, {}) and isinstance(primaries[ed][code], tuple) and primaries[ed][code][3] is not None:
                cross.eq(f"{ed} primary total '{code}' previous-year total vs {pe}", primaries[ed][code][3],
                         primaries[pe][code][2])
    for (y, name), (prev, ed) in prev_totals.items():
        if (y, name) in est_this:
            cross.eq(f"{ed} establishment '{name}' previous-year total vs {est_this[(y, name)][1]}", prev,
                     est_this[(y, name)][0])
    CHK["cross_table"] = cross
    compute_series()
    if write:
        write_all()
    report = {t: {"checks": c.n, "failures": c.fail} for t, c in CHK.items()}
    for t, c in COMP.items():
        report.setdefault(t, {})["reprints"] = c
    return report


HDR = ["census", "gallica_ark", "source_page", "gallica_view", "table_id"]


SER_OUT = {}
DERIVED = {}      # (table, edition, key, year) -> flag of a printed cell in that edition
# (table, key tuple, year) -> flag for cells of the windowed series (see the notes)
SERIES_FLAGS = {}


def compute_series():
    for tab in list(SERIES):
        SER_OUT[tab] = window_series(tab, SERIES[tab], lambda k: "/".join(map(str, k)))


def series_rows(tab, keycols, flagfn=None):
    rows = []
    for key, year, ed, v, rm, printings in sorted(SER_OUT.get(tab, []), key=lambda r: (r[1], str(r[0]))):
        f = SERIES_FLAGS.get((tab, key, year)) or DERIVED.get((tab, ed, key, year), "")
        rows.append(rm + [tab.replace("education_", ""), year] + list(key) + [v, f])
    return rows


def write_csv(name, header, rows):
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / f"{name}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


RESULTS = {}


def write_all():
    from education_notes import write_notes
    def put(name, header, rows):
        RESULTS[name] = {"rows": write_csv(name, header, rows), "header": header}
    put("education_total_pupils", HDR + ["year", "label_fr", "value", "flag"], ROWS["education_total_pupils"])
    put("education_exams_nationality",
        HDR + ["year", "exam", "exam_fr", "stage", "stage_fr", "sex", "sex_fr", "nationality", "nationality_fr",
               "value", "flag"], ROWS["education_exams_nationality"])
    put("education_civil_personality_establishments",
        HDR + ["year", "locality", "establishment", "measure", "measure_fr", "sex", "sex_fr", "nationality",
               "nationality_fr", "value", "flag"], ROWS["education_civil_personality_establishments"])
    if ROWS["education_secondary_establishments_sgt1939"]:
        put("education_secondary_establishments_sgt1939",
            HDR + ["year", "branch", "establishment", "sex", "sex_fr", "nationality", "nationality_fr", "value", "flag"],
            ROWS["education_secondary_establishments_sgt1939"])
    if ROWS["education_first_degree_sgt1939"]:
        put("education_first_degree_sgt1939",
            HDR + ["year", "school_type", "school_type_fr", "sex", "sex_fr", "nationality", "nationality_fr", "value",
                   "flag"], ROWS["education_first_degree_sgt1939"])
    put("education_music_school", HDR + ["year", "class", "class_fr", "sex", "sex_fr", "nationality", "nationality_fr",
                                         "value", "flag"], ROWS["education_music_school"])
    if ROWS["education_commerce_school"]:
        put("education_commerce_school", HDR + ["year", "course", "course_fr", "sex", "sex_fr", "nationality",
                                                "nationality_fr", "value", "flag"], ROWS["education_commerce_school"])
    put("education_primary_totals", HDR + ["year", "school_type", "school_type_fr", "measure", "sex", "sex_fr",
                                           "nationality", "nationality_fr", "value", "flag"],
        ROWS["education_primary_totals"])
    put("education_school_population", HDR + ["year", "school_type", "school_type_fr", "measure", "sex", "sex_fr",
                                              "nationality", "nationality_fr", "value", "flag"],
        ROWS["education_school_population"])
    put("education_vocational", HDR + ["year", "locality", "school_fr", "value", "flag"], ROWS["education_vocational"])
    put("education_libraries", HDR + ["year", "library", "library_fr", "measure", "measure_fr", "value", "flag"],
        series_rows("education_libraries", 4))
    put("education_arabic_courses", HDR + ["year", "course", "course_fr", "value", "flag"],
        series_rows("education_arabic_courses", 2))
    put("education_canteens", HDR + ["year", "portions", "portions_fr", "value", "flag"],
        series_rows("education_canteens", 2))
    put("education_comparative", HDR + ["year", "item", "item_fr", "value", "flag"],
        series_rows("education_comparative", 2))
    put("education_school_population_series", HDR + ["year", "sex", "sex_fr", "nationality", "nationality_fr",
                                                     "value", "flag"],
        series_rows("education_school_population_series", 4))
    put("education_quinquennial_pupils", HDR + ["year", "sex", "sex_fr", "sector", "sector_fr", "value", "flag"],
        series_rows("education_quinquennial_pupils", 4))
    if SERIES["education_budget"]:
        put("education_budget", HDR + ["year", "budget_line", "value_francs", "flag"],
            series_rows("education_budget", 1))
    write_notes(RESULTS, CHK, COMP, NOTES, SOURCES, EDITIONS, CHAPTER)



if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "check":
        rep = build(write=False)
        for t, r in rep.items():
            if "checks" in r:
                print(f"{t}: {r['checks']} checks, {len(r['failures'])} failures")
                for f in r["failures"]:
                    print("   ", f)
        for t, c in COMP.items():
            print(f"{t}: {c['compared']} reprinted cells compared, {len(c['diffs'])} differ")
            for d in c["diffs"]:
                print("   ", d)
    elif cmd == "build":
        rep = build()
        json.dump(rep, open(OUT / "education_summary_validation.json", "w"), indent=1, ensure_ascii=False)
        for k, v in RESULTS.items():
            print(k, v["rows"])
    else:
        print(__doc__)
