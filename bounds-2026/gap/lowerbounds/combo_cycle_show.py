#!/usr/bin/env python3
"""Decode the blocking cycle of combo_stab.py crit ORIENT into a periodic field (edges per row) and save it.
Edges introduced in a row are exactly the pending edges of the next phase-0 state with lower end at row -1."""
import sys, json
import numpy as np
import frac_stab as FS
from combo_stab import row_arcs, NS, CAP

orient = sys.argv[1]
R, N = row_arcs(orient)
states, W, src, dst, wt = FS.graph()
cyc = np.load(f"combo_cycle_{orient}.npy" if CAP == 4 else f"combo_cycle_{orient}_cap{CAP}.npy")
ra = cyc // NS
nodes = {}
for a in cyc:
    r = a // NS; c = a % NS
    nodes[(int(R[r][0]), int(c))] = a
# order: follow S -> D
def head(a):
    r = a // NS; c = a % NS
    return r
order = list(cyc)
# reconstruct order using the node ids
from combo_stab import augment
S_, D_, *_ = augment(R[np.unique(ra)], N)  # small: only the rows involved
# simpler: rebuild node ids directly
P = lambda c: (c // 80, (c % 80) // 5, c % 5)
src_node = {}
for a in cyc:
    r = int(a // NS); c = int(a % NS)
    src_node[(int(R[r][0]) * NS + c)] = a
E = []
a = cyc[0]
seen = []
for _ in range(len(cyc)):
    seen.append(a)
    r = int(a // NS); c = int(a % NS)
    u0, v0 = int(R[r][0]), int(R[r][1])
    # recompute target node id exactly as augment does
    sub, Nn = R[r:r + 1], N
    S1, D1, *_ = augment(sub, Nn)
    tgt = int(D1[c])
    a = src_node[tgt]
rows = []
for y, a in enumerate(seen):
    r = int(a // NS); v0 = int(R[r][1])
    for e in states[v0][1]:
        if e[1] == -1:
            rows.append([[e[0], y], [e[2], e[3] + 1 + y]])
print('period', len(seen), 'rows; edges:', sorted(rows))
json.dump({'period': len(seen), 'edges': rows}, open(f'combo_field_{orient}' + ('' if CAP == 4 else f'_cap{CAP}') + '.json', 'w'))
