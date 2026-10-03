"""Independent, light check of Claim 24; standard library, one process.

Angles are exact pairs (a,b) for a + b*atan(1/2) in degrees.
Floating point selects the principal branch only; comparisons use pairs.
Run from the project root: python3 gap/verifier/claim24_check.py
"""
import itertools
import json
import math
from fractions import Fraction

D = [(2, 1), (-2, 1), (1, -2), (1, 2),
     (-2, -1), (2, -1), (-1, 2), (-1, -2)]
A = [(0, 1), (180, -1), (-90, 1), (90, -1),
     (-180, 1), (0, -1), (90, 1), (-90, -1)]
theta = math.degrees(math.atan(0.5))

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def neg(a):
    return (-a[0], -a[1])

def turn(a, b):
    c = add(b, neg(a))
    while c[0] + c[1]*theta > 180:
        c = add(c, (-360, 0))
    while c[0] + c[1]*theta <= -180:
        c = add(c, (360, 0))
    return c

# Rebuild the free-fold graph from integer normals n.u=n.v=1.
adj = {i: set() for i in range(8)}
for i, (x, y) in enumerate(D):
    for j, (z, w) in enumerate(D):
        det = x*w-y*z
        if not det:
            continue
        normal = (Fraction(w-y, det), Fraction(x-z, det))
        if all(t.denominator == 1 for t in normal):
            adj[i].add(j)
assert all(adj[i] == {(i-1) % 8, (i+1) % 8} for i in range(8))
increments = [turn(A[i], A[(i+1) % 8]) for i in range(8)]
assert increments == [(180, -2), (90, 2)]*4

def rotation(k):
    m, odd = divmod(k, 2)
    return (270*m+180*odd, -2*odd)

required = {}
for i in (1, 4, 6, 7):
    for above in (False, True):
        close = (-90 if above else 90, 0)
        required[i, above] = add(
            (360 if above else -360, 0),
            neg(add(turn(A[i], close), turn(close, A[0]))))
assert required[1, True] == (180, -2)
assert required[1, False] == (-180, -2)
assert required[4, True] == (180, 0)
assert required[4, False] == (-180, 0)

hits = {}
for length in range(1, 12):
    for word in itertools.product((-1, 1), repeat=length):
        i, r = 0, (0, 0)
        for step in word:
            j = (i+step) % 8
            r = add(r, turn(A[i], A[j]))
            i = j
        assert r == rotation(sum(word))
        for above in (False, True):
            if (i, above) in required and r == required[i, above]:
                key = (i, above, sum(word))
                hits[key] = hits.get(key, 0)+1
assert hits == {(1, True, 1): 637, (7, False, -1): 637,
                (6, False, -2): 286}

# An actual seven-fold arc: every move raises y by one, so the arc is
# injective. Intermediate x values are positive. Equal y at a fold
# occurs only at the shared endpoint of the two incident segments.
points = [(0, 0)]
dirs = []
for leg, length in enumerate((4, 1, 1, 1, 1, 1, 1, 4)):
    d = D[leg % 2]
    for _ in range(length):
        x, y = points[-1]
        points.append((x+d[0], y+d[1]))
        dirs.append(d)
assert points[-1] == (0, 14)
assert all(x > 0 for x, y in points[1:-1])
assert len(set(points)) == len(points)
assert all(q[1] == p[1]+1 for p, q in zip(points, points[1:]))
assert sum(a != b for a, b in zip(dirs, dirs[1:])) == 7
assert all(D.index(b) in adj[D.index(a)]
           for a, b in zip(dirs, dirs[1:]) if a != b)

print(json.dumps({
    'date': '2026-10-03', 'status': 'PASS',
    'angle_unit': 'a + b*atan(1/2), in degrees',
    'positive_cycle_increments': increments,
    'rotation_matches_length_at_most_11': [
        {'end': D[i], 'above': above, 'net_steps': k, 'count': count}
        for (i, above, k), count in sorted(hits.items())],
    'seven_fold_simple_arc': points,
}, indent=2))
