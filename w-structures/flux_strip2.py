import sys
from seam import Seam, build_model
from ortools.sat.python import cp_model
from flux_strip import current_terms
import flux_strip
p = int(sys.argv[1]); D = int(sys.argv[2])
st = Seam(T=(0, p), hv=(-1, 0), w1=D - 1, w2=0, f1=(2, 1), form1=(1, -2), s=1)
for target in [int(a) for a in sys.argv[3:]] or range(-3, 2):
    m, x = build_model(st, lanes=False)
    terms, const = current_terms(st, x) if 'st' not in current_terms.__code__.co_varnames[:0] else None
    m.Add(sum(terms) + const == target)
    s = cp_model.CpSolver(); s.parameters.num_workers = 1; s.parameters.max_time_in_seconds = 120
    r = s.Solve(m)
    print('p', p, 'D', D, 'current', target, s.StatusName(r), s.ObjectiveValue() if r in (2, 4) else None,
          'per row', (s.ObjectiveValue() / p) if r in (2, 4) else None, flush=True)
