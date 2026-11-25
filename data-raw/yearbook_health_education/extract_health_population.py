#!/usr/bin/env python3
"""Health chapter (III) population tables of the Statistique générale de la
Tunisie, 12 editions 1922-1939: hospitals of Tunis (Hôpital civil français,
Hôpital Sadiki, Rabta / Ernest-Conseil, Manouba), hospitals and dispensaries of
the interior, and the "Statistique sanitaire de la ville de Tunis".

  python3 extract_health_population.py check   parse transcriptions, run every check
  python3 extract_health_population.py build   ... and write csv/health_*.csv + notes

Source of truth: transcribed/health_pop_<edition>.txt, transcribed from the page
images (half-resolution views, native-resolution crops from
data-raw/yearbook_demography/hires.py where a digit was doubtful), with Gallica
OCR drafts as a starting point. Format: sections '@<table> view=.. page=..
[year=..|years=..]', an optional 'cols:' line, rows 'label | v v v'. Values carry
no thousands separator; printed » = 0; '.' = cell not printed.
"""
import csv
import json
import re
import sys
from collections import defaultdict
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


# ----------------------------------------------------------------- parsing

def num(s):
    if s in (".", "x"):
        return None
    v = float(s)
    return int(v) if re.fullmatch(r"-?\d+", s) else v


def parse(ed):
    secs = []
    cur = None
    for line in (TR / f"health_pop_{ed}.txt").read_text().splitlines():
        line = line.rstrip()
        if not line.strip() or line.startswith("#"):
            continue
        if line.startswith("@"):
            parts = line[1:].split()
            cur = {"table": parts[0], "ed": ed, "ark": EDITIONS[ed], "rows": [], "cols": None}
            rest = " ".join(parts[1:])
            for k, v in re.findall(r"(\w+)=([^=]+?)(?=\s+\w+=|$)", rest):
                cur[k] = v.strip()
            cur["view"] = int(cur["view"])
            cur["page"] = int(cur["page"]) if cur.get("page", "").isdigit() else ""
            if "years" in cur:
                cur["years"] = [int(y) for y in cur["years"].split()]
            if "year" in cur:
                cur["year"] = int(cur["year"])
            secs.append(cur)
            continue
        if line.startswith("cols:"):
            c = line[5:].strip()
            cur["cols"] = [x.strip() for x in c.split(";")] if ";" in c else c.split()
            continue
        label, vals = line.rsplit("|", 1)
        label = label.strip()
        code = None
        if " ; " in label:
            code, label = [x.strip() for x in label.split(" ; ", 1)]
        raw = vals.split()
        vals = [num(x) for x in raw]
        if cur["cols"] and len(vals) != len(cur["cols"]):
            raise ValueError(f"{ed} {cur['table']} row {label!r}: {len(vals)} values, {len(cur['cols'])} cols")
        cur["rows"].append({"label": label, "code": code, "v": vals, "raw": raw})
    return secs


class Checks:
    def __init__(self):
        self.n = defaultdict(int)
        self.fail = defaultdict(list)

    def eq(self, topic, what, got, printed, tol=0):
        if got is None or printed is None:
            return
        self.n[topic] += 1
        if abs(got - printed) > tol + 1e-9:
            self.fail[topic].append(f"{what}: cells give {round(got, 3)}, printed {printed}")


CHK = Checks()
RECTIFIED_RULE = {}


def s(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) if xs else None


# ----------------------------------------------------------------- checks per section

def tot_label(lab):
    return re.match(r"(?i)^(totaux|total|totals?)\b", lab) is not None


def check_grid(sec, topic, row_total=True, col_total=True):
    """Last column = row total (if row_total); a TOTAUX row = column sums."""
    ed, t = sec["ed"], sec["table"]
    data = [r for r in sec["rows"] if not tot_label(r["label"]) and r["code"] != "extra"]
    tots = [r for r in sec["rows"] if tot_label(r["label"])]
    if row_total:
        for r in sec["rows"]:
            CHK.eq(topic, f"{ed} {t} row {r['label']}: cells vs row total", s(r["v"][:-1]), r["v"][-1])
    if col_total and tots:
        T = tots[-1]["v"]
        for j in range(len(T)):
            CHK.eq(topic, f"{ed} {t} column {sec['cols'][j] if sec['cols'] else j}: rows vs {tots[-1]['label']}",
                   s(r["v"][j] for r in data), T[j])


MOV_GROUPS = (("adm", "admitted"), ("rec", "discharged_recovered"), ("dth", "discharged_died"))


def check_movements(sec, topic):
    cols = sec["cols"]
    for r in sec["rows"]:
        d = dict(zip(cols, r["v"]))
        for g, _ in MOV_GROUPS + (("eoy", ""),):
            if f"{g}_t" in d:
                CHK.eq(topic, f"{sec['ed']} {sec['table']} {r['label']} {g}: m+f+c vs total",
                       s([d.get(f"{g}_m"), d.get(f"{g}_f"), d.get(f"{g}_c")]), d[f"{g}_t"])


def check_diff(sec, topic, rows=None):
    """Year columns, then 'en plus' / 'en moins' (last year minus the one before)."""
    y = sec["years"]
    n = len(y)
    a, b = (n - 1, n - 2) if y[-1] > y[-2] else (0, 1)
    for r in rows or sec["rows"]:
        v = r["v"]
        if len(v) < n + 2 or v[a] is None or v[b] is None or (v[n] is None and v[n + 1] is None):
            continue
        d = v[a] - v[b]
        plus, minus = v[n] or 0, v[n + 1] or 0
        CHK.eq(topic, f"{sec['ed']} {sec['table']} {r['label']}: difference", d, plus - minus, tol=0.011)


def check_interior(sec, topic):
    cols = sec["cols"]
    data = [r for r in sec["rows"] if not tot_label(r["label"])]
    for r in sec["rows"]:
        d = dict(zip(cols, r["v"]))
        for g in ("eur", "ind", "deu", "din", "pat", "dth"):
            if f"{g}_t" in d:
                CHK.eq(topic, f"{sec['ed']} interior {r['label']} {g}: m+f+c vs total",
                       s([d.get(f"{g}_m"), d.get(f"{g}_f"), d.get(f"{g}_c")]), d[f"{g}_t"])
        if "pat_all" in d:
            CHK.eq(topic, f"{sec['ed']} interior {r['label']}: eur+ind vs all", s([d.get("eur_t"), d.get("ind_t")]), d["pat_all"])
        if "dth_all" in d:
            CHK.eq(topic, f"{sec['ed']} interior {r['label']}: deaths eur+ind vs all", s([d.get("deu_t"), d.get("din_t")]), d["dth_all"])
    tots = [r for r in sec["rows"] if tot_label(r["label"])]
    if tots:
        for j, c in enumerate(cols):
            CHK.eq(topic, f"{sec['ed']} interior column {c}: rows vs TOTAL", s(r["v"][j] for r in data), tots[-1]["v"][j])


def check_natality(sec, topic):
    R = {r["code"]: r["v"] for r in sec["rows"]}
    check_grid({**sec, "rows": [r for r in sec["rows"] if r["code"] != "mortality_per_1000"]}, topic, col_total=False)
    for j in range(len(sec["cols"])):
        if "deaths_corrected" in R and "non_residents" in R:
            # the definition varies: 1922 subtracts only non-residents, later
            # editions also stillbirths; accept either and record which
            a = R["deaths"][j] - R["non_residents"][j]
            b = a - R["stillbirths"][j]
            got = a if a == R["deaths_corrected"][j] else b
            CHK.eq(topic, f"{sec['ed']} natality col {j}: deaths - non-residents (- stillbirths) vs rectified",
                   got, R["deaths_corrected"][j])
            RECTIFIED_RULE[(sec["ed"], j)] = "minus_nonres" if got == a else "minus_nonres_stillb"
        if "births_minus_deaths" in R:
            # sgt1935 and later use gross deaths here; earlier editions rectified deaths
            a = R["births"][j] - R["deaths_corrected"][j]
            b = R["births"][j] - R["deaths"][j]
            got = b if (b == R["births_minus_deaths"][j] and a != b) else a
            CHK.eq(topic, f"{sec['ed']} natality col {j}: births - deaths vs difference",
                   got, R["births_minus_deaths"][j])
        if "mortality_per_1000" in R and R["population"][j]:
            a = 1000 * R["deaths_corrected"][j] / R["population"][j]
            b = 1000 * R["deaths"][j] / R["population"][j]
            p = R["mortality_per_1000"][j]
            got = b if abs(b - p) < abs(a - p) else a
            CHK.eq(topic, f"{sec['ed']} natality col {j}: rate vs deaths/population",
                   got, p, tol=0.06)


def check_ward_days(sec, topic):
    rows = [r for r in sec["rows"] if not tot_label(r["label"]) and not r["label"].endswith("TOTAL")]
    check_diff(sec, topic, rows + [r for r in sec["rows"] if tot_label(r["label"])])
    T = [r for r in sec["rows"] if tot_label(r["label"])][-1]["v"]
    for j in range(len(T)):
        CHK.eq(topic, f"{sec['ed']} ward days col {j}: wards vs TOTAUX", s(r["v"][j] for r in rows), T[j])
    sub = [r for r in sec["rows"] if r["label"].endswith(" TOTAL")]
    for st in sub:
        p = st["label"][:-6]
        parts = [r for r in rows if r["label"].startswith(p + " ")]
        for j in range(2):
            CHK.eq(topic, f"{sec['ed']} ward days {p} col {j}: parts vs subtotal", s(r["v"][j] for r in parts), st["v"][j])


def check_wards(sec, topic):
    """Ward / Manouba tables: rows '<nat> paying|free', optional '<nat> TOTAL',
    'beds', 'TOTAL'. Checks: row total column (if any), column totals, nationality totals."""
    cols = sec["cols"]
    data = [r for r in sec["rows"] if r["label"].split()[-1] in ("paying", "free")]
    has_total = cols[-1] == "total"
    if has_total:
        for r in data:
            CHK.eq(topic, f"{sec['ed']} {topic} {r['label']}: cells vs row total", s(r["v"][:-1]), r["v"][-1])
        for r in sec["rows"]:
            if r["label"].endswith(" TOTAL"):
                nat = r["label"].split()[0]
                CHK.eq(topic, f"{sec['ed']} {topic} {nat}: paying+free vs bracket total",
                       s(x["v"][-1] for x in data if x["label"].split()[0] == nat), r["v"][-1])
    T = [r for r in sec["rows"] if r["label"] == "TOTAL"]
    if T:
        for j, c in enumerate(cols):
            if c.startswith("beds"):
                continue
            CHK.eq(topic, f"{sec['ed']} {topic} column {c}: rows vs TOTAL", s(r["v"][j] for r in data), T[0]["v"][j])
    B = [r for r in sec["rows"] if r["label"] == "beds"]
    if B and B[0]["v"][-1] is not None and has_total:
        CHK.eq(topic, f"{sec['ed']} {topic} beds: wards vs printed total", s(B[0]["v"][:-1]), B[0]["v"][-1])


def run_checks(secs):
    for sec in secs:
        t = sec["table"]
        if t.endswith("_movements"):
            check_movements(sec, t)
        elif t.endswith("_population"):
            check_diff(sec, t)
            R = {r["code"]: r["v"] for r in sec["rows"]}
            parts = [k for k in R if k.startswith("patient_days_")]
            if "patient_days" in R and parts:
                for j in range(2):
                    CHK.eq(t, f"{sec['ed']} {t} {sec['years'][j]}: patient-day categories vs patient days",
                           s(R[k][j] for k in parts), R["patient_days"][j])
        elif t in ("rabta_diseases", "rabta_months", "tunis_month_nationality", "tunis_cause_nationality",
                   "tunis_month_cause", "civil_births"):
            check_grid(sec, t)
        elif t == "tunis_natality_mortality":
            check_natality(sec, t)
        elif t == "interior":
            check_interior(sec, t)
        elif t in ("civil_wards", "sadiki_wards", "manouba"):
            check_wards(sec, t)
        elif t == "civil_ward_days":
            check_ward_days(sec, t)
        elif t.endswith("_consultations"):
            if sec["cols"] and "total" in sec["cols"]:
                i = sec["cols"].index("total")
                for r in sec["rows"]:
                    CHK.eq(t, f"{sec['ed']} {t} {r['label']}: parts vs total", s(r["v"][:i]), r["v"][i])
