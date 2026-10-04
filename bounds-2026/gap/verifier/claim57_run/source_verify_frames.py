"""Check the corner/side frames of corner_pot.py on a real ring solution (W-ring, n, arms A):
 ring cost = sum of 4 corner costs + sum of side row costs; each corner's vertical-cut state s and the next corner's
 horizontal-cut state t (local frame) satisfy: G-frame state at the far cut of the side == sigma(t).
 Also checks the potential identity: ring cost = sum_k [corner_k cost - h(s_k) + h(sigma t_k)] + sum sides [cost + h(s)-h(end)]
 for a random h.  usage: verify_frames.py n W A [states.bin]"""
import sys, random
from itertools import combinations
import numpy as np
from ortools.sat.python import cp_model
import corner_pot as cp
n, W, A = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
M = cp.M; lower = cp.lower
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
s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = 40; s.parameters.random_seed = int(sys.argv[5]) if len(sys.argv) > 5 else 0
st = s.Solve(m); print('ring solve', s.StatusName(st), s.ObjectiveValue())
ch = {p: next((a, b) for a, b, v in byp[p] if s.Value(v)) for p in cells}
S = cp.slots_of(W); sg = cp.sigma_perm(S); K = len(S)
rot = lambda p: (p[1], n - 1 - p[0])           # rho: BL -> TL, clockwise
def R(p, k):
    for _ in range(k): p = rot(p)
    return p
def Rv(d, k):
    for _ in range(k): d = (d[1], -d[0])
    return d
uses = lambda p, d: d in ch[p]
def vstate(k):   # corner k's vertical cut state, corner k = R^k(BL)
    return sum(1 << i for i, (x0, y0, x1, y1) in enumerate(S) if uses(R((x0, A + y0), k), Rv((x1 - x0, y1 - y0), k)))
def hstate(k):   # corner k's horizontal cut state, local frame
    return sum(1 << i for i, (x0, y0, x1, y1) in enumerate(S) if uses(R((A + y0, x0), k), Rv((y1 - y0, x1 - x0), k)))
def gstate(k, c):  # state at G-cut c on side k (side k leaves corner k's vertical arm), G frame rotated by k
    return sum(1 << i for i, (x0, y0, x1, y1) in enumerate(S) if uses(R((x0, c + y0), k), Rv((x1 - x0, y1 - y0), k)))
sig = lambda t: sum(1 << sg[j] for j in range(K) if t >> j & 1)
corner_cells = lambda k: [R((x, y), k) for x in range(A) for y in range(A) if min(x, y) < W]
tot = sum(r(p, *ch[p]) for p in cells); cc = [sum(r(p, *ch[p]) for p in corner_cells(k)) for k in range(4)]
side = [sum(r(R((x, y), k), *ch[R((x, y), k)]) for x in range(W) for y in range(A, n - A)) for k in range(4)]
print('total', tot, 'corners', cc, 'sides', side, 'sum', sum(cc) + sum(side))
ok = True
for k in range(4):
    s0, s1 = vstate(k), gstate(k, A); t = hstate((k + 1) % 4); e = gstate(k, n - A)
    print('corner', k, 'vstate==G(A)', s0 == s1, 'G(n-A)==sigma(t_next)', e == sig(t)); ok &= s0 == s1 and e == sig(t)
if len(sys.argv) > 4:
    stset = set(np.fromfile(sys.argv[4], dtype=np.uint64).tolist())
    for k in range(4):
        ins = [gstate(k, c) in stset for c in range(A, n - A + 1)]; print('side', k, 'all cut states in G:', all(ins)); ok &= all(ins)
print('ALL OK' if ok and tot == sum(cc) + sum(side) else 'MISMATCH')
if len(sys.argv) > 6:   # potential file: check side inequalities and corner reduced costs on this solution
    t = [int(x) for x in open(sys.argv[6]).read().split()]; sc, w = t[0], t[1:]
    h = lambda st: sum(w[i] for i in range(K) if st >> i & 1)
    for k in range(4):
        s0, e = gstate(k, A), gstate(k, n - A)
        print('side', k, 'S*cost', sc * side[k], '>= h(end)-h(start)', h(e) - h(s0), sc * side[k] >= h(e) - h(s0))
        red = sc * cc[k] - h(vstate(k)) + h(sig(hstate(k)))
        print('corner', k, 'reduced (scaled)', red)
