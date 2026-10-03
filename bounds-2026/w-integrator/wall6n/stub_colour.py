"""Signed stub colour per step for a cut of direction (a,b) through a field (KT Integrator, 2026-10-03).
H = {f > c}, f(p) = a*y - b*x. For each edge of the field with exactly one end in H, add chi(inner end),
chi = (-1)^(x+y). Report the average per step (a,b) over K steps, for c even and odd."""
import sys
from math import gcd
def field_edges(name, p):
    x, y = p
    if name in ('y0', 'y1'):
        val = (x + y) % 2 == int(name[1])
        return [(2, -1), (1, -2)] if val else [(-2, 1), (-1, 2)]
    if name in ('z0', 'z1'):
        val = (x + y) % 2 == int(name[1])
        return [(2, 1), (1, 2)] if val else [(-2, -1), (-1, -2)]
    F = {'21': (2, 1), '12': (1, 2), '2m1': (2, -1), '1m2': (1, -2)}[name]
    return [F, (-F[0], -F[1])]
def per_step(name, a, b, c, K=400):
    f = lambda p: a * p[1] - b * p[0]
    s = 0
    # cells near the line segment: parametrize by t along (a,b) and offset; brute-force box
    R = 6
    seen = set()
    for t in range(K):
        bx, by = t * a, t * b
        for dx in range(-R - abs(b) - 3, R + abs(b) + 4):
            for dy in range(-R - abs(a) - 3, R + abs(a) + 4):
                p = (bx + dx, by + dy)
                if p in seen: continue
                seen.add(p)
                # keep p if its projection along (a,b) falls in [0, K) steps
                proj = (p[0] * a + p[1] * b) / (a * a + b * b)
                if not (0 <= proj < K) or f(p) <= c: continue
                for d in field_edges(name, p):
                    q = (p[0] + d[0], p[1] + d[1])
                    if f(q) <= c: s += 1 if (p[0] + p[1]) % 2 == 0 else -1
    return s / K
if __name__ == '__main__':
    for a, b in [(0, 1), (1, 0), (1, 2), (2, 1), (1, 1), (1, -1), (1, 3), (3, 1), (5, 1), (1, 5), (2, 3)]:
        row = []
        for name in ('z0', 'z1', 'y0', 'y1', '21'):
            row.append(f"{name}:" + '/'.join(f"{per_step(name, a, b, c):+.2f}" for c in (0, 1)))
        print(f"({a},{b})", ' '.join(row))
