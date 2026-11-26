#!/usr/bin/env python3
"""Prisons chapter (chapter V, *Établissements pénitentiaires*; from sgt1936 printed inside chapter IV
*Justice*) of the Statistique générale de la Tunisie, 12 editions sgt1922-sgt1939.

  python3 extract_prisons.py check   parse the transcriptions, run every check, print failures
  python3 extract_prisons.py build   ... and write csv/prisons_*.csv, their .md notes, csv/prisons_survey.md
                                     and csv/prisons_validation.json

Source of truth: transcribed/prisons_<edition>.txt (format in yb_tables.py). Transcribed so far: the
"Récapitulation du chiffre des détenus" (yearly prison population: number at 1 January, entries, releases,
number at 31 December, days of detention, daily average), printed for overlapping year windows in every edition
(SPEC_ADDENDUM rule 4: each year from the latest edition printing it, every other printing compared).
The other tables of the chapter are listed in csv/prisons_survey.md and are not transcribed yet.
"""
import sys
from decimal import Decimal

from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parent))  # shared helper yb_tables.py
from yb_tables import (COMMON, EDITIONS, ORDER, OUT, TR, Checks, coverage_lines, parse, select_latest, ssum,
                       where, write_csv, write_notes, write_validation, years_of)

CHAPTER = "Établissements pénitentiaires"
SCRIPT = "extract_prisons.py"
CHK = Checks()

# Views of the prisons tables (chapter title .. last view before the next chapter), confirmed on the images.
CHAPTER_VIEWS = {
    "sgt1922": (95, 102), "sgt1923": (579, 586), "sgt1924": (1069, 1076), "sgt1925": (105, 112),
    "sgt1926": (655, 664), "sgt1927": (117, 126), "sgt1928": (641, 650), "sgt1929": (119, 128),
    "sgt1930": (653, 662), "sgt1935": (81, 90), "sgt1936": (58, 61), "sgt1939": (53, 56),
}

M = {"start": "Effectif au 1er janvier", "entries": "Nombre d'entrées", "exits": "Nombre de sorties",
     "end": "Effectif au 31 décembre", "detention_days": "Nombre de journées de détention",
     "average": "Effectif moyen"}

# (year, measure) -> edition whose printing is stored instead of the latest (flag reprint_corrected)
REPRINT = {(1934, "end"): "sgt1935"}
REPRINT_WHY = {(1934, "end"): "sgt1936 prints the 31 December 1934 population with its middle digit broken "
                              "(\"2 6·8\"); sgt1935 prints 2.638, which is also sgt1935's and sgt1936's 1 January 1935 "
                              "figure"}


def run_checks(sec):
    rows = {int(r["label"]): r["cells"] for r in sec["rows"]}
    for y, c in rows.items():
        g = {k: c[k].value for k in c}
        CHK.eq("recap", f"{where(sec)} {y}: end = start + entries - exits",
               ssum([g["start"], g["entries"], None if g["exits"] is None else -g["exits"]]), g["end"])
        if g["detention_days"] is not None and g["average"] is not None:
            days = 366 if y % 4 == 0 else 365
            CHK.eq("recap", f"{where(sec)} {y}: average = detention days / {days} (to 1)",
                   (g["detention_days"] / days).quantize(Decimal(1)), g["average"], tol=Decimal(1))
        if y + 1 in rows:
            CHK.eq("recap", f"{where(sec)} start {y + 1} = end {y}", g["end"], rows[y + 1]["start"].value)


def cells(sec):
    out = []
    for r in sec["rows"]:
        for m, c in r["cells"].items():
            out.append({"census": sec["ed"], "table_id": sec["table"], "gallica_ark": sec["ark"],
                        "source_page": sec["page"], "gallica_view": sec["view"], "year": int(r["label"]),
                        "measure": m, "measure_fr": M[m], "value": c.value, "flag": c.flag})
    return out


COLDOC = {
    "census": "edition the value is taken from (`sgt1922` … `sgt1939`)",
    "table_id": "transcription section name (`recap`)",
    "gallica_ark": "Gallica volume ark (views are numbered within a volume)",
    "source_page": "printed page number",
    "gallica_view": "Gallica view (fNNNN)",
    "year": "calendar year of the figures",
    "measure": "`start`, `entries`, `exits`, `end`, `detention_days`, `average`",
    "measure_fr": "printed column heading",
    "value": "number of prisoners (start, end, average), of entries / releases, or of days of detention",
    "flag": "empty, `illegible` or `reprint_corrected`",
}

SURVEY = {
    "sgt1922": "f95 chapter title; f96 blank; f97 Administration a) répartition des condamnés d'après la nationalité, "
               "l'âge, le sexe et la catégorie pénale, b) d'après la nationalité, la nature du délit et la catégorie "
               "pénale; f98 c) journées de travail des détenus (by establishment and kind of work), Mouvement de la "
               "population a) mouvement général d'entrée et de sortie, effectif au 31 décembre (men and boys); f99 d) "
               "tableau comparatif des dépenses et des journées de détention (by prison; personnel, upkeep, food, "
               "price of the day of detention, products of the work), population au 31 décembre; f100 b) mouvement "
               "général (women), c) Prison de Tunis : transfèrements; f101 d) état numérique des décès par prison et "
               "par maladie; f102 e) état comparatif du personnel de garde avec l'effectif journalier maximum, f) "
               "récapitulation 1913-1922. Next chapter at f103.",
    "sgt1923": "f579 title; f580 blank; f581-f586 as sgt1922 (a), b) f581; c), mouvement a) f582; d) f583; mouvement "
               "b), transfèrements f584; décès f585; personnel de garde, récapitulation 1914-1923 f586).",
    "sgt1924": "f1069 title; f1070 blank; f1071-f1076 as sgt1922 (décès f1075; personnel, récapitulation 1915-1924 "
               "f1076).",
    "sgt1925": "f105 title; f106 blank; f107 a), b); f108 c) journées de travail, e) mouvement général (men); f109 d) "
               "dépenses et journées de détention; f110 f) mouvement général (women), g) Prison de Tunis : "
               "transfèrements; f111 h) décès par prison et par maladie; f112 i) personnel de garde, j) récapitulation "
               "1924-1925.",
    "sgt1926": "f655 title; f656 blank; f657 a), b); f658-f659 c) journées de travail, d) dépenses (spread); "
               "f660-f661 e), f) mouvement général (spread); f662 g) service des transfèrements, h) décès; f663 i) "
               "personnel de garde, j) récapitulation 1925-1926; f664 blank.",
    "sgt1927": "f117 title; f118 blank; f119 a), b); f120-f121 c), d) (with totaux généraux dépenses et recettes); "
               "f122-f123 e), f); f124 g), h); f125 i), j) 1926-1927; f126 blank.",
    "sgt1928": "f641 title; f642 blank; f643 a), b); f644-f645 c), d); f646-f647 e), f); f648 g), h); f649 i), j) "
               "1927-1928; f650 blank.",
    "sgt1929": "f119 title; f120 blank; f121 a), b); f122-f123 c), d); f124-f125 e), f); f126 g), h); f127 i), j) "
               "1928-1929; f128 blank.",
    "sgt1930": "f653 title; f654 blank; f655 a), b); f656-f657 c), d); f658-f659 e) mouvement général; f660 g), h); "
               "f661 i), j) 1929-1930; f662 blank.",
    "sgt1935": "f81 title; f82 blank; f83 a), b); f84-f85 d) dépenses (no c) table); f86-f87 e), f); f88 g), h); "
               "f89 i), j) 1933-1935; f90 blank.",
    "sgt1936": "inside chapter IV (Justice): f58 répartition des condamnés d'après la nationalité, l'âge, le sexe; "
               "d'après la nationalité et la nature du délit; f59-f60 mouvement général d'entrée et de sortie (two "
               "tables); f61 récapitulation du chiffre des détenus 1932-1936. f62 = chapter V Propriété foncière.",
    "sgt1939": "inside chapter IV (Justice): f53 répartition par nationalité, âge, sexe; par nationalité et nature du "
               "délit; f54-f55 mouvement général d'entrée et de sortie (two tables); f56 récapitulation 1935-1939. "
               "f57 = chapter V Propriété foncière.",
}

NOT_DONE = ("Not transcribed yet (this session ran out of budget after the Justice chapter): every table of the "
            "chapter except the récapitulation, i.e. a) prisoners by nationality, age, sex and penal category; b) "
            "by nationality, nature of the offence and sentence; c) days of work of the prisoners by establishment "
            "and kind of work; d) expenditure and days of detention by establishment (cost per day, products of "
            "the work); mouvement général d'entrée et de sortie by establishment (two tables); transfers; deaths by "
            "prison and disease; guard staff compared with the maximum daily population. Their views are listed "
            "above, per edition.")


def write_survey():
    L = ["# Prisons chapter: survey of every edition", "",
         "Page-by-page survey of the *Établissements pénitentiaires* tables (chapter V up to sgt1935; printed at the "
         "end of chapter IV *Justice* in sgt1936 and sgt1939). Views confirmed on the images. Extraction: "
         "`extract_prisons.py`.", "", "| edition | ark | views |", "|---|---|---|"]
    L += [f"| {e} | `{EDITIONS[e]}` | {a}–{b} |" for e, (a, b) in CHAPTER_VIEWS.items()]
    L += ["", "## Tables per edition", ""] + [f"- **{e}**: {t}" for e, t in SURVEY.items()]
    L += ["", "## Not transcribed", "", NOT_DONE, ""]
    (OUT / "prisons_survey.md").write_text("\n".join(L) + "\n")


def build(write=True):
    secs = []
    for ed in ORDER:
        p = TR / f"prisons_{ed}.txt"
        if p.exists():
            secs += parse(p, ed)
    recs = []
    for s in secs:
        run_checks(s)
        recs += cells(s)
    kept, compared, diffs = select_latest(recs, ["year", "measure"])
    reprinted = []
    for i, r in enumerate(kept):
        k = (r["year"], r["measure"])
        if k in REPRINT:
            src = [x for x in recs if x["census"] == REPRINT[k] and (x["year"], x["measure"]) == k][0]
            reprinted.append((k, r["census"], r["value"], REPRINT[k], src["value"], REPRINT_WHY[k]))
            kept[i] = dict(src, flag="reprint_corrected")
    kept.sort(key=lambda r: (r["year"], list(M).index(r["measure"])))
    fails = CHK.fail["recap"]
    if write:
        out = "prisons_population_recap"
        cols = COMMON + ["measure", "measure_fr", "value", "flag"]
        write_csv(out, cols, kept)
        paras = [
            "\"Récapitulation du chiffre des détenus\" (\"Récapitulation\" with ten years up to sgt1924, two years "
            "sgt1925-sgt1930, three in sgt1935, five in sgt1936 and sgt1939): for all the prisons of the Regency, "
            "the number of prisoners at 1 January, entries, releases, number at 31 December, days of detention and "
            "the average daily population (*effectif moyen*). The year 1931 is not printed by any edition; 1932 is "
            "printed only by sgt1936.",
            "Checks: end = start + entries − releases; start of year N+1 = end of year N; average = days of "
            "detention / days in the year (to ±1).",
            "Cells stored from an earlier printing (flag `reprint_corrected`): " + "; ".join(
                f"{k[0]} {k[1]}: {v1} from {e1} ({why})" for k, e0, v0, e1, v1, why in reprinted) + ".",
            "sgt1924 reprints 1915 with end 3.082 and 1.012.231 days (sgt1922-sgt1923: 2.874 and 1.092.231); the "
            "latest printing is stored by rule 4 (3.082 also satisfies 3.147 + 23.044 − 23.109), the earlier "
            "figures are listed among the differences.",
            "Survey of the whole chapter in every edition, and the tables not yet transcribed: `prisons_survey.md`."]
        write_notes(out, CHAPTER, SCRIPT, kept, cols, COLDOC,
                    "Récapitulation du chiffre des détenus", "Prison population: yearly summary", paras,
                    CHK.n["recap"], fails, compared, diffs, coverage_lines(secs),
                    "Printed for overlapping year windows: each year is taken from the **latest** edition that prints "
                    "it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing is compared below.",
                    "Unit: persons (population figures and average), entries / releases (count), days of detention.")
        write_validation(OUT / "prisons_validation.json", {
            out: dict(rows=len(kept), checks=CHK.n["recap"], failed=fails, overlap_compared=compared,
                      overlap_diffs=[list(d) for d in diffs], reprint_corrected=[list(x) for x in reprinted]),
            "_chapter_views": CHAPTER_VIEWS, "_survey": SURVEY, "_not_transcribed": NOT_DONE})
        write_survey()
    return kept, compared, diffs, fails


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    kept, compared, diffs, fails = build(write=(mode == "build"))
    print(f"prisons_population_recap: {len(kept)} rows, {CHK.n['recap']} checks, {len(fails)} failed, "
          f"{compared} compared, {len(diffs)} diffs")
    for f in fails:
        print("   FAIL", f)
    for d in diffs:
        print("   DIFF", d)


if __name__ == "__main__":
    main()
