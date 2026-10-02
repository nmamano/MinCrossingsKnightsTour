"""Independent re-implementation (no imports from strip_dp.py / mmc.py) of the width-2 strip
transfer graph for crossings, and of the stability constants used in PROOF_crossings.md (C7).

Model: columns 0,1 = strip (degree exactly 2), columns 2,3 = ghosts (degree <= 2); edges = knight
moves inside columns 0..3 with at least one end in the strip; no cycle; weight = proper crossings.
Cells are scanned in the order (row, column). A state is (column to process next, frozenset of
pending edges with a component id each), coordinates relative to the current row.
Outputs: number of states, exact potential range, rho = minimum positive reduced cost (step weight
minus 1/4), number and length of tight cycles, longest tight path avoiding tight-cycle edges.
"""
from collections import deque


def sgn(v):
    return (v > 0) - (v < 0)


def turn(a, b, c):
    return sgn((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]))


def proper(e, f):
    a, b = e
    c, d = f
    return turn(a, b, c) * turn(a, b, d) == -1 and turn(c, d, a) * turn(c, d, b) == -1


UPMOVES = ((1, 2), (-1, 2), (2, 1), (-2, 1))
NCOL = 4


def successors(state):
    col, pend = state          # pend: tuple of ((lx,ly),(ux,uy),comp)
    here = (col, 0)
    inc = [p for p in pend if p[1] == here]
    others = [p for p in pend if p[1] != here]
    strip = col < 2
    cand = []
    for dx, dy in UPMOVES:
        t = (col + dx, dy)
        if 0 <= t[0] < NCOL and (strip or t[0] < 2):
            cand.append(t)
    need = [2 - len(inc)] if strip else list(range(0, 3 - len(inc)))
    res = []
    if len(inc) > 2 or (strip and need[0] < 0):
        return res
    if len(inc) == 2 and inc[0][2] == inc[1][2]:
        return res                      # would close a cycle
    for k in need:
        for i in range(len(cand)):
            for j in range(i, len(cand)):
                pick = []
                if k == 0:
                    if (i, j) != (0, 0):
                        continue
                elif k == 1:
                    if i != j:
                        continue
                    pick = [cand[i]]
                else:
                    if i == j:
                        continue
                    pick = [cand[i], cand[j]]
                # target degree
                load = {}
                for p in others:
                    load[p[1]] = load.get(p[1], 0) + 1
                bad = False
                for t in pick:
                    load[t] = load.get(t, 0) + 1
                    if load[t] > 2:
                        bad = True
                if bad:
                    continue
                newe = [(here, t) for t in pick]
                wgt = 0
                for n_, e in enumerate(newe):
                    for p in others:
                        if proper((p[0], p[1]), e):
                            wgt += 1
                    for e2 in newe[:n_]:
                        if proper(e2, e):
                            wgt += 1
                # components
                if inc:
                    lab = inc[0][2]
                    merge = inc[1][2] if len(inc) == 2 else None
                else:
                    lab = -1
                    merge = None
                lst = []
                for p in others:
                    c = lab if (merge is not None and p[2] == merge) else p[2]
                    lst.append((p[0], p[1], c))
                for e in newe:
                    lst.append((e[0], e[1], lab))
                ncol = col + 1
                dy = 0
                if ncol == NCOL:
                    ncol, dy = 0, 1
                lst = [((a[0], a[1] - dy), (b[0], b[1] - dy), c) for a, b, c in lst]
                lst.sort(key=lambda t: (t[0], t[1]))
                ren = {}
                out = []
                for a, b, c in lst:
                    if c not in ren:
                        ren[c] = len(ren)
                    out.append((a, b, ren[c]))
                res.append(((ncol, tuple(out)), wgt))
    return res


def main():
    start = (0, ())
    idx = {start: 0}
    states = [start]
    arcs = []
    q = deque([start])
    while q:
        s = q.popleft()
        best = {}
        for t, w in successors(s):
            if t not in idx:
                idx[t] = len(states); states.append(t); q.append(t)
            j = idx[t]
            if j not in best or w < best[j]:
                best[j] = w
        for j, w in best.items():
            arcs.append((idx[s], j, w))
    N = len(states)
    print('states', N, 'arcs', len(arcs))
    # exact Bellman-Ford with weights 4w - 1 from the start
    INF = float('inf')
    d = [INF] * N; d[0] = 0
    for it in range(N + 1):
        changed = False
        for u, v, w in arcs:
            if d[u] != INF and d[u] + 4 * w - 1 < d[v]:
                d[v] = d[u] + 4 * w - 1; changed = True
        if not changed:
            break
    assert not changed, 'negative cycle: min mean < 1/4'
    print('potential range (x1/4):', min(d), max(d))
    pos = [4 * w - 1 + d[u] - d[v] for u, v, w in arcs if 4 * w - 1 + d[u] - d[v] > 0]
    assert min(4 * w - 1 + d[u] - d[v] for u, v, w in arcs) >= 0
    print('rho (x1/4):', min(pos))
    tight = {}
    for u, v, w in arcs:
        if 4 * w - 1 + d[u] - d[v] == 0:
            tight.setdefault(u, []).append(v)
    # strongly connected components of the tight graph (Tarjan, iterative)
    index = {}; low = {}; onst = set(); st = []; comps = []; counter = [0]
    for root in range(N):
        if root in index:
            continue
        work = [(root, iter(tight.get(root, [])))]
        index[root] = low[root] = counter[0]; counter[0] += 1; st.append(root); onst.add(root)
        while work:
            v, it_ = work[-1]
            nxt = next(it_, None)
            if nxt is None:
                work.pop()
                if work:
                    low[work[-1][0]] = min(low[work[-1][0]], low[v])
                if low[v] == index[v]:
                    comp = []
                    while True:
                        x = st.pop(); onst.discard(x); comp.append(x)
                        if x == v:
                            break
                    comps.append(comp)
            elif nxt not in index:
                index[nxt] = low[nxt] = counter[0]; counter[0] += 1; st.append(nxt); onst.add(nxt)
                work.append((nxt, iter(tight.get(nxt, []))))
            elif nxt in onst:
                low[v] = min(low[v], index[nxt])
    cyc = [c for c in comps if len(c) > 1 or c[0] in tight.get(c[0], [])]
    print('tight cyclic components:', [len(c) for c in cyc])
    cyc_edges = set()
    for c in cyc:
        cs = set(c)
        inner = [(u, v) for u in c for v in tight.get(u, []) if v in cs]
        assert len(inner) == len(c), 'component is not a simple cycle'
        cyc_edges |= set(inner)
    # longest path in tight graph minus cycle edges (must be acyclic)
    adj = {u: [v for v in vs if (u, v) not in cyc_edges] for u, vs in tight.items()}
    indeg = [0] * N
    for u, vs in adj.items():
        for v in vs:
            indeg[v] += 1
    order = [u for u in range(N) if indeg[u] == 0]
    longest = [0] * N
    k = 0
    while k < len(order):
        u = order[k]; k += 1
        for v in adj.get(u, []):
            longest[v] = max(longest[v], longest[u] + 1)
            indeg[v] -= 1
            if indeg[v] == 0:
                order.append(v)
    assert len(order) == N, 'tight graph minus cycle edges has a cycle'
    print('T* =', max(longest))


if __name__ == '__main__':
    main()


def alpha_check(p=1, q=5):
    """Independent check: with weights q(4w-1) - 4p*[arc not on a tight cycle], no negative cycle
    (Bellman-Ford from a virtual source); print the potential range."""
    import sys
    start = (0, ())
    idx = {start: 0}; states = [start]; arcs = []
    from collections import deque
    dq = deque([start])
    while dq:
        s = dq.popleft()
        best = {}
        for t, w in successors(s):
            if t not in idx:
                idx[t] = len(states); states.append(t); dq.append(t)
            j = idx[t]
            if j not in best or w < best[j]:
                best[j] = w
        for j, w in best.items():
            arcs.append((idx[s], j, w))
    N = len(states)
    INF = float('inf')
    d = [INF] * N; d[0] = 0
    for it in range(N + 1):
        ch = False
        for u, v, w in arcs:
            if d[u] != INF and d[u] + 4 * w - 1 < d[v]:
                d[v] = d[u] + 4 * w - 1; ch = True
        if not ch:
            break
    tight = set((u, v) for u, v, w in arcs if 4 * w - 1 + d[u] - d[v] == 0)
    # cycle arcs = tight arcs inside tight SCCs: find by checking reachability back (small: use DFS)
    tadj = {}
    for u, v in tight:
        tadj.setdefault(u, []).append(v)
    def reach(a, b):
        seen = {a}; st = [a]
        while st:
            x = st.pop()
            for y in tadj.get(x, []):
                if y == b:
                    return True
                if y not in seen:
                    seen.add(y); st.append(y)
        return False
    cyc = set((u, v) for u, v in tight if reach(v, u))
    print('cycle arcs:', len(cyc))
    dist = [0] * N
    for it in range(N + 2):
        ch = False
        for u, v, w in arcs:
            ww = q * (4 * w - 1) - 4 * p * (0 if (u, v) in cyc else 1)
            if dist[u] + ww < dist[v]:
                dist[v] = dist[u] + ww; ch = True
        if not ch:
            print(f'alpha={p}/{q}: no negative cycle; potential range {min(dist)}..{max(dist)} (units 1/(4q))')
            return True
    print(f'alpha={p}/{q}: NEGATIVE CYCLE')
    return False
