# Tunisian census scans from Gallica (BnF)

`bnf_gallica_download.py` rebuilds full-resolution PDFs of the Tunisian census
documents digitized on Gallica, using the BnF's official IIIF gateway
(`openapi.bnf.fr`). `gallica.bnf.fr` itself is behind Cloudflare and refuses
scripted access. The gateway has no PDF endpoint, so the script downloads each
page as a full-resolution JPEG and wraps the pages losslessly into a PDF.

```bash
pip install img2pdf
python3 data-raw/bnf_gallica_download.py          # all 9 documents, ~2.6 GB
python3 data-raw/bnf_gallica_download.py --only bd6t53563851 bpt6k994559s   # census volumes only
```

The output goes to `data-raw/bnf_gallica/pdf/`, which is gitignored. Downloaded
pages are cached in `data-raw/bnf_gallica/pages/`, so an interrupted run resumes
where it stopped.

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

## Rights

Gallica marks these scans [NoC-NC](http://rightsstatements.org/vocab/NoC-NC/1.0/):
the works are in the public domain, but reuse of the scans must be
non-commercial and credited "Bibliothèque nationale de France / Gallica". This
differs from the package's CC BY 4.0 licence, which is one reason the PDFs are
not committed.
