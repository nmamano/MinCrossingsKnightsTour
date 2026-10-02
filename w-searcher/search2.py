"""CP-SAT strip search with a general PAIRING RULE instead of the lane rule (w-searcher, 2026-10-02).
Same strip model as kt/strip.py + kt/search.py (degrees, crossings, no cycle / no winding strand).
rule = None            -> lane-free: any pairing of line ends (only degree + no finite cycle + finite strands)
rule = (M, allowed)    -> every strand joins lines c < c' with ((c mod M), c' - c) in allowed.
Strand labels: A[u] = line of the strand's start terminal (orientation flow start -> end)."""
import time
from ortools.sat.python import cp_model
from kt.strip import Strip

def build(st, rule=None, wX=1, wT=0, hint=None, maxspan=40, pi=None):
    m = cp_model.CpModel()
    x = [m.NewBoolVar(f'x{i}') for i in range(len(st.var_edges))]
    for u in st.base:
        m.Add(sum(x[e] for e, _ in st.inc[u]) == 2 - len(st.fixed_inc[u]))
    Xterms, const = [], 0
    for ((ka, ia), (kb, ib)), c in st.cross.items():
        if ka == 'f' and kb == 'f': const += c
        elif ka == 'f': Xterms.append(c * x[ib])
        elif kb == 'f': Xterms.append(c * x[ia])
        elif ia == ib: Xterms.append(c * x[ia])
        else:
            z = m.NewBoolVar('')
            m.AddBoolOr([x[ia].Not(), x[ib].Not(), z])
            Xterms.append(c * z)
    Xexpr = sum(Xterms) + const
    Texpr = 0
    if wT:
        straight = []
        for u in st.base:
            has = {}
            for e, d in st.inc[u]: has[d] = x[e]
            for d in st.fixed_inc[u]: has[d] = 1
            for d in list(has):
                nd = (-d[0], -d[1])
                if nd in has and d > nd:
                    a, b = has[d], has[nd]
                    if isinstance(a, int) and isinstance(b, int): straight.append(1); continue
                    sv = m.NewBoolVar('')
                    for t in (a, b):
                        if not isinstance(t, int): m.AddImplication(sv, t)
                    straight.append(sv)
        Texpr = len(st.base) - sum(straight)
    # every non-terminal reaches a terminal (no cycle, no winding loop)
    N = len(st.base); term = set(st.terminals)
    net = {u: [] for u in st.base}
    for i, (u, v) in enumerate(st.var_edges):
        a = m.NewIntVar(0, N, ''); b = m.NewIntVar(0, N, '')
        m.Add(a <= N * x[i]); m.Add(b <= N * x[i])
        vb, k = st.canon(v)
        net[u].append(a - b); net[vb].append(b - a)
    for u in st.base:
        if u not in term: m.Add(sum(net[u]) == -1)
    # orientation flow start -> end, start label propagation
    shift = st.P if st.kind == 'bottom' else 2 * st.P      # line shift per period translation
    isS = {t: m.NewBoolVar('') for t in st.terminals}
    g = {u: [] for u in st.base}
    lines = [st.line_of(t) for t in st.terminals]
    lo, hi = min(lines) - maxspan, max(lines) + maxspan
    A = {u: m.NewIntVar(lo, hi, '') for u in st.base}
    Bl = {u: m.NewIntVar(lo, hi, '') for u in st.base} if pi is not None else None   # end line of the strand
    for i, (u, v) in enumerate(st.var_edges):
        gp = m.NewBoolVar(''); gn = m.NewBoolVar('')
        m.Add(gp + gn == x[i])
        vb, k = st.canon(v)
        g[u].append(gp - gn); g[vb].append(gn - gp)
        m.Add(A[u] == A[vb] + k * shift).OnlyEnforceIf(x[i])
        if Bl is not None: m.Add(Bl[u] == Bl[vb] + k * shift).OnlyEnforceIf(x[i])
    for u in st.base:
        if u in term:
            m.Add(sum(g[u]) == 1).OnlyEnforceIf(isS[u]); m.Add(sum(g[u]) == -1).OnlyEnforceIf(isS[u].Not())
            c = st.line_of(u)
            m.Add(A[u] == c).OnlyEnforceIf(isS[u])
            m.Add(A[u] != c).OnlyEnforceIf(isS[u].Not())
            if Bl is not None:
                m.Add(Bl[u] == c).OnlyEnforceIf(isS[u].Not()); m.Add(Bl[u] != c).OnlyEnforceIf(isS[u])
            if rule is not None:
                M, allowed = rule
                ok = set()
                for cs in range(lo, hi + 1):
                    a, b = min(cs, c), max(cs, c)
                    if ((a % M), b - a) in allowed: ok.add(cs)
                m.AddLinearExpressionInDomain(A[u], cp_model.Domain.FromValues(sorted(ok))).OnlyEnforceIf(isS[u].Not())
            # (lane-free: no condition on the end)
        else:
            m.Add(sum(g[u]) == 0)
    if pi is not None:
        # matching parity: number of pairs spanning the cut just below the lowest base terminal line, mod 2
        t0 = min(lines)
        sp = []
        for t in st.terminals:
            below = m.NewBoolVar('')
            # partner line = A (if t is an end) or Bl (if t is a start)
            m.Add(A[t] < t0).OnlyEnforceIf([below, isS[t].Not()]); m.Add(A[t] >= t0).OnlyEnforceIf([below.Not(), isS[t].Not()])
            m.Add(Bl[t] < t0).OnlyEnforceIf([below, isS[t]]); m.Add(Bl[t] >= t0).OnlyEnforceIf([below.Not(), isS[t]])
            sp.append(below)
        h = m.NewIntVar(0, len(sp), '')
        m.Add(sum(sp) == 2 * h + pi)
    m.Minimize(wX * Xexpr + wT * Texpr)
    if hint:
        for i in range(len(x)): m.AddHint(x[i], 1 if i in hint else 0)
    m._A, m._isS = A, isS
    return m, x

def solve(st, rule=None, wX=1, wT=0, time_limit=60, workers=2, hint=None, log=False):
    m, x = build(st, rule, wX, wT, hint)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = time_limit; s.parameters.num_workers = workers
    s.parameters.log_search_progress = log
    t0 = time.time(); r = s.Solve(m)
    res = {'status': s.StatusName(r), 'time': round(time.time() - t0, 1)}
    if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        ch = [i for i in range(len(x)) if s.Value(x[i])]
        X, T = st.evaluate(ch)
        res.update(obj=s.ObjectiveValue(), bound=s.BestObjectiveBound(), X=X, T=T, chosen=ch)
    return res

def solve_filtered(st, rule, accept, wX=1, time_limit=60, workers=2, max_iter=30, log=print, pi=None, hint=None):
    """Repeat: solve, test the template with accept(tpl) (e.g. integrator filter); if rejected, forbid
    that exact pairing (start/end labels of the terminals) and solve again."""
    from kt.search import to_template
    m, x = build(st, rule, wX, 0, pi=pi, hint=hint)
    A, isS = m._A, m._isS
    tried = 0
    best = None
    for it in range(max_iter):
        s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = time_limit; s.parameters.num_workers = workers
        r = s.Solve(m)
        if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return dict(status=s.StatusName(r), iters=it, best=best)
        ch = [i for i in range(len(x)) if s.Value(x[i])]
        X, T = st.evaluate(ch); tpl = to_template(st, ch)
        res = dict(status=s.StatusName(r), X=X, T=T, bound=s.BestObjectiveBound(), tpl=tpl, chosen=ch, iters=it)
        acc = accept(tpl)
        log('  iter %d: X=%d bound=%.1f status=%s accept=%s' % (it, X, s.BestObjectiveBound(), res['status'], bool(acc)))
        if acc:
            res['accept'] = acc
            return res
        # forbid this pairing
        lits = []
        for t in st.terminals:
            sv = s.Value(isS[t]); av = s.Value(A[t])
            b1 = m.NewBoolVar(''); m.Add(A[t] != av).OnlyEnforceIf(b1)
            lits.append(b1); lits.append(isS[t] if not sv else isS[t].Not())
        m.AddBoolOr(lits)
    return dict(status='ITER_LIMIT', best=best)
