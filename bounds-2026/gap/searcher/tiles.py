"""Quarter-triangle multiplicities of knight tiles for a corr.cpp witness (KT Edge Searcher).
Quarter triangle (i,j,k): unit square [i,i+1]x[j,j+1], k = 0 S, 1 E, 2 N, 3 W (adjacent to that side)."""
import sys, json
sys.path.insert(0, '.')
from verify_corr import field, KM, cross
from fractions import Fraction as Fr

def tile(e):
    a, b = e; x, y = a[0] + b[0], a[1] + b[1]
    if abs(a[0] - b[0]) == 2: c, d = (x // 2, (y - 1) // 2), (x // 2, (y + 1) // 2)
    else: c, d = ((x - 1) // 2, y // 2), ((x + 1) // 2, y // 2)
    return a, b, c, d

def inside(P, q):
    # q strictly inside convex quadrilateral P (any vertex order): use the 4 axes test like check_knight_tiles
    AX = ((1, 0), (0, 1), (1, 1), (1, -1))
    return all(min(ax * x + ay * y for x, y in P) < ax * q[0] + ay * q[1] < max(ax * x + ay * y for x, y in P) for ax, ay in AX)

CENT = [(Fr(1, 2), Fr(1, 6)), (Fr(5, 6), Fr(1, 2)), (Fr(1, 2), Fr(5, 6)), (Fr(1, 6), Fr(1, 2))]
def quarters(e):
    P = tile(e); out = []
    for i in range(min(p[0] for p in P), max(p[0] for p in P)):
        for j in range(min(p[1] for p in P), max(p[1] for p in P)):
            for k, (cx, cy) in enumerate(CENT):
                if inside(P, (i + cx, j + cy)): out.append((i, j, k))
    assert len(out) == 4, (e, out)
    return out

def full_edges(d, K=8):
    A, W, OFF, R = d['A'], d['W'], d['OFF'], d['rows']
    F = field(d['kind']); T = (A * R, R)
    u = lambda c: c[0] - A * c[1] - OFF
    band = lambda c: 0 <= u(c) < W
    E = set()
    for k in range(-2, K + 3):
        for e in d['edges']:
            a = (e[0] + k * T[0], e[1] + k * T[1]); b = (e[2] + k * T[0], e[3] + k * T[1])
            E.add(tuple(sorted((a, b))))
    for y in range(-3 * R, (K + 3) * R):
        for xx in range(OFF + A * y - 14, OFF + A * y + W + 14):
            c = (xx, y)
            v = F(*c); q = (c[0] + v[0], c[1] + v[1])
            if not (band(c) and band(q)): E.add(tuple(sorted((c, q))))
    return E

if __name__ == '__main__':
    for line in open(sys.argv[1]):
        d = json.loads(line)
        if 'edges' not in d or d['crossings'] == 0: continue
        if len(sys.argv) > 2 and d['current'] != int(sys.argv[2]): continue
        E = full_edges(d); R = d['rows']; A, OFF, W = d['A'], d['OFF'], d['W']
        mult = {}
        for e in E:
            for q in quarters(e): mult[q] = mult.get(q, 0) + 1
        y0 = 3 * R
        bad = sorted((q, m) for q, m in mult.items() if y0 <= q[1] < y0 + R and m != 1 and abs(q[0] - (OFF + A * q[1])) < W + 8)
        # holes: quarters in window with multiplicity 0
        holes = []
        for j in range(y0, y0 + R):
            for i in range(OFF + A * j - 8, OFF + A * j + W + 8):
                for k in range(4):
                    if mult.get((i, j, k), 0) == 0: holes.append((i, j, k))
        print(d['kind'], 'W', W, 'current', d['current'], 'X', d['crossings'], 'rows', R)
        print('  multiply covered:', [(q, m) for q, m in bad if m > 1])
        print('  holes:', holes)
