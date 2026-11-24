"""Gallica OCR helper for the 1906 and 1931 census extractions.

Gallica's word-level OCR for each page view is served by the BnF IIIF gateway as
a IIIF "supplementing" annotation page: one annotation per word, with its text
and an xywh box. In both census volumes the OCR boxes are transposed relative to
the canvas: OCR x runs down the page and OCR y runs across it. This module
returns words as (row_pos, col_pos, text), so callers can group words into
printed rows (similar row_pos) and assign them to columns (col_pos bands).

Responses are cached in data-raw/bnf_gallica/ocr/ (gitignored).
"""
import json
import re
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE.parent / "bnf_gallica" / "ocr"
URL = ("https://openapi.bnf.fr/iiif/presentation/v3/ark:/12148/{ark}/f{view}"
       "/annotationpage/supplementing.json")

ARK_1906 = "bd6t53563851"
ARK_1931 = "bpt6k994559s"


def _get(url, tries=6):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return r.read()
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 ** i)


def words(ark, view):
    """List of dicts {row, col, h, text} for one page view (1-based)."""
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / f"{ark}_f{view:03d}.json"
    if not p.exists():
        p.write_bytes(_get(URL.format(ark=ark, view=view)))
    out = []
    for it in json.loads(p.read_text()).get("items", []):
        x, y, w, h = map(int, re.search(r"xywh=(\d+),(\d+),(\d+),(\d+)", it["target"]).groups())
        # transposed frame: x is vertical, y is horizontal
        out.append({"row": x + w / 2, "col": y + h / 2, "h": w, "text": it["body"]["value"]})
    return out


def rows(ws, tol=18):
    """Group words into printed rows by row position; each row sorted left to right."""
    ws = sorted(ws, key=lambda w: w["row"])
    out = []
    for w in ws:
        if out and abs(w["row"] - out[-1][-1]["row"]) < tol:
            out[-1].append(w)
        else:
            out.append([w])
    return [sorted(r, key=lambda w: w["col"]) for r in out]


def page_text(ark, view, tol=18):
    """Human-readable dump: one printed row per line, words with column positions."""
    return "\n".join(" ".join(f"{w['text']}@{w['col']:.0f}" for w in r) for r in rows(words(ark, view), tol))


NUM = re.compile(r"^[\d.,]+$")


def to_int(tok):
    """Parse a printed count. '»' (and OCR variants like '))', 'D') mean zero.

    Returns None when the token is not a number, so callers can flag it.
    """
    t = tok.strip().rstrip(".").replace(" ", "")
    if t in {"»", "))", ")", "»»", "D", "»."}:
        return 0
    t = t.replace(",", ".").replace("O", "0").replace("o", "0").replace("l", "1").replace("I", "1")
    if not NUM.match(t):
        return None
    return int(t.replace(".", ""))  # thousands are separated by '.'


def page_image(ark, view):
    """Path to the cached full-resolution JPEG of a page view, for visual checks."""
    return HERE.parent / "bnf_gallica" / "pages" / ark / f"f{view:04d}.jpg"


if __name__ == "__main__":
    import sys
    print(page_text(sys.argv[1], int(sys.argv[2])))
