#!/usr/bin/env python3
"""Download Tunisian census documents from Gallica via the BnF IIIF gateway.

gallica.bnf.fr sits behind Cloudflare and rejects scripted clients, but the
BnF's official IIIF gateway (openapi.bnf.fr) serves the same documents. It has
no PDF endpoint, so this script reads each document's IIIF Presentation v3
manifest, fetches every page through the IIIF Image API, and wraps the pages
into one PDF per document (img2pdf).

Resolution: the gateway caps a whole-page request ("full/max") at half the
scan's native size, but serves a region at native size when the request names
an explicit output width. With --resolution full (the default) each page is
fetched as native-resolution tiles and stitched, then re-encoded once as JPEG
(quality 92). With --resolution half each page is a single "full/max" request,
kept byte for byte, which is four times smaller and much faster.

Sources are listed in data-raw/bnf_gallica_sources.csv. Downloads are cached
page by page (pages_full/ or pages/), so an interrupted run resumes where it
stopped.

Usage:
    pip install img2pdf pillow
    python3 data-raw/bnf_gallica_download.py [--resolution full|half] [--out DIR] [--only ARK ...]

Rights: the scans are public domain but not CC BY. BnF-held documents are
NoC-NC (non-commercial reuse) and partner-held documents are NoC-CR (holding
library's terms). Each PDF's metadata records the credit line
"Source gallica.bnf.fr / <holding institution>", read from the manifest. See
https://gallica.bnf.fr/edit/und/conditions-dutilisation-des-contenus-de-gallica
"""
import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import img2pdf
from PIL import Image

HERE = Path(__file__).resolve().parent
MANIFEST = "https://openapi.bnf.fr/iiif/presentation/v3/ark:/12148/{ark}/manifest.json"
UA = "tncensus-data-raw/1.0 (research; IIIF client)"


def get(url, tries=6, timeout=120):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if isinstance(e, urllib.error.HTTPError) and e.code == 404:
                raise
            wait = 2 ** i
            print(f"  retry {i + 1}/{tries} in {wait}s: {url} ({e})", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError(f"failed after {tries} tries: {url}")


def page_services(manifest):
    """IIIF Image API service URL for every canvas, in reading order."""
    return [canvas["items"][0]["items"][0]["body"]["service"][0]["id"]
            for canvas in manifest["items"]]


TILE = 900  # below the gateway's 1500-pixel cap on output width


def fetch_full(service):
    """Native-resolution page as JPEG bytes, stitched from region requests."""
    import io
    info = json.loads(get(f"{service}/info.json"))
    w, h = info["width"], info["height"]
    img = Image.new("RGB", (w, h), "white")
    for y in range(0, h, TILE):
        th = min(TILE, h - y)
        for x in range(0, w, TILE):
            tw = min(TILE, w - x)
            tile = Image.open(io.BytesIO(get(f"{service}/{x},{y},{tw},{th}/{tw},/0/default.jpg")))
            if tile.size != (tw, th):
                raise RuntimeError(f"{service}: tile {x},{y} is {tile.size}, expected {(tw, th)}")
            img.paste(tile.convert("RGB"), (x, y))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=92, dpi=(300, 300))
    return buf.getvalue()


def holder(manifest):
    """Holding institution ("Dépôt" in the manifest metadata), e.g. a partner library."""
    for item in manifest.get("metadata", []):
        if item["label"].get("fr", [""])[0] == "Dépôt":
            return next(iter(item["value"].values()))[0]
    return "Bibliothèque nationale de France"


def fetch_page(job):
    service, path, resolution = job
    if path.exists() and path.stat().st_size > 0:
        return
    if resolution == "full":
        data = fetch_full(service)
    else:
        data = get(f"{service}/full/max/0/default.jpg")
    if not data.startswith(b"\xff\xd8"):
        raise RuntimeError(f"not a JPEG: {service}")
    tmp = path.with_suffix(".part")
    tmp.write_bytes(data)
    tmp.replace(path)


def download(row, out, workers, resolution):
    ark = row["ark"]
    pdf = out / ("pdf" if resolution == "full" else "pdf_half") / row["filename"]
    if pdf.exists():
        print(f"[skip] {pdf.name} already built")
        return
    cache = out / ("pages_full" if resolution == "full" else "pages") / ark
    cache.mkdir(parents=True, exist_ok=True)
    mpath = cache / "manifest.json"
    if not mpath.exists():
        mpath.write_bytes(get(MANIFEST.format(ark=ark)))
    manifest = json.loads(mpath.read_text())
    credit = "Source gallica.bnf.fr / " + holder(manifest)
    services = page_services(manifest)
    jobs = [(u, cache / f"f{i:04d}.jpg", resolution) for i, u in enumerate(services, 1)]
    print(f"[get ] {ark} {row['title'][:70]} — {len(jobs)} pages, {resolution} resolution", flush=True)
    done = 0
    with ThreadPoolExecutor(workers) as ex:
        for _ in ex.map(fetch_page, jobs):
            done += 1
            if done % 50 == 0:
                print(f"  {ark}: {done}/{len(jobs)}", flush=True)
    pdf.parent.mkdir(parents=True, exist_ok=True)
    tmp = pdf.with_suffix(".part")
    with open(tmp, "wb") as f:
        img2pdf.convert(
            [str(p) for _, p, _ in jobs],
            outputstream=f,
            title=row["title"],
            author=credit,
            subject=f"{credit} — https://gallica.bnf.fr/ark:/12148/{ark} — {row['holding']} — rights: {manifest.get('rights', '')}",
            keywords=["Tunisie", "recensement", "dénombrement", ark],
        )
    tmp.replace(pdf)
    print(f"[done] {pdf} ({pdf.stat().st_size / 1e6:.1f} MB)", flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--sources", default=HERE / "bnf_gallica_sources.csv", type=Path)
    ap.add_argument("--out", default=HERE / "bnf_gallica", type=Path)
    ap.add_argument("--only", nargs="*", help="restrict to these arks")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--resolution", choices=["full", "half"], default="full",
                    help="full: native scan resolution (default); half: the gateway's whole-page cap")
    a = ap.parse_args()
    rows = list(csv.DictReader(open(a.sources, encoding="utf-8")))
    if a.only:
        rows = [r for r in rows if r["ark"] in a.only]
    for r in rows:
        download(r, a.out, a.workers, a.resolution)


if __name__ == "__main__":
    main()
