"""Complete the 8-triangle fold field into a 2-factor with CP-SAT (free zone = boundary
strips of depth D + centre box), minimise crossings, report cycles and crossings."""
import sys, itertools, time
from collections import defaultdict, Counter
from ortools.sat.python import cp_model
import networkx as nx
sys.path.insert(0, '.')
from strip_dp import cross
from fold_board import field

MOVES = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def build(n, D=4, R=3, threads=2, tlimit=300, cuts=False, maxcut_rounds=50, verbose=True):
    v = field(n)
    on = lambda p: 0 <= p[0] < n and 0 <= p[1] < n
    h = n // 2
    def free(p):
        x, y = p
        return (min(x, y, n - 1 - x, n - 1 - y) < D) or (abs(x - h + 0.5) <= R and abs(y - h + 0.5) <= R)
    fe = set()
    for p, d in v.items():
        q = (p[0] + d[0], p[1] + d[1])
        if on(q):
            fe.add(tuple(sorted([p, q])))
    fixed = [e for e in fe if not free(e[0]) and not free(e[1])]
    # non-free cells must have degree 2 from field edges
    deg = Counter()
    for e in fe:
        deg[e[0]] += 1; deg[e[1]] += 1
    bad = [p for p in v if not free(p) and deg[p] != 2]
    assert not bad, bad[:10]
    cand = set()
    for p in v:
        if not free(p):
            continue
        for dx, dy in MOVES:
            q = (p[0] + dx, p[1] + dy)
            if not on(q):
                continue
            e = tuple(sorted([p, q]))
            if free(q) or e in fe:
                cand.add(e)
    cand = sorted(cand)
    m = cp_model.CpModel()
    xv = {e: m.NewBoolVar('') for e in cand}
    inc = defaultdict(list)
    for e in cand:
        inc[e[0]].append(e); inc[e[1]].append(e)
    for p in v:
        if free(p):
            m.Add(sum(xv[e] for e in inc[p]) == 2)
    for e in cand:   # field edges into non-free cells are forced
        if not (free(e[0]) and free(e[1])):
            m.Add(xv[e] == 1)
    # crossings: candidate-candidate, and candidate-fixed
    seg = lambda e: (*e[0], *e[1])
    # spatial hash
    grid = defaultdict(list)
    for e in cand:
        grid[(min(e[0][0], e[1][0]) // 3, min(e[0][1], e[1][1]) // 3)].append(e)
    def near(e):
        cx, cy = min(e[0][0], e[1][0]) // 3, min(e[0][1], e[1][1]) // 3
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                yield from grid.get((cx + a, cy + b), [])
    terms = []
    const = 0
    for e in cand:
        for f in near(e):
            if e < f and cross(seg(e), seg(f)):
                z = m.NewBoolVar('')
                m.AddBoolOr([xv[e].Not(), xv[f].Not(), z])
                terms.append(z)
    fgrid = defaultdict(list)
    for f in fixed:
        fgrid[(min(f[0][0], f[1][0]) // 3, min(f[0][1], f[1][1]) // 3)].append(f)
    for e in cand:
        cx, cy = min(e[0][0], e[1][0]) // 3, min(e[0][1], e[1][1]) // 3
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                for f in fgrid.get((cx + a, cy + b), []):
                    if cross(seg(e), seg(f)):
                        terms.append(xv[e])
    m.Minimize(sum(terms))
    rounds = 0
    while True:
        s = cp_model.CpSolver()
        s.parameters.num_workers = threads
        s.parameters.max_time_in_seconds = tlimit
        t0 = time.time()
        st = s.Solve(m)
        chosen = [e for e in cand if s.Value(xv[e])]
        alle = set(chosen) | set(fixed)
        G = nx.Graph(); G.add_edges_from(alle)
        comps = list(nx.connected_components(G))
        if verbose:
            print(f'round {rounds}: {s.StatusName(st)} obj {s.ObjectiveValue()} bound {s.BestObjectiveBound()} '
                  f'cycles {len(comps)} sizes {sorted(len(c) for c in comps)[:12]} ({time.time()-t0:.0f}s)', flush=True)
        if len(comps) == 1 or not cuts or rounds >= maxcut_rounds:
            return alle, comps, s.ObjectiveValue()
        # subtour cuts on cycles that live entirely in the free zone + crossing cut sets
        for c in comps:
            if len(c) == n * n:
                continue
            cut = [e for e in cand if (e[0] in c) != (e[1] in c)]
            if cut:
                m.Add(sum(xv[e] for e in cut) >= 2)
        rounds += 1


def total_crossings(E):
    E = list(E)
    grid = defaultdict(list)
    for e in E:
        grid[(min(e[0][0], e[1][0]) // 3, min(e[0][1], e[1][1]) // 3)].append(e)
    c = 0
    for e in E:
        cx, cy = min(e[0][0], e[1][0]) // 3, min(e[0][1], e[1][1]) // 3
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                for f in grid.get((cx + a, cy + b), []):
                    if e < f and cross((*e[0], *e[1]), (*f[0], *f[1])):
                        c += 1
    return c


if __name__ == '__main__':
    n = int(sys.argv[1]); D = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    E, comps, obj = build(n, D=D, cuts='cuts' in sys.argv)
    print('n', n, 'edges', len(E), 'total crossings', total_crossings(E), 'cycles', len(comps))
