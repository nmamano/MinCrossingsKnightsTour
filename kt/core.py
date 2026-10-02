"""Core tour utilities: build tours from move-code grids, validate, count turns/crossings.
Grid convention follows board.js: tour[i][j] = 'ab' (two move codes), i row downward."""
import sys
from collections import defaultdict
MI = [-2, -1, 1, 2, 2, 1, -1, -2]
MJ = [1, 2, 2, 1, -1, -2, -2, -1]

def empty(w, h):
    return [['26'] * w for _ in range(h)]

def flip_cell(c):
    return 'xx' if c == 'xx' else ''.join(str((int(ch) + 4) % 8) for ch in c)

def rot180(struct):
    rows = [r.split(' ') for r in struct][::-1]
    return [' '.join(flip_cell(c) for c in r[::-1]) for r in rows]

def add_piece(t, i0, j0, struct):
    for di, line in enumerate(struct):
        for dj, c in enumerate(line.split(' ')):
            if c != 'xx':
                t[i0 + di][j0 + dj] = c

def neighbors(t, i, j):
    return [(i + MI[int(m)], j + MJ[int(m)]) for m in t[i][j]]

def edges(t):
    """Return set of undirected edges ((i,j),(i2,j2)) with a<b; raises on inconsistency."""
    h, w = len(t), len(t[0])
    E = set()
    for i in range(h):
        for j in range(w):
            for (a, b) in neighbors(t, i, j):
                if not (0 <= a < h and 0 <= b < w):
                    raise ValueError(f'move off board at {(i,j)} -> {(a,b)}')
                if (i, j) not in neighbors(t, a, b):
                    raise ValueError(f'asymmetric edge {(i,j)}-{(a,b)}')
                e = ((i, j), (a, b)) if (i, j) < (a, b) else ((a, b), (i, j))
                E.add(e)
    return E

def num_cycles(t):
    h, w = len(t), len(t[0])
    seen = [[False] * w for _ in range(h)]
    cyc = 0
    for i in range(h):
        for j in range(w):
            if seen[i][j]:
                continue
            cyc += 1
            stack = [(i, j)]
            seen[i][j] = True
            while stack:
                a, b = stack.pop()
                for (c, d) in neighbors(t, a, b):
                    if not seen[c][d]:
                        seen[c][d] = True
                        stack.append((c, d))
    return cyc

def validate(t):
    """True iff t encodes a single closed knight's tour."""
    E = edges(t)
    h, w = len(t), len(t[0])
    if len(E) != h * w:
        return False
    for i in range(h):
        for j in range(w):
            if t[i][j][0] == t[i][j][1]:
                return False
    return num_cycles(t) == 1

def num_turns(t):
    return sum(1 for row in t for c in row if c not in ('04', '40', '15', '51', '26', '62', '37', '73'))

def _orient(px, py, qx, qy, rx, ry):
    v = (qy - py) * (rx - qx) - (qx - px) * (ry - qy)
    return 0 if v == 0 else (1 if v > 0 else 2)

def seg_cross(p1, p2, q1, q2):
    """Open segments cross properly (shared endpoints never count)."""
    if p1 == q1 or p1 == q2 or p2 == q1 or p2 == q2:
        return False
    o1 = _orient(*p1, *p2, *q1); o2 = _orient(*p1, *p2, *q2)
    o3 = _orient(*q1, *q2, *p1); o4 = _orient(*q1, *q2, *p2)
    return o1 and o2 and o3 and o4 and o1 != o2 and o3 != o4

def crossing_list(E):
    """All crossing pairs among edge set E (edges as point pairs)."""
    by_cell = defaultdict(list)
    for e in E:
        by_cell[e[0]].append(e)
    out = []
    for e in E:
        (i, j) = e[0]
        for di in range(-3, 4):
            for dj in range(-3, 4):
                for f in by_cell.get((i + di, j + dj), ()):
                    if e < f and seg_cross(e[0], e[1], f[0], f[1]):
                        out.append((e, f))
    return out

def num_crossings(t):
    return len(crossing_list(edges(t)))

def grid_from_strings(struct):
    return [r.split(' ') for r in struct]
