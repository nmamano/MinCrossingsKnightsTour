#!/usr/bin/env python3
"""Does the joint model (Edge Searcher's spec) charge a given strip field? (gap/lowerbounds FINDINGS L5)

Fix the S edges (an end in column 0 or 1) of a periodic field on rows 0..L-1. Free edges: F23 (column 2 -
column 3) and J (column 3 - columns 4, 5), inside rows 0..L-1. Degrees: column 3 exactly 2 on rows
m..L-1-m (<= 2 near the ends), columns 2, 4, 5 <= 2. No cycle in S u F23 u J (lazy cuts). Minimise
wx = crossing pairs with at least one edge in F23 u J. Reports wx for two lengths; the slope is the rate.

usage: field_joint_cost.py FIELD L1 L2 [TIME]     FIELD = cap0 | combo8 | sat | cheap
"""
import sys
from itertools import combinations
from ortools.sat.python import cp_model
sys.path.insert(0, '..')
from check_frac_obstruction import crosses, E2


def S_field(name, L):
    E = set()
    for y in range(-4, L + 4):
        if name == 'cheap':                          # mirror P
            E.add(E2((2, y), (0, y + 1))); E.add(E2((3, y), (1, y + 1))); E.add(E2((1, y), (0, y + 2)))
            continue
        E.add(E2((1, y), (0, y + 2))); E.add(E2((2, y), (0, y + 1)))
        if name == 'cap0':
            if y % 6 in (0, 4, 5): E.add(E2((2, y), (1, y + 2)))
            if y % 6 in (2, 3, 4): E.add(E2((3, y), (1, y + 1)))
        elif name == 'combo8':
            if y % 8 != 2: E.add(E2((2, y), (1, y + 2)))
            else: E.add(E2((3, y + 1), (1, y + 2)))
        elif name == 'sat':
            E.add(E2((2, y), (1, y + 2)))
    return {e for e in E if all(0 <= p[1] < L for p in e)}


def solve(name, L, T, m=3):
    S = S_field(name, L)
    cells = [(x, y) for x in range(6) for y in range(L)]
    cand = set()
    for (x, y) in cells:
        for dx, dy in ((1, 2), (1, -2), (2, 1), (2, -1)):
            a, b = (x, y), (x + dx, y + dy)
            if not (0 <= b[1] < L and b[0] < 6): continue
            if (x == 2 and b[0] == 3) or (x == 3 and b[0] in (4, 5)):
                cand.add(E2(a, b))
    cand = sorted(cand)
    M = cp_model.CpModel()
    v = {e: M.NewBoolVar('') for e in cand}
    sdeg = {}
    for e in S:
        for p in e: sdeg[p] = sdeg.get(p, 0) + 1
    inc = {}
    for e in cand:
        for p in e: inc.setdefault(p, []).append(v[e])
    for (x, y) in cells:
        if x < 2: continue
        s = sum(inc.get((x, y), [])) + sdeg.get((x, y), 0)
        if x == 3 and m <= y < L - m: M.Add(s == 2)
        else: M.Add(s <= 2)
    obj = []
    for e in cand:
        c = sum(1 for f in S if crosses(e, f))
        if c: obj.append(c * v[e])
    for e, f in combinations(cand, 2):
        if crosses(e, f):
            z = M.NewBoolVar(''); M.Add(z >= v[e] + v[f] - 1); obj.append(z)
    M.Minimize(sum(obj))
    while True:
        sol = cp_model.CpSolver(); sol.parameters.num_workers = 2; sol.parameters.max_time_in_seconds = T
        st = sol.Solve(M)
        assert st in (cp_model.OPTIMAL, cp_model.FEASIBLE), sol.StatusName(st)
        chosen = [e for e in cand if sol.Value(v[e])]
        E = list(S) + chosen
        par = {}
        def find(c):
            while par.get(c, c) != c: c = par[c]
            return c
        adj = {}
        for a, b in E: adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
        # find a cycle by DFS
        cyc = None; seen = set()
        for s0 in adj:
            if s0 in seen: continue
            stack = [(s0, None)]; parent = {s0: None}; seen.add(s0)
            while stack and cyc is None:
                u, pu = stack.pop()
                for w_ in adj[u]:
                    if w_ == pu: continue
                    if w_ in parent:
                        # reconstruct
                        pa, pb = [u], [w_]
                        while pa[-1] is not None: pa.append(parent[pa[-1]])
                        while pb[-1] is not None: pb.append(parent[pb[-1]])
                        sa = set(pa); common = next(q for q in pb if q in sa)
                        path = pa[:pa.index(common) + 1] + pb[:pb.index(common)][::-1]
                        cyc = [E2(path[i], path[(i + 1) % len(path)]) for i in range(len(path))]
                        break
                    parent[w_] = u; seen.add(w_); stack.append((w_, u))
            if cyc: break
        if cyc is None:
            return sol.ObjectiveValue(), sol.BestObjectiveBound(), sol.StatusName(st), chosen
        fr = [v[e] for e in cyc if e in v]
        assert fr, 'cycle inside S'
        M.Add(sum(fr) <= len(fr) - 1)


if __name__ == '__main__':
    name, L1, L2 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    T = int(sys.argv[4]) if len(sys.argv) > 4 else 120
    r = []
    for L in (L1, L2):
        o, b, st, ch = solve(name, L, T)
        print(f'{name} L={L}: wx = {o} (bound {b}, {st})', flush=True); r.append((L, o, b))
    print(f'{name}: wx slope per row ~ {(r[1][1] - r[0][1]) / (L2 - L1):.4f} (lower-bound slope >= '
          f'{(r[1][2] - r[0][1]) / (L2 - L1):.4f})')
