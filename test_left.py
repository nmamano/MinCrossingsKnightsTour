from kt.strip import Strip
from kt.core import MI, MJ
from kt import templates as T
def chosen_left(st, tpl):
    rows = [r.split(' ') for r in tpl]
    Q = len(rows)
    want = set()
    for r, row in enumerate(rows):
        y = Q - 1 - r
        for x, code in enumerate(row):
            for m in code:
                d = (MJ[int(m)], -MI[int(m)])
                want.add(((x, y), (x + d[0], y + d[1])))
    return [eid for eid, (u, v) in enumerate(st.var_edges) if (u, v) in want or any((u2, v2) for (u2, v2) in [] )]
for off in range(8):
    st = Strip('left', 4, 2, off=off)
    ch = chosen_left(st, T.VerticalEdge)
    # wrapped edges: var edge (u, v) with v outside base y-range are stored unrolled; template gives them from u
    try:
        print('off', off, st.evaluate(ch), 'nvar', len(ch))
    except AssertionError as e:
        print('off', off, 'deg problem', e)
    break
