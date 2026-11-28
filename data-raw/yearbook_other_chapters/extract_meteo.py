#!/usr/bin/env python3
"""Meteorology (*Météorologie*, *Relevé pluviométrique*) of the Statistique générale de la Tunisie,
sgt1922-sgt1930 (end of the Agriculture chapter) and sgt1935, sgt1936 (after the research institutions).

  python3 extract_meteo.py check   parse the transcriptions, run every check, print failures
  python3 extract_meteo.py build   ... and write csv/meteo_*.csv, their .md notes, csv/meteo_survey.md
                                   and csv/meteo_validation.json

Source of truth: transcribed/meteo_<edition>.txt. Format (after yb_tables.py):

    @<section> view=<left view> page=<left page> year=<year> split=<n>   section header; the first n columns are
                                   printed on the left page (view, page), the others on the right page (+1)
    img: all                       every cell read on native-resolution crops
    cols: m01 .. m12 myr d01 .. d12 dyr
    region: <text>                 region heading as printed (applies to the station lines below)
    station: <text>                station heading (part d: the lines below are periods of that station)
    controle: <text>               contrôle heading as printed
    <station> | v1 v2 ...          one printed line

Cell tokens (idea copied from extract_research.py's Cell): number; 'g' = printed "gttes"/"gouttes" (traces:
value 0, obs = traces); '-' = printed dash, pas d'observation (NA, not_applicable, obs = no_observation);
'oi' = printed "O.I." alone (NA, not_applicable, obs = incomplete); '<number>oi' = a value printed with "O.I."
(value kept, obs = incomplete); 'x' = printed "×", nombre de jours non observés (NA, not_applicable,
obs = days_not_observed); '?' = illegible (NA, illegible); trailing '!' = ocr_corrected; trailing 'd' = cell hidden in the binding gutter and
typed as the printed Année minus the other months (flag derived_from_totals; its annual check is then
not independent).
Printed annual totals (Année) are checks, not rows.
Text columns (TEXT_COLS: dates of the absolute temperatures, vent dominant) keep the typed token, '_' = space,
'-' = nothing printed.
Every transcribed/meteo_<edition>*.txt file is read (e.g. meteo_sgt1930.txt then meteo_sgt1930_cd.txt).
"""
import re
import sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path as _Path

sys.path.insert(0, str(_Path(__file__).resolve().parent))
from yb_tables import COMMON, EDITIONS, ORDER, OUT, TR, Checks, ssum, write_csv, write_validation  # noqa: E402

CHAPTER = "Météorologie"
SCRIPT = "extract_meteo.py"
PREFIX = "meteo"
CHK = Checks()
CREDIT = "Source gallica.bnf.fr / Ministère des Affaires étrangères."

PRINTED = {"g": "traces", "oi": "incomplete", "x": "days_not_observed", "-": "no_observation"}
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
          "november", "december"]
MONTHS_FR = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre",
             "Novembre", "Décembre"]


class Cell:
    __slots__ = ("raw", "value", "flag", "obs")

    def __init__(self, raw):
        self.raw, self.flag, self.obs = raw, "", ""
        t = raw
        if t.endswith("!") and len(t) > 1:
            self.flag, t = "ocr_corrected", t[:-1]
        if t.endswith("d") and len(t) > 1:
            self.flag, t = "derived_from_totals", t[:-1]
        if t.endswith("oi") and len(t) > 2:
            self.obs, t = "incomplete", t[:-2]
        if t == "?":
            self.value, self.flag = None, "illegible"
        elif t in ("-", "oi", "x"):
            self.value, self.flag, self.obs = None, "not_applicable", PRINTED[t]
        elif t == "g":
            self.value, self.obs = Decimal(0), PRINTED[t]
        else:
            self.value = Decimal(t)

    def __repr__(self):
        return self.raw


TEXT_COLS = {"amaxd", "amind", "wdom"}


class Text:
    __slots__ = ("raw", "value", "flag", "obs")

    def __init__(self, raw):
        self.raw, self.flag, self.obs = raw, "", ""
        self.value = None if raw == "-" else raw.replace("_", " ")

    def __repr__(self):
        return self.raw


def parse(path, ed):
    secs, cur, region, controle, station = [], None, "", "", ""
    for n, line in enumerate(path.read_text().splitlines(), 1):
        line = line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("@"):
            head = line[1:]
            name = head.split()[0]
            cur = {"table": name, "ed": ed, "ark": EDITIONS[ed], "rows": [], "cols": None, "img": "", "line": n}
            for k, v1, v2 in re.findall(r'(\w+)=(?:"([^"]*)"|(\S+))', head[len(name):]):
                cur[k] = v1 or v2
            for k in ("view", "page", "year", "split"):
                cur[k] = int(cur[k])
            secs.append(cur)
            continue
        if line.startswith("img:"):
            cur["img"] = line[4:].strip()
            continue
        if line.startswith("cols:"):
            cur["cols"] = line[5:].split()
            continue
        if line.startswith("region:"):
            region, controle = line[7:].strip(), ""
            continue
        if line.startswith("station:"):
            station = line[8:].strip()
            continue
        if line.startswith("controle:"):
            controle = line[9:].strip()
            continue
        label, vals = line.rsplit("|", 1)
        if cur["cols"] is None:
            raise ValueError(f"{path.name}:{n}: no cols: line")
        cells = [(Text if col in TEXT_COLS else Cell)(x) for col, x in zip(cur["cols"], vals.split())]
        if len(vals.split()) != len(cur["cols"]):
            raise ValueError(f"{path.name}:{n} row {label!r}: {len(vals.split())} values for {len(cur['cols'])} "
                             "columns")
        cur["rows"].append({"label": label.strip(), "region": region, "controle": controle, "station": station,
                            "cells": dict(zip(cur["cols"], cells)), "line": n})
    return secs


def where(sec, r):
    return f"{sec['ed']} p.{sec['page']} (f{sec['view']}) {r['label']}"


# Cells flagged total_mismatch: the annual total does not equal the months, re-read on crops (see FAIL_NOTES).
# sgt1936 p.113 (f124): the printed Mai rainy-days column repeats the Avril column line for line (confirmed on
# the crop), so the annual totals fail; the Mai cells of the failing lines are flagged.
FLAGS = {("sgt1936", st, "d05"): "total_mismatch" for st in (
    "Bizerte (Port)", "Aïn-bou-Rass (Captage)", "Mateur", "El-Oggaline (Aïn-Rhelal)", "Tamera (Aïn-Kherma)",
    "Utique I", "Selma", "Djebel-Abiod", "Béja", "Oum-el-Aguareb", "El-Guéria", "Aïn-Essid", "Le Munchar",
    "Guermanez", "M'Zourah (Sidi-Khalled)", "Tabarka", "Aïn-Sebaa", "Aïn-Draham")}
# sgt1930 p.262 (f820) Menzel-Temime: Printemps printed 172.6, identical to Hiver; the printed Année 410.3 implies
# 66.9 (confirmed on a zoomed crop): the Printemps cell repeats the Hiver cell, kept as printed and flagged.
FLAGS[("sgt1930", "Menzel-Temime", "spr")] = "total_mismatch"
# sgt1929 p.283 (f311) Ben-Gardane: the extrême maxima "42.0 Août" is printed alone one line below the station's
# line (in the blank gap before Gafsa); typed on the Ben-Gardane line.
FLAGS[("sgt1929", "Ben-Gardane", "amax")] = "row_realigned"
FAIL_NOTES = {
    "meteo_climate": "Both failures re-read on zoomed native-resolution crops; printed values kept. sgt1930 p. 286 "
                     "Béja, mois le plus froid: maxima 14.6, minima 4.1, moyenne 10.3, every digit clear (the "
                     "midpoint is 9.35; misprinted cell not identifiable). p. 287 Djerba: wind days N 41, NE 31, "
                     "E 108, SE 44, S 27, SW 32, W 44, NW 38, calm 0, vent dominant printed W (E has the most "
                     "days): printed as such. sgt1929 p. 282 (f310), every cell re-read on native-resolution "
                     "crops, printed values kept: the hottest-month moyenne is printed 0.35-0.7 below the "
                     "midpoint of maxima and minima at Bizerte (Carouba), Tunis (Manoubia), Grombalia, "
                     "Medjez-el-Bab, Thala, Kairouan, Sousse, Bou-Thadi, Zarzis and Kébili, and 1.2 below at "
                     "Souk-el-Arba (40.1 / 19.5 / 28.6, every digit clear); the coldest-month moyenne is 0.35 "
                     "above the midpoint at Bizerte (Carouba) and Medjez-el-Bab. In sgt1929 the printed moyenne "
                     "is evidently computed from the daily means, not the midpoint, so these are not misprints. "
                     "Fort Saint coldest month: maxima 14.2, minima printed \"— 1.2\" (dash as at Mactar and "
                     "Thala, typed -1.2), moyenne 7.5: the midpoint is 6.5 (7.7 if the dash were a stray mark); "
                     "kept as printed.",
    "meteo_means": "Both failures re-read on zoomed native-resolution crops; printed values kept. sgt1930 p. 288 "
                   "Mabtouha (St-Victor) 1926-1930: Décembre 84, Janvier 113, Février 42 give 239, Hiver printed "
                   "199, and the printed Année 423 = 110 + 199 + 111 + 3 agrees with the Hiver: one of the three "
                   "month cells is misprinted (likely Janvier 113 for 73), not identifiable with certainty. p. 290 "
                   "Sousse 1926-1930: Septembre 64, Octobre 15, Novembre 25 give 104, Automne printed 106 (the "
                   "Année 257 agrees with 106): a printed inconsistency beyond rounding.",
    "meteo_rainfall_season": "Every failure was re-read on a zoomed native-resolution crop of the line; printed "
                             "values kept. sgt1930 p. 262 Menzel-Temime: Printemps (172.6) is printed identical "
                             "to Hiver, the Année implies 66.9, so the Printemps cell is flagged `total_mismatch`. "
                             "p. 265 Djebel-Mansour (Sainte-Gilberte) (540.8 vs 510.8, a difference of exactly "
                             "30: one digit misprinted, cell not identifiable). Small differences (p. 260 "
                             "Aïn-Sebaâ -0.6, p. 263 Le Kef I +0.2, p. 265 Sainte Maurice de Djebibina +0.1, "
                             "Kundar +0.9): printed inconsistencies, every digit clear. sgt1929 (every digit "
                             "clear on a zoomed crop, printed inconsistencies): p. 261 El-Alem (Henriville) "
                             "(seasons 508.0, Année 507.5), Mahédia (447.5 vs 447.3); p. 262 Bordj-Lacroix "
                             "(233.4 vs 233.7), Maknassy (Saint-Félix) (301.7 vs 305.7), Gabès (118.9 vs "
                             "119.5).",
    "meteo_rain_days": "sgt1936 p. 113 (f124): the Mai column is printed as an exact copy of the Avril column on "
                       "every line of the page, which explains all eighteen failures on that page (Mai cells "
                       "flagged `total_mismatch`; the true May values are not recoverable from the annual total "
                       "alone with certainty, so the printed values are kept). Every other failure below was "
                       "re-read month by month on zoomed native-resolution crops; the printed values are kept and "
                       "the misprinted cell cannot be identified unless stated: sgt1936 p. 115 Henchir-French, "
                       "Radès; p. 117 Fedjet-Khemakhem, Dridjat, Djebel-Oust, Menzel-bou-Zelfa, Beni-Aïech, "
                       "Bir-bou-Rekba; p. 121 Mell-Rechga; p. 123 Testour-Briouik; p. 123 Ksar-bou-Kriss "
                       "(Ouled-Zaïr), Henchir-Sidi-bou-Goussa, Henchir-el-Bey and Sidi-bou-Rouis (Gare): the "
                       "four days-Année cells at the foot of the page are printed out of line (the month sums "
                       "57, 54, 92, 40 match the printed 40/55/92/55 only after shifting), a misprint in the "
                       "totals, so no row is flagged; p. 125 Lorbeuss (Gare); p. 127 Sbeïtla (Henchir-Touille), "
                       "Sbeïtla-Nord; p. 129 El-Djem. sgt1935 p. 149 Djebel Oust (96 vs 101), p. 153 Sidi bou "
                       "Becker (91 vs 93), p. 157 Le Sers (gare) (60 vs 58), Tadjerouine (Aïn-Zouagha) (68 vs 73) "
                       "and Mactar (68 vs 78): every month re-read on zoomed crops; printed inconsistencies. sgt1929 (every "
                       "cell re-read on zoomed crops, printed values kept): p. 270-271 La Forestière (months 91, "
                       "Total printed 81); p. 274-275 Sbeïtla (Henchir-Touille) (months 90, Total printed 60, "
                       "likely 90 misprinted).",
    "meteo_rainfall_monthly": "Every failure was re-read on zoomed native-resolution crops of both pages; printed "
                              "values kept; misprint cell not identifiable unless stated. sgt1936: p. 112-113 "
                              "Aïn-bou-Rass (Captage); p. 116-117 Saint-Cyprien, Mengoub; p. 118-119 Zaghouan "
                              "(Contrôle), Djebel-Mansour (Saint-Joseph), Djebel-Mansour (Henchir-Karbine), Dhomda I; "
                              "p. 120-121 Bir-el-Akhdar; p. 122-123 Testour-Briouik (434.0 vs 494.0, October clearly "
                              "31.2, so the Année looks misprinted), Testour (Henchir-Aïn-Milled), Sidi-Attia, "
                              "Aïn-Tounga; p. 126-127 Sbeïtla (Henchir-Touille) (8 of the Année overprinted), "
                              "Dar-Ouled-Sidi-Ferhatt (273.1 vs 373.1: Année misprint by 100); p. 128-129 El-Kheley, "
                              "Monastir, Teboulba (Bonne-Veine) (388.4 vs 288.4: Année misprint by 100); p. 130-131 "
                              "Le Jujubier, Beauregard, La Provence (Limaya): the three Année cells are permuted in "
                              "print (months add to 142.1, 134.9, 183.2); p. 132-133 Tatahouine (167.8 vs 193.7). "
                              "sgt1935: p. 146 Mateur (Décembre clearly 108.0); p. 152-153 El-Akhouat (gare) "
                              "(Décembre clearly 42.7); p. 154-155 El-Aroussa (Fme-Alsacienne); p. 156 Rohia; p. 160 "
                              "Kundar (298.4 vs 318.4), Ksour-Essaf (262.0 vs 163.0, Janvier clearly 110.0, Année "
                              "misprint by 99); p. 162 Roderiebourg (Novembre printed \"4.0\" at the gutter, possibly "
                              "a lost leading digit; not derived because the fragment is complete as printed). "
                              "sgt1935 cells flagged `derived_from_totals` (Novembre lost in the binding gutter, typed "
                              "as Année minus the other months) cannot fail their check by construction. sgt1930 (cells re-read on "
                              "zoomed crops, printed values kept): p. 268-269 Bizerte Carouba (months 753.0, "
                              "Total 753.2; Juillet printed \"4 7\" read 4.7; part c) also prints 753.2), De "
                              "Carnières (Saint-Antoine) (445.3 vs 444.3); p. 270-271 El-Aouina (372.2 vs 362.2, "
                              "Total misprint by 10); p. 282-283 Sousse (237.2 vs 232.2: part c) prints 237.2, so "
                              "the part b) Total is the misprint), Maknassy (gare) (153.4 vs 371.4: every month "
                              "clear; the Total is not a plausible sum of the line, misprinted). sgt1929 (re-read "
                              "on zoomed crops, printed inconsistencies): p. 266-267 Saint-Cyprien (417.7 vs "
                              "417.6); p. 270-271 Dhomda II (533.0 vs 533.1), Sidi bou Becker (531.2 vs 541.2, one "
                              "digit off by 10); p. 272-273 Aïn-Tounga (531.0 vs 524.0).",
}


def rain_cells(sec):
    """Monthly rainfall (mm) and rainy days of the solar-year table; the annual totals are checks."""
    out_mm, out_d = [], []
    cols = sec["cols"]
    for r in sec["rows"]:
        c = r["cells"]
        for kind, store, tot in (("m", out_mm, "myr"), ("d", out_d, "dyr")):
            mcols = [f"{kind}{i:02d}" for i in range(1, 13)]
            vals = [c[m].value for m in mcols]
            # annual total checked only when every month is observed and the total is printed
            if all(c[m].obs in ("", "traces") for m in mcols):
                CHK.eq(f"{PREFIX}_{'rainfall_monthly' if kind == 'm' else 'rain_days'}",
                       f"{where(sec, r)} {'mm' if kind == 'm' else 'days'}: months vs Année", ssum(vals),
                       c[tot].value)
            for i, m in enumerate(mcols):
                cell = c[m]
                left = cols.index(m) < sec["split"]
                flag = FLAGS.get((sec["ed"], r["label"], m), cell.flag)
                store.append({
                    "census": sec["ed"], "table_id": "rainfall_solar_year", "gallica_ark": sec["ark"],
                    "source_page": sec["page"] if left else sec["page"] + 1,
                    "gallica_view": sec["view"] if left else sec["view"] + 1, "year": sec["year"],
                    "region": r["region"], "controle": r["controle"], "station": r["label"],
                    "month": MONTHS[i], "month_fr": MONTHS_FR[i],
                    "measure": "rainfall" if kind == "m" else "rain_days",
                    "measure_fr": "Hauteur totale en millimètres et dixièmes" if kind == "m" else "Nombre de jours",
                    "unit": "mm" if kind == "m" else "days", "value": cell.value, "obs": cell.obs, "flag": flag})
    return out_mm, out_d


SEASONS = [("aut", "autumn", "Automne"), ("win", "winter", "Hiver"), ("spr", "spring", "Printemps"),
           ("sum", "summer", "Eté")]


def season_cells(sec):
    """a) Agricultural-year rainfall by season. The printed Année of the year is a check, not a row; the printed
    normal annual rainfall (Année 1901-1925) is stored as a row with period 1901-1925."""
    out = []
    y = sec["year"]
    per = f"{y - 1}-{y}"
    for r in sec["rows"]:
        c = r["cells"]
        vals = [c[k].value for k, _, _ in SEASONS]
        if all(c[k].obs in ("", "traces") and c[k].flag != "illegible" for k, _, _ in SEASONS):
            CHK.eq("meteo_rainfall_season", f"{where(sec, r)}: seasons vs Année {per}", ssum(vals), c["yr"].value)
        base = {"census": sec["ed"], "table_id": "rainfall_agricultural_year", "gallica_ark": sec["ark"],
                "source_page": sec["page"], "gallica_view": sec["view"], "region": r["region"],
                "controle": r["controle"], "station": r["label"], "measure": "rainfall",
                "measure_fr": "Relevé des pluies totales par saison et pour l'année", "unit": "mm"}
        for k, en, fr in SEASONS:
            cell = c[k]
            out.append(dict(base, year=y, period=per, season=en, season_fr=fr, value=cell.value, obs=cell.obs,
                            flag=FLAGS.get((sec["ed"], r["label"], k), cell.flag)))
        cell = c["nor"]
        if cell.obs == "no_observation":   # no normal printed for this station: no row
            continue
        out.append(dict(base, year=None, period=sec.get("normal", "1901-1925"), season="year",
                        season_fr="Année", measure="rainfall_mean", value=cell.value, obs=cell.obs,
                        flag=cell.flag))
    return out


# c) Données climatologiques essentielles: column -> (measure, measure_fr, unit, date column)
CLIMATE = [
    ("mm", "rainfall", "Pluies : millimètres", "mm", None),
    ("days", "rain_days", "Pluies : nombre de jours", "days", None),
    ("hmax", "temp_hottest_month_max", "Température moyenne du mois le plus chaud : maxima", "degC", None),
    ("hmin", "temp_hottest_month_min", "Température moyenne du mois le plus chaud : minima", "degC", None),
    ("hmean", "temp_hottest_month_mean", "Température moyenne du mois le plus chaud : moyenne", "degC", None),
    ("cmax", "temp_coldest_month_max", "Température moyenne du mois le plus froid : maxima", "degC", None),
    ("cmin", "temp_coldest_month_min", "Température moyenne du mois le plus froid : minima", "degC", None),
    ("cmean", "temp_coldest_month_mean", "Température moyenne du mois le plus froid : moyenne", "degC", None),
    ("amax", "temp_absolute_max", "Température extrême annuelle : maxima", "degC", "amaxd"),
    ("amin", "temp_absolute_min", "Température extrême annuelle : minima", "degC", "amind"),
    ("ymax", "temp_annual_mean_max", "Température moyenne annuelle : maxima", "degC", None),
    ("ymin", "temp_annual_mean_min", "Température moyenne annuelle : minima", "degC", None),
    ("ymean", "temp_annual_mean", "Température moyenne annuelle : moyenne", "degC", None),
] + [(f"w{d}", f"wind_days_{d.lower()}", f"Nombre de jours au cours de l'année pendant lesquels le vent dominant "
      f"a été : {d}", "days", None) for d in ("N", "NE", "E", "SE", "S", "SW", "W", "NW")] + [
    ("wcalm", "calm_days", "Nombre de jours au cours de l'année pendant lesquels le vent dominant a été : Calme",
     "days", None)]
WINDS = ["wN", "wNE", "wE", "wSE", "wS", "wSW", "wW", "wNW"]
FOOTNOTES = {
    ("sgt1930", "1"): "Manque les maxima de janvier.",
    ("sgt1930", "2"): "Manque les minima de décembre.",
    ("sgt1930", "3"): "Manque les maxima de janvier et février.",
    ("sgt1930", "4"): "Manque les maxima de mai.",
    ("sgt1930", "5"): "Manque les maxima de juillet, août, octobre; les minima d'octobre.",
    ("sgt1929", "1"): "Manque les minima du mois de juillet.",
    ("sgt1929", "2"): "Manque les maxima de décembre.",
}


def climate_cells(sec):
    """c) One row per station and measure; the vent dominant is a text row (value NA, direction in text_fr).
    Checks: moyenne = (maxima + minima) / 2 (tolerance 0.3: the printed moyenne is computed from the daily
    observations and is only close to the midpoint); the wind days add to at most the days of the year
    (they add to 365 at only some stations: days without observation are not counted); the vent dominant is the direction with the most days (calm aside)."""
    out, t = [], "meteo_climate"
    ndays = Decimal(366 if sec["year"] % 4 == 0 else 365)
    for r in sec["rows"]:
        c = r["cells"]
        m = re.match(r"^(.*?)\s*\((\d)\)$", r["label"])
        station, note = (m.group(1), FOOTNOTES[(sec["ed"], m.group(2))]) if m else (r["label"], "")
        for mx, mn, me, what in (("hmax", "hmin", "hmean", "hottest month"), ("cmax", "cmin", "cmean",
                                 "coldest month"), ("ymax", "ymin", "ymean", "annual mean")):
            if c[me].flag != "derived_from_totals" and c[mx].value is not None and c[mn].value is not None:
                CHK.eq(t, f"{where(sec, r)}: {what} moyenne vs (maxima + minima) / 2", (c[mx].value + c[mn].value)
                       / 2, c[me].value, Decimal("0.3"))
        tot = ssum(c[w].value for w in WINDS + ["wcalm"])
        if tot is not None:   # days without a wind observation are simply not counted: at most the year
            CHK.n[t] += 1
            if tot > ndays:
                CHK.fail[t].append(f"{where(sec, r)}: wind days add to {tot}, more than the {ndays} days of the year")
        if c["wdom"].value and all(c[w].value is not None for w in WINDS):
            top = max(c[w].value for w in WINDS)
            got = " - ".join(w[1:] for w in WINDS if c[w].value == top)
            CHK.n[t] += 1
            if set(got.split(" - ")) != set(c["wdom"].value.split(" - ")):
                CHK.fail[t].append(f"{where(sec, r)}: vent dominant printed {c['wdom'].value}, most days {got}")
        base = {"census": sec["ed"], "table_id": "climate_essentials", "gallica_ark": sec["ark"], "year": sec["year"],
                "region": r["region"], "station": station, "note_fr": note}
        for col, meas, mfr, unit, dcol in CLIMATE:
            cell = c[col]
            left = sec["cols"].index(col) < sec["split"]
            date = c[dcol].value if dcol else None
            out.append(dict(base, source_page=sec["page"] + (not left), gallica_view=sec["view"] + (not left),
                            measure=meas, measure_fr=mfr, unit=unit, value=cell.value, date_fr=date or "",
                            text_fr="", obs=cell.obs, flag=FLAGS.get((sec["ed"], r["label"], col), cell.flag)))
        w = c["wdom"]
        out.append(dict(base, source_page=sec["page"] + 1, gallica_view=sec["view"] + 1, measure="dominant_wind",
                        measure_fr="Vent dominant", unit="direction", value=None, date_fr="", text_fr=w.value or "",
                        obs="" if w.value else "no_observation", flag="not_applicable"))
    return out


MEANS_COLS = [(f"m{i:02d}", MONTHS[i - 1], MONTHS_FR[i - 1], "month") for i in (9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8)]
MEANS_COLS += [(k, en, fr, "season") for k, en, fr in SEASONS] + [("yr", "year", "Année", "year")]
SEASON_MONTHS = {"aut": ("m09", "m10", "m11"), "win": ("m12", "m01", "m02"), "spr": ("m03", "m04", "m05"),
                 "sum": ("m06", "m07", "m08")}


def means_cells(sec):
    """d) Mean rainfall (whole mm) by month, season and year for a period; every printed cell is a row (the
    printed seasons and year are means in their own right, not totals of rows). Checks (rounding tolerance):
    each season = its three months (1 mm), Année = the four seasons (2 mm)."""
    out, t = [], "meteo_means"
    for r in sec["rows"]:
        c = r["cells"]
        ok = lambda ks: all(c[k].obs in ("", "traces") and c[k].flag not in ("illegible", "derived_from_totals")
                            for k in ks)
        for s, ms in SEASON_MONTHS.items():
            if ok(ms + (s,)):
                CHK.eq(t, f"{sec['ed']} p.{sec['page']} (f{sec['view']}) {r['station']} {r['label']}: months vs "
                       f"{s}", ssum(c[m].value for m in ms), c[s].value, Decimal(1))
        if ok(tuple(SEASON_MONTHS) + ("yr",)):
            CHK.eq(t, f"{sec['ed']} p.{sec['page']} (f{sec['view']}) {r['station']} {r['label']}: seasons vs "
                   f"Année", ssum(c[s].value for s in SEASON_MONTHS), c["yr"].value, Decimal(2))
        for col, en, fr, level in MEANS_COLS:
            cell = c[col]
            out.append({"census": sec["ed"], "table_id": "rainfall_means", "gallica_ark": sec["ark"],
                        "source_page": sec["page"], "gallica_view": sec["view"], "year": None,
                        "station": r["station"], "period": r["label"], "level": level, "month": en,
                        "month_fr": fr, "measure": "rainfall_mean",
                        "measure_fr": "Pluies moyennes mensuelles, par saison et annuelles", "unit": "mm",
                        "value": cell.value, "obs": cell.obs,
                        "flag": FLAGS.get((sec["ed"], r["station"], r["label"], col), cell.flag)})
    return out


DOC = {
    "census": "Source edition (`sgt1936` = *Statistique générale de la Tunisie*, 1936 edition).",
    "table_id": "`rainfall_solar_year` = *Relevé pluviométrique, année (solaire)*.",
    "gallica_ark": "Gallica ark of the volume (views are only unique within a volume).",
    "source_page": "Printed page number of the cell (mm January-September on the left page; mm October-December "
                   "and every rainy-days column on the right page).",
    "gallica_view": "Gallica view of `source_page`.",
    "year": "Calendar (solar) year of the observations.",
    "region": "Region heading as printed, without its roman numeral and in one case form across editions "
              "(e.g. `Tunisie du Nord`, `Tunisie du Centre (Hautes Plaines)`, `Haute Vallée de la Medjerdah`).",
    "controle": "Contrôle civil heading as printed (e.g. `Contrôle de Bizerte`).",
    "station": "Rain-gauge station exactly as printed.",
    "month": "Month (English); `month_fr` as printed.",
    "month_fr": "Month heading as printed.",
    "measure": "`rainfall` (total height of rain) or `rain_days` (number of days with rain).",
    "measure_fr": "Column heading as printed.",
    "unit": "`mm` (millimetres, one decimal) or `days`.",
    "value": "Value as printed; NA when nothing was observed.",
    "obs": "Printed observation sign: `traces` (\"gttes\", gouttes: rain too small to measure, value 0); "
           "`no_observation` (\"—\", pas d'observation, value NA); `incomplete` (\"O.I.\", observations "
           "incomplètes: NA when printed alone, the printed partial value when printed beside a number); "
           "`days_not_observed` (\"×\", nombre de jours non observés, NA). Empty otherwise.",
    "flag": "Empty, `not_applicable` (no value printed: see `obs`), `illegible`, `ocr_corrected`, "
            "`total_mismatch`, `derived_from_totals` (sgt1935: cell lost in the binding gutter, value = printed "
            "Année minus the other eleven months; its integer part, where visible, agrees).",
}
DIMS = ["region", "controle", "station", "month", "month_fr", "measure", "measure_fr", "unit"]
TABLES = {
    "meteo_rainfall_season": dict(
        title_fr="Relevé pluviométrique de l'année agricole : pluies totales par saison et pour l'année",
        title_en="Rainfall of the agricultural year: total rainfall by season and station", idx=2,
        dims=["region", "controle", "station", "period", "season", "season_fr", "measure", "measure_fr", "unit"],
        rows_text="(one per station and season of the agricultural year, plus one row per printed normal annual "
                  "rainfall). The agricultural year runs September-August (Automne = September-November, Hiver = "
                  "December-February, Printemps = March-May, Eté = June-August) and is coded in `year` as the year "
                  "it ends (1929-1930 = 1930). The printed annual total of the year (*Année 1929-30*) is a check, "
                  "not a row. The printed normal (*Année 1901-1925*) exists only as a mean: it is stored with "
                  "`season` = `year`, `measure` = `rainfall_mean`, `period` = `1901-1925` and `year` NA, only "
                  "where a value is printed.",
        check_text="Année of the agricultural year = sum of the four seasons, for every line whose four seasons "
                   "are printed and whose Année is printed",
        doc={"table_id": "`rainfall_agricultural_year` = *a) Relevé pluviométrique de l'année agricole*.",
             "source_page": "Printed page number (one page per table).",
             "year": "Year in which the agricultural year (September-August) ends (1928-1929 = 1929, 1929-1930 = 1930); NA for "
                     "the normals.",
             "region": "Natural-region heading as printed in sgt1930 part a) (sgt1929 prints no headings in part a): the sgt1930 names are supplied for the same groups) (e.g. `Kroumirie`, `Mogods`, `Golfe de "
                       "Tunis`, `Région de Dakla`), without roman numerals, in title case with accents restored "
                       "as in the solar-year tables. The part a) regions differ from the part b) regions.",
             "controle": "Empty (part a) has no contrôle headings).",
             "station": "Rain-gauge station exactly as printed.",
             "period": "`1928-1929` / `1929-1930` for the observations of the agricultural year; `1901-1925` for the printed "
                       "normal annual rainfall.",
             "season": "`autumn`, `winter`, `spring`, `summer`, or `year` (normal annual rainfall).",
             "season_fr": "Column heading as printed.",
             "measure": "`rainfall` (total rainfall of the season) or `rainfall_mean` (normal annual rainfall, "
                        "mean of the period).",
             "measure_fr": "Table heading as printed.",
             "unit": "`mm` (millimètres, one decimal).",
             "value": "Value as printed; NA when nothing was printed (`—`).",
             "obs": "`traces` (\"gouttes\": value 0); `no_observation` (\"—\", value NA). Empty otherwise.",
             "flag": "Empty, `not_applicable` (dash printed: see `obs`), `illegible`, `derived_from_totals` "
                     "(sgt1929: damaged digit typed as the printed Année minus the other seasons), "
                     "`total_mismatch` (sgt1930 Menzel-Temime Printemps)."}),
    "meteo_rainfall_monthly": dict(
        title_fr="Relevé pluviométrique : hauteur totale de pluie en millimètres et dixièmes, par station et par mois",
        title_en="Rainfall record: total rainfall in millimetres by station and month (solar year)", idx=0),
    "meteo_rain_days": dict(
        title_fr="Relevé pluviométrique : nombre de jours de pluie, par station et par mois",
        title_en="Rainfall record: number of rainy days by station and month (solar year)", idx=1),
    "meteo_climate": dict(
        title_fr="Données climatologiques essentielles fournies par les principales régions tunisiennes",
        title_en="Essential climatological data of the main Tunisian regions: rainfall, temperatures and winds "
                 "by station", idx=3,
        dims=["region", "station", "note_fr", "measure", "measure_fr", "unit", "date_fr", "text_fr"],
        rows_text="(one per station and measure: rainfall and rainy days of the year; maxima, minima and "
                  "moyenne of the hottest and of the coldest month; absolute (extrême annuelle) maxima and minima "
                  "with their dates; annual mean maxima, minima and moyenne; days of the year by dominant wind "
                  "direction N ... NW and calm; plus one `dominant_wind` row per station). The dominant wind "
                  "(*vent dominant*) is a direction, not a number: its row has `value` NA, flag "
                  "`not_applicable`, and the printed direction in `text_fr` (e.g. `NW`, `SE - SW`).",
        check_text="moyenne = (maxima + minima) / 2 within 0.3 degree (an approximate identity: at 0.1 degree "
                   "eleven sgt1930 cells differ by 0.15-0.3, so the printed moyenne is not exactly the midpoint; in sgt1929 the hottest-month moyenne is printed systematically below the midpoint), for the hottest month, the coldest month "
                   "and the annual mean, where both are printed; wind days N ... NW + calm at most the days of "
                   "the year (sgt1930: they add to exactly 365 at only 17 of the 31 stations: days without observation are "
                   "not counted, so equality is not an identity); printed vent dominant = direction(s) with the most days (calm aside)",
        doc={"table_id": "`climate_essentials` = *c) Données climatologiques essentielles fournies par les "
                         "principales régions tunisiennes*.",
             "source_page": "Printed page of the cell (rainfall and the hottest / coldest month on the left "
                            "page, the rest on the right page).",
             "year": "Calendar year of the observations.",
             "region": "Region heading as printed (vertical, without accents in print: `REGION DES OASIS`), "
                       "typed with accents restored (`Région du Nord`, `Région du Nord-Est`, `Région Centrale`, "
                       "`Sahel`, `Région des Oasis`, `Extrême Sud`, `Sahara`).",
             "station": "Localité as printed, without its footnote marker.",
             "note_fr": "Footnote of the station as printed (missing months), empty otherwise.",
             "measure": "`rainfall`, `rain_days`, `temp_hottest_month_max|min|mean`, "
                        "`temp_coldest_month_max|min|mean`, `temp_absolute_max|min`, `temp_annual_mean_max|min`, "
                        "`temp_annual_mean`, `wind_days_n` ... `wind_days_nw`, `calm_days`, `dominant_wind`.",
             "measure_fr": "Column heading as printed (group : column).",
             "unit": "`mm`, `days`, `degC` (degrees Celsius, one decimal) or `direction`.",
             "date_fr": "For `temp_absolute_max|min`: month(s) of the extreme as printed (`Juil.`, `J. F.` = "
                        "janvier and février, `J. D.` = janvier and décembre); empty otherwise.",
             "text_fr": "For `dominant_wind`: the printed direction; empty otherwise.",
             "value": "Value as printed; NA when a dash is printed and for `dominant_wind`.",
             "obs": "`no_observation` (\"—\" printed, value NA); `traces` (sgt1929 Fort Saint rainfall "
                    "printed \"0\" = gouttes, value 0). Empty otherwise.",
             "flag": "Empty, `not_applicable` (dash printed, or the text row `dominant_wind`), "
                     "`derived_from_totals` (sgt1930 Fort Saint coldest-month moyenne: decimal smudged, "
                     "typed (maxima + minima) / 2), `illegible` (sgt1929 Tabarca annual moyenne printed \"18°\" "
                     "without its decimal), `row_realigned` (sgt1929 Ben-Gardane extrême maxima, printed one "
                     "line low)."}),
    "meteo_means": dict(
        title_fr="Pluies moyennes mensuelles, par saison et annuelles",
        title_en="Mean monthly, seasonal and annual rainfall by station and period", idx=4,
        dims=["station", "period", "level", "month", "month_fr", "measure", "measure_fr", "unit"],
        rows_text="(one per station, period and printed column: twelve months September-August, four seasons, "
                  "the year). These retrospective means exist only as means (the yearly values behind them are "
                  "not printed in the same edition), so every printed cell is stored, the seasons and the year "
                  "included; `year` is NA.",
        check_text="each season = sum of its three months within 1 mm and the Année = sum of the four seasons "
                   "within 2 mm (the means are printed rounded to whole millimetres), where every cell is printed",
        doc={"table_id": "`rainfall_means` = *d) Pluies moyennes mensuelles, par saison et annuelles pour les "
                         "périodes : 1926-1930 et 1901-1930*.",
             "source_page": "Printed page number (one page per table).",
             "year": "NA (means of a period: see `period`).",
             "station": "Station heading as printed.",
             "period": "Period of the mean as printed (`1926-1930`, `1901-1930`).",
             "level": "`month`, `season` or `year`.",
             "month": "Month (English), season (`autumn` = September-November, `winter`, `spring`, `summer`) or "
                      "`year` (agricultural year September-August).",
             "month_fr": "Column heading as printed.",
             "measure": "`rainfall_mean` (mean rainfall over the period).",
             "measure_fr": "Table heading as printed.",
             "unit": "`mm` (whole millimetres).",
             "value": "Mean as printed; 0 for \"gttes\"; NA when a dash is printed.",
             "obs": "`traces` (\"gttes\", gouttes: value 0); `no_observation` (\"—\", value NA).",
             "flag": "Empty, `not_applicable` (dash printed), `derived_from_totals` (sgt1930 p. 290 Sfax "
                     "1926-1930 Hiver, broken type, typed as the sum of its three months)."}),
}

SURVEY = {
    "sgt1936": "f116-f122 research institutions (extract_research.py). f123-f144 *Relevé pluviométrique - année "
               "1936*, eleven two-page spreads (left page: stations and mm January-September; right page: mm "
               "October-December, Année, then nombre de jours January-December, Année), stations grouped by "
               "region and contrôle; N.B. signes conventionnels: — pas d'observation, × nombre de jours non "
               "observés, O.I. observations incomplètes; \"gttes\" = gouttes. Only part b) (solar year) is "
               "printed. f145 blank.",
    "sgt1935": "f165 (p. 145) Laboratoire de chimie (Sfax), analyses 1935 (not meteorology). f166-f183 *b) Relevé "
               "pluviométrique de l'année 1935*, nine two-page spreads (left page: stations and mm January-November, "
               "December in the binding gutter; right page: Total mm, then nombre de jours January-December, Total), "
               "same signes conventionnels as sgt1936; only part b) printed. The binding gutter hides the decimals "
               "of the November column on most spreads (cells derived from the annual total, flagged "
               "`derived_from_totals`). f184 blank.",
    "sgt1930": "Météorologie at the end of chapter XI Agriculture, printed pages 260-291. f818-f825 (p. 260-267) "
               "*a) Relevé pluviométrique de l'année agricole (1929-1930)*, one table per page: Automne, Hiver, "
               "Printemps, Eté, Année 1929-30, Année 1901-1925 (p. 266 head misprinted \"1901-1905\"), stations "
               "grouped by natural region (Kroumirie ... Extrême Sud), no contrôle headings; transcribed "
               "(meteo_rainfall_season). f826-f843 (p. 268-285) *b) Relevé pluviométrique de l'année 1930*, nine "
               "two-page spreads (left page: stations and Millimètres de pluie January-November; right page: "
               "December and Total, then Nombre de jours January-December and Total), key \"Signes "
               "conventionnels : — pas d'observation; × le nombre de jours manque; O gouttes; O. I. observations "
               "incomplètes\" across the top of the spread; transcribed (meteo_rainfall_monthly, "
               "meteo_rain_days). f844|f845 (p. 286-287) *c) Données climatologiques "
               "essentielles fournies par les principales régions tunisiennes (année 1930)*, one spread: localités "
               "grouped by region, Pluies (millimètres, nombre de jours), Température moyenne du mois le plus chaud "
               "/ le plus froid (moyennes, maxima, minima), Température absolue (maxima, minima, with dates), "
               "nombre de jours au cours de l'année pendant lesquels le vent a soufflé de N, NE, E, SE, S, SW, W, "
               "NW, calme, vent dominant; footnotes (1)-(5) on missing months; transcribed (meteo_climate, "
               "meteo_sgt1930_cd.txt). f846-f849 "
               "(p. 288-291) *Pluies moyennes mensuelles, par saison et annuelles pour les périodes : 1926-1930 et "
               "1901-1930*, two lines (1926-1930, 1901-1930) per station (Tabarka ... Tatahouine), columns "
               "Septembre-Août, Automne, Hiver, Printemps, Eté, Année, 39 stations; transcribed (means only: "
               "meteo_means, meteo_sgt1930_cd.txt).",
    "sgt1929": "Météorologie at the end of the Agriculture chapter, printed pages 256-284 (same volume and ark "
               "as sgt1930). f284-f290 (p. 256-262) *a) Relevé pluviométrique de l'année agricole (1928-1929)*, "
               "one table per page: Automne, Hiver, Printemps, Eté, Année 1928-29, Année 1901-1925; the station "
               "groups are separated by blank lines only (no region headings printed: the sgt1930 region names "
               "are supplied); transcribed (meteo_rainfall_season). f291 blank. f292-f309 (p. 264-281) *b) "
               "Relevé pluviométrique* of 1929, nine two-page spreads (left page: stations and mm "
               "January-November, November at the binding gutter; right page: December, Total, Nombre de jours "
               "January-December, Total), key \"— pas d'observation; × le nombre de jours manque; O gouttes; "
               "O. I. observations incomplètes\" (a bare \"0\" in a mm column = gouttes); transcribed "
               "(meteo_rainfall_monthly, meteo_rain_days). f310|f311 (p. 282-283) *c) Données climatologiques "
               "essentielles fournies par les principales régions tunisiennes (année 1929)*, one spread, same "
               "columns as sgt1930, 30 localités, footnotes (1)-(2); transcribed (meteo_climate, "
               "meteo_sgt1929_cd.txt). f312 (p. 284) *Station centrale de la Manoubia de Tunis, année 1929*: "
               "rainfall by wind direction and month, frequency of rainy winds, dominant wind on rainy days (fits "
               "no meteo_ table; not transcribed). No part d) (means) is printed.",
    "sgt1928": "f806-f835 Météorologie, parts a)-d) (views per part not yet surveyed page by page).",
    "sgt1927": "f282-f287 a) relevé pluviométrique de l'année agricole 1926-1927; f288-f303 b) année solaire 1927 "
               "(mm | jours spreads); f304|f305 c) données climatologiques essentielles 1927; f306|f307 d) période "
               "1901-1925, pluies moyennes mensuelles, saisonnières et annuelles (année agricole à partir de "
               "septembre).",
    "sgt1926": "f819-f825 a) année agricole 1925-1926; f826-f839 b) année solaire 1926; f840|f841 c) données "
               "climatologiques essentielles 1926; f842-f845 d) températures moyennes et extrêmes mensuelles, "
               "saisonnières et annuelles 1901-1925.",
    "sgt1925": "f309-f315 a) année agricole 1924-1925; f316-f329 b) année solaire 1925; f330|f331 c) données "
               "climatologiques 1925; f332-f334 d) pluviométrie agricole 1900-1901 à 1924-1925 (five-year means).",
    "sgt1924": "f1247-f1251 a) année agricole 1923-1924; f1252-f1263 b) année solaire 1924; f1264|f1265 c) données "
               "climatologiques 1924; f1266-f1268 d) moyennes pluviométriques mensuelles, saisonnières et annuelles "
               "de la période décennale 1911-1920.",
    "sgt1923": "f745-f749 a) année agricole 1922-1923 (with the 1901-1910 normal); f750-f759 b) année solaire 1923; "
               "f760|f761 c) données climatologiques essentielles 1923; f762-f764 d) pluviométrie agricole "
               "1900-1901 à 1919-1920 (five-year means).",
    "sgt1922": "f255-f259 a) année agricole 1921-1922; f260-f269 b) année solaire 1922; f270|f271 c) données "
               "climatologiques 1922; f272|f273 d) statistique thermométrique 1911-1920.",
}
VIEWS = {"sgt1922": "255-273", "sgt1923": "745-764", "sgt1924": "1247-1268", "sgt1925": "309-334",
         "sgt1926": "819-845", "sgt1927": "282-307", "sgt1928": "806-835", "sgt1929": "284-312",
         "sgt1930": "818-849", "sgt1935": "166-183", "sgt1936": "123-144"}
PLANNED = [
    ("meteo_rainfall_season", "a) agricultural-year rainfall by season (autumn, winter, spring, summer, year) "
     "per station, sgt1922-sgt1930; `year` = the year the agricultural year (September-August) ends, e.g. "
     "1929-1930 coded 1930; the printed normals stored with `period`"),
    ("meteo_rainfall_monthly", "b) solar-year rainfall in mm per station and month, every edition"),
    ("meteo_rain_days", "b) solar-year number of rainy days per station and month, every edition"),
    ("meteo_climate", "c) données climatologiques essentielles (temperatures, pressure, humidity, wind ... by "
     "region/station and month, with `measure`/`measure_fr` and `unit`), sgt1922-sgt1930"),
    ("meteo_means", "d) retrospective tables that exist only as means (five-year means 1900-1920 / 1900-1925, "
     "decade means 1911-1920, temperatures 1901-1925, rainfall means 1901-1925), stored with `period`"),
]


def build(write=True):
    secs = []
    for ed in ORDER:
        for p in sorted(TR.glob(f"{PREFIX}_{ed}.txt")) + sorted(TR.glob(f"{PREFIX}_{ed}_*.txt")):
            secs += parse(p, ed)
    recs = {k: [] for k in TABLES}
    for s in secs:
        if s["table"] == "season":
            recs["meteo_rainfall_season"] += season_cells(s)
        if s["table"] == "rain":
            mm, d = rain_cells(s)
            recs["meteo_rainfall_monthly"] += mm
            recs["meteo_rain_days"] += d
        if s["table"] == "climate":
            recs["meteo_climate"] += climate_cells(s)
        if s["table"] == "means":
            recs["meteo_means"] += means_cells(s)
    res = {}
    for out, spec in TABLES.items():
        rows = recs[out]
        eds = [e for e in ORDER if any(r["census"] == e for r in rows)]
        fails = CHK.fail[out]
        res[out] = dict(rows=len(rows), checks=CHK.n[out], failed=list(fails), editions=eds,
                        flagged=sum(1 for r in rows if r["flag"] and r["flag"] != "not_applicable"),
                        not_applicable=sum(1 for r in rows if r["flag"] == "not_applicable"),
                        overlap_compared=0, overlap_diffs=[])
        if write:
            cols = COMMON + spec.get("dims", DIMS) + ["value", "obs", "flag"]
            write_csv(out, cols, rows)
            write_md(out, spec, rows, cols, eds, fails)
    if write:
        write_validation(OUT / f"{PREFIX}_validation.json", dict(res, _views=VIEWS, _survey=SURVEY,
                                                                   _remaining=REMAINING))
        write_survey(res)
    return res


REMAINING = ("Transcribed: sgt1936 f123-f144 (complete), sgt1935 f166-f183 (complete), sgt1930 f818-f849 "
             "(parts a)-d), complete) and sgt1929 f284-f311 (parts a)-c)). NOT YET TRANSCRIBED: sgt1929 f312 "
             "(Manoubia rainfall by wind direction and month: fits no existing meteo_ table, would need a table "
             "of its own); every Météorologie page of sgt1928 (f806-f835), sgt1927 (f282-f307), sgt1926 "
             "(f819-f845), sgt1925 (f309-f334), sgt1924 (f1247-f1268), sgt1923 (f745-f764) and sgt1922 "
             "(f255-f273). meteo_climate holds sgt1929-sgt1930; meteo_means holds sgt1930 only.")


def write_md(out, spec, rows, cols, eds, fails):
    views = sorted({(r["census"], r["source_page"], r["gallica_view"]) for r in rows})
    fl = defaultdict(int)
    ob = defaultdict(int)
    for r in rows:
        fl[r["flag"]] += bool(r["flag"])
        ob[r["obs"]] += bool(r["obs"])
    L = [f"# {spec['title_fr']}", "", f"*{spec['title_en']}.*", "",
         f"Source: *Statistique générale de la Tunisie*, *{CHAPTER}*, editions {', '.join(eds)}. {CREDIT}", "",
         "Pages and views: " + "; ".join(f"{e} p. {p}, f{v}" for e, p, v in views) + ".", "",
         f"Transcriptions: `../transcribed/meteo_<edition>.txt`; rebuild with "
         f"`python3 -I data-raw/yearbook_other_chapters/{SCRIPT} build`.", "",
         f"Rows: {len(rows)} " + spec.get("rows_text", "(one per station, month and edition). The printed annual "
         "totals (*Année*) are checks, not rows. Each solar year is printed in one edition only, so no overlap "
         "selection is needed (SPEC_ADDENDUM rule 4 would apply to any year printed twice)."), "",
         "Partial coverage: " + REMAINING, "", "## Columns", ""]
    doc = dict(DOC, **spec.get("doc", {}))
    L += [f"- `{c}`: {doc[c]}" for c in cols]
    L += ["", "## Validation", "",
          "- " + spec.get("check_text", "Annual total = sum of the twelve months, for every line whose twelve "
                          "months are all observed and whose annual total is printed") + f": {CHK.n[out]} checks; passed {CHK.n[out] - len(fails)}; failed "
          f"{len(fails)}."]
    if fails:
        L += ["", "Failed checks (printed values kept; each re-read on a native-resolution crop):", ""]
        L += [f"  - {x}" for x in fails]
        if FAIL_NOTES.get(out):
            L += ["", FAIL_NOTES[out]]
    L += ["", "- Flags: " + (", ".join(f"{k}: {n}" for k, n in sorted(fl.items()) if n) or "none") + ".",
          "- Observation signs: " + (", ".join(f"{k}: {n}" for k, n in sorted(ob.items()) if n) or "none") + ".",
          "", "## Image versus OCR", "",
          "- Every cell typed from native-resolution crops of the page images; the Gallica OCR was not used."]
    if out == "meteo_rainfall_monthly":
        L += ["", "Reading notes: sgt1936 p. 114 Salammbô S.O.S, February: the second digit of \"3?.9 O.I.\" is "
              "damaged (illegible); April printed \"221 O.I.\" without decimal point, stored 22.1; May printed "
              "\"16 O.I.\", stored 16. p. 117 Bir-M'Cherga II, December: first digit overprinted, read 32.8 (confirmed by the "
              "printed annual total 506.4). sgt1935: see the header of `meteo_sgt1935.txt` for the binding-gutter "
              "re-reading (December cells of p. 146-147 and 152-153 read; November decimals derived; November "
              "column of p. 148 printed half a line high and re-aligned); Sedjenane (Gare) December read 208.0 with "
              "its first digit only partly visible (no annual total printed)."]
    (OUT / f"{out}.md").write_text("\n".join(L) + "\n")


def write_survey(res):
    L = ["# Meteorology: survey of every edition", "",
         "Survey of the meteorology pages of the *Statistique générale de la Tunisie*, view by view. Extraction: "
         "`extract_meteo.py`. Agricultural years run September-August and are coded by the year they end "
         "(1921-1922 = 1922).", "", "| edition | ark | views |", "|---|---|---|"]
    L += [f"| {e} | `{EDITIONS[e]}` | {VIEWS[e]} |" for e in ORDER if e in VIEWS]
    L += ["", "## Parts per edition (newest first)", ""]
    L += [f"- **{e}**: {SURVEY[e]}" for e in reversed(ORDER) if e in SURVEY]
    L += ["", "## Table design", ""] + [f"- `{t}`: {d}." for t, d in PLANNED]
    L += ["", "Common columns: census, table_id, gallica_ark, source_page, gallica_view, year, region, controle, "
          "station (as printed), month/season/period, measure, measure_fr, unit, value, obs, flag.", "",
          "## Tables built", "", "| CSV | editions | rows | checks | failed |", "|---|---|---|---|---|"]
    L += [f"| `{o}` | {', '.join(d['editions'])} | {d['rows']} | {d['checks']} | {len(d['failed'])} |"
          for o, d in res.items()]
    L += ["", "## Coverage", "", REMAINING, ""]
    (OUT / f"{PREFIX}_survey.md").write_text("\n".join(L) + "\n")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    res = build(write=(mode == "build"))
    for out, d in res.items():
        print(f"{out}: {d['rows']} rows, {d['checks']} checks, {len(d['failed'])} failed [{' '.join(d['editions'])}]")
        for f in d["failed"]:
            print("   FAIL", f)


if __name__ == "__main__":
    main()
