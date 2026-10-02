"""Fold field + arch flips + 4 diagonal flux templates + CP-SAT windows -> validated tour. KT Structures."""
import sys, time, json
from paste import paste_field
from fold3 import comps
from repair import clusters, window_cells, repair
from imbal import imbalance
from global_strip import to_grid
from kt.core import validate, num_crossings, num_turns, crossing_list
n = int(sys.argv[1]); rad = int(sys.argv[2]); tl = float(sys.argv[3])
import json as _j
_L = _j.load(open('diag_multi_p6_w3_t1.json'))
_cells = {tuple(map(int, k.split(','))): [tuple(m) for m in v] for k, v in _L[int(sys.argv[4]) if len(sys.argv) > 4 else 0]['cells'].items()}
tgs = {0: _cells, 1: _cells, 2: _cells, 3: _cells}
t = 1; h = n // 2
fl = lambda r, y: h - n // 4 <= y < h
E, deg = paste_field(n, t, tgs, fl, hi=h - 4)
cs, cyc, bad = comps(n, E, deg)
cls = clusters(bad, link=4)
free = set()
hint = set(E)
for c in cls:
    free |= window_cells(n, c, rad)
EXTRA = int(sys.argv[5]) if len(sys.argv) > 5 else 0
if EXTRA:
    from paste import Rot
    for r in range(4):
        for fy in (1/8, 3/8, 5/8):
            y0 = int(fy * n)
            for x in range(0, 9):
                for y in range(y0 - 4, y0 + 5):
                    free.add(Rot((x, y), n, r))
import networkx as nx
Gf = nx.Graph(); Gf.add_nodes_from(free)
for (x, y) in free:
    for d in ((1, 0), (0, 1), (1, 1), (1, -1)):
        if (x + d[0], y + d[1]) in free: Gf.add_edge((x, y), (x + d[0], y + d[1]))
wins = [set(c) for c in nx.connected_components(Gf)]
print('windows', [len(w) for w in wins], flush=True)
print('n', n, 'pre: comps', len(cs), 'closed', len(cyc), 'bad', len(bad), 'clusters', len(cls), 'free', len(free),
      'imb', [imbalance(n, E, window_cells(n, c, rad)) for c in cls], 'X(pre)', len(crossing_list(E)), flush=True)
t0 = time.time()
from circuit import solve_circuit
Ef = solve_circuit(n, E, free, tl=300, feas_only=True)
from kt.core import crossing_list as _cl
E2 = Ef
print('feasible tour X', len(_cl(E2)), flush=True)
for ps in range(int(sys.argv[6]) if len(sys.argv) > 6 else 3):
    for wset in wins:
        E3 = solve_circuit(n, E2, wset, tl=tl, hint=E2, verbose=False)
        if E3 is not None:
            E2 = E3
    print('LNS pass', ps, 'X', len(_cl(E2)), flush=True)
st = 'circuit'
print('status', st, round(time.time() - t0), 's', flush=True)
if E2:
    g = to_grid(n, E2)
    X = num_crossings(g)
    print('RESULT n', n, 'valid', validate(g), 'X', X, 'X/n %.3f' % (X / n), 'T', num_turns(g), flush=True)
    json.dump([' '.join(r) for r in g], open(f'tours/fold_diag_n{n}.json', 'w'))
