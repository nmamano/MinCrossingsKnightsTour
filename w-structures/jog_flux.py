"""Diagonal corridor (step (1,1)) inside a uniform (2,1) field with a forced line shift and a colour current.
Question (Integrator, 2026-10-02): can an odd line shift (jog band, index x-2y shifts by 3 mod 6) carry
current equal to the pure-field current (net 0), at zero or small crossing cost?
usage: jog_flux.py p w shift [shift...]   -> for each shift: min X (free current), its current, then min X
       for current targets base-6..base+6.  Lanes of 1 line, strand from side-1 line c ends on side-2 line c+shift."""
import sys
from seam import Seam, build_model
from seam_flux import cur_terms
from ortools.sat.python import cp_model

def mk(p, w, shift):
    return Seam(T=(p, p), hv=(-1, 1), w1=w, w2=w, f1=(2, 1), form1=(1, -2), f2=(2, 1), form2=(1, -2),
                s=1, shift=shift)

def run(st, tgt=None, tl=120):
    m, x = build_model(st, lanes=True)
    terms, const = cur_terms(st, x)
    if tgt is not None:
        m.Add(sum(terms) + const == tgt)
    s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = tl
    r = s.Solve(m)
    if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return s.StatusName(r), None, None, None
    ch = [1 if s.Value(v) else 0 for v in x]
    t, c = cur_terms(st, ch)
    return s.StatusName(r), s.ObjectiveValue(), s.BestObjectiveBound(), sum(t) + c

if __name__ == '__main__':
    p, w = int(sys.argv[1]), int(sys.argv[2])
    st0 = mk(p, w, 0)
    _, X0, _, I0 = run(st0)
    print(f'p={p} w={w} cells={len(st0.base)} shift 0: X {X0} base current I0 = {I0}', flush=True)
    for sh in [int(a) for a in sys.argv[3:]]:
        st = mk(p, w, sh)
        stat, X, bd, I = run(st)
        print(f' shift {sh}: free current -> {stat} X {X} current {I} (rel {None if I is None else I - I0})', flush=True)
        for dt in (-6, -3, -2, -1, 0, 1, 2, 3, 6):
            stat, X, bd, I = run(st, I0 + dt)
            print(f'   rel current {dt:+d}: {stat} X {X} bound {bd}', flush=True)
