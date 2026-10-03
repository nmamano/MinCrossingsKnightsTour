#!/usr/bin/env python3
"""Print one SAT witness of tree_islands.sat_check: per U square the n values (BR,TL,RT,LB), m (B,R,T,L), and
the active links (side: '/'/'\\') on U sides, plus degrees at U corners.  usage: [env] show_links.py s index"""
import sys
import tree_islands as T
s, idx = int(sys.argv[1]), int(sys.argv[2])
tp = sorted(T.tree_polyominoes(s)[s])
cnt = 0
for P in tp:
    U = [(x + 10, y + 10) for x, y in P]
    bs, labs = T.labellings(U)
    for lab, cuts in labs:
        r, model, _, edges, vid = T.sat_check(U, lab, cuts)
        if not r: continue
        if cnt < idx: cnt += 1; continue
        ms = set(l for l in model if l > 0)
        on = lambda S, d, sg: int(vid[T.link(S, d, sg)] in ms)
        n = lambda S, h: on(S, h[0], '/' if h in T.SPL['/'] else '\\') + on(S, h[1], '/' if h in T.SPL['/'] else '\\')
        print('U', U, 'label', set(lab.values()))
        for S in sorted(U):
            ns = {h: n(S, h) for h in ('BR', 'TL', 'RT', 'LB')}
            m = {q: ns[a] + ns[b] for q, (a, b) in T.QH.items()}
            print(f'  S={S} n={ns} m={m} links /:{ {d: on(S, d, "/") for d in "BRTL"} } \\:{ {d: on(S, d, chr(92)) for d in "BRTL"} }')
        for sg, e, f, hs in cuts: print('  cut', sg, e, f, 'k', len(hs), 'y0', on(e[0], e[1], sg), 'yk', on(f[0], f[1], sg))
        deg = {}
        for e in edges:
            if vid[e] in ms:
                for p in e: deg[p] = deg.get(p, 0) + 1
        corners = sorted({(x + a, y + b) for (x, y) in U for a in (0, 1) for b in (0, 1)})
        print('  corner degrees', {c: deg.get(c, 0) for c in corners})
        sys.exit()
