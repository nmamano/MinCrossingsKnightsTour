#!/usr/bin/env python3
"""W3b: minimum number of bad quarters forced by charged corner paths (gap/lowerbounds FINDINGS W3).

Corner box as in w3_corner.py (board corner at (0,0); box cells degree exactly 2; halo degree <= 2; no cycle).
Tile of a knight edge = parallelogram with long diagonal e and short diagonal the unit grid edge at its midpoint
(audited proof, section 1). Quarter multiplicity m_t = number of selected tiles containing quarter t (exact,
centroid test). A quarter is bad if m_t != 1. U = quarters of unit squares [x,x+1]x[y,y+1] with 1 <= x,y and
x,y <= K-4 (away from the strips' outer column and from the free halo). Constraint: gamma_R charged for
R0..R1. Objective: number of bad quarters in U. The square identity forces >= 2 per charged path (in distinct
squares), which is the 1/2 price; a private price 2/3 needs >= 8/3 per path.
usage: w3_quarters.py K R0 R1 [TIME]
"""
import sys, time, json
from ortools.sat.python import cp_model
sys.path.insert(0, '..')
from w3_flux import gamma, coeffs
from w1_enum import find_cycle

K8 = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def E2(a, b): return (a, b) if a < b else (b, a)


def tile(e):
    (x0, y0), (x1, y1) = e
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    if abs(x1 - x0) == 2: s = ((mx, my - 0.5), (mx, my + 0.5))      # short diagonal: vertical unit edge
    else: s = ((mx - 0.5, my), (mx + 0.5, my))
    return [(x0, y0), s[0], (x1, y1), s[1]]


def inside(poly, p):
    # convex polygon, strict interior test (centroids are never on edges)
    sgn = 0
    for i in range(4):
        a, b = poly[i], poly[(i + 1) % 4]
        c = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
        if c == 0: return False
        if sgn == 0: sgn = 1 if c > 0 else -1
        elif (c > 0) != (sgn > 0): return False
    return True


def quarters(x, y):
    cx, cy = x + 0.5, y + 0.5
    return {'b': (cx, cy - 0.33), 'r': (cx + 0.33, cy), 't': (cx, cy + 0.33), 'l': (cx - 0.33, cy)}


def main():
    K, R0, R1 = map(int, sys.argv[1:4]); T = int(sys.argv[4]) if len(sys.argv) > 4 else 600
    box = {(x, y) for x in range(K) for y in range(K)}
    edges = sorted({E2(a, (a[0] + dx, a[1] + dy)) for a in box for dx, dy in K8
                    if a[0] + dx >= 0 and a[1] + dy >= 0 and a[0] + dx < K + 2 and a[1] + dy < K + 2})
    M = cp_model.CpModel(); v = {e: M.NewBoolVar('') for e in edges}
    inc = {}
    for e in edges:
        for p in e: inc.setdefault(p, []).append(v[e])
    for p, l in inc.items():
        M.Add(sum(l) == 2) if p in box else M.Add(sum(l) <= 2)
    for R in range(R0, R1 + 1):
        const, c = coeffs(gamma(R), edges)
        z = M.NewIntVar(-200, 200, ''); r = M.NewIntVar(1, 2, '')
        M.Add(const + sum(c[e] * v[e] for e in c) == 3 * z + r)
    tiles = {e: tile(e) for e in edges}
    bad = []
    for x in range(1, K - 3):
        for y in range(1, K - 3):
            for q, pt in quarters(x, y).items():
                cov = [v[e] for e in edges if inside(tiles[e], pt)]
                bq = M.NewBoolVar('')
                M.Add(sum(cov) == 1).OnlyEnforceIf(bq.Not())
                bad.append(bq)
    M.Minimize(sum(bad))
    t0 = time.time(); cuts = 0
    while True:
        s = cp_model.CpSolver(); s.parameters.num_workers = 2
        s.parameters.max_time_in_seconds = max(5, T - (time.time() - t0))
        st = s.Solve(M)
        E = [e for e in edges if s.Value(v[e])]
        cyc = find_cycle(E)
        if not cyc or time.time() - t0 > T: break
        M.AddBoolOr([v[E2(*tuple(sorted(e)))].Not() for e in cyc]); cuts += 1
    n = R1 - R0 + 1
    print(f'K={K} paths R={R0}..{R1} ({n}): {s.StatusName(st)} bad quarters in U = {s.ObjectiveValue()} '
          f'(bound {s.BestObjectiveBound()}), per path {s.ObjectiveValue() / n:.3f} (bound {s.BestObjectiveBound() / n:.3f}); '
          f'cycle cuts {cuts}{"; LAST HAS CYCLE" if cyc else ""}', flush=True)
    json.dump(E, open(f'w3q_K{K}_R{R0}_{R1}.json', 'w'))


if __name__ == '__main__':
    main()
