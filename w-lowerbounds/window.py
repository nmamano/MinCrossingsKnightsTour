"""Window experiments: min crossings in a W x W window (all cells degree 2) under
conditions on the centre cell. Frame of width 2 around the window: degree <= 2.
Acyclicity by lazy cuts (re-solve). Crossings counted among chosen edges with >= 1 end in window."""
import sys, itertools
from ortools.sat.python import cp_model
sys.path.insert(0, '.')
from strip_dp import cross

MOVES = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def solve(W, centre_cond, threads=2, tlimit=120, extra=None):
    win = [(x, y) for x in range(W) for y in range(W)]
    allc = [(x, y) for x in range(-2, W + 2) for y in range(-2, W + 2)]
    ws = set(win)
    edges = {}
    for (x, y) in allc:
        for dx, dy in MOVES:
            u, v = (x, y), (x + dx, y + dy)
            if v not in set(allc) or not (u in ws or v in ws):
                continue
            key = tuple(sorted([u, v]))
            edges[key] = None
    E = list(edges)
    m = cp_model.CpModel()
    xv = {e: m.NewBoolVar('') for e in E}
    inc = {c: [] for c in allc}
    for e in E:
        inc[e[0]].append(e); inc[e[1]].append(e)
    for c in allc:
        if c in ws:
            m.Add(sum(xv[e] for e in inc[c]) == 2)
        else:
            m.Add(sum(xv[e] for e in inc[c]) <= 2)
    cr = []
    for e, f in itertools.combinations(E, 2):
        if cross((*e[0], *e[1]), (*f[0], *f[1])):
            z = m.NewBoolVar('')
            m.AddBoolAnd([xv[e], xv[f]]).OnlyEnforceIf(z)
            m.AddBoolOr([xv[e].Not(), xv[f].Not(), z])
            cr.append(z)
    centre_cond(m, xv, inc, (W // 2, W // 2))
    if extra:
        extra(m, xv, inc)
    m.Minimize(sum(cr))
    while True:
        s = cp_model.CpSolver()
        s.parameters.num_workers = threads
        s.parameters.max_time_in_seconds = tlimit
        st = s.Solve(m)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return None, s.StatusName(st), None
        chosen = [e for e in E if s.Value(xv[e])]
        import networkx as nx
        G = nx.Graph(); G.add_edges_from(chosen)
        cyc = nx.cycle_basis(G)
        if not cyc:
            return s.ObjectiveValue(), s.StatusName(st), (chosen, s.BestObjectiveBound())
        for c in cyc:
            ce = [tuple(sorted([c[i], c[(i + 1) % len(c)]])) for i in range(len(c))]
            m.Add(sum(xv[e] for e in ce) <= len(ce) - 1)


def turn_at(m, xv, inc, c):
    # centre cell's two edges are not opposite
    for e in inc[c]:
        for f in inc[c]:
            if e < f:
                d1 = (e[0][0] + e[1][0] - 2 * c[0], e[0][1] + e[1][1] - 2 * c[1])
                # e and f opposite iff other endpoints symmetric around c
                oe = e[1] if e[0] == c else e[0]
                of = f[1] if f[0] == c else f[0]
                if oe[0] + of[0] == 2 * c[0] and oe[1] + of[1] == 2 * c[1]:
                    m.AddBoolOr([xv[e].Not(), xv[f].Not()])


def draw(chosen, W):
    print('edges:', sorted(chosen))


if __name__ == '__main__':
    W = int(sys.argv[1])
    val, st, info = solve(W, turn_at)
    print('W', W, 'turn at centre: min crossings', val, st, 'bound', info[1] if info else None)
    if info:
        draw(info[0], W)
