#!/usr/bin/env python3
"""Beyond-5n pilot (KT Lower Bounds, 2026-10-03): per-side ledger on real tours.

For each side (local frame: x = distance from the side, y along the side) and the rows R0 <= r <= n-1-R0:
  XS   = crossing pairs of width-two edges (an end in local column 0 or 1), counted at the row of the lower end
         of the later edge (scan order (y, x)), as in the strip graph;
  gU, gD = rows with g = 1 (strong test, up / down orientation; f1v_stab.py definitions);
  NRE  = changed ports (exact, Structures nre_scan.py definition), counted at the row of the collar vertex;
  NSS  = changed ports whose collar partner is a steep port of the same side (both ends steep);
  NLOC = ports NOT on a local P path (4,y+1)-(2,y)-(0,y-1)-(1,y+1)-(3,y+2) or its mirror y -> -y (NLOC >= NRE).
Prints XS - rows - g, and the ratio (XS - rows - g) / NRE (an upper bound for the joint constant c on that tour,
up to the side-end constant).
usage: tour_scan.py TOUR.json [R0]
"""
import sys, json
from itertools import combinations
from pathlib import Path
from collections import defaultdict
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE.parent / 'windows'))
sys.path.insert(0, str(HERE.parent.parent / 'structures'))
import frac_stab as FS
from strip_dp import cross
from f1v_stab import tile_quarters
import nre_scan

MOVES = None


def load(f):
    import fold_exact_scan as F
    grid = json.loads(Path(f).read_text())['tour']; n = len(grid)
    E = {F.edge((x, n - 1 - y), (x + F.MOVES[int(v)][1], n - 1 - y - F.MOVES[int(v)][0]))
         for y, row in enumerate(grid) for x, code in enumerate(row) for v in code}
    return n, E


def vis_pairs(es, r):
    """VIS(r): crossing width-two pair, not both at column 0, two-quarter overlap with a quarter in squares (1..3, r)."""
    for e, f in combinations(es, 2):
        if not cross(e, f): continue
        if 0 in (e[0], e[2]) and 0 in (f[0], f[2]): continue
        ov = tile_quarters(e) & tile_quarters(f)
        if len(ov) == 2 and any(x in (1, 2, 3) and y == r for x, y, q in ov): return 1
    return 0


def side_ledger(n, E, s, R0, changed_rows, nloc_rows, ss_rows=None):
    T = [lambda v: v, lambda v: (n - 1 - v[0], v[1]), lambda v: (v[1], v[0]), lambda v: (n - 1 - v[1], v[0])][s]
    loc = [tuple(sorted((T(a), T(b)), key=lambda p: (p[1], p[0]))) for a, b in E]
    w2 = [(a[0], a[1], b[0], b[1]) for a, b in loc if min(a[0], b[0]) <= 1]   # lower end first (scan order)
    order = sorted(w2, key=lambda e: (e[1], e[0]))
    rows = range(R0, n - R0)
    XS = defaultdict(int)
    for i, f in enumerate(order):
        for e in order[:i]:
            if cross(e, f): XS[f[1]] += 1
    out = dict(rows=len(rows), XS=sum(XS[r] for r in rows))
    for orient in ('up', 'down'):
        coef, exc = FS.test(orient)
        g = 0
        for r in rows:
            F = 0; Ex = 0
            for (ax, ay, bx, by) in w2:
                k = FS.key((ax, ay - r), (bx, by - r)); F += coef.get(k, 0); Ex += k in exc
            near = [e for e in w2 if r - 3 <= e[1] <= r + 1 and e[3] >= r]
            vr = r if orient == 'up' else r - 1
            nearv = [e for e in w2 if vr - 3 <= e[1] <= vr + 1 and e[3] >= vr]
            g += 1 if (F % 3 != 2 or Ex >= 2 or vis_pairs(nearv, vr)) else 0
        out['g' + orient[0].upper()] = g
    out['NRE'] = sum(changed_rows[s][r] for r in rows)
    out['NLOC'] = sum(nloc_rows[s][r] for r in rows)
    if ss_rows: out['NSS'] = sum(ss_rows[s][r] for r in rows)
    return out


def main():
    f = sys.argv[1]; R0 = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    n, E = load(f)
    res = nre_scan.scan(f)
    # recompute per-port data (nre_scan returns totals only): exact changed ports and the local P test
    import fold_exact_scan as F
    Ts = [lambda v: v, lambda v: (n - 1 - v[0], v[1]), lambda v: (v[1], v[0]), lambda v: (n - 1 - v[1], v[0])]
    inside = lambda v: all(3 <= z <= n - 4 for z in v)
    adj = defaultdict(set)
    for a, b in E: adj[a].add(b); adj[b].add(a)
    changed_rows = [defaultdict(int) for _ in range(4)]; nloc_rows = [defaultdict(int) for _ in range(4)]
    ss_rows = [defaultdict(int) for _ in range(4)]
    Eset = set(E)
    ports = {}
    for a, b in E:
        if inside(a) == inside(b): continue
        o, q = (b, a) if inside(a) else (a, b)
        sd = [i for i, t in enumerate(Ts) if t(o)[0] < 3]
        if len(sd) != 1: continue
        L = Ts[sd[0]]; lo, lq = L(o), L(q); d = (lq[0] - lo[0], lq[1] - lo[1])
        sgn = 1 if d[0] * d[1] > 0 else -1
        lab = lq[0] - 2 * lq[1] if sgn == 1 else lq[0] + 2 * lq[1]
        ports[(o, q)] = dict(side=sd[0], sgn=sgn, steep=abs(d[0]) == 2, lab=lab, row=lo[1], lo=lo, lq=lq)
    def partner(o, q):
        prev, cur = q, o
        while True:
            nx = next(v for v in adj[cur] if v != prev); prev, cur = cur, nx
            if inside(cur): return (prev, cur)
    for k, p in ports.items():
        pp = ports.get(partner(*k))
        ok = pp and p['steep'] and pp['steep'] and pp['side'] == p['side'] and pp['sgn'] == p['sgn'] \
            and pp['lab'] - p['lab'] == (-3 if p['lab'] % 2 == 0 else 3)
        if not ok: changed_rows[p['side']][p['row']] += 1
        if not ok and pp and p['steep'] and pp['steep'] and pp['side'] == p['side']: ss_rows[p['side']][p['row']] += 1
        # local P path in the side frame
        Linv = {0: lambda v: v, 1: lambda v: (n - 1 - v[0], v[1]), 2: lambda v: (v[1], v[0]), 3: lambda v: (v[1], n - 1 - v[0])}[p['side']]
        assert Linv(Ts[p['side']](k[0])) == k[0]
        lo, lq = p['lo'], p['lq']
        def has(u, v): return tuple(sorted((Linv(u), Linv(v)))) in Eset
        y = lo[1]; loc_ok = False
        for sg in (1, -1):
            if lo[0] == 2 and lq == (4, y + sg):
                loc_ok |= has((2, y), (0, y - sg)) and has((0, y - sg), (1, y + sg)) and has((1, y + sg), (3, y + 2 * sg))
            if lo[0] == 1 and lq == (3, y + sg):
                y2 = y - sg
                loc_ok |= has((4, y2 + sg), (2, y2)) and has((2, y2), (0, y2 - sg)) and has((0, y2 - sg), (1, y))
        if not loc_ok: nloc_rows[p['side']][p['row']] += 1
    tot = defaultdict(int)
    print(Path(f).name, 'n', n, 'N_re(all)', res['N_re'])
    for s in range(4):
        L = side_ledger(n, E, s, R0, changed_rows, nloc_rows, ss_rows)
        for k, v in L.items(): tot[k] += v
        print(' side', s, L)
    for o in ('U', 'D'):
        slack = tot['XS'] - tot['rows'] - tot['g' + o]
        print(f' total {dict(tot)}  orient {o}: XS-rows-g = {slack}, /NRE = {slack / max(tot["NRE"], 1):.4f}, /NLOC = {slack / max(tot["NLOC"], 1):.4f}, /NSS = {slack / max(tot["NSS"], 1):.4f}')


if __name__ == '__main__':
    main()
