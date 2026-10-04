#!/usr/bin/env python3
"""Cross-insertion data generator (KT Integrator, 2026-10-04). Python standard library only. NOT a proof.

From a base board (tour or 2-factor, board.js grid) at size n0, build boards at n0 + k*S by copying S columns at a
vertical seam x = X and S rows at a horizontal seam y = Y, k times (cross insertion). This is valid when the base is
S-periodic across both seams (checked: cell moves equal at distance S for every cell within knight reach of a seam);
with a mixed interior S must be a multiple of 5. Every generated board is checked directly (on board, degree 2,
reciprocal knight edges) and its cycles and turns are counted.
Usage: mixgen.py BASE.json [--S 10] [--nmax 300] [--X x --Y y] [--out DIR]
"""
import argparse, json, os, sys
from math import gcd

DIRS = ((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2))   # move code -> (dx, dy) in check_upper_proofs
# board.js grid: row r = y from the top, move code k -> (dx, dy) = (MJ[k], -MI[k]) as in kt.core
MI = (-2, -1, 1, 2, 2, 1, -1, -2); MJ = (1, 2, 2, 1, -1, -2, -2, -1)

def load(path):
    d = json.load(open(path)); g = d.get('tour') or d.get('grid')
    n = len(g); mv = {}
    for r, row in enumerate(g):
        for x, code in enumerate(row):
            mv[(x, n - 1 - r)] = tuple(sorted((MJ[int(k)], -MI[int(k)]) for k in code))
    return n, mv, d

def periodic_seam(n, mv, S, X, axis):
    """True if moves equal at distance S across the seam at X (axis 0: columns, 1: rows), within knight reach."""
    for t in range(X - 2, X + 2):
        if t - S < 0 or t >= n: return False
        for u in range(n):
            a = (t, u) if axis == 0 else (u, t); b = (t - S, u) if axis == 0 else (u, t - S)
            if mv[a] != mv[b]: return False
    return True

def grow(n, mv, S, X, Y, k):
    m = n + k * S
    def back(v, Z):
        if v < Z: return v
        if v < Z + k * S: return Z - S + (v - Z) % S
        return v - k * S
    return m, {(x, y): mv[(back(x, X), back(y, Y))] for x in range(m) for y in range(m)}

def check(m, g):
    for (x, y), ds in g.items():
        if len(set(ds)) != 2: return 'degree'
        for dx, dy in ds:
            v = (x + dx, y + dy)
            if v not in g: return f'off board at {(x, y)}'
            if (-dx, -dy) not in g[v]: return f'not reciprocal at {(x, y)}'
    return None

def cycles(g):
    seen = set(); k = 0
    for s in g:
        if s in seen: continue
        k += 1; prev, u = None, s
        while True:
            seen.add(u); nx = [(u[0] + dx, u[1] + dy) for dx, dy in g[u]]
            v = nx[0] if nx[0] != prev else nx[1]
            prev, u = u, v
            if u == s: break
    return k

def turns(g):
    return sum(1 for u, ds in g.items() if ds[0][0] + ds[1][0] != 0 or ds[0][1] + ds[1][1] != 0)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('base'); ap.add_argument('--S', type=int)
    ap.add_argument('--nmax', type=int, default=300); ap.add_argument('--X', type=int); ap.add_argument('--Y', type=int)
    ap.add_argument('--out')
    a = ap.parse_args()
    n, mv, d = load(a.base)
    bad = check(n, mv); assert bad is None, f'base is not a 2-factor: {bad}'
    T0, c0 = turns(mv), cycles(mv)
    print(f'base {a.base}: n={n} T={T0} T-8n={T0 - 8 * n} cycles={c0}')
    Ss = [a.S] if a.S else [S for S in range(2, n // 2 + 1, 2)]
    found = None
    for S in Ss:
        Xs = [a.X] if a.X is not None else sorted(range(S + 2, n - 1), key=lambda t: abs(t - n // 2))
        Ys = [a.Y] if a.Y is not None else sorted(range(S + 2, n - 1), key=lambda t: abs(t - n // 2))
        X = next((t for t in Xs if periodic_seam(n, mv, S, t, 0)), None)
        Y = next((t for t in Ys if periodic_seam(n, mv, S, t, 1)), None)
        if X is not None and Y is not None: found = (S, X, Y); break
    if not found:
        print(f'NO cross insertion: the base is not S-periodic across any vertical and horizontal seam for S in {Ss[:12]}...')
        def miss(S, t, axis):
            if t - S - 2 < 0 or t + 2 > n: return None
            return sum(mv[(x, u) if axis == 0 else (u, x)] != mv[(x - S, u) if axis == 0 else (u, x - S)]
                       for x in range(t - 2, t + 2) for u in range(n))
        for S in [S for S in Ss if S % 10 == 0] or Ss[:3]:
            for axis, name in ((0, 'vertical'), (1, 'horizontal')):
                best = min(((miss(S, t, axis), t) for t in range(S + 2, n - 1) if miss(S, t, axis) is not None), default=None)
                print(f'  S={S} {name} seam: fewest mismatched cells {best[0] if best else "-"} at {best[1] if best else "-"} '
                      f'(of {4 * n} cells within knight reach)')
        sys.exit(2)
    S, X, Y = found
    print(f'cross insertion: S={S}, vertical seam X={X}, horizontal seam Y={Y}')
    rows = []
    for k in range(0, (a.nmax - n) // S + 1):
        m, g = grow(n, mv, S, X, Y, k)
        bad = check(m, g)
        if bad: rows.append((m, None, None, bad)); print(f'n={m}: INVALID ({bad})', flush=True); continue
        T, c = turns(g), cycles(g)
        rows.append((m, T, c, None)); print(f'n={m}: T={T} T-8n={T - 8 * m} cycles={c}', flush=True)
        if a.out and c == 1:
            os.makedirs(a.out, exist_ok=True)
            code = {v: i for i, v in enumerate(zip(MJ, [-x for x in MI]))}
            grid = [[''.join(sorted(str(code[dv]) for dv in g[(x, m - 1 - r)])) for x in range(m)] for r in range(m)]
            json.dump(dict(n=m, turns=T, source=a.base, S=S, X=X, Y=Y, k=k, tour=grid), open(os.path.join(a.out, f'n{m}.json'), 'w'))
    ok = [r for r in rows if r[1] is not None]
    if ok:
        dT = {(ok[i + 1][1] - ok[i][1]) for i in range(len(ok) - 1)}
        print(f'SUMMARY: S={S}; T - 8n values {sorted({T - 8 * m for m, T, c, _ in ok})}; dT per step {sorted(dT)} '
              f'(8S = {8 * S}); cycles by n: {[(m, c) for m, T, c, _ in ok]}')
        ones = [m for m, T, c, _ in ok if c == 1]
        print(f'single-cycle n: {ones}')
        if len(ones) >= 2:
            ks = [(m - n) // S for m in ones]
            K = 0
            for i in range(1, len(ks)): K = gcd(K, ks[i] - ks[0])
            print(f'gcd of k differences among single-cycle sizes: {K} (k = (n - {n})/{S}); a pattern hint, not a proof')

if __name__ == '__main__':
    main()
