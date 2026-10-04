"""Enumerate corner solutions with reduced value == target (scaled) at potential w; print distinct (s, t, sigma t) hex.
usage: cornopt.py W A wfile target maxsol tl"""
import sys
from ortools.sat.python import cp_model
import corner_pot as cp
W, A, wf, target, maxsol, tl = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), float(sys.argv[6])
t = [int(x) for x in open(wf).read().split()]; sc, w = t[0], t[1:]
m, c, phi, S = cp.build(W, A)
# rebuild cut indicator expressions (same as corner_pot.build)
from itertools import combinations
K = len(S); sg = cp.sigma_perm(S)
m.Add(sc * c + sum(wk * f for wk, f in zip(w, phi)) == target)
# access ev/eh: rebuild by re-running build internals is awkward; recompute via phi parts is ambiguous, so rebuild here
m2, c2, phi2, _ = None, None, None, None
class CB(cp_model.CpSolverSolutionCallback):
    def __init__(s, ev, eh): super().__init__(); s.ev, s.eh, s.seen, s.n = ev, eh, set(), 0
    def on_solution_callback(s):
        s.n += 1
        sv = sum(1 << k for k in range(K) if s.Value(s.ev[k])); tv = sum(1 << k for k in range(K) if s.Value(s.eh[k]))
        if (sv, tv) not in s.seen:
            s.seen.add((sv, tv)); st = sum(1 << sg[j] for j in range(K) if tv >> j & 1)
            print(f'{sv:x} {tv:x} {st:x}', flush=True)
        if len(s.seen) >= maxsol: s.StopSearch()
ev, eh = cp.LAST_EV, cp.LAST_EH
s = cp_model.CpSolver(); s.parameters.num_workers = 1; s.parameters.max_time_in_seconds = tl
s.parameters.enumerate_all_solutions = True; s.parameters.cp_model_presolve = False
cb = CB(ev, eh); st = s.Solve(m, cb)
print('#', s.StatusName(st), 'solutions', cb.n, 'distinct pairs', len(cb.seen), file=sys.stderr)
