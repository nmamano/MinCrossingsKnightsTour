#!/usr/bin/env python3
"""Standalone check of a sq2 witness (no solver). usage: sq2_check_witness.py file.edges R"""
import sys, os
from collections import Counter
from itertools import combinations
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'w-turnstheory'))
from check_knight_tiles import microtiles
E = [tuple(map(int, l.split())) for l in open(sys.argv[1])]; R = int(sys.argv[2])
E = [((a, b), (c, d)) for a, b, c, d in E]
deg = Counter(p for e in E for p in e)
for e in E:
    assert sorted((abs(e[0][0]-e[1][0]), abs(e[0][1]-e[1][1]))) == [1, 2]
    assert any(max(map(abs, p)) <= R for p in e)
assert len(set(E)) == len(E)
assert all(deg[(x, y)] == 2 for x in range(-R, R+1) for y in range(-R, R+1))
assert max(deg.values()) <= 2
T = {e: microtiles(e) for e in E}
C = Counter(t for e in E for t in T[e])
assert max(C.values()) <= 2
assert all(len(T[e] & T[f]) != 1 for e, f in combinations(E, 2))
m = [C[0, 0, k] for k in range(4)]
assert sum(v != 1 for v in m) == 2
print('PASS', len(E), 'edges; degree 2 on V, <= 2 outside; multiplicities <= 2; no one-quarter overlap; central', m)
