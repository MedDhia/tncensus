#!/usr/bin/env python3
"""Expulsions and naturalisations from the Statistique générale de la Tunisie.

Builds tidy CSVs in data-raw/yearbook_demography/csv/ from the hand
transcriptions in data-raw/yearbook_demography/transcribed/ (read from the page
images of the 1922-1939 editions), checks every printed total, compares the
overlapping printings, and writes a notes file next to each CSV.

Usage:  python3 data-raw/yearbook_demography/extract_expulsions_naturalisations.py
"""
import csv
import re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
TR = HERE / "transcribed"
OUT = HERE / "csv"

ARKS = {"sgt1922": "bpt6k9105649x", "sgt1923": "bpt6k9105649x", "sgt1924": "bpt6k9105649x",
        "sgt1925": "bpt6k9105650k", "sgt1926": "bpt6k9105650k", "sgt1927": "bpt6k91056510",
        "sgt1928": "bpt6k91056510", "sgt1929": "bpt6k9105652d", "sgt1930": "bpt6k9105652d",
        "sgt1935": "bpt6k9105653t", "sgt1936": "bpt6k91056547", "sgt1939": "bpt6k9105739w"}
SOURCE = ("*Statistique générale de la Tunisie*, Régence de Tunis (annual). Source "
          "gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR). Editions and views: "
          "see `EDITIONS.md`.")

CHECKS = defaultdict(lambda: [0, 0])      # table -> [checks, passed]
FAILS = defaultdict(list)                 # table -> messages


def num(tok):
    tok = tok.strip()
    if tok in ("»", "_", ""):
        return 0
    return int(tok.replace(".", ""))


def check(table, label, computed, printed):
    CHECKS[table][0] += 1
    if computed == printed:
        CHECKS[table][1] += 1
    else:
        FAILS[table].append(f"{label}: computed {computed} != printed {printed}")
    return computed == printed


def write(name, header, rows):
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / f"{name}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def notes(name, title, body, table_key):
    c, p = CHECKS[table_key]
    fails = "".join(f"- {m}\n" for m in FAILS[table_key])
    (OUT / f"{name}.md").write_text(
        f"# {title}\n\nSource: {SOURCE}\n\n{body.strip()}\n\n"
        f"## Validation\n\n{p} of {c} printed-total checks pass."
        + (f" Failing checks (each re-read on the image at full resolution; printed values kept):\n\n{fails}" if fails else "\n")
        + "\nCommon columns: `census` (source edition, e.g. `sgt1930`), `gallica_ark` (volume ark), "
          "`table_id`, `source_page` (printed page), `gallica_view`, `value`, `flag` (empty, "
          "`ocr_corrected`, `illegible`, `total_mismatch`, `derived_from_totals`, `not_applicable`, "
          "`reprint_corrected`; see `data-raw/colonial_census/SPEC.md`). A printed `»` is stored as 0. "
          "Printed totals are not stored; they were used for validation.\n",
        encoding="utf-8")


# ---------------------------------------------------------------- expulsions
EXP_NAT = {"Allemands": "german", "Anglais": "british", "Anglo-Maltais": "anglo_maltese",
           "Autrichiens": "austrian", "Belges": "belgian", "Egyptiens": "egyptian",
           "Espagnols": "spanish", "Grecs": "greek", "Italiens": "italian",
           "Marocains": "moroccan", "Ottomans": "ottoman", "Russes": "russian",
           "Suisses": "swiss", "Divers": "other"}


def parse_blocks(path):
    blocks, cur = [], None
    for ln in path.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        if ln.startswith("@"):
            p = ln[1:].split()
            if len(p) == 3:                       # "@ edition views pages" (no ark)
                p = [p[0], ARKS[p[0]], p[1], p[2]]
            cur = {"edition": p[0], "ark": p[1], "view": p[2], "page": p[3], "rows": [], "total": None}
            blocks.append(cur)
        elif ln.startswith("years") or ln.startswith("cols"):
            cur["cols"] = ln.split("|", 1)[1].split()
        elif ln.startswith("="):
            cur["total"] = ln.split("|", 1)[1].split()
        else:
            lab, vals = [s.strip() for s in ln.split("|", 1)]
            cur["rows"].append((lab, vals.split()))
    return blocks


def expulsions():
    t = "expulsions"
    blocks = parse_blocks(TR / "expulsions.txt")
    printings = defaultdict(dict)       # (year, nat) -> {edition: value}
    where = {}
    prev_1924 = {}
    for b in blocks:
        years = [int(y) for y in b["cols"] if y != "TOTAUX"]
        has_row_total = "TOTAUX" in b["cols"]
        sums = [0] * len(years)
        for lab, vals in b["rows"]:
            v = [num(x) for x in vals]
            cells = v[:len(years)]
            for i, y in enumerate(years):
                printings[(y, lab)][b["edition"]] = cells[i]
                sums[i] += cells[i]
            if has_row_total:
                extra = 0
                if b["edition"] == "sgt1935":       # row totals cover 1924-1934
                    extra = prev_1924.get(lab, 0)
                check(t, f"{b['edition']} {lab} row total", sum(cells) + extra, v[len(years)])
            if b["edition"] == "sgt1930":
                prev_1924[lab] = cells[years.index(1924)]
        tot = [num(x) for x in b["total"]]
        for i, y in enumerate(years):
            check(t, f"{b['edition']} {y} column total", sums[i], tot[i])
        if has_row_total:
            extra = sum(prev_1924.values()) if b["edition"] == "sgt1935" else 0
            check(t, f"{b['edition']} grand total", sum(sums) + extra, tot[len(years)])
        for y in years:
            where[(b["edition"], y)] = b
    # series: latest edition printing each year
    order = list(ARKS)
    rows, diffs, compared, equal = [], [], 0, 0
    for (y, lab), eds in sorted(printings.items()):
        latest = max(eds, key=order.index)
        b = where[(latest, y)]
        for e, v in eds.items():
            if e == latest:
                continue
            compared += 1
            if v == eds[latest]:
                equal += 1
            else:
                diffs.append(f"{y} {lab}: {e} prints {v}, {latest} prints {eds[latest]}")
        rows.append(["sgt" + latest[3:], ARKS[latest], "expulsions", int(b["page"]), int(b["view"]),
                     y, EXP_NAT[lab], lab, eds[latest], ""])
    n = write("expulsions_nationality",
              ["census", "gallica_ark", "table_id", "source_page", "gallica_view", "year",
               "nationality", "nationality_fr", "value", "flag"], rows)
    years = sorted({r[5] for r in rows})
    body = f"""
*Expulsions prononcées*, by nationality, {years[0]}-{years[-1]}. {n} rows: one per
nationality and year. Each edition prints the last ten years (sgt1922: 1913-1922 ...
sgt1935: 1925-1934; the 1936 and 1939 editions print no expulsions table). Each year
is taken from the latest edition that prints it (`census` names that edition).

Columns: `year`, `nationality` (English code), `nationality_fr` (as printed: Allemands,
Anglais, Anglo-Maltais, Autrichiens, Belges, Egyptiens, Espagnols, Grecs, Italiens,
Marocains, Ottomans, Russes, Suisses, Divers = `other`), `value` = persons expelled.

## Comparison of the overlapping printings

Every cell of every other printing of the same year was compared with the kept value:
{compared} comparisons, {equal} equal, {compared - equal} different:

""" + "".join(f"- {d}\n" for d in diffs) + """
What the differences mean:

- **Swiss and Russians, 1913-1923.** The 1922 and 1923 editions print under *Russes* the
  figures that the 1924 and later editions print under *Suisses*, and vice versa. Every
  later edition uses the 1924 assignment, which is kept here; but 1913 and 1914 are
  printed only in the 1922/1923 editions, so their Swiss and Russian values follow the
  1922/1923 labels and may be swapped. Use the two together if in doubt.
- **Italians, 1922.** The 1922-1925 editions print 33 (1922 total 44). The 1926 and
  1927 editions print 35 but leave the totals at the values implied by 33 (row totals
  463 and 475, 1922 total 44); from 1928 the totals are corrected (1922 total 46). The
  kept value is 35 (sgt1930), consistent with its own totals.
- **1917, Ottomans:** blank in the 1922-1925 editions, `»` from 1926; stored as 0.

## Printed totals

- The 1919 column total is printed 102 in the 1922-1926 editions, but its cells sum to
  80 in every printing; the 1924 edition's grand total (771) agrees with 80, and the
  1927 and later editions print 80.
- In sgt1935 the TOTAUX column covers 1924-1934 (eleven years) although the table shows
  only 1925-1934; the row and grand totals check once the 1924 values (from sgt1930)
  are added.
"""
    notes("expulsions_nationality", "Expulsions by nationality, 1913-1934", body, t)
    return n


# ---------------------------------------------------------- naturalisations a
def naturalisations_granted():
    t = "nat_a"
    rows, by_ed = [], defaultdict(dict)
    meta = {}
    with open(TR / "naturalisations_small.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            by_ed[r["edition"]][r["item"]] = num(r["value"])
            meta[r["edition"]] = (int(r["page"]), int(r["view"]))
            if r["section"] == "granted":
                rows.append([r["edition"], ARKS[r["edition"]], "a", int(r["page"]), int(r["view"]),
                             int(r["edition"][3:]), r["sex"], r["item"], r["item_fr"],
                             num(r["value"]), ""])
    for e, d in by_ed.items():
        g = {k: v for k, v in d.items() if not k.startswith(("total", "grand"))}
        minors = sum(v for k, v in g.items() if k.startswith("minor"))
        adults = sum(g.values()) - minors
        if e in ("sgt1922", "sgt1923", "sgt1924", "sgt1925", "sgt1926", "sgt1927", "sgt1928", "sgt1929"):
            # TOTAL excludes the women reinstated, who are added only in the grand total
            check(t, f"{e} total naturalisations", adults - g.get("women_reinstated", 0), d["total_adults"])
        else:
            check(t, f"{e} total adults", adults, d["total_adults"])
        check(t, f"{e} total minors", minors, d["total_minors"])
        check(t, f"{e} grand total", adults + minors, d["grand_total"])
    n = write("naturalisations_granted",
              ["census", "gallica_ark", "table_id", "source_page", "gallica_view", "year", "sex",
               "item", "item_fr", "value", "flag"], rows)
    body = f"""
Table a) *Naturalisations individuelles*: naturalisations granted in the edition year,
by category. {n} rows; years 1922-1930, 1935, 1936, 1939 (one edition each; `year` is
the edition year).

Columns: `sex`, `item` (English code), `item_fr` (printed heading), `value` = persons.

The categories change over time, so not every `item` exists every year:

- 1922-1929: men (civilians / soldiers), women naturalised, adult children naturalised
  with their parents (sons / daughters), women reinstated, minor children naturalised
  *définitivement* (and, in 1922-1923, *conditionnellement*) by sex.
- 1930-1936: minors are no longer split definitive/conditional (`minor_boys`, `minor_girls`).
- 1939: men naturalised / reinstated (no civilian/military split); no adult children.

In 1922-1929 the printed TOTAL excludes the women reinstated, who appear only in the
TOTAL GÉNÉRAL; from 1930 the adult total includes them. The grand totals equal the
annual totals of table e (e.g. 1925: 3.298; 1930: 1.609; 1935: 668).
"""
    notes("naturalisations_granted", "Naturalisations granted, by category (table a)", body, t)
    return n


# ------------------------------------------------------- naturalisations b-d
MS = ["single", "married_french_origin_wife", "married_foreign_origin_wife", "widowed", "divorced"]
MS_FR = ["Célibataires", "Mariés avec des femmes d'origine française",
         "Mariés avec des femmes d'origine étrangère", "Veufs", "Divorcés"]
WS = ["single", "married", "widowed", "divorced"]
WS_FR = ["Célibataires", "Mariées", "Veuves", "Divorcées"]
RES = [("more_than_10_years", "civilian"), ("more_than_10_years", "military"),
       ("less_than_10_years", "civilian"), ("less_than_10_years", "military")]
BIRTH = [("french_territory", "male"), ("french_territory", "female"), ("abroad", "male"), ("abroad", "female")]
AGE = [("under_25", "Moins de 25 ans"), ("25_40", "De 25 à 40 ans"), ("over_40", "Plus de 40 ans")]
PROF_FR = {"army": "Armée", "agriculture": "Agriculteurs", "commerce_industry": "Commerce et industrie",
           "employees_commerce_admin": "Employés de commerce ou d'administration",
           "industry_employees_workers": "Employés et ouvriers d'industrie",
           "cafe_keepers": "Cafetiers et débitants de boissons", "maritime_fishing": "Pêche maritime",
           "owners_rentiers": "Propriétaires et rentiers", "liberal_professions": "Professions libérales",
           "other": "Autres professions"}
TRADE_FR = {"army": "Armée", "farmers": "Agriculteurs", "butchers": "Bouchers", "drivers": "Chauffeurs auto",
            "chemists": "Chimistes", "hairdressers": "Coiffeurs", "traders": "Commerçants",
            "accountants": "Comptables", "electricians": "Electriciens",
            "administration_employees": "Employés d'administration",
            "public_works_employees": "Employés des travaux publics", "commerce_employees": "Employés de commerce",
            "public_works_contractors": "Entrepreneurs des travaux publics", "students": "Etudiants",
            "blacksmiths": "Forgerons", "surveyors": "Géomètres", "engineers": "Ingénieurs",
            "teachers": "Instituteurs", "day_labourers": "Journaliers", "masons": "Maçons",
            "mechanics": "Mécaniciens", "joiners": "Menuisiers", "miners": "Mineurs", "doctors": "Médecins",
            "fishermen": "Pêcheurs", "rentiers": "Rentiers", "bakers": "Boulangers", "employees": "Employés",
            "wheelwrights": "Charrons", "shoemakers": "Cordonniers", "painters": "Peintres",
            "dentists": "Dentistes", "jewellers": "Bijoutiers", "lawyers": "Avocats",
            "boilermakers": "Chaudronniers", "surveyors_draughtsmen": "Géomètres dessinateurs",
            "tailors": "Tailleurs", "locksmiths": "Serruriers", "cft_workers": "Ouvriers C.F.T.",
            "sales_representatives": "Représentants de commerce"}
NAT_FR = {"german": "Allemands", "austrian": "Autrichiens", "alsace_lorraine": "Alsaciens-Lorrains",
          "british_anglo_maltese": "Anglais et Anglo-Maltais", "anglo_maltese": "Anglo-Maltais",
          "belgian": "Belges", "spanish": "Espagnols", "italian": "Italiens",
          "algerian_jew_pre1870": "Israélites-Algériens (avant 1870)", "algerian_jew": "Israélites-Algériens",
          "luxembourger": "Luxembourgeois", "moroccan": "Marocains", "algerian_muslim": "Musulmans-Algériens",
          "swiss": "Suisses", "tunisian": "Tunisiens", "tunisian_muslim": "Musulmans Tunisiens",
          "tunisian_jew": "Israélites Tunisiens", "russian": "Russes", "other": "Autres nationalités"}
# cells confirmed on the image as printed although they do not add up
MEN_TOTAL = {}
BCD_MISPRINTS = {("sgt1922", "b_men"): "the men's total 128 includes the adult son (122 + 5 + 1); table c gives 127",
                 ("sgt1924", "b_men"): "cells sum to 433, printed total 434",
                 ("sgt1928", "c_prof"): "professions sum to 955, printed total 855 (Employés 412 likely 312)",
                 ("sgt1929", "d"): "nationalities sum to 787, printed total 786"}


def naturalisations_bcd():
    cs, age, prof, trade, nat = [], [], [], [], []
    ed = view = page = None
    for ln in (TR / "naturalisations_bcd.txt").read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        if ln.startswith("@"):
            ed, view, page = ln[1:].split()
            view, page = int(view), int(page)
            continue
        key, rest = ln.split(" ", 1)
        base = [ed, ARKS[ed], None, page, view, int(ed[3:])]
        if "|" in rest:
            body, total = rest.split("|")
            total = num(total)
        else:
            body, total = rest, None
        toks = body.split()
        if key == "b_men":
            MEN_TOTAL[ed] = total
        if key in ("b_men", "b_women"):
            codes, frs = (MS, MS_FR) if key == "b_men" else (WS, WS_FR)
            vals = [num(x) for x in toks]
            ok = check("nat_b", f"{ed} {key} total", sum(vals), total)
            flag = "" if ok else "total_mismatch"
            sex = "male" if key == "b_men" else "female"
            for c, fr, v in zip(codes, frs, vals):
                cs.append(base[:2] + ["b"] + base[3:] + ["civil_status", sex, c, fr, v, flag])
        elif key == "b_resid":
            vals = [num(x) for x in toks]
            # against the printed men's total (sgt1922: against table c's 127 men, because
            # its civil-status total also counts the adult son naturalised with his parents)
            check("nat_b", f"{ed} residence sum vs men", sum(vals), 127 if ed == "sgt1922" else MEN_TOTAL[ed])
            for (dur, kind), v in zip(RES, vals):
                fr = ("Plus de 10 ans" if dur.startswith("more") else "Moins de 10 ans") + (" : civils" if kind == "civilian" else " : militaires")
                cs.append(base[:2] + ["b"] + base[3:] + ["residence_in_tunisia", "male", f"{dur}_{kind}", fr, v, ""])
        elif key == "b_birth":
            vals = [num(x) for x in toks]
            for (where, sex), v in zip(BIRTH, vals):
                fr = ("Nés en territoires français" if where == "french_territory" else "Nés à l'étranger")
                cs.append(base[:2] + ["b"] + base[3:] + ["birthplace", sex, where, fr, v, ""])
            m = sum(r[10] for r in cs if r[0] == ed and r[6] == "civil_status" and r[7] == "male")
            w = sum(r[10] for r in cs if r[0] == ed and r[6] == "civil_status" and r[7] == "female")
            check("nat_b", f"{ed} birthplace men vs civil status", vals[0] + vals[2], m)
            check("nat_b", f"{ed} birthplace women vs civil status", vals[1] + vals[3], w)
        elif key == "c_age":
            vals = [num(x) for x in toks]
            for (c, fr), v in zip(AGE, vals):
                age.append(base[:2] + ["c"] + base[3:] + [c, fr, v, ""])
        elif key in ("c_prof", "c_trade", "d"):
            kv = [tok.split("=") for tok in toks]
            vals = [num(v) for _, v in kv]
            tb = {"c_prof": "nat_c_prof", "c_trade": "nat_c_trade", "d": "nat_d"}[key]
            ok = check(tb, f"{ed} {key} total", sum(vals), total)
            flag = "" if ok else "total_mismatch"
            if key in ("c_prof", "c_trade"):
                ages = sum(r[8] for r in age if r[0] == ed)
                check("nat_c_age", f"{ed} ages vs professions total", ages, total)
            fr_map = PROF_FR if key == "c_prof" else TRADE_FR if key == "c_trade" else NAT_FR
            target = prof if key == "c_prof" else trade if key == "c_trade" else nat
            for (c, _), v in zip(kv, vals):
                target.append(base[:2] + ["c" if key != "d" else "d"] + base[3:] + [c, fr_map[c], v, flag])
    mis = "".join(f"- {e} ({k}): {m}\n" for (e, k), m in BCD_MISPRINTS.items())
    n1 = write("naturalisations_civil_status",
               ["census", "gallica_ark", "table_id", "source_page", "gallica_view", "year", "section",
                "sex", "item", "item_fr", "value", "flag"], cs)
    notes("naturalisations_civil_status", "Civil status, residence and birthplace of the naturalised (table b)",
          f"""
Table b) *Renseignements d'état civil sur les naturalisés*, {n1} rows; editions 1922-1930,
1935, 1936, 1939 (`year` = edition year). `section`:

- `civil_status`: men by marital status (single; married to a wife of French origin;
  married to a wife of foreign origin; widowed; divorced) and women by marital status.
- `residence_in_tunisia` (1922-1930): naturalised men by length of residence in Tunisia or
  French territory (more / less than 10 years) and civilian / military.
- `birthplace` (1935-1939): men and women born in French territory / abroad.

Misprints confirmed on the scans (values kept, flagged `total_mismatch` where a total fails):

{mis}""", "nat_b")
    n2 = write("naturalisations_age_men",
               ["census", "gallica_ark", "table_id", "source_page", "gallica_view", "year",
                "age_group", "age_group_fr", "value", "flag"], age)
    notes("naturalisations_age_men", "Age of naturalised men (table c)",
          f"""
Table c) *Age et profession des hommes naturalisés*, age part: {n2} rows; naturalised men
under 25, 25-40 and over 40, editions 1922-1930, 1935, 1936, 1939. Each edition's age
groups were checked against its profession total.
""", "nat_c_age")
    n3 = write("naturalisations_profession_groups",
               ["census", "gallica_ark", "table_id", "source_page", "gallica_view", "year",
                "profession", "profession_fr", "value", "flag"], prof)
    notes("naturalisations_profession_groups", "Profession of naturalised men, 1922-1930 (table c)",
          f"""
Table c) profession part, editions 1922-1930: {n3} rows in nine broad groups (army;
agriculture; commerce and industry; employees of commerce or administration; café keepers
and drink sellers; sea fishing; owners and rentiers; liberal professions; other). The 1930
edition replaces café keepers with *employés et ouvriers d'industrie*. From 1935 the
table lists individual trades instead; see `naturalisations_profession_trades.csv`.
""", "nat_c_prof")
    n4 = write("naturalisations_profession_trades",
               ["census", "gallica_ark", "table_id", "source_page", "gallica_view", "year",
                "profession", "profession_fr", "value", "flag"], trade)
    notes("naturalisations_profession_trades", "Profession of naturalised men, 1935-1939 (table c)",
          f"""
Table c) profession part, editions 1935, 1936 and 1939: {n4} rows. These editions list 26 to
33 individual trades; the list changes from year to year (a trade not listed has no row).
""", "nat_c_trade")
    n5 = write("naturalisations_nationality",
               ["census", "gallica_ark", "table_id", "source_page", "gallica_view", "year",
                "nationality", "nationality_fr", "value", "flag"], nat)
    notes("naturalisations_nationality", "Nationality of the naturalised, 1922-1930 (table d)",
          f"""
Table d) *Nationalité des naturalisés*, editions 1922-1930: {n5} rows. Until 1929 the table
counts naturalised men only (its total equals the men's total of tables b and c). In 1930
it counts everyone naturalised, minors included (total 1.609 = table a grand total). The
categories change: 1922-1923 group all Tunisians; from 1924 Tunisian Muslims and Jews are
separate and Russians appear. From 1935 there is no table d; nationality is in table e.
""", "nat_d")
    return n1 + n2 + n3 + n4 + n5


# ---------------------------------------------------------- naturalisations e
E_NAT = {"Italiens": "italian", "Anglo-Maltais": "anglo_maltese", "Maltais": "maltese", "Suisses": "swiss",
         "Allemands": "german", "Autrichiens": "austrian", "Espagnols": "spanish", "Grecs": "greek",
         "Hollandais": "dutch", "Portugais": "portuguese", "Belges": "belgian", "Norvégiens": "norwegian",
         "Norvégiens et Suédois": "norwegian_swedish", "Tcheco-Slovaques": "czechoslovak",
         "Tchéco-Slovaques": "czechoslovak", "Bulgares": "bulgarian", "Hongrois": "hungarian",
         "Roumains": "romanian", "Serbes": "serbian", "Yougo-Slaves": "yugoslav",
         "Turcs et Syriens": "turkish_syrian", "Turcs": "turkish", "Albanais": "albanian",
         "Polonais": "polish", "Russes": "russian", "Luxembourgeois": "luxembourger",
         "Indigènes Catholiques": "indigenous_catholic", "Musulmans Algériens": "algerian_muslim",
         "Musulmans Tunisiens": "tunisian_muslim", "Musulmans Marocains": "moroccan_muslim", "Israélites Algériens": "algerian_jew",
         "Israélites Tunisiens": "tunisian_jew", "Divers": "other",
         "Algériens catholiques": "algerian_catholic", "Algériens musulmans": "algerian_muslim",
         "Algériens israélites": "algerian_jew", "Tunisiens catholiques": "tunisian_catholic",
         "Tunisiens musulmans": "tunisian_muslim", "Tunisiens israélites": "tunisian_jew",
         "Marocains": "moroccan", "Syriens": "syrian", "Indochinois": "indochinese",
         "Indigènes de l'A.O.F.": "french_west_african", "Anglais": "british"}
BASIS = {"d1887": "décret du 29 juillet 1887", "d1899": "décret du 28 février 1899",
         "d1910": "décret du 3 octobre 1910", "l1914": "loi du 5 août 1914", "l1923": "loi du 20 décembre 1923"}
AGEG = {"T": ("total", "Totaux"), "M": ("adults", "Majeurs"), "m": ("minors", "Mineurs")}
E_CMP = {}
# printed cells kept although inconsistent with the printed totals
E_FLAGS = {("sgt1939", "Suisses", "1938"): "total_mismatch"}
# sgt1930 prints the 1891-1910 figures (3, 3, 2) twice, under Indigènes Catholiques and
# under Divers. The 1924 edition prints them once (as Musulmans Marocains, with no
# Indigènes Catholiques row), and the 1935 and 1936 editions keep them under Divers (3
# and 5). The Indigènes Catholiques cells are set to 0; the printed totals then add up.
E_FIX = {("sgt1930", "Indigènes Catholiques", "1891-1898", "T"): 0,
         ("sgt1930", "Indigènes Catholiques", "1899-1910", "M"): 0,
         ("sgt1930", "Indigènes Catholiques", "1899-1910", "m"): 0}


def naturalisations_e():
    t = "nat_e"
    blocks = parse_blocks(TR / "naturalisations_by_nationality.txt")
    out_n = 0
    tables = {}
    for b in blocks:
        ed = b["edition"]
        pages = dict(zip(b["view"].split(","), b["page"].split(",")))
        cols = []
        for c in b["cols"]:
            spec, view = c.split("@")
            period, basis, ag = spec.split("/")
            cols.append((period, basis, ag, int(view), int(pages[view])))
        rows, sums = [], [0] * len(cols)
        for lab, vals in b["rows"]:
            v = [num(x) for x in vals]
            assert len(v) == len(cols), (ed, lab, len(v))
            for i, (period, basis, ag, view, page) in enumerate(cols):
                flag = E_FLAGS.get((ed, lab, period), "")
                if (ed, lab, period, ag) in E_FIX:
                    v[i], flag = E_FIX[(ed, lab, period, ag)], "reprint_corrected"
                sums[i] += v[i]
                rows.append([ed, ARKS[ed], "e", page, view, period, basis, BASIS[basis],
                             AGEG[ag][0], AGEG[ag][1], E_NAT[lab], lab, v[i], flag])
        tot = [num(x) for x in b["total"]]
        for i, c in enumerate(cols):
            check(t, f"{ed} {c[0]} {AGEG[c[2]][0]} column total", sums[i], tot[i])
        tables[ed] = rows
        if ed == "sgt1924":                # comparison printing only, no data file
            continue
        name = f"naturalisations_by_nationality_{ed}"
        out_n += write(name, ["census", "gallica_ark", "table_id", "source_page", "gallica_view", "period",
                              "legal_basis", "legal_basis_fr", "age_group", "age_group_fr", "nationality",
                              "nationality_fr", "value", "flag"], rows)
        tables[ed] = rows
    # cross-edition comparison: sgt1930 (adults + minors) vs sgt1939, on the years and
    # periods both print, by nationality where the categories match
    a = defaultdict(int)
    for r in tables["sgt1930"]:
        p = r[5]
        key_p = {"1911-1920": "1911-1922", "1921": "1911-1922", "1922": "1911-1922", "1923": "1911-1922"}.get(p, p)
        if p in ("1924", "1925", "1926", "1927", "1928"):
            key_p = "1924-1928"
        nat = {"anglo_maltese": "maltese", "turkish_syrian": "turkish", "serbian": "yugoslav",
               "norwegian": "norwegian_swedish", "indigenous_catholic": "algerian_catholic"}.get(r[10], r[10])
        a[(key_p, nat)] += r[12]
    bq = defaultdict(int)
    for r in tables["sgt1939"]:
        bq[(r[5], r[10])] += r[12]
    common = sorted({p for p, _ in a} & {p for p, _ in bq})
    comp, diffs = 0, []
    for p in common:
        ta = sum(v for (pp, _), v in a.items() if pp == p)
        tb = sum(v for (pp, _), v in bq.items() if pp == p)
        comp += 1
        if ta != tb:
            diffs.append(f"{p}, all nationalities: sgt1930 {ta}, sgt1939 {tb}")
        for nat in sorted({n for pp, n in a if pp == p} | {n for pp, n in bq if pp == p}):
            comp += 1
            if a.get((p, nat), 0) != bq.get((p, nat), 0):
                diffs.append(f"{p}, {nat}: sgt1930 {a.get((p, nat), 0)}, sgt1939 {bq.get((p, nat), 0)}")
    dl = "".join(f"- {d}\n" for d in diffs)
    # sgt1924 vs sgt1930, cell by cell (sgt1924 Musulmans Marocains = sgt1930 Divers)
    c24 = {(r[5], r[8], {"moroccan_muslim": "other"}.get(r[10], r[10])): r[12] for r in tables["sgt1924"]}
    c30 = {(r[5], r[8], r[10]): r[12] for r in tables["sgt1930"] if (r[5], r[8]) in {(k[0], k[1]) for k in c24}}
    keys = set(c24) | set(c30)
    d24 = [f"{p} {ag} {n}: sgt1924 {c24.get((p, ag, n), 0)}, sgt1930 {c30.get((p, ag, n), 0)}"
           for (p, ag, n) in sorted(keys) if c24.get((p, ag, n), 0) != c30.get((p, ag, n), 0)]
    E_CMP["n24"], E_CMP["d24"] = len(keys), d24
    for ed, body in (("sgt1930", f"""
Table e) *Naturalisations accordées (1891-1930)*, as printed in the 1930 edition
(pp. 24-25): {len(tables['sgt1930'])} rows, 27 nationalities. Columns `period` (a year, or
a range printed as one column), `legal_basis` (the decree or law the naturalisations were
granted under, as printed above each column group), `age_group` (`adults` = majeurs,
`minors` = mineurs, `total` where only a total is printed), `nationality`.

This is the last edition with the adults/minors split and the per-year columns for
1921-1930. Later editions (1935, 1936, 1939) regroup the early years and drop the split;
the 1939 printing is in `naturalisations_by_nationality_sgt1939.csv`.

Misprints confirmed on the scan:

- *Indigènes catholiques* and *Divers* both print 3 (1891-1898) and 3 / 2 (1899-1910
  adults / minors), and the printed totals (296, 733, 639) only add up with one of them.
  The 1924 edition prints these figures once (as *Musulmans marocains*, with no
  *Indigènes catholiques* row), and the 1935 and 1936 editions keep them under *Divers*
  (3 and 5). The three *Indigènes catholiques* cells are set to 0 (`reprint_corrected`);
  the totals then check.
- 1925 minors: the cells sum to 1.726, printed total 1.736; the year total (3.298) and
  table a (1.726 minors) confirm the cells.
- 1929 adults: the cells sum to 1.348, printed total 1.345; the year total (2.636) and
  table a agree with 1.345, so one cell is printed 3 too high; it cannot be identified.
- The 1922 minors column runs into the binding; it was read from the visible digits and
  checks against the printed total (283).

## Comparison with the other printings

- **sgt1924, cell by cell** (1891-1924, the first fifteen columns): {E_CMP['n24']}
  cells compared, {E_CMP['n24'] - len(E_CMP['d24'])} equal, {len(E_CMP['d24'])} different:

{"".join(f"  - {{d}}" + chr(10) for d in E_CMP['d24'])}
  (sgt1924's *Musulmans marocains* matched with this file's *Divers*; with the
  *Indigènes catholiques* correction above, every cell agrees.)
- **sgt1922, sgt1923, sgt1925-sgt1929, printed totals** (each period and year, adults
  and minors): all equal to this file's printed totals, with one exception. The 1925
  minors total is printed 1.726 in the 1925-1928 editions and 1.736 in the 1929 and 1930
  editions; 1.726 is right (it is the sum of the cells and table a's figure). Totals are
  not stored, so no value changes.
- **sgt1929, 1929 column, cell by cell:** identical to this file, including the adults
  that sum to 1.348 against a printed 1.345. No printing locates the cell that is 3 too
  high.
- The 1922-1923 and 1925-1929 printings were compared at the level of their printed
  totals only, not cell by cell.
"""), ("sgt1939", f"""
Table e) *Naturalisations accordées*, as printed in the 1939 edition (pp. 12-13):
{len(tables['sgt1939'])} rows, 32 nationalities. Same columns as the sgt1930 file;
`age_group` is always `total` (adults and minors together). Periods: 1891-1898, 1899-1910,
1911-1922, 1915-1924 (by legal basis), 1924-1928 (one column), then each year 1929-1939.
Categories differ from 1930: *Maltais* (for Anglo-Maltais), *Turcs* and *Syriens*
separately, *Yougo-Slaves* (for Serbes), Algerians and Tunisians by religion
(catholiques / musulmans / israélites), plus Marocains, Indochinois, Indigènes de
l'A.O.F. and Anglais.

Misprints confirmed on the scan:

- 1935: the cells sum to 668 but the total is printed 686 (transposed digits); the 1935
  edition's table a also gives 668.
- 1938, Suisses: printed `0` (zero is otherwise printed `»`); the column total (1.278)
  needs 10. The printed 0 is kept and flagged `total_mismatch`.

## Comparison with the 1930 printing

The two printings overlap on 1891-1930. Comparing sgt1930 (adults + minors, with its
categories mapped onto the 1939 ones: Anglo-Maltais = Maltais, Turcs et Syriens = Turcs,
Serbes = Yougo-Slaves, Norvégiens = Norvégiens et Suédois, Indigènes catholiques =
Algériens catholiques; 1911-1920 + 1921 + 1922 + 1923 = the 1939 column "1911 à 1922";
1924 + ... + 1928 = "1924 à 1928"): {comp} comparisons, {comp - len(diffs)} equal,
{len(diffs)} different:

{dl}
What the differences show:

- 1911-1922, 1915-1924 and 1930 agree exactly, nationality by nationality.
- 1891-1898 and 1899-1910 differ only through reclassification: the 1939 edition counts as
  Russians the entries that the 1930 edition prints under *Indigènes catholiques* and
  *Divers* (and the 1930 *Divers* row duplicates *Indigènes catholiques*, see the sgt1930
  notes).
- 1924-1928 and 1929 were revised, not only reclassified: the period totals are close
  (13.997 vs 13.996; 2.639 or 2.636 vs 2.601), but many nationalities change (1924-1928:
  Swiss 42 vs 63, Austrians 13 vs 40, Maltese 973 vs 1.002; 1929: Italians 1.389 vs
  1.330, Swiss 0 vs 10, Turks 0 vs 9), and the 1930 *Divers* (152 and 78) is spread over
  new categories (Marocains, Syriens, Anglais, Algerian Catholics, ...).

Values are kept as each edition prints them; neither file is corrected from the other.
For 1924-1929 the two files are alternative printings; prefer the 1939 printing for
totals by nationality, and the 1930 printing for the adults/minors split.

## Comparison with the 1935 and 1936 printings

Their printed totals for every period and year (1891-1898 to 1934 in sgt1935, to 1936 in
sgt1936; 1924-1928 summed from their yearly columns: 13.996) equal this file's, except
1935: both print 668, confirming that this edition's 686 is a misprinted total (the cells
sum to 668; no value changes). They also agree with this file on the revised 1929 total
(2.601). Only the totals were compared, not every cell. 1938 (Suisses printed 0) and 1937-1939
appear in no other printing.
""")):
        notes(f"naturalisations_by_nationality_{ed}",
              f"Naturalisations by nationality, legal basis and year ({ed} printing, table e)", body, t)
    return out_n, comp, len(diffs)


# --------------------------------------------------------- foreigners movement
FOR_NAT = {"Albanais": "albanian", "Allemands": "german", "Américains": "american",
           "Américains (Nord et Sud)": "american", "Anglais et Anglo-Maltais": "british_anglo_maltese",
           "Argentins": "argentine", "Arméniens": "armenian", "Australiens": "australian",
           "Autrichiens": "austrian", "Belges": "belgian", "Brésiliens": "brazilian", "Bulgares": "bulgarian",
           "Chiliens": "chilean", "Chinois": "chinese", "Colombiens": "colombian", "Danois": "danish",
           "Egyptiens": "egyptian", "Espagnols": "spanish", "Esthoniens": "estonian", "Finlandais": "finnish",
           "Grecs": "greek", "Hollandais": "dutch", "Hongrois": "hungarian", "Indous": "indian",
           "Italiens": "italian", "Japonais": "japanese", "Lettons": "latvian", "Libanais": "lebanese",
           "Luxembourgeois": "luxembourger", "Mexicains": "mexican", "Norvégiens": "norwegian",
           "Palestiniens": "palestinian", "Persans": "persian", "Polonais": "polish", "Portugais": "portuguese",
           "Roumains": "romanian", "Russes": "russian", "Serbes": "serbian", "Suédois": "swedish",
           "Suisses": "swiss", "Syriens": "syrian", "Tchéco-Slovaques": "czechoslovak",
           "Tripolitains": "tripolitanian", "Turcs": "turkish", "Vénézuéliens": "venezuelan",
           "Yougo-Slaves": "yugoslav", "Autres": "other"}
MOV = {"A": ("arrivals", "Arrivées"), "D": ("departures", "Départs")}
FOR_NAT.update({"Anglais": "british_anglo_maltese", "Anglo-Maltais": "british_anglo_maltese",
                "Autrichiens et Hongrois": "austrian_hungarian", "Autres étrangers": "other"})
OLD_LIST = {"sgt1926", "sgt1927"}            # 28-nationality list
# Columns whose latest printing is wrong (see the notes): use this edition instead.
# 1921: the 1929-1930 editions print 1917's figures as 1921 (sgt1927 and sgt1928 had put
# the 1917 column in the 1921 slot, labelled 1917); only sgt1926 prints 1921 itself.
# 1922-1927: the 1928-1935 editions re-keyed these years onto the 45-nationality list
# with errors; the older printings named here add up to the printed totals.
FOR_GOOD = {(1921, "A"): "sgt1926", (1921, "D"): "sgt1926",
            (1922, "A"): "sgt1927", (1922, "D"): "sgt1927", (1923, "A"): "sgt1927",
            (1924, "A"): "sgt1927", (1925, "A"): "sgt1927", (1925, "D"): "sgt1927",
            (1926, "A"): "sgt1926", (1926, "D"): "sgt1927",
            (1927, "A"): "sgt1927", (1927, "D"): "sgt1927"}


def foreigners():
    t = "foreigners"
    order = list(ARKS)
    cols_by = {}                              # (edition, year, mov) -> {code: value}
    meta = {}                                 # (edition, year, mov) -> (page, view)
    labels = defaultdict(set)
    for b in parse_blocks(TR / "foreigners.txt"):
        cols = [c.split("/") for c in b["cols"]]
        sums = [0] * len(cols)
        for lab, vals in b["rows"]:
            assert len(vals) == len(cols), (b["edition"], b["view"], lab, len(vals))
            code = FOR_NAT[lab]
            labels[code].add(lab)
            for i, (y, m) in enumerate(cols):
                v = None if vals[i] == "_" else num(vals[i])
                sums[i] += v or 0
                d = cols_by.setdefault((b["edition"], int(y), m), {})
                if code in d and d[code] is not None and v is not None:
                    d[code] += v                     # Anglais + Anglo-Maltais
                else:
                    d[code] = v
                meta[(b["edition"], int(y), m)] = (int(b["page"]), int(b["view"]))
        tot = [num(x) for x in b["total"]]
        for i, (y, m) in enumerate(cols):
            check(t, f"{b['edition']} {y} {MOV[m][0]} column total", sums[i], tot[i])

    def view(ed, y, m, collapse):
        d = dict(cols_by[(ed, y, m)])
        if collapse and ed not in OLD_LIST:
            d["austrian_hungarian"] = (d.pop("austrian", 0) or 0) + (d.pop("hungarian", 0) or 0)
        return d

    rows, diffs, compared, equal, fixes = [], [], 0, 0, []
    for (y, m) in sorted({(y, m) for (_, y, m) in cols_by}):
        eds = sorted([e for (e, y2, m2) in cols_by if (y2, m2) == (y, m)], key=order.index)
        latest = eds[-1]
        chosen = FOR_GOOD.get((y, m), latest)
        old = chosen in OLD_LIST or any(e in OLD_LIST for e in eds)
        base = view(chosen, y, m, chosen in OLD_LIST)
        # compare every other printing with the chosen one
        for e in eds:
            if e == chosen:
                continue
            other = view(e, y, m, chosen in OLD_LIST or e in OLD_LIST)
            ref = view(chosen, y, m, chosen in OLD_LIST or e in OLD_LIST)
            for code in sorted(set(ref) | set(other)):
                a, bv = ref.get(code), other.get(code)
                if a is None and bv is None:
                    continue
                if (code not in ref and not bv) or (code not in other and not a):
                    continue                        # category printed by one list only, zero
                compared += 1
                if a == bv:
                    equal += 1
                else:
                    diffs.append(f"{y} {MOV[m][0]} {code}: {e} prints {bv}, {chosen} prints {a}")
        # per-cell source: the chosen edition, or (no correction) the latest edition that
        # prints the nationality at all
        src = {code: chosen for code in base}
        if chosen == latest:
            for e in eds:
                for code, v in view(e, y, m, False).items():
                    if code not in base or src[code] == e or order.index(e) > order.index(src[code]):
                        if code not in base or order.index(e) >= order.index(src[code]):
                            base[code], src[code] = v, e
        lat = view(latest, y, m, chosen in OLD_LIST) if chosen != latest else base
        for code in sorted(set(base) | set(lat)):
            v = base.get(code)
            page, viewno = meta[(src.get(code, chosen), y, m)]
            if code not in base:
                if not lat.get(code):
                    continue
                v = 0                                # printed only by the faulty re-keying
            flag = "not_applicable" if v is None else ""
            if chosen != latest and v != lat.get(code, 0 if v == 0 else None):
                flag = "reprint_corrected"
                fixes.append(f"{y} {MOV[m][0]} {code}: {latest} prints {lat.get(code)}, kept {v} from {chosen}")
            lab = " + ".join(sorted(labels[code] & ({"Anglais", "Anglo-Maltais"} if chosen in OLD_LIST and code == "british_anglo_maltese" else labels[code]))) if chosen in OLD_LIST and code == "british_anglo_maltese" else sorted(labels[code])[0]
            ce = src.get(code, chosen)
            rows.append([ce, ARKS[ce], "foreigners", page, viewno, y, MOV[m][0], MOV[m][1], code, lab,
                         "" if v is None else v, flag])
    n = write("foreigners_movements", ["census", "gallica_ark", "table_id", "source_page", "gallica_view",
                                       "year", "movement", "movement_fr", "nationality", "nationality_fr",
                                       "value", "flag"], rows)
    years = sorted({r[5] for r in rows})
    body = f"""
*Mouvement des étrangers en Tunisie, entrées et sorties*: foreigners' arrivals and
departures by nationality, {years[0]}-{years[-1]}. {n} rows: one per year, movement and
nationality. Each cell is taken from the latest edition that prints it (`census`),
except the columns listed under "Corrections", where the latest printing is wrong.

Columns: `year`, `movement` (`arrivals` / `departures`), `nationality` (English code),
`nationality_fr` (as printed), `value` = persons. A footnote in the 1926-1930 editions
says that for 1923-1926 the figures are declarations of residence (men and women,
children excluded). In 1933 Serbs are printed as "compris dans les Yougoslaves" and
Tripolitanians as "compris dans les Italiens": `value` NA, flag `not_applicable`.

Two lists of nationalities are used. The 1926 and 1927 editions list 28 (with *Anglais*
and *Anglo-Maltais* separately, summed here into `british_anglo_maltese`;
*Autrichiens et Hongrois* together, `austrian_hungarian`; *Autres étrangers* = `other`);
from 1928 the table lists 45 (46 with *Indous* from 1935), and from 1936 32. Years taken
from the 1926-1927 editions (1917-1918, 1921-1927, see below) therefore use the short
list.

## Sources used

- sgt1926 (pp. 26-27, views 590-591): 1917-1926; the only printing of 1921.
- sgt1927 (pp. 26-27, views 54-55): 1918-1927; latest printing of 1918.
- sgt1928 (pp. 26-27, views 578-579): 1917, 1919-1928; latest printing of 1917 and 1919.
- sgt1929 (p. 26, view 54): 1920-1923; latest printing of 1920.
- sgt1930 (pp. 26-27, views 584-585): 1921-1930; the 1929 departures (in the binding of
  sgt1935).
- sgt1935 (pp. 16-17, views 36-37): 1926-1935; latest printing of 1928-1931, and of
  1932-1934 for the nationalities that the 1936 edition no longer lists.
- sgt1936 (p. 14, view 25): 1932-1936; latest printing of 1932-1934 where it lists the
  nationality.
- sgt1939 (p. 14, view 20): 1935-1939.

## The year labels of 1917 and 1921

The 1926 edition prints 1917-1926 in order. The 1927 edition (1918-1927) prints 1918,
1919, 1920 and then, in the slot where 1921 belongs, a column labelled **1917** with
1917's figures (3.388 arrivals, 2.302 departures; Italians 2.948 / 1.850), and no 1921.
The 1928 edition does the same (1919, 1920, "1917", 1922...). The 1929 and 1930 editions
keep that column but label it **1921**. So the figures printed as 1921 in the 1929 and
1930 editions are 1917's; the only printing of 1921 is the 1926 edition's (4.740 / 2.483,
whose cells add up to its printed totals). Here, 1917 is taken from sgt1928 (its
correctly labelled column, identical to sgt1926 and sgt1927) and 1921 from sgt1926.

## Corrections (`reprint_corrected`)

Besides 1921, the 1928 edition re-keyed 1922-1927 onto its new list of nationalities, and
the 1929-1935 editions copied it. The re-keyed columns do not add up to their printed
totals, while the 1926-1927 printings do; so those columns are taken from the older
printing (`FOR_GOOD` in the script):

- 1922 arrivals: Spaniards printed 34 for 64; Estonians 5 and Venezuelans 2 added, Yugoslavs
  2 dropped. 1922 departures: Belgians printed 7 for 17.
- 1923 arrivals: Tripolitanians 11 added (not in the older printing, which adds up without
  them).
- 1924 arrivals: Syrians 1 dropped. 1925: Persians 1 and Syrians 2 / 1 dropped. 1926
  departures and 1927: Persians and Syrians dropped; 1927 arrivals Italians 1.725 for 1.726.
- 1926 arrivals: the 1927 and later editions print Belgians 61 with a total of 3.562, which
  their cells do not reach; the 1926 edition prints 661, and its cells then add up to
  3.562. 661 is kept.

Every cell that changes is listed here:

""" + "".join(f"- {x}\n" for x in fixes) + f"""
Columns that still do not add up are misprints with no consistent printing: 1920 arrivals
(sgt1929 prints a total of 4.505; cells and the older printings give 4.506), 1928 arrivals,
1929 arrivals, 1930 departures, 1931 (arrivals printed 55.302, cells 19.546), 1933-1934,
and the 1936-1939 editions, whose rows omit 14 nationalities that their totals include.

## Comparison of the overlapping printings

Every other printing of each cell was compared with the kept value (categories mapped
between the two lists: Anglais + Anglo-Maltais; Autrichiens + Hongrois): {compared}
comparisons, {equal} equal, {compared - equal} different:

""" + "".join(f"- {d}\n" for d in diffs) + """
The 1925 edition (1925 only, with its own list including Cubains, Lithuaniens, Péruviens)
was not transcribed; its totals (2.233 / 1.052) equal the kept 1925 values.
"""
    notes("foreigners_movements", "Foreigners' arrivals and departures by nationality, 1917-1939", body, t)
    return n


# ------------------------------------------------------------------ recruitment
REC = {
    "fr_alloc": ("recruitment_french_allocation", "a", "Répartition du recrutement (recrutement français)",
                 [("registered", "Inscrits définitivement sur les tableaux de recensement"),
                  ("exempted_infirmity", "Exemptés pour infirmités"), ("remaining", "Reste"),
                  ("part1_armed_service", "1re partie : propres au service armé"),
                  ("part2_auxiliary_services", "2e partie : classés dans les services auxiliaires"),
                  ("part3_voluntary_enlistment", "3e partie : liés au service en vertu d'un engagement volontaire, d'un livret ou d'une commission"),
                  ("part4_excluded_art4", "4e partie : exclus en vertu des dispositions de l'art. 4"),
                  ("part5_postponed_art18", "5e partie : ajournés d'office conformément au § 3 de l'art. 18"),
                  ("part6_auxiliary_on_request", "6e partie : classés dans les services auxiliaires sur leur demande (art. 19)"),
                  ("part7_deferred_art20_21", "7e partie : ayant obtenu un sursis (art. 20 et 21)")]),
    "fr_educ": ("recruitment_french_education", "b", "Degré d'instruction des jeunes gens recrutés (recrutement français)",
                [("illiterate", "Ne sachant ni lire ni écrire"), ("read_only", "Sachant lire seulement"),
                 ("read_write", "Sachant lire et écrire"), ("read_write_count", "Sachant lire, écrire et compter"),
                 ("primary_certificate", "Ayant obtenu le brevet de l'enseignement primaire"),
                 ("baccalaureate", "Bacheliers"), ("not_verified", "Dont on n'a pu vérifier l'instruction")]),
    "fr_board": ("recruitment_french_draft_boards", "c", "Opérations des Conseils de révision (recrutement français)",
                 [("registered", "Inscrits sur le tableau de recensement"), ("exempted", "Exemptés"),
                  ("not_called_age_or_neo_french", "Hommes qui, en raison de leur âge, n'ont pas été appelés / Néo-français qui, en raison de leur âge, n'ont pas été appelés"),
                  ("to_be_called", "Nombre à appeler sous les drapeaux"), ("postponed", "Ajournés"),
                  ("deferred", "En sursis d'incorporation"), ("enlisted_maritime", "Engagés et inscrits maritimes"),
                  ("actually_called", "Appelés réellement sous les drapeaux")]),
    "ind_lottery": ("recruitment_indigenous_lottery", "a", "Opérations des Commissions de tirage au sort, répartition des conscrits (recrutement indigène)",
                    [("registered_at_lottery", "Inscrits au moment du tirage au sort"),
                     ("examined", "Examinés pour obtenir le contingent"),
                     ("designated", "Désignés pour le service militaire"), ("incorporated", "Incorporés"),
                     ("exonerated_by_payment", "Exonérés par suite du versement du prix de remplacement"),
                     ("surplus_to_contingent", "En excédent des besoins du contingent"),
                     ("exempt_family_support", "Dispensés comme soutien de famille"),
                     ("unfit_illness", "Inaptes pour cause de maladie"), ("discharged_unfit", "Réformés"),
                     ("exempt_art36_students", "Dispensés (art. 36) : élèves maîtres, Collège Sadiki, certificat d'études primaires, élèves des mosquées"),
                     ("volunteers", "Engagements volontaires"),
                     ("enrolled_ex_officio", "Inscrits d'office (bons absents) incorporés")]),
    "ind_educ": ("recruitment_indigenous_education", "b", "Degré d'instruction des jeunes gens recrutés (recrutement indigène)",
                 [("read_write_arabic", "Sachant lire et écrire l'arabe"),
                  ("read_write_french", "Sachant lire et écrire le français"),
                  ("read_write_french_arabic", "Sachant lire et écrire le français et l'arabe"),
                  ("speaks_french", "Parlant le français")]),
}
# 1924 class, enlisted: sgt1935 (the latest printing) prints 39; sgt1925 and sgt1930
# print 93, which the row identity requires.
REC_FIX = {("fr_board", 1924, "enlisted_maritime", "sgt1935"): 93}


def recruitment():
    order = list(ARKS)
    printings = defaultdict(dict)          # (tbl, year, item) -> {edition: value}
    where, rowflag = {}, {}
    cur = None
    for ln in (TR / "recruitment.txt").read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        if ln.startswith("@"):
            ed, ark, view, page, tbl = ln[1:].split()
            cur = (ed, int(view), int(page), tbl)
            continue
        ed, view, page, tbl = cur
        yr, rest = ln.split("|", 1)
        yr = int(yr)
        if "|" in rest:
            body, total = rest.split("|")
            total = num(total)
        else:
            body, total = rest, None
        vals = [num(x) for x in body.split()]
        items = [c for c, _ in REC[tbl][3]]
        assert len(vals) == len(items), (ed, tbl, yr, len(vals))
        printed = dict(zip(items, vals))
        d = dict(printed)
        for (t2, y2, it, e2), fix in REC_FIX.items():
            if (t2, y2, e2) == (tbl, yr, ed):
                d[it] = fix
        key = f"rec_{tbl}"
        ok = True
        if tbl == "fr_alloc":
            parts = sum(v for k, v in d.items() if k.startswith("part"))
            ok &= check(key, f"{ed} {yr} registered - exempted = remaining", d["registered"] - d["exempted_infirmity"], d["remaining"])
            ok &= check(key, f"{ed} {yr} parts = printed total", parts, total)
            ok &= check(key, f"{ed} {yr} printed total = remaining", total, d["remaining"])
        elif tbl in ("fr_educ", "ind_educ"):
            ok &= check(key, f"{ed} {yr} row total", sum(d.values()), total)
        elif tbl == "fr_board" and yr >= 1915:
            ok &= check(key, f"{ed} {yr} called = registered - exempted - neo-French - postponed - deferred - enlisted",
                        d["registered"] - d["exempted"] - d["not_called_age_or_neo_french"] - d["postponed"]
                        - d["deferred"] - d["enlisted_maritime"], d["actually_called"])
        for it, v in printed.items():
            printings[(tbl, yr, it)][ed] = v
            where[(tbl, yr, ed)] = (view, page)
            rowflag[(tbl, yr, ed)] = ok
    total_rows = 0
    for tbl, (name, tid, title, cols) in REC.items():
        fr = dict(cols)
        rows, diffs, comp, eq = [], [], 0, 0
        mine = [(k, v) for k, v in printings.items() if k[0] == tbl]
        for (t2, yr, it), eds in sorted(mine, key=lambda kv: (kv[0][1], [c for c, _ in cols].index(kv[0][2]))):
            latest = max(eds, key=order.index)
            for e, v in eds.items():
                if e != latest:
                    comp += 1
                    if v == eds[latest]:
                        eq += 1
                    else:
                        diffs.append(f"{yr} {it}: {e} prints {v}, {latest} prints {eds[latest]}")
            view, page = where[(tbl, yr, latest)]
            flag = "reprint_corrected" if (tbl, yr, it, latest) in REC_FIX else (
                "" if rowflag[(tbl, yr, latest)] else "total_mismatch")
            value = REC_FIX.get((tbl, yr, it, latest), eds[latest])
            rows.append([latest, ARKS[latest], tid, page, view, yr, it, fr[it], value, flag])
        n = write(name, ["census", "gallica_ark", "table_id", "source_page", "gallica_view", "year",
                         "item", "item_fr", "value", "flag"], rows)
        total_rows += n
        yrs = sorted({r[5] for r in rows})
        unit = "conscription class (classe)" if tbl.startswith("fr") else "year"
        extra = {
            "fr_alloc": "Checks per class: registered - exempted = remaining; the seven parts sum to the printed total; printed total = remaining.",
            "fr_educ": "Check per class: the seven categories sum to the printed total (printed totals are the registered men, or from 1933 the remaining men, of the allocation table).",
            "fr_board": ("Check per class (1915 onwards): actually called = registered - exempted - neo-French "
                         "not called - postponed - deferred - enlisted. The third column means *hommes qui, en "
                         "raison de leur âge, n'ont pas été appelés* before 1913 and *néo-français* later; the "
                         "pre-1915 classes do not follow the identity and are not checked. 1902-1903 are taken "
                         "from sgt1925 (the 1926-1929 editions, which may also print them, were not "
                         "transcribed). The 1924 class: sgt1935 prints 39 enlisted, sgt1925 and sgt1930 print "
                         "93, which the identity requires: 93 kept, flag `reprint_corrected`."),
            "ind_lottery": "No totals are printed and no identity holds between the columns, so this table has no total checks; only the overlapping printings were compared.",
            "ind_educ": "Check per year: the four categories sum to the printed total.",
        }[tbl]
        body = f"""
*{title}*: {n} rows, {unit}s {yrs[0]}-{yrs[-1]}, one row per {unit.split(' ')[0]} and item.
Each value is taken from the latest transcribed edition that prints it (`census`).
Columns: `year` ({unit}), `item` (English code), `item_fr` (printed heading), `value`.

{extra}

Rows of a class or year that fail a check are flagged `total_mismatch` (all items of that
row); the values are kept as printed.

## Editions used and compared

Transcribed: sgt1925 (1916-1925; draft boards 1902-1925), sgt1930 (1921-1930; draft
boards 1904-1930), sgt1935 (1926-1935; draft boards 1916-1935), sgt1936 (French classes
1933-1937; indigenous years 1932-1936), sgt1939 (1935-1939). Values for 1916-1920 come
from sgt1925, although the 1926-1929 editions also print some of these years; the
1922-1924 and 1926-1929 editions were not transcribed, and classes/years 1913-1915
(only in the 1922-1924 editions) are not covered, except the draft boards.

Every other transcribed printing of the same cell was compared: {comp} comparisons,
{eq} equal, {comp - eq} different:

""" + "".join(f"- {d}\n" for d in diffs)
        notes(name, title, body, f"rec_{tbl}")
    return total_rows


def main():
    n = recruitment()
    n += foreigners()
    n += expulsions()
    n += naturalisations_granted()
    n += naturalisations_bcd()
    ne, comp, nd = naturalisations_e()
    n += ne
    tot_c = sum(c for c, _ in CHECKS.values())
    tot_p = sum(p for _, p in CHECKS.values())
    print(f"{n} rows written; {tot_p}/{tot_c} printed-total checks pass")
    for k, msgs in FAILS.items():
        for m in msgs:
            print(f"  FAIL {k}: {m}")
    print(f"table e cross-edition comparisons: {comp}, differences: {nd}")


if __name__ == "__main__":
    main()
