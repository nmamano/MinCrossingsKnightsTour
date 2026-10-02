"""Gentle seam p=6 w=3, lanes of 3: min cost per (off2, shift, current). Saves feasible templates."""
import sys, json
from seam import Seam, build_model
from seam_flux import cur_terms
from ortools.sat.python import cp_model
p, w = int(sys.argv[1]), int(sys.argv[2])
res = {}
for off2 in (0, 1, 2):
    for sh in (-1, 0, 1):
        st = Seam(T=(p, p), hv=(-1, 1), w1=w, w2=w, f1=(2, -1), form1=(1, 2), f2=(1, -2), form2=(2, 1), s=3, shift=sh, off2=off2)
        for tgt in (-1, 0):
            m, x = build_model(st, lanes=True, drift=6)
            terms, const = cur_terms(st, x); m.Add(sum(terms) + const == tgt)
            s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = 60
            r = s.Solve(m)
            ok = r in (2, 4)
            print('off2', off2, 'shift', sh, 'cur', tgt, s.StatusName(r), s.ObjectiveValue() if ok else None, flush=True)
            if ok:
                ch = {i for i in range(len(x)) if s.Value(x[i])}
                cells = {}
                for u in st.base:
                    cells['%d,%d' % u] = [d for (e, d) in st.inc[u] if e in ch] + [d for d, _ in st.fixed_inc[u]]
                res['%d,%d,%d' % (off2, sh, tgt)] = dict(X=s.ObjectiveValue(), cells=cells)
json.dump(res, open(f"gentle_tpl_lanes_p{p}_w{w}.json", "w"))
