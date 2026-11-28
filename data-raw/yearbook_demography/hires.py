"""Full-resolution page images from the BnF IIIF gateway.

A plain `full/max` request is capped at about half the canvas resolution, and
any request is capped at 1500 pixels wide. A region request with an explicit
output width below that cap returns the region at native resolution, so this
fetches a page as a grid of tiles at native resolution and stitches them. Images are cached in data-raw/bnf_gallica/hires/ (gitignored).
"""
import io
import json
import time
import urllib.request
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
CACHE = HERE.parent / "bnf_gallica" / "hires"
BASE = "https://openapi.bnf.fr/iiif/image/v3/ark:/12148/{ark}/f{view}"


def _get(url, tries=6):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return r.read()
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 ** i)


def page(ark, view, tile_w=900, tile_h=900):
    """Path to the full-resolution JPEG of one page view (fetched on first use)."""
    CACHE.mkdir(parents=True, exist_ok=True)
    out = CACHE / f"{ark}_f{view:04d}.png"
    if out.exists():
        return out
    base = BASE.format(ark=ark, view=view)
    info = json.loads(_get(base + "/info.json"))
    w, h = info["width"], info["height"]
    img = Image.new("RGB", (w, h), "white")
    for y in range(0, h, tile_h):
        th = min(tile_h, h - y)
        for x in range(0, w, tile_w):
            tw = min(tile_w, w - x)
            tile = Image.open(io.BytesIO(_get(f"{base}/{x},{y},{tw},{th}/{tw},/0/default.jpg")))
            if tile.size != (tw, th):
                raise RuntimeError(f"tile {x},{y} came back {tile.size}, expected {(tw, th)}")
            img.paste(tile.convert("RGB"), (x, y))
    img.save(out)
    return out


if __name__ == "__main__":
    import sys
    print(page(sys.argv[1], int(sys.argv[2])))
