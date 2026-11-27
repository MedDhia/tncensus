#!/usr/bin/env python3
"""Public works chapter (*Travaux publics*: chapter IX up to sgt1935, chapter VIII in sgt1936 and sgt1939) of the
Statistique générale de la Tunisie, 12 editions sgt1922-sgt1939.

Tables: railways (operating results by network, financial results), roads, hydraulic works, mining permits,
mines and mine exports, phosphates, ores, iron ore, and sgt1939's vehicles / other transport / airport.

  python3 extract_publicworks.py check   parse the transcriptions, run every check, print failures
  python3 extract_publicworks.py build   ... and write csv/publicworks_*.csv, their .md notes,
                                         csv/publicworks_survey.md and csv/publicworks_validation.json

Source of truth: transcribed/publicworks_<edition>.txt (format in yb_tables.py). The roads table is a yearly
series printed for overlapping ten-year windows (SPEC_ADDENDUM rule 4: each year from the latest edition printing
it, every other printing compared cell by cell). It prints no totals; the checks are that the cumulative series
never decrease within a printing.
"""
import sys
from collections import defaultdict
from decimal import Decimal

from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parent))  # shared helper yb_tables.py
from yb_tables import (COMMON, EDITIONS, ORDER, OUT, TR, Checks, coverage_lines, parse, ssum, where, write_csv,
                       write_notes, write_validation)

CHAPTER = "Travaux publics"
SCRIPT = "extract_publicworks.py"
PREFIX = "publicworks"

# Views of the chapter (chapter title .. last view before the next chapter), confirmed on the images and the
# page headings.
CHAPTER_VIEWS = {
    "sgt1922": (173, 184), "sgt1923": (663, 674), "sgt1924": (1159, 1170), "sgt1925": (199, 210),
    "sgt1926": (755, 766), "sgt1927": (217, 228), "sgt1928": (741, 752), "sgt1929": (219, 230),
    "sgt1930": (753, 764), "sgt1935": (117, 126), "sgt1936": (84, 93), "sgt1939": (83, 92),
}

ROAD_M = {"road_km": ("roads", "Routes", "length_built_cumulative", "Longueurs cumulées construites", "km"),
          "road_fr": ("roads", "Routes", "expenditure_cumulative", "Dépenses cumulées", "francs"),
          "track_fr": ("tracks", "Pistes", "expenditure_cumulative", "Dépenses cumulées", "francs")}

HYD = {  # section: (work, work_fr)
    "water": ("drinking_water", "a) Alimentation en eau potable des centres habités"),
    "irrigation": ("agricultural_hydraulics", "b) Aménagement d'hydraulique agricole"),
    "wells": ("artesian_wells", "Forages artésiens"),
    "sanitation": ("sanitation", "Installation d'assainissement des centres habités"),
}
HYD_M = {("water", "m3"): ("daily_flow_cumulative", "Débits moyens journaliers cumulés (mètres cubes)", "m3_per_day"),
         ("irrigation", "m3"): ("daily_volume_cumulative",
                                "Volume utilisable des eaux d'irrigation permanente (m3 journaliers)", "m3_per_day"),
         ("wells", "ls"): ("flow", "Débit en litres par seconde", "litres_per_second"),
         "fr": ("expenditure_cumulative", "Dépenses cumulées", "francs")}

PERMIT_M = {"requested": "Permis demandés", "granted": "Permis délivrés", "current": "Permis en cours"}
EXPORT_M = {"mines": ("mines_worked", "Nombre de mines exploitées", "count"),
            "value": ("export_value", "Valeur du minerai exporté au cours du marché fob Tunis", "francs")}
DETAIL_M = {"conc_n": ("concessions_number", "Mines concédées : nombre", "count"),
            "conc_ha": ("concessions_area", "Mines concédées : superficie", "hectares"),
            "expl_n": ("worked_number", "Mines exploitées : nombre", "count"),
            "expl_ha": ("worked_area", "Mines exploitées : superficie", "hectares"),
            "workers": ("workers", "Ouvriers", "count"),
            "days": ("working_days", "Journées de travail", "count"),
            "prod_t": ("production", "Production", "tonnes"),
            "value": ("value", "Valeur", "francs")}
MINERAL = {"Fer": "iron", "Plomb": "lead", "Zinc": "zinc", "Cuivre": "copper", "Manganèse": "manganese",
           "Lignites": "lignite", "Mixtes": "mixed", "Mercure": "mercury", "Fluorine": "fluorite",
           "Plomb-Zinc": "lead_zinc", "Plomb-Zinc-Mercure": "lead_zinc_mercury",
           "Plomb-Zinc-Mercure-Fluorine": "lead_zinc_mercury_fluorite", "Totaux": "TOTAL"}
PHOS_M = {"t": ("tonnage", "Tonnage", "tonnes"), "fr": ("value", "Valeur", "francs")}
PWORK_M = {"state": ("workings_state_land", "Exploitations en terrains domaniaux", "count"),
           "private": ("workings_private_land", "Exploitations en terrains privés", "count"),
           "workers": ("workers", "Ouvriers", "count"), "days": ("working_days", "Journées de travail", "count"),
           "prod_t": ("production", "Production", "tonnes"), "value": ("value", "Valeur", "francs")}
ORE_M = {"mines": ("", "mines_conceded", "Nombre des mines concédées", "count"),
         "t_zinc": ("zinc", "tonnage", "Tonnage : zinc", "tonnes"),
         "t_lead": ("lead", "tonnage", "Tonnage : plomb", "tonnes"),
         "t_mixed": ("mixed", "tonnage", "Tonnage : mixtes", "tonnes"),
         "t_mercury": ("mercury", "tonnage", "Tonnage : mercure (en kilogs)", "kg"),
         "value_total": ("", "value_total", "Valeur totale au port d'embarquement (en francs)", "francs"),
         "v_zinc": ("zinc", "value", "Valeur des minerais : zinc", "francs"),
         "v_lead": ("lead", "value", "Valeur des minerais : plomb", "francs"),
         "v_mixed": ("mixed", "value", "Valeur des minerais : mixtes", "francs"),
         "v_mercury": ("mercury", "value", "Valeur des minerais : mercure", "francs"),
         "p_zinc": ("zinc", "average_price", "Cours moyens : zinc", None),
         "p_lead": ("lead", "average_price", "Cours moyens : plomb", None)}
IRON_M = {"t": ("tonnage", "Tonnage", "tonnes"), "fr": ("value", "Valeur", "francs")}

CHK = Checks()
OUTNAME = "publicworks_roads"
FAILREC = []


def dl(sec):
    return [r for r in sec["rows"] if "cells" in r and r["label"] not in ("Totaux", "Total")]


def row(sec, label):
    for r in sec["rows"]:
        if r["label"] == label:
            return r["cells"]
    return None


def chk_cumulative(out, sec):
    """cumulative series: each year >= the previous year, every column"""
    rows = dl(sec)
    for c in sec["cols"]:
        for a, b in zip(rows, rows[1:]):
            x, y = a["cells"][c].value, b["cells"][c].value
            if x is None or y is None:
                continue
            CHK.n[out] += 1
            if y < x:
                CHK.fail[out].append(f"{where(sec)} {c}: {b['label']} ({y}) below {a['label']} ({x}) in a "
                                     f"cumulative series")


def chk_roads(sec):
    chk_cumulative(OUTNAME, sec)


def base(sec, year):
    return {"census": sec["ed"], "table_id": sec["table"], "gallica_ark": sec["ark"], "source_page": sec["page"],
            "gallica_view": sec["view"], "year": year}


def mk(sec, cell, year, **dims):
    return dict(base(sec, year), **dims, value=cell.value, flag=cell.flag)


def cells_roads(sec):
    out = []
    for r in dl(sec):
        for c in sec["cols"]:
            w, wfr, m, mfr, unit = ROAD_M[c]
            out.append(mk(sec, r["cells"][c], int(r["label"]), work=w, work_fr=wfr, measure=m, measure_fr=mfr,
                          unit=unit))
    return out


def cells_hydraulics(sec):
    out = []
    w, wfr = HYD[sec["table"]]
    for r in dl(sec):
        for c in sec["cols"]:
            m, mfr, unit = HYD_M[c] if c == "fr" else HYD_M[(sec["table"], c)]
            y, moved = ore_year_of(sec, r["label"], c)
            rec = mk(sec, r["cells"][c], y, work=w, work_fr=wfr, measure=m, measure_fr=mfr, unit=unit)
            if moved and not rec["flag"]:
                rec["flag"] = "row_realigned"
            out.append(rec)
    return out


def cells_simple(mapping):
    def f(sec):
        out = []
        for r in dl(sec):
            for c in sec["cols"]:
                v = mapping[c]
                if isinstance(v, str):
                    m, mfr, unit = c, v, "count"
                else:
                    m, mfr, unit = v
                out.append(mk(sec, r["cells"][c], int(r["label"]), measure=m, measure_fr=mfr, unit=unit))
        return out
    return f


def cells_detail(sec):
    out = []
    y = int(sec["year"])
    for r in sec["rows"]:
        if "cells" not in r or r["label"] == "Totaux":
            continue
        mineral = MINERAL[r["label"]]
        for c in sec["cols"]:
            cell = r["cells"][c]
            if cell.flag == "not_applicable":
                continue   # nothing printed in this cell (bracketed figure stored on the group line)
            m, mfr, unit = DETAIL_M[c]
            if mineral == "mercury" and c == "prod_t":
                unit = "kg"
            out.append(mk(sec, cell, y, mineral=mineral, mineral_fr=r["label"], measure=m, measure_fr=mfr,
                          unit=unit))
    return out


def chk_detail(sec):
    out = "publicworks_mines_detail"
    t = row(sec, "Totaux")
    vals = [r["cells"]["value"].value for r in dl(sec) if r["cells"]["value"].value is not None]
    CHK.n[out] += 1
    got = sum(vals, Decimal(0))
    if got != t["value"].value:
        CHK.fail[out].append(f"{where(sec)} value: Totaux = sum of the minerals: cells give {got}, printed "
                             f"{t['value'].value} (difference {t['value'].value - got})")


def ore_year_of(sec, label, col):
    y = int(label)
    shift = sec.get("shift", "")
    if shift and col in shift.split(",") and y <= int(sec.get("shift_to", 0)):
        return y - 1, True
    return y, False


def cells_ores(sec):
    out = []
    for r in dl(sec):
        for c in sec["cols"]:
            cell = r["cells"][c]
            if cell.flag == "not_applicable":
                continue
            y, moved = ore_year_of(sec, r["label"], c)
            ore, m, mfr, unit = ORE_M[c]
            if unit is None:
                unit = "pounds_sterling_per_tonne" if y <= 1930 else "francs_per_tonne"
            rec = mk(sec, cell, y, ore=ore, measure=m, measure_fr=mfr, unit=unit, _printed_line=r["label"])
            if moved and not rec["flag"]:
                rec["flag"] = "row_realigned"
            out.append(rec)
    return out


def chk_ores_all(recs):
    """value_total = zinc + lead (+ mixtes) values, per printing, after realignment"""
    out = "publicworks_ores"
    by = defaultdict(dict)
    for r in recs:
        by[(r["census"], r["year"])][(r["ore"], r["measure"])] = r
    for (ed, y), d in sorted(by.items(), key=lambda kv: (ORDER.index(kv[0][0]), kv[0][1])):
        tot = d.get(("", "value_total"))
        parts = [d.get((o, "value")) for o in ("zinc", "lead")]
        if tot is None or any(p is None for p in parts) or tot["value"] is None:
            continue
        extra = [d[(o, "value")] for o in ("mixed", "mercury") if (o, "value") in d]
        vals = [p["value"] for p in parts + extra]
        if any(v is None for v in vals):
            continue
        CHK.n[out] += 1
        got = sum(vals, Decimal(0))
        if got != tot["value"]:
            CHK.fail[out].append(f"{ed} p.{tot['source_page']} (f{tot['gallica_view']}) {y}: value_total = zinc + "
                                 f"lead + mixtes/mercure values: cells give {got}, printed {tot['value']} "
                                 f"(difference {tot['value'] - got})")


def select(recs, key):
    """Rule 4: latest edition printing the cell, an aligned printing before a realigned one."""
    by = defaultdict(list)
    for r in recs:
        by[tuple(r[k] for k in key)].append(r)
    kept, n, diffs = [], 0, []
    for k, rs in by.items():
        rs.sort(key=lambda r: ORDER.index(r["census"]))
        legible = [r for r in rs if r["value"] is not None]
        aligned = [r for r in legible if r["flag"] != "row_realigned"]
        last = (aligned or legible or rs)[-1]
        for r in rs:
            if r is last or r["value"] is None:
                continue
            n += 1
            if r["value"] != last["value"]:
                diffs.append((k, r["census"], r["value"], last["census"], last["value"]))
        kept.append(last)
    return kept, n, diffs


# ----------------------------------------------------------------- railways and other transport

RAIL_M = {
    "len_km": ("average_length_worked", "Longueur moyenne exploitée", "km"),
    "rec_day": ("receipts_per_day", "Recettes moyennes par jour", "francs"),
    "rec_gv": ("receipts_fast_goods_passengers", "Recettes de la Grande Vitesse", "francs"),
    "rec_pv": ("receipts_slow_goods", "Recettes de la Petite Vitesse", "francs"),
    "rec_total": ("receipts_total", "Recette totale", "francs"),
    "rec_km": ("receipts_per_km_year", "Recette totale par kilomètre et par an", "francs"),
    "rec_train_km": ("receipts_per_train_km", "Recette par kilomètre de train", "francs"),
    "pass_n": ("passengers", "Nombre de voyageurs transportés", "count"),
    "pass_prod": ("passenger_receipts", "Trafic en voyageurs : produit total", "francs"),
    "pass_km": ("passenger_average_journey", "Parcours moyen d'un voyageur", "km"),
    "pass_avg": ("receipts_per_passenger", "Produit moyen d'un voyageur", "francs"),
    "pass_tariff": ("passenger_tariff_per_km", "Tarif kilométrique moyen (voyageurs)", "francs"),
    "goods_t": ("goods_tonnes", "Nombre de tonnes transportées (Petite Vitesse)", "tonnes"),
    "goods_prod": ("goods_receipts", "Trafic en marchandises : produit total", "francs"),
    "goods_km": ("goods_average_haul", "Parcours moyen d'une tonne", "km"),
    "goods_avg": ("receipts_per_tonne", "Produit moyen d'une tonne", "francs"),
    "goods_tariff": ("goods_tariff_per_km", "Tarif kilométrique moyen (marchandises)", "francs"),
    "train_km": ("train_km", "Parcours des trains", "km"),
}
COMPANY = {"bone_guelma": "Compagnie Bône-Guelma / Compagnie Fermière des Chemins de fer tunisiens",
           "gafsa": "Compagnie des phosphates et du chemin de fer de Gafsa / Compagnie Sfax-Gafsa",
           "tgm": "Chemins de fer électriques Tunis-Goulette-Marsa"}
NETWORK = {"medjerdah": "Réseau de la Medjerdah",
           "djedeida_bizerte": "Ligne de Djedeida à Bizerte et embranchements",
           "normal_gauge": "Réseau à voie normale", "narrow_gauge": "Réseau à voie étroite",
           "sfax_gafsa_metlaoui": "Ligne de Sfax à Gafsa et à Metlaoui (voie étroite)",
           "metlaoui_tozeur": "Ligne de Metlaoui à Tozeur (voie étroite)",
           "graiba_gabes": "Ligne de Graïba à Gabès (voie étroite)",
           "mining_branches": "Embranchements miniers",
           "tunis_goulette_marsa": "Ligne de Tunis-Goulette-Marsa"}


def cells_rail(sec):
    out = []
    for r in dl(sec):
        m, mfr, unit = RAIL_M[r["label"]]
        for c in sec["cols"]:
            rec = mk(sec, r["cells"][c], int(c), company=sec["company"], company_fr=COMPANY[sec["company"]],
                     network=sec["network"], network_fr=NETWORK[sec["network"]], measure=m, measure_fr=mfr,
                     unit=unit)
            if sec.get("realigned") and not rec["flag"]:
                rec["flag"] = "row_realigned"
            out.append(rec)
    return out


def _dec(x):
    e = x.as_tuple().exponent
    return -e if e < 0 else 0


def chk_rail(sec):
    out = "publicworks_railways"
    g = {r["label"]: r["cells"] for r in dl(sec)}
    for c in sec["cols"]:
        val = lambda k: g[k][c].value if k in g else None
        gv, pv, tot = val("rec_gv"), val("rec_pv"), val("rec_total")
        if None not in (gv, pv, tot):
            CHK.eq(out, f"{where(sec)} {sec['network']} {c}: recette totale = G.V. + P.V.", gv + pv, tot)
        # ratios (printed rounded): recette par km, par km de train, produit moyen voyageur / tonne
        for num, den, tgt in (("rec_total", "len_km", "rec_km"), ("rec_total", "train_km", "rec_train_km"),
                              ("pass_prod", "pass_n", "pass_avg"), ("goods_prod", "goods_t", "goods_avg")):
            a, b, t = val(num), val(den), val(tgt)
            if None in (a, b, t) or not b:
                continue
            q = a / b
            tol = Decimal(1).scaleb(-_dec(t)) + abs(t) * Decimal("0.01")
            CHK.eq(out, f"{where(sec)} {sec['network']} {c}: {tgt} = {num} / {den} (printed rounding, 1 %)",
                   q.quantize(Decimal(1).scaleb(-_dec(t))), t, tol=tol)


FIN_M = {
    "receipts": ("annual_receipts", "Recettes annuelles"),
    "shortfall": ("annual_shortfall", "Insuffisances annuelles"),
    "subsidy": ("french_government_subsidy", "Subvention du Gouvernement français"),
    "reserve_payment": ("reserve_fund_payment", "Versements annuels au fonds de réserve de 750.000 fr."),
    "reserve_fund": ("reserve_fund_31_dec", "Montant du fonds de réserve au 31 décembre de chaque année"),
    "djedeida": ("surplus_djedeida_bizerte", "Djedeida à Bizerte et embranchements"),
    "narrow": ("surplus_narrow_gauge", "Réseau à voie étroite"),
    "total": ("surplus_total", "Totaux annuels"),
    "cumulative": ("surplus_cumulative", "Total des excédents versés"),
    "profit": ("operating_profit", "Bénéfice d'exploitation"),
    "deficit": ("operating_deficit", "Déficit de l'exploitation"),
    "remuneration": ("company_remuneration", "Rémunération de la Compagnie"),
    "tr_works": ("treasury_complementary_works", "Versements au Trésor pour travaux complémentaires"),
    "tr_control": ("treasury_control_costs", "Versements au Trésor pour frais de contrôle"),
    "tr_interest": ("treasury_financial_charges", "Versements au Trésor pour intérêts des charges financières"),
    "tr_total": ("treasury_total", "Versements au Trésor : totaux"),
}
FIN_T = {"fin_medjerdah": ("medjerdah_guaranteed", "c) Ligne de la Medjerdah"),
         "fin_unguaranteed": ("unguaranteed_lines", "d) Lignes non garanties"),
         "fin_convention": ("whole_network_convention_1922",
                            "Ensemble du réseau, sous le régime institué par la Convention du 22 juin 1922")}


def cells_rail_finance(sec):
    out = []
    sch, sch_fr = FIN_T[sec["table"]]
    for r in dl(sec):
        for c in sec["cols"]:
            m, mfr = FIN_M[c]
            out.append(mk(sec, r["cells"][c], int(r["label"]), scheme=sch, scheme_fr=sch_fr, measure=m,
                          measure_fr=mfr, unit="francs"))
    return out


def chk_rail_finance(sec):
    out = "publicworks_railway_finance"
    rows = dl(sec)
    if sec["table"] == "fin_unguaranteed":
        prev = None
        for r in rows:
            c = r["cells"]
            CHK.eq(out, f"{where(sec)} {r['label']}: totaux = Djedeida + voie étroite",
                   ssum([c["djedeida"].value, c["narrow"].value]), c["total"].value)
            if prev is not None:
                CHK.eq(out, f"{where(sec)} {r['label']}: total des excédents = previous + totaux",
                       ssum([prev["cumulative"].value, c["total"].value]), c["cumulative"].value)
            prev = c
    elif sec["table"] == "fin_convention":
        for r in rows:
            c = r["cells"]
            CHK.eq(out, f"{where(sec)} {r['label']}: versements totaux = travaux + contrôle + intérêts",
                   ssum([c["tr_works"].value, c["tr_control"].value, c["tr_interest"].value]), c["tr_total"].value)


VEH = {"cars": "Voitures de tourismes, taxis, voitures de louage", "buses": "Autobus",
       "lorries": "Camions, camionnettes et voitures commerciales", "motorcycles": "Motocyclettes",
       "transfers": "Mutations de véhicules immatriculés"}
OPER = {"tgm": "Compagnie des Tramways de Tunis, réseau T.G.M.",
        "sahel": "Société tunisienne des transports automobiles du Sahel",
        "doglione": "Entreprise Doglione et Doucet"}
OPER_M = {"pass": ("passengers_thousands", "Nombre de milliers de voyageurs", "thousands"),
          "rec": ("receipts_thousand_francs", "Recettes en milliers de francs", "thousand_francs")}
AIR = {"passengers": ("passengers", "Nombre de passagers", "count"), "mail_kg": ("mail", "Poste", "kg"),
       "goods_kg": ("goods", "Marchandises", "kg"), "baggage_kg": ("baggage", "Bagages", "kg"),
       "movements": ("departures_arrivals", "Nombre de départs et d'arrivées", "count")}


def cells_transport(sec):
    out = []
    t = sec["table"]
    for r in dl(sec):
        if r["label"] == "Total":
            continue
        for c in sec["cols"]:
            if t == "vehicles":
                dims = dict(item="registered_vehicles" if r["label"] != "transfers" else "transfers",
                            item_fr="Nombre total des voitures automobiles immatriculées" if r["label"] !=
                            "transfers" else "Mutations", category=r["label"], category_fr=VEH[r["label"]],
                            unit="count")
                y = int(c)
            elif t == "airport":
                m, mfr, unit = AIR[r["label"]]
                dims = dict(item="tunis_airport", item_fr="Mouvement du port aérien de Tunis (Tunis-Carthage et "
                            "El-Aouina), transports publics", category=m, category_fr=mfr, unit=unit)
                y = int(c)
            else:
                op, mm = c.split(".")
                m, mfr, unit = OPER_M[mm]
                dims = dict(item=op, item_fr=OPER[op], category=m, category_fr=mfr, unit=unit)
                y = int(r["label"])
            out.append(mk(sec, r["cells"][c], y, **dims))
    return out


def chk_vehicles(sec):
    t = row(sec, "Total")
    for c in sec["cols"]:
        CHK.eq("publicworks_other_transport", f"{where(sec)} {c}: TOTAL = four categories",
               ssum(row(sec, k)[c].value for k in ("cars", "buses", "lorries", "motorcycles")), t[c].value)


FAIL_NOTES = {
    "publicworks_railways": "Ratio failures recur in every printing of the same year (e.g. Graïba-Gabès 1923 "
        "receipts per km 5.216 against 7.216 computed; mining branches 1921-1922 receipts per train-km), and are "
        "printed figures; total failures by 1 franc are rounding in the printed parts. Notable printed errors: "
        "sgt1929-sgt1930 Sfax-Gafsa 1929 G.V. 1.695.939 (total needs 1.685.939); sgt1935-sgt1936 narrow gauge 1934 "
        "total 37.298.535 (parts give 37.296.535); mining branches 1934 prints the 1933 P.V. receipts and "
        "passenger product again; sgt1935 Tunis-Goulette-Marsa 1934 total printed equal to the G.V. receipts; "
        "sgt1936 Metlaoui-Tozeur 1934 total 893.644 (sgt1935 393.644).",
    "publicworks_railway_finance": "1928 Trésor total 2.294.158 for parts summing to 2.294.150 (sgt1928-sgt1930); "
        "1935 total 4.998.823 for 4.998.883 (sgt1935-sgt1939).",
    "publicworks_other_transport": "1936 vehicles: the four categories sum to 28.512, TOTAL printed 28.962.",
    "publicworks_ores": "",
    "publicworks_hydraulics": "",
}
DOC = {
    "census": "edition the value is taken from: the latest edition printing that year (rule 5 tables: the edition)",
    "table_id": "transcription section",
    "gallica_ark": "Gallica volume ark (views are numbered within a volume)",
    "source_page": "printed page number",
    "gallica_view": "Gallica view (fNNNN)",
    "year": "year of the figures",
    "work": "work code (English)",
    "work_fr": "printed heading",
    "measure": "measure code (English)",
    "measure_fr": "printed column heading",
    "unit": "unit of `value`",
    "mineral": "mineral code (English); a bracketed group printed once for several minerals is coded with the "
               "joined names (e.g. `lead_zinc`)",
    "mineral_fr": "printed line heading",
    "ore": "`zinc`, `lead`, `mixed` (mixtes), `mercury`, or empty for the all-ores columns",
    "value": "printed value (» = 0)",
    "company": "railway company code", "company_fr": "company as named in the table title",
    "network": "network / line code", "network_fr": "printed column-group heading",
    "scheme": "financial scheme code", "scheme_fr": "printed table title",
    "item": "item code", "item_fr": "printed heading", "category": "category code", "category_fr": "printed line",
    "flag": "empty, or `illegible`, `not_applicable` (nothing printed), `row_realigned` (printed on the wrong "
            "line, stored on the year it belongs to), `total_mismatch`",
}

RULE4 = ("Printed for overlapping year windows: each year is taken from the **latest** edition that prints it "
         "(SPEC_ADDENDUM rule 4; `census` = that edition; an aligned printing is preferred to a realigned one); "
         "every other printing, read independently on its own page image, is compared below.")
RULE5 = ("Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, with "
         "`year`.")

TABLES = {
    "publicworks_railways": dict(
        secs=["rail"], cells=cells_rail, key=["year", "network", "measure"],
        dims=["company", "company_fr", "network", "network_fr", "measure", "measure_fr", "unit"],
        title_fr="Voies ferrées. Résultats comparés de l'exploitation des réseaux (Bône-Guelma / Compagnie Fermière, "
                 "Compagnie de Gafsa / Sfax-Gafsa, Tunis-Goulette-Marsa)",
        title_en="Railways: operating results by network and line (length, receipts, passengers, goods, train-km)",
        unit="Units: km, francs, counts and tonnes (`unit`); suggested value_type: mixed.",
        paras=["Tables a) (Bône-Guelma, from sgt1923 Compagnie Fermière des Chemins de fer tunisiens: Medjerdah and "
               "Djedeida-Bizerte to 1921, then réseau à voie normale (1) - new name of the Medjerdah and "
               "Djedeida-Bizerte networks - and réseau à voie étroite), b) (Compagnie de Gafsa, from sgt1936 "
               "Sfax-Gafsa: four lines; (1) figures supplied by the Company; frais forfaitaires per line) and "
               "Tunis-Goulette-Marsa (e) or f); sgt1935 d); not printed in sgt1936 and sgt1939). Five years per edition "
               "(sgt1922 prints 1917-1922 for the Medjerdah). From sgt1928 the layout drops the parcours moyens and "
               "tarifs kilométriques; lines printed » (parcours moyen d'un voyageur on the Fermière network from "
               "1924, averages and tariffs printed » in 1924-1927) are stored NA (`not_applicable`).",
               "Columns printed in the gutter of a spread are read where legible; cut cells are `illegible` and "
               "stored from another printing. sgt1936 heads the last two mining-branch columns 1936, 1935 in that "
               "order with the 1935 figures under 1936: stored on their years (`row_realigned`).",
               "Checks: recette totale = G.V. + P.V. (exact) and the printed ratios (recette par km et par an, par "
               "km de train, produit moyen d'un voyageur / d'une tonne) against the quotients of the printed totals "
               "(to printed rounding, 1 % tolerance). The ratios printed with a different definition fail by "
               "design (e.g. the Medjerdah receipts per km)."]),
    "publicworks_railway_finance": dict(
        secs=["fin_medjerdah", "fin_unguaranteed", "fin_convention"], cells=cells_rail_finance,
        key=["year", "scheme", "measure"], dims=["scheme", "scheme_fr", "measure", "measure_fr", "unit"],
        title_fr="Voies ferrées. Résultats financiers de l'exploitation du réseau (Bône-Guelma / Compagnie "
                 "Fermière des Chemins de fer tunisiens)",
        title_en="Railways: financial results (guaranteed Medjerdah line, unguaranteed lines, whole network under "
                 "the Convention of 22 June 1922)",
        unit="Unit: francs; value_type: francs.",
        paras=["c) Ligne de la Medjerdah and d) lignes non garanties, 1913-1921 (printed in every edition to "
               "sgt1930); NOTA: from 1922 all lines are worked by the Compagnie Fermière on actual expenses. e) "
               "Ensemble du réseau sous le régime de la Convention du 22 juin 1922, from sgt1923 (c) in sgt1935-"
               "sgt1939); the latest year of each edition is printed \"résultats provisoires\" up to sgt1928. "
               "Footnote from sgt1928: the interest line represents only the interest on sums paid from the State "
               "reserve fund for complementary works (3e Avenant du 28 avril 1928)."]),
    "publicworks_roads": dict(
        secs=["roads"], cells=cells_roads, key=["year", "work", "measure"],
        dims=["work", "work_fr", "measure", "measure_fr", "unit"],
        title_fr="Routes et pistes. Longueurs construites et dépenses faites cumulées",
        title_en="Roads and tracks: cumulative length built and cumulative expenditure",
        unit="Units: kilometres (`unit` = `km`) and francs (`francs`); suggested value_type: mixed.",
        paras=["sgt1922-sgt1924 title the table *Routes et pistes* and print three columns (routes: longueurs "
               "cumulées construites, kilomètres; dépenses cumulées, francs; pistes: dépenses cumulées, francs); "
               "from sgt1925 the title is *Routes* and the pistes column is dropped. The figures are cumulative. "
               "Not printed in sgt1935, sgt1936, sgt1939.",
               "sgt1929 prints for 1929 5.525 km and 106.497.742 francs, the figures that sgt1930 prints for 1930; "
               "sgt1930 prints 1929 as 5.475 km and 102.316.240 francs (kept, latest edition)."]),
    "publicworks_hydraulics": dict(
        secs=["water", "irrigation", "wells", "sanitation"], cells=cells_hydraulics,
        key=["year", "work", "measure"], dims=["work", "work_fr", "measure", "measure_fr", "unit"],
        title_fr="Travaux hydrauliques. Alimentation en eau potable, hydraulique agricole, forages artésiens, "
                 "assainissement",
        title_en="Hydraulic works: drinking water supply, agricultural hydraulics, artesian wells and sanitation "
                 "(cumulative flows and expenditure)",
        unit="Units: m3 per day, litres per second and francs (`unit`); suggested value_type: mixed.",
        paras=["Four small tables printed side by side: a) Alimentation en eau potable des centres habités (débits "
               "moyens journaliers cumulés, m3; dépenses cumulées) and b) Aménagement d'hydraulique agricole "
               "(volume utilisable des eaux d'irrigation permanente, m3 journaliers; dépenses cumulées), "
               "sgt1922-sgt1928 only; c) Forages artésiens (débit en litres par seconde; dépenses cumulées) and d) "
               "Installation d'assainissement des centres habités (dépenses cumulées), sgt1922-sgt1935 (lettered "
               "a) and b) from sgt1929). Not printed in sgt1936 and sgt1939.",
               "Printed oddities, kept as printed: drinking water 1927 is printed 1.144.660 m3 (sgt1927, sgt1928; "
               "1926 141.011, 1928 1.803.442), a jump the expenditure does not show. sgt1935 prints the "
               "artesian-well flows one line too low for 1926-1931 (its 1926 = 1.396 is sgt1930's 1925, ..., its "
               "1931 = 1.722 is sgt1930's 1930), and sgt1928-sgt1935 print 1927 as 1.451 l/s (sgt1927: 1.564): "
               "listed in the overlap differences below."]),
    "publicworks_mining_permits": dict(
        secs=["permits"], cells=cells_simple(PERMIT_M), key=["year", "measure"],
        dims=["measure", "measure_fr", "unit"],
        title_fr="Industrie minière. Mines : a) Permis de recherches demandés, délivrés et en cours",
        title_en="Mining: prospecting permits requested, granted and current",
        unit="Unit: number of permits; value_type: count.",
        paras=["Printed sgt1922-sgt1930 (not in sgt1935, sgt1936, sgt1939). No totals. sgt1924 prints the 1924 "
               "permits en cours \"6.2\" with a broken middle digit, read 652; every later edition prints 652."]),
    "publicworks_mines_exports": dict(
        secs=["mines_exports"], cells=cells_simple(EXPORT_M), key=["year", "measure"],
        dims=["measure", "measure_fr", "unit"],
        title_fr="Industrie minière. Mines exploitées et valeur globale des produits exportés",
        title_en="Mining: number of mines worked and value of the ore exported (fob Tunis)",
        unit="Units: count and francs; suggested value_type: mixed.",
        paras=["Printed in every edition. The value of the latest year is not the value of production of the "
               "*Renseignements généraux sur les mines* (it equals it only in sgt1922-sgt1923 and sgt1930)."]),
    "publicworks_mines_detail": dict(
        secs=["mines_detail"], cells=cells_detail, key=["census", "mineral", "measure"], rule5=True,
        dims=["mineral", "mineral_fr", "measure", "measure_fr", "unit"],
        title_fr="Industrie minière. Renseignements généraux sur les mines (Exploitations minières)",
        title_en="Mining: concessions, mines worked, workers, working days, production and value by mineral",
        unit="Units: count, hectares, tonnes (mercury in kg) and francs; suggested value_type: mixed.",
        paras=["Printed once per edition for the edition year. Lead and zinc (and from sgt1936 mercury, in sgt1939 "
               "also fluorite) share one bracketed figure for concessions, mines worked, workers and working days: "
               "it is stored once on a group line (`mineral` = `lead_zinc`, ...); their production and value are "
               "printed per mineral (sgt1935 prints one bracketed production and value for lead and zinc). The "
               "Totaux of the value column is a check. Footnotes: Manganèse (1) permis d'exploitation; sgt1922 "
               "Lignites (2) dont 1 permis d'exploitation; from sgt1935 \"Par mines exploitées, il faut comprendre "
               "mines productives\". Lines printed with » throughout (e.g. Mixtes in sgt1928) are stored as 0."]),
    "publicworks_phosphates": dict(
        secs=["phosphates"], cells=cells_simple(PHOS_M), key=["year", "measure"],
        dims=["measure", "measure_fr", "unit"],
        title_fr="Phosphates de chaux. a) Tonnage et valeur des produits transportés (mine à quai)",
        title_en="Calcium phosphates: tonnage and value carried (mine to quay)",
        unit="Units: tonnes and francs; suggested value_type: mixed.",
        paras=["Printed in every edition (ten years to sgt1930, five from sgt1935). sgt1928 and later print 1927 as "
               "228.000.000 francs (sgt1927: 328.000.000)."]),
    "publicworks_phosphate_works": dict(
        secs=["phosphate_works"], cells=cells_simple(PWORK_M), key=["year", "measure"],
        dims=["measure", "measure_fr", "unit"],
        title_fr="Phosphates de chaux. b) Renseignements généraux sur les exploitations de phosphates",
        title_en="Calcium phosphates: workings on state and private land, workers, working days, production, value",
        unit="Units: count, tonnes, francs; suggested value_type: mixed.",
        paras=["Printed for five years in every edition."]),
    "publicworks_ores": dict(
        secs=["ores"], cells=cells_ores, key=["year", "ore", "measure"],
        dims=["ore", "measure", "measure_fr", "unit"],
        title_fr="Minerais. a) Tonnage et valeur des minerais transportés (mine à quai)",
        title_en="Zinc, lead and mixed ores (from 1936 mercury): mines conceded, tonnage, value and average prices",
        unit="Units: count, tonnes (mercury kg), francs, average prices in pounds sterling per tonne to 1930 and "
             "francs per tonne from 1931; suggested value_type: mixed.",
        paras=["Every printing of 1918 (sgt1922-sgt1927) gives a total value of 14.077.870 for zinc 1.046.520 + lead "
               "18.031.350 = 19.077.870 (printed error, recurring). Columns mixtes from sgt1925 (» before 1925). Average prices printed » in 1917-1919 and 1921 (no "
               "quotation): stored NA (`not_applicable`). sgt1930 1930 footnote (1) on the 58 mines: 3 concessions "
               "ont disparu par fusion avec des concessions voisines; sgt1935-sgt1939 footnote (1): from 1931 only "
               "the concessions of the 3rd group (lead, zinc or both) are counted; cours moyen de la Livre: 89 fr. 14.",
               "Misprinted alignment in sgt1935, sgt1936 and sgt1939 (same standing type): the columns mines, zinc "
               "tonnage, mixtes tonnage, zinc value and mixtes value are printed one line too low on the lines up "
               "to 1934, while lead, total value and prices are aligned (the values printed on their lines "
               "1926-1931 are sgt1930's 1925-1930; the 1931 total 11.120.000 = 120.000 printed on the 1932 line + "
               "11.000.000; footnote (1) \"en 1931\" sits on the 50 printed on the 1932 line). The script stores "
               "those cells one year earlier (`row_realigned`); the line 1935 is taken as printed (the line 1936 "
               "of sgt1936 is aligned, agreeing with that edition's mines table). Consequently year 1934 has no "
               "mines / zinc values from these printings, and the 1935 check fails by 60.000 (zinc value 60.000 "
               "on the 1935 line), whichever year it is attached to. From sgt1936 the mixtes columns are headed "
               "\"mercure (en kilogs)\" from 1933 (no figures 1933-1935)."]),
    "publicworks_other_transport": dict(
        secs=["vehicles", "other_transport", "airport"], cells=cells_transport, key=["year", "item", "category"],
        dims=["item", "item_fr", "category", "category_fr", "unit"],
        title_fr="Voitures automobiles immatriculées ; Autres transports publics ; Mouvement du port aérien de Tunis",
        title_en="Registered motor vehicles, other public transport operators and Tunis airport traffic (sgt1939)",
        unit="Units: count, thousands, thousand francs, kg (`unit`); suggested value_type: mixed.",
        paras=["Printed in sgt1939 only (f88-f89): motor vehicles registered at 31 December 1936-1939 by category "
               "(TOTAL used as check) and transfers of registered vehicles; other public transport 1938-1939 "
               "(thousands of passengers and of francs; no figures for the Tunisienne Automobile Transports, "
               "autonomous since the end of the Convention tripartite, 1 January 1938); Tunis airport "
               "(Tunis-Carthage and El-Aouina bases, public transport) 1937-1939."]),
    "publicworks_iron_ore": dict(
        secs=["iron_ore"], cells=cells_simple(IRON_M), key=["year", "measure"],
        dims=["measure", "measure_fr", "unit"],
        title_fr="Minerais. b) Tonnage et valeur des minerais de fer transportés (mine à quai)",
        title_en="Iron ore: tonnage and value carried (mine to quay)",
        unit="Units: tonnes and francs; suggested value_type: mixed.",
        paras=["Printed in every edition. In sgt1922-sgt1924 the values are printed slightly below their year "
               "labels; aligned by order (in sgt1922 the last line equals the Fer line of the mines table). Ore "
               "carried is not the same as ore produced: from 1923 the figures differ from the Fer line of the "
               "mines table."]),
}

SURVEY = {
    "sgt1922": "f173 chapter IX title (Travaux publics); f174|f175 Voies ferrées a) résultats comparés de "
               "l'exploitation du réseau tunisien de la Compagnie Bône-Guelma (1918-1922: réseau de la Medjerdah, "
               "ligne de Djedeida à Bizerte et embranchements, réseau à voie normale, réseau à voie étroite); "
               "f176|f177 b) résultats comparés de l'exploitation du réseau de la Compagnie de Gafsa (1918-1922: "
               "Sfax-Gafsa-Metlaoui, Metlaoui-Tozeur, Graïba-Gabès, embranchements miniers); f178 c) résultats "
               "financiers du réseau Bône-Guelma, ligne de la Medjerdah (1913-1922), d) lignes non garanties "
               "(1913-1922); f179 e) chemins de fer électriques Tunis-Goulette-Marsa (1918-1922); f180 Routes et "
               "pistes, longueurs construites et dépenses cumulées (1913-1922) , Travaux hydrauliques "
               "a) alimentation en eau potable des centres habités, b) aménagement d'hydraulique agricole "
               "(1913-1922); f181 c) forages artésiens, d) installation d'assainissement des centres habités "
               "(1913-1922), Industrie minière: a) permis de recherches, b) mines exploitées et valeur des "
               "produits exportés (1913-1922); f182 c) renseignements généraux sur les mines (by mineral), "
               "Phosphates de chaux a) tonnage et valeur transportés (1913-1922), b) renseignements généraux sur "
               "les exploitations de phosphates; f183 Minerais a) tonnage et valeur des minerais transportés "
               "(zinc, plomb; 1913-1922), b) minerais de fer (1913-1922); f184 blank. f185 = chapter X Finances.",
    "sgt1923": "f663 title; f664|f665 a) Compagnie Fermière des Chemins de fer tunisiens (1919-1923); f666|f667 b) "
               "Compagnie de Gafsa (1919-1923); f668 c) résultats financiers (Compagnie Fermière); f669 f) "
               "Tunis-Goulette-Marsa; f670 Routes et pistes (1914-1923) , travaux hydrauliques; f671 "
               "c) forages artésiens, d) assainissement, industrie minière; f672 c) renseignements généraux sur les "
               "mines, phosphates; f673 minerais (1914-1923); f674 blank. f675 = chapter X.",
    "sgt1924": "f1159 title; f1160|f1161 a) (1920-1924); f1162|f1163 b) Gafsa (1920-1924); f1164 c); f1165 f) "
               "Tunis-Goulette-Marsa; f1166 Routes et pistes (1915-1924) , travaux hydrauliques; "
               "f1167 forages, assainissement, industrie minière; f1168 mines, phosphates; f1169 minerais "
               "(1915-1924); f1170 blank. f1171 = chapter X.",
    "sgt1925": "f199 title; f200|f201 a) (1921-1925); f202|f203 b) (1921-1925); f204 c); f205 f); f206 Routes "
               "(1916-1925; pistes no longer printed) , travaux hydrauliques; f207 forages, "
               "assainissement, industrie minière; f208 mines, phosphates; f209 minerais (1916-1925); f210 blank. "
               "f211 = chapter X.",
    "sgt1926": "f755 title; f756|f757 a) (1922-1926); f758|f759 b) (1922-1926; f758 nearly empty in the OCR); "
               "f760 c); f761 f); f762 Routes (1917-1926) , travaux hydrauliques; f763 forages, "
               "assainissement, industrie minière; f764 mines, phosphates; f765 minerais (1917-1926); f766 blank. "
               "f767 = chapter X.",
    "sgt1927": "f217 title; f218|f219 a) (1923-1927); f220|f221 b) (1923-1927); f222 c); f223 f); f224 Routes "
               "(1918-1927) , travaux hydrauliques; f225 forages, assainissement, industrie minière; "
               "f226 mines, phosphates; f227 minerais (1918-1927); f228 blank. f229 = chapter X.",
    "sgt1928": "f741 title; f742|f743 a) (1924-1928); f744|f745 b) (1924-1928); f746 c); f747 f); f748 Routes "
               "(1919-1928) , travaux hydrauliques; f749 forages, assainissement, industrie minière; "
               "f750 mines, phosphates; f751 minerais (1919-1928); f752 blank. f753 = chapter X.",
    "sgt1929": "f219 title; f220|f221 a) (1925-1929); f222|f223 b) (1925-1929); f224 c); f225 f); f226 Routes "
               "(1920-1929) , industrie minière; f227 travaux hydrauliques a) forages artésiens, b) "
               "assainissement; f228 mines, phosphates; f229 minerais (1920-1929); f230 blank. f231 = chapter X.",
    "sgt1930": "f753 title; f754|f755 a) (1926-1930); f756|f757 b) (1926-1930); f758 c); f759 f); f760 Routes "
               "(1921-1930) , industrie minière; f761 travaux hydrauliques; f762 mines, phosphates; "
               "f763 minerais (1921-1930); f764 blank. f765 = chapter X.",
    "sgt1935": "f117 chapter IX title; f118|f119 a) Compagnie Fermière (1931-1935; f118 row headings, the 1931 "
               "normal-gauge column in the gutter); f120|f121 b) Compagnie de Gafsa (1931-1935); f122 c) résultats "
               "financiers (Convention), d) Tunis-Goulette-Marsa (1931-1935), Routes (1926-1935); f123 travaux "
               "hydrauliques a) forages artésiens, b) assainissement (1926-1935), industrie minière (mines "
               "exploitées et valeur des produits exportés, 1926-1935); f124 b) renseignements généraux sur les mines "
               "(1935), phosphates a) and b) (1931-1935); f125 minerais a) zinc/plomb, b) fer (1926-1935); f126 "
               "blank. f127 = chapter X Finances.",
    "sgt1936": "f84 chapter VIII title (Travaux publics); f85|f86 a) Compagnie Fermière (1932-1936); f87|f88 b) "
               "Compagnie Sfax-Gafsa (1932-1936); f89 c) résultats financiers (1932-1936), a) forages artésiens "
               "(1927-1936); f90 industrie minière (1927-1936) and exploitations minières (1936); f91 phosphates a) "
               "(1932-1936) and b); f92 minerais a) (1927-1936) and b) fer; f93 blank. f94 = chapter IX Finances "
               "(f94-f99), f100 = chapter X Agriculture. No roads, no Tunis-Goulette-Marsa, no sanitation. Range 84-93 "
               "confirmed.",
    "sgt1939": "f83 chapter VIII title; f84|f85 a) Compagnie Fermière (1935-1939; the 1935 normal-gauge column cut "
               "by the binding); f86|f87 b) Compagnie Sfax-Gafsa (1935-1939); f88 c) résultats financiers "
               "(1935-1939), nombre total des voitures automobiles immatriculées (1936-1939); f89 autres transports "
               "publics (1938-1939), mouvement du port aérien de Tunis (1937-1939); f90 industrie minière (1930-1939), "
               "exploitations minières (1939); f91 phosphates; f92 minerais (1930-1939). f93 = chapter IX Finances. "
               "No roads, no hydraulic works.",
}

NOT_DONE = ("Every table of the chapter is transcribed in every edition that prints it, every cell read on "
            "native-resolution crops of the page images (whole-page views of every page from the chapter title to "
            "the next chapter title, then zoomed crops of every table). Cells cut by the binding are `illegible` "
            "(stored from another printing when one exists). Nothing printed in the chapter is left out; printed "
            "TOTAUX / TOTAL lines are used as checks only.")


def write_survey():
    L = ["# Public works chapter: survey of every edition", "",
         "Survey of the *Travaux publics* chapter (chapter IX up to sgt1935, chapter VIII in sgt1936 and sgt1939). "
         "First and last views confirmed for every edition (chapter-title pages and next chapter title, on the "
         "images or their OCR headings). Extraction: `extract_publicworks.py`.", "",
         "| edition | ark | views |", "|---|---|---|"]
    L += [f"| {e} | `{EDITIONS[e]}` | {a}–{b} |" for e, (a, b) in CHAPTER_VIEWS.items()]
    L += ["", "## Views per edition", ""] + [f"- **{e}**: {t}" for e, t in SURVEY.items()]
    L += ["", "## Tables (CSV)", "", "| CSV | sections | editions | read on the image |", "|---|---|---|---|",
         ] + [f"| `{o}` | {', '.join(sp['secs'])} | {', '.join(sp.get('_eds', []))} | every printing, cell by cell |"
               for o, sp in TABLES.items()] + ["",
          "## Coverage", "", NOT_DONE, ""]
    (OUT / "publicworks_survey.md").write_text("\n".join(L) + "\n")


def build(write=True):
    secs = []
    for ed in ORDER:
        p = TR / f"{PREFIX}_{ed}.txt"
        if p.exists():
            secs += parse(p, ed)
    for s in secs:
        t = s["table"]
        if t == "roads":
            chk_roads(s)
        elif t in HYD:
            chk_cumulative("publicworks_hydraulics", s)
        elif t == "mines_detail":
            chk_detail(s)
        elif t == "rail":
            chk_rail(s)
        elif t in FIN_T:
            chk_rail_finance(s)
        elif t == "vehicles":
            chk_vehicles(s)
    res = {}
    for out, spec in TABLES.items():
        ss = [s for s in secs if s["table"] in spec["secs"]]
        spec["_eds"] = [e for e in ORDER if any(s["ed"] == e for s in ss)]
        recs = []
        for s in ss:
            recs += spec["cells"](s)
        if out == "publicworks_ores":
            chk_ores_all(recs)
        kept, n, diffs = select(recs, spec["key"])
        order = {id(r): i for i, r in enumerate(recs)}
        kept.sort(key=lambda r: (r["year"], ORDER.index(r["census"]), order.get(id(r), 0)))
        flagged = [f"{r['census']} {r['year']} " + " / ".join(str(r.get(k, "")) for k in spec["key"][1:])
                   + f" = {r['value']} ({r['flag']})" for r in kept if r["flag"]]
        res[out] = dict(rows=len(kept), checks=CHK.n[out], failed=list(CHK.fail[out]), overlap_compared=n,
                        overlap_diffs=[list(x) for x in diffs], flagged=flagged, editions=spec["_eds"])
        if write:
            cols = COMMON + spec["dims"] + ["value", "flag"]
            write_csv(out, cols, kept)
            fl = CHK.fail[out]
            expl = []
            if fl:
                expl = [f"Every failed check below was re-read on a zoomed native-resolution crop, or recurs "
                        f"unchanged in independent readings of several editions: they are printed errors (printed "
                        f"values kept). " + FAIL_NOTES.get(out, "")]
            paras = list(spec.get("paras", [])) + expl + [
                "Survey of the whole chapter in every edition: "
                "`publicworks_survey.md`."]
            write_notes(out, CHAPTER, SCRIPT, kept, cols, {c: DOC[c] for c in cols}, spec["title_fr"],
                        spec["title_en"], paras, CHK.n[out], CHK.fail[out], n, diffs, coverage_lines(ss),
                        RULE5 if spec.get("rule5") else RULE4, spec["unit"])
    if write:
        write_validation(OUT / f"{PREFIX}_validation.json", dict(
            res, _chapter_views=CHAPTER_VIEWS, _survey=SURVEY, _not_transcribed=NOT_DONE))
        write_survey()
    return res


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    res = build(write=(mode == "build"))
    for out, d in res.items():
        print(f"{out}: {d['rows']} rows, {d['checks']} checks, {len(d['failed'])} failed, "
              f"{d['overlap_compared']} compared, {len(d['overlap_diffs'])} diffs, {len(d['flagged'])} flagged "
              f"[{' '.join(d['editions'])}]")
        for f in d["failed"]:
            print("   FAIL", f)
        for x in d["overlap_diffs"]:
            print("   DIFF", x)


if __name__ == "__main__":
    main()
