# Tunisian census scans from Gallica (BnF)

`bnf_gallica_download.py` rebuilds PDFs of the Tunisian census documents
digitized on Gallica, using the BnF's official IIIF gateway (`openapi.bnf.fr`).
`gallica.bnf.fr` itself is behind Cloudflare and refuses scripted access. The
gateway has no PDF endpoint, so the script downloads every page and wraps the
pages into one PDF per document.

```bash
pip install img2pdf pillow
python3 data-raw/bnf_gallica_download.py                      # all 9 documents, full resolution (~5.5 GB)
python3 data-raw/bnf_gallica_download.py --resolution half    # half resolution (~1 GB), much faster
python3 data-raw/bnf_gallica_download.py --only bd6t53563851 bpt6k994559s   # census volumes only
```

**Resolution.** A whole-page request to the gateway (`full/max`) is capped at
half the scan's native size: for example 1380 × 2121 pixels for a 2760 × 4243
page. The gateway does serve a region at native size when the request names an
explicit output width, so by default (`--resolution full`) the script fetches
each page as 900-pixel tiles at native resolution, stitches them, and
re-encodes the page once as JPEG (quality 92). `--resolution half` makes one
`full/max` request per page and keeps the JPEG byte for byte; it is lossless
with respect to what the gateway serves, four to five times smaller, and much
faster. The 1906 census volume, for instance, is 210 MB at full resolution and
38 MB at half.

Full-resolution PDFs go to `data-raw/bnf_gallica/pdf/`, half-resolution ones to
`data-raw/bnf_gallica/pdf_half/`, both gitignored. Pages are cached in
`data-raw/bnf_gallica/pages_full/` or `data-raw/bnf_gallica/pages/`, so an
interrupted run resumes where it stopped. The transcriptions in
`data-raw/colonial_census/` and `data-raw/yearbook_demography/` use the
half-resolution page cache plus native-resolution crops of hard-to-read cells
(`data-raw/yearbook_demography/hires.py`).

## Sources (`bnf_gallica_sources.csv`)

| Ark | Document | Pages |
|---|---|---:|
| [bd6t53563851](https://gallica.bnf.fr/ark:/12148/bd6t53563851) | Dénombrement de la population européenne civile en Tunisie au 16 décembre 1906 | 66 |
| [bpt6k994559s](https://gallica.bnf.fr/ark:/12148/bpt6k994559s) | Dénombrement de la population civile indigène (musulmane et israélite) en Tunisie au 22 mars 1931 | 81 |
| [bpt6k9105649x](https://gallica.bnf.fr/ark:/12148/bpt6k9105649x) | Statistique générale de la Tunisie 1922 | 1,471 |
| [bpt6k9105650k](https://gallica.bnf.fr/ark:/12148/bpt6k9105650k) | Statistique générale de la Tunisie 1925 | 1,061 |
| [bpt6k91056510](https://gallica.bnf.fr/ark:/12148/bpt6k91056510) | Statistique générale de la Tunisie 1927 | 1,057 |
| [bpt6k9105652d](https://gallica.bnf.fr/ark:/12148/bpt6k9105652d) | Statistique générale de la Tunisie 1929 | 1,071 |
| [bpt6k9105653t](https://gallica.bnf.fr/ark:/12148/bpt6k9105653t) | Statistique générale de la Tunisie 1935 | 340 |
| [bpt6k91056547](https://gallica.bnf.fr/ark:/12148/bpt6k91056547) | Statistique générale de la Tunisie 1936 | 212 |
| [bpt6k9105739w](https://gallica.bnf.fr/ark:/12148/bpt6k9105739w) | Statistique générale de la Tunisie 1939 | 190 |

These are all the BnF catalogue records (SRU API, `catalogue.bnf.fr/api/SRU`)
on Tunisian censuses or population statistics that link to a public Gallica copy.
Neighbouring arks were also probed through the gateway; no further
*Statistique générale* volumes turned up.

### Catalogued by the BnF but not on Gallica

The 1911, 1921, 1926, 1931 (European + indigenous), 1936 and 1956 census volumes
are catalogued as `LNUM` digital deposits (e.g. `cb46735991z`, `cb46736519c`,
`cb46736204h`, `cb46736246f`, `cb467362484`, `cb467362066`). These have no
Gallica ark and appear to be readable only on site at the BnF. The 1896 report on
the French population census (`cb304172920`) is print only.

## Rights and citation

Rights and holdings come from each document's IIIF manifest (`rights` and
`requiredStatement`):

- `bpt6k994559s` (1931 census) is held by the BnF and marked
  [NoC-NC](http://rightsstatements.org/vocab/NoC-NC/1.0/). Reuse is free if
  non-commercial; credit "Source gallica.bnf.fr / Bibliothèque nationale de France".
- `bd6t53563851` (1906 census) is held by the Bibliothèques de l'Université de
  Poitiers. The seven *Statistique générale* volumes are held by the Ministère
  des Affaires étrangères. These are marked
  [NoC-CR](http://rightsstatements.org/vocab/NoC-CR/1.0/): public domain, with
  reuse subject to the holding library's terms. Credit "Source gallica.bnf.fr /
  <holding institution>".

The script writes this credit line and the ark permalink into each PDF's
metadata (Author and Subject). The PDFs are not committed and are not covered by
the package's CC BY 4.0 licence. See "Archival Scans from Gallica" in the main
README for citation examples.
