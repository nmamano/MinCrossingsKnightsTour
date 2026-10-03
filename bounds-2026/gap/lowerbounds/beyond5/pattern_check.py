#!/usr/bin/env python3
"""Independent recount (tour_scan.py routines, not joint_stab.py) of S* crossings, g_up, g_down and changed ports
for a period-1 collar pattern. usage: pattern_check.py U|P"""
import sys
import tour_scan as TS
import frac_stab as FS
from strip_dp import cross
PAT = {'P': [((2, 0), (0, -1)), ((0, -1), (1, 1)), ((1, 1), (3, 2)), ((2, 0), (4, 1))],
       'U': [((3, -1), (1, 0)), ((1, 0), (0, 2)), ((0, 2), (2, 1)), ((2, 1), (4, 2))]}[sys.argv[1]]
R = 30
E = set()
for y in range(-R, R):
    for a, b in PAT:
        u, v = (a[0], a[1] + y), (b[0], b[1] + y); u, v = sorted((u, v), key=lambda p: (p[1], p[0])); E.add(u + v)
w2 = sorted([e for e in E if min(e[0], e[2]) <= 1], key=lambda e: (e[1], e[0]))
XS = sum(1 for i, f in enumerate(w2) if f[1] == 0 for e in w2[:i] if cross(e, f))
deg = {}
for e in E:
    for p in ((e[0], e[1]), (e[2], e[3])): deg[p] = deg.get(p, 0) + 1
assert all(deg[(x, 0)] == 2 for x in range(3)), deg
out = {}
for orient in ('up', 'down'):
    coef, exc = FS.test(orient)
    F = sum(coef.get(FS.key((a, b), (c, d)), 0) for a, b, c, d in w2); Ex = sum(FS.key((a, b), (c, d)) in exc for a, b, c, d in w2)
    vr = 0 if orient == 'up' else -1
    near = [e for e in w2 if vr - 3 <= e[1] <= vr + 1 and e[3] >= vr]
    out[orient] = (F % 3, Ex, TS.vis_pairs(near, vr))
print(sys.argv[1], 'S* crossings per row', XS, ' (F mod 3, exception edges, VIS) up/down', out)
