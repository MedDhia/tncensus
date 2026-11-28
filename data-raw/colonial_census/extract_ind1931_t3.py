#!/usr/bin/env python3
"""Extract Table III of the 1931 indigenous census (cheikhats x religion x nationality).

Source: Dénombrement de la population civile indigène (musulmane et israélite)
en Tunisie au 22 mars 1931 (Gallica ark bpt6k994559s), Tableau III "État de la
population indigène par Cheikhats", printed pages 12-97, Gallica views 11-53
(two-page spreads).

Each spread is parsed from Gallica's word-level OCR (see ocr.py). The left page
holds the cheikhat names and the seven Muslim nationality columns; the right
page holds the Muslim total, the seven Jewish nationality columns, the Jewish
total and the grand total. The two pages are grouped into rows separately and
paired in order, because a spread is often scanned with a vertical shift
between its pages.

Every row is checked three ways (Muslim columns sum to the Muslim total, Jewish
columns to the Jewish total, the two totals to the grand total). Every caidat is
also checked against its printed "Totaux", "A reporter" and "Report" lines.
Values the OCR gets wrong were read from the page images and are listed in
CORRECTIONS below, each keyed by view, printed row label and column. Section
headers (caidat, contrôle civil) and cheikhat names were also checked against
the images (NAMES, HEADERS).

Output: csv/ind1931_t3_cheikhat_nationality.csv (one row per cheikhat x
religion x nationality) and csv/ind1931_t3_cheikhat_nationality.md.
"""
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from ocr import ARK_1931, rows, to_int, words  # noqa: E402

VIEWS = range(11, 54)
SPLIT = 2600          # spine of the spread, in OCR column units
NAME_MAX = 1180       # cheikhat names end before this column
NAT = ["tunisian", "algerian", "moroccan", "sudanese", "syrian", "tripolitanian", "other"]
NAT_FR = ["Tunisiens", "Algériens", "Marocains", "Soudanais", "Syriens", "Tripolitains",
          "Autres nationalités"]
# 17 printed columns: 7 Muslim, Muslim total, 7 Jewish, Jewish total, grand total
NCOL = 17
ROW_TOL = 30
# header word -> offset from its centre to the right edge of its column's digits (view 11)
HEAD_L = [(r"^Tun", 0)]
HEAD_R = [(r"^mus", 7), (r"^isr", 15), (r"^G[ÉE]N", 16)]
NO_RIGHT_OCR = {14, 47, 48, 50}   # right page has no Gallica OCR: transcribed from the image

ZERO_JUNK = {"»", "))", ")", "»»", "D", "».", "B", "b", "5»", "*", "y>", "■»", ">", "«", ">>",
             "»)", "))»", "j»", "»j", "»,", "»;", "1»", "»1", "x>", "))>", "Y>", "y", "Ȏ",
             "»>", "(>", ">)", "\"", "»'", "'»", "»•", "•»", "*>", "»:", ":»", "»\"", "»”"}


def page_number(view):
    """Printed page numbers of a spread: view 11 is pages 12-13."""
    left = 2 * view - 10
    return left, left + 1


def parse_num(tok):
    t = tok.strip()
    if t in ZERO_JUNK or re.fullmatch(r"[»)>B\"'•.:;,]+", t):
        return 0
    v = to_int(t)
    return v


def load_words(view):
    """Words with vertical position and horizontal extent (left, right edges)."""
    words(ARK_1931, view)  # fills the cache
    import json
    d = json.loads((HERE.parent / "bnf_gallica" / "ocr" / f"{ARK_1931}_f{view:03d}.json").read_text())
    out = []
    for it in d.get("items", []):
        x, y, w, h = map(int, re.search(r"xywh=(\d+),(\d+),(\d+),(\d+)", it["target"]).groups())
        out.append({"row": x + w / 2, "col": y + h / 2, "l": y, "r": y + h, "text": it["body"]["value"]})
    return out


def is_bracket_junk(w):
    """Short non-numeric fragments left of the value columns: OCR debris of the
    vertical bracket labels (e.g. 'El-Hamma commune'), which would bridge rows."""
    t = w["text"].strip()
    if w["col"] >= 470:
        return False
    if re.fullmatch(r"\(\d\)|\(\d|\d\)", t):
        return False  # footnote markers
    return sum(ch.isalnum() for ch in t) < 3 and not re.search(r"\d", t)


def group_rows(ws, tol):
    """Group words into rows, comparing each word with its row's mean position."""
    ws = sorted(ws, key=lambda w: w["row"])
    out = []
    for w in ws:
        if out and abs(w["row"] - sum(x["row"] for x in out[-1]) / len(out[-1])) < tol:
            out[-1].append(w)
        else:
            out.append([w])
    return [sorted(r, key=lambda w: w["col"]) for r in out]


def is_cell_token(w):
    t = w["text"].strip()
    if not t or re.fullmatch(r"[|\]\[{}~^—–\-_!:;,.]+", t):
        return False
    return sum(ch.isalpha() for ch in t) < 3


def is_digit_token(w):
    return bool(re.fullmatch(r"[\d.,]*\d[\d.,]*", w["text"].strip()))


# Right edges of the 17 columns (digits are right-aligned), measured on view 11.
TEMPLATE = None


def fit_shift(tokens, template, lo=-350, hi=350, tol=22):
    """Shift that best aligns digit right edges with the template."""
    edges = [w["r"] for w in tokens if is_digit_token(w)]
    best = (-1, 0)
    for s in range(lo, hi + 1, 2):
        sc = sum(any(abs(e - (t + s)) <= tol for t in template) for e in edges)
        if sc > best[0]:
            best = (sc, s)
    return best[1]


def zones(template, shift, tol=30):
    re_ = [t + shift for t in template]
    return re_, tol


def assign_zone(tokens, template, shift, tol=32):
    """Column index for each token: right edge in (RE[i-1]+tol, RE[i]+tol]."""
    re_ = [t + shift for t in template]
    cells = [[] for _ in re_]
    stray = []
    for w in tokens:
        for i, e in enumerate(re_):
            lo = re_[i - 1] + tol if i else -10 ** 6
            if lo < w["r"] <= e + tol:
                cells[i].append(w)
                break
        else:
            stray.append(w)
    return cells, stray


def cell_value(toks):
    """Integer value of a cell from its tokens; None if unreadable; 0 if empty."""
    if not toks:
        return 0      # blank cell: '»' not captured by OCR
    texts = [w["text"].strip() for w in sorted(toks, key=lambda w: w["l"])]
    digits = [t for t in texts if re.search(r"\d", t)]
    if not digits:
        vals = [parse_num(t) for t in texts]
        return 0 if all(v == 0 for v in vals) else None
    return parse_num("".join(digits).replace("»", ""))


def learn_template():
    """Right edge of digits in each column, from view 11 (columns with no digit
    there are placed from their '»' marks plus the typical '»'-to-digit gap)."""
    ws = load_words(11)
    rs = rows(ws, 16)
    dig = [[] for _ in range(NCOL)]
    dash = [[] for _ in range(NCOL)]
    for r in rs:
        t = [w for w in r if w["col"] >= NAME_MAX and is_cell_token(w)]
        if len(t) == NCOL:
            for i, w in enumerate(t):
                (dig if is_digit_token(w) else dash)[i].append(w["r"])

    def med(c):
        c = sorted(c)
        return c[len(c) // 2] if c else None

    gaps = [med(d) - med(z) for d, z in zip(dig, dash) if d and z]
    gap = sorted(gaps)[len(gaps) // 2]
    return [med(d) if d else med(z) + gap for d, z in zip(dig, dash)]


HEAD_DELTA = {}


def header_anchor(ws, heads, lo, hi):
    """Shift implied by a column-title word, relative to view 11."""
    global HEAD_DELTA
    if not HEAD_DELTA:
        w11 = load_words(11)
        for pat, col in HEAD_L + HEAD_R:
            m = [w for w in w11 if re.match(pat, w["text"]) and w["row"] < 1300]
            HEAD_DELTA[pat] = TEMPLATE[col] - m[0]["col"]
    for pat, col in heads:
        m = [w for w in ws if re.match(pat, w["text"]) and w["row"] < 1300 and lo <= w["col"] < hi]
        if m:
            # shift such that template edge moves to header centre + delta
            return int(round(m[0]["col"] + HEAD_DELTA[pat] - TEMPLATE[col]))
    return None


def align(lpos, rpos, pred, skip=50, maxd=62, compat=None):
    """Order-preserving alignment of left and right rows by predicted position.

    compat(i, j) returns True when left row i's seven values sum to right row
    j's Muslim total, False when they don't, None when unknown; it makes a
    consistent pair cheaper and an inconsistent one dearer."""
    n, k = len(lpos), len(rpos)
    INF = float("inf")
    D = [[INF] * (k + 1) for _ in range(n + 1)]
    B = [[None] * (k + 1) for _ in range(n + 1)]
    D[0][0] = 0
    for i in range(n + 1):
        for j in range(k + 1):
            if D[i][j] == INF:
                continue
            if i < n and D[i][j] + skip < D[i + 1][j]:
                D[i + 1][j], B[i + 1][j] = D[i][j] + skip, (i, j, None)
            if j < k and D[i][j] + skip < D[i][j + 1]:
                D[i][j + 1], B[i][j + 1] = D[i][j] + skip, (i, j, None)
            if i < n and j < k:
                d = abs(rpos[j] - pred(lpos[i]))
                ok = compat(i, j) if compat else None
                lim = maxd + (60 if ok else 0)
                d = d - 35 if ok else d + (35 if ok is False else 0)
                if abs(rpos[j] - pred(lpos[i])) <= lim and D[i][j] + d < D[i + 1][j + 1]:
                    D[i + 1][j + 1], B[i + 1][j + 1] = D[i][j] + d, (i, j, (i, j))
    out, i, j = [], n, k
    while (i, j) != (0, 0):
        pi, pj, mt = B[i][j]
        if mt:
            out.append(mt)
        i, j = pi, pj
    return out[::-1]


def parse_spread(view):
    """Events in vertical order: (pos, 'row', label, values[17], raw, row_words) or (pos, 'text', text, None, side, words)."""
    global TEMPLATE
    if TEMPLATE is None:
        TEMPLATE = learn_template()
    ltpl, rtpl = TEMPLATE[:7], TEMPLATE[7:]
    ws = load_words(view)
    left = [w for w in ws if w["col"] < SPLIT]
    right = [w for w in ws if w["col"] >= SPLIT]
    left = [w for w in left if not is_bracket_junk(w)]
    lrows, rrows = group_rows(left, ROW_TOL), group_rows(right, ROW_TOL)

    def cells(r, lo, hi):
        return [w for w in r if lo <= w["col"] < hi and is_cell_token(w)]

    def ndig(ts):
        return sum(is_digit_token(w) for w in ts)

    # data rows: at least one digit on the left page among the value columns;
    # at least two digits on the right page (Muslim total and grand total)
    def named(r):
        return any(re.search(r"[A-Za-zÀ-ÿ]{3}", w["text"]) for w in r if w["col"] < NAME_MAX)

    # rows whose Muslim cells are all '»' (e.g. "Israélites de Gabès") count too
    ldata = [r for r in lrows if r[-1]["row"] > 1100 and (ndig(cells(r, NAME_MAX, SPLIT)) >= 1 or (
        named(r) and len(cells(r, NAME_MAX, SPLIT)) >= 3))]
    rdata = [r for r in rrows if ndig(cells(r, SPLIT, 10 ** 6)) >= 1 and r[-1]["row"] > 1100
             and not any(re.search(r"[A-Za-zé]{3}", w["text"]) for w in r)]
    def anchor(rs, lo, hi, first):
        edges = []
        for r in rs:
            d = [w for w in cells(r, lo, hi) if is_digit_token(w)]
            if d:
                edges.append(min(d, key=lambda w: w["l"])["r"])
        edges.sort()
        return int(edges[len(edges) // 2] - first)

    hl = header_anchor(ws, HEAD_L, 0, SPLIT)
    la = hl if hl is not None else anchor(ldata, NAME_MAX, SPLIT, ltpl[0])
    if view in NO_RIGHT_OCR:
        events = []
        for lr in ldata:
            lsh = fit_shift([w for r in ldata for w in cells(r, NAME_MAX, SPLIT)], ltpl, la - 40, la + 40)
            lc, ls = assign_zone(cells(lr, NAME_MAX, SPLIT), ltpl, lsh)
            vals = [cell_value(c) for c in lc] + [None] * 10
            name = " ".join(w["text"] for w in lr if w["col"] < NAME_MAX)
            raw = " ".join(w["text"] for w in lr if w["col"] >= NAME_MAX)
            ct = [[w["text"].strip() for w in c] for c in lc] + [[] for _ in range(10)]
            events.append((lr[0]["row"], "row", name, vals, raw, lr, ls, ct, None))
        used = {id(w) for r in ldata for w in r}
        for r in lrows:
            if not any(id(w) in used for w in r):
                events.append((r[0]["row"], "text", " ".join(w["text"] for w in r), None, "L", r, []))
        events.sort(key=lambda e: e[0])
        return events, la, None
    hr = header_anchor(ws, HEAD_R, SPLIT, 10 ** 6)
    ra = hr if hr is not None else anchor(rdata, SPLIT, 10 ** 6, rtpl[0])
    lshift = fit_shift([w for r in ldata for w in cells(r, NAME_MAX, SPLIT)], ltpl, la - 40, la + 40)
    rshift = fit_shift([w for r in rdata for w in cells(r, SPLIT, 10 ** 6)], rtpl, ra - 40, ra + 40)
    # drop left rows whose only digits sit outside the value columns (footnote lines)
    events = []
    lpos = [r[0]["row"] for r in ldata]
    rpos = [r[0]["row"] for r in rdata]

    def match(d, tol=30):
        out, j = [], 0
        for i, p in enumerate(lpos):
            while j < len(rpos) and rpos[j] - d < p - tol:
                j += 1
            if j < len(rpos) and abs(rpos[j] - d - p) <= tol:
                out.append((i, j))
                j += 1
        return out

    best = max(range(-200, 201, 2), key=lambda d: (len(match(d)), -abs(d)))
    m0 = match(best)
    # linear drift between the pages (scan skew): r = a + b * l
    if len(m0) >= 3:
        xs = [lpos[i] for i, _ in m0]
        ys = [rpos[j] for _, j in m0]
        mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
        sxx = sum((x - mx) ** 2 for x in xs) or 1
        b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
        a = my - b * mx
    else:
        a, b = best, 1.0
    lsum = []
    for r in ldata:
        lc, _ = assign_zone(cells(r, NAME_MAX, SPLIT), ltpl, lshift)
        vv = [cell_value(c) for c in lc]
        lsum.append(None if None in vv else sum(vv))
    rtot = []
    for r in rdata:
        rc, _ = assign_zone(cells(r, SPLIT, 10 ** 6), rtpl, rshift)
        rtot.append(cell_value(rc[0]) if rc[0] else None)

    def compat(i, j):
        if lsum[i] is None or rtot[j] is None:
            return None
        return lsum[i] == rtot[j]

    m = align(lpos, rpos, lambda p: a + b * p, compat=compat)
    pairs = [(ldata[i], rdata[j]) for i, j in m]
    mi, mj = {i for i, _ in m}, {j for _, j in m}
    for i, r in enumerate(ldata):
        if i not in mi:
            events.append((r[0]["row"], "text", "UNPAIRED-L " + " ".join(w["text"] for w in r), None, "L", r, []))
    for j, r in enumerate(rdata):
        if j not in mj:
            events.append((r[0]["row"] - best, "text", "UNPAIRED-R " + " ".join(w["text"] for w in r), None, "R", r, []))
    for lr, rr in pairs:
        lc, ls = assign_zone(cells(lr, NAME_MAX, SPLIT), ltpl, lshift)
        rc, rs_ = assign_zone(cells(rr, SPLIT, 10 ** 6), rtpl, rshift)
        vals = [cell_value(c) for c in lc] + [cell_value(c) for c in rc]
        name = " ".join(w["text"] for w in lr if w["col"] < NAME_MAX)
        raw = " ".join(w["text"] for w in lr if w["col"] >= NAME_MAX) + " || " + " ".join(w["text"] for w in rr)
        ct = [[w["text"].strip() for w in c] for c in lc + rc]
        events.append((lr[0]["row"], "row", name, vals, raw, lr + rr, ls + rs_, ct,
                       sum(w["row"] for w in rr) / len(rr)))
    used = {id(w) for r in ldata + rdata for w in r}
    vshift = best
    for r in lrows + rrows:
        if not any(id(w) in used for w in r):
            side = "L" if r[0]["col"] < SPLIT else "R"
            events.append((r[0]["row"] - (vshift if side == "R" else 0), "text", " ".join(w["text"] for w in r), None, side, r, []))
    events.sort(key=lambda e: e[0])
    return events, lshift, rshift


def check(vals):
    """Row checks: Muslim sum, Jewish sum, grand total. Returns list of failed check names."""
    if any(v is None for v in vals[:7]):
        return ["unreadable"]
    if any(v is None for v in vals):
        return ["right_missing"]
    bad = []
    if sum(vals[0:7]) != vals[7]:
        bad.append("muslim")
    if sum(vals[8:15]) != vals[15]:
        bad.append("jewish")
    if vals[7] + vals[15] != vals[16]:
        bad.append("grand")
    return bad


# ---------------------------------------------------------------------------
# Structure: caidat / contrôle context, row kinds, block checks

import difflib
import unicodedata

# Caidats as listed in the table of contents (printed page 4-5), in order.
CAIDATS = ["Aïn-Draham", "Aradh", "Béja", "Bizerte", "Djebeniana", "Djelass", "Djerba", "Djerid",
           "Fraichiches", "Gafsa", "Hammama", "Kairouan", "La Skhira", "Kef", "Madjeurs", "Mahdia",
           "Mateur", "Matmata", "Medjez-el-Bab", "Monastir", "Nabeul", "Nefzaoua", "Ouerghemma",
           "Oulad-Aoun", "Oulad-Ayar", "Sfax", "Soliman", "Souassi", "Souk-el-Arba", "Souk-el-Khemis",
           "Sousse", "Tadjerouine", "Tatahouine", "Téboursouk", "Tunis-Banlieue", "Tunis-Ville",
           "Zaghouan"]
CONTROLES = ["Béja", "Bizerte", "Djerba", "Gabès", "Gafsa", "Grombalia", "Kairouan", "Le Kef", "Maktar",
             "Medjez-el-Bab", "Sfax", "Souk-el-Arba", "Sousse", "Tabarka", "Thala", "Téboursouk",
             "Tozeur", "Tunis", "Zaghouan"]


def squash(t):
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z]", "", t)


def best_in(text, names, min_ratio=0.75):
    """Name from `names` that best matches a substring of `text` (both squashed)."""
    st = squash(text)
    best = (0, None)
    for n in names:
        sn = squash(n)
        L = len(sn)
        for i in range(0, max(1, len(st) - L + 1)):
            r = difflib.SequenceMatcher(None, st[i:i + L + 1], sn).ratio()
            if r > best[0]:
                best = (r, n)
    return best[1] if best[0] >= min_ratio else None


def row_kind(label):
    q = squash(label)
    if "reporter" in q or "areport" in q:
        return "carry_out"
    if q.startswith("report") or q.endswith("report"):
        return "carry_in"
    if "totaux" in q or q.startswith("total"):
        return "total"
    return "cheikhat"


def is_caidat_header(text):
    q = squash(text)
    return bool(re.search(r"[cg]a[il]d[ae]|aidat|caid", q)) and not re.search(r"\d{3}", text)


# Contrôle civil (or military territory) printed in each caidat's header, e.g.
# "Caïdat de Nefzaoua (Territoire militaire de Kebili)". Read from the images.
CONTROLE_OF = {
    "Aïn-Draham": "Tabarka", "Aradh": "Gabès", "Béja": "Béja", "Bizerte": "Bizerte",
    "Djebeniana": "Sfax", "Djelass": "Kairouan", "Djerba": "Djerba", "Djerid": "Tozeur",
    "Fraichiches": "Thala", "Gafsa": "Gafsa", "Hammama": "Gafsa", "Kairouan": "Kairouan",
    "La Skhira": "Sfax", "Kef": "Le Kef", "Madjeurs": "Thala", "Mahdia": "Sousse",
    "Mateur": "Bizerte", "Matmata": "Territoire militaire de Matmata",
    "Medjez-el-Bab": "Medjez-el-Bab", "Monastir": "Sousse", "Nabeul": "Grombalia",
    "Nefzaoua": "Territoire militaire de Kebili",
    "Ouerghemma": "Cercles de Médenine, Ben-Gardane et Zarzis",
    "Oulad-Aoun": "Maktar", "Oulad-Ayar": "Maktar", "Sfax": "Sfax", "Soliman": "Grombalia",
    "Souassi": "Sousse", "Souk-el-Arba": "Souk-el-Arba", "Souk-el-Khemis": "Souk-el-Arba",
    "Sousse": "Sousse", "Tadjerouine": "Le Kef", "Tatahouine": "Cercle militaire de Tatahouine",
    "Téboursouk": "Téboursouk", "Tunis-Banlieue": "Tunis", "Tunis-Ville": "Tunis",
    "Zaghouan": "Zaghouan",
}
# Caidat header exactly as printed (after "Caïdat")
CAIDAT_FR = {
    "Aïn-Draham": "Caïdat d'Aïn-Draham", "Aradh": "Caïdat de l'Aradh", "Kef": "Caïdat du Kef",
    "Djelass": "Caïdat des Djelass", "Djerid": "Caïdat du Djerid", "Fraichiches": "Caïdat des Fraichiches",
    "Hammama": "Caïdat des Hammama", "Madjeurs": "Caïdat des Madjeurs", "Ouerghemma": "Caïdat des Ouerghemma",
    "Oulad-Aoun": "Caïdat des Oulad-Aoun", "Oulad-Ayar": "Caïdat des Oulad-Ayar", "Souassi": "Caïdat des Souassi",
}


def structure():
    """All Table III rows with view, position, caidat, contrôle, kind, label, values.

    Caidats follow the order of the table of contents; each ends at its printed
    "Totaux" row (there is exactly one per caidat).
    """
    recs = []
    k = 0
    for v in VIEWS:
        ev, _, _ = parse_spread(v)
        for e in ev:
            if e[1] != "row":
                continue
            kind = row_kind(e[2])
            lw = [w for w in e[5] if w["col"] < SPLIT]
            recs.append({"view": v, "pos": e[0], "caidat": CAIDATS[k], "controle": CONTROLE_OF[CAIDATS[k]],
                         "kind": kind, "label": e[2], "values": list(e[3]), "raw": e[4], "cells": e[7],
                         "lpos": sum(w["row"] for w in lw) / len(lw), "rpos": e[8], "flags": {}})
            fix_nines(recs[-1])
            fill_single(recs[-1])
            if kind == "total":
                k += 1
    assert k == len(CAIDATS), k
    return apply_corrections(recs)


# Values read from the page images where the OCR is wrong or missing, keyed by
# (view, squashed OCR label). Each entry gives all 17 printed values in order
# (7 Muslim nationalities, Muslim total, 7 Jewish nationalities, Jewish total,
# grand total), "DROP" for an OCR artefact that is not a table row, or a dict
# with "values" and/or "label" (corrected cheikhat name) and "note".
CORRECTIONS = {}


def label_key(label):
    t = unicodedata.normalize("NFKD", label)
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]", "", t)[:16]


def C(view, label, vals=None, name=None, note=None, nth=0, printed_mismatch=False, duplicate=False):
    """printed_mismatch: the printed row itself does not add up (kept as printed)."""
    key = (view, label_key(label), nth)
    e = {}
    if vals == "DROP":
        e = "DROP"
    else:
        if vals:
            v = [int(x) for x in vals.split()]
            assert len(v) == NCOL, (view, label, v)
            assert bool(check(v)) == printed_mismatch, (view, label, v, check(v))
            e["values"] = v
            e["mismatch"] = check(v)
        if name:
            e["label"] = name
        if note:
            e["note"] = note
        if duplicate:
            e["duplicate"] = True
    assert key not in CORRECTIONS, key
    CORRECTIONS[key] = e


# sheet 0
C(11, "El-Ajarda et El-Ghouanem....", "1643 0 0 0 0 0 0 1643 0 0 0 0 0 0 0 0 1643")
C(11, "El-Hamran et Ed-Debabsa", "2750 0 7 0 0 0 0 2757 0 0 0 0 0 0 0 0 2757")
C(11, "Totaux", "37388 482 22 20 0 18 0 37930 31 0 0 0 0 0 0 31 37961")
C(12, "A reporter ...", "37578 31 2 84 0 39 0 37734 2912 0 0 0 0 5 0 2917 40651")
C(13, "Zarkine '", "2186 0 0 0 0 38 0 2224 15 0 0 0 0 0 0 15 2239")
C(13, "Beni-Saïd", "1928 22 0 0 0 10 0 1960 0 0 0 0 0 0 0 0 1960")
C(13, "Bou-Hezam", "4517 69 34 0 0 8 0 4628 0 0 0 0 0 0 0 0 4628")
C(14, "", "DROP")
C(14, "Report", "20999 299 110 3 0 46 0 21457 986 0 0 0 0 0 0 986 22443")
C(14, "Messatria", "1555 0 0 0 0 0 0 1555 0 0 0 0 0 0 0 0 1555")

# sheet 1
C(14, "Zouagha", "4236 174 4 0 0 27 0 4441 0 0 0 0 0 0 0 0 4441")
C(15, "Trabelsia", "1765 346 0 0 0 67 0 2178 0 0 0 0 0 0 0 0 2178")
C(16, "Chebba", "5777 33 13 0 0 21 0 5844 76 0 0 0 0 0 0 76 5920")
C(16, "Totaux |", "49512 33 20 0 0 995 0 50560 76 0 0 0 0 0 0 76 50636")
C(17, "Beïn-el-Adjebel", "4454 0 2 0 0 120 0 4576 0 0 0 0 0 0 0 0 4576")
C(17, "Messaïd. . .", "2804 8 2 0 0 2 0 2816 0 0 0 0 0 0 0 0 2816")
C(17, "Oulad-El-Hadj-Kaoub", "2742 11 0 0 0 9 0 2762 0 0 0 0 0 0 0 0 2762")
C(17, "Ouled Negguez", "2158 0 6 0 0 6 0 2170 0 0 0 0 0 0 0 0 2170")
C(19, "El-Hamma", "2178 94 0 0 0 0 0 2272 6 0 0 0 0 0 0 6 2278")
C(19, "Oule'd Aïssa et Brahmia", "2626 11 0 0 0 0 0 2637 0 0 0 0 0 0 0 0 2637", name="Ouled Aïssa et Brahmia")

# sheet 2 (values confirmed on the image; names wrap onto two lines)
C(19, "Ouled Majed", name="Ouled Majed")
C(19, "Ouled-el-Hadef", name="Ouled-el-Hadef")
C(20, "(3)", name="Gafsa Nord (partie communale)", note="(3)")
C(21, "Report", "18478 242 8 0 0 1684 0 20412 724 0 0 0 0 0 0 724 21136")
C(21, "Gafsa Nord (partie' rurale)", name="Gafsa Nord (partie rurale)", note="(1)")
C(21, "Oule'd Bou Amrane.'", "977 0 0 0 0 0 0 977 0 0 0 0 0 0 0 0 977", name="Ouled Bou Amrane")
C(21, "munale) ( 2 )", name="Ouled Mabrouk (partie communale)", note="(2)")
C(21, "2", "2648 1534 304 0 0 3217 0 7703 0 0 0 0 0 0 0 0 7703", name="Ouled Mabrouk (partie rurale)", note="(2)")
C(21, "Yahia", name="Ouled M'barek et Ouled Bou-Yahia")
C(21, "Ouled Mansour", name="Ouled Mansour")

# sheet 3
C(21, "Ouled Naceur", name="Ouled Naceur")
C(21, "Ouled Ouceïf", name="Ouled Ouceïf")
C(21, "Ouled Bedhouane 1", name="Ouled Redhouane")
C(21, "Sened", name="Sened")
C(22, "Henia", "3004 0 0 0 0 0 0 3004 0 0 0 0 0 0 0 0 3004")
C(23, "Driât", name="Driât")
C(23, "A reporter", "16230 2 0 0 0 16 0 16248 0 0 0 0 0 0 0 0 16248")
C(24, "El-Metbasseta..", "1475 0 0 0 0 11 0 1486 0 0 0 0 0 0 0 0 1486")

# Kairouan: two bracket groups; '—' repeats "(partie rurale)" / "(partie comm.)"
KB, KV = "Kairouan-Banlieue (1)", "Kairouan-Ville (2)"
C(24, "Houmet El—Arhraf (partie rurale)", name="Houmet El-Achraf (partie rurale)", note=KB)
C(24, "Houmet Ej-Jeblia", "1468 0 0 0 0 0 0 1468 0 0 0 0 0 0 0 0 1468", name="Houmet Ej-Jeblia (partie rurale)", note=KB)
C(24, "•55 lloumet El-Gucblia —", name="Houmet El-Gueblia (partie rurale)", note=KB)
C(24, "£3 1 Houmet El-Djemaâ —", name="Houmet El-Djemaâ (partie rurale)", note=KB)
C(24, "lloumet El-Achraf (partie comm.).", name="Houmet El-Achraf (partie communale)", note=KV)
C(24, "Houmet Ej-Jeblia —", name="Houmet Ej-Jeblia (partie communale)", note=KV, nth=1)
C(24, "Houmet El-Cueblla", name="Houmet El-Gueblia (partie communale)", note=KV)
C(24, "Houmet El-Djcmaâ —", name="Houmet El-Djemaâ (partie communale)", note=KV)

# rev3 sheet 0
C(15, "Totaux", "63537 3529 70 8 0 440 1 67585 1290 32 0 0 0 0 0 1322 68907")
C(25, "Aouin", "1405 0 0 0 0 0 0 1405 0 0 0 0 0 0 0 0 1405")
C(25, "Chematra", "2453 0 13 0 0 48 0 2514 0 0 0 0 0 0 0 0 2514")
C(25, "Dekh allia", "1991 0 0 0 0 6 0 1997 0 0 0 0 0 0 0 0 1997", name="Dekhaïlia")
C(25, "El-Atayat", "3355 0 0 0 0 0 0 3355 0 0 0 0 0 0 0 0 3355")
C(25, "El-Hadara", "1123 6 0 4 0 11 0 1144 0 0 0 0 0 0 0 0 1144")
C(25, "El-Keraïma", "1621 0 0 0 0 0 0 1621 0 0 0 0 0 0 0 0 1621")
C(25, "El-Krata", "1784 0 0 0 0 0 0 1784 0 0 0 0 0 0 0 0 1784")
C(25, "El-Letaïfa", "1271 0 0 0 0 0 0 1271 0 0 0 0 0 0 0 0 1271")

# rev3 sheet 1
C(25, "Er-Re’baïa", "1695 0 0 0 0 0 0 1695 0 0 0 0 0 0 0 0 1695", name="Er-Rebaïa")
C(25, "Gheraïba", "1111 0 0 0 0 41 0 1152 0 0 0 0 0 0 0 0 1152")
C(25, "Maharès P)", "3621 5 0 0 0 107 0 3733 53 0 0 0 0 0 0 53 3786", name="Maharès", note="(1)")
C(25, "Ouled Ghida", "1339 0 0 0 0 41 0 1380 0 0 0 0 0 0 0 0 1380")
C(25, "Ouled-Hadj-Moussa", "885 0 0 0 0 48 0 933 0 0 0 0 0 0 0 0 933")
C(25, "Ouled-Hamed", "2298 0 0 0 0 0 0 2298 0 0 0 0 0 0 0 0 2298")
C(25, "Ouled-M’Hammed", "1663 0 0 0 0 61 0 1724 0 0 0 0 0 0 0 0 1724", name="Ouled-M'Hammed")
C(25, "Semaâla.. .*", "1752 0 0 0 0 0 0 1752 0 0 0 0 0 0 0 0 1752", name="Semaâla")
C(25, "Totaux", "29367 11 13 4 0 363 0 29758 53 0 0 0 0 0 0 53 29811")
C(26, "El-Ghorfa Sud )", "2696 51 0 0 0 0 0 2747 0 0 0 0 0 0 0 0 2747", name="El-Ghorfa Sud", note="(2)")

# rev3 sheet 2
C(26, "El-Ghorfa Nord ) ........", name="El-Ghorfa Nord", note="(2)")
C(26, "El-Mardj'a", "2361 59 1 0 0 0 0 2421 16 0 0 0 0 0 0 16 2437", name="El-Mardja")
C(27, "Oued-Remel", "2358 200 0 0 0 0 0 2558 0 0 0 0 0 0 0 0 2558")
C(29, "Rejïch", "1979 0 0 0 0 0 0 1979 0 0 0 0 0 0 0 0 1979")
C(29, "Sidi-Assaker", "3695 0 4 0 0 35 0 3734 0 0 0 0 0 0 0 0 3734")
# printed Muslim total 70.491, but its parts sum to 70.490
C(29, "Totaux", "69971 2 52 0 0 465 0 70491 477 0 0 0 0 0 0 477 70968", printed_mismatch=True)
C(30, "Neffat", "1621 370 0 0 0 208 0 2199 0 0 0 0 0 0 0 0 2199")
C(31, "Chaouache", "3608 152 0 0 0 0 0 3760 0 0 0 0 0 0 0 0 3760")
C(31, "0 lad-Abd-Ennour", "1989 42 0 0 0 0 0 2031 0 0 0 0 0 0 0 0 2031", name="Oulad-Abd-Ennour")
C(31, "Oued-Zarga", "5012 0 0 0 0 0 0 5012 9 0 0 0 0 0 0 9 5021")

# rev3 sheet 3
C(31, "Testour et Ouled-S’lama", name="Testour et Ouled-S'lama")
C(33, "Lamta", "1413 0 0 0 0 0 0 1413 0 0 0 0 0 0 0 0 1413")
C(34, "Tazeghrane", "2141 0 0 0 0 0 0 2141 0 0 0 0 0 0 0 0 2141")
C(35, "Totaux", "34554 119 0 0 0 67 0 34740 372 0 0 0 0 0 0 372 35112")
C(37, "El-Khelaïfa \\", "508 0 0 0 0 137 0 645 240 0 0 0 0 16 0 256 901", name="El-Khelaïfa")
C(37, "Zarzis El-Mouansa", "657 0 0 0 0 0 0 657 0 0 0 0 0 0 0 0 657", name="El-Mouansa")
C(37, "Ez-Zaouia M ....", "523 9 0 0 0 31 0 563 13 0 0 0 0 0 0 13 576", name="Ez-Zaouia")
C(37, "Ouled-Bou-Ali", "3431 17 0 0 0 80 0 3528 500 0 0 0 0 0 0 500 4028")

# rev3 sheet 4
C(37, "Ouled-M’hamed ] |", name="Ouled-M'hamed")
C(37, "Ouled-Saïd", name="Ouled-Saïd")
C(37, "Totaux", "69199 50 0 0 0 820 0 70069 1838 0 0 0 0 16 0 1854 71923")
C(38, "Cheikhat des Algériens", name="Cheikhat des Algériens")
C(39, "El-Mansoura", "1627 1 1 0 0 2 0 1631 0 0 0 0 0 0 0 0 1631")

C(21, "", name="Gafsa Sud (partie communale)", note="(1)")
# rev4 sheet 0
C(36, "< rania de Ben-Gardane", name="Oulad-Aounallah et Barrania de Ben-Gardane")
C(36, "Cercle Rebaya et Aouine", name="Rebaya et Aouine")
C(40, "El-Araba", "1871 0 0 0 0 106 0 1977 0 0 0 0 0 0 0 0 1977")
C(40, "raie)", name="Merkez-Ben-Halima (partie rurale)")
C(40, "raie)", name="Merkez-Kammoun (partie rurale)", nth=1)
C(40, "Sakiet-ed-Daïr", "10957 0 0 0 0 203 0 11160 0 0 0 0 0 0 0 0 11160")
C(40, "Sakiet-Ez-Zit (partie rurale) t.", "10982 0 2 0 0 301 0 11285 0 0 0 0 0 0 0 0 11285",
  name="Sakiet-Ez-Zit (partie rurale)")
C(40, "Traka.", name="Traka")
C(41, "Sfax-Est", "6065 37 27 37 0 123 10 6299 0 0 0 0 0 0 0 0 6299")

# rev4 sheet 1
C(41, "] (partie communale)...", name="Merkez-Ben-Halima (partie communale)")
C(41, "j Merkez-Demak", "1019 0 9 4 0 888 0 1920 0 0 0 0 0 0 0 0 1920", name="Merkez-Demak")
C(41, "! tie communale)", name="Merkez-Kammoun (partie communale)")
C(41, "munale)", name="Sakiet-Ez-Zit (partie communale)")
C(41, "Israélites", "0 0 0 0 0 0 0 0 2984 0 0 0 0 72 2 3058 3058")
C(41, "Nianou....", "2176 0 0 0 0 0 0 2176 0 0 0 0 0 0 0 0 2176", name="Nianou")
C(41, "Soliman", "7393 37 10 0 0 0 0 7440 137 0 0 0 0 0 0 137 7577")
C(42, "Chehimate", "3383 0 0 0 0 7 0 3390 0 0 0 0 0 0 0 0 3390")
C(42, "El-Frada", "1713 0 0 0 0 0 0 1713 0 0 0 0 0 0 0 0 1713")
C(42, "Hebira", "2440 0 0 0 0 21 0 2461 0 0 0 0 0 0 0 0 2461")

# rev4 sheet 2
C(43, "Ghardimaou (Banlieue). )", "4804 487 0 0 0 0 0 5291 0 0 0 0 0 0 0 0 5291", name="Ghardimaou (Banlieue)", note="(1)")
C(43, "Ghardimaou (Ville). )", "257 157 0 0 0 0 0 414 5 0 0 0 0 0 0 5 419", name="Ghardimaou (Ville)", note="(1)")
C(43, "Hakim", "4114 37 2 0 0 0 0 4153 0 0 0 0 0 0 0 0 4153")
C(46, "Sousse (Ville) )", "12972 60 85 0 0 181 0 13298 3479 98 0 0 0 95 0 3672 16970", name="Sousse (Ville)", note="(1)")
C(49, "Dougga", "2314 259 44 0 0 0 0 2617 0 0 0 0 0 0 0 0 2617")
C(53, "Zaghouan (Ville) J", "3249 0 0 0 0 0 0 3249 7 0 0 0 0 0 0 7 3256", name="Zaghouan (Ville)", note="(1)")

C(12, "Israélites de Gabès", "0 0 0 0 0 0 0 0 2454 0 0 0 0 5 0 2459 2459")

C(37, "Report", "40254 1 0 0 0 314 0 40569 994 0 0 0 0 0 0 994 41563")
C(49, "Djouaouda....", "3210 601 43 0 0 0 0 3854 0 0 0 0 0 0 0 0 3854", name="Djouaouda")
C(53, "Totaux", "42033 194 60 3 0 1413 0 43703 7 0 0 0 0 0 0 7 43710")


def Z(view, label, mus, jew="", grand=None, **kw):
    """Shorthand: the 7 Muslim and 7 Jewish cells as read; the three totals are
    computed and must equal the printed grand total `grand`."""
    m = [int(x) for x in mus.split()]
    j = [int(x) for x in jew.split()] if jew else [0] * 7
    assert len(m) == 7 and len(j) == 7
    g = sum(m) + sum(j)
    assert grand is None or g == grand, (view, label, g, grand)
    C(view, label, " ".join(map(str, m + [sum(m)] + j + [sum(j), g])), **kw)


# view 14: right page has no OCR; both pages read from the image
Z(14, "El-Feraïdjia", "2033 17 0 0 0 0 0", grand=2050)
Z(14, "El-Ghe'raba", "2061 0 0 0 0 0 0", "3 0 0 0 0 0 0", 2064, name="El-Gheraba")
Z(14, "El-Hebaba", "1208 0 0 0 0 0 0", grand=1208)
Z(14, "El-Munchar", "4553 45 0 0 0 32 0", grand=4630)
Z(14, "Et-Tarhouni", "2238 5 0 0 0 0 0", grand=2243)
Z(14, "Fatnassa", "2989 30 0 0 0 0 0", grand=3019)
Z(14, "Gram et Kouka", "2916 0 0 0 0 0 0", grand=2916)
Z(14, "Kodhaâ,", "1704 0 0 0 0 2 0", grand=1706, name="Kodhaâ")
Z(14, "Messaâdia", "1236 0 0 0 0 0 0", grand=1236)
Z(14, "Ouchtata", "2632 8 0 0 0 0 0", grand=2640)
Z(14, "Ouled-bou-Ab", "1310 0 0 0 0 0 0", grand=1310, name="Ouled-bou-Ali")
Z(14, "Ouled-Gacem", "1982 0 0 0 0 13 0", grand=1995)
Z(14, "Ouled-Ghezia", "970 0 0 0 0 0 0", grand=970)
Z(14, "Ouled-Houimel", "1170 0 0 0 0 0 0", grand=1170)
Z(14, "Ouled-Moussa", "2437 2 0 0 0 0 0", grand=2439)
Z(14, "Ouled-Salem", "2299 0 0 0 0 1 0", grand=2300)
Z(14, "Remadhnia", "1766 0 0 0 0 0 0", grand=1766)
Z(14, "Sidi-es-Sehili", "2608 13 0 0 0 3 0", grand=2624)
Z(14, "Tebaba", "3692 0 0 0 0 0 0", grand=3692)
Z(14, "Zaouit Médien", "1785 0 0 0 0 0 0", grand=1785)
Z(14, "Totaux", "70379 593 114 3 0 124 0", "989 0 0 0 0 0 0", 72202)

# view 47 (Tadjerouine): right page has no OCR
Z(47, "Aïn-Kessiba", "2135 6 3 0 0 7 0", grand=2151)
Z(47, "Banou", "1685 53 0 0 0 3 0", grand=1741)
Z(47, "Besseriana", "1223 31 0 0 0 0 0", grand=1254)
Z(47, "Djerda", "1705 251 0 0 0 26 0", grand=1982)
Z(47, "Djezza", "1567 204 0 0 0 9 0", grand=1780)
Z(47, "El-Adjerda", "1753 185 0 0 0 0 0", grand=1938)
Z(47, "El-Falta", "3152 143 0 0 0 0 0", grand=3295)
Z(47, "El-Houdh", "3170 214 2 0 0 21 0", grand=3407)
Z(47, "El-Ksour", "1172 0 0 0 0 0 0", grand=1172)
Z(47, "El-Maskhia.", "3005 143 41 0 0 48 0", grand=3237, name="El-Maskhia")
Z(47, "Ez-Zouarine", "2455 26 0 0 0 0 0", grand=2481)
Z(47, "Guern-Alfaya", "3319 214 5 0 0 8 0", grand=3546)
Z(47, "Kalaât-Senan", "4561 851 8 0 0 23 0", grand=5443)
Z(47, "Koudiat-Echaïr", "2076 1 0 0 0 0 0", grand=2077)
Z(47, "Mezita", "2589 48 0 0 0 0 0", grand=2637)
Z(47, "Sidi-Abd-El-Basset", "2291 125 0 0 0 0 0", grand=2416)
Z(47, "Sidi-Abmed-Essalah", "1960 52 1 0 0 3 0", grand=2016, name="Sidi-Ahmed-Essalah")
Z(47, "Sidi-Barkat", "2733 24 0 0 0 0 0", grand=2757)
Z(47, "Sidi-Metir", "2864 373 0 0 0 0 0", grand=3237)
Z(47, "Slata", "3005 210 49 0 0 333 0", grand=3597)
Z(47, "Tadjerouine '", "2550 135 21 0 0 10 4", "11 0 0 0 0 0 0", 2731, name="Tadjerouine")
Z(47, "Totaux", "50970 3289 130 0 0 491 4", "11 0 0 0 0 0 0", 54895)

# view 48 (Tatahouine): right page has no OCR
Z(48, "Chenini", "909 0 0 0 0 4 0", grand=913)
Z(48, "Deghaghra", "3390 0 0 0 0 0 0", grand=3390)
Z(48, "Dehibat", "1096 0 0 0 0 0 0", grand=1096)
Z(48, "Donirat", "3055 0 0 0 0 65 0", grand=3120, name="Douirat")
Z(48, "El-Ababsa", "2358 0 0 0 0 0 0", grand=2358)
Z(48, "El-Amarna", "2103 0 0 0 0 0 0", grand=2103)
Z(48, "El-Adjarda", "747 0 0 0 0 4 0", grand=751)
Z(48, "El-Hamidia", "1633 0 0 0 0 0 0", grand=1633)
Z(48, "El-Hadada et Hamdoun", "3086 0 0 0 0 16 0", grand=3102)
Z(48, "El-Kraclioua", "2420 0 0 0 0 0 0", grand=2420, name="El-Krachoua")
Z(48, "Garmassa", "972 0 0 0 0 0 0", grand=972)
Z(48, "Ghomrassen-Ville", "259 3 0 0 0 49 0", grand=311)
Z(48, "Ghomrassen-Hedada", "4236 0 0 0 0 4 0", grand=4240)
Z(48, "Guetoufa", "2180 0 0 0 0 16 0", grand=2196)
Z(48, "Jelidet-Beni-Belal", "3028 0 0 0 0 0 0", grand=3028)
Z(48, "Jelidet-Tataouine", "3646 0 0 0 0 0 0", grand=3646)
Z(48, "Ouled-Chihida .", "3609 0 0 0 0 76 0", grand=3685, name="Ouled-Chihida")
Z(48, "Ouled-Dabbab", "3158 0 0 0 0 42 0", grand=3200)
Z(48, "Tataouine (Ville)", "531 0 0 27 0 4 0", "531 0 0 0 0 0 0", 1093)
Z(48, "Zourgane", "2423 0 0 0 0 0 0", grand=2423)
Z(48, "Totaux", "44839 3 0 27 0 280 0", "531 0 0 0 0 0 0", 45680)

# view 50 (Tunis-Banlieue): right page has no OCR
Z(50, "Aïn-Ghelal", "3465 512 0 0 0 87 0", grand=4064)
Z(50, "Ariana", "5453 0 0 0 0 0 0", "2637 0 0 0 0 0 0", 8090)
Z(50, "Bordj-El-Ameri", "3227 92 0 0 0 161 0", grand=3480)
Z(50, "Bordj-Et-Toumi", "2786 3 4 0 0 191 0", grand=2984)
Z(50, "Cebala", "4628 0 0 0 0 29 0", grand=4657)
Z(50, "Djedeïda", "3404 310 0 0 0 0 0", grand=3714)
Z(50, "El-Mellassine (P", "2127 0 0 0 0 0 0", grand=2127, name="El-Mellassine", note="(1)")
Z(50, "El-Mornaguia", "3306 0 0 0 0 0 0", grand=3306)
Z(50, "Kalaât-Landleuss", "3699 17 0 0 0 0 0", grand=3716)
Z(50, "Goulette et Le Kram( 2 )...", "3443 138 19 0 0 266 2", "842 0 1 0 0 0 0", 4711,
  name="La Goulette et Le Kram", note="(2)")
Z(50, "Marsa et Sidi-Bou-Saïd....", "6120 97 48 0 9 81 2", "285 0 0 0 0 0 0", 6642,
  name="La Marsa et Sidi-Bou-Saïd")
Z(50, "Lansarine", "3414 0 0 0 0 39 0", grand=3453)
Z(50, "Manouba", "3805 0 0 0 0 0 0", grand=3805)
Z(50, "Mohamedia", "4903 0 0 0 0 365 0", grand=5268)
Z(50, "Mornag", "5139 0 0 0 0 0 0", grand=5139)
Z(50, "Radès et Hammam-Lif ( 3 )", "7365 101 0 0 0 711 0", "283 0 0 0 0 0 0", 8460,
  name="Radès et Hammam-Lif", note="(3)")
Z(50, "Tébourba", "5667 0 0 0 0 71 0", "21 0 0 0 0 0 0", 5759)
Z(50, "Tripolitains et Tiaches", "3284 0 0 0 0 0 0", grand=3284, note="(4)")
Z(50, "Gens d’Ouerghemma et de Matmata", "3034 0 0 0 0 0 0", grand=3034,
  name="Gens d'Ouerghemma et de Matmata", note="(4)")
Z(50, "Gens Gabès et de nefzaoiia !", "5199 0 0 0 0 0 0", grand=5199,
  name="Gens de Gabès et de Nefzaoua", note="(4)")
Z(50, "Djerbiens", "1923 0 0 0 0 0 0", grand=1923, note="(4)")
Z(50, "Totaux", "85391 1270 71 0 9 2001 4", "4068 0 1 0 0 0 0", 92815)
C(50, "(4) releyant Ces groupements administrativement qui", "DROP")

# Tunis-Ville lists again the four Tunis-Banlieue groups of footnote (4) (p. 90-91);
# its footnote (1) says they live in Tunis-Ville but belong to the Tunis-Banlieue caidat.
C(52, "Cheikhats des Tripolitains et Tiaches \\", name="Cheikhats des Tripolitains et Tiaches", note="(1)", duplicate=True)
C(52, "Cheikhat des Djerbiens I", name="Cheikhat des Djerbiens", note="(1)", duplicate=True)
C(52, "IVefzaoua t", name="Cheikhats des Gens de Gabès et de Nefzaoua", note="(1)", duplicate=True)
C(52, "Matmata .... /", name="Cheikhats des Gens d'Ouerghemma et de Matmata", note="(1)", duplicate=True)


def apply_corrections(recs):
    out = []
    used = set()
    seen = {}
    for r in recs:
        k2 = (r["view"], label_key(r["label"]))
        n = seen.get(k2, 0)
        seen[k2] = n + 1
        key = k2 + (n,)
        e = CORRECTIONS.get(key)
        if e is None:
            out.append(r)
            continue
        used.add(key)
        if e == "DROP":
            continue
        if "values" in e:
            for i, (a, b) in enumerate(zip(r["values"], e["values"])):
                if a != b:
                    r["flags"][i] = "ocr_corrected"
            r["values"] = list(e["values"])
        if e.get("mismatch"):
            r["printed_mismatch"] = e["mismatch"]
        if "label" in e:
            r["name"] = e["label"]
        if "note" in e:
            r["note"] = e["note"]
        if e.get("duplicate"):
            r["duplicate"] = True
        r["checked"] = True
        out.append(r)
    missing = set(CORRECTIONS) - used
    assert not missing, f"corrections not applied: {sorted(missing)}"
    return out


def fix_nines(r):
    """OCR often reads the dash '»' as '9' (sometimes '8'). If setting such cells to 0 makes every
    row check pass (and no other change is needed), do it and flag the cells."""
    v = r["values"]
    if None in v or not check(v):
        return
    nines = [i for i, c in enumerate(r["cells"]) if c and all(t in ("9", "9.", "9»", "»9", "99", "8", "8»", "»8") for t in c)
             and i not in (7, 15, 16)]
    from itertools import combinations
    for k in range(1, len(nines) + 1):
        for comb in combinations(nines, k):
            w = [0 if i in comb else x for i, x in enumerate(v)]
            if not check(w):
                r["values"] = w
                for i in comb:
                    r["flags"][i] = "ocr_corrected"
                return


def fill_single(r):
    """A single cell the OCR missed is determined by the row's printed totals:
    fill it when the result is non-negative and every row check then passes."""
    v = r["values"]
    miss = [i for i, x in enumerate(v) if x is None]
    if len(miss) != 1 or r["view"] in NO_RIGHT_OCR:
        return
    i = miss[0]
    w = list(v)
    if i < 7:
        w[i] = w[7] - sum(x for k, x in enumerate(w[:7]) if k != i)
    elif i == 7:
        w[i] = sum(w[:7])
    elif i < 15:
        w[i] = w[15] - sum(x for k, x in enumerate(w[8:15], 8) if k != i)
    elif i == 15:
        w[i] = sum(w[8:15])
    else:
        w[i] = w[7] + w[15]
    if w[i] >= 0 and not check(w):
        r["values"] = w
        r["flags"][i] = "ocr_corrected"


def block_checks(recs):
    """Running sums within each caidat against 'A reporter', 'Report' and 'Totaux'."""
    out = []
    run = None
    prev_kind = None
    for r in recs:
        v = r["values"]
        if r["kind"] == "carry_in":
            # a "Report" printed at the foot of a page (view 27) closes a page
            if run is not None and prev_kind == "cheikhat":
                out.append((r, [None if a is None or b is None else b - a for a, b in zip(run, v)]))
            run = list(v) if None not in v else None
            prev_kind = r["kind"]
            continue
        prev_kind = r["kind"]
        if r["kind"] == "cheikhat":
            if run is None:
                run = [0] * NCOL
            run = [a + b if a is not None and b is not None else None for a, b in zip(run, v)]
            continue
        # carry_out or total
        if run is not None:
            diff = [None if a is None or b is None else b - a for a, b in zip(run, v)]
            out.append((r, diff))
        if r["kind"] == "total":
            run = None
    return out


def clean_name(label):
    """Cheikhat name from an OCR label: strip leading OCR debris (bracket
    fragments), trailing dot leaders and footnote markers. Returns (name, note)."""
    t = label.replace("’", "'").replace("—", "-")
    note = ""
    m = re.search(r"\(\s*(\d)\s*\)|\b[P(](\d)?\)|\((\d)\b", t)
    if m:
        d = next(g for g in m.groups() if g) if any(m.groups()) else "1"
        note = f"({d})"
        t = t[:m.start()] + t[m.end():]
    toks = t.split()
    # drop leading debris: tokens until the first word starting with a capital
    while toks and not re.match(r"[A-ZÉÈÂÎÔ][\w'-]", toks[0]):
        toks.pop(0)
    t = " ".join(toks)
    t = re.sub(r"[\s.:;,'\-_|\\/)(\]\[{}*•!]+$", "", t)
    t = re.sub(r"\s+[A-Za-z]$", "", t)        # stray single letter (bracket)
    t = re.sub(r"\s{2,}", " ", t).strip()
    t = t.replace("Oule'd", "Ouled").replace("OuIad", "Oulad").replace("lloumet", "Houmet")
    return t, note


# Names and bracket labels checked against the page images, keyed by
# (view, cleaned OCR name, occurrence): (printed name or None, cheikhat_note or None)
NAMEFIX = {}


def NF(view, cleaned, name=None, note=None, nth=0):
    key = (view, cleaned, nth)
    assert key not in NAMEFIX, key
    NAMEFIX[key] = (name, note)


def G(view, names, note):
    """Bracket group: give `note` to the listed (cleaned) names of a view."""
    seen = {}
    for n in names:
        k = seen.get(n, 0)
        seen[n] = k + 1
        old = NAMEFIX.get((view, n, k), (None, None))
        NAMEFIX[(view, n, k)] = (old[0], note if old[1] is None else old[1])


NF(11, "Oulad-Amor et Zouaoua t 1", "Oulad-Amor et Zouaoua", "(1)")
NF(12, "Chenini-Nord.", "Chenini-Nord", "(1)")
NF(12, "Clienini-Sud", "Chenini-Sud", "(1)")
NF(12, "Djara-Onest", "Djara-Ouest")
NF(12, "Ménzel-Onest", "Menzel-Ouest")
NF(12, "Meïizel-Ouest", "Menzel-Ouest")
G(12, ["Debdaba", "Ksar El-Hamma", "Israélites d'El-Hamma"], "El-Hamma commune (2)")
G(12, ["Djara-Est", "Djara-Onest", "Menzel-Est", "Ménzel-Onest", "Israélites de Gabès"], "Gabès commune (3)")
NAMEFIX[(12, "Djara-Est", 1)] = (None, "Gabès banlieue (4)")
NAMEFIX[(12, "Djara-Ouest", 0)] = (None, "Gabès banlieue (4)")
NAMEFIX[(12, "Menzel-Est", 1)] = (None, "Gabès banlieue (4)")
NAMEFIX[(12, "Meïizel-Ouest", 0)] = ("Menzel-Ouest", "Gabès banlieue (4)")
NF(13, "OX El-Médina", "El-Médina", "Béja-Ville (1)")
NF(13, "Béja-Ville ] ( Er-Rabtme", "Er-Rabtine", "Béja-Ville (1)")
NF(13, "El-Médina (partie rurale", "El-Médina (partie rurale)", "(2)")
NF(13, "Er-Rabtine", "Er-Rabtine (partie rurale)", "(2)")

# view 15: the two wrapped names were attached to the wrong OCR lines
NF(15, "Houme't El-Andlous", "Bizerte-Banlieue (non compris Houmet El-Andlous)")
NF(15, "Bizerte-Banlieue", "Houmet-el-Andlous (partie communale de Bizerte-Banlieue)", "Bizerte-Ville (1)")
G(15, ["Bizerte-Est", "Bizerte-Ouest", "Cheikhat des Israélites"], "Bizerte-Ville (1)")
NF(16, "Bou-Semir", "Oulad-el-Massekh et Oulad-Bou-Semir")
NF(17, "Chouamekh-et-D j ehinat", "Chouamekh-et-Djehinat")
NF(17, "El-Ghouiba-Essouda 0", "El-Ghouiba-Essouda", "(1)")
NF(17, "Khit-el-Oue'd", "Khit-el-Oued", "(2)")
NF(18, "Toual et Fedhoul ‘", "Toual et Fedhoul")
G(18, ["Hara-Kebira", "Hara-Sghira"], "Commune de Djerba (1)")
NF(18, "Houmet-Es-Souk", None, "Commune de Djerba (1); (2)")

NF(19, "Ouled-Amor (Degache", "Ouled-Amor (Degache)", "(1)")
NF(19, "Messatra (Degache", "Messatra (Degache)", "(1)")
NF(19, "Béni-Ali", "Beni-Ali")
G(19, ["Béni-Ali", "Beni-Yazid", "En-Nouasra", "Mouâda", "Ouled Aïssa et Brahmia", "Zaïbine", "Zebda"],
  "Commune de Nefta (2)")
G(19, ["Chabbia", "Guitna", "Hebaïla", "Messghouna", "Ouled-el-Hadef"], "Commune de Tozeur (3)")
NAMEFIX[(19, "Zebda", 1)] = (None, "Commune de Tozeur (3)")
NF(20, "He'rakta", "Herakta")
NF(20, "Thala (Banlieue)", None, "(1)")
NF(20, "Thala (Ville", "Thala (Ville)", "(1)")
NF(20, "El-Avaïcha", "El-Ayaïcha")
NF(20, "El-Guettar Nord", None, "(2)")
NF(20, "El-Guettar Sud", None, "(2)")
NF(21, "Ouled Chérit", "Ouled Cherit")
NF(22, "El-Harcliane", "El-Harchane")
NF(22, "Ouled Am or", "Ouled Amor")
NF(22, "Ouled Bel-IIadi", "Ouled Bel-Hadi")

NF(23, "Ouled Ivhalifa", "Ouled Khalifa")
NF(23, "Ouled M'barek (Maknassy", "Ouled M'barek (Maknassy)")
NF(23, "Ouled Youssef 1", "Ouled Youssef")
NF(24, "EI-Khadhera", "El-Khadhera")
NF(26, "Ebba-Ksour (Banlieue", "Ebba-Ksour (Banlieue)", "(1)")
NF(26, "Ebba-Ksour (Ville", "Ebba-Ksour (Ville)", "(1)")
NF(26, "Kef-Ville f ^harfiue (partieconnu nale", "Charfine (partie communale)", "Kef-Ville (3)")
NF(26, "Ben-Anine", None, "Kef-Ville (3)")
NF(26, "Ben-Anine (partie rurale) ^", "Ben-Anine (partie rurale)", "(4)")
NF(26, "Gharflne", "Charfine (partie rurale)", "(4)")

NF(27, "Sidi-Am'or", "Sidi-Amor")
NF(28, "Quled Moussa", "Ouled Moussa")
NF(28, "Aiaïcha (Téboulba", "Aïaïcha (Téboulba)", "(2)")
NF(28, "Houiiiet-es-Souk (léboulba", "Houmet-es-Souk (Téboulba)", "(2)")
NF(28, "Mahdia (Banlieue", "Mahdia (Banlieue)", "(3)")
NF(28, "Mahdia (Ville", "Mahdia (Ville)", "(3)")
NF(28, "Merabtine (El-Djem", "Merabtine (El-Djem)", "(4)")
NF(28, "Zaouia (El-Djem) ? )", "Zaouia (El-Djem)", "(4)")
NF(29, "Sidi-Messaoud (Ksour-Essaf", "Sidi-Messaoud (Ksour-Essaf)", "(1)")
NF(29, "Zeraraà (Ksour-Essaf) ) / ( 1J", "Zeraraâ (Ksour-Essaf)", "(1)")
NF(29, "Berrais", "Berraïs")
NF(30, "Mateur (Banlieue", "Mateur (Banlieue)", "(1)")
NF(30, "Mateur (Ville", "Mateur (Ville)", "(1)")
NF(30, "Téliente", "Téhente")
NF(30, "Acliaclies", "Achaches", "(2)")

NF(31, "Medjez-el-Rab (Banlieue) ‘", "Medjez-el-Bab (Banlieue)", "(1)")
NF(31, "Bab (Ville", "Medjez-el-Bab (Ville)", "(1)")
NF(32, "Beni-Iiassen", "Beni-Hassen")
NF(32, "Djernia de Cherahil", "Djemia de Cherahil")
NF(32, "Djemmal-Nord", None, "(1)")
NF(32, "Djemmal-Sud", None, "(1)")
NF(32, "Djenaïha Gheraïba (Amira", "Djenaïha et Gheraïba (Amira)", "(2)")
NF(32, "El-Hadjaj (Amira", "El-Hadjaj (Amira)", "(2)")
NF(32, "El-Fehoul (Amira", "El-Fehoul (Amira)", "(2)")
NF(32, "Touazra (Amira", "Touazra (Amira)", "(2)")
NF(32, "Ksar-Helal-Nord", None, "(3)")
NF(32, "Ksar-Helal-Sud", None, "(3)")
NF(33, "Masdour et Menzel-Hàrb", "Masdour et Menzel-Hârb")
NF(33, "Mesjed-A'ïssa", "Mesjed-Aïssa")
NF(33, "Quartier Est", None, "Moknine (1)")
NF(33, "Quartier Ouest", None, "Moknine (1)")
NF(33, "Israélites", None, "Moknine (1)")
NF(33, "Monastirt (El-Medina", "El-Medina", "Monastir (2)")
NF(33, "", "Er-Rebat", "Monastir (2)")
NF(33, "Beldia", None, "Touza (3)")
NF(33, "Oussaltia", None, "Touza (3)")
NF(33, "Zarmedine (Mrabtine", "Mrabtine", "Zarmedine (4)")
NF(33, "", "Beldia", "Zarmedine (4)", nth=1)
NF(34, "Keiibia", "Kelibia")
NF(34, "Nabeul (Banlieue)", None, "(1)")
NF(34, "Nabeul (Ville", "Nabeul (Ville)", "(1)")

NF(35, "Douz-Chargui", None, "(1)")
NF(35, "Douz-El-Gharbi", None, "(1)")
NF(35, "Ké'bili", "Kébili", "(2)")
BG = "Cercle de Ben-Gardane - Khalifalik des Touazines (1)"
NF(36, "Touazincs Jelalta", "Jelalta")
NF(36, "", "Oulad-Khelifa-Chougman")
NF(36, "Ben-Gardane Oulad-Khelifa-Djera", "Oulad-Khelifa-Djera")
G(36, ["El-Kraïna", "El-Melalha", "Touazincs Jelalta", "Maztoura", "Nebahna",
       "Oulad-Aounallah et Barrania de Ben-Gardane", "", "Ben-Gardane Oulad-Khelifa-Djera",
       "Oulad-Hamed", "Rebaya et Aouine", "Zliten"], BG)
MD = "Cercle de Médenine - Khalifalik des Khzours (2)"
NF(36, "Chàoua-El-Oula", "Châoua-El-Oula", MD)
NF(36, "Médenine Khzours 1 El-Mehabbel", "El-Mehabbel")
NF(36, "Cercle Khalifalik Jebbah", "Jebbah")
G(36, ["Barrania de Médenine", "Châoua-Et-Tania", "Médenine Khzours 1 El-Mehabbel", "El-Mehadha",
       "El-Mekazra", "Cercle Khalifalik Jebbah", "Jouamaâ", "Ghebenten"], MD)
G(37, ["Lemalma", "Médenine", "Oulad-Belgacem", "Oulad-Mahdi", "Temmara", "Zemamra"],
  "Cercle de Médenine - Khalifalik des Ksours (suite)")
ZR = "Cercle de Zarzis - Khalifalik des Accara (1)"
NF(37, "", "El-Khelaïfa (partie rurale)", ZR)
NF(37, "Accara rale", "El-Mouansa (partie rurale)", ZR)
NF(37, "Ez-Zaouia (partie rurale", "Ez-Zaouia (partie rurale)", ZR)
NF(37, "", "Oulad-Bou-Ali (partie rurale)", ZR, nth=1)
NF(37, "Khalifalik rurale", "Oulad-M'hamed (partie rurale)", ZR)
NF(37, "", "Oulad-Saïd (partie rurale)", ZR, nth=2)
G(37, ["El-Khelaïfa", "El-Mouansa", "Ez-Zaouia", "Ouled-Bou-Ali", "Ouled-M'hamed", "Ouled-Saïd"],
  ZR + "; Commune de Zarzis (2)")
NF(38, "Alaouna", None, "(1)")
NF(38, "EI-Bahirine", "El-Bahirine")

NF(39, "Ouled-Salali", "Ouled-Salah")
NF(39, "Saàdna", "Saâdna")
NF(40, "El-AttaJia", "El-Attaïa")
NF(40, "Er-Bemla", "Er-Remla")
G(40, ["Chergui", "El-AttaJia", "Er-Bemla", "Kheraïb"], "Iles de Kerkenah (1)")
G(41, ["Kellabine", "Mellita", "Oulad-Gacem", "Oulad-Yanègue"], "Iles de Kerkenah (1) (suite)")
G(41, ["Sfax-Est", "Sfax-Ouest", "Barrania", "Merkez-Ben-Halima (partie communale)", "Merkez-Demak",
       "Merkez-Kammoun (partie communale)", "Sakiet-Ez-Zit (partie communale)", "Israélites"],
  "Commune de Sfax (2)")
NF(41, "Bell", "Belli")
NF(42, "Sidi-Naceur", None, "(1)")

NF(43, "Cliouichia", "Chouichia")
NF(43, "Draâ-En-Nefikli", "Draâ-En-Nefikh")
NF(43, "El-Maleli", "El-Maleh")
NF(43, "Souk-El-Arba (Banlieue", "Souk-El-Arba (Banlieue)", "(2)")
NF(43, "Souk-El-Arba (Ville", "Souk-El-Arba (Ville)", "(2)")
NF(44, "EI-Djemamza", "El-Djemamza")
NF(44, "Souk-el-Khemis (Banlieue", "Souk-el-Khemis (Banlieue)", "(1)")
NF(44, "Souk-el-Khemis (Ville", "Souk-el-Khemis (Ville)", "(1)")
NF(45, "Dar-El-Bey (Enfidaville", "Dar-El-Bey (Enfidaville)")
NF(45, "Djerabâa (Kalaâ-Kebira)", None, "(1)")
NF(45, "Ez-Zeàrna", "Ez-Zeârna (Kalaâ-Kebira)", "(1)")
NF(45, "El-Djebline (M'Saken", "El-Djebline (M'Saken)", "(2)")
NF(45, "El-Djedidine (M'Saken", "El-Djedidine (M'Saken)", "(2)")
NF(45, "El-Kebline (M'Saken", "El-Kebline (M'Saken)", "(2)")
NF(45, "El-M'Naâma (M'Saken", "El-M'Naâma (M'Saken)", "(2)")
NF(45, "En-Nejajera (M'Saken)y", "En-Nejajera (M'Saken)", "(2)")
NF(45, "El-Menzel (Dar-Bel-Ouar", "El-Menzel (Dar-Bel-Ouar)")
NF(46, "Moétamer", "Moâtamer")
NF(46, "Ourima-T rabelsia", "Ourima-Trabelsia")
NF(46, "Sousse (Banlieue", "Sousse (Banlieue)", "(1)")

NF(49, "Krib", "El-Kelekh (y compris commune du Krib)")
NF(49, "Gaifour-Ouest", "Gaffour-Ouest")
NF(49, "Téboursouk (Banlieue", "Téboursouk (Banlieue)", "(1)")
NF(49, "Téboursouk (Ville", "Téboursouk (Ville)", "(1)")
NF(51, "Batbat-Essolli", "Bathat-Essolli")
NF(53, "Zaghouan (Banlieue", "Zaghouan (Banlieue)", "(1)")


def final_names(recs):
    """Printed name and note for each cheikhat row: cleaned OCR label, then the
    image-checked fixes (corrections first, NAMEFIX last)."""
    seen = {}
    for r in recs:
        if r["kind"] != "cheikhat":
            continue
        cleaned, note = clean_name(r["label"])
        if r.get("name") and not any(k[0] == r["view"] and k[1] == cleaned for k in NAMEFIX):
            cleaned = r["name"]
        k = (r["view"], cleaned)
        n = seen.get(k, 0)
        seen[k] = n + 1
        name = r.get("name") or cleaned
        note = r.get("note") or note
        fx = NAMEFIX.get((r["view"], cleaned, n))
        if fx:
            name = fx[0] or name
            note = fx[1] or note
            fx_used.add((r["view"], cleaned, n))
        r["cheikhat"], r["cheikhat_note"] = name, note
    unused = set(NAMEFIX) - fx_used
    assert not unused, sorted(unused)


fx_used = set()


REF_CAIDAT = {"Kef": "Le Kef", "Madjeurs": "Madjeur", "La Skhira": "Skhira", "Tatahouine": "Tataouine",
              "Tunis-Banlieue": "Tunis Banlieue", "Tunis-Ville": "Tunis Ville"}


def load_reference():
    """Ben Salah et al. (2024) cheikhat-level 1931 counts (data/colonial_tunisian_pop.rda).

    Used only to cross-check the extraction; the page images decide.
    """
    try:
        import pyreadr
    except ImportError:
        raise SystemExit("The cross-check against Ben Salah et al. (2024) reads "
                         "data/colonial_tunisian_pop.rda: pip install pyreadr")
    df = list(pyreadr.read_r(str(HERE.parent.parent / "data" / "colonial_tunisian_pop.rda")).values())[0]
    df = df[df.tunisian_muslims_1931.notna() | df.tunisian_jews_1931.notna()]
    out = {}
    for _, r in df.iterrows():
        g = lambda c: 0 if r[c] != r[c] or r[c] is None else int(r[c])  # noqa: E731
        out.setdefault(r.caidat_1931, []).append({
            "name": r.locality_1926, "tm": g("tunisian_muslims_1931"), "tj": g("tunisian_jews_1931"),
            "om": g("other_muslims_1931"), "oj": g("other_jews_1931")})
    return out


def ref_signature(vals):
    if any(v is None for v in vals):
        return None
    return (vals[0], vals[8], sum(vals[1:7]), sum(vals[9:15]))


def compare_reference(recs):
    """Match each cheikhat row to a reference row (same caidat, best name, then values)."""
    ref = load_reference()
    res = {}
    for c in CAIDATS:
        rows_c = [r for r in recs if r["caidat"] == c and r["kind"] == "cheikhat"]
        pool = list(ref.get(REF_CAIDAT.get(c, c), []))
        for r in rows_c:
            if not pool:
                res[id(r)] = (None, "no_ref")
                continue
            name = re.sub(r"\(.*?\)|[^\w' -]", " ", r["label"])
            sig = ref_signature(r["values"])

            def score(x):
                ns = difflib.SequenceMatcher(None, squash(name), squash(x["name"])).ratio()
                vs = 0
                if sig:
                    vs = sum(a == b for a, b in zip(sig, (x["tm"], x["tj"], x["om"], x["oj"]))) / 4
                elif r["values"][0] is not None:
                    vs = 0.5 * (r["values"][0] == x["tm"])
                return ns + vs
            best = max(pool, key=score)
            pool.remove(best)
            ok = sig == (best["tm"], best["tj"], best["om"], best["oj"]) if sig else (
                r["values"][0] == best["tm"])
            res[id(r)] = (best, "match" if ok else "differs")
        for x in pool:
            res.setdefault(("unused", c), []).append(x)
    return res


# ---------------------------------------------------------------------------
# Output

# Table I (printed page 6-7), totals by contrôle civil: Muslim total, Jewish
# total, grand total, read from the image. Used to validate Table III.
TABLE_I = {
    "Béja": (71213, 989, 72202), "Bizerte": (129650, 1771, 131421), "Djerba": (43841, 4128, 47969),
    "Gabès": (63199, 2954, 66153), "Gafsa": (117439, 816, 118255), "Grombalia": (126935, 2119, 129054),
    "Kairouan": (161960, 376, 162336), "Le Kef": (129666, 1087, 130753), "Maktar": (65105, 107, 65212),
    "Medjez-el-Bab": (50581, 141, 50722), "Sfax": (203321, 3187, 206508),
    "Souk-el-Arba": (89040, 333, 89373), "Sousse": (300520, 5053, 305573), "Tabarka": (37930, 31, 37961),
    "Thala": (107546, 273, 107819), "Téboursouk": (38977, 72, 39049), "Tozeur": (43887, 347, 44234),
    "Tunis": (165107, 29468, 194575), "Zaghouan": (43703, 7, 43710),
    "Territoires militaires": (169531, 2989, 172520),
}
TABLE_I_NATIONAL = [2086762, 40734, 2854, 445, 140, 28157, 59, 2159151,
                    55340, 185, 34, 0, 28, 556, 105, 56248, 2215399]
MILITARY = ("Territoire", "Cercle")
RELIGION = [("muslim", "Population musulmane"), ("jewish", "Population israélite")]
OUT = HERE / "csv" / "ind1931_t3_cheikhat_nationality.csv"
COLUMNS = ["census", "table_id", "source_page", "gallica_view", "controle_civil", "caidat", "cheikhat",
           "cheikhat_note", "duplicate", "religion", "religion_fr", "nationality", "nationality_fr",
           "value", "flag"]


def validate(recs):
    """Run every check; return a dict of counts (all failures must be explained)."""
    st = {"rows": len(recs), "row_checks": 0, "row_checks_passed": 0, "row_failures": []}
    for r in recs:
        st["row_checks"] += 3
        bad = check(r["values"])
        st["row_checks_passed"] += 3 - len(bad)
        if bad:
            st["row_failures"].append((r["view"], r["caidat"], r["kind"], r["label"], bad))
    blocks = block_checks(recs)
    st["block_checks"] = len(blocks) * NCOL
    st["block_failures"] = [(r["view"], r["caidat"], r["kind"], [(i, d) for i, d in enumerate(diff) if d])
                            for r, diff in blocks if any(diff)]
    st["block_checks_passed"] = st["block_checks"] - sum(len(f[3]) for f in st["block_failures"])
    ch = [r for r in recs if r["kind"] == "cheikhat"]
    by = {}
    for r in ch:
        if r.get("duplicate"):
            continue
        k = "Territoires militaires" if r["controle"].startswith(MILITARY) else r["controle"]
        by[k] = [a + b for a, b in zip(by.get(k, [0] * NCOL), r["values"])]
    st["table_i"] = {k: ((v[7], v[15], v[16]), TABLE_I[k]) for k, v in by.items()}
    nodup = [r for r in ch if not r.get("duplicate")]
    st["national"] = [sum(r["values"][k] for r in nodup) for k in range(NCOL)]
    st["national_ok"] = st["national"][:7] + st["national"][7:] == [
        x for x in TABLE_I_NATIONAL]
    cmp = compare_reference(recs)
    st["ref_match"] = sum(1 for r in ch if cmp[id(r)][1] == "match")
    st["ref_total"] = len(ch)
    st["cells_corrected"] = sum(len(r["flags"]) for r in ch)
    st["cheikhats"] = len(ch)
    st["checked_rows"] = sum(1 for r in recs if r.get("checked"))
    return st


def build():
    recs = structure()
    final_names(recs)
    st = validate(recs)
    rows = []
    for r in recs:
        if r["kind"] != "cheikhat":
            continue
        lp, rp = page_number(r["view"])
        for ri, (rel, rel_fr) in enumerate(RELIGION):
            for ni, (nat, nat_fr) in enumerate(zip(NAT, NAT_FR)):
                i = ri * 8 + ni
                rows.append({
                    "census": "ind1931", "table_id": "III",
                    "source_page": lp if ri == 0 else rp, "gallica_view": r["view"],
                    "controle_civil": r["controle"], "caidat": r["caidat"], "cheikhat": r["cheikhat"],
                    "cheikhat_note": r["cheikhat_note"] or "", "duplicate": int(bool(r.get("duplicate"))),
                    "religion": rel, "religion_fr": rel_fr, "nationality": nat,
                    "nationality_fr": NAT_FR[ni] if not (ri == 1 and ni == 6) else "Autres nationalités",
                    "value": r["values"][i], "flag": r["flags"].get(i, ""),
                })
    OUT.parent.mkdir(exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    return recs, rows, st


if __name__ == "__main__" and "--structure" in sys.argv:
    recs = structure()
    cmp = compare_reference(recs)
    for r in recs:
        bad = check(r["values"])
        if r["kind"] == "cheikhat":
            b, st = cmp[id(r)]
            if st != "match":
                bad = bad + [f"REF:{st}:" + (f"{b['name']} {b['tm']} {b['tj']} {b['om']} {b['oj']}" if b else "")]
        print(r["view"], f"{r['pos']:.0f}", r["caidat"], "|", r["controle"], "|", r["kind"], "|", r["label"][:50], "|",
              " ".join("?" if x is None else str(x) for x in r["values"]), "BAD:" + ",".join(bad) if bad else "")
    for k, v in cmp.items():
        if isinstance(k, tuple):
            print("UNUSED_REF", k[1], [(x["name"], x["tm"]) for x in v])
    print("== block checks")
    for r, d in block_checks(recs):
        if any(x not in (0, None) for x in d):
            print("BLOCK", r["view"], r["caidat"], r["kind"], r["label"][:30], d)
    sys.exit()
if __name__ == "__main__" and "--dump" in sys.argv:
    for v in VIEWS:
        ev, ls, rs = parse_spread(v)
        print(f"## view {v} shifts L{ls} R{rs}")
        for e in ev:
            if e[1] == "row":
                bad = check(e[3])
                print(v, f"{e[0]:.0f}", "ROW" if not bad else "BAD " + ",".join(bad), e[2], "|",
                      " ".join("?" if x is None else str(x) for x in e[3]), ("  STRAY " + " ".join(w["text"] for w in e[6])) if e[6] else "")
            else:
                print(v, f"{e[0]:.0f}", "TXT", e[4], e[2][:140])


if __name__ == "__main__" and len(sys.argv) == 1:
    recs, rows, st = build()
    import json
    print(json.dumps({k: v for k, v in st.items() if k not in ("table_i",)}, ensure_ascii=False, indent=1, default=str))
    for k, (got, want) in sorted(st["table_i"].items()):
        print("TABLE_I", k, got, want, "OK" if got == want else "DIFF")
    print(len(rows), "rows written to", OUT)
