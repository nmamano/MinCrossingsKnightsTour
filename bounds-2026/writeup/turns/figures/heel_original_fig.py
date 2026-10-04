#!/usr/bin/env python3
"""The paper's original heel (Algorithm 1 default heel, kt.templates.Sequence1Default) with the 4 knight paths of the
formation coloured (KT Integrator, 2026-10-03). Tour: demo/build_data.gen_orig(48). Output: writeup/turns/images/
heel_original.png (turns post only; the crossings post keeps its own labelled copy).
usage (from the project root): .venv/bin/python writeup/turns/figures/heel_original_fig.py"""
import shutil, sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import networkx as nx

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / 'demo'))
from build_data import gen_orig
from kt.core import MI, MJ

INK = '#22303a'
COLS = ['#e41a1c', '#2e8b57', '#1f4fe0', '#9b30d9']   # red, green, blue, purple as in formation_moves.png
n = 48
grid = gen_orig(n)[0]
g = {}
for i, row in enumerate(grid):
    for j, code in enumerate(row):
        x, y = j, n - 1 - i
        g[x, y] = [(x + MJ[int(k)], y - MI[int(k)]) for k in code]
X0, X1, Y0, Y1 = 8, 30, 0, 9                 # window (x in [X0, X1), y in [Y0, Y1))
HX = 14                                       # this heel: columns 14..21, rows 0..3
W = {(x, y) for x in range(X0, X1) for y in range(Y0, Y1)}
G = nx.Graph(); G.add_nodes_from(W)
for u in W:
    for v in g[u]:
        if v in W: G.add_edge(u, v)
heel = {(x, y) for x in range(HX, HX + 8) for y in range(4)}
paths = sorted([c for c in nx.connected_components(G) if len(c & heel) >= 7], key=lambda c: min(p[0] for p in c if p[1] == Y1 - 1) if any(p[1] == Y1 - 1 for p in c) else 99)
assert len(paths) == 4 and sum(len(c & heel) for c in paths) == 30, [len(c & heel) for c in paths]

fig, ax = plt.subplots(figsize=(7.6, 3.6))
ax.set_xlim(X0 - .6, X1 - .4); ax.set_ylim(Y0 - .9, Y1 - .4); ax.set_aspect('equal'); ax.axis('off')
for x in range(X0, X1):
    for y in range(Y0, Y1):
        if (x + y) % 2 == 0: ax.add_patch(mp.Rectangle((x - .5, y - .5), 1, 1, color='#eef1f4', lw=0, zorder=0))
ax.add_patch(mp.Rectangle((HX - .5, -.5), 8, 4, fill=False, ec=INK, lw=1.2, ls='--', zorder=1))
ax.plot([X0 - .5, X1 - .5], [-.5, -.5], color=INK, lw=2, zorder=1)          # bottom side of the board
drawn = set()
for u in W:
    for v in g[u]:
        e = tuple(sorted((u, v)))
        if e in drawn or not (u in W or v in W): continue
        drawn.add(e)
        col, lw, z = '#c3ccd4', .8, 2
        for k, c in enumerate(paths):
            if u in c and v in c: col, lw, z = COLS[k], 2.4, 3
        ax.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], color=col, lw=lw, zorder=z, solid_capstyle='round')
for k, c in enumerate(paths):
    ax.plot([p[0] for p in c], [p[1] for p in c], 'o', color=COLS[k], ms=3.5, zorder=4)
out = ROOT / 'writeup' / 'turns' / 'images' / 'heel_original.png'
fig.savefig(out, bbox_inches='tight', dpi=160, facecolor='white')
print('wrote', out, 'heel cells per path:', [len(c & heel) for c in paths])
