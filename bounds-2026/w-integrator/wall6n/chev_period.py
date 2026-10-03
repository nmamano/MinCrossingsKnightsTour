#!/usr/bin/env python
"""Periodic (1,2) chevron walls in the fold field: measure the wall cost per level (KT Integrator, 2026-10-03).
Fold field + 13 windows (no diagonal corridors) + 4 free wall bands (left chevron BL->(n/4,n/2)->TL, right chevron
by symmetry). The middle of each band (levels lo .. h-lo) is tied to its translate along the wall by P*(1,+-2).
Solve: feasibility, then rounds of (objective re-solve of the tied middles, LNS on the rest).
Measure: crossing points inside one middle segment strip, per 2P rows (= per 2P levels).
Usage: chev_period.py n [--w 3] [--P 4] [--lo 16] [--rounds 3]"""
import argparse, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from fold_assemble import setup, edges_to_nb
from kt.board import complete, to_grid, lns
from kt.core import validate, num_crossings, num_turns, crossing_list
from assemble import walk_check

MOV = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

def segments(n):
    """(name, s(x,y) = signed transversal offset from the wall line, level(x,y), translation T for 2 rows... )"""
    h = n // 2
    return [  # wall line s = 0; level = rows from the corner
        ('LB', lambda x, y: x - y / 2.0, lambda x, y: y, (1, 2)),
        ('LT', lambda x, y: x - (n - 1 - y) / 2.0, lambda x, y: n - 1 - y, (1, -2)),
        ('RB', lambda x, y: (n - 1 - x) - y / 2.0, lambda x, y: y, (-1, 2)),
        ('RT', lambda x, y: (n - 1 - x) - (n - 1 - y) / 2.0, lambda x, y: n - 1 - y, (-1, -2)),
    ]

def setup_walls(n, w, P, lo):
    h = n // 2
    E, free, info = setup(n, 4, {}, 4, band=None)
    cells = [(x, y) for x in range(n) for y in range(n)]
    ties, mids = [], {}
    for name, s, lev, d in segments(n):
        band = {c for c in cells if abs(s(*c)) <= w and lev(*c) <= h}
        free |= band
        mid = {c for c in band if lo <= lev(*c) < h - lo}
        mids[name] = mid
        T = (P * d[0], P * d[1])
        for c in mid:
            for m in MOV:
                q = (c[0] + m[0], c[1] + m[1])
                c2, q2 = (c[0] + T[0], c[1] + T[1]), (q[0] + T[0], q[1] + T[1])
                if q in mid and c2 in mid and q2 in mid and c < q:
                    ties.append(((c, q), (c2, q2)))
    return E, free, mids, ties, info

def per_period(n, g_edges, name, w, P, lo, segs):
    """Crossing points with |s| <= w + 3 and level in [lo + 2P, h - lo - 2P), per 2P levels."""
    h = n // 2
    s, lev = [(sg[1], sg[2]) for sg in segs if sg[0] == name][0]
    from kt.core import crossing_list as _cl
    cnt = 0
    for (a, b), (c, d) in g_edges:
        # intersection point of segments ab and cd
        (x1, y1), (x2, y2), (x3, y3), (x4, y4) = a, b, c, d
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        px, py = x1 + t * (x2 - x1), y1 + t * (y2 - y1)
        if abs(s(px, py)) <= w + 3 and lo + 2 * P <= lev(px, py) < h - lo - 2 * P:
            cnt += 1
    span = max(1, (h - lo - 2 * P) - (lo + 2 * P))
    return cnt, span

def full_to_edges(full):
    return {tuple(sorted((c, v))) for c, s in full.items() for v in s}

def crossing_pairs(E):
    """All properly crossing pairs among knight edges (local search by cell)."""
    from collections import defaultdict
    by = defaultdict(list)
    for e in E:
        (x1, y1), (x2, y2) = e
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                by[(x, y)].append(e)
    def cross(e, f):
        (a, b), (c, d) = e, f
        if len({a, b, c, d}) < 4: return False
        o = lambda p, q, r: (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
        return o(a, b, c) * o(a, b, d) < 0 and o(c, d, a) * o(c, d, b) < 0
    seen = set(); out = []
    for es in by.values():
        for i in range(len(es)):
            for j in range(i + 1, len(es)):
                e, f = es[i], es[j]
                k = (e, f) if e < f else (f, e)
                if k in seen: continue
                seen.add(k)
                if cross(e, f): out.append(k)
    return out

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('n', type=int); ap.add_argument('--w', type=float, default=3); ap.add_argument('--P', type=int, default=4)
    ap.add_argument('--lo', type=int, default=16); ap.add_argument('--rounds', type=int, default=3)
    ap.add_argument('--ftime', type=float, default=600); ap.add_argument('--mtime', type=float, default=240)
    a = ap.parse_args(); n = a.n; t0 = time.time()
    E, free, mids, ties, info = setup_walls(n, a.w, a.P, a.lo)
    mid = set().union(*mids.values())
    print(f'n={n} w={a.w} P={a.P} lo={a.lo} free={len(free)} mid={len(mid)} ties={len(ties)} {info}', flush=True)
    nb = edges_to_nb(n, E)
    full, ci = complete(n, nb, free, time_limit=a.ftime, workers=2, feasibility=True, ties=ties)
    if full is None:
        print(f'RESULT n={n}: no tour ({ci}) {time.time() - t0:.0f}s', flush=True); sys.exit()
    print(f'  feasible X={num_crossings(to_grid(n, full))} {time.time() - t0:.0f}s', flush=True)
    segs = segments(n)
    for rnd in range(a.rounds):
        new, ci = complete(n, full, mid, time_limit=a.mtime, workers=2, hint=full, ties=ties)
        if new is not None: full = new
        Xm = num_crossings(to_grid(n, full))
        full = lns(n, full, free - mid, win=8, step=4, time_limit=20, workers=2, rounds=1)
        g = to_grid(n, full)
        cp = crossing_pairs(full_to_edges(full))
        meas = {nm: per_period(n, cp, nm, a.w, a.P, a.lo, segs) for nm in mids}
        print(f'  round {rnd}: mid {ci.get("status") if isinstance(ci, dict) else ci} X={Xm} -> LNS X={num_crossings(g)} '
              f'(pairs {len(cp)}) per-level {{{", ".join(f"{k}: {c}/{s}={c / s:.3f}" for k, (c, s) in meas.items())}}} '
              f'{time.time() - t0:.0f}s', flush=True)
    g = to_grid(n, full)
    ok = validate(g) and walk_check(g)
    print(f'RESULT n={n} w={a.w} P={a.P}: valid={ok} X={num_crossings(g)} T={num_turns(g)} {time.time() - t0:.0f}s', flush=True)
    json.dump(dict(n=n, w=a.w, P=a.P, lo=a.lo, tour=g), open(os.path.join(HERE, f'chevP_n{n}_w{a.w}_P{a.P}.json'), 'w'))
