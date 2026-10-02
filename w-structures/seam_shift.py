"""Gentle seam (period (p,p), w): min crossings per period for each forced line shift (lanes of 1) and current."""
import sys
from seam import Seam, build_model
from seam_flux import cur_terms
from ortools.sat.python import cp_model
p, w = int(sys.argv[1]), int(sys.argv[2]); shifts = [int(v) for v in sys.argv[3].split(',')]
for sh in shifts:
    st = Seam(T=(p, p), hv=(-1, 1), w1=w, w2=w, f1=(2, -1), form1=(1, 2), f2=(1, -2), form2=(2, 1), s=int(sys.argv[4]) if len(sys.argv) > 4 else 1, shift=sh)
    out = []
    for tgt in (-1, 0):
        m, x = build_model(st, lanes=True, drift=8)
        terms, const = cur_terms(st, x); m.Add(sum(terms) + const == tgt)
        s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = 60
        r = s.Solve(m)
        out.append((tgt, s.StatusName(r), s.ObjectiveValue() if r in (2, 4) else None))
    print('shift', sh, out, flush=True)
