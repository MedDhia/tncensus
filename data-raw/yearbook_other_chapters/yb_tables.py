"""Shared helpers for extract_justice.py, extract_prisons.py and extract_property.py
(Statistique générale de la Tunisie, 12 editions sgt1922-sgt1939).

Transcription format (transcribed/<chapter>_<edition>.txt):

    # comment
    @<table> view=<gallica view> page=<printed page> [key=value ...]     (value with spaces: key="a b")
    img: all | <free text>        optional: 'all' = every cell of the section read on the page image;
                                  otherwise the cells rest on the Gallica OCR plus the checks, except
                                  cells marked '!'
    cols: c1 c2 ...
    check: tot = a + b - c        optional: row identity checked on every line of the section
    <label> | v1 v2 ...           one printed line; label as printed (or a code for row headings)
    <label> || text ;; text       text table: cells separated by ';;'

Cell tokens: integer or decimal ('.' before centimes/decimals, no thousands separator); printed » = 0;
'?' = illegible (stored NA, flag illegible); '-' = nothing printed / not applicable (NA, not_applicable);
a trailing '!' = read on the image, Gallica OCR differs (flag ocr_corrected).
"""
import csv
import json
import re
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
TR = HERE / "transcribed"
OUT = HERE / "csv"

EDITIONS = {
    "sgt1922": "bpt6k9105649x", "sgt1923": "bpt6k9105649x", "sgt1924": "bpt6k9105649x",
    "sgt1925": "bpt6k9105650k", "sgt1926": "bpt6k9105650k", "sgt1927": "bpt6k91056510",
    "sgt1928": "bpt6k91056510", "sgt1929": "bpt6k9105652d", "sgt1930": "bpt6k9105652d",
    "sgt1935": "bpt6k9105653t", "sgt1936": "bpt6k91056547", "sgt1939": "bpt6k9105739w",
}
ORDER = list(EDITIONS)
COMMON = ["census", "table_id", "gallica_ark", "source_page", "gallica_view", "year"]
CREDIT = "Source gallica.bnf.fr / Ministère des Affaires étrangères."


class Cell:
    __slots__ = ("raw", "value", "flag")

    def __init__(self, raw):
        self.raw = raw
        self.flag = ""
        t = raw
        if t.endswith("!"):
            self.flag, t = "ocr_corrected", t[:-1]
        if t == "?":
            self.value, self.flag = None, "illegible"
        elif t == "-":
            self.value, self.flag = None, "not_applicable"
        else:
            self.value = Decimal(t)

    def __repr__(self):
        return self.raw


def parse(path, ed):
    secs, cur = [], None
    for n, line in enumerate(path.read_text().splitlines(), 1):
        line = line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("@"):
            head = line[1:]
            name = head.split()[0]
            cur = {"table": name, "ed": ed, "ark": EDITIONS[ed], "rows": [], "cols": None, "img": "",
                   "line": n}
            for k, v1, v2 in re.findall(r'(\w+)=(?:"([^"]*)"|(\S+))', head[len(name):]):
                cur[k] = v1 or v2
            cur["view"] = int(cur["view"])
            cur["page"] = int(cur["page"])
            secs.append(cur)
            continue
        if line.startswith("check:"):
            tgt, rhs = line[6:].split("=")
            cur.setdefault("checks", []).append((tgt.strip(), rhs.replace("- ", "-").replace("+", " ").split()))
            continue
        if line.startswith("img:"):
            cur["img"] = line[4:].strip()
            continue
        if line.startswith("cols:"):
            cur["cols"] = line[5:].split()
            continue
        if "||" in line:
            label, txt = line.split("||", 1)
            cur["rows"].append({"label": label.strip(), "text": [t.strip() for t in txt.split(";;")]})
            continue
        label, vals = line.rsplit("|", 1)
        cells = [Cell(x) for x in vals.split()]
        if len(cells) != len(cur["cols"]):
            raise ValueError(f"{path.name}:{n} {cur['table']} row {label!r}: "
                             f"{len(cells)} values for {len(cur['cols'])} columns")
        cur["rows"].append({"label": label.strip(), "cells": dict(zip(cur["cols"], cells))})
    return secs


def years_of(sec):
    ys = sec.get("years")
    if ys:
        a, b = ys.split("-")
        return list(range(int(a), int(b) + 1))
    return [int(sec["year"])]


TOTAL_RE = re.compile(r"(?i)^(totaux|total|totals?)\b")


def is_total(label):
    return TOTAL_RE.match(label) is not None


# ----------------------------------------------------------------- checks

class Checks:
    def __init__(self):
        self.n = defaultdict(int)
        self.fail = defaultdict(list)

    def eq(self, topic, what, got, printed, tol=Decimal(0)):
        if got is None or printed is None:
            return
        self.n[topic] += 1
        if abs(got - printed) > tol:
            self.fail[topic].append(f"{what}: cells give {got}, printed {printed} (difference {printed - got})")


def v(sec, label, col):
    for r in sec["rows"]:
        if r["label"] == label:
            return r["cells"][col].value
    raise KeyError((sec["table"], sec["ed"], label, col))


def ssum(vals):
    vals = list(vals)
    if any(x is None for x in vals):
        return None
    return sum(vals, Decimal(0))


def where(sec):
    return f"{sec['ed']} p.{sec['page']} (f{sec['view']}) {sec['table']}" + (
        f" [{sec['court']}]" if sec.get("court") else "") + (f" [{sec['matter']}]" if sec.get("matter") else "")


def check_col_totals(chk, topic, sec, cols=None, total=is_total, rows=None):
    """Every printed total line = sum of the data lines above it (since the previous total line)."""
    cols = cols or sec["cols"]
    block = []
    for r in sec["rows"]:
        if "cells" not in r:
            continue
        if total(r["label"]):
            for c in cols:
                chk.eq(topic, f"{where(sec)} {c}: lines vs {r['label']}",
                       ssum(x["cells"][c].value for x in block), r["cells"][c].value)
            block = []
        elif rows is None or r["label"] in rows:
            block.append(r)


def check_row(chk, topic, sec, target, parts, label_ok=lambda l: True, sign=None):
    """target = sum(parts) on every line (parts may carry a leading '-')."""
    for r in sec["rows"]:
        if "cells" not in r or not label_ok(r["label"]):
            continue
        c = r["cells"]
        vals = []
        for p in parts:
            neg = p.startswith("-")
            x = c[p.lstrip("-")].value
            vals.append(None if x is None else (-x if neg else x))
        chk.eq(topic, f"{where(sec)} {r['label']}: {target} = {' + '.join(parts)}", ssum(vals), c[target].value)


# ----------------------------------------------------------------- selection (rules 4 and 5)

def select_latest(recs, key_dims):
    """recs: dicts with census + key dims + value/raw. One record per key, from the latest edition
    (SPEC_ADDENDUM rule 4; rule 5 tables printed twice are handled the same way). Returns
    (kept, compared, diffs) with diffs = (key, edition, printed, kept edition, kept printed)."""
    by = defaultdict(list)
    for r in recs:
        by[tuple(r.get(k) for k in key_dims)].append(r)
    kept, compared, diffs = [], 0, []
    for k, rs in by.items():
        rs.sort(key=lambda r: ORDER.index(r["census"]))
        last = rs[-1]
        for r in rs[:-1]:
            compared += 1
            if r["value"] != last["value"]:
                diffs.append((k, r["census"], r["value"], last["census"], last["value"]))
        if last.get("_prefer"):          # REPRINT override
            alt = [r for r in rs if r["census"] == last["_prefer"]][0]
            last = dict(alt, flag="reprint_corrected")
        kept.append(last)
    return kept, compared, diffs


# ----------------------------------------------------------------- output

def fmt_val(x):
    if x is None:
        return ""
    if isinstance(x, Decimal):
        return format(x, "f")
    return str(x)


def write_csv(name, cols, rows):
    OUT.mkdir(exist_ok=True)
    with (OUT / f"{name}.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: fmt_val(r.get(k)) for k in cols})


def fmt_views(rows):
    by = defaultdict(set)
    for r in rows:
        by[r["census"]].add((r["source_page"], r["gallica_view"]))
    return "; ".join(f"{e} (`{EDITIONS[e]}`): " + ", ".join(f"p. {p}, f{v}" for p, v in sorted(by[e]))
                     for e in ORDER if e in by)


def write_notes(name, chapter_fr, script, rows, cols, coldoc, title_fr, title_en, paras, checks_n, fails,
                compared, diffs, coverage, rule_text, unit_text):
    years = sorted({r["year"] for r in rows if r.get("year") is not None})
    eds = [e for e in ORDER if e in {r["census"] for r in rows}]
    L = [f"# {title_fr}", "", f"*{title_en}.*", "",
         f"Source: *Statistique générale de la Tunisie*, chapter *{chapter_fr}*, editions {', '.join(eds)}. "
         + CREDIT, "",
         f"Pages and views of the stored values: {fmt_views(rows)}.", "",
         f"Transcriptions: `../transcribed/{script.split('_')[1].split('.')[0]}_<edition>.txt`; rebuild with "
         f"`python3 data-raw/yearbook_other_chapters/{script} build`.", "",
         f"Rows: {len(rows)}. Years: {', '.join(map(str, years))}.", "",
         unit_text, "", rule_text, "", "## Columns", ""]
    for c in cols:
        L.append(f"- `{c}`: {coldoc[c]}")
    L.append("")
    for p in paras:
        L += [p, ""]
    L += ["## Validation", "",
          f"- Checks against printed totals and identities: {checks_n}; passed: {checks_n - len(fails)}; "
          f"failed: {len(fails)}."]
    if fails:
        L += ["", "Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs "
              "unchanged in another edition's printing of the same cells):", ""]
        L += [f"  - {x}" for x in fails]
    L += ["", f"- Overlapping printings: {compared} cell comparisons with other editions printing the same "
          f"cell; {len(diffs)} differences."]
    if diffs:
        L += ["", "| cell | edition | printed | stored from | printed |", "|---|---|---|---|---|"]
        L += [f"| {' / '.join(fmt_val(x) for x in d[0])} | {d[1]} | {fmt_val(d[2])} | {d[3]} | {fmt_val(d[4])} |"
              for d in diffs]
    fl = defaultdict(int)
    for r in rows:
        if r.get("flag"):
            fl[r["flag"]] += 1
    L += ["", "- Flagged cells: " + (", ".join(f"{k}: {n}" for k, n in sorted(fl.items())) if fl else "none")
          + "."]
    if fl:
        dims = [c for c in cols if c not in COMMON + ["value", "flag", "gallica_ark", "table_id"]
                and not c.endswith("_fr")]
        L += [""] + [f"  - {r['census']} p.{r['source_page']} {r.get('year', '')} "
                     + " / ".join(fmt_val(r.get(d)) for d in dims) + f" = {fmt_val(r['value']) or 'NA'} ({r['flag']})"
                     for r in rows if r.get("flag")]
    L += ["", "## Image versus OCR", ""] + coverage
    (OUT / f"{name}.md").write_text("\n".join(L) + "\n")


def coverage_lines(secs, stored_keys=None):
    """Which sections were read cell by cell on the image, which rest on the OCR plus checks."""
    img, ocr, ncor = [], [], 0
    for s in secs:
        tag = f"{s['ed']} f{s['view']}" + (f" {s['court']}" if s.get("court") else "") + (
            f" {s['matter']}" if s.get("matter") else "")
        ncor += sum(1 for r in s["rows"] if "cells" in r for c in r["cells"].values() if c.flag == "ocr_corrected")
        if s["img"] == "all":
            img.append(tag)
        else:
            ocr.append(tag + (f" ({s['img']})" if s["img"] else ""))
    out = []
    out.append(f"- Read cell by cell on the page images ({len(img)} printings): " + (", ".join(img) or "none") + ".")
    out.append(f"- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and "
               f"every unclear OCR token re-read on a native-resolution crop ({len(ocr)} printings): "
               + (", ".join(ocr) or "none") + ".")
    out.append(f"- Cells whose image reading differs from the OCR (flag `ocr_corrected`): {ncor}.")
    return out


def write_validation(path, d):
    path.write_text(json.dumps(d, indent=1, ensure_ascii=False, default=fmt_val) + "\n")
