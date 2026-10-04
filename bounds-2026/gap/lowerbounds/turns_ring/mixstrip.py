"""Side-strip test for turn-free interior fields that mix two line families by a residue rule.
A side strip (width 4, frame X inward / Y along) gets the forced interior edges of the field. The state is
(cut state, Y mod P). Reports, per side, the minimum cycle mean of the row cost (Karp); 0 means a zero-cost
periodic side exists. usage: mixstrip.py F1 F2 m R n   e.g. mixstrip.py A D 4 02 48"""
import sys
from itertools import combinations
sys.path.insert(0, '/home/nil/nil/knight-formation-research/gap/lowerbounds/turns_ring')
from strip import M, rcost
DIR = {'A': (2, -1), 'D': (2, 1), 'B': (1, 2), 'C': (1, -2)}
inv = lambda d, p: d[1] * p[0] - d[0] * p[1]


def field_rule(F1, F2, m, R):
    d1, d2 = DIR[F1], DIR[F2]
    assert inv(d1, d2) % m == 0, 'invariant of F1 must be constant mod m along F2 lines'
    return lambda p: d1 if inv(d1, p) % m in R else d2


def to_board(side, n):
    return {'left': lambda X, Y: (X, Y), 'right': lambda X, Y: (n - 1 - X, Y),
            'bottom': lambda X, Y: (Y, X), 'top': lambda X, Y: (Y, n - 1 - X)}[side]


def side_graph(rule, side, n, P):
    tb = to_board(side, n)
    def fam(X, Y):        # interior cell family as frame move pair
        bx, by = tb(X, Y); d = rule((bx, by))
        # transform board direction to frame direction
        e = [(X + 1, Y), (X, Y + 1)]
        ux = (tb(X + 1, Y)[0] - bx, tb(X + 1, Y)[1] - by); uy = (tb(X, Y + 1)[0] - bx, tb(X, Y + 1)[1] - by)
        # solve d = a*ux + b*uy (ux, uy are unit axis vectors)
        a = d[0] * ux[0] + d[1] * ux[1]; b = d[0] * uy[0] + d[1] * uy[1]
        return ((a, b), (-a, -b))
    Y0 = 10 * P          # work far from the board corners; frame rows Y0 + k
    def arcs_from(state, ph):
        pend = state
        inc = {}
        for (x0, y0, dx, dy) in pend:
            if y0 + dy == 0: inc.setdefault(x0 + dx, []).append((-dx, -dy))
        if any(len(v) > 2 for v in inc.values()): return
        Y = Y0 + ph
        opts = []
        for x in range(4):
            forced = list(inc.get(x, []))
            for d in M:
                X2, Y2 = x + d[0], Y + d[1]
                if X2 >= 4 and (-d[0], -d[1]) in fam(X2, Y2): forced.append(d)
            if len(forced) > 2: return
            free = [d for d in M if 0 <= x + d[0] < 4 and d[1] > 0 and d not in forced]
            opts.append([(tuple(forced + list(ex)), rcost(x, *(forced + list(ex)))) for ex in combinations(free, 2 - len(forced))])
        def rec(x, acc, c):
            if x == 4: yield acc, c; return
            for mv, cc in opts[x]: yield from rec(x + 1, acc + [(x, mv)], c + cc)
        keep = [e for e in pend if e[1] + e[3] > 0]
        for ch, c in rec(0, [], 0):
            new = [(x, 0, dx, dy) for x, mv in ch for dx, dy in mv if dy > 0 and x + dx < 4]
            load = {}
            for (x0, y0, dx, dy) in keep + new:
                k = (x0 + dx, y0 + dy); load[k] = load.get(k, 0) + 1
            if any(v > 2 for v in load.values()): continue
            yield frozenset((x0, y0 - 1, dx, dy) for (x0, y0, dx, dy) in keep + new), c
    start = (frozenset(), 0); ids = {start: 0}; st = [start]; arcs = []
    for s in st:
        best = {}
        for t, c in arcs_from(s[0], s[1]):
            key = (t, (s[1] + 1) % P)
            if key not in ids: ids[key] = len(st); st.append(key)
            v = ids[key]; best[v] = min(best.get(v, 99), c)
        arcs += [(ids[s], v, c) for v, c in best.items()]
    return st, arcs


def karp(N, arcs):
    """minimum cycle mean over the whole graph (all components)."""
    import numpy as np
    S = np.array([a[0] for a in arcs]); D = np.array([a[1] for a in arcs]); C = np.array([a[2] for a in arcs], dtype=float)
    INF = 1e18
    Dk = np.full((N + 1, N), INF); Dk[0, :] = 0
    for k in range(1, N + 1):
        nd = np.full(N, INF); np.minimum.at(nd, D, Dk[k - 1][S] + C); Dk[k] = nd
    best = INF
    ok = Dk[N] < INF / 2
    with np.errstate(invalid='ignore'):
        vals = np.max(np.where(Dk[:N] < INF / 2, (Dk[N][None, :] - Dk[:N]) / (N - np.arange(N))[:, None], -INF), axis=0)
    vals = vals[ok]
    return float(vals.min()) if len(vals) else None


if __name__ == '__main__':
    F1, F2, m, R, n = sys.argv[1], sys.argv[2], int(sys.argv[3]), {int(c) for c in sys.argv[4]}, int(sys.argv[5])
    rule = field_rule(F1, F2, m, R)
    out = {}
    for side in ('left', 'right', 'bottom', 'top'):
        st, arcs = side_graph(rule, side, n, 2 * m)
        import networkx as nx
        Z = nx.DiGraph(); Z.add_edges_from((u, v) for u, v, c in arcs if c == 0)
        try: cyc = len(nx.find_cycle(Z))
        except nx.NetworkXNoCycle: cyc = 0
        out[side] = (len(st), cyc)
    print(F1, F2, 'mod', m, 'R', sorted(R), 'n', n, {k: ('states', v[0], 'zero-cycle len', v[1]) for k, v in out.items()}, flush=True)
