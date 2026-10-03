"""Enumerate several current-carrying diagonal templates and keep their cells (KT Structures)."""
import sys, json
from seam import Seam, build_model, cell_moves
from seam_flux import KIND, cur_terms
from ortools.sat.python import cp_model
p, w, tgt, cmax, nsol = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
k = KIND['diagfree']
st = Seam(T=k['T'](p), hv=k['hv'], w1=w, w2=w, f1=k['f1'], form1=k['form1'], f2=k['f2'], form2=k['form2'], s=1)
m, x = build_model(st, lanes=False)
terms, const = cur_terms(st, x)
m.Add(sum(terms) + const == tgt)
m.Add(m._Xe <= cmax)
m.ClearObjective() if hasattr(m, 'ClearObjective') else None
out = []
for it in range(nsol):
    s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = 60
    r = s.Solve(m)
    if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        break
    ch = [i for i in range(len(x)) if s.Value(x[i])]
    out.append({'XT': st.evaluate(ch), 'cells': {f'{u[0]},{u[1]}': ds for u, ds in cell_moves(st, ch).items()}})
    m.AddBoolOr([x[i].Not() for i in ch])
    print(it, st.evaluate(ch), flush=True)
json.dump(out, open(f'diag_multi_p{p}_w{w}_t{tgt}.json', 'w'))
