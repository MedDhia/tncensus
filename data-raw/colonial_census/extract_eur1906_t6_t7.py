#!/usr/bin/env python3
"""Extract the 1906 European census profession tables.

Outputs (data-raw/colonial_census/csv/):
  eur1906_t6_profession_nationality.csv              Table VI  (pp. 24-25, view 28)
  eur1906_t7_profession_circonscription.csv          Table VII (pp. 26-33, views 29-32)

All values were transcribed by hand from crops of the Gallica page images
(data-raw/colonial_census/transcribed/); Gallica's OCR was too unreliable for
these tables. Table G (pp. 62-63) and the commentary profession tables
(pp. 57, 58, 61) are published by the other 1906 extraction; their
transcriptions here (transcribed/eur1906_tg.txt, eur1906_text_p*.csv) are
used only for validation and, for Table G, to pin down Table VII cells
hidden in the binding of the fold-out spreads.

Every printed subtotal and total is checked; the script exits non-zero if a
check fails. Disagreements between two printed tables (Table VII summed over
circonscriptions vs Table VI) are reported as warnings and kept as printed.

Run from the repository root:  python3 data-raw/colonial_census/extract_eur1906_t6_t7.py
"""
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ocr  # noqa: E402

OUT = HERE / "csv"
TR = HERE / "transcribed"
ARK = ocr.ARK_1906

NATS = [("french", "Français"), ("italian", "Italiens"), ("maltese", "Maltais"),
        ("spanish", "Espagnols"), ("greek", "Grecs"), ("other_european", "Autres Européens")]
NAT_KEYS = [n for n, _ in NATS]

# profession groups as printed in Tables VI and VII
PROFS = [
    ("agriculture", "Agriculteurs",
     "Farmers (landowners, tenant farmers, sharecroppers, managers, foremen, gardeners and agricultural workers of all kinds)"),
    ("commerce", "Commerçants",
     "Traders (staff of shops, banks, insurance companies, brokerage and rental agencies)"),
    ("industry", "Industriels",
     "Industry (employers and workers of all trades engaged in manufacturing, incl. mines, quarries, salt works, oil mills, public-works contractors, fishermen)"),
    ("transport", "Entrepreneurs et Agents de transports",
     "Transport contractors and agents (shipping and railway companies, carriers, car hire)"),
    ("public_administration", "Fonctionnaires et employés des Administrations publiques",
     "Civil servants and employees of public administrations (State and municipal civil services, incl. judiciary)"),
    ("police", "Représentants et Agents de la force publique",
     "Police (agents of the public force)"),
    ("liberal_professions", "Représentants des professions libérales",
     "Liberal professions (lawyers, doctors, pharmacists, dentists, experts, business agents, artists, clergy and religious communities)"),
    ("rentiers", "Personnes vivant exclusivement de revenus",
     "Persons living exclusively on income (annuities, securities, rents)"),
    ("unclassified", "Population non classée",
     "Unclassified population (persons fitting none of the above categories)"),
]
PROF_KEYS = [p for p, _, _ in PROFS]
PROF_FR = {p: fr for p, fr, _ in PROFS}
PROF_EN = {p: en for p, _, en in PROFS}
# groups with a "Famille des précédents" (family members) column pair
WITH_FAMILY = PROF_KEYS[:7]

STATUS = {"active": "Personnes exerçant elles-mêmes la profession",
          "family": "Famille des précédents"}
SEX_FR = {"male": "Masc.", "female": "Fém."}

# Table VII column order (32 columns): for the 7 groups with family,
# active M, active F, family M, family F; then rentiers M, F; unclassified M, F
T7_COLS = [(p, s, x) for p in WITH_FAMILY for s in ("active", "family") for x in ("male", "female")]
T7_COLS += [(p, "active", x) for p in ("rentiers", "unclassified") for x in ("male", "female")]

CIRCS = ["Béja", "Medjez-el-Bab", "Bizerte", "Gabès", "Djerba", "Gafsa", "Tozeur",
         "Grombalia", "Kairouan", "Le Kef", "Teboursouk", "Mactar", "Sfax",
         "Souk-el-Arba", "Tabarca", "Sousse", "Thala", "Tunis", "Territoires du Sud"]

FIELDS = ["census", "table_id", "source_page", "gallica_view", "controle_civil",
          "nationality", "nationality_fr", "profession", "profession_fr",
          "status", "status_fr", "sex", "sex_fr", "value", "flag"]


class Checks:
    def __init__(self):
        self.n = 0
        self.fail = []
        self.warn = []  # disagreements between two printed tables, kept as printed

    def eq(self, label, got, printed, warn=False):
        self.n += 1
        if got != printed:
            (self.warn if warn else self.fail).append(f"{label}: sum {got} != printed {printed}")


def read_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(name, rows, fields=FIELDS):
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / name, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return len(rows)


def num(s):
    s = str(s).strip()
    return 0 if s in ("", "»", "0") else int(s)


# --------------------------------------------------------------------------
# Table VI
# --------------------------------------------------------------------------

# Table VI misprint: grand total of family males printed 22.262; the nationality
# cells, the profession rows (both sum to 22.662) and the printed totals 68.768
# and 128.895 all imply 22.662.
VI_MISPRINTS = {("total", "total"): (2, 22662, "printed 22.262")}


def table6(chk):
    """transcribed/eur1906_t6.csv: profession, nationality (incl. 'total'), and
    act_m, act_f, fam_m, fam_f, plus the printed subtotals act_tot, fam_tot, grand."""
    rows = read_csv(TR / "eur1906_t6.csv")
    cells = {}
    printed = {}
    for r in rows:
        p, n = r["profession"], r["nationality"]
        v = [num(r[k]) for k in ("act_m", "act_f", "fam_m", "fam_f")]
        if (p, n) in VI_MISPRINTS:
            i, good, _ = VI_MISPRINTS[(p, n)]
            v[i] = good
        cells[(p, n)] = v
        printed[(p, n)] = tuple(r[k] for k in ("act_tot", "fam_tot", "grand"))
    profs = PROF_KEYS + ["total"]
    for p in profs:
        for n in NAT_KEYS + ["total"]:
            v = cells[(p, n)]
            at, ft, g = printed[(p, n)]
            chk.eq(f"VI {p}/{n} active M+F", v[0] + v[1], num(at))
            if ft != "":
                chk.eq(f"VI {p}/{n} family M+F", v[2] + v[3], num(ft))
            if g != "":
                chk.eq(f"VI {p}/{n} grand", sum(v), num(g))
    # totals column = sum of nationalities; totals row = sum of professions
    for p in profs:
        for i in range(4):
            chk.eq(f"VI {p} col{i} across nationalities",
                   sum(cells[(p, n)][i] for n in NAT_KEYS), cells[(p, "total")][i])
    for n in NAT_KEYS + ["total"]:
        for i in range(4):
            chk.eq(f"VI {n} col{i} down professions",
                   sum(cells[(p, n)][i] for p in PROF_KEYS), cells[("total", n)][i])
    out = []
    for p in PROF_KEYS:
        for n, nfr in NATS:
            for i, (st, sx) in enumerate([("active", "male"), ("active", "female"),
                                          ("family", "male"), ("family", "female")]):
                if st == "family" and p not in WITH_FAMILY:
                    continue  # printed as » by construction; not a category
                out.append(dict(census="eur1906", table_id="VI", source_page=24 if n in NAT_KEYS[:3] else 25,
                                gallica_view=28, controle_civil="", nationality=n, nationality_fr=nfr,
                                profession=p, profession_fr=PROF_FR[p], status=st, status_fr=STATUS[st],
                                sex=sx, sex_fr=SEX_FR[sx], value=cells[(p, n)][i], flag=""))
    return out, cells


# --------------------------------------------------------------------------
# Table G (French population by profession group, 1901 and 1906)
# --------------------------------------------------------------------------

G_GROUPS = PROF_KEYS + ["total"]
G_UNITS = {  # Table G circonscription groups -> Table VII circonscriptions
    "Béja et Medjez-el-Bab": ["Béja", "Medjez-el-Bab"],
    "Gafsa et Tozeur": ["Gafsa", "Tozeur"],
}


def read_tg():
    out = {}
    for line in (TR / "eur1906_tg.txt").read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        unit, year, vals = line.split("|")
        v = [int(x) for x in vals.split()]
        assert len(v) == 30, (unit, year, len(v))
        out[(unit, year)] = {g: v[3 * i:3 * i + 3] for i, g in enumerate(G_GROUPS)}
    return out


# documented misprints in Table G: (unit, year, group, index) -> value implied by the other figures
G_MISPRINTS = {
    ("Le Kef", "1906", "transport", 2): (82, "printed 582; 52 + 30 = 82"),
    ("Souk-el-Arba", "1906", "police", 2): (33, "printed 32; 12 + 21 = 33"),
    ("Territoires du Sud", "1906", "unclassified", 0): (1, "printed »; total 24 - 23 women = 1, and Table VII gives 1"),
    ("Béja et Medjez-el-Bab", "1906", "agriculture", 0): (319, "printed 269; row total 730, column total 2.660 and Table VII (149 + 170) all give 319"),
    ("Béja et Medjez-el-Bab", "1906", "agriculture", 2): (522, "printed 472 (= 269 + 203); 319 + 203 = 522, column total 4.443"),
    ("Grombalia", "1906", "total", 0): (591, "printed 691; sum of the groups and Table VII give 591"),
    ("Grombalia", "1906", "total", 1): (440, "printed 340; sum of the groups and Table VII give 440"),
    ("Mactar", "1906", "total", 0): (44, "printed 46; sum of the groups and Table VII give 44"),
    ("Mactar", "1906", "total", 2): (73, "printed 75; 44 + 29 = 73"),
}


def table_g(chk):
    tg = read_tg()
    units = [u for (u, y) in tg if y == "1906" and u not in ("ENSEMBLE",)]
    rows = []
    for (u, y), d in tg.items():
        for g in G_GROUPS:
            h, f, t = d[g]
            label = f"G {u} {y} {g}"
            fixed = {}
            for k in range(3):
                if (u, y, g, k) in G_MISPRINTS:
                    fixed[k] = G_MISPRINTS[(u, y, g, k)][0]
            hh, ff, tt = fixed.get(0, h), fixed.get(1, f), fixed.get(2, t)
            chk.eq(label + " H+F", hh + ff, tt)
            if u == "AUGMENTATION":
                continue
            for sx, val, k in (("male", h, 0), ("female", f, 1)):
                flag = ""
                if (u, y, g, k) in G_MISPRINTS:
                    flag = "total_mismatch"
                if g == "total":
                    continue
                rows.append(dict(census="eur1906", table_id="G", source_page=62 if G_GROUPS.index(g) < 4 else 63,
                                 gallica_view=61, controle_civil=u if u != "ENSEMBLE" else "TOTAL (printed)",
                                 census_year=int(y), nationality="french", nationality_fr="Français",
                                 profession=g, profession_fr=PROF_FR[g], status="active_and_family",
                                 status_fr="Personnes exerçant la profession et leurs familles",
                                 sex=sx, sex_fr={"male": "Hommes", "female": "Femmes"}[sx], value=val, flag=flag))
    # columns: sum over circonscriptions == Ensemble; row totals == sum of groups
    for y in ("1906", "1901"):
        for g in G_GROUPS:
            for k in range(3):
                got = sum((G_MISPRINTS.get((u, y, g, k), (tg[(u, y)][g][k],))[0]) for u in units)
                chk.eq(f"G {y} {g} col{k} down circonscriptions", got, tg[("ENSEMBLE", y)][g][k])
        for u in units + ["ENSEMBLE"]:
            for k in range(3):
                got = sum(G_MISPRINTS.get((u, y, g, k), (tg[(u, y)][g][k],))[0] for g in PROF_KEYS)
                chk.eq(f"G {u} {y} total col{k} across groups", got,
                       G_MISPRINTS.get((u, y, "total", k), (tg[(u, y)]["total"][k],))[0])
    for g in G_GROUPS:
        for k in range(3):
            chk.eq(f"G augmentation {g} col{k}",
                   tg[("ENSEMBLE", "1906")][g][k] - tg[("ENSEMBLE", "1901")][g][k], tg[("AUGMENTATION", "1901-1906")][g][k])
    return rows, tg


# --------------------------------------------------------------------------
# Table VII (hand transcription + constraint solver for hidden cells)
# --------------------------------------------------------------------------

T7_VIEW = {c: v for v, cs in {29: CIRCS[0:4], 30: CIRCS[4:9], 31: CIRCS[9:14], 32: CIRCS[14:19]}.items() for c in cs}
T7_PAGES = {29: (26, 27), 30: (28, 29), 31: (30, 31), 32: (32, 33)}
# pair index k (0..13) covers columns 2k, 2k+1; columns 28..31 have per-column printed totals
PAIR_OF_COL = {c: c // 2 for c in range(28)}

# Printed Table VII cells contradicted by the printed circonscription total AND by
# the national total of Table VI (and, for French cells, by Table G). The printed
# value is kept in the data (flag total_mismatch); the implied value is used only
# to confirm that it reconciles every check.
# (circ, nationality, column) -> (printed, implied, note)
T7_MISPRINTS = {
    ("Tunis", "french", 31): (1443, 1413, "printed 1.443; pair total 4.410, Table VI (2.054) and Table G (1.413) imply 1.413"),
    ("Djerba", "greek", 5): (7, 0, "printed 7; commerce active total 70 and Table VI Greek total (16) imply 0"),
    ("Le Kef", "italian", 26): (1, 0, "printed 1; liberal-professions family total 9 and Table VI Italian total (201) imply 0"),
    ("Souk-el-Arba", "other_european", 3): (0, 1, "printed »; agriculture family total 200 and Table VI total (61) imply 1"),
}


def read_t7():
    cells, unknown, pair, group = {}, {}, {}, {}
    for line in (TR / "eur1906_t7.txt").read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        circ, kind, vals = line.split("|")
        toks = vals.split()
        if kind == "PAIR":
            assert len(toks) == 18, circ
            pair[circ] = [int(t) for t in toks]
        elif kind == "GROUP":
            assert len(toks) == 9, circ
            group[circ] = [int(t) for t in toks]
        else:
            assert len(toks) == 32, (circ, kind, len(toks))
            for c, t in enumerate(toks):
                if t.startswith("?"):
                    unknown[(circ, kind, c)] = int(t[1:]) if len(t) > 1 else None  # last-digit hint
                    cells[(circ, kind, c)] = None
                else:
                    cells[(circ, kind, c)] = int(t)
    return cells, unknown, pair, group


def solve_hidden(cells, unknown, pair, t6cells, tg):
    """Determine hidden cells from linear constraints with non-negative integers.

    Constraints: (1) per circonscription, the printed total of the column's pair
    (or column) minus the known cells; (2) per nationality, the Table VI national
    total minus all known cells of that column; (3) for French cells, Table G
    (French men/women by profession group, active + family, per circonscription).
    Bound propagation; a cell is fixed when lower == upper bound. Cells still
    undetermined are returned as None.
    """
    INF = 10 ** 9
    lo = {u: 0 for u in unknown}
    hi = {u: INF for u in unknown}
    cons = []  # (list of unknown keys, residual)
    cols = sorted({c for (_, _, c) in unknown})
    six = {("active", "male"): 0, ("active", "female"): 1, ("family", "male"): 2, ("family", "female"): 3}
    for c in cols:
        p, st, sx = T7_COLS[c]
        # (1) circonscription totals
        for circ in CIRCS:
            us = [(circ, n, c) for n in NAT_KEYS if (circ, n, c) in unknown]
            if not us:
                continue
            if c < 28:
                k = PAIR_OF_COL[c]
                tot = pair[circ][k]
                known = sum(cells[(circ, n, cc)] or 0 for n in NAT_KEYS for cc in (2 * k, 2 * k + 1)
                            if (circ, n, cc) not in unknown)
                others = [(circ, n, cc) for n in NAT_KEYS for cc in (2 * k, 2 * k + 1)
                          if (circ, n, cc) in unknown and cc != c]
            else:
                tot = pair[circ][14 + (c - 28)]
                known = sum(cells[(circ, n, c)] for n in NAT_KEYS if (circ, n, c) not in unknown)
                others = []
            cons.append((us + others, tot - known))
        # (2) national totals (Table VI)
        for n in NAT_KEYS:
            us = [(circ, n, c) for circ in CIRCS if (circ, n, c) in unknown]
            if not us:
                continue
            known = sum(cells[(circ, n, c)] for circ in CIRCS if (circ, n, c) not in unknown)
            cons.append((us, t6cells[(p, n)][six[(st, sx)]] - known))
        # (3) Table G for French cells: G men = active M + family M; G women = active F + family F
        for circ in CIRCS:
            if ((circ, "french", c)) not in unknown or p not in WITH_FAMILY:
                continue
            unit = next((u for u, cs in G_UNITS.items() if circ in cs), circ)
            members = G_UNITS.get(unit, [circ])
            gval = tg[(unit, "1906")][p][0 if sx == "male" else 1]
            ks = [(m, "french", cc) for m in members for cc in range(32)
                  if T7_COLS[cc][0] == p and T7_COLS[cc][2] == sx]
            us = [k for k in ks if k in unknown]
            known = sum(cells[k] for k in ks if k not in unknown)
            cons.append((us, gval - known))
    changed = True
    while changed:
        changed = False
        for us, r in cons:
            for u in us:
                rest_hi = sum(min(hi[v], INF) for v in us if v != u)
                rest_lo = sum(lo[v] for v in us if v != u)
                nlo = max(lo[u], r - rest_hi) if rest_hi < INF else lo[u]
                nhi = min(hi[u], r - rest_lo)
                if nlo != lo[u] or nhi != hi[u]:
                    lo[u], hi[u] = nlo, nhi
                    changed = True
        # last-digit hints tighten bounds
        for u, d in unknown.items():
            if d is None:
                continue
            a = lo[u]
            while a % 10 != d:
                a += 1
            b = hi[u]
            if b < INF:
                while b % 10 != d:
                    b -= 1
            if (a, b) != (lo[u], hi[u]):
                lo[u], hi[u] = a, b
                changed = True
    res = {}
    for u in unknown:
        if lo[u] > hi[u]:
            raise SystemExit(f"infeasible constraints for hidden cell {u}: [{lo[u]}, {hi[u]}]")
        res[u] = lo[u] if lo[u] == hi[u] else None
    bounds = {u: (lo[u], hi[u]) for u in unknown}
    return res, bounds, cons


def table7(chk, t6cells, tg):
    cells, unknown, pair, group = read_t7()
    assert set(pair) == set(CIRCS) and set(group) == set(CIRCS)
    fixed = dict(cells)
    for k, (_, implied, _) in T7_MISPRINTS.items():
        fixed[k] = implied
    solved, bounds, cons = solve_hidden(fixed, unknown, pair, t6cells, tg)
    vals = dict(cells)
    for u, v in solved.items():
        vals[u] = v
    for k, (printed, implied, _) in T7_MISPRINTS.items():
        assert cells[k] == printed, (k, cells[k])
        vals[k] = implied  # for the checks only
    # printed-total checks (only where every cell is known)
    for circ in CIRCS:
        def s(cols):
            vv = [vals[(circ, n, c)] for n in NAT_KEYS for c in cols]
            return None if any(x is None for x in vv) else sum(vv)
        for k in range(14):
            got = s([2 * k, 2 * k + 1])
            if got is not None:
                chk.eq(f"VII {circ} pair {T7_COLS[2 * k][0]}/{T7_COLS[2 * k][1]}", got, pair[circ][k])
        for i, c in enumerate(range(28, 32)):
            got = s([c])
            if got is not None:
                chk.eq(f"VII {circ} {T7_COLS[c][0]}/{T7_COLS[c][2]}", got, pair[circ][14 + i])
        for gi in range(7):
            chk.eq(f"VII {circ} group {WITH_FAMILY[gi]} printed", pair[circ][2 * gi] + pair[circ][2 * gi + 1], group[circ][gi])
        chk.eq(f"VII {circ} group rentiers printed", pair[circ][14] + pair[circ][15], group[circ][7])
        chk.eq(f"VII {circ} group unclassified printed", pair[circ][16] + pair[circ][17], group[circ][8])
    # Table VII summed over circonscriptions == Table VI (where all cells known)
    six = [("active", "male"), ("active", "female"), ("family", "male"), ("family", "female")]
    for c, (p, st, sx) in enumerate(T7_COLS):
        for n in NAT_KEYS:
            vv = [vals[(circ, n, c)] for circ in CIRCS]
            if all(x is not None for x in vv):
                chk.eq(f"VII-vs-VI {p}/{n}/{st}/{sx}", sum(vv), t6cells[(p, n)][six.index((st, sx))], warn=True)
    # French cells vs Table G (men = active M + family M, women = active F + family F)
    for unit in [u for (u, y) in tg if y == "1906" and u not in ("ENSEMBLE",)]:
        members = G_UNITS.get(unit, [unit])
        for p in PROF_KEYS:
            for k, sx in ((0, "male"), (1, "female")):
                vv = [vals[(m, "french", c)] for m in members for c, (pp, _, x) in enumerate(T7_COLS) if pp == p and x == sx]
                if all(x is not None for x in vv):
                    printed = G_MISPRINTS.get((unit, "1906", p, k), (tg[(unit, "1906")][p][k],))[0]
                    chk.eq(f"VII-vs-G {unit} {p} {sx}", sum(vv), printed)
    out = []
    for circ in CIRCS:
        view = T7_VIEW[circ]
        for n, nfr in NATS:
            for c, (p, st, sx) in enumerate(T7_COLS):
                key = (circ, n, c)
                v = vals[key]
                flag = ""
                if key in unknown:
                    flag = "derived_from_totals" if v is not None else "illegible"
                if key in T7_MISPRINTS:
                    v, flag = T7_MISPRINTS[key][0], "total_mismatch"
                page = T7_PAGES[view][0] if c < 12 else T7_PAGES[view][1]
                out.append(dict(census="eur1906", table_id="VII", source_page=page, gallica_view=view,
                                controle_civil=circ, nationality=n, nationality_fr=nfr,
                                profession=p, profession_fr=PROF_FR[p], status=st, status_fr=STATUS[st],
                                sex=sx, sex_fr=SEX_FR[sx], value="" if v is None else v, flag=flag))
    return out, unknown, solved, bounds

# --------------------------------------------------------------------------
# Profession tables printed in the commentary (pp. 57, 58, 61)
# --------------------------------------------------------------------------

TFIELDS = ["census", "table_id", "source_page", "gallica_view", "census_year", "nationality", "nationality_fr",
           "profession", "profession_fr", "status", "status_fr", "sex", "sex_fr", "measure", "value", "flag"]
NAT_FR = dict(NATS, all_european="Ensemble des Européens")
SEXES = {"male": "Sexe masculin", "female": "Sexe féminin", "total": "Total"}
TEXT_STATUS = {"active": "Exerçant une profession", "family": "Famille des précédents", "total": "Ensemble"}


def text_tables(chk, t6cells):
    out57, out58, out61 = [], [], []
    six = {"active": (0, 1), "family": (2, 3)}
    for r in read_csv(TR / "eur1906_text_p57.csv"):
        n, st = r["nationality"], r["status"]
        nk = "total" if n == "all_european" else n
        # counts exclude rentiers and unclassified (no family distinction)
        a, b = six[st]
        m = sum(t6cells[(p, nk)][a] for p in WITH_FAMILY)
        f = sum(t6cells[(p, nk)][b] for p in WITH_FAMILY)
        printed_m = int(r["male_n"])
        if (n, st) == ("all_european", "family"):
            printed_m_check = 22662  # same misprint as Table VI (22.262)
        else:
            printed_m_check = printed_m
        chk.eq(f"p57 {n}/{st} male vs Table VI", m, printed_m_check)
        chk.eq(f"p57 {n}/{st} female vs Table VI", f, int(r["female_n"]))
        chk.eq(f"p57 {n}/{st} total", printed_m_check + int(r["female_n"]), int(r["total_n"]))
        for sx in ("male", "female", "total"):
            for meas in ("n", "pct"):
                flag = "total_mismatch" if (n, st, sx, meas) == ("all_european", "family", "male", "n") else ""
                out57.append(dict(census="eur1906", table_id="text_p57", source_page=57, gallica_view=56,
                                  census_year=1906, nationality=n, nationality_fr=NAT_FR[n],
                                  profession="all_with_family_distinction",
                                  profession_fr="Toutes professions sauf revenus et non classés",
                                  status=st, status_fr=TEXT_STATUS[st], sex=sx, sex_fr=SEXES[sx],
                                  measure="count" if meas == "n" else "percent_of_nationality",
                                  value=r[f"{sx}_{meas}"], flag=flag))
    for r in read_csv(TR / "eur1906_text_p58.csv"):
        p, st = r["profession"], r["status"]
        for n in ("all_european", "french", "italian", "maltese"):
            nk = "total" if n == "all_european" else n
            v = t6cells[(p, nk)]
            exp = {"active": v[0] + v[1], "family": v[2] + v[3], "total": sum(v)}[st]
            chk.eq(f"p58 {p}/{st}/{n} vs Table VI", exp, int(r[f"{n}_n"]))
            for meas in ("n", "pct"):
                out58.append(dict(census="eur1906", table_id="text_p58", source_page=58, gallica_view=57,
                                  census_year=1906, nationality=n, nationality_fr=NAT_FR[n],
                                  profession=p, profession_fr=PROF_FR[p], status=st, status_fr=TEXT_STATUS[st],
                                  sex="total", sex_fr="Total",
                                  measure="count" if meas == "n" else "percent_of_nationality",
                                  value=r[f"{n}_{meas}"], flag=""))
    groups61 = {"agriculture": "Agriculture", "commerce_industry": "Commerce, Industrie", "transport": "Transports",
                "public_admin_police_liberal": "Administrations publiques, Force publique, Profess. libérales",
                "rentiers": "Vivant de leurs revenus", "no_or_unknown_profession": "Sans profession, Profession inconnue"}
    for r in read_csv(TR / "eur1906_text_p61.csv"):
        tot = sum(float(r[g]) for g in groups61)
        chk.eq(f"p61 {r['census_year']} shares sum to ~100", abs(tot - 100) < 0.6, True)
        for g, gfr in groups61.items():
            out61.append(dict(census="eur1906", table_id="text_p61", source_page=61, gallica_view=60,
                              census_year=int(r["census_year"]), nationality="french", nationality_fr="Français",
                              profession=g, profession_fr=gfr, status="active_and_family",
                              status_fr="Personnes exerçant la profession et leurs familles", sex="total", sex_fr="Total",
                              measure="percent_of_french_population", value=r[g], flag=""))
    return out57, out58, out61


def main():
    chk = Checks()
    t6, t6cells = table6(chk)
    tgrows, tg = table_g(chk)
    t7, unknown, solved, bounds = table7(chk, t6cells, tg)
    n6 = write_csv("eur1906_t6_profession_nationality.csv", t6)
    n7 = write_csv("eur1906_t7_profession_circonscription.csv", t7)
    # Table G itself is published by the other 1906 extraction
    # (csv/eur1906_tg_french_by_occupation_1901_1906.csv); it is read here only
    # as a validation source and as a constraint for the hidden Table VII cells.
    # The commentary tables (pp. 57, 58, 61) are published by the other 1906
    # extraction (csv/eur1906_text_professional_status.csv,
    # eur1906_text_occupation_groups.csv, eur1906_text_french_occupation_1896_1906.csv);
    # they are only checked here against Table VI.
    text_tables(chk, t6cells)
    print(f"VI: {n6} rows; VII: {n7} rows")
    print(f"hidden VII cells: {len(unknown)}, determined: {sum(v is not None for v in solved.values())}")
    for u in sorted(unknown, key=lambda k: (k[2], CIRCS.index(k[0]), NAT_KEYS.index(k[1]))):
        print("   ", u, "->", solved[u], "bounds", bounds[u])
    print(f"checks: {chk.n}, failed: {len(chk.fail)}")
    for f in chk.fail:
        print("  FAIL", f)
    print(f"warnings (Table VII vs Table VI, both as printed): {len(chk.warn)}")
    for f in chk.warn:
        print("  WARN", f)
    return 1 if chk.fail else 0


if __name__ == "__main__":
    sys.exit(main())
