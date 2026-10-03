#!/usr/bin/env python3
"""W3a: corner-box red-team window for the private flux price (gap/lowerbounds FINDINGS W3).

Board corner at (0,0). Box cells 0 <= x,y < K have degree exactly 2; halo cells (x or y in [K, K+1], both >= 0)
degree <= 2; edges = knight moves with an end in the box. No cycle (lazy cuts). For every R in [R0, R1]
(R1 <= K-3) the corner path gamma_R must be charged: omega(gamma_R) != 0 mod 3 (exact linear flux, w3_flux).
Objective: crossing pairs (both edges touch the box) that are NOT in S* (S*: both edges have an endpoint at
x <= 1, or both at y <= 1). This is a relaxation of every closed tour, so the optimum is a lower bound on the
crossings outside S* in the box of any tour whose paths R0..R1 are all charged.
usage: w3_corner.py K R0 R1 [TIME] [mode]     mode = outS (default) | all (count all pairs) | free (no charge, outside S*) | freeall (no charge, all pairs)
"""
import sys, time
from itertools import combinations
from ortools.sat.python import cp_model
sys.path.insert(0, '..')
from check_frac_obstruction import crosses
from w3_flux import gamma, coeffs
from w1_enum import find_cycle

K8 = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def E2(a, b): return (a, b) if a < b else (b, a)


def build(K, R0, R1, mode):
    box = {(x, y) for x in range(K) for y in range(K)}
    edges = sorted({E2(a, (a[0] + dx, a[1] + dy)) for a in box for dx, dy in K8
                    if a[0] + dx >= 0 and a[1] + dy >= 0 and a[0] + dx < K + 2 and a[1] + dy < K + 2})
    M = cp_model.CpModel()
    v = {e: M.NewBoolVar('') for e in edges}
    inc = {}
    for e in edges:
        for p in e: inc.setdefault(p, []).append(v[e])
    for p, l in inc.items():
        M.Add(sum(l) == 2) if p in box else M.Add(sum(l) <= 2)
    if mode in ('outS', 'all'):
        for R in range(R0, R1 + 1):
            const, c = coeffs(gamma(R), edges)
            for e in c:
                assert all(p in box for p in e) or True
            z = M.NewIntVar(-200, 200, ''); r = M.NewIntVar(1, 2, '')
            M.Add(const + sum(c[e] * v[e] for e in c) == 3 * z + r)
    def inS(e, f):
        return (min(e[0][0], e[1][0]) <= 1 and min(f[0][0], f[1][0]) <= 1) or \
               (min(e[0][1], e[1][1]) <= 1 and min(f[0][1], f[1][1]) <= 1)
    obj = []; pairs = []
    for e, f in combinations(edges, 2):
        if crosses(e, f) and (mode in ('all', 'freeall') or not inS(e, f)):
            zz = M.NewBoolVar(''); M.Add(zz >= v[e] + v[f] - 1); obj.append(zz); pairs.append((e, f))
    M.Minimize(sum(obj))
    return M, v, edges, pairs


def solve(K, R0, R1, T, mode):
    M, v, edges, pairs = build(K, R0, R1, mode)
    t0 = time.time(); cuts = 0
    while True:
        s = cp_model.CpSolver(); s.parameters.num_workers = 2
        s.parameters.max_time_in_seconds = max(5, T - (time.time() - t0))
        st = s.Solve(M)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return s.StatusName(st), None, None, cuts, None
        E = [e for e in edges if s.Value(v[e])]
        cyc = find_cycle(E)
        if not cyc or time.time() - t0 > T:
            return s.StatusName(st), s.ObjectiveValue(), s.BestObjectiveBound(), cuts, (E, cyc)
        M.AddBoolOr([v[E2(*tuple(sorted(e)))].Not() for e in cyc]); cuts += 1


if __name__ == '__main__':
    K, R0, R1 = map(int, sys.argv[1:4])
    T = int(sys.argv[4]) if len(sys.argv) > 4 else 600
    mode = sys.argv[5] if len(sys.argv) > 5 else 'outS'
    st, ob, bd, cuts, sol = solve(K, R0, R1, T, mode)
    print(f'K={K} R={R0}..{R1} ({R1 - R0 + 1} paths) mode={mode}: {st} obj={ob} bound={bd} cycle cuts={cuts}'
          + ('' if sol is None or not sol[1] else ' (LAST SOLUTION STILL HAS A CYCLE)'), flush=True)
    if sol:
        import json
        json.dump(sol[0], open(f'w3_corner_K{K}_R{R0}_{R1}_{mode}.json', 'w'))
