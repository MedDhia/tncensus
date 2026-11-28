#!/usr/bin/env python3
"""Build 1906 European census Tables I-III (eur1906, Gallica ark bd6t53563851).

Two steps:

  draft  Parse Gallica's word-level OCR (via ocr.py) into one editable text file
         per page view, with one printed row per line and the row-sum check
         marked. Drafts go to a directory you name, so verified files are never
         overwritten:
             python3 extract_eur1906_t1_t3.py draft /tmp/drafts

  build  Read the verified transcriptions in transcriptions/eur1906_t[123]_f*.txt,
         run every total check, and write the tidy CSVs to csv/:
             python3 extract_eur1906_t1_t3.py build

Transcription format (checked against the page images, one file per view):
  # view N                    page view (Gallica fNNNN)
  ## Contrôle de X            section header (Table II; Table III uses ## A) / ## B))
  name | v1 v2 ... vk total   data row; '*' after a value = corrected from the image
  = Label | value             printed running total (Table III Report / A reporter)
  text after '  # '           note
"""
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TR = HERE / "transcriptions"
OUT = HERE / "csv"
sys.path.insert(0, str(HERE))
import ocr  # noqa: E402

ARK = ocr.ARK_1906
MANIFEST = HERE.parent / "bnf_gallica" / "pages" / ARK / "manifest.json"

NATS = ["french", "italian", "maltese", "spanish", "greek", "other_european"]
NATS_FR = ["Français", "Italiens", "Maltais", "Espagnols", "Grecs", "Autres Européens"]

# Table I circonscriptions, as printed there; annexes and their parent contrôle.
ANNEXE_PARENT = {"Medjez-el-Bab": "Béja", "Djerba": "Gabès", "Tozeur": "Gafsa",
                 "Teboursouk": "Le Kef", "Tabarca": "Souk-el-Arba"}
# Table II section headers -> (controle_civil, annexe), using Table I spellings.
HEADER = {
    "Contrôle de Béja": ("Béja", ""), "Annexe de Medjez-el-Bab": ("Béja", "Medjez-el-Bab"),
    "Contrôle de Bizerte": ("Bizerte", ""), "Contrôle de Gabès": ("Gabès", ""),
    "Annexe de Djerba": ("Gabès", "Djerba"), "Contrôle de Gafsa": ("Gafsa", ""),
    "Annexe de Tozeur": ("Gafsa", "Tozeur"), "Contrôle de Grombalia": ("Grombalia", ""),
    "Contrôle de Kairouan": ("Kairouan", ""), "Contrôle du Kef": ("Le Kef", ""),
    "Annexe de Téboursouk": ("Le Kef", "Teboursouk"), "Contrôle de Mactar": ("Mactar", ""),
    "Contrôle de Sfax": ("Sfax", ""), "Contrôle de Souk-el-Arba": ("Souk-el-Arba", ""),
    "Annexe de Tabarca": ("Souk-el-Arba", "Tabarca"), "Contrôle de Sousse": ("Sousse", ""),
    "Contrôle de Thala": ("Thala", ""), "Contrôle de Tunis": ("Tunis", ""),
    "Territoires du Sud": ("Territoires du Sud", ""),
}


def page_of_view():
    m = json.loads(MANIFEST.read_text())
    return {i + 1: c["label"]["fr"][0] for i, c in enumerate(m["items"])}


def read_rows(path):
    """Yield (kind, payload) from a transcription file."""
    for ln in path.read_text().splitlines():
        ln = ln.split("  # ")[0].rstrip()
        if not ln or ln.startswith("# "):
            continue
        if ln.startswith("## "):
            yield "header", ln[3:].strip()
        elif ln.startswith("= "):
            name, v = ln[2:].split("|")
            yield "check", (name.strip(), int(v))
        else:
            name, v = ln.split("|")
            toks = v.split()
            vals = [int(t.rstrip("*")) for t in toks]
            stars = [t.endswith("*") for t in toks]
            yield "row", (name.strip(), vals, stars)


class Log:
    def __init__(self):
        self.checks = self.passed = self.corrected = 0
        self.fail = []

    def check(self, what, got, want):
        self.checks += 1
        if got == want:
            self.passed += 1
        else:
            self.fail.append(f"{what}: computed {got}, printed {want}")


def write_csv(name, header, rows):
    OUT.mkdir(exist_ok=True)
    with open(OUT / name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def build_t1(pages, log):
    v = 9
    rows, totals, out = [], None, []
    for kind, (name, vals, stars) in ((k, p) for k, p in read_rows(TR / f"eur1906_t1_f{v:03d}.txt")):
        if name == "TOTAUX":
            totals = vals
            continue
        log.check(f"T1 row {name}", sum(vals[:6]), vals[6])
        rows.append((name, vals))
        ctrl, ann = (ANNEXE_PARENT[name], name) if name in ANNEXE_PARENT else (name, "")
        for i in range(6):
            log.corrected += stars[i]
            out.append(["eur1906", "I", int(pages[v]), v, ctrl, ann, NATS[i], NATS_FR[i], vals[i],
                        "ocr_corrected" if stars[i] else ""])
    for i in range(7):
        log.check(f"T1 column {i}", sum(r[1][i] for r in rows), totals[i])
    write_csv("eur1906_t1_circonscription_nationality.csv",
              ["census", "table_id", "source_page", "gallica_view", "controle_civil", "annexe",
               "nationality", "nationality_fr", "value", "flag"], out)
    return {r[0]: r[1] for r in rows}


def build_t2(pages, log, t1):
    out, sums = [], {}
    ctrl = ann = None
    n_loc = 0
    for v in range(10, 20):
        for kind, p in read_rows(TR / f"eur1906_t2_f{v:03d}.txt"):
            if kind == "header":
                ctrl, ann = HEADER[p]
                continue
            name, vals, stars = p
            n_loc += 1
            log.check(f"T2 row {name} (view {v})", sum(vals[:6]), vals[6])
            key = ann or ctrl
            s = sums.setdefault(key, [0] * 7)
            for i in range(7):
                s[i] += vals[i]
            for i in range(6):
                log.corrected += stars[i]
                out.append(["eur1906", "II", int(pages[v]), v, ctrl, ann, name, NATS[i], NATS_FR[i],
                            vals[i], "ocr_corrected" if stars[i] else ""])
    # every contrôle / annexe sum must equal its Table I row
    for unit, want in t1.items():
        for i in range(7):
            log.check(f"T2 sum {unit} col {i} vs Table I", sums.get(unit, [0] * 7)[i], want[i])
    write_csv("eur1906_t2_locality_nationality.csv",
              ["census", "table_id", "source_page", "gallica_view", "controle_civil", "annexe",
               "locality", "nationality", "nationality_fr", "value", "flag"], out)
    return n_loc


SECTION = {"A) Français": ("french", "Français"), "B) Etrangers": ("foreign", "Étrangers")}


def birthplace_type(group, name):
    if name.startswith("Algérie, département"):
        return "algeria_department"
    if name.startswith("Italie, "):
        return "italy_region"
    if group == "french":
        if name in ("Tunisie",):
            return "country"
        if name.startswith("Colonies"):
            return "french_colonies"
        if name == "Etranger":
            return "abroad"
        if name == "Lieux inconnus":
            return "unknown"
        return "france_department"
    if name in ("Amérique du Nord", "Amérique du Sud", "Antilles anglaises", "Asie", "Australie"):
        return "region"
    return "country"


def build_t3(pages, log):
    out, run, group = [], 0, None
    for v in (20, 21):
        for kind, p in read_rows(TR / f"eur1906_t3_f{v:03d}.txt"):
            if kind == "header":
                if SECTION[p][0] != group:
                    group = SECTION[p][0]
                    run = 0
                continue
            if kind == "check":
                name, want = p
                if name == "Report":
                    log.check(f"T3 report carried to view {v}", run, want)
                else:
                    log.check(f"T3 {group} '{name}' (view {v})", run, want)
                continue
            name, vals, stars = p
            run += vals[0]
            log.corrected += stars[0]
            out.append(["eur1906", "III", int(pages[v]), v, group, SECTION_FR[group],
                        birthplace_type(group, name), name, vals[0], "ocr_corrected" if stars[0] else ""])
    write_csv("eur1906_t3_birthplace.csv",
              ["census", "table_id", "source_page", "gallica_view", "nationality_group",
               "nationality_group_fr", "birthplace_type", "birthplace_fr", "value", "flag"], out)
    return len(out)


SECTION_FR = {"french": "Français", "foreign": "Étrangers"}


def build():
    pages = page_of_view()
    log = Log()
    t1 = build_t1(pages, log)
    n2 = build_t2(pages, log, t1)
    n3 = build_t3(pages, log)
    print(f"Table II localities: {n2}; Table III birthplaces: {n3}")
    print(f"checks: {log.checks}, passed: {log.passed}, cells corrected from image: {log.corrected}")
    for f in log.fail:
        print("MISMATCH", f)
    return 0 if not log.fail else 1


# ---------------------------------------------------------------- OCR drafts
def _words(view):
    ocr.words(ARK, view)
    out = []
    for it in json.loads((ocr.CACHE / f"{ARK}_f{view:03d}.json").read_text())["items"]:
        x, y, w, h = map(int, re.search(r"xywh=(\d+),(\d+),(\d+),(\d+)", it["target"]).groups())
        out.append({"row": x + w / 2, "col": y + h / 2, "l": y, "r": y + h, "text": it["body"]["value"]})
    return out


def draft(outdir, views=range(9, 20), ncol=7):
    """Rows of numbers binned to columns by right edge (figures are right-aligned)."""
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    last = None
    for v in views:
        rws = ocr.rows(_words(v), 18)
        cand = []
        for r in rws:
            tail = r[-ncol:]
            if len(r) > ncol and all(ocr.to_int(w["text"]) is not None for w in tail) \
                    and ocr.to_int(r[-ncol - 1]["text"]) is None:
                cand.append([w["r"] for w in tail])
        edges = [sorted(c[i] for c in cand)[len(cand) // 2] for i in range(ncol)] if len(cand) >= 3 else last
        last = edges
        numstart = edges[0] - 0.85 * (edges[1] - edges[0])
        lines = [f"# view {v}"]
        for r in rws:
            merged = []
            for w in r:  # re-join split thousands such as '1' + '.516'
                if merged and re.match(r"^[.,]\d{3}$", w["text"]) and re.match(r"^\d{1,3}$", merged[-1]["text"]) \
                        and w["l"] - merged[-1]["r"] < 60:
                    merged[-1] = dict(merged[-1], text=merged[-1]["text"] + w["text"], r=w["r"])
                else:
                    merged.append(w)
            lab = re.sub(r"\.{2,}", "", " ".join(w["text"] for w in merged if w["r"] <= numstart)).strip(" .")
            vals = [None] * ncol
            for w in merged:
                if w["r"] <= numstart:
                    continue
                iv = ocr.to_int(w["text"])
                if iv is None:
                    continue
                k = min(range(ncol), key=lambda i: abs(edges[i] - w["r"]))
                vals[k] = iv
            if all(x is None for x in vals):
                if lab and r[0]["row"] > 950:
                    lines.append(("## " if re.match(r"^(Contrôle|Annexe|Territoires)", lab) else "+ ") + lab)
                continue
            if r[0]["row"] < 950:
                continue
            ok = "" if None in vals or sum(vals[:-1]) == vals[-1] else "   !SUM"
            lines.append(f"{lab} | {' '.join('?' if x is None else str(x) for x in vals)}{ok}")
        (outdir / f"eur1906_f{v:03d}.txt").write_text("\n".join(lines) + "\n")
    print(f"drafts written to {outdir}")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "build":
        sys.exit(build())
    if len(sys.argv) >= 3 and sys.argv[1] == "draft":
        draft(sys.argv[2])
        sys.exit(0)
    print(__doc__)
    sys.exit(2)
