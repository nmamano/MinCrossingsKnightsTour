"""Helpers for the edge searcher (w-searcher). Imports kt/ read-only."""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kt.strip import Strip
from kt import search
from kt.core import MI, MJ

H16a = ['26 26 36 36 36 36 56 26','23 36 36 36 13 23 23 23','26 26 26 27 27 27 27 26','67 67 67 67 67 67 67 67']
H16b = ['46 46 56 56 56 26 46 46','14 14 14 45 45 45 45 46','05 15 15 15 15 05 05 05','01 01 01 01 01 01 01 01']
VE = ['23 24', '23 24', '02 27', '02 27']   # paper VerticalEdge, left, Q=4

def tile_bottom(tpl, P, D):
    rows = [r.split(' ') for r in tpl]
    p0 = len(rows[0]); assert P % p0 == 0
    rows = [r * (P // p0) for r in rows]
    rows = [['26'] * P for _ in range(D - len(rows))] + rows
    return [' '.join(r) for r in rows]

def tile_left(tpl, Q, D):
    rows = [r.split(' ') for r in tpl]
    q0 = len(rows); assert Q % q0 == 0
    rows = rows * (Q // q0)
    rows = [r + ['26'] * (D - len(r)) for r in rows]
    return [' '.join(r) for r in rows]

def chosen_from_template(st, tpl):
    rows = [r.split(' ') for r in tpl]
    want = set()
    for r, row in enumerate(rows):
        for c, code in enumerate(row):
            if st.kind == 'bottom':
                u = (c, len(rows) - 1 - r)
            else:
                u = (c, len(rows) - 1 - r)
            for m in code:
                d = (MJ[int(m)], -MI[int(m)])
                want.add((u, (u[0] + d[0], u[1] + d[1])))
    return [eid for eid, e in enumerate(st.var_edges) if e in want]

def run(kind, P, D, s=4, off=0, wX=1, wT=0, hint_tpl=None, time_limit=60, workers=2, log=False, **kw):
    st = Strip(kind, P, D, s=s, off=off)
    hint = None
    if hint_tpl is not None:
        hint = set(chosen_from_template(st, hint_tpl))
        print('hint eval', st.evaluate(hint), flush=True)
    r = search.solve(st, wX=wX, wT=wT, time_limit=time_limit, workers=workers, log=log, hint=hint, **kw)
    if 'chosen' in r:
        r['tpl'] = search.to_template(st, r['chosen'])
        del r['chosen']
    r.update(kind=kind, P=P, D=D, s=s, off=off, wX=wX, wT=wT)
    return r
