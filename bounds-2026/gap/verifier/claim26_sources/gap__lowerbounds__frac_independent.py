#!/usr/bin/env python3
"""Independent check for frac_stab.py (no import of strip_dp.py or frac_stab.py).

Graph: strip2_independent.build_graph(). Augmented node = (base state, frozenset of selected TEST edges
straddling the current row, local row parity). At column 0 the set starts with the pending test edges;
each arc adds the new edges whose lower end is the processed cell. At row end the penalty t = 2a is
computed from the set (FINDINGS 11.1-11.2): exception (both EXC edges) -> t=2; else
h = ((1+c)//2 + c*(F+2)) mod 3 with c = +1 / -1 for parity 0 / 1, and t = {0:1, 1:2, 2:0}[h].
The set is reset and the parity toggled. Weights q*(4w-1) - 2*p*t. Bellman-Ford from 0 on every node
(both initial parities). Reports convergence and the potential range, or non-convergence.

usage: python3 frac_independent.py ORIENT p q     (ORIENT = up | down)
"""
import sys
import strip2_independent as S

LIST = [(((0, -1), (1, 1)), -1), (((0, 0), (1, -2)), -1), (((0, 0), (2, -1)), -1), (((0, 2), (1, 0)), -1),
        (((1, 0), (2, 2)), -1), (((1, 1), (2, -1)), -1), (((0, 1), (1, -1)), 1), (((0, 1), (2, 0)), 1)]
EXC = [((0, 0), (2, 1)), ((0, 1), (2, 0))]


def norm(a, b):
    return (a, b) if a <= b else (b, a)


def make_test(orient):
    s = {'up': 1, 'down': -1}[orient]
    refl = lambda p: (p[0], s * p[1])
    coef = {norm(refl(a), refl(b)): c for (a, b), c in LIST}
    exc = frozenset(norm(refl(a), refl(b)) for a, b in EXC)
    return coef, exc


def penalty(seen, par, coef, exc):
    if exc <= seen:
        return 2
    F = sum(coef.get(e, 0) for e in seen)
    c = 1 - 2 * par
    h = ((1 + c) // 2 + c * (F + 2)) % 3
    return (1, 2, 0)[h]


def main():
    orient, p, q = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    coef, exc = make_test(orient)
    watch = set(coef) | exc
    states, arcs = S.build_graph()
    print('base states', len(states), 'arcs', len(arcs), flush=True)
    node = {}
    def nid(k):
        if k not in node:
            node[k] = len(node)
        return node[k]
    out = {}
    for u, v, w in arcs:
        out.setdefault(u, []).append((v, w))
    A = []
    todo = [(u, frozenset(), par) for u in range(len(states)) if states[u][0] == 0 for par in (0, 1)]
    done = set(todo)
    while todo:
        key = todo.pop()
        u, seen, par = key
        col, pend = states[u]
        if col == 0:
            seen = frozenset(norm(a, b) for a, b, c in pend if norm(a, b) in watch)
        for v, w in out.get(u, []):
            vcol, vpend = states[v]
            dy = 1 if vcol == 0 else 0
            new = {norm((a[0], a[1] + dy), (b[0], b[1] + dy)) for a, b, c in vpend if a == (col, -dy)}
            seen2 = seen | frozenset(e for e in new if e in watch)
            if vcol == 0:
                key2 = (v, frozenset(), 1 - par)
                A.append((nid(key), nid(key2), q * (4 * w - 1) - 2 * p * penalty(seen2, par, coef, exc)))
            else:
                key2 = (v, seen2, par)
                A.append((nid(key), nid(key2), q * (4 * w - 1)))
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
    print(f'{orient} beta={p}/{q}: NO convergence after {it} passes: a negative cycle exists')


if __name__ == '__main__':
    main()
