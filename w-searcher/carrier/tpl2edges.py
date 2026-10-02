"""Convert a Structures seam template (cells 'x,y' -> moves, period T=(p,p)) to band.cpp BASE edges."""
import json, sys
def convert(cells, T, sv, hv, w, out):
    LT = sv[0] * T[0] + sv[1] * T[1]
    E = set()
    for key, ds in cells.items():
        x, y = map(int, key.split(','))
        for d in ds:
            v = (x + d[0], y + d[1])
            if not (-w <= hv[0] * v[0] + hv[1] * v[1] <= w): continue     # fixed edge
            a1, b1 = sv[0] * x + sv[1] * y, hv[0] * x + hv[1] * y
            a2, b2 = sv[0] * v[0] + sv[1] * v[1], hv[0] * v[0] + hv[1] * v[1]
            if a1 > a2: a1, b1, a2, b2 = a2, b2, a1, b1
            k = a1 // LT; E.add((a1 - k * LT, b1, a2 - k * LT, b2))
    with open(out, 'w') as f:
        f.write('%d %d\n' % (LT, len(E)))
        for e in sorted(E): f.write('%d %d %d %d\n' % e)
if __name__ == '__main__':
    d = json.load(open(sys.argv[1])); cur = sys.argv[2]; p = int(sys.argv[3]); w = int(sys.argv[4])
    convert(d[cur]['cells'], (p, p), (1, 1), (-1, 1), w, sys.argv[5])
