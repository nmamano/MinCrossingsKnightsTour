"""Instance generator for certify.cpp (KT Edge Searcher, own code, written from the lemma statements
in w-lowerbounds/FINDINGS.md F15 and the model descriptions; no code shared with w-lowerbounds)."""
import sys
from fractions import Fraction as Fr
KN = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, 2), (-2, 1), (-2, -1), (-1, -2)]
def chi(p): return 1 if (p[0] + p[1]) % 2 == 0 else -1
def orient(a, b, c):
    v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return (v > 0) - (v < 0)
def crosses(a, b, c, d):
    return orient(a, b, c) * orient(a, b, d) < 0 and orient(c, d, a) * orient(c, d, b) < 0
def write(path, cells, req, edges, transpose=False):
    """cells: list of (x,y); req: dict cell->2/1; edges: list of (p, q, flags, w)."""
    T = (lambda p: (p[1], p[0])) if transpose else (lambda p: p)
    idx = {c: i for i, c in enumerate(cells)}
    with open(path, 'w') as f:
        f.write('%d\n' % len(cells))
        for c in cells: f.write('%d %d %d\n' % (*T(c), req[c]))
        f.write('%d\n' % len(edges))
        for p, q, fl, w in edges: f.write('%d %d %d %d\n' % (idx[p], idx[q], fl, w))
def knight_edges(cells, keep):
    cs = set(cells); out = set()
    for p in cells:
        for d in KN:
            q = (p[0] + d[0], p[1] + d[1])
            if q in cs and keep(p, q): out.add(tuple(sorted([p, q])))
    return sorted(out)
def flux_weight(e, A, B, left_rule):
    if not crosses(A, B, e[0], e[1]): return 0
    return chi(left_rule(e))

def m3(W, orient_, OX=0, OY=0):
    cells = [(x, y) for x in range(-2, W + 2) for y in range(-2, W + 2)]
    win = {(x, y) for x in range(W) for y in range(W)}
    req = {c: 2 if c in win else 1 for c in cells}
    E = knight_edges(cells, lambda p, q: p in win or q in win)
    c = W // 2
    A = (Fr(2 * c - 1, 2) + OX, Fr(2 * c - 1, 2) + OY)
    B = (A[0] + 1, A[1]) if orient_ == 'h' else (A[0], A[1] + 1)
    def left(e):   # endpoint on the left of the directed segment A->B
        return e[0] if orient(A, B, e[0]) > 0 else e[1]
    edges = [(p, q, 0, flux_weight((p, q), A, B, left)) for p, q in E]
    # cell on the right of s next to its midpoint
    mid = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
    rc = (int(mid[0]), int(mid[1] - Fr(1, 2))) if orient_ == 'h' else (int(mid[0] + Fr(1, 2)), int(mid[1]))
    return cells, req, edges, rc

if __name__ == '__main__':
    kind = sys.argv[1]
    if kind == 'm3':
        W, o, OX, OY, out = int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
        cells, req, edges, rc = m3(W, o, OX, OY)
        write(out, cells, req, edges)
        print('right cell', rc, 'chi', chi(rc), 'crossing edges', sum(1 for e in edges if e[3]))

def pattern_edges(s, y):
    """left-edge pattern P (s=+1) or P' (s=-1) at row y: (0,y)-(2,y+s), (0,y)-(1,y+2s), (1,y)-(3,y+s)."""
    return [((0, y), (2, y + s)), ((0, y), (1, y + 2 * s)), ((1, y), (3, y + s))]

def ne_m3(PAT, r, j, X=None):
    """Near-edge M3 as in w-lowerbounds/ne_m3.py (model re-implemented from its description)."""
    X = j + 5 if X is None else X
    Y0, Y1 = r - 6, r + 8
    cells = [(x, y) for x in range(0, X + 2) for y in range(Y0 - 2, Y1 + 2)]
    win = {(x, y) for x in range(X) for y in range(Y0, Y1)}
    req = {c: 2 if c in win else 1 for c in cells}
    E = knight_edges(cells, lambda p, q: p in win or q in win)
    Es = set(E)
    s = 1 if PAT == 'P' else -1
    forced = set()
    for y in range(Y0 - 4, Y1 + 4):
        for a, b in pattern_edges(s, y):
            e = tuple(sorted([a, b]))
            if e in Es: forced.add(e)
    A, B = (Fr(2 * j - 1, 2), Fr(2 * r + 1, 2)), (Fr(2 * j + 1, 2), Fr(2 * r + 1, 2))
    north = lambda e: e[0] if e[0][1] > e[1][1] else e[1]
    edges = []
    for e in E:
        if e in forced: fl = 1
        elif e[0][0] <= 1 or e[1][0] <= 1: fl = 2          # pattern cells keep exactly the pattern edges
        else: fl = 0
        edges.append((e[0], e[1], fl, flux_weight(e, A, B, north)))
    return cells, req, edges

def corner(M, d, PA, PB):
    """Corner neutrality as in w-lowerbounds/corner_neutral.py (re-implemented)."""
    cells = [(x, y) for x in range(M + 2) for y in range(M + 2)]
    win = {(x, y) for x in range(M) for y in range(M)}
    req = {c: 2 if c in win else 1 for c in cells}
    E = knight_edges(cells, lambda p, q: p in win or q in win)
    Es = set(E)
    forced = set()
    sA, sB = (1 if PA == 'P' else -1), (1 if PB == 'P' else -1)
    for y in range(d, M + 2):
        for a, b in pattern_edges(sA, y):
            e = tuple(sorted([a, b]))
            if e in Es: forced.add(e)
    for x in range(d, M + 2):
        for a, b in pattern_edges(sB, x):
            e = tuple(sorted([(a[1], a[0]), (b[1], b[0])]))
            if e in Es: forced.add(e)
    def pcell(dep, al, kind):
        if dep == 0: return al >= d
        if dep == 1: return al >= (d + 2 if kind == 'P' else d)
        return False
    pc = {(x, y) for (x, y) in win if pcell(x, y, PA) or pcell(y, x, PB)}
    box = lambda e: all(p[0] < d and p[1] < d for p in e)
    edges = []
    for e in E:
        if e in forced: fl = 1
        elif e[0] in pc or e[1] in pc: fl = 2
        else: fl = 4 if box(e) else 0
        edges.append((e[0], e[1], fl, 0))
    return cells, req, edges

if __name__ == '__main__' and sys.argv[1] == 'ne':
    PAT, r, j, out = sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    cells, req, edges = ne_m3(PAT, r, j)
    write(out, cells, req, edges, transpose=True)
    print('crossing edges', sum(1 for e in edges if e[3]), 'forced', sum(1 for e in edges if e[2] == 1))
if __name__ == '__main__' and sys.argv[1] == 'corner':
    M, d, PA, PB, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5], sys.argv[6]
    cells, req, edges = corner(M, d, PA, PB)
    write(out, cells, req, edges)
    print('forced', sum(1 for e in edges if e[2] == 1), 'exempt', sum(1 for e in edges if e[2] == 4))
