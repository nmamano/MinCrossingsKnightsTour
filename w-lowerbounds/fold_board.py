# 8-triangle fold construction: field of out-directions.
import sys
from collections import Counter
def field(n, ts=(0, 0, 0, 0), ms=(0, 0, 0, 0)):
    """ts: diagonal fold offsets per quadrant (BL, BR, TR, TL in rotation order);
    ms: midline offsets: (bottom vertical, right horizontal, top vertical, left horizontal)."""
    h = n // 2
    def rotd(d):
        return (-d[1], d[0])
    v = {}
    for x in range(n):
        for y in range(n):
            lower = y < h + (ms[3] if x < h else ms[1])
            left = x < h + (ms[0] if y < h else ms[2])
            r = {(True, True): 0, (False, True): 1, (False, False): 2, (True, False): 3}[(left, lower)]
            p = (x, y)
            for _ in range(r):
                p = (p[1], n - 1 - p[0])   # inverse rotation
            d = (2, 1) if p[1] > p[0] + ts[r] else (-1, -2)
            for _ in range(r):
                d = rotd(d)
            v[(x, y)] = d
    return v
