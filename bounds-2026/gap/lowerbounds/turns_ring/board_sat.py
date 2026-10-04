"""Full n x n board, CP-SAT: cells at depth >= W0 forced straight in field f (default (2,-1), W0=4); the rest free.
2-factor (no connectivity). Minimizes the number of turns T; prints T - 8n, the solver bound, and checks the
witness directly (degrees, symmetry of edges, turn count). Optional: interior window of size K at each corner freed.
usage: board_sat.py n [W0] [K] [tlimit]"""
import sys, json
from itertools import combinations
from ortools.sat.python import cp_model
M = [(dx, dy) for dx in (-2, -1, 1, 2) for dy in (-2, -1, 1, 2) if abs(dx) + abs(dy) == 3]
n = int(sys.argv[1]); W0 = int(sys.argv[2]) if len(sys.argv) > 2 else 4
K = int(sys.argv[3]) if len(sys.argv) > 3 else 0; TL = float(sys.argv[4]) if len(sys.argv) > 4 else 600
MIX = sys.argv[5] if len(sys.argv) > 5 else ''   # residues r of (x+2y) mod 4 that use field A=(2,-1); others use (2,1)
DIRS = {'A': (2, -1), 'D': (2, 1), 'B': (1, 2), 'C': (1, -2)}
def fmoves(p):
    # MIX forms: '' (pure A); 'R' digits (A/D, (x+2y) mod 4 in R -> A); 'F1F2:m:R' (inv_F1(p) mod m in R -> F1, else F2)
    if not MIX: return ((2, -1), (-2, 1))
    if ':' not in MIX:
        return ((2, -1), (-2, 1)) if (p[0] + 2 * p[1]) % 4 in {int(c) for c in MIX} else ((2, 1), (-2, -1))
    fam, mm, RR = MIX.split(':'); d1, d2 = DIRS[fam[0]], DIRS[fam[1]]
    d = d1 if (d1[1] * p[0] - d1[0] * p[1]) % int(mm) in {int(c) for c in RR} else d2
    return (d, (-d[0], -d[1]))
on = lambda p: 0 <= p[0] < n and 0 <= p[1] < n
depth = lambda p: min(p[0], p[1], n - 1 - p[0], n - 1 - p[1])
def inwindow(p):
    x, y = p
    return min(x, n - 1 - x) < K and min(y, n - 1 - y) < K
forced = lambda p: depth(p) >= W0 and not inwindow(p)
m = cp_model.CpModel(); X = {}; turn = []
cells = [(x, y) for x in range(n) for y in range(n)]
free = [p for p in cells if not forced(p)]
for p in free:
    must = {d for d in M if on((p[0]+d[0], p[1]+d[1])) and forced((p[0]+d[0], p[1]+d[1])) and (-d[0], -d[1]) in fmoves((p[0]+d[0], p[1]+d[1]))}
    allowed = [d for d in M if on((p[0]+d[0], p[1]+d[1])) and (not forced((p[0]+d[0], p[1]+d[1])) or d in must)]
    opts = []
    for a, b in combinations(allowed, 2):
        if not must <= {a, b}: continue
        v = m.NewBoolVar(''); X[p, a, b] = v; opts.append(v)
        if a[0] + b[0] != 0 or a[1] + b[1] != 0: turn.append(v)
    m.AddExactlyOne(opts)
fs = set(free); byp = {}
for (p, a, b), v in X.items(): byp.setdefault(p, []).append((a, b, v))
for p in free:
    for d in M:
        q = (p[0]+d[0], p[1]+d[1])
        if q in fs and p < q:
            m.Add(sum(v for a, b, v in byp[p] if d in (a, b)) == sum(v for a, b, v in byp[q] if (-d[0], -d[1]) in (a, b)))
m.Minimize(sum(turn))
s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = TL
st = s.Solve(m)
print('n', n, 'W0', W0, 'K', K, 'mix', MIX, s.StatusName(st), 'T-8n =', s.ObjectiveValue() - 8*n, 'bound', s.BestObjectiveBound() - 8*n, flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    mv = {p: (fmoves(p) if forced(p) else None) for p in cells}
    for (p, a, b), v in X.items():
        if s.Value(v): mv[p] = (a, b)
    T = 0
    for p in cells:
        a, b = mv[p]; assert a != b
        for d in (a, b):
            q = (p[0]+d[0], p[1]+d[1]); assert on(q) and (-d[0], -d[1]) in mv[q], (p, d)
        T += int(a[0]+b[0] != 0 or a[1]+b[1] != 0)
    print('witness check: degrees and symmetry OK; direct T - 8n =', T - 8*n, flush=True)
    json.dump({f'{x},{y}': mv[(x, y)] for x, y in cells}, open(f'/home/nil/nil/knight-formation-research/gap/lowerbounds/turns_ring/board_n{n}_W{W0}_K{K}_M{MIX.replace(':','-')}.json', 'w'))
