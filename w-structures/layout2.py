"""Free-fold layout search with line tracing (KT Structures, 2026-10-02).

Board [0,k]^2 = k x k squares, each cut by both diagonals into triangles S, E, N, W.
Each triangle gets a family: A (dir (2,-1)), A' (2,1), B (1,-2), B' (1,2).
Only FREE folds are allowed between different families (LB F3):
  horizontal A|A', vertical B|B', slope +1 A'|B', slope -1 A|B.
All four board edges steep: left/right triangles in {A, A'}, bottom/top triangles in {B, B'}.
So the interior has 0 crossings and every edge costs 1 per unit (pattern P).
For each layout: trace lines (continuous geometry) from sample points on all edges and measure
the edge length whose lines return to the SAME edge (chevrons and other same-edge nests).
Same-edge 1-fold nests are always trapped (LB F10d); the arch-flip fix costs 1/2 per unit of
trapped edge length, so arch cost (units of n) = L_same / (2k).
usage: layout2.py k [M]
"""
import sys, math
from collections import Counter
from ortools.sat.python import cp_model

A, Ap, B, Bp = 0, 1, 2, 3
NAMES = ['A', "A'", 'B', "B'"]
DIR = {A: (2, -1), Ap: (2, 1), B: (1, -2), Bp: (1, 2)}
FREE = {'h': {(A, Ap)}, 'v': {(B, Bp)}, 'd': {(Ap, Bp)}, 'a': {(A, B)}}
S, E, N, W = 0, 1, 2, 3


def ok(kind, a, b):
    return a == b or (min(a, b), max(a, b)) in FREE[kind]


def boundaries(k):
    out = []
    for i in range(k):
        for j in range(k):
            out += [((i, j, S), (i, j, E), 'a'), ((i, j, E), (i, j, N), 'd'),
                    ((i, j, N), (i, j, W), 'a'), ((i, j, W), (i, j, S), 'd')]
            if i + 1 < k:
                out.append(((i, j, E), (i + 1, j, W), 'v'))
            if j + 1 < k:
                out.append(((i, j, N), (i, j + 1, S), 'h'))
    return out


def enumerate_layouts(k, limit=10 ** 6):
    m = cp_model.CpModel()
    L = {}
    for i in range(k):
        for j in range(k):
            for t in range(4):
                L[i, j, t] = m.NewIntVar(0, 3, '')
    for (c1, c2, kind) in boundaries(k):
        allowed = [(a, b) for a in range(4) for b in range(4) if ok(kind, a, b)]
        m.AddAllowedAssignments([L[c1], L[c2]], allowed)
    for j in range(k):
        m.AddAllowedAssignments([L[0, j, W]], [(A,), (Ap,)])
        m.AddAllowedAssignments([L[k - 1, j, E]], [(A,), (Ap,)])
    for i in range(k):
        m.AddAllowedAssignments([L[i, 0, S]], [(B,), (Bp,)])
        m.AddAllowedAssignments([L[i, k - 1, N]], [(B,), (Bp,)])
    sols = []

    class CB(cp_model.CpSolverSolutionCallback):
        def on_solution_callback(self):
            sols.append({key: self.Value(v) for key, v in L.items()})
            if len(sols) >= limit:
                self.StopSearch()
    s = cp_model.CpSolver()
    s.parameters.enumerate_all_solutions = True
    s.parameters.num_workers = 1
    s.Solve(m, CB())
    return sols


def tri_of(p, k):
    x, y = p
    if not (0 < x < k and 0 < y < k):
        return None
    i, j = min(int(x), k - 1), min(int(y), k - 1)
    dx, dy = x - (i + .5), y - (j + .5)
    if dy <= -abs(dx):
        return (i, j, S)
    if dy >= abs(dx):
        return (i, j, N)
    return (i, j, E) if dx > 0 else (i, j, W)


def tri_edges(t):
    i, j, s = t
    c = (i + .5, j + .5)
    cs = {S: ((i, j), (i + 1, j)), E: ((i + 1, j), (i + 1, j + 1)),
          N: ((i + 1, j + 1), (i, j + 1)), W: ((i, j + 1), (i, j))}[s]
    a, b = cs
    return [(a, b), (b, c), (c, a)]


def exit_point(p, d, t):
    best = None
    for (a, b) in tri_edges(t):
        ex, ey = b[0] - a[0], b[1] - a[1]
        den = d[0] * (-ey) - d[1] * (-ex)
        if abs(den) < 1e-15:
            continue
        rx, ry = a[0] - p[0], a[1] - p[1]
        tt = (rx * (-ey) - ry * (-ex)) / den
        ss = (d[0] * ry - d[1] * rx) / den
        if tt > 1e-12 and -1e-9 <= ss <= 1 + 1e-9:
            if best is None or tt < best:
                best = tt
    return (p[0] + best * d[0], p[1] + best * d[1])


def edge_of(p, k):
    x, y = p
    e = 1e-6
    if x < e: return 'L'
    if x > k - e: return 'R'
    if y < e: return 'B'
    if y > k - e: return 'T'
    return None


def trace(lab, k, p, maxsteps=10000):
    """p on the board boundary. Returns (exit edge, exit point, folds) or None."""
    eps = 1e-7
    # step inside
    x, y = p
    inward = (1, 0) if x < 1e-9 else (-1, 0) if x > k - 1e-9 else (0, 1) if y < 1e-9 else (0, -1)
    t = tri_of((x + eps * inward[0], y + eps * inward[1]), k)
    f = lab[t]
    d = DIR[f]
    if d[0] * inward[0] + d[1] * inward[1] < 0:
        d = (-d[0], -d[1])
    folds = 0
    for _ in range(maxsteps):
        q = exit_point(p, d, t)
        nxt = tri_of((q[0] + eps * d[0], q[1] + eps * d[1]), k)
        if nxt is None:
            return edge_of(q, k), q, folds
        g = lab[nxt]
        if g != f:
            folds += 1
            d2 = DIR[g]
            for sg in (1, -1):
                dd = (sg * d2[0], sg * d2[1])
                if tri_of((q[0] + eps * dd[0], q[1] + eps * dd[1]), k) == nxt:
                    d = dd
                    break
            else:
                return None
            f = g
        p, t = q, nxt
    return None


def evaluate(lab, k, M=40):
    off = 0.2718281828 / M
    same, same_multi, bad, total = 0.0, 0.0, 0, 0
    per_edge = Counter()
    for side in 'LRBT':
        for m_ in range(M * k):
            s = (m_ + 0.5) / M + off
            p = {'L': (0.0, s), 'R': (float(k), s), 'B': (s, 0.0), 'T': (s, float(k))}[side]
            r = trace(lab, k, p)
            total += 1
            if r is None:
                bad += 1
                continue
            e, q, folds = r
            if e == side:
                same += 1.0 / M
                per_edge[side] += 1.0 / M
                if folds != 1:
                    same_multi += 1.0 / M
    return dict(arch=same / (2 * k), same_len=same, multi=same_multi, bad=bad, per_edge=dict(per_edge))


def show(lab, k):
    rows = []
    for j in reversed(range(k)):
        rows.append(' '.join('%s/%s/%s/%s' % tuple(NAMES[lab[i, j, t]] for t in (S, E, N, W)) for i in range(k)))
    return '\n'.join(rows)


if __name__ == '__main__':
    k = int(sys.argv[1]); M = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    sols = enumerate_layouts(k)
    print(f'k={k}: {len(sols)} free-fold layouts with all edges steep', flush=True)
    res = []
    for lab in sols:
        r = evaluate(lab, k, M)
        res.append((r['arch'], r['bad'], r, lab))
    res.sort(key=lambda z: (z[1] > 0, z[0]))
    hist = Counter(round(z[0], 3) for z in res if z[1] == 0)
    print('arch cost histogram (units of n, layouts with all traces ok):', sorted(hist.items())[:15])
    print('layouts with failed traces:', sum(1 for z in res if z[1]))
    for a, b, r, lab in res[:3]:
        print('arch', round(a, 4), r)
        print(show(lab, k))
