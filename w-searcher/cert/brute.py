"""Tiny brute-force cross-check of certify.cpp: backtracking over edges (own code)."""
import sys
sys.setrecursionlimit(10000)
def load(path):
    t = open(path).read().split(); i = 0
    nc = int(t[i]); i += 1; cells = []
    for _ in range(nc): cells.append((int(t[i]), int(t[i+1]), int(t[i+2]))); i += 3
    ne = int(t[i]); i += 1; E = []
    for _ in range(ne): E.append(tuple(int(v) for v in t[i:i+4])); i += 4
    return cells, E
def orient(a, b, c):
    v = (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0]); return (v > 0) - (v < 0)
def cr(a, b, c, d): return orient(a,b,c)*orient(a,b,d) < 0 and orient(c,d,a)*orient(c,d,b) < 0
cells, E = load(sys.argv[1])
P = [(c[0], c[1]) for c in cells]
X = {}
for i, e in enumerate(E):
    for j, f in enumerate(E):
        if i < j and not ((e[2] & 1) and (f[2] & 1)) and not ((e[2] | f[2]) & 4) and cr(P[e[0]], P[e[1]], P[f[0]], P[f[1]]):
            X.setdefault(i, []).append(j); X.setdefault(j, []).append(i)
deg = [0] * len(cells); ch = [False] * len(E); out = set()
inc = [[] for _ in cells]
for i, e in enumerate(E): inc[e[0]].append(i); inc[e[1]].append(i)
last = [max(inc[c]) if inc[c] else -1 for c in range(len(cells))]
def rec(i, fl):
    if i == len(E):
        if all(deg[c] == 2 for c in range(len(cells)) if cells[c][2] == 2): out.add(fl)
        return
    e = E[i]
    # option skip
    if not (e[2] & 1):
        ok = all(not (cells[c][2] == 2 and last[c] == i and deg[c] != 2) for c in (e[0], e[1]))
        if ok: rec(i + 1, fl)
    if not (e[2] & 2) and deg[e[0]] < 2 and deg[e[1]] < 2 and not any(ch[j] for j in X.get(i, [])):
        deg[e[0]] += 1; deg[e[1]] += 1; ch[i] = True
        ok = all(not (cells[c][2] == 2 and last[c] == i and deg[c] != 2) for c in (e[0], e[1]))
        if ok: rec(i + 1, fl + e[3])
        deg[e[0]] -= 1; deg[e[1]] -= 1; ch[i] = False
rec(0, 0)
print(sorted(out))
