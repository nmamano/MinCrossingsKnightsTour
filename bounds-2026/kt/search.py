"""CP-SAT search for periodic edge gadgets (see strip.py for the model)."""
import time
from ortools.sat.python import cp_model
from .strip import Strip

def build_model(st, wX=1, wT=0, lanes=True, max_label_drift=3, hint=None, ub=None):
    m = cp_model.CpModel()
    x = [m.NewBoolVar(f'x{i}') for i in range(len(st.var_edges))]
    # degrees
    for u in st.base:
        m.Add(sum(x[e] for e, _ in st.inc[u]) == 2 - len(st.fixed_inc[u]))
    obj = []
    # crossings
    Xterms = []
    const = 0
    for ((ka, ia), (kb, ib)), c in st.cross.items():
        if ka == 'f' and kb == 'f':
            const += c
        elif ka == 'f':
            Xterms.append(c * x[ib])
        elif kb == 'f':
            Xterms.append(c * x[ia])
        elif ia == ib:
            Xterms.append(c * x[ia])
        else:
            z = m.NewBoolVar('')
            m.AddBoolOr([x[ia].Not(), x[ib].Not(), z])
            Xterms.append(c * z)
    Xexpr = sum(Xterms) + const
    # turns: turn_u = 1 - sum straight indicators
    Texpr = 0
    if wT:
        straight = []
        for u in st.base:
            has = {}
            for e, d in st.inc[u]:
                has[d] = x[e]
            for d in st.fixed_inc[u]:
                has[d] = 1
            for d in list(has):
                nd = (-d[0], -d[1])
                if nd in has and d > nd:
                    a, b = has[d], has[nd]
                    if isinstance(a, int) and isinstance(b, int):
                        straight.append(1)
                        continue
                    sv = m.NewBoolVar('')
                    for t in (a, b):
                        if not isinstance(t, int):
                            m.AddImplication(sv, t)
                    straight.append(sv)
        Texpr = len(st.base) - sum(straight)
    # connectivity: every non-terminal reaches a terminal (single-commodity flow)
    N = len(st.base)
    term = set(st.terminals)
    fpos, fneg = [], []
    for i, (u, v) in enumerate(st.var_edges):
        a = m.NewIntVar(0, N, ''); b = m.NewIntVar(0, N, '')
        m.Add(a <= N * x[i]); m.Add(b <= N * x[i])
        fpos.append(a); fneg.append(b)
    netout = {u: [] for u in st.base}
    for i, (u, v) in enumerate(st.var_edges):
        vb, k = st.canon(v)
        netout[u].append(fpos[i] - fneg[i])
        netout[vb].append(fneg[i] - fpos[i])
    for u in st.base:
        if u not in term:
            m.Add(sum(netout[u]) == -1)
    if lanes:
        # lane-pair labels
        prs = {u: st.lane_info(u)[0] for u in st.terminals}
        lo, hi = min(prs.values()) - max_label_drift, max(prs.values()) + max_label_drift
        L = {u: m.NewIntVar(lo, hi, '') for u in st.base}
        for u, p in prs.items():
            m.Add(L[u] == p)
        for i, (u, v) in enumerate(st.var_edges):
            vb, k = st.canon(v)
            m.Add(L[u] == L[vb] + k * st.pairs_per_period).OnlyEnforceIf(x[i])
        # orientation flow: side-0 terminals emit 1, side-1 absorb 1
        g = {}
        net = {u: [] for u in st.base}
        for i, (u, v) in enumerate(st.var_edges):
            gp = m.NewBoolVar(''); gn = m.NewBoolVar('')
            m.Add(gp + gn <= x[i])
            vb, k = st.canon(v)
            net[u].append(gp - gn); net[vb].append(gn - gp)
        for u in st.base:
            if u in term:
                m.Add(sum(net[u]) == (1 if st.lane_info(u)[1] == 0 else -1))
            else:
                m.Add(sum(net[u]) == 0)
    m.Minimize(wX * Xexpr + wT * Texpr)
    if ub is not None:
        m.Add(wX * Xexpr + wT * Texpr <= ub)
    if hint:
        for i in range(len(x)):
            m.AddHint(x[i], 1 if i in hint else 0)
    return m, x, Xexpr, Texpr

def solve(st, wX=1, wT=0, time_limit=60, workers=2, log=False, **kw):
    m, x, Xe, Te = build_model(st, wX, wT, **kw)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = time_limit
    s.parameters.num_workers = workers
    s.parameters.log_search_progress = log
    t0 = time.time()
    r = s.Solve(m)
    res = {'status': s.StatusName(r), 'time': round(time.time() - t0, 1)}
    if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        ch = [i for i in range(len(x)) if s.Value(x[i])]
        X, T = st.evaluate(ch)
        res.update(obj=s.ObjectiveValue(), bound=s.BestObjectiveBound(), X=X, T=T, chosen=ch)
    return res

def to_template(st, chosen):
    """bottom kind: list of rows (top row first) of board.js move codes, like Sequence1."""
    from .core import MI, MJ
    code = {(MJ[m], -MI[m]): m for m in range(8)}
    dirs = {u: [] for u in st.base}
    for i in chosen:
        u, v = st.var_edges[i]
        vb, k = st.canon(v)
        d = (v[0] - u[0], v[1] - u[1])
        dirs[u].append(code[d]); dirs[vb].append(code[(-d[0], -d[1])])
    for u, ds in st.fixed_inc.items():
        for d in ds:
            dirs[u].append(code[d])
    if st.kind == 'bottom':
        return [' '.join(''.join(map(str, sorted(dirs[(x, y)]))) for x in range(st.P)) for y in range(st.D - 1, -1, -1)]
    # left: rows top (largest y) first, columns x = 0..D-1
    return [' '.join(''.join(map(str, sorted(dirs[(x, y)]))) for x in range(st.D)) for y in range(st.P - 1, -1, -1)]
