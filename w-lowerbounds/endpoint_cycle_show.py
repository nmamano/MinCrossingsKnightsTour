"""Print the critical cycle of endpoint_stab.py crit ORIENT as rows of selected edges, and check it unrolled."""
import sys
import numpy as np
from endpoint_stab import graph, augment, tests, key
orient = sys.argv[1]
states, W, src, dst, wt = graph()
S, D, Wt, B, M = augment(states, W, src, dst, wt, orient)
cyc = np.load(f'endpoint_cycle_{orient}.npy')
A = 9 ** len(tests(orient))
# order arcs along the cycle
nxt = {int(S[a]): int(a) for a in cyc}
start = [int(S[a]) for a in cyc if states[int(S[a]) // A][0] == 0][0]
order = []; v = start
for _ in range(len(cyc)):
    a = nxt[v]; order.append(a); v = int(D[a])
assert v == start
edges = set(); y = 0
for a in order:
    u = int(S[a]) // A; t = int(D[a]) // A; x = states[u][0]; shift = 1 if x == W - 1 else 0
    for e in states[t][1]:
        if (e[0], e[1]) == (x, -shift):
            edges.add(((e[0], y), (e[2], e[3] + shift + y)))
    print(f'row {y} cell x={x}: w={int(Wt[a])} b={int(B[a])}')
    if shift: y += 1
P = y
print('period (rows):', P, 'edges per period:', sorted(edges))
# unrolled check over many periods: degrees, crossings per period, test at every row
from strip2_independent import proper
K = 12
E = {((a[0], a[1] + P * k), (b[0], b[1] + P * k)) for k in range(K) for a, b in edges}
deg = {}
for a, b in E:
    for c in (a, b): deg[c] = deg.get(c, 0) + 1
mid = range(P * 3, P * (K - 3))
for yy in mid:
    for x in range(4):
        dgt = deg.get((x, yy), 0)
        assert (dgt == 2) if x < 2 else (dgt <= 2), (x, yy, dgt)
per = [e for e in E if P * 5 <= min(e[0][1], e[1][1]) < P * 6]
cr = 0
for e in per:
    for f in E:
        if f != e and proper(e, f):
            cr += 1 if min(f[0][1], f[1][1]) >= P * 5 and min(f[0][1], f[1][1]) < P * 6 and f < e else 0
            cr += 1 if not (P * 5 <= min(f[0][1], f[1][1]) < P * 6) and f[0][1] + f[1][1] < e[0][1] + e[1][1] else 0
print('degree check PASS on middle periods')
for yy in range(P * 5, P * 6):
    for coef, exc in tests(orient):
        sel = {key((a[0], a[1] - yy), (b[0], b[1] - yy)) for a, b in E if min(a[1], b[1]) <= yy <= max(a[1], b[1])}
        F = sum(coef.get(k, 0) for k in sel)
        print(f'row {yy}: F mod 3 = {F % 3}, exceptional edges = {len(exc & sel)}', '-> FAIL' if (F % 3 != 2 or len(exc & sel) == 2) else '-> pass')
