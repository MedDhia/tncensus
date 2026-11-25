#!/usr/bin/env python3
"""Health chapter (III) population tables of the Statistique générale de la
Tunisie, 12 editions 1922-1939: hospitals of Tunis (Hôpital civil français,
Hôpital Sadiki, Rabta / Ernest-Conseil, Manouba), hospitals and dispensaries of
the interior, and the "Statistique sanitaire de la ville de Tunis".

  python3 extract_health_population.py check   parse transcriptions, run every check, print failures
  python3 extract_health_population.py build   ... and write csv/health_*.csv, their .md notes
                                               and csv/health_validation.json

Source of truth: transcribed/health_pop_<edition>.txt, transcribed from the page
images (half-resolution views; native-resolution crops from
data-raw/yearbook_demography/hires.py where a digit was doubtful), with Gallica
OCR drafts as a starting point. Format: sections '@<table> view=.. page=..
[year=..|years=..]', an optional 'cols:' line, rows '[code ; ]label | v v v'.
Values carry no thousands separator, decimal commas are written '.', printed
» = 0, '.' = cell not printed, 'x' = printed » or blank where the figure was
not recorded or not split (not stored). Signs of printed differences are kept.

Year-windowed tables follow SPEC_ADDENDUM rule 4 (latest printing kept, all
printings compared; REPRINT / SOURCE_OVERRIDE below for documented exceptions);
tables printed once per edition follow rule 5. Printed totals and
"différence" columns are used for checks only. Identified misprints are listed
in CELL_FLAGS; the commentary written to each notes file is in COMMENT.
"""
import csv
import json
import re
import sys
from collections import defaultdict
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


# ----------------------------------------------------------------- parsing

def num(s):
    if s in (".", "x"):
        return None
    v = float(s)
    return int(v) if re.fullmatch(r"-?\d+", s) else v


def parse(ed):
    secs = []
    cur = None
    for line in (TR / f"health_pop_{ed}.txt").read_text().splitlines():
        line = line.rstrip()
        if not line.strip() or line.startswith("#"):
            continue
        if line.startswith("@"):
            parts = line[1:].split()
            cur = {"table": parts[0], "ed": ed, "ark": EDITIONS[ed], "rows": [], "cols": None}
            rest = " ".join(parts[1:])
            for k, v in re.findall(r"(\w+)=([^=]+?)(?=\s+\w+=|$)", rest):
                cur[k] = v.strip()
            cur["view"] = int(cur["view"])
            cur["page"] = int(cur["page"]) if cur.get("page", "").isdigit() else ""
            if "years" in cur:
                cur["years"] = [int(y) for y in cur["years"].split()]
            if "year" in cur:
                cur["year"] = int(cur["year"])
            secs.append(cur)
            continue
        if line.startswith("cols:"):
            c = line[5:].strip()
            cur["cols"] = [x.strip() for x in c.split(";")] if ";" in c else c.split()
            continue
        label, vals = line.rsplit("|", 1)
        label = label.strip()
        code = None
        if " ; " in label:
            code, label = [x.strip() for x in label.split(" ; ", 1)]
        raw = vals.split()
        vals = [num(x) for x in raw]
        if cur["cols"] and len(vals) != len(cur["cols"]):
            raise ValueError(f"{ed} {cur['table']} row {label!r}: {len(vals)} values, {len(cur['cols'])} cols")
        cur["rows"].append({"label": label, "code": code, "v": vals, "raw": raw})
    return secs


class Checks:
    def __init__(self):
        self.n = defaultdict(int)
        self.fail = defaultdict(list)

    def eq(self, topic, what, got, printed, tol=0):
        if got is None or printed is None:
            return
        self.n[topic] += 1
        if abs(got - printed) > tol + 1e-9:
            self.fail[topic].append(f"{what}: cells give {round(got, 3)}, printed {printed}")


CHK = Checks()
RECTIFIED_RULE = {}


def s(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) if xs else None


# ----------------------------------------------------------------- checks per section

def tot_label(lab):
    return re.match(r"(?i)^(totaux|total|totals?)\b", lab) is not None


def check_grid(sec, topic, row_total=True, col_total=True):
    """Last column = row total (if row_total); a TOTAUX row = column sums."""
    ed, t = sec["ed"], sec["table"]
    data = [r for r in sec["rows"] if not tot_label(r["label"]) and r["code"] != "extra"]
    tots = [r for r in sec["rows"] if tot_label(r["label"])]
    if row_total:
        for r in sec["rows"]:
            CHK.eq(topic, f"{ed} {t} row {r['label']}: cells vs row total", s(r["v"][:-1]), r["v"][-1])
    if col_total and tots:
        T = tots[-1]["v"]
        for j in range(len(T)):
            CHK.eq(topic, f"{ed} {t} column {sec['cols'][j] if sec['cols'] else j}: rows vs {tots[-1]['label']}",
                   s(r["v"][j] for r in data), T[j])


MOV_GROUPS = (("adm", "admitted"), ("rec", "discharged_recovered"), ("dth", "discharged_died"))


def check_movements(sec, topic):
    cols = sec["cols"]
    for r in sec["rows"]:
        d = dict(zip(cols, r["v"]))
        for g, _ in MOV_GROUPS + (("eoy", ""),):
            if f"{g}_t" in d:
                CHK.eq(topic, f"{sec['ed']} {sec['table']} {r['label']} {g}: m+f+c vs total",
                       s([d.get(f"{g}_m"), d.get(f"{g}_f"), d.get(f"{g}_c")]), d[f"{g}_t"])


def check_diff(sec, topic, rows=None):
    """Year columns, then 'en plus' / 'en moins' (last year minus the one before)."""
    y = sec["years"]
    n = len(y)
    a, b = (n - 1, n - 2) if y[-1] > y[-2] else (0, 1)
    for r in rows or sec["rows"]:
        v = r["v"]
        if len(v) < n + 2 or v[a] is None or v[b] is None or (v[n] is None and v[n + 1] is None):
            continue
        d = v[a] - v[b]
        plus, minus = v[n] or 0, v[n + 1] or 0
        CHK.eq(topic, f"{sec['ed']} {sec['table']} {r['label']}: difference", d, plus - minus, tol=0.011)


def check_interior(sec, topic):
    cols = sec["cols"]
    data = [r for r in sec["rows"] if not tot_label(r["label"])]
    for r in sec["rows"]:
        d = dict(zip(cols, r["v"]))
        for g in ("eur", "ind", "deu", "din", "pat", "dth"):
            if f"{g}_t" in d:
                CHK.eq(topic, f"{sec['ed']} interior {r['label']} {g}: m+f+c vs total",
                       s([d.get(f"{g}_m"), d.get(f"{g}_f"), d.get(f"{g}_c")]), d[f"{g}_t"])
        if "pat_all" in d:
            CHK.eq(topic, f"{sec['ed']} interior {r['label']}: eur+ind vs all", s([d.get("eur_t"), d.get("ind_t")]), d["pat_all"])
        if "dth_all" in d:
            CHK.eq(topic, f"{sec['ed']} interior {r['label']}: deaths eur+ind vs all", s([d.get("deu_t"), d.get("din_t")]), d["dth_all"])
    tots = [r for r in sec["rows"] if tot_label(r["label"])]
    if tots:
        for j, c in enumerate(cols):
            CHK.eq(topic, f"{sec['ed']} interior column {c}: rows vs TOTAL", s(r["v"][j] for r in data), tots[-1]["v"][j])


def check_natality(sec, topic):
    R = {r["code"]: r["v"] for r in sec["rows"]}
    check_grid({**sec, "rows": [r for r in sec["rows"] if r["code"] != "mortality_per_1000"]}, topic, col_total=False)
    for j in range(len(sec["cols"])):
        if "deaths_corrected" in R and "non_residents" in R:
            # the definition varies: 1922 subtracts only non-residents, later
            # editions also stillbirths; accept either and record which
            a = R["deaths"][j] - R["non_residents"][j]
            b = a - R["stillbirths"][j]
            got = a if a == R["deaths_corrected"][j] else b
            CHK.eq(topic, f"{sec['ed']} natality col {j}: deaths - non-residents (- stillbirths) vs rectified",
                   got, R["deaths_corrected"][j])
            RECTIFIED_RULE[(sec["ed"], j)] = "minus_nonres" if got == a else "minus_nonres_stillb"
        if "births_minus_deaths" in R:
            # sgt1935 and later use gross deaths here; earlier editions rectified deaths
            a = R["births"][j] - R["deaths_corrected"][j]
            b = R["births"][j] - R["deaths"][j]
            got = b if (b == R["births_minus_deaths"][j] and a != b) else a
            CHK.eq(topic, f"{sec['ed']} natality col {j}: births - deaths vs difference",
                   got, R["births_minus_deaths"][j])
        if "mortality_per_1000" in R and R["population"][j]:
            a = 1000 * R["deaths_corrected"][j] / R["population"][j]
            b = 1000 * R["deaths"][j] / R["population"][j]
            p = R["mortality_per_1000"][j]
            got = b if abs(b - p) < abs(a - p) else a
            CHK.eq(topic, f"{sec['ed']} natality col {j}: rate vs deaths/population",
                   got, p, tol=0.06)


def check_ward_days(sec, topic):
    rows = [r for r in sec["rows"] if not tot_label(r["label"]) and not r["label"].endswith("TOTAL")]
    check_diff(sec, topic, rows + [r for r in sec["rows"] if tot_label(r["label"])])
    T = [r for r in sec["rows"] if tot_label(r["label"])][-1]["v"]
    for j in range(len(T)):
        CHK.eq(topic, f"{sec['ed']} ward days col {j}: wards vs TOTAUX", s(r["v"][j] for r in rows), T[j])
    sub = [r for r in sec["rows"] if r["label"].endswith(" TOTAL")]
    for st in sub:
        p = st["label"][:-6]
        parts = [r for r in rows if r["label"].startswith(p + " ")]
        for j in range(2):
            CHK.eq(topic, f"{sec['ed']} ward days {p} col {j}: parts vs subtotal", s(r["v"][j] for r in parts), st["v"][j])


def check_wards(sec, topic):
    """Ward / Manouba tables: rows '<nat> paying|free', optional '<nat> TOTAL',
    'beds', 'TOTAL'. Checks: row total column (if any), column totals, nationality totals."""
    cols = sec["cols"]
    data = [r for r in sec["rows"] if r["label"].split()[-1] in ("paying", "free")]
    has_total = cols[-1] == "total"
    if has_total:
        for r in data:
            CHK.eq(topic, f"{sec['ed']} {topic} {r['label']}: cells vs row total", s(r["v"][:-1]), r["v"][-1])
        for r in sec["rows"]:
            if r["label"].endswith(" TOTAL"):
                nat = r["label"].split()[0]
                CHK.eq(topic, f"{sec['ed']} {topic} {nat}: paying+free vs bracket total",
                       s(x["v"][-1] for x in data if x["label"].split()[0] == nat), r["v"][-1])
    T = [r for r in sec["rows"] if r["label"] == "TOTAL"]
    if T:
        for j, c in enumerate(cols):
            if c.startswith("beds"):
                continue
            CHK.eq(topic, f"{sec['ed']} {topic} column {c}: rows vs TOTAL", s(r["v"][j] for r in data), T[0]["v"][j])
    B = [r for r in sec["rows"] if r["label"] == "beds"]
    if B and B[0]["v"][-1] is not None and has_total:
        CHK.eq(topic, f"{sec['ed']} {topic} beds: wards vs printed total", s(B[0]["v"][:-1]), B[0]["v"][-1])


def check_manouba_1939(sec, topic):
    """1939 layout: paying / free / total for men, women and both, by nationality, and a total row."""
    for r in sec["rows"]:
        d = dict(zip(sec["cols"], r["v"]))
        for g in ("_m", "_f", ""):
            CHK.eq(topic, f"{sec['ed']} manouba {r['label']} paying{g}+free{g} vs total{g}",
                   s([d["paying" + g], d["free" + g]]), d["total" + g])
        for k in ("paying", "free", "total"):
            CHK.eq(topic, f"{sec['ed']} manouba {r['label']} {k}: men+women vs both",
                   s([d[k + "_m"], d[k + "_f"]]), d[k])
    data = [r for r in sec["rows"] if r["label"] != "TOTAL"]
    T = [r for r in sec["rows"] if r["label"] == "TOTAL"][0]["v"]
    for j, c in enumerate(sec["cols"]):
        CHK.eq(topic, f"{sec['ed']} manouba column {c}: rows vs TOTAL", s(r["v"][j] for r in data), T[j])


def run_checks(secs):
    for sec in secs:
        t = sec["table"]
        if t.endswith("_movements"):
            check_movements(sec, t)
        elif t.endswith("_population"):
            check_diff(sec, t)
            R = {r["code"]: r["v"] for r in sec["rows"]}
            parts = [k for k in R if k.startswith("patient_days_")]
            if "patient_days" in R and parts:
                for j in range(2):
                    CHK.eq(t, f"{sec['ed']} {t} {sec['years'][j]}: patient-day categories vs patient days",
                           s(R[k][j] for k in parts), R["patient_days"][j])
        elif t in ("rabta_diseases", "rabta_months", "tunis_month_nationality", "tunis_cause_nationality",
                   "tunis_month_cause", "civil_births"):
            check_grid(sec, t)
        elif t == "tunis_natality_mortality":
            check_natality(sec, t)
        elif t == "interior":
            check_interior(sec, t)
        elif t == "manouba" and "paying_m" in sec["cols"]:
            check_manouba_1939(sec, t)
        elif t in ("civil_wards", "sadiki_wards", "manouba"):
            check_wards(sec, t)
        elif t == "civil_ward_days":
            check_ward_days(sec, t)
        elif t.endswith("_consultations"):
            if sec["cols"] and "total" in sec["cols"]:
                i = sec["cols"].index("total")
                for r in sec["rows"]:
                    CHK.eq(t, f"{sec['ed']} {t} {r['label']}: parts vs total", s(r["v"][:i]), r["v"][i])


# ================================================================= build
#
# Output files, one per table (see the notes .md next to each CSV). Tables
# printed for overlapping year windows follow SPEC_ADDENDUM rule 4 (each year
# from the latest edition printing it; every other printing compared); tables
# printed once per edition follow rule 5 (all editions kept, with `year`).

COMMON = ["census", "table_id", "gallica_ark", "source_page", "gallica_view"]

SEX_AGE = {"m": ("male", "Hommes"), "f": ("female", "Femmes"), "c": ("child", "Enfants"),
           "t": ("total", "Total")}
MOVEMENT = {
    "adm": ("carried_over_and_admitted", "Report au 1er janvier et entrées"),
    "rec": ("discharged_recovered", "Sorties par guérison"),
    "dth": ("discharged_died", "Sorties par décès"),
    "eoy": ("remaining_31_december", "Restants au 31 décembre"),
    "stillborn": ("stillborn", "Nouveau-nés morts-nés"),
}
# heading of the first column group as printed, where it differs from the default
MOVEMENT_ADM_FR = {(e, "civil_movements"): "Restants et entrées"
                   for e in ("sgt1922", "sgt1923", "sgt1924", "sgt1925")}
MOVEMENT_EOY_FR = {("sgt1925", "civil_movements"): "Observations et restants au 31 décembre 1925"}

NAT = {"french": "Français", "tunisian_muslim": "Musulmans", "tunisian_jewish": "Israélites tunisiens",
       "italian": "Italiens", "anglo_maltese": "Anglo-Maltais", "other": "Autres",
       "european": "Européens", "total": "Totaux"}
MONTHS = {"Janvier": "january", "Février": "february", "Mars": "march", "Avril": "april",
          "Mai": "may", "Juin": "june", "Juillet": "july", "Août": "august",
          "Septembre": "september", "Octobre": "october", "Novembre": "november",
          "Décembre": "december"}

CAUSE_EN = {
    "Maladies ordinaires": "ordinary_diseases", "Variole": "smallpox", "Diphtérie": "diphtheria",
    "Dyphtérie": "diphtheria", "Fièvre typhoïde": "typhoid_fever", "Typhoïde": "typhoid_fever",
    "Typhus": "typhus", "Typhus exanthématique": "typhus", "Fièvre récurrente": "relapsing_fever",
    "Rougeole": "measles", "Scarlatine": "scarlet_fever", "Tuberculose": "tuberculosis",
    "Tuberculose pulmonaire": "pulmonary_tuberculosis",
    "Tuberculose de l'appareil respiratoire": "respiratory_tuberculosis",
    "Autres tuberculoses": "other_tuberculosis", "Tuberculose chirurgicale": "surgical_tuberculosis",
    "Tuberculose médicale": "medical_tuberculosis", "Tuberculose osseuse": "bone_tuberculosis",
    "Grippe": "influenza", "Bronchite grippale": "influenzal_bronchitis", "Paludisme": "malaria",
    "Paludisme (malaria)": "malaria", "Fièvre et paludisme": "fever_and_malaria",
    "Affections cholériformes": "choleriform_diseases", "Affection cholériforme": "choleriform_diseases",
    "Peste": "plague", "Peste bubonique": "bubonic_plague", "Peste pulmonaire": "pneumonic_plague",
    "Rage": "rabies", "Erysipèle": "erysipelas", "Charbon": "anthrax", "Oreillons": "mumps",
    "Méningite cérébro-spinale": "cerebrospinal_meningitis", "Lèpre": "leprosy",
    "Varicelle": "chickenpox", "Coqueluche": "whooping_cough", "Dysentérie": "dysentery",
    "Dysenterie": "dysentery", "Fièvre méditerranéenne": "mediterranean_fever",
    "Encéphalée lithargique": "lethargic_encephalitis", "Purpura infect": "infectious_purpura",
    "Syphiligr. dermatologie": "syphilography_dermatology", "Médecine générale": "general_medicine",
    "Observations": "observation", "Observations et autres": "observation_and_other",
    "Observations et autres maladies": "observation_and_other", "Autres maladies": "other_diseases",
}

ACTIVITY_EN = {
    "patient_days": "Journées de malades", "patient_days_paying": "Journées de malades payants",
    "patient_days_indigent": "Journées de malades indigents",
    "patient_days_administrations": "Journées de malades : administrations",
    "patient_days_work_accidents": "Journées de malades : accidents de travail",
    "patient_days_wounded_soldiers": "Journées de malades : blessés militaires",
    "admissions": "Nombre d'admissions", "mean_daily_patients": "Effectif moyen journalier",
    "mean_stay_days": "Durée moyenne du séjour par malade",
    "staff_days_fed": "Journées du personnel nourri", "staff_days_not_fed": "Journées du personnel non nourri",
}

CONSULT = {
    "staff_external": ("staff_external", "Personnel externe"),
    "dressings": ("external_dressings", "Pansements externes"),
    "consultations": ("free_consultations", "Consultations gratuites"),
    "consultations_and_dressings": ("total", "Consultations et pansements (total)"),
    "radiology": ("radiology", "Service de la radiologie"),
    "electrotherapy": ("electrotherapy", "Électrothérapie"),
    "total": ("total", "Total"),
    "operations": ("operations", "Nombre des opérations"),
}

INTERIOR_COLS = {"beds": ("beds", "", "", "Nombre de lits")}
for _g, (_m, _p, _fr) in {"eur": ("patients", "european", "Malades traités : Européens"),
                          "ind": ("patients", "indigenous", "Malades traités : Indigènes"),
                          "deu": ("deaths", "european", "Décès : Européens"),
                          "din": ("deaths", "indigenous", "Décès : Indigènes")}.items():
    for _s in "mfct":
        INTERIOR_COLS[f"{_g}_{_s}"] = (_m, _p, _s, f"{_fr}, {SEX_AGE[_s][1]}")
INTERIOR_COLS["patient_days"] = ("patient_days", "all", "", "Nombre de journées")
INTERIOR_COLS["consultations"] = ("consultations", "all", "", "Consultations")

WARD = {"medg": ("general_medicine", "Médecine générale"), "chir": ("surgery", "Chirurgie"),
        "cont": ("contagious_diseases", "Maladies contagieuses"), "nerv": ("nervous_diseases", "Nerveux"),
        "mat": ("maternity", "Maternité"), "eyes": ("ophthalmology", "Yeux"),
        "ent": ("ent", "Oreilles, nez, gorge"), "med": ("medicine", "Médecine"),
        "births": ("maternity_births", "Naissances")}
PAY = {"paying": ("paying", "Payants"), "free": ("free", "Gratuits")}

# ----------------------------------------------------------------- per-cell flags
# (table, edition, row label or year, column code) -> flag. Printed values are kept
# unless the flag is reprint_corrected (see REPRINT). Reasons are in the notes.
CELL_FLAGS = {
    # sgt1922 ward days, 1921 column: the printed differences (en moins 18, en plus 666)
    # imply 10.165 and 16.556; with them the column sums to 88.859, the 1921 patient-days of
    # table c). The printed column total 92.929 is also wrong.
    ("civil_ward_days", "sgt1922", "Maternité", "1921"): "total_mismatch",
    ("civil_ward_days", "sgt1922", "Enfants", "1921"): "total_mismatch",
    # sgt1925 July diphtheria printed », but the row (608) and the column (17) each need 1
    ("tunis_month_cause", "sgt1925", "Juillet", "Diphtérie"): "total_mismatch",
    # sgt1928 October tuberculosis printed 59; row (490) and column (613) both need 51
    ("tunis_month_cause", "sgt1928", "Octobre", "Tuberculose"): "total_mismatch",
    # sgt1935 French paying, médecine générale women printed 39; row (922) and column (791) need 99
    ("civil_wards", "sgt1935", "french paying", "medg_f"): "total_mismatch",
    # sgt1936 Jewish free, médecine générale women printed 22; row (1.404) and column (766) need 222
    ("civil_wards", "sgt1936", "tunisian_jewish free", "medg_f"): "total_mismatch",
    # sgt1930 Rabta diphtheria, Italians printed 4; row (1) and column (121) need 0
    ("rabta_diseases", "sgt1930", "Dyphtérie", "italian"): "total_mismatch",
    # sgt1936 Rabta malaria, Muslims printed 47; row (97) and column (3.142) need 97
    ("rabta_diseases", "sgt1936", "Paludisme", "tunisian_muslim"): "total_mismatch",
    # natality tables: misprinted differences
    ("tunis_natality_mortality", "sgt1924", "Différence entre naissances et décès", "tunisian_muslim"): "total_mismatch",
    ("tunis_natality_mortality", "sgt1924", "Différence entre naissances et décès", "anglo_maltese"): "total_mismatch",
    ("tunis_natality_mortality", "sgt1928", "Différence entre naissances et décès", "other"): "total_mismatch",
    ("tunis_natality_mortality", "sgt1935", "Différence entre naissances et décès", "anglo_maltese"): "total_mismatch",
    ("tunis_natality_mortality", "sgt1935", "Différence entre naissances et décès", "other"): "total_mismatch",
    ("tunis_natality_mortality", "sgt1936", "Différence entre naissance et décès", "anglo_maltese"): "total_mismatch",
    # sgt1939 Muslim rectified deaths printed 373; 4.435 - 323 - 382 = 3.730 closes the row total 5.956
    ("tunis_natality_mortality", "sgt1939", "Mortalité rectifiée", "tunisian_muslim"): "total_mismatch",
    # sgt1935 Rabta, 1934 column: admissions and mean daily patients printed in each other's row
    ("rabta_population", "sgt1935", "admissions", "1934"): "total_mismatch",
    ("rabta_population", "sgt1935", "mean_daily_patients", "1934"): "total_mismatch",
}
REPRINT = {
    # sgt1936 prints 1.448; 2.393 + 1.488 + 428 = 4.309 (total printed in both editions)
    ("sadiki_movements", 1935, ("adm", "f")): "sgt1935",
    # sgt1936 prints 8.205; 8.209 + 75.297 = 83.506 (patient days printed in both editions)
    ("sadiki_population", 1935, "patient_days_paying"): "sgt1935",
    # sgt1927 table c) prints 70.687 / 36.518 for 1926; its own table b) and sgt1926 (tables
    # b and c) print 41.687 / 3.518
    ("civil_population", 1926, "staff_days_fed"): "sgt1926",
    ("civil_population", 1926, "staff_days_not_fed"): "sgt1926",
    # sgt1930 prints 110.446; 46.245 + 63.901 = 110.146 as in sgt1929 (tables b and c)
    ("civil_population", 1929, "patient_days"): "sgt1929",
    # sgt1930 prints 5.003; with 6.003 (sgt1929) the parts give 51.254, printed total 51.253
    ("civil_consultations", 1929, "radiology"): "sgt1929",
    # sgt1936 prints 28,410; 71.671 / 2.520 = 28,44 as in sgt1935
    ("rabta_population", 1935, "mean_stay_days"): "sgt1935",
    # sgt1936 prints the rows in the order indigents, payants with 2.973 / 68.698 (labels
    # swapped relative to sgt1935 and every earlier edition)
    ("rabta_population", 1935, "patient_days_paying"): "sgt1935",
    ("rabta_population", 1935, "patient_days_indigent"): "sgt1935",
}
SOURCE_OVERRIDE = {
    # sgt1923 reprints the 1922 ward column with three re-classified wards added on top of
    # the old ones (sum 113.524 vs 90.028 patient days): 1922 is taken from sgt1922
    ("civil_ward_days", 1922): "sgt1922",
}
COMMENT = defaultdict(list)


def flag_for(table, ed, row, col, raw=None):
    if raw == "x":
        return "not_applicable"
    return CELL_FLAGS.get((table, ed, str(row), col), "")


# ----------------------------------------------------------------- generic rule-4 series

class Series:
    """Collect printings of a year-windowed table; resolve per rule 4."""

    def __init__(self, table, year_level=False):
        self.table = table
        self.year_level = year_level    # take every cell of a year from one edition
        self.p = defaultdict(dict)      # (year, key) -> {ed: cell}
        self.stored = {}                # (year, key, ed) -> bool
        self.order = {}                 # key -> first-seen position (printed column/row order)

    def add(self, sec, year, key, value, raw, store, dims, row_label, col):
        self.p[(year, key)][sec["ed"]] = dict(value=value, raw=raw, sec=sec, dims=dims,
                                              row=row_label, col=col)
        self.stored[(year, key, sec["ed"])] = store
        self.order.setdefault(key, len(self.order))

    def resolve(self):
        rows, compared, diffs = [], 0, []
        chosen = {}
        year_eds = defaultdict(set)
        for (year, key), by in self.p.items():
            year_eds[year].update(by)
        for (year, key), by in sorted(self.p.items(), key=lambda kv: (kv[0][0], self.order[kv[0][1]])):
            ov = SOURCE_OVERRIDE.get((self.table, year))
            if self.year_level:
                ed = ov or [e for e in ORDER if e in year_eds[year]][-1]
            else:
                ed = ov if ov in by else [e for e in ORDER if e in by][-1]
            if ed not in by:       # cell not printed in the edition the year is taken from
                continue
            chosen[(year, key)] = ed
            for e in ORDER:
                if e in by and e != ed:
                    compared += 1
                    a, b = by[e]["value"], by[ed]["value"]
                    if a != b:
                        diffs.append((year, key, e, by[e]["raw"], ed, by[ed]["raw"]))
            if not self.stored[(year, key, ed)]:
                continue
            c = by[ed]
            flag = flag_for(self.table, ed, c["row"], c["col"], c["raw"])
            value, sec = c["value"], c["sec"]
            if (self.table, year, key) in REPRINT:
                e2 = REPRINT[(self.table, year, key)]
                value, sec, flag = by[e2]["value"], by[e2]["sec"], "reprint_corrected"
            rows.append(dict(census=sec["ed"], table_id=self.table, gallica_ark=sec["ark"],
                             source_page=sec["page"], gallica_view=sec["view"], year=year,
                             **c["dims"], value=value, flag=flag, _key=key))
        return rows, compared, diffs, chosen


def base(sec):
    return dict(census=sec["ed"], table_id=sec["table"], gallica_ark=sec["ark"],
                source_page=sec["page"], gallica_view=sec["view"])


def secs_of(all_secs, table):
    return [s for s in all_secs if s["table"] == table]


# ----------------------------------------------------------------- extractors

def ex_movements(all_secs, table):
    S = Series(table)
    for sec in secs_of(all_secs, table):
        cols = sec["cols"]
        for r in sec["rows"]:
            year = int(r["label"])
            d = dict(zip(cols, zip(r["v"], r["raw"])))
            for c, (v, raw) in d.items():
                if raw == ".":
                    continue
                if "_" in c:
                    g, sx = c.split("_")
                else:
                    g, sx = c, "t"
                if sx == "t":
                    comps = [d.get(f"{g}_{k}", (None, "."))[1] for k in "mfc"]
                    store = all(x == "." for x in comps)
                else:
                    store = True
                mv, mv_fr = MOVEMENT[g]
                if g == "adm":
                    mv_fr = MOVEMENT_ADM_FR.get((sec["ed"], table), mv_fr)
                if g == "eoy":
                    mv_fr = MOVEMENT_EOY_FR.get((sec["ed"], table), mv_fr)
                dims = dict(movement=mv, movement_fr=mv_fr, sex_age=SEX_AGE[sx][0], sex_age_fr=SEX_AGE[sx][1])
                S.add(sec, year, (g, sx), v, raw, store, dims, year, c)
    return S


def clean_label(lab):
    return re.sub(r"\s*\(printed [^)]*\)", "", lab).strip()


def ex_activity(all_secs, table):
    S = Series(table)
    for sec in secs_of(all_secs, table):
        n = len(sec["years"])
        for r in sec["rows"]:
            for y, v, raw in zip(sec["years"], r["v"][:n], r["raw"][:n]):
                if raw in (".", "x"):
                    continue
                dims = dict(indicator=r["code"], indicator_fr=clean_label(r["label"]))
                S.add(sec, y, r["code"], v, raw, True, dims, r["code"], str(y))
    return S


def ex_consultations(all_secs, table):
    S = Series(table)
    for sec in secs_of(all_secs, table):
        cols = sec["cols"]
        for r in sec["rows"]:
            year = int(r["label"])
            d = dict(zip(cols, zip(r["v"], r["raw"])))
            parts = [c for c in cols if c not in ("total", "operations", "consultations_and_dressings")]
            for c, (v, raw) in d.items():
                if raw == ".":
                    continue
                code, fr = CONSULT[c]
                if code == "total":
                    store = all(d[p][1] in ("x", ".") for p in parts)
                else:
                    store = raw != "x" or "total" not in d
                dims = dict(measure=code, measure_fr=fr)
                S.add(sec, year, code, v, raw, store and raw != "x", dims, year, c)
    return S


WARD_NORM = [(r"^Clinique du Dr Cuénod$|^Dr Cuénod$", "Dr Cuénod"), (r"^Pavillon A$", "A"),
             (r"^Nx ", "Nerveux "), (r"^D (Femmes|Enfants)$", r"André Vullien \1"),
             (r"^E\. Ch\. ", "Enfants Chirurgie "), (r"^Enfants \(Chirurgie\)$", "Enfants Chirurgie"),
             (r"^Isolés ", "Contagieux "), (r"^Tribaudeau$", "Tribeaudeau")]


def ward_key(lab):
    for pat, rep in WARD_NORM:
        lab = re.sub(pat, rep, lab)
    return lab


def ex_ward_days(all_secs):
    S = Series("civil_ward_days", year_level=True)
    for sec in secs_of(all_secs, "civil_ward_days"):
        for r in sec["rows"]:
            if tot_label(r["label"]) or r["label"].endswith(" TOTAL"):
                continue
            for y, v, raw in zip(sec["years"], r["v"][:2], r["raw"][:2]):
                if raw == ".":
                    continue
                dims = dict(ward_fr=r["label"])
                S.add(sec, y, ward_key(r["label"]), v, raw, True, dims, r["label"], str(y))
    return S


# ----------------------------------------------------------------- rule-5 tables

def rows_grid(sec, rowdim, coldims, rowmap, colmap, skip_total_col=True, keep_total_rows=()):
    """Generic grid: rowmap(label)->dict of row dims or None (skip); colmap(col)->dict or None."""
    out = []
    for r in sec["rows"]:
        rd = rowmap(r)
        if rd is None:
            continue
        for c, v, raw in zip(sec["cols"], r["v"], r["raw"]):
            cd = colmap(c, r)
            if cd is None or raw == ".":
                continue
            out.append(dict(**base(sec), year=sec["year"], **rd, **cd, value=v,
                            flag=flag_for(sec["table"], sec["ed"], r["label"], c, raw)))
    return out


def nat_col(c, r=None):
    if c in ("total", "TOTAUX"):
        return None
    return dict(nationality=c, nationality_fr=NAT[c])


def month_row(r):
    lab = r["label"]
    if tot_label(lab):
        return None
    if lab.startswith("Report"):
        return dict(month="carried_over_1_january", month_fr=lab)
    return dict(month=MONTHS[lab], month_fr=lab)


def cause_row(r):
    if tot_label(r["label"]):
        return None
    return dict(cause=CAUSE_EN[r["label"]], cause_fr=r["label"])


def ex_tunis(all_secs):
    out = defaultdict(list)
    for sec in all_secs:
        t = sec["table"]
        if t == "tunis_month_nationality":
            out[t] += rows_grid(sec, None, None, month_row, nat_col)
        elif t == "tunis_cause_nationality":
            out[t] += rows_grid(sec, None, None, cause_row, nat_col)
        elif t == "tunis_month_cause":
            out[t] += rows_grid(sec, None, None, month_row,
                                lambda c, r: None if c == "TOTAUX" else dict(cause=CAUSE_EN[c], cause_fr=c))
        elif t == "tunis_natality_mortality":
            out[t] += rows_grid(sec, None, None,
                                lambda r: dict(indicator=r["code"], indicator_fr=r["label"]),
                                lambda c, r: (dict(nationality="total", nationality_fr="Totaux")
                                              if c == "total" and r["code"] == "mortality_per_1000"
                                              else nat_col(c)))
        elif t == "rabta_diseases":
            out[t] += rows_grid(sec, None, None, cause_row, nat_col)
        elif t == "rabta_months":
            out[t] += rows_grid(sec, None, None, month_row, nat_col)
    return out


def ex_interior(all_secs):
    out = []
    for sec in secs_of(all_secs, "interior"):
        for r in sec["rows"]:
            if tot_label(r["label"]):
                continue
            for c, v, raw in zip(sec["cols"], r["v"], r["raw"]):
                m, p, sx, fr = INTERIOR_COLS[c]
                if sx == "t" or raw == ".":
                    continue
                out.append(dict(**base(sec), year=sec["year"], hospital=r["label"], measure=m,
                                population=p, sex_age=SEX_AGE[sx][0] if sx else "", column_fr=fr,
                                value=v, flag=flag_for("interior", sec["ed"], r["label"], c, raw)))
    return out


def ex_wards(all_secs, table):
    out = []
    for sec in secs_of(all_secs, table):
        for r in sec["rows"]:
            lab = r["label"]
            parts = lab.split()
            if lab == "beds":
                kind, nat, pay = "beds", "", ""
            elif len(parts) == 2 and parts[1] in PAY:
                kind, nat, pay = "patients", parts[0], parts[1]
            else:
                continue            # nationality brackets and TOTAL: printed totals
            for c, v, raw in zip(sec["cols"], r["v"], r["raw"]):
                if c == "total" or raw == ".":
                    continue
                w, sx = (c.split("_") + ["f"])[:2] if "_" in c else (c, "")
                wd, wfr = WARD[w]
                measure = kind if w != "births" else "births"
                if table == "civil_wards" and (kind == "beds" or w in ("mat", "births")):
                    sx = ""         # civil hospital: beds per ward, maternity not split by sex
                out.append(dict(**base(sec), year=sec["year"], measure=measure, ward=wd, ward_fr=wfr,
                                sex=SEX_AGE[sx][0] if sx else "", nationality=nat,
                                nationality_fr=NAT[nat] if nat else "", payment=PAY[pay][0] if pay else "",
                                payment_fr=PAY[pay][1] if pay else "", value=v,
                                flag=flag_for(table, sec["ed"], lab, c, raw)))
    return out


def ex_manouba(all_secs):
    out = []
    for sec in secs_of(all_secs, "manouba"):
        cols = sec["cols"]
        for r in sec["rows"]:
            lab = r["label"]
            for c, v, raw in zip(cols, r["v"], r["raw"]):
                if raw == ".":
                    continue
                if c.startswith("beds_"):            # beds, printed in the TOTAL row
                    measure, sx, nat, pay = "beds", c[-1], "", ""
                elif c.startswith("patients_"):       # 1935-1936 layout
                    if lab == "TOTAL":
                        continue
                    nat, pay = lab.split()
                    measure, sx = "patients", c[-1]
                else:                                 # 1939 layout: paying_m free_m total_m ...
                    if lab == "TOTAL" or c.startswith("total") or c in ("paying", "free"):
                        continue
                    pay, sx = c.split("_")
                    measure, nat = "patients", lab
                out.append(dict(**base(sec), year=sec["year"], measure=measure,
                                sex=SEX_AGE[sx][0], nationality=nat, nationality_fr=NAT[nat] if nat else "",
                                payment=PAY[pay][0] if pay else "", payment_fr=PAY[pay][1] if pay else "",
                                value=v, flag=flag_for("manouba", sec["ed"], lab, c, raw)))
    return out


def ex_births(all_secs):
    out = []
    for sec in secs_of(all_secs, "civil_births"):
        for r in sec["rows"]:
            if tot_label(r["label"]):
                continue
            for c, v, raw in zip(sec["cols"], r["v"], r["raw"]):
                if raw == "." or (c == "total" and r["code"] != "extra"):
                    continue
                sx = {"boys": ("male", "Garçons"), "girls": ("female", "Filles"), "total": ("total", "Total")}[c]
                cat = r["label"]
                out.append(dict(**base(sec), year=sec["year"],
                                category={"Légitimes": "legitimate", "Illégitimes": "illegitimate",
                                          "Morts-nés": "stillborn"}[cat], category_fr=cat,
                                sex=sx[0], sex_fr=sx[1], value=v,
                                flag=flag_for("civil_births", sec["ed"], r["label"], c, raw)))
    return out


# ----------------------------------------------------------------- output catalogue

OUTPUTS = {
    # name: (source table, rule, dimension columns, French title, English title)
    "health_hospital_civil_movements": ("civil_movements", 4,
        ["movement", "movement_fr", "sex_age", "sex_age_fr"],
        "Hôpital civil français de Tunis : mouvement des entrées et sorties",
        "French Civil Hospital of Tunis: admissions and discharges"),
    "health_hospital_civil_activity": ("civil_population", 4, ["indicator", "indicator_fr"],
        "Hôpital civil français de Tunis : mouvement de la population",
        "French Civil Hospital of Tunis: patient-days, admissions, mean stay"),
    "health_hospital_civil_ward_days": ("civil_ward_days", 4, ["ward_fr"],
        "Hôpital civil français de Tunis : répartition des journées par pavillon",
        "French Civil Hospital of Tunis: patient-days by ward (pavilion)"),
    "health_hospital_civil_births": ("civil_births", 5, ["category", "category_fr", "sex", "sex_fr"],
        "Hôpital civil français de Tunis : naissances à la maternité",
        "French Civil Hospital of Tunis: births in the maternity ward"),
    "health_hospital_civil_consultations": ("civil_consultations", 4, ["measure", "measure_fr"],
        "Hôpital civil français de Tunis : mouvement de la consultation et des pansements externes ; opérations",
        "French Civil Hospital of Tunis: external consultations and dressings; operations"),
    "health_hospital_civil_wards": ("civil_wards", 5,
        ["measure", "ward", "ward_fr", "sex", "nationality", "nationality_fr", "payment", "payment_fr"],
        "Hôpital civil français de Tunis : statistiques par pavillon",
        "French Civil Hospital of Tunis: patients by ward, sex, nationality and payment status"),
    "health_sadiki_movements": ("sadiki_movements", 4, ["movement", "movement_fr", "sex_age", "sex_age_fr"],
        "Hôpital Sadiki : mouvement des entrées et sorties", "Sadiki Hospital: admissions and discharges"),
    "health_sadiki_activity": ("sadiki_population", 4, ["indicator", "indicator_fr"],
        "Hôpital Sadiki : mouvement de la population", "Sadiki Hospital: patient-days, admissions, mean stay"),
    "health_sadiki_consultations": ("sadiki_consultations", 4, ["measure", "measure_fr"],
        "Hôpital Sadiki : mouvement de la consultation et des pansements externes ; opérations",
        "Sadiki Hospital: external consultations and dressings; operations"),
    "health_sadiki_wards": ("sadiki_wards", 5,
        ["measure", "ward", "ward_fr", "sex", "nationality", "nationality_fr", "payment", "payment_fr"],
        "Hôpital Sadiki : statistiques par service", "Sadiki Hospital: patients by ward"),
    "health_rabta_movements": ("rabta_movements", 4, ["movement", "movement_fr", "sex_age", "sex_age_fr"],
        "Hôpital des contagieux de la Rabta (Ernest-Conseil) : mouvement des entrées et sorties",
        "Rabta contagious-diseases hospital (Ernest-Conseil): admissions and discharges"),
    "health_rabta_activity": ("rabta_population", 4, ["indicator", "indicator_fr"],
        "Hôpital de la Rabta : mouvement de la population", "Rabta hospital: patient-days, admissions, mean stay"),
    "health_rabta_diseases_nationality": ("rabta_diseases", 5, ["cause", "cause_fr", "nationality", "nationality_fr"],
        "Hôpital de la Rabta : maladies traitées par nationalité",
        "Rabta hospital: diseases treated (admissions) by nationality"),
    "health_rabta_admissions_month_nationality": ("rabta_months", 5, ["month", "month_fr", "nationality", "nationality_fr"],
        "Hôpital de la Rabta : entrées par mois et par nationalité",
        "Rabta hospital: admissions by month and nationality"),
    "health_manouba_patients": ("manouba", 5,
        ["measure", "sex", "nationality", "nationality_fr", "payment", "payment_fr"],
        "Hôpital psychiatrique de la Manouba", "Manouba mental hospital: beds and patients"),
    "health_interior_hospitals": ("interior", 5,
        ["hospital", "measure", "population", "sex_age", "column_fr"],
        "Hôpitaux, annexes et infirmeries-dispensaires de l'intérieur : malades et décès",
        "Hospitals and dispensaries of the interior: beds, patients, patient-days, deaths, consultations"),
    "health_tunis_deaths_month_nationality": ("tunis_month_nationality", 5,
        ["month", "month_fr", "nationality", "nationality_fr"],
        "Statistique sanitaire de la ville de Tunis : décès par nationalité (par mois)",
        "Health statistics of the city of Tunis: deaths by month and nationality"),
    "health_tunis_deaths_month_cause": ("tunis_month_cause", 5, ["month", "month_fr", "cause", "cause_fr"],
        "Statistique sanitaire de la ville de Tunis : décès par genre de maladie (par mois)",
        "Health statistics of the city of Tunis: deaths by month and cause"),
    "health_tunis_deaths_cause_nationality": ("tunis_cause_nationality", 5,
        ["cause", "cause_fr", "nationality", "nationality_fr"],
        "Statistique sanitaire de la ville de Tunis : décès par genre de maladie et par nationalité",
        "Health statistics of the city of Tunis: deaths by cause and nationality"),
    "health_tunis_natality_mortality": ("tunis_natality_mortality", 5,
        ["indicator", "indicator_fr", "nationality", "nationality_fr"],
        "État comparatif de la natalité et de la mortalité à Tunis",
        "Comparative natality and mortality in Tunis, by nationality"),
}
TOPIC_OF = {v[0]: k for k, v in OUTPUTS.items()}


# ----------------------------------------------------------------- cross-checks

XCHK = defaultdict(list)    # output name -> lines


def cross_checks(all_secs):
    by = defaultdict(dict)
    for sec in all_secs:
        by[sec["ed"]][sec["table"]] = sec
    lines = []
    n = ok = 0
    for ed in ORDER:
        T = by[ed]
        mn, cn, mc, nm = (T.get(k) for k in ("tunis_month_nationality", "tunis_cause_nationality",
                                              "tunis_month_cause", "tunis_natality_mortality"))
        if not (mn and cn):
            continue
        tm = [r for r in mn["rows"] if tot_label(r["label"])][-1]["v"]
        tc = [r for r in cn["rows"] if tot_label(r["label"])][-1]["v"]
        dm = [s(r["v"][j] for r in mn["rows"] if not tot_label(r["label"])) for j in range(7)]
        dc = [s(r["v"][j] for r in cn["rows"] if not tot_label(r["label"])) for j in range(7)]
        for j, c in enumerate(mn["cols"]):
            sc = "sum of printed row totals" if c == "total" else "sum of cells"
            for what, a, b in (("printed TOTAUX", tm[j], tc[j]), (sc, dm[j], dc[j])):
                n += 1
                if a == b:
                    ok += 1
                else:
                    lines.append(f"{ed} {c}: deaths by month {what} {a} vs deaths by cause {what} {b}")
        if nm:
            d = [r for r in nm["rows"] if r["code"] == "deaths"][0]["v"]
            for j, c in enumerate(mn["cols"]):
                n += 1
                if d[j] == tm[j]:
                    ok += 1
                else:
                    lines.append(f"{ed} {c}: natality table 'Nombre de décès' {d[j]} vs deaths by month TOTAUX {tm[j]}")
        if mc:
            # month x cause row totals vs month x nationality row totals, and cause totals
            for r1, r2 in zip([r for r in mc["rows"]], [r for r in mn["rows"]]):
                n += 1
                if r1["v"][-1] == r2["v"][-1]:
                    ok += 1
                else:
                    lines.append(f"{ed} {r1['label']}: month x cause total {r1['v'][-1]} vs month x nationality total {r2['v'][-1]}")
            tmc = [r for r in mc["rows"] if tot_label(r["label"])][-1]["v"]
            ccause = {r["label"]: r["v"][-1] for r in cn["rows"] if not tot_label(r["label"])}
            for c, v in zip(mc["cols"][:-1], tmc[:-1]):
                n += 1
                eq = {"respiratory_tuberculosis": "pulmonary_tuberculosis"}
                cands = [k for k in ccause if eq.get(CAUSE_EN.get(k), CAUSE_EN.get(k)) == CAUSE_EN.get(c)]
                w = ccause[cands[0]] if cands else None
                if w == v:
                    ok += 1
                else:
                    lines.append(f"{ed} {c}: month x cause TOTAUX {v} vs cause x nationality total {w}")
    return n, ok, lines


def vital_comparison(tunis_rows):
    """Tunis city deaths (this chapter) vs état-civil deaths of the contrôle civil of Tunis."""
    root = HERE.parent / "yearbook_demography" / "csv"
    out = []
    for rel, nat in (("muslim", "tunisian_muslim"), ("jewish", "tunisian_jewish")):
        p = root / f"vital_{rel}_births_deaths.csv"
        if not p.exists():
            continue
        vit = {}
        with p.open() as f:
            for r in csv.DictReader(f):
                if r["controle_civil"] == "Tunis" and r["event"] == "deaths":
                    vit[int(r["year"])] = int(r["value"])
        city = defaultdict(int)
        for r in tunis_rows:
            if r["nationality"] == nat:
                city[r["year"]] += r["value"]
        for y in sorted(city):
            out.append((rel, y, city[y], vit.get(y)))
    return out


# ----------------------------------------------------------------- writing

def write_csv(name, rows, dims):
    cols = COMMON + ["year"] + dims + ["value", "flag"]
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


COLDOC = {
    "census": "edition the value is taken from (`sgt1922` … `sgt1939`)",
    "table_id": "transcription section the value comes from",
    "gallica_ark": "Gallica volume ark (views are numbered within a volume)",
    "source_page": "printed page number",
    "gallica_view": "Gallica view (fNNNN)",
    "year": "year the value refers to",
    "value": "count (integer), except where the notes say otherwise; printed » = 0",
    "flag": "empty, or `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)",
}


def write_notes(name, rows, info):
    table, rule, dims, tfr, ten = OUTPUTS[name]
    L = [f"# {tfr}", "", f"*{ten}.*", "",
         "Source: *Statistique générale de la Tunisie*, chapter III (health), editions "
         + ", ".join(sorted({r["census"] for r in rows})) + ". Source gallica.bnf.fr / Ministère des Affaires étrangères.",
         "", f"Pages and views used: {fmt_views(rows)}.", "",
         f"Transcriptions: `../transcribed/health_pop_<edition>.txt`, section `@{table}`; rebuild with "
         "`python3 data-raw/yearbook_health_education/extract_health_population.py build`. "
         "Per-check output: `health_validation.json`.", ""]
    years = sorted({r["year"] for r in rows})
    L += [f"Rows: {len(rows)}. Years: {years[0]}–{years[-1]}"
          + (f" ({len(years)} years: {', '.join(map(str, years))})" if len(years) != years[-1] - years[0] + 1 else "")
          + ".", ""]
    if rule == 4:
        L += ["Printed for overlapping year windows: each year is taken from the **latest** edition that prints it "
              "(SPEC_ADDENDUM rule 4; `census` = that edition) and every other printing of the same cell is compared "
              "below. Duplicate printings are not stored.", "",
              "Years printed by each edition: " + "; ".join(
                  f"{e} {min(ys)}–{max(ys)}" for e, ys in info["printed_years"].items()) + ".", ""]
    else:
        L += ["Printed once per edition, for the edition's own year; all editions are kept (SPEC_ADDENDUM rule 5).", ""]
    L += ["## Columns", ""]
    for c in COMMON + ["year"] + dims + ["value", "flag"]:
        L.append(f"- `{c}`: {COLDOC.get(c, DIMDOC.get(c, ''))}")
    L += ["", "Printed totals (row totals, TOTAUX lines, nationality brackets) and the printed "
          "\"différence en plus / en moins\" columns are not stored; they were used for validation.", ""]
    for para in COMMENT[name]:
        L += [para, ""]
    v = info["checks"]
    L += ["## Validation", "",
          f"- Checks against printed totals: {v['n']}; passed: {v['n'] - len(v['fail'])}; failed: {len(v['fail'])}."]
    if v["fail"]:
        L += ["", "Failed checks (printed values kept; every one was re-read on the page image and the printed "
              "figures are as transcribed; see the commentary above for the cells involved):", ""]
        L += [f"  - {x}" for x in v["fail"]]
    if rule == 4:
        L += ["", f"- Overlapping printings: {info['compared']} cell comparisons between editions; "
              f"{len(info['diffs'])} differences."]
        if info["diffs"]:
            kept = {(r["year"], r["_key"]): (r["census"], r["value"], r["flag"]) for r in rows if "_key" in r}
            L += ["", "| year | cell | edition | printed | latest edition | printed | stored (edition, flag) |",
                  "|---|---|---|---|---|---|---|"]
            for y, k, e, a, e2, b in info["diffs"]:
                ks = k if isinstance(k, str) else "/".join(k)
                st = kept.get((y, k))
                st = f"{st[1]} ({st[0]}{', ' + st[2] if st[2] else ''})" if st else "not stored (printed total)"
                L.append(f"| {y} | {ks} | {e} | {a} | {e2} | {b} | {st} |")
    fl = defaultdict(int)
    for r in rows:
        if r["flag"]:
            fl[r["flag"]] += 1
    L += ["", "- Flagged cells: " + (", ".join(f"{k}: {n}" for k, n in sorted(fl.items())) if fl else "none") + "."]
    if fl:
        L += [""] + [f"  - {r['census']} {r['year']} " + " / ".join(str(r[d]) for d in dims if r.get(d) not in (None, ""))
                     + f" = {r['value']} ({r['flag']})" for r in rows if r["flag"] and r["flag"] != "not_applicable"]
    for x in XCHK.get(name, []):
        L += ["", x]
    (OUT / f"{name}.md").write_text("\n".join(L) + "\n")


DIMDOC = {
    "movement": "`carried_over_and_admitted` (patients present on 1 January plus admissions during the year), "
                "`discharged_recovered`, `discharged_died`, `remaining_31_december`, `stillborn`",
    "movement_fr": "column heading as printed",
    "sex_age": "`male` (Hommes), `female` (Femmes), `child` (Enfants), `total` (only where the parts are not printed)",
    "sex_age_fr": "as printed",
    "indicator": "row code (listed in the commentary below / in the civil-hospital file)",
    "indicator_fr": "row label as printed in the edition the value is taken from",
    "ward_fr": "ward (pavillon) label as printed, with the sex sub-row where printed",
    "category": "`legitimate`, `illegitimate`, `stillborn`", "category_fr": "as printed",
    "sex": "`male`, `female`, or `total` / empty where not split",
    "sex_fr": "as printed",
    "measure": "what is counted (see below)", "measure_fr": "column heading (French)",
    "ward": "ward / service (English code)", "ward_fr": "as printed",
    "nationality": "`french`, `tunisian_muslim`, `tunisian_jewish`, `italian`, `anglo_maltese`, `other`; "
                   "`european` where the table groups the other Europeans; `total` for a printed all-nationality rate",
    "nationality_fr": "column or row heading (French)",
    "payment": "`paying` (Payants) or `free` (Gratuits)", "payment_fr": "as printed",
    "cause": "English code", "cause_fr": "disease label exactly as printed",
    "month": "`january` … `december`; `carried_over_1_january` for patients carried over (Rabta 1935)",
    "month_fr": "as printed",
    "hospital": "hospital or infirmary-dispensary, as printed",
    "population": "`european`, `indigenous`, or `all` (column not split)",
    "column_fr": "column heading (French)",
}


# ----------------------------------------------------------------- commentary for the notes

COMMENT.update({
    "health_hospital_civil_movements": [
        "Table a) \"Mouvement des entrées et sorties\". The first column group is headed \"Restants et entrées\" "
        "(sgt1922–sgt1925) and \"Report au 1er janvier et entrées\" (from sgt1926): patients present on 1 January "
        "plus admissions during the year. sgt1925 adds a single column \"Observations et restants au 31 décembre "
        "1925\" for 1925 only (stored as `remaining_31_december` / `total`). Printed totals per group are not stored.",
        "Checks: each group's men + women + children against its printed TOTAL. Failures (all re-read on the "
        "images, printed as transcribed): 1926 deaths 69 + 73 + 47 = 189 against a printed 201, repeated "
        "identically in all five editions that print 1926 (sgt1926–sgt1930); 1933 admissions 1.551 + 2.129 + "
        "1.402 = 5.082 against 5.182 (sgt1935); 1934 deaths 123 + 130 + 119 = 372 against 312 (sgt1935 and "
        "sgt1936). The faulty cell cannot be identified, so no cell is flagged.",
        "No edition prints 1931–1932 (there are no 1931–1934 yearbooks in the series).",
    ],
    "health_hospital_civil_activity": [
        "Table c) \"Mouvement de la population\": two year columns (three in sgt1930: 1928, 1929, 1930) and a "
        "\"différence en plus / en moins\" pair, which is not stored. Indicators: `patient_days` (Journées de "
        "malades), `patient_days_paying`, `patient_days_indigent`, `admissions` (Nombre d'admissions), "
        "`mean_daily_patients` (Effectif moyen journalier), `mean_stay_days` (Durée moyenne du séjour par malade, "
        "days), `staff_days_fed` / `staff_days_not_fed` (Journées du personnel nourri / non nourri; not printed "
        "from sgt1929 on). `mean_daily_patients` and `mean_stay_days` are rates (decimals where printed); all "
        "other values are counts. In sgt1925 the patient-days total is printed under the two parts (\"Totaux\").",
        "The 1924–1935 day counts are also printed in table b) \"Prix moyen de la journée de traitement\", a cost "
        "table that was not extracted (out of scope: financial). It was used to settle two conflicts: "
        "**1926 staff days**: sgt1927 table c) prints 70.687 / 36.518, but its own table b) and sgt1926 (tables "
        "b and c) print 41.687 / 3.518; the sgt1926 values are kept (`reprint_corrected`). **1929 patient days**: "
        "sgt1930 prints 110.446, but 46.245 + 63.901 = 110.146, as printed in sgt1929 tables b) and c); kept "
        "from sgt1929 (`reprint_corrected`).",
        "Other differences between printings, kept per rule 4: 1925 paying / indigent days are 51.258 / 48.893 "
        "in sgt1925 and 33.426 / 66.725 in sgt1926 (both pairs sum to the 100.151 printed in both); 1925 mean "
        "daily patients 274 (sgt1925) and 276 (sgt1926; 100.151 / 365 = 274,4).",
        "Failed difference checks are misprints in the printed \"différence\" columns (e.g. sgt1927 prints +26 "
        "for 273 → 301); the stored year values were re-read on the images. sgt1936 prints 1936 patient days "
        "150.255 against parts summing to 150.235.",
    ],
    "health_hospital_civil_ward_days": [
        "Table b) \"Répartition des journées par pavillon\", printed in sgt1922–sgt1925 only (two year columns "
        "plus differences). Ward labels are as printed and change between editions: sgt1924 and sgt1925 split "
        "the wards by sex/age (Hommes, Femmes, Enfants) and rename some (D = André Vullien, E. Ch. = Enfants "
        "Chirurgie, Isolés = Contagieux, Nx = Nerveux; Tribaudeau/Tribeaudeau). For the overlap comparison these "
        "names were matched; the stored `ward_fr` is the label of the edition the value comes from. The bracket "
        "subtotal \"G\" (Hommes + Femmes) and TOTAUX are not stored.",
        "**sgt1922, 1921 column**: Maternité 14.235 and Enfants 10.556 are misprints: the printed differences "
        "(en moins 18, en plus 666) imply 10.165 and 16.556, and with them the column sums to 88.859, the 1921 "
        "patient-days of table c). The printed column total 92.929 is also wrong (cells as printed sum to "
        "86.929). Printed values kept, flagged `total_mismatch`.",
        "**sgt1923** reprints the 1922 column with the old wards in bold and three re-classified wards added "
        "(André Vullien 5.505, Tribaudeau 10.147, Enfants (Chirurgie) 7.844), so that the column sums to its "
        "printed 113.524 instead of the 90.028 patient-days printed in both editions; its 1923 column counts "
        "Enfants 4.667 twice (also under André Vullien), summing to 94.568 instead of 89.901 (sgt1924). "
        "Rule 4 is therefore overridden for 1922 (taken from sgt1922, whose 14 cells equal sgt1923's bold "
        "cells), and 1923 comes from sgt1924 as rule 4 says. The sgt1923 1923 cells were compared with sgt1924 "
        "after aggregation: A, B, C, G, H, K, Dispensaire, Dr Cuénod and Tribaudeau are equal; Maternité "
        "4.096 = Enfants nés 3.345 + Enfants avec mère 751; Nerveux 4.760 = 2.802 + 1.857 + 101; Contagieux "
        "4.861 = Isolés 1.518 + 1.678 + 1.665; André Vullien 4.694 = D 27 + 4.667; Enfants (Chirurgie) 6.865 = "
        "218 + 6.647.",
        "sgt1925: Tribeaudeau 9.116 → 10.996 is printed with a difference of 1.180 (1.880), and the en-plus "
        "column total 5.228 agrees with the correct 1.880, not with the printed 1.180 (re-read at full resolution).",
    ],
    "health_hospital_civil_births": [
        "Table d) \"Naissances\" (maternity of the Hôpital civil français), printed sgt1922–sgt1925. Garçons / "
        "Filles by Légitimes / Illégitimes; the TOTAL column and TOTAUX row are not stored. sgt1925 adds a "
        "\"Récapitulation\" with Morts-nés 12 (stored as `stillborn` / `total`; recap total 354 = 342 + 12).",
    ],
    "health_hospital_civil_consultations": [
        "Table d) \"Mouvement de la consultation et des pansements externes avec distribution de médicaments à "
        "titre gratuit — Opérations\", printed from sgt1926. Columns: sgt1926–sgt1930 \"Personnel externe\" "
        "(`staff_external`), \"Consultations gratuites\", \"Service de la radiologie\", TOTAL, \"Nombre des "
        "opérations\"; from sgt1935 the first column is headed \"Pansements …\" (`external_dressings`). Operations "
        "1924–1925 are printed » meaning not recorded (not stored). TOTAL is not stored.",
        "1929 radiology: sgt1930 prints 5.003, sgt1929 6.003; with 6.003 the parts give 51.254 against the "
        "51.253 printed in both, so the sgt1929 value is kept (`reprint_corrected`). Remaining failures are "
        "printed totals off by 1–5: 1926 (72.070 vs 72.071, all five printings), 1929 (51.254 vs 51.253), 1936 "
        "(223.847 vs 223.852).",
    ],
    "health_hospital_civil_wards": [
        "\"Statistiques par pavillon\" (sgt1935, sgt1936, sgt1939): patients by ward (Médecine générale, "
        "Chirurgie, Maladies contagieuses, Nerveux: men/women; Maternité: not split, `sex` empty), by nationality "
        "(Français, Musulmans, Israélites, Européens = other Europeans; sgt1939 \"Tunisiens musulmans\", "
        "\"Tunisiens israélites\", \"Étrangers européens\") and Payants / Gratuits. `measure` = `patients`; `beds` "
        "(Nombre de lits organisés, per ward, printed in the TOTAL row); `births` (sgt1939 only: \"Nombre de "
        "naissances\" in the maternity, printed in the Gratuits rows; these births are included in the Gratuits "
        "row totals and in the 7.530 admissions). Row totals, nationality brackets and the TOTAL row are not stored.",
        "Identified misprints (printed values kept, `total_mismatch`): sgt1935 French paying, médecine générale "
        "women 39 (99 closes both the row total 922 and the column total 791); sgt1936 Jewish free, médecine "
        "générale women 22 (222 closes the row total 1.404 and the column total 766). sgt1935 also has row totals "
        "that disagree with their cells while every column total agrees (French free 2.876 vs 2.861; Jewish "
        "paying 105 vs 108; Jewish free 1.120 vs 1.132); no cell can be singled out.",
    ],
    "health_sadiki_movements": [
        "Table a) \"Mouvement des entrées et sorties\" of the Hôpital Sadiki, printed for long windows (5 to 14 "
        "years). The first group is \"Report au 1er janvier et entrées\". sgt1922 and sgt1923 add a column "
        "\"Nouveau-nés morts-nés\" (all », stored as 0, `stillborn` / `total`).",
        "**1935 women admitted**: sgt1936 prints 1.448, but 2.393 + 1.488 + 428 = 4.309 (printed in both); the "
        "sgt1935 value 1.488 is kept (`reprint_corrected`). Failed group checks, all re-read: sgt1925 1912 "
        "deaths (243 vs 245) and 1913 admissions (2.950 vs 2.951), 1934 recoveries 3.830 vs 3.930 (sgt1935 and "
        "sgt1936), and the 1936 row of sgt1936 (admissions 4.882 vs 4.874, recoveries 4.531 vs 4.331, deaths "
        "323 vs 343; the population table gives 4.680 admissions). No cell identifiable; none flagged.",
    ],
    "health_sadiki_activity": [
        "Table c) \"Mouvement de la population\" (two year columns plus differences, not stored). Indicators as "
        "in the civil hospital file; sgt1922 adds three patient-day categories (administrations, accidents de "
        "travail, blessés militaires; all »). Mean daily patients and mean stay are decimals.",
        "1935 paying patient-days: sgt1936 prints 8.205, sgt1935 8.209 (8.209 + 75.297 = 83.506, printed in "
        "both): kept from sgt1935 (`reprint_corrected`). 1934 (sgt1935 only): paying 7.072 + indigent 78.134 = "
        "85.206 against 85.226 printed (also 85.226 in table b). Most failed checks are misprinted difference "
        "columns (e.g. sgt1922 en moins 3.582 for 14.497 → 11.915; sgt1926 prints 398 for 1.398 and 465 for "
        "4,65); the sgt1936 difference column is garbled throughout.",
    ],
    "health_sadiki_consultations": [
        "Table d) consultations, external dressings and operations. sgt1922–sgt1923 print one column "
        "\"Consultations et pansements externes\" (stored as `total`); sgt1924–sgt1925 go back to 1905, with only "
        "totals for 1905–1916 (parts printed »; the total is stored); from sgt1936 a third part is added, "
        "\"Électrothérapie, R. ultra-violets, radiographie, radioscopie, teigne\" (`electrotherapy`), and the "
        "1934–1935 totals reprinted there include it (253.941 and 276.530 against 243.992 and 261.780 in "
        "sgt1935). Totals are stored only where the parts are not printed.",
        "1924 external dressings are printed 898.176 in sgt1924 and sgt1925 and 88.176 in sgt1926–sgt1930 "
        "(88.176 + 27.815 = 115.991, the printed total); rule 4 keeps 88.176. 1910 total: 24.594 (sgt1924) vs "
        "24.584 (sgt1925, kept). 1919: 63.261 + 20.389 = 83.650 against 83.640 in all five printings; 1936: parts "
        "339.090 against 338.786.",
    ],
    "health_sadiki_wards": [
        "\"Statistiques par pavillon\" (sgt1935, sgt1936, sgt1939): patients by service (Chirurgie, Yeux, "
        "Oto-rhino, Médecine: H/F; Maternité: F), nationality and Payants / Gratuits; `beds` = Nombre de lits "
        "organisés per service and sex. The printed TOTAL row is not stored; all column checks pass.",
        "sgt1936: the heading repeats the 1935 heading of sgt1935 (\"au cours de l'année 1935 : 4.116\", 251 "
        "beds) but the cells differ from sgt1935 and their column totals sum to 4.680, the 1936 admissions of the "
        "Sadiki population table, so they are stored as 1936. In the same table the French rows are both "
        "labelled Payants and the Jewish rows both Gratuits; the second French row is stored as free and the "
        "first Jewish row as paying.",
    ],
    "health_rabta_movements": [
        "Rabta contagious-diseases hospital (\"Annexe de la Rabta\" in sgt1922–sgt1923, then \"Hôpital des "
        "contagieux de la Rabta\", \"Hôpital Ernest-Conseil\" from sgt1935). sgt1926–sgt1928 add \"restants au "
        "31 décembre\" for the edition's last year.",
        "sgt1936 prints the year labels in reverse order (1936, 1935, 1934), but the first two rows equal the "
        "1934 and 1935 rows of sgt1935 and the third totals 3.183, the 1936 total of the diseases table, so the "
        "rows were assigned by content. Failed checks: 1929 deaths 182 + 22 + 15 = 219 against 270 (sgt1929 and "
        "sgt1930), 1933 recoveries 1.990 vs 1.989 (sgt1935).",
    ],
    "health_rabta_activity": [
        "Table c) \"Mouvement de la population\" of the Rabta (indicators as in the civil hospital file; staff "
        "days include half days, e.g. 4.817,5).",
        "**sgt1935, 1934 column**: admissions and mean daily patients are printed in each other's row "
        "(admissions 196,147, mean daily 2.408; the 1935 column and the differences, +112 admissions, show the "
        "intended order). Kept as printed and flagged `total_mismatch`.",
        "**Paying / indigent rows from sgt1936**: sgt1936 and sgt1939 print the row \"indigents\" first with a "
        "small figure (1935: 2.973; 1938: 4.146) and \"payants\" second with the large one (68.698; 77.366), the "
        "reverse of every earlier edition (sgt1935: payants 2.973, indigents 68.698). For 1935 the sgt1935 "
        "values are kept (`reprint_corrected`, both rows); 1936, 1938 and 1939, printed only there, are stored "
        "under the labels as printed, which are very probably swapped. 1935 mean stay: sgt1936 prints 28,410; "
        "71.671 / 2.520 = 28,44 as in sgt1935 (kept, `reprint_corrected`). 1925 mean stay: 27,051 (sgt1925) vs "
        "27,031 (sgt1926, kept; 16.543 / 612 = 27,03).",
        "1939: paying 64.161 + indigent 6.659 = 70.820 against 70.730 patient days.",
    ],
    "health_rabta_diseases_nationality": [
        "\"Répartition des maladies soignées (par maladie et par nationalité)\": admissions by disease and "
        "nationality for the edition's year. The list of diseases changes between editions; `cause_fr` is the "
        "label as printed (spellings such as \"Dyphtérie\", \"Encéphalée lithargique\" kept), `cause` an English "
        "code. TOTAUX row and column are not stored.",
        "Identified misprints (`total_mismatch`, printed value kept): sgt1930 diphtheria, Italians 4 (row "
        "total 1 and column total 121 both need 0); sgt1936 malaria, Muslims 47 (row total 97 and the Muslim "
        "column total 3.142 both need 97). Other failures: sgt1929 Muslim column 955 vs 956; sgt1936 typhus and "
        "typhoid row totals 15 and 6 against Muslim cells 20 and 17 (the column total agrees with the cells).",
    ],
    "health_rabta_admissions_month_nationality": [
        "\"Récapitulation des personnes hospitalisées par mois et par nationalité\" (sgt1922–sgt1930, sgt1935; "
        "not printed in sgt1936 and sgt1939). sgt1935 adds a first row \"Reports au 1er janvier 1935\" "
        "(`carried_over_1_january`), which the printed TOTAUX include. sgt1930: May row total 52 against cells "
        "62; the TOTAL column (1.126) agrees with 62.",
    ],
    "health_manouba_patients": [
        "Hôpital pour les maladies mentales de la Manouba, \"Nombre de malades hospitalisés au cours de "
        "l'année\" (sgt1935, sgt1936, sgt1939). sgt1935–sgt1936: patients by nationality × Payants/Gratuits × "
        "sex, and beds (Nombre de lits organisés) by sex, printed in the total row. sgt1939: paying / free / "
        "total by sex and nationality, no beds. `nationality` = `european` for \"Européens\". Totals not stored. "
        "sgt1936: women's cells sum to 67 against 70 printed.",
    ],
    "health_interior_hospitals": [
        "\"Renseignements généraux\" of the hospitals and infirmaries-dispensaries of the interior (and from "
        "sgt1936 the regional hospital of Sfax; sgt1939 also lists the Hôpital civil français, Sadiki, "
        "Ernest-Conseil and Manouba hospitals of Tunis and the Sfax regional hospital, kept as printed). "
        "Columns stored: Nombre de lits (`beds`), Malades hospitalisés européens / indigènes by men, women, "
        "children (`patients`), Nombre de journées d'hospitalisation (`patient_days`), Décès européens / "
        "indigènes by men, women, children (`deaths`), Nombre de consultations (`consultations`; not printed "
        "in sgt1927–sgt1930). The financial column (Prix de la journée) is not extracted; the Total columns "
        "and TOTAL row are not stored. Hospital names as printed (Kef (Le) / Le Kef, Mactar / Maktar, "
        "Médenine et annexes, Menzel-Temime …).",
        "Printed » = 0; cells printed 0 (sgt1936) are 0. sgt1935 prints no TOTAL row; its Médenine patient "
        "days are printed 2.294,5. sgt1936: the Médenine indigenous-deaths total is blank (the 80 printed "
        "between Médenine and Sfax belongs to Sfax). In sgt1939 the Tunis hospital rows repeat figures of the "
        "hospital tables (e.g. Sadiki 1.532 / 1.953 / 606 = its 1939 admissions). Footnote (sgt1939): the 520 beds "
        "of the Hôpital civil français, printed \"(a) 520\", exclude (a) the 280 beds for soldiers.",
        "The 90 failed checks are listed below. Every page was re-read on the image; the inconsistencies are in "
        "the print. They are concentrated in sgt1923 (TOTAL row whose men + women + children do not match its "
        "own totals), sgt1928, sgt1929 and above all sgt1936, whose table is visibly garbled (e.g. Sousse "
        "Europeans printed » » » 349, Monastir 69 / 199 / 81 / 8, Tabarka indigenous men 308 with a total of 0, "
        "consultations summing to 495.367 against 627.741). Cells are stored as printed and not flagged, "
        "because the faulty cell cannot be identified.",
    ],
    "health_tunis_deaths_month_nationality": [
        "\"Statistique sanitaire de la ville de Tunis\", a) \"Décès par nationalité\": deaths in the city of "
        "Tunis by month and nationality (Français, Musulmans, Israélites tunisiens, Italiens, Anglo-Maltais, "
        "Autres). TOTAUX row and column not stored. sgt1922: January is printed 499 against cells summing to "
        "491 (the month × cause table also gives 491; the printed TOTAUX 4.599 is consistent with 491).",
    ],
    "health_tunis_deaths_month_cause": [
        "b) \"Décès par genre de maladie\": deaths by month × cause (Maladies ordinaires and 12 epidemic "
        "diseases). In sgt1939 the tuberculosis column is \"Tuberculose pulmonaire\" and \"Maladies ordinaires\" "
        "(5.956) appears to include the 134 \"Autres tuberculoses\" that the cause × nationality table shows separately "
        "(5.827 + 134 = 5.961; the remaining 5 are the measles gap below).",
        "Identified misprints (`total_mismatch`): sgt1925 July diphtheria printed » (the row 608 and the column "
        "17 each need 1); sgt1928 October tuberculosis 59 (row 490 and column 613 need 51). Other failures: "
        "sgt1922 September and October rows off by −1 / +1 (columns agree); sgt1939 measles column sums to 117 "
        "against a printed 112 (the cause × nationality table also prints 112), so the TOTAUX row sums to 6.951 "
        "against 6.956.",
    ],
    "health_tunis_deaths_cause_nationality": [
        "c) \"Décès par genre de maladie et par nationalité\" (in sgt1935–sgt1939 printed before the month × "
        "cause table). sgt1939 splits tuberculosis into \"Tuberculose de l'appareil respiratoire\" and \"Autres "
        "tuberculoses\" and names \"Typhus exanthématique\", \"Paludisme (malaria)\". All checks pass.",
    ],
    "health_tunis_natality_mortality": [
        "d) \"État comparatif de la natalité et de la mortalité à Tunis\" by nationality. Indicators: `deaths`, "
        "`stillbirths` (Morts-nés), `non_residents`, `deaths_corrected` (Mortalité rectifiée), `births` "
        "(Naissances déclarées), `births_minus_deaths` (Différence entre naissances et décès; printed with + / − "
        "signs, stored signed), `population` (Population approximative), `mortality_per_1000` (rate, 2 decimals; "
        "the printed all-nationality rate is stored with `nationality` = `total`). Other TOTAUX not stored.",
        "Definitions vary by edition: sgt1922 rectifies deaths by non-residents only, later editions by "
        "non-residents and stillbirths; until sgt1930 the difference and the rate use rectified deaths, from "
        "sgt1935 gross deaths. sgt1935 prints the differences without signs. The population is the same in "
        "sgt1922–sgt1924 (171.676), sgt1926–sgt1928 (185.996), sgt1930–sgt1935 (202.405) and sgt1936–sgt1939 "
        "(219.277).",
        "Flagged misprints (`total_mismatch`, printed value kept): sgt1924 differences for Muslims (printed "
        "−253; 2.999 − 2.746 = +253) and Anglo-Maltese (printed +7; 122 − 129 = −7), the row total 1.771 needing "
        "the corrected signs; sgt1928 Autres printed −10 (35 − 25 = +10; the row total 2.135 needs +10); sgt1935 Anglo-Maltese 73 (printed without sign; 35 − 108 = −73) and Autres 96 "
        "(64 − 60 = 4; with −73 and 4 the row sums to the printed 2.313); sgt1936 Anglo-Maltese 55 (45 − 90 = "
        "−45; the row total 2.445 needs −45); sgt1939 Muslim rectified deaths 373 (4.435 − 323 − 382 = 3.730, "
        "which closes the printed 5.956). Unflagged: sgt1927 rectified deaths off by −9 / −6 / +2 (total "
        "4.853 vs 4.866); sgt1928 rates for French (15,71) and Muslims (30,87) imply 439 and 2.554 rectified deaths "
        "against the printed 429 and 2.545 (which agree with deaths − stillbirths − non-residents and with the "
        "total 4.306); sgt1930 Jewish rate 20,70 vs 522 / 25.399 = 20,55; sgt1935 Anglo-Maltese rectified 96 "
        "vs 97.",
    ],
})


# ----------------------------------------------------------------- main

def build(write=True):
    all_secs = []
    for ed in ORDER:
        all_secs += parse(ed)
    run_checks(all_secs)
    results = {}
    series = {"civil_movements": ex_movements(all_secs, "civil_movements"),
              "sadiki_movements": ex_movements(all_secs, "sadiki_movements"),
              "rabta_movements": ex_movements(all_secs, "rabta_movements"),
              "civil_population": ex_activity(all_secs, "civil_population"),
              "sadiki_population": ex_activity(all_secs, "sadiki_population"),
              "rabta_population": ex_activity(all_secs, "rabta_population"),
              "civil_consultations": ex_consultations(all_secs, "civil_consultations"),
              "sadiki_consultations": ex_consultations(all_secs, "sadiki_consultations"),
              "civil_ward_days": ex_ward_days(all_secs)}
    other = ex_tunis(all_secs)
    other["interior"] = ex_interior(all_secs)
    other["civil_wards"] = ex_wards(all_secs, "civil_wards")
    other["sadiki_wards"] = ex_wards(all_secs, "sadiki_wards")
    other["manouba"] = ex_manouba(all_secs)
    other["civil_births"] = ex_births(all_secs)
    xn, xok, xlines = cross_checks(all_secs)
    vit = vital_comparison(other["tunis_month_nationality"])
    for name, (table, rule, dims, *_ ) in OUTPUTS.items():
        if table in series:
            rows, compared, diffs, chosen = series[table].resolve()
        else:
            rows, compared, diffs = other[table], 0, []
        py = defaultdict(set)
        if table in series:
            for (y, k), by in series[table].p.items():
                for e in by:
                    py[e].add(y)
        results[name] = dict(rows=rows, compared=compared, diffs=diffs,
                             printed_years={e: sorted(py[e]) for e in ORDER if e in py},
                             checks=dict(n=CHK.n[table], fail=CHK.fail[table]))
    XCHK["health_tunis_deaths_month_nationality"].append(
        f"## Cross-checks\n\n- Deaths by month vs deaths by cause and the natality table, per nationality and "
        f"edition (printed totals and sums of cells): {xn} comparisons, {xok} equal.\n"
        + "".join(f"  - {x}\n" for x in xlines))
    XCHK["health_tunis_deaths_month_nationality"][0] += (
        "\nThe three differences are explained by two printing errors: sgt1922 January printed 499 instead of 491 "
        "in the month × nationality table (so its row totals sum to 4.607), and in sgt1939 the month × cause "
        "table counts the 134 \"Autres tuberculoses\" under \"Maladies ordinaires\" (see that file's notes). "
        "Every nationality total of deaths by month equals the one of deaths by cause and the \"Nombre de décès\" "
        "of the natality table, in all 12 editions.\n")
    XCHK["health_tunis_deaths_cause_nationality"].append(XCHK["health_tunis_deaths_month_nationality"][0])
    XCHK["health_tunis_deaths_month_cause"].append(XCHK["health_tunis_deaths_month_nationality"][0])
    vt = ["## Comparison with the état civil (contrôle civil of Tunis)", "",
          "Muslim and Jewish deaths in the city of Tunis (sum of this table's monthly cells) against deaths recorded "
          "in the contrôle civil of Tunis (`../../yearbook_demography/csv/vital_*_births_deaths.csv`). The contrôle "
          "covers more than the city (banlieue and rural cheikhats), so equality is not expected.", "",
          "| population | year | city of Tunis | contrôle civil of Tunis | city / contrôle |", "|---|---|---:|---:|---:|"]
    for rel, y, a, b in vit:
        vt.append(f"| {rel} | {y} | {a} | {b if b is not None else 'n/a'} | "
                  f"{(f'{a / b:.2f}' if b else 'n/a')} |")
    XCHK["health_tunis_deaths_month_nationality"].append("\n".join(vt))
    if write:
        for name, (table, rule, dims, *_ ) in OUTPUTS.items():
            write_csv(name, results[name]["rows"], dims)
            write_notes(name, results[name]["rows"], results[name])
        val = {name: dict(rows=len(r["rows"]), checks=r["checks"]["n"], failed=r["checks"]["fail"],
                          overlap_compared=r["compared"], overlap_diffs=[list(map(str, d)) for d in r["diffs"]])
               for name, r in results.items()}
        val["_cross_checks"] = dict(n=xn, equal=xok, differences=xlines)
        val["_vital_comparison"] = [dict(religion=a, year=b, city=c, controle=d) for a, b, c, d in vit]
        (OUT / "health_validation.json").write_text(json.dumps(val, indent=1, ensure_ascii=False) + "\n")
    return results, (xn, xok, xlines), vit


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    res, x, vit = build(write=(cmd == "build"))
    for name, r in res.items():
        print(f"{name}: {len(r['rows'])} rows; checks {r['checks']['n']}, failed {len(r['checks']['fail'])}; "
              f"overlap compared {r['compared']}, diffs {len(r['diffs'])}")
    print(f"cross-checks: {x[1]}/{x[0]} equal")
    if cmd == "check":
        for name, r in res.items():
            for f_ in r["checks"]["fail"]:
                print("  FAIL", f_)
            for d in r["diffs"]:
                print("  DIFF", name, d)
        for l_ in x[2]:
            print("  XCHK", l_)
