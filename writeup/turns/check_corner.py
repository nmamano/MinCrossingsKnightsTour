#!/usr/bin/env python3
"""Check the corner certificate exactly as printed in main.tex (Lemma 3). Standard library only."""
from itertools import combinations
MOVES = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
ALPHA = {0: [-1, 0, 0, -1], 1: [0, 1, 0, -1], 2: [0, 0, 0, -1], 3: [-1, -1, -1, -1]}  # ALPHA[y][x]
BETA = {((0, 1), (1, 3)): -1, ((0, 2), (2, 3)): -1, ((0, 3), (1, 1)): +1, ((1, 0), (3, 1)): -1,
        ((1, 1), (3, 0)): -1, ((1, 2), (3, 3)): -1, ((2, 0), (3, 2)): -1, ((2, 1), (3, 3)): -1,
        ((2, 2), (3, 0)): -1}


def L(i, nb_coords):
    """Local lower bound for a cell at distance i from one side; nb_coords = distances of its two neighbours."""
    if i == 0: return 1
    if i in (1, 2): return sum(c in (0, 3) for c in nb_coords) - 1
    if i == 3: return 1 - sum(c in (1, 2) for c in nb_coords)
    return 0


cases = 0; tight = set()
for x in range(4):
    for y in range(4):
        v = (x, y)
        legal = [m for m in MOVES if x + m[0] >= 0 and y + m[1] >= 0]
        for a, b in combinations(legal, 2):
            u1, u2 = (x + a[0], y + a[1]), (x + b[0], y + b[1])
            t = 0 if a == (-b[0], -b[1]) else 1
            r = t - L(x, [u1[0], u2[0]]) - L(y, [u1[1], u2[1]])
            D = 0
            for u in (u1, u2):
                e = tuple(sorted((v, u)))
                if e in BETA: D += BETA[e] if e[0] == v else -BETA[e]
            assert r - ALPHA[y][x] - D >= 0, (v, a, b)
            if r - ALPHA[y][x] - D == 0: tight.add(v)
            cases += 1
assert sum(map(sum, ALPHA.values())) == -7 and len(tight) == 16
print('PASS:', cases, 'cases; sum alpha = -7; every cell has a tight case')
