"""CP-SAT: ring of width W (cells at depth < W) on the n x n board; moves into deeper cells are FREE (not modelled).
Minimizes sum r over ring cells (r = t - sum of side L). This is the free-interior relaxation of task L1.
usage: ring_free_sat.py n W tlimit"""
import sys
from itertools import combinations
from ortools.sat.python import cp_model
M = [(dx, dy) for dx in (-2, -1, 1, 2) for dy in (-2, -1, 1, 2) if abs(dx) + abs(dy) == 3]
def lower(x, dxs):
    if x == 0: return 1
    if x in (1, 2): return sum(x + d in (0, 3) for d in dxs) - 1
    if x == 3: return 1 - sum(x + d in (1, 2) for d in dxs)
    return 0
n, W, TL = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
on = lambda p: 0 <= p[0] < n and 0 <= p[1] < n
depth = lambda p: min(p[0], p[1], n - 1 - p[0], n - 1 - p[1])
def r(p, a, b):
    x, y = p; t = int(a[0] + b[0] != 0 or a[1] + b[1] != 0)
    return t - lower(x, [a[0], b[0]]) - lower(n-1-x, [-a[0], -b[0]]) - lower(y, [a[1], b[1]]) - lower(n-1-y, [-a[1], -b[1]])
cells = [(x, y) for x in range(n) for y in range(n) if depth((x, y)) < W]; cs = set(cells)
m = cp_model.CpModel(); byp = {}; obj = []
for p in cells:
    opts = []
    for a, b in combinations([d for d in M if on((p[0]+d[0], p[1]+d[1]))], 2):
        v = m.NewBoolVar(''); byp.setdefault(p, []).append((a, b, v)); opts.append(v); obj.append(r(p, a, b) * v)
    m.AddExactlyOne(opts)
for p in cells:
    for d in M:
        q = (p[0]+d[0], p[1]+d[1])
        if q in cs and p < q:
            m.Add(sum(v for a, b, v in byp[p] if d in (a, b)) == sum(v for a, b, v in byp[q] if (-d[0], -d[1]) in (a, b)))
m.Minimize(sum(obj))
s = cp_model.CpSolver(); s.parameters.num_workers = int(sys.argv[4]) if len(sys.argv) > 4 else 2; s.parameters.max_time_in_seconds = TL; s.parameters.cp_model_presolve = False
st = s.Solve(m)
print('free-interior ring n', n, 'W', W, s.StatusName(st), 'min sum r =', s.ObjectiveValue(), 'bound', s.BestObjectiveBound(), flush=True)
