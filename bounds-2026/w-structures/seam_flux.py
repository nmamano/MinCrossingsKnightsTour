"""Min crossings of a periodic seam subject to a colour current through the transversal cut x = -1/2.
usage: seam_flux.py kind p w [targets...]   (kinds from run_seam.KIND + 'diagfree')"""
import sys
from seam import Seam, build_model
from ortools.sat.python import cp_model
from run_seam import KIND
KIND['diagfree'] = dict(T=lambda p: (p, p), hv=(-1, 1), f1=(1, 2), form1=(2, -1), f2=(2, 1), form2=(-1, 2))
chi = lambda c: 1 if (c[0] + c[1]) % 2 == 0 else -1
def cur_terms(st, x):
    terms, const = [], 0
    T = st.T
    def straddle(a, b):
        lo, hi = (a, b) if a[0] < b[0] else (b, a)
        return lo if lo[0] < 0 <= hi[0] else None
    for i, (u, v) in enumerate(st.var_edges):
        for k in range(-6, 7):
            a = (u[0] + k * T[0], u[1] + k * T[1]); b = (v[0] + k * T[0], v[1] + k * T[1])
            lo = straddle(a, b)
            if lo: terms.append(chi(lo) * x[i])
    for (u, v, sd) in st.fixed_edges:
        for k in range(-6, 7):
            a = (u[0] + k * T[0], u[1] + k * T[1]); b = (v[0] + k * T[0], v[1] + k * T[1])
            lo = straddle(a, b)
            if lo: const += chi(lo)
    return terms, const
if __name__ == '__main__':
    kind, p, w = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    k = KIND[kind]
    st = Seam(T=k['T'](p), hv=k['hv'], w1=w, w2=w, f1=k['f1'], form1=k['form1'], f2=k['f2'], form2=k['form2'], s=1)
    m, x = build_model(st, lanes=False)
    s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = 60
    s.Solve(m); X0 = s.ObjectiveValue()
    ch = [i for i in range(len(x)) if s.Value(x[i])]
    t0, c0 = cur_terms(st, [1 if i in ch else 0 for i in range(len(x))])
    print(kind, 'p', p, 'w', w, 'min X', X0, 'its current', sum(t0) + c0, flush=True)
    for tgt in [int(a) for a in sys.argv[4:]]:
        m, x = build_model(st, lanes=False)
        terms, const = cur_terms(st, x)
        m.Add(sum(terms) + const == tgt)
        s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = 120
        r = s.Solve(m)
        print('  current', tgt, s.StatusName(r), s.ObjectiveValue() if r in (2, 4) else None, 'per unit x', s.ObjectiveValue() / st.T[0] if r in (2, 4) else None, flush=True)
