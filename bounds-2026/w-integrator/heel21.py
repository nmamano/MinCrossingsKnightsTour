#!/usr/bin/env python
"""Rebuild the paper's turn-optimal heel (Figure 11 centre: 21 turns, 31 crossings) as an 8x4 template.

CP-SAT over the periodic bottom strip (kt.strip, P = 8, D = 4) with the EXACT strand pairing of the
paper's heels (each line end joins the same partner as in Sequence1Opt: no permutation), objective
turns first, then crossings. The result must be a drop-in heel for kt.gentour.gen_tour: it is checked
by building full tours for every even n in 48..80 (validate + walk_check) and measuring the turn slope.
Usage: heel21.py [--time 300] [--workers 3]
"""
import argparse, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from ortools.sat.python import cp_model
from kt.strip import Strip
from kt.search import build_model, to_template
from kt import templates as T
from strands import pairing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--time', type=float, default=300); ap.add_argument('--workers', type=int, default=3)
    a = ap.parse_args()
    st = Strip('bottom', 8, 4)
    ref = pairing(T.Sequence1Opt, 'bottom')['pairs']          # [(4, 9), (5, 8), (6, 11), (7, 10)]
    m, x, Xe, Te = build_model(st, wX=1, wT=1000, lanes=False)
    partner = {}
    for (p, q) in ref:
        partner[p % 8] = q - p; partner[q % 8] = p - q
    L = {u: m.NewIntVar(-64, 64, '') for u in st.base}
    for u in st.terminals:
        l = st.line_of(u)
        m.Add(L[u] == min(l, l + partner[l % 8]))
    for i, (u, v) in enumerate(st.var_edges):
        vb, k = st.canon(v)
        m.Add(L[u] == L[vb] + k * st.P).OnlyEnforceIf(x[i])
    # drop-in: the moves that cross the 8-column boundary equal those of Sequence1Opt
    from kt.board import tpl_moves
    mv, W, H = tpl_moves(T.Sequence1Opt)
    opt = {(u, (u[0] + d[0], u[1] + d[1])) for u in st.base for d in mv[u]}
    for i, (u, v) in enumerate(st.var_edges):
        if st.canon(v)[1] != 0:
            m.Add(x[i] == (1 if (u, v) in opt else 0))
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = a.time; s.parameters.num_workers = a.workers
    r = s.Solve(m)
    print('status', s.StatusName(r), 'obj', s.ObjectiveValue(), 'bound', s.BestObjectiveBound())
    ch = [i for i in range(len(x)) if s.Value(x[i])]
    X, Tn = st.evaluate(ch)
    tpl = to_template(st, ch)
    print('per period: X =', X, 'T =', Tn); print('template', tpl)
    print('pairing', pairing(tpl, 'bottom')['pairs'], 'ref', ref)
    # drop-in check in Algorithm 1
    from kt.gentour import gen_tour
    from kt.core import validate, num_turns, num_crossings
    from assemble import walk_check
    rows = []
    for n in range(48, 82, 2):
        try:
            g = gen_tour(n, n, heel=tpl); ok = validate(g) and walk_check(g)
        except Exception as e:
            ok = False
        rows.append((n, ok, num_turns(g) if ok else None, num_crossings(g) if ok else None))
    print('gen_tour:', rows)
    json.dump(dict(template=tpl, X_per8=X, T_per8=Tn, status=s.StatusName(r), pairing=ref, gen_tour=rows),
              open(os.path.join(HERE, 'gadgets', 'heel21.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
