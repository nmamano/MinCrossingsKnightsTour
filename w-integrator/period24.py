#!/usr/bin/env python
"""Period-24 argument for the H16a + VerticalEdge lane construction (off_L = 0, Z = 6).

(a) strand permutations per 8 lines in each region (BL: bottom+left, MID: left+right,
    TR: right+top) and their orders; outside path matching (zone-relative) for every even n,
    compared for n, n+8, n+16, n+24.
(b) for each even residue r mod 24, one base completion of the four 6x6 corner zones (solved at
    n0 = r in 48..70) is transplanted unchanged (zone-relative) to n0 + 24k, k = 0..K, and every
    result is validated (kt.core.validate + independent walk) and counted.
Writes corners/H16a_VE_res<r>.json (base zone contents) and prints a table.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from kt.board import build_skeleton, complete, to_grid, fixed_paths
from kt.core import validate, num_crossings, num_turns
from assemble import NAMED, walk_check
from strands import pairing

import argparse
B, L, Z = NAMED['H16a'], NAMED['VerticalEdge'], 6
TAG, OBJ = 'H16a_VE', 'crossings'
def load(s):
    return NAMED[s] if s in NAMED else json.load(open(s))

def corners(n):
    return {'BL': (0, 0), 'BR': (n - Z, 0), 'TL': (0, n - Z), 'TR': (n - Z, n - Z)}

def zone_of(n, c):
    for k, (cx, cy) in corners(n).items():
        if cx <= c[0] < cx + Z and cy <= c[1] < cy + Z:
            return k, (c[0] - cx, c[1] - cy)

def outside_matching(n):
    nb, free = build_skeleton(n, B, L, off_L=0, Z=Z)
    paths, closed = fixed_paths(n, nb, free)
    assert not closed
    # each path: entry cell u (free) -> exit cell v (free); record by the fixed cells adjacent too
    m = set()
    for (u, v, cells) in paths:
        a = zone_of(n, u) + (tuple(x - y for x, y in zip(cells[0], u)),)
        b = zone_of(n, v) + (tuple(x - y for x, y in zip(cells[-1], v)),)
        m.add(tuple(sorted([a, b])))
    return frozenset(m)

def compose(p, q):  # apply p then q
    return [q[p[i]] for i in range(4)]

def order(p):
    k, r = 1, p
    while r != [0, 1, 2, 3]:
        r = compose(r, p); k += 1
    return k

def region_perm(m1, m2, lo, hi):
    """Follow the 4 strands of the formation upward through one block of 8 lines in [lo, hi):
    find a block start a where both matchings move the 4 lines [a, a+4) up by one lane step,
    return the position permutation [a, a+4) -> [a+8, a+12)."""
    for a in range(lo, hi - 12):
        for f, g in ((m1, m2), (m2, m1)):
            if all(a + 4 <= f.get(a + i, -99) < a + 8 for i in range(4)):
                mid = [f[a + i] for i in range(4)]
                if all(a + 8 <= g.get(c, -99) < a + 12 for c in mid):
                    return [g[c] - a - 8 for c in mid]
    return None

def part_a():
    from strands import expand
    pB = pairing(B, 'bottom'); pL = pairing(L, 'left')
    print('per-8-line strand permutation in each region (formation positions 0..3), and its order:')
    for n in (64, 66, 68, 70):
        x0, X0, y0, Y0 = 0, (13 - 2 * n) % 8, 2, (-n // 2) % 4
        N = 3 * (n - 1)
        mB = expand(pB['pairs'], 8, x0, 1, 0, N + 1); mL = expand(pL['pairs'], 8, 2 * y0, 1, 0, N + 1)
        mR = expand(pL['pairs'], 8, n - 1 + 2 * Y0, -1, 0, N + 1); mT = expand(pB['pairs'], 8, X0 + 2 * (n - 1), -1, 0, N + 1)
        out = []
        for nm, m1, m2, lo, hi in (('BL', mB, mL, 8, n - 8), ('MID', mL, mR, n + 8, 2 * n - 8), ('TR', mR, mT, 2 * n + 8, N - 8)):
            p = region_perm(m1, m2, lo, hi)
            out.append(f'{nm} {p} order {order(p) if p else "-"}')
        print(f'  n={n}: ' + ';  '.join(out))
    print('outside matching (zone-relative path ends) by n:')
    M = {n: outside_matching(n) for n in range(48, 48 + 24 * 4, 2)}
    for n in range(48, 48 + 24 * 3, 2):
        print(f'  n={n}: same as n+24: {M[n] == M[n + 24]}, same as n+8: {M[n] == M[n + 8]}, '
              f'same as n+16: {M[n] == M[n + 16]}, paths={len(M[n])}')

def zone_content(n, full):
    out = {}
    for k, (cx, cy) in corners(n).items():
        for x in range(Z):
            for y in range(Z):
                c = (cx + x, cy + y)
                out[f'{k}:{x},{y}'] = sorted([v[0] - c[0], v[1] - c[1]] for v in full[c])
    return out

def apply_zone(n, content):
    nb, free = build_skeleton(n, B, L, off_L=0, Z=Z)
    full = {c: set(v) for c, v in nb.items()}
    cs = corners(n)
    for key, ds in content.items():
        k, xy = key.split(':'); x, y = map(int, xy.split(','))
        c = (cs[k][0] + x, cs[k][1] + y)
        full[c] = {(c[0] + d[0], c[1] + d[1]) for d in ds}
    return full

def part_b(K=5):
    os.makedirs(os.path.join(HERE, 'corners'), exist_ok=True)
    print(f'{TAG}: objective {OBJ} first; res n0 | n0+24k: valid, X, T')
    for n0 in range(48, 72, 2):
        nb, free = build_skeleton(n0, B, L, off_L=0, Z=Z)
        w = dict(turn_weight=1, crossing_weight=1000) if OBJ == 'crossings' else dict(turn_weight=1000, crossing_weight=1)
        full, info = complete(n0, nb, free, time_limit=TL, workers=3, **w)
        content = zone_content(n0, full)
        json.dump(dict(n0=n0, residue_mod24=n0 % 24, Z=Z, bottom=B, left=L, off_L=0,
                       objective=OBJ, note='zone-relative moves (dx, dy), x right, y up; corners BL=(0,0), BR=(n-Z,0), '
                            'TL=(0,n-Z), TR=(n-Z,n-Z); apply to build_skeleton(n, bottom, left, off_L=0, Z=6)',
                       info=info, zones=content),
                  open(os.path.join(HERE, 'corners', f'{TAG}_res{n0 % 24:02d}.json'), 'w'))
        row = []
        X0 = T0 = None
        for k in range(K + 1):
            n = n0 + 24 * k
            g = to_grid(n, apply_zone(n, content))
            ok = validate(g) and walk_check(g)
            X, T_ = num_crossings(g), num_turns(g)
            if k == 0: X0, T0 = X, T_
            row.append(f'{n}:{"ok" if ok else "BAD"} X={X} T={T_}')
        print(f'{n0 % 24:>3} {n0:>3} X={X0} T={T0} {info["status"]} | ' + ' | '.join(row), flush=True)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--bottom', default='H16a'); ap.add_argument('--left', default='VerticalEdge')
    ap.add_argument('--tag', default='H16a_VE'); ap.add_argument('--objective', default='crossings', choices=['crossings', 'turns'])
    ap.add_argument('--K', type=int, default=5); ap.add_argument('--time', type=float, default=60)
    ap.add_argument('--part', default='ab')
    a = ap.parse_args()
    B, L, TAG, OBJ, TL = load(a.bottom), load(a.left), a.tag, a.objective, a.time
    if 'a' in a.part: part_a()
    if 'b' in a.part: part_b(a.K)
