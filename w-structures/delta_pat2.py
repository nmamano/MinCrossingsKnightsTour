import sys
from delta_pat import make
import delta_pat
from seam import build_model, Seam
from flux_strip import current_terms
from ortools.sat.python import cp_model
p, D = int(sys.argv[1]), int(sys.argv[2])
for k in (-7, -5, -3, -1, 1, 3, 5, 7):
    pf = lambda c, k=k: (c // 2, 0) if c % 2 == 0 else ((c - k) // 2, 1)
    for cur in (-1, 0, 1):
        st = Seam(T=(0, p), hv=(-1, 0), w1=D - 1, w2=0, f1=(2, 1), form1=(1, -2), s=1)
        st.pairfun = pf; st.pair_ppp = st.delta // 2
        m, x = build_model(st, lanes=True, drift=8)
        terms, const = current_terms(st, x); m.Add(sum(terms) + const == cur)
        s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = 60
        r = s.Solve(m)
        print('pair c<->c+%d' % k, 'cur', cur, s.StatusName(r), (s.ObjectiveValue() / p) if r in (2, 4) else '', flush=True)
