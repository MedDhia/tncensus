#!/usr/bin/env python3
"""Communes chapter (chapter II) of the Statistique générale de la Tunisie,
12 editions 1922-1939: municipal budgets and communal property.

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


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
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
