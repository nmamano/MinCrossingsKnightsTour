"""Corner of the W-ring relaxation with a side potential h(s) = sum_k w_k [slot k in s] (linear in the cut slots).
Corner region (corner at origin): cells with min(x,y) < W and max(x,y) < A; moves to other cells are free.
Vertical arm cut (y = A): state s in the strip frame (depth x, rows y). Horizontal arm cut (x = A): state t in its
local strip frame (depth y, rows x). Ring order: each corner's vertical arm is the source of the next side, its
horizontal arm the target of the previous side, so (proof, see L1.md) the reduced corner cost is
    cost - h(s) + h(sigma(t)),   sigma = row mirror,  slot (x0,y0,x1,y1) -> (x1,-1-y1,x0,-1-y0),
and T - 8n >= R_W(n) >= 4 * min(reduced corner cost) for every n >= 2A, whenever h is valid on the side strip graph
(c(u,v) + h(u) - h(v) >= 0 on every arc; checked by stripz with WFILE).
API: solve(W, A, wint, scale, tl, workers) -> (status, value_scaled, bound_scaled, list of (cost, phi)) where
phi[k] = [slot sigma^-1... ] incidence vector: reduced = cost + sum_k w_k phi_k."""
import sys
from itertools import combinations
from ortools.sat.python import cp_model
M = [(dx, dy) for dx in (-2, -1, 1, 2) for dy in (-2, -1, 1, 2) if abs(dx) + abs(dy) == 3]
MV = [(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)]
def lower(x, dxs):
    if x == 0: return 1
    if x in (1, 2): return sum(x + d in (0, 3) for d in dxs) - 1
    if x == 3: return 1 - sum(x + d in (1, 2) for d in dxs)
    return 0
def slots_of(W):  # same order as stripz.cpp
    S = []
    for y0 in (-2, -1):
        for x0 in range(W):
            for dx, dy in MV:
                x1, y1 = x0 + dx, y0 + dy
                if dy > 0 and 0 <= x1 < W and y1 >= 0: S.append((x0, y0, x1, y1))
    return S
def sigma_perm(S):
    idx = {s: i for i, s in enumerate(S)}
    return [idx[(x1, -1 - y1, x0, -1 - y0)] for (x0, y0, x1, y1) in S]
def build(W, A):
    S = slots_of(W); sg = sigma_perm(S)
    r = lambda p, a, b: int(a[0] + b[0] != 0 or a[1] + b[1] != 0) - lower(p[0], [a[0], b[0]]) - lower(p[1], [a[1], b[1]])
    cells = [(x, y) for x in range(A) for y in range(A) if min(x, y) < W]; cs = set(cells)
    m = cp_model.CpModel(); byp = {}; cost = []
    for p in cells:
        opts = []
        for a, b in combinations([d for d in M if p[0]+d[0] >= 0 and p[1]+d[1] >= 0], 2):
            v = m.NewBoolVar(''); byp.setdefault(p, []).append((a, b, v)); opts.append(v); cost.append(r(p, a, b) * v)
        m.AddExactlyOne(opts)
    for p in cells:
        for d in M:
            q = (p[0]+d[0], p[1]+d[1])
            if q in cs and p < q:
                m.Add(sum(v for a, b, v in byp[p] if d in (a, b)) == sum(v for a, b, v in byp[q] if (-d[0], -d[1]) in (a, b)))
    use = lambda p, d: sum(v for a, b, v in byp[p] if d in (a, b))
    ev = [use((x0, A + y0), (x1 - x0, y1 - y0)) for (x0, y0, x1, y1) in S]           # vertical cut, strip frame
    eh = [use((A + y0, x0), (y1 - y0, x1 - x0)) for (x0, y0, x1, y1) in S]           # horizontal cut, local frame
    # phi_k: coefficient of w_k.  -[k in s] + [k in sigma(t)];  sigma(t) contains slot sg[j] iff t contains j
    phi = [None] * len(S)
    for k in range(len(S)): phi[k] = -ev[k]
    for j in range(len(S)): phi[sg[j]] = phi[sg[j]] + eh[j]
    global LAST_EV, LAST_EH; LAST_EV, LAST_EH = ev, eh
    return m, sum(cost), phi, S
class CB(cp_model.CpSolverSolutionCallback):
    def __init__(s, c, phi): super().__init__(); s.c, s.phi, s.sols = c, phi, []
    def on_solution_callback(s): s.sols.append((int(s.Value(s.c)), [int(s.Value(f)) for f in s.phi]))
def solve(W, A, wint, scale, tl, workers=2, hint=None):
    m, c, phi, S = build(W, A)
    m.Minimize(scale * c + sum(wk * f for wk, f in zip(wint, phi)))
    s = cp_model.CpSolver(); s.parameters.num_workers = workers; s.parameters.max_time_in_seconds = tl
    s.parameters.cp_model_presolve = False
    cb = CB(c, phi); st = s.Solve(m, cb)
    return s.StatusName(st), s.ObjectiveValue(), s.BestObjectiveBound(), cb.sols
if __name__ == '__main__':
    W, A, tl = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
    S = slots_of(W)
    w = [0] * len(S); scale = 1
    if len(sys.argv) > 4: w = [int(t) for t in open(sys.argv[4]).read().split()]; scale = int(sys.argv[5])
    st, val, bd, sols = solve(W, A, w, scale, tl)
    print('corner W', W, 'A', A, st, 'value', val / scale, 'bound', bd / scale, 'sols', len(sols), 'best cost', sols[-1][0] if sols else None)
