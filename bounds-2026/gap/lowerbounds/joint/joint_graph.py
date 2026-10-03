#!/usr/bin/env python3
"""Joint model transfer graph (second implementation of KT Edge Searcher's joint model; written from the spec).

Cells: columns 0..5, scanned in (row, column) order. Edge classes (knight moves, lower end first):
  S   : an end in column 0 or 1, other end in columns 0..3
  F23 : column 2 - column 3
  J   : column 3 - column 4 or 5
Degree: columns 0, 1, 3 exactly 2; columns 2, 4, 5 at most 2. No cycle (component labels).
State before cell (c, 0): (c, sorted tuple of pending edges ((lx,ly),(ux,uy),comp)) relative to the current row;
pending = selected edges whose lower end is processed and upper end is not.
Arc weights: w (new crossing pairs, both edges in S), w0 (both edges touch column 0), wx (at least one edge in
F23 u J). A pair is counted at the transition that adds the later edge.
"""
from collections import deque
from itertools import combinations

NC = 6
EXACT = {0, 1, 3}


def cls(a, b):
    xs = sorted((a[0], b[0]))
    if xs[0] <= 1 and xs[1] <= 3: return 'S'
    if xs == [2, 3]: return 'F'
    if xs[0] == 3 and xs[1] in (4, 5): return 'J'
    return None


def ccw(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def proper(e, f):
    a, b = e; c, d = f
    if len({a, b, c, d}) < 4: return False
    return ccw(a, b, c) * ccw(a, b, d) < 0 and ccw(c, d, a) * ccw(c, d, b) < 0


def up_cands(c):
    out = []
    for dx, dy in ((1, 2), (-1, 2), (2, 1), (-2, 1)):
        t = (c + dx, dy)
        if 0 <= t[0] < NC and cls((c, 0), t): out.append(t)
    return out


def step(state):
    c, pend = state
    here = (c, 0)
    inc = [p for p in pend if p[1] == here]
    rest = [p for p in pend if p[1] != here]
    if len(inc) > 2: return []
    if len(inc) == 2 and inc[0][2] == inc[1][2]: return []
    need = [2 - len(inc)] if c in EXACT else list(range(0, 3 - len(inc)))
    tdeg = {}
    for p in rest: tdeg[p[1]] = tdeg.get(p[1], 0) + 1
    res = []
    cands = up_cands(c)
    for k in need:
        if k < 0: continue
        for ch in combinations(cands, k):
            if any(tdeg.get(t, 0) + 1 > 2 for t in ch): continue
            new = [(here, t) for t in ch]
            w = w0 = wx = 0
            for f in new:
                for p in rest:
                    e = (p[0], p[1])
                    if proper(e, f):
                        ce, cf = cls(*e), cls(*f)
                        if ce == 'S' and cf == 'S':
                            w += 1
                            if 0 in (e[0][0], e[1][0]) and 0 in (f[0][0], f[1][0]): w0 += 1
                        else:
                            wx += 1
            lab = inc[0][2] if inc else 'n'
            mrg = inc[1][2] if len(inc) == 2 else None
            ne = [(p[0], p[1], lab if (mrg is not None and p[2] == mrg) else p[2]) for p in rest]
            ne += [(here, t, lab) for t in ch]
            nc = c + 1; sh = 0
            if nc == NC: nc, sh = 0, 1
            ne = sorted(((a[0], a[1] - sh), (b[0], b[1] - sh), g) for a, b, g in ne)
            rl = {}; can = []
            for a, b, g in ne:
                if g not in rl: rl[g] = len(rl)
                can.append((a, b, rl[g]))
            res.append(((nc, tuple(can)), w, w0, wx, tuple(new), len(inc) + k))
    return res


def build(limit=10 ** 7):
    start = (0, ())
    idx = {start: 0}; states = [start]; arcs = []
    dq = deque([start])
    while dq:
        s = dq.popleft(); u = idx[s]
        for t, w, w0, wx, new, deg in step(s):
            if t not in idx:
                idx[t] = len(states); states.append(t); dq.append(t)
                if len(states) > limit: raise RuntimeError('too many states')
            arcs.append((u, idx[t], w, w0, wx, new, deg))
    return states, arcs


if __name__ == '__main__':
    import time
    t0 = time.time()
    states, arcs = build()
    ph0 = sum(1 for s in states if s[0] == 0)
    print('states', len(states), 'phase-0', ph0, 'arcs', len(arcs), f'{time.time() - t0:.0f}s')
