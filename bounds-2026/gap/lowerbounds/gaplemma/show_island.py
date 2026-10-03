#!/usr/bin/env python3
"""Print per-square bad-quarter counts of SAT witnesses of tree_islands.sat_check (slack runs).
usage: SLACK=1 show_island.py SMIN SMAX"""
import sys, os
sys.argv = sys.argv[:1] + sys.argv[1:]
import tree_islands as T
SMIN, SMAX = int(sys.argv[1]), int(sys.argv[2])
tp = T.tree_polyominoes(SMAX)
for s in range(SMIN, SMAX + 1):
    for P in sorted(tp[s]):
        U = [(x + 10, y + 10) for x, y in P]
        bs, labs = T.labellings(U)
        for lab, cuts in labs:
            r, model, _, edges, vid = T.sat_check(U, lab, cuts)
            if not r: continue
            ms = set(l for l in model if l > 0)
            on = lambda S, d, sg: T.vid if False else (vid[T.link(S, d, sg)] in ms)
            def n(S, h):
                sg = '/' if h in T.SPL['/'] else '\\'
                return on(S, h[0], sg) + on(S, h[1], sg)
            bq = {S: sum((n(S, a) + n(S, b)) != 1 for q, (a, b) in T.QH.items()) for S in U}
            xs = [u[0] for u in U] + [u[0] for u in lab]; ys = [u[1] for u in U] + [u[1] for u in lab]
            print(f's={s} label {set(lab.values())} excess {sum(bq.values()) - 2 * s}; cuts (k, y0, yk):',
                  [(len(hs), int(on(e[0], e[1], sg)), int(on(f[0], f[1], sg))) for sg, e, f, hs in cuts])
            for y in range(max(ys), min(ys) - 1, -1):
                print('   ' + ''.join(str(bq[(x, y)]) if (x, y) in bq else (lab[(x, y)] if (x, y) in lab else '.')
                                      for x in range(min(xs), max(xs) + 1)))
