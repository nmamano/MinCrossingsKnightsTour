"""Strip relaxation lower bound for crossings of a closed knight's tour.

Model (left strip of width k, see FINDINGS.md):
  columns 0..k-1 = strip cells, degree exactly 2.
  columns k, k+1 = ghost cells, degree <= 2 (only strip edges counted).
  edges = knight moves with both ends in columns 0..k+1 and at least one end in the strip.
  chosen edges form a forest of paths (no cycle).
  weight = number of proper crossings between chosen edges.
Cells are processed in order (y, x), x = 0..W-1, W = k+2. State = pending edges
(lower end processed, upper end not yet) with geometry relative to the current
cell, plus a connectivity partition of the pending edges.
"""
import sys
from collections import deque

UP = [(2, 1), (-2, 1), (1, 2), (-1, 2)]


def orient(ax, ay, bx, by, cx, cy):
    v = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
    return (v > 0) - (v < 0)


def cross(e, f):
    (ax, ay, bx, by), (cx, cy, dx, dy) = e, f
    d1 = orient(ax, ay, bx, by, cx, cy)
    d2 = orient(ax, ay, bx, by, dx, dy)
    d3 = orient(cx, cy, dx, dy, ax, ay)
    d4 = orient(cx, cy, dx, dy, bx, by)
    return d1 * d2 < 0 and d3 * d4 < 0


def build(k, max_states=5_000_000, fam=None, mode='cross'):
    W = k + 2
    def okedge(x1, x2, dx, dy):
        if fam is None:
            return True
        if x1 < k and x2 < k:
            return True
        return (dx, dy) in (fam, (-fam[0], -fam[1]))
    def ghost_need(x):
        # number of family neighbours of ghost column x inside the strip
        c = 0
        for sx, sy in (fam, (-fam[0], -fam[1])):
            if 0 <= x + sx < k:
                c += 1
        return c
    # state: (x, edges) ; edges = tuple sorted of (lx, ly, ux, uy, comp)
    # coordinates: y relative to current row (current cell is at (x, 0)).
    start = (0, (), 0)
    index = {start: 0}
    states = [start]
    adj = []  # list of list of (target, weight)
    q = deque([0])
    while q:
        sid = q.popleft()
        x, edges, warm = states[sid]
        out = {}
        incoming = [e for e in edges if e[2] == x and e[3] == 0]
        rest = [e for e in edges if not (e[2] == x and e[3] == 0)]
        deg_in = len(incoming)
        strip = x < k
        cands = []
        for dx, dy in UP:
            tx = x + dx
            if 0 <= tx < W and (strip or tx < k) and okedge(x, tx, dx, dy):
                cands.append((x, 0, tx, dy))
        need = []
        if strip:
            r = 2 - deg_in
            if r < 0:
                continue
            need = [r] if (fam is None or warm >= 3) else list(range(0, r + 1))
        else:
            if deg_in > 2:
                continue
            need = list(range(0, 3 - deg_in))
            if fam is not None:
                g = ghost_need(x) - deg_in
                if g < 0 and warm >= 3:
                    continue
                need = [g] if warm >= 3 else list(range(0, max(g, 0) + 1))
        from itertools import combinations
        for r in need:
            for chosen in combinations(cands, r):
                # degree check at targets: count pending + chosen into each target
                ok = True
                tdeg = {}
                for e in rest:
                    tdeg[(e[2], e[3])] = tdeg.get((e[2], e[3]), 0) + 1
                for e in chosen:
                    key = (e[2], e[3])
                    tdeg[key] = tdeg.get(key, 0) + 1
                    if tdeg[key] > 2:
                        ok = False
                if not ok:
                    continue
                # connectivity: incoming comps + chosen edges joined at this cell
                comps_in = [e[4] for e in incoming]
                if len(comps_in) == 2 and comps_in[0] == comps_in[1]:
                    continue  # closes a cycle
                # weight
                w = 0
                if mode == 'turns':
                    if strip:
                        # the cell's two moves: incoming (from below) and chosen (upward)
                        vecs = [(e[0] - e[2], e[1] - e[3]) for e in incoming] + [(f[2] - f[0], f[3] - f[1]) for f in chosen]
                        if not (vecs[0][0] == -vecs[1][0] and vecs[0][1] == -vecs[1][1]):
                            w = 1
                    chosen_for_cross = ()
                else:
                    chosen_for_cross = chosen
                for i, f in enumerate(chosen_for_cross):
                    for e in rest:
                        if cross(e[:4], f):
                            w += 1
                    for g in chosen[:i]:
                        if cross(g, f):
                            w += 1
                # new component label for this cell
                if comps_in:
                    label = comps_in[0]
                    merge = comps_in[1] if len(comps_in) == 2 else None
                else:
                    label = 'new'
                    merge = None
                new_edges = []
                for e in rest:
                    c = e[4]
                    if merge is not None and c == merge:
                        c = label
                    new_edges.append((e[0], e[1], e[2], e[3], c))
                for f in chosen:
                    new_edges.append((f[0], f[1], f[2], f[3], label))
                # advance to next cell
                nx = x + 1
                shift = 0
                if nx == W:
                    nx = 0
                    shift = 1
                ne = [(a, b - shift, c, d - shift, comp) for (a, b, c, d, comp) in new_edges]
                ne.sort(key=lambda t: t[:4])
                relabel = {}
                canon = []
                for (a, b, c, d, comp) in ne:
                    if comp not in relabel:
                        relabel[comp] = len(relabel)
                    canon.append((a, b, c, d, relabel[comp]))
                ns = (nx, tuple(canon), min(warm + shift, 3) if fam is not None else 0)
                if ns not in index:
                    index[ns] = len(states)
                    states.append(ns)
                    q.append(index[ns])
                    if len(states) > max_states:
                        raise RuntimeError('too many states')
                t = index[ns]
                if t not in out or out[t] > w:
                    out[t] = w
        while len(adj) <= sid:
            adj.append(None)
        adj[sid] = list(out.items())
    while len(adj) < len(states):
        adj.append([])
    return states, adj, W


if __name__ == '__main__':
    k = int(sys.argv[1])
    states, adj, W = build(k)
    ne = sum(len(a) for a in adj)
    print('k', k, 'W', W, 'states', len(states), 'edges', ne)
