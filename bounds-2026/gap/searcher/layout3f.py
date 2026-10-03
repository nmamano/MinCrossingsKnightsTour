"""Layout search with costed seams (KT Structures, 2026-10-02). Extends layout2.py.
Allowed boundaries: free folds (cost 0) and the measured non-free seams (S1, lane-free):
  A|A' vertical 1.0 per unit y, B|B' horizontal 1.0 per unit x,
  A|B on slope +1 (gentle) 1.0 per unit x, A'|B' on slope -1 (gentle) 1.0 per unit x.
Board edges: steep family 1.0 per unit, shallow family 2.6 per unit (LB F1b, k=3).
Lines are traced through free folds only; a line that meets a seam is treated as rewired (not trapped).
Score (units of n) = edges + seams + arch, arch = same-edge free-fold length / 2.
usage: layout3.py k bound [M]   (enumerate layouts with edges + seams <= bound, then trace)"""
import sys
from collections import Counter
from ortools.sat.python import cp_model
import os
SH = int(os.environ.get('SH', '260'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'w-structures'))
import layout2 as L2
from layout2 import A, Ap, B, Bp, S, E, N, W, DIR, NAMES

SEAM = {'v': {(A, Ap): 1.0}, 'h': {(B, Bp): 1.0}, 'd': {(A, B): 1.0}, 'a': {(Ap, Bp): 1.0}}
XLEN = {'v': 1.0, 'h': 1.0, 'd': 0.5, 'a': 0.5}   # projected length of one grid boundary piece

def bcost(kind, a, b):
    if L2.ok(kind, a, b):
        return 0.0
    return SEAM[kind].get((min(a, b), max(a, b)))

def enumerate_layouts(k, bound, limit=200000):
    m = cp_model.CpModel()
    Lv = {}
    for i in range(k):
        for j in range(k):
            for t in range(4):
                Lv[i, j, t] = [m.NewBoolVar('') for _ in range(4)]
                m.AddExactlyOne(Lv[i, j, t])
    obj = []
    for (c1, c2, kind) in L2.boundaries(k):
        for a in range(4):
            for b in range(4):
                c = bcost(kind, a, b)
                if c is None:
                    m.AddBoolOr([Lv[c1][a].Not(), Lv[c2][b].Not()])
                elif c > 0:
                    z = m.NewBoolVar('')
                    m.AddBoolOr([Lv[c1][a].Not(), Lv[c2][b].Not(), z])
                    obj.append(int(round(100 * c * XLEN[kind])) * z)
    for j in range(k):
        for t in (Lv[0, j, W], Lv[k - 1, j, E]):
            obj += [100 * t[A], 100 * t[Ap], SH * t[B], SH * t[Bp]]
    for i in range(k):
        for t in (Lv[i, 0, S], Lv[i, k - 1, N]):
            obj += [100 * t[B], 100 * t[Bp], SH * t[A], SH * t[Ap]]
    m.Add(sum(obj) <= int(round(100 * bound * k)))
    sols = []
    class CB(cp_model.CpSolverSolutionCallback):
        def on_solution_callback(self):
            lab = {key: max(range(4), key=lambda f: self.Value(v[f])) for key, v in Lv.items()}
            sols.append((self.Value(sum(obj)) / (100.0 * k), lab))
            if len(sols) >= limit: self.StopSearch()
    s = cp_model.CpSolver(); s.parameters.enumerate_all_solutions = True; s.parameters.num_workers = 1
    s.Solve(m, CB())
    return sols

def trace(lab, k, p, maxsteps=10000):
    eps = 1e-7
    x, y = p
    inward = (1, 0) if x < 1e-9 else (-1, 0) if x > k - 1e-9 else (0, 1) if y < 1e-9 else (0, -1)
    t = L2.tri_of((x + eps * inward[0], y + eps * inward[1]), k)
    f = lab[t]; d = DIR[f]
    if d[0] * inward[0] + d[1] * inward[1] < 0: d = (-d[0], -d[1])
    folds = 0
    for _ in range(maxsteps):
        q = L2.exit_point(p, d, t)
        nxt = L2.tri_of((q[0] + eps * d[0], q[1] + eps * d[1]), k)
        if nxt is None:
            return L2.edge_of(q, k), folds
        g = lab[nxt]
        if g != f:
            kind = boundary_kind(t, nxt)
            if not L2.ok(kind, f, g):
                return 'seam', folds
            folds += 1
            d2 = DIR[g]
            for sg in (1, -1):
                dd = (sg * d2[0], sg * d2[1])
                if L2.tri_of((q[0] + eps * dd[0], q[1] + eps * dd[1]), k) == nxt:
                    d = dd; break
            else:
                return None
            f = g
        p, t = q, nxt
    return None

def boundary_kind(t1, t2):
    (i, j, s), (i2, j2, s2) = t1, t2
    if (i, j) == (i2, j2):
        return 'd' if {s, s2} in ({E, N}, {W, S}) else 'a'
    return 'v' if i != i2 else 'h'

def arch(lab, k, M):
    off = 0.2718281828 / M; same = 0.0; bad = 0
    for side in 'LRBT':
        for m_ in range(M * k):
            s = (m_ + 0.5) / M + off
            p = {'L': (0.0, s), 'R': (float(k), s), 'B': (s, 0.0), 'T': (s, float(k))}[side]
            r = trace(lab, k, p)
            if r is None: bad += 1; continue
            if r[0] == side: same += 1.0 / M
    return same / (2 * k), bad

if __name__ == '__main__':
    k, bound = int(sys.argv[1]), float(sys.argv[2]); M = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    sols = enumerate_layouts(k, bound)
    print(f'k={k}: {len(sols)} layouts with edges+seams <= {bound}', flush=True)
    res = []
    def steepcorners(lab):
        cs = [((0, 0, S), (0, 0, W)), ((k - 1, 0, S), (k - 1, 0, E)), ((0, k - 1, N), (0, k - 1, W)), ((k - 1, k - 1, N), (k - 1, k - 1, E))]
        return sum(1 for hb, vb in cs if lab[hb] in (B, Bp) and lab[vb] in (A, Ap))
    for c, lab in sols:
        a, bad = arch(lab, k, M)
        fc = steepcorners(lab)
        res.append((c + a + fc / 3.0, c, a, fc, bad, lab))
    res.sort(key=lambda z: z[0])
    print('best totals with flux n/3 per steep-steep corner (total, edges+seams, arch, steep corners, bad):')
    seen = set()
    for z in res[:40]:
        key = tuple(round(v, 3) for v in z[:5])
        if key in seen: continue
        seen.add(key); print('  ', key)
    for z in res[:3]:
        print(L2.show(z[5], k))
