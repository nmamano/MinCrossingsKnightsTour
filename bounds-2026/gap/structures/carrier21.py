"""Odd-current carrier parallel to the strands (SHEET 13.3, open item (2)). KT Structures, 2026-10-03.
Cylinder Z^2 / <T>, T = (2k, k). Line label c = x - 2y. Band: lines -w <= c <= w are free (degree exactly 2,
any knight moves inside the band); all other lines keep pure (2,1) edges. Cycles of any kind are allowed (a
relaxation, so the minimum is a valid lower bound for 2-factors and tours). Colour current through the cut x = -1/2
as in w-structures/seam_flux.py (chi = +1 on even x+y). Minimise bad quarters (or crossings) per period subject to
current - base current = J.
usage: python carrier21.py k w J[,J...] [bq|x] [time]"""
import sys
from ortools.sat.python import cp_model
import fold_exact_scan as F

MOVES = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

def orient(p, q, r):
    v = (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0]); return (v > 0) - (v < 0)
def cross(e, f):
    p1, p2 = e; q1, q2 = f
    if len({p1, p2, q1, q2}) < 4: return False
    return orient(p1, p2, q1)*orient(p1, p2, q2) < 0 and orient(q1, q2, p1)*orient(q1, q2, p2) < 0

def solve(k, w, J, obj="bq", tl=120, workers=4, T=None, hv=None):
    if T is None: T, hv = (2*k, k), (-1, 2)          # parallel to the strands: h = -(x - 2y)
    lab = lambda c: -(hv[0]*c[0] + hv[1]*c[1])
    def canon(c):
        m = c[0] // T[0]; return (c[0] - m*T[0], c[1] - m*T[1])
    def ecanon(a, b):
        a, b = sorted((a, b)); m = a[0] // T[0]; return ((a[0]-m*T[0], a[1]-m*T[1]), (b[0]-m*T[0], b[1]-m*T[1]))
    band = lambda c: -w <= lab(c) <= w
    W = w + 4
    cells = sorted({canon((x, y)) for x in range(T[0]) for y in range(-W - 2 - 2*T[0], T[1] + W + 3 + 2*T[0]) if -W - 2 <= lab((x, y)) <= W + 2})
    bcells = [c for c in cells if band(c)]
    m = cp_model.CpModel(); var = {}
    for c in bcells:
        for d in MOVES:
            nb = (c[0]+d[0], c[1]+d[1])
            if band(nb):
                e = ecanon(c, nb)
                if e not in var: var[e] = m.NewBoolVar(str(e))
    inc = {c: [] for c in bcells}
    for e, v in var.items():
        for end in e: inc[canon(end)].append(v)
    fixed = set()
    for c in cells:
        if not band(c) and abs(lab(c)) <= W:
            for d in ((2, 1), (-2, -1)):
                nb = (c[0]+d[0], c[1]+d[1])
                fixed.add(ecanon(c, nb))
                if band(nb): inc[canon(nb)].append(1)   # a fixed line edge entering the band
    for c in bcells: m.Add(sum(inc[c]) == 2)
    # translates for geometry
    def translates(e, rng=range(-3, 4)):
        (a, b) = e
        for t in rng: yield ((a[0]+t*T[0], a[1]+t*T[1]), (b[0]+t*T[0], b[1]+t*T[1]))
    # coverage of quarters
    cov = {}; const = {}
    def qcanon(x, y, kq):
        mm = x // T[0]; return (x - mm*T[0], y - mm*T[1], kq)
    def add_cov(e, v):
        a, b = sorted(e)
        for x, y, kq in F.templates[b[0]-a[0], b[1]-a[1]]:
            q = qcanon(x+a[0], y+a[1], kq)
            if v is None: const[q] = const.get(q, 0) + 1
            else: cov.setdefault(q, []).append(v)
    for e, v in var.items(): add_cov(e, v)
    for e in fixed: add_cov(e, None)
    qs = [q for q in cov]
    bad = {}
    for q in qs:
        b = m.NewBoolVar(''); bad[q] = b
        s = sum(cov[q]) + const.get(q, 0)
        m.Add(s - 1 <= 8*b); m.Add(1 - s <= b)
    # crossings (per period: pairs (e rep, f translate))
    xs = []
    if obj == 'x':
        ev = list(var.items()) + [(e, None) for e in fixed]
        for i, (e, v) in enumerate(var.items()):
            for f, u in ev:
                for ft in translates(f):
                    if cross(e, ft):
                        if u is None: xs.append(v)
                        elif (f, ft) != (e, e) and str(f) > str(e) or (f == e and ft != e):
                            z = m.NewBoolVar(''); m.AddBoolAnd([v, u]).OnlyEnforceIf(z); m.Add(z >= v + u - 1); xs.append(z)
    # current
    chi = lambda c: 1 if (c[0] + c[1]) % 2 == 0 else -1
    def straddle(a, b):
        lo, hi = (a, b) if a[0] < b[0] else (b, a)
        return lo if lo[0] < 0 <= hi[0] else None
    terms, I0 = [], 0
    for e, v in var.items():
        for a, b in translates(e, range(-4, 5)):
            lo = straddle(a, b)
            if lo: terms.append(chi(lo) * v)
    base_edges = {ecanon(c, (c[0]+d[0], c[1]+d[1])) for c in bcells for d in ((2, 1), (-2, -1))} - fixed
    assert all(e in var for e in base_edges)
    for be in base_edges:   # base: pure (2,1) edges at band cells (fixed edges are common to both, so they cancel)
        for a, b in translates(be, range(-4, 5)):
            lo = straddle(a, b)
            if lo: I0 += chi(lo)
    m.Add(sum(terms) - I0 == J)
    m.Minimize(sum(bad.values()) if obj == 'bq' else sum(xs))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = workers
    r = s.Solve(m)
    if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE): return s.StatusName(r), None, None
    return s.StatusName(r), s.ObjectiveValue(), s.BestObjectiveBound()

if __name__ == '__main__':
    if sys.argv[1] == 'h':   # horizontal band, period (p, 0): python carrier21.py h p w J [obj] [time]
        p, w = int(sys.argv[2]), int(sys.argv[3]); Js = [int(a) for a in sys.argv[4].split(',')]
        obj = sys.argv[5] if len(sys.argv) > 5 else 'bq'; tl = float(sys.argv[6]) if len(sys.argv) > 6 else 120
        for J in Js:
            st, v, bd = solve(0, w, J, obj, tl, T=(p, 0), hv=(0, 1))
            print(f'horizontal p={p} w={w} J={J:+d} obj={obj}: {st} value {v} bound {bd}'
                  + ('' if v is None else f'  per unit x {v/p:.3f} (bound {bd/p:.3f})'), flush=True)
        sys.exit()
    k, w = int(sys.argv[1]), int(sys.argv[2]); Js = [int(a) for a in sys.argv[3].split(',')]
    obj = sys.argv[4] if len(sys.argv) > 4 else 'bq'; tl = float(sys.argv[5]) if len(sys.argv) > 5 else 120
    for J in Js:
        st, v, bd = solve(k, w, J, obj, tl)
        print(f'k={k} (period x-length {2*k}) w={w} J={J:+d} obj={obj}: {st} value {v} bound {bd}'
              + ('' if v is None else f'  per unit x {v/(2*k):.3f} (bound {bd/(2*k):.3f})'), flush=True)
