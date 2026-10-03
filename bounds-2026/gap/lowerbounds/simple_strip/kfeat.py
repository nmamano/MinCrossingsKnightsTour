"""Potential psi(cut) as polynomial in pending-edge indicators for cost 2kappa(end) - 4g (+ alpha mix). L1 minimal."""
import sys, pickle, numpy as np
from itertools import combinations
sys.path.insert(0, 'gap/lowerbounds/simple_strip')
from nocyc_common import *
from ortools.linear_solver import pywraplp
K = pickle.load(open('gap/lowerbounds/simple_strip/kappa.pkl', 'rb'))
k2 = [int(2*K[v][0]) for v in range(len(bstates))]
k = int(sys.argv[1]); deg = int(sys.argv[2]); al = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
feats1 = sorted({e for s in bstates for e in s[1]})
F = []
for d in range(1, deg+1): F += list(combinations(feats1, d))
present = [frozenset(s[1]) for s in bstates]
Fs = [f for f in F if any(set(f) <= p for p in present)]
T = [[i for i, f in enumerate(Fs) if set(f) <= p] for p in present]
solver = pywraplp.Solver.CreateSolver('GLOP')
x = [solver.NumVar(-1000, 1000, f'x{i}') for i in range(len(Fs))]
ab = [solver.NumVar(0, 1000, f'a{i}') for i in range(len(Fs))]
for i in range(len(Fs)): solver.Add(ab[i] >= x[i]); solver.Add(ab[i] >= -x[i])
seen = {}
for u, v, W, m in rows:
    c = al*k2[u] + (1-al)*k2[v] - 4*g_of(m, k)
    if c >= 0 and set(T[u]) == set(T[v]): continue
    key = (u, v); seen[key] = min(seen.get(key, 1e9), c)
for (u, v), c in seen.items():
    coef = {}
    for i in T[u]: coef[i] = coef.get(i, 0) + 1
    for i in T[v]: coef[i] = coef.get(i, 0) - 1
    solver.Add(c + sum(cf * x[i] for i, cf in coef.items() if cf) >= 0)
solver.Minimize(sum(ab))
st = solver.Solve(); print('deg', deg, 'alpha', al, 'features', len(Fs), 'status', st)
if st == 0:
    print('L1', solver.Objective().Value())
    for f, xi in zip(Fs, x):
        if abs(xi.solution_value()) > 1e-9: print(round(xi.solution_value(), 4), f)
