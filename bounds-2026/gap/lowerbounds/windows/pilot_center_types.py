#!/usr/bin/env python3
"""Pilot (phase 1): which centre-cell types occur in a crossing-free k x k window?

Core = k x k cells, all degree exactly 2; halo = cells within distance 2 outside the core, degree <= 2;
edges = knight moves with at least one end in the core. No two edges that both touch the core may cross.
No cycle inside is NOT imposed (pilot). For each unordered pair of directions at the centre cell, report
FEASIBLE / INFEASIBLE.
usage: pilot_center_types.py k
"""
import sys
from itertools import combinations
from ortools.sat.python import cp_model
sys.path.insert(0, '..')
from check_frac_obstruction import crosses, E2

K8 = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def run(k):
    core = [(x, y) for x in range(k) for y in range(k)]
    cs = set(core)
    edges = sorted({E2(a, (a[0] + dx, a[1] + dy)) for a in core for dx, dy in K8})
    c = (k // 2, k // 2)
    res = {}
    for d1, d2 in combinations(range(8), 2):
        M = cp_model.CpModel()
        v = {e: M.NewBoolVar('') for e in edges}
        inc = {}
        for e in edges:
            for p in e: inc.setdefault(p, []).append(v[e])
        for p, lst in inc.items():
            M.Add(sum(lst) == 2) if p in cs else M.Add(sum(lst) <= 2)
        for e, f in combinations(edges, 2):
            if crosses(e, f): M.AddBoolOr([v[e].Not(), v[f].Not()])
        for i in range(8):
            e = E2(c, (c[0] + K8[i][0], c[1] + K8[i][1]))
            M.Add(v[e] == (1 if i in (d1, d2) else 0))
        s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = 60
        st = s.Solve(M)
        res[(K8[d1], K8[d2])] = s.StatusName(st)
    return res


if __name__ == '__main__':
    k = int(sys.argv[1])
    r = run(k)
    feas = [t for t, s in r.items() if s in ('OPTIMAL', 'FEASIBLE')]
    print(f'k={k}: {len(feas)} of 28 centre types feasible:')
    for t in feas:
        a, b = t
        kind = 'straight' if (a[0] == -b[0] and a[1] == -b[1]) else 'turn'
        print('  ', t, kind)
    print('undecided:', [t for t, s in r.items() if s not in ('OPTIMAL', 'FEASIBLE', 'INFEASIBLE')])
