"""Extend a band template (cells 'x,y' -> moves, period T) from width w to width W by adding plain
field cells: side 1 (hv.c < -w) moves +-f1, side 2 (hv.c > w) moves +-f2. Then write band.cpp BASE edges."""
import json, sys
from tpl2edges import convert
def extend(cells, T, hv, w, W, f1, f2):
    out = {k: [tuple(d) for d in v] for k, v in cells.items()}
    dot = lambda a, b: a[0] * b[0] + a[1] * b[1]
    xs = [tuple(map(int, k.split(','))) for k in cells]
    # cells of one period: canonical by the template's own key set range along T
    p = T[0] if T[0] else T[1]; ax = 0 if T[0] else 1
    R = 4 * (W + p + 4)
    for x in range(-R, R + 1):
        for y in range(-R, R + 1):
            c = (x, y)
            if not (0 <= c[ax] < p): continue
            h = dot(hv, c)
            if w < h <= W:
                if f2 is None: continue
                f = f2
            elif -W <= h < -w: f = f1
            else: continue
            out['%d,%d' % c] = [f, (-f[0], -f[1])]
    return out
if __name__ == '__main__':
    src, cur, p, w, W, fn = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
    d = json.load(open(src))
    cells = extend(d[cur]['cells'], (p, p), (-1, 1), w, W, (1, 2), (2, 1))
    convert(cells, (p, p), (1, 1), (-1, 1), W, fn)
