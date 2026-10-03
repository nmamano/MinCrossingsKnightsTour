#!/usr/bin/env python3
"""Numeric check of identity (I) in gap/searcher/PLAN.md: X - 4n + 2 = (G + X1 + W3)/2 on a closed tour.
G = uncovered quarters, X1 = crossing pairs whose tiles share exactly one quarter, W3 = sum binom(m-1,2).
Quarters: each unit square [i,i+1]x[j,j+1] split by both diagonals; a quarter is in a tile iff its centroid is.
Usage: python3 check_identity.py TOUR.json   (json with keys n, tour as in gap/lowerbounds/conn/)."""
import sys, json
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from kt.core import edges, crossing_list, validate

def tile_quarters(p, q):
    (x1, y1), (x2, y2) = p, q
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    # short diagonal: the unit grid edge with the same midpoint, perpendicular-ish: along the axis of the odd step
    if abs(dx) == 2: s = (0, 1)    # grid edge vertical through the midpoint
    else: s = (1, 0)
    a = (x1, y1); b = (mx - s[0] / 2, my - s[1] / 2); c = (x2, y2); d = (mx + s[0] / 2, my + s[1] / 2)
    poly = [a, b, c, d]
    def inside(px, py):
        sg = 0
        for k in range(4):
            ux, uy = poly[k]; vx, vy = poly[(k + 1) % 4]
            cr = (vx - ux) * (py - uy) - (vy - uy) * (px - ux)
            if abs(cr) < 1e-12: return False
            s2 = 1 if cr > 0 else -1
            if sg == 0: sg = s2
            elif s2 != sg: return False
        return True
    out = []
    for i in range(int(min(x1, x2)), int(max(x1, x2))):
        for j in range(int(min(y1, y2)), int(max(y1, y2))):
            for k, (cx, cy) in enumerate([(i + .5, j + 1 / 6), (i + 5 / 6, j + .5), (i + .5, j + 5 / 6), (i + 1 / 6, j + .5)]):
                if inside(cx, cy): out.append((i, j, k))
    assert len(out) == 4, (p, q, out)
    return out

def main():
    d = json.load(open(sys.argv[1])); t = d['tour']; n = len(t)
    E = sorted(edges(t)); assert len(E) == n * n
    TQ = {e: set(tile_quarters(*e)) for e in E}
    m = defaultdict(int)
    for e in E:
        for qq in TQ[e]: m[qq] += 1
    nq = 4 * (n - 1) ** 2
    G = nq - len(m); W3 = sum((v - 1) * (v - 2) // 2 for v in m.values() if v >= 1)
    C = crossing_list(E); X = len(C)
    X1 = 0
    for e, f in C:
        k = len(TQ[e] & TQ[f]); assert k in (1, 2), k
        X1 += k == 1
    # sanity: overlap only for crossing pairs (sampled: all pairs sharing a quarter must be crossing pairs)
    pairs = sum(v * (v - 1) // 2 for v in m.values()); assert pairs == sum(len(TQ[e] & TQ[f]) for e, f in C)
    print(f"n={n} X={X} E=X-4n+2={X - 4 * n + 2} G={G} X1={X1} W3={W3} (G+X1+W3)/2={(G + X1 + W3) / 2}")
    assert 2 * (X - 4 * n + 2) == G + X1 + W3
    print("PASS: identity (I) holds exactly")

if __name__ == "__main__":
    main()
