"""Independent SAT certificates for the finite lemmas M3 and NE-M3 (KT Lower Bounds, 2026-10-02).

This file does NOT reuse the CP-SAT scripts. It builds a plain CNF:
  - one variable per candidate knight edge,
  - degree: 'at most 2' = every triple has a false edge; 'at least 2' = every (k-1)-subset has a true edge,
  - forced edges as unit clauses, forbidden edges as negative units,
  - no crossing: a 2-clause for every properly crossing pair (own exact integer predicate below),
  - the claim's negation: the flux phi(s) is NOT congruent to the claimed value mod 3, written as one
    blocking clause per assignment of the (at most 8) edges that cross s.
It solves with Glucose 4 (python-sat), writes a DRUP proof, and checks the proof with check_drup.py.
UNSAT + checked proof = the lemma instance holds.
"""
import sys, itertools, json, os
from pysat.solvers import Solver

KM = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def orient(a, b, c):
    v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return (v > 0) - (v < 0)


def proper_cross(p1, p2, q1, q2):
    """exact proper intersection of segments (all coordinates multiplied by 2 to stay integral)"""
    return orient(p1, p2, q1) * orient(p1, p2, q2) < 0 and orient(q1, q2, p1) * orient(q1, q2, p2) < 0


def chi(c):
    return 1 if (c[0] + c[1]) % 2 == 0 else -1


def build(window, frame, forced, forbidden_cells, seg, value, allowed_cross=frozenset()):
    """window: set of cells with degree exactly 2; frame: extra cells with degree <= 2;
    forced: set of edges that must be present; forbidden_cells: cells whose only edges are forced ones;
    seg: ((ax2,ay2),(bx2,by2)) dual segment in doubled coordinates; value: claimed phi mod 3;
    allowed_cross: set of frozenset({e,f}) pairs allowed to cross."""
    cells = set(window) | set(frame)
    E = set()
    for c in cells:
        for d in KM:
            q = (c[0] + d[0], c[1] + d[1])
            if q in cells and (c in window or q in window):
                E.add(tuple(sorted([c, q])))
    E = sorted(E)
    for e in forced:
        assert e in set(E), ('forced edge outside candidate set', e)
    var = {e: i + 1 for i, e in enumerate(E)}
    cls = []
    inc = {c: [] for c in cells}
    for e in E:
        inc[e[0]].append(var[e]); inc[e[1]].append(var[e])
    for c in cells:
        vs = inc[c]
        for t in itertools.combinations(vs, 3):
            cls.append([-v for v in t])
        if c in window:
            for sub in itertools.combinations(vs, len(vs) - 1):
                cls.append(list(sub))
    for e in E:
        if e in forced:
            cls.append([var[e]])
        elif any(c in forbidden_cells for c in e):
            cls.append([-var[e]])
    D = lambda p: (2 * p[0], 2 * p[1])
    for e, f in itertools.combinations(E, 2):
        if frozenset((e, f)) in allowed_cross:
            continue
        if proper_cross(D(e[0]), D(e[1]), D(f[0]), D(f[1])):
            cls.append([-var[e], -var[f]])
    A2, B2 = seg
    fl = []
    for e in E:
        if proper_cross(A2, B2, D(e[0]), D(e[1])):
            left = e[0] if orient(A2, B2, D(e[0])) > 0 else e[1]
            fl.append((chi(left), var[e]))
    assert len(fl) <= 10
    for bits in itertools.product((0, 1), repeat=len(fl)):
        s = sum(c * b for (c, v), b in zip(fl, bits))
        if s % 3 == value % 3:
            cls.append([(-v if b else v) for (c, v), b in zip(fl, bits)])
    return E, cls, len(fl)


def solve_and_certify(name, E, cls, outdir='certs'):
    os.makedirs(outdir, exist_ok=True)
    nv = len(E)
    with open(f'{outdir}/{name}.cnf', 'w') as f:
        f.write(f'p cnf {nv} {len(cls)}\n')
        for c in cls:
            f.write(' '.join(map(str, c)) + ' 0\n')
    s = Solver(name='glucose4', bootstrap_with=cls, with_proof=True)
    sat = s.solve()
    if sat:
        return 'SAT'
    proof = s.get_proof()
    with open(f'{outdir}/{name}.drup', 'w') as f:
        for line in proof:
            f.write(line.strip() + ('\n' if line.strip().endswith('0') else ' 0\n'))
    return 'UNSAT'


def m3_instance(W, orient_, ox, oy):
    """interior M3: W x W window, frame width 2, segment near the centre (doubled coordinates)."""
    window = {(x, y) for x in range(W) for y in range(W)}
    frame = {(x, y) for x in range(-2, W + 2) for y in range(-2, W + 2)} - window
    c = W // 2
    if orient_ == 'h':
        A, B = (c - 0.5 + ox, c - 0.5 + oy), (c + 0.5 + ox, c - 0.5 + oy)
    else:
        A, B = (c - 0.5 + ox, c - 0.5 + oy), (c - 0.5 + ox, c + 0.5 + oy)
    mid = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
    d = (B[0] - A[0], B[1] - A[1])
    right = (round(mid[0] + 0.5 * d[1]), round(mid[1] - 0.5 * d[0]))
    val = chi(right) % 3
    seg = ((int(2 * A[0]), int(2 * A[1])), (int(2 * B[0]), int(2 * B[1])))
    return window, frame, set(), set(), seg, val


def nem3_instance(PAT, r, j):
    """near-edge M3: left edge x = 0, columns 0,1 in pattern PAT, window x < j+5, rows r-6..r+7,
    segment from (j-1/2, r+1/2) to (j+1/2, r+1/2). Claimed value: chi(cell (j, r)) (j >= 2)."""
    X = j + 5; Y0, Y1 = r - 6, r + 8
    window = {(x, y) for x in range(X) for y in range(Y0, Y1)}
    frame = {(x, y) for x in range(0, X + 2) for y in range(Y0 - 2, Y1 + 2)} - window
    s = 1 if PAT == 'P' else -1
    cells = window | frame
    forced = set()
    pedges = []
    for y in range(Y0 - 4, Y1 + 4):
        for a, b in [((0, y), (2, y + s)), ((0, y), (1, y + 2 * s)), ((1, y), (3, y + s))]:
            if a in cells and b in cells and (a in window or b in window):
                forced.add(tuple(sorted([a, b])))
    pcells = {c for c in cells if c[0] <= 1}
    allowed = set()
    for e, f in itertools.combinations(sorted(forced), 2):
        allowed.add(frozenset((e, f)))
    A, B = (j - 0.5, r + 0.5), (j + 0.5, r + 0.5)
    val = chi((j, r)) % 3
    seg = ((int(2 * A[0]), int(2 * A[1])), (int(2 * B[0]), int(2 * B[1])))
    return window, frame, forced, pcells, seg, val, allowed


if __name__ == '__main__':
    results = {}
    which = sys.argv[1]
    if which == 'm3':
        for o in 'hv':
            for ox in (0, 1):
                w, fr, fo, fc, seg, val = m3_instance(7, o, ox, 0)
                E, cls, k = build(w, fr, fo, fc, seg, val)
                name = f'm3_W7_{o}_ox{ox}'
                st = solve_and_certify(name, E, cls)
                results[name] = dict(status=st, vars=len(E), clauses=len(cls), claimed=val, crossing_edges=k)
                print(name, results[name], flush=True)
    elif which == 'nem3':
        for PAT in 'PQ':
            for r in (8, 9):
                for j in range(2, 9):
                    w, fr, fo, fc, seg, val, al = nem3_instance(PAT, r, j)
                    E, cls, k = build(w, fr, fo, fc, seg, val, al)
                    name = f'nem3_{PAT}_r{r}_j{j}'
                    st = solve_and_certify(name, E, cls)
                    results[name] = dict(status=st, vars=len(E), clauses=len(cls), claimed=val, crossing_edges=k)
                    print(name, results[name], flush=True)
    json.dump(results, open(f'certs/{which}_results.json', 'w'), indent=1)
