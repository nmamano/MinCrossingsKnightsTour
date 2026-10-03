"""Left-edge gadget for a vertical zigzag texture (KT Structures, 2026-10-02).
Texture: zigzags x = f(y) + d (all integers d), f(y+1)-f(y) = +-2, f periodic with period P (sum of steps 0).
Translates of a function graph never cross, so the texture has 0 crossings in the bulk.
Board x >= 0. Band 0 <= x < D is free; cells x >= D keep their texture edges.
Constraints: degree 2; labels = lane of zigzag d (lane = floor((d-off)/s)) constant along chosen edges;
every component winds upward (oriented cycles may cross the period cut y = 0 mod P only upward, and a
potential strictly increases along all other oriented edges), so no finite cycles.
Objective: crossings (+ turns) per period."""
from collections import defaultdict
import time, sys
from ortools.sat.python import cp_model
sys.path.insert(0, '/home/nil/nil/knight-formation-research')
from kt.core import seg_cross

MOVES = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

class TexEdge:
    def __init__(self, steps, D, s=4, off=0):
        # steps: list of +-2 of length P, f(0)=0, f(y+1)=f(y)+steps[y mod P]
        self.steps, self.P, self.D, self.s, self.off = steps, len(steps), D, s, off
        assert sum(steps) == 0 and all(abs(t) == 2 for t in steps)
        fv = [0]
        for t in steps[:-1]:
            fv.append(fv[-1] + t)
        mn = min(fv)
        self.fv = [v - mn for v in fv]          # f >= 0, min 0
        self.T = (0, self.P)
        self.base = [(x, y) for y in range(self.P) for x in range(D)]
        self.idx = {c: i for i, c in enumerate(self.base)}
        self._build()

    def f(self, y):
        return self.fv[y % self.P]

    def tex_nbrs(self, c):
        x, y = c
        d = x - self.f(y)
        return [(self.f(y - 1) + d, y - 1), (self.f(y + 1) + d, y + 1)]

    def zig(self, c):
        return c[0] - self.f(c[1])

    def canon(self, c):
        k = c[1] // self.P
        return (c[0], c[1] - k * self.P), k

    def shiftc(self, c, k):
        return (c[0], c[1] + k * self.P)

    def in_band(self, c):
        return 0 <= c[0] < self.D

    def _build(self):
        self.var_edges, self.fixed = [], []
        for u in self.base:
            for d in MOVES:
                v = (u[0] + d[0], u[1] + d[1])
                if self.in_band(v) and (d[1] > 0):
                    self.var_edges.append((u, v))
        # fixed edges: texture edges from outside cells into band
        self.fixed_inc = defaultdict(list)
        self.fixed_edges = []
        for u in self.base:
            for dd in MOVES:
                v = (u[0] + dd[0], u[1] + dd[1])
                if v[0] >= self.D and u in [self.canon(w)[0] if False else w for w in self.tex_nbrs(v)]:
                    self.fixed_edges.append((u, v))
                    self.fixed_inc[u].append(v)
        # arcs: follow texture from a terminal's outside neighbour until re-entering band
        self.arcs = []      # (u_base, v_base, k, zig d)  connecting band cell u to band cell v + k*T
        seen = set()
        for u in self.base:
            for v in self.fixed_inc[u]:
                if (u, v) in seen:
                    continue
                prev, cur = u, v
                path = [u, v]
                while not self.in_band(cur):
                    a, b = self.tex_nbrs(cur)
                    nxt = b if a == prev else a
                    prev, cur = cur, nxt
                    path.append(cur)
                    assert len(path) < 1000
                vb, k = self.canon(cur)
                ub, ku = self.canon(u)
                seen.add((u, v))
                # the reverse direction from vb starts with path[-2] shifted by -k
                last_out = path[-2]
                seen.add((vb, (last_out[0], last_out[1] - k * self.P)))
                self.arcs.append((u, vb, k, self.zig(v), path))
        self.terminals = sorted(self.fixed_inc)
        # crossings
        segs = [('v', i, e) for i, e in enumerate(self.var_edges)] + [('f', i, e) for i, e in enumerate(self.fixed_edges)]
        K = 12 // self.P + 2
        self.cross = defaultdict(int)
        for a in range(len(segs)):
            ka, ia, (p1, p2) = segs[a]
            for b in range(a, len(segs)):
                kb, ib, (q1, q2) = segs[b]
                if ka == 'f' and kb == 'f':
                    continue
                cnt = 0
                for k in range(-K, K + 1):
                    if a == b and k == 0:
                        continue
                    if seg_cross(p1, p2, self.shiftc(q1, k), self.shiftc(q2, k)):
                        cnt += 1
                if cnt:
                    if a == b:
                        cnt //= 2
                    self.cross[((ka, ia), (kb, ib))] += cnt

    def lane(self, d):
        return (d - self.off) // self.s


def build(st, wX=1, wT=0, lanes=True, hint=None):
    m = cp_model.CpModel()
    x = [m.NewBoolVar('') for _ in st.var_edges]
    inc = defaultdict(list)
    for i, (u, v) in enumerate(st.var_edges):
        vb, k = st.canon(v)
        inc[u].append(i); inc[vb].append(i)
    for u in st.base:
        m.Add(sum(x[i] for i in inc[u]) == 2 - len(st.fixed_inc[u]))
    Xt = []
    for ((ka, ia), (kb, ib)), c in st.cross.items():
        if ka == 'f':
            Xt.append(c * x[ib])
        elif kb == 'f' or ia == ib:
            Xt.append(c * x[ia])
        else:
            z = m.NewBoolVar(''); m.AddBoolOr([x[ia].Not(), x[ib].Not(), z]); Xt.append(c * z)
    Xe = sum(Xt)
    Te = 0
    if wT:
        st_dirs = defaultdict(list)
        for i, (u, v) in enumerate(st.var_edges):
            vb, k = st.canon(v)
            d = (v[0] - u[0], v[1] - u[1])
            st_dirs[u].append((d, x[i])); st_dirs[vb].append(((-d[0], -d[1]), x[i]))
        straight = []
        for u in st.base:
            has = {d: lit for d, lit in st_dirs[u]}
            for v in st.fixed_inc[u]:
                has[(v[0] - u[0], v[1] - u[1])] = 1
            for d in list(has):
                nd = (-d[0], -d[1])
                if nd in has and d > nd:
                    a, b = has[d], has[nd]
                    sv = m.NewBoolVar('')
                    for t in (a, b):
                        if not isinstance(t, int):
                            m.AddImplication(sv, t)
                    straight.append(sv)
        Te = len(st.base) - sum(straight)
    # orientation: each node in=1 out=1 over var edges + arcs
    N = len(st.base)
    phi = {u: m.NewIntVar(0, 4 * N, '') for u in st.base}
    out = defaultdict(list); inn = defaultdict(list)
    def orient(u, vb, k, lit_on):
        up = m.NewBoolVar(''); dn = m.NewBoolVar('')
        if lit_on is None:
            m.Add(up + dn == 1)
        else:
            m.Add(up + dn == lit_on)
        out[u].append(up); inn[vb].append(up)
        out[vb].append(dn); inn[u].append(dn)
        # u->vb+kT when up; vb->u-kT when dn
        for lit, a, b, kk in ((up, u, vb, k), (dn, vb, u, -k)):
            if kk == 0:
                m.Add(phi[b] >= phi[a] + 1).OnlyEnforceIf(lit)
            elif kk < 0:
                m.Add(lit == 0)
    for i, (u, v) in enumerate(st.var_edges):
        vb, k = st.canon(v)
        orient(u, vb, k, x[i])
    for (u, vb, k, d, path) in st.arcs:
        orient(u, vb, k, None)
    for u in st.base:
        m.Add(sum(out[u]) == 1); m.Add(sum(inn[u]) == 1)
    if lanes:
        lo = st.lane(-4) - 1; hi = st.lane(st.D + 8) + 1
        L = {u: m.NewIntVar(lo, hi, '') for u in st.base}
        for (u, vb, k, d, path) in st.arcs:
            m.Add(L[u] == st.lane(d)); m.Add(L[vb] == st.lane(d))
        for i, (u, v) in enumerate(st.var_edges):
            vb, k = st.canon(v)
            m.Add(L[u] == L[vb]).OnlyEnforceIf(x[i])
    m.Minimize(wX * Xe + wT * Te)
    return m, x

def evaluate(st, chosen):
    chosen = set(chosen)
    X = 0
    for ((ka, ia), (kb, ib)), c in st.cross.items():
        if (ka == 'f' or ia in chosen) and (kb == 'f' or ib in chosen):
            X += c
    dirs = defaultdict(list)
    for i in chosen:
        u, v = st.var_edges[i]; vb, k = st.canon(v)
        d = (v[0] - u[0], v[1] - u[1]); dirs[u].append(d); dirs[vb].append((-d[0], -d[1]))
    for u, vs in st.fixed_inc.items():
        for v in vs:
            dirs[u].append((v[0] - u[0], v[1] - u[1]))
    T = sum(1 for u in st.base if dirs[u][0] != (-dirs[u][1][0], -dirs[u][1][1]))
    return X, T, dirs

def solve(st, tl=60, workers=1, **kw):
    m, x = build(st, **kw)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = workers
    t0 = time.time(); r = s.Solve(m)
    res = {'status': s.StatusName(r), 'time': round(time.time() - t0, 1)}
    if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        ch = [i for i in range(len(x)) if s.Value(x[i])]
        X, T, dirs = evaluate(st, ch)
        res.update(X=X, T=T, bound=s.BestObjectiveBound(), chosen=ch)
    return res
