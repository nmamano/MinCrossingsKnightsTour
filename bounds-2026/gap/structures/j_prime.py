# KT Structures, 2026-10-03. BEYOND5 13.8: tour-level J' = J + Y_sh per side (side frame, LB rows 8..n-9).
# J = (X3 - rows) + Q3'/2 from q3_check.py logic (via b5plus_check RAW lines is not needed: recomputed here).
# Y_sh = crossing pairs NOT both reaching local x <= 2, whose overlap quarters all lie in squares x <= 4 with row in
# 8..n-9 (the shallow pair atoms of nu3 outside S3). usage: j_prime.py TOUR.json...
import sys, json
from pathlib import Path
from collections import defaultdict
import fold_exact_scan as F
def orient(a, b, c): return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
def proper(e, g):
    a, b = e; c, d = g
    return orient(a, b, c)*orient(a, b, d) < 0 and orient(c, d, a)*orient(c, d, b) < 0
for f in sys.argv[1:]:
    grid = json.loads(Path(f).read_text())['tour']; n = len(grid)
    E = {F.edge((x, n-1-y), (x+F.MOVES[int(v)][1], n-1-y-F.MOVES[int(v)][0])) for y, row in enumerate(grid) for x, code in enumerate(row) for v in code}
    T = [lambda v: v, lambda v: (n-1-v[0], v[1]), lambda v: (v[1], v[0]), lambda v: (n-1-v[1], v[0])]
    rows = range(8, n-8); res = []
    for sd in range(4):
        loc = [tuple(sorted((T[sd](a), T[sd](b)))) for a, b in E]
        near = [e for e in loc if min(e[0][0], e[1][0]) <= 6]
        tq = {e: {(x+e[0][0], y+e[0][1], k) for x, y, k in F.templates[e[1][0]-e[0][0], e[1][1]-e[0][1]]} for e in near}
        byrow = defaultdict(list)
        for e in near: byrow[min(e[0][1], e[1][1])].append(e)
        Y = 0
        for e in near:
            y0 = min(e[0][1], e[1][1])
            for r in range(y0-2, y0+3):
                for g in byrow[r]:
                    if g <= e or not proper(e, g): continue
                    if min(e[0][0], e[1][0]) <= 2 and min(g[0][0], g[1][0]) <= 2: continue
                    ov = tq[e] & tq[g]
                    if ov and all(q[0] <= 4 and q[1] in rows for q in ov): Y += 1
        res.append(Y)
    print(Path(f).name, n, 'Y_sh per side', res, 'total', sum(res), flush=True)
