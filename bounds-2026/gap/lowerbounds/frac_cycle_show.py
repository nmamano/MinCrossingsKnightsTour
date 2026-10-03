#!/usr/bin/env python3
"""Print the critical cycle of frac_stab.py crit ORIENT as rows of edges; re-check it on an unrolled field
with code that does not use the transfer graph (degrees, crossings per period, penalties per row)."""
import sys
from itertools import combinations
import numpy as np
from frac_stab import graph, augment, test, key, charge
from strip2_independent import proper
orient = sys.argv[1]
states, W, src, dst, wt = graph()
S, D, Wt, T, M = augment(states, W, src, dst, wt, orient)
cyc = np.load(f'frac_cycle_{orient}.npy')
A = 18
nxt = {int(S[a]): int(a) for a in cyc}
start = [int(S[a]) for a in cyc if states[int(S[a]) // A][0] == 0][0]
order = []; v = start
for _ in range(len(cyc)):
    a = nxt[v]; order.append(a); v = int(D[a])
assert v == start
edges = set(); y = 0
for a in order:
    u = int(S[a]) // A; t = int(D[a]) // A; x = states[u][0]; shift = 1 if x == W - 1 else 0
    par = (int(S[a]) % A) // 9
    for e in states[t][1]:
        if (e[0], e[1]) == (x, -shift):
            edges.add(((e[0], y), (e[2], e[3] + shift + y)))
    print(f'row {y} (parity {par}) cell x={x}: w={int(Wt[a])} t={int(T[a])}')
    if shift: y += 1
P = y
print('cycle length (rows):', P, 'edges:', sorted(edges))
K = 12
E = {((a[0], a[1] + P * k), (b[0], b[1] + P * k)) for k in range(K) for a, b in edges}
deg = {}
for a, b in E:
    for c in (a, b): deg[c] = deg.get(c, 0) + 1
for yy in range(P * 3, P * (K - 3)):
    for x in range(4):
        d = deg.get((x, yy), 0)
        assert (d == 2) if x < 2 else (d <= 2), (x, yy, d)
print('degree check PASS on middle periods (columns 0,1 degree 2; columns 2,3 degree <= 2)')
lo, hi = P * 5, P * 6
cr = sum(1 for e, f in combinations(E, 2) if proper(e, f)
         and lo <= max(min(e[0][1], e[1][1]), min(f[0][1], f[1][1])) < hi)
coef, exc = test(orient)
tot = [0, 0]
for yy in range(lo, hi):
    sel = {key((a[0], a[1] - yy), (b[0], b[1] - yy)) for a, b in E if min(a[1], b[1]) <= yy <= max(a[1], b[1])}
    F = sum(coef.get(k, 0) for k in sel) % 3; ex = len(exc & sel)
    ts = [charge(F, ex, (yy - lo + ph) % 2) for ph in (0, 1)]
    tot = [tot[0] + ts[0], tot[1] + ts[1]]
    print(f'row {yy}: F mod 3 = {F}, exceptional edges = {ex}, t(phase 0)={ts[0]} t(phase 1)={ts[1]}')
print(f'crossings per {P} rows: {cr}; sum(w-1/4) = {cr - P}; best phase: sum a = {max(tot) / 2}, '
      f'ratio = {(cr - P) / (max(tot) / 2)}')
