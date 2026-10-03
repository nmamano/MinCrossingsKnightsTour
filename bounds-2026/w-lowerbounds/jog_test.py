"""Insert a 'jog band' (two parallel free diagonal folds) into the lower arm of the left chevron
and check whether the chevron loops disappear (untrapping)."""
import sys
import networkx as nx
import fold_complete2
from fold_board import field as field0
from fold_complete import total_crossings
n = int(sys.argv[1]); t1 = int(sys.argv[2]); dl = int(sys.argv[3])
TS = (-1, -1, -1, -1); MS = (0, 1, 0, 1)
def field_jog(n_, **kw):
    v = field0(n_, **kw)
    h = n_ // 2
    for (x, y), d in list(v.items()):
        if d == (2, 1) and x < h and y < h + MS[3] and t1 <= x - y < t1 + dl:
            v[(x, y)] = (-1, -2)
    return v
for label, fld in (('no jog', field0), ('jog', field_jog)):
    fold_complete2.field = fld
    E, deg = fold_complete2.base(n, ts=TS, ms=MS)
    G = nx.Graph(); G.add_edges_from(E)
    comps = list(nx.connected_components(G))
    closed = [c for c in comps if all(deg[p] == 2 for p in c)]
    bad = sorted(p for p in G if deg[p] != 2)
    left = [c for c in closed if min(p[0] for p in c) == 0 and max(p[0] for p in c) < n // 2 and not any(p[1] in (0, n - 1) for p in c)]
    print(f'{label}: crossings {total_crossings(E)} components {len(comps)} closed {len(closed)} left-chevron loops {len(left)} defect cells {len(bad)}')
    if label == 'jog':
        print('  defect cells:', [p for p in bad if p[0] < n // 2 and p[1] < n // 2 + 2][:30])
