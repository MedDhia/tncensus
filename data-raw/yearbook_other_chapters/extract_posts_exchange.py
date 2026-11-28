#!/usr/bin/env python3
"""Posts chapter, section "c) Taxe de change" / "Taux de change" of the Statistique générale de la Tunisie
(editions sgt1922-sgt1930): dated exchange rates applied to international money orders, by country, from 1915.

  python3 extract_posts_exchange.py check   parse the transcriptions, run the checks, print anomalies
  python3 extract_posts_exchange.py build   ... and write csv/posts_exchange_rates.csv and .md,
                                            csv/posts_exchange_survey.md and csv/posts_exchange_validation.json
  python3 extract_posts_exchange.py qa      list transcribed values not found among the Gallica OCR tokens of
                                            their page (cross-check only: every value was read on the image)

Source of truth: transcribed/posts_exchange_<edition>.txt (format in the header of each file). Every edition
reprints the whole series from 1915, so the printings overlap: each (country, year) is taken from the latest
edition that prints it (SPEC_ADDENDUM rule 4) and every other printing of the same (country, year) is compared
entry by entry.
"""
import re
import sys
from collections import Counter, defaultdict
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # shared helper yb_tables.py
from yb_tables import CREDIT, EDITIONS, ORDER, OUT, TR, fmt_val, write_csv, write_validation  # noqa: E402

NAME = "posts_exchange_rates"
SCRIPT = "extract_posts_exchange.py"
TABLE_ID = "c"

# Views of the exchange-rate section per edition (first and last view confirmed on the images).
VIEWS = {
    "sgt1922": (159, 171), "sgt1923": (643, 661), "sgt1924": (1133, 1156), "sgt1925": (169, 197),
    "sgt1926": (719, 752), "sgt1927": (181, 214), "sgt1928": (705, 738), "sgt1929": (183, 216),
    "sgt1930": (717, 750),
}
DONE = [e for e in ORDER if (TR / f"posts_exchange_{e}.txt").exists()]

MO_FR = "Mandats émis en monnaie étrangère"
COUNTRY = {  # code: (country_fr, money-order heading, normal conversion value as printed, default unit)
    "uk": ("Grande-Bretagne", MO_FR, "Valeur normale de la conversion : 1 £ = 25 fr. 20", "fr_per_pound"),
    "us": ("États-Unis d'Amérique", MO_FR, "Valeur normale de la conversion : 1 dollar = 5 fr. 25", "fr_per_dollar"),
    "nl": ("Pays-Bas", MO_FR, "Valeur normale de la conversion : 1 florin = 2 fr. 10", "fr_per_florin"),
    "dk": ("Danemark", MO_FR, "Valeur normale de la conversion : 1 couronne = 1 fr. 41", "fr_per_krone"),
    "se": ("Suède", MO_FR, "Valeur normale de la conversion : 1 couronne = 1 fr. 41", "fr_per_krone"),
    "no": ("Norvège", MO_FR, "Valeur normale de la conversion : 1 couronne = 1 fr. 41", "fr_per_krone"),
    "ch": ("Suisse", "", "", "change_pct"),
    "gr": ("Grèce", "", "", "change_pct"),
}
COUNTRY_EN = {"uk": "united_kingdom", "us": "united_states", "nl": "netherlands", "dk": "denmark", "se": "sweden",
              "no": "norway", "ch": "switzerland", "gr": "greece"}
UNIT = {  # code: unit_fr (column heading as printed, with the unit it implies)
    "fr_per_pound": "Francs (pour 1 £)",
    "fr_per_dollar": "Francs (pour 1 dollar)",
    "fr_per_florin": "Francs (pour 1 florin)",
    "fr_per_krone": "Francs (pour 1 couronne)",
    "change_pct": "Change % (fr.)",
    "fr_per_drachma": "Change % (fr.) : cours normal, 1 dr. = (francs pour 1 drachme)",
}
MONTH_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre",
            "novembre", "décembre"]

ENTRY = re.compile(r'^(?:(\(?\d{4}\)?)(?:=(\d{4}))?\s+)?(\d{1,2})\.(\d{1,2})(?:=(\d{1,2})\.(\d{1,2}))?\s+(\S+)(?:\s+"([^"]*)")?$')


# ----------------------------------------------------------------- parsing

def parse(ed):
    path = TR / f"posts_exchange_{ed}.txt"
    secs, cur, unit_state, notes = [], None, {}, []
    for n, line in enumerate(path.read_text().splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("@"):
            name, *kv = line[1:].split()
            kv = dict(x.split("=", 1) for x in kv)
            if name not in COUNTRY:
                raise ValueError(f"{path.name}:{n}: unknown country {name}")
            cur = {"country": name, "ed": ed, "view": int(kv["view"]), "page": int(kv["page"]), "img": "",
                   "entries": [], "year": None}
            unit_state.setdefault(name, COUNTRY[name][3])
            secs.append(cur)
            continue
        if line.startswith("img:"):
            cur["img"] = line[4:].strip()
            continue
        if line.startswith("unit:"):
            u = line[5:].strip()
            if u not in UNIT:
                raise ValueError(f"{path.name}:{n}: unknown unit {u}")
            unit_state[cur["country"]] = u
            continue
        if line.startswith("note:"):
            notes.append(line[5:].strip())
            continue
        m = ENTRY.match(line)
        if not m:
            raise ValueError(f"{path.name}:{n}: cannot parse {line!r}")
        ypr, ycor, dp, mp, dc, mc, tok, txt = m.groups()
        d, mo = (dc, mc) if dc else (dp, mp)
        if ypr and ypr.startswith("("):     # year not printed (a dash in the Années column): inferred
            cur["year"] = int(ypr.strip("()"))
            year_printed = None
            INFERRED.append((ed, cur["page"], cur["view"], cur["country"], cur["year"]))
        elif ypr:
            cur["year"] = int(ycor or ypr)
            year_printed = ypr
        elif cur["year"] is None:
            raise ValueError(f"{path.name}:{n}: no year at the top of the section")
        else:
            year_printed = None
        flag, value, prefer = "", None, None
        if ">" in tok:                      # printed value misprinted: take the value of another edition
            tok, prefer = tok.split(">")
        if tok.endswith("!"):
            flag, tok = "ocr_corrected", tok[:-1]
        if tok == "?":
            flag = "illegible"
        elif tok == "-":
            flag = "not_applicable"
        else:
            value = Decimal(tok)
        try:
            dt = date(cur["year"], int(mo), int(d))
        except ValueError as e:
            raise ValueError(f"{path.name}:{n}: {e}")
        cur["entries"].append({
            "census": ed, "table_id": TABLE_ID, "gallica_ark": EDITIONS[ed], "source_page": cur["page"],
            "gallica_view": cur["view"], "year": cur["year"], "date_from": dt, "date_to": None,
            "period_fr": f"{'1er' if int(dp) == 1 else int(dp)} {MONTH_FR[int(mp) - 1]} "
                         f"{year_printed or cur['year']}",
            "year_printed": year_printed, "year_misprint": bool(ycor), "date_misprint": bool(dc),
            "country": COUNTRY_EN[cur["country"]], "code": cur["country"], "country_fr": COUNTRY[cur["country"]][0],
            "money_order_fr": COUNTRY[cur["country"]][1], "par_fr": COUNTRY[cur["country"]][2],
            "unit": unit_state[cur["country"]], "unit_fr": UNIT[unit_state[cur["country"]]],
            "value": value, "value_type": "rate", "flag": flag, "note_fr": txt or ("; ".join(notes) if notes else ""),
            "break_before": bool(notes), "raw": tok, "line": n, "prefer": prefer, "printed": value,
        })
        notes = []
    return secs


# ----------------------------------------------------------------- checks

def check_printing(ed, series):
    """Within one printing: dates must increase down each country's column; printed years must increase."""
    anomalies, nchk = [], 0
    for c, es in series.items():
        for a, b in zip(es, es[1:]):
            nchk += 1
            if b["date_from"] <= a["date_from"]:
                anomalies.append(f"{ed} p.{b['source_page']} (f{b['gallica_view']}) {COUNTRY[c][0]}: "
                                 f"\"{b['period_fr']}\" ({fmt_val(b['printed']) or b['note_fr']}) printed after "
                                 f"\"{a['period_fr']}\" ({fmt_val(a['printed'])}): dates not increasing")
        for e in es:
            if e["date_misprint"]:
                anomalies.append(f"{ed} p.{e['source_page']} (f{e['gallica_view']}) {COUNTRY[c][0]}: date printed "
                                 f"\"{e['period_fr']}\" out of sequence, read as {e['date_from']} (`period_fr` "
                                 f"keeps the printed date)")
            if e["year_misprint"]:
                anomalies.append(f"{ed} p.{e['source_page']} (f{e['gallica_view']}) {COUNTRY[c][0]}: year printed "
                                 f"{e['year_printed']} in the Années column, read as {e['year']}")
        vals = [e for e in es if e["value"] is not None]
        for a, b, d in zip(vals, vals[1:], vals[2:]):
            if a["unit"] == b["unit"] == d["unit"] and b["value"] and a["value"] and d["value"]:
                r1, r2 = b["value"] / a["value"], b["value"] / d["value"]
                if (r1 > Decimal("1.5") and r2 > Decimal("1.5")) or (r1 < Decimal("0.67") and r2 < Decimal("0.67")):
                    anomalies.append(f"{ed} p.{b['source_page']} (f{b['gallica_view']}) {COUNTRY[c][0]}: "
                                     f"\"{b['period_fr']}\" printed {fmt_val(b['printed'])} between "
                                     f"{fmt_val(a['printed'])} and {fmt_val(d['printed'])} (isolated jump)")
    return nchk, anomalies


REPRINT = []
INFERRED = []
DOUBTS = [
    "sgt1923 p.158 (f660), Grèce, 15 January to 8 October 1923: the value column is printed without the leading "
    "dash and drifts upwards against the dates (by about two thirds of a line at the foot). There are 36 dates and "
    "36 value cells (one of them a bare \"»\"), so dates and values were paired in order. sgt1924 p.165 (f1155) "
    "reprints these entries with values and dates aligned line by line and gives the same pairing for every date.",
    "Grèce, 8 May 1921: sgt1922 prints 0.95, sgt1923 0.59 (digits transposed in one of them; the next values are "
    "0.80, 0.95, 0.90); sgt1924 repeats 0.59. The latest printing is stored, as for every other difference.",
    "États-Unis, 9 November 1923: sgt1923 and sgt1924 print \"48 »\" between 17.50 and 18.50; sgt1925-sgt1930 print 18, "
    "which is stored.",
    "Danemark, July 1926 (sgt1926-sgt1930): two value lines, 10 80 and 11 », are printed with no date between "
    "\"24 juillet\" and \"31 juillet\" (probably the 28 and 29 juillet printed for the other countries). Having no "
    "date, they are not stored.",
    "Norvège, 20 February 1924 (sgt1930 p.185): the value is printed \"3 5\" (a digit missing); 3.15 is taken from "
    "sgt1929, which agrees with sgt1924-sgt1928. Norvège, 13 August 1924: sgt1930 prints 2.25 and sgt1924-sgt1929 "
    "print 2.55 (between 2.65 and 2.60); 2.55 is taken from sgt1929. Both are flagged reprint_corrected.",
    "Dates printed out of order (13/6/8 September 1923 for Pays-Bas in sgt1928-sgt1930, 20/13 June 1920 for Suède "
    "in sgt1930, 28/27 February 1924 for Danemark in sgt1927-sgt1930, \"28 février\" for 28 avril 1924, \"8 juillet\" "
    "for 8 août 1925) are paired with their values as printed and read in date sequence. The earlier printings "
    "give the same date-value pairs in order. `period_fr` keeps the printed date.",
    "The 1923 sub-column of the Swiss table (sgt1930 p.191) has values that drift upwards against the dates. "
    "Dates and values (67 of each) were paired in order, and every other printing gives the same pairs.",
]


def select(all_series):
    """Rule 4 by (country, year): the latest edition printing that year for that country; compare the others."""
    by = defaultdict(dict)   # (code, year) -> ed -> [entries]
    for ed, series in all_series.items():
        for c, es in series.items():
            for e in es:
                by[(c, e["year"])].setdefault(ed, []).append(e)
    kept, compared, diffs, only = [], 0, [], []
    for (c, y), eds in sorted(by.items(), key=lambda kv: (list(COUNTRY).index(kv[0][0]), kv[0][1])):
        order = sorted(eds, key=ORDER.index)
        last = order[-1]
        for e in eds[last]:
            if e["prefer"]:
                alt = [x for x in eds.get(e["prefer"], []) if x["date_from"] == e["date_from"]]
                if len(alt) != 1:
                    raise ValueError(f"{e['census']} {c} {e['date_from']}: no single entry in {e['prefer']}")
                REPRINT.append(f"{e['census']} p.{e['source_page']} {COUNTRY[c][0]} {e['period_fr']}: printed "
                               f"\"{e['raw']}\", value {fmt_val(alt[0]['value'])} taken from {e['prefer']} "
                               f"p.{alt[0]['source_page']} (reprint_corrected)")
                e["value"], e["flag"] = alt[0]["value"], "reprint_corrected"
        kept += eds[last]

        def keyed(es):
            cnt, out = Counter(), {}
            for e in es:
                k = (e["date_from"], cnt[e["date_from"]])
                cnt[e["date_from"]] += 1
                out[k] = e
            return out
        L = keyed(eds[last])
        for ed in order[:-1]:
            O = keyed(eds[ed])
            for k in sorted(set(O) | set(L)):
                if k in O and k in L:
                    compared += 1
                    if O[k]["printed"] != L[k]["printed"] or O[k]["unit"] != L[k]["unit"]:
                        diffs.append({"country": COUNTRY[c][0], "date": k[0].isoformat(), "edition": ed,
                                      "printed": fmt_val(O[k]["printed"]), "page": O[k]["source_page"],
                                      "stored_from": last, "stored": fmt_val(L[k]["printed"]),
                                      "stored_page": L[k]["source_page"]})
                else:
                    e = O.get(k) or L[k]
                    only.append({"country": COUNTRY[c][0], "date": k[0].isoformat(), "value": fmt_val(e["value"]),
                                 "printed_in": e["census"], "page": e["source_page"],
                                 "missing_in": last if k in O else ed})
    return kept, compared, diffs, only


def assign_date_to(kept):
    """date_to = the day before the next later date printed for the country (stored series, sorted by date);
    left empty for the last date, for a date printed twice, and before a printed interruption of service."""
    by = defaultdict(list)
    for r in kept:
        by[r["code"]].append(r)
    out = []
    for c in COUNTRY:
        es = sorted(by.get(c, []), key=lambda r: (r["date_from"], ORDER.index(r["census"]), r["line"]))
        dates = Counter(r["date_from"] for r in es)
        for i, r in enumerate(es):
            nxt = next((x for x in es[i + 1:] if x["date_from"] > r["date_from"]), None)
            if nxt is not None and dates[r["date_from"]] == 1 and not nxt["break_before"]:
                r["date_to"] = nxt["date_from"] - timedelta(days=1)
            out.append(r)
    return out


def long_gaps(rows, days=365):
    by = defaultdict(list)
    for r in rows:
        by[r["code"]].append(r)
    g = []
    for c, es in by.items():
        for a, b in zip(es, es[1:]):
            if (b["date_from"] - a["date_from"]).days > days:
                g.append(f"{COUNTRY[c][0]}: {a['date_from']} to {b['date_from']}"
                         + (f" ({b['note_fr']})" if b["break_before"] else ""))
    return g


# ----------------------------------------------------------------- OCR cross-check

def ocr_values(ark, view):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "colonial_census"))
    import ocr  # noqa: E402
    vals = Counter()
    ws = [w for w in ocr.words(ark, view)]
    for a in ws:
        ta = a["text"].strip(".:,'")
        if not re.fullmatch(r"\d{1,3}", ta):
            continue
        vals[ta] += 1                                   # '26 »' with the » lost
        for b in ws:
            tb = b["text"].strip(".:,'")
            if abs(b["row"] - a["row"]) < 10 and 0 < b["col"] - a["col"] < 75 and re.fullmatch(r"\d{2,3}", tb):
                vals[f"{ta}.{tb}"] += 1
        m = re.fullmatch(r"(\d{1,3})[.,](\d{2,3})", a["text"])
        if m:
            vals[f"{m[1]}.{m[2]}"] += 1
    return vals


def fmt_pr(v):
    s = format(v, "f")
    if "." in s:
        i, f = s.split(".")
        return f"{i}.{f.ljust(2, '0')}"
    return s


def qa(eds):
    for ed in eds:
        for s in parse(ed):
            ov = ocr_values(EDITIONS[ed], s["view"])
            miss = [f"{e['period_fr']} {fmt_pr(e['value'])}" for e in s["entries"]
                    if e["value"] is not None and ov[fmt_pr(e["value"])] == 0]
            print(f"{ed} f{s['view']} {s['country']}: {len(s['entries'])} entries, {len(miss)} not in OCR: "
                  + "; ".join(miss))


# ----------------------------------------------------------------- output

COLS = ["census", "table_id", "gallica_ark", "source_page", "gallica_view", "year", "date_from", "date_to",
        "period_fr", "country", "country_fr", "money_order_fr", "par_fr", "unit", "unit_fr", "value", "value_type",
        "flag", "note_fr"]
COLDOC = {
    "census": "edition the value is taken from (`sgt1922` … `sgt1930`): the latest edition printing that country "
              "and year",
    "table_id": "`c` (section c) of the chapter's money-order tables: *Taxe de change*, later *Taux de change*)",
    "gallica_ark": "Gallica volume ark (views are numbered within a volume)",
    "source_page": "printed page number",
    "gallica_view": "Gallica view (fNNNN)",
    "year": "year of `date_from` (the *Années* column, printed at the top of each page and where the year changes)",
    "date_from": "ISO date printed in the *Dates* column: the date from which the rate applied",
    "date_to": "derived, not printed: the day before the next later date printed for the same country in the "
               "stored series; empty for the last date of a country, for a date printed twice, and before the "
               "printed interruption of the Greek service",
    "period_fr": "the date as printed (day, month and the year of the *Années* column as printed)",
    "country": "English code: `united_kingdom`, `united_states`, `netherlands`, `denmark`, `sweden`, `norway`, "
               "`switzerland`, `greece`",
    "country_fr": "country heading as printed (capitals in the source)",
    "money_order_fr": "sub-heading printed over the country (*Mandats émis en monnaie étrangère*: money orders "
                      "issued in the foreign currency); empty for Suisse and Grèce, which print none",
    "par_fr": "normal (par) value of the conversion printed under the heading; empty where none is printed",
    "unit": "`fr_per_pound`, `fr_per_dollar`, `fr_per_florin`, `fr_per_krone` (French francs for one unit of the "
            "foreign currency, column *Francs*), `change_pct` (column *Change %*, sub-heading *FR.*: the "
            "exchange premium in French francs per 100 francs of the foreign currency), `fr_per_drachma` "
            "(Greece from May 1921: francs for one drachma, after the printed line *Cours norm. 1 dr. =*)",
    "unit_fr": "the column heading as printed and the unit it implies",
    "value": "the rate as printed (`26 »` = 26; `25 60` = 25.60; `5 875` = 5.875)",
    "value_type": "`rate`",
    "flag": "empty, `ocr_corrected` (read on the image, the Gallica OCR differs), `illegible`, or "
            "`not_applicable` (a date printed with text instead of a rate; the text is in `note_fr`)",
    "note_fr": "text printed with the entry: a value cell holding text, or a line printed in the column before "
               "the entry (interruption of service)",
}


def notes_md(rows, res):
    eds = [e for e in ORDER if e in {r["census"] for r in rows}]
    years = sorted({r["year"] for r in rows})
    L = ["# Taxe de change (mandats-poste internationaux)", "",
         "*Exchange rates applied to international money orders, by country and date.*", "",
         f"Source: *Statistique générale de la Tunisie*, chapter *Postes - Télégraphes - Téléphones*, section "
         f"\"c) Taxe de change\" (heading of the first page; later editions print it the same way or as \"Taux de "
         f"change\"), editions transcribed: {', '.join(DONE)}. " + CREDIT, "",
         "Pages and views: " + "; ".join(
             f"{e} (`{EDITIONS[e]}`): f{VIEWS[e][0]}-f{VIEWS[e][1]}" for e in DONE) + ". Survey page by page: "
         "`posts_exchange_survey.md`.", "",
         f"Transcriptions: `../transcribed/posts_exchange_<edition>.txt`; rebuild with "
         f"`python3 data-raw/yearbook_other_chapters/{SCRIPT} build`.", "",
         f"Rows: {len(rows)} (one per printed date and rate). Years: {years[0]}-{years[-1]}. Stored from: "
         + ", ".join(f"{e} {sum(1 for r in rows if r['census'] == e)}" for e in eds) + ".", "",
         "Units: see `unit`. For the six countries under *Mandats émis en monnaie étrangère* the rate is the number "
         "of French francs given for one pound, dollar, florin or crown (the printed par value is in `par_fr`). "
         "For Switzerland and Greece the column is *Change %* with the sub-heading *FR.*: the premium of the "
         "foreign currency over the franc, in francs per 100 (e.g. 150 = 150 % premium). Greece switches on "
         "27 April 1921 to a direct quotation: the value cell of that date prints *Cours norm.*, the next line "
         "*1 dr. =*, and the following values (preceded by a dash that repeats *1 dr. =*) are francs per drachma "
         "(`fr_per_drachma`). value_type: rate.", "",
         "Every edition reprints the whole series from 1915 with the new dates added, so the printings overlap. "
         "Each country-year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = "
         "that edition); every other printing of the same country-year, read on its own page images, is compared "
         "date by date below.", "", "## Columns", ""]
    L += [f"- `{c}`: {COLDOC[c]}" for c in COLS]
    L += ["", "## Footnote", "",
          "Printed under the first page, against the title *Taxe de change (1)*: \"(1) A l'égard des pays pour "
          "lesquels les titres sont émis en monnaie étrangère, elle ressort du taux de conversion (voir tableaux "
          "ci-après, pages 146 et 147).\" Translation: (1) For the countries for which the money orders are issued "
          "in foreign currency, the exchange charge follows from the conversion rate (see the tables below, pages "
          "146 and 147). The page numbers are those of sgt1922 (the Swiss and Greek tables).", "",
          "## Validation", "",
          "There are no totals. Checks made instead:", "",
          f"- Order of the dates down each country's column, in every printing: {res['order_checks']} consecutive "
          f"pairs checked; {len(res['anomalies'])} anomalies (dates not increasing, or a misprinted year), kept as "
          "printed:"]
    L += [f"  - {a}" for a in res["anomalies"]] or ["  - none"]
    L += ["", "- Validity periods: `date_to` is derived from the next later date, so the stored periods are "
          "continuous and do not overlap by construction, except where a date is printed twice (both rows keep an "
          "empty `date_to`). Intervals longer than a year between two consecutive dates of a country (not gaps in "
          "the transcription: the next date printed is that far):"]
    L += [f"  - {g}" for g in res["long_gaps"]] or ["  - none"]
    L += ["", f"- Overlapping printings: {res['compared']} dates compared with another edition printing the same "
          f"country-year; {len(res['diffs'])} value differences; {len(res['only'])} dates printed in one edition "
          "but not in the other."]
    if res["diffs"]:
        L += ["", "| country | date | edition | printed (page) | stored from | printed (page) |",
              "|---|---|---|---|---|---|"]
        L += [f"| {d['country']} | {d['date']} | {d['edition']} | {d['printed']} (p. {d['page']}) | "
              f"{d['stored_from']} | {d['stored']} (p. {d['stored_page']}) |" for d in res["diffs"]]
    if res["only"]:
        L += ["", "| country | date | value | printed in (page) | not printed in |", "|---|---|---|---|---|"]
        L += [f"| {d['country']} | {d['date']} | {d['value']} | {d['printed_in']} (p. {d['page']}) | "
              f"{d['missing_in']} |" for d in res["only"]]
    L += ["", "- Values taken from another edition's printing (`reprint_corrected`):"]
    L += [f"  - {x}" for x in REPRINT] or ["  - none"]
    L += ["", "- Years not printed in the *Années* column (a dash where the year changes), inferred from the "
          "order of the dates:"]
    L += [f"  - {e} p.{p} (f{v}) {COUNTRY[c][0]}: {y}" for e, p, v, c, y in INFERRED] or ["  - none"]
    L += ["", "## Doubts", ""] + [f"- {x}" for x in DOUBTS]
    fl = Counter(r["flag"] for r in rows if r["flag"])
    L += ["", "- Flagged cells: " + (", ".join(f"{k}: {n}" for k, n in sorted(fl.items())) if fl else "none") + "."]
    L += [f"  - {r['census']} p.{r['source_page']} {r['country_fr']} {r['period_fr']}: "
          f"{fmt_val(r['value']) or 'NA'} ({r['flag']}{'; ' + r['note_fr'] if r['note_fr'] else ''})"
          for r in rows if r["flag"]]
    L += ["", "## Image versus OCR", "",
          "Every entry of every transcribed printing was read on native-resolution crops of the page image (strips "
          "of about 40 lines at full resolution, zoomed crops for doubtful digits); every section is marked "
          "`img: all`. The Gallica word OCR reads most rates but few dates; it was used only as a cross-check "
          f"(`{SCRIPT} qa`). Cells flagged `ocr_corrected`: {fl.get('ocr_corrected', 0)}."]
    remaining = [e for e in VIEWS if e not in DONE]
    if remaining:
        L += ["", "## Coverage", "", "Not yet transcribed: " + ", ".join(
            f"{e} f{VIEWS[e][0]}-f{VIEWS[e][1]}" for e in remaining) + ". Their dates and rates (which reprint and "
            "extend the series above) are not stored and not compared yet."]
    (OUT / f"{NAME}.md").write_text("\n".join(L) + "\n")


SURVEY = {}   # edition -> list of (view, page, text); filled from the transcriptions
METHOD = {
    "sgt1922": "read entirely on its own page images",
    "sgt1923": "compared line by line with this edition's page images, starting from an adjacent transcription",
    "sgt1924": "compared line by line with this edition's page images, starting from an adjacent transcription",
    "sgt1925": "drafted from the sgt1930 transcription, every line compared with this edition's page images",
    "sgt1926": "drafted from the sgt1930 transcription cut at 1926, every line compared with this edition's page images",
    "sgt1927": "drafted from the sgt1930 transcription cut at 1927, every line compared with this edition's page images",
    "sgt1928": "drafted from the sgt1930 transcription cut at 1928, every line compared with this edition's page images",
    "sgt1929": "drafted from the sgt1930 transcription cut at 1929, every line compared with this edition's page images",
    "sgt1930": "read entirely and independently on its own page images (native-resolution strips); no other "
               "transcription used",
}


def survey_md(all_secs):
    L = ["# Posts chapter, exchange rates: survey of every edition", "",
         "Section \"c) Taxe de change\" of the *Postes - Télégraphes - Téléphones* chapter (after the money-order "
         "tables a) and b)), page by page. First and last views confirmed on the page images (the view before is "
         "the money-order table b), the view after is the Caisse nationale d'épargne table). Extraction: "
         f"`{SCRIPT}`; table `{NAME}`.", "",
         "| edition | ark | views | transcribed | method |", "|---|---|---|---|---|"]
    for e, (a, b) in VIEWS.items():
        L.append(f"| {e} | `{EDITIONS[e]}` | {a}–{b} | {'yes' if e in DONE else 'not yet'} | "
                 f"{METHOD[e] if e in DONE else ''} |")
    L += ["", "## Views per edition", ""]
    for e in VIEWS:
        if e not in all_secs:
            L.append(f"- **{e}**: f{VIEWS[e][0]}-f{VIEWS[e][1]}, not transcribed yet.")
            continue
        pages = defaultdict(list)
        for s in all_secs[e]:
            pages[(s["view"], s["page"])].append(s)
        items = []
        for (v, p), ss in sorted(pages.items()):
            parts = []
            for s in ss:
                es = s["entries"]
                parts.append(f"{COUNTRY[s['country']][0]} {es[0]['date_from']} to {es[-1]['date_from']} "
                             f"({len(es)})")
            items.append(f"f{v} p. {p}: " + "; ".join(parts))
        L.append(f"- **{e}**: " + ". ".join(items) + ".")
    L += ["", "Countries, in printed order: Grande-Bretagne, États-Unis d'Amérique, Pays-Bas (three per page, "
          "*Mandats émis en monnaie étrangère*, column *Francs*); Danemark, Suède, Norvège (same layout); Suisse "
          "and Grèce (column *Change %*; Suisse printed in two sub-columns per page). Each page carries the "
          "columns *Années*, *Dates*, rate."]
    (OUT / "posts_exchange_survey.md").write_text("\n".join(L) + "\n")


def build(write=True):
    all_secs = {ed: parse(ed) for ed in DONE}
    all_series = {}
    nchk, anomalies = 0, []
    for ed, secs in all_secs.items():
        by = defaultdict(list)
        for s in secs:
            by[s["country"]].extend(s["entries"])
        all_series[ed] = by
        n, a = check_printing(ed, by)
        nchk += n
        anomalies += a
    kept, compared, diffs, only = select(all_series)
    rows = assign_date_to(kept)
    res = {"order_checks": nchk, "anomalies": anomalies, "compared": compared, "diffs": diffs, "only": only,
           "long_gaps": long_gaps(rows)}
    print(f"{len(rows)} rows from {', '.join(DONE)}; {nchk} order checks, {len(anomalies)} anomalies; "
          f"{compared} overlap comparisons, {len(diffs)} differences, {len(only)} dates in one printing only")
    for a in anomalies:
        print("  ", a)
    if write:
        write_csv(NAME, COLS, rows)
        notes_md(rows, res)
        survey_md(all_secs)
        write_validation(OUT / "posts_exchange_validation.json", {
            NAME: {"rows": len(rows), "editions_transcribed": DONE,
                   "editions_not_transcribed": [e for e in VIEWS if e not in DONE],
                   "rows_by_edition": {e: sum(1 for r in rows if r["census"] == e) for e in DONE},
                   "printed_entries_by_edition": {e: sum(len(s["entries"]) for s in all_secs[e]) for e in DONE},
                   "order_checks": nchk, "anomalies": anomalies, "overlap_compared": compared,
                   "overlap_diffs": diffs, "overlap_dates_in_one_printing": only, "long_intervals": res["long_gaps"],
                   "flagged": [f"{r['census']} p.{r['source_page']} {r['country']} {r['date_from']}: {r['flag']}"
                               for r in rows if r["flag"]]},
            "_views": VIEWS})
    return rows


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    if mode == "qa":
        qa(sys.argv[2:] or DONE)
    else:
        build(write=(mode == "build"))


if __name__ == "__main__":
    main()
