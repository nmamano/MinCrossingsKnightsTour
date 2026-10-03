"""S1 minimal strip certificate (2026-10-03). Self-contained: standard library + NumPy; no project imports.

Model (side frame, inward column x = 0..3, row y). S = knight edges with an endpoint in column 0 or 1 and both
endpoints in columns 0..3. Every vertex in columns 0, 1 has S-degree 2; columns 2, 3 have S-degree <= 2.
NO forest / no-cycle condition is used.
A CUT STATE is the set of S-edges that cross the cut between two consecutive rows (lower end below, upper end
at or above). A ROW ARC chooses the S-edges whose lower endpoint is in the next row. w = number of new proper
crossings (new x pending, new x new). The row mask = all S-edges that meet the row. g(row) is the strong UP / DOWN
indicator of PROOF_5N.md section 4 (test failure OR exception OR VIS).
Certificate: integer potentials h_up, h_down on cut states with 4w - 4 - 4g + h(u) - h(v) >= 0 on every arc.
Usage: python3 check_cut_certificate.py      (prints sizes, ranges, interface, and the side constant)
"""
import sys
from itertools import combinations
import numpy as np


def cross(e, f):
    def det(a, b, c): return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
    (a, b), (c, d) = e, f
    return det(a, b, c)*det(a, b, d) < 0 and det(c, d, a)*det(c, d, b) < 0


def edge(p, q): return tuple(sorted((p, q)))


# Endpoint test of PROOF_5N.md section 2 (UP frame) and the seven UP visibility pairs of section 4.
TERMS = {edge((0, -1), (1, 1)): -1, edge((0, 0), (1, -2)): -1, edge((0, 0), (2, -1)): -1, edge((0, 1), (1, -1)): 1,
         edge((0, 1), (2, 0)): 1, edge((0, 2), (1, 0)): -1, edge((1, 0), (2, 2)): -1, edge((1, 1), (2, -1)): -1}
EXC = [edge((0, 0), (2, 1)), edge((0, 1), (2, 0))]
VIS = [((0, 0), (2, 1), (1, 0), (2, 2)), ((0, 1), (2, 0), (1, 1), (2, -1)), ((1, -1), (2, 1), (1, 0), (3, 1)),
       ((1, -1), (2, 1), (1, 1), (2, -1)), ((1, 0), (2, 2), (1, 2), (2, 0)), ((1, 0), (3, 1), (1, 1), (3, 0)),
       ((1, 1), (3, 0), (1, 2), (2, 0))]
VIS = [(edge(a, b), edge(c, d)) for a, b, c, d in VIS]


def refl(e): return edge(*[(x, -y) for x, y in e])


def g_value(mask, sign):
    t = (lambda e: e) if sign == 1 else refl
    F = sum(c for e, c in TERMS.items() if t(e) in mask) % 3
    E = all(t(e) in mask for e in EXC)
    V = any(t(a) in mask and t(b) in mask for a, b in VIS)
    return int(F != 2 or E or V)


MOVES = [(dx, dy) for dx in (-2, -1, 1, 2) for dy in (1, 2) if abs(dx) != dy]


def row_arcs(state):
    """state: frozenset of edges ((x0,y0),(x1,y1)) sorted, lower end row < 0 <= upper end row. Yields (next, w, mask)."""
    into = {}
    for e in state:
        hi = max(e, key=lambda p: p[1])
        if hi[1] == 0: into[hi[0]] = into.get(hi[0], 0) + 1
    if any(v > 2 for v in into.values()): return
    options = {x: [edge((x, 0), (x+dx, dy)) for dx, dy in MOVES if 0 <= x+dx <= 3 and min(x, x+dx) < 2] for x in range(4)}
    choices = []
    for x in range(4):
        need = 2 - into.get(x, 0)
        counts = [need] if x < 2 else range(need + 1)
        choices.append([c for k in counts for c in combinations(options[x], k)])

    def rec(x, chosen):
        if x == 4:
            yield list(chosen); return
        for c in choices[x]: yield from rec(x+1, chosen + list(c))
    for new in rec(0, []):
        load = {}
        for e in new + list(state):
            hi = max(e, key=lambda p: p[1])
            if hi[1] > 0: load[hi] = load.get(hi, 0) + 1
        if any(v > 2 for v in load.values()): continue
        w = sum(cross(a, b) for a in new for b in state) + sum(cross(a, b) for a, b in combinations(new, 2))
        mask = frozenset(state) | frozenset(new)
        keep = [e for e in list(state) + new if max(p[1] for p in e) > 0]
        nxt = frozenset(edge((a[0], a[1]-1), (b[0], b[1]-1)) for a, b in keep)
        yield nxt, w, mask


def main():
    start = frozenset(); states = [start]; ids = {start: 0}; arcs = []
    for s in states:
        for t, w, mask in row_arcs(s):
            if t not in ids: ids[t] = len(states); states.append(t)
            arcs.append((ids[s], ids[t], w, g_value(mask, 1), g_value(mask, -1)))
    S = np.array([a[0] for a in arcs]); D = np.array([a[1] for a in arcs]); W = np.array([a[2] for a in arcs])
    print('cut states', len(states), 'row arcs', len(arcs), 'distinct pending edges', len(set().union(*states)), flush=True)
    pots = []
    for k, name in ((3, 'up'), (4, 'down')):
        cost = 4*W - 4 - 4*np.array([a[k] for a in arcs])
        h = np.zeros(len(states), dtype=np.int64)
        for it in range(10000):
            nh = h.copy(); np.minimum.at(nh, D, h[S] + cost)
            if np.array_equal(nh, h): break
            h = nh
        else: sys.exit('negative cycle in ' + name)
        assert (cost + h[S] - h[D]).min() >= 0
        print(name, 'passes', it + 1, 'potential range', int(h.min()), int(h.max()), flush=True)
        pots.append(h)
    diff = pots[0] - pots[1]
    print('interface h_up - h_down range', int(diff.min()), int(diff.max()))
    # 4(X - rows - G) >= h_up(m) - h_up(a) + h_down(z) - h_down(m) >= min(diff) - max(h_up) + min(h_down)
    err = -(int(diff.min()) - int(pots[0].max()) + int(pots[1].min()))
    print('per-side bound: G_sigma <= X_sigma - rows +', err, '/ 4')
    np.save('gap/lowerbounds/simple_strip/cut_potential_up.npy', pots[0]); np.save('gap/lowerbounds/simple_strip/cut_potential_down.npy', pots[1])


if __name__ == '__main__':
    main()
