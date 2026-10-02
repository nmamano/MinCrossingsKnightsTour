"""General periodic seam model (KT Structures, 2026-10-02).

Unrolled plane coordinates (x, y), y up. A straight seam with integer period vector T.
h(c) = hv . c (hv . T == 0). Band: -w1 <= h <= w2 (all cells free).
Side 1 (h < -w1): every cell keeps its two edges along direction f1 (lines of family 1).
Side 2 (h >  w2): lines of family 2 along f2  (or a wall = off-board, if f2 is None).
Line ids: form1 . c on side 1, form2 . c on side 2 (form . f == 0). form1.T == form2.T required.
Lanes of s lines: lane_j(c) = floor((form_j.c - off_j)/s).
Mode 'cross': every strand joins a side-1 end to a side-2 end with lane2 == lane1 + shift
              (strands may permute inside a lane).
Mode 'wall' : (f2 None) strands join side-1 ends of lanes 2j and 2j+1 (paper heel rule).
No cycles anywhere (incl. winding ones). Objective: crossings (+ turns) per period.
"""
from collections import defaultdict
import time
from ortools.sat.python import cp_model
import sys
sys.path.insert(0, '/home/nil/nil/knight-formation-research')
from kt.core import seg_cross

MOVES = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
dot = lambda a, b: a[0] * b[0] + a[1] * b[1]
add = lambda a, b: (a[0] + b[0], a[1] + b[1])
neg = lambda a: (-a[0], -a[1])


class Seam:
    def __init__(self, T, hv, w1, w2, f1, form1, f2=None, form2=None, s=4, off1=0, off2=0, shift=0):
        assert dot(hv, T) == 0
        self.T, self.hv, self.w1, self.w2 = T, hv, w1, w2
        self.f1, self.form1, self.f2, self.form2 = f1, form1, f2, form2
        self.s, self.off1, self.off2, self.shift = s, off1, off2, shift
        self.wall = f2 is None
        assert dot(form1, f1) == 0
        self.delta = dot(form1, T)
        if not self.wall:
            assert dot(form2, f2) == 0
            assert dot(form2, T) == self.delta, (dot(form2, T), self.delta)
        assert self.delta % s == 0
        self.lpp = self.delta // s                     # lanes per period
        self.ax = 0 if T[0] != 0 else 1
        assert T[self.ax] > 0
        self._build()

    def h(self, c):
        return dot(self.hv, c)

    def side(self, c):
        hh = self.h(c)
        return 1 if hh < -self.w1 else (2 if hh > self.w2 else 0)

    def canon(self, c):
        k = c[self.ax] // self.T[self.ax]
        return (c[0] - k * self.T[0], c[1] - k * self.T[1]), k

    def shiftc(self, c, k):
        return (c[0] + k * self.T[0], c[1] + k * self.T[1])

    def _build(self):
        p = self.T[self.ax]
        R = abs(self.w1) + abs(self.w2) + 3 * p + 10
        base = []
        for a in range(p):
            for b in range(-R, R + 1):
                c = (a, b) if self.ax == 0 else (b, a)
                if self.side(c) == 0:
                    base.append(c)
        self.base = sorted(base)
        self.idx = {c: i for i, c in enumerate(self.base)}
        self.var_edges, self.fixed_edges = [], []
        for u in self.base:
            for d in MOVES:
                v = add(u, d)
                sd = self.side(v)
                if sd == 0:
                    if d[0] > 0:
                        self.var_edges.append((u, v))
                elif sd == 1:
                    if d in (self.f1, neg(self.f1)):
                        self.fixed_edges.append((u, v, 1))
                elif sd == 2 and not self.wall:
                    if d in (self.f2, neg(self.f2)):
                        self.fixed_edges.append((u, v, 2))
        self.inc = defaultdict(list)
        for eid, (u, v) in enumerate(self.var_edges):
            vb, k = self.canon(v)
            d = (v[0] - u[0], v[1] - u[1])
            self.inc[u].append((eid, d))
            self.inc[vb].append((eid, neg(d)))
        self.fixed_inc = defaultdict(list)     # u -> [(dir, side)]
        for (u, v, sd) in self.fixed_edges:
            self.fixed_inc[u].append(((v[0] - u[0], v[1] - u[1]), sd))
        self.terminals = sorted(self.fixed_inc)
        # crossings among segments, with translates
        segs = [('v', i, (u, v)) for i, (u, v) in enumerate(self.var_edges)] + \
               [('f', i, (u, v)) for i, (u, v, _) in enumerate(self.fixed_edges)]
        span = max(abs(c[0]) + abs(c[1]) for c in self.base) * 2 + 8
        K = span // p + 2
        self.cross = defaultdict(int)
        for a in range(len(segs)):
            ka, ia, (p1, p2) = segs[a]
            for b in range(a, len(segs)):
                kb, ib, (q1, q2) = segs[b]
                cnt = 0
                for k in range(-K, K + 1):
                    if a == b and k == 0:
                        continue
                    r1, r2 = self.shiftc(q1, k), self.shiftc(q2, k)
                    if seg_cross(p1, p2, r1, r2):
                        cnt += 1
                if cnt:
                    if a == b:
                        assert cnt % 2 == 0
                        cnt //= 2
                    self.cross[((ka, ia), (kb, ib))] += cnt

    def lane(self, u, sd):
        if sd == 1:
            return (dot(self.form1, u) - self.off1) // self.s
        return (dot(self.form2, u) - self.off2) // self.s

    def evaluate(self, chosen):
        chosen = set(chosen)
        X = 0
        for ((ka, ia), (kb, ib)), c in self.cross.items():
            if (ka == 'f' or ia in chosen) and (kb == 'f' or ib in chosen):
                X += c
        turns = 0
        for u in self.base:
            dirs = [d for (eid, d) in self.inc[u] if eid in chosen] + [d for d, _ in self.fixed_inc[u]]
            assert len(dirs) == 2, (u, dirs)
            if dirs[0] != neg(dirs[1]):
                turns += 1
        return X, turns


def build_model(st, wX=1, wT=0, drift=4, hint=None, lanes=True):
    m = cp_model.CpModel()
    x = [m.NewBoolVar(f'x{i}') for i in range(len(st.var_edges))]
    for u in st.base:
        need = 2 - len(st.fixed_inc[u])
        if need < 0:
            m.AddBoolOr([])  # infeasible
        m.Add(sum(x[e] for e, _ in st.inc[u]) == need)
    Xt, const = [], 0
    for ((ka, ia), (kb, ib)), c in st.cross.items():
        if ka == 'f' and kb == 'f':
            const += c
        elif ka == 'f':
            Xt.append(c * x[ib])
        elif kb == 'f' or ia == ib:
            Xt.append(c * x[ia])
        else:
            z = m.NewBoolVar('')
            m.AddBoolOr([x[ia].Not(), x[ib].Not(), z])
            Xt.append(c * z)
    Xe = sum(Xt) + const
    Te = 0
    if wT:
        straight = []
        for u in st.base:
            has = {}
            for e, d in st.inc[u]:
                has[d] = x[e]
            for d, _ in st.fixed_inc[u]:
                has[d] = 1
            for d in list(has):
                nd = neg(d)
                if nd in has and d > nd:
                    a, b = has[d], has[nd]
                    if isinstance(a, int) and isinstance(b, int):
                        straight.append(1); continue
                    sv = m.NewBoolVar('')
                    for t in (a, b):
                        if not isinstance(t, int):
                            m.AddImplication(sv, t)
                    straight.append(sv)
        Te = len(st.base) - sum(straight)
    # no cycles: every non-terminal sends one unit to terminals
    N = len(st.base)
    term = set(st.terminals)
    net = {u: [] for u in st.base}
    for i, (u, v) in enumerate(st.var_edges):
        a = m.NewIntVar(0, N, ''); b = m.NewIntVar(0, N, '')
        m.Add(a <= N * x[i]); m.Add(b <= N * x[i])
        vb, k = st.canon(v)
        net[u].append(a - b); net[vb].append(b - a)
    for u in st.base:
        if u not in term:
            m.Add(sum(net[u]) == -1)
    if lanes:
        labs = {}
        for u in st.terminals:
            for d, sd in st.fixed_inc[u]:
                if st.wall and getattr(st, 'pairfun', None):
                    lab = st.pairfun(dot(st.form1, u))[0]
                elif st.wall:
                    lab = st.lane(u, 1) // 2
                else:
                    lab = st.lane(u, 1) if sd == 1 else st.lane(u, 2) - st.shift
                if u in labs and labs[u] != lab:
                    m.AddBoolOr([])
                labs[u] = lab
        lo, hi = min(labs.values()) - drift, max(labs.values()) + drift
        L = {u: m.NewIntVar(lo, hi, '') for u in st.base}
        for u, lab in labs.items():
            m.Add(L[u] == lab)
        ppp = (st.pair_ppp if getattr(st, 'pairfun', None) else st.lpp // 2) if st.wall else st.lpp
        for i, (u, v) in enumerate(st.var_edges):
            vb, k = st.canon(v)
            m.Add(L[u] == L[vb] + k * ppp).OnlyEnforceIf(x[i])
        # orientation flow
        net2 = {u: [] for u in st.base}
        for i, (u, v) in enumerate(st.var_edges):
            gp = m.NewBoolVar(''); gn = m.NewBoolVar('')
            m.Add(gp + gn <= x[i])
            vb, k = st.canon(v)
            net2[u].append(gp - gn); net2[vb].append(gn - gp)
        for u in st.base:
            sup = 0
            for d, sd in st.fixed_inc[u]:
                if st.wall and getattr(st, 'pairfun', None):
                    sup += 1 if st.pairfun(dot(st.form1, u))[1] == 0 else -1
                elif st.wall:
                    sup += 1 if st.lane(u, 1) % 2 == 0 else -1
                else:
                    sup += 1 if sd == 1 else -1
            m.Add(sum(net2[u]) == sup)
    m.Minimize(wX * Xe + wT * Te)
    m._Xe = Xe
    if hint:
        for i in range(len(x)):
            m.AddHint(x[i], 1 if i in hint else 0)
    return m, x


def solve(st, wX=1, wT=0, time_limit=60, workers=1, log=False, **kw):
    m, x = build_model(st, wX, wT, **kw)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = time_limit
    s.parameters.num_workers = workers
    s.parameters.log_search_progress = log
    t0 = time.time()
    r = s.Solve(m)
    res = {'status': s.StatusName(r), 'time': round(time.time() - t0, 1)}
    if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        ch = [i for i in range(len(x)) if s.Value(x[i])]
        X, Tn = st.evaluate(ch)
        res.update(obj=s.ObjectiveValue(), bound=s.BestObjectiveBound(), X=X, T=Tn, chosen=ch)
    return res


def cell_moves(st, chosen):
    """dict base cell -> list of two move vectors (dx, dy)."""
    dirs = {u: [] for u in st.base}
    for i in chosen:
        u, v = st.var_edges[i]
        vb, k = st.canon(v)
        d = (v[0] - u[0], v[1] - u[1])
        dirs[u].append(d); dirs[vb].append(neg(d))
    for u, lst in st.fixed_inc.items():
        for d, _ in lst:
            dirs[u].append(d)
    return dirs
