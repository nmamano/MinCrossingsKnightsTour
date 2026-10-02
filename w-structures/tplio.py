"""Convert board.js-style templates (rows top first, codes (di,dj) with i down) to chosen edge sets."""
import sys
sys.path.insert(0, '/home/nil/nil/knight-formation-research')
from kt.core import MI, MJ
CODE2D = [(MJ[m], -MI[m]) for m in range(8)]
D2CODE = {d: m for m, d in enumerate(CODE2D)}

def chosen_from_cells(st, cellmoves):
    """cellmoves: dict base-cell -> list of (dx,dy). Returns var edge ids."""
    eid = {}
    for i, (u, v) in enumerate(st.var_edges):
        eid[(u, (v[0]-u[0], v[1]-u[1]))] = i
    ch = set()
    for u, ds in cellmoves.items():
        for d in ds:
            if (u, d) in eid:
                ch.add(eid[(u, d)])
            else:
                v = (u[0]+d[0], u[1]+d[1])
                vb, k = st.canon(v)
                key = (vb, (-d[0], -d[1]))
                if key in eid:
                    ch.add(eid[key])
    return sorted(ch)

def bottom_template_cells(tpl):
    rows = [r.split(' ') for r in tpl]
    D = len(rows)
    out = {}
    for r, row in enumerate(rows):
        y = D - 1 - r
        for x, code in enumerate(row):
            out[(x, y)] = [CODE2D[int(c)] for c in code]
    return out

def render(st, dirs, ylist=None):
    """Return text rows of move codes for base cells (any shape): one line per base cell row group."""
    out = []
    for u in sorted(dirs):
        out.append(f'{u}:' + ''.join(str(D2CODE[d]) for d in sorted(dirs[u], key=lambda d: D2CODE[d])))
    return out
