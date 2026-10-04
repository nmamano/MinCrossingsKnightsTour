#!/usr/bin/env python3
"""The left side of the paper's tour (VerticalEdge, 2 turns per row) with the 4 knight paths of one formation
coloured, in the style of band_paths_fig.py (Personal Site Agent, 2026-10-04). Tour: demo/build_data.gen_heel21(48),
the paper's tour with Parker's heels; its left side is the paper's. Lines c = x + 2y 46..49 form one lane; they
turn at the left side into lines 50..53 (46-51, 47-50, 48-53, 49-52).
Output: writeup/turns/images/side_paths.png, and left_band.png for the 16-turn tour (same colours as t16_paths.png).
usage (from the project root): .venv/bin/python writeup/turns/figures/side_paths_fig.py"""
import sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import networkx as nx

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / 'demo'))
from build_data import gen_heel21, gen_TT16
from kt.core import MI, MJ

INK = '#22303a'
COLS = ['#e41a1c', '#2e8b57', '#1f4fe0', '#9b30d9']   # same colours as the heel figures
n = 48

def draw(gen, p0, y0, name):
    grid = gen(n)[0]
    g = {}
    for i, row in enumerate(grid):
        for j, code in enumerate(row):
            x, y = j, n - 1 - i
            g[x, y] = [(x + MJ[int(k)], y - MI[int(k)]) for k in code]
    X0, X1, Y0, Y1 = 0, 14, y0, y0 + 10
    LANE = range(p0, p0 + 4)
    W = {(x, y) for x in range(X0, X1) for y in range(Y0, Y1)}
    G = nx.Graph(); G.add_nodes_from(W)
    for u in W:
        for v in g[u]:
            if v in W: G.add_edge(u, v)
    line = lambda p: p[0] + 2 * p[1]
    paths = [c for c in nx.connected_components(G) if any(line(p) in LANE and p[0] >= 6 for p in c)]
    entry = lambda c: next(line(p) for p in c if line(p) in LANE and p[0] >= 6)
    paths.sort(key=entry)
    assert [entry(c) for c in paths] == list(LANE), [entry(c) for c in paths]

    fig, ax = plt.subplots(figsize=(4.6, 3.4))
    ax.set_xlim(X0 - .9, X1 - .4); ax.set_ylim(Y0 - .6, Y1 - .4); ax.set_aspect('equal'); ax.axis('off')
    for x in range(X0, X1):
        for y in range(Y0, Y1):
            if (x + y) % 2 == 0: ax.add_patch(mp.Rectangle((x - .5, y - .5), 1, 1, color='#eef1f4', lw=0, zorder=0))
    ax.plot([-.5, -.5], [Y0 - .5, Y1 - .5], color=INK, lw=2, zorder=1)          # left side of the board
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
    out = ROOT / 'writeup' / 'turns' / 'images' / name
    fig.savefig(out, bbox_inches='tight', dpi=160, facecolor='white')
    print('wrote', out)


draw(gen_heel21, 46, 18, 'side_paths.png')
# The 16-turn tour: lines 24..27 are the formation coloured in t16_paths.png (band_paths_fig.py); at the left side
# each line c joins line c + 3 or c - 3 (21-24, 25-28, 23-26, 27-30). Rows 7-16, above the 6 x 6 corner.
draw(gen_TT16, 24, 7, 'left_band.png')

