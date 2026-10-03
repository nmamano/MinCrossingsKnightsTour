# KT Structures, 2026-10-03. BEYOND5 10 (P5 test): in an H-regime tour, re-pair the ports of one vertical side by the
# P rule (partner(c) = c - 3 for even c, c + 3 for odd c; same side, same sign, steep) and count the cycles of the
# interior edges + collar links. Ports and labels exactly as LB r_b.py / nre_scan.py. A port with no P partner keeps
# its actual collar partner (reported). usage: trap_h.py TOUR.json SIDE...
import sys, json
from pathlib import Path
from collections import defaultdict
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'lowerbounds'/'beyond5'))
import r_b
TS = r_b.TS
f = sys.argv[1]; sides = [int(s) for s in sys.argv[2:]]
n, E = TS.load(f)
Ts = [lambda v: v, lambda v: (n-1-v[0], v[1]), lambda v: (v[1], v[0]), lambda v: (n-1-v[1], v[0])]
inside = lambda v: all(3 <= z <= n-4 for z in v)
adj = defaultdict(set)
for a, b in E: adj[a].add(b); adj[b].add(a)
ports = {}
for a, b in E:
    if inside(a) == inside(b): continue
    o, q = (b, a) if inside(a) else (a, b)
    sd = [i for i, t in enumerate(Ts) if t(o)[0] < 3]
    if len(sd) != 1: continue
    lo, lq = Ts[sd[0]](o), Ts[sd[0]](q); d = (lq[0]-lo[0], lq[1]-lo[1])
    sgn = 1 if d[0]*d[1] > 0 else -1
    ports[(o, q)] = dict(side=sd[0], sgn=sgn, steep=abs(d[0]) == 2, lab=lq[0]-2*lq[1] if sgn == 1 else lq[0]+2*lq[1], row=lo[1])
def partner(o, q):
    prev, cur = q, o
    while True:
        nx = next(v for v in adj[cur] if v != prev); prev, cur = cur, nx
        if inside(cur): return (prev, cur)
# all boundary-crossing edges (including corner ports) with their actual collar partner
cross = {}
for a, b in E:
    if inside(a) != inside(b):
        o, q = (b, a) if inside(a) else (a, b); cross[(o, q)] = partner(o, q)
link = {}
for k, pk in cross.items(): link[k] = pk
for sd in sides:
    idx = {(p['sgn'], p['lab']): k for k, p in ports.items() if p['side'] == sd and p['steep']}
    new = {}; miss = 0
    for k, p in ports.items():
        if p['side'] != sd: continue
        t = (p['sgn'], p['lab'] - 3 if p['lab'] % 2 == 0 else p['lab'] + 3)
        if p['steep'] and t in idx: new[k] = idx[t]
        else: miss += 1
    ok = sum(1 for k, v in new.items() if new.get(v) == k)
    print('side', sd, 'ports', sum(p['side'] == sd for p in ports.values()), 'P-paired', len(new), 'symmetric', ok, 'no P partner', miss)
    for k, v in new.items():
        if new.get(v) == k: link[k] = v
# inner graph: interior edges + links between inner vertices
g = defaultdict(list)
for a, b in E:
    if inside(a) and inside(b): g[a].append(b); g[b].append(a)
for k, v in link.items():
    g[k[1]].append(v[1])
seen = set(); comps = []
for v in list(g):
    if v in seen: continue
    st = [v]; seen.add(v); c = 0
    while st:
        u = st.pop(); c += 1
        for w in g[u]:
            if w not in seen: seen.add(w); st.append(w)
    comps.append(c)
deg = defaultdict(int)
for v in g: deg[len(g[v])] += 1
print(Path(f).name, 'sides re-paired', sides, 'components', len(comps), 'sizes', sorted(comps)[:12], '... max', max(comps), 'degree hist', dict(deg))
# membership of the re-paired side's P pairs, in row order (component index by size rank)
if sides:
    comp = {}; ci = 0
    for v in g:
        if v in comp: continue
        st = [v]; comp[v] = ci
        while st:
            u = st.pop()
            for w in g[u]:
                if w not in comp: comp[w] = ci; st.append(w)
        ci += 1
    sd = sides[0]
    seq = sorted((p['row'], comp[k[1]]) for k, p in ports.items() if p['side'] == sd)
    ids = {}
    print('rows/comp along side', sd, ' '.join(f"{r}:{ids.setdefault(c, len(ids))}" for r, c in seq))
