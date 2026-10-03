"""Get diagonal free-fold band templates carrying colour current (KT Structures)."""
import sys, json
from seam import Seam, build_model, cell_moves
from seam_flux import KIND, cur_terms
from ortools.sat.python import cp_model
def template(p, w, tgt, tl=300):
    k = KIND['diagfree']
    st = Seam(T=k['T'](p), hv=k['hv'], w1=w, w2=w, f1=k['f1'], form1=k['form1'], f2=k['f2'], form2=k['form2'], s=1)
    m, x = build_model(st, lanes=False)
    terms, const = cur_terms(st, x)
    m.Add(sum(terms) + const == tgt)
    s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = tl
    r = s.Solve(m)
    ch = [i for i in range(len(x)) if s.Value(x[i])]
    dirs = cell_moves(st, ch)
    return s.StatusName(r), st.evaluate(ch), {f'{u[0]},{u[1]}': ds for u, ds in dirs.items()}
if __name__ == '__main__':
    p, w = int(sys.argv[1]), int(sys.argv[2])
    out = {}
    for tgt in [int(a) for a in sys.argv[3:]]:
        st, ev, d = template(p, w, tgt)
        print(tgt, st, ev, flush=True)
        out[tgt] = {'status': st, 'XT': ev, 'cells': d}
    json.dump(out, open(f'diag_tpl_p{p}_w{w}.json', 'w'))
