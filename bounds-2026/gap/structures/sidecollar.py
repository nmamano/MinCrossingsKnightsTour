"""C2 (PLAN.md): price of a side next to a ribbon field with an arbitrary ribbon word. KT Structures, 2026-10-03.
Left strip x in [0, D) free (degree 2, any knight move, cycles allowed = relaxation, so values are lower bounds),
period p rows. Exterior x >= D: '/' ribbon field with periodic word w (ribbon k = y - x mod q, H = (2,1), V = (1,2));
every field edge with an endpoint at x >= D is fixed. Minimum crossings per period (OPTIMAL = exact in this model).
Baseline: all-H word -> P, 1 per row. Reports the excess per V ribbon end (one ribbon end per row at the strip).
usage: python sidecollar.py D qmax [time]
"""
import sys, itertools
from collections import defaultdict
from ortools.sat.python import cp_model
from classphase import cross, KM

def field_edges(w, xlo, xhi, ylo, yhi):
    q = len(w); out = []
    for x in range(xlo, xhi):
        for y in range(ylo, yhi):
            if w[(y - x) % q] == 'H': out.append(((x, y), (x+2, y+1)))
            if w[(y - x + 1) % q] == 'V': out.append(((x, y), (x+1, y+2)))
    return out

def solve(w, D, p, tlim=60):
    cells = [(x, y) for x in range(D) for y in range(p)]
    wrap = lambda c: (c[0], c[1] % p)
    cand = []
    for (x, y) in cells:
        for dx, dy in KM:
            r = (x+dx, y+dy)
            if 0 <= r[0] < D and (dy > 0 or (dy == 0 and dx > 0)):
                cand.append(((x, y), r))
    fixed = [e for e in field_edges(w, D-3, D+4, 0, p) if max(e[0][0], e[1][0]) >= D]
    fdeg = defaultdict(int)
    for e in fixed:
        for c in e:
            if c[0] < D: fdeg[wrap(c)] += 1
    m = cp_model.CpModel(); X = {e: m.NewBoolVar('') for e in cand}
    inc = defaultdict(list)
    for e in cand: inc[wrap(e[0])].append(X[e]); inc[wrap(e[1])].append(X[e])
    for c in cells:
        if fdeg[c] > 2: return None
        m.Add(sum(inc[c]) == 2 - fdeg[c])
    tr = lambda e, t: ((e[0][0], e[0][1]+t), (e[1][0], e[1][1]+t))
    obj = []
    for i, e in enumerate(cand):
        for j, f in enumerate(cand):
            for k in range(0, 3):
                if k == 0 and j <= i: continue
                if cross(e, tr(f, k*p)):      # orbit pairs: k = 0 with i < j, k > 0 with all (i, j)
                    z = m.NewBoolVar(''); m.Add(z >= X[e] + X[f] - 1); obj.append(z)
    for e in cand:
        for f in fixed:
            for k in range(-2, 3):
                if cross(e, tr(f, k*p)): obj.append(X[e])
    m.Minimize(sum(obj))
    s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = tlim
    st = s.Solve(m)
    if st == cp_model.INFEASIBLE: return ('INFEASIBLE', None, None)
    return (s.StatusName(st), s.ObjectiveValue(), s.BestObjectiveBound())

def words(q):
    seen = set()
    for t in itertools.product('HV', repeat=q):
        w = ''.join(t)
        if any(w == w[:d] * (q // d) for d in range(1, q) if q % d == 0): continue   # primitive only
        r = min(w[i:] + w[:i] for i in range(q))
        if r not in seen: seen.add(r); yield r

if __name__ == '__main__':
    D, qmax = int(sys.argv[1]), int(sys.argv[2]); tl = float(sys.argv[3]) if len(sys.argv) > 3 else 60
    print(f'D={D}  word  p  status  crossings/period  per row  excess per V end', flush=True)
    for q in range(1, qmax + 1):
        for w in words(q):
            p = 2 * q * int(sys.argv[4]) if len(sys.argv) > 4 else (q if q % 2 == 0 else 2 * q)
            r = solve(w, D, p, tl)
            if r is None: print(f'{w:8s} p={p} field degree > 2 at strip'); continue
            st, val, bd = r
            nv = w.count('V') * p // q
            ex = (bd - p) / nv if (val is not None and nv) else None
            print(f'{w:8s} p={p:2d} {st:10s} {val} (bound {bd}) per row {None if val is None else round(bd/p,3)} '
                  f'excess/Vend {None if ex is None else round(ex,3)}', flush=True)
