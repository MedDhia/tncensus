#!/usr/bin/env python3
"""Build the place-name crosswalk for the colonial census and yearbook tables.

Collects every place name printed in the tables in inst/extdata/colonial
(controle_civil, annexe, caidat, commune, cheikhat, locality), gives each a
canonical contrôle civil (and caidat, for cheikhats), and links communes,
cheikhats and localities to the historical gazetteer `historical_geonames`
(data/historical_geonames.rda, read through R) where the match is unambiguous.

Output: data-raw/colonial_census/place_crosswalk.csv, saved as the
`colonial_place_crosswalk` dataset by place_crosswalk.R.

Matching rule. Names are normalised (accents, case, hyphens, apostrophes,
Arabic articles such as "El-"/"(El)", and common French/Arabic transliteration
variants: ou/u, dj/j, kh/k, ch/sh). A printed name matches a gazetteer entry
when the normalised names are equal (`exact`), or equal after dropping a
printed qualifier such as "(Ville)", "(Banlieue)", "(partie rurale)"
(`qualifier_stripped`). When several gazetteer entries match, the candidates
are narrowed to those in the same 1931 caidat (for cheikhats) or contrôle civil
(for localities and communes); a link is made only if exactly one remains.
A single candidate whose gazetteer contrôle civil differs from the printed
one (allowing for 1906 annexes, the military territories and the gazetteer's
use of "Soliman" for Grombalia) is not linked and is marked `conflict`: these
are mostly tribal names that recur in several regions. Otherwise the row is
`ambiguous` (several candidates left) or `none`. No fuzzy matching is done.

Usage:  python3 data-raw/colonial_census/place_crosswalk.py   (needs R with tncensus's data/)
"""
import csv
import re
import subprocess
import tempfile
import unicodedata
from collections import defaultdict
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PARQ = ROOT / "inst" / "extdata" / "colonial"
OUT = HERE / "place_crosswalk.csv"

# Canonical contrôle civil for every printed spelling (1931 spellings).
CONTROLE = {
    "Bizerte": "Bizerte", "Contrôle de Bizerte": "Bizerte",
    "Béja": "Béja", "Contrôle de Béja": "Béja",
    "Djerba": "Djerba", "Annexe de Djerba": "Djerba",
    "Gabès": "Gabès", "Contrôle de Gabès": "Gabès",
    "Gafsa": "Gafsa", "Contrôle de Gafsa": "Gafsa",
    "Grombalia": "Grombalia", "Contrôle de Grombalia": "Grombalia",
    "Kairouan": "Kairouan", "Contrôle de Kairouan": "Kairouan",
    "Le Kef": "Le Kef", "Kef (Le)": "Le Kef", "Kef": "Le Kef", "Contrôle du Kef": "Le Kef",
    "Maktar": "Maktar", "Mactar": "Maktar", "Contrôle de Mactar": "Maktar",
    "Medjez-el-Bab": "Medjez-el-Bab", "Medjez-El-Bab": "Medjez-el-Bab",
    "Annexe de Medjez-el-Bab": "Medjez-el-Bab",
    "Sfax": "Sfax", "Contrôle de Sfax": "Sfax",
    "Souk-el-Arba": "Souk-el-Arba", "Souk-El-Arba": "Souk-el-Arba", "Contrôle de Souk-el-Arba": "Souk-el-Arba",
    "Sousse": "Sousse", "Contrôle de Sousse": "Sousse",
    "Tabarka": "Tabarka", "Tabarca": "Tabarka", "Annexe de Tabarca": "Tabarka",
    "Téboursouk": "Téboursouk", "Teboursouk": "Téboursouk", "Annexe de Teboursouk": "Téboursouk",
    "Thala": "Thala", "Contrôle de Thala": "Thala",
    "Tozeur": "Tozeur", "Annexe de Tozeur": "Tozeur",
    "Tunis": "Tunis", "Contrôle de Tunis": "Tunis",
    "Zaghouan": "Zaghouan",
    # The southern military territories: "Territoire(s) du Sud" until the
    # early 1920s, "Territoires militaires" afterwards; the 1931 census volume
    # names their four subdivisions.
    "Territoire du Sud": "Territoires militaires du Sud", "Territoires du Sud": "Territoires militaires du Sud",
    "Territoires militaires": "Territoires militaires du Sud", "Territoires Militaires": "Territoires militaires du Sud",
    "Terr. Militaires": "Territoires militaires du Sud", "Territ. Milit.": "Territoires militaires du Sud",
    "Territoire militaire de Kebili": "Territoires militaires du Sud",
    "Territoire militaire de Matmata": "Territoires militaires du Sud",
    "Cercle militaire de Tatahouine": "Territoires militaires du Sud",
    "Cercles de Médenine, Ben-Gardane et Zarzis": "Territoires militaires du Sud",
    # 1906 Table G groups two districts in one row.
    "Béja et Medjez-el-Bab": "Béja et Medjez-el-Bab", "Gafsa et Tozeur": "Gafsa et Tozeur",
    "Ensemble du territoire (printed)": "Tunisie (total)",
}
CONTROLE_NOTE = {
    "Béja et Medjez-el-Bab": "1906 Table G groups Béja and its annexe Medjez-el-Bab in one row",
    "Gafsa et Tozeur": "1906 Table G groups Gafsa and its annexe Tozeur in one row",
    "Ensemble du territoire (printed)": "printed national total row",
    "Territoire militaire de Kebili": "1931 subdivision of the military territories (caidat of Nefzaoua)",
    "Territoire militaire de Matmata": "1931 subdivision of the military territories (caidat of Matmata)",
    "Cercle militaire de Tatahouine": "1931 subdivision of the military territories (caidat of Tatahouine)",
    "Cercles de Médenine, Ben-Gardane et Zarzis": "1931 subdivision of the military territories (caidat of Ouerghemma)",
}
for k in ("Annexe de Djerba", "Annexe de Medjez-el-Bab", "Annexe de Tabarca", "Annexe de Teboursouk", "Annexe de Tozeur"):
    CONTROLE_NOTE[k] = "an annexe (sub-district) in 1906; a contrôle civil in its own right by 1921"
# Canonical caidat (1931 Table II spellings) for every printed spelling.
CAIDAT = {"Aïn-Drahâm": "Aïn-Draham", "Djérid": "Djerid", "Kef": "Le Kef", "Madjeur": "Madjeurs",
          "Medjez-El-Bab": "Medjez-el-Bab", "Ouerghemma (Terr. de Médenine)": "Ouerghemma",
          "Ouerghemma (Terr. de Zarzis)": "Ouerghemma", "Ouled-Aoun": "Oulad-Aoun", "Ouled-Ayar": "Oulad-Ayar",
          "Souk-El-Arba": "Souk-el-Arba", "Souk-El-Khemis": "Souk-el-Khemis", "Tunis": "Tunis-Ville"}
# Gazetteer contrôle names that are equivalent to a canonical contrôle.
GAZ_CONTROLE = {"Soliman": "Grombalia", "Kef": "Le Kef", "Kebili": "Territoires militaires du Sud",
                "Matmata": "Territoires militaires du Sud", "Territoires du Sud": "Territoires militaires du Sud",
                "Cercle militaire de Tatahouine": "Territoires militaires du Sud",
                "Medenine, Ben-Gardane, Zarzis": "Territoires militaires du Sud"}
# 1906 annexes and their parent contrôle: a locality printed under either is compatible with both.
# The contrôle of Zaghouan was later carved out of the contrôle of Tunis, so
# 1906 localities printed under Tunis may be in Zaghouan in the gazetteer.
ANNEXE_PARENT = {"Djerba": "Gabès", "Medjez-el-Bab": "Béja", "Tabarka": "Souk-el-Arba",
                 "Téboursouk": "Le Kef", "Tozeur": "Gafsa", "Zaghouan": "Tunis"}


def compatible(gaz_ctl, ctl_std):
    """True unless the gazetteer places the entry in a different contrôle civil."""
    if not gaz_ctl or not ctl_std or ctl_std in ("Tunisie (total)",):
        return True
    a = GAZ_CONTROLE.get(gaz_ctl, gaz_ctl)
    group = {ctl_std, ANNEXE_PARENT.get(ctl_std, ctl_std)}
    group |= {k for k, v in ANNEXE_PARENT.items() if v == ctl_std}
    group |= {part.strip() for part in ctl_std.split(" et ")}
    return norm(a) in {norm(x) for x in group}


QUALIFIER = re.compile(r"\s*\((?:ville|banlieue|partie [a-zé]+|y compris [^)]*|commune[^)]*|centre|quartiers?[^)]*|"
                       r"environs|nord|sud|est|ouest|\d+)\)\s*|\s*\(\d+\)|\s*,.*$", re.I)


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[-'’().,:;/]", " ", s)
    s = re.sub(r"\b(el|la|le|les|l|ed|es|er|ez|et|de|du|des|d)\b", " ", s)
    for a, b in (("ou", "u"), ("dj", "j"), ("kh", "k"), ("ch", "sh"), ("ss", "s"), ("ll", "l"), ("ee", "e")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()


def gazetteer():
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "hg.csv"
        subprocess.run(["Rscript", "-e", f'load("{ROOT}/data/historical_geonames.rda"); '
                        f'write.csv(historical_geonames, "{out}", row.names = FALSE, na = "", fileEncoding = "UTF-8")'],
                       check=True, capture_output=True, env={"LANG": "en_US.UTF-8", "PATH": "/usr/bin:/usr/local/bin"})
        return pd.read_csv(out, dtype=str, keep_default_na=False)


def collect():
    """{(level, name, controle_printed, caidat_printed): set(tables)}"""
    seen = defaultdict(set)
    for f in sorted(PARQ.glob("*.parquet")):
        if f.stem == "index":
            continue
        d = pd.read_parquet(f)
        cols = [c for c in ("controle_civil", "annexe", "caidat", "commune", "cheikhat", "locality") if c in d.columns]
        if not cols:
            continue
        for _, r in d[cols].drop_duplicates().iterrows():
            ctl = r.get("controle_civil") if "controle_civil" in cols else None
            cai = r.get("caidat") if "caidat" in cols else None
            ctl = None if ctl is None or ctl != ctl else ctl   # NaN -> None
            cai = None if cai is None or cai != cai else cai
            for lvl in cols:
                v = r[lvl]
                if v is None or v != v or str(v).startswith("TOTAL"):
                    continue   # empty, or a printed-total marker, not a place
                key = (lvl, v, ctl if lvl in ("commune", "cheikhat", "locality", "annexe") else None,
                       cai if lvl in ("commune", "cheikhat", "locality") else None)
                seen[key].add(f.stem)
    return seen


def main():
    hg = gazetteer()
    gidx = defaultdict(set)
    for i, r in hg.iterrows():
        for c in ("locality_name_source", "locality_name_modern"):
            if r[c]:
                gidx[norm(r[c])].add(i)
    # caidat -> canonical contrôle, from the 1931 cheikhat table
    t3 = pd.read_parquet(PARQ / "ind1931_t3_cheikhat_nationality.parquet")
    caidat_ctl = {CAIDAT.get(c, c): CONTROLE[k] for k, c in t3[["controle_civil", "caidat"]].drop_duplicates().values}
    caidat_ctl["Le Kef"] = "Le Kef"

    rows = []
    for (lvl, name, ctl, cai), tables in sorted(collect().items(), key=lambda kv: (kv[0][0], kv[0][1], str(kv[0][2]), str(kv[0][3]))):
        ctl_std = CONTROLE.get(ctl) if ctl else None
        cai_std = CAIDAT.get(cai, cai) if cai else None
        note = ""
        if lvl == "controle_civil":
            ctl_std = CONTROLE[name]
            note = CONTROLE_NOTE.get(name, "")
            name_std = ctl_std
        elif lvl == "caidat":
            name_std = CAIDAT.get(name, name)
            ctl_std = caidat_ctl.get(name_std)
            if "Ouerghemma (" in name:
                note = "printed with its territory; part of the caidat of Ouerghemma"
        elif lvl == "annexe":
            name_std = CONTROLE.get(f"Annexe de {name}", name)
            ctl_std = ctl_std or name_std
        else:
            name_std = QUALIFIER.sub("", name).strip() or name
            if not ctl_std and cai_std:
                ctl_std = caidat_ctl.get(cai_std)
        match, cand, link = "none", [], None
        if lvl in ("commune", "cheikhat", "locality"):
            for method, key in (("exact", norm(name)), ("qualifier_stripped", norm(name_std))):
                cand = sorted(gidx.get(key, ()))
                if not cand:
                    continue
                if len(cand) > 1 and (cai_std or ctl_std):
                    narrowed = [i for i in cand
                                if (cai_std and norm(hg.at[i, "caidat_1931"]) == norm(cai_std))
                                or (ctl_std and norm(hg.at[i, "civil_control_1931"]) == norm(ctl_std))]
                    if narrowed:
                        cand = narrowed
                if len(cand) == 1:
                    if compatible(hg.at[cand[0], "civil_control_1931"], ctl_std):
                        match, link = method, cand[0]
                    else:
                        match = "conflict"
                else:
                    match = "ambiguous"
                break
        g = hg.loc[link] if link is not None else None
        rows.append({
            "level": lvl, "name_printed": name, "controle_civil_printed": ctl or "",
            "caidat_printed": cai or "", "name_std": name_std, "controle_civil_std": ctl_std or "",
            "caidat_std": cai_std or "", "note": note,
            "match": match if lvl in ("commune", "cheikhat", "locality") else "",
            "n_candidates": len(cand) if match in ("ambiguous", "conflict") else (1 if link is not None else 0),
            "locality_id_2024": g["locality_id_2024"] if g is not None else "",
            "locality_name_modern": g["locality_name_modern"] if g is not None else "",
            "delegation_1956": g["delegation_1956"] if g is not None else "",
            "lat": g["lat"] if g is not None else "", "lon": g["lon"] if g is not None else "",
            "tables": ";".join(sorted(tables)),
        })
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    df = pd.DataFrame(rows)
    print(f"{len(df)} rows")
    print(df.groupby("level")["match"].value_counts().unstack(fill_value=0))


if __name__ == "__main__":
    main()
