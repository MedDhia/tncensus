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


def parse(path, ed):
    secs, cur, region, controle = [], None, "", ""
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
        if line.startswith("controle:"):
            controle = line[9:].strip()
            continue
        label, vals = line.rsplit("|", 1)
        cells = [Cell(x) for x in vals.split()]
        if len(cells) != len(cur["cols"]):
            raise ValueError(f"{path.name}:{n} row {label!r}: {len(cells)} values for {len(cur['cols'])} columns")
        if cur["cols"] is None:
            raise ValueError(f"{path.name}:{n}: no cols: line")
        cur["rows"].append({"label": label.strip(), "region": region, "controle": controle,
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
FAIL_NOTES = {
    "meteo_rainfall_season": "Every failure was re-read on a zoomed native-resolution crop of the line; printed "
                             "values kept. sgt1930 p. 262 Menzel-Temime: Printemps (172.6) is printed identical "
                             "to Hiver, the Année implies 66.9, so the Printemps cell is flagged `total_mismatch`. "
                             "p. 265 Djebel-Mansour (Sainte-Gilberte) (540.8 vs 510.8, a difference of exactly "
                             "30: one digit misprinted, cell not identifiable). Small differences (p. 260 "
                             "Aïn-Sebaâ -0.6, p. 263 Le Kef I +0.2, p. 265 Sainte Maurice de Djebibina +0.1, "
                             "Kundar +0.9): printed inconsistencies, every digit clear.",
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
                       "and Mactar (68 vs 78): every month re-read on zoomed crops; printed inconsistencies.",
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
                              "as Année minus the other months) cannot fail their check by construction.",
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
             "year": "Year in which the agricultural year (September-August) ends (1929-1930 = 1930); NA for "
                     "the normals.",
             "region": "Natural-region heading as printed in part a) (e.g. `Kroumirie`, `Mogods`, `Golfe de "
                       "Tunis`, `Région de Dakla`), without roman numerals, in title case with accents restored "
                       "as in the solar-year tables. The part a) regions differ from the part b) regions.",
             "controle": "Empty (part a) has no contrôle headings).",
             "station": "Rain-gauge station exactly as printed.",
             "period": "`1929-1930` for the observations of the agricultural year; `1901-1925` for the printed "
                       "normal annual rainfall.",
             "season": "`autumn`, `winter`, `spring`, `summer`, or `year` (normal annual rainfall).",
             "season_fr": "Column heading as printed.",
             "measure": "`rainfall` (total rainfall of the season) or `rainfall_mean` (normal annual rainfall, "
                        "mean of the period).",
             "measure_fr": "Table heading as printed.",
             "unit": "`mm` (millimètres, one decimal).",
             "value": "Value as printed; NA when nothing was printed (`—`).",
             "obs": "`traces` (\"gouttes\": value 0); `no_observation` (\"—\", value NA). Empty otherwise.",
             "flag": "Empty, `not_applicable` (dash printed: see `obs`), `illegible`."}),
    "meteo_rainfall_monthly": dict(
        title_fr="Relevé pluviométrique : hauteur totale de pluie en millimètres et dixièmes, par station et par mois",
        title_en="Rainfall record: total rainfall in millimetres by station and month (solar year)", idx=0),
    "meteo_rain_days": dict(
        title_fr="Relevé pluviométrique : nombre de jours de pluie, par station et par mois",
        title_en="Rainfall record: number of rainy days by station and month (solar year)", idx=1),
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
               "two-page spreads (left page: stations and Millimètres de pluie by month; right page: the rest of "
               "the mm and Total, then Nombre de jours by month and Total; the exact split column is to be "
               "confirmed when transcribing), key \"Signes conventionnels : — pas d'observation; × ...\" across "
               "the top of the spread; NOT YET TRANSCRIBED. f844|f845 (p. 286-287) *c) Données climatologiques "
               "essentielles fournies par les principales régions tunisiennes (année 1930)*, one spread: localités "
               "grouped by region, Pluies (millimètres, nombre de jours), Température moyenne du mois le plus chaud "
               "/ le plus froid (moyennes, maxima, minima), Température absolue (maxima, minima, with dates), "
               "nombre de jours au cours de l'année pendant lesquels le vent a soufflé de N, NE, E, SE, S, SW, W, "
               "NW, calme, vent dominant; footnotes (1)-(3) on missing months; NOT YET TRANSCRIBED. f846-f849 "
               "(p. 288-291) *Pluies moyennes mensuelles, par saison et annuelles pour les périodes : 1926-1930 et "
               "1901-1930*, two lines (1926-1930, 1901-1930) per station (Tabarka ... Tatahouine), columns "
               "Septembre-Août, Automne, Hiver, Printemps, Eté, Année; NOT YET TRANSCRIBED (means only: "
               "meteo_means).",
    "sgt1929": "f284-f312 Météorologie, parts a)-d) (views per part not yet surveyed page by page).",
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
        p = TR / f"{PREFIX}_{ed}.txt"
        if p.exists():
            secs += parse(p, ed)
    recs = {k: [] for k in TABLES}
    for s in secs:
        if s["table"] == "season":
            recs["meteo_rainfall_season"] += season_cells(s)
        if s["table"] == "rain":
            mm, d = rain_cells(s)
            recs["meteo_rainfall_monthly"] += mm
            recs["meteo_rain_days"] += d
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


REMAINING = ("Transcribed: sgt1936 f123-f144 (complete), sgt1935 f166-f183 (complete) and sgt1930 part a) "
             "f818-f825 (complete). NOT YET TRANSCRIBED: sgt1930 parts b) f826-f843, c) f844-f845 and d) "
             "f846-f849; every Météorologie page of sgt1929 (f284-f312), sgt1928 (f806-f835), sgt1927 "
             "(f282-f307), sgt1926 (f819-f845), sgt1925 (f309-f334), sgt1924 (f1247-f1268), sgt1923 (f745-f764) and "
             "sgt1922 (f255-f273). Tables meteo_climate and meteo_means are designed but have no rows yet.")


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
