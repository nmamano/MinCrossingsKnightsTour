"""Sparsest potential for cost 2kappa(end)-4g: LP min sum |d|, integrality check."""
import sys, pickle, numpy as np
from collections import Counter
sys.path.insert(0, 'gap/lowerbounds/simple_strip')
from nocyc_common import *
from ortools.linear_solver import pywraplp
K = pickle.load(open('gap/lowerbounds/simple_strip/kappa.pkl', 'rb'))
k2 = np.array([int(2*K[v][0]) for v in range(len(bstates))])
k = int(sys.argv[1]); al = float(sys.argv[2]) if len(sys.argv) > 2 else 0
N = len(bstates)
solver = pywraplp.Solver.CreateSolver('GLOP')
d = [solver.NumVar(-100, 100, f'd{i}') for i in range(N)]
ab = [solver.NumVar(0, 100, f'a{i}') for i in range(N)]
for i in range(N): solver.Add(ab[i] >= d[i]); solver.Add(ab[i] >= -d[i])
for u, v, W, m in rows:
    c = al*k2[u] + (1-al)*k2[v] - 4*g_of(m, k)
    if u == v:
        assert c >= 0; continue
    solver.Add(c + d[u] - d[v] >= 0)
solver.Minimize(sum(ab))
print('status', solver.Solve())
x = np.array([v.solution_value() for v in d])
print('L1', solver.Objective().Value(), 'support', int((np.abs(x) > 1e-7).sum()), 'values', Counter(np.round(x, 3)).most_common(10))
np.save(f'gap/lowerbounds/simple_strip/sparse_{k}_{al}.npy', x)
