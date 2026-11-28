"""Extract the 1931 indigenous census tables (except Table III) to tidy CSVs.

See data-raw/colonial_census/SPEC.md. Numbers are read from Gallica's word OCR
(via ocr.py's cache) and assigned to printed columns by right edge; every table
is validated against its printed totals, and cells the OCR got wrong are
corrected from the page images (see CORRECTIONS and the notes files).
"""
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ocr  # noqa: E402

ARK = ocr.ARK_1931
OUT = HERE / "csv"


def boxes(view):
    """Words with vertical centre `row`, horizontal left/right edges, text."""
    ocr.words(ARK, view)  # populate cache
    data = json.loads((ocr.CACHE / f"{ARK}_f{view:03d}.json").read_text())
    out = []
    for it in data.get("items", []):
        x, y, w, h = map(int, re.search(r"xywh=(\d+),(\d+),(\d+),(\d+)", it["target"]).groups())
        out.append({"row": x + w / 2, "left": y, "right": y + h, "text": it["body"]["value"]})
    return out


def lines(ws, tol=18):
    ws = sorted(ws, key=lambda w: w["row"])
    out = []
    for w in ws:
        if out and abs(w["row"] - sum(t["row"] for t in out[-1]) / len(out[-1])) < tol:
            out[-1].append(w)
        else:
            out.append([w])
    return [sorted(r, key=lambda w: w["left"]) for r in out]


ZERO = {"»", "))", ")", "»»", "»)", ")»", "»>", ">»", ">", ">>", ")>", "*>", "2>", "y", "».", "»,", "«", "»'", "*", "D", "b", "B", "!"}
NUMRE = re.compile(r"^\d{1,3}([.,]\d{3})*$|^\d+$")


def num_tok(t):
    """Numeric value of a token, 0 for printed '»', None otherwise."""
    t = t.strip().replace("'", "").replace("-", "")
    if t in ZERO:
        return 0
    t = t.lstrip(".")
    if t in ZERO:
        return 0
    t = re.sub(r"(?<=\d)[iIl]|[iIl](?=\d)", "1", t.replace("O", "0").replace("o", "0"))
    if t.endswith(".") and NUMRE.match(t[:-1]):
        t = t[:-1]
    if t in ZERO:
        return 0
    if NUMRE.match(t):
        return int(t.replace(".", "").replace(",", ""))
    return None


def cluster_edges(ws, min_count=4, gap=45, shift=45):
    """Right edges of right-aligned numeric columns, by clustering."""
    xs = sorted(w["right"] + (shift if w["text"].strip() in ZERO else 0)
                for w in ws if num_tok(w["text"]) is not None)
    groups = []
    for x in xs:
        if groups and x - groups[-1][-1] < gap:
            groups[-1].append(x)
        else:
            groups.append([x])
    return [sorted(g)[len(g) // 2] for g in groups if len(g) >= min_count]


def merge_split(line, gap=60):
    """Join '1 034' style numbers that OCR split at the thousands space."""
    out = []
    for w in line:
        if (out and re.fullmatch(r"\d{3}", w["text"].strip())
                and re.fullmatch(r"\d{1,3}([.,]\d{3})*", out[-1]["text"].strip())
                and 0 <= w["left"] - out[-1]["right"] < gap and abs(w["row"] - out[-1]["row"]) < 30):
            p = dict(out[-1])
            p["text"] = p["text"].strip() + "." + w["text"].strip()
            p["right"] = w["right"]
            out[-1] = p
        else:
            out.append(w)
    return out


def assign(line, edges, zero_shift=45, tol=95, label_max=None):
    """Map tokens of one printed line to columns (by nearest right edge).

    Returns (cells, label_tokens, stray) where cells[i] is the int value or None.
    Several numeric tokens in one column are concatenated (OCR split '1 034').
    """
    line = merge_split(sorted(line, key=lambda w: w["left"]))
    cells = [[] for _ in edges]
    label, stray = [], []
    first = label_max if label_max is not None else edges[0] - 260
    for w in line:
        v = num_tok(w["text"])
        r = w["right"] + (zero_shift if w["text"].strip() in ZERO else 0)
        if w["right"] < first:
            label.append(w)
            continue
        d = [abs(r - e) for e in edges]
        i = min(range(len(edges)), key=d.__getitem__)
        if d[i] > tol or v is None:
            stray.append(w)
            continue
        cells[i].append(w)
    out = []
    for c in cells:
        if not c:
            out.append(None)
        elif len(c) == 1:
            out.append(num_tok(c[0]["text"]))
        else:
            digits = "".join(re.sub(r"\D", "", t["text"]) for t in c)
            out.append(int(digits) if digits else 0)
    return out, label, stray


def spread_rows(view, edges, row_min, row_max, split=None, tol=18, ptol=40, label_max=None):
    """Printed rows of a two-page spread, joining each left-page line with its
    right-page continuation (the right page is printed slightly offset).

    Returns a list of dicts: row (position), label (str), cells (list, one per
    edge), stray (unassigned tokens), raw (tokens).
    """
    ws = [w for w in boxes(view) if row_min <= w["row"] <= row_max]
    if split is None:
        gaps = [(edges[i + 1] - edges[i], i) for i in range(1, len(edges) - 1)]
        _, i = max(gaps)
        split = (edges[i] + edges[i + 1]) / 2 - 150
    L = lines([w for w in ws if w["left"] < split], tol)
    R = lines([w for w in ws if w["left"] >= split], tol)
    rpos = lambda ln: sum(w["row"] for w in ln) / len(ln)
    diffs = []
    for l in L:
        if R:
            r = min(R, key=lambda r: abs(rpos(r) - rpos(l)))
            diffs.append(rpos(r) - rpos(l))
    off = sorted(diffs)[len(diffs) // 2] if diffs else 0
    used, out = set(), []
    for l in L:
        cand = [(abs(rpos(r) - rpos(l) - off), j) for j, r in enumerate(R) if j not in used]
        tokens = list(l)
        if cand:
            d, j = min(cand)
            if d < ptol:
                used.add(j)
                tokens += R[j]
        cells, lab, stray = assign(tokens, edges, label_max=label_max)
        out.append({"row": rpos(l), "label": label_text(lab), "cells": cells, "stray": stray, "raw": tokens})
    for j, r in enumerate(R):
        if j not in used:
            cells, lab, stray = assign(r, edges, label_max=label_max)
            out.append({"row": rpos(r) - off, "label": "", "cells": cells, "stray": stray, "raw": r, "orphan_right": True})
    return sorted(out, key=lambda d: d["row"])


def label_text(tokens):
    t = " ".join(w["text"] for w in tokens)
    t = re.sub(r"\.{2,}.*$", "", t)          # leader dots
    t = re.sub(r"^\d{1,3}\s+", "", t)        # order number
    t = re.sub(r"\s*\.+\s*$", "", t)
    return t.strip(" .:")


def write_csv(name, rows, cols):
    OUT.mkdir(exist_ok=True)
    with open(OUT / name, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})
    print(f"wrote {name}: {len(rows)} rows")


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "dump":
    v = int(sys.argv[2])
    lo = float(sys.argv[3]) if len(sys.argv) > 3 else 0
    for r in lines(boxes(v)):
        if r[0]["row"] >= lo:
            print(f"{r[0]['row']:.0f}: " + " ".join(f"{w['text']}|{w['right']}" for w in r))
    sys.exit()


def page_rows(view, edges, row_min, row_max, tol=22, label_cut=230, text_gap=70):
    """Rows of a single-page table: label (left text), numeric cells, and the
    trailing text column (e.g. caidat) right of the last numeric column."""
    ws = [w for w in boxes(view) if row_min <= w["row"] <= row_max]
    out = []
    for ln in lines(ws, tol):
        right_txt = [w for w in ln if w["left"] > edges[-1] + text_gap]
        rest = [w for w in ln if w not in right_txt]
        cells, lab, stray = assign(rest, edges, label_max=edges[0] - label_cut)
        out.append({"row": sum(w["row"] for w in ln) / len(ln), "label": label_text(lab), "cells": cells,
                    "right": " ".join(w["text"] for w in right_txt).strip(), "stray": stray})
    return out


# --------------------------------------------------------------------------
# Common
# --------------------------------------------------------------------------
NATS = [("tunisian", "Tunisiens"), ("algerian", "Algériens"), ("moroccan", "Marocains"),
        ("sudanese", "Soudanais"), ("syrian", "Syriens"), ("tripolitanian", "Tripolitains"),
        ("other", "Autres nationalités")]
RELIGIONS = [("muslim", "Population musulmane"), ("jewish", "Population israélite")]
BASE = ["census", "table_id", "source_page", "gallica_view"]
LOG = {}   # table -> dict of validation counts


def log(table, key, n=1):
    LOG.setdefault(table, {}).setdefault(key, 0)
    LOG[table][key] += n


def fill_zero_if_balanced(cells, groups, table):
    """Cells the OCR left empty are '»' in the image (checked visually for the
    pages concerned); fill them with 0 when that makes the printed row totals
    balance. `groups` is a list of (part_indices, total_index).
    Returns the set of filled indices."""
    filled = set()
    for parts, tot in groups:
        miss = [i for i in parts if cells[i] is None]
        if miss and cells[tot] is not None and sum(cells[i] or 0 for i in parts) == cells[tot]:
            for i in miss:
                cells[i] = 0
                filled.add(i)
    if filled:
        log(table, "empty_ocr_cells_filled_0", len(filled))
    return filled


def check_rows(cells, groups):
    return all(None not in [cells[i] for i in parts + [tot]] and sum(cells[i] for i in parts) == cells[tot]
               for parts, tot in groups)


# --------------------------------------------------------------------------
# Tables I and II: nationality x religion by contrôle civil / caidat
# --------------------------------------------------------------------------
NAT_GROUPS = [(list(range(0, 7)), 7), (list(range(8, 15)), 15), ([7, 15], 16)]

# (table, unit label as printed, column index) -> value read from the image
CORRECTIONS = {
    ("I", "Tozeur", 15): 347,       # OCR '317'; image '347' (335 + 12)
    ("II", "Gafsa", 0): 49553,      # OCR missed; image '49.553'
    ("II", "Kairouan", 4): 1,       # OCR put '1' on its own line; image '1'
    ("IV", "Medjez-El-Bab", 8): 7089,   # OCR '89' (+ 'T'); image '+ 7.089'
    ("VI", "Matmata", 4): 64,            # OCR '4'; image '64'
    ("VI", "Souk-El-Khemis", 6): 74,     # OCR missed; image '74'
    ("VI", "Tadjerouine", 14): 0,        # OCR '9' (stray); image '»'
    ("V", "Fraichiches", 10): 39085,
    ("VIII", "Beni-Khalled", 0): 3273,   # OCR '3.278'; image '3.273' (3.273 + 45 = 3.318)
    ("VIII", "Berghouthia", 2): 208,     # OCR '20S'; image '208'
    ("VIII", "Zaghdoud", 2): 202,        # OCR 'CM O'; image '202'

    ("VII", "Djerba", 2): 4341,          # OCR '4.34J'; image '4.341'
    ("VII", "Soliman", 1): 137,          # OCR '37' ('j' stray); image '137'
    ("VII_annex", "Carthage", 1): 666,   # OCR '606'; image '666'
    ("VII_annex", "El-Djem", 0): 0,      # printed '»'
    ("VII_annex", "Hadjeb-El-Aïoun", 0): 0,
    ("VII_annex", "Saint-Germain", 0): 0,
    ("VII_annex", "Saint-Germain", 2): 0,
    ("VII_annex", "Sbeïtla", 0): 0,
    ("VII_annex", "Sbeïtla", 1): 0,    # OCR "39.0^5"; image "39.085"
}


def apply_corrections(table_id, lab, cells):
    fixed = set()
    for (t, l, i), v in CORRECTIONS.items():
        if t == table_id and l == lab:
            cells[i] = v
            fixed.add(i)
    if fixed:
        log(table_id, "cells_corrected_from_image", len(fixed))
    return fixed
LABEL_FIX = {"Bize'rte": "Bizerte", "Djèrba": "Djerba"}


# Unit names as printed (read from the page images), in print order.
T1_UNITS = ["Béja", "Bizerte", "Djerba", "Gabès", "Gafsa", "Grombalia", "Kairouan", "Le Kef",
            "Maktar", "Medjez-el-Bab", "Sfax", "Souk-el-Arba", "Sousse", "Tabarka", "Thala",
            "Téboursouk", "Tozeur", "Tunis", "Zaghouan", "Territoires militaires"]
T2_UNITS = ["Aïn-Draham", "Aradh", "Béja", "Bizerte", "Djebeniana", "Djelass", "Djerba", "Djerid",
            "Fraichiches", "Gafsa", "Hammama", "Kairouan", "La Skhira", "Le Kef", "Madjeurs",
            "Mahdia", "Mateur", "Matmata", "Medjez-el-Bab", "Monastir", "Nabeul", "Nefzaoua",
            "Ouerghemma", "Oulad-Aoun", "Oulad-Ayar", "Sfax", "Soliman", "Souassi", "Souk-el-Arba",
            "Souk-el-Khemis", "Sousse", "Tadjerouine", "Tatahouine", "Téboursouk", "Tunis-Banlieue",
            "Tunis-Ville", "Zaghouan"]


def nat_table(table_id, views, pages, row_window, geo_col, fname, names, tol=18):
    rows_out, units, sums = [], [], [0] * 17
    queue = list(names)
    printed_total = None
    for view, (pl, pr) in zip(views, pages):
        ws = [w for w in boxes(view) if row_window[0] <= w["row"] <= row_window[1]]
        edges = cluster_edges(ws)
        edges = [e for e in edges if e > 900]          # drop the order-number column
        assert len(edges) == 17, (view, edges)
        for r in spread_rows(view, edges, *row_window, label_max=edges[0] - 250, tol=tol):
            lab = LABEL_FIX.get(r["label"], r["label"])
            c = r["cells"]
            low = lab.lower()
            if not ("report" in low or low.startswith("totaux")) and sum(v is not None for v in c) >= 8:
                lab = queue.pop(0)   # data row: take the next printed unit name
            elif not ("report" in low or low.startswith("totaux")):
                print(table_id, "skipped fragment", r["label"], c)
                continue
            if "report" in low:            # carry-forward lines: check running sums
                if None not in c:
                    log(table_id, "carry_forward_checks")
                    if c == sums:
                        log(table_id, "carry_forward_passed")
                    else:
                        print(table_id, "carry-forward mismatch", lab, c, sums)
                continue
            if low.startswith("totaux"):
                printed_total = c
                continue
            r["corr"] = apply_corrections(table_id, lab, c)
            filled = fill_zero_if_balanced(c, NAT_GROUPS, table_id)
            log(table_id, "row_checks")
            if check_rows(c, NAT_GROUPS):
                log(table_id, "row_checks_passed")
            else:
                print(table_id, "ROW FAIL", lab, c, [w["text"] for w in r["stray"]])
            units.append(lab)
            sums = [a + (b or 0) for a, b in zip(sums, c)]
            for ri, (rel, rel_fr) in enumerate(RELIGIONS):
                for ni, (nat, nat_fr) in enumerate(NATS):
                    idx = ri * 8 + ni
                    flag = "ocr_corrected" if idx in r.get("corr", set()) | filled else ""
                    rows_out.append({"census": "ind1931", "table_id": table_id,
                                     "source_page": pl if ri == 0 else pr, "gallica_view": view,
                                     geo_col: lab, "religion": rel, "religion_fr": rel_fr,
                                     "nationality": nat, "nationality_fr": nat_fr,
                                     "value": c[idx], "flag": flag})
    log(table_id, "column_total_checks", 17)
    ok = sum(a == b for a, b in zip(sums, printed_total))
    log(table_id, "column_total_passed", ok)
    if ok != 17:
        print(table_id, "COLUMN TOTAL mismatch", sums, printed_total)
    assert not queue, queue
    write_csv(fname, rows_out, BASE + [geo_col, "religion", "religion_fr", "nationality",
                                       "nationality_fr", "value", "flag"])
    return units


def table_1():
    return nat_table("I", [8], [(6, 7)], (1350, 3420), "controle_civil",
                     "ind1931_t1_controle_nationality.csv", T1_UNITS)


def table_2():
    return nat_table("II", [9, 10], [(8, 9), (10, 11)], (1300, 3500), "caidat",
                     "ind1931_t2_caidat_nationality.csv", T2_UNITS, tol=30)


# --------------------------------------------------------------------------
# Table IV: 1926 vs 1931 by contrôle civil; Annex IV: by nationality
# --------------------------------------------------------------------------
T4_UNITS = ["Béja", "Bizerte", "Djerba", "Gabès", "Gafsa", "Grombalia", "Kairouan", "Le Kef",
            "Maktar", "Medjez-El-Bab", "Sfax", "Souk-El-Arba", "Sousse", "Tabarka", "Thala",
            "Téboursouk", "Tozeur", "Tunis", "Zaghouan", "Territoires Militaires"]


def read_csv(name):
    with open(OUT / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def table_4():
    t = "IV"
    view = 54
    ws = [w for w in boxes(view) if 1200 <= w["row"] <= 3300]
    edges = [e for e in cluster_edges(ws) if e > 900]
    assert len(edges) == 9, edges
    # 1931 totals per contrôle from Table I, for cross-checking
    t1 = {}
    for r in read_csv("ind1931_t1_controle_nationality.csv"):
        t1.setdefault((T1_UNITS.index(r["controle_civil"]), r["religion"]), 0)
        t1[(T1_UNITS.index(r["controle_civil"]), r["religion"])] += int(r["value"])
    queue, out, sums, printed = list(T4_UNITS), [], [0] * 9, None
    for r in spread_rows(view, edges, 1200, 3300, label_max=edges[0] - 300, tol=22):
        c = r["cells"]
        if r["label"].lower().startswith("totaux"):
            printed = c
            continue
        if sum(v is not None for v in c) < 5:
            continue
        lab = queue.pop(0)
        i = T4_UNITS.index(lab)
        corr = apply_corrections(t, lab, c)
        checks = [None not in (c[a], c[b], c[d]) and abs(c[b] - c[a]) == c[d]
                  for a, b, d in ((0, 1, 2), (3, 4, 5), (6, 7, 8))]
        checks.append(None not in c and c[0] + c[3] == c[6] and c[1] + c[4] == c[7])
        log(t, "row_checks", len(checks))
        log(t, "row_checks_passed", sum(checks))
        if not all(checks):
            print(t, "ROW FAIL", lab, c, [w["text"] for w in r["stray"]])
        log(t, "crosscheck_table_I", 2)
        if c[1] == t1[(i, "muslim")] and c[4] == t1[(i, "jewish")]:
            log(t, "crosscheck_table_I_passed", 2)
        else:
            print(t, "T1 mismatch", lab, c[1], c[4], t1[(i, "muslim")], t1[(i, "jewish")])
        sums = [a + b for a, b in zip(sums, c)]
        for ri, (rel, rel_fr) in enumerate(RELIGIONS):
            for yi, year in enumerate((1926, 1931)):
                out.append({"census": "ind1931", "table_id": t, "source_page": 98 if ri == 0 else 99,
                            "gallica_view": view, "controle_civil": lab, "religion": rel,
                            "religion_fr": rel_fr, "census_year": year, "value": c[ri * 3 + yi],
                            "flag": "ocr_corrected" if ri * 3 + yi in corr else ""})
    assert not queue, queue
    for k in (0, 1, 3, 4, 6, 7):
        log(t, "column_total_checks")
        if sums[k] == printed[k]:
            log(t, "column_total_passed")
        else:
            print(t, "COLUMN mismatch", k, sums[k], printed[k])
    write_csv("ind1931_t4_controle_1926_1931.csv", out,
              BASE + ["controle_civil", "religion", "religion_fr", "census_year", "value", "flag"])


# Annex IV (p.100, printed rotated 90°): transcribed from the image.
# columns: muslim 1926, muslim 1931, jewish 1926, jewish 1931, total 1926, total 1931
T4A = [
    ("Tunisiens", 1864908, 2086762, 53022, 55340, 1917930, 2142102),
    ("Algériens", 39882, 40734, 81, 185, 39963, 40919),
    ("Marocains", 3571, 2854, 36, 34, 3607, 2888),
    ("Soudanais", 296, 445, 0, 0, 296, 445),
    ("Syriens", 26, 140, 15, 28, 41, 168),
    ("Tripolitains", 20305, 28157, 615, 556, 20920, 28713),
    ("Autres nationalités", 3196, 59, 474, 105, 3670, 164),
]
T4A_TOTAL = (1932184, 2159151, 54243, 56248, 1986427, 2215399)


def table_4annex():
    t = "IV_annex"
    nat_of = {fr: en for en, fr in NATS}
    out = []
    for row in T4A:
        fr, v = row[0], row[1:]
        log(t, "row_checks", 2)
        log(t, "row_checks_passed", (v[0] + v[2] == v[4]) + (v[1] + v[3] == v[5]))
        for ri, (rel, rel_fr) in enumerate(RELIGIONS):
            for yi, year in enumerate((1926, 1931)):
                out.append({"census": "ind1931", "table_id": t, "source_page": 100, "gallica_view": 55,
                            "religion": rel, "religion_fr": rel_fr, "nationality": nat_of[fr],
                            "nationality_fr": fr, "census_year": year, "value": v[ri * 2 + yi], "flag": ""})
    for k in range(6):
        log(t, "column_total_checks")
        log(t, "column_total_passed", sum(r[k + 1] for r in T4A) == T4A_TOTAL[k])
    # 1931 by nationality must equal the Table I column totals
    t1 = {}
    for r in read_csv("ind1931_t1_controle_nationality.csv"):
        t1[(r["religion"], r["nationality"])] = t1.get((r["religion"], r["nationality"]), 0) + int(r["value"])
    for row in T4A:
        n = nat_of[row[0]]
        log(t, "crosscheck_table_I", 2)
        log(t, "crosscheck_table_I_passed", (row[2] == t1[("muslim", n)]) + (row[4] == t1[("jewish", n)]))
    write_csv("ind1931_t4annex_nationality_1926_1931.csv", out,
              BASE + ["religion", "religion_fr", "nationality", "nationality_fr", "census_year", "value", "flag"])


# --------------------------------------------------------------------------
# Generic spread table with carry-forward lines and printed totals
# --------------------------------------------------------------------------
def spread_table(table_id, views, row_windows, ncols, groups, names=None, tol=22, min_cells=None,
                 label_cut=250, edge_min=900, edges_override=None):
    """Yield (view, unit label, cells, corrected-or-filled indices) for each data row,
    validating rows, carry-forward ('A reporter'/'Report') lines and the final
    'Totaux' line. If `names` is given, data rows take those names in order."""
    queue = list(names) if names else None
    sums, printed = [0] * ncols, None
    min_cells = min_cells or ncols // 2
    out = []
    for view, win in zip(views, row_windows):
        ws = [w for w in boxes(view) if win[0] <= w["row"] <= win[1]]
        edges = edges_override.get(view) if edges_override else None
        edges = edges or [e for e in cluster_edges(ws) if e > edge_min]
        assert len(edges) == ncols, (table_id, view, edges)
        for r in spread_rows(view, edges, *win, label_max=edges[0] - label_cut, tol=tol):
            lab, c = r["label"], r["cells"]
            low = lab.lower().replace(" ", "")
            if "report" in low:
                if None not in c:
                    log(table_id, "carry_forward_checks")
                    if c == sums:
                        log(table_id, "carry_forward_passed")
                    else:
                        print(table_id, "carry-forward mismatch", lab, [(i, a, b) for i, (a, b) in enumerate(zip(c, sums)) if a != b])
                continue
            if low.startswith("totaux") or low.startswith("total"):
                printed = c
                continue
            if sum(v is not None for v in c) < min_cells:
                if any(v is not None for v in c) or lab:
                    print(table_id, "skipped fragment", repr(lab), c)
                continue
            if queue is not None:
                lab = queue.pop(0)
            corr = apply_corrections(table_id, lab, c)
            filled = fill_zero_if_balanced(c, groups, table_id)
            log(table_id, "row_checks")
            if check_rows(c, groups):
                log(table_id, "row_checks_passed")
            else:
                print(table_id, "ROW FAIL", lab, c, [w["text"] for w in r["stray"]])
            sums = [a + (b or 0) for a, b in zip(sums, c)]
            out.append((view, lab, c, corr | filled))
    if queue:
        print(table_id, "UNUSED NAMES", queue)
    if printed is None:
        print(table_id, "no printed total found")
    else:
        log(table_id, "column_total_checks", ncols)
        ok = sum(a == b for a, b in zip(sums, printed))
        log(table_id, "column_total_passed", ok)
        if ok != ncols:
            print(table_id, "COLUMN TOTAL mismatch", [(i, a, b) for i, (a, b) in enumerate(zip(sums, printed)) if a != b])
    return out


def caidat_totals_t2():
    t = {}
    for r in read_csv("ind1931_t2_caidat_nationality.csv"):
        k = (T2_UNITS.index(r["caidat"]), r["religion"])
        t[k] = t.get(k, 0) + int(r["value"])
    return t


# --------------------------------------------------------------------------
# Table V: sex and age by caidat; Annex V
# --------------------------------------------------------------------------
SEXAGE = [("male", "adult_18_plus", "Hommes"), ("female", "adult_18_plus", "Femmes"),
          ("male", "child_under_18", "Garçons"), ("female", "child_under_18", "Filles")]
T5_GROUPS = [([0, 1, 2, 3], 4), ([5, 6, 7, 8], 9), ([4, 9], 10)]


def table_5():
    t = "V"
    rows = spread_table(t, [57, 58], [(1250, 3400), (1150, 3400)], 11, T5_GROUPS)
    t2 = caidat_totals_t2()
    out = []
    assert len(rows) == 37, len(rows)
    for k, (view, lab, c, fl) in enumerate(rows):
        name = T5_NAMES[k]
        log(t, "crosscheck_table_II", 2)
        good = (c[4] == t2[(k, "muslim")]) + (c[9] == t2[(k, "jewish")])
        log(t, "crosscheck_table_II_passed", good)
        if good != 2:
            print(t, "T2 mismatch", name, c[4], c[9], t2[(k, "muslim")], t2[(k, "jewish")])
        for ri, (rel, rel_fr) in enumerate(RELIGIONS):
            for si, (sex, age, fr) in enumerate(SEXAGE):
                idx = ri * 5 + si
                out.append({"census": "ind1931", "table_id": t,
                            "source_page": {57: 102, 58: 104}[view] + ri, "gallica_view": view,
                            "caidat": name, "religion": rel, "religion_fr": rel_fr, "sex": sex,
                            "age_group": age, "category_fr": fr, "value": c[idx],
                            "flag": "ocr_corrected" if idx in fl else ""})
    write_csv("ind1931_t5_caidat_sex_age.csv", out,
              BASE + ["caidat", "religion", "religion_fr", "sex", "age_group", "category_fr", "value", "flag"])
    return [r[1] for r in rows]


# Annex V (p.106, printed rotated 90°), transcribed from the image.
# muslim 1926, 1931, jewish 1926, 1931, total 1926, 1931
T5A = [("Hommes", 510112, 563791, 14033, 15008, 524145, 578799),
       ("Femmes", 491853, 540408, 13839, 15132, 505692, 555540),
       ("Garçons", 489506, 551901, 12863, 12869, 502369, 564770),
       ("Filles", 440713, 503051, 13508, 13239, 454221, 516290)]
T5A_TOTAL = (1932184, 2159151, 54243, 56248, 1986427, 2215399)


def table_5annex():
    t = "V_annex"
    out = []
    lookup = {fr: (sex, age) for sex, age, fr in SEXAGE}
    for row in T5A:
        fr, v = row[0], row[1:]
        log(t, "row_checks", 2)
        log(t, "row_checks_passed", (v[0] + v[2] == v[4]) + (v[1] + v[3] == v[5]))
        for ri, (rel, rel_fr) in enumerate(RELIGIONS):
            for yi, year in enumerate((1926, 1931)):
                out.append({"census": "ind1931", "table_id": t, "source_page": 106, "gallica_view": 59,
                            "religion": rel, "religion_fr": rel_fr, "sex": lookup[fr][0],
                            "age_group": lookup[fr][1], "category_fr": fr, "census_year": year,
                            "value": v[ri * 2 + yi], "flag": ""})
    for k in range(6):
        log(t, "column_total_checks")
        log(t, "column_total_passed", sum(r[k + 1] for r in T5A) == T5A_TOTAL[k])
    t5 = {}
    for r in read_csv("ind1931_t5_caidat_sex_age.csv"):
        k = (r["religion"], r["category_fr"])
        t5[k] = t5.get(k, 0) + int(r["value"])
    for row in T5A:
        log(t, "crosscheck_table_V", 2)
        log(t, "crosscheck_table_V_passed", (row[2] == t5[("muslim", row[0])]) + (row[4] == t5[("jewish", row[0])]))
    write_csv("ind1931_t5annex_sex_age_1926_1931.csv", out,
              BASE + ["religion", "religion_fr", "sex", "age_group", "category_fr", "census_year", "value", "flag"])


# --------------------------------------------------------------------------
# Table VI: occupations of adult males (18+) by caidat; Annex VI
# --------------------------------------------------------------------------
PROFS = [("agriculture", "Agriculteurs"), ("commerce", "Commerçants"), ("industry", "Industriels"),
         ("day_labourers", "Ouvriers journaliers"), ("transport", "Agents de transport"),
         ("public_service", "Fonctionnaires et employés des Administrations et Établissements publics"),
         ("liberal_professions", "Professions libérales"), ("unclassified", "Population non classée")]


def table_6():
    t = "VI"
    w61 = [w for w in boxes(61) if 1150 <= w["row"] <= 3500]
    e61 = [e for e in cluster_edges(w61) if e > 1150]
    rows = spread_table(t, [61, 62], [(1150, 2900), (1280, 2900)], 16, [],
                        names=T6_NAMES, edges_override={61: e61})
    men = {}
    for r in read_csv("ind1931_t5_caidat_sex_age.csv"):
        if r["sex"] == "male" and r["age_group"] == "adult_18_plus":
            men[(T5_NAMES.index(r["caidat"]), r["religion"])] = int(r["value"])
    out = []
    assert len(rows) == 37, len(rows)
    for k, (view, lab, c, fl) in enumerate(rows):
        ext = c + [men[(k, "muslim")], men[(k, "jewish")]]
        groups = [(list(range(0, 8)), 16), (list(range(8, 16)), 17)]
        fl = fl | fill_zero_if_balanced(ext, groups, t)
        c = ext[:16]
        log(t, "crosscheck_table_V_adult_men", 2)
        good = sum(None not in ext[a:a + 8] and sum(ext[a:a + 8]) == ext[16 + a // 8] for a in (0, 8))
        log(t, "crosscheck_table_V_adult_men_passed", good)
        if good != 2:
            print(t, "T5 mismatch", lab, c, ext[16:])
        for ri, (rel, rel_fr) in enumerate(RELIGIONS):
            for pi, (prof, prof_fr) in enumerate(PROFS):
                idx = ri * 8 + pi
                page = {61: 108, 62: 110}[view] + (0 if idx < 6 else 1)
                out.append({"census": "ind1931", "table_id": t, "source_page": page, "gallica_view": view,
                            "caidat": lab, "religion": rel, "religion_fr": rel_fr, "sex": "male",
                            "age_group": "adult_18_plus", "occupation": prof, "occupation_fr": prof_fr,
                            "value": c[idx], "flag": "ocr_corrected" if idx in fl else ""})
    write_csv("ind1931_t6_caidat_profession.csv", out,
              BASE + ["caidat", "religion", "religion_fr", "sex", "age_group", "occupation", "occupation_fr",
                      "value", "flag"])


# Annex VI (p.112, printed rotated 90°), transcribed from the image.
T6A = [("Agriculteurs", 318828, 338991, 56, 108, 318884, 339099),
       ("Commerçants", 21460, 23744, 7256, 6919, 28716, 30663),
       ("Industriels", 18502, 19405, 2913, 4075, 21415, 23480),
       ("Ouvriers journaliers", 119452, 149598, 2045, 1669, 121497, 151267),
       ("Agents de transport", 7313, 8100, 235, 330, 7548, 8430),
       ("Fonctionnaires et employés des Administrations et Établissements publics", 5308, 5873, 48, 33, 5356, 5906),
       ("Professions libérales", 6813, 6574, 921, 1273, 7734, 7847),
       ("Population non classée", 12436, 11506, 559, 601, 12995, 12107)]
T6A_TOTAL = (510112, 563791, 14033, 15008, 524145, 578799)


def table_6annex():
    t = "VI_annex"
    code = {fr: en for en, fr in PROFS}
    t6 = {}
    for r in read_csv("ind1931_t6_caidat_profession.csv"):
        t6[(r["religion"], r["occupation"])] = t6.get((r["religion"], r["occupation"]), 0) + int(r["value"])
    out = []
    for row in T6A:
        fr, v = row[0], row[1:]
        log(t, "row_checks", 2)
        log(t, "row_checks_passed", (v[0] + v[2] == v[4]) + (v[1] + v[3] == v[5]))
        log(t, "crosscheck_table_VI", 2)
        log(t, "crosscheck_table_VI_passed", (v[1] == t6[("muslim", code[fr])]) + (v[3] == t6[("jewish", code[fr])]))
        for ri, (rel, rel_fr) in enumerate(RELIGIONS):
            for yi, year in enumerate((1926, 1931)):
                out.append({"census": "ind1931", "table_id": t, "source_page": 112, "gallica_view": 63,
                            "religion": rel, "religion_fr": rel_fr, "sex": "male", "age_group": "adult_18_plus",
                            "occupation": code[fr], "occupation_fr": fr, "census_year": year,
                            "value": v[ri * 2 + yi], "flag": ""})
    for k in range(6):
        log(t, "column_total_checks")
        log(t, "column_total_passed", sum(r[k + 1] for r in T6A) == T6A_TOTAL[k])
    write_csv("ind1931_t6annex_profession_1926_1931.csv", out,
              BASE + ["religion", "religion_fr", "sex", "age_group", "occupation", "occupation_fr",
                      "census_year", "value", "flag"])


# --------------------------------------------------------------------------
# Table VII: communes (Muslim / Jewish / total, caidat); Annex VII: 1921/1926/1931
# --------------------------------------------------------------------------
# Commune names as printed in Table VII (pp.113-114), read from the images.
T7_NAMES = ["Aïn-Draham", "Ariana (L')", "Bardo", "Ben-Gardane", "Béja", "Bizerte", "Carthage", "Djemmal",
            "Djerba", "Ebba-Ksour", "El-Djem", "Ferryville", "Feriana", "Foum-Tatahouine", "Gabès", "Gafsa",
            "Ghardimaou", "Goulette (La)", "Grombalia", "Hadjeb-El-Aïoun", "Hammam-Lif", "Hamma (El)",
            "Kairouan", "Kalaâ-Kebira", "Kef (Le)", "Krib (Le)", "Ksour-Essaf", "Maharès", "Mahdia",
            "Marsa (La)", "Mateur", "Maxula-Radès", "Médenine", "Medjez-El-Bab", "M'Saken", "Menzel-Bou-Zelfa",
            "Menzel-Temime", "Moknine", "Monastir", "Nabeul", "Nefta", "Philippe-Thomas", "Saint-Germain",
            "Sbeïtla", "Sfax", "Sidi-Bou-Saïd", "Soliman", "Souk-El-Arba", "Souk-El-Khemis", "Sousse",
            "Tabarka", "Thala", "Tébourba", "Téboursouk", "Tunis", "Tozeur", "Zaghouan", "Zarzis"]
# Caidat column as printed ('—' = no caidat printed).
T7_CAIDATS = ["Aïn-Draham", "Tunis-Banlieue", "—", "Ouerghemma", "Béja", "Bizerte", "Tunis-Banlieue",
              "Monastir", "Djerba", "Le Kef", "Mahdia", "Bizerte", "Madjeurs", "Tatahouine", "Aradh", "Gafsa",
              "Souk-El-Arba", "Tunis-Banlieue", "Soliman", "Djelass", "Tunis-Banlieue", "Aradh", "Kairouan",
              "Sousse", "Le Kef", "Téboursouk", "Mahdia", "La Skhira", "Mahdia",
              "Tunis-Banlieue", "Mateur", "Tunis-Banlieue", "Ouerghemma", "Medjez-El-Bab", "Sousse", "Soliman",
              "Nabeul", "Monastir", "—", "Nabeul", "Djerid", "Gafsa", "Tunis-Banlieue", "Madjeurs", "Sfax",
              "Tunis-Banlieue", "Soliman", "Souk-El-Arba", "Souk-El-Khemis", "Sousse", "Aïn-Draham",
              "Fraichiches", "Tunis-Banlieue", "Téboursouk", "Tunis", "Djerid", "Zaghouan", "Ouerghemma"]
# Annex VII spells a few names differently (pp.115-116).
T7A_SPELLING = {"Ariana (L')": "Ariana", "Feriana": "Fériana", "Kalaâ-Kebira": "Kalaâ-Kébira"}


def single_table(table_id, views, edges, names, row_min=1300, row_max=4000, groups=()):
    queue, out = list(names), []
    for view in views:
        for r in page_rows(view, edges[view], row_min, row_max):
            c = r["cells"]
            if sum(v is not None for v in c) < 2 and not any(r["label"] for _ in [0]):
                continue
            if sum(v is not None for v in c) < 1:
                continue
            if not queue:
                print(table_id, "extra row", r)
                continue
            lab = queue.pop(0)
            corr = apply_corrections(table_id, lab, c)
            filled = fill_zero_if_balanced(c, list(groups), table_id) if groups else set()
            if groups:
                log(table_id, "row_checks")
                if check_rows(c, list(groups)):
                    log(table_id, "row_checks_passed")
                else:
                    print(table_id, "ROW FAIL", lab, c, [w["text"] for w in r["stray"]])
            if None in c:
                print(table_id, "MISSING", lab, c, [w["text"] for w in r["stray"]])
            out.append((view, lab, c, corr | filled, r))
    if queue:
        print(table_id, "UNUSED NAMES", queue)
    return out


def table_7():
    t = "VII"
    rows = single_table(t, [64, 65], {64: [1201, 1502, 1806], 65: [1367, 1666, 1976]}, T7_NAMES,
                        groups=[([0, 1], 2)])
    out = []
    for k, (view, lab, c, fl, r) in enumerate(rows):
        caid = T7_CAIDATS[k]
        mism = c[0] + c[1] != c[2]   # Tébourba: printed 3.107 + 42 != 3.128 (checked on the image)
        if mism:
            log(t, "printed_inconsistencies_kept")
        for ri, (rel, rel_fr) in enumerate(RELIGIONS):
            out.append({"census": "ind1931", "table_id": t, "source_page": {64: 113, 65: 114}[view],
                        "gallica_view": view, "commune": lab, "caidat": "" if caid == "—" else caid,
                        "religion": rel, "religion_fr": rel_fr, "value": c[ri],
                        "flag": "total_mismatch" if mism else ("ocr_corrected" if ri in fl else "")})
    write_csv("ind1931_t7_communes.csv", out,
              BASE + ["commune", "caidat", "religion", "religion_fr", "value", "flag"])
    return {lab: c[2] for _, lab, c, _, _ in rows}


def table_7annex():
    t = "VII_annex"
    t7 = table_7()
    names = [T7A_SPELLING.get(n, n) for n in T7_NAMES]
    rows = single_table(t, [66, 67], {66: [1552, 1924, 2295], 67: [1625, 1998, 2370]}, names)
    out = []
    for k, (view, lab, c, fl, r) in enumerate(rows):
        log(t, "crosscheck_1931_vs_table_VII")
        if c[2] == t7[T7_NAMES[k]]:
            log(t, "crosscheck_1931_vs_table_VII_passed")
        else:
            print(t, "1931 != VII total", lab, c[2], t7[T7_NAMES[k]])
        for yi, year in enumerate((1921, 1926, 1931)):
            out.append({"census": "ind1931", "table_id": t, "source_page": {66: 115, 67: 116}[view],
                        "gallica_view": view, "commune": lab, "census_year": year, "value": c[yi],
                        "flag": "ocr_corrected" if yi in fl else ""})
    log(t, "rows_compared_with_image", len(rows))
    write_csv("ind1931_t7annex_communes_1921_1931.csv", out,
              BASE + ["commune", "census_year", "value", "flag"])


# --------------------------------------------------------------------------
# Table VIII: non-commune localities with more than 25 households
# --------------------------------------------------------------------------
T8_VIEWS = list(range(68, 79))   # pp.117-127


def table_8_raw():
    out = []
    for v in T8_VIEWS:
        ws = [w for w in boxes(v) if w["row"] > 1150]
        edges = [e for e in cluster_edges(ws, min_count=6) if e > 900]
        assert len(edges) == 3, (v, edges)
        for r in page_rows(v, edges, 1150, 4100, tol=40 if v == 75 else 22):
            if all(x is None for x in r["cells"]):
                if r["label"] or r["right"]:
                    out.append((v, r, "text_only"))
                continue
            out.append((v, r, "data"))
    return out


import difflib  # noqa: E402

FOOT = re.compile(r"\(\s*([123])\s*\)|\s[lt(]\s*([123])\s*\)")


def clean_name(lab):
    """Name text as printed, minus footnote markers; returns (name, footnote_no)."""
    fn = None
    m = FOOT.search(lab)
    if m:
        fn = m.group(1) or m.group(2)
        lab = FOOT.sub("", lab)
    lab = re.sub(r"\s*-\s*$", "", lab)
    lab = re.sub(r"\s+", " ", lab).replace("’", "'").strip(" .,;:'|I")
    return lab, fn


def known_caidats():
    return sorted(set(T6_NAMES) | set(T7_CAIDATS) | set(T5_NAMES) | {"Ouerghemma (Terr. de Médenine)"})


def match_caidat(txt):
    t = re.sub(r"[^\w\-() éèêàâîïôûüç—]", "", txt.replace("T unis", "Tunis")).strip()
    if not t or t in {"—", "-"} or set(t) <= set("—- "):
        return "—", 1.0
    if "Terr" in t:
        return "Ouerghemma (Terr. de Médenine)", 1.0
    best = max(known_caidats(), key=lambda k: difflib.SequenceMatcher(None, k.lower(), t.lower()).ratio())
    return best, difflib.SequenceMatcher(None, best.lower(), t.lower()).ratio()


# Name fixes after reading every page image of Table VIII: OCR-cleaned name -> name as printed.
T8_NAME_FIX = {
    "Ahoueeh (El)": "Ahouech (El)", "Ahzèg": "Ahzeg", "Akoua ch e-Da r-Ch e ikh": "Akouache-Dar-Cheikh",
    "Akouda -": "Akouda", "Aoùinet-Oum-Hend": "Aouinet-Oum-Hend", "Arain": "Aram", "Avaïcha (El)": "Ayaïcha (El)",
    "Sembla": "Bembla", "Bennanc": "Bennane", "Bbirine (El)": "Bhirine (El)", "B.oudher": "Boudher",
    "Darnous": "Damous", "Dar-Braharn": "Dar-Braham", "Dj eziret-El-Ouchichi": "Djeziret-El-Ouchichi",
    "Feliri (El)": "Fehri (El)", "Hencha (Et)": "Hencha (El)", "Houcb-Sfaïa": "Houch-Sfaïa", "vebili": "Kebili",
    "Kellabine (B": "Kellabine", "vheraïb (El)": "Kheraïb (El)", "lvheriba (El)": "Kheriba (El)",
    "K naïs": "Knaïs", "Ksonr": "Ksour", "Laalaa (EJ)": "Laalaa (El)", "Lala. • •": "Lala",
    "Maamoura (El) ••": "Maamoura (El)", "Mellasinie": "Mellasine", "Mellita 0)": "Mellita",
    "Meilara (El)": "Menara (El)", "Menzel-Kamel • • •": "Menzel-Kamel", "Mesjéd-Aïssa": "Mesjed-Aïssa",
    "Moàtamer": "Moâtamer", "Nebenr": "Nebeur", "N eh al": "Nehal", "Oulad-Bou-Ali P)": "Oulad-Bou-Ali",
    "Oulad-Bou-Gbanem": "Oulad-Bou-Ghanem", "Babta": "Rabta", "Ras-Djebèl": "Ras-Djebel", "Tombai*": "Tombar",
    "Zaouit-EI-Anès": "Zaouit-El-Anès", "Zaouiet-Es-Saliraoui": "Zaouiet-Es-Sahraoui", "Zerg'ane": "Zergane",
    "Mouamena El": "Mouamena El",
}
# Footnote markers the OCR mangled (name as printed -> footnote number)
T8_FOOT_FIX = {"Kellabine": "1", "Mellita": "1", "Oulad-Bou-Ali": "1"}
# View 76 (p.125): OCR names unusable (and a library stamp on the page); names read from the image.
T8_V76 = ["Rejich", "Remada", "Remla", "Roudha", "Sabria", "Saheline", "Saïada", "Sakiet-Sidi-Youssef",
          "Sartout", "Sedjenane", "Sembat", "Sened", "Sidi-Ahmed-Djedidi", "Sidi-Ali-Ben-Nasr-Allah",
          "Sidi-Ali-Chebab", "Sidi-Alouane", "Sidi-Ameur", "Sidi-Bou-Ali", "Sidi-Bou-Lebaba", "Sidi-Bou-Zid",
          "Sidi-Fathallah", "Sidi-Hamada", "Sidi-Naceur", "Sidi-Naïja", "Siliana", "Skalba"]
T8_V76_FOOT = {"Remla": "1", "Sartout": "2"}
# Caidat cells printed differently from the caidat list
T8_CAIDAT_FIX = {"Hassi-Djerbi": "Ouerghemma (Terr. de Zarzis)",
                 "Hencha (El)": "Mahdia"}   # printed 'Madhia' (misprint)


def table_8():
    t = "VIII"
    out, n76 = [], list(T8_V76)
    for v, r, kind in table_8_raw():
        if kind != "data":
            continue
        c = r["cells"]
        if v == 76:
            if c[0] is None and c[2] is None:      # stamp fragment
                log(t, "stamp_fragments_dropped")
                continue
            name = n76.pop(0)
            fn = T8_V76_FOOT.get(name)
        else:
            name, fn = clean_name(r["label"])
            name = T8_NAME_FIX.get(name, name)
            fn = fn or T8_FOOT_FIX.get(name)
        txt = r["right"] or " ".join(w["text"] for w in r["stray"] if num_tok(w["text"]) is None)
        caid, score = match_caidat(txt)
        # keep 'Ouled-' spellings where printed so
        if "oule" in txt.lower() and caid.startswith("Oulad-"):
            caid = caid.replace("Oulad-", "Ouled-")
        caid = T8_CAIDAT_FIX.get(name, caid)
        corr = apply_corrections(t, name, c)
        filled = fill_zero_if_balanced(c, [([0, 1], 2)], t)
        log(t, "row_checks")
        if check_rows(c, [([0, 1], 2)]):
            log(t, "row_checks_passed")
        else:
            print(t, "ROW FAIL", v, name, c)
        page = 117 + T8_VIEWS.index(v)
        for ri, (rel, rel_fr) in enumerate(RELIGIONS):
            out.append({"census": "ind1931", "table_id": t, "source_page": page, "gallica_view": v,
                        "locality": name, "caidat": "" if caid == "—" else caid,
                        "note": "Kerkennah islands (printed footnote)" if fn else "",
                        "religion": rel, "religion_fr": rel_fr, "value": c[ri],
                        "flag": "ocr_corrected" if ri in corr | filled else ""})
    assert not n76, n76
    log(t, "pages_compared_with_image", len(T8_VIEWS))
    write_csv("ind1931_t8_localities.csv", out,
              BASE + ["locality", "caidat", "note", "religion", "religion_fr", "value", "flag"])


T6_NAMES = ["Aïn-Draham", "Aradh", "Béja", "Bizerte", "Djebeniana", "Djelass", "Djerba", "Djerid",
            "Fraichiches", "Gafsa", "Hammama", "Kairouan", "La Skhira", "Le Kef", "Madjeurs",
            "Mahdia", "Mateur", "Matmata", "Medjez-El-Bab", "Monastir", "Nabeul", "Nefzaoua",
            "Ouerghemma", "Oulad-Aoun", "Oulad-Ayar", "Sfax", "Soliman", "Souassi", "Souk-El-Arba",
            "Souk-El-Khemis", "Sousse", "Tadjerouine", "Tatahouine", "Téboursouk", "Tunis-Banlieue",
            "Tunis-Ville", "Zaghouan"]

T5_NAMES = ["Aïn-Drahâm", "Aradh", "Béja", "Bizerte", "Djebeniana", "Djelass", "Djerba", "Djérid",
            "Fraichiches", "Gafsa", "Hammama", "Kairouan", "La Skhira", "Le Kef", "Madjeur",
            "Mahdia", "Mateur", "Matmata", "Medjez-El-Bab", "Monastir", "Nabeul", "Nefzaoua",
            "Ouerghemma", "Oulad-Aoun", "Oulad-Ayar", "Sfax", "Soliman", "Souassi", "Souk-El-Arba",
            "Souk-El-Khemis", "Sousse", "Tadjerouine", "Tatahouine", "Téboursouk", "Tunis-Banlieue",
            "Tunis-Ville", "Zaghouan"]


if __name__ == "__main__":
    which = sys.argv[1:] or ["1", "2", "4", "4annex", "5", "5annex", "6", "6annex", "7annex", "8"]
    for w in which:
        globals()[f"table_{w}"]()
    print(json.dumps(LOG, indent=1))
    (HERE / "csv" / "ind1931_other_validation.json").write_text(json.dumps(LOG, indent=1))


# --------------------------------------------------------------------------
# Notes files (one per CSV), generated from NOTES and the validation log
# --------------------------------------------------------------------------
SRC = ("Source: *Dénombrement de la population civile indigène (musulmane et israélite) en Tunisie "
       "au 22 mars 1931*, Régence de Tunis, Direction générale de l'intérieur, Tunis, Impr. J. Aloccio, 1932. "
       "Gallica ark `bpt6k994559s` (Source gallica.bnf.fr / Bibliothèque nationale de France).")
COMMON = """
## Method

Numbers come from Gallica's word OCR (via `ocr.py`), assigned to printed columns by right edge,
with page images used to correct the OCR. Script: `extract_ind1931_other.py`. Printed `»` = 0.
Printed subtotal, total, `A reporter` and `Report` lines are not stored; they were used for validation.
`flag = ocr_corrected` marks a cell where the OCR value was missing or wrong and the value was read
from the page image (an empty OCR cell is set to 0 only where the image shows `»` and the printed
row totals then balance; every such cell was confirmed on the image).
"""
NOTES = {
 "ind1931_t1_controle_nationality.csv": ("Tableau I — État de la population indigène par circonscription de Contrôle Civil",
   "Table I: indigenous population by contrôle civil (civil-control district), by religion and nationality",
   "pp. 6–7, view 8", "I",
   "One row per contrôle civil × religion × nationality (20 contrôles × 2 × 7). Muslim nationalities "
   "are printed on p.6 and Jewish ones on p.7. Unit: persons.", ""),
 "ind1931_t2_caidat_nationality.csv": ("Tableau II — État de la population indigène par Caïdats",
   "Table II: indigenous population by caidat, by religion and nationality",
   "pp. 8–11, views 9–10", "II",
   "One row per caidat × religion × nationality (37 caidats). Unit: persons.", ""),
 "ind1931_t4_controle_1926_1931.csv": ("Tableau IV — Statistique comparée des dénombrements de 1926-1931 concernant la population indigène de la Tunisie répartie par Contrôles Civils",
   "Table IV: indigenous population by contrôle civil, 1926 and 1931 censuses",
   "pp. 98–99, view 54", "IV",
   "One row per contrôle civil × religion × census year. The printed 'Augmentation ou diminution' "
   "(change) columns and the general totals are not stored; they were checked (|1931 − 1926| = printed change; "
   "Muslim + Jewish = general total). 1931 values were also cross-checked against Table I.",
   "Printed note (translated): the Muslim population, 1,932,184 in 1926, increased by 226,967; the Jewish "
   "population, 54,243 in 1926, increased by 2,005; the total indigenous population, 1,986,427 in 1926, increased "
   "by 228,972. 'This happy result must, without any doubt, be attributed to the improvement of hygiene and of "
   "material conditions of existence.' The scan has pencil circles around some Sfax and Tunis figures; the printed values are used."),
 "ind1931_t4annex_nationality_1926_1931.csv": ("Annexe au Tableau IV — Statistique comparée des dénombrements de 1926-1931 concernant le classement de la population indigène d'après l'origine",
   "Annex to Table IV: indigenous population by origin (nationality), 1926 and 1931",
   "p. 100, view 55 (printed rotated 90°)", "IV_annex",
   "One row per religion × nationality × census year. The page is printed sideways; values were transcribed "
   "from the rotated image and validated against printed totals and Table I (1931).", ""),
 "ind1931_t5_caidat_sex_age.csv": ("Tableau V — Répartition de la population musulmane et israélite d'après le sexe et l'âge",
   "Table V: Muslim and Jewish population by sex and age group, by caidat",
   "pp. 102–105, views 57–58", "V",
   "One row per caidat × religion × category. Categories: Hommes / Femmes = adults aged 18 and over "
   "(`age_group = adult_18_plus`); Garçons / Filles = children (`child_under_18`). Caidat totals "
   "were cross-checked against Table II. Overlaps the package's existing `colonial_age_caidat_1931`.", ""),
 "ind1931_t5annex_sex_age_1926_1931.csv": ("Annexe au Tableau V — Statistique comparée des dénombrements de 1926-1931 concernant le classement de la population indigène d'après le sexe et l'âge",
   "Annex to Table V: indigenous population by sex and age group, 1926 and 1931",
   "p. 106, view 59 (printed rotated 90°)", "V_annex",
   "One row per religion × category × census year. Transcribed from the rotated image; 1931 values "
   "cross-checked against Table V sums.", ""),
 "ind1931_t6_caidat_profession.csv": ("Tableau VI — Classement, d'après la profession, des adultes mâles âgés de 18 ans au moins",
   "Table VI: occupations of adult males aged 18 and over, by caidat",
   "pp. 108–111, views 61–62", "VI",
   "One row per caidat × religion × occupation. The table prints no row totals, so each caidat's 8 "
   "occupations were checked against that caidat's adult men in Table V (`crosscheck_table_V_adult_men`); "
   "`row_checks` in the log is not meaningful for this table. Column totals and the carry-forward line were checked. "
   "Muslim occupations (1)–(6) are on the left page, (7)–(8) on the right page with the Jewish columns.",
   "Printed footnotes (translated): (1) rural landowners, farmers and agricultural workers of every kind: "
   "managers, foremen, khammès (sharecroppers), gardeners, shepherds. (2) traders, staff of all shops, "
   "commercial and bank employees, pedlars. (3) employers and workers of all trades actually engaged in "
   "manufacturing; fisheries. (4) labourers, jobbers, all those who, without a well-defined occupation, work by "
   "the day in commercial, industrial or agricultural concerns. (5) railway and tramway employees, maritime "
   "transport agents, carters, porters, camel drivers. (6) staff of the administrations and public services, "
   "including the judiciary, the police, the oudjak. (7) lawyers, oukils, doctors, business agents, experts, "
   "brokers, representatives, amines, notaries, artists, members of religious teaching and of the clergy. "
   "(8) persons not belonging in any of the previous categories: students, the infirm, people of private means. "
   "NOTA: covers only adult males aged 18 and over, i.e. 563,791 Muslims and 15,008 Jews = 578,799."),
 "ind1931_t6annex_profession_1926_1931.csv": ("Annexe au Tableau VI — Statistique comparée des dénombrements de 1926-1931 concernant le classement, d'après la profession, des adultes mâles âgés de 18 ans au moins",
   "Annex to Table VI: occupations of adult males aged 18+, 1926 and 1931",
   "p. 112, view 63 (printed rotated 90°)", "VI_annex",
   "One row per religion × occupation × census year. Transcribed from the rotated image; 1931 values "
   "cross-checked against Table VI sums.", ""),
 "ind1931_t7_communes.csv": ("Tableau VII — Population musulmane et israélite des localités érigées en Commune",
   "Table VII: Muslim and Jewish population of the localities constituted as communes (municipalities)",
   "pp. 113–114, views 64–65", "VII",
   "One row per commune × religion (58 communes). `caidat` as printed in the table's last column; "
   "empty where the table prints '—' (Bardo, Monastir). The OCR has no commune names on p.113, so names were read "
   "from the images; the printed total column is not stored but was checked (Muslim + Jewish = total) "
   "and equals the 1931 column of Annex VII for every commune.",
   "Tébourba is printed 3.107 + 42 = 3.128 (should be 3.149); printed values kept, flagged `total_mismatch`; "
   "Annex VII also gives 3.128 for 1931. Saint-Germain is printed '»' in all columns."),
 "ind1931_t7annex_communes_1921_1931.csv": ("Annexe au Tableau VII — Statistique comparée des dénombrements de 1921, 1926 et 1931 concernant la population indigène des localités érigées en commune",
   "Annex to Table VII: indigenous population of the communes at the 1921, 1926 and 1931 censuses",
   "pp. 115–116, views 66–67", "VII_annex",
   "One row per commune × census year (total indigenous population). Names spelled as printed in the annex "
   "(e.g. 'Ariana', 'Fériana', 'Kalaâ-Kébira'), in the same order as Table VII. 1931 values equal the Table VII "
   "totals for all 58 communes; 1921 and 1926 values have no printed total and were compared line by line with the "
   "page images. '»' printed for a year (e.g. El-Djem, Hadjeb-El-Aïoun, Ksour-Essaf in 1921; Sbeïtla in 1921 and 1926; "
   "Saint-Germain in 1921 and 1931) is stored as 0 per the spec; it likely means the locality was not a commune "
   "or not counted separately that year.", ""),
 "ind1931_t8_localities.csv": ("Tableau VIII — Population musulmane et israélite des localités non érigées en Commune et comptant plus de 25 foyers",
   "Table VIII: Muslim and Jewish population of localities not constituted as communes and having more than 25 households",
   "pp. 117–127, views 68–78", "VIII",
   "One row per locality × religion (281 localities). `caidat` as printed; empty where the table prints '—'. "
   "Caidat spellings follow the print ('Oulad-Aoun' on p.118, 'Ouled-Aoun'/'Ouled-Ayar' elsewhere). "
   "Hassi-Djerbi's caidat is printed 'Ouerghemma (Terr. de Zarzis)'; Beni-Kheddache and Métameur 'Ouerghemma (Terr. de Médenine)'. "
   "Hencha (El)'s caidat is misprinted 'Madhia' and stored as 'Mahdia'. Duplicate names (Aouina (El), Chenini, "
   "Gueliâ (El), Mansoura (El), Zriba) are distinct localities in different caidats. Every row was checked "
   "(Muslim + Jewish = printed total); all names and caidats were compared with the page images "
   "(the OCR names on p.125 were unusable and were read from the image; a library stamp covers part of that page).",
   "Printed footnotes: localities marked (1), (2), (3) are in the Kerkennah islands; stored in `note`."),
}


def write_notes():
    log_ = json.loads((OUT / "ind1931_other_validation.json").read_text())
    for fname, (fr, en, pages, tid, body, foot) in NOTES.items():
        rows = read_csv(fname)
        v = log_.get(tid, {})
        val = "\n".join(f"- `{k}`: {n}" for k, n in v.items())
        flags = {}
        for r in rows:
            if r["flag"]:
                flags[r["flag"]] = flags.get(r["flag"], 0) + 1
        txt = (f"# {fr}\n\n*{en}*\n\n{SRC}\n\nPages: {pages}. Table id: `{tid}`. Rows: {len(rows)}.\n\n"
               f"## Content\n\n{body}\n\nColumns: {', '.join(rows[0].keys())}.\n"
               + (f"\n## Notes and printed footnotes\n\n{foot}\n" if foot else "")
               + COMMON + f"\n## Validation\n\n{val}\n\nFlags: {flags or 'none'}.\n")
        (OUT / fname.replace(".csv", ".md")).write_text(txt, encoding="utf-8")
    print("notes written:", len(NOTES))


if __name__ == "__main__":
    write_notes()
