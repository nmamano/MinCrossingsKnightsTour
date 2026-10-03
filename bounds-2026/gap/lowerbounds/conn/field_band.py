#!/usr/bin/env python3
"""Field closure inside a band (gap/lowerbounds FINDINGS L2).

Tour T (saved), mirror-P run on its left side. Force the 11.3 field (phase s) on rows Y0..Y1, columns 0..3.
Free: all knight edges with both ends in the band B = columns 0..K-1, rows Y0-m..Y1+m. Fixed: T edges that
leave B. Degree 2 everywhere. Objective: crossing pairs involving a free edge (exact; fixed-fixed pairs are
constant). Lazy subtour cuts for a single cycle. Hint: T. Reports the new total crossing count, recounted.

usage: field_band.py TOUR Y0 Y1 s K m TIME [feas]
"""
import sys, time
from itertools import combinations
from ortools.sat.python import cp_model
from field_close import load, E2, cross, field_edges, tour_edges, components, count_crossings, residues, KM


PER = 90


def run(name, Y0, Y1, s, K, m, T, feas=False, force=True, log=True):
    n, g, d = load(name)
    E0 = tour_edges(g)
    ylo, yhi = max(0, Y0 - m), min(n - 1, Y1 + m)
    reg = {(x, y) for x in range(K) for y in range(ylo, yhi + 1)}
    free = sorted({E2(a, (a[0] + dx, a[1] + dy)) for a in reg for dx, dy in KM if (a[0] + dx, a[1] + dy) in reg})
    fixed = {e for e in E0 if not (e[0] in reg and e[1] in reg)}
    M = cp_model.CpModel()
    x = {e: M.NewBoolVar('') for e in free}
    fdeg = {}
    for a, b in fixed:
        fdeg[a] = fdeg.get(a, 0) + 1; fdeg[b] = fdeg.get(b, 0) + 1
    inc = {v: [] for v in reg}
    for e in free:
        inc[e[0]].append(x[e]); inc[e[1]].append(x[e])
    for v in reg:
        M.Add(sum(inc[v]) == 2 - fdeg.get(v, 0))
    FE = field_edges(Y0, Y1, s)
    if force:
        for e in FE:
            M.Add(x[e] == 1)
    for e in free:
        M.AddHint(x[e], e in E0)
    if not feas:
        near = [f for f in fixed if min(f[0][0], f[1][0]) <= K + 2 and ylo - 3 <= min(f[0][1], f[1][1]) <= yhi + 3]
        obj = []
        for e in free:
            c = sum(1 for f in near if cross(e, f))
            if c: obj.append(c * x[e])
        for e, f in combinations(free, 2):
            if abs(e[0][1] - f[0][1]) <= 4 and cross(e, f):
                z = M.NewBoolVar(''); M.Add(z >= x[e] + x[f] - 1); obj.append(z)
        M.Minimize(sum(obj))
    cuts = 0; t0 = time.time()
    while True:
        S = cp_model.CpSolver(); S.parameters.num_workers = 2
        S.parameters.max_time_in_seconds = max(10, min(PER, T - (time.time() - t0)))
        st = S.Solve(M)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return dict(status=S.StatusName(st), cuts=cuts, K=K, rows=Y1 - Y0 + 1)
        E = fixed | {e for e in free if S.Value(x[e])}
        comps = components(n, E)
        if len(comps) == 1:
            break
        for c in comps:
            cs = set(c)
            M.Add(sum(x[e] for e in free if (e[0] in cs) != (e[1] in cs)) >= 2)
        cuts += len(comps)
        if log: print(f'  round: {len(comps)} components, obj {S.ObjectiveValue() if not feas else "-"}, '
                      f'bound {S.BestObjectiveBound() if not feas else "-"}, {round(time.time()-t0)}s', flush=True)
        if time.time() - t0 > T:
            return dict(status='TIME_IN_CUTS', cuts=cuts, K=K, rows=Y1 - Y0 + 1)
    assert len(E) == n * n
    deg = {}
    for a, b in E:
        deg[a] = deg.get(a, 0) + 1; deg[b] = deg.get(b, 0) + 1
    assert all(v == 2 for v in deg.values()) and len(deg) == n * n
    X = count_crossings(E); X0 = count_crossings(E0)
    a = residues(n, E, range(Y0, Y1 + 1), 'top' if Y0 > n // 2 else 'bot')
    r = dict(status=S.StatusName(st), K=K, rows=Y1 - Y0 + 1, s=s, X=X, X0=X0, dX=X - X0,
             obj=S.ObjectiveValue() if not feas else None, bound=S.BestObjectiveBound() if not feas else None,
             cuts=cuts, sum_a=sum(a), changed=len(E ^ E0) // 2, secs=round(time.time() - t0))
    return r, E


if __name__ == '__main__':
    a = sys.argv[1:]
    res = run(a[0], int(a[1]), int(a[2]), int(a[3]), int(a[4]), int(a[5]), int(a[6]), len(a) > 7)
    print(res[0] if isinstance(res, tuple) else res, flush=True)
