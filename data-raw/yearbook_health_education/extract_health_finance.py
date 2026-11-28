#!/usr/bin/env python3
"""Health chapter (III) finance and institute tables of the Statistique générale de la
Tunisie, editions sgt1922-sgt1939: public-assistance budget (receipts, expenditure, credits),
child-protection credits, accounts of the subsidised societies, the "État des recettes et des
dépenses" (sgt1935-sgt1939), Institut Pasteur and Institut Arloing (budgets, serums and vaccines
distributed), the "situation financière" of the hospitals of the interior and the day-cost tables
("prix moyen de la journée de traitement") of the Tunis hospitals.

  python3 extract_health_finance.py check   parse, run every check, print failures, differences, cross-checks
  python3 extract_health_finance.py build   ... and write csv/health_<topic>.csv, their .md notes and
                                            csv/health_finance_validation.json

Source of truth: transcribed/health_finance_<edition>.txt. Format: sections
'[<table>] key=value ...' (views=, pages=, year= or years=, cols= 'a ; b ; c', title=, ...);
optional 'cols:' / 'units:' lines; '@ view=N page=P' moves the following rows to another page;
rows 'label | v v v [| v v ...]' (column groups separated by '|'), and in the budget tables
'K | [article |] label | v v v' with K = A article, D amount printed in the label column (detail
of the article above), H heading, S "A reporter", I sub-total, B section total, T TOTAUX,
R recapitulation total, N footnote. Values: no thousands separators, decimal point for the
decimal comma (centimes), printed » = 0, '-' or '—' = no figure printed (not stored), 'mémoire'
and 'déficit' as printed (stored empty, not_applicable), 'x' = printed » standing for "not
reported" (stored empty, not_applicable), '?' illegible. Token suffixes: {d} derived_from_totals,
{tm} total_mismatch (printed value kept). Comment lines (#) are copied into the notes.

Tables printed for overlapping year windows follow SPEC_ADDENDUM rule 4 (latest printing kept,
every printing compared; REPRINT lists documented exceptions); tables printed once per edition
follow rule 5. Printed totals, "Total" columns and "différence" columns are used for checks only.
Commentary written to each notes file is in COMMENT.
"""
import csv
import json
import re
import sys
import unicodedata
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
TOKFLAG = {"d": "derived_from_totals", "tm": "total_mismatch", "oc": "ocr_corrected", "rc": "reprint_corrected"}


def tok(t):
    """-> (value, raw, flag). » = 0; '-' / '—' = nothing printed (None)."""
    flag = ""
    m = re.fullmatch(r"(.*?)\{(\w+)\}", t)
    if m:
        t, f = m.groups()
        flag = TOKFLAG.get(f, "")
    if t in ("»", "0"):
        return 0, t, flag
    if t == "x":
        return None, t, "not_applicable"
    if t in ("-", "—", ".", "mémoire", "déficit", "?"):
        return None, t, flag or ("illegible" if t == "?" else "")
    return (int(t) if re.fullmatch(r"-?\d+", t) else float(t)), t, flag


def parse(ed):
    p = TR / f"health_finance_{ed}.txt"
    if not p.exists():
        return []
    secs, cur = [], None
    for ln, line in enumerate(p.read_text().splitlines(), 1):
        line = line.rstrip()
        if not line.strip() or line.startswith("#"):
            continue
        if line.startswith("["):
            m = re.match(r"\[(\w+)\]\s*(.*)", line)
            cur = {"table": m.group(1), "ed": ed, "ark": EDITIONS[ed], "rows": [], "cols": None, "units": None}
            for k, v in re.findall(r"(\w+)=(.+?)(?=\s+\w+=|$)", m.group(2)):
                cur[k] = v.strip()
            cur["views"] = [int(x) for x in (cur.get("views") or cur.get("view")).split(",")]
            cur["pages"] = [int(x) for x in (cur.get("pages") or cur.get("page")).split(",")]
            if "years" in cur:
                cur["years"] = [int(y) for y in cur["years"].split()]
            if "year" in cur:
                cur["year"] = int(cur["year"])
            if isinstance(cur.get("cols"), str):
                cur["cols"] = [x.strip() for x in cur["cols"].split(";")]
            secs.append(cur)
            continue
        if line.startswith("cols:"):
            cur["cols"] = [x.strip() for x in line[5:].split(";")]
            continue
        if line.startswith("units:"):
            cur["units"] = [x.strip() for x in line[6:].split(";")]
            continue
        if line.startswith("@"):      # '@ view=N page=P': the following rows are printed on that page
            d = dict(re.findall(r"(\w+)=(\d+)", line))
            cur["at"] = (int(d["view"]), int(d["page"]))
            continue
        if line.startswith("section:"):
            cur["rows"].append({"kind": "H", "code": "", "label": line[8:].strip(), "groups": [], "line": ln})
            continue
        parts = [x.strip() for x in line.split("|")]
        r = {"line": ln, "kind": None, "code": "", "at": cur.get("at")}
        if parts[0] in ("A", "H", "S", "T", "D", "N", "I", "B", "R") and len(parts) >= 2:
            r["kind"] = parts.pop(0)
            if r["kind"] == "A":
                r["code"] = parts.pop(0)
        r["label"] = parts[0]
        if cur["table"] == "pasteur_products":
            r["unit"] = parts[1]
            parts = [parts[0], parts[2]]
        try:
            r["groups"] = [[tok(t) for t in g.split()] for g in parts[1:]]
        except ValueError as e:
            raise ValueError(f"{ed} line {ln}: {line[:80]}: {e}")
        cur["rows"].append(r)
    return secs


class Checks:
    def __init__(self):
        self.n = defaultdict(int)
        self.fail = defaultdict(list)

    def eq(self, topic, what, got, printed, tol=0.005):
        if got is None or printed is None:
            return
        self.n[topic] += 1
        if abs(got - printed) > tol:
            self.fail[topic].append(f"{what}: cells give {round(got, 2)}, printed {printed}")


CHK = Checks()


def s(xs):
    xs = [x for x in xs if x is not None]
    return round(sum(xs), 2) if xs else None


def V(r, g=0):
    return [v for v, _, _ in r["groups"][g]] if len(r["groups"]) > g else []


def is_total(lab):
    return re.match(r"(?i)^(totaux|total)\b", lab) is not None


def is_sub(lab):
    return lab.startswith("SUBTOTAL")


def check_running(sec, t, groups):
    """SUBTOTAL rows (à reporter) = sum of the data rows above them; TOTAUX = sum of all data rows."""
    seen = []
    for r in sec["rows"]:
        if r["kind"] is not None:
            continue
        if is_sub(r["label"]) or is_total(r["label"]):
            for g in range(groups(r)):
                for j in range(len(r["groups"][g])):
                    CHK.eq(t, f"{sec['ed']} {t} {r['label']} (line {r['line']}) group {g} col "
                           f"{sec['years'][j] if 'years' in sec else j}: rows above vs printed",
                           s(V(x, g)[j] if len(V(x, g)) > j else None for x in seen), V(r, g)[j])
        else:
            seen.append(r)


def check_series(sec):
    check_running(sec, sec["table"], lambda r: 1)


def check_budget(sec):
    """A rows accumulate. S (à reporter) and B (section subtotal) = sum since the last B; I = sum since
    the last I; T / R (grand total, recapitulation) = sum since the last heading naming a 'Chapitre'.
    D rows (amounts printed in the label column) must sum to the credit of the article above them.
    Where a column is headed Total, it must equal the sum of the columns before it."""
    t, ed = sec["table"], sec["ed"]
    cols = sec["cols"] or []
    ncol = max((len(V(r)) for r in sec["rows"] if r["kind"] in ("A", "T", "R")), default=0)
    acc = {k: [0] * ncol for k in ("run", "sec", "sub")}
    lastA, dsum = None, None
    ti = next((i for i, c in enumerate(cols) if c.strip().lower() == "total"), None)

    def close_detail():
        nonlocal dsum
        if lastA is not None and dsum is not None:
            CHK.eq(t, f"{ed} {t} art {lastA['code']} {lastA['label'][:40]}: detail lines vs credit", dsum, V(lastA)[0])
        dsum = None

    for r in sec["rows"]:
        v, k = V(r), r["kind"]
        if k == "H" and "chapitre" in r["label"].lower():
            acc["run"] = [0] * ncol
        if k == "A":
            close_detail()
            lastA = r
            for j, x in enumerate(v[:ncol]):
                if x is not None:
                    for a in acc.values():
                        a[j] += x
            if ti is not None and len(v) > ti:
                CHK.eq(t, f"{ed} {t} art {r['code']} {r['label'][:40]}: titles vs total", s(v[:ti]), v[ti])
        elif k == "D":
            dsum = (dsum or 0) + (v[0] or 0)
        elif k in ("S", "T", "B", "I", "R"):
            close_detail()
            ref = acc["sub"] if k == "I" else acc["sec"] if k in ("S", "B") else acc["run"]
            for j, x in enumerate(v[:ncol]):
                CHK.eq(t, f"{ed} {t} {r['label']} (line {r['line']}) col {j}", round(ref[j], 2), x)
            if ti is not None and len(v) > ti:
                CHK.eq(t, f"{ed} {t} {r['label']} (line {r['line']}): titles vs total", s(v[:ti]), v[ti])
            if k == "I":
                acc["sub"] = [0] * ncol
            if k == "B":
                acc["sec"] = [0] * ncol
    close_detail()


def check_societies(sec):
    t, ed = sec["table"], sec["ed"]
    for r in sec["rows"]:
        rc, ex = V(r, 0), V(r, 1)
        CHK.eq(t, f"{ed} L{r['line']} {r['label'][:45]}: receipts parts vs total", s(rc[:-1]), rc[-1])
        CHK.eq(t, f"{ed} L{r['line']} {r['label'][:45]}: expenditure parts vs total", s(ex[:-1]), ex[-1])
        bal = V(r, 2)[0] if len(r["groups"]) > 2 else None
        if bal is not None and rc[-1] is not None and ex[-1] is not None and rc[-1] >= ex[-1]:
            CHK.eq(t, f"{ed} L{r['line']} {r['label'][:45]}: receipts - expenditure vs balance", round(rc[-1] - ex[-1], 2), bal)
    check_running(sec, t, lambda r: len(r["groups"]))


def check_summary(sec):
    t, ed = sec["table"], sec["ed"]
    for r in sec["rows"]:
        a, b, c = V(r, 0)
        if a is not None and b is not None and c is not None and a >= b:
            CHK.eq(t, f"{ed} L{r['line']} {r['label'][:45]}: receipts - expenditure vs balance", round(a - b, 2), c)


def check_kv(sec):
    """institute_budget: 'receipts: X | v' lines, TOTAL lines."""
    t, ed = sec["table"], sec["ed"]
    for side in ("receipts", "expenditure"):
        rows = [r for r in sec["rows"] if r["label"].startswith(side + ":")]
        data = [r for r in rows if "TOTAL" not in r["label"]]
        tot = [r for r in rows if "TOTAL" in r["label"]]
        if tot:
            CHK.eq(t, f"{ed} {sec.get('institute')} {side}: lines vs total", s(V(r)[0] for r in data), V(tot[0])[0])


def check_grid(sec):
    t, ed = sec["table"], sec["ed"]
    data = [r for r in sec["rows"] if not is_total(r["label"])]
    tot = [r for r in sec["rows"] if is_total(r["label"])]
    if tot:
        for j, c in enumerate(sec["cols"]):
            CHK.eq(t, f"{ed} {t} {sec.get('kind', '')} {c}: months vs TOTAUX", s(V(r)[j] for r in data), V(tot[-1])[j])


def check_hospfin(sec):
    """Receipt columns (all before total_receipts) sum to total_receipts; every column sums to the TOTAL row."""
    t, ed = sec["table"], sec["ed"]
    cols = sec["cols"]
    ti = cols.index("total_receipts")
    data = [r for r in sec["rows"] if not is_total(r["label"])]
    for r in sec["rows"]:
        v = V(r)
        CHK.eq(t, f"{ed} L{r['line']} {r['label']}: receipts vs total receipts", s(v[:ti]), v[ti])
    T = [r for r in sec["rows"] if is_total(r["label"])][-1]
    for j, c in enumerate(cols):
        CHK.eq(t, f"{ed} column {c}: hospitals vs {T['label']}", s(V(r)[j] for r in data), V(T)[j])


def check_day_cost(sec):
    """Patient days + staff days (fed, not fed) = total days; cost per day = expenditure / patient days
    (to the printed precision, 1 % tolerance, since the printed price is rounded or truncated)."""
    t, ed = sec["table"], sec["ed"]
    for r in sec["rows"]:
        v = V(r)
        CHK.eq(t, f"{ed} {sec['hospital']} {r['label']}: patient + staff days vs total days", s(v[:3]), v[3])
        if v[4] and v[0] and v[5]:
            CHK.eq(t, f"{ed} {sec['hospital']} {r['label']}: expenditure / patient days vs printed cost per day",
                   round(v[4] / v[0], 3), v[5], tol=max(0.011, 0.01 * v[5]))


def check_etat_receipts(sec):
    rows = sec["rows"]
    CHK.eq(sec["table"], f"{sec['ed']} receipts: titles vs total", s(V(r)[0] for r in rows[:-1]), V(rows[-1])[0])


def run_checks(secs):
    for sec in secs:
        t = sec["table"]
        if t in ("receipts_series", "expenditure_series"):
            check_series(sec)
        elif t == "day_cost":
            check_day_cost(sec)
        elif t == "etat_receipts":
            check_etat_receipts(sec)
        elif t in ("budget_receipts", "budget_expenditure", "child_protection", "budget_summary", "etat_subsidies",
                   "complementary_allocations"):
            check_budget(sec)
        elif t == "societies":
            check_societies(sec)
        elif t == "societies_summary":
            check_summary(sec)
        elif t == "institute_budget":
            check_kv(sec)
        elif t == "arloing_doses":
            check_grid(sec)
        elif t == "hospital_finance":
            check_hospfin(sec)


# ================================================================= build
#
# One CSV per table type (see OUTPUTS). Tables printed for overlapping year windows (the
# ten-year receipt and expenditure series, the two-year budget receipts, the day-cost tables)
# follow SPEC_ADDENDUM rule 4: each year is taken from the latest edition printing it, and every
# other printing is compared. Tables printed once per edition follow rule 5 (all editions kept).

COMMON = ["census", "table_id", "gallica_ark", "source_page", "gallica_view"]

WORDS = [  # French -> English, applied to accent-stripped lower-case labels to build the *_en codes
    ("petites soeurs des pauvres", "little sisters of the poor"), ("doses preparees et distribuees", "doses prepared distributed"),
    ("charbon symptomatique", "blackleg"), ("fievre charbonneuse", "anthrax"), ("rouget du porc", "swine erysipelas"),
    ("diphterie aviaire", "fowl diphtheria"), ("typhon aviaire", "fowl typhoid"), ("piroplasmose", "piroplasmosis"),
    ("antivariolique", "smallpox"), ("antityphoidique", "typhoid"), ("antipesteux", "plague"),
    ("antidiphterique", "diphtheria"), ("antitetanique", "tetanus"), ("anticoquelucheux", "whooping cough"),
    ("antimeningococcique", "meningococcal"), ("antistreptococcique", "streptococcal"),
    ("antistaphylococcique", "staphylococcal"), ("antigonococcique", "gonococcal"), ("antimediterraneen", "mediterranean fever"),
    ("anticholerique", "cholera"), ("antivenimeux", "antivenom"), ("antidysenterique", "dysentery"),
    ("anticharbonneux", "anthrax"), ("anticlaveleux", "sheep pox"), ("claveleux", "sheep pox"),
    ("antisymptomatique", "blackleg"), ("antipneumococcique", "pneumococcal"), ("antigangreneux", "gas gangrene"),
    ("antistreptobacillaire", "streptobacillary"), ("tuberculine", "tuberculin"), ("malleine", "mallein"),
    ("preventif", "preventive"), ("curatif", "curative"), ("sourds-muets et aveugles", "deaf mutes and blind"),
    ("societe francaise de bienfaisance", "french benevolent society"),
    ("societe de bienfaisance francaise", "french benevolent society"),
    ("societe musulmane de bienfaisance", "muslim benevolent society"),
    ("societe italienne de bienfaisance", "italian benevolent society"),
    ("societe de bienfaisance italienne", "italian benevolent society"),
    ("societe israelite de secours et de bienfaisance", "jewish relief and benevolent society"),
    ("caisse de secours et de bienfaisance israelite", "jewish relief and benevolent fund"),
    ("caisse de bienfaisance israelite", "jewish benevolent fund"),
    ("comite israelite de bienfaisance", "jewish benevolent committee"),
    ("comite de bienfaisance israelite", "jewish benevolent committee"),
    ("communaute israelite", "jewish community"), ("conseil de la communaute israelite", "council jewish community"),
    ("societe de secours aux blesses militaires", "society for aid to wounded soldiers"),
    ("union des femmes de france", "union of french women"), ("croix-rouge", "red cross"), ("croix rouge", "red cross"),
    ("croix verte", "green cross"), ("croix-verte", "green cross"), ("goutte de lait", "milk dispensary"),
    ("gouttes de lait", "milk dispensaries"), ("fourneau des pauvres", "poor kitchen"),
    ("cuisines populaires", "soup kitchens"), ("cantines scolaires", "school canteens"),
    ("asile de nuit", "night shelter"), ("maternite", "maternity"), ("garderie", "day nursery"),
    ("vestiaire central", "central clothing store"), ("protection de la jeune fille", "protection of young girls"),
    ("institut heliotherapique", "heliotherapy institute"), ("oeuvre de la creche", "creche charity"),
    ("protection du premier age", "infant protection"), ("protection du 1er age", "infant protection"),
    ("dispensaire", "dispensary"), ("hopital", "hospital"), ("hopitaux", "hospitals"), ("clinique", "clinic"),
    ("soeurs", "sisters"), ("asile des vieillards", "old peoples home"), ("asile de vieillards", "old peoples home"),
    ("vieillards", "elderly"), ("incurables", "incurables"), ("orphelinat", "orphanage"), ("orphelins", "orphans"),
    ("alienes", "insane"), ("tuberculeux", "tuberculous"), ("sourds-muets", "deaf mutes"), ("aveugles", "blind"),
    ("assistance medicale", "medical assistance"), ("assistance aux indigents", "relief of the poor"),
    ("assistance publique", "public assistance"), ("indigents", "poor"), ("enfance", "childhood"), ("enfants", "children"),
    ("subventions exceptionnelles", "exceptional subsidies"), ("subvention", "subsidy"), ("subventions", "subsidies"),
    ("depenses imprevues", "unforeseen expenses"), ("depenses", "expenditure"), ("recettes", "receipts"),
    ("versement au fonds de reserve", "payment to reserve fund"), ("fonds de reserve", "reserve fund"),
    ("fonds de secours", "relief fund"), ("fonds de concours", "contribution fund"), ("placement", "placement"),
    ("legs", "bequest"), ("dotation", "endowment"), ("jeune fille", "young girl"), ("service", "service"),
    ("consultations", "consultations"), ("oeuvre", "charity"), ("oeuvres", "charities"), ("societe", "society"),
    ("secours", "relief"), ("personnel subalterne", "junior staff"), ("personnel", "staff"),
    ("fonctionnement des services", "running of services"), ("ventes de produits", "sales of products"),
    ("subvention de l'etat", "state subsidy"), ("subventions de l'etat", "state subsidies"),
    ("vaccin", "vaccine"), ("serum", "serum"), ("doses", "doses"), ("mere", "mother"), ("meres", "mothers"),
    ("francaise", "french"), ("francais", "french"), ("musulmane", "muslim"), ("musulmans", "muslims"),
    ("israelite", "jewish"), ("israelites", "jewish"), ("italienne", "italian"), ("etrangers", "foreigners"),
    ("bienfaisance", "benevolent"), ("produit", "proceeds"), ("produits", "proceeds"), ("taxe", "tax"),
    ("droit", "duty"), ("amendes", "fines"), ("allocation", "allocation"), ("complementaire", "complementary"),
    ("titre", "title"), ("total", "total"),
]
STOP = {"de", "du", "des", "la", "le", "les", "l", "d", "a", "au", "aux", "et", "en", "pour", "par", "sur", "son",
        "ses", "sa", "m", "mme", "president", "presidente", "directeur", "superieure", "rue"}


def strip_acc(t):
    t = t.replace("œ", "oe").replace("Œ", "Oe")
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")


def en_code(label, maxlen=70):
    t = strip_acc(label).lower()
    t = re.sub(r"[«»\"()\[\]:;,.]", " ", t)
    for fr, en in WORDS:
        t = re.sub(rf"(?<![a-z]){re.escape(fr)}(?![a-z])", en.replace(" ", "_"), t)
    ws = [w for w in re.split(r"[\s'’/-]+", t) if w and w not in STOP]
    code = re.sub(r"_+", "_", "_".join(ws)).strip("_")
    return code[:maxlen].rstrip("_")


def base(sec, view=None, page=None):
    return dict(census=sec["ed"], table_id=sec["table"], gallica_ark=sec["ark"],
                source_page=page or sec["pages"][0], gallica_view=view or sec["views"][0])


def secs_of(all_secs, table):
    return [x for x in all_secs if x["table"] == table]


# ----------------------------------------------------------------- rule-4 series

class Series:
    def __init__(self, table):
        self.table = table
        self.p = defaultdict(dict)       # (year, key) -> {ed: cell}
        self.order = {}

    def add(self, sec, year, key, value, raw, flag, dims, store=True):
        self.p[(year, key)][sec["ed"]] = dict(value=value, raw=raw, flag=flag, sec=sec, dims=dims, store=store)
        self.order.setdefault(key, len(self.order))

    def resolve(self, override=None):
        rows, compared, diffs = [], 0, []
        for (year, key), by in sorted(self.p.items(), key=lambda kv: (kv[0][0], self.order[kv[0][1]])):
            eds = [e for e in ORDER if e in by]
            ed = (override or {}).get((year, key)) or eds[-1]
            for e in eds:
                if e != ed:
                    compared += 1
                    if by[e]["value"] != by[ed]["value"]:
                        diffs.append((year, key, e, by[e]["raw"], ed, by[ed]["raw"]))
            c = by[ed]
            if not c["store"] or c["raw"] in ("-", "—", "."):
                continue
            flag = c["flag"]
            if (self.table, year, key) in REPRINT:
                e2 = REPRINT[(self.table, year, key)]
                c = dict(c, value=by[e2]["value"], sec=by[e2]["sec"])
                flag = "reprint_corrected"
            rows.append(dict(**base(c["sec"]), year=year, **c["dims"], value=c["value"], flag=flag, _key=key,
                             _printed_in=",".join(eds)))
        return rows, compared, diffs


# Rule-4 cells kept from an earlier printing because the latest one is a misprint (reason in COMMENT)
REPRINT = {
    # sgt1930 prints 22,861 for 1927; 1.985.314,45 / 88.784 = 22,361 as printed in sgt1927, sgt1928 and sgt1929
    ("day_cost", 1927, ("sadiki", "cost_per_patient_day")): "sgt1929",
}
OVERRIDE = {}


def norm_label(lab):
    return re.sub(r"\s+", " ", strip_acc(lab).lower().replace("’", "'")).strip(" .")


# ----------------------------------------------------------------- extractors

def ex_receipts_series(all_secs):
    S = Series("receipts_series")
    for sec in secs_of(all_secs, "receipts_series"):
        for r in sec["rows"]:
            tot = is_total(r["label"])
            key = "TOTAUX" if tot else norm_label(r["label"])
            for y, (v, raw, f) in zip(sec["years"], r["groups"][0]):
                S.add(sec, y, key, v, raw, f, dict(line_fr=r["label"], line_en=en_code(r["label"])), store=not tot)
    return S


def ex_expenditure_series(all_secs):
    S = Series("expenditure_series")
    for sec in secs_of(all_secs, "expenditure_series"):
        part = ""
        for r in sec["rows"]:
            if r["kind"] == "H":
                part = r["label"]
                continue
            if is_sub(r["label"]):
                continue
            tot = is_total(r["label"])
            key = "TOTAUX" if tot else norm_label(r["label"])
            for y, (v, raw, f) in zip(sec["years"], r["groups"][0]):
                S.add(sec, y, key, v, raw, f, dict(part_fr=part, line_fr=r["label"], line_en=en_code(r["label"])),
                      store=not tot)
    return S


def ex_budget_receipts(all_secs):
    S = Series("budget_receipts")
    for sec in secs_of(all_secs, "budget_receipts"):
        years = [int(c) for c in sec["cols"]]
        for r in sec["rows"]:
            if r["kind"] not in ("A", "T"):
                continue
            key = r["code"] if r["kind"] == "A" else "TOTAUX"
            for y, (v, raw, f) in zip(years, r["groups"][0]):
                if raw == "mémoire":
                    f = "not_applicable"
                S.add(sec, y, key, v, raw, f, dict(article=r["code"], line_fr=r["label"], line_en=en_code(r["label"])),
                      store=r["kind"] == "A")
    return S


def colmeasure(c):
    lc = strip_acc(c).lower()
    if "en plus" in lc:
        return "diff_plus"
    if "en moins" in lc:
        return "diff_minus"
    if lc.strip() == "total":
        return "total"
    if "allocation complementaire" in lc and "titre" not in lc:
        return "credit_complementary_allocation"
    if re.search(r"tit(re|\.) (ii|2)\b", lc):
        return "credit_title_II_complementary" if "complementaire" in lc else "credit_title_II"
    if re.search(r"titre (i|1)(er)?\b|titre 1er", lc) or "titre i," in lc:
        return "credit_title_I"
    if "dotation forfaitaire" in lc:
        return "credit_lump_sum_allocation"
    return "credit"


def ex_budget_lines(all_secs, tables, keep_kinds=("A", "D")):
    out = []
    for sec in [x for x in all_secs if x["table"] in tables]:
        cols = sec.get("cols") or ["Montant"]
        meas = [colmeasure(c) for c in cols]
        heads, last_art, nrep = [], "", 0
        for r in sec["rows"]:
            k = r["kind"] if r["kind"] else "A"
            if k == "S":
                nrep += 1
            i = min(nrep, len(sec["views"]) - 1)
            vp = r["at"] or (sec["views"][i], sec["pages"][min(i, len(sec["pages"]) - 1)])
            if k == "H":
                heads = (heads + [r["label"]])[-2:]
                continue
            if k not in keep_kinds or (r["kind"] is None and is_total(r["label"])):
                continue
            if k == "A":
                last_art = r["code"]
            for j, (v, raw, f) in enumerate(r["groups"][0] if r["groups"] else []):
                m = meas[j] if j < len(meas) else "credit"
                if k == "D":
                    m = "credit_detail"
                if m in ("diff_plus", "diff_minus", "total") or raw in ("-", "—"):
                    continue
                if raw == "mémoire":
                    f = "not_applicable"
                out.append(dict(**base(sec, view=vp[0], page=vp[1]), year=sec.get("year") or int(sec["ed"][3:]),
                                section_fr=" / ".join(heads), article=r["code"] if k == "A" else last_art,
                                line_type="article" if k == "A" else "detail", line_fr=r["label"],
                                line_en=en_code(r["label"]), measure=m, column_fr=cols[j] if k == "A" and j < len(cols) else "",
                                value=v, flag=f))
    return out


SOC_REC = [("cash_1_january", "En caisse au 1er janvier"), ("festivities_and_donations", "Fêtes et dons"),
           ("public_assistance_subsidies", "Subventions A. P."), ("other_subsidies_and_receipts", "Subventions et recettes diverses"),
           ("total_receipts", "TOTAL")]
SOC_EXP = [("general_expenses", "Frais généraux"), ("relief_cash_or_kind", "Secours en espèces ou nature"),
           ("maintenance_orphans_elderly", "Entretien d'orphelins, vieillards, etc."),
           ("relief_through_work", "Assistance par le travail"), ("medical_assistance", "Assistance médicale"),
           ("other_expenses", "Dépenses diverses"), ("total_expenditure", "TOTAL")]
SOC_BAL = [("cash_remaining_end_of_year", "Reste en caisse au 1er janvier suivant")]
SOC_STAT = [("persons_assisted", "Nombre de personnes secourues"),
            ("relief_grants_cash_or_kind", "Nombre de secours en espèces ou nature"),
            ("persons_medical_assistance", "Nombre de personnes ayant bénéficié de l'assistance médicale"),
            ("repatriations", "Nombre de rapatriements"), ("meals_distributed", "Repas distribués")]
UNREPORTED = defaultdict(list)


def ex_societies(all_secs):
    out = []
    for sec in secs_of(all_secs, "societies"):
        spread = 0      # sgt1926 prints the table over two spreads, separated by an "A reporter" line
        for r in sec["rows"]:
            lab = r["label"]
            if is_sub(lab):
                spread += 1
            if is_total(lab) or is_sub(lab):
                continue
            vw = sec["views"][2 * spread: 2 * spread + 2] if len(sec["views"]) > 2 else sec["views"]
            pg = sec["pages"][2 * spread: 2 * spread + 2] if len(sec["pages"]) > 2 else sec["pages"]
            allraw = [raw for g in r["groups"] for _, raw, _ in g]
            if all(x in ("»", "-", "—") for x in allraw):
                UNREPORTED[sec["ed"]].append(lab)
                continue
            for gi, (g, spec, grp) in enumerate(zip(r["groups"], (SOC_REC, SOC_EXP, SOC_BAL, SOC_STAT),
                                                    ("receipts", "expenditure", "balance", "statistics"))):
                for j, (v, raw, f) in enumerate(g):
                    m, mfr = spec[j]
                    if m.startswith("total") or raw in ("-", "—"):
                        continue
                    out.append(dict(**base(sec, page=pg[0] if gi == 0 else pg[-1], view=vw[0] if gi == 0 else vw[-1]),
                                    year=sec["year"], society_fr=lab, society_en=en_code(lab), group=grp,
                                    measure=m, measure_fr=mfr, value=v,
                                    flag=FLAGS.get(("societies", sec["ed"], r["line"], gi, j), f)))
    return out


def ex_societies_summary(all_secs):
    out = []
    spec = [("total_receipts", "Recettes"), ("total_expenditure", "Dépenses"),
            ("cash_remaining_1_january_next", "Reste en caisse au 1er janvier 1935")]
    for sec in secs_of(all_secs, "societies_summary"):
        for r in sec["rows"]:
            if all(raw in ("»", "-", "—") for g in r["groups"] for _, raw, _ in g):
                UNREPORTED["sgt1935 summary"].append(r["label"])
                continue
            for gi, g in enumerate(r["groups"]):
                sp = spec if gi == 0 else SOC_STAT[:4]
                for j, (v, raw, f) in enumerate(g):
                    m, mfr = sp[j]
                    if raw in ("-", "—"):
                        continue
                    if raw == "déficit":
                        f = "not_applicable"
                    out.append(dict(**base(sec, *(r["at"] or (None, None))),
                                    year=sec["year"], society_fr=r["label"], society_en=en_code(r["label"]),
                                    group="accounts" if gi == 0 else "statistics", measure=m, measure_fr=mfr,
                                    value=v, flag=f))
    return out


def ex_etat_receipts(all_secs):
    out = []
    for sec in secs_of(all_secs, "etat_receipts"):
        for r in sec["rows"][:-1]:
            v, raw, f = r["groups"][0][0]
            out.append(dict(**base(sec), year=sec["year"], line_fr=r["label"], line_en=en_code(r["label"]),
                            value=v, flag=f))
    return out


INST_EN = {"subvention de l'etat": "state_subsidy", "subventions de l'etat": "state_subsidy",
           "subventions particulieres": "private_subsidies", "ventes de produits": "sales_of_products",
           "recettes diverses": "miscellaneous_receipts", "(2e partie) recettes nouvelles": "part2_new_receipts",
           "(2e partie) recettes reportees": "part2_receipts_carried_forward",
           "(3e partie) reste a payer": "part3_outstanding_payments", "(3e partie) restes a payer": "part3_outstanding_payments",
           "personnel": "staff", "personnel subalterne": "junior_staff", "fonctionnement des services": "running_of_services",
           "depenses diverses": "miscellaneous_expenditure", "2e partie, emploi des recettes nouvelles": "part2_use_of_new_receipts",
           "3e partie, depenses des exercices clos": "part3_expenditure_closed_years"}


def ex_institutes(all_secs):
    out = []
    for sec in secs_of(all_secs, "institute_budget"):
        for r in sec["rows"]:
            side, lab = [x.strip() for x in r["label"].split(":", 1)]
            if "TOTAL" in lab:
                continue
            v, raw, f = r["groups"][0][0]
            out.append(dict(**base(sec), year=sec["year"], institute=sec["institute"],
                            institute_fr={"pasteur": "Institut Pasteur", "arloing": "Institut Arloing"}[sec["institute"]],
                            side=side, line_fr=lab, line_en=INST_EN[norm_label(lab)], value=v, flag=f))
    return out


PREFIX = {"X": "Centre vaccinogène", "V": "Service des vaccins microbiens, nombre de doses distribuées",
          "C": "Service des sérums de convalescents", "S": "Sérums thérapeutiques préparés à l'Institut",
          "P": "Produits divers non préparés à l'Institut"}


def ex_pasteur(all_secs):
    out = []
    for sec in secs_of(all_secs, "pasteur_products"):
        for r in sec["rows"]:
            lab = r["label"]
            m = re.match(r"^([XVCSP]): (.*)$", lab)
            if m:
                grp, prod = PREFIX[m.group(1)], m.group(2)
            else:
                grp, prod = [x.strip() for x in lab.split(" / ", 1)]
            v, raw, f = r["groups"][0][0]
            out.append(dict(**base(sec), year=sec["year"], service_fr=grp, product_fr=prod, product_en=en_code(prod),
                            unit_fr="" if r["unit"] == "-" else r["unit"], value=v, flag=f))
    return out


MONTHS = {"Janvier": "january", "Février": "february", "Mars": "march", "Avril": "april", "Mai": "may",
          "Juin": "june", "Juillet": "july", "Août": "august", "Septembre": "september", "Octobre": "october",
          "Novembre": "november", "Décembre": "december"}


def ex_arloing(all_secs):
    out = []
    for sec in secs_of(all_secs, "arloing_doses"):
        units = sec["units"] or [""] * len(sec["cols"])
        for r in sec["rows"]:
            if is_total(r["label"]):
                continue
            for c, u, (v, raw, f) in zip(sec["cols"], units, r["groups"][0]):
                out.append(dict(**base(sec), year=sec["year"], kind=sec["kind"], product_fr=c, product_en=en_code(c),
                                unit_fr=u, month=MONTHS[r["label"]], month_fr=r["label"], value=v, flag=f))
    return out


HF_FR = {"state": "Subventions : État", "temporary_indigenous_contributions": "Subventions : Cotisations temporaires indigènes",
         "public_assistance": "Subventions : Assistance publique", "habous": "Subventions : Habous",
         "municipalities": "Subventions : Municipalités", "municipality": "Subventions : Municipalité",
         "region": "Subventions : Région", "regions": "Subventions : Participation des Régions",
         "communes": "Subventions : Participation des Communes",
         "patient_day_receipts": "Produit des journées d'hospitalisation", "other_receipts": "Autres recettes",
         "expenditure": "Dépenses", "total_expenditure": "Total : Dépenses"}
HF_FR_1925 = {"state": "Subventions : Participation de l'État", "region": "Subventions : Participation de la Région"}


def ex_hospfin(all_secs):
    out = []
    for sec in secs_of(all_secs, "hospital_finance"):
        for r in sec["rows"]:
            if is_total(r["label"]) or all(raw == "»" for _, raw, _ in r["groups"][0]):
                continue      # sgt1923 Gabès: » in every column (no account), not stored
            for c, (v, raw, f) in zip(sec["cols"], r["groups"][0]):
                if c == "total_receipts":
                    continue
                fr = HF_FR_1925.get(c, HF_FR[c]) if sec["ed"] == "sgt1925" else HF_FR[c]
                out.append(dict(**base(sec), year=sec["year"], hospital=r["label"],
                                measure="expenditure" if c == "total_expenditure" else c, column_fr=fr, value=v, flag=f))
    return out


DC_FR = {"patient_days": "Nombre de journées de malades", "staff_days_fed": "Nombre de journées du personnel nourri",
         "staff_days_not_fed": "Nombre de journées du personnel non nourri", "total_days": "Total des journées",
         "expenditure": "Montant des dépenses", "cost_per_patient_day": "Prix moyen (de revient) de la journée de malade"}
HOSP_FR = {"civil": "Hôpital civil français de Tunis", "sadiki": "Hôpital Sadiki",
           "rabta": "Hôpital des contagieux de la Rabta (Ernest-Conseil)"}


def ex_day_cost(all_secs):
    S = Series("day_cost")
    for sec in secs_of(all_secs, "day_cost"):
        for r in sec["rows"]:
            y = int(r["label"])
            for c, (v, raw, f) in zip(sec["cols"], r["groups"][0]):
                S.add(sec, y, (sec["hospital"], c), v, raw, f,
                      dict(hospital=sec["hospital"], hospital_fr=HOSP_FR[sec["hospital"]], measure=c, measure_fr=DC_FR[c]),
                      store=c != "total_days")
    return S


FLAGS = {}   # (table, edition, line, group, col) -> flag, for cells identified as misprints not marked in the files


# ----------------------------------------------------------------- output catalogue

OUTPUTS = {
    # name: (source key, rule, dims, French title, English title, unit)
    "health_assistance_receipts_series": ("receipts_series", 4, ["line_fr", "line_en"],
        "Assistance publique : recettes (séries décennales)",
        "Public assistance budget: receipts by budget line, ten-year series (sgt1922–sgt1926)", "francs"),
    "health_assistance_expenditure_series": ("expenditure_series", 4, ["part_fr", "line_fr", "line_en"],
        "Assistance publique : dépenses (séries décennales)",
        "Public assistance budget: expenditure by budget line, ten-year series (sgt1922–sgt1923)", "francs"),
    "health_assistance_budget_receipts": ("budget_receipts", 4, ["article", "line_fr", "line_en"],
        "Recettes du budget de l'Assistance publique",
        "Public assistance budget: receipts by article, budget year and previous year (sgt1924–sgt1930)", "francs"),
    "health_assistance_budget_credits": ("budget_credits", 5,
        ["section_fr", "article", "line_type", "line_fr", "line_en", "measure", "column_fr"],
        "Dépenses du budget de l'Assistance publique : crédits par article",
        "Public assistance budget: credits (expenditure) by article (sgt1924–sgt1930)", "francs"),
    "health_child_protection_credits": ("child_protection", 5,
        ["section_fr", "article", "line_type", "line_fr", "line_en", "measure", "column_fr"],
        "Répartition des crédits réservés aux œuvres de protection et d'assistance de l'enfance",
        "Credits reserved for child-protection and child-assistance works, by work (sgt1924–sgt1930)", "francs"),
    "health_subsidised_societies": ("societies", 5,
        ["society_fr", "society_en", "group", "measure", "measure_fr"],
        "Situation des sociétés et œuvres subventionnées sur le budget de l'Assistance publique",
        "Accounts of the societies and charities subsidised by public assistance: receipts, expenditure, "
        "cash balance and people assisted (sgt1922–sgt1930)", "francs (statistics: counts)"),
    "health_subsidised_societies_summary": ("societies_summary", 5,
        ["society_fr", "society_en", "group", "measure", "measure_fr"],
        "Situation des sociétés et œuvres subventionnées (récapitulation, sgt1935)",
        "Subsidised societies and charities: total receipts, expenditure, balance and people assisted (sgt1935 layout)",
        "francs (statistics: counts)"),
    "health_assistance_etat_receipts": ("etat_receipts", 5, ["line_fr", "line_en"],
        "État des recettes et des dépenses du budget de l'Assistance publique : I. Recettes",
        "Public assistance budget statement: receipts, credits allotted (sgt1935–sgt1939)", "francs"),
    "health_assistance_etat_subsidies": ("etat_subsidies", 5,
        ["section_fr", "article", "line_type", "line_fr", "line_en", "measure", "column_fr"],
        "État des recettes et des dépenses du budget de l'Assistance publique : II. Dépenses (subventions)",
        "Public assistance budget statement: subsidies granted by society (sgt1935–sgt1939)", "francs"),
    "health_institutes_budget": ("institutes", 5, ["institute", "institute_fr", "side", "line_fr", "line_en"],
        "Institut Pasteur et Institut Arloing : budget",
        "Institut Pasteur and Institut Arloing: budget receipts and expenditure (sgt1922–sgt1930)", "francs"),
    "health_serum_vaccine_doses_pasteur": ("pasteur", 5, ["service_fr", "product_fr", "product_en", "unit_fr"],
        "Institut Pasteur : travaux de l'Institut (vaccins et sérums distribués)",
        "Institut Pasteur: vaccines, serums and other products distributed, by product (sgt1922–sgt1930)",
        "doses or containers, as printed in unit_fr"),
    "health_serum_vaccine_doses_arloing": ("arloing", 5, ["kind", "product_fr", "product_en", "unit_fr", "month", "month_fr"],
        "Institut Arloing : doses de sérums et de vaccins distribuées",
        "Institut Arloing (veterinary): doses of serums and vaccines distributed, by product and month (sgt1922–sgt1930)",
        "doses (or cc. / grammes where unit_fr says so)"),
    "health_hospital_finance": ("hospfin", 5, ["hospital", "measure", "column_fr"],
        "Hôpitaux et infirmeries-dispensaires de l'intérieur : situation financière",
        "Hospitals and infirmaries-dispensaries of the interior: receipts by source and expenditure (sgt1922–sgt1930)",
        "francs"),
    "health_hospital_day_cost": ("day_cost", 4, ["hospital", "hospital_fr", "measure", "measure_fr"],
        "Prix moyen de la journée de traitement",
        "Average cost of a patient-day, with patient-days, staff-days and expenditure: French Civil Hospital, "
        "Sadiki Hospital, Rabta hospital (sgt1922–sgt1935)", "days (counts), francs"),
}
SOURCE_TABLES = {"budget_credits": ("budget_expenditure", "complementary_allocations"),
                 "institutes": ("institute_budget",), "pasteur": ("pasteur_products",), "arloing": ("arloing_doses",),
                 "hospfin": ("hospital_finance",)}
CHECK_TOPICS = {"receipts_series": ["receipts_series"], "expenditure_series": ["expenditure_series"],
                "budget_receipts": ["budget_receipts"], "budget_credits": ["budget_expenditure", "complementary_allocations", "budget_summary"],
                "child_protection": ["child_protection"], "societies": ["societies"], "societies_summary": ["societies_summary"],
                "etat_receipts": ["etat_receipts"], "etat_subsidies": ["etat_subsidies"], "institutes": ["institute_budget"],
                "pasteur": [], "arloing": ["arloing_doses"], "hospfin": ["hospital_finance"], "day_cost": ["day_cost"]}

COLDOC = {
    "census": "edition the value is taken from (`sgt1922` … `sgt1939`)",
    "table_id": "transcription section the value comes from",
    "gallica_ark": "Gallica volume ark (views are numbered within a volume)",
    "source_page": "printed page number (for a table over two pages, the page of the column group)",
    "gallica_view": "Gallica view (fNNNN)",
    "year": "year the value refers to (budget year, account year or calendar year; see below)",
    "flag": "empty, or `derived_from_totals`, `total_mismatch`, `not_applicable`, `illegible`, `reprint_corrected` (see below)",
    "line_fr": "budget line / article label as printed (ditto marks expanded)",
    "line_en": "English code built from the French label (key words translated, place names kept)",
    "part_fr": "part / section of the budget as printed",
    "article": "article number as printed (`-` = printed without a number; letters/prefixes added where the edition "
               "numbers sub-items or restarts numbering by section, see the transcription file)",
    "section_fr": "the last one or two headings printed above the line",
    "line_type": "`article` (a budget line with its own amount) or `detail` (an amount printed in the label column "
                 "breaking down the article above it; do not add details to articles)",
    "measure": "what the value is (see below)",
    "column_fr": "column heading as printed (French)",
    "society_fr": "society / charity name exactly as printed", "society_en": "English code built from the name",
    "group": "column group: `receipts`, `expenditure`, `balance`, `statistics` (`accounts` in the sgt1935 summary)",
    "measure_fr": "column heading (French)",
    "institute": "`pasteur` or `arloing`", "institute_fr": "as printed", "side": "`receipts` or `expenditure`",
    "service_fr": "service heading of the Institut Pasteur report as printed", "product_fr": "product as printed",
    "product_en": "English code", "unit_fr": "unit printed against the product (empty where none is printed)",
    "kind": "`serum` (c) Doses de sérums distribuées) or `vaccine` (d) Doses de vaccins distribuées)",
    "month": "`january` … `december`", "month_fr": "as printed",
    "hospital": "hospital as printed (day-cost table: `civil`, `sadiki`, `rabta`)", "hospital_fr": "hospital name",
}
COMMENT = defaultdict(list)



COMMENT.update({
    "health_assistance_receipts_series": [
        "Table \"Recettes\" of the public-assistance budget, printed in sgt1922–sgt1926 for ten budget years (sgt1925: "
        "eleven), one row per receipt line (tax on gunpowder and arms permits, Nichan-Iftikhar decorations, court "
        "fines, cemetery concessions, theatre tax, etc.). `year` = budget year. Cells printed without an amount "
        "(\"-\": a bracket groups the line with lines carrying the amount) are not stored; printed » = 0. TOTAUX is "
        "not stored (checked, and compared between printings).",
        "From the 1923 budget the receipts are one lump-sum allocation: sgt1923 prints 559.100 across the first nine "
        "lines with a footnote splitting it into \"1° Allocation forfaitaire …\" (529.100) and \"2° Allocations "
        "complémentaires\" (30.000), stored as those two lines; sgt1924 keeps that split for 1923 and prints 745.500 "
        "for 1924 as one bracketed amount; sgt1925 and sgt1926 print each year from 1923 as one bracketed amount, "
        "stored as the line \"Montant unique imprimé en accolade sur les neuf premières lignes\" (a label written by "
        "the transcriber, not printed). The two differences between printings below come from this change of "
        "presentation (1923: split in sgt1924–sgt1925, bracketed in sgt1926, same total). sgt1926 prints 924.100 for "
        "1926, the lump-sum allocation only; the 1926 budget also had a complementary allocation of 95.000 "
        "(`health_assistance_budget_receipts`).",
    ],
    "health_assistance_expenditure_series": [
        "Table \"Dépenses\" of the public-assistance budget, printed in sgt1922 (1913–1922) and sgt1923 (1914–1923): "
        "credits by line (subsidies to the hospitals of the interior, upkeep of French children and of the insane "
        "in France, subsidies to each society, reserve fund, unforeseen expenses). `part_fr` = the part/section "
        "heading as printed (\"Première Partie, Section A/B\", \"Section C\"; sgt1923 also \"Deuxième Partie\", "
        "\"Annexe\"). The \"A reporter\" line of sgt1923 and TOTAUX are not stored.",
        "Failed checks, sgt1922 TOTAUX: 1913 (lines 168.500, printed 168.000), 1919 (lines 238.937,50, printed "
        "252.937,50) and 1920 (lines 350.700, printed 349.700). For 1919 and 1920 sgt1923 prints totals equal to the "
        "sum of the lines (238.937,50 and 350.700), and the sgt1922 figures are those of the receipts series: the "
        "sgt1922 totals line was set from the receipts. The 1913 difference is not resolved (only sgt1922 prints "
        "1913; not re-read cell by cell). sgt1923 prints all years up to 1922 with the same lines and amounts as "
        "sgt1922 (585 comparisons, no difference except these two totals).",
    ],
    "health_assistance_budget_receipts": [
        "\"Recettes\" of the public-assistance budget by article (sgt1924–sgt1930), printed for the budget year and the "
        "previous year; `article` = article number as printed. The \"Total\" sub-lines and TOTAUX GÉNÉRAUX are not "
        "stored. Cells printed \"mémoire\" (pour mémoire, no amount) are stored empty with `not_applicable`; the "
        "\"3. Mémoire. — Dotation Joséphine Virieu\" line of sgt1924–sgt1925 has no amount and is not stored.",
        "Article 1 is the allocation on the receipts collected by the Treasury for public assistance (budget of the "
        "State, chap. III, art. 14, then Titre I art. 13 § 1); article 2 the complementary allocation / exceptional "
        "resources (from 1929 the drawing on the reserve fund).",
    ],
    "health_assistance_budget_credits": [
        "\"Dépenses\" of the public-assistance budget by article (sgt1924–sgt1930), for the edition's budget year. "
        "Column layouts change: sgt1924–sgt1925 one credit column (`credit`); sgt1926 credits on the lump-sum "
        "allocation (`credit_lump_sum_allocation`) and a complementary allocation (`credit_complementary_allocation`); "
        "sgt1927 Titre I (`credit_title_I`), Titre II from the reserve fund (`credit_title_II`) and Titre II from the "
        "complementary allocation on the 1926 surplus (`credit_title_II_complementary`); sgt1928–sgt1930 Titre I and "
        "Titre II. Printed Total columns and the \"différence avec le budget de l'année précédente, en plus / en "
        "moins\" columns are not stored (checked; the totals-line difference is cross-checked against the previous "
        "edition below). Amounts printed in the label column under an article (e.g. the elderly-care subsidies under "
        "\"Vieillards et incurables\") are stored as `line_type` = `detail`, `measure` = `credit_detail`; they break "
        "down the article and must not be added to it. \"A reporter\", section totals (sgt1930) and TOTAUX are not "
        "stored. sgt1928 adds \"Allocations complémentaires à provenir des excédents de recettes de 1927\" (table "
        "`complementary_allocations`, stored with `measure` = `credit`). The child-protection credit (one article) is "
        "broken down in `health_child_protection_credits`. sgt1930 prints the budget as I. Assistance publique "
        "(Dépenses d'État), II. Chapitre 1er (four sections) and a recapitulation; article numbers restart in each "
        "section and are stored with a section prefix (I.1, 1.III.31, …).",
        "Identified misprints (printed value kept, `total_mismatch`): sgt1928 art. 3 (Aliénés) Titre II printed "
        "194.100 (the total 272.000 and all later \"A reporter\" lines need 194.900; re-read on the image); sgt1928 "
        "art. 25 and sgt1929 art. 26 (Œuvre israélite des couvertures) Titre I printed 7.500 with a total of 7.000 "
        "(the \"A reporter\" lines need 7.000; confirmed on the OCR and the image); sgt1929 art. 3 Titre II 292.000 "
        "(272.000 needed); the printed totals of sgt1929 art. 18 (483.000 for 483.400) and art. 50 and 51 (\"1.00\", \"637 60\") are misprints too, but totals are not stored. "
        "Other failed checks are misprinted \"A reporter\" or TOTAUX lines (e.g. sgt1924: en moins 4.000 carried on "
        "page 49, 2.000 everywhere else; total 745.500 against articles summing to 745.450; sgt1927 Titre II "
        "TOTAUX 160.900 against 166.900 in the \"A reporter\" lines and the recapitulation).",
    ],
    "health_child_protection_credits": [
        "\"Tableau de répartition des crédits réservés aux œuvres de protection et d'assistance de l'enfance\" "
        "(annex to the budget, sgt1924–sgt1930; decree of 15 January 1923): credit per work (Dispensaire Alapetite, "
        "Œuvre de la Crèche, orphanages, Institut héliothérapique du Kram, Gouttes de lait by region …). Columns and "
        "conventions as in `health_assistance_budget_credits` (Total and difference columns, \"A reporter\" and "
        "TOTAUX not stored; `detail` lines are breakdowns printed in the label column). sgt1930 adds the \"Crédit "
        "global affecté par le Grand Conseil\" (530.000) to a printed sub-total.",
        "Failed checks: sgt1925 and sgt1929 articles sum to 50 less than the printed TOTAUX (234.950 vs 235.000, "
        "464.950 vs 465.000; re-read on the images: the whole sgt1929 page and the last articles of sgt1925); sgt1928 the \"A reporter\" en plus 54.000 "
        "against cells summing to 51.400; sgt1930 TOTAUX Titre II printed 148.000 (148.800 in the sub-total and the "
        "recapitulation; the TOTAUX line is not stored).",
    ],
    "health_subsidised_societies": [
        "\"Situation des sociétés et œuvres subventionnées sur le budget de l'Assistance publique\" (sgt1922–sgt1930): "
        "one row per society as printed (names exactly as printed; sgt1926 prints them as addressees, \"M. le "
        "Président de la Société …\"). `year` = year of the accounts (the edition's year; cash at 1 January of that "
        "year, cash remaining at 1 January of the next). Groups and measures: `receipts` (`cash_1_january`, "
        "`festivities_and_donations`, `public_assistance_subsidies` = Subventions A. P., "
        "`other_subsidies_and_receipts`), `expenditure` (`general_expenses`, `relief_cash_or_kind`, "
        "`maintenance_orphans_elderly`, `relief_through_work`, `medical_assistance`, `other_expenses`), `balance` "
        "(`cash_remaining_end_of_year`, printed \"Reste en caisse au 1er janvier\" of the next year), `statistics` "
        "(`persons_assisted`, `relief_grants_cash_or_kind`, `persons_medical_assistance`, `repatriations`; sgt1925 "
        "adds `meals_distributed`). Money in francs with centimes; statistics are counts. The two printed TOTAL "
        "columns, \"A reporter\" (sgt1926) and TOTAUX are not stored. A dash printed in a cell is not stored. Rows "
        "printed with » in every cell (no account returned) are not stored; they are listed below.",
        "The printed tables are internally inconsistent in many places (204 of 1.290 checks fail): row totals that do "
        "not add up (often by 0,09–0,90 francs, transposed centimes), balances that are not receipts − expenditure, "
        "and in several editions TOTAUX lines that leave out late rows (sgt1925: the Conseil de la Communauté "
        "israélite de Tunis, 608.293,32 of receipts in column 4, is not in the TOTAUX; in sgt1924 the TOTAUX of \"Frais généraux\", 296.057,79, repeats the sgt1923 total). sgt1923 "
        "repeats the figures of one society under another name (Cuisines populaires musulmanes = Société musulmane de "
        "Tunis; Goutte de lait Lucien Saint de Sfax = Goutte de lait de Sfax); sgt1927 prints the totals of the "
        "Cuisines populaires israélites and the Société italienne in each other's row. All are kept as printed. "
        "The draft transcription was checked against the page images for every row with a failed check in sgt1922, "
        "sgt1924, sgt1927, sgt1928, sgt1929 and sgt1930 and for part of sgt1925 and sgt1926 (row crops at native "
        "resolution), and against the Gallica OCR elsewhere; no transcription error was found in those rows (one "
        "doubtful sgt1928 cell, Goutte de lait de Thala, Subventions A. P. 1.100, is printed so).",
        "Flagged (`total_mismatch`): balances misprinted where receipts and expenditure both agree with their parts "
        "and the next edition's cash at 1 January confirms the computed balance: sgt1926 Société française de Sfax "
        "(printed 534,40; 553,40 computed and carried into sgt1927) and de Bizerte (414,90; 14,90), sgt1927 Société "
        "musulmane de Kairouan (637; 6.377 computed). Cells marked `derived_from_totals` (sgt1923, cut off in the "
        "binding) were solved from the printed row total. sgt1925: \"20 familles\" (persons assisted, Société "
        "française de Kairouan) is stored as 20.",
    ],
    "health_subsidised_societies_summary": [
        "sgt1935 layout of the societies table: total receipts, total expenditure, \"reste en caisse au 1er janvier "
        "1935\" and the four statistics, by society (no TOTAUX line). The year printed in the heading is 1935 for "
        "the balance; the accounts are stored with `year` = 1935. Where the balance is printed \"déficit\" it is "
        "stored empty with `not_applicable`. The \"Nombre de secours\" of the Caisse israélite de Bizerte is printed "
        "\"7.210 95\" (a money amount, apparently misplaced) and stored as 7210.95. Failed checks: three balances "
        "that are not receipts − expenditure (Nabeul 3.815,16 vs 3.815,46; Bizerte musulmane 9.347,66 vs 8.347,66; "
        "Œuvre de la Crèche 46.286,30 vs 46.291,30). Not printed in sgt1936 and sgt1939. The Société française de "
        "Kairouan, printed » in every column, is not stored.",
    ],
    "health_assistance_etat_receipts": [
        "\"État des recettes et des dépenses du budget de l'Assistance publique\", I. Recettes: credits allotted, "
        "Titre I and Titre II (sgt1935, sgt1936, sgt1939; sgt1939: Titre I = special credit on the State budget, "
        "Titre II = cash available in the reserve fund). The total line is not stored; all totals check.",
    ],
    "health_assistance_etat_subsidies": [
        "II. Dépenses of the same statement: subsidies by society and service (Titre I, Titre II; the Total column is "
        "not stored). Sub-items printed under a society heading (a), b) …) are stored with the heading prefixed to "
        "the label (\"Société française de bienfaisance de Tunis : Orphelinat\"). sgt1939 groups the lines by region "
        "and by kind of subsidy (ordinary, exceptional, conditional, complementary; then V. Fonds de réserve) "
        "(`section_fr`), and prints \"Totaux\" before the reserve-fund line and a \"Total général\".",
        "Failed checks: sgt1935 TOTAL, 0,90 franc short: the Legs Joséphine Virieu and the Dépenses imprévues are "
        "printed 637,05 and 10.862,05 (637,50 and 10.862,50 close the total; both flagged `total_mismatch`); sgt1936 "
        "the lines sum to 2.058.100 against 2.050.000 printed for Titre I (8.100 more; every line re-read on the "
        "image, not resolved).",
    ],
    "health_institutes_budget": [
        "a) Budget of the Institut Pasteur de Tunis and of the Institut Arloing (sgt1922–sgt1930; not printed in "
        "sgt1935–sgt1939): receipts and expenditure lines as printed; the Arloing budget has a second part (new "
        "receipts, receipts carried forward and their use) and a third part (amounts outstanding / expenditure of "
        "closed years) in sgt1922–sgt1924. TOTAL lines not stored. Failed checks (printed figures as transcribed; the "
        "lines were compared with the Gallica OCR where it is legible): sgt1923 Arloing receipts 0,60 off; sgt1925 Pasteur receipts 3.000 off; sgt1928 "
        "Arloing expenditure 10.005,95 off; sgt1930 Arloing receipts 40 off. The budget year is the edition's year.",
    ],
    "health_serum_vaccine_doses_pasteur": [
        "b) \"Travaux de l'Institut\" of the Institut Pasteur: only the lines counting vaccines, serums and other "
        "products distributed are stored (the laboratory analyses, rabies treatments and fermentation lines of the "
        "same table are not). `service_fr` = the service heading (Centre vaccinogène; Service des vaccins microbiens, "
        "nombre de doses distribuées; Service des sérums de convalescents; Sérums thérapeutiques préparés à "
        "l'Institut; Produits divers non préparés à l'Institut). `unit_fr` = the unit printed against the line "
        "(doses, flacons, flacons de 10 c.c., ampoules, échantillons); a unit printed once applies to the lines below "
        "it, which are stored with `unit_fr` empty. No totals are printed, so there is no arithmetic check; the "
        "values were compared with the Gallica OCR (every difference was an OCR gap).",
    ],
    "health_serum_vaccine_doses_arloing": [
        "c) \"Doses de sérums distribuées\" (`kind` = `serum`) and d) \"Doses de vaccins distribuées\" (`kind` = "
        "`vaccine`) of the Institut Arloing (veterinary products: sheep-pox, anthrax, blackleg, fowl diseases, "
        "piroplasmosis …), by month. Products change between editions; `product_fr` as printed. `unit_fr` from the "
        "units printed in the totals line (cc., d. = doses, gr.); empty where none is printed. TOTAUX not stored.",
        "Failed checks (cells re-read on the images for sgt1922 and sgt1926; printed as transcribed): sgt1922 "
        "antistreptococcal serum 66 vs 60 cc. and blackleg vaccine 5.575 vs 5.845; sgt1923 anticlaveleux serum, "
        "printed in two sub-columns (e.g. \"100 40\") and stored as decimals (100.40), sums to 424,07 against 405,26; "
        "sgt1926 sheep-pox vaccine 199.973 vs 200.973 and anthrax vaccine 14.705 vs 13.705; sgt1930 anthrax vaccine "
        "11.370 vs 11.376.",
    ],
    "health_hospital_finance": [
        "a) \"Situation financière\" of the hospitals and infirmaries-dispensaries of the interior (sgt1922–sgt1930; "
        "from sgt1935 the interior table has no financial part). `year` = the edition's year, as for the "
        "\"Renseignements généraux\" table in `health_interior_hospitals.csv`. Hospital names as printed. The "
        "columns change with the edition (`measure`, with the heading in `column_fr`): sgt1922–sgt1924 subsidies "
        "from the State, temporary indigenous contributions, public assistance, Habous and municipalities; sgt1925 "
        "participation of the State, the Region and the communes; sgt1926–sgt1927 State, Regions, public assistance, "
        "Habous, municipalities; sgt1928–sgt1930 State, Region, municipality; then in every edition the proceeds of "
        "patient-days (`patient_day_receipts`), other receipts, total receipts (not stored: printed row total) and "
        "expenditure. The TOTAL line is not stored.",
        "This table was not in the inherited draft. It was drafted from the Gallica OCR with column bands taken from "
        "the page rules and then read on the page images, every row, at native resolution (two crops per page); "
        "about 100 OCR misreadings were corrected. Flags: `derived_from_totals` for sgt1922 Enfidaville expenditure "
        "(blotted digit; 9.416,84 is what the column total needs), sgt1927 Djerba State subsidy (first digit lost in "
        "the binding; 20.000 closes the row), sgt1930 Tabarka municipality (printed \"2.00\"; 2.100 closes the row, "
        "the column total would need 1.750); `total_mismatch` for cells that make both their row and their column "
        "disagree and whose correction closes both: sgt1925 Kef and Djerba total receipts (not stored), sgt1927 "
        "Monastir Régions 50.000 (40.000), sgt1928 Souk-el-Arba other receipts 31.673,85 (81.673,85); "
        "`not_applicable` for sgt1925 Ferryville, whose total receipts and expenditure are printed » (its receipts "
        "are not in the printed TOTAL line either). sgt1923 Medjez-el-Bab expenditure is printed \"50.8988 73\" and "
        "stored as 50.898,73 (the value the column total needs). sgt1923 Gabès is printed » in every column "
        "(no account) and is not stored.",
        "The remaining failed checks are in the print: the sgt1929 table in particular (Souk-el-Arba, Madhia, Thala, "
        "Kairouan totals that do not add up; four of seven column totals off), sgt1930 (Sousse, Kairouan, Médenine). "
        "Some rows repeat the previous edition's figures exactly: sgt1929 Bizerte = sgt1928 Bizerte, sgt1930 "
        "Medjez-el-Bab = sgt1929 Medjez-el-Bab; sgt1923 Mateur and Grombalia = sgt1924. They are kept as printed.",
    ],
    "health_hospital_day_cost": [
        "\"Prix moyen de la journée de traitement\" of the Hôpital civil français (e) or b) in the civil-hospital pages), "
        "the Hôpital Sadiki and the Rabta contagious-diseases hospital (b)), sgt1922–sgt1930 and sgt1935 (not printed "
        "in sgt1936 and sgt1939). Measures: `patient_days`, `staff_days_fed`, `staff_days_not_fed` (counts; the Rabta "
        "has half days), `expenditure` (\"Montant des dépenses\", civil hospital \"dépenses ordinaires\", francs), "
        "`cost_per_patient_day` (francs, as printed: two decimals for the civil hospital, three for Sadiki and the "
        "Rabta; = expenditure / patient-days). The printed \"Total des journées\" is not stored (checked and "
        "compared). The civil hospital prints one row (\"Civils\") in sgt1922–sgt1924 and one year in sgt1925, then "
        "three- to five-year windows; Sadiki five- to fourteen-year windows (from 1912); the Rabta from 1918. "
        "sgt1935 prints 1933–1935 without expenditure and cost for 1935 (blank). This table was not in the inherited "
        "draft (the population-table worker skipped it); it was transcribed from the OCR and the page images.",
        "Rule 4 exception: 1927 Sadiki cost per day is printed 22,861 in sgt1930 (the latest printing) and 22,361 in "
        "sgt1927–sgt1929 (1.985.314,45 / 88.784 = 22,361): the sgt1929 value is stored (`reprint_corrected`; re-read "
        "on the image). Other differences between printings are kept per rule 4 (table below): civil 1924 total "
        "days printed 65.850 in sgt1924 (166.252 later; the parts give 166.252) and expenditure 1.900.816,37 "
        "(1.900.811,37 later); civil 1925 total days 148.600 in sgt1925 (164.718 later); Sadiki 1914 expenditure "
        "221.088,07 (sgt1923) / 221.088,17 (sgt1925), 1924 expenditure 1.102.825,72 (sgt1924) / 1.102.826,62 "
        "(sgt1925–sgt1930), 1923 cost per day 10,766 (sgt1923–sgt1924) / 10,889 (sgt1925–sgt1930; computed 10,777).",
        "Failed checks repeated identically in every printing (print errors): Sadiki 1922 total days 133.046 against "
        "parts summing to 133.041, 1916 total 110.835 against 110.825; Rabta 1928 cost per day 11,811 against "
        "474.031,91 / 28.352 = 16,72; Sadiki 1923 cost (above). Single printings: Sadiki 1912 cost 3,237 (computed "
        "3,466); civil 1930 total days 211.161 (parts 211.261); civil 1933 and 1934 cost 29,76 and 27,02 (computed "
        "31,45 and 28,70); Sadiki 1935 staff days fed 16.425 (total 155.776 needs 36.625; the sgt1935 activity table "
        "also prints 16.425). All re-read on the images.",
    ],
})


# ----------------------------------------------------------------- writing

def write_csv(name, rows, dims):
    cols = COMMON + ["year"] + dims + ["value", "flag"]
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


def tr_remarks(all_secs, tables):
    """Transcription comment lines (#) inside the sections of these tables, by edition."""
    out = []
    for ed in ORDER:
        p = TR / f"health_finance_{ed}.txt"
        if not p.exists():
            continue
        cur, lines, buf = None, [], []
        for line in p.read_text().splitlines() + ["[end]"]:
            if line.startswith("["):
                if cur is None:
                    buf = []          # file header comments
                cur = re.match(r"\[(\w+)\]", line).group(1)
                if cur in tables:
                    lines += buf      # comments written just above a section belong to it
                buf = []
            elif line.startswith("#"):
                buf.append(line[1:].strip())
            else:                     # a data or blank line closes the comment block for the current section
                if cur in tables:
                    lines += buf
                buf = []
        if lines:
            out.append(f"- {ed}: " + " ".join(lines))
    return out


def write_notes(name, rows, info, all_secs):
    key, rule, dims, tfr, ten, unit = OUTPUTS[name]
    tables = SOURCE_TABLES.get(key, (key,))
    L = [f"# {tfr}", "", f"*{ten}.*", "",
         "Source: *Statistique générale de la Tunisie*, chapter III (health and assistance), editions "
         + ", ".join(sorted({r['census'] for r in rows} | set(info.get("printed_eds", [])))) + ". Source gallica.bnf.fr / BnF.",
         "", f"Pages and views of the stored values: {fmt_views(rows)}.", "",
         "Transcriptions: `../transcribed/health_finance_<edition>.txt`, sections "
         + ", ".join(f"`[{t}]`" for t in tables) + "; rebuild with "
         "`python3 data-raw/yearbook_health_education/extract_health_finance.py build`. "
         "Per-check output: `health_finance_validation.json`.", ""]
    years = sorted({r["year"] for r in rows})
    L += [f"Rows: {len(rows)}. Years: {years[0]}–{years[-1]}"
          + (f" ({len(years)} years: {', '.join(map(str, years))})" if len(years) != years[-1] - years[0] + 1 else "")
          + f". Unit of `value`: {unit}; amounts are as printed, centimes kept as decimals (printed » = 0).", ""]
    if rule == 4:
        L += ["Printed for overlapping year windows: each year is taken from the **latest** edition that prints it "
              "(SPEC_ADDENDUM rule 4; `census` = that edition) and every other printing of the same cell is compared "
              "below. Duplicate printings are not stored.", "",
              "Years printed by each edition: " + "; ".join(
                  f"{e} {min(ys)}–{max(ys)}" for e, ys in info["printed_years"].items()) + ".", ""]
    else:
        L += ["Printed once per edition; all editions are kept (SPEC_ADDENDUM rule 5).", ""]
    L += ["## Columns", ""]
    for c in COMMON + ["year"] + dims + ["value", "flag"]:
        L.append(f"- `{c}`: {COLDOC.get(c, '')}" if c != "value" else f"- `value`: {unit}; empty where the flag says so")
    L += [""]
    for para in COMMENT[name]:
        L += [para, ""]
    rem = tr_remarks(all_secs, tables)
    if rem:
        L += ["## Remarks recorded in the transcriptions", ""] + rem + [""]
    v = info["checks"]
    L += ["## Validation", "",
          f"- Checks against printed totals: {v['n']}; passed: {v['n'] - len(v['fail'])}; failed: {len(v['fail'])}."]
    if v["fail"]:
        L += ["", "Failed checks (printed values kept, unless a flag below says otherwise; `L<n>` = line of the "
              "transcription file). See the commentary above for which ones were re-read on the page images and "
              "which are repeated identically in several printings:", ""]
        L += [f"  - {x}" for x in v["fail"]]
    if rule == 4:
        L += ["", f"- Overlapping printings: {info['compared']} cell comparisons between editions; "
              f"{len(info['diffs'])} differences."]
        if info["diffs"]:
            kept = {(r["year"], r["_key"]): (r["census"], r["value"], r["flag"]) for r in rows}
            L += ["", "| year | cell | edition | printed | latest edition | printed | stored (edition, flag) |",
                  "|---|---|---|---|---|---|---|"]
            for y, k, e, a, e2, b in info["diffs"]:
                ks = k if isinstance(k, str) else "/".join(k)
                st = kept.get((y, k))
                st = f"{st[1]} ({st[0]}{', ' + st[2] if st[2] else ''})" if st else "not stored (printed total)"
                L.append(f"| {y} | {ks[:60]} | {e} | {a} | {e2} | {b} | {st} |")
    fl = defaultdict(int)
    for r in rows:
        if r["flag"]:
            fl[r["flag"]] += 1
    L += ["", "- Flagged cells: " + (", ".join(f"{k}: {n}" for k, n in sorted(fl.items())) if fl else "none") + "."]
    if fl:
        L += [""] + [f"  - {r['census']} {r['year']} " + " / ".join(str(r[d]) for d in dims if r.get(d) not in (None, "") and not d.endswith("_en"))[:160]
                     + f" = {r['value']} ({r['flag']})" for r in rows if r["flag"]]
    for x in info.get("xchk", []):
        L += ["", x]
    (OUT / f"{name}.md").write_text("\n".join(L) + "\n")


# ----------------------------------------------------------------- cross-checks

def fm(v):
    return "" if v is None else (f"{v:.2f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v))


def xc_day_cost(day_series):
    """Patient-days and staff-days of the day-cost tables against the validated hospital activity tables
    (csv/health_hospital_civil_activity.csv, health_sadiki_activity.csv, health_rabta_activity.csv), for every
    printing of the day-cost table (not only the stored one)."""
    files = {"civil": "health_hospital_civil_activity.csv", "sadiki": "health_sadiki_activity.csv",
             "rabta": "health_rabta_activity.csv"}
    act = {}
    for h, fn in files.items():
        p = OUT / fn
        if not p.exists():
            continue
        with p.open() as f:
            for r in csv.DictReader(f):
                if r["indicator"] in ("patient_days", "staff_days_fed", "staff_days_not_fed") and r["value"]:
                    act[(h, int(r["year"]), r["indicator"])] = (float(r["value"]), r["census"])
    n = eq = 0
    lines = []
    for (year, (h, c)), by in sorted(day_series.p.items()):
        if c not in ("patient_days", "staff_days_fed", "staff_days_not_fed"):
            continue
        a = act.get((h, year, c))
        if not a:
            continue
        for e, cell in by.items():
            if cell["value"] is None:
                continue
            n += 1
            if abs(cell["value"] - a[0]) < 0.01:
                eq += 1
            else:
                lines.append(f"{h} {year} {c}: day-cost table ({e}) {cell['raw']} vs activity table ({a[1]}) {fm(a[0])}")
    miss = sorted({(h, y) for (y, (h, c)), _ in day_series.p.items() if c == "patient_days"
                   and (h, y, "patient_days") not in act})
    return n, eq, lines, miss


def xc_budget(all_secs, S_rec, S_exp):
    """Totals of the same budget year printed in different tables and editions."""
    tot = defaultdict(dict)    # year -> {what: value}
    for (y, k), by in S_rec.p.items():
        if k == "TOTAUX":
            for e, c in by.items():
                tot[y][f"receipts series TOTAUX ({e})"] = c["value"]
    for (y, k), by in S_exp.p.items():
        if k == "TOTAUX":
            for e, c in by.items():
                tot[y][f"expenditure series TOTAUX ({e})"] = c["value"]
    for sec in secs_of(all_secs, "budget_receipts"):
        T = [r for r in sec["rows"] if r["kind"] == "T"][-1]
        for y, (v, raw, f) in zip([int(c) for c in sec["cols"]], T["groups"][0]):
            tot[y][f"budget receipts TOTAUX ({sec['ed']})"] = v
    credT = {}
    for sec in secs_of(all_secs, "budget_expenditure"):
        summ = [x for x in all_secs if x["table"] == "budget_summary" and x["ed"] == sec["ed"]]
        src = summ[0] if summ else sec
        meas = [colmeasure(c) for c in src["cols"]]
        if summ:   # sgt1930: no grand total in the detailed table; the recapitulation lines add up to it
            v = [s(V(r)[j] for r in src["rows"] if r["kind"] == "A") for j in range(len(meas))]
        else:
            v = V([r for r in sec["rows"] if r["kind"] in ("T", "R")][-1])
        tot_j = meas.index("total") if "total" in meas else None
        cr = v[tot_j] if tot_j is not None else s(x for x, m in zip(v, meas) if m.startswith("credit"))
        tot[sec["year"]][f"budget credits TOTAUX ({sec['ed']})"] = cr
        if "diff_plus" in meas:
            j = meas.index("diff_plus")
            credT[sec["year"]] = (v[j - 1], v[j], v[j + 1] if len(v) > j + 1 else None, sec["ed"], src["cols"][j - 1])
    n = eq = 0
    lines = []
    for y in sorted(tot):
        vals = tot[y]
        if len(vals) < 2:
            continue
        ref = list(vals.items())[0]
        for k, v in list(vals.items())[1:]:
            if v is None or ref[1] is None:
                continue
            n += 1
            if abs(v - ref[1]) < 0.01:
                eq += 1
            else:
                lines.append(f"{y}: {ref[0]} {fm(ref[1])} vs {k} {fm(v)}")
    # printed differences with the previous budget (totals line): en plus - en moins = total(N) - total(N-1)
    for y, (cr, dp, dm, ed, cname) in sorted(credT.items()):
        prev = tot.get(y - 1, {})
        pv = next((v for k, v in prev.items() if k.startswith("budget credits")), None) or \
            next((v for k, v in prev.items() if k.startswith("budget receipts")), None)
        if pv is None or dp is None:
            continue
        n += 1
        d = round(cr - pv, 2)
        if abs(d - ((dp or 0) - (dm or 0))) < 0.01:
            eq += 1
        else:
            lines.append(f"{y} ({ed}): printed difference with {y - 1} (en plus {fm(dp)} - en moins {fm(dm or 0)}) vs "
                         f"column '{cname[:40]}' {fm(cr)} - total {y - 1} {fm(pv)} = {fm(d)}")
    return n, eq, lines


def xc_child(all_secs):
    """Child-protection table total against the article of the main budget that reserves the credit."""
    n = eq = 0
    lines = []
    for sec in secs_of(all_secs, "child_protection"):
        T = [r for r in sec["rows"] if r["kind"] in ("T", "R")][-1]
        meas = [colmeasure(c) for c in sec["cols"]]
        cp = V(T)[meas.index("total")] if "total" in meas else V(T)[0]
        main = [x for x in all_secs if x["table"] in ("budget_expenditure", "budget_summary") and x["ed"] == sec["ed"]]
        cand = []
        for m in main:
            mm = [colmeasure(c) for c in m["cols"]]
            for r in m["rows"]:
                if r["kind"] == "A" and re.search(r"(?i)enfance", r["label"]):
                    v = V(r)
                    cand.append((r["label"][:60], v[mm.index("total")] if "total" in mm else v[0]))
        if not cand:
            continue
        n += 1
        if any(abs((c or 0) - cp) < 0.01 for _, c in cand):
            eq += 1
        else:
            lines.append(f"{sec['ed']}: child-protection TOTAUX {fm(cp)} vs main-budget article(s) "
                         + "; ".join(f"{a!r} {fm(c)}" for a, c in cand))
    return n, eq, lines


def xc_societies(soc_rows):
    """Cash at 1 January of year N against the cash remaining at the end of year N-1 (previous edition), for
    societies whose name code matches in both editions."""
    by = {}
    for r in soc_rows:
        if r["measure"] in ("cash_1_january", "cash_remaining_end_of_year"):
            by[(r["society_en"], r["year"], r["measure"])] = r["value"]
    n = eq = 0
    lines = []
    for (soc, y, m), v in sorted(by.items()):
        if m != "cash_1_january":
            continue
        p = by.get((soc, y - 1, "cash_remaining_end_of_year"))
        if p is None or v is None:
            continue
        n += 1
        if abs(p - v) < 0.01:
            eq += 1
        else:
            lines.append(f"{soc} {y}: cash at 1 January {fm(v)} vs cash remaining end {y - 1} {fm(p)}")
    return n, eq, lines


# ----------------------------------------------------------------- main

def build(write=True):
    all_secs = []
    for ed in ORDER:
        all_secs += parse(ed)
    run_checks(all_secs)
    series = {"receipts_series": ex_receipts_series(all_secs), "expenditure_series": ex_expenditure_series(all_secs),
              "budget_receipts": ex_budget_receipts(all_secs), "day_cost": ex_day_cost(all_secs)}
    other = {"budget_credits": ex_budget_lines(all_secs, ("budget_expenditure", "complementary_allocations")),
             "child_protection": ex_budget_lines(all_secs, ("child_protection",)),
             "etat_subsidies": ex_budget_lines(all_secs, ("etat_subsidies",)),
             "societies": ex_societies(all_secs), "societies_summary": ex_societies_summary(all_secs),
             "etat_receipts": ex_etat_receipts(all_secs), "institutes": ex_institutes(all_secs),
             "pasteur": ex_pasteur(all_secs), "arloing": ex_arloing(all_secs), "hospfin": ex_hospfin(all_secs)}
    X = {"day_cost": xc_day_cost(series["day_cost"]),
         "budget": xc_budget(all_secs, series["receipts_series"], series["expenditure_series"]),
         "child": xc_child(all_secs), "societies": xc_societies(other["societies"])}
    results = {}
    for name, (key, rule, dims, *_ ) in OUTPUTS.items():
        if key in series:
            rows, compared, diffs = series[key].resolve(OVERRIDE)
            py = defaultdict(set)
            for (y, k), by in series[key].p.items():
                for e in by:
                    py[e].add(y)
            printed = {e: sorted(py[e]) for e in ORDER if e in py}
        else:
            rows, compared, diffs, printed = other[key], 0, [], {}
        topics = CHECK_TOPICS[key]
        fails = [f for t in topics for f in CHK.fail[t]]
        if key in ("etat_subsidies", "budget_credits", "child_protection"):
            pass
        results[name] = dict(rows=rows, compared=compared, diffs=diffs, printed_years=printed,
                             printed_eds=sorted(printed), checks=dict(n=sum(CHK.n[t] for t in topics), fail=fails), xchk=[])
    n, eq, lines, miss = X["day_cost"]
    results["health_hospital_day_cost"]["xchk"].append(
        f"## Cross-check with the hospital activity tables\n\nPatient-days and staff-days (fed, not fed) of every "
        f"printing of the day-cost tables against `health_hospital_civil_activity.csv`, `health_sadiki_activity.csv` "
        f"and `health_rabta_activity.csv` (the validated \"Mouvement de la population\" tables): {n} comparisons, "
        f"{eq} equal, {n - eq} different.\n" + "".join(f"  - {x}\n" for x in lines)
        + (f"\nYears of the day-cost tables with no patient-days in the activity tables: "
           + ", ".join(f"{h} {y}" for h, y in miss) + ".\n" if miss else ""))
    n, eq, lines = X["budget"]
    txt = (f"## Cross-check of budget totals\n\nThe total of each budget year printed in the receipt series, the "
           f"expenditure series, the receipts table and the credits table of every edition that prints it, and the "
           f"printed difference with the previous budget (totals line) against the two totals: {n} comparisons, {eq} equal.\n"
           + "".join(f"  - {x}\n" for x in lines))
    for nm in ("health_assistance_receipts_series", "health_assistance_expenditure_series",
               "health_assistance_budget_receipts", "health_assistance_budget_credits"):
        results[nm]["xchk"].append(txt)
    n, eq, lines = X["child"]
    results["health_child_protection_credits"]["xchk"].append(
        f"## Cross-check with the main budget\n\nTotal of the child-protection table against the article of the "
        f"main budget that reserves the credit (same edition): {n} comparisons, {eq} equal.\n"
        + "".join(f"  - {x}\n" for x in lines))
    n, eq, lines = X["societies"]
    results["health_subsidised_societies"]["xchk"].append(
        f"## Cross-check between editions\n\nCash at 1 January of year N against the cash remaining at the end of "
        f"year N−1 printed in the previous edition, for societies whose name code is the same in both editions: "
        f"{n} comparisons, {eq} equal.\n" + "".join(f"  - {x}\n" for x in lines))
    results["health_subsidised_societies"]["xchk"].insert(0, "## Rows printed with no figures (not stored)\n\n" + "".join(
        f"- {ed}: " + "; ".join(UNREPORTED[ed]) + "\n" for ed in ORDER if UNREPORTED.get(ed)))
    results["health_hospital_day_cost"]["xchk"].append(
        "The 11 differences are three cells, each printed identically in every day-cost table: Sadiki 1925 staff "
        "days not fed 18.505 (the day-cost total 137.500 needs 18.505; the sgt1926 activity table prints 18.501), "
        "civil 1927 staff days fed 76.147 (the day-cost total 225.199 needs 76.147; the sgt1928 activity table prints "
        "76.900), Sadiki 1935 staff days not fed 35.645 (the activity tables print 55.645; neither closes the printed "
        "total 155.776). All patient-day counts agree (the 1929 civil patient-days, 110.146, equal the value the "
        "activity table took from sgt1929 as `reprint_corrected`; the sgt1930 activity table prints 110.446).")
    if write:
        OUT.mkdir(exist_ok=True)
        for name, (key, rule, dims, *_ ) in OUTPUTS.items():
            write_csv(name, results[name]["rows"], dims)
            write_notes(name, results[name]["rows"], results[name], all_secs)
        val = {name: dict(rows=len(r["rows"]), checks=r["checks"]["n"], failed=r["checks"]["fail"],
                          overlap_compared=r["compared"], overlap_diffs=[list(map(str, d)) for d in r["diffs"]])
               for name, r in results.items()}
        val["_cross_checks"] = {k: dict(n=v[0], equal=v[1], differences=v[2]) for k, v in X.items()}
        (OUT / "health_finance_validation.json").write_text(json.dumps(val, indent=1, ensure_ascii=False) + "\n")
    return results, X


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    res, X = build(write=(cmd == "build"))
    for name, r in res.items():
        print(f"{name}: {len(r['rows'])} rows; checks {r['checks']['n']}, failed {len(r['checks']['fail'])}; "
              f"overlap compared {r['compared']}, diffs {len(r['diffs'])}")
    for k, v in X.items():
        print(f"cross-check {k}: {v[1]}/{v[0]} equal")
    if cmd == "check":
        for name, r in res.items():
            for f_ in r["checks"]["fail"]:
                print("  FAIL", f_)
            for d in r["diffs"]:
                print("  DIFF", name, d)
        for k, v in X.items():
            for l_ in v[2]:
                print("  XCHK", k, l_)
