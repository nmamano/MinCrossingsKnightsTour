# cross-check: does CP-SAT find a periodic gadget that differs from given template(s)? (ignores objective)
import sys, json
from lib import *
from ortools.sat.python import cp_model
from verify import check
kind, P, D, off = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
st = Strip(kind, P, D, off=off)
m, x, Xe, Te = search.build_model(st, 1, 0)
m.ClearObjective()
sols = []
for it in range(int(sys.argv[5]) if len(sys.argv) > 5 else 20):
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 60; s.parameters.num_workers = 2
    r = s.Solve(m)
    if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print('no more:', s.StatusName(r)); break
    ch = [i for i in range(len(x)) if s.Value(x[i])]
    tpl = search.to_template(st, ch); c = check(kind, tpl, off=off)
    print(st.evaluate(ch), c['ok'], c['X_per_period'], tpl, flush=True)
    m.AddBoolOr([x[i].Not() for i in ch])
