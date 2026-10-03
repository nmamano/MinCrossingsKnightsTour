"""Print and independently re-check the single-cut half-version witness (single_cut.py, k=5). KT Structures, 2026-10-03."""
import sys
sys.argv = ['x', '10', '5', '5', '120', 'HALF']
src = open('single_cut.py').read().split('for k in range(k0')[0]
src = src.replace("    return s.StatusName(st), s.ObjectiveValue(), s.BestObjectiveBound()",
                  "    return s, E, nodes, y")
exec(src)
s, E, nodes, y = run(5, 'BR')
edges = [kk for kk, v in E.items() if s.Value(v)]
# independent recomputation from the edge list
cov = {}
for (x, yy, t) in edges:
    for hk in halves(x, yy, t): cov[hk] = cov.get(hk, 0) + 1
n = lambda sq, h: cov.get((sq, h), 0)
mq = lambda sq, q: n(sq, QH[q][0]) + n(sq, QH[q][1])
deg = {}
for (x, yy, t) in edges:
    dx, dy = MV[t]
    for pt in ((x, yy), (M(x+dx), M(yy+dy))): deg[pt] = deg.get(pt, 0) + 1
assert all(deg.get((i, j), 0) == 2 for i in range(p) for j in range(p))
print('nodes', nodes); print('y', [s.Value(v) for v in y])
for sq, h in nodes:
    print(sq, h, 'n=', n(sq, h), 'quarters', {q: mq(sq, q) for q in 'BRTL'},
          'halves', {hh: n(sq, hh) for hh in ('BR', 'TL', 'RT', 'LB')})
print('bad quarters in gap halves:', sum(mq(sq, q) != 1 for sq, h in nodes[1:-1] for q in h))
print('edges', sorted(edges))
