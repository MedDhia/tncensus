#!/usr/bin/env python3
"""Communes chapter (chapter II) of the Statistique générale de la Tunisie,
12 editions 1922-1939: municipal budgets and communal property (this file), and
loans, building permits and terraces/stalls (communes_more.py, run from here).

  python3 extract_communes.py check   parse transcriptions, run every check, print failures
  python3 extract_communes.py build   ... and write csv/communes_*.csv, their .md notes
                                      and csv/communes_validation.json

Source of truth: transcribed/communes_<edition>.txt, transcribed from the page
images (native-resolution crops from data-raw/yearbook_demography/hires.py),
Gallica OCR used only as a draft. Format: sections '@<table> view=.. page=..
[year=..|years=..]', a 'cols:' line, rows 'label | v v v'. Money in francs with
centimes after '.', no thousands separator; printed » = 0; 'NNN.xx' = franc part
legible, centimes hidden in the binding.

Tables printed for overlapping year windows (the budget, five years per
edition) follow SPEC_ADDENDUM rule 4: each year is taken from the latest
edition printing it, and every other printing of the same cell is compared.
Tables printed once per edition (communal property, at 31 December of a year)
follow rule 5; the one year printed twice (1928, sgt1928 and sgt1929) is taken
from the later edition and the two printings are compared. Printed totals are
used for checks only.

Corrections applied here (never in the transcriptions) are listed in SHIFT and
REPRINT; their reasons are in COMMENT and in the notes files.
"""
import csv
import json
import re
import sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
TR = HERE / "transcribed"
OUT = HERE / "csv"

EDITIONS = {
    "sgt1922": "bpt6k9105649x", "sgt1923": "bpt6k9105649x", "sgt1924": "bpt6k9105649x",
    "sgt1925": "bpt6k9105650k", "sgt1926": "bpt6k9105650k", "sgt1927": "bpt6k91056510",
    "sgt1928": "bpt6k91056510", "sgt1929": "bpt6k9105652d", "sgt1930": "bpt6k9105652d",
    "sgt1935": "bpt6k9105653t", "sgt1936": "bpt6k91056547", "sgt1939": "bpt6k9105739w",
}
ORDER = list(EDITIONS)

# Chapter view ranges (chapter title page .. last view before chapter III), confirmed on the images.
CHAPTER_VIEWS = {
    "sgt1922": (49, 64), "sgt1923": (527, 546), "sgt1924": (1015, 1034), "sgt1925": (47, 68),
    "sgt1926": (595, 616), "sgt1927": (59, 80), "sgt1928": (583, 604), "sgt1929": (59, 82),
    "sgt1930": (589, 614), "sgt1935": (41, 56), "sgt1936": (28, 39), "sgt1939": (23, 34),
}


# ----------------------------------------------------------------- parsing

class Cell:
    __slots__ = ("raw", "value", "hidden")

    def __init__(self, raw):
        self.raw = raw
        self.hidden = raw.endswith(".xx")
        if raw in (".", "?", "x"):
            self.value = None
        elif self.hidden:
            self.value = Decimal(raw[:-3])          # franc part only
        else:
            self.value = Decimal(raw)

    def money(self):
        return None if self.value is None or self.hidden else f"{self.value:.2f}"


def parse(ed):
    secs, cur = [], None
    for line in (TR / f"communes_{ed}.txt").read_text().splitlines():
        line = line.rstrip()
        if not line.strip() or line.startswith("#"):
            continue
        if line.startswith("@"):
            parts = line[1:].split()
            cur = {"table": parts[0], "ed": ed, "ark": EDITIONS[ed], "rows": [], "cols": None}
            for k, v in re.findall(r"(\w+)=([^=]+?)(?=\s+\w+=|$)", " ".join(parts[1:])):
                cur[k] = v.strip()
            cur["view"] = int(cur["view"])
            cur["page"] = int(cur["page"])
            if "years" in cur:
                ys = cur["years"]
                cur["years"] = (list(range(int(ys[:4]), int(ys[5:]) + 1)) if "-" in ys
                                else [int(y) for y in ys.split()])
            if "year" in cur:
                cur["year"] = int(cur["year"])
            secs.append(cur)
            continue
        if line.startswith("cols:"):
            cur["cols"] = line[5:].split()
            continue
        label, vals = line.rsplit("|", 1)
        cells = [Cell(x) for x in vals.split()]
        if len(cells) != len(cur["cols"]):
            raise ValueError(f"{ed} {cur['table']} view {cur['view']} row {label!r}: "
                             f"{len(cells)} values for {len(cur['cols'])} columns")
        cur["rows"].append({"label": label.strip(), "cells": cells})
    return secs


def is_total(label):
    return re.match(r"(?i)^totaux", label) is not None


def ckey(name):
    """Commune key for matching printings: spelling variants and footnote calls removed."""
    k = re.sub(r"\s*\(\d\)", "", name).replace("((", "(")
    for a, b in (("Fériana", "Feriana"), ("Kalaa", "Kalla"), ("Sbeïtla", "Sbeitla"),
                 ("Hadjeb-el-Aïoun", "Hadjeb-el-Aioun")):
        k = k.replace(a, b)
    return k


# ----------------------------------------------------------------- checks

class Checks:
    def __init__(self):
        self.n = defaultdict(int)
        self.fail = defaultdict(list)

    def eq(self, topic, what, got, printed, tol=Decimal(0)):
        if got is None or printed is None:
            return
        self.n[topic] += 1
        if abs(got - printed) > tol:
            self.fail[topic].append(f"{what}: cells give {got}, printed {printed} (difference {printed - got})")


CHK = Checks()


def check_budget(sec):
    data = [r for r in sec["rows"] if not is_total(r["label"])]
    tot = [r for r in sec["rows"] if is_total(r["label"])][-1]
    for j, c in enumerate(sec["cols"]):
        cells = [r["cells"][j] for r in data if r["cells"][j].value is not None]
        if len(cells) != len(data):
            continue                     # column not transcribed (sgt1923 rec_1921 is complete)
        nh = sum(1 for x in cells if x.hidden)
        got = sum(x.value for x in cells)
        # hidden centimes: each hidden cell may add up to 0,99
        tol = Decimal(nh) * Decimal("0.99")
        printed = tot["cells"][j].value
        if nh and printed is not None:
            CHK.n["budget"] += 1
            if not (got <= printed <= got + tol):
                CHK.fail["budget"].append(f"{sec['ed']} p.{sec['page']} {c}: franc parts give {got} "
                                          f"(+ up to {tol} hidden centimes), printed {printed}")
            continue
        CHK.eq("budget", f"{sec['ed']} p.{sec['page']} {c}: communes vs TOTAUX", got, printed)


def check_property(sec):
    for r in sec["rows"]:
        a, b, m, t = (x.value for x in r["cells"])
        CHK.eq("property", f"{sec['ed']} p.{sec['page']} {r['label']}: public + private + movable vs total",
               a + b + m, t)


# ----------------------------------------------------------------- corrections

COMMUNE_ORDER_1923 = ["Syndicat des Communes de la Banlieue Nord de Tunis", "Tabarka", "Tatahouine",
                      "Tebourba", "Teboursouk", "Thala", "Tozeur", "Tunis", "Zaghouan", "Zarzis"]
# (table, year, column kinds, ordered commune keys, shift): in every printing of the 1923 budget
# columns (sgt1923-sgt1927, the same type reused) the cells from the Syndicat line to the Zaghouan
# line belong one line lower (Tozeur's line carries the 10.483.423,50 of Tunis, Zarzis's line a »).
SHIFT = [("budget", 1923, ("rec", "dep"), COMMUNE_ORDER_1923, 1)]
# (year, commune key, kind) -> edition whose printing is stored instead of the latest one.
# sgt1923 and sgt1924 print the 1920 expenditure of Ferryville .. Grombalia one line too low
# (Ferryville », Gabès 208.247,74 ...); sgt1922 prints them on their own lines.
REPRINT = {(1920, c, "dep"): "sgt1922" for c in
           ("Ferryville", "Gabès", "Gafsa", "Ghardimaou", "Goulette (La)", "Grombalia")}


def apply_shift(table, year, kind, cells_by_commune, order_keys):
    """cells_by_commune: key -> (label, cell). Returns dict key -> cell after the shift."""
    out = {k: v for k, v in cells_by_commune.items()}
    moved = []
    for t, y, kinds, order, sh in SHIFT:
        if t != table or y != year or kind not in kinds:
            continue
        keys = [ckey(c) for c in order]
        printed = [cells_by_commune[k] for k in keys]
        # value printed on line i belongs to commune i+sh; the first sh communes get the cell
        # printed on the last sh lines (», i.e. 0)
        for i, k in enumerate(keys):
            src = keys[i - sh] if i - sh >= 0 else keys[len(keys) - sh + i]
            out[k] = cells_by_commune[src]
            if src != k:
                moved.append((k, cells_by_commune[src][1].raw, cells_by_commune[k][1].raw))
    return out, moved


# ----------------------------------------------------------------- build: budget

MEASURE = {"rec": ("receipts", "Recettes"), "dep": ("expenditure", "Dépenses")}
MEASURE_FR = {("sgt1936", "rec"): "Recettes y compris excédents laissés par les exercices antérieurs",
              ("sgt1939", "rec"): "Recettes y compris excédents laissés par les exercices antérieurs"}


def build_budget(all_secs):
    # printings[(year, key, kind)][ed] = dict(cell, label, sec)
    printings = defaultdict(dict)
    order = {}
    moved_all = []
    realigned = set()   # (year, commune key, kind) whose printed cell sits on another line
    for sec in [s for s in all_secs if s["table"] == "budget"]:
        check_budget(sec)
        data = [r for r in sec["rows"] if not is_total(r["label"])]
        for j, c in enumerate(sec["cols"]):
            kind, year = c.split("_")
            year = int(year)
            byc = {ckey(r["label"]): (r["label"], r["cells"][j]) for r in data}
            shifted, moved = apply_shift("budget", year, kind, byc, None)
            moved_all += [(sec["ed"], year, kind) + m for m in moved]
            realigned.update((year, m[0], kind) for m in moved)
            for i, r in enumerate(data):
                k = ckey(r["label"])
                label, cell = r["label"], shifted[k][1]
                if cell.value is None:
                    continue
                printings[(year, k, kind)][sec["ed"]] = dict(cell=cell, label=label, sec=sec)
                order.setdefault(k, (len(order)))
    rows, compared, diffs = [], 0, []
    for (year, k, kind), by in sorted(printings.items(), key=lambda kv: (kv[0][0], order[kv[0][1]], kv[0][2])):
        latest = [e for e in ORDER if e in by][-1]
        src = REPRINT.get((year, k, kind), latest)
        for e in by:
            if e != latest:
                compared += 1
                a, b = by[e]["cell"], by[latest]["cell"]
                if a.hidden or b.hidden:          # centimes hidden in one printing: compare franc parts
                    same = int(a.value) == int(b.value)
                else:
                    same = a.value == b.value
                if not same:
                    diffs.append((year, by[latest]["label"], kind, e, by[e]["cell"].raw, latest, by[latest]["cell"].raw))
        p = by[src]
        flag = ""
        if src != latest:
            flag = "reprint_corrected"
        if p["cell"].hidden:
            flag = "illegible"
        elif not flag and (year, k, kind) in realigned:
            flag = "row_realigned"
        sec = p["sec"]
        mfr = MEASURE_FR.get((sec["ed"], kind), MEASURE[kind][1])
        rows.append(dict(census=sec["ed"], table_id="budget", gallica_ark=sec["ark"], source_page=sec["page"],
                         gallica_view=sec["view"], year=year, commune=p["label"], measure=MEASURE[kind][0],
                         measure_fr=mfr, value=p["cell"].money(), flag=flag,
                         _hidden=str(p["cell"].value) if p["cell"].hidden else None))
    return rows, compared, diffs, moved_all, printings


# ----------------------------------------------------------------- build: property

PROP = {"public": ("public_domain_real_estate", "Valeurs immobilières : immeubles du domaine public"),
        "private": ("private_domain_real_estate", "Valeurs immobilières : immeubles du domaine privé"),
        "movable": ("movable_assets", "Valeurs mobilières")}


def build_property(all_secs):
    secs = [s for s in all_secs if s["table"] == "property"]
    for s in secs:
        check_property(s)
    by_year = defaultdict(list)
    for s in secs:
        by_year[s["year"]].append(s)
    rows, compared, diffs = [], 0, []
    for year, ss in sorted(by_year.items()):
        ss = sorted(ss, key=lambda s: ORDER.index(s["ed"]))
        keep = ss[-1]
        for other in ss[:-1]:
            a = {ckey(r["label"]): r for r in other["rows"]}
            for r in keep["rows"]:
                o = a.get(ckey(r["label"]))
                for j, c in enumerate(keep["cols"]):
                    compared += 1
                    if o is None or o["cells"][j].value != r["cells"][j].value:
                        diffs.append((year, r["label"], c, other["ed"], o["cells"][j].raw if o else "absent",
                                      keep["ed"], r["cells"][j].raw))
        for r in keep["rows"]:
            for j, c in enumerate(keep["cols"]):
                if c == "total":
                    continue
                code, fr = PROP[c]
                rows.append(dict(census=keep["ed"], table_id="property", gallica_ark=keep["ark"],
                                 source_page=keep["page"], gallica_view=keep["view"], year=year,
                                 commune=r["label"], category=code, category_fr=fr,
                                 value=r["cells"][j].money(), flag=""))
    return rows, compared, diffs


# ----------------------------------------------------------------- build: gas

GAS = {"public": ("public_lighting", "Éclairage public"), "private": ("private_lighting", "Éclairage privé")}
GAS_M = {"cons": ("consumption_m3", "Consommation (mètres cubes)"), "rec": ("receipts", "Recettes (fr. c.)")}


def check_gas(sec):
    for r in sec["rows"]:
        d = dict(zip(sec["cols"], r["cells"]))
        for m in ("cons", "rec"):
            a, b, t = d[f"{m}_public"].value, d[f"{m}_private"].value, d[f"{m}_total"].value
            if None in (a, b, t):
                continue
            CHK.eq("gas", f"{sec['ed']} p.{sec['page']} {r['label']} {m}: public + private vs total", a + b, t)


def build_gas(all_secs):
    printings = defaultdict(dict)
    for sec in [s for s in all_secs if s["table"] == "gas"]:
        check_gas(sec)
        for r in sec["rows"]:
            for c, cell in zip(sec["cols"], r["cells"]):
                printings[(int(r["label"]), c)][sec["ed"]] = dict(cell=cell, sec=sec)
    rows, compared, diffs = [], 0, []
    for (year, c), by in sorted(printings.items(), key=lambda kv: (kv[0][0], kv[0][1].split("_")[1], kv[0][1])):
        latest = [e for e in ORDER if e in by][-1]
        for e in by:
            if e != latest:
                compared += 1
                if by[e]["cell"].raw != by[latest]["cell"].raw:
                    diffs.append((year, "Tunis", c, e, by[e]["cell"].raw, latest, by[latest]["cell"].raw))
        m, l = c.split("_")
        if l == "total":
            continue
        p = by[latest]
        cell, sec = p["cell"], p["sec"]
        val = None if cell.value is None else (str(int(cell.value)) if m == "cons" else cell.money())
        rows.append(dict(census=sec["ed"], table_id="gas", gallica_ark=sec["ark"], source_page=sec["page"],
                         gallica_view=sec["view"], year=year, commune="Tunis", lighting=GAS[l][0],
                         lighting_fr=GAS[l][1], measure=GAS_M[m][0], measure_fr=GAS_M[m][1], value=val,
                         flag="not_applicable" if cell.raw == "x" else ""))
    return rows, compared, diffs


# ----------------------------------------------------------------- notes

COMMON = ["census", "table_id", "gallica_ark", "source_page", "gallica_view", "year"]
OUTPUTS = {
    "communes_budget": (["commune", "measure", "measure_fr"],
                        "Finances municipales : a) Budget des communes",
                        "Municipal finances: receipts and expenditure of each commune"),
    "communes_gas_tunis": (["commune", "lighting", "lighting_fr", "measure", "measure_fr"],
                           "Gaz : consommation (ville de Tunis)",
                           "Gas consumption and receipts, city of Tunis, public and private lighting"),
    "communes_property": (["commune", "category", "category_fr"],
                          "Biens communaux : valeurs immobilières et mobilières appartenant aux communes au 31 décembre",
                          "Communal property: real estate and movable assets owned by each commune at 31 December"),
}
COLDOC = {
    "census": "edition the value is taken from (`sgt1922` … `sgt1939`)",
    "table_id": "transcription section (`budget`, `property`, `gas`)",
    "gallica_ark": "Gallica volume ark (views are numbered within a volume)",
    "source_page": "printed page number",
    "gallica_view": "Gallica view (fNNNN)",
    "year": "budget year (exercice) / year of the 31 December valuation",
    "commune": "commune name exactly as printed in the edition the value is taken from (footnote calls such as "
               "`Kram (Le) (1)` kept)",
    "measure": "`receipts` (Recettes) or `expenditure` (Dépenses)",
    "measure_fr": "column heading as printed",
    "lighting": "`public_lighting` (Éclairage public) or `private_lighting` (Éclairage privé)",
    "lighting_fr": "column heading (French)",
    "category": "`public_domain_real_estate`, `private_domain_real_estate`, `movable_assets`",
    "category_fr": "column heading (French)",
    "value": "francs, centimes kept (two decimals); printed » = 0.00. Gas: consumption in cubic metres "
             "(integer), receipts in francs with centimes",
    "flag": "empty, `reprint_corrected`, `row_realigned`, `illegible` or `not_applicable` (see below)",
}
COMMENT = {
    "communes_budget": [
        "Table a) \"Budget des communes\" of the *Finances municipales* (a two-page spread from sgt1922 to "
        "sgt1935, one page in sgt1936 and sgt1939): for every commune, the receipts (*Recettes*) and "
        "expenditure (*Dépenses*) of the budget year, for five years (sgt1922–sgt1935) or three years "
        "(sgt1936: 1933–1935; sgt1939: 1936–1938). No budget lines are printed, only the two totals per "
        "commune. sgt1936 and sgt1939 head the receipts column \"Recettes y compris excédents laissés par les "
        "exercices antérieurs\" (receipts including surpluses carried over from earlier years); the 1933 and "
        "1934 figures are identical in sgt1935 (headed \"Recettes\") and sgt1936, so the heading changed, not "
        "the definition. The printed TOTAUX row is not stored. Printed » is stored as 0.00: it is printed for "
        "communes that had no budget yet (e.g. El-Djem, Hadjeb-el-Aïoun, Ksour-Essaf before 1923) or no "
        "longer (Kram (Le) from 1926, Pêcherie (La) from 1928) and for the Syndicat in some years.",
        "Years 1931–1932 are printed only in sgt1935 and 1935–1938 only in sgt1936 / sgt1939 (there are no "
        "1931–1934 or 1937–1938 yearbooks in the series).",
        "**Lines printed one row out of place.** (1) In all five printings of 1923 (sgt1923–sgt1927, the same "
        "type) the receipts and expenditure from the line of the Syndicat des Communes de la Banlieue Nord de "
        "Tunis to the line of Zaghouan belong one line lower: Tozeur's line carries 10.483.423,50 / "
        "7.065.936,84 (Tunis's budget; Tozeur has 125.715 in 1925), Tunis's line 60.716,43, and the line of "
        "Zarzis a ». Assigned by content (SHIFT in the script; the stored cells are flagged "
        "`row_realigned`): Syndicat 0, Tabarka 76.911,56 / 32.073,33 … Zarzis 42.900,01 / 25.617,81; "
        "every moved cell is listed below. (2) sgt1923 and sgt1924 print the 1920 expenditure of Ferryville, "
        "Gabès, Gafsa, Ghardimaou, Goulette (La) and Grombalia one line too low (Ferryville », Gabès "
        "208.247,74 …, Grombalia 132.138,19); sgt1922 prints them on their own lines (Ferryville 208.247,74 … "
        "Goulette 132.138,19, Grombalia »), which fits the receipts. These six cells are taken from sgt1922 "
        "(`reprint_corrected`).",
        "**1931 expenditure** (sgt1935 only): the centimes of the whole column are hidden in the binding "
        "(only the first digit of some is visible). The 59 cells are stored with value NA and flag "
        "`illegible`; their franc parts, which are legible, are listed below. Check: the franc parts sum to "
        "60.171.942, the printed total is 60.171.965,80 (difference 23,80 for 59 hidden centimes amounts, "
        "consistent). In sgt1922 the centimes of the 1919 expenditure are hidden in the same way; 1919 is "
        "stored from sgt1923, where they are legible, and only the franc parts of the sgt1922 printing were "
        "compared.",
        "Footnotes: sgt1926–sgt1930 \"Kram (Le) (1)\": (1) *Commune rattachée à celle de la Goulette à dater du "
        "1er juin 1926* (merged with La Goulette from 1 June 1926); sgt1928–sgt1930, Pêcherie (La), 1928 "
        "column \"(2) »\": (2) *Commune rattachée à celle de Bizerte à dater du 1er août 1928*; sgt1935, the "
        "1933 and 1934 expenditure of El-Djem, Kalla-Kebira and M'saken carry \"(1)\": (1) *Chiffres de 1933* "
        "(figures of 1933; El-Djem and Kalla-Kebira 1933 also nearly repeat 1932). sgt1922 prints \"Soliman (1)\" "
        "with no footnote on the page.",
        "Failed total checks (below) were re-read on the images; most are repeated identically in every "
        "printing of the year (e.g. 1922 receipts 235.190,61 short of the printed total in all five "
        "printings), so they are in the print. No cell could be identified, so none is flagged. Large ones: "
        "1918 receipts (−99.109,90), 1927 receipts (600.090,00; Ebba-Ksour prints receipts 144.669,40 and "
        "expenditure 644.386,16 in all four printings), 1929 receipts (409.989,80), 1932–1934 (sgt1935 / sgt1936, "
        "e.g. 1934 expenditure −1.125.155,10), 1938 receipts (−300.000).",
    ],
    "communes_gas_tunis": [
        "\"Gaz : consommation (ville de Tunis)\" (table b) of the *Service des eaux* pages in sgt1922–sgt1929, "
        "\"GAZ — Consommation (ville de Tunis)\" from sgt1930): for ten years (sgt1936: 1932–1936), the gas "
        "consumed (*Consommation*, cubic metres) and the receipts (*Recettes*, francs) for public lighting "
        "(*Éclairage public*) and private lighting (*Éclairage privé*); the TOTAL GÉNÉRAL columns are not stored "
        "(used for the row checks). sgt1939 prints no such series (only *Exploitation du gaz à Tunis* 1938–1939, "
        "not extracted).",
        "**How the cells were read.** Each printing was drafted from Gallica's OCR; every cell where the OCR of "
        "the 2–8 printings of a year disagreed, or did not parse, was read on a native-resolution crop of "
        "that printing (48 cells), and the rows missed by the OCR (sgt1926 1924–1925, sgt1927 1925, sgt1930 "
        "1921, sgt1936 1932–1936) were read on the images. Cells on which the OCR of all printings agreed were "
        "not looked at one by one; the overlap comparison is therefore only as independent as the OCR.",
        "The only difference between printings is sgt1928, 1925 public consumption, printed 812.614 (every "
        "other printing 312.614; 312.614 + 2.200.875 = 2.513.489, the printed total), stored from sgt1930 "
        "(312.614) as rule 4 says. 1934 receipts are printed » in sgt1935 and sgt1936 while consumption is "
        "given: stored as NA, `not_applicable` (not reported). 1926 repeats the 1925 consumption figures "
        "(312.614 / 2.200.875 / 2.513.489) in all five printings, with different receipts; kept as printed. "
        "1922 private consumption is printed \"1.459 904\" (1.459.904).",
        "Row-check failures repeat identically in every printing (they are in the print): e.g. 1919 receipts "
        "32.080,83 + 417.468,30 = 449.549,13 printed 469.549,13; 1920 68.636,98 + 472.404,90 printed "
        "496.041,88; 1925 539.725,47 + 1.964.968,81 printed 2.484.694,28; 1936 (sgt1936) 47.340,43 + "
        "7.788.430,21 printed 4.835.770,64.",
    ],
    "communes_property": [
        "\"Biens communaux — Valeurs immobilières et mobilières appartenant aux Communes au 31 décembre …\": "
        "per commune, real estate of the public domain (*Immeubles du domaine public*), real estate of the "
        "private domain (*Immeubles du domaine privé*), movable assets (*Valeurs mobilières*) and their sum "
        "(*Total général*, not stored; used for the row check). No column totals are printed.",
        "Valuation dates: sgt1922 → 31.12.1922 … sgt1928 → 31.12.1928; **sgt1929 reprints the 1928 table** "
        "(heading \"au 31 décembre 1928\", every cell equal to sgt1928): 1928 is stored from sgt1929 and the "
        "sgt1928 printing compared (rule 4); sgt1930 → 1930; sgt1935 → 1934; sgt1936 → 1935; sgt1939 → 1937. "
        "The years 1929, 1931–1933 and 1936 are not printed.",
        "The commune list follows the page (sgt1929, sgt1930 and sgt1935 have no Sbeïtla row; Kram and "
        "Pêcherie are listed until sgt1930). Values are often printed half a line below their label; rows "
        "were assigned by counting lines, and the row totals confirm the assignment. Printed » is stored as "
        "0.00.",
        "Row-check failures (below) were re-read on native-resolution crops and agree with the Gallica OCR; "
        "the print is inconsistent and no cell can be singled out, so none is flagged. Some repeat across "
        "editions (Medjez-el-Bab 38.000 + 22.000 = 60.000 printed 70.000, sgt1925–sgt1930; Maxula-Radès "
        "99.743,97 + 10.810,40 printed 104.554,37 in sgt1924–sgt1926, corrected to 110.554,37 from sgt1927; "
        "Zarzis 142.043,59 + 9.243,65 printed 151.337,24, sgt1927–sgt1930). sgt1923: the 0,20 of Tunis's "
        "movable assets (188.475,20) is printed on Tozeur's total (102.650,20) instead of Tunis's "
        "(11.215.475 »).",
    ],
}


def write_csv(name, rows):
    dims = OUTPUTS[name][0]
    cols = COMMON + dims + ["value", "flag"]
    OUT.mkdir(exist_ok=True)
    with (OUT / f"{name}.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in cols})


def fmt_views(rows):
    by = defaultdict(set)
    for r in rows:
        by[r["census"]].add((r["source_page"], r["gallica_view"]))
    return "; ".join(f"{e} (`{EDITIONS[e]}`): " + ", ".join(f"p. {p}, f{v}" for p, v in sorted(by[e]))
                     for e in ORDER if e in by)


def write_notes(name, rows, info):
    dims, tfr, ten = OUTPUTS[name]
    years = sorted({r["year"] for r in rows})
    L = [f"# {tfr}", "", f"*{ten}.*", "",
         "Source: *Statistique générale de la Tunisie*, chapter II *Communes*, editions "
         + ", ".join(e for e in ORDER if e in {r['census'] for r in rows} or e in info.get("printed_eds", ()))
         + ". Source gallica.bnf.fr / Ministère des Affaires étrangères.", "",
         f"Pages and views of the stored values: {fmt_views(rows)}.", "",
         "Transcriptions: `../transcribed/communes_<edition>.txt`, section "
         f"`@{rows[0]['table_id']}`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_communes.py "
         "build`. Per-check output: `communes_validation.json`.", "",
         f"Rows: {len(rows)}. Years: {', '.join(map(str, years))}.", "",
         "Unit: francs (French/Tunisian franc), as printed, centimes kept.", ""]
    if info.get("rule4"):
        L += [info["rule4"], ""]
    L += ["## Columns", ""]
    for c in COMMON + dims + ["value", "flag"]:
        L.append(f"- `{c}`: {COLDOC[c]}")
    L += [""]
    for p in COMMENT[name]:
        L += [p, ""]
    v = info["checks"]
    L += ["## Validation", "",
          f"- Checks against printed totals: {v['n']}; passed: {v['n'] - len(v['fail'])}; failed: {len(v['fail'])}."]
    if v["fail"]:
        L += ["", "Failed checks (printed values kept):", ""] + [f"  - {x}" for x in v["fail"]]
    L += ["", f"- Overlapping printings: {info['compared']} cell comparisons between editions; "
          f"{len(info['diffs'])} differences."]
    if info["diffs"]:
        L += ["", "| year | commune | column | edition | printed | latest edition | printed |", "|---|---|---|---|---|---|---|"]
        L += [f"| {d[0]} | {d[1]} | {d[2]} | {d[3]} | {d[4]} | {d[5]} | {d[6]} |" for d in info["diffs"]]
    if info.get("moved"):
        L += ["", f"- Cells assigned by content (SHIFT, {len(info['moved'])} printed cells in "
              f"{len({m[0] for m in info['moved']})} editions): stored cell ← value printed on the line above "
              "(edition, year, column, commune, value assigned, value printed on its own line):", ""]
        L += [f"  - {m[0]} {m[1]} {m[2]} {m[3]}: {m[4]} (own line: {m[5]})" for m in info["moved"]]
    fl = defaultdict(int)
    for r in rows:
        if r["flag"]:
            fl[r["flag"]] += 1
    L += ["", "- Flagged cells: " + (", ".join(f"{k}: {n}" for k, n in sorted(fl.items())) if fl else "none") + "."]
    if fl:
        L += [""] + [f"  - {r['census']} {r['year']} {r['commune']} {r.get('measure', r.get('category'))} = "
                     f"{r['value'] if r['value'] is not None else 'NA'}"
                     + (f" (franc part {r['_hidden']})" if r.get("_hidden") else "") + f" ({r['flag']})"
                     for r in rows if r["flag"]]
    (OUT / f"{name}.md").write_text("\n".join(L) + "\n")


# ----------------------------------------------------------------- main

def build(write=True):
    all_secs = []
    for ed in ORDER:
        all_secs += parse(ed)
    brows, bcomp, bdiffs, moved, _ = build_budget(all_secs)
    prows, pcomp, pdiffs = build_property(all_secs)
    grows, gcomp, gdiffs = build_gas(all_secs)
    res = {
        "communes_budget": dict(rows=brows, compared=bcomp, diffs=bdiffs, moved=moved,
                                checks=dict(n=CHK.n["budget"], fail=CHK.fail["budget"]),
                                rule4="Printed for overlapping five-year windows: each year is taken from the "
                                      "**latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that "
                                      "edition) and every other printing of the same cell is compared below."),
        "communes_gas_tunis": dict(rows=grows, compared=gcomp, diffs=gdiffs,
                                   checks=dict(n=CHK.n["gas"], fail=CHK.fail["gas"]),
                                   rule4="Printed for overlapping ten-year windows: each year is taken from the "
                                         "**latest** edition that prints it (rule 4) and every other printing "
                                         "compared."),
        "communes_property": dict(rows=prows, compared=pcomp, diffs=pdiffs,
                                  checks=dict(n=CHK.n["property"], fail=CHK.fail["property"]),
                                  rule4="Printed once per edition (rule 5), for 31 December of the year in the "
                                        "heading; the 1928 table printed twice is taken from the later edition."),
    }
    if write:
        for name, r in res.items():
            write_csv(name, r["rows"])
            write_notes(name, r["rows"], r)
        val = {name: dict(rows=len(r["rows"]), checks=r["checks"]["n"], failed=r["checks"]["fail"],
                          overlap_compared=r["compared"], overlap_diffs=[list(map(str, d)) for d in r["diffs"]],
                          shifted_cells=[list(map(str, m)) for m in r.get("moved", [])])
               for name, r in res.items()}
        val["_chapter_views"] = CHAPTER_VIEWS
        (OUT / "communes_validation.json").write_text(json.dumps(val, indent=1, ensure_ascii=False) + "\n")
    return res


# =================================================================== more tables
# Loans (Emprunts communaux; Caisse des Prêts Communaux), building permits (Autorisations de bâtir;
# Constructions immobilières 1939) and terraces / street stalls (Terrasses et étalages).
# Transcriptions: transcribed/communes_<topic>_<edition>.txt. Same conventions as above, plus:
#   'x' = text printed instead of a number (stored NA, not_applicable; the text is in a '#' comment above
#   the row and in the notes), '?' = illegible (NA, illegible), 'néant' = printed "néant" (stored 0),
#   '= <heading>' starts a commune block (loans), 'NNN.xx' = franc part only (centimes in the binding).
# Every table here is printed once per edition (SPEC_ADDENDUM rule 5); the year is the edition's.

MORE_MEASURES = {
    "permits": {
        "constructions": ("constructions", "Constructions ou reconstructions"),
        "raising": ("raising", "Surélévation"),
        "n_auth": ("permits_issued", "Nombre d'autorisations"),
    },
    "constructions": {
        "n_auth": ("permits_issued", "Nombre total des autorisations de bâtir"),
        "housing": ("value_housing", "Valeur : logements à usage d'habitation"),
        "commercial": ("value_commercial_industrial", "Valeur : bâtiments commerciaux et industriels"),
        "other": ("value_other", "Valeur : constructions diverses"),
    },
    "terraces": {
        "terr_n": ("terraces_number", "Terrasses (chaises de tables de limonadiers) : nombre"),
        "terr_surf": ("terraces_surface_m2", "Terrasses : surface (mètre carré)"),
        "terr_prod": ("terraces_receipts", "Terrasses : produits"),
        "stall_n": ("stalls_number", "Étalages (dépôts de marchandises de toutes sortes) : nombre"),
        "stall_surf": ("stalls_surface_m2", "Étalages : surface (mètre carré)"),
        "stall_prod": ("stalls_receipts", "Étalages : produits"),
    },
    "caisse": {
        "dur": ("duration_years", "Durée des emprunts (ans)"),
        "cap_net": ("capital_received", "Capital net touché par la Commune"),
        "cap_nom": ("capital_nominal", "Capital nominal à rembourser par la Commune"),
        "rate": ("interest_rate_pct", "Taux de l'intérêt"),
        "annuity": ("annuity", "Montant de chaque annuité"),
        "due": ("annuities_due_to_date", "Annuités échues à la fin de l'année"),
        "paid_year": ("paid_in_year", "Payements : en <année>"),
        "paid_before": ("paid_before", "Payements : antérieurement"),
        "paid_total": ("paid_total", "Payements : total"),
        "arrears": ("arrears", "Restes à payer sur les annuités échues"),
        "amortised": ("capital_amortised", "Amortissement : capital compris dans les annuités payées"),
        "remaining": ("capital_remaining", "Amortissement : capital restant à amortir à la fin de l'année"),
    },
    "tunis_bonds": {
        "dur": ("duration_years", "Durée des emprunts (ans)"),
        "rate": ("interest_rate_pct", "Taux de l'intérêt"),
        "cap_net": ("capital_received", "Capital net encaissé par la Commune"),
        "cap_nom": ("capital_nominal", "Capital nominal à rembourser par la Commune"),
        "int_due": ("interest_due", "Sommes échues : intérêts (coupons échus)"),
        "cap_due": ("capital_due", "Sommes échues : capitaux (obligations sorties aux tirages)"),
        "int_paid_year": ("interest_paid_in_year", "Payements effectués en <année> : intérêts"),
        "cap_paid_year": ("capital_paid_in_year", "Payements effectués en <année> : capitaux"),
        "int_paid_before": ("interest_paid_before", "Payements effectués antérieurement : intérêts"),
        "cap_paid_before": ("capital_paid_before", "Payements effectués antérieurement : capitaux"),
        "int_paid_total": ("interest_paid_total", "Payements effectués, total : intérêts"),
        "cap_paid_total": ("capital_paid_total", "Payements effectués, total : capitaux"),
        "int_lapsed": ("interest_lapsed", "Sommes atteintes par la déchéance : intérêts"),
        "cap_lapsed": ("capital_lapsed", "Sommes atteintes par la déchéance : capitaux"),
        "int_outstanding": ("interest_outstanding", "Restes à payer à la clôture de l'exercice : intérêts"),
        "cap_outstanding": ("capital_outstanding", "Restes à payer à la clôture de l'exercice : capitaux"),
    },
}
INT_COLS = {"constructions", "raising", "n_auth", "terr_n", "stall_n", "dur"}
MORE_CHK = Checks()


class MCell:
    __slots__ = ("raw", "value", "hidden", "flag")

    def __init__(self, raw):
        self.raw, self.hidden, self.flag = raw, raw.endswith(".xx"), ""
        if raw == "x":
            self.value, self.flag = None, "not_applicable"
        elif raw == "?":
            self.value, self.flag = None, "illegible"
        elif raw == ".":
            self.value, self.flag = None, "absent"
        elif raw == "néant":
            self.value = Decimal(0)
        elif self.hidden:
            self.value, self.flag = Decimal(raw[:-3]), "illegible"
        else:
            self.value = Decimal(raw)

    def num(self):
        return self.value

    def out(self, col):
        if self.value is None or self.hidden:
            return None
        if col in INT_COLS and self.value == int(self.value):
            return str(int(self.value))
        if col == "rate" or self.value != int(self.value) or col.endswith("surf"):
            return format(self.value.normalize(), "f") if col in ("rate",) or col.endswith("surf") else f"{self.value:.2f}"
        return f"{self.value:.2f}"


def parse_more(path, ed):
    secs, cur, head, comment = [], None, None, []
    for line in path.read_text().splitlines():
        line = line.rstrip()
        if not line.strip():
            continue
        if line.startswith("#"):
            if cur is not None:
                comment.append(line[1:].strip())
            continue
        if line.startswith("@"):
            parts = line[1:].split()
            cur = {"table": parts[0], "ed": ed, "ark": EDITIONS[ed], "rows": []}
            for k, v in re.findall(r"(\w+)=(\S+)", " ".join(parts[1:])):
                cur[k] = int(v)
            secs.append(cur)
            head, comment = None, []
            continue
        if line.startswith("cols:"):
            cur["cols"] = line[5:].split()
            continue
        if line.startswith("="):
            head = line[1:].strip()
            continue
        label, vals = line.rsplit("|", 1)
        cells = [MCell(x) for x in vals.split()]
        if len(cells) != len(cur["cols"]):
            raise ValueError(f"{path.name} {label!r}: {len(cells)} values for {len(cur['cols'])} columns")
        cur["rows"].append({"label": label.strip(), "head": head, "cells": dict(zip(cur["cols"], cells)),
                            "note": " ".join(comment)})
        comment = []
    return secs


def is_tot(label):
    return re.match(r"(?i)^tota", label) is not None


def commune_of(head):
    return re.sub(r"^Commune (de la |de |d'|d’|du )", lambda m: "" if m.group(1) in ("de ", "d'", "d’") else
                  {"de la ": "la ", "du ": "le "}[m.group(1)], head)


def chk_col_totals(topic, sec, groups):
    """groups: list of (name, data rows, total row). Hidden centimes widen the tolerance."""
    for name, data, tot in groups:
        for c in sec["cols"]:
            t = tot["cells"][c]
            if t.value is None:
                continue
            # a cell with text instead of a number ('x') adds nothing to the printed total
            xs = [r["cells"][c] for r in data if r["cells"][c].flag != "not_applicable"]
            if any(x.value is None for x in xs):
                MORE_CHK.n[topic + "_skipped"] += 1
                continue
            nh = sum(1 for x in xs + [t] if x.hidden)
            got = sum(x.value for x in xs)
            MORE_CHK.n[topic] += 1
            tol = Decimal(nh) * Decimal("0.99")
            if abs(got - t.value) > tol:
                MORE_CHK.fail[topic].append(f"{sec['ed']} p.{sec['page']} {name} {c}: cells give {got}, "
                                            f"printed total {t.raw} (difference {t.value - got})")


def chk_identities(topic, sec, row, rels, name):
    for tgt, plus, minus in rels:
        cs = [row["cells"][c] for c in [tgt] + plus + minus]
        if any(x.value is None for x in cs):
            continue
        nh = sum(1 for x in cs if x.hidden)
        got = sum(row["cells"][c].value for c in plus) - sum(row["cells"][c].value for c in minus)
        MORE_CHK.n[topic] += 1
        if abs(got - row["cells"][tgt].value) > Decimal(nh) * Decimal("0.99"):
            MORE_CHK.fail[topic].append(f"{sec['ed']} p.{sec['page']} {name}: {tgt} printed "
                                        f"{row['cells'][tgt].raw}, {' + '.join(plus)}"
                                        f"{''.join(' - ' + m for m in minus)} = {got}")


LOAN_RELS = {
    "caisse": [("paid_total", ["paid_year", "paid_before"], []), ("arrears", ["due"], ["paid_total"]),
               ("remaining", ["cap_nom"], ["amortised"])],
    "tunis_bonds": [("int_paid_total", ["int_paid_year", "int_paid_before"], []),
                    ("cap_paid_total", ["cap_paid_year", "cap_paid_before"], []),
                    ("int_outstanding", ["int_due"], ["int_paid_total", "int_lapsed"]),
                    ("cap_outstanding", ["cap_due"], ["cap_paid_total", "cap_lapsed"])],
}


def more_rows(sec, row, topic, commune, extra):
    out = []
    for c, cell in row["cells"].items():
        code, fr = MORE_MEASURES[sec["table"]][c]
        flag = cell.flag if cell.flag != "absent" else ""
        if cell.flag == "absent":
            continue
        right = "view2" in sec and c not in LEFT_COLS.get(sec["table"], ())
        out.append(dict(census=sec["ed"], table_id=sec["table"], gallica_ark=sec["ark"],
                        source_page=sec["page"] + (1 if right else 0),
                        gallica_view=sec.get("view2", sec["view"]) if c not in LEFT_COLS.get(sec["table"], ())
                        else sec["view"], year=sec["year"], commune=commune, **extra,
                        measure=code, measure_fr=fr.replace("<année>", str(sec["year"])),
                        value=cell.out(c), flag=flag,
                        _hidden=str(cell.value) if cell.hidden else None, _note=row["note"]))
    return out


# columns printed on the left page of a two-page loan spread (the others are on view2)
LEFT_COLS = {"caisse": ("dur", "cap_net", "cap_nom", "rate", "annuity"),
             "tunis_bonds": ("dur", "rate", "cap_net", "cap_nom", "int_due", "cap_due")}


def build_more(write=True, verbose=False):
    secs = []
    for f in sorted(TR.glob("communes_*_sgt*.txt")):
        ed = re.search(r"(sgt\d{4})", f.name).group(1)
        secs += parse_more(f, ed)
    res = {}
    # ---- building permits (one layout sgt1922-sgt1936)
    rows = []
    for s in [s for s in secs if s["table"] == "permits"]:
        data = [r for r in s["rows"] if not is_tot(r["label"])]
        tots = [r for r in s["rows"] if is_tot(r["label"])]
        if tots:
            chk_col_totals("permits", s, [("communes", data, tots[0])])
        for r in data:
            rows += more_rows(s, r, "permits", r["label"], {})
    res["communes_building_permits"] = rows
    rows = []
    for s in [s for s in secs if s["table"] == "constructions"]:
        for r in s["rows"]:
            rows += more_rows(s, r, "constructions", r["label"], {})
    res["communes_building_values_1939"] = rows
    # ---- terraces
    rows = []
    for s in [s for s in secs if s["table"] == "terraces"]:
        data = [r for r in s["rows"] if not is_tot(r["label"])]
        tots = [r for r in s["rows"] if is_tot(r["label"])]
        if tots:
            chk_col_totals("terraces", s, [("communes", data, tots[0])])
        for r in data:
            rows += more_rows(s, r, "terraces", r["label"], {})
    res["communes_terraces"] = rows
    # ---- loans
    xed = []   # cross-edition: paid_before(N) = paid_total(N-1)
    for t, name in (("caisse", "communes_loans_caisse"), ("tunis_bonds", "communes_loans_tunis_bonds")):
        rows = []
        for s in [s for s in secs if s["table"] == t]:
            groups = defaultdict(list)
            for r in s["rows"]:
                groups[r["head"]].append(r)
            gl = []
            for head, rs in groups.items():
                data = [r for r in rs if not is_tot(r["label"])]
                tots = [r for r in rs if is_tot(r["label"])]
                for r in rs:
                    chk_identities("loans", s, r, LOAN_RELS[t], f"{head} / {r['label']}")
                if tots:
                    gl.append((head, data, tots[0]))
                for i, r in enumerate(data, 1):
                    rows += more_rows(s, r, "loans", commune_of(head), dict(commune_heading_fr=head,
                                                                           loan_fr=r["label"]))
            chk_col_totals("loans", s, gl)
        res[name] = rows
    # cross-edition consistency of the loan tables
    for name, pairs in (("communes_loans_caisse", [("paid_before", "paid_total")]),
                        ("communes_loans_tunis_bonds", [("interest_paid_before", "interest_paid_total"),
                                                        ("capital_paid_before", "capital_paid_total")])):
        idx = {}
        for r in res[name]:
            idx[(r["year"], r["commune"], r["loan_fr"], r["measure"])] = r
        for (y, c, l, m), r in idx.items():
            for before, total in pairs:
                if m != MORE_MEASURES["caisse" if "caisse" in name else "tunis_bonds"].get(
                        {"paid_before": "paid_before"}.get(before, ""), (before,))[0] and m != before:
                    continue
                p = idx.get((y - 1, c, l, total))
                if p is None or r["value"] is None or p["value"] is None:
                    continue
                MORE_CHK.n["loans_xed"] += 1
                if Decimal(r["value"]) != Decimal(p["value"]):
                    xed.append(f"{c} {l}: {before} {y} ({r['census']}) = {r['value']}, {total} {y - 1} "
                               f"({p['census']}) = {p['value']}")
    MORE_CHK.fail["loans_xed"] = xed
    if write:
        for name, rows in res.items():
            write_more(name, rows)
    if verbose:
        for name, rows in res.items():
            print(f"{name}: {len(rows)} rows")
        for t in ("permits", "terraces", "loans", "loans_xed"):
            print(f"  checks {t}: {MORE_CHK.n[t]}, failed {len(MORE_CHK.fail[t])}"
                  + (f", skipped (NA cell in column) {MORE_CHK.n[t + '_skipped']}" if MORE_CHK.n[t + '_skipped'] else ""))
            for f_ in MORE_CHK.fail[t]:
                print("    FAIL", f_)
    return res


MORE_DIMS = {
    "communes_building_permits": ["commune", "measure", "measure_fr"],
    "communes_building_values_1939": ["commune", "measure", "measure_fr"],
    "communes_terraces": ["commune", "measure", "measure_fr"],
    "communes_loans_caisse": ["commune", "commune_heading_fr", "loan_fr", "measure", "measure_fr"],
    "communes_loans_tunis_bonds": ["commune", "commune_heading_fr", "loan_fr", "measure", "measure_fr"],
}


MORE_NOTES = {
    "communes_building_permits": (
        "Concessions sur la voie publique : a) Autorisations de bâtir",
        "Building permits issued by each commune: constructions or reconstructions, raisings (surélévations) "
        "and number of permits.",
        "communes_permits_<edition>.txt",
        "count (integer); printed » and printed *néant* are stored as 0",
        ["Table a) of the *Concessions sur la voie publique* pages (sgt1922–sgt1935), \"Autorisations de bâtir "
         "délivrées en 1936\" in sgt1936. Columns: *Constructions ou reconstructions*, *Surélévation*, *Nombre "
         "d'autorisations* (sgt1936: footnote (1) on the last column, *Toutes opérations comprises*). The number "
         "of permits is often not the sum of the first two columns (e.g. Gabès 1924: 8 + 2, 65 permits); this is "
         "how the table is printed, so no row identity is checked. sgt1939 prints a different table "
         "(`communes_building_values_1939.csv`). sgt1935 page 26 of view 46.",
         "**Image versus OCR.** Every cell of every edition was read on native-resolution crops of the page "
         "image (half-page strips of the label column and the three value columns); Gallica's OCR was only used "
         "as a draft and to locate lines. In sgt1928, sgt1929 and sgt1930 the values are printed half a line to a "
         "full line below their labels and the OCR assigns them to the wrong commune; the rows were assigned by "
         "counting the 58 value lines against the 58 labels. Uncertain readings: sgt1928 Hammam-Lif permits 83 "
         "(last digit damaged, or 88); sgt1929 Tunis permits printed with a broken middle digit (7?7) → NA, "
         "`illegible`. sgt1935: the permits column is curved into the binding on view 46; Ariana 34, Grombalia "
         "22, Kalaa-Kebira 112 and Maxula-Radès 62 were read on the gutter strip visible at the left edge of view "
         "47 (view 46 alone suggests 31/23/113/63).",
         "Not applicable cells: sgt1924 El-Djem (\"Il n'existe pas de droits de voirie à El-Djem\" printed "
         "across the row); sgt1930 Foum-Tatahouine raising printed \"3 m. 50\" (a length, not a count).",
         "Printed totals: sgt1922–sgt1925 all three columns; sgt1926 and sgt1927 the permits column only; none "
         "from sgt1928. Failed checks were re-read on the images (the printed cells are as transcribed); "
         "no single cell explains them, so no cell is flagged.",
         "Footnotes (calls kept in the commune names): sgt1922 (1) El-Djem, (2) Hadjeb-el-Aïoun, (3) Ksour-Essaf: "
         "*Commune créée le 29 mars 1922 / 9 mai 1922 / 29 mars 1922*. sgt1926–sgt1930 calls on Béja, El-Djem, "
         "Kairouan, Kef, Monastir, Tabarka, Tunis, Ferryville, Menzel-bou-Zelfa, Soliman, Zarzis refer to notes "
         "on the stalls/terraces of the facing page (see `communes_terraces.md`)."]),
    "communes_building_values_1939": (
        "Constructions immobilières en 1939 (Villes de plus de 5.000 habitants)",
        "Building in 1939, towns of more than 5,000 inhabitants: number of building permits and value of the "
        "buildings (housing, commercial and industrial, other).",
        "communes_constructions_sgt1939.txt",
        "permits: integer count (*néant* = 0); values: francs (no centimes printed, stored with .00 only where "
        "printed so: here integers)",
        ["sgt1939 page 21 (view 27) only; it replaces the *Autorisations de bâtir* table of the earlier editions. "
         "30 towns, in the printed order (not alphabetical). No total is printed, so there is no check. All "
         "cells read on a native-resolution crop of the page (OCR as draft). Gabès housing is printed "
         "\"860.000\" (OCR \"8(50.000\")."]),
    "communes_terraces": (
        "Concessions sur la voie publique : b) Terrasses et étalages",
        "Pavement concessions: café terraces (chairs and tables of lemonade sellers) and street stalls "
        "(goods of all kinds): number, surface and receipts, per commune.",
        "communes_terraces_<edition>.txt",
        "number: integer as printed; surface: square metres (*mètre carré*), decimals as printed; receipts "
        "(*produits*): francs with centimes. Printed » and *néant* = 0",
        ["Table b) of the *Concessions sur la voie publique* pages, printed on the right-hand page facing table "
         "a) (building permits), **without commune labels**: each value line was matched to the commune labels of "
         "the facing page by OCR line position and by counting lines, and checked against the large communes "
         "(Bizerte, Kairouan, Sfax, Sousse, Tunis). sgt1922–sgt1930 and sgt1935; sgt1936 and sgt1939 print no "
         "such table.",
         "**Image versus OCR.** Every cell was read on native-resolution crops of the page images (half-page "
         "crops at ~0.7 scale, re-cropped at full scale where faint); the OCR was a draft only. The sgt1926 page "
         "is faint: El-Djem stalls 35.696,10, Kef 40.200, Mateur terraces 4.321,40 and Sousse stalls 45.580,79 "
         "were read on the image where the OCR differs.",
         "**What the numbers are.** Communes reported very differently: \"number\" is sometimes the surface "
         "repeated (Bizerte 42.900 / 42.900 m²) or a count of days or tickets; surfaces are sometimes rates "
         "(Nabeul 1928 \"1 20\", 1935 \"0 30\"). Values are stored as printed; the cells where the printed "
         "entry is text (\"droits affermés\", \"divers\", \"variables\", \"concédés à l'adjudicataire\", "
         "\"70 m2 à 1 fr.\" …) are NA with flag `not_applicable` and the text is listed below. sgt1925 Tunis "
         "stalls surface is printed \"965.057\": the printed total (404.045,87) is consistent with 965,057 m² "
         "(the sum is then 1,26 short), not 965.057 m²; stored as printed (965057) and the column check fails. "
         "sgt1925 Médenine stalls number printed \"233 50\" stored 233.50.",
         "Footnotes and remarks printed with the table: sgt1926 (1) Produits affermés; (2) Étalages (par métrés et "
         "par abonnements); (3) Concédés avec les droits de marché; (4) Adjugé avec les droits de marché; (5)–(6) "
         "adjudication / affermés avec les marchés. sgt1927: (1) Droits affermés en 1927; (2) Droits donnés en "
         "adjudication; (3) Affermé avec les droits de marché; (4) Produits affermés avec les droits de marché; "
         "(5) Droits affermés. sgt1928, under the table: *Il y a lieu d'ajouter à ces droits : 505 étalages sur "
         "façades soit 758 m2 25 : 16.476 20* (to be added: 505 façade stalls, 758,25 m², 16.476,20 fr.; not "
         "stored as a row, no commune named). sgt1929: (1)(2) Droits adjugés; (3) Montant total des droits de "
         "concession; (4) Droits affermés avec les droits de marché. sgt1930: (1) Y compris droits colportage; "
         "(2) Droits adjugés; (3)(4) Droits affermés avec ceux du marché; (5) avec droits de marché; (6) Droits "
         "affermés. sgt1935 *Observations* column: Bizerte, parking dues collected by a contractor, 38.627 fr. in "
         "1935; Grombalia (1), dues collected by the market farmer, 19.701 fr. to the commune in 1935; "
         "Maxula-Radès, of which 2.705 fr. collected by tickets; Sidi-bou-Saïd, parking 550 fr.; Sousse, of which "
         "3.803,30 fr. collected by tickets.",
         "Printed totals: sgt1922–sgt1925 every column (TOTAUX), sgt1926 and sgt1927 the stalls receipts only "
         "(TOTAL), none afterwards. sgt1923 matches in all six columns. The sgt1924 mismatches (notably stalls "
         "receipts, 33.356 fr. short) were re-read line by line on the image without finding the cause; the "
         "printed cells are kept and nothing is flagged, but a misassigned or misread line in that edition cannot "
         "be excluded."]),
    "communes_loans_caisse": (
        "Finances municipales : c) Emprunts contractés à la Caisse des Prêts Communaux",
        "Municipal loans from the Caisse des Prêts Communaux: one block per commune, one line per loan, with "
        "terms, annuities due and paid, arrears and capital amortised / outstanding at the end of the year.",
        "communes_loans_<edition>.txt, section `@caisse`",
        "francs with centimes, except `duration_years` (years) and `interest_rate_pct` (percent: \"3 75\" = "
        "3.75, \"7 »\" = 7)",
        ["Two-page spreads (left page: columns 1–6, date to annuity; right page: columns 7–13). `gallica_view` "
         "is the view of the page the cell is printed on. Editions transcribed: **sgt1922, sgt1923, sgt1924 and "
         "sgt1925 only**. sgt1925: the first spread (views 52–53: Tunis, Béja, Bizerte, Ferryville) is not "
         "transcribed because view 52 is a black image in the Gallica scan; only views 54–57 are stored for that "
         "edition. sgt1926–sgt1930 (three to four spreads each, e.g. sgt1930 views 594–601) are not done.",
         "**Image versus OCR.** Every cell was read on native-resolution crops of the spreads (left and right "
         "page stitched at the same height); the OCR was used to find the column positions and lines. In "
         "sgt1922 the annuity column runs into the binding: the centimes are hidden, so those cells are NA, "
         "`illegible` (franc parts listed below); sgt1924 has the same for the first two Tunis loans and the "
         "three Sfax/Sousse 3,75 % loans and Souk-el-Khemis total.",
         "Checks: for every loan line and total line, total payments = payments in the year + earlier payments; "
         "arrears = annuities due − total payments; capital remaining = nominal capital − capital amortised; and "
         "every commune *Totaux* line against its loans. Cross-edition: earlier payments of year N = total "
         "payments of year N−1. Every failure was re-read on a native-resolution crop and the printed value is "
         "kept; most are visible slips in the print (e.g. sgt1922 and sgt1923 print Tunis's total capital "
         "5.600.000 for four loans summing to 9.600.000; sgt1923 and sgt1924 repeat the 1923 payment 137.221,20 "
         "of the Sfax 1909 9-million loan while the total includes 418.708,10; Souk-el-Arba's nominal capital "
         "is printed » in sgt1922–23).",
         "Durations are as printed (\"30 ans\" → 30). The *Capital nominal* of Souk-el-Arba 1921 is printed » in "
         "sgt1922 and sgt1923 (stored 0.00)."]),
    "communes_loans_tunis_bonds": (
        "Finances municipales : b) Emprunts communaux (Commune de Tunis)",
        "Bond loans of the city of Tunis (1891 and 1897): coupons and bonds due, paid in the year and earlier, "
        "lapsed, and outstanding at the close of the year.",
        "communes_loans_<edition>.txt, section `@tunis_bonds`",
        "francs with centimes, except `duration_years` and `interest_rate_pct` (\"3 1/2\" = 3.5)",
        ["Top of the first loan spread (columns 1–7 on the left page, 8–17 on the right). Editions transcribed: "
         "sgt1922, sgt1923, sgt1924 (sgt1925: left page view 52 is a black image, not transcribed; sgt1926–"
         "sgt1930 not done). All cells read on native-resolution crops. In sgt1922 the column *capitaux "
         "(obligations sorties aux tirages)* runs into the binding: centimes hidden, cells NA `illegible` with "
         "the franc part below. Checks: total = year + earlier payments (interest and capital), outstanding = due "
         "− paid − lapsed, the *Totaux* line, and earlier payments(N) = total payments(N−1) across editions."]),
}


def write_more(name, rows):
    cols = COMMON + MORE_DIMS[name] + ["value", "flag"]
    with (OUT / f"{name}.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in cols})
    # validation lists for the notes (written by hand around these generated lists)
    topic = {"communes_building_permits": "permits", "communes_terraces": "terraces",
             "communes_loans_caisse": "loans", "communes_loans_tunis_bonds": "loans",
             "communes_building_values_1939": None}[name]
    L = [f"Rows: {len(rows)}."]
    if topic:
        fails = [x for x in MORE_CHK.fail[topic]
                 if (name != "communes_loans_caisse" or "p." in x)]
        L += [f"Checks ({topic}): {MORE_CHK.n[topic]}; failed: {len(MORE_CHK.fail[topic])}."]
        L += ["  - " + x for x in fails]
        if topic == "loans":
            L += [f"Cross-edition checks (paid before in year N = paid total in year N-1): "
                  f"{MORE_CHK.n['loans_xed']}; differences: {len(MORE_CHK.fail['loans_xed'])}."]
            L += ["  - " + x for x in MORE_CHK.fail["loans_xed"]]
    fl = defaultdict(list)
    for r in rows:
        if r["flag"]:
            fl[r["flag"]].append(r)
    L += [f"Flagged cells: " + (", ".join(f"{k}: {len(v)}" for k, v in sorted(fl.items())) or "none") + "."]
    for k, v in sorted(fl.items()):
        for r in v:
            L.append(f"  - {r['census']} {r['commune']}"
                     + (f" / {r['loan_fr']}" if r.get("loan_fr") else "") + f" {r['measure']}: {k}"
                     + (f" (franc part {r['_hidden']})" if r.get("_hidden") else "")
                     + (f" — printed text: {r['_note']}" if k == "not_applicable" and r.get("_note") else ""))
    eds = [e for e in ORDER if e in {r["census"] for r in rows}]
    H = [f"# {MORE_NOTES[name][0]}", "", f"*{MORE_NOTES[name][1]}*", "",
         "Source: *Statistique générale de la Tunisie*, chapter *Communes*, editions " + ", ".join(eds)
         + ". Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR).", "",
         f"Pages and views of the stored values: {fmt_views(rows)}.", "",
         f"Rebuild: `python3 data-raw/yearbook_other_chapters/extract_communes.py build` (transcriptions "
         f"`../transcribed/{MORE_NOTES[name][2]}`).", "",
         "Printed once per edition (SPEC_ADDENDUM rule 5): `year` is the year the edition reports on; no year is "
         "printed twice, so there is no overlap to compare.", "", "## Columns", ""]
    doc = dict(COLDOC, table_id="transcription section", commune="commune as printed (for loans: the name in the "
               "block heading, e.g. `Tunis` from *Commune de Tunis*; `le Kef` from *Commune du Kef*)",
               commune_heading_fr="block heading exactly as printed", loan_fr="date of the loan as printed "
               "(identifies the loan within the commune)", measure="English code of the printed column",
               measure_fr="column heading as printed (French)", value=MORE_NOTES[name][3],
               flag="empty, `not_applicable` (text printed instead of a number: value NA; the text is listed "
               "below), `illegible` (value NA; for money with hidden centimes the franc part is listed below)",
               year="year of the edition's figures (exercice / calendar year)")
    for c in COMMON + MORE_DIMS[name] + ["value", "flag"]:
        H.append(f"- `{c}`: {doc[c]}")
    H += [""] + [p_ + "\n" for p_ in MORE_NOTES[name][4]] + ["## Validation", ""]
    (OUT / f"{name}.md").write_text("\n".join(H + L) + "\n")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    build_more(write=(cmd == "build"), verbose=(cmd == "check"))
    res = build(write=(cmd == "build"))
    for name, r in res.items():
        print(f"{name}: {len(r['rows'])} rows; checks {r['checks']['n']}, failed {len(r['checks']['fail'])}; "
              f"overlap compared {r['compared']}, diffs {len(r['diffs'])}")
    if cmd == "check":
        for name, r in res.items():
            for f_ in r["checks"]["fail"]:
                print("  FAIL", f_)
            for d in r["diffs"]:
                print("  DIFF", name, d)
