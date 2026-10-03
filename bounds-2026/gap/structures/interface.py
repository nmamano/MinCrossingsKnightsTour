"""C3 (PLAN.md): tension of a straight defect line between two ribbon fields. KT Structures, 2026-10-03.

Plane, period vector T (along the line), level function h(c) = hv . c with hv . T = 0, hv primitive.
Band: cells with -a <= h <= a are free (degree 2, any knight move, cycles allowed = relaxation, so every value is a
LOWER bound in this model). Side 1 (h < -a) carries ribbon field F1, side 2 (h > a) carries F2; every field edge with
an endpoint on its side is fixed. A field = (split, word): split '/' (ribbon index y - x, H = (2,1), V = (1,2)) or
'\' (ribbon index y + x, H = (2,-1), V = (1,-2) mirrored), word periodic in the ribbon index (STRUCTURE.md T2).
Objective: all crossings per period (fixed-fixed, fixed-free, free-free), CP-SAT exact.
Absorbed ribbon ends per period: if splits differ, every ribbon of either side that meets the line ends there;
if the split is equal, the ribbons whose bits differ end on both sides (2 ends each).
usage: python interface.py a [tlim]          (runs the 8 slopes x ordered pairs of the 4 pure fields)
       python interface.py a tlim mixed      (also words of period 2 and 3 on each side, splits / and \\)
"""
import sys, itertools, math
from collections import defaultdict
from ortools.sat.python import cp_model

KM = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

def orient(p, q, r):
    v = (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])
    return (v > 0) - (v < 0)

def cross(e, f):
    p1, p2 = e; q1, q2 = f
    if len({p1, p2, q1, q2}) < 4: return False
    return orient(p1, p2, q1)*orient(p1, p2, q2) < 0 and orient(q1, q2, p1)*orient(q1, q2, p2) < 0

def field_has(F, x, y, d):
    """is the edge (x,y)->(x,y)+d (d in KM) an edge of field F?"""
    split, w = F; q = len(w)
    u, v = (x, y), (x+d[0], y+d[1])
    if split == '\\':           # mirror x -> -x
        u, v = (-u[0], u[1]), (-v[0], v[1])
    if u[1] > v[1] or (u[1] == v[1] and u[0] > v[0]): u, v = v, u
    dx, dy = v[0]-u[0], v[1]-u[1]
    k = u[1] - u[0]
    if (dx, dy) == (2, 1):  return w[k % q] == 'H'
    if (dx, dy) == (-2, -1): return False
    if (dx, dy) == (1, 2):  return w[(k+1) % q] == 'V'
    return False

def ribbon_index(split, c):
    return c[1] - c[0] if split == '/' else c[1] + c[0]

def absorbed(F1, F2, T):
    (s1, w1), (s2, w2) = F1, F2
    r = lambda s: abs(ribbon_index(s, T))
    if s1 != s2: return r(s1) + r(s2)
    D = r(s1)
    if D == 0: return 0
    base = (0, 0)
    ks = [ribbon_index(s1, base) + i for i in range(D)]
    return 2*sum(1 for k in ks if w1[k % len(w1)] != w2[k % len(w2)])

def solve(T, hv, a, F1, F2, tlim=60):
    assert hv[0]*T[0] + hv[1]*T[1] == 0
    h = lambda c: hv[0]*c[0] + hv[1]*c[1]
    ax = 0 if T[0] != 0 else 1
    P = abs(T[ax]); sg = 1 if T[ax] > 0 else -1
    Tn = (T[0]*sg, T[1]*sg)
    def canon(c):
        k = c[ax] // P
        return (c[0] - k*Tn[0], c[1] - k*Tn[1]), k
    side = lambda c: 1 if h(c) < -a else (2 if h(c) > a else 0)
    # band cells (canonical)
    R = 12 * (abs(T[0]) + abs(T[1]) + a + 3)
    cells = [(x, y) for x in range(-R, R) for y in range(-R, R) if side((x, y)) == 0 and canon((x, y))[1] == 0]
    cellset = set(cells)
    def ekey(p, d):
        q = (p[0]+d[0], p[1]+d[1])
        c1, k1 = canon(p); c2 = (q[0]-k1*Tn[0], q[1]-k1*Tn[1])
        cq, kq = canon(q); c3 = (p[0]-kq*Tn[0], p[1]-kq*Tn[1])
        return min((c1, c2), (cq, c3))
    # fixed edge orbits: field edges with an endpoint on their own side, within reach of the band
    fixed = set()
    reach = 8 * (abs(hv[0]) + abs(hv[1]))
    for x in range(-R, R):
        for y in range(-R, R):
            c = (x, y)
            if canon(c)[1] != 0: continue
            sd = side(c)
            if sd == 0 or abs(h(c)) > a + reach: continue
            F = F1 if sd == 1 else F2
            for d in KM:
                if field_has(F, x, y, d):
                    q = (x+d[0], y+d[1])
                    if side(q) not in (0, sd): return ('BAD-BAND', None, None)   # jumps over the band
                    fixed.add(ekey(c, d))
    free = set()
    for c in cells:
        for d in KM:
            q = (c[0]+d[0], c[1]+d[1])
            if side(q) == 0: free.add(ekey(c, d))
    free -= fixed
    fixed, free = sorted(fixed), sorted(free)
    fdeg = defaultdict(int)
    for (u, v) in fixed:
        for z in (u, v):
            if side(z) == 0: fdeg[canon(z)[0]] += 1
    m = cp_model.CpModel(); X = {e: m.NewBoolVar('') for e in free}
    inc = defaultdict(list)
    for e in free:
        for z in e: inc[canon(z)[0]].append(X[e])
    for c in cells:
        if fdeg[c] > 2: return ('FIELD-CONFLICT', None, None)
        m.Add(sum(inc[c]) == 2 - fdeg[c])
    # side cells must have degree 2 from their field (checked on the canonical window)
    tr = lambda e, k: ((e[0][0]+k*Tn[0], e[0][1]+k*Tn[1]), (e[1][0]+k*Tn[0], e[1][1]+k*Tn[1]))
    K = 6
    allE = [(e, True) for e in fixed] + [(e, False) for e in free]
    const = 0; obj = []
    for i in range(len(allE)):
        e, fe = allE[i]
        for j in range(i, len(allE)):
            f, ff = allE[j]
            n = sum(1 for k in range(-K, K+1) if (j != i or k > 0) and cross(e, tr(f, k)))
            if n == 0: continue
            if fe and ff: const += n
            elif fe: obj += [X[f]]*n
            elif ff: obj += [X[e]]*n
            else:
                z = m.NewBoolVar(''); m.Add(z >= X[e] + X[f] - 1); obj += [z]*n
    m.Minimize(sum(obj) + const)
    s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = tlim
    st = s.Solve(m)
    if st == cp_model.INFEASIBLE: return ('INFEASIBLE', None, None)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): return (s.StatusName(st), None, None)
    return (s.StatusName(st), s.ObjectiveValue(), s.BestObjectiveBound())

SLOPES = {'0': ((1, 0), (0, 1)), 'inf': ((0, 1), (1, 0)), '+1': ((1, 1), (1, -1)), '-1': ((1, -1), (1, 1)),
          '+1/2': ((2, 1), (1, -2)), '-1/2': ((2, -1), (1, 2)), '+2': ((1, 2), (2, -1)), '-2': ((1, -2), (2, 1))}

def mult_for(T, F1, F2):
    """smallest m such that m*T maps both fields to themselves (ribbon index shift = 0 mod word period)."""
    for mm in range(1, 13):
        ok = all((ribbon_index(F[0], (mm*T[0], mm*T[1]))) % len(F[1]) == 0 for F in (F1, F2))
        if ok: return mm
    return None

MULTS = [1]
if __name__ == '__main__':
    a = int(sys.argv[1]); tl = float(sys.argv[2]) if len(sys.argv) > 2 else 60
    mixed = len(sys.argv) > 3 and sys.argv[3] == 'mixed'
    MULTS = [int(t) for t in sys.argv[4].split(',')] if len(sys.argv) > 4 else [1]
    fields = [(s, b) for s in '/\\' for b in 'HV']
    if mixed: fields += [(s, w) for s in '/\\' for w in ('HV', 'HHV', 'HVV')]
    best = None
    print(f'band |h| <= {a}; columns: slope, F1 (side h<0), F2, period vector, status, crossings/period, '
          f'absorbed ends/period, crossings per absorbed end', flush=True)
    for sl, (T0, hv) in SLOPES.items():
        for F1, F2 in itertools.permutations(fields, 2):
            mm = mult_for(T0, F1, F2)
            if mm is None: continue
            if absorbed(F1, F2, T0) == 0 and absorbed(F1, F2, (mm*T0[0], mm*T0[1])) == 0: continue
            # need the band thick enough that no knight move jumps it: max |h step| <= 2a+1
            if max(abs(hv[0]*d[0] + hv[1]*d[1]) for d in KM) > 2*a + 1:
                print(sl, F1, F2, 'band too thin'); continue
            res = []
            for k in MULTS:
                T = (k*mm*T0[0], k*mm*T0[1])
                ends = absorbed(F1, F2, T)
                st, val, bd = solve(T, hv, a, F1, F2, tl)
                r = None if bd is None else bd / ends
                res.append((r, k, T, st, val, bd, ends))
            feas = [x for x in res if x[0] is not None]
            r, k, T, st, val, bd, ends = min(feas) if feas else res[0]
            print(f'{sl:5s} {F1[0]}{F1[1]:4s} {F2[0]}{F2[1]:4s} T={T} {st:10s} {val} (bound {bd}) ends {ends} '
                  f'per end {None if r is None else round(r, 4)}   [per multiplier: '
                  + ' '.join(f"x{x[1]}:{None if x[0] is None else round(x[0],3)}" for x in res) + ']', flush=True)
            if r is not None and (best is None or r < best[0]): best = (r, sl, F1, F2)
    print('MINIMUM crossings per absorbed end:', best)
