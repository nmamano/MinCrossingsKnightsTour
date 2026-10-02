"""Paste periodic diagonal-band templates into the fold field (KT Structures 2026-10-02)."""
import json
from collections import Counter
from fold3 import build
TPL = {}
def load(p=6, w=3):
    d = json.load(open(f'diag_tpl_p{p}_w{w}.json'))
    out = {}
    for tgt, v in d.items():
        cells = {}
        for key, ds in v['cells'].items():
            x, y = map(int, key.split(','))
            cells[(x, y)] = [tuple(m) for m in ds]
        out[int(tgt)] = cells
    return out
def Rot(p, n, r):
    for _ in range(r):
        p = (n - 1 - p[1], p[0])
    return p
def paste_field(n, t, tgts, flipfun, p=6, w=3, h0=None, a=0, lo=None, hi=None, ts=None):
    """tgts: dict r -> template current (None = no template). Band in BL frame: |y-x-h0|<=w, lo<=x<hi."""
    tpl = load(p, w)
    ts = ts or (t, t, t, t)
    E, deg = build(n, ts=ts, flip=flipfun)
    h = n // 2
    lo = 6 if lo is None else lo
    hi = h - 8 if hi is None else hi
    E = set(E)
    for r, tg in tgts.items():
        if tg is None:
            continue
        cells = tpl[tg] if not isinstance(tg, dict) else tg
        hh = ts[r] if h0 is None else h0
        R = set()
        for x in range(lo, hi):
            for y in range(x + hh - w, x + hh + w + 1):
                R.add((x, y))
        Rb = {Rot(c, n, r) for c in R}
        E = {e for e in E if e[0] not in Rb and e[1] not in Rb}
        for c in R:
            k = (c[0] - a) // p
            u = (c[0] - p * k - a, c[1] - p * k - a - hh)
            for d in cells[u]:
                q = (c[0] + d[0], c[1] + d[1])
                e = tuple(sorted([Rot(c, n, r), Rot(q, n, r)]))
                E.add(e)
    deg = Counter()
    for e in E:
        deg[e[0]] += 1; deg[e[1]] += 1
    return E, deg
