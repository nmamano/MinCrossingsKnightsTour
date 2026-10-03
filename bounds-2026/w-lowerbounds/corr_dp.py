"""Exact transfer-matrix model for colour-flux corridors (KT Lower Bounds, 2026-10-02).

Coordinates: transverse u, along-route y. Planar cell P(u, y) = (u + a*y + off, y).
Band cells u = 0..W-1: degree exactly 2, any knight move (both ends on board).
Ghost cells u in [-gl, 0) and [W, W+2): keep their base edges; an edge band-ghost is allowed only
if it is a base edge, and then it is forced. Ghost-ghost edges are not represented (they are base
edges, constant). No cycle among represented edges.
Weight: proper crossings among represented edges.
Colour current through the cut between rows Y-1 and Y: sum over pending edges of chi(lower end).
States at row boundaries with even Y (and a=0) or any Y (a=1) are restricted to current = target.
Min mean cycle (Howard) = min crossings per row for that current.
"""
import sys
from collections import deque
from itertools import combinations
sys.path.insert(0, '.')
from strip_dp import cross
from mmc import prune, howard

KM = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def make_route(name, W):
    """returns a, off, gl, on(planar), base_nbrs(planar)->set of planar nbrs"""
    if name == 'edge':
        a, off, gl = 0, 0, 0
        on = lambda c: c[0] >= 0
        v = lambda c: (2, 1)
        extra = lambda c: [(1, c[1] + 2)] if c[0] == 0 else ([(0, c[1] - 2)] if c[0] == 1 else [])
    elif name == 'interior':
        a, off, gl = 0, 0, 2
        on = lambda c: True
        v = lambda c: (2, 1)
        extra = lambda c: []
    elif name == 'diag':       # fold x - y = 0: (2,1) where x-y <= -1, (-1,-2) where x-y >= 0
        a, off, gl = 1, -(W // 2), 3
        on = lambda c: True
        v = lambda c: (2, 1) if c[0] - c[1] <= -1 else (-1, -2)
        extra = lambda c: []
    elif name == 'diagint':    # uniform (2,1) lines, corridor along (1,1)
        a, off, gl = 1, -(W // 2), 3
        on = lambda c: True
        v = lambda c: (2, 1)
        extra = lambda c: []
    elif name == 'mid':        # transposed midline fold: (1,2) where x <= -1, (1,-2) where x >= 0
        a, off, gl = 0, -(W // 2), 2
        on = lambda c: True
        v = lambda c: (1, 2) if c[0] <= -1 else (1, -2)
        extra = lambda c: []
    else:
        raise ValueError(name)
    def nbrs(c):
        out = set()
        d = v(c); q = (c[0] + d[0], c[1] + d[1])
        if on(q): out.add(q)
        for dx, dy in KM:
            q = (c[0] - dx, c[1] - dy)
            if on(q) and v(q) == (dx, dy):
                out.add(q)
        for q in extra(c):
            out.add(q)
        return out
    return a, off, gl, on, nbrs


def build(name, W, target=None, max_states=3_000_000):
    a, off, gl, on, nbrs = make_route(name, W)
    gr = 3 if a == 1 else 2
    U = list(range(-gl, W + gr))
    P = lambda u, y: (u + a * y + off, y)
    chi = lambda c: 1 if (c[0] + c[1]) % 2 == 0 else -1
    isband = lambda u: 0 <= u < W
    # move vectors in (u, y) coords
    def to_uv(d):
        return (d[0] - a * d[1], d[1])
    UPM = [(dx, dy) for dx, dy in KM if dy > 0]
    # state: (u_phase, ypar, edges) ; edge = (lu, ly, hu, hy, comp) with y relative to current row
    start = (U[0], 0, (), 0)
    index = {start: 0}; states = [start]; adj = []
    q = deque([0])
    while q:
        sid = q.popleft()
        u, ypar, edges, warm = states[sid]
        y = 0
        c = P(u, ypar)          # absolute planar position uses ypar for colour (a=0) only
        out = {}
        incoming = [e for e in edges if e[2] == u and e[3] == 0]
        rest = [e for e in edges if not (e[2] == u and e[3] == 0)]
        cplan = P(u, 0)
        valid = on(cplan) if a == 0 else True
        if not valid:
            # off-board cell (edge route, u<0 never happens since gl=0)
            options = [()] if not incoming else []
        else:
            bn = nbrs(cplan)
            cands = []
            for dx, dy in UPM:
                du, dv = to_uv((dx, dy))
                tu = u + du
                if tu not in U:
                    continue
                tgt = (cplan[0] + dx, cplan[1] + dy)
                if not on(tgt):
                    continue
                if isband(u) and isband(tu):
                    cands.append(((dx, dy), tu, dy, False))
                elif isband(u) or isband(tu):
                    if tgt in bn:
                        cands.append(((dx, dy), tu, dy, True))
            forced = [cd for cd in cands if cd[3]]
            free = [cd for cd in cands if not cd[3]]
            if isband(u):
                r = 2 - len(incoming) - len(forced)
                if warm >= 3:
                    options = [tuple(forced) + ch for ch in combinations(free, r)] if r >= 0 else []
                else:
                    options = [tuple(forced) + ch for rr in range(0, max(r, 0) + 1) for ch in combinations(free, rr)]
                # forced down-edges must be present among incoming: check
                need_down = [qq for qq in bn if qq[1] < cplan[1] and not isband_q(qq, a, off, W)]
            else:
                # ghost: incoming from band must be exactly its base down-edges to band
                options = [tuple(forced)]
        for ch in options:
            # degree / forced-down checks
            if valid and isband(u) and warm >= 3:
                down_ok = True
                for qq in nbrs(cplan):
                    if qq[1] < cplan[1] and not isband_q(qq, a, off, W):
                        # forced edge from a ghost below must be incoming
                        qu = qq[0] - a * qq[1] - off
                        if qu in U and not any(e[0] == qu and e[1] == qq[1] - cplan[1] for e in incoming):
                            down_ok = False
                if not down_ok:
                    continue
            if valid and not isband(u) and warm >= 3:
                # ghost incoming edges must all be base edges (they are, by construction) and the
                # count of band-ghost base edges below must match incoming
                need = sum(1 for qq in nbrs(cplan) if qq[1] < cplan[1] and isband_q(qq, a, off, W))
                if need != len(incoming):
                    continue
            tdeg = {}
            for e in rest:
                tdeg[(e[2], e[3])] = tdeg.get((e[2], e[3]), 0) + 1
            ok = True
            for (d, tu, dy, fz) in ch:
                key = (tu, dy); tdeg[key] = tdeg.get(key, 0) + 1
                if tdeg[key] > 2: ok = False
            if not ok:
                continue
            comps_in = [e[4] for e in incoming]
            if len(comps_in) == 2 and comps_in[0] == comps_in[1]:
                continue
            newe = [(u, 0, tu, dy) for (d, tu, dy, fz) in ch]
            plan = lambda e: (*P(e[0], e[1]), *P(e[2], e[3]))
            w = 0
            for i, f in enumerate(newe):
                for e in rest:
                    if cross(plan(e), plan(f)): w += 1
                for g in newe[:i]:
                    if cross(plan(g), plan(f)): w += 1
            if comps_in:
                label = comps_in[0]; merge = comps_in[1] if len(comps_in) == 2 else None
            else:
                label = 'new'; merge = None
            ne = []
            for e in rest:
                cc = label if (merge is not None and e[4] == merge) else e[4]
                ne.append((e[0], e[1], e[2], e[3], cc))
            for f in newe:
                ne.append((*f, label))
            ui = U.index(u)
            if ui + 1 < len(U):
                nu, shift, nypar = U[ui + 1], 0, ypar
            else:
                nu, shift, nypar = U[0], 1, (ypar + 1) % 2
            ne = [(p0, p1 - shift, p2, p3 - shift, cc) for (p0, p1, p2, p3, cc) in ne]
            ne.sort(key=lambda t: t[:4])
            rl = {}; canon = []
            for t in ne:
                if t[4] not in rl: rl[t[4]] = len(rl)
                canon.append((*t[:4], rl[t[4]]))
            if a == 1:
                nypar = 0
            ns = (nu, nypar, tuple(canon), min(warm + shift, 3))
            if shift == 1 and target is not None and nypar == 0 and warm + shift >= 3:
                # current through the cut below the new row: pending edges, lower end colour
                cur = 0
                for (lu, ly, hu, hy, cc) in canon:
                    lp = P(lu, ly)
                    col = (lp[0] + lp[1] + (0 if a == 1 else 0)) % 2
                    # absolute colour: row index parity is nypar(=0) + ly
                    cur += 1 if col == 0 else -1
                if cur != target:
                    continue
            if ns not in index:
                index[ns] = len(states); states.append(ns); q.append(index[ns])
                if len(states) > max_states:
                    raise RuntimeError('too many states')
            t = index[ns]
            if t not in out or out[t] > w:
                out[t] = w
        while len(adj) <= sid:
            adj.append(None)
        adj[sid] = list(out.items())
    while len(adj) < len(states):
        adj.append([])
    return states, adj, len(U)


def isband_q(qq, a, off, W):
    u = qq[0] - a * qq[1] - off
    return 0 <= u < W


def rate(name, W, target):
    states, adj, L = build(name, W, target)
    alive = prune(adj)
    if not any(alive):
        return None, len(states)
    mu, pol, eta = howard(adj, alive)
    return mu * L, len(states)


if __name__ == '__main__':
    name, W = sys.argv[1], int(sys.argv[2])
    targets = [int(t) for t in sys.argv[3:]]
    # first: unrestricted, to find the base current values that occur on optimal cycles
    for t in targets:
        r, ns = rate(name, W, t)
        print(f'{name} W={W} current(even rows)={t}: min crossings/row {r}  states {ns}', flush=True)
