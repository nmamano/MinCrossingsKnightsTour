"""Extract the optimal periodic corridor from corr_dp (Howard policy cycle) and verify it
independently by unrolling it in a large window with the base field outside."""
import sys, itertools
from collections import Counter
import networkx as nx
from corr_dp import build, make_route
from mmc import prune, howard
from strip_dp import cross
name, W, target = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
states, adj, L = build(name, W, target)
alive = prune(adj); mu, pol, eta = howard(adj, alive)
u0 = next(v for v in eta if eta[v] == mu)
seen = []
while u0 not in seen:
    seen.append(u0); u0 = pol[u0][0]
cyc = seen[seen.index(u0):]
a, off, gl, on, nbrs = make_route(name, W)
gr = 3 if a == 1 else 2
U = list(range(-gl, W + gr))
i0 = next(i for i, c in enumerate(cyc) if states[c][0] == U[0] and states[c][1] == 0)
cyc = cyc[i0:] + cyc[:i0]
rows = len(cyc) // len(U)
P = lambda u, y: (u + a * y + off, y)
edges = []
for step, c in enumerate(cyc):
    u, ypar, es, warm = states[c]
    y = step // len(U)
    nxt = states[pol[c][0]]
    shift = 1 if nxt[0] == U[0] else 0
    for (lu, ly, hu, hy, cc) in nxt[2]:
        if lu == u and ly + shift == 0:
            edges.append((P(lu, y), P(hu, y + hy)))
wsum = sum(pol[c][1] for c in cyc)
print(f'{name} W={W} target={target}: period {rows} rows, crossings/period {wsum} = {mu*L}/row')
print('template (planar edges in one period, y = row along route):')
print(sorted(edges))
# independent check: unroll R periods, base field outside the band
T = (a * rows, rows)
inb = lambda c: 0 <= c[0] - a * c[1] - off < W
R = 8
E = set()
for k in range(R):
    for (p, q) in edges:
        E.add(tuple(sorted([(p[0] + k * T[0], p[1] + k * T[1]), (q[0] + k * T[0], q[1] + k * T[1])])))
ylo, yhi = 0, R * rows
box = [(x, y) for y in range(ylo - 4, yhi + 4) for x in range(a * ylo + off - 14, a * yhi + off + W + 14) if on((x, y))]
for c in box:
    if not inb(c):
        for q in nbrs(c):
            if not inb(q):
                E.add(tuple(sorted([c, q])))
deg = Counter()
for e in E:
    deg[e[0]] += 1; deg[e[1]] += 1
mid = [c for c in box if inb(c) and 2 * rows <= c[1] < (R - 2) * rows]
bad = [c for c in mid if deg[c] != 2]
G = nx.Graph(); G.add_edges_from(e for e in E if inb(e[0]) or inb(e[1]))
cycles = [c for c in nx.cycle_basis(G)]
# crossings attributed to middle periods: count pairs with lower edge-end row in [3*rows, 4*rows)
Eb = [e for e in E if inb(e[0]) or inb(e[1])]
cnt = 0
EE = list(E)
for e in Eb:
    if not (3 * rows <= min(e[0][1], e[1][1]) < 4 * rows):
        continue
    for f in EE:
        if f == e: continue
        if cross((*e[0], *e[1]), (*f[0], *f[1])):
            # count pair once: if f also in Eb and in the attribution window, count only if f > e
            fb = (inb(f[0]) or inb(f[1])) and 3 * rows <= min(f[0][1], f[1][1]) < 4 * rows
            if fb and f < e: continue
            cnt += 1
chi = lambda c: 1 if (c[0] + c[1]) % 2 == 0 else -1
def current(Y):
    return sum(chi(e[0] if e[0][1] < e[1][1] else e[1]) for e in E if min(e[0][1], e[1][1]) < Y <= max(e[0][1], e[1][1]))
print('verify: degree violations', len(bad), '| cycles touching band', len(cycles),
      '| current at rows', [current(Y) for Y in range(3 * rows, 3 * rows + 4)])
# total crossing pairs whose lower-left edge starts in middle periods, all edges
def total(Eset, y0, y1):
    EL = list(Eset); c = 0
    for i, e in enumerate(EL):
        for f in EL[i + 1:]:
            if abs(e[0][1] - f[0][1]) > 3: continue
            if cross((*e[0], *e[1]), (*f[0], *f[1])):
                m_ = min(min(e[0][1], e[1][1]), min(f[0][1], f[1][1]))
                if y0 <= m_ < y1: c += 1
    return c
print('all-edge crossings attributed to periods 3..4:', total(E, 3 * rows, 5 * rows) / 2, 'per period')
for (p, q) in sorted(E):
    pass
