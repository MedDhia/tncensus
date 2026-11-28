"""Parse and check the town tables (Europeans by nationality, Muslims, Jews)."""
import sys
def parse(path):
    B = []
    for ln in open(path, encoding="utf-8"):
        ln = ln.split("#")[0].rstrip()
        if not ln.strip(): continue
        if ln.startswith("@"):
            p = ln.split(); B.append(dict(group=p[1], view=int(p[2]), page=int(p[3]), rows=[])); continue
        town, ctrl, eur, ind, tot = [s.strip() for s in ln.split("|")]
        B[-1]["rows"].append(dict(town=town, controle=ctrl, eur=list(map(int, eur.split())),
                                  ind=list(map(int, ind.split())), total=int(tot)))
    return B
def check(B, out=print):
    n = bad = 0; fails = []
    def c(nm, a, b):
        nonlocal n, bad
        n += 1
        if a != b: bad += 1; fails.append(nm); out(f"  {nm}: {a} != printed {b}")
    for b in B:
        for r in b["rows"]:
            e, i = r["eur"], r["ind"]
            c(f"{b['group']} {r['town']} european total", sum(e[:6]), e[6])
            c(f"{b['group']} {r['town']} indigenous total", i[0] + i[1], i[2])
            c(f"{b['group']} {r['town']} grand total", e[6] + i[2], r["total"])
    return n, bad, fails
if __name__ == "__main__":
    print(check(parse(sys.argv[1]))[:2])
