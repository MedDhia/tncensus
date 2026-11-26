#!/usr/bin/env python3
"""Communes chapter (chapter II) of the Statistique générale de la Tunisie,
12 editions 1922-1939: municipal budgets and communal property (this file), and
loans, building permits and terraces/stalls, slaughter dues, and (section "public services" at the end) the
water service, the Tunis gas works and the electricity tables, written to csv/communes_water_*.csv,
communes_gas_operation.csv, communes_gas_tunis_1937_1939.csv, communes_electricity_*.csv and
csv/communes_validation_services.json (the earlier outputs are unchanged).

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

LOAN_TOPIC = {"caisse": "loans_caisse", "tunis_bonds": "loans_bonds"}
# rule-4 comparison of the 1928 tables printed twice (sgt1928, sgt1929): differences per file, and counts
LOAN_OVERLAP = defaultdict(list)
# loans whose block or date changes between editions, for the cross-edition check only:
# (year, heading, date, ordinal) -> (heading, date, ordinal) of the same loan in year - 1
LOAN_ALIAS = {
    # Le Kram was merged with La Goulette in June 1926; its loan is listed under La Goulette from sgt1930
    (1929, "Commune de la Goulette", "16 mai 1924", 1): ("Commune du Kram", "16 mai 1924", 1),
    (1929, "Commune de la Goulette", "16 mai 1924", 2): ("Commune de la Goulette", "16 mai 1924", 1),
    # sgt1930 prints "8 février 1921" for the "28 février 1921" loan
    (1929, "Commune de Souk-el-Khemis", "8 février 1921", 1): ("Commune de Souk-el-Khemis", "28 février 1921", 1),
}
# sgt1925, first loan spread: the left page (view 52) is a black image. Its loan terms are taken from the
# printings on both sides (sgt1924 and sgt1926) when the two agree (flag reprint_corrected); the Tunis bonds'
# sums due are solved from the right page (due = paid total + lapsed + outstanding; derived_from_totals).
FILL_TERMS = ("dur", "cap_net", "cap_nom", "rate", "annuity")
FILLED = []


def fill_1925(sec, row, head, by_ed):
    if not (sec["ed"] == "sgt1925" and sec["view"] == 52):
        return
    c = row["cells"]
    for col in FILL_TERMS:
        if col not in c or c[col].flag != "absent":
            continue
        found = []
        for ed in ("sgt1924", "sgt1926"):
            for s2 in by_ed[(ed, sec["table"])]:
                n = 0
                for r2 in s2["rows"]:
                    if r2["head"] == head and r2["label"] == row["label"]:
                        n += 1
                        if n == row["ord"]:
                            found.append((ed, r2["cells"][col].raw))
        vals = {v for _, v in found}
        if len(found) == 2 and len({v.removesuffix(".xx").split(".")[0] for v in vals}) == 1:
            vals = {v for v in vals if not v.endswith(".xx")}     # a franc part only: take the full printing
        if len(found) == 2 and len(vals) == 1:
            c[col] = MCell(vals.pop())
            c[col].flag = "reprint_corrected"
            FILLED.append((sec["table"], head, row["label"], col, c[col].raw,
                           "sgt1924 = sgt1926" if found[0][1] == found[1][1] else
                           "; ".join(f"{e} {v}" for e, v in found)))
        else:
            FILLED.append((sec["table"], head, row["label"], col, None,
                           "; ".join(f"{e} {v}" for e, v in found) or "not printed in sgt1924 or sgt1926"))
    if sec["table"] == "tunis_bonds":
        for kind in ("int", "cap"):
            col = f"{kind}_due"
            if c[col].flag != "absent":
                continue
            v = sum(c[f"{kind}_{x}"].value for x in ("paid_total", "lapsed", "outstanding"))
            c[col] = MCell(f"{v:.2f}")
            c[col].flag = "derived_from_totals"
            FILLED.append((sec["table"], head, row["label"], col, f"{v:.2f}", "paid total + lapsed + outstanding"))


def build_more(write=True, verbose=False):
    secs = []
    for f in sorted(TR.glob("communes_*_sgt*.txt")):
        if f.name.startswith(("communes_slaughter_", "communes_water_", "communes_gasop_", "communes_elec_")):
            continue                     # read by build_slaughter / build_services
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
    by_ed = defaultdict(list)
    for s in secs:
        by_ed[(s["ed"], s["table"])].append(s)
    for t, name in (("caisse", "communes_loans_caisse"), ("tunis_bonds", "communes_loans_tunis_bonds")):
        topic = LOAN_TOPIC[t]
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
                    chk_identities(topic, s, r, LOAN_RELS[t], f"{head} / {r['label']}")
                if tots:
                    gl.append((head, data, tots[0]))
                seen = defaultdict(int)
                for r in data:
                    seen[r["label"]] += 1
                    r["ord"] = seen[r["label"]]
                    fill_1925(s, r, head, by_ed)
                    for x in more_rows(s, r, topic, commune_of(head), dict(commune_heading_fr=head,
                                                                           loan_fr=r["label"])):
                        x["_key"] = (x["year"], head, r["label"], r["ord"], x["measure"])
                        rows.append(x)
            chk_col_totals(topic, s, gl)
        # SPEC_ADDENDUM rule 4: a year printed by two editions (1928: sgt1928 and its reprint in sgt1929) is
        # stored from the later edition; every cell of the other printing is compared.
        latest = {}
        for x in rows:
            k = x["_key"]
            if k not in latest or ORDER.index(x["census"]) > ORDER.index(latest[k]["census"]):
                latest[k] = x
        kept, ndup = [], 0
        for x in rows:
            k = x["_key"]
            if latest[k] is x:
                kept.append(x)
                continue
            ndup += 1
            y = latest[k]
            a = x["value"] if x["value"] is not None else (x["_hidden"] and x["_hidden"] + " (franc part)")
            b = y["value"] if y["value"] is not None else (y["_hidden"] and y["_hidden"] + " (franc part)")
            same = a == b or (x["_hidden"] and y["value"] is not None
                              and int(Decimal(y["value"])) == int(Decimal(x["_hidden"])))
            if not same:
                LOAN_OVERLAP[name].append(f"{k[0]} {k[1]} / {k[2]} {k[4]}: {x['census']} {a}, {y['census']} {b}")
        LOAN_OVERLAP[name + "_n"] = ndup
        res[name] = kept
    # cross-edition consistency: earlier payments of year N = total payments of year N-1 (stored rows)
    for name, pairs in (("communes_loans_caisse", [("paid_before", "paid_total")]),
                        ("communes_loans_tunis_bonds", [("interest_paid_before", "interest_paid_total"),
                                                        ("capital_paid_before", "capital_paid_total")])):
        topic = LOAN_TOPIC["caisse" if "caisse" in name else "tunis_bonds"]
        idx = {r["_key"]: r for r in res[name]}
        xed = []
        for (y, head, loan, o, m), r in idx.items():
            for before, total in pairs:
                if m != before:
                    continue
                h0, l0, o0 = LOAN_ALIAS.get((y, head, loan, o), (head, loan, o))
                p = idx.get((y - 1, h0, l0, o0, total))
                if p is None or r["value"] is None or p["value"] is None:
                    continue
                MORE_CHK.n[topic + "_xed"] += 1
                if Decimal(r["value"]) != Decimal(p["value"]):
                    xed.append(f"{commune_of(head)} {loan}{' (' + str(o) + ')' if o > 1 else ''}: {before} {y} "
                               f"({r['census']}) = {r['value']}, {total} {y - 1} ({p['census']}) = {p['value']}")
        MORE_CHK.fail[topic + "_xed"] = xed
    if write:
        for name, rows in res.items():
            write_more(name, rows)
    if verbose:
        for name, rows in res.items():
            print(f"{name}: {len(rows)} rows")
        for t in ("permits", "terraces", "loans_caisse", "loans_caisse_xed", "loans_bonds", "loans_bonds_xed"):
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
         "is the view of the page the cell is printed on. Editions transcribed: sgt1922–sgt1930 (two spreads up "
         "to sgt1925, three in sgt1926–sgt1929, four in sgt1930); the later editions print no loan table. "
         "`year` is the year of the figures: sgt1922 → 1922 … sgt1928 → 1928; **sgt1929 reprints the 1928 "
         "tables** (same type, same headings \"à la fin de 1928\", every cell equal; see Validation) and sgt1930 "
         "gives 1929 (its Caisse headings still read \"à la fin de 1928\" / \"en 1928\", but the bond headings say "
         "1929 and every *antérieurement* cell continues the 1928 totals). There is no 1930 table.",
         "**sgt1925, first spread (views 52–53).** View 52 (left page) is a black image in the Gallica scan, but "
         "view 53 (right page) is legible: its columns 7–13 for Tunis (4 loans and Totaux), Béja (3), Bizerte and "
         "Ferryville were transcribed from the image (view 53 has no dates or headings; each line was matched by "
         "its numbers: earlier payments = 1924 totals of sgt1924, totals = earlier payments of sgt1926, every line "
         "agrees). Columns 2–6 (terms) of view 52 are taken from the printings on both sides when sgt1924 and "
         "sgt1926 print the same value (flag `reprint_corrected`, `gallica_view` 52, listed below); they are left "
         "out where the two differ (Tunis 31 décembre 1921 annuity: 192.304,75 in sgt1924, 384.609,50 in "
         "sgt1926) or where only sgt1926 prints the loan (Béja 23 mai 1924 and 5 juin 1924). The annuities "
         "due at the end of 1925 (column 7) are on view 53 and are stored. The column totals of view 52 are lost.",
         "**Image versus OCR.** Every cell was read on native-resolution crops of the page images (full or "
         "half-page strips; the OCR was used only as a draft and to locate lines). sgt1929: the six pages were read "
         "on the images and compared line by line with the sgt1928 transcription (identical, misprints "
         "included); its annuity column is not cut by the binding, so the 1928 annuities are complete. Hidden "
         "centimes: sgt1922 annuity column (into the binding), sgt1924 a few annuities, sgt1928 the annuities of "
         "view 590 (stored from sgt1929 anyway). Faint digits completed by shape and confirmed by column 4 − "
         "column 12 are listed in the transcription comments (sgt1930 Monastir, Sfax). Illegible: sgt1928/29 Sfax "
         "10 mai 1923 total payments printed \"549.81 90\" (a digit missing; NA) and Souk-el-Khemis Totaux "
         "\"71.34 72\" (total row, not stored).",
         "Checks: for every loan line and total line, total payments = payments in the year + earlier payments; "
         "arrears = annuities due − total payments; capital remaining = nominal capital − capital amortised; and "
         "every commune *Totaux* line against its loans. Cross-edition: earlier payments of year N = total "
         "payments of year N−1 (loans matched by commune heading, date and order within the block; the Kram loan "
         "of 16 mai 1924, listed under La Goulette from sgt1930, and Souk-el-Khemis \"8 février 1921\" in sgt1930 "
         "= \"28 février 1921\" are matched by hand). Every failure was re-read on a native-resolution crop and the "
         "printed value is kept (no cell is flagged for a failed check); most are visible slips in the print "
         "(e.g. sgt1922–23 Tunis capital total 5.600.000 for 9.600.000; sgt1928/29 Hammam-Lif total payments "
         "\"2.435 80\" for 22.435,80, Kairouan \"91.763 26\" for 191.763,26, Béja remaining total "
         "\"11.661788 43\" for 1.661.788,43, Sfax earlier payments \"391627 50\" for 319.627,50). The sgt1930 "
         "*antérieurement* column departs from the 1928 totals for several loans (e.g. Tunis 20 mai 1924: "
         "1.130.416,97 against 1.125.883,64; 27 juillet 1926: 905.976,35 against 675.287,74): read twice on the "
         "image, kept as printed.",
         "Text cells: Médenine 23 mai 1924, capital remaining printed \"(1)\" with footnote *(1) Soldé par "
         "anticipation* (repaid early), sgt1927 and sgt1928/29: NA, `not_applicable`; the loan is no longer "
         "listed in sgt1930. Commune du Kram is listed until sgt1929 (merged with La Goulette in 1926). Two "
         "loans of one commune can share a date (Sfax 22 juin 1909 ×2; La Goulette 16 mai 1924 ×2 in sgt1930): "
         "they are distinct lines, in printed order. Durations are as printed (\"30 ans\" → 30). The *Capital "
         "nominal* of Souk-el-Arba 1921 is printed » in sgt1922 and sgt1923 (stored 0.00)."]),
    "communes_loans_tunis_bonds": (
        "Finances municipales : b) Emprunts communaux (Commune de Tunis)",
        "Bond loans of the city of Tunis (1891 and 1897): coupons and bonds due, paid in the year and earlier, "
        "lapsed, and outstanding at the close of the year.",
        "communes_loans_<edition>.txt, section `@tunis_bonds`",
        "francs with centimes, except `duration_years` and `interest_rate_pct` (\"3 1/2\" = 3.5)",
        ["Top of the first loan spread (columns 1–7 on the left page, 8–17 on the right). Editions transcribed: "
         "sgt1922–sgt1930; `year` as in `communes_loans_caisse.md` (sgt1929 reprints the 1928 table, sgt1930 "
         "gives 1929). All cells read on native-resolution crops. In sgt1922 the column *capitaux (obligations "
         "sorties aux tirages)* runs into the binding: centimes hidden, cells NA `illegible` with the franc part "
         "below. Checks: total = year + earlier payments (interest and capital), outstanding = due − paid − lapsed, "
         "the *Totaux* line, and earlier payments(N) = total payments(N−1) across editions.",
         "**sgt1925** (views 52–53): the left page is a black image; columns 8–17 are transcribed from view 53. "
         "Duration, rate and capital (columns 2–5) are taken from sgt1924 = sgt1926 (`reprint_corrected`), and the "
         "sums due (columns 6–7) are solved as total paid + lapsed + outstanding (`derived_from_totals`): "
         "3.530.712,50 / 1.755.482,50 (1891) and 1.840.378,75 / 696.851,25 (1897).",
         "**sgt1926 prints stale sums due.** Its columns 6–7 (headed \"à la fin de l'exercice 1924\") carry "
         "exactly the 1925 values solved above, so the 1926 identities outstanding = due − paid − lapsed fail by "
         "the 1926 coupons and bonds (listed below); stored as printed. From sgt1927 the column is current again "
         "(headed 1927; sgt1928/29 \"1927\" with 1928 figures; sgt1930 1929)."]),
}

LOAN_RULE = ("Printed once per edition (SPEC_ADDENDUM rule 5): `year` is the year of the figures. The one year "
             "printed twice, 1928 (sgt1928, reprinted unchanged in sgt1929), is stored from the later edition "
             "(sgt1929) and every cell of the sgt1928 printing is compared (rule 4; result under Validation).")


def write_more(name, rows):
    cols = COMMON + MORE_DIMS[name] + ["value", "flag"]
    with (OUT / f"{name}.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in cols})
    # validation lists for the notes (written by hand around these generated lists)
    topic = {"communes_building_permits": "permits", "communes_terraces": "terraces",
             "communes_loans_caisse": "loans_caisse", "communes_loans_tunis_bonds": "loans_bonds",
             "communes_building_values_1939": None}[name]
    L = [f"Rows: {len(rows)}."]
    if topic and topic.startswith("loans"):
        L = [f"Rows: {len(rows)}. Years: " + ", ".join(f"{y} ({e})" for y, e in
                                                         sorted({(r["year"], r["census"]) for r in rows})) + ".", ""]
        L += [f"- Checks (row identities and commune *Totaux*): {MORE_CHK.n[topic]}; passed: "
              f"{MORE_CHK.n[topic] - len(MORE_CHK.fail[topic])}; failed: {len(MORE_CHK.fail[topic])} (printed "
              f"values kept; each re-read on the image)"
              + (f"; skipped (a cell of the column NA): {MORE_CHK.n[topic + '_skipped']}" if
                 MORE_CHK.n[topic + "_skipped"] else "") + "."]
        L += ["  - " + x for x in MORE_CHK.fail[topic]]
        L += [f"- Cross-edition checks (paid before in year N = paid total in year N-1): "
              f"{MORE_CHK.n[topic + '_xed']}; differences: {len(MORE_CHK.fail[topic + '_xed'])}."]
        L += ["  - " + x for x in MORE_CHK.fail[topic + "_xed"]]
        L += [f"- 1928 printed twice (sgt1928 and sgt1929; stored from sgt1929, rule 4): {LOAN_OVERLAP[name + '_n']} "
              f"cells compared; differences: {len(LOAN_OVERLAP[name])}"
              + (" (sgt1928 franc-only annuities compared on the franc part)" if name.endswith("caisse") else "")
              + "."]
        L += ["  - " + x for x in LOAN_OVERLAP[name]]
        tb = "caisse" if name.endswith("caisse") else "tunis_bonds"
        fill = [f_ for f_ in FILLED if f_[0] == tb]
        L += [f"- sgt1925 view 52 (black image), left-page cells: {sum(1 for f_ in fill if f_[4])} filled, "
              f"{sum(1 for f_ in fill if not f_[4])} left out:"]
        L += [f"  - {f_[1]} / {f_[2]} {MORE_MEASURES[tb][f_[3]][0]}: "
              + (f"{f_[4]} ({f_[5]})" if f_[4] else f"not stored ({f_[5]})") for f_ in fill]
    elif topic:
        fails = [x for x in MORE_CHK.fail[topic]
                 if (name != "communes_loans_caisse" or "p." in x)]
        L += [f"Checks ({topic}): {MORE_CHK.n[topic]}; failed: {len(MORE_CHK.fail[topic])}."]
        L += ["  - " + x for x in fails]
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
         (LOAN_RULE if name.startswith("communes_loans") else
          "Printed once per edition (SPEC_ADDENDUM rule 5): `year` is the year the edition reports on; no year is "
          "printed twice, so there is no overlap to compare."), "", "## Columns", ""]
    doc = dict(COLDOC, table_id="transcription section", commune="commune as printed (for loans: the name in the "
               "block heading, e.g. `Tunis` from *Commune de Tunis*; `le Kef` from *Commune du Kef*)",
               commune_heading_fr="block heading exactly as printed", loan_fr="date of the loan as printed "
               "(identifies the loan within the commune)", measure="English code of the printed column",
               measure_fr="column heading as printed (French)", value=MORE_NOTES[name][3],
               flag="empty, `not_applicable` (text printed instead of a number: value NA; the text is listed "
               "below), `illegible` (value NA; for money with hidden centimes the franc part is listed below)"
               + (", `reprint_corrected` (sgt1925 view 52, black image: value taken from sgt1924 = sgt1926), "
                  "`derived_from_totals` (sgt1925 bond sums due, solved from the right page)"
                  if name.startswith("communes_loans") else ""),
               year="year of the edition's figures (exercice / calendar year)")
    for c in COMMON + MORE_DIMS[name] + ["value", "flag"]:
        H.append(f"- `{c}`: {doc[c]}")
    H += [""] + [p_ + "\n" for p_ in MORE_NOTES[name][4]] + ["## Validation", ""]
    (OUT / f"{name}.md").write_text("\n".join(H + L) + "\n")


# =================================================================== slaughter dues
# "Droits d'abatage" (sgt1922-sgt1930): per commune and animal, the tariff per head and the sums collected,
# with the row total. Transcriptions transcribed/communes_slaughter_<edition>.txt (format in their header).

SL_ANIMALS = {"beef": "Bœuf", "veal": "Veau", "sheep": "Mouton et agneaux", "goat": "Chèvre et chevreaux",
              "pig": "Porc", "horse": "Chevaux et mulets", "camel": "Chameau", "other": "Autres",
              "donkey": "Âne"}
SL_MEASURE = {"t": ("tariff_per_head", "Tarif par tête"), "s": ("sums_collected", "Sommes perçues"),
              "total": ("total_collected", "Totaux")}
SL_CHK = Checks()
# Printed cells that a failing row check and a failing column check both point to (kept as printed, flagged).
# The sgt1923 failures are listed in the notes only (no cell is flagged there).
SL_FLAG = {
    ("sgt1922", "Saint-Germain", "sheep_s"): "total_mismatch",  # 6 printed; row total and sheep Totaux exclude it
    ("sgt1924", "Sousse", "goat_s"): "total_mismatch",          # 6.460,55; row and goat Totaux both 10.000 more
    ("sgt1924", "Tunis", "camel_s"): "total_mismatch",          # "11 52"; row and camel Totaux both 1.140,48 more
}


def sl_eq(ed, what, got, printed):
    """One check, counted overall ('slaughter') and per edition."""
    SL_CHK.eq("slaughter", what, got, printed)
    SL_CHK.eq(ed, what, got, printed)


def parse_slaughter(path, ed):
    secs, cur, comment = [], None, []
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
            comment = []
            continue
        if line.startswith("cols:"):
            cur["cols"] = line[5:].split()
            continue
        if line.startswith("callnotes:"):        # numbered notes called from tariff cells "(n) »" (sgt1926 on)
            cur["callnotes"] = dict(x.split("=", 1) for x in line[10:].split(";"))
            continue
        if line.startswith("animals_fr:"):
            cur["animals_fr"] = dict(x.split("=", 1) for x in line[11:].split(";"))
            continue
        label, vals = line.rsplit("|", 1)
        toks = vals.split()
        if len(toks) != len(cur["cols"]):
            raise ValueError(f"{path.name} {label!r}: {len(toks)} values for {len(cur['cols'])} columns")
        cur["rows"].append({"label": label.strip(), "cells": dict(zip(cur["cols"], toks)), "note": comment})
        comment = []
    return secs


def sl_num(tok):
    """(value, flag, text): '.' absent, '?' illegible, 'T:' text tariff, '~' covered by a text across the row,
    'NNN.xx' francs legible and centimes hidden in the binding (value solved in build_slaughter)."""
    if tok.endswith(".xx"):
        return None, "hidden", Decimal(tok[:-3])
    if tok == ".":
        return None, "absent", None
    if tok == "?":
        return None, "illegible", None
    if tok.startswith("T:"):
        return None, "not_applicable", tok[2:].replace("_", " ")
    if tok == "~":
        return None, "not_applicable", None
    if tok.startswith("P:"):            # row total that includes dues not itemised by animal (per kilo)
        return Decimal(tok[2:]), "", None
    return Decimal(tok), "", None


def is_sl_tot(label):
    return re.match(r"(?i)^(a reporter|report|totaux|total)", label) is not None


def build_slaughter(write=True, verbose=False):
    secs = []
    for f in sorted(TR.glob("communes_slaughter_sgt*.txt")):
        secs += parse_slaughter(f, re.search(r"(sgt\d{4})", f.name).group(1))
    rows = []
    by_ed = defaultdict(list)
    for sec in secs:
        by_ed[sec["ed"]].append(sec)
    for ed, ss in by_ed.items():
        carried = None          # running totals carried from the previous page ("A reporter" / "Report")
        for sec in ss:
            sums = [c for c in sec["cols"] if c.endswith("_s") or c == "total"]
            acc = defaultdict(Decimal)
            for r in sec["rows"]:
                lab = r["label"]
                vals = {c: sl_num(t) for c, t in r["cells"].items()}
                hid = [c for c in sums if vals[c][1] == "hidden"]
                if hid and not is_sl_tot(lab):
                    # one sum with its centimes in the binding: solved from the row total, checked on the francs
                    if len(hid) != 1 or hid[0] == "total" or vals["total"][0] is None:
                        raise ValueError(f"{ed} {lab}: cannot solve hidden cells {hid}")
                    c = hid[0]
                    got = vals["total"][0] - sum(vals[k][0] for k in sums
                                                 if k not in ("total", c) and vals[k][0] is not None)
                    francs = vals[c][2]
                    sl_eq(ed, f"{ed} p.{sec['page']} {lab}: {c} solved from Totaux vs francs printed",
                              Decimal(int(got)), francs)
                    vals[c] = (got, "derived_from_totals", None) if int(got) == francs else \
                        (francs, "total_mismatch", None)
                if is_sl_tot(lab):
                    if re.match(r"(?i)^report", lab):
                        for c in sums:
                            if carried is not None and vals[c][0] is not None and c in carried:
                                sl_eq(ed, f"{ed} p.{sec['page']} Report {c} vs previous A reporter",
                                          carried[c], vals[c][0])
                            if vals[c][0] is not None:
                                acc[c] += vals[c][0]
                        continue
                    for c in sums:
                        if vals[c][0] is not None:
                            sl_eq(ed, f"{ed} p.{sec['page']} {lab} {c}", acc[c], vals[c][0])
                        elif vals[c][1] == "hidden":          # column total with centimes in the binding
                            sl_eq(ed, f"{ed} p.{sec['page']} {lab} {c} (francs; centimes hidden)",
                                      Decimal(int(acc[c])), vals[c][2])
                    carried = {c: vals[c][0] for c in sums if vals[c][0] is not None}
                    continue
                for c in sums:
                    if vals[c][0] is not None:
                        acc[c] += vals[c][0]
                ss_ = [vals[c][0] for c in sums if c != "total"]
                itemised = any(v for v in ss_ if v is not None) and not any(
                    t == "~" for t in r["cells"].values()) and not r["cells"]["total"].startswith("P:")
                if itemised and vals["total"][0] is not None and not hid:
                    sl_eq(ed, f"{ed} p.{sec['page']} {lab}: sums vs Totaux",
                              sum(v for v in ss_ if v is not None), vals["total"][0])
                notes = " ".join(r["note"])
                for c, tok in r["cells"].items():
                    v, flag, text = vals[c]
                    flag = SL_FLAG.get((ed, lab, c), flag)
                    if flag == "absent":
                        continue
                    if c == "total":
                        if itemised:
                            continue          # row total of itemised sums: used for the check only
                        animal, kind = "all", "total"
                    else:
                        animal, kind = c.rsplit("_", 1)
                    if text and re.fullmatch(r"\(\d+\)", text) and text in sec.get("callnotes", {}):
                        text = f"{text} » [{sec['callnotes'][text]}]"
                    if tok == "~":
                        text = re.sub(r"^span:\s*", "", next((n for n in r["note"] if n.startswith("span:")), ""))
                    right = c not in sec["cols"][:sec.get("nleft", 8)]
                    afr = sec.get("animals_fr", {}).get(animal, SL_ANIMALS.get(animal, "Tous animaux"))
                    rows.append(dict(census=ed, table_id="slaughter", gallica_ark=sec["ark"],
                                     source_page=sec["page"] + (1 if right else 0),
                                     gallica_view=sec["view2"] if right else sec["view"], year=sec["year"],
                                     commune=lab, animal=animal, animal_fr=afr, measure=SL_MEASURE[kind][0],
                                     measure_fr=SL_MEASURE[kind][1],
                                     value=None if v is None else (format(v.normalize(), "f") if kind == "t"
                                                                    or tok.endswith(".xx") and flag != "derived_from_totals"
                                                                    else f"{v:.2f}"),
                                     text_fr=text or "", flag=flag,
                                     _obs=" ".join(n[4:].strip() for n in r["note"] if n.startswith("obs:"))))
    if verbose:
        print(f"communes_slaughter_dues: {len(rows)} rows; checks {SL_CHK.n['slaughter']}, failed "
              f"{len(SL_CHK.fail['slaughter'])}")
        for f_ in SL_CHK.fail["slaughter"]:
            print("    FAIL", f_)
    if write:
        write_slaughter(rows)
    return rows


SL_COLS = COMMON + ["commune", "animal", "animal_fr", "measure", "measure_fr", "value", "text_fr", "flag"]


def write_slaughter(rows):
    with (OUT / "communes_slaughter_dues.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SL_COLS, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in SL_COLS})
    (OUT / "communes_slaughter_dues.md").write_text(slaughter_notes(rows))


# Views of the table per edition (confirmed on the page images) and what each edition's notes say.
SL_VIEWS = {"sgt1922": "58–59", "sgt1923": "536–541", "sgt1924": "1024–1029", "sgt1925": "58–63",
            "sgt1926": "606–611", "sgt1927": "70–75", "sgt1928": "594–599", "sgt1929": "70–75",
            "sgt1930": "602–607"}
SL_ED = {
    "sgt1922": dict(
        layout="One two-page spread (views 58–59, pp. 34–35) with a single *Totaux* line; heading *d) Droits "
               "d'abatage* with no year (`year` = 1922, the edition year, as for the chapter's other sgt1922 "
               "tables). Column order beef, veal, sheep, goat | pig, horse, **camel, other**. Communes taxing per "
               "kilogram (or not taxing) have a text printed across the whole row instead of figures (*0 fr. 06 "
               "par kilogr. de viande abattue*, *compris avec la commune de La Goulette*, *Droits affermés*): "
               "their 16 cells are stored NA, `not_applicable`, with the text in `text_fr`, and their printed "
               "row total as `animal` = `all`. Bizerte: rate text over beef–goat, pigs itemised (10 fr., 11.340), "
               "rule over the rest. Many tariffs are printed as several rates (\"6, 8\", \"7 70-6 20-5 70\"): "
               "`not_applicable` with the text. Footnotes: El-Djem (1) and Ksour-Essaf (3) *Commune créée le 29 "
               "mars 1922*; Hadjeb-el-Aïoun (2) *Commune créée le 9 mai 1922*.",
        reading="Every line read on native-resolution crops of both pages (left page full width; right page "
                "with the commune names stitched in), the goat column on 1.4× and 5× crops across the binding, "
                "multi-rate tariffs on full-scale crops. Gallica's OCR is very poor on this spread and was not "
                "used for any value. The goat sums run into the binding: francs legible (repeated on the gutter "
                "of the right page), centimes lost. 32 goat sums are solved from the row total "
                "(`derived_from_totals`), each checked against the printed francs.",
        failures="Re-read on crops; printed values kept. (i) Djemmal and Zaghouan goat sums print 680 and 4 003 "
                 "but their row totals give 689,30 and 4.903,50: stored as the printed francs (680, 4003; "
                 "centimes hidden), `total_mismatch`. (ii) The goat *Totaux* 71.647 matches neither reading (the "
                 "row totals and the other printed column totals imply 71.946,88). (iii) Saint-Germain prints a "
                 "lone 6 in the sheep sums with row total »; the sheep *Totaux* also excludes it (sum − 6 = "
                 "printed): stored, `total_mismatch`. (iv) The grand total 1.219.603,74 is the sum of the row "
                 "totals less Téboursouk's 5.358,80 (a line left out of the addition). (v) Camel (−1,00) and "
                 "*Autres* (+0,10) column totals differ slightly; every cell of both columns re-read."),
    "sgt1923": dict(
        layout="Three two-page spreads (views 536–541, pp. 34–39), *A reporter* / *Report* between them; heading "
               "*Droits d'abatage perçus en 1923*. Column order beef, veal, sheep, goat | pig, horse, other, camel. "
               "Communes taxing per kilogram print » in every cell and their rate in *Observations*; their row "
               "total is stored as `animal` = `all` (Ferryville, Gabès, La Goulette, Hammam-Lif, Mahdia, Mateur, "
               "Souk-el-Arba, Souk-el-Khemis, Sousse; and Bizerte, where only pigs are itemised, 6.180 of "
               "118.241,40).",
        reading="All three spreads read on native-resolution crops of both pages stitched at the same height "
                "(0.55–0.85 scale, every line), with separate full-scale strips of the goat column, which runs "
                "into the binding (its last digits repeat on the gutter of the right page) and of the pig tariff "
                "column; Gallica's OCR served as a draft only.",
        failures="Re-read on the image; printed values kept, no cell flagged (e.g. Tunis 8,50 × … 329.970 + … = "
                 "536.346,35 printed 518.346,35; Tebourba 4.540 printed 3.540; La Marsa 9.954,60 printed "
                 "10.854,60)."),
    "sgt1924": dict(
        layout="Three two-page spreads (views 1024–1029, pp. 34–39) with *A reporter* / *Report*; heading *d) "
               "Droits d'abatage* with no year (`year` = 1924, the edition year). Column order as sgt1923 (… pig, "
               "horse, other, camel), with an *Observations* column. Many tariffs printed as text (\"0,06 par kg.\", "
               "\"5 et 4\", \"0,60-1,00\", two rates braced on two lines, written \"a/b\"): `not_applicable` with the "
               "text. Mahdia prints its rate \"0 08\" also in the beef sums column: stored as text (NA), so the row "
               "counts as non-itemised and its total (6.143,68) is kept. Monastir's beef tariff column prints "
               "\"1.048 »\" (stored 1048 as printed). Observations are assigned to the commune they describe where "
               "the text starts a line higher (Ferryville, Tozeur).",
        reading="Every line read on native-resolution crops of each whole spread (both pages stitched, 0.55 "
                "scale); every failing row, every page-total line and the goat column at the binding re-read on "
                "full-scale strips (0.9–3×). The goat sums are legible in full in this edition. Gallica's OCR "
                "used as a draft only (it misreads e.g. Djemmal's sheep sum as 3.162,40; the image shows 3.462,40).",
        failures="Every failing row and total line re-read on full-scale strips; printed values kept. Two cells are "
                 "pinned down by a row check and a column check failing by the same amount and are flagged "
                 "`total_mismatch`: Sousse goat 6.460,55 (row and goat *Totaux* both imply 16.460,55) and Tunis "
                 "camel \"11 52\" (both imply 1.152). Djemmal sheep 3.462,40 agrees with its row total; the first "
                 "*A reporter* (sheep 44.437,96) evidently carries 3.162,40, and the *Report* reprints it as 44.437,90. "
                 "The other failures are small differences (0,02–6,00 francs) or rows whose printed total "
                 "disagrees with its cells (Kairouan 600, Zaghouan 800)."),
    "sgt1925": dict(
        layout="Three two-page spreads (views 58–63, pp. 34–39) with *A reporter* / *Report* and *Observations*; "
               "heading *d) Droits d'abatage* with no year (`year` = 1925). Column order as sgt1923. Text tariffs "
               "(\"0,06 par kg.\", \"6 » les 100 kil.\", \"4 et 5 fr.\") are `not_applicable` with the text. Some "
               "per-kilogram communes print the rate, or its second line \"kil.\", in a sums column (Béja veal, "
               "sheep and goat; Ebba-Ksour and Mahdia beef): stored as text (NA), so these rows count as "
               "non-itemised and their printed totals are kept. Bizerte: pigs itemised (8.232), total stored "
               "as `all` (it includes the per-kilo dues). M'saken's goat sum loses its last centime digit in "
               "the binding (solved from the row total: 1.267,80).",
        reading="Every line read on native-resolution crops of each whole spread (0.55 scale); the goat column "
                "at the binding on 1.6–3× strips; all rows of the third spread, every failing row and every "
                "page-total line re-read on full-scale strips (0.8–0.85×). Gallica's OCR used as a draft only.",
        failures="Every failing row and total line re-read on full-scale strips; printed values kept, no cell "
                 "flagged (no failing row and failing column share the same difference). The camel *A reporter* "
                 "of p. 34 (3.620) is 1.766,80 above its cells and the final camel *Totaux* 1.766,80 below them, "
                 "so the camel column is consistent over the table; the p. 38 *Report* of the grand total "
                 "(635.503,59) differs from the p. 36 *A reporter* (635.305,39); the last page's *Totaux* for "
                 "beef, goat, pig and the total disagree with their cells (pig by 8.310)."),
    "sgt1926": dict(
        layout="Three two-page spreads (views 606–611, pp. 34–39); heading *d) Droits d'abatage* with no year "
               "(`year` = 1926). New layout: the column *Autres* is replaced by *Âne* (`donkey`, before the "
               "camel), and *A reporter* / *Report* / *Totaux* are printed for the row-total column only. Many "
               "tariff cells print a note call \"(n) »\" referring to numbered notes in the *Observations* column "
               "(numbering restarts on each page): `not_applicable`, `text_fr` = the call and the note text in "
               "brackets. Rows whose total includes foreign-meat dues not itemised (*Y compris … viandes "
               "foraines*: Foum-Tatahouine, Grombalia, Nabeul) and rows with no itemised sums keep their row total "
               "as `animal` = `all`. Kairouan prints \"4 20\" in the horse tariff column with the sums » (stored "
               "as a tariff).",
        reading="Every line read on native-resolution crops of each whole spread (0.55 scale); the goat column "
                "at the binding on 1.5–2.5× strips (legible in full); the third spread (faint print), every "
                "itemised row of it and every failing row re-read on full-scale strips. Gallica's OCR not used "
                "for values.",
        failures="Every failing row re-read on full-scale strips of both pages; printed values kept, no cell "
                 "flagged (only the row-total column has page totals, so no failure can be pinned to one cell). "
                 "The final *Totaux* (1.368.192,41) is 19.699,90 above the *Report* plus the p. 39 row totals, "
                 "every one of which was re-read; Téboursouk's goat sum reads 263,45 against a row total that "
                 "implies 2.943,45."),
    "sgt1927": dict(
        layout="Three two-page spreads (views 70–75, pp. 42–47); heading *d) Droits d'abatage* with no year "
               "(`year` = 1927). Layout as sgt1926 (page totals for the row-total column only), but with *Autres* "
               "again (no *Âne*); per-kilogram communes print » throughout with the rate in *Observations* "
               "(Kairouan, Kalaa-Kebira and Maharès itemise sums with the tariff »: stored 0 as printed). New "
               "commune Sbeïtla (all »). Rows whose total includes foreign-meat dues (*Dont … viandes foraines*: "
               "Foum-Tatahouine, Grombalia, Nabeul) or festival dues (Tunis: *Y compris 12.420 fr. fêtes de l'Aïd "
               "El Kebir et Israélite*) keep their row total as `animal` = `all`.",
        reading="Every line read on native-resolution crops of each whole spread (0.55 scale); the goat column "
                "at the binding on 1.4–1.5× strips (legible in full); every failing row and the row-total column "
                "re-read on full-scale strips. Gallica's OCR not used for values.",
        failures="Every failing row re-read on full-scale strips of both pages; printed values kept, no cell "
                 "flagged. Djemmal's row total is printed » although its sums (14.602) are itemised; the p. 44 "
                 "*A reporter* is 280 below the *Report* plus the row totals."),
    "sgt1928": dict(
        layout="Three two-page spreads (views 594–599, pp. 42–47); heading *d) Droits d'abatage* with no year "
               "(`year` = 1928). Layout as sgt1927, but **no page totals at all** (no *A reporter*, *Report* or "
               "*Totaux*), so only the row checks apply. Commune names as printed in this edition (\"Bardo\", "
               "\"Gardimaou\", \"Hammama\", \"Kalâa-Kebira\", \"Kef\", \"Krib\", \"La Marsa\", \"Foum Tatahouine\"). "
               "Ariana prints \"0 70\" in the goat sums column (the tariff repeated; stored 0.70 as printed).",
        reading="View 595 (right page of the first spread) has almost no Gallica OCR text, and the whole table "
                "was read on the images: native-resolution crops of each spread (0.55 scale, 530-pixel bands), "
                "the goat column at the binding on 1.2–1.3× strips (legible in full), the faint third spread "
                "and every failing row re-read on full-scale strips. The left-page OCR was used only to locate "
                "row positions; no value rests on it.",
        failures="Every failing row re-read on full-scale strips of both pages; printed values kept, no cell "
                 "flagged (no column totals are printed, so no failure can be pinned to one cell)."),
    "sgt1929": dict(
        layout="Three two-page spreads (views 70–75, pp. 42–47); heading *d) Droits d'abatage* with no year "
               "(`year` = 1929). Headings in the plural (*Bœufs et vaches*, *Veaux*, …), *Ânes* (`donkey`) in place "
               "of *Autres*, and no page totals, so only the row checks apply. **Not a reprint of sgt1928**: the "
               "commune list and layout are the same but every itemised row differs (e.g. Ariana beef 1.980 vs "
               "1.500, Djemmal total 19.101 vs 17.207, Bizerte 414.643 vs 361.948,70), so both editions are kept "
               "as separate years and no cell comparison applies. Text printed in a sums column (Kalâa-Kebira "
               "goat \"65.899 kil. 500\" and pig \"0 20\", Soliman goat \"99.270\" kilos) is stored as text (NA). "
               "Kairouan's row total prints \"4.91  0\" with type missing: `illegible`. On p. 44 some lines sit a "
               "little off their commune names; values follow the printed order, which matches the names.",
        reading="Every line read on native-resolution crops of each whole spread (0.55 scale, 540-pixel bands); "
                "the goat column is clear of the binding in this volume; every failing row re-read on "
                "full-scale strips of both pages. Gallica's OCR used only to locate row positions.",
        failures="Every failing row re-read on full-scale strips of both pages; printed values kept, no cell "
                 "flagged (no column totals are printed). Menzel-Temime's total (15.219,30) includes dues not "
                 "itemised (Observations: *5.297,50 et 6 kilos viande foraine à 0,30, au total*)."),
    "sgt1930": dict(
        layout="Three two-page spreads (views 602–607, pp. 44–49); heading *d) Droits d'abatage* with no year "
               "(`year` = 1930). Layout as sgt1929 (*Ânes*, no page totals, so only the row checks apply). Rows "
               "whose total includes non-itemised dues keep it as `animal` = `all` (Maxula-Radès *Y compris "
               "viandes foraines*; Menzel-Temime *Y compris 38 fr. 40 …*; Tunis, whose sheep sums column prints "
               "two amounts, \"38.158\" over \"139.045,50\", stored as text, with the note *Les taxes pour abatage "
               "des agneaux et chevaux sont comprises dans la somme de 139.045 fr. 10*). Sfax prints per-kilogram "
               "rates (\"0 30 par kil.\" …) in five tariff columns.",
        reading="Every line read on native-resolution crops of each whole spread (0.55 scale, 540-pixel bands); "
                "the goat column at the binding on 1.4× strips (centimes repeat on the gutter; legible in full); "
                "every failing row re-read on full-scale strips of both pages. Gallica's OCR used only to locate "
                "row positions.",
        failures="Every failing row re-read on full-scale strips of both pages; printed values kept, no cell "
                 "flagged (no column totals are printed). Medjez-el-Bab's goat sum prints \"66 50\" where its row "
                 "total implies 6.050; Foum Tatahouine's total (8.526,25) is close to its cells without the beef "
                 "264."),
}


def slaughter_notes(rows):
    eds = [e for e in ORDER if e in {r["census"] for r in rows}]
    missing = [e for e in SL_VIEWS if e not in eds]
    fl = defaultdict(list)
    for r in rows:
        if r["flag"]:
            fl[r["flag"]].append(r)
    obs = sorted({(r["census"], r["commune"], r["_obs"]) for r in rows if r["_obs"]})
    n_all, f_all = SL_CHK.n["slaughter"], SL_CHK.fail["slaughter"]
    L = ["# Droits d'abatage (slaughter dues)", "",
         "*Slaughter dues collected by each commune: tariff per head and sums collected for each kind of "
         "animal, and the total collected.*", "",
         "Source: *Statistique générale de la Tunisie*, chapter *Communes*, table d) *Droits d'abatage [perçus en "
         "<année>]*, editions " + ", ".join(eds) + ". Source gallica.bnf.fr / Ministère des Affaires étrangères "
         "(NoC-CR).", "",
         f"Pages and views of the stored values: {fmt_views(rows)}.", "",
         "Rebuild: `python3 data-raw/yearbook_other_chapters/extract_communes.py build` (transcriptions "
         "`../transcribed/communes_slaughter_<edition>.txt`).", "",
         f"Rows: {len(rows)} (" + ", ".join(f"{e} {sum(r['census'] == e for r in rows)}" for e in eds) + "). "
         "Printed once per edition (SPEC_ADDENDUM rule 5); `year` = the year in the heading.", "",
         "**Coverage:** " + ", ".join(f"{e} (views {SL_VIEWS[e]})" for e in eds) + " transcribed"
         + (("; not done: " + ", ".join(f"{e} (views {SL_VIEWS[e]})" for e in missing)) if missing else "")
         + ". The table is not printed in sgt1935–sgt1939.", "",
         "## Columns", "",
         "- `census`, `table_id`, `gallica_ark`, `source_page`, `gallica_view`, `year`: as in the other files "
         "(left page: beef to goat; right page: pig, horse, camel/other and the total)",
         "- `commune`: as printed (footnote calls such as \"(1)\" kept)",
         "- `animal`: `beef` (Bœuf), `veal` (Veau), `sheep` (Mouton et agneaux), `goat` (Chèvre [et chevreaux]), "
         "`pig` (Porc), `horse` (Chevaux et mulets), `other` (Autres; to sgt1925), `donkey` (Âne; from sgt1926), "
         "`camel` (Chameau); `all` for a total "
         "stored on its own (see below)",
         "- `animal_fr`: column heading as printed in that edition (French)",
         "- `measure`: `tariff_per_head` (*Tarif par tête*, francs), `sums_collected` (*Sommes perçues*, francs), "
         "`total_collected` (*Totaux*)",
         "- `value`: francs; printed » = 0. Tariffs as printed (\"0 15\" = 0.15). A sum stored as whole francs "
         "without centimes (e.g. `680`) has its centimes hidden in the binding and could not be solved",
         "- `text_fr`: text printed in place of a tariff or across the row (e.g. \"0,10 par kg\", \"1,00-1,20\", "
         "\"0 fr. 06 par kilogr. de viande abattue\")",
         "- `flag`: empty; `not_applicable` (tariff printed as text, or cell covered by a text printed across the "
         "row: value NA, text in `text_fr`); `derived_from_totals` (sum whose centimes are hidden in the binding, "
         "solved as row total − other sums and checked against the printed francs); `total_mismatch` (printed "
         "value kept although the checks show it inconsistent, see the edition's section); `illegible`", "",
         "The row *Totaux* is stored only for communes whose dues are not itemised by animal (all sums » or a "
         "text across the row, and the total printed: dues levied per kilogram, farmed out, or counted with "
         "another commune): `animal` = `all`, `measure` = `total_collected`. For the other communes it equals the "
         "sum of the animals and is used for the check only. The page totals (*A reporter*, *Report*, *Totaux*) "
         "are not stored.", "",
         "Observations column (printed text, translated below): " + "; ".join(
             f"{c} ({e}): *{o}*" for e, c, o in obs) + ". (*par kil. poids vif* = per kg live weight; *par kilo "
         "[de viande abattue]* = per kilogram of meat; *Affermés* = farmed out; *Taxes instituées en 1924* = dues "
         "introduced in 1924.)", "",
         "## Validation", "",
         f"Checks, all editions: {n_all} (each itemised row against its *Totaux*; every column of each page "
         f"against the *A reporter* / *Totaux* line, with the carried *Report*; each sum solved from the row "
         f"total against its printed francs); passed {n_all - len(f_all)}; failed {len(f_all)}. Every failure "
         f"was re-read on a native-resolution crop.", ""]
    for e in eds:
        info, fails = SL_ED.get(e, {}), SL_CHK.fail[e]
        L += [f"### {e} (`{EDITIONS[e]}`, views {SL_VIEWS[e]})", "",
              f"- Rows: {sum(r['census'] == e for r in rows)}. " + info.get("layout", ""),
              "- Image versus OCR: " + info.get("reading", ""),
              f"- Checks: {SL_CHK.n[e]}; passed {SL_CHK.n[e] - len(fails)}; failed {len(fails)}."
              + (" " + info.get("failures", "") if fails else "")]
        L += ["  - " + x for x in fails]
        if info.get("extra"):
            L += ["- " + x for x in info["extra"]]
        L += [""]
    L += ["## Flagged cells", "",
          "- " + (", ".join(f"{k}: {len(v)}" for k, v in sorted(fl.items())) or "none") + "."]
    for k, v in sorted(fl.items()):
        L += [f"  - {r['census']} {r['commune']} {r['animal']} {r['measure']}: {k}"
              + (f" = {r['value']}" if r["value"] not in (None, "") else "")
              + (f" (printed \"{r['text_fr']}\")" if r["text_fr"] else "") for r in v]
    return "\n".join(L) + "\n"


# @@SERVICES BEGIN@@
# =================================================================== public services (water, gas, electricity)
# Service des eaux (pipe lengths, rule 4; water sales, rule 5), Exploitation du gaz à Tunis (sgt1935-sgt1939) and
# the electricity tables (Éclairage). Transcriptions transcribed/communes_water_<edition>.txt,
# communes_gasop_<edition>.txt, communes_elec_<edition>.txt; format in their headers. Written to new files only
# (csv/communes_water*.csv, communes_gas_operation.csv, communes_electricity*.csv, their notes, and
# csv/communes_validation_services.json); the files above are not touched.

SV_CHK = Checks()


def sv_key(name):
    """Locality key for matching printings: accents, punctuation, footnote calls and known renamings removed."""
    import unicodedata
    k = re.sub(r"\s*\(\d\)", "", name)
    k = "".join(c for c in unicodedata.normalize("NFD", k) if unicodedata.category(c) != "Mn").lower()
    k = re.sub(r"[^a-z]", "", k)
    for pre, to in (("sousse", "sousse"), ("mrira", "mrirafouchana"), ("darchabane", "darchabane"),
                    ("mejezelbab", "medjezelbab"), ("gaffour", "gafour")):
        if k.startswith(pre):
            k = to
    return k


def parse_sv(path, ed):
    """Sections '@<table> view=.. [view2=..] page=.. key=value ...' (values: one token, or several for
    years= / printed_years= / left=), optional 'cols:' line, rows 'label | tokens'."""
    secs, cur = [], None
    for line in path.read_text().splitlines():
        line = line.rstrip()
        if not line.strip() or line.startswith("#"):
            continue
        if line.startswith("@"):
            parts = line[1:].split()
            cur = {"table": parts[0], "ed": ed, "ark": EDITIONS[ed], "rows": [], "cols": None}
            for k, v in re.findall(r"(\w+)=(.+?)(?=\s+\w+=|$)", " ".join(parts[1:])):
                cur[k] = v.strip()
            for k in ("view", "view2", "page"):
                if k in cur:
                    cur[k] = int(cur[k])
            if "years" in cur:
                ys = cur["years"]
                cur["years"] = (list(range(int(ys[:4]), int(ys[5:]) + 1)) if re.fullmatch(r"\d{4}-\d{4}", ys)
                                else [int(y) for y in ys.split()])
            secs.append(cur)
            continue
        if line.startswith("cols:"):
            cur["cols"] = line[5:].split()
            continue
        label, vals = line.rsplit("|", 1)
        cur["rows"].append({"label": label.strip(), "toks": vals.split()})
    return secs


class WLen:
    """A printed pipe length. Tokens: 'km.mmm' or 'km.mmm,dd' (km and m sub-columns; ',dd' decimals of a metre),
    '»' = 0, '281.-' = km printed with the metres blank (taken as 281 km), 'p:319.8' = only the first digits are
    legible (rest in the binding; NA), 'T:text' = text instead of a number (NA), '.' = blank cell (not stored)."""
    __slots__ = ("raw", "value", "flag", "text", "prefix")

    def __init__(self, raw):
        self.raw, self.flag, self.text, self.prefix = raw, "", None, None
        if raw in ("»", "néant"):
            self.value = Decimal(0)
        elif raw == ".":
            self.value, self.flag = None, "absent"
        elif raw.startswith("p:"):
            self.value, self.flag, self.prefix = None, "illegible", raw[2:]
        elif raw.startswith("T:"):
            self.value, self.flag, self.text = None, "not_applicable", raw[2:].replace("_", " ")
        elif raw.endswith(".-"):
            self.value = Decimal(raw[:-2]) * 1000
        else:
            m = re.fullmatch(r"(\d+)\.(\d{3})(?:,(\d{2}))?", raw)
            if not m:
                raise ValueError(f"bad length token {raw!r}")
            self.value = Decimal(m.group(1)) * 1000 + Decimal(m.group(2)) + (Decimal(m.group(3)) / 100 if m.group(3)
                                                                             else 0)

    def out(self):
        if self.value is None:
            return None
        return str(int(self.value)) if self.value == int(self.value) else f"{self.value:.2f}"

    def same(self, other):
        """Equal as printed; a partly legible printing is compared on its legible digits."""
        if self.value is not None and other.value is not None:
            return self.value == other.value
        a, b = (self, other) if self.prefix is not None else (other, self)
        if a.prefix is not None and b.value is not None:
            return b.raw.replace(",", "").startswith(a.prefix) or (b.value == 0 and a.prefix == "")
        return self.raw == other.raw


def money_tok(raw):
    """(value or None, flag, text) for a money cell: '»'/'néant' = 0, 'T:text' = text (NA, not_applicable)."""
    if raw in ("»", "néant"):
        return Decimal(0), "", None
    if raw.startswith("T:"):
        return None, "not_applicable", raw[2:].replace("_", " ")
    if raw == "?":
        return None, "illegible", None
    return Decimal(raw), "", None


def sv_secs(prefix):
    secs = []
    for ed in ORDER:
        f = TR / f"communes_{prefix}_{ed}.txt"
        if f.exists():
            secs += parse_sv(f, ed)
    return secs


# (year, locality key) -> edition stored instead of the latest printing, which is an evident misprint: sgt1936 prints
# the 1935 lengths of Armand Colin and Eddekhila one line low (Armand Colin 0.920 repeats Aïn-el-Asker's line,
# Eddekhila 1.303 is Armand Colin's figure; Eddekhila's 2.274 of 1931-1935 and 1936 is lost). sgt1935 prints them
# on their own lines (1.303 / 2.274), consistent with 1931-1934 and with sgt1936's own 1936 column for Eddekhila.
WATER_REPRINT = {(1935, "armandcolin"): "sgt1935", (1935, "eddekhila"): "sgt1935"}


def build_water():
    secs = sv_secs("water")
    printings = defaultdict(dict)        # (year, key) -> ed -> dict(cell, label, sec, view)
    order = {}
    sales = []
    for sec in secs:
        years = sec["years"]
        left = [int(y) for y in sec.get("left", "").split()]
        for r in sec["rows"]:
            toks = r["toks"]
            if len(toks) != len(years) + 1:
                raise ValueError(f"{sec['ed']} water {r['label']!r}: {len(toks)} tokens for {len(years)} years + sales")
            k = sv_key(r["label"])
            order.setdefault(k, len(order))
            for y, t in zip(years, toks[:-1]):
                c = WLen(t)
                if c.flag == "absent":
                    continue
                view = sec["view"] if ("view2" not in sec or y in left) else sec["view2"]
                page = sec["page"] + (0 if ("view2" not in sec or y in left) else 1)
                printings[(y, k)][sec["ed"]] = dict(cell=c, label=r["label"], sec=sec, view=view, page=page)
            v, fl, text = money_tok(toks[-1])
            sales.append(dict(census=sec["ed"], table_id="water", gallica_ark=sec["ark"],
                              source_page=sec["page"] + (1 if "view2" in sec else 0),
                              gallica_view=sec.get("view2", sec["view"]), year=int(sec["sales"]),
                              locality=r["label"], measure="water_sales_receipts",
                              measure_fr=f"Vente d'eau : Recettes en {sec.get('sales_heading', sec['sales'])}",
                              value=None if v is None else f"{v:.2f}", text_fr=text or "", flag=fl))
    rows, compared, diffs = [], 0, []
    for (y, k), by in sorted(printings.items(), key=lambda kv: (kv[0][0], order[kv[0][1]])):
        eds = [e for e in ORDER if e in by]
        latest = eds[-1]
        src, flag = latest, by[latest]["cell"].flag
        if (y, k) in WATER_REPRINT:
            src, flag = WATER_REPRINT[(y, k)], "reprint_corrected"
        if by[latest]["cell"].value is None and by[latest]["cell"].prefix is not None:
            # partly legible in the latest printing: the latest fully legible printing that agrees with the
            # legible digits is stored instead (reprint_corrected)
            ok = [e for e in eds[:-1] if by[e]["cell"].value is not None and by[e]["cell"].same(by[latest]["cell"])]
            if ok:
                src, flag = ok[-1], "reprint_corrected"
        for e in eds:
            if e == latest:
                continue
            compared += 1
            if not by[e]["cell"].same(by[latest]["cell"]):
                diffs.append((y, by[latest]["label"], e, by[e]["cell"].raw, latest, by[latest]["cell"].raw))
        p = by[src]
        rows.append(dict(census=p["sec"]["ed"], table_id="water", gallica_ark=p["sec"]["ark"], source_page=p["page"],
                         gallica_view=p["view"], year=y, locality=by[latest]["label"] if src == latest else p["label"],
                         measure="pipe_length_m", measure_fr="Développement des canalisations (km. m.)",
                         value=p["cell"].out(), text_fr=p["cell"].text or "", flag=flag,
                         _from=(latest, by[latest]["cell"].raw) if src != latest else None,
                         _eds=",".join(eds)))
    return rows, compared, diffs, sales, secs


SV_DIMS = {
    "communes_water_pipes": ["locality", "measure", "measure_fr"],
    "communes_water_sales": ["locality", "measure", "measure_fr"],
    "communes_gas_operation": ["commune", "measure", "measure_fr", "unit"],
    "communes_gas_tunis_1937_1939": ["commune", "lighting", "lighting_fr", "measure", "measure_fr"],
    "communes_electricity_networks": ["locality", "measure", "measure_fr", "unit"],
    "communes_electricity_production": ["centrale", "measure", "measure_fr", "unit"],
    "communes_electricity_distribution": ["region", "measure", "measure_fr", "unit"],
    "communes_electricity_lines": ["centrale", "area", "measure", "measure_fr", "unit"],
}
SV_NOTEXT = {"communes_gas_operation", "communes_gas_tunis_1937_1939"}
SV_VAL = {}     # name -> validation summary for communes_validation_services.json


def sv_write_csv(name, rows):
    cols = COMMON + SV_DIMS[name] + ["value"] + ([] if name in SV_NOTEXT else ["text_fr"]) + ["flag"]
    with (OUT / f"{name}.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in cols})


def sv_header(title_fr, title_en, rows, transcr, rule, coldoc):
    eds = [e for e in ORDER if e in {r["census"] for r in rows}]
    years = sorted({r["year"] for r in rows})
    L = [f"# {title_fr}", "", f"*{title_en}*", "",
         "Source: *Statistique générale de la Tunisie*, chapter *Communes*, editions " + ", ".join(eds)
         + " (stored values). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR).", "",
         f"Pages and views of the stored values: {fmt_views(rows)}.", "",
         "Rebuild: `python3 data-raw/yearbook_other_chapters/extract_communes.py build` (transcriptions "
         f"`../transcribed/{transcr}`). Per-check output: `communes_validation_services.json`.", "",
         f"Rows: {len(rows)}. Years: {', '.join(map(str, years))}.", "", rule, "", "## Columns", ""]
    for c, d in coldoc:
        L.append(f"- `{c}`: {d}")
    return L + [""]


SV_BASECOLS = [
    ("census", "edition the value is taken from (`sgt1922` … `sgt1939`)"),
    ("table_id", "transcription section"),
    ("gallica_ark", "Gallica volume ark (views are numbered within a volume)"),
    ("source_page", "printed page number of the cell"),
    ("gallica_view", "Gallica view (fNNNN) of the cell"),
]


def water_notes(rows, compared, diffs, sales):
    by_ed_sales = defaultdict(int)
    for r in sales:
        by_ed_sales[r["census"]] += 1
    cd = SV_BASECOLS + [
        ("year", "year of the length (column heading; see the misprinted headings below)"),
        ("locality", "locality as printed in the edition the value is taken from"),
        ("measure", "`pipe_length_m`"),
        ("measure_fr", "*Développement des canalisations* (printed in two sub-columns *km.* and *m.*)"),
        ("value", "length of the pipe network in **metres** (printed km × 1000 + printed m; decimals of a metre "
                  "where printed, e.g. 72.819 50 → 72819.50); printed » = 0"),
        ("text_fr", "text printed instead of a number"),
        ("flag", "empty; `reprint_corrected` (value taken from another printing of the same year, see below); "
                 "`not_applicable` (text instead of a number, value NA)"),
    ]
    L = sv_header("Service des eaux : développement des canalisations",
                  "Water service: length of the water-supply pipe network of each locality, ten years per edition "
                  "(two years from sgt1936).", rows, "communes_water_<edition>.txt",
                  "Printed for overlapping year windows (sgt1922: 1913–1922 … sgt1930: 1921–1930; sgt1935: 1926–1935; "
                  "sgt1936: 1935–1936; sgt1939: 1938–1939): each year is taken from the **latest** edition that "
                  "prints it (SPEC_ADDENDUM rule 4; `census` = that edition) and every other printing of the same "
                  "cell is compared below. 1937 is not printed. The water sales of the same tables, one year per "
                  "edition, are in `communes_water_sales.csv`.", cd)
    L += WATER_TEXT
    L += ["## Validation", "",
          "- No total is printed in any of these tables (no column or row totals), so no sum check is possible; "
          "the validation is the comparison of the overlapping printings.",
          f"- Overlapping printings (rule 4): {compared} cell comparisons with the stored (latest) printing; "
          f"{len(diffs)} differences (a partly legible sgt1935 1929 cell counts as equal when its legible digits "
          "match):", "",
          "| year | locality (latest) | other edition | printed there | latest edition | printed there |",
          "|---|---|---|---|---|---|"]
    L += [f"| {d[0]} | {d[1]} | {d[2]} | {d[3]} | {d[4]} | {d[5]} |" for d in diffs]
    fl = [r for r in rows if r["flag"]]
    L += ["", f"- Flagged cells: {len(fl)}."]
    for r in fl:
        L.append(f"  - {r['year']} {r['locality']}: {r['value'] if r['value'] is not None else 'NA'} ({r['flag']}"
                 + (f"; stored from {r['census']}, latest printing {r['_from'][0]} prints `{r['_from'][1]}`"
                    if r.get("_from") else "") + (f"; printed \"{r['text_fr']}\"" if r["text_fr"] else "") + ")")
    return "\n".join(L) + "\n"


WATER_TEXT = [
    "**Editions and layout.** *Service des eaux — Développement des canalisations ; vente d'eau*: sgt1922 p. 38 "
    "(view 62), sgt1923 p. 42 (544), sgt1924 p. 42 (1032), sgt1925 p. 42 (66), sgt1926 p. 50 (614), sgt1927 p. 50 "
    "(78), sgt1928 p. 50 (602); headed *Service des eaux (Régies d'État)* in sgt1929 p. 50 (78), sgt1930 p. 52 "
    "(610), sgt1935 pp. 28–29 (views 48–49, a two-page spread), sgt1936 p. 21 (32) and sgt1939 p. 22 (28). The "
    "locality list grows from 7 (sgt1922–sgt1924) to 51 (sgt1936, sgt1939). sgt1929 and later list only the "
    "state-run (*régie*) services: Nabeul, Ferryville, Mateur, Tozeur, Le Kef, Béja, Tabarka, Kairouan, Téboursouk, "
    "Medjez-el-Bab and Gabès are dropped in sgt1929, and Béja, Tabarka, Gabès … return in sgt1935 with » for the "
    "years before they became régies. Their earlier lengths therefore come from the last edition that printed them "
    "(e.g. Nabeul 1928 from sgt1928).",
    "**Misprinted year headings.** sgt1923 and sgt1924 head the 1923 column \"1913\"; sgt1925 heads 1923 \"1913\" "
    "and 1925 \"1915\". The columns are assigned by position (they continue the sequence, and the figures match the "
    "1923/1925 columns of the later editions). sgt1927 heads its sales column \"Recettes en 1926\" but its amounts "
    "are new (see `communes_water_sales.md`).",
    "**What the lengths are.** Up to 1926 every printing gives cumulative network lengths. sgt1927, sgt1928 and "
    "sgt1929 print small figures for 1927–1929 for the large towns (Bizerte 345 m, Sousse 213 m, Sfax 300 m in "
    "1927; Bizerte 337 m, Sousse 225 m in 1928), apparently the extensions of the year, and » where nothing was "
    "added, while the other localities keep cumulative figures (Hammamet 9.017). sgt1930 and sgt1935 reprint "
    "1927–1929 as cumulative lengths (Bizerte 12.725 / 13.062 / 19.370). The stored values are those of the latest "
    "printing (cumulative); the earlier printings are listed as differences. The Sousse series is printed as "
    "*Sousse* (to sgt1929), *Sousse-Monastir et villages* (sgt1930) and *Sousse, Kairouan et villages du Sahel* "
    "(sgt1935–sgt1939): the overlapping years agree (222.878 … 224.360), so the three labels are matched as one "
    "series; from 1927 the figure drops to 183.837 (a redefined network). Other renamings matched: *M'Rira "
    "Fouchai* (the label is cut by the column rule) = *M'Rira Fouchana (Mohamédia)*; *Dar Chabane* = *Dar Chabane "
    "El-Fehri*; *Mejez el Bab* = *Medjez-el-Bab*; *Gaffour* = *Gafour*; accents ignored (Tébourba, Fériana, "
    "Kélibia, Sbeïtla …).",
    "**Particular cells.** Tunis 1924 is printed \"281\" with the metres blank in all six printings (sgt1924–"
    "sgt1930): stored as 281000. sgt1925 prints Tunis 1925 \"571 107\" (all later printings 287 107) and "
    "Ferryville 1925 \"9 104 50\" (later 9 104). sgt1929 Dar Chabane 1926 is blank (not stored; sgt1935 »). "
    "sgt1935: the 1929 column runs into the binding of the spread (views 48–49) and only its first digits are "
    "legible; its 17 non-zero cells are stored from sgt1930 (`reprint_corrected`), each agreeing with the legible "
    "digits (Tunis \"319 8…\" = 319.826 …). sgt1936, 1935: M'Rira-Fouchana prints *constitué en Syndicat* (formed "
    "into a syndicate; NA, `not_applicable`); sgt1936 prints the 1935 lengths of Armand Colin and Eddekhila one "
    "line low (Armand Colin 0.920 = Aïn-el-Asker's figure repeated, Eddekhila 1.303 = Armand Colin's): these two "
    "are stored from sgt1935 (1.303 and 2.274, `reprint_corrected`). sgt1936 also prints, for 1935, Thala 2.507 "
    "(sgt1935: 8.979,78), Fériana 3.994 (3.557,20), Sbeïtla 2.200 (»), Gafsa 5.001 (»), Sidi-bou-Ali 2.032 "
    "(2.052), and Souk-el-Arba / Souk-el-Khemis 12.862 / 23.187 (sgt1935: 23.187 / 12.862, which itself swaps the "
    "two towns' 1932–1933 figures); these are kept from sgt1936 as rule 4 requires (no printing can be shown "
    "wrong). sgt1939 Sfax prints 1938 \"843 40\" and 1939 \"1.002 30\" (sgt1936: 225.741 km): stored as printed "
    "(843.40 m and 1002.30 m).",
    "**Image versus OCR.** Every cell of every edition was read on native-resolution crops of the page images "
    "(whole table at 0.45–0.6 scale, then the label column stitched to the value columns at 0.6–1.0 scale, the "
    "sgt1935 binding strip of both views at 0.75, and single cells at 1.5–2×). Gallica's OCR was used only as a "
    "draft for sgt1922–sgt1924 (where it agrees with the images); it is scrambled for sgt1925–sgt1930 and was not "
    "used there. No value rests on the OCR alone.",
    "",
]


def sales_notes(sales):
    cd = SV_BASECOLS + [
        ("year", "year of the sales (*Recettes en <année>*)"),
        ("locality", "locality as printed"),
        ("measure", "`water_sales_receipts`"),
        ("measure_fr", "column heading as printed (*Vente d'eau : Recettes en <année>*)"),
        ("value", "francs with centimes; printed » and *néant* = 0.00"),
        ("text_fr", "text printed instead of an amount"),
        ("flag", "empty or `not_applicable` (text instead of an amount: value NA, text in `text_fr`)"),
    ]
    L = sv_header("Service des eaux : vente d'eau (recettes)",
                  "Water service: receipts from the sale of water, per locality, for the edition year.", sales,
                  "communes_water_<edition>.txt", "Printed once per edition (SPEC_ADDENDUM rule 5), as the last "
                  "column of the pipe-length table (`communes_water_pipes.md`); `year` = the year of the receipts. "
                  "No year is printed twice.", cd)
    # sgt1927's column is headed 1926: compare it with sgt1926's 1926 sales
    a = {sv_key(r["locality"]): r["value"] for r in sales if r["census"] == "sgt1926"}
    b = {sv_key(r["locality"]): r["value"] for r in sales if r["census"] == "sgt1927"}
    lab = {sv_key(r["locality"]): r["locality"] for r in sales if r["census"] == "sgt1927"}
    common = [k for k in b if k in a]
    eq = [k for k in common if a[k] == b[k]]
    SV_VAL["sales_1927_vs_1926"] = dict(compared=len(common), equal=eq)
    L += ["**Headings.** sgt1922–sgt1935 *Recettes en <année>*, sgt1936 and sgt1939 *Recette en <année>*. sgt1927 "
          "heads the column \"Recettes en 1926\", but of the "
          f"{len(common)} localities also in sgt1926 only {len(eq)} have the same amount as sgt1926's 1926 sales "
          f"({', '.join(f'{lab[k]} {a[k]}' for k in eq) or 'none'}; Tunis 3.478.497,30 against 2.762.081,90), so the column is taken as the "
          "1927 receipts (`year` = 1927, heading kept in `measure_fr`). Gabès prints 19.379,80 in both sgt1927 "
          "and sgt1928 (kept as printed).", "",
          "**Texts.** sgt1936: El-Aroussa, Le Goubellat and Testour, *Les régies ne fonctionnent qu'à partir du 1er "
          "janvier 1937* (the services only operate from 1 January 1937; printed across the three lines); Gafour, "
          "*Régie à partir du 1-1-37*; sgt1939: Aïn-Kerma \"(1)\", footnote *Ne fonctionne pas encore* (not working "
          "yet). These are NA, `not_applicable`. *Néant* (sgt1935, sgt1936) is stored as 0.00. In sgt1936 the value "
          "lines sit half a line off their names; they were assigned in order (51 lines for 51 names).", "",
          "**Image versus OCR.** Every amount read on native-resolution crops (see `communes_water_pipes.md`); "
          "OCR not relied on.", "",
          "## Validation", "",
          "- No totals are printed, so there is no sum check; each year is printed once, so there is no overlap "
          "comparison (the sgt1927 heading was checked against sgt1926 as above).",
          f"- Rows per edition: " + ", ".join(f"{e} {sum(r['census'] == e for r in sales)}" for e in ORDER
                                              if any(r['census'] == e for r in sales)) + "."]
    fl = [r for r in sales if r["flag"]]
    L += [f"- Flagged cells: {len(fl)}."] + [f"  - {r['census']} {r['locality']}: {r['flag']} (\"{r['text_fr']}\")"
                                             for r in fl]
    return "\n".join(L) + "\n"


GASOP = {
    "emission": ("gas_emitted_m3", "Émission totale de l'année en mètres cubes", "m3"),
    "subscribers": ("subscribers", "Nombre d'abonnés au 31 décembre", "count"),
    "cons_public": ("consumed_m3_public_lighting", "Nombre de mètres cubes consommés : Éclairage public", "m3"),
    "cons_private_roads": ("consumed_m3_private_roads_lighting",
                           "Nombre de mètres cubes consommés : Éclairage — voies privées", "m3"),
    "cons_ordinary": ("consumed_m3_private_ordinary_tariff",
                      "Nombre de mètres cubes consommés : Particuliers (tarif ordinaire)", "m3"),
    "cons_reduced": ("consumed_m3_administration_reduced_tariff",
                     "Nombre de mètres cubes consommés : Administration et divers (tarif réduit)", "m3"),
    "len_all": ("mains_length_m_all_diameters", "Longueur totale des canalisations en service au 31 décembre", "m"),
}
for _d in (500, 400, 350, 300, 250, 200, 175, 150, 100, 90, 80, 70, 60, 50):
    GASOP[f"len_{_d}"] = (f"mains_length_m_diameter_{_d}mm",
                          f"Longueur totale des canalisations en service au 31 décembre : diamètre {_d} m/m", "m")


def build_gasop():
    secs = [s for s in sv_secs("gasop") if s["table"] == "gasop"]
    printings = defaultdict(dict)
    for sec in secs:
        years = [int(y) for y in sec["years"]] if isinstance(sec["years"], list) else sec["years"]
        for r in sec["rows"]:
            for y, t in zip(years, r["toks"]):
                printings[(y, r["label"])][sec["ed"]] = dict(v=Decimal(t), raw=t, sec=sec)
        for y in years:
            col = {r["label"]: Decimal(r["toks"][years.index(y)]) for r in sec["rows"]}
            cons = [k for k in col if k.startswith("cons_") and k != "cons_TOTAL"]
            SV_CHK.eq("gasop", f"{sec['ed']} p.{sec['page']} {y}: m3 consumed by use vs TOTAL",
                      sum(col[k] for k in cons), col["cons_TOTAL"])
            lens = [k for k in col if re.fullmatch(r"len_\d+", k)]
            if lens:
                SV_CHK.eq("gasop", f"{sec['ed']} p.{sec['page']} {y}: lengths by diameter vs TOTAL",
                          sum(col[k] for k in lens), col["len_TOTAL"])
    rows, compared, diffs = [], 0, []
    items = list(GASOP)
    for (y, item), by in sorted(printings.items(), key=lambda kv: (kv[0][0], (items + ["cons_TOTAL", "len_TOTAL"])
                                                                   .index(kv[0][1]))):
        eds = [e for e in ORDER if e in by]
        latest = eds[-1]
        for e in eds[:-1]:
            compared += 1
            if by[e]["v"] != by[latest]["v"]:
                diffs.append((y, item, e, by[e]["raw"], latest, by[latest]["raw"]))
        if item.endswith("TOTAL"):
            continue
        p = by[latest]
        code, fr, unit = GASOP[item]
        rows.append(dict(census=latest, table_id="gasop", gallica_ark=p["sec"]["ark"], source_page=p["sec"]["page"],
                         gallica_view=p["sec"]["view"], year=y, commune="Tunis", measure=code, measure_fr=fr,
                         unit=unit, value=str(int(p["v"])), flag=""))
    return rows, compared, diffs, printings


def gas_tunis_printings():
    """communes_gas_tunis cells (existing transcriptions, section @gas) plus sgt1939's @gastunis printing."""
    out = defaultdict(dict)       # (year, col) -> ed -> Cell
    for ed in ORDER:
        for sec in parse(ed):
            if sec["table"] == "gas":
                for r in sec["rows"]:
                    for c, cell in zip(sec["cols"], r["cells"]):
                        out[(int(r["label"]), c)][ed] = cell
    for sec in sv_secs("gasop"):
        if sec["table"] == "gastunis":
            for r in sec["rows"]:
                for c, t in zip(sec["cols"], r["toks"]):
                    out[(int(r["label"]), c)][sec["ed"]] = Cell(t)
    return out


def build_gas_1937(gt):
    """sgt1939's GAZ — Consommations (Ville de Tunis), years not in communes_gas_tunis (1937-1939)."""
    sec = [s for s in sv_secs("gasop") if s["table"] == "gastunis"][0]
    check_rows = []
    rows, compared, same = [], 0, 0
    for r in sec["rows"]:
        y = int(r["label"])
        d = {c: Cell(t) for c, t in zip(sec["cols"], r["toks"])}
        for m in ("cons", "rec"):
            SV_CHK.eq("gas_1937", f"sgt1939 p.23 {y} {m}: public + subscribers vs total",
                      d[f"{m}_public"].value + d[f"{m}_private"].value, d[f"{m}_total"].value)
        if y <= 1936:
            for c in sec["cols"]:
                others = {e: x for e, x in gt[(y, c)].items() if e != "sgt1939"}
                for e, x in others.items():
                    compared += 1
                    same += x.value == d[c].value
                    if x.value != d[c].value:
                        check_rows.append((y, c, e, x.raw, d[c].raw))
            continue
        for c in sec["cols"]:
            m, l = c.split("_")
            if l == "total":
                continue
            fr = {"public": "Éclairage public", "private": "Abonnés"}[l]
            cell = d[c]
            rows.append(dict(census="sgt1939", table_id="gastunis", gallica_ark=sec["ark"], source_page=sec["page"],
                             gallica_view=sec["view"], year=y, commune="Tunis", lighting=GAS[l][0], lighting_fr=fr,
                             measure=GAS_M[m][0], measure_fr=GAS_M[m][1],
                             value=str(int(cell.value)) if m == "cons" else cell.money(), flag=""))
    return rows, compared, same, check_rows


def gas_cross(printings, gt):
    """Exploitation du gaz vs GAZ — Consommations, same edition and year: public + private roads = public
    lighting; ordinary + reduced tariff = private lighting / subscribers; TOTAL = total general."""
    out = []
    for (y, item), by in printings.items():
        if item != "cons_TOTAL":
            continue
        for e in by:
            def g(it):
                x = printings.get((y, it), {}).get(e)
                return x["v"] if x else Decimal(0)
            for what, got, col in (("public + private roads", g("cons_public") + g("cons_private_roads"), "cons_public"),
                                   ("ordinary + reduced tariff", g("cons_ordinary") + g("cons_reduced"), "cons_private"),
                                   ("TOTAL", g("cons_TOTAL"), "cons_total")):
                c = gt.get((y, col), {}).get(e)
                if c is None:
                    continue
                SV_CHK.eq("gas_cross", f"{e} {y}: Exploitation {what} vs GAZ Consommations {col}", got, c.value)
                out.append((e, y, col))
    return out


def gasop_notes(rows, compared, diffs):
    cd = SV_BASECOLS + [
        ("year", "year of the figures (column heading)"),
        ("commune", "`Tunis`"),
        ("measure", "English code of the printed line (`gas_emitted_m3`, `subscribers`, `consumed_m3_*`, "
                    "`mains_length_m_diameter_<d>mm`, `mains_length_m_all_diameters`)"),
        ("measure_fr", "line label as printed (French)"),
        ("unit", "`m3` (mètres cubes), `m` (mètres) or `count`"),
        ("value", "integer, in the unit as printed"),
        ("flag", "empty (no cell is flagged)"),
    ]
    L = sv_header("Exploitation du gaz à Tunis", "Operation of the Tunis gas works: gas emitted, subscribers, "
                  "gas consumed by use, and length of the mains in service by diameter.", rows,
                  "communes_gasop_<edition>.txt", "Printed for two-year windows (sgt1935: 1934–1935; sgt1936: "
                  "1935–1936; sgt1939: 1938–1939): each year is taken from the latest edition printing it (rule 4); "
                  "1935, printed twice, is stored from sgt1936 and the sgt1935 printing compared. 1937 is not printed.",
                  cd)
    L += ["**Tables.** sgt1935 p. 31 (view 51) *Exploitation du gaz à Tunis (1934-1935)*; sgt1936 p. 23 (view 34) "
          "and sgt1939 p. 23 (view 29) *Exploitation du gaz à Tunis*. Lines: *Émission totale de l'année en mètres "
          "cubes*; *Nombre d'abonnés au 31 décembre*; *Nombre de mètres cubes consommés*: *Éclairage public*, *— "
          "voies privées* (lighting of private roads; not printed in sgt1939), *Particuliers (tarif ordinaire)*, "
          "*Administration et divers (tarif réduit)*, *Total* (not stored, used for the check); *Longueur totale des "
          "canalisations en service au 31 décembre* by diameter 500 … 50 m/m with a *Total* (sgt1935, sgt1936; the "
          "total is not stored), or as a single figure (sgt1939, stored as `mains_length_m_all_diameters`).", "",
          "**Image versus OCR.** Every cell was read on native-resolution crops (0.5–1.0 scale); the OCR (which "
          "agrees except for the sgt1936 \"50\" line, read \"90\") was a draft only.", "",
          "**Overlap with `communes_gas_tunis`.** The gas consumption series (*Gaz : consommation (ville de Tunis)*) "
          "gives the same gas in two columns: its *Éclairage public* consumption equals *Éclairage public* + *voies "
          "privées* here, its *Éclairage privé* / *Abonnés* consumption equals *Particuliers* + *Administration*, "
          "and its total equals the *Total* here. These identities were checked for every year both tables print in "
          "the same edition (sgt1935: 1934, 1935; sgt1936: 1935, 1936; sgt1939: 1938, 1939; result below). Only "
          "the breakdown (voies privées; ordinary / reduced tariff), the gas emitted, the subscribers and the mains "
          "are new; receipts are only in `communes_gas_tunis`.", "",
          "**sgt1939 also prints the consumption series** (*GAZ — Consommations (Ville de Tunis)*, 1935–1939, on "
          "the same page 23, view 29, headed *Éclairage public / Abonnés / Total général*), which "
          "`communes_gas_tunis.md` says is absent. Its 1935–1936 cells equal the sgt1936 printing stored there "
          "(compared below); 1937–1939 are stored in `communes_gas_tunis_1937_1939.csv`, because "
          "`communes_gas_tunis.csv` is kept unchanged. Under rule 4 the 1935–1936 rows of `communes_gas_tunis.csv` "
          "would carry `census` = sgt1939 (same values).", "",
          "## Validation", ""]
    L += [f"- Printed totals (m3 consumed by use vs *Total*; lengths by diameter vs *Total*): {SV_CHK.n['gasop']}; "
          f"passed {SV_CHK.n['gasop'] - len(SV_CHK.fail['gasop'])}; failed {len(SV_CHK.fail['gasop'])}:"]
    L += [f"  - {x}" for x in SV_CHK.fail["gasop"]]
    L += ["  Both failures were re-read on a native-resolution crop and are as printed (no cell flagged): the "
          "1936 consumption *Total* 5.548.049 is 10.000 below the sum of its lines, which the consumption series "
          "prints as 5.558.049 (in sgt1936 and sgt1939); the 1936 lengths sum to 149.960 against the printed "
          "150.007.",
          f"- Cross-table identities with the consumption series, same edition and year: {SV_CHK.n['gas_cross']}; "
          f"passed {SV_CHK.n['gas_cross'] - len(SV_CHK.fail['gas_cross'])}; failed "
          f"{len(SV_CHK.fail['gas_cross'])}:"] + [f"  - {x}" for x in SV_CHK.fail["gas_cross"]]
    L += [f"- Overlapping printings (1935: sgt1935 and sgt1936): {compared} cells compared (totals included); "
          f"{len(diffs)} differences." + ("" if not diffs else " " + "; ".join(map(str, diffs))),
          "- Note: in 1935 the 70 mm and 60 mm lines read 5.080 / 33.403 in both printings, while 1934 reads "
          "30.996 / 5.080; kept as printed.", "- Flagged cells: none."]
    return "\n".join(L) + "\n"


def gas1937_notes(rows, compared, same, cr):
    cd = SV_BASECOLS + [("year", "year"), ("commune", "`Tunis`"),
                        ("lighting", "`public_lighting` (*Éclairage public*) or `private_lighting` (*Abonnés*: "
                                     "subscribers, the *Éclairage privé* of the earlier editions)"),
                        ("lighting_fr", "column heading as printed in sgt1939"),
                        ("measure", "`consumption_m3` or `receipts`"), ("measure_fr", "column heading (French)"),
                        ("value", "consumption in cubic metres (integer); receipts in francs with centimes "
                                  "(printed » in the centimes = .00)"),
                        ("flag", "empty (no cell is flagged)")]
    L = sv_header("GAZ — Consommations (Ville de Tunis), 1937–1939",
                  "Gas consumption and receipts, city of Tunis, public lighting and subscribers: the years "
                  "1937–1939, printed only in sgt1939.", rows, "communes_gasop_sgt1939.txt, section `@gastunis`",
                  "Continuation of `communes_gas_tunis.csv` (same columns and codes), kept in a separate file so "
                  "that file stays unchanged. sgt1939 prints 1935–1939; only 1937–1939 are stored here.", cd)
    L += ["sgt1939 p. 23, view 29, lower table. Read on a native-resolution crop (0.6 scale); OCR agrees. The "
          "TOTAL GÉNÉRAL columns are not stored (row checks).", "", "## Validation", "",
          f"- Row checks (public + subscribers vs total, consumption and receipts, 1935–1939): "
          f"{SV_CHK.n['gas_1937']}; failed {len(SV_CHK.fail['gas_1937'])}:"]
    L += [f"  - {x}" for x in SV_CHK.fail["gas_1937"]]
    L += ["  The 1936 receipts failure is the same misprint as in sgt1936 (7.835.770,64 printed 4.835.770,64), see "
          "`communes_gas_tunis.md`.",
          f"- Overlap with `communes_gas_tunis` (1935–1936, sgt1939 against every earlier printing): {compared} "
          f"cells compared, {same} equal" + ("." if not cr else "; differences: " + "; ".join(map(str, cr))),
          "- Cross-check with *Exploitation du gaz à Tunis* (same page): 1938 and 1939 public, subscriber and "
          "total consumption agree (see `communes_gas_operation.md`).", "- Flagged cells: none."]
    return "\n".join(L) + "\n"


# ----------------------------------------------------------------- electricity

EL_MEAS = {
    # sgt1929-sgt1930 table a) Électricité (networks): code, French heading, unit
    "len": ("network_length_m", "Longueur des canalisations", "m"),
    "pw_l": ("installed_power_lighting_kw", "Puissance des installations en service au 31 décembre : Éclairage", "kW"),
    "pw_o": ("installed_power_other_kw", "Puissance des installations en service au 31 décembre : Autres usages", "kW"),
    "pw_t": ("installed_power_total_kw", "Puissance des installations : TOTAL", "kW"),
    "sub_l": ("subscribers_lighting", "Nombre d'abonnés : Éclairage", "count"),
    "sub_o": ("subscribers_other", "Nombre d'abonnés : Autres usages", "count"),
    "sub_ht": ("subscribers_high_voltage", "Nombre d'abonnés : Haute tension", "count"),
    "sub_t": ("subscribers_total", "Nombre d'abonnés : TOTAL", "count"),
    "kwh_pl": ("kwh_private_lighting", "Nombre de kilowattheures consommés : Particuliers, Éclairage", "kWh"),
    "kwh_pf": ("kwh_private_power", "Nombre de kilowattheures consommés : Particuliers, Force", "kWh"),
    "kwh_vl": ("kwh_town_lighting", "Nombre de kilowattheures consommés : Ville, Éclairage", "kWh"),
    "kwh_vf": ("kwh_town_power", "Nombre de kilowattheures consommés : Ville, Force", "kWh"),
    "kwh_t": ("kwh_total", "Kilowattheures consommés : TOTAL", "kWh"),
    "rec_pl": ("receipts_private_lighting", "Produits bruts : Particuliers, Éclairage", "francs"),
    "rec_pf": ("receipts_private_power", "Produits bruts : Particuliers, Force", "francs"),
    "rec_vl": ("receipts_town_lighting", "Produits bruts : Ville, Éclairage", "francs"),
    "rec_vf": ("receipts_town_power", "Produits bruts : Ville, Force", "francs"),
    "rec_t": ("receipts_total", "Produits bruts : TOTAL", "francs"),
    "redev": ("royalty_to_town_and_control_fee", "Redevance à la ville et droit de contrôle", "francs"),
    "droits": ("underground_occupation_dues", "Droits d'occupation des sous-sols", "francs"),
    # production
    "st_kw": ("steam_turbines_installed_kw", "Production thermique, turbines à vapeur : puissance des usines installée", "kW"),
    "st_kwh": ("steam_turbines_energy_kwh", "Production thermique, turbines à vapeur : énergie fournie aux réseaux "
                                            "(aux bornes de l'usine)", "kWh"),
    "ic_kw": ("combustion_engines_installed_kw", "Production thermique, moteurs à combustion interne : puissance "
                                                "installée des usines", "kW"),
    "ic_kwh": ("combustion_engines_energy_kwh", "Production thermique, moteurs à combustion interne : énergie fournie "
                                                "aux réseaux (aux bornes de l'usine)", "kWh"),
    "tot_kw": ("total_installed_kw", "Production totale aux bornes de sortie de l'usine : puissance installée totale",
               "kW"),
    "max_kw": ("maximum_power_produced_kw", "Production totale : puissance maximum produite", "kW"),
    "tot_kwh": ("total_energy_produced_kwh", "Production totale : énergie produite totale", "kWh"),
    # distribution, Tableau I
    "ht_traction": ("kwh_high_voltage_traction", "Énergie livrée, haute tension : Traction", "kWh"),
    "ht_other": ("kwh_high_voltage_other", "Énergie livrée, haute tension : Autres usages", "kWh"),
    "ht_public": ("kwh_high_voltage_public_services", "Énergie livrée, haute tension : Services publics", "kWh"),
    "ht_t": ("kwh_high_voltage_total", "Énergie livrée, haute tension : TOTAL", "kWh"),
    "bt_dom": ("kwh_low_voltage_light_domestic", "Énergie livrée, basse tension : Lumière et usages domestiques", "kWh"),
    "bt_force": ("kwh_low_voltage_power", "Énergie livrée, basse tension : Force", "kWh"),
    "bt_publight": ("kwh_low_voltage_public_lighting", "Énergie livrée, basse tension : Éclairage publics", "kWh"),
    "bt_public": ("kwh_low_voltage_public_services", "Énergie livrée, basse tension : Services publics", "kWh"),
    "bt_t": ("kwh_low_voltage_total", "Énergie livrée, basse tension : TOTAL", "kWh"),
    "total": ("kwh_total_high_and_low_voltage", "TOTAL général haute et basse tension", "kWh"),
    # distribution, Tableau II
    "len_ht": ("line_length_high_voltage_m", "Longueurs des lignes : haute tension", "m"),
    "len_bt": ("line_length_low_voltage_m", "Longueurs des lignes : basse tension", "m"),
}
# row totals (not stored; used for the checks): column -> its parts
EL_ROW = {
    "elec": [("pw_t", ["pw_l", "pw_o"]), ("sub_t", ["sub_l", "sub_o"]),
             ("kwh_t", ["kwh_pl", "kwh_pf", "kwh_vl", "kwh_vf"]), ("rec_t", ["rec_pl", "rec_pf", "rec_vl", "rec_vf"])],
    "prod": [("tot_kw", ["st_kw", "ic_kw"]), ("tot_kwh", ["st_kwh", "ic_kwh"])],
    "distr1": [("sub_t", ["sub_l", "sub_o", "sub_ht"]), ("ht_t", ["ht_traction", "ht_other", "ht_public"]),
               ("bt_t", ["bt_dom", "bt_force", "bt_publight", "bt_public"]), ("total", ["ht_t", "bt_t"])],
    "distr2": [],
}
EL_TOTALCOLS = {"pw_t", "sub_t", "kwh_t", "rec_t", "tot_kw", "tot_kwh", "ht_t", "bt_t", "total"}
EL_FILES = {"elec": "communes_electricity_networks", "prod": "communes_electricity_production",
            "distr1": "communes_electricity_distribution", "distr2": "communes_electricity_lines"}
# printed cells flagged total_mismatch: the row check fails and the cell is evidently on the wrong line (see notes)
TRAM = "Compagnie des Tramways de Tunis (Banlieue de Tunis et dans un rayon de 60 km. autour de Tunis)"
EL_FLAG = {("sgt1930", "Oued-Sahil", "pw_l"): "total_mismatch", ("sgt1930", "Bizerte", "pw_l"): "total_mismatch",
           # a row check and a column check fail by the same amount
           ("sgt1935", TRAM, "sub_o"): "total_mismatch",            # 745; both imply 475
           ("sgt1936", TRAM, "bt_force"): "total_mismatch",         # 8.374.526; both imply 837.452,6
           ("sgt1939", "Ferryville (Centrale de Ferryville) Alternatif", "bt_public"): "total_mismatch"}  # 27.984,6 / 27.894,6


class ECell:
    __slots__ = ("raw", "value", "flag", "text", "prefix")

    def __init__(self, raw):
        self.raw, self.flag, self.text, self.prefix = raw, "", None, None
        if raw in ("»", "néant"):
            self.value = Decimal(0)
        elif raw == ".":
            self.value, self.flag = None, "absent"
        elif raw.startswith("T:"):
            self.value, self.flag, self.text = None, "not_applicable", raw[2:].replace("_", " ")
        elif raw.startswith("S:"):          # two figures printed in one cell
            self.value = sum(Decimal(x) for x in raw[2:].split("+"))
            self.text = " / ".join(raw[2:].split("+"))
        elif raw.startswith("p:"):
            self.value, self.prefix, self.flag = None, raw[2:].replace(".", ""), "partial"
        else:
            self.value = Decimal(raw)


def el_rows(sec):
    out = []
    n = len(sec["cols"])
    for r in sec["rows"]:
        toks = r["toks"]
        if r["label"] == "GRANDTOTAL":
            toks = toks + ["."] * (n - len(toks))
        if len(toks) < n and toks and toks[-1].startswith("T:"):
            toks = toks + [toks[-1]] * (n - len(toks))
        if len(toks) != n:
            raise ValueError(f"{sec['ed']} {sec['table']} {r['label']!r}: {len(toks)} tokens for {n} columns")
        out.append((r["label"], {c: ECell(t) for c, t in zip(sec["cols"], toks)}))
    return out


def el_fmt(v, unit):
    if v is None:
        return None
    if unit == "francs":
        return f"{v:.2f}"
    return str(int(v)) if v == int(v) else format(v.normalize(), "f")


def build_electricity():
    secs = [s for s in sv_secs("elec") if s["table"] in EL_FILES]
    res = defaultdict(list)
    derived = []
    for sec in secs:
        t, ed = sec["table"], sec["ed"]
        rows = el_rows(sec)
        excl = sec.get("ht_excl_traction") == "1"
        rels = [(a, [x for x in b if not (excl and x == "ht_traction")]) for a, b in EL_ROW[t]]
        data = [(lab, c) for lab, c in rows if lab not in ("Totaux", "GRANDTOTAL")]
        tot = dict(rows).get("Totaux")
        # solve partly legible cells from their row identity, then check the legible digits
        for lab, c in rows:
            for col, cell in c.items():
                if cell.prefix is None:
                    continue
                tgt, parts = next((a, b) for a, b in rels if col in b)
                v = c[tgt].value - sum(c[x].value for x in parts if x != col)
                ok = str(v).replace(".", "").startswith(cell.prefix)
                SV_CHK.n[f"elec_{t}"] += 1
                if not ok:
                    SV_CHK.fail[f"elec_{t}"].append(f"{ed} {lab} {col}: solved {v}, legible digits {cell.prefix}")
                cell.value, cell.flag = v, "derived_from_totals"
                derived.append((ed, t, lab, col, v, cell.prefix))
        for lab, c in rows:
            if lab == "GRANDTOTAL":
                continue
            for tgt, parts in rels:
                if c[tgt].value is None or any(c[x].value is None for x in parts):
                    continue
                SV_CHK.eq(f"elec_{t}", f"{ed} p.{sec['page']} {lab}: {' + '.join(parts)} vs {tgt}",
                          sum(c[x].value for x in parts), c[tgt].value)
        if tot:
            for col in sec["cols"]:
                xs = [c[col] for _, c in data if c[col].flag != "absent"]
                if tot[col].value is None or any(x.value is None for x in xs if x.flag != "not_applicable"):
                    continue
                SV_CHK.eq(f"elec_{t}", f"{ed} p.{sec['page']} column {col} vs Totaux",
                          sum(x.value for x in xs if x.value is not None), tot[col].value)
        gt = dict(rows).get("GRANDTOTAL")
        if gt:
            g = Decimal(sec["rows"][-1]["toks"][0])
            SV_CHK.eq(f"elec_{t}", f"{ed} p.{sec['page']} Totaux HT + BT vs grand total",
                      tot["len_ht"].value + tot["len_bt"].value, g)
        left = int(sec.get("left", 99))
        for lab, c in data:
            for j, (col, cell) in enumerate(c.items()):
                if col in EL_TOTALCOLS or cell.flag == "absent":
                    continue
                code, fr, unit = EL_MEAS[col]
                right = "view2" in sec and j >= left
                flag = cell.flag if cell.flag in ("not_applicable", "derived_from_totals") else ""
                flag = EL_FLAG.get((ed, lab, col), flag)
                rec = dict(census=ed, table_id=t, gallica_ark=sec["ark"],
                           source_page=sec["page"] + (1 if right else 0),
                           gallica_view=sec["view2"] if right else sec["view"], year=int(sec["year"]),
                           measure=code, measure_fr=fr, unit=unit, value=el_fmt(cell.value, unit),
                           text_fr=cell.text or "", flag=flag)
                if t == "distr2":
                    cen, area = lab.split(" :: ")
                    rec.update(centrale=cen, area=area)
                elif t == "prod":
                    rec.update(centrale=lab)
                elif t == "distr1":
                    rec.update(region=lab)
                else:
                    rec.update(locality=lab)
                res[EL_FILES[t]].append(rec)
    return res, derived


EL_DIMS = {
    "communes_electricity_networks": ["locality", "measure", "measure_fr", "unit"],
    "communes_electricity_production": ["centrale", "measure", "measure_fr", "unit"],
    "communes_electricity_distribution": ["region", "measure", "measure_fr", "unit"],
    "communes_electricity_lines": ["centrale", "area", "measure", "measure_fr", "unit"],
}
EL_TOPIC = {"communes_electricity_networks": "elec_elec", "communes_electricity_production": "elec_prod",
            "communes_electricity_distribution": "elec_distr1", "communes_electricity_lines": "elec_distr2"}
EL_TITLE = {
    "communes_electricity_networks": (
        "a) Électricité : longueur des canalisations ; puissance des installations ; abonnés ; consommation ; produits",
        "Electricity by locality (sgt1929, sgt1930): length of the network, installed power at 31 December, "
        "subscribers, kilowatt-hours consumed and gross receipts."),
    "communes_electricity_production": (
        "Production d'électricité", "Electricity production by power station (sgt1935, sgt1936, sgt1939): "
        "installed power and energy of steam turbines and internal-combustion engines, maximum power produced."),
    "communes_electricity_distribution": (
        "Distribution d'électricité, Tableau I : abonnés et énergie livrée par les réseaux à la consommation",
        "Electricity distribution by distributor or region (sgt1935, sgt1936, sgt1939): subscribers and "
        "energy delivered at high and low voltage by use."),
    "communes_electricity_lines": (
        "Distribution d'électricité, Tableau II : longueurs des lignes",
        "Length of the high- and low-voltage lines by power station and town or region electrified (sgt1935, "
        "sgt1936, sgt1939)."),
}
EL_TEXT = {
    "communes_electricity_networks": [
        "**Tables.** sgt1929 pp. 52–53 (views 80–81) and sgt1930 pp. 54–55 (views 612–613), each a two-page spread "
        "headed *a) Électricité : longueur des canalisations ; puissance des installations ; abonnés ; consommation ; "
        "produits* in the *Éclairage* pages. Left page: locality, length (mètres), power of the installations in service "
        "at 31 December (kW: *Éclairage*, *Autres usages*, *TOTAL*), subscribers (*Éclairage*, *Autres usages*, "
        "*TOTAL*), kWh consumed by private customers (*Particuliers*: *Éclairage*, *Force*). Right page: kWh consumed "
        "by the town (*Ville*: *Éclairage*, *Force*), kWh *TOTAL*, gross receipts (*Produits bruts*: Particuliers "
        "Éclairage / Force, Ville Éclairage / Force, *TOTAL*, francs), *Redevance à la ville et droit de contrôle* "
        "and *Droits d'occupation des sous-sols* (francs). The row totals (power, subscribers, kWh, receipts) are "
        "not stored; they are used for the row checks. No column totals are printed. `year` = the year of the "
        "power heading (*au 31 décembre 1929 / 1930*), taken for the whole table.",
        "**Units.** Length in metres as printed (\"160.700\" = 160 700 m; sgt1929 prints some short lengths as "
        "\"0.850\" = 850 m, as the table header says *mètres*); power in kW as printed (Mateur 1929 \"236.92\" "
        "kept as 236.92 kW; Sfax 1929 prints 1.384.490 / 1.002.600 / 2.387.090 and Gabès 221.260 / 5.500 / "
        "226.760, apparently watts, kept as printed); kWh with one decimal where printed; francs with centimes.",
        "**Text cells.** In sgt1929 several localities print a text across the consumption and receipts columns "
        "instead of figures: La Goulette *Région Bac compris dans Djebel-Djelloud*, Ste-Monique and Archevêché "
        "*Compris dans Sidi-bou-Saïd*, La Soukra and Cherguia *Compris dans Montplaisir*, Forgemol *Compris dans Le "
        "Bardo*, Mégrine *Compris dans Djebel-Djelloud* (consumption counted with that locality); Salammbo's town "
        "lighting *Compris dans Carthage* and Dermech's *id.*: each covered cell is NA, `not_applicable`, with the "
        "text in `text_fr`. Hammam-Lif and Mornag are braced in the kWh and receipts columns (sgt1929): those cells "
        "are stored under `Hammam-Lif et Mornag`. sgt1930 braces Ste-Monique, Sidi-bou-Saïd, Archevêché and La "
        "Soukra, Chergula in all columns (one row each, joined label).",
        "**sgt1930 layout faults.** (1) The kWh *Force* column of view 612 curves into the binding and its lower "
        "lines sit up to half a line above their names; they were assigned in order and every line was confirmed by "
        "kWh TOTAL − the three other kWh cells (St-Germain \"4 8\" = 4,8 kWh). (2) In the power columns, from "
        "Beni-Khalled the TOTAL column runs one line late (Beni-Khalled 12 + » printed 13 = Beni-Khiar's total; "
        "Fondouk-Djedid 2 + » printed 12 …), and the lighting cells of Oued-Sahil and Bizerte carry 550 and "
        "221.260 (Bizerte 550 + 400 = 950, its printed total; 221.260 is Gabès's 1929 figure, a line of type left "
        "standing). Printed values are stored; Oued-Sahil and Bizerte lighting power are flagged `total_mismatch`.",
        "**Image versus OCR.** Every cell was read on native-resolution crops (each page in three bands at 0.62–0.7 "
        "scale, the label column stitched to the value columns; small-type kWh cells at 2–5×). The OCR was used as a "
        "draft and to locate lines. Doubtful reading: sgt1929 Tunis kWh *Particuliers Force* \"3.467,748 8\" in "
        "condensed type (stored 3467748.8); a reading 3.167.748,8 would reduce Tunis's kWh row failure from "
        "300.230,8 to 230,8, but the glyph matches the 4 of \"748\".",
    ],
    "communes_electricity_production": [
        "**Tables.** *Production d'électricité*: sgt1935 p. 32 (view 52; view 53, given in the scope as part of the "
        "table, is a blank page), sgt1936 p. 24 (view 35), sgt1939 p. 24 (view 30). Rows: power stations (*Centrale "
        "de La Goulette, de Ferryville, de Bizerte, de Béja, de Souk-el-Arba, de Sousse, de Sfax, de Gabès, de "
        "Gafsa*). Columns: *Production thermique d'énergie électrique* by steam turbines (*Turbines à vapeur*: "
        "installed power of the plants, kW; energy supplied to the networks at the plant terminals, kWh) and by "
        "internal-combustion engines (*Moteurs à combustion interne*: same two columns), and *Production totale "
        "d'énergie électrique aux bornes de sortie de l'usine* (installed power, kW; maximum power produced, kW; "
        "energy produced, kWh). The total installed power and total energy are row totals (not stored); the "
        "column-total line is not stored either. Only La Goulette has steam turbines.",
        "**Year.** No year is printed in the headings; `year` is the edition year (1935, 1936, 1939), as for the "
        "other once-per-edition tables of these editions. Printed once per edition (rule 5), so there is no overlap.",
        "**Image versus OCR.** Every cell read on native-resolution crops (0.45–0.6 scale). The OCR was a draft; "
        "it misreads sgt1936 46.914.360 as 40.914.300 and 1.692.517 as 1.092.517.",
    ],
    "communes_electricity_distribution": [
        "**Tables.** *Distribution d'électricité, Tableau I* (sgt1935 pp. 34–35, views 54–55) and the same table "
        "without a number in sgt1936 (pp. 26–27, views 37–38) and sgt1939 (pp. 26–27, views 32–33); each a two-page "
        "spread. Rows: distributors or regions (*Compagnie des Tramways de Tunis (Banlieue de Tunis et dans un rayon "
        "de 60 km. autour de Tunis)*, *Compagnie du Gaz de Tunis (à Tunis)*, … *Gafsa*). Columns: number of "
        "subscribers (*Éclairage*, *Autres usages*, *Haute tension*, *TOTAL*), and energy delivered by the networks to "
        "consumers (*Énergie livrée par les réseaux à la consommation*, kWh): high voltage (*Traction*, *Autres "
        "usages*, *Services publics*, *TOTAL*), low voltage (*Lumière et usages domestiques*, *Force*, *Éclairage(s) "
        "publics*, *Services publics*, *TOTAL*), and *TOTAL général haute et basse tension*. The TOTAL columns and the "
        "column-total line are not stored (checks). `year` = edition year (no year printed). Braced names "
        "(*Ferryville (Fourniture C. T. T.)* / *(Centrale de Ferryville)*, *Bizerte - La Pêcherie* / *Région de "
        "Bizerte*) share one line of figures and are stored under the joined label; sgt1939 instead gives "
        "Ferryville *Continu* and *Alternatif* lines and a *Région de Ferryville* line.",
        "**HT total without traction in sgt1939.** In sgt1939 the HT TOTAL is *Autres usages* + *Services publics* "
        "only, and the *TOTAL général* = HT TOTAL + BT TOTAL, so the traction energy (8.432.247 kWh, Tramways) is in "
        "neither (sgt1935 and sgt1936 include it). The row checks follow the printed definition of each edition.",
        "**Cells in the binding.** sgt1935 Tramways HT *Autres usages* is printed \"5.900.714\" with the decimal "
        "digit in the binding; sgt1939's whole HT *Autres usages* column runs into the binding, with only its leading "
        "digits legible. These cells are solved from the row identity (HT total − the other HT cells) and checked "
        "against the legible digits (all agree; listed below), flag `derived_from_totals`.",
        "**Other particular cells.** sgt1936 Bizerte BT *Services publics* prints two figures one above the other "
        "(106.605 and 39.060, for the two braced names): stored as their sum, 145665, with the printed text in "
        "`text_fr` (the BT total 1.050.746 includes both). sgt1936 Téboursouk's BT services publics, BT total and "
        "total général are printed on the line below its name. sgt1936 Tramways subscribers print 10.185 high-voltage "
        "subscribers (total 20.370; the column total 10.338 confirms it).",
        "**Image versus OCR.** Every cell read on native-resolution crops (each page in two bands at 0.48–0.62 "
        "scale; the binding strips of both views stitched; faint cells checked against the row totals). OCR was a "
        "draft (it misreads e.g. sgt1936 Goulette subscribers 1.496 as 1.406).",
    ],
    "communes_electricity_lines": [
        "**Tables.** *Distribution d'électricité, Tableau II* (sgt1935 p. 36, view 56), and the same table without "
        "a number in sgt1936 (p. 25, view 36) and sgt1939 (p. 25, view 31): length of the lines (*Longueurs des "
        "lignes*, metres) at high voltage (*Haute tension*) and low voltage (*Basse tension*), by power station "
        "(*Centrales*, braced over the towns it serves) and town or region electrified (*Villes ou régions "
        "électrifiées*). Column totals (and in sgt1936 a grand total HT + BT, 2.168.093) are not stored. `year` = "
        "edition year (no year printed). sgt1935 braces *Bizerte-Pêcherie* and *Région de Bizerte* into one line "
        "(joined label); sgt1936 and sgt1939 give them separately.",
        "**Image versus OCR.** Every cell read on native-resolution crops (0.45–0.5 scale); OCR was a draft only "
        "(it is poor on sgt1939).",
    ],
}


def el_notes(name, rows, derived):
    dims = EL_DIMS[name]
    doc = dict(SV_BASECOLS)
    doc.update(year="year of the figures (see below)", locality="locality as printed",
               centrale="power station as printed", region="distributor or region as printed (braced names joined "
                                                                "with ' + ')",
               area="town or region electrified, as printed", measure="English code of the printed column",
               measure_fr="column heading as printed (French), with its group heading", unit="unit of `value`: "
               "`m`, `kW`, `kWh`, `count` or `francs`",
               value="number in `unit`, as printed (decimals kept; francs with centimes); printed » = 0",
               text_fr="text printed instead of a number (or the two figures of a double cell)",
               flag="empty; `not_applicable` (text instead of a number: value NA); `derived_from_totals` (cell "
                    "partly in the binding, solved from the row identity and checked against its legible digits); "
                    "`total_mismatch` (printed value kept; a row check and a column check, or the evident line "
                    "fault described below, show it inconsistent)")
    L = sv_header(EL_TITLE[name][0], EL_TITLE[name][1], rows, "communes_elec_<edition>.txt",
                  "Printed once per edition (SPEC_ADDENDUM rule 5); no year is printed twice, so there is no overlap "
                  "comparison.", [(c, doc[c]) for c in ["census", "table_id", "gallica_ark", "source_page",
                                                        "gallica_view", "year"] + dims + ["value", "text_fr", "flag"]])
    for p_ in EL_TEXT[name]:
        L += [p_, ""]
    tp = EL_TOPIC[name]
    L += ["## Validation", "",
          f"- Checks (row totals, column-total line, solved cells against legible digits): {SV_CHK.n[tp]}; passed "
          f"{SV_CHK.n[tp] - len(SV_CHK.fail[tp])}; failed {len(SV_CHK.fail[tp])}. Every failure was re-read on a "
          "native-resolution crop; printed values are kept."]
    L += [f"  - {x}" for x in SV_CHK.fail[tp]]
    L += EL_FAIL_TEXT.get(name, [])
    dv = [d for d in derived if EL_FILES[d[1]] == name]
    if dv:
        L += [f"- Cells solved from the row identity ({len(dv)}, `derived_from_totals` except the Totaux line, "
              "which is not stored):"]
        L += [f"  - {d[0]} {d[2]} {d[3]}: {d[4]} (legible digits {d[5]})" for d in dv]
    fl = [r for r in rows if r["flag"] and r["flag"] != "not_applicable"]
    na = [r for r in rows if r["flag"] == "not_applicable"]
    L += [f"- Flagged cells: not_applicable {len(na)} (text cells, see above)"
          + "".join(f"; {k} {sum(r['flag'] == k for r in fl)}" for k in sorted({r['flag'] for r in fl})) + "."]
    L += [f"  - {r['census']} {r.get('locality') or r.get('region') or r.get('centrale')} {r['measure']} = "
          f"{r['value']} ({r['flag']})" for r in fl]
    return "\n".join(L) + "\n"


EL_FAIL_TEXT = {
    "communes_electricity_networks": [
        "  The failures are in the print: e.g. sgt1929 Mateur receipts TOTAL 22.562,52 (= its town-lighting cell) for "
        "292.562,52, Sousse kWh TOTAL 323.925 for 723.925, Sfax 527.120,9 for 1.437.120,9; sgt1930 the power-column "
        "line fault described above (Beni-Khalled to Bizerte). Except for the two sgt1930 lighting cells, no stored "
        "cell can be singled out (only row totals are printed), so none is flagged.",
    ],
    "communes_electricity_production": [
        "  sgt1939: the printed column total of the energy produced, 68.715.636 kWh, is 2.000.000 below the sum of "
        "the stations (70.715.636) and below the sum of its own line (57.966.290 + 12.749.346); it is a total line "
        "(not stored), so no stored cell is flagged.",
    ],
    "communes_electricity_distribution": [
        "  Pinned cells (`total_mismatch`): sgt1935 Tramways subscribers *Autres usages* 745 (row and column checks "
        "both imply 475); sgt1936 Tramways BT *Force* 8.374.526 (both imply 837.452,6); sgt1939 Ferryville "
        "*Alternatif* BT *Services publics* 27.984,6 (both imply 27.894,6). **sgt1939 BT totals:** in 12 of the 18 lines "
        "(besides Ferryville Alternatif) the BT TOTAL exceeds the sum of the four printed BT columns (Tramways by 1.496.466, Sousse 138.234, Sfax "
        "142.678 …; the column total by 1.891.193), while each BT column agrees with its own column total, and HT "
        "TOTAL + BT TOTAL = TOTAL général on every line. The BT TOTAL therefore includes some low-voltage energy "
        "not shown in any printed column; no cell is wrong and none is flagged.",
    ],
}


def build_services(write=True, verbose=False):
    rows, compared, diffs, sales, _ = build_water()
    SV_VAL["communes_water_pipes"] = dict(rows=len(rows), checks=0, overlap_compared=compared,
                                          overlap_diffs=[list(map(str, d)) for d in diffs])
    SV_VAL["communes_water_sales"] = dict(rows=len(sales), checks=0)
    res = {"communes_water_pipes": rows, "communes_water_sales": sales}
    notes = {"communes_water_pipes": water_notes(rows, compared, diffs, sales),
             "communes_water_sales": sales_notes(sales)}
    grows, gcomp, gdiffs, gprint = build_gasop()
    gt = gas_tunis_printings()
    g7, g7c, g7s, g7cr = build_gas_1937(gt)
    gas_cross(gprint, gt)
    res["communes_gas_operation"] = grows
    res["communes_gas_tunis_1937_1939"] = g7
    notes["communes_gas_operation"] = gasop_notes(grows, gcomp, gdiffs)
    notes["communes_gas_tunis_1937_1939"] = gas1937_notes(g7, g7c, g7s, g7cr)
    SV_VAL["communes_gas_operation"] = dict(rows=len(grows), checks=SV_CHK.n["gasop"], failed=SV_CHK.fail["gasop"],
                                            cross_checks=SV_CHK.n["gas_cross"], cross_failed=SV_CHK.fail["gas_cross"],
                                            overlap_compared=gcomp, overlap_diffs=[list(map(str, d)) for d in gdiffs])
    SV_VAL["communes_gas_tunis_1937_1939"] = dict(rows=len(g7), checks=SV_CHK.n["gas_1937"],
                                                  failed=SV_CHK.fail["gas_1937"], overlap_compared=g7c,
                                                  overlap_equal=g7s)
    eres, derived = build_electricity()
    for name, rs in eres.items():
        res[name] = rs
        notes[name] = el_notes(name, rs, derived)
        tp = EL_TOPIC[name]
        SV_VAL[name] = dict(rows=len(rs), checks=SV_CHK.n[tp], failed=SV_CHK.fail[tp],
                            solved_cells=[list(map(str, d)) for d in derived if EL_FILES[d[1]] == name])
    if write:
        for name, rs in res.items():
            sv_write_csv(name, rs)
            (OUT / f"{name}.md").write_text(notes[name])
        (OUT / "communes_validation_services.json").write_text(
            json.dumps(SV_VAL, indent=1, ensure_ascii=False) + "\n")
    if verbose:
        for name, rs in res.items():
            print(f"{name}: {len(rs)} rows")
        print(f"  water overlap: {compared} compared, {len(diffs)} differences")
    return res


# ----------------------------------------------------------------- electricity, sgt1922-sgt1928
# The earlier forms of table a) Électricité (lower half of the water and gas pages), in
# transcribed/communes_elec_<edition>.txt: sections '@elec22' (sgt1922-sgt1927: power in hectowatts, kWh and receipts
# split Particuliers / Éclairage public or Ville) -> csv/communes_electricity_1922_1927.csv, and '@elec28' (sgt1928:
# the column set of sgt1929-sgt1930, codes of EL_MEAS) -> csv/communes_electricity_1928.csv; their notes and
# csv/communes_validation_elec_1922_1928.json. Nothing above reads these sections (build_electricity keeps only the
# tables of EL_FILES). Tokens as in the elec sections, plus 'p:NNN' on a TOTAL cell = only the leading digits NNN
# legible (checked against the sum of the parts on those digits), '?' = illegible and 'W:value:word' = a figure
# printed with a word beneath it (value stored, the word in text_fr).

EE_MEAS = {
    "len": ("network_length_m", "Longueur des canalisations", "m"),
    "pw_l": ("installed_power_lighting_hw", "Puissance des installations en service au 31 décembre : Éclairage",
             "hW"),
    "pw_o": ("installed_power_other_hw", "Puissance des installations en service au 31 décembre : Autres usages",
             "hW"),
    "pw_t": ("installed_power_total_hw", "Puissance des installations en service au 31 décembre : TOTAL", "hW"),
    "sub_l": ("subscribers_lighting", "Nombre d'abonnés : Éclairage", "count"),
    "sub_o": ("subscribers_other", "Nombre d'abonnés : Autres usages", "count"),
    "sub_t": ("subscribers_total", "Nombre d'abonnés : TOTAL", "count"),
    "kwh_p": ("kwh_private", "Nombre de kilowats-heures consommés : Particuliers", "kWh"),
    "kwh_pub": ("kwh_public_lighting", "Nombre de kilowats-heures consommés : Éclairage public", "kWh"),
    "kwh_t": ("kwh_total", "Nombre de kilowats-heures consommés : TOTAL", "kWh"),
    "rec_p": ("receipts_private", "Produits bruts : Particuliers", "francs"),
    "rec_v": ("receipts_town", "Produits bruts : Ville", "francs"),
    "rec_t": ("receipts_total", "Produits bruts : TOTAL", "francs"),
    "redev": ("royalty_to_town_and_control_fee", "Redevance à la ville et droit de contrôle", "francs"),
    "droits": ("underground_occupation_dues", "Droit d'occupation du sous-sol", "francs"),
}
# section -> (output file, column codes, row identities, TOTAL columns)
EE_LAYOUT = {
    "elec22": ("communes_electricity_1922_1927", EE_MEAS,
               [("pw_t", ["pw_l", "pw_o"]), ("sub_t", ["sub_l", "sub_o"]), ("kwh_t", ["kwh_p", "kwh_pub"]),
                ("rec_t", ["rec_p", "rec_v"])], {"pw_t", "sub_t", "kwh_t", "rec_t"}),
    # sgt1928 heads the kWh group "Kilowatheures consommés" (EL_MEAS codes, French headings as printed)
    "elec28": ("communes_electricity_1928",
               {k: (c, fr.replace("Nombre de kilowattheures consommés", "Kilowatheures consommés")
                    .replace("Kilowattheures consommés", "Kilowatheures consommés"), u)
                for k, (c, fr, u) in EL_MEAS.items()},
               EL_ROW["elec"], {"pw_t", "sub_t", "kwh_t", "rec_t"}),
}
EE_TOTALROW = "Totaux"
EE_CHK = Checks()                      # topic = '<output file>|<edition>'
EE_FLAG = {}                           # (edition, locality, column) -> flag for a printed cell kept as printed
EE_PREFIX = defaultdict(list)          # file -> (edition, locality, column, legible digits, sum of the parts, ok)
EE_DERIVED = defaultdict(list)         # file -> (edition, locality, column, value, legible digits)


def ee_cell(raw):
    if raw == "?":
        c = ECell(".")
        c.raw, c.flag = raw, "illegible"
        return c
    if raw.startswith("p:"):
        c = ECell(".")
        c.raw, c.prefix, c.flag = raw, raw[2:].replace(".", ""), "partial"
        return c
    if raw.startswith("W:"):
        _, v, word = raw.split(":", 2)
        c = ECell(v)
        c.raw, c.text = raw, word.replace("_", " ")
        return c
    return ECell(raw)


def ee_digits(v):
    return str(v).replace(".", "").lstrip("0") or "0"


def ee_section(sec, out):
    ed, cols = sec["ed"], sec["cols"]
    name, meas, rows_rel, totalcols = EE_LAYOUT[sec["table"]]
    tp = f"{name}|{ed}"
    n, left = len(cols), int(sec.get("left", 99))
    page = {c: sec["page"] + (1 if j >= left else 0) for j, c in enumerate(cols)}
    rows = []
    for r in sec["rows"]:
        toks = r["toks"]
        if len(toks) < n and toks and toks[-1].startswith("T:"):
            toks = toks + [toks[-1]] * (n - len(toks))
        if len(toks) != n:
            raise ValueError(f"{ed} {sec['table']} {r['label']!r}: {len(toks)} tokens for {n} columns")
        rows.append((r["label"], {c: ee_cell(t) for c, t in zip(cols, toks)}))
    rels = [(a, b) for a, b in rows_rel if a in cols and all(x in cols for x in b)]
    # partly legible cells: a part cell is solved from its row identity (derived_from_totals) and checked on its
    # legible digits; a TOTAL cell is checked on its legible digits against the sum of its parts
    for lab, c in rows:
        for col, cell in c.items():
            if cell.prefix is None:
                continue
            if col in totalcols:
                parts = dict(rels)[col]
                if any(c[x].value is None for x in parts):
                    continue
                v = sum(c[x].value for x in parts)
                ok = ee_digits(v).startswith(cell.prefix)
                EE_CHK.n[tp] += 1
                EE_PREFIX[name].append((ed, lab, col, cell.prefix, v, ok))
                if not ok:
                    EE_CHK.fail[tp].append(f"{ed} p.{page[col]} {lab}: {' + '.join(parts)} = {v} vs legible "
                                             f"digits of {col} {cell.prefix}")
                continue
            tgt, parts = next((a, b) for a, b in rels if col in b)
            v = c[tgt].value - sum(c[x].value for x in parts if x != col)
            ok = ee_digits(v).startswith(cell.prefix)
            EE_CHK.n[tp] += 1
            if not ok:
                EE_CHK.fail[tp].append(f"{ed} {lab} {col}: solved {v}, legible digits {cell.prefix}")
            cell.value, cell.flag = v, "derived_from_totals"
            EE_DERIVED[name].append((ed, lab, col, v, cell.prefix))
    data = [(lab, c) for lab, c in rows if lab != EE_TOTALROW]
    tot = dict(rows).get(EE_TOTALROW)
    for lab, c in rows:
        for tgt, parts in rels:
            if c[tgt].value is None or any(c[x].value is None for x in parts):
                continue
            EE_CHK.eq(tp, f"{ed} p.{page[tgt]} {lab}: {' + '.join(parts)} vs {tgt}",
                      sum(c[x].value for x in parts), c[tgt].value)
    if tot:
        for col in cols:
            xs = [c[col] for _, c in data if c[col].flag != "absent"]
            if tot[col].value is None or any(x.value is None for x in xs if x.flag != "not_applicable"):
                continue
            EE_CHK.eq(tp, f"{ed} p.{page[col]} column {col} vs {EE_TOTALROW}",
                      sum(x.value for x in xs if x.value is not None), tot[col].value)
    for lab, c in data:
        for j, col in enumerate(cols):
            cell = c[col]
            if col in totalcols or cell.flag == "absent":
                continue
            code, fr, unit = meas[col]
            right = "view2" in sec and j >= left
            flag = cell.flag if cell.flag in ("not_applicable", "derived_from_totals", "illegible") else ""
            flag = EE_FLAG.get((ed, lab, col), flag)
            out[name].append(dict(census=ed, table_id=sec["table"], gallica_ark=sec["ark"], source_page=page[col],
                                  gallica_view=sec["view2"] if right else sec["view"], year=int(sec["year"]),
                                  locality=lab, measure=code, measure_fr=fr, unit=unit,
                                  value=el_fmt(cell.value, unit), text_fr=cell.text or "", flag=flag))


def build_elec_early(write=True, verbose=False):
    out = defaultdict(list)
    for sec in sv_secs("elec"):
        if sec["table"] in EE_LAYOUT:
            ee_section(sec, out)
    val = {}
    for name in [v[0] for v in EE_LAYOUT.values()]:
        rs = out[name]
        eds = [e for e in ORDER if any(r["census"] == e for r in rs)]
        val[name] = dict(
            rows=len(rs), checks=sum(EE_CHK.n[f"{name}|{e}"] for e in eds),
            failed=[f for e in eds for f in EE_CHK.fail[f"{name}|{e}"]],
            by_edition={e: dict(rows=sum(r["census"] == e for r in rs), checks=EE_CHK.n[f"{name}|{e}"],
                                failed=len(EE_CHK.fail[f"{name}|{e}"])) for e in eds},
            prefix_checks=[list(map(str, p)) for p in EE_PREFIX[name]],
            solved_cells=[list(map(str, d)) for d in EE_DERIVED[name]])
    if write:
        for name, rs in out.items():
            SV_DIMS[name] = ["locality", "measure", "measure_fr", "unit"]
            sv_write_csv(name, rs)
            (OUT / f"{name}.md").write_text(ee_notes(name, rs, val[name]))
        (OUT / "communes_validation_elec_1922_1928.json").write_text(
            json.dumps(val, indent=1, ensure_ascii=False) + "\n")
    if verbose:
        for name, v in val.items():
            print(f"{name}: {v['rows']} rows; checks {v['checks']}, failed {len(v['failed'])}")
            for f_ in v["failed"]:
                print("  FAIL", f_)
    return out, val


EE_TITLE = {
    "communes_electricity_1922_1927": (
        "a) Électricité : longueur des canalisations ; puissance des installations ; abonnés ; consommation ; produits",
        "Electricity by locality, earlier layout (sgt1922–sgt1927): length of the network, installed power at "
        "31 December (hectowatts), subscribers, kilowatt-hours consumed (private customers, public lighting) and gross "
        "receipts (private customers, town)."),
    "communes_electricity_1928": (
        "a) Électricité : longueur des canalisations ; puissance des installations ; abonnés ; consommation ; produits",
        "Electricity by locality, sgt1928: length of the network, installed power at 31 December 1928, subscribers, "
        "kilowatt-hours consumed and gross receipts, each split by private customers / town and lighting / power."),
}
EE_UNITS = {"communes_electricity_1922_1927": "`m` (metres), `hW` (hectowatts, as headed), `kWh`, `count` or `francs`",
            "communes_electricity_1928": "`m` (metres), `kW` (as headed, *Kws*), `kWh`, `count` or `francs`"}
EE_TEXT = {
    "communes_electricity_1922_1927": [
        "**Tables.** Lower half of the *Service des eaux* page (left) and of the *Gaz* page (right) under the heading "
        "*Éclairage*: sgt1922 pp. 38–39 (views 62–63, 7 localities), sgt1923 pp. 42–43 (views 544–545, 6), sgt1924 "
        "pp. 42–43 (views 1032–1033, 6), all in `bpt6k9105649x`; sgt1925 pp. 42–43 (views 66–67, 7) and sgt1926 "
        "pp. 50–51 (views 614–615, 8), in `bpt6k9105650k`; sgt1927 pp. 50–51 (views 78–79, 17), in `bpt6k91056510`. "
        "Left page: locality, length of the network (*Longueur des canalisations*, mètres), power of the installations "
        "in service at 31 December (*Éclairage*, *Autres usages*, *TOTAL*, headed *hectowats*), number of subscribers "
        "(*Éclairage*, *Autres usages*, *TOTAL*). Right page: kilowatt-hours consumed (*Nombre de kilowats-heures "
        "consommés*: *Particuliers*, *Éclairage public*, *TOTAL*), gross receipts (*Produits bruts*: *Particuliers*, "
        "*Ville*, *TOTAL*, fr. c.), *Redevance à la ville et droit de contrôle* and *Droit d'occupation du sous-sol* "
        "(fr. c.). The column set is the same in all six editions (sgt1928 changes it: "
        "`communes_electricity_1928.csv`). The TOTAL columns are not stored (row checks). No column totals and no "
        "footnotes are printed.",
        "**Year.** The power heading reads *au 31 décembre* with no year, and no other year is printed in the table; "
        "`year` is the edition year, as for the water sales (*Recettes en 1922*, …) and the gas table printed beside "
        "it, which run to the edition year.",
        "**Units.** Length in metres as printed (\"144.870\" = 144 870 m); power in hectowatts as headed, with a "
        "decimal digit where printed (sgt1925 Ferryville 49,5 and 94,5; Sfax 7.528,3 / 1.264,8 / 8.793,1); kWh as "
        "printed, with the decimals of sgt1924–sgt1925 (kWh printed with a centimes-like sub-column, e.g. Sfax "
        "220.535,30); francs with centimes; printed » = 0. **sgt1927 Bizerte power** is printed 4.975.820 / 2.626 / "
        "4.278.446, a thousand times the 3.200–3.700 hW of the earlier years: apparently watts (like Sfax and Gabès "
        "in sgt1929), kept as printed in `hW`.",
        "**Particular cells.** sgt1922: the subscribers TOTAL column runs into the binding, only its leading digits "
        "legible (Tunis \"9.4\" …); each is checked on those digits against the sum of its parts (all agree; listed "
        "below). sgt1924: the kWh *Particuliers* column curves into the binding; Tunis \"(4.)449.733\" (leading 4 "
        "faint on the curve and repeated on the edge of the facing view). sgt1926: Tunis *Redevance* \"482.337 05\" "
        "with the word *majoration* printed beneath it (value stored, word in `text_fr`); Tunis length \"157.26?\" "
        "with a broken last digit, read 157.260 (the OCR gives \"157.26>\"; lengths have no check). sgt1926 is "
        "faintly printed throughout; its summed figures are confirmed by the row totals, which all agree.",
        "**Image versus OCR.** Every cell was read on native-resolution crops of `hires.py` pages (each page at "
        "0.6–1.1 scale, the binding strips of both views stitched at 1–1.2×, every failing or doubtful cell at "
        "1.3–4×). The Gallica OCR was used only as a cross-check; it agrees with every figure it reads except its own "
        "misreadings (e.g. sgt1922 Ferryville kWh 69.300 for 62.300, Sfax 118.888 for 178.888; sgt1926 Bizerte "
        "length 32.107 for 32.407). No stored value rests on the OCR alone.",
    ],
    "communes_electricity_1928": [
        "**Table.** sgt1928 pp. 50–51 (views 602–603, `bpt6k91056510`), lower half of the *Service des eaux* page "
        "(left) and of the *Gaz* page (right): 17 localities. The column set is that of sgt1929–sgt1930 "
        "(`communes_electricity_networks.csv`), and the measure codes are the same: left page: locality, length "
        "(mètres), power of the installations in service at 31 December 1928 (*Éclairage*, *Autres usages*, *TOTAL*, "
        "headed *Kws*), subscribers (*Éclairage*, *Autres usages*, *TOTAL*), kWh consumed (*Kilowatheures "
        "consommés*) by private customers (*Particuliers*: *Éclairage*, *Force*); right page: kWh *Ville* "
        "(*Éclairage*, *Force*), kWh *TOTAL*, *Produits bruts* (Particuliers Éclairage / Force, Ville Éclairage / "
        "Force, *TOTAL*, francs), *Redevance à la ville et droit de contrôle*, *Droits d'occupation des sous-sols*. "
        "The TOTAL columns are not stored (row checks). No column totals and no footnotes are printed. `year` = 1928, "
        "the year of the power heading.",
        "**Units.** Length in metres; power in kW as headed (*Kws*), kept as printed although the figures look like "
        "hectowatts or watts (Tunis 122.468 + 43.418 = 165.886 Kws; sgt1929 prints 13.693 + 5.068 kW for Tunis); kWh "
        "with one decimal where printed (decimal comma, thousands point); francs with centimes. Printed » and "
        "*Néant* = 0.",
        "**Particular cells.** The kWh *Particuliers Force* column (view 602, against the binding) is set "
        "progressively higher than its lines, the last entries about half a line high; its 17 entries were assigned in "
        "order and each is confirmed by its kWh row total (all rows check except Ariana, below). Tunis kWh "
        "*Particuliers Éclairage* 7.469.424 and Béja 1.279.977 are in smaller type (confirmed by the row totals). "
        "St-Germain kWh *Ville Éclairage* is printed \"2.114 5\" (2.114,5).",
        "**Image versus OCR.** Every cell was read on native-resolution crops (each page in two parts at 0.9–1.0 "
        "scale; every failing or doubtful cell at 1.8–3×). The Gallica OCR agrees with every figure it reads; it "
        "misses the kWh *Particuliers Force* column, which rests on the image (and the row totals) only.",
    ],
}
EE_FAIL_TEXT = {
    "communes_electricity_1922_1927": [
        "  Each failure was re-read at 1.3–4×: the stored cells are as printed and only a row total is printed, so no "
        "stored cell can be singled out and none is flagged. Several look like misprints of the TOTAL (sgt1923 Sfax "
        "kWh 208.267 for 280.267; sgt1925 Bizerte receipts 540.728,70 for 490.728,70) or of a part (sgt1927 Bizerte "
        "lighting power 4.975.820 where the TOTAL implies 4.275.820).",
    ],
    "communes_electricity_1928": [
        "  Each failure was re-read at 1.8–3×; the stored cells are as printed and none can be singled out (only row "
        "totals are printed), so none is flagged.",
    ],
}


def ee_notes(name, rows, v):
    doc = dict(SV_BASECOLS)
    doc.update(year="year of the figures (see below)", locality="locality as printed",
               measure="English code of the printed column", measure_fr="column heading as printed (French), "
               "with its group heading", unit="unit of `value`: " + EE_UNITS[name],
               value="number in `unit`, as printed (decimals kept; francs with centimes); printed » or *Néant* = 0",
               text_fr="word printed with or instead of a number",
               flag="empty; `not_applicable` (text instead of a number: value NA); `derived_from_totals` (cell partly "
                    "hidden, solved from the row identity and checked on its legible digits); `illegible` (value "
                    "NA); `total_mismatch` (printed value kept)")
    other = ("the earlier layout is in `communes_electricity_1922_1927.csv`, the later one (sgt1929–sgt1930) in "
             "`communes_electricity_networks.csv`" if name.endswith("1928") else
             "the later layouts are in `communes_electricity_1928.csv` (sgt1928) and "
             "`communes_electricity_networks.csv` (sgt1929–sgt1930)")
    L = sv_header(EE_TITLE[name][0], EE_TITLE[name][1], rows, "communes_elec_<edition>.txt",
                  "Printed once per edition (SPEC_ADDENDUM rule 5); no year is printed twice, so there is no overlap "
                  f"comparison. Same table, other layouts: {other}.",
                  [(c, doc[c]) for c in ["census", "table_id", "gallica_ark", "source_page", "gallica_view", "year",
                                         "locality", "measure", "measure_fr", "unit", "value", "text_fr", "flag"]])
    sec = "`@elec28`" if name.endswith("1928") else "`@elec22`"
    L = [x.replace("Per-check output: `communes_validation_services.json`.",
                   f"Sections {sec}. Per-check output: `communes_validation_elec_1922_1928.json`.") for x in L]
    for p_ in EE_TEXT[name]:
        L += [p_, ""]
    L += ["## Validation", "",
          f"- Checks (row totals; TOTAL cells partly in the binding, on their legible digits): {v['checks']}; passed "
          f"{v['checks'] - len(v['failed'])}; failed {len(v['failed'])}. Every failure was re-read on a "
          "native-resolution crop; printed values are kept.", "",
          "| edition | rows | checks | failed |", "|---|---|---|---|"]
    L += [f"| {e} | {d['rows']} | {d['checks']} | {d['failed']} |" for e, d in v["by_edition"].items()]
    L += ["", "Failed checks:", ""] if v["failed"] else []
    L += [f"  - {x}" for x in v["failed"]]
    L += EE_FAIL_TEXT[name]
    if v["prefix_checks"]:
        L += [f"- TOTAL cells partly in the binding, checked on their legible digits ({len(v['prefix_checks'])}; "
              "not stored): " + "; ".join(f"{p[0]} {p[1]} {p[2]} \"{p[3]}…\" = sum {p[4]} "
                                           f"({'agrees' if p[5] == 'True' else 'DISAGREES'})"
                                           for p in v["prefix_checks"]) + "."]
    if v["solved_cells"]:
        L += [f"- Cells solved from the row identity ({len(v['solved_cells'])}, `derived_from_totals`):"]
        L += [f"  - {d[0]} {d[1]} {d[2]}: {d[3]} (legible digits {d[4]})" for d in v["solved_cells"]]
    fl = [r for r in rows if r["flag"]]
    L += ["- Flagged cells: " + (", ".join(f"{k} {sum(r['flag'] == k for r in fl)}"
                                           for k in sorted({r['flag'] for r in fl})) if fl else "none") + "."]
    L += [f"  - {r['census']} {r['locality']} {r['measure']} = {r['value'] if r['value'] is not None else 'NA'} "
          f"({r['flag']})" for r in fl]
    return "\n".join(L) + "\n"
# @@SERVICES END@@


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    build_more(write=(cmd == "build"), verbose=(cmd == "check"))
    build_slaughter(write=(cmd == "build"), verbose=(cmd == "check"))
    build_services(write=(cmd == "build"), verbose=(cmd == "check"))
    build_elec_early(write=(cmd == "build"), verbose=(cmd == "check"))
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
