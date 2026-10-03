"""Potential as function of pending-edge features: singles + pairs (+ triples option). L1-minimal via GLOP."""
import sys, numpy as np
from itertools import combinations
sys.path.insert(0, 'gap/lowerbounds/simple_strip')
from nocyc_common import *
from ortools.linear_solver import pywraplp
k = int(sys.argv[1]); deg = int(sys.argv[2])
feats1 = sorted({e for s in bstates for e in s[1]})
F = [()]
for d in range(1, deg+1): F += list(combinations(feats1, d))
present = [frozenset(s[1]) for s in bstates]
Fs = [f for f in F if any(set(f) <= p for p in present)]
print('features', len(Fs))
def phi_terms(p): return [i for i, f in enumerate(Fs) if set(f) <= p]
T = [phi_terms(p) for p in present]
solver = pywraplp.Solver.CreateSolver('GLOP')
x = [solver.NumVar(-1000, 1000, f'x{i}') for i in range(len(Fs))]
ab = [solver.NumVar(0, 1000, f'a{i}') for i in range(len(Fs))]
for i in range(len(Fs)): solver.Add(ab[i] >= x[i]); solver.Add(ab[i] >= -x[i])
for u, v, W, m in rows:
    c = 4*W - 4 - 4*g_of(m, k)
    coef = {}
    for i in T[u]: coef[i] = coef.get(i, 0) + 1
    for i in T[v]: coef[i] = coef.get(i, 0) - 1
    solver.Add(c + sum(cf * x[i] for i, cf in coef.items() if cf) >= 0)
solver.Minimize(sum(ab[1:]))
st = solver.Solve(); print('status', st)
if st == 0:
    print('L1', solver.Objective().Value())
    for f, xi in zip(Fs, x):
        if abs(xi.solution_value()) > 1e-9: print(round(xi.solution_value(), 4), f)
