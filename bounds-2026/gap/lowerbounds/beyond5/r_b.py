#!/usr/bin/env python3
"""BEYOND5 request R-b (KT Lower Bounds, 2026-10-03): G_free and N_free(d0) per side on real tours.

Side frames as in tour_scan.py (side 0 left, 1 right, 2 bottom, 3 top; local x = distance from the side, local y
along it). Rows 8..n-9. g(r) = F1-V strong test in the orientation that points away from the nearer corner:
up for r < n/2, down for r >= n/2 (the orientation of the corner candidates that end at that row).
Candidates (fx, fy, r), 12 <= r < n/2 - 3 (check_hall_v3.retained): left/right end at side 0/1 row r or n-1-r,
bottom/top end at side 2/3 row r or n-1-r. LOST = not retained; DEFICIENT = retained with s_i < 2 payable quarters
in its squares (beyond5_ledger.py definition, copied). Each lost / deficient candidate OWNS one end row with g = 1
(vertical-side end first if both ends have g = 1); a candidate with no g end is reported (Claim V says none).
G_free = #g rows - #owned rows. N_free(d0) = changed ports (nre_scan definition, counted at the collar vertex row)
at distance > d0 from every g row of the side.
usage: r_b.py TOUR.json ...
"""
import sys, json
from pathlib import Path
from collections import defaultdict
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(ROOT / 'gap/turnstheory')); sys.path.insert(0, str(ROOT / 'gap/verifier'))
import tour_scan as TS
import frac_stab as FS
from check_hall_v3 import geometry
from claim38_switch import edge, qs
from check import MOVES


def gfun(w2, r, orient):
    coef, exc = FS.test(orient)
    F = sum(coef.get(FS.key((a, b - r), (c, d - r)), 0) for a, b, c, d in w2)
    Ex = sum(FS.key((a, b - r), (c, d - r)) in exc for a, b, c, d in w2)
    vr = r if orient == 'up' else r - 1
    near = [e for e in w2 if vr - 3 <= e[1] <= vr + 1 and e[3] >= vr]
    return 1 if (F % 3 != 2 or Ex >= 2 or TS.vis_pairs(near, vr)) else 0


def run(f):
    grid = json.loads(Path(f).read_text())['tour']
    info, cs, atoms = geometry(grid); n = info['n']
    es = {edge((x, n - 1 - y), (x + MOVES[int(v)][1], n - 1 - y - MOVES[int(v)][0])) for y, row in enumerate(grid) for x, code in enumerate(row) for v in code}
    own = defaultdict(list)
    for e in es:
        for q in qs(e): own[q].append(e)
    lookup = {(a[0], a[3]): j for j, a in enumerate(atoms)}
    def payable(q):
        ls = own[q]; m = len(ls)
        if m == 1: return None
        if not m: return lookup['G', q]
        if m >= 3: return lookup['W3', q]
        pair = tuple(sorted(ls)); return lookup.get(('pair', pair), lookup.get(('X1', pair)))
    def squares(c):
        fx, fy, r = c
        return [(n - 2 - x if fx else x, n - 2 - y if fy else y) for x, y in [(r, j) for j in range(1, r + 1)] + [(i, r) for i in range(r - 1, 0, -1)]]
    retained = set(cs)
    allc = [(fx, fy, r) for fx in (0, 1) for fy in (0, 1) for r in range(12, n // 2 - 3)]
    s = {c: sum(1 for x, y in squares(c) for k in range(4) if payable((x, y, k)) is not None) for c in cs}
    lost = [c for c in allc if c not in retained]; deficient = [c for c in cs if s[c] < 2]
    # per side: g rows and changed ports
    n_, E = TS.load(f)
    Ts = [lambda v: v, lambda v: (n - 1 - v[0], v[1]), lambda v: (v[1], v[0]), lambda v: (n - 1 - v[1], v[0])]
    rows = range(8, n - 8)
    G = []
    for sd in range(4):
        loc = [tuple(sorted((Ts[sd](a), Ts[sd](b)), key=lambda p: (p[1], p[0]))) for a, b in E]
        w2 = [(a[0], a[1], b[0], b[1]) for a, b in loc if min(a[0], b[0]) <= 1]
        G.append({r: gfun(w2, r, 'up' if r < n / 2 else 'down') for r in rows})
    # changed ports by collar row (exact nre_scan definition)
    inside = lambda v: all(3 <= z <= n - 4 for z in v)
    adj = defaultdict(set)
    for a, b in E: adj[a].add(b); adj[b].add(a)
    ports = {}
    for a, b in E:
        if inside(a) == inside(b): continue
        o, q = (b, a) if inside(a) else (a, b)
        sd = [i for i, t in enumerate(Ts) if t(o)[0] < 3]
        if len(sd) != 1: continue
        lo, lq = Ts[sd[0]](o), Ts[sd[0]](q); d = (lq[0] - lo[0], lq[1] - lo[1])
        sgn = 1 if d[0] * d[1] > 0 else -1
        ports[(o, q)] = dict(side=sd[0], sgn=sgn, steep=abs(d[0]) == 2, lab=lq[0] - 2 * lq[1] if sgn == 1 else lq[0] + 2 * lq[1], row=lo[1])
    def partner(o, q):
        prev, cur = q, o
        while True:
            nx = next(v for v in adj[cur] if v != prev); prev, cur = cur, nx
            if inside(cur): return (prev, cur)
    chg = [defaultdict(int) for _ in range(4)]
    for k, p in ports.items():
        pp = ports.get(partner(*k))
        ok = pp and p['steep'] and pp['steep'] and pp['side'] == p['side'] and pp['sgn'] == p['sgn'] \
            and pp['lab'] - p['lab'] == (-3 if p['lab'] % 2 == 0 else 3)
        if not ok: chg[p['side']][p['row']] += 1
    # ownership
    def ends(c):
        fx, fy, r = c
        return [(1 if fx else 0, n - 1 - r if fy else r), (3 if fy else 2, n - 1 - r if fx else r)]
    owned = [0] * 4; noend = []
    for c in lost + deficient:
        e = [(sd, r) for sd, r in ends(c) if G[sd].get(r)]
        if not e: noend.append(c); continue
        owned[e[0][0]] += 1
    out = dict(tour=Path(f).name, n=n, lost=len(lost), deficient=len(deficient), no_g_end=noend, sides=[])
    tot = defaultdict(int)
    for sd in range(4):
        grows = [r for r in rows if G[sd][r]]
        rec = dict(g=len(grows), owned=owned[sd], G_free=len(grows) - owned[sd], N_re=sum(chg[sd][r] for r in rows))
        for d0 in (1, 2, 3):
            rec[f'N_free{d0}'] = sum(chg[sd][r] for r in rows if all(abs(r - t) > d0 for t in grows))
        out['sides'].append(rec)
        for k, v in rec.items(): tot[k] += v
    out['total'] = dict(tot)
    return out


if __name__ == '__main__':
    for f in sys.argv[1:]:
        r = run(f)
        print(r['tour'], 'n', r['n'], 'lost', r['lost'], 'deficient', r['deficient'], 'no g end', r['no_g_end'])
        for sd, rec in enumerate(r['sides']): print('  side', sd, rec)
        print('  total', r['total'], flush=True)
