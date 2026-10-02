#!/usr/bin/env python3
"""Minimum number of bad quarters (multiplicity != 1) in the inner squares, for the
sq2_lemma.py model. usage: sq2_min.py R W  (count squares with lower-left in [-W,W-1]^2)."""
import sys
from collections import defaultdict
from itertools import combinations, product
from sq2_lemma import build
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF

R, W = int(sys.argv[1]), int(sys.argv[2])
V, edges, var, tiles, cover, cnf, banned = build(R)
w = WCNF(); w.extend(cnf.clauses)
top = cnf.nv; b = {}
for x, y, k in product(range(-W, W), range(-W, W), range(4)):
    t = (x, y, k); S = [var[e] for e in cover[t]]
    top += 1; b[t] = top
    w.append([b[t]] + S)                      # m = 0 -> bad
    for p, q in combinations(S, 2):
        w.append([b[t], -p, -q])              # m >= 2 -> bad
    w.append([-b[t]], weight=1)
with RC2(w, solver='cadical153') as rc2:
    m = rc2.compute()
    print('R', R, 'W', W, 'min bad quarters', rc2.cost)
model = set(l for l in m if l > 0)
C = defaultdict(int)
for e in edges:
    if var[e] in model:
        for t in tiles[e]: C[t] += 1
for y in range(W - 1, -W - 1, -1):
    print(' '.join(''.join(str(C[x, y, k]) for k in range(4)) for x in range(-W, W)), ' y =', y)
if len(sys.argv) > 3:
    sel = [e for e in edges if var[e] in model]
    adj = defaultdict(list)
    for a, c in sel:
        adj[a].append((c[0]-a[0], c[1]-a[1])); adj[c].append((a[0]-c[0], a[1]-c[1]))
    names = {d: i for i, d in enumerate([(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)])}
    print('vertex move pairs (move index 0..7 = (1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)):')
    for y in range(R, -R-1, -1):
        print(' '.join(''.join(str(names[d]) for d in sorted(adj[(x, y)], key=names.get)) for x in range(-R, R+1)), ' y =', y)
    with open(f'sq2_min_R{R}W{W}.edges', 'w') as f:
        for e in sel: f.write(f'{e[0][0]} {e[0][1]} {e[1][0]} {e[1][1]}\n')
