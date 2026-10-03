#!/usr/bin/env python3
"""Independent check for r1_stab.py (no import of strip_dp.py, frac_stab.py or r1_stab.py).

Graph: strip2_independent.build_graph(); augmented node = (base state, set of selected test edges, parity),
as in frac_independent.py. Per arc, w0 = new crossing pairs whose two edges both have an endpoint in column 0,
recomputed with strip2_independent.proper; the recomputed total must equal the stored w.
Weights q*(4w-1) + p*(4w0-1) - 2p*t. Bellman-Ford from 0 on every node; reports convergence and range.

usage: python3 r1_independent.py ORIENT p q
"""
import sys
import strip2_independent as S
from frac_independent import make_test, penalty, norm


def main():
    orient, p, q = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    coef, exc = make_test(orient)
    watch = set(coef) | exc
    states, arcs = S.build_graph()
    out = {}
    for u, v, w in arcs:
        col, pend = states[u]
        vcol, vpend = states[v]
        dy = 1 if vcol == 0 else 0
        new = [((a[0], a[1] + dy), (b[0], b[1] + dy)) for a, b, c in vpend if a == (col, -dy)]
        rest = [(a, b) for a, b, c in pend if b != (col, 0)]
        tot = w0 = 0
        for j, f in enumerate(new):
            for e in rest + new[:j]:
                if S.proper(e, f):
                    tot += 1
                    if 0 in (e[0][0], e[1][0]) and 0 in (f[0][0], f[1][0]):
                        w0 += 1
        assert tot == w, (u, v, tot, w)
        out.setdefault(u, []).append((v, w, w0, new))
    print('base states', len(states), 'arcs', len(arcs), '(w recomputed and matched)', flush=True)
    node = {}
    def nid(k):
        if k not in node:
            node[k] = len(node)
        return node[k]
    A = []
    todo = [(u, frozenset(), par) for u in range(len(states)) if states[u][0] == 0 for par in (0, 1)]
    done = set(todo)
    while todo:
        key = todo.pop()
        u, seen, par = key
        col, pend = states[u]
        if col == 0:
            seen = frozenset(norm(a, b) for a, b, c in pend if norm(a, b) in watch)
        for v, w, w0, new in out.get(u, []):
            seen2 = seen | frozenset(norm(a, b) for a, b in new if norm(a, b) in watch)
            base = q * (4 * w - 1) + p * (4 * w0 - 1)
            if states[v][0] == 0:
                key2 = (v, frozenset(), 1 - par)
                A.append((nid(key), nid(key2), base - 2 * p * penalty(seen2, par, coef, exc)))
            else:
                key2 = (v, seen2, par)
                A.append((nid(key), nid(key2), base))
            if key2 not in done:
                done.add(key2); todo.append(key2)
    print('augmented nodes', len(node), 'arcs', len(A), flush=True)
    dist = [0] * len(node)
    for it in range(1, 2 * len(node) + 2):
        ch = False
        for a, b, ww in A:
            if dist[a] + ww < dist[b]:
                dist[b] = dist[a] + ww; ch = True
        if not ch:
            print(f'{orient} beta={p}/{q}: converged after {it} passes, no negative cycle; '
                  f'potential range {min(dist)}..{max(dist)} (units 1/(4q))')
            return
        if it > 5000:
            break
    print(f'{orient} beta={p}/{q}: NO convergence after {it} passes: a negative cycle exists')


if __name__ == '__main__':
    main()
