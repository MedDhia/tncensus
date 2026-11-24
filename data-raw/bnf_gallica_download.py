#!/usr/bin/env python3
"""Download Tunisian census documents from Gallica via the BnF IIIF gateway.

gallica.bnf.fr sits behind Cloudflare and rejects scripted clients, but the
BnF's official IIIF gateway (openapi.bnf.fr) serves the same documents. It has
no PDF endpoint, so this script reads each document's IIIF Presentation v3
manifest, fetches every page at full resolution as JPEG through the IIIF Image
API, and wraps the JPEGs losslessly into one PDF per document (img2pdf).

Sources are listed in data-raw/bnf_gallica_sources.csv. Downloads are cached
page by page, so an interrupted run resumes where it stopped.

Usage:
    pip install img2pdf
    python3 data-raw/bnf_gallica_download.py [--out DIR] [--only ARK ...]

Rights: Gallica marks these scans http://rightsstatements.org/vocab/NoC-NC/1.0/
(public domain, non-commercial reuse; credit "Bibliothèque nationale de
France / Gallica"). See https://gallica.bnf.fr/edit/und/conditions-dutilisation-des-contenus-de-gallica
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


def page_urls(manifest):
    """Full-resolution JPEG URL for every canvas, in reading order."""
    urls = []
    for canvas in manifest["items"]:
        body = canvas["items"][0]["items"][0]["body"]
        service = body["service"][0]["id"]
        urls.append(f"{service}/full/max/0/default.jpg")
    return urls


def fetch_page(job):
    url, path = job
    if path.exists() and path.stat().st_size > 0:
        return
    data = get(url)
    if not data.startswith(b"\xff\xd8"):
        raise RuntimeError(f"not a JPEG: {url}")
    tmp = path.with_suffix(".part")
    tmp.write_bytes(data)
    tmp.replace(path)


def download(row, out, workers):
    ark = row["ark"]
    pdf = out / "pdf" / row["filename"]
    if pdf.exists():
        print(f"[skip] {pdf.name} already built")
        return
    cache = out / "pages" / ark
    cache.mkdir(parents=True, exist_ok=True)
    mpath = cache / "manifest.json"
    if not mpath.exists():
        mpath.write_bytes(get(MANIFEST.format(ark=ark)))
    manifest = json.loads(mpath.read_text())
    urls = page_urls(manifest)
    jobs = [(u, cache / f"f{i:04d}.jpg") for i, u in enumerate(urls, 1)]
    print(f"[get ] {ark} {row['title'][:70]} — {len(jobs)} pages", flush=True)
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
            [str(p) for _, p in jobs],
            outputstream=f,
            title=row["title"],
            author="Bibliothèque nationale de France / Gallica",
            subject=f"https://gallica.bnf.fr/ark:/12148/{ark} — {row['holding']}",
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
    a = ap.parse_args()
    rows = list(csv.DictReader(open(a.sources, encoding="utf-8")))
    if a.only:
        rows = [r for r in rows if r["ark"] in a.only]
    for r in rows:
        download(r, a.out, a.workers)


if __name__ == "__main__":
    main()
