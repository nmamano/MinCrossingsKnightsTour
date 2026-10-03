"""Calibrate: band-local flux through a sweep cut x+y=a+1/2 vs Structures' current through x=-1/2."""
import json, sys
chi = lambda c: 1 if (c[0] + c[1]) % 2 == 0 else -1
def edges_from_tpl(cells, T, K=8):
    E = set()
    for key, ds in cells.items():
        x, y = map(int, key.split(','))
        for k in range(-K, K + 1):
            u = (x + k * T[0], y + k * T[1])
            for d in ds:
                v = (u[0] + d[0], u[1] + d[1])
                E.add(tuple(sorted([u, v])))
    return E
def flux_cut(E, f, lim):
    """sum over edges crossing level f(c) = t+1/2 (lower end f <= t < upper end) of chi(lower end)."""
    out = {}
    for t in lim:
        s = 0
        for a, b in E:
            lo, hi = (a, b) if f(a) < f(b) else (b, a)
            if f(lo) <= t < f(hi): s += chi(lo)
        out[t] = s
    return out
if __name__ == '__main__':
    d = json.load(open(sys.argv[1])); p = int(sys.argv[2]); T = (p, p)
    for cur, v in d.items():
        E = edges_from_tpl(v['cells'], T)
        # only edges near the origin matter; restrict to edges with both ends within |x|,|y| < 4p
        E = {e for e in E if all(abs(c[0]) < 4 * p and abs(c[1]) < 4 * p for c in e)}
        theirs = flux_cut({e for e in E if abs(e[0][1] - e[0][0]) <= 6}, lambda c: c[0], [-1])[-1]
        mine = flux_cut({e for e in E if abs(e[0][1] - e[0][0]) <= 6 or abs(e[1][1]-e[1][0]) <= 6}, lambda c: c[0] + c[1], range(-2, 4))
        print('current', cur, 'x-cut (band edges)', theirs, 'sweep cuts', mine)
def var_flux(cells, p, w, ts=range(-2, 4)):
    E = edges_from_tpl(cells, (p, p))
    E = {e for e in E if all(abs(c[1] - c[0]) <= w and abs(c[0]) < 4 * p for c in e)}
    return flux_cut(E, lambda c: c[0] + c[1], ts)
