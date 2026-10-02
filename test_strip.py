from kt.strip import Strip
from kt.core import MI, MJ
from kt import templates as T
# bottom heel templates: rows listed top (y=3) to bottom (y=0); board.js move m -> (dx,dy) = (MJ[m], -MI[m])
def chosen_from_template(st, tpl):
    rows = [r.split(' ') for r in tpl]
    h = len(rows)
    want = set()
    for r, row in enumerate(rows):
        y = h - 1 - r
        for x, code in enumerate(row):
            for m in code:
                d = (MJ[int(m)], -MI[int(m)])
                want.add(((x, y), (x + d[0], y + d[1])))
    ch = []
    for eid, (u, v) in enumerate(st.var_edges):
        # edge present if template says so from u (u in base) towards v
        if (u, v) in want:
            ch.append(eid)
    return ch
for name, tpl, P in [('opt heel', T.Sequence1Opt, 8), ('default heel', T.Sequence1Default, 8), ('P40', T.SequenceP40, 40)]:
    st = Strip('bottom', P, 4)
    if 'xx' in ' '.join(tpl):
        tpl = [r.replace('xx', '26') for r in tpl]
    ch = chosen_from_template(st, tpl)
    try:
        print(name, 'X,turns per period =', st.evaluate(ch))
    except AssertionError as e:
        print(name, 'degree problem', e)
