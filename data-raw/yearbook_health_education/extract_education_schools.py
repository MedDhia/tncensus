"""Rebuild education_schools.csv (and its notes) from the hand transcriptions.

Sources: the school-by-school lists of the public-instruction chapter of the
Statistique generale de la Tunisie, editions sgt1922, sgt1930 and sgt1939
(see transcribed/education_schools_<edition>.txt for the format).

Run from anywhere:  python3 data-raw/yearbook_health_education/extract_education_schools.py
Writes csv/education_schools.csv, csv/education_schools.md (notes; the
validation section is regenerated) and csv/education_schools_validation.json.
"""
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TRANS = HERE / "transcribed"
OUT = HERE / "csv"

EDITIONS = {
    "sgt1922": {"ark": "bpt6k9105649x", "year": 1922},
    "sgt1930": {"ark": "bpt6k9105652d", "year": 1930},
    "sgt1939": {"ark": "bpt6k9105739w", "year": 1939},
}

NAT = ["french", "muslim", "jewish", "italian", "maltese", "other"]
NAT_FR_M = ["Français", "Musulmans", "Israélites", "Italiens", "Maltais", "Divers"]
NAT_FR_F = ["Françaises", "Musulmanes", "Israélites", "Italiennes", "Maltaises", "Diverses"]

# column groups: name -> list of (measure, sex, nationality, nationality_fr) for each
# printed cell; None marks a printed total (validation only, not stored)
GROUPS = {
    "classes": [("classes", "total", "", "")],
    "staff": [("staff_french_diploma", "total", "", ""), ("staff_arabic", "total", "", ""),
              ("staff_other", "total", "", ""), None],
    "boys": [("pupils", "male", n, f) for n, f in zip(NAT, NAT_FR_M)] + [None],
    "girls": [("pupils", "female", n, f) for n, f in zip(NAT, NAT_FR_F)] + [None],
    "gen": [None],
    "prev": [("pupils_total_previous_year", "total", "total", "Totaux généraux de l'année précédente")],
    "apprentices": [("apprentices", "total", "", "")],
}
GROUPS["cstaff"] = GROUPS["classes"] + GROUPS["staff"]
GROUPS["genprev"] = GROUPS["gen"] + GROUPS["prev"]
# which page of a two-page spread carries each column (L = left/even view)
SIDE_SPREAD = {"classes": "LLLLL", "staff": "LLLL", "boys": "LLRRRRR", "girls": "R" * 7,
               "gen": "R", "prev": "R", "apprentices": "L",
               "cstaff": "LLLLL", "genprev": "RR"}

SPECIAL = {"REPORT", "AREPORTER", "TOTAL", "SUB", "SECTOT", "CMP"}


class Cell:
    def __init__(self, tok):
        self.raw = tok
        self.flag = ""
        t = tok
        self.alt = None
        m2 = re.fullmatch(r"(\d+)\+(\d+)", t)
        if m2:  # one cell printed as two numbers (bracketed schools): store the sum
            self.v, self.flag, self.alt = int(m2.group(1)) + int(m2.group(2)), "derived_from_totals", None
            return
        m = re.fullmatch(r"(\d+|»)#(\d+)", t)
        if m:  # printed value, then the value the printed totals imply (used for the checks)
            t, self.alt = m.group(1) + "#", int(m.group(2))
        if t.endswith("!"):
            self.flag, t = "ocr_corrected", t[:-1]
        elif t.endswith("#"):
            self.flag, t = "total_mismatch", t[:-1]
        if t in ("»", "0"):
            self.v = 0
        elif t == "?":
            self.v = None
        elif t == "-":  # cell left blank in print (only in total lines)
            self.v = None
        elif t == "na":  # printed a word instead of a number ("Création", "Réouverture")
            self.v, self.flag = None, "not_applicable"
        else:
            if not re.fullmatch(r"\d+", t):
                raise ValueError(f"bad token {tok!r}")
            self.v = int(t)


def parse(edition):
    path = TRANS / f"education_schools_{edition}.txt"
    blocks = []
    blk = view = None
    for ln, line in enumerate(path.read_text().splitlines(), 1):
        s = line.split("  #")[0].rstrip()
        if not s.strip() or s.startswith("# "):
            continue
        if s.startswith("@ "):
            parts = s[2:].split()
            kw = dict(p.split("=", 1) for p in parts[1:])
            blk = {"name": parts[0], "sector": kw["sector"], "level": kw["level"],
                   "cols": kw["cols"].split(","), "table_fr": kw.get("table", "").replace("_", " "),
                   "rows": []}
            blocks.append(blk)
            continue
        if s.startswith("## "):
            m = re.match(r"## views? (\d+)(?: (\d+))? pages? (\d+)(?: (\d+))?", s)
            l, r, pl, pr = m.groups()
            view = {"L": (int(l), int(pl)), "R": (int(r or l), int(pr or pl))}
            continue
        if s.startswith("% "):
            blk["rows"].append({"kind": "SECTION", "label": s[2:].strip(), "ln": ln})
            continue
        f = [x.strip() for x in re.split(r"\s*\|\s*", s)]
        loc, school, groups = f[0], f[1], f[2:]
        if len(groups) != len(blk["cols"]):
            raise ValueError(f"{path.name}:{ln}: {len(groups)} groups, expected {len(blk['cols'])}")
        cells = {}
        for g, txt in zip(blk["cols"], groups):
            toks = txt.split()
            if len(toks) != len(GROUPS[g]):
                raise ValueError(f"{path.name}:{ln}: group {g} has {len(toks)} cells")
            cells[g] = [Cell(t) for t in toks]
        kind = loc if loc in SPECIAL else "SCHOOL"
        blk["rows"].append({"kind": kind, "loc": loc, "school": school, "cells": cells,
                            "view": view, "ln": ln})
    return blocks


log_alt = []


def check_rows(edition, blk, log):
    """Row checks; derive '?' cells from row totals. Returns counts."""
    n = ok = 0
    for r in blk["rows"]:
        if r["kind"] == "SECTION":
            continue
        c = r["cells"]
        for g in ("staff", "cstaff", "boys", "girls"):
            if g not in c:
                continue
            parts, tot = c[g][:-1], c[g][-1]
            if all(x.flag == "not_applicable" for x in c[g]):
                continue
            if g == "cstaff":
                parts = c[g][1:-1]
            if tot.alt is not None:  # misprinted total cell: check against the value the parts imply
                n += 1
                ok += sum(x.v for x in parts if x.v is not None) == tot.alt
                log_alt.append(f"{edition} l{r['ln']} {r['loc']} / {r['school']}: printed {g} total {tot.v}, cells sum to {tot.alt}")
                continue
            unk = [x for x in parts if x.v is None]
            if r["kind"] in ("SCHOOL", "TOTAL") and len(unk) == 1 and tot.v is not None:
                unk[0].v = tot.v - sum((x.alt if x.alt is not None else x.v) for x in parts if x.v is not None)
                unk[0].flag = "derived_from_totals"
                if unk[0].v < 0:
                    log.append(f"{edition} l{r['ln']} {g}: derived negative value")
                continue  # the total was used to derive: no independent check
            if any(x.alt is not None for x in parts):
                n += 1
                if sum(x.alt if x.alt is not None else x.v for x in parts) == tot.v:
                    ok += 1
                    log_alt.append(f"{edition} l{r['ln']} {r['loc']} / {r['school']}: {g} sum {sum(x.v for x in parts)} != printed {tot.v}; printed cell kept, flagged total_mismatch")
                else:
                    log.append(f"{edition} l{r['ln']} {g}: alt value does not fix the row")
                continue
            if r["kind"] != "SCHOOL" and not unk and tot.v is not None and any(x.flag == "total_mismatch" for x in c[g]):
                n += 1
                if sum(x.v for x in parts) == tot.v:
                    ok += 1
                else:
                    log_alt.append(f"{edition} l{r['ln']} {r['loc']} / {r['school']}: {g} sum {sum(x.v for x in parts)} != printed {tot.v} (misprinted total cell, see column checks)")
                continue
            if unk or tot.v is None:
                if r["kind"] == "SCHOOL" and unk:
                    log.append(f"{edition} l{r['ln']} {g}: unresolved unknowns")
                continue
            n += 1
            s = sum(x.v for x in parts)
            if s == tot.v:
                ok += 1
            else:
                log.append(f"{edition} l{r['ln']} {r['loc']} / {r['school']}: {g} sum {s} != printed {tot.v}")
        gen = c.get("gen", c.get("genprev"))
        if gen and gen[0].v is not None:
            if "boys" in c and c["boys"][-1].v is not None and c["girls"][-1].v is not None:
                n += 1
                s = sum(x.alt if x.alt is not None else x.v for x in (c["boys"][-1], c["girls"][-1]))
                if s == gen[0].v:
                    ok += 1
                else:
                    log.append(f"{edition} l{r['ln']} {r['loc']} / {r['school']}: boys+girls {s} != total {gen[0].v}")
    return n, ok


def check_columns(edition, blk, log, results):
    """Compare running column sums with the printed Report / A reporter / totals."""
    n = ok = 0
    cum = {}       # cumulative over the block
    sub = {}       # since last SUB / SECTION
    sec = {}       # since last SECTION
    last_carry = None

    def add(acc, r):
        for g, cs in r["cells"].items():
            for i, x in enumerate(cs):
                if x.v is not None:
                    acc[(g, i)] = acc.get((g, i), 0) + (x.alt if x.alt is not None else x.v)

    for r in blk["rows"]:
        k = r["kind"]
        if k == "SECTION":
            sub.clear()
            sec.clear()
            continue
        if k == "SCHOOL":
            add(cum, r)
            add(sub, r)
            add(sec, r)
            continue
        ref = {"AREPORTER": cum, "TOTAL": cum, "REPORT": cum, "SUB": sub, "SECTOT": sec, "CMP": cum}[k]
        for g, cs in r["cells"].items():
            for i, x in enumerate(cs):
                if x.v is None:
                    continue
                if g == "prev" and k in ("SUB", "SECTOT"):
                    pass
                n += 1
                got = ref.get((g, i), 0)
                if k == "REPORT" and last_carry and last_carry.get((g, i)) == x.v:
                    got = x.v  # same figure as the previous page's printed "A reporter"
                if got == x.v:
                    ok += 1
                elif x.flag == "total_mismatch":  # printed total that does not add up; marked '#' after reading the image
                    log_alt.append(f"{edition} {blk['name']} l{r['ln']} {k} {r['school']}: column {g}[{i}] sum {got} != printed {x.v} (printed total kept; the cells were re-read on the image)")
                else:
                    log.append(f"{edition} {blk['name']} l{r['ln']} {k} {r['school']}: column {g}[{i}] sum {got} != printed {x.v}")
        if k in ("REPORT", "AREPORTER"):  # carry the printed figures forward, so each page is checked on its own
            if k == "AREPORTER":
                last_carry = {}
            for g, cs in r["cells"].items():
                for i, x in enumerate(cs):
                    if x.v is None:
                        continue
                    if k == "AREPORTER":
                        last_carry[(g, i)] = x.v
                    if k == "REPORT" or x.flag != "total_mismatch":
                        cum[(g, i)] = x.v
        if k == "SUB":
            sub.clear()
        if k == "TOTAL":
            results.append({"edition": edition, "block": blk["name"], "label": r["school"],
                            "printed": {f"{g}[{i}]": x.v for g, cs in r["cells"].items() for i, x in enumerate(cs)}})
    return n, ok


def rows_out(edition, blk):
    e = EDITIONS[edition]
    out = []
    order = 0
    section = ""
    for r in blk["rows"]:
        if r["kind"] == "SECTION":
            section = r["label"]
            continue
        stored_total = r["kind"] == "TOTAL" and r["school"].endswith("[store]")
        if r["kind"] != "SCHOOL" and not stored_total:
            continue
        order += 1
        for g, cs in r["cells"].items():
            for i, x in enumerate(cs):
                spec = GROUPS[g][i]
                if spec is None:
                    continue
                measure, sex, nat, natfr = spec
                side = SIDE_SPREAD[g][i]
                view, page = r["view"][side]
                flag = x.flag
                if x.v is None and not flag:
                    flag = "illegible"
                out.append({
                    "census": edition, "gallica_ark": e["ark"], "source_page": page,
                    "gallica_view": view, "year": e["year"], "school_sector": blk["sector"],
                    "school_level": blk["level"], "table_fr": blk["table_fr"], "section_fr": section,
                    "inspection_district": "",
                    "locality": "TOTAL (printed)" if stored_total else r["loc"],
                    "school": r["school"].replace(" [store]", ""),
                    "row_order": order, "measure": measure, "sex": sex, "nationality": nat,
                    "nationality_fr": natfr, "value": "" if x.v is None else x.v, "flag": flag})
    return out


def main():
    allrows, log, summary, totals = [], [], {}, []
    for ed in EDITIONS:
        p = TRANS / f"education_schools_{ed}.txt"
        if not p.exists():
            continue
        for blk in parse(ed):
            rn, rok = check_rows(ed, blk, log)
            cn, cok = check_columns(ed, blk, log, totals)
            rows = rows_out(ed, blk)
            allrows += rows
            nsch = sum(1 for r in blk["rows"] if r["kind"] == "SCHOOL")
            summary[f"{ed}/{blk['name']}"] = {
                "schools": nsch, "cells": len(rows), "row_checks": rn, "row_checks_passed": rok,
                "column_checks": cn, "column_checks_passed": cok,
                "flags": {f: sum(1 for x in rows if x["flag"] == f) for f in sorted({x["flag"] for x in rows}) if f}}
    OUT.mkdir(exist_ok=True)
    cols = ["census", "gallica_ark", "source_page", "gallica_view", "year", "school_sector",
            "school_level", "table_fr", "section_fr", "inspection_district", "locality", "school",
            "row_order", "measure", "sex", "nationality", "nationality_fr", "value", "flag"]
    with open(OUT / "education_schools.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, cols)
        w.writeheader()
        w.writerows(allrows)
    json.dump({"summary": summary, "mismatches": log, "kept_misprints": log_alt, "printed_totals": totals},
              open(OUT / "education_schools_validation.json", "w"), ensure_ascii=False, indent=1)
    for k, v in summary.items():
        print(k, v)
    print(len(allrows), "cells;", len(log), "problems")
    for m in log:
        print("  ", m)
    for m in log_alt:
        print("  kept:", m)
    return summary, log, totals


if __name__ == "__main__":
    main()
