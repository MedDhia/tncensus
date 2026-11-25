#!/usr/bin/env python3
"""1926 census tables a, b, c, d, i, j, k from the Statistique générale de la Tunisie.

Builds data-raw/yearbook_demography/csv/cens1926_*.csv from the verified
transcriptions in transcribed/ and runs every printed-total check and the
cross-checks against the 1931 census volume. Exits non-zero if an unexpected
check fails.

How the transcriptions were made (see the notes files for details):
tables a and b are the cell-by-cell majority of Gallica's OCR across the five
printings (sgt1926-sgt1930), with every disagreement read on the scans; tables
c, d, i, j and k were transcribed from the scans and every cell compared with
the OCR of all five printings.

Usage:  python3 data-raw/yearbook_demography/extract_cens1926_a.py
"""
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TR = HERE / "transcribed"
OUT = HERE / "csv"
C31 = HERE.parent / "colonial_census" / "csv"
ARK26, ARK27 = "bpt6k9105650k", "bpt6k91056510"

CHECKS = {"done": 0, "passed": 0, "failed": []}
EXPECTED_FAILURES = set()


def check(name, got, want, expected_fail=False):
    CHECKS["done"] += 1
    if got == want:
        CHECKS["passed"] += 1
    else:
        CHECKS["failed"].append(f"{name}: computed {got} != printed {want}")
        if expected_fail:
            EXPECTED_FAILURES.add(name)


def lines(name):
    for ln in (TR / name).read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if ln and not ln.startswith("#"):
            yield ln


def write(name, header, rows):
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / f"{name}.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    print(f"{name}: {len(rows)} rows")
    return rows


NAT_EU = [("french", "Français"), ("italian", "Italiens"), ("maltese", "Maltais"),
          ("spanish", "Espagnols"), ("greek", "Grecs"), ("other_european", "Autres européens")]
NAT_IND = [("tunisian", "Tunisiens"), ("algerian", "Algériens"), ("moroccan", "Marocains"),
           ("sudanese", "Soudanais"), ("syrian", "Syriens"), ("tripolitanian", "Tripolitains"),
           ("other", "Autres nationalités")]
HDR = ["census", "table_id", "source_page", "gallica_ark", "gallica_view"]


# --- a) population by contrôle civil --------------------------------------
def table_a():
    rows, data, tot = [], [], None
    for ln in lines("cens1926_a_controle.txt"):
        name, vals = [s.strip() for s in ln.split("|")]
        v = [int(x) for x in vals.split()]
        assert len(v) == 24, name
        if name.startswith("="):
            tot = v
        else:
            data.append((name, v))
    for name, v in data + [("Totaux", tot)]:
        check(f"a {name} Europeans", sum(v[0:6]), v[6])
        check(f"a {name} Muslims", sum(v[7:14]), v[14])
        check(f"a {name} Jews", sum(v[15:21]), v[21])
        check(f"a {name} indigenous", v[14] + v[21], v[22])
        check(f"a {name} grand total", v[6] + v[22], v[23])
    for j in range(24):
        check(f"a column {j} vs Totaux", sum(v[j] for _, v in data), tot[j])
    flags = {("Thala", "muslim", "sudanese"): "ocr_corrected"}
    for name, v in data:
        groups = [("european", "Population européenne", NAT_EU, v[0:6], 2, 566),
                  ("muslim", "Population musulmane", NAT_IND, v[7:14], 2, 566),
                  ("jewish", "Population israélite",
                   [n for n in NAT_IND if n[0] != "sudanese"], v[15:21], 3, 567)]
        for grp, grp_fr, nats, vals, page, view in groups:
            for i, ((nat, nat_fr), x) in enumerate(zip(nats, vals)):
                if grp == "muslim" and i >= 4:
                    page, view = 3, 567
                rows.append(["sgt1926", "a", page, ARK26, view, 1926, name, grp, grp_fr, nat, nat_fr, x,
                             flags.get((name, grp, nat), "")])
    write("cens1926_controle_nationality",
          HDR + ["census_year", "controle_civil", "population_group", "population_group_fr",
                 "nationality", "nationality_fr", "value", "flag"], rows)
    return {n: v for n, v in data}, tot


# --- b) French by place of birth, 1891-1926 -------------------------------
YB = [1891, 1896, 1901, 1906, 1911, 1921, 1926]
# Printed cells that contradict the printed totals (kept as printed):
B_MISPRINTS = {("Tarn", 1906): 194, ("Vienne (Haute-)", 1921): 142}
B_FLAGS = {("Algérie : Oran", 1891): "ocr_corrected", ("Drôme", 1926): "ocr_corrected",
           ("Tarn", 1906): "total_mismatch", ("Vienne (Haute-)", 1921): "total_mismatch"}


def table_b():
    rows, run, page, view, data = [], [0] * 7, None, None, []
    for ln in lines("cens1926_b_birthplace.txt"):
        if ln.startswith("@"):
            page, view = map(int, ln[1:].split())
        elif ln.startswith("="):
            printed = [int(x) for x in ln[1:].split()]
            for k in range(7):
                # a misprinted cell explains the gap exactly: printed total = sum + (implied - printed cell)
                fix = sum(B_MISPRINTS[(n, YB[k])] - v[k] for n, v, _, _ in data if (n, YB[k]) in B_MISPRINTS)
                check(f"b running total p.{page} {YB[k]}", run[k], printed[k],
                      expected_fail=fix != 0 and run[k] + fix == printed[k])
        else:
            name, vals = [s.strip() for s in ln.split("|")]
            v = [int(x) for x in vals.split()]
            data.append((name, v, page, view))
            run = [a + b for a, b in zip(run, v)]
    for name, v, page, view in data:
        for k, y in enumerate(YB):
            rows.append(["sgt1926", "b", page, ARK26, view, name, y, v[k], B_FLAGS.get((name, y), "")])
    write("cens1926_french_birthplace",
          HDR + ["birthplace_fr", "census_year", "value", "flag"], rows)
    return {n: v for n, v, _, _ in data}, run


# --- c) foreigners by place of birth; d) Italians by province -------------
def blocks(name):
    out, cur = {}, None
    for ln in lines(name):
        if ln.startswith("@"):
            cur = ln[1:].strip()
            out[cur] = {"rows": [], "tot": None}
        elif ln.startswith("="):
            out[cur]["tot"] = [int(x) for x in ln[1:].split()]
        else:
            n, v = ln.split("|")
            out[cur]["rows"].append((n.strip(), [int(x) for x in v.split()]))
    return out


def table_cd():
    B = blocks("cens1926_c_d.txt")
    res = {}
    for t, fname, col, col_fr in (("c", "cens1926_foreign_birthplace", "birthplace_fr", None),
                                  ("d", "cens1926_italian_provinces", "province_fr", None)):
        left, right = B[f"{t} left"], B[f"{t} right"]
        for k, y in enumerate((1921, 1926)):
            check(f"{t} {y} carried total", sum(v[k] for _, v in left["rows"]), left["tot"][k])
            check(f"{t} {y} grand total", left["tot"][k] + sum(v[k] for _, v in right["rows"]),
                  right["tot"][k])
        rows = []
        for n, v in left["rows"] + right["rows"]:
            for k, y in enumerate((1921, 1926)):
                rows.append(["sgt1926", t, 6, ARK26, 570, n, y, v[k], ""])
        write(fname, HDR + [col, "census_year", "value", "flag"], rows)
        res[t] = ({n: v for n, v in left["rows"] + right["rows"]}, right["tot"])
    return res


# --- i) five largest towns, j) towns by size class ------------------------
COLS_TOWN = NAT_EU + [("european_total", "TOTAL de la population européenne"),
                      ("muslim", "Musulmans"), ("jewish", "Israélites"),
                      ("indigenous_total", "TOTAL de la population indigène"),
                      ("total", "TOTAL GÉNÉRAL")]


# Zarzis Italians: printed 9 in table j (all five printings) but 19 in table k;
# only 19 makes the printed European total (168) add up. Kept as printed, flagged.
J_MISPRINTS = {"Zarzis": ("italian", 19)}


def table_ij():
    rows, out, cls = [], {}, None
    classes = {"1° plus de 10.000 habitants": "over_10000",
               "2° de 5.000 à 10.000 habitants": "5000_to_10000"}
    for ln in lines("cens1926_i_j.txt"):
        if ln.startswith("@"):
            label = ln[1:].strip()[2:].strip()
            cls = (classes[label], label)
            continue
        n, c, v = [s.strip() for s in ln.split("|")]
        v = [int(x) for x in v.split()]
        check(f"j {n} Europeans", sum(v[:6]), v[6],
              expected_fail=n in J_MISPRINTS and sum(v[:6]) + J_MISPRINTS[n][1] - v[1] == v[6])
        check(f"j {n} indigenous", v[7] + v[8], v[9])
        check(f"j {n} total", v[6] + v[9], v[10])
        out[n] = v
        top5 = n in ("Tunis", "Sfax", "Sousse", "Bizerte", "Kairouan")
        for (code, fr), x in zip(COLS_TOWN, v):
            if code.endswith("total"):
                continue  # totals are validation only
            flag = "total_mismatch" if J_MISPRINTS.get(n, ("",))[0] == code else ""
            rows.append(["sgt1926", "j", 13, ARK26, 577, n, c, cls[0], cls[1], int(top5), code, fr, x, flag])
    write("cens1926_towns", HDR + ["town", "controle_civil", "size_class", "size_class_fr",
                                   "in_table_i", "population_group", "population_group_fr",
                                   "value", "flag"], rows)
    return out


# --- k) communes -----------------------------------------------------------
MONTHS = {m: i for i, m in enumerate(["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
                                       "août", "septembre", "octobre", "novembre", "décembre"], 1)}


def iso(d):
    m = re.fullmatch(r"(\d+)(?:er)? (\w+) (\d{4})", d)
    if m:
        return f"{m.group(3)}-{MONTHS[m.group(2)]:02d}-{int(m.group(1)):02d}"
    return d if re.fullmatch(r"\d{4}", d) else ""


def table_k():
    rows, out = [], {}
    for ln in lines("cens1926_k_communes.txt"):
        no, n, d, c, vals = [s.strip() for s in ln.split("|")]
        v = [int(x) for x in vals.split()]
        check(f"k {n} Europeans", sum(v[:6]), v[6])
        check(f"k {n} indigenous", v[7] + v[8], v[9])
        check(f"k {n} total", v[6] + v[9], v[10])
        out[n] = (c, v)
        no = int(no)
        for (code, fr), x, j in zip(COLS_TOWN, v, range(11)):
            if code.endswith("total"):
                continue
            left = j < 6
            page = (14 if no <= 30 else 16) + (0 if left else 1)
            view = (42 if no <= 30 else 44) + (0 if left else 1)
            rows.append(["sgt1927", "k", page, ARK27, view, no, n, iso(d), d, c, code, fr, x, ""])
    write("cens1926_communes", HDR + ["commune_no", "commune", "decree_date", "decree_date_fr",
                                      "controle_civil", "population_group", "population_group_fr",
                                      "value", "flag"], rows)
    return out


# --- cross-checks ---------------------------------------------------------
def norm(s):
    import unicodedata
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"\((l'|le|la|el|les|houmt-souk)\)", "", s)
    s = re.sub(r"\b(l'|le|la|el)\b", "", s)
    return re.sub(r"[^a-z]", "", s)


def cross_checks(A, B, CD, J, K):
    res = {}
    # a vs 1931 volume, Table IV (1926 column)
    t4 = list(csv.DictReader(open(C31 / "ind1931_t4_controle_1926_1931.csv", encoding="utf-8-sig")))
    t4 = {(norm(r["controle_civil"]), r["religion"]): int(r["value"]) for r in t4 if r["census_year"] == "1926"}
    ok = bad = 0
    diffs = []
    for n, v in A.items():
        for rel, x in (("muslim", v[14]), ("jewish", v[21])):
            y = t4.get((norm(n), rel))
            if y == x:
                ok += 1
            else:
                bad += 1
                diffs.append((n, rel, x, y))
    res["a_vs_ind1931_t4"] = (ok, bad, diffs)
    # k vs 1931 volume, Annex to Table VII (1926 column)
    t7 = list(csv.DictReader(open(C31 / "ind1931_t7annex_communes_1921_1931.csv", encoding="utf-8-sig")))
    t7 = {norm(r["commune"]): int(r["value"]) for r in t7 if r["census_year"] == "1926"}
    ok, diffs, missing = 0, [], []
    for n, (_, v) in K.items():
        y = t7.get(norm(n))
        if y is None:
            missing.append(n)
        elif y == v[9]:
            ok += 1
        else:
            diffs.append((n, v[9], y))
    extra = sorted(set(t7) - {norm(n) for n in K})
    res["k_vs_ind1931_t7annex"] = (ok, diffs, missing, extra)
    # within-yearbook consistency
    check("a French total vs b 1926 total", A_tot[0], B_tot[6])
    check("c Italy 1926 vs d total 1926", CD["c"][0]["Italie"][1], CD["d"][1][1])
    check("c Italy 1921 vs d total 1921", CD["c"][0]["Italie"][0], CD["d"][1][0])
    kk = {norm(n): v for n, (_, v) in K.items()}
    jk_ok = jk_n = 0
    for n, v in J.items():
        if norm(n) in kk:
            jk_n += 1
            jk_ok += kk[norm(n)] == v
            check(f"j {n} vs k", v, kk[norm(n)], expected_fail=n in J_MISPRINTS)
    res["j_vs_k"] = (jk_ok, jk_n)
    return res


if __name__ == "__main__":
    A, A_tot = table_a()
    B, B_tot = table_b()
    CD = table_cd()
    J = table_ij()
    K = table_k()
    X = cross_checks(A, B, CD, J, K)
    print(f"checks: {CHECKS['done']} done, {CHECKS['passed']} passed")
    for f in CHECKS["failed"]:
        print("  FAIL", f)
    for k, v in X.items():
        print(k, v)
    unexpected = [f for f in CHECKS["failed"] if f.split(":")[0] not in EXPECTED_FAILURES]
    sys.exit(1 if unexpected else 0)
