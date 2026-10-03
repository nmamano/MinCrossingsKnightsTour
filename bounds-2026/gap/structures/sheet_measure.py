"""Measure the Sheet Lemma quantities on validated tours (SHEET.md (B)). KT Structures, 2026-10-03.
BQ  = bad quarters in interior squares (all corners at distance >= d from the boundary).
SSR = chords (maximal tour subpaths whose vertices are all interior, i.e. distance >= d) with both ends on one side
      (the side nearest to the outside neighbour of each end; corner ends within d of two sides are dropped).
EXCp = proxy for exception slots: slot rows (columns) whose collar strip [0, d] holds a crossing count != 1
      (cheap patterns P, P' have exactly 1 crossing per row).
Prints BQ + 2 SSR + 2 EXCp against 4n, and E = X - 4n + 2.
usage: python sheet_measure.py [d] tour.json ...
"""
import sys
from collections import Counter
from cluster_scan import load, halves, cross
args = sys.argv[1:]
d = int(args[0]) if args and args[0].isdigit() else 3
files = [a for a in args if not a.isdigit()]
QH = {'B': ('BR', 'LB'), 'R': ('BR', 'RT'), 'T': ('TL', 'RT'), 'L': ('TL', 'LB')}
for path in files:
    n, es = load(path)
    nb = {}
    for a, b in es: nb.setdefault(a, []).append(b); nb.setdefault(b, []).append(a)
    cov = Counter()
    for e in es:
        for hk in halves(e): cov[hk] += 1
    inside = lambda p: d <= p[0] <= n-1-d and d <= p[1] <= n-1-d
    BQ = 0
    for i in range(d, n-1-d):
        for j in range(d, n-1-d):
            for q, (h1, h2) in QH.items():
                if cov[((i, j), h1)] + cov[((i, j), h2)] != 1: BQ += 1
    # crossings: X and per-row collar counts
    X = 0; rowc = Counter()
    es_list = list(es)
    from itertools import combinations
    by_cell = {}
    for e in es_list:
        (x1, y1), (x2, y2) = e
        for cx in range(min(x1, x2), max(x1, x2)):
            for cy in range(min(y1, y2), max(y1, y2)):
                by_cell.setdefault((cx, cy), []).append(e)
    seen = set()
    for cell, lst in by_cell.items():
        for e, f in combinations(lst, 2):
            key = (min(e, f), max(e, f))
            if key in seen or not cross(e, f): continue
            seen.add(key); X += 1
            # crossing point
            (p1, p2), (q1, q2) = e, f
            dx1, dy1 = p2[0]-p1[0], p2[1]-p1[1]; dx2, dy2 = q2[0]-q1[0], q2[1]-q1[1]
            den = dx1*dy2 - dy1*dx2
            t = ((q1[0]-p1[0])*dy2 - (q1[1]-p1[1])*dx2) / den
            cx, cy = p1[0] + t*dx1, p1[1] + t*dy1
            if cx <= d: rowc[('L', int(cy))] += 1
            if cx >= n-1-d: rowc[('R', int(cy))] += 1
            if cy <= d: rowc[('B', int(cx))] += 1
            if cy >= n-1-d: rowc[('T', int(cx))] += 1
    EXCp = 0
    for s in 'LRBT':
        for t in range(d, n-1-d):
            if rowc[(s, t)] != 1: EXCp += 1
    # chords
    def side(u):
        ds = {'L': u[0], 'R': n-1-u[0], 'B': u[1], 'T': n-1-u[1]}
        close = [s for s, v in ds.items() if v < d]
        return close[0] if len(close) == 1 else None
    vis = set(); SSR = 0; chords = 0; cross_ch = Counter()
    for v in list(nb):
        if not inside(v) or v in vis: continue
        comp = [v]; vis.add(v); k = 0
        while k < len(comp):
            for w in nb[comp[k]]:
                if inside(w) and w not in vis: vis.add(w); comp.append(w)
            k += 1
        ends = [(u, w) for u in comp for w in nb[u] if not inside(w)]
        if len(ends) != 2: continue      # interior cycles have 0 ends
        chords += 1
        s1, s2 = side(ends[0][1]), side(ends[1][1])
        if s1 and s1 == s2: SSR += 1
        elif s1 and s2: cross_ch[''.join(sorted(s1 + s2))] += 1
    E = X - 4*n + 2
    print(f'{path.split("/")[-1]}: n={n} d={d} X={X} E={E} BQ={BQ} SSR={SSR} chords={chords} cross={dict(cross_ch)} '
          f'EXCp={EXCp}  BQ+2SSR+2EXCp={BQ+2*SSR+2*EXCp} vs 4n={4*n};  price BQ/4+SSR/2+EXCp/2={BQ/4+SSR/2+EXCp/2:.1f} vs E', flush=True)
