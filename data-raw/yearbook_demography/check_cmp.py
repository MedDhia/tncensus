"""Parse and check the 'Statistique comparée' tables (Europeans by circonscription, two censuses)."""
import sys
NATS = ["french", "italian", "maltese", "spanish", "greek", "other_european"]
def parse(path):
    R = {}
    for ln in open(path, encoding="utf-8"):
        ln = ln.split("#")[0].strip()
        if not ln: continue
        name, rest = ln.split(None, 1)
        g = [[int(x) for x in s.split()] for s in rest.split("|")]
        R[name.replace("_", " ")] = g
    return R
def check(R, out=print, ngroups=7):
    n = bad = 0
    def c(nm, a, b):
        nonlocal n, bad
        n += 1
        if a != b: bad += 1; out(f"  {nm}: {a} != printed {b}")
    rows = [k for k in R if k != "TOTAUX"]
    for k in rows:
        g = R[k]
        for i in range(ngroups):
            if len(g[i]) == 3: c(f"{k} g{i} change", g[i][1] - g[i][0], g[i][2])
        for y in (0, 1):
            c(f"{k} total y{y}", sum(g[i][y] for i in range(6)), g[6][y])
    for i in range(ngroups):
        for j in range(len(R["TOTAUX"][i])):
            c(f"TOTAUX g{i}.{j}", sum(R[k][i][j] for k in rows), R["TOTAUX"][i][j])
    if len(R["TOTAUX"]) > ngroups:
        for j in range(len(R["TOTAUX"][ngroups])):
            c(f"TOTAUX g{ngroups}.{j}", sum(R[k][ngroups][j] for k in rows), R["TOTAUX"][ngroups][j])
    return n, bad
if __name__ == "__main__":
    print(check(parse(sys.argv[1])))
