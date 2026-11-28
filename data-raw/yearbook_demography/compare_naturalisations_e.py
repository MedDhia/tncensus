"""Cell-by-cell comparison of the reprints of table e (naturalisations by
nationality, legal basis and year) with the two stored printings.

Reads the hand transcriptions transcribed/naturalisations_e_<edition>.txt
(format documented at the top of naturalisations_e_sgt1922.txt), checks each
printing against its own printed totals, and compares every cell with
csv/naturalisations_by_nationality_sgt1930.csv (editions 1922-1928) or
csv/naturalisations_by_nationality_sgt1939.csv (editions 1935, 1936).

Every reprint row is mapped explicitly to a stored nationality (LABELS, with
period-specific overrides in OVERRIDES), and every reprint column to a stored
period (stored_period); several reprint rows or columns mapped to one stored cell are
summed. Stored rows that the reprint does not print are checked to be 0 for the
compared periods ("absent rows"), not skipped. Results go to
naturalisations_e_comparison.json. Nothing in csv/ is modified.

Run: python3 data-raw/yearbook_demography/compare_naturalisations_e.py
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
TR = HERE / "transcribed"
CSV = HERE / "csv"
OUT = HERE / "naturalisations_e_comparison.json"

EDITIONS_1930 = ["sgt1922", "sgt1923", "sgt1925", "sgt1926", "sgt1927", "sgt1928"]
EDITIONS_1939 = ["sgt1935", "sgt1936"]
AGE = {"T": "total", "M": "adults", "m": "minors"}

# --- row labels -> stored nationality codes -----------------------------------
LABELS_1930 = {
    "Italiens": "italian", "Anglo-Maltais": "anglo_maltese", "Suisses": "swiss",
    "Allemands": "german", "Autrichiens": "austrian", "Espagnols": "spanish",
    "Grecs": "greek", "Hollandais": "dutch", "Portugais": "portuguese",
    "Belges": "belgian", "Norvégiens": "norwegian", "Bulgares": "bulgarian",
    "Roumains": "romanian", "Serbes": "serbian", "Polonais": "polish",
    "Russes": "russian", "Luxembourgeois": "luxembourger",
    # sgt1922/sgt1923 print "Turcs"; later editions "Turcs et Syriens".
    "Turcs": "turkish_syrian", "Turcs et Syriens": "turkish_syrian",
    "Musulmans Algériens": "algerian_muslim", "Musulmans Tunisiens": "tunisian_muslim",
    "Israélites Algériens": "algerian_jew", "Israélites Tunisiens": "tunisian_jew",
    "Israélites tunisiens": "tunisian_jew",
    # The 1922-1928 editions print 3 / 3 / 2 (1891-1898, 1899-1910 adults/minors)
    # as "Musulmans Marocains"; sgt1930 prints them as Divers (and again, as a
    # duplicate, as Indigènes catholiques, which the stored file sets to 0); the
    # sgt1924 comparison already matched Marocains with Divers.
    "Musulmans Marocains": "other",
    "Divers": "other",
    # "Musulmans Soudanais" (sgt1922, sgt1923 only): see OVERRIDES.
    "Musulmans Soudanais": "tunisian_muslim",
}
# (edition, label, reprint period) -> stored nationality, where it differs from LABELS.
# Soudanais 1891-1898 (1) is counted with the Algerians from the 1925 edition on
# (Algériens 2 + Soudanais 1 = 3); Soudanais 1923 (1 / 1, sgt1923) with the
# Tunisians (17 + 1 = 18 adults, 17 + 1 = 18 minors in sgt1925-sgt1930). All other
# Soudanais cells are ».
OVERRIDES = {
    ("sgt1922", "Musulmans Soudanais", "1891-1898"): "algerian_muslim",
    ("sgt1923", "Musulmans Soudanais", "1891-1898"): "algerian_muslim",
}
LABELS_1939 = {
    "Italiens": "italian", "Anglo-Maltais": "maltese", "Suisses": "swiss",
    "Allemands": "german", "Autrichiens": "austrian", "Espagnols": "spanish",
    "Grecs": "greek", "Hollandais": "dutch", "Portugais": "portuguese",
    "Belges": "belgian", "Norvégiens et Suédois": "norwegian_swedish",
    "Tchéco-Slovaques": "czechoslovak", "Bulgares": "bulgarian", "Hongrois": "hungarian",
    "Roumains": "romanian", "Yougo-Slaves": "yugoslav", "Turcs": "turkish",
    "Albanais": "albanian", "Polonais": "polish", "Russes": "russian",
    "Luxembourgeois": "luxembourger",
    "Algériens catholiques": "algerian_catholic", "Algériens musulmans": "algerian_muslim",
    "Algériens israélites": "algerian_jew", "Tunisiens catholiques": "tunisian_catholic",
    "Tunisiens musulmans": "tunisian_muslim", "Tunisiens israélites": "tunisian_jew",
    "Anglais": "british",
    # sgt1935/sgt1936 print a Divers row; sgt1939 replaces it by four new rows.
    # Divers is compared with the sum of those four (pseudo-code "divers_group").
    "Divers": "divers_group",
}
DIVERS_GROUP_1939 = ["moroccan", "syrian", "indochinese", "french_west_african"]

# --- reprint periods -> stored periods (summed when several map to one) -------
def stored_period(ed, period, basis):
    """(stored period, kind). kind 'exact' = the same set of years;
    'subperiod' = the reprint covers only part of the stored period."""
    if ed in ("sgt1922", "sgt1923"):
        if basis == "d1910" and period.isdigit() and 1911 <= int(period) <= 1920:
            return "1911-1920", "exact"
        if basis == "l1914":
            return "1915-1924", "subperiod"      # 1915-1922 / 1915-1923 of 1915-1924
        return period, "exact"
    if ed == "sgt1935":
        if period == "1911-1923":                 # sgt1935 heads it "De 1911 à 1923",
            return "1911-1922", "exact"           # sgt1939 "De 1911 à 1922": same column
        if basis == "l1923" and 1924 <= int(period) <= 1928:
            return "1924-1928", "exact"
        return period, "exact"
    if ed == "sgt1936":
        if basis == "l1923" and 1925 <= int(period) <= 1928:
            return "1924-1928", "missing_1924"    # sgt1936 prints no 1924 column
        return period, "exact"
    return period, "exact"


def num(tok):
    if tok == "»":
        return 0
    if tok == "?":
        return None
    if tok == "-":
        return 0          # blank cell, nothing printed
    return int(tok.replace(".", ""))


def parse(path):
    b = None
    for ln in path.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        if ln.startswith("@"):
            _, ed, views, pages = ln.split()
            b = {"edition": ed, "views": views, "pages": pages, "cols": [], "rows": {},
                 "blank": set(), "total": None, "pairs": {}}
            continue
        head, _, rest = ln.partition("|")
        head, toks = head.strip(), rest.split()
        if head == "cols":
            for t in toks:
                spec, view = t.split("@")
                period, basis, ag = spec.split("/")
                b["cols"].append((period, basis, ag, int(view)))
        elif head == "= TOTAUX":
            b["total"] = [num(t) for t in toks]
        elif head == "==":
            for t in toks:
                k, v = t.split("=")
                b["pairs"][tuple(k.split("/"))] = num(v)
        else:
            assert len(toks) == len(b["cols"]), (path.name, head, len(toks), len(b["cols"]))
            b["rows"][head] = [num(t) for t in toks]
            for i, t in enumerate(toks):
                if t == "-":
                    b["blank"].add((head, i))
    assert b["total"] is not None and len(b["total"]) == len(b["cols"]), path.name
    return b


def own_checks(b):
    out = []
    for i, (period, basis, ag, view) in enumerate(b["cols"]):
        vals = [r[i] for r in b["rows"].values()]
        pr = b["total"][i]
        if None in vals or pr is None:
            out.append({"check": f"{period} {basis} {AGE[ag]} column total", "computed": None,
                        "printed": pr, "result": "not_checkable",
                        "why": "column partly or wholly hidden in the binding"})
            continue
        out.append({"check": f"{period} {basis} {AGE[ag]} column total", "computed": sum(vals),
                    "printed": pr, "result": "pass" if sum(vals) == pr else "FAIL"})
    for (period, basis), pr in b["pairs"].items():
        ix = [i for i, c in enumerate(b["cols"]) if c[0] == period and c[1] == basis]
        tots = [b["total"][i] for i in ix]
        if pr is None:
            out.append({"check": f"{period} {basis} adults+minors pair total", "computed": None,
                        "printed": None, "result": "not_checkable", "why": "pair total hidden"})
            continue
        if None in tots:   # derive the hidden column total from the pair total
            out.append({"check": f"{period} {basis} adults+minors pair total", "computed": None,
                        "printed": pr, "result": "used_to_derive",
                        "why": f"hidden column total = {pr} - {sum(t for t in tots if t is not None)}"})
            continue
        out.append({"check": f"{period} {basis} adults+minors pair total", "computed": sum(tots),
                    "printed": pr, "result": "pass" if sum(tots) == pr else "FAIL"})
    return out


def load(name):
    with open(CSV / f"naturalisations_by_nationality_{name}.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return {(r["period"], r["legal_basis"], r["age_group"], r["nationality"]): int(r["value"]) for r in rows}


def compare(b, stored, labels, divers_group=None):
    ed = b["edition"]
    agg = defaultdict(int)          # (stored key, kind) -> reprint value
    src = defaultdict(list)         # same -> reprint cells summed
    hidden = defaultdict(list)      # stored key -> hidden reprint cells
    blank = set()
    for lab, vals in b["rows"].items():
        for i, (period, basis, ag, view) in enumerate(b["cols"]):
            nat = OVERRIDES.get((ed, lab, period), labels[lab])
            sp, kind = stored_period(ed, period, basis)
            key = (sp, basis, AGE[ag], nat)
            if vals[i] is None:
                hidden[key].append(f"{lab} {period}/{basis}/{ag}")
                continue
            agg[(key, kind)] += vals[i]
            src[(key, kind)].append(f"{lab} {period}={vals[i]}")
            if (lab, i) in b["blank"]:
                blank.add(key)

    def stored_value(key):
        sp, basis, age, nat = key
        if nat == "divers_group":
            return sum(stored[(sp, basis, age, n)] for n in divers_group)
        return stored[key]

    res = {k: {"compared": 0, "equal": 0, "different": 0, "differences": []}
           for k in ("exact", "subperiod")}
    skipped_missing_1924 = 0
    hidden_checks = []
    compared_keys = set()
    for (key, kind), v in sorted(agg.items()):
        if key in hidden:
            continue
        if kind == "missing_1924":     # sum lacks 1924: not a comparison (see derived check)
            skipped_missing_1924 += 1
            continue
        sv = stored_value(key)
        r = res[kind]
        r["compared"] += 1
        compared_keys.add(key)
        if v == sv:
            r["equal"] += 1
        else:
            r["different"] += 1
            r["differences"].append({"period": key[0], "legal_basis": key[1], "age_group": key[2],
                                     "nationality": key[3], "reprint": v, "stored": sv,
                                     "reprint_cells": src[(key, kind)],
                                     **({"blank_in_reprint": True} if key in blank else {})})
    # cells whose sum includes a hidden reprint cell: implied hidden value
    for key, cells in sorted(hidden.items()):
        kinds = [k for (kk, k) in agg if kk == key]
        visible = sum(agg[(key, k)] for k in kinds)
        hidden_checks.append({"period": key[0], "legal_basis": key[1], "age_group": key[2],
                              "nationality": key[3], "stored": stored_value(key),
                              "visible_sum": visible, "implied_hidden": stored_value(key) - visible,
                              "hidden_cells": cells})
    # stored rows that the reprint does not print, for the periods it covers
    covered = {(k[0], k[1], k[2]) for (k, _) in agg} | {(k[0], k[1], k[2]) for k in hidden}
    # nationalities this reprint actually prints (after mapping)
    mapped = {k[3] for (k, _) in agg} | {k[3] for k in hidden}
    if "divers_group" in mapped:
        mapped |= set(divers_group)
    absent = [{"period": k[0], "legal_basis": k[1], "age_group": k[2], "nationality": k[3], "stored": v}
              for k, v in sorted(stored.items()) if (k[0], k[1], k[2]) in covered and k[3] not in mapped]
    if skipped_missing_1924:
        res["not_compared_missing_1924"] = {
            "cells": skipped_missing_1924,
            "why": "sgt1936 prints 1925-1928 but no 1924 column, so its sum is not the stored "
                   "1924-1928; see derived_1924_1928_with_sgt1935_1924"}
    return res, hidden_checks, {"cells": len(absent), "nonzero": [a for a in absent if a["stored"] != 0],
                                "nationalities": sorted({a["nationality"] for a in absent})}


def printing_vs_printing(a, b):
    """Year columns printed in both a and b (same period and basis): cell by cell."""
    ca = {(c[0], c[1], c[2]): i for i, c in enumerate(a["cols"])}
    out = {"compared": 0, "equal": 0, "differences": []}
    for i, c in enumerate(b["cols"]):
        j = ca.get((c[0], c[1], c[2]))
        if j is None:
            continue
        for lab, vals in b["rows"].items():
            if lab not in a["rows"]:
                continue
            x, y = a["rows"][lab][j], vals[i]
            if x is None or y is None:
                continue
            out["compared"] += 1
            if x == y:
                out["equal"] += 1
            else:
                out["differences"].append({"period": c[0], "legal_basis": c[1], "row": lab,
                                           a["edition"]: x, b["edition"]: y})
    return out


def main():
    s30, s39 = load("sgt1930"), load("sgt1939")
    result = {"stored": {"sgt1930": "csv/naturalisations_by_nationality_sgt1930.csv",
                         "sgt1939": "csv/naturalisations_by_nationality_sgt1939.csv"},
              "mappings": {"labels_vs_sgt1930": LABELS_1930, "labels_vs_sgt1939": LABELS_1939,
                           "overrides": {" | ".join(k): v for k, v in OVERRIDES.items()},
                           "divers_group_sgt1939": DIVERS_GROUP_1939,
                           "periods": {"sgt1922/sgt1923": "years 1911..1920 (d1910) summed = 1911-1920; "
                                       "1915..1922/1923 (l1914) summed vs 1915-1924 (subperiod)",
                                       "sgt1935": "'1911-1923' (d1910) = sgt1939 '1911-1922'; "
                                       "1924..1928 summed = 1924-1928",
                                       "sgt1936": "1925..1928 summed vs 1924-1928 (no 1924 column: "
                                       "missing_1924)"}},
              "editions": {}}
    blocks = {}
    for ed in EDITIONS_1930 + EDITIONS_1939:
        b = parse(TR / f"naturalisations_e_{ed}.txt")
        blocks[ed] = b
        assert b["edition"] == ed
        if ed in EDITIONS_1930:
            res, hid, absent = compare(b, s30, LABELS_1930)
            against = "sgt1930"
        else:
            res, hid, absent = compare(b, s39, LABELS_1939, DIVERS_GROUP_1939)
            against = "sgt1939"
        checks = own_checks(b)
        result["editions"][ed] = {
            "transcription": f"transcribed/naturalisations_e_{ed}.txt",
            "views": b["views"], "pages": b["pages"], "compared_with": against,
            "printed_total_checks": {"n": len(checks),
                                     "pass": sum(c["result"] == "pass" for c in checks),
                                     "fail": [c for c in checks if c["result"] == "FAIL"],
                                     "not_checkable": [c for c in checks if c["result"] in
                                                       ("not_checkable", "used_to_derive")]},
            "cells": res,
            "hidden_cells": hid,
            "absent_rows": absent,
        }
    # sgt1936 has no 1924 column: also give its 1924-1928 with sgt1935's 1924 added,
    # and compare the year columns the two printings share.
    b35, b36 = blocks["sgt1935"], blocks["sgt1936"]
    i24 = [i for i, c in enumerate(b35["cols"]) if c[0] == "1924"][0]
    d = {"compared": 0, "equal": 0, "different": 0, "differences": []}
    i36 = [i for i, c in enumerate(b36["cols"]) if c[1] == "l1923" and 1925 <= int(c[0]) <= 1928]
    sums = defaultdict(int)
    for lab, vals in b36["rows"].items():
        sums[LABELS_1939[lab]] += sum(vals[i] for i in i36) + b35["rows"][lab][i24]
    for nat, v in sorted(sums.items()):
        sv = (sum(s39[("1924-1928", "l1923", "total", n)] for n in DIVERS_GROUP_1939)
              if nat == "divers_group" else s39[("1924-1928", "l1923", "total", nat)])
        d["compared"] += 1
        if v == sv:
            d["equal"] += 1
        else:
            d["different"] += 1
            d["differences"].append({"nationality": nat, "sgt1936_1925_1928_plus_sgt1935_1924": v,
                                     "stored": sv})
    result["editions"]["sgt1936"]["derived_1924_1928_with_sgt1935_1924"] = d
    result["sgt1935_vs_sgt1936_shared_columns"] = printing_vs_printing(b35, b36)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    for ed, r in result["editions"].items():
        c = r["cells"]
        print(f"{ed} vs {r['compared_with']}: totals {r['printed_total_checks']['pass']}/"
              f"{r['printed_total_checks']['n']} pass, {len(r['printed_total_checks']['fail'])} fail; "
              + "; ".join(f"{k}: {v['compared']} compared, {v['equal']} equal, {v['different']} different"
                          for k, v in c.items() if v.get("compared"))
              + f"; absent-row cells {r['absent_rows']['cells']} ({len(r['absent_rows']['nonzero'])} nonzero)"
              + f"; hidden {len(r['hidden_cells'])}")
    p = result["sgt1935_vs_sgt1936_shared_columns"]
    print(f"sgt1935 vs sgt1936 shared columns: {p['compared']} compared, {p['equal']} equal")


if __name__ == "__main__":
    main()
