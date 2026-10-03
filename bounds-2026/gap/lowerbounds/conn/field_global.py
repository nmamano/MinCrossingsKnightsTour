#!/usr/bin/env python3
"""Field closure through the folds (gap/lowerbounds FINDINGS L2).

Tour FOLD24_n166. Force the 11.3 field on the left side, rows Y0..Y1. Free region = left band (columns 0..K-1,
rows Y0-m..Y1+m) + a band of half-width w around the midline fold (row 83, x <= 90) + a band of half-width w
around the anti-diagonal fold (x+y = 166, y >= 78). All other tour edges stay fixed. Degree 2, single cycle
(lazy cuts), minimise crossings involving free edges. Hint = the original tour.

usage: field_global.py Y0 Y1 s K m w TIME [PER]
"""
import sys, time
from itertools import combinations
from ortools.sat.python import cp_model
from field_close import load, E2, cross, field_edges, tour_edges, components, count_crossings, residues, KM


def region(n, Y0, Y1, K, m, w):
    R = set()
    for x in range(n):
        for y in range(n):
            if x < K and Y0 - m <= y <= Y1 + m: R.add((x, y))
            if abs(y - 83) <= w and x <= 90: R.add((x, y))
            if abs(x + y - 166) <= w and y >= 78: R.add((x, y))
    return R


def main():
    Y0, Y1, s, K, m, w, T = map(int, sys.argv[1:8])
    PER = int(sys.argv[8]) if len(sys.argv) > 8 else 300
    global ONE
    ONE = len(sys.argv) > 9 and sys.argv[9] == 'one'
    n, g, d = load('FOLD24_n166')
    E0 = tour_edges(g)
    reg = region(n, Y0, Y1, K, m, w)
    free = sorted({E2(a, (a[0] + dx, a[1] + dy)) for a in reg for dx, dy in KM if (a[0] + dx, a[1] + dy) in reg})
    fixed = {e for e in E0 if not (e[0] in reg and e[1] in reg)}
    print('cells', len(reg), 'free edges', len(free), flush=True)
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
    for e in field_edges(Y0, Y1, s):
        M.Add(x[e] == 1)
    for e in free:
        M.AddHint(x[e], e in E0)
    by = {}
    for f in fixed: by.setdefault(f[0], []).append(f); by.setdefault(f[1], []).append(f)
    obj = []; t0 = time.time(); objT = [0]
    for e in free:
        cands = set()
        for p in e:
            for dx in range(-3, 4):
                for dy in range(-3, 4):
                    cands.update(by.get((p[0] + dx, p[1] + dy), ()))
        c = sum(1 for f in cands if cross(e, f))
        if c:
            obj.append(c * x[e])
            if e in E0: objT[0] += c
    fb = {}
    for e in free: fb.setdefault(e[0], []).append(e)
    nz = 0
    for e in free:
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                for f in fb.get((e[0][0] + dx, e[0][1] + dy), ()):
                    if e < f and cross(e, f):
                        z = M.NewBoolVar(''); M.Add(z >= x[e] + x[f] - 1); obj.append(z); nz += 1
                        objT[0] += (e in E0) and (f in E0)
    M.Minimize(sum(obj))
    print('objective of the original tour T:', objT[0], flush=True)
    print('pair vars', nz, 'built in', round(time.time() - t0), 's', flush=True)
    obj_T = None
    cuts = 0; best = None
    while time.time() - t0 < T:
        S = cp_model.CpSolver(); S.parameters.num_workers = 2
        S.parameters.max_time_in_seconds = max(10, min(PER, T - (time.time() - t0)))
        st = S.Solve(M)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print('status', S.StatusName(st), flush=True); break
        E = fixed | {e for e in free if S.Value(x[e])}
        comps = components(n, E)
        print(f'  round: {len(comps)} components, obj {S.ObjectiveValue()}, bound {S.BestObjectiveBound()}, '
              f'{round(time.time() - t0)}s', flush=True)
        import pickle
        pickle.dump(sorted(E), open(f'twofactor_{Y0}_{Y1}_{s}.pkl', 'wb'))
        if len(comps) == 1 or ONE:
            best = (S.ObjectiveValue(), S.BestObjectiveBound(), E, S.StatusName(st)); break
        for c in comps:
            cs = set(c)
            M.Add(sum(x[e] for e in free if (e[0] in cs) != (e[1] in cs)) >= 2)
        cuts += len(comps)
        M.ClearHints()
        for e in free:
            M.AddHint(x[e], e in E)
    if best:
        E = best[2]
        deg = {}
        for a, b in E:
            deg[a] = deg.get(a, 0) + 1; deg[b] = deg.get(b, 0) + 1
        assert all(v == 2 for v in deg.values()) and len(deg) == n * n and len(E) == n * n
        print('components', len(components(n, E)), flush=True)
        X = count_crossings(E); X0 = count_crossings(E0)
        a = residues(n, E, range(Y0, Y1 + 1), 'top')
        print(dict(status=best[3], rows=Y1 - Y0 + 1, X=X, X0=X0, dX=X - X0, obj=best[0], bound=best[1],
                   cuts=cuts, sum_a=sum(a), changed=len(E ^ E0) // 2), flush=True)
        import pickle
        pickle.dump(sorted(E), open(f'global_{Y0}_{Y1}_{s}.pkl', 'wb'))


if __name__ == '__main__':
    main()
