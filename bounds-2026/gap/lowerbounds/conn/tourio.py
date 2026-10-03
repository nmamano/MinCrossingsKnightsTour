"""Load saved tours (w-integrator/tours) as adjacency dicts in (x, y) coordinates, y upward."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
MOV = ((1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2))


def load(name):
    d = json.loads((ROOT / 'w-integrator/tours' / f'{name}.json').read_text())
    n = d['n']
    g = {(x, n - 1 - y): {(x + MOV[int(c)][0], n - 1 - y + MOV[int(c)][1]) for c in d['tour'][y][x]}
         for y in range(n) for x in range(n)}
    return n, g, d


def runs(g, n):
    """Maximal row runs on the left side where columns 0,1 follow mirror-P (M) or P."""
    def pat(y):
        a, b = g[(0, y)], g[(1, y)]
        if a == {(1, y - 2), (2, y - 1)} and b == {(3, y - 1), (0, y + 2)}: return 'M'
        if a == {(1, y + 2), (2, y + 1)} and b == {(3, y + 1), (0, y - 2)}: return 'P'
        return '.'
    s = ''.join(pat(y) for y in range(n))
    out = []; y = 0
    while y < n:
        if s[y] == '.': y += 1; continue
        z = y
        while z < n and s[z] == s[y]: z += 1
        out.append((s[y], y, z - 1)); y = z
    return out
