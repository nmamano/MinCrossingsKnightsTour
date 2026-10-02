"""Left-edge strip, steep A' lines (x-2y=c), no lanes: min crossings, then range of colour current
through a horizontal cut among min-crossing patterns. KT Structures 2026-10-02."""
import sys
from seam import Seam, build_model
from ortools.sat.python import cp_model
p = int(sys.argv[1]) if __name__ == "__main__" else 2; D = int(sys.argv[2]) if __name__ == "__main__" else 3; slack = 0
st = Seam(T=(0, p), hv=(-1, 0), w1=D - 1, w2=0, f1=(2, 1), form1=(1, -2), s=1) if __name__ == "__main__" else None
chi = lambda c: 1 if (c[0] + c[1]) % 2 == 0 else -1
def current_terms(st, x):
    # cut between rows y=-1 and y=0 (unrolled): edges (u,v) with u.y < 0 <= v.y or v.y < 0 <= u.y
    terms, const = [], 0
    for i, (u, v) in enumerate(st.var_edges):
        # all translates: edge u -> v (v unrolled); translate by k*T so that it straddles y=0
        for k in range(-4, 5):
            a = (u[0], u[1] + k * st.T[1]); b = (v[0], v[1] + k * st.T[1])
            lo, hi = (a, b) if a[1] < b[1] else (b, a)
            if lo[1] < 0 <= hi[1]:
                terms.append(chi(lo) * x[i])
    for (u, v, sd) in st.fixed_edges:
        for k in range(-4, 5):
            a = (u[0], u[1] + k * st.T[1]); b = (v[0], v[1] + k * st.T[1])
            lo, hi = (a, b) if a[1] < b[1] else (b, a)
            if lo[1] < 0 <= hi[1]:
                const += chi(lo)
    return terms, const
if __name__ == '__main__':
    res = {}
    for sense in ('min', 'max'):
        m, x = build_model(st, lanes=False)
        s = cp_model.CpSolver(); s.parameters.num_workers = 1; s.parameters.max_time_in_seconds = 60
        r = s.Solve(m); Xopt = round(s.ObjectiveValue())
        # rebuild with X <= Xopt + slack and optimise current
        m2, x2 = build_model(st, lanes=False)
        terms, const = current_terms(st, x2)
        m2.Add(m2._Xe <= Xopt + slack)
        cur = sum(terms) + const
        if sense == 'min': m2.Minimize(cur)
        else: m2.Maximize(cur)
        s2 = cp_model.CpSolver(); s2.parameters.num_workers = 1; s2.parameters.max_time_in_seconds = 60
        r2 = s2.Solve(m2)
        res[sense] = (s2.StatusName(r2), s2.ObjectiveValue())
    print('p', p, 'D', D, 'Xopt', Xopt, 'slack', slack, res)
