"""Parse and check a transcription of table e (age x sex x marital status)."""
import sys
AGES = ["0_4", "5_9", "10_14", "15_19", "20_24", "25_29", "30_34", "35_39", "40_44",
        "45_49", "50_54", "55_59", "60_plus"]
FLAGS = {}
def parse(path):
    B = []; G = None; FLAGS.clear()
    for ln in open(path, encoding="utf-8"):
        ln = ln.split("#")[0].strip()
        if not ln: continue
        p = ln.split()
        if p[0] == "@": B.append(dict(nat=p[1], view=int(p[2]), page=int(p[3]), rows={}, S=None, T=None))
        elif p[0] == "S": B[-1]["S"] = list(map(int, p[1:]))
        elif p[0] == "T": B[-1]["T"] = list(map(int, p[1:]))
        elif p[0] == "G": G = list(map(int, p[1:]))
        elif p[0] == "F": FLAGS[(p[1], p[2], int(p[3]))] = (p[4], " ".join(p[5:]))
        else: B[-1]["rows"][p[0]] = list(map(int, p[1:]))
    return B, G
def check(B, G=None, out=print):
    bad = 0; n = 0
    def c(name, a, b):
        nonlocal bad, n
        n += 1
        if a != b: bad += 1; out(f"  {name}: cells {a} != printed {b}")
    for b in B:
        R = b["rows"]
        assert list(R) == AGES, (b["nat"], list(R))
        for a in AGES:
            c(f"{b['nat']} {a} row", sum(R[a][:8]), R[a][8])
        for k in range(8):
            c(f"{b['nat']} col {k} vs Totaux par sexe", sum(R[a][k] for a in AGES), b["S"][k])
        for m in range(4):
            c(f"{b['nat']} Totaux {m} = M+F", b["S"][2 * m] + b["S"][2 * m + 1], b["T"][m])
        c(f"{b['nat']} total col", sum(R[a][8] for a in AGES), b["T"][4])
        c(f"{b['nat']} grand = sum Totaux", sum(b["T"][:4]), b["T"][4])
    if G:
        for m in range(4):
            c(f"Totaux généraux {m}", sum(b["T"][m] for b in B), G[m])
        c("Totaux généraux total", sum(b["T"][4] for b in B), G[4])
    return n, bad
if __name__ == "__main__":
    B, G = parse(sys.argv[1]); n, bad = check(B, G); print(f"{n} checks, {bad} failing")
