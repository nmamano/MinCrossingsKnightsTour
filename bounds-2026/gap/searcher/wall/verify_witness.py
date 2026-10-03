#!/usr/bin/env python3
"""Independent check of a periodic wall witness from wall.cpp (KT Edge Searcher, 2026-10-03).
Edges of one period (board coordinates), period vector (PX, PY). Unrolls K periods, then reports, for the middle
rows: degrees of modeled cells, cycles among the edges, crossings per row, quarter multiplicities per square
column, and the psi jump (sum of chi(a)(m_+ + m_- + 1) mod 3 along a horizontal transversal)."""
import sys, itertools
from collections import defaultdict
sys.path.insert(0, __file__.rsplit('/', 2)[0])
from check_identity import tile_quarters   # same directory level: gap/searcher/check_identity.py

def run(period_edges, PX, PY, modeled, K=12, label=''):
    E = set()
    for k in range(-K, K + 1):
        for (a, b) in period_edges:
            p = (a[0] + k * PX, a[1] + k * PY); q = (b[0] + k * PX, b[1] + k * PY)
            E.add(tuple(sorted([p, q])))
    deg = defaultdict(int)
    for p, q in E: deg[p] += 1; deg[q] += 1
    ylo, yhi = -2 * PY, 2 * PY   # inspect middle rows
    bad = [(c, deg[c]) for c in deg if ylo <= c[1] < yhi and modeled(c) and deg[c] != 2]
    bad += [(c, d) for c in [(x, y) for y in range(ylo, yhi) for x in range(-20, 30) if modeled((x, y))] for d in [deg[c]] if d != 2]
    print(f"{label}: modeled cells with degree != 2 in rows [{ylo},{yhi}): {sorted(set(bad))[:6]}")
    print(f"{label}: max degree overall {max(deg.values())}")
    # cycles (union-find)
    par = {}
    def f(x):
        while par.setdefault(x, x) != x: par[x] = par[par[x]]; x = par[x]
        return x
    cyc = 0
    for p, q in sorted(E):
        a, b = f(p), f(q)
        if a == b: cyc += 1
        else: par[a] = b
    print(f"{label}: edges closing a cycle: {cyc}")
    # crossings with lower-row assignment in the middle period
    def cross(e, g):
        (p1, p2), (q1, q2) = e, g
        if len({p1, p2, q1, q2}) < 4: return False
        def o(a, b, c): v = (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0]); return (v > 0) - (v < 0)
        return o(p1, p2, q1) * o(p1, p2, q2) < 0 and o(q1, q2, p1) * o(q1, q2, p2) < 0
    EL = sorted(E)
    TQ = {e: set(tile_quarters(*e)) for e in EL}
    nx = 0
    for e, g in itertools.combinations(EL, 2):
        if cross(e, g) and 0 <= max(min(e[0][1], e[1][1]), min(g[0][1], g[1][1])) < PY: nx += 1
    print(f"{label}: crossings per period (later edge's lower row in [0,{PY})): {nx}  -> {nx / PY} per row")
    m = defaultdict(int)
    for e in EL:
        for t in TQ[e]: m[t] += 1
    for j in range(0, PY):
        row = []
        for X in range(-4, 12):
            row.append(''.join(str(m[(X, j, q)]) for q in range(4)))
        print(f"   square row {j}: " + ' '.join(f"{X}:{r}" for X, r in zip(range(-4, 12), row)))
    return E, m

if __name__ == '__main__':
    W = [((-1,0),(1,1)), ((1,0),(3,1)), ((1,0),(2,2)), ((2,0),(3,2)), ((3,0),(5,1)), ((3,0),(4,2)),
         ((0,1),(2,2)), ((2,1),(4,2)), ((2,1),(3,3)), ((4,1),(6,2)), ((4,1),(5,3)),
         ((1,2),(3,3)), ((1,2),(2,4)), ((3,2),(5,3)),
         ((0,3),(2,4)), ((2,3),(4,4)), ((2,3),(3,5)), ((4,3),(6,4)), ((4,3),(5,5))]
    # modeled cells: u = x - floor((1 + y)/2) + floor(1/2) in [0, 4)
    mod = lambda c: 0 <= c[0] - ((1 + c[1]) // 2) < 4
    run(W, 2, 4, mod, label='shear 1/2 witness')
