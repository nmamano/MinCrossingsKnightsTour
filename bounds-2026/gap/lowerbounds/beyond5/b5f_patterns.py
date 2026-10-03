# KT Lower Bounds, 2026-10-03, B5f: exact J per row of the period-1 width-6 collars of FOLD24_n96 side 0
# (U: rows 33..39, P: rows 8..27; b5f_boundary.py). J = (X3 - rows) + Q3/2 with r_b.py's definitions.
import sys
from pathlib import Path
from collections import defaultdict
from itertools import combinations
from math import comb
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(ROOT / 'gap/turnstheory')); sys.path.insert(0, str(ROOT / 'gap/verifier'))
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE.parent / 'windows'))
from f1v_stab import tile_quarters
from strip_dp import cross
PORTS = [(4, 2, 1), (5, 2, 1)]
PAT = {'P': [(0, 1, 2), (0, 2, 1), (1, 2, 1), (2, 2, 1), (3, 2, 1)],
       'U': [(0, 2, 1), (1, -1, 2), (1, 2, 1), (2, 2, 1), (3, 2, 1)]}
for name, pat in PAT.items():
    E = [(x, y, x + dx, y + dy) for y in range(-12, 40) for x, dx, dy in pat + PORTS]
    rows = range(0, 24)
    w3 = [e for e in E if min(e[0], e[2]) <= 2]
    X3 = sum(1 for i, f in enumerate(w3) if f[1] in rows for e in w3[:i] if e != f and cross(e, f))
    X3 = sum(1 for e, f in combinations(w3, 2) if cross(e, f) and min(e[1], f[1]) in rows and max(e[1], f[1]) in rows or (cross(e, f) and max(e[1], f[1]) in rows and min(e[1], f[1]) not in rows and False))
    # count each crossing pair once, booked on the later lower end (r_b.py convention)
    X3 = sum(1 for e, f in combinations(w3, 2) if cross(e, f) and max(e[1], f[1]) in rows)
    w5 = [e for e in E if min(e[0], e[2]) <= 4]
    tq = {e: tile_quarters(e) for e in w5}
    mult = defaultdict(int); byq = defaultdict(list)
    for e in w5:
        for t in tq[e]: mult[t] += 1; byq[t].append(e)
    holes = w3c = x1 = 0
    for r in rows:
        for x in range(5):
            for qn in 'brtl':
                m = mult[(x, r, qn)]
                if m == 0: holes += 1
                else: w3c += comb(m - 1, 2)
    seen = set()
    for t, es in byq.items():
        if not (0 <= t[0] <= 4 and t[1] in rows): continue
        for e1, e2 in combinations(es, 2):
            if (e1, e2) in seen: continue
            seen.add((e1, e2))
            if len(tq[e1] & tq[e2]) == 1: x1 += 1
    R = len(rows); Q3 = holes + w3c + x1
    print(name, 'per row: X3', X3 / R, 'holes', holes / R, 'W3', w3c / R, 'X1', x1 / R, 'Q3', Q3 / R, 'J', (X3 - R) / R + Q3 / 2 / R)
