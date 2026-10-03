#!/usr/bin/env python3
"""W1: enumerate all central type maps of crossing-free windows (gap/lowerbounds FINDINGS W1).

Core k x k (degree exactly 2), halo of width 2 (degree <= 2), edges = knight moves with an end in the core,
no crossing between two edges that both touch the core, no cycle (lazy cuts). A central map gives, for each
cell of the central (k-2b) x (k-2b) block, its pair of edge directions. Enumerate all distinct central maps
with blocking clauses. Output: JSON list of maps (cell -> [dir index, dir index]).
usage: w1_enum.py k b OUT.json
"""
import sys, json, time
from itertools import combinations
from ortools.sat.python import cp_model
sys.path.insert(0, '..')
from check_frac_obstruction import crosses, E2

K8 = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def find_cycle(E):
    adj = {}
    for a, b in E: adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    seen = set()
    for s in adj:
        if s in seen: continue
        parent = {s: None}; stack = [s]; seen.add(s)
        while stack:
            u = stack.pop()
            for w in adj[u]:
                if w == parent[u]: continue
                if w in parent:
                    pa = [u]
                    while pa[-1] is not None: pa.append(parent[pa[-1]])
                    pb = [w]
                    while pb[-1] is not None: pb.append(parent[pb[-1]])
                    sa = set(pa); c = next(q for q in pb if q in sa)
                    path = pa[:pa.index(c) + 1] + pb[:pb.index(c)][::-1]
                    return [E2(path[i], path[(i + 1) % len(path)]) for i in range(len(path))]
                parent[w] = u; seen.add(w); stack.append(w)
    return None


def main():
    k, b, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    core = [(x, y) for x in range(k) for y in range(k)]
    cs = set(core)
    cen = [(x, y) for x in range(b, k - b) for y in range(b, k - b)]
    edges = sorted({E2(a, (a[0] + dx, a[1] + dy)) for a in core for dx, dy in K8})
    M = cp_model.CpModel()
    v = {e: M.NewBoolVar('') for e in edges}
    inc = {}
    for e in edges:
        for p in e: inc.setdefault(p, []).append(v[e])
    for p, lst in inc.items():
        M.Add(sum(lst) == 2) if p in cs else M.Add(sum(lst) <= 2)
    for e, f in combinations(edges, 2):
        if crosses(e, f): M.AddBoolOr([v[e].Not(), v[f].Not()])
    maps = []; cuts = 0; t0 = time.time()
    while True:
        s = cp_model.CpSolver(); s.parameters.num_workers = 2
        st = s.Solve(M)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): break
        E = [e for e in edges if s.Value(v[e])]
        cyc = find_cycle(E)
        if cyc:
            M.AddBoolOr([v[e].Not() for e in cyc]); cuts += 1; continue
        m = {}
        lits = []
        for c in cen:
            ds = [i for i, (dx, dy) in enumerate(K8) if s.Value(v[E2(c, (c[0] + dx, c[1] + dy))])]
            m[c] = ds
            lits += [v[E2(c, (c[0] + K8[i][0], c[1] + K8[i][1]))].Not() for i in ds]
        maps.append({f'{x},{y}': ds for (x, y), ds in m.items()})
        M.AddBoolOr(lits)
        if len(maps) % 200 == 0:
            print(len(maps), 'maps', cuts, 'cycle cuts', f'{time.time() - t0:.0f}s', flush=True)
    print(f'k={k} b={b}: {len(maps)} central maps, {cuts} cycle cuts, {time.time() - t0:.0f}s', flush=True)
    json.dump(maps, open(out, 'w'))


if __name__ == '__main__':
    main()
