"""Parse a printed numeric table from Gallica's word OCR into a grid.

Used by the 1926 census extraction (extract_cens1926_a.py). OCR word boxes in
these volumes are transposed relative to the canvas: OCR x runs down the page,
OCR y across it, and h is a word's horizontal extent. The cached page images
are half the canvas size, so image (px, py) = (y / 2, x / 2).

grid(ark, view, ncols, row_range, col_range) groups the numeric words in the
table body into printed rows, and assigns each word to one of `ncols` columns
by clustering the words' right edges (numbers are right-aligned). It returns a
list of rows; each row is a list of `ncols` raw strings ('' when the OCR has
nothing there).
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "colonial_census"))
import ocr  # noqa: E402

NUMTOK = re.compile(r"^[\d.,»)(\]\[SsOoIl*]+$")


def raw_words(ark, view):
    ocr.words(ark, view)  # fills the cache
    p = ocr.CACHE / f"{ark}_f{view:03d}.json"
    out = []
    for it in json.loads(p.read_text()).get("items", []):
        x, y, w, h = map(int, re.search(r"xywh=(\d+),(\d+),(\d+),(\d+)", it["target"]).groups())
        out.append({"row": x + w / 2, "left": y, "right": y + h, "text": it["body"]["value"].strip()})
    return out


def is_num(t):
    t = t.strip()
    return bool(t) and (t in {"»", "))", ")", "»»"} or (NUMTOK.match(t) and any(c.isdigit() for c in t)))


def kmeans1d(xs, k, iters=50):
    xs = sorted(xs)
    if len(xs) < k:
        raise ValueError("fewer points than columns")
    cs = [xs[int((i + 0.5) * len(xs) / k)] for i in range(k)]
    for _ in range(iters):
        groups = [[] for _ in cs]
        for x in xs:
            j = min(range(k), key=lambda i: abs(x - cs[i]))
            groups[j].append(x)
        new = [sum(g) / len(g) if g else cs[i] for i, g in enumerate(groups)]
        if new == cs:
            break
        cs = new
    return sorted(cs)


def grid(ark, view, ncols, row_range, col_range, row_tol=16, centers=None):
    ws = [w for w in raw_words(ark, view)
          if row_range[0] <= w["row"] <= row_range[1] and col_range[0] <= w["right"] <= col_range[1]
          and is_num(w["text"])]
    if centers is None:
        centers = kmeans1d([w["right"] for w in ws], ncols)
    rows = []
    for w in sorted(ws, key=lambda w: w["row"]):
        if rows and abs(w["row"] - rows[-1][-1]["row"]) < row_tol:
            rows[-1].append(w)
        else:
            rows.append([w])
    out = []
    for r in rows:
        cells = [""] * ncols
        for w in sorted(r, key=lambda w: w["left"]):
            j = min(range(ncols), key=lambda i: abs(w["right"] - centers[i]))
            cells[j] = (cells[j] + " " + w["text"]).strip()
        out.append({"row": sum(w["row"] for w in r) / len(r), "cells": cells})
    return out, centers


def val(s):
    """Parse an OCR cell to an int; None if not clean."""
    s = s.strip().replace(" ", "")
    if s in {"»", "))", ")", "»»", "»)"}:
        return 0
    s = s.replace(",", ".")
    if re.fullmatch(r"\d{1,7}", s):
        return int(s)
    if not re.fullmatch(r"\d{1,3}(\.\d{3})*", s):
        return None
    return int(s.replace(".", ""))
