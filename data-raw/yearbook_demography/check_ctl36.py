"""Parse and check the 1936 contrôle-civil table (Muslim | Jewish | indig | European | grand)."""
import sys
def parse(path):
    R = {}
    for ln in open(path, encoding="utf-8"):
        ln = ln.split("#")[0].strip()
        if not ln: continue
        name, rest = ln.split(None, 1)
        R[name.replace("_", " ")] = [[int(x) for x in s.split()] for s in rest.split("|")]
    return R
def check(R, out=print):
    n = bad = 0
    def c(nm, a, b):
        nonlocal n, bad
        n += 1
        if a != b: bad += 1; out(f"  {nm}: {a} != printed {b}")
    rows = [k for k in R if k != "TOTAUX"]
    for k in R:
        m, j, i, e, g = R[k]
        c(f"{k} muslim total", sum(m[:7]), m[7]); c(f"{k} jewish total", sum(j[:6]), j[6])
        c(f"{k} indigenous", m[7] + j[6], i[0]); c(f"{k} european total", sum(e[:6]), e[6])
        c(f"{k} grand", i[0] + e[6], g[0])
    for gi in range(5):
        for k in range(len(R["TOTAUX"][gi])):
            c(f"column {gi}.{k}", sum(R[r][gi][k] for r in rows), R["TOTAUX"][gi][k])
    return n, bad
if __name__ == "__main__":
    print(check(parse(sys.argv[1])))
