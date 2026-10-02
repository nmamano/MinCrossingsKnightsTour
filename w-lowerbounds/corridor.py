"""Periodic colour-flux corridor model (KT Lower Bounds, 2026-10-02).

A route with translation T (one period). Cells in a band (invariant under T) are free: degree
exactly 2, any knight move. Cells outside the band keep their base edges (field lines, edge U-turns).
An edge between a band cell and an outside cell is allowed only if it is a base edge (then forced).
Objective: crossings per period among edges that touch the band (variable-variable and
variable-fixed), counted in the unrolled plane. Constraint: colour current through the transverse
cut lambda = -1/2 equals base + k, where current = sum over edges crossing the cut of chi(end on the
negative side), chi(x,y) = +1 if x+y even else -1 (lambda = y, or x for horizontal routes).

usage: corridor.py ROUTE p w k1 [k2 ...]
ROUTE: edge | diag | mid | interior
"""
import sys, itertools, math
from collections import defaultdict
from ortools.sat.python import cp_model
sys.path.insert(0, '.')
from strip_dp import cross

MOVES = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
chi = lambda c: 1 if (c[0] + c[1]) % 2 == 0 else -1


def route(name, p, w):
    if name == 'edge':
        T = (0, p); lam = lambda c: c[1]
        on = lambda c: c[0] >= 0
        inband = lambda c: 0 <= c[0] < w
        trans = lambda c: c[0]                 # transverse coordinate (for neighbourhoods)
        def base_edges_at(c):
            out = [((c), (c[0] + 2, c[1] + 1))]
            if c[0] == 0:
                out.append((c, (1, c[1] + 2)))
            return out
    elif name == 'interior':
        T = (0, p); lam = lambda c: c[1]
        on = lambda c: True
        inband = lambda c: 0 <= c[0] < w
        trans = lambda c: c[0]
        def base_edges_at(c):
            return [(c, (c[0] + 2, c[1] + 1))]
    elif name == 'diag':
        T = (p, p); lam = lambda c: c[1]
        on = lambda c: True
        inband = lambda c: -w <= c[0] - c[1] <= w - 1
        trans = lambda c: c[0] - c[1]
        def base_edges_at(c):
            d = (2, 1) if c[0] - c[1] <= -1 else (-1, -2)
            return [(c, (c[0] + d[0], c[1] + d[1]))]
    elif name == 'mid':
        T = (p, 0); lam = lambda c: c[0]
        on = lambda c: True
        inband = lambda c: -w <= c[1] <= w - 1
        trans = lambda c: c[1]
        def base_edges_at(c):
            d = (2, 1) if c[1] <= -1 else (-2, 1)
            return [(c, (c[0] + d[0], c[1] + d[1]))]
    else:
        raise ValueError(name)
    return T, lam, on, inband, trans, base_edges_at


def build(name, p, w):
    T, lam, on, inband, trans, base_at = route(name, p, w)
    assert (T[0] + T[1]) % 2 == 0
    def canon(c):
        k = math.floor(lam(c) / p)
        return (c[0] - k * T[0], c[1] - k * T[1]), k
    def norm_edge(a, b):
        """canonical form of the T-orbit of undirected edge {a,b}"""
        ra, ka = canon(a); bb = (b[0] - ka * T[0], b[1] - ka * T[1])
        rb, kb = canon(b); aa = (a[0] - kb * T[0], a[1] - kb * T[1])
        return min((ra, bb), (rb, aa))
    # base edges in a large window (orbit-normalised)
    R = 3 * p + 12
    tr = [t for t in range(-w - 8, w + 8)]
    base = set()
    # enumerate cells near the band in one period: lam in [0,p), trans within range
    cells = []
    for x in range(-R, R):
        for y in range(-R, R):
            c = (x, y)
            if not on(c) or not (0 <= lam(c) < p):
                continue
            if -w - 8 <= trans(c) < w + 8 + (0 if name in ('diag', 'mid') else 0):
                cells.append(c)
    for c in cells:
        for (a, b) in base_at(c):
            if on(b):
                base.add(norm_edge(a, b))
    # the base edges are generated from out-edges; an edge whose tail is outside the window
    # range but head inside would be missed, so also generate from cells one period around
    band = [c for c in cells if inband(c)]
    bandset = set(band)
    def is_band(c):
        return inband(c)
    var = set()
    for u in band:
        for d in MOVES:
            v = (u[0] + d[0], u[1] + d[1])
            if not on(v):
                continue
            e = norm_edge(u, v)
            if is_band(v) or e in base:
                var.add(e)
    var = sorted(var)
    fixed = sorted(e for e in base if not is_band(e[0]) and not is_band(e[1])
                   and min(abs(trans(e[0])), abs(trans(e[1]))) < w + 6)
    return dict(T=T, lam=lam, canon=canon, band=band, var=var, fixed=fixed, base=base,
                is_band=is_band, inband=inband)


def contractible_cycles(ch, M):
    canon, isb = M['canon'], M['is_band']
    adj = defaultdict(list)
    for e in ch:
        a, b = e
        if not (isb(a) and isb(b)):
            continue
        (ra, ka), (rb, kb) = canon(a), canon(b)
        adj[ra].append((rb, kb - ka, e)); adj[rb].append((ra, ka - kb, e))
    phi, par, out = {}, {}, []
    for r0 in list(adj):
        if r0 in phi:
            continue
        phi[r0] = 0; par[r0] = None; stack = [r0]; order = []
        while stack:
            u = stack.pop()
            for v, sft, e in adj[u]:
                if v not in phi:
                    phi[v] = phi[u] + sft; par[v] = (u, e); stack.append(v)
        # non-tree edges
        seen = set()
        for u in list(phi):
            for v, sft, e in adj[u]:
                if (par.get(v) and par[v][1] == e and par[v][0] == u) or (par.get(u) and par[u][1] == e and par[u][0] == v):
                    continue
                if e in seen:
                    continue
                seen.add(e)
                if phi[u] + sft - phi[v] == 0:
                    # fundamental cycle: path u->root, v->root
                    def path(z):
                        P = []
                        while par[z] is not None:
                            P.append(par[z][1]); z = par[z][0]
                        return P
                    pu, pv = path(u), path(v)
                    su, sv = set(pu), set(pv)
                    C = [x for x in pu if x not in sv] + [x for x in pv if x not in su] + [e]
                    out.append(C)
    return out


def instances(e, T, K):
    for k in range(-K, K + 1):
        yield k, ((e[0][0] + k * T[0], e[0][1] + k * T[1]), (e[1][0] + k * T[0], e[1][1] + k * T[1]))


def solve(name, p, w, ks, threads=2, tlimit=300, show=False):
    M = build(name, p, w)
    T, var, fixed, canon, lam = M['T'], M['var'], M['fixed'], M['canon'], M['lam']
    K = 4
    m = cp_model.CpModel()
    xv = {e: m.NewBoolVar('') for e in var}
    # degree
    inc = defaultdict(list)
    for e in var:
        for c in e:
            if M['is_band'](c):
                inc[canon(c)[0]].append(e)
    for c in M['band']:
        m.Add(sum(xv[e] for e in inc[c]) == 2)
    for e in var:
        if not (M['is_band'](e[0]) and M['is_band'](e[1])):
            m.Add(xv[e] == 1)
    seg = lambda e: (*e[0], *e[1])
    terms = []
    pairs = 0
    for i, e in enumerate(var):
        for j in range(i, len(var)):
            f = var[j]
            cnt = 0
            for k, fi in instances(f, T, K):
                if i == j and k <= 0:
                    continue
                if cross(seg(e), seg(fi)):
                    cnt += 1
            if cnt:
                if i == j:
                    terms.append(cnt * xv[e])
                else:
                    z = m.NewBoolVar('')
                    m.AddBoolOr([xv[e].Not(), xv[f].Not(), z])
                    terms.append(cnt * z)
        for f in fixed:
            cnt = sum(1 for k, fi in instances(f, T, K) if cross(seg(e), seg(fi)))
            if cnt:
                terms.append(cnt * xv[e])
    m.Minimize(sum(terms))
    # current through cut lam = -1/2
    cur = []
    for e in var:
        c = 0
        for k, ei in instances(e, T, K + 2):
            a, b = ei
            la, lb = lam(a), lam(b)
            if la < 0 <= lb:
                c += chi(a)
            elif lb < 0 <= la:
                c += chi(b)
        if c:
            cur.append((c, e))
    base_cur = sum(c for c, e in cur if e in M['base'])
    base_obj = None
    res = {}
    for kk in ks:
        mm = m.Clone()
        xs = {e: mm.GetBoolVarFromProtoIndex(xv[e].Index()) for e in var}
        mm.Add(sum(c * xs[e] for c, e in cur) == base_cur + kk)
        s = cp_model.CpSolver(); s.parameters.num_workers = threads; s.parameters.max_time_in_seconds = tlimit
        while True:
            st = s.Solve(mm)
            if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                res[kk] = (s.StatusName(st), None, None, None); break
            ch = [e for e in var if s.Value(xs[e])]
            cyc = contractible_cycles(ch, M)
            if not cyc:
                res[kk] = (s.StatusName(st), s.ObjectiveValue(), s.BestObjectiveBound(), ch); break
            for C in cyc:
                mm.Add(sum(xs[e] for e in C) <= len(C) - 1)
    # base objective (k=0 with base edges) for reference
    bobj = 0
    bset = [e for e in var if e in M['base']]
    return M, res, base_cur


if __name__ == '__main__':
    name, p, w = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    ks = [int(a) for a in sys.argv[4:]] or [0, 1, 2]
    M, res, bc = solve(name, p, w, ks)
    for kk in ks:
        st, obj, bd, ch = res[kk]
        print(f'{name} p={p} w={w} current=base{kk:+d}: {st} crossings/period {obj} bound {bd}', flush=True)
        if ch is not None and '-v' in sys.argv[0:0]:
            print(sorted(ch))
