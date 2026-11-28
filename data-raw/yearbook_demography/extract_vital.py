#!/usr/bin/env python3
"""Vital statistics ("Mouvement de la population") from the 12 editions of the
Statistique générale de la Tunisie, 1922-1939.

Tables (per edition, see EDITIONS.md):
  a) European marriages by nationality of groom and bride
  b) mixed marriages between Europeans and indigenous Tunisians (from 1926)
  c) European births by nationality and sex
  d) European deaths by nationality and sex
  Muslim births and deaths by contrôle civil (5-year window)
  Jewish births and deaths by contrôle civil (5-year window)

Workflow:
  python3 extract_vital.py draft <dir>   OCR drafts of every page, written to <dir>
                                         (never over the verified transcriptions)
  python3 extract_vital.py build         parse transcribed/vital_*.txt, check every
                                         printed total and every overlapping printing,
                                         write csv/vital_*.csv and their notes

The verified transcriptions in transcribed/ are the source of truth. They were
made from the drafts by reading full-resolution page images (the IIIF server
returns full resolution only for region requests with an explicit size; see
fetch_fullres()).
"""
import csv
import io
import json
import re
import sys
import time
import urllib.request
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OCR_CACHE = ROOT / "data-raw" / "bnf_gallica" / "ocr"
TR = HERE / "transcribed"
OUT = HERE / "csv"

# edition code -> (volume ark, {table: view})
EDITIONS = {
    "sgt1922": ("bpt6k9105649x", {"eur_marriages": 39, "eur_births_deaths": 40, "muslim": 41, "jewish": 42}),
    "sgt1923": ("bpt6k9105649x", {"eur_marriages": 517, "eur_births_deaths": 518, "muslim": 519, "jewish": 520}),
    "sgt1924": ("bpt6k9105649x", {"eur_marriages": 1005, "eur_births_deaths": 1006, "muslim": 1007, "jewish": 1008}),
    "sgt1925": ("bpt6k9105650k", {"eur_marriages": 37, "eur_births_deaths": 38, "muslim": 39, "jewish": 40}),
    "sgt1926": ("bpt6k9105650k", {"eur_marriages": 582, "eur_births_deaths": 583, "muslim": 584, "jewish": 585}),
    "sgt1927": ("bpt6k91056510", {"eur_marriages": 46, "eur_births_deaths": 47, "muslim": 48, "jewish": 49}),
    "sgt1928": ("bpt6k91056510", {"eur_marriages": 570, "eur_births_deaths": 571, "muslim": 572, "jewish": 573}),
    "sgt1929": ("bpt6k9105652d", {"eur_marriages": 46, "eur_births_deaths": 47, "muslim": 48, "jewish": 49}),
    "sgt1930": ("bpt6k9105652d", {"eur_marriages": 576, "eur_births_deaths": 577, "muslim": 578, "jewish": 579}),
    "sgt1935": ("bpt6k9105653t", {"eur_marriages": 27, "eur_births_deaths": 28, "muslim": 29, "jewish": 30}),
    "sgt1936": ("bpt6k91056547", {"eur_marriages": 18, "eur_births_deaths": 19, "muslim": 20, "jewish": 21}),
    "sgt1939": ("bpt6k9105739w", {"eur_marriages": 13, "eur_births_deaths": 14, "muslim": 15, "jewish": 16}),
}
EDITION_ORDER = list(EDITIONS)

# --------------------------------------------------------------------------- OCR


def words(ark, view):
    """Words with vertical centre, left and right edge (OCR boxes are transposed)."""
    p = OCR_CACHE / f"{ark}_f{view:03d}.json"
    out = []
    for it in json.loads(p.read_text()).get("items", []):
        x, y, w, h = map(int, re.search(r"xywh=(\d+),(\d+),(\d+),(\d+)", it["target"]).groups())
        out.append({"row": x + w / 2, "left": y, "right": y + h, "text": it["body"]["value"]})
    return out


def rows(ws, tol=16):
    ws = sorted(ws, key=lambda w: w["row"])
    out = []
    for w in ws:
        if out and abs(w["row"] - out[-1][-1]["row"]) < tol:
            out[-1].append(w)
        else:
            out.append([w])
    return [sorted(r, key=lambda w: w["left"]) for r in out]


NUMTOK = re.compile(r"^[\d.,»)S$Il]+$")


def clean_num(t):
    t = t.strip().rstrip(".,")
    if t in {"»", "))", ")", "»»", "»)"}:
        return 0
    t = t.replace("S", "8").replace("$", "8").replace("I", "1").replace("l", "1").replace(",", ".")
    t = t.replace(".", "")
    return int(t) if t.isdigit() else None


def number_cells(row):
    """Merge split thousands ('2' + '289') and return [(right_edge, value, raw)]."""
    toks = [w for w in row if NUMTOK.match(w["text"]) and clean_num(w["text"]) is not None]
    out = []
    i = 0
    while i < len(toks):
        w = toks[i]
        raw, right = w["text"], w["right"]
        if (i + 1 < len(toks) and re.fullmatch(r"\d{1,2}", w["text"].rstrip("."))
                and re.fullmatch(r"\d{3}\.?", toks[i + 1]["text"])
                and toks[i + 1]["left"] - w["right"] < 40):
            raw = w["text"].rstrip(".") + "." + toks[i + 1]["text"].rstrip(".")
            right = toks[i + 1]["right"]
            i += 1
        out.append((right, clean_num(raw), raw))
        i += 1
    return out


def column_edges(rows_cells, n):
    """Right edges of n columns: medians of the right edges of rows that have n cells."""
    full = [c for c in rows_cells if len(c) == n]
    if not full:
        return None
    return [sorted(r[k][0] for r in full)[len(full) // 2] for k in range(n)]


def assign(cells, edges, tol=45):
    out = [None] * len(edges)
    for right, v, raw in cells:
        k = min(range(len(edges)), key=lambda j: abs(edges[j] - right))
        if abs(edges[k] - right) < tol and out[k] is None:
            out[k] = v
    return out


def draft_grid(ark, view, ncols):
    """Text draft: 'label | v1 v2 ...' per printed row, '?' for cells not found."""
    rs = rows(words(ark, view))
    cells = [number_cells(r) for r in rs]
    edges = column_edges(cells, ncols)
    lines = []
    for r, c in zip(rs, cells):
        if len(c) < max(2, ncols // 3):
            continue
        label = " ".join(w["text"] for w in r if not (NUMTOK.match(w["text"]) and clean_num(w["text"]) is not None)
                         and w["right"] < (edges[0] - 60 if edges else 10 ** 9))
        vals = assign(c, edges) if edges else [v for _, v, _ in c]
        lines.append(f"{label or '?'} | " + " ".join("?" if v is None else str(v) for v in vals))
    return lines


# ------------------------------------------------------------------- full resolution

IIIF = "https://openapi.bnf.fr/iiif/image/v3/ark:/12148/{ark}/f{v}"


def fetch_fullres(ark, view, out_dir):
    """Full-resolution page image, stitched from four region tiles.

    The gateway caps whole-image requests at about half resolution, but returns a
    region at native resolution when the output width equals the region width.
    """
    from PIL import Image
    out_dir = Path(out_dir)
    p = out_dir / f"{ark}_f{view:04d}.jpg"
    if p.exists():
        return p
    def get(u):
        for i in range(6):
            try:
                return urllib.request.urlopen(u, timeout=120).read()
            except Exception:
                time.sleep(2 ** i)
        raise RuntimeError(u)
    base = IIIF.format(ark=ark, v=view)
    info = json.loads(get(base + "/info.json"))
    W, H = info["width"], info["height"]
    tw, th = (W + 1) // 2, (H + 1) // 2
    img = Image.new("RGB", (W, H))
    for x in range(0, W, tw):
        for y in range(0, H, th):
            w, h = min(tw, W - x), min(th, H - y)
            img.paste(Image.open(io.BytesIO(get(base + f"/{x},{y},{w},{h}/{w},/0/default.jpg"))), (x, y))
    out_dir.mkdir(parents=True, exist_ok=True)
    img.save(p, quality=92)
    return p


# ------------------------------------------------------------------- drafts

def header_years(ark, view):
    ys = []
    for r in rows(words(ark, view))[:12]:
        found = [int(m) for w in r for m in re.findall(r"(19[0-4]\d|18\d\d)", w["text"].replace("O", "0"))]
        if len(found) >= 2 and len(found) > len(ys):
            ys = found
    return sorted(set(y for y in ys if 1910 <= y <= 1940))


CONTROLES = ["Béja", "Bizerte", "Djerba", "Gabès", "Gafsa", "Grombalia", "Kairouan", "Kef",
             "Mactar", "Medjez-el-Bab", "Sfax", "Souk-el-Arba", "Sousse", "Tabarka",
             "Téboursouk", "Thala", "Tozeur", "Tunis", "Zaghouan", "Territoires du Sud"]
# Years printed in each edition's indigenous tables (header OCR is unreliable)
INDIG_YEARS = {"sgt1922": range(1918, 1923), "sgt1923": range(1918, 1924),
               "sgt1924": range(1920, 1925), "sgt1925": range(1921, 1926),
               "sgt1926": range(1922, 1927), "sgt1927": range(1923, 1928),
               "sgt1928": range(1924, 1929), "sgt1929": range(1925, 1930),
               "sgt1930": range(1926, 1931), "sgt1935": range(1930, 1935),
               "sgt1936": range(1932, 1937), "sgt1939": range(1935, 1940)}


def draft_indigenous(ed, table):
    """Draft with canonical row names: the 20 data rows in printed order, then the totals."""
    ark, views = EDITIONS[ed]
    view = views[table]
    years = list(INDIG_YEARS[ed])
    grid = draft_grid(ark, view, 2 * len(years))
    data = [l for l in grid if l.split("|")[1].split().count("?") <= len(years)]
    # drop header lines (year numbers) at the top
    data = [l for l in data if not re.search(r"\b19[0-4]\d\b.*\b19[0-4]\d\b", l.split("|")[1])]
    lines = [f"# {ed} {table} ark {ark} view {view} (OCR draft: {len(data)} rows found, expect 21)",
             "years: " + " ".join(map(str, years))]
    names = CONTROLES + ["TOTAUX"]
    if len(data) == 21:
        lines += [f"{n} | {l.split('|')[1].strip()}" for n, l in zip(names, data)]
    else:
        lines += [f"?? {l}" for l in data]
    return lines


def cmd_draft(out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for ed in EDITIONS:
        for table in ("muslim", "jewish"):
            (out_dir / f"vital_{table}_{ed}.txt").write_text("\n".join(draft_indigenous(ed, table)) + "\n")
    print("drafts written to", out_dir)


# ------------------------------------------------------------------- build

NAT = {"Français": "french", "Italiens": "italian", "Maltais": "maltese", "Grecs": "greek",
       "Espagnols": "spanish", "Autres Européens": "other_european",
       "Nationalité non signalée": "not_stated"}
NAT_FR = {"Nationalité non signalée": "Époux dont la nationalité n'a pas été signalée"}
GROOM_NAT = {"Français": "french", "Italiens": "italian", "Maltais": "maltese",
             "Etrangers autres": "other_foreign", "Musulmans": "muslim", "Israélites": "jewish"}
BRIDE_COLS = [("muslim", "Musulmanes"), ("jewish", "Israélites"), ("french", "Françaises"),
              ("italian", "Italiennes"), ("maltese", "Maltaises"), ("other_foreign", "Étrangères autres")]


# Printed page numbers (from the page headers; these volumes' manifests carry no
# page labels): first page of the four tables, in EDITIONS[...] order.
FIRST_PAGE = {"sgt1922": 15, "sgt1923": 15, "sgt1924": 15, "sgt1925": 13, "sgt1926": 18,
              "sgt1927": 18, "sgt1928": 18, "sgt1929": 18, "sgt1930": 18, "sgt1935": 7,
              "sgt1936": 7, "sgt1939": 7}
PRINTED_PAGE = {}
for _ed, (_ark, _views) in EDITIONS.items():
    for _k, _v in _views.items():
        PRINTED_PAGE[(_ark, _v)] = FIRST_PAGE[_ed] + (_v - _views["eur_marriages"])


def page_label(ark, view):
    key = (ark, view)
    if key not in PRINTED_PAGE:
        m = json.loads((ROOT / "data-raw" / "bnf_gallica" / "pages" / ark / "manifest.json").read_text())
        lab = " ".join(next(iter(m["items"][view - 1].get("label", {}).values()), [""]))
        d = re.findall(r"\d+", lab)
        PRINTED_PAGE[key] = int(d[0]) if d else ""
    return PRINTED_PAGE[key]


class Checks:
    def __init__(self):
        self.n = 0
        self.fail = []

    def eq(self, what, got, printed):
        self.n += 1
        if got != printed:
            self.fail.append(f"{what}: cells sum to {got}, printed {printed}")


def read_indigenous(ed, table):
    p = TR / f"vital_{table}_{ed}.txt"
    L = p.read_text().splitlines()
    years = [int(y) for y in L[1].split(":")[1].split()]
    rows = {}
    for l in L[2:]:
        if "|" in l:
            n, v = l.split("|")
            rows[n.strip()] = [int(x) for x in v.split()]
    assert list(rows)[:-1] == CONTROLES and list(rows)[-1] == "TOTAUX", (ed, table)
    return years, rows


def read_european(ed):
    secs, cur = {}, None
    for l in (TR / f"vital_european_{ed}.txt").read_text().splitlines():
        if not l.strip() or l.startswith("#"):
            continue
        if l.startswith("["):
            name = l[1:l.index("]")]
            ys = [int(y) for y in l.split("years:")[1].split()] if "years:" in l else []
            cur = secs[name] = {"years": ys, "rows": {}}
            continue
        n, v = l.split("|")
        cur["rows"][n.strip()] = [None if x == "." else int(x) for x in v.split()]
    return secs


# Cells that are evidently misprinted: the printed column total, repeated in every
# reprint, implies a value with one digit dropped or changed, and the printed
# value is far from the same contrôle's neighbouring years. Kept as printed.
#   Territoires du Sud 1929 births: printed 564; 5.640 closes the 5,076 gap exactly
#     (1928: 5.399, 1930: 6.211).
#   Medjez-el-Bab 1936 births: printed 4.741; 1.741 closes the 3,000 gap exactly
#     (1935: 1.296, 1937: 1.451).
CELL_FLAGS = {
    ("muslim", "Territoires du Sud", 1929, "births"): "total_mismatch",
    ("muslim", "Medjez-el-Bab", 1936, "births"): "total_mismatch",
}


def build_indigenous(table, chk, notes):
    """Return {(controle, year, event): (value, edition)} from the latest printing, and
    compare every other printing of each cell."""
    printings = defaultdict(dict)   # (ctrl, year, event) -> {ed: value}
    totals = defaultdict(dict)
    for ed in EDITION_ORDER:
        years, rows = read_indigenous(ed, table)
        for c in range(2 * len(years)):
            y, ev = years[c // 2], ("births", "deaths")[c % 2]
            col = sum(rows[n][c] for n in CONTROLES)
            chk.eq(f"{ed} {y} {ev} column vs TOTAUX", col, rows["TOTAUX"][c])
            for n in CONTROLES:
                printings[(n, y, ev)][ed] = rows[n][c]
            totals[(y, ev)][ed] = rows["TOTAUX"][c]
    out, compared, diffs = {}, 0, []
    for key, by_ed in printings.items():
        eds = [e for e in EDITION_ORDER if e in by_ed]
        latest = eds[-1]
        out[key] = (by_ed[latest], latest)
        for e in eds[:-1]:
            compared += 1
            if by_ed[e] != by_ed[latest]:
                diffs.append((key, e, by_ed[e], latest, by_ed[latest]))
    for key, by_ed in totals.items():
        eds = [e for e in EDITION_ORDER if e in by_ed]
        for e in eds[:-1]:
            compared += 1
            if by_ed[e] != by_ed[eds[-1]]:
                diffs.append((("TOTAUX",) + key, e, by_ed[e], eds[-1], by_ed[eds[-1]]))
    notes["compared"], notes["diffs"] = compared, diffs
    notes["totals"] = {k: (v[[e for e in EDITION_ORDER if e in v][-1]], [e for e in EDITION_ORDER if e in v][-1]) for k, v in totals.items()}
    return out


def build_european(chk, notes):
    cells = defaultdict(dict)        # (table, nat, year, sex_or_role) -> {ed: v}
    tot = defaultdict(dict)          # (table, year) -> {ed: v}
    mixed = []
    for ed in EDITION_ORDER:
        s = read_european(ed)
        m = s["marriages"]
        R = m["rows"]
        for i, y in enumerate(m["years"]):
            g = sum(R[n][2 * i] for n in NAT)
            chk.eq(f"{ed} marriages {y}: grooms vs printed total", g, R["TOTAUX"][i])
            for n in NAT:
                cells[("marriages", n, y, "groom")][ed] = R[n][2 * i]
                cells[("marriages", n, y, "bride")][ed] = R[n][2 * i + 1]
            tot[("marriages", y)][ed] = R["TOTAUX"][i]
        x = s["mixed"]["rows"]
        year = s["births"]["years"][-1]
        for grp, names, cols in (("TOTAL_EUROPEAN_GROOMS", ["Français", "Italiens", "Maltais", "Etrangers autres"], [0, 1, 2]),
                                 ("TOTAL_INDIGENOUS_GROOMS", ["Musulmans", "Israélites"], [0, 3, 4, 5, 6])):
            for c in cols:
                if x[grp][c] is not None:
                    chk.eq(f"{ed} mixed marriages {grp} col {c}", sum(x[n][c] or 0 for n in names), x[grp][c])
            for n in names:
                chk.eq(f"{ed} mixed marriages {n}: number vs brides", sum(x[n][c] or 0 for c in cols[1:]), x[n][0])
                for c in cols[1:]:
                    bn, bfr = BRIDE_COLS[c - 1]
                    mixed.append(dict(year=year, edition=ed, groom=GROOM_NAT[n], groom_fr=n, bride=bn,
                                      bride_fr=bfr, value=x[n][c] if x[n][c] is not None else 0))
        for sec in ("births", "deaths"):
            b = s[sec]
            R = b["rows"]
            for i, y in enumerate(b["years"]):
                for k, sx in ((0, "male"), (1, "female")):
                    chk.eq(f"{ed} {sec} {y} {sx}: nationalities vs subtotal",
                           sum(R[n][2 * i + k] for n in NAT if n in R), R["SUBTOTAL"][2 * i + k])
                    for n in NAT:
                        if n in R:
                            cells[(sec, n, y, sx)][ed] = R[n][2 * i + k]
                chk.eq(f"{ed} {sec} {y}: male + female vs total",
                       R["SUBTOTAL"][2 * i] + R["SUBTOTAL"][2 * i + 1], R["TOTAUX"][i])
                tot[(sec, y)][ed] = R["TOTAUX"][i]
    out, compared, diffs = {}, 0, []
    for key, by_ed in cells.items():
        eds = [e for e in EDITION_ORDER if e in by_ed]
        out[key] = (by_ed[eds[-1]], eds[-1])
        for e in eds[:-1]:
            compared += 1
            if by_ed[e] != by_ed[eds[-1]]:
                diffs.append((key, e, by_ed[e], eds[-1], by_ed[eds[-1]]))
    for key, by_ed in tot.items():
        eds = [e for e in EDITION_ORDER if e in by_ed]
        for e in eds[:-1]:
            compared += 1
            if by_ed[e] != by_ed[eds[-1]]:
                diffs.append((("TOTAUX",) + key, e, by_ed[e], eds[-1], by_ed[eds[-1]]))
    notes["compared"], notes["diffs"] = compared, diffs
    notes["totals"] = {k: (v[[e for e in EDITION_ORDER if e in v][-1]], [e for e in EDITION_ORDER if e in v][-1]) for k, v in tot.items()}
    return out, mixed


def write_csv(name, header, rows):
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / f"{name}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def meta(ed, kind):
    ark, views = EDITIONS[ed]
    v = views[kind]
    return ed, ark, page_label(ark, v), v


def cmd_build():
    report = {}
    for table, fr in (("muslim", "Population musulmane"), ("jewish", "Population israélite")):
        chk, notes = Checks(), {}
        data = build_indigenous(table, chk, notes)
        rows = []
        for (ctrl, y, ev), (v, ed) in sorted(data.items(), key=lambda kv: (kv[0][1], CONTROLES.index(kv[0][0]), kv[0][2])):
            e, ark, page, view = meta(ed, table)
            rows.append([e, "etat_civil_indigene", ark, page, view, y, ctrl, table, fr, ev,
                         {"births": "Naissances", "deaths": "Décès"}[ev], v,
                         CELL_FLAGS.get((table, ctrl, y, ev), "")])
        n = write_csv(f"vital_{table}_births_deaths",
                      ["census", "table_id", "gallica_ark", "source_page", "gallica_view", "year",
                       "controle_civil", "religion", "religion_fr", "event", "event_fr", "value", "flag"], rows)
        report[table] = (n, chk, notes)
    chk, notes = Checks(), {}
    data, mixed = build_european(chk, notes)
    names = {"marriages": "vital_european_marriages", "births": "vital_european_births",
             "deaths": "vital_european_deaths"}
    for sec, fname in names.items():
        rows = []
        keys = sorted((k for k in data if k[0] == sec), key=lambda k: (k[2], list(NAT).index(k[1]), k[3]))
        for k in keys:
            v, ed = data[k]
            e, ark, page, view = meta(ed, "eur_marriages" if sec == "marriages" else "eur_births_deaths")
            role_fr = {"groom": "Époux", "bride": "Épouses", "male": "Sexe masculin", "female": "Sexe féminin"}[k[3]]
            rows.append([e, "etat_civil_europeen", ark, page, view, k[2], NAT[k[1]], NAT_FR.get(k[1], k[1]),
                         k[3], role_fr, v, ""])
        col = "spouse" if sec == "marriages" else "sex"
        report[sec] = (write_csv(fname, ["census", "table_id", "gallica_ark", "source_page", "gallica_view", "year",
                                         "nationality", "nationality_fr", col, f"{col}_fr", "value", "flag"], rows),)
    mrows = []
    for r in mixed:
        e, ark, page, view = meta(r["edition"], "eur_marriages")
        mrows.append([e, "mariages_mixtes", ark, page, view, r["year"], r["groom"], r["groom_fr"],
                      r["bride"], r["bride_fr"], r["value"], ""])
    report["mixed"] = (write_csv("vital_mixed_marriages",
                                 ["census", "table_id", "gallica_ark", "source_page", "gallica_view", "year",
                                  "groom_group", "groom_group_fr", "bride_group", "bride_group_fr", "value", "flag"],
                                 mrows),)
    report["european"] = (None, chk, notes)
    json.dump({k: {"rows": v[0], "checks": v[1].n if len(v) > 1 else None,
                   "failures": v[1].fail if len(v) > 1 else None,
                   "compared": v[2]["compared"] if len(v) > 2 else None,
                   "differences": [list(map(str, d)) for d in v[2]["diffs"]] if len(v) > 2 else None}
               for k, v in report.items()}, open(OUT / "vital_validation.json", "w"), indent=1, ensure_ascii=False)
    for k, v in report.items():
        print(k, "rows", v[0], *(("checks", v[1].n, "fail", len(v[1].fail), "compared", v[2]["compared"],
                                  "diffs", len(v[2]["diffs"])) if len(v) > 1 else ()))


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "draft":
        cmd_draft(sys.argv[2])
    elif len(sys.argv) > 1 and sys.argv[1] == "build":
        cmd_build()
    else:
        print(__doc__)
