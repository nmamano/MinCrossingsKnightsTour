#!/usr/bin/env python3
"""Does the 11.3 blocking field survive in a single closed tour? (gap/lowerbounds FINDINGS L2)

Start from a saved closed tour with a long mirror-P run on its left side. Re-solve a region
(columns 0..K-1, rows Y0-m..Y1+m) with CP-SAT: all tour edges that leave the region stay fixed, every region
cell has degree 2, and the objective is the exact number of crossing pairs that involve a region edge.
Single cycle: lazy subtour cuts x(delta(S)) >= 2 for each component S of the solution.
Mode 'base': no extra constraint. Mode 'field': the blocking field (phase s) is forced on rows Y0..Y1.
The output tour is re-validated and its crossings recounted from scratch (kt/core.py).

usage: field_close.py TOUR Y0 Y1 s [K m TIME]
"""
import sys
from itertools import combinations
from pathlib import Path
from ortools.sat.python import cp_model
from tourio import load, ROOT
sys.path.insert(0, str(ROOT / 'kt'))
sys.path.insert(0, str(ROOT / 'gap/lowerbounds'))
from core import seg_cross
from check_frac_obstruction import LIST, EXC

KM = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def E2(a, b):
    return (a, b) if a < b else (b, a)


def cross(e, f):
    if set(e) & set(f): return False
    return seg_cross(e[0], e[1], f[0], f[1])


def field_edges(Y0, Y1, s):
    F = set()
    for y in range(Y0 - 4, Y1 + 4):
        F.add(E2((2, y), (0, y + 1))); F.add(E2((3, y), (1, y + 1)))
        if (y - s) % 4 != 3: F.add(E2((1, y), (0, y + 2)))
        if (y - s) % 4 == 1: F.add(E2((0, y), (1, y + 2)))
    return {e for e in F if all(Y0 <= p[1] <= Y1 for p in e)}


def tour_edges(g):
    return {E2(a, b) for a in g for b in g[a]}


def components(n, E):
    adj = {}
    for a, b in E:
        adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    seen = set(); comps = []
    for v in adj:
        if v in seen: continue
        st = [v]; seen.add(v); c = []
        while st:
            u = st.pop(); c.append(u)
            for w in adj[u]:
                if w not in seen: seen.add(w); st.append(w)
        comps.append(c)
    return comps


def count_crossings(E):
    by = {}
    for e in E: by.setdefault(e[0], []).append(e)
    c = 0
    for e in E:
        (x, y) = e[0]
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                for f in by.get((x + dx, y + dy), ()):
                    if e < f and cross(e, f): c += 1
    return c


def residues(n, E, rows, corner):
    """Penalty a per row with the up test in the local frame of the bottom-left ('bot') or top-left corner."""
    out = []
    for y in rows:
        if corner == 'bot':
            loc = lambda p: (p[0], p[1]); R = y
        else:
            loc = lambda p: (p[0], n - 1 - p[1]); R = n - 1 - y
        sel = set()
        for e in E:
            a, b = loc(e[0]), loc(e[1])
            if a[0] <= 2 and b[0] <= 2 and min(a[1], b[1]) <= R <= max(a[1], b[1]):
                sel.add(E2((a[0], a[1] - R), (b[0], b[1] - R)))
        Fv = sum(c for (a, b), c in LIST if E2(a, b) in sel) % 3
        exc = all(E2(a, b) in sel for a, b in EXC)
        c = 1 if R % 2 == 0 else -1
        h = ((1 + c) // 2 + c * (Fv + 2)) % 3
        out.append(1 if exc else {0: 0.5, 1: 1, 2: 0}[h])
    return out


def solve(name, Y0, Y1, s, K=6, m=8, T=600, mode='field'):
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
    if mode == 'field':
        for e in field_edges(Y0, Y1, s):
            assert e in x, e
            M.Add(x[e] == 1)
    near = [f for f in fixed if min(abs(f[0][0] - 0), abs(f[1][0] - 0)) <= K + 2
            and ylo - 3 <= min(f[0][1], f[1][1]) <= yhi + 3]
    obj = []
    for e in free:
        c = sum(1 for f in near if cross(e, f))
        if c: obj.append(c * x[e])
    for e, f in combinations(free, 2):
        if abs(e[0][1] - f[0][1]) <= 4 and cross(e, f):
            z = M.NewBoolVar(''); M.Add(z >= x[e] + x[f] - 1); obj.append(z)
    M.Minimize(sum(obj))
    cuts = 0
    while True:
        S = cp_model.CpSolver(); S.parameters.num_workers = 2; S.parameters.max_time_in_seconds = T
        st = S.Solve(M)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return dict(status=S.StatusName(st), cuts=cuts)
        E = fixed | {e for e in free if S.Value(x[e])}
        comps = components(n, E)
        if len(comps) == 1:
            break
        for c in comps:
            cs = set(c)
            M.Add(sum(x[e] for e in free if (e[0] in cs) != (e[1] in cs)) >= 2)
        cuts += len(comps)
    deg = {}
    for a, b in E:
        deg[a] = deg.get(a, 0) + 1; deg[b] = deg.get(b, 0) + 1
    assert all(deg.get((i, j), 0) == 2 for i in range(n) for j in range(n)) and len(E) == n * n
    for a, b in E:
        assert sorted((abs(a[0] - b[0]), abs(a[1] - b[1]))) == [1, 2]
    X = count_crossings(E)
    corner = 'top' if Y0 > n // 2 else 'bot'
    a = residues(n, E, range(Y0, Y1 + 1), corner)
    return dict(status=S.StatusName(st), bound=S.BestObjectiveBound(), obj=S.ObjectiveValue(), cuts=cuts,
                X=X, X0=count_crossings(E0), sum_a=sum(a), rows=Y1 - Y0 + 1, E=E)


if __name__ == '__main__':
    a = sys.argv[1:]
    K, m, T = (int(a[4]), int(a[5]), int(a[6])) if len(a) > 4 else (6, 8, 600)
    for mode in ('base', 'field'):
        r = solve(a[0], int(a[1]), int(a[2]), int(a[3]), K, m, T, mode)
        r.pop('E', None)
        print(mode, r, flush=True)
