"""8-triangle fold field + deterministic edge U-turns (pattern P, rotated/mirrored),
then CP-SAT repairs small windows around cells with wrong degree. Reports cycles/crossings."""
import sys, time
from collections import defaultdict, Counter
from ortools.sat.python import cp_model
import networkx as nx
sys.path.insert(0, '.')
from strip_dp import cross
from fold_board import field
from fold_complete import total_crossings

MOVES = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def base(n, **kw):
    v = field(n, **kw)
    on = lambda p: 0 <= p[0] < n and 0 <= p[1] < n
    E = set()
    for p, d in v.items():
        q = (p[0] + d[0], p[1] + d[1])
        if on(q):
            E.add(tuple(sorted([p, q])))
    deg = Counter()
    for e in E:
        deg[e[0]] += 1; deg[e[1]] += 1
    # U-turns: pair line ends. For a line end p (deg 1) at an edge, the U-turn partner is the
    # other deg-1 cell q such that p-q is a knight move and the move is "pattern P":
    # left edge, family (2,+-1): (0,y)-(1,y+-2) where the sign matches the family slope.
    h = n // 2
    def rot(p): return (n - 1 - p[1], p[0])
    for x0, y0 in [(0, y) for y in range(n)]:
        for r in range(4):
            pass
    # do it generically: for each deg-1 cell p in column 0 (and rotations), with field family
    # direction d = v[p] (or the in-direction), pick partner p + (1, 2*sign)
    for r in range(4):
        def R(p, k=r):
            for _ in range(k):
                p = rot(p)
            return p
        for y in range(n):
            p = R((0, y))
            if deg[p] != 1:
                continue
            # family slope in the un-rotated frame: look at the line edge of (0,y)
            nb = [e[0] if e[1] == p else e[1] for e in E if p in e][0]
            # un-rotate neighbour
            # find dx,dy in base frame: compare with R of candidates
            for dy in (1, -1):
                if R((2, y + dy)) == nb:
                    q = R((1, y + 2 * dy))
                    if on(q) and deg[q] == 1:
                        e = tuple(sorted([p, q]))
                        if e not in E:
                            E.add(e); deg[p] += 1; deg[q] += 1
    return E, deg


def repair(n, E, rad=3, threads=2, tlimit=120, cuts=True):
    on = lambda p: 0 <= p[0] < n and 0 <= p[1] < n
    deg = Counter()
    for e in E:
        deg[e[0]] += 1; deg[e[1]] += 1
    cells = [(x, y) for x in range(n) for y in range(n)]
    badc = [p for p in cells if deg[p] != 2]
    free = set()
    for (x, y) in badc:
        for a in range(-rad, rad + 1):
            for b in range(-rad, rad + 1):
                if on((x + a, y + b)):
                    free.add((x + a, y + b))
    fixed = [e for e in E if e[0] not in free and e[1] not in free]
    cand = set()
    for p in free:
        for dx, dy in MOVES:
            q = (p[0] + dx, p[1] + dy)
            if on(q):
                e = tuple(sorted([p, q]))
                if q in free or e in E:
                    cand.add(e)
    cand = sorted(cand)
    m = cp_model.CpModel()
    xv = {e: m.NewBoolVar('') for e in cand}
    inc = defaultdict(list)
    for e in cand:
        inc[e[0]].append(e); inc[e[1]].append(e)
    for p in free:
        m.Add(sum(xv[e] for e in inc[p]) == 2)
    for e in cand:
        if not (e[0] in free and e[1] in free):
            m.Add(xv[e] == 1)
    seg = lambda e: (*e[0], *e[1])
    terms = []
    for i, e in enumerate(cand):
        for f in cand[i + 1:]:
            if abs(e[0][0] - f[0][0]) <= 4 and abs(e[0][1] - f[0][1]) <= 4 and cross(seg(e), seg(f)):
                z = m.NewBoolVar('')
                m.AddBoolOr([xv[e].Not(), xv[f].Not(), z])
                terms.append(z)
        for f in fixed:
            if abs(e[0][0] - f[0][0]) <= 4 and abs(e[0][1] - f[0][1]) <= 4 and cross(seg(e), seg(f)):
                terms.append(xv[e])
    m.Minimize(sum(terms))
    print(f'free cells {len(free)} cand edges {len(cand)} crossing terms {len(terms)}', flush=True)
    rounds = 0
    while True:
        s = cp_model.CpSolver()
        s.parameters.num_workers = threads
        s.parameters.max_time_in_seconds = tlimit
        st = s.Solve(m)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print('repair infeasible', s.StatusName(st)); return None, None
        chosen = [e for e in cand if s.Value(xv[e])]
        alle = set(chosen) | set(fixed)
        G = nx.Graph(); G.add_edges_from(alle)
        comps = list(nx.connected_components(G))
        print(f'round {rounds}: {s.StatusName(st)} obj {s.ObjectiveValue()} cycles {len(comps)} '
              f'sizes {sorted(len(c) for c in comps)[:20]}', flush=True)
        # cuts only for cycles fully inside the free zone
        added = 0
        for c in comps:
            if c <= free:
                cut = [e for e in cand if (e[0] in c) != (e[1] in c)]
                m.Add(sum(xv[e] for e in cut) >= 2); added += 1
        if not added or not cuts:
            return alle, comps
        rounds += 1


if __name__ == '__main__':
    n = int(sys.argv[1])
    E, deg = base(n)
    bad = sorted(p for p in [(x, y) for x in range(n) for y in range(n)] if deg[p] != 2)
    print('n', n, 'cells with deg != 2 after U-turns:', len(bad), bad[:40])
    E2, comps = repair(n, E)
    if E2:
        print('n', n, 'total crossings', total_crossings(E2), 'per n %.3f' % (total_crossings(E2) / n),
              'cycles', len(comps))
