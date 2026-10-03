"""Topology test of the B'/B layout (KT Edge Searcher, gap mission, 2026-10-03).
Field: (1,2) lines for x <= h-1, (1,-2) lines for x >= h (free vertical fold at x = h).
Bottom/top edges: steep cheap U-turn pattern P (rotated F12 edge pattern). Left/right edges: shallow, a periodic
corr2 edgeB template (depth 4, 11/6 crossings per row) pasted with a row phase. Corners, the fold ends and the
bottom nest are NOT repaired here: the script reports the components, so that we can see which nests are trapped.
usage: python3 nest_test.py n phaseL phaseR [template-current]"""
import sys, json
from collections import defaultdict

def build(n, phL, phR, tpl, flips=()):
    h = n // 2
    on = lambda c: 0 <= c[0] < n and 0 <= c[1] < n
    out = lambda c: (1, 2) if c[0] <= h - 1 else (1, -2)
    E = set()
    for x in range(n):
        for y in range(n):
            c = (x, y); d = out(c); q = (x + d[0], y + d[1])
            if on(q): E.add(tuple(sorted((c, q))))
    # left edge band x in 0..3: remove base edges inside the band, paste template
    def paste(side, ph):
        R = tpl['rows']
        mir = (lambda c: c) if side == 'L' else (lambda c: (n - 1 - c[0], c[1]))
        band = lambda c: 0 <= mir(c)[0] <= 3
        for e in list(E):
            if band(e[0]) and band(e[1]): E.discard(e)
        for k in range(-2, n // R + 3):
            for a0, b0, a1, b1 in tpl['edges']:
                p = mir((a0, b0 + ph + k * R)); q = mir((a1, b1 + ph + k * R))
                if on(p) and on(q): E.add(tuple(sorted((p, q))))
    paste('L', phL)
    # mirror template for the right edge: field (1,-2) at the right wall is the x-mirror of (1,2)?
    # x-mirror maps direction (1,2) to (-1,2) = -(1,-2): yes, same undirected lines.
    paste('R', phR)
    # bottom: P (x,0)-(x+2,1) in the (1,2) half, (x,0)-(x-2,1) in the (1,-2) half; top: reflected
    for x in range(n):
        if x <= h - 1:
            if on((x + 2, 1)): E.add(((x, 0), (x + 2, 1)))
            if on((x - 2, n - 2)): E.add(tuple(sorted(((x, n - 1), (x - 2, n - 2)))))
        else:
            if on((x - 2, 1)): E.add(tuple(sorted(((x, 0), (x - 2, 1)))))
            if on((x + 2, n - 2)): E.add(tuple(sorted(((x, n - 1), (x + 2, n - 2)))))
    return E

def components(n, E):
    adj = defaultdict(list)
    for a, b in E: adj[a].append(b); adj[b].append(a)
    seen = set(); comps = []
    for x in range(n):
        for y in range(n):
            s = (x, y)
            if s in seen: continue
            st = [s]; seen.add(s); cs = []
            while st:
                u = st.pop(); cs.append(u)
                for v in adj[u]:
                    if v not in seen: seen.add(v); st.append(v)
            cyc = all(len(adj[u]) == 2 for u in cs)
            comps.append((cyc, cs))
    return comps, adj

if __name__ == '__main__':
    n, phL, phR = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    cur = int(sys.argv[4]) if len(sys.argv) > 4 else -1
    tpl = [d for d in map(json.loads, open('eB4.jsonl')) if d.get('rate_per_row') == '11/6' and d['current'] == cur][0]
    E = build(n, phL, phR, tpl)
    comps, adj = components(n, E)
    bad = sum(1 for x in range(n) for y in range(n) if len(adj[(x, y)]) != 2)
    cyc = [c for c in comps if c[0]]
    print(f'n={n} phL={phL} phR={phR}: {len(comps)} components, {len(cyc)} closed cycles, {bad} cells with degree != 2')
    def where(cs):
        xs = [c[0] for c in cs]; ys = [c[1] for c in cs]
        return (min(xs), max(xs), min(ys), max(ys))
    for c in sorted(cyc, key=lambda c: -len(c[1]))[:12]:
        print('  cycle size', len(c[1]), 'box', where(c[1]))
