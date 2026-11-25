"""Parse and check a transcription of table f (profession x nationality)."""
import sys
CATS = ["agriculture", "commerce", "industry", "transport", "public_administration",
        "police_force", "liberal_professions", "independent_means", "unclassified"]
NATS = ["french", "italian", "maltese", "spanish", "greek", "other_european"]
E_TOTALS = {"french": 71020, "italian": 89216, "maltese": 8396, "spanish": 517, "greek": 646,
            "other_european": 3486}
FLAGS = {}
def parse(path):
    B = {}; cur = None; FLAGS.clear()
    for ln in open(path, encoding="utf-8"):
        ln = ln.split("#")[0].strip()
        if not ln: continue
        if ln.startswith("@"):
            _, nat, view, page = ln.split(); cur = B[nat] = dict(view=int(view), page=int(page), rows={})
        elif ln.startswith("F "):
            p = ln.split(); FLAGS[(p[1], p[2], int(p[3]))] = (p[4], " ".join(p[5:]))
        else:
            a, b = ln.split("|"); a = a.split()
            cur["rows"][a[0]] = (list(map(int, a[1:])), list(map(int, b.split())))
    return B
def check(B, out=print):
    n = bad = 0
    def c(name, x, y):
        nonlocal n, bad
        n += 1
        if x != y: bad += 1; out(f"  {name}: cells {x} != printed {y}")
    for nat, b in B.items():
        R = b["rows"]
        for cat in CATS + ["total"]:
            v, s = R[cat]
            c(f"{nat} {cat} active M+F", v[0] + v[1], s[0])
            c(f"{nat} {cat} family M+F", v[2] + v[3], s[1])
            c(f"{nat} {cat} subtotals", s[0] + s[1], s[2])
        for k in range(4):
            c(f"{nat} col {k} vs TOTAUX", sum(R[cat][0][k] for cat in CATS), R["total"][0][k])
        for k in range(3):
            c(f"{nat} subtotal {k} vs TOTAUX", sum(R[cat][1][k] for cat in CATS), R["total"][1][k])
        if nat in E_TOTALS:
            c(f"{nat} total vs table e", R["total"][1][2], E_TOTALS[nat])
    for cat in CATS + ["total"]:
        for k in range(4):
            c(f"all {cat} col {k} = sum of nationalities", sum(B[nat]["rows"][cat][0][k] for nat in NATS), B["all_europeans"]["rows"][cat][0][k])
        for k in range(3):
            c(f"all {cat} subtotal {k} = sum of nationalities", sum(B[nat]["rows"][cat][1][k] for nat in NATS), B["all_europeans"]["rows"][cat][1][k])
    return n, bad
if __name__ == "__main__":
    n, bad = check(parse(sys.argv[1])); print(f"{n} checks, {bad} failing")
