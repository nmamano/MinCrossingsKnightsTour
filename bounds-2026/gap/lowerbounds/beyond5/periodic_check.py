#!/usr/bin/env python3
"""Exact check of a periodic side strip (KT Lower Bounds, 2026-10-03, beyond-5n pilot).

Takes the width-three edges (an end in columns 0..2) of one side of a tour, rows a..a+P-1 (by lower end), repeats
them with period P, and checks in the middle period:
  degree exactly 2 in columns 0, 1, 2; degree <= 2 in the ghost columns 3, 4; no finite cycle in columns 0..2;
  XS  = width-two crossing pairs per period (counted at the lower end row of the later edge);
  g_up(r), g_down(r) (f1v_stab.py definitions: up test F, exception pair, VIS(r) / VIS(r-1));
  NRE = changed ports per period (Structures definition, collar = columns 0..2, P rule c -> c -+ 3),
        collar partner traced inside the periodic strip.
Prints XS - P - g and NRE per period.
usage: periodic_check.py TOUR.json SIDE a P
"""
import sys
from collections import defaultdict
import tour_scan as TS
import frac_stab as FS
from strip_dp import cross

f, s, a, P = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
n, E = TS.load(f)
T = [lambda v: v, lambda v: (n - 1 - v[0], v[1]), lambda v: (v[1], v[0]), lambda v: (n - 1 - v[1], v[0])][s]
loc = [tuple(sorted((T(u), T(v)), key=lambda p: (p[1], p[0]))) for u, v in E]
base = [(u[0], u[1] - a, v[0], v[1] - a) for u, v in loc if min(u[0], v[0]) <= 2 and a <= u[1] < a + P]
K = 8
edges = sorted({(x0, y0 + k * P, x1, y1 + k * P) for k in range(-K, K + 1) for (x0, y0, x1, y1) in base},
               key=lambda e: (e[1], e[0]))
lo, hi = -2 * P, 3 * P          # rows checked for degrees: far from the truncated ends
deg = defaultdict(int); adj = defaultdict(set)
for x0, y0, x1, y1 in edges:
    deg[x0, y0] += 1; deg[x1, y1] += 1
    adj[x0, y0].add((x1, y1)); adj[x1, y1].add((x0, y0))
for y in range(lo, hi):
    for x in range(5):
        d = deg[x, y]
        assert (d == 2 if x <= 2 else d <= 2), ('degree', x, y, d)
w2 = [e for e in edges if min(e[0], e[2]) <= 1]
XS = 0
for i, f2 in enumerate(w2):
    if not 0 <= f2[1] < P: continue
    for e in w2[:i]:
        if cross(e, f2): XS += 1
g = {}
for orient in ('up', 'down'):
    coef, exc = FS.test(orient); gs = []
    for r in range(P):
        F = sum(coef.get(FS.key((x0, y0 - r), (x1, y1 - r)), 0) for x0, y0, x1, y1 in w2)
        Ex = sum(FS.key((x0, y0 - r), (x1, y1 - r)) in exc for x0, y0, x1, y1 in w2)
        vr = r if orient == 'up' else r - 1
        near = [e for e in w2 if vr - 3 <= e[1] <= vr + 1 and e[3] >= vr]
        gs.append(1 if (F % 3 != 2 or Ex >= 2 or TS.vis_pairs(near, vr)) else 0)
    g[orient] = gs
# collar paths and ports (collar = columns 0..2, interior = columns >= 3)
def label(o, q):
    d = (q[0] - o[0], q[1] - o[1]); sgn = 1 if d[0] * d[1] > 0 else -1
    return (sgn, abs(d[0]) == 2, q[0] - 2 * q[1] if sgn == 1 else q[0] + 2 * q[1])
def partner(o, q):
    prev, cur, steps = q, o, 0
    while True:
        nx = [v for v in adj[cur] if v != prev]
        assert len(nx) == 1; prev, cur = cur, nx[0]; steps += 1
        assert steps < 4 * P * K, 'collar path too long (infinite collar path?)'
        if cur[0] >= 3: return (prev, cur)
NRE = 0; ports = 0
for x0, y0, x1, y1 in edges:
    u, v = (x0, y0), (x1, y1)
    if (u[0] <= 2) == (v[0] <= 2): continue
    o, q = (u, v) if u[0] <= 2 else (v, u)
    if not 0 <= o[1] < P: continue
    ports += 1
    po, pq = partner(o, q); l1, l2 = label(o, q), label(po, pq)
    ok = l1[1] and l2[1] and l1[0] == l2[0] and l2[2] - l1[2] == (-3 if l1[2] % 2 == 0 else 3)
    NRE += 0 if ok else 1
# finite cycles inside the collar
seen = set()
for y in range(lo, hi):
    for x in range(3):
        if (x, y) in seen: continue
        comp, st = [], [(x, y)]
        while st:
            v = st.pop()
            if v in seen or v[0] > 2: continue
            seen.add(v); comp.append(v); st.extend(adj[v])
        if all(lo - 4 * P < v[1] < hi + 4 * P for v in comp) and all(len([w for w in adj[v] if w[0] <= 2]) == 2 for v in comp):
            raise AssertionError(('finite collar cycle', comp[:6]))
print(f'{f.split("/")[-1]} side {s} rows {a}..{a + P - 1} (period {P}): XS = {XS}, g_up = {sum(g["up"])} {g["up"]}, '
      f'g_down = {sum(g["down"])} {g["down"]}, ports = {ports}, NRE = {NRE}')
print(f'  XS - P - g_up = {XS - P - sum(g["up"])},  XS - P - g_down = {XS - P - sum(g["down"])},  NRE = {NRE}')
