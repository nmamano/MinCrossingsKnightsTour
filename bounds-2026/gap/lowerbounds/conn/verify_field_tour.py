#!/usr/bin/env python3
"""Verify a saved closed tour that carries the 11.3 field (FINDINGS L2), with no CP-SAT code.

Checks: n*n knight edges, every cell degree 2, one cycle through all cells (Hamiltonian), crossing count by
kt/core.py crossing_list, the field edges present on rows Y0..Y1 (left side), and the endpoint penalty a of
FINDINGS 11.2 per row (top-left corner frame, up test). Compares with the original tour.
usage: verify_field_tour.py TOURJSON ORIGINAL Y0 Y1 s
"""
import sys, json
from tourio import load, ROOT, MOV
sys.path.insert(0, str(ROOT / 'kt'))
from core import crossing_list
from field_close import field_edges, residues, E2


def read(path):
    d = json.load(open(path)); n = d['n']
    E = set()
    for yy, row in enumerate(d['tour']):
        for x, cell in enumerate(row):
            y = n - 1 - yy
            for c in cell:
                E.add(E2((x, y), (x + MOV[int(c)][0], y + MOV[int(c)][1])))
    return n, E


def main():
    path, orig, Y0, Y1, s = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    n, E = read(path)
    deg = {}
    for a, b in E:
        assert tuple(sorted((abs(a[0] - b[0]), abs(a[1] - b[1])))) == (1, 2)
        for p in (a, b):
            assert 0 <= p[0] < n and 0 <= p[1] < n
            deg[p] = deg.get(p, 0) + 1
    assert len(E) == n * n and len(deg) == n * n and set(deg.values()) == {2}
    adj = {}
    for a, b in E: adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    start = (0, 0); prev, cur, k = None, start, 0
    while True:
        nxt = adj[cur][0] if adj[cur][0] != prev else adj[cur][1]
        prev, cur, k = cur, nxt, k + 1
        if cur == start: break
    assert k == n * n, k
    X = len(crossing_list(E))
    n0, g, d = load(orig)
    E0 = {E2(a, b) for a in g for b in g[a]}
    X0 = len(crossing_list(E0))
    F = field_edges(Y0, Y1, s)
    assert F <= E
    a = residues(n, E, range(Y0, Y1 + 1), 'top')
    a0 = residues(n, E0, range(Y0, Y1 + 1), 'top')
    print(f'PASS: closed knight tour n={n}; X = {X} (original {X0}, change {X - X0}); field present on rows '
          f'{Y0}..{Y1} ({Y1 - Y0 + 1} rows); sum a = {sum(a)} (original {sum(a0)})')


if __name__ == '__main__':
    main()
