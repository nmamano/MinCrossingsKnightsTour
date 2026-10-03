"""Check (standard library only): for every pair of properly crossing knight edges that both have an
end point in column 0 (x = 0, all other cells x >= 0), the quarter triangles shared by their tiles
(Turns Theory 6.1) lie in x <= 2 and none of them is the right quarter of a square [1,2] x [j,j+1].
Hence these overlaps avoid every quarter triangle adjacent to a dual step at x >= 3/2 (the charged
paths of Turns Theory 7.3/7.4). By transposition the same holds at the bottom edge."""
from fractions import Fraction as F
import itertools
KM = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, 2), (-2, 1), (-1, -2), (-2, -1)]
def tile(a, b):
    mx, my = F(a[0] + b[0], 2), F(a[1] + b[1], 2)
    dx, dy = b[0] - a[0], b[1] - a[1]
    # short diagonal: unit grid edge with the same midpoint, perpendicular-ish: horizontal if |dy|==1? 
    if abs(dx) == 2:   # long diagonal mostly horizontal; midpoint (x.5? no): dx even -> mx integer, my half
        s1, s2 = (mx, my - F(1, 2)), (mx, my + F(1, 2))      # vertical unit edge
    else:
        s1, s2 = (mx - F(1, 2), my), (mx + F(1, 2), my)      # horizontal unit edge
    return [a, s1, b, s2]
def inside(poly, p):
    sg = None
    for i in range(4):
        q, r = poly[i], poly[(i + 1) % 4]
        c = (r[0] - q[0]) * (p[1] - q[1]) - (r[1] - q[1]) * (p[0] - q[0])
        if c == 0: return False
        s = c > 0
        if sg is None: sg = s
        elif sg != s: return False
    return True
def quarters(poly):
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    out = set()
    for i in range(int(min(xs)) - 1, int(max(xs)) + 1):
        for j in range(int(min(ys)) - 1, int(max(ys)) + 1):
            for name, c in (('L', (F(i) + F(1, 6), F(j) + F(1, 2))), ('R', (F(i) + F(5, 6), F(j) + F(1, 2))),
                            ('B', (F(i) + F(1, 2), F(j) + F(1, 6))), ('T', (F(i) + F(1, 2), F(j) + F(5, 6)))):
                if inside(poly, c): out.add((i, j, name))
    return out
def cross(e, f):
    def o(a, b, c):
        v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]); return (v > 0) - (v < 0)
    (a, b), (c, d) = e, f
    return o(a, b, c) * o(a, b, d) < 0 and o(c, d, a) * o(c, d, b) < 0
edges = set()
for y in range(-6, 7):
    for dx, dy in KM:
        q = (dx, y + dy)
        if q[0] >= 0: edges.add(tuple(sorted([(0, y), q])))
edges = sorted(edges)
for e in edges: assert len(quarters(tile(*e))) == 4, e
pairs = bad = 0
for e, f in itertools.combinations(edges, 2):
    if cross(e, f):
        pairs += 1
        ov = quarters(tile(*e)) & quarters(tile(*f))
        assert ov, ('crossing without overlap', e, f)
        for (i, j, nm) in ov:
            if i >= 2 or (i == 1 and nm == 'R'):
                bad += 1; print('VIOLATION', e, f, (i, j, nm))
print(f'column-0 crossing pairs checked: {pairs}; violations: {bad}')
