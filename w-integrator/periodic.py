#!/usr/bin/env python
"""Period-in-n argument + reused corner completions for ANY gadget combo (generalises period24.py).

(a) with fixed phases (xb, xt, yl, yr): region rules for every even n in a range, the outside path
    matching (zone-relative ends of all fixed paths) for every n, and its smallest period p in n.
(b) for each even residue class mod p: solve the four ZxZ corner zones once at the smallest
    n0 >= --nmin, then reuse them unchanged at n0 + p*k (k = 0..K); validate and count each tour.
Usage:
  periodic.py --bottom gadgets/b_T16.json --left gadgets/l_free.json --right gadgets/l_d5lowm20.json \
      --phases 0,1,0,0 --objective turns --tag TT16 [--part ab] [--K 3]
"""
import argparse, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from kt.board import build_general, complete, to_grid, fixed_paths
from kt.core import validate, num_crossings, num_turns
from assemble import load_tpl, walk_check
from strands import pairing, region_check

def corners(n, Z):
    return {'BL': (0, 0), 'BR': (n - Z, 0), 'TL': (0, n - Z), 'TR': (n - Z, n - Z)}

def zone_of(n, Z, c):
    for k, (cx, cy) in corners(n, Z).items():
        if cx <= c[0] < cx + Z and cy <= c[1] < cy + Z:
            return k, (c[0] - cx, c[1] - cy)

class Combo:
    def __init__(self, B, T, L, R, phases, Z):
        self.B, self.T, self.L, self.R, self.ph, self.Z = B, T, L, R, phases, Z
        self.p = [pairing(B, 'bottom'), pairing(L, 'left'), pairing(R, 'left'), pairing(T, 'bottom')]

    def skeleton(self, n):
        return build_general(n, self.B, self.L, self.T, self.R, phases=self.ph, Z=self.Z)

    def regions_ok(self, n):
        prof = region_check(*self.p, n, self.ph)
        return all(not r['cycles'] and not any(c % 2 for c in r['cuts']) for r in prof.values()), \
            {k: r['strands'] for k, r in prof.items()}

    def outside(self, n):
        nb, free = self.skeleton(n)
        paths, closed = fixed_paths(n, nb, free)
        if closed: return None
        m = set()
        for (u, v, cells) in paths:
            a = zone_of(n, self.Z, u) + (tuple(x - y for x, y in zip(cells[0], u)),)
            b = zone_of(n, self.Z, v) + (tuple(x - y for x, y in zip(cells[-1], v)),)
            m.add(tuple(sorted([a, b])))
        return frozenset(m)

    def zone_content(self, n, full):
        out = {}
        for k, (cx, cy) in corners(n, self.Z).items():
            for x in range(self.Z):
                for y in range(self.Z):
                    c = (cx + x, cy + y)
                    out[f'{k}:{x},{y}'] = sorted([v[0] - c[0], v[1] - c[1]] for v in full[c])
        return out

    def apply(self, n, content):
        nb, free = self.skeleton(n)
        full = {c: set(v) for c, v in nb.items()}
        cs = corners(n, self.Z)
        for key, ds in content.items():
            k, xy = key.split(':'); x, y = map(int, xy.split(','))
            c = (cs[k][0] + x, cs[k][1] + y)
            full[c] = {(c[0] + d[0], c[1] + d[1]) for d in ds}
        return full

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--bottom', required=True); ap.add_argument('--top'); ap.add_argument('--left', required=True)
    ap.add_argument('--right'); ap.add_argument('--phases', required=True); ap.add_argument('--Z', type=int, default=6)
    ap.add_argument('--objective', default='crossings', choices=['crossings', 'turns'])
    ap.add_argument('--tag', required=True); ap.add_argument('--part', default='ab')
    ap.add_argument('--nmin', type=int, default=48); ap.add_argument('--nmax', type=int, default=200)
    ap.add_argument('--K', type=int, default=3); ap.add_argument('--time', type=float, default=120)
    a = ap.parse_args()
    B, L = load_tpl(a.bottom), load_tpl(a.left)
    T = load_tpl(a.top) if a.top else B; R = load_tpl(a.right) if a.right else L
    C = Combo(B, T, L, R, tuple(int(v) for v in a.phases.split(',')), a.Z)
    ns = list(range(a.nmin, a.nmax + 1, 2))
    M, bad = {}, []
    for n in ns:
        ok, st = C.regions_ok(n)
        M[n] = C.outside(n) if ok else None
        if not ok or M[n] is None: bad.append(n)
    print(f'{a.tag}: phases {C.ph}; n with failing region rules or closed fixed cycles: {bad}')
    period = None
    for p in range(2, 97, 2):
        if all(M[n] == M[n + p] for n in ns if n + p in M and M[n] is not None):
            period = p; break
    print(f'smallest period of the outside matching in n (checked n = {ns[0]}..{ns[-1]}): {period}')
    if 'b' not in a.part or period is None: return
    os.makedirs(os.path.join(HERE, 'corners'), exist_ok=True)
    w = dict(turn_weight=1, crossing_weight=1000) if a.objective == 'crossings' else dict(turn_weight=1000, crossing_weight=1)
    print(f'objective {a.objective} first. res n0 | n0+{period}k: valid, X, T')
    for n0 in range(a.nmin, a.nmin + period, 2):
        if M.get(n0) is None:
            print(f'{n0 % period:>3} {n0:>3} skipped (bad)'); continue
        nb, free = C.skeleton(n0)
        full, info = complete(n0, nb, free, time_limit=a.time, workers=3, **w)
        if full is None:
            print(f'{n0 % period:>3} {n0:>3} completion failed: {info}', flush=True); continue
        content = C.zone_content(n0, full)
        json.dump(dict(n0=n0, period=period, residue=n0 % period, Z=a.Z, phases=C.ph, objective=a.objective,
                       bottom=B, top=T, left=L, right=R, info=info, zones=content,
                       note='zone-relative moves (dx, dy), x right, y up; corners BL=(0,0), BR=(n-Z,0), '
                            'TL=(0,n-Z), TR=(n-Z,n-Z); apply to kt.board.build_general(n, bottom, left, top, right, phases, Z)'),
                  open(os.path.join(HERE, 'corners', f'{a.tag}_res{n0 % period:02d}.json'), 'w'))
        row = []
        for k in range(a.K + 1):
            n = n0 + period * k
            g = to_grid(n, C.apply(n, content))
            ok = validate(g) and walk_check(g)
            row.append(f'{n}:{"ok" if ok else "BAD"} X={num_crossings(g)} T={num_turns(g)}')
        print(f'{n0 % period:>3} {n0:>3} {info["status"]} | ' + ' | '.join(row), flush=True)

if __name__ == '__main__':
    main()
