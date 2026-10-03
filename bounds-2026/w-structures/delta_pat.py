"""Left-edge steep A' patterns (x-2y=c) with a prescribed U-turn pairing type and colour current.
pairing 'cheap': c even <-> c-3 ; 'flip': c even <-> c+3.  KT Structures 2026-10-02."""
import sys, json
from seam import Seam, build_model, cell_moves
from flux_strip import current_terms
from ortools.sat.python import cp_model
def pf_cheap(c):
    return (c // 2, 0) if c % 2 == 0 else ((c + 3) // 2, 1)
def pf_flip(c):
    return (c // 2, 0) if c % 2 == 0 else ((c - 3) // 2, 1)
def make(p, D, pairing):
    st = Seam(T=(0, p), hv=(-1, 0), w1=D - 1, w2=0, f1=(2, 1), form1=(1, -2), s=1)
    st.pairfun = pf_cheap if pairing == 'cheap' else pf_flip
    st.pair_ppp = st.delta // 2
    return st
def solve_pat(p, D, pairing, cur=None, tl=120):
    st = make(p, D, pairing)
    m, x = build_model(st, lanes=True, drift=6)
    if cur is not None:
        terms, const = current_terms(st, x)
        m.Add(sum(terms) + const == cur)
    s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = tl
    r = s.Solve(m)
    if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return st, s.StatusName(r), None
    ch = [i for i in range(len(x)) if s.Value(x[i])]
    return st, s.StatusName(r), ch
if __name__ == '__main__':
    p, D = int(sys.argv[1]), int(sys.argv[2])
    for pairing in ('cheap', 'flip'):
        for cur in (None, -1, 0, 1, -2) if D != 4 else (None, 0, 1, -1, 2):
            st, status, ch = solve_pat(p, D, pairing, cur)
            if ch is None:
                print(pairing, 'cur', cur, status); continue
            X, T = st.evaluate(ch)
            xv = [1 if i in ch else 0 for i in range(len(st.var_edges))]
            t, c = current_terms(st, xv)
            print(pairing, 'cur', cur, status, 'X', X, 'per row', X / p, 'current', sum(t) + c, flush=True)
