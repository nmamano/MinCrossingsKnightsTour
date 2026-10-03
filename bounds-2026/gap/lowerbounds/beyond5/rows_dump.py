#!/usr/bin/env python3
"""Per-row dump of one side: XS(r), g_up(r), changed ports (exact) at row r, and the width-three edge word of row r.
usage: rows_dump.py TOUR.json SIDE [R0]"""
import sys
from collections import defaultdict
import tour_scan as TS
import frac_stab as FS
from strip_dp import cross

f, s = sys.argv[1], int(sys.argv[2]); R0 = int(sys.argv[3]) if len(sys.argv) > 3 else 8
n, E = TS.load(f)
T = [lambda v: v, lambda v: (n - 1 - v[0], v[1]), lambda v: (v[1], v[0]), lambda v: (n - 1 - v[1], v[0])][s]
loc = [tuple(sorted((T(a), T(b)), key=lambda p: (p[1], p[0]))) for a, b in E]
w3 = sorted([(a[0], a[1], b[0], b[1]) for a, b in loc if min(a[0], b[0]) <= 2], key=lambda e: (e[1], e[0]))
w2 = [e for e in w3 if min(e[0], e[2]) <= 1]
XS = defaultdict(int)
for i, f2 in enumerate(w2):
    for e in w2[:i]:
        if cross(e, f2): XS[f2[1]] += 1
coef, exc = FS.test('up')
for r in range(R0, n - R0):
    F = sum(coef.get(FS.key((a, b - r), (c, d - r)), 0) for a, b, c, d in w2)
    Ex = sum(FS.key((a, b - r), (c, d - r)) in exc for a, b, c, d in w2)
    near = [e for e in w2 if r - 3 <= e[1] <= r + 1 and e[3] >= r]
    g = 1 if (F % 3 != 2 or Ex >= 2 or TS.vis_pairs(near, r)) else 0
    word = ' '.join(f'{a}{c}{d-b:+d}' for a, b, c, d in w3 if b == r)
    print(f'{r:3d} XS={XS[r]} g={g} F={F%3} Ex={Ex} | {word}')
