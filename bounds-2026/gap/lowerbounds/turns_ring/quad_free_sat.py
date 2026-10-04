"""CP-SAT: one corner of the W-ring relaxation. Quadrant x,y >= 0; region = cells with min(x,y) < W and max(x,y) < A
(arms of length A, free ends). Moves to cells outside the region are free. Minimizes sum r (corner L terms only).
usage: quad_free_sat.py W A tlimit workers"""
import sys
from itertools import combinations
from ortools.sat.python import cp_model
M = [(dx, dy) for dx in (-2, -1, 1, 2) for dy in (-2, -1, 1, 2) if abs(dx) + abs(dy) == 3]
def lower(x, dxs):
    if x == 0: return 1
    if x in (1, 2): return sum(x + d in (0, 3) for d in dxs) - 1
    if x == 3: return 1 - sum(x + d in (1, 2) for d in dxs)
    return 0
W, A, TL, NW = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
def r(p, a, b):
    t = int(a[0] + b[0] != 0 or a[1] + b[1] != 0)
    return t - lower(p[0], [a[0], b[0]]) - lower(p[1], [a[1], b[1]])
cells = [(x, y) for x in range(A) for y in range(A) if min(x, y) < W]; cs = set(cells)
m = cp_model.CpModel(); byp = {}; obj = []
for p in cells:
    opts = []
    for a, b in combinations([d for d in M if p[0]+d[0] >= 0 and p[1]+d[1] >= 0], 2):
        v = m.NewBoolVar(''); byp.setdefault(p, []).append((a, b, v)); opts.append(v); obj.append(r(p, a, b) * v)
    m.AddExactlyOne(opts)
for p in cells:
    for d in M:
        q = (p[0]+d[0], p[1]+d[1])
        if q in cs and p < q:
            m.Add(sum(v for a, b, v in byp[p] if d in (a, b)) == sum(v for a, b, v in byp[q] if (-d[0], -d[1]) in (a, b)))
m.Minimize(sum(obj))
s = cp_model.CpSolver(); s.parameters.num_workers = NW; s.parameters.max_time_in_seconds = TL; s.parameters.cp_model_presolve = False
st = s.Solve(m)
print('quadrant W', W, 'arm', A, s.StatusName(st), 'min sum r =', s.ObjectiveValue(), 'bound', s.BestObjectiveBound(), flush=True)
