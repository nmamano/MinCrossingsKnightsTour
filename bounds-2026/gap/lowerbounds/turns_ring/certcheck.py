"""Re-solve the corner at a fixed integer potential (file 'S w0..w27') with several solver settings.
usage: certcheck.py W A wfile tl"""
import sys
from ortools.sat.python import cp_model
import corner_pot as cp
W, A, wf, tl = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], float(sys.argv[4])
t = [int(x) for x in open(wf).read().split()]; sc, w = t[0], t[1:]
for presolve in (False, True):
    for seed in (0, 7):
        m, c, phi, S = cp.build(W, A)
        m.Minimize(sc * c + sum(wk * f for wk, f in zip(w, phi)))
        s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = tl
        s.parameters.cp_model_presolve = presolve; s.parameters.random_seed = seed
        st = s.Solve(m)
        print(f'A {A} presolve {presolve} seed {seed}: {s.StatusName(st)} value {s.ObjectiveValue()}/{sc} bound {s.BestObjectiveBound()}/{sc} cost {s.Value(c)}', flush=True)
