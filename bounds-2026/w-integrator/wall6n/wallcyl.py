#!/usr/bin/env python
"""Cost of a charged straight wall between two STRAIGHT ribbon fields, periodic cylinder model (KT Integrator,
2026-10-03). Wall direction (a,b), a <= b: band coordinate s = x - floor(a*y/b); band cells 0 <= s < WM are free;
cells with s < 0 or s >= WM keep their exterior field moves +-F (F_left, F_right) except moves into the band,
which become free (one per cut field line). Rows y mod H, H = b*L, identified with (x + a*L, y + H).
Constraints: degree 2 everywhere; psi jump across one transversal row = sum chi(a)(m_+ + m_- + 1) != 0 mod 3
(formula (2) of w-turnstheory/PROOF_crossings_lower.md). Objective: crossing pairs per period (exact count on the
cylinder). Output: min crossings per period and per level (b*L levels per period for a wall steeper than 45 deg).
Usage: wallcyl.py a b L WM FL FR [--D 6] [--zero]   F in {21, 12, 2m1, 1m2}"""
import argparse, sys
from collections import defaultdict
sys.path.insert(0, '/home/nil/nil/knight-formation-research/gap/searcher')
from check_identity import tile_quarters
from ortools.sat.python import cp_model

FIELDS = {'21': (2, 1), '12': (1, 2), '2m1': (2, -1), '1m2': (1, -2)}
MV = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

def seg_cross(p1, p2, q1, q2):
    if len({p1, p2, q1, q2}) < 4: return False
    o = lambda a, b, c: (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return o(p1, p2, q1) * o(p1, p2, q2) < 0 and o(q1, q2, p1) * o(q1, q2, p2) < 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('a', type=int); ap.add_argument('b', type=int); ap.add_argument('L', type=int)
    ap.add_argument('WM', type=int); ap.add_argument('FL'); ap.add_argument('FR')
    ap.add_argument('--D', type=int, default=6); ap.add_argument('--zero', action='store_true', help='force psi jump 0 (calibration)')
    ap.add_argument('--time', type=float, default=600); ap.add_argument('--nopsi', action='store_true'); ap.add_argument('--show', action='store_true')
    A = ap.parse_args()
    a, b, L, WM, D = A.a, A.b, A.L, A.WM, A.D
    H, TX = b * L, a * L
    diffs = {(d1[0] - d2[0], d1[1] - d2[1]) for d1 in MV for d2 in MV} | set(MV)
    assert all((k * TX, k * H) not in diffs for k in (1, 2)), 'period vector collapses knight edges; change L'
    sv = lambda c: c[0] - (a * c[1]) // b
    def canon(c):
        k = c[1] // H
        return (c[0] - TX * k, c[1] - H * k)
    inwin = lambda c: (0 if A.FL == 'none' else -D) <= sv(c) < WM + D
    cells = [(x, y) for y in range(H) for x in range(-D + (a * y) // b - 1, WM + D + (a * y) // b + 1) if inwin((x, y))]
    cellset = set(cells)
    band = lambda c: 0 <= sv(c) < WM
    side = lambda c: 'L' if sv(c) < 0 else 'R'
    soft = lambda c: (A.FL != 'none' and sv(c) < -D + 2) or sv(c) >= WM + D - 2
    # candidate edges (canonical key -> representative (p, q) with p canonical)
    rep = {}
    for c in cells:
        for d in MV:
            q = (c[0] + d[0], c[1] + d[1])
            if not inwin(q): continue
            key = tuple(sorted([c, canon(q)]))
            if key[0] == key[1]: continue
            rep.setdefault(key, (c, q))
    fixed, free = [], []
    for key, (p, q) in rep.items():
        d = (q[0] - p[0], q[1] - p[1])
        pb, qb = band(p), band(q)
        if not pb and not qb and side(p) == side(q):
            FN = A.FL if side(p) == 'L' else A.FR
            if FN.startswith('g'):             # generic zigzag g<v>_<d1x>_<d1y>_<d2x>_<d2y>: valleys send +d1, +d2
                parts = FN[1:].split('_'); vv = int(parts[0]); d1 = (int(parts[1]), int(parts[2])); d2 = (int(parts[3]), int(parts[4]))
                val = (p[0] + p[1]) % 2 == vv
                if (val and d in (d1, d2)) or (not val and d in ((-d1[0], -d1[1]), (-d2[0], -d2[1]))): fixed.append(key)
                continue
            if FN in ('y0', 'y1'):             # (1,1) zigzag field: valleys send +(2,-1), +(1,-2)
                val = (p[0] + p[1]) % 2 == int(FN[1])
                if (val and d in ((2, -1), (1, -2))) or (not val and d in ((-2, 1), (-1, 2))): fixed.append(key)
                continue
            if FN in ('z0', 'z1'):             # (1,-1) zigzag field: valleys (x+y = v mod 2) send +(2,1), +(1,2)
                val = (p[0] + p[1]) % 2 == int(FN[1])
                if (val and d in ((2, 1), (1, 2))) or (not val and d in ((-2, -1), (-1, -2))): fixed.append(key)
                continue
            F = FIELDS[FN]
            if d in (F, (-F[0], -F[1])): fixed.append(key)
            continue
        if pb or qb: free.append(key)
    m = cp_model.CpModel()
    x = {k: m.NewBoolVar('') for k in free}
    inc = defaultdict(list); fdeg = defaultdict(int)
    for k in free:
        inc[k[0]].append(x[k]); inc[k[1]].append(x[k])
    for k in fixed:
        fdeg[k[0]] += 1; fdeg[k[1]] += 1
    for c in cells:
        tot = sum(inc[c]) + fdeg[c]
        if soft(c): m.Add(tot <= 2)
        else: m.Add(tot == 2)
    # quarter multiplicities on the transversal row y in [0,1): squares (i, 0)
    lin = defaultdict(list); const = defaultdict(int)
    def add_cov(k, var):
        p, q = rep[k]
        for kk in (-1, 0, 1):                      # translates of the edge that touch row 0
            pp, qq = (p[0] + TX * kk, p[1] + H * kk), (q[0] + TX * kk, q[1] + H * kk)
            for (i, j, t) in tile_quarters(pp, qq):
                if j == 0:
                    if var is None: const[(i, t)] += 1
                    else: lin[(i, t)].append(var)
    for k in fixed: add_cov(k, None)
    for k in free: add_cov(k, x[k])
    # transversal: dual steps from square (i,0) to (i+1,0) cross the grid edge x = i+1, a = (i+1, 1) on the left
    i_lo, i_hi = (-1 if A.FL == 'none' else -D + 3), WM + D - 4
    terms, cst = [], 0
    for i in range(i_lo, i_hi):
        chi = 1 if (i + 1 + 1) % 2 == 0 else -1
        # m_+ = right quarter (t=1) of square (i,0); m_- = left quarter (t=3) of square (i+1,0)
        for key in [(i, 1), (i + 1, 3)]:
            terms += [chi * v for v in lin[key]]; cst += chi * const[key]
        cst += chi
    S = sum(terms) + cst
    K = m.NewIntVar(-1000, 1000, 'K'); r = m.NewIntVar(0, 2, 'r')
    m.Add(S == 3 * K + r)
    if A.nopsi: pass
    elif A.zero: m.Add(r == 0)
    else: m.Add(r >= 1)
    # crossings per period: unordered pairs of edge translates, counted once per period
    allk = [(k, None) for k in fixed] + [(k, x[k]) for k in free]
    zs = []
    for i1 in range(len(allk)):
        k1, v1 = allk[i1]
        p1, q1 = rep[k1]
        for i2 in range(i1, len(allk)):
            k2, v2 = allk[i2]
            if v1 is None and v2 is None: continue
            p2, q2 = rep[k2]
            for kk in (-2, -1, 0, 1, 2):
                if i1 == i2 and kk <= 0: continue
                pp, qq = (p2[0] + TX * kk, p2[1] + H * kk), (q2[0] + TX * kk, q2[1] + H * kk)
                if seg_cross(p1, q1, pp, qq):
                    if v1 is None: zs.append(v2)
                    elif v2 is None: zs.append(v1)
                    else:
                        z = m.NewBoolVar(''); m.AddBoolOr([v1.Not(), v2.Not(), z]); zs.append(z)
    m.Minimize(sum(zs))
    s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = A.time
    res = s.Solve(m)
    lv = H  # levels per period for a steep wall (a <= b): one per row
    print(f'wall ({a},{b}) L={L} WM={WM} D={D} fields {A.FL}|{A.FR} zero={A.zero}: {s.StatusName(res)}', end='')
    if res in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        val = round(s.ObjectiveValue())
        print(f' crossings/period={val} bound={s.BestObjectiveBound():.0f} per level={val}/{lv}={val / lv:.4f} r={s.Value(r)}')
        if A.show:
            for k in free:
                if s.Value(x[k]): print('  ', rep[k])
    else:
        print()

if __name__ == '__main__':
    main()
