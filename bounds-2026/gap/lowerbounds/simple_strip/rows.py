"""Row-level graph: each arc = one full row (4 cells) between row-boundary states. Saves rows.pkl."""
import pickle, numpy as np
from collections import defaultdict
G = pickle.load(open('gap/lowerbounds/simple_strip/graph.pkl', 'rb'))
states, nodes, src, dst, w, rm = G['states'], G['nodes'], G['src'], G['dst'], G['w'], G['rowmask']
out = defaultdict(list)
for i, s in enumerate(src): out[s].append(i)
bnd = [i for i, (u, m) in enumerate(nodes) if states[u][0] == 0 and m == 0]
bset = set(bnd)
rows = []  # (u, v, W, mask)
for b in bnd:
    stack = [(b, 0)]
    while stack:
        x, W = stack.pop()
        for a in out[x]:
            y = dst[a]
            if y in bset: rows.append((b, y, W + w[a], rm[a]))
            else: stack.append((y, W + w[a]))
print('boundary states', len(bnd), 'row arcs', len(rows))
pickle.dump(dict(bnd=bnd, rows=rows), open('gap/lowerbounds/simple_strip/rows.pkl', 'wb'))
